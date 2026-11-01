# B8 — La cisterna di Rethmar e l'assedio

> Lotto B8 di [PIANO-STANDALONE-GIARDINO-SALE-CALCE](../../PIANO-STANDALONE-GIARDINO-SALE-CALCE.md), progetto, 2026-11-01. Richiesta del DM: *«collegandolo a rethmar per 3.5 in modo da dare una scelta ampia a i pg con conseguenze anche ai difensori dell'assedio e o vantaggi agli attaccanti»*.
> Si aggancia a quello che il repo ha già, senza aprire contatori nuovi: il **Fronte** (STRUTTURA §9.1 di ARC-09 P3), il **Morale Cittadino** (`Bestiario/png/Consiglio_Rethmar/` §C2, che ha già la riga «cisterne avvelenate non risolte −1»), i **contingenti** e gli **scenari** di `difensori_rethmar` in `campaign/state.yaml`, i clock di **Sonjak** (4/8) e di **Sal** (0/6), e i valori di supporto di Fase 1 («Drow sabotaggio 0/1/2»). È la regola usata per Mira Serani: *ogni intel alimenta i clock esistenti, non ne apre uno nuovo*.

## La verità (versione 3.5)

Sotto la piazza del mercato di Rethmar c'è la **Grande Cisterna**, scavata sul modello delle cisterne del Calimshan da un ingegnere venuto da laggiù, **Mastro Tariq**. Con l'assedio alle porte è l'acqua della città: chi la controlla decide quanto resiste Rethmar.

**Sonjak** ha bisogno di una strada sotto le mura per la Notte dei Drow (Fase 0) e di una città assetata per la Fase 1. Il **Collezionista** vuole altro: il **Cuore di Selenite**, una gemma del Piano dell'Acqua strappata a un santuario del Sottosuolo, da far crescere dentro una città viva. **Sal**, l'agente di superficie di entrambi, ha comprato Tariq con la promessa di Umberlee e ha portato nella cisterna **Karkator**, l'aboleth mezzo-immondo uscito dagli esperimenti sulle aberrazioni di Sonjak (il waypoint «Sonjak halt — aberrazioni experiments» del ledger). Karkator usa il Cuore per corrompere l'acqua e asservire chi la beve. La galleria di drenaggio sul fondo arriva ai campi drow sotto la linea di Rethmar, dove Zin'thara raccoglie prove contro Sonjak.

Le tre parti non si fidano l'una dell'altra, come nell'Abbazia: Sonjak vuole il tunnel, il Collezionista il Cuore, Karkator una città di schiavi. I PG che lo capiscono possono metterle una contro l'altra.

## Gli ingressi (richiesta del DM del 2026-11-01)

*«una e sotto la cripta della cattedrale […] e poi una altra entrata nascosta da scoprire con minacce diverse in relazione a quale parte della mappa sottostante scendono»*. La cattedrale del canone è la **Cattedrale di Lathander** nel quartiere alto (n. 18 della pianta di Rethmar, `scripts/piante/rethmar.py`), dove sta **Tredora Occhidoro** (`Bestiario/png/Secondo_Anello_Rethmar/`). Non va confusa con le cripte del **Tempio di Rethmar** (n. 16), che sono il bersaglio della Notte dei Drow.

| Ingresso | Come lo trovano | Dove arrivano | Chi li aspetta | Cosa cambia |
|---|---|---|---|---|
| **A · La cripta della Cattedrale di Lathander** | Brenna o Tredora: quando la cisterna fu scavata, il clero dell'Alba benediceva l'acqua, e dalla cripta parte la vecchia galleria di servizio. Tredora dà la chiave | **quota media (+6 m)**, sul ponte ovest della Torre delle Volte | gli skum di guardia e l'allarme di Tariq: si entra nello scontro della Torre da una parte sola | è la via «onesta»: Tredora può scendere fino alla soglia e offrire il *consacrare* per purificare il Cuore (riga 1). Sal ha un uomo fra i sacrestani, e Tariq lo sa |
| **B · Lo sfioratore calishita (nascosto)** | va scoperto: le carte di Tariq nella sua bottega, un profugo di Lorana che di notte ha visto «uomini-pesce» uscire dal fiume, la corrente che a valle del ponte gira al contrario. Conoscenze (architettura e ingegneria) o Sopravvivenza CD 20 per capire dove sbocca | **il fondo (−12 m)**, nella galleria di drenaggio sotto la riva del Cannath, vicino al Ponte (n. 7) | acqua alla gola e corrente; i **chuul** nell'acqua bassa; asserviti in catene che lavorano alla galleria; esploratori drow di Sonjak di passaggio | arrivano alle spalle di tutto, nel punto della galleria verso il Sottosuolo (righe 10-11) e sotto il Santuario: possono colpire Karkator prima della Torre, ma dal punto più pericoloso. Chi passa di qui vede la strada dei drow e trova le prove della riga 12 |
| **C · Il pozzo grande del mercato** | è sotto gli occhi di tutti: la gabbia di discesa della chat, sotto i cinque pozzi di luce del foro (n. 8 e 13) | **quota alta (+15 m)**, sulle passerelle | i **Ragni delle Catene** e la nebbia di calce | è la via più rapida e la più esposta: Mira Serani e gli uomini di Sal tengono d'occhio la piazza (riga 4) |

L'ordine degli scontri dipende dall'ingresso: da A si comincia dalla Torre, da B dal Santuario e dalla galleria, da C dai ragni. Il modulo scrive ogni area con le reazioni per chi arriva da ognuna delle tre parti. Chi è già allertato e da quale direzione lo dicono le tattiche della Torre e del Santuario, come nell'Abbazia per le tre vie di discesa.

## Le scelte dei PG e le conseguenze sull'assedio

Ogni riga dice cosa cambia **per i difensori** e cosa **per gli attaccanti**. I valori si sommano a quelli della matrice ESITI §2 e del Morale Cittadino e non li sostituiscono.

| # | Scelta | Difensori | Attaccanti |
|---|---|---|---|
| 1 | **Purificare il Cuore** (*consacrare* o *santificare* sull'altare, rito sotto pressione) | acqua pulita per tutto l'assedio: Morale Cittadino +1; il Fronte non scende mai per sete | il Collezionista perde il premio e lo cerca: un incontro con lui in Fase 2-4 diventa probabile |
| 2 | **Distruggere il Cuore** | la cisterna torna pulita in 24 ore; nessun bonus oltre a togliere il malus | — |
| 3 | **Tenere il Cuore corrotto** (Artemis può sintonizzarsi: patto) | un'arma: una volta nell'assedio *inversione della gravità* su un settore (nega una carta drago o una breccia) | ogni uso fa avanzare di 1 il clock di Sonjak: lei *sente* il Cuore. Il Morale scende di 1 se si sa |
| 4 | **Rendere pubblica la corruzione** prima di risolverla | Morale −1 subito (panico, code ai pozzi); se poi la risolvono in pubblico +2 | Mira Serani lo riferisce: l'orda sa che la città ha poca acqua (CD di Morale delle ondate +2 finché la cisterna non è pulita) |
| 5 | **Tenere tutto segreto** | nessun malus subito; se falliscono, al Giorno 40 Morale −2 invece di −1 | — |
| 6 | **Catturare Tariq vivo** e portarlo al Consiglio | come «Halveth smascherato»: Morale +1. Sa dell'**Olio del Sabotaggio**: se i PG agiscono, il trigger del clock di Sal (l'olio sulle armi, rischio di TS fallito contro il boss di Fase 3) non scatta | Sal capisce di essere scoperto e anticipa: la consegna delle statue a Varis (Fase 4) scatta un giorno prima |
| 7 | **Uccidere Tariq** | nessuna testimonianza; le chiuse vanno riparate (un giorno di lavoro, una prova di Conoscenze (architettura e ingegneria) CD 25) | — |
| 8 | **Curare gli asserviti** (operai della cisterna e guardie che hanno bevuto) con *rimuovi maledizione* o spezzando il Cuore | +150 miliziani di nuovo in forza (contingente «Guarnigione») e Morale +1 | — |
| 9 | **Lasciare gli asserviti al loro destino** o ucciderli in combattimento | la guarnigione perde 150 uomini; Morale −1 se si sa | nella Notte dei Drow gli asserviti aprono una poterna: un settore parte già in breccia |
| 10 | **Murare la galleria verso il Sottosuolo** (*muro di pietra*, *scolpire pietra*, o crollo controllato) | «Drow sabotaggio» +1 (una strada in meno per la Fase 0) | Sonjak deve passare dall'altra galleria, più lunga: la Notte dei Drow perde un'ondata |
| 11 | **Tendere un'imboscata nella galleria** e lasciarla aperta come esca | se riesce, «Drow sabotaggio» +2 e i prigionieri drow parlano | se fallisce, la cisterna diventa la testa di ponte della Fase 0 sotto la piazza del mercato |
| 12 | **Leggere le carte nello studio di Tariq**: ricevute di Sal, ordini con il sigillo di Sajak | sono le prove dei traffici Sonjak↔Collezionista: valgono come le due lettere di Ghaurush per trattare con Zin'thara (il suo clock sale di 2) | — |
| 13 | **Lasciare vivi i Ragni delle Catene** | — | nella Notte dei Drow i ragni escono dai pozzi di luce nella piazza: carta d12 «assassino» automatica su un comandante |
| 14 | **Lasciar fuggire Karkator** nel Sottosuolo | — | in Fase 2 Karkator è il «focus» di un rituale di Sonjak: una carta EVENT-DECK in più, CR 16 |
| 15 | **Tempo speso** | ogni giorno nella cisterna è un giorno di March Clock | — |

**Soglia di fallimento.** Se al Giorno 40 il Cuore è ancora acceso nella cisterna valgono la riga del Morale «cisterne avvelenate non risolte» (−1), il Fronte −1, e la riga 9 (asserviti). Questa è la versione che il ledger chiama già «sabotaggi parziali».

**Risultato migliore.** Cuore purificato, Tariq catturato, galleria murata o imboscata riuscita, asserviti curati: Fronte +1, Morale da +3 a +4, 150 uomini e «Drow sabotaggio» 2. Da solo non cambia lo scenario, ma sposta lo scenario «medio» verso «ottimale» insieme alle altre quest.

## PNG e villain coinvolti (tutti già nel canone, salvo i nuovi segnati)

| Chi | Dove sta nel repo | Cosa fa qui |
|---|---|---|
| **Sal** (Salvatore della Luna d'Argento) | state.yaml, villain | ha comprato Tariq e porta l'Olio del Sabotaggio; scena possibile in superficie |
| **Sonjak** (Matrona Sajak) | state.yaml, villain | mandante del tunnel; non compare, firma gli ordini |
| **Il Collezionista** | state.yaml, villain | vuole il Cuore; non compare se non per la riga 1 |
| **Mira Serani** | `Bestiario/villain/Mira_Serani/` | infiltrata fra i profughi: osserva i PG alla discesa e riferisce (righe 4 e 6) |
| **Zin'thara Vel'Ryn** | `Bestiario/villain/Zin_thara_Vel_Ryn/` | compra le prove della riga 12 |
| **Brenna Sorvane** | consigliera militare di Rethmar | chi affida la missione ai PG; riceve Tariq |
| **Lorana** | `Bestiario/png/Lorana/` | i profughi bevono per primi dai pozzi bassi: sono i primi asserviti |
| **Il Consiglio di Rethmar** | `Bestiario/png/Consiglio_Rethmar/` | Seduta straordinaria se la cosa diventa pubblica |
| **Mastro Tariq** *(nuovo)* | B4 | ingegnere calishita, chierico di Umberlee |
| **Karkator** *(nuovo)* | B4 | aboleth mezzo-immondo con il Cuore |
| **Ragni delle Catene** *(nuovi)* | B4 | guardiani delle volte |

## Le mappe da fare

Tutte in pianta da stampa (ADR-0106), alla scala del repo (1,5 m a quadretto), con i tre blocchi Ambiente, Tattiche ed Evoluzione del modello di mappa tattica.

| ID | Mappa | Tipo | Note |
|---|---|---|---|
| GS-0 | Rethmar, il quartiere del mercato con i cinque pozzi di luce | ambientazione | dal generatore della pianta di Rethmar (`scripts/piante/rethmar.py`), con l'ingresso della cisterna e la strada dei profughi |
| GS-1 | La cripta della Cattedrale di Lathander e la galleria di servizio (ingresso A) | tattica | Tredora, la sacrestia, il sacrestano di Sal |
| GS-1b | Lo sfioratore sotto la riva del Cannath (ingresso B) | tattica | acqua, corrente, la prima stretta della galleria |
| GS-1c | La piazza del pozzo grande e la gabbia di discesa (ingresso C) | tattica | scena in superficie, possibile scontro con gli uomini di Sal |
| GS-2 | La Grande Cisterna, quota alta (+15 m): passerelle, catene, nidi dei ragni | tattica | 40 × 27 quadretti |
| GS-3 | La Grande Cisterna, quota media (+6 m): arconi, ponti verso la Torre | tattica | stessa griglia, livello diverso |
| GS-4 | La Torre delle Volte e lo studio di Tariq | tattica di dettaglio | la ruota delle chiuse, la scala, le carte della riga 12 |
| GS-5 | Il Santuario di Sale: bacino, altare sommerso, il Cuore a +3 m | tattica | la colonna d'acqua dell'*inversione della gravità* segnata come zona |
| GS-6 | La galleria di drenaggio verso il Sottosuolo | tattica | il punto da murare o dove tendere l'imboscata (righe 10-11) |
| GS-S1 | Sezione verticale della cisterna, da +20 a −12 m | schema (`render_schemi.py`) | la vista laterale chiesta nella chat: quote, nebbia, livelli dell'acqua |
| GS-S2 | Sezione della Torre delle Volte | schema | chiuse e livelli |

La versione PF1e (Qasr al-Milah) usa le stesse piante della cisterna (GS-2…GS-S2) e una pianta di città sua al posto di GS-0 e GS-1.
