---
name: pathfinder-1e-srd
description: >
  Pathfinder 1st Edition SRD (PRD / OGL) rules — mechanics, monster advancement,
  simple templates, NPC building, and 3.5 <-> PF1e conversion. Use for "Pathfinder",
  "PF1e", "PFRPG", "simple template", "advanced template", "CMB/CMD", "monster
  statistics by CR", "NPC codex", or when backporting Pathfinder material into a
  D&D 3.5 game. This campaign RUNS on D&D 3.5; PF1e is a compatible toolkit used
  mainly to boost NPCs, villains, and monsters quickly.
---

# Pathfinder 1e SRD — Rules & Conversion Toolkit

Pathfinder 1e is a direct evolution of the d20 3.5 system (OGL). ~90% of its
math is drop-in compatible with 3.5. In this repo PF1e serves two purposes:

1. **Boost toolkit** — simple templates and benchmark tables to strengthen
   NPCs/villains/monsters at the table in minutes (see also the
   `npc-villain-boosting` skill, which is the decision layer on top of this).
2. **Rules reference** — when PF1e material (adventure paths, bestiaries,
   NPC Codex) is imported into the 3.5 campaign.

**Sources:** https://aonprd.com (official PRD archive) • https://www.d20pfsrd.com

## Domain → File

| Domain | File |
|---|---|
| PF1e vs 3.5 differences: CMB/CMD, skills, feats, classes, actions | `references/core-differences.md` |
| Monster advancement: simple templates, adding HD/levels, stats-by-CR benchmarks | `references/monster-advancement.md` |
| NPC building: classed NPCs, CR from level, gear by level, arrays | `references/npc-building.md` |
| Converting content 3.5 → PF1e and PF1e → 3.5 | `references/conversion-guide.md` |

## Adjudication Rules

- Same d20 core: d20 + modifier vs DC/AC/save. Specific overrides general.
- **This campaign is D&D 3.5.** When a PF1e rule conflicts with a 3.5 rule at
  the table (e.g., grapple vs CMB, skill names), the **3.5 rule wins** unless
  `campaign/lore/house-rules.md` says otherwise. PF1e numbers (hp, AC, attack,
  DCs) can be imported as-is; PF1e *subsystems* need conversion.
- Cite sources: `[PF1e: Bestiary]`, `[PF1e: Core Rulebook]`, `[PF1e: GameMastery
  Guide]`, with an aonprd.com or d20pfsrd.com URL when possible.
- **Never invent** stat blocks or template effects. Flag uncertain values as
  `[INFERRED — needs DM confirmation]` per repo policy in `AGENTS.md`.

## Web Lookup Templates

```
https://aonprd.com/MonsterDisplay.aspx?ItemName=[Monster+Name]
https://aonprd.com/SpellDisplay.aspx?ItemName=[Spell+Name]
https://aonprd.com/FeatDisplay.aspx?ItemName=[Feat+Name]
https://www.d20pfsrd.com/bestiary/monster-listings/[type]/[monster-name]/
https://www.d20pfsrd.com/bestiary/rules-for-monsters/simple-templates/
```

## Output Templates

**Rule:** one-line answer • **Source:** PF1e book + URL • **3.5 delta:** what
changes at this table • **Example:** brief.

For imported monsters, output the 3.5 SRD stat-block format (see
`dnd-35-srd/references/monsters.md`) with a `Conversion notes:` line listing
every PF1e-only mechanic that was translated.
