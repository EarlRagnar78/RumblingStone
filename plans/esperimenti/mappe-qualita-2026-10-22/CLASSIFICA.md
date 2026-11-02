# La classifica delle mappe, 2026-10-22

La prima misura del corpus con lo standard di qualità
([standard-qualita-mappe.md](../../../skills/rumblingstone-mapmaking/references/standard-qualita-mappe.md),
[ADR-0098](../../adr/ADR-0098-la-qualita-delle-mappe-si-misura-con-uno-standard.md)).
In questo giro nessuna mappa è stata toccata; qui c'è che cosa rifare e in che
ordine.

```bash
python3 scripts/qualita_mappe.py --classifica
```

Il corpus del collaudo ha 50 griglie in 26 file. Le copie identiche (il master
d'arco e l'Atlante ARC-07) stanno su una riga: restano 44 griglie diverse.
Errori dello strumento: 0. Avvisi: 81, di cui 24 sono `contesto/quota-mancante`,
la regola nuova di oggi. Voto medio 88. Il voto somma i rilievi del collaudo
(per esempio `posa/nel-muro`, una porta che non sta in un muro), che pesano 12
punti l'uno: per questo le mappe in cima hanno pochi codici e voti bassi.

Le mappe di ARC-08 (`08_La Battaglia Di Hammerfist/Mappe/`) sono segnate a
parte, come chiesto: si valutano, non si modificano.

## La tabella, dalla peggiore

| # | Voto | Banda | Arco | Mappa | File | Rilievi principali |
|---:|---:|---|---|---|---|---|
| 1 | 43 | da rifare | **ARC-08** | MAPPA 3Z REVISED: L'Incrocio Silenzioso (imboscata) | `Hammerfist-L3-REVISED-Ultra-Clear.md` | `posa/nel-muro`×6, `struttura/senza-anelli`, `spazio/affollato`, `fazioni/a-contatto` |
| 2 | 52 | da rifare | ARC-07 | CAMPO DEI CRISTALLI VIVENTI — 30 m × 12 m (20 col × 8 righ | `ARC07-DEF-1-PIANO-TERRA-TERROS.md`; `ARC07-MAPPE-DEFINITIVO.md` | `simbolo/ignoto`×2, `posa/nel-muro`×2, `nord/mancante` |
| 3 | 62 | da rivedere | Drappo | Tarsilia — le stalle dell'Istrice (assalto notturno) | `tarsilia-stalle.md` | `posa/nel-muro`×3, `m4/esposizione` |
| 4 | 63 | da rivedere | Drappo | Tarsilia — la Ruota (pista del Drappo) | `tarsilia-la-ruota.md` | `posa/nel-muro`×2, `dimensioni/oltre-tavolo`, `contesto/quota-mancante`, `spazio/disperso` |
| 5 | 65 | da rivedere | Drappo | Tarsilia — versione giocatore | `tarsilia-la-ruota-giocatori.md` | `posa/nel-muro`×2, `dimensioni/oltre-tavolo`, `contesto/quota-mancante`, `m1/copertura` |
| 6 | 73 | da rivedere | ARC-09 | DESPERATE LAST STAND (Round 36-40) | `Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md` | `ingombro/grande`×4, `contesto/quota-mancante`, `taglia/non-dichiarata`, `m1/copertura` |
| 7 | 78 | da ritoccare | **ARC-08** | MAPPA 2B-CORRETTA REVISED: Attacco del Drago sui Bastioni | `Hammerfist-L2-REVISED-Ultra-Clear.md` | `coerenza/mura-sottili`, `contesto/quota-mancante`, `posa/nel-muro`, `m1/copertura` |
| 8 | 78 | da ritoccare | **ARC-08** | MAPPA 3Y REVISED: Il Ponte Sospeso (retroguardia) | `Hammerfist-L3-REVISED-Ultra-Clear.md` | `struttura/senza-anelli`, `fazioni/a-contatto`, `posa/nel-muro`, `m1/copertura` |
| 9 | 80 | da ritoccare | ARC-07 | MAPPA PF-4: FORGIA ADAMANTINA (Boss Elder Fire Elemental) | `Portale-Forgia-L2-REVISED-UltraClear.md` | `oggetti/fuoco-enorme`×4, `struttura/un-ingresso`, `struttura/senza-anelli`, `m1/copertura` |
| 10 | 81 | da ritoccare | **ARC-08** | MAPPA 5 REVISED: Il Cuore della Montagna (ultima resistenz | `Hammerfist-L3-REVISED-Ultra-Clear.md` | `dimensioni/oltre-tavolo`, `oggetti/porta-enorme`, `struttura/un-ingresso`, `struttura/senza-anelli` |
| 11 | 84 | da ritoccare | ARC-07 | IL CUORE DELLA MONTAGNA — caverna sacra 100 m × 80 m (33 c | `ARC07-DEF-5-RITORNO-HAMMERFIST.md`; `ARC07-MAPPE-DEFINITIVO.md` | `scala/tattica-non-a-1-5`, `struttura/un-ingresso`, `struttura/senza-anelli`, `fazioni/a-contatto` |
| 12 | 85 | da ritoccare | **ARC-08** | MAPPA 4 REVISED: Battaglia Finale Terrestre (carica in dis | `Hammerfist-L3-REVISED-Ultra-Clear.md` | `scala/tattica-non-a-1-5`, `dimensioni/oltre-tavolo`, `contesto/quota-mancante`, `fazioni/a-contatto` |
| 13 | 86 | da ritoccare | **ARC-08** | MAPPA 1A-3 REVISED: Campo della Mano Rossa (griglia strate | `Hammerfist-L1-REVISED-Ultra-Clear.md` | `scala/titolo`, `oggetti/tende-a-grappolo`, `contesto/quota-mancante`, `m1/copertura` |
| 14 | 87 | da ritoccare | **ARC-08** | MAPPA 1A-1 REVISED: Il Sentiero Nascosto (canyon completo) | `Hammerfist-L1-REVISED-Ultra-Clear.md` | `contesto/quota-mancante`, `spazio/disperso`, `fazioni/lontane`, `m1/copertura` |
| 15 | 88 | da ritoccare | ARC-07 | MAPPA PF-2: SALA DELLA FORGIA ETERNA (Hub Divino) | `Portale-Forgia-L1-REVISED-UltraClear.md` | `struttura/un-ingresso`, `struttura/senza-anelli`, `m1/copertura`, `m2/vuoto` |
| 16 | 89 | da ritoccare | ARC-07 | PF-3 CORRIDOIO DEL FUOCO (Fire Gauntlet) | `Portale-Forgia-L2-REVISED-UltraClear.md` | `lettura/affollata`, `struttura/senza-anelli`, `m1/copertura`, `m2/vuoto` |
| 17 | 91 | buona | ARC-07 | CAMERA CENTRALE — sfera Ø 60 m · ZERO-G ovunque TRANNE l'A | `ARC07-DEF-1-PIANO-TERRA-TERROS.md`; `ARC07-MAPPE-DEFINITIVO.md` | `struttura/senza-anelli`, `m1/copertura`, `m2/vuoto`, `m4/esposizione` |
| 18 | 91 | buona | **ARC-08** | MAPPA H3-1 REVISED: Cortile sfondato, ultima difesa ed eva | `Hammerfist-L3-REVISED-Ultra-Clear.md` | `oggetti/fuoco-enorme`, `contesto/quota-mancante`, `m1/copertura`, `m2/vuoto` |
| 19 | 92 | buona | **ARC-08** | MAPPA 2A REVISED: Fortezza Hammerfist top-down (scala pien | `Hammerfist-L2-REVISED-Ultra-Clear.md` | `oggetti/porta-enorme`×2, `coerenza/mura-sottili`, `contesto/quota-mancante` |
| 20 | 93 | buona | ARC-09 | CAMPO DROW 2 - FORWARD BASE (98m × 80m, Grid 65×53, Scala  | `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | `dimensioni/oltre-tavolo`, `contesto/quota-mancante`, `spazio/disperso` |
| 21 | 93 | buona | ARC-09 | CERCHIO SACRO DELLA FORESTA (60m Diameter Circle) | `Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO-maps.md` | `contesto/quota-mancante`, `m1/copertura`, `m2/vuoto`, `m4/esposizione` |
| 22 | 93 | buona | ARC-09 | Foresta in Fiamme — I Piromanti Drow (quest di Hella, P1B) | `Arco-Post-Hammerfist-P1B-Foresta-In-Fiamme-MAPPA.md` | `oggetti/fuoco-enorme`, `contesto/quota-mancante`, `taglia/non-dichiarata` |
| 23 | 93 | buona | **ARC-08** | MAPPA 1A-2 REVISED: Il Torrione di Vedetta (griglia densa) | `Hammerfist-L1-REVISED-Ultra-Clear.md` | `contesto/quota-mancante`, `m1/copertura`, `m2/vuoto`, `m4/esposizione` |
| 24 | 93 | buona | ARC-09 | ONDATA 2 POSITIONS (Round 22 Fase 2) | `Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md` | `contesto/quota-mancante`, `m1/copertura`, `m2/vuoto`, `m4/esposizione` |
| 25 | 95 | buona | ARC-07 | CORTILE INTERNO — 36 m × 27 m (24 col × 18 righe · 1,5 m)  | `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`; `ARC07-MAPPE-DEFINITIVO.md` | `contesto/quota-mancante`, `m2/vuoto`, `m4/esposizione` |
| 26 | 95 | buona | ARC-07 | M7-F — La fucina grande, livello −3 (notte, ≈372 DR) | `M7-F-fucina-grande-372.md` | `struttura/senza-anelli`, `m4/esposizione` |
| 27 | 95 | buona | ARC-07 | M7-F/1372 — La fucina grande, livello −3 (Giorno 3 dell'as | `M7-F-fucina-grande-1372.md` | `struttura/senza-anelli`, `m4/esposizione` |
| 28 | 96 | buona | **ARC-08** | MAPPA 1 REVISED: Disposizione Generale Giorno 1 (0-300 m) | `Hammerfist-L2-REVISED-Ultra-Clear.md` | `oggetti/tende-a-grappolo`, `contesto/quota-mancante` |
| 29 | 97 | buona | ARC-09 | CAMPO DROW 1 - BURNING OPERATIONS (80m × 60m = 53×40 grid, | `Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md` | `contesto/quota-mancante`, `m2/vuoto` |
| 30 | 97 | buona | ARC-09 | CAMPO DROW 1 - BURNING OPERATIONS BASE (80m × 60m, Grid 53 | `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | `contesto/quota-mancante`, `m2/vuoto` |
| 31 | 97 | buona | ARC-07 | M7-C — La tenda del comando di Zog'tar (notte, ≈372 DR) | `ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md` | `oggetti/fuoco-sotto-il-telo`, `contesto/quota-mancante` |
| 32 | 97 | buona | ARC-07 | M7-D — Il corridoio della fucina, livello −1 (notte, ≈372  | `M7-D-livello-1-372.md` | `struttura/senza-anelli` |
| 33 | 97 | buona | ARC-07 | M7-D/1372 — Il corridoio della fucina, livello −1 (Giorno  | `M7-D-livello-1-1372.md` | `struttura/senza-anelli` |
| 34 | 98 | buona | ARC-09 | Dauth, Carta C — Il chiostro-ospedale (Giorno 3) | `DAUTH-C1-chiostro-ospedale.md` | `lettura/affollata` |
| 35 | 98 | buona | ARC-07 | M7-E/1372 — I passaggi antichi, livello −2 (Giorno 3 dell' | `M7-E-gallerie-1372.md` | `struttura/fila-indiana` |
| 36 | 98 | buona | ARC-07 | MAPPA PF-1: STANZA DELLA CORONA (Boss Fight Belkram) | `Portale-Forgia-L1-REVISED-UltraClear.md` | `m4/esposizione` |
| 37 | 99 | buona | ARC-09 | Dauth, Carta A — La breccia della Porta Sud (Giorno 3) | `DAUTH-A-breccia-porta-sud.md` | `contesto/quota-mancante` |
| 38 | 99 | buona | ARC-09 | Dauth, Carta B — Il Razorfiend sui bastioni (Giorno 3) | `DAUTH-B-razorfiend-sui-bastioni.md` | `contesto/quota-mancante` |
| 39 | 99 | buona | ARC-09 | Dauth, Carta D — Le lance di Khorn sulle mura ovest (Giorn | `DAUTH-D-lance-di-khorn.md` | `contesto/quota-mancante` |
| 40 | 100 | buona | ARC-09 | Dauth, Carta C — Il cunicolo della cisterna, sotto il chio | `DAUTH-C2-cunicolo-cisterna.md` | — |
| 41 | 100 | buona | ARC-09 | Dauth, Carta E — La cellula nelle mura: corpo di guardia e | `DAUTH-E-cellula-nelle-mura.md` | — |
| 42 | 100 | buona | ARC-07 | FORESTA DI CRISTALLI GIGANTI — 27 m × 15 m (18 col × 10 ri | `ARC07-DEF-1-PIANO-TERRA-TERROS.md`; `ARC07-MAPPE-DEFINITIVO.md` | — |
| 43 | 100 | buona | ARC-07 | M7-E — Le gallerie di Zeth, livello −2 (notte, ≈372 DR) | `M7-E-gallerie-372.md` | — |
| 44 | 100 | buona | ARC-07 | STANZA DELLA CORONA — 15 m × 19,5 m (10 col × 13 righe · 1 | `ARC07-DEF-2-RITORNO-E-AFFRESCHI.md`; `ARC07-MAPPE-DEFINITIVO.md` | — |

## Le schede, dalla peggiore (fuori da ARC-08)

**2 · Campo dei Cristalli Viventi (52)**, ARC-07 DEF-1 e la sua copia
nell'Atlante. Due simboli che nessuna legenda spiega (💠 e 💚), il nord non
dichiarato, due porte ai bordi che non stanno in un muro, il 7,5% di copertura.
È una grotta di 30 × 12 m: si gioca, ma il giocatore non sa che cosa ha
davanti. **Per rifarla:** 💠 e 💚 nella legenda locale o sostituiti da simboli
universali; `@north`; le porte ai bordi tolte (un'apertura nella roccia è
pavimento) o chiuse fra due 🪨; qualche cristallo grande come copertura a metà.

**3 · Tarsilia, le stalle dell'Istrice (62)**, Drappo. Tre porte dei box
(H10, L10, P10) posate dove non c'è muro, e da quasi ogni cella si vede quasi
tutto (M4 0,64). **Per rifarla:** i box con le pareti di tavole, una porta per
box nella parete; un fienile o un carro che spezzi la vista fra le due metà.

**4-5 · Tarsilia, la Ruota e la sua versione giocatore (63, 65)**, Drappo. È la
pista del Palio: 64 × 46 quadretti, 2,1 Flip-Mat Enormous, 228 celle per
creatura, il 78% dello spazio aperto senza coperture. Una corsa vuole spazio
aperto, quindi M1 e M2 vanno derogati; il resto no. Due porte fuori dai muri
(BD14, J42) e nessuna quota. **Per rifarla:** una vista strategica della pista
intera (`@tipo strategica`) e due o tre carte tattiche a 1,5 m per le curve dove
si combatte; le porte in un muro; `@quota` e `@dislivello` della piazza.

**6 · Desperate Last Stand (73)**, ARC-09 P1C. Quattro creature Grandi che con
un ingombro di 2 × 2 non arrivano ai PG, e il treant in U18 senza `@taglia`. Lo
spazio è grande (40 × 40) e il cerchio non ha strozzature utili. **Per
rifarla:** `@taglia` sul treant; i varchi fra le pietre del cerchio larghi
almeno 2 quadretti dove passano i Grandi, o le creature Grandi spostate fuori;
la quota della radura.

**9 · PF-4 Forgia Adamantina (80)**, ARC-07. Quattro vasche di lava da 35-40
celle segnate come fuoco, un ingresso solo, nessun anello, nessuna copertura
fra l'ingresso e il boss. **Per rifarla:** la lava con il suo simbolo o
derogata con la ragione («vasche di colata, non fuochi»); una seconda via
(il canale di scolo, una passerella sopra le vasche) che faccia un anello
attorno a un'incudine o a un pilastro; due o tre coperture alte fra porta e
boss.

**11 · Il Cuore della Montagna (84)**, ARC-07 DEF-5 e Atlante. Una caverna di
100 × 80 m disegnata a 3 m per quadretto e collaudata come tattica: le
miniature non ci stanno. Un ingresso, nessun anello, nemici adiacenti ai PG al
via. **Per rifarla:** `@tipo strategica` per la caverna intera, più una carta
a 1,5 m del punto dello scontro; un secondo accesso (una fenditura, un pozzo
d'aria, che una caverna abitata deve avere comunque); le posizioni di partenza
separate o l'imboscata scritta.

**15 · PF-2 Sala della Forgia Eterna (88)**, ARC-07. Un ingresso, nessun anello,
da ogni cella si vede tutta la sala. È un hub divino senza nemici, quindi la
tattica conta poco. **Per rifarla:** solo se ci si combatte: una seconda porta e
un pilastro o un altare grande che faccia girare attorno.

**16 · PF-3 Corridoio del Fuoco (89)**, ARC-07. Il 57% del pavimento ha
un'icona e non si legge il terreno; nessun anello. **Per rifarla:** la metà
delle icone di pericolo sostituita da una zona (`@zone`) con la sua regola;
un passaggio laterale che faccia un anello.

Le altre mappe fuori da ARC-08 stanno sopra 90. Fra 91 e 94 i rilievi sono
quasi solo la quota mancante e le metriche di copertura non calibrate (M1, M2,
M4): Camera Centrale (gravità zero, senza coperture per costruzione), Foresta in
Fiamme (il treant in M07 senza `@taglia` e un incendio da derogare), Cerchio
Sacro, Ondata 2, Campo Drow 2 (2,5 Flip-Mat: da dividere o dichiarare
strategica). Le 15 mappe rifatte il 2026-10-21 stanno fra 93 e 100.

## ARC-08, da valutare e segnalare

Le mappe di `08_La Battaglia Di Hammerfist/Mappe/` stanno in tre file
(`Hammerfist-L1/L2/L3-REVISED-Ultra-Clear.md`). Nessuna è stata toccata.

**1 · 3Z L'Incrocio Silenzioso (43, da rifare).** La peggiore del corpus. Sei
porte posate fuori dai muri, 124 creature su 33 × 33 quadretti (3,3 celle per
creatura: non ci si muove), PG e nemici adiacenti, nessun anello. **Per
rifarla:** meno creature sulla griglia (il resto come truppe fuori campo),
almeno 6-8 celle libere per creatura; le porte nei muri; un anello attorno al
blocco centrale dell'incrocio, che è il senso di un'imboscata a un crocevia.

**7 · 2B Attacco del Drago sui Bastioni (78).** Tutte le mura spesse un
quadretto, mentre il testo dice mura di 12 m con camminamento; una porta fuori
dal muro; il 76% del bastione senza copertura. **Per rifarla:** la cortina a
2-3 quadretti con il camminamento disegnato, merli come copertura ½, le torri
sporgenti; la quota del camminamento (+12-15 m) e quella della fortezza.

**8 · 3Y Il Ponte Sospeso (78).** Nessun anello (è un ponte: va derogato),
nemici adiacenti al via, una porta fuori dal muro, da ogni cella si vede tutto.
**Per rifarla:** la deroga per l'anello; le partenze a distanza di carica; le
due teste del ponte con una copertura ciascuna; il dislivello sotto il ponte.

**10 · MAPPA 5 Il Cuore della Montagna (81).** 67 × 53 quadretti (2,6 Flip-Mat),
un portone di 6 quadretti (9 m), un ingresso, nessun anello, 182 creature.
**Per rifarla:** come il Cuore della Montagna di ARC-07: vista strategica e una
carta tattica dello scontro; il portone a 3 quadretti o derogato come porta
cerimoniale dei nani; un secondo accesso.

**12 · MAPPA 4 Battaglia Finale Terrestre (85).** Tattica a 3 m per quadretto,
3 Flip-Mat, 318 creature, il 93% dello spazio senza copertura, nemici a
contatto. È una battaglia d'eserciti scritta come scontro. **Per rifarla:**
`@tipo strategica` con le unità, e una carta tattica a 1,5 m per il punto dove
combattono i PG; la quota della piana e della porta, perché la «carica in
discesa» ha bisogno di un dislivello scritto.

**13 · 1A-3 Campo della Mano Rossa (86).** Il titolo dice «griglia
strategica», la mappa non lo dichiara; quattro ⛺ attaccate; 328 creature.
**Per rifarla:** `@tipo strategica`; le tende in file con le corsie e un
quadretto libero per i tiranti (ricerca accampamenti del 2026-10-21).

**14 · 1A-1 Il Sentiero Nascosto (87).** Un canyon di 20 × 100 quadretti con i
nemici a 70 m dai PG: quattro round prima del contatto, 222 celle per
creatura. **Per rifarla:** dividere il canyon in due carte, o spostare la
vedetta nemica entro 50 m dal punto d'ingresso dei PG.

**18-19 · H3-1 Cortile sfondato (91) e 2A Fortezza Hammerfist (92).** H3-1 ha
un incendio da derogare. La 2A è la pianta della fortezza (180 × 120 m,
`@tipo strategica`): due porte di 12 quadretti (18 m) e mura sottili al 98%.
Il testo dice «cancello 6 m»: la griglia è il doppio della scheda.

### Hammerfist non sta dove la vuole il DM

Il DM: Hammerfist è scavata nella collina o nella montagna, sopra la pianura
con gli accampamenti dell'orda, sia nel −1000 sia nel 1372.

- **ARC-08 la mette in piano.** La MAPPA 2A ha un «pendio fangoso +3 m» prima
  del fossato e scrive che «il resto è piana aperta»; il testo parla di
  «pendio 15%» su cinque righe (7,5 m di strada: poco più di 1 m di salita).
  Le baliste hanno 120 m di gittata nella scheda, il drago sorvola a 45 m
  «fuori gittata», il nemico arretra di notte «a 200 m». Con la fortezza in
  alto, 200 m dalle mura sono dentro il tiro dell'arco lungo (fino a circa
  366 m) e della balista antica (oltre 460 m), e il campo non ci starebbe.
- **ARC-07 la appoggia alla montagna.** L'Atlante (M7, D44) mette la montagna a
  nord, la fortezza appoggiata, il campo a sud e l'arrivo del portale a circa
  500 m dalle mura. Un vecchio file in archivio diceva 2 km. Le carte M7-D, E,
  F sono i livelli −1, −2, −3 scavati nella roccia, coerenti con il DM.
- **La regionale** mette gli Hammerfist Holds sulle colline ai piedi della
  North Wall, dove la neve resta tutto l'anno sopra i 3.000 piedi (circa
  900 m), a circa 55 miglia da Dauth.

**Proposta di numeri, da far scegliere al DM:** la porta a circa 950 m s.l.m.,
**+120-150 m sulla piana** dell'orda (come Mehrangarh, 122 m sopra Jodhpur);
una strada a tornanti con più porte in salita (Mehrangarh ne ha sette, il Krak
un corridoio voltato di 137 m); il campo dell'orda **fra 500 m e 1 km** dalle
mura, fuori dal tiro dall'alto, come già dice ARC-07; le mura spesse 2-3
quadretti, le torri ogni 20-30 m. Con un pendio del 15%, 120 m di salita
vogliono circa 800 m di strada: è la distanza che l'assalto deve fare sotto il
tiro, e cambia i round della MAPPA 4.

## Le mappe che non sono griglie

Lo strumento misura solo i master a emoji. Le altre si sono misurate a mano,
sulla barra di scala dell'immagine.

**La regionale della Cannath Vale** (`cannath-vale-gm-versia3ys4.webp`,
rifacimento di antariuk della Elsir Vale). Barra 0-80 miglia su 365 px. Rethmar
→ Cannathgate misura circa 85 miglia, la tabella dei viaggi ne dice 35;
Drellin's Ferry → Rethmar 98 contro 50. Il rilievo è solo il tratteggio di
colline e monti, senza quote. Nessun fiume unisce Cannathgate a Rethmar: vedi
[OPZIONI-FIUME.md](OPZIONI-FIUME.md). **Per rifarla:** una regionale nostra con
fasce di quota (la piana, le colline, la North Wall), la barra di scala
allineata alla tabella dei viaggi, e il corso d'acqua che il DM sceglie.

**Rethmar** (`rethmar-labels*.webp`, sempre antariuk, dalla Brindol di *Red
Hand of Doom*; si guarda, non si copia). Barra di 1.000 piedi su 385 px: la
cinta misura circa 1.100 × 520 m, una cinquantina di ettari. A 150 abitanti per
ettaro sono circa 7.000 persone, coerenti con una città piccola. Il fiume corre a nord, fuori dalle mura, con il ponte e il
mercato alla testa del ponte: è il modello di un municipium romano in piano.
Le torri della cinta sono poco più di una decina su circa 3,2 km, una ogni
200-300 m: ad Ávila e
a Roma ce n'è una ogni 30 m. Le strade principali sono larghe circa 10 m, più
delle vie romane (4,8-6,5 m). **Per rifarla (per l'assedio del Day 42):** una
pianta nostra con le torri ogni 30-60 m, le porte con le torri gemelle, un foro
rettangolare (come a Pompei) al posto della piazza circolare, il cardo e il decumano;
`@quota` della piana e del fiume, perché la «Marea Montante» allaga i guadi.

**Channathgate** (`P2D-Palio-Allegati/immagini/channathgate-mappa.png`, il
master visivo del DM, in stile Watabou; barra di 500 m). La cinta è un'ellisse
di circa 1,0 × 1,0 km, 80 ettari; l'abitato con i sobborghi arriva a 2,2 km. A
150 per ettaro fanno 12.000 persone dentro e forse 30-40.000 con i sobborghi:
più di Rethmar, mentre il canone la vuole «la più grande dopo Rethmar». Il
fiume corre da nord a sud fuori dalle mura, sul lato ovest; lo schema
`channathgate-citta.svg` lo fa scendere «a Rethmar (SO)», ma Rethmar sulla
regionale sta a ovest-nordovest. Le torri sono una ventina su 3,2 km, una ogni
160 m. La forma è quella di una città europea medievale. Il DM la vuole sulla
scala di Roma imperiale e mediorientale: Roma aureliana chiudeva 1.400 ettari,
Ctesifonte 3.000, la Baghdad rotonda circa 300 con quattro porte. **Per
rifarla:** decidere se Channathgate è più grande di Rethmar (allora si corregge
il canone) o più piccola (allora si stringe la mappa); per il carattere
persiano, una cittadella (*arg*) su una terrazza alta (Persepoli: 18 m), una
piazza grande (Naqsh-e Jahan: 560 × 160 m) e il bazar coperto che ne parte, i
giardini murati, l'acqua dei qanat; le torri ogni 30-60 m.

**Dauth** (`dauth-pianta.watabou.json` e le sei carte DAUTH A-E). Il canone non
dà né abitanti né misure: ha le mura con la Porta Sud e le mura ovest, un
tempio con chiostro diventato ospedale, una piazza per il Torneo e le cisterne
(nessun fiume, coerente con la regionale). La pianta Watabou non è ancora
generata: il seme c'è, la dimensione no. Le carte tattiche hanno mura di 2
quadretti e porta di 3, giuste. **Modello reale proposto:** Ávila, una città
murata in altura: 2,5 km di mura, alte 12 m e
spesse 3, 88 torri, 9 porte, 31 ettari, che a 150 per ettaro
farebbero circa 4.500 abitanti.
**Per rifarla:** generare la pianta con la dimensione dichiarata (piccola, 30 ha
circa), le torri fitte, le cisterne segnate; `@quota` e `@dislivello` sulle
carte A, B e D, che stanno all'aperto.

## Le 15 peggiori

| # | Voto | Mappa | Arco | Perché |
|---:|---:|---|---|---|
| 1 | 43 | 3Z L'Incrocio Silenzioso | **ARC-08** | sei porte fuori dai muri, 3,3 celle per creatura, nemici a contatto, nessun anello |
| 2 | 52 | Campo dei Cristalli Viventi | ARC-07 | due simboli ignoti, nord mancante, due porte fuori dai muri |
| 3 | 62 | Tarsilia, le stalle | Drappo | tre porte dei box fuori dai muri, vista libera ovunque |
| 4 | 63 | Tarsilia, la Ruota | Drappo | 2,1 Flip-Mat, 228 celle per creatura, due porte fuori dai muri |
| 5 | 65 | Tarsilia, versione giocatore | Drappo | come la Ruota |
| 6 | 73 | Desperate Last Stand | ARC-09 | quattro Grandi che non passano, treant senza taglia |
| 7 | 78 | 2B Attacco del Drago sui Bastioni | **ARC-08** | mura sottili al 100%, porta fuori dal muro, bastione senza copertura |
| 8 | 78 | 3Y Il Ponte Sospeso | **ARC-08** | nemici a contatto, porta fuori dal muro, vista libera |
| 9 | 80 | PF-4 Forgia Adamantina | ARC-07 | quattro vasche di lava segnate come fuoco, un ingresso, nessun anello |
| 10 | 81 | MAPPA 5 Il Cuore della Montagna | **ARC-08** | 2,6 Flip-Mat, portone di 9 m, un ingresso, nessun anello |
| 11 | 84 | Il Cuore della Montagna | ARC-07 | tattica a 3 m, un ingresso, nemici a contatto |
| 12 | 85 | MAPPA 4 Battaglia Finale Terrestre | **ARC-08** | tattica a 3 m, 3 Flip-Mat, 318 creature, il 93% senza copertura |
| 13 | 86 | 1A-3 Campo della Mano Rossa | **ARC-08** | strategica non dichiarata, tende a grappolo |
| 14 | 87 | 1A-1 Il Sentiero Nascosto | **ARC-08** | nemici a 70 m, 222 celle per creatura |
| 15 | 88 | PF-2 Sala della Forgia Eterna | ARC-07 | un ingresso, nessun anello, vista libera |

Fuori dalla classifica numerica, e prima di ogni griglia per l'assedio di
Rethmar e il Palio: **la regionale** (scala e fiume) e **Channathgate**
(grandezza e carattere), perché decidono le distanze di tutte le altre.
