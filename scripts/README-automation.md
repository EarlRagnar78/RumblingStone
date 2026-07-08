# RumblingStone — DM automation scripts

Zero-burden helpers that read what the DM already writes (session logs,
state.md, Armate atlas) and produce prep material. **Nothing overwrites
canon** — scripts either generate new files or print suggestions for
manual review. Respects `AGENTS.md`: we never invent statblocks; we only
index/compose what exists (or mark `[INFERRED]`).

## Tool map

| Script | Purpose | Input | Output |
|---|---|---|---|
| `build_monster_catalog.py` | Index every statblock in the repo | `Bestiario/` (mostri/villain/png/pregen-pcgen), `*STATBLOCCHI*.md`, arc folders | `scripts/monster_catalog.yaml` (+ empty `monster_catalog.custom.yaml` for DM additions) |
| `validate_bestiario.py` | CI gate for the `Bestiario/` library: standard structure, `-crN` kebab naming, required headers, filename↔header CR match, catalog in sync | `Bestiario/{mostri,villain,png}/**/*.md` + `monster_catalog.yaml` | exit 0/1 + violation list (runs in `.github/workflows/ci.yml`) |
| `suggest_encounter.py` | 3–5 encounter proposals for a target EL | catalog + filters (env, faction, role, size) | markdown tables with CR math + source file links |
| `suggest_map.py` | Pick a 5ft-square tactical grid (ASCII) | `scripts/map_templates/*.yaml` (11 included) | ready-to-print grid + legend + tactical notes |
| `render_map_svg.py` | Render the arcs' emoji-grid maps to print-quality SVG (uniform palette, coordinates, scale bar, legend) | any `*MAPPE*`/`*Ultra-Clear*` markdown with emoji grids | `rendered/*.svg` next to the source (generated artifacts — the markdown stays the master) |
| `update_xp.py` | Cumulative XP ledger per PC | `campaign/sessions/*.md` `## XP awarded` | `campaign/pg/xp-ledger.md` (auto) |
| `state_sync.py` | Propose edits to `campaign/state.md` after a session | `## World events triggered` in session logs | markdown diff report (DM applies manually) |

## Typical DM workflow

```bash
# 1. Build/refresh the monster index (once; re-run when you add stat files)
python3 scripts/build_monster_catalog.py

# 2. Plan next session's combat
python3 scripts/suggest_encounter.py --el 13 --env forest --faction red-hand
python3 scripts/suggest_map.py --env forest

# 3. After the session — auto-update XP ledger
python3 scripts/update_xp.py

# 4. Review proposed state.md edits from triggers in the session log
python3 scripts/state_sync.py --session 2026-05-01_session-42.md
```

## Extending

- **Add a custom monster**: append to `scripts/monster_catalog.custom.yaml`
  (same schema: `id / name / cr / faction / role / environment / source_file`).
  `suggest_encounter.py` merges it automatically.
- **Add a map**: drop a new YAML in `scripts/map_templates/` (copy an
  existing one). `suggest_map.py` picks it up on next run.
- **New trigger for state_sync**: edit the `TRIGGERS` regex list at the top
  of `scripts/state_sync.py`.

## Design rules

- Python 3 stdlib only (no `pip install` required).
- Every script is idempotent and safe to re-run.
- No script writes to `campaign/state.md` or `campaign/sessions/*.md`
  automatically — those remain DM-owned canon.
- All generated files carry an "Auto-generated — do not edit by hand" header.
