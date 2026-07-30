# PIANO — Audit degli script: qualità, contratti machine-readable e standard

> **Ambito**: infrastruttura (`scripts/`, `converters/`, `docs/`, CI).
> **Origine**: richiesta DM 2026-07-24 — audit dettagliato degli script con
> best practice senior, contratti I/O deterministici usabili da altri tool,
> indice documentale categorizzato, razionalizzazione della struttura, e una
> **regola vincolante** per il software futuro verificabile in CI.
> **Decisioni**: manifest per-tool + registry · nuova `docs/` con INDEX ·
> de-collisione `Script/`→`converters/` · normalizzazione + refactor mirato.

## Stato: 🟢 eseguito (2026-07-24)

## Lotti

- [x] **F0 — Audit read-only**: `docs/audit/AUDIT-REPORT.md` + `SCORECARD.md`
      (rubrica 12-assi su ~40 tool). Findings F1–F9.
- [x] **F1 — Manifest & registry**: `scripts/schemas/tool_manifest.schema.json`,
      `scripts/tools.manifest.json` (fonte di verità, 37 tool),
      `scripts/tools_manifest.py` (validatore/generatore stdlib-only),
      `docs/tools/{registry.json,README.md,mcp-tools.json}` generati.
- [x] **F2 — Normalizzazione CLI**: argparse + `--help` senza side-effect su
      `build_monster_catalog`, `dm_dossier`, `validate_bestiario`,
      `validate_modules` (risolve F1: `--help` non esegue più lo script).
- [x] **F3 — `--json` opt-in** su `validate_maps`, `validate_skills`,
      `validate_bestiario`, `validate_modules`, `check_plans_discipline`
      (default testuale invariato).
- [x] **F4 — `docs/INDEX.md`** categorizzato + federazione doc + link dal
      README di root.
- [x] **F5 — Gate CI + test per-regola**: step `tools_manifest --check`
      (bloccante) + shellcheck (non bloccante); `test_tools_manifest.py`,
      `test_determinism.py`.
- [x] **F6 — De-collisione** `Script/`→`converters/` ([ADR-0011](adr/ADR-0011-de-collisione-scripts-converters.md)).
- [x] **F7 — Standard ingegneria** ([ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md))
      + [`docs/guides/TOOL-AUTHORING-STANDARD.md`](../docs/guides/TOOL-AUTHORING-STANDARD.md),
      applicato dal gate CI.

## Gate / follow-up (al tavolo / opzionali)

- shellcheck: oggi **non bloccante** (non verificabile nell'ambiente di sviluppo);
  promuovere a bloccante dopo una passata pulita su `converters/Image-to-webp`.
- opzionale: portare i convertitori (`converters/`) allo standard pieno
  (argparse/test) — oggi marcati `external-toolchain` nel manifest.
- opzionale: fallback pyyaml in `compress_skills.py` (oggi `external_deps`).

## Invarianti rispettate

- Nessuna modifica al comportamento di default degli script (solo aggiunte
  opt-in e fix a rischio-zero); renderer/parser mappe **non toccati**.
- 70/70 test verdi; `tools_manifest --check` pulito (0 warning).
