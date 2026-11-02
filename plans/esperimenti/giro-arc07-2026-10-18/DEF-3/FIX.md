# ARC07-DEF-3, la resurrezione di Hella: correzioni dopo il giro

Esiti: CORRETTO 23 · DECISIONE DM 9 · RESPINTO 2 · 🟡 lasciati 19

Master: `07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md`.
Rapporti: DEVELOPER (D), PLAYTESTER (P), DM (M). I rilievi doppi sono uniti
nella stessa riga.

Verifica dopo le correzioni:
- `misura_craft.py --box`: 19 box, 0 oltre 12 righe, 1 con parentesi, 9 con più
  di un nome proprio. Gli stessi numeri di prima: nessun box è stato toccato.
- `validate_modules.py`: 5 master conformi, 0 errori. Resta l'avviso «nessun
  flag [INFERRED]», che c'era già e che vale per tutti e cinque i DEF.
- `validate_prosa.py`: 6 rilievi, tutti su box che c'erano già (possessivi,
  antitesi, maiuscole). Nessuno viene dal testo nuovo.

Fonti usate per i fatti: `campaign/state.md` (DES di Thorik, Ego 14 di Aegis
Fang, *Eldritch Blast* 7d6), il foglio per la giocatrice `09-SCHEDA-HELLA-RISORTA.md`
e la scheda `01_Collana_dei_Semi_Eterni.md` (Evocazione, Treant, *Luce di
Lathander*), `08-SCHEDA-DURIK.md` (statistiche di Durik), `DEF-2` §7 (le tre
Benedizioni), `campaign-artifacts.md` (*Luce di Lathander* è dell'Anello). Le
regole SRD sono citate per sezione. d20srd.org e Firecrawl non hanno risposto:
la tabella degli incantesimi del druido è quella SRD a memoria (chierico e
druido condividono la progressione: 12° = 6/5/4/4/3/3/2).

## I rilievi

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Eco del Custode e attacco extra di *velocità* (D#1, P#13) | 🟠 | CORRETTO | §5: il passo da 1,5 m non conta (SRD, Azioni in combattimento); da adiacente il vincolo è soddisfatto e Thorik può fare l'attacco completo. La nota dice che l'attacco extra scatta solo nei round in cui è già accanto, e che la velocità per un nano a 6 m sale di 6 m (SRD, *velocità*, al massimo il doppio) |
| Scudo contro energia e area, vulnerabilità al fuoco (D#2) | 🟠 | CORRETTO | §5, sotto la catena: la RD vale solo contro danni fisici (SRD, Riduzione del danno); esempio col fuoco 40 → 20 → 30; con l'area Hella subisce il suo danno e, sopra, la metà del protetto. L'ordine fra resistenza e vulnerabilità resta aperto (vedi 🟡 D#20) |
| Rigenerazione SRD contro guarigione rapida (D#3) | 🟠 | DECISIONE DM | Cambia il significato di un dono «canone giocato» del viaggio. Decisione 1 |
| Step 4 automatico ma con un fallimento, +1 della porta DES (D#4, P#7, M#10) | 🟠 | CORRETTO | Vince il canone D35 (automatico). Tolta la riga di fallimento dal §4; la porta DES dà l'immagine del triangolo che tiene e nessun bonus. Il «seme non germogliato» del §9 resta valido: è il seme dormiente di chi rifiuta |
| Soglia 3 su 3 con 0 successi, regole dello Step 5 sparse (D#5, D#15, M#18) | 🟠 | CORRETTO | Nuova tabella «Lo Step 5 in una tabella» in fondo al §5: Doni versati × successi → riga del §9. 0 successi con soglia 3 su 3 vale «0 su 3» (non c'è riga peggiore). Il ritiro finisce sempre su «1 su 3» per D67/D72/D83, quindi la sua soglia non cambia l'esito. Quick-Reference e §9 rimandano lì |
| DES di Thorik «un punto solo» (D#6, M#12) | 🟠 | CORRETTO | §2-bis: −4 al punteggio, −2 al modificatore (state.md, Corona); «un punto solo in più rispetto a prima dello Smeraldo», come dice E-07c |
| Aegis Fang: chi tira nel conflitto (D#7) | 🟠 | CORRETTO | §5: Thorik tira Volontà CD 14 (Ego, state.md); se fallisce comanda l'ascia (SRD, Oggetti intelligenti, «Oggetti contro personaggi») |
| Treant di Adamantio senza DV, TS, caratteristiche e tattica (D#8, P#22, M#22) | 🟠 | DECISIONE DM | Mancano numeri che nessuna fonte ha (l'archivio P3B dà gli stessi sette valori). Corretto solo il «lei» della *Luce di Lathander*: è Artemis, col potere 1/giorno dell'Anello, entro 9 m, come nel foglio di Hella. Decisione 2 |
| Avatar della Radice senza numeri (D#9) | 🟠 | DECISIONE DM | La Collana rimanda a un «profilo completo in P3B» che non esiste. Decisione 3 |
| Orologio: 3g 15h e «tre ore» (D#10, P#29, M#9, P#9) | 🟠 | DECISIONE DM | Il valore alla soglia è canone (D81, D83). Corretta solo la frase che è sbagliata sotto ogni ipotesi: alla soglia Hella respira da un'ora (§8-bis), non da tre. Decisione 4 |
| La giocatrice di Hella senza niente da fare nelle Scene 1-5 (P#4) | 🟠 | DECISIONE DM | Darle un personaggio da giocare cambia la regia della serata. Decisione 6 |
| Il Cuore è un rubino e l'incasso è vuoto (P#5) | 🟠 | CORRETTO | §9, riga nuova: non entra (pugno contro unghia, dal testo stesso), e una battuta di Moradin che non dice niente sull'incasso, come chiede il §2-bis |
| Chi risponde alla Custode, se Hella è incosciente o il gruppo si divide (P#19, P#20, M#15) | 🟠 | DECISIONE DM | Chi decide l'eco A/B/C è una scelta di regia e di canone. Decisione 7 |
| CA di Hella scomposta male, armatura «media» (P#24, M#21, D#11) | 🟠 | CORRETTO | App. A.1: +5 cuoio borchiato +2, +2 scudo leggero di legno +1, +3 naturale della Collana = 20 (il totale c'era già); contatto 10, sprovvista 20; velocità 6 m da nana (SRD, nano: l'armatura non la riduce). «Leggero» è dedotto dal totale: vedi Decisione 5 |
| Slot da druido di 13° (P#25) | 🟠 | CORRETTO | App. A.1: 6/5+2/4+1/4+1/3+1/3+1/2, base SRD del druido di 12° più i bonus di SAG 20 |
| Riposo prima della soglia, «cercare un'alternativa» vuota (P#30) | 🟠 | DECISIONE DM | D81 dice «non c'è riposo prima della soglia»: se sia un divieto o la sola scaletta lo dice il DM. Decisione 8 |
| Rimandare il rito contro «il varco conta quattro» (P#31) | 🟠 | DECISIONE DM | Le due righe si contraddicono e la risposta tocca il canone del varco. Decisione 9 |
| I testi dei fogli non sono nel modulo (M#5) | 🟠 | RESPINTO | I testi esistono: `homebrew/sessione-resurrezione-mille-anni/` (`03`-`11`, più `HANDOUT-1-cronache-quattro-eroi.hb.md`), e il master li nomina per titolo nel volume *Il Cuore e la Porta*. Il lettore a freddo non li aveva. Ho aggiunto in §12 il percorso, dentro `<!-- apparato -->` |
| Quando si danno i primi due fogli, «risveglio» ambiguo (M#6) | 🟠 | CORRETTO | §0: «prima di cominciare la serata, piegati»; l'eco di Hella «quando il gruppo si sveglia nella Sala dopo il riposo (`DEF-2` §7-bis), prima del rito: non è il risveglio di Hella del §7». Il percorso della regia è in apparato |
| Le tre Benedizioni stanno solo nel PDF (M#8, P#27, D#20 in parte) | 🟠 | CORRETTO | §8-bis: Pelle di Pietra, Cuore Incrollabile, Vigore della Forgia, con gli effetti presi da `DEF-2` §7 |
| Evocazione dei Guardiani contraddittoria (M#20, P#23) | 🟠 | CORRETTO | §7 allineato al foglio della giocatrice e alla scheda della Collana: due Treant al massimo, uno per seme; Durik dal seme III torna subito per un'ora e all'alba è intero; i due Treant insieme spengono l'Evocazione per un mese e Durik, se cade in quel mese, torna all'alba |
| Thorik dona «il +2» ma perde 1 (D#14, P#12, M#13) | 🟡 | CORRETTO | Quick-Reference, tabella dei doni, «Cosa dona», Echo Ledger: «metà del +2 di deflessione, che scende a +1». La restituzione ridà quel +1 |
| Il +1 della porta COS a chi va (D#18, P#3) | 🟡 | CORRETTO | «al primo tiro del rito di chi l'ha superata» |
| Durik senza statistiche (D#19, M#22 in parte) | 🟡 | CORRETTO | App. A.1: pf, CA, attacchi, TS, RD, percezione tellurica da `08-SCHEDA-DURIK.md`, e il rimando al foglio. Il ramo C «secondo il Sogno» resta com'è |
| Momento Hella-Tordek, rimando vuoto (D#21, P#28) | 🟡 | CORRETTO | §8-bis: due frasi su come cambia se Tordek ha rifiutato |
| «Sei fogli» contro sette consegne (M#7) | 🟡 | CORRETTO | §0 e §12 |
| Step 6 rimanda al §9 (M#11) | 🟡 | CORRETTO | §4: lo Step 6 è automatico e non fallisce |
| Livello negativo «dell'SRD» (M#16, P#17) | 🟡 | CORRETTO | §9: segue l'SRD tranne il TS su Tempra dopo 24 ore, che è regola del rito. Quante pergamene di *ristorare* abbia il gruppo resta da segnare |
| Valore della bacchetta (M#23, P#32) | 🟡 | CORRETTO | §11 C: 2.250 mo (SRD, Bacchette: 750 × 2° × LI 3 = 4.500 a 50 cariche); lordo 17.550 mo |
| Il cerchio «sull'Altare» (M#24) | 🟡 | CORRETTO | App. B: «attorno all'Altare». La griglia ASCII R-1 non l'ho toccata |
| Nessuna durata reale (M#25) | 🟡 | CORRETTO | §0, «Quanto dura»: novanta minuti più un quarto d'ora, dalla regia della serata |
| «Countdown A7» (M#26 in parte) | 🟡 | CORRETTO | §9: «l'orologio di Hammerfist». Rituale 4 e Prova di Risonanza restano senza spiegazione nel modulo |
| *Eldritch Blast* 7d6 a un warlock di 13° (M#14) | 🟡 | RESPINTO | `state.md`, riga di Artemis: «Eldritch Blast 7d6». Il numero è canone |
| SAG 20 comprende la Collana? (D#12) | 🟡 | DECISIONE DM | È un fatto della scheda della giocatrice. Decisione 5 |

### 🟡 lasciati

D#13 talenti (sette invece di cinque più Seguire Tracce; *Extra Wild Shape* e
*Power of Nature*) · D#16, P#16, M#17 cosa vuol dire «attecchisce a metà» e di
chi è il dono se chi ha fallito non ha donato · D#17, P#8 Thorik allo Step 1
senza gradi, Aiutare un altro, cedere lo step · D#20 «per una battaglia» e
l'ordine fra resistenza al fuoco e vulnerabilità · P#1, P#2, M#19 la porta CAR
che ripete la battuta di Therysol, e se lei dice del Sud a chi glielo chiede ·
P#6 esaminare o portar via il Cuore · P#10 se i giocatori conoscono la soglia
3 su 3 prima di scegliere · P#11 doni diversi da quelli chiesti · P#14 la
restituzione «per una scena» · P#15 Anello spento e varco · P#18 Durik al Sud
· P#21 la ghianda come pegno · P#26 in che stato si sveglia Hella · P#33, M#27
i PX di Hella · M#1, M#2, M#3, M#4 la vista di chi scorre · M#28 dove finisce
la serata se il gruppo non attraversa.

## Decisioni per il DM

### 1 · La Rigenerazione di Hella

Il dono del viaggio dice «Rigenerazione 1 pf/round a contatto con terra o
pietra, non se ha preso fuoco il round prima». Nell'SRD la Rigenerazione
trasforma i danni in non letali, e la creatura muore solo per i tipi che la
superano: scritta così, Hella su pietra muore solo col fuoco. Anche «Radici del
Mondo» dice «rigenera» senza numero.

**Domanda.** Scegli quale regola SRD vale per la Rigenerazione di Hella.

- **Guarigione rapida** · guarigione rapida 1 su terra o pietra (e su suolo
  sacro con Radici del Mondo), sospesa il round dopo un danno da fuoco: Hella
  muore come tutti.
- **Rigenerazione SRD** · danni non letali, il fuoco li supera: Hella cade
  priva di sensi ma muore solo per il fuoco, finché tocca terra.
- **Rigenerazione larga** · come la precedente, e la superano anche fuoco e
  acido.

**Raccomandata: Guarigione rapida.** La regola della versione più forte
porterebbe alla seconda, ma su un PG la rende immortale fuori dal fuoco, e
toglie il costo a ogni scontro di `DEF-4` dove Hella combatte su pietra. La
clausola del fuoco resta, e con la vulnerabilità ×1,5 il prezzo della Via della
Radice continua a farsi sentire. Diverge dall'SRD solo nel nome: il testo dice
«Rigenerazione» e va scritto «guarigione rapida».

### 2 · Lo statblocco del Treant di Adamantio

Il Treant ha sette valori (taglia Grande, 90 pf, RD 10/adamantio, CA 24,
9 m, due schianti +18 da 2d8+9, Siegebreaker), uguali nell'archivio e nel
foglio della giocatrice. Mancano DV, TS, caratteristiche, iniziativa, portata
e una riga di tattica, e Hella lo può evocare già in `DEF-4`.

**Domanda.** Completa il Treant da una base SRD, o scrivilo tu?

- **Treant SRD** · si completano DV, TS, caratteristiche e portata dal Treant
  dell'SRD, tenendo i sette valori del canone dove sono più alti.
- **Costrutto** · si completa da un golem SRD di pari GS: TS deboli, immunità
  da costrutto.
- **Scrive il DM** · il modulo lascia la riga vuota finché il DM non la
  scrive.

**Raccomandata: Treant SRD.** È la versione più forte: il Treant SRD è Enorme
con TS di Tempra e Volontà alti, e tenere i valori del canone dove sono più
alti dà il guardiano più duro. Va deciso anche se resta Grande (canone) o
diventa Enorme (SRD): consiglio Grande, perché il foglio è già nelle mani della
giocatrice. Con la base scelta scrivo la riga di tattica: obbedisce a Hella, e
senza ordini si mette fra lei e il nemico più vicino.

### 3 · I numeri dell'Avatar della Radice

L'Avatar è il potere da combattimento più forte della Collana: 1/giorno, 10
round, Ibrido Treant Enorme, +8 FOR, portata, schianti. La scheda della
Collana rimanda a un profilo completo che non è in nessun file.

**Domanda.** Decidi da quale regola SRD vengono taglia, schianti e portata.

- **Cambio di taglia** · da Media a Enorme con la regola SRD del cambio di
  taglia: −2 CA e attacco, +8 Lotta, portata 3 m, schianto da Enorme;
  l'equipaggiamento si fonde come nella forma selvatica.
- **Forma del Treant** · usa gli schianti e la portata del Treant SRD, più il
  +8 FOR del canone.
- **Scrive il DM**.

**Raccomandata: Forma del Treant.** È la più forte (schianti e portata da
Treant, non da nana ingrandita) ed è coerente col nome. La Collana funziona già
in forma selvatica, quindi l'equipaggiamento che si fonde è la scelta che
toglie meno.

### 4 · L'orologio di Hammerfist alla soglia

Il master parte da 3g 16h e dice che il rito costa un'ora (3g 15h, D81), più
un'altra ora se c'è l'indagine del Sud (D83). Ma dopo il rito c'è anche «la
prima ora» del §8-bis, e ogni tentativo fallito degli Step 1-3 costa 10 minuti,
fino a 90. Ho corretto solo «respira da tre ore» in «da un'ora».

**Domanda.** Conta il tempo alla soglia a ore fisse o minuto per minuto?

- **Ora fissa** · alla soglia segna 3g 15h, o 3g 14h con l'indagine del Sud: i
  tentativi e la prima ora stanno dentro.
- **Tutto contato** · 3g 16h, meno un'ora di rito, meno 10 minuti per tentativo
  fallito, meno la prima ora, meno l'ora del Sud: il DM lo dice ai giocatori
  alla soglia.
- **Ore intere** · come la precedente, arrotondata all'ora per eccesso.

**Raccomandata: Tutto contato.** È la versione più dura e la più leggibile al
tavolo: ogni tiro fallito si sente sull'orologio, e alla soglia la scelta
«cercare un'alternativa» ha un numero vero. Lascia valido D81 alla lettera
(il rito vale un'ora) e aggiunge solo quello che il master già descrive.

### 5 · Due fatti della scheda di Hella

La scheda dice SAG 20 e «scudo di legno +1». Se SAG 20 comprende già il +4
della Collana, gli slot corretti sono quelli scritti ora; se no, Hella ha SAG
24 e cambiano slot (6/5+2/4+2/4+2/3+1/3+1/2+1) e CD. Lo scudo l'ho scritto
leggero perché è l'unico tipo che dà il totale 20.

**Domanda.** Conferma dalla scheda della giocatrice SAG e tipo di scudo.

- **SAG 20, leggero** · come è scritto ora: nessun altro cambio.
- **SAG 24, leggero** · slot e CD salgono, CA 20.
- **SAG 20, pesante** · CA 21.

**Raccomandata: la scheda.** Non è una scelta di regole: decide il foglio della
giocatrice. Se la scheda non lo dice, vale **SAG 20, leggero**, che è l'unica
lettura in cui tutti i numeri del master tornano.

### 6 · La giocatrice di Hella nelle Scene 1-5

Dalla Sala alla Custode Hella è morta: le porte e gli step sono dei tre
officianti. La giocatrice legge il suo eco al mattino, e poi aspetta fino al
risveglio del §7, circa un'ora di tavolo.

**Domanda.** Dai alla giocatrice di Hella qualcosa da giocare prima del risveglio?

- **Durik** · gioca Durik dalla Scena 1: non parla, si muove attorno al corpo,
  fa il click; il DM le dice cosa sente sotto i piedi.
- **Therysol** · gioca Therysol, con la sua scheda d'entrata.
- **Il silenzio** · nessun ruolo: l'assenza è il punto, e il suo spotlight
  arriva al §7 e al §8.

**Raccomandata: Durik.** Non dice niente che lei non debba sapere, perché non
parla, e porta al tavolo la presenza che il §7 paga quando Durik appoggia la
testa sul petto di Hella. Therysol sa del Sud, e in mano alla giocatrice
rischierebbe di sciogliere il vicolo cieco del §9.

### 7 · Chi risponde alla Custode delle Radici

Le risposte A e B dicono «Hella o il party», ma allo Step 5 lo spirito di Hella
sta varcando la soglia e lei si sveglia solo allo Step 6. La Custode guarda
Hella, non chi parla. Il master non dice cosa succede se i tre non sono
d'accordo.

**Domanda.** Stabilisci chi ha l'ultima parola sul Debito della Radice.

- **Hella dalla soglia** · la giocatrice dice una frase sola, dallo spirito
  sulla soglia, e quella frase decide A, B o C.
- **Il gruppo** · decidono i tre officianti; se non si accordano la Custode
  aspetta, e alla fine vale la maggioranza.
- **Il silenzio è B** · se il gruppo non si accorda, la Custode prende il
  silenzio per un rifiuto e si ritira.

**Raccomandata: Hella dalla soglia**, con **il silenzio è B** come riserva se
nemmeno lei parla. È il Voto di Hella a creare il debito, e il §8 ha già la sua
battuta «il prezzo lo pago io». La riserva è la versione più dura: il vuoto che
risale in ARC-09. Dà anche alla giocatrice una battuta prima del risveglio.

### 8 · Riposare, o cercare un'alternativa, prima della soglia

D81 dice che il rito dura un'ora e che non c'è riposo prima della soglia. Un
tavolo vero chiederà di dormire otto ore prima di attraversare, e la riga
«cercare prima un'alternativa» non dice dove si va né cosa si trova.

**Domanda.** Permetti otto ore di sonno prima della soglia, e a che prezzo?

- **Si dorme** · otto ore in meno sull'orologio; si recuperano incantesimi,
  capacità al giorno e 1 pf per livello (SRD); l'Anello spento resta spento
  fino alle 24 ore.
- **Il varco non aspetta** · Moradin: la Corona tiene il portale pronto un'ora
  sola; chi dorme lo riapre domani, al prezzo di un giorno.
- **Nessun riposo** · resta la scaletta: chi chiede di dormire si sente dire
  che Hammerfist non dorme.

**Raccomandata: Si dorme.** Ha il costo più chiaro e lo paga l'orologio, che è
la posta della scena. Per l'«alternativa» propongo che la riga del §8-ter
voglia dire proprio questo, cioè riposare e prepararsi, senza un luogo nuovo da
scrivere.

### 9 · Se il gruppo rimanda il rito

Il §9 dice che se rimandano Hella resta morta e il gruppo va al `DEF-4` senza il
4° PG. Ma alla soglia Moradin dice che il varco conta quattro e non apre per
meno. Il master non dice nemmeno fino a quando il rito si può fare.

**Domanda.** Decidi se il varco si apre in tre, e fino a quando si può fare il rito.

- **Il varco aspetta** · senza Hella il varco non apre: rimandare costa solo
  tempo sull'orologio, e il rito si può fare quando vogliono.
- **Il varco apre in tre** · la frase di Moradin vale per «uno solo»: in tre si
  passa, e Hella resta morta fino al ritorno.
- **Il Cuore scade** · il rito si può rimandare, ma i semi sul corpo reggono
  fino a una scadenza che il DM fissa.

**Raccomandata: Il varco aspetta.** Tiene la battuta di Moradin alla lettera e
rende la scelta di rimandare un costo vero ma giocabile: ogni ora che passa è
un'ora tolta a Hammerfist. Va corretta la riga del §9 «nessun 4° PG al
`DEF-4`».

## Secondo giro

Dalla `VERIFICA.md`: 4 PARZIALE e 7 NUOVI 🟡. Chiusi 3 PARZIALE e 6 NUOVI;
1 PARZIALE resta tale per la parte in attesa del DM; 1 NUOVO diventa la
Decisione 10. Le voci IN ATTESA DM non sono state toccate.

| Voce della verifica | Esito | Cosa ho fatto |
|---|---|---|
| P#25 slot, Periapto | CHIUSO (la SAG resta alla Decisione 5) | App. A.1, EQUIP: «Periapto di Saggezza +2 (non si somma alla Collana: vale il +4)», come nel foglio della giocatrice |
| M#5 testi dei fogli | CHIUSO per il percorso | §12, apparato: le Cronache stanno in `homebrew/HANDOUT-1-cronache-quattro-eroi.hb.md`. Che cosa rivelano le Cronache resta nel foglio, non nel master: è un handout, e il master dice quando si consegna |
| M#8 Benedizioni | CHIUSO | §8-bis: Vigore della Forgia con le cariche che tornano dopo un sonno di otto ore, 3d8+5 a sé, 2d8+2 a contatto (`DEF-2` §7) |
| M#21 CA e SAG | PARZIALE | La CA era già chiusa; la SAG è la Decisione 5 |
| NUOVO 1 · Aegis Fang, durata | CHIUSO | §5: se Thorik fallisce la Volontà CD 14, comanda l'ascia per un giorno o finché non arriva una situazione critica, come nell'SRD (Oggetti contro personaggi). È la versione più dura, e non diverge dall'SRD |
| NUOVO 2 · Vigore della Forgia | CHIUSO | come M#8 |
| NUOVO 3 · §4, fallimento dello Step 5 | CHIUSO | §4, riga 5: si ritenta quando l'esito è la riga «0 su 3», cioè 0 successi, o 1 solo se i Doni versati sono uno o nessuno, con rimando alla tabella del §5 |
| NUOVO 4 · semi allo Step 4 e seme dormiente | CHIUSO | Porta DES: «le radici dei tre semi entrano nello stesso istante». §4: le radici entrano sempre, e un seme resta dormiente, senza niente sopra, solo se il donatore rifiuta allo Step 5. §9: l'indizio è «il seme dormiente, se qualcuno ha rifiutato» |
| NUOVO 5 · resistenze al fuoco | CHIUSO | §5, sotto la catena: Pelle di Pietra (10) e Mantello della Fiamma (20) non si sommano, vale la più alta (SRD, resistenze allo stesso tipo di energia) |
| NUOVO 6 · percorso delle Cronache | CHIUSO | come M#5 |
| NUOVO 7 · druido col cuoio borchiato | DECISIONE DM | Decisione 10, qui sotto |

Misure dopo il secondo giro: `misura_craft --box` 19 box, 0 oltre 12 righe,
1 con parentesi, 9 con più di un nome proprio (invariati); `validate_modules`
0 errori. Nessun box toccato.

### 10 · Il cuoio borchiato di una druida

La scheda di Hella le dà il cuoio borchiato +2, e il DM ha deciso il
2026-09-25 che vale la scheda della giocatrice. Nell'SRD il druido non porta
armature di metallo: può indossare armatura imbottita, di cuoio o di pelle, e
il cuoio borchiato ha borchie di metallo. Chi lo indossa perde incantesimi e
capacità soprannaturali per 24 ore.

**Domanda.** Decidi se il cuoio borchiato di Hella è un'eccezione o va cambiato.

- **Eccezione** · le borchie sono di legno di ferro o d'adamantio vegetale,
  «venato di corteccia» come dice il §11 C: si dichiara nella scheda, CA 20.
- **Cuoio** · diventa armatura di cuoio +2 (+4): CA 19, valore quasi uguale.
- **Pelle** · diventa armatura di pelle +2 (+5, media): CA 20, ma DES massima
  +4 e penalità alla prova d'armatura più alta.

**Raccomandata: Eccezione.** Tiene la scheda della giocatrice, che il DM ha già
dichiarato prevalente, e il §11 C dice già che l'armatura è «ora venata di
corteccia, adattata all'Ibrido». Va scritto che diverge dall'SRD.
