# Campaign Coherence Constraints

Hard rules an agent (and DM) must respect when generating new content for
RumblingStone. The point is to keep a long, sandbox-style campaign coherent
across many sessions without losing the R.A. Salvatore tone of slow
internal stakes.

These rules are **enforceable**, not aspirational. If a generated proposal
would violate one, the agent must stop and flag it to the DM rather than
silently retcon.

---

## 0. Source Ranking (when sources disagree)

Higher rank wins. If two facts conflict, take the higher and flag the
lower-rank file as needing an update.

```
1. campaign/state.md                                 (most recent truth)
2. skills/rumblingstone-campaign/references/*.md     (structured truth)
3. campaign/lore/campaign-history.md                  (prose narration)
4. SRD / FR canon                                     (default backdrop)
5. Inferred / model knowledge                         (last resort, must be flagged)
```

If you cannot find a fact in 1–4, **say so**. Do not invent. Ask the DM or
mark the suggestion as `[INFERRED — needs DM confirmation]`.

---

## 1. History Reference Constraints

History is the past. The past is **locked**. Agents may add detail to past
events (a forgotten name, a sensory description) but may not change outcomes,
death/survival of named NPCs, location of resolved encounters, or the order
of events.

### Locked events (NEVER reframe)

| Event | Arc | Locked outcome |
|---|---|---|
| Thorik dies at Drellin's Ferry | 00 | Death, then divine resurrection bonded to Aegis Fang |
| Maur defeated at Minotaur Lair | Pre-01 | Killed |
| Il Collezionista escapes Minotaur Lair | Pre-01 | Escaped (re-uses this villain forever) |
| Ring of Chaotic Illumination bonds to Artemis | 02 | Bonded; cannot be passed to another PC |
| Hella dies in Crown Chamber | 06 | Died, then resurrected at Eternal Forge with cost |
| Cuore di Moradin spent for Hella's resurrection | 07 | Single-use artifact; cannot be re-used |
| Ruby gem of Corona spent at year -1000 battle | 07 | Single-use already expended |
| Hammerfist siege: 210 dwarves killed, 90 survive | 08 | Death toll fixed; named survivors fixed (Re Thorek, Dana Forgiapietra) |
| Fauci di Palude (black dragon) escapes Hammerfist gravely wounded | 08 | Escaped; can return wounded |

### Adding to history (allowed)

- Filling in a side NPC's name not previously stated.
- Describing a room, smell, weather not previously described.
- Adding a private memory of a PC about a past event (with player buy-in).

### Modifying history (forbidden without DM override)

- Changing whether an NPC died.
- Changing who delivered a killing blow.
- Changing the location an event happened.
- Reordering the sequence of arcs.
- Re-using a single-use artifact effect.

If a player asks "what if we had done X instead?" handle it as a hypothetical,
do not actually rewrite the past.

---

## 2. Artifact Constraints

Artifacts are powerful and trackable. Three rules:

### 2.1 Only listed powers exist

An artifact can only do what `campaign-artifacts.md` says it can do, plus
what `state.md` says it currently can do (e.g., a gem newly activated).
Inventing a new artifact power mid-session = coherence violation.

### 2.2 Single-use is single-use

Already-spent powers (see §1 locked events and `state.md` §5) **cannot**
be invoked again. If a player attempts it, the DM rules it out and the
agent must not assist.

### 2.3 Bonded artifacts cannot be transferred

Bondings are listed in `campaign-artifacts.md` and `state.md`:

- Aegis Fang ↔ Thorik
- Ring of Chaotic Illumination ↔ Artemis
- Corona di Adamantio ↔ Thorik (requires dwarf + BAB +5 + Moradin faith OR Aegis Fang bond)
- Bracieri Gemelli ↔ Tordek
- Collana dei Semi Eterni ↔ Hella

A bonded artifact cannot be picked up and used by another PC. It can be
*lost* (stolen, destroyed, etc.) and that becomes a new arc.

### 2.4 Artifact cost is paid, not handwaved

Every artifact effect that has a cost (XP, perm CON, gp, time, age) must
deduct that cost. Agents proposing artifact use must list the cost in the
proposal. The DM enforces. Costs are tracked in `state.md`.

---

## 3. PG Interaction Constraints

### 3.1 NPC knowledge is bounded

An NPC only knows what `state.md` §3 says they know, plus what they could
plausibly have learned through normal in-fiction information channels
(scouts, rumors, divinations they have access to). When generating dialogue,
**check §3 first**. If the NPC has not learned a fact, they cannot reference it.

When an NPC learns something new during play, the DM updates §3 at end of
session. Until then, that fact is private to the party.

### 3.2 Promises are debts

Every promise/bargain in `state.md` §4 is real. Agents proposing scenes must
honor them:

- If Thorik promised to lead Rethmar's defense, NPCs expect him there.
- If Artemis owes Varis an artifact per quarter, that clock ticks even
  off-screen.
- Breaking a debt has the listed consequence — non-negotiable.

When a debt is settled or broken, move it from §4 to §7 (changelog) with
the resolution.

### 3.3 PC personalities are stable

Treat the four PCs per `campaign-party.md` and the DM strategy file:

- **Thorik**: strategic, manager-of-conflict, intolerant of waste, dark humor.
- **Tordek**: anti-authority, engineer-of-physics, drawn to loot.
- **Hella**: moral compass, ethics-first, story-listener, stone-bonded.
- **Artemis**: analytical, exploits-systems, planar-broker, intrigue-magnet.

Generated dialogue or proposed actions must read true to these. If a
proposal makes a PC act against character, flag it.

### 3.4 PC-to-PC bonds are tracked

| Bond | Status | Implication |
|---|---|---|
| Tordek ↔ Hella | Romantic, post-resurrection deepened | Each owes the other narrative space |
| Thorik ↔ Hella | Moral debtor (sacrificed CON for her) | Hella weighs his arguments more heavily |
| Artemis ↔ Tordek | Loot-and-tactics partnership | They scheme together against authority figures |
| Thorik ↔ Artemis | Strategic respect, mutual frustration | Best together when there is a manipulator villain to dismantle |

These bonds should drive at least one Shine Time moment each session per
the DM strategy doc.

---

## 4. Tone Constraints (R.A. Salvatore profile)

The campaign asks for adult, slow-build intrigue. To maintain it, agents
generating prose or read-aloud text must:

- **Do**: physical sensory detail, internal monologue beats, named NPCs
  with backstory, moral cost of victories, cold weather and stone, named
  weapons remembered.
- **Do not**: modern slang, fourth-wall winks, generic fantasy filler,
  cartoonish villains, deus-ex-machina rescues, victory without cost.
- **Pacing**: an investigation scene gets the same word-count as a combat
  scene. Both have stakes.
- **Suspense**: foreshadow at least one villain countdown clock per session
  (a rumor, a missing patrol, a half-overheard ritual). Players must feel
  the world is moving without them.

---

## 5. Sandbox / "Andor-like" Constraints

The user explicitly wants a less-railroad, more-intrigue experience.
Operationally, this means:

### 5.1 Multiple viable next moves

At any point in `state.md` §6 (Open Threads) there must be **at least 3**
viable next-session paths. If there are ever fewer than 3, the DM must
seed new ones before next session.

### 5.2 Villains advance off-screen

Every in-world day, advance the relevant villain clock in `state.md` §2 by
1 (or by the rate listed). This happens whether or not the party is doing
anything related. Players feel the cost of inaction.

### 5.3 No bivio binario (binary-fork)

Never present "Door A or Door B." Always offer a triangolo di rischio:
three competing demands on party resources, where any choice gives up
something. See `campaign-dm-strategy.md` §C for the pattern.

### 5.4 Manipulator villains, not just sword-targets

For each high-level arc, at least one antagonist must be undefeatable by
combat (Conte Valerius pattern). The win condition is political, social,
or evidentiary. This forces Artemis-and-Thorik teamwork.

---

## 6. Agent Self-Check Protocol

Before delivering generated content for this campaign, the agent runs
this checklist (silently or aloud):

1. Did I read `state.md` for current truth? (If no → reload.)
2. Does anything I wrote contradict §1 locked events? (If yes → stop, flag.)
3. Did I invent an artifact power not in `campaign-artifacts.md` or §5 of state? (If yes → strip.)
4. Does any NPC reveal info not in `state.md` §3? (If yes → restrict.)
5. Did I honor promises/debts in `state.md` §4? (If no → revise.)
6. Did I leave at least 3 viable next paths? (If no → seed more.)
7. Tone check: any modern slang or fourth-wall slip? (If yes → rewrite.)

If all pass, deliver. If any fail and the DM is not present, deliver with
explicit `[COHERENCE WARNING: <which rule>]` so the DM can adjudicate.

---

## 7. Changelog (append-only)

```
2026-05-01  Initial coherence rules drafted (Step 8 of skills optimization).
            Source ranking, history-locks, artifact-locks, NPC knowledge
            discipline, PC bonds, R.A. Salvatore tone, sandbox triangolo
            rules, agent self-check protocol.
```
