---
name: rumblingstone-campaign
description: >
  RumblingStone campaign reference — Red Hand of Doom adapted to the
  Cannath Vale (Forgotten Realms, 1372 DR). Use for questions about the four
  PCs (Thorik, Tordek, Hella, Artemis), custom artifacts (Aegis Fang, Corona
  di Adamantio, Ring of Chaotic Illumination, Bracieri Gemelli, Collana dei
  Semi Eterni, Cuore di Moradin), campaign villains/allies (Il Collezionista,
  Sonjak, Therysol), arc progression, DM strategy (Shine Time, State Machine,
  Triangolo di Rischio), and coherence constraints. Trigger on PC names, "what
  arc", "what's next session", "Shine Time", "State Machine", "RumblingStone".
---

# RumblingStone — Campaign Reference

Custom campaign material for the RumblingStone D&D 3.5 game. For pure
mechanics load `dnd-35-srd`. For Forgotten Realms canon load
`forgotten-realms-lore`. This skill ONLY contains custom campaign content.

**Critical loading order for any campaign question:**

1. `references/campaign-coherence.md` — what must stay consistent
2. `../../campaign/state.md` — current world state (changes per session)
3. The specific reference for the domain

If `state.md` and a reference disagree, **state.md wins** (it is the most
recent truth). If a reference and `campaign/lore/campaign-history.md`
disagree, the reference wins (history is prose narration; references are
structured truth).

## Domain → File

| Domain | File |
|---|---|
| Coherence rules — must-not-violate constraints | `references/campaign-coherence.md` |
| Party — Thorik, Tordek, Hella, Artemis stats and history | `references/campaign-party.md` |
| DM Strategy — Shine Time, State Machine, Triangolo di Rischio | `references/campaign-dm-strategy.md` |
| Custom artifacts — Aegis Fang, Corona, Ring, Bracieri, Collana, Cuore | `references/campaign-artifacts.md` |
| Story arcs — timeline, current state, villain/ally tracker | `references/campaign-story-arcs.md` |
| DM toolkit — branching quests, monster art, faction expansion | `references/dm-expansion-toolkit.md` |
| Living world state (per-session) | `../../campaign/state.md` |
| Full prose history | `../../campaign/lore/campaign-history.md` |
| House rules | `../../campaign/lore/house-rules.md` |

## Decision Logic

- "Who is Thorik / Tordek / Hella / Artemis?" → `campaign-party.md`
- "What does the Corona / Ring / Bracieri / Collana do?" → `campaign-artifacts.md`
- "What arc is the party in?" → `campaign-story-arcs.md` + `state.md`
- "Who is Il Collezionista / Sonjak / Therysol?" → `campaign-party.md` (NPCs section)
- "What happened at the Mine / Fungi Tower / Eternal Forge?" → `campaign-story-arcs.md`
- "How do I DM for Artemis?" / "What is Shine Time?" → `campaign-dm-strategy.md`
- "Can NPC X already know Y?" / "Has artifact Z been used yet?" → `campaign-coherence.md` + `state.md`
- "Generate a quest / monster image" → `dm-expansion-toolkit.md`

## Coherence Discipline (read this every time)

Before generating any new campaign content, the agent must:

1. Check `campaign-coherence.md` for the relevant constraint family
   (history-locked events, artifact powers, NPC knowledge, PG promises).
2. Read the relevant section of `state.md` for current truth.
3. If proposing something that contradicts a constraint, **stop and flag it
   to the DM** — do not silently retcon.
4. Default tone: R.A. Salvatore — slow build, sensory detail, internal stakes,
   moral cost. Avoid camp, anachronism, modern jargon.

## Adult Group Conventions

- "Premium Design": no empty combats, every encounter has a decision dimension.
- "Shine Time": each session must give at least one PC their personalized hook.
- "Triangolo di Rischio": every dilemma should split the party's resources
  three ways (one PC each, plus a time-pressure cost).
- Reactive State Machine, not linear plot: villains have agendas that advance
  whether or not the party intervenes; track countdown clocks in `state.md`.
