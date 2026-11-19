# ADR-0145 — L'ordine dei capitoli del booklet della serata e del volume d'arco si misura

**Stato**: proposta (2026-11-19), in attesa delle card di Jfs sui doppioni e su Durik
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19: «mi controlli se l'ordine logico del booklet con cui compaiono le varie sezioni ha senso e segue gli standard editoriali validi […] cercarle e vedere quanto sono applicate misurando e testando il risultato», e «creare se non ci sono strumenti per correggere questi difetti editoriali […] sempre con test tdd», e alle 13:10 UTC: «aggiungi lo stesso lavoro anche per l'avventura completa».
**Rapporti**: segue [ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md) (struttura del booklet di sessione), [ADR-0122](ADR-0122-il-volume-segue-lo-schema-degli-adventure-path.md) e [ADR-0144](ADR-0144-due-stampe-per-arco-e-rimandi-con-la-pagina.md); usa `plans/RICERCA-USABILITA-AL-TAVOLO-2026-11.md`. Misura: `scripts/misura_ordine.py`, regole per la serata di ARC-07 in `plans/esperimenti/ordine-serata-2026-11-19/ruoli-serata.json` e per il volume d'arco in `plans/esperimenti/ordine-volume-2026-11-19/ruoli-volume.json`.

## Contesto

Il booklet della serata di ARC-07 (v3, 131 pagine) era nato tagliando il
booklet lungo: i capitoli erano nell'ordine dei file, non in quello in cui il
DM li apre. Nessuna misura guardava l'ordine. Letto con le regole qui sotto,
il PDF aveva 15 difetti di struttura (un blocco fuori posto conta uno, perché i segnalibri sono piatti e un capitolo con le sue sezioni è un difetto, non cinque):

- la preparazione (§0-ter, i momenti dei PG, le zone, la cassetta, Durik)
  stava alle pp. 102-118, dopo l'ultima scena;
- tre riassunti su quattro venivano dopo il loro dettaglio («7. in numeri»
  a p. 38 per il dettaglio di p. 29, C.2 a p. 74 per la Scena 6 di p. 52,
  C.3 a p. 96 per la Scena 11 di p. 85);
- tre pagine del dopo-serata (barile §10 e §13) stavano fra le scene;
- la guida ai capitoli dell'introduzione era quella del booklet lungo,
  cinque righe sbagliate su otto («V · La cassetta», «VIII · Durik»);
- due schede stampate due volte, e una delle due è sbagliata per stanotte:
  A.1 è Skullcrusher adulto maturo GS 14 (297 pf), l'appendice delle
  creature ha Skullcrusher Vecchio GS 17, che è il canone della serata (D60).

## Le regole e da dove vengono

Lo standard di fatto della comunità per un volume da tavolo è lo schema
degli AP Paizo e di Red Hand of Doom (scelto da Jfs il 09/11): prima il
quadro, poi le parti nell'ordine di gioco, poi le appendici. Le altre fonti
lette (Alexander, *The Art of the Key*; Shea, *Return of the Lazy Dungeon
Master*; Milton, il «pannello di controllo»; il thread di EN World sui
moduli facili da giocare) dicono la stessa cosa da lati diversi: l'ordine
è quello del bisogno al tavolo, il riassunto viene prima del dettaglio, una
cosa si stampa una volta.

| Regola | Che cosa chiede | Fonte |
|---|---|---|
| R1 | il riferimento rapido e il foglio della serata in testa | Milton; K-tavolo della ricerca |
| R2 | la preparazione prima della prima scena | Shea, passi 1-6; ADR-0013 |
| R3 | le scene nell'ordine in cui si giocano | Paizo, RHoD |
| R4 | il riassunto di un atto prima del suo dettaglio | Alexander; EN World («scheme stated up front») |
| R6 | niente dopo-serata fra le scene | Paizo (Concluding the Adventure in coda) |
| R7 | una scheda o un riferimento si stampa una volta, e il riferimento non sta in mezzo al gioco | ADR-0070; Lynch |
| R8 | la guida ai capitoli dice i capitoli che il volume ha davvero | ADR-0013 |

R5 (una mappa nella stessa pagina dell'incontro) è già di
`misura_distanza_pagine.py` e non si duplica.

## Decisione

- **`scripts/misura_ordine.py PDF RUOLI.json`** legge l'indice del PDF,
  dà un ruolo a ogni sezione con le regole del file dei ruoli (espressioni
  sul titolo, con eredità dal capitolo perché i segnalibri sono piatti) e
  conta i difetti R1-R8. Test in `scripts/tests/test_misura_ordine.py`:
  un volume con cinque difetti noti e la sua versione giusta.
- **La guida ai capitoli si genera.** Se un capitolo del manifest ha
  `quando`, la tabella fra `<!-- guida-capitoli -->` e
  `<!-- /guida-capitoli -->` la scrive `dmcore.testo.guida_capitoli`
  nell'ordine dei capitoli; `guida_righe_finali` aggiunge ciò che non è un
  capitolo (il volume dei giocatori). Test in
  `scripts/tests/test_guida_capitoli.py`.
- **I rimandi dei sorgenti nominano il file, mai il numero romano.** Un
  «capitolo III» scritto a mano si rompe al primo riordino; un rimando
  `` `ARC07-BARILE-SULLA-TENDA.md` §10 `` lo traduce il volume. Un master
  diviso in più capitoli (`sezioni`) manda il §N al capitolo che stampa
  quella parte; `principale` dice quale capitolo prende i rimandi senza
  parte.
- **La serata di ARC-07 passa all'ordine v4**: foglio e riferimento rapido,
  regia, preparazione, cast, chi c'è, i tre atti con il riassunto in testa,
  il duello, il dopo-serata, le appendici, Durik.

## Alternative considerate

1. **Riordinare a mano senza misura.** Scartata: il booklet lungo era
   ordinato a mano e la serata ne ha ereditato la guida sbagliata.
2. **Una regola generale per tutti i booklet.** Rimandata: i ruoli dipendono
   dai titoli di ogni volume, e c'è un volume misurato solo. Il file dei
   ruoli resta un esperimento finché un secondo booklet non lo usa.
3. **Scrivere la pagina nella guida a mano.** Si rompe come i romani.

## Conseguenze

Misure del 2026-11-19 sulla serata di ARC-07:

| | v3 (131 pp) | v4 (134 pp) |
|---|---|---|
| Difetti di struttura | 15 | 3 |
| Blocchi di preparazione dopo il gioco (R2) | 2 (§0-ter con i momenti dei PG e le zone; la cassetta con Durik) | 1 (Durik) |
| Riassunto dopo il dettaglio (R4) | 3 su 4 | 0 su 4 |
| Pagine di dopo-serata fra le scene (R6) | 3 | 0 |
| Righe sbagliate nella guida (R8) | 5 | 0 |
| Doppioni (R7) | 2 | 2 |
| Rimandi con pagina, tutti giusti | 101 su 124 (15 a un titolo assente) | 115 su 124 (1 a un titolo assente) |

Quello che si paga:

- tre pagine in più (131 → 134), per i capitoli che ora aprono su pagina
  nuova;
- i 3 difetti rimasti sono scelte di Jfs: Durik in coda e i due
  doppioni A.1 e A.6, che si tolgono solo con il suo sì;
- il rimando a «Se l'alba arriva prima della tenda» va al capitolo giusto
  ma senza pagina, perché nel master è un'apertura in grassetto e non un
  titolo;
- i segnalibri del PDF sono piatti: titolo del capitolo e sue sezioni allo
  stesso livello. È un difetto di navigazione che questa misura aggira e
  non corregge;

## Il volume d'arco

Un AP non è una serata: è un volume con più parti, ognuna una serata o più.
Le regole della serata si contano parte per parte (una regola con
`"parte": true` apre la parte), e a livello del volume se ne aggiungono tre:

| Regola | Che cosa chiede | Fonte |
|---|---|---|
| V1 | il quadro del volume (l'arco in breve, come si usa) prima della Parte I | Paizo, «Adventure Background» e «Adventure Summary» |
| V2 | l'indice in una o due pagine; i segnalibri del PDF restano completi | l'indice di un AP Paizo è una pagina |
| V3 | nessuna parte senza gioco fra due parti giocate | Paizo, «Concluding the Adventure» dopo l'ultima parte |

Che cosa una parte deve avere in testa (`§0` Quickstart, `§0-bis`
Quick-Reference) i master DEF lo hanno già: lì le parti erano a posto.

Volume v1.2 (294 pp), con le regole lette sui suoi titoli: 12 difetti.
Non c'era il quadro dell'arco (V1), l'indice era di otto pagine (V2), il
ponte verso ARC-08 «La Forgia ricorda le ferite» stava fra il duello e il
ritorno (V3), e quattro riassunti venivano dopo il loro dettaglio: «7. in
numeri» del barile, e l'Appendice C delle versioni veloci con C.2 e C.3,
fino a cinquanta pagine dopo le scene. Anche C.1 stava lì, ma riassume
scene di un'altra parte, e la misura parte per parte non la conta: è un
limite della regola.

Volume v1.3 (288 pp): 0 difetti. Una pagina nuova, «Il quadro dell'arco»
(`volume-arco/00-INTRO-VOLUME.md`): l'arco in cinque righe e la guida ai
capitoli generata dal manifest. Chiave nuova `indice_profondita: 1`:
l'indice in una pagina. Le versioni veloci in testa alla loro parte di
`DEF-4`, il «7. in numeri» del barile dopo il §1, il ponte dopo il ritorno
a Hammerfist. Rimandi: 242 con pagina su 255, tutti giusti; prima uno puntava a un
§7-bis di `DEF-3` che non esiste, ed è corretto nel sorgente (`DEF-2`,
riga 1118: la ghianda è nel §11 C); l'altro è l'apertura in grassetto di
`DEF-4`.

Lo spostamento ha fatto uscire un bug di `estrai_sezioni`: una sezione
chiesta per nome usciva anche se nel master è avvolta in `storico` (il §12
«Domande al DM» del barile, 21 righe fuori margine). Ora la sezione resta
dentro il suo blocco, con un doctest; gli altri booklet con `sezioni` non
cambiano.

Quello che si paga nel volume:

- l'indice stampato dice solo i capitoli: per arrivare a Terros si apre il
  capitolo e il suo «Indice del modulo», o i segnalibri del PDF;
- l'Appendice C non esiste più come blocco: le tre versioni veloci stanno
  ognuna in testa alla sua parte;
- il quadro dell'arco è testo nuovo, scritto dai riquadri «La serata in tre
  frasi» dei master: va letto da Jfs.
