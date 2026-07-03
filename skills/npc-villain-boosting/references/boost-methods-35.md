# Boost Methods — D&D 3.5 SRD (Improving Monsters)

Source: https://www.d20srd.org/srd/improvingMonsters.htm (DMG ch. 5).
This is the RAW path — full fidelity, produces a legal 3.5 stat block.
All tables verified against the official WotC 3.5 SRD distribution
(`ImprovingMonsters`, 2026-07-03).

Three levers: **more Hit Dice**, **a template**, **class levels**. Plus the
cheap fourth lever for humanoids: **elite array + equipment**.

---

## 1. Advancing Hit Dice

Every monster's stat block has an `Advancement:` line (e.g. Troll:
`7–9 HD (Large); 10–14 HD (Huge)`). Stay inside it to stay RAW.

Each added HD grants:

- hp: +1 die of the type's HD (see type table in
  `dnd-35-srd/references/monsters.md`) + Con mod
- BAB and saves: per type progression (recompute at new total HD)
- Skill points: per type + Int mod
- Feats: total = 1 + (total HD ÷ 3, rounded down) → new feat at 6, 9, 12… HD
- Ability increase: +1 at every 4th total HD

**CR increase per added HD** (Table: Improved Monster CR Increase):

| Original type | CR +1 per |
|---|---|
| Aberration, construct, elemental, fey, giant, humanoid, ooze, plant, undead, vermin | 4 HD added |
| Animal, magical beast, monstrous humanoid | 3 HD added |
| Dragon, outsider | 2 HD added |

### Size increases

If added HD push the creature into the next size bracket of its Advancement
line, apply Table: Changes to Statistics by Size:

| Old → New size | Str | Dex | Con | Natural armor |
|---|---|---|---|---|
| Tiny → Small | +4 | −2 | — | — |
| Small → Medium | +4 | −2 | +2 | — |
| Medium → Large | +8 | −2 | +4 | +2 |
| Large → Huge | +8 | −2 | +4 | +3 |
| Huge → Gargantuan | +8 | — | +4 | +4 |
| Gargantuan → Colossal | +8 | — | +4 | +5 |

Repeat the adjustment per size category gained. Also recompute: size mod
to attack/AC (M +0, L −1, H −2, G −4, C −8), grapple special size mod
(L +4, H +8, G +12, C +16), space/reach, and step damage dice up one size
per category (1d2→1d3→1d4→1d6→1d8→2d6→3d6; 1d10→2d8→3d8).

**Other RAW CR modifiers** (SRD, Table: Improved Monster CR Increase):
size increased to Large or larger **+1 CR**; elite array instead of
standard **+1 CR** (not if advanced by class levels — those already assume
it); added special attacks/qualities that significantly improve combat
**+2 CR**, minor ones **+1 CR**. The added-HD CR increase does **not**
stack with a class-level CR increase — use one or the other.

## 2. Templates (SRD, with CR adjustment)

| Template | CR | Notes |
|---|---|---|
| Celestial / Fiendish | +0 (HD ≤3), +1 (HD 4–7), +2 (HD 8+) | resistances, SR, smite 1/day |
| Half-Celestial / Half-Fiend | +1 (HD ≤5 / ≤4), +2 (mid), +3 (HD 11+) | big ability boosts, SLAs, wings |
| Half-Dragon | +2 (min 3) | +8 Str, +2 Con/Int/Cha, breath 1/day, immunity |
| Lich | +2 | undead, touch attack, fear aura, phylactery |
| Vampire | +2 | undead, energy drain, dominate; weaknesses |
| Ghost | +2 | incorporeal, manifestation powers |
| Skeleton / Zombie | rebuild | replaces abilities wholesale; CR from new HD |

Templates buy **gimmicks** (immunities, auras, modes of attack) more than raw
numbers — ideal for making a returning villain *feel different*, not just
bigger. Full template text: d20srd.org/srd/monsters/[templateName].htm.

## 3. Class levels (villains and named PNGs)

- **Associated class** (amplifies what the monster already does — barbarian/
  fighter on a brute, sorcerer on a Cha-caster with SLAs): **CR +1 per level**.
- **Nonassociated class** (works against the chassis — wizard on an ogre):
  **CR +1 per 2 levels**, until the nonassociated class levels equal the
  creature's original HD; from that point each additional level of the same
  (or a similar) class is associated, +1 CR each. NPC classes (warrior,
  adept…) are always nonassociated. (Verified vs SRD Improving Monsters.)
- A humanoid with 1 racial HD drops it when taking its first class level
  (build as a classed character: PC classes CR = level; NPC classes
  CR = level − 1).
- Class levels are the *only* boost that scales spellcasting DCs — for caster
  villains at APL 13 they are usually the correct knob.

## 4. Elite array & equipment (humanoid PNGs, 5 minutes)

- Elite array 15/14/13/12/10/8 replaces the standard array (RAW **+1 CR**
  on a monster; PC-classed NPCs use it by default). Nonelite array is
  13/12/11/10/9/8. This alone turns a "warrior 1" into a credible sergeant.
- NPC gear budget: DMG Table 4–23 (non-SRD; verify in your copy). The
  verified PF1e equivalent — Core Rulebook, Table: NPC Gear — prices a
  heroic level-13 NPC at 27,000 gp and works fine at a 3.5 table (see
  `pathfinder-1e-srd/references/npc-building.md`). A +2 weapon and +1
  to-hit is often a better boost than 4 HD, and the party can loot it —
  self-balancing.
- Potions/scrolls/wands on the villain = spike power *during* the fight
  without permanent wealth inflation.

## Always finish: benchmark

Additive CR (+1 here, +2 there) drifts. After any 3.5 boost, compare final
AC / hp / attack / DCs to the PF1e Monster-Statistics-by-CR row
(`pathfinder-1e-srd/references/monster-advancement.md`) and set the CR the
numbers actually earn. Award XP from that final CR.
