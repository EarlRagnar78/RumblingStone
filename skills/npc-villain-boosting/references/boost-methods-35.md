# Boost Methods — D&D 3.5 SRD (Improving Monsters)

Source: https://www.d20srd.org/srd/improvingMonsters.htm (DMG ch. 5).
This is the RAW path — full fidelity, produces a legal 3.5 stat block.

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

Also recompute: size mod to attack/AC (M +0, L −1, H −2, G −4, C −8),
grapple special size mod (L +4, H +8, G +12, C +16), space/reach, and step
damage dice up one size (1d6→1d8→2d6→2d8/3d6…). A size-category jump
normally justifies **an additional +1 CR** on top of the HD table — the SRD
treats the table as a guide; benchmark the result (see below).

## 2. Templates (SRD, with CR adjustment)

| Template | CR | Notes |
|---|---|---|
| Celestial / Fiendish | +0 (HD ≤3), +1 (HD 4–7), +2 (HD 8+) | resistances, SR, smite 1/day |
| Half-Celestial / Half-Fiend | +1 (HD ≤5 / ≤4), +2 (mid), +3 (HD 11+) | big ability boosts, SLAs, wings |
| Half-Dragon | +2 | +8 Str, +2 Int/Cha, breath 1/day, immunity |
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
  **CR +1 per 2 levels**, until the class levels equal the racial HD; beyond
  that they count as associated. NPC classes (warrior, adept…) are always
  nonassociated. `[Verify wording vs d20srd Improving Monsters]`
- A humanoid with 1 racial HD drops it when taking its first class level
  (build as a classed character: PC classes CR = level; NPC classes
  CR = level − 1).
- Class levels are the *only* boost that scales spellcasting DCs — for caster
  villains at APL 13 they are usually the correct knob.

## 4. Elite array & equipment (humanoid PNGs, 5 minutes)

- Elite array 15/14/13/12/10/8 replaces the standard array — this alone is
  what turns a "warrior 1" into a credible sergeant (DMG: nonelite vs elite).
- NPC gear budget: DMG Table 4–23 (level 13 NPC ≈ 21,000 gp
  `[Verify — DMG p.127]`). A +2 weapon and +1 to-hit is often a better boost
  than 4 HD, and the party can loot it — self-balancing.
- Potions/scrolls/wands on the villain = spike power *during* the fight
  without permanent wealth inflation.

## Always finish: benchmark

Additive CR (+1 here, +2 there) drifts. After any 3.5 boost, compare final
AC / hp / attack / DCs to the PF1e Monster-Statistics-by-CR row
(`pathfinder-1e-srd/references/monster-advancement.md`) and set the CR the
numbers actually earn. Award XP from that final CR.
