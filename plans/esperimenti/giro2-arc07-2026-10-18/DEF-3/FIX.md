# ARC07-DEF-3 · giro 2 · correzioni

Esiti: CORRETTO 16 · DECISIONE DM 13 · RESPINTO 1 · 🟡 lasciati 20

Master corretto: `07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md`.
Rapporti: DEV = developer, PT = playtester, DM = DM a freddo. I rilievi doppi sono
uniti nella stessa riga. Le tredici decisioni sono otto rilievi 🟠, un 🟡 che
tre lettori hanno fatto (i PX), i tre `[INFERRED]` che erano già nel master e
non stanno in un'altra decisione, e due contraddizioni che ho trovato io
confrontando il master con `DEF-2` e con i fogli dei giocatori.

Verifiche dopo le correzioni: `misura_craft --box` dà 20 box, 0 oltre le 12
righe, 0 parentesi, 0 con più di un nome (come prima). Verdi `validate_modules`,
`domande_developer --check`, `copertura_scene --check`, `test_storico`,
`componenti --check`, `validate_prosa`. `test_storico` si era rotto per una
data che avevo scritto nella riga del Marchio di Varis: l'ho tolta. Nessun box
è stato toccato. Le due righe da leggere che ho aggiunto (le varianti col Sud
già tenuto) stanno fuori dai box, e nel master non c'è nessun `[INFERRED]`
nuovo.

## I rilievi

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Il dono che «attecchisce a metà» non ha una regola; e se chi fallisce aveva rifiutato (DEV#1, PT#12, DM#12) | 🟠 | DECISIONE DM | È una regola nuova su tre poteri della Collana: D1 |
| Un PG lascia il suo punto per tenere il Sud: il buco nuovo conta? (DEV#2, PT#3, DM#7) | 🟠 | DECISIONE DM | Decide l'esito dello Step 5: D2 |
| Durik sdraiato al Sud vale come risposta? (PT#4, DM#6) | 🟠 | DECISIONE DM | È la stessa domanda: D2 |
| Manca la giocatrice di Hella (DEV#3) | 🟠 | DECISIONE DM | Tocca il ramo del Debito, che è canone: D3, insieme alla riga di scala `[INFERRED]` |
| Con quali risorse torna Hella (DEV#4) | 🟠 | DECISIONE DM | Un miracolo, non l'incantesimo: D4 |
| «Per una battaglia» e «1/battaglia» non sono durate 3.5; rinnovo; Pelle di Pietra ancora attiva? (DEV#5, PT#18, DM#15) | 🟠 | DECISIONE DM | Durate in D5. Corretti sul posto i nomi «Skullcrusher/Fauci», che diventano «gli scontri di `DEF-4`», e il rinnovo del §11, che ora dice dieci minuti di preghiera, una volta ogni 24 ore vissute, come `DEF-2` §7 |
| La percezione tellurica di Durik e il battito nell'Altare (PT#1) | 🟠 | CORRETTO | Nel §2 una riga: il DM dice il vero (qualcosa batte, sessanta al minuto, fermo) ma non che cosa sia. È lo stesso che dà la porta di SAG, e il «Cosa NON dire» regge |
| Sud occupato prima dello Step 5: l'apertura di round e il box della Custode diventano falsi (PT#2, DEV#9, DM#8) | 🟠 | CORRETTO | Una variante nell'apertura di round 5 e una per la seconda frase del box della Custode, tutte e due fuori dal box. Nel §9: se il richiamo riesce non cambia niente, e allo Step 5 tirano sempre i tre officianti; chi tiene il Sud tira solo nel ritiro |
| Prendere 10 o 20 sulle prove del rito (PT#5); aiutare un altro, Therysol, incantesimi (PT#6, DEV#13) | 🟠 | DECISIONE DM | Cambia quanto spesso il rito costa: D6 |
| Il DM non sa che cosa dicono gli echi e gli altri fogli (PT#7, DM#10, PT#9) | 🟠 | CORRETTO | Nel §0 una tabella «Che cosa dicono i fogli, per il DM», una riga per foglio, presa dai fogli veri in `homebrew/sessione-resurrezione-mille-anni/` e dalle Cronache |
| Un PG si offre: «lo porto io» (PT#11) | 🟠 | CORRETTO | Nel §6 la risposta che il master aveva già: la Custode non guarda gli altri tre, il debito è della radice e la radice è di Hella. L'offerta resta detta, e al §8 Hella la ricorda |
| Non attraversano il portale e corrono a Hammerfist (PT#16) | 🟠 | DECISIONE DM | Riordinerebbe gli archi: D7 |
| La vista non mostra gli echi da dare prima né il volume dei giocatori (DM#1) | 🟠 | CORRETTO | «Cosa stampare» comincia dal volume *Il Cuore e la Porta*, e in grassetto dice che gli echi privati si danno prima di cominciare |
| 92 minuti di lettura: con un'ora il DM si ferma prima del §9 (DM#4) | 🟠 | CORRETTO | Il master non si accorcia senza riscriverlo. Nel §0 c'è adesso «Se hai un'ora per prepararti», con le quattro parti che servono quando un tiro va male: §0, §0-bis, la tabella dello Step 5 e il §9 |
| §1 «nessuna coscienza» contro la frase di Hella dalla soglia; come si sente lo spirito (DM#5, DEV#12) | 🟠 | CORRETTO | Nel §1 c'è l'eccezione: alla soglia del §6, per una frase, la giocatrice lascia Durik. Nel §6 una riga: la frase si sente con la voce di Hella, bassa, dal Cuore sul suo petto, e nessuno la vede. È regia, non un potere |
| L'orologio di Hammerfist è fuori dal file (DM#9) | 🟠 | CORRETTO | Nel §0 due frasi da `DEF-2` §0-bis: che cosa conta, dove lo leggono i PG (A7) e che cosa succede sotto i 2 giorni |
| *Eldritch Blast* 7d6 per un warlock di 13° (DM#11) | 🟠 | RESPINTO | `campaign/state.md` §1, riga di Artemis: «Eldritch Blast **7d6**». Lo stato batte il manuale (coerenza §0). Il dado in più può venire dall'Anello, e il master non lo dice. Se la scheda di Artemis dice 6d6, va corretto lo stato, non il master |
| *augurio* non risponde con una frase (DEV#6) | 🟡 | CORRETTO | Nella riga del Sud, *augurio* risponde solo «bene» (SRD, *Augurio*); la frase la dà *divinazione* |
| «Dormire prima» del rito rimanda a una riga che parla della soglia (DEV#10, PT#10) | 🟡 | CORRETTO | La riga del §9 ora vale «prima del rito o prima della soglia». La tariffa resta una decisione: D11 |
| TS di Hella senza numeri (DEV#18, PT#19, DM#13) | 🟡 | CORRETTO | Tempra +16, Riflessi +8, Volontà +15, col conto dalle tabelle SRD del ranger e del druido. I sette talenti contro i cinque dei 13 DV restano: vengono dalla scheda della giocatrice |
| Treant tenuto Grande con COS 21 (DEV#19) | 🟡 | CORRETTO | Nel ⚠ «Non SRD» c'è adesso anche COS 21, che l'SRD da Grande farebbe 17 |
| «Prova di Risonanza» e Zog'tar (DEV#20, DM#16) | 🟡 | CORRETTO | Il termine non esiste in nessun master. L'eco di Durik diventa «il primo scontro accanto a Hella, contro Zog'tar in `DEF-4`» |
| Eco di Hella: quale metà si legge, «Atto 0» o «Atto I» (PT#8, in parte DM#21) | 🟡 | CORRETTO | Ad alta voce si legge la prima metà, «Mentre gli altri dormono», come dice il foglio 06. Nel §7 «dall'Atto I» diventa «dal risveglio del gruppo» |
| Il Marchio di Varis: Artemis lo porta? (DM#20) | 🟡 | CORRETTO | Dallo stato, §7: non lo porta, il Seme è nello zaino di Tordek e nessuno l'ha toccato |
| La mappa S-1 di `DEF-2` e l'Appendice B (DM#24) | 🟡 | CORRETTO | Una mezza riga: è la stessa Sala |
| PX di Hella, morta per quasi tutta la serata (DEV#22, PT#21, DM#22) | 🟡 | DECISIONE DM | Tre lettori: D13 |
| Mancano segreti nel blocco «Se lo divinano» (DEV#7) | 🟡 | lasciato | Le proposte sono dentro D8 |
| Perché il Cuore è l'unico modo, dentro la finzione (DEV#8) | 🟡 | lasciato | È canone, non si aggiunge senza il DM |
| Hella rifiuta Durik: vale A o B? (DEV#11) | 🟡 | lasciato | |
| Il ritiro si tira ma finisce sempre su «1 su 3» (DEV#14, PT#13) | 🟡 | lasciato | Lo fissano D67 e D72. Se il DM vuole, il ritiro si può dichiarare un tiro di scena |
| Tre durate dell'Eco del Custode; Hella protegge Thorik stesso (DEV#15) | 🟡 | lasciato | |
| Ordine fra lo Scudo e il TS su Riflessi del protetto (DEV#16) | 🟡 | lasciato | |
| Che cosa fa il giocatore di Thorik se l'ascia comanda (DEV#17) | 🟡 | lasciato | Servirebbe inventare cosa pretende l'ascia |
| La Collana restituisce: Hella tiene il dono nel frattempo? (DEV#21) | 🟡 | lasciato | Riguarda un potere di artefatto |
| La ghianda: a che cosa va il +1 (DEV#23, DM#17) | 🟡 | lasciato | Canone del DM del 2026-07-23 |
| Il Cuore regge «finché il tavolo lavora»: quanto scende l'orologio (PT#14) | 🟡 | lasciato | |
| Quante pergamene di *ristorare*, e chi le legge (PT#15) | 🟡 | lasciato | |
| Evocazione dei Guardiani: tipo d'azione, secondo Treant (PT#17) | 🟡 | lasciato | Potere di artefatto |
| La tabella «Chi si trova qui» nella Forgia (PT#20) | 🟡 | lasciato | Costa otto righe, quasi tutte «nessuno» |
| «Chi si oppone» non compare nella vista (DM#2) | 🟡 | lasciato | Dipende dallo strumento della vista |
| Grassetti di servizio nella vista (DM#3) | 🟡 | lasciato | Stanno quasi tutti nell'apparato, che non va in stampa |
| Di che tipo è il +3 della Collana (DM#14) | 🟡 | lasciato | Potere di artefatto |
| Prove di Conoscenze per riconoscere la Custode (DM#18) | 🟡 | lasciato | |
| Come si apre il varco (DM#19) | 🟡 | lasciato | È materia di `DEF-4` |
| La serata comincia col risveglio del gruppo? (DM#21) | 🟡 | lasciato in parte | Il foglio di Hella è sistemato; per l'inizio della serata vedi D11 e D12 |
| Nessuna battuta di Hella per il ramo B (DM#23) | 🟡 | lasciato | Prosa nuova: la scrive chi decide il ramo |

## Decisioni per il DM

### D1 · Il dono che attecchisce a metà

Con 2 successi su 3 allo Step 5 «un dono attecchisce a metà» e il PG che ha
fallito lo scopre a −1.000, ma la regola non c'è. La Pelle è una RD passiva,
lo Scudo è 1/giorno, e chi ha fallito può essere uno che ha rifiutato e non ha
un dono. La riga «1 su 3» invece non tocca i doni: ha già il livello negativo.

**Domanda.** Decidi che cosa fa, nelle regole, un dono che attecchisce a metà.

- **Primo uso perso.** A −1.000 il primo uso non funziona e si consuma: lo Scudo spende l'uso del giorno senza prendere il danno, la Pelle non toglie niente al primo colpo fisico, il Rovo manca e l'azione è spesa.
- **Metà valore.** Per la prima scena il dono vale la metà: lo Scudo prende tre quarti del danno, la RD è 1, il Rovo fa 1d6.
- **Solo un'eco.** Nessun effetto di regole: il dono esita una volta, e il DM lo racconta.

**Raccomandata: Primo uso perso**, più una riga: se chi ha fallito aveva
rifiutato, attecchisce a metà il dono di un altro, e lo sceglie il DM. È la
versione più forte e quella che il master promette: «nel momento peggiore».
Non è SRD, perché nell'SRD un dono così non esiste: è una regola del rito.

### D2 · Chi può tenere il Sud

Il §9 dice che il Sud lo tiene «un PG o Therysol», e che se lo tiene un PG
«tirano lui e gli altri due». I PG vivi però sono i tre officianti, quindi chi
va al Sud lascia vuoto il suo punto. La mossa più probabile della giocatrice è
Durik sdraiato al Sud, perché il corpo «si gira verso sud». Qui rientra anche
l'`[INFERRED]` della riga «Se i PG chiedono a Therysol del corpo».

**Domanda.** Stabilisci chi può tenere il Sud, e se un punto lasciato conta.

- **Chi non officia.** Valgono Therysol e Durik. Un PG che si sposta apre un buco nuovo e il ritiro non parte; Moradin lo dice, e il tavolo ha escluso una pista.
- **Chiunque.** Vale anche un PG, e il punto che lascia non conta: è il testo letto alla lettera.
- **Solo Therysol.** Durik è del Sogno e tira dall'altra parte: al Sud non vale.

**Raccomandata: Chi non officia.** Premia la mossa naturale della giocatrice e
prepara l'opzione C della Custode, dove Durik è già «metà di là». Lo
spostamento di un PG resta una risposta sbagliata che porta da qualche parte,
come vuole la skill dell'indagine. Allo Step 5 tirano sempre i tre officianti,
ed è già scritto.

### D3 · Se manca la giocatrice di Hella

Il master prevede l'assenza di un officiante (riga di scala, `[INFERRED]`), non
quella della giocatrice di Hella. Lei gioca Durik, sceglie A, B o C dalla
soglia ed è la protagonista del §8. Se manca, il testo porta da solo al ramo B.

**Domanda.** Scegli che cosa si fa se la giocatrice di Hella non c'è.

- **Si rinvia.** La serata si sposta: è la sua.
- **Frase prima.** Il DM le chiede prima della serata A, B o C e la frase; Durik lo muove il DM, e il §8 si gioca alla serata dopo.
- **Come è scritto.** Il silenzio vale B.

**Raccomandata: Si rinvia**, e «Frase prima» se il tavolo non può aspettare.
Il ramo B per assenza punisce una persona che non c'era. La riga per
l'officiante assente la confermerei così com'è: è sensata, e lascia il dono a
chi tornerà.

### D4 · Con che cosa torna Hella

Il master non dice con quali pf, incantesimi, usi della Collana e forme
selvatiche torna Hella. Il §8-bis le fa evocare un orso e lanciare *Produce
Flame* subito prima della soglia, e la scelta «Attraversare adesso» la porta
dritta negli scontri di `DEF-4`.

**Domanda.** Fissa le risorse di Hella al risveglio, e se il §8-bis le spende.

- **Come resurrezione.** Pf pieni e gli incantesimi che aveva preparati alla morte (SRD, *Resurrezione*: «nessuna perdita di incantesimi preparati»); Collana e forma selvatica con tutti gli usi del giorno. Le prove del §8-bis spendono slot veri.
- **Prove gratis.** Come sopra, ma le prove del §8-bis sono scena e non spendono niente.
- **Svuotata.** Pf a metà e nessuno slot fino a otto ore di sonno: il ritorno costa, e la soglia spinge a dormire.

**Raccomandata: Come resurrezione.** È la versione SRD più forte, e il Cuore
è un miracolo più grande dell'incantesimo. Il costo vero resta quello che il
master ha già: provare il corpo nuovo prima di attraversare ha un prezzo in
slot, ed è una scelta del tavolo.

### D5 · Quanto durano il Mantello della Fiamma e la Benedizione di Moradin Incarnato

«Per una battaglia» e «1/battaglia» non sono misure 3.5, e il Mantello non ha
un tipo d'azione. `DEF-2` §7 dice che le tre Benedizioni del PDF durano 24 ore
vissute dalla preghiera; se la Pelle di Pietra di `DEF-2` sia ancora attiva al
rito dipende da quando hanno pregato.

**Domanda.** Dai una durata 3.5 alle due Benedizioni di Hella.

- **Ventiquattro ore.** Il Mantello (resistenza al fuoco 20) dura 24 ore vissute come le altre e non si somma alla Pelle di Pietra; Incarnato 1/giorno, azione veloce, 1 minuto.
- **Dieci minuti.** Il Mantello si attiva con un'azione gratuita, 1/giorno, e dura 10 minuti; Incarnato come sopra.
- **Un uso solo.** Il Mantello dura fino al primo scontro e poi si spegne per sempre.

**Raccomandata: Ventiquattro ore.** È la più forte, ed è coerente con la
regola delle Benedizioni in `DEF-2` §7; si rinnovano all'Altare con le altre.
La vulnerabilità al fuoco resta il prezzo vero, perché a −1.000 la Sala non
c'è e le 24 ore finiscono. Per la Pelle di Pietra basta guardare l'ora della
preghiera nel registro di `DEF-2`.

### D6 · Prendere 10, aiutare, incantesimi sulle prove del rito

Il cerchio è «sacro e sicuro» e ogni tentativo costa 10 minuti: per l'SRD,
senza minaccia né distrazione si può prendere 10. Prendere 20 l'SRD lo esclude
già, perché il fallimento costa (−2 cumulativo, 2d6 non letali, il tempo).
Non è scritto se valgono *aiutare un altro*, Therysol o un incantesimo lanciato
prima di uno step.

**Domanda.** Decidi che cosa vale sulle prove degli Step 1-3 e sulla Volontà.

- **Niente aiuti.** Il rito è una distrazione (la voce di Moradin nella testa, il corpo che tira): niente 10 e niente 20. Nessun aiuto, perché chi officia non fa altro e un aiuto da fuori è un'azione esterna. Gli incantesimi lanciati prima del rito valgono.
- **Prendere 10.** L'SRD letto alla lettera: il 10 vale, il 20 no, gli aiuti no.
- **Aiuti larghi.** Il 10 vale, e Therysol può aiutare una prova a step.

**Raccomandata: Niente aiuti.** È la più forte, e diverge dall'SRD solo nel
dichiarare il rito una distrazione, cosa che l'SRD lascia al DM. Con il 10
Tordek passerebbe la Concentrazione CD 20 quasi sempre, e i prezzi ❌ degli
step non uscirebbero mai.

### D7 · Non attraversano e corrono a Hammerfist

Le scelte della soglia sono tre: attraversare, riposare, mandarne uno. Il
master non dice se si può lasciare la Forgia senza il portale, e un tavolo con
l'orologio che scende ci penserà. In `DEF-2` §0-bis il viaggio a −1.000 costa
0 ore, e il Rubino li riporta nel Cuore della Montagna (`DEF-5` §3).

**Domanda.** Stabilisci se dalla Forgia si può uscire senza passare dal portale.

- **Una porta sola.** La Forgia non ha altra uscita verso Faerûn: si torna passando di là, e Moradin lo dice.
- **I Bracieri aprono.** Le chiavi planari di Tordek li riportano a Hammerfist subito, saltando `DEF-4`: l'ARC-08 parte senza Rubino e senza Cronache.
- **Uscita col prezzo.** Si esce, ma il portale del Tempo si chiude per sempre.

**Raccomandata: Una porta sola.** Lo stato elenca P5, il raccordo e poi
l'Arco 08, e la coerenza vieta di riordinare gli archi senza il DM. È anche la
versione più dura: l'unica strada per salvare Hammerfist passa da mille anni
fa.

### D8 · Il blocco «Se lo divinano» (`[INFERRED]` già nel master)

Le quattro righe sono tutte `[INFERRED]`. In questo giro ho corretto
*augurio*, che risponde solo «bene» o «male». A stasera può divinare chi ha
pergamene o Utilizzare Oggetti Magici, e Thorik con la Comunione 1/mese della
Corona (stato, §6). Mancano tre segreti: la forma dei Doni, il Cuore dentro
l'Altare, *parlare con i morti* sul corpo.

**Domanda.** Conferma il blocco, e decidi se aggiungere i tre segreti mancanti.

- **Confermo così.** Le quattro righe restano, senza marca.
- **Confermo e aggiungo.** Tre righe nuove: *individuazione del magico* sull'Altare sente una presenza divina senza dire che cosa sia; la forma dei Doni la *divinazione* non la dice prima del sì; *parlare con i morti* fa rispondere il corpo con quello che Hella sapeva alla morte.
- **Riscrivo.** Il blocco si rifà col DM.

**Raccomandata: Confermo e aggiungo.** La terza riga viene dall'SRD: *parlare
con i morti* legge la conoscenza rimasta nel corpo, non l'anima, quindi il
corpo non sa niente del viaggio e il §8 resta intatto. Le altre due premiano
chi lancia senza bruciare il §3 e il §5.

### D9 · Esaminano o toccano il Cuore (`[INFERRED]` già nel master)

La riga dice che il Cuore scalda la mano, batte sessanta al minuto e non si
lascia studiare, e Moradin chiude con «Si spende, non si porta».

**Domanda.** Conferma che il Cuore si lascia toccare ma non studiare.

- **Confermo.** La riga resta com'è, senza marca.
- **Con un prezzo.** Chi lo stringe senza officiare prende danni da fuoco.
- **Si studia.** *Analizzare dweomer* o *identificare* dicono che cosa fa.

**Raccomandata: Confermo.** Il prezzo inventerebbe un effetto a una reliquia
di un dio, e lo studio toglierebbe al §3 la sua rivelazione.

### D10 · Il seme dormiente durante l'ora d'indagine (`[INFERRED]` già nel master)

Se lo Step 5 va a zero e qualcuno aveva rifiutato, il tavolo può pensare che a
mancare sia il dono. Il master fa rispondere Moradin che il seme si riempirà
più avanti e che non è quello che manca.

**Domanda.** Conferma che durante l'ora non si può più donare.

- **Confermo.** Il seme resta chiuso fino ad ARC-09.
- **Si dona tardi.** Chi aveva rifiutato può donare adesso: il seme germoglia, ma il ritiro resta sulla riga «1 su 3».

**Raccomandata: Confermo.** Tiene la regola «il rifiuto è una quest», e la
risposta sbagliata porta comunque al Sud.

### D11 · Quanto costa dormire nella Sala (contraddizione trovata in questo giro)

`DEF-2` §0-bis dice di possedere l'orologio e che ogni sonno nella Sala costa
**−4 ore**, perché lì il tempo scorre più lento; ai giocatori lo sconto non si
dice. Questo master, con la marca `[CANONE — DM 2026-10-18]`, fa costare
**otto ore** il sonno prima della soglia (§8-ter, §9) e scrive che «i PG lo
sanno». Nessun lettore l'ha visto, perché nessuno aveva `DEF-2`.

**Domanda.** Scegli la tariffa del sonno nella Sala dopo il rito.

- **Vale DEF-2.** Quattro ore, come per ogni sonno nella Sala; il master si allinea in due righe e i PG vedono solo l'affresco.
- **Vale DEF-3.** Otto ore: dopo il rito la Sala smette di rallentare il tempo, e `DEF-2` lo dice in una riga.

**Raccomandata: Vale DEF-2.** È il file che possiede l'orologio e lo scrive:
«se i numeri divergono, vale questo». Se l'otto ore del 2026-10-18 era voluto,
serve una ragione nella finzione, e `DEF-2` va aggiornato.

### D12 · Chi dice il nome di Hella nel sonno (contraddizione trovata in questo giro)

Il paragrafo «Come arrivano» del master dice che Hella «ha già sentito
**Thorik** dire il suo nome nel sonno». Il foglio della giocatrice (06, prima
metà) dice: «La voce è quella di **Tordek**». Anche il §1 di Tordek («la voce
che Hella ha sentito nel buio») e la prima battuta di Hella al §7 vanno verso
Tordek, e il box di `DEF-2` §7-bis dice solo «un nano che hai tenuto per mano».

**Domanda.** Conferma chi dice il nome di Hella nel sonno.

- **Tordek.** Si corregge una riga del master.
- **Thorik.** Si corregge il foglio 06, e il §7 cambia senso.

**Raccomandata: Tordek.** Lo dicono il foglio già stampato, il §1 e il §7. Non
l'ho corretto da solo perché il sogno di `DEF-2` potrebbe essere già stato
letto al tavolo.

### D13 · I PX di Hella

Il budget del §11 è di circa 1.900 PX per PG: il rito, la scelta-costo, il
Debito e il racconto. Hella è morta fino allo Step 6, ma risponde alla Custode
e fa il racconto. Il master non dice se li prende, né se qualcuno arriva al
14° stasera.

**Domanda.** Decidi quanti PX del beat prende Hella.

- **Tutti.** 1.900, come gli altri: il gruppo resta allineato verso il 14°.
- **Solo i suoi.** Debito e racconto, 700.
- **Niente.** Il beat è degli altri tre.

**Raccomandata: Tutti.** Il master dice che il 14° matura a Hammerfist per il
gruppo intero, e un PG un passo indietro per essere morto è un costo che la
campagna non ha mai deciso.

## Seconda passata

Esiti: CORRETTO 8 (3 PARZIALE, il nuovo 🟠, 4 🟡) · lasciati 0. I nove IN ATTESA DM restano le decisioni D1-D7.

| Rilievo (VERIFICA) | Gravità | Esito | Cosa ho fatto |
|---|---|---|---|
| PT#1 · che cosa sente Durik (PARZIALE), con N3 | 🟠 | CORRETTO | La riga del §2 dice adesso «sotto i piedi qualcosa batte, sessanta al minuto, e non si sposta». Il DM non dice né dove né che cosa: Durik sente il ritmo e la fermezza, non la pietra. Il ❌ della quarta colonna regge, e il §3 resta la rivelazione |
| PT#11 · «lo porto io» (PARZIALE) | 🟠 | CORRETTO | Nel §8, dopo la battuta per Durik, la battuta che mancava: Hella guarda chi si è offerto, *«Ti sei offerto. Non era tuo da portare, e lo sapevi.»* (14 parole) |
| DM#1 · la vista non mostra echi e volume (PARZIALE) | 🟠 | CORRETTO | In testa al §0 c'è adesso il riquadro «La serata in tre frasi», nella forma di `DEF-2`: niente scontri, chi si oppone (la morte, l'orologio di A7, la Custode), gli echi privati del volume *Il Cuore e la Porta* da dare prima di cominciare. Ho rigenerato la vista con `vista_di_chi_scorre.py` e il riquadro compare sotto «LA SERATA» |
| N1 · la tariffa delle otto ore allargata al sonno prima del rito | 🟠 | CORRETTO | Ho rimesso la riga del §9 a «prima della soglia». La riga dice adesso che prima del rito vale la tariffa della Sala di `DEF-2` §0-bis, che possiede l'orologio; per la soglia resta la marca del 2026-10-18. La contraddizione rimasta è solo quella dopo il rito, cioè D11, nella misura di prima |
| N2 · «chi tiene il Sud tira solo nel ritiro» contro la regola di Therysol | 🟡 | CORRETTO | Diventa «chi tiene il Sud non tira allo Step 5»; chi tira nel ritiro lo dice la riga «0 su 3» |
| N3 | 🟡 | CORRETTO | Con PT#1, sopra |
| N4 · le strofe della preghiera | 🟡 | CORRETTO | «quattro strofe in italiano; la terza chiude su *«Quello che manca…»*», come nel foglio 10 |
| N5 · la riga privata del foglio di Hella letta ad alta voce | 🟡 | CORRETTO | Nella tabella delle consegne: la prima metà si legge «senza la riga «Solo per te», che resta sua». Il nome di Tordek non esce, e D12 resta aperta |

Gate dopo la seconda passata: `misura_craft --box` dà per DEF-3 20 box, 0 oltre le 12 righe, 0 parentesi, 0 con più di un nome. Verdi `validate_modules`, `domande_developer --check`, `copertura_scene --check`, `test_storico` (8 su 8) e `validate_prosa`. Il riquadro nuovo è una nota per il DM, non un read-aloud, e non entra nel conteggio dei box. `componenti --check` dà un solo errore, su `APPARATO-ARC07-DEF-5-RITORNO-HAMMERFIST.md`, che non è il mio master; quello di DEF-3 è allineato. Non ho lanciato `--apparato`.
