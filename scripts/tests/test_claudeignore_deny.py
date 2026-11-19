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

    def test_ogni_voce_e_tradotta_o_leggibile_col_perche(self) -> None:
        testo = cd.SORGENTE.read_text(encoding="utf-8")
        voci = cd.voci(testo)
        leggibili = cd.leggibili(testo)
        for voce, motivo in leggibili.items():
            self.assertIn(voce, voci)
            self.assertTrue(motivo.strip(), f"voce leggibile senza motivo: {voce}")
        self.assertEqual(len(cd.regole(testo)), len(voci) - len(leggibili))

    def test_marca_leggibile_vale_fino_alla_riga_vuota(self) -> None:
        testo = ("# leggibile: si apre apposta\n*.png\n*.pdf\n\nbuild/\n"
                 "# leggibile: stato\n.claude/.stato\n# commento normale\ndist/\n")
        self.assertEqual(cd.leggibili(testo), {"*.png": "si apre apposta", "*.pdf": "si apre apposta",
                                               ".claude/.stato": "stato"})
        self.assertEqual(cd.regole(testo), ["Read(**/build/**)", "Read(**/dist/**)"])

    def test_marca_leggibile_senza_motivo_rifiutata(self) -> None:
        with self.assertRaises(SystemExit):
            cd.leggibili("# leggibile:\n*.png\n")

    def test_le_eccezioni_stanno_nella_fonte(self) -> None:
        # Le eccezioni stanno in .claudeignore, la fonte: lo script non porta
        # una sua tabella di percorsi (test_tabelle boccia chi nomina lo
        # specchio delle skill, ed è così che la tabella di prima è caduta).
        self.assertFalse(hasattr(cd, "ESCLUSE"))

    def test_lo_stato_delle_skill_resta_leggibile(self) -> None:
        self.assertNotIn("Read(/.claude/.skills-sync-status)", cd.regole(cd.SORGENTE.read_text(encoding="utf-8")))

    def test_negazioni_rifiutate(self) -> None:
        with self.assertRaises(SystemExit):
            cd.voci("build/\n!build/keep.md\n")


if __name__ == "__main__":
    unittest.main()
