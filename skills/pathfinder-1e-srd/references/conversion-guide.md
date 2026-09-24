# Converting Between D&D 3.5 and Pathfinder 1e

Source: Paizo's official *Pathfinder RPG Conversion Guide* (free PDF,
paizo.com) summarizes 3.5→PF1e; this file covers both directions for the
needs of a 3.5 campaign that borrows PF1e material.

**Rule of thumb: don't convert — import.** The systems share the d20 OGL
skeleton; printed numbers work as-is at the table 90% of the time. Convert
only the subsystems listed below, and only when they actually come up.

---

## PF1e monster → 3.5 table (checklist)

1. **hp, AC, attacks, damage, saves, DCs, SR, DR, speeds**: keep as printed.
2. **CMB/CMD**: replace with 3.5 grapple = BAB + Str mod + special size mod
   (Large +4, Huge +8, Gargantuan +12, Colossal +16). For trip/bull rush use
   the 3.5 opposed-check rules with the creature's Str/Dex.
3. **Perception** → Spot AND Listen at the same bonus (also Search at
   Int-based approximation). **Stealth** → Hide AND Move Silently.
   **Acrobatics** → Balance/Jump/Tumble.
4. **PF-only feats**: map to nearest 3.5 feat or drop; common maps:
   - Improved Natural Armor / Toughness (PF) → Toughness ×n or Improved
     Toughness `[Non-SRD: Complete Warrior]`
   - Combat Reflexes, Power Attack, Cleave, Vital Strike: Power Attack and
     Cleave exist in 3.5 (use 3.5 wording); Vital Strike has no 3.5 twin —
     drop it or treat as a flavor rider on a single attack.
5. **Channel energy** → 3.5 turn/rebuke undead at cleric level, or keep as a
   house-ruled 30-ft burst (declare which in the encounter file).
6. **Polymorph-line spells** → use the 3.5 spell text.
7. **CR**: keep the printed PF1e CR. PF1e monsters of the same CR are
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

---

## PF1e spells for `--piu-cattivi` — what actually gets you more, and what doesn't

Requested by the DM: *when generating the harsher variant at the same CR, use
PF1e spells where they are stronger.* The mechanism exists
(`genera_creatura.py --piu-cattivi`, or `--incantesimi pf1e`), but the premise
does not survive contact with the table above, and the option is scoped to match
reality rather than the wish.

**On the shared core spells PF1e is not stronger — it is equal or weaker.** The
compatibility table in this same file says so: *grease*, *glitterdust* and
*black tentacles* were nerfed through CMB and save changes; the save-or-die line
(*finger of death* and relatives) was converted into damage; the polymorph line
was rewritten and this repo's standing rule is to cast it from the 3.5 text.
Swapping *fireball* for "PF1e *fireball*" buys nothing: it is the same spell.

Three things do make a PF1e-flavoured caster harder at the same CR, and only the
first is about spells at all:

1. **Spells that exist only in PF1e**, with no 3.5 twin — the list below.
2. **The Advanced template's +4 to mental scores**, which raises every save DC
   by 2. `--piu-cattivi` already applies this; it is the largest single effect.
3. **PF1e summon lists**, which offer better creatures per spell level.

### PF1e-only spells with no 3.5 equivalent

**55 rows**, held in `scripts/dmcore/incantesimi.py` (`PF1E_SOLO`) as
`(Italian name, PRD name)` pairs with the page's own one-line description beside
each. They are a curated pick from the full APG lists transcribed below, chosen
for one thing: whether they change how an encounter goes. The pick is a
proposal; the class and level of every row are checked by
`test_incantesimi.py` against the §"PF1e spell lists" section of this file.

Each is given with its PRD name, because a DM who wants one has to read the PF1e
text — there is no 3.5 paragraph to fall back on. The generator prints them as
`nome italiano (PF1e: prd name)` and lists each in the block's `rincari`.

**Transcribing them from the page caught three errors** that had been written
here by hand from memory first, all of the same kind the 3.5 class lists exist to
prevent:

- *ill omen* was on the sorcerer/wizard list at 1st. It is a **witch**, psychic
  and mesmerist spell. Removed.
- *stone call* was at 3rd for sorcerer/wizard. It is **sorcerer/wizard 2**
  (druid 2, ranger 2). Moved.
- *hungry pit* looked absent on a first automated pass. It is there, at
  sorcerer/wizard 5 — the name carries the focus-component superscript
  (`Hungry Pit`<sup>F</sup>) and the extractor was gluing it to the name. A
  silent absence inside an anchor is worse than a missing anchor: the test still
  passes.

⚠️ **The cleric has no rows at 1st, 6th or 7th, on purpose.** At those levels the
APG adds nothing that changes a fight (1st: *ant haul*, *dancing lantern*; 6th:
*planar adaptation, mass* alone; 7th: nothing). A declared gap beats a row put
there to make the table look complete — a "harsher" variant that is not harsher
is the worst kind of wrong, because nobody sees it until the table.

### What the generator refuses to do

It will not "upgrade" a spell that this file already flags as *nerfed in PF1e*
(*grease*, *glitterdust*, *black tentacles*, the save-or-die line, the polymorph
line). Presenting a weaker spell as the harsher variant would be the worst kind
of wrong: invisible at generation time, and discovered at the table.

---

## PF1e spell lists — the anchor for `--incantesimi pf1e`

These are the **Advanced Player's Guide** spell lists: the spells PF1e *adds*
on top of what 3.5 already has. Pathfinder's core spell list is, name for name,
close enough to the 3.5 SRD that swapping one for the other buys nothing (see
the compatibility table above). What a PF1e caster has that a 3.5 one does not
is this list, and that is why it is the one worth holding in the repo.

`scripts/dmcore/incantesimi.py` (`PF1E_SOLO`) draws a small curated selection
from here, and `test_incantesimi.py` checks every row against this section — the
same discipline as the 3.5 class lists in `dnd-35-srd/references/spells.md`.

⚠️ **What this section is not.** It is not the full PF1e spell list: the core
half is deliberately absent, because for this repo's purpose it is the 3.5 list
under another cover. A future pass that wants PF1e-native casters needs the core
half too.

Source: `pathfinder.d20srd.org`, Advanced Spell Lists (OGL Open Game Content).
Transcribed from the page itself rather than from memory — the check caught
*ill omen* on the wrong class list and *stone call* at the wrong level, both of
which had been written here by hand first.

### Mago / Stregone

- **0**: spark
- **1**: alter winds · ant haul · break · crafter's curse · crafter's fortune · dancing lantern · expeditious excavation · flare burst · gravity bow · hydraulic push · memory lapse · sculpt corpse · stone fist · stumble gap · touch of gracelessness · touch of the sea · vanish
- **2**: accelerate poison · arrow eruption · burning gaze · create pit · create treasure map · dust of twilight · elemental speech · elemental touch · fire breath · glide · share language · slipstream · stone call
- **3**: aqueous orb · blood biography · campfire wall · cloak of winds · devolution · draconic reservoir · elemental aura · enter image · hydraulic torrent · pain strike · seek thoughts · shifting sand · spiked pit · twilight knife · versatile weapon
- **4**: acid pit · ball lightning · calcific touch · detonate · dragon's breath · firefall · moonstruck · river of wind · shadow projection · share senses · true form · wandering star motes
- **5**: fire snake · geyser · hungry pit · life bubble · pain strike, mass · phantasmal web · planar adaptation · suffocation · treasure stitching
- **6**: cloak of dreams · contagious flame · enemy hammer · fluid form · getaway · sirocco · unwilling shield
- **7**: deflection · expend · firebrand · fly, mass · phantasmal revenge · planar adaptation, mass · rampart · vortex
- **8**: euphoric tranquility · seamantle · stormbolts · wall of lava
- **9**: clashing rocks · fiery body · suffocation, mass · tsunami · wall of suppression · winds of vengeance · world wave

### Chierico

- **0**: spark
- **1**: ant haul · dancing lantern
- **2**: blessing of courage and life · ghostbane dirge · grace · instant armor · oracle's burden · share language · weapon of awe
- **3**: blood biography · borrow fortune · elemental speech · enter image · guiding star · nap stack · sacred bond · wrathful mantle
- **4**: blessing of fervor · planar adaptation · rest eternal · spiritual ally
- **5**: cleanse · ghostbane dirge, mass · life bubble · pillar of life · snake staff · treasure stitching
- **6**: planar adaptation, mass
- **8**: divine vessel · euphoric tranquility · stormbolts
- **9**: winds of vengeance

### Druido

- **0**: spark
- **1**: alter winds · ant haul · aspect of the falcon · bristle · call animal · cloak of shade · detect aberration · expeditious excavation · feather step · flare burst · hydraulic push · keen senses · negate aroma · stone fist · touch of the sea
- **2**: accelerate poison · aspect of the bear · burning gaze · campfire wall · eagle eye · elemental speech · feast of ashes · glide · lockjaw · natural rhythm · pox pustules · scent trail · share language · slipstream · stone call
- **3**: aqueous orb · cloak of winds · create treasure map · cup of dust · feather step, mass · hide campsite · hydraulic torrent · lily pad stride · nature's exile · shifting sand
- **4**: aspect of the stag · ball lightning · bloody claws · geyser · grove of respite · life bubble · moonstruck · river of wind · strong jaw · thorn body · true form
- **5**: aspect of the wolf · blessing of the salamander · fire snake · rest eternal · snake staff · threefold aspect
- **6**: sirocco · swarm skin
- **7**: rampart · vortex
- **8**: euphoric tranquility · seamantle · stormbolts · wall of lava
- **9**: clashing rocks · tsunami · winds of vengeance · world wave

### Bardo

- **0**: sift · spark · unwitting ally
- **1**: beguiling gift · borrow skill · dancing lantern · feather step · flare burst · innocence · invigorate · memory lapse · restful sleep · saving finale · share language · solid note · timely inspiration · touch of gracelessness · vanish
- **2**: blood biography · cacophonous call · create treasure map · dust of twilight · enter image · gallant inspiration · ghostbane dirge · hidden speech · honeyed tongue · versatile weapon
- **3**: arcane concordance · campfire wall · coordinated effort · elemental speech · feather step, mass · invigorate, mass · jester's jaunt · purging finale · reviving finale · seek thoughts · thunderous drums
- **4**: denounce · discordant blast · ghostbane dirge, mass · heroic finale · treasure stitching · wandering star motes
- **5**: bard's escape · cacophonous call, mass · cloak of dreams · deafening song bolt · foe to friend · frozen note · phantasmal web · stunning finale · unwilling shield
- **6**: brilliant inspiration · deadly finale · euphoric tranquility · fool's forbiddance · getaway · pied piping

### Ranger

- **1**: ant haul · aspect of the falcon · call animal · cloak of shade · dancing lantern · detect aberration · feather step · glide · gravity bow · hunter's howl · keen senses · lead blades · negate aroma · residual tracking · tireless pursuit
- **2**: accelerate poison · allfood · arrow eruption · aspect of the bear · bloodhound · campfire wall · chameleon stride · create treasure map · eagle eye · guiding star · hide campsite · hunter's eye · lockjaw · perceive cues · protective spirit · slipstream · stone call · versatile weapon
- **3**: aspect of the stag · bloody claws · cloak of winds · feather step, mass · instant enemy · life bubble · strong jaw · tireless pursuers · venomous bolt
- **4**: aspect of the wolf · blessing of the salamander · bow spirit · grove of respite

### Paladino

- **1**: challenge evil · ghostbane dirge · grace · hero's defiance · honeyed tongue · knight's calling · rally point · veil of positive energy
- **2**: aura of greater courage · bestow grace · blessing of courage and life · corruption resistance · fire of entanglement · instant armor · light lance · paladin's sacrifice · righteous vigor · sacred bond · saddle surge · wake of light · weapon of awe
- **3**: divine transfer · fire of judgment · ghostbane dirge, mass · holy whisper · marks of forbiddance · sanctify armor · wrathful mantle
- **4**: blaze of glory · fire of vengeance · forced repentance · king's castle · oath of peace · resounding blow · sacrificial oath · stay the hand

