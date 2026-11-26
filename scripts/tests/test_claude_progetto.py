"""`scripts/claude-progetto.sh` porta la config Claude del repo nella cartella dei thread (ADR-0140).

Nei thread del progetto Claude parte nella cartella che contiene il clone:
senza questi file non vede CLAUDE.md, hook, skillOverrides né il server
`rumblingstone-tools`. I test lavorano su una copia minima del repo in una
cartella temporanea, mai sulla cartella che contiene il clone vero.
"""
from __future__ import annotations

import json
import os
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
        ambiente = {**os.environ, "HOME": str(self.casa), "RS_SALTA_SKILL": "1"}
        return subprocess.run(["bash", str(self.repo / "scripts" / SCRIPT.name), *argomenti],
                              capture_output=True, text=True, check=True, env=ambiente).stdout

    @property
    def casa(self) -> Path:
        casa = self.tmp / "casa"
        casa.mkdir(exist_ok=True)
        return casa

    def test_configurazione_anche_a_livello_utente(self) -> None:
        # Dal 22/11 i thread ignorano .claude/settings.json della cartella di
        # partenza: hook, plugin spenti e server MCP arrivano solo dal livello
        # utente (misura del 25/11, ADR-0146).
        (self.casa / ".claude.json").write_text(json.dumps({"altro": 1}), encoding="utf-8")
        self.lancia()
        utente = json.loads((self.casa / ".claude" / "settings.json").read_text(encoding="utf-8"))
        originale = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(utente["enabledPlugins"], originale["enabledPlugins"])
        self.assertEqual(set(utente["hooks"]), set(originale["hooks"]))
        comando = utente["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertNotIn("$CLAUDE_PROJECT_DIR", comando)
        ancorate = [r for r in utente["permissions"]["deny"] if r.startswith("Read(/")]
        self.assertTrue(ancorate and all(r.startswith(f"Read(/{self.repo}/") for r in ancorate),
                        "a livello utente le regole ancorate sono assolute (//percorso)")
        stato = json.loads((self.casa / ".claude.json").read_text(encoding="utf-8"))
        self.assertEqual(stato["altro"], 1, "il resto di ~/.claude.json resta com'è")
        argomento = stato["mcpServers"]["rumblingstone-tools"]["args"][0]
        self.assertTrue(Path(argomento).is_absolute() and Path(argomento).is_file())
        prima = (self.casa / ".claude" / "settings.json").read_text(encoding="utf-8")
        self.lancia()
        self.assertEqual((self.casa / ".claude" / "settings.json").read_text(encoding="utf-8"), prima)

    def test_impostazioni_utente_altrui_non_si_toccano(self) -> None:
        (self.casa / ".claude").mkdir()
        (self.casa / ".claude" / "settings.json").write_text("{}\n", encoding="utf-8")
        uscita = self.lancia()
        self.assertEqual((self.casa / ".claude" / "settings.json").read_text(encoding="utf-8"), "{}\n")
        self.assertIn("non sono nostre", uscita)

    def test_i_plugin_nuovi_dell_account_sono_spenti(self) -> None:
        piani = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        for nome in ("superpowers", "agentic-council", "ai-mentor", "frontend-design", "skill-creator"):
            with self.subTest(plugin=nome):
                self.assertIs(piani["enabledPlugins"].get(f"{nome}@synced"), False)

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

    def test_agenti_del_repo_collegati_e_hook_di_vincolo_risolto(self) -> None:
        (self.repo / ".claude" / "agents").mkdir()
        (self.repo / ".claude" / "agents" / "x.md").write_text("---\nname: x\n---\n", encoding="utf-8")
        self.lancia()
        agenti = self.tmp / ".claude" / "agents"
        self.assertTrue(agenti.is_symlink(), "collegamento, così gli agenti restano quelli del repo")
        self.assertTrue((agenti / "x.md").is_file())
        self.lancia()  # il rilancio non rompe il collegamento
        self.assertTrue((agenti / "x.md").is_file())
        impostazioni = json.loads((self.tmp / ".claude" / "settings.json").read_text(encoding="utf-8"))
        comando = impostazioni["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        self.assertNotIn("$CLAUDE_PROJECT_DIR", comando)
        self.assertIn("vincolo_skill.py --hook", comando)
        claude_md = (self.tmp / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("rumblingstone-narrative-style", claude_md)
        self.assertIn("ADR-0146", claude_md)

    def test_agenti_altrui_non_si_toccano(self) -> None:
        (self.repo / ".claude" / "agents").mkdir()
        (self.tmp / ".claude" / "agents").mkdir(parents=True)
        uscita = self.lancia()
        self.assertIn("non è un collegamento nostro", uscita)
        self.assertFalse((self.tmp / ".claude" / "agents").is_symlink())

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
