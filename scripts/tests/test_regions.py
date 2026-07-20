"""Test di dmcore.regions — il contratto di sicurezza di ADR-0007:
fuori dai marker i byte NON cambiano mai."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore.regions import (RegionError, find_regions, replace_region, wrap)  # noqa: E402

DOC = (
    "# Titolo\n"
    "prosa del DM che nessuno tocca\n"
    "<!-- auto:begin key=march-clock -->\n"
    "**Current March Day:** **19** (test).\n"
    "<!-- auto:end key=march-clock -->\n"
    "altra prosa intoccabile\n"
    "<!-- auto:begin key=changelog -->\n"
    "```\n"
    "2026-05-01  init\n"
    "```\n"
    "<!-- auto:end key=changelog -->\n"
    "coda\n"
)


class TestRegions(unittest.TestCase):
    def test_find(self):
        regs = find_regions(DOC)
        self.assertEqual(set(regs), {"march-clock", "changelog"})
        self.assertIn("Current March Day", regs["march-clock"].content(DOC))

    def test_replace_keeps_outside_bytes(self):
        new = replace_region(DOC, "march-clock", "**Current March Day:** **20** (x).\n")
        regs_old, regs_new = find_regions(DOC), find_regions(new)
        # proprietà: tutto ciò che sta fuori dalla regione è byte-identico
        self.assertEqual(DOC[:regs_old["march-clock"].start],
                         new[:regs_new["march-clock"].start])
        self.assertEqual(DOC[regs_old["march-clock"].end:],
                         new[regs_new["march-clock"].end:])
        self.assertIn("**20**", new)
        self.assertNotIn("**19**", new)

    def test_missing_region(self):
        with self.assertRaises(RegionError):
            replace_region(DOC, "inesistente", "x")

    def test_unbalanced_markers(self):
        with self.assertRaises(RegionError):
            find_regions("<!-- auto:begin key=a -->\nsenza chiusura\n")
        with self.assertRaises(RegionError):
            find_regions("<!-- auto:end key=a -->\n")

    def test_duplicate_key(self):
        doc = (wrap("a", "uno\n") + "\n" + wrap("a", "due\n"))
        with self.assertRaises(RegionError):
            find_regions(doc)

    def test_wrap_roundtrip(self):
        doc = "pre\n" + wrap("k", "contenuto\n") + "\npost\n"
        regs = find_regions(doc)
        self.assertEqual(regs["k"].content(doc), "contenuto\n")


if __name__ == "__main__":
    unittest.main()
