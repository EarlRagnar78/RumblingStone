"""Gli agenti di `.claude/agents/`: tre classi, skill che esistono, verificatori in sola lettura (ADR-0146)."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vincolo_skill as vs  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENTI = sorted((ROOT / ".claude" / "agents").glob("*.md"))
CLASSI = {"Autori", "Tecnici", "Verificatori"}
SKILL = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}


def _frontmatter(f: Path) -> "dict[str, str]":
    m = re.match(r"---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
    return dict(re.findall(r"^(\w+): ?(.*)$", m.group(1), re.M)) if m else {}


class TestAgenti(unittest.TestCase):
    def test_sono_dodici(self) -> None:
        self.assertEqual(len(AGENTI), 12, [f.name for f in AGENTI])

    def test_nome_descrizione_classe_e_skill(self) -> None:
        for f in AGENTI:
            with self.subTest(agente=f.stem):
                fm = _frontmatter(f)
                self.assertEqual(fm.get("name"), f.stem)
                self.assertGreater(len(fm.get("description", "")), 40)
                classe = re.search(r"<!-- Classe: (\w+)", f.read_text(encoding="utf-8"))
                self.assertTrue(classe and classe.group(1) in CLASSI)
                precaricate = vs.precaricate(f.stem)
                self.assertTrue(precaricate, "nessuna skill precaricata")
                self.assertLessEqual(precaricate, SKILL, precaricate - SKILL)
                self.assertFalse({"rumblingstone-narrative-style",
                                  "rumblingstone-prosa-documenti"} <= precaricate,
                                 "le due prose non si mescolano (ADR-0035)")

    def test_i_verificatori_non_scrivono(self) -> None:
        for f in AGENTI:
            if "Classe: Verificatori" not in f.read_text(encoding="utf-8"):
                continue
            with self.subTest(agente=f.stem):
                strumenti = _frontmatter(f).get("tools", "")
                self.assertTrue(strumenti, "un verificatore elenca i suoi strumenti")
                self.assertNotRegex(strumenti, r"\b(Edit|Write|MultiEdit|NotebookEdit)\b")

    def test_ogni_agente_dice_che_documentazione_aggiornare(self) -> None:
        """L'agente della documentazione non interroga gli altri: legge i loro resoconti."""
        for f in AGENTI:
            if f.stem == "autore-documenti":
                continue
            with self.subTest(agente=f.stem):
                self.assertIn("Documentazione da aggiornare:", f.read_text(encoding="utf-8"))

    def test_l_agente_nominato_dall_hook_precarica_la_skill_di_prosa(self) -> None:
        self.assertIn(vs.SKILL_PROSA, vs.precaricate("autore-prosa-gioco"))

    def test_ogni_skill_obbligatoria_ha_un_agente(self) -> None:
        """L0, L1 e L2 di ORCHESTRAZIONE; l'indagine la carica su richiesta l'autore della prosa."""
        obbligatorie = {"rumblingstone-campaign", "rumblingstone-narrative-style",
                        "rumblingstone-prosa-documenti", "rumblingstone-indagine",
                        "rumblingstone-module-standard", "npc-villain-boosting"}
        coperte = set().union(*(vs.precaricate(f.stem) for f in AGENTI))
        self.assertEqual(obbligatorie - coperte, {"rumblingstone-indagine"})
        self.assertIn("rumblingstone-indagine",
                      (ROOT / ".claude/agents/autore-prosa-gioco.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
