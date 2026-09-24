# ADR-0027 — `pdfcpu` come seconda dipendenza binaria, e la regola di degradazione

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: DM, lotto F2 di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md):
*«Sì, con ADR»*
**Precedente**: [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md)
(un binario, non un toolchain) · **Sblocca**: H3 (imposizione)

## Contesto

La catena di stampa produce **un volume**: pagine A4 in ordine, con segnalibri.
Chi lo porta in copisteria ottiene una **risma**. Un libretto (le pagine
riordinate a due a due sul foglio, piegate e cucite al centro) richiede
l'**imposizione**, che è un riordino geometrico: pagina 1 accanto all'ultima,
2 accanto alla penultima, e così via.

Typst non la fa, e farla a mano nel tema significherebbe reimplementare la
segnatura dentro il documento, cioè legare l'**ordine di stampa** al **contenuto**.
È esattamente il confine che ADR-0003 tiene: il markdown è il master,
l'impaginazione è un artefatto, e la piegatura è un artefatto dell'artefatto.

`pdfcpu` fa `booklet` nativamente, è Apache-2.0, è un **eseguibile Go statico**
senza dipendenze di sistema, e ha una modalità offline esplicita. È la stessa
forma di dipendenza che ADR-0020 ha già accettato per `typst`.

## Decisione

**Si accetta `pdfcpu` come seconda dipendenza binaria**, opzionale, per la sola
imposizione, e si scrive **una volta sola**, in codice, la regola che finora
esisteva a parole.

### 1. La regola di degradazione pulita — `scripts/binari.py`

> Se il binario manca, lo script dice **come installarlo** ed **esce**.
> Non fallisce a metà.

Fallire a metà è il modo in cui una dipendenza opzionale diventa un problema di
fiducia: un PDF di 40 pagine su 96, scritto e troncato, indistinguibile da uno
buono finché non lo si apre, la sera prima della sessione. Perciò:

- `binari.esigi(B)` restituisce il percorso **oppure** stampa e alza `SystemExit`;
  non restituisce `None` a un chiamante che «poi decide», perché è nel *poi
  decide* che il file di destinazione è già stato aperto;
- l'uscita è **2** (`binari.MANCA`), **distinta da 1**. Due dice *«non ho
  nemmeno cominciato: manca uno strumento»*; uno dice *«ho provato e non ci sono
  riuscito»*. Non sono la stessa notizia, né per la CI né per chi legge;
- ogni binario dichiara il suo **ripiego**: cosa resta possibile senza. Una
  dipendenza senza ripiego dichiarato è obbligatoria e finge di non esserlo.
  Per `pdfcpu`: *il PDF da stampa resta valido e stampabile pagina per pagina;
  l'imposizione è un di più per chi rilega.*

La regola sta in un posto solo e ha **due utenti**: `typst` è stato portato sopra
lo stesso helper nello stesso commit, perché una regola con un solo utente non è
una regola, è un caso particolare.

### 2. Come si invoca

Sempre con `-c disable` e `-o`. Non è pedanteria:

- **`-c disable`**: al primo avvio `pdfcpu` **scrive** `~/.config/pdfcpu/` e vi
  installa un font («installing user font: Roboto-Regular»). Uno strumento della
  catena non deve modificare la macchina di chi lo esegue;
- **`-o`** (offline) disabilita il traffico HTTP. Stessa ragione di
  [ADR-0026](ADR-0026-vendoring-pacchetti-typst.md): la rete non entra nella build.

### 3. Cosa è stato verificato, non supposto

Su `ARC07-TEASER-GIOCATORI-STAMPA.pdf` (3 pagine A4), `pdfcpu v0.11.0`:

- **funziona**: 3 pagine → **2 fogli** A4, stile `n=2`, exit 0. Il conto torna
  (3 arrotondato a 4, quattro pagine su due facciate);
- ⚠️ **l'output NON è byte-identico fra due esecuzioni**, e questo va detto
  perché ADR-0020 promette determinismo. Misurato: due file, md5 diversi. La
  differenza è **la seconda metà dell'array `/ID`**, l'identificatore di
  revisione, che `pdfcpu` rigenera a ogni scrittura, più la lunghezza dello
  stream XRef che ne dipende. **`CreationDate` e `ModDate` sono identici**
  (ereditati da Typst, già deterministici), e i **flussi di contenuto delle
  pagine hanno lo stesso md5**, pagina per pagina.

  Quindi: **il documento è deterministico, il file no.** Ne segue la regola
  d'uso: un PDF imposto **non si versiona e non si confronta a byte**: è un
  artefatto di consegna, prodotto al momento della stampa. Il confronto
  riproducibile resta quello sul volume, che è il file che ADR-0020 governa.

## Conseguenze

**Buone.**
- H3 è sbloccato: un libretto da piegare invece di una risma.
- Il compagno di questa decisione è `export_booklet_typst.py --formato a5`
  (2026-09-03): imporre un volume **già** A4 mette due pagine per foglio e
  scala tutto al 71%, cioè porta il corpo da 10.2 pt a ~7,2. Comporre in A5 a
  una colonna (9.6 pt) e poi imporre lascia il testo leggibile. Le due cose
  stanno accanto: l'imposizione piega, il formato decide *cosa* si piega.
- La regola di degradazione esiste in codice e ha dei test; prima era una frase
  in un piano, e una frase in un piano non ferma nessuno.
- `typst` ci ha guadagnato: il suo messaggio d'installazione era duplicato nello
  script, ora è una voce sola accanto all'altra, con licenza e ADR dichiarati.

**Il prezzo, dichiarato.**
- **Una seconda cosa da installare** per chi rilega. È opzionale, e il messaggio
  lo dice.
- **Il PDF imposto non è riproducibile a byte.** Sta scritto qui, ed è il motivo per cui quei file non entrano nel repo.
- `pdfcpu` è un progetto vivo: le opzioni di `booklet` possono cambiare. La
  versione usata (`v0.11.0`) va citata dove si invoca, come per typst in CI.

**Cosa NON decide.** Non apre la porta a una terza dipendenza binaria: la terza
sarà un'altra decisione, con lo stesso onere: licenza aperta, eseguibile
singolo, ripiego dichiarato, e una riga in `binari.TUTTI`.
