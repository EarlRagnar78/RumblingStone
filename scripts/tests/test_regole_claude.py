"""`.claude/rules/rs-*.md` ricavate da AGENTS.md senza perdere nulla (ADR-0141)."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import regole_claude as rc  # noqa: E402


class TestRegoleClaude(unittest.TestCase):
    def test_le_regole_su_disco_sono_allineate_ad_agents(self) -> None:
        esito = subprocess.run([sys.executable, str(ROOT / "scripts" / "regole_claude.py"), "--check"],
                               capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_nessuna_riga_di_agents_va_persa(self) -> None:
        testo = rc.AGENTS.read_text(encoding="utf-8")
        self.assertEqual("".join(c for _, c in rc.sezioni(testo)), testo)
        regole = rc.regole(testo)
        corpi = "".join(regole.values())
        for titolo, corpo in rc.sezioni(testo):
            self.assertIn(corpo, corpi, f"sezione persa: {titolo!r}")

    def test_una_sezione_nuova_senza_regola_ferma_tutto(self) -> None:
        testo = rc.AGENTS.read_text(encoding="utf-8") + "\n## Sezione nuova\n\ntesto\n"
        with self.assertRaises(SystemExit):
            rc.regole(testo)

    def test_il_nucleo_vale_sempre_le_altre_solo_sui_loro_file(self) -> None:
        self.assertEqual(rc.carica("scripts/dm.py"), ["rs-nucleo.md"])
        arco = rc.carica("07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md")
        self.assertIn("rs-campagna.md", arco)
        self.assertNotIn("rs-strumenti-esterni.md", arco)


if __name__ == "__main__":
    unittest.main()
