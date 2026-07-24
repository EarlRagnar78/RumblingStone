# Standard di authoring dei tool — RumblingStone

> **Regola vincolante** (ADR-0012): ogni nuovo tool eseguibile del repo
> (`scripts/`, `converters/`) rispetta questo standard, **verificato in CI**.
> Implementazione di riferimento: [`scripts/tools_manifest.py`](../../scripts/tools_manifest.py).

Questo documento è la checklist operativa per chi scrive o modifica uno script.
Ogni regola ha un **come si verifica** automatico: se il comando è rosso, il tool
non è conforme.

---

## 0. TL;DR — checklist per un nuovo tool

```
[ ] shebang + module docstring (Scopo · Uso · Input · Output · Exit)
[ ] argparse con --help; nessun flag informativo con side-effect
[ ] exit code secondo convenzione 0/1/2
[ ] voce in scripts/tools.manifest.json (conforme allo schema)
[ ] determinismo dichiarato; se deterministico → output byte-identico
[ ] non scrive canone senza dichiararlo + conferma
[ ] dipendenze dichiarate (stdlib_only o external_deps/external_bins)
[ ] almeno uno smoke --help in CI; test di comportamento se logica non banale
[ ] (shell) set -euo pipefail + shellcheck pulito
[ ] plans/CHANGELOG.md aggiornato nello stesso commit (ADR-0009)
```

Verifica tutto in un colpo:

```bash
python3 scripts/tools_manifest.py --check      # manifest + copertura + flag
python3 -m compileall -q scripts converters    # niente errori di sintassi
python3 -m unittest discover -s scripts/tests  # test verdi
```

---

## 1. Interfaccia CLI

- **`argparse` obbligatorio** con `description` = docstring e `--help` funzionante.
- Un flag **informativo** (`--help`, `--list`, `--check`, `--validate-only`,
  `--dry-run`) **non deve avere side-effect**: niente scritture, niente commit.
  *(È il difetto storico F1: `--help` che eseguiva lo script.)*
- Flag in `kebab-case` (`--from-encounter`), positional documentati nella docstring.
- I flag dei **subcomandi** stanno nei rispettivi sub-parser.

**Come si verifica**
```bash
python3 scripts/<tool>.py --help          # stampa aiuto, exit 0, non scrive nulla
git status --porcelain                     # invariato dopo --help
```

## 2. Convenzione degli exit code

| Codice | Significato |
|---|---|
| `0` | successo |
| `1` | errore di **dominio** (validazione fallita, risorsa incoerente) |
| `2` | errore d'**uso** (argomenti mancanti/errati, file non trovato) |
| `>2` | codici specifici del tool, **documentati** nel manifest (`exit_codes`) |
| `130` | interruzione utente (Ctrl-C) |

`main()` ritorna l'int; l'entrypoint fa `sys.exit(main())` / `raise SystemExit(main())`.

## 3. Contratto machine-readable (manifest)

Ogni tool ha **una voce** in [`scripts/tools.manifest.json`](../../scripts/tools.manifest.json)
conforme a [`scripts/schemas/tool_manifest.schema.json`](../../scripts/schemas/tool_manifest.schema.json).
Campi minimi: `id, path, category, language, invocation, summary, stability,
stdlib_only, external_bins, args, inputs, outputs, exit_codes, determinism,
side_effects, idempotent`.

Il manifest è la **fonte di verità**: da lì si generano gli artefatti che
consumano altri tool/umani.

```bash
python3 scripts/tools_manifest.py --emit-all   # rigenera registry.json / README.md / mcp-tools.json
python3 scripts/tools_manifest.py --check      # gate: schema + copertura + flag == --help
```

Il `--check` è **bloccante in CI**: se aggiungi uno script senza manifest, o
dichiari un flag che non esiste in `--help`, la build è rossa.

## 4. Determinismo

- Dichiaralo in `determinism.deterministic`. Se `true`, a parità di input
  l'output è **byte-identico** (nessun timestamp/wallclock nel contenuto salvato,
  output ordinato, `--seed` se usi `random`).
- Se stampi la data di generazione in un header, dichiaralo in `determinism.notes`
  (resta accettabile per artefatti di presentazione, non per output verificati in CI).

**Come si verifica** (per i tool idonei): l'harness esegue due volte e confronta.
```bash
python3 -m unittest scripts.tests.test_determinism
```

## 5. Sicurezza e side-effect

- Non scrivere `campaign/state.md` o `campaign/sessions/*` senza
  `side_effects.writes_canon: true` **e** conferma interattiva o `--yes`
  (ADR-0007: scritture canone solo su branch di gruppo, solo in regioni `auto:`).
- Idempotente dove possibile (ri-eseguibile senza danni).
- Gli output generati portano un header **"auto-generated — do not edit by hand"**.
- Accessi git/rete dichiarati (`side_effects.git_commit`, `side_effects.network`).

## 6. Dipendenze

- **Preferisci stdlib** (`stdlib_only: true`). Il repo gira in CI con il solo
  `pyyaml` come extra: se ne aggiungi altri, dichiarali in `external_deps` e
  motiva nel PR.
- Binari esterni (chromium, cwebp, docker, git) → `external_bins`, con fallback
  o messaggio d'errore chiaro se assenti.
- Dipendenze opzionali con fallback (es. tiktoken) → `optional_deps`.

## 7. Test

- **Minimo**: uno smoke `--help` nella sezione "DM tool smoke tests" della CI.
- **Logica non banale** (parsing, validazione, trasformazioni): test di
  comportamento sotto `scripts/tests/` (unittest, stdlib).
- I validatori/gate espongono `--json` per essere consumati da altri tool.

## 8. Shell script

- `#!/usr/bin/env bash` + `set -euo pipefail`.
- Quoting delle variabili; niente `cd` non necessari (usa path assoluti).
- `shellcheck` pulito.

```bash
shellcheck scripts/*.sh
```

## 9. Disciplina dei piani (ADR-0009)

Qualsiasi modifica strutturale (`scripts/`, `converters/`, `.github/`,
`skills/`, `plans/adr/`) richiede una riga in `plans/CHANGELOG.md` **nello stesso
commit**. Un tool nuovo che tocca la governance (nuovo gate, nuovo schema) valuta
anche un ADR in `plans/adr/`.

---

## Perché così (razionale da senior)

Una regola che la macchina non verifica non è una regola: è una speranza. Questo
standard sposta il costo dell'uniformità **una volta sola** (scrivere il manifest)
e lo rende **auto-difeso** dal gate `tools_manifest --check`. Il risultato è che
la documentazione non può divergere dal codice, e un orchestratore esterno può
trattare gli script del repo come tool tipizzati con input/output/exit-code noti.
