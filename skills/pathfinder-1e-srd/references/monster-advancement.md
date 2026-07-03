# PF1e Monster Advancement — Simple Templates & Benchmarks

Source: PF1e Bestiary, "Monster Advancement" + Appendix (Table 1–1).
Verify: https://www.d20pfsrd.com/bestiary/rules-for-monsters/simple-templates/
and https://aonprd.com/Rules.aspx?Name=Monster%20Advancement&Category=Appendix

These are the **fastest legal way to boost a monster** — each template is a
one-line change usable mid-session. They are fully compatible with 3.5 stat
blocks. The decision of *whether* to boost lives in `npc-villain-boosting`.

---

## Simple Templates (apply in minutes)

Each simple template has **Quick Rules** (apply on the fly, don't rewrite the
stat block) and **Rebuild Rules** (recompute the block properly). Quick rules
are the table-side tool; rebuild when the monster becomes a recurring villain.

### Advanced (CR +1) — the universal "elite" knob

- **Quick:** +2 on **all** rolls (including damage rolls) and all special
  ability DCs; +4 to AC and CMD; +2 hp per HD.
- **Rebuild:** +4 to all ability scores; +2 natural armor.
- Stackable with itself in a pinch (Advanced ×2 ≈ CR +2) — coarse but legal
  at the table. `[DM guidance, not RAW]`

### Giant (CR +1) — bigger, hits harder (not applicable to Colossal)

- **Quick:** +2 on all Str- and Con-based rolls, +2 hp per HD, −1 on all
  Dex-based rolls.
- **Rebuild:** size +1 category; +4 size bonus to Str and Con, −2 Dex;
  +3 natural armor; increase damage dice one step; recompute size modifiers
  to attack/AC (Large −1, Huge −2), reach and space.

### Young (CR −1) — the *downgrade* knob (also useful: de-boost, add numbers)

Not for creatures that grow through age categories (dragons) or Fine ones.

- **Quick:** +2 on all Dex-based rolls, −2 on all **other** rolls, −2 hp
  per HD.
- **Rebuild:** size −1 category; −4 Str, −4 Con, +4 size bonus to Dex;
  −2 natural armor (min +0); damage dice one step down.

### Celestial / Fiendish (CR +0 for HD 1–4; CR +1 for HD 5+)

Quick and rebuild rules are the same:

- Darkvision 60 ft.
- Energy resistance — Celestial: acid/cold/electricity; Fiendish: cold/fire —
  5 (HD 1–4), 10 (HD 5–10), 15 (HD 11+).
- DR — none (HD 1–4), 5/evil or 5/good (HD 5–10), 10/evil or 10/good (HD 11+).
- SR = new CR + 5.
- **Smite** evil (celestial) / good (fiendish) 1/day as a swift action:
  +Cha mod to attack rolls, +HD to damage vs the smitten target; persists
  until the target is dead or the creature rests.
- 3.5 has the same two templates with slightly different scaling
  (see `dnd-35-srd/references/monsters.md`); either version is fine —
  pick one and note which. `[3.5 CR: +0 HD≤3, +1 HD 4–7, +2 HD 8+]`

### Entropic / Resolute (CR +0 for HD 1–4; CR +1 for HD 5+)

Chaos/law mirror of celestial/fiendish, same structure (darkvision 60 ft.,
SR = new CR + 5, smite 1/day as swift action):

- **Entropic**: resist acid/fire 5 → 10 → 15; DR 5/lawful (HD 5–10),
  10/lawful (HD 11+); smite law.
- **Resolute**: resist acid/cold/fire 5 → 10 → 15; DR 5/chaotic (HD 5–10),
  10/chaotic (HD 11+); smite chaos.

---

## Adding Hit Dice (PF1e)

Same skeleton as 3.5: extra HD → more hp, +BAB/saves by type, feats
(PF: 1 per 2 HD — odd HD totals), skill ranks, +1 ability every 4 HD.
**CR:** PF1e uses the benchmark table below instead of the 3.5 per-type
divisor — after advancing, compare the result to Table 1–1 and *read the CR
off the monster's new numbers*. That is the philosophical difference:
**PF1e assigns CR by output, not by input.** It is the sanity check to apply
to every 3.5 advancement too.

## Adding class levels (PF1e)

- Key class (plays to the monster's strengths, e.g. barbarian on a brute):
  +1 CR per level.
- Non-key class: +1 CR per 2 levels, until the levels added equal (or
  exceed) the creature's **original CR** — from then on they count as key,
  +1 CR per level. NPC classes are never key. (Note the 3.5 threshold is
  different: original racial *HD*, not CR.)
- PC-class levels also grant +4/+4/+2/+2/+0/−2 ability adjustments assigned
  to fit the class; NPC-class levels grant none.
- After building, benchmark against Table 1–1 and adjust CR to match actual
  output.

---

## Monster Statistics by CR — benchmark targets

PF1e Bestiary Table 1–1 gives the target numbers a monster of CR *n* should
hit. **Use it to price any boost, including 3.5 ones:** if your boosted
villain's AC, hp, attack, and DCs land on the CR 13 row, it *is* CR 13 no
matter what the additive rules said.

Anchor rows for this campaign's level band (Bestiary Table 1–1 values,
cross-checked for consistency against the official per-step Monster
Advancement deltas below):

| CR | AC | hp | High attack | Avg dmg (high) | Primary DC | Good save | Poor save |
|---|---|---|---|---|---|---|---|
| 8 | 21 | 100 | +15 | 30 | 17 | +11 | +8 |
| 10 | 24 | 130 | +18 | 45 | 19 | +13 | +9 |
| 11 | 25 | 145 | +19 | 50 | 20 | +14 | +10 |
| 12 | 27 | 160 | +19 | 55 | 20 | +15 | +11 |
| 13 | 28 | 180 | +21 | 61 | 21 | +15 | +11 |
| 14 | 29 | 200 | +22 | 67 | 22 | +16 | +12 |
| 15 | 30 | 220 | +23 | 74 | 23 | +17 | +12 |
| 16 | 31 | 240 | +24 | 80 | 24 | +18 | +13 |

**Table: Monster Advancement — what one CR step buys** (Bestiary appendix,
verified): when raising a monster from the lower CR to the higher one, add:

| CR step (from → to) | hp | AC | Attack | Damage |
|---|---|---|---|---|
| <1 → 1 | +5 | +1 | +1 | +2–3 |
| 1 → 2 … 2 → 3 | +5–10 | +1–2 | +1–2 | +2–3 |
| 3 → 4 | +10 | +2 | +2 | +2–3 |
| 4 → 5 … 11 → 12 | +15 | +1–2 | +1–2 | +3–5 |
| 12 → 13 … 15 → 16 | +20 | +1 | +1–2 | +3–10 |
| 16 → 17 … 18 → 19 | +30 | +1 | +1 | +7–10 |
| 19 → 20 and beyond | +40 | +2 | +1 | +8–10 |

This is the fastest sanity check for a hand-boost: if you claimed +2 CR
but only added 10 hp and +1 to hit, you under-delivered.

How to read the benchmarks against a 3.5 party of four level-13 PCs (APL 13):

- A **boss** (EL = APL+2…+3) wants the CR 15–16 row.
- A **hard standard fight** (EL = APL) wants the CR 13 row *split across
  several monsters* — one CR 13 creature alone is action-economy-starved.
- If a boosted monster beats the row on offense but misses it on defense
  (or vice versa), its real CR is between rows — price it at the lower row
  and expect it to feel swingy.
