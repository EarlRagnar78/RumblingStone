"""La fedeltà del riscritto (RICERCA-GUARDRAIL §9): le coppie da confrontare,
la correzione automatica e l'aggancio a ciclo_prosa. Il modello NLI è finto:
la scelta delle coppie e la correzione sono deterministiche."""
from __future__ import annotations

import doctest
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import ciclo_prosa as cp  # noqa: E402
import misura_fedelta_nli as fn  # noqa: E402

NORD = "Il drago si alza in volo sopra il campo e si gira verso nord, ruggendo forte.\n"
SUD = "Il drago si alza in volo sopra il campo e si gira verso sud, ruggendo forte.\n"
PIANO = "Il drago si alza piano sopra il campo e si gira verso nord, ruggendo forte.\n"
ALTRO = "\nUna riga che non cambia e resta uguale nei due testi, lunga abbastanza.\n"


class Sud:
    """Il giudice finto: contraddice chi cambia il punto cardinale."""

    def punteggio(self, a: str, b: str) -> float:
        return 0.97 if ("sud" in a) != ("sud" in b) else 0.02


class TestCoppie(unittest.TestCase):

    def test_la_riga_cambiata_si_appaia_alla_sua(self):
        c = fn.coppie(NORD + ALTRO, SUD + ALTRO)
        self.assertEqual([(x["riga"], x["riga_prima"]) for x in c], [(1, 1)])

    def test_righe_uguali_corte_o_tabelle_no(self):
        self.assertEqual(fn.coppie(NORD, NORD), [])
        self.assertEqual(fn.coppie("Corta.\n", "Corto.\n"), [])
        self.assertEqual(fn.coppie("| a | " + NORD.strip() + " |\n", "| a | " + SUD.strip() + " |\n"), [])

    def test_riga_riscritta_del_tutto_non_e_una_coppia(self):
        altra = "Nessuna parola in comune con quella di prima: qui si parla di tutt'altro.\n"
        self.assertEqual(fn.coppie(NORD, altra), [])


class TestRipara(unittest.TestCase):

    def test_la_contraddizione_torna_all_originale(self):
        testo, rimesse = fn.ripara(NORD + ALTRO, SUD + ALTRO, Sud())
        self.assertEqual(testo, NORD + ALTRO)
        self.assertEqual(len(rimesse), 1)

    def test_la_riscrittura_fedele_resta(self):
        testo, rimesse = fn.ripara(NORD + ALTRO, PIANO + ALTRO, Sud())
        self.assertEqual(testo, PIANO + ALTRO)
        self.assertEqual(rimesse, [])

    def test_si_tocca_solo_la_riga_contraddetta(self):
        prima = NORD + ALTRO + NORD.replace("drago", "wyvern")
        dopo = SUD + ALTRO + PIANO.replace("drago", "wyvern")
        testo, _ = fn.ripara(prima, dopo, Sud())
        self.assertEqual(testo, NORD + ALTRO + PIANO.replace("drago", "wyvern"))


class TestCicloProsa(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "ORIG.md", d / "RISC.md"
        self.orig.write_text(NORD + ALTRO, encoding="utf-8")
        self.risc.write_text(SUD + ALTRO, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_la_revisione_non_porta_la_contraddizione_al_dm(self):
        with mock.patch.object(fn, "carica_giudice", return_value=(Sud(), "")):
            testo, _ = cp.revisione(self.orig, self.risc)
        self.assertIn("1 righe contraddicevano l'originale", testo)
        self.assertNotIn("verso sud", testo.split("## Le modifiche")[1])

    def test_misura_boccia_la_contraddizione(self):
        with mock.patch.object(fn, "carica_giudice", return_value=(Sud(), "")), \
                redirect_stdout(io.StringIO()) as out:
            esito = cp.misura_cmd(self.orig, self.risc)
        self.assertEqual(esito, 1)
        self.assertIn("contraddice l'originale", out.getvalue())

    def test_senza_modello_lo_dice(self):
        with mock.patch.object(fn, "carica_giudice", return_value=(None, "manca")):
            testo, _ = cp.revisione(self.orig, self.risc)
        self.assertIn("fedeltà NLI non controllata: manca", testo)


class TestDoctest(unittest.TestCase):

    def test_doctest(self):
        self.assertEqual(doctest.testmod(fn).failed, 0)


if __name__ == "__main__":
    unittest.main()
