# PIANO — Le skill di `awesome-llm-apps/agent_skills`: cosa si adotta, cosa si scarta

> **Cos'è**: la valutazione delle otto skill di
> [`Shubhamsaboo/awesome-llm-apps/agent_skills`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills)
> (più la loro cartella `evals/`), fatta contro le diciotto skill del repo, e i
> lotti per adottare il poco che serve. Letto al commit upstream
> `4bf51ab` (2026-09-28).
>
> **Stato**: 🟡 L6, L0, L7 ✅ (2026-10-01); D1-D7 decise il 2026-10-01, i lotti partono in fila · **Decisore**: DM, che sceglie
> quali lotti partono (D1…D7 qui sotto) · **Regola**:
> [ADR-0010](adr/ADR-0010-vendoring-skill-terzi.md), cherry-pick e mai
> collezioni; l'ADR di adozione (ADR-0076) nasce con il primo lotto che porta
> codice nel repo.
> **Gate**: ogni lotto ha il suo, scritto nell'intestazione; nessuna skill
> nuova (G5): tutto entra in skill che esistono già.

---

## 0 · Perché

Il DM, il 2026-09-30, dopo aver guardato `first-reader`: quattro idee valgono
per il lettore e il playtester a freddo. La lettura senza guardare avanti, la
prova di memoria del giorno dopo fatta sul diario, i lettori che restano
disponibili per le domande, e l'«ancora» che confronta una lettura con la
precedente. Il resto della cartella andava letto per decidere se serve.

Il bisogno è misurato nel repo, non supposto:

- il lettore a freddo riceve tutto il modulo insieme, e la rubrica chiede di
  trovare `L-ORDINE` («un'informazione serve prima del punto in cui compare»)
  a un agente che il punto dopo l'ha già letto;
- il quiz a due agenti chiede **ogni volta** una chiave approvata dal DM
  (`plans/quiz/` ne ha una sola, DEF-4), e il passo 7 del ciclo del master è
  fermo su DEF-5, DEF-1, DEF-2 e DEF-3 per questo;
- **D26** di PIANO-LETTORE, decisa il 2026-09-30: il registro delle letture a
  freddo in JSON, con l'impronta del testo letto e un cancello in CI. È «un
  lotto da aprire», e nessuno l'ha aperto.

## 1 · Cosa ho guardato prima, e cosa questo piano non rifà

Regola di apertura (ADR-0044). `grep` su `plans/` per *awesome-llm*,
*agent_skills*, *first-reader*: niente. PR aperte: la #99 e la #106, estranee.
Rami: nessun file con *lettur*, *freddo* o *registro* mai arrivato su `main`
(`plans/contenuti-nei-rami.json`).

**Perché un piano nuovo e non un lotto di PIANO-LETTORE.** I lotti L1-L5 stanno
nel perimetro di PIANO-LETTORE; L6-L8 no (le skill come file, la sicurezza, il
lint delle descrizioni). Tenere insieme la valutazione di una fonte esterna è
quello che ADR-0010 chiede: una fonte, un'attribuzione, un ADR. PIANO-LETTORE
riceve un rimando in F4 e la D26 resta sua: questo piano la esegue.

Non rifà:

- le rubriche di lettore e playtester (`rumblingstone-playtest/references/`):
  le estende con il modo di leggere, non con domande o codici nuovi;
- il quiz a due agenti e `quiz_lettura.py`: restano dove c'è una chiave;
- `copertura_scene.py`: il riconoscimento della scena si riusa dal suo profilo
  in `plans/copertura-scene.json`, non si riscrive;
- il gate delle skill (`validate_skills.py`, ADR-0041 e ADR-0058): si allarga,
  non si affianca a un secondo validatore.

**La quarta rubrica, il DM a freddo.** Il DM la dà come bozza usata sul giro di
DEF-4 e DEF-5 del 30 settembre. Nel repo non c'è: nessun file, nessun ramo,
nessuna PR aperta la contiene, e le cartelle `esperimenti/def5-ciclo/` e
`esperimenti/def4-seconda-serata/` hanno solo letture di lettore e playtester.
Il lotto L5 non la scrive da zero prima che il DM dica dove sta (D2).

## 2 · La licenza, verificata skill per skill

Il repository upstream ha un `LICENSE` Apache 2.0 alla radice e nessun file
`NOTICE`. Il `registry.json` dichiara `Apache-2.0` per sette skill su otto.

| Skill | Licenza dichiarata dalla skill | Autore (storia git) | Esito |
|---|---|---|---|
| `first-reader` | ⚠️ **nessuna**: il frontmatter non ha `license`, il `registry.json` ha `"license": ""`. Solo il README dice «Apache-2.0» in fondo | Shubham Saboo (`c70e7b78`, 2026-09-09); una correzione di Haris Chechi (`36bde77`) | Apache 2.0 per la licenza della radice; nell'ADR si scrive che la skill non la dichiara |
| `advisor-orchestrator-worker` | Apache-2.0 | Shubham Saboo | ok |
| `commit-archaeologist` | Apache-2.0 | Matt Van Horn | ok |
| `dependency-doctor` | Apache-2.0 | Matt Van Horn | ok |
| `project-graveyard` | Apache-2.0 | Shubham Saboo | ok |
| `scope-creep-detector` | Apache-2.0 | Matt Van Horn | ok |
| `thinking-out-loud` | Apache-2.0 | Shubham Saboo | ok |
| `self-improving-agent-skills` | nessuna (non è una skill: app Next.js + backend) | — | scartata comunque |
| `evals/tools/*.py` | il file dice *vendored* da altre due skill mai pubblicate (*skill-builder*, *agent-security-auditor*) | — | Apache 2.0 per la radice; la provenienza a due salti va scritta |

**Cosa chiede Apache 2.0 a chi adatta** (§4): una copia della licenza, un avviso
visibile nei file modificati, le note di copyright e attribuzione conservate.
Nel repo gli script stanno sotto MIT e il testo sotto CC BY-NC-SA
(`LICENSES.md`, ADR-0029). Un file adattato da codice Apache resta Apache 2.0
**per la parte che viene da lì**: `LICENSES.md` guadagna una terza riga con
l'elenco dei file, e il testo della licenza entra in `scripts/LICENSE-APACHE-2.0`. <!-- validate-docs: futuro -->
Le rubriche in italiano prendono **idee** (la lettura a passaggi, il diario, il
ricordo dal diario), che non sono coperte da diritto d'autore: si citano per
correttezza, senza cambiare licenza al testo.

## 3 · La tabella — skill esterna, cosa ha di buono, dove va, cosa si scarta

Letti per intero: gli otto `SKILL.md`, tutti i `references/`, tutti gli script
di `first-reader`, gli script degli altri per le parti citate, `evals/README.md`,
i quattro strumenti di `evals/tools/` e il `ledger.md` di `first-reader`. Del
repo: le diciotto `SKILL.md`, tutti i `references/` delle cinque skill che la
tabella tocca (`playtest`, `module-standard`, `plans`, `prosa-documenti`,
`edizione`), `ORCHESTRAZIONE.md`, `REGISTRO-NORME-EDITORIALI.md`,
PIANO-LETTORE. ⚠️ Dei `references/` delle skill di consultazione (`dnd-35-srd`,
`forgotten-realms-lore`, `pathfinder-1e-srd`) ho letto solo la riga segnalata
dallo scanner (L7): nessuna skill esterna tocca il loro contenuto.

| Skill esterna | Cosa ha di buono, per noi | Dove va | Cosa si scarta, e perché |
|---|---|---|---|
| **`first-reader`** · `feed.py` | Il testo servito **un passaggio alla volta** da un processo su `127.0.0.1`; il passaggio dopo arriva solo dopo una riga di diario (ago da −2 a +2, cosa mi aspettavo, cosa ho trovato), mai prima di un tempo minimo di lettura, e il testo non tocca il disco finché i lettori non hanno finito. Il lettore non ha il percorso del file, ha un indirizzo con un gettone | **L1** → `rumblingstone-playtest` (lettore, playtester) | il taglio a 85 parole: per noi il passaggio è la **scena** (`### SCENA`, o il titolo del profilo in `copertura-scene.json`). Il `state.json` finale che salva i passaggi: da noi salverebbe una copia del master in `plans/`, si salva l'impronta per scena |
| `first-reader` · `recall.py` | La prova di memoria fatta da un agente **nuovo** con il solo diario, su domande fisse (ridire in una frase, cosa è rimasto, il momento più forte, come finisce, dove il pezzo è più vivo, cosa farei ora). Non serve una chiave: si giudica contro l'intenzione dichiarata | **L2** → `quiz-a-due-agenti.md`, passo 7 del ciclo | le domande da lettore di blog. Le nostre sono quelle di un DM: *in tre frasi la serata*, *chi è il cattivo e cosa vuole*, *dove si arriva*, *cosa succede se si fallisce*, *cosa ho dovuto rileggere*. L'intenzione contro cui si giudica c'è già: il riquadro *La serata in tre frasi* e il §0 del master |
| `first-reader` · `ask.py` | Il lettore resta disponibile: la domanda del DM va a un agente nuovo con persona e diario, **mai** il testo; se il diario non basta, risponde «non l'ho annotato» | **L2** → rubriche del lettore e del playtester | la regola «mai proporre riscritture» resta, ed è già la nostra («non propone riscritture») |
| `first-reader` · «again», `manifest.json`, `previous_run` | Una lettura nuova, stessi ruoli, menti nuove, e il confronto con la precedente scena per scena | **L4** → il registro D26 | `room.py` e la pagina HTML con la striscia dell'attenzione: nel repo il rapporto è markdown in `plans/esperimenti/`, e una pagina da pubblicare è un Artifact, non un file del repo |
| `first-reader` · `skim.py` | La vista di chi scorre: titoli, grassetti, prime parole, numeri. Chi scorre dice *cos'è* e *se lo apre* | **L5** → il DM a freddo: «scorrendo il master, so cosa succede stasera?» | `signals.py` (la fiducia nell'autore): regex inglesi di esitazione e certezza, pensate per un saggio. Un master non ha un autore implicito da giudicare |
| `first-reader` · `personas.md`, `report.md` | Tre regole: *mai fabbricare rilievi*, *il rapporto può dire che va bene*, e un **caso di controllo** nell'eval che verifica proprio questo. Le letture del repo danno fra 17 e 46 rilievi **ogni volta**: nessuno ha mai misurato se ne inventano | **L1** → una scena di controllo nella calibrazione | la tabella della pazienza (dati di pagine web e feed social): il DM che prepara ha un altro tempo, e lo misura L5. L'ordine del rapporto di Lerman: la nostra uscita è una tabella di rilievi, e resta così |
| `first-reader` · `interview.md` | «Mai migliorare una risposta»: *ci è voluto un po'* non diventa *tre settimane* | già nostro: `[INFERRED — needs DM confirmation]` | tutto il resto: l'intervista all'autore serve a chi scrive un saggio |
| **`advisor-orchestrator-worker`** | Il formato del **brief** per un agente senza memoria: input incollati per intero, criteri d'accettazione numerati, una riga `INPUT GAP` in testa se manca qualcosa. E la verifica che esercita il risultato vero, non un file accanto (è la nostra G2) | **L1** → il testo di invio del lettore e del playtester | il motore: `agy`, Gemini, API a pagamento, chiavi in ambiente, chiamate di rete. Il repo usa gli agenti della sessione |
| **`evals/tools/skill_lint.py`** | Il limite della specifica agentskills.io: **descrizione ≤ 1024 caratteri**. Misurato sul repo: **tre** skill oltre, `rumblingstone-indagine` 1.195, `rumblingstone-edizione` 1.147, `rumblingstone-mapmaking` 1.068 | **L6** → `validate_skills.py` | il controllo «ogni `scripts/…` citato esiste nella cartella della skill»: sul repo dà **24 errori, 24 falsi positivi**, perché le nostre skill citano `scripts/dm.py` della radice. Il corpo ≤ 500 righe: il massimo del repo è 300 (`editoria`), non serve un cancello |
| **`evals/tools/skill_scanner.py`** | Cerca nelle skill i modi in cui una skill fa danni: script scaricati e passati alla shell, rete non dichiarata, credenziali, codice offuscato. Sul repo: **1 CRITICO vero**, `dnd-35-srd/references/resources.md:250`, `curl -fsSL https://ollama.ai/install.sh \| sh` | **L7** → `validate_skills.py` | niente: si adotta intero e non adattato, così un aggiornamento è un diff (ADR-0010 §3) |
| **`evals/tools/run_trigger_evals.py`** | Prove di instradamento: frasi che devono accendere una skill e frasi vicine che non devono | **L8**, da decidere | il controllo di collisione: sul repo la coppia più vicina è al **16%** di vocabolario comune (`forgotten-realms-lore` e `rumblingstone-campaign`), quindi sarebbe verde, e non vede la sovrapposizione vera (C3, `indagine` e `narrative-style`). E la regola «la frase mette prima la sua skill» contraddice ORCHESTRAZIONE, dove C5-C7 vogliono **due** skill insieme |
| **`thinking-out-loud`** | Prima di agire su un messaggio lungo con molte decisioni, rimandare un'**eco**: missione, decisioni prese, domande aperte, ripensamenti, e **in una sezione a parte** quello che l'agente ha dedotto o indovinato | **L9**, facoltativo → `rumblingstone-plans`, quando il DM chiude un blocco di decisioni (il 2026-09-30 ne ha chiuse trenta) | la modalità dettatura e la persistenza in `CLAUDE.md`: da noi le decisioni stanno nella tabella del piano, marcata per `decisioni_dm.py` |
| **`commit-archaeologist`** | Perché una riga esiste, dalla storia git: il commit che l'ha introdotta, i file che cambiano sempre insieme a lei, i segnali d'intento nei messaggi, con tre livelli di confidenza | nessun lotto: se ne parla in D7 | ADR-0069 tiene la storia delle scelte **nel sorgente** (`<!-- storico -->`) e la regola §7 di `playtest` scrive nel file «correzione del playtest, rilievo N». La domanda «perché questa regola è così» ha già una risposta scritta; 388 righe per un secondo canale non si giustificano oggi |
| **`scope-creep-detector`** | Confronta il diff con l'intenzione e propone tieni, dividi, giustifica | scartato | la parentela fra percorso e intenzione: la regola d'oro dei piani obbliga **ogni** PR a toccare `plans/INDEX.md` e `plans/CHANGELOG.md`, che il rilevatore segnalerebbe sempre |
| **`dependency-doctor`** | Legge un `requirements.txt` in cerca di pacchetti che imitano la libreria standard e di backport inutili | scartato | la skill stessa dice di non usarla come cancello di CI, e il repo ha due manifest piccoli e fissati |
| **`project-graveyard`** | L'autopsia dei progetti abbandonati dalla storia git | scartato | i rami mai arrivati su `main` li conta già `contenuti_nei_rami.py`; il resto guarda la macchina di chi programma, non un repo |
| **`self-improving-agent-skills`** | ottimizza le skill con un modello | scartato | Gemini e ADK, rete, un'app Next.js; niente licenza propria |
| `evals/first-reader/ledger.md` | Ogni regola porta la sua provenienza, e un riscontro resta riscontro finché non si generalizza | già nostro: «un tipo di rilievo che torna in due moduli diventa una regola dello script» (`lettore-a-freddo.md`) | — |

## 4 · I lotti (uno per PR)

Nessuno parte senza il sì del DM. L'ordine è quello consigliato; L1 è il
prerequisito di L2, L4 e L5.

### L0 · L'ADR di adozione e la licenza — ✅ (2026-10-01, con L7)

- [x] [ADR-0076](adr/ADR-0076-adozione-da-awesome-llm-apps.md): fonte, commit
      `4bf51ab`, autori, la licenza non dichiarata di `first-reader`, cosa entra
      e cosa no, come si aggiorna; riga in `docs/INDEX.md`
- [x] la licenza sta accanto al codice: `scripts/terzi/LICENSE-APACHE-2.0` e
      `scripts/terzi/README.md` (fonte, commit, «modificato: no»), più la terza
      riga di `LICENSES.md`. Diverso dal piano, che la voleva in `scripts/`:
      tenerla nella cartella dei file di terzi dice a chi copia che lì non vale MIT
- [ ] ogni file **adattato** apre con origine, commit, autore, licenza,
      «modificato»: vale dai lotti L1, L2, L5, che sono i primi ad adattare
- [x] **D7 · le adozioni rimandate non si perdono**:
      `plans/adozioni-in-attesa.json` con fonte, commit, licenza, autore, URL
      dei file e una condizione misurabile; `scripts/adozioni_in_attesa.py
      --check` in CI, con cinque test. Prima voce `commit-archaeologist`: scatta
      quando almeno 3 file di gioco cambiano 10 o più volte in 60 giorni senza
      una riga di storia nel sorgente. Misurato il 2026-10-01: 0 file, la
      condizione è spenta. In un clone parziale lo script dice «non misurabile»

### L1 · La lettura a scene, senza guardare avanti — ✅ (2026-10-01)

- [x] `scripts/lettura_a_scene.py`, adattato da `feed.py`: servito su
      127.0.0.1, un passaggio per scena col riconoscitore di `copertura_scene`
      (premessa, scene, tratti fra le scene, coda: i cinque DEF si ricompongono
      identici), diario con i campi fissi, alla chiusura impronte e titoli e mai
      il testo. Il tempo minimo è 0,08 s per parola, e per gli agenti si mette a
      0: un agente legge in un istante, la barriera vera è il diario
- [x] nove test (`test_lettura_a_scene.py`), voce nel manifest
- [x] la rubrica del lettore («La lettura a scene») e il messaggio d'invio nella
      forma di `advisor-orchestrator-worker`; una norma nel registro
- [x] **calibrazione** (`esperimenti/lettura-a-scene-def4/`): DEF-4 del tavolo
      (`ddd683c`), due agenti nuovi, stessa rubrica. Intera **69** rilievi, **7**
      `L-ORDINE`; a scene **55** e **7**, **3 in comune**, contati a mano; delle
      lacune inventate al tavolo **3** contro **2**. Il diario non ha guardato
      avanti. **L'ipotesi del piano non regge su questo caso**: la lettura a scene
      non trova più `L-ORDINE`, ne trova di diversi. Il salto da 3 (settembre) a
      7 viene dalla rubrica. La rubrica è stata riscritta per dirlo, prima del
      merge; la scelta del modo è D8
- [ ] la scena di controllo per le invenzioni: nessuna scena di questo DEF-4 è
      senza difetti noti, quindi non c'è. Resta da fare su un master che ne abbia una

### L2 · Il ricordo del giorno dopo e le domande ai lettori — ✅ (2026-10-01)

`[engine: Sonnet · effort: medio · qualità: test + una prova su DEF-5 confrontata con il quiz di DEF-4]` — **C**

- [x] `scripts/ricordo_lettura.py` (da `recall.py` e `ask.py`, un file solo
      invece di due: leggono lo stesso diario): `domande` dà il pacchetto per
      un agente nuovo, sette domande da DM; `chiedi <corsa> <lettore|tutti>`
      le domande dopo la lettura; `intenzione <master>` la serata dichiarata,
      dal riquadro o dal Quickstart, ed esce 1 se il master non la dichiara.
      Sette test; uno è nato rosso: il pacchetto nominava solo la prima chiave
      del JSON di risposta
- [x] `quiz-a-due-agenti.md` «Il ricordo dal diario», il passo 7 in
      `module-standard`, la riga in `playtest` §2-bis, l'aggiornamento di
      ADR-0075 (D1); una norma nel registro (il master dichiara la sua serata)
- [x] prova (`esperimenti/lettura-a-scene-def4/RISULTATI.md`): DEF-4 del
      tavolo, quiz e ricordo sullo stesso diario della lettura a scene. Quiz
      **8 su 14** contro i 6 degli appunti di settembre, e q4 (la missione)
      giusta per la prima volta. Il confronto non è pari: 3.582 parole di
      diario contro 400 di appunti. Il ricordo ritrova quattro rilievi delle
      letture. L'intenzione di `ddd683c` è il primo paragrafo del Quickstart e
      non dice la missione: senza riquadro il giudizio non ha metro, che è
      quello che la norma del registro chiede

⚠️ Il quiz ha un punteggio deterministico, il ricordo no: lo giudica un agente.
È più economico e meno ripetibile, e il lotto lo scrive.

### L3 · (unito a L2)

Il DM aveva le domande ai lettori come idea a sé. Usano lo stesso diario e lo
stesso formato del ricordo: una PR sola.

### L4 · L'ancora: il registro delle letture a freddo (D26) — ✅ (2026-10-01)

- [x] `plans/letture-a-freddo.json`: per ogni master DEF le letture, con
      ruolo, data, rapporto, impronta del testo letto e i rilievi 🔴/🟠 con lo
      stato (`corretto` · `residuo` + ragione · `domanda` + decisione)
- [x] `scripts/registro_letture.py --check` in CI, dieci test: blocca una
      lettura scaduta, salvo una catena di voci «sola forma» con la ragione, e un
      🔴/🟠 senza stato. `--registra` aggiunge la lettura di una corsa di
      `lettura_a_scene.py` e rifiuta quella di un testo diverso da quello di
      oggi; `--confronta A B` mette due letture affiancate, scena per scena
- [x] **D4, avviso e poi bloccante da solo, master per master**: un master è
      sotto cancello quando l'ultima lettura del lettore e del playtester ha
      l'impronta. Da lì non torna in avviso, e un master nuovo senza letture
      non ci rimette gli altri. Diverso dalla prima stesura, che contava il
      registro intero: col primo master di ARC-08 tutto sarebbe tornato in avviso
- [x] le letture già fatte sono entrate così come sono: **21 letture, nessuna
      con un'impronta ricostruibile** fra le diciotto di settembre (ogni commit
      che ha aggiunto un rapporto ha cambiato anche il master), più le tre della
      calibrazione F2, che dichiarano il commit letto (`ddd683c`) e quindi
      l'impronta ce l'hanno. Oggi tutti e cinque i master sono in avviso: si
      chiudono con la prima lettura a scene di lettore e playtester
- [x] le due letture della calibrazione di L1 **non** entrano: leggono
      `ddd683c`, un testo già superato, e servono a confrontare due modi di
      leggere, non a dire se il master di oggi regge
- [x] PIANO-LETTORE: D26 rimanda a questo lotto; `playtest` §2-bis dice quando
      si rifà una lettura; una norma **maggiore** nel registro, 🟡

### L5 · Il DM a freddo, la quarta rubrica — 🟡 primo passo provato (2026-10-01) · si parte dalla vista di chi scorre (D2)

`[engine: Opus, sessione principale · effort: alto · qualità: una corsa su DEF-5 con L1 e L2, e il DM che riconosce la sua preparazione]` — **G**

- [x] `scripts/vista_di_chi_scorre.py`, adattato da `skim.py`: la serata
      dichiarata, i titoli, la riga «In scena» e la prima frase di ogni scena,
      i grassetti, le CD con le quattro parole prima. Sette test, voce nel
      manifest
- [x] `rumblingstone-playtest/references/dm-a-freddo.md`: tre passi (la vista,
      la preparazione a scene con un tempo dichiarato, il giorno dopo con le
      domande di chi conduce) e quattro codici `D-*`. Marcata **in prova**
- [x] **la prova del primo passo** (`esperimenti/dm-a-freddo/`): cinque agenti
      nuovi, uno per DEF, con la sola vista. La serata 5 su 5; chi si oppone
      **1 su 5**, ed è DEF-4, l'unico col riquadro. In DEF-2 e 3 un avversario
      non c'è e l'agente lo dice bene; in DEF-1 (cosa vuole Terros) e DEF-5 (gli
      orchi senza capo) sono rilievi veri. Tre agenti su cinque non sapevano a
      cosa servissero le CD: era la vista, corretta dopo la prova
- [x] `playtest` §2-bis: la terza riga dei ruoli, «in prova»; `module-standard`
      passo 6 lo nomina come non obbligatorio; una riga nel registro (🟡)
- [x] **la corsa intera su DEF-5** (`esperimenti/dm-a-freddo/corsa-def5/`):
      preparazione a scene con un'ora dichiarata, 13 rilievi (🔴 2), circa 40
      minuti «bastati in parte». Sette verificati a mano: sei veri, uno falso
      (Re Thorek si rialza solo se curato). Rispetto alle letture del 30
      settembre i nuovi sono due (Cantitrici e PNG giocabili senza scheda);
      cambia il peso, l'handout da 🟠 a 🔴. Il giorno dopo il diario non tiene
      chi parla per primo: la rubrica ora lo chiede. I rilievi del 30 settembre
      su handout e portale sono ancora aperti nel master
- [x] il DM che dice se la preparazione che ne esce somiglia alla sua (D9):
      **no, la sua copre molto di più** (D12). La rubrica ha ora undici voci
      `P-*` e la regola del confine fra ciò che sanno i PG e ciò che sa il master
- [ ] una corsa su DEF-5 che esegue le undici voci; i passi 2 e 3 escono dalla
      prova dopo quella

### L6 · Le descrizioni delle skill entro i 1024 caratteri — ✅ (2026-10-01)

`[engine: Sonnet · effort: basso · qualità: validate_skills verde con il controllo nuovo, e un test che lo fa mordere]` — **M**

- [x] `validate_skills.py`: descrizione ≤ 1024 caratteri, errore; due test in
      `test_skills_routing.py` (il repo sta sotto, e 1025 morde mentre 1024 no).
      Provato sul difetto vero: con le descrizioni di prima, 3 errori
- [x] accorciate `indagine` (1.195 → 989), `edizione` (1.147 → 959),
      `mapmaking` (1.068 → 904), con un controllo a macchina che **nessun
      trigger fra virgolette** è andato perso; `indagine` ne aveva due ripetuti
      («cospirazione», «sparizione»)
- [x] ~~riga nel registro delle norme~~: non serve. Il registro tiene le norme
      **editoriali**; le regole sulla forma delle skill (ADR-0041, ADR-0058)
      vivono nel gate `validate_skills.py`, e questa sta con loro

Cosa fa ciascun agente con una descrizione oltre il limite (la tronca, la
scarta, la tiene) **non l'ho verificato**: il limite è della specifica, e i
mirror di `build-skills.sh` finiscono in agenti diversi.

### L7 · Lo scanner di sicurezza delle skill — ✅ (2026-10-01)

- [x] `scripts/terzi/skill_scanner.py`, **identico** all'originale (nessuna
      intestazione aggiunta: un file toccato non è più copiato); la provenienza
      sta in `scripts/terzi/README.md`
- [x] un passo suo in CI, accanto a `validate_skills.py` invece che chiamato da
      lui: un cancello di terzi resta riconoscibile come tale; voce nel manifest
- [x] `dnd-35-srd/references/resources.md`: tolto `curl … | sh`, resta il
      rimando alla pagina ufficiale (D5). Scanner su `skills/`: 0 CRITICI
- [x] **il controllo non si perde** (la domanda del DM su D5):
      `test_skill_scanner.py` rimette la riga in una skill finta e verifica che
      lo scanner esca 1; fissa anche l'impronta SHA-256 del file

### L8 · Prove d'instradamento delle skill — ✅ (2026-10-01) · D6

`[engine: Sonnet · effort: medio · qualità: da definire con il DM]` — **R** prima di **C**

- [x] trenta frasi vere del DM, da `plans/`, `skills/` e `AGENTS.md`, con le
      skill obbligatorie di ORCHESTRAZIONE §4 (`instradamento/casi.json`),
      metà per tarare e metà per verificare
- [x] `scripts/instradamento_skill.py`: per ogni frase, quali skill
      obbligatorie raggiungono i trigger fra virgolette delle descrizioni;
      omissioni, skill in più, conflitti fra le due L1. Dieci test. In CI, a
      cricchetto sul tetto del file
- [x] **la misura** (`instradamento/RISULTATI.md`): 38 omissioni su 46 prima,
      **13** dopo; sulle frasi di verifica, mai usate per tarare, da 19 a 8.
      Le skill in più salgono da 2 a 7, ed è scritto
- [x] **applicate**: trigger italiani nelle descrizioni di `campaign` (i nomi
      dei PG, «canone», «arco», «Bestiario», «PNG»…), `module-standard`
      («modulo», «master», «avventura», «stanze»…), `npc-villain-boosting`
      («statblocco», «più forte», «archetipi»…), `prosa-documenti`
      («documentazione», «piano», «ADR», «PRD») e `narrative-style` («prosa»,
      «stile», «echi», «faide»). Tolto il trigger «documento» da
      `narrative-style`, che avrebbe mandato una frase sui documenti del repo
      alla L1 sbagliata. Tutte sotto i 1024 caratteri
- [x] una norma nel registro (maggiore, 🟡)

### L9 · L'eco prima di applicare un blocco di decisioni — ✅ (2026-10-01) · D6

`[engine: Opus · effort: basso · qualità: la norma ha una riga nel registro, misurata o col perché]` — **G**

- [x] la norma in `rumblingstone-plans`, «L'eco prima di applicare»: due o
      più decisioni chiuse in un messaggio vogliono nel piano il blocco
      `<!-- eco: ETICHETTA DATA -->` con **Decise**, **Aperte**, **Cambiate** e
      **Dedotto da me**
- [x] il piano diceva «nessuno la misura»: la misura invece c'è, perché le
      tabelle le legge già `decisioni_dm.py`. `scripts/eco_decisioni.py` le
      raggruppa per data di chiusura, e da due in su chiede l'eco di quella
      data. Sette test, uno sul repo. In CI
- [x] **provata prima di applicare**: sul repo il rilevatore ha bocciato
      l'unico blocco dal 2026-10-01, D1-D7 di questo piano, che l'eco non
      l'aveva. **Applicata**: l'eco scritta nel piano, con quello che ho
      dedotto io a parte (D4 per master, il test di D5, le frasi vere di L8).
      Ora il gate è verde
- [x] una norma nel registro, maggiore, 🟢. Le sei chiusure a blocchi di
      prima del 2026-10-01 si contano e non bloccano: scriverne l'eco oggi
      sarebbe inventarla

### L8-bis · Il campione verificato e confrontato con la comunità — ✅ (2026-10-01) · D10

- [x] test sul campione (`test_instradamento_skill.py`, `TestIlCampione`): ogni
      frase letterale nella sua fonte e attribuita al DM; etichette coerenti
      con ORCHESTRAZIONE (una L1, attese ed escluse disgiunte); chi nomina uno
      dei 322 nomi della campagna vuole `campaign`; le due metà hanno casi e
      quasi-casi. **Trovati e corretti**: una frase che era mia e non del DM, una
      composta da due citazioni, le fonti scritte a memoria
- [x] il confronto con agentskills.io, `skill-creator` di Anthropic e
      `run_trigger_evals.py` di awesome-llm-apps (`instradamento/RISULTATI.md`,
      D10). Adottati: i quasi-casi e il campo «escluse» con un secondo tetto,
      le collisioni fra descrizioni, la prova con agenti veri a tre corse.
      Non adottati, col perché: la skill giusta per prima (qui le skill si
      sommano), la riscrittura automatica (chiede `claude -p` in CI)
- [x] la prova comportamentale: tre agenti caricano 40 obbligatorie su 47,
      contro le 32 dei soli trigger. Un confine nella descrizione di
      `narrative-style`, scelto sulla metà di taratura, porta le escluse
      caricate da 1 a 0. Due etichette corrette sulle prove, sei disaccordi
      lasciati scritti
- [x] `--frase` per avere un primo suggerimento da una richiesta del DM,
      citato in ORCHESTRAZIONE §2

### L10 · `commit-archaeologist`, quando la condizione scatta — ⬜ · in attesa

`[engine: Opus · effort: medio · qualità: ADR-0010 rispettato, la voce del registro passa a «da adottare»]` — **G**

Si apre da solo: `adozioni_in_attesa.py --check` esce 1 in CI quando almeno tre
file di gioco cambiano dieci o più volte in sessanta giorni senza una riga di
storia nel sorgente. Fonte, commit, licenza e URL dei file stanno nel registro.

### L11 · Il giro sulle skill di scrittura — ✅ (2026-10-02) · D11

`[engine: Opus, sessione principale + agenti di corsa · effort: alto · qualità: la verifica migliora dopo correzioni fatte sulla sola taratura]` — **G**

Il DM: *«includi nel giro anche le skilsl che si occupano di scrivere con lo
stile i costrains tipiche specificate nel repo […] Usa lo stesso metodo ricerca
e affinamento usato per le altre skills»*. Il metodo di L8 e L8-bis, portato
dall'instradamento all'**uscita**: cosa scrive un agente con la skill e senza.

- [x] FASE 1 sulle skill di scrittura, e i `references/` letti per intero (G1):
      i quattro obbligatori di `narrative-style`, `passate-redazionali`,
      `pc-protagonism`, `prosa-documenti`, `sviluppo-degli-incontri`
- [x] la ricerca editoriale (`RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09` §6): il
      formato degli incontri Paizo e i consigli sul boxed text di Shawn Merwin
      (D&D Beyond), confrontati con le norme già registrate. Quasi tutto c'è
      già; l'unica norma candidata nuova è «niente *sembra* e *pare* nei box»
      (D13)
- [x] **due difetti trovati leggendo, prima di ogni corsa**: P1 («il box non
      presuppone un'azione o un senso del giocatore», 🟢 nel registro) non è
      scritta in `read-aloud-adulti.md`, che il registro cita come fonte, e tre
      esempi ✅ della skill la violano (*«Ti accorgi che hai smesso di
      camminare»*); `validate_prosa.py` legge 32.765 delle 55.680 parole di
      read-aloud (59%), perché riconosce solo i box nudi e solo la prima riga
- [x] `scripts/voto_scrittura.py`: il voto riusa i rilevatori di `misura_craft`
      e `validate_prosa`, nessuna regex nuova nel punteggio; i casi
      (`plans/scrittura/casi.json`) nello schema di `skill-creator`, dieci, a
      metà fra taratura e verifica, stratificati per genere
- [x] tornata A: tre corse con le skill e tre senza. Una senza skill
      scartata perché aveva letto il voto (`plans/scrittura/scartate/`) e
      rifatta. Con le skill **96%** in taratura e **94%** in verifica, senza
      **89%** e **81%**
- [x] le correzioni al metro, che non sono stile: `validate_prosa` legge
      tutti i box con il rilevatore di `misura_craft` (i rilievi del repo da 180
      a 229); le sigle DES, COS, CAR e ARC non sono più «maiuscole di enfasi»
      (tre handout su tre puniti per aver riportato bene il canone)
- [x] le correzioni alle skill, solo sui fallimenti di taratura delle corse
      con le skill: l'etichetta su **ogni** box, il tono del dialogo in poche
      parole (`editorial-standards` §2); D14, P1 scritta in
      `read-aloud-adulti.md` §1 e l'esempio della reticenza rifatto; D13, la
      norma su «sembra» nella skill, nel registro e nel voto. Il 2026-10-02,
      su richiesta del DM, anche i due esempi di `italiano-nativo.md` §6 e §7
      (testi per un solo giocatore, dove P1 lascia la seconda persona): ora
      a muoversi è l'oggetto, non il PG
- [x] il lotto dei box con «sembra» o «pare» (D13): 30 box, non 34
      («appare» tolto dal rilevatore). Undici documenti di revisione in
      `plans/scrittura/revisioni-D13/`, 27 modifiche su 25 box; cinque box
      restano, con la ragione (D17). ✅ **Approvato dal DM e applicato il
      2026-10-03**, tutte le 27 modifiche
- [x] tornata B con le skill corrette: verifica da 96% a **100%**, taratura
      100%. Le ultime bocciature erano del metro (etichetta su una riga sua),
      corretto e riapplicato a tutte le corse
- [x] `plans/scrittura/RISULTATI.md`, 22 test del voto, la voce nel manifest

### L12 · Dal segnalare al correggere, e le skill secondo la guida — ✅ (2026-10-02) · D15, D16, D17 chiuse

`[engine: Opus, sessione principale + agenti di corsa · effort: alto · qualità: tornata C ≥ B sulla verifica, e la correzione non cambia un fatto]` — **G**

Il DM: *«Il valore delle skills e poi non solo segnalare ma migliorare cosa
segnalano […] si fa riferimento alle migliori soluzioni indicate dalla
community»*. Due fonti, lette il 2026-10-02:

- **Anthropic, *Skill authoring best practices***: tre esempi input/output per
  comportamento, valutazioni prima della documentazione, il ciclo «validatore →
  correggi → ripeti», un indice nei references oltre le 100 righe, references a
  un solo livello dallo `SKILL.md`.
- **Humanizer** (blader, MIT, su *Signs of AI writing* di Wikipedia): segnala
  **e** riscrive; tic ordinati per forza, i «deboli da soli» contano in gruppo;
  non inventa fatti; prima bozza, critica, versione finale. Si adottano le idee,
  non il codice.

Misure di partenza: 20 references di scrittura su 21 oltre le 100 righe senza
indice; `style-pillars.md` rimanda a 4 references, `documento-ed-errore-fecondo.md`
a 5; `italiano-nativo.md` ha 6 coppie ❌/✅ su più di trenta regole, e nessuna
sui tic del §9.

- [x] `italiano-nativo.md` §1-bis: per i sei calchi misurati, due casi veri
      dai file di gioco (lo sbagliato con la riscrittura, e quello giusto che
      il rilevatore prende per sbaglio, cioè il confine) accanto al terzo
      della tabella. Per *assumere* il repo non ha un caso sbagliato
- [x] l'indice in testa ai references oltre le 100 righe, in tutte le skill:
      `indice_references.py`, in CI, 51 su 59. I rimandi a un livello:
      misurati, zero references raggiungibili solo passando da un altro
- [x] la self-check come ciclo: domanda 8 in `narrative-style` e in G4 di
      `AGENTS.md`, con `ciclo_prosa.py`. 78 norme
- [x] `scripts/ciclo_prosa.py` (stdlib), tre comandi come fra revisore e
      autore (D15): `segnala`, `revisione` (il documento con le modifiche in
      CriticMarkup, numerate, ognuna con la sua norma e una casella, e le due
      garanzie: nessun controllo peggiora, nessun fatto cambia), `applica` (le
      sole spuntate, mai su `main`, con la riga `revisione-testo: rN`). 16 test
- [x] ADR-0077, con l'attribuzione: CriticMarkup (Apache 2.0), Humanizer (MIT),
      *Signs of AI writing* (CC BY-SA 4.0), evaluator-optimizer di Anthropic.
      Nessun codice di terzi; scartati Vale, proselint e LanguageTool
- [x] la norma nuova nel registro (G3): i tic minori in gruppo, 🟡 e fuori dal
      punteggio finché la soglia non è tarata. 76 norme
- [x] il ciclo provato su un testo di corsa (A-senza-4/S04): undici cambi di
      una parola diventati tre modifiche; il secondo giro riporta il residuo
      della modifica non spuntata. La prova ha trovato un buco di D13 (il
      participio «sembrato»), corretto alla fonte
- [x] l'applicazione automatica di quello che migliora (richiesta del DM del
      2026-10-02): `applica --auto` applica le modifiche motivate che, da
      sole, non cambiano un fatto, non peggiorano un controllo e non
      abbassano la lettura (Gulpease, ritmo delle frasi), e le segna
      `[x] auto` nel documento. LanguageTool come servizio facoltativo
      (`--languagetool URL`, LGPL fuori dal repo); dal container è bloccato
      dalla rete. ADR-0077 §7-8, 77 norme, 26 test
- [x] tornata C sulla verifica: 98/99, e l'unica bocciatura è un falso
      positivo sul confine di §1-bis (contata a mano, C = B). Tutti e tre gli
      agenti hanno usato `ciclo_prosa.py segnala` da soli. Due correzioni al
      metro (l'etichetta che va a capo, l'insieme non chiesto), A e B
      invariati. Il ciclo provato sui testi delle corse (A-senza-4/S04) e sui
      master (lotto D13)

### L13 · Di quanto migliora — ✅ (2026-10-03)

`[engine: Opus, sessione principale · effort: alto · qualità: nessuna revisione applicata peggiora la misura, e il cancello lo prova in CI]` — **G**

Il DM, il 2026-10-03: *«si può automatizzarla migliorando la prosa il più
possibile e misurando il miglioramento ottenuto»*. Decisione nell'estensione di
[ADR-0077](adr/ADR-0077-revisione-a-due-giri.md).

- [x] D13 applicato (27 modifiche, undici master) e D17 decisa: il «sembra»
      smentito entro la frase dopo resta. Confine scritto in
      `read-aloud-adulti.md` §1 punto 7 e nel rilevatore
      (`voto_scrittura.sembra_esitanti`); sui file di gioco restano 3 box su
      502, tre falsi positivi dichiarati nel registro delle norme
- [x] il documento di revisione porta «Di quanto migliora»: MQM e segnalazioni
      norma per norma, prima e dopo, e la garanzia che MQM non scenda
- [x] `ciclo_prosa.py lotto` (pacchetti e classifica MQM), `misura` (il delta
      di un giro, e quando fermarsi), `registro --check` (in CI)
- [x] `plans/scrittura/miglioramenti.json` riempito con le undici revisioni
      D13: segnalazioni da 293 a 265, MQM +2,52 punti
- [x] «sembra/pare» nel punteggio MQM (`box_sembra_pare`, minore): le norme
      pesate passano da 12 a 13, e la linea di base si riscrive
- [x] la prova sull'ARC-08: classifica in `plans/scrittura/lotto-ARC08-2026-10-03/`,
      quattro revisioni in `plans/scrittura/revisioni-pilota-ARC08/`, **da
      approvare** (D15). Il metro dei nomi propri contava due un nome composto:
      corretto con i dati (`misura_craft._nomi_composti`)
- [x] 10 test nuovi in `test_ciclo_prosa.py`, 4 in `test_voto_scrittura.py`
- [ ] il DM approva le quattro revisioni della prova; poi il lotto di
      `ARC08-01-GUIDA-DM.md` (55 segnalazioni, la più grande)

## 5 · Decisioni aperte al DM

<!-- decisioni-dm: AGENT-SKILLS -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | L2 | ✅ **Decisa il 2026-10-01**: sì. Il ricordo dal diario diventa il passo 7 del ciclo per tutti i master; il quiz resta dove una chiave approvata c'è già (DEF-4). ADR-0075 va aggiornato in L2. Era: **Il ricordo del giorno dopo sostituisce il quiz?** |
| ~~D2~~ | L5 | ✅ **Decisa il 2026-10-01**: la bozza non c'è; L5 parte dalla vista di chi scorre (`skim.py`), poi il DM la rivede. Era: **Dov'è la bozza del DM a freddo?** |
| ~~D3~~ | L1 | ✅ **Decisa il 2026-10-01**: sì, il passaggio è la scena intera; una scena troppo lunga per una lettura è un rilievo. Era: **Il passaggio è la scena intera?** |
| ~~D4~~ | L4 | ✅ **Decisa il 2026-10-01**: in avviso finché le letture già fatte hanno l'impronta, poi **bloccante, da solo**: il DM, *«dopo se c'è l'avviso vogliono siano bloccati così si modificano davvero»*. Il cancello passa a bloccante appena il registro è popolato, senza un intervento a mano. Era: **Il cancello del registro parte bloccante o in avviso?** |
| ~~D5~~ | L7 | ✅ **Decisa il 2026-10-01**: si toglie il comando, resta il rimando; e il controllo resta in CI con un test che lo fa mordere. Era: **La riga `curl … \| sh` in `dnd-35-srd`** |
| ~~D6~~ | L8, L9 | ✅ **Decisa il 2026-10-01**: partono tutti e due. L8: misure sulle frasi vere del DM e un rilevatore; L9: si prova, poi si applica, *«altrimenti non servono a niente»*. Era: **Partono, o restano proposte?** |
| ~~D7~~ | L10 | ✅ **Decisa il 2026-10-01**: resta fuori per ora, ma citato e messo in un registro di adozioni in attesa con gli URL e una condizione che, quando si accende, fa partire l'adozione (`plans/adozioni-in-attesa.json`, ADR-0076). Era: **`commit-archaeologist` resta fuori?** |
| ~~D8~~ | L1 | ✅ **Decisa il 2026-10-01**: due letture: prima a scene, con il diario, poi il modulo intero; la tabella dice in quale è nato ogni rilievo. Il DM: *«leggere la scena la prima volta per capire cosa capisce della scena e poi una seconda lettura che legge tutto intero»*. Era: **Il lettore a freddo legge intero o a scene? |
| ~~D9~~ | L5 | ✅ **Decisa il 2026-10-01**: proposta accettata: il primo passo obbligatorio al passo 6, il secondo e il terzo in prova finché il DM non giudica `corsa-def5/PREPARAZIONE.md`. Il registro delle letture chiede ora anche la lettura `dm`. Era: **Il DM a freddo entra nel ciclo del master? |
| ~~D10~~ | L8 | ✅ **Decisa il 2026-10-01**: non si confermano a mano: si verificano con test di correttezza e coerenza, e si confrontano con le pratiche di agentskills.io, `skill-creator` di Anthropic e `run_trigger_evals.py` di awesome-llm-apps (L8-bis). Era: **Gli insiemi attesi delle trenta frasi sono giusti? |
| ~~D11~~ | L8-bis | ✅ **Decisa il 2026-10-01**: sì. Confine aggiunto e cinque frasi nuove di verifica: le obbligatorie caricate dagli agenti salgono a 45 su 50, le nuove 3 su 3. Il confine non ha avuto effetto sulla frase del Drappo, che il Drappo non lo nomina: corretta l'etichetta. Era: **Il Drappo fuori dalla campagna, nella descrizione di `campaign`?** |
| ~~D12~~ | L5 | ✅ **Decisa il 2026-10-01**: la preparazione dell'agente non basta. Il DM elenca la sua: risolvere i problemi oltre a vederli, lo stato del gruppo e del mondo, cosa si muove senza i PG, lo stile e le immagini già fatte, le immagini e gli handout mancanti, il flusso, le domande dei PG, i congegni descritti col read-aloud senza anticipare, le interazioni con artefatti e mondo, e il confine fra ciò che sanno i PG e ciò che sa il master. Diventano le undici voci `P-*` di `dm-a-freddo.md`. Era: **La preparazione di `corsa-def5/PREPARAZIONE.md` somiglia alla tua?** |
| ~~D13~~ | L11 | ✅ **Decisa il 2026-10-01**: sì. «Sembra» e «pare» nei box diventano una norma **minore**, con il rilevatore di `voto_scrittura.py` che passa da indizio a controllo e un lotto che corregge i 34 box; «come se» resta fuori. Era: **«Sembra» e «pare» nei box: norma nuova?** |
| ~~D14~~ | L11 | ✅ **Decisa il 2026-10-01**: vince P1. Il gesto passa a un PNG o al mondo; P1 si scrive in `read-aloud-adulti.md` §1 e i tre esempi ✅ si correggono. Era: **P1 contro la reticenza sull'emozione** |
| ~~D15~~ | L12 | ✅ **Decisa il 2026-10-02**: sì, con un documento di revisione in mezzo. Il DM: *«deve proporre un documento che faccia leggere cosa e cambiato rispetto all originale così si possono approvare le modifiche»*, come fra revisore e autore. Le modifiche si approvano una per una, e il testo approvato porta la riga di revisione (ADR-0077). Era: **Fin dove arriva la correzione automatica?** |
| ~~D17~~ | L12 | ✅ **Decisa il 2026-10-03**: sì. Il «sembra» smentito entro la frase dopo resta; il confine è in `read-aloud-adulti.md` §1 punto 7 e il rilevatore lo salta (`voto_scrittura.sembra_esitanti`). Era: **«Sembra» seguito dalla smentita è lecito?** Tre box usano l'apparenza per prepararne la rottura: «quella che sembrava una parete — è una palpebra». Lì «sembra» non esita, è il colpo. *Proposta*: sì, entra in `read-aloud-adulti.md` §1 punto 7 come confine, e il rilevatore salta un «sembra» seguito entro la frase dopo da «invece», «non lo è», «si rivela», «è». I box restano come sono finché il DM non decide |
| ~~D16~~ | L12 | ✅ **Decisa il 2026-10-02**: si cercano le soluzioni della comunità con una licenza compatibile e si applicano: CriticMarkup, Humanizer, *Signs of AI writing*, la guida di Anthropic sulle skill (ADR-0077). Era: **Quale «documento migliorato» si migliora con le misure?** |

### L'eco del 2026-10-01

Il DM ha chiuso D1-D7 in un messaggio solo. L'eco, scritta dopo e non prima
(la norma è nata da questo lotto, L9): è il caso da cui viene.

<!-- eco: AGENT-SKILLS 2026-10-01 -->
- **Decise**: D1 il ricordo dal diario fa il passo 7, il quiz resta dove la chiave c'è · D2 il DM a freddo parte da `skim`, «e poi vediamo» · D3 il passaggio è la scena intera · D4 il registro in avviso, poi bloccante da solo · D5 via il `curl … | sh`, il controllo resta · D6 partono L8 e L9 · D7 `commit-archaeologist` fuori, in un registro d'attesa con la condizione
- **Aperte**: nessuna di quelle sette; restano D8, D9, D10, nate dopo dai lotti
- **Cambiate**: D4, dalla proposta «parte in avviso» a «avviso, poi bloccante da solo, master per master»; D7, da «resta fuori» a «fuori con una condizione che la fa entrare»
- **Dedotto da me**: che «bloccante da solo» valga master per master e non per il registro intero (L4: un master nuovo senza letture avrebbe rimesso tutto in avviso); che la domanda su D5, «quel test non è perso giusto?», chiedesse un test che fa mordere lo scanner, e non solo il controllo in CI; che per L8 «misurazioni» volesse dire frasi vere del DM e non frasi scritte da me

Seconda eco dello stesso giorno, per D8-D10. Scritta dopo aver applicato D8 e
D9, che toccavano solo rubriche, e prima del lavoro di D10.

<!-- eco: AGENT-SKILLS 2026-10-01 -->
- **Decise**: D8 il lettore legge due volte, prima a scene e poi intero · D9 il primo passo del DM a freddo obbligatorio, gli altri due in prova · D10 gli insiemi attesi si verificano con test e col confronto con le pratiche della comunità
- **Aperte**: il giudizio del DM su `corsa-def5/PREPARAZIONE.md`, che fa uscire dalla prova i passi 2 e 3 del DM a freddo
- **Cambiate**: D8, dalla proposta «intero il lettore, a scene playtester e DM» a «tutti e due i modi, nello stesso lettore»; D10, da «li confermi tu» a «li verificano i test»
- **Dedotto da me**: che per D8 il lettore sia **lo stesso** nelle due letture (il DM dice «una seconda lettura», non «un secondo lettore»), e che quindi il guadagno misurato con due agenti diversi vada rimisurato; che per D9 «obbligatorio» voglia dire un cancello, e che il cancello giusto sia il registro delle letture col ruolo `dm` accanto a lettore e playtester; che per D10 le «skill in rete» da confrontare siano gli strumenti di valutazione dell'attivazione, non altre skill di contenuto

Terza eco dello stesso giorno, per D11. Il DM l'ha chiusa insieme a una
richiesta nuova (il giro sulle skill di scrittura, L11).

<!-- eco: AGENT-SKILLS 2026-10-01 -->
- **Decise**: D11, il confine sul Drappo in `campaign` e cinque frasi nuove come seconda verifica
- **Aperte**: il giudizio del DM su `corsa-def5/PREPARAZIONE.md`, che ha chiesto di leggere per approvarla o modificarla
- **Cambiate**: nessuna
- **Dedotto da me**: che le «cinque frasi nuove» potessero venire dai suoi messaggi di oggi, trascritti nel repo, perché frasi scritte nei piani dopo oggi ancora non ce ne sono; che «includi nel giro anche le skill che scrivono con lo stile» chieda per quelle skill la prova sull'**uscita** (cosa scrive un agente con e senza la skill), e non solo l'instradamento

Quarta eco dello stesso giorno, per D12: la risposta del DM su
`PREPARAZIONE.md`, arrivata mentre L11 era a metà.

<!-- eco: AGENT-SKILLS 2026-10-01 -->
- **Decise**: D12, la preparazione del DM a freddo non è una lettura: sono undici lavori, più il confine fra ciò che sanno i PG e ciò che sa il master
- **Aperte**: una corsa su DEF-5 con le undici voci, che fa uscire dalla prova i passi 2 e 3
- **Cambiate**: il passo 2, da «leggi a scene e annota dove inventeresti» a «prepara la serata»; i passi restano in prova, ma per un motivo diverso
- **Dedotto da me**: che in una corsa d'agente «generare le immagini mancanti» valga come **elencarle** quando la corsa non può generarle, e che gli handout invece si scrivano; che «risolvere tutti questi problemi» chieda una risposta da dare al tavolo per ogni rilievo, non una correzione del master, che resta un lavoro a parte con le sue letture; che il confine PG/master sia una regola trasversale e non una dodicesima voce

Quinta eco dello stesso giorno, per D13 e D14, arrivate a tornata A ferma.

<!-- eco: AGENT-SKILLS 2026-10-01 -->
- **Decise**: D13 «sembra» e «pare» nei box sono una norma minore, con rilevatore e correzione dei 34 box · D14 vince P1, il gesto passa a un PNG o al mondo
- **Aperte**: nessuna delle due; restano la tornata A e la corsa DEF-5 con le undici voci di D12
- **Cambiate**: nessuna, tutte e due come proposte. D14 è stata chiarita con una domanda, perché il messaggio si fermava a «d14»
- **Dedotto da me**: che le due decisioni si applichino **dopo** la tornata A, perché le corse di base devono girare sulle skill com'erano, altrimenti il prima e dopo non si legge; che il lotto dei 34 box segua la FASE 1 sui file d'arco e non tocchi gli archivi dichiarati

Sesta eco, del 2026-10-02, per D15 e D16. Il DM ha risposto insieme, e su
`ciclo_prosa.py` ha aggiunto una richiesta: non solo gli stili del repo.

<!-- eco: AGENT-SKILLS 2026-10-02 -->
- **Decise**: D15 la correzione passa per un documento di revisione da approvare modifica per modifica, poi torna al revisore per i residui · D16 si applicano le soluzioni della comunità con licenza compatibile
- **Aperte**: il resto di L12 (le skill di scrittura con tre esempi per regola e l'indice, i rimandi a un livello, la tornata C); il lotto dei 34 box di D13, che ora passa per `ciclo_prosa`
- **Cambiate**: D15, dalla proposta «chi lavora la applica sul ramo» a «il DM approva le modifiche una per una su un documento che mostra cosa è cambiato»; D16, da «quale documento» a «quali soluzioni della comunità»
- **Dedotto da me**: che il «meccanismo di versioning del DEF» sia una riga di revisione nel testo e non un sistema nuovo, perché la storia sta già in git e ADR-0071 fa lo stesso sulle pagine degli artefatti; che «non usare solo stili» chieda regole prese fuori dal repo **e** adattate all'italiano, perché quelle inglesi (Vale, proselint) non si applicano; che lo script debba fare il revisore e non l'autore, perché la riscrittura sicura resta di un modello o di una persona

## 6 · Validazione

- ogni lotto: `validate_skills.py`, `validate_docs.py`,
  `validate_norme_editoriali.py`, `check_plans_discipline.py`, i test del suo
  script, e `fase1.py` sui bersagli prima di toccarli (G6)
- L1 e L2 non sono cancelli: danno rilievi da contare a mano, come le letture
  di oggi. Il cancello è L4, e dice solo **quando** una lettura va rifatta
