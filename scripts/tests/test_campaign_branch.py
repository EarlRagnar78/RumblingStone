"""Test della guardia branch-per-gruppo (dmcore.gitio + config) su repo
git temporanei — mai sul repo reale."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import config as cfg  # noqa: E402
from dmcore import gitio  # noqa: E402


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True)


class TestBranchGuard(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _git(self.repo, "init", "-q", "-b", "main")
        _git(self.repo, "config", "user.email", "t@t")
        _git(self.repo, "config", "user.name", "t")
        (self.repo / "x.txt").write_text("x")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-qm", "init")

    def tearDown(self):
        self._tmp.cleanup()

    def test_guard_blocks_protected_branches(self):
        with self.assertRaises(gitio.BranchGuardError):
            gitio.guard_canon_branch(self.repo)

    def test_guard_allows_group_branch(self):
        _git(self.repo, "checkout", "-qb", "campaign-group-test")
        self.assertEqual(gitio.guard_canon_branch(self.repo), "campaign-group-test")

    def test_guard_enforces_expected(self):
        _git(self.repo, "checkout", "-qb", "altro-branch")
        with self.assertRaises(gitio.BranchGuardError):
            gitio.guard_canon_branch(self.repo, expected="campaign-group-test")

    def test_group_config_roundtrip(self):
        self.assertIsNone(cfg.load_group(self.repo))
        cfg.write_group(self.repo, "rumblingstone-dm-gianfranco")
        self.assertEqual(cfg.load_group(self.repo), "rumblingstone-dm-gianfranco")
        self.assertEqual(cfg.group_branch("x"), "campaign-group-x")

    def test_commit_paths_idempotent(self):
        _git(self.repo, "checkout", "-qb", "campaign-group-test")
        (self.repo / "y.txt").write_text("y")
        sha = gitio.commit_paths(self.repo, ["y.txt"], "add y")
        self.assertIsNotNone(sha)
        self.assertIsNone(gitio.commit_paths(self.repo, ["y.txt"], "noop"))


if __name__ == "__main__":
    unittest.main()
