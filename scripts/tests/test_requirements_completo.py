"""requirements-completo.txt e il registro di `binari.py` dicono la stessa cosa.

Una libreria che il registro manda a installare con requirements-completo.txt
deve stare nel file; e il file parte dalla dotazione di sviluppo, così chi lo
installa ha anche tutto ciò che vuole la CI.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import binari  # noqa: E402

FILE = ROOT / "requirements-completo.txt"


class TestCompleto(unittest.TestCase):
    def setUp(self):
        righe = [r.split("#")[0].strip() for r in FILE.read_text(encoding="utf-8").splitlines()]
        self.righe = [r for r in righe if r]
        self.pacchetti = {re.split(r"[<>=;\s\[]", r, maxsplit=1)[0].lower()
                          for r in self.righe if not r.startswith("-")}

    def test_parte_dalla_dotazione_di_sviluppo(self):
        self.assertIn("-r requirements-dev.txt", self.righe)

    def test_ogni_libreria_che_il_registro_ci_manda_sta_nel_file(self):
        for lib in binari.LIBRERIE:
            if "requirements-completo.txt" in lib.installa:
                self.assertIn(lib.nome.lower(), self.pacchetti, lib.nome)

    def test_torch_viene_dall_indice_cpu(self):
        self.assertIn("--extra-index-url https://download.pytorch.org/whl/cpu", self.righe)


if __name__ == "__main__":
    unittest.main()
