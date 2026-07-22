# Boost Decision — Is It Needed? Is It Worth It?

The most common boosting mistake is boosting at all. Work through the gates
in order; stop at the first "no".

---

## Gate 1 — Is the encounter actually under-tuned?

3.5 EL math (DMG ch. 3; implemented in `scripts/suggest_encounter.py`):

```
EL ≈ 2 · log2( Σ 2^(CR/2) )      # doubling equal-CR creatures = EL +2
```

Against this party (APL 13, but artifact-loaded — treat as **effective APL
13–14** for tuning; see `campaign-party.md`):

| EL vs APL | Feel | Party resources used | Use for |
|---|---|---|---|
| APL − 4 or less | trivial | ~0% | color, morale, power fantasy |
| APL − 1 … +0 | standard | ~20% | the bread-and-butter fight |
| APL +1 … +2 | hard | 30–50% | lieutenants, set-pieces |
| APL +3 … +4 | very hard | may cost a PC | bosses, arc climaxes |
| APL +5+ | overpowering | TPK-shaped | only with a signposted exit |

If the printed encounter already lands in the row you *want*, don't boost.
An arc needs trivial and standard fights; if every encounter is boosted to
"hard", the players stop feeling level 13.

## Gate 2 — Is the problem the monster, or the action economy?

One creature vs 4 PCs loses ~3:1 on actions regardless of CR. Symptoms:
boss dies round 2, never acts twice, save-or-lose ends it. Before touching
the stat block:

- **Add bodies** (cheapest, most fun): 2 bodyguards of CR ≈ boss−4 barely
  move EL but soak actions. Doubling the boss's CR-equals adds EL +2.
- **Terrain & tactics** (free, EL +0): cover, reach + 5-ft steps, chokepoints,
  readied actions, prepared buffs (a caster villain with 2 rounds of warning
  is effectively +1–2 CR). See `campaign-dm-strategy.md`.
- Only if the monster must be alone AND must last: boost survivability
  (hp/AC/saves), not damage — a solo damage boost just changes *which* PC
  dies before the anticlimax.

## Gate 3 — Is it worth the prep and the XP inflation?

- **XP:** boosted CR feeds the 3.5 XP table. +2 CR across every fight of an
  arc accelerates leveling by roughly half a level per arc — check the pacing
  intent in `campaign/state.md` before blanket-boosting.
- **Prep cost:** PF quick template = 0 minutes; 3.5 HD advancement = 15–30
  min; class levels = 30–60 min. Spend rebuild time only on creatures with a
  name or a return appearance.
- **Worth test:** "Will the players tell a story about this fight?" If the
  boost only changes numbers on scratch paper, it wasn't worth it.

## Choosing the knob (summary)

| Situation | Method |
|---|---|
| Mid-session, fight is flat | PF **Advanced** quick template (+1 CR, one line) |
| Brute should feel huge | PF **Giant** quick or 3.5 size advancement |
| Monster too strong / want swarms | PF **Young** (−1 CR) + more bodies |
| Signature monster, prep time | 3.5 **HD advancement** (fidelity, Advancement line) |
| Named villain / recurring PNG | 3.5 **class levels** (associated class) |
| Villain needs a gimmick, not power | 3.5 **template** (fiendish, half-dragon, lich…) |
| NPC humanoid needs muscle fast | Equipment + elite array (3.5 DMG) or PF NPC recipe |
| Anything, before the table | **Benchmark vs PF Table 1–1** and set final CR |

## De-boosting

The same machinery runs downward (party split, attrition day, low-resource
scenario): PF Young template (−1 CR), strip class levels, cut HD to the
bottom of the Advancement range. Log de-boosts the same way as boosts.
