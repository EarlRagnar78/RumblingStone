"""Le skill che scrivono contenuto hanno lo stesso blocco vincoli, e nessuna riscrive la grammatica (ADR-0109).

Il DM, 2026-11-07: per regole, skill e agent vale la regola più stringente, e
senza duplicazioni. La grammatica delle marche sta in un posto solo,
`docs/reference/GUIDA-MARCATURE.md`; le skill dove nascono i fatti di gioco hanno
la sezione «Vincoli sui fatti» con lo stesso elenco della guida, parola per
parola. Se la guida cambia, questa prova dice quali skill vanno riallineate.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUIDA = ROOT / "docs" / "reference" / "GUIDA-MARCATURE.md"
SEZIONE = "## Vincoli sui fatti"

# Le skill dove nascono i fatti di gioco (scheda 5 = A).
DI_CONTENUTO = (
    "dnd-35-srd", "pathfinder-1e-srd", "forgotten-realms-lore",
    "npc-villain-boosting", "rumblingstone-campaign",
    "rumblingstone-module-standard", "rumblingstone-narrative-style",
    "rumblingstone-playtest", "rumblingstone-indagine", "rumblingstone-editoria",
)

# Le forme vecchie: una skill che le scrive sta riscrivendo la regola.
FORME_VECCHIE = re.compile(r"needs DM\s+confirmation|\[ACCEPTED|\[INFERRED\]")


def elenco(testo: str) -> str:
    """L'elenco numerato 1-5, a spazi normalizzati."""
    righe = [r[1:].lstrip() if r.startswith(">") else r for r in testo.splitlines()]
    t = "\n".join(righe)
    m = re.search(r"^1\. .*?^5\. .*?(?=\n\s*\n|\Z)", t, re.S | re.M)
    return re.sub(r"\s+", " ", m.group(0)).strip() if m else ""


def sezione(testo: str) -> str:
    i = testo.find(SEZIONE)
    if i < 0:
        return ""
    resto = testo[i + len(SEZIONE):]
    fine = re.search(r"^## ", resto, re.M)
    return resto[:fine.start()] if fine else resto


class TestVincoliDelleSkill(unittest.TestCase):
    def setUp(self):
        guida = GUIDA.read_text(encoding="utf-8")
        i = guida.index("> **Vincoli sui fatti**")
        self.atteso = elenco(guida[i:])
        self.assertTrue(self.atteso, "la guida non ha l'elenco 1-5 del blocco vincoli")

    def test_le_skill_di_contenuto_hanno_il_blocco_della_guida(self):
        for nome in DI_CONTENUTO:
            with self.subTest(skill=nome):
                testo = (ROOT / "skills" / nome / "SKILL.md").read_text(encoding="utf-8")
                s = sezione(testo)
                self.assertIn("GUIDA-MARCATURE.md", s)
                self.assertEqual(elenco(s), self.atteso)

    def test_nessuna_skill_riscrive_la_grammatica_vecchia(self):
        for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=p.parent.name):
                self.assertNotRegex(p.read_text(encoding="utf-8"), FORME_VECCHIE)

    def test_agents_rimanda_alla_guida(self):
        testo = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("docs/reference/GUIDA-MARCATURE.md", testo)
        self.assertNotRegex(testo, r"needs DM\s+confirmation")


if __name__ == "__main__":
    unittest.main()
