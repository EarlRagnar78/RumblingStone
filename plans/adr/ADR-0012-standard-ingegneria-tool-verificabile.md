# ADR-0012 — Standard di ingegneria obbligatorio per ogni nuovo tool/script, verificabile in CI

**Stato**: accettata
**Data**: 2026-07-24
**Decisione-fonte**: richiesta DM (audit script, 2026-07-24) — "una regola per
tutte le future creazioni di software, verificabile in CI/CD con test tool per
ogni verifica".

## Contesto

L'audit del 2026-07-24 (`docs/audit/AUDIT-REPORT.md`) ha trovato un toolkit
maturo ma **non uniforme**: due script ignoravano `argv` (il loro `--help`
eseguiva la logica scrivendo file), altri parsavano i flag a mano, il claim
"stdlib-only" era impreciso, e — soprattutto — non esisteva alcun **contratto
machine-readable** che un altro tool/agente potesse consumare. Ogni script era
"di qualità" a discrezione di chi lo scriveva, senza una barra comune né un
controllo automatico che la facesse rispettare nel tempo.

Senza una regola *verificata dalla macchina*, l'uniformità raggiunta con
l'audit degraderebbe alla prima aggiunta successiva (drift).

## Decisione

Ogni **nuovo** tool eseguibile del repo (Python o shell, sotto `scripts/` o
`converters/`) DEVE rispettare lo **standard di authoring** codificato in
[`docs/guides/TOOL-AUTHORING-STANDARD.md`](../../docs/guides/TOOL-AUTHORING-STANDARD.md).
Lo standard non è una linea guida "morbida": è **applicato in CI** e la sua
violazione fa fallire la build (gate bloccante), esattamente come i gate
esistenti su mappe/bestiario/piani.

Regole non negoziabili (il dettaglio operativo e i comandi di verifica sono
nella guida):

1. **Interfaccia**: `argparse` con `--help`; un flag informativo (`--help`,
   `--list`, `--check`) **non ha side-effect**.
2. **Contratto machine-readable**: una voce in `scripts/tools.manifest.json`
   conforme a `scripts/schemas/tool_manifest.schema.json` (input, output,
   `exit_codes`, `determinism`, `side_effects`, dipendenze).
3. **Exit code**: convenzione `0=ok · 1=errore-dominio · 2=errore-uso`.
4. **Determinismo**: dichiarato; se `deterministic: true`, output byte-identico
   a parità di input (verificato dall'harness double-run per i tool idonei).
5. **Sicurezza**: non scrive canone senza `writes_canon: true` dichiarato e
   conferma/`--yes`; idempotente dove possibile; output generati con header
   "auto-generated".
6. **Dipendenze**: `stdlib_only` preferito; ogni pacchetto di terze parti o
   binario esterno va dichiarato nel manifest (`external_deps`/`external_bins`).
7. **Test**: almeno uno smoke `--help` in CI; test di comportamento per la
   logica non banale.

L'implementazione di riferimento dello standard è **`scripts/tools_manifest.py`**
(stdlib-only, argparse, exit code canonici, deterministico, testato).

## Applicazione (verificabile — "test tool per ogni verifica")

| Regola | Strumento di verifica (CI/CD) | Esito |
|---|---|---|
| Manifest presente e conforme; nessuno script scoperto | `tools_manifest.py --check` | gate bloccante |
| Flag dichiarati == flag reali in `--help` | `tools_manifest.py --check` (cross-check) | gate bloccante |
| `--help` compila e non ha side-effect | smoke CI + `compileall` | gate bloccante |
| Determinismo dei tool `deterministic:true` | harness double-run (`test_determinism`) | gate bloccante |
| Shell robuste (`set -euo pipefail`, quoting) | `shellcheck` sui `*.sh` | gate (warning→bloccante dove pulito) |
| Convenzione exit code / stdlib-only | review + campo manifest | gate documentale |

## Conseguenze

- **Aggiungere un tool** significa: scrivere lo script conforme **+** la sua
  voce di manifest **+** (se serve) il test, nello stesso commit. Se manca il
  manifest o i flag non combaciano, la CI è rossa. Questo è il costo — voluto.
- Un orchestratore/agente esterno può scoprire e invocare i tool leggendo
  `docs/tools/registry.json` / `mcp-tools.json` senza leggere il codice.
- La doc umana (`docs/tools/README.md`) è **generata** dal manifest: non può
  più mentire rispetto al codice.
- Gli script **preesistenti** sono stati portati allo standard durante l'audit;
  eventuali eccezioni legacy sono marcate `stability: deprecated`/`internal` nel
  manifest e non fanno testo per i nuovi.

## Alternative scartate

- **Solo linee guida in un CONTRIBUTING** (non applicate): è ciò che ha prodotto
  il drift attuale. Scartata: senza gate, la regola non regge.
- **Adottare un validatore JSON-Schema di terze parti** (jsonschema): introduce
  una dipendenza pip nel cuore della governance. Scartata a favore di un
  validatore stdlib mirato in `tools_manifest.py`.
