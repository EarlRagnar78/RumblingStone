# The Living World — NPC/Villain Agency and World Reaction

Principle: **the world does not orbit the PCs**. NPCs, villains, and
factions move for their own interests and their own reasons, whether or
not anyone is watching. PC protagonism (`pc-protagonism.md`) governs the
*camera* — how scenes are framed on-screen; this file governs the
*causality* — why things happen at all. The two are complementary:

> **Protagonism is the camera, not gravity.** Off-screen, the world runs
> on agendas. On-screen, scenes are framed from the PCs' vantage: what
> they can see, exploit, prevent, or suffer. An NPC whose only reason to
> exist is serving the PCs' plot fails this file; a scene the PCs merely
> watch fails the Protagonism Test. Good content passes both.

This file extends the campaign's State Machine design
(`campaign-dm-strategy.md` §2, coherence §5.2 "villains advance
off-screen") and grounds it in D&D 3.5 SRD / PF1e OGL mechanics.

---

## 1. NPC agency — Want / Fear / Leverage / Next step

Every named NPC and faction carries four agency lines (on the NPC card
or the faction tracker, `dm-expansion-toolkit` PART 4):

- **Want**: what they pursue *for themselves* — never "help/oppose the
  party". If the Want mentions the PCs, rewrite it one level deeper
  (Varis doesn't want "to trade with Artemis"; he wants a monopoly on
  planar goods — Artemis is currently useful for that).
- **Fear**: what they protect at any cost. Fear is what makes NPCs
  refuse, lie, or betray *even against their own Want*.
- **Leverage**: what they have that others need (goods, access,
  secrets, force). Leverage is why the world keeps knocking.
- **Next step**: the one concrete action they will take *this in-world
  week if nobody interferes*. This is the line the world-turn advances.

NPCs may say no, drive bargains, have bad days, be busy with their own
crises, and pursue goals that have nothing to do with the party. NPCs
interact with *each other*: deals, feuds, and marriages happen between
NPCs off-screen, and the results reach the PCs as news, prices, and
opportunities (GoT layer: the board moves).

## 2. The World Turn (between sessions)

During session prep, run one **world turn** — the operational form of
coherence §5.2:

1. **Clocks**: advance villain clocks (`state.md` §2–§3) by elapsed
   in-world days. Unattended threads resolve (echo rule: absence is a
   choice, `consequence-echoes.md` §2.3).
2. **Agenda steps**: for each *active* named NPC/faction (those within
   reach of the party's region), execute their **Next step**, then
   write the new one. One line each, logged in `state.md` §8 or the
   faction tracker. NPCs act on Want/Fear — not on what would be
   dramatic for the party.
3. **Collisions**: where two agendas cross, resolve the NPC-vs-NPC
   outcome now (a die roll or judgment call). Collisions are the
   world's best content generator — their fallout becomes hooks.
4. **Signals**: choose 2–3 world-turn results and convert them into
   *perceptible signals* for next session — a rumor, a price change, a
   refugee column, a patrol that never reported back, a wedding
   invitation. Tolkien/Andor texture: the players must feel the world
   moving without them (coherence §4 suspense rule).

Budget: the world turn is ~15 minutes of prep, one line per actor. If
it grows past that, retire distant NPCs to `dormant` (they still exist;
they just don't get turns until the party nears their orbit).

## 3. SRD mechanics — attitude as the reaction engine (D&D 3.5)

Use the SRD **NPC attitude system** (Diplomacy skill, d20srd.org) as
the mechanical spine of world reaction. Attitudes: **Hostile /
Unfriendly / Indifferent / Friendly / Helpful**.

- Every named NPC and faction tracks a current attitude **toward the
  party** (and exceptions per PC where bonds/history differ). Record
  it on the NPC card (`Attitude:` line) and in the faction tracker.
- **Starting attitude is set by the world, not the plot**: race
  relations, faction allegiance, Fama/Infamia (`pc-protagonism.md`
  §3–§4), and fired echoes. A dwarf quartermaster starts Friendly to
  Tordek and Indifferent to Artemis for *reasons*, not for pacing.
- **Shifting attitude is play, not fiat**: use the SRD Diplomacy DC
  table (e.g. Indifferent → Friendly DC 15; Unfriendly → Indifferent
  DC 15; Hostile shifts are hard) with situational modifiers the DM
  states out loud. Rushed Diplomacy takes −10 (SRD). Intimidate shifts
  behave temporarily and sour later (SRD) — a lever Thorik can use,
  with echo written.
- **Attitude gates content, not outcomes**: Helpful NPCs volunteer aid
  and information; Hostile ones act on it. But an NPC's Want/Fear can
  override attitude — a Friendly NPC still refuses what their Fear
  forbids. Attitude is disposition, agency is will.
- Rumor flow uses **Gather Information** (SRD): world-turn signals are
  what a DC 10–20 check can retrieve, with quality scaled by the roll
  and by district/faction. Lies and distortions propagate at the same
  speed as truth (fame arrives distorted — protagonism §3).

## 4. PF1e OGL tools — settlements and reactions

Approved support toolkit (same policy as `npc-villain-boosting`): PF1e
OGL material via d20pfsrd:

- **Settlement stat blocks** (PF1e GameMastery, OGL): give each visited
  settlement Alignment, Qualities, Disadvantages, and a **base
  attitude** the same five-step scale applies to. A town's attitude
  moves with the party's public deeds there (echo-driven), and gates
  prices, rumor DCs, and militia response.
- **NPC gallery practice**: stock each settlement with 3–5 statless
  named NPCs (role + Want/Fear/Leverage only); promote to full
  statblocks via `pathfinder-1e-srd/references/npc-building.md` only
  when play demands it. The world feels populated without prep debt.
- **Reaction adjustments**: apply circumstance modifiers (±2/±5) to
  attitude checks for deeds, insignia, reputation, and race relations
  — state them openly so players learn the world's physics.

## 5. Encounter tables as world sensors

Random/travel encounters are not filler — they are **sensors of the
world state**. Re-key encounter tables when clocks advance: if the
Horde is at Day 25, the road tables show forage parties and refugee
columns, not generic bandits. A wandering-monster roll that reflects
the current clocks *is* the living world made visible (and doubles as
the coherence §4 foreshadow requirement). Build tables with
`suggest_encounter.py` where applicable, then reskin entries to the
current world turn.

## 6. The world initiates

At least once per session, the world makes first contact — the party
receives, rather than seeks: a petitioner, a creditor, a summons, a
rival's provocation, an old echo walking through the door. Generated
from agendas (§1–§2), delivered through attitude (§3), framed by the
camera rule (a PC decision inside the scene). This is the BG2
stronghold pattern generalized: existence at the PCs' level of fame
*generates* inbound events.

## 7. Self-check additions (run with the SKILL.md self-check)

1. Does every named NPC in this content have a Want that isn't about
   the PCs? (If no → deepen it one level.)
2. Did any NPC/faction act *against* party convenience for their own
   reasons? (A living world says no to the party sometimes.)
3. Are attitudes and their shifts grounded in SRD mechanics + logged
   causes (Fama, echoes, deeds), not in plot need?
4. Did the world turn produce signals the players can perceive and
   investigate this session?
