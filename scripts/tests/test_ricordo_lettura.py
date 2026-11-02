"""Il ricordo dal diario: l'agente nuovo non vede mai il testo, e il master dice la sua serata.

L2 di PIANO-AGENT-SKILLS-ESTERNE (D1 del 2026-10-01). I test fissano le due
cose che il ricordo promette: il pacchetto contiene il diario e non il
modulo, e un master senza intenzione dichiarata e' un rilievo, non un vuoto.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _modulo():
    spec = importlib.util.spec_from_file_location("ricordo_lettura", ROOT / "scripts" / "ricordo_lettura.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RL = _modulo()


class TestRicordo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.corsa = Path(self.tmp.name) / "corsa"
        lettore = self.corsa / "lettore"
        lettore.mkdir(parents=True)
        (lettore / "stato.json").write_text(json.dumps({
            "master": "MODULO.md", "persona": "un DM che conduce stasera", "smesso_a": None,
            "passaggi": [{"titolo": "premessa", "impronta": "x" * 64, "parole": 10}]}), encoding="utf-8")
        (lettore / "diario.jsonl").write_text(json.dumps({
            "passaggio": 1, "titolo": "premessa", "smesso": False,
            "diario": "ago=+1 | mi aspettavo: un assedio | ho trovato: un drago | so adesso: il re vuole il generale"},
            ensure_ascii=False) + "\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_il_pacchetto_ha_il_diario_e_tutte_le_domande(self):
        p = RL.pacchetto_domande(self.corsa / "lettore")
        self.assertIn("il re vuole il generale", p)
        for chiave, _ in RL.DOMANDE:
            self.assertIn(chiave, p)
        self.assertIn("non e' rimasto niente", p)

    def test_la_domanda_al_lettore_risponde_dal_diario(self):
        p = RL.pacchetto_domanda(self.corsa / "lettore", "perché ti sei fermato?")
        self.assertIn("perché ti sei fermato?", p)
        self.assertIn("non l'ho annotato", p)

    def test_tutti_i_lettori(self):
        self.assertEqual(RL.main(["chiedi", str(self.corsa), "tutti", "cosa ricordi?"]), 0)

    def test_una_lettura_non_chiusa_non_da_un_pacchetto(self):
        (self.corsa / "lettore" / "stato.json").unlink()
        self.assertEqual(RL.main(["domande", str(self.corsa / "lettore")]), 1)


class TestIntenzione(unittest.TestCase):
    def test_il_riquadro_vince_sul_quickstart(self):
        fonte, testo = RL.intenzione(ROOT / "07_il Portale Della Forgia Eterna" / "ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md")
        self.assertIn("riquadro", fonte)
        self.assertIn("Zog'tar", testo)
        # dal 2026-10-18 anche DEF-5 apre il §0 col riquadro (riscrittura di stile)
        fonte, testo = RL.intenzione(ROOT / "07_il Portale Della Forgia Eterna" / "ARC07-DEF-5-RITORNO-HAMMERFIST.md")
        self.assertIn("riquadro", fonte)
        self.assertIn("Re Thorek", testo)

    def test_senza_riquadro_si_ripiega_sul_quickstart(self):
        """Il ripiego, su un master che il riquadro non ce l'ha.

        Fino al 2026-10-18 il bersaglio era `ARC07-DEF-5`, che allora apriva
        il §0 senza riquadro. La riscrittura di stile di quel giorno gli ha
        dato «La serata in tre frasi» e ha tenuto tutto il Quickstart (dove
        siete, chi c'e', cosa segnare da DEF-4, cosa stampare, i tempi, dove
        porta): il master non ha perso niente, e' il bersaglio del test che
        non provava piu' il ripiego. Un master vero che oggi non ha il
        riquadro puo' riceverlo domani, quindi il ripiego si prova su un
        master scritto apposta, come il master muto qui sotto; il riquadro
        vero resta provato su DEF-4 e DEF-5 nel test accanto."""
        with tempfile.TemporaryDirectory() as tmp:
            senza = Path(tmp) / "M.md"
            senza.write_text("# Modulo\n\n## §0 — QUICKSTART DM\n\n**Dove siete.** Sulla "
                             "soglia della forgia.\n\n**Chi c'e'.** Il re.\n", encoding="utf-8")
            fonte, testo = RL.intenzione(senza)
        self.assertIn("QUICKSTART", fonte.upper())
        self.assertNotIn("riquadro", fonte)
        self.assertEqual(testo, "**Dove siete.** Sulla soglia della forgia.")

    def test_un_master_senza_intenzione_e_un_rilievo(self):
        with tempfile.TemporaryDirectory() as tmp:
            muto = Path(tmp) / "M.md"
            muto.write_text("# Modulo\n\n### SCENA 1 — Una porta\n\nTesto.\n", encoding="utf-8")
            self.assertEqual(RL.main(["intenzione", str(muto)]), 1)


if __name__ == "__main__":
    unittest.main()
