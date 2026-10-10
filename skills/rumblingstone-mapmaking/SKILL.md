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
   Local extra symbols must be declared in the file; they render with the
   Noto Emoji SVG from `scripts/emoji-noto/` (ADR-0085), so they look the same
   on every machine — run `python3 scripts/build_emoji_noto.py` after adding
   one. A concept becomes universal only when it means the same thing in every
   map that uses it.
4. Every map ships with the three companion blocks (Ambiente / Tattiche /
   Evoluzione) per `campaign/templates/mappa-tattica-template.md`.
5. Art is procedural/in-house by default. A third-party file enters a map
   only under ADR-0085: a licence that allows redistribution without imposing
   itself (CC0, CC BY, CC BY-NC, Apache-2.0, OFL, MIT — never CC BY-SA or GPL),
   with the licence and a `CREDITS.md` (author, changes) in its folder. No
   tracing of third-party art. The map text uses the volumes' fonts, embedded
   (`scripts/fonts/mappe/`, `build_font_mappe.py`).
   **Richer maps go through CC0 only** (DM, 2026-10-09, D13-D15 of
   RESA-ASSET): the texture theme fills the terrains with Poly Haven CC0
   textures (`build_texture_cc0.py`, `scripts/texture-cc0/`), committed in
   `rendered-texture/` next to the parchment and checked by `validate_maps`.
   In that theme the props become webp tiles rendered top-down in Blender from
   CC0 3D models (Poly Haven; Quaternius Fantasy Props MegaKit **Standard**
   only), one lock of camera, sun and footprint for the whole set
   (`build_oggetti_cc0.py`, `scripts/oggetti-cc0/`, D17-D22); the models stay
   on the DM's machine. Fire, effects, doors, windows, grates, bars, markers,
   creatures and stairs stay glyphs (`render.tessera_cc0: false` in `legend.yaml`); where no tile exists the
   glyph stays. The parchment keeps every glyph. **A substitution enters only
   if measured and preferred** (ADR-0086, D23): `misura_resa.py` (contour
   contrast WCAG 1.4.11, SSIM to the nearest symbol, ΔE2000 to the house
   palette) must not get worse, and the DM must choose it on the choice page
   (`misura_resa.py coppie [--anche DIR]` for objects, `terreni-scelta` for
   terrain textures, then `voti`): every box is labelled, identical options are
   dropped and said, «nessuna va bene» throws the image away for that symbol and
   «non vedo differenze» keeps the cheaper one; `misura_resa.py --check` in CI
   blocks any rendering measure that drops more than 5%, and `misura_resa.py
   tara` retunes halo and per-terrain veil of the texture theme. 2-Minute Tabletop is an optional extra for
   the DM's own table: the packs live outside git (`asset-esterni/`,
   `dm.py asset installa <zip> --categoria base|premium`), and a **premium**
   pack (Plus, Patron Packs, tokens, even if paid for) has no licence beyond
   the table — `dm.py asset controlla` fails on it (GUIDA-MAPPE §5.1-§5.2).
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
9. **A map is done when it plays, not when it renders** (DM, 2026-10-08,
   ADR-0082). Every new or redrawn tactical map passes
   `scripts/collaudo_mappe.py` with zero E-class findings (or a written
   `@deroga` with its reason), declares `@north`, links every staircase or
   trapdoor to its twin with `@collega`, and then goes to the **cold map
   checker** role. Doors, grates and windows sit in a wall; secret doors never
   appear on the players' version (`@vista giocatori`). A closure takes the
   axis of its wall from its four neighbours (ADR-0083): the renderer turns the
   glyph and the UVTT export turns the portal from that same answer, so you
   never draw the direction, you only write `@verso <cell> ; NS|EO` where the
   checker says the neighbours are ambiguous. The checker needs `tcod`
   (`pip install -r requirements-dev.txt`, ADR-0084). Use the symbol set of
   `legend.yaml` (doors by type, bars, stairs up/down, cave floor, shallow
   water, sewer, debris, furniture) before inventing a local symbol.
   Procedure and rubric: `references/collaudo-mappe.md`.

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
| **Collaudo**: does the map play? the checker tool, the `@` directives, the cold map-checker role | `references/collaudo-mappe.md` |
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
python3 scripts/collaudo_mappe.py <file.md>        # does it play? (ADR-0082)
python3 scripts/dm.py asset texture && python3 scripts/dm.py maps texture   # CC0 texture theme, all maps
.venv/bin/python scripts/build_oggetti_cc0.py --prova   # CC0 3D props for the texture theme (Blender or bpy), GUIDA-MAPPE §5.1.1
python3 scripts/misura_resa.py --check               # the rendering did not get worse (ADR-0086), GUIDA-MAPPE §5.1.2
python3 scripts/dm.py asset installa <zip> --categoria base   # 2-Minute Tabletop, optional, table only
python3 scripts/dm.py maps citta <scheda>.watabou.json --export svg  # a Watabou city plan from a committed seed (R5)
```
