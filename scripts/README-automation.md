# RumblingStone — DM automation scripts

Zero-burden helpers that read what the DM already writes (session logs,
state.md, Armate atlas) and produce prep material. **Nothing overwrites
canon** — scripts either generate new files or print suggestions for
manual review. Respects `AGENTS.md`: we never invent statblocks; we only
index/compose what exists (or mark `[INFERRED]`).

> **Disambiguazione**: questa cartella `scripts/` (minuscolo) è
> l'automazione DM. La cartella `Script/` (maiuscolo) contiene invece i
> convertitori di contenuto (pdf→md, html→md, immagini→webp) — vedi
> ADR-0002 in `plans/adr/`.

## One entrypoint: `dm.py`

Everything below is reachable from a single CLI mapped to the Playbook
phases (it *orchestrates* the scripts — they all remain usable directly):

```bash
python3 scripts/dm.py prep --el 13 --env forest   # encounter + map + loot
python3 scripts/dm.py post                        # XP ledger + state.md diff proposal
python3 scripts/dm.py recap --hype                # player recap + Homebrewery V3 version
python3 scripts/dm.py handout --tipo profezia --da <file> --sezione "HANDOUT 1"
python3 scripts/dm.py maps validate               # or: maps render <file.md>
python3 scripts/dm.py hype setup && dm.py hype start   # Homebrewery locale (localhost:8000)
python3 scripts/dm.py doctor                      # environment diagnosis
```

## Tool map

| Script | Purpose | Input | Output |
|---|---|---|---|
| `build_monster_catalog.py` | Index every statblock in the repo | `Bestiario/` (mostri/villain/png/pregen-pcgen), `*STATBLOCCHI*.md`, arc folders | `scripts/monster_catalog.yaml` (+ empty `monster_catalog.custom.yaml` for DM additions) |
| `validate_bestiario.py` | CI gate for the `Bestiario/` library: standard structure, `-crN` kebab naming, required headers, filename↔header CR match, catalog in sync. With `--rules` (non-blocking warning in CI): PF1e CR benchmark on hp/AC, `[INFERRED]` flag policy, mandatory `Boost log:` | `Bestiario/{mostri,villain,png}/**/*.md` + `monster_catalog.yaml` | exit 0/1 + violation list (runs in `.github/workflows/ci.yml`) |
| `suggest_encounter.py` | 3–5 encounter proposals for a target EL | catalog + filters (env, faction, role, size) | markdown tables with CR math + source file links |
| `suggest_map.py` | Pick a 5ft-square tactical grid (ASCII) | `scripts/map_templates/*.yaml` (11 included) | ready-to-print grid + legend + tactical notes |
| `render_map_svg.py` | Render the arcs' emoji-grid maps to print-quality SVG in the **"pergamena" illustrated style** (procedural terrain textures, inked boundaries, cast shadows, VTT-style tokens, coordinates, scale bar, legend — all deterministic, no external assets) | any `*MAPPE*`/`*Ultra-Clear*` markdown with emoji grids | `rendered/*.svg` next to the source (generated artifacts — the markdown stays the master) |
| `import_watabou.py` | Convert a Watabou One Page Dungeon JSON export into an emoji-grid map master (template-conformant, ready for `render_map_svg.py`) | JSON exported from https://watabou.github.io/dungeon.html | a new `*.md` map master with grid + companion skeleton |
| `update_xp.py` | Cumulative XP ledger per PC | `campaign/sessions/*.md` `## XP awarded` | `campaign/pg/xp-ledger.md` (auto) |
| `state_sync.py` | Propose edits to `campaign/state.md` after a session | `## World events triggered` in session logs | markdown diff report (DM applies manually) |
| `session_recap.py` | Spoiler-safe Italian recap for players (R.A. Salvatore tone) | last N session logs + state.md §0 public rows | `campaign/recaps/recap-YYYY-MM-DD.md` (+ optional PDF) |
| `hype_homebrew.py` | Wrap the recap (or a handout) in Homebrewery V3 layout | latest recap, or `--handout TIPO --da <canon file>` + `campaign/templates/homebrew/*.hb.md` | `.hb.md` generated artifacts to paste on homebrewery.naturalcrit.com |
| `suggest_loot.py` | Treasure proposals per EL/faction (SRD-only) | `loot_tables.yaml` + `magic_items_srd.yaml` | markdown loot tables |
| `validate_maps.py` | CI gate: emoji grids ↔ rendered SVG consistency | `*MAPPE*` markdown + `rendered/*.svg` | exit 0/1 (runs in `.github/workflows/ci.yml`) |
| `dm.py` | **Single entrypoint** — orchestrates all of the above by Playbook phase | subcommand + passthrough flags | whatever the underlying script produces |

## Typical DM workflow

```bash
python3 scripts/dm.py prep --el 13 --env forest --factions red-hand  # before the session
python3 scripts/dm.py post --session 2026-05-01_session-42.md        # after the session
python3 scripts/dm.py recap --hype                                    # 1-2 days before next
```

## Extending

- **Add a custom monster**: append to `scripts/monster_catalog.custom.yaml`
  (same schema: `id / name / cr / faction / role / environment / source_file`).
  `suggest_encounter.py` merges it automatically.
- **Add a map**: drop a new YAML in `scripts/map_templates/` (copy an
  existing one). `suggest_map.py` picks it up on next run.
- **New trigger for state_sync**: edit the `TRIGGERS` regex list at the top
  of `scripts/state_sync.py`.

## Mappe di qualità professionale (stile "pergamena")

`render_map_svg.py` produce battle map illustrate in stile handout
professionale (benchmark: le mappe ufficiali di *Red Hand of Doom* e gli
export di Dungeon Scrawl/DungeonDraft). Tutta la grafica è **procedurale**
(pattern e filtri SVG): niente asset esterni, niente vincoli di licenza,
output byte-deterministico (requisito di `validate_maps.py` in CI).

La pipeline completa (vedi `plans/RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md`
per il razionale e le alternative valutate):

1. **Mappe esistenti**: la griglia emoji resta il MASTER; ogni modifica al
   markdown si rigenera con `python3 scripts/render_map_svg.py <file.md>`.
2. **Nuovi dungeon**: generare il layout su
   https://watabou.github.io/dungeon.html → Export JSON →
   `python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md`
   → adattare la griglia e compilare i companion → renderizzare.
3. **Mappe regionali** (Dalelands/Cannath Vale): Azgaar Fantasy Map
   Generator (https://azgaar.github.io/Fantasy-Map-Generator/, MIT) —
   committare il file `.map` come master + l'export SVG/PNG.
4. **Città** (Rethmar, Palio): Medieval Fantasy City Generator
   (https://watabou.github.io/city-generator/) — committare l'export SVG
   annotando il **seed** nell'URL per la rigenerazione.

## Design rules

- Python 3 stdlib only (no `pip install` required).
- Every script is idempotent and safe to re-run.
- No script writes to `campaign/state.md` or `campaign/sessions/*.md`
  automatically — those remain DM-owned canon.
- All generated files carry an "Auto-generated — do not edit by hand" header.
