# The Echo Ledger — BG3-Style Long-Range Consequences

Principle (pillar 7): **the world remembers**. Every meaningful PC
choice writes an *echo* — a recorded consequence with a fuse — that
returns later, *transformed*. The power of the technique is the delay:
instant karma is a reaction; an echo three arcs later is a world.

This file defines the ledger format, where it lives, and the rules for
arming and firing echoes. It operationalizes what the campaign already
does informally (villain clocks, promises/debts in `state.md` §5,
"Conseguenze-Echi" files in the Post-Hammerfist arc).

---

## 1. Where echoes live

The ledger is a subsection of `campaign/state.md` **§7 Open Narrative
Threads**, so no existing section is renumbered:

```markdown
### §7.E Echo Ledger (choices the world remembers)

| ID | Origin (sess., PC, choice) | Tone | Fuse | Payoff sketch | Status |
|----|----------------------------|------|------|---------------|--------|
| E-012 | S23, Hella spared the drow scout | + | medium (3–5 sess.) | Scout resurfaces as deserter with tunnel maps — owes her | armed |
```

- **ID**: `E-` + incrementing number, never reused.
- **Tone**: `+` (reward), `−` (cost), `tragic` (ripple-onto-the-house,
  see `pc-protagonism.md` §4), `mixed`.
- **Fuse**: `short` (1–2 sessions), `medium` (3–5), `long` (next arc or
  later), or an in-world-day count tied to a §2/§3 clock.
- **Status**: `armed` → `fired (S<N>)` → move a one-line record to the
  session log; or `expired` (fiction closed the path — note why).

Existing structures keep their jobs: promises/debts stay in §5, villain
clocks in §2–§3. An echo is for *unstructured* consequence — the world's
memory of a choice, good or evil, big or small.

## 2. Writing echoes (arming)

After every session (session wizard / recap flow), scan the log's
**Key decisions** and **World events triggered** sections and arm
**1–3 new echoes**. Selection rules:

1. **Both big and small.** At least every other session, arm one echo
   from a *minor* beat (a coin given, an insult, a door left open).
   Small echoes produce the best "it remembered THAT?" table moments.
2. **Both good and evil.** Kindness compounds and cruelty compounds;
   over time the ledger must show both tones for every PC. Protagonism
   in the evil gets echoes too — as story, never as DM revenge.
3. **Absence is a choice.** When the party ignores a viable thread
   (coherence §5.1's three open paths), arm an echo for how it resolves
   *without* them; the world shows the outcome later.
4. Every echo names **at least one PC** as its author. Party-wide
   echoes exist but are the minority.

**Fuse selection — the transformation law**: the longer the fuse, the
more the consequence must be *transformed* when it returns. Short fuse
= direct reaction (the guard you bribed talks). Medium = changed actor
(the spared scout is now a deserter). Long = changed world (the village
you saved is now a fortified town that flies your colors — or the cult
you humiliated has rebuilt around hating you specifically).

## 3. Firing echoes (payoff)

When generating any session, quest, or scene content:

1. Read §7.E first. **Prefer firing an armed echo over inventing a new
   NPC or hook** — if the scene needs a courier, a traitor, a patron, or
   a complication, check whether an echo can be that thing.
2. Quota: each session fires **≥1** armed echo when fiction allows;
   arc climaxes fire ≥2 (convergence: old choices stack into the
   finale — the BG3 act-three pattern).
3. **Legibility rule**: when an echo fires, players must be able to
   reconstruct the causal chain in one conversation. If the chain needs
   a DM lecture, simplify the payoff.
4. **Scale rule**: payoff magnitude ≤ origin magnitude + one step. A
   spared scout may save the party once; he does not hand them the war.
5. Fired echoes are logged in the session file and marked
   `fired (S<N>)`. A fired echo may arm a *new* echo (chains), but
   never silently respawn.

## 3-bis. Graded outcomes — the "regola pieno/ridotto" (Palio pattern)

For **arc-scale set pieces** (tournaments, battles, councils, festivals),
don't emit a single echo — build a **one-page consequence matrix**, as
pioneered by `...P2D-PALIO-CONSEGUENZE-ECHI.md` (the repo's worked
exemplar):

1. **Outcome axis**: every possible winner/result gets a row (including
   the disaster row — see below).
2. **Conduct modulation**: the *magnitude* of each row is graded by how
   the PCs got there — **full effect** if they won it or backed the
   winner; **reduced (−1 step)** if the winner was hostile to them;
   **+1 step** for exceptional conduct (side objectives completed).
   Outcome says *what* happens; PC conduct says *how much*.
3. **Campaign wiring row**: each outcome lists its effect on clocks,
   allies, and the next arc's difficulty (VP, GS, reinforcements) —
   numbers, not vibes.
4. **The bittersweet row**: losing while achieving the strategic goal
   (making the rival lose, preventing the worst) is a *distinct* result
   with its own rewards and its own echoes — never collapse it into
   "defeat".
5. **The disaster row is playable**: the worst outcome opens a
   desperate branch (the Palio's "Fase 0-bis"), never a game over.
6. **Per-PC echo row**: each institutional role/PC gets one personal
   echo line from the set piece (debts of honor, secrets that weigh,
   a ballad that becomes an anthem — or an accusation).

Matrix rows that fire become ledger entries (§1) as usual.

## 4. Anti-patterns (do not)

- **No combinatorial trees.** The ledger is flat lines, not nested
  what-ifs. Branches reconverge with scars (pillar 7): record the scar,
  drop the counterfactual.
- **No echo spam.** More than ~12 armed echoes = prune: fire, merge, or
  expire the stale ones during session prep.
- **No pure punishment ledger.** If the last three fired echoes were all
  `−`/`tragic` for the same PC, the next one fired for them must be `+`.
- **No retcon echoes.** An echo's origin must exist in a session log or
  `state.md` changelog. Inventing a past choice violates coherence §1.

## 5. Integration hooks

- `campaign/templates/session-template.md` → **Key decisions** is the
  primary echo source; **Next session hooks** is the primary firing site.
- `scripts/session_recap.py` (per-PG recaps) → recaps should surface
  fired echoes by name ("la tua scelta alla Miniera è tornata").
- Coherence self-check (`campaign-coherence.md` §6) → style self-check
  (SKILL.md) asks "did I surface or write an echo?".
- The Post-Hammerfist `*-CONSEGUENZE-ECHI-*` files are the prose layer
  of this system; the ledger is the index that keeps them findable.
