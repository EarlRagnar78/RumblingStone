#!/usr/bin/env python3
"""
compile_map_json.py — compile a RIGID tactical-map JSON contract into an
emoji-grid markdown master (the repo's canonical map format).

This is the fix for "the LLM draws maps at random": an LLM must NEVER emit
ASCII art (it drifts by one square after a few rows and destroys the layout).
Instead it emits ONLY the structured JSON described by
`scripts/schemas/tactical_map.schema.json`; this script validates that JSON
against rigid geometric constraints and DETERMINISTICALLY paints the grid.
If the JSON is invalid, the script rejects it with precise errors (the LLM is
asked to correct and resend) — the LLM never touches pixels or coordinates on
the canvas directly.

Pipeline position (Modalita 3 — mappa tattica con strutture ed eserciti):

    [LLM] --(solo JSON valido)--> compile_map_json.py --> MASTER griglia-emoji
                                                              |
        render_map_svg.py (SVG)  <---------------------------+
        export_map_png.py (PNG stampa/VTT)                    |
        export_uvtt.py (.uvtt/.dd2vtt: muri + luci per Foundry/Roll20)

Army abstraction: units are UNITS/OCCUPIED-AREAS, not one token per soldier
(as Paizo modules reason). `quantity` is a number carried into the DM
companion table, never N separate tokens — so the LLM context never has to
track every creature.

Professional overlay: the JSON's `north`, `movements` (patrol routes), unit
roster and labelled areas are emitted as `@`-directives inside the fenced
block (@north / @path / @mark / @zone). render_map_svg.py draws them as a
compass, dashed movement arrows, numbered callouts and zone brackets, plus an
"INDICAZIONI" legend — so the rendered map carries positions, movements,
orientation and references (not just the bare grid).

Validation is pure standard library (no external deps, matching the rest of
the repo). The JSON Schema file is provided for editors/interop; `pydantic`
would be an equivalent stricter option but is intentionally NOT a dependency.

Usage:
    python3 scripts/compile_map_json.py spec.json -o <arco>/NUOVA-MAPPA.md
    python3 scripts/compile_map_json.py spec.json --validate-only
    python3 scripts/compile_map_json.py spec.json            # master to stdout

After compiling, render and (optionally) export for the VTT:
    python3 scripts/render_map_svg.py <arco>/NUOVA-MAPPA.md
    python3 scripts/export_uvtt.py    <arco>/NUOVA-MAPPA.md

Pure Python 3, no dependencies.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reuse the single source of truth for the universal legend.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map_svg as rms  # noqa: E402

SYMBOLS = rms.SYMBOLS
DEFAULT_BASE_TERRAIN = "🟩"

# Full line-of-sight blockers (used only to sanity-check structures here; the
# UVTT exporter owns the authoritative wall set).
FILL_SYMS = {s for s, d in SYMBOLS.items() if d.get("mode") == "fill"}
UNIT_SYMS = {s for s, d in SYMBOLS.items() if d.get("mode") == "unit"}


class SpecError(Exception):
    """Raised when the JSON contract is invalid. Message lists every error."""


# --------------------------------------------------------------------------- #
# Validation (rigid geometric contract)
# --------------------------------------------------------------------------- #
def _is_coord(v) -> bool:
    return isinstance(v, list) and len(v) == 2 and all(isinstance(n, int) for n in v)


def validate(spec: dict) -> tuple[int, int]:
    """Validate the spec. Return (cols, rows). Raise SpecError with all errors."""
    errors: list[str] = []

    if not isinstance(spec, dict):
        raise SpecError("La radice del JSON deve essere un oggetto.")

    # title
    title = spec.get("title")
    if not isinstance(title, str) or not (3 <= len(title) <= 100):
        errors.append("'title': stringa obbligatoria (3-100 caratteri).")

    # map_size
    size = spec.get("map_size")
    cols = rows = 0
    if not (isinstance(size, list) and len(size) == 2
            and all(isinstance(n, int) and 1 <= n <= 200 for n in size)):
        errors.append("'map_size': [colonne, righe] interi in [1..200].")
    else:
        cols, rows = size

    def check_symbol(sym, where, want_fill=False, want_unit=False):
        if not isinstance(sym, str) or sym not in SYMBOLS:
            errors.append(f"{where}: simbolo '{sym}' non nella legenda universale "
                          f"(vedi SYMBOLS in render_map_svg.py).")
            return
        mode = SYMBOLS[sym].get("mode")
        if want_fill and mode != "fill":
            errors.append(f"{where}: '{sym}' non e un terreno (modo 'fill').")
        if want_unit and mode != "unit":
            errors.append(f"{where}: '{sym}' non e un token unita (modo 'unit').")

    def in_bounds(x, y, where):
        if cols and rows and not (0 <= x < cols and 0 <= y < rows):
            errors.append(f"{where}: coordinata ({x},{y}) fuori dalla griglia "
                          f"{cols}x{rows}.")

    def check_rect(rect, where):
        if not (isinstance(rect, list) and len(rect) == 4
                and all(isinstance(n, int) for n in rect)):
            errors.append(f"{where}: 'rect' deve essere [x,y,larghezza,altezza] interi.")
            return
        x, y, w, h = rect
        if w <= 0 or h <= 0:
            errors.append(f"{where}: larghezza/altezza del rect devono essere > 0.")
        in_bounds(x, y, where)
        in_bounds(x + w - 1, y + h - 1, where)

    # base_terrain
    base = spec.get("base_terrain", DEFAULT_BASE_TERRAIN)
    check_symbol(base, "'base_terrain'", want_fill=True)

    # scale
    scale = spec.get("scale_m_per_square", 1.5)
    if not isinstance(scale, (int, float)) or scale <= 0:
        errors.append("'scale_m_per_square': numero > 0.")

    # regions
    for i, r in enumerate(spec.get("regions", []) or []):
        w = f"regions[{i}]"
        check_symbol(r.get("terrain"), w, want_fill=True)
        if "rect" in r:
            check_rect(r["rect"], w)
        elif "polygon" in r:
            poly = r["polygon"]
            if not (isinstance(poly, list) and len(poly) >= 3 and all(_is_coord(p) for p in poly)):
                errors.append(f"{w}: 'polygon' deve avere >=3 vertici [x,y].")
            else:
                for p in poly:
                    in_bounds(p[0], p[1], w)
        else:
            errors.append(f"{w}: serve 'rect' oppure 'polygon'.")

    # structures / hazards share the geometry vocabulary
    def check_placement(obj, w, allow_line=True):
        keys = [k for k in ("at", "line", "rect", "center") if k in obj]
        if not keys:
            errors.append(f"{w}: serve una fra 'at', 'line', 'rect', 'center'.")
        if "at" in obj:
            if _is_coord(obj["at"]):
                in_bounds(obj["at"][0], obj["at"][1], w)
            else:
                errors.append(f"{w}: 'at' deve essere [x,y].")
        if "line" in obj:
            if not allow_line:
                errors.append(f"{w}: 'line' non ammesso qui.")
            ln = obj["line"]
            if not (isinstance(ln, list) and len(ln) >= 2 and all(_is_coord(p) for p in ln)):
                errors.append(f"{w}: 'line' deve avere >=2 punti [x,y].")
            else:
                for p in ln:
                    in_bounds(p[0], p[1], w)
        if "rect" in obj:
            check_rect(obj["rect"], w)
        if "center" in obj:
            if _is_coord(obj["center"]):
                in_bounds(obj["center"][0], obj["center"][1], w)
                if not isinstance(obj.get("radius", 0), int) or obj.get("radius", 0) < 0:
                    errors.append(f"{w}: 'radius' intero >= 0 richiesto con 'center'.")
            else:
                errors.append(f"{w}: 'center' deve essere [x,y].")

    for i, s in enumerate(spec.get("structures", []) or []):
        w = f"structures[{i}]"
        check_symbol(s.get("type"), w)
        check_placement(s, w, allow_line=True)

    for i, h in enumerate(spec.get("hazards", []) or []):
        w = f"hazards[{i}]"
        check_symbol(h.get("type"), w)
        check_placement(h, w, allow_line=False)

    for i, l in enumerate(spec.get("lights", []) or []):
        w = f"lights[{i}]"
        if not _is_coord(l.get("at")):
            errors.append(f"{w}: 'at' [x,y] obbligatorio.")
        else:
            in_bounds(l["at"][0], l["at"][1], w)

    # north / orientation
    north = spec.get("north")
    if north is not None:
        ok = isinstance(north, str) and (
            north.upper() in {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
            or north.replace(".", "", 1).isdigit())
        if not ok:
            errors.append("'north': usa N/NE/E/SE/S/SW/W/NW o gradi (0-359).")

    # movements — patrol routes
    for i, mv in enumerate(spec.get("movements", []) or []):
        w = f"movements[{i}]"
        path = mv.get("path")
        if not (isinstance(path, list) and len(path) >= 2 and all(_is_coord(p) for p in path)):
            errors.append(f"{w}: 'path' deve avere >=2 waypoint [x,y].")
        else:
            for p in path:
                in_bounds(p[0], p[1], w)

    # units — army abstraction
    for i, u in enumerate(spec.get("units", []) or []):
        w = f"units[{i}]"
        check_symbol(u.get("token"), w, want_unit=True)
        if "at" in u:
            if _is_coord(u["at"]):
                in_bounds(u["at"][0], u["at"][1], w)
            else:
                errors.append(f"{w}: 'at' deve essere [x,y].")
        elif "area" in u and isinstance(u["area"], dict) and "rect" in u["area"]:
            check_rect(u["area"]["rect"], w + ".area")
        else:
            errors.append(f"{w}: serve 'at' oppure 'area.rect'.")
        if "quantity" in u and (not isinstance(u["quantity"], int) or u["quantity"] < 1):
            errors.append(f"{w}: 'quantity' intero >= 1.")

    if errors:
        raise SpecError("JSON non valido — correggi e reinvia:\n  - " + "\n  - ".join(errors))
    return cols, rows


# --------------------------------------------------------------------------- #
# Painting
# --------------------------------------------------------------------------- #
def _new_grid(cols: int, rows: int, base: str) -> list[list[str]]:
    return [[base for _ in range(cols)] for _ in range(rows)]


def _set(grid, x, y, sym):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        grid[y][x] = sym


def _fill_rect(grid, rect, sym):
    x, y, w, h = rect
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            _set(grid, xx, yy, sym)


def _draw_line(grid, p0, p1, sym):
    x0, y0 = p0
    x1, y1 = p1
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        _set(grid, x0, y0, sym)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _fill_disk(grid, center, radius, sym):
    cx, cy = center
    for yy in range(cy - radius, cy + radius + 1):
        for xx in range(cx - radius, cx + radius + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= radius ** 2:
                _set(grid, xx, yy, sym)


def _fill_polygon(grid, pts, sym):
    ys = [p[1] for p in pts]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(round(xs[i])), int(round(xs[i + 1])) + 1):
                _set(grid, x, y, sym)


def paint(spec: dict, cols: int, rows: int) -> list[list[str]]:
    base = spec.get("base_terrain", DEFAULT_BASE_TERRAIN)
    grid = _new_grid(cols, rows, base)

    for r in spec.get("regions", []) or []:
        if "rect" in r:
            _fill_rect(grid, r["rect"], r["terrain"])
        elif "polygon" in r:
            _fill_polygon(grid, r["polygon"], r["terrain"])

    for s in spec.get("structures", []) or []:
        sym = s["type"]
        if "rect" in s:
            _fill_rect(grid, s["rect"], sym)
        if "center" in s:
            _fill_disk(grid, s["center"], s.get("radius", 0), sym)
        if "line" in s:
            pts = s["line"]
            for i in range(len(pts) - 1):
                _draw_line(grid, pts[i], pts[i + 1], sym)
        if "at" in s:  # placed last so a door in a wall line stays visible
            _set(grid, s["at"][0], s["at"][1], sym)

    for h in spec.get("hazards", []) or []:
        sym = h["type"]
        if "rect" in h:
            _fill_rect(grid, h["rect"], sym)
        if "at" in h:
            _set(grid, h["at"][0], h["at"][1], sym)

    # units on top: stamp the occupied footprint so a mass unit reads as a
    # block of cells; the count lives in the companion table.
    for u in spec.get("units", []) or []:
        tok = u["token"]
        if "area" in u and "rect" in u["area"]:
            _fill_rect(grid, u["area"]["rect"], tok)
        elif "at" in u:
            _set(grid, u["at"][0], u["at"][1], tok)

    return grid


# --------------------------------------------------------------------------- #
# Master emission
# --------------------------------------------------------------------------- #
def _coord_label(x: int, y: int) -> str:
    return f"{rms.col_label(x)}{y + 1}"


def _unit_cell(u: dict) -> tuple[int, int] | None:
    if "at" in u and _is_coord(u["at"]):
        return tuple(u["at"])
    if "area" in u and isinstance(u["area"], dict) and "rect" in u["area"]:
        x, y, w, h = u["area"]["rect"]
        return x + w // 2, y + h // 2
    return None


def _annotation_lines(spec: dict) -> list[str]:
    """Render the JSON's orientation, movements, unit roster and labelled
    areas as `@`-directives that render_map_svg.py draws as an overlay."""
    lines: list[str] = []
    if spec.get("north"):
        lines.append(f"@north {spec['north']}")

    # numbered roster (one @mark per unit)
    for i, u in enumerate(spec.get("units", []) or [], 1):
        cell = _unit_cell(u)
        if not cell:
            continue
        name = u.get("name", SYMBOLS.get(u["token"], {}).get("it", u["token"]))
        if u.get("cr"):
            name = f"{name} ({u['cr']})"
        lines.append(f"@mark {i} ; {_coord_label(*cell)} ; {name}")

    # movement routes
    for mv in spec.get("movements", []) or []:
        pts = " ".join(_coord_label(*p) for p in mv["path"])
        if mv.get("loop"):
            pts += " loop"
        color = mv.get("color", "#c81d25")
        lines.append(f"@path {mv.get('name', 'Rotta')} ; {pts} ; {color}")

    # labelled areas (structures/hazards with rect + label)
    for obj in (spec.get("structures", []) or []) + (spec.get("hazards", []) or []):
        if "rect" in obj and obj.get("label"):
            x, y, w, h = obj["rect"]
            lines.append(f"@zone {_coord_label(x, y)}-{_coord_label(x + w - 1, y + h - 1)}"
                         f" ; {obj['label']}")
    return lines


def emit_master(spec: dict, grid: list[list[str]]) -> str:
    cols = len(grid[0])
    rows = len(grid)
    scale = spec.get("scale_m_per_square", 1.5)
    scale_str = ("%g" % scale).replace(".", ",")
    title = spec["title"]
    width_m = ("%g" % (cols * scale)).replace(".", ",")
    height_m = ("%g" % (rows * scale)).replace(".", ",")

    out: list[str] = []
    out.append(f"# {title}")
    out.append("")
    out.append(f"**Dimensioni**: {width_m} m × {height_m} m "
               f"({cols} colonne × {rows} righe, scala {scale_str} m/quadretto)  ")
    out.append("**Origine**: generata da `scripts/compile_map_json.py` "
               "(contratto JSON → griglia; non modificare la griglia a mano, "
               "rigenerala dal JSON)  ")
    out.append("**SVG**: rigenerare con "
               "`python3 scripts/render_map_svg.py <questo-file>.md`  ")
    out.append("**VTT**: esportare con "
               "`python3 scripts/export_uvtt.py <questo-file>.md`")
    out.append("")
    out.append("## Griglia")
    out.append("")

    # column ruler as a comment line (never parsed as a grid row)
    ruler = "COLONNE:  " + " ".join(rms.col_label(x) for x in range(cols))
    out.append("```")
    out.append(title)  # banner picked up by render_map_svg
    out.append(ruler)
    for y in range(rows):
        cells = " ".join(grid[y])
        out.append(f"{y + 1:02d} {cells}")

    # --- annotation directives (compass, routes, callouts, zones) -----------
    ann_lines = _annotation_lines(spec)
    if ann_lines:
        out.append("")
        out.extend(ann_lines)
    out.append("```")
    out.append("")

    # ---- Companion DM (three blocks per campaign/templates/mappa-tattica) --
    out.append("### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)")
    out.append("")
    out.append("| Elemento | Dove (coord.) | Effetto meccanico 3.5 |")
    out.append("|---|---|---|")
    hz = spec.get("hazards", []) or []
    if hz:
        for h in hz:
            where = _placement_coords(h)
            label = h.get("label") or SYMBOLS.get(h["type"], {}).get("it", h["type"])
            effect = h.get("effect", "[INFERRED — needs DM confirmation]")
            out.append(f"| {h['type']} {label} | {where} | {effect} |")
    else:
        out.append("| Luce | … | [luce/oscurità, scurovisione a X m] |")
        out.append("| Terreno | … | [difficile ×2, copertura +4 CA, occultamento 20%…] |")
    out.append("")

    out.append("### ⚔️ TATTICHE (come si comportano i nemici — round per round)")
    out.append("")
    units = spec.get("units", []) or []
    if units:
        out.append("**Forze in campo** (astrazione per unità — un blocco = un'unità, "
                   "non un token per creatura):")
        out.append("")
        out.append("| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |")
        out.append("|---|---|---|---|---|---|")
        for u in units:
            faction = u.get("faction", "—")
            name = u.get("name", SYMBOLS.get(u["token"], {}).get("it", u["token"]))
            qty = u.get("quantity", 1)
            cr = u.get("cr", "—")
            where = _placement_coords(u)
            out.append(f"| {faction} | {name} | {u['token']} | {qty} | {cr} | {where} |")
        out.append("")
    out.append("- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]")
    out.append("- **Round 1-2**: [reazione al contatto]")
    out.append("- **Round 3+**: [piano B, focus-fire, uso del terreno]")
    out.append("- **Morale**: [soglia di ripiegamento/resa]")
    out.append("")

    out.append("### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)")
    out.append("")
    out.append("| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |")
    out.append("|---|---|---|---|")
    out.append("| A (iniziale) | — | com'è disegnata | — |")
    for note in (spec.get("notes", []) or []):
        out.append(f"| B | [trigger] | {note} | [effetto] |")
    if not (spec.get("notes")):
        out.append("| B | [evento/round/allarme] | [celle che cambiano] | [nuove CD/danni/EL] |")
    out.append("")
    out.append("> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle "
               "scelte dei PG, mai del copione.")
    out.append("")
    return "\n".join(out)


def _placement_coords(obj: dict) -> str:
    if "at" in obj and _is_coord(obj["at"]):
        return _coord_label(*obj["at"])
    if "area" in obj and isinstance(obj["area"], dict) and "rect" in obj["area"]:
        x, y, w, h = obj["area"]["rect"]
        return f"{_coord_label(x, y)}–{_coord_label(x + w - 1, y + h - 1)}"
    if "rect" in obj:
        x, y, w, h = obj["rect"]
        return f"{_coord_label(x, y)}–{_coord_label(x + w - 1, y + h - 1)}"
    if "center" in obj:
        return _coord_label(*obj["center"])
    if "line" in obj:
        pts = obj["line"]
        return f"{_coord_label(*pts[0])}→{_coord_label(*pts[-1])}"
    return "…"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="file JSON del contratto mappa")
    ap.add_argument("-o", "--output", help="scrivi il master su file (default: stdout)")
    ap.add_argument("--validate-only", action="store_true",
                    help="valida soltanto, senza generare il master")
    args = ap.parse_args(argv)

    if not args.spec:
        ap.error("serve il file JSON del contratto (o --help)")

    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERRORE: impossibile leggere/parsare {args.spec}: {e}", file=sys.stderr)
        return 2

    try:
        cols, rows = validate(spec)
    except SpecError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1

    if args.validate_only:
        print(f"✓ JSON valido — griglia {cols}×{rows}, "
              f"{len(spec.get('units', []) or [])} unità, "
              f"{len(spec.get('structures', []) or [])} strutture.")
        return 0

    grid = paint(spec, cols, rows)
    master = emit_master(spec, grid)

    if args.output:
        Path(args.output).write_text(master + "\n", encoding="utf-8")
        print(f"✓ master scritto: {args.output} (griglia {cols}×{rows})\n"
              f"  render:  python3 scripts/render_map_svg.py {args.output}\n"
              f"  VTT:     python3 scripts/export_uvtt.py {args.output}")
    else:
        print(master)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
