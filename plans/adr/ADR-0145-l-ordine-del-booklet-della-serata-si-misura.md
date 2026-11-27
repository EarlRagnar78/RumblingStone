# ADR-0145 — L'ordine dei capitoli del booklet della serata e del volume d'arco si misura

**Stato**: proposta (2026-11-19); le card di Jfs sui doppioni e su Durik hanno risposto lo stesso giorno (v4.1)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19: «mi controlli se l'ordine logico del booklet con cui compaiono le varie sezioni ha senso e segue gli standard editoriali validi […] cercarle e vedere quanto sono applicate misurando e testando il risultato», e «creare se non ci sono strumenti per correggere questi difetti editoriali […] sempre con test tdd», e alle 13:10 UTC: «aggiungi lo stesso lavoro anche per l'avventura completa».
**Rapporti**: segue [ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md) (struttura del booklet di sessione), [ADR-0122](ADR-0122-il-volume-segue-lo-schema-degli-adventure-path.md) e [ADR-0144](ADR-0144-due-stampe-per-arco-e-rimandi-con-la-pagina.md); usa `plans/RICERCA-USABILITA-AL-TAVOLO-2026-11.md`. Misura: `scripts/misura_ordine.py`; i ruoli della serata e del volume d'arco di ARC-07 stanno nei loro manifest (chiave `ruolo` dei capitoli e lista `ruoli_sezioni`), il cancello è `difetti_ordine` in `scripts/misura_stampa.py`. Fino al 2026-11-19 stavano in due file a parte sotto `plans/esperimenti/ordine-*-2026-11-19/`, tolti quando i ruoli sono passati nel manifest.

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

| | v3 (131 pp) | v4 (134 pp) | v4.1 (132 pp) |
|---|---|---|---|
| Difetti di struttura | 15 | 3 | 0 |
| Blocchi di preparazione dopo il gioco (R2) | 2 (§0-ter con i momenti dei PG e le zone; la cassetta con Durik) | 1 (Durik) | 0 (Durik è riferimento) |
| Riassunto dopo il dettaglio (R4) | 3 su 4 | 0 su 4 | 0 su 4 |
| Pagine di dopo-serata fra le scene (R6) | 3 | 0 | 0 |
| Righe sbagliate nella guida (R8) | 5 | 0 | 0 |
| Doppioni (R7) | 2 | 2 | 0 |
| Rimandi con pagina, tutti giusti | 101 su 124 (15 a un titolo assente) | 115 su 124 (1 a un titolo assente) | 113 su 122 (1 a un'apertura in grassetto) |

v4.1 segue le due card del 19/11. Durik resta in coda, «come galleria
PNG» (Jfs): il file dei ruoli lo dichiara riferimento. Dei due doppioni,
A.1 (l'Adulto) esce dalla serata e la sua parte «Cosa cambia al tavolo»
diventa A.1-ter con i numeri di entrambi i draghi; la scheda del Vecchio
(A.1-bis) è stata resa intera, perché rimandava ad A.1 in sei punti. A.6
resta: porta la tabella delle complicazioni, non solo schede.

Quello che si paga:

- tre pagine in più (131 → 134), per i capitoli che ora aprono su pagina
  nuova;
- i 3 difetti rimasti in v4 erano scelte di Jfs, chiuse in v4.1 (sopra);
- il rimando a «Se l'alba arriva prima della tenda» va al capitolo giusto
  ma senza pagina, perché nel master è un'apertura in grassetto e non un
  titolo;
- i segnalibri del PDF erano piatti: titolo del capitolo e sue sezioni allo
  stesso livello. Corretto il 2026-11-19, sotto in «I segnalibri annidati».

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

## I segnalibri annidati e il confronto con le case

Jfs (19/11, 14:07 e 14:10 UTC) chiede di chiudere i limiti in modo
deterministico, seguendo uno standard editoriale professionale, e di dire
dove questo standard è allineato a Paizo, a Wizards e alla community e dove
se ne discosta. Le differenze entrano solo se sono proprie del repo e
migliorano davvero il volume (14:11).

I segnalibri ora seguono l'albero dei titoli: il capitolo al primo livello,
le sue sezioni sotto. Il convertitore inserisce `#set heading(offset: 1)`
dopo il primo capitolo e porta ogni capitolo a cominciare dal secondo
livello, così le sezioni sorelle restano sorelle. In PDF/UA-1 nessun titolo
salta un livello. Il titolo nascosto del capitolo non è un segnalibro, lo è
quello visibile, perché Typst appende i segnalibri all'ultimo titolo
segnalato. Un numero in testa al titolo («7. In numeri») si protegge, se no
diventa un elenco e sparisce dal segnalibro.

| | prima (main 6547ff60) | dopo |
|---|---|---|
| Serata, 132 pp | 143 segnalibri piatti | 143 su 4 livelli, 20 al primo |
| Volume d'arco, 289 pp | 439 segnalibri piatti | 439 su 4 livelli, 13 al primo |
| PDF/UA-1 e PDF/A-2a | sì | sì |
| Rimandi con la pagina giusta | 113 su 113 e 242 su 242 | uguali |
| Difetti d'ordine (`misura_ordine.py`) | 0 e 0 | 0 e 0 |

Le due fonti, lette sui PDF caricati da Jfs: *Burnt Offerings* (Paizo,
2007) e l'estratto di *Red Hand of Doom* (WotC, 2006). Tutti e due hanno
segnalibri gerarchici. Per la community si sono guardati Ben Milton
(Questing Beast) e Mike Shea (*Return of the Lazy Dungeon Master*).

| Scelta del repo | Paizo (*Burnt Offerings*) | Wizards (*Red Hand of Doom*) | Esito |
|---|---|---|---|
| Segnalibri a più livelli | sì: Part One…Four sotto l'avventura | sì: Preparation, Background sotto Introduction | allineato da questa decisione |
| Preparazione prima del gioco (R2) | Adventure Background prima della Part One | Introduction: Character Hooks, Running the Adventure | allineato |
| Il riassunto in testa alla parte (R4) | l'intro di ogni Part | il sommario di ogni Part | allineato |
| Il dopo-serata dopo le scene, prima delle appendici (R6) | Concluding the Adventure | Concluding the Adventure | allineato |
| PNG e creature in fondo (Durik, la galleria) | Characters, Bestiary | appendice delle creature | allineato |
| Indice di una pagina (V2) | una pagina | due | allineato |
| Il foglio della serata e il riferimento rapido in testa | no | no | della community (Milton, Shea): resta, perché al tavolo è la prima pagina aperta |
| Due stampe per arco, volume e serata (ADR-0144) | no: un volume | no: un volume | del repo, già deciso da Jfs: resta |
| La scheda stampata sia nella scena sia in appendice («entrambe») | in appendice, rimando nella scena | nella scena | del repo: l'unica differenza non misurata, su card a Jfs |

Le divergenze che restano sono tre. Il foglio in testa viene dalla
community, non dalle case, e si tiene perché al tavolo è la pagina aperta
per prima. Le due stampe per arco le ha decise Jfs con ADR-0144. La scheda
stampata due volte non ha ancora una misura che dica che migliora il
volume: finché Jfs non risponde sulla card, resta com'è.

Il ruolo di ogni sezione, scritto a mano nei file dei ruoli, e la misura
d'ordine come cancello sono passati nella PR successiva: sotto, in «I ruoli
nel manifest».

Si paga così:

- `misura_distanza_pagine.py --volume` conta S1 sui segnalibri di primo
  livello. Con l'albero il denominatore cambia: per la serata da 6 su 69 a
  1 su 17, per il volume da 44 su 129 a 7 su 12. Il thread del volume lo sa
  e rifà la soglia;
- nell'Abbazia della Rotta Sicura le pagine passano da 45 a 46, per i titoli
  che cambiano livello.

## I ruoli nel manifest, e l'ordine diventa un cancello

Fino a qui il ruolo di ogni sezione stava in due file di regole sotto
`plans/esperimenti/`, uno per la serata e uno per il volume, e la misura
d'ordine si lanciava a mano. Erano due limiti dichiarati: un capitolo
rinominato perdeva il ruolo senza che nessuno se ne accorgesse, e un
riordino sbagliato arrivava su main.

Lo standard è quello degli editori. CMOS 1.4 divide ogni libro in materia
d'apertura, corpo e chiusura (front, body, back matter), ed EPUB 3 scrive la
stessa divisione dentro il file, sezione per sezione, con `epub:type`
(`frontmatter`, `bodymatter`, `backmatter`, e i ruoli fini come `preface`,
`appendix`, `glossary`). Il ruolo sta accanto al contenuto che giudica, non in
un registro a parte. I nostri sette ruoli sono una suddivisione di quei tre:

| Ruolo | CMOS 1.4 | `epub:type` più vicino |
|---|---|---|
| avvio | front matter | `frontmatter`, `preface` |
| preparazione | front matter | `frontmatter`, `introduction` |
| gioco | body matter | `bodymatter`, `chapter`, `part` |
| sintesi | body matter | `bodymatter` |
| regole | body matter | `bodymatter`, `sidebar` |
| fuori-serata | back matter | `backmatter`, `afterword` |
| riferimento | back matter | `backmatter`, `appendix` |

La suddivisione è del repo e resta perché il tavolo la usa: «preparazione»
e «avvio» sono entrambe front matter, ma al tavolo una si legge il giorno
prima e l'altra si tiene aperta. È la differenza che R2 misura.

Decisione:

- **Ogni capitolo del manifest dichiara `ruolo`**; `parte`, `scena`,
  `riassume` e `doppione_di` passano dal file di regole al capitolo. Le
  eccezioni dentro un capitolo (una sintesi, una scena, una sezione di
  riferimento in un master di gioco) stanno nella lista `ruoli_sezioni` del
  manifest, con la grammatica di prima. Lo schema
  `scripts/schemas/booklet_manifest.schema.json` ammette solo i sette valori.
- **L'introduzione e le appendici generate non dichiarano niente.** Non sono
  capitoli del manifest: le aggiunge l'esportatore. Prima dei capitoli
  valgono «avvio», dopo valgono «riferimento», come la materia d'apertura e
  di chiusura di CMOS.
- **Il titolo di un capitolo combacia intero**, non con una regex: un
  capitolo rinominato porta con sé il ruolo.
- **R0: un capitolo senza ruolo è un difetto**, se il manifest ne dichiara
  almeno uno.
- **`misura_stampa.py` registra `difetti_ordine`** per ogni booklet il cui
  manifest dichiara i ruoli, con un tetto che scende soltanto; la CI lo
  controlla con `--check` nel lavoro delle misure di stampa. Gli altri
  booklet registrano 0, perché senza ruoli l'ordine non si misura.
- **`test_misura_ordine.py` tiene un cancello senza PDF**: un manifest del
  repo che dichiara i ruoli li dichiara per ogni capitolo, con un valore
  ammesso.

Misure del 2026-11-19, sui PDF della #502:

| | serata | volume d'arco |
|---|---|---|
| Sezioni etichettate dal manifest, uguali a quelle del file di regole | 128 su 128 | 398 su 398 |
| Difetti d'ordine | 0 | 0 |
| Regole nel manifest: capitoli, eccezioni | 17, 24 | 11, 20 |
| Un manifest rotto apposta (un capitolo senza ruolo, un atto marcato fuori serata) | 3 difetti contro un tetto di 0 | |

Si paga così:

- le regole delle eccezioni restano espressioni sul titolo, come prima: una
  sezione rinominata dentro un master perde la sua eccezione e prende il
  ruolo del capitolo. Il capitolo, invece, no;
- due regole del file della serata e una del volume non combaciano più con
  nessuna sezione (A.1, l'Adulto, uscito dalla serata; la cassetta, che nella
  serata non c'è; l'Appendice C delle versioni veloci). Restano come
  guardie: se la sezione torna, torna con il suo ruolo;
- i booklet senza ruoli (tutti tranne questi due) non hanno ancora un
  cancello d'ordine. Si estende un manifest alla volta, quando il suo
  booklet passa per un giro di lettura.

