# Lo standard del volume: misura dei riferimenti e dei nostri booklet (2026-11-10)

Blocco 1-bis della roadmap, ADR-0122. Domanda del DM del 2026-11-09: gli AP di
carta hanno un'introduzione per capitolo, mappe con le chiavi d'area vicino alla
descrizione, un'appendice su regione e PNG. È uno standard di fatto? Noi quale
seguiamo, con che criteri e con che misure? Decisione del DM dello stesso giorno:
**schema Paizo come base, schede in appendice come *Red Hand of Doom***.

Strumento: `python3 scripts/misura_distanza_pagine.py --volume` (lo script della
distanza esteso, non uno nuovo). Soglie in `docs/audit/volume-booklet.json`.

## 1. I riferimenti

| | *Burnt Offerings* (Paizo 2007, 100 pp.) | *Red Hand of Doom* (WotC 2006, estratto di 22 pp.) |
|---|---|---|
| PDF | comprato dal DM, sha256 `79ac9236…`, fuori dal repo | comprato dal DM, sha256 `4ef9e4e2…`, fuori dal repo |
| **S1** introduzione di capitolo | 4 parti su 4, da 574 a 4.366 caratteri prima del primo sottotitolo; *Adventure Background* e *Synopsis* in testa | Parte I: 1.320 caratteri prima di *Adventure Start*; *Adventure Background* e *Outline* nell'introduzione |
| **S2** chiavi testo ↔ mappa | 88 codici su 91 del testo stanno sulla mappa (96,7%); 0 codici solo sulla mappa. Fuori: C24-C26 (tesoro e grotte marine, senza pianta) | 9 su 9 (Drellin's Ferry) |
| **S3** descrizione entro una pagina dalla mappa | **54,5%**, mediana 1 pagina, massimo 8 | 100%, mediana 0: le mappe d'incontro stanno nella pagina dell'incontro |
| **S4** appendice | 22 pp. di regione (Sandpoint, Thassilon) e 11 di creature e personaggi su 100 | non misurabile sull'estratto (la regione sta nell'introduzione) |
| **S5** PNG principali con ritratto | 8 su 15 (misura del 2026-10-29) | non misurabile sull'estratto |

Come sono state lette le mappe: le etichette sono raster calligrafiche e l'OCR
non le legge (tesseract 5.3: 4 codici su 23 sulla pianta più leggibile, 0 su
due piante). Le chiavi sono trascritte a vista una volta, pagina per pagina, in
`riferimenti/*.json`; da lì il conto è lo stesso codice che misura i nostri
booklet. Numeri grezzi in `riferimenti-misura.jsonl`.

**La sorpresa che conta**: Paizo non mette ogni descrizione a una pagina dalla
mappa. Mette la pianta in testa al luogo e poi descrive le aree per 4-10
pagine (Thistletop: mappa a p. 34, aree fino a p. 42). Solo metà delle aree
sta entro una pagina. RHoD, con le mappe piccole dentro l'incontro, sta al
100%. La soglia S3 è quindi il valore più basso dei due, 54%: chiedere «sempre
entro una pagina» sarebbe più severo dello standard che si vuole seguire.

## 2. I nostri booklet del DM (main f65d78e, compilati come `misura_stampa`)

```
volume                                      pag  S1 intro S1 vol   S2 cod  S3 ≤1p S3 nome S4 reg/png  S5 ritr
ARC07-NOTTE-E-ALBA-BOOKLET                  158       1/8     sì      0/0       —      8%        0/3      4/4
ARC07-SERATA-RESURREZIONE-BOOKLET           172       0/6     sì      0/8       —      9%        0/4      4/4
ARC07-RITORNO-FORGIA-BOOKLET                 29       1/2     sì      0/8       —     13%        0/0      0/0
ARC07-SESSIONE-TERROS-BOOKLET                65       2/9     sì      0/0       —     12%        0/3      0/1
ARC07-MILLE-ANNI-VOLUME                     105       0/4     no      0/0       —     11%        0/4      4/4
PALIO-BOOKLET                                65      7/16     no      0/0       —       —        0/1      0/0
giardino-sale-calce                          40       1/2     sì     0/17       —      4%        0/2      0/0
giardino-sale-calce-pf1e                     25       1/2     sì     0/14       —      4%        0/2      0/0
DRAPPO-BOOKLET-DM                            87      6/18     no      0/8       —       —        0/2      0/0
abbazia-rotta-sicura                         43       1/1     sì      0/0       —       —       0/14      0/0
```

36 misure sotto soglia su 10 booklet; nessun booklet le passa tutte. Per misura:

- **S1**: i capitoli dei booklet di serata aprono con «Chi si incontra in questo
  capitolo» o con il frontespizio del master incluso, non con un'introduzione.
  20 capitoli su 68 superano i 500 caratteri, 13 dei quali nel Palio e nel Drappo.
  Il volume ha un antefatto o una sintesi in 7 booklet su 10.
- **S2**: **nessuna nostra mappa stampa le chiavi d'area.** Le piante (ADR-0106)
  hanno la griglia (A-AR, 01-40), i segnalini numerati dei personaggi e la
  legenda nella pagina dopo, ma non «A1», «B3». Il testo invece usa chiavi in 5
  booklet (Giardino A1-G7, Resurrezione A1-A8…). Le due metà non si parlano.
- **S3**: non si misura sulle chiavi, che mancano; sulla citazione per nome
  («M7-C», «GS-1») la pagina che cita la mappa sta a una pagina da lei nel
  4-13% dei casi (riferimento 54%). Drappo, Palio e Abbazia hanno mappe raster
  o nessuna pianta riconoscibile: «—».
- **S4**: l'appendice dei PNG c'è (le creature, ADR-0105 D5); **l'appendice sulla
  regione non c'è in nessun booklet**.
- **S5**: dove si misura, 12 PNG principali su 13 hanno il ritratto vicino ai
  numeri (ADR-0107 funziona). Nei moduli stand alone la misura non trova PNG
  principali: i loro riquadri non sono fra quelli del repo che lo script legge.
  Non vuol dire che vadano bene, vuol dire che non è misurato.

## 3. Cosa la misura non sa, dichiarato

- S1 conta i caratteri, non se sono un'introduzione vera. Un capitolo che apre
  con il titolo del master incluso (VI di *Notte e Alba*: 17 caratteri, poi
  «Il Portale della Forgia Eterna…» e il QUICKSTART) conta come senza intro.
- S2 da noi legge i codici dei titoli dell'indice del PDF: nel Drappo «A1 · La
  ricevuta» è un indizio, non un'area, e conta lo stesso (8 codici così).
- S3 per nome conta ogni pagina che cita la mappa, anche un rimando di regia.
- Le soglie vengono da due riferimenti, uno dei quali è un estratto. Sono un
  punto di partenza dichiarato, non una legge.

## 4. Che cosa segue

La misura dice dove i nostri booklet sono lontani dallo standard scelto. Il DM
ha chiesto (2026-11-10) di **scegliere lui prima di togliere qualcosa**, con le
card che dicono dove va ogni contenuto di oggi, e poi una versione del booklet
centrata sullo svolgimento della serata, misurata contro l'attuale. Il canale
resta testing finché quelle scelte non sono fatte.
