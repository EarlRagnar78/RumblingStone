# PF1e vs D&D 3.5 — Core Mechanical Differences

Source: PF1e Core Rulebook (aonprd.com). Use this when importing PF1e material
into the 3.5 campaign or reading PF1e stat blocks.

---

## Combat Maneuvers (biggest table-level difference)

3.5 uses opposed checks (grapple, trip, disarm, bull rush…). PF1e unifies them:

- **CMB** (Combat Maneuver Bonus) = BAB + Str mod + size modifier
  (verified, PF size table: Fine −8, Diminutive −4, Tiny −2, Small −1,
  Medium +0, Large +1, Huge +2, Gargantuan +4, Colossal +8 — the inverse
  of the AC/attack size modifiers)
- **CMD** (Combat Maneuver Defense) = 10 + BAB + Str mod + Dex mod + size mod
  (+ deflection/dodge/etc. bonuses to AC)
- Maneuver succeeds on CMB check ≥ CMD.

**Converting PF1e → 3.5 at the table:** ignore CMB/CMD; rebuild the 3.5 grapple
modifier = BAB + Str mod + special size modifier (Large +4, Huge +8,
Gargantuan +12, Colossal +16). A quick approximation: 3.5 grapple ≈ CMB with
the size modifier upgraded from PF's (+1/+2/+3/+4) to 3.5's (+4/+8/+12/+16).

## Skills

PF1e consolidates 3.5 skills:

| PF1e skill | Replaces (3.5) |
|---|---|
| Perception | Spot + Listen + Search |
| Stealth | Hide + Move Silently |
| Acrobatics | Balance + Jump + Tumble |
| Disable Device | Disable Device + Open Lock |
| Linguistics | Speak Language + Decipher Script + Forgery |
| Fly | (new) |

- No cross-class skill *cost*: ranks cost 1 point each; class skills get a flat
  +3 bonus if at least 1 rank is invested. Max ranks = character HD (not HD+3).
- **Converting PF1e → 3.5:** split Perception into Spot/Listen at the same
  bonus; split Stealth into Hide/Move Silently at the same bonus. Close enough
  for NPC/monster use.

## Feats & advancement

- PF1e characters gain a feat at **every odd level** (1, 3, 5, …) vs 3.5's
  every 3rd level. PF1e monsters/NPCs therefore run ~1–2 feats richer.
- Favored class bonus: +1 hp **or** +1 skill point per favored-class level —
  PF1e NPCs have slightly more hp than the 3.5 math predicts. Keep the printed
  hp when importing; it is intended.
- Ability score increase every 4 levels (same as 3.5).

## Classes (headline changes)

- All core classes rebalanced upward: fighters get weapon/armor training,
  paladins get smite that sticks, sorcerers get bloodlines, wizards get school
  powers. **A PF1e classed NPC is stronger than a 3.5 NPC of the same level —
  roughly +1 effective level.** This is a feature when boosting villains.
- Barbarian rage is measured in rounds/day; paladin smites/day scale.
- No PF1e class has 3.5-style dead levels.

## Magic & misc

- Concentration is **not a skill**: check = d20 + caster level + casting
  ability modifier vs DC (defensive casting DC = 15 + 2 × spell level).
- Polymorph school rewritten (fixed bonuses per form instead of full stat
  swap) — do NOT import PF1e polymorph rulings into 3.5 or vice versa.
- Turn undead → Channel Energy (30-ft burst, damage/heal). Convert clerics
  back to 3.5 turning when importing, or keep channel as a house-ruled burst.
- Death at −Con (not flat −10). 0 hp = disabled, negatives = dying.
- Diagonals still 5-10-5. Attacks of opportunity, action types (standard/
  move/swift/immediate/free/full-round) identical to 3.5.
- XP/level tables differ (PF1e has fast/medium/slow tracks) — never mix XP
  systems; this campaign uses the 3.5 XP table (`dnd-35-srd`).

## What is safe to import as-is

| Safe as-is | Needs conversion |
|---|---|
| hp, AC, attack bonuses, damage | Grapple/maneuvers (CMB→3.5 grapple) |
| Save bonuses, DCs, SR, DR, resistances | Skills (split Perception/Stealth) |
| Feats that exist in both systems | PF-only feats (pick nearest 3.5 feat) |
| Spell lists (95% shared names) | Polymorph-line spells, channel energy |
| Simple templates (see monster-advancement.md) | XP awards, wealth-by-level tables |
