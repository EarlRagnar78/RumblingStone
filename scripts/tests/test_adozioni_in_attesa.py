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
            if v.get("tipo", "esterna") != "esterna":
                continue
            self.assertTrue(v["fonte"].startswith("https://github.com/"), v["id"])
            self.assertEqual(len(v["commit_upstream"]), 40, v["id"])

    def test_i_lotti_interni_dicono_piano_e_decisione(self):
        """R-6 del piano di recupero: un lotto interno rimandato porta il piano e chi ha deciso."""
        lotti = [v for v in AD.carica() if v.get("tipo") == "lotto"]
        self.assertTrue(any(v["id"] == "generatore-lotto-k" for v in lotti))
        for v in lotti:
            self.assertTrue(v["piano"].startswith("plans/"), v["id"])
            self.assertTrue((ROOT / v["piano"].split()[0]).exists(), v["id"])
            self.assertIn("Jfs", v["decisione"], v["id"])

    def test_un_lotto_senza_piano_non_passa(self):
        originale = AD.REGISTRO
        voce = {"id": "x", "tipo": "lotto", "stato": "in attesa", "quando_scatta": "-",
                "condizione": {"misura": "versione_rilasciata", "versione": "9.9.9"}}
        with tempfile.TemporaryDirectory() as tmp:
            rotto = Path(tmp) / "r.json"
            rotto.write_text(json.dumps({"adozioni": [voce]}), encoding="utf-8")
            AD.REGISTRO = rotto
            try:
                self.assertEqual(AD.main(["--check"]), 2)
            finally:
                AD.REGISTRO = originale

    def test_un_tipo_sconosciuto_non_passa(self):
        with self.assertRaises(ValueError):
            originale = AD.REGISTRO
            with tempfile.TemporaryDirectory() as tmp:
                rotto = Path(tmp) / "r.json"
                rotto.write_text(json.dumps({"adozioni": [{"id": "x", "tipo": "boh"}]}), encoding="utf-8")
                AD.REGISTRO = rotto
                try:
                    AD.carica()
                finally:
                    AD.REGISTRO = originale

    def test_la_versione_rilasciata_si_accende_col_changelog(self):
        originale = AD.CHANGELOG
        with tempfile.TemporaryDirectory() as tmp:
            cl = Path(tmp) / "CHANGELOG.md"
            cl.write_text("## [Non rilasciato]\n\n## [1.1.0] - 2026-11-24\n", encoding="utf-8")
            AD.CHANGELOG = cl
            try:
                self.assertIs(AD.versione_rilasciata("1.2.0")[0], False)
                self.assertIs(AD.versione_rilasciata("1.1.0")[0], True)
                # «1.2.0» non si accende su «1.2.01» ne' su una menzione nel testo
                cl.write_text("- prima della [1.2.0]\n## [1.2.01] - x\n", encoding="utf-8")
                self.assertIs(AD.versione_rilasciata("1.2.0")[0], False)
                cl.unlink()
                self.assertEqual(AD.versione_rilasciata("1.2.0")[0], AD.NON_MISURABILE)
            finally:
                AD.CHANGELOG = originale

    def test_il_lotto_k_scatta_al_rilascio_della_1_2_0(self):
        AD.MISURE["versione_rilasciata"] = lambda **_: (True, "finta")
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (False, "finta")
        self.assertEqual(AD.main(["--check"]), 1)

    def test_una_condizione_accesa_morde(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (True, "finta")
        self.assertEqual(AD.main(["--check"]), 1)

    def test_una_condizione_spenta_passa(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (False, "finta")
        AD.MISURE["versione_rilasciata"] = lambda **_: (False, "finta")
        self.assertEqual(AD.main(["--check"]), 0)

    def test_non_misurabile_non_e_spenta_e_non_morde(self):
        AD.MISURE["file_rimaneggiati_senza_storia"] = lambda **_: (AD.NON_MISURABILE, "finta")
        AD.MISURE["versione_rilasciata"] = lambda **_: (AD.NON_MISURABILE, "finta")
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

    def test_la_riga_di_comfyui_si_riconosce_dal_seed(self):
        """Blockbench aspetta una serie vera (Jfs, card del 2026-11-13): righe col seed, non quelle di Gemini."""
        self.assertTrue(AD.RIGA_COMFYUI.match(
            "ritratto-vanna.png · SDXL 1.0 base · OpenRAIL++-M · seed 1234 · 2026-11-20 · DM"))
        self.assertIsNone(AD.RIGA_COMFYUI.match(
            "#   <file> · <modello e versione> · <licenza dei pesi> · seed <n> · <data> · <chi>"))
        self.assertIsNone(AD.RIGA_COMFYUI.match(
            "drappo.png · Gemini 2.5 Flash Image · Google ToS · SEED: NON DISPONIBILE · 2026-08-15 · DM"))


if __name__ == "__main__":
    unittest.main()
