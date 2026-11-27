"""Ogni skill dichiara i suoi cancelli deterministici, e i cancelli esistono (2026-11-03).

Il DM: «è necessario mettere delle guardrail anche a tutte le skills, anche a
quelle dello stile». Una skill che non dice quale comando la verifica lascia
il controllo alla memoria di chi la usa. Questa prova chiede la sezione e
controlla che ogni comando citato sia uno script vero, dichiarato in
`tools.manifest.json`.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEZIONE = "## Cancelli deterministici"


def sezione(testo: str) -> str:
    i = testo.find(SEZIONE)
    if i < 0:
        return ""
    resto = testo[i + len(SEZIONE):]
    fine = re.search(r"^## ", resto, re.M)
    return resto[:fine.start()] if fine else resto


class TestCancelliDelleSkill(unittest.TestCase):
    def setUp(self):
        man = json.loads((ROOT / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        self.dichiarati = {t["path"] for t in man["tools"]} if isinstance(man, dict) and "tools" in man \
            else {t["path"] for t in man}

    def test_ogni_skill_ha_la_sezione_con_almeno_un_comando(self):
        for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=p.parent.name):
                self.assertRegex(sezione(p.read_text(encoding="utf-8")), r"python3 scripts/\w+\.py")

    def test_ogni_comando_citato_esiste_ed_e_dichiarato(self):
        for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
            for script in re.findall(r"python3 (scripts/\w+\.py)", sezione(p.read_text(encoding="utf-8"))):
                with self.subTest(skill=p.parent.name, script=script):
                    self.assertTrue((ROOT / script).is_file(), script)
                    self.assertTrue(script in self.dichiarati, f"{script} non è in tools.manifest.json")


if __name__ == "__main__":
    unittest.main()
