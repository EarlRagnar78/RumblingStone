# PIANO — Riconciliazione delle PR aperte e dei piani

> **Stato**: 🟡 **in corso** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«controlla le vecchie PR se sono ancora
> valide e se sono state superate […] fai la riconciliazione di PR e piani»*, poi
> *«#109 analizza le modifiche […] se le modifiche sono valide fammi le domande
> per risolvere i dubbi e aggiorna il main»*.

## Perché questo piano esiste

Sette PR erano aperte senza che nessuno le avesse più guardate. La più vecchia,
la #72, stava in bozza dal 26 luglio e conteneva **tre piani commerciali e due
ADR** che a settembre sono stati riscritti da zero da chi non l'aveva letta.
Il costo non è stato il lavoro doppio: è stato che **due dei suoi ADR erano
migliori** di quello che è stato riscritto al posto loro.

Il rimedio in `PIANO-VENDIBILITA` §8.4 — *prima di aprire un piano, si guardano
le PR aperte* — è una regola, e una regola senza gate si stacca dalla realtà.
Questo piano è il lavoro di rientro: portare su `main` ciò che nelle PR aperte è
**valido e non superato**, un pezzo alla volta e con la fonte dichiarata.

Il criterio di giudizio è uno solo, e non è l'età della PR:

> Una PR è **superata** se il suo contenuto è stato riscritto altrove, meglio o
> uguale. È **abbandonata** se nessuno l'ha ripresa, ma il contenuto è ancora
> l'unico che quel problema abbia. Le abbandonate **non si chiudono per far
> scendere un contatore**: si svuotano portando fuori quello che vale.

---

## Lotto R1 — la correzione del Peso del Mondo `[✅ fatto]`

**Fonte**: PR #99, correzione DM del 2026-08-06, mai arrivata su `main`.

`main` diceva che al rito dello Smeraldo il **Peso del Mondo** l'aveva accettato
**Tordek**. Il DM ha stabilito il 6 agosto che era **Thorik**, il portatore della
Corona — e la #99 lo aveva scritto, ma è rimasta bozza. Per un mese il canone
pubblicato ha attribuito a un PG un pegno permanente di un altro.

⚠️ Il DM ha riconfermato la correzione il 2026-09-04 prima che partisse.

Non era uno scambio di nomi. La #99 stabilisce la regola, e questo lotto la
segue: *un'eco registra **una scelta**; se cambia la mano che ha scelto, l'eco o
si riscrive da zero o si annulla. Gli ID non si riusano.*

- [x] `campaign/state.md`: riga di riepilogo, riga di Tordek, riga di Thorik,
      riga della **Corona**, ed **E-07c riscritta** da zero
- [x] `campaign/state.md`: **E-07e annullata** (`✖ annullata`) e **E-07f** nuova —
      la presenza verde al rito era Hella, e Thorik non lo sa
- [x] `ARC07-DEF-1` §9: blocco «CANONE GIOCATO» riscritto, con la nota di
      correzione che dice cosa diceva prima e perché
- [x] `ARC07-DEF-2` §7-bis «Le Quattro Ore Rubate»: le **mani fredde sotto la
      trave** tornano a Thorik; la notte di Tordek scende a **una scena sola**
- [x] Booklet della sessione Terros e del ritorno alla Forgia (`.hb.md` + `.html`
      rigenerati dal manifest), `00-INTRO-DOVE-SIAMO.md`
- [x] Scheda giocatore della Corona + versione DM (`02_Corona_2_Gemme_DM.html`):
      «il bilancio di Thorik» non dice più che *ha guardato Tordek pagare*
- [x] Scheda Bracieri di Tordek: l'avvertenza sommava un **−2 DES che non è suo**
- [x] `plans/PIANO-INCANTATORI-MEMORABILI-…`: il −2 DES passa alla riga di Thorik
- [x] `plans/PIANO-DM-TOOLKIT-HYPE-…` e `plans/CHANGELOG.md`: **non corretti**,
      annotati. Sono log storici: dicono cosa fu deciso allora, ed è vero

**Portato dentro anche il ritrovamento del 2026-08-09**, perché è un fatto del
modulo giocato e non una decisione nuova: `PortaleForgia-P1-REVISED-Corretta.md`
elenca fra le **Limitazioni** della Corona indossata un **−2 DES**, con il
ricalcolo scritto (*DES 10 → 8, CA 22 → 21, CAR 8 → 12*). Quel blocco non era
mai stato riportato in nessuna scheda successiva: tutte elencavano solo i bonus.
Sommato al pegno del rito, Thorik è a **DES 6**.

> ⚠️ **Due cose restano da decidere dal DM** (`INF-007` nella #99), perché sono
> nel testo di P1 e nessuno le ha né confermate né revocate: il **+4 CAR** e la
> clausola che la Corona **non sia rimovibile** finché mancano gemme. Il +4 CAR
> è a favore del giocatore, la non-rimovibilità è un vincolo di trama. Se
> valgono, valgono entrambi. Segnate sulla scheda, non applicate d'ufficio.

---

## Lotto R2 — l'instradamento delle skill `[✅ fatto]`

**Fonte**: PR #109 (rilievo), decisione DM 2026-09-04 *«Obbligo, e con un gate
che lo verifica»*.

`AGENTS.md` §Skills apriva dicendo che *gli agenti scoprono le skill da soli* —
falso — ed elencava **13** skill a fronte di **18** directory con un `SKILL.md`.
Le cinque mancanti (`editoria`, `edizione`, `indagine`, `module-standard`,
`prosa-documenti`) sono tutte nate dopo l'ultima riscrittura della sezione.
Nessuna era stata rimossa: nessuna era mai stata aggiunta.

- [x] [ADR-0041](adr/ADR-0041-instradamento-delle-skill-con-un-gate.md):
      il principio prima degli esempi, e il gate bidirezionale
- [x] `AGENTS.md` §Skills riscritta: **principio** (chi legge, in che forma esce)
      → **tabella per compito** → **inventario completo** delle 18
- [x] `scripts/validate_skills.py`: quarto controllo **bloccante**, nelle due
      direzioni (skill orfana · puntatore morto)
- [x] `scripts/tests/test_skills_routing.py`: 5 test, di cui **tre che provano
      che il gate morde** — senza quelli, il test sul repo reale passerebbe
      anche con un gate vuoto

**Non fatto, e dichiarato**: i banner «Caricami quando» in testa a ciascun
`SKILL.md`. Sarebbero 18 file toccati per duplicare quello che il frontmatter
`description:` già dice agli agenti che lo leggono. Il difetto misurato era
l'**omissione nell'instradamento**, e quello lo chiude il gate.

---

## Lotto R3 — la legenda funzionale `[✅ recuperata, ⬜ non risolta]`

**Fonte**: PR #72, `docs/guides/LEGENDA-FUNZIONALE-SPEC.md`.

Il documento è stato recuperato e **ri-verificato sui numeri di oggi**, non
ricopiato: parte dei difetti che elencava sono già stati chiusi, e ne è emerso
uno nuovo che nella #72 non c'era.

| Simbolo | Stato oggi |
|---|---|
| 🗿 🗼 🏛 | ✅ già corretti dopo la #72 |
| ⛰ «Montagne / creste rocciose» | ⬜ **2.415 celle in 16 file** — ancora aperto |
| ⬛ «Struttura (tenda, edificio, dais)» | 🔴 **8.205 celle in 21 file** — **nuovo**: simbolo sovraccarico, tre significati diversi sotto un glifo |
| 🪨 | ✅ correttamente **non** un muro (copertura parziale) |

⚠️ ⬛ **non si chiude con una riga in `WALL_SYMS`.** Un dais non è un muro, una
tenda lo è a metà, un edificio lo è. Serve una **decisione di legenda** — cioè
tre glifi invece di uno — e cambierebbe gli SVG, non solo l'export. È una
domanda per il DM, non un fix.

---

## Lotto R9 — il censimento rifatto, e la PR che mancava `[✅ fatto]`

`[G giudizio · Opus 5, sessione principale · alto · **ogni PR che `list_pull_requests --state open` restituisce ha una riga di verdetto**]`

**Fonte**: richiesta DM del 2026-09-05 — *«vedi se ci sono PR e piani aperti e
me li elenchi, così vediamo cosa è rimasto, cosa è superato e cosa c'è da fare
sul serio; non vorrei piani e PR che si sovrappongono o parzialmente obsolete
che per sbaglio mergio»*.

Rifatto il conto sulle PR effettivamente aperte oggi, invece di ricopiarlo da
R5: sono **cinque**, e una — la **#67** — non ha mai avuto un giudizio. R5 ne
elencava cinque, ma erano #109, #99, #106, #63, #52: la #67 non compare in
nessuna riga di questo piano, né in `INDEX`, né in `CHANGELOG`, né in
`STATO-E-ORDINE`.

⚠️ **Perché è sfuggita, e perché è il caso peggiore.** Le altre si notano: 88
file, o un branch di mesi fa, o un conflitto. La #67 aggiunge **un file solo**,
non tocca nessun `.md`, non ha conflitti — quindi in una lista di PR è la riga
che l'occhio salta, ed è l'unica che si potrebbe mergiare senza leggerla. Il
giudizio è nella sezione qui sotto: **superata, e contraria alla norma di oggi**.

Verificato anche il resto del perimetro: **zero issue aperte** sul repo, e le
quattro PR abbandonate sono ferme dove le aveva lasciate R5 (nessun commit
nuovo dopo il 2026-08-15).

### Che cosa ha insegnato su ADR-0045

R5 era **l'esempio di classe G** che sta nella tabella di
[ADR-0045](adr/ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md)
(*«giudicare cinque PR»*). Girava sull'engine giusto, all'effort giusto, e ha
soddisfatto il suo criterio di qualità — *«il DM lo legge e riconosce il proprio
problema»* — **restando incompleto**. Non è un errore di esecuzione: è che quel
criterio, per come è scritto, **non può accorgersi di un'assenza**. Si legge una
lista di cinque verdetti, ci si riconosce dentro, e non si sa che manca il sesto.

Il rimedio non è un criterio più severo per **G**: è togliere al giudizio la
parte che non è giudizio. Da qui la **quarta regola** di ADR-0045 — *un lotto che
lavora su un insieme dichiara da dove conta l'insieme* — e la dichiarazione in
testa a questo lotto, che nomina il comando invece di promettere attenzione.

⚠️ **La classificazione dei 19 lotti di `PIANO-RIPRESA-PR-ABBANDONATE` non
cambia.** Il difetto era nel lotto che *decide* se una PR si continua o si
butta, non in quelli che poi la svuotano.

---

## Giudizio nel merito delle PR aperte

Ogni riga è **verificata sul codice di oggi**, non letta dal corpo della PR.

### #109 — instradamento delle skill · **superata, chiusa**

Aveva ragione sulla diagnosi e ha rinunciato a metà del rimedio: *«nessun gate
in CI, un gate semantico che indovina sarebbe peggio del problema»*. La premessa
era sbagliata — il gate non deve indovinare se hai **caricato** la skill giusta,
deve contare se è **instradata**, e quello è verificabile a macchina. Il DM ha
rovesciato la rinuncia; il contenuto è nel lotto R2. Il difetto che la #109 non
aveva misurato è l'**incompletezza** dell'elenco: 13 voci su 18.

### #99 — audit globale su tre assi · **abbandonata, non superata** · la più grossa

88 file, +14.078 / −4.931. **Non è un audit**: è un cambio di architettura dei
dati di campagna, cresciuto dentro una PR nata read-only. Il corpo lo ammette
(*«la riga originale non vale più»*).

| Cosa porta | Perché conta |
|---|---|
| **ADR-0017** — `state.yaml` come sorgente dei fatti, `state.md` **generato** | `state.md` era **1677 righe di cui 1150 (68%) di changelog**. Lo storico esce in `state-changelog.md` e il file scende a 546 righe |
| Il vincolo che chiude alla radice il difetto dei «due tempi» | `oggi` e `tempo` **obbligatori** nello schema: un fatto senza tempo dichiarato **non è esprimibile** |
| **4 validatori nuovi** (`validate_docs/links/pg/state`) + `render_state --check` | `validate_docs` nasce perché `AGENTS.md` documentava `campaign/npcs/`, `locations/`, `encounters/`: **nessuna delle tre è mai esistita** <!-- validate-docs: ignore --> |
| Schede PG a dati (`PG/schede/*.yaml` + `.md` generati) | oggi le schede PG non esistono come dato da nessuna parte |
| **ADR-0018** — `groups/<slug>/` invece di branch-per-gruppo | e il **no a un memory store** per gli agenti: sarebbe non versionato e divergente |
| Il reset per gruppo nuovo **perdeva** | azzerava `state.md` e `sessions/` e lasciava `state.yaml`, `state-changelog.md`, `campaign-history.md` e i recap al gruppo successivo |
| La correzione del Peso | ✅ già portata fuori nel lotto R1 |

⚠️ **Da non fare in blocco.** È il pezzo che tocca la parte più delicata del
repo (il canone come dato), e va valutato **a lotti** — G1, G2, G2-bis,
G2-ter, G2-quater sono già separati nel corpo della PR. Ordine consigliato:
`validate_docs` per primo (indipendente, chiude un difetto reale), poi ADR-0017.

⚠️ **La sua misura più utile, e va guardata in faccia**: *«la pipeline che
avrebbe prevenuto questi difetti è costruita, ha 31 test, è al ~98% — e non è
mai stata accesa.»*

### #106 — catena dei raster + Blender · **abbandonata, non superata** · e risponde alla domanda sull'AI

`comfyui_batch.py` (567 righe, 216 di test) e `render_map_blender.py` (381 +
346 nello script Blender, 202 di test). **Nessuno dei due esiste su `main`.**

Misurata contro la pratica corrente dell'illustrazione digitale AI-aided, questa
PR fa **cinque cose su sei**:

| Requisito | #106 |
|---|---|
| **Riproducibilità**: prompt, seed, modello e risoluzione fissati fuori dal codice | ✅ annotazione in **commento HTML** sopra il blocco di prompt nel markdown — invisibile nel rendering; il prompt si corregge **nel documento**, mai nello script |
| **Determinismo prima della scelta** | ✅ il seed è **derivato dall'`id` con SHA-256**, non sorteggiato: due macchine partono dalle stesse diciotto immagini. `--reroll N` cambia tentativo in modo altrettanto ripetibile |
| **Provenienza scritta** | ✅ `PROVENIENZA.txt` con file · modello e versione · **licenza dei pesi** · seed · data · chi. Il file nasce **prima** delle immagini |
| **Igiene di licenza sui pesi** | ✅ **exit 1 come codice, non come avvertimento**, se il checkpoint contiene `flux1-dev` e varianti — e *prima* di qualsiasi scrittura o chiamata di rete (ADR-0019: la licenza è dei pesi, non del software) |
| **Condizionamento da geometria reale, non da prompt** | ✅ `--profondita`: il pass Z di Blender alimenta ControlNet depth, e la **stessa `paint()`** che genera l'SVG risolve la geometria — le due catene **non possono** divergere. Con i due passi scritti nel codice perché non li salti: **normalizza** e **inverti** (saltare l'inversione dà un'immagine che *sembra* giusta e guida il modello al contrario) |
| **Il giudizio umano nel ciclo** | ⚠️ **il pezzo che manca**: `--fissa-seed` registra la scelta, ma non c'è nessun registro di *cosa è stato scartato e perché*. `rumblingstone-art-direction` dice che **un'immagine si butta** invece di tenerla perché «è già venuta»; qui non c'è dove scriverlo |

Due dettagli che valgono più del resto perché sono **decisioni, non codice**:
il conteggio del capitolato è diventato un **gate** (*«il capitolato dice
diciotto, i prompt sono venti»* → CI rossa al diciannovesimo: non è un divieto,
è un modo di obbligare a **decidere**), e `batch_size` è fisso a 1 sui 6 GiB di
VRAM misurati.

⚠️ **I diciotto raster non ci sono**: questo ambiente non ha GPU. Il collo di
bottiglia è **il giudizio, non la GPU** — ~1,5-2 ore sulla macchina del DM.

### #63 — le 17 griglie Ultra-Clear di Hammerfist · **abbandonata, non superata**

**Verificato su `main` oggi**: i tre master `Hammerfist-L{1,2,3}-REVISED-Ultra-
Clear.md` esistono ma hanno **un `map01` ciascuno** — cioè **3 mappe tattiche su
17**, esattamente lo stato che la PR descriveva come *prima*. La **3Y Ponte
Sospeso** non ha alcuna griglia in tutto il repo: compare solo nell'atlante e nel
Lotto-3 **deprecato**.

**Verificato che non è marcita.** Nonostante **222 commit** di distanza dalla sua
base e un rifacimento del renderer nel mezzo (*«renderer mappe a fedeltà
piena»*), i cinque SVG del master L3 rigenerati con lo script di oggi sono
**byte-identici** a quelli committati nella PR. Le griglie sono compilate da
contratto JSON, non scritte a mano, e la determinatezza ha retto.

⚠️ **Il problema che introduce, e non è nel corpo della PR.** Cancella **tutti e
sette** gli SVG dei tre master `Hammerfist-Lotto-*` deprecati, ma **tiene i
master** (ci aggiunge solo un banner). Verificato: quei master **generano ancora
7 mappe**. E `validate_maps` **non se ne accorge** — rende solo i markdown che
hanno già almeno un SVG committato, quindi togliendoli **tutti** il master
sparisce dal controllo. *«validate_maps verde»* qui non significa che le mappe
deprecate siano ancora rigenerabili: significa che **nessuno le guarda più**. È
la stessa classe di difetto delle liste di incantesimi — l'assenza che nessun
test cerca.

**Rimedio, piccolo**: o si tengono i 7 SVG, o `validate_maps` guadagna un
controllo per il master che genera mappe e ha **zero** SVG committati senza
essere su una lista KO dichiarata.

### #52 — overlay professionale sulle mappe degli incendi drow · **abbandonata, non superata**

**Verificato su `main` oggi**: nessuna direttiva `@compass/@path/@zone/@mark` nel
`Cerchio Sacro della Foresta` né nel supplemento dei campi drow, e la scena
**«Foresta in Fiamme» non esiste**. I 14 master che oggi usano le direttive sono
altri.

Il suo valore non è il disegno: è la **dimostrazione** che le direttive `@` di
[ADR-0006](adr/ADR-0006-annotazioni-mappa-overlay-professionale.md) funzionano
anche sui master **scritti a mano**, non solo su quelli generati da JSON — e
in-place, senza ricostruire la griglia (nessuna perdita del disegno esistente).

**Verificato che regge**: rigenerati oggi, due dei tre SVG sono **byte-identici**
a quelli della PR. Il terzo **cambia solo di nome**, non di contenuto:
`…grid-6553-scal.svg` → `…grid-65-53-sca.svg`. È la `slug` corretta dal **lotto A
di PIANO-QUALITA-DEL-CODICE**, che aveva trovato sette implementazioni diverse e
**tutte e sette** incollavano `65×53` in `6553`. Quindi il costo di riprenderla
è **una rinominazione**, non un rifacimento.

### #67 — booklet HTML degli hint per Terros · **superata, da chiudere**

⚠️ **Questa PR il giudizio del 2026-09-04 non l'aveva vista.** R5 dice «cinque PR
aperte»: erano **sei**. La #67 è sfuggita perché è la più innocua da guardare —
un file aggiunto, nessun conflitto, nessun `.md` toccato — ed è esattamente il
profilo che si mergia per sbaglio.

Aggiunge `07_il Portale Della Forgia Eterna/ARC07-BOOKLET-HINT-TERROS.html`:
428 righe, un booklet HTML **scritto a mano**, quattro pagine per-PG per la
serata del Guardiano.

**Verificato su `main` oggi.** Lo stesso oggetto esiste, in forma migliore, in
`07_…/homebrew/sessione-terros/`: manifest ADR-0013, intro, regia, master
integrale, teaser, e **quattro** handout per-PG — `02-HINT-THORIK`,
`03-HINT-TORDEK`, `04-HINT-ARTEMIS`, `05-ECHI-HELLA` — con `.hb.md` e `.html`
generati. Il primo di quei file è arrivato il **31 luglio**, sette giorni dopo
la #67, e l'ultimo giro di rigenerazione è del **5 settembre**, con dentro la
correzione R1 del Peso del Mondo.

Non c'è niente da svuotare. Cercati uno per uno, **tutti** i motivi della #67
sono già nel canone: «Radice a Terra», «Sisma Contrario», «Valvola di Sfogo»,
«Trinità Divina», «Scudo di Geodi», la pioggia di stalattiti e il cabochon di
Varis stanno in `ARC07-DEF-1` e in `01-REGIA-SESSIONE`.

**E mergiarla farebbe un danno**, che è la ragione per cui non basta lasciarla
aperta e ignorarla:

| | La #67 | `main` di oggi |
|---|---|---|
| Dove sta | radice dell'arco, fuori da `homebrew/` | dentro la cartella di sessione |
| Come nasce | HTML a mano, CSS proprio | manifest + `build_booklet_html.py` |
| Chi la controlla | nessuno: `validate_booklets` non la vede | il gate ADR-0013 |
| Cosa dice al giocatore | *«fatti Aiutare e vinci una prova di Forza contrapposta»*, *«sei lo star DPS designato»*, la tabella accetta/rifiuta del Seme-Mercato con **l'esito già scritto** | *«qui non ci sono istruzioni: sono cose che il TUO personaggio sente»* |

L'ultima riga è la sola che conta davvero. Gli handout di `main` seguono la
norma che il tavolo si è dato — al giocatore si danno **sensazioni**, non
tattiche, e mai l'esito di una scelta prima che la faccia. La #67 gliele dà
tutte e tre. Non è vecchia: è **contraria alla regola di oggi**, e l'avrebbe
riaperta di soppiatto dentro un file che nessun validatore guarda.

**Azione**: chiudere la #67 con questa motivazione. Nessun contenuto da
recuperare — è il secondo caso, dopo la #109, in cui «superata» vuol dire
davvero superata.

✅ **Fatta il 2026-09-11**, su decisione del DM, insieme a #63 e #52 (il cui
contenuto la ripresa aveva già portato con F1 e F2). La motivazione qui sopra è
stata scritta nel thread della PR, non solo qui: chi la ritrova fra sei mesi
deve poter leggere **perché** è chiusa senza dover cercare il piano.

---

## Cosa resta da decidere al DM

| # | Domanda |
|---|---|
| R6 | Il simbolo **⬛** copre tenda, edificio e dais: **tre glifi o uno?** Non si chiude con una riga in `WALL_SYMS` — cambierebbe gli SVG, non solo l'export |
| R7 | La Corona di Thorik: il **+4 CAR** e la **non-rimovibilità** sono nel testo di P1 e nessuno li ha né confermati né revocati. Se valgono, valgono entrambi |
| R8 | **Ordine di ripresa** delle quattro PR abbandonate. La mia proposta: **#63** (contenuto pronto, costo quasi zero, chiude un buco che si sente al tavolo) → **#52** (una rinominazione) → **#106** (serve la tua GPU per l'ultimo passo) → **#99 a lotti** (la più grossa e la più delicata) |

## Piano di validazione

Ogni lotto chiude solo se passano, **nello stesso commit**:

- `python3 -m pytest scripts/tests/ -q`
- `python3 scripts/validate_skills.py` (ora comprende il gate ADR-0041)
- `python3 scripts/dm.py doctor --ci`
- `python3 scripts/check_plans_discipline.py`
- per R1, in più: **zero** occorrenze residue dell'attribuzione sbagliata fuori
  dai log append-only (`plans/CHANGELOG.md`, `_ARCHIVIO/`), che restano com'erano
  perché sono record storici e non canone vivo
