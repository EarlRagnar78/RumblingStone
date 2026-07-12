#!/usr/bin/env python3
"""
render_map_svg.py — render the campaign's emoji-grid tactical maps to SVG.

The revised maps of ARC-07/08/09 (files `*Ultra-Clear*.md`, `*MAPPE*.md`,
`SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`, ...) share one format:
fenced code blocks whose rows start with a 2-digit row number followed by
emoji cells (with or without spaces). This script parses those grids and
emits print-quality SVG battlemaps in the "pergamena" (parchment) style:
procedurally textured terrain, inked hand-drawn boundaries, cast shadows on
walls/structures, VTT-style unit tokens, 1,5 m/quadretto grid, column
letters / row numbers, scale bar and legend — the same map for every arc,
in one style, regenerable whenever the markdown master changes.

Everything is generated procedurally (SVG patterns + filters): no external
image assets, no licensing constraints, byte-deterministic output (enforced
by scripts/validate_maps.py in CI).

The markdown grid stays the MASTER (human-readable, diffable, table-usable);
the SVG is a generated artifact. Never hand-edit the SVG.

Usage:
    python3 scripts/render_map_svg.py <file.md> [...]      # render all maps
    python3 scripts/render_map_svg.py <file.md> --list     # list maps found
    python3 scripts/render_map_svg.py <file.md> -o DIR     # output directory
    python3 scripts/render_map_svg.py <file.md> --map 2    # only map #2

Default output: a `rendered/` directory next to the input file,
one `<input-stem>_mapN_<slug>.svg` per map. Pure Python 3, no dependencies.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

CELL = 28          # px per grid square (1,5 m)
MARGIN = 46        # px around the grid for coordinates
LEGEND_ROW_H = 22  # px per legend row
MIN_WIDTH = 480    # px, so the legend never overflows on tiny maps

FONT = "Georgia, 'Palatino Linotype', 'Times New Roman', serif"
PAPER = "#efe4c9"       # parchment base
PLATE = "#e6d9b8"       # map plate behind the grid
INK = "#3b2e1e"         # dark ink
INK_SOFT = "#7a6a50"    # faded ink

# ---------------------------------------------------------------------------
# Symbol table — universal legend of the repo
# (SUPPLEMENTO-P1C drow maps + Ultra-Clear maps ARC-07/08).
# mode "fill":   textured terrain square ("pat" = procedural pattern id)
# mode "unit":   colored token circle (radial gradient + ink ring)
# mode "icon":   emoji glyph anchored by a ground blot; the underlying
#                terrain is inherited from the nearest terrain cell
# ---------------------------------------------------------------------------
SYMBOLS: dict[str, dict] = {
    # terrain (textured fills)
    "🌲": {"mode": "fill", "pat": "t_forest", "fill": "#55754d", "it": "Foresta densa (Furtività +5, copertura)"},
    "🌿": {"mode": "fill", "pat": "t_veg", "fill": "#9db97b", "it": "Vegetazione bassa"},
    "🟩": {"mode": "fill", "pat": "t_grass", "fill": "#b3c489", "it": "Pianura / area aperta"},
    "🟫": {"mode": "fill", "pat": "t_earth", "fill": "#b08d68", "it": "Terra battuta / sentiero"},
    "🟨": {"mode": "fill", "pat": "t_sand", "fill": "#e4cf9c", "it": "Sabbia / area segnalata"},
    "🟧": {"mode": "fill", "pat": "t_lava", "fill": "#d59650", "it": "Lava raffreddata / pericolo"},
    "🟥": {"mode": "fill", "pat": "t_lethal", "fill": "#b94a3c", "it": "Zona letale"},
    "🟦": {"mode": "fill", "pat": "t_deep", "fill": "#4c7ba3", "it": "Acqua profonda"},
    "🌊": {"mode": "fill", "pat": "t_water", "fill": "#6aa5c4", "it": "Acqua / corrente"},
    "⬛": {"mode": "fill", "pat": "t_struct", "fill": "#6b5b47", "it": "Struttura (tenda, edificio, dais)"},
    "⬜": {"mode": "fill", "pat": "t_floor", "fill": "#d8cdb4", "it": "Pavimento lavorato"},
    "🏰": {"mode": "fill", "pat": "t_wall", "fill": "#3f3931", "it": "Muro / roccia solida"},
    "🟪": {"mode": "fill", "pat": "t_pillar", "fill": "#8a67b5", "it": "Pilastro / mithral"},
    "🪨": {"mode": "icon", "fill": "#ced4da", "it": "Rocce/macerie (copertura +4 CA, terreno difficile)"},
    "🔥": {"mode": "icon", "fill": "#ffb4a2", "it": "Fuoco (1d6 fuoco/round)"},
    "💥": {"mode": "icon", "fill": "#ffb4a2", "it": "Fiamme / esplosione"},
    "💀": {"mode": "icon", "fill": "#e9ecef", "it": "Fossa / trappola"},
    "🕳": {"mode": "icon", "fill": "#495057", "it": "Voragine / buco"},
    # units (tokens)
    "🔵": {"mode": "unit", "fill": "#1d6fd8", "it": "PG / alleati"},
    "🔴": {"mode": "unit", "fill": "#d62828", "it": "Nemico standard"},
    "⚫": {"mode": "unit", "fill": "#212529", "it": "Boss / comandante"},
    "🟡": {"mode": "unit", "fill": "#f4b400", "it": "Incantatore nemico"},
    "🟢": {"mode": "unit", "fill": "#2b9348", "it": "Creatura evocata / bestia"},
    "🟣": {"mode": "unit", "fill": "#9d4edd", "it": "Creatura speciale"},
    # specials (icons)
    "🌳": {"mode": "icon", "fill": "#b7e4c7", "it": "Treant / creatura vegetale"},
    "⭐": {"mode": "icon", "fill": "#fff3b0", "it": "Obiettivo primario"},
    "🚪": {"mode": "icon", "fill": "#e6ccb2", "it": "Porta / ingresso"},
    "🗼": {"mode": "icon", "fill": "#dee2e6", "it": "Torre / struttura alta"},
    "🏺": {"mode": "icon", "fill": "#f8f9fa", "it": "Contenitore / bottino"},
    "🔔": {"mode": "icon", "fill": "#fff3b0", "it": "Allarme / trappola sonora"},
    "💎": {"mode": "icon", "fill": "#caf0f8", "it": "Tesoro / oggetto magico"},
    "👑": {"mode": "icon", "fill": "#fff3b0", "it": "Trono / Corona"},
    "🏮": {"mode": "icon", "fill": "#ffd166", "it": "Braciere / fonte di luce"},
    "🪓": {"mode": "icon", "fill": "#e9ecef", "it": "Rastrelliera / armi"},
    "🛏": {"mode": "icon", "fill": "#e9ecef", "it": "Giaciglio"},
    "📦": {"mode": "icon", "fill": "#e6ccb2", "it": "Casse / rifornimenti"},
    "🐴": {"mode": "icon", "fill": "#e6ccb2", "it": "Cavalcature"},
    "🕸": {"mode": "icon", "fill": "#dee2e6", "it": "Ragnatele (terreno difficile)"},
    "❄": {"mode": "icon", "fill": "#caf0f8", "it": "Ghiaccio"},
    "⚡": {"mode": "icon", "fill": "#fff3b0", "it": "Energia / pericolo magico"},
    "🌀": {"mode": "icon", "fill": "#caf0f8", "it": "Portale / vortice"},
}
DEFAULT_TERRAIN = {"mode": "fill", "fill": PAPER, "it": ""}

# walls, buildings and pillars cast a shadow and get the heavy ink outline
HEAVY_PATS = {"t_wall", "t_struct", "t_pillar"}

# ---------------------------------------------------------------------------
# Procedural texture patterns (pure SVG, deterministic — no external assets)
# ---------------------------------------------------------------------------


def _pattern(pid: str, tile: int, body: str) -> str:
    return (
        f'<pattern id="{pid}" width="{tile}" height="{tile}" '
        f'patternUnits="userSpaceOnUse">{body}</pattern>'
    )


def _canopy(cx: float, cy: float, r: float) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#435f3c"/>'
        f'<circle cx="{cx - r * 0.28}" cy="{cy - r * 0.3}" r="{r * 0.62}" fill="#5d7f53"/>'
        f'<circle cx="{cx - r * 0.4}" cy="{cy - r * 0.45}" r="{r * 0.26}" fill="#6f9163"/>'
    )


PATTERNS: dict[str, str] = {
    "t_grass": _pattern("t_grass", 28,
        '<rect width="28" height="28" fill="#b3c489"/>'
        '<path d="M5 21q1.5-4 3-5M8 21q0-3 2-5M20 8q1.5-2.5 3-3.5" '
        'stroke="#94a76a" stroke-width="0.9" stroke-opacity="0.6" fill="none" stroke-linecap="round"/>'
        '<circle cx="14" cy="16" r="0.9" fill="#c5d29b"/>'
        '<circle cx="24" cy="24" r="0.8" fill="#c5d29b"/>'
        '<circle cx="4" cy="7" r="0.8" fill="#a3b573"/>'
        '<circle cx="25" cy="13" r="0.7" fill="#a3b573"/>'),
    "t_veg": _pattern("t_veg", 28,
        '<rect width="28" height="28" fill="#9db97b"/>'
        '<circle cx="7" cy="8" r="3.2" fill="#7d9c5e"/>'
        '<circle cx="9.5" cy="9.5" r="2.4" fill="#8fae6e"/>'
        '<circle cx="20" cy="20" r="3.6" fill="#7d9c5e"/>'
        '<circle cx="22.5" cy="18.5" r="2.6" fill="#8fae6e"/>'
        '<circle cx="24" cy="6" r="1" fill="#b9cf97"/>'
        '<circle cx="4" cy="23" r="1" fill="#b9cf97"/>'),
    "t_forest": _pattern("t_forest", 42,
        '<rect width="42" height="42" fill="#55754d"/>'
        + _canopy(10, 12, 9) + _canopy(30, 28, 10) + _canopy(34, 6, 7) + _canopy(6, 34, 7.5)),
    "t_earth": _pattern("t_earth", 28,
        '<rect width="28" height="28" fill="#b08d68"/>'
        '<circle cx="6" cy="6" r="1.1" fill="#93714e"/>'
        '<circle cx="18" cy="11" r="0.9" fill="#93714e"/>'
        '<circle cx="24" cy="22" r="1.2" fill="#93714e"/>'
        '<circle cx="9" cy="20" r="1" fill="#c8a87f"/>'
        '<circle cx="22" cy="4" r="0.8" fill="#c8a87f"/>'
        '<path d="M3 15q4-1.5 8 0" stroke="#a17d59" stroke-width="0.8" fill="none"/>'),
    "t_sand": _pattern("t_sand", 28,
        '<rect width="28" height="28" fill="#e4cf9c"/>'
        '<circle cx="5" cy="8" r="0.8" fill="#c8ad72"/>'
        '<circle cx="14" cy="4" r="0.7" fill="#c8ad72"/>'
        '<circle cx="23" cy="12" r="0.8" fill="#c8ad72"/>'
        '<circle cx="9" cy="19" r="0.7" fill="#c8ad72"/>'
        '<circle cx="20" cy="24" r="0.8" fill="#c8ad72"/>'
        '<circle cx="26" cy="26" r="0.6" fill="#f0e0b4"/>'
        '<circle cx="3" cy="25" r="0.6" fill="#f0e0b4"/>'),
    "t_lava": _pattern("t_lava", 28,
        '<rect width="28" height="28" fill="#d59650"/>'
        '<path d="M3 24l5-6 3 2 4-7M18 26l4-5 3 1" '
        'stroke="#9c5a2a" stroke-width="1" fill="none"/>'
        '<circle cx="8" cy="8" r="1.1" fill="#b3542c"/>'
        '<circle cx="21" cy="14" r="1" fill="#e8b070"/>'),
    "t_lethal": _pattern("t_lethal", 28,
        '<rect width="28" height="28" fill="#b94a3c"/>'
        '<path d="M-2 8L8-2M6 30L30 6M20 34L34 20" '
        'stroke="#93392e" stroke-width="2" stroke-opacity="0.7"/>'
        '<circle cx="14" cy="18" r="1" fill="#d9776a"/>'),
    "t_deep": _pattern("t_deep", 28,
        '<rect width="28" height="28" fill="#4c7ba3"/>'
        '<path d="M2 8q5-3 10 0t10 0" stroke="#6f9dc0" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
        '<path d="M-4 20q5-3 10 0t10 0t10 0" stroke="#3c648c" stroke-width="1.2" fill="none" stroke-linecap="round"/>'),
    "t_water": _pattern("t_water", 28,
        '<rect width="28" height="28" fill="#6aa5c4"/>'
        '<path d="M2 9q5-3 10 0t10 0" stroke="#a5cede" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
        '<path d="M-4 21q5-3 10 0t10 0t10 0" stroke="#4f86a6" stroke-width="1.1" fill="none" stroke-linecap="round"/>'),
    "t_struct": _pattern("t_struct", 28,
        '<rect width="28" height="28" fill="#6b5b47"/>'
        '<path d="M-2 6l8-8M-2 14l16-16M-2 22l24-24M6 30l24-24M14 30l16-16M22 30l8-8" '
        'stroke="#5a4b39" stroke-width="0.9"/>'
        '<path d="M0 14.5h28" stroke="#7d6c56" stroke-width="0.8"/>'),
    "t_floor": _pattern("t_floor", 28,
        '<rect width="28" height="28" fill="#d8cdb4"/>'
        '<path d="M0 0.5h28M0 14.5h28M7 0.5v14M21 14.5v14" '
        'stroke="#b4a789" stroke-width="1"/>'
        '<circle cx="15" cy="8" r="2.4" fill="#cfc3a9" fill-opacity="0.6"/>'
        '<circle cx="6" cy="22" r="2" fill="#cfc3a9" fill-opacity="0.5"/>'),
    "t_wall": _pattern("t_wall", 28,
        '<rect width="28" height="28" fill="#3f3931"/>'
        '<path d="M-2 6l8-8M-2 14l16-16M-2 22l24-24M-2 30l32-32M6 30l24-24M14 30l16-16M22 30l8-8" '
        'stroke="#2b2620" stroke-width="1"/>'
        '<circle cx="8" cy="18" r="1" fill="#554d42"/>'
        '<circle cx="21" cy="7" r="0.9" fill="#554d42"/>'),
    "t_pillar": _pattern("t_pillar", 28,
        '<rect width="28" height="28" fill="#8a67b5"/>'
        '<path d="M9 0v28" stroke="#b697dd" stroke-width="3" stroke-opacity="0.7"/>'
        '<path d="M20 0v28" stroke="#6d4c96" stroke-width="3" stroke-opacity="0.5"/>'),
}

EMOJI_RANGES = (
    (0x2600, 0x27BF),
    (0x2B00, 0x2BFF),
    (0x1F000, 0x1FAFF),
    (0xFE00, 0xFE0F),   # variation selectors (skipped, but recognised)
    (0x200D, 0x200D),   # ZWJ
)


def is_emoji_char(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in EMOJI_RANGES)


ROW_RE = re.compile(r"^\s*(\d{1,3})(?:-(\d{1,3}))?\s")
TITLE_KEYWORDS = ("MAPPA", "MAP ", "CAMPO", "ARENA", "TORRE", "FASE", "GRID", "LIVELLO")


def parse_row_cells(text: str) -> list[str]:
    """Extract emoji cells from a row line (after the row number)."""
    cells: list[str] = []
    for ch in text:
        if ch in (" ", "\t", "│", "|"):
            continue
        cp = ord(ch)
        if 0x2500 <= cp <= 0x257F:  # box drawing — annotations, stop reading
            break
        if cp in (0xFE0F, 0x200D):  # modifier: belongs to previous cell
            continue
        if is_emoji_char(ch):
            cells.append(ch)
        elif ch.isascii() and (ch.isalnum() or ch in "()[]{}<>─-=+*'\".,;:!?/\\"):
            # trailing prose/callout on the same line — stop at first ASCII text
            if cells:
                break
    return cells


def col_label(i: int) -> str:
    label = ""
    i += 1
    while i > 0:
        i, rem = divmod(i - 1, 26)
        label = chr(ord("A") + rem) + label
    return label


def slugify(title: str) -> str:
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:48] or "mappa"


def extract_maps(md_text: str) -> list[dict]:
    """Find fenced code blocks with >=3 emoji grid rows.

    Title preference: the banner line inside the fence (between ═══ rules,
    e.g. "CAMPO DROW 1 - BURNING OPERATIONS BASE (...)"), then the nearest
    heading containing a map keyword, then the nearest heading.
    """
    maps: list[dict] = []
    lines = md_text.splitlines()
    headings: list[str] = []
    in_fence = False
    block: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                grid = parse_block(block)
                if grid and len(grid["rows"]) >= 3:
                    grid["title"] = grid.pop("banner", "") or _pick_heading(headings) \
                        or f"Mappa {len(maps) + 1}"
                    maps.append(grid)
                block = []
            in_fence = not in_fence
            continue
        if in_fence:
            block.append(line)
        else:
            m = re.match(r"^#{1,4}\s+(.*)", stripped)
            if m:
                headings.append(m.group(1).strip().rstrip("#").strip())
    return maps


def _pick_heading(headings: list[str]) -> str:
    for kw in TITLE_KEYWORDS:  # keyword priority, then nearest heading
        for h in reversed(headings[-4:]):
            if kw in h.upper():
                return h
    return headings[-1] if headings else ""


def parse_block(block_lines: list[str]) -> dict | None:
    rows: dict[int, list[str]] = {}
    filled: set[int] = set()
    banner = ""
    for line in block_lines:
        s = line.strip()
        if not banner and s and not set(s) <= {"═", "─", "="} and not ROW_RE.match(line) \
                and 8 < len(s) < 120 \
                and not s.startswith(("COLONNE", "RIGHE", "-", "NOTA", "SCALA", "LEGENDA",
                                      "TOTALE", "DIMENSIONI", "TUTTO", "POSIZIONI")) \
                and not any(c in s for c in "│└┘├┤┌┐↑↓←→") \
                and any(ch.isalpha() for ch in s):
            banner = s
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = parse_row_cells(line[m.end():])
        if len(cells) >= 5:  # ignore stray numbered annotations
            n0 = int(m.group(1))
            n1 = int(m.group(2)) if m.group(2) else n0
            for n in range(n0, n1 + 1):
                # keep the widest reading if a row number repeats
                if n not in rows or len(cells) > len(rows[n]):
                    rows[n] = cells
                if n != n0:
                    filled.add(n)
    if not rows:
        return None
    # the source files skip rows identical to the previous one: fill the
    # gaps by repeating the last drawn row (marked gray in the output)
    nums = sorted(rows)
    for n in range(nums[0], nums[-1] + 1):
        if n not in rows:
            rows[n] = rows[max(k for k in rows if k < n)]
            filled.add(n)
    return {"rows": rows, "filled": filled, "banner": banner}


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;")


def _mix(hex_color: str, target: str, k: float) -> str:
    """Blend hex_color toward target (#rrggbb) by factor k in [0,1]."""
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(target[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * k):02x}" for x, y in zip(a, b))


def _grad_id(color: str) -> str:
    return "g_" + color.lstrip("#")


def _unit_gradient(color: str) -> str:
    gid = _grad_id(color)
    return (
        f'<radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.8">'
        f'<stop offset="0" stop-color="{_mix(color, "#ffffff", 0.45)}"/>'
        f'<stop offset="0.55" stop-color="{color}"/>'
        f'<stop offset="1" stop-color="{_mix(color, "#000000", 0.35)}"/>'
        f'</radialGradient>'
    )


def _resolve_bases(rows: dict[int, list[str]], n_cols: int) -> dict[int, list[str | None]]:
    """Per-cell terrain pattern id. Units/icons/unknown inherit the nearest
    terrain in their row (left first, then right); cells beyond the row's
    width stay None (bare parchment)."""
    row_nums = sorted(rows)
    base: dict[int, list[str | None]] = {}
    for rn in row_nums:
        cells = rows[rn]
        direct: list[str | None] = []
        for c in range(n_cols):
            e = cells[c] if c < len(cells) else None
            if e is None:
                direct.append(None)
                continue
            spec = SYMBOLS.get(e)
            if spec and spec["mode"] == "fill":
                direct.append(spec["pat"])
            else:
                direct.append("INHERIT")
        resolved: list[str | None] = list(direct)
        last: str | None = None
        for c in range(n_cols):  # left neighbor pass
            if direct[c] == "INHERIT":
                resolved[c] = last
            elif direct[c] is not None:
                last = direct[c]
        nxt: str | None = None
        for c in range(n_cols - 1, -1, -1):  # right neighbor fallback
            if direct[c] == "INHERIT":
                if resolved[c] is None:
                    resolved[c] = nxt
            elif direct[c] is not None:
                nxt = direct[c]
        base[rn] = resolved
    return base


def _runs_path(cells: list[tuple[int, int]], ox: int, oy: int) -> str:
    """Merge (row, col) cells into horizontal runs, return a path 'd'."""
    d: list[str] = []
    by_row: dict[int, list[int]] = {}
    for r, c in cells:
        by_row.setdefault(r, []).append(c)
    for r in sorted(by_row):
        cols = sorted(by_row[r])
        start = prev = cols[0]
        for c in cols[1:] + [None]:
            if c is not None and c == prev + 1:
                prev = c
                continue
            w = (prev - start + 1) * CELL
            d.append(f"M{ox + start * CELL} {oy + r * CELL}h{w}v{CELL}h{-w}z")
            if c is not None:
                start = prev = c
    return "".join(d)


def _boundary_paths(base: dict[int, list[str | None]], row_nums: list[int],
                    n_cols: int, ox: int, oy: int) -> tuple[str, str]:
    """Ink strokes where adjacent terrains differ: (heavy_d, soft_d)."""
    n_rows = len(row_nums)

    def at(r: int, c: int) -> str | None:
        if r < 0 or r >= n_rows or c < 0 or c >= n_cols:
            return None
        return base[row_nums[r]][c]

    def klass(a: str | None, b: str | None) -> str | None:
        if a == b:
            return None
        if a is None and b is None:
            return None
        if a in HEAVY_PATS or b in HEAVY_PATS:
            return "heavy"
        return "soft"

    heavy: list[str] = []
    soft: list[str] = []
    # vertical edges (between columns), merged over consecutive rows
    for c in range(n_cols + 1):
        r = 0
        while r < n_rows:
            k = klass(at(r, c - 1), at(r, c))
            if k is None:
                r += 1
                continue
            r0 = r
            while r + 1 < n_rows and klass(at(r + 1, c - 1), at(r + 1, c)) == k:
                r += 1
            seg = f"M{ox + c * CELL} {oy + r0 * CELL}v{(r - r0 + 1) * CELL}"
            (heavy if k == "heavy" else soft).append(seg)
            r += 1
    # horizontal edges (between rows), merged over consecutive columns
    for r in range(n_rows + 1):
        c = 0
        while c < n_cols:
            k = klass(at(r - 1, c), at(r, c))
            if k is None:
                c += 1
                continue
            c0 = c
            while c + 1 < n_cols and klass(at(r - 1, c + 1), at(r, c + 1)) == k:
                c += 1
            seg = f"M{ox + c0 * CELL} {oy + r * CELL}h{(c - c0 + 1) * CELL}"
            (heavy if k == "heavy" else soft).append(seg)
            c += 1
    return "".join(heavy), "".join(soft)


def render_svg(grid: dict, source_name: str) -> str:
    rows = grid["rows"]
    row_nums = sorted(rows)
    n_rows = row_nums[-1] - row_nums[0] + 1
    n_cols = max(len(c) for c in rows.values())
    grid_w, grid_h = n_cols * CELL, n_rows * CELL
    width = max(MARGIN * 2 + grid_w, MIN_WIDTH)
    used = sorted({e for cells in rows.values() for e in cells})

    header_h = 58
    ox = MARGIN
    oy = header_h + 22
    sb_y = oy + grid_h + 24
    ly = sb_y + 32
    legend_h = 18 + LEGEND_ROW_H * len(used)
    height = ly + legend_h + 26

    base = _resolve_bases(rows, n_cols)
    used_pats = sorted({p for r in base.values() for p in r if p})
    unit_colors = sorted({SYMBOLS[e]["fill"] for e in used
                          if e in SYMBOLS and SYMBOLS[e]["mode"] == "unit"})

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )

    # --- defs: filters, vignette, terrain patterns, token gradients --------
    defs: list[str] = ["<defs>"]
    defs.append(
        '<filter id="grain" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" '
        'seed="11" stitchTiles="stitch"/>'
        '<feColorMatrix type="matrix" values="0 0 0 0 0.36 0 0 0 0 0.28 '
        '0 0 0 0 0.16 0 0 0 0.18 0"/>'
        '<feComposite operator="over" in2="SourceGraphic"/></filter>'
    )
    defs.append(
        '<filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" '
        'seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"/></filter>'
    )
    defs.append(
        '<filter id="softblur" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur stdDeviation="1.6"/></filter>'
    )
    defs.append(
        '<radialGradient id="vign" cx="0.5" cy="0.45" r="0.75">'
        '<stop offset="0.62" stop-color="#3b2e1e" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#3b2e1e" stop-opacity="0.16"/>'
        '</radialGradient>'
    )
    for p in used_pats:
        defs.append(PATTERNS[p])
    for color in unit_colors:
        defs.append(_unit_gradient(color))
    defs.append("</defs>")
    out.extend(defs)

    # --- parchment sheet, vignette, double frame ----------------------------
    out.append(f'<rect width="{width}" height="{height}" fill="{PAPER}" filter="url(#grain)"/>')
    out.append(f'<rect width="{width}" height="{height}" fill="url(#vign)"/>')
    out.append(
        f'<rect x="5" y="5" width="{width - 10}" height="{height - 10}" fill="none" '
        f'stroke="{INK}" stroke-width="0.8" opacity="0.8"/>'
    )
    out.append(
        f'<rect x="9" y="9" width="{width - 18}" height="{height - 18}" fill="none" '
        f'stroke="{INK}" stroke-width="2" opacity="0.85"/>'
    )

    # --- header --------------------------------------------------------------
    title = _esc(grid["title"])
    out.append(
        f'<text x="{MARGIN}" y="34" font-size="19" font-weight="bold" '
        f'fill="{INK}" letter-spacing="0.5">{title}</text>'
    )
    out.append(
        f'<text x="{MARGIN}" y="51" font-size="11" font-style="italic" fill="{INK_SOFT}">'
        f'{n_cols}×{n_rows} quadretti · scala 1,5 m/quadretto</text>'
    )

    # --- map plate -----------------------------------------------------------
    out.append(
        f'<rect x="{ox - 5}" y="{oy - 5}" width="{grid_w + 10}" height="{grid_h + 10}" '
        f'fill="{PLATE}" stroke="{INK}" stroke-width="1.6"/>'
    )

    # --- terrain: one merged path per texture (light first, heavy last) ------
    light_cells: dict[str, list[tuple[int, int]]] = {}
    heavy_cells: dict[str, list[tuple[int, int]]] = {}
    for r, rn in enumerate(row_nums):
        for c in range(n_cols):
            p = base[rn][c]
            if p is None:
                continue
            (heavy_cells if p in HEAVY_PATS else light_cells).setdefault(p, []).append((r, c))
    for p in sorted(light_cells):
        out.append(f'<path d="{_runs_path(light_cells[p], ox, oy)}" fill="url(#{p})"/>')
    # cast shadow of walls/structures onto the floor, then the solids themselves
    if heavy_cells:
        all_heavy = [cell for cells in heavy_cells.values() for cell in cells]
        out.append(
            f'<path d="{_runs_path(sorted(all_heavy), ox, oy)}" fill="#241c10" '
            f'opacity="0.28" filter="url(#softblur)" transform="translate(2.6,3.4)"/>'
        )
        for p in sorted(heavy_cells):
            out.append(f'<path d="{_runs_path(heavy_cells[p], ox, oy)}" fill="url(#{p})"/>')

    # --- inked terrain boundaries (hand-drawn wobble) -------------------------
    heavy_d, soft_d = _boundary_paths(base, row_nums, n_cols, ox, oy)
    if soft_d:
        out.append(
            f'<path d="{soft_d}" fill="none" stroke="{INK_SOFT}" stroke-width="0.9" '
            f'opacity="0.5" stroke-linecap="round" filter="url(#rough)"/>'
        )
    if heavy_d:
        out.append(
            f'<path d="{heavy_d}" fill="none" stroke="#241c10" stroke-width="1.8" '
            f'opacity="0.9" stroke-linecap="round" filter="url(#rough)"/>'
        )

    # --- grid lines (thin every square, thick every 5) ------------------------
    grid_d = "".join(
        f"M{ox + c * CELL} {oy}v{grid_h}" for c in range(n_cols + 1) if c % 5
    ) + "".join(
        f"M{ox} {oy + r * CELL}h{grid_w}" for r in range(n_rows + 1) if r % 5
    )
    grid5_d = "".join(
        f"M{ox + c * CELL} {oy}v{grid_h}" for c in range(0, n_cols + 1, 5)
    ) + "".join(
        f"M{ox} {oy + r * CELL}h{grid_w}" for r in range(0, n_rows + 1, 5)
    )
    out.append(f'<path d="{grid_d}" stroke="#2e2313" stroke-width="0.5" opacity="0.16" fill="none"/>')
    out.append(f'<path d="{grid5_d}" stroke="#2e2313" stroke-width="1.2" opacity="0.28" fill="none"/>')

    # --- icons and unit tokens -------------------------------------------------
    for r, rn in enumerate(row_nums):
        cells = rows[rn]
        for c in range(n_cols):
            emoji = cells[c] if c < len(cells) else None
            if emoji is None:
                continue
            spec = SYMBOLS.get(emoji)
            x, y = ox + c * CELL, oy + r * CELL
            cx, cy = x + CELL / 2, y + CELL / 2
            if spec and spec["mode"] == "unit":
                rr = CELL * 0.37
                out.append(
                    f'<ellipse cx="{cx + 1.4}" cy="{cy + 2.2}" rx="{rr}" ry="{rr * 0.82}" '
                    f'fill="#241c10" opacity="0.3"/>'
                )
                out.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="url(#{_grad_id(spec["fill"])})" '
                    f'stroke="#241c10" stroke-width="1.6"/>'
                )
                out.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{rr - 2.4}" fill="none" '
                    f'stroke="#ffffff" stroke-width="0.9" opacity="0.55"/>'
                )
            elif spec is None or spec["mode"] == "icon":
                out.append(
                    f'<ellipse cx="{cx}" cy="{cy + 6}" rx="7.5" ry="2.8" '
                    f'fill="#241c10" opacity="0.14"/>'
                )
                out.append(
                    f'<text x="{cx}" y="{cy + 6}" font-size="17" '
                    f'text-anchor="middle">{emoji}</text>'
                )

    # --- coordinates ------------------------------------------------------------
    for c in range(n_cols):
        out.append(
            f'<text x="{ox + c * CELL + CELL / 2}" y="{oy - 8}" font-size="10" '
            f'text-anchor="middle" fill="{INK_SOFT}">{col_label(c)}</text>'
        )
    filled = grid.get("filled", set())
    for r, rn in enumerate(row_nums):
        color = "#b1a184" if rn in filled else INK_SOFT
        out.append(
            f'<text x="{ox - 9}" y="{oy + r * CELL + CELL / 2 + 3}" font-size="10" '
            f'text-anchor="end" fill="{color}">{rn:02d}</text>'
        )

    # --- scale bar (5 squares = 7,5 m, alternating cartographic segments) -------
    for i in range(5):
        fill = INK if i % 2 == 0 else PAPER
        out.append(
            f'<rect x="{ox + i * CELL}" y="{sb_y - 5}" width="{CELL}" height="7" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1"/>'
        )
    out.append(
        f'<text x="{ox + 5 * CELL + 10}" y="{sb_y + 3}" font-size="11" '
        f'fill="{INK}">7,5 m (5 quadretti)</text>'
    )

    # --- legend -------------------------------------------------------------------
    out.append(
        f'<text x="{ox}" y="{ly}" font-size="12" font-weight="bold" fill="{INK}" '
        f'letter-spacing="2">LEGENDA</text>'
    )
    out.append(
        f'<path d="M{ox + 74} {ly - 4}H{width - MARGIN}" stroke="{INK_SOFT}" '
        f'stroke-width="0.7" opacity="0.7"/>'
    )
    for i, emoji in enumerate(used):
        spec = SYMBOLS.get(emoji)
        label = spec["it"] if spec and spec["it"] else "(simbolo locale — vedi legenda del file sorgente)"
        y = ly + 18 + i * LEGEND_ROW_H
        if spec and spec["mode"] == "unit":
            out.append(
                f'<circle cx="{ox + 9}" cy="{y - 4}" r="7.5" '
                f'fill="url(#{_grad_id(spec["fill"])})" stroke="#241c10" stroke-width="1.2"/>'
            )
        elif spec and spec["mode"] == "fill":
            out.append(
                f'<rect x="{ox}" y="{y - 12}" width="19" height="15" fill="url(#{spec["pat"]})" '
                f'stroke="{INK_SOFT}" stroke-width="0.7"/>'
            )
        else:
            out.append(f'<text x="{ox}" y="{y}" font-size="14">{emoji}</text>')
        out.append(f'<text x="{ox + 27}" y="{y}" font-size="11" fill="{INK}">{emoji} — {label}</text>')

    # --- footer ---------------------------------------------------------------------
    out.append(
        f'<text x="{ox}" y="{height - 16}" font-size="9" font-style="italic" '
        f'fill="{INK_SOFT}">fonte: {_esc(source_name)} · SVG generato da '
        f'scripts/render_map_svg.py (stile pergamena) — non modificare a mano</text>'
    )

    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="markdown file(s) containing emoji-grid maps")
    ap.add_argument("-o", "--outdir", help="output directory (default: rendered/ next to input)")
    ap.add_argument("--map", type=int, help="render only map #N (1-based) of each file")
    ap.add_argument("--list", action="store_true", help="list maps found, render nothing")
    args = ap.parse_args()

    total = 0
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"ERRORE: {path} non esiste", file=sys.stderr)
            return 1
        maps = extract_maps(path.read_text(encoding="utf-8"))
        if not maps:
            print(f"{path.name}: nessuna griglia emoji trovata")
            continue
        if args.list:
            print(f"{path.name}: {len(maps)} mappe")
            for i, g in enumerate(maps, 1):
                rows = g["rows"]
                n_cols = max(len(c) for c in rows.values())
                print(f"  {i:2d}. {g['title']}  ({n_cols}×{len(rows)} celle)")
            continue
        outdir = Path(args.outdir) if args.outdir else path.parent / "rendered"
        outdir.mkdir(parents=True, exist_ok=True)
        for i, g in enumerate(maps, 1):
            if args.map and i != args.map:
                continue
            name = f"{path.stem}_map{i:02d}_{slugify(g['title'])}.svg"
            (outdir / name).write_text(render_svg(g, path.name), encoding="utf-8")
            print(f"✓ {outdir / name}")
            total += 1
    if not args.list:
        print(f"Totale: {total} SVG generati")
    return 0


if __name__ == "__main__":
    sys.exit(main())
