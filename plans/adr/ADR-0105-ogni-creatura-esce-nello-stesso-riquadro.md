# ADR-0105 — Ogni creatura esce in stampa nello stesso riquadro

**Stato**: proposta
**Data**: 2026-10-29
**Decisione-fonte**: il DM (Jfs), 2026-10-29, sfogliando i booklet: *«perché i png i villan i mostri e gli altri pg che compaiono nello ap hanno sempre layout visivi diversi per esempio non so i draghi sembrano parti di testo mentre i png e forse boss minori hanno un layout grafico migliore […] possiamo rendere il layout uniforme per tutti i tipi di creature e png villan e mostri in modo che seguano lo stile layout migliore possibile misurando questo miglioramento anche nei booklet che vengono stampati?»*
**Rapporti**: completa [ADR-0021](ADR-0021-statblocchi-machine-readable.md) (i numeri sono un blocco) e [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) (la scheda si legge in Difesa, Attacco, Statistiche, Capacità speciali, Tattiche), che fissavano la forma nel sorgente e non sulla carta; usa il tema di [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md). Il numero 0104 resta al thread delle immagini dei personaggi in posa, che lo ha proposto senza prenotarlo.

## Contesto

La stampa non decideva nessuna forma: copiava quella del master. Solo il
recinto ` ```statblocco ` diventava un riquadro, e solo nel PDF; l'HTML e
Homebrewery lo mostravano come codice. I master scrivevano le statistiche in
cinque modi, e ognuno arrivava in pagina così com'era:

| Forma nel master | In stampa | Esempio prima di questa decisione |
|---|---|---|
| recinto ` ```statblocco ` | un riquadro coi campi in fila | Balvar nel volume |
| recinto qualunque con un cartiglio di `====` | testo a spaziatura fissa | Skullcrusher, Terros, Hella |
| paragrafo con i numeri in grassetto | un paragrafo, come la prosa | Xorn, Sentinella, Durin |
| riga di tabella | una riga di tabella | |
| righe di ADR-0091 staccate dal recinto | due paragrafi | il Bestiario incluso nei master |

Il drago che sembrava «testo» era la forma a spaziatura fissa; il PNG che
sembrava curato era il recinto. La misura del 2026-10-29 su `main`
(`scripts/misura_statblocchi_booklet.py`) dava 4 schede su 79 nel riquadro, il
5%, in nove booklet.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Un riquadro a fasce, alimentato dal recinto e dalle righe di ADR-0091, uguale in PDF, HTML e Homebrewery; le schede si convertono nei master; una misura con un tetto per booklet** (scelta) | una forma sola, dal goblin al drago; i numeri restano nel blocco che i controlli già leggono; la misura dice quanto manca | la conversione è lavoro a mano, scheda per scheda; un riquadro lungo (Terros) occupa più di una colonna |
| Riconoscere in stampa le forme libere e ridisegnarle | nessun master da toccare | cinque parser fragili; un paragrafo che cita una CA per spiegarla diventerebbe un riquadro; i numeri resterebbero fuori dal blocco |
| Solo uno stile più curato per il testo a spaziatura fissa | poco lavoro | le forme restano cinque; i paragrafi in prosa restano prosa |
| Lasciare la forma ai master | nessun lavoro | è la situazione che il DM ha visto |

Per il punto 7 (dove sta il riquadro):

| Opzione | A favore | Contro |
|---|---|---|
| **Appendice in fondo, nell'incontro una riga col rimando e la tattica** (scelta del DM, modello WotC) | le pagine dell'incontro restano corte; una creatura ha un solo riquadro da tenere giusto | al tavolo si gira pagina per i numeri |
| Riquadro alla prima comparsa, poi «vedi pagina N» (modello Paizo, *Burnt Offerings*) | i numeri sono dove si combatte la prima volta | la prima comparsa dipende dall'ordine di lettura, non di gioco |
| Riquadro intero a ogni comparsa (la prima versione di questo ADR) | nessun rimando | più pagine e più riquadri spezzati; lo stesso riquadro ripetuto può divergere |

## Decisione

1. **Il riquadro è uno.** Barra col nome e il GS, riga del tipo, riga di
   iniziativa e sensi, poi le fasce **Difesa**, **Attacco**, **Statistiche**
   (con la griglia delle sei caratteristiche quando ci sono tutte e sei),
   **Capacità speciali**, **Tattiche**, come nei blocchi di *Red Hand of Doom*
   e dei Bestiari PF1e. La stessa forma esce dal tema Typst
   (`#statblocco` in `scripts/typst/tema-rumblingstone.typ`), dall'HTML
   (`statblocco_html` in `build_booklet_html.py`) e da Homebrewery
   (`{{monster,frame}}`).
2. **Il riquadro si riempie dal master.** Le fasce prendono le righe di
   ADR-0091 che seguono il recinto, quando ci sono; altrimenti i campi del
   blocco, in riga e separati da « · ». `sezioni_leggibili` in
   `dmcore/statblock.py` le legge; `accosta_parte_leggibile` riporta sotto il
   recinto le righe che nel Bestiario stanno dopo le note.
3. **Il campo `gs` dice cosa stampare.** Un numero (o `~10`) esce come
   «GS 10»; un testo come «PG di 13°» esce com'è; «—» non esce. Così entrano
   nel riquadro anche i PG, le forme dei PG e i costrutti senza GS dichiarato.
4. **`#scheda` è l'ancora di inclusione per la stampa**: `componenti.py`
   copia il recinto più le righe di ADR-0091 e mette nel blocco il nome dal
   titolo della scheda. `#statblocco` resta per chi vuole solo i numeri.
5. **Le schede si convertono nei master, senza toccare i numeri.** Ogni
   conversione passa un confronto dei numeri fra prima e dopo; quel che è
   regia per il tavolo (il contro-momento di Thorik contro Terros, i conti, la
   nota «Non SRD», il registro del potenziamento) resta fuori dal riquadro,
   subito sotto.
6. **La misura è uno script con un tetto per booklet.**
   `misura_statblocchi_booklet.py` conta le schede di ogni booklet e la forma
   in cui escono; `--stampa` conta i `#statblocco(` nel sorgente Typst, la
   prova che il riquadro arriva sulla carta. I tetti stanno in
   `docs/audit/statblocchi-booklet.json` e scendono soltanto (`--aggiorna`);
   la CI esegue `--check`.
7. **Il riquadro intero sta in appendice, la tattica nell'incontro** (D5 del
   [piano dello standard di stampa](../PIANO-STANDARD-STAMPA.md), decisa dal
   DM il 2026-10-29: *«allora C ma la tattica del particolare incontro rimane
   dove compare»*). Ogni volume raccoglie i riquadri interi delle sue creature
   in un'appendice in fondo, come *Red Hand of Doom*. Nel punto
   dell'incontro restano una riga col nome, il GS e il rimando alla pagina
   dell'appendice, e la tattica di quell'incontro. Un PNG che cambia tattica
   nel tempo, o che si incontra in stanze o luoghi diversi, porta una tattica
   per ogni incontro. Il riquadro non si ripete più a ogni comparsa.
   Nel tema: la riga dell'incontro ha nome, GS, CA, pf, «scheda a pagina N»
   e la fascia Tattiche; l'appendice (`appendice-creature`) mette i riquadri
   in ordine di nome, a due colonne, uno per creatura (stesso nome e stessi
   numeri; la tattica non conta). Un riquadro non si spezza; quello più alto
   di una colonna comincia in cima a una pagina, o su una pagina pari se è
   più alto di due, porta «continua nella colonna accanto» o «continua a
   pagina N» in fondo e il nome con «(segue)» in cima al pezzo dopo, come
   *Red Hand of Doom*. HTML e Homebrewery fanno lo stesso, con un
   collegamento al posto del numero di pagina. Un manifest con
   `"schede": "qui"` tiene i riquadri dove sono scritti.

## Conseguenze

- Misura dopo la conversione di ARC-07 (DEF-1, DEF-3, DEF-4 e il foglio di
  Hella): 45 schede su 83 nel riquadro, il 54%, e tutti e cinque i booklet di
  ARC-07 al 100%, contro 4 su 79 prima. Le schede contate sono di più perché
  alcune guardie e comparse, prima citate in una riga, ora hanno un riquadro.
- Restano fuori il Palio, l'Abbazia della Rotta Sicura e il Drappo di
  Tarsilia (38 schede): i loro tetti valgono il conto di oggi e scendono con
  la loro conversione.
- Una scheda nuova in un booklet fa salire il conto: se non è in un recinto
  ` ```statblocco `, la CI la ferma.
- La misura riconosce le forme libere per indizi (CA, pf, e i TS o un attacco
  coi dadi). Un paragrafo di regia che cita i numeri di una creatura può
  contare come scheda; i paragrafi di conto con un'apertura fissa no. Per
  questo il cancello è un tetto e non un obbligo a zero.
- Non misura la leggibilità: dice che la forma è una, non che è bella. Quella
  la giudica il DM sulle pagine di prima e dopo.

- Col punto 7 l'appendice diventa un elemento del volume: il generatore la
  compone dai recinti dei master, e la misura dei riquadri spezzati la conta
  lì. È lavoro del piano dello standard di stampa (I3, I4), non di questa PR.

## Da rivedere se

- il DM, sfogliando le pagine, trova il riquadro meno leggibile delle forme
  di prima per una famiglia di creature (i draghi, i PG);
- un booklet nuovo ha bisogno di una forma che il riquadro non regge (un
  mostro con due forme, un esercito);
- al tavolo girare pagina per l'appendice costa più del previsto: si
  riprende il modello Paizo del punto 7;
- i master del Drappo, che è PF1e, chiedono campi che il blocco non ha
  (BMC e DMC).

## Seguito del 2026-10-30: le mappe grandi nel booklet (tema stampa)

**Contesto.** Con M7-H (44×40) nell'Appendice D di DEF-4, i tre volumi di
ARC-07 prendevano +98 righe sotto 7 pt e +9 immagini sotto 300 dpi: la mappa
entra nella pagina solo a scala 0,3, e Typst rasterizza i filtri della
pergamena a 288 dpi. Alzare i tetti era la via più breve; Jfs ha scelto di
rifare le scritte.

**Decisione.** Un modo di stampa per ogni tema delle mappe (`--stampa`,
`rendered-stampa-<tema>/`), adottato una mappa alla volta: corpi in punti per la gabbia A4 (17,5 cm),
mai sotto 7,4 pt; indicazioni e legenda in un secondo SVG sulla pagina dopo;
zone con una lettera; nessun filtro né vignettatura. Alternative scartate:
alzare i tetti (il difetto restava), dividere la mappa in quarti (quattro
pagine e la legenda ripetuta), rasterizzare la mappa (le scritte piccole
sparivano dalla misura senza diventare leggibili).

Al cieco del 2026-10-30 fra pergamena, texture e pianta, tutte e tre dentro
i tetti, Jfs ha scelto la pianta (lo stile di Dauth, ADR-0102): scala in
metri, raggio delle luci, teli chiari distinti dal terreno.

**Conseguenze.** I tetti dei tre volumi non salgono. Le mappe di stampa
perdono grana e ombre sfumate. M7-H e M7-C sono le prime; le altre mappe
sotto 7 pt (I2) possono passare allo stesso modo quando si rifà il loro
booklet.
