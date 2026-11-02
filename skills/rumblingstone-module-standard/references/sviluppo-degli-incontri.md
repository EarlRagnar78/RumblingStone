# Lo sviluppo degli incontri — le domande del developer

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- 1 · La lente dei Tier: chi resta senza niente da fare
- 2 · Volo e invisibilità, dal 5° livello
- 3 · I tre tiri salvezza
- 4 · Chi sente il rumore
- 5 · Il boss cambia, non si allunga
- 6 · Lo skill challenge si scrive per intero
- 7 · Chi si diverte in questa scena
- 8 · Ogni scontro che il master rende possibile ha la sua tattica
- 9 · Il segreto e la divinazione, dal 9° livello
- 10 · Ogni scontro ha la sua riga di scala
- 11 · Il mostro che nessun altro sostituisce
- 12 · Il pericolo che qualcuno usa
- 13 · L'incontro che resta uno
- 14 · Il rinforzo che i PG vedono arrivare
- 15 · Niente dossi al 13°
- 16 · Il PG fuori gioco per un tiro salvezza
- 17 · Le domande nate dai giri su ARC-07
- 18 · La domanda della scena
- 19 · La scelta che si vede
- 20 · Il cattivo si annuncia
- 21 · La rete degli indizi, marcata
- Come si scrive un rilievo del developer
<!-- /indice -->

Nei colophon di Paizo e WotC il testo passa da due mani: l'editor chiede *«si
capisce?»*, il developer chiede *«si gioca?»*. Il repo ha già l'editor
(`rumblingstone-prosa-documenti`, il lettore a freddo) e i numeri dei mostri
(`npc-villain-boosting`). Questo file tiene le domande del developer che non
stavano da nessuna parte.

Vengono da due manuali che il DM ha portato il 2026-09-26, controllati uno per
uno: il verdetto su ciascun punto, con le fonti e gli errori trovati, è in
`plans/RICERCA-MANUALE-DEL-MASTER-2026-09.md`. Qui resta solo quello che ha
superato il controllo, riscritto per la 3.5.

Le §9-§16 vengono da un secondo giro, il 2026-10-18: le avventure della
community 3.5 e PF1e (Pathfinder Society, i giudici di RPG Superstar, Necromancer
e Frog God, Raging Swan, l'Alexandrian, il Gruppo Chimera), messe accanto ai
nostri master. Sono le domande che lì si fanno e qui no, quasi tutte sull'alto
livello. Le fonti e ciò che è stato scartato:
`plans/RICERCA-AVVENTURE-COMMUNITY-2026-10.md`; la decisione:
[ADR-0092](../../../plans/adr/ADR-0092-le-domande-dell-alto-livello.md).

Si applica a ogni master nuovo o riscritto, **dopo** la checklist del
`SKILL.md` e **prima** della lettura a freddo (`rumblingstone-playtest` §2-bis).

Le §18-§21 vengono da un terzo giro, il 2026-10-22: le regole d'architettura
delle avventure che in rete si possono verificare sul testo (la domanda
drammatica, la scelta che si vede, il presagio del cattivo, la Three Clue
Rule). Fonti e calibrazione: `plans/RICERCA-QUALITA-MISURABILE-2026-10.md` §4 e
il lotto 7b di `plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md`.

**Chi le misura.** `python3 scripts/domande_developer.py` guarda la forma del
testo per le domande 1-6, 9, 10, 15, 16 e 18-21 e dice in quale scena la risposta
manca; `--check`
gira in CI, e un rilievo che non è un difetto si dichiara con la ragione in
`plans/domande-developer.json`. È un indicatore: vede che la parola c'è («se
volano», «l'allarme arriva in 2 round»), non che la risposta regga. La 7, la 8, le
11-14 e la 17 non le misura nessuno: per rispondere bisogna aver simulato lo scontro. Calibrazione: `plans/esperimenti/domande-developer-def4/`.

## 1 · La lente dei Tier: chi resta senza niente da fare

In 3.5 le classi non valgono uguale. La classificazione di JaronK (Giant in the
Playground) mette Mago, Chierico e Druido nel Tier 1, e Guerriero, Monaco e
Paladino nel Tier 5: in gioco i primi cambiano la realtà, i secondi fanno bene
una cosa sola. È il *linear warrior, quadratic wizard* dei forum.

Il gruppo di RumblingStone è sbilanciato in basso: Thorik (Guerriero) e Tordek
(Guerriero/Monaco) sono Tier 5, Artemis (Warlock) sta fra 3 e 4 a seconda della
lista, e Hella (Ranger/Druido) porta la magia del Tier 1 dimezzata dal
multiclasse. La campagna compensa già con gli artefatti.

> **La domanda.** In ogni scontro chiave, il PG di Tier più basso ha **una cosa
> che solo lui può fare**? Se il nemico vola, chi non vola e non ha gittata cosa
> fa nei round in quota?

Esempio vero: la prima lettura di `ARC07-DEF-4` (playtester #42) ha trovato
Tordek senza azioni per tre round contro un drago che resta in quota, e con la
Cintura che rifiuta di attivarsi.

## 2 · Volo e invisibilità, dal 5° livello

Dal 5° livello un gruppo vola e si rende invisibile. Un luogo che non ha una
risposta per questo non esiste più: lo si sorvola.

> **La domanda.** Per ogni luogo sorvegliato: *e se volano? e se sono
> invisibili? e se sono silenziosi?* (*silenzio*, o Muoversi Silenziosamente
> che non si sente). Le tre cose un gruppo le fa **insieme**, e la risposta
> deve reggere anche alla somma. La risposta non annulla il piano. Lo **premia e sposta il
> rischio**: chi vede l'invisibile, chi fiuta, cosa scatta sulla soglia, quanto
> dura la pozione, cosa succede all'atterraggio.

Esempio vero: la variante «dall'alto» di `ARC07-DEF-4` Scena 6 è nata perché il
tavolo l'ha fatto, e il modulo non aveva risposta.

## 3 · I tre tiri salvezza

Un modulo che chiede solo Volontà bersaglia sempre lo stesso PG, e ne lascia
tranquillo un altro.

> **La domanda.** Negli scontri del master, gli effetti con un tiro salvezza
> toccano **Tempra, Riflessi e Volontà**? Se uno manca, è voluto?

Le scene di rito e di dialogo non contano: `DEF-2` e `DEF-3` chiedono solo
Volontà, ed è giusto così.

## 4 · Chi sente il rumore

Un luogo con più gruppi di nemici è un sistema. Se nella stanza A si combatte,
cosa fanno quelli della stanza B? La domanda viene dall'ecologia del dungeon che
la DMG 3.5 raccomanda di pensare.

> **La domanda.** Per ogni scontro: **chi sente**, **in quanti round arriva**, e
> **cosa lo ferma**. Un allarme che il modulo non descrive diventa un allarme
> che il DM inventa.

Esempio vero: la seconda lettura di `ARC07-DEF-4` (playtester #24, 🔴) chiedeva
se lo scontro nella tenda facesse suonare il corno che chiama il drago. Il
modulo non lo diceva.

## 5 · Il boss cambia, non si allunga

Un boss solo contro quattro PG cade in due round per l'economia d'azione, e la
cura è quella di `npc-villain-boosting` Gate 2: prima gli sgherri, poi i numeri.
Quello che si aggiunge qui riguarda la **forma**.

> **La domanda.** Il boss ha almeno **una soglia** (di pf, di round, di evento)
> in cui **cambia tattica o cambia il terreno**? Esempio del repo: Skullcrusher
> in `DEF-4`, che a un terzo dei pf **esita** per la prima volta nella sua
> vita, e da lì o muore o fugge nelle paludi.

⚠️ Dentro l'SRD. Recuperare pf fra una fase e l'altra, avere azioni in più per
round o immunità nuove sono **meccaniche inventate**: si scrivono
`[INFERRED — needs DM confirmation]`, passano dal tetto EL ≤ APL+4 e lasciano il
loro `Boost log:`. I boss pronti dei due manuali (Valerius, Xar'Kesh) non si
importano: i numeri non sono verificati e uno è sbagliato («RD 5/Magia e Adamo»).

## 6 · Lo skill challenge si scrive per intero

Lo skill challenge viene dalla DMG di D&D 4e (2008): tanti successi prima di tre
fallimenti, da 4 a 12 secondo la complessità. In 3.5 non esiste. Nel repo è una
convenzione, e una convenzione mezza scritta genera due regole in conflitto.
Ne ha trovate proprio così la prima lettura di `DEF-4` (lettore #21, 🔴).

> **La domanda.** Il testo dice **chi tira** (tutti, uno, una prova di gruppo
> SRD), **cosa tira** (abilità 3.5: niente Atletica, Intuizione, Percezione,
> Furtività), **cosa vale un successo**, **quanti ne servono** e **cosa costa
> ogni fallimento**? Il fallimento costa, e non ferma: è la regola dei «modi di
> fallimento» già misurata da `misura_craft`.

Un solo posto per la regola. Se compare anche nella Quick-Reference o in
un'appendice, dice la stessa cosa.

## 7 · Chi si diverte in questa scena

*Robin's Laws of Good Game Mastering* (Robin D. Laws, 2002) distingue sette
modi di stare al tavolo: chi ottimizza, chi vuole menare, il tattico, il
casuale, lo specialista, l'interprete e il narratore.

Per il gruppo di RumblingStone valgono i **profili veri** di
`rumblingstone-campaign/references/campaign-dm-strategy.md`, che sono più
precisi di qualunque tipologia. I sette modi servono dove il gruppo non si
conosce: gli stand-alone e i moduli per un gruppo nuovo.

> **La domanda** (stand-alone e gruppi nuovi). Fra le scene del modulo, ognuno
> dei sette modi trova almeno **una** scena fatta per lui?

## 8 · Ogni scontro che il master rende possibile ha la sua tattica

Un master non lineare apre scontri che il tavolo può non giocare mai: la
pattuglia che arriva dopo tre fallimenti, il generale che sopravvive e sale
sulle mura, i lupi che fiutano. Se il testo li rende possibili e non dice come
combattono, il DM li inventa al tavolo, ed è proprio lì che un master di
qualità smette di esserlo.

> **La domanda.** Per ogni scontro che il master **rende possibile**, anche solo
> come complicazione o come esito di una scelta: il testo dice **come combatte**
> chi c'è (chi va su chi, cosa fa contro chi vola e contro chi è invisibile),
> **quando smette** (fugge, si arrende, fa quadrato) e **chi sente** (la §4)?
> Le statistiche da sole non bastano: dicono quanto fa male, non cosa fa.

Una riga per caso basta, e i numeri restano quelli dell'SRD e dell'appendice.
Dove la tattica aggiunge un fatto che il canone non ha (un'altezza, un tempo
d'arrivo), si scrive `[INFERRED — needs DM confirmation]` finché il DM non lo
conferma.

Esempio vero: il DM, preparando la seconda serata di `ARC07-DEF-4`
(2026-10-12), ha chiesto se gli scontri, *anche quelli ipotetici*, avessero le
tattiche. Le avevano Zog'tar, Balvar, Skullcrusher e il drago sulla tenda; non
le avevano la pattuglia dei tre fallimenti, la squadra dei lupi, gli sciamani,
le guardie della tenda e Zog'tar sulla breccia all'alba.

## 9 · Il segreto e la divinazione, dal 9° livello

Sotto l'11° livello un modulo può nascondere un'informazione; sopra, i PG la
ottengono quando vogliono (Ryan Dancey, giudice di RPG Superstar 2011). Al 13°
il gruppo ha *divinazione*, *comunione*, *leggende e tradizioni*, *scrutare*,
*localizza creatura*. Un'indagine o un colpo di scena che regge solo sul segreto
cade alla prima lancia.

> **La domanda.** Per ogni segreto del master: **quale incantesimo lo rompe**,
> **cosa ottiene chi lo lancia**, e **come prosegue il modulo** se lo rompono?

La risposta giusta non è la schermatura, che toglie una capacità ai giocatori e
li punisce per averla usata. È il modulo che cambia strada e premia chi ha
lanciato: un nome in più, una scena saltata, un nemico che se ne accorge. Si
scrive in un blocco **«Se lo divinano»**, uno per master, una riga per segreto.
Vale anche per i testimoni: il TS Volontà di chi si interroga, e cosa succede
con *charme*, *zona di verità*, *individuazione dei pensieri*, *parlare con i
morti* (`rumblingstone-indagine` per la forma del nodo).

È la §2 applicata ai segreti invece che ai luoghi.

## 10 · Ogni scontro ha la sua riga di scala

La sidebar «Scalare lo scontro» della checklist è per il boss. Pathfinder
Society ne mette una a **ogni** combattimento, in una frase, e la lega alla
storia. Per un gruppo fisso di quattro serve soprattutto quando un PG manca: è
già successo, con Hella morta fino alla resurrezione di DEF-3.

> **La domanda.** Lo scontro dice cosa cambia **con tre PG** e **con cinque**?

Non «togli un hobgoblin», ma chi manca e dove si sposta l'altro: *«con tre PG
manca il sergente, rimasto al corno: l'allarme parte un round prima»*. I numeri
restano quelli dell'appendice; la riga dice solo chi c'è. Un modulo che scala
in un indice maestro (l'Abbazia) lo dichiara nel profilo e non ripete la riga.

## 11 · Il mostro che nessun altro sostituisce

Il giudice developer di RPG Superstar, e prima di lui un concorrente: *se
cambiassi questo mostro con un altro dello stesso GS, l'incontro funzionerebbe
ancora?*

> **La domanda.** Il nemico fa **qualcosa che un altro dello stesso GS non
> farebbe**? Se no, è un segnaposto, e il GS si spende meglio altrove.

Vale doppio per il villain. Quello che piace di più non se ne va dopo aver
parlato: la critica più netta del 2016 è stata la strega che sparisce a metà
scontro, che sarebbe stata il villain giusto.

## 12 · Il pericolo che qualcuno usa

*«Perché non c'è niente che spinga i PG nel magma?»* (Steven T. Helt, RPG
Superstar 2016).

> **La domanda.** Ogni pericolo della mappa (lava, precipizio, corrente, fuoco)
> ha **almeno un nemico che ci spinge dentro i PG**, e i PG possono usarlo
> contro i nemici?

Un pericolo che nessuno usa è scenografia, e allora va nel box, non nelle
tattiche.

## 13 · L'incontro che resta uno

> **La domanda.** Nell'ordine in cui il tavolo probabilmente lo gioca, lo
> scontro **resta uno**, o diventa due di seguito, ognuno più debole?

Succede quando i nemici sono in due stanze, o quando la trappola scatta solo
dopo. Lo scontro diviso costa due volte il tempo e la metà della tensione: o si
uniscono (i secondi arrivano al round 2, e lo si scrive) o si dichiarano due
incontri con il loro EL.

## 14 · Il rinforzo che i PG vedono arrivare

*«Il DM sa che arrivano i rinforzi, i PG no»*, quindi non c'è urgenza (Owen
K.C. Stephens). La §4 dice chi sente e in quanti round arriva; questa dice se
**il tavolo** lo sa.

> **La domanda.** Se arrivano rinforzi, i PG hanno **un segno che li avverte**
> prima che arrivino: un corno, dei passi, una porta che sbatte, un conto alla
> rovescia?

## 15 · Niente dossi al 13°

Un gruppo di nemici di GS basso, dal 9° livello in su, sparisce con un
incantesimo ad area. Paizo li chiama *speed bumps*, dossi: costano spazio e
tempo e non tolgono risorse.

> **La domanda.** Se lo scontro ha **sei o più nemici contati**, il testo dice
> cosa li tiene in vita (copertura, dispersione, ondate, un capo che li
> raduna)? Oppure diventa **un boss e un luogotenente**?

Un'orda che serve a dare l'allarme o a coprire una fuga può morire in un round:
allora lo si scrive, e il rilievo si chiude con la ragione.

## 16 · Il PG fuori gioco per un tiro salvezza

*Dominare*, *paralizzare*, *pietrificare*, *blocca persone*, *confusione*:
effetti che con un TS fallito tolgono un giocatore dal tavolo per molti round.
Sono legali e fanno paura, ed è giusto che ci siano. Il problema è il giocatore
che guarda.

> **La domanda.** Per ogni effetto «salva o sei fuori» negli scontri: come ne
> esce il PG (**un nuovo TS**, un alleato che lo libera, la durata), e **cosa fa
> il giocatore** nel frattempo (un PG dominato lo muove lui, con gli ordini del
> nemico)?

Stordito e frastornato durano di norma un round, e non contano. La versione più
forte dell'effetto resta: la domanda chiede la via d'uscita, non lo toglie.

## 17 · Le domande nate dai giri su ARC-07

Le quattro domande che seguono non vengono da un manuale. Sono quelle che i
developer dei due giri del 2026-10-18 su ARC-07 si sono fatti da soli, e due
hanno prodotto i 🔴 del secondo giro. Valgono per ogni scontro.

> **Chi vede al buio.** Per ogni luce, ombra o occultamento che il master usa:
> chi dei presenti ha scurovisione, vista cieca, percezione tellurica o fiuto, e
> l'ombra serve ancora contro di loro? *(il fondo buio della tenda di DEF-4 dava
> occultamento contro guardie con scurovisione)*

> **CA e pf di ogni bersaglio.** Ogni creatura che il modulo mette sotto
> attacco, alleati e PNG da proteggere compresi, ha CA e pf scritti, o una
> soglia a colpi dichiarata. *(in DEF-5 mancava la CA di Re Thorek, l'unico
> bersaglio della scena)*

> **In che riga di scala sta il gruppo di stasera.** La riga di scala (§10)
> dice anche quale riga vale per il gruppo che giocherà, contato con i PG e i
> livelli dello stato attuale.

> **L'economia d'azione SRD.** Per ogni mostro che fa più cose in un turno
> (emerge e morde, vola e soffia, attacca e si ritira): ogni pezzo è un'azione
> che l'SRD gli concede, o serve un talento che non ha? *(gli Xorn di DEF-1
> emergevano, mordevano e si rituffavano nello stesso turno senza Attacco
> Rapido)*

## 18 · La domanda della scena

Per The Angry GM ogni incontro risponde a una domanda drammatica, una domanda
sì o no che il DM conosce prima di cominciare ([*Four things you've never heard
of that make encounters not suck*](https://theangrygm.com/four-things-youve-never-heard-of-that-make-encounters-not-suck/)).
Se il DM non sa cosa è in gioco, la scena finisce quando finiscono i pf, e un
negoziato non finisce mai.

> **La domanda.** Ogni scena giocabile, di scontro o sociale, dichiara in una
> riga **la domanda sì o no** a cui risponde?

La forma è fissa, in testa alla scena, sotto la riga *In scena*:

```
**Domanda:** gli Xorn lasciano passare il gruppo senza prendersi il mithral?
```

oppure `**Posta in gioco:** … ?`. Un **Obiettivo** scritto come tale vale
anche lui (la guida agli scontri di ARC-08 li ha). La domanda resta aperta:
*«il re muore?»* in una scena dove il re muore comunque non è una domanda, è
un annuncio. La regola D18 guarda le scene con un tiro di scontro o con
Diplomazia, Raggirare, Intimidire o Percepire Intenzioni; il tempo libero con
l'orologio a tacche e le scene raccontate si dichiarano con la ragione.

## 19 · La scelta che si vede

Una scelta dei giocatori conta se la sua conseguenza **si percepisce**
(Wardrip-Fruin, Mateas, Dow e Sali, [*Agency Reconsidered*](https://www.cs.uky.edu/~sgware/reading/papers/wardripfruin2009agency.pdf),
DiGRA 2009). Il master che scrive «Se i PG…» e poi non dice dove torna quella
scelta lascia al DM ricordarsene.

> **La domanda.** Ogni blocco di scelta («Se i PG…», un **Se** in grassetto
> retto dai PG, le opzioni **A**, **B**, **C**) dice **dove si vede** la
> conseguenza?

Basta un rimando: `→ Scena 8`, un paragrafo (`§7`), un'eco, il carry-over,
l'Echo Ledger, l'esito della scena (► **Esito**), l'orologio, un cambio
permanente sulla scheda, o la parola *Conseguenza*. Il blocco è il paragrafo,
o la fila di paragrafi attaccati che si aprono con una scelta; un titolo
`#### Se i PG…` vale fino al titolo dopo. Nelle scene di scontro un **Se** in
grassetto è quasi sempre tattica, e la conseguenza si vede al round dopo: lì
la D19 guarda solo «Se i PG…» e le opzioni.

## 20 · Il cattivo si annuncia

Bryce Lynch chiede a ogni modulo che recensisce che il cattivo si faccia
conoscere prima dello scontro ([lo standard di tenfootpole](https://tenfootpole.org/ironspike/?page_id=1201)).
Un boss che arriva senza essere mai stato nominato è un mostro grosso, non un
nemico.

> **La domanda.** Il boss è **nominato o indiziato in almeno due scene** prima
> di quella dello scontro?

Un nome detto da un PNG, un'impronta, un corno, un'ombra che passa sopra il
campo: basta che stia nel testo della scena. La D20 prende i nomi dal titolo
della scena del boss e dalla sua *Scheda d'entrata*; un indizio che non porta
il nome («il drago», «le ali nere») si dichiara nel profilo del master in
`plans/domande-developer.json`, alla voce `presagi`. Un modulo in più file
(la guida di ARC-08 e la sua guida agli scontri) può avere il presagio
nell'altro file: allora il rilievo si chiude con la ragione.

## 21 · La rete degli indizi, marcata

La Three Clue Rule (Justin Alexander, [*The Three Clue Rule*](https://thealexandrian.net/?p=7985)):
per ogni conclusione che i PG devono raggiungere, **almeno tre indizi**. La
norma del repo la scrive già (`rumblingstone-indagine/references/nodi-e-sei-porte.md`
§4: ogni conclusione necessaria si raggiunge da almeno due nodi diversi), ma
nessun master la marca, e nessuno la poteva contare.

> **La domanda.** Ogni conclusione necessaria ha **almeno tre indizi**, sparsi
> in **almeno due nodi** diversi?

La marcatura è un commento HTML, che in stampa non si vede:

```
<!-- conclusione C1: la profezia della targa parla dei PG -->
...
#### 🔍 Nodo d'indizio — la targa di bronzo
| **Nome** <!-- indizio C1 --> | ...
```

La conclusione si dichiara una volta, dove il DM la legge per prima; ogni
indizio porta il suo `<!-- indizio C1 -->` (o `C1, C3` se ne regge due). Il
nodo è il titolo *Nodo d'indizio* o `N3 — …` sotto cui sta l'indizio,
altrimenti la scena. La D21 conta solo dove la marcatura c'è: il 2026-10-22
nessun master la usa, e la regola non dà rilievi. Un master nuovo con
un'indagine la marca, e da lì il cancello vale.

## Come si scrive un rilievo del developer

Il developer scrive una riga per rilievo, in questa tabella:

| # | Scena | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|

Il **codice** è la sezione di questo file a cui il rilievo risponde, seguita
dal tipo: `§8 · regola` (un numero o una regola contro l'SRD, con l'URL del
mirror), `§1 · contraddizione` (due punti del master che dicono cose diverse),
`§10 · manca` (il dato che la domanda chiede non c'è), `§17 · regola`, e così
via. Un rilievo che non risponde a nessuna sezione usa `§0 · altro`. La prova
è la citazione fra « » dal master, e dall'SRD dove serve.
