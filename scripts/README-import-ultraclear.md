# `import_ultraclear.py` — contratto I/O

> Documentazione d'interfaccia (input/output) dell'importer di mappe
> **ultra-clear** → **bozza JSON contratto + report conflitti**. Pensata per chi
> deve **consumare a valle** i file prodotti (un editor visuale, uno script di
> migrazione, una CI): definisce con precisione cosa il tool legge, cosa
> restituisce, i tipi di record, i metadati e le garanzie. Per l'uso "operativo"
> e il razionale di dominio vedi `skills/rumblingstone-mapmaking/references/import-ultraclear.md`;
> qui è il **contratto**.

- **Sorgente**: `scripts/import_ultraclear.py` (Python 3, **solo stdlib**).
- **Schemi formali**: bozza → `scripts/schemas/tactical_map.schema.json`;
  report → `scripts/schemas/map_conflicts.schema.json`.
- **Determinismo**: a parità di input, **byte identici** su tutti gli output.

---

## 1. Cosa fa

Importa una mappa ultra-clear (griglia emoji + tabelle di coordinate + posizioni
PG scritte a mano) ed emette:

1. una **bozza** del contratto mappa (Modalità 3), conforme a
   `tactical_map.schema.json`;
2. un **report dei conflitti** figura↔tabella, in due formati (markdown per
   l'umano, JSON per un tool).

**Non decide** quale fonte ha ragione quando la griglia disegnata e le tabelle
divergono: rende la divergenza esplicita. **Policy di default**: *la tabella
vince* (dato autoritativo) — dichiarata nel report come `source_of_truth`.
**Non inventa** geometria; **non tocca** i master di canone (emette file nuovi).

---

## 2. Interfaccia a riga di comando

```
import_ultraclear.py INPUT.md [opzioni]
```

| Opzione | Tipo | Default | Significato |
|---|---|---|---|
| `INPUT.md` | path (posizionale, obbligatorio) | — | master ultra-clear da importare |
| `-o, --output` | path | stdout | dove scrivere la **bozza JSON** |
| `--conflicts` | path | stderr | **report markdown** leggibile |
| `--json-report` | path | *(non emesso)* | **report JSON** machine-readable (per l'editor) |
| `--emit-md` | dir | *(off)* | compila subito la bozza in un master `.md` nella cartella (round-trip) |
| `--map` | int (1-based) | tutte | se il file ha più mappe, importane una sola |
| `--strict` | flag | off | i `WARN` diventano fatali (exit 1) |
| `-q, --quiet` | flag | off | non stampare il report su stderr |
| `-v, --verbose` | flag | off | stampa anche gli errori di validazione della bozza |

### Exit code (contratto stabile, script-friendly)

| Code | Significato | Uso in automazione |
|---|---|---|
| `0` | bozza compilabile, **nessun ERROR** (WARN/INFO ammessi) | ok, procedi |
| `1` | prodotti **ERROR**: la bozza non è compilabile → **human-in-the-loop** (non è un crash) | ferma la pipeline, mostra i conflitti |
| `2` | errore d'uso/IO (file mancante, nessuna mappa a griglia, `--emit-md` fallito) | errore di invocazione |

Con `--strict`, la presenza di soli `WARN` forza `1`.

---

## 3. Input — cosa il tool parsa e con quali tipi

La griglia è letta con il **parser di `render_map_svg`** (single source of
truth): ciò che il tool "vede" è identico a ciò che il renderer disegnerebbe.
Il modello interno è la dataclass **`ParsedMap`** (deterministica):

| Campo | Tipo | Origine |
|---|---|---|
| `index` | int (1-based) | ordine della mappa nel file |
| `title` | str | banner interno al fence, o heading più vicino |
| `matrix` | `list[list[str]]` (0-based, densa e rettangolare) | griglia emoji (righe corte paddate col terreno base) |
| `declared_dims` | `(cols, rows)` \| `None` | header `N colonne × M righe` (banner o riga `**Dimensioni:**`) |
| `scale_m` | float | `… m/quadrato` (default 1.5) |
| `tables` | `list[TableEntry]` | tabelle markdown con colonne `COLONNE`/`RIGHE` |
| `pg` | `list[PgPos]` | righe prosa `**Nome:** Col X, Riga Y` |
| `north` | str | `NORD ↑`/default `N` |

Record ausiliari:

```text
TableEntry(name: str, col: (int,int), row: (int,int), note: str)   # col/row 1-based INCLUSIVI
PgPos(name: str, col: int, row: int, extra: str)                   # 1-based
```

`actual_dims` è una **property calcolata** dalla matrice (non può divergere dai
dati). Ciò che il parser non sa interpretare **degrada** a `notes`/INFO, mai a
dati inventati.

### Convenzione di coordinate (unica, in tutta la pipeline)

Le tabelle ultra-clear sono **1-based inclusive**; il contratto JSON è
**0-based** `[x, y]` (x = colonna, y = riga). Conversione:

```
punto:  Col C, Riga R            → [C-1, R-1]
rect:   Col Cs-Ce, Riga Rs-Re    → [Cs-1, Rs-1, Ce-Cs+1, Re-Rs+1]
```

Esempio verificato: `Col 60, Riga 34` → `[59, 33]`; `Col 18-21, Riga 17-19` →
`[17, 16, 4, 3]`.

---

## 4. Output A — la bozza JSON (contratto mappa)

Conforme a **`tactical_map.schema.json`**. È una **bozza**: va sempre rivista
(`compile_map_json.py --validate-only`). Forma (mappa singola):

```jsonc
{
  "schema_version": "1.0",
  "title": "…",
  "scale_m_per_square": 1.5,
  "units_in": "squares",          // sempre "squares" in uscita
  "map_size": [120, 80],          // [colonne, righe]
  "base_terrain": "🟩",           // simbolo fill più frequente
  "north": "N",
  "regions":    [ { "terrain": "⛰", "rect": [x,y,w,h], "label": "…" }, … ],
  "structures": [ { "type": "🗼", "rect": [x,y,w,h] | "at": [x,y], "label": "…" }, … ],
  "hazards":    [ { "type": "🔥", "at": [x,y] }, … ],
  "units":      [ { "token": "🔵", "area": {"rect": [x,y,w,h]}, "quantity": 50,
                    "name": "…", "faction": "…", "cr": "…" }, … ],
  "notes": [ "provenienza + elementi lasciati fuori + ruoli dedotti (specchio leggibile)" ]
}
```

- Le chiavi di lista (`regions`/`structures`/`hazards`/`units`) sono **presenti
  solo se non vuote**.
- `units` usa l'**astrazione per unità/aree** (`area.rect` + `quantity`), non un
  token per creatura.
- **Provenienza**: NON è nella bozza (il contratto è `additionalProperties:false`);
  vive nel report (Output B) come record con `target` che punta all'elemento.

**Multi-mappa**: se il file contiene più mappe e non usi `--map`, l'output è
`{ "maps": [ <bozza>, <bozza>, … ] }`.

---

## 5. Output B — il report conflitti JSON (`--json-report`)

Conforme a **`map_conflicts.schema.json`**. È il formato pensato per essere
**consumato da un altro tool** (l'editor visuale, una dashboard, una CI).

### 5.1 Envelope (metadati)

```jsonc
{
  "report_version": "1.0",        // versione del contratto del report
  "tool": "import_ultraclear.py",
  "map": 1,                       // indice 1-based della mappa
  "title": "…",
  "declared_dims": [120, 80],     // header, o null
  "actual_dims": [48, 65],        // celle reali contate
  "source_of_truth": "table",     // policy su divergenza figura↔tabella
  "counts": { "ERROR": 1, "WARN": 40, "INFO": 32 },
  "conflicts": [ <record>, … ]    // ordinati deterministicamente
}
```

Multi-mappa: `{ "maps": [ <envelope>, … ] }`.

### 5.2 Record di conflitto

Chiavi in ordine fisso; le chiavi vuote/`null` sono **omesse** (byte-stabili):

| Campo | Tipo | Sempre? | Significato |
|---|---|---|---|
| `uid` | str | ✓ | **chiave d'istanza stabile** (fingerprint `blake2s` del contenuto, indipendente dall'ordine). L'editor la usa per tracciare lo stato "risolto/ignorato" fra un run e l'altro |
| `id` | str `R1`..`R12` | ✓ | id della **REGOLA** (non dell'istanza): più record possono condividerlo |
| `rule` | str (slug) | ✓ | nome regola (vedi §6) |
| `severity` | `ERROR`\|`WARN`\|`INFO` | ✓ | gravità |
| `map` | int | ✓ | indice mappa |
| `source` | `grid`\|`table`\|`both`\|`legend` | ✓ | da dove nasce l'evidenza |
| `message` | str | ✓ | descrizione leggibile |
| `suggestion` | str | – | come risolverlo, in prosa |
| `where` | obj | – | **ancora geometrica** da evidenziare: `{ row?, cell?[x,y], cells?, rect?[x,y,w,h], coord? }` (0-based; `coord` = etichetta A1 tipo `V66`) |
| `observed` | obj\|null | – | la candidata lato **FIGURA**: `{ source, coord?, cell?, symbol?, name?, value? }` |
| `expected` | obj\|null | – | la candidata lato **TABELLA/legenda** (stessa forma): le due opzioni fra cui scegliere |
| `target` | str | – | **JSON Pointer (RFC 6901)** all'elemento della bozza, es. `/units/3`, `/map_size` |
| `actions` | array | – | risoluzioni **machine-actionable**: `[{ kind, label, params? }]` (vedi §7) |

### 5.3 Esempi reali

Conflitto **drift figura↔tabella** (WARN, le due candidate + i bottoni):

```json
{
  "uid": "R4-3b30a110", "id": "R4", "rule": "annotation-coord-drift",
  "severity": "WARN", "map": 1, "source": "both",
  "message": "«Nala Cantapietre» dichiarato a col 22, riga 66 ma la griglia lì mostra '🟨', non un token unità",
  "where": { "cell": [21, 65], "coord": "V66" },
  "observed": { "source": "grid",  "cell": [21, 65], "symbol": "🟨" },
  "expected": { "source": "table", "cell": [21, 65], "coord": "V66", "name": "Nala Cantapietre" },
  "actions": [ { "kind": "use_table", "label": "Colloca ai dati dichiarati (tabella)" },
               { "kind": "use_grid",  "label": "Tieni la figura ('🟨' resta terreno)" },
               { "kind": "ignore",    "label": "Ignora" } ]
}
```

**Assunzione semantica** (INFO, ancorata all'elemento con `target`):

```json
{
  "uid": "R12-…", "id": "R12", "rule": "inferred-role",
  "severity": "INFO", "map": 1, "source": "table",
  "message": "ruolo/simbolo DEDOTTO da un nome: «5 Cantitrici» → structure ⬛ (da verificare)",
  "observed": { "source": "table", "name": "5 Cantitrici" },
  "expected": { "role": "structure", "symbol": "⬛" },
  "target": "/structures/4",
  "actions": [ { "kind": "confirm", "label": "Conferma: structure ⬛" },
               { "kind": "reclassify", "label": "Cambia ruolo/simbolo" } ]
}
```

---

## 6. Registro delle regole (`id` → `rule`, severità)

| id | rule (slug) | Sev. | Rileva |
|---|---|---|---|
| R1 | `grid-header-mismatch` | ERROR | celle reali ≠ dimensioni dichiarate nell'header (D1) |
| R2 | `grid-nonuniform-rows` | WARN | righe di larghezza molto diversa fra loro |
| R3 | `symbol-not-in-legend` | ERROR/WARN | simbolo assente dalla legenda; variation-selector = WARN con suggerimento (D2) |
| R4 | `annotation-coord-drift` | WARN | token dove *appare* ≠ dove *dichiarato* (D4) |
| R5 | `name-collision` | WARN | nomi simili a coordinate diverse (Dara/Dana) (D3) |
| R6 | `coord-out-of-bounds` | ERROR | coordinata di tabella fuori da `map_size` |
| R7 | `overlapping-structures` | INFO | due strutture puntuali sulla stessa cella |
| R8 | `quantity-mismatch` | WARN | `quantity` dichiarata ≠ celle occupate dall'area |
| R9 | `non-emoji-cell` | WARN | carattere non-emoji dentro la matrice |
| R10 | `schematic-map-detected` | INFO | vista schematica/laterale → **saltata** (`render:none`) |
| R11 | `uncategorized-draft-error` | ERROR | **catch-all**: difetto non catalogato che rende la bozza non compilabile (scatta solo se nessun ERROR del registro lo spiega già) |
| R12 | `inferred-role` | INFO | **assunzione**: ruolo/simbolo/token dedotto da un nome (con `target` + `confirm`/`reclassify`) |

Il registro è **pluggabile**: una regola nuova = una funzione + un test.

---

## 7. Vocabolario delle azioni (`actions[].kind`)

L'editor mappa ogni `kind` a un bottone; applicarlo modifica la bozza in modo
deterministico. `params` opzionale.

| kind | params | Effetto atteso |
|---|---|---|
| `use_table` | `{to?}` | adotta il valore della tabella (autoritativo) |
| `use_grid` | — | adotta il valore della figura |
| `replace_symbol` | `{from, to}` | sostituisce un glifo |
| `resize_map` | `{to:[c,r]}` | cambia `map_size` |
| `edit_coord` | `{coord}` | corregge una coordinata |
| `set_quantity` | `{to}` | allinea il numero dichiarato |
| `confirm_distinct` | — | conferma che due nomi simili sono due entità |
| `rename` | `{name}` | rinomina una delle entità in collisione |
| `confirm` | — | accetta un'assunzione euristica |
| `reclassify` | `{role?, symbol?}` | cambia un ruolo/simbolo dedotto |
| `ignore` | — | scarta (no-op) |

---

## 8. Come consumarlo da un altro tool

- **Guida dall'exit code**: `0` procedi, `1` mostra i conflitti e fermati
  (human-in-the-loop), `2` errore d'invocazione.
- **`uid`** è la chiave stabile per lo stato di risoluzione (idempotente fra run).
- **`target`** è un JSON Pointer valido nella bozza corrispondente: risolvilo per
  saltare conflitto → elemento (badge "dedotto/da verificare" sull'elemento).
- **`where`** dà le celle/rect 0-based da evidenziare sul canvas.
- **`observed`/`expected`** sono le due candidate per una UI "scegli-una".
- **`source_of_truth`** dichiara la policy applicata (oggi `table`).
- **Determinismo**: puoi diffare due report per rilevare *cambiamenti reali* (gli
  `uid` non ballano con l'ordine).
- **Provenienza**: la trovi nei record `R12` (non nella bozza) — ogni elemento
  dedotto ha un record con `target` che lo indica.

### Esempio end-to-end

```bash
python3 scripts/import_ultraclear.py MAP.md \
    -o MAP.draft.json --json-report MAP.conflicts.json --conflicts MAP.report.md
rc=$?                                   # 0 ok · 1 ERROR (rivedi) · 2 IO
python3 scripts/compile_map_json.py MAP.draft.json --validate-only
# … l'editor legge MAP.conflicts.json, l'utente risolve, poi:
python3 scripts/compile_map_json.py MAP.draft.json -o MAP.master.md
python3 scripts/render_map_svg.py MAP.master.md
```

---

## 9. Garanzie / invarianti

- **Deterministico**: output byte-stabile (ordinamenti su `sorted`/`min`, nessuna
  iterazione dipendente da hash, `uid` = fingerprint del contenuto, JSON a chiavi
  fisse). Verificato in `scripts/tests/test_import_ultraclear.py`.
- **Fedeltà del parser**: nessun secondo parser divergente (riuso `render_map_svg`).
- **Nessun dato inventato**: l'illeggibile degrada a `notes`/INFO.
- **Niente di semantico è silenzioso**: ogni deduzione del tool è un record `R12`
  con `target` (parità 1:1 testata); ogni difetto che rompe la compilazione è
  `R11`.
- **Non-regressione**: `compile_map_json`/`validate_maps`/i test restano verdi;
  nessun master di canone toccato.
