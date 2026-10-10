"""Un master generato da compile_map_json.py è il suo JSON, ricompilato.

Il 2026-10-09 la correzione di M7-C aveva scritto a mano TATTICHE, EVOLUZIONE e
`@taglia`, perché il compilatore scriveva solo i segnaposto: la ricompilazione
successiva le avrebbe cancellate in silenzio. Ora il JSON le porta (`tattiche`,
`evoluzione`, `note_dm`, `taglie`), e questo test boccia un master generato che
non è più quello che il suo JSON produce.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MARCA = "generata da `scripts/compile_map_json.py`"


def coppie() -> list[tuple[Path, Path]]:
    out = []
    for j in sorted(REPO.rglob("*.json")):
        if "_ARCHIVIO" in j.parts or ".git" in j.parts:
            continue
        m = j.with_suffix(".md")
        if m.exists() and MARCA in m.read_text(encoding="utf-8")[:2000]:
            out.append((j, m))
    return out


class TestMasterGenerati(unittest.TestCase):
    def test_ci_sono(self):
        self.assertGreaterEqual(len(coppie()), 18)

    def test_ogni_master_generato_e_il_suo_json_ricompilato(self):
        with tempfile.TemporaryDirectory() as tmp:
            for j, m in coppie():
                with self.subTest(master=str(m.relative_to(REPO))):
                    out = Path(tmp) / "m.md"
                    r = subprocess.run([sys.executable, str(REPO / "scripts" / "compile_map_json.py"),
                                        str(j), "-o", str(out)], capture_output=True, text=True)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    self.assertEqual(out.read_text(encoding="utf-8"), m.read_text(encoding="utf-8"),
                                     "il master è stato toccato a mano: la modifica va nel JSON")


if __name__ == "__main__":
    unittest.main()
