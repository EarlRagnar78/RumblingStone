# ARC07-DEF-2 · giro 2 · le correzioni

Esiti: CORRETTO 18 · DECISIONE DM 12 · RESPINTO 4 · 🟡 lasciati 9

Master corretto: `07_il Portale Della Forgia Eterna/ARC07-DEF-2-RITORNO-E-AFFRESCHI.md`.
Rapporti: DEVELOPER (DEV), PLAYTESTER (PT), DM. I rilievi doppi sono uniti nella stessa riga.

Verifiche dopo le correzioni: `misura_craft.py --box` dà per DEF-2 31 box, 0 oltre le 12 righe, 0 parentesi, 0 con più di un nome, 0 oltre le quattro frasi, 0 oltre i 500 caratteri. `validate_modules` è verde (0 errori), come `domande_developer --check` (18 rilievi, tutti dichiarati), `copertura_scene --check` (15, tutti dichiarati), `test_storico.py` (8 passati) e `componenti --check`.

⚠️ `componenti.py --apparato` rigenera tutti gli apparati. Oltre a quello di DEF-2 ha riscritto una riga di `APPARATO-ARC07-DEF-5-RITORNO-HAMMERFIST.md`, perché il master DEF-5 era già stato modificato dall'agente che lo corregge. Il file nuovo è quello che il suo master genera adesso, e `--check` lo voleva così. Il master DEF-5 non l'ho toccato.

## I rilievi

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Il +1 della Stanza non si somma ad A1 né alla Risonanza, e il «ritual-master» non esiste in `DEF-3` (DEV#1) | 🟠 | DECISIONE DM | D1 qui sotto. Il rito del `DEF-3` non ha un ritual-master: l'unico TS è quello dello Step 5, e lo tirano tutti e tre |
| Sala o Stanza: «pagando otto ore in più per un +1» contro «si prende anche senza dormirci» (DEV#2) | 🟠 | CORRETTO | §6: tolto «per un +1». Adesso il testo dice che cosa si paga (otto ore, i sogni della Sala tranne quello di Hella) e che il +1 si prende col tocco, ovunque dormano |
| Lo spirito di Hella in due posti (DEV#3, PT#6, DM#14) | 🟠 | CORRETTO | §1: lo spirito ha attraversato l'Incudine del Mondo (`state.md` r.20, «viaggio spirituale… nell'Incudine del Mondo») e ora è trattenuto nel Sogno della Terra dalle radici del Voto (`DEF-3` §6, `state.md` [DEBITO DELLA RADICE]). I due nomi erano il viaggio e il luogo. In «Se lo divinano» ho aggiunto la riga sullo spirito |
| Da dove si esce dalla Forgia per cercare un tempio (DEV#4, PT#3) | 🟠 | DECISIONE DM | D2. La geografia fuori dalla Sala non sta in nessun file di ARC-07 né in ARC-06 |
| Benedizioni: quando hanno pregato l'ultima volta, e se sono ancora attive (PT#1, DEV#12) | 🟠 | DECISIONE DM | D3. L'ultima preghiera è quella della partenza per la Terra (`DEF-1` §2), ma le ore vissute nel Piano nessuno le ha contate |
| Quanto costa all'orologio il tempo da svegli (PT#2, DM#17) | 🟠 | DECISIONE DM | D4. Il canone ha solo le due tariffe del sonno |
| Therysol: che cosa sa fare (PT#4, DM#20) | 🟠 | CORRETTO | Scena 1: un paragrafo con gli incantesimi della scheda (`Bestiario/png/Therysol/Therysol/Therysol.md`, «Incantesimi Conosciuti & Slot»): cura ferite leggere 3/g, moderate 2/g, ristorazione inferiore, aiuto, benedizione. Non divina e non rianima. Ho usato gli slot senza le perle |
| I PG con ore libere: forgiare, mandare messaggi, rimedi (PT#5) | 🟠 | CORRETTO in parte · DECISIONE DM | Scena 1: tabella **Chi si trova qui** con le sei righe (C7 verde). Resta aperto se i PG possono lavorare alla Forgia Eterna: D5 |
| La vista non mostra la serata (DM#1, DEV#13) | 🟠 | CORRETTO | §0: riquadro «🧭 La serata in tre frasi» prima della tabella, nella forma di `DEF-4`. `ricordo_lettura.intenzione` lo legge per primo |
| 66 minuti di lettura, e nessuna durata (DM#5) | 🟠 | CORRETTO | Tabella «In trenta secondi»: due righe nuove, «Quanto dura» (stima per scena, e quando cominciare a tagliare) e «Se hai un'ora per prepararti» (cosa leggere prima). Le durate sono una stima di regia, non canone |
| Lo stato d'ingresso dipende dal `DEF-1`, e «hanno fatto il rito» (DM#6) | 🟠 | CORRETTO | «Stato al tavolo» diceva «hanno fatto il rito», ma in `state.md` la resurrezione non è giocata (righe 26, 93, 95). Vince `state.md`: adesso il testo dice che hanno giocato fino al sonno. In §0 ho aggiunto la tabella «Con che cosa arrivano dal `DEF-1`», con gruppo di oggi e gruppo nuovo, da `state.md` [MARCHIO DI VARIS] e `DEF-1` §6-bis |
| Il bazar del sogno di Artemis (DM#7, PT#8) | 🟠 | CORRETTO | §7-bis: il bazar è la vetrina di Varis, giocata (`DEF-1` §6-bis, «La visione del bazar (giocata)»). Per un Artemis nuovo che non l'ha vista c'è un box di una riga che prende il posto del primo. La variante del Seme portato da Artemis resta 🟡 |
| H1 tratto dalla S-1, che porta dati da DM (DM#8, PT#15) | 🟠 | CORRETTO | §11: scritto che cosa resta su H1 (ottagono, titoli, punti cardinali, Altare, P1) e che cosa si toglie |
| La Visione si ritenta subito? (DEV#5, DM#11) | 🟡 | CORRETTO | §5: «Stasera non si ritenta.» Il testo diceva già «ritentabile dopo la resurrezione». L'innesco nella finzione (DM#11, seconda metà) resta 🟡 |
| Riga di scala della Visione e ruoli senza giocatore (DEV#6) | 🟡 | lasciato | Chiede soglie nuove per due e quattro PG: è una regola da decidere, non una riga |
| N3: come arriva il «conta quattro» (DEV#7) | 🟡 | CORRETTO | §4, A6: il portale pulsa quattro volte sotto la mano, e il quarto battito è più debole. È un dettaglio sensoriale, che la coerenza §1 permette di aggiungere; il DM può toglierlo. Corretto anche un rimando sbagliato: la porta fisica è di N3, il testo diceva N2 |
| N4: Conoscenze (storia) CD 20 senza gradi (DEV#8) | 🟡 | DECISIONE DM | Dentro D6, perché le CD del §4-bis sono `[INFERRED]` |
| *Comunione*: cinque parole al massimo (DEV#9) | 🟡 | CORRETTO | «Se lo divinano»: sul tempo, *comunione* risponde «sì», *divinazione* dà la frase di N6 (SRD, *commune*: sì, no, non chiaro, o una frase di cinque parole). La riga sul pollice del sogno di Artemis resta 🟡 |
| Benedizione della Cronaca: il tema di A4, l'abilità per «leggere» (DEV#10, DM#13) | 🟡 | lasciato | Il tema di A4 e l'abilità per leggere vanno decisi. Anche qui c'è il problema delle Conoscenze senza gradi |
| A6: due abilità o una (DEV#11, PT#9, DM#19) | 🟡 | CORRETTO | Quick-Reference allineata al testo, che lo scrive due volte (§1, §4): Sapienza Magica CD 18 |
| L'anello sigillo: è magico? Chi lo identifica? (PT#7) | 🟡 | lasciato | Non è sicuro che il +2 di circostanza sia solo sociale |
| A8 si ripete se riportano il corpo? (PT#10) | 🟡 | lasciato | Per A3 il limite è scritto, per A8 andrebbe deciso |
| Il muro della Stanza: numeri non SRD, spessore, che cosa succede alla Cronaca (PT#11) | 🟡 | RESPINTO in parte | I numeri sono quelli di ARC-06, già giocato: `06_…/Tactics_and_maps.md` r.54, «hardness 8, 360 hp per 10 ft. section, break DC 35». Non si cambiano. Che cosa succede alla Cronaca se rompono la parete resta aperto |
| A7: fra 2g 00h e 2g 07h l'immagine anticipa la breccia (PT#12) | 🟡 | CORRETTO | §0-bis: l'affresco mostra l'ultima riga che l'orologio ha raggiunto, e la breccia solo sotto i due giorni |
| Tordek senza scelte nelle Scene 2 e 4 (PT#13) | 🟡 | RESPINTO | È una scelta dichiarata del beat (§1, «Non è il protagonista degli affreschi, ed è giusto così»). Tordek ha il sogno dello zaino e la conversazione con Artemis (§7-bis) |
| PX della Visione se il TS fallisce (PT#14) | 🟡 | lasciato | È una regola di premio da decidere |
| Cornici: chi perde le Benedizioni (PT#16) | 🟡 | CORRETTO | §8: «a chi ci ha provato», come dice la frase dopo («Un Custode che ruba…») |
| La vista prende Karrn per l'avversario (DM#2) | 🟡 | CORRETTO | Il riquadro della serata nomina l'avversario: l'orologio di A7 |
| La vista non mostra cosa stampare (DM#3) | 🟡 | lasciato | Il riquadro sta in tre frasi, e «Cosa stampare» è subito sotto |
| I grassetti della vista, «In scena» e «Comparse» (DM#4) | 🟡 | RESPINTO | «In scena» e «Comparse» li impone ADR-0073 a ogni scena. I grassetti di lavorazione stanno nel blocco `apparato`, che non va in stampa |
| H4 è un PDF esterno, H3 non ha immagine (DM#9) | 🟡 | CORRETTO | §7: se il PDF non c'è, le carte si scrivono dalla tabella. Il simbolo di H3 è descritto nel box di A8 |
| Gli altri artefatti sulle pareti, la voce dei Bracieri (DM#10) | 🟡 | lasciato | Scriverli vuol dire inventare reazioni d'artefatto (coerenza §2.1) |
| Due regole sui bonus degli affreschi (DM#12) | 🟡 | CORRETTO | §3: il tetto di un solo bonus vale per le meditazioni; i doni di A3 e A8 si prendono lo stesso, e per ogni tiro vale il sacro più alto, come dice il box PF1e. La durata del +1 «a un tiro» resta 🟡 |
| A1 chiama Artemis «figlio nanico» (DM#15) | 🟡 | CORRETTO | Box 2 di A1: «Lavora per proteggere figli che ancora non esistono.» La riga è più corta, e cade la spiegazione «cioè voi» |
| Karrn, Belkram, gli Yochlol, Urialle senza spiegazione (DM#16) | 🟡 | RESPINTO | Sono la storia di ARC-06 che i giocatori hanno vissuto. Stanno nei Dati per il DM e nella legenda della S-2, che rimanda al file di ARC-06 |
| I salti per A7, la Stanza, le tariffe (DM#18) | 🟡 | lasciato | Per toglierli bisogna spostare sezioni, e questo giro non riordina il master |

## Decisioni per il DM

### D1 · Il +1 della Stanza della Corona

Chi tocca l'incisione della druida guadagna «+1 sacro al primo TS del ritual-master» (D36 e). Nel rito del `DEF-3` però non c'è un ritual-master: l'unico TS è quello di Volontà dello Step 5, e lo tirano tutti e tre. In più chi ha meditato davanti ad A1 ha già +1 sacro a tutti i TS per 24 ore, e i bonus sacri non si sommano (box PF1e del §0-bis): per chi ha fatto A1 il tocco non conta niente.

**Domanda:** decidi chi riceve il +1 della Stanza e se si somma.

- **Senza tipo** · +1 al TS dello Step 5 di ogni PG che ha toccato l'incisione, che si somma a tutto.
- **Sacro com'è** · +1 sacro al TS dello Step 5 di chi l'ha toccata; per chi ha meditato davanti ad A1 non conta.
- **Sacro a tutti** · il primo che la tocca dà +1 sacro al TS dello Step 5 di tutti e tre; non si somma ad A1.

**Raccomandata: Senza tipo.** È la versione più forte, e la scelta di scendere nella Stanza compra qualcosa. Diverge dall'SRD soltanto perché un dono divino senza tipo è raro, e lo si scrive. Va aggiunto anche nella tabella dello Step 5 del `DEF-3`, che oggi non lo nomina.

### D2 · Da dove si esce dalla Forgia

Il §8 prevede che i PG escano a cercare un chierico o un tempio, ma la sola uscita della mappa è la Stanza della Corona. La S-2 dice che l'ingresso sud della Stanza porta alla Sala, e il portale drow è sigillato. Nessun file di ARC-06 o ARC-07 dice dove si arriva uscendo né quanto si cammina.

**Domanda:** stabilisci se i PG possono uscire dalla Forgia prima del rito, e dove.

- **Porta chiusa** · finché il ciclo non è compiuto, dalla Forgia si esce solo dai portali dei Piani. «Cercano un'altra via» diventa una scena di dialogo con Therysol e la Sala.
- **Sottosuolo con prezzo** · si esce dalla Stanza per la strada di ARC-06, e il primo tempio è a più di due giorni: chi ci va scende sotto la soglia del §8, con il pannello velato e la Fase 0 dura.
- **Sottosuolo giocato** · si esce, e un lotto nuovo scrive viaggio, abitato e incontri con le loro tattiche.

**Raccomandata: Sottosuolo con prezzo.** È la versione più terrificante, e si regge sulle regole che il master ha già (−12 h a sonno, la soglia dei 2 giorni). Non chiede incontri nuovi: il prezzo è l'orologio, e l'incantesimo comunque fallisce (§8).

### D3 · Le Benedizioni all'arrivo

Le Benedizioni durano 24 ore vissute e si rinnovano una volta ogni 24. L'ultima preghiera è quella della partenza per la Terra (`DEF-1` §2), e le ore vissute nel Piano non le ha contate nessuno. Il master consegna H4 «a preghiera finita», quindi si aspetta un rinnovo.

**Domanda:** stabilisci se all'arrivo nella Sala la preghiera rinnova le Benedizioni.

- **Scadute** · all'arrivo sono spente, e la preghiera le rinnova: si consegna H4.
- **Contate** · si contano le ore vissute dalla preghiera della partenza, e se non sono 24 l'Altare tace.
- **Ancora attive** · durano fino al prossimo sonno, poi la preghiera del mattino le rinnova.

**Raccomandata: Scadute.** Il Piano della Terra è stato un giorno intero di marcia e di scontri, e la scena dell'Altare con H4 esiste per questo. Le altre due chiedono un conto che il tavolo non ha.

### D4 · Il tempo da svegli nella Sala

L'orologio scende solo con il sonno: −4 h nella Sala, −12 h fuori. Il rito del `DEF-3` conta un'ora, e da lì il tempo si conta tutto (`DEF-3`, `[CANONE — DM 2026-10-18]`). Prima del rito nessuno dice quanto costa un pomeriggio passato davanti agli affreschi.

**Domanda:** decidi quanto costano all'orologio le ore da svegli nella Sala.

- **A metà** · nella Sala il tempo scorre più lento anche da svegli: due ore vissute costano un'ora all'orologio.
- **Per intero** · ogni ora da svegli costa un'ora, e lo sconto vale solo per il sonno.
- **Gratis** · conta solo il sonno, come scrive oggi il master.

**Raccomandata: A metà.** Viene dalla stessa regola della Sala, «il tempo vi scorre più lento», e tiene un prezzo per chi indugia. Per il gruppo di oggi non cambia niente: il registro giocato è canone.

### D5 · La Forgia Eterna come bottega

I PG hanno ore libere accanto alla Forgia Eterna, con due guerrieri e i Bracieri. Vorranno riparare o migliorare le armi. Il canone ha la Forgia che riforgia nei riti (l'Anello, Durik), mai su richiesta.

**Domanda:** decidi se i PG possono lavorare il metallo alla Forgia Eterna.

- **Solo riti** · la Forgia arde per Moradin. Chi ci mette un'arma senza un rito la ritira intatta e fredda.
- **Artigianato SRD** · si lavora come a una forgia normale, con i tempi dell'SRD, e il tempo paga l'orologio (D4).
- **Forgia divina** · Artigianato con un bonus sacro, e i tempi si dimezzano.

**Raccomandata: Solo riti.** Tiene i poteri d'artefatto dentro le schede (coerenza §2.1) e non apre una bottega che il beat non regge. Se un giocatore insiste, c'è la contingenza del gesto per la Cronaca (§8).

### D6 · Le CD nuove della rete della Sala (`[INFERRED]` nel §4-bis)

Le Letture di N1, N2 e N4 hanno CD nuove: Conoscenze (religioni) CD 15 per N1 e N2, Conoscenze (storia) CD 20 per N4. Nessuno dei PG ha Conoscenze (storia) di classe, e una prova di Conoscenze senza gradi arriva al massimo a CD 10 (SRD, *Knowledge*): la porta della prova di N4 è chiusa.

**Domanda:** conferma le CD del §4-bis, e scegli una porta di prova che i PG possano usare per N4.

- **Confermate** · le CD restano. N4 si apre da Aegis Fang ad A7 e dalla prova di chi ha i gradi.
- **N4 per Sapienza Magica** · la Lettura di N4 diventa Sapienza Magica CD 20 sull'aura di A6, che Artemis può tirare.
- **N4 senza gradi** · una prova di Intelligenza CD 10 per un nano: è la storia della sua gente.

**Raccomandata: N4 per Sapienza Magica**, confermando le altre due CD. È la porta più difficile che resta aperta, e la dà al PG che A6 ha già al centro.

### D7 · L'ordine dei tagli (`[INFERRED]` in §0)

Il master dice di tagliare A4, A5, la lettura di Artemis su A6 e la Stanza, e di non tagliare mai A7, A3 e il sogno di Hella.

**Domanda:** conferma che cosa non si taglia mai, se manca tempo.

- **Confermato** · A7, A3 e il sogno di Hella restano sempre.
- **Anche A8** · si aggiunge la manifestazione di Hella, che consegna H3 e la Ghianda.
- **Solo A7** · resta solo l'orologio; tutto il resto si può tagliare.

**Raccomandata: Anche A8.** È l'unico momento in cui la giocatrice di Hella vede il suo PG prima del sogno, e porta la Ghianda che serve al `DEF-3` (§10 B).

### D8 · Il ricordo di Thorik dipinto su A3 (`[INFERRED]` in §4)

Prima del TS, il giocatore di Thorik racconta che cosa rivede per primo. La parete lo dipinge, e da quel momento chiunque passi davanti ad A3 lo vede.

**Domanda:** conferma che l'invenzione del giocatore resta dipinta su A3, per tutti.

- **Per tutti** · il ricordo diventa pubblico, ed è il prezzo dello yes-and.
- **Solo per Thorik** · la parete lo dipinge, ma lo vede solo chi porta la Corona.
- **Fino al rito** · resta finché Hella torna; dopo, A3 aggiunge la scena di Hella viva.

**Raccomandata: Per tutti.** È la versione con i denti, e il ricordo più intimo del portatore diventa una cosa che gli altri possono nominare.

### D9 · I Dipinti Invisibili (`[INFERRED]` nel §4-bis)

Nella Stanza restano i Dipinti Invisibili di ARC-06 (J11-J12), e nessun file del repo dice che cosa siano. Il master li lascia muti e rimanda la decisione al DM.

**Domanda:** decidi se e quando i Dipinti Invisibili si aprono.

- **Muti in ARC-07** · stasera non dicono niente, e la loro scena si scrive più avanti, quando servirà.
- **Si aprono al rito** · si accendono quando Hella torna, e mostrano la sua morte vista dalla Stanza.
- **Mai** · sono decorazione di ARC-06 e restano tali.

**Raccomandata: Muti in ARC-07.** Non inventa contenuto e lascia un filo aperto. Chi li esamina stasera li trova muti, e anche questo è un'informazione.

### D10 · «Se lo divinano» (`[INFERRED]` nel §4-bis)

La tabella dice che cosa ottengono *parlare con i morti*, *comunione*, *divinazione*, *leggende e tradizioni* e *individuazione del magico*. Ho aggiunto in questo giro la riga sullo spirito di Hella e ho messo la risposta sul tempo nel limite SRD di *comunione*. Thorik ha *Comunione* 1/mese dalla Corona (`state.md`, Mantle of Stone and Spirit), quindi la tabella si userà.

**Domanda:** conferma le risposte della tabella «Se lo divinano».

- **Confermate** · valgono tutte le righe, compresa quella nuova sullo spirito.
- **Più avare** · Moradin risponde «non chiaro» a tutto ciò che riguarda il rito, finché non comincia.
- **Più generose** · *comunione* sul rito dice anche che serve il dono di ognuno.

**Raccomandata: Confermate.** Premiano chi lancia senza rompere la sorpresa del `DEF-3`, come chiede la §9 del developer.

### D11 · Il gesto inventato per la Cronaca (`[INFERRED]` nel §8)

Se i PG incidono un nome, lasciano un'offerta o giurano davanti a una parete, la Sala lo incide su A8 la notte stessa. Se era un giuramento e lo rompono, Moradin non gira più la testa ad A1.

**Domanda:** conferma che i gesti dei PG entrano su A8, con il prezzo del giuramento.

- **Confermato** · il gesto entra su A8, e il giuramento rotto spegne A1.
- **Senza prezzo** · il gesto entra su A8, e non succede niente se lo rompono.
- **Prezzo più alto** · un giuramento rotto vela anche il pannello di A8, come l'orologio sprecato.

**Raccomandata: Prezzo più alto.** È la versione più dura e usa una conseguenza che il master ha già, il pannello velato del §8.

### D12 · Dove sta il corpo di Hella (`[INFERRED]` nella legenda della S-1)

La mappa mette il corpo accanto all'Altare, sul lato sud, e lo porta davanti ad A8 solo per la manifestazione. Il resto del testo dice soltanto «accanto all'Altare».

**Domanda:** conferma il corpo di Hella sul lato sud dell'Altare.

- **Lato sud** · come sulla mappa: il corpo guarda verso A8, ed è coerente con N1.
- **Davanti ad A8** · il corpo sta già sotto la tela, e la manifestazione parte appena arrivano.
- **Lato nord** · il corpo sta verso il Portale P1, e il giro verso sud diventa più visibile.

**Raccomandata: Lato sud.** Regge l'indizio di Therysol («si gira ancora verso sud») senza anticipare la manifestazione.

## Seconda passata

Esiti: CORRETTO 4 · DECISIONE DM 2 · RESPINTO 0

Questa volta `componenti.py --apparato` non l'ho lanciato. Gli altri gate sono verdi: box (31, 0 oltre le 12 righe), validate_modules, domande_developer, copertura_scene e test_storico. `componenti --check` boccia un solo file, `APPARATO-ARC07-DEF-1-PIANO-TERRA-TERROS.md`: il master DEF-1 lo sta cambiando un altro agente, e quell'apparato lo rigenera chi orchestra. Il master DEF-2 cambia l'apparato di DEF-2 solo nella riga di Therysol.

| Voce della verifica | Esito | Cosa ho fatto / perché |
|---|---|---|
| PT#5 · PARZIALE, lavorare alla Forgia Eterna | DECISIONE DM | Senza canone la risposta non c'è: resta D5. La tabella «Chi si trova qui» risponde a tutto il resto |
| DM#6 · PARZIALE, i fatti d'ingresso che mancavano | CORRETTO | Nella tabella «Con che cosa arrivano dal `DEF-1`» ho aggiunto due righe. Quello che Artemis ha detto a Tordek è canone ma nessun file lo scrive, quindi il DM lo chiede ai due giocatori prima di cominciare. La luce verde dell'eco E-07f è vissuta dal gruppo di oggi (`state.md` §7.E); per un gruppo nuovo che non l'ha avuta, il sogno delle mani fredde resta lo stesso. Le Benedizioni restano D3. I pf restano «come a fine Terros», perché nessun file ha il numero |
| NUOVO 1 · Therysol, il conto degli slot | CORRETTO | Ora c'è il conto della scheda: tre incantesimi di 1° e due di 2° al giorno, cinque e quattro con le perle, scelti dalla lista |
| NUOVO 2 · «Non ha divinazioni» | CORRETTO | Le sue divinazioni sono *individuazione del magico* e *guida*. Sugli affreschi vale la riga di «Se lo divinano», e dello spirito non sa niente |
| NUOVO 3 · nomi di file nel testo stampato | CORRETTO | `state.md` (Stato al tavolo) e `Bestiario/png/Therysol` adesso stanno in `<!-- apparato -->` inline, come gli altri rimandi del master |
| NUOVO 4 · aggiunte senza tag | DECISIONE DM per il portale · niente tag per le altre due | Il portale che pulsa quattro volte è un dettaglio inventato: lo marco `[INFERRED — needs DM confirmation]`, ed entra in D13 qui sotto. «Stasera non si ritenta» viene dal testo che c'era già («ritentabile dopo la resurrezione»). «messaggi · nessuno» dice che nella Sala non c'è un messaggero, e il master lo conferma (§0, «Chi c'è»). Le due righe non aggiungono fatti, quindi niente tag |

### D13 · Il segno del «conta quattro» su A6 (`[INFERRED]` nel §4)

Al nodo N3 i PG dovrebbero capire che il varco aspetta quattro Custodi. Prima di questo giro il testo non diceva come lo capiscono. Ho aggiunto un segno fisico: sotto la mano, il portale dorato pulsa quattro volte, e il quarto battito è più debole.

**Domanda:** conferma il segno fisico che dice ai PG «conta quattro».

- **Quattro battiti** · il portale pulsa quattro volte e il quarto è debole: la porta fisica di N3 regge.
- **La quarta figura** · il varco si spegne quando lo toccano, e su A2 la quarta figura si accende per un attimo.
- **Nessun segno** · il vetro non cede e basta; il Nome di N3 arriva solo al `DEF-3`.

**Raccomandata: Quattro battiti.** Senza un segno la porta fisica di N3 non c'è più, e questo non cambia nessun canone.
