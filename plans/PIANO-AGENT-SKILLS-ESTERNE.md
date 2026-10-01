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
- [x] PIANO-LETTORE: D26 rimanda a questo lotto; `playtest` §2-bis dice quando
      si rifà una lettura; una norma **maggiore** nel registro, 🟡

### L5 · Il DM a freddo, la quarta rubrica — ⬜ · si parte dalla vista di chi scorre (D2)

`[engine: Opus, sessione principale · effort: alto · qualità: una corsa su DEF-5 con L1 e L2, e il DM che riconosce la sua preparazione]` — **G**

- [ ] `rumblingstone-playtest/references/dm-a-freddo.md`: il DM che conduce
      stasera. Prima la vista di chi scorre (da `skim.py`: titoli, grassetti,
      prima riga di ogni scena, il riquadro): *so cosa succede stasera?*. Poi la
      lettura a scene (L1) con un tempo di preparazione dichiarato. Poi il
      ricordo del giorno dopo (L2) con le domande di chi conduce: *chi entra per
      primo*, *cosa dico se chiedono X*, *dove ho dovuto tornare indietro*
- [ ] `rumblingstone-playtest` §2-bis: la terza riga della tabella dei ruoli;
      `module-standard` ciclo, passo 6
- [ ] riga nel registro delle norme

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

### L8 · Prove d'instradamento delle skill — ⬜ · parte (D6)

`[engine: Sonnet · effort: medio · qualità: da definire con il DM]` — **R** prima di **C**

Frasi italiane del DM («prepara la serata», «il modulo è pronto?») con
l'insieme di skill che ORCHESTRAZIONE vuole per ciascuna, controllate contro le
descrizioni. Sarebbe la misura di «zero omissioni di ciò che è obbligatorio».
Lo strumento esterno misura la cosa sbagliata (una skill prima, non un insieme),
e un controllo lessicale su descrizioni lunghe dà poco: prima una ricognizione
su 20 frasi vere del DM, poi si decide se vale un cancello.

### L9 · L'eco prima di applicare un blocco di decisioni — ⬜ · parte (D6)

`[engine: Opus · effort: basso · qualità: la norma ha una riga nel registro, misurata o col perché]` — **G**

Una sezione in `rumblingstone-plans`: quando il DM chiude più decisioni in un
messaggio, prima di toccare i file si rimanda l'eco (decise, aperte, cambiate
di posizione, e **a parte** quello che l'agente ha dedotto). Nessuno la misura:
si registra con il perché.

### L10 · `commit-archaeologist`, quando la condizione scatta — ⬜ · in attesa

`[engine: Opus · effort: medio · qualità: ADR-0010 rispettato, la voce del registro passa a «da adottare»]` — **G**

Si apre da solo: `adozioni_in_attesa.py --check` esce 1 in CI quando almeno tre
file di gioco cambiano dieci o più volte in sessanta giorni senza una riga di
storia nel sorgente. Fonte, commit, licenza e URL dei file stanno nel registro.

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
| D8 | L1 | **Il lettore a freddo legge intero o a scene?** Calibrato il 2026-10-01 sul DEF-4 del tavolo: intero 69 rilievi e 7 `L-ORDINE`, a scene 55 e 7, tre in comune; il diario della lettura a scene però porta il ricordo (8 domande del quiz su 14 contro 6 degli appunti, e la missione che gli appunti perdevano sempre). Proposta: **il lettore legge intero** (trova di più); **il playtester e il DM a freddo leggono a scene**, e il loro diario fa il passo 7. Così ogni master ha tutte e due le letture, senza costi in più |

## 6 · Validazione

- ogni lotto: `validate_skills.py`, `validate_docs.py`,
  `validate_norme_editoriali.py`, `check_plans_discipline.py`, i test del suo
  script, e `fase1.py` sui bersagli prima di toccarli (G6)
- L1 e L2 non sono cancelli: danno rilievi da contare a mano, come le letture
  di oggi. Il cancello è L4, e dice solo **quando** una lettura va rifatta
