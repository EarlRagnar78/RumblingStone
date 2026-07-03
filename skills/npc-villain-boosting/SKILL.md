---
name: npc-villain-boosting
description: >
  Decision framework + workflow for boosting (or de-boosting) NPCs (PNG),
  villains, and monsters in the RumblingStone campaign. Combines D&D 3.5 SRD
  advancement (HD, templates, class levels) with Pathfinder 1e simple templates
  and CR benchmarks. Trigger on "boost", "potenziare", "buff the villain",
  "too easy", "too hard", "upscale", "the party is level 13 and the monster is
  CR 9", "make this boss survive", "advance this monster", "add class levels".
---

# NPC / Villain / Monster Boosting — When, Whether, How

The party (4 PCs, level 13, artifact-heavy — see
`rumblingstone-campaign/references/campaign-party.md`) outguns most printed
*Red Hand of Doom* content, which is written for levels 5–12. This skill
decides **when a boost is needed, whether it is worth it, and which method
to use** — then hands off to the method references.

**Load order for a boost request:**
1. This file (decision).
2. `references/boost-decision.md` (is it worth it? which knob?).
3. Method file: `references/boost-methods-35.md` (3.5 SRD advancement) and/or
   `pathfinder-1e-srd/references/monster-advancement.md` (PF simple templates).
4. `references/boost-workflow.md` (recalculation checklist + output template).
5. `campaign/state.md` + `rumblingstone-campaign/references/campaign-coherence.md`
   before boosting any *named* PNG — a boost must not contradict established
   fiction (a villain the party already fought doesn't silently gain 6 HD).

## The 60-second decision

```
Is the encounter under-tuned for APL 13?
├─ No → DON'T BOOST. Not every fight must threaten. Mook fights are pacing.
└─ Yes → Is the problem action economy (1 monster vs 4 PCs)?
    ├─ Yes → ADD BODIES first (minions/bodyguards), boost second.
    │        Doubling equal-CR creatures = EL +2 (3.5 DMG math).
    └─ No → Is the fight happening THIS session?
        ├─ Yes → PF1e SIMPLE TEMPLATE (Advanced/Giant, quick rules).
        │        One line, CR +1 each, no rebuild.
        └─ No (prep time) → 3.5 advancement: HD, template, or class
                 levels. Then BENCHMARK vs PF Table 1-1 and log it.
```

## Hard limits (always enforced)

- **EL cap:** boosted encounter EL ≤ APL + 4 unless the DM explicitly wants a
  "flee or die" set-piece (must be signposted in the fiction and have an exit).
- **Visibility rule:** every +1 CR must buy something the players *feel*
  (to-hit/DC pressure or survivability) — never boost bookkeeping-only.
- **Coherence rule:** boosts to named PNGs/villains are permanent and must be
  written to the PNG's file (`PNG/` or `campaign/npcs/`) with a
  `Boost log:` line (date, method, CR before → after). No stealth retcons.
- **No invention:** boosted stats derive from SRD/PF1e rules cited in the
  method files. Uncertain values are flagged `[INFERRED — needs DM
  confirmation]` per `AGENTS.md`.

## Domain → File

| Question | File |
|---|---|
| Should I boost? Which method? EL/XP math | `references/boost-decision.md` |
| 3.5 SRD: add HD, size changes, templates, class levels | `references/boost-methods-35.md` |
| PF1e: simple templates, stats-by-CR benchmark | `pathfinder-1e-srd/references/monster-advancement.md` |
| Step-by-step rebuild checklist + output format + worked example | `references/boost-workflow.md` |
