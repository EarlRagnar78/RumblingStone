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

- **Quick:** +2 on **all** rolls (attack, damage, saves, checks) and all
  special ability DCs; +4 AC and CMD; +2 hp per HD.
- **Rebuild:** +4 to all ability scores (Int min 3 unless mindless);
  +2 natural armor.
- Stackable with itself in a pinch (Advanced ×2 ≈ CR +2) — coarse but legal
  at the table. `[DM guidance, not RAW]`

### Giant (CR +1) — bigger, hits harder (corporeal, Huge or smaller)

- **Quick:** +2 on all Str- and Con-based rolls, +2 hp per HD, −1 on all
  Dex-based rolls (including AC/touch AC), +3 natural armor.
- **Rebuild:** size +1 category; +4 Str, +4 Con, −2 Dex; +3 natural armor;
  increase damage dice one step; recompute size modifiers to attack/AC
  (Large −1, Huge −2), reach and space.

### Young (CR −1) — the *downgrade* knob (also useful: de-boost, add numbers)

- **Quick:** −2 on all rolls based on Str or Con, −2 hp per HD, +2 on all
  Dex-based rolls.
- **Rebuild:** size −1 category; +2 Dex, −4 Str, −4 Con; −2 natural armor
  (min +0); damage dice one step down.

### Celestial / Fiendish (CR +0 for HD 1–4; CR +1 for HD 5+)

- Darkvision 60 ft.
- Energy resistance — Celestial: acid/cold/electricity; Fiendish: cold/fire —
  5 (HD 1–4), 10 (HD 5–10), 15 (HD 11+).
- DR — none (HD 1–4), 5/evil or 5/good (HD 5–10), 10/evil or 10/good (HD 11+).
- SR = new CR + 5.
- **Smite** evil (celestial) / good (fiendish) 1/day: +Cha mod to attack,
  +HD to damage vs the smitten target.
- 3.5 has the same two templates with slightly different scaling
  (see `dnd-35-srd/references/monsters.md`); either version is fine —
  pick one and note which. `[3.5 CR: +0 HD≤3, +1 HD 4–7, +2 HD 8+]`

### Entropic / Resolute (Bestiary 2; CR +0 for HD 1–4; CR +1 for HD 5+)

- Chaos/law mirror of celestial/fiendish: Entropic resists acid+fire,
  DR /lawful, smite law; Resolute resists acid+cold+fire? — check exact
  resistances at aonprd before use `[Verify — Bestiary 2]`; DR /chaotic,
  smite chaos. Same numeric scaling as celestial/fiendish.

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
- Non-key class: +1 CR per 2 levels until the class levels equal the racial
  HD, then +1 per level.
- After building, benchmark against Table 1–1 and adjust CR to match actual
  output. (Same procedure as 3.5 associated/nonassociated — the systems agree.)

---

## Monster Statistics by CR — benchmark targets

PF1e Bestiary Table 1–1 gives the target numbers a monster of CR *n* should
hit. **Use it to price any boost, including 3.5 ones:** if your boosted
villain's AC, hp, attack, and DCs land on the CR 13 row, it *is* CR 13 no
matter what the additive rules said.

Anchor rows for this campaign's level band (values from Bestiary Table 1–1;
`[Verify vs aonprd before final stat-block use]`):

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

How to read it against a 3.5 party of four level-13 PCs (APL 13):

- A **boss** (EL = APL+2…+3) wants the CR 15–16 row.
- A **hard standard fight** (EL = APL) wants the CR 13 row *split across
  several monsters* — one CR 13 creature alone is action-economy-starved.
- If a boosted monster beats the row on offense but misses it on defense
  (or vice versa), its real CR is between rows — price it at the lower row
  and expect it to feel swingy.
