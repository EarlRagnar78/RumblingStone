"""🌫, il vuoto: RIPRESA-PR 4j-4 (2026-09-24), dal ramo della PR #42.

La PR #42 fu chiusa senza merge perche' le sue quattro griglie erano gia' in
`ARC07-MAPPE-DEFINITIVO.md`. Restava il suo simbolo per l'aria dove non c'e'
pavimento, che su `main` era solo un simbolo locale: due mappe di ARC-07 lo
usavano (346 celle) e il renderer le disegnava come emoji. Il DM ha deciso di
portarlo nella legenda.

Il test fissa le due cose che contano: il simbolo si disegna col suo motivo, e
non diventa ne' un muro ne' un pericolo, perche' cadere o fluttuare dipende
dalla scena.
"""

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402
import export_uvtt as U  # noqa: E402
from dmcore import legenda  # noqa: E402

VUOTO = "\U0001f32b"


class TestIlVuoto(unittest.TestCase):
    def test_e_nella_legenda_come_terreno(self):
        self.assertIn(VUOTO, R.SYMBOLS)
        self.assertEqual(R.SYMBOLS[VUOTO]["mode"], "fill")
        self.assertEqual(R.SYMBOLS[VUOTO]["pat"], "t_void")

    def test_non_e_un_muro_ne_un_pericolo(self):
        self.assertNotIn(VUOTO, U.WALL_SYMS)
        self.assertNotIn(VUOTO, legenda.pericoli())

    def test_si_disegna_col_suo_motivo(self):
        griglia = ("## MAPPA T-9: il salto (griglia 6×3, scala 1,5 m/q)\n\n"
                   "```\n"
                   "     A  B  C  D  E  F\n"
                   f" 1 | ⬜ ⬜ {VUOTO} {VUOTO} ⬜ ⬜ |\n"
                   f" 2 | ⬜ ⬜ {VUOTO} {VUOTO} ⬜ ⬜ |\n"
                   f" 3 | ⬜ ⬜ {VUOTO} {VUOTO} ⬜ ⬜ |\n"
                   "```\n")
        mappe = R.extract_maps(griglia)
        self.assertEqual(len(mappe), 1)
        svg = R.render_svg(mappe[0], "prova")
        self.assertIn('id="t_void"', svg)


if __name__ == "__main__":
    unittest.main()
