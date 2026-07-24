"""Gate di conformita' del manifest dei tool (ADR-0012).

Verifica che scripts/tools.manifest.json sia valido contro lo schema, che ogni
script del repo sia coperto e che gli artefatti generati siano deterministici.
Tutto stdlib (unittest) — gira nella suite CI `unittest discover`.
"""
import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TM_PATH = REPO / "scripts" / "tools_manifest.py"

spec = importlib.util.spec_from_file_location("tools_manifest", TM_PATH)
tm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tm)


class TestManifestConformance(unittest.TestCase):
    def setUp(self):
        self.manifest = tm.load_manifest()
        self.schema = tm._load_json(tm.SCHEMA)

    def test_schema_valid(self):
        errors = tm.validate(self.manifest, self.schema)
        self.assertEqual(errors, [], "manifest non conforme:\n" + "\n".join(errors))

    def test_full_coverage(self):
        problems = tm.coverage(self.manifest)
        self.assertEqual(problems, [], "script scoperti:\n" + "\n".join(problems))

    def test_unique_ids(self):
        ids = [t["id"] for t in self.manifest["tools"]]
        self.assertEqual(len(ids), len(set(ids)), "id duplicati nel manifest")

    def test_exit_code_convention(self):
        # ogni tool CLI dichiara almeno l'exit 0
        for t in self.manifest["tools"]:
            if t["category"] in ("lib", "tests", "J-data-assets"):
                continue
            self.assertIn("0", t.get("exit_codes", {}),
                          f"{t['id']}: manca l'exit code 0")

    def test_paths_exist(self):
        for t in self.manifest["tools"]:
            self.assertTrue((REPO / t["path"]).exists(),
                            f"{t['id']}: path inesistente {t['path']}")


class TestGeneratedArtifactsDeterministic(unittest.TestCase):
    """Rigenerare due volte produce byte identici (no drift)."""

    def test_registry_stable(self):
        m = tm.load_manifest()
        self.assertEqual(tm.emit_registry(m), tm.emit_registry(m))

    def test_markdown_stable(self):
        m = tm.load_manifest()
        self.assertEqual(tm.emit_markdown(m), tm.emit_markdown(m))

    def test_mcp_stable(self):
        m = tm.load_manifest()
        self.assertEqual(tm.emit_mcp(m), tm.emit_mcp(m))

    def test_committed_artifacts_in_sync(self):
        """Gli artefatti committati combaciano col manifest (drift = rosso)."""
        m = tm.load_manifest()
        reg = tm.OUT_DIR / "registry.json"
        if reg.exists():
            self.assertEqual(reg.read_text(encoding="utf-8"), tm.emit_registry(m),
                             "docs/tools/registry.json out-of-sync: "
                             "rigenera con tools_manifest.py --emit-all")


if __name__ == "__main__":
    unittest.main()
