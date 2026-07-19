# ADR-0006 — Annotazioni mappa: overlay professionale (bussola, movimenti, callout, zone)

**Stato**: accettata
**Data**: 2026-07-19
**Decisione-fonte**: richiesta DM del 2026-07-19 (mappe drow Ultra-Clear: "voglio le posizioni, i movimenti, le leggende e l'orientamento a Nord, altrimenti non si capisce niente") — segue ADR-0003 (markdown master) e il piano `PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md`.

## Contesto

Le mappe Ultra-Clear (es. campi drow, quest di Hella) portano molte informazioni
inline nell'ASCII: rotte pattuglia, allarmi, zone tende, statistiche. Il renderer
`render_map_svg.py` — per scelta — legge **solo** le celle emoji e scarta le
annotazioni testuali, così l'SVG mostrava una griglia pulita ma **priva di
riferimenti** (movimenti, orientamento, callout). Inoltre l'ASCII a mano soffre
di drift: le etichette testuali ("Col M06") non sempre coincidono con la cella
dove sta davvero il token. Serviva un modo per portare posizioni, movimenti,
orientamento e leggende **nell'SVG**, restando deterministici e diffabili.

## Decisione

Introdurre **direttive `@` opzionali** dentro il blocco della griglia (dopo le
righe), che il renderer disegna come overlay + una legenda **INDICAZIONI**;
niente formati nuovi, niente asset esterni.

- `@north <deg|N..NW>` → bussola orientata (sempre presente sull'SVG; di default Nord in alto).
- `@path <label> ; <c1 c2 … [loop]> ; [#rrggbb]` → rotta di movimento (freccia tratteggiata + legenda).
- `@mark <n> ; <coord> ; <text>` → callout numerato (badge sul token + roster in legenda).
- `@zone <c1-c2> ; <text>` → area etichettata (rettangolo tratteggiato + legenda).

Le coordinate usano le **etichette A1** del righello (lettera colonna + numero
riga). Le direttive sono ignorate dal parser della griglia (non iniziano con un
numero di riga), quindi non alterano il censimento né la lettura delle celle.
`compile_map_json.py` (Modalità 3) **genera** queste direttive dai campi JSON
`north`, `movements`, dal roster `units` e dalle `label` delle aree — così una
mappa progettata da un LLM nasce già con orientamento, movimenti e riferimenti,
alle coordinate esatte (nessun drift).

Il **markdown resta il master** (ADR-0003): le direttive sono testo diffabile;
l'SVG resta l'artefatto generato e deterministico, validato in CI da
`validate_maps.py`.

## Conseguenze

- **Più facile**: leggere una mappa renderizzata (Nord, chi si muove dove, cosa
  sono le aree) senza aprire il markdown; progettare mappe tattiche "pronte"
  via JSON con posizioni verificate.
- **Costo**: aggiungere la bussola cambia i byte di **tutti** gli SVG committati
  → vanno rigenerati nello stesso commit (fatto). Le direttive sono un piccolo
  vocabolario in più da conoscere (documentato in `tre-modalita-mappe.md` e negli
  header degli script).
- **Da rivisitare**: se in futuro si vuole rendere anche gli statblock inline
  delle Ultra-Clear come callout, si estende `@mark`/una nuova direttiva, senza
  toccare il formato master. Le vecchie Ultra-Clear scritte a mano restano
  valide: acquisiscono la bussola subito; rotte/callout solo se si aggiungono le
  direttive (a mano o rigenerandole da un JSON).
