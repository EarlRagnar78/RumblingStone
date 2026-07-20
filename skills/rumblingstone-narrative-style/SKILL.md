---
name: rumblingstone-narrative-style
description: >
  Narrative style engine for ALL generated RumblingStone content — quests,
  session prose, read-aloud/boxed text, NPC dialogue, hooks, recaps,
  handouts, villain scenes. Fuses eight pillars into one voice: R.A.
  Salvatore prose, Tolkien/LotR epic depth, House of David dynastic destiny,
  Andor slow-burn intrigue, Game of Thrones political gray, Matt Mercer
  table technique, Baldur's Gate 3 long-range consequences, Baldur's Gate
  1–2 complex quest design — with the PCs always protagonists, in good and
  in evil. Trigger on any content-generation request: "genera", "scrivi",
  "crea la quest", "prepara la sessione", "read-aloud", "boxed text",
  "recap", "hook", "descrivi la scena", "session prep", "new quest",
  "dialogo", "conseguenze", "stile narrativo", "mondo vivo", "living
  world", "world turn", "cosa fanno i PNG", "agenda dei villain".
---

# RumblingStone — Narrative Style Engine (Eight Pillars)

**This skill is mandatory for every content-generation request** in this
repo. It defines *how* content sounds and is structured; the other skills
define *what* is true (rules, lore, campaign state). Load it automatically
whenever asked to generate quests, prose, dialogue, hooks, or recaps —
the user should never have to ask for "the style" explicitly.

**Load order for any generation request:**

1. `rumblingstone-campaign/references/campaign-coherence.md` + `campaign/state.md`
   — establish what is true (coherence always beats style).
2. This file — pick the pillar mix for the scene type (table below).
3. `references/style-pillars.md` — the eight pillars: what to take,
   what to avoid, fusion rules.
4. The specific reference for the task (table below).

## The Eight Pillars (one-line summary)

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

**Fusion rule — never all eight at once.** Every scene has ONE lead pillar
and at most two support pillars, chosen by scene type. The mixer:

| Scene type | Lead | Support |
|---|---|---|
| Combat / action prose | Salvatore | Mercer (finisher), LotR (stakes) |
| Read-aloud / location intro | LotR | Salvatore (senses) |
| Political / faction scene | Game of Thrones | Andor |
| Investigation / infiltration | Andor | BG1–2 (structure) |
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

**Worked exemplar in repo**: the Palio di Channathgate
(`09_.../Arco-Post-Hammerfist-P2D-PALIO-DM-MASTER-REFERENCE.md` + allegati)
is the reference implementation of this skill's standards — Salvatore
prose + Critical Role direction (declared), BG3-graded consequence matrix,
time-axis milestones, ceremonial meters, PC offices. When generating a
multi-session set piece, study its *shape* first
(`references/quest-design-baldur.md` §6-bis).

## Non-negotiables (checked on every output)

1. **PCs are the protagonists** — every generated scene must give at least
   one PC a decision, a spotlight, or a consequence of a past choice. No
   scene where NPCs resolve the plot among themselves.
   See `references/pc-protagonism.md`.
1-bis. **…but the world is alive** — protagonism is the camera, not
   gravity: NPCs, villains, and factions act for their own Want/Fear,
   off-screen and against party convenience too, with reactions grounded
   in SRD attitude mechanics. No NPC whose only reason to exist is the
   PCs' plot. See `references/living-world.md`.
2. **Consequences are never forgotten** — meaningful choices write an echo
   (`references/consequence-echoes.md`); generated content must surface at
   least one *past* echo when the fiction allows it.
3. **Coherence beats style** — if a stylistic flourish contradicts
   `campaign-coherence.md` or `state.md`, drop the flourish, flag the
   conflict. Never retcon for drama.
4. **No pillar parody** — the pillars are craft sources, not brands to
   imitate loudly. Never name-drop them in generated fiction, never copy
   protected text, characters, or proper nouns from them.
5. **Tone floor** — adult, slow-build, no modern slang, no fourth-wall
   winks, no victory without cost (inherited from
   `rumblingstone-campaign/references/campaign-coherence.md` §4).

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
