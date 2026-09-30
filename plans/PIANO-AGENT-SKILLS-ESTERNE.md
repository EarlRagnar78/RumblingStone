# PIANO — Le skill di `awesome-llm-apps/agent_skills`: cosa si adotta, cosa si scarta

> **Cos'è**: la valutazione delle otto skill di
> [`Shubhamsaboo/awesome-llm-apps/agent_skills`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills)
> (più la loro cartella `evals/`), fatta contro le diciotto skill del repo, e i
> lotti per adottare il poco che serve. Letto al commit upstream
> `4bf51ab` (2026-09-28).
>
> **Stato**: ⬜ proposta, nessun lotto partito · **Decisore**: DM, che sceglie
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
l'elenco dei file, e il testo della licenza entra in `scripts/LICENSE-APACHE-2.0`.
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

### L0 · L'ADR di adozione e la licenza — ⬜

`[engine: Opus, sessione principale · effort: medio · qualità: validate_docs verde, LICENSES.md elenca ogni file Apache]` — **G**. Viaggia con il primo lotto che porta codice.

- [ ] ADR-0076, *adozione da awesome-llm-apps*: fonte, commit `4bf51ab`, autori
      per skill, la licenza non dichiarata di `first-reader`, cosa si prende e
      cosa si scarta (la tabella §3 in forma breve), come si aggiorna
- [ ] `scripts/LICENSE-APACHE-2.0` e la terza riga di `LICENSES.md`
- [ ] ogni file adattato apre con: origine, commit, autore, licenza, «modificato»

### L1 · La lettura a scene, senza guardare avanti — ⬜

`[engine: Opus per la calibrazione, Sonnet per lo script · effort: alto · qualità: test che provano il cancello mordere + calibrazione su DEF-4 contata a mano]` — **C** + **G**

- [ ] `scripts/lettura_a_scene.py`, adattato da `feed.py`: servito su
      `127.0.0.1`, un passaggio per scena col riconoscimento di
      `copertura_scene.py`, diario per scena con campi fissi: `ago` (−2…+2),
      `mi aspettavo`, `ho trovato`, **`so adesso`** (cosa sanno i PG e da chi),
      e i codici `L-`/`P-` al momento in cui scattano. Chiude scrivendo titolo e
      impronta di ogni scena, mai il testo
- [ ] test (`scripts/tests/test_lettura_a_scene.py`): il testo non è su disco
      prima della chiusura; il passaggio dopo non arriva senza diario né prima
      del tempo minimo; un diario sotto i 25 caratteri è rifiutato; le scene
      sono quelle di `copertura_scene`
- [ ] le rubriche del lettore e del playtester: un paragrafo «La lettura a
      scene», e il brief d'invio (formato di `advisor-orchestrator-worker`:
      input interi, criteri numerati, `INPUT GAP`)
- [ ] **calibrazione**: DEF-4 al commit del tavolo (`ddd683c`, come F2), letto
      intero e letto a scene, da agenti nuovi. Si contano a mano i rilievi
      `L-ORDINE` delle due letture, più **una scena di controllo** senza difetti
      noti, per vedere se la lettura ne inventa
- [ ] voce nel manifest, riga nel registro delle norme («il lettore legge a
      scene»: misurata dal cancello del registro L4, o dichiarata non misurata)

⚠️ **Il limite, da scrivere nella rubrica.** L'agente che legge ha il repo
davanti: se cerca il master con `grep`, lo trova. Il meccanismo gli toglie il
percorso, non la possibilità. `first-reader` ha lo stesso limite e lo tiene
con l'istruzione. Da noi si controlla dopo: il diario di un lettore che ha
guardato avanti cita cose delle scene successive, e la calibrazione lo guarda.

### L2 · Il ricordo del giorno dopo e le domande ai lettori — ⬜

`[engine: Sonnet · effort: medio · qualità: test + una prova su DEF-5 confrontata con il quiz di DEF-4]` — **C**

- [ ] `scripts/ricordo_lettura.py` (da `recall.py`): dal solo diario, sette
      domande da DM, giudicate contro *La serata in tre frasi* o il §0 del
      master. Nessuna chiave nuova da approvare
- [ ] `scripts/chiedi_al_lettore.py` (da `ask.py`): persona, diario, domanda;
      `tutti` per ogni lettore della corsa
- [ ] `quiz-a-due-agenti.md`: quando basta il ricordo e quando serve il quiz (D1)
- [ ] prova: DEF-4, dove la chiave c'è, ricordo e quiz sullo stesso diario, per
      vedere se il ricordo trova quello che il quiz trova (la missione mancante
      di q4 in `esperimenti/quiz-def4/`)

⚠️ Il quiz ha un punteggio deterministico, il ricordo no: lo giudica un agente.
È più economico e meno ripetibile, e il lotto lo scrive.

### L3 · (unito a L2)

Il DM aveva le domande ai lettori come idea a sé. Usano lo stesso diario e lo
stesso formato del ricordo: una PR sola.

### L4 · L'ancora: il registro delle letture a freddo (D26) — ⬜

`[engine: Opus per le regole del cancello, Sonnet per lo script · effort: alto · qualità: il cancello morde in un test su master cambiato e su 🔴 senza stato]` — **C** + **G**

- [ ] `plans/letture-a-freddo.json`: per ogni master DEF e ogni lettura, ruolo
      (lettore, playtester, DM a freddo), data, cartella della corsa, impronta
      del testo intero e di ogni scena, rilievi 🔴 e 🟠 con lo stato
      (`corretto` · `residuo` + ragione · `domanda al DM` + D-n)
- [ ] `scripts/registro_letture.py --check` in CI: rosso se il master è cambiato
      dopo l'ultima lettura (salvo una voce «sola forma» con la ragione), o se
      un 🔴 o un 🟠 non ha stato. `--confronta A B`: scena per scena, l'ago
      prima e dopo, dove il lettore si è fermato o ha riletto
- [ ] le letture già fatte (`def5-ciclo/`, `f4-def1-def3/`,
      `def4-seconda-serata/`) entrano con l'impronta del commit che hanno letto,
      dove la storia git lo dice; dove non lo dice, la voce lo scrive e il
      cancello chiede una lettura nuova
- [ ] PIANO-LETTORE: D26 passa da «lotto da aprire» a questo lotto

⚠️ **Il costo, già detto nella D26**: ogni modifica a un DEF, anche un refuso,
chiede una lettura prima del merge o una voce «sola forma». Il primo giorno il
cancello è rosso su ogni master la cui lettura non ha un'impronta
ricostruibile. Proposta: parte in avviso (stampa, esce 0) finché il registro è
popolato, poi blocca (D4).

### L5 · Il DM a freddo, la quarta rubrica — ⬜ · ⛔ su D2

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

### L6 · Le descrizioni delle skill entro i 1024 caratteri — ⬜

`[engine: Sonnet · effort: basso · qualità: validate_skills verde con il controllo nuovo, e un test che lo fa mordere]` — **M**

- [ ] `validate_skills.py`: descrizione ≤ 1024 caratteri, errore
- [ ] accorciare `indagine` (1.195), `edizione` (1.147), `mapmaking` (1.068)
      senza perdere i trigger che ORCHESTRAZIONE usa
- [ ] riga nel registro delle norme

Cosa fa ciascun agente con una descrizione oltre il limite (la tronca, la
scarta, la tiene) **non l'ho verificato**: il limite è della specifica, e i
mirror di `build-skills.sh` finiscono in agenti diversi.

### L7 · Lo scanner di sicurezza delle skill — ⬜

`[engine: Sonnet · effort: basso · qualità: lo scanner gira in CI su skills/, zero CRITICI]` — **M** + **G** per la riga di `resources.md`

- [ ] `scripts/terzi/skill_scanner.py`, intero, con l'intestazione di origine
- [ ] passo in CI, e `validate_skills.py` che lo chiama
- [ ] `dnd-35-srd/references/resources.md:250`: la riga `curl … | sh` diventa il
      rimando alla pagina d'installazione ufficiale, senza il comando da incollare

### L8 · Prove d'instradamento delle skill — ⬜ · proposta: rimandare

`[engine: Sonnet · effort: medio · qualità: da definire con il DM]` — **R** prima di **C**

Frasi italiane del DM («prepara la serata», «il modulo è pronto?») con
l'insieme di skill che ORCHESTRAZIONE vuole per ciascuna, controllate contro le
descrizioni. Sarebbe la misura di «zero omissioni di ciò che è obbligatorio».
Lo strumento esterno misura la cosa sbagliata (una skill prima, non un insieme),
e un controllo lessicale su descrizioni lunghe dà poco: prima una ricognizione
su 20 frasi vere del DM, poi si decide se vale un cancello.

### L9 · L'eco prima di applicare un blocco di decisioni — ⬜ · facoltativo

`[engine: Opus · effort: basso · qualità: la norma ha una riga nel registro, misurata o col perché]` — **G**

Una sezione in `rumblingstone-plans`: quando il DM chiude più decisioni in un
messaggio, prima di toccare i file si rimanda l'eco (decise, aperte, cambiate
di posizione, e **a parte** quello che l'agente ha dedotto). Nessuno la misura:
si registra con il perché.

## 5 · Decisioni aperte al DM

<!-- decisioni-dm: AGENT-SKILLS -->

| # | Lotto | Domanda |
|---|---|---|
| D1 | L2 | **Il ricordo del giorno dopo sostituisce il quiz?** Proposta: il ricordo diventa il passo 7 del ciclo per tutti i master (non chiede una chiave), e il quiz resta dove una chiave approvata c'è già, oggi solo DEF-4. Cambia ADR-0075: va scritto |
| D2 | L5 | **Dov'è la bozza del DM a freddo** usata il 30 settembre? Non è nel repo, né nei rami, né nelle PR aperte. Se c'è un testo, L5 parte da quello; se no, la scrivo dal piano e il DM la corregge |
| D3 | L1 | **Il passaggio è la scena intera?** Nei cinque master di ARC-07 ci sono 39 scene `### SCENA`, e 4 superano le 150 righe; la più lunga, DEF-4 Scena 5, ne ha 404 (contate fino al titolo successivo di livello 1-3, quindi per difetto). Proposta: sì, la scena; una scena troppo lunga per una lettura è già un rilievo |
| D4 | L4 | **Il cancello del registro parte bloccante o in avviso?** Proposta: in avviso finché le letture già fatte hanno un'impronta, poi bloccante |
| D5 | L7 | **La riga `curl … \| sh` in `dnd-35-srd`**: si toglie il comando e resta il rimando, o si toglie tutta la sezione sull'IA locale? |
| D6 | L8, L9 | Partono, o restano proposte? |
| D7 | — | `commit-archaeologist` resta fuori? Proposta: sì, finché la storia nel sorgente (ADR-0069) risponde |

## 6 · Validazione

- ogni lotto: `validate_skills.py`, `validate_docs.py`,
  `validate_norme_editoriali.py`, `check_plans_discipline.py`, i test del suo
  script, e `fase1.py` sui bersagli prima di toccarli (G6)
- L1 e L2 non sono cancelli: danno rilievi da contare a mano, come le letture
  di oggi. Il cancello è L4, e dice solo **quando** una lettura va rifatta
