"""Test del driver che porta una mappa in Blender (ADR-0012 §7).

Blender non c'è in CI e non ci deve essere: qui si prova **tutto ciò che si può
provare senza una GPU** — la fusione dei rettangoli, le altezze, il ribaltamento
dell'asse, l'esclusione del livello tattico e la degradazione pulita. Quello che
resta dentro `blender/costruisci_mappa.py` è solo ciò che senza `bpy` non esiste.
"""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MODULO = REPO / "scripts" / "render_map_blender.py"
MAPPA = REPO / "STANDALONE-Il-Drappo-di-Tarsilia" / "ALLEGATI" / "mappe" / "tarsilia-la-ruota.json"

spec = importlib.util.spec_from_file_location("render_map_blender", MODULO)
rmb = importlib.util.module_from_spec(spec)
sys.modules["render_map_blender"] = rmb
spec.loader.exec_module(rmb)


class TestFusione(unittest.TestCase):
    """Una griglia 64x46 sono 2.944 cubi: senza fusione Blender la mastica."""

    def test_rettangolo_pieno_diventa_un_solido(self):
        griglia = [list("aaa") for _ in range(4)]
        self.assertEqual(rmb.unisci(griglia), [("a", 0, 0, 3, 4)])

    def test_corse_orizzontali_e_verticali(self):
        griglia = [list("aaabb"), list("aaabb"), list("aaabb")]
        self.assertEqual(sorted(rmb.unisci(griglia)), [("a", 0, 0, 3, 3), ("b", 3, 0, 2, 3)])

    def test_larghezze_diverse_non_si_fondono(self):
        """Due corse dello stesso simbolo ma di larghezza diversa restano due
        solidi: fonderle vorrebbe dire spezzare la corsa più lunga, che è il
        contrario di quello che serve."""
        griglia = [list("aaa"), list("aab")]
        fusi = sorted(rmb.unisci(griglia))
        self.assertEqual(fusi, [("a", 0, 0, 3, 1), ("a", 0, 1, 2, 1), ("b", 2, 1, 1, 1)])

    def test_copertura_completa_senza_sovrapposizioni(self):
        """La proprietà che conta: ogni cella finisce in esattamente un solido."""
        griglia = [list("abbacc"), list("abbacc"), list("aabbcc"), list("dddddd")]
        viste: set[tuple[int, int]] = set()
        for simbolo, x, y, larghezza, profondita in rmb.unisci(griglia):
            for dy in range(profondita):
                for dx in range(larghezza):
                    cella = (x + dx, y + dy)
                    self.assertNotIn(cella, viste, "cella coperta due volte")
                    self.assertEqual(griglia[y + dy][x + dx], simbolo)
                    viste.add(cella)
        self.assertEqual(len(viste), 6 * 4)


class TestAltezze(unittest.TestCase):
    def test_muri_piu_alti_dei_mobili(self):
        self.assertGreater(rmb.altezza("🏰"), rmb.altezza("📦"))

    def test_torre_piu_alta_del_muro(self):
        self.assertGreater(rmb.altezza("🗼"), rmb.altezza("🏰"))

    def test_acqua_e_voragine_sono_scavi(self):
        self.assertLess(rmb.altezza("🟦"), 0)
        self.assertLess(rmb.altezza("🕳"), rmb.altezza("🟦"))

    def test_porta_e_un_varco_non_un_volume(self):
        """Se la porta fosse alta quanto il muro, la pianta perderebbe l'unica
        informazione che una porta porta."""
        self.assertEqual(rmb.altezza("🚪"), 0.0)

    def test_terreni_piatti_restano_piatti(self):
        for simbolo in ("🟩", "🟫", "⬜", "🟨"):
            self.assertEqual(rmb.altezza(simbolo), 0.0, simbolo)

    def test_simbolo_ignoto_non_esplode(self):
        self.assertEqual(rmb.altezza("🦄"), 0.0)


class TestColori(unittest.TestCase):
    def test_il_colore_viene_dal_renderer_svg(self):
        """Una sola fonte di verità per due catene: è il difetto di PROCEDURA.md §7
        evitato per costruzione invece che per disciplina."""
        self.assertEqual(rmb.colore("🏰"), rmb.rms.SYMBOLS["🏰"]["fill"])

    def test_colore_di_ripiego_valido(self):
        self.assertTrue(rmb.colore("🦄").startswith("#"))


class TestPianta(unittest.TestCase):
    def setUp(self):
        self.spec = rmb.cmj.normalize_units(json.loads(MAPPA.read_text(encoding="utf-8")))

    def test_le_unita_escono_sempre(self):
        self.assertEqual(rmb.pianta_sola(self.spec, con_insidie=True)["units"], [])

    def test_le_insidie_escono_di_default_e_si_possono_tenere(self):
        self.assertEqual(rmb.pianta_sola(self.spec, con_insidie=False)["hazards"], [])
        self.assertTrue(rmb.pianta_sola(self.spec, con_insidie=True)["hazards"])

    def test_lo_spec_originale_non_viene_toccato(self):
        rmb.pianta_sola(self.spec, con_insidie=False)
        self.assertTrue(self.spec["units"], "pianta_sola ha mutato lo spec del chiamante")


class TestPiano(unittest.TestCase):
    def piano(self, **override):
        args = rmb.costruisci_parser().parse_args([str(MAPPA)] + list(override.get("argv", [])))
        spec = rmb.cmj.normalize_units(json.loads(MAPPA.read_text(encoding="utf-8")))
        return rmb.piano_di_scena(spec, args)

    def test_nessun_token_fra_i_solidi(self):
        for solido in self.piano()["solidi"]:
            modo = rmb.rms.SYMBOLS.get(solido["simbolo"], {}).get("mode")
            self.assertNotEqual(modo, "unit", solido["simbolo"])

    def test_la_fusione_paga(self):
        piano = self.piano()
        celle = piano["griglia"][0] * piano["griglia"][1]
        self.assertLess(len(piano["solidi"]), celle // 20, "la fusione non sta lavorando")

    def test_il_terreno_di_base_e_incluso(self):
        """Senza, una voragine resterebbe coperta dal piano di appoggio e il passo
        di profondità la leggerebbe piatta."""
        simboli = {s["simbolo"] for s in self.piano()["solidi"]}
        self.assertIn(self.piano()["terreno_base"]["simbolo"], simboli)

    def test_i_solidi_stanno_dentro_la_mappa(self):
        piano = self.piano()
        larghezza = piano["terreno_base"]["larghezza_m"]
        profondita = piano["terreno_base"]["profondita_m"]
        for s in piano["solidi"]:
            self.assertLessEqual(s["x_m"] + s["larghezza_m"], larghezza + 1e-6)
            self.assertLessEqual(s["y_m"] + s["profondita_m"], profondita + 1e-6)

    def test_le_misure_sono_in_metri_non_in_quadretti(self):
        piano = self.piano()
        scala = piano["scala_m_per_quadretto"]
        self.assertAlmostEqual(piano["terreno_base"]["larghezza_m"], piano["griglia"][0] * scala)

    def test_aspetto_del_render_uguale_a_quello_della_mappa(self):
        piano = self.piano()
        atteso = piano["griglia"][1] / piano["griglia"][0]
        reso = piano["render"]["altezza_px"] / piano["render"]["larghezza_px"]
        self.assertAlmostEqual(atteso, reso, places=2)

    def test_lock_di_luce_dichiarato(self):
        luce = self.piano()["luce"]
        self.assertEqual(luce["azimut"], rmb.LUCE_AZIMUT)
        self.assertEqual(luce["elevazione"], rmb.LUCE_ELEVAZIONE)

    def test_profondita_cambia_solo_il_render(self):
        base = self.piano()
        prof = self.piano(argv=["--profondita"])
        self.assertFalse(base["render"]["profondita"])
        self.assertTrue(prof["render"]["profondita"])
        self.assertEqual(base["solidi"], prof["solidi"])


class TestCLI(unittest.TestCase):
    def test_mappa_mancante_e_errore_d_uso(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(rmb.main(["/non/esiste.json"]), 2)

    def test_json_invalido_e_errore_di_dominio(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "rotta.json"
            p.write_text("{non json", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(rmb.main([str(p)]), 1)

    def test_piano_solo_scrive_il_piano_e_non_chiama_blender(self):
        with tempfile.TemporaryDirectory() as d:
            uscita = Path(d) / "x.png"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(rmb.main([str(MAPPA), "-o", str(uscita), "--piano-solo"]), 0)
            piani = list(Path(d).glob("*.piano.json"))
            self.assertEqual(len(piani), 1)
            self.assertFalse(uscita.exists())
            piano = json.loads(piani[0].read_text(encoding="utf-8"))
            self.assertEqual(piano["uscita"], str(uscita.resolve()))

    def test_blender_assente_degrada_pulito_lasciando_il_piano(self):
        """ADR-0019 §4: si dice quale binario manca, si esce con 1, e ciò che era
        già calcolato non si butta."""
        with tempfile.TemporaryDirectory() as d:
            uscita = Path(d) / "x.png"
            errore = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(errore):
                codice = rmb.main([str(MAPPA), "-o", str(uscita), "--blender", "blender-che-non-esiste"])
            self.assertEqual(codice, 1)
            self.assertIn("blender", errore.getvalue().lower())
            self.assertTrue(list(Path(d).glob("*.piano.json")), "il piano è stato buttato")
            self.assertFalse(uscita.exists())


if __name__ == "__main__":
    unittest.main()
