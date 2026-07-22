---
name: dnd-35-rules
description: >
  Meta-router skill kept for backwards compatibility (docs and older agent
  configs still point here). Real content was split into focused skills:
  dnd-35-srd (mechanics), forgotten-realms-lore (1372 DR setting),
  rumblingstone-campaign (this campaign), pathfinder-1e-srd (PF1e rules +
  conversion), npc-villain-boosting (boost/advance NPCs, villains, monsters),
  rumblingstone-narrative-style (style engine for generated content),
  rumblingstone-mapmaking (battle-map pipeline), rumblingstone-automation
  (dm.py CLI + session-state pipeline), rumblingstone-plans (plan-archive
  discipline). Trigger words identical to those skills combined.
---

# D&D 3.5 Rules — Meta Router (legacy)

This skill is a routing entrypoint only — it has no reference content of its
own. The actual material was split into focused skills so agents load only
what's relevant:

| If the question is about... | Load skill |
|---|---|
| Pure 3.5 mechanics, SRD rules, generic d20 | `dnd-35-srd` |
| Forgotten Realms canon (1372 DR), deities, regions, factions | `forgotten-realms-lore` |
| RumblingStone campaign, the four PCs, custom artifacts, current arc | `rumblingstone-campaign` |
| Pathfinder 1e rules, PF↔3.5 conversion, simple templates, CR benchmarks | `pathfinder-1e-srd` |
| Boosting/advancing a PNG, villain, or monster ("too easy", "upscale", "potenziare") | `npc-villain-boosting` |
| Generating narrative content — quests, prose, read-aloud, dialogue, hooks, recaps ("genera", "scrivi") | `rumblingstone-narrative-style` |
| Battle maps — creating, rendering, JSON contract, UVTT export ("mappa", "griglia") | `rumblingstone-mapmaking` |
| Session lifecycle & scripts — `dm.py`, "fine sessione", recap, brief, `state.md`, Homebrewery | `rumblingstone-automation` |
| Work plans, lotti, INDEX/CHANGELOG, ADRs ("piano", "traccia le modifiche") | `rumblingstone-plans` |

A typical campaign-prep question loads, in this order:

1. `rumblingstone-campaign/SKILL.md` (and its `references/campaign-coherence.md`
   plus `campaign/state.md`) — establishes what is currently true.
2. `forgotten-realms-lore/SKILL.md` — establishes the setting frame.
3. `dnd-35-srd/SKILL.md` — establishes the rules frame.

Any *generation* request additionally loads `rumblingstone-narrative-style`
(mandatory style engine — AGENTS.md rule 11).

## Why split skills, not one

The previous monolithic skill loaded ~60K tokens of references for any query.
Splitting lets agents load only the relevant tree (a narrow question costs
~4–12K tokens instead of ~60K). If a question genuinely needs several trees,
the split costs nothing extra.

## Deprecation status

New docs must reference the focused skills directly, never this router.
This shim gets removed the day nothing in the repo (and no supported agent
config) points at `dnd-35-rules` anymore.
