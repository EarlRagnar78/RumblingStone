"""`.claudeignore` diventa `permissions.deny` con regole Read (ADR-0142)."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import claudeignore_deny as cd  # noqa: E402


class TestClaudeignoreDeny(unittest.TestCase):
    def test_settings_allineato(self) -> None:
        esito = subprocess.run([sys.executable, str(ROOT / "scripts" / "claudeignore_deny.py"), "--check"],
                               capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_traduzione_gitignore(self) -> None:
        self.assertEqual(cd.regola("build/"), "Read(**/build/**)")
        self.assertEqual(cd.regola("*.hb.md"), "Read(**/*.hb.md)")
        self.assertEqual(cd.regola("scripts/typst/packages/"), "Read(/scripts/typst/packages/**)")
        self.assertEqual(cd.regola("**/rendered/"), "Read(**/rendered/**)")
        self.assertEqual(cd.regola("Bestiario/pregen-pcgen/**/*.js"), "Read(/Bestiario/pregen-pcgen/**/*.js)")

    def test_ogni_voce_e_tradotta_o_esclusa_col_perche(self) -> None:
        voci = cd.voci(cd.SORGENTE.read_text(encoding="utf-8"))
        for esclusa, motivo in cd.ESCLUSE.items():
            self.assertIn(esclusa, voci, f"esclusione senza voce in .claudeignore: {esclusa}")
            self.assertTrue(motivo.strip())
        self.assertEqual(len(cd.regole("\n".join(voci))), len(voci) - len(cd.ESCLUSE))

    def test_lo_stato_delle_skill_resta_leggibile(self) -> None:
        self.assertNotIn("Read(/.claude/.skills-sync-status)", cd.regole(cd.SORGENTE.read_text(encoding="utf-8")))

    def test_negazioni_rifiutate(self) -> None:
        with self.assertRaises(SystemExit):
            cd.voci("build/\n!build/keep.md\n")


if __name__ == "__main__":
    unittest.main()
