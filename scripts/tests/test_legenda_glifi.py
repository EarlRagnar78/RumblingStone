"""ADR-0042: i tre glifi che stavano sotto ⬛ devono restare tre cose distinte.

Il test guarda l'invariante che si era rotto — un glifo con tre significati e
un export che li appiattiva tutti su «muro» — e la proprieta' che rende la
decisione applicabile: ⬛ NON cambia comportamento, quindi nessuna delle 8.216
celle gia' disegnate si muove sotto i piedi di nessuno.
"""

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402
import export_uvtt as U  # noqa: E402
import import_ultraclear as I  # noqa: E402

EDIFICIO, TENDA, DAIS = "⬛", "⛺", "\U0001f533"


class TestTreGlifi(unittest.TestCase):
    def test_i_tre_glifi_esistono_e_sono_distinti(self):
        for g in (EDIFICIO, TENDA, DAIS):
            self.assertIn(g, R.SYMBOLS, f"{g} non e' nella legenda")
        etichette = {R.SYMBOLS[g]["it"] for g in (EDIFICIO, TENDA, DAIS)}
        self.assertEqual(len(etichette), 3, "due glifi condividono l'etichetta")

    def test_nessuna_etichetta_elenca_piu_di_una_cosa(self):
        """Il difetto era proprio questo: «Struttura (tenda, edificio, dais)»."""
        for g in (EDIFICIO, TENDA, DAIS):
            testo = R.SYMBOLS[g]["it"].lower()
            presenti = [k for k in ("tenda", "edificio", "dais") if k in testo]
            self.assertLessEqual(
                len(presenti), 1,
                f"{g} elenca ancora piu' significati: {R.SYMBOLS[g]['it']!r}")

    def test_edificio_e_tenda_sono_muri_il_dais_no(self):
        self.assertIn(EDIFICIO, U.WALL_SYMS)
        self.assertIn(TENDA, U.WALL_SYMS, "un telo teso blocca la vista")
        self.assertNotIn(DAIS, U.WALL_SYMS, "su una pedana ci si sale, non ci si sbatte")

    def test_il_dais_ha_un_disegno_suo(self):
        self.assertEqual(R.SYMBOLS[DAIS]["pat"], "t_dais")
        self.assertIn("t_dais", R.PATTERNS)
        self.assertNotEqual(R.PATTERNS["t_dais"], R.PATTERNS["t_struct"])

    def test_l_edificio_non_ha_cambiato_comportamento(self):
        """La proprieta' che rende ADR-0042 applicabile senza migrazione."""
        self.assertEqual(R.SYMBOLS[EDIFICIO]["mode"], "fill")
        self.assertEqual(R.SYMBOLS[EDIFICIO]["pat"], "t_struct")
        self.assertEqual(R.SYMBOLS[EDIFICIO]["fill"], "#6b5b47")

    def test_l_import_riconosce_i_nomi_delle_tre_cose(self):
        atteso = {"tenda": TENDA, "accampamento": TENDA,
                  "dais": DAIS, "pedana": DAIS}
        trovato = {kw: sym for kw, _role, sym in I.STRUCT_KEYWORDS if kw in atteso}
        self.assertEqual(trovato, atteso)

    def test_i_tre_glifi_si_disegnano_diversi(self):
        """Prova end-to-end: una griglia coi tre glifi produce tre riempimenti.

        La griglia e' 6x3 perche' `parse_block` scarta i blocchi troppo stretti:
        una mappa di tre colonne non e' una mappa.
        """
        griglia = ("## MAPPA T-1: tre glifi (griglia 6×3, scala 1,5 m/q)\n\n"
                   "```\n"
                   "     A  B  C  D  E  F\n"
                   " 1 | ⬜ ⬛ ⬛ ⬜ ⛺ ⬜ |\n"
                   " 2 | ⬜ ⬛ ⬛ ⬜ ⛺ ⬜ |\n"
                   " 3 | ⬜ ⬜ ⬜ \U0001f533 \U0001f533 ⬜ |\n"
                   "```\n")
        mappe = R.extract_maps(griglia)
        self.assertEqual(len(mappe), 1)
        svg = R.render_svg(mappe[0], "prova")
        for frammento in ("t_struct", "pr_tent", "t_dais"):
            self.assertIn(frammento, svg, f"{frammento} non compare nell'SVG")

if __name__ == "__main__":
    unittest.main()
