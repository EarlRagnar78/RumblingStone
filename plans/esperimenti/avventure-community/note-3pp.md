# Note di ricerca — avventure di terze parti per D&D 3.5 e PF1e

*Ricercatore: agente, 2026-10-18. Base di confronto: `brief-standard-attuale.md`.*

Legenda delle fonti:
- **[LETTO]** = ho letto il testo alla fonte indicata (anteprima ufficiale DriveThruRPG, pagina del
  recensore, pagina dell'editore). Le citazioni sono tradotte o riportate brevi.
- **[RECENSIONE]** = quello che un recensore dice del prodotto; il prodotto non l'ho letto.
- **[DEDOTTO]** = mia inferenza o ricordo non verificato in questa sessione.

Non ho usato copie pirata (Scribd, spawningpool, dokumen.pub, z-library compaiono nei risultati
di ricerca: le ho escluse di proposito). Le anteprime ufficiali di DriveThruRPG
(`d1vzi28wh99zvq.cloudfront.net/pdf_previews/<id>-sample.pdf`) sono le prime 6-8 pagine messe
a disposizione dall'editore.

Verifiche nel repo prima di proporre (sola lettura, grep):
- la mappa per i giocatori senza porte segrete né trappole **esiste già** come controllo D9 in
  `skills/rumblingstone-mapmaking/references/collaudo-mappe.md:131`;
- le tabelle di incontri casuali legate agli orologi **esistono già** come principio in
  `skills/rumblingstone-narrative-style/references/living-world.md:133`;
- in `skills/rumblingstone-module-standard/` non trovo occorrenze di: anelli/loop nelle mappe,
  tabella degli incontri riassuntiva, elenco degli statblocchi, schermature/rilevazioni,
  mostri erranti. Sono quindi i candidati più netti.

---

## 1. Necromancer Games / Frog God Games

### Che cosa voleva dire «Third Edition Rules, First Edition Feel»

**[LETTO]** Clark Peterson, citato da Black Gate
(https://www.blackgate.com/2015/11/09/of-necromancers-frog-gods-part-one/): il «feel» riguarda
«la scelta dei mostri, lo stile di gioco, le influenze e l'ambientazione»; è «il Vault of the Drow
e non Drizzt», «la Tomb of Horrors e non le Rovine di Myth Drannor», «Tolkien, Moorcock, Howard e
Leiber, non Eddings, Hickman, Jordan e Salvatore». Wikipedia aggiunge l'aspetto grafico:
numero del modulo in alto a sinistra, banda diagonale, illustrazioni inserite nel testo
(https://en.wikipedia.org/wiki/Necromancer_Games).

Quindi lo slogan è un **gusto**, non una regola. In pratica, dalle anteprime:

**[LETTO] Rappan Athuk PF (2012)**, anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/112601-sample.pdf):
- Introduzione dichiaratamente anti-ecologica: «perché ci sono 16 troll in una caverna con una
  *jug of alchemy*? A nessuno importa. […] Non è un esperimento di ecologia, è un dungeon».
- Soglie d'ingresso esplicite: i primi livelli non vanno tentati con meno di sei PG di 4°; dal 3°
  livello in giù 5°+; l'ingresso dal «Pozzo» sotto il 7° è sconsigliato.
- Una voce che tutti i sopravvissuti ripetono: **«Non scendete nel Pozzo»**. È un'avvertenza
  diegetica unica e memorabile, un presagio che il tavolo ricorda.
- Ringraziamenti: «446 personaggi uccisi da quando ho concepito questo posto». È un collaudo
  dichiarato in forma di numero di morti, più trent'anni di tavoli e i demo team GenCon 2001-2005
  elencati per nome fra i playtester.
- Il livello 15 «è solo da leggere per il GM: Orcus deve restare imbattibile».
- Appendici: pregenerati, **mappe da battaglia** (pp. 600-637), divinità.

**[RECENSIONE] Intestazione di livello Necromancer** (Rappan Athuk Reloaded, recensione su
directorygold: http://directorygold.com/a-review-of-the-role-playing-game-supplement-rappan-athuk-reloaded/).
Ogni livello apre con una tabella fissa:
- **Livello di difficoltà**: il livello a cui un gruppo di sei PG è messo alla prova;
- **Ingressi** e **Uscite**: da dove si arriva e dove si va (altri livelli, superficie);
- **Mostri erranti**: tabella breve;
- **Schermature**: effetti che impediscono divinazioni;
- **Rilevazioni**: che cosa rivelano le divinazioni generiche su quel livello;
- **Effetti continui**: quello che vale per tutto il livello;
- **Caratteristiche standard**: porte, pareti, luce;
- (in alcune versioni) **funzionamento e recupero degli incantesimi**.

La stessa recensione critica il prodotto perché statistiche e mappe stanno in volumi separati
dal testo: per giocare bisogna stampare due libri su tre.

**[RECENSIONE] Bryce Lynch su Rappan Athuk** (https://tenfootpole.org/ironspike/?p=1008):
interconnessione «seconda a nessuno», «almeno diciassette ingressi», stanze come set piece; ma
«troppe parole per descrivere molte stanze», nessuna fazione visibile, poco presagio. Nei
commenti: «un tritacarne, almeno un personaggio morto a sessione».

**[LETTO] The Grey Citadel PF**, anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/335343-sample.pdf). È il pezzo più utile
di tutta la ricerca per noi:
- **Tre tipi di incontro con notazione propria**: *Chiave* (lettera della mappa + numero: D-1;
  i livelli del dungeon 2-9), *A tempo* (giorno.evento: «1.2 è il secondo evento del primo
  giorno»), *Casuali* (tabella cittadina). Gli incontri a tempo «si possono spostare o annullare
  senza rompere la trama».
- **Regola del tre a livello di struttura**: tre elementi del mistero (mago, ladri, demoni), ogni
  elemento con tre vie d'accesso (tre indizi del mago, tre furti, tre cittadini sedotti); tre
  eventi a tempo per ciascuno dei primi tre giorni.
- **L'indagine paga nel dungeon in moneta tattica**: «il buon lavoro investigativo in città viene
  premiato con informazioni sul dungeon: chi lo occupa, le debolezze, le armi da usare». Esempio
  dato: portare l'acido per il troll. Il modulo dice anche che un 5° livello «si presume abbia
  indagato bene» e quindi abbia quei vantaggi.
- **Cronologia con giorni negativi** (–1 mese … –1 giorno, Giorno 1, 2, 3, 4+) per rispondere alle
  domande «quando?» dei giocatori, più: «a ogni ritorno in città sottolineate il deterioramento».
- **Personaggi di rimpiazzo scritti come PNG** della storia: Rasputin, Fitch, Brother Melph,
  Stump, Yelm possono unirsi al gruppo se cala di numero; il testo avverte che consegnarli troppo
  presto rompe i loro ruoli.
- **Adattare l'avventura**, con una regola semplice: i tre capi devono avere «circa il doppio dei
  punti ferita della media del gruppo», gli avversari minori «pari o un livello sotto» il gruppo.
- **Politica del read-aloud**: c'è solo per PNG importanti e luoghi difficili da visualizzare;
  «dove manca, la descrizione è scritta per essere parafrasata».
- La tabella degli incontri casuali cittadini serve anche a «consegnare una voce al momento
  giusto»: incontro casuale come veicolo d'indizio.

**[RECENSIONE] sulla stessa Grey Citadel**: ENWorld (https://www.enworld.org/threads/the-grey-citadel.118592/)
loda gli statblocchi dentro ogni incontro e il fatto che «non ci si può bloccare, ci sono vari
modi di affrontare il problema»; segnala errori di statistiche (tre PNG con Ambidestria senza il
prerequisito), nessun indice, nessuna chiave sulle mappe, cinque luoghi con sottoaree senza
mappa. Bryce Lynch (https://tenfootpole.org/ironspike/?p=9166) la stronca: «pagine intere di
statblocchi compressi in corpo piccolo», «quasi una pagina per descrivere la segheria», read-aloud
da quindici minuti.

**[LETTO] Stoneheart Valley PF** (contiene The Wizard's Amulet, Crucible of Freya, Tomb of
Abysthor), anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/176362-sample.pdf):
- «Using this Adventure» in sei passi numerati con obiettivo: «giocare entro quindici minuti».
- Una frase di collaudo dentro il testo: «**Il playtest dimostra che questa composizione del
  gruppo dà le migliori probabilità di successo**», seguita dalle correzioni per gruppi più
  piccoli o meno combattivi.
- **Informazioni supplementari segrete per un solo giocatore** (quello di Corian), da consegnare
  dopo la scelta dei personaggi e da rivelare a sua discrezione.
- «Side box» a margine con tattiche dei mostri, riassunti delle trappole, cose da ricordare.
- La «regola d'oro» Frog God: «usate ciò che volete, scartate o cambiate il resto».
- Crediti agli utenti del forum che hanno compilato il thread di errata del Tomb of Abysthor:
  l'errata della comunità entra nella revisione ed è ringraziata per nome.

**[RECENSIONE] Lost City of Barakus**, Endzeitgeist
(https://www.pathfinderinfinite.com/product_reviews_info.php?&reviews_id=135035&products_id=142507):
«la definizione da manuale di un sandbox vasto e aperto», città con statblocchi di insediamento,
molte mappe; manca il voto pieno perché mancano **mappe per i giocatori di tutte le aree**.
ENWorld: un gruppo lo ha giocato per circa 35 sessioni
(https://www.enworld.org/threads/which-necromancer-games-adventures-worth-getting-avoiding.254265/).

**[RECENSIONE] Slumbering Tsar**: fazioni dentro la cittadella, incontri fissi più casuali per
ogni area della Desolazione, eventi del campo che «avvengono nell'arco di più visite», PNG da
salvare che fanno da rimpiazzi, letalità dichiarata; manca l'indice e mancano i segnalibri, cosa
grave per un libro così rimandato a sé stesso
(http://directorygold.com/a-review-of-the-role-playing-game-supplement-the-slumbering-tsar-saga/).
Endzeitgeist sulla parte 5 loda nemici «finalmente intelligenti» e un enigma che premia chi ha
seguito il retroscena (https://www.gmsmagazine.com/slumbering-tsar-the-hidden-citadel-part-5-the-mind-of-chaos/).

---

## 2. Raging Swan Press (Creighton Broadhurst)

**[LETTO] Principi dichiarati** (https://www.creightonbroadhurst.com/raging-swan-press/):
- «Il GM non dovrebbe passare otto ore a preparare una sessione di quattro».
- **«Tutto su una pagina»**: «tutte le informazioni su un argomento stanno su una o due pagine
  affiancate»; «per le avventure, una volta disegnata la mappa dell'incontro, tutto il resto che
  serve al GM sta su una o due pagine affiancate»; «il GM non dovrebbe mai andare a cercare
  un'informazione vitale nascosta altrove nel modulo».
- Statblocchi, PNG, mappe e incontri estraibili e modificabili singolarmente.
- Avventure «più di una serie di combattimenti debolmente collegati».
- Stampa economica: niente fondi pieni a colori che consumano cartucce; doppio PDF, uno
  ottimizzato per la stampa e uno per lo schermo (confermato da Endzeitgeist su Agravaine's Rest,
  https://www.gmsmagazine.com/rpg-review-village-backdrop-agravaines-rest/).

**[LETTO] Retribution (ed. 2022)**, anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/387357-sample.pdf). La struttura si vede
dall'indice:
- **Elenco degli statblocchi** in apertura: tabella *statblock · grado di sfida · appendice ·
  parte (incontro)*.
- **Combattimenti e incontri numerati, luoghi indicati per lettera** («per vostra comodità»).
- Ogni parte apre con **«Running [parte]»**: *Cosa sanno i personaggi*, *La tempesta che
  arriva* (l'ambiente), *Dressing dell'ambiente*, **Troubleshooting**; nella parte II anche
  *Interpretare il clero* e *Cronologia degli eventi*; nella III *Pacing*.
- Nella parte del dungeon: *Riassunto dei luoghi* e *Riassunto degli incontri* su una pagina.
- **Cast in doppia forma**: «Folk of Cymer — Player Handout» (pag. 22) e «Folk of Cymer — GM
  Reference» (pag. 66). Lo stesso elenco di persone, una versione per il tavolo e una per il DM.
- *Daily Life at Cymer* e *Things to do at Cymer*: che cosa possono fare i PG nei giorni
  d'attesa.
- Ganci con un motivo diverso per ogni personaggio («personaggi diversi potrebbero avere ragioni
  diverse; lasciate tempo nella parte II per chiudere ciascuna missione»).
- Il sommario indica per ogni parte chi è l'avversario principale (nella parte I è la tempesta).
- Crediti con **Development** separato dal **Design** e **Playtesters** per nome.
- Riedizione dopo dodici anni con «molte revisioni, chiarimenti e correzioni»; aggiornamento
  successivo di *Shadowed Keep* con «appendici di statblocchi riorganizzate per rendere più facile
  condurre l'avventura» (https://www.ragingswanpress.com/). Statblocchi dentro l'incontro **e**
  raccolti in appendice: le due cose insieme.

**[RECENSIONE] Road of the Dead**, Endzeitgeist (https://www.gmsmagazine.com/road-of-the-dead/):
incontri autosufficienti, con le regole riassunte dentro l'incontro (tabelle per il combattimento
in acqua), così il GM non deve sfogliare il manuale; l'ha condotta dopo un'ora di lettura. Mappa
per i giocatori, tabella dei tempi di viaggio per diverse velocità, illustrazioni dei luoghi per i
giocatori, «niente scomparti segreti sulle mappe dei giocatori».

**[LETTO] Articoli del blog**
(https://www.ragingswanpress.com/swan-blog/dungeon-design-tips-for-beginners e
https://www.ragingswanpress.com/swan-blog/dressed-vs-undressed-an-example-of-play):
- «Pochissime aree di un dungeon sono spoglie»; le tracce degli abitanti e dei predecessori
  premiano chi osserva; «premiare i giocatori che colgono gli indizi alza il livello del gioco»,
  ma senza descrivere troppo.
- Esempio di scala «vestita»: il centro dei gradini consumato «come dal passo di molti piedi»,
  lichene grigiastro su metà del gradino sotto la crepa. Il dettaglio fa scegliere ai giocatori
  (stare lontani dalla crepa e dal lichene): è dressing **giocabile**, non decorativo.

**[LETTO] Interviste** (Tribality 2015, https://www.tribality.com/2015/01/12/interview-with-creighton-broadhurst-of-raging-swan-press/;
randroll, https://www.randroll.com/interview_raging_swan/). Onestà: **non** parlano di
impaginazione, editing o playtest. Dicono: ridurre le barriere d'ingresso e il lavoro del GM;
contro l'inflazione di regole («liste infinite di talenti»); «scrivere una tabella casuale è
diverso dallo scrivere testo d'avventura: descrizioni succinte e saporite»; le tabelle «20 Things»
sono nate al suo tavolo.

**[RECENSIONE] Critiche a RSP** — Bryce Lynch, che dà la misura opposta:
- *Shadowed Keep on the Borderlands* (https://tenfootpole.org/ironspike/?p=2895): «96 pagine,
  circa 20 di contenuto»; «una stanza vuota sono quattro paragrafi»; «un muro di testo»; «finta
  organizzazione»; i mostri erranti «sono solo statblocchi». Salva **la cronologia** (i banditi
  della torre in schermaglia con i goblin del dungeon).
- *Gibbous Moon* (https://tenfootpole.org/ironspike/?p=2859): «il testo che descrive cose normali
  è testo sprecato: ci serve descritto l'insolito»; tabella casuale per le stanze vuote inutile,
  «metteteci le cose e basta»; il cattivo con dieci-undici paragrafi di descrizione è troppo per
  il tavolo; «non concentratevi sui moduli, né sugli statblocchi: concentratevi sull'avventura».

Morale onesta: il formato RSP è disciplinato nella **navigazione** (elenchi, numerazione, pagine
affiancate, doppio PDF), meno nella **densità** del testo.

---

## 3. Kobold Press / Open Design

Onestà: **qui ho letto poco**. I saggi dei *Kobold Guide* non sono liberamente disponibili e ho
escluso le copie pirata. Ho letto solo riassunti di recensioni:
- Know Direction sul vol. III (https://knowdirectionpodcast.com/2010/06/kgtgmiii/2/): Baur,
  *Location as a Fulcrum for Superior Design* (il luogo come leva dell'immersione); Baur,
  *Buckets in the Sandbox: Non-Linear and Event-Driven Design* (mondo aperto in cui i giocatori
  controllano il ritmo con cui scoprono la trama); Monte Cook, *Myths & Realities of Game Balance*;
  Baur, *Collaboration and Design* (scrittori, artisti, editor e **playtester** fanno il prodotto);
  Greenwood, *Crafting a Dastardly Plot*, giudicato elementare.
- Goodreads (https://www.goodreads.com/en/book/show/17177271-complete-kobold-guide-to-game-design):
  più recensori lo trovano motivazionale e astratto più che operativo.
- *Streets of Zobeck* (Gold ENnie Best Adventure 2012, https://pathfinderwiki.com/wiki/ENnie_Awards)
  è criticato su RPGGeek come «un binario verso un noir poco noir» (titolo del thread; il testo
  non era raggiungibile).

**[DEDOTTO]** Per noi il valore di Kobold è il modello di **design per patronato** (Open Design:
i sostenitori commentavano le bozze), che somiglia al nostro ciclo con revisione; non ho trovato
una regola di formato specifica da importare. Se serve approfondire, il saggio da leggere è
*Buckets in the Sandbox*.

---

## 4. Goodman Games, Dungeon Crawl Classics per 3.5 (2003-2008)

**[LETTO] DCC #37 The Slithering Overlord (3.5)**, anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/24077-sample.pdf):
- Crediti con **Playtesters** per nome e figure distinte di line editor e proofreader.
- **Encounter Table** «per aiutare il GM a prepararsi»: colonne *Loc* (numero sulla mappa),
  *Pg* (pagina), *Type* (T trappola, P enigma, C combattimento, anche combinati C/T), *Encounter*
  (nomi in corsivo = PNG con classi), *EL*. Trenta e più righe, il boss a EL 12 su un modulo
  per il 4°.
- **Chi brilla**: l'introduzione dice quali PG servono (druidi e ranger, «di solito limitati al
  chiuso», un nano, un elfo per le porte segrete, Sopravvivenza).
- **Tre fazioni in competizione** nel complesso (grimlock con un drider, duergar, trogloditi di una
  naga); «i PG devono superarne almeno due per il successo completo»; i nemici sono numerosi ma
  disuniti, e questo aiuta il gruppo.
- **Scaling Information** in due paragrafi con istruzioni meccaniche precise: gruppi deboli, un
  avversario di GS 1 in meno per incontro, pf dei mostri singoli ridotti di un terzo, livelli di
  classe −1/−2; gruppi forti, due livelli o DV ai tre capi nominati, un secondo mostro solitario
  «se lo spazio lo permette», tesoro adeguato.
- **Recurring Creatures**: i tratti razziali comuni (vista cieca dei grimlock, fetore dei
  trogloditi) scritti **una volta**, all'inizio, «per risparmiare spazio»; negli statblocchi solo
  le varianti.
- Appendice di mostri e **Player Handouts** separati.

**[LETTO, solo descrizione]** I moduli torneo (DCC #13, #30 *Vault of the Dragon Kings*, #49
*Palace in the Wastes*) includono «il sistema di punteggio ufficiale del torneo, personaggi
pregenerati e handout illustrati» (descrizione del prodotto,
https://www.drivethrurpg.com/en/product/12367/Dungeon+Crawl+Classics+%2330%3A+Vault+of+the+Dragon+Kings).
Non ho letto il sistema di punteggio.

**[RECENSIONE]** ENWorld su *From Here to There* (Goodman): utile lo Scaling in ogni avventura,
tabella con tipo d'incontro, ma **numeri di pagina sbagliati** nella tabella
(https://www.enworld.org/threads/review-of-from-here-to-there-by-goodman-games.298558/).
Bryce Lynch su DCC #36 (https://tenfootpole.org/ironspike/?p=947): «è lo stile della 3E: è
impossibile trovare qualcosa nel testo»; «un quarto di colonna di statblock per lei e il suo
gatto famiglio»; «CD dei muri delle capanne, CD dei forzieri di metallo»; mappa a corridoio unico.
Su DCC #50 di Monte Cook (https://tenfootpole.org/ironspike/?p=866): «se i personaggi devono
superare una prova per completare l'avventura, l'avete scritta male» — la prova come **tassa**.

---

## 5. Legendary Games, AAW Games, Rite, Lost Lands, ENnies

**ENnies Best Adventure 2008-2014** (https://pathfinderwiki.com/wiki/ENnie_Awards,
https://ennie-awards.com/portfolio-item/2014-nominees-and-winners/): Paizo Gold 2008-2011 e 2013;
*Streets of Zobeck* (Open Design) Gold 2012; *Razor Coast: Heart of the Razor* (Frog God) Silver
2014; *Rise of the Drow* (AAW) nominato 2014. Necromancer: Gold Best Adventure 2004 per *Lost City
of Barakus*, Silver per cartografia e impaginazione 2003 (Wikipedia, sopra).

**[LETTO] Rise of the Drow (AAW)**, anteprima ufficiale
(https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/126800-sample.pdf):
- Tesoro con **tabella di storia**: per ogni oggetto *età, origine, bonus, magia, aspetto*, e una
  seconda tabella *abilità · CD · informazione* (Conoscenze storia CD 25: «archi così erano comuni
  fra gli arcieri d'élite secoli fa»). L'oggetto magico diventa un piccolo indizio di mondo.
- Scelta strategica con conseguenza scritta: se i PG tornano in superficie ad avvisare, i drow
  saccheggiano Embla, si perde la guida Miah e resta solo l'assalto frontale; se proseguono, si
  apre la «Strada di Dietro», più leggera.
- Statblocchi d'insediamento PF (Corruzione, Crimine, Mercato…).
- Due pagine piene di retroscena prima del gancio: è quello che Bryce chiama «epic backstory».
- Endzeitgeist, 5 stelle (https://www.drivethrurpg.com/product_reviews_info.php?&reviews_id=113680&products_id=126800):
  ogni casata con scheda completa (due casate ombra comprese), usabile come sandbox o come AP
  lineare; segnala crunch difettosa e effetti senza dettagli per dissolverli.

**[RECENSIONE] Mini-Dungeon AAW**: 2 pagine, una mappa e il testo, con gli statblocchi
**collegati** al d20pfsrd invece che stampati; Endzeitgeist toglie spesso il massimo per la
mappa senza versione per i giocatori (risultati su pathfinderinfinite.com/dmsguild.com, es.
*Mini-Dungeon #005*).

**[RECENSIONE] Zeitgeist #2 The Dying Skyseer** (EN Publishing), Endzeitgeist
(https://www.storytellersvault.com/product_reviews_info.php?products_id=96300): indagine
ramificata, tabella del cast e lista rapida dei PNG, **undici pagine di mappe a colori per i
giocatori senza chiave**, due pagine di handout, i PNG «reagiscono in modo logico ai PG»; serve un
GM esperto.

**[RECENSIONE] Legendary Beginnings: Crisis at Falling Spring Station** (Endzeitgeist, pagina
recensioni Legendary Games su pathfinderinfinite.com): **la risoluzione non violenta vale più PX
dell'uccisione**; perde il sigillo d'approvazione **solo** per la mancanza di mappe senza
etichette.

### I criteri ricorrenti di Endzeitgeist

Estratti da decine di recensioni (pagine di elenco su drivethrurpg.com e pathfinderinfinite.com
con `customers_id=189525`, più le singole sopra). Sono abbastanza stabili da farne una griglia:

1. **Conteggio delle pagine** in apertura: totale, poi copertina, colophon, pubblicità, OGL, e
   «restano N pagine di contenuto».
2. **Editing su due livelli, sempre separati**: *formale* (refusi, grassetti, maiuscole) e
   *linguaggio di regole* (la regola si applica come scritta?).
3. **Formattazione giudicata sull'uso**, non sull'aspetto: «la formattazione è elementare e non
   aiuta a condurre il libro».
4. **Segnalibri e collegamenti** interni nel PDF, proporzionati alla lunghezza.
5. **Mappe per i giocatori** senza etichette né segreti: la mancanza è la causa più frequente del
   voto non pieno.
6. **Read-aloud distinto** dal testo per il GM con un segno formale.
7. **Errori di statblock** puntuali (prerequisiti, abilità non in grassetto, aspetto mancante).
8. **Coerenza GS-numeri**: «CA 23 e GS 7» non regge; la trappola che non scala.
9. **Le regole devono corrispondere alla storia**: «le regole NON HANNO ALCUNA CORRELAZIONE con la
   storia».
10. **Scalabilità** concreta: premia «4 statblocchi per PNG», uno per fascia di livello.
11. **Abilità del giocatore più dei dadi**; premia le soluzioni non violente.
12. **Durata giocata rispetto al prezzo.**
13. **Sigillo d'approvazione** come soglia sopra le 5 stelle: va a ciò che è innovativo *e* privo
    di difetti d'uso.

### I criteri di Bryce Lynch (Ten Foot Pole)

**[LETTO]** Standard di recensione (https://tenfootpole.org/ironspike/?page_id=1201):
- tabelle di **mostri erranti** necessarie, perché consumano risorse; e i mostri erranti
  **devono fare qualcosa** (pattugliano, cercano cibo);
- i mostri agiscono invece di dormire o fare la guardia; gli umanoidi intelligenti **chiamano
  aiuto** e il modulo dice **quando arrivano i rinforzi**;
- il cattivo va **presagito** prima dello scontro finale;
- **mappe con anelli**: «i dungeon lineari non sono una buona cosa»; i dungeon a più livelli hanno
  più collegamenti fra livelli;
- togliere capacità ai giocatori «raramente è buona cosa»;
- testo **asciutto ed evocativo**, «del vostro retroscena epico non mi importa»;
- il read-aloud in genere è un male (posizione estrema, vedi «cosa non portare»).

---

## 6. Che cosa fanno meglio o diversamente rispetto al nostro standard

Confronto puntuale col brief. Segno ciò che è **nuovo**, ciò che è **già nostro ma fatto meglio
lì** e ciò che è **già nostro e basta** (non lo ripeto).

| Pratica | Chi | Da noi | Giudizio |
|---|---|---|---|
| Tabella degli incontri a colpo d'occhio: luogo, pagina, tipo C/T/P/S, EL | DCC | Quickstart e Quick-Reference con le CD; nessuna tabella degli incontri trovata | **nuovo** |
| Elenco degli statblocchi: nome, GS, appendice, scene | RSP | appendici a lettere | **nuovo** come indice incrociato |
| Tratti ricorrenti scritti una volta | DCC | statblock completi | **nuovo**, riduce lunghezza |
| Intestazione di zona: difficoltà, ingressi/uscite, erranti, schermature, rilevazioni, effetti continui, caratteristiche standard | Necromancer | «dati per il DM», ambiente dinamico | **nuovo**, prezioso al 13° |
| Incontri chiave / a tempo / casuali con notazione (D-1, 1.2) | Grey Citadel | scene in ordine di gioco, eventi d6 | **parziale**: manca la notazione a tempo |
| Cronologia a giorni negativi | Grey Citadel | Echo Ledger, contingenze | **nuovo** come tabella |
| L'indagine paga in vantaggi tattici nominati | Grey Citadel | nodi a tre strati, sei porte | **meglio lì**: il legame indizio → vantaggio è esplicito |
| PNG scritti come rimpiazzi possibili | Grey Citadel, Tsar | sconfitta senza TPK | **nuovo** |
| Boss ≈ 2× pf medi del gruppo | Grey Citadel | calibrazione, tabella DPR | controllo incrociato veloce, non sostituto |
| «Cosa sanno i personaggi» all'inizio di ogni parte | RSP | contratto «In scena» | **nuovo** come riepilogo per il tavolo |
| Troubleshooting per parte | RSP | contingenze «se i PG fanno X» | già nostro |
| Cast in due versioni, per il tavolo e per il DM | RSP | foglio del cast per il DM | **nuovo** il lato giocatori |
| Tutto ciò che serve all'incontro su due pagine affiancate | RSP | numeri in appendice | **diverso**: vedi proposta S2 |
| Statblock dentro l'incontro e raccolti anche in appendice | RSP 2022 | solo appendice | **diverso** |
| Mostri erranti con attività e rinforzi a tempo | Bryce, RSP | tabelle legate agli orologi (living-world) | **meglio lì** la colonna «cosa stanno facendo» |
| Mappa con anelli e più vie fra i livelli | Bryce | developer: volo, invisibilità, chi sente il rumore | **nuovo** come controllo |
| Nessuna prova obbligatoria che blocca l'avanzamento | Bryce | tre indizi per le indagini | **meglio lì**: esteso a porte, passaggi, enigmi |
| Tesoro con tabella di storia e CD | Rise of the Drow | tesoro itemizzato | **nuovo** |
| Tre fazioni, «superarne almeno due» | DCC #37 | nemici con motivazioni | **meglio lì**: condizione di vittoria per fazioni |
| Frasi di collaudo nel testo («il playtest dimostra…») | Stoneheart | rilievi numerati nei report | **nuovo**: il collaudo entra nel master |
| Errata della comunità ringraziata e integrata | Stoneheart, RSP 2022 | ciclo alfa → beta → collaudato | già nostro, manca il registro errata pubblico |
| Mappe per i giocatori senza segreti | tutti | controllo D9 in collaudo-mappe | già nostro |
| Informazione segreta per un solo giocatore | Wizard's Amulet | handout, prop | **meglio lì**: handout privato per PG |
| Read-aloud «scritto per essere parafrasato» quando manca | Grey Citadel | read-aloud ≤12 righe + dati DM | **nuovo** come regola di scrittura dei dati DM |
| PX maggiorati per risoluzione non violenta | Legendary | PX ad hoc, ≥2 vie non combattive | **meglio lì**: incentivo numerico |
| Editing formale e di regole verificati separatamente | Endzeitgeist | audit meccanico in 7 passate | già nostro sulle regole; il formale è dell'editoria |
| Segnalibri e doppio PDF stampa/schermo | RSP, Endzeitgeist | booklet e PDF | da verificare in `editoria` (non controllato) |

---

## 7. Proposte concrete

Ogni proposta ha un nome breve, chi la misurerebbe (G3) e dove andrebbe.

### DEF (master definitivo)

- **D1 · Tabella degli incontri.** In testa al master, dopo il Quickstart: *Codice · Pagina ·
  Tipo (C combattimento, S sociale, T trappola, P enigma, E esplorazione, combinabili) · Chi/che
  cosa · EL · Vie non combattive (n)*. Si misura: ogni scena con EL nel corpo ha la sua riga, e
  il numero di pagina corrisponde (l'errore che ENWorld rimprovera a Goodman). Rende anche
  visibile la **miscela** dei tipi sull'intero modulo.
- **D2 · Elenco degli statblocchi.** In testa alle appendici: *Statblock · GS · Appendice · Scene
  dove compare*. Si misura con un incrocio meccanico fra statblocchi in appendice e richiami nelle
  scene: nessun orfano da nessuna delle due parti.
- **D3 · Intestazione di zona** (Necromancer), per ogni dungeon, edificio o area chiusa: *Livello
  di sfida · Ingressi · Uscite · Erranti · Schermature · Rilevazioni · Effetti continui ·
  Caratteristiche standard*. Al 13° livello è il punto: chiaroveggenza, *scrutare*,
  *teletrasporto*, *individuazione del male*, *localizza oggetto* sono domande che il DM riceve
  al primo minuto. Campo obbligatorio misurabile (presenza delle otto voci).
- **D4 · Notazione degli incontri a tempo** (giorno.evento, `2.3`) e **cronologia a giorni
  negativi** per gli archi con indagine o assedio. Gli eventi a tempo dichiarano se si possono
  spostare o annullare.
- **D5 · «Cosa sanno i PG»** in apertura di ogni atto: tre-cinque righe di fatti già in mano al
  tavolo. Serve dopo una pausa fra sessioni, ed è il contrario del read-aloud: elenco, non prosa.
- **D6 · Cast in due versioni.** Oltre al foglio del cast per il DM, una scheda per i giocatori
  con nome, ruolo in una riga, dove l'hanno incontrato. È anche il modo di rispettare «un nome
  proprio nuovo per box» senza perdere i nomi già usati.
- **D7 · Rimpiazzi in scena.** Ogni atto con rischio di morte nomina uno o due PNG che possono
  entrare nel gruppo, con il momento dopo il quale consegnarli non rompe la trama. Si misura:
  presenza per atto con scontro di EL ≥ APL+2.
- **D8 · Tesoro con storia.** Per gli oggetti non banali, due colonne: *aspetto / origine* e
  *abilità · CD · che cosa si scopre*. Si collega all'Echo Ledger quando l'origine è un PNG.

### Incontri

- **I1 · Indizio → vantaggio tattico.** Ogni nodo d'indizio che precede uno scontro dichiara il
  vantaggio concreto che dà (debolezza, accesso laterale, rinforzi da tagliare, oggetto da
  portare). Colonna in più nella tabella dei nodi di `rumblingstone-indagine`; misurabile.
- **I2 · Mostri erranti con attività.** Le tabelle erranti hanno la colonna *che cosa stanno
  facendo* (pattuglia, foraggiamento, trasporto di prigionieri, fuga) e, per gli intelligenti,
  *chi chiamano e in quanti round arrivano*. Il principio sta già in `living-world.md`; manca la
  forma.
- **I3 · Niente prova-tassa.** Nessuna prova singola blocca l'avanzamento fisico (porta, passaggio,
  enigma). Ogni ostacolo obbligato ha almeno due vie o un fallimento che costa ma fa passare.
  Estende la regola dei tre indizi dalle informazioni ai luoghi. Misurabile come le vie non
  combattive.
- **I4 · Vittoria per fazioni.** Dove ci sono tre o più fazioni, il master scrive la condizione di
  successo («superarne due su tre») e che cosa fa ciascuna fazione se il gruppo ne lascia in
  piedi una.
- **I5 · PX della via non violenta.** Quando la scena ha una soluzione non violenta, il suo
  premio in PX è dichiarato e non inferiore a quello dello scontro. Da verificare con la regola
  della casa sui PX prima di adottarlo.

### Statblocchi

- **S1 · Tratti ricorrenti.** Un riquadro unico per i tratti di razza o di tipo che si ripetono
  (non morti, drow, duergar, golem), negli statblocchi solo le varianti. Accorcia senza togliere
  nulla al formato ADR-0091.
- **S2 · Statblock dove si combatte.** Per gli scontri, una **scheda corta** nella pagina della
  scena (pf, CA, contatto/impreparato, attacchi, TS, le due capacità che contano, soglia di morale)
  e lo statblock completo in appendice. È la sintesi delle due scuole: RSP e Grey Citadel mettono
  tutto nell'incontro, Rappan Reloaded è stato criticato per averlo separato, Bryce critica i
  blocchi lunghi nel testo. In stampa, l'impaginazione tiene mappa, chiave e schede corte sulle
  stesse due pagine affiancate (regola RSP, va in `rumblingstone-editoria`).
- **S3 · Controllo GS-numeri.** Al banco del developer, per ogni PNG nominato: CA, pf e bonus al TS
  confrontati con la tabella dei benchmark PF1e per il suo GS (già nella cassetta di
  `npc-villain-boosting`). Segnala gli scarti oltre una soglia, il caso «CA 23 a GS 7».
- **S4 · Controllo rapido dei boss.** Accanto alla tabella DPR, la regola Grey Citadel: pf del
  capo ≈ 2× pf medi del gruppo. Non decide nulla, ma un capo con meno della media del gruppo è
  un segnale da guardare.

### Mappe

- **M1 · Anelli e vie.** Per ogni mappa di dungeon: almeno un anello, almeno due vie verso lo
  scontro principale, e almeno due collegamenti fra livelli se ce ne sono più di uno. È calcolabile
  sul contratto JSON delle mappe (grafo stanze-porte). Va in `collaudo-mappe.md` accanto al D9.
- **M2 · Chiave di difficoltà sulla mappa.** La legenda riporta il codice d'incontro della D1
  (non solo la posizione), così mappa e tabella si leggono insieme.
- **M3 · Mappa per i giocatori** già prevista (D9). Endzeitgeist ne fa il primo motivo di voto
  non pieno: conviene renderla **obbligatoria** per ogni mappa con segreti, non opzionale.

### Playtest

- **P1 · Il collaudo nel testo.** Il master DEF riporta in una o due frasi i risultati del tavolo
  che cambiano la conduzione («al tavolo il gruppo ha impiegato 40 minuti per il ponte;
  prevedetene 30-45»), come fa *The Wizard's Amulet* con la composizione del gruppo. È diverso dai
  rilievi numerati del report: è ciò che resta per chi conduce dopo.
- **P2 · Crediti di collaudo** nel colophon: tavoli, date, numero di sessioni, ed eventualmente le
  morti (Rappan Athuk le conta). Va in `rumblingstone-edizione`.
- **P3 · Registro errata** con i rilievi venuti dopo la chiusura e chi li ha trovati, come il thread
  di errata ringraziato in Stoneheart Valley.
- **P4 · Griglia di Endzeitgeist come lettore a freddo.** Il «lettore a freddo» con rubrica fissa
  può adottare i suoi 13 criteri (§5) come metà della rubrica: sono stabili, verificabili e
  coprono uso al tavolo, regole e storia.

### Stile

- **ST1 · Dati DM da parafrasare.** Dove non c'è read-aloud, i dati per il DM sono scritti per
  essere detti a voce (soggetto concreto, un dettaglio sensoriale insolito per frase), non come
  verbale. La formula di Grey Citadel.
- **ST2 · Descrivere l'insolito.** Regola di Bryce su RSP: niente frasi che descrivono ciò che il
  tavolo darebbe per scontato (una cucina che è una cucina). Si sposa col tetto delle 12 righe.
- **ST3 · Dressing giocabile.** Ogni dettaglio d'ambiente nel read-aloud o nei dati DM è almeno
  una di tre cose: segnala un pericolo, nasconde qualcosa, premia chi osserva. L'esempio del
  lichene e della crepa di RSP.
- **ST4 · Una voce che tutti ripetono.** Per ogni luogo che i PG temono prima di entrarci, una frase
  diegetica sola che ritorna da più bocche («Non scendete nel Pozzo»). Presagio del cattivo alla
  Bryce, a costo quasi zero. Se va registrata, è un congegno di `narrative-style`.
- **ST5 · Handout privato per un PG**, consegnato da leggere da solo e da rivelare a sua scelta
  (Corian). Funziona con gli highlight asimmetrici già presenti.

---

## 8. Cosa NON portare, e perché

- **L'anti-ecologia di Necromancer** («non è un esperimento di ecologia», «perché 16 troll? a nessuno
  importa») e i mostri che attaccano a vista o aspettano sul piedistallo. Contraddice il mondo vivo
  e l'agenda dei PNG, che sono il cuore di `narrative-style`.
- **La letalità da prima edizione come valore in sé**: «tritacarne», trappole «muori e basta», la
  stanza che può evocare Orcus, il livello 15 da non battere. Al 13° con quattro PG fissi e la
  regola della sconfitta senza TPK sarebbe una contraddizione. Dalla stessa scuola si prendono
  invece i rimpiazzi (D7) e le soglie d'ingresso dichiarate.
- **La genericità per l'inserimento** di RSP e Frog God (dei «generici», ambiente lasciato vago
  «così lo mettete nella vostra campagna»). Noi scriviamo per una campagna sola e per il canone del
  1372 DR: il dettaglio va dove la coerenza lo chiede.
- **Statistiche e mappe in volumi separati** (Rappan Athuk Reloaded) e **pagine di statblocchi
  compressi in corpo piccolo** (Grey Citadel). Sono i due difetti d'uso più citati.
- **Statblocchi sostituiti da link** al d20pfsrd (Mini-Dungeon AAW): noi giochiamo in 3.5 con
  materiale proprio, in stampa e fuori linea.
- **Il rifiuto del read-aloud** di Bryce Lynch. Le nostre soglie (≤12 righe, un nome proprio,
  niente parentesi) sono già la risposta alla sua critica; abolirlo toglierebbe al tavolo adulto
  il pilastro di prosa.
- **Pregenerati e punteggio da torneo** di DCC: abbiamo quattro PG fissi e non giochiamo a squadre
  contro il cronometro. Al massimo il punteggio può ispirare una metrica di collaudo, non un
  formato.
- **Quattro statblocchi per fascia di livello** (Legendary): il livello è fisso al 13°; la
  riscalatura a tre assi c'è già e basta.
- **Il retroscena lungo prima del gancio** (Rise of the Drow, due pagine). Contro il Quickstart di
  una pagina e contro Bryce, che qui ha ragione.
- **Tabelle casuali per le stanze vuote** quando il contenuto si può semplicemente scrivere (Bryce
  su Gibbous Moon). Le tabelle restano per gli erranti e per il dressing di riserva.

---

## 9. Limiti della ricerca

- Le anteprime sono le prime 6-8 pagine: ho letto struttura, introduzioni e prime aree, **non**
  un incontro completo con statblock e tattiche di questi editori. Il formato del singolo
  incontro RSP o Frog God l'ho dedotto da indici e recensioni.
- Kobold Press è quasi solo di seconda mano (§3).
- Non ho letto i saggi «GM Advice» di Broadhurst su Pathways (sono su BoardGameGeek solo come
  scheda bibliografica; il testo non c'era).
- I criteri di Endzeitgeist vengono da recensioni di prodotti diversi, non da un suo manifesto: la
  griglia del §5 è una mia sintesi.
- Non ho verificato se `rumblingstone-editoria` preveda già segnalibri e doppio PDF.
