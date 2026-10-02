"""measure_tokens: il lettore dei file obbligatori, non la misura.

`test_tool_decidono.py` tiene fuori `measure_tokens` di proposito: misura, e un
test sulla misura sarebbe cerimonia. Questo file collauda un'altra cosa, la
logica aggiunta da RIPRESA-PR 4j-3 (2026-09-24): quali file una skill obbliga a
caricare prima della reference, letti dalla sua sezione «load order», e il
fatto che un file mancante sia dichiarato invece di contare 0.

Il difetto che presidia: fino al 2026-09-24 una domanda di campagna risultava
costare circa 5.000 token invece di circa 20.000, perché `state.md` e
`campaign-coherence.md` non erano contati.

Solo `unittest`.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import measure_tokens as mt  # noqa: E402


def conta(testo: str) -> int:
    return max(1, len(testo) // 4)


class TestFileObbligatori(unittest.TestCase):
    def test_la_skill_di_campagna_obbliga_coherence_e_state(self):
        pre = mt.required_preload(mt.SKILLS_DIR / "rumblingstone-campaign")
        nomi = [p.relative_to(REPO).as_posix() for p in pre]
        self.assertIn("skills/rumblingstone-campaign/references/campaign-coherence.md", nomi)
        self.assertIn("campaign/state.md", nomi)

    def test_una_skill_senza_load_order_non_obbliga_niente(self):
        self.assertEqual(mt.required_preload(mt.SKILLS_DIR / "dnd-35-srd"), [])

    def test_il_proprio_skill_md_non_e_un_file_obbligatorio(self):
        for d in sorted(mt.SKILLS_DIR.iterdir()):
            with self.subTest(d.name):
                self.assertNotIn((d / "SKILL.md").resolve(), mt.required_preload(d))

    def test_si_ferma_alla_fine_dell_elenco(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "references").mkdir()
            (d / "references" / "a.md").write_text("x", encoding="utf-8")
            (d / "references" / "b.md").write_text("x", encoding="utf-8")
            (d / "SKILL.md").write_text(
                "# X\n\n**Load order:**\n\n1. `references/a.md`\n2. altro\n\n"
                "Poi, fuori dall'elenco, `references/b.md`.\n",
                encoding="utf-8")
            nomi = [p.name for p in mt.required_preload(d)]
            self.assertEqual(nomi, ["a.md"])


class TestLaDomandaDiCampagnaContaTutto(unittest.TestCase):
    def test_i_file_obbligatori_entrano_nel_conto(self):
        righe, _ = mt.measure_queries(
            [("q", "rumblingstone-campaign", "campaign-party.md")], conta)
        r = righe[0]
        self.assertFalse(r["missing"])
        self.assertGreater(r["tokens_preload"], 0)
        solo_due = mt.total_tokens(
            [mt.SKILLS_DIR / "rumblingstone-campaign" / "SKILL.md",
             mt.SKILLS_DIR / "rumblingstone-campaign" / "references" / "campaign-party.md"],
            conta)
        self.assertGreater(r["tokens_targeted"], solo_due)

    def test_un_file_mancante_e_dichiarato_non_contato_zero(self):
        righe, _ = mt.measure_queries(
            [("q", "rumblingstone-campaign", "non-esiste.md")], conta)
        self.assertTrue(righe[0]["missing"])
        self.assertIn("non-esiste.md", righe[0]["missing"][0])


if __name__ == "__main__":
    unittest.main()
