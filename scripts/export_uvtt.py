#!/usr/bin/env python3
"""
export_uvtt.py — export an emoji-grid map master to a Universal VTT file
(`.uvtt` / `.dd2vtt`): the JSON format Foundry VTT and Roll20 import NATIVELY,
carrying walls (line_of_sight), doors (portals), lights and the grid — so a
map imports with vision-blocking walls and dynamic lighting already wired,
without drawing anything by hand in the VTT.

The master markdown grid stays the MASTER; the `.uvtt` is a generated artifact
derived from it (like the SVG). It is NOT committed by default and NOT checked
by validate_maps.py — it is a presentation/export layer for the table.

What is extracted from the grid (universal legend of the repo):
  - line_of_sight  ← cell edges between a WALL cell and a non-wall cell,
                      greedily merged into straight runs (walls: 🏰 ⬛ 🟪 🗼 🏛).
  - portals        ← door cells (🚪): a short segment across the opening.
  - lights         ← light sources (🏮 braziere, 🕯 candele, 🔥 fuoco,
                      🔮 cristalli), or the explicit `lights` of a JSON spec.
  - resolution     ← map_size in grid units + pixels_per_grid (--ppg).
  - image          ← optional base64 PNG (--image file.png); Foundry can also
                      set the background manually after import.

Coordinates are in GRID UNITS (0..cols on x, 0..rows on y), as the UVTT
importers expect. The exporter re-uses render_map_svg.py's grid parser so the
reading is identical to what the SVG renders.

Usage:
    python3 scripts/export_uvtt.py <file.md>                 # all maps in file
    python3 scripts/export_uvtt.py <file.md> --map 2         # only map #2
    python3 scripts/export_uvtt.py <file.md> --ext dd2vtt    # Dungeondraft ext
    python3 scripts/export_uvtt.py <file.md> --ppg 100 --image rendered/x.png
    python3 scripts/export_uvtt.py <file.md> -o DIR

Default output: a `rendered/vtt/` directory next to the input file,
one `<stem>_mapN_<slug>.uvtt` per map. Pure Python 3, no dependencies.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map_svg as rms  # noqa: E402

# Full vision-blocking cells (line_of_sight). Low walls (🧱) give cover but do
# not block sight, so they are intentionally excluded.
WALL_SYMS = {"🏰", "⬛", "🟪", "🗼", "🏛", "🗿"}
DOOR_SYMS = {"🚪"}
# light source symbol -> (range in grid squares, hex color)
LIGHT_SYMS = {
    "🏮": (6.0, "ffd9a0"),   # braziere
    "🔥": (5.0, "ffb37a"),   # fuoco
    "🕯": (3.0, "ffe6b3"),   # candele
    "🕳": (0.0, "000000"),   # (no light) — placeholder, filtered out
    "🔮": (4.0, "b3e6ff"),   # cristalli / altare magico
    "✨": (3.0, "e6ccff"),
    "⚡": (4.0, "fff0a0"),
}


def _grid_matrix(gmap: dict) -> list[list[str]]:
    rows = gmap["rows"]
    nums = sorted(rows)
    width = max(len(rows[n]) for n in nums)
    matrix = []
    for n in nums:
        row = list(rows[n])
        row += [""] * (width - len(row))  # pad ragged rows
        matrix.append(row)
    return matrix


def _is_wall(matrix, x, y) -> bool:
    if 0 <= y < len(matrix) and 0 <= x < len(matrix[0]):
        return matrix[y][x] in WALL_SYMS
    return False  # out of bounds = open (walls border the mass, not the map edge)


def extract_walls(matrix) -> list[list[dict]]:
    """Trace cell-edge walls between wall and non-wall cells, then greedily
    merge collinear unit edges into straight segments (fewer, cleaner walls)."""
    h = len(matrix)
    w = len(matrix[0]) if h else 0
    horiz: set[tuple[int, int]] = set()  # horizontal unit edge at grid line y, spanning x..x+1
    vert: set[tuple[int, int]] = set()   # vertical unit edge at grid line x, spanning y..y+1
    for y in range(h):
        for x in range(w):
            if matrix[y][x] not in WALL_SYMS:
                continue
            if not _is_wall(matrix, x, y - 1):
                horiz.add((x, y))          # top edge
            if not _is_wall(matrix, x, y + 1):
                horiz.add((x, y + 1))      # bottom edge
            if not _is_wall(matrix, x - 1, y):
                vert.add((x, y))           # left edge
            if not _is_wall(matrix, x + 1, y):
                vert.add((x + 1, y))       # right edge

    segments: list[list[dict]] = []

    # merge horizontal runs along each grid line y
    by_line: dict[int, list[int]] = {}
    for (x, y) in horiz:
        by_line.setdefault(y, []).append(x)
    for y, xs in by_line.items():
        xs.sort()
        run_start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            segments.append([{"x": run_start, "y": y}, {"x": prev + 1, "y": y}])
            if x is not None:
                run_start = prev = x

    # merge vertical runs along each grid line x
    by_col: dict[int, list[int]] = {}
    for (x, y) in vert:
        by_col.setdefault(x, []).append(y)
    for x, ys in by_col.items():
        ys.sort()
        run_start = prev = ys[0]
        for y in ys[1:] + [None]:
            if y is not None and y == prev + 1:
                prev = y
                continue
            segments.append([{"x": x, "y": run_start}, {"x": x, "y": prev + 1}])
            if y is not None:
                run_start = prev = y

    return segments


def extract_portals(matrix) -> list[dict]:
    portals = []
    h = len(matrix)
    w = len(matrix[0]) if h else 0
    for y in range(h):
        for x in range(w):
            if matrix[y][x] not in DOOR_SYMS:
                continue
            # orient the door across the wall run it sits in
            vertical_wall = _is_wall(matrix, x, y - 1) or _is_wall(matrix, x, y + 1)
            if vertical_wall:
                bounds = [{"x": x + 0.5, "y": y}, {"x": x + 0.5, "y": y + 1}]
            else:
                bounds = [{"x": x, "y": y + 0.5}, {"x": x + 1, "y": y + 0.5}]
            portals.append({
                "position": {"x": x + 0.5, "y": y + 0.5},
                "bounds": bounds,
                "rotation": 0,
                "closed": True,
                "freestanding": False,
            })
    return portals


def extract_lights(matrix, explicit=None) -> list[dict]:
    lights = []
    if explicit:
        for l in explicit:
            x, y = l["at"]
            lights.append({
                "position": {"x": x + 0.5, "y": y + 0.5},
                "range": float(l.get("range", 6.0)),
                "intensity": 1.0,
                "color": l.get("color", "ffd9a0"),
                "shadows": True,
            })
        return lights
    h = len(matrix)
    w = len(matrix[0]) if h else 0
    for y in range(h):
        for x in range(w):
            sym = matrix[y][x]
            if sym in LIGHT_SYMS:
                rng, color = LIGHT_SYMS[sym]
                if rng <= 0:
                    continue
                lights.append({
                    "position": {"x": x + 0.5, "y": y + 0.5},
                    "range": rng,
                    "intensity": 1.0,
                    "color": color,
                    "shadows": True,
                })
    return lights


def build_uvtt(gmap: dict, ppg: int, image_b64: str = "",
               explicit_lights=None) -> dict:
    matrix = _grid_matrix(gmap)
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    return {
        "format": 0.3,
        "resolution": {
            "map_origin": {"x": 0, "y": 0},
            "map_size": {"x": cols, "y": rows},
            "pixels_per_grid": ppg,
        },
        "line_of_sight": extract_walls(matrix),
        "objects_line_of_sight": [],
        "portals": extract_portals(matrix),
        "lights": extract_lights(matrix, explicit_lights),
        "environment": {"baked_lighting": False, "ambient_light": "ffffff"},
        "image": image_b64,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="markdown master con griglie emoji")
    ap.add_argument("-o", "--output", help="directory di output (default: rendered/vtt/ accanto al file)")
    ap.add_argument("--map", type=int, help="esporta solo la mappa N (1-based)")
    ap.add_argument("--ppg", type=int, default=100, help="pixel per quadretto nel VTT (default 100)")
    ap.add_argument("--ext", choices=["uvtt", "dd2vtt", "df2vtt"], default="uvtt",
                    help="estensione del file (default uvtt; dd2vtt per Dungeondraft)")
    ap.add_argument("--image", help="PNG di sfondo da incorporare in base64 (opzionale)")
    ap.add_argument("--list", action="store_true", help="elenca solo le mappe trovate")
    args = ap.parse_args(argv)

    if not args.file:
        ap.error("serve il file markdown (o --help)")

    src = Path(args.file)
    try:
        text = src.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        return 2

    maps = rms.extract_maps(text)
    if not maps:
        print(f"Nessuna griglia trovata in {src}", file=sys.stderr)
        return 1

    if args.list:
        for i, m in enumerate(maps, 1):
            w = max(len(r) for r in m["rows"].values())
            print(f"   {i}. {m['title']}  ({w}×{len(m['rows'])} celle)")
        return 0

    image_b64 = ""
    if args.image:
        img = Path(args.image)
        if img.exists():
            image_b64 = base64.b64encode(img.read_bytes()).decode("ascii")
        else:
            print(f"AVVISO: immagine {img} non trovata — 'image' resta vuoto.",
                  file=sys.stderr)

    out_dir = Path(args.output) if args.output else src.parent / "rendered" / "vtt"
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for i, m in enumerate(maps, 1):
        if args.map and i != args.map:
            continue
        uvtt = build_uvtt(m, args.ppg, image_b64)
        slug = rms.slugify(m["title"])
        name = f"{src.stem}_map{i:02d}_{slug}.{args.ext}"
        dest = out_dir / name
        dest.write_text(json.dumps(uvtt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {dest}  "
              f"({len(uvtt['line_of_sight'])} muri, {len(uvtt['portals'])} porte, "
              f"{len(uvtt['lights'])} luci)")
        count += 1

    if not count:
        print("Nessuna mappa esportata (indice --map fuori range?)", file=sys.stderr)
        return 1
    print(f"Totale: {count} file .{args.ext} — import nativo in Foundry VTT / Roll20.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
