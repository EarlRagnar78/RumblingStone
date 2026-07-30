"""Harness di determinismo (ADR-0012 regola 4).

Per i tool marcati ``determinism.deterministic: true`` che producono un
artefatto verificabile, eseguire due volte deve dare byte identici. Copre qui
la pipeline mappe (compile_map_json), la piu' sensibile al drift.
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
EX = REPO / "scripts" / "examples" / "esempio-accampamento-mano-rossa.json"


def _run(args):
    return subprocess.run([sys.executable, *args], capture_output=True,
                          text=True, cwd=str(REPO))


@unittest.skipUnless(EX.exists(), "esempio mappa assente")
class TestCompileMapJsonDeterministic(unittest.TestCase):
    def test_double_run_identical(self):
        a = _run(["scripts/compile_map_json.py", str(EX)])
        b = _run(["scripts/compile_map_json.py", str(EX)])
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(b.returncode, 0, b.stderr)
        self.assertEqual(a.stdout, b.stdout,
                         "compile_map_json non deterministico su due esecuzioni")


class TestManifestCheckPasses(unittest.TestCase):
    """Il gate di conformita' e' verde (equivalente a `tools_manifest --check`)."""

    def test_check_exit_zero(self):
        r = _run(["scripts/tools_manifest.py", "--check"])
        self.assertEqual(r.returncode, 0,
                         f"tools_manifest --check rosso:\n{r.stdout}\n{r.stderr}")


if __name__ == "__main__":
    unittest.main()
