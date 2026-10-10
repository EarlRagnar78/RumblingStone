"""La scheda di una città di Watabou diventa sempre lo stesso URL (R5, D10)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import watabou_citta as W  # noqa: E402

DAUTH = (SCRIPTS.parent / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
         / "Mappe" / "dauth-assedio" / "dauth-pianta.watabou.json")


def _scheda(**parametri):
    return {"generatore": "city", "parametri": {"seed": 7, **parametri}}


class TestUrl(unittest.TestCase):
    def test_lo_stesso_url_per_la_stessa_scheda_in_qualunque_ordine(self):
        a = W.url(_scheda(walls=1, temple=1))
        b = W.url({"generatore": "city", "parametri": {"temple": 1, "walls": 1, "seed": 7}})
        self.assertEqual(a, b)
        self.assertTrue(a.startswith(W.BASE))

    def test_senza_seme_e_un_errore(self):
        with self.assertRaises(ValueError):
            W.url({"generatore": "city", "parametri": {"walls": 1}})

    def test_un_parametro_ignoto_e_un_errore(self):
        with self.assertRaises(ValueError):
            W.url(_scheda(arena=1))

    def test_un_interruttore_vale_zero_o_uno(self):
        with self.assertRaises(ValueError):
            W.url(_scheda(walls=2))

    def test_export_si_aggiunge_in_coda(self):
        self.assertTrue(W.url(_scheda(), "svg").endswith("&export=svg"))

    def test_la_scheda_di_dauth_e_valida(self):
        scheda = W.leggi(DAUTH)
        self.assertIn("seed=1372032", W.url(scheda))

    def test_da_riga_di_comando_una_scheda_rotta_esce_1(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"generatore": "dungeon"}, f)
        r = subprocess.run([sys.executable, str(SCRIPTS / "watabou_citta.py"), f.name],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
