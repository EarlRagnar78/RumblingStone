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
      + [`docs/reference/TOOL-AUTHORING-STANDARD.md`](../docs/reference/TOOL-AUTHORING-STANDARD.md),
      applicato dal gate CI.

## Gate / follow-up (al tavolo / opzionali)

- 📅 shellcheck: oggi **non bloccante** (non verificabile nell'ambiente di sviluppo);
  promuovere a bloccante dopo una passata pulita su `converters/Image-to-webp`.
  *Condizione*: la passata pulita. 🔀 **Spostata il 2026-11-09 in
  [AMBIENTE A6](PIANO-AMBIENTE-RIPRODUCIBILE.md)**, che ha la stessa voce
  («shellcheck … bloccante in CI»): resta aperta là, non chiusa.
  📅 **2026-11-13, D5 del piano di recupero**: è un lotto del blocco
  piattaforma, [milestone v1.5.0](https://github.com/gsamuele78/RumblingStone/milestone/5)
  («shellcheck bloccante» nella roadmap del motore).
- 📅 opzionale: portare i convertitori (`converters/`) allo standard pieno
  (argparse/test) — oggi marcati `external-toolchain` nel manifest.
  *Condizione*: nessuna scritta; resta aperta al DM in RECUPERO D5.
  📅 **2026-11-13, Jfs sulla card (D5 del piano di recupero): «nel blocco
  piattaforma (v1.5.0)»**, una voce sola «convertitori con i test» nella
  [milestone v1.5.0](https://github.com/gsamuele78/RumblingStone/milestone/5).
  Non è un'attesa: è un lotto con la sua milestone.
- ~~opzionale: fallback pyyaml in `compress_skills.py` (oggi `external_deps`).~~
  ✅ **Chiusa come superata il 2026-11-09** (card del DM, «Chiudi, superato»).
  *Prova*: PyYAML è una dipendenza dichiarata (`requirements.txt:28`,
  `pyyaml>=6.0.3`) e `compress_skills.py` gira solo in fase di build
  (`scripts/build-skills.sh`, chiamato dal job CI e dal rilascio), dove le
  dipendenze sono installate. La misura del 2026-11-08 lo conferma: il ripiego
  darebbe lo stesso risultato (18 skill su 18), ma servirebbe solo a chi salta
  `pip install -r requirements.txt`, e lì falliscono altri 17 script. Misura in
  [`esperimenti/ripiego-pyyaml-2026-11-08/ESITO.md`](esperimenti/ripiego-pyyaml-2026-11-08/ESITO.md).

## Invarianti rispettate

- Nessuna modifica al comportamento di default degli script (solo aggiunte
  opt-in e fix a rischio-zero); renderer/parser mappe **non toccati**.
- 70/70 test verdi; `tools_manifest --check` pulito (0 warning).
