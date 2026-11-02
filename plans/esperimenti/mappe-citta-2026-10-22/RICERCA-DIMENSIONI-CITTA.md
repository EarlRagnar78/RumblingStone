# Ricerca: quanto sono grandi Rethmar, Dauth e Channathgate

Data: 2026-10-22. Scopo: dare alle piante di città della Cannath Vale abitanti,
superficie, mura e porte che reggano il confronto con le fonti di *Red Hand of
Doom* (RHoD), con il canone dei Forgotten Realms e con città vere, e fissare le
regole per il generatore SVG.

Convenzione delle etichette:

- **[CITATO]** è il testo di una fonte, riportato o parafrasato da vicino, con l'URL.
- **[DI SECONDA MANO]** è un numero del manuale RHoD che ho trovato solo in siti di
  fan che lo trascrivono; il manuale non l'ho aperto.
- **[DEDOTTO]** è un mio calcolo o una mia scelta.
- **[CONOSCENZA GENERALE]** è un dato noto ma non riverificato in questa sessione.

Firecrawl era senza crediti: le ricerche sono passate da WebSearch e WebFetch.

## 1. La Elsir Vale nelle fonti di RHoD

### La tabella del DMG 3.5 (p. 137, «Random Town Generation»)

[CITATO] trascritta in https://www.enworld.org/threads/e-tools-tables-towns.21989/post-329014

| Categoria | Abitanti | Limite in mo |
|---|---|---|
| Thorp | 20-80 | 40 |
| Hamlet | 81-400 | 100 |
| Village | 401-900 | 200 |
| Small town | 901-2.000 | 800 |
| Large town | 2.001-5.000 | 3.000 |
| Small city | 5.001-12.000 | 15.000 |
| Large city | 12.001-25.000 | 40.000 |
| Metropolis | 25.001+ | 100.000 |

### Le località

| RHoD | Cannath Vale | Categoria e abitanti | Mura, acqua | Fonte |
|---|---|---|---|---|
| Brindol | Rethmar | small city, **8.400** (limite 15.000 mo) [DI SECONDA MANO] | mura di pietra alte 20 ft e spesse 10 su tre lati, il fiume Elsir a nord; tre ponti di pietra | Damien (a), warscales (b), ORC Edinburgh (c), connorssettings (d) |
| Dennovar | Channathgate | small city, **11.600** [DI SECONDA MANO]; «the largest community in Elsir Vale», «trade-city» | «an outer defensive wall of stone»; sul **lago Ern**, non su un fiume | (a), (e), rpol (f) |
| Drellin's Ferry | Drellin's Ferry | small town, **1.150** (limite 800 mo) [DI SECONDA MANO] | sul fiume, traghetto; mura non citate | (a), (f) |
| Dauth | Dauth | **hamlet, circa 200** («sleepy little hamlet») | mura non citate | (d), (e), giantitp (g) |
| Talar | Talar | small town | traghetto sull'Elsir | (d), (g) |
| Terrelton | Terrelton | small town («a dusty town») | non citate | (d), (g) |
| Witchcross | Witchcross | large village, al guado del Witchstream | non citate | (d), (g) |
| Elsircross | Cannathcross | small town, al guado dell'Elsir | «surrounded by a decrepit palisade» | (d), (g) |
| Rhest | Lhesper | antica capitale, rovina mezza sommersa nei Blackfens | canali e chiuse in rovina | (a), (f) |

Fonti: (a) https://www.tapatalk.com/groups/necromancergames/damien-39-s-red-hand-of-doom-campaign-information-t8303.html
(«Small City; 15,000 gp limit; population 8,400», «Small City; 15,000 gp limit; population 11,600»,
«Small Town; 800 gp limit; population 1,150») ·
(b) http://warscales.wikidot.com/brindol (mura 20×10 ft, porte a est, ovest, sud e alle teste dei ponti; questo sito dà 6.700 abitanti) ·
(c) https://orcedinburgh.co.uk/wiki/Brindol («had a population of 8,400 souls» prima della guerra, «some 6,700 now live within Brindol's walls») ·
(d) http://connorssettings.wikidot.com/printer--friendly//elsir-vale ·
(e) https://frredhandofdoom.blogspot.com/2019/05/red-hand-of-doom.html (Brindol 8.400, Dennovar 11.600, Dauth circa 200) ·
(f) https://wiki.rpol.net/?id=74866 (Dennovar «Population 11,000», «outer defensive wall of stone») ·
(g) https://forums.giantitp.com/archive/index.php/t-271605.html

Siti scartati perché sono rifacimenti con numeri propri: corwyn.wikidot.com
(Dennovar 3.200) e worldanvil «Points of Light» (Brindol 6.000, Dauth 500).

Tre cose che ne seguono:

1. **Nella Elsir Vale Dennovar è più grande di Brindol** (11.600 contro 8.400).
   Il canone del repo dice il contrario: Rethmar è la città maggiore e
   Channathgate la seconda. Brindol pesa di più per ruolo (sede di Lord
   Jarmaath, consiglio di guerra, assedio finale), non per abitanti.
2. **Dauth in RHoD è un borgo di 200 anime senza mura.** La Dauth della campagna,
   con mura, Porta Sud, torneo e guarnigione di mercenari nani, è già
   un'invenzione del repo [DEDOTTO]. Stringerla la avvicina al libro.
3. **Dennovar ha mura e sta su un lago.** Farne una città aperta è una scelta
   nuova, compatibile con la mappatura FR qui sotto.

### La pianta di Brindol e il rifacimento di antariuk

Il manuale non l'ho avuto sottomano; la scala della pianta originale resta da
verificare sul libro. La pianta di Rethmar di antariuk (Arne Haschen), già
misurata in `plans/esperimenti/mappe-qualita-2026-10-22/CLASSIFICA.md`, ha una
barra di 1.000 piedi su 385 px; la cinta misura circa **1.100 × 520 m, una
cinquantina di ettari**, circa 3,2 km di perimetro e poco più di una decina di
torri [CITATO dal repo]. Il fiume è a nord, fuori dalle mura, con il ponte e il
mercato alla sua testa: lo stesso schema di Brindol nelle fonti (b) e (c).

## 2. Il canone dei Forgotten Realms

- **Channath Vale** è canone [CITATO]: valle stretta, calda e umida al margine
  sud dello Shaar sotto il North Wall, sul Traders' Way fra la Lapaliiya e il
  Great Rift; fiumi Channath e Talar; insediamenti Channathgate («the
  easternmost town in the Vale, south of the Channathwood»), Rethmar, Kormul,
  Fryndul. Il wiki **non dà abitanti**. Fonti principali: *Shining South* (2004)
  pp. 155-159, 186-189; *Red Hand of Doom* p. 8 la colloca lì.
  https://forgottenrealms.fandom.com/wiki/Channath_Vale
- **Rethmar canonica** (Ed Greenwood, colonna «Rethmar, Rathole of the Shaar»,
  EN World, 4 novembre 2019) [CITATO]: «the off-season population of Rethmar was
  around 3,300» nel 1365 DR, più fino a 600 nella stagione delle carovane;
  circa 4.700 nel 1479 DR. **Nessuna mura costruita**: la protegge una cresta di
  basalto a mezzaluna, lo Stoneshield, «that stands as a wall to the northwest,
  north, and northeast», con due torri di guardia sulla cresta (le Fangs). Al
  centro un mercato ovale aperto, The Hard, e tre stagni di sorgente.
  https://www.enworld.org/threads/rethmar-rathole-of-the-shaar.667088/
- **Channathgate canonica**: popolazione non trovata. Kanka la dà a 10.000 ma
  senza fonte (https://app.kanka.io/w/127499/entities/3084517): da non usare.

[DEDOTTO] La Rethmar di Greenwood è un **borgo carovaniero aperto di 3.300
anime**. La campagna usa invece la scala di Brindol (città murata per
l'assedio). Le due si tengono insieme dicendo che la Rethmar del 1372 è
cresciuta come Brindol dentro mura nuove, mentre la Rethmar di Greenwood è una
fotografia di sette anni prima. Il modello della città aperta, quello di
Greenwood, si sposta invece benissimo su Channathgate.

## 3. Dagli abitanti alla superficie

### S. John Ross, *Medieval Demographics Made Easy*

[CITATO] https://www.martinralya.com/wp-content/uploads/2021/05/Medieval-Demographics-Made-Easy.pdf

- «the average population density will float somewhere around 150 per hectare
  (61 per acre)»; «Very crowded cities might have densities close to 300/ha»;
  «some sparse cities will have densities as low as 75».
- «the land within the walls of a city of 10,000 would be around 67 hectares».
- Categorie: villaggi 20-1.000, town 1.000-8.000, city 8.000-12.000, big city
  12.000-100.000.

### Città vere

| Città | Superficie dentro le mura | Mura, torri, porte | Abitanti | Fonte |
|---|---|---|---|---|
| Ávila | 31 ha | 2.516 m, 88 torri (una ogni ~29 m), 9 porte | — | [CITATO] https://en.wikipedia.org/wiki/Walls_of_Ávila |
| Carcassonne, la Cité | 11 ha (area del sito) | doppia cinta di 3 km, 52 torri | 3.000-4.000 verso il 1130, compresi i due borghi sotto le mura | [CITATO] https://en.wikipedia.org/wiki/Cité_de_Carcassonne |
| York | non riportata | 3,4 km, 4 porte maggiori (bars) e 2 minori | — | [CITATO] https://en.wikipedia.org/wiki/York_city_walls |

[DEDOTTO] Carcassonne a 11 ha con 3-4.000 persone (borghi inclusi) sta fra
150 e 250 ab/ha nel nucleo, e mostra che una città piccola ha sempre i borghi
fuori. Ávila a 150 ab/ha farebbe circa 4.600 persone.

### Le città aperte dell'Iran e dell'Asia centrale

- [CITATO] La città tripartita dell'Asia centrale ha la cittadella, lo
  *shahristan* («residential area inside the walls») e il *rabad*, i sobborghi.
  https://en.wikipedia.org/wiki/Rabad
- [CITATO] Nella tabella di Matthee sulle mura safavidi Isfahan ha mura «weak»
  nel tardo XVI e nel XVII secolo; Ardabil, Rasht, Farahabad, Zanjan e Qazvin
  risultano senza mura; «many European travellers» trovavano le città orientali
  «often unwalled». https://en.wikipedia.org/wiki/Defensive_walls_in_Safavid_Iran
- [CONOSCENZA GENERALE] Com'era fatta una città aperta: una cittadella murata
  (*arg*, *kuhandiz*) su un'altura o una terrazza; un bazar lineare, spesso
  coperto, che fa da spina dorsale fra la cittadella e le strade carovaniere; i
  quartieri (*mahalle*) chiusi da porte di notte, con vicoli ciechi; ai margini
  giardini murati, frutteti, cimiteri e caravanserragli sulle strade d'arrivo.
  Il confine della città è un fossato, un argine di terra o il muro dei giardini,
  non una cinta con torri. La densità crolla dal nucleo ai giardini.

### Densità consigliate [DEDOTTO, sulla base di Ross]

| Zona | ab/ha |
|---|---|
| Dentro le mura, città normale | 120-180 (valore di lavoro **150**) |
| Nucleo affollato di una città aperta, bazar | 150-200 |
| Sobborghi a nastro lungo le strade | 50-90 |
| Quartieri-giardino, frutteti abitati | 15-40 |
| Cittadella (soldati, corte, magazzini) | 40-80 |

## 4. Come si fa una buona pianta di città

### Watabou, Medieval Fantasy City Generator

- **Licenza** [CITATO] https://watabou.itch.io/medieval-fantasy-city-generator:
  le mappe generate «as you like: copy, modify, include in your commercial rpg
  adventures», attribuzione gradita ma non obbligatoria. Il codice
  (TownGeneratorOS su GitHub) è **GPL-3.0**: si può studiare l'algoritmo, ma
  copiarne il codice nel repo vincolerebbe lo script alla GPL. Meglio una
  reimplementazione nostra dell'idea.
- **Come lavora** [CITATO, `Model.hx`]
  https://github.com/watabou/TownGeneratorOS/blob/master/Source/com/watabou/towngenerator/building/Model.hx
  - punti a spirale (`a = sa + sqrt(i)*5`, `r = 10 + i*(2+rnd)`), Voronoi,
    tre passate di rilassamento sulle celle centrali;
  - le prime `nPatches` celle sono la città. Il commento del codice dà la scala:
    **small town 6, large town 10, small city 15, large city 24, metropolis 40**;
  - plaza, cittadella e mura sono ciascuna un sì o no a caso; la cittadella è
    la cella numero `nPatches`, scartata se poco compatta (< 0,75);
  - le porte stanno sui vertici della cinta; da ogni porta una strada va alla
    piazza (A* sul grafo dei bordi delle celle) e una via esterna va verso
    l'infinito; le arterie vengono lisciate;
  - i quartieri: mercato sulla piazza, poi una lista pesata di 36 voci in gran
    parte artigiani, con mercanti, cattedrale, amministrazione, patriziato,
    militare, parco e slum, ciascuno messo nella cella che valuta migliore;
  - fuori dalle porte nasce un «GateWard» (sobborgo) con probabilità
    `1 - 1/(nPatches-5)`; oltre, campi e terreno vuoto.

### I cartografi di riferimento

- **Jonathan Roberts** (Fantastic Maps) [CITATO]
  https://www.fantasticmaps.com/2012/02/more-city-design-tips/ e
  https://www.fantasticmaps.com/?p=1185 : prima il terreno (fiumi, colli); il
  centro del potere su un colle o in un'ansa; il nucleo vecchio cresce fra
  l'acqua e il potere; le strade per le altre città puntano al centro, seguono
  le curve di livello e piegano ai guadi; le mura segnano la città vecchia e
  deviano le strade; i luoghi maggiori (porto, mercato, granai, templi,
  caserme) fanno da raggiera; le strade hanno gomiti ma «go in one clear
  direction»; gli slum sono irregolari, i quartieri ricchi a viali e griglie;
  le strade si leggono come vuoto fra i blocchi; troppi tetti disegnati
  confondono i quartieri. Un commento aggiunge la crescita a «pseudopodi»
  lungo le strade, poi riempiti.
- **Mike Schley, Dyson Logos, Paizo** [CONOSCENZA GENERALE, non riverificato]:
  Schley (molte mappe WotC del periodo 3.5) usa isolati pieni con poche case
  disegnate e una legenda numerata; Dyson Logos lavora in bianco e nero, a
  tratteggio, con molte mappe libere anche per uso commerciale; le piante Paizo
  (Sandpoint, Magnimar) hanno edifici singoli, numeri di legenda e nomi solo per
  quartieri e luoghi chiave.

### Regole per il generatore SVG [DEDOTTO dalle fonti sopra]

1. **Ordine di costruzione**: terreno (quote, fiume, lago), cittadella sul punto
   alto o nell'ansa, strade esterne verso le città vicine, porte dove le strade
   tagliano la cinta, piazza dove le strade convergono, poi i blocchi.
2. **Gerarchia delle strade**: arterie 8-12 m dalle porte alla piazza;
   secondarie 4-6 m; vicoli 1,5-3 m, ciechi nei quartieri orientali. In SVG
   l'arteria è larga almeno il doppio del vicolo.
3. **Blocchi**: suddivisione ricorsiva dei poligoni (come i `createAlleys` di
   Watabou) fino a lotti con fronte di 5-8 m e profondità di 15-30 m, aperti
   sulla strada, con cortili interni.
4. **Gradiente di densità**: copertura 80-90% al centro, 60-70% vicino alle
   mura, 30-50% nei sobborghi, che corrono a nastro per 1-3 file lungo le strade
   per 200-500 m dalle porte. Una testa di ponte oltre il fiume.
5. **Spazi aperti**: 10-15% della superficie fra piazze, sagrati, orti; una
   fascia libera di 5-10 m dentro le mura e un fossato fuori.
6. **Mura**: torri ogni 30-60 m (Ávila 29), porte con torri gemelle, 2-5 porte
   per una città piccola, una per ogni strada maggiore.
7. **Città aperta**: niente cinta; cittadella murata compatta; un argine o un
   fossato discontinuo; quartieri distinti da porte di quartiere; giardini murati
   e caravanserragli sul bordo.
8. **Scritte**: nomi dei quartieri in maiuscoletto spaziato lungo il quartiere;
   nomi di strada solo sulle arterie; luoghi con un numero e legenda; barra di
   scala in metri e piedi e la rosa. Mai un'etichetta per casa.
9. **Resa**: edifici pieni scuri, strade come vuoto (Roberts), mura spesse con
   cerchi per le torri, acqua con linee di riva, campi a strisce fuori dalla
   città.
10. **Controllo numerico**: lo script calcola ettari dentro le mura, ettari dei
    sobborghi e abitanti = somma(area × densità della zona), e fallisce se il
    totale esce di oltre il 10% dal valore dichiarato.

## 5. Raccomandazione

| | Rethmar (Brindol) | Dauth | Channathgate (Dennovar) |
|---|---|---|---|
| Categoria DMG | small city | large town | small city |
| Abitanti totali | **8.400** | **2.600** (2.300-3.000) | **7.500** (fino a 11.600 se si segue RHoD) |
| Dentro le mura | 50 ha, ~7.000 ab. (140/ha) | 17 ha, ~2.400 ab. (140/ha) | **nessuna cinta**; cittadella murata di 4 ha (~250 ab.) |
| Fuori | sobborghi 15 ha, ~1.400 ab.: testa di ponte a nord e nastri sulla Dawn Way | borgo fuori dalla Porta Sud, 2-3 ha, ~200 ab. | nucleo del bazar 30 ha a 160/ha (~4.800); quartieri-giardino e caravanserragli 60 ha a 40/ha (~2.400) |
| Perimetro e torri | ~3,2 km; torri ogni 40-50 m, circa 70 | ~1,5-1,6 km; torri ogni ~40 m, circa 40 | cittadella ~0,75 km, 12-15 torri |
| Porte | 5: est e ovest sulla Dawn Way, sud, due alle teste dei ponti | 3: Porta Sud, una a nord, una postierla a ovest | 4-6 ingressi di strada senza porta urbana; porte di quartiere; 2 porte alla cittadella |
| Acqua | fiume Cannath a nord, fuori dalle mura | nessun fiume, cisterne | lago a sud, Cannath sul lato ovest |

Perché:

- **Rethmar**. I 50 ha sono quelli della pianta di antariuk e a 140 ab/ha
  fanno 7.000 persone dentro. Con i sobborghi si arriva a 8.400, il numero di
  Brindol nel libro. Cinque porte sono quelle di Brindol (fonte b). Resta la
  prima città per ruolo e la più fortificata, come vuole il canone del repo.
- **Dauth**. Il DM la vuole sotto 32 ha e 5.100 abitanti; il libro la dà a 200.
  Una large town di 2.600 anime basta per un torneo, una guarnigione e un
  assedio, e resta una città, non un borgo. 17 ha sono metà di Ávila: si tiene
  il modello di Ávila (torri fitte, città in altura) a scala ridotta, fra Ávila
  (31 ha) e la Cité di Carcassonne (11 ha). Tre porte bastano perché nessun
  fiume e nessuna strada maggiore la attraversa.
- **Channathgate**. Il canone del repo la vuole seconda dopo Rethmar; il libro
  la vuole prima (11.600). Con 7.500 abitanti su circa 95 ha costruiti la sua
  impronta supera quella di Rethmar (65 ha), quindi sulla carta sembra grande,
  ma conta meno persone e nessuna cinta: è la città mercantile dispersa del
  modello persiano (cittadella, bazar, giardini) e la Rethmar aperta di
  Greenwood. Se il DM preferisce seguire RHoD, si porta a 11.600 aggiungendo
  quartieri-giardino fino a ~150 ha; allora il canone va corretto in
  «Rethmar è la capitale, Channathgate la più popolosa».
- Le piante attuali (Channathgate 45 ha + 82 di sobborghi per ~11.700 ab.;
  Dauth 32 ha, 88 torri, 9 porte) vanno ridisegnate su questi numeri; la
  Rethmar di 50 ha regge.
- Parametri di partenza per un generatore alla Watabou [DEDOTTO]: Dauth 10
  celle con mura; Rethmar 15 celle con mura, fiume e cittadella; Channathgate
  15 celle senza mura, cittadella sì, sobborghi a ogni strada.

## 6. Una taglia sopra: le piante v3 (DM, 2026-10-22)

Il DM vuole le tre città di una categoria DMG più grandi, perché reggano
l'assedio dell'orda della Mano Rossa (circa 10.000 al Day 1, meno con gli hook).
Le taglie della Elsir Vale (Brindol 8.400, Dennovar 11.600, Dauth un borgo)
restano nel §1 come fonte; le piante seguono la scelta del DM. Numeri misurati
sulle piante, canone dal 2026-10-23 `[CANONE — DM 2026-10-23]`:

| Città | Categoria DMG 3.5 | Superficie | Abitanti | Mura | Torri | Edifici |
|---|---|---|---:|---|---:|---:|
| Rethmar | grande città | 110 ha dentro le mura + ~23 ha di sobborghi | ~18.000 (15.400 dentro, 140 ab./ha) | 4,3 km (1,2 sul fiume) | 95 | 3.843 dentro, 737 fuori |
| Dauth | piccola città | 42 ha sullo sperone, quote 530-556 m invariate | ~7.000 (167 ab./ha) | 2,55 km | 59 | 1.750 dentro, 45 fuori |
| Channathgate | grande città, aperta | ~250 ha costruiti (nucleo 66 ha, arg 5 ha, due rabad) | ~25.000 | solo l'arg, 828 m | 27 + 2 | 8.307 |

**Quanti difensori servono.** La regola del Burghal Hidage del Wessex (una
guarnigione di 4 uomini ogni 5,5 m, cioè circa 0,8 uomini per metro di mura) dà:

- Rethmar: 4,3 km chiedono circa 3.400 uomini. La leva degli uomini abili (18%
  di 18.000) è di circa 3.240; con i difensori degli scenari di ARMATE-SYNC §3
  (1.280-3.980) si arriva a 4.500-7.200. Regge.
- Dauth: 2,55 km chiedono circa 2.000 uomini. Leva circa 1.260, con i 300
  mercenari e le 150 lance circa 1.700, più la guarnigione nanica. Non regge
  sull'intero giro: si tengono sud e ovest e si lasciano leggeri i fianchi ripidi.
- Channathgate: senza cinta la regola non si applica. Se dovesse reggere un
  assedio, conterebbe sull'arg e sui muri dei rioni.

## Da verificare sul manuale

- La scala della pianta di Brindol nel libro e il numero esatto di porte.
- Le cifre di Dauth, Talar, Terrelton, Witchcross ed Elsircross nel gazetteer
  (qui sono solo categorie, da fonti secondarie).
- Se *Shining South* dà gli abitanti di Channathgate.

## 7. Canone e controllo della legenda (DM, 2026-10-23)

Il DM ha tenuto la v3 e ha reso canone il rilievo, le quote, le taglie e la
posizione dei luoghi delle tre piante. Resta `[INFERRED]` solo il conto dei
difensori, perché è una regola empirica e a Dauth manca ancora il numero della
guarnigione nanica.

Prima di renderle canone ho controllato i 78 numeri sulle piante contro le voci
della legenda, ritagliando l'intorno di ciascuno. Sei erano fuori posto:

| Pianta | N. | Voce | Dov'era | Dov'è ora |
|---|---:|---|---|---|
| Rethmar | 6 | Mura sud, la breccia del Settore C | nei campi, 30 m fuori dalle mura | sulla cinta sud |
| Rethmar | 8 | Mercato del Ponte | sulla riva, fra le mura e il fiume, dove non c'è nulla | nel foro, alla testa del ponte |
| Rethmar | 27 | Torre di Immerstal il Rosso | copriva la torre | accanto alla torre |
| Dauth | 2 | Bastioni sud, il Razorfiend | nei campi sotto le mura | sulla cinta sud-est |
| Dauth | 4 | Mura ovest, le lance di Khorn | fra il fossato e il boschetto | sulla cinta ovest |
| Channathgate | 16 | Campo profughi dell'Istrice | sulle case del rione | sul campo di tende |

Lo spostamento del 6 di Rethmar ha fatto alzare la scritta del Quartiere Nobile.
Nessun documento del repo cita i numeri della legenda, quindi i testi non
cambiano.

