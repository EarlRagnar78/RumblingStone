# Editorial Standards — convenzioni redazionali (best practice editoriali)

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- 1. Terminologia canonica (mai deviazioni)
- 2. Read-aloud / boxed text (la resa che i giocatori sentono)
- 3. Gerarchia e struttura della pagina
- 4. Igiene editoriale
- 4-bis. Le scelte proprie del repo
- 5. Chi fa cosa (per non sprecare token)
<!-- /indice -->

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
| **otto ore di sonno** (incantesimi, capacità al giorno, 1 pf per livello), una **sosta** di N ore (3.5 e PF1e) | riposo breve, riposo lungo, short/long rest (5e) |
| **Lotta** (grapple 3.5); CMB/CMD solo in box PF1e dichiarati | CMB/CMD fuori dai box |
| Skill in italiano 3.5: Osservare, Nascondersi, Raggirare, Sapienza Magica… | Spot, Hide, Bluff, Spellcraft nel testo da tavolo |
| **Durik** (maschio) · **Skullcrusher** · **Terros** | Nymeria · Skulldark/Infernotooth · doppioni di boss |
| metri e **1,5 m/quadretto** | piedi nel testo da tavolo (ft solo negli statblock importati, con conversione) |
| 1.000 anni prima (≈372 DR) | "Anno −1000 DR" come data assoluta |

## 2. Read-aloud / boxed text (la resa che i giocatori sentono)

- **Blockquote in corsivo**, 3–10 righe; MAI più di un concetto di scena per box.
- **Un dettaglio sensoriale concreto per paragrafo** (regola Salvatore): il
  divino e gli artefatti si sentono **nel corpo** (denti, sterno, dita), non
  si "vedono" soltanto.
- Chiudere i box di combattimento su un **decision point** («Che fate?»),
  mai risolvere l'azione dei PG dentro il read-aloud.
- **Occhio da avventuriero, non da architetto** (ADR-0014): il box descrive
  ciò che si coglie in **sei secondi**, con scala per paragone («una bolla
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
- **La quarta colonna** ([ADR-0057](../../../plans/adr/ADR-0057-la-quarta-colonna-e-di-tutto-il-repo.md)):
  un blocco che descrive un ambiente **per sensi** chiude con **«Cosa NON
  dire»**, vincolante quanto le righe sopra. In tabella è la quarta colonna
  (Occhi / Orecchie / Pelle-naso / **Cosa NON dire**); in elenco è l'ultimo
  punto. Serve contro un rischio preciso: *il DM che, descrivendo
  l'atmosfera, racconta anche la scoperta*. Viene dall'Abbazia della Rotta
  Sicura, che ne ha 39 — **il dettaglio che non dici appartiene a chi fa la
  domanda**. ⚠️ Non è un obbligo su ogni read-aloud: vale dove il sensoriale
  è **strutturato in scheda**.
- Etichettare la regia: `**Read-aloud (pilastro lead).**`, così il prossimo
  agente sa quale voce continuare. **Ogni box** la porta, anche il micro-box di
  un attore e la riga d'esito di un tiro: un box senza etichetta, a metà di una
  sequenza, non dice più a chi appartiene la voce (L11, 2026-10-01: nelle prove
  è il difetto più frequente con la skill caricata).
- I dialoghi dei PNG: `**NOME (registro/tono):** *«battuta»*`: il tono
  dichiarato è parte del canone del personaggio. Fra parentesi **il tono in
  poche parole** (*sottovoce*, *senza alzare gli occhi*); il gesto lungo va
  fuori, come didascalia in corsivo dopo la battuta. Una parentesi da quindici
  parole non è più un tono, ed è quella che il prossimo agente non riconosce.

## 3. Gerarchia e struttura della pagina

- `#` solo per il titolo del file; `##` per le sezioni numerate (`§N`);
  `###` per le sotto-scene. Niente salti di livello.
- Tabelle per fatti enumerabili (CD, loot, soglie); prosa per tutto ciò che
  ha causa/effetto. Mai spiegazioni dentro le celle: la tabella enumera, il
  paragrafo spiega.
- I numeri di gioco nel testo: **grassetto** (CD 22, 345 pf, +30) così il DM
  li pesca a colpo d'occhio; corsivo per i nomi di incantesimi (*Muro di
  Pietra*).
- MAIUSCOLE di enfasi: con parsimonia, solo il beat che il DM deve far
  atterrare (PESO, TUMP), max 1-2 per read-aloud.

## 4. Igiene editoriale

- Niente code conversazionali AI («Perfetto! Procedo…»), niente meta-testo
  rivolto all'engine dentro i file di gioco: le note di lavorazione vivono
  nei banner di testa o nei commenti `> ⚠️`.
- Ogni fatto non attestato: `[INFERRED — <domanda al DM>; base: <fonte o dato>]` inline,
  MAI inventato in silenzio.
- Tono floor (coherence §4): adulto, slow-build, niente slang moderno,
  niente strizzate d'occhio alla quarta parete, nessuna vittoria senza costo.
- **La *d* eufonica** (CODA D3, 2026-11-08; ADR-0120): *ad* ed *ed* solo davanti
  alla **stessa** vocale (*legato ad Aegis Fang*, *armi ed equipaggiamento*); davanti
  alle altre vocali *a* ed *e* (*a ogni*, *a oggi*, *a un*, *e indifesa*). Resta solo
  *ad esempio* (*ad es.*). Mai *od*. Lo misura `validate_lingua.py` (cancello a zero),
  tarato su LanguageTool ST_03_001. Una citazione alla lettera che ha un'altra
  forma si marca sulla sua riga con `<!-- sic -->`.
- File name: `PortaleForgia-*`/`ARC*-DEF-*`: niente spazi anomali, casing
  coerente; i file superati prendono il banner e poi `_ARCHIVIO/`.

## 4-bis. Le scelte proprie del repo

Lo standard segue *Dungeon*, Paizo e WotC in quasi tutte le regole di
mestiere. Qui stanno le sole tecniche in cui il repo fa diverso dalle case
**e** ha una prova che il diverso è meglio per questo tavolo: il voto cieco
del DM (ADR-0093). Una tecnica entra qui solo se è peculiare e ha vinto al
cieco con un margine netto; le altre restano usi della casa, nei rispettivi
file. Le ha scelte il DM sulle card del 2026-11-19
([RICERCA-PROSA-PECULIARE](../../../plans/RICERCA-PROSA-PECULIARE-2026-11.md)).

| Scelta | Dove sta la regola | Le case dicono | La prova |
|---|---|---|---|
| **I sensi battono il tetto di lunghezza.** Quando il tetto delle frasi o dei caratteri e i dettagli sensoriali si scontrano, restano luce, colore, suono, caldo, freddo e il corpo che sente | `read-aloud-adulti.md` §2-ter, regola 1 | *Dungeon*: poche frasi; Merwin: niente dettagli superflui | 5 voti su 5 (giro 2, 2026-10-18) |
| **La chiusa enfatica resta.** La frase finale che dà nome alla meraviglia o all'eroe non si taglia; si tolgono solo le parole goffe, tradotte o ricercate | `read-aloud-adulti.md` §2-ter, regola 3 | LAMP: la frase «che spiega» si taglia | 4 voti su 4 (riscrittura, 2026-10-22) |

Nessuna delle due aggiunge parole o rende obbligatorio qualcosa: vietano un
taglio. Restano i limiti del registro alto (`read-aloud-adulti.md` §4-5).

## 5. Chi fa cosa (per non sprecare token)

| Livello | Chi |
|---|---|
| Ortografia/termini banditi/sezioni obbligatorie | `validate_modules.py` (CI, gratis) |
| Coerenza di canone (chi sa cosa, stati artefatti) | agente con `campaign-coherence.md` + `state.md` |
| Voce e pathos delle scene | agente con `style-pillars.md` (mix per scena) |
| Struttura/profondità del modulo | agente con `rumblingstone-module-standard` |
