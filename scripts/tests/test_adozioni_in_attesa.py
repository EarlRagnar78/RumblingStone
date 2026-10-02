"""Il registro delle adozioni rimandate: quando la condizione si accende, il cancello lo dice.

D7 del 2026-10-01: `commit-archaeologist` non si adotta oggi, ma non si perde.
Questi test provano che la condizione accesa su una voce ancora «in attesa»
fa uscire 1, che una spenta lascia passare, e che un registro rotto non passa.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _modulo():
    spec = importlib.util.spec_from_file_location("adozioni_in_attesa",
                                                  ROOT / "scripts" / "adozioni_in_attesa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AD = _modulo()


class TestAdozioniInAttesa(unittest.TestCase):
    def setUp(self):
        self.misure = dict(AD.MISURE)

    def tearDown(self):
        AD.MISURE.clear()
        AD.MISURE.update(self.misure)

    def test_il_registro_del_repo_e_ben_formato(self):
        voci = AD.carica()
        self.assertTrue(any(v["id"] == "commit-archaeologist" for v in voci))
        for v in voci:
            self.assertTrue(v["fonte"].startswith("https://github.com/"), v["id"])
            self.assertEqual(len(v["commit_upstream"]), 40, v["id"])

    def test_una_condizione_accesa_morde(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (True, "finta")
        self.assertEqual(AD.main(["--check"]), 1)

    def test_una_condizione_spenta_passa(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (False, "finta")
        self.assertEqual(AD.main(["--check"]), 0)

    def test_non_misurabile_non_e_spenta_e_non_morde(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (AD.NON_MISURABILE, "finta")
        self.assertEqual(AD.main(["--check"]), 0)

    def test_un_registro_senza_condizione_non_passa(self):
        originale = AD.REGISTRO
        with tempfile.TemporaryDirectory() as tmp:
            rotto = Path(tmp) / "r.json"
            rotto.write_text(json.dumps({"adozioni": [{"id": "x"}]}), encoding="utf-8")
            AD.REGISTRO = rotto
            try:
                self.assertEqual(AD.main(["--check"]), 2)
            finally:
                AD.REGISTRO = originale


if __name__ == "__main__":
    unittest.main()
