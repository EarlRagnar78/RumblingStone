"""Test della policy di visibilità per-PG (dmcore.visibility, Lotto D)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import visibility  # noqa: E402

LOG = (
    "# Session 5 — Split (2026-06-01)\n\n"
    "## Summary\n\npubblico per tutti\n\n"
    "## Next session hooks\n\n- hook pubblico\n\n"
    "## Split — Tordek @ Torneo di Dauth\n\n"
    "**Visto da**: Tordek\n\n"
    "Solo Tordek vede Sethrax mascherato.\n\n"
    "## Split — Hella, Artemis @ Foresta Sacra\n\n"
    "Le due vedono la Quercia Vecchia.\n\n"
    "## DM notes (private — optional)\n\n- segreto assoluto del DM\n"
)


class TestVisibility(unittest.TestCase):
    def test_split_blocks_parsed(self):
        blocks = visibility.split_blocks(LOG)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].pgs, ("Tordek",))
        self.assertEqual(blocks[0].place, "Torneo di Dauth")
        self.assertNotIn("**Visto da**", blocks[0].body)
        self.assertEqual(blocks[1].pgs, ("Hella", "Artemis"))

    def test_for_pg(self):
        self.assertEqual(len(visibility.for_pg(LOG, "tordek")), 1)
        self.assertEqual(len(visibility.for_pg(LOG, "Artemis")), 1)
        self.assertEqual(len(visibility.for_pg(LOG, "Thorik")), 0)
        self.assertIn("Sethrax", visibility.for_pg(LOG, "Tordek")[0].body)

    def test_dm_notes_never_leak(self):
        for blk in visibility.split_blocks(LOG):
            self.assertNotIn("segreto assoluto", blk.body)

    def test_strip_splits(self):
        out = visibility.strip_splits(LOG)
        self.assertNotIn("Sethrax", out)
        self.assertNotIn("Quercia Vecchia", out)
        self.assertIn("pubblico per tutti", out)
        self.assertIn("DM notes", out)  # strip_splits non tocca il resto

    def test_log_without_splits_unchanged(self):
        plain = "# S\n\n## Summary\n\nx\n\n## DM notes\n\n- y\n"
        self.assertEqual(visibility.split_blocks(plain), [])
        self.assertEqual(visibility.strip_splits(plain), plain)


if __name__ == "__main__":
    unittest.main()
