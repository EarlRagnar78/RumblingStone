# PC Protagonism — Protagonists in Good and in Evil

The campaign's contract: **the four PCs are the protagonists of every
scene that matters** — when they are heroic, when they fail, and when
they choose evil. The world is reactive (State Machine, coherence §5),
but reactivity must always be *legible as a response to them*.

This file extends (does not replace) the Shine Time system in
`rumblingstone-campaign/references/campaign-dm-strategy.md` §1 and the
PC bonds table in `campaign-coherence.md` §3.

---

## 1. The Protagonism Test (every generated scene)

A scene passes if at least ONE is true:

1. A PC makes a decision with a cost (not "which door", but "what do I
   give up" — triangolo di rischio).
2. A PC's *past choice* visibly shapes the scene (an echo fires — see
   `consequence-echoes.md`).
3. A PC's backstory, bond, artifact, or anointing thread is on stage.
4. The scene hands a PC narrative authorship (HDYWTDT cue, a plan to
   design, an NPC who defers to them).

If none is true, the scene is scenery — cut it or rewire it. NPCs
never resolve plot among themselves on-screen; if two NPC factions
clash, the scene is generated *from the vantage of what the PCs can
see, exploit, or prevent*.

**Protagonism is the camera, not gravity.** This test constrains how
scenes are *framed*, never why the world *moves*: NPCs, villains, and
factions act for their own Want/Fear, off-screen and on, including
against party convenience (`living-world.md`). An NPC who exists only
to serve the PCs' plot fails the living-world check; a scene the PCs
merely watch fails this test. Generated content must pass both.

## 2. Spotlight rotation (Mercer layer, formalized)

- Session plans mark each scene with `Shine: <PC>` — whose profile it
  serves (Artemis: intrigue/system-cracking; Thorik: command/diplomacy;
  Tordek: engineering/physics-breaking; Hella: moral compass/nature).
- Quota per session: every PC ≥1 marked scene; no PC >40% of marked
  scenes.
- Killing blows and clutch saves: generated encounter content includes
  `[HDYWTDT — hand the finisher to the player]` at boss-death and
  arc-climax points.
- Bonds count as spotlight: a scene serving the Tordek↔Hella or
  Thorik↔Artemis bond serves both PCs.

## 3. Protagonists in the good — fame

Track a **Fama** line per PC (and one for the party) in `state.md` §7
as subsection `### §7.R Reputation (Fama / Infamia)` — same pattern as
the `§7.E Echo Ledger` (`consequence-echoes.md` §1), so no existing
section is renumbered. Fame is earned by *witnessed* deeds and spreads
at rumor speed, distorted:

- Deeds gain epithets: NPCs address PCs by what they did ("il nano che
  spense la fornace", "colei che tornò dalla pietra"). Generate one new
  epithet per arc; reuse established ones.
- Fame is spendable: doors open, prices drop, militia obey Thorik,
  strangers bring Hella their disputes. Spending fame is a resource
  decision, not free flavor.
- Fame attracts: petitioners, imitators, recruiters, and — per GoT —
  people who need the PCs' fame for their own agendas.

## 4. Protagonists in the evil — infamy and the ripple

PCs are allowed to choose badly; the world must take those choices as
seriously as their heroism. Two mechanisms:

**Infamia** (mirror of fame): witnessed cruelty, broken promises,
desecrations. Same rules — epithets, rumor speed, attraction (extorters,
blackmailers, zealots, would-be apprentice villains).

**The ripple onto the house** (Casa di Davide layer): when a PC commits
a genuine wrong, the primary price lands on what they love — followers,
temple standing, family, the bond partner — with a fuse of 2–4 sessions,
never instantly. Write it as an echo with `tone: tragic`. The point is
consequence-as-tragedy the player can *recognize as authored by their
own choice*, never DM revenge. Rules of use:

- Proportionality: the ripple is at most as large as the wrong.
- Legibility: when it lands, the causal chain must be reconstructible
  by the players in one conversation.
- A door back: every ripple includes at least one path of repair
  (restitution, confession, quest) — redemption is story, damnation is
  an ending. The PC may refuse the door; that too is protagonism.

**Never punish the player for engaging.** Infamy content must generate
*play* (leverage, dilemmas, enemies with faces), not lectures or loss
of agency.

## 5. Anointing threads (destiny without railroad)

Each PC carries one open **anointing thread** — a destiny-shaped hook
(Casa di Davide layer) they can pursue, defile, or ignore:

- Written as: `Anointing: <PC> — <mark> — <status: dormant/active/
  embraced/defiled/refused>` in `state.md` §7.R (Reputation subsection).
- The mark is *potential*, announced by the world (a prophecy-shaped
  rumor, an heirloom that wakes, an NPC prophet's word) — never a
  scripted outcome.
- Refusal and defilement are valid resolutions and generate their own
  arcs (the refused crown becomes someone else's — who?).
- At most one anointing beat per PC per arc; destiny is seasoning.

## 6. Villains must have a personal claim

Every arc-level antagonist wants something *from a specific PC* (BG1/2
layer): Artemis's ring, Tordek's engineering genius, Thorik's command
legitimacy, Hella's grace. Generic world-domination villains are
support cast. When generating or boosting a villain
(`npc-villain-boosting`), add a `Claim:` line — which PC, what they
want, what they'll offer before they take.

## 7. Output requirements

Generated content must carry these markers where applicable:

- Session plan scenes: `Shine: <PC>` tags.
- Encounters: `[HDYWTDT]` cue at climax kills.
- NPC cards: `Voice:` and `Wants from each PC:` lines.
- Villains: `Claim:` line.
- Wrong-doing scenes: a `tone: tragic` echo written to the ledger.
- Recaps: address each PC's contribution by name and epithet — recaps
  are per-PG (see `scripts/session_recap.py` per-PG recap support).
