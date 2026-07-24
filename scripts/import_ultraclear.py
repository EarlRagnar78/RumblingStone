#!/usr/bin/env python3
"""
import_ultraclear.py — from an ASCII "ultra-clear" map to a DRAFT of the
rigid JSON contract (Modalità 3) + a conflict report.

An ultra-clear master fuses two things that ought to stay separate: a
*readable figure* (the emoji grid, drawn by hand and prone to drift) and the
*authoritative data* (the coordinate tables). When they diverge, the figure
lies. This tool makes the divergence EXPLICIT: it parses both, emits a draft
`tactical_map.schema.json` spec, and lists every conflict with a severity and
a suggestion — so a human/LLM resolves only the flagged points instead of
discovering them by eye after the render.

Design rules (PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md):

  - Single source of truth for the grid: it is read with render_map_svg's own
    parser (`extract_maps` / `parse_row_cells`), so what this tool "sees" is
    identical to what the renderer would draw — the only faithful way to
    diagnose D1 (header vs cells) and D4 (drawn vs declared).
  - The tool NEVER auto-fixes semantics. When the grid and a table disagree,
    the DEFAULT is *the table wins* (authoritative data) + a WARN — it never
    silently picks a side without saying so.
  - It does not invent geometry: elements without coordinates are left out of
    the grid and recorded in `notes`.
  - It does not touch the canonical arc masters: it emits new files only.

Downstream the pipeline is identical to Modalità 3:
    import_ultraclear.py IN.md -o OUT.draft.json
    compile_map_json.py OUT.draft.json --validate-only   # human-in-the-loop
    compile_map_json.py OUT.draft.json -o MASTER.md
    render_map_svg.py MASTER.md

Usage:
    python3 scripts/import_ultraclear.py INPUT.md [-o OUT.draft.json]
        [--conflicts REPORT.md] [--json-report REPORT.conflicts.json]
        [--emit-md DIR] [--map N] [--strict] [-q|-v]

Exit codes (stable, script-friendly):
    0 — draft compilabile, nessun ERROR (WARN/INFO ammessi);
    1 — prodotti ERROR: la bozza NON è compilabile (segnale human-in-the-loop);
    2 — errore d'uso/IO (file mancante, markdown senza mappe, --emit-md fallito).

Pure Python 3, no dependencies. Deterministic output (byte-stable).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path

REPORT_VERSION = "1.0"        # version of the conflict-report contract (editor input)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map_svg as rms          # noqa: E402  (single source of truth: grid parser + legend)
import compile_map_json as cmj        # noqa: E402  (validation + meters→squares, for the round-trip)

SCHEMA_VERSION = "1.0"
DEFAULT_BASE_TERRAIN = "🟩"
DEFAULT_SCALE = 1.5

SYMBOLS = rms.SYMBOLS
FILL_SYMS = {s for s, d in SYMBOLS.items() if d.get("mode") == "fill"}
UNIT_SYMS = {s for s, d in SYMBOLS.items() if d.get("mode") == "unit"}
ICON_SYMS = {s for s, d in SYMBOLS.items() if d.get("mode") == "icon"}

# icons that read as environmental hazards rather than built structures
HAZARD_SYMS = {"🔥", "💥", "💀", "🕳", "⚡", "❄", "🕸"}

# keyword → (role, symbol) for reconstructing geometry from a coordinate table
# (used only when the grid is unusable and the table is authoritative). Ordered:
# first substring match wins. Each assignment is echoed into `notes`, never hidden.
STRUCT_KEYWORDS: list[tuple[str, str, str]] = [
    ("montagn", "region", "⛰"),
    ("fossato", "region", "🟦"),
    ("pendio", "region", "🟫"),
    ("torre", "structure", "🗼"),
    ("bastione", "structure", "🏰"),
    ("muro", "structure", "🏰"),
    ("mura", "structure", "🏰"),
    ("porta", "structure", "🚪"),
    ("cancello", "structure", "🚪"),
    ("ponte", "structure", "🌉"),
    ("balista", "structure", "🎯"),
    ("balestra", "structure", "🎯"),
]

# keyword (matched on WORD boundaries, so "re" ≠ "torre") → unit token.
UNIT_KEYWORDS: list[tuple[str, str]] = [
    (r"\bre\b", "⚫"), (r"comando", "⚫"), (r"comandant\w*", "⚫"), (r"\bboss\b", "⚫"),
    (r"incantatore", "🟡"), (r"\bmago\b", "🟡"), (r"caster", "🟡"),
    (r"cecchin\w*", "🟢"), (r"sniper", "🟢"), (r"bardic\w*", "🟢"), (r"\bcura\b", "🟢"),
    (r"healing", "🟢"), (r"\bmadre\b", "🟢"), (r"guaritric\w*", "🟢"),
]
DEFAULT_PG_TOKEN = "🟢"      # a named PC/NPC with no explicit role keyword
DEFAULT_TROOP_TOKEN = "🔵"   # a mass unit ("50 Nani")

TROOP_WORDS = ("nani", "nano", "guerrier", "cantitric", "cantitrice", "elite",
               "élite", "arcier", "soldat", "riserva", "fanti", "truppe")


# --------------------------------------------------------------------------- #
# Conflict model (§7 / §8 of the plan)
# --------------------------------------------------------------------------- #
SEV_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}


# action vocabulary the visual editor maps to buttons (§7 — editor input).
# Keep in sync with scripts/schemas/map_conflicts.schema.json.
ACTION_KINDS = {
    "use_table",        # adopt the table (authoritative) value      — params: {}
    "use_grid",         # adopt the grid (figure) value              — params: {}
    "replace_symbol",   # swap a glyph                               — params: {from, to}
    "resize_map",       # change map_size                            — params: {to:[c,r]}
    "edit_coord",       # fix a coordinate                           — params: {coord}
    "set_quantity",     # align the written count                    — params: {to}
    "confirm_distinct", # confirm two similar names are two entities — params: {}
    "rename",           # rename one of the colliding entities       — params: {name}
    "ignore",           # dismiss (no-op)                            — params: {}
}


@dataclass
class Conflict:
    id: str                       # rule id R1..R10 (identifies the RULE, not the instance)
    rule: str                     # slug, e.g. "grid-header-mismatch"
    severity: str                 # ERROR | WARN | INFO
    message: str
    map: int = 1                  # 1-based map index in the file
    where: dict = field(default_factory=dict)   # anchor: {row?, cell?[x,y], cells?, rect?, coord?}
    suggestion: str = ""
    source: str = "grid"          # grid | table | both
    # --- structured fields that make the record editor-consumable (§7) ---
    observed: dict | None = None  # the FIGURE side  {source, coord?, cell?, symbol?, value?}
    expected: dict | None = None  # the TABLE side   (same shape) — the two candidates to choose
    target: str | None = None     # RFC6901 JSON Pointer into the draft (element concerned)
    actions: list = field(default_factory=list)  # [{kind, label, params}] machine-actionable fixes
    uid: str = ""                 # deterministic content fingerprint (editor state key)

    def sort_key(self) -> tuple:
        w = self.where or {}
        cell = w.get("cell") or [10**6, 10**6]
        return (self.map, self.id, w.get("row", 10**6), cell[0], cell[1], self.message)

    def fingerprint(self) -> str:
        raw = json.dumps([self.id, self.map, self.where, self.message],
                         ensure_ascii=False, sort_keys=True)
        return self.id + "-" + hashlib.blake2s(raw.encode("utf-8"), digest_size=4).hexdigest()


def _act(kind: str, label: str, **params) -> dict:
    assert kind in ACTION_KINDS, kind
    a = {"kind": kind, "label": label}
    if params:
        a["params"] = params
    return a


# --------------------------------------------------------------------------- #
# Parsed model
# --------------------------------------------------------------------------- #
@dataclass
class TableEntry:
    """A row of a COORDINATE table: named element with a col/row extent."""
    name: str
    col: tuple[int, int]          # 1-based inclusive (start, end)
    row: tuple[int, int]          # 1-based inclusive (start, end)
    note: str = ""


@dataclass
class PgPos:
    """A '**Name:** Col X, Riga Y' line (a single point, 1-based)."""
    name: str
    col: int
    row: int
    extra: str = ""


@dataclass
class ParsedMap:
    index: int                    # 1-based
    title: str
    matrix: list[list[str]]       # [y][x] symbol; actual dims (0-based rows)
    declared_dims: tuple[int, int] | None   # (cols, rows) from header
    scale_m: float
    tables: list[TableEntry]
    pg: list[PgPos]
    raw_lines: list[str]          # raw grid-block lines (for raw-glyph rules)
    north: str = "N"

    @property
    def actual_dims(self) -> tuple[int, int]:
        cols = max((len(r) for r in self.matrix), default=0)
        return cols, len(self.matrix)

    def cell(self, x: int, y: int) -> str | None:
        if 0 <= y < len(self.matrix) and 0 <= x < len(self.matrix[y]):
            return self.matrix[y][x]
        return None


# --------------------------------------------------------------------------- #
# F1 — grid parser (reuse render_map_svg)
# --------------------------------------------------------------------------- #
_SCALE_RE = re.compile(r"([\d]+[.,]?\d*)\s*m\s*/\s*quadr", re.IGNORECASE)


def _iter_grid_blocks(md_text: str) -> list[list[str]]:
    """Raw lines of every fenced block that render_map_svg accepts as a grid.

    Mirrors extract_maps' selection (>=3 parsed rows, honouring
    `<!-- render: none -->`) so raw blocks align 1:1 with the structured maps.
    """
    blocks: list[list[str]] = []
    in_fence = False
    skip_next = False
    block: list[str] = []
    for line in md_text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            if in_fence:
                if not skip_next:
                    grid = rms.parse_block(block)
                    if grid and len(grid["rows"]) >= 3:
                        blocks.append(block)
                block = []
                skip_next = False
            in_fence = not in_fence
            continue
        if in_fence:
            block.append(line)
        elif re.search(r"render:\s*none", s, re.IGNORECASE):
            skip_next = True
        elif s:
            skip_next = False
    return blocks


def _matrix_from_grid(grid: dict) -> list[list[str]]:
    """render_map_svg grid dict → dense 0-based matrix (rows in printed order)."""
    rows = grid["rows"]
    if not rows:
        return []
    nums = sorted(rows)
    n_cols = max(len(c) for c in rows.values())
    matrix: list[list[str]] = []
    for n in range(nums[0], nums[-1] + 1):
        cells = list(rows.get(n, []))
        cells += [DEFAULT_BASE_TERRAIN] * (n_cols - len(cells))  # pad short rows
        matrix.append(cells[:n_cols])
    return matrix


def _file_dims(md_text: str) -> tuple[int, int] | None:
    """Fallback for a `**Dimensioni:** ... (N colonne × M righe)` line that sits
    OUTSIDE the fenced block (parse_block only sees the in-fence banner)."""
    m = rms._DIMS_RE.search(md_text)
    return (int(m.group(1)), int(m.group(2))) if m else None


def parse_maps(md_text: str) -> list[ParsedMap]:
    grids = rms.extract_maps(md_text)
    raw_blocks = _iter_grid_blocks(md_text)
    tables = _parse_tables(md_text)
    pg = _parse_pg_positions(md_text)
    file_dims = _file_dims(md_text)
    parsed: list[ParsedMap] = []
    for i, g in enumerate(grids):
        raw = raw_blocks[i] if i < len(raw_blocks) else []
        scale = g.get("scale_m") or _scan_scale(raw) or DEFAULT_SCALE
        # in-fence banner dims win; else the file-level **Dimensioni:** line
        # (assigned to the first map only, to avoid mis-attributing on multi-map files)
        declared = g.get("declared_dims") or (file_dims if i == 0 else None)
        parsed.append(ParsedMap(
            index=i + 1,
            title=g.get("title") or f"Mappa {i + 1}",
            matrix=_matrix_from_grid(g),
            declared_dims=declared,
            scale_m=scale,
            # the coordinate tables/PG lists live OUTSIDE the fence and describe
            # the whole file; on a single-map file (the usual ultra-clear) they
            # belong to it. On a multi-map file they attach to the first map and
            # are reported (INFO) rather than mis-split.
            tables=tables if i == 0 else [],
            pg=pg if i == 0 else [],
            raw_lines=raw,
            north=_scan_north(raw),
        ))
    return parsed


def _scan_scale(raw_lines: list[str]) -> float | None:
    for line in raw_lines:
        m = _SCALE_RE.search(line)
        if m:
            try:
                return float(m.group(1).replace(",", "."))
            except ValueError:
                pass
    return None


def _scan_north(raw_lines: list[str]) -> str:
    for line in raw_lines[:6]:
        up = line.upper()
        if "NORD" in up and ("↑" in line or "TOP" in up):
            return "N"
    return "N"


# --------------------------------------------------------------------------- #
# F2 — table + PG parser (heuristic, conservative)
# --------------------------------------------------------------------------- #
_RANGE_RE = re.compile(r"(\d{1,3})\s*[-–]\s*(\d{1,3})")
_INT_RE = re.compile(r"\d{1,3}")
_PG_RE = re.compile(r"col\.?\s*(\d{1,3})\s*,\s*rig[ah]\.?\s*(\d{1,3})", re.IGNORECASE)


def _parse_extent(text: str) -> tuple[int, int] | None:
    """'18-21' -> (18,21); '60' -> (60,60); '01-120' -> (1,120)."""
    text = text.strip()
    m = _RANGE_RE.search(text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return (min(a, b), max(a, b))
    m = _INT_RE.search(text)
    if m:
        v = int(m.group(0))
        return (v, v)
    return None


def _split_md_row(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    cells = [c.strip() for c in s.strip("|").split("|")]
    return cells if len(cells) >= 2 else None


def _parse_tables(md_text: str) -> list[TableEntry]:
    """Markdown tables whose header carries COLONNE and RIGHE columns."""
    lines = md_text.splitlines()
    entries: list[TableEntry] = []
    i = 0
    while i < len(lines):
        cells = _split_md_row(lines[i])
        if cells:
            header = [c.upper() for c in cells]
            col_i = next((k for k, h in enumerate(header) if "COLONN" in h), None)
            row_i = next((k for k, h in enumerate(header) if "RIGH" in h), None)
            name_i = next((k for k, h in enumerate(header)
                           if any(w in h for w in ("STRUTTURA", "ELEMENTO", "NOME"))), 0)
            note_i = next((k for k, h in enumerate(header) if "NOTE" in h), None)
            if col_i is not None and row_i is not None:
                i += 1
                if i < len(lines) and set(lines[i].strip()) <= set("|-: "):
                    i += 1  # skip the |---|---| separator row
                while i < len(lines):
                    body = _split_md_row(lines[i])
                    if not body or len(body) <= max(col_i, row_i):
                        break
                    name = re.sub(r"[*`]", "", body[name_i]).strip()
                    col = _parse_extent(body[col_i])
                    row = _parse_extent(body[row_i])
                    note = body[note_i].strip() if note_i is not None and note_i < len(body) else ""
                    if name and col and row:
                        entries.append(TableEntry(name=name, col=col, row=row, note=note))
                    i += 1
                continue
        i += 1
    return entries


def _parse_pg_positions(md_text: str) -> list[PgPos]:
    """Prose bullets '**Name:** Col X, Riga Y (extra)'. First occurrence per name."""
    out: list[PgPos] = []
    seen: set[str] = set()
    for line in md_text.splitlines():
        s = line.strip().lstrip("-*• ").strip()
        m = _PG_RE.search(s)
        if not m:
            continue
        name = re.split(r":", s, 1)[0]
        name = re.sub(r"[*`]", "", name).strip()
        if not name or len(name) > 60 or name.lower() in seen:
            continue
        extra = s[m.end():].strip(" ()")
        out.append(PgPos(name=name, col=int(m.group(1)), row=int(m.group(2)), extra=extra))
        seen.add(name.lower())
    return out


# --------------------------------------------------------------------------- #
# geometry helpers
# --------------------------------------------------------------------------- #
def _rect_decompose(cells: set[tuple[int, int]]) -> list[tuple[int, int, int, int]]:
    """Cover a cell set with axis-aligned rectangles (deterministic greedy)."""
    remaining = set(cells)
    rects: list[tuple[int, int, int, int]] = []
    while remaining:
        x0, y0 = min(remaining, key=lambda p: (p[1], p[0]))
        w = 0
        while (x0 + w, y0) in remaining:
            w += 1
        h = 0
        while all((xx, y0 + h) in remaining for xx in range(x0, x0 + w)):
            h += 1
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                remaining.discard((xx, yy))
        rects.append((x0, y0, w, h))
    return rects


def _components(cells: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    """4-connected components (deterministic order)."""
    seen: set[tuple[int, int]] = set()
    comps: list[set[tuple[int, int]]] = []
    for start in sorted(cells):
        if start in seen:
            continue
        stack = [start]
        comp: set[tuple[int, int]] = set()
        while stack:
            p = stack.pop()
            if p in seen:
                continue
            seen.add(p)
            comp.add(p)
            x, y = p
            for nb in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if nb in cells and nb not in seen:
                    stack.append(nb)
        comps.append(comp)
    return comps


def _bbox(cells: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1


def _to_rect(col: tuple[int, int], row: tuple[int, int]) -> list[int]:
    """1-based inclusive col/row extents -> 0-based [x, y, w, h]."""
    x = col[0] - 1
    y = row[0] - 1
    w = col[1] - col[0] + 1
    h = row[1] - row[0] + 1
    return [x, y, w, h]


def _leading_count(*texts: str) -> int | None:
    for t in texts:
        m = re.search(r"\b(\d{1,4})\b", t or "")
        if m and any(w in (t or "").lower() for w in TROOP_WORDS):
            return int(m.group(1))
    return None


def _role_token(name: str) -> str:
    low = name.lower()
    for pat, tok in UNIT_KEYWORDS:
        if re.search(pat, low):
            return tok
    return DEFAULT_PG_TOKEN


# --------------------------------------------------------------------------- #
# F4 — draft emission
# --------------------------------------------------------------------------- #
def _most_common_fill(matrix: list[list[str]]) -> str:
    counts: dict[str, int] = {}
    for row in matrix:
        for s in row:
            if s in FILL_SYMS:
                counts[s] = counts.get(s, 0) + 1
    if not counts:
        return DEFAULT_BASE_TERRAIN
    # deterministic: highest count, then legend order
    return sorted(counts, key=lambda s: (-counts[s], s))[0]


def _emit_from_grid(pmap: ParsedMap) -> tuple[dict, list[str]]:
    """Draft built from the emoji grid alone (the reliable path for a uniform
    ultra-clear). Every `fill` symbol becomes terrain, every unit token a unit
    block, every icon a structure/hazard."""
    matrix = pmap.matrix
    cols, rows = pmap.actual_dims
    base = _most_common_fill(matrix)
    notes: list[str] = []

    by_sym: dict[str, set[tuple[int, int]]] = {}
    for y, row in enumerate(matrix):
        for x, s in enumerate(row):
            by_sym.setdefault(s, set()).add((x, y))

    regions, structures, hazards, units = [], [], [], []
    for sym in sorted(by_sym):
        cells = by_sym[sym]
        if sym in FILL_SYMS:
            if sym == base:
                continue
            for (x, y, w, h) in _rect_decompose(cells):
                regions.append({"terrain": sym, "rect": [x, y, w, h],
                                "label": SYMBOLS[sym].get("it", "")})
        elif sym in UNIT_SYMS:
            for comp in _components(cells):
                if len(comp) == 1:
                    (x, y) = next(iter(comp))
                    units.append({"token": sym, "at": [x, y],
                                  "name": SYMBOLS[sym].get("it", "")})
                else:
                    bx, by, bw, bh = _bbox(comp)
                    units.append({"token": sym, "area": {"rect": [bx, by, bw, bh]},
                                  "quantity": len(comp), "name": SYMBOLS[sym].get("it", "")})
        elif sym in ICON_SYMS:
            bucket = hazards if sym in HAZARD_SYMS else structures
            key = "type"
            for comp in _components(cells):
                if len(comp) == 1:
                    (x, y) = next(iter(comp))
                    bucket.append({key: sym, "at": [x, y]})
                else:
                    bx, by, bw, bh = _bbox(comp)
                    bucket.append({key: sym, "rect": [bx, by, bw, bh]})
        # non-legend symbols are handled by rule R3 and dropped from geometry

    draft = _assemble(pmap, [cols, rows], base, regions, structures, hazards, units, notes,
                      source="griglia emoji (figura)")
    return draft, notes


def _emit_from_tables(pmap: ParsedMap, map_size: list[int]) -> tuple[dict, list[str]]:
    """Draft rebuilt from the authoritative coordinate tables — used when the
    grid is unusable (D1). Role/symbol come from a documented keyword map; every
    assignment is echoed into `notes` so the human verifies (never hidden)."""
    base = _most_common_fill(pmap.matrix) if any(pmap.matrix) else DEFAULT_BASE_TERRAIN
    notes = ["Bozza ricostruita dai DATI AUTORITATIVI (tabelle coordinate), "
             "non dal disegno ASCII: la griglia divergeva dall'header (vedi conflitti)."]
    regions, structures, hazards, units = [], [], [], []

    for e in pmap.tables:
        rect = _to_rect(e.col, e.row)
        low = e.name.lower()
        role, sym = "structure", "⬛"
        for kw, r, s in STRUCT_KEYWORDS:
            if kw in low:
                role, sym = r, s
                break
        if role == "region" and "cortile" in low and "estern" in low:
            sym = "🟨"
        elif "cortile" in low:
            role, sym = "region", ("🟨" if "estern" in low else "🟩")

        count = _leading_count(e.name, e.note)
        if role == "region":
            regions.append({"terrain": sym, "rect": rect, "label": e.name})
        else:
            entry = {"type": sym}
            if rect[2] == 1 and rect[3] == 1:
                entry["at"] = [rect[0], rect[1]]
            else:
                entry["rect"] = rect
            entry["label"] = e.name + (f" — {e.note}" if e.note else "")
            structures.append(entry)
        if count is not None:
            units.append({"faction": "", "name": f"{e.name} ({count})",
                          "token": DEFAULT_TROOP_TOKEN,
                          "area": {"rect": rect}, "quantity": count})
        notes.append(f"[ruolo dedotto] «{e.name}» → {role} {sym} "
                     f"(col {e.col[0]}-{e.col[1]}, riga {e.row[0]}-{e.row[1]}) — verificare.")

    for p in pmap.pg:
        token = _role_token(p.name + " " + p.extra)
        units.append({"faction": "", "name": p.name + (f" — {p.extra}" if p.extra else ""),
                      "token": token, "at": [p.col - 1, p.row - 1], "cr": "PG"})

    draft = _assemble(pmap, map_size, base, regions, structures, hazards, units, notes,
                      source="tabelle coordinate (dati autoritativi)")
    return draft, notes


def _assemble(pmap, map_size, base, regions, structures, hazards, units, notes, source):
    draft: dict = {
        "schema_version": SCHEMA_VERSION,
        "title": pmap.title[:100],
        "scale_m_per_square": pmap.scale_m,
        "units_in": "squares",
        "map_size": map_size,
        "base_terrain": base,
        "north": pmap.north,
    }
    if regions:
        draft["regions"] = regions
    if structures:
        draft["structures"] = structures
    if hazards:
        draft["hazards"] = hazards
    if units:
        draft["units"] = units
    head = [f"Bozza generata da import_ultraclear da «{pmap.title}» (fonte: {source})."]
    draft["notes"] = head + list(notes)
    return draft


def build_draft(pmap: ParsedMap, grid_usable: bool) -> dict:
    if grid_usable or not pmap.tables:
        declared = pmap.declared_dims
        cols, rows = pmap.actual_dims
        # a usable grid keeps its declared header dims when they hold, else the
        # real cell extent — never a size the geometry doesn't fit in.
        if declared and declared[0] >= cols and declared[1] >= rows:
            size = list(declared)
        else:
            size = [max(1, cols), max(1, rows)]
        draft, _ = _emit_from_grid(pmap)
        draft["map_size"] = size
        return draft
    # grid unusable + tables present → authoritative table reconstruction
    if pmap.declared_dims:
        size = list(pmap.declared_dims)
    else:
        max_c = max((e.col[1] for e in pmap.tables), default=1)
        max_r = max((e.row[1] for e in pmap.tables), default=1)
        size = [max_c, max_r]
    draft, _ = _emit_from_tables(pmap, size)
    return draft


# --------------------------------------------------------------------------- #
# F3 — conflict rules (registry R1..R10)
# --------------------------------------------------------------------------- #
@dataclass
class Ctx:
    pmap: ParsedMap
    draft: dict
    grid_usable: bool


def _nfc_strip(ch: str) -> str:
    """Drop variation selectors / ZWJ and NFC-normalise a single glyph."""
    return unicodedata.normalize("NFC", "".join(
        c for c in ch if ord(c) not in (0xFE0F, 0x200D)))


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def rule_grid_header(ctx: Ctx) -> list[Conflict]:
    p = ctx.pmap
    if not p.declared_dims or not any(p.matrix):
        return []
    dc, dr = p.declared_dims
    ac, ar = p.actual_dims
    out = []
    if ac != dc or ar != dr:
        out.append(Conflict(
            "R1", "grid-header-mismatch", "ERROR", map=p.index, source="both",
            where={"row": len(p.matrix)},
            message=(f"header dichiara {dc}×{dr} quadretti ma la griglia disegnata "
                     f"misura {ac}×{ar} (celle reali)"),
            suggestion=("la figura ASCII diverge dai dati: la bozza usa i dati "
                        "autoritativi (tabelle) — riallineare la griglia o l'header"),
            observed={"source": "grid", "value": [ac, ar]},
            expected={"source": "table", "value": [dc, dr]},
            target="/map_size",
            actions=[_act("use_table", f"Usa dimensioni dichiarate {dc}×{dr}", to=[dc, dr]),
                     _act("resize_map", f"Ridimensiona a {ac}×{ar} (celle reali)", to=[ac, ar]),
                     _act("ignore", "Ignora")]))
    return out


def rule_nonuniform(ctx: Ctx) -> list[Conflict]:
    p = ctx.pmap
    if not any(p.matrix):
        return []
    widths = [len([c for c in row]) for row in p.matrix]
    # use the pre-pad widths from raw parse is hard; approximate with trimmed base
    trimmed = []
    for row in p.matrix:
        n = len(row)
        while n > 0 and row[n - 1] == DEFAULT_BASE_TERRAIN:
            n -= 1
        trimmed.append(n)
    if not trimmed:
        return []
    mode = max(set(trimmed), key=trimmed.count)
    out = []
    for y, w in enumerate(trimmed):
        if w and abs(w - mode) > 2:
            out.append(Conflict(
                "R2", "grid-nonuniform-rows", "WARN", map=p.index, source="grid",
                where={"row": y + 1},
                message=f"riga {y + 1}: {w} celle (le altre righe ne hanno ~{mode})",
                suggestion="riga di larghezza anomala — probabile drift del disegno"))
    return out[:20]  # cap the noise


def rule_symbol_legend(ctx: Ctx) -> list[Conflict]:
    p = ctx.pmap
    out: list[Conflict] = []
    seen_raw: set[str] = set()
    # (a) variation-selector / near-match on the RAW glyphs (parse_row_cells
    # strips U+FE0F, so this must look at the raw block text — that is D2).
    for raw in p.raw_lines:
        for m in re.finditer(r"(.)[️‍]+", raw):
            base = m.group(1)
            if base in seen_raw:
                continue
            seen_raw.add(base)
            norm = _nfc_strip(m.group(0))
            if norm in SYMBOLS and (m.group(0) not in SYMBOLS):
                out.append(Conflict(
                    "R3", "symbol-not-in-legend", "WARN", map=p.index, source="grid",
                    message=(f"simbolo '{m.group(0)}' con variation-selector non è in "
                             f"legenda; il canonico '{norm}' sì"),
                    suggestion=f"sostituire con il simbolo canonico '{norm}'",
                    observed={"source": "grid", "symbol": m.group(0)},
                    expected={"source": "legend", "symbol": norm},
                    actions=[_act("replace_symbol", f"Sostituisci con '{norm}'",
                                  **{"from": m.group(0), "to": norm}),
                             _act("ignore", "Ignora")]))
    # (b) genuinely unknown glyphs left in the parsed matrix
    unknown: set[str] = set()
    for y, row in enumerate(p.matrix):
        for x, s in enumerate(row):
            if s not in SYMBOLS and s not in unknown:
                unknown.add(s)
                norm = _nfc_strip(s)
                sev = "WARN" if norm in SYMBOLS else "ERROR"
                sug = (f"usare il canonico '{norm}'" if norm in SYMBOLS
                       else "aggiungere il simbolo alla legenda o correggerlo")
                acts = [_act("ignore", "Ignora")]
                if norm in SYMBOLS:
                    acts.insert(0, _act("replace_symbol", f"Sostituisci con '{norm}'",
                                        **{"from": s, "to": norm}))
                out.append(Conflict(
                    "R3", "symbol-not-in-legend", sev, map=p.index, source="grid",
                    where={"cell": [x, y], "coord": _coord(x, y)},
                    message=f"simbolo '{s}' assente dalla legenda universale",
                    suggestion=sug,
                    observed={"source": "grid", "cell": [x, y], "symbol": s},
                    expected=({"source": "legend", "symbol": norm} if norm in SYMBOLS else None),
                    actions=acts))
    return out


def rule_drift(ctx: Ctx) -> list[Conflict]:
    """D4: a named token declared at a table coord but the grid cell there is
    not a unit token (or is out of the drawn area)."""
    p = ctx.pmap
    if not any(p.matrix):
        return []
    out = []
    for pos in p.pg:
        x, y = pos.col - 1, pos.row - 1
        if y >= len(p.matrix):
            continue
        cell = p.cell(x, y)
        coord = _coord(x, y)
        if cell is None:
            out.append(Conflict(
                "R4", "annotation-coord-drift", "WARN", map=p.index, source="both",
                where={"cell": [x, y], "coord": coord},
                message=(f"«{pos.name}» dichiarato a col {pos.col}, riga {pos.row} ma "
                         f"quella cella è fuori dalla griglia disegnata"),
                suggestion="la figura non arriva a quelle coordinate — usare la tabella",
                observed={"source": "grid", "cell": [x, y], "symbol": None},
                expected={"source": "table", "cell": [x, y], "coord": coord, "name": pos.name},
                actions=[_act("use_table", "Colloca ai dati dichiarati (tabella)"),
                         _act("ignore", "Ignora")]))
        elif cell not in UNIT_SYMS:
            out.append(Conflict(
                "R4", "annotation-coord-drift", "WARN", map=p.index, source="both",
                where={"cell": [x, y], "coord": coord},
                message=(f"«{pos.name}» dichiarato a col {pos.col}, riga {pos.row} ma la "
                         f"griglia lì mostra '{cell}', non un token unità"),
                suggestion="drift figura↔tabella: la bozza colloca il token ai dati dichiarati",
                observed={"source": "grid", "cell": [x, y], "symbol": cell},
                expected={"source": "table", "cell": [x, y], "coord": coord, "name": pos.name},
                actions=[_act("use_table", "Colloca ai dati dichiarati (tabella)"),
                         _act("use_grid", f"Tieni la figura ('{cell}' resta terreno)"),
                         _act("ignore", "Ignora")]))
    return out[:20]


_STOP_WORDS = {"madre", "padre", "re", "sir", "lord", "lady", "capitano", "bastione",
               "torre", "porta", "muro", "mura", "cortile", "nord", "sud", "est", "ovest"}


def _key_words(name: str) -> list[str]:
    """Significant name tokens (>=4 chars, not a title/role word)."""
    return [w for w in re.findall(r"[a-zàèéìòù]+", name.lower())
            if len(w) >= 4 and w not in _STOP_WORDS]


def rule_name_collision(ctx: Ctx) -> list[Conflict]:
    """D3: near-identical names at different coordinates (Dara vs Dana)."""
    p = ctx.pmap
    named: list[tuple[str, int, int]] = [(e.name, e.col[0], e.row[0]) for e in p.tables]
    named += [(pos.name, pos.col, pos.row) for pos in p.pg]
    out = []
    reported: set[tuple[str, str]] = set()
    for i in range(len(named)):
        for j in range(i + 1, len(named)):
            (na, ca, ra), (nb, cb, rb) = named[i], named[j]
            if (ca, ra) == (cb, rb):
                continue
            # compare every significant word of A against every one of B
            hit = next(((wa, wb) for wa in _key_words(na) for wb in _key_words(nb)
                        if wa != wb and _levenshtein(wa, wb) == 1), None)
            if not hit:
                continue
            key = tuple(sorted((na.lower(), nb.lower())))
            if key in reported:
                continue
            reported.add(key)
            out.append(Conflict(
                "R5", "name-collision", "WARN", map=p.index, source="table",
                where={"coord": f"{ca},{ra} · {cb},{rb}"},
                message=(f"nomi simili a coordinate diverse: «{na}» (col {ca}, riga {ra}) "
                         f"vs «{nb}» (col {cb}, riga {rb}) — «{hit[0]}»/«{hit[1]}»"),
                suggestion="confermare che siano due entità distinte (non uno scambio)",
                observed={"source": "table", "name": na, "cell": [ca - 1, ra - 1]},
                expected={"source": "table", "name": nb, "cell": [cb - 1, rb - 1]},
                actions=[_act("confirm_distinct", "Sono due entità distinte"),
                         _act("rename", f"Rinomina «{na}»", name=na),
                         _act("rename", f"Rinomina «{nb}»", name=nb)]))
    return out


def rule_oob(ctx: Ctx) -> list[Conflict]:
    """R6: a table coordinate outside the chosen map_size."""
    size = ctx.draft.get("map_size")
    if not (isinstance(size, list) and len(size) == 2):
        return []
    cols, rows = size
    out = []
    for e in ctx.pmap.tables:
        if e.col[1] > cols or e.row[1] > rows:
            out.append(Conflict(
                "R6", "coord-out-of-bounds", "ERROR", map=ctx.pmap.index, source="table",
                where={"coord": f"{e.col}/{e.row}"},
                message=(f"«{e.name}»: estensione col {e.col}, riga {e.row} fuori dalla "
                         f"griglia {cols}×{rows}"),
                suggestion="correggere la coordinata o le dimensioni della mappa"))
    for pos in ctx.pmap.pg:
        if pos.col > cols or pos.row > rows:
            out.append(Conflict(
                "R6", "coord-out-of-bounds", "ERROR", map=ctx.pmap.index, source="table",
                where={"coord": f"{pos.col}/{pos.row}"},
                message=(f"«{pos.name}»: col {pos.col}, riga {pos.row} fuori dalla "
                         f"griglia {cols}×{rows}"),
                suggestion="correggere la coordinata o le dimensioni della mappa"))
    return out


def rule_overlap(ctx: Ctx) -> list[Conflict]:
    """R7: two point-structures on the same cell (ambiguous precedence)."""
    seen: dict[tuple[int, int], str] = {}
    out = []
    for st in ctx.draft.get("structures", []) or []:
        if "at" in st:
            key = tuple(st["at"])
            if key in seen:
                out.append(Conflict(
                    "R7", "overlapping-structures", "INFO", map=ctx.pmap.index, source="grid",
                    where={"cell": list(key)},
                    message=f"due strutture sulla cella {list(key)}: '{seen[key]}' e '{st['type']}'",
                    suggestion="precedenza ambigua — tenerne una o spostarle"))
            else:
                seen[key] = st["type"]
    return out


def rule_quantity(ctx: Ctx) -> list[Conflict]:
    """R8: a unit's written quantity differs from the cells it occupies."""
    out = []
    for i, u in enumerate(ctx.draft.get("units", []) or []):
        name = u.get("name", "")
        written = u.get("quantity")
        if written is None or "area" not in u:
            continue
        rect = u["area"]["rect"]
        occupied = rect[2] * rect[3]
        if abs(written - occupied) > max(2, occupied // 5):
            out.append(Conflict(
                "R8", "quantity-mismatch", "WARN", map=ctx.pmap.index, source="both",
                where={"rect": rect},
                message=(f"«{name}»: dichiarati {written} ma l'area occupa {occupied} quadretti"),
                suggestion="la quantità è un dato del companion, non un token per creatura",
                observed={"source": "grid", "value": occupied},
                expected={"source": "table", "value": written},
                target=f"/units/{i}",
                actions=[_act("set_quantity", f"Usa il numero dichiarato ({written})", to=written),
                         _act("ignore", "Ignora (area = astrazione)")]))
    return out


def rule_non_emoji(ctx: Ctx) -> list[Conflict]:
    """R9: a non-emoji glyph sitting inside the parsed cell matrix."""
    out = []
    seen: set[str] = set()
    for y, row in enumerate(ctx.pmap.matrix):
        for x, s in enumerate(row):
            if s and not rms.is_emoji_char(s[0]) and s not in seen:
                seen.add(s)
                out.append(Conflict(
                    "R9", "non-emoji-cell", "WARN", map=ctx.pmap.index, source="grid",
                    where={"cell": [x, y]},
                    message=f"cella non-emoji '{s}' dentro la matrice",
                    suggestion="rimuovere il carattere spurio dalla griglia"))
    return out


def rule_schematic(ctx: Ctx) -> list[Conflict]:
    """R10: informational — schematic/side-view blocks are deliberately skipped
    (handled upstream by the `render: none` marker / non-grid fences)."""
    return []


RULES = [rule_grid_header, rule_nonuniform, rule_symbol_legend, rule_drift,
         rule_name_collision, rule_oob, rule_overlap, rule_quantity,
         rule_non_emoji, rule_schematic]


def _coord(x: int, y: int) -> str:
    return f"{rms.col_label(x)}{y + 1}"


def diagnose(pmap: ParsedMap, grid_usable: bool, draft: dict) -> list[Conflict]:
    ctx = Ctx(pmap=pmap, draft=draft, grid_usable=grid_usable)
    conflicts: list[Conflict] = []
    for rule in RULES:
        conflicts.extend(rule(ctx))
    conflicts.sort(key=lambda c: c.sort_key())
    for c in conflicts:
        c.uid = c.fingerprint()   # stable editor-state key (order-independent content hash)
    return conflicts


def grid_is_usable(pmap: ParsedMap) -> bool:
    if not any(pmap.matrix):
        return False
    if not pmap.declared_dims:
        return True
    dc, dr = pmap.declared_dims
    ac, ar = pmap.actual_dims
    return ac == dc and ar == dr


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #
def render_report_md(pmap: ParsedMap, conflicts: list[Conflict]) -> str:
    lines = [f"# Report conflitti — {pmap.title}", ""]
    counts = {sev: sum(1 for c in conflicts if c.severity == sev)
              for sev in ("ERROR", "WARN", "INFO")}
    lines.append(f"- **ERROR**: {counts['ERROR']} · **WARN**: {counts['WARN']} "
                 f"· **INFO**: {counts['INFO']}")
    dc = f"{pmap.declared_dims[0]}×{pmap.declared_dims[1]}" if pmap.declared_dims else "—"
    ac0, ar0 = pmap.actual_dims
    lines.append(f"- griglia dichiarata: {dc} · celle reali: {ac0}×{ar0} "
                 f"· tabelle: {len(pmap.tables)} · posizioni PG: {len(pmap.pg)}")
    lines.append("")
    if not conflicts:
        lines.append("_Nessun conflitto rilevato._")
        return "\n".join(lines) + "\n"
    lines.append("| Sev | Regola | Dove | Messaggio | Suggerimento |")
    lines.append("|---|---|---|---|---|")
    for c in conflicts:
        where = ""
        if c.where.get("coord"):
            where = str(c.where["coord"])
        elif c.where.get("cell"):
            where = _coord(c.where["cell"][0], c.where["cell"][1])
        elif c.where.get("row"):
            where = f"riga {c.where['row']}"
        msg = c.message.replace("|", "\\|")
        sug = c.suggestion.replace("|", "\\|")
        lines.append(f"| {c.severity} | {c.id} {c.rule} | {where} | {msg} | {sug} |")
    return "\n".join(lines) + "\n"


def _conflict_dict(c: Conflict) -> dict:
    """Ordered, None/empty-stripped record — stable bytes for the editor."""
    d = asdict(c)
    ordered = {"uid": d["uid"], "id": d["id"], "rule": d["rule"],
               "severity": d["severity"], "map": d["map"], "source": d["source"],
               "message": d["message"], "suggestion": d["suggestion"],
               "where": d["where"], "observed": d["observed"], "expected": d["expected"],
               "target": d["target"], "actions": d["actions"]}
    return {k: v for k, v in ordered.items() if v not in (None, {}, [], "")}


def _report_payload(pmap: ParsedMap, conflicts: list[Conflict]) -> dict:
    counts = {sev: sum(1 for c in conflicts if c.severity == sev)
              for sev in ("ERROR", "WARN", "INFO")}
    return {
        "report_version": REPORT_VERSION,
        "tool": "import_ultraclear.py",
        "map": pmap.index,
        "title": pmap.title,
        "declared_dims": list(pmap.declared_dims) if pmap.declared_dims else None,
        "actual_dims": list(pmap.actual_dims),
        "source_of_truth": "table",   # DEFAULT policy: table wins on grid↔table divergence
        "counts": counts,
        "conflicts": [_conflict_dict(c) for c in conflicts],
    }


def render_report_json(pmap: ParsedMap, conflicts: list[Conflict]) -> str:
    return json.dumps(_report_payload(pmap, conflicts), ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def process(pmap: ParsedMap) -> tuple[dict, list[Conflict]]:
    usable = grid_is_usable(pmap)
    draft = build_draft(pmap, usable)
    conflicts = diagnose(pmap, usable, draft)
    return draft, conflicts


def _dumps(draft: dict) -> str:
    return json.dumps(draft, ensure_ascii=False, indent=2, sort_keys=False)


def _validate_draft(draft: dict) -> list[str]:
    """Run the real contract validator; return the list of errors (empty = ok)."""
    try:
        spec = cmj.normalize_units(json.loads(_dumps(draft)))
        cmj.validate(spec)
        return []
    except cmj.SpecError as e:
        return str(e).splitlines()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="master ultra-clear (.md)")
    ap.add_argument("-o", "--output", help="bozza JSON (default: stdout)")
    ap.add_argument("--conflicts", help="report leggibile (markdown); default: stderr")
    ap.add_argument("--json-report", help="report machine-readable (.conflicts.json)")
    ap.add_argument("--emit-md", metavar="DIR",
                    help="compila subito la bozza in un master .md nella cartella DIR")
    ap.add_argument("--map", type=int, help="se il file ha più mappe, quale importare (1-based)")
    ap.add_argument("--strict", action="store_true", help="i WARN diventano fatali (CI severa)")
    ap.add_argument("-q", "--quiet", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    try:
        md = Path(args.input).read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERRORE: impossibile leggere {args.input}: {e}", file=sys.stderr)
        return 2

    maps = parse_maps(md)
    if not maps:
        print(f"ERRORE: nessuna mappa a griglia trovata in {args.input}", file=sys.stderr)
        return 2

    if args.map is not None:
        if not (1 <= args.map <= len(maps)):
            print(f"ERRORE: --map {args.map} fuori range (1..{len(maps)})", file=sys.stderr)
            return 2
        maps = [maps[args.map - 1]]

    multi = len(maps) > 1
    drafts, all_conflicts = [], []
    for pmap in maps:
        draft, conflicts = process(pmap)
        drafts.append(draft)
        all_conflicts.extend(conflicts)

    # --- write the draft(s) ---
    if multi:
        payload = _dumps({"maps": drafts})
    else:
        payload = _dumps(drafts[0])
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    # --- conflict reports ---
    report_md = "\n".join(render_report_md(m, [c for c in all_conflicts if c.map == m.index])
                          for m in maps)
    if args.conflicts:
        Path(args.conflicts).write_text(report_md, encoding="utf-8")
    elif not args.quiet:
        print(report_md, file=sys.stderr)
    if args.json_report:
        if multi:
            js = json.dumps({"maps": [json.loads(render_report_json(
                m, [c for c in all_conflicts if c.map == m.index])) for m in maps]},
                ensure_ascii=False, indent=2)
        else:
            js = render_report_json(maps[0], all_conflicts)
        Path(args.json_report).write_text(js + "\n", encoding="utf-8")

    # --- validate the emitted draft against the real contract ---
    errors = sum(1 for c in all_conflicts if c.severity == "ERROR")
    warns = sum(1 for c in all_conflicts if c.severity == "WARN")
    for draft in drafts:
        verr = _validate_draft(draft)
        if verr and args.verbose:
            print("Bozza non conforme al contratto:\n  - " + "\n  - ".join(verr),
                  file=sys.stderr)
        if verr:
            errors += 1

    # --- optional immediate compile (round-trip) ---
    if args.emit_md and not multi:
        outdir = Path(args.emit_md)
        outdir.mkdir(parents=True, exist_ok=True)
        stem = rms.slugify(maps[0].title)
        json_tmp = outdir / f"{stem}.draft.json"
        json_tmp.write_text(_dumps(drafts[0]) + "\n", encoding="utf-8")
        rc = cmj.main([str(json_tmp), "-o", str(outdir / f"{stem}.md")])
        if rc != 0:
            print(f"ERRORE: compile_map_json ha rifiutato la bozza (exit {rc})",
                  file=sys.stderr)
            return 2

    if not args.quiet:
        verdict = "✗ ERROR presenti — bozza da correggere" if errors else "✓ bozza compilabile"
        print(f"{verdict} (ERROR {errors}, WARN {warns})", file=sys.stderr)

    if errors:
        return 1
    if args.strict and warns:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
