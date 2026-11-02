# Read-aloud per adulti che leggono fantasy

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- 1. La cosa che cambia tutto: **si ascolta, non si legge**
- 2. Lunghezza: la finestra reale è più corta di quanto sembri
- 2-bis. Il box di luogo: poche frasi, un ordine, niente creature
- 2-ter. Riscrivere un box che c'è: si taglia il superfluo, non ciò che si sente
- 3. Cosa premia questo pubblico
- 4. Cosa li fa staccare (e sono tutti errori di genere, non di lingua)
- 5. Il registro alto senza il ridicolo
- 6. Il dialogo dei PNG davanti a questo pubblico
- 7. La checklist prima di leggere ad alta voce
- 8. Rapporto con gli altri riferimenti
<!-- /indice -->

**Il pubblico di questo tavolo**: adulti acculturati, lettori di fantasy da
vent'anni. Hanno letto Tolkien, Martin, Le Guin, Wolfe, Salvatore,
Abercrombie. Conoscono i cliché del genere **meglio di chi scrive**, e li sentono
arrivare da lontano.

Questo cambia tre cose in modo non negoziabile:

| Non serve | Serve |
|---|---|
| spiegare cosa provano | **fidarsi che lo capiscano** |
| dire che è epico | **una cosa concreta e vera**, e l'epica la costruiscono loro |
| offrire un mondo | **offrire competenza**: che chi racconta sappia come funziona una forgia |

> **Il criterio unico.** Se il tuo box regge davanti a qualcuno che ha letto
> *Il Signore degli Anelli* tre volte, regge. Se gli sembra «già visto», è già
> visto — non è severità, è memoria.

---

## 1. La cosa che cambia tutto: **si ascolta, non si legge**

Un read-aloud non è prosa: è **testo parlato**. Il lettore di un libro può
tornare indietro; chi ascolta no. Da qui i vincoli che la pagina non ha:

1. **Un solo nome proprio nuovo per box.** Chi ascolta non può rileggere.
   Se in un box compaiono *Skullcrusher*, *Thorgrim* e *Barbadiferro*, la
   metà del tavolo ne ha persi due.
2. **Massimo due livelli di subordinate.** Al terzo, l'orecchio perde il
   filo del soggetto anche se l'occhio non lo perderebbe.
3. **Niente parentesi, niente incisi lunghi fra trattini.** All'orale non
   esistono: diventano una frase che si interrompe e non riprende.
4. **Ri-ancorare i soggetti.** Dopo tre righe, «lui» non è più nessuno.
   Ripeti il nome: nel parlato la ripetizione è chiarezza, non povertà.
5. **L'ultima cosa detta è quella che resta.** Metti in fondo ciò che vuoi
   che ricordino, e **non aggiungere niente dopo**.
6. **Il box non decide per il giocatore** (P1, dalle linee guida di
   *Dungeon*). Niente *«entrate»*, *«vedete»*, *«ti accorgi»*, *«senti»*: il box
   dice cosa c'è, il giocatore dice cosa fa e cosa prova. Restano fuori i
   dialoghi, le visioni d'artefatto e i testi per **un solo** giocatore (echi,
   hint), dove la seconda persona è la scelta giusta. Misura:
   `misura_craft --p1` (D14 di PIANO-AGENT-SKILLS-ESTERNE).
7. **Niente *«sembra»* né *«pare»*.** Il narratore che esita toglie al tavolo
   la certezza su ciò che vede: se la sala è vuota, è vuota; se non lo è, la
   cosa che non torna si descrive. *«Come se»* resta, perché è un paragone.
   Viene da Shawn Merwin (*D&D Beyond*); misura: `punteggio_mqm.py`, norma
   `box_sembra_pare`, col rilevatore `validate_prosa.sembra_esitanti` (D13).
   **Il confine**: *«sembra»* seguito dalla smentita resta. *«Quella che
   sembrava una parete — è una palpebra»*: lì il narratore non esita, prepara
   il colpo. La smentita arriva entro la frase dopo, con *«invece»*, *«non lo
   è»*, *«si rivela»* o un trattino seguito da *«è»*; più lontano, è di nuovo
   un'esitazione (D17 di PIANO-AGENT-SKILLS-ESTERNE, 2026-10-03).

**Prova pratica, dieci secondi**: leggi il box **ad alta voce**. Se ti manca il
fiato, se devi rileggere una riga, se inciampi su un nome — il testo è
sbagliato. Non è il tuo respiro: è la frase.

---

## 2. Lunghezza: la finestra reale è più corta di quanto sembri

| Tipo di box | Righe | Perché |
|---|---|---|
| **Apertura di scena** | 8-12 | è l'unico momento in cui hanno pazienza per la descrizione |
| **Round di combattimento** | 2-4 | stanno aspettando di agire: ogni riga in più è tempo rubato |
| **Micro-box per PG** (rito, skill challenge) | 2-3 | uno a testa, in fila: la somma è già lunga |
| **Rivelazione / colpo di scena** | 4-6 | corto. La brevità **è** il colpo |
| **Chiusura di sessione** | 6-10 | possono di nuovo ascoltare, la tensione è scesa |

⚠️ **Oltre le 12 righe l'attenzione cade, e con adulti cade in silenzio** —
non ti interrompono, smettono di ascoltare e tu non te ne accorgi. Se un box
supera le 12 righe: o è due box, o metà è ridondante.

**Le lunghezze variano.** La tabella sopra è già una varietà: un box d'urto da
due righe accanto a un'apertura da dieci. Un autore umano alterna così; un
master riscritto per stare sotto i tetti tende a fare tutti i box uguali. Nel
corpus di riferimento (`plans/esperimenti/avventure-community/note-prosa-corpus.md`
§2) il 46-52% dei box sta fra 30 e 70 parole; il rifacimento di ARC-07 della
#249 ci metteva il 90%, e il DM ha chiesto di riportarlo verso il corpus.

⚙️ `misura_craft --stile`, colonna `30-70`: la quota dei box fra 30 e 70
parole. È un indicatore e non un tetto (ADR-0036 non vuole soglie assolute
sulla prosa di gioco): sopra il 70% i box sono più regolari di qualunque
autore misurato, e vale la pena guardarli.

---

## 2-bis. Il box di luogo: poche frasi, un ordine, niente creature

Le linee guida per gli autori di *Dungeon* (Paizo, era 3.5) dicono che il
read-aloud di un'area **solo di rado supera poche frasi**, e che i testi lunghi
stanno meglio in un handout. Dicono anche una cosa che il repo non aveva
scritto: **il box di un luogo non descrive le creature che ci sono**, perché
dove stanno e cosa fanno dipende da come arrivano i PG (se li hanno sentiti,
se è giorno o notte). Fonte e misure: `RICERCA-STANDARD-PROSA-WOTC-PAIZO` §1.4.

**Il box di luogo** (una stanza, una radura, un cortile) segue un ordine che
funziona quasi sempre:

1. **com'è lo spazio e com'è la luce**, per paragone con cose già viste
   (ADR-0014: le misure vanno nei **Dati per il DM**, non nella voce);
2. **cosa lo occupa**: poco, e solo ciò con cui i giocatori vorranno fare
   qualcosa;
3. **per ultima, la cosa strana o pericolosa**, quella che chiama un'azione.
   È il punto 5 del §1 applicato al luogo: l'ultima cosa detta è quella che
   resta.

Poi **il box si ferma**: prima dell'iniziativa e prima di qualunque azione dei
PG. Chi c'è entra con la sua **scheda d'entrata** o con un box suo
(ADR-0073), non dentro la descrizione della stanza.

> *La volta è crollata a metà, e dalla breccia scende la luce della luna.
> Fra i blocchi di marmo caduti, una fontana a forma di drago getta un liquido
> rosso e denso che non fa schiuma. Tre porte di legno marcio, una per parete.
> L'aria sa di zolfo.*

Quattro frasi, e nessuna misura: la stanza si capisce dal paragone, e i nove
metri di lato stanno nei Dati per il DM.

**Il box d'area** (un livello intero del dungeon, una città, una valle) è
l'**apertura di scena** della tabella del §2: 8-12 righe, letta una volta,
quando il tavolo sa che comincia una parte nuova. Lì vanno il clima, la luce
e la forma del luogo intero. La storia del luogo ci entra solo come cosa che
si vede (un'iscrizione consumata, un muro rifatto due volte), mai come
spiegazione.

⚙️ `python3 scripts/misura_craft.py --box` conta i box oltre le **quattro
frasi** e oltre i **500 caratteri**. Sono indicatori, non soglie: il tetto del
repo resta quello delle righe, finché il DM non decide (PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE, D1).

## 2-ter. Riscrivere un box che c'è: si taglia il superfluo, non ciò che si sente

Il primo confronto cieco del DM (2026-10-18, [ADR-0093](../../../plans/adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md),
`plans/esperimenti/prosa-cieco/ESITO-ARC07-2026-10-18.md`) ha messo una
riscrittura di ARC-07 contro l'originale: 8 a 8. I numeri del repo erano
migliorati tutti; il DM no. E le sue scelte avevano due regole.

1. **Una riscrittura non toglie dettagli sensoriali.** Luce, colore, suono,
   caldo e freddo, il corpo che sente: dove la versione nuova ne aveva meno,
   il DM ha scelto la vecchia cinque volte su cinque. Si tagliano le
   maiuscole d'enfasi, le date, i nomi in più e le spiegazioni: lì la nuova
   ha vinto.
2. **Un monologo resta un blocco.** Spezzarlo in battute con un inciso in
   corsivo fra l'una e l'altra ha perso tutte e due le volte. Il gesto
   dentro il monologo si scrive dentro il monologo.

⚙️ `python3 scripts/cieco_versioni.py coppie` applica le due regole a ogni
coppia di versioni e manda al cieco solo quelle che non decide, più quattro
di controllo; `misura_craft --stile` conta i dettagli sensoriali per file
(colonna `sens.`). ⚠️ Il tetto di un nome proprio **nuovo** per box (§1) non chiede di togliere i
nomi che il tavolo conosce: `misura_craft --box` conta i nomi **distinti**,
perché non sa quali siano nuovi, e un nome noto cambiato in perifrasi per
stare sotto quella colonna insegue l'indicatore, non la norma. Il voto non ne
fa una terza regola: Moradin diventato «il dio dei nani» ha perso (coppia 5),
ma Fauci di Palude diventato «un drago enorme dalle ali nere» e Hella
diventata «la druida» hanno vinto (6 e 10).

Le due regole vengono da sedici coppie e da un lessico
scritto dopo averle viste: se il DM smentisce più di un controllo su quattro,
`esito` lo dice e si torna al cieco intero.

Il cieco del 2026-10-22 (catena vecchia contro nuova su 16 box di ARC-07 e
ARC-08, `plans/esperimenti/qualita-misurabile-2026-10-22/riscrittura/ESITO-VOTO.md`,
8 a 5 per la vecchia) aggiunge tre cautele per chi riscrive:

3. **Non si taglia la frase che chiude con enfasi.** Togliere la riga che
   «spiega» (l'etichetta LAMP) ha perso quattro volte su quattro: lo
   spettacolo «terrificante e magnifico», la chiusa sull'eroe. Si tolgono
   le parole goffe, tradotte o ricercate, non la chiusa.
4. **Spezzare una subordinata non è un rimedio automatico.** Nella prova ha
   vinto una volta e perso una, e sulle 38 coppie già votate vince più spesso
   la versione con più subordinate (11 su 12). Si spezza solo dove al terzo
   livello l'orecchio si perde (§1, regola 2), non per far tacere un indicatore.
5. **Un rilievo di `misura_sintassi` si guarda prima di riscrivere.** Tre
   riscritture fatte su un falso del parser hanno perso tutte, due per
   «ritmo». Il soggetto messo dopo il verbo, quando il calco è vero, ha
   vinto.

---

## 3. Cosa premia questo pubblico

### La competenza concreta

Il modo più veloce per essere creduti è **sapere come funzionano le cose**. Un
lettore adulto perdona un drago, non perdona un fabbro che lavora male.

> ❌ *«La spada era di fattura splendida, forgiata con maestria antica.»*
> ✅ *«Sul filo, a guardarla in controluce, si vede la piega: l'hanno
> ripiegata sette, otto volte. Chi l'ha fatta ci ha messo un mese e non
> aveva fretta.»*

Le aree in cui vale la pena essere precisi in questa campagna: **metallo e
forgia** (tempra, piega, scoria, vena), **pietra** (strati, faglia, umidità,
il suono che cambia con lo spessore), **assedio** (logistica, turni di
guardia, cosa mangia un esercito), **animali e tempo** (come si comporta un
cane prima di un temporale).

### L'allusione al posto dell'affermazione

Il piacere di un lettore esperto è **completare**. Lasciagli il lavoro.

> ❌ *«Capisci che il vecchio ha ucciso molti uomini in vita sua.»*
> ✅ *«Ti versa da bere con la sinistra. La destra resta sul tavolo, aperta,
> rivolta verso di te.»*

### Il dettaglio che non serve a niente

Tutto ciò che è significativo insieme diventa scenografia. **Una cosa per
scena deve essere solo vera**: una cinghia allentata, un odore di cavolo,
qualcuno che ha le mani sporche di grasso. Non paga in trama. Paga in mondo.

### La reticenza sull'emozione

> ❌ *«Provi una tristezza profonda e inaspettata.»*
> ✅ *«Durin si ferma. Si toglie l'elmo, e non dice niente.»*

Il comportamento al posto dell'etichetta. Sempre. E il comportamento è di
**qualcun altro**, o del mondo: quello del PG lo decide il giocatore (punto 6).
Fino al 2026-10-01 l'esempio qui sopra era *«Ti accorgi che hai smesso di
camminare»*, che decideva proprio questo (D14).

---

## 4. Cosa li fa staccare (e sono tutti errori di genere, non di lingua)

| Difetto | Come suona | Rimedio |
|---|---|---|
| **Voce YA** | battute, ironia costante, personaggi che si prendono in giro sotto pressione | il registro floor della campagna: adulto, lento, nessuna strizzata d'occhio |
| **Tutto epico** | ogni scena è la più importante di sempre | **inflazione**: se tutto è epico, l'epico non esiste. Massimo **un** picco a sessione |
| **Esposizione travestita da dialogo** | *«Come sai, Thorik, la Corona fu forgiata…»* | nessuno spiega a un altro cose che sa già. Se serve l'informazione, che la dia il mondo |
| **Aggettivi viola** | «un'oscurità pulsante e malevola» | un sostantivo concreto batte due aggettivi. Sempre |
| **Il predestinato senza costo** | il party è speciale e basta | in questa campagna nessuna vittoria è gratis: è la regola di coerenza §4 |
| **Il mostro spiegato** | «è un elementale della terra avanzato» detto ai PG | i PG vedono una collina che respira. Le categorie stanno nello statblock |

---

## 5. Il registro alto senza il ridicolo

Un pubblico colto **regge** e apprezza il registro alto — a due condizioni:

1. **Una volta sola per scena.** L'anastrofe, il passato remoto, la
   solennità: sono spezie. *«Grande era il silenzio, e vecchio.»* è bello
   perché intorno c'è prosa normale.
2. **Mai sulla logistica.** Il registro alto si usa per il divino, la
   memoria, la morte. Non per aprire una porta.

**Il salto di registro è lo strumento più forte che hai**: dieci righe di
concreto sporco, e poi una riga che si alza. L'effetto è tutto nello scarto.

---

## 6. Il dialogo dei PNG davanti a questo pubblico

- **Nessuno parla in modo grammaticalmente perfetto.** Fai interrompere,
  ripetersi, correggersi: *«Era… no. Non era così. Era peggio.»*
- **L'idioletto batte l'accento.** Non «parla con accento rude»: dagli **una
  costruzione sua** che ripete. Balvar parla di ciò che è già accaduto al
  passato remoto perché per lui lo è. I Bracieri dicono meno del necessario.
- **Il silenzio è una battuta.** *«Non risponde. Continua a incidere.»* dice
  più di tre righe.
- Mai gli epiteti da romanzo di serie B: «il nano», «l'elfo», «il guerriero»
  al posto del nome. All'orale è già confuso; per iscritto è pigro.

---

## 7. La checklist prima di leggere ad alta voce

- [ ] L'ho **letto ad alta voce** almeno una volta?
- [ ] Sta **sotto le 12 righe** (2-4 se è un round)?
- [ ] Se è un box di luogo: spazio e luce, poi cosa lo occupa, per ultima la
      cosa strana; **nessuna creatura** dentro, e si ferma prima dell'azione?
- [ ] C'è **al massimo un nome proprio nuovo**?
- [ ] Nessuna subordinata di terzo livello, nessuna parentesi?
- [ ] Nessun *«vedete»*, *«entrate»*, *«ti accorgi»*, che decidono al posto del giocatore?
- [ ] Nessun *«sembra»* o *«pare»*?
- [ ] C'è **una cosa concreta e competente** (materiale, mestiere, tempo)?
- [ ] C'è **un dettaglio che non serve a niente**?
- [ ] Ho tolto **la frase che spiega** l'ultima immagine?
- [ ] Il registro alto compare **una volta sola**, e non su una porta?
- [ ] L'**ultima riga** è quella che voglio gli resti?
- [ ] Se è un box di combattimento, finisce su **«Che fate?»**?

---

## 8. Rapporto con gli altri riferimenti

| Cosa | Dove |
|---|---|
| La **lingua** (calchi, ritmo, tic dell'IA) | `italiano-nativo.md` |
| La **voce** (i nove pilastri, il mix per scena) | `style-pillars.md` |
| Il **mistero** (indizi, documenti, errore fecondo) | skill `rumblingstone-indagine` |
| La **pagina** (blockquote, grassetti, terminologia) | `editorial-standards.md` |
| L'**obbligo di regia** (nessuna sequenza a battute senza box) | ADR-0014 |
| **Questo file** | il *pubblico*: cosa regge e cosa stacca un adulto che il fantasy lo conosce |

> **Ordine d'applicazione**: prima la voce, poi la lingua, **poi questo** — che
> è l'ultima passata, quella in cui ti metti dalla parte di chi ascolta invece
> che di chi scrive.
