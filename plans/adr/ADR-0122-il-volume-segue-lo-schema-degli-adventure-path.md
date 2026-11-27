# ADR-0122 — Il volume segue lo schema degli Adventure Path, misurato sul PDF

**Stato**: proposta (2026-11-10)
**Data**: 2026-11-10
**Decisione-fonte**: il DM (Jfs), 2026-11-09, nel thread dell'audit: schema Paizo come base, con le schede in appendice come in *Red Hand of Doom*. Blocco 1-bis della roadmap. Il 2026-11-10: prima di togliere qualcosa dai booklet decide lui, con card che dicono dove va ogni contenuto; poi una versione del booklet centrata sulla serata.
**Rapporti**: completa [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) e [ADR-0106](ADR-0106-ogni-mappa-si-stampa-in-pianta.md) (lo standard della pagina) con lo standard del volume. Usa [ADR-0107](ADR-0107-chi-si-incontra-sta-nel-capitolo.md) per S5 e [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) per il canale. Segue la regola del DM «prima lo standard di fatto, la soluzione nostra solo se la misura lo boccia».

## Contesto

Lo standard della pagina è definito e misurato in CI (`misura_stampa`, criteri
C1-C15). Lo standard del **volume** no: nessuno script diceva se un capitolo
apre con un'introduzione, se le chiavi d'area del testo sono sulla mappa, se la
mappa sta vicino alla descrizione, se in fondo c'è l'appendice su regione e
PNG. Il DM li ha visti negli AP di carta (RHoD, *Rise of the Runelords*) e ha
chiesto se esiste uno standard di fatto e quale seguiamo, con quali misure.

Lo schema Paizo (*Adventure Background*, *Synopsis*, le *Part* con
un'introduzione, le aree con chiave A1-E10, gli articoli di supporto in fondo)
è lo stesso in ogni volume di AP dal 2007 al 2019: è lo standard di fatto più
costante e documentato per 3.5 e PF1e. RHoD ha gli stessi elementi tranne gli
articoli di supporto, e ha le schede in appendice, già scelte con ADR-0105 D5.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Schema Paizo + schede in appendice come RHoD, misurato sul PDF** (scelta) | lo standard di fatto, scelto dal DM; si misura sul volume stampato come gli AP, quindi riferimenti e nostri booklet passano dallo stesso codice | le mappe dei riferimenti sono raster: le loro chiavi si trascrivono a vista una volta |
| Schema WotC (RHoD) puro | mappe d'incontro nella pagina dell'incontro (S3 al 100%) | senza articoli di supporto; l'unico riferimento WotC è un estratto di 22 pagine |
| Misurare il markdown dei master invece del PDF | niente compilazione | non misura ciò che il DM sfoglia (capitoli portati, copie delle mappe, appendice); i riferimenti esistono solo in PDF |
| Uno script nuovo | separato dalla distanza dei numeri | il brief chiede di estendere `misura_distanza_pagine.py`, che legge già il PDF con PyMuPDF |
| OCR per le chiavi delle mappe di carta | nessuna trascrizione a mano | provato: tesseract 5.3 legge 4 codici su 23 sulla pianta migliore e 0 su due altre (etichette calligrafiche) |

## Decisione

Il volume del DM segue lo schema degli Adventure Path, e cinque misure lo
controllano sul PDF stampato: `misura_distanza_pagine.py --volume`.

| | misura | soglia (dai riferimenti) |
|---|---|---|
| **S1** | caratteri fra il titolo di un capitolo e il primo sottotitolo; antefatto o sintesi prima del primo capitolo | ≥ 500 caratteri in ogni capitolo; antefatto presente |
| **S2** | codici d'area dei titoli del testo contro quelli stampati sulla mappa, orfani nei due sensi | ≥ 96% del testo sulla mappa, 0 solo sulla mappa |
| **S3** | pagine fra la descrizione di un'area e la sua mappa (da noi anche fra chi cita una mappa per nome e la mappa) | ≥ 54% entro una pagina |
| **S4** | appendice di regione e appendice di PNG/creature in fondo | entrambe presenti |
| **S5** | PNG principali con numeri e ritratto entro una pagina dai numeri | ≥ 53% |

Le soglie sono il valore più basso fra *Burnt Offerings* intero e l'estratto di
RHoD (`docs/audit/volume-booklet.json`); le annotazioni dei riferimenti stanno
in `plans/esperimenti/standard-volume-2026-11-10/riferimenti/`, i PDF no.

**Canale testing** (ADR-0099): in CI un passo non bloccante del job
`stampa-misurata` legge i PDF appena compilati e stampa le misure sotto soglia;
`dm.py volume --stampa` ha il passo `struttura`, che avvisa. **Nessun contenuto
dei booklet cambia con questo ADR**: la ristrutturazione passa dalle card del DM
(dove va ogni contenuto di oggi) e da una versione del booklet centrata sulla
serata, misurata contro quella attuale.

## Misura (2026-11-10)

`plans/esperimenti/standard-volume-2026-11-10/RISULTATO.md`. Sui 10 booklet del
DM: 36 misure sotto soglia, nessun booklet le passa tutte.
- S1: 20 capitoli su 68 con introduzione; antefatto in 7 volumi su 10.
- S2: **nessuna nostra mappa stampa le chiavi d'area**; il testo le usa in 5 booklet.
- S3: per nome mappa, 4-13% entro una pagina (riferimento 54%).
- S4: appendice delle creature sì, **appendice di regione in nessun booklet**.
- S5: 12 PNG principali su 13 con ritratto vicino ai numeri, dove si misura.

Lo standard di fatto non è bocciato dalla misura: è la nostra struttura a
esserne lontana. Una cosa sola dei riferimenti non si prende alla lettera: S3
«sempre entro una pagina» è più severo di Paizo stesso (54%), quindi la soglia è
il dato del riferimento, non la regola ideale.

## Conseguenze

- Il passaggio di milestone della piattaforma ha una misura del volume, accanto
  a `misura_stampa`: ogni PR che tocca un booklet mostra il prima e il dopo.
- Le mappe di ADR-0106 dovranno stampare le chiavi d'area, se il DM sceglie lo
  schema Paizo anche per le piante: è il buco più grande e il più meccanico.
- I booklet di serata (regia, cast, scena dopo scena) non sono capitoli
  d'avventura: S1 e S4 per loro sono da decidere con il DM, non da imporre.
- I riferimenti sono due e uno è un estratto: le soglie si rifanno se arriva un
  altro AP intero (un volume PF1e o RHoD completo).
- Falsi positivi dichiarati: un indizio con codice («A1 · La ricevuta») conta
  come chiave; un capitolo che apre con il frontespizio del master incluso
  conta come senza introduzione.

**Da rivedere se**: il DM sceglie una struttura diversa per i booklet di serata;
arriva un terzo riferimento intero che sposta una soglia; un OCR legge le
etichette delle mappe di carta (allora la trascrizione a vista si toglie);
dopo 14 giorni e 10 corse su `main` senza falsi allarmi non spiegati, e con le
scelte del DM fatte, il passo può salire a stable.

## Aggiornamento del 2026-11-13: pagina fitta, provata e abbandonata

**Contesto.** La serata «La Notte e l'Alba» era di 125 pagine. La misura delle
ripetizioni (MS-0086) dice che le copie valgono poco e che pesa la pagina: 561
parole contro le 725 di *Burnt Offerings*. Il DM ha chiesto pagina più fitta e
copie tolte.

**Che cosa si è provato.** Una chiave di manifest `"pagina": "fitta"` (A4 a
9,6 pt, interlinea 0,56em) portava la serata a 114 pagine; le copie «una volta
sola» non toglievano pagine.

**Decisione.** Il DM le ha bocciate tutte, lo stesso giorno: le schede
accorpate si leggono peggio, le schede strette «sembrano tutte attaccate», e
alla fine «preferisco sempre la versione del 12 novembre». La chiave è tolta.
La pagina dei booklet resta quella ariosa: 10,2 pt, interlinea 0,62em.

**Conseguenze.** La serata resta di 125 pagine. Lo scarto di densità dagli AP
è una scelta di leggibilità del DM, non un difetto da correggere.
