# PF1e NPC Building — Classed NPCs and Villains

Source: PF1e Core Rulebook ch. 14, GameMastery Guide (NPC creation),
NPC Codex. Verify: https://www.d20pfsrd.com/gamemastering/npc-creation/

Use this when a villain or named PNG needs class levels rather than a
template. Works for 3.5 tables: build with PF1e speed, then apply the
conversion notes in `core-differences.md`.

---

## CR from character level

| NPC build | CR |
|---|---|
| PC-class levels, heroic array, class-appropriate gear | level − 1 |
| NPC-class levels only (warrior, expert, adept, aristocrat, commoner) | level − 2 (min 1/3) |
| Racial HD + class levels | build as monster + class levels, then benchmark |

- 3.5 prices the same characters at level (PC classes) or level − 1
  (NPC classes). **The PF1e pricing is more honest** — a lone classed NPC
  underperforms a monster of equal CR (fewer hp, no special attacks). When a
  3.5 classed villain feels weak for its listed CR, the PF1e discount is why.
- Boss NPCs that must survive alone deserve CR-appropriate hp: take max hp at
  first level *and* consider the toughness/favored-class hp margin, or pair
  the boss with bodyguards. See `npc-villain-boosting` for the decision rules.

## Ability arrays (no rolling)

| Array | Scores (before racial) | Use for |
|---|---|---|
| Basic | 13, 12, 11, 10, 9, 8 | mooks, NPC-class characters |
| Heroic | 15, 14, 13, 12, 10, 8 | classed villains, lieutenants |
| Elite (3.5's elite array equivalent) | 15, 14, 13, 12, 10, 8 + racial | named recurring villains |

Add +1 per 4 levels as normal. For spellcasting villains, prioritize the
casting stat: DC pressure is what makes casters scary at APL 13.

## NPC gear by level (PF1e "heroic NPC" column)

Gear is ~½ of a PC's wealth-by-level. Key rows
(`[Verify — PF Core, Table 14–9]`):

| Level | NPC gear value |
|---|---|
| 9 | 8,000 gp |
| 11 | 12,500 gp |
| 13 | 20,000 gp |
| 15 | 33,000 gp |

- Spend on the villain's *one* signature trick (weapon or DC-booster) plus
  AC. Consumables (potions, scrolls) are loot the party recovers — they are
  the safe way to over-gear a villain without inflating campaign wealth.
- 3.5 equivalent: DMG Table 4–23 NPC gear value. The numbers are close
  enough to use either; this campaign audits treasure against 3.5 WBL
  (see `campaign/` treasure audits), so log whatever the party actually loots.

## Fast villain recipe (10 minutes)

1. Pick chassis: existing SRD monster or race + PC class.
2. Level = target CR + 1 (PC class) or CR + 2 (NPC class).
3. Heroic array; max hp at level 1; favored-class bonus into hp.
4. Two feats that define the tactic (e.g., Power Attack + Cleave, or
   Spell Focus + Greater Spell Focus). Fill the rest from a printed
   NPC Codex block of the same class/level instead of hand-picking.
5. Gear from the table above: one signature item + best affordable armor.
6. **Benchmark** against `monster-advancement.md` Table 1–1 row; nudge
   AC/hp/DCs to the row. Done.
7. Output in the 3.5 stat-block format with `Conversion notes:` line.
