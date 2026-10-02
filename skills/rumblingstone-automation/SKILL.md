---
name: rumblingstone-automation
description: >
  DM automation for the RumblingStone repo — the single CLI `scripts/dm.py`
  and the session-state pipeline on group branches (ADR-0007). Use WHENEVER
  closing or preparing a session, updating campaign/state.md, generating
  recaps (group or per-PG), briefs, teasers, handouts, Homebrewery output,
  or running/choosing any script in scripts/. Trigger on: "dm.py",
  "fine sessione", "chiudi la sessione", "session end", "wizard",
  "prossima sessione", "brief", "teaser", "recap", "recap per-PG",
  "state.md", "March Clock", "XP ledger", "branch di gruppo",
  "campaign-group", "Homebrewery", "hype", "handout", "dossier",
  "doctor", "doctor --ci", "prep incontro", "suggest_encounter",
  "genera il booklet", "prepara la serata", "corredo", "corredo della serata",
  "stampa la sessione", "dm.py corredo", "validate_corredo".
---

# RumblingStone — Automazione DM (`dm.py` e pipeline di sessione)

Tutta l'automazione DM passa da **un solo entrypoint**:
`python3 scripts/dm.py <sottocomando>` (solo orchestrazione, ADR-0002).
Gli script sottostanti restano usabili direttamente e usano solo stdlib.

**Fonti di verità (non duplicare, puntare):**

| Cosa | Dove |
|---|---|
| Tool map completa (tutti gli script: scopo, parametri, I/O) | `scripts/README-automation.md` |
| Guida operativa per nuovi DM (~15 min) | `campaign/DM-QUICKSTART-NUOVI-DM.md` |
| Workflow manuale pre/durante/post sessione | `campaign/DM-CAMPAIGN-PLAYBOOK.md` (§2, §4, §7) |
| Gruppo nuovo che rigioca la campagna | `python3 scripts/dm.py gruppo nuovo`: un modulo a domande, nessun YAML a mano (Playbook §7.2) |
| Perché il CLI è orchestrazione-only | `plans/adr/ADR-0002-cli-unica-dm-orchestratore.md` |
| Perché i layout `.hb.md` sono generati, mai editati | `plans/adr/ADR-0003-markdown-master-layout-generati.md` |
| Quando gli script possono scrivere canone | `plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md` |
| Contratti verificati (31 test in CI) | `scripts/tests/` |

## ⚖️ Regole non negoziabili (ADR-0007, triplo vincolo)

### 🔴 Prima di tutto: il canone di campagna ha **tre** master, non uno

| File | Cosa ci sta | Come ci si scrive |
|---|---|---|
| `campaign/state.yaml` | i fatti tabellari di §0, §1, §2.4, §3, §4, §6, §7.E | **qui**, poi `python3 scripts/render_state.py` |
| `campaign/state.md` | §2 waypoint e orda, §5, §7, i banner dei due tempi, la prosa | qui, **fuori** dai marcatori `gen:state:` |
| `campaign/state-changelog.md` | lo storico | append-only, in coda |

⚠️ `state.md` è **insieme master e vista**: dentro `<!-- gen:state:NOME -->` il
contenuto è generato da `state.yaml`. Modificarlo lì non è «una modifica che poi
si rigenera»: è una modifica che **sparisce** al prossimo `render_state.py`,
senza errore e senza avviso. `render_state.py --check` gira in CI e diventa
rosso, ma la modifica è già persa.

Non esiste una via `state.md` → `state.yaml`. Il flusso è a senso unico.

Gli script scrivono canone (i tre file sopra, `campaign/sessions/*`)
SOLO se valgono **tutte insieme**:

1. **Branch**: mai su `main`/`master` — il canone vivo di un gruppo sta su
   `campaign-group-<nome>` (guardia `campaign_branch.py`; il branch non si
   mergia mai in `main`).
2. **Conferma**: il DM vede e conferma il **diff esatto, blocco per
   blocco** (`--yes` esiste solo per test/CI).
3. **Regioni marcate**: in `state.md` **non resta nessuna regione `auto:`**
   (decisione D14): tutto ciò che la macchina scrive passa da `state.yaml` e
   torna come vista generata. L'unica regione `auto:` è `changelog`, in
   `state-changelog.md`, append-only. Dentro `state.yaml` la macchina scrive
   **quattro** cose: `march_clock.giorno_corrente`, il `clock` dei villain, e il
   loro `stato` su morte e fuga. Tutto il resto — prosa, §1 party, alleanze —
   resta **proposta a video**, e la proposta dice **in quale dei tre master** va.
   **Da dove le legge** (lotto 4e): dal front-matter `delta:` del log, che
   scrive il wizard e che nomina i villain per `png_id`. Un log senza
   front-matter ricade sulla regex di `state_sync`, che conosce solo i nomi
   scritti nel suo sorgente (3 clock su 9, 5 morti su 13 il 2026-09-24). Un
   delta che non torna con lo stato di oggi non scrive **niente**.
   ⚠️ `state_apply` scrive `stato` ma **non** `reversibile`: se il canone prevede
   un ritorno lo dice il DM, e la regola R9 di `validate_state` glielo chiede.
4. **Reversibilità**: i tre master puliti in git prima dell'apply, commit
   dedicato subito dopo; l'undo è sempre `git revert`.

Un agente che "aggiorna state.md" a mano fuori dalle regioni marcate, o dentro
una regione `gen:state:` invece che in `state.yaml`, o su `main`, sta violando
l'ADR: fermarsi e proporre il flusso corretto.

## Flusso di sessione (`dm.py session`)

| Comando | Cosa fa | Script sottostanti |
|---|---|---|
| `session end` | wizard guidato fine-sessione (senza `--session`): log canonico in `campaign/sessions/` con in testa il **front-matter dei delta** (villain per `png_id`, risolti contro `state.yaml` mentre il DM risponde), blocchi `## Split — <PG> @ <luogo>` se il party si divide, poi ledger XP → diff di `state.yaml` e della vista → conferma → commit | `session_wizard` + `update_xp` + `state_apply` |
| `session next [--hype]` | brief ⚠️SOLO-DM (finestre quest, clock ≤2 tick, hook aperti, `❓ forse già giocato`) + teaser player spoiler-safe in `campaign/next/` | `next_session` |
| `session recap [--pg <PG>]` | recap di gruppo o personale per-PG (visibilità: i blocchi Split li vede solo quel PG; `## DM notes (private)` non esce MAI) | `session_recap` + `hype_homebrew --pg` |
| `session status` / `session branch --group <nome>` | stato branch/guardie · setup branch di gruppo + `campaign/group.yaml` | `campaign_branch` |

Setup una-tantum di un nuovo gruppo: `dm.py session branch --group <nome>`
poi `state_apply.py --migrate --commit` (marca la regione `changelog` di
`state-changelog.md`; in `state.md` non c'è più niente da marcare).

## Il corredo della serata (norma, dal 2026-09-25)

Quando il DM dice **«genera il booklet»**, «prepara la serata» o «stampa la
sessione», l'agente non consegna un volume: consegna **il corredo intero** della
serata, riveduto con le regole in vigore, senza che il DM debba elencarlo. Vale
lo stesso per «genera i prompt» o «genera le immagini»: si fa la parte
immagini del corredo, con la sua procedura.

La norma nasce da una misura. Il 2026-09-25 la serata della resurrezione di
Hella aveva sette pezzi sparsi in tre cartelle, e nessun documento diceva quali
fossero: il booklet del DM aveva la sua tecnica, il resto lo teneva insieme la
memoria di chi l'aveva scritto.

| Pezzo | Obbligatorio | Si scrive con | Chi lo controlla |
|---|---|---|---|
| **booklet del DM**: regia, cassetta, i master che si giocano (due per una serata normale, anche il terzo per una sessione lunga) in ordine di gioco con le appendici A4. Nessun foglio ✉: la regia li cita per titolo | sì | `rumblingstone-editoria` §2-bis | `validate_booklets`, `dm.py volume` |
| **volume dei fogli ✉**: tutte le pagine da consegnare, solo capitoli `player`. È l'unico posto dove un foglio si stampa | sì | `rumblingstone-narrative-style` | `validate_corredo`: nessun capitolo `dm` qui, nessun foglio ✉ altrove |
| **volume di approfondimento** | solo se non ristampa un capitolo del booklet | come il booklet | `validate_corredo`: lo stesso capitolo in due volumi è rosso |
| **echi per PG**: un file per ogni PG al tavolo | sì | `consequence-echoes.md`, regola 3: un eco non anticipa | `validate_corredo` per la presenza; la regola 3 no (vedi sotto) |
| **carte e handout**: doni, schede, preghiere, tavole, documenti | quelli che il master consegna | `narrative-style`, e `rumblingstone-indagine` per un documento d'indagine | `validate_corredo`: esistono e stanno nel volume dei fogli |
| **prompt delle immagini**, con la sezione «Confronto immagine-scheda» | se la serata ha immagini nuove | `rumblingstone-art-direction` §7-bis | `validate_corredo`: ogni blocco `img` ha il suo file e la sua riga nel confronto |
| **PDF da stampa** di ogni volume | sì | `typst` via `dm.py corredo --stampa` | `validate_corredo --pdf`: 0 righe sovrapposte, 0 testo a meno di 30 pt dal bordo, box ≤ 12 righe, **0 apparato di lavoro** (ADR-0070); `validate_booklets --stampa` |

Il corredo si **dichiara** in un file `<SERATA>.corredo.json` accanto al booklet
del DM (contratto: `scripts/schemas/corredo_serata.schema.json`, versionato e
solo additivo). Esemplare: `07_il Portale Della Forgia Eterna/homebrew/sessione-resurrezione-mille-anni/ARC07-SERATA-RESURREZIONE.corredo.json`.

**In ordine**, quando il DM lo chiede:

1. si scrivono o si rivedono i pezzi con le skill della tabella, e la
   self-check di `narrative-style` si esegue su ogni pagina ✉ (regola G4);
2. si aggiorna il `.corredo.json`: un foglio nuovo entra nel manifest dei fogli
   **e** nel corredo;
3. `python3 scripts/dm.py corredo <SERATA>.corredo.json --stampa`: controlla i
   pezzi, e se ne manca uno si ferma senza compilare niente; poi fa ogni volume
   con la catena di `volume` (prosa, lingua, manifest, colophon, schermo,
   stampa), rifà il `.hb.md`, e misura i PDF;
4. si guardano a vista le pagine con le mappe (`rumblingstone-editoria` §4, «Il
   controllo a vista»): nessuna misura sa se una mappa si legge;
5. si consegna solo con il passo 3 verde. PyMuPDF è fra le dipendenze di
   sviluppo (`pip install -r requirements-dev.txt`); se manca, la misura del
   PDF è **saltata e dichiarata**: si dice al DM, non si scrive «0
   sovrapposizioni».

**Una pagina si stampa una volta**, e **l'apparato di lavoro non va in stampa**
([ADR-0070](../../plans/adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md)):
i metadati del repo stanno in `<!-- apparato -->`, i rimandi si scrivono
`DEF-N` e l'esportatore li traduce nel capitolo del volume. Per ARC-07 il
booklet della serata stampa `DEF-2`, `DEF-3` e `DEF-4`; il volume del −1000 è un
libro a sé, fuori da questo corredo.

Un box read-aloud oltre le 12 righe si spezza in battute, nella forma di Balvar
in `DEF-4`, e non si taglia: il controllo lo misura sul testo **senza lo
storico**, cioè su quello che si stampa (ADR-0069).

⚠️ **Quello che il controllo non vede.** Se un eco anticipa una scelta
(regola 3 degli echi), se una pagina ✉ è scritta bene, se la riga «✉ Si
consegna qui» del master corrisponde al foglio giusto: sono giudizio, e restano
a chi scrive e al DM. E il corredo è preparazione, non canone: cosa è successo
al tavolo si chiude con `dm.py session end` sul ramo del gruppo (ADR-0007).

## Altri sottocomandi

- `prep --el N --env <amb>`: proposte incontro+mappa+loot (non scrive nulla).
- **Incontri che non si ripetono** (ADR-0034):
  `suggest_encounter.py --el N --con-generatore` pesca **in parte** dal
  catalogo e in parte da creature costruite sul momento dalle tabelle SRD;
  `--piu-cattivi` rende più dura la **sola** parte generata (template *Advanced*
  di PF1e senza alzare il GS), mai i mostri veri del catalogo. Per costruirne
  una sola: `genera_creatura.py --gs N --ruolo <bruto|schermagliatore|tiratore|
  comandante|controllore|blaster>` (`artigliere` resta come alias del vecchio
  nome). Con `--classe` si aggiunge `--funzione <controllore|blaster|supporto|
  utilita>`: il ruolo dice **come combatte**, la funzione **cosa fa con gli
  incantesimi**, e le liste vanno per **lista di classe** — mai per tradizione,
  perché chierico e druido sono tutti e due divini e hanno liste diverse.
  `--incantesimi pf1e` innesta gli incantesimi PF1e senza equivalente 3.5 (lo
  accende anche `--piu-cattivi`). ⚠️ Non scrive mai dentro `Bestiario/`:
  propone, e nel canone copia il DM. Se nel catalogo c'è già qualcosa di simile,
  **potenziare** è meglio → skill `npc-villain-boosting`.
- `bestiario <azione> [flag]`: i cinque script delle creature da un solo
  ingresso, con i flag passati allo script. `estrai` → `extract_statblocks`,
  `deriva` → `derive_statblocks`, `attributi` → `genera_attributi`,
  `creatura` → `genera_creatura`, `conformita` → `conformita_statblocchi`.
  `dm.py bestiario creatura --help` stampa l'aiuto dello script, e il codice
  d'uscita è quello dello script. Gli script restano invocabili per nome.
- `post --session <file>`: flusso manuale legacy (ledger + report-only).
- `recap --hype` · `handout --tipo T --da <file>` · `dossier` (⚠️ solo DM) —
  vesti Homebrewery V3: i `.hb.md` sono **generati**, mai editati a mano.
- `hype setup|start|docker`: Homebrewery self-hosted (ADR-0004).
- `booklet <manifest.json> [--format html|hb|both] [--pdf|--pdf-all]`: booklet «pergamena» da manifest (**ADR-0013**): HTML autonomo, `.hb.md` V3
  per il self-hosted, e **PDF A4 per scheda** (prefissi `pg-`/`dm-`).
  Standard obbligatorio: file del gruppo SEPARATO e spoiler-free (titolo
  evocativo, mai il nome dello scontro), hint/echi per-PG, canone giocato
  annotato nei master. 📘 **Procedura completa**:
  `docs/guides/GUIDA-BOOKLET-E-PDF.md` (prerequisiti, manifest, container
  opzionali, troubleshooting, checklist di consegna).
- `corredo <SERATA>.corredo.json [--stampa]`: l'intero corredo della serata
  (sezione qui sopra). Controlla i pezzi con `validate_corredo.py`, fa ogni
  volume con la catena di `volume` e il `.hb.md`, poi misura i PDF.
- `maps render|validate`: per il *contenuto* delle mappe caricare
  `rumblingstone-mapmaking` (questa skill copre solo l'invocazione).
- `skills build|sync`: rebuild dei mirror per-agente (generati, gitignored).
- `doctor [--ci]`: diagnosi ambiente: primo comando se qualcosa non va.

## Confini con le altre skill

- Contenuto/qualità mappe → `rumblingstone-mapmaking`.
- Tracciatura piani/lotti/ADR → `rumblingstone-plans`.
- Cosa scrivere nel recap/brief (stile) → `rumblingstone-narrative-style`;
  questa skill governa solo *come* generarli e *dove* finiscono.
- Verità di campagna (PG, archi, coerenza) → `rumblingstone-campaign`.
