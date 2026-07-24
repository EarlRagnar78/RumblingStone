<!-- Auto-generated companion doc — audit Fase 0. Aggiornare a mano solo la colonna "Azione". -->
# Scorecard qualità script — RumblingStone

> Audit del **2026-07-24** su `scripts/` (automazione DM) e `Script/` (convertitori).
> Rubrica a 12 assi, punteggio `0` = assente · `1` = parziale · `2` = pieno.
> Metodo: lettura diretta del sorgente + smoke della CLI. Nessun punteggio "a sensazione".

## Legenda assi

| Asse | Significato |
|---|---|
| **CLI** | `argparse` + `--help` reale, flag coerenti |
| **Doc** | module docstring con Scopo/Uso/Input/Output |
| **Exit** | exit code documentati e semantici (0/1/2…) |
| **Det** | determinismo (seed, output ordinato, no wallclock nell'output) |
| **Safe** | idempotenza, `--check`/`--dry-run`, non sovrascrive canone |
| **Err** | errori su stderr, niente traceback nudi |
| **Val** | valida l'input e rigetta il malformato |
| **Out** | contratto d'output stabile + header generato |
| **Fx** | side-effect (git/net/FS) dichiarati |
| **Test** | coperto da `tests/` o smoke CI |
| **Dep** | dipendenze reali dichiarate (stdlib-only verificato) |
| **Man** | manifest machine-readable presente |

`Man` è a `0` ovunque prima della Fase 1 (il manifest non esisteva): non lo ripeto per riga.

## A. Session Prep

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `suggest_encounter.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Esemplare. YAML via parser custom stdlib. Manca test unit dedicato → smoke CI ok |
| `suggest_map.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Esemplare |
| `suggest_loot.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Esemplare |

## B. Maps Pipeline

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `render_map_svg.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Deterministico byte-identico (requisito CI). Aggiungere test double-run |
| `compile_map_json.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Valida contro JSON Schema + geometria. Esemplare |
| `export_uvtt.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Round-trip CI |
| `import_watabou.py` | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 0 | 2 | Errori via `SystemExit("msg")` (exit 1 generico, non 2 per uso) |
| `export_map_png.py` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 0 | 1 | Richiede **Chromium** esterno → dichiarare in manifest (`external_bins`) |
| `validate_maps.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Gate CI. Aggiungere `--json` (Fase 3) |
| `import_ultraclear.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Contratto I/O già documentato a parte. Esemplare |

## C. Post-Session Canon

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `update_xp.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | `--check` dry-run. Ok |
| `state_sync.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Solo proposta, mai scrive canone. Ok |
| `state_apply.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Scrive canone SOLO in regioni `auto:`, con conferma. Test presente |
| `next_session.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Aggregatore deterministico. Test presente |
| `session_wizard.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Commit automatico dichiarato. Test presente |
| `campaign_branch.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Guardia branch. Test presente |

## D. Player/DM Materials

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `session_recap.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Taglia sempre le note private DM. Test per-PG presente |
| `hype_homebrew.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Non duplica il filtro spoiler. Ok |
| `dm_dossier.py` | **0** | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 0 | 2 | **Ignora `argv`**: `--help` **esegue** e scrive `DM-DOSSIER.hb.md`. → argparse |

## E. Bestiary / Catalog

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `build_monster_catalog.py` | **0** | 2 | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 0 | 2 | **Ignora `argv`**: la CI chiama `--help` e in realtà **rigenera il catalogo** (side-effect). → argparse + `--check` |
| `validate_bestiario.py` | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | `--help`/`--rules` parsati a mano. → argparse. Aggiungere `--json` |

## F. Skill Build Pipeline

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `build-skills.sh` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | 2 | `set -euo pipefail`. shellcheck consigliato |
| `sync-skills.sh` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 0 | 2 | idem |
| `validate_skills.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | Richiede **pyyaml** (exit 2 pulito se assente). Aggiungere `--json` |
| `index_skills.py` | 2 | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 0 | 2 | Ok |
| `compress_skills.py` | 2 | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 0 | **0** | **`import yaml` senza fallback**: rompe il claim stdlib-only. → dichiarare dep o fallback |
| `measure_tokens.py` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 0 | 2 | Ha già `--json` (precedente per Fase 3) |

## G. Orchestration & Governance

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `dm.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | Orchestratore (ADR-0002). 11 sottocomandi + `doctor` |
| `new-campaign-group.sh` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 0 | 2 | Ok |
| `check_plans_discipline.py` | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | Gate ADR-0009. Aggiungere `--json` |
| `install-git-hooks.sh` | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 0 | 2 | Ok |
| `validate_modules.py` | **1** | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | `--verbose` parsato a mano, nessun `--help`. → argparse |
| `dmcore/` (lib) | — | 2 | — | 2 | 2 | 2 | 2 | — | 2 | 2 | 2 | Non è CLI. Coperto da `tests/` |
| `tests/` | — | 1 | — | — | — | — | — | — | — | 2 | 2 | Suite unittest ADR-0007 |

## H. Local Infra (opt-in envs)

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `comfyui-local/*.sh` | 1 | 2 | 2 | — | 2 | 2 | 1 | — | 2 | 0 | 1 | Richiede GPU/Distrobox. `stability: local-only` |
| `homebrew-local/*.sh` | 1 | 2 | 2 | — | 2 | 2 | 1 | — | 2 | 0 | 1 | Richiede Docker/Node. `stability: local-only` |

## I. Content Converters (`Script/` — de-collisione in Fase 6)

| Script | CLI | Doc | Exit | Det | Safe | Err | Val | Out | Fx | Test | Dep | Note / Azione |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `pdf-to-md-engine/` | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 0 | 0 | Toolchain esterna (pandoc/…). Audit dettagliato in AUDIT-REPORT §I |
| `Html_to_markdown/` | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 0 | 0 | idem |
| `Image-to-webp/` | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 0 | 1 | `cwebp` esterno. Path hardcoded `Script/` → aggiornare in Fase 6 |

## Deprecati (conservati per policy "non cancellare")

| Script | Stato |
|---|---|
| `Old/deploy-skills.sh` | ⚠️ Superato — `stability: deprecated` nel manifest |
| `Old/sync-skills.sh` | ⚠️ Superato — `stability: deprecated` nel manifest |

## Sintesi

- **28 script Python** + **12 shell** + libreria `dmcore/` + `tests/`.
- **Qualità di base alta**: la stragrande maggioranza è a punteggio pieno su determinismo, sicurezza sul canone, contratto d'output ed exit code.
- **Gap concreti** (→ vedi `AUDIT-REPORT.md` per il dettaglio azionabile):
  1. **2 script ignorano `argv`** (`build_monster_catalog`, `dm_dossier`): `--help` esegue con side-effect. **Priorità alta.**
  2. **2 script** con parsing manuale (`validate_bestiario`, `validate_modules`): niente argparse/`--help` standard.
  3. **Claim "stdlib-only" impreciso**: `compress_skills`/`validate_skills` usano `pyyaml`.
  4. **Nessun contratto machine-readable** → manifest+registry (Fase 1) e gate anti-drift (Fase 5).
  5. **Doc frammentata + collisione `scripts/`↔`Script/`** → `docs/INDEX` (Fase 4) + de-collisione (Fase 6).
