# PIANO — Automazione stato campagna & sessioni su branch-per-gruppo ("dm.py session")

> **Richiesta DM (2026-07-20)**: estendere `dm.py` perché gestisca
> automaticamente lo stato della campagna usando i file esistenti; a fine
> sessione un flusso guidato chiede al DM i fatti importanti, genera/aggiorna
> il session log, `campaign/state.md` e il campaign log, e produce gli hint
> per la sessione successiva; separa ciò che sanno i PG (anche
> singolarmente, se il party è diviso) da ciò che sa solo il DM; tutto vive
> su un branch di campagna dedicato (es. `campaign-group-rumblingstone-dm-gianfranco`)
> per non sporcare `main`.
>
> **Questo documento** è il piano di system design (stile PRD + lotti come
> gli altri piani del repo). Contiene un **verdetto di fattibilità onesto**,
> l'analisi dei punti duri, l'architettura proposta, i lotti di lavoro con
> stime, il piano di test e le domande aperte per il DM.

**Stato**: ⬜ proposto — in attesa di approvazione DM
**Decisioni architetturali collegate**: ADR-0002 (dm.py orchestratore), ADR-0007 (bozza, §6 qui sotto)

---

## §0 — Verdetto di fattibilità (TL;DR onesto)

**Sì, è fattibile ed è un addon efficace** — a patto di accettare tre
compromessi che derivano dalla natura del repo:

| Richiesta | Fattibilità | Nota onesta |
|---|---|---|
| Branch-per-gruppo automatico, `main` pulito | ✅ **alta** | Esiste già `scripts/new-campaign-group.sh` (Playbook §7). Va solo integrato in `dm.py` con una *guardia di branch* (rifiuta scritture di canone su `main`). Lavoro piccolo, rischio basso. |
| Wizard fine-sessione (domande → session log dal template) | ✅ **alta** | Il template `campaign/templates/session-template.md` è già strutturato a sezioni. Un wizard interattivo stdlib (input() con default) che compila il template è meccanico e deterministico. |
| Aggiornamento **automatico** di `state.md` | 🟡 **media — il punto duro** | `state.md` è prosa libera + tabelle. L'auto-edit affidabile è possibile SOLO su regioni strutturate (tabella §0, clock, changelog §8). La prosa narrativa **non va toccata da regex**: resta il flusso attuale "proposta → il DM conferma → applica". Chi promette il 100% automatico su un file di prosa sta mentendo. |
| Hint/evoluzioni per la prossima sessione | 🟡 **media** | Senza LLM (filosofia attuale del toolkit: deterministico, stdlib, zero API): si possono *aggregare* gli hook esistenti (`## Next session hooks`), le deadline dei clock (§0) e le finestre Day X-Y — utile ma non "creativo". Le *evoluzioni narrative* generate richiedono un LLM: modulo opzionale, spento di default (§5.5). |
| Separazione conoscenza PG / DM, anche per-PG con party diviso | ✅ **alta** (con modifica template) | La base c'è già: `session_recap.py` taglia `## DM notes (private)`. Per il per-PG serve un tag di visibilità nel template (retro-compatibile) + estensione del recap. Meccanico, testabile. |
| Testabilità | ✅ **alta** | Tutto stdlib + git: test con repo git temporanei e golden file. Nessuna dipendenza esterna. |

**Rischio principale**: non tecnico ma **di processo** — l'automazione che
scrive canone contraddice la regola attuale «gli script non scrivono mai
`state.md`/`sessions/`» (docstring dm.py, design rules toolkit). La
soluzione non è ignorare la regola ma **sostituirla formalmente** con
ADR-0007: *scritture di canone permesse solo (1) su branch di campagna,
mai su `main`, (2) dopo conferma esplicita del DM diff alla mano, (3) con
commit git immediato prima e dopo (undo naturale)*.

---

## §1 — PRD: attori, user story, requisiti

### Attori
- **DM** (Gianfranco): unico utente interattivo. Usa `dm.py` da terminale.
- **Giocatori/PG** (Thorik, Tordek, Hella, Artemis): consumatori passivi di
  recap/handout. Non toccano il repo.
- **Agenti AI** (skills): leggono `state.md` come fonte di verità — quindi
  l'automazione deve mantenerlo *coerente*, non solo aggiornato.

### User story
1. *Come DM*, a fine sessione lancio **un solo comando** che mi fa le
   domande giuste (XP, decisioni, clock, loot, PNG morti/fuggiti, hook) e
   ottengo il file sessione canonico già nominato `YYYY-MM-DD_session-N.md`.
2. *Come DM*, voglio che i cambi meccanici di `state.md` (dashboard §0,
   March/Ritual/Villain clock, changelog §8) siano **applicati** dopo che
   ho visto e confermato il diff — non voglio più fare copia-incolla a mano.
3. *Come DM*, voglio un brief "prossima sessione" con: hook aperti,
   deadline clock imminenti, dove ho lasciato ogni PG — e una versione
   spoiler-safe da girare ai giocatori.
4. *Come DM*, quando il party è diviso (com'è ORA: Tordek→Torneo,
   Hella→Foresta Sacra, Artemis→Torre Invisibile), voglio recap separati
   per-PG che contengano **solo** ciò che quel PG ha visto/sa.
5. *Come DM*, tutto questo avviene sul **mio branch di gruppo**
   (`campaign-group-<nome>`); `main` resta la libreria pulita di prep
   (archi, Bestiario, mappe) condivisibile con altri gruppi/DM.

### Requisiti non funzionali (ereditati dal toolkit)
- **R1** Solo stdlib Python ≥3.8 (nessuna dipendenza, come oggi).
- **R2** Deterministico e idempotente; rieseguire non deve corrompere nulla.
- **R3** dm.py resta orchestratore (ADR-0002): la logica vive in script
  dedicati, singolarmente invocabili e testabili.
- **R4** Ogni scrittura di canone è preceduta da un diff mostrato al DM e
  seguita da un commit git dedicato (recuperabilità totale).
- **R5** Retro-compatibilità: i file sessione esistenti (senza tag
  visibilità) continuano a funzionare in tutti gli script.

### Non-obiettivi (espliciti, per onestà)
- ❌ Riscrittura automatica della **prosa** di `state.md` (§1 party
  narrativo, §5-§7): resta proposta+applicazione manuale/assistita.
- ❌ Nessun database/SQLite: il markdown resta l'unica fonte di verità
  (leggibile, diffabile, merge-abile — è il punto di forza del repo).
- ❌ Nessun push automatico senza conferma; nessuna azione distruttiva
  (force-push, reset) mai.
- ❌ LLM nel percorso critico: se il modulo opzionale (§5.5) fallisce o è
  assente, tutto il resto funziona identico.

---

## §2 — As-is: cosa esiste già (e va riusato, non riscritto)

| Componente | Cosa fa oggi | Riuso nel piano |
|---|---|---|
| `dm.py post` | orchestra `update_xp.py` + `state_sync.py` (solo proposta) + checklist §4 stampata | diventa il "motore" dentro `dm.py session end` |
| `state_sync.py` | scandisce `## World events triggered`, regex sui trigger canonici, **report di proposte** mai applicato | riusato tal quale come *proposal engine*; si aggiunge solo l'*apply engine* a valle (§5.3) |
| `update_xp.py` | ledger XP cumulativo per PC (già scrive `campaign/pg/xp-ledger.md`) — precedente di scrittura automatica sicura | invariato |
| `session_recap.py` | recap spoiler-safe (taglia `## DM notes`), tono Salvatore, template deterministici | esteso con visibilità per-PG (§5.4) |
| `new-campaign-group.sh` | branch `campaign-group-<nome>` + reset state da template | invariato; la *branch guard* (§5.1) lo referenzia |
| `session-template.md` | sezioni canoniche incl. `## World events triggered` e `## DM notes (private)` | esteso v2 con tag visibilità (retro-compatibile) |
| Playbook §4 | procedura manuale 4.1→4.6 | resta la documentazione; il wizard ne è l'esecutore |
| `dm.py doctor` | diagnosi ambiente | esteso con i check nuovi (branch, marker state.md) |

**Gap reali** rispetto alla richiesta: (a) nessun wizard interattivo;
(b) nessun apply engine per `state.md`; (c) nessuna guardia di branch in
dm.py; (d) nessuna visibilità per-PG; (e) nessun generatore di brief
"prossima sessione". Tutto il resto c'è.

---

## §3 — Architettura proposta (to-be)

```
dm.py (orchestratore, ADR-0002 — invariato nello spirito)
 └── session                      ← NUOVO gruppo di sottocomandi
      ├── start   → session_wizard.py --start    (draft live da Playbook §3)
      ├── end     → session_wizard.py --end      (wizard Q&A → file sessione)
      │             update_xp.py                 (ledger, come oggi)
      │             state_sync.py                (proposta diff, come oggi)
      │             state_apply.py               ← NUOVO (applica SOLO su conferma)
      │             git commit (2×: pre-apply, post-apply)
      ├── next    → next_session.py              ← NUOVO (brief DM + teaser player)
      └── recap   → session_recap.py [--pg NOME] (esteso per-PG)

 guardia trasversale: campaign_branch.py  ← NUOVO
   - rifiuta `session end/apply` se branch == main
   - propone/crea `campaign-group-<nome>` (riusa la semantica di
     new-campaign-group.sh); il nome è configurato in campaign/group.yaml
```

### Flusso fine-sessione (happy path)

```
DM: python3 scripts/dm.py session end
 1. branch guard      → sei su campaign-group-rumblingstone-dm-gianfranco? ok.
                        (su main → STOP con istruzioni; mai scrittura)
 2. wizard Q&A        → data, n° sessione, presenti, summary (editor $EDITOR),
                        decisioni, XP, loot, clock tick, PNG morti/fuggiti,
                        hook, note DM private, [v2] blocchi per-PG
 3. scrive            → campaign/sessions/YYYY-MM-DD_session-N.md
 4. git commit #1     → "Session N: log" (il canone grezzo è al sicuro)
 5. update_xp.py      → ledger (come oggi)
 6. state_sync.py     → proposte diff (come oggi)
 7. state_apply.py    → mostra diff SOLO per le regioni marcate;
                        DM conferma per blocco [y/n/edit]; applica;
                        appende entry §8 changelog automaticamente
 8. git commit #2     → "Session N: state.md sync"
 9. stampa            → residuo manuale (prosa §5-§7, PNG files, push)
DM: python3 scripts/dm.py session next   (quando vuole, anche giorni dopo)
```

### Modello dei dati: regioni gestite in `state.md`

Il compromesso chiave (§0). Si introducono marker HTML-comment invisibili
al rendering:

```markdown
<!-- auto:begin key=dashboard -->
| Arc | Fase | Stato | March Clock | PG Lv | Note |
...
<!-- auto:end key=dashboard -->
```

Regioni gestite in v1: `dashboard` (§0), `march-clock`, `ritual-clock`,
`villain-clocks`, `changelog` (§8, append-only). Tutto ciò che è fuori dai
marker è **territorio del DM**: `state_apply.py` per costruzione non può
toccarlo (il parser lavora solo dentro i marker). Questo rende l'automazione
*dimostrabilmente* sicura invece che "speriamo che la regex non sbagli".

### Separazione conoscenza (v2 del template sessione)

```markdown
## Summary                        ← pubblico (tutti i PG), come oggi
## Split — Tordek @ Torneo di Dauth        ← NUOVO blocco opzionale
### Visto da: Tordek
...solo ciò che Tordek ha visto...
## Split — Hella @ Foresta Sacra
### Visto da: Hella
...
## DM notes (private — optional)  ← solo DM, già oggi mai esportato
```

Regole di visibilità (implementate in un modulo unico `visibility.py`,
usato sia da recap sia da hint, così la policy vive in UN posto):
- default: sezione pubblica → tutti i PG;
- blocco `## Split — <PG> @ <luogo>` → solo i PG elencati in `Visto da:`;
- `## DM notes` e tutto ciò che segue → **mai** esportato (regola attuale,
  invariata);
- `session recap --pg Tordek` → `campaign/recaps/pg/recap-YYYY-MM-DD-tordek.md`
  = sezioni pubbliche + soli i suoi blocchi Split;
- `session recap` senza flag → comportamento identico a oggi (R5).

### Hint "prossima sessione" (`dm.py session next`) — deterministico

Aggrega, senza inventare nulla:
1. `## Next session hooks` delle ultime N sessioni (non ancora "consumati");
2. deadline imminenti da §0 (es. "P1A Quest Hellas: finestra Day 20-30,
   March Clock a Day 19 → **URGENTE**") — è un confronto numerico, non AI;
3. posizione/stato di ogni PG da §1 (party diviso → un paragrafo per PG);
4. clock villain vicini alla soglia (es. Ritual ≥12/18 → warning canonico
   già previsto da `state_sync.py`).

Output: `campaign/next/brief-YYYY-MM-DD-DM.md` (tutto) +
`campaign/next/teaser-YYYY-MM-DD.md` (filtrato con `visibility.py`,
spoiler-safe, riusa il tono di `session_recap.py`). Onestà: questo è un
*aggregatore intelligente*, non uno sceneggiatore — le "evoluzioni"
inventate stanno solo nel modulo opzionale §5.5.

---

## §4 — Perché branch-per-gruppo funziona (e i suoi costi reali)

**Funziona** perché il repo separa già nettamente *prep riusabile* (archi,
Bestiario, mappe, skills — su `main`) da *stato vivo* (`state.md`,
`sessions/`, `recaps/` — per gruppo). Il modello:

- `main` = libreria: mai canone di gruppo; CI e revisioni continuano qui.
- `campaign-group-rumblingstone-dm-gianfranco` = branch **long-lived** del
  gruppo: tutti i commit del wizard finiscono qui. Non si mergia MAI in main.
- aggiornamenti di prep (nuovi statblock, mappe, fix script) fluiscono
  `main → branch gruppo` con `git merge main` periodico.

**Costi onesti da mettere in conto**:
1. *Drift*: se il DM dimentica il merge periodico, il branch resta indietro
   sugli script. Mitigazione: `doctor` mostra `git rev-list --count
   <branch>..main` e avvisa se > soglia; `session next` lo ricorda.
2. *Conflitti*: se `main` tocca `state.md`/template (non dovrebbe, ma è
   successo — le revisioni ARC lo modificano), il merge confligge.
   Mitigazione di processo: dopo l'adozione, su `main` `state.md` diventa
   di fatto un template di riferimento e le revisioni di canone giocato si
   fanno sul branch gruppo. Va scritto nel Playbook §7 (lotto F).
3. *Un solo branch attivo per checkout*: chi fa prep su `main` e gioca sul
   branch deve cambiare branch. Mitigazione documentata: `git worktree`
   (due directory, zero switch) — solo documentazione, nessun tooling.

---

## §5 — Lotti di lavoro (con stime e gate)

Stime in ore di lavoro focalizzato, incluse le prove. Ordine = dipendenze.

### Lotto A — Fondazioni: ADR-0007 + branch guard + scheletro CLI *(≈3-4h, rischio basso)*
- A1 ADR-0007 (bozza in §6) discussa e accettata dal DM.
- A2 `scripts/campaign_branch.py`: legge/crea `campaign/group.yaml`
  (`group: rumblingstone-dm-gianfranco`), verifica branch corrente,
  crea `campaign-group-<nome>` se manca (riusando la logica di
  `new-campaign-group.sh`, senza duplicarla: la parte comune migra in
  funzioni condivise o lo .sh viene invocato).
- A3 `dm.py session` (start/end/next/recap) registrato, sub-help, `doctor`
  esteso (branch, group.yaml, marker presenti in state.md).
- **Gate**: su `main`, `dm.py session end` rifiuta con messaggio chiaro.

### Lotto B — Wizard fine-sessione *(≈6-8h, rischio basso-medio)*
- B1 `scripts/session_wizard.py`: Q&A stdlib con default intelligenti
  (data odierna, N = ultimo+1, presenti = ultimi presenti), sezioni lunghe
  via `$EDITOR` o multi-riga; `--from-draft` importa il live-draft §3.
- B2 Output conforme al template; validazione minima (XP numerici, clock
  `X → Y` ben formati così `state_sync.py` li riconosce — il wizard
  *garantisce* il formato che oggi il DM deve ricordare a memoria).
- B3 Commit #1 automatico post-scrittura.
- B4 Modalità `--non-interactive --answers file.yaml` (serve ai test E2E).
- **Gate**: una sessione fittizia completa produce un file indistinguibile
  dal worked example del Playbook §4.bis.

### Lotto C — Apply engine per `state.md` *(≈8-12h, **il lotto rischioso**)*
- C1 Migrazione una-tantum: inserire i marker `auto:begin/end` in
  `state.md` (commit dedicato sul branch gruppo; su `main` si aggiornano
  solo `templates/state-blank.md` + Playbook).
- C2 `scripts/state_apply.py`: parser delle regioni marcate; consuma le
  proposte di `state_sync.py` (refactor: `state_sync` espone le proposte
  anche come dati strutturati — oggi solo markdown umano — mantenendo
  identico l'output testuale attuale);
  per ogni proposta → diff colorato → `[y/n/e]` → applica.
- C3 Append automatico changelog §8 (`data — Session N: one-liner`).
- C4 Fail-safe: qualsiasi anomalia di parsing → nessuna scrittura, si
  ricade nel report-only attuale (mai "meglio di niente" sul canone).
- **Gate**: property test — per ogni input, il testo FUORI dai marker è
  byte-identico prima/dopo. Questo è il contratto di sicurezza.

### Lotto D — Visibilità per-PG *(≈5-7h, rischio basso-medio)*
- D1 Template sessione v2 (blocchi `## Split — <PG> @ <luogo>` +
  `Visto da:`); wizard li chiede quando il DM dichiara party diviso.
- D2 `scripts/visibility.py` (policy unica, §3) + unit test.
- D3 `session_recap.py --pg NOME` → recap per-PG in `campaign/recaps/pg/`;
  senza flag, output identico a oggi (golden test di regressione).
- **Gate**: con la sessione-tipo attuale (Tordek/Hella/Artemis divisi), il
  recap di Tordek non contiene una riga dei blocchi di Hella/Artemis.

### Lotto E — Brief prossima sessione *(≈5-6h, rischio basso)*
- E1 `scripts/next_session.py`: aggregatore deterministico (§3) → brief DM
  + teaser player.
- E2 Tracciamento hook "consumati": un hook citato nel Summary/decisioni di
  una sessione successiva esce dal brief (euristica per matching testuale;
  onestà: sarà imperfetta → il brief marca i dubbi con `?` invece di
  tacerli, e il DM può chiudere hook a mano con `- [x]`).
- **Gate**: con lo stato attuale del repo (March Day 19, finestre ARC-09),
  il brief segnala P1A/P1B come imminenti — verificabile a mano oggi stesso.

### Lotto E-bis (OPZIONALE, decisione DM) — Evoluzioni via LLM *(≈4-6h + costi API)*
- Adapter `--llm` per `session next`: prompt = brief deterministico +
  state.md → 3 proposte di evoluzione narrativa marcate `⚠ NON-CANONE
  (generato)`. Mai scritte in state.md; file separato in `campaign/next/`.
- Onestà: introduce dipendenza (API key, rete), non-determinismo e rischio
  di allucinazioni sul canone. Per questo: spento di default, output
  quarantenato, e l'intero resto del piano NON dipende da questo lotto.
  In alternativa a costo zero: il DM usa gli agenti già configurati
  (skills del repo) passando il brief come prompt — nessun codice nuovo.

### Lotto F — Test, CI, documentazione *(≈6-8h, rischio basso)*
- F1 Suite `tests/` (unittest stdlib, runnabile con `python3 -m unittest`):
  - unit: wizard (answers-file), visibility, parser marker, apply engine;
  - E2E: repo git temporaneo (fixture) → `session end --non-interactive`
    → assert su file sessione, state.md, ledger, 2 commit, branch giusto;
  - golden: recap e brief confrontati con file attesi;
  - property (C): fuori-marker byte-identico; idempotenza (2° run = no-op).
- F2 Workflow CI (`.github/workflows/`): lint + suite su push (gira su
  `main` e sui branch `campaign-group-*` e `claude/*`).
- F3 Playbook: §4 riscritto attorno a `session end` (la procedura manuale
  resta come appendice "cosa fa il wizard sotto il cofano"); §7 aggiornato
  con la policy merge main→gruppo e il worktree tip; AGENTS.md aggiornato.
- **Gate**: `dm.py doctor` verde; CI verde; un "collaudo al tavolo" reale
  alla prima sessione utile (come da tradizione dei piani di questo repo).

**Totale stimato**: ≈33-45h senza E-bis. Nessun lotto blocca il gioco: il
flusso manuale attuale resta funzionante in ogni momento (R5).

---

## §6 — Bozza ADR-0007 (da estrarre in `plans/adr/` al via del Lotto A)

**Titolo**: Scritture di canone da parte degli script — permesse con triplo vincolo
**Contesto**: la regola storica "gli script non scrivono mai
`state.md`/`sessions/`" nasce per proteggere il canone da automazioni
cieche (e ha già un'eccezione di fatto: `update_xp.py` scrive il ledger).
Il costo è che il DM ricopia a mano modifiche meccaniche già calcolate.
**Decisione**: gli script POSSONO scrivere canone solo se, insieme:
(1) branch corrente ≠ `main` (guardia `campaign_branch.py`);
(2) il DM ha confermato il diff esatto (o modalità `--non-interactive` nei
test, mai nel flusso reale);
(3) dentro regioni marcate `auto:begin/end` per `state.md` (i file
sessione, creati ex-novo dal wizard, non necessitano marker);
(4) con commit git immediato prima e dopo l'applicazione.
**Conseguenze**: il canone resta curato dal DM (conferma per blocco);
l'undo è sempre `git revert`; la prosa è strutturalmente intoccabile;
`state_sync.py` resta utilizzabile in modalità solo-report.

---

## §7 — Rischi e mitigazioni (tabella onesta)

| # | Rischio | Prob. | Impatto | Mitigazione |
|---|---|---|---|---|
| R1 | Regex/parsing sbaglia un'applicazione su state.md | media | alto (canone) | marker + conferma per blocco + fail-safe C4 + property test + commit pre-apply (revert a costo zero) |
| R2 | Drift branch gruppo ↔ main / conflitti merge | media | medio | doctor avvisa; policy Playbook §7; state.md non più editato su main |
| R3 | Wizard troppo lungo a fine serata (il DM è stanco, sono le 23:30) | media | medio (adozione) | default ovunque, invio=salta, `--from-draft`, si può interrompere e riprendere (il file resta, gli step 5-8 sono rilanciabili — idempotenza R2) |
| R4 | Tag visibilità sbagliato → spoiler nel recap di un PG | bassa | alto (fiducia al tavolo) | default = NON esportare i blocchi Split ambigui; test dedicati; anteprima a schermo prima di scrivere i file per-PG |
| R5 | Hook "consumati" rilevati male (E2) | alta | basso | il brief marca i dubbi, mai rimozione silenziosa; chiusura manuale `- [x]` |
| R6 | LLM inventa canone (solo E-bis) | alta | alto se non contenuto | quarantena `NON-CANONE`, opt-in, mai scrittura in state.md |
| R7 | Violazione strisciante di ADR-0002 (logica dentro dm.py) | media | medio (manutenzione) | tutta la logica in script nuovi dedicati; dm.py solo dispatch; review checklist |

---

## §8 — Domande aperte per il DM (bloccanti solo dove indicato)

1. **Nome branch** (bloccante Lotto A): confermi
   `campaign-group-rumblingstone-dm-gianfranco`? (Coerente con lo schema
   `campaign-group-<nome>` esistente; il suffisso `-dm-<nome>` permette in
   futuro più DM sullo stesso gruppo.)
2. **Migrazione marker** (bloccante Lotto C): ok inserire i commenti
   `<!-- auto:... -->` in `state.md` sul branch gruppo? (Invisibili nel
   rendering, ma presenti nel sorgente.)
3. **Lotto E-bis LLM**: dentro o fuori? (Raccomandazione: fuori dalla v1;
   il brief deterministico + skills esistenti copre l'80% del valore a
   costo e rischio zero.)
4. **Recap per-PG**: consegna come file markdown da girare a mano, o serve
   anche la veste Homebrewery (`.hb.md`) come per i recap attuali?
   (Non bloccante: si aggiunge dopo, riusa `hype_homebrew.py`.)
5. **Lingua wizard**: italiano, coerente col resto? (Assunto: sì.)

---

## §9 — Criterio di successo del piano

Alla terza sessione reale gestita col nuovo flusso:
- tempo di chiusura post-sessione ≤ 10 min (oggi: 10 min *dichiarati* nel
  Playbook, ma con ricopiatura manuale del diff);
- zero interventi manuali su §0/clock/changelog di state.md;
- zero spoiler negli artefatti per i player (verifica DM);
- `main` senza alcun commit di canone di gruppo;
- il DM non è tornato spontaneamente al flusso manuale (il vero KPI di
  un tool per una persona sola).
