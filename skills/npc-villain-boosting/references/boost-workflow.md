# Boost Workflow — Rebuild Checklist, Output Format, Worked Example

Run this after choosing a method in `boost-decision.md`. It guarantees the
boosted block is complete, legal, and logged.

---

## Rebuild checklist (in order — later steps depend on earlier ones)

1. **Abilities** — apply HD-milestone increases, size changes, template
   adjustments. Everything downstream reads from these.
2. **HD / hp** — new dice + Con mod per die. Bosses: consider max hp on the
   first HD (3.5 monster convention is average; max-first-die is a legal DM
   call — note it).
3. **BAB / grapple** — type progression at new HD; grapple = BAB + Str mod +
   special size mod.
4. **Attacks** — recompute to-hit (BAB + Str/Dex + size), damage
   (new dice size + new Str mod; ×1.5 two-handed/sole natural weapon).
5. **AC** — new natural armor, new size mod, new Dex.
6. **Saves** — type progression + new ability mods.
7. **Skills / feats** — new totals (feat at every 3rd HD, 3.5). Pick feats
   that serve the tactic; don't optimize beyond the table's fun.
8. **Special attack DCs** — 10 + ½ HD + ability mod: recompute, these shift
   with HD and abilities and are easy to miss.
9. **CR** — additive rules first, then **benchmark vs PF Table 1–1**
   (`pathfinder-1e-srd/references/monster-advancement.md`); final CR = what
   the numbers earn.
10. **Log it** — update the PNG/monster file: `Boost log:` line + new block.

## Output format

Use the 3.5 SRD stat-block format (`dnd-35-srd/references/monsters.md`) plus:

```
Boost log: [date] — [method] — CR [old] → [new] — [reason, one line]
Conversion notes: [only if PF1e material was imported]
Benchmark: PF T1-1 row [CR]: AC ok / hp ok / atk +1 over / DC 1 under
```

## Worked example — SRD Troll, from "speed bump" to mini-boss

Party: APL 13. Printed Troll (CR 5, Large giant, 6d8+36 HD, 63 hp, AC 16,
claw +9, rend, regeneration 5) is a trivial-row encounter (APL − 8).

**Path A — mid-session, zero prep: PF Advanced quick template (CR 5 → 6)**
+2 all rolls and DCs, +4 AC, +2 hp/HD → 75 hp, AC 20, claw +11.
Two of them + terrain = EL 8. Still an easy fight; fine as a warm-up wave.

**Path B — prep: 3.5 HD advancement to the top of the range (CR 5 → 8)**

- Advancement line: `7–9 HD (Large); 10–14 HD (Huge)` → take 12 HD (Huge).
- +6 HD, giant type → CR +1 per 4 HD = **+1**; Large→Huge size jump = **+1**.
- Size table: +8 Str (23→31), −2 Dex (14→12), +4 Con (23→27), natural
  armor +3 (5→8).
- 12d8 + 96 hp ≈ **150 hp**; regeneration 5 unchanged (fire/acid still the
  answer — players who learned that keep their reward).
- BAB (giant ¾) 6→9; grapple 9 + 10 + 8 (Huge) = **+27**.
- Claw to-hit = 9 (BAB) + 10 (Str) − 2 (Huge) = **+17**;
  damage steps 1d6 → 1d8, +10 Str → claw 1d8+10, bite 2d6+5, rend 2d8+15.
- AC: 10 + 8 natural − 2 size + 1 Dex = **17** (AC lags — expected for
  trolls; regeneration is the real defense).
- Feats: 12 HD → 4 feats (was 3): add Improved Natural Attack or Power Attack.
- Additive CR: 5 + 1 (HD) + 1 (size) = **7–8**. Benchmark vs PF row 8
  (AC 21, hp 100, atk +15): hp over, attack over, AC well under → call it
  **CR 8** with a glass-cannon profile. Two of these = EL 10; add four
  Advanced trolls from Path A and the encounter reaches EL ~13 — a true
  standard fight for this party.

**Path C — named villain: class levels**
The same 12-HD Huge troll with 4 levels of barbarian (associated for a
giant brute: +4 CR) becomes a CR ~12 named lieutenant with rage, +hp, and
uncanny dodge — worth a name, a PNG file, and a `Boost log:` line.

## Anti-patterns

- Boosting *every* encounter of an arc (+pacing collapse, XP inflation).
- Boosting DCs past the party's weak saves at APL+4 (save-or-lose lottery).
- Silent boosts to creatures the party has already measured in the fiction.
- Boosting instead of fixing action economy — a solo CR 17 monster still
  loses to 4 level-13 PCs who each act every round.
