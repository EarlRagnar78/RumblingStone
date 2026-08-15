# RICERCA — cosa vale la pena prendere dal panorama dei tool per DM (agosto 2026)

**Aperta**: 2026-08-15
**Domanda-fonte (DM)**: *«può servire analizzare questi thread Reddit per vedere cosa
si può usare o quali idee includere nel repo e nel mini modulo, se ha senso e porta
valore aggiunto ed è compatibile con le licenze»* — con due link:
`r/rpg/comments/1rd55ll` (*my favourite DM tools after testing 15 different apps*) e
`r/dndai/comments/1be4zkb` (*RPG AI tools mega-discussion thread*).

> **La conclusione in due righe**: di quindici app testate da altri, **due idee
> valgono il costo** — la trascrizione locale della sessione (§3) e **l'ancora a una
> scuola pittorica in pubblico dominio** per tenere insieme le immagini generate
> (§3-bis). Il resto o è già nel repo in forma migliore, o è un servizio che non si
> può importare. E il commento più utile dei due thread **non consiglia un tool: ne
> critica uno** — vedi §3.1.

---

## §0 · Come è stata fatta, e cosa è cambiato in corsa

**Prima passata (blind)**: i due thread **non sono raggiungibili da questo ambiente** —
Reddit è bloccato a monte, il proxy risponde `CONNECT tunnel failed, 403` su `curl`,
la fetch diretta rifiuta il dominio, gli estrattori esterni falliscono sull'URL. Ho
avuto solo l'anteprima dei motori di ricerca: l'elenco troncato *«Notion; Saga20;
Syrinscape …»* e la riga d'apertura del mega-thread. L'analisi partiva quindi dalle
**categorie**, non dai nomi.

**Seconda passata (2026-08-15, testo fornito dal DM)**: il DM ha incollato il
contenuto dei due thread, commenti compresi. Da lì sono usciti **cinque nomi nuovi**
che la prima passata non poteva conoscere — Lost Atlas, Shieldmaiden, Pocketbard,
Tokenstamp 2, Owlbear Rodeo — e, cosa più utile, **un'obiezione argomentata alla
raccomandazione principale**. Questo documento è la versione dopo la seconda passata:
dove la prima aveva ragione l'ho lasciata, dove aveva un buco l'ho detto.

---

## §1 · Il panorama, per categoria — e cosa risponde già il repo

| Categoria | Chi la occupa fuori | Cosa ha il repo | Divario reale |
|---|---|---|---|
| **Wiki di mondo** | Notion, Obsidian, World Anvil, Kanka | markdown in git + `validate_*` + skill di canone | **nessuno**: qui il canone è versionato e validato a macchina, cosa che nessuno dei quattro fa |
| **Tracker di campagna / recap** | Saga20, GM Assistant, Tabletop Arc, Archivist | `state.md` + `state_apply.py` + `session_recap.py` + `next_session.py` | **uno, e vero**: manca il pezzo *audio → verbale di sessione*. Vedi §3 |
| **Ambiente sonoro** | Syrinscape, Tabletop Audio | cue **descritti**, non brani (ADR-0014, cassetta del DM §5) | nessuno — e la forma del repo è **più portabile**, vedi §2.3 |
| **Mappe** | Inkarnate, Dungeondraft, Dungeon Alchemist | contratto JSON → master → SVG → PNG → UVTT | nessuno sul funzionale; il divario è **artistico**, ed è già tracciato (Lotto 6) |
| **Impaginazione** | Homebrewery, Affinity | `build_booklet_html.py` + Homebrewery self-hosted | tipografia embedded, già tracciata |
| **Al tavolo** (iniziativa, HP) | Improved Initiative, Fight Club, DM's Toolbox | niente — **per scelta** | fuori perimetro: questo è un repo di documenti, non un'app di gioco |
| **Generazione immagini** | Midjourney, ChatGPT Images, CharGen | prompt standardizzati (ADR-0015) + ComfyUI locale | la produzione dei raster, già tracciata |

---

## §2 · I tre tool nominati nello snippet — verdetto uno per uno

### 2.1 Notion — ❌ non importabile, e non serve

SaaS proprietario. Il valore che il thread gli attribuisce (*world builder*) qui è già
coperto meglio: un database Notion non ha diff, non ha revisione, non ha gate. Il repo
ha `git`, `validate_bestiario`, `validate_maps`, `check_plans_discipline`.

**Idea da rubare**: nessuna. L'unica tentazione — i wiki-link `[[così]]` in stile
Obsidian — **peggiorerebbe** il repo: `validate_standalone.py` e `validate_modules.py`
verificano i link relativi, e i wiki-link li renderebbero non verificabili.

### 2.2 Saga20 — ❌ il servizio, ✅ l'idea

Tracker di campagna a **9 USD/mese** che registra la sessione, la trascrive e ne fa un
riassunto. La recensione comparativa più seria che ho trovato (EN World, tre tool a
confronto) gli dà il punteggio migliore ma segnala anche il problema che qui è
dirimente: nei concorrenti *«l'audio resta archiviato senza un modo chiaro di
cancellarlo»*.

**Non si importa** — è un servizio. **L'idea sì**, ed è l'unica del lotto che paga:
vedi §3.

### 2.3 Syrinscape — ❌ e il repo fa già meglio

Libreria sonora in abbonamento, con licenza per traccia. Importare i titoli dei brani
in un modulo creerebbe una **dipendenza che il lettore non può soddisfare
legalmente** senza pagare.

Il repo ha già la forma giusta, ed è scritta nella cassetta del DM del Drappo:

> *«Non serve una colonna sonora. Servono quattro cue per serata, e il silenzio in
> mezzo. Nessun titolo di brano: **descrizioni**, così ognuno usa quello che ha.»*

Un cue come *«un tamburo solo, lento, e poi stop netto sul nome»* funziona con
Syrinscape, con YouTube, con una playlist personale e con un DM che batte le nocche sul
tavolo. Un titolo di brano funziona solo per chi ha quell'abbonamento.
**Nessuna modifica**: questa è già la scelta migliore, e va lasciata in pace.

---

## §3 · La proposta principale — la trascrizione locale della sessione

**Il divario**, in una riga: `session_recap.py` legge
`campaign/sessions/YYYY-MM-DD_session-*.md` e ne ricava il recap per i giocatori. Ma
**quel file lo scrive il DM a mano, dopo**, quando è stanco — ed è il punto in cui la
catena si rompe più spesso. È esattamente ciò che Saga20 e simili vendono a 9-27 USD
al mese.

**La versione license-clean**: [whisper.cpp](https://github.com/ggml-org/whisper.cpp) —
**licenza MIT**, implementazione C/C++ senza dipendenze, inferenza **CPU-only**, e
soprattutto **interamente locale**: i pesi si scaricano una volta e poi non c'è
nessuna rete. Il problema di riservatezza dei servizi cloud — la voce dei giocatori
caricata su un server terzo — **non si pone**: l'audio non esce dalla macchina del DM.

Forma proposta: `scripts/transcribe_session.py`, che prende un file audio e produce la
**bozza** del verbale nel formato che `state_apply.py` e `session_recap.py` già
leggono, con i campi obbligatori vuoti e da riempire.

⚠️ **Non è una decisione da prendere di sfuggita**, e per questo qui c'è la proposta e
non il codice:

1. sarebbe la **prima dipendenza da un binario esterno** nel toolkit — finora tutto è
   stdlib o browser headless. ADR-0012 chiede il manifest; questo chiede **un ADR
   suo**, con la regola di degradazione (se il binario non c'è, lo script dice come
   installarlo ed esce pulito, non fallisce a metà);
2. tocca il **consenso**: registrare i giocatori si chiede prima. La regola va scritta
   nel tool, non lasciata al buon senso;
3. la trascrizione produce una **bozza**, mai canone. ADR-0007 (triplo vincolo sulle
   scritture di canone) resta intatto: il DM legge, taglia e firma.

**Costo stimato**: mezza giornata per lo script + l'ADR. **Guadagno**: chiude C3 della
ricerca precedente e toglie l'attrito dove la campagna lo perde davvero.

### 3.1 · L'obiezione, che è fondata — e come cambia la proposta

Il commento più votato del thread r/rpg non consiglia un tool: **ne critica uno**, e
colpisce esattamente questa proposta.

> *«I giocatori che amano prendere appunti e a volte fraintendono alcune cose, che
> diventano veri e propri punti della trama che rubo da loro? Quella cosa è morta con
> le note delle sessioni trascritte.»*

Ha ragione, e non è un dettaglio di gusto. **L'errore di memoria di un giocatore è
materiale narrativo**: il PNG che si ricorda male, il nome storpiato che diventa un
soprannome, il patto che il tavolo crede di aver stretto e che nessuno ha stretto. Una
trascrizione fedele non li registra: **li cancella**, perché sostituisce il ricordo
con il verbale.

Due conseguenze, e le scrivo qui perché la proposta del §3 non nasca già sbagliata:

1. **La trascrizione serve al DM, non ai giocatori.** Alimenta il verbale, che
   alimenta `state_apply.py`. **Non** si consegna al tavolo come sostituto degli
   appunti: chi vuole prendere appunti continua a prenderli, ed è un bene che lo
   faccia.
2. Il verbale guadagna un campo che oggi non ha — **«cosa hanno capito male»**. Non è
   un errore da correggere: è la lista dei ganci regalati. Va scritta a mano dal DM,
   perché è l'unica riga che una macchina non può ricavare dall'audio: richiede di
   sapere cosa **era** vero.

Lo stesso commento fa un'osservazione più generale che il repo farebbe bene a tenere:
*«più gadget aggiungo, più pressione metto su di me e il gioco diventa meno divertente
per tutti»*. È il §6 di questo documento detto da un altro.

---

## §3-bis · La seconda idea che paga — l'ancora storica per le immagini

Viene dal thread r/dndai, ed è l'unica cosa **non commerciale** in mezzo a una fila di
lanci di prodotto: un commento consiglia di studiare **pittori medievali e
pre-rinascimentali** come riferimento, notando che *«alcuni stili fiamminghi e
veneziani starebbero benissimo»* per generazioni fantasy.

Sembra un consiglio di gusto. È invece la risposta a un problema **tecnico e legale**
che il repo ha già scritto nero su bianco nel capitolato del booklet: *«la coerenza fra
dieci illustrazioni generate resta il punto debole di qualsiasi pipeline automatica»*.

- ADR-0005 e la skill di stile vietano di nominare un **illustratore vivente** o di
  usare tavole altrui come reference. Giusto, e resta.
- Ma una **scuola pittorica in pubblico dominio da secoli** non è la firma di nessuno:
  è una **categoria storica**. `flemish panel painting`, `venetian cinquecento`,
  `northern renaissance oil glazing`, `egg tempera, gold-leaf ground` si possono
  chiedere senza toccare il diritto di nessuno.
- E funziona meglio di un elenco di aggettivi perché **fissa insieme** palette, resa
  della luce, trattamento di mani e volti e profondità di campo: sono un pacchetto
  storico, non scelte indipendenti. È il sostituto economico dell'art director che
  qui non c'è.

⚠️ **Con una cautela che vale specificamente per il Drappo**: la scuola si sceglie per
la *resa*, non per il *luogo*. Ancorare a «pittura senese» — che sarebbe la scelta
ovvia — rimetterebbe dalla finestra l'associazione che `IP-E-LICENZE.md` §4 sta
togliendo dalla porta.

**Applicato subito** (costo: due paragrafi, nessun codice):

- `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md` — nuova
  sezione «L'ancora che invece si può usare: la scuola storica», con il confine fra
  *tecnica del periodo* (lecita) e *opera specifica* (no);
- `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` §1 — il blocco d'ancoraggio per la
  serie di Tarsilia, con la cautela su Siena.

---

## §3-ter · La pila libera per arrivare al livello di stampa — verificata

Domanda del DM: *«c'è codice MIT o open source integrabile per elevare i moduli al
livello Paizo/WotC? Per esempio un generatore di immagini open source di qualità
professionale, automatizzabile? Blender?»*. Sì, e la pila esiste quasi tutta. Ma il
pezzo che sposta di più **non è l'immagine**.

| Strumento | Licenza (verificata) | A cosa serve **qui** |
|---|---|---|
| **Typst** | **Apache 2.0** | ⭐ **il più alto rapporto valore/costo.** Chiude da solo [2] tipografia, [4] PDF unico con segnalibri e metà di [6] frontespizio |
| **ComfyUI** | GPL-3.0, **API locale con coda asincrona** | già nel repo (`scripts/comfyui-local/`). Manca solo lo script che lo pilota |
| **SDXL** (pesi) | **OpenRAIL++-M** — commerciale ammesso | default per i ritratti: ControlNet e LoRA più maturi, gira su 8 GB |
| **FLUX.1 [schnell]** (pesi) | **Apache 2.0** | la licenza più libera: se serve testo dentro l'immagine o la massima garanzia |
| **FLUX.1 [dev]** (pesi) | ❌ **BFL Non-Commercial v2.0** | esclude anche l'uso *«indirettamente connesso ad attività commerciali»*. **Da non usare** su materiale che potrebbe essere pubblicato |
| **Blender** | GPL | non per i ritratti: per la **geometria**. Vedi sotto |
| **Krita** + `krita-ai-diffusion` | GPL | ritocco e inpainting, parlando con lo stesso ComfyUI |
| **Scribus** | GPL | DTP vero con CMYK e PDF/X — ma GUI-first, scripting fragile: **scartato in favore di Typst** |

### La cosa meno ovvia: il divario più grosso è tipografico, non pittorico

Oggi la catena è `markdown → HTML → Chromium → un PDF A4 per capitolo`. **Chromium
impagina pagine web, non libri**: non controlla vedove e orfane, non fa crenatura
fine, non produce un indice cliccabile degno, e i font restano quelli di sistema.
Nessuna quantità di CSS lo trasforma in InDesign.

**Typst** (Apache 2.0) fa quello che serve: CLI `typst compile`, font embedded via
`--font-path`, linguaggio di impaginazione scriptabile, PDF singolo con segnalibri.
La forma giusta **non è sostituire** `build_booklet_html.py` — l'HTML e il sorgente
Homebrewery restano per lo schermo — ma affiancargli un **secondo binario, quello
dell'edizione da stampa**. È la separazione che usa qualsiasi editore: una versione
per leggere, una per il torchio.

### E Blender? Sì, ma non per disegnare

Blender non serve a fare ritratti — lì un generatore fa meglio e costa meno. Serve a
una cosa che **nessun generatore sa fare**, ed è precisamente ciò che distingue un AP
pubblicato: **far combaciare l'illustrazione con la mappa**. In un modulo Paizo la
tavola della locanda e la pianta della locanda sono la stessa stanza; qui oggi sono
due cose scollegate.

La catena è tutta libera: geometria dal JSON della mappa → **Blender in headless**
(`blender -b -P script.py`, API Python completa) → render del **passo di profondità**
→ **ControlNet depth** in ComfyUI → l'illustrazione ha la pianta esatta della Ruota,
con le curve dove sono davvero.

⚠️ È il pezzo **più costoso** dell'elenco, e ha senso **solo dopo** Typst e lo script
di generazione. Un uso minore dello stesso strumento costa molto meno e rende quasi
altrettanto: la **stessa luce d'ambiente** su tutti e sei i ritratti, che è metà del
problema di coerenza.

### L'ordine consigliato

1. **Typst** — nessuna GPU, licenza Apache, chiude tre divari su sei;
2. **lo script di batch su ComfyUI** — piccolo, stdlib-only (urllib + json), rende la
   serie **riproducibile** invece che irripetibile, con seed fissi e righe di
   `PROVENIENZA.txt` scritte dalla macchina;
3. **Blender → depth → ControlNet** — il salto vero, e il più caro.

**Quello che nessuno dei tre risolve** resta scritto: la **direzione artistica**.
L'ancora storica (§3-bis), il seed fisso e la luce condivisa sono tre stampelle
buone; un art director è un'altra cosa.

---

## §4 · Quello che ho verificato e scartato

| Tool | Licenza verificata | Verdetto |
|---|---|---|
| **whisper.cpp** | **MIT**, offline, CPU-only | ✅ unico candidato all'import (§3) |
| **Kanka** | **non è open source**: sorgente pubblico ma con **Commons Clause** sopra (Owlchester SNC) — vietato «vendere» il software, inclusi hosting e supporto a pagamento | ❌ come codice da importare. Utilizzabile come servizio esterno, ma duplicherebbe il canone: due fonti di verità, e quella fuori dal repo non ha gate |
| **Notion · World Anvil · Saga20 · GM Assistant · Tabletop Arc · Archivist · CharGen** | SaaS proprietari, da 9 a 27 USD/mese | ❌ non importabili per costruzione |
| **Syrinscape · Tabletop Audio** | licenza per traccia / termini proprietari | ❌ come asset. Vedi §2.3 |
| **Inkarnate · Dungeondraft · Dungeon Alchemist** | asset proprietari | ❌ già sulla lista nera del capitolato del booklet |
| **Improved Initiative · Fight Club · DM's Toolbox** | varie, alcune libere | ❌ **fuori perimetro**: sono app da usare *durante* la partita; il repo produce documenti |
| **game-icons.net · Watabou · font OFL** | CC BY 3.0 · permissivi · OFL | ✅ **già dentro**, con attribuzione in `CREDITS.md` |

### I cinque nomi emersi solo nella seconda passata

| Tool | Cos'è, verificato | Verdetto |
|---|---|---|
| **Lost Atlas** | **motore di ricerca** su 5.000+ mappe tattiche gratuite di autori terzi (Angela Maps, Tehox, Morvold Press…). Non produce niente: indicizza | 🟡 **ottimo per il tavolo di casa, inutile qui.** Due ragioni, e la seconda conta più della prima: (a) è un **aggregatore**, quindi la licenza è quella del singolo autore, diversa mappa per mappa — «gratis da usare in partita» non è «ridistribuibile dentro un modulo»; (b) le mappe del repo **non sono immagini**: sono un contratto JSON da cui escono muri, porte e luci per l'esportazione UVTT, e sono vincolate alle tattiche scritte nel testo. Una mappa trovata è bella e non sa dov'è la botola del fienile |
| **Shieldmaiden** | tracker di combattimento web, core gratuito, 5e sotto OGL. Cita **Delapouite, Lorc e Skoll** nei crediti: sono gli autori di **game-icons.net**, la stessa fonte CC BY 3.0 già usata per gli stemmi | ❌ come tool (**fuori perimetro**: si usa durante la partita) — ✅ **come conferma di due scelte del repo**, vedi sotto |
| **Owlbear Rodeo** | VTT leggero, agnostico rispetto al sistema, gratis nell'uso base | 🟡 **da citare, non da importare**: gli SVG del repo si trascinano dentro come immagini e il modulo diventa giocabile online senza toccare niente. Una riga nel README delle mappe, quando serve |
| **Tokenstamp 2** | ritaglia un'immagine dentro un bordo circolare da token | 🟡 utile **solo dopo** che esisteranno i ritratti raster (Lotto 6). Oggi non c'è niente da ritagliare |
| **Pocketbard · Donjon · Fantasy Name Generator** | libreria sonora mobile · generatori (donjon oggi con componenti AI) · liste di nomi | ❌ i nomi di Tarsilia sono **scritti**, non estratti: è la scelta che rende il modulo IP-clean. E il suono resta descritto (§2.3) |

**Su Shieldmaiden vale la pena fermarsi**, perché il post chiama la sua funzione di
**auto-bilanciamento** *«fondamentale»* — potere rifare i conti di un incontro **a
metà sessione** quando si vede che sta diventando un TPK o una passeggiata.

Quella funzione qui esiste già, **su carta**: sono le tabelle di scalabilità 4/5/6/7
giocatori di `06-VILLAIN-E-AGENDE.md`, calcolate in anticipo proprio perché al tavolo
non ci sia niente da calcolare. La differenza è che l'app fa i conti dal vivo e il
modulo li ha **già fatti**: per un modulo stampato la seconda è la forma giusta.

Resta però confermato che **D5 della ricerca precedente non era un capriccio**: un
budget incontri PF1e come script (`suggest_encounter.py` fa la matematica 3.5) è la
versione riusabile della cosa che un DM su quindici app ha giudicato decisiva.

---

## §5 · E il mini-modulo? — una modifica sola, e conta

Dopo la seconda passata la risposta cambia in un punto: **l'ancora storica del §3-bis
è già applicata** a `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`. È l'unica cosa dei
due thread che tocca il Drappo, ed è anche la più economica: due paragrafi che
rendono i sei ritratti una serie invece di sei immagini scollegate.

Per il resto **non cambia niente**, e non per pigrizia:

- i **suoni** sono già nella forma portabile (§2.3);
- la **continuità fra le serate** ha già `STATO-DEL-MODULO.md`, che è di carta e sta in
  una pagina: per tre serate un tracker in abbonamento sarebbe sovradimensionato;
- la **trascrizione** del §3 è pensata per la campagna lunga. Su tre serate il verbale
  non serve: il modulo finisce prima che la memoria diventi un problema;
- le **mappe** non si cercano su un motore di ricerca perché non sono immagini (§4);
- il **bilanciamento** è già precalcolato sulle tabelle 4/5/6/7 (§4).

Quello che al Drappo manca davvero resta quello già misurato nel capitolato
(`PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`): **immagini raster**, tipografia
embedded, mappa in versione giocatore, PDF unico. Nessuno dei quindici tool testati da
altri lo risolve al posto nostro — ma il §3-bis rende migliore il primo dei quattro.

---

## §6 · Il criterio, per la prossima volta

Da questa ricerca esce una regola riusabile, e vale la pena scriverla:

> **Un tool esterno entra nel repo solo se supera tre soglie**: la licenza permette
> l'uso *e* la ridistribuzione di ciò che produce; funziona **offline** o degrada
> in modo pulito; e sostituisce un attrito **misurato**, non uno immaginato.

Le prime due si verificano in dieci minuti. La terza è quella che scarta quasi tutto:
il repo non ha un problema di funzionalità mancanti, ha un problema di **arte**, e
l'arte non si risolve abbonandosi a un tracker di campagna.

E una quarta soglia, che la seconda passata ha aggiunto e che nessuna licenza copre:

> **Un tool che automatizza una cosa che il tavolo faceva a mano va guardato due
> volte**, perché quella cosa fatta a mano poteva produrre qualcosa che
> l'automazione non produce. Gli appunti sbagliati dei giocatori sono il caso
> esemplare (§3.1): il tool li elimina *e* elimina i ganci che contenevano.
