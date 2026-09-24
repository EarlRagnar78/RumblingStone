"""Test di comportamento del generatore di serie ComfyUI (ADR-0012 §7, ADR-0019).

Coprono le tre cose che, se si rompono, si scoprono troppo tardi: il conteggio
della serie (diciotto, non venti), la ripetibilita' dei seed, e il cancello sui
pesi non commerciali. Tutto stdlib, nessuna rete: i test non parlano con ComfyUI.
"""
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MODULO = REPO / "scripts" / "comfyui_batch.py"
PROMPTS = (
    REPO
    / "STANDALONE-Il-Drappo-di-Tarsilia"
    / "ALLEGATI"
    / "immagini"
    / "PROMPT-RITRATTI-E-TAVOLE.md"
)

spec = importlib.util.spec_from_file_location("comfyui_batch", MODULO)
cb = importlib.util.module_from_spec(spec)
# Registrato prima di eseguirlo: @dataclass risolve le annotazioni differite
# (`from __future__ import annotations`) cercando il modulo in sys.modules.
sys.modules["comfyui_batch"] = cb
spec.loader.exec_module(cb)


class TestLettura(unittest.TestCase):
    def setUp(self):
        self.testo = PROMPTS.read_text(encoding="utf-8")
        self.immagini = cb.leggi_immagini(self.testo)
        self.blocchi = cb.leggi_blocchi(self.testo)

    def test_serie_base_e_diciotto(self):
        """Il capitolato dice diciotto. Se qualcuno ne aggiunge un diciannovesimo
        senza deciderlo, questo test lo dice prima che finisca in stampa."""
        base = [i for i in self.immagini if i.serie == "base"]
        self.assertEqual(len(base), 18, [i.ident for i in base])

    def test_composizione_della_serie(self):
        base = [i for i in self.immagini if i.serie == "base"]
        ritratti = [i for i in base if i.stile == "ritratto"]
        self.assertEqual(len(ritratti), 11, "6 PG + 5 PNG")
        self.assertEqual(len([i for i in base if i.larghezza == 1536]), 3, "3 tavole")
        self.assertEqual(len([i for i in base if i.larghezza == 800]), 2, "2 spot")

    def test_id_unici(self):
        identificativi = [i.ident for i in self.immagini]
        self.assertEqual(len(identificativi), len(set(identificativi)))

    def test_blocchi_condivisi_presenti(self):
        for atteso in ("look-comune", "negativi", "ancora-storica"):
            self.assertIn(atteso, self.blocchi)

    def test_ancora_storica_non_e_senese(self):
        """La scuola si sceglie per la resa, non per il luogo: ancorare a Siena
        rimetterebbe dalla finestra cio' che IP-E-LICENZE §4 ha tolto dalla porta."""
        self.assertNotIn("sienese", self.blocchi["ancora-storica"].lower())
        self.assertIn("flemish", self.blocchi["ancora-storica"].lower())

    def test_nessun_segnaposto_residuo(self):
        """Ogni `[look comune]` scritto nel markdown viene sostituito, non lasciato."""
        for img in self.immagini:
            positivo, _ = cb.componi(img, self.blocchi)
            self.assertNotIn("[look comune]", positivo, img.ident)

    def test_ritratti_portano_look_e_ancora(self):
        vanna = next(i for i in self.immagini if i.ident == "ritratto-vanna")
        positivo, negativo = cb.componi(vanna, self.blocchi)
        self.assertIn("waist-up character sheet portrait", positivo)
        self.assertIn("flemish panel painting light", positivo)
        self.assertIn("watermark", negativo)

    def test_tavole_non_portano_il_look_da_ritratto(self):
        """Il look comune dice «waist-up portrait»: su una veduta e' un difetto."""
        cena = next(i for i in self.immagini if i.ident == "tavola-la-cena")
        positivo, _ = cb.componi(cena, self.blocchi)
        self.assertNotIn("waist-up", positivo)
        self.assertIn("flemish panel painting light", positivo)


class TestSeed(unittest.TestCase):
    def immagine(self, ident="ritratto-vanna", seed=None):
        return cb.Immagine(ident, 832, 1216, "ritratto", "base", "corpo", seed)

    def test_stabile_fra_esecuzioni(self):
        self.assertEqual(self.immagine().seed(0), self.immagine().seed(0))

    def test_diverso_per_immagini_diverse(self):
        self.assertNotEqual(self.immagine("a").seed(0), self.immagine("b").seed(0))

    def test_reroll_cambia_ma_resta_deterministico(self):
        img = self.immagine()
        self.assertNotEqual(img.seed(0), img.seed(1))
        self.assertEqual(img.seed(1), self.immagine().seed(1))

    def test_seed_fissato_ha_la_precedenza(self):
        self.assertEqual(self.immagine(seed=1234).seed(0), 1234)

    def test_reroll_ignora_il_seed_fissato(self):
        """Chiedere esplicitamente un altro tentativo deve poterlo dare anche a
        un'immagine gia' bloccata."""
        self.assertNotEqual(self.immagine(seed=1234).seed(1), 1234)

    def test_dentro_i_limiti_di_comfyui(self):
        self.assertTrue(0 <= self.immagine().seed(0) < 2**31)


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        img = cb.Immagine("x", 832, 1216, "ritratto", "base", "corpo", None)
        self.grafo = cb.workflow(img, "positivo", "negativo", 42, cb.MODELLI["sdxl"])

    def test_nodo_di_salvataggio_presente(self):
        self.assertEqual(self.grafo["9"]["class_type"], "SaveImage")

    def test_seed_e_dimensioni_finiscono_nel_grafo(self):
        self.assertEqual(self.grafo["3"]["inputs"]["seed"], 42)
        self.assertEqual(self.grafo["5"]["inputs"]["width"], 832)
        self.assertEqual(self.grafo["5"]["inputs"]["height"], 1216)

    def test_batch_sempre_uno(self):
        """Su 6 GiB di VRAM un batch e' il modo piu' rapido di esaurire la memoria."""
        self.assertEqual(self.grafo["5"]["inputs"]["batch_size"], 1)


class TestCancelloSuiPesi(unittest.TestCase):
    """ADR-0019 §1: FLUX.1 [dev] non e' sconsigliato, e' rifiutato."""

    def test_flux_dev_rifiutato(self):
        for nome in ("flux1-dev.safetensors", "FLUX.1-dev-fp8.safetensors", "flux-dev.gguf"):
            with self.subTest(nome=nome), contextlib.redirect_stderr(io.StringIO()):
                uscita = cb.main(["--checkpoint", nome, "--solo", "il-drappo"])
                self.assertEqual(uscita, 1)

    def test_modelli_ammessi_dichiarano_la_licenza(self):
        for nome, mod in cb.MODELLI.items():
            with self.subTest(modello=nome):
                self.assertTrue(mod["ammesso"])
                self.assertTrue(mod["licenza"])
                self.assertNotIn("dev", mod["checkpoint"].lower().replace("safetensors", ""))

    def test_lista_non_scrive_nulla(self):
        """Un flag informativo non ha side-effect (ADR-0012 §1)."""
        prima = PROMPTS.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cb.main(["--lista"]), 0)
            self.assertEqual(cb.main(["--dry-run"]), 0)
        self.assertEqual(PROMPTS.read_bytes(), prima)


class TestProvenienza(unittest.TestCase):
    """ADR-0019 §2: senza la riga, l'immagine non si committa."""

    def test_crea_con_intestazione(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PROVENIENZA.txt"
            cb.scrivi_provenienza(p, "a.png", "a.png · SDXL · OpenRAIL++-M · seed 1 · 2026-08-15 · DM")
            testo = p.read_text(encoding="utf-8")
            self.assertIn("ADR-0019", testo)
            self.assertIn("a.png · SDXL", testo)

    def test_rigenerare_sostituisce_invece_di_accodare(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PROVENIENZA.txt"
            cb.scrivi_provenienza(p, "a.png", "a.png · SDXL · L · seed 1 · 2026-08-15 · DM")
            cb.scrivi_provenienza(p, "b.png", "b.png · SDXL · L · seed 2 · 2026-08-15 · DM")
            cb.scrivi_provenienza(p, "a.png", "a.png · SDXL · L · seed 9 · 2026-08-16 · DM")
            righe = [r for r in p.read_text(encoding="utf-8").split("\n") if r.startswith("a.png")]
            self.assertEqual(len(righe), 1)
            self.assertIn("seed 9", righe[0])


class TestFissaSeed(unittest.TestCase):
    def test_scrive_il_seed_senza_toccare_il_prompt(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prompt.md"
            p.write_text(
                "<!-- img id=tal size=832x1216 stile=tavola serie=base -->\n"
                "```\nun prompt qualsiasi\n```\n",
                encoding="utf-8",
            )
            self.assertTrue(cb.fissa_seed(p, "tal", 777))
            testo = p.read_text(encoding="utf-8")
            self.assertIn("seed=777", testo)
            self.assertIn("un prompt qualsiasi", testo)
            self.assertEqual(cb.leggi_immagini(testo)[0].seed_fissato, 777)

    def test_rifissare_non_accumula(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prompt.md"
            p.write_text(
                "<!-- img id=tal size=832x1216 stile=tavola serie=base seed=1 -->\n"
                "```\nprompt\n```\n",
                encoding="utf-8",
            )
            cb.fissa_seed(p, "tal", 2)
            self.assertEqual(p.read_text(encoding="utf-8").count("seed="), 1)
            self.assertEqual(cb.leggi_immagini(p.read_text(encoding="utf-8"))[0].seed_fissato, 2)

    def test_id_assente_non_modifica_il_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prompt.md"
            p.write_text("<!-- img id=tal size=1x1 stile=tavola serie=base -->\n```\nx\n```\n", encoding="utf-8")
            prima = p.read_bytes()
            self.assertFalse(cb.fissa_seed(p, "altro", 5))
            self.assertEqual(p.read_bytes(), prima)


class TestRegistroDegliScarti(unittest.TestCase):
    """Il sesto requisito: il giudizio che butta un'immagine deve lasciare traccia.

    `PROVENIENZA.txt` registra la SCELTA; qui si prova che il repo registra anche
    il RIFIUTO, e soprattutto che **un rifiuto senza motivo non passa** — il
    gate deve mordere, non limitarsi a esistere.
    """

    def _prompt_finto(self, d):
        p = Path(d) / "prompt.md"
        p.write_text(
            "<!-- img id=tal size=832x1216 stile=tavola serie=base -->\n```\nprompt\n```\n",
            encoding="utf-8",
        )
        return p

    def test_reroll_senza_motivo_esce_2_e_non_scrive_niente(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._prompt_finto(d)
            prima = sorted(x.name for x in Path(d).iterdir())
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                codice = cb.main(["--prompts", str(p), "--reroll", "1"])
            self.assertEqual(codice, 2)
            self.assertIn("--motivo", err.getvalue())
            # nessun file nato: il rifiuto senza motivo non deve nemmeno cominciare
            self.assertEqual(sorted(x.name for x in Path(d).iterdir()), prima)

    def test_motivo_di_soli_spazi_non_conta_come_motivo(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._prompt_finto(d)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cb.main(["--prompts", str(p), "--reroll", "2",
                                          "--motivo", "   "]), 2)

    def test_reroll_zero_non_chiede_motivo(self):
        """Il gate riguarda il rifiuto, non la generazione: senza reroll non c'e'
        niente da buttare, e chiedere un motivo sarebbe attrito senza scopo."""
        with tempfile.TemporaryDirectory() as d:
            p = self._prompt_finto(d)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                codice = cb.main(["--prompts", str(p), "--lista"])
            self.assertEqual(codice, 0)
            self.assertNotIn("--motivo", err.getvalue())

    def test_la_riga_porta_id_seed_reroll_e_motivo(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "SCARTI.txt"
            cb.scrivi_scarto(f, "ritratto-vanna", 12345, 0, "tre dita alla mano sinistra")
            testo = f.read_text(encoding="utf-8")
            self.assertIn("ritratto-vanna · seed 12345 · reroll 0 · tre dita alla mano sinistra", testo)
            self.assertIn("OBBLIGATORIO", testo)   # l'intestazione spiega la regola

    def test_rilanciare_lo_stesso_scarto_non_accoda_una_seconda_riga(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "SCARTI.txt"
            cb.scrivi_scarto(f, "tal", 7, 0, "posa sbagliata")
            cb.scrivi_scarto(f, "tal", 7, 0, "posa sbagliata, e la luce viene da destra")
            righe = [r for r in f.read_text(encoding="utf-8").split("\n") if r.startswith("tal ·")]
            self.assertEqual(len(righe), 1)
            self.assertIn("la luce viene da destra", righe[0])

    def test_scarti_diversi_convivono(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "SCARTI.txt"
            cb.scrivi_scarto(f, "tal", 7, 0, "primo")
            cb.scrivi_scarto(f, "tal", 9, 1, "secondo")
            cb.scrivi_scarto(f, "altro", 7, 0, "terzo")
            righe = [r for r in f.read_text(encoding="utf-8").split("\n")
                     if r and not r.startswith("#")]
            self.assertEqual(len(righe), 3)

    def test_la_cartella_viene_creata_se_manca(self):
        """Lo scarto si scrive PRIMA del primo PNG, quindi prima che la cartella esista."""
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "mai-vista" / "SCARTI.txt"
            cb.scrivi_scarto(f, "tal", 1, 0, "motivo")
            self.assertTrue(f.is_file())



if __name__ == "__main__":
    unittest.main()
