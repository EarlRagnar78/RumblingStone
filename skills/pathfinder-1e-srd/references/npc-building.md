# PF1e NPC Building — Classed NPCs and Villains

Source: PF1e Core Rulebook (Gamemastering + NPC chapters), NPC Codex.
Lookup: https://www.d20pfsrd.com/gamemastering/npc-creation/

Use this when a villain or named PNG needs class levels rather than a
template. Works for 3.5 tables: build with PF1e speed, then apply the
conversion notes in `core-differences.md`.

---

## CR from character level

Verified rule (PF Core, encounter design): a creature with class levels and
no racial HD:

| NPC build | CR |
|---|---|
| PC-class levels | class levels − 1 |
| NPC-class levels only (warrior, expert, adept, aristocrat, commoner) | class levels − 2 |
| Racial HD + class levels | build as monster + class levels, then benchmark |

Below CR 1, each step down follows the progression 1/2, 1/3, 1/4, 1/6, 1/8.

- 3.5 prices the same characters at level (PC classes) or level − 1
  (NPC classes). **The PF1e pricing is more honest** — a lone classed NPC
  underperforms a monster of equal CR (fewer hp, no special attacks). When a
  3.5 classed villain feels weak for its listed CR, the PF1e discount is why.
- Boss NPCs that must survive alone deserve CR-appropriate hp: take max hp at
  first level *and* consider the toughness/favored-class hp margin, or pair
  the boss with bodyguards. See `npc-villain-boosting` for the decision rules.

## Ability arrays (no rolling)

Verified (PF Core, NPC creation) — apply racial modifiers after assigning:

| Array | Scores (before racial) | Use for |
|---|---|---|
| Basic | 13, 12, 11, 10, 9, 8 | NPC-class characters (mooks, mobs) |
| Heroic | 15, 14, 13, 12, 10, 8 | PC-class NPCs: villains, lieutenants |

The heroic array is identical to 3.5's elite array — one array to remember
across both systems. Add +1 to one score per 4 levels as normal. For spellcasting villains, prioritize the
casting stat: DC pressure is what makes casters scary at APL 13.

## NPC gear by level (PF1e "heroic NPC" column)

Gear runs well below a PC's wealth-by-level. Verified rows from PF Core,
Table: NPC Gear (heroic-class NPCs; basic-class NPCs use one level lower):

| Heroic NPC level | Total gear value |
|---|---|
| 7 | 6,000 gp |
| 9 | 10,050 gp |
| 11 | 16,350 gp |
| 13 | 27,000 gp |
| 15 | 45,000 gp |
| 17 | 75,000 gp |

High-fantasy campaign: double these; low-fantasy: halve them. Fast XP
track: treat NPCs as one level higher for gear; slow track: one lower.

- Spend on the villain's *one* signature trick (weapon or DC-booster) plus
  AC. Consumables (potions, scrolls) are loot the party recovers — they are
  the safe way to over-gear a villain without inflating campaign wealth.
- 3.5 equivalent: DMG Table 4–23 NPC gear value (non-SRD — verify in your
  copy; e.g. its level-13 row is lower than PF's 27,000 gp). Either scale
  works; this campaign audits treasure against 3.5 WBL (see `campaign/`
  treasure audits), so log whatever the party actually loots.

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
