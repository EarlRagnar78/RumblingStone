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
└── lore/                    # House rules, campaign history, DM/player strategy

# NPCs, locations and encounters do NOT live under campaign/. NPC and villain
# cards are in Bestiario/png/ and Bestiario/villain/; locations and encounters
# are inside the arc modules (00_… to 09_…), with their tactical maps.

skills/
├── dnd-35-srd/             # D&D 3.5 SRD mechanics (no setting bias)
├── forgotten-realms-lore/  # Faerûn 1372 DR canon
├── rumblingstone-campaign/ # custom campaign + coherence rules
├── rumblingstone-narrative-style/ # nine-pillar style engine (mandatory for generation)
├── rumblingstone-mapmaking/ # battle-map pipeline (3 modes, JSON contract, UVTT)
├── rumblingstone-automation/ # dm.py CLI + session-state pipeline (ADR-0007)
├── rumblingstone-debugging/ # root-cause debugging, SOLO infrastruttura scripts/CI (vendored da obra/superpowers, MIT — ADR-0010)
├── rumblingstone-plans/    # plan-archive discipline (INDEX, CHANGELOG, ADRs)
├── rumblingstone-playtest/ # collaudo: audit, dry-run, feedback, alfa→beta→collaudato
├── rumblingstone-art-direction/ # coerenza di un set di immagini: ancora storica, schede-personaggio, lock, gate di rifiuto
├── pathfinder-1e-srd/      # PF1e rules, templates, 3.5<->PF conversion
├── npc-villain-boosting/   # when/whether/how to boost PNGs, villains, monsters
└── dnd-35-rules/           # legacy meta-router (points to the skills above)

STANDALONE-Il-Drappo-di-Tarsilia/  # self-contained PF1e module set in Golarion —
           # shares the race SYSTEM with arc 09's Palio and nothing else
           # (no Faerûn, no RHoD, no campaign PCs). Start at 00-HUB-E-QUICKSTART-DM.md

plans/     # work-plan archive: INDEX.md (status + % + gates), CHANGELOG.md, adr/
scripts/   # DM automation — single entrypoint: python3 scripts/dm.py
converters/ # content converters (pdf→md, html→md, img→webp) — NOT the DM automation
```

Per-agent mirrors (`.claude/skills/`, `.cursor/skills/`, etc.) are
generated artifacts of `scripts/build-skills.sh` and are gitignored.
`.hb.md` files are generated Homebrewery layouts (`plans/adr/ADR-0003`):
regenerate via `dm.py recap --hype` / `dm.py handout`, never edit by hand.

> **DMs: start with `campaign/DM-CAMPAIGN-PLAYBOOK.md`.** It contains the
> pre/during/post-session workflow, worked examples for session files and
> `state.md` diffs, the `§0 Campaign Status At-a-Glance` dashboard, and the
> branch-per-group reset procedure (`scripts/new-campaign-group.sh`) for
> running this campaign with a new group.

---

## Skills

**Il principio, prima della tabella.** Prima di produrre qualunque cosa,
chiediti **chi la leggerà** e **in che forma uscirà**. Quelle due risposte —
non l'argomento — scelgono la skill. Un mostro descritto in un booklet da
stampare e lo stesso mostro dentro `Bestiario/` non vogliono lo stesso
apparato; un ADR e un read-aloud sono entrambi prosa italiana e seguono norme
**opposte** (ADR-0035).

La tabella qui sotto **illustra** il principio, non lo esaurisce: se il tuo
compito non c'è, applica la domanda. Le skill marcate **obbligatorie** vanno
caricate anche se il DM non le nomina — è il DM ad averlo chiesto, e non
doverle chiedere è il punto.

### Cosa carico, in base a cosa sto per fare

| Sto per… | Carico (obbligatorie in **grassetto**) |
|---|---|
| Scrivere prosa che un **giocatore** leggerà o sentirà — read-aloud, handout, dialoghi, teaser, recap, echi | **`rumblingstone-narrative-style`** (+ il suo `references/italiano-nativo.md`, obbligatorio) |
| Scrivere un **documento del repo** — guida, ADR, piano, README, corpo di PR, messaggio di commit | **`rumblingstone-prosa-documenti`** ⚠️ regole opposte alla riga sopra: non mescolarle |
| Costruire o giocare un **caso**: mistero, indizi, enigma, ricomposizione, vicolo cieco | **`rumblingstone-indagine`** (sopra `narrative-style`, che resta il fondo) |
| Consolidare un beat d'arco in un **master definitivo** di qualità AP | **`rumblingstone-module-standard`** |
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
o se questo documento cita una skill che non esiste.

⚠️ Nessun agente «scopre» queste skill da solo. Alcuni leggono le descrizioni
del frontmatter, altri caricano solo ciò che un documento gli nomina, altri
non hanno alcun meccanismo di scoperta. È questa sezione a instradarli.

| Skill | Che cos'è |
|---|---|
| `skills/dnd-35-srd/` | meccaniche d20 SRD pure |
| `skills/pathfinder-1e-srd/` | regole PF1e, template semplici, benchmark GS, conversione 3.5↔PF1e |
| `skills/forgotten-realms-lore/` | canone di Faerûn, 1372 DR |
| `skills/npc-villain-boosting/` | framework decisionale e workflow per potenziare PNG, villain e mostri |
| `skills/rumblingstone-campaign/` | questa campagna: PG, artefatti, archi, coerenza |
| `skills/rumblingstone-narrative-style/` | motore di stile a nove pilastri (prosa Salvatore, profondità LotR, destino Casa di Davide, intrigo Andor, politica GoT, tecnica di tavolo Mercer, echi BG3, quest design BG1/2, il caso ricomposto), protagonismo dei PG nel bene e nel male |
| `skills/rumblingstone-indagine/` | come si costruisce e si gioca un **caso**: nodo d'indizio a tre strati, le sei porte, registro Acume/Perizia/Metodo (ADR-0022), ricomposizione, vicolo cieco |
| `skills/rumblingstone-prosa-documenti/` | come si scrivono i **documenti** del repo perché non suonino generati a macchina — tic di composizione dell'IA, tropi inglesi da non importare |
| `skills/rumblingstone-module-standard/` | standard di qualità dei master DEF: profondità, struttura, livello di finitura (benchmark: Red Hand of Doom + AP Pathfinder 1e) |
| `skills/rumblingstone-editoria/` | il mestiere del layout designer e del tipografo: riquadri, blocchi statistiche, dove si tocca (nel tema, mai nel `.typ` generato) |
| `skills/rumblingstone-edizione/` | il mestiere dell'editore: colophon, Product Identity / Open Content, **gate d'uscita** IP, versione/ristampa/errata |
| `skills/rumblingstone-art-direction/` | il mestiere dell'art director: cosa hanno in comune le immagini di un set, e quando un'immagine si butta ([ADR-0019](plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)) |
| `skills/rumblingstone-mapmaking/` | workflow di generazione mappe: Watabou, template, export VTT |
| `skills/rumblingstone-automation/` | CLI `dm.py` e pipeline sessione→stato: wizard di fine sessione, recap per PG, brief; scritture di canone solo sotto il vincolo triplo ADR-0007 |
| `skills/rumblingstone-playtest/` | come si collauda: audit meccanico, dry-run cronometrato, schede di feedback, ciclo alfa → beta → collaudato ([ADR-0018](plans/adr/ADR-0018-apparato-uso-obbligatorio.md)) |
| `skills/rumblingstone-plans/` | convenzioni dell'archivio dei piani: INDEX, gate, ADR |
| `skills/rumblingstone-debugging/` | debugging sistematico per root cause, **solo infrastruttura**; vendorizzata da obra/superpowers (MIT), politica in ADR-0010 |
| `skills/dnd-35-rules/` | meta-router legacy: rimanda alle skill qui sopra |

### Quando un agente risponde

1. Applica il principio: **chi legge, in che forma esce**. Poi guarda la
   tabella per compito.
2. Carica il `SKILL.md` della skill scelta **per primo**; segui la sua tabella
   di routing interna.
3. Per domande di campagna, carica anche `campaign/state.md` e
   `skills/rumblingstone-campaign/references/campaign-coherence.md`.
4. Cita le fonti: sezione SRD, FRCS p.X, oppure `[Private — Red Hand of Doom, p.X]`.
5. **Non inventare mai** blocchi statistiche, effetti di incantesimi, statistiche
   di PNG o poteri di artefatti. Marca `[INFERRED — needs DM confirmation]`.

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

## Supported Agents

The canonical skill source is the whole `skills/` tree (every directory with
a `SKILL.md`; `build-skills.sh` auto-discovers them). Per-agent mirrors are
**generated artifacts**, not committed to git (see `.gitignore`). Each
developer/CI runs the build pipeline locally:

- **Claude Code** → `.claude/skills/<skill>/` (compact.md format)
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
  start of every session, **asynchronously**: the session starts at once
  while the build runs in background.
- **Stale-mirror protocol (async race guard)**: the hook writes
  `.claude/.skills-sync-status` (`syncing…` → `ok <sha> <ts>` | `failed`).
  Before the FIRST campaign-content generation of a session, the agent must
  check that file: if it is missing or not `ok`, **tell the user** the skill
  mirrors may be stale and ask whether to update now; on yes run
  `./scripts/build-skills.sh && ./scripts/sync-skills.sh --no-build`, then
  continue the conversation normally. If the user declines, proceed reading
  the canonical `skills/` tree directly (always current in git).
- **Other agents / plain git users**: run `./scripts/install-git-hooks.sh`
  once; it installs a `post-merge` git hook that resyncs the mirrors after
  every `git pull` that touches `skills/`.

Why mirrors aren't committed: they are 6× the source size (~3MB), drift over
time, and any agent that needs them can regenerate deterministically from
`skills/`. Treat `skills/` as the only thing humans edit.
