# ARC-07 · Il barile sulla tenda di Zog'tar

> **Che cos'è.** Il supplemento alle Scene 7 e 8 di DEF-4<!-- apparato --> (`ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`)<!-- /apparato -->
> per quello che il tavolo ha fatto davvero: invece di entrare nella tenda del
> comando, i PG ci hanno lasciato cadere sopra, da 48 m e invisibili, una botte
> d'olio piena di sassi, con i rostri dei fabbri nanici sotto e le fiale della
> fenice legate con le corde. In apertura c'è la **scheda da tavolo**, dieci
> passi da tirare senza improvvisare; poi la caduta e la deviazione, i danni
> della caduta, dell'olio e delle palle di fuoco e l'area che coprono, tutto
> rifatto per la quota da cui il tavolo rigioca lo sgancio, il telo e i rostri, le 25
> cadute possibili sopra il palo centrale, che cosa vedono i PG da 48 m e chi
> li può trovare, quando si tira l'iniziativa e che cosa fanno le rune, le
> tattiche di chi è dentro e del campo, round per round, chi suona il corno se
> Grask muore, i
> due barilotti da 10 litri e una procedura, con i PE, per le trovate dei
> giocatori delle prossime volte.
>
> **Le mappe** sono M7-C, lo spiazzo del capo con la tenda, e M7-H, il campo
> attorno<!-- apparato --> (`Mappe/`)<!-- /apparato -->. Le coordinate di questo documento sono quelle di M7-C; su
> M7-H si sommano otto colonne e otto righe.
>
> **Da dove vengono i numeri.** Dall'SRD 3.5. Dove l'SRD non ha una regola per
> quello che è successo, c'è una **variazione**, segnata come tale e costruita
> su una regola dell'SRD vicina; quando le letture possibili sono due, vale la
> più forte, come vuole il DM. Le probabilità vengono da 20.000 prove di una
> simulazione che usa queste stesse regole<!-- storico -->
> (`plans/esperimenti/barile-zogtar-2026-10-24/simula_barile.py`; i risultati
> completi sono in `ESITI-SIMULAZIONE.md`, nella stessa cartella)<!-- /storico -->.

## La scheda da tavolo

Dieci passi, nell'ordine in cui si tirano. Ogni riga dice da quale regola
dell'SRD viene; le variazioni sono segnate ◆ e sono le scelte del DM B4, B5, B6,
B12 e B16. I dadi delle righe 2 e 3 dipendono dalla quota da cui i PG
sganciano: la tabella è nel §2-bis. Con questa scheda il DM non deve inventare niente: tira i dadi
della colonna di destra.

<!-- pagina: una-colonna -->

| # | Che cosa | Regola | Si tira |
|---|---|---|---|
| 1 | **Lo sgancio** | Non è un attacco (SRD, *invisibilità*: chi causa danno in modo indiretto non attacca). È un'azione gratuita, e chi sgancia resta invisibile. Si può fare nel round di sorpresa, e tutti e quattro i PG possono sganciare nello stesso round | niente |
| 2 | **Dove cade** | Non si mira: la deviazione è l'attrito dell'aria più quanto chi sgancia era spostato dalla verticale. Come l'arma a spargimento che manca (SRD): 1d8 per la direzione, 1 = nord e poi in senso orario. ◆ La distanza dipende dalla **quota**, dal peso e da che cosa vede chi sgancia (§2 e §2-bis): da 48 m la botte, sopra la tenda illuminata dai fuochi, 1d4−1 quadretti, un barilotto 1d6−1; se chi sgancia non vede il bersaglio, un dado in più. Se si è mosso in quel round, in più 6 quadretti nella direzione del volo | **1d8** e il dado della quota (§2-bis); da 48 m **1d4−1**, barilotto **1d6−1** |
| 3 | **Che cosa prende** | Il telo non la ferma: i rostri lo tagliano e toglie solo 3 danni (§3). Una creatura nella casella: oggetto in caduta (SRD), senza TS, meno la RD; ◆ in più le lame dei rostri, 1d4 lame da 1d8, nello stesso colpo. La riga 12, cioè un palo in cima (K12, N12, Q12) o la trave del colmo: la botte prende il legno, durezza 5 e 60 pf (SRD, §3). Se lo spezza, la tenda crolla subito; se no gli si apre sopra, e sotto nessuno prende il colpo diretto | i dadi della quota (§2-bis): da 48 m **15d6** − 3 + **1d4 × 1d8** (barilotto 3d6 − 3); sul legno **13d6 + 1d4 × 1d8 − 5**, si spezza a 60 |
| 4 | **Le fiale** | Si rompono sempre: prendono anche loro i 15d6 della caduta, e il vetro ha 1 pf. Ogni fiala è una *palla di fuoco* (SRD). L'origine è un angolo della casella d'impatto (d4, o quello che sceglie il DM). ◆ Sotto il telo la tenda fa da forno: chi è dentro la tenda è nell'area. Fuori dal telo valgono i 6 m dall'angolo | **6d6 per fiala**, **Riflessi CD 14** dimezza, un TS per fiala |
| 5 | **L'olio, subito** | Il **cuore** è la casella d'impatto e le otto attorno: chi c'è è colpito in pieno, come da un'ampolla d'olio (SRD, fuoco dell'alchimista), e prende fuoco ◆ senza TS. Il resto dell'olio copre **tutto il pavimento della tenda** (all'aperto: fino a 7 m): chi c'è prende lo spruzzo | cuore **1d6**; resto **1** |
| 6 | **L'olio, ogni round** | La palla di fuoco lo accende tutto nello stesso istante. Chi sta nell'olio che brucia prende 1d3 (SRD, la pinta versata) e tira per non prendere fuoco (SRD, «Catching on Fire»). Chi è nel cuore prende il secondo 1d6 dell'ampolla al round dopo l'impatto. ◆ Il cuore brucia 10 round, il resto del pavimento 3 (all'aperto 2) | **1d3**, **Riflessi CD 15** |
| 7 | **Chi brucia** | SRD, «Catching on Fire»: 1d6 a round, un TS a round per spegnersi; rotolarsi a terra dà +4, ma non dentro l'olio, che riaccende. Un mantello addosso, gettato da un altro, dà +4 come il rotolarsi | **1d6** a round, **Riflessi CD 15** |
| 8 | **Il crollo** | Se non è già crollata, la tenda crolla alla fine del round 1d4+1. Chi è sotto il telo che cade prende il fuoco del telo, è intralciato e per uscire tira un TS a round, con 1d6 a ogni round sotto `[Regola della casa, costruita sullo stato F di M7-C]` | **2d6**, **Riflessi CD 15** |
| 9 | **Il fumo** | SRD, «Smoke Effects», sotto il telo: chi fallisce passa il round a tossire, due round di fila fanno 1d6 non letali; occultamento 20% per tutti | **Tempra CD 15**, +1 per prova |
| 10 | **Il danno massiccio** | SRD 3.5: 50 danni o più da un solo attacco, e chi fallisce muore; un 1 naturale fallisce sempre. ◆ Le palle di fuoco nate insieme contano come un attacco solo; il colpo diretto e l'olio restano a parte | **Tempra CD 15** |

<!-- /pagina -->

**Due conti da avere in testa.** Il colpo diretto da 15d6 fa 50 o più due
volte su tre. Due palle di fuoco fanno 42 in media a chi fallisce tutti e due i
TS, 21 a chi li supera.

## 1. Che cosa hanno fatto, e che cosa si suppone

Il racconto del DM, messo in ordine:

- I PG volano sopra il campo, invisibili, a **48 m** di quota, in una notte
  stellata. Partono dalla postierla in volo, come nella variante «dall'alto»
  della Scena 6.
- Lasciano cadere **una botte da 59 litri**: in fondo sassi, sopra **50 litri
  d'olio**, e sotto il fondo i **rostri**, lame forgiate dai fabbri nanici di
  Hammerfist. Alla botte sono legate con le corde le **fiale della fenice**, da
  6d6 con l'effetto di una *palla di fuoco*.
- Tengono in mano **due barilotti da 10 litri**, senza rostri e senza sassi,
  ciascuno con le sue fiale della fenice legate.
- Vogliono squarciare la tenda di Zog'tar.

Quello che il racconto non dice si suppone così, e ogni supposizione è una
scelta del DM:

- Le fiale sulla botte sono **due**. Le tabelle danno anche una e tre.
- Una fiala della fenice **scoppia quando si rompe**: il vetro che va in pezzi
  è l'innesco, come per un'ampolla di fuoco dell'alchimista.
- Nella tenda c'è la **disposizione A** di M7-C (Scena 7): Zog'tar sul seggio
  che racconta, le quattro guardie attorno, Balvar che incide, il sacerdote
  che dorme, Grask fuori.
- Chi sgancia **sta fermo in aria**. La pozione di *volare* dà manovrabilità
  buona, e con la manovrabilità buona si resta sospesi (SRD, movimento
  aereo).

## 2. La caduta e dove finisce il barile

| | Botte (circa 93 kg, 205 libbre) | Barilotto (circa 14 kg, 31 libbre) |
|---|---|---|
| Quota | 48 m, 157 piedi | 48 m |
| Tempo di caduta | 3,15 s | 3,18 s |
| Velocità all'impatto | 30 m/s, 109 km/h | 29 m/s |
| Energia | 40 kJ | 6 kJ |
| Deriva con 5 m/s di vento laterale | 20 cm | 40 cm |
| Spostamento se chi sgancia vola a 18 m per round | 9,5 m in avanti | 9,5 m |

L'aria quasi non frena una botte così pesante: la velocità finale è il 98%
di quella nel vuoto, e il vento di una notte di pianura la sposta meno di un
quadretto. Contano due cose: se chi sgancia si muove, e quanto l'attrito e il
buio lo portano lontano dalla verticale.

**Nessun tiro per colpire.** L'SRD dice che chi è invisibile e «causa danno in
modo indiretto» non attacca: l'esempio è chi taglia le corde di un ponte con i
nemici sopra. Lasciar cadere un barile è lo stesso gesto. Non è un attacco,
quindi non c'è tiro per colpire, l'invisibilità resta, e lasciarlo andare è
un'azione gratuita.

**La deviazione** `[Variazione sull'SRD, B4]`.
I PG non mirano: lasciano andare. Il barile finisce lontano dalla verticale
per due ragioni, e la regola le mette tutte e due in un dado solo.

- **L'attrito.** Un oggetto pesante e compatto cade quasi dritto; uno leggero
  e storto si gira, e l'aria lo spinge di lato. La botte coi sassi in fondo
  cade sui rostri come una freccia sulla punta: a 30 m/s l'aria la frena del
  12% del suo peso, e se la spinge di lato la sposta di 0,5-2 m. Un barilotto
  da 14 kg senza sassi rotola: l'aria lo frena del 30%, e lo sposta di 1,5-4
  m.
- **La luce.** Chi sgancia sa di essere sopra il bersaglio solo se lo vede. A
  48 m la scurovisione non arriva (18 m) e le stelle non bastano: si vedono
  solo i fuochi, e ciò che illuminano. La tenda si vede, nera in mezzo ai due
  falò della guardia e al fuoco del consiglio. Un punto fuori dalla luce non
  si vede, e si sgancia a stima.

L'SRD ha una regola sola per un oggetto che cade dove non si voleva, l'arma a
spargimento che manca: **1d8 per la direzione** (1 è il nord, poi in senso
orario) e una distanza in quadretti. La distanza, da 48 m, è questa:

| Che cosa cade (le fasce di peso degli oggetti in caduta, SRD) | Bersaglio nella luce di un fuoco | Bersaglio al buio |
|---|---|---|
| pesante e compatto, 200 libbre (91 kg) o più: la botte con i sassi | **1d4−1** quadretti (0-4,5 m) | 1d6−1 (0-7,5 m) |
| medio, da 31 a 200 libbre: i barilotti da 14 kg | **1d6−1** (0-7,5 m) | 1d8−1 (0-10,5 m) |
| leggero o storto, sotto le 31 libbre | 1d8−1 (0-10,5 m) | 1d10−1 (0-13,5 m) |

- Da più in alto o più in basso: un dado in più o in meno ogni 15 m di
  differenza dai 48 (sotto i 15 m non si devia).
- In diagonale lo stesso numero di quadretti è più lontano: tre quadretti in
  diagonale sono 6,4 m.
- Se chi sgancia si è mosso in quel round, la botte conserva la sua velocità:
  in più, 6 quadretti nella direzione del volo, e la tenda si manca.

Il conto della fisica sta nella simulazione<!-- apparato --> (`simula_barile.py`)<!-- /apparato -->; la regola lo arrotonda per
eccesso, perché al buio si sbaglia anche il punto da cui si parte.

## 2-bis. Rigiocare lo sgancio: tutto dalla quota

Il DM farà rigiocare lo sgancio, e la quota la scelgono i PG. Da quella
dipendono tre cose: quanti dadi fa la botte a chi sta sotto, quanto devia, e
chi dei PG vede davvero dove la lascia andare. Più in basso si vede meglio e
si sbaglia meno, ma la botte fa meno male, e dal round dopo i PG sono a
portata del campo.

**Prima: chi vede che cosa, al buio.** La notte è stellata, ma le stelle non
fanno luce per l'SRD: a occhio nudo si vedono le sagome contro i fuochi, non il
punto dove lasciar andare la botte. Le luci attorno alla tenda, su M7-C:

| Fuoco | Luce (come una torcia dell'SRD) | Che cosa illumina della tenda |
|---|---|---|
| i due falò della guardia, H17 e T17 | intensa entro 6 m, fioca fino a 12 m | gli angoli sud del telo. La cima del palo centrale è a 11,7 m da ciascuno in pianta e a 6 m d'altezza: **13,2 m, appena fuori**. Grask, a P16, è a 4 m da T17: in piena luce |
| i fuochi delle sentinelle, D12 e X12 | intensa entro 6 m, fioca fino a 12 m | il bordo ovest e il bordo est del telo, non il colmo (15 m) |
| il fuoco del consiglio, N5 | brace: fioca entro 3 m | niente: il telo è a 6 m |
| i due bracieri, L10 e K14 | dentro, sotto il telo nero | da fuori non si vedono |

Chi ha la **visione crepuscolare** vede il doppio lontano con la stessa luce
(SRD): per lui i falò fanno luce fioca fino a 24 m, e il colmo ci sta dentro.
La **scurovisione** si misura fino al colmo, che è a 6 m da terra: chi ha 18 m
di scurovisione vede il colmo da 24 m di quota.

| PG | Che cosa ha | Vede il colmo, da che quota |
|---|---|---|
| **Artemis** | scurovisione 36 m, Vista del Diavolo 18 m e visione crepuscolare, dall'Anello dell'Illuminazione Caotica | **da qualunque quota**, nella luce doppia dei falò; col solo buio fino a 42 m |
| **Thorik** | *Visione del Vero* della Corona, 1 volta al giorno per 10 minuti: vede nel buio, anche magico, e vede gli invisibili | **42 m**, se la attiva prima |
| **Hella** | nana dei sogni, scurovisione 27 m | **33 m** |
| **Tordek** | nano, scurovisione 18 m | **24 m** |

Chi sgancia e vede il colmo usa la colonna «chi vede» della tabella; chi non lo
vede, quella «al buio», un dado in più.

**Lo sgancio guidato** `[CANONE — DM 2026-10-29, B23]`. Se Tordek
tiene la botte e Artemis guida, c'è un problema che al tavolo non si vede
subito: **Artemis vede la tenda, ma non vede Tordek**, perché anche lui è
invisibile. Può dirgli «ora», non «un metro a sinistra».

| Chi sgancia | Chi lo guida | Che colonna usa |
|---|---|---|
| vede il colmo | nessuno | «chi vede» |
| non lo vede | **Thorik con la Visione del Vero**, che vede il colmo e vede anche lui | «chi vede» |
| non lo vede | **Artemis**, che lo tiene per la spalla o è legata a lui con una corda corta | «chi vede», e **1 quadretto in più** nella direzione del d8: lei sa dov'è la sua mano, non dov'è la botte |
| non lo vede | Artemis a voce, senza toccarlo | «al buio»: lei non sa dov'è lui |
| tengono la botte in due, e la lascia andare chi vede | | quella di chi lascia andare |

Da 48 m, Tordek guidato da Artemis con la mano sulla spalla sbaglia di **1d4**
quadretti (da 1 a 4); da solo, al buio, di 1d6−1 (da 0 a 5). Conviene l'ultima
riga: la botte la tengono in due, e la lascia andare Artemis.

Parlare si sente: Ascoltare ha −1 ogni 3 m (SRD). Un sussurro è CD 15
`[CANONE — DM 2026-10-29]`: da 48 m diventa CD 31, e Zog'tar con +11 non lo sente; da 18 m è
CD 21, e lo sente una volta su due.

**La tabella.** Danno dell'oggetto in caduta dall'SRD: la botte con i sassi
pesa 205 libbre, quindi 1d6 più 1d6 ogni 3 m oltre i primi; il barilotto da
31 libbre fa 1d6 ogni 12 m. La botte si apre se il danno della sua stessa
caduta (1d6 ogni 3 m, come chi cade) passa durezza 5 e 10 pf. Deviazione: un
gradino di dado ogni 15 m di caduta, uno in più per il barilotto, uno in più
se chi sgancia non vede il bersaglio (§2).

| Quota | Caduta | Botte: danno a chi sta sotto | 50 o più | La botte si apre | Spezza un palo o la trave | Deviazione: botte nella luce / al buio | Barilotto: danno, deviazione nella luce |
|---|---|---|---:|---:|---:|---|---|
| 48 m | 3,2 s | **15d6** | 68% | 100% | 19% | 1d4−1 / 1d6−1 | 3d6 · 1d6−1 |
| 42 m | 3,0 s | **13d6** | 26% | 100% | 4% | 1d3−1 / 1d4−1 | 3d6 · 1d4−1 |
| 36 m | 2,7 s | **11d6** | 2% | 100% | 0% | 1d3−1 / 1d4−1 | 2d6 · 1d4−1 |
| 30 m | 2,5 s | **9d6** | 0% | 100% | 0% | 1d3−1 / 1d4−1 | 2d6 · 1d4−1 |
| 27 m | 2,4 s | **8d6** | 0% | 100% | 0% | 1d2−1 / 1d3−1 | 2d6 · 1d3−1 |
| 24 m | 2,2 s | **7d6** | 0% | 99% | 0% | 1d2−1 / 1d3−1 | 1d6 · 1d3−1 |
| 18 m | 1,9 s | **5d6** | 0% | 78% | 0% | 1d2−1 / 1d3−1 | 1d6 · 1d3−1 |
| 12 m | 1,6 s | **3d6** | 0% | 9% | 0% | nessuna / 1d2−1 | niente · 1d2−1 |
| 9 m | 1,4 s | **2d6** | 0% | 0% | 0% | nessuna / 1d2−1 | niente · 1d2−1 |

- **Sotto i 18 m la botte può restare intera.** Le fiale si rompono lo stesso
  (il vetro ha 1 pf) e le palle di fuoco scoppiano. Il fuoco apre la botte
  alla fine del round, e l'olio esce al round dopo: niente cuore e niente
  pavimento inzuppato al primo round, solo una pozza di 3 × 3 quadretti attorno
  alla botte che brucia per 10 round.
- **Sopra un palo o sulla trave** la botte cade 6 m in meno, e il danno va al
  legno (§3): da 48 m lo spezza una volta su cinque, da 42 m una volta su
  venticinque, più in basso mai. Se il legno regge, la botte gli si apre sopra.
- **Il danno massiccio** arriva solo dall'alto: due volte su tre da 48 m, una
  volta su quattro da 42, quasi mai sotto.

**Che cosa rischiano i PG, quota per quota.** Al momento dello sgancio
nessuno sta guardando in alto; i rischi valgono dal round dopo.

| Quota | Che cosa li raggiunge |
|---|---|
| sopra i 45 m | niente. Fuori dalla gittata massima dei giavellotti, fuori da ogni scurovisione |
| da 45 a 37 m | i giavellotti, ma solo se qualcuno li vede (il giavellotto con la *luce*, §8) |
| 36 m e sotto | la scurovisione di Skullcrusher, se arriva |
| 19,5 m e sotto | l'*epurare invisibilità* di Balvar: raggio 19,5 m attorno a lui. Se lo lancia, chi è dentro torna visibile |
| 18 m e sotto | la scurovisione di tutto il campo: visibili, li vedono tutti; invisibili, li vede il sacerdote con *vedere invisibilità*. *Comando* del sacerdote a 12 m |
| 9 m e sotto | Osservare CD 20 per notare un invisibile che si muove (SRD) |
| 6 m e sotto | sono dentro la loro stessa palla di fuoco |

**Che cosa succede, quota per quota.** Il barile lasciato cadere sopra il palo
centrale da chi vede il colmo, due fiale; 20.000 prove per riga, fino alla
fine del primo round.

| Quota | La tenda giù subito | La botte resta intera | Zog'tar, pf (mediana) | Il sacerdote morto | Una guardia a terra (M13) | Grask morto |
|---|---:|---:|---:|---:|---:|---:|
| 48 m | 8% | 0% | 250 | 34% | 6% | 30% |
| 42 m | 2% | 0% | 249 | 32% | 7% | 30% |
| 36 m | 0% | 0% | 249 | 33% | 7% | 31% |
| 30 m | 0% | 1% | 249 | 31% | 7% | 29% |
| 27 m | 0% | 4% | 249 | 30% | 9% | 28% |
| 24 m | 0% | 15% | 250 | 29% | 9% | 28% |
| 18 m | 0% | 65% | 257 | 18% | 5% | 28% |
| 12 m | 0% | 100% | 260 | 8% | 0% | 25% |
| 9 m | 0% | 100% | 260 | 9% | 0% | 25% |

**Che cosa vuol dire.** Il danno della botte conta poco: sotto il palo
centrale non c'è nessuno, e quello che uccide è il fuoco, che non dipende dalla
quota. Scendere serve a sbagliare meno, non a fare più male a Zog'tar. Il
crollo subito è raro (una volta su dodici da 48 m, mai sotto i 36), ma la tenda
crolla comunque alla fine del round 1d4+1. Sotto i 24 m la botte resta intera
sempre più spesso, l'olio esce un round dopo, e il sacerdote se la cava: da 18 m
muore una volta su cinque invece di una su tre. La quota buona, se il
DM vuole un consiglio da dare, è **fra 30 e 36 m**, con Artemis o Thorik che
sgancia: vedono la tenda anche dove i falò non arrivano, la deviazione scende a
1d3−1, la botte si apre sempre, e restano fuori da tutto quello che il campo può
fare.

## 3. Il telo, il colmo e i rostri

**Il telo non la ferma, e non la rallenta.** La botte arriva a 30 m/s con
40 kJ. Per tagliare un telo di pelle con la punta di una lama bastano poche
centinaia di joule: il telo le toglie meno dell'1% dell'energia, mezzo punto
percentuale di velocità. Nell'SRD la pelle ha durezza 2 e 5 pf per pollice di
spessore; un telo di 6 mm ha 1 pf. Al tavolo vale così: **il telo toglie 3 danni
al colpo diretto** (durezza 2 più 1 pf), e la botte arriva a terra come se il
telo non ci fosse.

**Che cosa fanno i rostri.** Sono lame di spada piantate nel fondo della
botte, con le punte in giù. Tre cose:

- **Tagliano invece di tirare.** Una botte senza rostri sfonderebbe il telo
  lo stesso, ma lo trascinerebbe giù con sé, e tirerebbe i pali: la tenda
  crollerebbe più spesso. Con i rostri lo squarcio è pulito, largo un metro e
  mezzo, e il telo attorno resta su.
- **Tengono la botte dritta e la piantano.** Con i sassi sul fondo la botte
  cade sulle punte come una freccia, e le punte entrano nella terra battuta:
  non rotola e non rimbalza.
- **Feriscono chi è sotto** `[CANONE — DM 2026-10-26, B16]`. L'SRD ha la fossa con gli spuntoni, dove chi cade
  finisce su 1d4 punte. Qui è rovesciato: le punte cadono su chi sta sotto.
  Chi prende il colpo diretto prende anche **1d4 lame da 1d8**, nello stesso
  colpo, quindi contano per i 50 danni del danno massiccio.

**Lacera tutto, lacera in parte, rotola al bordo?** Le tre possibilità che il
DM ha chiesto di pesare, con i numeri:

| Dove tocca il telo | Che cosa succede alla botte | Al tavolo |
|---|---|---|
| sulla falda, fra il colmo e il bordo | taglia e passa: la falda scende di 50° circa, ma a 30 m/s la botte non scivola, e le punte mordono prima che la pelle ceda | arriva a terra nella casella tirata: il caso normale |
| sulla riga 12: un palo in cima (K12, N12, Q12) o la trave del colmo | prende il legno, a 6 m da terra | il danno della caduta va al legno (qui sotto): se lo spezza, la tenda crolla subito; se no la botte gli si apre sopra, e olio e fiale cadono da lì. Sotto nessuno prende il colpo diretto; il fuoco e l'olio sono gli stessi |
| sul bordo del telo, l'anello esterno di M7-C | taglia il telo dove scende verso terra, a un metro e mezzo d'altezza `[CANONE — DM 2026-10-29]` | arriva a terra contro la parete: metà dell'olio resta dentro, metà esce, e fuori arriva fino a 3 m |
| un barilotto, sulla falda | senza rostri e senza sassi cade storto, di piatto o di spigolo `[CANONE — DM 2026-10-26, B20]` | d6: con 1-2 rimbalza sulla falda, scivola giù e si apre fuori, nella casella oltre il bordo, dalla parte della falda (nord se è sopra la riga 12, sud se è sotto). Con 3-6 sfonda e cade dentro |

**I pali e la trave reggono la botte?** Prima quanto devono reggere. Il telo
copre 16,5 × 10,5 m: con le due falde sono circa 230 m² di pelle, a 2 kg al
metro quadro 450 kg. La trave del colmo, quercia di 15 × 20 cm lunga 16,5 m,
pesa 300 kg. Metà del telo tira sui picchetti del bordo, e sui tre pali vanno
circa 180 kg ciascuno. Un palo di legno alto 6 m regge quel peso cinque volte,
con il vento e il telo bagnato, se ha almeno 10-12 cm di diametro; il padiglione
di un capo ha pali da **15 cm**, e la trave ha lo stesso spessore `[CANONE — DM 2026-10-29]`.
Nell'SRD il legno ha durezza 5 e 10 pf ogni 2,5 cm di spessore: palo e trave
hanno **60 pf**.

La botte che cade sul palo o sulla trave fa al legno il danno della sua caduta
fino a 6 m da terra, più le lame dei rostri (B16). Se, tolta la durezza, arriva
a 60, il legno si spezza.

| Quota di sgancio | Danno al legno | Il palo o la trave si spezza |
|---|---|---|
| 48 m | 13d6 + 1d4 × 1d8 | **19%**, una volta su cinque |
| 42 m | 11d6 + 1d4 × 1d8 | 4% |
| 36 m e sotto | 9d6 + lame, o meno | mai |
| un barilotto, da qualunque quota | 3d6 al massimo | mai: si apre sul legno |

**La fisica, su questo, non è d'accordo del tutto, e va detto** (B22). In punta
il palo lavora di compressione, e la botte ci si infilza sopra: SRD e fisica
dicono la stessa cosa, il palo regge quasi sempre. Una trave presa in mezzo,
fra due pali, invece si piega: assorbe un paio di kJ prima di rompersi, e la
botte ne porta 40. Per la fisica la trave presa fra due pali si spezza sempre.

**Le palle di fuoco scoppiano sotto il telo.** Le fiale si rompono quando la
botte tocca terra, o la trave, e tutte e due stanno sotto il telo. L'olio e il
fuoco nascono dentro la tenda, mai sopra; solo al bordo metà resta fuori. Se una
fiala si rompesse sul telo, la palla di fuoco nascerebbe sul tetto: la tenda fa
da forno lo stesso, e chi è dentro è comunque nell'area.

La runa della barriera di lame è incisa sul palo centrale, N12. Se il palo si
spezza, la runa si spezza con lui **senza scattare**: scatta solo quando la
attiva Balvar `[CANONE — DM 2026-10-29, B7]`.

## 4. La botte e le fiale toccano terra

Nell'SRD un oggetto che cade prende anche lui il danno della caduta, 1d6 ogni
3 m, e la durezza lo riduce. La botte e le fiale cadono da 48 m: **15d6**, in
media 52.

| Che cosa | Durezza e pf (SRD) | Che fine fa |
|---|---|---|
| La botte, doghe di quercia e cerchi di ferro | durezza 5, 10 pf, come una porta di legno semplice `[CANONE — DM 2026-10-29]` | si apre sempre: anche il minimo, 15, passa la durezza e i punti ferita |
| Le fiale della fenice, legate alle doghe | vetro: durezza 1, 1 pf | si rompono sempre, nella casella dell'impatto, e scoppiano insieme |
| I barilotti | durezza 5, 5 pf `[CANONE — DM 2026-10-29]` | si aprono sempre |

I sassi tengono il fondo in basso, quindi la botte cade dritta, sui rostri, e
i rostri la piantano nel terreno: non rotola. Che il barile non scoppi o che
una fiala resti intera non succede con le regole dell'SRD: la versione di
prima, con il d20 per la tenuta, è tolta.

## 5. I danni

### Il colpo diretto: l'oggetto in caduta

Chi sta nella casella dove cade la botte prende il danno di un **oggetto in
caduta** (SRD 3.5, «Falling Objects»): un oggetto da 200 libbre in su fa 1d6
ogni 200 libbre, più 1d6 per ogni 3 m di caduta oltre i primi, fino a 20d6. Da
48 m sono **15d6**, in media 52. L'SRD non dà un TS e non chiede un tiro per
colpire: lo prende chi sta sotto. La riduzione del danno conta (Zog'tar ha RD
3/—). Il telo toglie 3 danni, e i rostri aggiungono 1d4 lame da 1d8 nello
stesso colpo (§3, variazione B16). Da 48 m, quindi, chi è sotto prende 15d6 − 3
+ 1d4 × 1d8, in media 60. Da un'altra quota, i dadi del §2-bis.

Una creatura sola prende il colpo diretto, quella della casella. Per Zog'tar,
che è Grande, basta una delle sue quattro caselle.

> **Il peso sta sul filo.** Botte di quercia da 59 litri con i cerchi di ferro
> 14-16 kg, olio 45,5 kg, sassi 15-24 kg (al massimo i 9 litri che l'olio
> lascia liberi), rostri 4-6 kg, fiale e corde 2 kg: da **80 a 93 kg**. Dalle
> 200 libbre (91 kg) in su l'SRD dà 15d6; sotto, nella fascia da 101 a 200
> libbre, dà 1d6 ogni 6 m, cioè **7d6**. Con i sassi fino all'orlo la botte
> pesa 93 kg e vale la prima riga: 15d6. La fisica è d'accordo: 40 kJ uccidono
> un uomo, e 7d6 non ucciderebbero una guardia hobgoblin
> `[CANONE — DM 2026-10-29, B3: 15d6]`.

### Le palle di fuoco, e perché non si allargano

Ogni fiala rotta è una *palla di fuoco* da 6d6. L'SRD fa partire un'area da un
incrocio della griglia: l'origine è **un angolo della casella d'impatto**, a
scelta del DM o con 1d4. La palla è uno spargimento di **6 m di raggio, 4
quadretti**. Riflessi **CD 14** dimezza: è la CD dell'SRD per un oggetto con un
incantesimo di 3° livello, 10 + 3 + 1. Due fiale sono due palle di fuoco dallo
stesso angolo, con due TS, e i danni si sommano. Nessuno nella tenda ha
Eludere.

**Perché non si allarga.** Nel 3.5 la *palla di fuoco* ha un raggio fisso: se
trova un muro si ferma, se trova un angolo lo gira, ma non riempie il volume
che le manca. Era l'AD&D a farla allargare nei luoghi chiusi. Due palle di
fuoco nello stesso punto non fanno un'area più grande: fanno due volte il
danno nella stessa area.

**La tenda fa da forno** `[Variazione — la versione più terribile, B12]`. Il
telo è chiuso su quattro lati e alto da 3 a 6 m: le fiamme non hanno dove
andare, e riempiono tutto quello che c'è sotto prima di squarciarlo. **Chi è
sotto il telo è nell'area, dovunque sia**, anche oltre i 6 m. Dal palo
centrale cambia poco, perché la palla da 6 m copre già quasi tutto il
pavimento: aggiunge Balvar nel fondo buio e la guardia Q14, che l'SRD puro
lascia fuori con tre angoli d'origine su quattro. Fuori dal telo valgono i 6 m
dell'SRD: Grask, a P16, è dentro o fuori secondo l'angolo.

### L'olio: quanto ne cade e dove arriva

L'SRD dà due regole per l'olio, e qui servono tutte e due.

- **La pinta versata.** Mezzo litro d'olio (una pinta) copre un quadretto, se
  il terreno è liscio; acceso, brucia **2 round** e fa **1d3 da fuoco** a round
  a chi ci sta.
- **L'ampolla lanciata.** Un'ampolla d'olio è un'arma a spargimento, con le
  regole del fuoco dell'alchimista: chi è colpito in pieno prende **1d6**, e
  **1d6 ancora il round dopo**; chi è vicino prende lo **spruzzo, 1 danno**.

La botte ha 50 litri, cioè **105 pinte**. Una botte che si apre a 110 all'ora
schizza l'olio tutto attorno, e il conto delle pinte dice fin dove arriva
`[Variazione sull'SRD, B6]`:

| Zona | All'aperto | Dentro la tenda | Olio | Brucia |
|---|---|---|---|---|
| **Cuore** | la casella d'impatto e le otto attorno, 3 × 3 | lo stesso | 5 pinte a quadretto, 45 in tutto | 10 round |
| **Il resto** | fino a **7 m** dall'impatto: 60 quadretti | **tutto il pavimento**, J10–R14, e le pareti del telo inzuppate fino a 3 m: il telo ferma gli schizzi | 1 pinta a quadretto all'aperto, quasi 2 dentro | 2 round all'aperto, 3 dentro |

**Quanto va oltre la palla di fuoco.** All'aperto l'olio arriva a 7 m e la
palla di fuoco a 6: **un metro in più**, un anello sottile di un quadretto,
che prende fuoco nello stesso istante, perché il velo d'olio è tutto unito e
la fiammata lo corre in un attimo. Dentro la tenda la domanda non si pone: dal
palo centrale il telo è a 4,5 m a nord e a sud e a 7,5 m a est e a ovest,
quindi l'olio si ferma sul telo e copre ogni quadretto del pavimento. Se il
barile cade sul bordo del telo (le cadute da 4,5 m del §6), metà dell'olio va
fuori, in una striscia di un quadretto lungo il telo da quella parte.

La variazione è una sola: le pinte nello stesso quadretto si sommano, e ogni
pinta in più fa bruciare il quadretto 2 round in più, non più forte. Il resto
è l'SRD.

### L'olio acceso

- **Si accende subito**, tutto: la palla di fuoco accende i combustibili
  nell'area (SRD), e la fiammata corre il velo d'olio fino al bordo.
- **Chi sta nell'olio che brucia** prende **1d3 da fuoco** a round (SRD, la
  pinta) e tira **Riflessi CD 15** per non prendere fuoco (SRD, «Catching on
  Fire»: chi è esposto a olio in fiamme).
- **Chi era nel cuore è inzuppato**: prende il secondo 1d6 dell'ampolla e
  prende fuoco **senza TS** `[Variazione — la versione più terribile; per l'SRD
  tira anche lui Riflessi CD 15]`.
- **Chi brucia** prende **1d6 a round** finché non riesce Riflessi CD 15;
  rotolarsi a terra dà +4, ma non dentro l'olio, che riaccende. Una palla di
  fuoco da sola non accende i vestiti (SRD: gli effetti istantanei non lo
  fanno); l'olio sì.

### Il fumo e il crollo

- **Fumo**, da subito, sotto il telo: Tempra CD 15, +1 per ogni prova
  precedente, o il round si passa a tossire; due round di fila fanno 1d6 non
  letali. Il fumo dà occultamento (20%) a tutti quelli dentro (SRD, «Smoke
  Effects»).
- **Il telo brucia** dal primo round. Alla fine del round **1d4+1** crolla, se
  non è crollato prima per il colmo: chi è ancora sotto prende 2d6 da fuoco, è
  intralciato e tira Riflessi CD 15 per uscire, un tentativo per round, con 1d6
  da fuoco a ogni round sotto il telo che brucia `[Regola della casa, costruita
  sullo stato F di M7-C]`.
- **La luce**: la tenda che brucia illumina lo spiazzo come un falò grande. Il
  fondo buio di M7-C non c'è più.

### Il danno massiccio

Nel 3.5 chi prende **50 danni o più da un solo attacco** e non è già morto tira
**Tempra CD 15**: se fallisce, muore, quali che siano i suoi punti ferita. Un 1
naturale fallisce sempre, quindi anche Zog'tar, con Tempra +18, ha il 5%.

- Il **colpo diretto** da 15d6 arriva a 50 due volte su tre.
- **Le due palle di fuoco contano come un attacco solo**: si sommano, e la
  somma è quella che conta per i 50 `[Variazione, la versione più terribile —
  B5: per l'SRD ogni palla di fuoco è un attacco a sé, e 6d6 non
  arrivano mai a 50]`. Con due fiale e il TS fallito, la somma
  arriva a 50 una volta su dieci.
- Il colpo diretto, il fuoco e l'olio restano attacchi diversi.

### Le cose

| Che cosa | Che fine fa |
|---|---|
| La mappa di Hammerfist con le croci rosse, sulla tavola a J10 | brucia nel primo round se J10 è nella palla di fuoco; chi la vuole la prende prima |
| La lastra d'ardesia di Balvar | non brucia. La ha in mano, e la porta fuori con sé |
| Il corno di ferro nero, nella custodia al polso di Grask | non brucia. La custodia è di cuoio e ferro, e il glifo resta |
| Le armature delle guardie | niente: l'SRD fa danneggiare gli oggetti indossati solo con un 1 naturale al TS |

## 6. Il palo centrale, caduta per caduta

I PG non hanno mirato: stavano più o meno sopra il palo centrale, N12, e hanno
lasciato andare il barile. La deviazione del §2 dice quanto erano spostati
dalla verticale. Una volta su quattro erano proprio sopra il palo; le altre
volte il barile cade da 1,5 a 4,5 m più in là, nella direzione del d8, e in
diagonale un po' di più, fino a 6,4 m.

Le 25 cadute possibili, con quello che prende il barile, chi sta nel cuore
dell'olio (colpito in pieno, prende fuoco) e chi resta fuori dalle palle di
fuoco con la tenda che fa da forno. Chi non è nominato nelle ultime due colonne
è nell'area: prende le palle di fuoco e l'olio del pavimento.

<!-- pagina: una-colonna -->

| d8 · metri | Casella | Probabilità | Che cosa prende | Nel cuore dell'olio | Fuori dalle palle di fuoco |
|---|---|---:|---|---|---|
| nessuna deviazione | N12 | 25% | il palo centrale, in cima: lo spezza il 19%, e la tenda crolla; se no la botte gli si apre sopra | Zog'tar, Guardia M13, Guardia N13 | nessuno · secondo l'angolo: Grask |
| 1 nord · 1,5 m | N11 | 3,1% | il pavimento | nessuno | Grask |
| 2 nord-est · 2,1 m | O11 | 3,1% | il pavimento | nessuno | Grask |
| 3 est · 1,5 m | O12 | 3,1% | la trave del colmo: la spezza il 19%, e la tenda crolla; se no la botte le si apre sopra, e sotto niente colpo diretto | Zog'tar, Guardia N13 | nessuno · secondo l'angolo: Grask |
| 4 sud-est · 2,1 m | O13 | 3,1% | **Zog'tar**, 15d6 − 3 + 1d4 × 1d8 | Zog'tar, Guardia N13, Sacerdote | nessuno |
| 5 sud · 1,5 m | N13 | 3,1% | **Guardia N13**, 15d6 − 3 + 1d4 × 1d8 | Zog'tar, Guardia M13, Guardia N13, Guardia M14, Sacerdote | nessuno · secondo l'angolo: Grask |
| 6 sud-ovest · 2,1 m | M13 | 3,1% | **Guardia M13**, 15d6 − 3 + 1d4 × 1d8 | Guardia M13, Guardia N13, Guardia M14, Sacerdote | nessuno · secondo l'angolo: Grask |
| 7 ovest · 1,5 m | M12 | 3,1% | la trave del colmo: la spezza il 19%, e la tenda crolla; se no la botte le si apre sopra, e sotto niente colpo diretto | Guardia M13, Guardia N13 | Grask |
| 8 nord-ovest · 2,1 m | M11 | 3,1% | il pavimento | nessuno | Grask |
| 1 nord · 3,0 m | N10 | 3,1% | il pavimento | nessuno | Grask |
| 2 nord-est · 4,2 m | P10 | 3,1% | il pavimento | nessuno | Grask |
| 3 est · 3,0 m | P12 | 3,1% | la trave del colmo: la spezza il 19%, e la tenda crolla; se no la botte le si apre sopra, e sotto niente colpo diretto | Zog'tar | nessuno · secondo l'angolo: Grask |
| 4 sud-est · 4,2 m | P14 | 3,1% | **Zog'tar**, 15d6 − 3 + 1d4 × 1d8 | Zog'tar, Guardia Q14 | nessuno |
| 5 sud · 3,0 m | N14 | 3,1% | **Sacerdote**, 15d6 − 3 + 1d4 × 1d8 | Zog'tar, Guardia M13, Guardia N13, Guardia M14, Sacerdote | nessuno |
| 6 sud-ovest · 4,2 m | L14 | 3,1% | il pavimento | Guardia M13, Guardia M14 | nessuno · secondo l'angolo: Grask |
| 7 ovest · 3,0 m | L12 | 3,1% | la trave del colmo: la spezza il 19%, e la tenda crolla; se no la botte le si apre sopra, e sotto niente colpo diretto | Guardia M13 | Grask |
| 8 nord-ovest · 4,2 m | L10 | 3,1% | il pavimento | nessuno | Grask |
| 1 nord · 4,5 m | N9 | 3,1% | il telo, sul bordo: metà olio fuori | nessuno | Grask |
| 2 nord-est · 6,4 m | Q9 | 3,1% | il telo, sul bordo: metà olio fuori | nessuno | Grask |
| 3 est · 4,5 m | Q12 | 3,1% | il palo est, in cima: lo spezza il 19%, e la tenda crolla; se no la botte gli si apre sopra | Zog'tar | nessuno · secondo l'angolo: Grask |
| 4 sud-est · 6,4 m | Q15 | 3,1% | il telo, sul bordo: metà olio fuori | Zog'tar, Guardia Q14, Balvar, Grask | nessuno |
| 5 sud · 4,5 m | N15 | 3,1% | il telo, sul bordo: metà olio fuori | Zog'tar, Guardia M14, Sacerdote | nessuno |
| 6 sud-ovest · 6,4 m | K15 | 3,1% | il telo, sul bordo: metà olio fuori | nessuno | Grask |
| 7 ovest · 4,5 m | K12 | 3,1% | il palo ovest, in cima: lo spezza il 19%, e la tenda crolla; se no la botte gli si apre sopra | nessuno | Grask |
| 8 nord-ovest · 6,4 m | K9 | 3,1% | il telo, sul bordo: metà olio fuori | nessuno | Grask |

<!-- /pagina -->

**Come si legge al tavolo.** Si tirano il d4 e il d8, si trova la riga, e la
riga dice tutto: chi prende i 15d6, se la tenda crolla subito, chi è
inzuppato. Poi si tirano i TS della scheda per tutti gli altri.

**Che cosa dice la tabella.** Il caso più probabile, una volta su quattro, è
la botte che si schianta in cima al palo centrale. Una volta su cinque lo
spezza, e il colmo viene giù con il telo in fiamme; le altre volte gli si apre
sopra, e l'olio e le fiale cadono da 6 m sullo stesso punto. Nessuno prende il
colpo diretto, perché sotto il palo non c'è nessuno. Zog'tar lo prende solo con
due righe su 25 (O13 e P14), una volta su sedici.

## 7. Che cosa succede, in numeri

Venti mila prove con le regole della scheda, la disposizione A, il barile
lasciato cadere sopra il palo centrale e due fiale. Il conto va fino alla fine
del primo round: lo scoppio, l'olio che brucia una volta, chi prende fuoco, il
telo che crolla addosso se il palo o il colmo si sono spezzati.

| Chi | pf pieni | pf alla fine del round 1 (mediana) | in fiamme | a 0 pf o meno | morto |
|---|---:|---:|---:|---:|---:|
| Zog'tar | 283 | 249 | 65% | 0% | 0% |
| Guardia M13, N13 (ciascuna) | 60 | 20 | 71% | 6-7% | 4% |
| Guardia Q14, M14 (ciascuna) | 60 | 22-23 | 60% | 1% | 1% |
| Il sacerdote, che dorme | 38 | −5 | 66% | 71% | 34% |
| Balvar | 101 | 72 | 33% | 0% | 0% |
| Grask, fuori a P16 | 6 | 6 | 0% | 30% | 30% |

- La tenda crolla subito l'**8%** delle volte, quando la botte spezza il palo o la trave (§3). Le altre volte crolla alla fine del round 1d4+1.
- Il sacerdote dorme: è indifeso, la sua Destrezza conta 0 (SRD), e i suoi
  Riflessi scendono da +4 a −1 `[CANONE — DM 2026-10-29: Destrezza 14 nella scheda, quindi
  da +4 a −1]`. Per questo è il primo a cadere.
- Con **una fiala** il sacerdote muore il 3% delle volte e le guardie
  restano a metà; con **tre fiale** il sacerdote muore nove volte su dieci e
  ogni guardia una volta su quattro.
- **Con la lettura SRD pura** (le palle di fuoco sono attacchi separati,
  l'inzuppato tira il TS, la palla resta di 6 m anche sotto il telo) il
  sacerdote muore il 28% delle volte, Balvar resta quasi intatto e Zog'tar
  brucia una volta su quattro invece di due su tre.
- **Se fossero stati sopra il seggio** invece che sopra il palo, Grask
  sarebbe morto l'83% delle volte e Zog'tar avrebbe preso i 15d6 una volta su
  tre<!-- apparato -->: i numeri sono in `ESITI-SIMULAZIONE.md`<!-- /apparato -->.

**Che cosa vuol dire.** Il barile **non uccide Zog'tar**: 283 punti ferita, RD
3 e Riflessi +9 reggono anche il colpo in pieno. Gli toglie un quinto dei punti
ferita prima ancora di cominciare, gli brucia la tenda, la mappa dell'assalto
e la scena di Balvar, e una volta su tre gli toglie il sacerdote. Lascia vivo Grask
due volte su tre, e Grask suona il corno: per questo i barilotti contano (§9).
Con 50 litri d'olio in una tenda di 100 metri quadri un giocatore si aspetta
una strage, e per Zog'tar questa non è una strage: va detto al tavolo prima di
tirare.

## 8. Chi vede che cosa, e le tattiche round per round

### Che cosa vedono e possono fare i PG da 48 m

| Che cosa | Regola | Al tavolo |
|---|---|---|
| **Vedere giù** | La scurovisione dei nani arriva a 18 m: a 48 m non serve. Si vede solo quello che è illuminato. Osservare ha −1 ogni 3 m di distanza (SRD), qui −15 | Si vedono i fuochi, i bracieri, e dal round 1 la tenda che brucia, che illumina lo spiazzo come un falò grande. Contare le sagome è facile; dire chi è chi chiede **Osservare CD 25** (10 + 15). Grask si riconosce perché sta dove sta |
| **Restare invisibili** | Lasciar cadere un barile o un barilotto non è un attacco. Lanciare un incantesimo che colpisce un nemico, o tirare con l'arco, rompe l'invisibilità (SRD) | Anche visibili, a 48 m nel buio nessuno li vede: sono fuori dalla luce del fuoco e oltre la scurovisione. Rompere l'invisibilità quassù costa poco, finché nessuno illumina il cielo |
| **Farsi sentire** | Ascoltare: −1 ogni 3 m (SRD), −15. *Volare* non fa rumore. Parlare a voce normale è CD 0, quindi 15 | **Non parlate.** Zog'tar ha Ascoltare +11: sente voci dall'alto una volta su tre, e da quel momento sa dove guardare. Le componenti verbali degli incantesimi si sentono allo stesso modo |
| **Colpire da quassù** | Gittata media: 30 m + 3 m per livello, al 13° 69 m. Gittata corta (7,5 m + 1,5 m ogni due livelli, 16,5 m al 13°) non arriva. Arco lungo: 48 m sono due incrementi, −2 | Incantesimi a gittata media e lunga sì, a contatto e corta no. Le frecce arrivano, ma chi le prende capisce che vengono dall'alto |
| **Il tempo** | Pozione di *volare* dell'incantatore di 5°: 5 minuti, 50 round. Pozione di *invisibilità* del 3°: 3 minuti, 30 round | L'invisibilità finisce prima del volo. Il viaggio di ritorno è quello della Scena 6. Se il corno suona, il drago arriva al round 70: chi è ancora in aria lì sopra non c'è più, perché il volo è finito da un pezzo |

### Chi può trovarli

| Chi | Che cosa ha | Che cosa può fare contro chi sta a 48 m |
|---|---|---|
| Guardie, orchi, lance della Guardia | scurovisione 18 m, Osservare e Ascoltare +1/+2 | niente. Notare un invisibile che si muove si fa solo entro 9 m (SRD, *invisibilità*, Osservare CD 20) |
| **Zog'tar** | scurovisione 18 m, Ascoltare +11, Int 16, tre giavellotti Grandi (incremento 9 m, al massimo cinque incrementi: 45 m) | capisce subito che il barile è venuto dall'alto. Non vede niente, ma sa dove guardare e non sta mai fermo nella luce |
| **Il sacerdote** (adepto 7) | *vedere invisibilità*, *luce*, *comando* (gittata corta, 12 m) | *vedere invisibilità* fa vedere gli invisibili, ma non fa luce: a 48 m nel buio non vede nessuno. Con *luce* su un giavellotto che Zog'tar scaglia verso l'alto illumina per un istante 6 m attorno al punto più alto del tiro, a 45 m: se un PG è lì vicino, lo vede (sotto) |
| **Balvar** (chierico 13) | *Leggere il Fuori-Posto* (18 m), *epurare invisibilità* (19,5 m), *dissolvi magie* (gittata media, 69 m, area di 6 m di raggio) | le prime due non arrivano a 48 m. *Dissolvi magie* ad area sì: può lanciarlo alla cieca sopra la tenda, o sul punto che il giavellotto ha illuminato (sotto, e B13) |
| Gli sciamani dei clan (15 adepti di 5°) | *vedere invisibilità*, *luce* | arrivano solo dopo il corno; stessi limiti del sacerdote |
| **Skullcrusher** | scurovisione 36 m, percezione cieca 18 m, *vedere invisibilità*, Osservare +29, vola | l'unico che li trova davvero. Arriva 70 round dopo il primo suono del corno (Scena 6) |

**Il giavellotto con la luce** `[CANONE — DM 2026-10-29]`. Se il
sacerdote è sopravvissuto ed è sveglio, al round 3 ha già *vedere invisibilità* addosso e
lancia *luce* su un giavellotto di Zog'tar (azione standard tutti e due). Zog'tar
lo scaglia dritto in alto sopra la tenda: arriva a 45 m e illumina 6 m attorno
per un round. Se i PG sono ancora sulla verticale della tenda (entro 6 m dal
punto), il sacerdote li vede, e li indica. Se si sono spostati anche solo di
dieci metri, il giavellotto illumina il vuoto. È la ragione per cui, dopo lo
sgancio, conviene allontanarsi.

**Il dissolvi di Balvar** `[CANONE — DM 2026-10-29, B13]`. *Dissolvi
magie* ad area ha 6 m di raggio. Se il giavellotto ha mostrato i PG, Balvar lo
lancia lì al round 4. Se non li ha mostrati, può lanciarlo alla cieca sopra la
tenda, e prende chi è rimasto sulla verticale una volta su sei. Ogni PG nell'area
tira la prova del dissolvi contro ogni effetto: d20 + 10 contro **CD 16** per il
*volare* della pozione (11 + 5) e **CD 14** per l'invisibilità (11 + 3). Chi
perde il volo cade: 48 m, **15d6** (SRD, 1d6 ogni 3 m). Lo fa solo se è in
modalità «minacciato, o attaccato» della Scena 7, ed è il caso: il barile è un
attacco.

### Quando si tira l'iniziativa, e che cosa fanno le rune

**L'iniziativa si tira quando i PG decidono di sganciare**, prima di tirare i
dadi della caduta: per l'SRD il combattimento comincia quando una parte agisce
contro l'altra, e i PG sono gli unici che sanno che sta cominciando. Tirano tutti,
PG e PNG. Poi:

1. **Il round di sorpresa è solo dei PG.** Nessuno nel campo sa che sono lì.
   Ognuno ha un'azione standard o di movimento, e lasciar cadere qualcosa è
   un'azione gratuita: la botte e i due barilotti possono andare giù nello stesso
   round. La botte cade in 3 secondi, meno di mezzo round: **arriva nel turno di
   chi l'ha lasciata**, e il DM risolve subito la scheda, dal passo 2 al 5.
2. **Il round 1 comincia in ordine d'iniziativa.** Chi è nella tenda è colto alla
   sprovvista fino al suo primo turno: niente Destrezza alla CA, che quassù conta
   poco. I TS contro le palle di fuoco li tira con il suo bonus pieno: l'SRD toglie
   la Destrezza alla CA, non ai Riflessi.
3. **L'olio che brucia** (passo 6 della scheda) si tira alla fine di ogni round,
   per tutti insieme. È lì che chi brucia perde i punti ferita.

**Balvar non è colto alla sprovvista** `[CANONE — DM 2026-10-26, B18]`. Il suo *Leggere il Fuori-Posto* è acceso, un cono di 18 m verso la
soglia, e il palo centrale ci sta dentro. Le fiale della fenice sono magiche:
Balvar le sente arrivare un battito prima dell'urto. Non fa in tempo a fare
niente, il round di sorpresa resta dei PG, ma al round 1 non è colto alla
sprovvista, e sa che cosa è caduto prima di vederlo.

**Le rune non scattano con il barile.** Una per una, con la regola di ciascuna:

| La runa o il glifo | Scatta? | Perché, e la versione più forte |
|---|---|---|
| La soglia, *epurare invisibilità* | no | scatta quando un nano varca la soglia: la botte non è una creatura, e i PG sono a 48 m. Se dopo uno di loro scende sotto i 19,5 m sopra la soglia, scatta su di lui |
| Il palo centrale, *barriera di lame* | no | la attiva Balvar. Se il palo si spezza, la runa si spezza senza scattare (B7) |
| Su Balvar, *silenzio* | non da sola | la accende lui, a comando. Contro chi è a 48 m non serve: la tiene per dopo |
| Il glifo sul telo sopra il seggio, 5d8 sonori | no, per l'SRD | il glifo scatta solo per una creatura che lo varca o lo tocca. La versione più forte, scelta dal DM `[CANONE — DM 2026-10-26, B17]`: **scatta quando il telo che lo porta brucia o crolla**, alla fine del round 1 o al crollo. Scoppio sonoro di 5d8, Riflessi CD 18 dimezza, su chi sta entro 1,5 m dal punto del telo sopra il seggio: Zog'tar, se è ancora lì, e la guardia Q14 |
| La custodia del corno, al polso di Grask | no | cuoio e ferro: il fuoco non la apre, e il glifo scatta solo per chi la apre senza la parola |
| La gemella della Catena, sul corno | non scatta, ma **ascolta** | tutto quello che si grida vicino a Grask arriva a Skullcrusher sulle colline (Scena 6). Il boato, «A ME, CANI! IL CORNO!» e «Dall'alto. Hanno ali.»: all'alba il drago sa che i nani volano, e guarda in alto `[CANONE — DM 2026-10-26, B21]` |

### Le tattiche, round per round

Le righe valgono per i due casi del §6: la tenda crollata subito (8%) e la
tenda in piedi che brucia.

| Chi | Round 1 | Round 2-3 | Dal round 4 |
|---|---|---|---|
| **Zog'tar** (Iniz +9) | Ira Superiore, azione gratuita, e il grido *«A ME, CANI! IL CORNO!»*. Se la tenda è crollata è sotto il telo in fiamme: lo squarcia con l'ascia ed esce in un round (Riflessi CD 15, ha +9). Se è in piedi esce dal lato più corto, tagliando il telo. Prende fuoco quasi sempre: si getta a terra fuori dall'olio (+4) | Fuori, guarda in alto e non vede niente. Capisce: *«Dall'alto. Hanno ali.»* Esce dalla luce del fuoco e non ci rientra: non sta mai fermo dove un secondo barile lo troverebbe. Al round 3 scaglia il giavellotto con la *luce* del sacerdote, se il sacerdote è vivo. Se Grask è morto va al corpo e strappa la custodia: il glifo gli scoppia addosso, 5d8 sonori, Riflessi CD 18, e lui suona lo stesso (B8) | Raduna le guardie nel buio, lontano dalla tenda, e manda le lance a cercare per il campo chi ha portato il fuoco. Se un PG scende sotto i 45 m e si fa vedere, i giavellotti; se scende sotto i 3 m, la carica |
| **Le quattro guardie** (Iniz +1) | Chi brucia si getta a terra fuori dall'olio (+4). Chi non brucia trascina fuori il sacerdote, se è vivo, oppure spegne Zog'tar con il mantello | Spengono chi brucia con i mantelli (+4, un'azione standard ciascuno), poi si mettono attorno al generale, scudi alzati, nel buio | Come Zog'tar. Non tirano verso l'alto finché nessuno indica un bersaglio |
| **Il sacerdote** (se è vivo) | Si sveglia nel fuoco, indifeso fino al suo turno. Striscia fuori, quasi sempre in fiamme | Round 2 si spegne. Round 3 *vedere invisibilità* e *luce* sul giavellotto di Zog'tar | Cura chi brucia. Se vede un PG, lo indica a Balvar; *comando* arriva solo a 12 m |
| **Balvar** (se è vivo) | Esce dal telo est, quello a sinistra, e si spegne. Guarda la botte squarciata e i rostri: lavoro dei fabbri di Hammerfist, lo riconosce al primo sguardo | Va da Zog'tar: *«Nani. Dall'alto.»* E la parola che conta: *«Chiamate il drago.»* Se Grask è morto e la custodia è intera, dà a Zog'tar la parola che la apre senza glifo | Il barile è un attacco: Balvar è «minacciato, o attaccato» (Scena 7). Al round 4 *dissolvi magie* ad area dove il giavellotto ha mostrato i PG, o alla cieca sopra la tenda (B13) |
| **Grask**, il suonatore del corno | Se è vivo, sveglio o no, il boato lo sveglia: suona il corno entro **1d4 round**, come al primo grido di Zog'tar (Scena 6) | Suona finché qualcuno non gli dice di smettere. Sta dove sta: è lui il bersaglio più facile del campo | |
| **Le due guardie del turno dopo** | Si svegliano nella loro tenda, a X4–Y5 | Arrivano al round 2, armate, da Zog'tar | Con le altre |
| **Il campo** (M7-H) | Le sentinelle dei fuochi gridano. I clan degli orchi si svegliano tutti insieme | Le ronde d'orchi arrivano dalla via ovest in 1d4+2 round, le lance della Guardia della Mano dalle vie nord e sud in 2d4+2. Finché Zog'tar è in piedi non vanno addosso alla tenda: fanno quadrato nello spiazzo, a una decina di metri dal telo, e portano acqua e pelli bagnate | Gli sciamani, se il corno ha suonato, cercano con *vedere invisibilità* e *luce*; nessuno vede a 48 m. Il campo resta sveglio fino all'alba |
| **Skullcrusher** | | | Se il corno ha suonato, arriva **70 round** dopo il primo suono e caccia sopra il campo (Scena 6, «Se il corno suona di notte») |

### Chi suona il corno, se Grask muore

Il corno chiama il drago chiunque lo suoni: la Catena è incisa sul corno, non su
Grask. Il problema è la custodia, chiusa da un glifo e incatenata al polso del
ragazzo morto. In ordine, chi ci prova:

| Chi | Quando | Come |
|---|---|---|
| **Balvar**, se è vivo | round 2-3 | non apre la custodia: dà la parola a Zog'tar, o a una guardia, e il corno suona senza glifo **al round 3-4** |
| **Zog'tar**, se Balvar è morto o lontano | round 2-3 | va al corpo, spezza la catena e strappa la custodia: il glifo gli scoppia addosso, 5d8 sonori, Riflessi CD 18, e lui suona lo stesso **al round 3** (B8) |
| **La guardia più vicina**, se Zog'tar è a terra | appena Zog'tar lo ordina, anche da a terra | come Zog'tar, ma con 60 pf e Riflessi +4 il glifo la può uccidere: una guardia già bruciata muore una volta su tre `[CANONE — DM 2026-10-29]`. Se muore, il corno resta nella custodia aperta, e lo prende la seguente |
| **Il primo capolancia della Guardia della Mano** | quando arriva, round 4-10 (2d4+2) | se nella tenda nessuno è in piedi a dare ordini, il capolancia sa che il corno è il segnale dell'alba e del drago. Lo fa suonare `[CANONE — DM 2026-10-26, B19]` |
| **Nessuno** | | se sono morti Grask, Zog'tar e Balvar, e le guardie sono tutte a terra prima che arrivino le lance. È il caso «se rubano o rompono il corno» della Scena 6: il drago arriva a metà mattina, furioso |

Il drago arriva 70 round dopo il primo suono, chiunque abbia suonato.

### Se sopravvivono: che cosa fanno dopo la notte

| Chi | Che cosa fa fino all'alba | All'alba |
|---|---|---|
| **Zog'tar** | brucia di rabbia, ma non perde la testa: dorme al buio, fuori dalla luce, e ogni ora in un posto diverso. Fa spegnere i fuochi dello spiazzo e mette due guardie a guardare il cielo. Manda le lance a cercare per il campo, perché pensa a un traditore prima che a dei nani in volo | guida l'assalto (§10), con il segno delle ustioni addosso. Ai suoi dice che il fuoco era un segno: chi l'ha attraversato vince |
| **Balvar** | è stato attaccato: non tratta più da solo (§10). Incide di nuovo i glifi scattati, rifà la custodia, e ricorda la botte di Hammerfist | sta sulla collina col drago, come nel canone. Ha capito che i nani vengono dall'alto, e lo dice al drago attraverso la Catena |
| **Il sacerdote** | cura chi brucia fino a finire gli incantesimi. Prepara *vedere invisibilità* e *luce* per la notte dopo | sale sulla breccia con Zog'tar, se ci sono incantesimi da spendere |
| **Le guardie** | stanno attorno al generale, con gli scudi alzati, al buio. Chi ha visto morire i compagni nel fuoco odia i nani in un modo nuovo | combattono con Zog'tar sulla breccia |
| **Grask**, se è vivo | non lascia più il corno. Dorme in piedi | suona all'alba, e il drago arriva sull'assalto |

### L'orda: che cosa fa, che cosa vede, che cosa può fare

Il campo è un'orda di circa diecimila: la Guardia della Mano, che è
disciplinata, le bande d'orchi, che non lo sono, i goblin sui carri, i lupi fuori.
Una tenda che scoppia nel cuore del campo, di notte, senza un nemico in vista,
non è una cosa che l'orda abbia mai visto. Su M7-H, attorno allo spiazzo, ci
sono otto lance della Guardia (quattro tende da otto attorno a ogni fuoco) e
quattro bande d'orchi a ovest, una ventina ciascuna con il loro sciamano.

| Chi | Che cosa fa | Che cosa vede, e fin dove | Che cosa può fare a chi vola |
|---|---|---|---|
| **Le sentinelle** dei fuochi e dei falò | round 1 gridano, round 2 corrono alla tenda e tirano fuori chi possono | scurovisione 18 m, e tutto quello che i fuochi illuminano: la tenda in fiamme, nessun nemico | giavellotti, solo se vedono qualcuno |
| **La Guardia della Mano**, otto lance | escono armate al round 2, arrivano nello spiazzo in 2d4+2 round. Quattro lance fanno quadrato a 10 m dal telo, portano acqua e pelli bagnate e tengono indietro gli orchi; le altre chiudono le quattro vie battute e cercano tenda per tenda chi ha portato il fuoco | come le sentinelle. Ascoltare e Osservare +2 | giavellotti: incremento 9 m, al massimo 45 m, −2 a incremento |
| **Le bande d'orchi** | non capiscono, e si infuriano. Un fuoco dal cielo senza nemici: gli sciamani gridano che è l'occhio di Gruumsh, e le quattro bande corrono armate allo spiazzo con le torce, urlando al cielo. Arrivano in 1d4+2 round, come le ronde, senza ritardo: fanno muro attorno alla Guardia, e ogni torcia è un occhio in più che guarda in alto `[CANONE — DM 2026-10-29, B25]` | scurovisione 18 m, Ascoltare e Osservare +1. Le torce fanno luce fino a 12 m da terra | giavellotti alla cieca contro il cielo: chi è invisibile ha occultamento totale, 50% di mancare, e l'orco deve indovinare il quadretto (SRD) |
| **Le vedette goblin** sui carri | strillano, e non scendono | scurovisione 18 m | niente |
| **I lupi**, fuori dal campo | le sei squadre si stringono verso il campo e girano sotto le vie del ritorno: il viaggio a piedi della Scena 6 si tira a CD +2 `[CANONE — DM 2026-10-29, B25]` | fiuto a 9 m (18 col vento): chi vola sopra i 20 m ne resta fuori | i goblin in sella tirano giavellotti; i worg aspettano l'atterraggio |
| **Gli sciamani**, quindici adepti di 5° | dopo il corno: *vedere invisibilità*, e *luce* sulle punte dei giavellotti | vedono gli invisibili, ma solo dove vedono: 18 m di scurovisione, o la luce | *raggio rovente* (4d6, gittata corta: 10,5 m). La *ragnatela* arriva a 45 m ma in aria non ha dove attaccarsi, e non si forma (SRD) |

**Chi li vede, e chi li colpisce, quota per quota.** La tenda che brucia fa
luce come un falò grande: intensa entro 12 m, fioca fino a 24 m, finché non
crolla `[CANONE — DM 2026-10-29, B24]`. I numeri dei giavellotti
sono per un hobgoblin o un orco con +1 a distanza `[CANONE — DM 2026-10-29: statistiche del
combattente dell'SRD]`.

| Quota sopra la tenda | Visibili | Invisibili | Che cosa arriva |
|---|---|---|---|
| sopra i 45 m | nessuno li vede | nessuno li vede | niente: oltre la gittata dei giavellotti |
| da 45 a 25 m | nessuno, se non li illumina il giavellotto con la *luce* (§8) | nessuno | giavellotti a −4/−8 (−2 ogni 9 m): colpiscono solo col 20 naturale, 1d6+1 |
| da 24 a 19 m | **tutti**, nella luce dell'incendio | nessuno, finché non suona il corno; dopo, gli sciamani | giavellotti a −4: raffiche di 20-30, colpisce un giavellotto ogni venti `[CANONE — DM 2026-10-29: CA dei PG di 13° livello sopra il 20]` |
| 18 m e sotto | tutti, anche al buio | gli sciamani dopo il corno, e il sacerdote. *Comando* del sacerdote a 12 m | giavellotti a −2 o senza penalità; Zog'tar con i giavellotti Grandi |
| 10,5 m e sotto | | | il *raggio rovente* degli sciamani, 4d6 |

Il conto che conta: l'orda non può far male a chi resta in alto. Quello che
temere sono quattro cose sole, e tutte hanno un nome: il *dissolvi* di Balvar,
il giavellotto con la *luce* di Zog'tar, il corno, e il drago.

**Che cosa rischiano i PG.** Finché restano a 48 m, zitti, e si allontanano
dalla verticale della tenda dopo lo sgancio, niente: nessuno nel campo vede
così in alto al buio. Restano sopra la tenda a guardarla bruciare, e dal round
3-4 rischiano il giavellotto con la luce e il dissolvi di Balvar, cioè una
caduta da 48 m. Il resto è tempo: il volo dura 50 round, l'invisibilità 30, e
se il corno ha suonato il drago è lì al round 70.

**La mossa migliore, se la chiedono.** Nel round di sorpresa, insieme alla
botte, un barilotto su Grask. Ha 6 pf e Riflessi +1: una palla di fuoco lo
uccide anche se il TS gli riesce (3d6, in media 10). Grask sta nella luce del
falò della guardia, quindi il barilotto devia di 1d6−1 quadretti: lasciato
cadere sopra P16, la palla di fuoco lo prende due volte su tre. Tutti e due i
barilotti su di lui, nello stesso round: nove volte su dieci. Senza
Grask il corno resta nella custodia col glifo, e la notte resta senza drago.

## 9. I due barilotti da 10 litri

| | Il numero | Da dove |
|---|---|---|
| Peso | circa 14 kg, 31 libbre: 9 kg d'olio, 5 di doghe e cerchi | |
| Dove cade | 1d8 per la direzione, **1d6−1 quadretti** nella luce di un fuoco, 1d8−1 al buio: senza sassi rotola, e l'aria lo sposta | §2 |
| Colpo diretto | oggetto in caduta da 31 a 50 libbre: 1d6 ogni 12 m, da 48 m **3d6** | SRD |
| Tenuta | si apre sempre: 15d6 contro durezza 5 e 5 pf | §4 |
| Fiale | una per barilotto `[CANONE — DM 2026-10-29]`: una *palla di fuoco* da 6d6, 6 m di raggio, Riflessi CD 14 | §5 |
| Olio | 21 pinte: il cuore è la sola casella d'impatto (5 pinte, 10 round, colpito in pieno chi c'è), il resto i quadretti entro 3 m (16, una pinta l'uno, 2 round, lo spruzzo): l'olio va 3 m, la palla di fuoco 6 | §5, con la stessa variazione |

La palla di fuoco del barilotto è grande quanto quella della botte; l'olio
copre un quarto dell'area.

Dove fanno più male, in ordine:

1. **Su Grask, prima che suoni.** Ha 6 pf e Riflessi +1: una palla di fuoco lo
   uccide quasi sempre, e senza Grask il corno resta nella custodia col glifo.
   È l'unico modo di tenere lontano il drago senza scendere. Dal round 1 Grask
   è a P16, nella luce del falò: lasciato cadere sopra di lui, il barilotto lo
   prende due volte su tre; tutti e due, nove volte su dieci (§8).
2. **Su una via battuta quando arrivano i rinforzi.** Le ronde d'orchi
   arrivano in fila dalla via ovest: gli orchi hanno 5 pf, e una palla di
   fuoco ne ammazza una ronda intera. Le lance della Guardia (guerrieri di 4°,
   30 pf) passano bruciate ma vive.
3. **Su Zog'tar fuori dalla tenda.** Fa poco: 3d6 se lo prende in pieno, 6d6
   di fuoco, e lo trova già in Ira.
4. **Sulla tenda del turno dopo**, a X4–Y5, prima che le due guardie escano.

Un consiglio da dire al tavolo solo se lo chiedono: i barilotti valgono di più
**contro il corno** che contro Zog'tar.

## 10. Che cosa cambia per la storia

- **Balvar.** Se è vivo, è stato attaccato: non tratta più da solo. La
  Diplomazia CD 18 del nipote funziona solo con chi non l'ha minacciato, e
  bruciargli la tenda è una minaccia. Resta la lastra d'ardesia, che porta
  fuori dal fuoco: chi la guarda (Osservare CD 20, da vicino) legge il nome di
  Hald, e chi gli parla del ragazzo per primo lo trova ancora aperto, perché
  quella leva non dipende da come lo si è trattato (Scena 7, «Ricattabile»).
  Se è morto nel fuoco è il caso «ucciso senza ascoltarlo» della Scena 7: la
  lastra resta fra le ceneri della tenda, e qualcuno la trova in ARC-09. La
  Catena sul drago e la sua gemella sul corno restano: le rune incise
  sopravvivono al runaio `[CANONE — DM 2026-10-29]`.
- **Il corno e il drago.** Se Grask muore e nessuno apre la custodia, all'alba
  nessuno chiama il drago, ed è il caso «se rubano o rompono il corno» della
  Scena 6: arriva tardi, a metà mattina, furioso. Se il corno suona di notte,
  vale «se il corno suona di notte»: il duello all'alba si fa senza sorpresa,
  con il drago già in quota.
- **L'assalto dell'alba.** Le mura contano quello che arriva dalla notte
  (Scena 10), e il barile ci porta due righe del canone: il boato è un
  **allarme**, quindi un successo in meno, e Zog'tar quasi sempre è **vivo
  all'alba**, quindi un altro successo in meno, e guida l'assalto. Tutte e due
  valgono anche se la tenda è bruciata. Per bilanciarle propongo di leggere la
  tenda in fiamme come la riga «Zog'tar umiliato davanti alle guardie»: il
  generale tirato fuori dal fuoco davanti ai suoi annulla il successo in meno
  dell'allarme `[CANONE — DM 2026-10-29]`. Se il barile uccide il
  sacerdote, Zog'tar sale sulla breccia senza di lui, come il canone prevede
  già (EL 16, senza Balvar e senza il sacerdote).
- **Hammerfist vede.** Dalle mura le sentinelle vedono la tenda nera prendere
  fuoco a un chilometro, nel mezzo del campo. Re Thorek lo sa prima che i PG
  rientrino.
- **Il nemico impara.** Dopo questa notte Zog'tar sa che i nani volano. Per il
  resto dell'assedio dorme ogni notte in un posto diverso, al buio, e non sotto
  una tenda; i fuochi dello spiazzo si spengono; gli sciamani tengono pronti
  *vedere invisibilità* e *luce* sui giavellotti, e due di loro guardano il
  cielo `[CANONE — DM 2026-10-29]`. Un secondo barile non trova più
  niente di così facile.
- **I PE per la trovata**: §13.
- **Echo Ledger** (§7 di DEF-4): «la notte del barile», con chi è morto e se il
  corno ha suonato.

## 11. Le mappe

**Perché al tavolo la tenda sembrava enorme.** Il ramo di gruppo
`campaign-group-rumblingstone` e il booklet stampato il 12 ottobre hanno
ancora la vecchia M7-C: un salone da 18 × 16,5 m su un palo solo, con sette
croci di tendine attaccate. Su `main` la tenda è stata rifatta il 21 ottobre
(PR #261) come padiglione a tre pali, 13,5 × 7,5 m di pavimento, ed è quella
del booklet ristampato il 22. Questa PR fa un passo in più, e toglie lo
steccato che la #261 ci aveva messo attorno: orchi e hobgoblin dell'orda sono
un'orda nomade, non una legione.

Il modello è il campo di un capo nomade: l'ordo di un khan mongolo, con la
tenda del capo sola in mezzo e gli anelli di tende attorno; il khalasar di un
khal, senza mura, dove il capo dorme al centro e i suoi fedeli più vicini; il
campo di una banda gota o gallica, raccolta attorno al fuoco del capo e ai
pali dei trofei, con i carri del bottino lasciati dove si sono fermati.

- **M7-C** è lo **spiazzo del capo**: terra battuta senza recinto, larga una
  quarantina di metri, con la tenda sola nel mezzo. Davanti alla soglia il
  fuoco del consiglio, a notte fonda ridotto a brace (luce fioca solo entro 3
  m, così l'avvicinamento della Scena 6 non cambia), e i due pali dei trofei
  con lo stendardo della Mano Rossa; il bottino della valle ammucchiato
  davanti al capo. Sul bordo, staccate l'una dall'altra, le tende dei servi e
  del bottino, senza soldati, e la tenda del turno dopo a 9 m (X4–Y5). La
  tenda, le persone e tutte le coordinate delle scene **non cambiano**.
- **M7-H** è il **campo attorno**, 66 × 60 m. A 20-30 m dal telo le lance della
  Guardia della Mano: quattro tende da otto attorno al fuoco della lancia, a
  gruppi staccati, con 3 m fra il fuoco e i teli; a ovest i clan degli orchi,
  ripari storti attorno al fuoco della banda, con il vuoto fra un clan e
  l'altro; i lupi da guerra ai picchetti, i carri del bottino, il palo degli
  sciamani. Le vie sono solo terra battuta, a raggiera dallo spiazzo, e i
  rinforzi arrivano da lì. Nessuna tenda della Guardia è dentro i 6 m del
  barile.

Le misure vengono dalla ricerca sugli accampamenti, nelle parti sui campi
mongoli e d'avventura<!-- storico --> (`plans/esperimenti/mappe-campo-2026-10-21/RICERCA-ACCAMPAMENTI.md`)<!-- /storico -->. Le due mappe passano il collaudo senza
errori, con voto di qualità 100 tutte e due.

<!-- storico -->
## 12. Domande al DM

Ogni domanda ha la proposta ★, scelta come la versione più forte quando le
regole lasciano scegliere.

| # | Domanda | ★ Proposta | Le altre |
|---|---|---|---|
| B1 | Quante fiale della fenice ci sono sulla botte, e quante su ciascun barilotto? | **decisa dal DM il 2026-10-29:** due sulla botte, una per barilotto | una o tre sulla botte: §7 dà i numeri |
| B2 | Una fiala della fenice scoppia quando si rompe? Con che CD? | **decisa dal DM il 2026-10-29:** sì, Riflessi CD 14 | CD 15 se è una pozione del re fatta al 6°; o un innesco a miccia, con il 50% di accensione dell'olio dell'SRD |
| B3 | Il colpo diretto della botte: 15d6 o 7d6? | **decisa dal DM il 2026-10-29:** 15d6: con i sassi fino all'orlo pesa più di 200 libbre | 7d6 se la botte pesa meno |
| B4 | La deviazione senza tiro per colpire: 1d8 per la direzione, la distanza secondo peso e luce (botte nella luce 1d4−1, barilotto 1d6−1, un dado in più al buio) | **decisa dal DM il 2026-10-29:** sì | un quadretto ogni 10 piedi come l'arma a spargimento (fino a 15 quadretti: la tenda si manca quasi sempre); oppure nessuna deviazione |
| B5 | Le palle di fuoco che scoppiano insieme contano come un attacco solo per il danno massiccio? | **decisa dal DM il 2026-10-29:** sì | no, come nell'SRD: ogni fiala è un attacco |
| B6 | L'olio: cuore 3 × 3 colpito in pieno (10 round), il resto copre il pavimento della tenda (3 round) o arriva a 7 m all'aperto (2 round), tutto acceso insieme; l'inzuppato prende fuoco senza TS | **decisa dal DM il 2026-10-29:** sì | l'SRD puro: ogni quadretto brucia 2 round, l'olio fuori dalla palla di fuoco si accende al round dopo, e anche l'inzuppato tira Riflessi CD 15 |
| B7 | Il palo centrale spezzato fa scattare la barriera di lame? | **decisa dal DM il 2026-10-29:** no, la runa si spezza | sì, 13d6 lungo la riga 12, Riflessi CD 21 |
| B8 | Zog'tar sa la parola della custodia del corno? | **decisa dal DM il 2026-10-29:** no: la sanno Grask e Balvar | sì, e il corno suona al round 2 senza glifo |
| B9 | In che tacca è caduta la botte, e quindi Grask era sveglio? | **decisa dal DM il 2026-10-29:** quella del tavolo: lo stato di Grask si fissa all'arrivo dei PG (Scena 6) | |
| B10 | La Catena del drago sopravvive a Balvar morto? | **decisa dal DM il 2026-10-29:** sì | no: con Balvar morto la Catena si spezza, e il drago è libero e furioso |
| B11 | La tenda bruciata col generale dentro vale come «Zog'tar umiliato davanti alle guardie» sulle mura? | **decisa dal DM il 2026-10-29:** sì: annulla il successo in meno dell'allarme | no: restano i due successi in meno (allarme e Zog'tar vivo) |
| B12 | La tenda fa da forno: chi è sotto il telo è nell'area delle palle di fuoco, anche oltre i 6 m? | **decisa dal DM il 2026-10-29:** sì | no: 6 m dall'angolo, come nell'SRD; dal palo centrale restano fuori Balvar e la guardia Q14 con tre angoli su quattro |
| B13 | Balvar lancia *dissolvi magie* ad area nel cielo (dove il giavellotto con la luce ha mostrato i PG, o alla cieca sopra la tenda, una volta su sei)? | **decisa dal DM il 2026-10-29:** sì: chi perde il volo cade da 48 m, 15d6 | no: Balvar non attacca dei nani che non vede |
| B14 | La procedura delle trovate (§13) entra nello standard dei moduli, con la riga «se ci fanno l'ingegnere» nei master dei prossimi archi? | **decisa dal DM il 2026-10-29:** sì, da ARC-08 | solo questa volta |
| B15 | I PE per l'ingegno: tre fasce, GS = livello −4, −2, pari al livello; per il barile la fascia di mezzo, o quella alta se il corno non suona | **decisa dal DM il 2026-10-29:** sì | un premio fisso a sessione; o niente oltre ai nemici sconfitti |
| B16 | I rostri sono lame di spada: chi prende il colpo diretto prende anche 1d4 lame da 1d8, nello stesso colpo? | **decisa dal DM il 2026-10-26: sì** | no: i rostri servono solo a tagliare il telo, come prima |
| B17 | Il glifo sul telo sopra il seggio scatta quando il telo brucia o crolla? | **decisa dal DM il 2026-10-26: sì** | no, come l'SRD: si brucia senza scattare |
| B18 | Balvar, col Fuori-Posto acceso, sente arrivare le fiale e non è colto alla sprovvista al round 1? | **decisa dal DM il 2026-10-26: sì** | no: è sorpreso come gli altri |
| B19 | Se nella tenda non resta nessuno in piedi, il primo capolancia fa suonare il corno? | **decisa dal DM il 2026-10-26: sì** | no: aspetta l'alba senza ordini |
| B20 | Un barilotto senza rostri che cade sulla falda può rimbalzare fuori, 1-2 su d6? | **decisa dal DM il 2026-10-26: sì** | no: sfonda sempre, come la botte |
| B21 | Il drago sente attraverso la gemella del corno i gridi della notte, e all'alba guarda in alto? | **decisa dal DM il 2026-10-26: sì** | no: il sussurro porta solo i nomi |
| B22 | Pali e trave: il danno della caduta contro durezza 5 e 60 pf (SRD), che da 48 m li spezza una volta su cinque? | **decisa dal DM il 2026-10-29:** sì, come ha chiesto il DM: si conta con durezza e spessore | la fisica: il palo preso in punta regge, la trave presa fra due pali si spezza sempre. È la versione più distruttiva |
| B23 | Lo sgancio guidato: chi non vede, guidato da chi vede il colmo, usa la colonna «chi vede», con 1 quadretto in più se la guida non vede chi sgancia | **decisa dal DM il 2026-10-29:** sì | la guida a voce vale sempre «chi vede»; o non vale niente |
| B24 | La tenda che brucia fa luce come un falò grande: intensa entro 12 m, fioca fino a 24 m, finché non crolla e diventa brace | **decisa dal DM il 2026-10-29:** sì | la luce di un falò normale, 6 m e 12 m |
| B25 | Come reagiscono le bande d'orchi e i lupi al barile | **decisa dal DM il 2026-10-29: la furia.** Le quattro bande corrono armate allo spiazzo con le torce, senza ritardo; i lupi si stringono e il ritorno a piedi si tira a CD +2 | il caos (saccheggio, ronde in ritardo di 1d4 round); la disciplina; la caccia per tutta la notte (CD +4) |
<!-- /storico -->

## 13. Le trovate dei giocatori: come gestirle le prossime volte

Il barile non è stato un incidente: il tavolo ha guardato quello che aveva
(olio, botti, fabbri nanici, pozioni, volo e invisibilità) e ha costruito
un'arma che il modulo non prevedeva. Succederà ancora, ed è una cosa da
premiare, non da contenere. Perché il DM non debba improvvisare, serve una
procedura breve e sempre uguale `[Proposta — B14 e B15]`.

**La procedura, in cinque passi.**

1. **La regola più vicina dell'SRD.** Quasi tutto quello che i giocatori
   costruiscono è già nell'SRD sotto un altro nome: oggetto in caduta, arma a
   spargimento, olio e fuoco dell'alchimista, danni agli oggetti (durezza e
   pf), trappole, crolli, fumo, annegamento. Si parte da lì e si scrive la
   variazione, una sola, accanto.
2. **Un tiro per l'imprevisto, non di più.** Se la trovata non è un attacco,
   non c'è tiro per colpire. L'imprevisto si tira con un dado solo, come la
   deviazione di questo documento (1d8 per la direzione, un dado per la
   distanza), o con una prova di abilità del PG che l'ha costruita
   (Artigianato, Conoscenze (architettura e ingegneria), Disattivare
   Congegni) contro **CD 15 / 20 / 25** per una cosa semplice, ingegnosa o al
   limite.
3. **Il danno dalle tabelle.** Se la trovata fa danno, si prende la tabella
   SRD più vicina (oggetti in caduta, trappole) e si sta dentro il tetto
   delle trappole dell'SRD per il livello del gruppo: al 13° una trappola
   seria fa in media 50-70 danni e ha CD 20-25. Il barile di questa notte,
   15d6 + 12d6 di fuoco, sta proprio lì.
4. **Le reazioni, da una tabella fissa.** Ogni scena di un modulo dovrebbe
   avere tre righe pronte: chi è colpito e che cosa fa al suo primo turno, chi
   se ne accorge e in quanti round, e che cosa arriva (allarme, rinforzi,
   incantatori). È quello che il §8 fa per questa scena.
5. **La conseguenza e il premio.** Una riga di canone (che cosa cambia nel
   mondo) e i PE.

**I PE per l'ingegno.** Il 3.5 lascia al DM i premi fuori dagli scontri. La
proposta è dare per la trovata, oltre ai PE dei nemici che cadono davvero, i
PE di uno scontro immaginario, con il GS legato a quanto la trovata pesa:

| La trovata | GS dello scontro immaginario | Al 13°, PE da dividere fra i quattro |
|---|---|---|
| risolve una scena in un modo che il modulo non prevedeva | livello del gruppo −4 | 975, cioè 244 a testa |
| cambia l'arco: tocca il canone, toglie un pezzo al nemico | livello del gruppo −2 | 1.950, cioè 487 a testa |
| ribalta l'arco: salva un luogo, abbatte un boss prima del tempo | livello del gruppo | 3.900, cioè 975 a testa |

Per il barile, la proposta è la seconda riga: brucia la tenda del comando, la
mappa dell'assalto e quasi sempre il sacerdote, e tocca le mura all'alba. Se
uccide Grask e il corno non suona, sale alla terza. I PE si segnano a mano: il
registro PE dello script parte da zero, e senza un punto di partenza non va
usato.

**Lasciare che i PG stravolgano le cose.** Il modulo non deve difendere le sue
scene. Due cose aiutano. La prima: nei master dei prossimi archi, accanto alle
risorse che i PG trovano, una riga «se ci fanno l'ingegnere», con la regola SRD
più vicina già scritta (la botte d'olio, la diga, il ponte, il forno della
forgia). La seconda: i nemici intelligenti imparano. Dopo questa notte Zog'tar
sa che i nani volano, e il resto dell'assedio lo mostra (§10).

## Fonti

- SRD 3.5, «Falling Objects», «Catching on Fire», «Smoke Effects»:
  <https://www.d20srd.org/srd/environment.htm>
- SRD 3.5, olio (la pinta versata, l'ampolla lanciata, la miccia) e fuoco
  dell'alchimista: <https://www.d20srd.org/srd/equipment/goodsAndServices.htm>
- SRD 3.5, armi a spargimento e deviazione:
  <https://www.d20srd.org/srd/combat/specialAttacks.htm>
- SRD 3.5, danni agli oggetti, durezza e punti ferita:
  <https://www.d20srd.org/srd/combat/specialAttacks.htm>
- SRD 3.5, *invisibilità* («causing harm indirectly is not an attack»), *palla
  di fuoco*, aree e incroci della griglia, danno massiccio, CD degli oggetti
  magici: d20srd.org, voci omonime
- La fisica della caduta<!-- apparato --> (`simula_barile.py` nella cartella dell'esperimento)<!-- /apparato -->:
  densità dell'olio 0,91 kg/l, aria a 870 m 1,12 kg/m³, coefficiente di
  resistenza 0,9.
