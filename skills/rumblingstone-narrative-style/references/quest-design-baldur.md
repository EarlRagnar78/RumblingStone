# Complex Quest Architecture — BG1/BG2 Patterns

Principle (pillar 8): a quest is a **dramatic machine with stages**, not
a checklist. These patterns extend the quest-tree format of
`rumblingstone-campaign/references/dm-expansion-toolkit.md` PART 2 —
keep using that file's Stage/Branch markdown format; this file defines
*which shapes* to build with it.

Every generated quest must also pass the Protagonism Test
(`pc-protagonism.md` §1) and arm at least one echo
(`consequence-echoes.md` §2).

---

## 1. The Stage Rule — each stage changes the question

3–5 stages, and each stage **reframes** the quest, never just extends
it. The test: state the quest as a question at every stage; if the
question hasn't changed, the stage is padding.

```
Stage 1  "Who is stealing from the caravans?"        (mystery)
Stage 2  "Why does the thief have a Zhent warrant?"  (reframe: protection)
Stage 3  "Which patron do we expose — or replace?"   (reframe: allegiance)
Stage 4  "What do we do with the vacuum we created?" (reframe: consequence)
```

Stage transitions are **discoveries or choices**, never travel. The
final stage is always a choice the PCs own (echo written).

## 2. The Mirrored Factions pattern

Two organizations in conflict both offer the PCs a quest line toward
the same objective; progress with one **forecloses** the other
(visibly — burned bridge, not hidden flag).

- Both factions pass the GoT test first: each has *belief, want, fear,
  and an opinion of each PC* (style-pillars §5).
- Mirror the stages: the same locations/NPCs seen from both sides.
  Cost efficiency for the DM, moral weight for the players.
- Betrayal option: switching sides mid-line is allowed, expensive, and
  echo-heavy.
- Use the existing faction tracker (dm-expansion-toolkit PART 4) to
  record the foreclosure.

## 3. Quests within quests

A main objective requiring 2–3 sub-objectives, each of which is a real
quest with its own stages and its own choice — never a fetch chain.
The sub-quests should be completable in different orders, and the order
chosen should matter (what you learn in one changes your options in the
next — information as loot).

## 4. Personal quests (the stronghold pattern)

Each PC gets quest content **only they can unlock**, arriving *unbidden*
mid-arc — the world offers it because of who they are, not because they
asked at a quest board:

- Keyed to the PC's Shine Time profile (`campaign-dm-strategy.md` §1),
  backstory, artifact, or anointing thread (`pc-protagonism.md` §5).
- **With power comes a domain, and the domain generates problems**: as
  PCs accumulate titles, halls, followers, and fame, their holdings
  produce quests (petitioners, sabotage, succession disputes, taxes).
  This is the BG2 stronghold pattern and the Casa di Davide dynasty
  layer in one mechanism.
- One personal quest active per PC at most; they interleave with the
  main line, never queue behind it.
- The other three PCs must have real roles in it (bonds table,
  coherence §3) — personal ≠ solo.

## 5. The villain's personal claim

Arc antagonists want something *from a specific PC* (soul, lineage,
artifact, guilt, genius). Consequences for quest generation:

- The villain **offers before taking**: at least one stage where the
  claim arrives as a bargain (BG2's bargain-with-the-devil beats).
- The villain's plan *uses* the PCs — their actions somewhere in the
  quest advance his agenda until they see it (the manipulation reveal
  is a stage transition).
- Record the claim as a `Claim:` line on the villain file
  (`npc-villain-boosting` output format).

## 6. The rival party

A recurring mirror group of adventurers pursuing the same objectives:

- 3–5 named members with one-line personalities and a leader with a
  grudge or grudging respect toward a specific PC.
- They appear 2–3 times per arc: once ahead of the party, once
  interfering, once at a moment of choice (fight / bargain / rescue).
- Killable but expensive (political patrons, split loyalties, one
  member the party likes). Every clash arms echoes.

## 6-bis. The set-piece arc (Palio pattern — worked exemplar in repo)

For a multi-session self-contained event (tournament, festival, siege
council, race), the gold standard is the Palio di Channathgate
(`...P2D-PALIO-DM-MASTER-REFERENCE.md` + allegati). Its reusable shape:

- **Dual nature**: playable standalone *and* a geopolitical node — its
  outcome feeds the main campaign in numbers (votes, reinforcements,
  clock ticks), satisfying §7 by construction.
- **Hub + attachments**: one master file (tone, structure, checklist)
  routing to per-day/per-subsystem files — same progressive-disclosure
  layout as the skills themselves.
- **Real-world procedural skeleton**: built on a documented real ritual
  (the historical palio, step by step), then reskinned — borrowed
  structure gives instant depth and coherence for free.
- **Victory conditions beyond winning**: making the rival lose counts;
  the bittersweet result and the playable disaster branch are distinct
  outcomes (see `consequence-echoes.md` §3-bis).
- **Milestone grid on the time axis** + ceremonial meters
  (`living-world.md` §5-bis) + PC offices with powers and debts
  (`pc-protagonism.md` §2).

When generating a new set-piece arc, clone this shape, not the Palio's
content.

## 7. Side-quest discipline

Every side quest must touch **at least one** of: a faction (PART 4
tracker), an armed echo, a PC thread (bond, anointing, artifact), or a
villain clock. A side quest touching none is filler — rewire or cut.
Side quests respect the main clocks (coherence §5.2): time spent is
time the villains use.

## 8. Generation checklist

When asked to "crea una quest" / "genera una side quest":

1. Load `state.md` (§0 dashboard, §7 threads + §7.E echoes) and
   `campaign-coherence.md`.
2. Pick the shape: staged main / mirrored factions / quest-in-quest /
   personal / rival-party interference.
3. Write stages in the dm-expansion-toolkit PART 2 format, one
   reframing question per stage.
4. Wire minimum connections: 1 faction, 1 echo fired or armed, 1
   Shine Time tag per stage, final stage = owned choice.
5. Apply the scene mixer (SKILL.md) for each stage's prose tone.
6. Run the style self-check + coherence self-check before delivering.
