#!/usr/bin/env python3
"""
import_watabou.py — convert a Watabou "One Page Dungeon" JSON export into an
emoji-grid map master conforming to the repo's tactical-map template.

Workflow (Fase 2 of plans/RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md):
  1. Generate a dungeon at https://watabou.github.io/dungeon.html
  2. Export → JSON (the export is a plain list of rectangular rooms/corridors
     plus doors, columns, water cells and numbered notes).
  3. python3 scripts/import_watabou.py dungeon.json -o <arc-dir>/NUOVA-MAPPA.md
  4. Fill in the companion blocks (Ambiente / Tattiche / Evoluzione) per
     `campaign/templates/mappa-tattica-template.md`.
  5. python3 scripts/render_map_svg.py <arc-dir>/NUOVA-MAPPA.md

Symbol mapping (universal legend of the repo):
  outside rooms → 🏰 (roccia solida)   room/corridor floor → ⬜
  doors (any type) → 🚪                 columns → 🟪
  water cells → 🟦                      numbered notes → ⭐ (text listed below)

The generator is free but not open source; only its documented JSON export
format is used here. The output markdown is a normal map MASTER: it stays
human-editable and diffable, and renders with render_map_svg.py.

Pure Python 3, no dependencies.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import unicodedata
from pathlib import Path

ROCK, FLOOR, DOOR, PILLAR, WATER, NOTE = "🏰", "⬜", "🚪", "🟪", "🟦", "⭐"


def col_label(i: int) -> str:
    label = ""
    i += 1
    while i > 0:
        i, rem = divmod(i - 1, 26)
        label = chr(ord("A") + rem) + label
    return label


def slugify(title: str) -> str:
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    import re
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:48] or "mappa"


def _cells_of_rect(rect: dict) -> list[tuple[int, int]]:
    """All (x, y) cells covered by a room; 'rotunda' rooms are carved round."""
    x0, y0 = rect["x"], rect["y"]
    w, h = rect["w"], rect["h"]
    cells = []
    if rect.get("rotunda"):
        cx, cy, r = x0 + w / 2, y0 + h / 2, min(w, h) / 2
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if math.hypot(x + 0.5 - cx, y + 0.5 - cy) <= r + 0.15:
                    cells.append((x, y))
    else:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                cells.append((x, y))
    return cells


def convert(data: dict, pad: int = 1) -> tuple[str, list[str], str]:
    """Return (title, grid rows as emoji strings, notes markdown)."""
    title = (data.get("title") or "Dungeon senza nome").strip()
    rects = data.get("rects") or []
    if not rects:
        raise SystemExit("ERRORE: il JSON non contiene 'rects' — non è un export One Page Dungeon?")

    floor: set[tuple[int, int]] = set()
    for rect in rects:
        floor.update(_cells_of_rect(rect))

    def cell_pt(obj: dict) -> tuple[int, int]:
        return int(math.floor(obj["x"])), int(math.floor(obj["y"]))

    doors = [cell_pt(d) for d in (data.get("doors") or [])]
    columns = [cell_pt(c) for c in (data.get("columns") or [])]
    water = [cell_pt(w) for w in (data.get("water") or [])]
    notes = data.get("notes") or []
    note_cells: dict[tuple[int, int], str] = {}
    for n in notes:
        pos = n.get("pos") or {}
        if "x" in pos and "y" in pos:
            note_cells[(int(math.floor(pos["x"])), int(math.floor(pos["y"])))] = \
                str(n.get("ref", "•"))

    everything = list(floor) + doors + columns + water + list(note_cells)
    min_x = min(x for x, _ in everything) - pad
    min_y = min(y for _, y in everything) - pad
    max_x = max(x for x, _ in everything) + pad
    max_y = max(y for _, y in everything) + pad
    n_cols = max_x - min_x + 1
    n_rows = max_y - min_y + 1
    if n_cols > 120 or n_rows > 120:
        raise SystemExit(f"ERRORE: dungeon {n_cols}×{n_rows} troppo grande (limite 120×120)")

    grid = [[ROCK] * n_cols for _ in range(n_rows)]

    def put(x: int, y: int, sym: str) -> None:
        grid[y - min_y][x - min_x] = sym

    for x, y in floor:
        put(x, y, FLOOR)
    for x, y in water:
        put(x, y, WATER)
    for x, y in columns:
        put(x, y, PILLAR)
    for x, y in doors:
        put(x, y, DOOR)
    for (x, y) in note_cells:
        put(x, y, NOTE)

    rows = ["".join(r) for r in grid]

    notes_md = ""
    if notes:
        lines = ["", "**Note del generatore** (⭐ sulla griglia, da adattare alla campagna):", ""]
        for n in notes:
            ref = n.get("ref", "•")
            pos = n.get("pos") or {}
            coord = ""
            if "x" in pos and "y" in pos:
                cx = int(math.floor(pos["x"])) - min_x
                cy = int(math.floor(pos["y"])) - min_y + 1
                coord = f" ({col_label(cx)}{cy:02d})"
            lines.append(f"- **{ref}**{coord}: {n.get('text', '').strip()}")
        notes_md = "\n".join(lines) + "\n"
    return title, rows, notes_md


def build_markdown(title: str, rows: list[str], notes_md: str, story: str,
                   out_name: str) -> str:
    n_rows, n_cols = len(rows), len(rows[0])
    dims = f"{n_cols * 1.5:g}m × {n_rows * 1.5:g}m ({n_cols} colonne × {n_rows} righe, scala 1,5 m/quadretto)"
    banner = f"{title.upper()} ({n_cols * 1.5:g}m x {n_rows * 1.5:g}m, Grid {n_cols}x{n_rows}, Scala 1,5m/sq)"
    header_cols = "COLONNE →  " + " ".join(col_label(c) for c in range(n_cols))

    grid_lines = [banner, "", header_cols, ""]
    for i, row in enumerate(rows, 1):
        grid_lines.append(f"{i:02d} {row}")

    story_block = f"\n> {story.strip()}\n" if story else ""
    svg_name = f"rendered/{out_name}_map01_<slug>.svg"

    return f"""# {title} — [Parte/Scena, Arco DA ASSEGNARE]

> Griglia generata da `scripts/import_watabou.py` a partire da un export JSON
> del One Page Dungeon di Watabou (https://watabou.github.io/dungeon.html).
> Questo file è il MASTER: adattarlo alla campagna (simboli unità, pericoli,
> callout) e compilare i blocchi companion secondo
> `campaign/templates/mappa-tattica-template.md`.
{story_block}
**Dimensioni**: {dims}
**Incontro**: [DA COMPILARE — chi c'è, EL, link statblock]
**Quando si usa**: [DA COMPILARE — scena/trigger]
**SVG**: `{svg_name}` (rigenerare con `python3 scripts/render_map_svg.py` dopo ogni modifica)

### Griglia

```
{chr(10).join(grid_lines)}
```
{notes_md}
### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| Luce | [DA COMPILARE] | [DA COMPILARE] |
| Terreno | [DA COMPILARE] | [DA COMPILARE] |
| Pericoli | [DA COMPILARE] | [DA COMPILARE] |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

- **Disposizione iniziale**: [DA COMPILARE]
- **Round 1-2**: [DA COMPILARE]
- **Round 3+**: [DA COMPILARE]
- **Morale**: [DA COMPILARE]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [DA COMPILARE] | [DA COMPILARE] | [DA COMPILARE] |
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_file", help="export JSON del One Page Dungeon di Watabou")
    ap.add_argument("-o", "--out", help="file markdown di destinazione "
                                        "(default: <slug-del-titolo>.md accanto al JSON)")
    ap.add_argument("--pad", type=int, default=1,
                    help="quadretti di roccia solida attorno al dungeon (default: 1)")
    args = ap.parse_args()

    src = Path(args.json_file)
    if not src.exists():
        print(f"ERRORE: {src} non esiste", file=sys.stderr)
        return 1
    data = json.loads(src.read_text(encoding="utf-8"))
    title, rows, notes_md = convert(data, pad=max(0, args.pad))

    out = Path(args.out) if args.out else src.with_name(f"{slugify(title)}.md")
    md = build_markdown(title, rows, notes_md, data.get("story", ""), out.stem)
    out.write_text(md, encoding="utf-8")
    n_rows, n_cols = len(rows), len(rows[0])
    print(f"✓ {out}  ({n_cols}×{n_rows} quadretti, {len(data.get('rects') or [])} stanze/corridoi)")
    print(f"  ora: 1) adatta la griglia alla campagna  2) compila i companion  "
          f"3) python3 scripts/render_map_svg.py {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
