---
name: rumblingstone-mapmaking
description: >
  RumblingStone tactical map pipeline: create, edit, and render battle maps at
  AP quality (Red Hand of Doom / Paizo benchmark). Use for "mappa", "battle
  map", "griglia tattica", "battlemap", "render SVG", "nuova mappa", "import
  watabou", "hero map", "mappa regionale", "mappa città", "mappa esercito",
  "assedio", "accampamento", "coordinate", "JSON mappa", "contratto JSON",
  "compile_map_json", "export UVTT", "uvtt", "dd2vtt", "Foundry", "Roll20",
  "muri e luci", "mappa cinematografica", "handout", "audit mappe", "atlante
  mappe", "mappe definitive", "parity pass mappe", "consolidamento mappe",
  "MAPPE-DEFINITIVO", "posizionamenti canonici", files *MAPPE* or
  *Ultra-Clear*, and render_map_svg, import_watabou, compile_map_json,
  export_uvtt, validate_maps. Covers the 3 map modes, the emoji-grid master,
  the JSON contract, the legend, the parchment renderer, VTT export and the
  optional ComfyUI hero map.
---

# RumblingStone — Mapmaking Pipeline

> 📘 **Guida passo-passo per umani** (quale modalità scegliere, comandi, export
> VTT, troubleshooting): [`docs/guides/GUIDA-MAPPE.md`](../../docs/guides/GUIDA-MAPPE.md).
> Questa skill è la reference operativa per gli agenti.

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
   `scripts/legend.yaml` is the source of truth (ADR-0048): renderer, UVTT
   export, importer and the Blender chain all derive from it.
   Local extra symbols render as raw emoji and must be declared in the file.
4. Every map ships with the three companion blocks (Ambiente / Tattiche /
   Evoluzione) per `campaign/templates/mappa-tattica-template.md`.
5. All art is procedural/in-house (no external assets, no tracing of
   third-party art — style conventions yes, files never).
6. **Fidelity contract** (piano RENDER-MAPPE-FEDELTÀ, 2026-07-23): side
   annotations on a grid row start after **≥3 spaces** (or a detached `│`
   preceded by ≥2 spaces, or box-drawing) — the parser never reads them as
   cells, even if they contain emoji. The header line `N col × M righe · S m`
   is a **validated declaration**: mismatches warn (`--strict` fails) and the
   declared scale drives the SVG subtitle/scale-bar. A `<!-- render: none -->`
   comment right before the fence marks schematic/diagram maps that must NOT
   be rendered. The in-fence `LEGENDA · 🧲 descrizione · …` line is parsed
   automatically: local symbols get their real description in the SVG legend
   (universal SYMBOLS keep their canonical text).
7. **A map inside a booklet either fits a column or gets an A4 page**
   (DM, 2026-09-25). A column holds 48 cells, an A4 one-column page 110
   (an emoji counts 2.5). Put map sections in an appendix between
   `<!-- pagina: una-colonna -->` and `<!-- /pagina -->`; keep every grid
   line, side annotation and `LEGENDA` line within 110 cells so it prints at
   full 9 pt. The typst exporter enforces the column/A4 split on its own
   (`rumblingstone-editoria` §4, point 4), but a 180-cell legend line still
   shrinks the whole map: shorten the annotation, never the grid.
8. **Hero map from a service (Canva AI), until the local ComfyUI pass is
   tested** (DM, 2026-09-25). Canva AI paints **only** the player-facing hero
   map. The prompt is written **from the map's JSON** (the Mode 3 contract, or
   the UVTT export for an emoji master): size ratio, terrain, rooms, doors and
   accesses in words, north up. The tactical truth stays the grid master, its
   JSON, the SVG, `validate_maps` and the UVTT. A hero map that moves a door, a
   room or an access against the SVG is **discarded**, not kept because it
   looks good. **No AI generator draws the grid**: if the table needs one, it
   is laid over from the SVG. Procedure: `references/hero-map-comfyui.md`,
   «Finché ComfyUI non è collaudato».

## Domain → File

## Le 3 modalità di mappa (quale pipeline)

Tutte usano lo stesso formato MASTER (griglia emoji); cambia la *sorgente*:

1. **Tattica standard**: griglia scritta a mano o dungeon importato
   (`import_watabou.py`) → `render_map_svg.py`.
2. **Cinematografica / scenica**: l'LLM fa il *prompt engineer*; immagine
   d'atmosfera con ComfyUI locale (`scripts/comfyui-local/`,
   `references/hero-map-comfyui.md`), banca prompt in `campaign/ai-media-prompts/`.
3. **Tattica con strutture ed eserciti**: l'LLM emette **solo JSON rigido**
   (`scripts/schemas/tactical_map.schema.json`), `compile_map_json.py` valida e
   dipinge la griglia. Un LLM non disegna MAI arte ASCII di mappe.

Dettaglio e "system prompt" per l'LLM: `references/tre-modalita-mappe.md`.

### Le tavole di supporto: quando dall'alto non basta

Le tre modalità sono tutte **zenitali**: si guarda il luogo da sopra. È la vista
giusta per muovere miniature, ed è quella sbagliata per tre domande che al tavolo
arrivano sempre:

| Domanda | Vista che risponde |
|---|---|
| «Cosa vediamo arrivando?» | **veduta** — prospettica, dal punto da cui i PG arrivano davvero (dal mare, dalla strada, dal crinale) |
| «Quanto è alto? Si può scendere di lì?» | **profilo laterale** — sezione con **quote**, e le vie verticali segnate |
| «Quanto ci mettiamo?» | il profilo con i **tempi di percorrenza** annotati sui tratti, non solo le distanze |

**La regola**: una tavola di supporto si aggiunge **quando risponde a una domanda
che la griglia non può**, non per completezza. Tre viste dello stesso cortile sono
tre file da tenere allineati; una veduta di un promontorio che i PG raggiungono in
barca fa risparmiare cinque minuti di descrizione a ogni gruppo.

Si numerano insieme alle altre nella stessa serie, con una lettera: `Tavola I`
(zenitale), `Tavola I-a` (veduta), `Tavola I-b` (profilo). Così restano
riconoscibili come **lo stesso luogo visto in un altro modo**, e non come mappe
diverse.

⚠️ **Non sostituiscono la griglia** e non hanno coordinate tattiche: nessuno ci
muove sopra una miniatura, quindi niente quadretti e niente legenda tattica.
Restano SVG originali come il resto (ADR-0005).
Esemplare: `10-stand-alone/L'abbazia Della Rotta Sicura/` — Tavola I-a «il
promontorio, veduta dal mare» e Tavola I-b «profilo laterale: quote, distanze e
tempi».

## Domain → File

| Task | Reference |
|---|---|
| **Audit/consolidamento mappe di un arco** (atlante definitivo, fonti canoniche, add-on DM, render+verifica) | `references/audit-mappe-workflow.md` |
| Le 3 modalità, contratto JSON, system prompt LLM | `references/tre-modalita-mappe.md` |
| **Migrare un ultra-clear esistente → bozza JSON + report conflitti** (`import_ultraclear.py`) | `references/import-ultraclear.md` |
| Full workflow: new map, edit, render, validate, dungeon import, overland/city | `references/workflow-mappe.md` |
| Universal legend: every terrain/unit/prop symbol with meaning | `references/legenda-universale.md` |
| Direzione artistica handout/splash (convenzioni + confini IP) | `references/stile-illustrazione-handout.md` |
| Optional local "hero map" painterly pass (ComfyUI + ControlNet + MCP), and the Canva AI hero map until ComfyUI is tested | `references/hero-map-comfyui.md` |

## Quick commands

```bash
python3 scripts/render_map_svg.py <file.md>        # render all maps in file
python3 scripts/render_map_svg.py <file.md> --list # list maps found
python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md
python3 scripts/compile_map_json.py spec.json -o <arco>/NUOVA-MAPPA.md  # Mod. 3: JSON → master
python3 scripts/compile_map_json.py spec.json --validate-only           # solo validazione
python3 scripts/import_ultraclear.py ULTRACLEAR.md -o OUT.draft.json --json-report OUT.conflicts.json  # migra un ultra-clear
python3 scripts/export_map_png.py rendered/<mappa>.svg   # hi-res PNG (print / hero input)
python3 scripts/export_uvtt.py <file.md>           # .uvtt/.dd2vtt (Foundry/Roll20: muri+luci)
python3 scripts/validate_maps.py                   # CI gate (run before commit)
```
