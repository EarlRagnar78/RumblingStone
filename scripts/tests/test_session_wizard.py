"""Test del wizard di fine sessione (Lotto B): answers-file → log canonico
che gli altri script capiscono (state_sync, update_xp, visibility)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import session_wizard  # noqa: E402
from dmcore import visibility  # noqa: E402
from state_sync import extract_events  # noqa: E402

ANSWERS = {
    "date": "2026-08-01",
    "number": 4,
    "title": "Il Guado dei Non-Morti",
    "players": "Marco (Thorik), Luca (Tordek)",
    "location": "Blackfens",
    "in_world": "from Day 20 to Day 21",
    "summary": ["Il party ha attraversato il guado.", "Poi la palude."],
    "decisions": ["Thorik guida la colonna"],
    "xp_lines": ["Pattuglia (EL 11) → 3.300 / 4"],
    "xp_total": 825,
    "loot": ["Anello +1 → Tordek"],
    "march_clock": "Day 20 → Day 21 (+1)",
    "hooks": ["Voci di razorfiend a est"],
    "dm_notes": ["Segreto: Sal avanza"],
    "splits": [{"pgs": "Tordek", "place": "Riva nord",
                "body": ["Tordek nota impronte drow."]}],
}


class TestSessionWizard(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.repo), "init", "-q", "-b", "main"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "t"], check=True)
        (self.repo / "x").write_text("x")
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "init"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-qb",
                        "campaign-group-test"], check=True)
        self.answers = self.repo / "answers.json"
        self.answers.write_text(json.dumps(ANSWERS), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_wizard_writes_canonical_log(self):
        rc = session_wizard.main(["--answers", str(self.answers),
                                  "--repo-root", str(self.repo)])
        self.assertEqual(rc, 0)
        out = self.repo / "campaign" / "sessions" / "2026-08-01_session-4.md"
        text = out.read_text(encoding="utf-8")

        # header + formato canonico che update_xp/state_sync capiscono
        self.assertIn("# Session 4 — Il Guado dei Non-Morti (2026-08-01)", text)
        self.assertIn("- **Total**: 825 xp a testa", text)
        ev = extract_events(out)
        kinds = [k for k, _, _ in ev["hits"]]
        self.assertIn("march_clock", kinds)  # "Day 20 → Day 21" riconosciuto

        # split e note DM al posto giusto
        blocks = visibility.for_pg(text, "Tordek")
        self.assertEqual(len(blocks), 1)
        self.assertIn("impronte drow", blocks[0].body)
        self.assertEqual(visibility.for_pg(text, "Thorik"), [])
        self.assertIn("## DM notes", text)
        self.assertTrue(text.index("## DM notes") > text.index("## Split"))

        # commit automatico eseguito
        log = subprocess.run(["git", "-C", str(self.repo), "log", "-1", "--format=%s"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("Session 4", log)

    def test_wizard_refuses_overwrite(self):
        self.assertEqual(session_wizard.main(
            ["--answers", str(self.answers), "--repo-root", str(self.repo)]), 0)
        self.assertEqual(session_wizard.main(
            ["--answers", str(self.answers), "--repo-root", str(self.repo)]), 1)

    def test_wizard_blocked_on_main(self):
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-q", "main"], check=True)
        rc = session_wizard.main(["--answers", str(self.answers),
                                  "--repo-root", str(self.repo)])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
