"""Test di compile_map_json.normalize_units — l'authoring in METRI produce
la STESSA griglia dell'equivalente in quadretti (proporzioni esatte per
aritmetica, zero drift). Copre anche il loop reject-and-resend su input non
convertibili."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compile_map_json as C  # noqa: E402

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class TestMeters(unittest.TestCase):
    def test_squares_mode_is_noop(self):
        spec = {"title": "Test", "map_size": [10, 8]}
        self.assertIs(C.normalize_units(spec), spec)  # unchanged, same object

    def test_map_size_meters_to_squares(self):
        spec = {"title": "Test", "scale_m_per_square": 1.5,
                "units_in": "meters", "map_size": [45, 33]}
        out = C.normalize_units(spec)
        self.assertEqual(out["map_size"], [30, 22])
        self.assertEqual(out["units_in"], "squares")  # flag consumed
        self.assertEqual(spec["map_size"], [45, 33])   # original untouched

    def test_meters_equal_squares_grid(self):
        """A meters spec and the hand-computed squares spec paint the SAME grid."""
        meters = {
            "title": "Equivalenza", "scale_m_per_square": 1.5,
            "units_in": "meters", "map_size": [30, 15],
            "base_terrain": "🟩",
            "regions": [{"terrain": "🟫", "rect": [3, 3, 9, 6]}],
            "structures": [{"type": "🧱", "line": [[0, 0], [28.5, 0]]},
                           {"type": "🚪", "at": [15, 0]}],
            "units": [{"token": "🟢", "at": [7.5, 7.5], "name": "PG"}],
        }
        squares = {
            "title": "Equivalenza", "scale_m_per_square": 1.5,
            "map_size": [20, 10], "base_terrain": "🟩",
            "regions": [{"terrain": "🟫", "rect": [2, 2, 6, 4]}],
            "structures": [{"type": "🧱", "line": [[0, 0], [19, 0]]},
                           {"type": "🚪", "at": [10, 0]}],
            "units": [{"token": "🟢", "at": [5, 5], "name": "PG"}],
        }
        cols_m, rows_m = C.validate(C.normalize_units(meters))
        cols_s, rows_s = C.validate(squares)
        self.assertEqual((cols_m, rows_m), (cols_s, rows_s))
        grid_m = C.paint(C.normalize_units(meters), cols_m, rows_m)
        grid_s = C.paint(squares, cols_s, rows_s)
        self.assertEqual(grid_m, grid_s)

    def test_rect_edge_snapping_is_proportional(self):
        """A 9x6 m rect at (3,3) m snaps origin AND far edge -> [2,2,6,4] sq."""
        spec = {"title": "Snap", "scale_m_per_square": 1.5, "units_in": "meters",
                "map_size": [30, 30], "regions": [{"terrain": "🟫", "rect": [3, 3, 9, 6]}]}
        out = C.normalize_units(spec)
        self.assertEqual(out["regions"][0]["rect"], [2, 2, 6, 4])

    def test_bad_units_value_rejected(self):
        with self.assertRaises(C.SpecError):
            C.normalize_units({"title": "x", "units_in": "feet", "map_size": [10, 10]})

    def test_non_numeric_meter_rejected(self):
        with self.assertRaises(C.SpecError):
            C.normalize_units({"title": "x", "units_in": "meters",
                               "map_size": ["wide", 10]})

    def test_committed_meters_example_compiles(self):
        spec = json.loads((EXAMPLES / "esempio-misure-in-metri.json").read_text("utf-8"))
        cols, rows = C.validate(C.normalize_units(spec))
        self.assertEqual((cols, rows), (30, 22))
        # deterministic: normalize+paint twice yields identical grids
        g1 = C.paint(C.normalize_units(spec), cols, rows)
        g2 = C.paint(C.normalize_units(spec), cols, rows)
        self.assertEqual(g1, g2)


if __name__ == "__main__":
    unittest.main()
