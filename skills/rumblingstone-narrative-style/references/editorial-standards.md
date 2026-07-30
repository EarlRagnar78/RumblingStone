# Editorial Standards — convenzioni redazionali (best practice editoriali)

Copy-editing e tipografia per TUTTO il contenuto generato del repo. Le
regole di *voce* stanno in `style-pillars.md`; qui sta la **resa sulla
pagina**: come si scrive, si formatta e si nomina. La parte meccanica di
queste regole è enforced in CI da `scripts/validate_modules.py` (zero
token): l'agente non la ri-verifica a mano.

## 1. Terminologia canonica (mai deviazioni)

| ✅ Canone | ❌ Vietato / deprecato |
|---|---|
| **CD** (Classe Difficoltà) | DC |
| azione **veloce** / **immediata** / preparata (3.5) | bonus action, reaction, lair action, vantaggio/svantaggio (5e) |
| **Lotta** (grapple 3.5); CMB/CMD solo in box PF1e dichiarati | CMB/CMD fuori dai box |
| Skill in italiano 3.5: Osservare, Nascondersi, Raggirare, Sapienza Magica… | Spot, Hide, Bluff, Spellcraft nel testo da tavolo |
| **Durik** (maschio) · **Skullcrusher** · **Terros** | Nymeria · Skulldark/Infernotooth · doppioni di boss |
| metri e **1,5 m/quadretto** | piedi nel testo da tavolo (ft solo negli statblock importati, con conversione) |
| 1.000 anni prima (≈372 DR) | "Anno −1000 DR" come data assoluta |

## 2. Read-aloud / boxed text (la resa che i giocatori sentono)

- **Blockquote in corsivo**, 3–10 righe; MAI più di un concetto di scena per box.
- **Un dettaglio sensoriale concreto per paragrafo** (regola Salvatore) — il
  divino e gli artefatti si sentono **nel corpo** (denti, sterno, dita), non
  si "vedono" soltanto.
- Chiudere i box di combattimento su un **decision point** («Che fate?») —
  mai risolvere l'azione dei PG dentro il read-aloud.
- **Occhio da avventuriero, non da architetto** (ADR-0014): il box descrive
  ciò che si coglie in **sei secondi** — scala per paragone («una bolla
  grande come la piazza di un mercato», «una lastra larga quanto la sala di
  una locanda»), materiali, temperatura, odore, cosa è *sbagliato*. Le
  metrature e i Ø restano nel blocco **«Dati per il DM (non da leggere)»**
  o sulla mappa: un DM che legge «sfera Ø 60 m» ai giocatori sta leggendo
  una perizia, non raccontando una stanza.
- **Nessuna sequenza a battute senza regia** (ADR-0014): dove c'è un giro di
  round/fasi (rito, boss, skill challenge, hazard) servono apertura di
  round, **un micro-box per attore** nell'ordine di gioco, **una riga di
  esito per riuscita e una per fallimento**, chiusura di round. I dadi senza
  descrizione spengono la scena. Esemplare: `ARC07-DEF-1` §9 «FASE 2 — la
  regia dei tre round».
- Etichettare la regia: `**Read-aloud (pilastro lead).**` — così il prossimo
  agente sa quale voce continuare.
- I dialoghi dei PNG: `**NOME (registro/tono):** *«battuta»*` — il tono
  dichiarato è parte del canone del personaggio.

## 3. Gerarchia e struttura della pagina

- `#` solo per il titolo del file; `##` per le sezioni numerate (`§N`);
  `###` per le sotto-scene. Niente salti di livello.
- Tabelle per fatti enumerabili (CD, loot, soglie); prosa per tutto ciò che
  ha causa/effetto. Mai spiegazioni dentro le celle: la tabella enumera, il
  paragrafo spiega.
- I numeri di gioco nel testo: **grassetto** (CD 22, 345 pf, +30) così il DM
  li pesca a colpo d'occhio; corsivo per i nomi di incantesimi (*Muro di
  Pietra*).
- MAIUSCOLE di enfasi: con parsimonia — solo il beat che il DM deve far
  atterrare (PESO, TUMP), max 1-2 per read-aloud.

## 4. Igiene editoriale

- Niente code conversazionali AI («Perfetto! Procedo…»), niente meta-testo
  rivolto all'engine dentro i file di gioco: le note di lavorazione vivono
  nei banner di testa o nei commenti `> ⚠️`.
- Ogni fatto non attestato: `[INFERRED — needs DM confirmation]` inline,
  MAI inventato in silenzio.
- Tono floor (coherence §4): adulto, slow-build, niente slang moderno,
  niente strizzate d'occhio alla quarta parete, nessuna vittoria senza costo.
- File name: `PortaleForgia-*`/`ARC*-DEF-*` — niente spazi anomali, casing
  coerente; i file superati prendono il banner e poi `_ARCHIVIO/`.

## 5. Chi fa cosa (per non sprecare token)

| Livello | Chi |
|---|---|
| Ortografia/termini banditi/sezioni obbligatorie | `validate_modules.py` (CI, gratis) |
| Coerenza di canone (chi sa cosa, stati artefatti) | agente con `campaign-coherence.md` + `state.md` |
| Voce e pathos delle scene | agente con `style-pillars.md` (mix per scena) |
| Struttura/profondità del modulo | agente con `rumblingstone-module-standard` |
