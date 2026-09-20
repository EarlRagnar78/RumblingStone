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

### 🥇 REGOLA D'ORO DELLA PROSA — una skill non è il suo `SKILL.md`

> **Prima di scrivere una riga di prosa di gioco, o di misurarla, o di dire che
> uno standard manca: apri i `references/` e leggili. Tutti quelli che la
> riga della tabella ti assegna, per intero. Il `SKILL.md` è l'indice, non la
> norma.**

🔴 **Questa regola nasce da un fallimento misurato, il 2026-09-18.** Un agente
— io — ha costruito un metro dello stile leggendo **due** `SKILL.md` e nessun
`references/`, e ha concluso che certi standard «non esistevano». Esistevano:
`read-aloud-adulti.md` prescrive da agosto **box ≤ 12 righe, un solo nome
proprio nuovo, niente parentesi**; `editorial-standards.md` §2 prescrive la
forma dei dialoghi che avevo dichiarato «inventata». E `ADR-0014` — *regia
sensoriale obbligatoria*, luglio — era stato applicato a **un documento su
cento**: la chiusura su «Che fate?», dovuta a *ogni* box di combattimento,
esisteva **una volta in tutto il repo**.

⚠️ **Non era un problema di scopribilità.** Tutti e 56 i `references/` sono
già citati dai loro `SKILL.md`: un cancello sulla citazione sarebbe verde e
inutile. Il problema è che **una norma che nessuno misura non fa rumore quando
viene ignorata** — per settimane, in silenzio.

Quindi la regola ha **tre obblighi**, e il terzo è quello che la rende diversa
da un buon proposito:

1. **Leggi i `references/`**, non il loro elenco. Sono la norma; il `SKILL.md`
   è la mappa. Dieci file solo in `narrative-style`.
2. **Misura prima di affermare.** «Questo standard manca», «lo stile non è
   arrivato qui», «questa forma non la usa nessuno» sono affermazioni
   *misurabili*: `python3 scripts/misura_craft.py [--box|--copertura|--spotlight]`.
   Un'affermazione sullo stato del repo senza una misura accanto non vale.
3. **Se introduci una norma, registrala.**
   [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) elenca
   ogni norma con **chi la misura**, o con **il perché nessuno la misura**.
   Il gate `python3 scripts/validate_norme_editoriali.py` boccia un file
   normativo non registrato e un rimando a uno strumento che non esiste
   ([ADR-0056](plans/adr/ADR-0056-una-norma-senza-misura-non-esiste.md)).

> **Il corollario scomodo**: introdurre uno standard **non è** aver fatto il
> lavoro. I due commit che hanno portato `read-aloud-adulti.md` e `ADR-0014`
> erano ottimi e sono rimasti lettera morta, uno perché non ha toccato un solo
> file d'arco, l'altro perché ne ha toccato uno. **Una norma nuova arriva con
> il suo lotto di applicazione e la sua misura, o non è arrivata.**

#### 🔴 Quarto obbligo: **la self-check prima di consegnare** *(aggiunto lo stesso giorno)*

Il DM, poche ore dopo la prima stesura: *«perché non è partita automaticamente?
Non è che c'è una skill che l'aveva previsto?»*

**Ce l'aveva.** `rumblingstone-narrative-style` ha una sezione
**«Self-check before delivering generated content»**: il controllo di coerenza
più **sette domande**. Non era partita perché i tre obblighi qui sopra dicono
**«leggi»** e **«misura»**, non **«esegui la self-check prima di consegnare»** —
e una riscrittura è esattamente il momento in cui serve.

> **4. Prima di consegnare prosa di gioco, esegui la self-check della skill.**
> Non «tienila a mente»: **eseguila**, domanda per domanda. Dove la domanda è
> misurabile, la risposta è un **comando**, non un'impressione.

| Domanda della self-check | Come si risponde |
|---|---|
| 1 · Quale pilastro guida la scena? *(se «tutti» → riscrivi)* | `misura_craft` → `PILASTRO dichiarato (lead/support)` |
| 2 · Almeno un PG agisce, sceglie o riceve un'eco? | `--spotlight` (indicatore) |
| 3 · Ho scritto o fatto riemergere un'eco? | congegno `eco / conseguenze a distanza` |
| 4 · Sopravvive senza i numeri di serie — niente nomi presi in prestito? | **giudizio**, nessuna misura |
| 5 · Ogni PNG nominato ha un *Want* che non riguarda i PG? | congegno `grigio politico` |
| 6 · La rete d'indizi è ridondante, e la risposta sbagliata porta comunque da qualche parte? | congegni `nodo d'indizio` + `modi di fallimento` |
| 7 · **Qualche box è cresciuto oltre il tetto perché la prosa era venuta bene?** *(→ taglia; vince il tetto)* | `misura_craft --box`, colonna `>12 righe` |

🔎 **La settima non è un esempio scelto a caso: è quella che ho fallito.** La
riscrittura di `ARC07-DEF-4` del 2026-09-18 ha lasciato un box da **15 righe**
— proprio quello meglio scritto, l'ingresso di Balvar — e l'ho corretto solo
dopo che il DM ha fatto questa domanda. Spezzandolo in tre battute il testo è
**migliorato**, perché il silenzio del vecchio è diventato la prima battuta.
La domanda 7 esiste per quello.

⚠️ **E la self-check non basta da sola**: due congegni che la skill dichiara —
`[HDYWTDT]` (il finisher va al giocatore, ai punti di morte dei boss) e
*yes-and with teeth* (l'invenzione del giocatore entra nel canone **e** genera
una complicazione) — erano a **zero in tutti e nove gli archi** e non erano
nemmeno nel metro. Adesso sono due congegni di `misura_craft`. **Se una cosa
sta in una skill e in nessun rilevatore, prima o poi sparisce.**

#### 🧭 Quinto obbligo: **l'ordine di caricamento è a strati, e sta in un dato**

Il DM: *«fai un ordine gerarchico delle skill che eviti di far saltare le skill
[…] verifica se ci sono skill che si sovrappongono e orchestrale in maniera
smart, con meccanismi davvero misurabili»*.

> **5. Prima di caricare, applica l'algoritmo a cinque domande di
> [`skills/ORCHESTRAZIONE.md`](skills/ORCHESTRAZIONE.md).** Cinque strati più
> la consultazione, otto conflitti ognuno con un vincitore dichiarato, e un
> gate (`validate_skills.py`) che boccia una skill senza posto nella gerarchia.

| # | Domanda | Cosa carichi |
|---|---|---|
| 1 | **Tocco il canone?** | sì → **L0 sempre**, e batte tutti (regola 8) |
| 2 | **Chi legge?** | giocatore → `narrative-style` · il repo → `prosa-documenti`. ⚠️ **una sola delle due, mai entrambe** (ADR-0035) |
| 3 | **Che cosa sto scrivendo?** | L2: `indagine` · `module-standard` · `npc-villain-boosting` |
| 4 | **In che forma esce?** | L3: `editoria` · `edizione` · `mapmaking` · `art-direction` |
| 5 | **Che gesto sto facendo?** | L4: `plans` · `automation` · `playtest` · `debugging` |

Solo la **2** ha una risposta sola; dalla 3 in poi si somma. La consultazione
(SRD, lore) si apre per un **fatto**, mai per decidere.

🔎 **La gerarchia non è stata inventata**: esisteva già, sparsa in **cinque
frasi** di questo documento («la coerenza batte lo stile», «sopra
`narrative-style`, che resta il fondo», «regole opposte», «le righe si
sommano», «read-aloud ceilings winning any conflict»). Erano tutte corrette e
**nessuna verificabile**. Le diciotto skill entrano in diciotto caselle, una
per una — ed è la prova che la struttura c'era.

⚠️ **E «massimizzare l'uso» è il bersaglio sbagliato, dichiarato in
[ADR-0058](plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md).**
Caricarle tutte e diciotto sarebbe il danno: `narrative-style` e
`prosa-documenti` dettano regole **opposte** sullo stesso italiano, e insieme
danno un testo che sbaglia in entrambi i modi. **Il bersaglio misurabile è
*zero omissioni di ciò che è obbligatorio*** — e l'obbligo vero è su **L0-L2**.
L4 e LR **non** si caricano per sicurezza.

#### 🔎 Sesto obbligo: **la FASE 1 si esegue in sola lettura, prima di toccare**

Il DM, il 2026-09-20: *«mettere una golden rule che esegue i passi della Fase 1
di analisi in sola lettura […] e si usa preferibilmente il registro delle
norme, l'algoritmo a strati e i 322 nomi di Bestiario prima di qualsiasi regex,
in modo da eliminare errori di analisi ricorrenti»*.

> **6. Prima di modificare qualunque cosa, esegui
> `python3 scripts/fase1.py <bersagli>`.** I quattro passi vanno in
> **quest'ordine**, e una regex nuova è l'ultima risorsa.

| # | La domanda | Chi la risponde, e perché prima della regex |
|---|---|---|
| **1** | «questa cosa la misura già qualcuno?» | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md). Se sì **si riusa**: *una norma, un rilevatore* ([RICERCA-STANDARD-PROSA](plans/RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md) §4) |
| **2** | «quali skill devo avere aperte?» | [`skills/ORCHESTRAZIONE.md`](skills/ORCHESTRAZIONE.md), le cinque domande. Il bersaglio risponde **da sé** alla 2: un file sotto `plans/` parla al repo, uno d'arco parla al tavolo |
| **3** | «cosa è archivio, cosa è superato, chi sono i nomi propri?» | i **322 nomi** da `Bestiario/` e `state.md`; `_SNAPSHOT-STORICO.md`; `ESCLUSI_NOME`; le matrici delle versioni |
| **4** | «da che numero parto?» | `misura_craft`, sui bersagli veri e non su un campione |

🔴 **Non è una precauzione: è la classifica dei difetti veri.** Quattordici
misure sbagliate fra il 2026-09-17 e il 2026-09-20, e **nessuna** veniva da una
regex scritta male. Venivano tutte dall'aver scritto una regex **prima di
guardare se il dato c'era già** — la virgola contata come trigger (82 coppie
invece di 5), «web» che cattura *web enhancement* (80% invece di 39%), «caso»
che è italiano comune (55 indagini invece di 3), le maiuscole d'inizio frase
contate come nomi propri (nove box invece di tre, **e il numero falso finito
nel corpo di una PR**), un filtro di percorso che non scattava mai (1.548 file
invece di 511).

⚠️ **Questa regola nasce già violata.** L'ordine del DM è arrivato mentre
scrivevo la FASE 1 di `PIANO-QUATTRO-ORDINI-2026-09-20`, e quella FASE 1 aveva
appena commesso **due** degli errori dell'elenco. Il cancello `--check` esiste
per il primo dei due: `fase1.py --check` **esce 1** se stai per modificare un
archivio che il repo dichiara tale.

### Cosa carico, in base a cosa sto per fare

| Sto per… | Carico (obbligatorie in **grassetto**) |
|---|---|
| Scrivere prosa che un **giocatore** leggerà o sentirà — read-aloud, handout, dialoghi, teaser, recap, echi | **`rumblingstone-narrative-style`** e i suoi `references/` — **obbligatori e da leggere**, non da elencare: `italiano-nativo.md` (la lingua), `read-aloud-adulti.md` (le soglie: ≤12 righe, un nome proprio, niente parentesi), `editorial-standards.md` (le due forme prescritte), `style-pillars.md` (la *fusion rule*) |
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
