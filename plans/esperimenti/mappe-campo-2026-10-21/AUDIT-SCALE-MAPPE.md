# Audit delle scale delle mappe tattiche

Data: 2026-10-21. Richiesta del DM (Jfs): sulle mappe le scale sono sballate,
per esempio una tenda con un solo palo di 6 m larga più di 50 m e tende piccole
attaccate alla tenda principale. «Fai lo stesso per le altre mappe, cerca in
rete esempi da usare come modello per fare mappe un po' più coerenti e sensate».

Questo giro è in sola lettura: nessuna mappa è stata modificata. Restano fuori
la tenda del comando M7-C (`ARC07-MAPPE-M7C-TENDA-DEL-COMANDO`) e la mappa del
campo dell'orda del 372 (M7-A), che un altro agente sta rifacendo.

Metodo. Ogni griglia è stata letta con `render_map_svg.extract_maps` e misurata
per componenti connesse (ingombro di ogni simbolo in quadretti e in metri), poi
confrontata con il testo che la accompagna, con le altre mappe dello stesso luogo
e con i dati reali raccolti sotto. In più è stato lanciato `collaudo_mappe.py
--solo-errori` sul corpus (50 mappe, 69 rilievi E). Scala del contratto:
1 quadretto = 1,5 m. Le coordinate sono quelle stampate sulle griglie
(colonna-lettera, riga-numero).

Gravità: **alta** se cambia il combattimento o è assurdo a vista (o se l'SVG o
l'UVTT dicono una cosa falsa); **media** se è incoerente ma si gioca; **bassa** se
è un ritocco.

---

## 1. Regole di misura (con le fonti)

Valori da usare come modello. Fra parentesi i quadretti da 1,5 m.

| Elemento | Misura reale di riferimento | In quadretti | Fonte |
|---|---|---|---|
| Muro di dungeon in muratura | ≥ 0,3 m (1 ft); pietra tagliata ≥ 0,9 m; roccia viva ≥ 1,5 m | il muro sta sul bordo o in 1 quadretto | [PF1 Core, Environment, Table Walls](https://legacy.aonprd.com/coreRuleBook/environment.html) |
| Porta | spessore 2,5-10 cm; luce reale 0,9-1,2 m (una porta = 1 quadretto, doppia = 2) | 1-2 | idem, Table Doors |
| Cortina di castello | Beaumaris: 10,7 m alta, 3 m spessa; Caernarfon: fino a 6 m di spessore; Carcassonne gallo-romana: 2-3 m | 2-4 quadretti di spessore, camminamento 1-2 | [h2g2, Curtain Wall](https://www.h2g2.com/edited_entry/A18154857); [World History, Caernarfon](https://worldhistory.org/Caernarfon_Castle); [Cité de Carcassonne](https://www.ancient-history-sites.com/sites/citadel-of-carcassonne/) |
| Merli e cannoniere | merlo ~2 m largo, cannoniera ~1 m | merli alternati a 1 quadretto | [h2g2](https://www.h2g2.com/edited_entry/A18154857) |
| Torre muraria | Carcassonne: base piena 4,5-7 m di diametro, 11-14 m alta; torre maestra (Eagle Tower, Caernarfon): 10,5 m, 30 m alta | 3-5 (mastio 7) | [Carcassonne](https://www.ancient-history-sites.com/sites/citadel-of-carcassonne/); [Caernarfon](https://worldhistory.org/Caernarfon_Castle) |
| Passaggio di porta urbana | «largo quanto basta per un carro e un cavallo» (≈ 3 m); porte dei castra romani ≈ 15 m comprese le torri | 2 di luce, torri 3-4 per lato | [Timeref, Gatehouses](https://www.timeref.com/castles/gatehouses.htm); [Imperium Romanum, castra](https://imperiumromanum.pl/en/roman-army/roman-camp/) |
| Scala a chiocciola | gradino utile ~1 m, vano ~2-2,5 m (stima di mestiere: nessuna fonte aperta con il numero trovata) | 1 quadretto con 🔼/🔽, o 2×2 | [Ryder, The spiral stair or vice](https://chesterrep.openrepository.com/handle/10034/239772) (tesi, senza misure nell'abstract) |
| Navata di tempio | Notre-Dame 12 m, Reims 14,65 m, Sens 15,25 m; la più larga gotica, Girona, 22,98 m | 8-10 (15 eccezionale) | [Girona Cathedral](https://en.wikipedia.org/wiki/Girona_Cathedral) |
| Salone scavato nella roccia (modello di dwarven hold) | Cappella di Santa Kinga, Wieliczka: 54 × 18 m, 12 m alta | 36 × 12 | [Aleteia](https://aleteia.org/2017/09/29/st-kingas-chapel-in-wieliczka-poland-the-worlds-biggest-church-built-underground) |
| Miniera, galleria | Hallstatt: gallerie di coltivazione 5-27 m larghe e fino a 20 m alte; cunicoli di servizio ~2 m | cunicolo 1, gallerie di coltivazione 4-18 | [NHM Wien, Hallstatt](https://www.nhm-wien.ac.at/hallstatt/en/salt_mine/hallstatt_period/mining_facilities) |
| Grotta naturale | nessuna regola: Deer Cave 169 × 125 m di sezione, Sarawak Chamber 700 × 400 m | libera, ma va scritta | [Mulu Caves](https://mulucaves.org.uk/?p=1730) |
| Casa di villaggio | longhouse del basso medioevo 15-18 m (50-60 ft); ~40 case e i loro tofts a Wharram Percy | 4-5 × 10-12 | [Longhouse](https://en.wikipedia.org/wiki/Longhouse); [English Heritage, Wharram Percy](https://english-heritage.org.uk/visit/places/wharram-percy-deserted-medieval-village/history/description) |
| Ponte in pietra | Pont Valentré: impalcato 5 m, 138 m; Ponte Carlo: 9,5 m, 516 m | 3-6 | [Pont Valentré](https://en.wikipedia.org/wiki/Pont_Valentr%C3%A9); [Charles Bridge](https://en.wikipedia.org/wiki/Charles_Bridge) |
| Forgia | focolare: fossa ~1 m; tubiere 12-30 cm; spazio libero intorno a morsa e incudine per barre lunghe | focolare 1, incudine 1, 2 quadretti liberi intorno | [HMS datasheet 303](https://historicalmetallurgy.org/media/mxiorxzr/hmsdatasheet303.pdf); [Beautiful Iron, shop setup](https://beautifuliron.com/gs_setting_up_shop.htm) |
| Tenda a un palo | bell tent: palo 3 m → 5 m di diametro, 6 persone; padiglione tondo: 5 m di diametro con un palo centrale e 16 laterali | palo h → diametro ≈ 1,5-1,7 h; **un palo da 6 m regge al massimo 9-10 m (6-7 quadretti)** | [Mountain Warehouse, bell tent 5 m](https://mountainwarehouse.com/5m-polycotton-bell-tent-zipped-pvc-groundsheet-p58336.aspx/white); [5 Żywiołów, padiglione 5 m](https://www.5zywiolow.com/shop/en/equipment-main/camp-life/tents/round-pavilion-tent-5-m) |
| Tenda militare e accampamento | contubernium (8 uomini) ~3 × 3 m (10 piedi romani); tenda del generale ~3,6 m di lato; arretramento di ~1,5 m dalla strada per i tiranti; intervallum di 18-60 m fra vallo e prime tende | tenda 2×2, 1 quadretto vuoto attorno per i tiranti, strade 2-4 | [Karwansaray, The Roman Camp](https://www.karwansaraypublishers.com/gb_army/the-roman-camp/); [Imperium Romanum](https://imperiumromanum.pl/en/roman-army/roman-camp/) |
| Fuoco da campo | nessuna fonte numerica; un falò da bivacco sta in 1-2 quadretti; il fuoco a meno di 3 m dai teli è un errore di accampamento | 1-2 | (regola di buon senso, coerente con i tiranti sopra) |

Principi di design delle battlemap raccolti:

- **Realismo e regole tirano in direzioni opposte, e va deciso caso per caso.**
  James Jacobs (Paizo) preferisce stanze di misura realistica, ammette che la
  regola «una creatura per quadretto» le rende strette, e come rimedio propone di
  cambiare scala (1 quadretto = 10 ft), non di gonfiare la stanza; Ron Lundeen lo
  riconosce come punto da migliorare
  ([Paizo forum, Abomination Vaults C27](https://paizo.com/threads/rzs43dl6)).
  Per noi: si gonfia lo spazio di manovra (cortili, navate, campi), non gli
  oggetti (tende, porte, torri).
- **Dyson Logos** dichiara la scala di ogni mappa e pensa i saloni dei giganti in
  quadretti da 10 ft (sale da 9-12 m), ammettendo che «corridoi irragionevolmente
  larghi» si giustificano a fatica come costruzione reale ma servono al gioco
  ([Dyson Logos, The Giant's Halls](https://dysonlogos.blog/2015/10/16/friday-map-the-giants-halls-part-1/)).
  Per noi: un'esagerazione si scrive nella mappa, con la sua ragione.
- **Flip-Mat**: i tappeti Paizo sono 30" × 46" a quadretti da 1 pollice, cioè
  ~30 × 46 quadretti, ~45 × 70 m
  ([Paizo, Flip-Mat Enormous](https://store.paizo.com/pathfinder-flip-mat-enormous-basic-pdf/)).
  È la misura «normale» di un campo di scontro: oltre si passa a una scala
  strategica dichiarata.
- **Mike Schley** (cartografo di Red Hand of Doom e del DMG): nessun testo
  pubblico sulle scale trovato in rete; ci si attiene alle sue mappe come
  riferimento visivo (l'atlante delle tavole RHoD è in
  `00_Red Hand Of Doom/Immagini/Area Map/`, da guardare e non da copiare).

Tre regole di casa che ne seguono:

1. **Un oggetto ha la sua misura reale, sempre.** Tende, porte, torri, ponti,
   letti, incudini non cambiano con la scala della mappa. Se una mappa è
   strategica (3 o 6 m a quadretto) l'oggetto diventa un segno, non si allarga.
2. **La scala dichiarata deve arrivare nel recinto.** L'intestazione
   `N col × M righe · S m` dentro la fence è la sola che il renderer legge; una
   scala scritta solo nel testo sopra lascia nell'SVG la barra da 1,5 m.
3. **Il simbolo dice la funzione.** ⬛ è «muratura piena» e l'UVTT ne fa muro: non
   si usa per pavimenti, mostri o tende. 🟢 è una creatura: non si usa come erba.

---

## 2. Censimento

52 griglie emoji in 22 file (escluse le fixture di `scripts/`, i doppioni nei
booklet `.hb.md` e la guida). In più 16 file di ARC-09 con mappe in prosa e 15
tavole SVG disegnate a mano. Le mappe dell'archivio (`_ARCHIVIO`) sono elencate in
fondo e non sono state misurate in dettaglio: sono superate.

Le griglie di ARC-07 dentro i master DEF (`ARC07-DEF-1`, `-2`, `-4`, `-5`) e nei
booklet sono identiche a quelle dell'Atlante: i rilievi valgono per tutte le copie.

---

## 3. Mappe da rifare, per gravità

| # | Mappa | Gravità | Problema in una riga |
|---|---|---|---|
| 1 | Campo Drow 2, Forward Base (ARC-09) | alta | l'intero campo (67 × 66 m) è un blocco di ⬛ pieno: tende, recinto, tenda del Wyrmlord non esistono e il boss è murato |
| 2 | Fortezza di Hammerfist: 2A, MAPPA 1, MAPPA 4, 2B (ARC-08) | alta | quattro misure diverse della stessa fortezza; ponte levatoio che non scavalca il fossato; mura da 1,5 m alte 12 m; bastioni da 27 m² con 40 nani e 2 baliste |
| 3 | 1A-3 Campo della Mano Rossa e MAPPA 1 Disposizione (ARC-08) | alta | scala dichiarata 6 m e 3 m solo fuori dal recinto: l'SVG stampa 1,5 m, il campo di un esercito diventa 60 × 75 m |
| 4 | Campo Drow 1, Burning Operations (ARC-09, in due file) | alta | 13 tende a 1,5 m l'una dall'altra, tenda comando e cucina a fianco, falò di 13,5 × 4,5 m a 1,5 m dai teli |
| 5 | Cerchio Sacro, Ondata 2, Last Stand (ARC-09) | alta | foresta disegnata in ⬛ (muratura), radura in 🟢 (creature); il «cerchio di 60 m» è un ovale di 35 × 48 m fuori centro, e nelle altre due mappe misura 15 × 30 m |
| 6 | PF-3 Corridoio del Fuoco e PF-4 Forgia Adamantina (ARC-07) | alta | porte murate, 32 nemici dentro la roccia piena, forgia senza ingresso |
| 7 | S-2 Stanza della Corona e CM-1 Cuore della Montagna (ARC-07) | alta | pavimento scritto con ⬛: SVG e UVTT ne fanno un blocco di muratura; porta sud della Corona nel mezzo del pavimento |
| 8 | Campo C, Base di Comando (ARC-09, prosa) | media | tenda 12 × 12 m che contiene il cerchio di evocazione, il portale e le guardie che dovrebbero stare fuori |
| 9 | T-2, T-6 (ARC-07) | media | mostri scritti con ⬛ (Fauci di Diamante, Terros): diventano edifici |
| 10 | 1A-1 Sentiero Nascosto (ARC-08) | media | la «strozzatura di ~9 m» è larga 21 m sulla griglia; il canyon è 21 m percorribili per 150 m |
| 11 | PF-1 Stanza della Corona (ARC-07, UltraClear) | media | 30 × 21 m contro i 15 × 19,5 m canonici dell'ARC-06; bracieri usati come muri |
| 12 | M7-F Fucina grande, M7-D fucina di Gunnvor (ARC-07) | media | una fucina di 36 × 24 m senza un focolare né un'incudine |
| 13 | Foresta in Fiamme, Last Stand, 2B | media | treant e drago su 1 quadretto (Enormi: 3 × 3) |
| 14 | Le altre (Dauth A-E, M7-B, M7-D, M7-E, H3-1, 3Y, 3Z, MAPPA 5, T-3, Tarsilia) | bassa | ritocchi |

---

## 4. Schede per mappa

### ARC-07 · Atlante `07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-DEFINITIVO.md`

Copie identiche in `ARC07-DEF-1/-2/-4/-5` e nei booklet di `homebrew/`.

**T-2 Foresta di Cristalli Giganti** (18 × 10 = 27 × 15 m). Usata da DEF-1 §5:
Thorik F04, Artemis I04, Tordek G05, Xorn G02 e O05, Fauci G09.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| cristalli 🔷 | gruppi 2×3 / 3×3 (3-4,5 m) | sensati come copertura | — |
| Fauci di Diamante | ⬛ in G09, 1 cella | mostro scritto come muratura: l'SVG disegna un pilastro, l'UVTT un muro | media |
| PG 🛡🥋 e 💠 | simboli locali | nel DEF-1 la legenda locale non li dichiara (rilievo E del collaudo) | bassa |
| campo | 27 × 15 m per 3 PG e 3 nemici | giusto | — |

**T-3 Campo dei Cristalli Viventi** (20 × 8 = 30 × 12 m). Skill challenge, DEF-1 §6.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| 🚪 A06 e T06 | porte in campo aperto | ingresso e uscita senza muro: serve un segno di accesso, non una porta | bassa |
| 49 cristalli a scacchiera | 1 ogni 2 celle | leggibile; non è uno scontro | — |

**T-6 Camera dell'Altare, Terros** (24 × 16 = 36 × 24 m, vista equatoriale della
sfera Ø 60 m). DEF-1 §8: Terros K08-M10, Thorik J09, Tordek N08.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| Altare 🟩+🟡 | 9 × 6 = 13,5 × 9 m | coerente con il testo | — |
| Terros | ⬛ 3×3 | Enorme giusto, ma il simbolo è muratura: l'UVTT lo fa muro | media |
| sfera Ø 60 m | la griglia ne mostra 36 × 24 m e nessuna parete | i «27 m dalla soglia» e il «muro curvo» non si misurano sulla carta: segnare l'arco della parete | bassa |

**S-2 Stanza della Corona** (10 × 13 = 15 × 19,5 m). Geometria canonica ARC-06
(`06_.../StanzaCoronaDiAdamantio/Tactics_and_maps.md`). DEF-2 §6, §10; Cassetta del DM.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| pavimento | 88 celle di ⬛ | legenda locale «⬛ = pavimento» contro l'universale «muratura piena»: SVG e UVTT mostrano una stanza piena (rilievo E) | alta |
| ingresso D-F02 | porta tripla 4,5 m in mezzo al pavimento, con la riga 01 ancora stanza | una porta senza muro: la riga 01 va tolta o diventare muro | alta |
| colonne 🔲 | 1 cella, file a 3 m | giusto | — |
| dimensione | 15 × 19,5 m per «vasta navata» | fra Notre-Dame (12 m) e Reims (14,65 m) di larghezza: sta | — |

**M7-B Cortile interno, Skullcrusher** (24 × 18 = 36 × 27 m). DEF-4, Scena 11.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| cortile | 36 × 27 m | giusto per un drago Enorme e 5 PG | — |
| mura 🏰 | 1 cella | sottili per una fortezza nanica (vedi §1), ma è l'interno | bassa |
| porte O04 (2), L18 (2), W18 (1) | 3 m e 1,5 m | giuste | — |
| gru 🏗 B10 e W10, portata 15 m | coerente con il testo | — | — |

**CM-1 Il Cuore della Montagna** (33 × 27 a 3 m = 99 × 81 m). DEF-5, Cassetta del DM.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| pavimento | 683 celle di ⬛ | stesso errore di S-2: caverna resa come blocco pieno; il collaudo dice boss e obiettivi irraggiungibili | alta |
| porta P01-Q01 | 6 m nella roccia del bordo | ok come varco | — |
| misure | 99 × 81 m, coerente con la MAPPA 5 di ARC-08 (100 × 80 m) | giusto; grotta grande ma credibile (Wieliczka 54 × 18 m scavata; grotte naturali molto più grandi) | — |

### ARC-07 · `Mappe/Portale-Forgia-L1-REVISED-UltraClear.md` e `-L2-`

L'indice dell'arco le dice ancora usate per le «stanze storiche»; nessun master
DEF cita PF-1, PF-2, PF-3. PF-4 è citata da `RicalibrazioneScontriPianoDelFuoco.md`.

**PF-1 Stanza della Corona** (20 × 14 = 30 × 21 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| stanza | 12 × 11 celle = 18 × 16,5 m utili | non è la geometria canonica (15 × 19,5 m, 10 × 13) e ha un altro orientamento: due Stanze della Corona diverse | media |
| bracieri 🏮 | file di 11 celle (O3-R13), blocchi 3×3 | bracieri usati come muri: 22 bracieri su un fianco | media |
| muri | 3 colonne per lato (4,5 m) | roccia, accettabile | — |

**PF-2 Sala della Forgia Eterna** (27 × 27 = 40,5 m). Coerente con l'ottagono
Ø 40 m dell'Atlante (S-1). Bassa: macerie 🪨 come anello continuo lungo tutto il
muro, che sembra una seconda parete.

**PF-3 Corridoio del Fuoco «[COLONNA K]»** (21 × 53 = 31,5 × 79,5 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| corridoio | 7 celle = 10,5 m × 79,5 m di fuoco | largo come una navata: è una sala, non un corridoio | media |
| 4 porte agli angoli A01, S01, A53, S53 | 4,5 m, dentro 7 colonne di roccia piena | murate (collaudo E): non si entra | alta |
| 32 nemici 🔴 | colonne D16-D26, R36-R43, dentro la roccia ⬛ | nemici dentro il muro | alta |

**PF-4 Forgia Adamantina** (33 × 33 = 49,5 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| porta O01-Q01 | 4,5 m, seguita da 2 righe di roccia | murata: la sala non ha ingresso | alta |
| sala | ottagono di ~46 m | enorme per un elementale Enorme; si gioca ma è vuota per metà | bassa |

### ARC-07 · `Mappe/hammerfist-372-1372/` (M7-D, M7-E, M7-F, versioni 372 e 1372)

Usate da DEF-4 Scena 5 e DEF-5.

**M7-D Il corridoio della fucina, livello −1** (36 × 23 = 54 × 34,5 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| corridoio | 2 righe = 3 m, 51 m | giusto per un'arteria nanica | — |
| quartieri | 7 × 5 = 10,5 × 7,5 m, 6 letti in fila | giusto | — |
| cappella | 8 × 6 = 12 × 9 m | navatella credibile | — |
| sala grande (fucina di Gunnvor) | 14 × 8 = 21 × 12 m, un solo 🔥 (T14) | una fucina senza incudine né focolare segnato | media |
| porte | 1 cella, doppia T13 | giuste | — |

**M7-E Le gallerie di Zeth, livello −2** (34 × 24 = 51 × 36 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| gallerie | 1 cella = 1,5 m | coerenti con i cunicoli di Hallstatt (~2 m) e con «strette, puntellate» | — |
| camera centrale | 5 × 3 attorno al pozzo T14 | piccola ma sensata | — |
| combattimento | tutto in fila indiana | è voluto; scriverlo nel companion | bassa |

**M7-F La fucina grande, livello −3** (30 × 22 = 45 × 33 m)

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| sala | 24 × 16 = 36 × 24 m | coerente con il testo (36 × 24 m, volta alta) | — |
| arredi | 12 bracieri lungo i muri, un tavolo, due barili | **nessun focolare, nessuna incudine, nessun mantice**: è un salone, non una fucina | media |
| pilastri 🟪 | 8, a 6 m | giusti | — |
| fila di 20 nani in riga 5 (372) | 20 celle | schierati come un muro di scudi; ok | — |

### ARC-08 · `08_La Battaglia Di Hammerfist/Mappe/`

Usate da `ARC08-01-GUIDA-DM.md` (righe 1227-2557), `ARC08-04`, `ARC08-10`,
`ARC08-11`, `ARC08-14`, e da DEF-5 di ARC-07 per la MAPPA 5.

**La fortezza di Hammerfist in quattro mappe (alta).** Stessa fortezza, misure
diverse:

| Mappa | Scala | Fronte sud delle mura | Porta | Spessore mura |
|---|---|---|---|---|
| 2A Fortezza top-down (120 × 80) | 1,5 m | 81 celle = 121,5 m | 6 celle = 9 m (tabella: 6 × 3 m) | 1 cella = 1,5 m |
| MAPPA 1 Disposizione (60 × 108) | dichiarata 3 m, resa 1,5 m | 52 celle = 156 m (a 3 m) | 2 celle = 6 m | 2 righe = 6 m |
| MAPPA 4 Battaglia finale (60 × 68) | 3 m | 52 celle = 156 m | 2 celle = 6 m | 2 righe = 6 m |
| 2B Bastioni (40 × 26) | 1,5 m | — | — | parapetto + 3 righe + muro = 7,5 m |

**2A Fortezza top-down** (180 × 120 m). GUIDA-DM righe 1496-1536; tabella
postazioni.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| cortina | 1,5 m di spessore, «12 m» di altezza | Beaumaris: 3 m per 10,7 m; Caernarfon fino a 6 m. Per una fortezza nanica 3-4,5 m (2-3 celle) | alta |
| ponte levatoio BE74-BJ75 | 9 × 3 m, sulle righe 74-75 | il fossato comincia in riga 76: il ponte sta sulla terra e non scavalca niente; la tabella dice 9 × 4,5 m su un fossato di 6 m, ancora corto | alta |
| cancello BE72-BJ73 | 9 m (griglia) contro 6 m (tabella) | la luce reale è ~3 m (carro e cavallo); per una porta nanica 4,5-6 m | media |
| bastioni G1/G2 | 6 × 4,5 m = 12 celle «40 nani + 2 baliste» | 40 Medi chiedono 40 celle: sovraffollato di 3-4 volte | alta |
| bastioni B1/B2 | 6 × 4,5 m, 20 nani + 1 balista | stesso problema | media |
| torri H61, CL61 | 4 × 2 di 🗼 + 4 × 2 di PG = 6 × 6 m, «20 m» | Carcassonne 4,5-7 m per 11-14 m; 6 m per 20 m è snella ma possibile | bassa |
| cortile interno | 79 × 21 = 118 × 31 m | ampio, giusto per una battaglia di massa | — |

**MAPPA 1 Disposizione Generale Giorno 1** (60 × 108). GUIDA-DM riga 1453
(«griglia di regia 60×108, 3 m/q»).

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| scala | il testo dice 3 m/q e «180 × 324 m»; nel recinto manca `· 3 m`; l'SVG stampa «scala 1,5 m/quadretto» e 162 m | barra di scala falsa per il DM | alta |
| titolo «0-300 m» | 108 righe a 3 m = 324 m | coerente solo a 3 m | — |
| tenda ⛺ Z62 | 3 × 3 = 9 m a 3 m/q | tenda di comando credibile se a 3 m; resa a 1,5 m diventa 4,5 m | bassa |

**MAPPA 4 Battaglia finale terrestre** (60 × 68 a 3 m = 180 × 204 m). GUIDA-DM
riga 191, 2557. Scala dichiarata e resa giuste. Il problema è solo la differenza
con 2A (fronte 156 m contro 121,5 m).

**2B-CORRETTA Attacco del drago sui bastioni** (40 × 26 = 60 × 39 m). GUIDA-DM
righe 1833-1866.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| camminamento | 3 righe = 4,5 m fra parapetto e muro interno | largo; con il muro sono 7,5 m, contro 1,5 m in 2A | media |
| drago 🟣 U01 | 1 cella | un drago Enorme occupa 3 × 3 | media |
| porta W15 | in cortile aperto | porta senza muro (collaudo E) | bassa |

**1A-3 Campo della Mano Rossa** (40 × 50). GUIDA-DM riga 1302 («griglia
strategica 40×50, 6 m/q»). Fuori dal mio perimetro se è la mappa che l'altro
agente sta rifacendo; la includo perché è il campo del 1372, non l'orda del 372.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| scala | testo 6 m/q, «240 × 300 m»; il recinto non lo dice; l'SVG stampa 1,5 m e 60 × 75 m | l'accampamento di un esercito reso grande come un cortile | alta |
| tenda ⛺ Q29-R31 | 2 × 3 celle: 3 × 4,5 m a 1,5 m, 12 × 18 m a 6 m | a 6 m è un padiglione da più pali, non una tenda a un palo; va segnata come simbolo | media |
| accampamento | una sola tenda per un esercito | manca il campo: file di tende, strade, recinto (vedi §1, accampamento romano) | media |

**1A-2 Il Torrione di Vedetta** (40 × 40 = 60 × 60 m). GUIDA-DM riga 1263.
Torre 4 × 4 = 6 × 6 m per 18 m di altezza: snella ma nella forbice di Carcassonne.
Nessuna porta e nessun interno: si scala da fuori (Scalare CD 12), quindi va bene.
I PNG si chiamano ancora Dara, Borin, Thorin, Nala. Bassa.

**1A-1 Il Sentiero Nascosto** (20 × 100 = 30 × 150 m). GUIDA-DM riga 1228.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| canyon | 2 colonne di monte per lato, 14 celle percorribili = 21 m | il testo parla di canyon e di una «strozzatura di ~9 m» alle righe 10-14, dove la griglia ha ancora 14 celle libere | media |
| sentiero | 4 celle = 6 m | una mulattiera è larga 1,5-3 m | bassa |

**H3-1 Cortile sfondato** (40 × 40 = 60 × 60 m). GUIDA-DM riga 1994, ARC08-10.
Mura di 1 cella con due brecce di 15 m ai lati (righe 16-25): coerenti con
«sfondato». Statua 4 × 3 = 6 × 4,5 m davanti alla porta R01: grande ma è un
monumento. Bassa.

**3Y Il Ponte Sospeso** (33 × 27 = 49,5 × 40,5 m). Ponte 2 × 10 = 3 × 15 m su un
abisso di 15 m: per un ponte di corde è largo (1-1,5 m), per un ponte nanico in
pietra è giusto (Valentré 5 m). Porta Q01 senza muro ai lati. Bassa.

**3Z L'Incrocio Silenzioso** (33 × 33 = 49,5 m). GUIDA-DM riga 2061. Sei tunnel di
3 celle (4,5 m) che finiscono con una porta di 1 cella senza muro accanto (collaudo
E su tutte e sei): una porta stretta in fondo a un tunnel largo. Si gioca. Bassa.

**MAPPA 5 Il Cuore della Montagna** (67 × 53 = 100,5 × 79,5 m). GUIDA-DM righe
2164-2434, ARC08-11, DEF-5. Sala ellittica di ~76 × 64 m, porta di 6 celle (9 m)
cerimoniale. Coerente con CM-1. Bassa.

### ARC-09 · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/`

**Campo Drow 1, Burning Operations Base** (53 × 40 = 79,5 × 60 m). In
`SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` mappa 1 e, identica, in
`Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md` mappa 1. Citata da
`ERRATA-PARTE1-Quest-Hellas-35-Verification.md`, `INDICE-GENERALE-COMPLETO-CAMPAGNA.md`.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| 13 tende I10-AC18 | 3 × 3 = 4,5 m, distanziate di 1 cella | la tenda è credibile (il contubernium romano è 3 m per 8 uomini), la distanza no: i tiranti chiedono ~1,5 m per parte, cioè 2 celle fra un telo e l'altro | alta |
| tenda del comando H24-T27 | anello di 13 × 4 = 19,5 × 6 m | tenda lunga e sottile disegnata come recinto; un padiglione di comando realistico è 6-10 m | media |
| cucina H29-T31 | 13 × 3 = 19,5 × 4,5 m, 1 riga sotto il comando | **tenda attaccata alla tenda principale**, il caso segnalato dal DM | alta |
| falò M20-U22 | 9 × 3 = 13,5 × 4,5 m, testo «diametro 10,5 m, 2d6 entro 3 m» | il falò è a 1 riga dalle tende delle righe 18 e 24: i teli stanno nella fascia dei 2d6 | alta |

**Campo Drow 2, Forward Base** (65 × 53 = 97,5 × 79,5 m). Stesso file, mappa 2.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| interno della palizzata | 45 × 44 celle di ⬛ | tutto il campo è muratura piena: le 25 tende, il recinto ogre e la tenda del Wyrmlord sono solo nel testo; boss, tesoro e prigionieri irraggiungibili (collaudo E) | alta |
| cancello nord AB07 | 5 celle = 7,5 m | largo come la porta di un castrum con le torri; per una palizzata 3-4,5 m | media |
| cancello sud | annotato (AD48), non disegnato | manca | media |
| torretta AB12 | 3 × 3 = 4,5 m, 9 m alta | giusta | — |

**Cerchio Sacro della Foresta** (`Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO-maps.md`,
40 × 40 = 60 × 60 m). Citato in 24 file, fra cui ARC07-DEF-3 e DEF-5.

| Elemento | Misura | Giudizio | Gravità |
|---|---|---|---|
| foresta | 674 celle di ⬛ | la foresta è resa come edificio pieno | alta |
| radura | 602 celle di 🟢 «creatura evocata» | il terreno è scritto come mostri: l'SVG la riempie di gettoni | alta |
| cerchio «Ø 60 m» | radura 23 × 32 = 35 × 48 m, spostata a ovest (colonne B-AB) | non è un cerchio di 60 m e non è centrato | media |
| porta O02-Q02 | 3 celle nel bosco | un varco nel bosco, non una porta | bassa |

**Ondata 2 Positions** e **Desperate Last Stand** (`...P1C-Rituale-COMPLETO-SCALE.md`
mappe 2 e 3, 26 × 26 e 26 × 29). Stesso cerchio in un'altra misura: 10 × 20 celle
= 15 × 30 m, contro i 60 m della mappa madre (media). Radura in 🟢 (alta, come
sopra). Treant 🌳 in blocchi di 2 × 1: un treant è Enorme, 3 × 3 (media).
Simbolo 🌱 non dichiarato.

**Foresta in Fiamme** (`Arco-Post-Hammerfist-P1B-Foresta-In-Fiamme-MAPPA.md`,
34 × 24 = 51 × 36 m). Nessun master la cita. Tre treant 🌳 su una cella sola
(L8, S9, P17): Enormi, vanno 3 × 3 (media). Il resto è sensato: radura di 28 m,
fronte di fuoco di 6 × 15 m.

**Dauth, carte A-E** (`Mappe/dauth-assedio/`). Usate da
`...DAUTH-DAY3-CITY-SIEGE.md`, `...SUBQUEST-Thorik.md`, `...P3-BATTAGLIA-FINALE-EVENT-DECK.md`.

| Carta | Misura | Giudizio | Gravità |
|---|---|---|---|
| A Breccia della Porta Sud | 18 × 13,5 m; varco 4,5 m in mura di 3 m; torri 4,5 × 4,5 m | giusta; torri di porta piccole (Carcassonne 4,5-7 m) | bassa |
| B Razorfiend sui bastioni | camminamento 6 m, merli alternati a 1,5 m | camminamento largo, merli giusti | bassa |
| C1 Chiostro-ospedale | 15 × 15 m, giardino 6 × 6 m, 16 letti | piccolo ma credibile | — |
| C2 Cunicolo della cisterna | 4,5 m con canale d'acqua | giusto | — |
| D Lance di Khorn | torri 🗼 A02 e N02 di 1 cella | una torre di 1,5 m non esiste: è una scala o una garitta | bassa |
| E Cellula nelle mura | corpo di guardia 6 × 4,5 m | giusto | — |

**Mappe in prosa di ARC-09** (nessuna griglia, scala 1,5 m dichiarata):

| File | Misure dichiarate | Giudizio | Gravità |
|---|---|---|---|
| `P1-MAPPE-COMPLETO` Campo C | tenda 8 × 8 = 12 × 12 m centrata su (20,20); cerchio d'evocazione (18,20), portale r 3 su (16,20), guardie (18,18)-(22,22) | cerchio, portale e guardie «agli angoli» cadono **dentro** la tenda; un padiglione di 12 m chiede più pali | media |
| `P1-MAPPE-COMPLETO` Campi A, B; Cerchio | palizzata r 10 (30 m), piattaforma Ø 15 m | sensate | — |
| `P2A-Torre` 1-4 | stanze 18-20 q (27-30 m), corridoio 6 × 45 m, volta ≥ 15 m | grandi ma da torre magica; ok | bassa |
| `P2B-Torneo` 1 e 2 | arena Ø 60 m, cancelli 4,5-6 m | ampia per un duello; ok | bassa |
| `P2D-PALIO` | «1 quadretto = 5 ft» | unità in piedi in una campagna in metri: scrivere 1,5 m | bassa |
| `P3-FASE0-4` | griglie 20-60 q, cerchi Ø 18 m, trincea 3 m | sensate | — |
| `P3-Ghostlord` | Leone di pietra 30 × 15 m, Sala del trono 30 × 30 m | ok | — |
| `P3-Sabotaggio` | corridoio 6 m con carri 3 × 4,5 m, ponte 6 × 15-18 m | ok | — |
| `P3-Starsong-Hill` | collina Ø 45 m, tende 3 × 3 m | ok | — |

### Il Drappo di Tarsilia (modulo autonomo PF1e)

**La Ruota** e **versione giocatori** (64 × 46 = 96 × 69 m). Pista 🟫 larga 9-12
celle (13,5-18 m), blocco centrale ⬛ 42 × 27 m. Pista larga per otto cavalli
Grandi (2 × 2): sensata. Porte BD14 e J42 senza muro (collaudo E). Bassa.

**Le stalle dell'Istrice** (21 × 15 = 31,5 × 22,5 m). Box 3 × 4 celle (4,5 × 6 m)
per un cavallo Grande: un box reale è sui 3,5 m di lato, qui c'è spazio per il
combattimento. Porte dei box in muretti bassi (collaudo E). Bassa.

### Tavole SVG disegnate a mano (non misurabili da griglia)

`10-stand-alone/L'abbazia Della Rotta Sicura/tavole/*.svg` (scala in piedi,
«1 quadr. = 5 ft», profilo «2.400 ft»), `P2D-Palio-Allegati/mappe/*.svg`
(«1 quadretto = 5 ft»), `03_la Cittadella/01_Il Guardiano/temple-map-revised.svg`
(15 × 30 m, 24 m di altezza: navata da tempio grande, sta). Unica nota: le unità
in piedi; da allineare a 1,5 m se rientrano nella campagna.

### Archivio (superato, non misurato in dettaglio)

`08_.../Mappe/_ARCHIVIO/Hammerfist-Lotto-1/2/3*.md`: l'intestazione del Lotto 2
dichiara 120 × 80 e disegna 34 × 80. `07_.../Mappe/_ARCHIVIO/Portale-Forgia-L3`
e `TACTICAL-GRIDS-COMPLETE`: niente griglia emoji. Da non usare.

---

## 5. Note per chi rifà le mappe

- Partire dal JSON in metri (`units_in: "meters"`, `references/tre-modalita-mappe.md`)
  con le misure del §1, non dai quadretti.
- Fortezza di Hammerfist: decidere una volta sola fronte sud, porta, fossato e
  spessore delle mura e portarli in 2A, MAPPA 1, MAPPA 4 e 2B. Proposta da
  discutere col DM: cortina 3-4,5 m con camminamento 3 m, porta 4,5-6 m fra due
  torri da 6-7 m, ponte levatoio più lungo del fossato.
- Accampamenti: tenda di truppa 2 × 2 (3 m), tenda di ufficiale 3 × 3, padiglione
  di comando 5 × 5-7 × 7 a più pali; 2 celle libere fra un telo e l'altro, strade
  di 2-4 celle, falò di 1-2 celle ad almeno 3 celle dai teli, uno spazio vuoto fra
  palizzata e prime tende (l'intervallum romano).
- Nessun pavimento, mostro o tenda in ⬛; nessun terreno in 🟢. Il collaudo lo
  segnala già come `legenda/funzione-opposta`.
- Mettere `· S m` nell'intestazione del recinto di ogni mappa strategica.

Durante questo giro l'albero di lavoro aveva già modifiche non mie in
`scripts/legend.json`, `scripts/legend.yaml`, `scripts/render_map_svg.py` e
`references/legenda-universale.md` (presumibilmente l'agente della M7-C): le
misure sopra sono state prese con quella versione del renderer.

---

## 6. Il secondo giro (2026-10-21): ARC-07 e ARC-09

Rifatte le mappe di gravità alta e media di ARC-07 e ARC-09. ARC-08, la M7-A e
la M7-C sono di un altro thread e non sono state toccate; per questo restano
aperte la 2B (drago su una cella) e le misure della fortezza di Hammerfist.

### Fonti aggiunte

| Fonte | Cosa dà | Dove è servita |
|---|---|---|
| [Nebraska Forest Service, *Fires and camping*](https://nfs.unl.edu/fires-and-camping/) | 15 ft (4,5 m) sgombri attorno a tende ed edifici, 5 ft attorno al fuoco, legna a 15 ft | fuochi dei Campi Drow 1 e 2 |
| [FortWiki, Fort Boonesborough](https://www.fortwiki.com/Fort_Boonesborough) | palizzata di 250 × 150 ft con fortini agli angoli | palizzata e torrette del Campo 2 |
| [Curle, Newstead](https://curlesnewstead.org.uk/31.htm) | varco della porta romana ristretto a ~12 ft | cancelli di 4,5 m del Campo 2 |
| [Wikipedia, Ring of Brodgar](https://en.wikipedia.org/wiki/Ring_of_Brodgar) e [Castlerigg](https://en.wikipedia.org/wiki/Castlerigg_stone_circle) | cerchi di pietre da 104 m e da 32,6 × 29,5 m, pietre alte fino a 2,3 m | il Cerchio Sacro di 60 m con otto menhir |
| [Birthright wiki, D20 Treant](https://birthright.net/wiki/index.php/Treant) | treant Enorme, spazio e portata 15 ft | treant 3 × 3 nel Cerchio, nel Last Stand e nella Foresta in Fiamme |
| [Wikipedia, Lava tube](https://en.wikipedia.org/wiki/Lava_tube) | tubi di lava larghi fino a 15 m, gradini di colata lungo le pareti | il Corridoio del Fuoco PF-3 |
| [IFI, *Tool & equipment layout*](https://www.iforgeiron.com/topic/22450-tool-38-equpiment-layout-38-setup/) | dalla forgia all'incudine si arriva con un passo | incudini di M7-D e M7-F |

### Cosa è cambiato

| Mappa | Prima | Dopo |
|---|---|---|
| Campo Drow 2 (SUPPLEMENTO) | interno di 45 × 44 celle in ⬛, cancello murato, distanza 28 | palizzata 🏰 di 67,5 × 60 m, quattro torrette, cancelli di 4,5 m, 25 tende 🎪 a 3 m l'una dall'altra, padiglione del Wyrmlord di 10,5 × 7,5 m; distanza 0 |
| Campo Drow 1 (SUPPLEMENTO e P1C-Rituale) | 13 tende a 1,5 m, comando e cucina attaccati, inceneritore a una riga dai teli | 15 tende a 3 m attorno alla piazza, inceneritore a 10,5 m dalla tenda più vicina, comando e cucina staccati |
| Cerchio Sacro, Ondata 2, Last Stand (P1B, P1C) | foresta in ⬛, radura in 🟢, cerchio ovale di 35 × 48 m, tre misure diverse | tre griglie 40 × 40 con lo stesso disco di 60 m; colonne +5 nel testo |
| PF-3 Corridoio del Fuoco | 21 righe su 53, cenge in ⬛, porte e nemici nella roccia | 53 righe, lava 10,5 m, cenge 🟤 di 3 m, pianerottoli di 6 m, ponti 🌉 di 10,5 × 3 m |
| PF-4 Forgia Adamantina | porta su due righe di roccia | androne O02-Q03, roccia 🏰, anello ⬜, passerelle 🌉 |
| PF-1 Stanza della Corona | 40 bracieri a muro, erba, dais in ⬛ | sala ⬜, dais 🔳, otto torce |
| S-2 (Atlante e DEF-2) | pavimento ⬛, porta D-F02 in mezzo al pavimento | pavimento ⬜, porta nel muro sud, androne D-F01; posizioni canoniche invariate |
| CM-1 (Atlante e DEF-5) | pavimento ⬛, pareti 🪨 | pavimento 🟤, pareti 🏰; da distanza 19 a 0 |
| T-2 e T-6 (Atlante e DEF-1) | Fauci di Diamante e Terros in ⬛ | 🟣, Fauci Grande G09-H10, Terros Enorme K08-M10 |
| M7-D e M7-F (372 e 1372) | forge senza incudine | un'incudine ⚒ davanti a ogni forgia; gli orchi della M7-F/1372 scendono di due righe |
| Foresta in Fiamme | treant su una cella | treant 3 × 3, anche l'alleato di Hella |
| Campo C (P1-MAPPE, prosa) | tenda di 12 m che conteneva cerchio, portale e guardie | tenda spostata a est, 4,5 m fra portale e telo |
