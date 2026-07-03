#!/usr/bin/env python3
"""
render_map_svg.py — render the campaign's emoji-grid tactical maps to SVG.

The revised maps of ARC-07/08/09 (files `*Ultra-Clear*.md`, `*MAPPE*.md`,
`SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`, ...) share one format:
fenced code blocks whose rows start with a 2-digit row number followed by
emoji cells (with or without spaces). This script parses those grids and
emits print-quality SVG battlemaps: uniform palette, 1,5 m/quadretto grid,
column letters / row numbers, scale bar and legend — the same map for every
arc, in one style, regenerable whenever the markdown master changes.

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

# ---------------------------------------------------------------------------
# Symbol table — universal legend of the repo
# (SUPPLEMENTO-P1C drow maps + Ultra-Clear maps ARC-07/08).
# mode "fill":   solid terrain square, no glyph
# mode "unit":   colored token circle
# mode "icon":   emoji glyph drawn over a base terrain fill
# ---------------------------------------------------------------------------
SYMBOLS: dict[str, dict] = {
    # terrain (fills)
    "🌲": {"mode": "fill", "fill": "#2d6a4f", "it": "Foresta densa (Furtività +5, copertura)"},
    "🌿": {"mode": "fill", "fill": "#74c69d", "it": "Vegetazione bassa"},
    "🟩": {"mode": "fill", "fill": "#b7e4c7", "it": "Pianura / area aperta"},
    "🟫": {"mode": "fill", "fill": "#b08968", "it": "Terra battuta / sentiero"},
    "🟨": {"mode": "fill", "fill": "#ffe066", "it": "Sabbia / area segnalata"},
    "🟧": {"mode": "fill", "fill": "#f8961e", "it": "Lava raffreddata / pericolo"},
    "🟥": {"mode": "fill", "fill": "#e5383b", "it": "Zona letale"},
    "🟦": {"mode": "fill", "fill": "#4895ef", "it": "Acqua profonda"},
    "🌊": {"mode": "fill", "fill": "#48cae4", "it": "Acqua / corrente"},
    "⬛": {"mode": "fill", "fill": "#343a40", "it": "Struttura (tenda, edificio, dais)"},
    "⬜": {"mode": "fill", "fill": "#f8f9fa", "it": "Pavimento lavorato"},
    "🏰": {"mode": "fill", "fill": "#6c757d", "it": "Muro / roccia solida"},
    "🟪": {"mode": "fill", "fill": "#9d4edd", "it": "Pilastro / mithral"},
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
DEFAULT_TERRAIN = {"mode": "fill", "fill": "#f1f3f5", "it": ""}

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


def render_svg(grid: dict, source_name: str) -> str:
    rows = grid["rows"]
    row_nums = sorted(rows)
    n_rows = row_nums[-1] - row_nums[0] + 1
    n_cols = max(len(c) for c in rows.values())
    width = MARGIN * 2 + n_cols * CELL
    used = sorted({e for cells in rows.values() for e in cells})
    legend_h = 30 + LEGEND_ROW_H * len(used)
    height = MARGIN * 2 + n_rows * CELL + 30 + legend_h

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Noto Sans, sans-serif">'
    )
    out.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    title = grid["title"].replace("&", "&amp;").replace("<", "&lt;")
    out.append(
        f'<text x="{MARGIN}" y="24" font-size="15" font-weight="bold" fill="#212529">{title}</text>'
    )
    out.append(
        f'<text x="{MARGIN}" y="40" font-size="11" fill="#6c757d">'
        f'{n_cols}×{n_rows} quadretti · scala 1,5 m/quadretto · fonte: {source_name} '
        f'(SVG generato — non modificare a mano)</text>'
    )

    ox, oy = MARGIN, MARGIN + 14

    # cells
    for rn in row_nums:
        r = rn - row_nums[0]
        cells = rows.get(rn, [])
        for c in range(n_cols):
            x, y = ox + c * CELL, oy + r * CELL
            emoji = cells[c] if c < len(cells) else None
            spec = SYMBOLS.get(emoji, None) if emoji else None
            if spec is None and emoji:
                spec = {"mode": "icon", "fill": "#f1f3f5", "it": ""}
            base = spec["fill"] if spec and spec["mode"] == "fill" else (
                spec["fill"] if spec and spec["mode"] == "icon" else "#f1f3f5"
            )
            if spec is None:
                base = DEFAULT_TERRAIN["fill"]
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" fill="{base}"/>')
            if spec and spec["mode"] == "unit":
                cx, cy, rr = x + CELL / 2, y + CELL / 2, CELL * 0.36
                out.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{spec["fill"]}" '
                    f'stroke="#ffffff" stroke-width="2"/>'
                )
            elif spec and spec["mode"] == "icon" and emoji:
                out.append(
                    f'<text x="{x + CELL / 2}" y="{y + CELL / 2 + 6}" font-size="17" '
                    f'text-anchor="middle">{emoji}</text>'
                )

    # grid lines (thin every square, thick every 5)
    for c in range(n_cols + 1):
        x = ox + c * CELL
        w = 1.4 if c % 5 == 0 else 0.5
        out.append(
            f'<line x1="{x}" y1="{oy}" x2="{x}" y2="{oy + n_rows * CELL}" '
            f'stroke="#495057" stroke-width="{w}" opacity="0.55"/>'
        )
    for r in range(n_rows + 1):
        y = oy + r * CELL
        w = 1.4 if r % 5 == 0 else 0.5
        out.append(
            f'<line x1="{ox}" y1="{y}" x2="{ox + n_cols * CELL}" y2="{y}" '
            f'stroke="#495057" stroke-width="{w}" opacity="0.55"/>'
        )

    # coordinates
    for c in range(n_cols):
        out.append(
            f'<text x="{ox + c * CELL + CELL / 2}" y="{oy - 6}" font-size="10" '
            f'text-anchor="middle" fill="#495057">{col_label(c)}</text>'
        )
    filled = grid.get("filled", set())
    for rn in row_nums:
        r = rn - row_nums[0]
        color = "#adb5bd" if rn in filled else "#495057"
        out.append(
            f'<text x="{ox - 8}" y="{oy + r * CELL + CELL / 2 + 3}" font-size="10" '
            f'text-anchor="end" fill="{color}">{rn:02d}</text>'
        )

    # scale bar (5 squares = 7,5 m)
    sb_y = oy + n_rows * CELL + 18
    out.append(
        f'<line x1="{ox}" y1="{sb_y}" x2="{ox + 5 * CELL}" y2="{sb_y}" '
        f'stroke="#212529" stroke-width="2"/>'
    )
    for i in (0, 5):
        out.append(
            f'<line x1="{ox + i * CELL}" y1="{sb_y - 4}" x2="{ox + i * CELL}" y2="{sb_y + 4}" '
            f'stroke="#212529" stroke-width="2"/>'
        )
    out.append(
        f'<text x="{ox + 5 * CELL + 8}" y="{sb_y + 4}" font-size="11" fill="#212529">7,5 m (5 quadretti)</text>'
    )

    # legend
    ly = sb_y + 26
    out.append(f'<text x="{ox}" y="{ly}" font-size="12" font-weight="bold" fill="#212529">LEGENDA</text>')
    for i, emoji in enumerate(used):
        spec = SYMBOLS.get(emoji)
        label = spec["it"] if spec and spec["it"] else "(simbolo locale — vedi legenda del file sorgente)"
        y = ly + 16 + i * LEGEND_ROW_H
        if spec and spec["mode"] == "unit":
            out.append(
                f'<circle cx="{ox + 9}" cy="{y - 4}" r="8" fill="{spec["fill"]}" '
                f'stroke="#ffffff" stroke-width="1.5"/>'
            )
        elif spec and spec["mode"] == "fill":
            out.append(
                f'<rect x="{ox}" y="{y - 12}" width="18" height="16" fill="{spec["fill"]}" '
                f'stroke="#adb5bd" stroke-width="0.5"/>'
            )
        else:
            out.append(f'<text x="{ox}" y="{y}" font-size="14">{emoji}</text>')
        out.append(f'<text x="{ox + 26}" y="{y}" font-size="11" fill="#212529">{emoji} — {label}</text>')

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
