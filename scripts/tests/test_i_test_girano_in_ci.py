"""Che i test girino davvero in CI, e che girerebbero sotto **entrambi** i corridori.

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
vede verde e non si accorge di niente. Per un mese il repo ha girato entrambi
i corridori; dal <data della decisione del DM> la CI gira solo pytest, e questo
file misura la **parita'** senza il secondo giro: ogni modulo si importa sotto
`unittest discover`, ogni file ha una TestCase, e i due conti coincidono. Se
non coincidono, qualcosa girerebbe sotto un corridore e non sotto l'altro.

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
        for pacchetto in ("pyyaml", "pillow", "tiktoken", "typst"):
            self.assertIn(pacchetto, t,
                          f"{pacchetto} e' importato da scripts/ e non e' dichiarato")
        self.assertIn("pytest", dev.read_text(encoding="utf-8").lower())
        self.assertNotIn("pytest", t,
                         "pytest e' una dipendenza di sviluppo, non di esecuzione "
                         "(emendamento 2026-09-21 ad ADR-0037)")


def giri_pytest_del_job(ci: Path, job: str = "validate") -> "list[str]":
    """Le righe `python -m pytest scripts/tests …` dei passi del `job` in `ci.yml`."""
    import yaml
    dati = yaml.safe_load(ci.read_text(encoding="utf-8"))
    righe = []
    for passo in dati["jobs"][job].get("steps", []):
        for riga in str(passo.get("run", "")).splitlines():
            if "-m pytest scripts/tests" in riga:
                righe.append(riga.strip())
    return righe


class TestLaCiGiraLaSuiteIntera(unittest.TestCase):
    """pytest-xdist e' stable dal 2026-11-25 (ADR-0099): il job principale gira
    la suite in due giri, in parallelo e poi in serie i moduli che scrivono nel
    repo (conftest.py). Insieme devono fare la suite intera: un giro che manca, o
    un filtro che non e' il complemento dell'altro, lascerebbe prove fuori."""

    def test_i_due_giri_del_job_principale_sono_complementari(self):
        import shlex
        giri = giri_pytest_del_job(ROOT / ".github" / "workflows" / "ci.yml")
        filtri = {}
        for g in giri:
            a = shlex.split(g)
            m = a[a.index("-m", a.index("pytest")) + 1] if a.count("-m") > 1 else ""
            filtri[m] = "-n" in a
        self.assertEqual(set(filtri), {"not scrive_nel_repo", "scrive_nel_repo"}, giri)
        self.assertTrue(filtri["not scrive_nel_repo"], "il primo giro e' quello parallelo (-n auto)")
        self.assertFalse(filtri["scrive_nel_repo"], "i moduli che scrivono nel repo girano in serie")

    def test_il_marcatore_e_quello_di_conftest(self):
        conftest = (TESTS / "conftest.py").read_text(encoding="utf-8")
        self.assertIn("pytest.mark.scrive_nel_repo", conftest)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
