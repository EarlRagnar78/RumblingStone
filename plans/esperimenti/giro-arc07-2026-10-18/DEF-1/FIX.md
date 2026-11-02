# DEF-1 · Il Piano della Terra e Terros l'Antico — correzioni del giro

Esiti: CORRETTO 23 · DECISIONE DM 6 · RESPINTO 0 · 🟡 lasciati 18

Oltre ai 29 rilievi 🔴 e 🟠 (unificati dai tre rapporti), ho corretto 22 🟡 che costavano una riga ed erano sicuri. Master toccato: `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md`. Nessun box read-aloud è stato toccato.

**Verifica.** `misura_craft.py --box`: DEF-1 identico a prima (28 box, 0 oltre le 12 righe, 3 con parentesi, 7 con più di un nome, gli stessi di `craft-prima.txt`). `validate_modules.py`: 5 master conformi, 0 errori. `componenti.py --check` segnala da rigenerare tutti e cinque gli `APPARATO-ARC07-DEF-*.md`: per DEF-1 c'entra la riga «Combatte» della scheda d'entrata di Terros, che ho cambiato (rilievo PT#25). Non l'ho rigenerato, perché le regole del giro vietano di toccare altri file: va fatto da chi orchestra con `python3 scripts/componenti.py --apparato`, a giro chiuso.

## Rilievi 🔴 e 🟠

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Earth Glide nell'Altare di mithral (DEV#1, PT#21, DM#20) | 🔴 | CORRETTO | Nello statblocco, sotto EARTH GLIDE: l'Altare, mithral consacrato, conta come pietra anche per l'Earth Glide, come già per l'Earth Mastery. La riga dichiara che diverge dall'SRD («except metal») e vale la versione più forte del guardiano. Così resta valido quello che il tavolo ha giocato |
| PG espulso a −1 pf: come rientra, e il rito senza Thorik (PT#24, DM#27) | 🔴 | CORRETTO | Nella riga «Un PG scende a −1 pf» di *Scalare lo scontro*: l'espulso non rientra nello scontro, e il rito lo aspetta. Chi è rimasto torna a prenderlo rifacendo il §7a, e se l'espulso è Thorik il rito aspetta lui, perché la Corona è legata al portatore (coerenza §2.3). La riga della sconfitta adesso dice come si torna |
| «Nauseato» usato come −4/−4 (DEV#2, DM#21) | 🟠 | CORRETTO | Diventa «intontito dal canto: −4 ad attacco e CA il round 1, agisce normalmente», con la nota che non è il *nauseato* SRD. Ho tenuto il −4/−4 perché è quello giocato. Il *nauseato* del box PF1e sullo zero-G è la condizione vera, e l'ho lasciato |
| Round 1 di Terros con due azioni standard (DEV#3, DM#22) | 🟠 | CORRETTO | TATTICHE R1: l'Onda è l'azione del round. Il Lancio di roccia o la carica li fa solo se nessuno è sull'Altare, al posto dell'Onda |
| Il potere «Tremore» non esiste (DEV#4, DM#25) | 🟠 | CORRETTO | «Tremore/Onda» diventa Onda; «Tremori a ripetizione» diventa «un'Onda ogni volta che la ricarica lo permette» |
| Artemis invisibile in volo (DEV#5, PT#32) | 🟠 | CORRETTO | Paragrafo in 8c-1 con le regole SRD dell'*invisibilità*: chi combatte si sente con Ascoltare CD 0, più 1 ogni 3 m, e chi supera la CD di 20 trova il quadretto. Le Stalattiti sono un'area e non tirano la probabilità di mancare, e un'*invisibilità* normale finisce al primo Blast |
| Quanti «massi principali», e cosa annulla un blast preparato (DEV#6, PT#23) | 🟠 | DECISIONE DM | D-1 qui sotto |
| «Radice a Terra»: dove deve stare Thorik, e quando si tira il caso «alla cieca» (DEV#7, DM#23) | 🟠 | CORRETTO | Riga «DOVE E QUANDO» nello statblocco. Terros deve essere nella portata di Thorik. L'azione preparata scatta all'emersione entro la portata, e se Terros riemerge lontano va persa. Il caso «alla cieca» si tenta nel turno di Thorik contro un Terros adiacente, e il blocco vale fino al suo turno successivo. Sono le regole SRD dell'azione preparata applicate alla manovra che il modulo ha già |
| Elementali della Terra Grandi senza tattica (DEV#8) | 🟠 | CORRETTO | Una riga: emergono dall'Altare (non c'è pavimento), non volano, uno per nano, non inseguono nello zero-G e tornano nella pietra quando Terros cade |
| Diapason contro l'Immunità alla magia della Sentinella (DEV#9, PT#20, DM#18) | 🟠 | CORRETTO | Il DM ha già deciso (D89) che fa danno sonico, com'è stato giocato. Ho scritto l'eccezione: il Diapason è un dono della Madre e passa come la Risonanza dei Bracieri, con la divergenza dall'SRD dichiarata. Nello statblocco ora c'è «(non al Diapason)», come per lo stordimento di Terros |
| Statblocco di Fauci di Diamante contro l'SRD, la RD 10/adamantio, la calibrazione e il Boost log (DEV#10, DM#12, DM#13) | 🟠 | DECISIONE DM | D-2 |
| Via B: imboscata contro la percezione tremorica (DEV#11, PT#7) | 🟠 | CORRETTO | La via B non sorprende gli Xorn, che emergono per primi. Il −2/+2 viene dallo schieramento sui punti d'emersione e non è fiancheggiamento. I numeri sono quelli di prima |
| *Vigore della Forgia* e le altre Benedizioni non definite (PT#1, DM#7, PT#2) | 🟠 | CORRETTO | Nella Scena 1, tabella delle tre Benedizioni presa da `DEF-2` §6 e dal PDF: ogni PG ha le sue, il Vigore cura 3d8+5 a sé o 2d8+2 a un alleato a contatto, è un'azione standard e nel Piano torna dopo ogni riposo (D87). Ne segue che Artemis, prono alla parete, non cura Tordek |
| Volare in 3.5 (PT#5, DM#9, DEV#21) | 🟠 | DECISIONE DM | D-3 |
| Skill challenge: cosa conta come fallimento (PT#10, DEV#22) | 🟠 | CORRETTO | Ogni prova fallita è uno dei tre fallimenti, Diplomazia compresa, e il canto fallito toglie in più un successo. È la lettura più dura delle due possibili |
| I due cristalli crepati danno 4 successi gratis (PT#11, DEV#22) | 🟠 | CORRETTO | Riforgiare è la prova del giro di quel PG: si tira Osservare, e un fallimento conta. Ogni cristallo si riforgia una volta sola. Il «+2 automatico» resta, ma adesso costa un tiro |
| Artemis stacca cristalli vivi (PT#12) | 🟠 | CORRETTO | Conta un fallimento, e se è il terzo il giardino urla. Se lo skill challenge non era cominciato, comincia lì. Il cristallo staccato si spegne e non vale niente |
| La scala si alza con il Diapason o con la Frequenza? (PT#16, DM#17, DEV#18) | 🟠 | DECISIONE DM | D-4 |
| 40 m o 50 m, e l'ordine della MAPPA T-4 (PT#17, DM#33) | 🟠 | CORRETTO | Il Tempio è a 40 m dalla riva e il portale 50 m sopra l'oceano: una è la distanza, l'altra l'altezza. Una frase dice che la T-4 mostra il ramo dei tre ruoli, con le rune colpite all'arrivo. La mappa non l'ho toccata: è identica a quella dell'Atlante, che è un altro file |
| Secondo tentativo con la Sentinella senza metallo e a piedi (PT#19) | 🟠 | CORRETTO | Nuova riga in §7b, costruita solo con D87 e D88: la Magnetite non li incolla, ma Thorik può solo Aiutare, ad Artemis passano solo le invocazioni su sé o sui compagni, e il duello resta di Tordek |
| Onda contro Artemis in volo (PT#22, DM#10) | 🟠 | CORRETTO | Ho allineato lo statblocco al box del primo scambio e alle Sinergie: chi è in volo con le Ali d'Ombra all'inizio dell'Onda non si sposta. Due testi su tre dicevano così, e il box è quello letto al tavolo |
| Come si esce dal Piano (PT#36) | 🟠 | DECISIONE DM | D-5 |
| Tre cose necessarie stanno fuori dal file (DM#3) | 🟠 | CORRETTO | Le Benedizioni ora sono nella Scena 1. Per i poteri Terra dei Bracieri c'è una tabella in §7b, presa dalla scheda dei Bracieri (§2-5). L'orologio era già riassunto in §0. Il Quickstart dice dove stanno |
| Pugno Frana e Tremore del Forgiatore senza meccanica (DM#8) | 🟠 | CORRETTO | Tabella in §7b con uso, azione ed effetto, copiati dalla scheda dei Bracieri senza cambiare un numero |
| Un'ora di preparazione non basta (DM#5) | 🟠 | CORRETTO | Nel Quickstart: cosa leggere per intero (§0, §0-bis, Scene 7-9) e cosa si salta in preparazione |
| Una serata o due, e dove si stacca (DM#6) | 🟠 | CORRETTO | Nel Quickstart: al tavolo sono state due serate, il 24 luglio fino alla Sentinella e il 31 il Seme, Terros e il rito. Lo dicono le date dei blocchi di canone. Il punto di stacco è l'anticamera |
| Contratto del Seme: chi ascolta la voce ha già firmato (DM#14) | 🟠 | DECISIONE DM | D-6 |
| Regole della Frequenza sparse in sei punti (DM#35) | 🟠 | CORRETTO | La Quick-Reference dice dove sono la Frequenza in combattimento (§8) e la modalità sonica (8c-1), e il «più avanti» ora è «in 8c-1» |
| Il canone giocato si mescola alle regole del gruppo nuovo, soprattutto il Diapason (DM#37) | 🟠 | CORRETTO | Nel Quickstart, il paragrafo «Un gruppo nuovo non eredita il canone giocato», e in Quick-Reference una riga sul Diapason |

## 🟡 corretti

| Rilievo | Cosa ho fatto |
|---|---|
| DM#26 Frantumare contraddittorio | Sinergie e DEBOLEZZA ora dicono che i pugni di Tordek sono sonici col canto, ×1,5, come lo statblocco |
| DM#16, PT#14 Varis nel Campo dei Cristalli | La tabella delle zone non dice più «Cristalli + Varis». Le mappe T-1 e T-3 no: sono copie dell'Atlante |
| DM#29 Affresco A7 mostrato nel Tempio | «Al ritorno nella Sala mostra l'affresco A7» |
| DM#30 Iniziativa senza mostri | Aggiunti Xorn +0 (DES 10, SRD) e Sentinella +2 (il suo statblocco). Fauci aspetta la D-2, i PG la loro scheda |
| DEV#15 Geode: copertura totale o +4 | Nel §5 vale +4: Fauci morde dalle crepe, quindi la copertura non è totale |
| DEV#16 Xorn solitario e Xorn ritrovati | Una riga ciascuno: il solitario si rituffa e non torna, i ritrovati scavano via a metà pf |
| DEV#17 Chi sente | Nel Tempio non ci sono altri guardiani, e Terros non sente il duello |
| DEV#20 «Teletrasportarsi in Glide» | Earth Glide entro 6 m dall'Altare, con l'emersione sotto il ladro |
| DEV#23 «Togli 1 uso al Diapason» | «Togli il Diapason, che è monouso» |
| PT#4 *Endure Elements* | Il §4 ora dice che serve il filtro (+4) e che *Endure Elements* non basta, come il §0-bis |
| PT#6 Via C fallita | Se la Diplomazia fallisce o il tributo manca, gli Xorn attaccano come al round 1 |
| PT#8 Spaccare sull'armatura | Diventa «scudo o arma». Ho tolto «come la Sentinella», perché lei non fa Spaccare |
| PT#13 Lacrima di Cristallo | Ora la consegna il testo del Successo |
| PT#25 «Ignora chi è a terra» | Non colpisce chi è a 0 pf o meno; chi è prono resta un bersaglio |
| PT#26 Countdown dopo la fuga | Scende solo se riposano: −12 h a riposo |
| PT#28 Tentacoli contro Lotta +40 | Allineato all'8c-2b: anche col 20 naturale la parità va a Terros |
| PT#29, DM#31 Blast «automatico» | Manca con l'1 naturale (SRD), in tre punti |
| PT#30 Trinità sulla Spinta | Il +4 ai TS non vale sulla Spinta, che è una prova di Forza |
| PT#31 Mask e Lathander in 8c-4 | Tolti, come esclude il §1 |
| PT#33 Apertura sonica dopo il riposo | Non vale: Terros è già sveglio |
| PT#34 Un altro PG si offre per il Peso | La Corona accetta solo il portatore (coerenza §2.3). Resta aperto il caso del gruppo che non sceglie né A né B |
| PT#35 Tentacoli sull'Altare e rito | Il rito comincia quando il campo si spegne, dopo 13 round (1 per livello) |

## 🟡 lasciati

DEV#12 e DM#24, i conti dello statblocco di Terros (CA 25, contatto 7, +31, Volontà +14, 348 pf). Sono i numeri giocati, e correggerli cambia il DPR, la Trinità e la Radice: lo decide il DM. · DEV#13 e DM#11, Xorn comuni contro l'SRD: non ho la pagina SRD sotto mano per riscrivere ogni numero con certezza. · DEV#14, l'EL dichiarato. · DEV#19, i tre TS. · DM#1, DM#2 e DM#4, la vista di chi scorre. · DM#15 e PT#15, l'ora della pergamena dentro il §6-bis: è un blocco-componente condiviso con `DEF-4`. · DM#19, i pf della Sentinella. · DM#28, quali CD salgono a 34 DV. · DM#32, la battuta d'entrata di Fauci: è prosa nuova da tavolo e va scritta col ciclo della prosa, non qui. · DM#34, l'Altare che «scende a livello del pavimento» nello zero-G: la frase sta anche nel blocco di canone giocato. · DM#36, il registro dei riposi. · PT#3, le due regole di caduta. · PT#9, il mithral dopo la via C. · PT#18, due prove senza esito (campo gravitazionale, rune «Arcane»). · PT#27, la fatica dopo la sconfitta e il Vigore. · Mappe T-1 e T-3 con la runa di Varis: vanno corrette nell'Atlante e poi riportate qui.

## Decisioni per il DM

### D-1 · Il blast contro la Pioggia di Stalattiti

Il contro-momento di Artemis dice «un blast per masso principale», ma non dice quanti siano i massi. Un'azione preparata dell'SRD dà un attacco solo, e il DM non sa se quel blast annulla tutti gli 8d6 o una parte.

**Domanda.** Decidi quanto annulla un solo Eldritch Blast preparato contro le Stalattiti.

| Opzione | Conseguenza |
|---|---|
| **Tutto** | Un blast che colpisce annulla il danno per tutti i compagni: lettura generosa, contro-momento quasi garantito |
| **Un compagno** | Il blast abbatte il masso sopra un compagno a scelta, che non prende danni; gli altri tirano Riflessi 22 |
| **Metà** | Il blast dimezza il danno per tutti, e Riflessi lo dimezza ancora |

**Raccomandata: Un compagno.** È l'unica che rispetta la regola SRD (un'azione preparata è un attacco) ed è la versione più forte del boss. Il momento di gloria di Artemis resta: sceglie chi salvare.

### D-2 · Fauci di Diamante

Lo Xorn Anziano dell'SRD ha già 15 DV (circa 130 pf), CA 25, RD 5/contundente ed è GS 8. Il modulo gli dà 180 pf, CA 28, RD 10/adamantio e GS 11, senza `Boost log:`. Con l'adamantio né Aegis Fang (un'ascia) né i pugni di Tordek passano, e la calibrazione del modulo («la Raffica aggira la RD») non regge. Mancano anche taglia, iniziativa, velocità, caratteristiche e CA di contatto, che serve al Blast.

**Domanda.** Scegli la riduzione del danno di Fauci e fai chiudere il suo statblocco.

| Opzione | Conseguenza |
|---|---|
| **Adamantio** | Resta RD 10/adamantio: lo scontro diventa di Artemis, la calibrazione va riscritta e serve il Boost log |
| **Contundente 10** | RD 10/contundente con 180 pf e CA 28: i pugni di Tordek passano, l'ascia di Thorik no, la calibrazione regge |
| **SRD** | Xorn Anziano dell'SRD puro, GS 8: l'incontro scende verso EL 10 e i PX dei gruppi futuri calano |

**Raccomandata: Contundente 10.** È la versione più forte che tiene in piedi la calibrazione scritta e la lente dei Tier: Tordek ha il suo colpo, e Thorik ha la via B e lo Spaccare da reggere. In ogni caso lo statblocco va completato passando da `npc-villain-boosting`, con tetto EL e `Boost log:`.

### D-3 · Il volo di Artemis in gravità 2×

Il §3 chiede «Volare CD 20 a fine round o precipita», e dice da sé che l'abilità in 3.5 non esiste. La scheda 3.5 di Artemis non ha un modificatore da tirare, e la regola pesa nello scontro con gli Xorn.

**Domanda.** Stabilisci che prova tira Artemis per restare in volo nella gravità doppia.

| Opzione | Conseguenza |
|---|---|
| **DES CD 20** | Prova di Destrezza, come vuole l'SRD per un'abilità che manca: volare nel Piano diventa raro e rischioso |
| **Volare PF1e** | Si usa l'abilità di PF1e (DES più la manovrabilità delle Ali d'Ombra): servono i dati delle Ali, che il modulo non ha |
| **Nessuna prova** | In gravità 2× Artemis vola solo a balzi e atterra a fine turno, senza tiro |

**Raccomandata: DES CD 20.** Resta dentro il 3.5 ed è la più dura. Il peso del Piano diventa vero anche per chi vola, e nella camera di Terros, in gravità zero, la regola non si applica: lì il volo resta suo.

### D-4 · La scala cantata: Diapason o Frequenza

Il canone D34 dice che la scala si alza suonando il Diapason. Il blocco giocato dice che il gruppo l'ha alzata cantando la Frequenza, e che i blocchi sono crollati a metà strada. Un gruppo che vince i Cristalli senza il critico ha la Frequenza ma non il Diapason, e il testo non dice cosa può fare. Lo stesso testo confonde poi «senza Diapason» con «hanno saltato i Cristalli».

**Domanda.** Decidi cosa serve per alzare la scala di pietra sull'oceano.

| Opzione | Conseguenza |
|---|---|
| **Solo Diapason** | Come scritto: col successo semplice si attraversa coi tre ruoli |
| **Basta la Frequenza** | Chiunque abbia vinto i Cristalli alza la scala; il Diapason non serve qui |
| **A metà** | Con la sola Frequenza la scala arriva a metà strada e il resto si fa coi tre ruoli; col Diapason arriva fino al portale |

**Raccomandata: A metà.** È esattamente quello che è successo al tavolo, e premia il successo critico senza lasciare a mani vuote chi ha vinto i Cristalli per la via semplice.

### D-5 · Come si esce dal Piano

Il read-aloud della Scena 10 porta il gruppo dritto nella Sala, e `DEF-2` dice «attraversato a ritroso il portale della Terra». Il modulo non dice da dove si esce, né se c'è il viaggio di ritorno di 2 km che il §5 sembra prevedere («se il party ripassa di qui»). Nel Piano del Fuoco, alla vittoria, si apriva un portale di ritorno sopra la piattaforma.

**Domanda.** Stabilisci da dove e come i PG tornano dal Piano alla Sala.

| Opzione | Conseguenza |
|---|---|
| **Come nel Fuoco** | Alla vittoria si apre un portale sopra l'Altare che porta alla Sala; il ritorno a piedi resta una scelta |
| **A ritroso** | Si rifà la strada, 2 km e circa 2 ore e mezza, con gli eventi del d6 e gli Xorn ritrovati |
| **La soglia** | La soglia del Tempio diventa il portale: si esce dal Tempio senza rifare il salto |

**Raccomandata: Come nel Fuoco.** C'è già il precedente nel Piano del Fuoco, combacia con il read-aloud e con `DEF-2`, e non aggiunge un viaggio che il tavolo non ha giocato.

### D-6 · Il Seme di Varis: voce e firma

Varis parla «col tocco della gemma», ma la clausola 1 dice che firma il primo tocco a pelle nuda. Letto così, chi sente l'offerta l'ha già firmata, e non può più scegliere. La scena dell'ora della pergamena in `DEF-4` fa tenere ad Artemis la gemma col guanto, aspettando una voce che a ≈372 DR non arriva: questo fa pensare che col guanto la voce passi e la firma no.

**Domanda.** Decidi se la voce di Varis arriva anche senza firmare.

| Opzione | Conseguenza |
|---|---|
| **Col guanto** | La voce arriva a ogni tocco, anche col guanto o col panno; firma solo la pelle nuda |
| **Con la vetrina** | La voce arriva già con la visione del bazar, a distanza, prima di qualunque tocco |
| **Voce è firma** | Chi tocca a pelle nuda sente e firma insieme: la scelta si fa prima, senza sentire l'offerta |

**Raccomandata: Col guanto.** Tiene insieme la clausola 1, la scena della pergamena di `DEF-4` e il canone giocato, dove Artemis non ha mai toccato la gemma a mani nude. Va solo confermato che al tavolo, maneggiandola col panno, non abbia sentito Varis.

## Secondo giro

Dopo `VERIFICA.md`: ho chiuso 2 PARZIALE, 4 NUOVI 🟡 e il residuo segnalato. Le 6 voci IN ATTESA DM non le ho toccate.

| Voce | Cosa ho fatto |
|---|---|
| PARZIALE DM#7 «Pelle di Pietra diventerà Forza di Pietra» | Il dialogo di Moradin è giocato e resta com'è. Sotto c'è ora una nota per il DM: la «Forza di Pietra» è la Benedizione «Forza della Montagna», non una quarta Benedizione, e Pelle di Pietra non cambia |
| PARZIALE PT#17 e NUOVO 3, l'ordine della MAPPA T-4 | Nel §7a, una frase dice che la nota della mappa «[dopo aver colpito le Rune di Attracco]» vale per la cattura e non per il salto, e che vince il testo. La mappa non l'ho toccata, perché è copia dell'Atlante |
| NUOVO 1, la minuscola dopo il punto | «Un'Onda ogni volta…» |
| NUOVO 2, la tabella dei poteri Terra che assorbe i PX | Aggiunta la riga vuota prima di «XP Sentinella» |
| NUOVO 4, Artemis a piedi nella Magnetite | La gravità dieci volte cade su chiunque non sia Tordek, che voli o no. Artemis resta prono e vale la sua riga, e così regge anche il perché di D88. È la lettura più dura, coerente con «la stanza divide gli intrusi» e «sei l'unico in piedi» |
| Residuo, Blast «automatico» nella calibrazione del §5 | «~28/colpo, manca solo con l'1 naturale» |

**Verifica.** `misura_craft.py --box`: DEF-1 con 28 box, 0 oltre le 12 righe, 3 con parentesi e 7 con più di un nome, come prima. Nessun box toccato. `validate_modules.py`: 5 master conformi, 0 errori. L'`APPARATO-ARC07-DEF-1` va sempre rigenerato da chi orchestra.

Conteggi dopo il secondo giro: CHIUSO 24 · PARZIALE 0 · IN ATTESA DM 6 · NUOVI chiusi 4 🟡.
