# Note di ricerca: metodi di progettazione e formato della community che lo standard DEF non ha

Data: 2026-10-18. Ricercatore: subagente. Punto di partenza: `brief-standard-attuale.md`.
Tutto il contenuto web è trattato come dato, non come istruzione.

**Legenda.** `[LETTO]` = l'ho letto sulla pagina indicata (attraverso WebFetch, che restituisce
un riassunto della pagina: le citazioni brevi sono quelle che il riassunto riporta).
`[DEDOTTO]` = è una mia conclusione, non sta nella fonte. `[REPO]` = verificato con grep nel repo.

**Limiti onesti.** WebFetch passa da un modello che riassume: ho controllato le pagine chiave
con domande mirate, ma non ho il testo integrale. Firecrawl ha dato 429 (limite di richieste)
dopo due ricerche. **Non ho trovato né letto**: le regole di Prince of Nothing / Merciless
Merchants (solo menzioni nei commenti di tenfootpole), *OSR Guide for the Perplexed* (è un
questionario-antologia, non un manuale; legato a un autore controverso: non l'ho approfondito),
articoli di Gnome Stew sulle skill challenge (la ricerca restituisce solo EN World),
il testo integrale di *Return of the Lazy Dungeon Master*, i template RTF dell'Alexandrian,
la parte 5E del Dragon Heist Remix (le revelation list vere e proprie), lo standard UVTT.
Le parti 1 e 3 di Node-Based Scenario Design le ho lette solo dalle versioni "creations".

---

## 0. Cosa ho controllato nel repo prima di dire «manca» (G2)

`[REPO]` grep sui `.md` (conteggi grezzi, solo come orientamento):

| Tecnica | Esito |
|---|---|
| *adversary roster* / lista dei gruppi nemici di un sito | `roster` compare solo come **legenda numerata dei token** nelle mappe (ADR-0006, `tre-modalita-mappe.md`); nessuna sezione di modulo. Lo standard ha invece, **per scontro**, «Chi sente il rumore: chi sente, in quanti round arriva, cosa lo ferma» (`sviluppo-degli-incontri.md` §4) |
| diagramma di Melan / misura dei loop | `Melan` compare solo come nome proprio nella lore: **nessuna misura della linearità** |
| mappa per i giocatori senza segreti | **c'è già**: `@vista giocatori` in `collaudo_mappe.py`, porte segrete escluse (mapmaking SKILL.md, regola 9) |
| *secrets and clues*, *strong start* | 0 file |
| tabelle di incontri casuali / mostri erranti | 5 file (gli «eventi di viaggio d6» del brief) |
| *order of battle* / ordine di battaglia | 2 file |
| statblocco ridotto per comparse | ADR-0091 ha il «dossier breve» e la tabella **Comparse** (una riga), ma non un **blocco statistico ridotto** |
| contingenze «se i PG fanno X» | **c'è ed è un obbligo** (module-standard, voce 9): vedi §1.4, la fonte più citata lo sconsiglia |

---

## 1. The Alexandrian (oltre a Three Clue Rule e Art of the Key 1-3)

### 1.1 Adversary Roster — *Art of the Key, parte 4* `[LETTO]`
https://thealexandrian.net/wordpress/38547/roleplaying-games/the-art-of-the-key-part-4-adversary-rosters

Regole operative:
- Tabella a **tre colonne**: *gruppo d'azione* («2 guardie orchesche», «Capitano Gnarltooth»),
  *posizione* (area), *note* (o note a piè di tabella se lunghe).
- Posizioni variabili scritte così: «Area 19 **o** Area 6», percentuali («80%»),
  condizioni fra parentesi («giorno», «notte»).
- **Quattro tipi di gruppo**: *Pattuglia* (percorso chiave), *Mobile* (il default: risponde ai
  PG), *Quasi fermo* (lascia la sua area solo se attivato; nella tabella va **rientrato**),
  *Fermo* (non esce mai: resta nella chiave della stanza, **non** nel roster).
- **Etichette di comportamento** («Squadra della morte», «Guardia perimetrale») abbinate al
  foglio statistiche omonimo.
- Si raggruppa chi agisce insieme; si divide un gruppo se le sue parti possono agire da sole.
- **Tetto**: 15-20 gruppi si gestiscono; oltre ~25 si spezza il complesso in sezioni o si passa
  a tabelle d'incontro casuale. **Roster e incontri casuali di solito non si mescolano.**
- **Roster distinti per stato**: normale / in allerta (e, in Porphyry House, giorno / notte su
  pagine separate) — https://thealexandrian.net/wordpress/52083/roleplaying-games/ptolus-running-the-campaign-prepping-porphyry-house
- **Al tavolo**: gruppi numerati, segnalini numerati sulla mappa del DM alla posizione di
  partenza, si spostano. Il DM lavora con due fonti: la chiave dell'area corrente e il roster.
- Avvertenza: gruppi dello stesso roster possono confluire nello stesso scontro, quindi i
  singoli scontri vanno tarati **meno letali**.

Perché ci interessa `[DEDOTTO]`: «Chi sente il rumore» risponde **scontro per scontro**; il roster
risponde **per il sito intero** e rende banale il caso in cui i PG si infilano da un ingresso
non previsto, o tornano dopo un riposo. Con PG di 13° (teletrasporto, *scrutare*, invisibilità,
volo) l'ingresso non previsto è la norma, non l'eccezione. Il nostro emoji-grid ha già il
roster numerato dei token: manca la **tabella dei gruppi con tipo, stato e risposta**.

### 1.2 Status dei luoghi tra una sessione e l'altra `[LETTO]`
https://thealexandrian.net/?p=48582 (Campaign Status Documents)
- Per ogni luogo: intestazione con codice del modulo («5.4 ZHENTARIM – KOLAT TOWERS»),
  **punti di stato** («Mimic ucciso»), **roster aggiornato** che sostituisce l'originale,
  **diff della chiave** (una-due frasi per stanza cambiata dai PG), **cronologia** dello
  scenario con gli eventi passati **barrati, non cancellati**, e **status quo atteso**: dove si
  assesta il luogo se i PG non tornano.
- La cronologia si prepara solo fino a quando è probabile che i PG tornino.

`[DEDOTTO]` Il repo ha `state.md` per la campagna e l'Echo Ledger; non ho trovato un formato per
lo **stato di un sito** (roster superstite + diff della chiave + status quo). È la parte
naturale da affiancare al roster.

### 1.3 Node-Based Scenario Design: strutture e regola inversa `[LETTO]`
https://thealexandrian.net/creations/misc/node-design/node-design2.html ·
https://www.thealexandrian.net/creations/misc/node-design/node-design5.html ·
https://thealexandrian.net/creations/misc/node-design/node-design7.html ·
https://thealexandrian.net/?p=8176 (Advanced, parte 2: navigazione)
- **Regola inversa dei tre indizi**: se i PG hanno accesso a tre indizi qualsiasi, quasi
  certamente arrivano ad almeno una conclusione → un nodo può avere più uscite e lasciar
  scegliere. Esempio numerico: nodo iniziale con 3 indizi verso A, B, C; dopo A e C restano 3
  indizi che puntano a B.
- **Contabilità per nodo**: almeno **3 indizi dentro** ogni nodo e almeno **3 indizi che vi
  puntano**. Gli indizi verso un vicolo cieco o verso un nodo con meno di 3 indizi sono
  «bonus» e non contano. Eccezione: tanti nodi da 2 indizi quanti sono gli indizi del nodo
  iniziale. Il vicolo cieco deve comunque dare qualcosa (tesoro, lore, arma).
- **Strutture con nome**: *Conclusione* (nodi del secondo strato che puntano tutti al finale,
  con **carote e bastoni** per renderli non saltabili: A ha la mappa di D, B l'ingresso segreto,
  C ha gli sgherri che rinforzano D se non li si batte); *Imbuto* (strati liberi separati da un
  nodo-cancello: utile in D&D a livelli); *Torta a strati* (ogni nodo punta nel suo strato e dà
  un indizio allo strato dopo; si prepara solo fino allo strato successivo); *Anello* (4 nodi
  che puntano ognuno agli altri tre).
- **Tipi di nodo**: luogo, persona, organizzazione, evento, attività. Nodi annidati in nodi.
- **Modi di navigazione**: indizio, geografia, tempo, caso, **nodo proattivo** (viene a cercare
  i PG; esempio: una «Alert Track» in cui l'opposizione che cresce cambia i nodi), pista,
  iniziativa dei giocatori. Una porta segreta è un **punto unico di guasto**; un solo indizio su
  *come* arrivare rende fragile lo scenario anche con molti indizi su *perché* andarci.

`[DEDOTTO]` Il repo ha la regola dei tre indizi e «nodi»; quello che non ho visto è il
**conteggio verificabile** (entranti/uscenti per nodo) e la **dichiarazione della struttura**
(imbuto, torta, anello) con carote e bastoni scritti. È misurabile: un grafo nodi→indizi.

### 1.4 Don't Prep Plots / Tools, Not Contingencies `[LETTO]` — attrito con il nostro standard
https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots ·
https://thealexandrian.net/wordpress/37422/roleplaying-games/dont-prep-plots-tools-not-contingencies
- Si preparano **situazioni**, non trame: obiettivi del cattivo e cosa succede se i PG non
  intervengono (lista di obiettivi o cronologia).
- **Non** alberi «se i PG fanno X allora Y»: lunghi, usati di rado, non coprono il piano che i
  giocatori inventano davvero. Al massimo un appunto.
- Si prepara invece la **cassetta degli attrezzi** di ogni antagonista e luogo: *personale,
  equipaggiamento, luoghi, informazioni*, e **a cosa serve** ciascuno («la squadra di sgherri
  sorveglia il covo», «la moglie separata conosce la sicurezza della villa»); si raggruppa in
  squadre.
- Esempio dell'ospedale (Eternal Lies): la versione «contingenze» descrive prove e CD per ogni
  piano; la versione «attrezzi» dice: due uscite, finestre alte che quasi non si aprono,
  infermiere con bonus a notare chi curiosa, posti di guardia a ogni piano, guardie all'ingresso
  della terapia intensiva che reagiscono a tutto, e «se i ragazzi escono parte una caccia
  all'uomo». Con la seconda il DM risolve anche bomba finta, calata dalla finestra, ostaggi.
- **Criterio di riuscita** dichiarato: la preparazione è buona se si risolvono piani **non
  previsti** usando solo gli attrezzi scritti. La lunghezza non conta se ogni dettaglio è un
  attrezzo.
- Due domande per decidere cosa preparare: *a cosa saranno interessati i PG* (non cosa
  faranno) e *quali sono i piani dei PNG* (status quo e traiettorie, non reazioni ai PG).

`[DEDOTTO]` Il nostro punto 9 («Contingenze "Se i PG fanno X"») è esattamente la forma che
Alexander scarta. Non va buttato: la riga **sconfitta senza TPK** è un attrezzo vero, e le voci
«parlare col boss / rubare / fuggire» sono poche e prevedibili. Ma la prova del suo criterio è
un buon test da playtester: *dare al lettore a freddo tre piani che il modulo non prevede
e vedere se il master li regge.*

### 1.5 Xandering (Jaquaying) the Dungeon `[LETTO]`
https://thealexandrian.net/wordpress/13085/roleplaying-games/jaquaying-the-dungeon ·
https://thealexandrian.net/wordpress/13103/roleplaying-games/xandering-the-dungeon-part-2-xandering-techniques ·
https://thealexandrian.net/?p=44474 (esempio di revisione)
- Dodici tecniche: ingressi multipli; anelli; connessioni multiple fra livelli; connessioni
  **discontinue** (dal livello 1 al 3, tunnel segreto dal 4 alla superficie); percorsi segreti e
  **insoliti** (crollo da sgomberare, botola, rete di teletrasporto da decifrare, ponte di corda
  raggiungibile da sotto, passaggio sommerso fra due laghi); sottolivelli; **livelli divisi**
  (il livello 3 non si attraversa senza passare dal 2 o dal 4); dungeon annidati; piccoli
  dislivelli dentro un livello (scale e rampe che non segnalano un cambio di livello);
  **ingresso a metà** (si sceglie se salire o scendere); geometria non euclidea; spazi
  extradimensionali.
- **Diagnosi**: si disegna il **diagramma di Melan** (si tolgono i corridoi che non diramano) e si
  misura la linearità come **profondità massima delle diramazioni** rispetto alla via
  ingresso→conclusione (nell'esempio: tre stanze).
- Procedura di revisione: trovare il perno; spezzare il dungeon in **blocchi concettuali**
  (tempio, alloggi, santuario); riordinare i blocchi a livello macro; aggiungere almeno qualche
  collegamento trasversale (passaggio dietro un arazzo); scegliere apposta gli snodi; **mappare
  per ultimo**.
- Nessun numero fisso di anelli (lo dice la fonte).
- Bryce Lynch lo mette fra gli standard: «Linear dungeons are bad», anelli per esplorazione,
  aggiramento, imboscata, ritirata; più vie fra livelli (vedi §2).

`[DEDOTTO]` Il repo ha mappe molto curate (griglia, `@collega` per scale e botole, collaudo a
classi E) ma nessuna misura della **topologia**. `collaudo_mappe.py` ha già i collegamenti fra
livelli: contare cicli del grafo delle aree, ingressi, profondità delle diramazioni e punti unici
di guasto (una porta segreta sola sulla via critica) è un'estensione piccola e misurabile.
A 13° conta doppio: volo, *passa pareti*, *porta dimensionale* trasformano ogni dungeon lineare
in un dungeon con scorciatoie non previste. Meglio progettarle.

### 1.6 Party Planning (eventi sociali) `[LETTO]`
https://thealexandrian.net/wordpress/37995/roleplaying-games/game-structure-party-planning
- **Luogo**: più zone dove si formano gruppi (sala da ballo, bar, area riservata) + almeno uno
  spazio privato o semiprivato (vedere chi entra ed esce crea intrigo).
- **Invitati**: circa **15 PNG** (sotto 10 è piatto, sopra 20 è rumore); lista principale dei
  nomi; per gli importanti: relazioni con altri PNG, reazioni a stimoli, azioni da innescare,
  indizi, agganci, storia condivisa con un PG, oggetti insoliti. **Un PNG per foglio sciolto**,
  da tirare fuori quando entra in conversazione; ritratto da mostrare.
- **Sequenza di eventi principale** (di solito lineare; il primo evento è il gancio d'apertura);
  la sequenza è un'impalcatura, non la storia.
- **Argomenti di conversazione**: 5-8, alcuni irrilevanti per contrasto; per i rilevanti **2-3
  punti di vista** in cui i PNG improvvisano.
- **Al tavolo, a ogni giro**: chi parla con chi, chi si unisce ai PG, di cosa si parla; spingere
  i PG a separarsi; far rimbalzare gli eventi fra i gruppi; riportare i PNG con cui c'è stata
  intesa; se cala, tagliare o far partire l'evento successivo.
- **Versione da 5 minuti**: 3-5 luoghi, 10 personaggi, 5 eventi, 5 argomenti; se i PG hanno un
  obiettivo, tre modi di raggiungerlo.

`[DEDOTTO]` Lo standard ha «Contratto In scena», Comparse, foglio del cast con tic vocale, e la
tabella «Chi si trova qui» a sei righe. Manca la **forma della festa/consiglio/udienza come
mappa di nodi**: zone, argomenti con schieramenti, sequenza di eventi. È proprio la scena
«politica GoT» che lo stile chiede.

### 1.7 Pointcrawl `[LETTO]` e hexcrawl (solo struttura) `[LETTO]`
https://thealexandrian.net/wordpress/48666/roleplaying-games/pointcrawls ·
https://thealexandrian.net/wordpress/46020/roleplaying-games/5e-hexcrawl
- Pointcrawl: **punti** (a ogni scala, annidabili) + **collegamenti** letterali (strade) o
  astratti; **tempo di viaggio** standard o per collegamento, segnato sulla mappa con numeri o
  puntini (un puntino = un intervallo); **una prova d'incontro per intervallo**; procedura per
  mossa: segui il collegamento → prova d'incontro → arrivo e nuove uscite descritte.
  I «colli di bottiglia» (un solo ponte) sono nodi della mappa.
- Hexcrawl: si chiavano **luoghi**, non incontri; quasi ogni esagono ha contenuto (esagoni vuoti
  frequenti = scala sbagliata); gli esagoni sono un'astrazione del DM, nascosti ai giocatori.

`[DEDOTTO]` La campagna è guidata dagli archi, non è un sandbox: un hexcrawl completo non serve.
Un **pointcrawl della Valle** (o di una città) per gli spostamenti fra luoghi chiave, al posto
o accanto agli «eventi di viaggio d6», darebbe tempi e scelte di percorso leggibili.

### 1.8 Tabelle d'incontro `[LETTO]`
https://thealexandrian.net/wordpress/46498/roleplaying-games/hexcrawl-errata-using-encounter-tables
- Voce di tabella: nome, intervallo di d20, numero (dadi), **% Tana**, **% Tracce**, rimando
  all'esagono della tana; regola di massima 20% tana, 40% tracce.
- Incontri **procedurali** (elementi generici che il DM contestualizza, riusabili) vs
  **progettati** (spesso preparazione sprecata, usabili una volta). Principio: non preparare
  ciò che si improvvisa facilmente.

### 1.9 Come si prepara un modulo per giocarlo `[LETTO]`
https://thealexandrian.net/wordpress/46535/roleplaying-games/how-to-prep-a-module-part-2
- **Il passo di valore più alto è fare l'adversary roster.**
- **Revelation list** per i misteri: (1) le conclusioni essenziali; (2) i luoghi, persone,
  organizzazioni, eventi dove si trovano indizi; (3) gli indizi per ciascuna conclusione; poi si
  aggiungono indizi finché ogni rivelazione ne ha almeno tre.
- **Fogli statistiche separati**: tutte le statistiche di uno scontro **stese insieme** senza
  sfogliare; raggruppate per fazione, luogo o gruppo d'azione; **le capacità e i meccanismi
  poco familiari si copiano dentro il blocco** per non cercarli durante la sessione.
- Ordine delle sezioni d'esempio: fogli di riferimento → revelation list / roster → materiale
  dell'avventura → schede PNG → fogli statistiche → mappe → prop; ciò che si usa di più va
  **all'inizio e alla fine**.
- Read-aloud: un lettore suggerisce di leggerlo ad alta voce prima, o di ridurlo a parole
  chiave in elenco puntato.

`[DEDOTTO]` Abbiamo appendici e Quick-Reference, ma il «foglio dello scontro» con tutti i blocchi
di un combattimento sulla stessa facciata, e il testo degli incantesimi ricopiato nel blocco,
non li ho visti come regola. A 13° un mago o un chierico ha 30-40 incantesimi in lista: è il
punto in cui il DM sfoglia il manuale a metà round.

### 1.10 Remix di Dragon Heist: squadre di risposta delle fazioni `[LETTO]`
https://thealexandrian.net/wordpress/42918/roleplaying-games/dragon-heist-remix-part-7-how-the-remix-works
- **Faction Response Team**: ogni fazione ha una squadra da mandare contro i PG. Lista di
  decisione: i PG cercano una pista? → indirizzali a un avamposto. Hanno fatto arrabbiare una
  fazione? → attiva la squadra. Sono bloccati? → attiva la squadra.
- Calendario dei livelli dichiarato (dopo quale evento si sale).
- Le revelation list vere sono nella parte 5E, **che non ho letto**.

---

## 2. Bryce Lynch (tenfootpole.org) e l'area OSR

### 2.1 Review Standards di Bryce `[LETTO]`
https://tenfootpole.org/ironspike/?page_id=1201 ·
https://tenfootpole.org/ironspike/?p=3870 (retrospettiva di Dungeon) ·
https://tenfootpole.org/ironspike/?p=2773
- Primo criterio: «useful to the DM at the table while they running it»; scrittura che si
  **scorre in pochi secondi**: «terse and evocative», ben organizzata.
- Contro: padding, «Mountains of backstory, mountains of room text»; read-aloud lungo
  («Boxed text: usually not good»); dopo il n. 100 di Dungeon, avventure «more linear and more
  focused on stat blocks»; critica ai «long stat blocks».
- Tabelle di mostri erranti **generalmente necessarie** (consumano risorse, impediscono il
  riposo gratuito); erranti **con uno scopo** (pattugliano, cacciano).
- Mappe ad anello, più connessioni fra livelli; trappole e trucchi **con indizi** per chi
  cerca; vasche e statue strane, alcune **benefiche** (altrimenti i giocatori smettono di
  toccarle); mostri non standard; **foreshadowing del cattivo principale** prima dello
  scontro; **ordine di battaglia** (quando arrivano gli alleati del nemico durante lo scontro);
  mostri **colti a metà di un'attività**; fazioni; oggetti magici unici, mai «spada +1».
- Scala di valutazione (dalla stessa pagina): **GM Complexity 0-6** espressa in **ore di
  preparazione per 4 ore di gioco** (6 = zero preparazione; 5 = 1-2 ore; 4 = 3-4 ore con
  riordino); Linguaggio 0-4 (4 = succinto ed evocativo); Mappe 0-3 (0 = **incoerenti con il
  testo**); Grafica 0-4 (4 = usabile al tavolo **con i giocatori**).

### 2.2 Le 30 regole di Bryce, riassunte da terzi `[LETTO, fonte secondaria]`
http://into-the-dark-rpg.blogspot.com/2016/07/bryce-lynchs-adventure-design-tips.html
Quelle che non abbiamo o abbiamo peggio `[DEDOTTO]`:
- **Contesto**: i giocatori devono avere abbastanza informazioni sulle conseguenze probabili
  perché la scelta sia una scelta (n. 2).
- **Tabella delle voci (rumor table)**: ganci accoppiati a dettagli di colore (n. 7, 28a).
- **Solo il background che influenza il gioco** (n. 12).
- **Tesoro non magico legato all'ambientazione**, che dà indizi su mostri, PNG, luoghi (n. 24).
- **Oggetti magici descritti per come si vedono e come si attivano** (n. 26).
- **Tabella dei mostri/PNG con tratti, motivazioni e posizione** (n. 28b): è l'adversary roster
  arricchito.
- **Simboli sulla mappa per le condizioni standard** (illuminato, chiuso a chiave) invece di
  scriverle nella chiave (n. 30).

### 2.3 Principia Apocrypha `[LETTO]`
https://www.osr.camp/principia-apocrypha
Applicabili alla 3.5 `[DEDOTTO dalla mia lettura]`:
- **Give Them Layers To Peel**: descrivere ciò che è *ovvio, sottile, nascosto, invisibile* in
  un ambiente. Si incastra con il nostro Read-aloud → Dati DM: la gradazione mappa sulle CD di
  Cercare/Osservare.
- **Telegraph Lethality**: avvertire della minaccia così che la morte discenda da una scelta.
- **Build Challenges With Multiple Answers** (idealmente tre) … **and Challenges With No Answer**
  (qualche minaccia aperta senza soluzione prevista, con cautela sulla via critica).
- **Reveal The Situation / Don't Bury The Lead**: dire ciò che i PG sanno ragionevolmente;
  dettagli abbastanza specifici da poterci agire.
- **NPCs Aren't Scripts**: si ritirano o si arrendono quando perdono (abbiamo le soglie di morale).
- Non applicabili: PX per il tesoro, tiri di reazione e morale OSR.

---

## 3. Lazy DM, Five Room Dungeon, One Page Dungeon

### 3.1 Sly Flourish, gli otto passi `[LETTO]`
https://slyflourish.com/eight_steps_2023.html · https://slyflourish.com/great_adventure_criteria.html
- **Strong start**: «something happens», un evento che tira dentro i giocatori.
- **Segreti e indizi**: una-due frasi ciascuno; **si scrive il segreto, non come lo si scopre**:
  il mezzo (un PNG, un affresco, una visione) si decide al tavolo; si portano avanti quelli non
  ancora rivelati (il metodo originale ne voleva dieci a sessione).
- **Luoghi fantastici**: una frase; per gli scontri importanti **1-3 elementi interagibili**.
- Ripasso dei personaggi: per ogni PG, quale gancio lo tira dentro la prossima sessione.
- Fra i criteri di una buona avventura: tabelle casuali, scrittura economica, «situational
  setups» invece di scene sceneggiate, mondo vivo con fazioni che perseguono i loro scopi.

`[DEDOTTO]` I segreti **astratti dal luogo** sono la toppa al punto debole della regola dei tre
indizi: se i PG saltano il nodo, il segreto si sposta. È diverso dal nostro «nodo d'indizio»
legato a un luogo; i due si sommano. La «Strong start» manca come voce dichiarata: un'apertura
di sessione **in medias res** per ogni capitolo è misurabile (c'è o non c'è).

### 3.2 Five Room Dungeon (Johnn Four) `[LETTO, fonte secondaria con permesso dell'autore]`
https://www.scabard.com/features/5-room-dungeon
- 1 Ingresso e guardiano (spiega perché il luogo è intatto); 2 Enigma o prova di
  interpretazione (**spotlight a PG diversi** dalla stanza 1; indizi della soluzione piantati
  nella 1); 3 Trucco o battuta d'arresto (può **consumare la risorsa** a cui il nemico finale è
  vulnerabile); 4 Climax con terreno che conta; 5 Ricompensa, rivelazione o colpo di scena
  (anche non fisico).

`[DEDOTTO]` Lo abbiamo già in larga parte (spotlight, terreno, highlight asimmetrici). Utile solo
come **controllo della varietà di un sito**: la sequenza delle stanze alterna combattimento /
enigma / sociale / trappola, e la stanza 3 prepara la 4.

### 3.3 One Page Dungeon `[LETTO]`
https://thealexandrian.net/wordpress/4974/roleplaying-games/halls-of-the-mad-mage
- Vincolo: mappa + poche note **su una pagina**; si gioca con manuale, il foglio e i dadi.
  L'autore (vincitore 2009) lo considera una **disciplina**, non una soluzione completa.

`[DEDOTTO]` Non è un formato per i nostri master DEF (troppa densità meccanica a 13°), ma una
**«pagina del sito»** (mappa + chiave in una riga per area + roster) come foglio da tenere aperto
è il naturale riassunto del roster di §1.1.

### 3.4 Skill challenge e Gnome Stew
**Non trovato.** Le ricerche portano a EN World (discussioni 4e). Il repo ha già lo skill
challenge scritto per intero: non ho niente di verificato da aggiungere.

---

## 4. Mappe di community

### 4.1 Licenza di Dyson Logos `[LETTO]`
https://dysonlogos.blog/maps/commercial-maps/
- Licenza **gratuita, royalty-free, commerciale**: le mappe si possono «used, reused, modified,
  remixed, mangled and published for personal or commercial use»; obbligo: «credit the map or
  cartography to Dyson Logos».
- Riserve: **diritti morali** secondo la legge canadese (artt. 28.1-28.2): modifiche che
  pregiudicano onore o reputazione, o l'uso associato a prodotti, cause, istituzioni.
- Vale **solo per le mappe marcate commerciali** (quelle linkate dalla pagina); **non** per il
  testo dei post (storie, agganci). Esiste un «Map Copyright & Usage Agreement» separato che
  **non ho letto**: da leggere prima di adottare.
- Si possono togliere le diciture Patreon/dysonlogos.com e il titolo.

`[DEDOTTO]` Non è una CC: va trattata dal gate d'uscita di `rumblingstone-edizione` come licenza
propria, con la riga di credito nel colophon.

### 4.2 Mappa del DM e mappa dei giocatori `[LETTO]`
https://paizo.com/threads/rzs2np78 (Frog God Games, sondaggio sulle mappe di Slumbering Tsar) ·
https://forum.profantasy.com/discussion/comment/124863/
- Preferenza maggioritaria: **mappe del DM dentro il testo** accanto alla chiave (niente pagine
  da sfogliare, critica esplicita ai libri WotC) **e** mappe dei giocatori raccolte a parte
  (handout, fotocopia, VTT).
- Nelle mappe dei giocatori FGG ha tolto **numeri delle stanze, porte segrete e trappole**,
  **schiarito la griglia**, tolto le texture; un PDF «Player Maps» separato. Lamentela: griglia e
  ombreggiature dei muri si confondono.
- Su ProFantasy: la mappa per i giocatori «is supposed to show them what they see, not be a
  reference item»; porte segrete su un **livello SEGRETO** separato.

`[REPO]` Abbiamo già `@vista giocatori` senza porte segrete. `[DEDOTTO]` Da verificare se la vista
giocatori toglie anche **numeri, trappole, segnalini nemici e annotazioni tattiche**, e se la
griglia è attenuata: è la lista di FGG, ed è controllabile in `collaudo_mappe`.

### 4.3 Cosa non ho trovato
Nulla di letto su: sezioni verticali e altezze come standard di community, Paizo Flip-Mat,
standard UVTT/linee di vista. Il repo ha già l'export UVTT: non l'ho approfondito.

---

## 5. Statblocchi: quale formato vince al tavolo

### 5.1 Il formato WotC 2006-2007 (MM IV/V, DMG II, RHoD) `[LETTO]`
https://thealexandrian.net/?p=979 · https://thealexandrian.net/creations/advanced-rules/stat-block.html
- Principi WotC (secondo Alexander): **tutto ciò che serve per far agire il mostro** e
  **ordinato per quando si usa nello scontro**, in cinque sezioni: inizio dello scontro, turno
  dei PG, turno del mostro, dettagli rari, testo esplicativo.
- Pro: più facile da usare **sotto pressione**. Contro: ha tolto il **tipo di DV e il calcolo dei
  pf** (danno alla preparazione e agli aggiustamenti al volo); occupa più pagina (font più
  grande: 67 righe/pagina nel MM, 55 nel MM V), quindi avventure meno dense. Esempio di
  misura: golem di magma 22 righe contro 27 del golem di carne.
- **Proposta di Alexander**: blocco pieno rivisto (etichette in grassetto, DV e pf ripristinati)
  **più un blocco breve per i PNG minori**, in quest'ordine: intestazione; individuazione (sensi,
  Ascoltare/Osservare, Iniziativa, aura, lingue); difese (CA con contatto/impreparato, pf con
  DV, probabilità di mancare, RD, immunità, resistenze, debolezze); azioni (velocità, mischia,
  distanza, spazio/portata, BAB, Lotta, opzioni d'attacco, attacchi speciali, talenti di
  combattimento, equipaggiamento da combattimento); qualità speciali; caratteristiche; TS;
  talenti; abilità; proprietà. **Senza testo esplicativo.** Attacco completo: «Mischia» lista
  l'attacco completo, l'attacco singolo è una selezione; «OPPURE» fra attacchi completi
  alternativi. Un lettore: un grindylow PF da **46 a 17 righe**.

### 5.2 Paizo (PF1e) `[LETTO]`
https://paizo.com/threads/rzs2hnfa (2007) · https://paizo.com/threads/rzs2g9fp (2005)
- Il formato Paizo è «simile al DMG II/MM IV ma con cambiamenti notevoli»: intestazioni nel
  blocco (Difesa, Attacco…) e una **sezione Tattiche**. Un utente apprezza trovare i TS sotto
  «Difesa»; un altro dice che le tattiche **a metà blocco** confondono e che per i mostri di
  alto livello **servono una pagina intera**: le sposta in fondo.
- Lamentela ricorrente: liste di incantesimi da 40 voci che seppelliscono il resto; un DM
  ricopia i dettagli degli incantesimi nel blocco perché a metà scontro serve la gittata.
- James Jacobs (2005, Dungeon): la CA «shouldn't take up 3 lines of a stat block»; spazio e
  portata omessi se 1,5 m/1,5 m.

### 5.3 Fogli e PDF degli scontri `[LETTO]`
https://paizo.com/threads/rzs2gtw7&page=1 · https://www.enworld.org/posts/4897838/
- Per *Savage Tide* (2006) un fan ha fatto un PDF con **un blocco per pagina** (formato MM IV),
  per avere «laptop behind the screen» tutte le creature di uno scontro senza sfogliare; nel
  thread si cita un **PDF simile fatto da WotC per Red Hand of Doom**.
- *War of the Burning Sky* (4e): scontri tattici in un'appendice, 1-4 pagine ciascuno (di solito
  due), rimandi incrociati con icona fra la storia e lo scontro. Contro: lunghezza variabile.

### 5.4 Discussione 4e sul blocco ridotto `[LETTO]`
https://www.enworld.org/threads/the-incredible-shrinking-stat-block.310846/ (2011, 4e)
- Contro la compressione: servono le caratteristiche per le prove non addestrate e per
  **giudicare la tattica**; i blocchi compressi «fanno vagare l'occhio» a tarda sera; i
  promemoria di regola costano poco ai veterani ma aiutano i nuovi. Proposta condivisa:
  **livelli di dettaglio diversi per ruolo** (sgherro, normale, élite, solitario).

### 5.5 Verdetto `[DEDOTTO]`
Nessuna fonte dichiara un vincitore unico. Il consenso che ricavo:
1. Al tavolo vince il **blocco ordinato per uso** (WotC 2006 / PF1e); il nostro ADR-0091 c'è già.
2. Deve **conservare DV e calcolo dei pf** (critica di Alexander; utile per scalare).
3. **Due taglie**: pieno per boss e PNG con nome, **breve** per sgherri e comparse combattenti.
   Il nostro standard ha il dossier breve e la tabella Comparse, non un blocco breve.
4. **Testo degli effetti dentro il blocco** (o in un foglio accanto), soprattutto incantesimi.
5. **Foglio dello scontro**: tutti i blocchi di un combattimento sulla stessa facciata o
   pagine affiancate: è ciò che WotC ha dato per RHoD e i fan hanno rifatto per Savage Tide.
6. Le tattiche dei mostri di alto livello **non** stanno dentro il blocco: in fondo o a parte.
   Noi le abbiamo a parte, agganciate alla mappa: è il lato giusto del dibattito.

---

## Proposte concrete

Ordinate per rapporto valore/costo `[DEDOTTO]`. Ogni proposta dice come si misura (G3).

### DEF (struttura del master)
1. **Roster dei nemici per sito** (§1.1). Un'appendice per ogni luogo con più di tre gruppi
   ostili: tabella *gruppo · tipo (Pattuglia / Mobile / Quasi fermo) · posizione · note ·
   foglio*; varianti **normale / allerta** (e giorno / notte dove serve); tetto 20 gruppi.
   Gli occupanti fermi restano nella chiave. Misura: `copertura_scene`/`collaudo_mappe` →
   un sito con ≥4 gruppi nemici ha la tabella; ogni gruppo Mobile ha una posizione; i numeri
   coincidono con i token della mappa. «Chi sente il rumore» resta per scontro, e diventa una
   riga del roster.
2. **Attrezzi del cattivo al posto dell'albero «se i PG fanno X»** (§1.4). La voce 9 si
   riscrive in due parti: (a) la riga **sconfitta** e le 2-3 contingenze davvero probabili,
   come oggi; (b) un riquadro **Risorse** per ogni antagonista: personale, equipaggiamento,
   luoghi, informazioni, ognuno con «a cosa serve», più la **squadra di risposta** e la regola di
   attivazione (PG che fanno arrabbiare la fazione / PG bloccati). Test di playtest sotto.
3. **Stato del sito** (§1.2) per i luoghi a cui si torna: roster superstite, diff della
   chiave, cronologia con eventi barrati, **status quo atteso** se i PG non tornano. Vive su
   `state.md` del ramo di gruppo (ADR-0007), non nel master.
4. **Revelation list** in testa a ogni indagine (§1.9): conclusioni → dove sono gli indizi →
   indizi per conclusione, con conteggio. Più **struttura dichiarata** (imbuto / torta a strati /
   anello / conclusione) e **carote e bastoni** per i nodi saltabili (§1.3). Misura: ≥3 indizi
   per conclusione, ≥3 entranti e ≥3 uscenti per nodo, bonus esclusi dal conteggio.
5. **Segreti mobili** (§3.1): sotto ogni indagine 5-10 segreti di una-due frasi **senza luogo**,
   da consegnare con il mezzo che il tavolo offre. Si sommano ai nodi, non li sostituiscono.
6. **Scena sociale come mappa di nodi** (§1.6) per feste, consigli, udienze: zone (3-5, una
   riservata), invitati (~15, uno per scheda), argomenti (5-8, due-tre schieramenti ciascuno),
   sequenza di eventi con il primo come gancio. Misura: presenza dei quattro elenchi.
7. **Apertura forte** dichiarata per ogni capitolo/sessione (§3.1) e **foreshadowing del
   cattivo** (§2.1): almeno N apparizioni indirette prima dello scontro finale. Misurabile come
   congegno di `misura_craft`.
8. **Tabella delle voci** per ogni luogo abitato (§2.2): ganci con dettaglio di colore, veri e
   falsi marcati per il DM.

### Playtest
9. **Prova dei piani non previsti** (§1.4): il playtester a freddo riceve tre piani che il
   modulo non contempla (ingresso dal tetto con volo, *scrutare* + *teletrasporto* nella stanza
   del boss, travestimento) e annota se gli attrezzi scritti bastano a risolverli. Rilievo 🔴 se
   il DM deve inventare la posizione dei nemici.
10. **Ore di preparazione per 4 ore di gioco** (§2.1, scala GM Complexity di Bryce) come misura
    del dry-run: il DM a freddo cronometra quanto gli serve per essere pronto. Bersaglio
    dichiarabile (es. ≤ 1-2 ore = livello 5 di Bryce).
11. **Mappa incoerente con il testo** come rilievo 🔴 esplicito (Bryce: Mappe 0 = «logical
    inconsistencies with the text»): la consistenza chiave↔mappa (porte, numeri, token) va nel
    collaudo, se non c'è già.

### Incontri
12. **Ordine di battaglia** (§2.1): per ogni scontro con alleati vicini, in che round arriva chi
    e da dove, scritto nel roster. È «chi sente il rumore» trasformato in tabella.
13. **Nemici colti a metà di un'attività** e **erranti con uno scopo**: ogni gruppo Mobile ha
    un verbo («sta portando il prigioniero al pozzo»), non solo una posizione.
14. **Strati da sbucciare** (§2.3): nelle Dati DM, gradazione ovvio / sottile (CD bassa) /
    nascosto (CD alta) / invisibile (solo magia). Si appoggia alle CD che già scriviamo.

### Statblocchi
15. **Blocco breve** per sgherri e comparse combattenti (§5.1), nell'ordine di Alexander
    tradotto: deve tenere DV e calcolo dei pf, CA con contatto/impreparato, BAB/Lotta. Da
    registrare in ADR-0091 come terza forma accanto a dossier pieno e breve.
16. **Foglio dello scontro** generato (§1.9, §5.3): per ogni scontro, i blocchi di tutte le
    creature sulla stessa facciata A4, con il **testo ridotto degli incantesimi e delle capacità**
    che si usano (gittata, TS, effetto). È ciò che WotC diede per RHoD. Generabile da
    `derive_statblocks`/`extract_statblocks` e dal booklet.
17. Liste di incantesimi: in testa le **5-8 che il PNG userà davvero** (coerenti con le
    tattiche), il resto sotto. Misura: ogni incantesimo citato nelle tattiche ha il suo effetto
    nel foglio.

### Mappe
18. **Topologia misurata** (§1.5) in `collaudo_mappe.py`: numero di ingressi, numero di cicli del
    grafo delle aree, profondità massima delle diramazioni dalla via critica, **punti unici di
    guasto** (porta segreta o passaggio unico sulla via obbligata). Avviso, non errore: un rifugio
    a corridoio unico può essere voluto, ma va dichiarato con `@deroga`.
19. **Vista giocatori completa** (§4.2): verificare che tolga numeri, trappole, token nemici,
    annotazioni; griglia attenuata. Mappe del DM accanto al testo, mappe dei giocatori raccolte in
    un fascicolo o PDF a parte.
20. **Simboli per le condizioni** (illuminato / buio / chiuso a chiave / sbarrato) in
    `legend.yaml`, se non ci sono, al posto di scriverle nella chiave.
21. **Pointcrawl** per gli spostamenti di un arco o di una città (§1.7): punti, collegamenti con
    tempo in intervalli, una prova d'incontro per intervallo, colli di bottiglia. Accanto agli
    eventi di viaggio d6, non al posto.
22. Mappe di **Dyson Logos** adottabili come base per luoghi minori, **dopo** aver letto il
    «Map Copyright & Usage Agreement» e passato il gate di `rumblingstone-edizione`; credito nel
    colophon.

### Stile
23. **Solo il background che cambia il gioco** (§2.2): un controllo per sezione «storia del
    luogo»: ogni paragrafo deve finire in un indizio, una CD, un'eco o un aggancio; altrimenti va
    in un'appendice di lore o si taglia.
24. **Tesoro che racconta** (§2.2): il tesoro non magico dice qualcosa su chi lo possedeva; ogni
    oggetto magico ha aspetto e modo d'attivazione. Si somma al tesoro itemizzato che abbiamo.

---

## Cosa NON portare e perché

- **Il benchmark d'incontro del Lazy DM** e qualunque regola 5e (vantaggio, gradi di sfida 5e,
  «bounded accuracy»): sistema diverso. Le parti 5e dell'hexcrawl dell'Alexandrian (viaggio,
  foraggiamento) idem.
- **PX per il tesoro, tiri di reazione e di morale OSR**: cambiano l'economia della 3.5. Le
  soglie di morale le abbiamo già nel formato 3.5.
- **«Boxed text: usually not good» preso alla lettera**: il nostro tetto di 12 righe, un nome
  proprio, niente parentesi, è già la risposta alla critica di Bryce, e regge in un modulo che si
  legge al tavolo in italiano. Non va abolito, va solo tenuto corto. L'idea delle **parole chiave
  da improvvisare** può essere un ausilio facoltativo per il DM, non una sostituzione.
- **L'avversione di Bryce per i blocchi lunghi e per gli scontri bilanciati**: a 13° in 3.5 un
  PNG senza blocco completo è ingiocabile, e la calibrazione/DPR serve. Si accorcia lo sgherro,
  non il boss.
- **«Gli umanoidi diventino banditi»** e la preferenza OSR per vermi, melme e non morti: è
  gusto da bassi livelli; non si applica a un esercito di Hobgoblin e draghi.
- **Incontri casuali procedurali pesanti dentro i siti con roster**: l'Alexandrian stesso dice di
  non mescolarli. A 13° un incontro casuale costa risorse vere (incantesimi al giorno) e
  pochissimo tempo di storia `[DEDOTTO]`: usarli con parsimonia e solo con uno scopo.
- **Hexcrawl completo**: la campagna è ad archi, non un sandbox; basta il pointcrawl.
- **Geometria non euclidea e spazi extradimensionali** come tecnica generica: possibili per un
  luogo (Forgia, piani), ma rischiano di rompere `collaudo_mappe` e l'export UVTT; vanno con
  `@deroga`.
- **Eliminare del tutto le contingenze**: la riga sconfitta-senza-TPK e le contingenze ovvie
  restano; si taglia solo l'albero.
- **One Page Dungeon come formato del master**: troppo poco spazio per la meccanica 3.5 di alto
  livello; va bene solo come foglio-riassunto del sito.
- **Mappe di Dyson senza leggere l'accordo completo** e senza credito: i diritti morali
  canadesi vietano associazioni a «cause o istituzioni»; il testo dei suoi post non è coperto.

---

## Fonti lette (URL)

- https://thealexandrian.net/wordpress/38547/roleplaying-games/the-art-of-the-key-part-4-adversary-rosters
- https://thealexandrian.net/wordpress/52083/roleplaying-games/ptolus-running-the-campaign-prepping-porphyry-house
- https://thealexandrian.net/?p=48582
- https://thealexandrian.net/creations/misc/node-design/node-design2.html
- https://www.thealexandrian.net/creations/misc/node-design/node-design5.html
- https://thealexandrian.net/creations/misc/node-design/node-design7.html
- https://thealexandrian.net/?p=8176
- https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots
- https://thealexandrian.net/wordpress/37422/roleplaying-games/dont-prep-plots-tools-not-contingencies
- https://thealexandrian.net/wordpress/13085/roleplaying-games/jaquaying-the-dungeon
- https://thealexandrian.net/wordpress/13103/roleplaying-games/xandering-the-dungeon-part-2-xandering-techniques
- https://thealexandrian.net/?p=44474
- https://thealexandrian.net/wordpress/37995/roleplaying-games/game-structure-party-planning
- https://thealexandrian.net/wordpress/48666/roleplaying-games/pointcrawls
- https://thealexandrian.net/wordpress/46020/roleplaying-games/5e-hexcrawl
- https://thealexandrian.net/wordpress/46498/roleplaying-games/hexcrawl-errata-using-encounter-tables
- https://thealexandrian.net/wordpress/46535/roleplaying-games/how-to-prep-a-module-part-2
- https://thealexandrian.net/wordpress/42918/roleplaying-games/dragon-heist-remix-part-7-how-the-remix-works
- https://thealexandrian.net/?p=41217 (Remix parte 1: niente regole sui colpi, solo rimandi)
- https://thealexandrian.net/?p=38259 (indice dei cheat sheet: nessun formato di campi)
- https://thealexandrian.net/wordpress/4974/roleplaying-games/halls-of-the-mad-mage
- https://thealexandrian.net/?p=979 · https://thealexandrian.net/creations/advanced-rules/stat-block.html
- https://tenfootpole.org/ironspike/?page_id=1201 · https://tenfootpole.org/ironspike/?p=3870 · https://tenfootpole.org/ironspike/?p=2773
- http://into-the-dark-rpg.blogspot.com/2016/07/bryce-lynchs-adventure-design-tips.html (secondaria)
- https://www.osr.camp/principia-apocrypha
- https://slyflourish.com/eight_steps_2023.html · https://slyflourish.com/great_adventure_criteria.html
- https://www.scabard.com/features/5-room-dungeon (secondaria, con permesso di Johnn Four)
- https://dysonlogos.blog/maps/commercial-maps/
- https://paizo.com/threads/rzs2np78 · https://forum.profantasy.com/discussion/comment/124863/
- https://paizo.com/threads/rzs2hnfa · https://paizo.com/threads/rzs2g9fp · https://paizo.com/threads/rzs2gtw7&page=1
- https://www.enworld.org/posts/4897838/ · https://www.enworld.org/threads/the-incredible-shrinking-stat-block.310846/
