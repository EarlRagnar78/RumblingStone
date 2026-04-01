---
name: dnd-35-rules
description: >
  Comprehensive D&D 3.5 Edition rules assistant and referee. Use this skill whenever the user
  asks about D&D 3.5, d20 System, or Forgotten Realms 3.5 rules — including character creation,
  class features, spells, combat, feats, skills, ability checks, monsters, prestige classes,
  Forgotten Realms lore, or any rules adjudication. Trigger on phrases like "D&D 3.5",
  "d20 SRD", "3.5 edition", "Forgotten Realms", "DM ruling", "how does [spell/feat/class feature]
  work in 3.5", "can my character do X", or any tabletop RPG question rooted in the 3.5 ruleset.
  Also trigger for session prep, encounter building, NPC creation, and lore lookups for Faerûn.
---

# D&D 3.5 Edition Rules Reference

Primary source: **d20 SRD 3.5** (Open Game License) — `https://www.d20srd.org`
Secondary sources: **Forgotten Realms Wiki** (fandom.com/wiki/Forgotten_Realms_Wiki),
**IMarvinTPA Spell DB** (`https://www.imarvintpa.com/dndLive/spells.php`)

---

## How to Use This Skill

1. **Identify the domain** of the question using the table below.
2. **Load the relevant reference file** with the `view` tool before answering.
3. **Cite the source** (SRD section, book + page, or wiki) in every rules ruling.
4. **Flag non-SRD content** clearly — distinguish OGL/SRD from splatbook content.

### Domain → Reference File Map

#### Core d20 Rules (SRD / OGL)

| Question domain | Load file |
|---|---|
| Core mechanics, ability scores, skills, saves, XP, encumbrance | `references/core-mechanics.md` |
| Base classes, multiclassing, class features, level tables | `references/classes.md` |
| Spells, spell slots, metamagic, schools, key spell list | `references/spells.md` |
| Combat, actions, conditions, AoO, grapple, terrain | `references/combat.md` |
| Monsters, creature types, CR, templates, encounter distance | `references/monsters.md` |
| Magic items, crafting, pricing, wondrous items, wands/scrolls | `references/items.md` |
| Free/open tools, d20srd.org URLs, VTT, local AI RAG setup | `references/resources.md` |

#### Forgotten Realms — Lore & Setting

| Question domain | Load file |
|---|---|
| FR overview, quick ref: regions, Weave, Shadow Weave, calendar | `references/forgotten-realms.md` |
| **All deities** — Faerûnian, Drow, Elven, Dwarven, Gnomish, Halfling, Orcish, Dragon pantheons | `references/fr-deities-complete.md` |
| **All regions** — Sword Coast, Heartlands, North, Moonsea, Dalelands, East, South, Underdark | `references/fr-regions-complete.md` |
| **All races & subraces** — Human variants, elf subraces, drow, duergar, genasi, planetouched | `references/fr-races-complete.md` |
| **Factions & organizations** — Harpers, Zhentarim, Red Wizards, cults, guilds, knightly orders | `references/fr-factions.md` |
| **Prestige classes** — FR-specific PrCs from FRCS, Races of FR, Unapproachable East, etc. | `references/fr-prestige-classes.md` |
| **Feats** — Regional feats, Divine feats, FR-specific general and metamagic feats | `references/fr-feats.md` |
| **History & timeline** — Ancient empires, Time of Troubles, key events 1–1372 DR | `references/fr-history.md` |
| **Artifacts & legendary items** — Nether Scrolls, Moonblades, Tablets of Fate, named items | `references/fr-artifacts.md` |
| **Campaign setting** — Cannath Vale (Elsir Vale → Dalelands), RHoD location/NPC mapping | `references/fr-cannath-vale.md` |
| **Monster art + upscaling** — AI prompts (SD/DALL-E), VTT token workflow | `references/dm-expansion-toolkit.md` |
| **Branching quests + DM toolkit** — quest trees, artifact chains, villain expansion, faction tracker | `references/dm-expansion-toolkit.md` |
| **All sources + URLs** — dndtools.one, realmshelps.net, orbitalflower Wayback patterns | `references/resources.md` |

#### Campaign-Specific (RumblingStone)

| Question domain | Load file |
|---|---|
| **Party composition** — Thorik, Tordek, Hella, Artemis, Rumbling Stone group, PCs | `references/campaign-party.md` |
| **Campaign artifacts** — Aegis Fang, Corona di Adamantio, Ring of Chaotic Illumination, Bracieri Gemelli, Collana dei Semi Eterni, Cuore di Moradin | `references/campaign-artifacts.md` |
| **Campaign story arcs** — Timeline, what happened, what's next, current state, arc index, villain/ally tracker | `references/campaign-story-arcs.md` |
| **Campaign factions** — Il Collezionista, Sonjak, Githyanki, Circle of Eight, Hammerfist | `references/fr-factions.md` (campaign section) |
| **Underdark geography** — Eternal Forge, dungeon chain, Fire/Earth/Temporal planes | `references/fr-cannath-vale.md` (Underdark section) |

#### Decision Logic for FR Questions
- "Who is the god of X?" → `fr-deities-complete.md`
- "What domains does deity X grant?" → `fr-deities-complete.md`
- "Tell me about Waterdeep / Thay / Rashemen / Menzoberranzan" → `fr-regions-complete.md`
- "What prestige class should a [class] take in FR?" → `fr-prestige-classes.md` + `classes.md`
- "What feats are available from the Dalelands?" → `fr-feats.md`
- "Tell me about the Harpers / Zhentarim / Red Wizards" → `fr-factions.md`
- "What happened during the Time of Troubles?" → `fr-history.md`
- "What does [artifact name] do?" → `fr-artifacts.md`
- "What are the drow racial abilities?" → `fr-races-complete.md`
- "Where is Brindol / Rhest / the Blackfens in FR?" → `fr-cannath-vale.md`
- "Generate a monster image / token" → `dm-expansion-toolkit.md`
- "Give me a quest for [artifact] / [villain]" → `dm-expansion-toolkit.md`
- "How do I use dndtools.one / realmshelps.net / the WotC archive?" → `resources.md`
- "Who is Thorik / Tordek / Hella / Artemis?" → `campaign-party.md`
- "What does the Corona / Ring / Bracieri / Collana do?" → `campaign-artifacts.md`
- "What happened at the Mine / Fungi Tower / Eternal Forge?" → `fr-cannath-vale.md` (Underdark)
- "Who is Il Collezionista / Sonjak?" → `fr-factions.md` (campaign section)
- "What arc is the party in?" / "What's next?" / "Campaign timeline" → `campaign-story-arcs.md`
- "What happened after Drellin's Ferry / Hammerfist / the Underdark?" → `campaign-story-arcs.md`
- "Who is Therysol / Zalkatar?" → `campaign-party.md` (NPCs section)

---

## Core Principles for Rules Adjudication

### The d20 System Contract
- **Roll d20 + modifier vs. DC or opponent's AC/save.** Everything resolves this way.
- **Specific overrides General.** A class feature that says "you may" trumps a general rule that says "you may not."
- **Actions cost action economy.** Always clarify: Standard / Move / Free / Swift / Immediate / Full-Round.
- **RAW vs. RAI.** State which you're providing. If ambiguous, give both interpretations.

### Ability Scores
| Score | Modifier formula |
|---|---|
| 1 | −5 |
| 2–3 | −4 |
| 4–5 | −3 |
| 6–7 | −2 |
| 8–9 | −1 |
| 10–11 | +0 |
| 12–13 | +1 |
| 14–15 | +2 |
| 16–17 | +3 |
| 18–19 | +4 |
| 20–21 | +5 |

**Formula:** `floor((score − 10) / 2)`

### The Six Saves
3.5 has **three** saving throws (not five):
- **Fortitude** (CON) — poison, disease, death effects, massive damage
- **Reflex** (DEX) — traps, area spells, falls
- **Will** (WIS) — mind-affecting, illusions, enchantments

Good save progression: +2 at level 1, +0.5/level → total `2 + floor(level/2)`
Poor save progression: +0 at level 1, +0.33/level → total `floor(level/3)`

---

## Quick Reference: Key DCs

| Task | DC |
|---|---|
| Very Easy | 5 |
| Easy | 10 |
| Average | 15 |
| Tough | 20 |
| Challenging | 25 |
| Formidable | 30 |
| Heroic | 35 |
| Nearly Impossible | 40 |

---

## Character Creation Checklist

1. **Choose race** → apply racial modifiers to ability scores, note special abilities
2. **Assign ability scores** (point buy 28 pts standard; elite array: 15,14,13,12,10,8)
3. **Choose class(es)** → record HD, BAB progression, saves, class skills
4. **Apply racial modifiers** to saves, skills, AC
5. **Allocate skill points** = (class base + INT mod) × 4 at level 1; ×1 thereafter
6. **Choose feats** (1 at level 1 + bonus feats; +1 every 3 levels: 3,6,9…)
7. **Buy equipment** (standard starting gold by class)
8. **Calculate derived stats**: HP, AC, Initiative, Speed, Attack bonus

---

## BAB Progressions

| Progression | Per level | Classes |
|---|---|---|
| Full (+1/lvl) | BAB = level | Fighter, Paladin, Ranger, Barbarian |
| 3/4 | BAB = ¾ level | Cleric, Druid, Rogue, Bard, Monk |
| 1/2 | BAB = ½ level | Wizard, Sorcerer |

**Iterative attacks** at BAB +6: second attack at BAB−5; +11: third at BAB−10; +16: fourth.

---

## Skill System Summary

- **Class skill** max ranks = character level + 3
- **Cross-class skill** max ranks = (character level + 3) / 2
- **Cost**: 1 skill point per rank in class skill; 2 skill points per rank in cross-class
- **Untrained**: most skills CAN be used untrained; some require training (marked in SRD)
- **Take 10**: allowed when not threatened or distracted
- **Take 20**: 20× the time, assumes all results tried; treated as roll of 20; fails if penalties for failure

---

## Encounter Building (Quick)

| EL | Challenge for party of 4 at APL |
|---|---|
| APL − 2 | Easy |
| APL − 1 | Low |
| APL | Standard |
| APL + 1 | High |
| APL + 2 | Severe |
| APL + 4 | Nearly fatal |

EL = CR of single monster, or combined CR for groups (every doubling = +2 EL)

---

## Non-SRD Content Policy

When answering questions about **non-SRD content** (e.g., Tome of Battle, Complete series, Unearthed Arcana variants, Forgotten Realms Campaign Setting prestige classes):
1. State clearly: *"This is non-SRD content from [Book Name]."*
2. Describe mechanics accurately if known from training data.
3. Recommend the user verify against their physical/PDF source.
4. For FR-specific content, load `references/forgotten-realms.md`.

---

## Web Fetching for Live Lookups

When the user needs **exact SRD text** or a **spell/feat not in training data**, use `web_fetch`:

```
# Spell lookup
https://www.d20srd.org/srd/spells/[spellNameCamelCase].htm

# Class page
https://www.d20srd.org/srd/classes/[className].htm

# Monster
https://www.d20srd.org/srd/monsters/[monsterName].htm

# Forgotten Realms lore
https://forgottenrealms.fandom.com/wiki/[Article_Name]

# Spell database (structured)
https://www.imarvintpa.com/dndLive/spells.php?ID=[spell_id]
```

Always prefer fetching live SRD pages over relying on training data for exact rule text.

---

## Response Format Guidelines

**For rules questions:**
```
**Rule:** [concise answer]
**Source:** SRD p. X / [Book] p. Y / d20srd.org/srd/...
**Example:** [brief in-context example]
**Edge cases / common mistakes:** [if relevant]
```

**For spell lookups:**
```
[Spell Name]
School: [school] ([subschool]) [descriptor]
Level: [class] [n]
Components: V, S, M/DF
Casting Time: [time]
Range: [range]
Target/Area/Effect: [...]
Duration: [...]
Saving Throw: [type]; SR: Yes/No
Description: [...]
```

**For monster stat blocks**, use the standard SRD block format.

**For lore / Forgotten Realms:**
- Lead with the canonical answer
- Note the canonical source (FR Campaign Setting 3.5, FRCS, Faiths & Pantheons, etc.)
- Distinguish 3.5-era canon from 4e/5e retcons explicitly
