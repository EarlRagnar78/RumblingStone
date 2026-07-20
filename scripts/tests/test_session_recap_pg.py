"""Regressione recap (Lotto D/F): il recap di GRUPPO non cambia con i
blocchi Split e non fa mai trapelare Split/DM notes; il recap --pg
contiene SOLO gli split del PG richiesto."""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import session_recap  # noqa: E402

BASE_LOG = (
    "# Session 5 — Il Bivio (2026-06-01)\n\n"
    "**Players present**: Marco (Thorik), Luca (Tordek)\n"
    "**Location**: Blackfens\n"
    "**In-world dates**: from Day 20 to Day 21\n\n"
    "## Summary\n\nIl party si è diviso al bivio del fiume.\n\n"
    "## Key decisions\n\n- Dividersi in due gruppi\n\n"
    "## Next session hooks\n\n- Il ponte crollato a est\n"
)
SPLITS = (
    "\n## Split — Tordek @ Riva nord\n\n**Visto da**: Tordek\n\n"
    "Tordek vede il sigillo segreto di Sethrax.\n"
    "\n## Split — Thorik @ Riva sud\n\nThorik trova la lettera di Brenna.\n"
)
DM = "\n## DM notes (private — optional)\n\n- imboscata pianificata Day 22\n"

MINI_STATE = (
    "# State\n\n## §0 At-a-Glance\n\nx\n\n"
    "## 1. Party — Current Position\n\n"
    "| PC | Class | Location | HP / status | Threads |\n|---|---|---|---|---|\n"
    "| Tordek | Monk | Riva nord | Full | — |\n\n"
    "## 2. Altro\n\nx\n"
)


class TestRecapPg(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.sessions = root / "sessions"
        self.recaps = root / "recaps"
        self.sessions.mkdir()
        (root / "state.md").write_text(MINI_STATE, encoding="utf-8")
        # monkeypatch dei path del modulo (root-based)
        self._saved = (session_recap.SESSIONS_DIR, session_recap.STATE_FILE,
                       session_recap.RECAPS_DIR)
        session_recap.SESSIONS_DIR = self.sessions
        session_recap.STATE_FILE = root / "state.md"
        session_recap.RECAPS_DIR = self.recaps

    def tearDown(self):
        (session_recap.SESSIONS_DIR, session_recap.STATE_FILE,
         session_recap.RECAPS_DIR) = self._saved
        self._tmp.cleanup()

    def _write_log(self, text: str):
        (self.sessions / "2026-06-01_session-5.md").write_text(text, encoding="utf-8")

    def _run(self, *argv) -> str:
        out = self.recaps / "out.md"
        rc = session_recap.main([*argv, "--seed", "7", "--out", str(out)])
        self.assertIsNone(rc)  # main non ritorna codici
        return out.read_text(encoding="utf-8")

    def test_group_recap_identical_with_or_without_splits(self):
        self._write_log(BASE_LOG + DM)
        plain = self._run()
        self._write_log(BASE_LOG + SPLITS + DM)
        with_splits = self._run()
        self.assertEqual(plain, with_splits)  # R5: zero regressioni di gruppo

    def test_group_recap_never_leaks(self):
        self._write_log(BASE_LOG + SPLITS + DM)
        text = self._run()
        for secret in ("Sethrax", "lettera di Brenna", "imboscata"):
            self.assertNotIn(secret, text)

    def test_pg_recap_contains_only_own_split(self):
        self._write_log(BASE_LOG + SPLITS + DM)
        tordek = self._run("--pg", "Tordek")
        self.assertIn("Il tuo cammino — Tordek", tordek)
        self.assertIn("Sethrax", tordek)              # il SUO split
        self.assertNotIn("lettera di Brenna", tordek)  # lo split di Thorik NO
        self.assertNotIn("imboscata", tordek)          # DM notes MAI


if __name__ == "__main__":
    unittest.main()
