<!-- Report d'audit — Fase 0. Documento di analisi (plans/CHANGELOG registra la modifica strutturale). -->
# Audit degli script — RumblingStone

**Data:** 2026-07-24 · **Ambito:** `scripts/` (automazione DM) + `Script/` (convertitori) ·
**Metodo:** lettura diretta del sorgente, smoke della CLI, confronto doc↔codice.
**Metro:** best practice di senior developer / system engineer / architect —
CLI POSIX-friendly, I/O deterministico, exit code semantici, contratti
machine-readable, gate CI verificabili.

Companion: [`SCORECARD.md`](SCORECARD.md) (punteggi per script).

---

## 1. Verdetto sintetico

Il toolkit è **maturo**. Punti di forza già presenti, non da inventare:

- **Separazione delle responsabilità**: libreria condivisa `dmcore/`, orchestratore
  unico `dm.py` (ADR-0002), i singoli tool restano usabili in isolamento.
- **Sicurezza sul canone**: nessuno script sovrascrive `state.md`/`sessions/` senza
  conferma; scritture confinate alle regioni `<!-- auto: -->` (ADR-0007).
- **Determinismo**: `--seed` dove serve, output ordinato, render SVG byte-identico
  (requisito di `validate_maps.py` in CI).
- **Contratti già formalizzati** per le mappe: 2 JSON Schema in `scripts/schemas/`.
- **Gate CI reali**: `validate_*`, round-trip mappe, unit test `dmcore`, `dm.py doctor`.
- **Disciplina d'output**: header "auto-generated" sui file prodotti.

L'audit **non** propone di riscrivere ciò che funziona. Interviene solo dove la
**uniformità** e la **consumabilità da altri tool** sono carenti.

---

## 2. Findings azionabili

Severità: 🔴 alta · 🟠 media · 🟢 bassa/info.

### 🔴 F1 — Due script ignorano `argv`: `--help` esegue con side-effect

`build_monster_catalog.py` e `dm_dossier.py` non parsano gli argomenti: il `main()`
gira incondizionatamente e **scrive file**.

- `scripts/build_monster_catalog.py`: la CI esegue
  `python scripts/build_monster_catalog.py --help > /dev/null` (ci.yml) — che **non**
  stampa aiuto ma **rigenera `monster_catalog.yaml`** (e crea `.custom.yaml`). Effetto
  collaterale mascherato da smoke test.
- `scripts/dm_dossier.py`: qualunque argomento (incluso `--help`) produce e scrive
  `campaign/DM-DOSSIER.hb.md`.

**Impatto:** viola il principio "un flag informativo non ha effetti collaterali";
rende gli script non introspezionabili da un orchestratore.
**Azione (Fase 2):** aggiungere `argparse` con `--help` privo di effetti; per
`build_monster_catalog` aggiungere `--check`/`--stdout` (dry-run) e `-o`. Aggiornare
la riga CI perché lo smoke resti significativo.

### 🟠 F2 — Parsing manuale invece di argparse

- `scripts/validate_bestiario.py`: gestisce `--help`/`-h`/`--rules` con `in sys.argv`.
- `scripts/validate_modules.py`: gestisce `--verbose` con `in sys.argv`, nessun `--help`.

**Impatto:** niente usage/errore-uso standard, flag ignoti accettati in silenzio.
**Azione (Fase 2):** convertire ad `argparse` mantenendo identici flag/semantica.

### 🟠 F3 — Il claim "stdlib-only" non è vero per la pipeline skill

`README-automation.md` dichiara *"Python 3 stdlib only (no pip install required)"*, ma:

- `scripts/compress_skills.py`: `import yaml` **senza fallback** → crash se manca pyyaml.
- `scripts/validate_skills.py`: richiede pyyaml (gestito con `except ImportError` → exit 2).
- `scripts/measure_tokens.py`, `compress_skills.py`: `tiktoken` **opzionale** (fallback).
- La CI infatti fa `pip install pyyaml`.

Nota: gli script "core" (`suggest_encounter` ecc.) leggono YAML con un **parser custom
stdlib** (`load_yaml`), quindi per loro il claim regge.

**Impatto:** aspettativa d'ambiente sbagliata per chi integra i tool.
**Azione:** (a) il **manifest** dichiara `stdlib_only` e `external_deps` per-tool (verità
puntuale); (b) correggere il claim globale nella doc; (c) opzionale: dare a
`compress_skills` lo stesso fallback di `validate_skills`.

### 🟠 F4 — Nessun contratto machine-readable ("usabile da altri tool")

La "tool map" esiste solo come **prosa markdown** scritta a mano in
`README-automation.md`. Un orchestratore/altro tool/agente non ha uno schema
formale di input/output/exit-code/determinismo da consumare, e la prosa **deriva**
dal codice nel tempo.

**Azione (Fase 1+5):** `scripts/schemas/tool_manifest.schema.json` + un manifest per
tool + `docs/tools/registry.json` (+ vista MCP) + generatore `tools_manifest.py` che
**rigenera** le tabelle umane e **valida in CI** l'allineamento manifest↔`--help`.

### 🟠 F5 — Documentazione frammentata + collisione di naming

Doc sparsa fra `scripts/README.md`, `README-automation.md`,
`README-import-ultraclear.md`, README di sotto-cartelle, `plans/`, `plans/adr/`,
file `PIANO-*` in root. Nessun **indice maestro categorizzato**. Inoltre `scripts/`
(minuscolo) e `Script/` (maiuscolo) collidono su filesystem case-insensitive
(macOS/Windows) — rischio checkout/merge.

**Azione:** `docs/INDEX.md` categorizzato (Fase 4) + de-collisione `Script/` →
`converters/` con ADR-0011 (Fase 6).

### 🟢 F6 — Convenzione exit-code non codificata

Gli script usano exit code sensati ma eterogenei: alcuni ricchi (`suggest_encounter`
0/2/3/4), altri 0/1. Nessuna convenzione scritta a livello repo.
**Azione (Fase 7):** codificare `0=ok · 1=errore-dominio · 2=errore-uso · >2=specifici`
nello standard, e documentare `exit_codes` per-tool nel manifest.

### 🟢 F7 — `import_watabou`/`export_map_png` segnalano errori-uso come exit 1

Usano `raise SystemExit("msg")` (→ exit 1) anche per input malformato, dove la
convenzione vorrebbe exit 2 (errore d'uso). Cosmetico.
**Azione (Fase 2, best-effort):** allineare alla convenzione senza rompere la CI.

### 🟢 F8 — Determinismo asserito ma non testato con double-run

Il render è byte-identico per contratto, ma non c'è un test che esegua due volte e
confronti. **Azione (Fase 5):** harness `deterministic:true` → doppia esecuzione +
diff byte a byte.

### 🟢 F9 — Dipendenze esterne (binari) non dichiarate uniformemente

`export_map_png.py` richiede **Chromium/Chrome**; i convertitori richiedono
`cwebp`/pandoc; gli env locali richiedono Docker/Distrobox/GPU. Oggi sono citati solo
in prosa. **Azione (Fase 1):** campo `external_bins` nel manifest.

---

## 3. Convertitori `Script/` (uppercase) — §I

Tre sotto-progetti eterogenei (`pdf-to-md-engine/`, `Html_to_markdown/`,
`Image-to-webp/`), con toolchain esterne e path **hardcoded** su `Script/`
(`Image-to-webp/setup.sh`, `conver_webp_new.sh`, README). Sono di qualità inferiore
al toolkit DM (niente `--help` uniforme, niente test) ma **funzionali e isolati**.

**Azione:** rientrano nel manifest come categoria `converters` con
`stability: external-toolchain`; la **de-collisione** (Fase 6, ADR-0011) rinomina la
cartella in `converters/` aggiornando *tutti* i riferimenti (ADR-0002, `.gitignore`,
CI `compileall`, README, skill `rumblingstone-plans`, e i path interni degli script).

---

## 4. Piano di rientro (mappa finding → fase)

| Finding | Fase | Deliverable |
|---|---|---|
| F4, F9 | 1 | `tool_manifest.schema.json`, manifest per-tool, `registry.json`, `tools_manifest.py` |
| F1, F2, F7 | 2 | argparse su 4 script; exit-code allineati |
| F3 (c) | 2/3 | fallback pyyaml opzionale; `--json` sui validatori |
| F5 (doc) | 4 | `docs/INDEX.md` + federazione |
| F4, F6, F8 | 5 | gate CI `tools_manifest --check`, determinismo, shellcheck |
| F5 (rename) | 6 | de-collisione `Script/`→`converters/` + ADR-0011 |
| F6 (regola) | 7 | ADR-0012 + `TOOL-AUTHORING-STANDARD.md` + gate conformità |

---

## 5. Cosa NON tocchiamo (per prudenza da senior)

- I **renderer/parser** delle mappe (`render_map_svg`, `compile_map_json`,
  `import_ultraclear`): logica delicata e byte-deterministica. Solo manifest+doc.
- Il **formato dei file canone** e la semantica di `state_apply`/`session_wizard`:
  governati da ADR-0007, con test. Nessun refactor.
- I file in `Old/`: conservati per policy, marcati `deprecated`.
