"""La gerarchia dell'EL, e da dove viene il numero (rilievo del DM, 2026-09-03).

Il lotto C aveva trovato che `suggest_loot`, quando un file non portava un
`**Combined EL**`, ripiegava su un **10 scritto nel codice** invece di rifiutare.
Il DM ha fatto due osservazioni, e tutte e due erano giuste:

1. nella catena vera l'EL **viene da `suggest_encounter`**, che emette sempre
   `**Combined EL**`, quindi il 10 non si vedeva mai;
2. quando non c'è, il numero si potrebbe guardare nell'avventura — e infatti
   `campaign/state.md` dichiara `**Party APL:** 13` nell'intestazione, fuori
   dalle regioni ``auto:``, e **nessuno dei due strumenti lo leggeva**.
   `suggest_encounter` pretendeva `--el` a ogni chiamata.

Da qui la gerarchia: `--el` → il file → il Party APL → il rifiuto. Questi test
la fissano in tutti e quattro i gradini, perché è l'ordine che conta, non i
singoli valori.

Solo `unittest`.
"""

from __future__ import annotations

import json
import subprocess
import sys
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dmcore.tavolo import APL_RE, leggi_apl, origine_el  # noqa: E402


@contextmanager
def cartella():
    d = Path(tempfile.mkdtemp(prefix="tavolo-"))
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


def stato_finto(d: Path, riga: str) -> Path:
    p = d / "state.md"
    p.write_text(f"# Stato\n\n**Last updated:** 2026-09-03\n{riga}\n\n## §0\n",
                 encoding="utf-8")
    return p


class TestLeggiApl(unittest.TestCase):
    def test_legge_il_valore_dichiarato(self):
        with cartella() as d:
            self.assertEqual(leggi_apl(stato_finto(d, "**Party APL:** 13")), 13.0)

    def test_ignora_la_parentesi_di_contesto(self):
        """La riga vera ha un commento accanto: `13 (ARC-07 D8 — …)`."""
        with cartella() as d:
            riga = "**Party APL:** 13 (ARC-07 D8 — livello reale già raggiunto)"
            self.assertEqual(leggi_apl(stato_finto(d, riga)), 13.0)

    def test_accetta_la_virgola_decimale(self):
        with cartella() as d:
            self.assertEqual(leggi_apl(stato_finto(d, "**Party APL:** 12,5")), 12.5)

    def test_senza_la_riga_torna_None_invece_di_alzare(self):
        with cartella() as d:
            p = d / "state.md"
            p.write_text("# Stato\n\nNessun APL qui.\n", encoding="utf-8")
            self.assertIsNone(leggi_apl(p))

    def test_file_inesistente_torna_None(self):
        with cartella() as d:
            self.assertIsNone(leggi_apl(d / "non-esiste.md"))

    def test_legge_lo_state_vero_del_repo(self):
        """Se qualcuno cambia il formato della riga in state.md, questo cade."""
        self.assertIsNotNone(leggi_apl(),
                             "campaign/state.md non dichiara piu' un `**Party APL:**` "
                             "nel formato che il lettore conosce")


class TestGerarchia(unittest.TestCase):
    """L'ordine di autorità, gradino per gradino."""

    def test_1_esplicito_vince_su_tutto(self):
        with cartella() as d:
            s = stato_finto(d, "**Party APL:** 13")
            self.assertEqual(origine_el(esplicito=17, dal_file=11, state=s).el, 17.0)

    def test_2_il_file_vince_sull_apl(self):
        with cartella() as d:
            s = stato_finto(d, "**Party APL:** 13")
            o = origine_el(dal_file=11, state=s)
            self.assertEqual(o.el, 11.0)
            self.assertIn("file", o.etichetta)

    def test_3_l_apl_e_l_ultimo_numero(self):
        with cartella() as d:
            s = stato_finto(d, "**Party APL:** 13")
            o = origine_el(state=s)
            self.assertEqual(o.el, 13.0)
            self.assertIn("state.md", o.etichetta)

    def test_4_senza_niente_e_un_rifiuto_non_un_numero(self):
        """Il difetto era proprio qui: c'era un 10 al posto del `None`."""
        with cartella() as d:
            p = d / "state.md"
            p.write_text("# Stato senza APL\n", encoding="utf-8")
            self.assertIsNone(origine_el(state=p))

    def test_l_etichetta_dice_sempre_da_dove_viene(self):
        with cartella() as d:
            s = stato_finto(d, "**Party APL:** 13")
            for kw in (dict(esplicito=9), dict(dal_file=9), dict()):
                with self.subTest(kw):
                    self.assertTrue(origine_el(state=s, **kw).etichetta.strip())

    def test_l_apl_avverte_che_non_e_una_scelta_di_regia(self):
        """APL non è EL: il ripiego deve dirlo, o diventa un numero preso sul serio."""
        with cartella() as d:
            o = origine_el(state=stato_finto(d, "**Party APL:** 13"))
            self.assertIn("--el", o.etichetta)


def esegui(script: str, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *argv],
                          capture_output=True, text=True, cwd=str(REPO))


class TestNeiDueStrumenti(unittest.TestCase):
    """La gerarchia dove serve: sulla riga di comando, con l'exit code vero."""

    def test_suggest_encounter_senza_el_ora_parte(self):
        r = esegui("suggest_encounter.py", "--seed", "1")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        self.assertIn("Party APL", r.stderr)

    def test_suggest_encounter_con_el_non_annuncia_niente(self):
        r = esegui("suggest_encounter.py", "--el", "15", "--seed", "1")
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("Party APL", r.stderr)
        self.assertIn("EL 15", r.stdout)

    def test_la_catena_vera_prende_l_el_dal_file_e_tace(self):
        """Il caso normale non deve cambiare: era l'osservazione del DM."""
        with cartella() as d:
            enc = d / "enc.md"
            r = esegui("suggest_encounter.py", "--el", "12", "--seed", "1")
            enc.write_text(r.stdout, encoding="utf-8")
            r2 = esegui("suggest_loot.py", "--from-encounter", str(enc))
            self.assertEqual(r2.returncode, 0, r2.stderr[-300:])
            self.assertNotIn("Party APL", r2.stderr)
            self.assertIn("Combined EL", enc.read_text(encoding="utf-8"))

    def test_un_file_senza_el_usa_l_apl_e_lo_dichiara(self):
        """Prima qui usciva un 10 muto."""
        with cartella() as d:
            vuoto = d / "vuoto.md"
            vuoto.write_text("# Nessuna proposta\n", encoding="utf-8")
            r = esegui("suggest_loot.py", "--from-encounter", str(vuoto))
            self.assertEqual(r.returncode, 0, r.stderr[-300:])
            self.assertIn("Party APL", r.stderr)
            self.assertNotIn("EL 10", r.stdout)

    def test_in_main_nessun_EL_e_scritto_nel_codice(self):
        """Il difetto era un numero letterale in `main()`, non altrove.

        `render_loot()` ha ancora un `else 10` difensivo per il caso `el=None`,
        che dopo la gerarchia non arriva più da nessun chiamante: è morto, ma è
        un clamp di visualizzazione, non una decisione, e toglierlo è un'altra
        cosa. Qui si guarda dove la decisione si prende.
        """
        testo = (SCRIPTS / "suggest_loot.py").read_text(encoding="utf-8")
        corpo = testo[testo.index("def main():"):]
        righe = [r.strip() for r in corpo.splitlines()
                 if "10.0" in r and not r.strip().startswith("#")]
        self.assertEqual(righe, [], f"EL scritto nel codice dentro main(): {righe}")
        self.assertIn("origine_el(", corpo, "main() non usa piu' la gerarchia")


class TestManifestAllineato(unittest.TestCase):
    """I codici dichiarati devono descrivere la gerarchia nuova, non quella vecchia."""

    def _tool(self, tid):
        m = json.loads((SCRIPTS / "tools.manifest.json").read_text(encoding="utf-8"))
        return next(t for t in m["tools"] if t["id"] == tid)

    def test_suggest_loot_dichiara_di_nuovo_il_3_e_ora_e_raggiungibile(self):
        codici = self._tool("suggest_loot")["exit_codes"]
        self.assertIn("3", codici)
        self.assertIn("Party APL", codici["3"])

    def test_i_due_use_case_nominano_l_apl(self):
        for tid in ("suggest_loot", "suggest_encounter"):
            with self.subTest(tid):
                self.assertIn("APL", self._tool(tid)["use_case"])


if __name__ == "__main__":
    unittest.main()
