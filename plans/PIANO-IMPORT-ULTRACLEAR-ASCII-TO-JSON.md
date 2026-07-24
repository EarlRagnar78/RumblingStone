# 🧭 PIANO — `import_ultraclear.py`: da ASCII ultra-clear a JSON di bozza + report conflitti

> **Cos'è**: il piano per uno strumento che **importa una mappa ultra-clear**
> (griglia emoji + tabelle di coordinate + posizioni PG scritte a mano) e ne
> emette una **bozza del contratto JSON** (`scripts/schemas/tactical_map.schema.json`,
> Modalità 3) **insieme a un report dei conflitti** che l'ASCII porta con sé.
> Serve a **migrare in semi-automatico** le ~30 mappe ultra-clear esistenti nel
> formato canonico corretto, senza fingere che una macchina possa risolvere da
> sola gli errori *semantici* (quelli restano una decisione umana/LLM).
>
> **Origine**: caso pilota **Hammerfist L2** (2026-07-23). Ricostruendo a mano
> `08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md` in
> `scripts/examples/hammerfist-L2-assedio.json` sono emersi 4 difetti-tipo
> dell'ultra-clear che **confondono la pipeline**; questo tool li rende
> *diagnosticabili e migrabili* invece che scoprirli a occhio dopo il render.
>
> **Non duplica** ma **completa** la Modalità 3: là un LLM *scrive* il JSON da
> zero; qui si *estrae* una bozza da un ultra-clear già esistente. Downstream la
> pipeline è identica (`compile_map_json.py` → `render_map_svg.py` → `export_uvtt.py`).
>
> Engine: Opus (design/diagnostica) + Sonnet (parser/impl.) · Skill di dominio:
> `rumblingstone-mapmaking`, `rumblingstone-debugging`. Regola d'oro dei piani:
> chi chiude un lotto aggiorna checklist + `plans/INDEX.md` + `plans/CHANGELOG.md`.

---

## §0 — TL;DR

Un importer **non può** correggere da solo un ultra-clear rotto: gli errori sono
*semantici* (l'header dice 120 colonne ma le righe ne hanno 34-48; l'annotazione
"DARA Top" è sotto la riga sbagliata). Ma **può**: (1) parsare fedelmente la
griglia e le tabelle, (2) emettere una **bozza JSON**, (3) **elencare i
conflitti** con severità e suggerimenti, così l'umano/LLM risolve solo i punti
segnalati. È l'80% del lavoro di migrazione automatizzato, con la parte di
giudizio isolata e visibile.

---

## §1 — I 4 difetti-tipo dell'ultra-clear (dal caso Hammerfist L2)

| # | Difetto | Sintomo nella pipeline | Cosa fa il tool |
|---|---|---|---|
| D1 | **Griglia non uniforme**: righe con 34-48 celle sotto header dichiarato `120×80` | il renderer disegna la figura approssimata, non le coordinate vere → posizioni sbagliate | conta le celle per riga, confronta con l'header, **segnala la divergenza** e la riga/e incriminate |
| D2 | **Simbolo fuori legenda**: `⛰️` (con variation-selector U+FE0F) ≠ `⛰` canonico | reso come emoji grezzo «simbolo locale», semantica persa | normalizza/riconosce i quasi-match e **suggerisce il simbolo di legenda** corretto |
| D3 | **Collisione/confusione nomi**: Dara (cecchino, torre) vs Dana (guaritrice, cortile) | posizioni scambiate, PG sul posto sbagliato | rileva nomi simili a coordinate diverse e **chiede conferma** (non decide) |
| D4 | **Drift annotazione↔coordinata**: "DARA Top" sotto la riga 64 ma tabella dice riga 62; torri disegnate a col 01-02 ma tabella col 08-11 | la posizione a schermo non combacia con quella dichiarata | confronta la cella dove *appare* il token con quella *dichiarata* nelle tabelle e **segnala lo scarto** |

**Causa comune**: l'ultra-clear **fonde due cose** che vanno separate — la
*figura leggibile* e i *dati autoritativi* (tabelle). Quando divergono, la figura
mente. Il tool rende esplicita la divergenza e produce l'output basato sui **dati
autoritativi** quando ci sono, sulla figura quando sono l'unica fonte.

---

## §2 — Ambito (cosa fa / cosa NON fa)

**Fa**:
- legge **un master ultra-clear** `.md` (uno o più blocchi mappa);
- parsa la **griglia emoji** riusando lo stesso parser di `render_map_svg.py`
  (single source of truth: niente secondo parser che diverge);
- parsa le **tabelle di coordinate** («| STRUTTURA | COLONNE | RIGHE | … |») e le
  **liste posizioni PG** («**Nome:** Col X, Riga Y»);
- **riconcilia** griglia ↔ tabelle e produce una **bozza JSON** conforme allo
  schema (in `units_in: squares`, 0-based);
- emette un **report conflitti** con severità `ERROR`/`WARN`/`INFO` + suggerimenti;
- opz. `--emit-md`: compila subito la bozza via `compile_map_json.py` per un
  round-trip immediato.

**NON fa** (per scelta, non per limite tecnico):
- **non decide** quale fonte ha ragione quando griglia e tabella divergono
  (segnala, non sceglie);
- **non inventa** geometria mancante (muri non dichiarati, riserve senza coord →
  lasciati fuori e annotati in `notes`);
- **non tocca** i master canonici degli archi: emette file nuovi (`.json` +
  opz. `.md`), l'originale ultra-clear resta invariato finché il DM non canonizza.

---

## §3 — Architettura tecnica

```
ultra-clear.md
   │
   ├─(A) parser griglia   → riuso render_map_svg.extract_maps / parse_row_cells
   ├─(B) parser tabelle   → coordinate strutture + posizioni PG (euristiche md)
   │
   ▼
(C) motore di riconciliazione/diagnostica
   │   • header-dims vs celle reali (D1)
   │   • simboli vs legenda universale, quasi-match/variation-selector (D2)
   │   • nomi simili a coord diverse (D3)
   │   • token disegnato vs token dichiarato (D4)
   ▼
(D) emissione
   ├─ bozza JSON (tactical_map.schema.json, units_in: squares)  → *.draft.json
   └─ report conflitti (stdout + opz. *.conflicts.md)           → ERROR/WARN/INFO
        │
        └─(opz. --emit-md) compile_map_json.py → master .md → render_map_svg.py
```

**Punti di progetto chiave**:

- **(A) Riuso del parser esistente**: la griglia si legge con le funzioni di
  `render_map_svg.py` (`extract_maps`, `parse_row_cells`) — così ciò che il tool
  «vede» è *identico* a ciò che il renderer disegnerebbe. È il modo per
  diagnosticare D1/D4 in modo fedele.
- **(B) Parser tabelle**: euristico ma **conservativo**. Riconosce (b1) tabelle
  markdown con header contenente `COLONNE`/`RIGHE` e (b2) righe in prosa
  `Nome: Col X, Riga Y (+Zm)`. Ogni valore non parsabile diventa un `INFO`, mai
  un dato inventato.
- **(C) Diagnostica**: ogni check produce un record `{severità, dove (coord/riga),
  messaggio, suggerimento}`. `ERROR` = la bozza sarebbe non compilabile o
  semanticamente rotta (dims incoerenti, simbolo ignoto senza quasi-match);
  `WARN` = divergenza risolvibile (drift D4, collisione nomi D3); `INFO` = dato
  lasciato fuori (riserve senza coord).
- **(D) Emissione**: la bozza usa i **dati autoritativi** (tabelle) per le
  posizioni quando presenti; ricade sulla figura solo dove le tabelle tacciono.
  Mappa simboli→ruolo dalla legenda (`SYMBOLS`: `fill`→terreno/region,
  `icon`→structure/hazard, `unit`→units). L'euristica unità: token `unit` isolato
  → `at`; blocco contiguo di stesso token → `area.rect` con `quantity` stimata
  dal conteggio celle **e** segnalata come `WARN` se diverge dal numero scritto
  nelle tabelle ("50 Nani").
- **Zero dipendenze** (stdlib), **deterministico**, stile coerente col repo.

---

## §4 — Fasi (engine consigliato + impegno)

> Routing engine per fase (regola `rumblingstone-plans`): NON è un gate CI.

| Fase | Obiettivo | Engine | Impegno |
|---|---|---|---|
| **F1 — Parser griglia (riuso)** | Estrarre celle/righe con `render_map_svg` e ricavare dims reali, mappa cella→simbolo, blocchi contigui di token | Sonnet | Basso |
| **F2 — Parser tabelle** | Estrarre coordinate strutture (tabelle md) e posizioni PG (prosa `Col X, Riga Y`); normalizzare 1-based→0-based | Sonnet | Medio |
| **F3 — Diagnostica conflitti** | I 4 check D1-D4 + simboli fuori legenda + collisioni nomi; record con severità/suggerimento | Opus (regole) | Medio |
| **F4 — Emissione bozza JSON** | Comporre `map_size/regions/structures/hazards/units/movements` dai dati riconciliati; ruoli da `SYMBOLS`; `notes` con gli elementi lasciati fuori | Opus (resa) + Sonnet | Medio |
| **F5 — CLI + round-trip** | `import_ultraclear.py in.md -o out.draft.json [--conflicts f.md] [--emit-md dir]`; loop con `compile_map_json.py --validate-only` | Sonnet | Basso |
| **F6 — Test + golden case** | `scripts/tests/test_import_ultraclear.py`: parser griglia/tabelle, ognuno dei 4 conflitti su fixture minime, e **Hammerfist L2 come golden case** (l'output riconcilia verso `hammerfist-L2-assedio.json` già committato) | Sonnet | Medio |
| **F7 — Doc + CI** | `references/import-ultraclear.md` nella skill mapmaking + voce in `tre-modalita-mappe.md`; smoke test in `ci.yml` (`--help`, import di un fixture); README esempi | Sonnet | Basso |

---

## §5 — Gate & definizione di "fatto"

- **Fedeltà del parser**: ciò che il tool legge dalla griglia coincide con ciò che
  `render_map_svg.py` disegnerebbe (nessun secondo parser divergente).
- **Bozza compilabile**: l'output `*.draft.json` supera `compile_map_json.py
  --validate-only` **oppure** il report elenca gli `ERROR` che lo impediscono (mai
  un JSON silenziosamente rotto).
- **Golden case**: importando l'ultra-clear di Hammerfist L2, il report elenca i 4
  difetti-tipo e la bozza, applicati i suggerimenti, converge verso
  `scripts/examples/hammerfist-L2-assedio.json` (diff semantico manuale accettabile).
- **Non-regressione**: `validate_maps`/`validate_skills`/test verdi; nessun master
  di canone toccato.

---

## §6 — Rischi / attenzioni

- **Il parser tabelle è euristico**: formati di tabella molto liberi possono non
  essere riconosciuti → devono degradare a `INFO` («tabella non interpretata»),
  mai a dati inventati.
- **Tentazione di "auto-fixare" la semantica**: da evitare. Il valore del tool è
  *rendere visibili* i conflitti, non nasconderli con scelte arbitrarie.
- **Mappe non-rettangolari/schematiche** (esagonali, side-view, prospettiche come
  le VISTA 3/4 di Hammerfist): riconoscerle e **saltarle** con un `INFO`
  (`render: none`-like), non forzarle in una griglia.
- **Variation-selector e quasi-simboli** (D2): normalizzazione Unicode prudente;
  suggerire, non sostituire in silenzio.
- **Coerenza `SYMBOLS`**: il tool legge la legenda da `render_map_svg.SYMBOLS`
  (unica fonte) — se in futuro nasce `legend.json` (vedi
  [PIANO-EDITOR-VISUALE-MAPPE-TATTICHE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) §4),
  il tool vi si aggancia per non duplicare.

## §7 — Contratto CLI & I/O (interface spec)

```
import_ultraclear.py INPUT.md [opzioni]
  -o, --output FILE        bozza JSON (default: stdout)
  --conflicts FILE         report leggibile (markdown); default: stderr
  --json-report FILE       report machine-readable (.conflicts.json) per l'editor
  --emit-md DIR            compila subito la bozza (compile_map_json) → master .md
  --map N                  se il file ha più mappe, quale importare (default: tutte)
  --strict                 WARN diventano fatali (per la CI severa)
  -q/-v                    verbosità
```

**Exit code** (contratto stabile, script-friendly):
- `0` — bozza compilabile, nessun `ERROR` (eventuali WARN/INFO nel report);
- `1` — prodotti `ERROR`: la bozza NON è compilabile → va corretta (è il segnale
  di "human-in-the-loop", non un crash);
- `2` — errore d'uso/IO (file mancante, markdown illeggibile).

**Schema del record conflitto** (una voce del `--json-report`):
```json
{ "id": "R1", "rule": "grid-header-mismatch", "severity": "ERROR",
  "map": 1, "where": { "row": 25, "cell": [59,33], "coord": "BH34" },
  "message": "riga 25: 48 celle ma header dichiara 120 colonne",
  "suggestion": "riallineare la riga o correggere l'header",
  "source": "grid|table|both" }
```
`--json-report` è pensato per essere **consumato dall'editor visuale** (Piano 2)
che evidenzia le celle in conflitto. Determinismo: a parità di input, byte
identici (regole in ordine fisso, nessun timestamp).

---

## §8 — Registro regole conflitti (estensibile, non solo i 4 difetti-tipo)

I 4 difetti-tipo (D1-D4) sono l'insieme *iniziale*. L'architettura è un **registro
di regole** pluggabili `rules: list[Callable[[ParsedMap], list[Conflict]]]`, così
aggiungerne una non tocca il resto. Catalogo minimo alla v1:

| Regola | ID | Severità | Cosa rileva |
|---|---|---|---|
| grid-header-mismatch (D1) | R1 | ERROR | conteggio celle riga ≠ header dichiarato |
| grid-nonuniform-rows | R2 | WARN | righe di larghezza diversa fra loro |
| symbol-not-in-legend (D2) | R3 | ERROR/WARN | simbolo assente da `SYMBOLS`; quasi-match (variation-selector) = WARN con suggerimento |
| annotation-coord-drift (D4) | R4 | WARN | token dove *appare* ≠ dove *dichiarato* nelle tabelle |
| name-collision (D3) | R5 | WARN | nomi simili a coordinate diverse (Dara/Dana) |
| coord-out-of-bounds | R6 | ERROR | coordinata di tabella fuori da `map_size` |
| overlapping-structures | R7 | INFO | due strutture sulla stessa cella (precedenza ambigua) |
| quantity-mismatch | R8 | WARN | `quantity` scritta ≠ celle occupate dal blocco unità |
| non-emoji-cell | R9 | WARN | cella con carattere non-emoji dentro la matrice |
| schematic-map-detected | R10 | INFO | side-view/prospettica/esagonale → **saltata** (`render:none`) |

Ogni regola dichiara `id`, `severità di default`, e produce record conformi a §7.
Il `--strict` promuove i WARN a fatali. Nuove regole = un test unità ciascuna.

---

## §9 — NFR, versioning, testing (best practices)

**Non-funzionali**:
- **Determinismo**: output byte-stabile (nessun ordinamento dipendente da hash o
  tempo); vale sia per la bozza sia per i report.
- **Zero dipendenze** (stdlib), coerente col repo; **performance** su mappe fino a
  `200×200` (limite schema) in <1 s.
- **Unicode**: normalizzazione NFC prudente; i quasi-match (es. `⛰️`→`⛰`) si
  *suggeriscono*, non si applicano in silenzio.
- **Idempotenza**: reimportare la bozza già compilata non deve generare nuovi
  ERROR (round-trip stabile).

**Versioning/migrazione**: la bozza emessa dichiara `schema_version` e
`units_in: "squares"`; se un ultraclear esprime misure in metri nelle tabelle,
l'importer può emettere `units_in: "meters"` (riusa la conversione del
compilatore) — deciso in F4.

**Strategia di test** (`scripts/tests/test_import_ultraclear.py`):
- **unit per regola** (una fixture minima che scatta ciascuna R1-R10);
- **golden case** Hammerfist L2 → converge a `hammerfist-L2-assedio.json`;
- **property/round-trip**: `import → compile_map_json --validate-only` verde su
  tutti i fixture senza ERROR; bozza→compile→(re)import senza nuovi conflitti;
- **fixtures** in `scripts/tests/fixtures/ultraclear/` (griglia uniforme, griglia
  driftata, mappa schematica, simbolo fuori legenda).

---

## §10 — MVP / walking skeleton (da dove partire)

Fetta verticale minima che gira end-to-end **prima** di tutte le regole:
> `F1 (parse griglia) → F4-min (emetti bozza dalla sola griglia, senza tabelle) →
> F5 (CLI + compile --validate-only)`. Su una **griglia uniforme** produce già una
> bozza compilabile. Poi si aggiungono, una alla volta, il parser tabelle (F2) e
> le regole del registro (§8), ognuna col suo test. Questo dà valore al primo
> giorno e riduce il rischio d'integrazione.

---

## §11 — Decisioni aperte → **FISSATE** (2026-07-24)

1. **Fonte di verità in caso di conflitto griglia↔tabella**: ✅ *la tabella
   vince* (dati autoritativi) + WARN. Registrata nel report come
   `source_of_truth: "table"`.
2. **Formato report**: ✅ **entrambi** — md leggibile (`--conflicts`) **e**
   `.conflicts.json` (`--json-report`, per l'editor).
3. **`--emit-md`**: ✅ **opt-in** (l'importer produce dati, non master, salvo
   richiesta esplicita).

> Nota d'attuazione (§7 rafforzato): il record di conflitto è stato reso
> pienamente **editor-consumable** oltre alla bozza §7 originaria — ogni voce
> porta `uid` (fingerprint d'istanza stabile), `observed`/`expected` (le due
> candidate figura↔tabella), `target` (JSON Pointer RFC 6901 nella bozza) e
> `actions` machine-actionable (i bottoni dell'editor). Contratto formale in
> `scripts/schemas/map_conflicts.schema.json`. La provenienza per-elemento vive
> nel sidecar, non nella bozza (che resta `additionalProperties:false`).

---

## §12 — Stato

🟢 **ESEGUITO** (2026-07-24, branch `claude/piani-completare-5b85qg`). Tutte le
fasi F1-F7 implementate e testate:

- **F1** parser griglia — riuso `render_map_svg.extract_maps`/`parse_row_cells`
  (single source of truth); dims reali, matrice, blocchi contigui.
- **F2** parser tabelle (`| COLONNE | RIGHE |`) + posizioni PG prose
  (`Col X, Riga Y`); normalizzazione 1-based → 0-based.
- **F3** diagnostica — **registro R1-R10** (`RULES`), record con severità +
  suggerimento + campi strutturati.
- **F4** emissione bozza — `regions/structures/hazards/units` da griglia
  (path uniforme) o da tabelle autoritative (path grid-inutilizzabile);
  `notes` con gli elementi lasciati fuori e i ruoli dedotti.
- **F5** CLI (`-o/--conflicts/--json-report/--emit-md/--map/--strict/-q/-v`),
  exit code 0/1/2, round-trip `compile_map_json.validate`.
- **F6** `scripts/tests/test_import_ultraclear.py` (17 test): fixture-per-regola
  in `scripts/tests/fixtures/ultraclear/`, golden case Hammerfist L2,
  round-trip, determinismo. 55 test totali verdi.
- **F7** doc skill (`skills/rumblingstone-mapmaking/references/import-ultraclear.md`
  + rimandi in `SKILL.md`/`tre-modalita-mappe.md`), `scripts/README-automation.md`,
  smoke test in `.github/workflows/ci.yml`, contratto report
  `scripts/schemas/map_conflicts.schema.json`.

**Gate soddisfatti** (§5): parser fedele (nessun secondo parser), bozza
compilabile o `ERROR` elencati, golden case converge (aree Cantitrici/Nani-Elite
byte-identiche, PG ai coord dichiarati, `map_size 120×80`), non-regressione
verde, nessun master di canone toccato.

Prerequisiti usati: parser griglia (`render_map_svg`), contratto+compilatore
(`compile_map_json`), caso pilota committato (`hammerfist-L2-assedio.*`).
