# Perché la legenda funzionale è fatta così

> Forma: **spiegazione** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)). Il principio da cui nasce la legenda e la storia misurata della divergenza fra SVG e UVTT; la specifica dei campi e dei simboli sta nel riferimento. Nato il 2026-11-10 dalle sezioni di spiegazione di [LEGENDA-FUNZIONALE-SPEC](../reference/LEGENDA-FUNZIONALE-SPEC.md). Le sezioni tengono il numero che avevano lì, così un rimando scritto prima («LEGENDA-FUNZIONALE-SPEC §N») resta vero: nella guida, al posto della sezione, c'è un rimando a questo file.

---

## 1. Il principio: la geometria è neutra, i numeri no

Un simbolo porta **due informazioni indipendenti**, e la confusione fra le due
è la causa di tutti i difetti misurati:

| | Cos'è | Dove vive | Cambia con il sistema? |
|---|---|---|---|
| **Render** | come si disegna (pattern, colore, prop) | `legend.yaml` → `render` | **no** |
| **Funzione** | cosa fa nello spazio (blocca? copre? a che quota?) | `legend.yaml` → `function` | **no** |
| **Numeri di gioco** | +4 CA · 20% · ×2 movimento · CD 15 | `rules/<sistema>.yaml` | **sì** |

**La regola**: `legend.yaml` non contiene **nessun numero di gioco**. Una roccia
«dà copertura parziale» — che poi valga +4 CA in 3.5, +4 CA in PF1e o +2 CA in 5e
è affare del profilo. È ciò che permette di supportare tre sistemi senza tre
legende, e ciò che tiene i vincoli OGL confinati a un file solo ([LEGENDA-FUNZIONALE-SPEC §5](../reference/LEGENDA-FUNZIONALE-SPEC.md#5-confini-di-licenza--cosa-può-essere-venduto)).

---

## 6. La divergenza SVG↔UVTT, rimisurata il 2026-09-04

Il renderer e l'esportatore UVTT non concordano su cosa sia un muro. La regola
d'arbitrato resta quella di luglio — **una cella occupata da roccia, edificio,
torre o statua è impenetrabile e opaca** — ma lo stato del codice è cambiato.

`WALL_SYMS` in `export_uvtt.py` contiene oggi **otto** simboli: `🏰 ⬛ ⛺ ⛰ 🟪 🗼 🏛 🗿` — `⛺` aggiunto con ADR-0042, `⛰` con ADR-0043, entrambi il 2026-09-04.

| Simbolo | Etichetta nel renderer | UVTT | Verdetto |
|---|---|---|---|
| `🗿` `🗼` `🏛` | Statua · Torre · Edificio/tempio | **è muro** | ✅ **già a posto** — la correzione prevista a luglio risulta applicata |
| `⛰` | Montagne / creste rocciose | **è muro** *(dal 2026-09-04)* | ✅ **chiuso** — vedi §6.1 |
| `⬛` | **Edificio** (muratura piena) | è muro | ✅ **risolto** — vedi §6.2 |
| `⛺` | **Tenda** | è muro *(dal 2026-09-04)* | ✅ risolto insieme a `⬛` |
| `🔳` | **Dais / pedana** | **non** è muro, ed è giusto | ✅ glifo nuovo |
| `🪨` | Rocce/macerie (copertura +4 CA, terreno difficile) | non è muro | ✅ corretto: è copertura **parziale**, non totale |

### 6.1 · `⛰` — ✅ CHIUSO il 2026-09-04

**2.423 celle in 21 file.** Il renderer disegnava la montagna come solida —
ombra, contorno, riempimento roccioso, e il suo pattern è dentro `HEAVY_PATS` —
e l'export UVTT non ci metteva un muro. In Foundry un personaggio **attraversava
la catena montuosa e ci vedeva attraverso**.

Era il bug che questa spec esiste per chiudere, ed è rimasto aperto **sei
settimane** con la riga di codice da cambiare già scritta qui dentro. Il DM lo ha
messo in cima alla coda il 2026-09-04; è chiuso da
[ADR-0043](../../plans/adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md).

**Quanto era grosso**, misurato sull'export prima e dopo:

| Mappa | celle `⛰` | segmenti prima | dopo |
|---|---:|---:|---:|
| `Hammerfist-L1-REVISED-Ultra-Clear` | 338 | 8 | **20** |
| `Hammerfist-L2-REVISED-Ultra-Clear` | 808 | 44 | **66** |
| `Hammerfist-Lotto-1-Ricognizione` map02 | 179 | 4 | **14** |
| `hammerfist-L2-assedio` | 1.800 | 50 | **54** |

⚠️ L'ultima riga va letta bene: 1.800 celle e **+4** segmenti soli, perché lì la
montagna è un bordo compatto e la fusione greedy la riduce a poche corse lunghe.
Il numero di segmenti misura la **geometria**, non quanta roccia c'è.

`🪨` resta **fuori** dai muri, ed è corretto: è copertura **parziale** (+4 CA,
terreno difficile), non totale.

⚠️ **Il rovescio, e va detto.** Il muro è binario e la montagna non lo è: un
valico, una sella, un sentiero fra due creste sono attraversabili nella finzione
e adesso sono muro nell'export. Chi disegna un passo deve usare un simbolo di
terreno per il passo, **non** `⛰`. Prima si passava ovunque, adesso non si passa
da nessuna parte: è il meno sbagliato dei due, non il giusto.

### 6.1-bis · Il punto cieco di `validate_maps`, trovato scrivendo la Fase 0

`validate_maps` rendeva **solo i markdown con almeno un SVG committato**. Il
rovescio, che nessuno aveva guardato: **cancella tutti gli SVG di un master e
quel master sparisce dal controllo** — CI verde, e nessuno guarda più quelle
mappe.

Non è ipotetico: è quello che fa la **PR #63**, che cancella i sette SVG dei tre
master `Hammerfist-Lotto-*` deprecati **tenendo i master**, che generano ancora
sette mappe. *«validate_maps verde»* nel corpo di quella PR è vero e significa
*«nessuno guarda più»*.

Chiuso dallo stesso ADR-0043: un master che genera mappe e non ha **nessun** SVG
è un errore, salvo che si dichiari nel proprio testo con
`<!-- validate_maps: non-renderizzato — motivo -->`. Il marcatore sta nel master
e non in una lista altrove, per la stessa ragione di ADR-0041: una lista in un
altro file si stacca dalla realtà.

🔎 **Il gate ha trovato subito due casi già in `main`**: `…P1B-Cerchio-Treant`
e `…P1C-Rituale-COMPLETO-SCALE`, quattro mappe in tutto, mai renderizzate.
Adesso ci sono — **31 SVG / 17 master**, erano 27 e 15.

⚠️ Renderizzandole è emerso un difetto di **contenuto** in `…P1C` mappa 3:
l'intestazione dichiara 40×40 e le celle lette sono 26×29. Il renderer avvisa e
disegna lo stesso. **Non corretto**: la griglia è contenuto, e ridisegnarla è una
decisione del DM.

### 6.2 · `⬛` — ✅ RISOLTO il 2026-09-04: tre glifi per tre cose

**8.216 celle in 24 file**, ed era il simbolo più usato dei tre. L'etichetta del
renderer diceva *«Struttura (tenda, edificio, dais)»*: **tre cose diverse sotto
un simbolo solo**, e l'export le trattava tutte da muro pieno.

**Il difetto era peggiore di così, e la spec di luglio non l'aveva visto**: la
legenda conteneva **già** `⛺ Tenda` e `🏛 Edificio / tempio`. `⬛` non era solo
sovraccarico — **duplicava due glifi che esistevano**. E `⛺` non era in
`WALL_SYMS`: le tende disegnate col glifo giusto **non bloccavano nemmeno la
vista**, mentre quelle disegnate col glifo sbagliato bloccavano tutto. Le due
direzioni dell'errore si annullavano solo per caso.

**Decisione DM del 2026-09-04** (*«fai 3 glifi separati, altrimenti non si
capisce niente»*), formalizzata in
[ADR-0042](../../plans/adr/ADR-0042-tre-glifi-per-tre-cose.md):

| Glifo | Significato | Vista | Movimento | Muro UVTT |
|---|---|---|---|---|
| `⬛` | **Edificio / corpo di fabbrica** — muratura piena | blocca | blocca | **sì** *(invariato)* |
| `⛺` | **Tenda** — telo teso: si taglia, si abbatte, brucia | blocca | blocca finché sta in piedi | **sì** *(era «no»: è il fix)* |
| `🔳` | **Dais / pedana rialzata** — ci si sale sopra | **no** | **no** | **no**, è quota |

`🔳` è nuovo e non compariva da nessuna parte nel repo: nessuna collisione.

⚠️ **`⬛` non cambia comportamento**, ed è la scelta che rende la decisione
applicabile subito: nessuna delle 8.216 celle esistenti si muove sotto i piedi
di nessuno, nessuna geometria di SVG cambia. L'unica differenza negli artefatti
è **la riga di legenda stampata dentro l'SVG** — 17 SVG rigenerati, 66 righe,
tutte di legenda.

Il glifo generico tiene il significato **strutturalmente più forte**, non quello
statisticamente più comune: se avessimo dato a `⬛` il senso di «tenda» (il
gruppo più numeroso nei conteggi) avremmo cambiato in un colpo solo ogni mappa
di città e di fortezza già disegnata.

#### La coda: quali celle vanno riclassificate

Le 8.216 celle restano `⬛`. **Non si riscrivono in blocco**: sapere quali sono
tende, quali edifici e quali dais vuol dire leggere la mappa, non contare i
caratteri. La coda si smaltisce quando quella mappa viene toccata per altri
motivi.

📌 **Aggiornamento 2026-09-05.** La coda viva è di **6.960** celle in **23** file:
le 1.256 di `Hammerfist-Lotto-3-FINALE` sono uscite quando il master è stato
archiviato (D1). Il conteggio di 8.216 resta corretto **come misura del
2026-09-04** e non si riscrive: era vero allora.

| File | Celle `⬛` | Sospetto, da verificare leggendo |
|---|---:|---|
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | 2.173 | accampamento → quasi tutte **tende** ⛺ |
| ~~`Hammerfist-Lotto-3-FINALE.md`~~ | ~~1.256~~ | 🗄 **archiviato** il 2026-09-05 in `08_…/Mappe/_ARCHIVIO/` (decisione D1): fuori dalla coda, il master definitivo è `Hammerfist-L3-REVISED-Ultra-Clear` |
| `ARC07-MAPPE-DEFINITIVO.md` | 800 | forgia → edifici **+ l'Altare**: il candidato **dais** 🔳 più probabile del repo (e ha già 93 celle `⛺`) |
| `ARC07-DEF-5-RITORNO-HAMMERFIST.md` | 684 | fortezza → **edifici** |
| `tarsilia-la-ruota-giocatori.md` | 642 | città → **edifici** |
| `tarsilia-la-ruota.md` | 641 | città → **edifici** |
| `Portale-Forgia-L2-REVISED-UltraClear.md` | 539 | forgia → **edifici** |
| `Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO-maps.md` | 519 | da leggere |
| `scripts/examples/campo-drow-1.md` | 382 | accampamento → **tende** ⛺ |
| `Portale-Forgia-L1-REVISED-UltraClear.md` | 240 | forgia → **edifici** |
| altri 14 file | < 100 ciascuno | — |

⚠️ *«Dominata da un significato»* non è *«composta da»*: nel campo drow ci sono
anche un palizzato e una tenda di comando, e un `sed` non li distingue.

⚠️ **Nessun gate distingue un uso corretto da uno pigro.** Un agente può
continuare a mettere `⬛` ovunque e la CI resta verde. Il controllo qui è la
legenda e chi la legge — al contrario di ADR-0041, dove l'invariante era
contabile. `scripts/tests/test_legenda_glifi.py` verifica che i tre glifi
restino **distinti** e che `⬛` **non cambi comportamento**: due proprietà
misurabili, non la correttezza dell'uso.

### 6.3 · Cosa cambia negli artefatti

**Nessun SVG cambia.** Modo di rendering e funzione sono campi ortogonali: una
statua continua a disegnarsi come prop illustrato e *contemporaneamente* a
dichiararsi opaca. L'unico artefatto che cambia è l'export UVTT delle mappe con
`⛰` — ed era esattamente il bug, ora chiuso (§6.1).

✅ **Per `⬛` il timore si è rivelato infondato**, e vale la pena dire perché.
Temevo che togliere tenda e dais dal significato cambiasse **gli SVG** di quelle
celle. Non succede, perché la decisione lascia a `⬛` la semantica che aveva: le
celle già disegnate restano edifici e si disegnano identiche. Cambia solo la
**riga di legenda** dentro l'SVG — 17 file, 66 righe, zero geometria. Il costo
vero non è nel rendering: è nella **coda di riclassificazione** (§6.2), che è
lavoro di lettura e non di sostituzione.
