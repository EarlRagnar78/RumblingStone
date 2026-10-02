# ADR-0072 — La scheda di un artefatto porta la sua immagine dentro

- **Stato**: accettata
- **Data**: 2026-09-25
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, lo stesso giorno: *«le vecchie schede
  utilizzavano un annegato nel html per lo stile, ha senso riprodurlo in
  maniera automatica per le nuove schede così si mantiene il flavour ed il
  layout»*; alla domanda sul come, *«Sì, incorporate»* (webp compresso, una
  immagine per artefatto, un test sul peso)
- **Rapporti**: estende [ADR-0071](ADR-0071-gli-artefatti-crescono-per-stadi-e-ogni-pagina-ha-una-versione.md)
  (le pagine vive sono quelle del suo registro); le immagini che mancano si
  commissionano con `rumblingstone-art-direction`

## Contesto

Le schede degli artefatti di prima degli stadi (in `Old/` e negli
`_ARCHIVIO/`) avevano l'immagine dentro l'HTML, come `data:` URI. Si
stampavano e si passavano a un giocatore come un file solo. Le avevano però
incorporate a piena risoluzione: fra 1,1 e 2,7 MB a pagina.

Le pagine degli stadi, uscite dai generatori, avevano perso quel pezzo.
Misurato il 2026-09-25 sulle 36 pagine vive del registro, su `main`: 22 senza
immagine, 12 con un `<img src="file.jpg">` che si rompe appena la pagina esce
dalla cartella, 2 con l'immagine dentro (la scheda 05 dei Bracieri, giocatore
e DM). Dopo: 27 con l'immagine messa dallo strumento, le 2 di prima, 7
mancanti dichiarate; la più pesante è 72 KB.

## La decisione

1. **Ogni pagina viva porta la sua immagine dentro**, come `data:` URI in
   webp, sotto la testata, con l'attributo `data-immagine-artefatto="<chiave>"`.
2. **Quale immagine, lo dice un dato**: `PG/Artefatti/immagini-artefatti.json`,
   con tre sezioni: le immagini (file master e testo alternativo), le pagine
   (una voce vale per la pagina del giocatore e per quella DM dello stesso
   stadio) e le **mancanti**, ognuna con la ragione.
3. **Lo scrive uno strumento**, `scripts/incorpora_immagini_artefatti.py`:
   riduce il master a 480 px sul lato lungo, lo ricomprime in webp qualità 72
   (20-60 KB invece di un megabyte) e lo inserisce o lo sostituisce. Si
   rilancia dopo ogni rigenerazione di una pagina: i generatori riscrivono
   l'HTML intero e l'immagine se ne va con lui.
4. **I master restano file** nella cartella dell'artefatto. Lo strumento li
   legge e non li tocca.
5. **Il gate** è `scripts/tests/test_immagini_artefatti.py`: fallisce se una
   pagina viva collega un'immagine come file, se supera 300 KB, se il JSON le
   assegna un'immagine che non porta, o se non ha immagine e non è fra le
   mancanti dichiarate.

## Le conseguenze

- **Quello che si guadagna**: il flavour delle schede di prima, in un file che
  si stampa o si manda da solo, a un decimo del peso.
- **Quello che si paga**: Pillow per chi rigenera (è già fra i requisiti
  opzionali; il test non ne ha bisogno), e un passo in più dopo ogni
  generatore. Se lo si salta, il test è rosso.
- **Cosa il gate non vede**: che l'immagine sia **quella giusta** per lo
  stadio. La Corona a zero, una e due gemme usa la stessa immagine a gemme
  spente, perché un'immagine per stadio non c'è; se ne arriva una, si cambia
  una riga del JSON.
- **Cosa manca**: un'immagine di Aegis Fang (nessuna nel repo) e una dei
  Bracieri dormienti. Stanno nelle mancanti del JSON, e vanno commissionate.
