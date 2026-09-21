# PIANO — La misura editoriale si porta agli standard del mestiere

> **Cos'è**: portare le misure di qualità del repo dalla forma che hanno oggi
> — conteggi di congegni, senza pesi e senza soglia — alla forma che l'editoria
> professionale usa da decenni: **tipologia d'errore con severità pesata,
> soglia dichiarata prima, campionamento, accordo fra valutatori**.
>
> **Stato**: 🟡 **in corso** (2026-09-19 · F1.1 + F1.2 + F1.3 + F1.4 + F2.1 + F2.2 + F2.5 + F2.6 + F3.1 + F3.2 chiusi il 2026-09-21) · **Decisore**: DM
> **Gate del piano**: `python3 scripts/punteggio_mqm.py --soglia` esce 0 su
> tutti i master DEF, e il κ misurato fra i due campioni è ≥ 0,6

---

## 0 · Perché, in una riga

`misura_craft.py` risponde alla domanda «questo congegno c'è?». È utile e ha
già trovato difetti veri, ma è una metrica **che mi sono inventato**: non ha
pesi, non ha una soglia di accettazione, e il suo metro d'oro l'ha scritto un
solo valutatore. Il mestiere ha risposto a questo problema prima di noi.

---

## 1 · Cosa misura davvero l'editoria — la ricerca, con le fonti

### 1.1 · MQM e ISO 5060 — la tipologia con severità

**MQM** (Multidimensional Quality Metrics) è in uso industriale da dieci anni.
Due componenti: una **tipologia d'errore** gerarchica (Accuracy, Fluency,
Terminology, Style, Locale, Non-translation) e un **modello di punteggio**.
A ogni errore si assegna una **severità definita dall'impatto sul lettore**,
con moltiplicatori canonici **minore 1 · maggiore 5 · critico 25**.

Dal febbraio 2024 la stessa impostazione è **norma ISO** — `ISO 5060:2024`,
*Evaluation of translation output* — e la sua definizione di errore è quella
che serve qui: **«mancato rispetto delle specifiche di progetto»**. Non
«brutto»: *difforme da ciò che era stato dichiarato*. È esattamente il
problema del repo — una skill dichiara una norma, un documento non ce l'ha.

MQM è dichiarato applicabile a output **umano, automatico e generato da IA**:
non stiamo forzando uno strumento fuori dal suo dominio.

### 1.2 · La soglia si dichiara prima

Il punteggio MQM si ottiene dalle penalità normalizzate sul conteggio di
riferimento. Esempio tipico del framework: una tolleranza di **10 errori
minori oppure 2 maggiori per 1.000 parole** dà un punteggio di 99. Il pass/fail
ha **due** condizioni, e la prima è assoluta:

> **nessun errore critico** **E** punteggio ≥ soglia.

### 1.3 · Campionamento, non censimento

`ISO 2859-1` (AQL) per la regola generale. Nella pratica LQA si campiona —
tipicamente il 10% — e si riserva la revisione totale a ciò che è ad alto
rischio. Il monito che riguarda noi da vicino: *evitare di essere falsamente
rassicurati da pochi esempi puliti*.

### 1.4 · L'accordo fra valutatori

Krippendorff α / Cohen κ. Per un giudice LLM il bersaglio dichiarato in
letteratura è **κ 0,7–0,8** (il soffitto umano-umano); **sotto 0,6 la metrica
è dominata dal rumore del giudice**, non dal segnale. È il pilastro di cui il
repo oggi non ha *niente*.

### 1.5 · Paizo / Dungeon — e una regola che il repo non aveva scritto

Le linee guida ufficiali di *Dungeon* prescrivono due cose verificabili sul
read-aloud:

1. il testo **non fa riferimento a chi guarda**;
2. si evitano *«vedi»*, *«appena entri nella stanza»* e **qualunque frase che
   presupponga un'azione del giocatore**.

🔴 ~~**Misurato sul repo, oggi**: su **1.334** box read-aloud, **229 — il 17% —**
presuppongono un'azione del giocatore. Per arco: 143 ARC-07, 53 ARC-09,
22 ARC-08, 11 ARC-06.~~ **Cifre corrette il 2026-09-20, vedi sotto.** Resta
vero il resto: questa norma **non era scritta da nessuna parte** in `skills/`,
e nessuno strumento la guardava.

> 🔴 **CORREZIONE (2026-09-20).** Il conteggio di sopra usava un criterio di
> «box» scritto per questa ricerca invece di riusare `box_read_aloud`, che è il
> rilevatore che il repo **già possiede**. Rimisurato con quello:
>
> | | Box totali | Con la violazione | % |
> |---|---|---|---|
> | pubblicato il 2026-09-19 | 1.334 | **229** | 17% |
> | col rilevatore vero | 626 | **131** | 21% |
> | al netto di archivi dichiarati, prompt d'immagine e `DEPRECATO` | **540** | **104** | **19%** |
>
> Il **denominatore era più del doppio** di quello vero. La percentuale regge
> — anzi peggiora di due punti — ma il numero assoluto che il DM ha visto era
> il doppio del lavoro reale. Dettaglio in
> [PIANO-QUATTRO-ORDINI](PIANO-QUATTRO-ORDINI-2026-09-20.md) §1.2.

⚠️ **E non tutte e 104 sono errori dello stesso tipo.** Una parte sono visioni
d'artefatto — la Corona che parla al suo portatore — dove la seconda persona è
la scelta giusta: lì la norma non si applica perché quello è **dialogo**, non
narrazione. È il motivo per cui questa classe nasce **minore**, con il
perimetro dichiarato, e non maggiore.

---

## 2 · Assunzioni dichiarate, e cosa manca

1. **La tipologia non si importa, si mappa.** Le sette dimensioni MQM
   contengono *Locale* e *Non-translation*, che qui non esistono. Portarsele
   dietro vuote farebbe sembrare il sistema più rigoroso di quanto è — lo
   stesso difetto della quarta colonna vuota. Si mappano le **44 norme già
   registrate** in `skills/REGISTRO-NORME-EDITORIALI.md`, non altro.
2. **La soglia nasce dal repo, non da un manuale.** Vedi §4: una soglia
   importata boccerebbe lavoro buono.
3. **Il punteggio non giudica la bellezza.** Misura la *conformità alle
   specifiche dichiarate* (ISO 5060). Un documento a punteggio pieno può
   essere noioso; nessuna metrica di questa famiglia lo vede, e va detto
   invece che lasciato credere.
4. **Il campione umano costa tempo al DM.** Se quel tempo non c'è, il piano
   si ferma alla FASE 2 e il κ resta non misurato — il che va **scritto**,
   non aggirato con un secondo modello che finge di essere un secondo parere.

---

## 3 · Il modello di punteggio

### 3.1 · Le severità

| Severità | Peso | Cos'è qui | Esempi dal repo |
|---|---:|---|---|
| **critico** | **25** | rende il documento ingiocabile, o **viola il canone** (regola 8 di `AGENTS.md`) | statblocco inventato · contraddizione con `state.md` · EL oltre APL+4 senza `Boost log:` |
| **maggiore** | **5** | viola una norma **prescrittiva** registrata | box oltre le 12 righe · forma del dialogo fuori da `editorial-standards.md` §2 · read-aloud assente dove `module-standard` §6 lo impone |
| **minore** | **1** | un congegno **assente dove sarebbe servito**, o una prassi disattesa | nessun `[HDYWTDT]` ai punti di morte di un boss · più di un nome proprio nuovo in un box · la regola Paizo di §1.5 |

🔎 **Il critico è pass/fail assoluto.** Un solo critico boccia il documento
qualunque sia il punteggio, ed è la differenza più importante rispetto a
`misura_craft` di oggi, dove tutto pesa uguale.

### 3.2 · La formula

```
penalità = Σ (conteggio_errori × peso_severità)
punteggio = 100 × (1 − penalità / righe_di_riferimento × 1000 / 1000)
```

Normalizzato **per 1.000 righe**, non in percentuale su un totale arbitrario:
un master DEF da 1.300 righe e un handout da 40 non si confrontano altrimenti.

---

## 4 · Le soglie — calibrate sul repo, non importate

Questo è il punto che il DM ha posto esplicitamente: **una soglia ragionevole,
che non butti via niente**.

🔎 **Perché importare una soglia è sbagliato, con la prova.** Ho calcolato
**Gulpease** (l'indice tarato sull'italiano) su tutto il repo:

| | mediana | sotto 40 | fuori scala (>100) | nella fascia «professionale» 80-89 |
|---|---:|---:|---:|---:|
| ~~read-aloud (1.334 box)~~ | ~~67,1~~ | ~~3~~ | ~~77 = 6%~~ | ~~102 = 8%~~ |
| **read-aloud, rimisurato (475 box)** | **70,1** | **1** | **70 = 15%** | **53 = 11%** |
| documenti del repo (53) | **65,4** | 0 | 0 | 21% |

> 🔎 **Rimisurato il 2026-09-20 sul set vero dei box** (stessa correzione di
> §1.5: si riusa `box_read_aloud` invece di un criterio proprio). **La
> conclusione non cambia, e su un punto si rafforza**: i box *fuori scala* —
> quelli in cui la prosa spezzata prescritta fa esplodere la formula — passano
> dal 6% al **15%**, due volte e mezzo. L'argomento «Gulpease non è tarato su
> questo genere di testo» regge meglio sui numeri veri che su quelli vecchi.

La fascia «testo professionale per pubblico generale» è **80-89**. Se
importassimo quella soglia, **boccheremmo l'89% dei read-aloud del repo** —
compresi quelli scritti meglio. E ci sono due ragioni per cui sarebbe una
sciocchezza:

- un read-aloud **non è** un foglio informativo: la prosa spezzata che
  `read-aloud-adulti.md` *prescrive* fa esplodere la formula, e infatti il
  **15%** dei box esce dalla scala 0-100;
- Gulpease **non discrimina** qui: 70,1 contro 65,4 fra due prose che il repo
  governa con norme **opposte** (ADR-0035). Come voto è cieco.

> **Regola di calibrazione**: la soglia iniziale è il **valore che il repo ha
> già oggi**, arrotondato in basso. Il cancello **nasce verde** e non butta
> niente; da lì si stringe per gradi, e ogni stretta porta la sua ragione
> scritta (ADR-0036: si misura il miglioramento, non lo stato).

| Classe di documento | Soglia iniziale | Come si ottiene | Quando si stringe |
|---|---|---|---|
| **master DEF** | il P25 attuale della classe | misurato in F1.4 | quando il 75% supera la soglia successiva |
| **file d'arco non-DEF** | P10 attuale | idem | idem |
| **handout / player-facing** | P25 attuale **+ zero critici** | idem | mai sul critico: quello è già assoluto |
| **documenti del repo** | solo critici | la prosa-documenti ha norme diverse | — |

⚠️ **Gulpease resta, ma declassato**: non è un voto, è un **guard rail** sull'unico
box sotto 40. Entra come **minore**, e solo quando il box è fuori dalla fascia
*e* non è prosa spezzata (>100 non conta).

---

## FASE 1 — Audit / accertamento

| | Lotto | Cosa produce | Come si verifica |
|---|---|---|---|
| ✅ | **F1.1** Mappare le norme del registro su tipologia × severità | una colonna nuova in `REGISTRO-NORME-EDITORIALI.md` | `validate_norme_editoriali.py` estende il controllo: ogni norma ha una severità o una ragione scritta per non averla |
| ✅ | **F1.2** Separare rilevabile da giudizio | quante hanno uno strumento e quante no — **derivato, non scritto** | conteggio nel registro, e un gate che lo confronta con le righe vere |
| ✅ | **F1.3** Potere discriminante di ogni congegno | `misura_craft --discriminante`: per ciascuno, quante coppie di bersagli separa | 🔴 un congegno che **non separa mai** due documenti è rumore e si toglie — è il controllo *non-discriminating* della skill-creator |

> ### 🔎 Cosa hanno trovato F1.1-F1.3, il 2026-09-21
>
> **Le norme non erano 44 e non erano 34: sono 39**, e i tre numeri diversi
> che circolavano erano tutti scritti a mano. Il piano diceva 44, il registro
> ne dichiarava *«16+9+12+3»* (cioè 40) in tabella e *«undici su
> trentaquattro»* nel paragrafo sotto, e il riepilogo del cancello ne stampava
> **47** perché contava le **emoji in tutto il file**, prosa compresa. Dal
> lotto F1.2 il conto lo deriva `validate_norme_editoriali.py` dalle righe, e
> un numero scritto a mano che non combacia fa rossa la CI.
>
> **F1.1 — la severità, e una tabella incrociata che le due colonne separate
> non potevano dare.** Delle 39 norme: **1 critica**, 15 maggiori, 20 minori,
> 3 senza peso con la ragione accanto. Incrociando severità e copertura:
>
> * **l'unico critico è l'unico completamente scoperto.** `EL ≤ APL+4` è la
>   norma più cara del registro ed è 🔴, perché il suo controllo esiste ma non
>   ha superficie. La severità più alta e la copertura più bassa cadono sulla
>   stessa riga;
> * le **maggiori** stanno meglio delle minori — 9 su 15 misurate contro 9 su
>   20 — e non per caso: una norma prescrittiva ha una forma, e una forma si
>   cerca;
> * 🔴 **ma il punteggio di ADR-0059 pesa il bordo, non il centro**: delle
>   quattro norme che ci entrano, **tre sono minori**. Il punteggio di oggi è
>   quasi tutto penalità da 1 punto, e questo spiega perché la classe `arco`
>   ha P10, P25, P50 e P75 tutti a **100,00** — non è che i documenti siano
>   perfetti, è che quel che li separerebbe non è pesato.
>
> ⚠️ **Un candidato al critico non promosso, e perché.** *«Ogni fatto
> raggiungibile da ≥2 nodi diversi»* è la causa documentata di un caso che
> muore in un vicolo cieco, quindi somiglia molto a un critico. È rimasta
> **maggiore** perché **nessuno la misura**, e un pass/fail assoluto appeso a
> un rilevatore inesistente è un pass/fail su niente.
>
> **F1.3 — la previsione del piano non ha retto, ed è un esito.** Il lotto era
> aperto sull'ipotesi che qualche congegno fosse rumore da togliere. Misurato:
> **zero congegni su 23 non separano nessuna coppia**; il più debole — «ADR
> interni al documento» — ne separa **11 su 66**, e le separa tutte perché un
> solo bersaglio su dodici ce l'ha. La tabella di `misura_craft` non ha righe
> da buttare.
>
> 🔎 **E la misura ha avuto bisogno di due colonne, non una.** Il conteggio
> grezzo separa anche solo perché ARC-08 ha 6.096 righe e DEF-5 ne ha 516:
> qualunque congegno frequente li distingue, per la ragione sbagliata. La
> densità per 1.000 righe toglie la taglia di mezzo, ed è la colonna su cui si
> decide. Un congegno costante in densità — presente ovunque nella stessa
> misura — è informativo quanto uno assente ovunque, cioè per niente: i test
> provano proprio questo caso, che è il meno ovvio dei due.
| ✅ | **F1.4** Distribuzione attuale per classe | P10/P25/P50/P75 del punteggio su tutto il repo | è l'input delle soglie di §4: **prima si misura, poi si sceglie** |
| ✅ | **F1.5** Estrarre i due campioni | `campioni_kappa.py --estrai` → **20 + 20, disgiunti** (sovrapposizione 0), stratificati per classe con almeno un documento per classe, **seme fisso 20260921** | `campaign/misure/campioni-kappa.json` |

> ### 🔴 F3.3 — il κ è **0,0**, e non perché i giudici siano in disaccordo
>
> Il campione **B** è stato giudicato il 2026-09-21 (giudice: il modello di
> questa sessione, **bias dichiarato**: ha scritto metà dei rilevatori, quindi
> il suo κ è un **limite superiore ottimistico**). Il risultato:
>
> ```
> n=20   Po=0,95   Pe=0,95   κ = 0,0   («lieve», sotto la soglia 0,60)
> ```
>
> **I due giudici concordano nel 95% dei casi — e concorderebbero nel 95% dei
> casi tirando i dadi.** L'accordo osservato è identico a quello atteso per
> caso, quindi porta **zero informazione**. È esattamente il difetto che il κ
> esiste per rendere visibile, e che la percentuale grezza avrebbe nascosto:
> «95% d'accordo» sarebbe sembrato un ottimo risultato.
>
> **La causa non è il giudice: è la soglia.** La macchina ha promosso **20 su
> 20**. Il documento che il giudice ha bocciato —
> `06_…/CoronaDiAdamantio/maps.md`, una griglia ASCII disallineata con la
> legenda in inglese (*Wall*, *Throne*, *Hidden Portal*) e senza intestazione —
> prende **100,0**. Non perché sia buono: perché **nessuna delle 12 norme
> pesate lo tocca**. Non ha box read-aloud, quindi non ha difetti nei box; non
> ha prosa, quindi non ha calchi. Un documento che non contiene niente di
> misurabile è, per questa metrica, perfetto.
>
> #### Cosa ne consegue, in ordine
>
> 1. 🔴 **La metrica NON è validata**, e lo dice la regola che il piano si è
>    dato: sotto κ 0,60 si dichiara non affidabile. `punteggio_mqm --soglia`
>    resta in CI come **cancello d'osservazione** — utile a prendere una
>    regressione — ma il suo verde **non è un giudizio di qualità**.
> 2. ⚠️ **Il campione A, oggi, darebbe κ ≈ 0 qualunque cosa voti il DM.** Se
>    la macchina promuove tutto, nessun insieme di voti può produrre accordo
>    informativo. Chiedere al DM le sue venti valutazioni *adesso* gli
>    costerebbe tempo per un numero già noto.
> 3. ✅ **Ma la scheda A resta utile per un'altra domanda**, e vale la pena
>    dirla: non «la metrica è affidabile?» ma **«cosa deve imparare a vedere?»**.
>    I documenti che il DM boccia e la macchina promuove sono l'elenco esatto
>    delle norme che mancano al punteggio.
> 4. 🔵 **Il passo che sblocca il κ non è un giudice migliore: è una norma che
>    morda su un documento vuoto.** Il candidato naturale è il controllo di
>    conformità 3.5/PF1e, che sarebbe il primo `critico` della catena — oggi il
>    pass/fail è cablato e non scatta mai.
>
> 🔎 **E questo lotto ha fatto il suo mestiere.** F3.3 era scritto come *«κ ≥
> 0,6 o la metrica si dichiara non affidabile»*: il criterio è stato applicato
> alla lettera e la risposta è no. Un lotto di validazione che non può dire di
> no non è una validazione.

## FASE 2 — Sviluppo

| | Lotto | Cosa produce |
|---|---|---|
| ✅ | **F2.1** `scripts/punteggio_mqm.py` | legge il registro, applica severità e pesi, stampa punteggio + dettaglio errori per documento; `--json` per la CI |
| ✅ | **F2.2** `specifiche-qualita.yaml` | le soglie per classe, **fuori dal codice**: è una decisione di prodotto e deve poterla cambiare il DM senza toccare Python |
| ✅ | **F2.7** *(nuovo, ordine DM 2026-09-21)* **Richiamare i rilevatori che esistono e nessuno chiamava** | da **4 norme pesate a 11**, e da **1 maggiore a 3**. Nessun rilevatore nuovo: `validate_prosa` misurava sei di quelle norme da settembre, e mancava il **nome** — `controlla()` restituiva stringhe già formattate. Ora `rilievi()` emette record `(chiave, messaggio)` e `controlla()` ne è la proiezione, **identica byte per byte** su tutto il repo |
| ✅ | **F2.8** *(nuovo, ordine DM 2026-09-21)* **I due rilevatori che mancavano davvero** | `--metrature` (ADR-0014 §2, **28 box su 477**, 1 falso positivo su 28 contato a mano) **entra nel punteggio**; `--costrutto-italiano` (`italiano-nativo.md` §8, **281 su 477**) **misura e non pesa**, perché la dislocazione a sinistra è rilevata a metà e una norma positiva rilevata a metà produce penalità false |
| ✅ | **F2.9** *(nuovo, ordine DM 2026-09-21)* **La superficie delle norme scoperte** | `superficie_norme.py` + [ADR-0062](adr/ADR-0062-una-norma-senza-superficie-lo-dichiara.md): per ognuna delle **9** norme che nessuno misura, **manca il codice o manca il dato?** Misurato: per **otto su nove non manca il codice**. Quattro stati — superficie vuota (2) · convenzione assente (4) · oggetto assente (1) · fuori dominio (2) — e un gate in CI che boccia una riga che ha smesso di dire il vero |
| ✅ | **F3.4** Stabilità | ✅ **misurata, non dichiarata**: `test_tutti_i_rilevatori.py` esegue **ogni** rilevatore due volte e il punteggio di un documento **tre**, su un campione deterministico — **460 sotto-prove**. Più le due proprietà che nessuno verifica mai: nessun rilevatore restituisce un `set` (l'ordine di iterazione non è garantito, e romperebbe ogni confronto prima/dopo) e **nessuno tocca il disco mentre misura**, provato con un'impronta SHA-256 prima e dopo |
| ⬜ | **F2.3** Il rilevatore della regola Paizo | la norma di §1.5, con l'esenzione «visione d'artefatto» dichiarata nel registro |
| ⬜ | **F2.4** Gulpease come guard rail | `--leggibilita`, severità minore, esente sopra 100 |
| ✅ | **F2.5** `ADR-0059` | la decisione: *il punteggio di qualità è MQM adattato, e la soglia nasce dal repo*. Numero **ancora libero e riservato a questo piano**: nel frattempo sono stati scritti ADR-0060 e ADR-0061, che hanno saltato il 0059 apposta |
| ✅ | **F2.6** Gate in CI | `punteggio_mqm.py --soglia` fra i cancelli, **non bloccante alla prima messa in opera** — un giro di osservazione, poi bloccante |

## FASE 3 — Validazione

| | Lotto | Criterio di superamento |
|---|---|---|
| ✅ | **F3.1** Il cancello morde, per ogni severità | un critico iniettato → **rosso anche con punteggio alto**; un maggiore iniettato → punteggio scende di 5 volte un minore; rimosso → verde |
| ✅ | **F3.2** Nessun documento buono bocciato | alla soglia iniziale, **zero** master DEF in rosso. Se ne cade uno, la soglia è sbagliata, non il documento |
| 🟡 | **F3.3** κ sui due campioni | **ESEGUITO sul campione B il 2026-09-21: κ = 0,0.** La metrica **si dichiara non affidabile**, come la regola prescrive. ⚠️ La causa non è il giudice — Po e Pe sono **entrambi 0,95** — ma la soglia, che promuove 20 su 20. Il campione **A resta da votare**, e il suo valore oggi non è il κ ma **l'elenco di cosa la metrica non vede**: `campioni_kappa.py --scheda A` |
| ⬜ | **F3.5** Non-regressione | `misura_craft` continua a girare: il punteggio **affianca**, non sostituisce |

---

## 5 · I due campioni, e perché sono diversi

Il DM ha scelto **due campioni distinti** invece di un doppio passaggio sullo
stesso. È la scelta giusta e vale la pena dire perché: due valutatori sullo
*stesso* campione misurano l'accordo ma non la copertura; due campioni
disgiunti misurano **anche** se la metrica regge su materiale diverso.

| | Campione A | Campione B |
|---|---|---|
| **chi valuta** | il DM | un secondo modello, **diverso** da quello che produce il punteggio |
| **dimensione** | 20 documenti | 20 documenti |
| **estrazione** | stratificata per classe e per arco, seme fisso | idem, **disgiunto da A** |
| **cosa misura** | l'accordo fra la macchina e chi decide | la tenuta su materiale che il DM non ha visto |
| **cosa NON misura** | 🔴 niente sulla bellezza: solo conformità | 🔴 l'accordo fra due macchine **non è** un secondo parere umano |

⚠️ **Il κ che conta è quello del campione A.** Se il campione B dà κ alto e A
basso, la metrica è coerente con sé stessa e in disaccordo col DM — e in quel
caso ha torto la metrica.

---

## 6 · Cosa questo piano NON copre

- **L'impaginazione.** La ricerca sul lato editoriale/grafico è la tappa
  successiva e ha standard suoi, tutti misurabili e già individuati:
  `PDF/UA — ISO 14289` con i **136 checkpoint verificabili** del Matterhorn
  Protocol e il validatore **veraPDF**; `PDF/X — ISO 15930` per la stampa;
  e le misure tipografiche (45-75 caratteri per riga su colonna singola,
  40-50 su due colonne; interlinea 1,4-1,6 per il testo corrente). Diventerà
  un piano gemello.
- **La qualità narrativa.** Nessuna metrica di questa famiglia sa se una scena
  è bella. Restano il collaudo al tavolo (`rumblingstone-playtest`) e il
  giudizio del DM.

---

## 7 · Decisioni aperte

| | Decisione | Perché serve il DM |
|---|---|---|
| 🔵 | **Le soglie iniziali** (§4) | F1.4 le propone dalla distribuzione, ma «quanto stringiamo» è prodotto, non tecnica |
| 🔵 | **Il tempo del campione A** | 20 documenti da annotare. Senza, il κ non esiste e va dichiarato |
| 🔵 | **La regola Paizo: 104 box** *(era «229», cifra corretta in §1.5)* | si correggono, si esentano per classe, o si lascia il rilevatore solo come avviso? |

---

## Fonti

[MQM Council](https://www.themqm.org/) ·
[MQM scoring models](https://www.themqm.org/mqm-pillars/the-mqm-scoring-models/) ·
[ISO 5060:2024](https://www.iso.org/standard/80701.html) ·
[ISO 2859-1 / AQL](https://blog.ansi.org/ansi/iso-2859-1-2026-aql-sampling/) ·
[LQA: campionamento vs revisione totale](https://www.acclaro.com/blog/do-you-still-need-language-quality-assurance-a-practical-guide-for-localization-teams/) ·
[Agreement metrics per LLM-as-judge](https://www.alphaxiv.org/abs/2606.00093) ·
[Dungeon writers' guidelines](https://paizo.com/writersguidelines/dungeon_writer_guidelines.pdf) ·
[PDF/UA — ISO 14289](https://pdfa.org/resource/iso-14289-pdfua/) ·
[PDF/X — ISO 15930](https://pdfa.org/resource/iso-15930-pdfx/) ·
[Indice Gulpease](https://it.wikipedia.org/wiki/Indice_Gulpease)

---

## 8 · 🔎 Cosa ha trovato l'attuazione, il 2026-09-21

Il piano prevedeva che F1.4 producesse dei numeri. Ne ha prodotti, e ha anche
trovato **tre difetti nello strumento che li produceva**, tutti della stessa
famiglia che questo repo insegue da una settimana.

| | Difetto | Come è venuto fuori |
|---|---|---|
| 🔴 | **Le prime soglie erano inventate** — «P25 99,7», «P10 97,8» — scritte nel YAML **prima** di eseguire F1.4. I valori veri sono P25 **97,90** e P10 **100,00** | eseguendo il comando che le avrebbe dovute produrre |
| 🔴 | Il classificatore usava `Path.match`, che confronta solo la **coda** del percorso: **294 documenti su 515** finivano «fuori classe», cioè senza soglia, cioè non bocciabili | la prima esecuzione di `--distribuzione` |
| 🟡 | La regola «soglia = P10» **non si applica alla classe `arco`**: la distribuzione è così schiacciata sul 100 che il P10 *è* 100, e usarlo boccerebbe la coda — l'opposto dell'istruzione del DM | guardando la tabella |

E la domanda del DM sul rilevatore dei critici — *«ci sono le regole 3.5 e PF1e
come skill, non si possono usare per farlo in maniera deterministica?»* — ha
una risposta misurata: **uno dei tre casi sì, e non ha superficie**.

`validate_modules.py --tetto-el` esiste, legge l'APL da `state.md` (13),
calcola il tetto (17) e cerca gli incontri che lo sforano. Trova **zero
incontri marcati**, perché la forma che `AGENTS.md` prescrive — `**EL**: [N]` —
ha **zero occorrenze** nel repo, mentre i 150 «EL N» nudi mescolano
dichiarazioni (*«Boss Fight - EL 14»*) e menzioni (*«Standard Treasure for
EL 16»*). Allargare la regex darebbe un numero, e sarebbe finto.

> **Quindi il controllo dice che non ha superficie, invece di dire zero.**
> Marcare gli incontri è un lotto nuovo; il giorno in cui è fatto, questa
> norma si accende da sola e diventa il **primo critico vero** del punteggio.
