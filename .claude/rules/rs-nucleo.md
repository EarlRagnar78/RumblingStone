<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->
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

