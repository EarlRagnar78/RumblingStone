"""Test di indice_references.py (L12, ADR-0077 §9)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import indice_references as ir  # noqa: E402


def _lungo(titoli):
    corpo = "".join(f"## {t}\n" + "riga\n" * 40 for t in titoli)
    return "# Titolo\n\nIntro.\n\n" + corpo


class TestLIndice(unittest.TestCase):
    def test_un_file_corto_non_ne_vuole(self):
        self.assertIsNone(ir.indice("# T\n\n## A\n## B\n## C\n"))

    def test_sotto_il_titolo_con_le_sezioni(self):
        t = ir.con_indice(_lungo(["Uno", "Due", "Tre"]))
        righe = t.splitlines()
        self.assertEqual(righe[0], "# Titolo")
        self.assertEqual(righe[2], ir.APRE)
        self.assertIn("- Due", t)
        self.assertIn("Intro.", t)

    def test_idempotente(self):
        una = ir.con_indice(_lungo(["Uno", "Due", "Tre"]))
        self.assertEqual(ir.con_indice(una), una)

    def test_si_aggiorna_quando_cambia_una_sezione(self):
        una = ir.con_indice(_lungo(["Uno", "Due", "Tre"]))
        due = ir.con_indice(una.replace("## Tre", "## Quattro"))
        self.assertIn("- Quattro", due)
        self.assertNotIn("- Tre", due)

    def test_i_titoli_nel_codice_non_contano(self):
        self.assertEqual(ir.titoli("```\n## finto\n```\n## vero\n"), [(2, "vero")])

    def test_il_repo_e_allineato(self):
        self.assertEqual(ir.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
