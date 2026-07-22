# Converting Between D&D 3.5 and Pathfinder 1e

Source: Paizo's official *Pathfinder RPG Conversion Guide* (free PDF,
paizo.com) summarizes 3.5→PF1e; this file covers both directions for the
needs of a 3.5 campaign that borrows PF1e material.

**Rule of thumb: don't convert — import.** The systems share the d20 OGL
skeleton; printed numbers work as-is at the table 90% of the time. Convert
only the subsystems listed below, and only when they actually come up.

---

## PF1e monster → 3.5 table (checklist)

1. **hp, AC, attacks, damage, saves, DCs, SR, DR, speeds** — keep as printed.
2. **CMB/CMD** — replace with 3.5 grapple = BAB + Str mod + special size mod
   (Large +4, Huge +8, Gargantuan +12, Colossal +16). For trip/bull rush use
   the 3.5 opposed-check rules with the creature's Str/Dex.
3. **Perception** → Spot AND Listen at the same bonus (also Search at
   Int-based approximation). **Stealth** → Hide AND Move Silently.
   **Acrobatics** → Balance/Jump/Tumble.
4. **PF-only feats** — map to nearest 3.5 feat or drop; common maps:
   - Improved Natural Armor / Toughness (PF) → Toughness ×n or Improved
     Toughness `[Non-SRD: Complete Warrior]`
   - Combat Reflexes, Power Attack, Cleave, Vital Strike: Power Attack and
     Cleave exist in 3.5 (use 3.5 wording); Vital Strike has no 3.5 twin —
     drop it or treat as a flavor rider on a single attack.
5. **Channel energy** → 3.5 turn/rebuke undead at cleric level, or keep as a
   house-ruled 30-ft burst (declare which in the encounter file).
6. **Polymorph-line spells** → use the 3.5 spell text.
7. **CR** — keep the printed PF1e CR. PF1e monsters of the same CR are
   slightly tougher than 3.5 ones on average; that is acceptable drift for a
   party that outguns printed 3.5 content (this one does — 4 PCs at level 13
   with artifacts).
8. Add a `Conversion notes:` line to the stat block listing what changed.

## 3.5 monster → PF1e (rarely needed here)

1. Keep everything printed.
2. CMB = BAB + Str + PF size mod; CMD = 10 + BAB + Str + Dex + PF size mod.
3. Merge Spot/Listen → Perception (take the better), Hide/MS → Stealth.
4. Consider +2 hp/HD or the Advanced template — 3.5 monsters run soft by
   PF1e benchmarks.

## XP, wealth, and progression — never mix

- Award XP from the **3.5 DMG table only** (`dnd-35-srd`), regardless of the
  monster's origin. A CR 13 kill is a CR 13 kill.
- Audit treasure against **3.5 WBL** (campaign standard; see arc treasure
  audits under `campaign/`).
- PF1e fast/medium/slow XP tracks, PF WBL, and PF item pricing are OFF —
  they exist in this repo only for reading PF1e sources correctly.

## Spell compatibility

~95% of spell names and effects match. Known traps:

| Spell | Difference |
|---|---|
| *Polymorph* family | Completely rewritten in PF1e — always use 3.5 text |
| *Grease, Glitterdust, Black Tentacles* | PF1e nerfed via CMB/save tweaks — use 3.5 text |
| *Save-or-die* (finger of death, etc.) | PF1e converts to damage — use 3.5 text |
| *Cure X Wounds* | identical — either |
| Core blasting/buffs (fireball, haste, stoneskin…) | identical enough — either |

When a villain is built with PF1e class features but casts spells, cast from
the 3.5 spell text with the PF1e DCs. That combination is stable and fast.
