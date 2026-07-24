"""Test di import_ultraclear.py — ASCII ultra-clear → bozza JSON + report conflitti.

Copre (PIANO-IMPORT-ULTRACLEAR §9):
- parser griglia (riuso render_map_svg) e parser tabelle/posizioni PG;
- una fixture minima per ciascuna regola del registro (R1-R10);
- il GOLDEN CASE Hammerfist L2: il report elenca i 4 difetti-tipo (D1-D4) e la
  bozza converge (per aree/coordinate) verso hammerfist-L2-assedio.json;
- round-trip: ogni bozza senza ERROR supera compile_map_json --validate-only;
- determinismo: a parità di input, byte identici.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import import_ultraclear as I     # noqa: E402
import compile_map_json as C      # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "ultraclear"
GOLDEN_MD = ROOT.parent / "08_La Battaglia Di Hammerfist" / "Mappe" / "Hammerfist-L2-REVISED-Ultra-Clear.md"
GOLDEN_JSON = ROOT / "examples" / "hammerfist-L2-assedio.json"


def _load(name):
    return (FIX / name).read_text(encoding="utf-8")


def _ids(conflicts):
    return {c.id for c in conflicts}


def _run(name):
    """Parse the single-map fixture, emit draft + conflicts."""
    maps = I.parse_maps(_load(name))
    assert maps, f"nessuna mappa in {name}"
    draft, conflicts = I.process(maps[0])
    return maps[0], draft, conflicts


class TestParsers(unittest.TestCase):
    def test_grid_reuses_render_parser(self):
        pmap, _, _ = _run("uniform.md")
        # 10x6 as declared, actual matches
        self.assertEqual(pmap.declared_dims, (10, 6))
        self.assertEqual(pmap.actual_dims, (10, 6))
        self.assertAlmostEqual(pmap.scale_m, 1.5)

    def test_table_and_pg_parse_1based_to_0based(self):
        entries = I._parse_tables(_load("tables_conflicts.md"))
        names = {e.name for e in entries}
        self.assertIn("Torre Dara", names)
        pg = I._parse_pg_positions(_load("tables_conflicts.md"))
        dara = next(p for p in pg if p.name == "Dara")
        self.assertEqual((dara.col, dara.row), (2, 2))  # kept 1-based in the model
        # _to_rect converts to 0-based [x,y,w,h]
        self.assertEqual(I._to_rect((2, 3), (2, 3)), [1, 1, 2, 2])
        self.assertEqual(I._to_rect((60, 60), (34, 34)), [59, 33, 1, 1])


class TestRules(unittest.TestCase):
    def test_uniform_clean_and_compilable(self):
        _, draft, conflicts = _run("uniform.md")
        self.assertNotIn("R1", _ids(conflicts))
        self.assertNotIn("R2", _ids(conflicts))
        self.assertEqual([], I._validate_draft(draft))  # compiles clean

    def test_r1_grid_header_mismatch(self):
        _, _, conflicts = _run("r1_header.md")
        r1 = [c for c in conflicts if c.id == "R1"]
        self.assertEqual(len(r1), 1)
        self.assertEqual(r1[0].severity, "ERROR")
        self.assertEqual(r1[0].expected["value"], [8, 5])   # header
        self.assertEqual(r1[0].observed["value"], [5, 3])   # real cells
        self.assertEqual(r1[0].target, "/map_size")
        self.assertTrue(any(a["kind"] == "resize_map" for a in r1[0].actions))

    def test_r2_nonuniform_rows(self):
        _, _, conflicts = _run("r2_nonuniform.md")
        self.assertIn("R2", _ids(conflicts))

    def test_r3_symbol_not_in_legend(self):
        _, _, conflicts = _run("r3_symbol.md")
        r3 = [c for c in conflicts if c.id == "R3"]
        self.assertTrue(r3)
        sevs = {c.severity for c in r3}
        self.assertIn("WARN", sevs)    # ⛰️ variation-selector near-match
        self.assertIn("ERROR", sevs)   # 🦄 unknown
        warn = next(c for c in r3 if c.severity == "WARN")
        self.assertTrue(any(a["kind"] == "replace_symbol" for a in warn.actions))

    def test_r4_r5_r6_r8_from_tables(self):
        _, draft, conflicts = _run("tables_conflicts.md")
        ids = _ids(conflicts)
        self.assertIn("R4", ids)   # drift: PG su cella terreno / fuori figura
        self.assertIn("R5", ids)   # Dara vs Dana
        self.assertIn("R6", ids)   # col 40 fuori 10x6
        self.assertIn("R8", ids)   # 50 nani in area 2x2
        r5 = next(c for c in conflicts if c.id == "R5")
        self.assertTrue(any(a["kind"] == "confirm_distinct" for a in r5.actions))

    def test_r10_schematic_skipped(self):
        # a render:none schematic block yields no grid map at all
        maps = I.parse_maps(_load("schematic.md"))
        self.assertEqual(maps, [])

    def test_r11_catch_all_uncatalogued_defect(self):
        # a draft that no R1-R10 rule explains but that STILL won't compile must
        # not be swallowed: R11 surfaces it as an ERROR (the raw validator msg).
        pmap = I.ParsedMap(index=1, title="X", matrix=[], declared_dims=None,
                           scale_m=1.5, tables=[], pg=[], raw_lines=[])
        bad_draft = {"title": "X"}   # manca map_size → il contratto rifiuta
        conflicts = I.diagnose(pmap, grid_usable=False, draft=bad_draft)
        r11 = [c for c in conflicts if c.id == "R11"]
        self.assertTrue(r11)
        self.assertEqual(r11[0].severity, "ERROR")
        self.assertTrue(r11[0].uid)

    def test_r11_silent_when_registry_already_explains(self):
        # if a catalogued ERROR already fires, R11 stays quiet (no duplicate noise)
        _, _, conflicts = _run("r1_header.md")   # R1 ERROR present
        self.assertIn("R1", _ids(conflicts))
        self.assertNotIn("R11", _ids(conflicts))


class TestEditorContract(unittest.TestCase):
    """The conflict record must be consumable by the visual editor (§7)."""

    def test_records_have_stable_unique_uid(self):
        _, _, conflicts = _run("tables_conflicts.md")
        uids = [c.uid for c in conflicts]
        self.assertTrue(all(uids))
        self.assertEqual(len(uids), len(set(uids)))          # unique per instance
        # stable across a second run (content fingerprint, order-independent)
        _, _, again = _run("tables_conflicts.md")
        self.assertEqual(sorted(c.uid for c in conflicts),
                         sorted(c.uid for c in again))

    def test_actions_use_known_vocabulary(self):
        for name in ("r1_header.md", "r3_symbol.md", "tables_conflicts.md"):
            _, _, conflicts = _run(name)
            for c in conflicts:
                for a in c.actions:
                    self.assertIn(a["kind"], I.ACTION_KINDS)
                    self.assertIn("label", a)

    def test_json_report_shape(self):
        pmap, _, conflicts = _run("tables_conflicts.md")
        payload = json.loads(I.render_report_json(pmap, conflicts))
        self.assertEqual(payload["report_version"], I.REPORT_VERSION)
        self.assertEqual(payload["source_of_truth"], "table")
        self.assertIn("counts", payload)
        # every serialized conflict keeps the required keys, drops empties
        for rec in payload["conflicts"]:
            self.assertIn("uid", rec)
            self.assertIn("id", rec)
            self.assertIn("severity", rec)
            self.assertNotIn("", rec.values())


class TestGoldenCase(unittest.TestCase):
    def setUp(self):
        if not GOLDEN_MD.exists():
            self.skipTest("golden ultra-clear non presente")
        self.maps = I.parse_maps(GOLDEN_MD.read_text(encoding="utf-8"))
        self.pmap = self.maps[0]
        self.draft, self.conflicts = I.process(self.pmap)

    def test_reports_the_four_defect_types(self):
        ids = _ids(self.conflicts)
        self.assertIn("R1", ids)   # D1 — griglia non uniforme vs header 120×80
        self.assertIn("R3", ids)   # D2 — ⛰️ con variation-selector
        self.assertIn("R5", ids)   # D3 — collisione Dara/Dana
        self.assertIn("R4", ids)   # D4 — drift annotazione↔coordinata

    def test_map_size_from_authoritative_header(self):
        self.assertEqual(self.draft["map_size"], [120, 80])

    def test_units_converge_to_committed_golden(self):
        golden = json.loads(GOLDEN_JSON.read_text(encoding="utf-8"))
        gold_areas = {tuple(u["area"]["rect"]) for u in golden["units"] if "area" in u}
        draft_areas = {tuple(u["area"]["rect"]) for u in self.draft.get("units", []) if "area" in u}
        # the mass-unit blocks reconstructed from the tables match the hand-built master
        common = gold_areas & draft_areas
        # the count-bearing table entries reconstruct EXACTLY (Cantitrici, Nani
        # Elite); the bastioni were hand-tuned in the committed master, so an
        # exact byte match is not expected — "diff semantico accettabile" (§5).
        self.assertGreaterEqual(len(common), 2, f"aree comuni: {common}")
        self.assertGreaterEqual(len(draft_areas), 6)   # comparable mass-unit count

    def test_named_pg_placed_at_declared_coords(self):
        units = self.draft.get("units", [])
        dara = next(u for u in units if u.get("name", "").startswith("Dara Occhiolesto"))
        self.assertEqual(dara["at"], [8, 61])       # Col 09, Riga 62 → 0-based
        self.assertEqual(dara["token"], "🟢")       # sniper, non ⚫ (word-boundary role)


class TestRoundTrip(unittest.TestCase):
    def test_clean_fixtures_validate_only_ok(self):
        for name in ("uniform.md", "r2_nonuniform.md"):
            _, draft, conflicts = _run(name)
            errors = [c for c in conflicts if c.severity == "ERROR"]
            self.assertEqual(errors, [], f"{name} inatteso ERROR")
            self.assertEqual(I._validate_draft(draft), [], f"{name} non compila")

    def test_determinism_byte_identical(self):
        pmap, _, conflicts = _run("tables_conflicts.md")
        a = I.render_report_json(pmap, conflicts)
        pmap2, _, conflicts2 = _run("tables_conflicts.md")
        b = I.render_report_json(pmap2, conflicts2)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
