# PIANO — Uno standard solo per i dati delle creature e per la stampa dei booklet

> **Stato**: 🟡 in corso (2026-10-29). Audit A1-A3 fatti, misura registrata e in CI. D5 decisa (appendice), I3 fatto, I6 e I7 in parte; primo cieco di I6 votato (box nel riquadro, interlinea non decisa) · **Classe**: C per il codice, K per i master da convertire
> **Nasce da**: la richiesta del DM del 2026-10-29, dopo la PR #295: *«uniformare tutti i master nel miglior template possibile […] e poi il miglior layout possibile per la stampa usando questo master di dati […] in una pipeline che azzera i glitch […] e sia misurabile e registri il miglioramento […] creando delle pipeline std e dei test concreti e reali e professionali che verifichino la correttezza, il miglioramento e l'aderenza agli standard professionali dell'editoria»*. Poi, sulla scheda di decisione: la #295 non si unisce, si rifà dentro questo standard (scelta B, «Fermarla»), e il layout si confronta con quello degli AP 3.5 e PF1e più apprezzati dalla community.
> **Decisioni collegate**: [ADR-0105](adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro unico, proposta, nella #295); [ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) (la catena Typst); [ADR-0070](adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md) (l'apparato non va in stampa).
> **Misura riproducibile**: `python3 scripts/misura_stampa.py --tutti`, registro in [`docs/audit/stampa-booklet.json`](../docs/audit/stampa-booklet.json).

## Dove siamo

La #295 fa metà del lavoro: le creature escono in una forma sola. Restano tre
problemi.

1. **I numeri sono scritti due volte.** Nel master c'è il blocco
   ` ```statblocco ` e sotto ci sono le righe leggibili (Difesa, Attacco…) che
   ripetono gli stessi numeri a mano. Possono divergere. Oggi lo impedisce
   solo un confronto dei numeri fatto durante la conversione.
2. **Il layout esiste in tre copie.** Typst, HTML e Homebrewery implementano
   ognuno ogni elemento (riquadro, read-aloud, tabella, nota DM, figura).
   Colori, caratteri e spaziature sono ripetuti in tre posti, e le schede dei
   PG (`scheda-pg.typ`) hanno margini propri, non speculari.
3. **La stampa si misurava solo in parte.** Fino a questo piano la CI
   controllava che il libro compilasse, che l'apparato non finisse in stampa e
   che le righe non si sovrapponessero. Non misurava corpo minimo, immagini,
   font, gabbia, riquadri spezzati.

## Prima misura (A2, 2026-10-29)

`misura_stampa.py` compila i 17 booklet e ne legge il PDF.

| Misura | Esito |
|---|---|
| Font non incorporati | 0 in tutti i booklet |
| Corpo mediano del testo | 10 pt (9 pt le schede PG del Drappo) |
| Testo oltre la gabbia dei margini | 0, tranne il titolo di copertina del Ritorno alla Forgia (1) e le schede PG del Drappo (299: margini di 1 cm, non quelli del tema) |
| Testo sotto 7 pt | 1.255 righe in 7 booklet, quasi tutte etichette di mappe SVG rimpicciolite fino a 2,5-3,9 pt; nel Drappo anche le griglie a spaziatura fissa a 6,1 pt |
| Immagini sotto 300 dpi | 222, soprattutto nell'appendice mappe di ARC-07 (strati a 72 dpi) |
| Riquadri di creatura spezzati fra due pagine | 14 su 76 riquadri stampati (Terros, la Sentinella, Fra' Timoteo…) |
| Pagine con un'immagine di almeno un quarto di pagina | 0-26%; le mappe vettoriali non contano |

Note oneste sulla misura:
- La gabbia ammette 4 pt di sporgenza: è la punteggiatura che Typst appende al
  margine di proposito.
- Gli strati sfocati che Typst rasterizza sopra un'immagine a piena
  risoluzione non contano come immagini sgranate. Quelli a 72 dpi di ARC-07
  contano, perché sotto non c'è un'immagine buona. Non ho ancora guardato a
  occhio se si vedono stampati.
- La misura compila senza i font di sistema: con quelli, il ripiego per i
  glifi che i nostri font non hanno cambiava da una macchina all'altra e la CI
  contava 1-3 righe in più del portatile. Il fatto che i booklet ricorrano a
  font di sistema (FreeSans, Unifont, Inter compaiono nel PDF) è esso stesso
  un difetto da togliere in I1.
- Vedove e orfane, e i glifi mancanti, non si misurano ancora.

## Seconda misura (2026-10-29, dopo l'appendice)

| Misura | Prima | Dopo |
|---|---|---|
| Riquadri spezzati fra due pagine | 14 | 0 |
| Testo oltre la gabbia, schede PG del Drappo | 299 | 0 (gabbia di 1 cm) |
| Testo sotto 7 pt, schede PG del Drappo | etichette a 6,x pt | 0 |
| Pagine dei volumi DM | Notte 101, Resurrezione 145, Terros 59, Palio 64 | 101, 146, 60, 65 |

Il conto delle pagine cambia di una al massimo: l'appendice occupa quanto
tolgono le righe compatte. `pagine_con_immagine_decimo` (soglia 1/10 di
pagina) è registrata senza tetto; l'obiettivo ≥ 0,3 resta di I6.

Varianti di I6 su ARC07-NOTTE-E-ALBA, tutte senza peggiorare le misure con
tetto: base 101 pagine e interlinea 1,28; interlinea stretta 92 pagine e
1,08; box da leggere colorato senza riquadro 100 pagine. Le 8 coppie
cieche sono nella cartella condivisa, `standard-stampa/cieco-2026-10-29/`.

Voto cieco del DM (2026-10-29, `VOTO.json` nella stessa cartella):

| Variante | Scelta la base | Scelta la variante | Esito |
|---|---|---|---|
| Box da leggere colorato, senza riquadro | 4 | 0 | scartata: il box resta nel riquadro |
| Interlinea stretta 1,08 | 2 | 2 | non decisa: resta 1,30 |

Quattro coppie per variante sono poche: 4 a 0 ha probabilità 1/16 di uscire
a caso. Basta per tenere il libro di sempre, non per dire che la variante è
peggiore in assoluto. L'interlinea si potrà rimettere al cieco su un altro
booklet con più coppie; il guadagno sarebbe 9 pagine su 101.

## Terza misura (2026-10-29, dopo l'unione della #295)

La rimisura su main del thread delle schede ha trovato due difetti nati
dalla colonna stretta dell'appendice, e correggendoli ne è emerso un terzo.

| Misura | Su main dopo la #295 | Dopo la correzione |
|---|---|---|
| Titoli dei riquadri spezzati con il trattino, appendici dei 7 volumi | 23 | 0 |
| Colonne dell'appendice piene meno del 60% (ultima pagina esclusa) | 5 | 4 |
| Rimandi di pagina sbagliati (nuova misura, tetto 0) | 1 (Terros, «continua a pagina 60») | 0 |
| Impaginazioni che non convergono (ora fanno fallire la misura) | 0 | 0 |

Le 4 colonne che restano sotto il 60% sono colonne di destra seguite da una
scheda che non ci sta: continuarla nella pagina dopo vorrebbe dire
spezzarla a pagina girata, che il criterio WotC esclude. Le toglierebbe solo
un ordine diverso dall'alfabetico.

## Decisioni proposte

- **D1. Dati una volta sola.** La creatura diventa un dato con uno schema, come
  già le schede dei PG in `PG/schede/*.yaml`. Lo schema copre 3.5 e PF1e
  (BMC/DMC, Percezione), capacità, incantesimi, tattiche, fonte e marcatori di
  canone. Le righe leggibili si generano dal dato.
- **D2. Un layout, tre uscite.** Il markdown diventa una rappresentazione
  intermedia di elementi tipizzati. I tre renderer partono da quella. Colori,
  caratteri e misure stanno in un solo file di token letto da Typst e dal CSS.
- **D3. Varianti di layout misurate.** La pipeline scarta le varianti con
  errori misurabili. Fra quelle senza errori sceglie il DM alla cieca, come per
  la prosa.
- **D4. Un registro.** Ogni booklet ha i suoi tetti di stampa in git, che
  scendono soltanto. ✅ attuato con `docs/audit/stampa-booklet.json`.
- **D5. Dove sta la scheda intera** (decisa dal DM il 2026-10-29, scelta
  «Appendice»): le schede intere delle creature vanno in un'appendice in fondo
  al volume, come in *Red Hand of Doom*. Nell'incontro restano una riga con il
  rimando alla pagina e la **tattica di quell'incontro**: se un PNG cambia
  tattica nel tempo, o lo si incontra in stanze o luoghi diversi, ogni
  incontro porta la sua. Cambia ADR-0105, che oggi mette il riquadro intero a
  ogni comparsa. Dal confronto con Paizo, arrivato dopo la decisione: *Burnt
  Offerings* non usa l'appendice ma un ibrido. La scheda intera sta alla prima
  comparsa del PNG unico, poi c'è «vedi pagina N», e il Bestiario in fondo
  serve solo ai mostri nuovi. Anche lì la tattica sta nell'incontro.

## Fase 1 — Audit

- [x] **A1** I riferimenti: gli AP 3.5 e PF1e più premiati e più citati per
  l'impaginazione, e 15 criteri misurabili (C1-C15). Ricerca nella cartella
  condivisa `standard-stampa/RIFERIMENTI-AP.md`; Reddit e archive.org erano
  chiusi dal proxy.
- [x] **A2** La prima misura di stampa dei 17 booklet, in CI con i tetti.
- [x] **A3** Il confronto con le pagine degli AP di riferimento. Lato Paizo
  fatto il 2026-10-29 (thread «Confronto layout con gli AP»): cinque pagine
  ciascuno della Player's Guide di CotCT e di cinque moduli Free RPG Day,
  tutti PDF gratuiti, tenuti fuori dal repo. Contro ARC-07 Notte e Alba,
  Paizo ha il corpo a 8,5 pt contro 10, l'interlinea a 1,41 contro 1,30, circa
  30 righe per colonna contro 26,5, le schede allo stesso corpo del testo
  contro 9,5-10, e soprattutto 0,7 pagine con un'illustrazione grande contro
  0,09. Sotto 7 pt Paizo ha solo fregi, marchi e licenza, quindi la soglia
  regge. Sono moduli, non volumi di AP, e cinque pagine sono poche.
  Dettaglio in `standard-stampa/CONFRONTO-AP-2026-10-29.md` nella cartella
  condivisa. Lato WotC, solo schede (stesso giorno): le 100 schede della Web
  Enhancement di *Red Hand of Doom* (caricata dal DM il 2026-10-18) contro
  ARC-07 col riquadro nuovo. Corpo 9 pt uguale, densità per pagina uguale;
  interlinea 1,11 contro 1,24; **righe della scheda da 46 caratteri (Paizo
  31-45) contro 106 nostre**; schede spezzate 3 su 100, sempre con
  «(encounter continues on page N)», contro 14 su 76 senza rimando. Dettaglio
  in `standard-stampa/CONFRONTO-WOTC-2026-10-29.md`. Resta fuori la prosa
  WotC: web.archive.org, drivethrurpg e dmsguild sono chiusi anche dai thread
  nuovi. Poi, alle 15:05, 18 pagine interne della copia di *Red Hand of Doom*
  del DM: testo a 9,75 pt, interlinea 1,10, 61 caratteri per riga (noi 10 pt,
  1,30, 59), circa 4.650 caratteri per pagina (noi 3.570). Il box da leggere
  è corsivo colorato nel testo, senza riquadro (14,5% del testo). Immagini:
  con la soglia di ¼ di pagina WotC 0,06 contro noi 0,09, con la soglia di
  1/10 WotC 0,50 contro noi 0,18. Nel libro le schede intere stanno
  nell'appendice; nell'incontro c'è una riga sola col rimando.
  Infine, lo stesso giorno, un AP Paizo intero comprato dal DM, *Burnt
  Offerings* (100 pagine, 3.5), misurato tutto al posto dei campioni
  gratuiti. Testo a 9 pt, interlinea 1,33, 63 caratteri per riga, circa
  4.350 caratteri per pagina, niente sotto 7 pt: il campione dei moduli
  (8,5 pt e 1,41) non rappresentava l'AP. Il box da leggere è sans marrone
  nel testo, senza riquadro (12%). Le righe della scheda sono da 31-34
  caratteri, e la tattica sta sempre nell'incontro, anche sotto la riga col
  rimando. Ci sono 15 schede intere negli incontri dove il PNG unico si
  combatte e 6 nel Bestiario in fondo, solo per i mostri nuovi. Altre 28
  righe rimandano al Monster Manual, al Bestiario o a una scheda
  precedente. Si spezzano 9 schede su 15, 3 a pagina girata e senza
  «continua»; 8 su 15 hanno accanto il ritratto del PNG. Con lo stesso
  metodo raster su tutti e due, Paizo ha il 24% di pagine con
  un'illustrazione di almeno ¼ e il 40% con una di almeno 1/10, con il 17%
  di area illustrata. ARC-07 ha 10%, 17% e 5,7%. Dettaglio in
  `standard-stampa/CONFRONTO-PAIZO-AP-2026-10-29.md`.
- [ ] **A4** Il censimento degli elementi di layout nei tre renderer e delle
  forme dei dati (Bestiario, master, PG, Drappo PF1e).

## Fase 2 — Implementazione, a PR piccole

- [ ] **I1** File dei token di stile, letto da Typst e dal CSS. La misura deve
  restare uguale.
- [x] **I2** Le etichette delle mappe non scendono sotto il corpo minimo: la
  scala della figura decide la dimensione delle etichette nel renderer.
  Fatto con la #298 e ADR-0106: ogni mappa del repo ha la pianta in stampa
  (`rendered-stampa-pianta/`, scritte a 7,4 pt, niente filtri) e i booklet
  usano solo quella. Nei tre volumi di ARC-07 le righe sotto 7 pt passano da
  217/256/217 a 0.
- [x] **I3** Il riquadro che si spezza ripete la testata con «(continua a
  pagina N)», come fa WotC, oppure passa intero alla colonna dopo quando è
  più corto di una colonna. Fatto nella #295 insieme a D5: le schede intere
  stanno nell'appendice delle creature, in ordine alfabetico, e una scheda
  più corta di una colonna non si spezza mai. Una più lunga ripete il nome
  con «(segue)» in testa e chiude con «continua nella colonna accanto» o
  «continua a pagina N»; se è più lunga di due colonne parte da una pagina
  pari, così non si spezza a pagina girata. Nell'incontro resta una riga con
  GS, CA, pf, il rimando alla pagina della scheda e la tattica di quel
  momento. I volumi dei giocatori tengono le schede dove compaiono
  (`"schede": "qui"` nel manifest).
- [ ] **I4** Schema della creatura e generatore delle righe leggibili.
  Migrazione a lotti: ARC-07 e il Bestiario, poi il resto.
- [ ] **I5** Rappresentazione intermedia e renderer unici, un elemento alla
  volta, con il confronto visivo delle pagine.
- [~] **I6** Varianti di layout e scelta alla cieca del DM. Dal confronto
  di A3: il corpo resta a 10 pt; si provano le schede a 9 pt e l'interlinea
  a 1,35-1,4; `pagine_con_immagine` resta registrata senza tetto, con
  obiettivo ≥ 0,3. Dal lato WotC: una variante «scheda in colonna», un
  campo per riga e righe da 40-60 caratteri, contro il riquadro largo di
  oggi; le fasce colorate al cieco. Interlinea fra 1,10 (WotC) e 1,33
  (Paizo, AP intero): decide il cieco. Una variante del box da leggere senza
  riquadro, colorata, come fanno tutti e due gli AP. `pagine_con_immagine`
  misurata anche con la soglia di 1/10 di pagina, ed è lì l'obiettivo ≥ 0,3
  (Paizo 0,40, noi 0,17). Il divario viene soprattutto dal ritratto del PNG
  accanto alla sua scheda, che appartiene al lavoro delle immagini
  (ADR-0104). Criterio per le schede spezzate (modello WotC, deciso dal
  thread padre il 2026-10-29): nessuna scheda spezzata a pagina girata, e
  ogni scheda che si spezza porta il «continua».
- [~] **I7** Le schede PG del Drappo nello stesso tema. Prima parte nella
  #295: le etichette sotto 7 pt salgono a 7 pt e le schede si misurano con
  la loro gabbia di 1 cm (geometria `scheda`), quindi 0 righe fuori margine
  invece di 299. Resta da portarle nel tema comune.

## Fase 3 — Validazione

- [ ] **V1** Ogni PR mostra le misure prima e dopo; nessuna sale (la CI lo fa
  rispettare dal 2026-10-29).
- [ ] **V2** Confronto visivo pagina per pagina con la versione approvata.
- [ ] **V3** Una stampa di prova di un fascicolo su carta, guardata dal DM.

## Cosa manca e cosa si assume

- Dove stampa il DM: si assume casa o copisteria, A4, senza abbondanza, RGB.
  Una tipografia chiederebbe abbondanza di 3 mm, CMYK e PDF/X.
- Formati: si assume A4; A5 c'è già nel tema per i libretti.
- Le pagine degli AP per A3: dal DM o dalle fonti legali che si raggiungono
  dall'ambiente.
