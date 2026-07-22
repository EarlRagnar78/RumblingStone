---
name: rumblingstone-mapmaking
description: >
  RumblingStone tactical map pipeline — create, edit, and render the campaign's
  battle maps at professional AP quality (Red Hand of Doom / Paizo benchmark).
  Use for "mappa", "battle map", "griglia tattica", "battlemap", "render SVG",
  "nuova mappa", "import watabou", "hero map", "mappa regionale", "mappa città",
  "mappa esercito", "assedio", "accampamento", "coordinate", "JSON mappa",
  "contratto JSON", "compile_map_json", "export UVTT", "uvtt", "dd2vtt",
  "Foundry", "Roll20", "muri e luci", "mappa cinematografica", "handout",
  or whenever creating/editing files matching *MAPPE*, *Ultra-Clear*, or
  running scripts/render_map_svg.py, scripts/import_watabou.py,
  scripts/compile_map_json.py, scripts/export_uvtt.py, scripts/validate_maps.py.
  Covers the 3 map modes, the emoji-grid master format, the rigid JSON contract,
  the universal legend, the parchment renderer, VTT export, and the optional
  local ComfyUI "hero map" pass.
---

# RumblingStone — Mapmaking Pipeline

Every tactical map of this campaign is an **emoji grid in markdown** (the
MASTER: human-readable, diffable, playable at the table) rendered to a
print-quality **"pergamena" SVG** by `scripts/render_map_svg.py` (organic
terrain regions, ambient occlusion, original vector props, 1,5 m/quadretto
grid, legend, scale bar). SVGs live in `rendered/` next to their master and
are **generated artifacts — never hand-edit them**. CI
(`scripts/validate_maps.py`) enforces byte-identical, deterministic renders.

## Golden rules

1. The markdown grid is the master; regenerate the SVG after EVERY edit:
   `python3 scripts/render_map_svg.py <file.md>`
2. Scale is **1,5 m/quadretto**, declared in the file header.
3. Use ONLY the universal legend symbols (`references/legenda-universale.md`);
   the `SYMBOLS` table in `scripts/render_map_svg.py` is the source of truth.
   Local extra symbols render as raw emoji and must be declared in the file.
4. Every map ships with the three companion blocks (Ambiente / Tattiche /
   Evoluzione) per `campaign/templates/mappa-tattica-template.md`.
5. All art is procedural/in-house (no external assets, no tracing of
   third-party art — style conventions yes, files never).

## Domain → File

## Le 3 modalità di mappa (quale pipeline)

Tutte usano lo stesso formato MASTER (griglia emoji); cambia la *sorgente*:

1. **Tattica standard** — griglia scritta a mano o dungeon importato
   (`import_watabou.py`) → `render_map_svg.py`.
2. **Cinematografica / scenica** — l'LLM fa il *prompt engineer*; immagine
   d'atmosfera con ComfyUI locale (`scripts/comfyui-local/`,
   `references/hero-map-comfyui.md`), banca prompt in `campaign/ai-media-prompts/`.
3. **Tattica con strutture ed eserciti** — l'LLM emette **solo JSON rigido**
   (`scripts/schemas/tactical_map.schema.json`), `compile_map_json.py` valida e
   dipinge la griglia. Un LLM non disegna MAI arte ASCII di mappe.

Dettaglio e "system prompt" per l'LLM: `references/tre-modalita-mappe.md`.

## Domain → File

| Task | Reference |
|---|---|
| Le 3 modalità, contratto JSON, system prompt LLM | `references/tre-modalita-mappe.md` |
| Full workflow: new map, edit, render, validate, dungeon import, overland/city | `references/workflow-mappe.md` |
| Universal legend: every terrain/unit/prop symbol with meaning | `references/legenda-universale.md` |
| Direzione artistica handout/splash (convenzioni + confini IP) | `references/stile-illustrazione-handout.md` |
| Optional local "hero map" painterly pass (ComfyUI + ControlNet + MCP) | `references/hero-map-comfyui.md` |

## Quick commands

```bash
python3 scripts/render_map_svg.py <file.md>        # render all maps in file
python3 scripts/render_map_svg.py <file.md> --list # list maps found
python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md
python3 scripts/compile_map_json.py spec.json -o <arco>/NUOVA-MAPPA.md  # Mod. 3: JSON → master
python3 scripts/compile_map_json.py spec.json --validate-only           # solo validazione
python3 scripts/export_map_png.py rendered/<mappa>.svg   # hi-res PNG (print / hero input)
python3 scripts/export_uvtt.py <file.md>           # .uvtt/.dd2vtt (Foundry/Roll20: muri+luci)
python3 scripts/validate_maps.py                   # CI gate (run before commit)
```
