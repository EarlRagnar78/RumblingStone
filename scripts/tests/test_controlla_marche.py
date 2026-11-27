"""controlla_marche.py: i due cancelli delle marche sulle righe cambiate (ADR-0109).

Si prova su un repo git finto, così il diff è vero e i test non dipendono dal ramo.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import controlla_marche as C  # noqa: E402


def git(d: Path, *a: str) -> None:
    subprocess.run(["git", *a], cwd=d, check=True, capture_output=True)


class Repo:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        git(self.d, "init", "-q", "-b", "main")
        git(self.d, "config", "user.email", "t@t")
        git(self.d, "config", "user.name", "t")

    def scrivi(self, rel: str, testo: str) -> None:
        p = self.d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding="utf-8")

    def commit(self, msg: str = "x") -> None:
        git(self.d, "add", "-A")
        git(self.d, "commit", "-q", "-m", msg)

    def avvisi(self) -> list[str]:
        return C.avvisi(C.per_file(C.diff("base", self.d)))


class TestCancelli(unittest.TestCase):
    def setUp(self):
        self.r = Repo()
        self.r.scrivi("07_arco/modulo.md", "Il gufo ha 30 PF [INFERRED — Quanti PF ha?; base: MM 3.5].\n")
        self.r.commit()
        git(self.r.d, "branch", "base")

    def tearDown(self):
        self.r.tmp.cleanup()

    def test_marca_nuova_senza_domanda_avvisa(self):
        self.r.scrivi("07_arco/modulo.md", "Il gufo ha 30 PF [INFERRED — Quanti PF ha?; base: MM 3.5].\n"
                                          "Vola a 24 m [INFERRED — needs DM confirmation].\n")
        self.r.commit()
        a = self.r.avvisi()
        self.assertEqual(len(a), 1)
        self.assertIn("modulo.md:2", a[0])

    def test_marca_con_domanda_e_base_passa(self):
        self.r.scrivi("07_arco/modulo.md", "Il gufo ha 30 PF [INFERRED — Quanti PF ha?; base: MM 3.5].\n"
                                          "Vola a 24 m [INFERRED — Quanto vola?; base: gufo gigante MM].\n")
        self.r.commit()
        self.assertEqual(self.r.avvisi(), [])

    def test_inferred_tolto_in_silenzio_avvisa(self):
        self.r.scrivi("07_arco/modulo.md", "Il gufo ha 30 PF.\n")
        self.r.commit()
        a = self.r.avvisi()
        self.assertEqual(len(a), 1)
        self.assertIn("tolti", a[0])

    def test_inferred_chiuso_con_canone_passa(self):
        self.r.scrivi("07_arco/modulo.md", "Il gufo ha 30 PF [CANONE — DM 2026-11-07, card 3].\n")
        self.r.commit()
        self.assertEqual(self.r.avvisi(), [])

    def test_file_cancellato_conta(self):
        (self.r.d / "07_arco/modulo.md").unlink()
        self.r.commit()
        self.assertEqual(len(self.r.avvisi()), 1)

    def test_piani_modelli_e_volumi_non_contano(self):
        for rel in ("plans/ESITO.md", "campaign/templates/x-template.md", "07_arco/vol.hb.md",
                    "skills/x/SKILL.md"):
            self.r.scrivi(rel, "fatto [INFERRED]\n")
        self.r.commit()
        self.assertEqual(self.r.avvisi(), [])

    def test_lo_schema_e_le_citazioni_non_contano(self):
        self.r.scrivi("docs/guides/GUIDA-X.md", "marca `[INFERRED — <domanda>; base: <…>]`;\n"
                                                "i fatti marcati `[INFERRED]` restano.\n")
        self.r.commit()
        self.assertEqual(self.r.avvisi(), [])

    def test_togliere_una_citazione_non_e_togliere_un_fatto(self):
        self.r.scrivi("docs/guides/GUIDA-Y.md", "i fatti marcati `[INFERRED]` restano.\n")
        self.r.commit()
        git(self.r.d, "branch", "-f", "base")
        self.r.scrivi("docs/guides/GUIDA-Y.md", "i fatti marcati restano.\n")
        self.r.commit()
        self.assertEqual(self.r.avvisi(), [])


if __name__ == "__main__":
    unittest.main()
