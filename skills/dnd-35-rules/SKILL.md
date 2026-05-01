---
name: dnd-35-rules
description: >
  Meta-router skill kept for backwards compatibility. Real content was split
  into three focused skills: dnd-35-srd (mechanics), forgotten-realms-lore
  (1372 DR setting), and rumblingstone-campaign (this campaign). Trigger words
  identical to those three skills combined.
---

# D&D 3.5 Rules — Meta Router

This skill is a routing entrypoint. The actual reference content was split into
three skills so agents only load what's relevant:

| If the question is about... | Load skill |
|---|---|
| Pure 3.5 mechanics, SRD rules, generic d20 | `dnd-35-srd` |
| Forgotten Realms canon (1372 DR), deities, regions, factions | `forgotten-realms-lore` |
| RumblingStone campaign, the four PCs, custom artifacts, current arc | `rumblingstone-campaign` |

Most questions need exactly one of the three. A typical campaign-prep
question may need all three — load them in this order:

1. `rumblingstone-campaign/SKILL.md` (and its `references/campaign-coherence.md`
   plus `campaign/state.md`) — establishes what is currently true.
2. `forgotten-realms-lore/SKILL.md` — establishes the setting frame.
3. `dnd-35-srd/SKILL.md` — establishes the rules frame.

## Why three skills, not one

The previous monolithic skill loaded ~60K tokens of references for any query.
Splitting lets agents load only the relevant tree:

- A pure rules question loads ~6–10K tokens (SRD only).
- A lore question loads ~4–8K tokens (FR only).
- A campaign question loads ~5–12K tokens (campaign + state).

If a question genuinely needs all three, the split costs nothing extra; it
only saves tokens when the question is narrow (most of the time).
