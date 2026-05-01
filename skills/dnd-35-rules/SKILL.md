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

# D&D 3.5 Edition Rules — Routing Skill

This SKILL.md is intentionally minimal. **Its only job is routing.** Load the matching reference
file below to get the actual content. Loading every reference at once wastes tokens.

**Primary source:** d20 SRD 3.5 — https://www.d20srd.org
**Secondary:** Forgotten Realms Wiki, IMarvinTPA Spell DB.

---

## Loading Protocol (read this once)

1. Identify the domain → match the table below.
2. Load **only** the file(s) listed for that domain.
3. Cite source: SRD section, book + page, or wiki URL.
4. Flag non-SRD content as `[Non-SRD: <book>]` or `[Private — Red Hand of Doom, p.X]`.
5. **Never invent** stat blocks, spell effects, or NPC stats not in the files.

If a campaign question depends on current world state, also load
`../../campaign/state.md` (single source of truth for what's currently true in the world).

---

## Domain → File Map

### Core d20 Rules (SRD / OGL)

| Domain | File |
|---|---|
| Core mechanics, ability scores, skills, saves, XP, encumbrance, BAB, DCs | `references/core-mechanics.md` |
| Base & expanded classes, multiclassing, Psionics, level tables | `references/classes.md` |
| Spells, spell slots, metamagic, schools, psionic powers | `references/spells.md` |
| Combat, actions, conditions, AoO, grapple, terrain | `references/combat.md` |
| Monsters, CR, templates, Draconomicon, Libris Mortis | `references/monsters.md` |
| Magic & psionic items, crafting, wondrous items, wands | `references/items.md` |
| Free tools, d20srd.org URLs, VTT, dndtools.one | `references/resources.md` |

### Forgotten Realms — Lore & Setting

| Domain | File |
|---|---|
| FR overview, Weave/Shadow Weave, calendar | `references/forgotten-realms.md` |
| All deities — Faerûnian, Drow, Elven, Dwarven, Gnomish, Halfling, Orc, Dragon | `references/fr-deities-complete.md` |
| All regions — Sword Coast, Heartlands, North, Moonsea, Dalelands, Underdark | `references/fr-regions-complete.md` |
| All races & subraces — humans, elves, drow, duergar, genasi, planetouched | `references/fr-races-complete.md` |
| Factions — Harpers, Zhentarim, Red Wizards, cults, guilds | `references/fr-factions.md` |
| Prestige classes — FR, Complete series, Draconomicon, Libris Mortis | `references/fr-prestige-classes.md` |
| Feats — Regional, Divine, FR-specific | `references/fr-feats.md` |
| History & timeline — ancient empires → 1372 DR | `references/fr-history.md` |
| Artifacts — Nether Scrolls, Moonblades, Tablets of Fate | `references/fr-artifacts.md` |
| Cannath Vale — RHoD adapted location/NPC mapping | `references/fr-cannath-vale.md` |

### Campaign-Specific (RumblingStone)

| Domain | File |
|---|---|
| Party — Thorik, Tordek, Hella, Artemis stats and history | `references/campaign-party.md` |
| DM Strategy — Shine Time, State Machine, Triangolo di Rischio | `references/campaign-dm-strategy.md` |
| Campaign artifacts — Aegis Fang, Corona, Ring, Bracieri, Collana, Cuore | `references/campaign-artifacts.md` |
| Story arcs — timeline, current state, villain/ally tracker | `references/campaign-story-arcs.md` |
| Coherence rules — what must stay consistent across sessions | `references/campaign-coherence.md` |
| Branching quests, monster art, faction tracker | `references/dm-expansion-toolkit.md` |
| Current world state (changes per session) | `../../campaign/state.md` |

---

## Decision Logic — Quick Examples

- "Who is god of X?" → `fr-deities-complete.md`
- "Tell me about Waterdeep / Thay / Menzoberranzan" → `fr-regions-complete.md`
- "What feats from the Dalelands?" → `fr-feats.md`
- "What does [artifact name] do?" → `fr-artifacts.md` (canon FR) or `campaign-artifacts.md` (custom)
- "Who is Thorik / Tordek / Hella / Artemis?" → `campaign-party.md`
- "How do I DM for Artemis?" / "What is Shine Time?" → `campaign-dm-strategy.md`
- "What arc is the party in?" / "Campaign timeline" → `campaign-story-arcs.md` + `state.md`
- "Who is Il Collezionista / Sonjak / Therysol?" → `fr-factions.md` (campaign section) or `campaign-party.md` (NPCs)
- "Where is Brindol / Rhest?" → `fr-cannath-vale.md`
- "Generate monster image / quest" → `dm-expansion-toolkit.md`
- "Can NPC X already know Y?" / "Has artifact Z been used yet?" → `campaign-coherence.md` + `state.md`

---

## Adjudication Principles (very short — full text in `core-mechanics.md`)

- d20 + modifier vs DC or AC/save; specific overrides general.
- State **RAW vs RAI** when ambiguous; give both.
- Action economy: Standard / Move / Free / Swift / Immediate / Full-round.
- **Rules ranking:** house rules (`campaign/lore/house-rules.md`) > SRD > splatbook RAW > RAI.
- **Coherence ranking:** `campaign/state.md` > `campaign-story-arcs.md` > `campaign-history.md` > inferred.

If two sources disagree, the higher rank wins and you flag the conflict for the DM.

---

## Web Lookup Templates (when you need exact SRD text)

```
https://www.d20srd.org/srd/spells/[spellNameCamelCase].htm
https://www.d20srd.org/srd/classes/[className].htm
https://www.d20srd.org/srd/monsters/[monsterName].htm
https://forgottenrealms.fandom.com/wiki/[Article_Name]
https://www.imarvintpa.com/dndLive/spells.php?ID=[id]
```

---

## Output Templates

**Rules ruling:**
```
Rule: <one-line answer>
Source: <SRD section / book p.X>
Example: <one-line>
Edge cases: <only if relevant>
```

**Spell:** standard SRD block (School, Level, Components, Range, Duration, Save, SR, Description).
**Monster:** standard SRD stat block.
**Lore:** canonical answer → source → flag any 4e/5e retcon explicitly (this campaign is 1372 DR).

---

## Non-SRD Content Policy

For Tome of Battle, Complete series, Expanded Psionics, Draconomicon, Libris Mortis, FRCS:

1. State `[Non-SRD: <book name>]`.
2. Describe mechanics if known; recommend user verify against their copy.
3. Never reproduce copyrighted text verbatim.
