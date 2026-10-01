"""Le frasi del DM raggiungono le skill obbligatorie: il rilevatore e il suo cricchetto.

L8 di PIANO-AGENT-SKILLS-ESTERNE (D6 del 2026-10-01). Fissano il matcher
(elisioni e plurali italiani), la lettura della descrizione, il conflitto fra
le due L1, e il gate che fallisce quando le omissioni superano il tetto.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import instradamento_skill as I  # noqa: E402

SKILL = {
    "rumblingstone-indagine": ["mistero"],
    "rumblingstone-module-standard": ["avventura"],
    "rumblingstone-narrative-style": ["prosa"],
    "rumblingstone-prosa-documenti": ["documentazione"],
}


class TestMatcher(unittest.TestCase):
    def test_l_elisione_si_stacca(self):
        self.assertIn("rumblingstone-module-standard", I.raggiunte("l'avventura è completa?", SKILL))

    def test_il_plurale_italiano(self):
        self.assertIn("rumblingstone-indagine", I.raggiunte("misteri non banali", SKILL))

    def test_la_radice_non_prende_parole_diverse(self):
        self.assertNotIn("rumblingstone-indagine", I.raggiunte("misteriosamente", SKILL))

    def test_il_trigger_lungo_e_intero(self):
        skill = {"x": [I.normalizza("crea la quest")]}
        self.assertIn("x", I.raggiunte("Crea la quest del ponte", skill))
        self.assertNotIn("x", I.raggiunte("crea la questione", skill))


class TestDescrizione(unittest.TestCase):
    def test_lo_scalare_piegato(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "SKILL.md"
            f.write_text('---\nname: x\ndescription: >\n  Fa cose. Trigger on "uno",\n  «due».\nother: 1\n---\n# x\n', encoding="utf-8")
            self.assertEqual(I.trigger(I.descrizione(f)), ["uno", "due"])

    def test_le_descrizioni_vere_hanno_trigger(self):
        skill = I.tutte_le_skill()
        self.assertEqual(len(skill), 18)
        self.assertTrue(skill["rumblingstone-campaign"])


class TestGate(unittest.TestCase):
    def _casi(self, d, casi, tetto):
        p = Path(d) / "casi.json"
        p.write_text(json.dumps({"tetto_omissioni": tetto, "casi": casi}), encoding="utf-8")
        return p

    def test_conflitto_fra_le_due_l1(self):
        r = I.misura([{"frase": "prosa e documentazione", "attese": []}], SKILL)
        self.assertTrue(r[0]["conflitto_l1"])

    def test_sopra_il_tetto_fallisce(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._casi(d, [{"frase": "niente di niente", "attese": ["rumblingstone-campaign"]}], 0)
            self.assertEqual(I.main(["--check", "--casi", str(p)]), 1)

    def test_senza_tetto_fallisce(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._casi(d, [], None)
            self.assertEqual(I.main(["--check", "--casi", str(p)]), 1)

    def test_il_repo_sta_sotto_il_tetto(self):
        self.assertEqual(I.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
