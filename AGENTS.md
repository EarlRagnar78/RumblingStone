# AGENTS.md — RumblingStone Campaign Repo

**Project**: *RumblingStone*, a custom D&D 3.5 campaign set in the Forgotten Realms,
based on *Red Hand of Doom* (Jacobs & Wyatt, 2006). Content is privately owned.
**System**: D&D 3.5 Edition (d20 SRD / OGL). Non-SRD content is privately held.
**Setting**: Faerûn, 1372 DR. Adapted from the Elsir Vale to the Dalelands region.

---

## What This Repo Contains

```
Bestiario/                   # STANDARD library of monsters, villains & NPCs (T-D12)
├── mostri/                  # generic units/monsters, one statblock per file (-crN.md)
├── villain/                 # unique antagonists (dossier folder + statblock)
├── png/                     # unique allies/neutrals (dossier folder/file + statblock)
├── pregen-pcgen/            # historical sources: PCGen .pcg + HTML/PDF exports (read-only)
└── tokens/                  # webp art/tokens for monsters & NPCs

campaign/
├── DM-CAMPAIGN-PLAYBOOK.md  # DM operational guide (workflow + examples + reset)
├── state.md                 # Living world state (§0 dashboard first)
├── sessions/                # Session logs (YYYY-MM-DD_session-N.md)
├── recaps/                  # Generated recaps (group and per-PC)
├── ai-media-prompts/        # Image/audio prompt masters (ADR-0015)
├── templates/               # Blank state + session templates for new groups
└── lore/                    # House rules, premise (shared) + chronicle (per group), DM/player strategy

# NPCs, locations and encounters do NOT live under campaign/. NPC and villain
# cards are in Bestiario/png/ and Bestiario/villain/; locations and encounters
# are inside the arc modules (00_… to 09_…), with their tactical maps.

skills/    # le diciotto skill: vedi «Inventario completo» più sotto

10-stand-alone/Il-Drappo-di-Tarsilia/  # self-contained PF1e module set in Golarion —
           # shares the race SYSTEM with arc 09's Palio and nothing else
           # (no Faerûn, no RHoD, no campaign PCs). Start at 00-HUB-E-QUICKSTART-DM.md

plans/     # work-plan archive: INDEX.md (status + % + gates), CHANGELOG.md, adr/
scripts/   # DM automation — single entrypoint: python3 scripts/dm.py
converters/ # content converters (pdf→md, html→md, img→webp) — NOT the DM automation
```

`.hb.md` files are generated Homebrewery layouts (`plans/adr/ADR-0003`):
regenerate via `dm.py recap --hype` / `dm.py handout`, never edit by hand.

> **Agenti e DM, per ripartire: prima [`MEMORIA.md`](MEMORIA.md)**, la
> memoria del lavoro generata da `python3 scripts/memoria.py`
> ([ADR-0087](plans/adr/ADR-0087-la-memoria-del-lavoro-e-generata.md)).
> Non si scrive a mano: si corregge la fonte che indica, poi si rigenera. E
> niente di utile resta nello scratchpad di una sessione: prima di chiudere
> entra nel repo.
>
> **Il lavoro che non è ancora su main** (PR aperte, rami, cartelle dei thread)
> sta in [`plans/LAVORO-IN-CORSO.md`](plans/LAVORO-IN-CORSO.md), che si
> rigenera con `python3 scripts/lavoro_in_corso.py --fetch` dal registro curato
> `plans/lavoro-in-corso.json`; in Claude Code e in OpenCode il comando è
> `/lavoro-in-corso`
> ([ADR-0157](plans/adr/ADR-0157-il-lavoro-fuori-da-main-ha-una-pagina-dal-vivo.md)).
>
> **La storia dietro una scelta** (regressione, soluzione già provata) sta in
> [`plans/MEMORIA-STORICA.md`](plans/MEMORIA-STORICA.md): si cerca con
> `python3 scripts/memoria_storica.py --pr N | --adr N | --tema T | parole`.
> Ogni PR che aggiunge una riga a `plans/CHANGELOG.md` aggiunge anche una
> voce lì (decisioni, misure, questioni aperte: la CI la esige), e chi
> toglie una riga dalla memoria delle sessioni la archivia lì prima
> ([ADR-0127](plans/adr/ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md)).
> Il lavoro che non finisce in una PR (scelta su card, dato verificato, thread
> che si risolve) lascia la sua voce nella coda del thread, e
> `python3 scripts/memoria_coda.py DIR --thread "Titolo"` dice se manca
> ([ADR-0138](plans/adr/ADR-0138-la-coda-della-memoria-storica-ha-un-cancello.md)).
> Prima di togliere righe dalla memoria del progetto e prima di un merge,
> `python3 scripts/memoria_custode.py verifica` dice quali righe tolte non
> sono archiviate (`archivia` le scrive in coda), e l'agente
> `custode-memoria` risponde da memoria del progetto, file storico e coda
> ([ADR-0151](plans/adr/ADR-0151-la-memoria-del-progetto-ha-uno-specchio-e-un-custode.md)).

> **DMs: start with `campaign/DM-CAMPAIGN-PLAYBOOK.md`**: session workflow,
> worked examples, the `§0` dashboard and the new-group reset
> (`python3 scripts/dm.py gruppo nuovo`).

---

## Skills

**Il principio, prima della tabella.** Prima di produrre qualunque cosa,
chiediti **chi la leggerà** e **in che forma uscirà**: quelle due risposte, non
l'argomento, scelgono la skill. Un ADR e un read-aloud sono entrambi prosa
italiana e seguono norme **opposte** (ADR-0035). La tabella qui sotto
**illustra** il principio, non lo esaurisce: se il tuo compito non c'è, applica
la domanda. Le skill marcate **obbligatorie** vanno caricate anche se il DM non
le nomina.

### 🥇 REGOLA D'ORO DELLA PROSA — una skill non è il suo `SKILL.md`

> **Prima di scrivere una riga di prosa di gioco, o di misurarla, o di dire che
> uno standard manca: apri i `references/` e leggili. Tutti quelli che la
> riga della tabella ti assegna, per intero. Il `SKILL.md` è l'indice, non la
> norma.**

Le sei regole, ordinate per il momento in cui scattano, con comando,
verificatore e i conflitti fra loro (la quinta viene prima della prima), stanno
in [`skills/REGOLE-DORO.md`](skills/REGOLE-DORO.md)
([ADR-0061](plans/adr/ADR-0061-le-regole-d-oro-sono-un-dato-ordinato-per-momento.md)).
Perché esistono: [ADR-0056](plans/adr/ADR-0056-una-norma-senza-misura-non-esiste.md)
(dalla prima alla quarta), [ADR-0058](plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md)
(la quinta), `plans/CHANGELOG.md` alle righe del 2026-09-18 e del 2026-09-20
(la quarta e la sesta).

1. **`G1` · Leggi i `references/`**, non il loro elenco. Sono la norma; il
   `SKILL.md` è la mappa.
2. **`G2` · Misura prima di affermare.** «Questo standard manca», «lo stile non è
   arrivato qui», «questa forma non la usa nessuno» sono affermazioni
   *misurabili*: `python3 scripts/misura_craft.py [--box|--copertura|--spotlight]`.
   Un'affermazione sullo stato del repo senza una misura accanto non vale.
3. **`G3` · Se introduci una norma, registrala.**
   [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) elenca
   ogni norma con **chi la misura**, o con **il perché nessuno la misura**.
   Il gate `python3 scripts/validate_norme_editoriali.py` boccia un file
   normativo non registrato e un rimando a uno strumento che non esiste.
   Introdurre uno standard non è aver fatto il lavoro: **una norma nuova arriva
   con il suo lotto di applicazione e la sua misura, o non è arrivata.**
4. **`G4` · Prima di consegnare prosa di gioco, esegui la self-check della skill**
   *(il quarto obbligo)*. Non «tienila a mente»: **eseguila**, domanda per
   domanda. Dove la domanda è misurabile, la risposta è un **comando**, non
   un'impressione.

   | Domanda della self-check | Come si risponde |
   |---|---|
   | 1 · Quale pilastro guida la scena? *(se «tutti» → riscrivi)* | `misura_craft` → `PILASTRO dichiarato (lead/support)` |
   | 2 · Almeno un PG agisce, sceglie o riceve un'eco? | `--spotlight` (indicatore) |
   | 3 · Ho scritto o fatto riemergere un'eco? | congegno `eco / conseguenze a distanza` |
   | 4 · Sopravvive senza i numeri di serie — niente nomi presi in prestito? | **giudizio**, nessuna misura |
   | 5 · Ogni PNG nominato ha un *Want* che non riguarda i PG? | congegno `grigio politico` |
   | 6 · La rete d'indizi è ridondante, e la risposta sbagliata porta comunque da qualche parte? | congegni `nodo d'indizio` + `modi di fallimento` |
   | 7 · **Qualche box è oltre il tetto?** *(→ taglia; vince il tetto)* | `misura_craft --box`, colonna `>12 righe` |
   | 8 · Ho corretto ciò che la misura segnala, e rimisurato? Su un file che c'era già, il DM approva le modifiche una per una? | `ciclo_prosa.py segnala` (o `lotto`) → `misura` a ogni giro → `revisione` → `applica [--auto]` ([ADR-0077](plans/adr/ADR-0077-revisione-a-due-giri.md)) |

5. **`G5` · Prima di caricare, applica l'algoritmo a cinque domande di
   [`skills/ORCHESTRAZIONE.md`](skills/ORCHESTRAZIONE.md)**: canone (L0, sempre),
   chi legge (L1: `narrative-style` **o** `prosa-documenti`, mai entrambe),
   che cosa (L2), in che forma (L3), che gesto (L4). Solo la seconda ha una
   risposta sola; dalla terza in poi si somma, e la consultazione (SRD, lore)
   si apre per un **fatto**, mai per decidere. Il bersaglio è *zero omissioni
   di ciò che è obbligatorio*, e l'obbligo vero è su **L0-L2**: L4 e LR **non**
   si caricano per sicurezza.
6. **`G6` · Prima di modificare qualunque cosa, esegui
   `python3 scripts/fase1.py <bersagli>`.** I quattro passi, in
   **quest'ordine**, con una regex nuova come ultima risorsa: (1) la misura già
   qualcuno? il [registro delle norme](skills/REGISTRO-NORME-EDITORIALI.md), e
   se sì si riusa (*una norma, un rilevatore*); (2) quali skill aprire?
   [`skills/ORCHESTRAZIONE.md`](skills/ORCHESTRAZIONE.md), e un file sotto
   `plans/` parla al repo, uno d'arco al tavolo; (3) cosa è archivio, superato,
   nome proprio, rimasto nei rami? i nomi da `Bestiario/` e `state.md`,
   `_SNAPSHOT-STORICO.md`, `ESCLUSI_NOME`, le matrici delle versioni,
   `plans/contenuti-nei-rami.json`; (4) da che numero parto? `misura_craft` sui
   bersagli veri, non su un campione. `fase1.py --check` **esce 1** se stai per
   modificare un archivio che il repo dichiara tale.

### Cosa carico, in base a cosa sto per fare

| Sto per… | Carico (obbligatorie in **grassetto**) |
|---|---|
| Scrivere prosa che un **giocatore** leggerà o sentirà — read-aloud, handout, dialoghi, teaser, recap, echi | **`rumblingstone-narrative-style`** e i suoi `references/` — **obbligatori e da leggere**, non da elencare: `italiano-nativo.md` (la lingua), `read-aloud-adulti.md` (le soglie: ≤12 righe, un nome proprio, niente parentesi), `editorial-standards.md` (le due forme prescritte), `style-pillars.md` (la *fusion rule*) |
| Scrivere un **documento del repo** — guida, ADR, piano, README, corpo di PR, messaggio di commit | **`rumblingstone-prosa-documenti`** ⚠️ regole opposte alla riga sopra: non mescolarle |
| Costruire o giocare un **caso**: mistero, indizi, enigma, ricomposizione, vicolo cieco | **`rumblingstone-indagine`** (sopra `narrative-style`, che resta il fondo) |
| Consolidare un beat d'arco in un **master definitivo** di qualità AP, o riscrivere e rifinire nello stile un master che c'è | **`rumblingstone-module-standard`** e i suoi `references/sviluppo-degli-incontri.md` (il developer) e `references/il-banco.md` (dove i PG comprano e vendono). Il master è DEF solo dopo i sette passi del suo «ciclo completo», compresi lettore e playtester a freddo di `rumblingstone-playtest` ([ADR-0075](plans/adr/ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md)) |
| **Impaginare**: booklet, manifest, PDF, tabella che si spezza, font, copertina, edizione da stampa | **`rumblingstone-editoria`** |
| **Far uscire qualcosa dal repo**: pubblicare, condividere, consegnare, colophon, licenza, OGL, Product Identity, «si può vendere» | **`rumblingstone-edizione`** — il gate d'uscita si passa *prima* di consegnare |
| Generare o correggere **immagini**: prompt, set coerente, seed/luce/camera, quando un'immagine si butta | **`rumblingstone-art-direction`** |
| Disegnare o esportare una **mappa** (Watabou, template, UVTT) | **`rumblingstone-mapmaking`** |
| **Potenziare** un PNG, un villain o un mostro | **`npc-villain-boosting`** — impone il tetto EL ≤ APL+4, il benchmark e il `Boost log:`. Mai potenziare in silenzio |
| Rispondere su **regole** 3.5 | `dnd-35-srd` (+ `pathfinder-1e-srd` per template semplici, benchmark GS, conversioni 3.5↔PF1e) |
| Rispondere su **lore** di Faerûn, 1372 DR | `forgotten-realms-lore` |
| Rispondere su **questa campagna**: PG, artefatti, archi, coerenza | **`rumblingstone-campaign`** + `campaign/state.md` + `references/campaign-coherence.md` |
| **Chiudere una sessione** o scrivere canone via script | **`rumblingstone-automation`** (unico ingresso: `python3 scripts/dm.py`) — vincolo triplo ADR-0007 |
| **Collaudare**: audit meccanico, dry-run, schede di feedback, alfa → beta → collaudato | **`rumblingstone-playtest`** |
| Aprire, aggiornare o chiudere un **piano di lavoro** | **`rumblingstone-plans`** (regola d'oro: piano + `INDEX.md` + `CHANGELOG.md` nello **stesso commit**) |
| **Debuggare l'infrastruttura**: `scripts/`, CI, pytest, renderer, `dm.py` | `rumblingstone-debugging` — **solo** infrastruttura, mai contenuto |

Due avvertenze che la tabella non può contenere:

- **Le righe si sommano.** Un handout è player-facing *e* impaginato: vuole
  `narrative-style` **e** `editoria`. Un modulo definitivo che contiene
  un'indagine vuole `module-standard` **e** `indagine`.
- **La coerenza batte lo stile.** Se `campaign-coherence` e una regola di
  stile si contraddicono, vince la coerenza (regola 8 più sotto).

### Inventario completo

Diciotto skill. L'elenco è **verificato da un gate**
([ADR-0041](plans/adr/ADR-0041-instradamento-delle-skill-con-un-gate.md)):
`validate_skills.py` fallisce se una directory con `SKILL.md` non è citata qui,
o se questo documento cita una skill che non esiste. Nessun agente «scopre»
queste skill da solo: è questa sezione a instradarli.

| Skill | Che cos'è |
|---|---|
| `skills/dnd-35-srd/` | meccaniche d20 SRD pure |
| `skills/pathfinder-1e-srd/` | regole PF1e, template semplici, benchmark GS, conversione 3.5↔PF1e |
| `skills/forgotten-realms-lore/` | canone di Faerûn, 1372 DR |
| `skills/npc-villain-boosting/` | quando e come potenziare PNG, villain e mostri |
| `skills/rumblingstone-campaign/` | questa campagna: PG, artefatti, archi, coerenza |
| `skills/rumblingstone-narrative-style/` | motore di stile a nove pilastri, protagonismo dei PG nel bene e nel male |
| `skills/rumblingstone-indagine/` | come si costruisce e si gioca un **caso**: nodo d'indizio, registro Acume/Perizia/Metodo (ADR-0022), ricomposizione, vicolo cieco |
| `skills/rumblingstone-prosa-documenti/` | come si scrivono i **documenti** del repo perché non suonino generati a macchina |
| `skills/rumblingstone-module-standard/` | standard di qualità dei master DEF (benchmark: Red Hand of Doom + AP Pathfinder 1e) |
| `skills/rumblingstone-editoria/` | layout e tipografia: riquadri, blocchi statistiche, dove si tocca (nel tema, mai nel `.typ` generato) |
| `skills/rumblingstone-edizione/` | il mestiere dell'editore: colophon, Product Identity / Open Content, **gate d'uscita** IP, versione/ristampa/errata |
| `skills/rumblingstone-art-direction/` | coerenza di un set di immagini, e quando un'immagine si butta ([ADR-0019](plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)) |
| `skills/rumblingstone-mapmaking/` | generazione mappe: Watabou, template, export VTT |
| `skills/rumblingstone-automation/` | CLI `dm.py` e pipeline sessione→stato; scritture di canone solo sotto il vincolo triplo ADR-0007 |
| `skills/rumblingstone-playtest/` | collaudo: audit meccanico, dry-run, schede di feedback, alfa → beta → collaudato ([ADR-0018](plans/adr/ADR-0018-apparato-uso-obbligatorio.md)) |
| `skills/rumblingstone-plans/` | convenzioni dell'archivio dei piani: INDEX, gate, ADR |
| `skills/rumblingstone-debugging/` | debugging per root cause, **solo infrastruttura**; vendorizzata da obra/superpowers (MIT), ADR-0010 |
| `skills/dnd-35-rules/` | meta-router legacy: rimanda alle skill qui sopra |

### Gli agenti di `.claude/agents/`

Quattordici agenti ([ADR-0146](plans/adr/ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md)),
ognuno con le sue skill precaricate. Li lancia il thread con lo strumento Agent
(`subagent_type: "<nome>"`); un agente non ne avvia altri, quindi la catena la
guida il thread. Ogni catena che cambia file finisce con `autore-documenti`, e
la riga «Catena: a → b» nelle istruzioni del thread ferma push e PR finché
manca una chiamata (`scripts/instradamento_agenti.py --cancello`).

| Agente | Classe | Quando |
|---|---|---|
| `autore-prosa-gioco` | Autori | box read-aloud, handout, recap, dialoghi, introduzioni e appendici dei volumi |
| `autore-master` | Autori | master DEF di un arco: stanze, incontri, tattiche, bottega |
| `autore-documenti` | Autori | ADR, piani, guide, corpi di PR; la documentazione dopo ogni lavoro |
| `integratore-dm` | Tecnici | `dm.py`, `dmcore`, plugin di sistema, server MCP, manifest degli strumenti |
| `sviluppatore` | Tecnici | il resto di `scripts/`, CI, test, hook |
| `piattaforma` | Tecnici | canali, versioni fissate, promozioni, rilasci, roadmap |
| `cartografo` | Tecnici | mappe tattiche, Watabou, UVTT |
| `impaginatore` | Tecnici | booklet, PDF, typst, licenze e gate d'uscita |
| `art-director` | Tecnici | immagini, prompt, set coerenti |
| `regolista` | Tecnici | statblock, schede, potenziamenti, arbitrati 3.5 e PF1e |
| `sincronizzatore-giocato` | Tecnici | il giocato sul ramo di gruppo e il merge di main in quel ramo ([ADR-0149](plans/adr/ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md)) |
| `custode-memoria` | Tecnici | che cosa sanno memoria del progetto, file storico e coda; righe tolte da `MEMORY.md`, tetto della memoria, merge fermato dal custode ([ADR-0151](plans/adr/ADR-0151-la-memoria-del-progetto-ha-uno-specchio-e-un-custode.md)) |
| `lettore-a-freddo` | Verificatori, sola lettura | lettura a freddo di prosa o master appena scritti |
| `custode-canone` | Verificatori, sola lettura | coerenza con il canone della campagna e del 1372 DR |

Un agente nuovo entra in questa tabella nella stessa PR: la CI lo controlla
con `scripts/documentazione_allineata.py`
([ADR-0153](plans/adr/ADR-0153-la-documentazione-segue-la-struttura.md)).

### Quando un agente risponde

1. Applica il principio: **chi legge, in che forma esce**. Poi guarda la
   tabella per compito.
2. Carica il `SKILL.md` della skill scelta **per primo**, con lo strumento
   Skill e non a memoria: in Claude Code un hook ferma la scrittura di prosa di
   gioco (handout, recap, introduzioni dei volumi, box read-aloud) se
   `rumblingstone-narrative-style` non è stata caricata, e ricorda
   `rumblingstone-prosa-documenti` sui documenti
   ([ADR-0146](plans/adr/ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md)).
   Gli agenti di `.claude/agents/` le precaricano. Segui la sua tabella
   di routing interna.
3. Per domande di campagna, carica anche `campaign/state.md` e
   `skills/rumblingstone-campaign/references/campaign-coherence.md`.
4. Cita le fonti: sezione SRD, FRCS p.X, oppure `[Private — Red Hand of Doom, p.X]`.
5. **Non inventare mai** blocchi statistiche, effetti di incantesimi, statistiche
   di PNG o poteri di artefatti. Se manca la fonte, marca INFERRED con
   domanda e base: la grammatica sta in `docs/reference/GUIDA-MARCATURE.md`
   (ADR-0109).
6. Per una scelta di metodo, in ogni parte del progetto, parti dallo
   **standard di fatto della comunità**: una soluzione nostra entra solo se
   la misura lo boccia, con il motivo nell'ADR. Le schede di skill, brief e
   prove sono in `docs/reference/GUIDA-SCHEDE-PROMPT.md` (ADR-0114).

---

## Campaign-Specific Conventions

### File naming

- Sessions: `campaign/sessions/YYYY-MM-DD_session-N.md`
- NPCs and villains: `Bestiario/png/` and `Bestiario/villain/` (statblock + catalog entry)
- Encounters: inside the arc module that uses them, next to their tactical map

### NPC file format

```markdown
# [NPC Name]
**Role**: [villain / ally / neutral]
**Status**: [alive / dead / unknown]
**Location**: [current known location]
**Motivation**: [one sentence]
**CR**: [N] | **Race/Class**: [race, class N]
**Key stats**: HP X, AC Y, Attack +Z
**Notes**: [adaptation from RHoD original]
```

### Session log format

```markdown
# Session N — [Title] (YYYY-MM-DD)
**Players present**: [list]
**Location**: [in-world location]
## Summary
## Key decisions
## XP awarded
## Loot distributed
## Next session hooks
```

### Encounter file format

```markdown
# Encounter: [Name]
**Location**: [room/area]
**EL**: [N] | **CR breakdown**: [list monsters + CR]
**Terrain**: [description]
## Tactics
## Adaptations from RHoD original
## Read-aloud text (custom)
```

---

## Rules Adjudication Policy

1. **SRD first**: use d20srd.org for all rules lookups
2. **Non-SRD**: flag as `[Private source]`; do not reproduce copyrighted text verbatim
3. **House rules** live in `campaign/lore/house-rules.md`; always check before ruling
4. **RAW vs RAI**: state which you're providing; give both if ambiguous
5. **Red Hand of Doom adaptations**: documented in `skills/rumblingstone-campaign/references/campaign-coherence.md` (canonical) and summarised in `campaign/DM-QUICKSTART-NUOVI-DM.md`
6. **DM Strategy & Player Profiles**: For adult-oriented, non-linear sessions (Shine Time, State Machine design), consult `skills/rumblingstone-campaign/references/campaign-dm-strategy.md` (canonical). The lore folder file `campaign/lore/dm-player-strategy.md` is now a pointer to that canonical source.
7. **Living world state**: Before describing what NPCs know, where parties/villains currently are, or what threads are open, load `campaign/state.md`. It is the single source of truth for *current* world state (changes per session).
8. **Coherence**: Before introducing artifact powers, NPC knowledge, or callbacks to past PG actions, consult `skills/rumblingstone-campaign/references/campaign-coherence.md`.
9. **Boosting PNGs/villains/monsters**: The campaign runs on D&D 3.5; Pathfinder 1e SRD material (simple templates, Monster-Statistics-by-CR benchmarks, NPC recipes) is an approved boost toolkit. Always go through `skills/npc-villain-boosting/`: it enforces the EL cap (≤ APL+4), the benchmark step, and the `Boost log:` requirement on named-NPC files. Never boost silently.
10. **Session lifecycle & canon writes**: Closing a session, updating `state.md`, generating recaps/briefs/teasers, or invoking anything in `scripts/` goes through `skills/rumblingstone-automation/` (single entrypoint `python3 scripts/dm.py`). Scripts may write canon ONLY under the ADR-0007 triple constraint: group branch (never `main`), DM-confirmed diff, and `<!-- auto: -->` marked regions of `state.md`. Everything else stays a printed proposal the DM applies by hand.
11. **Narrative content generation**: ANY request to generate quests, session prose, read-aloud/boxed text, NPC dialogue, hooks, recaps, or handouts MUST load `skills/rumblingstone-narrative-style/` (nine-pillar style engine) automatically; the user should never have to ask for "the style". It enforces the scene mixer (one lead pillar per scene), the PC Protagonism Test, the living-world rules (NPC/villain agency + SRD attitude mechanics, where protagonism is the camera and not gravity), the Echo Ledger (`state.md` §7.E), and the BG1/2 quest-stage patterns. For **mysteries, clues and in-fiction documents** the case skill `skills/rumblingstone-indagine/` carries the operational layer, including the Eco register (`references/documento-ed-errore-fecondo.md`): the document and its omissions, the rule book as a political engine, the table's wrong deduction made productive instead of corrected, and the guard clause (structure and object, never paragraph length), with the read-aloud ceilings winning any conflict. Coherence (rule 8) always beats style.

---

## For AI Agents: Key DO / DON'T

| DO | DON'T |
|---|---|
| Read session logs before generating continuations | Invent events that contradict session logs |
| Check `Bestiario/png/` and `Bestiario/villain/` before describing NPCs | Invent NPC stats not in files |
| Use 3.5 SRD for all mechanics | Use 5e rules (different system) |
| Load the focused skill for the question (`dnd-35-srd`, `forgotten-realms-lore`, …) | Quote non-SRD books verbatim |
| Close/prep sessions via `dm.py session` (ADR-0007) | Hand-edit `state.md` `auto:` regions or write canon on `main` |
| Flag 4e/5e Forgotten Realms lore as post-1372 DR | Present Spellplague as canon for this campaign |
| Preserve 3.5-era Faerûn canon (1372 DR) | Mix in FR lore from after 1385 DR |

---

## Strumenti esterni: server MCP e skill dei plugin

La configurazione di Claude Code per questo repo sta in `.claude/settings.json`
e `.mcp.json`: sono accesi solo gli strumenti esterni che servono davvero, il
resto è spento o caricato su richiesta.

**Caricati su richiesta, senza chiedere al DM.** I tool MCP sono differiti
(`ENABLE_TOOL_SEARCH`): un agente che ne ha bisogno li carica con `ToolSearch`
e li usa. Le skill generiche (`engineering:*`, `docs:*`, `reflexion:*`,
`anthropic-skills:*`) compaiono solo per nome: si invocano con `Skill` quando
il compito lo chiede, e le skill `rumblingstone-*` hanno sempre la precedenza.

| Server MCP | Quando si usa |
|---|---|
| `rumblingstone-tools` | i tool di `scripts/tools.manifest.json` (quanti sono lo dice `python3 scripts/tools_manifest.py --check`) ([ADR-0030](plans/adr/ADR-0030-server-mcp-sui-tool.md)). Gira in sola lettura: i tool che scrivono canone restano bloccati (ADR-0007) |
| Canva, Fonts | immagini e tipografia (`rumblingstone-art-direction`, `rumblingstone-editoria`) |
| Context7 | documentazione di librerie e di Typst |
| Firecrawl | ricerche di lore e regole sul web |
| Unstructured Transform | conversione da PDF a markdown, in alternativa a `converters/` |
| Hugging Face | modelli e licenze dei pesi per la hero map ([ADR-0019](plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)) |
| draw.io, tldraw | diagrammi |
| Serena | navigazione del codice |

**Spenti in questo progetto**: Gmail, Google Drive, Tavily, arxiv, bioRxiv,
r-btw. Gmail, Google Drive, Channel3, Clipkit, Mobbin, Microsoft Learn, MDN,
Shutterstock, bioRxiv e pg-aiguide sono negati da `permissions.deny` di
`.claude/settings.json`, che toglie i loro tool dal contesto (scelta del DM del
2026-11-19, ADR-0140). Se un compito ne richiede uno, l'agente lo dice al DM,
che lo riaccende con `/mcp` o togliendo la regola. I plugin dell'account che il
repo non ha mai usato sono spenti con `enabledPlugins: false`: restano accesi
`pdf-viewer`, `review` e `tdd`, più i nove di metodo di sviluppo (`sdd`, `sadd`,
`engineering`, `reflexion`, `docs`, `fpf`, `ddd`, `recursive-decomposition`,
`mcp`) riaccesi su scelta del DM (ADR-0140, punto 5). Lo stesso vale per i plugin spenti a livello globale: un agente non
può accenderli da solo.

**File generati e vendorizzati**: `.claudeignore` elenca ciò che l'agente non
deve leggere, ma Claude Code non lo legge da solo: `scripts/claudeignore_deny.py`
lo traduce in regole `Read(...)` di `permissions.deny` (ADR-0142), che valgono
anche per Grep e Glob. Le scelte e come tornare indietro sono in
`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`.

---

## Supported Agents

The canonical skill source is the whole `skills/` tree (every directory with
a `SKILL.md`; `build-skills.sh` auto-discovers them). The one exception is the
game-system skills (ADR-0111, L6): a skill listed by a plugin in
`sistemi/<id>/sistema.toml` is built and synced only when that system is
`attivi` or `rinforzo` in `sistemi.toml`; `python3 scripts/sistemi.py
--skill-escluse` prints the skills that are skipped; skills no plugin lists
are always built. Per-agent mirrors are **generated artifacts**, not committed
to git (see `.gitignore`); each developer/CI builds them locally:

- **Claude Code** → `.claude/skills/<skill>/` (compact.md format). Claude Code also gets THIS file
  split into `.claude/rules/rs-*.md` by `python3 scripts/regole_claude.py`
  (ADR-0141): each section loads only with the files it is for. Edit AGENTS.md,
  then regenerate; `--check` fails when the two drift apart.
- **OpenAI Codex** → `.agents/skills/<skill>/` (machine.json)
- **GitHub Copilot** → `.github/copilot/skills/<skill>/` (compact.md)
- **Cursor** → `.cursor/skills/<skill>/` (machine.json)
- **Windsurf** → `.windsurf/skills/<skill>/` (compact.md)
- **Gemini** → `.gemini/skills/<skill>/` (structured.yaml)
- **ChatGPT** → `.chatgpt/skills/<skill>/` (compact.md)

Build commands:

```
./scripts/build-skills.sh           # build + deploy to ~/.<agent>/skills/
./scripts/build-skills.sh --no-deploy  # build only (CI)
./scripts/sync-skills.sh            # build + populate in-repo mirrors locally
```

**Automatic sync (no manual step needed):**

- **Claude Code** (web + CLI): `.claude/hooks/session-start.sh` (registered
  in `.claude/settings.json`) rebuilds and deploys ALL skill mirrors at the
  start of every session, **asynchronously**, in background.
- **Stale-mirror protocol (async race guard)**: the hook writes
  `.claude/.skills-sync-status` (`syncing…` → `ok <sha> <ts>` | `failed`).
  Before the FIRST campaign-content generation of a session, the agent must
  check that file: if it is missing or not `ok`, **tell the user** the skill
  mirrors may be stale and ask whether to update now; on yes run
  `./scripts/build-skills.sh && ./scripts/sync-skills.sh --no-build`, then
  continue the conversation normally. If the user declines, proceed reading
  the canonical `skills/` tree directly (always current in git).
- **Claude Code started OUTSIDE the repo** (the project threads on claude.ai
  start in the folder that contains the clone): `scripts/claude-progetto.sh`,
  run by the cloud environment's setup script, writes there a short
  `CLAUDE.md`, the repo's `.claude/settings.json` with absolute paths and the
  `.mcp.json`, so the hook, the skills and `rumblingstone-tools` apply
  ([ADR-0140](plans/adr/ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md)).
- **Other agents / plain git users**: run `./scripts/install-git-hooks.sh`
  once; it installs a `post-merge` git hook that resyncs the mirrors after
  every `git pull` that touches `skills/`, and a `pre-push` hook that runs the
  blocking, fast CI gates (`python3 scripts/gate_locale.py --pre-push`, about
  45 s, via pre-commit when installed;
  [ADR-0143](plans/adr/ADR-0143-i-gate-veloci-girano-prima-del-push.md)). In
  Claude Code cloud sessions the SessionStart hook installs both.

Treat `skills/` as the only thing humans edit; mirrors regenerate
deterministically from it.
