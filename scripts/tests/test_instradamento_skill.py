"""Le frasi del DM raggiungono le skill obbligatorie: il rilevatore e il suo cricchetto.

L8 di PIANO-AGENT-SKILLS-ESTERNE (D6 del 2026-10-01). Fissano il matcher
(elisioni e plurali italiani), la lettura della descrizione, il conflitto fra
le due L1, e il gate che fallisce quando le omissioni superano il tetto.
"""
from __future__ import annotations

import json
import re
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


class TestIlCampione(unittest.TestCase):
    """D10 del 2026-10-01: il campione si verifica, non si conferma a mano."""

    @classmethod
    def setUpClass(cls):
        cls.casi = json.loads(I.CASI.read_text(encoding="utf-8"))["casi"]

    def test_ogni_frase_e_letterale_nella_sua_fonte(self):
        for c in self.casi:
            testo = I.normalizza((ROOT / c["fonte"]).read_text(encoding="utf-8").replace(">", " "))
            self.assertIn(I.normalizza(c["frase"]), testo, c["frase"])

    def test_ogni_frase_e_attribuita_al_dm(self):
        # nella fonte, poco prima della citazione, c'e' il DM: una frase scritta
        # dall'agente dopo «il DM a freddo:» e' gia' entrata una volta per sbaglio
        for c in self.casi:
            testo = (ROOT / c["fonte"]).read_text(encoding="utf-8").replace("\n> ", " ").replace("\n", " ")
            i = testo.find(c["frase"][:25])
            self.assertGreaterEqual(i, 0, c["frase"])
            prima = testo[max(0, i - 120):i]
            self.assertIn("DM", prima, c["frase"])
            self.assertNotIn("DM a freddo", prima, c["frase"])

    def test_le_etichette_rispettano_orchestrazione(self):
        for c in self.casi:
            attese, escluse = set(c["attese"]), set(c.get("escluse", []))
            self.assertLessEqual(attese | escluse, I.OBBLIGATORIE, c["frase"])
            self.assertLessEqual(len(attese & set(I.L1)), 1, c["frase"])
            self.assertFalse(attese & escluse, c["frase"])

    def test_un_nome_proprio_della_campagna_vuole_campaign(self):
        import misura_craft as mc
        nomi = mc._registro_dei_nomi()
        for c in self.casi:
            if any(re.search(r"\b" + re.escape(n) + r"\b", c["frase"]) for n in nomi):
                self.assertIn("rumblingstone-campaign", c["attese"], c["frase"])

    def test_le_due_meta_hanno_casi_e_quasi_casi(self):
        for ins in ("taratura", "verifica"):
            sub = [c for c in self.casi if c["insieme"] == ins]
            self.assertTrue(any(c.get("tipo") == "quasi-caso" for c in sub), ins)
            self.assertTrue(any(c["attese"] for c in sub), ins)

    def test_nessuna_frase_doppia(self):
        frasi = [I.normalizza(c["frase"]) for c in self.casi]
        self.assertEqual(len(frasi), len(set(frasi)))


class TestComportamentale(unittest.TestCase):
    def test_la_maggioranza_decide(self):
        casi = [{"frase": "x", "attese": ["rumblingstone-campaign"], "escluse": ["rumblingstone-prosa-documenti"]}]
        with tempfile.TemporaryDirectory() as d:
            for i, scelte in enumerate((["rumblingstone-campaign"], ["rumblingstone-campaign"], [])):
                (Path(d) / f"run{i}.json").write_text(json.dumps({"1": scelte}), encoding="utf-8")
            r = I.comportamentale(Path(d), casi)
        self.assertEqual((r["attese_caricate"], r["attese_saltate"], r["violazioni"]), (1, 0, 0))

    def test_le_corse_del_repo_si_rileggono(self):
        r = I.comportamentale(ROOT / "plans" / "instradamento" / "comportamentale",
                              json.loads(I.CASI.read_text(encoding="utf-8"))["casi"])
        self.assertEqual(r["corse"], 3)


if __name__ == "__main__":
    unittest.main()
