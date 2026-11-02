# Verifica · ARC-08, Sessione 1 coi pregen (2026-10-21)

Verificatore fresco, sul testo dei file e non sulle sezioni «Applicate» di
[`TRIAGE.md`](TRIAGE.md). Abbreviazioni dei file, tutti in
`08_La Battaglia Di Hammerfist/`:

| Sigla | File |
|---|---|
| `M` | `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md` (il master, 1570 righe) |
| `APP` | `APPARATO-ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md` |
| `LIB` | `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md` |
| `SEG` | `ARC08-19-SEGRETI-DELL-ORDA.md` |
| `HO` | `ARC08-15-HANDOUTS-GIOCATORE.md` |
| `L1` | `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md` |
| `01`, `02`, `10` | `ARC08-01-GUIDA-DM.md`, `ARC08-02-SCHEDE-…`, `ARC08-10-ESITI-…` (guardati solo per le voci che li nominano) |

## Riepilogo

| | |
|---|---|
| Voci T1-T60 | **58 chiuse**, **2 parziali** (T14, T28), **0 aperte**, 0 respinte |
| Nuovi rilievi | **0 🔴**, **5 🟠**, **27 🟡** |
| Statblocchi | tornano tutti coi conti SRD 3.5 (CA, attacchi, TS, pf), salvo il nome dell'armatura degli hobgoblin regolari (🟡 B.13) |
| Controlli automatici | `componenti.py --apparato`: l'apparato è identico a quello che il master genera oggi. `validate_modules`: nessun rilievo sul master. `validate_lingua`: nessun refuso. `validate_prosa`: un rilievo non bloccante (riga 434). `validate_maps`: nessun errore su `L1` |

**Verdetto: sì, giocabile stasera.** Le scene ci sono tutte, ognuna con la
sua uscita, i numeri fra master, libretto e segreti coincidono, e la mappa
del pendio esiste col suo SVG. Prima di sedersi servono quattro ritocchi,
una ventina di minuti in tutto:

1. in `HO` 78-79 togliere «che si legge a inizio serata» (B.1): è l'unico
   testo per i giocatori che contraddice il libretto spiegato a pezzi;
2. decidere se al Consiglio si mostrano la tabella «Chi tiene cosa» e i tre
   modi del libretto, o se la scelta del modo passa all'alba del Giorno 1 (B.3);
3. una riga su cosa succede quando il fiuto di un worg scatta (B.4);
4. non stampare, o barrare, le tabelle di regia di 1A-1, 1A-2 e 1A-3 in `L1`,
   che hanno ancora le regole vecchie (B.5).

Il resto sono 🟡 che il DM può aggiustare a voce.

---

## A. Le sessanta voci

Stato: **chiusa** (il testo fa quello che la voce chiede), **parziale**
(fatto in un file, contraddetto in un altro), **aperta**, **respinta a
ragione**. Righe dei file come sono oggi.

### §1 del triage · la Sessione 1 (oggi il master `M`)

| Voce | Stato | Dove la vedo, o perché no |
|---|---|---|
| T1 | chiusa | Scena 8 «1D · L'avanguardia» `M` 1040-1216; indice `M` 58; `01` 39-46 rimanda al master; la nota `01` 117-123 ha `[CANONE — DM 2026-10-21]` |
| T2 | chiusa | scheda da compilare `M` 1273-1296, tabella delle leve 1298-1329, morale da +1 a ±5 `M` 225-228; una sola famiglia di trappole `M` 928 e 1183-1186. Nel master non restano «iniziativa di massa», «CA alle mura», «CA delle fortificazioni» (grep). Il residuo in `L1` 637 è in B.5 |
| T3 | chiusa | le quattro decisioni come leve `M` 855-868; il Re e il Cancello 870-877; Dana e le Cantitrici 879-883; schede d'entrata 501-509 e 836-844 |
| T4 | chiusa | statblocchi `M` 1456-1466 (copia di `SEG` 76-135); EL 9 / 9 / 11 in `M` 200-202; «5-12» non c'è più |
| T5 | chiusa | quattro gradini `M` 798-805, ricerca della pattuglia e corpi 622-625; prove contrapposte `M` 170-176, 587-591. Scelta l'opzione «contrapposte», non «CD +5» (vedi B.9 sulla frase di 166-168) |
| T6 | chiusa | regole della scena `M` 991-1013 (quota 60 m, Presenza, baliste e RD, Dara +19, *colpo infuocato* 66 m, una risposta sola); tre opzioni con le leve 1015-1024 |
| T7 | chiusa | box `M` 828-834 coi quattro pregen; battuta di Dana senza pausa 848-849 |
| T8 | chiusa | due azioni, niente prendere 20, fallire di 5 spreca l'azione, aiutare `M` 920-923; prove su abilità vere 925-931; Thorin 933-938 |
| T9 | chiusa | nessuna penalità di distanza e cannocchiale `M` 720-721; box a gradini 20/25/30 `M` 727-755; nemico prescelto 723-725; cannocchiale sulla scheda `HO` 124-125 |
| T10 | chiusa | tre presagi sui pregen con leve `M` 1232-1243; Borin 1241-1243; via Warlock e «magia demoniaca» 1245-1249 |
| T11 | chiusa | ordine drago → avanguardia → presagi e lettere nuove `M` 254-267 e §6; `ARC08-16` 52-55 già con le lettere nuove. Restano due frasi del master che dicono il contrario (B.14) |
| T12 | chiusa | schede di Grimjaw, Gorthak e Fauci `M` 768-796 (CA 26 / 178 pf; CA 25 / 202 pf / fugge sotto 101); il +2 «nei primi 3 round del duello Sfidare» `M` 1311 |
| T13 | chiusa | «Chi si trova dove» `M` 316-331; nel cortile 903-912 |
| T14 | **parziale** | tre riquadri in testa `M` 30-42, 104-126, 128-146; `HO` 18-21 dà un solo momento per l'Handout 0. Ma `HO` 78-79 dice ancora che il libretto «si legge a inizio serata» (B.1) |
| T15 | chiusa | ora, fiuto, silenzio (e volo) `M` 547-565, fiuto come l'SRD (9 / 18 / 4,5 m); carta di Dara `HO` 207. Manca cosa succede quando il fiuto scatta (B.4) |
| T16 | chiusa | alba con polvere e fuochi, senza «oceano di ferro» `M` 466-479; Scena 3 col Re che manda i quattro 484-534 |
| T17 | chiusa | tabella dei tempi con cosa tagliare `M` 128-146; durate in testa a ogni scena. La somma non è quella dichiarata (B.10) |
| T18 | chiusa | box di chiusura `M` 1263-1269, scheda 1273-1296, ponte 1331-1332 |
| T19 | chiusa | nota ridotta, fra `<!-- storico -->` `M` 1030-1035 |
| T20 | chiusa | niente «6-8 righe», niente schizzi ASCII, niente «SUPPORT_MAGICO» né «Worg Riders» nel master (grep); Borin in copertura o sul fianco «come scelta» `M` 675-677 |
| T21 | chiusa | box dei presagi `M` 1224-1230 («si vedono appena», «punteggiano», via la chiusa); drago 983-989 («alto sopra le torri, e basso quanto basta», «Non ha bisogno di parlare»); nessun «si rivela essere» né «letteralmente» |
| T22 | chiusa | `01` 700 (Borin Int 10, Sag 10, Car 12), `01` 787 e 806 (Thorin Ascoltare e Osservare +6) |

### §2 · il libretto

| Voce | Stato | Dove |
|---|---|---|
| T23 | chiusa | `LIB` 252 |
| T24 | chiusa | trappole sul gruppo `LIB` 355-357; ritirata di gruppo 362-365; «Quanto restare» coi numeri del triage 405-412 |
| T25 | chiusa | `LIB` 214 e 400-401; `SEG` 165 e 192-193; `10` 282-284; script `assedio_v3.py` 144 (`giorno <= 2`); ferocia rifatta `SEG` 186-190 («8-9 volte su 10») |
| T26 | chiusa | tabella «vale / non vale» `LIB` 384-393; copia in `M` 1099-1108 |
| T27 | chiusa | `LIB` 245-262; `M` 412-420 |
| T28 | **parziale** | la decisione del DM (a pezzi) è in `LIB` 3-4 e 336 e in `M` 951-968, ma i due testi non dicono la stessa cosa e il master dice che la riga del libretto «non c'è» (B.2) |
| T29 | chiusa | regola in `LIB` 150-156; intestazione delle carte `HO` 178-184; carte allineate (`HO` 193, 209, 232, 240, 242, 267, 271) |
| T30 | chiusa | `LIB` 139-140 |
| T31 | chiusa | il vecchio §12 è `SEG` §4 (174-226); `LIB` §12 è «Il tempo» (330-336). Nessun rimando a «§12» per il materiale del DM nei cinque file (grep) |
| T32 | chiusa | `SEG` 27 e 205 (un macigno per settore) |
| T33 | chiusa | `LIB` 377-382; `HO` 284; `M` 1163-1167 |
| T34 | chiusa | `LIB` 109-114, coi numeri rifatti (una volta su quattro) |
| T35 | chiusa | foglio dei reparti `LIB` 418-448; tracciatore `SEG` 137-151 |
| T36 | chiusa | `LIB` 395-398; `M` 1194-1196 e 1212-1213; `SEG` 133-135 |
| T37 | chiusa | `LIB` 347 |
| T38 | chiusa | `LIB` 212 |
| T39 | chiusa | `LIB` 158-161 |
| T40 | chiusa | `LIB` 324-326 |
| T41 | chiusa | `SEG` 194-195 |
| T42 | chiusa | `LIB` 21, 211, 267-268, 349-350, 359-360, 280-282 |

### §3 · i segreti

| Voce | Stato | Dove |
|---|---|---|
| T43 | chiusa | mazzo per round `SEG` 47-52; «o a 0 PFU» `LIB` 366-368 |
| T44 | chiusa | Sfidare e retroguardia separati `LIB` 369-376; statblocco e «stesso sergente» `SEG` 66-95; in `M` 679-682, 689-698, 1153-1162 |
| T45 | chiusa | `SEG` 17-19; `LIB` 72 |
| T46 | chiusa | box del corno e cresta fuori tiro `SEG` 58-64; `M` 1141-1149 |
| T47 | chiusa | `SEG` 27 e 205; lo script toglie le merlature dal macigno (`assedio_v3.py` 95-98) |
| T48 | chiusa | `SEG` 25 |

### §4 · gli handout

| Voce | Stato | Dove |
|---|---|---|
| T49 | chiusa | righe Abilità e Lingue `HO` 102-105, 118-123, 137-141, 157-164; riga Spia Maestra `HO` 283; copia in `02` 631-720; tabella `M` 1476-1481 |
| T50 | chiusa | `HO` 50-52; `M` 1072-1073 e 1360-1362 |
| T51 | chiusa | `HO` 27-29 |
| T52 | chiusa | `HO` 67-69; `M` 100-102; nei box il Re è «il Re», Dana «la Madre Superiora», il pregen «Runaforte» |
| T53 | chiusa | componenti `HO` 142-143 e 165; *comunione* e PE `HO` 234; *guarigione* +1 PFU `HO` 227 e `LIB` 136 |
| T54 | chiusa | `HO` 267 |
| T55 | chiusa | via l'etichetta di stile e il Rubino (`HO` 25-36); l'unico `[INFERRED]` rimasto è nella nota DM (`HO` 63), come la voce consente |
| T56 | chiusa | la parte decisa (Thorin due facciate) in `HO` 82-85; l'Handout 0 per un tavolo senza la campagna è rinviato, come diceva la voce |

### §5 · gli altri file

| Voce | Stato | Dove |
|---|---|---|
| T57 | chiusa | `10` 236 («trappole di 1D e della Preparazione»), 269-288 (§5.4-bis senza `[INFERRED]`, rimanda alla tabella delle leve e a `ARC08-19` §4) |
| T58 | chiusa | `02` 631-720 (righe di T49); `02` 875-877 (il sergente dell'avanguardia non è quello di reparto) |
| T59 | chiusa | MAPPA 1D in `L1` 649-697 e in `M` 1513-1569, identiche; SVG `Mappe/rendered/Hammerfist-L1-REVISED-Ultra-Clear_map04_mappa-1d-il-pendio-sotto-le-mura.svg` presente. Le marche 1-5 cadono sui 🔵 e sul ⚫ della griglia. La cresta è a sud, non a nord come nel triage: è giusto, a nord ci sono le mura |
| T60 | chiusa | `assedio_v3.py` 144 (`giorno <= 2`), 95-98 (macigno per settore, senza merlature); `avanguardia.py` 23 (Borin con la Guardia, 11/22/12) |

---

## B. Seconda passata da DM a freddo

Letto come se lo conducessi stasera. Gli statblocchi li ho rifatti a mano
(B.13 in fondo ha i conti).

### 🟠

**B.1 · 🟠 · L'handout dice che il libretto si legge in apertura.**
`HO` 78-79: le schede si danno «insieme al libretto della battaglia campale
(`ARC08-18`), che si legge a inizio serata». Il master lo consegna dopo la
pausa (`M` 121-126, 1425-1426) e lo spiega a pezzi (`M` §5); il libretto
dice lo stesso (`LIB` 3-4, 336). È il solo testo che va ai giocatori a
contraddire la decisione del DM. Correzione: «…con la loro carta dei
poteri. Il libretto della battaglia campale si dà più tardi, prima della
battaglia.» Tiene aperta T14.

**B.2 · 🟠 · Il master e il libretto non dicono le stesse cose su «cosa si spiega quando».**
- `M` 958 spiega stasera §1, §2, §3, §4 con Scavare, §5, il morale «in una
  frase» (§6), §7 e §13; `LIB` 336 dice §1, §3, §4, Combattere e Comandare
  di §5, §7, e manda **§6 e §9 alla Sessione 2**.
- `M` 958 lo mette «dopo la pausa, prima del drago»; `LIB` 336 «prima della
  scaramuccia» e `LIB` 343 «subito prima».
- `M` 966-968: «Il libretto avrà la sua riga su cosa si spiega stasera…
  finché non c'è, vale questa tabella». La riga c'è (`LIB` 336).

Stasera il morale conta (il drago lo muove, le squadre travolte lo tolgono),
quindi ha ragione il master: §6 in una frase va spiegato. Correzione: `LIB`
336 prende la lista del master e «dopo la pausa, prima del drago»; `M`
966-968 si riduce a «La riga è in `LIB` §12». Tiene aperta T28.

**B.3 · 🟠 · Il Consiglio usa il libretto prima che i giocatori ce l'abbiano.**
La Scena 5 (`M` 861-868) fa scegliere a ogni giocatore il modo A, B o C del
libretto §9 e parte dalla tabella «Chi tiene cosa» del §1; la scheda lo
registra (`M` 1282). Ma il libretto arriva dopo la pausa (`M` 125), che è
dopo la Scena 6, e `LIB` 336 dice che §9 si spiega alla Sessione 2. Le tre
frasi di `M` 866-868 bastano per un DM, non per un giocatore che deve
scegliere. Due strade: al Consiglio si mostrano solo la tabella di `LIB`
38-45 e quella di `LIB` 235-239, letti dal DM; oppure la decisione 3 si
toglie dal Consiglio e il modo si sceglie all'alba del Giorno 1, quando lo
chiede già `LIB` 232 («Il gruppo sceglie il modo prima di ogni giorno»). La
seconda è più pulita e toglie un quarto d'ora di regole a metà serata.

**B.4 · 🟠 · Il fiuto dei worg scatta, e il testo non dice cosa succede.**
`M` 551-557 dice chi il worg sente, `M` 585 che senza la finestra «si passa
dentro il fiuto», `M` 606 che con l'invisibilità «resta il fiuto». Nessuna
riga dice l'esito: per l'SRD il fiuto rivela la presenza e la direzione, non
il quadretto. Il box di `M` 629-633 lo suggerisce («annusa l'aria due
volte»), ma il DM al tavolo deve decidere da solo se è «visti» o una prova.
Correzione, una riga dopo `M` 557: «Chi passa nel raggio del fiuto non è
visto, ma la pattuglia si ferma: il worg annusa (box), e per un round tutti
tirano Osservare e Ascoltare con +5. Chi è invisibile non è trovato, ma la
pattuglia resta lì un altro giro.» Il +5 è quello di `L1` 528.

**B.5 · 🟠 · Le tabelle di regia delle mappe 1A hanno ancora le regole vecchie.**
Il master manda il DM a stampare 1A-1, 1A-2 e 1A-3 da `L1` (`M` 116-117,
1503-1509), e quelle pagine dicono altro:
- `L1` 232-235 e 318: Osservare CD 25 «identifica Grimjaw, Gorthak, Drago»,
  CD 30 «layout tattico e punti deboli», «10 minuti di osservazione»; il
  master ha il drago al gradino 30 e cinque round (`M` 713-755);
- `L1` 304: +2 di circostanza all'Osservare dalla cima, che il master non dà;
- `L1` 316-326: Nascondersi **CD 20** fisso e sorpresa con CD 25, contro le
  prove contrapposte del master (`M` 170-176, 655-660);
- `L1` 528-529: «carica dei 3 worg; corno al round 2», contro `M` 614-618
  («i goblin non caricano», il capo suona se ha un round libero);
- `L1` 504: fiuto a 9 m senza il vento;
- `L1` 636-640: CD 15 / 20 / 25 / 30 con «**+2 Iniziativa di massa** dei
  nani» e Sopravvivenza CD 22: è l'unità che T2 ha tolto.

Correzione minima per stasera: in testa alle sezioni ⚔️ TATTICHE ed
EVOLUZIONE di 1A-1 e 1A-2 e al blocco «INTELLIGENCE A SOGLIE» di 1A-3 una
riga «Le prove e gli esiti sono nel master, Scena 4: questa tabella è
superata». Correzione vera: le tre tabelle riscritte coi numeri del master.

### 🟡

**Contraddizioni fra i file**

- **B.6** · Il sergente che fugge: `SEG` 69-70 «fugge, come un comandante»;
  `LIB` 146 e 178 danno +2 al morale quando un comandante fugge; `M`
  1156-1157 dice che la fuga del sergente il +2 non lo dà. Una riga in
  `LIB` §13 («la sua fuga non muove il morale») chiude il dubbio, che il
  giocatore legge sul libretto e non sul master.
- **B.7** · Il morale sul pendio: `LIB` 389 «più quello che la serata ha già
  portato (il consiglio, il drago)»; per il master il Consiglio non porta
  morale e la Diplomazia di Nala vale dall'alba del Giorno 1 (`M` 225-228,
  1104). In `LIB` 389: «(il drago)».
- **B.8** · `M` 605: «*Invisibilità* (Nala ne ha una, più tre pozioni)». Nala
  è barda, lancia spontanea, quattro incantesimi di 2° al giorno (`HO`
  262), quindi fino a quattro *invisibilità*; le tre pozioni non sono sulla
  sua scheda. O le pozioni vanno in `HO` 165, o la riga dice «Nala può
  renderne invisibili fino a quattro, uno per incantesimo».
- **B.9** · `M` 166-168: «alzate di 5 dove la CD è fissa». Restano alle CD
  base Sopravvivenza 15 (`M` 172, 555, 581), Scalare 12, Ascoltare 15 per
  Nala, i presagi a 15 e 18. Per Dara (+19 all'aperto) la Sopravvivenza 15 è
  certa. O si alza, o la frase dice «contrapposte dove qualcuno guarda; le
  CD fisse restano quelle del manuale».
- **B.10** · La durata: le righe di `M` 130-143 sommano **3 h 10 – 3 h 55**,
  e **4 h 10** col duello del sergente; `M` 145 dice 3 h 15 – 3 h 50. La 1A
  a 45-60' con tre fasi, tre mappe e un possibile scontro è la stima più
  ottimista della serata: se sfora, il taglio scritto (`M` 135) va usato
  subito, non alla fine.
- **B.11** · `M` 1343 (Contingenze): se gli scout suonano il corno il
  gradino è «visti ma via». Ma per `M` 805, se il corno suona prima che Dara
  arrivi in cima, è «allarme e niente vista», con +50 rinforzi nel finale.
  La riga di 1343 va completata: «se suona prima che Dara abbia contato,
  allarme».
- **B.12** · Due «+2 contro Gorthak» (prigioniero `M` 1311, Nala ai presagi
  `M` 1329): non si dice se si sommano. Proposta: sì, uno sui primi tre
  round, l'altro sul primo attacco.
- **B.14** · `M` 256-258 e 1442 dicono che `ARC08-16` e `ARC08-04` usano le
  lettere vecchie; `ARC08-16` 52-55 ha già 1C per il drago. Le due frasi si
  tolgono, la tabella di §0-ter resta come storia.

**Statblocchi e regole SRD**

- **B.13** · Conti rifatti, tutti tornano:
  - goblin cavalcatore: CA 19 = 10 +1 taglia +4 Des +4 armatura (contatto 15,
    sprovvista 15); arco +12 = BAB 5 +1 taglia +4 Des +1 perfetto +1 Arma
    Focalizzata; TS +6/+5/+1; cinque talenti per un guerriero 5°; 42 pf col
    massimo al primo DV;
  - worg 6 DV: morso +9 = BAB 6 + For 3, 1d8+4 (Attacco Naturale Migliorato,
    1,5 × For); TS +7/+7/+4 (buono, buono, scarso a 6 DV); 51 pf = 6d10 +12
    Cos +6 Robustezza Migliorata; tre talenti;
  - hobgoblin regolare: CA 19, contatto 11, sprovvista 18; spada +6, arco +4;
    TS +6/+3/+1 con Sag 9 e mantello +1; 23 pf. **Ma** l'armatura non è un
    «giaco di maglia» (*chain shirt*, +4, leggera): il PCGen
    (`Bestiario/pregen-pcgen/…/hobgoblin regular 3 liv.htm` 149) dice
    *Masterwork Chainmail*, la **cotta di maglia** (+5, media). Solo con la
    cotta tornano CA 19 e velocità 6 m. Da correggere in `M` 705 e 1462 e in
    `SEG` 127;
  - sergente: CA 21 = 10 +8 +1 Des (tetto) +1 deviazione +1 Difesa con Due
    Armi, contatto 12 (lo scudo non vale al contatto), sprovvista 20; spada
    +11/+6 (1d8+6); con due spade −2/−2 grazie a *Oversized Two-Weapon
    Fighting*: +9/+4 e +9/+4 (1d8+3); TS +7/+6/+5; 50 pf; sette talenti per
    un guerriero 6°; Combattere con Due Armi Migliorato chiede Des 17, ha 18.
    Tutto coincide col PCGen;
  - Fauci: CA 29 (−2 taglia, +21 naturale), 337 pf (25d12+175), soffio CD 29
    (10 + 12 + Cos 7), Presenza CD 25 (10 + 12 + Car 3);
  - pregen: CA 25 / 21 / 22 / 20 tornano dalle voci delle schede; Borin +21
    (BAB 13 + For 5 + 2 + 1), Dara +19 e i suoi nemici prescelti in `HO` 203
    (il +2 contro i draghi che `M` 1001-1002 usa c'è).
- **B.15** · *Potere della giustizia* di Thorin (`HO` 232) ha i numeri di
  Pathfinder (+4 For, +12 pf), con la RD 6/male del 3.5. Nell'SRD 3.5 è +8
  For e +4 Cos: martello **+17**, danni **2d6+9**, **+24 pf**, e Combattere
  +17 nel round in cui lo lancia. Stasera non pesa, alla Sessione 2 sì.
- **B.16** · *Frantumare* di Nala (`HO` 277) «fino a 54 m»: nell'SRD è a
  distanza vicina, **13,5 m** al 8° livello.
- **B.17** · *Affascinare* (`HO` 269; `LIB` 382; `M` 1167): «TS Volontà CD
  18». Nell'SRD 3.5 la CD è il risultato della prova di Intrattenere di
  Nala (d20 + 16, in media 26). Con la CD fissa l'inganno riesce «due su
  tre»; con l'SRD quasi sempre. Va bene la semplificazione, ma va detta sulla
  carta («CD 18 nella battaglia campale»).
- **B.18** · Scacciare non morti di Thorin «prova 1d20+8» (`HO` 257): con Car
  16 e la sinergia di Conoscenze (religione) il conto SRD fa +5. Da
  verificare sul blocco di `01`; stasera non serve.
- **B.19** · *Presenza Comandante* di Borin (`HO` 194: +2 ai TS degli alleati
  entro 9 m) non entra nella Presenza terrificante del drago (`M` 994-998).
  Chi sta accanto a Borin sulle mura tira con +2.
- **B.20** · `M` 997-998 e 1468: «l'SRD dà 63 m all'adulto maturo». Fauci è un
  adulto avanzato (`01` 159): l'SRD per l'adulto dà 54 m (9 m per categoria
  d'età, categoria 6). Il potenziamento resta, cambia la nota.
- **B.21** · EL della pattuglia: tre GS 5 fanno EL 8, i tre worg GS 2 non lo
  alzano di un punto intero. «EL 9 circa» (`M` 200, 620, 1460) è generoso;
  scout EL 9 torna, i due insieme sono EL 10-11. Per pregen di 12°-13° non
  cambia niente, ma il dato è quello.
- **B.22** · Intimidire **CD 23** fisso per il prigioniero (`M` 684): nell'SRD
  3.5 è contrapposto (d20 + DV + Sag + bonus contro la paura; un hobgoblin
  tira in media 12, il sergente 17). La CD fissa è più dura dell'SRD: va
  bene, ma è una scelta, e va marcata come tale.

**Scene senza un'uscita scritta**

- **B.23** · Scena 8: manca l'esito «tutte le squadre travolte prima della
  ritirata» (la scena finisce lì: zero trappole dal pendio, resta quella
  della Preparazione) e «il sergente muore nel duello» (sulla mappa, con le
  regole normali, un critico di Borin con *Colpo devastante* lo porta da 30 a
  sotto zero: vale come la fuga, e non si interroga). Due righe sotto `M`
  1159.
- **B.24** · Il turno della ritirata è ambiguo: «alla fine di ogni round si
  decide insieme» (`M` 1088-1090, `LIB` 362-365) e «nel round in cui il
  gruppo si ritira, un eroe resta indietro» (`M` 1160-1162, `LIB` 374-376).
  Si gioca un round di ritirata dopo la decisione, o la decisione chiude la
  scena? La lettura che regge la retroguardia è la prima: lo si scriva.
- **B.25** · Round 1 con «visti ma via» (`M` 1118): due reparti di lupi su
  una squadra sola. Lo Sbilanciare (`SEG` 26, −2 al bianco) vale una volta o
  due? Proposta: una volta, come «Due uguali non si sommano».
- **B.26** · Il gradino 30 di Dara (il drago sulla palude, `M` 749-755) non
  ha leva nella tabella (`M` 1305-1312), ma la contingenza di `M` 1342 lo
  offre come premio a chi scende al campo. O una leva («il Giorno 3 il
  soffio è annunciato: un round prima, i reparti delle Mura possono
  Tenere»), o la contingenza dice «vale il gradino 25».
- **B.27** · La seconda azione della Preparazione è «la mattina del Giorno −1»
  (`M` 892), cioè dopo il drago, che si gioca all'alba nella Scena 7. Al
  tavolo si gioca prima. Se qualcuno spende un incantesimo di 3° per
  l'opzione B la mattina del −1, non ce l'ha per «Rispondere con la magia»
  all'alba? Più semplice: le due azioni sono il Giorno −2, mattina e
  pomeriggio.

**Read-aloud**

- **B.28** · `M` 429 (e `HO` 30): «Per quei giorni si guarda da altri occhi»
  suona tradotto. «Quei giorni li vedrete con gli occhi di altri.»
- **B.29** · `M` 727-728: «e non è un modo di dire» è un calco dell'inglese
  (*and that's not a figure of speech*). Basta togliere la frase.
- **B.30** · `M` 730 «Orchi e hobgoblin, a migliaia» e `M` 1228 «migliaia di
  torce», mentre il conto è novecento (`M` 736). Sotto il gradino 20 può
  essere l'impressione di chi non sa contare, e allora va detto: «sembrano
  migliaia». Le torce si correggono in «centinaia». Anche `M` 1342 «ha
  novecento occhi» (novecento creature ne hanno il doppio): «novecento paia
  d'occhi».
- **B.31** · `M` 1054 «Le mura sono alle spalle, alte, e da quaggiù lontane»,
  contro la MAPPA 1D dove la cinta è a 5-15 m dalle squadre (righe 01-08). E
  `M` 1145 / `SEG` 60 «Lassù, contro il cielo» con la cresta a sud, in fondo
  a un pendio che scende verso sud (`M` 1531, 1546; `L1` 657-659). Se la
  cresta è dall'altra parte della valle, più alta del pendio, una parola nel
  box lo dice («sulla cresta di fronte»); se no, «laggiù».
- **B.32** · Cosmetici: `M` 547 «Tre cose da sapere» sopra quattro punti; le
  righe 728, 735, 742 e 751 del master vanno a capo dopo un rigo lunghissimo
  (in stampa non si vede, nel sorgente sì); `M` 984 «si alza in volo per la
  prima volta» si legge come se prima non volasse: «si mostra per la prima
  volta». `validate_prosa` segnala «Le loro mani» (`M` 434): qui il
  possessivo è voluto (contrappone le mani dei quattro alle vostre), si
  tiene.

**Da sapere, non da correggere stasera**

- Restano otto `[INFERRED]` nel master (`M` 717, 876, 1009, 1208, 1307, 1379,
  1489, 1560): tutti dichiarati e con un valore di ripiego. Nessuno blocca
  la serata.
- Il tesoro (`M` 1405-1407) non conta le nove cotte di maglia perfette, gli
  scudi pesanti +1, le spade perfette degli scout e la spada perfetta del
  sergente: i pregen escono di scena alla Sessione 3, ma se qualcuno chiede
  «cosa c'è sui corpi» la lista è corta.
- L'apparato (`APP`) è allineato al master: rigenerato oggi, coincide riga
  per riga.

---

## Seconda passata applicata (2026-10-21)

Applicata sui sei file della verifica (`M`, `APP` rigenerato, `LIB`, `SEG`,
`HO`, `L1`), con le scelte del coordinatore: modo di gioco e «Chi tiene
cosa» all'alba del Giorno 1; il libretto §12 è la fonte di «cosa si spiega
quando»; numeri SRD 3.5 per gli incantesimi; Nala senza pozioni, perché la
sua scheda in `Bestiario/png/` non le ha.

| Voce | Cosa ho fatto |
|---|---|
| T14 | chiusa con B.1 |
| T28 | chiusa con B.2 |
| B.1 | `HO`, Handout 1-4: le schede si danno con la carta dei poteri, il libretto «più tardi, prima della battaglia». L'Handout 0 ha una riga nuova con i pezzi del libretto |
| B.2 | `LIB` §12 resta la fonte, con due aggiunte: il momento («dopo il drago e prima della scaramuccia») e le regole del pendio del §13; il morale non si spiega, il DM dice quanto vale sui dadi. `M` §5, `M` §0 (preparare, consegne, tempi), `M` §11 e `HO` 0 elencano gli stessi paragrafi. La frase «il libretto avrà la sua riga» è diventata «fa fede il libretto §12». Il pezzo del libretto è passato fra la Scena 7 e la Scena 8; la pausa resta dopo la Scena 6 |
| B.3 | Consiglio: tolta la decisione «Strategie di resistenza»; la decisione 3 è ora «Il Re e il Cancello» (Diplomazia CD 18 o una ragione), con la sua riga nella tabella delle leve. La decisione 1 non usa più la tabella del libretto, e i due reparti si scambiano all'alba del Giorno 1. Tolta la riga «modo di ogni giocatore» dalla scheda. `LIB` §1 dice che «Chi tiene cosa» si guarda all'alba del Giorno 1. Consiglio a 20' |
| B.4 | `M` Scena 4, «Il fiuto dei worg»: cosa succede quando scatta (la pattuglia si ferma, +5 per un round, l'invisibile non è trovato ma la pattuglia resta un giro), segnato come scelta del modulo. Lo stesso in `L1` 1A-1 |
| B.5 | correzione vera, non barrata: in `L1` riscritte SEQUENZA TATTICA, DISTANZE (via il +2 d'altezza), AMBIENTE, TATTICHE ed EVOLUZIONE di 1A-2; PROVE FURTIVE (era la sfida a successi), DISTANZE (fiuto SRD), luce, TATTICHE ed EVOLUZIONE di 1A-1; «Quando si usa» e INTELLIGENCE A SOGLIE di 1A-3 (via l'Iniziativa di massa e la Sopravvivenza CD 22). Ogni sezione ha in testa il rimando al master. Le griglie non cambiano: gli SVG rigenerati sono identici |
| B.6 | `LIB` §13 e `SEG` §2: la fuga del sergente, e la sua morte, non muovono il morale |
| B.7 | `LIB` §13, «vale / non vale»: «(il drago)» |
| B.8 | `M` Scena 4 e App. A.6: *invisibilità* a tocco, una per incantesimo di 2°, fino a quattro al giorno; niente pozioni. `HO`, carta di Nala, lo dice. Lo statblocco di `ARC08-01` elenca ancora tre pozioni: file fuori da questo giro |
| B.9 | `M` §0-bis: le CD fisse di natura e fatica restano quelle del manuale, quelle sociali e di mestiere sono alzate |
| B.10 | `M` §0: totale 3 h 05 – 3 h 50, 4 h 05 col duello; se la 1A sfora a fine Fase 2, il taglio si usa subito |
| B.11 | `M` §3, «Come finisce», e §8: il corno dopo il conto di Dara è «visti ma via», prima è «allarme, e niente vista» |
| B.12 | `M` §7: i due +2 contro Gorthak si sommano (primi tre round; primo attacco a +4) |
| B.13 | cotta di maglia perfetta in `M` (comparse, A.3) e `SEG`; il sergente ha l'armatura completa «al posto della corazza di piastre +1», come nella scheda del Bestiario |
| B.14 | `M` §0-ter e §11: tolte le due frasi sulle lettere vecchie di `ARC08-16` e `ARC08-04`; la tabella resta come storia |
| B.15 | **respinta a ragione**: nel *Player's Handbook* 3.5 (p. 273, testo SRD) *potere della giustizia* dà +4 For, +2 Cos, +2 armatura naturale e RD 6/male al 12°. La carta di Thorin (+15, 2d6+7, +12 pf, CA 23) torna; il +8/+4 della verifica è il 3.0 |
| B.16 | `HO`: *frantumare* a 13,5 m (vicino, LI 8) |
| B.17 | `HO`, `LIB` §13 e `M` Scena 8: CD 18 di *affascinare* dichiarata come semplificazione della battaglia campale; nell'SRD è la prova di Intrattenere |
| B.18 | `HO`: Scacciare 1d20+5 (Car +3, sinergia +2), come lo statblocco di `ARC08-01` |
| B.19 | `M` Scena 7 e §0-bis: +2 alla Volontà contro la Presenza per chi sta entro 9 m da Borin |
| B.20 | `M` Scena 7 e A.5: l'SRD dà 54 m all'adulto |
| B.21 | EL 8 la pattuglia, 9 circa gli scout, 10 circa insieme, in `M`, `SEG` e `L1` |
| B.22 | `M` Scena 4 e §0-bis: Intimidire CD 23 segnato come scelta del modulo, con il conto SRD accanto |
| B.23 | `M` Scena 8: due esiti nuovi, il sergente morto nel duello (vale come la fuga, non si interroga) e tutte le squadre travolte (zero trappole dal pendio, resta quella della Preparazione); la scheda ha «sergente fuggito o morto» |
| B.24 | `M` e `LIB` §13: la decisione di correre apre il round della ritirata (nessuno scava, l'orda tira i bianchi, poi la scena finisce); la retroguardia vale in quel round |
| B.25 | `M` round 1 e `SEG` §1: lo Sbilanciare vale una volta sola anche con due reparti di lupi |
| B.26 | `M` §8: chi scende al campo torna col box del gradino 30, senza leva; il gradino di Dara resta il suo, la ricognizione finisce «visti ma via» |
| B.27 | `M` Scena 6: le due azioni sono la mattina e il pomeriggio del Giorno −2; gli incantesimi tornano prima del drago |
| B.28 | `M` e `HO`: «Quei giorni li ha visti qualcun altro» (la proposta «li vedrete» faceva scattare il P1 del box) |
| B.29 | tolto «e non è un modo di dire» |
| B.30 | «Orchi e hobgoblin, e il fumo di cento fuochi» (il «più di quanti sappiate contare» resta); «centinaia di torce»; «novecento paia d'occhi» |
| B.31 | pendio: «così vicine che l'ombra della cinta arriva fino alla prima fossa»; corno in `M` e `SEG`: «Laggiù, in piedi sulla cresta… guarda verso le mura» |
| B.32 | «Quattro cose da sapere»; i quattro box della Fase 3 riportati a capo; «si mostra per la prima volta». «Le loro mani» si tiene, come diceva la verifica |
| Da sapere | tesoro: aggiunte le cotte, gli scudi +1, le spade e gli archi degli scout e la spada perfetta del sergente. Gli otto `[INFERRED]` restano |

Misure: `validate_modules` 0 errori; `copertura_scene --file` 0 rilievi;
`ciclo_prosa confronta --rif HEAD` 0 box impoveriti sui quattro file (i ✗
sono i numeri cambiati di proposito); `misura_craft --box` invariato per
ARC-08 (104 box, nessuno sopra le 12 righe); `validate_maps` tutto
allineato; `componenti --check` allineato; `gate_locale --rapido` 50 passi, 0
rossi, 2 avvisi (typst assente in locale: corredo e schede in PDF non
compilati). `memoria.py` rigenerata per la riga nuova del CHANGELOG.
