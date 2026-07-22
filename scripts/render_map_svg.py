#!/usr/bin/env python3
"""
render_map_svg.py — render the campaign's emoji-grid tactical maps to SVG.

The revised maps of ARC-07/08/09 (files `*Ultra-Clear*.md`, `*MAPPE*.md`,
`SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`, ...) share one format:
fenced code blocks whose rows start with a 2-digit row number followed by
emoji cells (with or without spaces). This script parses those grids and
emits print-quality SVG battlemaps in the "pergamena" (parchment) style:

  - procedurally textured terrain, merged into ORGANIC regions (traced cell
    contours smoothed by corner-cutting, so caves and coasts curve instead
    of stair-stepping);
  - inked hand-drawn boundaries, ambient-occlusion darkening beside walls,
    cast shadows of walls/structures, low-frequency tonal mottling that
    breaks texture repetition;
  - an ORIGINAL vector prop library (door, bed, crate, brazier, tree, …)
    drawn in-house — icons render as illustrated objects, not emoji;
  - VTT-style unit tokens, 1,5 m/quadretto grid, coordinates, scale bar,
    a compass rose (orientation) and a textured legend.

Optional `@`-directives inside the fenced block (after the grid) add a
professional overlay + an "INDICAZIONI" legend — orientation, movement
routes, numbered callouts and labelled zones (see parse_annotations):
    @north <deg|N|NE|E|SE|S|SW|W|NW>   rotate the compass ("up" = this dir)
    @path  <label> ; <c1 c2 c3 ...[ loop]> ; [#rrggbb]   movement route
    @mark  <n> ; <coord> ; <text>                        numbered callout
    @zone  <c1-c2> ; <text>                               labelled area
Coordinates use A1 labels (column letters + printed row number, e.g. "M6").
`scripts/compile_map_json.py` emits these directives from a JSON contract.

Everything is generated procedurally (SVG patterns + filters + in-house
symbols): no external image assets, no licensing constraints, and
byte-deterministic output (enforced by scripts/validate_maps.py in CI).

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
import math
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
# mode "icon":   illustrated in-house prop ("prop" = symbol id) anchored by
#                a ground blot; the underlying terrain is inherited from the
#                nearest terrain cell. Icons without a prop (local symbols)
#                fall back to the emoji glyph.
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
    "⛰": {"mode": "fill", "pat": "t_mountain", "fill": "#8d8271", "it": "Montagne / creste rocciose"},
    "🪨": {"mode": "icon", "prop": "pr_rocks", "fill": "#ced4da", "it": "Rocce/macerie (copertura +4 CA, terreno difficile)"},
    "🔥": {"mode": "icon", "prop": "pr_fire", "fill": "#ffb4a2", "it": "Fuoco (1d6 fuoco/round)"},
    "💥": {"mode": "icon", "prop": "pr_boom", "fill": "#ffb4a2", "it": "Fiamme / esplosione"},
    "💀": {"mode": "icon", "prop": "pr_skull", "fill": "#e9ecef", "it": "Fossa / trappola"},
    "🕳": {"mode": "icon", "prop": "pr_pit", "fill": "#495057", "it": "Voragine / buco"},
    # units (tokens)
    "🔵": {"mode": "unit", "fill": "#1d6fd8", "it": "PG / alleati"},
    "🔴": {"mode": "unit", "fill": "#d62828", "it": "Nemico standard"},
    "⚫": {"mode": "unit", "fill": "#212529", "it": "Boss / comandante"},
    "🟡": {"mode": "unit", "fill": "#f4b400", "it": "Incantatore nemico"},
    "🟢": {"mode": "unit", "fill": "#2b9348", "it": "Creatura evocata / bestia"},
    "🟣": {"mode": "unit", "fill": "#9d4edd", "it": "Creatura speciale"},
    # specials (illustrated props)
    "🌳": {"mode": "icon", "prop": "pr_tree", "fill": "#b7e4c7", "it": "Treant / creatura vegetale"},
    "⭐": {"mode": "icon", "prop": "pr_star", "fill": "#fff3b0", "it": "Obiettivo primario"},
    "🚪": {"mode": "icon", "prop": "pr_door", "fill": "#e6ccb2", "it": "Porta / ingresso"},
    "🗼": {"mode": "icon", "prop": "pr_tower", "fill": "#dee2e6", "it": "Torre / struttura alta"},
    "🏺": {"mode": "icon", "prop": "pr_urn", "fill": "#f8f9fa", "it": "Contenitore / bottino"},
    "🔔": {"mode": "icon", "prop": "pr_bell", "fill": "#fff3b0", "it": "Allarme / trappola sonora"},
    "💎": {"mode": "icon", "prop": "pr_gem", "fill": "#caf0f8", "it": "Tesoro / oggetto magico"},
    "👑": {"mode": "icon", "prop": "pr_crown", "fill": "#fff3b0", "it": "Trono / Corona"},
    "🏮": {"mode": "icon", "prop": "pr_brazier", "fill": "#ffd166", "it": "Braciere / fonte di luce"},
    "🪓": {"mode": "icon", "prop": "pr_rack", "fill": "#e9ecef", "it": "Rastrelliera / armi"},
    "🛏": {"mode": "icon", "prop": "pr_bed", "fill": "#e9ecef", "it": "Giaciglio"},
    "📦": {"mode": "icon", "prop": "pr_crate", "fill": "#e6ccb2", "it": "Casse / rifornimenti"},
    "🐴": {"mode": "icon", "prop": "pr_horse", "fill": "#e6ccb2", "it": "Cavalcature"},
    "🕸": {"mode": "icon", "prop": "pr_web", "fill": "#dee2e6", "it": "Ragnatele (terreno difficile)"},
    "❄": {"mode": "icon", "prop": "pr_ice", "fill": "#caf0f8", "it": "Ghiaccio"},
    "⚡": {"mode": "icon", "prop": "pr_bolt", "fill": "#fff3b0", "it": "Energia / pericolo magico"},
    "🌀": {"mode": "icon", "prop": "pr_portal", "fill": "#caf0f8", "it": "Portale / vortice"},
    # markers and props promoted from the arcs' local legends
    "⬇": {"mode": "icon", "prop": "pr_down", "fill": "#dee2e6", "it": "Discesa / pendenza"},
    "🏛": {"mode": "icon", "prop": "pr_temple", "fill": "#dee2e6", "it": "Edificio / tempio"},
    "🌋": {"mode": "icon", "prop": "pr_volcano", "fill": "#ffb4a2", "it": "Bocca vulcanica / fumarola"},
    "🗿": {"mode": "icon", "prop": "pr_statue", "fill": "#dee2e6", "it": "Statua"},
    "🌉": {"mode": "icon", "prop": "pr_bridge", "fill": "#e6ccb2", "it": "Ponte / passerella"},
    "🎯": {"mode": "icon", "prop": "pr_target", "fill": "#fff3b0", "it": "Obiettivo tattico"},
    "🖼": {"mode": "icon", "prop": "pr_mural", "fill": "#dee2e6", "it": "Affresco / quadro"},
    "✨": {"mode": "icon", "prop": "pr_sparkle", "fill": "#fff3b0", "it": "Effetto magico attivo"},
    "⚔": {"mode": "icon", "prop": "pr_swords", "fill": "#dee2e6", "it": "Zona di scontro"},
    # dungeon & wilderness dressing (available to every map master)
    "⚰": {"mode": "icon", "prop": "pr_coffin", "fill": "#e6ccb2", "it": "Sarcofago / bara"},
    "🛢": {"mode": "icon", "prop": "pr_barrel", "fill": "#e6ccb2", "it": "Barile"},
    "🪜": {"mode": "icon", "prop": "pr_stairs", "fill": "#dee2e6", "it": "Scale / rampa"},
    "🦴": {"mode": "icon", "prop": "pr_bones", "fill": "#e9ecef", "it": "Ossa / resti"},
    "🍄": {"mode": "icon", "prop": "pr_mushrooms", "fill": "#ffb4a2", "it": "Funghi giganti"},
    "🕯": {"mode": "icon", "prop": "pr_candles", "fill": "#fff3b0", "it": "Candele / rituale"},
    "🌾": {"mode": "icon", "prop": "pr_bush", "fill": "#b7e4c7", "it": "Erba alta / cespugli (occultamento)"},
    "⛺": {"mode": "icon", "prop": "pr_tent", "fill": "#e6ccb2", "it": "Tenda"},
    "🔮": {"mode": "icon", "prop": "pr_crystal", "fill": "#caf0f8", "it": "Cristalli / altare magico"},
    "🪑": {"mode": "icon", "prop": "pr_table", "fill": "#e6ccb2", "it": "Tavolo e sedie"},
    "🧱": {"mode": "icon", "prop": "pr_lowwall", "fill": "#e6ccb2", "it": "Muretto / copertura bassa (+4 CA)"},
}
DEFAULT_TERRAIN = {"mode": "fill", "fill": PAPER, "it": ""}

# walls, buildings, pillars and massifs cast a shadow and get the heavy
# ink outline (plus a light grid on top, so squares stay countable)
HEAVY_PATS = {"t_wall", "t_struct", "t_pillar", "t_mountain"}

# paint order: backgrounds first, solids last (small overlaps hide seams)
Z_ORDER = ["t_grass", "t_veg", "t_sand", "t_earth", "t_floor", "t_lava",
           "t_lethal", "t_deep", "t_water", "t_forest", "t_mountain",
           "t_struct", "t_pillar", "t_wall"]

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
    "t_mountain": _pattern("t_mountain", 42,
        '<rect width="42" height="42" fill="#8d8271"/>'
        '<path d="M2 22L11 6l9 16z" fill="#a49a87"/>'
        '<path d="M11 6l9 16h-9z" fill="#6f6553"/>'
        '<path d="M2 22L11 6l9 16" stroke="#4a4237" stroke-width="1" fill="none"/>'
        '<path d="M20 40l8-14 8 14z" fill="#a49a87"/>'
        '<path d="M28 26l8 14h-8z" fill="#6f6553"/>'
        '<path d="M20 40l8-14 8 14" stroke="#4a4237" stroke-width="1" fill="none"/>'
        '<path d="M28 16l6-10 6 10z" fill="#9c9280"/>'
        '<path d="M34 6l6 10h-6z" fill="#776b58"/>'
        '<circle cx="7" cy="30" r="1" fill="#776b58"/>'
        '<circle cx="16" cy="36" r="0.9" fill="#a49a87"/>'),
}

# ---------------------------------------------------------------------------
# In-house illustrated prop library (original vector art, drawn for this
# repo following pro-cartography conventions: ink outline, muted palette,
# small highlight — inspired by the *conventions* of published AP maps,
# every path authored from scratch here).
# ---------------------------------------------------------------------------

_PK = "#2f2415"  # prop ink


def _symbol(pid: str, body: str) -> str:
    return f'<symbol id="{pid}" viewBox="0 0 28 28">{body}</symbol>'


PROPS: dict[str, str] = {
    "pr_door": _symbol("pr_door",
        f'<rect x="5" y="9.5" width="18" height="9" rx="1.4" fill="#8a6032" stroke="{_PK}" stroke-width="1.2"/>'
        '<path d="M9.5 9.5v9M14 9.5v9M18.5 9.5v9" stroke="#6e4b26" stroke-width="1"/>'
        f'<circle cx="7.2" cy="14" r="0.9" fill="{_PK}"/><circle cx="20.8" cy="14" r="0.9" fill="{_PK}"/>'),
    "pr_rocks": _symbol("pr_rocks",
        f'<path d="M5 16l3-5.5 5.5-1.5 3.5 4-1 5.5-7 2.5z" fill="#9b917f" stroke="{_PK}" stroke-width="1.1"/>'
        '<path d="M8 10.5l5.5-1.5 1 4.5-6.5 2z" fill="#b0a692"/>'
        f'<path d="M16 19l2-4.5 5-1 2.5 4-3 4.5h-4.5z" fill="#8a8071" stroke="{_PK}" stroke-width="1"/>'
        '<path d="M18 14.5l5-1 1.5 2.5-5.5 1z" fill="#a29885"/>'
        '<circle cx="12" cy="21.5" r="1" fill="#6f6552"/>'
        '<circle cx="20" cy="9" r="1.2" fill="#776b58"/>'),
    "pr_rocks_b": _symbol("pr_rocks_b",
        f'<path d="M11 8l5.5 1 2.5 5-2.5 5-6 .5-2.5-5z" fill="#948a77" stroke="{_PK}" stroke-width="1.1"/>'
        '<path d="M11 8l5.5 1 1 3.5-6 1z" fill="#aca28e"/>'
        f'<path d="M6 18.5l1.5-3.5 4-.5 1.5 3-1.5 3.5h-4z" fill="#8a8071" stroke="{_PK}" stroke-width="1"/>'
        '<path d="M7.5 15l4-.5 1 2-4.5 1z" fill="#a29885"/>'
        '<circle cx="19.5" cy="20.5" r="1.6" fill="#8a8071" stroke="#2f2415" stroke-width="0.8"/>'
        '<circle cx="6.5" cy="9.5" r="1" fill="#776b58"/>'),
    "pr_fire": _symbol("pr_fire",
        '<path d="M14 4c4 5 7 8 7 13a7 7 0 0 1-14 0c0-5 3-8 7-13z" fill="#e2762d" stroke="#8a3c14" stroke-width="1"/>'
        '<path d="M14 9c2.5 3.5 4.5 5.5 4.5 8.5a4.5 4.5 0 0 1-9 0c0-3 2-5 4.5-8.5z" fill="#f2a93b"/>'
        '<path d="M14 14c1.3 1.8 2.3 2.8 2.3 4.4a2.3 2.3 0 0 1-4.6 0c0-1.6 1-2.6 2.3-4.4z" fill="#f8d778"/>'),
    "pr_boom": _symbol("pr_boom",
        '<path d="M14 3l2.2 6 5-3.6-1.8 5.9 6.2.7-5.2 3.4 4 4.8-6-1.4.2 6.2-4.6-4.2-4.6 4.2.2-6.2-6 1.4 4-4.8-5.2-3.4 6.2-.7-1.8-5.9 5 3.6z" '
        'fill="#d9542f" stroke="#7e2810" stroke-width="1"/>'
        '<circle cx="14" cy="14" r="4.5" fill="#f2a93b"/><circle cx="14" cy="14" r="2.2" fill="#f8d778"/>'),
    "pr_skull": _symbol("pr_skull",
        f'<circle cx="14" cy="12.5" r="7" fill="#e8e2d2" stroke="{_PK}" stroke-width="1.1"/>'
        f'<rect x="10.5" y="17" width="7" height="5" rx="1.5" fill="#e8e2d2" stroke="{_PK}" stroke-width="1.1"/>'
        f'<circle cx="11.3" cy="12" r="1.8" fill="{_PK}"/><circle cx="16.7" cy="12" r="1.8" fill="{_PK}"/>'
        f'<path d="M14 14.2l-1.1 2.2h2.2z" fill="{_PK}"/>'
        f'<path d="M12.2 18.6v2.2M14 18.6v2.2M15.8 18.6v2.2" stroke="{_PK}" stroke-width="0.8"/>'),
    "pr_pit": _symbol("pr_pit",
        '<ellipse cx="14" cy="14" rx="9.5" ry="7.5" fill="#141009" stroke="#4d4132" stroke-width="1.4"/>'
        '<ellipse cx="14" cy="12.6" rx="7" ry="5" fill="#000000" opacity="0.65"/>'
        '<path d="M6 16.5q4 4 12 2.7" stroke="#6a5c46" stroke-width="0.8" fill="none" opacity="0.7"/>'),
    "pr_tree": _symbol("pr_tree",
        '<circle cx="14" cy="14" r="9.2" fill="#4a6a42" stroke="#26331f" stroke-width="1.2"/>'
        '<circle cx="9" cy="10" r="4.2" fill="#567a4c"/>'
        '<circle cx="18.5" cy="10.5" r="3.6" fill="#516f47"/>'
        '<circle cx="19" cy="17.5" r="3.8" fill="#43603b"/>'
        '<circle cx="10.5" cy="18.5" r="4" fill="#47653f"/>'
        '<circle cx="14" cy="13" r="3.6" fill="#5d8153"/>'
        '<path d="M20.5 18.5A9.2 9.2 0 0 1 9.5 21.2" stroke="#33492d" stroke-width="1.6" fill="none" opacity="0.7"/>'
        '<circle cx="9.5" cy="9.5" r="1.6" fill="#6f9163"/>'
        '<circle cx="12.5" cy="11.5" r="1" fill="#6f9163"/>'),
    "pr_tree_b": _symbol("pr_tree_b",
        '<circle cx="14" cy="14" r="8.6" fill="#50704a" stroke="#26331f" stroke-width="1.2"/>'
        '<circle cx="17.5" cy="9.5" r="4" fill="#5d8153"/>'
        '<circle cx="9.5" cy="12" r="3.8" fill="#567a4c"/>'
        '<circle cx="16.5" cy="18" r="4.2" fill="#43603b"/>'
        '<circle cx="12" cy="16.5" r="3" fill="#4c6b44"/>'
        '<path d="M19.8 18.8A8.6 8.6 0 0 1 10.2 20.8" stroke="#33492d" stroke-width="1.5" fill="none" opacity="0.7"/>'
        '<circle cx="16.5" cy="8.5" r="1.5" fill="#75996a"/>'
        '<circle cx="10" cy="11" r="1" fill="#6f9163"/>'),
    "pr_star": _symbol("pr_star",
        '<path d="M14 4l2.6 6.6 7.1.5-5.5 4.5 1.8 6.9-6-3.9-6 3.9 1.8-6.9-5.5-4.5 7.1-.5z" '
        'fill="#e8b73a" stroke="#7e5b14" stroke-width="1.1"/>'),
    "pr_tower": _symbol("pr_tower",
        f'<circle cx="14" cy="14" r="10" fill="#8a8172" stroke="{_PK}" stroke-width="1.2"/>'
        '<circle cx="14" cy="14" r="8.4" fill="none" stroke="#5f574a" stroke-width="2.4" stroke-dasharray="3.3 2.4"/>'
        '<circle cx="14" cy="14" r="5.2" fill="#6f675a"/>'
        '<circle cx="14" cy="14" r="2" fill="#3a332a"/>'),
    "pr_urn": _symbol("pr_urn",
        '<path d="M11 6h6l-.8 2.6c2.6 1.2 4 3.2 4 6 0 4.2-2.6 7-6.2 7s-6.2-2.8-6.2-7c0-2.8 1.4-4.8 4-6z" '
        'fill="#b0703f" stroke="#5c3517" stroke-width="1.1"/>'
        '<path d="M11.5 8.4h5" stroke="#5c3517" stroke-width="0.8"/>'
        '<path d="M8.6 11.5q-2.4.6-1.6 2.6M19.4 11.5q2.4.6 1.6 2.6" stroke="#5c3517" stroke-width="1" fill="none"/>'
        '<path d="M11 11q-1.4 2.4 0 5.4" stroke="#d09a6a" stroke-width="0.9" fill="none"/>'),
    "pr_bell": _symbol("pr_bell",
        '<path d="M14 5c4 0 6 3 6 7 0 3 .8 4.6 2 5.6H6c1.2-1 2-2.6 2-5.6 0-4 2-7 6-7z" '
        'fill="#c9a13b" stroke="#6e5312" stroke-width="1.1"/>'
        '<circle cx="14" cy="20.4" r="1.7" fill="#6e5312"/>'
        '<circle cx="14" cy="4.6" r="1.3" fill="#6e5312"/>'
        '<path d="M10.5 8.5q-1.3 2-1.3 4.5" stroke="#e8cd7e" stroke-width="0.9" fill="none"/>'),
    "pr_gem": _symbol("pr_gem",
        '<path d="M9 8h10l4 5-9 11-9-11z" fill="#7fc4d8" stroke="#245a70" stroke-width="1.1"/>'
        '<path d="M9 8l5 5 5-5M4.9 13h18.2M14 13v11" stroke="#d9f0f7" stroke-width="0.9" fill="none"/>'),
    "pr_crown": _symbol("pr_crown",
        '<path d="M6 19v-9l4 3.4L14 7l4 6.4 4-3.4v9z" fill="#e8b73a" stroke="#7e5b14" stroke-width="1.1"/>'
        '<rect x="6" y="19" width="16" height="3" fill="#d3a127" stroke="#7e5b14" stroke-width="1"/>'
        '<circle cx="10" cy="20.5" r="0.9" fill="#a33434"/>'
        '<circle cx="14" cy="20.5" r="0.9" fill="#3d6a9e"/>'
        '<circle cx="18" cy="20.5" r="0.9" fill="#a33434"/>'),
    "pr_brazier": _symbol("pr_brazier",
        f'<circle cx="14" cy="14" r="9" fill="#5a4a38" stroke="{_PK}" stroke-width="1.2"/>'
        '<circle cx="14" cy="14" r="6.4" fill="#33291d"/>'
        '<circle cx="14" cy="14" r="4.6" fill="#e2762d"/>'
        '<circle cx="13.2" cy="13.4" r="2.8" fill="#f2a93b"/>'
        '<circle cx="12.8" cy="13" r="1.4" fill="#f8d778"/>'),
    "pr_rack": _symbol("pr_rack",
        '<path d="M7 6v16M21 6v16" stroke="#6e4b26" stroke-width="2"/>'
        '<path d="M6 9.5h16" stroke="#8a6032" stroke-width="2.2"/>'
        '<path d="M11 8.5v13" stroke="#8f8574" stroke-width="1.4"/>'
        '<path d="M11 5.6l1.6 3.2h-3.2z" fill="#9aa0a6" stroke="#4c5257" stroke-width="0.7"/>'
        '<path d="M17 8.5v13" stroke="#8f8574" stroke-width="1.4"/>'
        '<path d="M17 9c3 .4 3.6 3 2.6 4.6L17 12.4z" fill="#9aa0a6" stroke="#4c5257" stroke-width="0.7"/>'),
    "pr_bed": _symbol("pr_bed",
        f'<rect x="7" y="4" width="14" height="20" rx="1.5" fill="#7a5a38" stroke="{_PK}" stroke-width="1.1"/>'
        '<rect x="8.4" y="5.4" width="11.2" height="17.2" rx="1" fill="#cbb894"/>'
        '<rect x="9.6" y="6.4" width="8.8" height="4.2" rx="1.6" fill="#efe6d0" stroke="#b3a78a" stroke-width="0.8"/>'
        '<path d="M8.4 12.5h11.2v8.1a1 1 0 0 1-1 1h-9.2a1 1 0 0 1-1-1z" fill="#96473a"/>'
        '<path d="M8.4 14.6h11.2" stroke="#7e392e" stroke-width="0.9"/>'),
    "pr_crate": _symbol("pr_crate",
        f'<rect x="6" y="6" width="16" height="16" fill="#a5814f" stroke="{_PK}" stroke-width="1.2"/>'
        '<rect x="8.2" y="8.2" width="11.6" height="11.6" fill="none" stroke="#7e5f36" stroke-width="1"/>'
        '<path d="M8.2 8.2l11.6 11.6M19.8 8.2L8.2 19.8" stroke="#7e5f36" stroke-width="1"/>'),
    "pr_horse": _symbol("pr_horse",
        f'<ellipse cx="14" cy="16" rx="4.4" ry="7.6" fill="#7a5a3a" stroke="{_PK}" stroke-width="1.1"/>'
        f'<ellipse cx="14" cy="6.4" rx="2.4" ry="3.4" fill="#6b4d30" stroke="{_PK}" stroke-width="1"/>'
        f'<path d="M12.8 3.8l.5-1.4M15.2 3.8l-.5-1.4" stroke="{_PK}" stroke-width="0.9"/>'
        '<path d="M14 9.5v3" stroke="#4f3a24" stroke-width="1.2"/>'
        f'<rect x="11.4" y="12.8" width="5.2" height="4.6" rx="1.2" fill="#8a3d2e" stroke="{_PK}" stroke-width="0.8"/>'
        '<path d="M14 17.8v5" stroke="#4f3a24" stroke-width="1.2"/>'
        '<path d="M14 23.5q.4 2.4-1 3.2" stroke="#4f3a24" stroke-width="1.2" fill="none"/>'),
    "pr_web": _symbol("pr_web",
        '<g stroke="#cfc8b6" stroke-width="0.9" fill="none" opacity="0.9">'
        '<path d="M4 4L24 6M4 4l18 10M4 4l10 18M4 4l2 20"/>'
        '<path d="M12 4a8 8 0 0 1-8 8M17 4a13 13 0 0 1-13 13M22 4A18 18 0 0 1 4 22"/>'
        '</g>'),
    "pr_ice": _symbol("pr_ice",
        '<g stroke="#8fc3d6" stroke-width="1.3" stroke-linecap="round" fill="none">'
        '<path d="M14 4v20M5.3 9l17.4 10M22.7 9L5.3 19"/>'
        '<path d="M11.6 6.4L14 8.8l2.4-2.4M16.4 21.6L14 19.2l-2.4 2.4"/>'
        '</g>'),
    "pr_bolt": _symbol("pr_bolt",
        '<path d="M16.5 3L8 15.5h4.5L11 25l9-13.5h-4.8z" fill="#f2c744" stroke="#8a6a10" stroke-width="1.1"/>'),
    "pr_portal": _symbol("pr_portal",
        '<circle cx="14" cy="14" r="9.6" fill="#79aec7" opacity="0.35"/>'
        '<path d="M14 4.4A9.6 9.6 0 1 1 4.4 14 7.4 7.4 0 1 0 11.8 6.6 5.2 5.2 0 1 1 6.6 11.8" '
        'fill="none" stroke="#2e6a8a" stroke-width="1.8" stroke-linecap="round"/>'),
    "pr_down": _symbol("pr_down",
        f'<path d="M14 6v11" stroke="{_PK}" stroke-width="2.4" stroke-linecap="round" opacity="0.6"/>'
        f'<path d="M8.5 13.5L14 21l5.5-7.5" fill="none" stroke="{_PK}" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>'),
    "pr_temple": _symbol("pr_temple",
        f'<rect x="5" y="6" width="18" height="16" fill="#b3a689" stroke="{_PK}" stroke-width="1.2"/>'
        '<rect x="9" y="10" width="10" height="8" fill="#9c8f74" stroke="#6f6350" stroke-width="0.8"/>'
        '<g fill="#6f6350">'
        '<circle cx="7.4" cy="8" r="1"/><circle cx="11.8" cy="8" r="1"/>'
        '<circle cx="16.2" cy="8" r="1"/><circle cx="20.6" cy="8" r="1"/>'
        '<circle cx="7.4" cy="20" r="1"/><circle cx="11.8" cy="20" r="1"/>'
        '<circle cx="16.2" cy="20" r="1"/><circle cx="20.6" cy="20" r="1"/>'
        '<circle cx="7.4" cy="14" r="1"/><circle cx="20.6" cy="14" r="1"/>'
        '</g>'),
    "pr_volcano": _symbol("pr_volcano",
        f'<circle cx="14" cy="14" r="9.5" fill="#6b5344" stroke="{_PK}" stroke-width="1.2"/>'
        '<circle cx="14" cy="14" r="5" fill="#3a2a20"/>'
        '<circle cx="14" cy="14" r="3.2" fill="#d9542f"/>'
        '<circle cx="13.2" cy="13.2" r="1.5" fill="#f2a93b"/>'
        '<path d="M14 4.5v3M5 10l2.5 1.5M23 10l-2.5 1.5M6 20l2.6-1M22 20l-2.6-1" '
        'stroke="#8a6a52" stroke-width="1"/>'),
    "pr_statue": _symbol("pr_statue",
        f'<path d="M14 4l10 10-10 10L4 14z" fill="#8d8577" stroke="{_PK}" stroke-width="1.1"/>'
        '<circle cx="14" cy="14" r="5.6" fill="#a99f8d" stroke="#6f675c" stroke-width="0.8"/>'
        '<circle cx="14" cy="12.6" r="2" fill="#6f675c"/>'
        '<path d="M10.8 16.8q3.2-2.4 6.4 0" stroke="#6f675c" stroke-width="1.6" fill="none"/>'),
    "pr_bridge": _symbol("pr_bridge",
        f'<rect x="3" y="9" width="22" height="10" fill="#8a6a42" stroke="{_PK}" stroke-width="1.2"/>'
        '<path d="M7 9v10M11 9v10M15 9v10M19 9v10M23 9v10" stroke="#6e4b26" stroke-width="1"/>'
        '<path d="M3 9h22M3 19h22" stroke="#4f3a24" stroke-width="1.8"/>'),
    "pr_target": _symbol("pr_target",
        f'<circle cx="14" cy="14" r="9" fill="#ded5c0" stroke="{_PK}" stroke-width="1.1"/>'
        '<circle cx="14" cy="14" r="6" fill="#c0392b"/>'
        '<circle cx="14" cy="14" r="3.6" fill="#ded5c0"/>'
        '<circle cx="14" cy="14" r="1.6" fill="#c0392b"/>'),
    "pr_mural": _symbol("pr_mural",
        f'<rect x="5" y="7" width="18" height="14" fill="#c9a13b" stroke="{_PK}" stroke-width="1.1"/>'
        '<rect x="7.2" y="9.2" width="13.6" height="9.6" fill="#ded5c0"/>'
        '<path d="M8.5 16.5l3-3.5 2.5 2.5 3-4 3.5 5" stroke="#8a7350" stroke-width="1" fill="none"/>'
        '<circle cx="17.5" cy="11.5" r="1.2" fill="#d3a127"/>'),
    "pr_sparkle": _symbol("pr_sparkle",
        '<g fill="#e8c85a" stroke="#7e5b14" stroke-width="0.7">'
        '<path d="M11 5l1.5 4.5L17 11l-4.5 1.5L11 17l-1.5-4.5L5 11l4.5-1.5z"/>'
        '<path d="M20 4.5l.9 2.6 2.6.9-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9z"/>'
        '<path d="M18 15l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/>'
        '</g>'),
    "pr_swords": _symbol("pr_swords",
        f'<path d="M7 5.8L21.4 20.2M21 5.8L6.6 20.2" stroke="{_PK}" stroke-width="3.8" stroke-linecap="round"/>'
        '<path d="M7 5.8L21.4 20.2M21 5.8L6.6 20.2" stroke="#b9bfc4" stroke-width="2.2" stroke-linecap="round"/>'
        '<path d="M6.2 10.4l4.2-4.2M17.6 6.2l4.2 4.2" stroke="#6e4b26" stroke-width="2"/>'
        '<circle cx="6.4" cy="5.2" r="1.4" fill="#6e4b26"/>'
        '<circle cx="21.6" cy="5.2" r="1.4" fill="#6e4b26"/>'),
    "pr_coffin": _symbol("pr_coffin",
        f'<path d="M10.5 4h7l3.5 6-2.5 14h-9L7 10z" fill="#7a5a38" stroke="{_PK}" stroke-width="1.1"/>'
        '<path d="M7.6 10.6h12.8" stroke="#4f3a24" stroke-width="0.9"/>'
        '<path d="M14 12.5v8M11.5 15.5h5" stroke="#4f3a24" stroke-width="1.1"/>'),
    "pr_barrel": _symbol("pr_barrel",
        f'<circle cx="14" cy="14" r="8.6" fill="#8a6a42" stroke="{_PK}" stroke-width="1.2"/>'
        '<circle cx="14" cy="14" r="5.6" fill="none" stroke="#6e4b26" stroke-width="1"/>'
        '<circle cx="14" cy="14" r="2" fill="#6e4b26"/>'
        '<path d="M14 5.4v17.2M5.4 14h17.2" stroke="#4f3a24" stroke-width="1" opacity="0.55"/>'),
    "pr_stairs": _symbol("pr_stairs",
        '<g stroke="#6f6552" stroke-width="0.6">'
        '<rect x="6" y="4.5" width="16" height="3.4" fill="#cbbfa4"/>'
        '<rect x="6" y="8.4" width="16" height="3.4" fill="#b8ab8f"/>'
        '<rect x="6" y="12.3" width="16" height="3.4" fill="#a4977c"/>'
        '<rect x="6" y="16.2" width="16" height="3.4" fill="#8f836a"/>'
        '<rect x="6" y="20.1" width="16" height="3.4" fill="#7a6f59"/>'
        '</g>'),
    "pr_bones": _symbol("pr_bones",
        f'<path d="M8.5 8.5L19.5 19.5M19.5 8.5L8.5 19.5" stroke="{_PK}" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M8.5 8.5L19.5 19.5M19.5 8.5L8.5 19.5" stroke="#e8e2d2" stroke-width="2.4" stroke-linecap="round"/>'
        '<g fill="#e8e2d2" stroke="#2f2415" stroke-width="0.6">'
        '<circle cx="7.2" cy="9.4" r="1.5"/><circle cx="9.4" cy="7.2" r="1.5"/>'
        '<circle cx="20.8" cy="18.6" r="1.5"/><circle cx="18.6" cy="20.8" r="1.5"/>'
        '<circle cx="18.6" cy="7.2" r="1.5"/><circle cx="20.8" cy="9.4" r="1.5"/>'
        '<circle cx="9.4" cy="20.8" r="1.5"/><circle cx="7.2" cy="18.6" r="1.5"/>'
        '</g>'),
    "pr_mushrooms": _symbol("pr_mushrooms",
        '<rect x="9.2" y="13" width="2.6" height="7" rx="1.2" fill="#d9cfae" stroke="#8f8368" stroke-width="0.7"/>'
        f'<path d="M4.5 13.5q6-9 12 0z" fill="#b3543f" stroke="{_PK}" stroke-width="1"/>'
        '<circle cx="8" cy="10.8" r="0.9" fill="#e8dfc8"/>'
        '<circle cx="12" cy="10" r="0.8" fill="#e8dfc8"/>'
        '<circle cx="10.2" cy="12.4" r="0.7" fill="#e8dfc8"/>'
        '<rect x="18.4" y="16" width="2" height="4.8" rx="1" fill="#d9cfae" stroke="#8f8368" stroke-width="0.6"/>'
        f'<path d="M15.5 16.5q4-6 8 0z" fill="#c07a4a" stroke="{_PK}" stroke-width="0.9"/>'),
    "pr_candles": _symbol("pr_candles",
        '<ellipse cx="14" cy="21.5" rx="8" ry="2.4" fill="#d9cfae" stroke="#b3a78a" stroke-width="0.6"/>'
        '<g fill="#e8e2d2" stroke="#b3a78a" stroke-width="0.6">'
        '<rect x="8" y="12" width="2.6" height="8.5" rx="1"/>'
        '<rect x="12.8" y="9.5" width="2.6" height="11" rx="1"/>'
        '<rect x="17.6" y="13" width="2.6" height="7.5" rx="1"/>'
        '</g>'
        '<g fill="#f2a93b">'
        '<ellipse cx="9.3" cy="10.6" rx="1" ry="1.6"/>'
        '<ellipse cx="14.1" cy="8.1" rx="1" ry="1.6"/>'
        '<ellipse cx="18.9" cy="11.6" rx="1" ry="1.6"/>'
        '</g>'
        '<circle cx="14.1" cy="8.4" r="0.5" fill="#f8d778"/>'),
    "pr_bush": _symbol("pr_bush",
        '<g stroke="#7d9c5e" stroke-width="1.2" fill="none" stroke-linecap="round">'
        '<path d="M8 21q-1-5 0-9M10 21q0-6 2-9M12.5 21q1-5 3-8M17 21q0-5-1-8M19.5 21q1-4 2.5-7"/>'
        '</g>'
        '<g fill="#c9b45a">'
        '<ellipse cx="8" cy="11.5" rx="1" ry="1.8"/>'
        '<ellipse cx="12.3" cy="11.6" rx="1" ry="1.8"/>'
        '<ellipse cx="15.8" cy="12.8" rx="0.9" ry="1.6"/>'
        '<ellipse cx="22" cy="13.8" rx="0.9" ry="1.6"/>'
        '</g>'),
    "pr_tent": _symbol("pr_tent",
        '<path d="M6 7l8-2 8 2v14l-8 2-8-2z" fill="#a8965f"/>'
        '<path d="M14 5l8 2v14l-8 2z" fill="#8a7a50"/>'
        '<path d="M14 5v18" stroke="#6f6144" stroke-width="1.4"/>'
        f'<path d="M6 7l8-2 8 2v14l-8 2-8-2z" fill="none" stroke="{_PK}" stroke-width="1.1"/>'
        '<path d="M6 7L3.5 4.5M22 7l2.5-2.5M6 21l-2.5 2.5M22 21l2.5 2.5" stroke="#6f6144" stroke-width="0.8"/>'),
    "pr_crystal": _symbol("pr_crystal",
        '<ellipse cx="14" cy="21.5" rx="6.5" ry="2" fill="#6f5a94" opacity="0.6"/>'
        '<path d="M11 21L8 10l4-4 2 5z" fill="#9d7fd0" stroke="#4a3670" stroke-width="1"/>'
        '<path d="M15 21l-1-9 4-5 3 7z" fill="#b79ae0" stroke="#4a3670" stroke-width="1"/>'
        '<path d="M12 6.5l1.5 4M18 7l-1.5 4.5" stroke="#e2d4f4" stroke-width="0.8"/>'),
    "pr_table": _symbol("pr_table",
        f'<rect x="11.5" y="4.5" width="5" height="3" rx="1" fill="#6e4b26" stroke="{_PK}" stroke-width="0.8"/>'
        f'<rect x="11.5" y="20.5" width="5" height="3" rx="1" fill="#6e4b26" stroke="{_PK}" stroke-width="0.8"/>'
        f'<rect x="8" y="8.5" width="12" height="11" rx="1" fill="#8a6a42" stroke="{_PK}" stroke-width="1.1"/>'
        '<path d="M10 11h8M10 14h8M10 17h8" stroke="#6e4b26" stroke-width="0.7"/>'),
    "pr_lowwall": _symbol("pr_lowwall",
        f'<rect x="4" y="10" width="20" height="8" fill="#9c7a5a" stroke="{_PK}" stroke-width="1.2"/>'
        '<path d="M4 14h20M9 10v4M15 10v4M21 10v4M6 14v4M12 14v4M18 14v4" '
        'stroke="#6e4b3a" stroke-width="0.8"/>'),
}

# deterministic per-cell shape variants (breaks repetition in fields of the
# same prop: tree lines, rubble fields)
VARIANTS: dict[str, list[str]] = {
    "pr_tree": ["pr_tree", "pr_tree_b"],
    "pr_rocks": ["pr_rocks", "pr_rocks_b"],
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


# ---------------------------------------------------------------------------
# Map annotations (compass, movement routes, numbered callouts, area zones)
#
# Optional `@`-directives placed inside the fenced block, after the grid.
# They are ignored by the grid parser (they never match ROW_RE) and let a
# map declare orientation, patrol movements, numbered references and zones —
# rendered as an overlay + an "INDICAZIONI" legend. Coordinates use the same
# A1 labels as the ruler (column letters + printed row number), e.g. "M6".
#
#   @north <deg|N|NE|E|SE|S|SW|W|NW>   rotate the compass ("up" = this dir)
#   @path  <label> ; <c1 c2 c3 ...[ loop]> ; [#rrggbb]
#   @mark  <n> ; <coord> ; <text>
#   @zone  <c1-c2> ; <text>            (c1 top-left, c2 bottom-right)
# ---------------------------------------------------------------------------
_COORD_RE = re.compile(r"^([A-Za-z]+)(\d{1,3})$")
_DIR_DEG = {"N": 0, "NE": 45, "E": 90, "SE": 135,
            "S": 180, "SW": 225, "W": 270, "NW": 315}


def col_index(label: str) -> int:
    x = 0
    for ch in label:
        if not ch.isalpha():
            break
        x = x * 26 + (ord(ch.upper()) - ord("A") + 1)
    return x - 1


def coord_to_cell(token: str):
    """'M6' -> (col_index, printed_row_number) or None."""
    m = _COORD_RE.match(token.strip())
    if not m:
        return None
    return col_index(m.group(1)), int(m.group(2))


def parse_annotations(raw_lines: list[str]) -> dict:
    ann = {"north": 0, "paths": [], "marks": [], "zones": []}
    for line in raw_lines:
        s = line.strip()
        if not s.startswith("@"):
            continue
        kind, _, rest = s[1:].partition(" ")
        kind = kind.lower()
        parts = [p.strip() for p in rest.split(";")]
        if kind == "north":
            v = rest.strip().upper()
            if v in _DIR_DEG:
                ann["north"] = _DIR_DEG[v]
            else:
                try:
                    ann["north"] = float(v) % 360
                except ValueError:
                    pass
        elif kind == "path" and len(parts) >= 2:
            coords = [coord_to_cell(t) for t in parts[1].split() if t.lower() != "loop"]
            loop = "loop" in parts[1].lower().split()
            coords = [c for c in coords if c]
            if len(coords) >= 2:
                color = parts[2] if len(parts) >= 3 and parts[2].startswith("#") else "#c81d25"
                ann["paths"].append({"label": parts[0], "coords": coords,
                                     "loop": loop, "color": color})
        elif kind == "mark" and len(parts) >= 3:
            c = coord_to_cell(parts[1])
            if c:
                ann["marks"].append({"n": parts[0], "coord": c, "text": parts[2]})
        elif kind == "zone" and len(parts) >= 2:
            ends = parts[0].split("-")
            if len(ends) == 2:
                a, b = coord_to_cell(ends[0]), coord_to_cell(ends[1])
                if a and b:
                    ann["zones"].append({"a": a, "b": b, "text": parts[1]})
    return ann


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
    annotations: list[str] = []
    for line in block_lines:
        s = line.strip()
        if s.startswith("@"):
            annotations.append(s)
            continue
        if not banner and s and not set(s) <= {"═", "─", "="} and not ROW_RE.match(line) \
                and 8 < len(s) < 120 \
                and not s.startswith(("COLONNE", "RIGHE", "-", "NOTA", "SCALA", "LEGENDA",
                                      "TOTALE", "DIMENSIONI", "TUTTO", "POSIZIONI", "@")) \
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
    return {"rows": rows, "filled": filled, "banner": banner, "annotations": annotations}


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;")


def _n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


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


def _legend_key(e: str) -> tuple:
    """Group the legend elegantly: terrains, then units, then objects,
    then local symbols — alphabetical inside each group."""
    spec = SYMBOLS.get(e)
    if spec is None:
        return (3, "", e)
    rank = {"fill": 0, "unit": 1}.get(spec["mode"], 2)
    return (rank, spec["it"], e)


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


def _trace_loops(cells: set[tuple[int, int]]) -> list[list[tuple[float, float]]]:
    """Trace the boundary of a set of (row, col) cells into closed loops of
    grid-corner points (x, y). Outer loops and holes are both returned; the
    even-odd fill rule sorts them out. Deterministic."""
    edges: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def add(a: tuple[int, int], b: tuple[int, int]) -> None:
        edges.setdefault(a, []).append(b)

    for (r, c) in sorted(cells):
        if (r - 1, c) not in cells:
            add((c, r), (c + 1, r))
        if (r, c + 1) not in cells:
            add((c + 1, r), (c + 1, r + 1))
        if (r + 1, c) not in cells:
            add((c + 1, r + 1), (c, r + 1))
        if (r, c - 1) not in cells:
            add((c, r + 1), (c, r))

    loops: list[list[tuple[float, float]]] = []
    while edges:
        start = min(edges)
        pt = start
        prev_dir: tuple[int, int] | None = None
        loop: list[tuple[float, float]] = [pt]
        while True:
            outs = edges[pt]
            if len(outs) == 1 or prev_dir is None:
                nxt = sorted(outs)[0]
            else:
                # at pinch points prefer the sharpest right turn, keeping
                # touching loops separate (y grows downward: right = cw)
                px, py = prev_dir

                def turn(q: tuple[int, int]) -> float:
                    dx, dy = q[0] - pt[0], q[1] - pt[1]
                    return math.atan2(px * dy - py * dx, px * dx + py * dy)

                nxt = max(outs, key=lambda q: (turn(q), q))
            outs.remove(nxt)
            if not outs:
                del edges[pt]
            prev_dir = (nxt[0] - pt[0], nxt[1] - pt[1])
            pt = nxt
            if pt == start:
                break
            loop.append(pt)
        if len(loop) >= 4:
            loops.append(loop)
    return loops


def _dedup_collinear(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        if (p1[0] - p0[0]) * (p2[1] - p1[1]) != (p1[1] - p0[1]) * (p2[0] - p1[0]):
            out.append(p1)
    return out if len(out) >= 3 else pts


def _smooth_loop(pts: list[tuple[float, float]], cut: float = 0.35,
                 iters: int = 2) -> list[tuple[float, float]]:
    """Corner cutting with an absolute cut distance (grid units): straight
    runs stay straight, corners get a uniform hand-drawn rounding."""
    for _ in range(iters):
        out: list[tuple[float, float]] = []
        n = len(pts)
        for i in range(n):
            p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
            for q in (p0, p2):
                dx, dy = q[0] - p1[0], q[1] - p1[1]
                dist = math.hypot(dx, dy)
                if dist < 1e-9:
                    continue
                d = min(cut, dist * 0.45)
                out.append((p1[0] + dx / dist * d, p1[1] + dy / dist * d))
        pts = out
        cut *= 0.55
    return pts


def _region_path(cells: set[tuple[int, int]], ox: int, oy: int) -> str:
    """Organic path (with holes) for a set of cells, in px coordinates."""
    parts: list[str] = []
    for loop in _trace_loops(cells):
        sm = _smooth_loop(_dedup_collinear(loop))
        coords = [f"{_n(ox + x * CELL)} {_n(oy + y * CELL)}" for x, y in sm]
        parts.append("M" + "L".join(coords) + "Z")
    return "".join(parts)


def _compass_svg(cx: float, cy: float, r: float, north_deg: float) -> str:
    """Compass rose; the needle/'N' point to 'north_deg' measured clockwise
    from screen-up (0 = North is up)."""
    g = [f'<g transform="translate({_n(cx)},{_n(cy)}) rotate({_n(north_deg)})">']
    g.append(f'<circle r="{_n(r + 5)}" fill="{PAPER}" fill-opacity="0.82" '
             f'stroke="{INK}" stroke-width="1"/>')
    d = r * 0.16
    g.append(f'<path d="M0 {_n(-r)}L{_n(d)} {_n(-d)}L{_n(r)} 0L{_n(d)} {_n(d)}'
             f'L0 {_n(r)}L{_n(-d)} {_n(d)}L{_n(-r)} 0L{_n(-d)} {_n(-d)}Z" '
             f'fill="{INK_SOFT}" opacity="0.5"/>')
    g.append(f'<path d="M0 {_n(-r)}L{_n(r * 0.24)} 0L0 {_n(-r * 0.22)}'
             f'L{_n(-r * 0.24)} 0Z" fill="{INK}"/>')
    g.append(f'<text x="0" y="{_n(-r - 6)}" font-size="11" font-weight="bold" '
             f'text-anchor="middle" fill="{INK}">N</text>')
    g.append("</g>")
    return "".join(g)


def _arrowhead(x1: float, y1: float, x2: float, y2: float, color: str, size: float = 7.0) -> str:
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    p1 = (x2 + size * math.cos(a1), y2 + size * math.sin(a1))
    p2 = (x2 + size * math.cos(a2), y2 + size * math.sin(a2))
    return (f'<path d="M{_n(x2)} {_n(y2)}L{_n(p1[0])} {_n(p1[1])}'
            f'L{_n(p2[0])} {_n(p2[1])}Z" fill="{color}"/>')


def render_svg(grid: dict, source_name: str) -> str:
    rows = grid["rows"]
    row_nums = sorted(rows)
    n_rows = row_nums[-1] - row_nums[0] + 1
    n_cols = max(len(c) for c in rows.values())
    grid_w, grid_h = n_cols * CELL, n_rows * CELL
    width = max(MARGIN * 2 + grid_w, MIN_WIDTH)
    used = sorted({e for cells in rows.values() for e in cells})

    ann = parse_annotations(grid.get("annotations", []) or [])
    ann_items = len(ann["paths"]) + len(ann["marks"]) + len(ann["zones"])
    ann_h = (22 + 15 * ann_items) if ann_items else 0

    header_h = 58
    ox = MARGIN
    oy = header_h + 22
    sb_y = oy + grid_h + 24
    ann_y = sb_y + 30
    ly = sb_y + 32 + (ann_h + 12 if ann_items else 0)
    two_cols = width >= 940 and len(used) > 10
    legend_rows = math.ceil(len(used) / 2) if two_cols else len(used)
    legend_h = 18 + LEGEND_ROW_H * legend_rows
    height = ly + legend_h + 26

    base = _resolve_bases(rows, n_cols)
    used_pats = sorted({p for r in base.values() for p in r if p})
    unit_colors = sorted({SYMBOLS[e]["fill"] for e in used
                          if e in SYMBOLS and SYMBOLS[e]["mode"] == "unit"})
    prop_set: set[str] = set()
    for e in used:
        spec = SYMBOLS.get(e)
        if spec and spec.get("prop"):
            prop_set.update(VARIANTS.get(spec["prop"], [spec["prop"]]))
    used_props = sorted(prop_set)

    # organic terrain regions (computed early: defs need the heavy outline)
    pat_cells: dict[str, set[tuple[int, int]]] = {}
    for r, rn in enumerate(row_nums):
        for c in range(n_cols):
            p = base[rn][c]
            if p is not None:
                pat_cells.setdefault(p, set()).add((r, c))
    order = [p for p in Z_ORDER if p in pat_cells] + \
            sorted(p for p in pat_cells if p not in Z_ORDER)
    paths = {p: _region_path(pat_cells[p], ox, oy) for p in order}
    heavy_present = [p for p in order if p in HEAVY_PATS]
    heavy_union = set()
    for p in heavy_present:
        heavy_union |= pat_cells[p]
    heavy_union_d = _region_path(heavy_union, ox, oy) if heavy_union else ""

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )

    # --- defs: filters, vignette, terrain patterns, props, token gradients --
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
        '<filter id="aoblur" x="-30%" y="-30%" width="160%" height="160%">'
        '<feGaussianBlur stdDeviation="3.2"/></filter>'
    )
    defs.append(
        '<filter id="mottle" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" '
        'seed="4" stitchTiles="stitch"/>'
        '<feColorMatrix type="matrix" values="0 0 0 0 0.24 0 0 0 0 0.18 '
        '0 0 0 0 0.10 0 0 0 0.5 0"/></filter>'
    )
    defs.append(
        '<radialGradient id="vign" cx="0.5" cy="0.45" r="0.75">'
        '<stop offset="0.62" stop-color="#3b2e1e" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#3b2e1e" stop-opacity="0.16"/>'
        '</radialGradient>'
    )
    defs.append(
        f'<clipPath id="clipgrid"><rect x="{ox}" y="{oy}" width="{grid_w}" '
        f'height="{grid_h}"/></clipPath>'
    )
    if heavy_union_d:
        defs.append(
            f'<clipPath id="clipheavy"><path d="{heavy_union_d}" '
            f'clip-rule="evenodd"/></clipPath>'
        )
    for p in used_pats:
        defs.append(PATTERNS[p])
    for p in used_props:
        defs.append(PROPS[p])
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

    # --- organic terrain regions ----------------------------------------------
    out.append(f'<g clip-path="url(#clipgrid)">')
    # light terrains (slight self-stroke overlap hides seams between regions)
    for p in order:
        if p in HEAVY_PATS:
            continue
        out.append(
            f'<path d="{paths[p]}" fill="url(#{p})" fill-rule="evenodd" '
            f'stroke="url(#{p})" stroke-width="2.4" stroke-linejoin="round"/>'
        )
    if heavy_union_d:
        # ambient occlusion: floor darkens beside walls (inner half is
        # covered by the wall fill drawn right after)
        out.append(
            f'<path d="{heavy_union_d}" fill="none" stroke="#241c10" '
            f'stroke-width="9" opacity="0.22" filter="url(#aoblur)"/>'
        )
        # cast shadow, then the solids themselves
        out.append(
            f'<path d="{heavy_union_d}" fill="#241c10" fill-rule="evenodd" '
            f'opacity="0.28" filter="url(#softblur)" transform="translate(2.6,3.4)"/>'
        )
        for p in heavy_present:
            out.append(
                f'<path d="{paths[p]}" fill="url(#{p})" fill-rule="evenodd" '
                f'stroke="url(#{p})" stroke-width="2.4" stroke-linejoin="round"/>'
            )
    # low-frequency tonal mottling breaks texture repetition
    out.append(
        f'<rect x="{ox}" y="{oy}" width="{grid_w}" height="{grid_h}" '
        f'filter="url(#mottle)" opacity="0.35"/>'
    )
    # inked hand-drawn boundaries
    for p in order:
        if p in HEAVY_PATS:
            continue
        out.append(
            f'<path d="{paths[p]}" fill="none" stroke="{INK_SOFT}" stroke-width="0.9" '
            f'opacity="0.5" stroke-linejoin="round" filter="url(#rough)"/>'
        )
    for p in heavy_present:
        out.append(
            f'<path d="{paths[p]}" fill="none" stroke="#241c10" stroke-width="1.8" '
            f'opacity="0.9" stroke-linejoin="round" filter="url(#rough)"/>'
        )
    out.append("</g>")

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
    out.append(f'<path d="{grid_d}" stroke="#2e2313" stroke-width="0.6" opacity="0.3" fill="none"/>')
    out.append(f'<path d="{grid5_d}" stroke="#2e2313" stroke-width="1.4" opacity="0.48" fill="none"/>')
    if heavy_union_d:
        # light grid pass over dark solids, so squares stay countable there
        out.append(
            f'<g clip-path="url(#clipheavy)">'
            f'<path d="{grid_d}" stroke="{PAPER}" stroke-width="0.6" opacity="0.16" fill="none"/>'
            f'<path d="{grid5_d}" stroke="{PAPER}" stroke-width="1.4" opacity="0.26" fill="none"/>'
            f'</g>'
        )

    # --- illustrated props and unit tokens --------------------------------------
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
            elif spec and spec.get("prop"):
                variants = VARIANTS.get(spec["prop"], [spec["prop"]])
                prop = variants[(r * 7 + c * 13) % len(variants)]
                out.append(
                    f'<ellipse cx="{cx + 1}" cy="{cy + 3}" rx="9" ry="4.5" '
                    f'fill="#241c10" opacity="0.2"/>'
                )
                out.append(
                    f'<use href="#{prop}" x="{x}" y="{y}" '
                    f'width="{CELL}" height="{CELL}"/>'
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

    # --- annotation overlay: zones, movement routes, numbered callouts ----------
    row_min = row_nums[0]

    def _cc(cell):  # (col, printed_row) -> pixel center
        cx0, rn = cell
        return ox + cx0 * CELL + CELL / 2, oy + (rn - row_min) * CELL + CELL / 2

    # zones first (under routes/marks)
    for z in ann["zones"]:
        (ax, ay0), (bx, by0) = z["a"], z["b"]
        x0 = ox + min(ax, bx) * CELL
        y0 = oy + (min(ay0, by0) - row_min) * CELL
        w = (abs(bx - ax) + 1) * CELL
        h = (abs(by0 - ay0) + 1) * CELL
        out.append(
            f'<rect x="{_n(x0)}" y="{_n(y0)}" width="{_n(w)}" height="{_n(h)}" '
            f'rx="4" fill="none" stroke="#2c2313" stroke-width="1.6" '
            f'stroke-dasharray="5 4" opacity="0.75"/>'
        )
        out.append(
            f'<text x="{_n(x0 + 4)}" y="{_n(y0 + 13)}" font-size="10.5" '
            f'font-weight="bold" fill="#2c2313">{_esc(z["text"])}</text>'
        )

    # movement routes (dashed, arrowhead, start dot, label near start)
    for p in ann["paths"]:
        pts = [_cc(c) for c in p["coords"]]
        if p["loop"]:
            pts = pts + [pts[0]]
        d = "M" + "L".join(f"{_n(x)} {_n(y)}" for x, y in pts)
        out.append(
            f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="3.6" '
            f'opacity="0.55" stroke-linejoin="round" stroke-linecap="round"/>'
        )
        out.append(
            f'<path d="{d}" fill="none" stroke="{p["color"]}" stroke-width="2" '
            f'stroke-dasharray="7 4" stroke-linejoin="round" stroke-linecap="round"/>'
        )
        (sx, sy) = pts[0]
        out.append(f'<circle cx="{_n(sx)}" cy="{_n(sy)}" r="3.4" fill="{p["color"]}" '
                   f'stroke="#ffffff" stroke-width="1"/>')
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        out.append(_arrowhead(x1, y1, x2, y2, p["color"]))

    # numbered callouts (badge at cell corner)
    for m in ann["marks"]:
        cx, cy = _cc(m["coord"])
        bx, by = cx + CELL * 0.30, cy - CELL * 0.30
        out.append(f'<circle cx="{_n(bx)}" cy="{_n(by)}" r="7" fill="#1a140a" '
                   f'stroke="#ffffff" stroke-width="1.1"/>')
        out.append(f'<text x="{_n(bx)}" y="{_n(by + 3.4)}" font-size="9.5" '
                   f'font-weight="bold" text-anchor="middle" fill="#fff">'
                   f'{_esc(str(m["n"]))}</text>')

    # compass rose (always), top-right inside the map plate
    out.append(_compass_svg(ox + grid_w - 22, oy + 22, 15, ann["north"]))

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

    # --- indications legend (movements / callouts / zones) ----------------------
    if ann_items:
        out.append(
            f'<text x="{ox}" y="{ann_y}" font-size="12" font-weight="bold" '
            f'fill="{INK}" letter-spacing="2">INDICAZIONI</text>'
        )
        out.append(
            f'<path d="M{ox + 96} {ann_y - 4}H{width - MARGIN}" stroke="{INK_SOFT}" '
            f'stroke-width="0.7" opacity="0.7"/>'
        )
        ey = ann_y + 17
        for m in ann["marks"]:
            cx0, rn = m["coord"]
            coord_lbl = f"{col_label(cx0)}{rn}"
            out.append(f'<circle cx="{ox + 8}" cy="{ey - 4}" r="7" fill="#1a140a" '
                       f'stroke="#fff" stroke-width="1"/>')
            out.append(f'<text x="{ox + 8}" y="{ey - 0.6}" font-size="9.5" '
                       f'font-weight="bold" text-anchor="middle" fill="#fff">'
                       f'{_esc(str(m["n"]))}</text>')
            out.append(f'<text x="{ox + 22}" y="{ey}" font-size="11" fill="{INK}">'
                       f'{coord_lbl} — {_esc(m["text"])}</text>')
            ey += 15
        for p in ann["paths"]:
            out.append(f'<line x1="{ox}" y1="{ey - 4}" x2="{ox + 16}" y2="{ey - 4}" '
                       f'stroke="{p["color"]}" stroke-width="2" stroke-dasharray="6 3"/>')
            out.append(_arrowhead(ox + 10, ey - 4, ox + 18, ey - 4, p["color"], 5))
            route = " → ".join(f"{col_label(c[0])}{c[1]}" for c in p["coords"])
            if p["loop"]:
                route += " → (loop)"
            out.append(f'<text x="{ox + 24}" y="{ey}" font-size="11" fill="{INK}">'
                       f'{_esc(p["label"])}: {route}</text>')
            ey += 15
        for z in ann["zones"]:
            out.append(f'<rect x="{ox}" y="{ey - 11}" width="15" height="12" rx="2" '
                       f'fill="none" stroke="#2c2313" stroke-width="1.4" '
                       f'stroke-dasharray="4 3"/>')
            za = f"{col_label(z['a'][0])}{z['a'][1]}"
            zb = f"{col_label(z['b'][0])}{z['b'][1]}"
            out.append(f'<text x="{ox + 22}" y="{ey}" font-size="11" fill="{INK}">'
                       f'{za}–{zb} — {_esc(z["text"])}</text>')
            ey += 15

    # --- legend -------------------------------------------------------------------
    out.append(
        f'<text x="{ox}" y="{ly}" font-size="12" font-weight="bold" fill="{INK}" '
        f'letter-spacing="2">LEGENDA</text>'
    )
    out.append(
        f'<path d="M{ox + 74} {ly - 4}H{width - MARGIN}" stroke="{INK_SOFT}" '
        f'stroke-width="0.7" opacity="0.7"/>'
    )
    col_w = (width - 2 * MARGIN) / 2 if two_cols else width - 2 * MARGIN
    for i, emoji in enumerate(sorted(used, key=_legend_key)):
        spec = SYMBOLS.get(emoji)
        label = spec["it"] if spec and spec["it"] else "(simbolo locale — vedi legenda del file sorgente)"
        col = i // legend_rows if two_cols else 0
        row_i = i % legend_rows if two_cols else i
        lx = ox + col * col_w
        y = ly + 18 + row_i * LEGEND_ROW_H
        if spec and spec["mode"] == "unit":
            out.append(
                f'<circle cx="{lx + 9}" cy="{y - 4}" r="7.5" '
                f'fill="url(#{_grad_id(spec["fill"])})" stroke="#241c10" stroke-width="1.2"/>'
            )
        elif spec and spec["mode"] == "fill":
            out.append(
                f'<rect x="{lx}" y="{y - 12}" width="19" height="15" fill="url(#{spec["pat"]})" '
                f'stroke="{INK_SOFT}" stroke-width="0.7"/>'
            )
        elif spec and spec.get("prop"):
            out.append(
                f'<use href="#{spec["prop"]}" x="{lx}" y="{y - 13}" width="18" height="18"/>'
            )
        else:
            out.append(f'<text x="{lx}" y="{y}" font-size="14">{emoji}</text>')
        out.append(f'<text x="{lx + 27}" y="{y}" font-size="11" fill="{INK}">{emoji} — {label}</text>')

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
