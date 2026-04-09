# Combat — D&D 3.5 SRD Reference

Source: d20srd.org/srd/combat/

---

## Combat Sequence

1. **Roll Initiative**: d20 + DEX mod (+ misc bonuses like Improved Initiative)
2. **Surprise round** (if applicable): only aware combatants act; only standard OR MvA
3. **Combat rounds** (6 seconds each): all combatants act in initiative order

**Flat-footed**: Before your first action in combat (or if caught unaware). Lose DEX bon to AC; cannot use Dodge bon; cannot make attacks of opportunity.

---

## Action Types /rnd

| Action Type | Count /rnd | Examples |
|---|---|---|
| Standard | 1 | Attack, cast most spells, activate item |
| Move | 1 | Move speed, draw weapon, stand from prone |
| Full-Round | Replaces std+move | Full attack, charge (at speed), run |
| Free | Unlimited (GM discretion) | Drop item, speak phrase, cease concentration |
| Swift | 1 /rnd | Some spells/abilities (Complete Adventurer) |
| Immediate | 1 /rnd* | Immediate-action spells (uses next round's swift) |

*Only 1 immediate + 0 swift, OR 0 immediate + 1 swift /rnd.

**Convert actions downward**: Standard → Move; Full-Round → Standard+Move

---

## The Full Attack

A character who has multiple attacks from high BAB MUST take a FRA to use all of them. Moving AND attacking (single strike) = StdA only (no iteratives).

**Two-Weapon Fighting penalties (base):**
- Primary hand: −6
- Off hand: −10
- With Two-Weapon Fighting feat: −4/−4
- With light off-hand weapon (no feat): −4/−8
- With TWF feat + light off-hand: −2/−2

---

## Attack bon Calculation

**mel attack:** BAB + STR mod + size mod + misc
**rng attack:** BAB + DEX mod + range penalty + size mod + misc
**Touch attack:** BAB + STR/DEX mod + size mod (ignores armor/natural/shield bon to AC)
**rng touch attack:** as above, range penalty applies

**Power Attack**: Before attack roll, declare penalty to attack (up to BAB) → equal bon to damage (two-handed: 2× damage bon)

**Combat Expertise**: Before attack roll, declare penalty (up to 5) → equal dodge bon to AC until next turn (req: INT 13)

---

## Damage

**Damage roll** = weapon die + STR mod (mel / thrown) + magic + misc
- Two-handed weapon: STR × 1.5 (round down)
- Off-hand weapon: STR × 0.5 (min +0 from STR, but penalties apply fully)

**Critical Hits**:
1. Roll within threat range (e.g., 18–20 for scimitar) → threat
2. Confirm: roll again; if it would hit the opponent's AC → critical
3. Multiply damage (not bonuses from Power Attack, sneak attack, etc.) by crit multiplier (×2 standard, ×3 lance/falchion, ×4 scythe)

---

## Conditions Quick Reference

| Condition | Key Effects |
|---|---|
| Blinded | −2 AC, lose DEX to AC, −4 attacks, attackers get +2; 50% miss chance |
| Confused | Roll d% each round for action |
| Cowering | Lose DEX, −2 AC; no actions |
| Dazed | No actions; AC, saves normal |
| Dazzled | −1 attack rolls, Spot checks |
| Dead | Dead |
| Deafened | −4 Initiative; 20% spell failure; −4 Listen |
| Dying | −1 to −9 HP; unconscious; lose 1 HP/round; save DC 10 at −1, +1 /rnd |
| Energy Drained | −1 effective level per negative level; −1 all d20 rolls /lvl |
| Entangled | −2 attacks, −4 DEX; move at half speed; spells need Concentration DC 15+SL |
| Exhausted | STR/DEX −6; half speed; becomes fatigued after rest |
| Fascinated | Flat-footed; only Spot/Listen as free actions |
| Fatigued | STR/DEX −2; cannot run/charge |
| Flat-Footed | Lose DEX to AC; cannot make AoOs; before first turn |
| Frightened | Flee if possible; −2 attacks/saves/checks |
| Grappled | −4 DEX; −4 attack vs. non-grappled; no AoOs; limited to grapple actions |
| Helpless | DEX 0; attackers get +4 to hit; adjacent gets coup de grace |
| Incorporeal | Immune to nonmagic/mundane; 50% with magic; own attacks only affect incorporeal/ethereal |
| Invisible | +2 attacks; defenders lose DEX; 50% miss |
| Nauseated | Only MvA; no attack/cast/concentration |
| Panicked | Drop items; flee; −2 attacks/saves/checks |
| Paralyzed | STR/DEX 0; helpless; falls prone |
| Petrified | Object; retain INT; immune to everything practically |
| Pinned | Held in grapple; only escape attempt; −4 AC vs. grappler; cannot cast (usually) |
| Prone | −4 mel attacks; +4 AC vs. rng; −4 AC vs. mel; move = crawl (5 ft/MvA) |
| Shaken | −2 attacks/saves/checks (not as severe as frightened/panicked) |
| Sickened | −2 attacks/damage/saves/checks |
| Stable | Dying but no longer losing HP; still unconscious |
| Staggered | 0 HP; only single actions (standard OR move) |
| Stunned | Lose DEX; drop items; no actions; attackers get +2 |
| Turned | Fleeing from cleric/paladin's turning |
| Unconscious | Helpless; asleep or knocked out |

---

## Attacks of Opportunity (AoO)

**Provoked by (in mel threatened area):**
- Moving out of a threatened square (not a 5-ft step)
- Making a rng attack
- Casting a spell with Verbal/Somatic components (unless defensively: Concentration DC 15+SL)
- Using a skill in mel (some skills)
- Standing from prone
- Drawing a weapon without Improved Draw / Quick Draw
- Retrieving a stored item

**AoO does NOT provoke unless stated otherwise.**

**Combat Reflexes feat**: DEX mod extra AoOs /rnd (still only 1 per triggering creature /rnd)

**5-foot step**: Free; does not provoke; only if you haven't moved otherwise this round.

---

## Grapple

1. Provoke AoO (unless you have Improved Grapple feat)
2. Make mel touch attack vs. opponent
3. If hits: opposed Grapple checks: d20 + BAB + STR mod + size mod
4. Success → grappling; both are grappled

**While grappling (Full-Round to do one):**
- Attack with light weapon or natural weapon (−4 attack)
- Pin opponent (opponent is pinned; you are still grappled)
- Damage opponent (deal unarmed/light weapon damage)
- Draw light weapon
- Escape grapple (opposed grapple or Escape Artist vs. grapple check)
- Retrieve spell component
- Cast defensively (very limited)

---

## Movement and Terrain

| Terrain | Cost |
|---|---|
| Normal | 1 sq = 5 ft |
| Difficult | 2 sq = 5 ft |
| Steep slope/rubble | 2 sq = 5 ft |
| Dense undergrowth | 4 sq = 5 ft |
| Mud/shallow water | 2 sq = 5 ft |
| Deep water/swimming | Swim check |

**Charge**: Move up to 2× speed in straight line; +2 to attack; −2 to AC until next turn; provokes AoO during movement if applicable

**Run**: 4× speed (3× in heavy armor); straight line; −2 AC; lose DEX until next turn

---

## Cover and Concealment

**Cover:**
- Soft cover (other creatures): +4 AC vs. rng
- Standard cover (half): +4 AC, +2 Ref
- Improved cover (¾): +8 AC, +4 Ref
- Total cover: Cannot be targeted directly

**Concealment (miss chance):**
- 20% concealment (light fog, foliage)
- 50% concealment (total darkness, Heavy concealment)
- Total concealment: target must guess square; 50% miss; cannot make AoOs

---

## Damage, Death, and Dying

| HP | State |
|---|---|
| ≥1 | Conscious and active |
| 0 | Staggered (standard OR move, not both) |
| −1 to −9 | Dying: unconscious, lose 1 HP/round |
| −10 or below | Dead |

**Massive Damage Rule (optional)**: Taking 50+ damage in one hit → Fort save DC 15 or die.

**Stabilize**: Someone adjacent can use a DC 15 Heal check (StdA) to stabilize a dying character. Also: Heal spell, healing magic.

**Natural Stabilization**: 10% chance /rnd to stabilize naturally.

**Recovery**: Stable character wakes after d% hours unconscious; starts recovering at 1 HP/day with complete rest.