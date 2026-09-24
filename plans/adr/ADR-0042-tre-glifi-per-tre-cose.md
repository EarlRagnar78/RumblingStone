# ADR-0042 — Tre cose sotto un glifo: ⬛ si separa in edificio, tenda e dais

- **Stato**: accettata
- **Data**: 2026-09-04
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: `LEGENDA-FUNZIONALE-SPEC` §6.2 · decisione DM del 2026-09-04:
  *«fai 3 glifi separati, altrimenti non si capisce niente»*

## Contesto

Il glifo `⬛` portava questa etichetta nel renderer:

> *Struttura (tenda, edificio, dais)*

Tre cose diverse sotto un simbolo solo, su **8.216 celle in 24 file** — il
glifo di terreno più usato del repo dopo il pavimento. E l'export UVTT le
trattava **tutte e tre da muro pieno**.

Sono davvero diverse, e la differenza si sente al tavolo:

- un **edificio** è un muro: blocca la vista, blocca il movimento, non lo
  abbatti nel giro di un combattimento;
- una **tenda** blocca la vista come un muro, ma è un telo teso su pali: ci si
  entra, si taglia, brucia. In un accampamento è il terreno principale;
- un **dais** — la pedana rialzata di una sala del trono — **non è un muro
  affatto**. Ci si sale sopra. Semmai è `elevation_m`.

Un DM che apre la mappa di un accampamento drow su Foundry oggi trova 2.173
quadretti di muro invalicabile dove ci sono delle tende.

**Il difetto peggiore, che la spec di luglio non aveva visto**: la legenda
conteneva **già** `⛺ Tenda` e `🏛 Edificio / tempio`. `⬛` non era solo
sovraccarico — **duplicava due glifi che esistevano**, e per giunta `⛺` non era
in `WALL_SYMS`, quindi le tende disegnate col glifo giusto non bloccavano
nemmeno la vista, mentre quelle disegnate col glifo sbagliato bloccavano tutto.
Le due direzioni dell'errore si annullavano solo per caso.

## Decisione

### 1. Tre glifi, e uno è nuovo

| Glifo | Significato | Vista | Movimento | Muro UVTT |
|---|---|---|---|---|
| `⬛` | **Edificio / corpo di fabbrica** — muratura piena | blocca | blocca | **sì** *(invariato)* |
| `⛺` | **Tenda** — telo teso: si taglia, si abbatte, brucia | blocca | blocca finché sta in piedi | **sì** *(era «no»)* |
| `🔳` | **Dais / pedana rialzata** — ci si sale sopra | **no** | **no** | **no**, è quota |

`🔳` è nuovo e non compariva da nessuna parte nel repo: nessuna collisione.
`🏛` resta quello che era — *edificio / tempio* come **prop illustrato**, mentre
`⬛` è il riempimento pieno; sono due modi di rendering della stessa cosa, non
due significati.

### 2. `⬛` non cambia comportamento

È la scelta che rende la decisione applicabile subito: `⬛` conserva
**esattamente** la semantica di oggi (muratura piena, muro UVTT). Nessuna delle
8.216 celle esistenti cambia comportamento; nessuna geometria di SVG cambia.
L'unica differenza negli artefatti è **la riga di legenda stampata dentro
l'SVG**, che ora dice il vero — 17 SVG rigenerati, 66 righe, tutte di legenda.

Se invece avessimo assegnato a `⬛` il significato di «tenda» (il più frequente
nei numeri), avremmo cambiato in un colpo solo il comportamento di ogni mappa di
città e di fortezza. Il glifo generico tiene il significato **strutturalmente
più forte**, non quello statisticamente più comune.

### 3. La riclassificazione è un lavoro a parte, e dichiarato

Le 8.216 celle restano `⬛`. **Non si riscrivono in blocco**: sapere quali sono
tende, quali edifici e quali dais vuol dire leggere la mappa, non contare i
caratteri. La coda misurata sta in `LEGENDA-FUNZIONALE-SPEC` §6.2, mappa per
mappa, e si smaltisce quando quella mappa viene toccata per altri motivi.

Sospetti forti, da verificare leggendo:
`SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW` (2.173) e `campo-drow-1` (382) sono
accampamenti — quasi tutte **tende**; `tarsilia-la-ruota` (1.283 fra le due
versioni) è una città e `Hammerfist-Lotto-3` (1.256) una fortezza — quasi tutti
**edifici**; l'Altare di `ARC07` è il candidato **dais** più probabile del repo.

### 4. L'import impara i nomi

`import_ultraclear.py` usava `⬛` come default quando nessuna parola chiave
combaciava. Ora `tenda / tende / padiglione / accampamento` producono `⛺` e
`dais / pedana / piattaforma` producono `🔳`. Il default resta `⬛`, ma adesso
significa «edificio» invece che «una delle tre, chissà».

## Conseguenze

**Positive.**

- Una mappa nuova non può più dire «struttura» e lasciare al lettore di
  indovinare quale delle tre.
- Le tende disegnate col glifo giusto **bloccano finalmente la vista** nel VTT.
  Era un difetto reale, opposto e simmetrico a quello di `⛰`.
- Il dais ha un modo di esistere che non lo trasforma in un muro.

**Negative, e vanno dette.**

- **Le 8.216 celle restano ambigue finché qualcuno non le guarda.** Questa ADR
  rende la legenda corretta; non rende corrette le mappe già disegnate. Chi
  apre oggi il campo drow su Foundry trova ancora muri al posto delle tende.
- **`⛺` in `WALL_SYMS` cambia l'export** delle 93 celle che già lo usano in
  `ARC07-MAPPE-DEFINITIVO`. È il comportamento giusto, ma è un cambiamento: una
  tenda che prima si attraversava adesso no.
- **Nessun gate distingue un uso corretto da uno pigro.** Un agente può
  continuare a mettere `⬛` ovunque e la CI resta verde. Il controllo è la
  legenda e chi la legge, non una macchina — al contrario di ADR-0041, dove
  l'invariante era contabile.
- `🔳` e `⬛` **si somigliano molto** in alcuni font di sistema. Sul rendering a
  pergamena si distinguono bene (riempimento pieno contro pedana con gradino),
  ma nella griglia emoji del master markdown la differenza è sottile. È il
  prezzo di restare nella famiglia dei quadrati, che è come si legge il terreno.

## Alternative scartate

**Dichiarare `⬛` = «tenda»** e spostare edificio e dais. Segue i numeri (le
tende sono il gruppo più grande) e cambia il comportamento di ogni mappa di
città e fortezza già disegnata. Scartata: il glifo generico tiene il significato
più forte, non il più frequente.

**Riscrivere le 8.216 celle adesso, per file.** Sembra fattibile perché ogni
mappa è dominata da un significato — ma «dominata» non è «composta da»: nel
campo drow c'è anche un palizzato e una tenda di comando, e un `sed` non li
distingue. Cambierebbe gli SVG di 24 file su una supposizione.

**Un quarto glifo per «struttura generica, da classificare».** Legittimare
l'ambiguità con un simbolo apposito la rende permanente. `⬛` con un significato
preciso e una coda dichiarata è più onesto.
