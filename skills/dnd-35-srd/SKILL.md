---
name: dnd-35-srd
description: >
  D&D 3.5 SRD (System Reference Document) and OGL rules — pure mechanics with no
  setting bias. Use for character creation, class features, spells, combat, feats,
  ability checks, monsters, magic items, prestige classes, and any rules
  adjudication that does not depend on a specific campaign setting. Trigger on
  "D&D 3.5", "d20 SRD", "3.5 edition", "how does <spell/feat/class feature>
  work", "what's the DC for X", "rules ruling".
---

# D&D 3.5 SRD — Mechanics-Only Reference

Pure d20 SRD content. No Forgotten Realms lore, no campaign state.
For setting questions load `forgotten-realms-lore`. For RumblingStone
campaign questions load `rumblingstone-campaign`.

**Source:** https://www.d20srd.org

## Domain → File

| Domain | File |
|---|---|
| Core: ability scores, skills, saves, BAB, DCs, XP, encumbrance | `references/core-mechanics.md` |
| Classes, multiclassing, level tables, psionics | `references/classes.md` |
| Spells, slots, metamagic, schools, psionic powers | `references/spells.md` |
| Combat: actions, conditions, AoO, grapple, terrain | `references/combat.md` |
| Monsters, CR, templates | `references/monsters.md` |
| Items: magic, psionic, crafting, wondrous, wands | `references/items.md` |
| External tools, d20srd URLs, dndtools.one | `references/resources.md` |

## Adjudication Rules

- d20 + modifier vs DC or AC/save. Specific overrides general.
- State **RAW vs RAI** when ambiguous; provide both if needed.
- Action economy: Standard / Move / Free / Swift / Immediate / Full-round.
- Always cite source: SRD section or `[Non-SRD: <book>]`.

## Web Lookup Templates

```
https://www.d20srd.org/srd/spells/[spellNameCamelCase].htm
https://www.d20srd.org/srd/classes/[className].htm
https://www.d20srd.org/srd/monsters/[monsterName].htm
https://www.imarvintpa.com/dndLive/spells.php?ID=[id]
```

## Output Templates

**Rule:** one-line answer • **Source:** SRD section / book p.X • **Example:** brief • **Edge cases:** if relevant.

For spells use SRD spell-block format. For monsters use SRD stat-block format.

## Non-SRD Policy

Tome of Battle, Complete series, Expanded Psionics, Draconomicon, Libris Mortis:
flag as `[Non-SRD: <book>]`, describe mechanics if known, recommend user verify
against their copy, never reproduce copyrighted text verbatim.
