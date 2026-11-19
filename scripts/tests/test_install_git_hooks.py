"""Il hook pre-push lancia i gate bloccanti e veloci della CI (ADR-0143)."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
COMANDO = "scripts/gate_locale.py --pre-push"


def _ha_pre_commit() -> bool:
    return subprocess.run(["python3", "-c", "import pre_commit"], capture_output=True).returncode == 0


class TestInstallGitHooks(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / "scripts").mkdir()
        shutil.copy(ROOT / "scripts" / "install-git-hooks.sh", self.repo / "scripts")
        shutil.copy(ROOT / ".pre-commit-config.yaml", self.repo)

    def tearDown(self) -> None:
        shutil.rmtree(self.repo, ignore_errors=True)

    def _installa(self, *env: str) -> str:
        r = subprocess.run(["env", *env, "bash", str(self.repo / "scripts" / "install-git-hooks.sh")],
                           capture_output=True, text=True, cwd=self.repo)
        self.assertEqual(r.returncode, 0, r.stderr)
        return (self.repo / ".git" / "hooks" / "pre-push").read_text(encoding="utf-8")

    def test_senza_pre_commit_il_hook_nativo_lancia_il_gate(self) -> None:
        hook = self._installa("RS_HOOK_NATIVO=1")
        self.assertIn(COMANDO, hook)
        self.assertIn("--no-verify", hook, "il hook dice come si salta, consapevolmente")

    @unittest.skipUnless(_ha_pre_commit(), "pre-commit non installato (requirements-dev.txt)")
    def test_con_pre_commit_il_hook_e_quello_del_framework(self) -> None:
        hook = self._installa()
        self.assertIn("pre-commit", hook)

    def test_rilancio_idempotente(self) -> None:
        self.assertEqual(self._installa("RS_HOOK_NATIVO=1"), self._installa("RS_HOOK_NATIVO=1"))

    def test_post_merge_resta(self) -> None:
        self._installa("RS_HOOK_NATIVO=1")
        self.assertTrue((self.repo / ".git" / "hooks" / "post-merge").exists())


class TestConfigPreCommit(unittest.TestCase):
    def test_un_solo_hook_locale_senza_rete_che_lancia_lo_stesso_comando(self) -> None:
        cfg = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
        self.assertEqual([r["repo"] for r in cfg["repos"]], ["local"],
                         "solo hook locali: niente download (il motivo per cui ADR-0099 lo scartava)")
        hooks = cfg["repos"][0]["hooks"]
        self.assertEqual(len(hooks), 1)
        self.assertEqual(hooks[0]["language"], "system")
        self.assertIn(COMANDO, hooks[0]["entry"])
        self.assertEqual(hooks[0]["stages"], ["pre-push"])

    def test_nei_thread_il_hook_si_installa_all_avvio(self) -> None:
        avvio = (ROOT / ".claude" / "hooks" / "session-start.sh").read_text(encoding="utf-8")
        self.assertIn("install-git-hooks.sh", avvio)


if __name__ == "__main__":
    unittest.main()
