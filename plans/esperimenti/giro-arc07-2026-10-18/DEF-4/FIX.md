# ARC07-DEF-4: correzioni dopo il giro a freddo

Esiti: CORRETTO 16 · DECISIONE DM 6 · RESPINTO 0 · 🟡 lasciati 38

Master: `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`.
Rapporti: DEVELOPER (D), PLAYTESTER (P), DM (M). I doppi sono uniti in una riga.

Verifica dopo le correzioni:

- `misura_craft.py --box`: 35 box, **0 oltre le 12 righe**, come prima. Nessun read-aloud è stato toccato.
- `validate_modules.py`: 5 master conformi, 0 errori. `copertura_scene.py --check`: verde.
- ⚠️ `componenti.py --check` segnala `APPARATO-ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` da rigenerare (`componenti.py --apparato`): le correzioni toccano prove e CD che l'apparato raccoglie. Non l'ho rigenerato perché è un altro file; lo stesso cancello segnala anche l'apparato di DEF-5, che non ho toccato.
- L'SRD in linea non l'ho aperto nemmeno io. I numeri che ho corretto li ho rifatti sulle regole 3.5: *Awesome Blow* vale solo contro un avversario più piccolo; *mind blank* protegge da tutti gli effetti che influenzano la mente, e la presenza terrificante è un effetto di paura che influenza la mente; *comando superiore*, *dissolvi magie*, *àncora dimensionale* e *slay living* hanno tutti la componente verbale; l'armatura completa dà +8 con DES massima +1, quindi le guardie hanno CA 19 (la loro armatura è comune: lo dice il bottino di §8 B).

## I rilievi

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Colpo Devastante sul Treant (D#1, P#2) | 🟠 | CORRETTO | Scena 5, tabella dei Treant, riga «Dentro la tenda»: il Colpo Devastante sul Treant non funziona (SRD, avversario più piccolo; tutti e due Grandi), Zog'tar lo colpisce con l'Attacco Poderoso e tiene il Colpo Devastante per i PG |
| Rinforzi alla tenda: quanti, come combattono, quando smettono (D#2) | 🟠 | DECISIONE DM | il numero e il ritmo delle ondate cambiano l'EL oltre il tetto: decisione 1 |
| Cariche della Collana: il Treant della tenda torna all'alba o no (P#1, M#6) | 🟠 | CORRETTO | vince la scheda della Collana (`DEF-3` §7: «3/g», «I semi tornano all'alba»). L'ultima frase ora dice che le tre cariche sono una riserva sola fino all'alba, e che un Treant solo alla tenda non toglie niente ai due dell'alba. La regola del mese per due Treant insieme di notte resta |
| Re Thorek a 8 pf nella fila del duello (P#3) | 🟠 | DECISIONE DM | se il drago può puntarlo e cosa succede se lo prende è canone del duello: decisione 2 |
| Le richieste rimaste aperte al banco (*silenzio*, pietra di Brynja, *identificare*): si comprano ancora, e a che tacca (P#4) | 🟠 | DECISIONE DM | tocca quello che è successo al tavolo del 25 settembre e il conto delle tacche: decisione 3 |
| Il Seme-Mercato: la scheda sta in un altro master (P#5, M#15) | 🟠 | CORRETTO | Scena 5, «Le dieci pozioni»: una riga di stampa (DEF-1 §6-bis va con questo master), il prezzo della pergamena, il costo di 1 tacca, e il riassunto di quello che *identificare* rivela, preso dalle clausole di DEF-1 senza aggiungere niente. Nuova riga nella tabella dell'orologio (§4), «Identificare il Seme-Mercato», 1 tacca, come dice già DEF-1 |
| Il corno rubato suonato apposta, per attirare il drago (P#6) | 🟠 | DECISIONE DM | dove va il drago cambia il luogo del duello: decisione 4 |
| La vista racconta la serata dal tramonto (M#1) | 🟠 | CORRETTO | §0, «La serata in tre frasi»: una riga in coda che dice che il gruppo di oggi riprende dalla notte con 3 tacche, e rimanda al riquadro sotto |
| Quickstart: fiducia, pozioni, acquisti rimandati a un log esterno (M#4, P#27) | 🟠 | CORRETTO | il rimando ora va alla Scena 5, «Il conto della fucina, come l'ha giocato il tavolo», con il riassunto in una riga (fiducia piena, dotazione dall'alto, 5 *volare* e 4 cure) |
| La lista «un'ora» lascia fuori i numeri della tenda (M#5) | 🟠 | CORRETTO | la lista ora comprende la tabella d'uscita dell'orologio, le rune di Balvar, Grask e «Come torna il drago», «Da dove entrano», la Catena, il ritorno con Balvar o Zog'tar e le Appendici A.2 e A.4. Il tempo dichiarato passa a un'ora e dieci minuti |
| Per la tenda si salta fra quattro punti lontani (M#25) | 🟠 | CORRETTO | con la riga sopra: la lista mette in fila i pezzi della tenda nell'ordine in cui servono. Non ho spostato sezioni, perché il riordino del 2026-09-25 è canone |
| Grask scopre l'atterraggio: cosa fa (M#7) | 🟠 | CORRETTO | Scena 6, variante dall'alto: Grask non grida, va al corno, ed è l'allarme della tenda con il corno entro 1d4 round, la stessa regola che il master dà al primo grido. In quei round lo si ferma con un colpo (6 pf) o con la mano sulla bocca della Via B (FOR grezza CD 16). Nessun numero nuovo |
| Balvar legge i PG prima della soglia: portata, azione, uso (M#8) | 🟠 | DECISIONE DM | quando il potere è attivo decide se l'avviso «il telo a sinistra» arriva: decisione 5 |
| La griglia di M7-C sta in un file esterno (M#12) | 🟠 | CORRETTO | Appendice D, M7-C: un paragrafo «Dove sta chi, se la griglia non è stampata», con le coordinate prese dal file della mappa (soglia, palo, seggio, guardie, Balvar, telo est, telo del glifo, Grask, sacerdote). Grask a N15 è davvero a due quadretti dal seggio |
| Balvar nel *silenzio* lancia incantesimi verbali (D#3, M#11) | 🟡 | CORRETTO | Scena 7, «Tattica»: se qualcuno vola, *comando superiore* al round 1 al posto di *righteous might*, al round 2 *slay living* o *dissolvi magie*, *àncora dimensionale* solo nei primi due round; dal round 3 niente verbale (SRD). In Scena 8 una frase che rimanda lì |
| CA delle guardie 20, l'SRD dà 19 (D#4) | 🟡 | CORRETTO | A.2: CA 19, con il conto. Il bottino di §8 B dice che l'armatura è comune, quindi il punto in più non ha fonte |
| Thorik e le due Presenze (D#5, M#17) | 🟡 | CORRETTO | Scena 8, dopo «Thorik è immune»: lo è anche alla Presenza Minacciosa e alla Presenza Terrificante (SRD, effetti di paura che influenzano la mente; *mente vuota* della Corona da `state.md`). Scena 11, round 1: Thorik non tira |
| Complicazione 3: «se la metà fallisce» contro «riesce se riesce la metà» (D#7) | 🟡 | CORRETTO | ora «se fallisce più della metà del gruppo», la stessa soglia del blocco |
| Orologio: le otto tacche dopo il consiglio o con il consiglio (D#13, P#7, M#26) | 🟡 | CORRETTO | vince §4, su cui è scritto lo stato del gruppo (3 tacche, 5 rimaste). Scena 1 ora dice che il consiglio è la prima delle otto tacche |
| Echo Ledger: Zog'tar «hobgoblin» (D#16) | 🟡 | CORRETTO | «mezzo-ogre», come in A.2 e nella scheda d'entrata |
| GS 17 «oltre il tetto» per un gruppo di 13° (M#20) | 🟡 | CORRETTO | in Scena 11 e in A.1-bis: è il tetto esatto, APL+4. La scelta del DM (D60: il Vecchio solo per il gruppo di 14°, le wyvern per quello di 13°) non cambia |
| Durata dell'invisibilità a piedi: 360 m e «due blocchi» (D#6) | 🟡 | DECISIONE DM | due regole scritte danno risultati diversi, e la lettura SRD ne dà una terza: decisione 6 |
| La pattuglia: il conto dei fallimenti si azzera? (D#8) | 🟡 | lasciato | una seconda pattuglia è una regola nuova |
| Gli orchi della complicazione 3 senza statistiche e tattica (D#9) | 🟡 | lasciato | |
| La banda dello sciamano senza tattica (D#10) | 🟡 | lasciato | |
| I quattro posti di guardia GP1-GP4 mai usati (D#11) | 🟡 | lasciato | |
| *Trasporto vegetale*: tre blocchi o cinque dal margine del campo (D#12) | 🟡 | lasciato | dipende da quanto il bosco si avvicina al centro; il canone D74 dice tre |
| Via A: Intimidire a CD fissa invece che contrapposto (D#14) | 🟡 | lasciato | è una regola della casa non dichiarata; va dichiarata dal DM |
| Vatore senza CA (D#15, P#18) | 🟡 | lasciato | Vatore non ha statblocco per canone (Scena 9) |
| Duello e breccia senza Tempra (D#17) | 🟡 | lasciato | Tempra c'è nella tenda (*slay living*) e con le wyvern |
| L'alba coglie fuori chi rientra in volo o invisibile (D#18) | 🟡 | lasciato | |
| Nascondersi sulla soglia illuminata (D#19) | 🟡 | lasciato | |
| La profezia citata dal re non è quella della targa (P#8) | 🟡 | lasciato | indizio o refuso lo decide il DM |
| Un gruppo che vola salta Durin e la porta (P#9) | 🟡 | lasciato | |
| La mappa persa del consiglio fallito non ha effetto (P#10) | 🟡 | lasciato | |
| Senza fiducia piena, chi compra la magia (P#11) | 🟡 | lasciato | |
| Il tetto «assoluto» e l'eccezione dell'adamantio (P#12) | 🟡 | lasciato | l'eccezione è già scritta e motivata; manca solo «salvo l'adamantio» nella riga del tetto |
| Le rune di Zeth: una tacca o due (P#13) | 🟡 | lasciato | per il gruppo di oggi Zeth è già trovato |
| I 12 minuti d'invisibilità e i blocchi ritentati (P#14) | 🟡 | lasciato | va con la decisione 6 |
| Balvar «conta per la metà del gruppo» (P#15) | 🟡 | lasciato | |
| Cosa mostra *individuazione del magico* sulla tenda (P#16) | 🟡 | lasciato | |
| «La Luce di Lathander in mano» non spiegata (P#17) | 🟡 | lasciato | è un potere dell'Anello di Artemis: non lo invento |
| L'Occhio di Ossidiana «avverte» Zog'tar (P#19) | 🟡 | lasciato | sarebbe un potere d'artefatto nuovo |
| Corno rubato: l'ora di respiro sulla prova delle mura (P#20, M#13) | 🟡 | lasciato | va con la decisione 4 |
| Hald sul camminamento est: può essere il nano che muore (P#21) | 🟡 | lasciato | |
| Leggere la runa nel duello: serve la prova (P#22) | 🟡 | lasciato | |
| Balvar scioglie la Catena: che azione (P#23, M#19) | 🟡 | lasciato | |
| Il drago sulle colline: distanza (P#24) | 🟡 | lasciato | |
| Il rito dà la parola solo a Thorik (P#25) | 🟡 | lasciato | Scena 12, stasera non si gioca |
| Durin: ascia doppia e scudo insieme (P#26, M#24) | 🟡 | lasciato | Durin stasera non combatte; il livello è già una decisione aperta nel Bestiario (D4) |
| Vista: cosa vuole Zog'tar, il runaio senza nome (M#2) | 🟡 | lasciato | |
| Vista: grassetti di servizio, CD senza prova (M#3) | 🟡 | lasciato | |
| Il glifo della custodia: legato ai nani anche lui (M#9) | 🟡 | lasciato | |
| La runa gemella del corno nel conto delle quattro (M#10) | 🟡 | lasciato | |
| Il dono a metà di Hella dipende da DEF-3 (M#14) | 🟡 | lasciato | |
| La scheda di Hella: druida di 12° e la stabilità (M#16) | 🟡 | lasciato | `state.md` dice Ranger 1 / Druido 12; la razza (nana del sogno) e la stabilità vanno guardate sulla scheda |
| Le campane: coprono il drago o tolgono la sorpresa (M#18) | 🟡 | lasciato | |
| Nessun box per la runa vista sulla scaglia (M#21) | 🟡 | lasciato | prosa nuova, fuori da queste correzioni minime |
| B4 e la regia della serata sono in volumi esterni (M#22) | 🟡 | lasciato | |
| Grask, il sacerdote, Hrodgar e Hald senza ritratto (M#23) | 🟡 | lasciato | |

Una cosa trovata fuori dal mio file: `Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md` dà ai giavellotti di Zog'tar **+20**, A.2 dice **+19**. Non l'ho toccato.

## Decisioni per il DM

### 1 · I rinforzi alla tenda (D#2)

Il master dice quando arrivano le ronde (1d4+2 round) e gli squadroni (2d4+2), ma non quanti, come combattono, né quando smettono. Lo scontro con Zog'tar è costruito per durare (283 pf), quindi i rinforzi arriveranno spesso a scontro aperto, con la tenda già a EL 17.

**La domanda**: decidi quanti rinforzi arrivano alla tenda, e con quale ritmo.

| Opzione | Conseguenza |
|---|---|
| **Un'ondata** | arrivano una ronda e uno squadrone (statistiche A.6), circondano la tenda e tagliano l'uscita: lo scontro sale sopra il tetto una volta sola |
| **Ondate continue** | dal primo arrivo, un'altra ronda ogni round e uno squadrone ogni due: chi resta nella tenda è sommerso, ed è «combattere l'orda» alla lettera |
| **Fuori, non dentro** | i rinforzi non entrano finché Zog'tar combatte (le guardie lo guardano, e lui non vuole aiuto); fanno quadrato fuori e aspettano chi esce |

**Raccomandata: Ondate continue**, con la regola di «Fuori, non dentro» finché Zog'tar è in piedi. È la versione più dura e la più fedele alla frase che c'è già («chi resta oltre il loro arrivo combatte l'orda»), e lascia il tetto EL 17 allo scontro col generale, come per il drago sulla tenda (EL 18-19, «voluto dal DM»).

### 2 · Re Thorek nella fila del duello (P#3)

Il drago «cala sul cortile dove sta il re» e vuole uccidere un secondo re davanti all'orda. Con un successo solo sulle mura il re ha 8 pf, nella fila dei PG (M7-B, L16). Il master dice solo «nessun malus meccanico». Alla Scena 12 il re è vivo, e la timeline è auto-consistente (§6).

**La domanda**: decidi se Skullcrusher può prendere di mira il re, e cosa succede.

| Opzione | Conseguenza |
|---|---|
| **Fuori bersaglio** | il soffio e gli attacchi non lo prendono mai; resta pressione emotiva, come scritto |
| **Lo punta** | se nessun PG lo chiama per nome in un round, il drago va sul re; chi si mette in mezzo prende il colpo. Il re non muore, perché è vivo alla Scena 12: cade a terra stabile, e il Rubino lo ricorda come «il re è caduto» |
| **Lo punta, e il re paga** | come sopra, ma un re caduto costa anche un successo in meno al tono del Rubino e un nome in più fra i caduti del 372 (la sua guardia) |

**Raccomandata: Lo punta.** È la versione più terrificante che il canone permette: dà al «Prossimo passo» del drago un effetto sul tavolo, obbliga i PG a scegliere fra il drago e il re, e non contraddice la Scena 12.

### 3 · Le richieste rimaste aperte al banco (P#4)

Al tavolo del 25 settembre il gruppo ha chiesto pergamene di *silenzio*, la pietra di Brynja e *identificare*, ma il conto della fucina non le mette fra gli acquisti. La variante dall'alto conta sulla bolla di *silenzio*, e la tacca della fucina è già segnata.

**La domanda**: stabilisci se stanotte le richieste aperte si comprano ancora, e quanto costano.

| Opzione | Conseguenza |
|---|---|
| **Tacca già pagata** | si chiudono all'inizio della serata, dentro la tacca della fucina già segnata; si pagano in monete |
| **Tacca nuova** | tornare in cappella o in bottega costa 1 tacca (4 segnate prima di uscire), e con il volo Grask dorme |
| **Non comprate** | il tavolo non le ha prese: la notte parte senza *silenzio* né *identificare* |

**Raccomandata: Tacca già pagata.** Erano richieste fatte al banco quella sera, e il master le scrive con la risposta del banco; farle pagare di nuovo punisce il giro della fortezza, che §4 vuole premiare («guardarsi intorno»). Il costo vero resta: l'ora per identificare il Seme è 1 tacca (DEF-1), e le cure comprate pesano sul dado dei caduti.

### 4 · Il corno rubato, suonato apposta (P#6)

Il master spiega ai PG che il corno obbliga il drago a tornare. Un tavolo che lo ruba lo suonerà per attirare il drago lontano o in un'imboscata. Il master copre solo «rubato o rotto» (il drago arriva tardi e furioso) e l'allarme.

**La domanda**: decidi dove va il drago quando i PG suonano il corno rubato.

| Opzione | Conseguenza |
|---|---|
| **Al corno** | la Catena lo tira verso il corno, dovunque sia; arriva in 70 round, sa chi lo ha chiamato e va prima su chi lo tiene |
| **Al campo** | la Catena lo riporta al campo come sempre; il corno lontano lo fa solo arrivare prima, e il duello resta all'alba |
| **Al corno, una volta sola** | la prima volta va al corno; dopo, il drago ha capito e non risponde più fino all'alba, quando arriva furioso come per il corno rubato |

**Raccomandata: Al corno.** È la lettura più forte della frase già scritta («la Catena tira e Skullcrusher deve tornare»), premia un'idea specifica del tavolo come vuole §0-ter, e il rischio è vero: il drago arriva sapendo chi lo ha messo al guinzaglio, e va su di lui come su chi dice la Catena ad alta voce. Con questa scelta va decisa anche la riga «ora di respiro» della Scena 10 (P#20, M#13).

### 5 · Quando Balvar legge i PG con il Fuori-Posto (M#8)

L'avviso *«Non la soglia. Il telo a sinistra.»* decide se si entra con la sorpresa. Il master dice che Balvar li legge «comunque», ma il Fuori-Posto è «come *individuazione del magico*», 3 al giorno: per l'SRD vuol dire un cono di 18 m, concentrazione, 1 minuto per livello. Non è scritto se è già attivo quando arrivano.

**La domanda**: decidi se Balvar ha il Fuori-Posto attivo quando i PG si avvicinano.

| Opzione | Conseguenza |
|---|---|
| **Già attivo** | ha speso un uso aspettando gli esploratori; il telo non ferma il cono, e chi entra nei 18 m è letto: l'avviso arriva sempre |
| **A un segnale** | lo attiva solo se sente qualcosa: Ascoltare +5 contro il Muoversi Silenziosamente di chi atterra o si avvicina; senza segnale, niente avviso |
| **Al primo round** | lo attiva quando un PG è già alla soglia: l'avviso arriva solo a chi si ferma lì un round |

**Raccomandata: Già attivo.** Il master lo dice in tre punti («li vede comunque», «Balvar li legge comunque», la tabella delle tattiche), le due incursioni naniche fermate in dieci notti spiegano perché tiene un uso pronto, e l'avviso è la leva della Scena 7. La versione più dura è «A un segnale», ma toglierebbe la scena al gruppo che fa tutto bene.

### 6 · Quanto dura l'invisibilità del re a piedi (D#6, con P#14)

Il master dice 3 m a round, cioè 360 m in 12 minuti, «i primi due blocchi»; ma i blocchi sono da 200 m, e la regola subito dopo dice che il blocco in cui l'invisibilità finisce si tira a Nascondersi. Con la lettura SRD (metà velocità per ogni azione di movimento, 6 m a round) i blocchi coperti sarebbero tre. Vale solo per i gruppi a piedi con la dotazione dal basso, non per il gruppo di oggi.

**La domanda**: scegli quanti blocchi copre l'invisibilità del re a piedi.

| Opzione | Conseguenza |
|---|---|
| **Uno** | 3 m a round, 360 m: il primo blocco a Muoversi Silenziosamente, dal secondo Nascondersi, come vuole la regola del blocco in cui finisce |
| **Due** | si tiene «i primi due blocchi» e si toglie la regola del blocco in cui finisce, per la pozione del re |
| **Tre** | lettura SRD, 6 m a round: tre blocchi coperti, e il quarto si tira a Nascondersi |

**Raccomandata: Uno.** È la versione più dura, e l'unica in cui le due frasi già scritte non si contraddicono. Per i blocchi ritentati (P#14) i minuti continuano a scorrere: un blocco fallito consuma la sua parte d'invisibilità come uno riuscito.

## Secondo giro

Esiti: CORRETTO 6 (PARZIALE 3, NUOVI 3) · IN ATTESA DM 5, non toccati

Dopo le correzioni `misura_craft.py --box` dà ancora 35 box per DEF-4, **0 oltre le 12 righe**; `validate_modules.py` è verde. Nessun read-aloud toccato. L'apparato di DEF-4 resta da rigenerare (`componenti.py --apparato`), come nel primo giro.

| Voce di VERIFICA.md | Gravità | Esito | Cosa ho fatto |
|---|---|---|---|
| NUOVO 1 · la variante dall'alto conta ancora le cariche alla vecchia maniera (chiude anche il PARZIALE P#1 · M#6) | 🟠 | CORRETTO | Scena 6, «Chi vola, e chi no»: richiamare Durik alla tenda è una carica della notte, all'alba i semi tornano tutti e tre, e dopo i due Treant dell'alba ne resta una per richiamarlo nel duello. Ora variante, Scena 5 e `DEF-3` §7 dicono la stessa cosa |
| NUOVO 2 · il rimando di Grask alla Via B dice «qui sotto» | 🟡 | CORRETTO | ora «più sopra»: la Via B sta nella complicazione 6, prima della variante |
| NUOVO 3 · le ore della Scena 1 non tornano più | 🟡 | CORRETTO | «le prime quattro ore se ne vanno fra l'arrivo e la porta, poi il consiglio apre l'orologio»: 4 ore più 8 tacche, consiglio compreso, fanno le dodici ore dichiarate. Resta una sfumatura in §4 («Dal tramonto all'alba ci sono 8 tacche», mentre l'arrivo è un quarto d'ora prima del buio): non l'ho toccata, perché lì il conto è canone del DM e torna con le 3 tacche del gruppo di oggi |
| PARZIALE M#5 · le due cose della Scena 5 senza minuti | 🟠 | CORRETTO | §0, «La vostra serata»: una riga dà loro 10 minuti, da leggere prima della lista |
| PARZIALE M#25 · al tavolo la tenda resta in quattro posti | 🟠 | CORRETTO | Scena 7, «Da dove entrano decide come comincia»: un riassunto di cinque righe con quello per cui il DM tornava alla Scena 6 (la runa della soglia, il glifo sopra il seggio con la sua CD, il telo est, dove sta Grask e quando dorme). I numeri sono quelli della Scena 6, non ne ho aggiunti |
| IN ATTESA DM (D#2, P#3, P#4, P#6, M#8) | 🟠 | non toccate | restano le decisioni 1-5 qui sopra. La parte di M#15 che chiedeva se la pergamena è stata comprata dipende dalla decisione 3 |
