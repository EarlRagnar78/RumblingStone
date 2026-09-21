"""Che i test girino davvero in CI, sotto **entrambi** i corridori.

🔴 **Il difetto che presidia, misurato il 2026-09-21.** La CI eseguiva
`python -m unittest discover -s scripts/tests` e pytest non era installato
(ADR-0037, stdlib-only). Tre file di test nuovi erano scritti in stile pytest:

  * due importavano `pytest` -> in CI il modulo **non si importava**, e la
    build e' diventata rossa (`ModuleNotFoundError`, run 35567918916);
  * uno era fatto di **funzioni nude**, che `unittest discover` importa senza
    eseguire -> in CI girava a vuoto, **in silenzio**, che e' peggio del rosso.

Il conto: in locale pytest vedeva 966 prove, la CI ne eseguiva **942**.

⚠️ **E la cura ha riaperto il buco al contrario.** L'emendamento del 2026-09-21
ad ADR-0037 ammette pytest come dipendenza di **sviluppo**, e da quel momento le
funzioni nude girano sotto pytest e **non** sotto `unittest`: chi le scrive
vede verde e non si accorge di niente. Per questo il repo gira entrambi i
corridori e questo file misura la **parita'**: se i due non vedono lo stesso
numero di prove, qualcosa non gira da qualche parte.

Questo file usa la sola libreria standard di proposito: e' il controllo che
deve funzionare anche quando l'altro corridore non e' installato.
"""
from __future__ import annotations

import ast
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "scripts" / "tests"


def file_di_test() -> "list[Path]":
    return sorted(p for p in TESTS.glob("test_*.py"))


def prove_viste_da_unittest() -> int:
    caricati = unittest.defaultTestLoader.discover(str(TESTS), top_level_dir=str(ROOT))
    return caricati.countTestCases()


def prove_viste_da_pytest() -> "int | None":
    """Quante ne raccoglie pytest, o None se qui non c'e'."""
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q",
                        str(TESTS)], capture_output=True, text=True, cwd=ROOT)
    if r.returncode not in (0, 5) and "No module named" in (r.stderr + r.stdout):
        return None
    for riga in reversed((r.stdout or "").splitlines()):
        # l'ultima riga utile e' del tipo «975 tests collected in 0.42s»
        pezzi = riga.split()
        for i, p in enumerate(pezzi):
            if p in ("test", "tests") and i and pezzi[i - 1].isdigit():
                return int(pezzi[i - 1])
    return None


class TestOgniProvaGiraDavvero(unittest.TestCase):

    def test_nessun_modulo_di_test_e_rotto(self):
        """Un `_FailedTest` e' un file che non si importa: la CI lo vede rosso."""
        caricati = unittest.defaultTestLoader.discover(str(TESTS),
                                                       top_level_dir=str(ROOT))
        rotti = [repr(t) for t in caricati._tests if "_FailedTest" in repr(t)]
        self.assertEqual(rotti, [], f"moduli che non si importano: {rotti}")

    def test_ogni_file_definisce_almeno_una_testcase(self):
        """Le funzioni nude non falliscono sotto `unittest`: non girano."""
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

    def test_i_due_corridori_vedono_lo_stesso_numero(self):
        """La misura del difetto del 2026-09-21: 966 contro 942."""
        con_pytest = prove_viste_da_pytest()
        if con_pytest is None:
            self.skipTest("pytest non installato qui: `pip install -r requirements-dev.txt`")
        con_unittest = prove_viste_da_unittest()
        self.assertEqual(
            con_unittest, con_pytest,
            f"`unittest discover` vede {con_unittest} prove e pytest ne vede "
            f"{con_pytest}: qualcosa gira sotto un corridore e non sotto l'altro")

    def test_le_dipendenze_sono_dichiarate(self):
        """ADR-0037: un file di dipendenze che non nomina cio' che il repo importa."""
        runtime = (ROOT / "requirements.txt")
        dev = (ROOT / "requirements-dev.txt")
        self.assertTrue(runtime.exists(), "manca requirements.txt (ADR-0037)")
        self.assertTrue(dev.exists(), "manca requirements-dev.txt (ADR-0037)")
        t = runtime.read_text(encoding="utf-8").lower()
        for pacchetto in ("pyyaml", "pillow", "tiktoken"):
            self.assertIn(pacchetto, t,
                          f"{pacchetto} e' importato da scripts/ e non e' dichiarato")
        self.assertIn("pytest", dev.read_text(encoding="utf-8").lower())
        self.assertNotIn("pytest", t,
                         "pytest e' una dipendenza di sviluppo, non di esecuzione "
                         "(emendamento 2026-09-21 ad ADR-0037)")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
