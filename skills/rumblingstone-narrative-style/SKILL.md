---
name: rumblingstone-narrative-style
description: >
  Narrative style engine for ALL generated RumblingStone content — quests,
  session prose, read-aloud/boxed text, NPC dialogue, hooks, recaps,
  handouts, villain scenes. Fuses nine pillars into one voice: R.A.
  Salvatore prose, Tolkien/LotR epic depth, House of David dynastic destiny,
  Andor slow-burn intrigue, Game of Thrones political gray, Matt Mercer
  table technique, Baldur's Gate 3 long-range consequences, Baldur's Gate
  1–2 complex quest design, il caso ricomposto (deduction as climax) —
  with the PCs always protagonists, in good and in evil. Trigger on any content-generation request: "genera", "scrivi",
  "crea la quest", "prepara la sessione", "read-aloud", "boxed text",
  "recap", "hook", "descrivi la scena", "session prep", "new quest",
  "dialogo", "conseguenze", "stile narrativo", "mondo vivo", "living
  world", "world turn", "cosa fanno i PNG", "agenda dei villain",
  "indagine", "mistero", "indizio", "ricomposizione",
  "handout", "documento", "chi è stato", "pista falsa", "railroad".
---

# RumblingStone — Narrative Style Engine (Nine Pillars)

**This skill is mandatory for every content-generation request** in this
repo. It defines *how* content sounds and is structured; the other skills
define *what* is true (rules, lore, campaign state). Load it automatically
whenever asked to generate quests, prose, dialogue, hooks, or recaps —
the user should never have to ask for "the style" explicitly.

**Load order for any generation request:**

1. `rumblingstone-campaign/references/campaign-coherence.md` + `campaign/state.md`
   — establish what is true (coherence always beats style).
2. This file — pick the pillar mix for the scene type (table below).
3. `references/style-pillars.md`: the nine pillars: what to take,
   what to avoid, fusion rules.
4. ⚠️ **`references/italiano-nativo.md` — PRIMA DI SCRIVERE**, non prima di
   consegnare. **Spostato qui il 2026-09-02, e il motivo è misurato**: i
   giocatori hanno fatto lo stesso rilievo due volte, il **2026-07-31** e il
   **2026-09-02**, con in mezzo questo motore di stile da duemila righe. Il
   traduttese **non è una lista di errori da correggere in revisione**: è il
   modo in cui la frase è stata costruita. Se scrivi con la testa in inglese e
   poi correggi i dieci calchi che la lista nomina, restano la sintassi, il
   ritmo e l'ordine delle informazioni — che sono esattamente ciò che un
   lettore sente. La checklist di 30 secondi del file resta come **ultima**
   passata; il file si legge **all'inizio**.
5. The specific reference for the task (table below).
6. **La checklist di 30 secondi di `italiano-nativo.md` — prima di consegnare**,
   su qualsiasi testo player-facing (hint, **echi**, teaser, iscrizioni,
   lettere) e qualsiasi **read-aloud**. È la seconda metà del punto 4, non un
   doppione: lì si legge il file per scrivere in italiano, qui si ripassa il
   testo scritto.
   Guarda soprattutto il **§9 sui tic dell'IA**, che è un problema **diverso**
   dal traduttese: lì la sintassi è giusta ma sempre la stessa, e a tradire non
   sono gli errori ma le **abitudini** — l'antitesi «non X: è Y», il tricolon,
   la chiusa a effetto obbligatoria, il fatto che ogni dettaglio sia
   significativo.
   🤖 **Da qui in poi non conti a mano**: `python3 scripts/validate_prosa.py FILE`
   misura i calchi e i tic a densità («massimo uno per documento» è la regola
   che un revisore non applica mai, perché dovrebbe contare).
   **Non è opzionale e non è stilistico: è la differenza fra un handout che i
   giocatori leggono e uno che li stacca.**
7. **`references/read-aloud-adulti.md` — prima di scrivere qualsiasi
   read-aloud.** Il pubblico di questo tavolo è fatto di **adulti che leggono
   fantasy da vent'anni**: conoscono i cliché meglio di chi scrive. Il file
   copre il vincolo che cambia tutto — **un read-aloud si ascolta, non si
   legge** (un nome nuovo per box, max due subordinate, niente parentesi,
   l'ultima riga è quella che resta) — le lunghezze reali per tipo di box, cosa
   premia questo pubblico (competenza concreta, allusione, il dettaglio
   inutile, il comportamento al posto dell'emozione etichettata) e cosa lo fa
   staccare (voce YA, tutto-epico, esposizione travestita da dialogo).

> 🇮🇹 **Lingua sorgente: italiano, sempre** ([ADR-0016](../../plans/adr/ADR-0016-lingua-sorgente-e-edizioni.md)).
> L'inglese è un'edizione derivata, mai la stesura. I nomi propri si scrivono
> come da [`campaign/GLOSSARIO-E-LOCALIZZAZIONE.md`](../../campaign/GLOSSARIO-E-LOCALIZZAZIONE.md).

## The Nine Pillars (one-line summary)

| # | Pillar | What it contributes |
|---|---|---|
| 1 | **R.A. Salvatore** | Prose voice: sensory detail, combat as choreography, internal monologue, moral cost |
| 2 | **Tolkien / LotR** | Epic depth: layered history, landscape as character, hope under burden, mercy that pays off |
| 3 | **La Casa di Davide** | Destiny & dynasty: the anointed-but-not-yet-crowned, faith tested, a leader's sins ripple onto his house |
| 4 | **Andor** | Slow-burn intrigue: the machinery of oppression, ordinary people radicalized, sacrifice without witnesses |
| 5 | **Game of Thrones** | Political gray: every faction believes it is right, no plot armor for NPCs, dinner tables as battlefields |
| 6 | **Matt Mercer** | Table technique: distinct NPC voices, "how do you want to do this?", yes-and, backstory woven into plot |
| 7 | **Baldur's Gate 3** | Long-range consequences: every meaningful choice writes an echo that returns changed, sessions later |
| 8 | **Baldur's Gate 1–2** | Quest architecture: multi-stage quests, interleaved factions, personal companion quests, villains with a personal claim on the PCs |
| 9 | **Il caso ricomposto** | Deduction as climax: clues posed innocent and re-read by one key, six doors so combat-built PCs can investigate, the retrospective montage. Literary anchor: **Umberto Eco**, *Il nome della rosa* — the document and its omissions, the rule book as a political engine, the fruitful error |

> **Due piani, non uno.** Il mixer qui sotto è **per scena**. Il piano
> **per arco** — di che colore è l'arco intero, e se quel colore è già stato
> usato in quello prima — sta in `references/varieta-fra-archi.md`, e va
> deciso **prima** di scrivere il contenuto dell'arco. La monotonia di una
> campagna non è un difetto di scena: è un difetto di sequenza, e non si vede
> leggendo un modulo.

**Fusion rule — never all nine at once.** Every scene has ONE lead pillar
and at most two support pillars, chosen by scene type. The mixer:

| Scene type | Lead | Support |
|---|---|---|
| Combat / action prose | Salvatore | Mercer (finisher), LotR (stakes) |
| Read-aloud / location intro | LotR | Salvatore (senses) |
| Political / faction scene | Game of Thrones | Andor |
| Investigation / mystery (a case) | Il caso ricomposto | Andor (procedure), GoT (who profits) |
| Infiltration / heist | Andor | BG1–2 (structure) |
| Reveal / recomposition scene | Il caso ricomposto | Salvatore (senses), BG3 (echoes surfaced) |
| **In-fiction document / handout with an author** | **Il caso ricomposto** (registro Eco) | Mercer (the voice that wrote it) |
| PC personal arc / destiny beat | Casa di Davide | Mercer, BG3 (echoes) |
| NPC dialogue | Mercer | GoT (agendas) |
| Quest design (structure) | BG1–2 | BG3 (echoes), Andor (intrigue) |
| Consequence / callback scene | BG3 | Casa di Davide (reaping) |
| Villain scene | GoT | Casa di Davide (fallen king), Salvatore |
| Session recap / hype | Salvatore | BG3 (echoes surfaced) |

## Domain → File

| Task | File |
|---|---|
| Full pillar profiles: take / avoid / techniques / fusion rules | `references/style-pillars.md` |
| PCs as protagonists in good AND evil — spotlight, flaws, fame/infamy | `references/pc-protagonism.md` |
| BG3-style echo ledger: writing, timing, and paying off consequences | `references/consequence-echoes.md` |
| BG1/2-style complex quest patterns: stages, factions, personal quests | `references/quest-design-baldur.md` |
| Living world: NPC/villain agency, world turn, SRD attitude system, settlements | `references/living-world.md` |
| **Varietà fra gli archi** — la tavolozza d'arco (dominante · contrappunto · famiglia di caso · congegno · picco), le sei tinte e il difetto di ciascuna, le regole di rotazione, **la prova del recap**; e per gli archi **modulari** la **quota di modulo** (quanti puliti / con mistero / con congegno) e **l'orchestrazione dinamica** (vocazioni, gettone in mano, la regola dello scarto) | `references/varieta-fra-archi.md` |
| **Casi, indizi, enigmi, il congegno finale** — nodi a tre strati, le sei porte per i PG senza gradi, Acume/Perizia/Metodo, la ricomposizione; e il **registro Eco** — il documento e le sue assenze, il regolamento della comunità chiusa, **l'errore fecondo** (anti-binario), il dettaglio-meccanismo | **skill dedicata `rumblingstone-indagine`** (per il registro Eco: `references/documento-ed-errore-fecondo.md`) |
| Editorial standards: terminologia canonica, resa read-aloud, tipografia, igiene (enforced in CI da `validate_modules.py`) | `references/editorial-standards.md` |
| **Le passate redazionali** — il *giro*, non la norma: le tre passate (struttura → voce → bozze), quando un testo è **chiuso**, e i tre soli casi che lo riaprono. La 2ª si legge **ad alta voce**: il traduttese si sente e non si vede | **`references/passate-redazionali.md`** |
| **Read-aloud per adulti che leggono fantasy** — si ascolta non si legge, lunghezze per tipo di box, competenza concreta, cosa fa staccare, checklist | **`references/read-aloud-adulti.md`** |
| **Italiano nativo + anti-riconoscibilità** — calchi, dislocazioni, diminutivi, tempi, ritmo, registro nanico (§1-8) · **i tic dell'IA: antitesi «non X: è Y», tricolon, chiuse a effetto, tutto-è-significativo** (§9) · checklist | **`references/italiano-nativo.md`** |

**Worked exemplar in repo**: the Palio di Channathgate
(`09_.../Arco-Post-Hammerfist-P2D-PALIO-DM-MASTER-REFERENCE.md` + allegati)
is the reference implementation of this skill's standards — Salvatore
prose + Critical Role direction (declared), BG3-graded consequence matrix,
time-axis milestones, ceremonial meters, PC offices. When generating a
multi-session set piece, study its *shape* first
(`references/quest-design-baldur.md` §6-bis).

## Non-negotiables (checked on every output)

1. **PCs are the protagonists**: every generated scene must give at least
   one PC a decision, a spotlight, or a consequence of a past choice. No
   scene where NPCs resolve the plot among themselves.
   See `references/pc-protagonism.md`.
1-bis. **…but the world is alive** — protagonism is the camera, not
   gravity: NPCs, villains, and factions act for their own Want/Fear,
   off-screen and against party convenience too, with reactions grounded
   in SRD attitude mechanics. No NPC whose only reason to exist is the
   PCs' plot. See `references/living-world.md`.
2. **Consequences are never forgotten**: meaningful choices write an echo
   (`references/consequence-echoes.md`); generated content must surface at
   least one *past* echo when the fiction allows it.
3. **Coherence beats style**: if a stylistic flourish contradicts
   `campaign-coherence.md` or `state.md`, drop the flourish, flag the
   conflict. Never retcon for drama.
4. **No pillar parody**: the pillars are craft sources, not brands to
   imitate loudly. Never name-drop them in generated fiction, never copy
   protected text, characters, or proper nouns from them.
5. **Tone floor**: adult, slow-build, no modern slang, no fourth-wall
   winks, no victory without cost (inherited from
   `rumblingstone-campaign/references/campaign-coherence.md` §4).
6. **Un mistero ha una soluzione scritta**: ogni domanda che il modulo pone
   ai giocatori ha una risposta preparata e una **rete ridondante** di nodi su
   canali diversi (`rumblingstone-indagine`). Aperto non è sinonimo di
   indefinito: senza soluzione preparata l'errore fecondo diventa
   improvvisazione, e i giocatori se ne accorgono al secondo tentativo.
7. **La lunghezza non è mai un pilastro**: il registro Eco entra al livello
   della struttura e dell'oggetto, mai a quello del paragrafo. In conflitto
   vincono sempre i tetti di `references/read-aloud-adulti.md`.

## Self-check before delivering generated content

Run the coherence self-check (`campaign-coherence.md` §6) first, then:

1. Which pillar leads this scene? (If "all of them" → rewrite: pick one.)
2. Does at least one PC act, choose, or get echoed? (If no → rewrite.)
3. Did I surface or write an echo? (If the scene is meaningful → yes.)
4. Would this scene survive with the serial numbers filed off — no borrowed
   names, no imitation so close it reads as the source? (If no → rewrite.)
5. Living-world check: does every named NPC have a Want that isn't about
   the PCs, and did the world act for its own reasons somewhere? (If no →
   rewire; see `references/living-world.md` §7.)
6. If the scene poses a question: is the clue network redundant, and does the
   table's wrong answer still lead somewhere real? (If no → see
   `rumblingstone-indagine/references/documento-ed-errore-fecondo.md` §4-5.)
7. Did any box grow past the read-aloud ceiling because the prose got
   interesting? (If yes → cut; the ceiling wins.)

---

## Il confine con i documenti del repo

Questa skill governa la prosa **di gioco**: read-aloud, handout, dialoghi, echi,
teaser, iscrizioni. Guide, ADR, piani, skill, README e corpi delle PR seguono
`rumblingstone-prosa-documenti`, e alcune sue regole qui sarebbero **sbagliate**:
là il numero annunciato prima dell'elenco è un tic, qui «tre porte, tre serrature»
è ritmo; là la frase breve isolata è un tell, qui è il colpo che chiude un box.

Quello che vale su tutti e due i lati è §9 di `italiano-nativo.md`: l'antitesi
«non X: è Y» e il trattino lungo come respiro suonano generati ovunque.
