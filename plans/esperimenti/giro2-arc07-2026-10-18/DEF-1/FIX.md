# ARC07-DEF-1, secondo giro: le correzioni

Esiti: CORRETTO 30 · DECISIONE DM 11 · RESPINTO 2 · 🟡 lasciati 13

Il master corretto è `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md`. Ho rigenerato soltanto il suo apparato (`APPARATO-ARC07-DEF-1-…`), perché lo chiedeva `componenti.py --check` dopo le mie modifiche. Le decisioni comprendono anche i cinque `[INFERRED]` già presenti nel master, che nessun lettore aveva segnalato. Non ho aggiunto nessun `[INFERRED]` nuovo.

Le misure dopo le correzioni:

- `misura_craft --box`: 43 box, nessuno sopra le 12 righe, nessuna parentesi, nessun box con più di un nome proprio nuovo. Sono gli stessi numeri di prima, perché non ho toccato nessun box.
- `validate_prosa`: nessun tic oltre soglia.
- `domande_developer --check`, `copertura_scene --check`, `test_storico` (8 test) e `validate_modules` sono verdi. Prima del mio giro `copertura_scene` falliva su DEF-2; ora passa.
- `componenti --check` è rosso solo su `APPARATO-ARC07-DEF-5`, che dipende dal master di un altro correttore. Non l'ho toccato.

Le righe di legenda che ho cambiato nelle MAPPE T-2, T-5 e T-6 sono le stesse nell'Atlante (`Mappe/ARC07-MAPPE-DEFINITIVO.md`, righe 260 e 329). Quel file non è mio: lì le righe sono rimaste quelle di prima, e qualcuno deve riportarle.

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Xorn che emergono, mordono e si rituffano nello stesso turno (DEV#1, PT#1, DM#4) | 🔴 | CORRETTO | Ho riscritto le Tattiche, il round 1, il round 2 e la legenda della T-2 secondo l'SRD. Lo Xorn che emerge e morde resta in superficie, al turno dopo fa l'attacco completo oppure si rituffa e riemerge con un morso solo. Il round di sorpresa serve solo a emergere. È la lettura più forte fra quelle legali, perché toglie i round vuoti e aggiunge gli attacchi completi. |
| Di che tipo è Aegis Fang (DEV#2) | 🟠 | CORRETTO | `state.md` §5 la dà come ascia da guerra nanica. Dove il testo diceva «lancia» (il gancio Returning, la Radice a Terra, lo yes-and, 8c-2) ora dice «ascia». |
| EL con cinque PG: 13 o 14 (DEV#3, PT#6) | 🟡 | RESPINTO | Il conto dà 13. Un GS 6 vale 1/8 di un GS 12, quindi quattro Xorn sommano 0,5; il totale è 1,5 volte Fauci, cioè EL 12 + 2·log₂1,5 ≈ 13,2. Il master è giusto. |
| Blast ~28 contro gli Xorn (DEV#4) | 🟡 | CORRETTO | Ora è ~25: il d6 di fuoco e quello di freddo non contano, perché gli Xorn ne sono immuni. |
| Spaccare senza bonus di taglia (DEV#5) | 🟡 | CORRETTO | Ho messo +37 nello statblocco e nel round 2, con la fonte (SRD *Spezzare*: +4 per categoria di taglia). |
| Fenditure senza nessuno che le usi, Push di Terros nella foresta (DEV#6) | 🟡 | CORRETTO in parte | Nella cella ora spinge Fauci di Diamante, che ha Spinta Migliorata. Le fenditure non sono disegnate sulla T-2 e manca la riga di tattica: quella parte resta da fare. |
| Rompere un cristallo vale −1 successo o un fallimento (DEV#7) | 🟠 | CORRETTO | Ho allineato l'Atlante al §6, che è il punto in cui sta la regola: vale un fallimento. |
| Skill challenge, salto e rito scritti per tre PG (DEV#8, PT#24) | 🟠 | CORRETTO | Ho aggiunto tre righe. Nello skill challenge la soglia resta 6 prima di 3, e chi non ha una prova sicura aiuta o passa il giro. Nel salto il quarto PG sale la corda come Thorik. Nel rito il quarto PG aiuta Tordek o Artemis (Aiutare dell'SRD). |
| La giocatrice di Hella non sceglie mai (PT#24, la parte su Hella) | 🟠 | RESPINTO | È voluto: il §1 apre con il principio di regia chiesto dal DM, e Hella morta è canone bloccato (`campaign-coherence` §1). |
| Fisica del salto verso il Tempio (DEV#9, DM#13) | 🟠 | DECISIONE DM | Ho corretto una parola (chi scivola «finisce» nell'oceano, non «cade»). Il resto è canone che manca: vedi la decisione D1. |
| pf, caratteristiche e TS della Sentinella (DEV#10, PT#12, PT#13, DM#9) | 🟡 | CORRETTO | Restano i 160 pf, con la nota che la media SRD sarebbe 129. Ho aggiunto FOR 27, DES 14, SAG 11, CAR 1, BAB/Lotta +13/+25 e TS +6/+8/+6, calcolati dalle regole SRD dei costrutti; la FOR viene dallo schianto +20. |
| Attrazione Fatale senza bersaglio, pareti «LETALI» (DEV#11) | 🟡 | CORRETTO | Ora strappa a Tordek il metallo che non è un artefatto, e se Tordek non ne porta non la usa. Nella legenda della T-5 le pareti «incollano». |
| La tattica di Terros non si applica a questo gruppo (DEV#12) | 🟠 | CORRETTO | Ho riscritto R2, R4+, il punto 3 dello statblocco e il «trucco della frana». Terros passa un turno dentro l'Altare, e al turno dopo riemerge con uno schianto accanto al PG a terra. Ogni riemersione è il momento della Radice a Terra. |
| Quanto del pugno di Tordek diventa sonico (DEV#13, DM#5, PT#19) | 🟠 | DECISIONE DM | Vedi D2. |
| Spallata illegale contro un Enorme (DEV#14) | 🟡 | CORRETTO | 8c-2b ora dice che non è legale (SRD *Spingere*). Ho tolto la spallata anche dalle tre righe che la davano come risposta all'arrocco, e dalla T-6. |
| Raffica con un attacco di troppo (DEV#15, PT#20) | 🟡 | CORRETTO | La raffica è +12/+12/+7. Il DPR scende da ~12 a ~11, perché il quarto attacco colpiva solo col 20. |
| Terros senza riga di scala per quattro o cinque PG (DEV#16) | 🟠 | CORRETTO | Ho aggiunto una riga che usa varianti già scritte: con quattro PG il profilo a 34 DV, con cinque i 34 DV più i due Elementali Grandi. Non c'è nessun numero nuovo. |
| Il duello formale non ha regole (DEV#17, PT#17) | 🟠 | DECISIONE DM | Vedi D3. |
| Tutti i TS di Terros sono su Riflessi (DEV#18) | 🟡 | lasciato | Non so se è voluto, e dichiararlo voluto sarebbe inventare. |
| «Rigenera» si legge come la Rigenerazione dell'SRD, percezione tremorica non dichiarata (DEV#19, PT#22) | 🟡 | CORRETTO | Nello statblocco e nella Quick-Reference ora c'è «guarigione rapida, il danno resta letale». La percezione tremorica è entrata nel riquadro ⚠ Non SRD. La legenda della T-6 dice che il gruppo non può spingere Terros nello zero-G. |
| Terros senza Boost log né benchmark (DEV#20) | 🟡 | lasciato | Per giustificare il GS 15 servono le regole di avanzamento della MM, che non sono nell'SRD che posso controllare. |
| Velocità «~7 m» (DEV#21, PT#7, DM#12) | 🟡 | CORRETTO | Si arrotonda per difetto al quadretto: 9 m diventano 6 m, i 6 m dei nani diventano 4,5 m. |
| Il pilastro crolla, ma dove e su chi (PT#2) | 🟠 | DECISIONE DM | Vedi D4. |
| Conoscenze CD 18 senza gradi (PT#3) | 🟡 | CORRETTO | Ho scritto che oltre la CD 10 servono i gradi, e che i nani possono tirare Cercare CD 18 come al §6. |
| Chi parla Terran (PT#4) | 🟡 | lasciato | Le lingue dei PG non sono nel repo che ho letto. |
| Il mithral dopo il negoziato (PT#5) | 🟡 | CORRETTO | Ho allineato il §5 al tesoro del §11-bis B: il mithral c'è con le vie B e C, i geodi solo dagli Xorn uccisi. |
| Due regole di caduta (PT#8, DM#11) | 🟡 | CORRETTO | Le fenditure sono profonde 18 m, ricavati dal vecchio 6d6, e fanno 6d10 con la regola del §3. |
| Durata delle Benedizioni, 24 h o finché si resta nel Piano (PT#9) | 🟡 | lasciato | Non è chiaro quale delle due righe sia canone. Serve `DEF-2` §6, che non è mio. |
| La scala cantata (PT#10) | 🟠 | DECISIONE DM | Ho chiarito il testo: le quattro prove fanno la scala intera, e canta un PG alla volta come nel §8. La parte sui tentativi illimitati va al DM: vedi D5. |
| Velocità di volo di Artemis (PT#11) | 🟡 | lasciato | È sulla scheda del PG, e quella non l'ho. |
| Con quale azione Thorik si libera (PT#14) | 🟡 | lasciato | Non so se sia standard o di round completo. |
| Il Seme senza durezza (PT#15) | 🟡 | lasciato | Per il gruppo di oggi la scena è giocata. |
| Echo Ledger con la scelta di Varis al §6 superato (PT#16, DM#15) | 🟡 | CORRETTO | Ho tolto la riga. La riga del Seme-Mercato (§6-bis) copre già lo stesso filo. |
| Il Blast sonico conta come canto? (PT#18) | 🟡 | CORRETTO | No. Ora lo dice in chiaro: non rende sonici i pugni di Tordek. |
| Round di sorpresa a un solo PG (PT#21) | 🟡 | CORRETTO | Nell'SRD agisce ogni PG pronto, con un'azione standard o di movimento. |
| Thorik rifiuta il Peso e nessuno paga (PT#23, DM#8) | 🟠 | DECISIONE DM | Vedi D6. |
| Iniziative «+?» (PT#25) | 🟡 | CORRETTO | Ora dice «dalla scheda». La DES di Thorik è cambiata due volte (`state.md`). |
| Compratori per il bottino (PT#26) | 🟡 | lasciato | Il delta WBL si colma a Hammerfist, ARC-08. |
| La vista non dice cosa vuole Terros, né chi è Varis (DM#1) | 🟠 | CORRETTO | Ho aggiunto al primo paragrafo del §0, che è quello che la vista mostra, il voto di Terros e Varis «un mercante di Rethmar». |
| La vista non mostra l'orologio né le schede esterne (DM#2) | 🟠 | CORRETTO | Nello stesso paragrafo ho aggiunto la scheda dei Bracieri e l'orologio a 3g 20h. |
| Grassetti della vista (DM#3) | 🟡 | lasciato | Li sceglie il generatore della vista, che non è il master. |
| Un'ora non basta per la via breve (DM#6) | 🟠 | CORRETTO | La via breve ora indica i pezzi delle Scene 7, 8 e 9 da leggere, invece delle scene intere. |
| La scheda dei Bracieri è fuori dal file (DM#7) | 🟠 | CORRETTO | Ho aggiunto al §7b la tabella dei poteri Fuoco, presa dal riepilogo di `05_Bracieri_Gemelli_Scheda_PG_Completa.md`: Pugni di Magma, Colpi del Fuoco, Salto, Cariche, Frantumare, Martello. Nessun numero è mio. |
| pf di Terros: 345, 346 o 348 (DM#10) | 🟡 | CORRETTO | 346 era un refuso, ora è 345. Lo statblocco dice che con Robustezza sarebbero 348, e che il modulo tiene 345 per non spostare le soglie. |
| Totali di PX e di mo (DM#14) | 🟡 | CORRETTO | 10.300 diventa 10.500 in due punti; ~5.200 mo diventano ~3.100. |
| La pietra vivente del rito: di chi è (DM#16) | 🟡 | lasciato | È un fatto di canone che manca. |
| Artemis che precipita in gravità doppia (DM#17) | 🟡 | CORRETTO | Cade dalla quota a cui vola e prende il danno del §3. |
| La Scena 5 stampata fuori ordine, la Frequenza sparsa (DM#18) | 🟡 | lasciato | Sarebbe un riordino, fuori dal mandato di un giro di correzioni. |
| Asset esterni (DM#19) | 🟡 | lasciato | Sono file fuori dal master. |
| «Tre affari» di Varis non detti (DM#20) | 🟡 | lasciato | Stanno nella scheda di Varis nel Bestiario, che non era fra i miei file. |
| Lo Xorn 2 da O05 non arriva ad Artemis (DM#21) | 🟡 | CORRETTO | Il round 1 ora dice che le 🕳️ sono i punti di pattuglia e che gli Xorn si portano sotto il bersaglio mentre il party si avvicina. La griglia non l'ho toccata. |

## Decisioni per il DM

### D1 · La fisica del salto verso il Tempio

Attorno al Tempio la gravità è zero, ma il salto è scritto come un Saltare CD 25 in gravità normale. Nell'SRD una CD 25 vale 7,5 m con la rincorsa e raddoppia senza rincorsa, mentre la gravità del Tempio cattura Tordek solo a 20 m dalla riva. Il testo non dice quanti salti servono, né se il «Take 10 = 26» comprende già il −5 della gravità e il +2 della Benedizione.

**Domanda.** Decidi come si attraversano i 20 m di zero-G fino alla cattura.

- **Spinta unica.** Il Saltare CD 25 decide la direzione della spinta (la regola dello zero-G del §0-bis): se riesce, Tordek arriva ai 20 m in linea retta con un solo tiro, e se fallisce entra in gioco l'Ancora.
- **SRD letterale.** Ogni salto copre 7,5 m, e dai detriti la CD raddoppia: servono tre salti, e il terzo è quasi impossibile.
- **Catena di detriti.** Due salti CD 25 da detrito a detrito, ognuno con la sua Ancora.

**Raccomandata: Spinta unica.** È l'unica che usa la regola dello zero-G già scritta nel modulo e che regge il «Take 10 = 26» confermato al tavolo. Il pericolo resta nell'Ancora e nell'oceano. Va anche confermato che il 26 comprende già gravità e Benedizione.

### D2 · Quanto del pugno di Tordek diventa sonico

Nel round in cui il gruppo canta la Frequenza, i colpi di Tordek «sono sonici». Il testo non dice se lo diventa tutto il colpo o solo il danno senz'armi, e da questo dipendono sia la soglia del Frantuma-Scudo (>15 sonici) sia la RD 10/—.

**Domanda.** Stabilisci quale parte del colpo di Tordek diventa sonica.

- **Tutto.** Diventa sonico il colpo intero, Pugno Frana e fuoco compresi: la RD non si applica e Terros prende ×1,5. Il Frantuma-Scudo scatta spesso.
- **Solo la base.** Diventa sonico solo il danno senz'armi (1d10+2); i 4d6 e il fuoco restano del loro tipo. Il Frantuma-Scudo scatta di rado.
- **Base più Pugno Frana.** Diventano sonici il danno senz'armi e i 4d6 del Pugno Frana; il fuoco resta fuoco.

**Raccomandata: Base più Pugno Frana.** Mettere il boss nella versione più forte vorrebbe «Solo la base», ma così la contromossa firmata di Tordek non scatterebbe quasi mai. Con il Pugno Frana la soglia si passa solo con il potere a 3/giorno, e ogni scudo rotto costa a Tordek un uso.

### D3 · Il duello formale con Terros

Le Contingenze offrono un duello formale con un campione, e il §8 lo dà come strada verso il rito. Non c'è scritto con quale profilo combatte Terros, cosa vuol dire «onorato», né cosa succede se il campione cade o se Terros resta vivo.

**Domanda.** Scegli le regole del duello formale, o toglilo.

- **Toglierlo.** Terros ascolta una frase e risponde col voto; resta il rispetto dopo lo scontro.
- **Fino alla morte.** Il campione combatte senza aiuti contro Terros a profilo pieno. Se cade viene espulso come nella riga del PG caduto, e il gruppo può combattere dopo.
- **Fino all'arrocco.** Profilo pieno, niente aiuti; quando Terros scende a 172 pf la Forza è dimostrata, lui si inginocchia e assiste vivo al rito. Il campione che cade viene espulso.

**Raccomandata: Fino all'arrocco.** È la più dura che non finisce per forza in un TPK. Un singolo PG che regge Terros fino a metà pf è un'impresa leggendaria, e il guardiano vivo che assiste al rito è un'eco per il #4.

### D4 · Dove cade il pilastro della via A

La via A abbatte il pilastro sugli Xorn (10d6, Riflessi CD 22), ma il master non dice in che direzione cade, quanto è grande l'area né chi c'è dentro. Il canone dice solo che travolge chi è sotto.

**Domanda.** Definisci l'area del crollo del pilastro.

- **Linea scelta.** Una striscia larga 3 m e lunga 30 m dalla base G08, nella direzione scelta da chi ha superato la Conoscenze; se la prova è fallita, la direzione si tira col d8. I PG nella striscia tirano anche loro.
- **Cerchio alla base.** Un raggio di 6 m attorno a G08, dove gli Xorn mangiano: prende Fauci di sicuro e forse i PG vicini.
- **Solo gli Xorn.** Chi ha letto l'angolo di rottura fa cadere il pilastro solo sugli Xorn.

**Raccomandata: Linea scelta.** È la più pericolosa e premia la prova di Tordek: chi legge bene la pietra sceglie dove cade, chi sbaglia rischia di prenderselo addosso.

### D5 · Quante volte si può cantare la scala

La scala cantata si costruisce con quattro prove riuscite, e ogni fallimento fa ricadere un blocco. Nel Piano il tempo non muove l'orologio, quindi oggi i tentativi sono illimitati e gratis, contro il «mai gratis» dello yes-and della stessa pagina.

**Domanda.** Fissa un limite ai tentativi della scala cantata.

- **Illimitati.** Resta com'è: ogni fallimento costa un blocco e basta.
- **Tre fallimenti.** Al terzo fallimento la scala crolla tutta e si passa ai tre ruoli, come è successo al tavolo.
- **Un round a prova.** Ogni prova costa un round, e al terzo fallimento cade chi sta sui blocchi.

**Raccomandata: Tre fallimenti.** Rifà quello che è successo al tavolo, dove i blocchi sono crollati a metà, e dà un costo alla strada cantata senza toccare l'orologio.

### D6 · Thorik rifiuta il Peso e nessuno paga

La Fase 1 del rito ha due uscite: 40.500 mo, che il bottino non copre, oppure il Peso nel corpo di Thorik. Se il giocatore di Thorik dice di no e il gruppo non paga, il rito non ha un seguito scritto, e la gemma con la campagna restano ferme. Al tavolo di oggi Thorik ha accettato; la riga serve a un gruppo nuovo.

**Domanda.** Decidi cosa succede se Thorik rifiuta e nessuno paga.

- **Si riposa.** Il rito non parte. Dopo un riposo (−12 h) Moradin ripete la domanda, e al secondo rifiuto la Corona prende il Peso da sola.
- **La Corona prende.** Il rito parte subito e Thorik paga il Peso comunque, senza averlo scelto.
- **Pagamento misto.** Il gruppo dà tutto il bottino e Thorik paga metà del Peso (−1 DES, +1 COS, +2 CAR).

**Raccomandata: Si riposa.** Costa tempo e una seconda domanda davanti a tutti, che pesa più della prima, e il rito non resta mai bloccato. Lasciare scegliere al giocatore è la regola della Fase 1.

### D7 · «Se lo divinano» `[INFERRED]` (§0)

La tabella dice cosa risponde una divinazione per ogni segreto del modulo, ed è marcata come non confermata.

**Domanda.** Conferma la tabella «Se lo divinano» come canone.

- **Confermare.** La tabella diventa canone così com'è.
- **Stringere.** Diventano canone tutte le righe tranne quella della Sala, che resta muta: il riposo che costa meno resta un segreto anche per la divinazione.

**Raccomandata: Confermare.** Le risposte premiano chi lancia (§9 della skill del developer) e nessuna rompe l'asimmetria su Hella.

### D8 · Chi capisce il campo gravitazionale del Tempio `[INFERRED]` (§7a)

Chi supera la Conoscenze CD 18 o l'Osservare CD 20 vede i tre ruoli e il punto di cattura; chi fallisce li scopre per tentativi, e Aegis Fang li suggerisce.

**Domanda.** Conferma cosa ottiene chi capisce il campo del Tempio.

- **Confermare.** Il testo resta com'è.
- **Senza aiuto.** Chi fallisce scopre i ruoli solo per tentativi, e Aegis Fang non suggerisce niente.

**Raccomandata: Senza aiuto.** È la versione più dura, e la vibrazione di Aegis Fang fa già da bussola altrove nel modulo. Qui il fallimento deve costare un tentativo.

### D9 · L'Overdrive della Sentinella con un PG più debole `[INFERRED]` (§7b)

Con un PG del duello di livello 12 o meno, oppure con CA sotto 26, l'Overdrive dà due attacchi invece di tre.

**Domanda.** Scegli quanti attacchi dà l'Overdrive contro un PG più debole.

- **Due attacchi.** Il testo resta com'è.
- **Tre sempre.** L'Overdrive resta a tre attacchi: la rete di sicurezza è il secondo tentativo, che riparte dalle crepe già aperte.

**Raccomandata: Tre sempre.** È la versione più forte, e il modulo ha già due reti: Tordek a −1 resta stabile, e chi ritenta riparte dalle crepe aperte.

### D10 · Terros a 34 DV: le CD e il segno degli Elementali `[INFERRED]` (§8, Scalare lo scontro)

Nel profilo a 34 DV il +1 alle CD vale per Onda e Stalattiti, mentre Spinta e Radice a Terra restano a 25. Anche il segno dei due Elementali Grandi (le rune che si spengono, la pietra che si gonfia) non è confermato.

**Domanda.** Fissa le CD del profilo a 34 DV e il segno dei rinforzi.

- **Com'è scritto.** +1 solo a Onda e Stalattiti, il segno com'è.
- **Spinta 26.** Anche la Spinta, che è un potere di Terros, sale a 26; la Radice a Terra resta 25, il segno com'è.
- **Tutto +1.** Spinta e Radice a Terra salgono a 26.

**Raccomandata: Spinta 26.** Il boss più forte spinge più forte. La Radice a Terra è un'errata calibrata proprio per essere tentabile, e alzarla toglierebbe a Thorik la sua sola risposta all'arrocco.

### D11 · La fatica della sconfitta contro Terros `[INFERRED]` (§8, Contingenze)

I caduti espulsi hanno un livello di affaticamento che nessun riposo nel Piano toglie, e nemmeno il *Vigore della Forgia*.

**Domanda.** Conferma che la fatica della sconfitta non si cura nel Piano.

- **Confermare.** La fatica resta fino alla Sala.
- **Col Vigore.** Una carica di *Vigore della Forgia* la toglie, come la fatica del viaggio.

**Raccomandata: Confermare.** È la versione più dura, ed è il prezzo della sconfitta che il modulo promette: «costa tempo e orgoglio».

## Seconda passata

Esiti: CHIUSI 4 (PARZIALE 1, NUOVO 🟠 1, NUOVI 🟡 2) · in attesa del DM restano D1-D11.

| Voce di VERIFICA.md | Gravità | Esito | Cosa ho fatto |
|---|---|---|---|
| DM#6 · la via breve di un'ora è ancora troppo lunga | 🟠 (PARZIALE) | CHIUSO | Della Scena 8 restano da leggere lo statblocco e le Tattiche; i box della soglia e delle Scene 1-6 si leggono al tavolo dal file, e Contingenze e §8c si consultano durante lo scontro. Il riferimento della Scena 9 ora porta al titolo vero, «Il giro del round in quattro battute». Ho anche tolto il doppio «§8c» dalla frase dopo. Contate col mio script: circa 7.400 parole (§0 e §0-bis 2.164, Scena 7 fino alla regia 1.409, statblocco e Tattiche 3.035, Fase 1 751, giro 73), cioè 35-40 minuti di lettura, con il resto dell'ora per gli appunti. |
| NUOVO 1 · l'Atlante contraddice il master sugli Xorn, su «LETALI» e sullo zero-G | 🟠 | CHIUSO | In `Mappe/ARC07-MAPPE-DEFINITIVO.md`, su richiesta del coordinatore, ho cambiato quattro righe e nient'altro: le tattiche degli Xorn e la tattica dei PG ora seguono la regola SRD del master (§5); nella legenda T-5 le pareti «incollano chi porta metallo»; nella T-6 Terros nello zero-G non guarisce, ma il gruppo non ha come spingercelo. Ho riletto il file subito prima di toccarlo. |
| NUOVO 2 · «la l'ascia» | 🟡 | CHIUSO | Ora è «(l'ascia di Thorik come rampino…)». |
| NUOVO 3 · «Rigenerazione» rimasta in due punti | 🟡 | CHIUSO | «la guarigione scende a 10/round» e «(NIENTE GUARIGIONE)». |

I gate dopo la seconda passata: `domande_developer --check`, `copertura_scene --check`, `test_storico` (8 test), `validate_modules`, `validate_maps` e `validate_prosa` sono verdi. In `misura_craft --box` restano 43 box e nessuno sopra le 12 righe. Come mi è stato chiesto, non ho lanciato `componenti.py --apparato`: l'apparato di DEF-1 va rigenerato, perché il §0 è cambiato.
