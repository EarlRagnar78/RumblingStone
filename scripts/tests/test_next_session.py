"""Test di next_session su una fixture minimale: il brief DM contiene
finestre/clock, il teaser player non contiene MAI materiale DM-only."""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import next_session  # noqa: E402

MINI_STATE = (
    "# State\n\n"
    "## §0 Campaign Status At-a-Glance\n\n"
    "| Arc | Fase | Stato | March Clock | PG Lv | Note |\n"
    "|---|---|---|---|---|---|\n"
    "| 08 Battaglia | ✅ | completato | Day 19 | 13 | — |\n"
    "| 09 P1A Quest Hellas | ⬜ | preparato | Day 20-30 window | 13 | Deadline |\n"
    "| 09 P3 Finale | ⬜ | preparato | Day 42 | 14 | — |\n\n"
    "## 1. Party — Current Position & Condition\n\n"
    "| PC | Class | Location | HP / status | Open personal threads |\n"
    "|---|---|---|---|---|\n"
    "| Tordek | Monk | Verso Dauth | Full | Torneo delle Otto Porte |\n"
    "| Hella | Druid | Foresta Sacra | Full | Rito del Cerchio |\n\n"
    "## 3. Active Villain Threads (Countdown Clocks)\n\n"
    "| Villain | Where | Agenda | Clock | Trigger if filled |\n"
    "|---|---|---|---|---|\n"
    "| Zalkatar | Torre | intel | 6/8 | torre mobile |\n"
    "| Sal | strada | profiling | 0/6 | sabotaggio |\n\n"
    "### 2.1 March Clock\n\n"
    "**Current March Day:** **20** (test).\n"
)

MINI_SESSION = (
    "# Session 3 — Test (2026-05-03)\n\n"
    "## Next session hooks\n\n"
    "- La nebbia si addensa verso est\n"
    "- Tordek riceve una missiva da Sorella Maewen\n"
    "- [x] hook già chiuso che non deve comparire\n\n"
    "## DM notes (private — optional)\n\n"
    "- segreto: Sethrax infiltration\n"
)


class TestNextSession(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        (self.repo / "campaign" / "state.md").write_text(MINI_STATE, encoding="utf-8")
        (self.repo / "campaign" / "sessions" / "2026-05-03_session-3.md").write_text(
            MINI_SESSION, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _outputs(self):
        rc = next_session.main(["--hype", "--repo-root", str(self.repo)])
        self.assertEqual(rc, 0)
        out = self.repo / "campaign" / "next"
        brief = next(out.glob("brief-*-DM.md")).read_text(encoding="utf-8")
        teaser = next(out.glob("teaser-*-PLAYERS.md")).read_text(encoding="utf-8")
        return out, brief, teaser

    def test_brief_contents(self):
        _, brief, _ = self._outputs()
        self.assertIn("SOLO DM", brief)
        self.assertIn("P1A Quest Hellas", brief)      # finestra Day 20-30
        self.assertIn("🔴", brief.replace("🟡", "🔴"))  # una urgenza marcata
        self.assertIn("Zalkatar", brief)              # clock 6/8 → soglia
        self.assertNotIn("| Sal |", brief)            # 0/6 lontano dalla soglia
        self.assertIn("Sorella Maewen", brief)
        self.assertNotIn("hook già chiuso", brief)    # - [x] filtrato
        self.assertNotIn("Sethrax", brief)            # DM notes mai lette

    def test_teaser_is_spoiler_safe(self):
        _, _, teaser = self._outputs()
        self.assertIn("Sorella Maewen", teaser)
        self.assertNotIn("hook già chiuso", teaser)
        self.assertNotIn("Sethrax", teaser)
        for rx in next_session.SPOILER_PATTERNS:
            self.assertIsNone(rx.search(teaser),
                              f"pattern DM-only nel teaser: {rx.pattern}")

    def test_hype_vests(self):
        out, _, _ = self._outputs()
        hb = out / "homebrew"
        self.assertTrue(list(hb.glob("brief-*-DM.hb.md")))
        self.assertTrue(list(hb.glob("teaser-*.hb.md")))
        dm_vest = next(hb.glob("brief-*-DM.hb.md")).read_text(encoding="utf-8")
        self.assertIn("MATERIALE DM", dm_vest)


if __name__ == "__main__":
    unittest.main()

MINI_SESSION_4 = (
    "# Session 4 — Seguito (2026-05-10)\n\n"
    "## Summary\n\n"
    "Il party ha raggiunto Sorella Maewen: la missiva della monaca "
    "mezza-elfa portava l'invito al Cerchio.\n\n"
    "## Next session hooks\n\n- Un nuovo hook diverso\n"
)


class TestConsumedHooks(TestNextSession):
    """E2: hook della sessione vecchia raccontato nella successiva → ❓."""

    def test_consumed_annotation(self):
        (self.repo / "campaign" / "sessions" / "2026-05-10_session-4.md").write_text(
            MINI_SESSION_4, encoding="utf-8")
        rc = next_session.main(["--last-n", "2", "--repo-root", str(self.repo)])
        self.assertEqual(rc, 0)
        brief = next((self.repo / "campaign" / "next").glob("brief-*-DM.md")
                     ).read_text(encoding="utf-8")
        # l'hook su Maewen è raccontato nel Summary della sessione 4 → ❓
        i = brief.index("missiva da Sorella Maewen")
        self.assertIn("❓ forse già giocato", brief[i:i + 300])
        # l'hook sulla nebbia NON è stato raccontato → nessuna annotazione
        # (controllo la sola riga dell'hook e quella subito dopo)
        lines = brief.splitlines()
        k = next(i for i, ln in enumerate(lines) if "nebbia si addensa" in ln)
        self.assertNotIn("❓", lines[k])
        self.assertNotIn("forse già giocato", lines[k + 1] if k + 1 < len(lines) else "")
