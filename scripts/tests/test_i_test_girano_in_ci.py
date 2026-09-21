"""Che i test girino davvero in CI, e non solo sulla macchina di chi li scrive.

🔴 **Il difetto che presidia, misurato il 2026-09-21.** La CI esegue
`python -m unittest discover -s scripts/tests` e **pytest non e' installato**
(ADR-0037, stdlib-only; `PIANO-QUALITA-DEL-CODICE` lotto 0 dice esplicitamente
no a pytest come dipendenza). Tre file di test nuovi erano scritti in stile
pytest:

  * due importavano `pytest` -> in CI il modulo **non si importava**, e la
    build e' diventata rossa (`ModuleNotFoundError`, run 35567918916);
  * uno era fatto di **funzioni nude**, che `unittest discover` importa senza
    eseguire -> in CI girava a vuoto, **in silenzio**, che e' peggio del rosso.

Il conto: in locale `pytest` vedeva 966 prove, la CI ne eseguiva **942**.
Ventiquattro prove scritte, nessuna eseguita dove conta. Questo file rende
quel divario impossibile da ripetere senza accorgersene.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "scripts" / "tests"


def file_di_test() -> "list[Path]":
    return sorted(p for p in TESTS.glob("test_*.py"))


class TestOgniTestEEseguibileDaUnittest(unittest.TestCase):

    def test_nessun_file_importa_pytest(self):
        """ADR-0037: la CI non ha pytest, e un import lo scopre solo da rossa."""
        colpevoli = []
        for f in file_di_test():
            albero = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            for nodo in ast.walk(albero):
                if isinstance(nodo, ast.Import):
                    if any(a.name.split(".")[0] == "pytest" for a in nodo.names):
                        colpevoli.append(f.name)
                elif isinstance(nodo, ast.ImportFrom):
                    if (nodo.module or "").split(".")[0] == "pytest":
                        colpevoli.append(f.name)
        self.assertEqual(
            colpevoli, [],
            "questi file importano pytest, che in CI non esiste: "
            f"{colpevoli} — riscrivili come unittest.TestCase (ADR-0037)")

    def test_ogni_file_definisce_almeno_una_testcase(self):
        """Le funzioni nude non falliscono: non girano, ed e' peggio."""
        vuoti = []
        for f in file_di_test():
            albero = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            classi = [n for n in albero.body if isinstance(n, ast.ClassDef)]
            ha_testcase = any(
                any(getattr(b, "attr", getattr(b, "id", "")) == "TestCase"
                    for b in c.bases)
                for c in classi)
            if not ha_testcase:
                vuoti.append(f.name)
        self.assertEqual(
            vuoti, [],
            "questi file non definiscono nessuna unittest.TestCase, quindi "
            f"`unittest discover` li importa e non esegue niente: {vuoti}")

    def test_il_numero_di_prove_non_scende(self):
        """Una rete di sicurezza grossolana contro un file che smette di caricarsi."""
        caricati = unittest.defaultTestLoader.discover(str(TESTS), top_level_dir=str(ROOT))
        n = caricati.countTestCases()
        self.assertGreaterEqual(
            n, 960,
            f"`unittest discover` vede solo {n} prove: un modulo non si carica piu'")
        errori = [t for t in caricati._tests if "_FailedTest" in repr(t)]
        self.assertEqual(errori, [], f"moduli che non si importano: {errori}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
