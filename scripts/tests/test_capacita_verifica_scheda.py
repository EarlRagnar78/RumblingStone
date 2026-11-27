"""`verifica_scheda` dichiara nel manifest tutte le capacità dei plugin che legge (ADR-0126)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import sistemi as S  # noqa: E402

RADICE = Path(__file__).resolve().parents[2]


class TestCapacitaDichiarate(unittest.TestCase):
    def test_ogni_capacita_letta_e_nel_manifest(self):
        import verifica_scheda as V
        lette: set[str] = set()
        vera = S.capacita

        def spia(id_, nome, root=None):
            lette.add(nome)
            return vera(id_, nome, root)

        S.capacita = spia
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                V.main(["Bestiario", "--json"])
        finally:
            S.capacita = vera
        manifest = json.loads((RADICE / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        dichiarate = set(next(t for t in manifest["tools"] if t["id"] == "verifica_scheda")["sistema"]["capacita"])
        self.assertGreater(len(lette), 5)
        self.assertEqual(sorted(lette - dichiarate), [], "capacità lette e non dichiarate nel manifest")


if __name__ == "__main__":
    unittest.main()
