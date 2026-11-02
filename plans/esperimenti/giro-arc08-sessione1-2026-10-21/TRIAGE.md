# Triage · ARC-08, Sessione 1 coi pregen (giro del 2026-10-21)

Fonti: i quattro rapporti di questa cartella, [`PLAYTESTER.md`](PLAYTESTER.md)
(32 rilievi, sigla **P#n**), [`LETTORE.md`](LETTORE.md) (59, **L#n**),
[`DEVELOPER.md`](DEVELOPER.md) (29, **D-Rn / D-An / D-Gn**) e
[`DM.md`](DM.md) (37, **DM-Rn / DM-Vn / DM-G1**). In tutto 157 rilievi,
uniti qui in **60 voci** più 7 rilievi respinti.

## Riepilogo

| | |
|---|---|
| Voci | **60** |
| 🔴 | **13** (T1-T7, T23-T25, T43-T44, T49) |
| 🟠 | **28** |
| 🟡 | **19** |
| Convergenti (2 lettori o più) | **40**, di cui **25** con 3 o 4 lettori e **14** trovate da tutti e quattro |
| Voci «DM?» | **2** |
| Respinti | 7 (in fondo, prima della struttura) |

Lavoro stimato per file, a correzione intera:

| File da correggere | Voci | Lavoro |
|---|---|---|
| `08_La Battaglia Di Hammerfist/ARC08-01-GUIDA-DM.md` (Sessione 1, righe 1194-1421; indice 39-47; nota 117-121; statblocchi dei pregen 691-870) | 22 | **il grosso**: la Sessione 1 si riscrive a scene (da ~230 a ~420 righe) con la struttura in fondo. Una giornata, 5-6 ore |
| `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md` | 20 | una ventina di righe puntuali, §13 riscritto, tabella della ferocia da ricalcolare con gli script. 2-3 ore |
| `ARC08-19-SEGRETI-DELL-ORDA.md` | 6 | §2 riscritto (mazzo, sergente, corno). 1 ora |
| `ARC08-15-HANDOUTS-GIOCATORE.md` | 8 | righe Abilità e Lingue sulle quattro schede, sei ritocchi alle carte, Handout 0. 1,5-2 ore |
| `ARC08-10-ESITI-E-CONTINGENZE.md` | 1 | tre righe di §5.1 e §5.4-bis. 15 minuti |
| `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` | 1 | copia delle righe dei pregen, sergenti allineati. 30 minuti |
| `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md` | 1 | una mappa nuova (il pendio di 1D). 1-1,5 ore con la pipeline |
| `plans/esperimenti/battaglia-campale-2026-10-21/*.py` | 1 | D22 e giganti negli script, poi le prove rifatte. 30 minuti |

In tutto, 12-14 ore. L'ordine sensato: script (T60) → libretto e segreti
(per avere i numeri) → handout → Sessione 1 riscritta → esiti e mappa.

**Le sole voci «DM?»**

1. **T28** · quando si spiega il libretto: tutto in apertura, come dice oggi,
   o trenta secondi in apertura e dieci minuti prima della scaramuccia.
2. **T31** · il §12 «Per il DM» resta nel libretto che hanno i giocatori, o
   passa nei Segreti.

### Decisioni del DM già prese, applicate qui senza richiederle

- Il flashback dei pregen si gioca **prima**, in tre sessioni; la
  **Sessione 1** è lettura del libretto + avvistamento + scaramuccia
  dell'avanguardia.
- **D22**: una trappola dell'avanguardia annulla una tacca del **Giorno 1 o
  del Giorno 2** (T25).
- L'incontro **1B** si gioca come **Consiglio di guerra e poi Preparazione
  delle difese**: l'attuale 1C diventa la seconda metà di 1B (T3, T8).
- Il **cancello ha 200 pf**. Nessuna voce di questo giro lo tocca: i pf del
  cancello servono ai combattimenti sulla mappa della Sessione 2, il libretto
  misura la breccia con le tacche. La riga «CA delle fortificazioni 23-27»
  dei Risultati sparisce (T2) e non va tradotta in pf.
- La **ritirata dell'avanguardia è di gruppo** (T24).
- **Numeri e mostri**: la versione più potente e terrificante, fonti
  nell'ordine D&D 3.5, Pathfinder 1e, SRD, con il segno su quello che non è
  SRD. Applicata in T4, T6, T25, T32, T39, T44 e negli statblocchi in fondo.

### Come si leggono le righe

Le righe della copia in freddo tradotte nel file vero, verificate con `diff`:

| Copia in `freddo/` | File vero | Scarto |
|---|---|---|
| `SESSIONE-1.md` riga *n* | `ARC08-01-GUIDA-DM.md` riga *n* + 1187 | esatto su tutte le 234 righe |
| `LIBRETTO.md` | `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md` | stesse righe (cambia solo la riga 13, il link all'ADR) |
| `HANDOUT-PREGEN.md` riga *n* | `ARC08-15-HANDOUTS-GIOCATORE.md` riga *n* + 15 | esatto; il file vero si chiama HANDOUT**S** |
| `SEGRETI-DM.md` | `ARC08-19-SEGRETI-DELL-ORDA.md` | identico |

Nelle voci tutte le righe sono già quelle dei file veri. Abbreviazioni:
`01` = `ARC08-01-GUIDA-DM.md`, `LIB` = `ARC08-18`, `SEG` = `ARC08-19`,
`HO` = `ARC08-15`, `10` = `ARC08-10`, `02` = `ARC08-02`.

Due cose che i lettori non potevano sapere, perché non avevano i file, e che
cambiano le correzioni: gli **statblocchi** di Fauci di Palude, Grimjaw,
Gorthak, Re Thorek e Madre Dana esistono già in `01` (157, 293, 336, 384,
419) e in `02` §1-§2; e quelli dei pregen in `01` 691-870 danno già alcune
caratteristiche (Int 12 a Dara e Thorin, For 14 / Int 14 / Sag 10 a Nala) e
Ascoltare/Osservare. Le **abilità** invece non ci sono da nessuna parte.

---

## 1. `ARC08-01-GUIDA-DM.md` · la Sessione 1

### 🔴

**T1 · 🔴 · La scaramuccia dell'avanguardia non c'è nella Sessione 1.**
P#1, L#1, D-R1, DM-R1, DM-V1 · quattro lettori.
- *Dove*: `01` 1386-1416 (Fase 3: solo 1E e 1F), indice 39-47, nota 117-121.
- *Correzione*: un incontro **1D · L'avanguardia** nella Fase 3, fra il drago
  (alba) e i presagi (notte). Una pagina sola per il DM (DM-R27): le quattro
  squadre e chi guida cosa, il mazzo per round (T43), il sergente (T44),
  «vale / non vale» (T26), la ritirata di gruppo e le trappole (T24), cosa
  porta all'assedio (T2), tempo 30-40 minuti. Rimanda a `LIB` §13 e `SEG` §2
  per le regole, ma il DM al tavolo legge da qui. Nell'indice (39-47) si
  aggiunge la riga. La nota 117-121 perde `[INFERRED — needs DM
  confirmation]` e prende `[CANONE — DM 2026-10-21]`. Struttura completa in
  fondo.
- *DM*: deciso.

**T2 · 🔴 · Gli esiti della serata sono in unità che il libretto non legge.**
P#3, P#7, L#5, D-R2, DM-R2 · quattro lettori.
- *Dove*: `01` 1347-1350 (ricompense di 1A), 1372-1382 (1C), 1418-1421
  (Risultati). Di riflesso `10` 231-237.
- *Difetto*: «+2 iniziativa di massa», «+2 CA alle mura», «trappole +2
  danni», «+1 morale», «−1 al primo assalto», «morale da −2 a +4», «CA delle
  fortificazioni 23-27». Il libretto ha morale che parte da +1, tacche e
  trappole che annullano una tacca. Le trappole di 1C (Ingegneria) e quelle
  di §13 sono due sistemi per la stessa cosa (P#7).
- *Correzione*: i Risultati diventano una scheda da compilare (*trappole N ·
  squadre travolte · morale della rocca M · leve ottenute · righe di `10`
  §5.1*) e ogni prova della serata dà una **leva del libretto**, con la
  tabella in fondo (§ «La tabella delle leve»). Il morale parte da **+1** e
  le leve ci si sommano, tetto ±5, sui dadi ±2 (`LIB` 153-157). Una sola
  famiglia di trappole: la prova di trappole della Preparazione dà **+1
  trappola** che si somma a quelle di 1D. Le righe «CA delle mura» e «CA
  delle fortificazioni» spariscono. «Intelligence completa» resta anche nel
  finale (`10` §5.1, «+2 iniziativa di massa» dei Rumbling Stones), ma
  nell'assedio dei pregen vale la leva.
- *DM*: no (D22 già applicata nella tabella).

**T3 · 🔴 · Il Consiglio di guerra non ha opzioni, esiti né PNG con una voce.**
P#4, L#15, D-A7, DM-R11 · quattro lettori.
- *Dove*: `01` 1354-1365.
- *Correzione*: 1B in due tempi, come ha deciso il DM. **1B-1 Il Consiglio**
  (sera del Giorno −3): le quattro «decisioni strategiche» sono quattro leve
  del libretto. *Distribuzione delle forze* = la tabella «Chi tiene cosa»
  (`LIB` 38-45); Diplomazia CD 18 riuscita: il gruppo scambia due reparti fra
  settori. *Difese magiche* = l'opzione B della Preparazione. *Strategie di
  resistenza* = il modo A/B/C di `LIB` §9 per ogni giocatore. *Evacuazione* =
  Diplomazia riuscita: la riga «Evacuazione» di `10` §5.3 non scende sotto
  «parziale». Re Thorek e Madre Dana prendono una riga ciascuno (cosa
  vogliono, una battuta) dai loro blocchi in `01` 384 e 419: il re vuole
  tenere il Cancello di persona e Borin glielo deve togliere dalla testa;
  Dana vuole le Cantitrici sulle Mura. **1B-2 La Preparazione** è l'ex 1C
  (T8).
- *DM*: deciso (1B = Consiglio, poi Preparazione).

**T4 · 🔴 · Ricognizione: pattuglia e scout senza statistiche.**
P#8, L#4, L#39, L#40, D-R4, DM-R8 · quattro lettori.
- *Dove*: `01` 1225 («Livello di Sfida 5-12»), 1248-1249 (pattuglia), 1256
  (prove contrapposte), 1291 (scout).
- *Correzione*: gli statblocchi in fondo (§ «Statblocchi mancanti»), dalle
  schede di *Red Hand of Doom* (D&D 3.5, non SRD) che il Bestiario ha già in
  `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/`. La pattuglia
  diventa **3 goblin cavalcatori di worg** (guerriero 5°) su **3 worg da 6
  DV**: è quello che dicono `02`, `ARC08-04` e il libretto («lupi e goblin»),
  e chiude L#40. Gli scout sono **9 hobgoblin regolari** (guerriero 3°) e il
  **sergente**, lo stesso della 1D. Al posto di «5-12»: pattuglia EL 9 circa,
  scout EL 9 circa, tutti e due insieme EL 11.
- *DM*: no.

**T5 · 🔴 · Ricognizione: nessun esito di fallimento, nessun allarme.**
P#8, P#11, L#11, D-R4, DM-R9 · quattro lettori.
- *Dove*: `01` 1226 (obiettivo), 1347-1350 (solo ricompense).
- *Correzione*: tre gradini, ognuno con il suo costo.

  | Come finisce 1A | Costo |
  |---|---|
  | **Pulito**: nessuno li vede, o chi li vede non torna e i corpi spariscono | niente; vale «Eliminazione silenziosa» (tabella delle leve) |
  | **Visti ma via**: un goblin fugge sul worg, o il sergente suona il corno | l'allarme arriva al campo in 3 round; niente «Eliminazione silenziosa»; in 1D i lupi arrivano già con **fronte due** dal round 1 |
  | **Scontro aperto**, nessuno fugge | nessun costo nell'assedio, ma dal torrione Dara ha 2 round invece di 5: una sola prova di Osservare |
  | Allarme e niente vista | riga «Ricognizione» di `10` §5.1 a «fallito» (+50 rinforzi nel finale) |

  Una pattuglia che non rientra viene cercata (P#11): se i corpi non si
  nascondono, il gradino è «visti ma via». Con le abilità dei pregen (T49) le
  CD fisse sono quasi certe: le CD fisse salgono di 5 (Osservare 25,
  Sopravvivenza 27, Nascondersi 27) oppure si tira contrapposto contro i
  modificatori degli statblocchi. Il vero pericolo è il fiuto dei worg (T15).
- *DM*: no.

**T6 · 🔴 · Il drago di 1F si può attaccare, e il testo non dice cosa succede.**
P#13, L#6, D-R5, DM-R14 · quattro lettori.
- *Dove*: `01` 1397-1416 (box 1399, opzioni 1413-1416).
- *Correzione*: lo statblocco c'è già (`01` 157-250, `02` 64-178: CA 29, 337
  pf, RD 10/magia, RI 21, volare 45 m scarsa, soffio in linea di 30 m 14d4
  acido Riflessi CD 29, Presenza terrificante 90 m Volontà CD 25). 1F non è
  uno scontro, e va scritto perché. Proposta nella versione più
  terrificante:
  - **quota 60 m** sopra le mura. Per l'SRD la Presenza terrificante scatta
    quando il drago sorvola: chi è sulle mura entro 90 m tira Volontà CD 25
    (i pregen sono scossi per 4d6 round se falliscono: Borin +8, Dara +9,
    Nala +11, Thorin +16). Il raggio di 90 m è un potenziamento non SRD, già
    segnato sul blocco (l'SRD dà 63 m all'adulto maturo);
  - le **baliste** tirano e non servono: i dardi non sono magici, la RD
    10/magia se li mangia. Il box dice «le baliste lo colpiscono, e lui non
    se ne accorge» invece di «abbastanza in alto da evitarle»;
  - si può colpire: Dara a 60 m è al secondo incremento (−2), con il nemico
    prescelto +2 tira a +19 contro CA 29; *Colpo infuocato* (66 m) lo
    raggiunge, RI 21 contro LI 12. Fauci non scende: se qualcuno lo colpisce
    risponde **una volta** con il soffio in linea sulla postazione da cui è
    partito il colpo, poi se ne va in 2 round;
  - le tre opzioni hanno ognuna la sua leva (tabella delle leve): la
    Presenza toglie **1** al morale della rocca; **Attaccare** con un colpo a
    segno lo rende e ne aggiunge 1 (+1 netto), al prezzo del soffio;
    **Rispondere con magia** (un incantesimo di 3° o più, visibile) lo rende
    (0 netto) e l'incantesimo è speso per 1D; **Ignorare** lascia il −1, ma
    chi lo ha proposto ha un gesto Comandare gratis nel round 1 di 1D.
- *DM*: no (preferenza già data: versione più terrificante).

**T7 · 🔴 · Il box del Consiglio parla ai PG della campagna, non ai pregen.**
P#5, L#2, L#47, DM-R11 · tre lettori (sale da 🟠 per convergenza: letto ad
alta voce rompe la cornice della visione).
- *Dove*: `01` 1356.
- *Correzione*: «…si raccolgono i capitani, i chierici e voi quattro: il
  nipote del vecchio re, il custode delle rune, l'occhio delle montagne e la
  barda che sa tutto di tutti.» La battuta di Dana senza la pausa scritta
  (L#47): «La situazione è grave. Sono sette contro uno. Ma noi abbiamo la
  montagna, e la montagna ha noi.»
- *DM*: no.

### 🟠

**T8 · 🟠 · La Preparazione delle difese non ha un tempo né un prezzo.**
P#20, L#16, D-A6 · tre lettori.
- *Dove*: `01` 1367-1382 (ex 1C).
- *Correzione*: «Ognuno ha **due azioni**, una per giorno di preparativi, al
  massimo una per area. Niente prendere 20: si lavora con l'orda in vista.
  Chi fallisce di 5 o più spreca l'azione.» Le prove si riscrivono sulle
  abilità che i pregen hanno (T49): niente più «Conoscenze (Ingegneria)»,
  che nessuno ha; le trappole si progettano con Sopravvivenza (Dara) o
  Artigianato (pietra) (Borin) CD 18. Opzione B: «Sapienza Magica CD 22 (Thorin
  +16), o un incantesimo di 3° o più consumato per la giornata: **+1 al
  bianco** nel settore di chi lo lancia, round 1 del Giorno 1». Thorin ha
  la sua scena (P#20): *Scolpire pietra* vale come un Artigianato (pietra)
  riuscito, le *Rune di potere* come la prova di Sapienza Magica. Otto azioni
  e sei leve: il gruppo sceglie.
- *DM*: no.

**T9 · 🟠 · La vista sul campo: Osservare a 400 m e cosa vede Dara.**
P#9, P#10, L#10, L#41, D-A5, DM-R10, DM-R25 · quattro lettori.
- *Dove*: `01` 1302-1327, 1336.
- *Correzione*: «Per contare un esercito non c'è penalità di distanza.» Il
  cannocchiale va sulla scheda di Dara (equipaggiamento in `01` 749, scheda `HO` 94-105), e senza
  la CD sale di 10. Un box letto «Cosa vede Dara», a gradini: **meno di 20**
  «sono più di quanti sappiate contare», orchi e hobgoblin a migliaia;
  **20** i numeri (novecento, sette contro uno) e gli otto giganti; **25** i
  chierici e gli sciamani, l'ettin e le catapulte, la tenda di Grimjaw (è
  «Intelligence completa»); **30** l'ombra del drago sulla palude e il suo
  cavaliere. Contro gli orchi Dara ha il nemico prescelto, +6.
- *DM*: no.

**T10 · 🟠 · 1E: gli agganci sono per Warlock, Druido e Monaco.**
P#12, L#17, D-A8, DM-R13 · quattro lettori.
- *Dove*: `01` 1392-1395.
- *Correzione*: gli stessi tre presagi coi pregen. Con l'ordine nuovo 1E
  viene dopo 1D (T11), quindi le leve vanno sull'assedio. **Thorin**
  (Conoscenze religione CD 15): l'odore di un sacrificio a Tiamat, la magia
  dei chierici dell'orda; al Giorno 1 tira con +2 il TS della carta «La palla
  di fuoco». **Dara** (Sopravvivenza CD 15): gli animali che scendono dicono
  da dove sale l'orda; nel round 1 del Giorno 1 gli orchi non hanno la
  Carica selvaggia. **Nala** (Ascoltare CD 18, in goblin): un canto di marcia
  col nome di Gorthak; +2 al primo attacco nel duello con lui. Esce «magia
  demoniaca (Generale Grimjaw)»: Grimjaw è un orog guerriero (`01` 293).
- *DM*: no.

**T11 · 🟠 · Cronologia della Fase 3 rovesciata e lettere degli incontri.**
P#6, L#9, L#36, D-G9, DM-R4, DM-R5 · quattro lettori.
- *Dove*: `01` 1386-1416; indice 39-47; rimandi in `ARC08-16-CUE-SONORI.md`
  55 e `ARC08-04-MARCIA-MANO-ROSSA.md` 103.
- *Correzione*: l'ordine è drago (alba) → avanguardia (pomeriggio) → presagi
  (notte), e la serata chiude sulla notte dei fuochi. Con 1C assorbito in 1B
  conviene rinumerare in ordine di tempo: **1A** ricognizione, **1B**
  consiglio e preparazione, **1C** il drago (ex 1F), **1D** l'avanguardia,
  **1E** presagi. Si aggiornano i due rimandi a «1F». Se si preferisce non
  toccarli, si tengono le lettere vecchie e si cambia solo l'ordine. Le
  «FASE 1/2/3» della sessione diventano «Giorno −3 / −2 / −1», e restano
  «Fase 1/2/3» solo dentro 1A.
- *DM*: no.

**T12 · 🟠 · Grimjaw, Gorthak e Fauci sono nomi senza volto, e il +2 contro Gorthak non ha una CA.**
L#14, D-A10, DM-R10, DM-V2 · tre lettori.
- *Dove*: `01` 1312-1319 (mappa 1A-3), 1349, 1393.
- *Correzione*: due righe ciascuno nel box di Dara (T9), prese dalle
  descrizioni in `01` 293 (Grimjaw, l'orog con la benda e tre dita mozze),
  336 (Gorthak, l'ettin a tre teste corazzato) e 157 (Fauci): aspetto e cosa
  vogliono. Per il +2 contro Gorthak: «nei primi 3 round del duello Sfidare»
  (L#42), contro CA 25 e 202 pf (fugge sotto 101); Grimjaw CA 26, 178 pf.
- *DM*: no.

**T13 · 🟠 · Hammerfist dentro le mura: chi comanda, chi cura, dove si prende quello che serve.**
P#14, L#13, DM-R11, DM-G1 · tre lettori.
- *Dove*: `01` 1354-1382.
- *Correzione*: un riquadro «Hammerfist in tre giorni», sei righe: Re Thorek
  nella sala del trono; Madre Dana al tempio di Moradin (cure, benedizioni,
  i componenti dal tesoro del tempio); l'armeria (riparazioni senza prezzo);
  la guardia della porta; niente mercato, la città è in guerra e si
  requisisce. I componenti dei pregen in T53.
- *DM*: no.

**T14 · 🟠 · L'apertura della serata è scritta in tre posti, e nessuno dice cosa preparare.**
P#1, L#20, L#23, L#51, DM-R28, DM-V1, DM-V3 · tre lettori.
- *Dove*: `01` 1194-1210; `HO` 18-23 e 72-74.
- *Correzione*: in testa alla Sessione 1 tre riquadri. **La serata in tre
  frasi**. **Apertura**: fuori gioco un minuto («stasera e per due serate non
  giocate i vostri personaggi»), Handout 0 letto, schede e carte sul tavolo,
  assegnazione di `HO` 61-63, chi non vuole un pregen lo dice ora, poi il box
  dell'odore e l'introduzione. **Cosa preparare**: le quattro schede con le
  carte, il libretto (§1-§11 e §13), quattro d20 rossi e quattro bianchi, il
  foglio dei reparti e il tracciatore (T35), le mappe 1A-1 e 1A-2, il pendio
  di 1D (T59). In `HO` 18-23 e 72-74 un solo momento: l'Handout 0 la
  settimana prima o in apertura, le schede in apertura.
- *DM*: no.

**T15 · 🟠 · Le risorse dei pregen saltano le prove, e il testo non lo sa.**
P#11, D-A5 · due lettori.
- *Dove*: `01` 1228-1256, 1262-1296; carta di Dara `HO` 164.
- *Correzione*: tre righe in 1A. **Il fiuto**: un worg sente chi passa entro
  9 m (18 m sottovento), invisibile o no; il sentiero passa a 6 m dalla
  pattuglia, quindi si passa sopravvento (Sopravvivenza CD 15) o si aspetta
  un round in più, con un'altra prova. **L'ora**: all'alba; la scurovisione
  di goblin e hobgoblin col chiarore non conta. **Il silenzio**: *Silenzio*
  copre chi ci sta dentro, e chi ci sta dentro non sente (Nala non origlia
  da lì). Sulla carta di Dara *Passare senza tracce* dice «niente orme né
  odore»: per l'SRD impedisce di seguire le tracce, anche col fiuto, ma non
  nasconde chi è a 9 m da un worg. La carta va corretta così.
- *DM*: no.

**T16 · 🟠 · Nessuno manda i quattro in ricognizione, e l'esercito si vede già dalle mura.**
L#7, L#8, DM-R12, DM-G1 · due lettori.
- *Dove*: `01` 1210, 1214-1219.
- *Correzione*: l'introduzione mostra polvere e fuochi a molte miglia, non la
  composizione (via «oceano di ferro»: quello lo vede Dara in 1A-3). «Il
  Rapporto delle Sentinelle» diventa una scena di cinque minuti: Re Thorek
  ascolta e manda i quattro, perché Dara conosce il crinale e Nala parla la
  lingua dei goblin. È il primo PNG che parla, e oggi il DM lo inventa.
- *DM*: no.

**T17 · 🟠 · Nessuna durata, né per scena né per la serata.**
P#21, DM-R30 · due lettori.
- *Dove*: `01` 1194-1421.
- *Correzione*: una riga di durata per scena e cosa tagliare, dalle due
  stime (che si somigliano): apertura 15'; 1A 45-60' (lo scontro con la
  pattuglia si risolve a racconto); 1B 45-60' (si taglia alle sole
  decisioni sui settori); pausa 10'; spiegazione del libretto 10-15'; drago
  10-15'; 1D 30-40' (il corno al round 4 se si è in ritardo), più 15' se
  qualcuno sfida il sergente; 1E e Risultati 10-15' (1E diventa il box).
  Totale 3 h 15 – 3 h 50; con il libretto letto tutto in apertura, oltre le
  4 ore.
- *DM*: no.

**T18 · 🟠 · La sessione finisce su due righe: niente chiusura, niente ponte.**
L#19, DM-R4 · due lettori.
- *Dove*: `01` 1418-1421.
- *Correzione*: un box di chiusura sulla notte dei fuochi (1E), poi la scheda
  dei Risultati di T2, poi una riga: «le leve si leggono all'alba del Giorno
  1, all'inizio della Sessione 2».
- *DM*: no.

### 🟡

**T19 · 🟡 · La nota del carry-over di Skullcrusher non serve ai pregen.**
L#18, DM-R14 · due lettori.
- *Dove*: `01` 1401-1411.
- *Correzione*: nessun pregen porta un artefatto, e i numeri di Fauci non
  cambiano in Sessione 1. La nota si riduce a una riga: «Il carry-over del P5
  tocca Fauci solo nel finale (blocco di Fauci, `01` 157); coi pregen non
  scatta.» Il resto vive già sul blocco.
- *DM*: no.

**T20 · 🟡 · Residui di lavorazione nel testo che il DM legge.**
P#31, L#35, L#37, L#38, L#43, L#48, DM-R5, DM-R6, D-G2 · quattro lettori.
In parte respinti: vedi in fondo.
- *Dove*: `01` 1197 («6-8 righe» sopra un box di quattro), 1234-1236 e
  1269-1271 (scale ASCII «~5 m», «~3 m» contro la griglia da 1,5 m), 1287 e
  1296 (Borin in copertura o sul fianco), 1318 e 1322 («SUPPORT_MAGICO»,
  «Worg Riders»).
- *Correzione*: «4 righe»; sotto ogni schizzo «non in scala: la griglia è in
  `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`», con la distanza fra
  sentiero e pattuglia scritta in metri (6 m, T15); Borin in copertura e il
  fiancheggiamento come scelta, «se gli scout lo vedono»; «SUPPORTO MAGICO»,
  «Goblin su worg».
- *DM*: no.

**T21 · 🟡 · La prosa dei box letti.**
L#44, L#45, L#46 · un lettore.
- *Dove*: `01` 1210, 1390, 1399.
- *Correzione*: «si rivela essere» → «è»; via «come promesse di morte» e
  «battito cardiaco impazzito»; «puntellano» → «punteggiano»; «le stelle sono
  più deboli» → «le stelle si vedono appena»; via la chiusa «il drago sta
  annunciando la sua presenza»; in 1F «abbastanza in alto … abbastanza in
  basso» → «alto sopra le torri, e basso quanto basta perché tutti lo
  vedano»; via «letteralmente»; il messaggio non è una frase del drago: «Non
  ha bisogno di parlare.»
- *DM*: no.

**T22 · 🟡 · I pregen di `01` 691-870 sono la fonte delle schede.**
Dal triage, nessun lettore (non avevano il file).
- *Dove*: `01` 697 (Borin: Ascoltare/Osservare +2 senza caratteristiche),
  691-870.
- *Correzione*: la riga Abilità e Lingue di T49 entra qui prima che nelle
  schede, e Borin prende Int 10, Sag 10, Car 12 (la sua Volontà +8 torna con
  Sag 10; Ascoltare e Osservare +2 con due gradi ciascuno).
- *DM*: no.

---

## 2. `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md`

### 🔴

**T23 · 🔴 · Il libretto dice che nella Sessione 1 la battaglia campale non c'è.**
P#15, L#21, D-R1, DM-R3 · quattro lettori.
- *Dove*: `LIB` 238-240 contro 361-363.
- *Correzione*: «Nella Sessione 1 la battaglia campale c'è solo
  nell'avanguardia (§13): il capitano guida una squadra di guastatori in più,
  e chi ha scelto l'orda pesca le carte dell'avanguardia.» Il resto in T27.
- *DM*: no.

**T24 · 🔴 · Ritirata e trappole: la regola scritta non è quella provata, e ha una scelta dominante.**
P#23, L#54, D-R6 · tre lettori.
- *Dove*: `LIB` 373-379, 392-395.
- *Correzione* (la ritirata di gruppo l'ha decisa il DM; le trappole contate
  sul gruppo sono quello che lo script già fa):
  - 373-374: «Ogni due round di scavo fanno una trappola, **contati su tutto
    il gruppo**: quattro squadre che scavano un round fanno due trappole.»
  - 377-379: «La ritirata è **di tutto il gruppo**: alla fine di ogni round
    si decide insieme se restare. Una squadra sola non si ritira; può solo
    smettere di scavare e combattere (Colpire o Tenere).»
  - 392-395: «chi si ritira dopo il terzo round porta a casa in media cinque
    trappole, una volta su tre sei o più, e perde una squadra ogni quattro
    serate; dopo il quarto, lo stesso numero di trappole e quasi una squadra
    persa ogni volta. Dopo il secondo, quattro trappole sicure.» (Simulazioni
    del developer, ferocia feroce, 3000 prove: round 2 = 4,00 trappole e 0
    squadre; round 3 = 5,07 e 0,25; round 4 = 5,01 e 0,89; round 6 = 2,23 e
    2,93.)
- *DM*: deciso.

**T25 · 🔴 · D22: le trappole valgono il Giorno 1 o il Giorno 2, e la tabella della ferocia va rifatta.**
D-R7, più la decisione del DM.
- *Dove*: `LIB` 200, 387-390, 316-320; `SEG` 60; `10` 280-282; script
  `assedio_v3.py` 135.
- *Correzione*: in tutti e quattro i testi «annulla una tacca **del Giorno 1
  o del Giorno 2**, nel settore che volete». Nello script `giorno == 1`
  diventa `giorno <= 2`. Poi la tabella di `LIB` 316-320 si rifà con le
  prove: con le trappole valide due giorni la riga «Feroce» passa da 7 a 8-9
  su 10 di breccia contenuta (D-R7). La tabella si rifà insieme a T32 (un
  macigno per settore, la regola che le prove già usano): con un macigno
  solo per giorno la feroce salirebbe ancora. Si pubblicano i numeri che
  escono, senza abbassare la ferocia di default.
- *DM*: deciso (D22); il resto è conto.

### 🟠

**T26 · 🟠 · Quali regole dell'assedio valgono sul pendio.**
P#18, P#24, L#54, DM-R16 · tre lettori.
- *Dove*: `LIB` 371-382.
- *Correzione*: tre righe «vale / non vale» in §13. Non vale il +1 al bianco
  del primo giorno (non ci sono mura). Vale il morale della rocca: parte da
  +1 più le leve di 1B e del drago. Una squadra travolta, o a 0 PFU (D-A3), è
  un reparto perso: −1 al morale. Vale l'eroe ferito. Le tacche si contano
  per squadra. I guastatori, travolti o no, non entrano nell'assedio.
- *DM*: no.

**T27 · 🟠 · Il capitano e il giocatore dell'orda, stasera.**
L#22, D-G11, DM-R21 · tre lettori.
- *Dove*: `LIB` 231-240; `01` 1228-1256.
- *Correzione*: in 1A il capitano guida due esploratori nani di scorta (prove
  di gruppo a +8 piatto, nessuna scheda); in 1D guida una quinta squadra di
  veterani senza eroe, che scava e non combatte. Il giocatore dell'orda in
  1A tira Osservare e Ascoltare dei nemici (statblocchi in fondo), in 1D pesca
  le carte e decide su quale squadra cadono i lupi; gli si dà solo `SEG` §2.
  Se rifiuta chi doveva giocare Dara, Dara passa a un altro giocatore.
- *DM*: no.

**T28 · 🟠 · DM? · Quando si spiega il libretto.**
P#21, DM-R29 · due lettori.
- *Dove*: `LIB` 3-4, 361-363; `01` 117-121.
- *Difetto*: letto tutto in apertura (25-45 minuti), il primo dado rosso
  arriva tre ore dopo, e nessuno se lo ricorda.
- *Correzione proposta*: trenta secondi in apertura («più tardi guiderete i
  vostri soldati; vi spiego come quando succede»); dieci-quindici minuti
  prima di 1D con §1, §3, §4 (e Scavare), §5 (Combattere e Comandare), §7 (la
  tacca); il primo round giocato piano, come l'esempio di §10. §6, §8 e §9 alla
  Sessione 2. Nel libretto una riga «cosa si spiega stasera, cosa la prossima
  volta».
- *DM?*: sì. La decisione di oggi mette la lettura del libretto nella
  Sessione 1 e la elenca per prima; questa proposta la tiene nella Sessione 1
  ma la sposta e la spezza.

**T29 · 🟠 · Le carte dei poteri traducono le durate con criteri diversi, e non si sa se un incantesimo minore costa il gesto.**
P#19, P#22, DM-R24 · due lettori.
- *Dove*: `LIB` 126-136; carte `HO` 150, 166, 189, 197, 199, 224, 228.
- *Correzione*: una regola in §5. «Un incantesimo sotto il 3° livello si
  lancia e non costa il gesto: un round di battaglia sono dieci round. Un
  effetto che dura 10 round o più vale per il round di battaglia in cui lo
  lanci (*potere divino*, *potere della giustizia*); sotto i 10 round non vale
  nella battaglia campale (*postura difensiva*). Gli aiuti che aiutano tutti
  (*preghiera*, *eroismo*, *velocità*, il canto) valgono per il giorno.» Le
  carte si allineano a questa riga.
- *DM*: no.

**T30 · 🟠 · «Due uguali non si sommano»: uguali come?**
L#27, D-G8 · due lettori.
- *Dove*: `LIB` 134-136.
- *Correzione*: «Gli aiuti che durano tutto il giorno non si sommano fra loro:
  un reparto ne ha uno solo.»
- *DM*: no.

**T31 · 🟠 · DM? · Il §12 «Per il DM» sta nel libretto che hanno i giocatori.**
L#56, DM-R26 · due lettori.
- *Dove*: `LIB` 306-356 contro `LIB` 3, 202-203 e `HO` 64-66.
- *Difetto*: il libretto è «lo stesso per tutti» e dice che le capacità
  dell'orda «le scoprirete sul campo», poi elenca il mazzo, le carte (il
  soffio del terzo giorno, la ritirata), le percentuali e la tabella dei
  bonus, che l'Handout 0 dice di non dare ai giocatori.
- *Correzione proposta*: (a) §12 passa in `SEG` come §4, e nel libretto resta
  solo «Il tempo»; oppure (b) una riga in testa: «§12 non va nelle copie dei
  giocatori». Consigliata la (a): toglie la contraddizione con ADR-0096 senza
  stampare due libretti. «Quanto restare» (§13) resta nel libretto: serve
  alla scelta della ritirata.
- *DM?*: sì, tocca il principio del libretto unico.

**T32 · 🟠 · Le percentuali della ferocia contano un macigno in ogni settore; il libretto ne concede uno.**
D-A1 · un lettore.
- *Dove*: `LIB` 322, 330.
- *Correzione*: la carta «I giganti» diventa «round 2: **un macigno per
  settore**». È la versione che le prove hanno misurato ed è la più dura;
  la tabella si rifà con T25.
- *DM*: no (preferenza già data).

**T33 · 🟠 · Nala non ha niente da fare nell'avanguardia.**
D-A4 · un lettore.
- *Dove*: `LIB` 371-385.
- *Correzione*: «**L'inganno** (Nala, o chiunque abbia un'illusione o un
  ammaliamento di 1° o più): il reparto nemico davanti alla tua squadra tira
  il TS, d20 + 4 contro la CD dell'incantesimo; se fallisce, per quel round
  non tira il bianco e la squadra non prende la tacca.» Con *immagine
  silenziosa* (CD 15) riesce metà delle volte, con *affascinare* (CD 18) due
  su tre.
- *DM*: no.

**T34 · 🟠 · Il libretto avverte su Tenere con un numero sbagliato.**
D-A9 · un lettore.
- *Dove*: `LIB` 108-111.
- *Correzione*: «Tenere sempre salva i reparti e perde le mura: nelle prove,
  chi tiene sempre arriva alla ritirata con quasi tutti i reparti, ma chiude
  i primi due giorni senza brecce solo una volta su quattro. Caricare sempre
  perde tutte e due le cose.» Da ricontare dopo T25.
- *DM*: no.

**T35 · 🟠 · Il foglio dei reparti e il tracciatore dell'orda non ci sono.**
DM-R31 · un lettore.
- *Dove*: `LIB` 34-36.
- *Correzione*: una facciata stampabile in coda al libretto (§14 o un handout
  in `HO`): per giocatore due reparti coi quadratini dei PFU, le tacche, gli
  ordini; sul retro la tabella unica, gli ordini e i gesti. Per il DM, in
  `SEG`, un tracciatore: quattro squadre, fino a due reparti nemici
  ciascuna, coi PFU.
- *DM*: no.

### 🟡

**T36 · 🟡 · Nessuna riga di scala.** D-G1.
- *Dove*: `LIB` 387-390; `01` 1224-1350.
- *Correzione*: «Con tre giocatori le soglie sono 5 / 2-4 / meno di 2, e il
  capitano porta la quarta squadra senza eroe. Con cinque, il quinto guida
  una squadra di veterani senza eroe, e le soglie salgono a 7 / 4-6.» In 1A,
  con tre pregen, gli scout sono sei più il sergente.

**T37 · 🟡 · Borin guida veterani o Guardia nell'avanguardia?** D-G3.
- *Dove*: `LIB` 366. *Correzione*: «Borin la Guardia del Cancello, Thorin e
  Nala veterani, Dara balestrieri», come lo script.

**T38 · 🟡 · Le Mura il primo giorno: +1 o +2?** D-G4.
- *Dove*: `LIB` 196-198. *Correzione*: «+1 al bianco **dal secondo
  giorno**, finché le Mura non hanno ceduto una volta (il primo giorno vale
  già il +1 di tutti).»

**T39 · 🟡 · L'eroe ferito quasi non scatta, e non conta.** D-G7.
- *Dove*: `LIB` 145-147. *Correzione*, nella versione più dura: si tiene, e
  conta: «l'eroe ferito ha −2 al gesto del round dopo».

**T40 · 🟡 · La riga degli eroi dà a Dara +19 e basta.** P#32.
- *Dove*: `LIB` 301-302. *Correzione*: «Dara **+19** (+25 contro gli orchi,
  +23 contro i giganti, +21 con *grazia del gatto*)».

**T41 · 🟡 · La ferocia ha un nome negli script e un altro nel libretto.** D-G12.
- *Dove*: `LIB` 320. *Correzione*: «Negli script: normale = 1, feroce = 2,
  terrificante = 3.»

**T42 · 🟡 · Piccole ambiguità.**
L#52, L#53, L#55, P#25, DM-R18, DM-R19 · tre lettori.
- *Dove e correzione*: `LIB` 21-23, «un reparto è una decina di soldati»
  (Guardia e veterani hanno 12 e 11 PFU); 197, «e l'orda in salita non
  allarga il fronte»; 244-246, «il settore che cede col d6 conta come
  breccia»; 367-368, «le trappole sono già a metà: i round sono gli ultimi
  colpi di piccone»; in §13, «Scavare davanti ai lupi fa −4 al bianco: ditelo
  prima del primo round»; 258-259, «il macigno lo tira il DM: è l'unico tiro
  che non tirate voi».

---

## 3. `ARC08-19-SEGRETI-DELL-ORDA.md`

### 🔴

**T43 · 🔴 · L'avanguardia non ha un mazzo.**
P#16, L#30, D-A3, DM-R15 · quattro lettori (sale da 🟠: al round 3-4 il DM
si ferma).
- *Dove*: `SEG` 37-41; `LIB` 376, 380.
- *Correzione*, nella versione più dura e uguale allo script: «Round 1-2:
  un reparto di lupi e goblin per squadra; se cade, ne arriva un altro.
  Dal round 3 ogni reparto distrutto è sostituito da un reparto di hobgoblin,
  senza limite: l'avanguardia è lunga quanto la pazienza del gruppo. Round 4:
  niente. Round 5: il corno. Ferocia: quella dell'assedio, feroce se il DM
  non dice altro.» In `LIB` 380: «alla terza tacca, **o a 0 PFU**, la
  squadra fugge… l'eroe torna con lei, con i punti ferita che ha».
- *DM*: no.

**T44 · 🔴 · Il sergente: la sfida arriva quando non serve più, e non ha statistiche.**
P#17, L#28, L#29, D-A2, DM-R17 · quattro lettori.
- *Dove*: `SEG` 43-46; `LIB` 137-143, 383-385; `01` 1291.
- *Correzione*: in `LIB` 383-385 due regole separate. «**Sfidare il
  sergente**: dal round 3 un eroe lascia la sua squadra per un round e sfida
  il sergente sulla mappa, come il gesto Sfidare di §5. In quel round la sua
  squadra tira senza di lui e non prende tacche. Sotto metà dei punti ferita
  il sergente fugge, e il suo +1 esce.» «**La retroguardia**: chi resta
  indietro copre la ritirata di tutti; in quel round nessuna squadra è
  travolta.» In `SEG` 44 lo statblocco (in fondo) e la riga: «è lo stesso
  sergente della postazione di 1A: se in 1A è morto o preso, la carta del
  round 3 arriva senza il suo +1». La mappa del pendio in T59.
- *DM*: no.

### 🟠

**T45 · 🟠 · Le capacità «senza annunciarle», ma il bersaglio lo calcolano i giocatori.**
L#32, DM-R20 · due lettori.
- *Dove*: `SEG` 15-16; `LIB` 66-72.
- *Correzione*: «Il DM dice sempre il numero del bersaglio («stavolta contro
  32»). La prima volta racconta quello che si vede, senza spiegare la
  regola.»
- *DM*: no.

**T46 · 🟠 · Il corno di Grimjaw «va letto ad alta voce», e il testo non c'è; Grimjaw sulla cresta è a tiro?**
P#30, L#31 · due lettori.
- *Dove*: `SEG` 41-42.
- *Correzione*: la cresta è a 400 m, fuori dalla portata dell'arco di Dara
  (330 m). Il box: «Dalla cresta viene un suono lungo, basso, che non è di un
  animale. Le file degli hobgoblin si fermano tutte insieme, e poi ripartono
  più in fretta. Lassù, contro il cielo, un orog con una benda nera guarda
  giù e non si muove.»
- *DM*: no.

### 🟡

**T47 · 🟡 · I giganti e le merlature.** D-G5.
- *Dove*: `LIB` 330 contro `SEG` 24. *Correzione*: `LIB` 330 «(con il +1 del
  primo giorno e il morale; le merlature delle Mura non contano)», e lo
  script toglie le merlature dal tiro dei giganti.

**T48 · 🟡 · Formazione tattica: i guerrieri hobgoblin contano?** P#29, D-G6.
- *Dove*: `SEG` 22. *Correzione*: «due o più reparti di hobgoblin (i
  guerrieri non contano: non marciano al tamburo)», come lo script e
  l'esempio di `LIB` 252-275.

---

## 4. `ARC08-15-HANDOUTS-GIOCATORE.md`

### 🔴

**T49 · 🔴 · I pregen non hanno abilità, lingue né tutte le caratteristiche, e la serata è fatta di prove.**
P#2, L#3, L#12, D-R3, D-G10, DM-R7, DM-V3, DM-R25 · quattro lettori.
- *Dove*: schede `HO` 82-129; fonte `01` 691-870 (T22); copia in `02`
  612-722.
- *Correzione*: una riga **Abilità** e una **Lingue** per scheda, gradi
  massimi dell'SRD (livello + 3), con le caratteristiche dei blocchi di `01`.
  Tabella in fondo (§ «Abilità e lingue dei pregen»). «Linguaggi (parlare
  Orco/Goblin)» in `01` 1345 esce: Nala parla orchesco e goblin, capisce gli
  ordini entro 9 m (Ascoltare CD 15, o Nascondersi contrapposto se vuole
  restare nascosta). Sulla carta di Nala una riga per le capacità della Spia
  Maestra (Master Spy, *Complete Adventurer*, non SRD) che il DM usa.
- *DM*: no.

### 🟠

**T50 · 🟠 · Se un pregen muore, il giocatore cosa gioca?**
L#25, DM-R17 · due lettori.
- *Dove*: `HO` 43-47; `LIB` 231-240.
- *Correzione*: «Se il tuo eroe muore, per il resto della visione giochi da
  capitano (modo C). Nella Sessione 1, dopo la ricognizione, guidi in 1D la
  squadra di guastatori del caduto, senza gesto.»
- *DM*: no.

**T51 · 🟠 · Tre giorni o sei?**
L#24 · un lettore.
- *Dove*: `HO` 29-30.
- *Correzione*: «…quelli la Corona li trattiene: i giorni in cui Hammerfist
  si è preparata e ha tenuto le mura senza di voi.»
- *DM*: no.

**T52 · 🟠 · Thorin, Thorek, Thorik; Dara e Dana.**
P#26, L#26 · due lettori.
- *Dove*: `HO` 61-63; `01` 1356.
- *Correzione*: i nomi sono canone e `02` 9 li disambigua già; non si
  cambiano. Al tavolo e nei box il re è «il Re» o «Thorek Hammerfist», Dana
  è «la Madre Superiora», il pregen è «Runaforte». Una riga in `HO` 61-63 lo
  dice.
- *DM*: no. (Rinominare sarebbe una scelta di canone: non proposta.)

### 🟡

**T53 · 🟡 · Componenti materiali, costi in PE e *Guarigione* su un reparto.**
P#14, L#58, DM-R24 · tre lettori.
- *Dove*: `HO` 184, 187, 190, 238; carta di Thorin per *Comunione*.
- *Correzione*: equipaggiamento di Thorin: due dosi di polvere di diamante da
  250 mo (*pelle di pietra*), un diamante da 5.000 mo (*rianimare morti*); di
  Nala: una perla da 100 mo (*identificare*). *Comunione* costa 100 PE: si
  pagano dai PE del livello (i pregen non ne guadagnano, ma ne hanno).
  *Guarigione* su un reparto: «**1 PFU**», non 1d4, perché è un bersaglio
  solo e il libretto tiene 1d4 per le cure di massa.

**T54 · 🟡 · Il Canto di Guerra Nanico non si capisce.** L#59.
- *Dove*: `HO` 224. *Correzione*: «Quando canti Ispirare Coraggio, i nani
  alleati hanno +1 in più a colpire (+3 in tutto). Nel libretto non cambia
  niente: il canto dà +1 ai dadi per il giorno.»

**T55 · 🟡 · Etichette di lavorazione nel testo per i giocatori.** L#49, L#50.
- *Dove*: `HO` 25 («(BG3 lead, LotR support)»), 27 («il filo del Rubino»),
  60 e 74 (`[INFERRED]`, sigle D4/D6); `LIB` 325.
- *Correzione*: via l'etichetta di stile; il Rubino o si spiega in mezza riga
  o si toglie; le sigle restano solo nelle note per il DM. Dove la decisione
  di oggi chiude un `[INFERRED]`, diventa `[CANONE — DM 2026-10-21]`.

**T56 · 🟡 · Handout 0 pensato solo per il gruppo della campagna; carta di Thorin di due pagine.** DM-R22, DM-R23.
- *Correzione*: rinviato. Una presentazione per un tavolo senza la campagna
  non serve a questo giro; la carta di Thorin si stampa su due facciate e
  `HO` 76-77 dice «una pagina l'una, quella di Thorin due».

---

## 5. Gli altri file

**T57 · 🟠 · `ARC08-10-ESITI-E-CONTINGENZE.md`: §5.1 e §5.4-bis da allineare.**
D-R2, D-R7, DM-R2 · due lettori.
- *Dove*: `10` 231-237, 269-287.
- *Correzione*: §5.1 «Difese preparate (Incontro 1B)» → «(trappole di 1D e
  della Preparazione)»; §5.4-bis 280-282 «una tacca del Giorno 1 o del Giorno
  2» (D22); §5.4-bis perde `[INFERRED]` sulla struttura della Sessione 1,
  decisa oggi; una riga che rimanda alla tabella delle leve della Sessione 1.

**T58 · 🟡 · `ARC08-02`: le schede §3 e i sergenti.**
Dal triage.
- *Dove*: `02` 612-722 (schede stampabili), 854-866 («Hobgoblin sergenti»:
  CA 18, 38 pf).
- *Correzione*: le righe di T49 anche qui; il sergente dell'avanguardia è il
  guerriero 6° dello statblocco in fondo (più forte di quello di unità), e
  `02` 854 lo dice in una riga, così le due schede non si contraddicono.

**T59 · 🟠 · `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`: il pendio di 1D non ha mappa.**
P#17, D-G2, DM-R32 · tre lettori.
- *Correzione*: una **MAPPA 1D — Il pendio** di 12×12 quadretti da 1,5 m: il
  sentiero sotto le mura, quattro cantieri di guastatori, pini abbattuti,
  una frana preparata, la cresta di Grimjaw a nord fuori mappa (400 m). Si
  usa per Sfidare il sergente e per la retroguardia. Le mappe 1A-1 e 1A-2 si
  stampano con la sessione.

**T60 · 🟡 · Gli script della battaglia campale.**
D-R6, D-R7, D-A1, D-G3, D-G5 · un lettore.
- *Dove*: `plans/esperimenti/battaglia-campale-2026-10-21/assedio_v3.py` 84-90
  e 135; `avanguardia.py` 17.
- *Correzione*: trappole `giorno <= 2`; giganti un macigno per settore (già
  così: la tabella si rifà con questo); le merlature fuori dal tiro dei
  giganti; Borin con la Guardia resta. Poi si rifanno le prove per T25, T34
  e la riga «Quanto restare» di T24.

---

## Rilievi respinti

| Rilievo | Perché |
|---|---|
| **P#27** (incantesimi di Thorin uno in più per livello) | Chierico 12° nell'SRD: 6/5/5/5/4/3/2, più i bonus di Sag 22 (2/2/1/1/1/1): 4° = 5, 3° = 6, 2° = 7, come la carta. Il conto del rapporto ha saltato i bonus |
| **P#28** (attacchi di Thorin) | Il BAB di Thorin è +8 (`01` 786): *arma spirituale* +8 +6 Sag = +14; *potere divino* 12 + For 22 (+6) + 2 + 1 = +21. La carta ha ragione |
| **L#57** (Postura Difensiva alza la Volontà) | La carta dice «+2 ai TS sulla Volontà»: +8 → +10 torna |
| **L#34, DM-V4** («4. CAPITOLO 2» in testa) | Nel master è il titolo giusto del capitolo: l'ha prodotto il taglio della copia |
| **L#35, DM-R6, L-RIFERIMENTO** (rimandi a `ARC08-16`, `ERRATA-…`, `Mappe/…`, `ARC08-10`, `ARC07-DEF-5`) | I file esistono nel repo; mancavano solo nel pacchetto a freddo. Resta da stampare le mappe con la sessione (T59) |
| **L#50** (nomi dei file diversi) | Le copie erano rinominate per il giro (`SEGRETI-DM.md` = `ARC08-19-SEGRETI-DELL-ORDA.md`) |
| **DM-R19 come difetto** | Non è sbagliato; resta come riga di chiarezza in T42 |

---

## 6. Struttura proposta: la Sessione 1 riscritta a scene

Destinazione: `01` 1194-1421, che si sostituisce intero. Lettere in ordine
di tempo (T11). Ogni scena con: titolo, *in scena* in una frase, durata,
box letto, cosa possono fare i pregen, esiti con le leve.

### Testata (tre riquadri, T14)

- **La serata in tre frasi.** Tre giorni prima dell'assedio, quattro nani di
  Hammerfist spiano l'orda, decidono la difesa e preparano le mura. All'alba
  dell'ultimo giorno il drago si mostra; nel pomeriggio le loro squadre
  scavano trappole sul pendio finché l'avanguardia della Mano Rossa non le
  scaccia. Quello che portano a casa decide come comincia l'assedio.
- **Cosa preparare**: schede e carte, libretto (§1-§11 e §13; §12 secondo
  T31), 4 d20 rossi e 4 bianchi, foglio dei reparti e tracciatore (T35),
  mappe 1A-1, 1A-2 e 1D, questa pagina di statblocchi.
- **Tempi**: tabella di T17, con la scena da tagliare.

### Le scene

| # | Scena | Quando | Durata | Cosa contiene |
|---|---|---|---|---|
| 0 | **Apertura** (fuori gioco) | | 15' | un minuto per la cornice, Handout 0, schede e carte, chi non vuole un pregen (T27), trenta secondi sul libretto (T28) |
| 1 | **La notte prima** | Giorno −4, notte | 5' | box dell'odore (`01` 1199-1201), introduzione riscritta (T16, T21) |
| 2 | **Il rapporto delle sentinelle** | Giorno −3, alba | 5' | Re Thorek ascolta e manda i quattro; prima battuta del re (T16) |
| 3 | **1A · La ricognizione** | Giorno −3, mattina | 45-60' | Fase 1 il sentiero (pattuglia, fiuto, vento: T4, T15); Fase 2 il torrione (scout e sergente); Fase 3 la vista: box «Cosa vede Dara» a gradini (T9, T12); tre esiti (T5) |
| 4 | **1B · Il Consiglio di guerra** | Giorno −3, sera | 25' | box corretto (T7); Re Thorek e Madre Dana con una voce (T3, T13); quattro decisioni = quattro leve |
| 5 | **1B · La Preparazione delle difese** | Giorno −2 | 20-30' | due azioni a testa, tre opzioni, prove sulle abilità vere, le leve (T8) |
| | *Pausa · spiegazione del libretto* | | 10' + 10-15' | §1, §3, §4 con Scavare, §5, §7; primo round lento (T28) |
| 6 | **1C · La dimostrazione di forza** (ex 1F) | Giorno −1, alba | 10-15' | Fauci a 60 m, Presenza terrificante, baliste inutili, tre opzioni con le leve (T6) |
| 7 | **1D · L'avanguardia** | Giorno −1, pomeriggio | 30-40' (+15') | la pagina unica: squadre (Borin Guardia, Thorin e Nala veterani, Dara balestrieri, capitano con una quinta squadra), Scavare, fronte 1 poi 2, mazzo per round (T43), corno al round 5 (T46), Sfidare il sergente e retroguardia (T44), l'inganno di Nala (T33), vale / non vale (T26), ritirata di gruppo e trappole sul gruppo (T24), cosa porta all'assedio |
| 8 | **1E · Presagi funesti** | Giorno −1, notte | 10' | box corretto (T21); un presagio per Thorin, Dara e Nala (T10); box di chiusura (T18) |
| 9 | **Risultati** | | 5' | la scheda da compilare e la tabella delle leve (sotto) |

### La tabella delle leve (T2)

Cosa porta ogni esito della serata nel libretto. Il morale della rocca parte
da **+1**; le leve di morale si sommano, tetto ±5, sui dadi ±2.

| Esito della serata | Leva nell'assedio (libretto) | Riga di `10` §5 |
|---|---|---|
| 1A · Osservare 25+ («Intelligence completa») | Giorno 1: ogni giocatore vede a inizio round il primo reparto del mazzo del suo settore | §5.1 Ricognizione «pieno» |
| 1A · Osservare 20-24 | nessuna | §5.1 «parziale» |
| 1A · allarme e nessuna vista | in 1D i lupi hanno fronte due dal round 1 | §5.1 «fallito» (+50 rinforzi nel finale) |
| 1A · «Eliminazione silenziosa» (gradino «pulito» di T5) | la carta **I giganti** non si gioca il Giorno 1 | |
| 1A · prigionieri interrogati (Intimidire CD 23) | +2 a colpire nei primi 3 round del duello **Sfidare** contro Gorthak | |
| 1A · sergente degli scout morto o preso | in 1D il round 3 arriva senza il +1 del sergente | |
| 1B-1 · Diplomazia CD 18 (Consiglio) | il gruppo scambia due reparti fra settori in «Chi tiene cosa» | |
| 1B-1 · evacuazione (Diplomazia CD 18) | | §5.3 Evacuazione non sotto «parziale» |
| 1B-2 · Artigianato (pietra) CD 20 o *scolpire pietra* | +1 al bianco in un settore a scelta, Giorno 2 | |
| 1B-2 · trappole progettate (Sopravvivenza o Artigianato CD 18) | **+1 trappola**, sommata a quelle di 1D | §5.1 Difese preparate |
| 1B-2 · Diplomazia CD 16 (Nala fra le truppe) | morale **+1** all'alba del Giorno 1 | |
| 1B-2 · Intimidire CD 20 (Borin) | round 1 del Giorno 1: −1 AU all'orda in tutti i settori | |
| 1B-2 · Sapienza Magica CD 22, *rune di potere* o un incantesimo di 3°+ consumato | +1 al bianco nel settore di chi lo lancia, round 1 del Giorno 1 | |
| 1C (drago) · la Presenza | morale **−1** | |
| 1C · Attaccare, con un colpo a segno | morale **+2** (netto +1); Fauci soffia sulla postazione | |
| 1C · Rispondere con magia (3°+, visibile) | morale **+1** (netto 0); l'incantesimo è speso per 1D | |
| 1C · Ignorare | resta il −1; chi lo ha proposto ha un Comandare gratis nel round 1 di 1D | |
| 1D · trappole portate a casa | ognuna annulla una tacca del **Giorno 1 o del Giorno 2**, nel settore scelto (D22) | §5.1 Difese preparate: 6+ «pieno», 3-5 «parziale», meno di 3 «fallito» |
| 1D · squadra travolta o a 0 PFU | morale **−1** ciascuna | |
| 1D · sergente fuggito | nessuna nell'assedio; il racconto lo ricorda | |
| 1E · Thorin, Dara, Nala | TS a +2 contro «La palla di fuoco»; niente Carica selvaggia nel round 1 del Giorno 1; +2 al primo attacco contro Gorthak | |

### Statblocchi mancanti

Fonti nell'ordine del DM. Le schede di *Red Hand of Doom* sono D&D 3.5 ma
**non SRD** (WotC): sono nel Bestiario come PCGen in
`Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/`. Vanno in fondo a 1A
e in `SEG` §2, in forma compatta.

**Goblin cavalcatore di worg** (×3, pattuglia di 1A-1) · *goblin worg raider*,
RHoD, non SRD · GS 5 · goblin guerriero 5°, Piccolo, LM · Iniz +4 ·
scurovisione 18 m · Ascoltare +1, Osservare +3, Nascondersi +9, Muoversi
Silenziosamente +9, Cavalcare +17 · CA 19, pf 42 · Temp +6, Rifl +5, Vol +1 ·
arco corto composito perfetto +12 (1d4, ×3), entro 9 m +13 (1d4+1);
scimitarra perfetta +7 (1d4, 18-20) · Tiro in Sella, Combattere in Sella,
Tiro Ravvicinato, Tiro Preciso, Arma Focalizzata (arco corto) · lingue
Comune, Draconico, Goblin.

**Worg** (×3) · scheda del Bestiario, avanzato a 6 DV (l'SRD dà 4 DV e 30 pf:
potenziamento) · GS 3 · bestia magica Media · Iniz +2 · scurovisione 18 m,
visione crepuscolare, **fiuto** · Ascoltare +7, Osservare +7, Nascondersi +4,
Muoversi Silenziosamente +7, Sopravvivenza +2 (+6 seguendo col fiuto) · CA
14, pf 51 · Temp +7, Rifl +7, Vol +4 · velocità 15 m · morso +9 (1d8+4) e
**sbilanciare** gratuito (+3) · Allerta, Attacco Naturale Migliorato (morso),
Robustezza Migliorata (non SRD).

Pattuglia intera: EL 9 circa.

**Hobgoblin regolare** (×9, postazione di 1A-2) · *hobgoblin regular*, RHoD,
non SRD · GS 2 · hobgoblin guerriero 3° (classe PNG) · Iniz +1 · scurovisione
18 m · Ascoltare +3, Osservare +2 · CA 19 (giaco di maglia perfetta, scudo
pesante +1), pf 23 · Temp +6, Rifl +3, Vol +1 · velocità 6 m · spada lunga
perfetta +6 (1d8+1, 19-20); arco lungo composito (+1) +4 (1d8+1, ×3) ·
mantello della resistenza +1, una pozione di cura ferite moderate.

**Il sergente** (1A-2 e 1D, lo stesso) · base *hobgoblin bladebearer*, RHoD,
non SRD, con l'armatura completa che `SEG` 44 gli dà · GS 6 · hobgoblin
guerriero 6° · Iniz +4 · scurovisione 18 m · CA **21** (armatura completa +8,
Des +1 dal tetto dell'armatura, anello di protezione +1, Difesa con Due Armi
+1), pf **50** · Temp +7, Rifl +6, Vol +5 · velocità 6 m · spada lunga +1
+11/+6 (1d8+6, 19-20), o con due spade +9/+4 (1d8+6) e +9/+4 (1d8+3) ·
Combattere con Due Armi, Combattere con Due Armi Migliorato, Difesa con Due
Armi, Arma Focalizzata e Specializzata (spada lunga), Volontà di Ferro,
*Oversized Two-Weapon Fighting* (non SRD) · nell'avanguardia: **+1** ad AU e
DU di tutti i reparti dal round 3 · **fugge a 25 pf**, come un comandante.
Da ricontare sul PCGen al momento di scriverlo: l'armatura completa cambia
Scalare, Saltare e Acrobazia.

**Fauci di Palude in 1C (ex 1F)** · non si ricopia: rimando a `01` 157-250.
Per la scena servono solo CA 29, pf 337, RD 10/magia, RI 21, volare 45 m
(scarsa), soffio in linea 30 m 14d4 acido (Riflessi CD 29), Presenza
terrificante 90 m Volontà CD 25 (potenziamento non SRD: 63 m nell'SRD), più
le regole di T6.

### Abilità e lingue dei pregen (T49)

Gradi al massimo SRD (livello + 3: 16 per Borin, 15 per gli altri),
caratteristiche dei blocchi di `01`. I valori di Ascoltare e Osservare già
scritti nei blocchi si tengono. Da confermare sui blocchi quando si
scrivono: `[INFERRED — da verificare in scrittura]`, non una scelta di gusto.

| Pregen | Caratteristiche da aggiungere | Abilità | Lingue |
|---|---|---|---|
| **Borin** (Gue 10 / Campione 3; Int 10 → 32 punti) | Int 10, Sag 10, Car 12 | Intimidire **+17**, Artigianato (pietra) **+12**, Ascoltare +2, Osservare +2, Scalare +5; Muoversi Silenziosamente e Nascondersi **−5** (penalità d'armatura −6) | Comune, Nanico |
| **Dara** (Ran 8 / Esploratrice 4; Int 12 → 105 punti) | (ci sono: Int 12, Sag 14, Car 10) | Osservare **+18** (+24 contro orchi), Ascoltare **+18**, Nascondersi **+24** (con il mantello elfico), Muoversi Silenziosamente **+19**, Sopravvivenza **+17**, Scalare **+18**, Conoscenze (natura) +16 · cannocchiale | Comune, Nanico |
| **Thorin** (Chi 9 / Sacerdote delle Rune 3; Int 12 → 45 punti) | (ci sono: Des 12, Int 12) | Concentrazione **+20**, Conoscenze (religione) **+16**, Sapienza Magica **+16**, Ascoltare +5, Osservare +5 | Comune, Nanico, Terran |
| **Nala** (Bar 8 / Spia Maestra 4; Int 14 → 120 punti) | (ci sono: For 14, Int 14, Sag 10) | Diplomazia **+23** (sinergie di Raggirare e Percepire Intenzioni), Raggirare **+21** (Persuasivo), Camuffare **+19** (+21 per recitare una parte), Nascondersi **+19**, Muoversi Silenziosamente **+19**, Ascoltare +15, Osservare +15, Percepire Intenzioni +15, Intimidire +8 | Comune, Nanico, **Orchesco, Goblin** |

Con questi numeri le CD della prima stesura sono quasi certe per chi ha
l'abilità giusta: per questo T5 alza di 5 le CD fisse o le rende
contrapposte, e T9 mette i gradini dell'Osservare a 20 / 25 / 30.

---

## Applicate (correzioni 1)

Il 2026-10-21, sui file che non sono la Sessione 1: `LIB`, `SEG`, `HO` e gli
script di `plans/esperimenti/battaglia-campale-2026-10-21/` (con il
README). Il conto delle abilità dei pregen sta in
[`ABILITA-PREGEN.md`](ABILITA-PREGEN.md).

**Fatte, intere**: T23, T24, T25 (in `LIB`, `SEG` e nello script), T26, T27,
T29, T30, T32, T33, T34, T35, T36, T37, T38, T39, T40, T41, T42, T43, T45,
T46, T47, T48, T49 (sulle schede di `HO`), T50, T51, T53, T54, T55, T60.

**Fatte in parte**, solo nei file di questo giro:

| Voce | Fatto | Resta, e dove |
|---|---|---|
| T4 | statblocchi di pattuglia, worg, scout e sergente in `SEG` §2 | il rimando in fondo a 1A e l'EL al posto di «5-12» in `01` |
| T9 | il cannocchiale sulla scheda di Dara | il box «Cosa vede Dara» in `01` |
| T14 | un solo momento per l'Handout 0 e le schede in `HO` | i tre riquadri in testa alla Sessione 1 |
| T15 | la carta di Dara: *passare senza tracce* non nasconde dal fiuto | le tre righe in 1A |
| T44 | le due regole in `LIB` §13, lo statblocco e la riga del sergente in `SEG` | `01` 1291 |
| T52 | la riga sui nomi in `HO` | i box di `01` |
| T56 | la carta di Thorin «due pagine» in `HO` | l'Handout 0 per un tavolo senza la campagna, rinviato |

**Lasciate**:

- **T28** e **T31**: aspettano il DM. Il §12 resta dov'è e com'è ordinato;
  dentro ha preso solo i numeri e le righe di altre voci (la tabella della
  ferocia, la carta dei giganti, la riga sui nomi degli script, il
  `[INFERRED]` di T55). La riga del §13 su quando si legge il libretto, e
  quella dell'handout 1-4, non sono cambiate.
- **T1-T3, T5-T8, T10-T13, T16-T22**: sono la Sessione 1 in `01`, che fa un
  altro giro dopo questo.
- **T57** (`ARC08-10`), **T58** (`ARC08-02`), **T59** (la mappa del pendio):
  fuori dai file di questo giro.

**Le prove rifatte** (3.000 battaglie, seme 1372, comandi nel README):

| Orda | Breccia contenuta «pieno», 3-6 trappole | Posizioni tenute «pieno» |
|---|---|---|
| normale | 95-98% | 87-88% |
| feroce | 78-89% | 57-60% |
| terrificante | 47-63% | 18-23% |

Tenere sempre, feroce, 4 trappole: breccia «pieno» 25%, posizioni 94%;
caricare sempre 14% e 0%. L'avanguardia non cambia (lo script ritirava già
tutto il gruppo): round 2 quattro trappole e nessuna squadra, round 3 5,07 e
0,25, round 4 5,01 e 0,89, round 6 2,23 e 2,93.

**Dove le correzioni si allontanano dal triage**:

- Borin ha Scalare −1, non +5: la tabella del triage non contava la penalità
  d'armatura.
- Dara ha Conoscenze (natura) +18 e Sopravvivenza +19 all'aperto: mancavano
  le sinergie. Prende Gigante come lingua bonus per Int 12.
- Nala ha Intrattenere 12 gradi, che il triage non aveva e la *suggestione*
  della musica chiede; per farci stare i punti, Nascondersi e Muoversi
  Silenziosamente scendono a +14. La Spia Maestra è letta a 8 + Int punti a
  livello, da verificare sul manuale.
- Thorin ha Ascoltare e Osservare +6, non il +5 dello statblocco: con Sag 22
  il conto è quello. Da allineare in `01` con T22.
- Il sergente fugge sotto metà dei pf, a 25: la voce T44 e la struttura
  dicevano la stessa cosa in due modi.


## Applicate (correzioni 3, 2026-10-21)

- T28 (DM: a pezzi): libretto §12 «Il tempo» con «Cosa si spiega quando», intestazione e §13 aggiornati; il master la scrive come definitiva.
- T31 (DM: nei Segreti): il vecchio §12 «Per il DM» è ora `ARC08-19` §4; nel libretto restano «Il tempo» e i rimandi senza numero di paragrafo; `ARC08-10` §5.4-bis punta ad `ARC08-19` §4.
- Fiuto dei worg: handout di Dara e `ARC08-19` allineati all'SRD (18 m se il vento porta l'odore, 4,5 m sottovento); tolta la nota di contraddizione dal master.
- Lettere degli incontri: `ARC08-16` (1F → 1C) e `ARC08-04` (1F → 1C) allineate al master.
