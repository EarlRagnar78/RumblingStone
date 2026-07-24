# Import ultra-clear → bozza JSON + report conflitti (`import_ultraclear.py`)

**Quando**: hai una mappa **ultra-clear** già scritta (griglia emoji + tabelle
di coordinate + posizioni PG scritte a mano) e vuoi migrarla nel **contratto
JSON** (Modalità 3) senza ridisegnarla da zero. Lo strumento estrae una
**bozza** e, soprattutto, **elenca i conflitti** che l'ASCII porta con sé.

> Non duplica la Modalità 3: là un LLM *scrive* il JSON da zero; qui si
> *estrae* una bozza da un ultra-clear esistente. Downstream la pipeline è
> identica (`compile_map_json.py` → `render_map_svg.py` → `export_uvtt.py`).

## Perché serve: l'ultra-clear fonde due cose

Un ultra-clear mescola la **figura leggibile** (la griglia disegnata a mano,
soggetta a drift) e i **dati autoritativi** (le tabelle di coordinate). Quando
divergono, la figura mente. Lo strumento **non decide** chi ha ragione: rende
la divergenza esplicita. Policy di default: **la tabella vince** (dati
autoritativi) + un WARN.

## Uso

```bash
python3 scripts/import_ultraclear.py INPUT.md \
    -o OUT.draft.json \
    --conflicts REPORT.md \          # report leggibile (default: stderr)
    --json-report REPORT.conflicts.json \   # report per l'editor visuale
    [--emit-md DIR] [--map N] [--strict] [-q|-v]

# human-in-the-loop: la bozza va sempre rivista
python3 scripts/compile_map_json.py OUT.draft.json --validate-only
```

**Exit code** (stabile, script-friendly):

| code | significato |
|---|---|
| `0` | bozza compilabile, nessun ERROR (WARN/INFO ammessi) |
| `1` | prodotti ERROR: la bozza NON è compilabile → correggere (segnale human-in-the-loop, non un crash) |
| `2` | errore d'uso/IO (file mancante, nessuna mappa a griglia) |

`--strict` promuove i WARN a fatali (per una CI severa).

## I 4 difetti-tipo (dal caso pilota Hammerfist L2)

| # | Difetto | Regola | Cosa fa il tool |
|---|---|---|---|
| D1 | griglia non uniforme vs header dichiarato | R1 `grid-header-mismatch` (ERROR) | conta le celle reali, segnala la divergenza, usa i dati autoritativi |
| D2 | simbolo fuori legenda (`⛰️` con variation-selector ≠ `⛰`) | R3 `symbol-not-in-legend` | riconosce i quasi-match e **suggerisce** il canonico (non sostituisce in silenzio) |
| D3 | collisione nomi (Dara/Dana) | R5 `name-collision` (WARN) | rileva nomi simili a coordinate diverse e chiede conferma |
| D4 | drift annotazione↔coordinata | R4 `annotation-coord-drift` (WARN) | confronta dove il token *appare* con dove è *dichiarato* |

Registro completo (estensibile): R1–R10 — vedi `§8` del piano
`plans/PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md`.

## Il report `--json-report` è input per l'editor visuale

Ogni conflitto è un record **machine-actionable** (contratto
`scripts/schemas/map_conflicts.schema.json`):

```json
{ "uid": "R4-3b30a110", "id": "R4", "rule": "annotation-coord-drift",
  "severity": "WARN", "source": "both",
  "message": "«Nala» dichiarato a col 22, riga 66 ma la griglia lì mostra '🟨'…",
  "where": { "cell": [21, 65], "coord": "V66" },
  "observed": { "source": "grid",  "cell": [21,65], "symbol": "🟨" },
  "expected": { "source": "table", "cell": [21,65], "name": "Nala" },
  "target": "/units/3",
  "actions": [ { "kind": "use_table", "label": "Colloca ai dati dichiarati" },
               { "kind": "use_grid",  "label": "Tieni la figura" },
               { "kind": "ignore",    "label": "Ignora" } ] }
```

- **`uid`** — chiave d'istanza stabile (fingerprint deterministico): l'editor
  traccia lo stato "risolto/ignorato" fra un'esecuzione e l'altra.
- **`where`** — ancora geometrica (celle/rect) da evidenziare, coord 0-based.
- **`observed` / `expected`** — le due candidate (figura vs tabella) fra cui
  scegliere.
- **`target`** — JSON Pointer (RFC 6901) all'elemento della bozza.
- **`actions`** — i bottoni dell'editor; applicare un'azione cambia la bozza in
  modo deterministico. Vocabolario: `use_table`, `use_grid`, `replace_symbol`,
  `resize_map`, `edit_coord`, `set_quantity`, `confirm_distinct`, `rename`,
  `ignore`.

La **provenienza per-elemento** vive nel report (sidecar), non nella bozza: il
contratto `tactical_map.schema.json` resta puro (`additionalProperties:false`).

## Cosa NON fa (per scelta)

- non decide quale fonte ha ragione (segnala, non sceglie);
- non inventa geometria mancante (elementi senza coordinate → in `notes`);
- non tocca i master canonici degli archi: emette file nuovi.
- mappe schematiche (side-view/prospettiche, `render: none`) → **saltate**.
