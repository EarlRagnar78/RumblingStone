"""`scripts/claude-progetto.sh` porta la config Claude del repo nella cartella dei thread (ADR-0140).

Nei thread del progetto Claude parte nella cartella che contiene il clone:
senza questi file non vede CLAUDE.md, hook, skillOverrides né il server
`rumblingstone-tools`. I test lavorano su una copia minima del repo in una
cartella temporanea, mai sulla cartella che contiene il clone vero.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "claude-progetto.sh"


class TestClaudeProgetto(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "Repo Con Spazio"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / ".claude" / "hooks").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.repo / "scripts" / SCRIPT.name)
        shutil.copy2(ROOT / "scripts" / "mcp_server.py", self.repo / "scripts" / "mcp_server.py")
        shutil.copy2(ROOT / ".claude" / "settings.json", self.repo / ".claude" / "settings.json")
        shutil.copy2(ROOT / ".claude" / "hooks" / "session-start.sh",
                     self.repo / ".claude" / "hooks" / "session-start.sh")
        shutil.copy2(ROOT / ".mcp.json", self.repo / ".mcp.json")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def lancia(self, *argomenti: str) -> str:
        return subprocess.run(["bash", str(self.repo / "scripts" / SCRIPT.name), *argomenti],
                              capture_output=True, text=True, check=True).stdout

    def test_scrive_i_tre_file_con_percorsi_che_esistono(self) -> None:
        self.lancia()
        claude_md = (self.tmp / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Repo Con Spazio/.claude/rules/", claude_md)
        self.assertIn("fase1.py", claude_md)
        self.assertLessEqual(len(claude_md.splitlines()), 10, "il CLAUDE.md resta corto (ADR-0140)")
        self.assertNotIn("@", claude_md, "rimanda, non incorpora")

        impostazioni = json.loads((self.tmp / ".claude" / "settings.json").read_text(encoding="utf-8"))
        originale = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(impostazioni["skillOverrides"], originale["skillOverrides"])
        comando = impostazioni["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertNotIn("$CLAUDE_PROJECT_DIR", comando)
        hook = Path(subprocess.run(["bash", "-c", f"printf %s {comando}"], capture_output=True,
                                   text=True, check=True).stdout)
        self.assertTrue(hook.is_file(), f"l'hook punta a un file che c'è: {comando}")

        ancorate = [r for r in impostazioni["permissions"]["deny"] if r.startswith("Read(/")]
        self.assertTrue(ancorate and all(r.startswith("Read(/Repo Con Spazio/") for r in ancorate),
                        "le regole Read ancorate puntano dentro il repo (ADR-0142)")

        mcp = json.loads((self.tmp / ".mcp.json").read_text(encoding="utf-8"))
        argomento = mcp["mcpServers"]["rumblingstone-tools"]["args"][0]
        self.assertTrue(Path(argomento).is_absolute() and Path(argomento).is_file())

    def test_non_tocca_un_claude_md_altrui_e_rilancio_idempotente(self) -> None:
        (self.tmp / "CLAUDE.md").write_text("mio\n", encoding="utf-8")
        self.lancia()
        self.assertEqual((self.tmp / "CLAUDE.md").read_text(encoding="utf-8"), "mio\n")
        prima = (self.tmp / ".claude" / "settings.json").read_text(encoding="utf-8")
        self.lancia()
        self.assertEqual((self.tmp / ".claude" / "settings.json").read_text(encoding="utf-8"), prima)
        marca = (self.tmp / ".claude" / ".generato-da-rumblingstone").read_text(encoding="utf-8").split()
        self.assertEqual(sorted(marca), [".mcp.json", "settings.json"])

    def test_il_repo_come_destinazione_non_scrive_niente(self) -> None:
        uscita = self.lancia(str(self.repo))
        self.assertIn("repo stesso", uscita)
        self.assertFalse((self.repo / "CLAUDE.md").exists())

    def test_l_hook_trova_il_repo_dal_suo_percorso(self) -> None:
        testo = (ROOT / ".claude" / "hooks" / "session-start.sh").read_text(encoding="utf-8")
        self.assertIn('cd "$(dirname "${BASH_SOURCE[0]}")/../.."', testo)
        self.assertNotIn('cd "${CLAUDE_PROJECT_DIR', testo)


if __name__ == "__main__":
    unittest.main()
