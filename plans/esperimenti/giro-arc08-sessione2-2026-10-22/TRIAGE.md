# Triage · ARC-08, Sessione 2 coi pregen (giro del 2026-10-22)

Il master è `08_La Battaglia Di Hammerfist/ARC08-DEF-2-TRE-GIORNI-DI-SANGUE.md`.
Le fonti sono i quattro rapporti di questa cartella:

| Rapporto | Rilievi | Sigla | 🔴 | 🟠 | 🟡 |
|---|---:|---|---:|---:|---:|
| [`PLAYTESTER.md`](PLAYTESTER.md) | 49 | **P#n** | 0 | 16 | 33 |
| [`LETTORE.md`](LETTORE.md) | 59 | **L#n** | 1 | 19 | 39 |
| [`DEVELOPER.md`](DEVELOPER.md) | 43 | **D-Rn**, più le domande **D-An** | 0 | 18 | 25 |
| [`DM.md`](DM.md) | 26 | **DM-Rn / DM-Vn** | 0 | 10 | 16 |
| **In tutto** | **177** | | **1** | **63** | **113** |

I lettori sono quattro `claude -p` nuovi, lanciati uno dopo l'altro sulla
copia a freddo in `freddo/` (il master senza i blocchi `storico` e
`apparato`, più libretto, segreti, handout e le rubriche). Il registro
`plans/letture-a-freddo.json` non ha voci per ARC-08, quindi questo giro non
vi si registra (il giro della Sessione 1 non lo faceva).

I 177 rilievi sono raccolti qui in **41 voci** (T1-T41) più **5 respinte** (R1-R5). Ogni voce ha un esito:

- **corretta**: il master (o l'handout) è cambiato;
- **già decisa**: Jfs l'aveva già decisa, oppure è una scelta `[INFERRED]`
  che era già nell'elenco delle domande per il DM;
- **domanda per il DM**: è nuova, ed è entrata nell'elenco delle domande in
  testa al master (numeri 13-18);
- **respinta**: la voce non regge, e accanto c'è la fonte che lo dice.

## Riepilogo

| Esito | Voci |
|---|---:|
| corretta | **40** (T1 è anche già decisa: domanda 3) |
| già decisa, senza correzione | **1** (T31, le baliste: domanda 2) |
| corretta, con una domanda nuova per il DM | **6** dentro le 40 (T3, T4, T9, T19, T38, T39: domande 13-18) |
| respinta | **5** (R1-R5, 9 rilievi) |
| rimasta fuori dal master | **2** (D-R40 sulla carta di Thorin, l'Handout 7) |

Dei 64 rilievi 🔴/🟠 ne restano aperti due, ed entrambi come limite dichiarato:
T18 (Thorin ha molti compiti, ed è il suo personaggio) e T26 (la vista di
chi scorre non estrae l'avversario).

Due decisioni di Jfs del 2026-10-22, arrivate durante il giro, valgono qui
come «già decise» e sono nel master come `[CANONE — DM 2026-10-22]`:

1. **Domanda 1.** Il Giorno 3 resta nella Sessione 2: l'uscita A è il
   default, B e C sono di riserva (§0, «Il punto di taglio», nell'elenco
   delle domande e nell'apparato).
2. **Domanda 3.** Il Re arriva al Cuore a 8 pf fissi, per l'acido rimasto
   nell'armatura corrosa (Scena 6). Il master ha adesso una procedura che si
   esegue, «Il conto del Re» (T1).

## Le voci

### 🔴 e 🟠: la scena centrale e la ritirata

| Voce | Rilievi | Cosa | Esito |
|---|---|---|---|
| **T1** 🔴 | L#1, P#35, P#36, P#37, D-R17, D-R22, D-A2, DM-R1, L#36, L#38 | Il Re a 8 pf non aveva una procedura: le cure lo «tenevano vivo e non in piedi», la *protezione dall'energia* faceva e non faceva l'acido, togliergli l'armatura non aveva risposta | **già decisa** (domanda 3) e **corretta**. Scena 6, «Il conto del Re», in sei passi: soffio, lancia, acido 2d6 a round dal round 6 finché porta l'armatura, le cure lo tengono sopra 0, l'armatura si slaccia nel tunnel (1d4+1 minuti), poi 8 pf fissi fino al Cuore; CA 13 sulla barella, −4 da prono. La *protezione dall'energia* è ridefinita: assorbe 120 in tutto e compra tempo, non cambia l'arrivo |
| **T2** 🟠 | P#34, L#2, D-R20, D-R10 | Fauci a terra non aveva attacchi in mischia | **corretta**: morso, artigli, ali e coda (da `ARC08-02`) in §0-bis, nelle Tattiche e in A.5 |
| **T3** 🟠 | P#41, P#42, P#47, L#12, L#13, L#16, D-R25, D-R26, DM-R3, DM-R13, P#43, L#17, D-R27 | La ritirata (Scena 7) non aveva un motore: chi tira, cosa costa una via vuota, quando arriva l'orda, perché gli orchi passano nella Scena 8 | **corretta**: round di 6 secondi, 18 round contati dall'apertura, l'orda dalle scale della scarpa dal round 2 e dalla Porta Interna dal round 4 (la Porta Interna regge fino al round 4, non mezz'ora); «Come si tiene una via», con d20 + Combattere contro CD 28/30/32, e la via vuota che costa 1d4 nani a round; i 30 orchi della Scena 8 passano solo se il chokepoint della fase 3 resta vuoto. Il tiro è nuovo, ed è la domanda 13 |
| **T4** 🟠 | P#7, P#24, D-R1, D-R2, P#15, L#25, D-A1 | I duelli uccidono il pregen da solo, e tre giocatori stanno fermi | **corretta**: il DM avvisa prima (Borin da solo cade circa una volta su due); i round di battaglia si tirano prima del duello e gli altri giocatori muovono i troll; Sfidare va dal round 3 al 5. Chi si unisce lasciando il settore: domanda 14 |
| **T5** 🟠 | P#16, P#17, D-R18, P#18, D-R9 | *Dissolvi magie* sulle protezioni di Fauci; *scudo* che «dura la giornata»; Borin e Nala senza niente al sorvolo | **corretta**: *armatura magica* all'alba e *scudo* (7 minuti) a ogni passaggio; *dissolvi magie* per Thorin e Nala con la CD 18; Nala con ispirare coraggio o l'immagine; Borin con la Presenza |
| **T6** 🟠 | P#32, D-R16, DM-R15, L#37 | La spinta di Borin era una Forza CD 25 | **corretta**: spinta contrapposta (+5/+7 contro il +9 del Re), servono 10 di scarto, circa una volta su dieci |
| **T7** 🟠 | P#33, D-R19, DM-R14, L#55 | Soffio e carica nello stesso round; il cavaliere come bersaglio; il box del corno contro la tabella | **corretta**: sequenza a cinque round, il soffio al round 4 e la picchiata con la lancia al round 5; il cavaliere ha CA 23 e 95 pf, e se cade dalla sella la picchiata non c'è; box del corno riallineato |
| **T8** 🟠 | P#44, P#45, D-R29, D-R30, L#15, D-R34, L#14 | L'imboscata: Osservare a CD fissa, a che distanza, cosa fa l'avviso, scurovisione, Borin dal lato sbagliato | **corretta**: Osservare contro il Nascondersi dei bugbear (d20 + 17), −1 ogni 3 m; l'avviso toglie la sorpresa e quindi l'attacco mortale; i bugbear si nascondono dietro gli spigoli, perché la scurovisione li vedrebbe; Borin proposto in S19, fra il Re e la bocca est |
| **T9** 🟠 | D-R31, D-A4 | Un pregen paralizzato senza via d'uscita | **corretta** (la via d'uscita: *libertà di movimento*, 1d6+2 round, il colpo di grazia del bugbear come minaccia). Se i bugbear uccidono anche i pregen: domanda 15 |
| **T10** 🟠 | D-R33 | *Invisibilità* sul Re risolve la scena | **corretta**: il fiuto dei bugbear lo trova a 9 m; gli resta il 50% di occultamento |
| **T11** 🟠 | L#3 | «Il Cuore della Montagna» non era mai spiegato | **corretta**: un paragrafo nel §0 |
| **T12** 🟠 | L#4, D-R38, DM-R4 | Tre mazzi per quattro settori, nessun modo di costruirli | **corretta**: quattro mazzi di quattordici carte, fatti con due mazzi di carte da gioco, e la regola del mazzo finito |
| **T13** 🟠 | L#5, D-R4, D-R12, DM-R10, L#28, P#10 | L'ariete non sfonda in sette round; i pf del cancello in quattro versioni | **corretta**: 36,5 di media, 16,5 netti, circa dodici round; un solo conto: 200 → 120 → 140 all'alba (+20 la notte) → 60 → 80 all'alba del Giorno 3; scheda §7 «a sera» |
| **T14** 🟠 | L#6, D-R6, DM-R11, P#14, L#7 | I giganti senza CA; il master contro il libretto su Dara e i giganti | **corretta**: giganti delle colline CA 20, 102 pf in §0-bis; Dara contro i giganti è un'eccezione dichiarata al libretto, con −2/−6 di distanza |
| **T15** 🟠 | L#8, P#4, L#42 | «Il bianco sale di uno» contato due volte; il +1 delle Mura il Giorno 3 | **corretta**: è lo stesso +1; il Giorno 3 le Mura lo tengono se non hanno mai ceduto |
| **T16** 🟠 | L#9, L#19, P#25, D-R14, DM-R6, L#10, D-R8 | Dove si combatte Grimjaw, Gorthak e Grimjaw il Giorno 2 e 3 | **corretta**: ordine dei criteri per il settore; il box letto con «la scala» fuori dal Muro Est; Gorthak torna se ha più di 101 pf; il Giorno 3 Grimjaw entra al round 1 nel settore non sfidato |
| **T17** 🟠 | L#18, L#44 | Il Re sulla barella non aveva comportamento; il tragitto dal cancello alla statua non era finito | **corretta**: cosciente, l'acido, l'armatura nel tunnel; il tragitto (scala di G1, 45 m, la scarpa, il cortile interno) vale circa 10 round di griglia |
| **T18** 🟠 | L#20 | Thorin con troppi compiti per round | **corretta** in parte: le sue opzioni del soffio e della Scena 8 dicono ognuna che cosa costa (il canto o l'azione del round). Il carico resta, ed è il personaggio |
| **T19** 🟠 | P#8, P#9, D-R7, P#19 | Il ponte levatoio, la *barriera di lame* sul ponte, il fossato | **corretta**: l'argano, 80 pf e durezza 5, chi cade nel fossato; la barriera segue l'SRD (12d6, Riflessi CD 22, i troll rigenerano); Nuotare con la penalità d'armatura doppia, l'annegamento, la corda. Il ponte che si rompe è «scelta del modulo»: domanda 18 |
| **T20** 🟠 | P#21, D-R43 | Sabotare la rampa di notte, la sortita invisibile | **corretta**: la contingenza della rampa nella Scena 3 c'era; il §8 ora la richiama per la sortita invisibile |
| **T21** 🟠 | P#28 | Aprire il tunnel prima, mandare un esploratore | **corretta**: riga nuova nel §8 (il Re non lo vuole aprire; Dara trova le tracce con Sopravvivenza CD 20, e vale come la divinazione) |
| **T22** 🟠 | DM-R2 | Il soffio a cono senza box ai round 2 e 3 | **corretta**: due box nuovi, il drago che cerca e il respiro |
| **T23** 🟠 | DM-R5, L#21, D-R39, P#49 | Le domande dell'apparato lasciate nel testo come «domanda N» | **corretta**: ogni `[INFERRED — domanda N]` porta adesso il nome della scelta (le baliste, Gorthak sotto metà…); la scelta di default è scritta dove serve |
| **T24** 🟠 | DM-R7, DM-R17 | Il percorso breve salta le scene che chiedono più invenzione; la scheda della Sessione 1 data per scontata | **corretta**: «Con poco tempo per leggere» comprende le Scene 1, 4 e 7; se la scheda manca, morale +1 e nessuna leva |
| **T25** 🟠 | DM-V1, DM-R22 | La vista di chi scorre prendeva il primo paragrafo del §0 invece della serata; la cornice della visione stava solo nell'handout | **corretta**: il riquadro della serata ha 🧭 e la posta (il Re vivo al Cuore); la cornice della Corona ha il suo riquadro; «Quando si gioca» e «Party» sono in un blocco a parte |
| **T26** 🟠 | DM-V2, DM-V3 | La vista non trova l'avversario né il «prepara» | **corretta** in parte: con il riquadro giusto la vista legge la serata; l'avversario della serata (l'orda, il drago, i bugbear) è nella tabella «Chi c'è» del §0, che la vista non estrae. È un limite dello strumento, e qui non si corregge |

### 🟡

| Voce | Rilievi | Cosa | Esito |
|---|---|---|---|
| **T27** | P#1, L#51, D-R37, DM-R8, L#52, DM-R18 | I tempi della serata e le soglie del punto di taglio | **corretta**: Scena 1 a 25', totale fra 3 h 15 e 4 h 20; soglie B e C scritte in ore |
| **T28** | P#3, L#34, L#53 | Il sapere bardico di Nala, il segreto del Re, il macigno di Dara | **corretta**: righe nuove per il sapere bardico; il Re rivela il segreto nella Scena 5; Dara può fermare un macigno |
| **T29** | P#5, L#22, L#23, L#24, P#2, P#6 | Le leve della Sessione 1 (prigioniero e presagio insieme, la Diplomazia, il presagio di Dara letto in chiaro); le capacità dell'orda | **corretta**: leve separate, +4 insieme; scambio di Diplomazia chiarito; il presagio di Dara si applica senza spiegarlo; le tre capacità dell'orda in «Cosa preparare» come cosa del DM |
| **T30** | P#11, P#12, DM-R9, D-R5, P#13 | La corda dalla piattaforma, il ritorno dallo sportello, il giavellotto | **corretta**: corda in 5 round (3 con l'accelerata); il giavellotto entro 27 m |
| **T31** | P#20, D-R11, L#41 | Le baliste contro CA 37 | **già decisa** (domanda 2 dell'apparato, già su card a Jfs): il master dice che col libretto il d20+10 non vale contro il drago, e la balista B colpisce solo col 20 naturale |
| **T32** | P#22, P#29, D-R42 | Thorin morto, i pf del Re all'alba, Dana che perde i suoi pf | **corretta**: Thorin lo rianima Dana; il Re riparte da 196 ogni alba salvo eccezioni; Dana perde i pf sulle Mura |
| **T33** | P#26, DM-R16, L#33 | Nala e l'orchesco entro 9 m | **corretta** (§1 e Scena 4) |
| **T34** | P#30, L#39, D-R23 | Chi tira contro il soffio in linea; i danni del sorvolo; dove sono gli eroi dopo la sequenza | **corretta**: Thorin tira se è sulle Mura; i danni del sorvolo non passano al Giorno 3; ai round 3-4 ogni eroe sceglie se restare col Re |
| **T35** | P#38, P#40, DM-R20 | *Comunione* in 1 minuto; il comando «Apri» | **corretta**: 10 minuti nel master e nell'handout `ARC08-15` (riga 241); la Corona usa *comando* «Lascia!» sulle guardie, o il Re sfonda la porta |
| **T36** | P#39, DM-R12, L#40 | La freccia assassina | **corretta** (Tempra CD 20 o 50 danni, SRD 3.5; la soglia dei 50 danni per atterrare vale per tutti gli eroi) |
| **T37** | P#46, D-R32, D-R41 | Il furtivo di Nala sui bugbear fiancheggiati; il canto e gli incantesimi; la CD 16 | **corretta** la parte di Nala (non si fiancheggiano; mentre canta non lancia); la parte sui bugbear è **respinta** (sotto) e A.7 scrive Int 18 |
| **T38** | P#48, L#47, L#48, L#49 | Quale bocca porta alla porta, l'anello fisso, Dana, perché la porta si apre, il Re che muore all'incrocio | **corretta**: le sei bocche con il nord verso la porta; l'anello cala coi salvati; Dana in Q20; la porta risponde alla Corona e al sangue. Il Re all'incrocio (esito aperto o −9) era un `[INFERRED]` senza numero: domanda 16 |
| **T39** | L#26, L#27, L#29, L#30, L#31, L#32, D-R15, D-R24, D-R13 | Gli adepti, le lanterne, la riserva, le Cantitrici, il «Dove» della Scena 4, il sergente, le guardie reali, «superare» una guardia | **corretta**; quante Cantitrici cadono resta del master: domanda 17 |
| **T40** | L#35, L#43, L#45, L#50, L#54, L#56, L#57, L#58, DM-R19, DM-R21, D-R35, D-R36, DM-V4 | Battuta del Re, «brecce est e ovest», la barriera «tunnel», i rimandi (§3, Rethmar, il cavaliere «caduto»), Handout 7, la targa, «un uomo che grida», «non scende sul cortile», le immagini delle Scene 7-9, il morale extra, il segnale degli orchi, le righe di scala | **corretta**; per le immagini il master dichiara che le Scene 7-9 non ne hanno |
| **T41** | P#23, P#31 | Le notti con poco da fare per tre giocatori; «se non è fuggito due volte» | **corretta** P#31; P#23 resta: le notti durano 5' l'una, ed è una scelta di ritmo |

### Respinti

| Voce | Rilievi | Perché |
|---|---|---|
| **R1** | D-R3 | Gorthak con sei attacchi è giusto. Nell'SRD l'ettin ha «Two Weapons» come capacità razziale e attacca con ogni mano senza penalità, e il bonus di attacco base da 15 DV dà gli iterativi a ogni mano: +21/+16/+11 e +21/+16/+11 |
| **R2** | D-R32 | Il bugbear Ladro 5 / Assassino 2 ha schivare prodigioso migliorato legalmente: l'SRD lo dà a chi ha schivare prodigioso da due classi (Ladro 4 e Assassino 2) |
| **R3** | D-R41 | La CD 16 c'era già: 10 + 2 + 4 di Int 18. Il master la scrive adesso in A.7, ma non cambia |
| **R4** | L#11, L#59 | Il soffio «troppo debole» per il racconto: il soffio (14d4, Riflessi CD 29) è un vincolo del giro e non si tocca; il Re arriva a 8 per il canone (T1). «Trenta nani» è la riserva intera, tre reparti, non uno |
| **R5** | L#46, D-R28, P#39 (la parte dei 3d6) | La 3Z è 33 × 33 quadretti e l'ottagono di 40 m sta dentro: le due misure tornano. Orchi e hobgoblin deboli per il livello: sono la diversione e l'inseguimento, e la scena li vuole così. La freccia assassina nel 3.5 non fa 3d6 extra al TS riuscito: era la regola 3.0 |

## Le domande nuove per il DM

**Decise il 2026-10-22:** Jfs ha scelto «Tutte», le sei raccomandazioni sono canone nel master.

Sono nell'elenco in testa al master (13-18) e nell'apparato.

| N. | Domanda | Raccomandazione |
|---|---|---|
| 13 | La prova della ritirata (d20 + Combattere contro CD 28/30/32) | tenerla: senza un tiro la Scena 7 non ha un motore |
| 14 | Chi si unisce a un duello: il settore lasciato prende le tacche, anche se Dara tira dalla torre? | sì per chi scende; Dara che tira senza scendere lascia il settore a metà, e il settore prende le tacche solo se le avrebbe prese |
| 15 | L'attacco mortale sui pregen: paralisi o morte? | paralisi sui pregen, morte solo sul Re |
| 16 | Il Re all'incrocio: esito aperto o dadi fermi a −9? | esito aperto, detto ai giocatori prima della Scena 8 |
| 17 | Quante Cantitrici cadono se le Mura cedono entro il round 3 | tre, così il Coro si perde: è la posta del Giorno 2 |
| 18 | Il ponte levatoio che si rompe (80 pf, durezza 5) | tenerlo: è la mossa che un tavolo prova contro Gorthak |

## Cosa non è nel master

- **D-R40** · la carta di Thorin in `ARC08-15` ha sette incantesimi di 3° e
  il chierico di 12° con Saggezza 22 ne prepara sei. Si corregge sulla carta
  e nella scheda di `ARC08-02`, togliendone uno: quale togliere lo sceglie
  chi tiene le schede dei pregen. Qui non si tocca.
- **DM-R19** · l'Handout 7 va ancora ricavato a mano da `immagini/04.webp`.

## Verifica e seconda passata

La verifica (un `claude -p` nuovo sulla copia corretta in `freddo-2/`) è in
[`VERIFICA.md`](VERIFICA.md): T1-T26 con 19 voci chiuse, 6 parziali, 1
aperta (T26, dichiarata), nessun 🔴; tredici rilievi nuovi (N1-N13, due 🟠).
La seconda passata, sul master:

| Rilievo | Esito |
|---|---|
| N1 🟠 Dara contro il cavaliere | **corretto**: +15, colpisce con 8, circa 15 danni a round; da sola non lo abbatte prima del round 5 |
| N2 🟠 il master pesa 22.400 parole | **resta**: è il prezzo delle procedure aggiunte (il conto del Re, la prova della ritirata, i bugbear). Il percorso breve resta quello di T24 |
| N3 l'orologio delle fasi | **corretto**: le fasi contano i round della colonna, dalla statua aperta |
| N4 il rimando del box di Grimjaw | **corretto** |
| N5 «vivo sopra gli 8» nella scheda | **corretto**: tolto, c'è «dove» |
| N6 più di 15 caduti all'incrocio | **corretto**: riga nuova |
| N7 le probabilità della spinta | **corretto**: una su venti, dieci, sette |
| N8 il Re che sfonda la porta | **corretto**: 20 pf e durezza 5, il martello |
| N9 il tragitto del Re | **corretto**: circa 20 round, con l'acido |
| N10 la lancia contro la CA corrosa | **corretto** |
| N11 il muro di Dana speso due volte | **corretto**: nella Scena 8 solo se non l'ha speso nella Scena 7 |
| N12 regole da riscontrare | **restano a memoria**: SRD 3.5 *slaying arrow* (Tempra CD 20 o 50 danni, nulla a TS riuscito) e il tempo per togliere un'armatura pesante (1d4+1 minuti con aiuto); la rete non raggiunge l'SRD |
| N13 Dara e la stalagmite | **corretto**: «a circa 3 m dalla S5 (L7)» |
| T23 i default | **corretto**: baliste A se il DM non sceglie; il Re all'incrocio a esito aperto finché il DM non decide |
