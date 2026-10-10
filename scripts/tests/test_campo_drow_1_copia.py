"""Il Campo Drow 1 ha due copie della stessa griglia, e devono restare uguali.

La mappa sta nel SUPPLEMENTO-P1C (con le didascalie) e nel P1C-Rituale (dove
l'incontro si gioca). Il 2026-10-09 le due erano diverse: uno schizzo di 9 righe
da una parte, 25 righe dall'altra. Si modifica il SUPPLEMENTO e si ricopia: se
qualcuno tocca una copia sola, questo test lo dice.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import render_map_svg as R  # noqa: E402

ARCO = REPO / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"


def _campo_1(nome: str) -> dict:
    mappe = R.extract_maps((ARCO / nome).read_text(encoding="utf-8"))
    return next(m for m in mappe if "CAMPO DROW 1" in m["title"].upper())


class TestCampoDrow1(unittest.TestCase):
    def test_le_due_copie_hanno_la_stessa_griglia_intera(self):
        sup = _campo_1("SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md")
        p1c = _campo_1("Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md")
        self.assertEqual(sorted(sup["rows"]), list(range(1, 41)))
        self.assertTrue(all(len(r) == 53 for r in sup["rows"].values()))
        self.assertEqual(sup["rows"], p1c["rows"])


if __name__ == "__main__":
    unittest.main()
