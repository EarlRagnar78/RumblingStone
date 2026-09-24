# ADR-0028 — Anche un modulo nato in HTML ha un master markdown

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: DM, lotto F4 di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md) —
*«Convertire»*
**Applica**: [ADR-0003](ADR-0003-markdown-master-layout-generati.md) ·
**Riguarda**: [ADR-0017](ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md)

## Contesto

`10-stand-alone/L'abbazia Della Rotta Sicura/` è nato come **quattro pagine HTML
autonome**: stile dentro il file, tavole disegnate in SVG in linea, ~2.750 righe.
Si apre nel browser ed è bello. Ma stava **fuori da entrambe le catene**, e il
prezzo era concreto, non teorico:

- **nessun colophon**: il volume era anonimo, senza versione né regime d'uso,
  che è esattamente il buco che ADR-0023 ha chiuso per tutti gli altri;
- **nessuna edizione da stampa**: niente volume unico, niente segnalibri,
  niente impaginazione a due colonne: si stampava una pagina web;
- **lo stile in quattro copie**: una modifica tipografica andava rifatta quattro
  volte, e la quarta si dimenticava;
- **le tavole prigioniere della prosa**: un SVG dentro un `<figure>` non si apre
  in un editor vettoriale, non si riusa e non si cita da un altro documento.

## Decisione

**Il modulo prende un master markdown e un manifest**, come ogni altro volume del
repo. L'HTML resta nel repo come **edizione di riferimento congelata**, non come
sorgente viva; toglierlo è una decisione del DM, non di questo ADR.

### 1. Il travaso si fa con uno strumento, e una volta sola

`scripts/import_html_module.py` conosce il vocabolario di questa famiglia e lo
traduce in quello che le due catene già leggono: `p.ra` → **blockquote**
(read-aloud), `div.warn/.adr/.mech/.sb/.meta` → `{{note}}`, `div.entry` → chiave
d'area `#### C22 Le Celle`, `figure > svg` → **file `.svg` separato** più
`![didascalia]()`. Davanti a un tag che non conosce **lascia passare il contenuto
e lo dichiara**, invece di inventare una traduzione.

È **una volta sola** e lo strumento lo impone: se i master esistono già si ferma.
Dal momento in cui esistono, il markdown è il master — ci si correggono le chiavi
d'area, ci si rilegge la prosa — e rilanciare butterebbe via quel lavoro in
silenzio.

### 2. Le tavole escono, e escono **autonome**

Sette tavole in `tavole/*.svg`. «Autonome» ha voluto dire risolvere due difetti
che nessun controllo automatico vede:

- i **`<defs>` condivisi** (pattern di riempimento, marker delle frecce) stavano
  in un `<svg width="0">` in testa al documento e ogni tavola li citava con
  `url(#rock)`. Estratte senza, le tavole restavano formalmente valide e
  **rendevano sbagliato**. Ora ogni tavola se li porta dentro;
- **`html.parser` minuscola tutto, e XML è case-sensitive.** `viewBox` diventava
  `viewbox` e spariva; `patternUnits` diventava `patternunits` e il riempimento
  del mare tornava al default `objectBoundingBox`, cioè **un quadratino azzurro
  nell'angolo**. Il file restava XML valido: il difetto si vedeva solo
  guardando la pagina.

### 3. Cosa si è verificato

- **perdita di contenuto: zero parole**, su ~20.000, confrontando il testo
  visibile dei quattro HTML con i quattro markdown più le didascalie e il testo
  dentro le tavole estratte. È il controllo che ha trovato tutto il resto:
  `megereGrinza` (una ripulitura di «`** **`» che cancellava lo spazio fra due
  neretti adiacenti), i nomi dei PNG sparati **fuori** da una tabella da un
  `<br>` dentro una cella, e la barra `.meta` che stavo buttando via — e che
  invece dice *«Sostituisce: Tavola I e il blocco Il conto che non torna»*,
  cioè il rapporto fra un'appendice e il documento principale;
- **11 read-aloud su 11**: stavano su `<p class="ra">`, non su un `div`, e la
  prima versione li appiattiva tutti in prosa normale. Al tavolo è la differenza
  fra ciò che si legge ad alta voce e ciò che si riassume. Tre di essi stanno
  **dentro** un riquadro d'avviso, dove l'etichetta `⚠` finiva davanti al `>` e
  scioglieva la citazione;
- **le due catene compilano**: HTML 615 KB, PDF di **34 pagine** con segnalibri,
  frontespizio e **colophon**;
- **le pagine sono state guardate**, non solo compilate — è così che si sono
  visti il quadratino azzurro e le tavole senza texture.

### 4. Le chiavi d'area prendono il codice

`#### 22 Le Celle` → `#### C22 Le Celle`, sui codici dell'indice maestro
(B/A/T/C/G/X). Nella conversione la collisione si vedeva a occhio nudo: nello
**stesso file** c'erano `#### 3 Corpo di Guardia` (borgo) e `#### 3 Navata`
(abbazia).

## Conseguenze

**Buone.** Il modulo entra nelle due catene, guadagna colophon e volume da
stampa, e le sue sette tavole diventano asset riusabili.

**Il prezzo, dichiarato.**
- **Master e riferimento divergono.** I cerchietti numerati sulle **mappe**
  restano a numero nudo: il cerchio dell'HTML è largo 22 px e `C18` non ci sta.
  Le chiavi in prosa hanno il codice, le mappe no — e va bene perché ogni tavola
  dichiara il proprio livello, ma è una divergenza e sta scritta qui.
- **`div.?` non tradotto**: resta un `<div>` senza classe il cui contenuto passa
  ma la cui cornice si perde. È dichiarato dallo strumento a ogni esecuzione.
- **Gli statblocchi restano prosa**, dentro una cornice. Non diventano il formato
  machine-readable di [ADR-0021](ADR-0021-statblocchi-machine-readable.md): è un
  lavoro a sé, e mescolarlo al travaso avrebbe reso il diff illeggibile.

**Cosa NON decide.** Non dice di cancellare l'HTML, e non dice che ogni modulo
futuro debba nascere in HTML per poi essere convertito: **nascono in markdown**.
Questo strumento esiste per il debito già contratto.
