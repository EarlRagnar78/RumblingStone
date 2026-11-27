"""F0 di PIANO-MOTORE-AGNOSTICO-D20: il censimento è deterministico e non sale (ADR-0112)."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUI = ROOT / "plans" / "esperimenti" / "motore-agnostico-2026-11-08"

_spec = importlib.util.spec_from_file_location("censimento_formule", QUI / "censimento_formule.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)


class TestCensimentoFormule(unittest.TestCase):

    def test_deterministico(self):
        self.assertEqual(C.censisci(), C.censisci())

    def test_nessuna_misura_sale(self):
        rif = json.loads((QUI / "CENSIMENTO.json").read_text(encoding="utf-8"))["misure"]
        for k, v in C.censisci()["misure"].items():
            self.assertLessEqual(v, rif[k], k)

    def test_riconosce_una_formula_e_un_caricamento(self):
        import ast
        t = ast.parse('X = dati("dnd35", "c")\ndef f(dv):\n    """doc"""\n    return 2 + dv // 2\n'
                      'def g(x):\n    return x.attr\n')
        self.assertEqual(C.a1_caricamenti_all_import({"scripts/dmcore/z.py": t}), ['scripts/dmcore/z.py:1 «dnd35»'])
        self.assertEqual(C.a3_formule({"scripts/dmcore/z.py": t}), ["scripts/dmcore/z.py:f"])


if __name__ == "__main__":
    unittest.main()
