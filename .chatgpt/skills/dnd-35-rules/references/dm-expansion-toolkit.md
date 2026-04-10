# DM Expansion Toolkit — RumblingStone Campaign

This file is the **DM's scratchpad and expansion layer**. It contains:
1. Monster art generation prompts (PNG upscale-ready)
2. Branching quest trees for artifacts, villains, and factions
3. Secondary objective and side quest bank
4. Villain expansion templates
5. Faction alliance/opposition tracker
6. DM "add your own" section

---

## PART 1 — MONSTER ART GENERATION

### How to Generate Monster Art

Use any of these free/open tools to generate visual references for monsters at the table:

**Free AI art tools (2026):**
- **Stable Diffusion** (local, free): https://github.com/AUTOMATIC1111/stable-diffusion-webui
  Models: SDXL + realistic_vision for monster art; fantasy_worlds for environments
- **Comfy UI** (local, free): https://github.com/comfyanonymous/ComfyUI — more control
- **Bing Image Creator** (free, web): https://www.bing.com/create — DALL-E based
- **Leonardo.ai** (free tier): https://leonardo.ai — good for fantasy subjects

**Upscaling free tools:**
- **Real-ESRGAN** (local): https://github.com/xinntao/Real-ESRGAN — 4× upscale, open source
- **Upscayl** (desktop app, free): https://upscayl.org — GUI wrapper for ESRGAN
- **Topaz Gigapixel** (paid) — best quality for print

**Recommended workflow:**
```
1. Generate base image with SD/DALL-E (512×512 or 768×768)
2. Upscale 4× with Real-ESRGAN or Upscayl → 2048×2048
3. Crop to monster only; remove background (remove.bg or GIMP)
4. Save as PNG with transparency → use as VTT token in Owlbear Rodeo or Roll20
```

---

### Monster Art Prompt Templates

Use these prompts in Stable Diffusion (SDXL) or DALL-E. Adjust details as needed.

**General structure:**
```
[creature type], [key physical features], [posture/action], [color palette],
[lighting], [art style], [quality tags]
```

**Quality tags to always append (Stable Diffusion):**
```
highly detailed, D&D 3.5 monster manual art style, fantasy illustration,
professional concept art, dramatic lighting, no background, transparent background
```

#### Red Hand of Doom / Cannath Vale Monsters

**Hobgoblin Warrior (Standard Soldier)**
```
hobgoblin warrior in red-lacquered iron armor, battle-scarred face with orange skin and
amber eyes, holding a glaive, aggressive combat stance, red and black color scheme,
torchlight from below, D&D monster manual style, full body, no background
```

**Hobgoblin Wyrmlord (Elite Leader)**
```
hobgoblin warlord in ornate black plate armor with dragon motifs, cloak of deep crimson,
one eye replaced by a glowing red gem, commanding pose, five-headed dragon standard behind him,
dramatic backlit sunset, D&D fantasy illustration style, full body portrait
```

**Azarr Kul (High Wyrmlord, BBEG)**
```
powerful hobgoblin warpriest, muscular, wearing full plate engraved with Tiamat's five heads,
horned helm, cloak of iridescent black scales, wielding a dragon-headed morningstar,
crackling with five-colored elemental energy, throne room background of stone and dragon
skull trophies, epic fantasy art style, vertical portrait
```

**Regiarix (Adult Black Dragon)**
```
adult black dragon, massive obsidian scales dripping with swamp water, acid dripping from
curved fangs, enormous wingspan, perched on a half-submerged stone ruin emerging from a
bog, yellow eyes with vertical pupils, dramatic overcast sky, dark fantasy style, full body
```

**Saarvith (Green Dragon Wyrmlord, wyvern-rider)**
```
hobgoblin ranger in green leather armor, lean and cunning expression, bow slung across back,
riding a wyvern through forest canopy, green scale cloak, poison vials on belt, dappled
forest light, D&D fantasy illustration, dynamic pose
```

**Tiri Kitor Wild Elf Scout (Shaarcah Forest Conclave)**
```
wild elf ranger, bare-footed, wearing leaf-weave leather armor with natural camouflage
patterns, green-grey body paint, bow drawn, crouching in dense undergrowth, alert amber eyes,
dappled forest light filtering through canopy, D&D 3.5 art style, full body
```

**The Lich of Vraath Keep (The Ghostlord adaptation)**
```
ancient lich in tattered Netherese scholar's robes, skeletal hands visible, phylactery pendant
of carved bone, surrounded by floating necrotic runes in Draconic script, haunted stone
fortress hall with collapsed ceiling, green-black energy emanating from eye sockets, high
fantasy undead aesthetic, vertical portrait
```

**Black Exarch (Koth the Mudwing, Wyrmlord)**
```
heavyset hobgoblin in swamp-crusted black iron armor, alligator skull pauldrons, wielding
a great flail with barbed chains, standing knee-deep in murky swamp water, mist at ankles,
overcast grey sky, sinister expression, D&D fantasy art
```

#### Standard Monsters (Reusable)

**Ogre Shock Trooper**
```
enormous ogre in crude iron plate armor reinforced with scrap metal, wielding an iron-bound
club the size of a tree trunk, war paint on grey-green skin, one eye blind and scarred,
bellowing war cry, battlefield with smoke, D&D monster manual style
```

**Manticore Rider**
```
goblin cavalry riding a manticore in mid-flight, the manticore's lion body with iron-tip
tail spines, wings spread wide against a stormy sky, goblin rider in chainmail lashing with
a short whip, dramatic aerial angle, D&D fantasy illustration
```

**Will-o-Wisp Cluster (Lhespenbog)**
```
three spectral floating lights hovering above dark swamp water at night, pale blue-white
ethereal glow, surrounding a half-sunken stone tower, fog at water level, eerie silence,
dark fantasy illustration, hauntingly beautiful
```

---

### Token Generation for VTT

For Roll20 / Owlbear Rodeo tokens, use this Stable Diffusion config:
```
Aspect ratio: 1:1 (square)
Resolution: 512×512 → upscale to 1024×1024
Style: bust portrait, circular frame, solid dark background
Prompt suffix: "token art, circular frame, top-down perspective, game token"
```

Then in Owlbear Rodeo: Upload PNG → Set as token image → Set size to match grid

---

## PART 2 — BRANCHING QUEST TREES

### Quest Structure Format

```
QUEST: [Name]
Type: [Main / Side / Artifact / Faction / Villain]
Hook: [How the party discovers this]
Stage 1: [Initial goal + condition to advance]
  → Branch A: [If PCs succeed in X]
  → Branch B: [If PCs fail X or take different approach]
Stage 2: [Second goal; may differ by branch]
Stage 3: [Climax / resolution]
Rewards: [XP / loot / story rewards]
Connections: [Links to other quests]
```

---

### MAIN QUEST TREE — The Red Hand of Tiamat

```
QUEST: The Red Hand Marches
Type: Main AP
Hook: Session 1 opening — the PCs are in Rethmar or on the Old North Road / The Dawn Way when the first
      hobgoblin raids strike.

Stage 1: Stop the Advance Guard
  Goal: Defeat/route the hobgoblin advance and close Nimon Gap temporarily
  → Branch A (success): Gain 2 weeks before main horde arrives; Shaarcah Forest elves willing to talk
  → Branch B (partial): Gap only slowed; lose 1 week; elves remain neutral
  → Branch C (failure): Horde arrives early; Drellin's Ferry area burns AND Witchcross; start at −1 week

Stage 2A: The Skull Gorge
  Goal: Destroy or hold the Bridge (Skull Gorge equivalent)
  → Success: Horde must spend 5 days finding another crossing; party gains time for allies
  → Failure: Horde crosses; Drellin's Ferry is next target immediately
  Note: Even on failure, a partial success (slowing the horde) is valuable.

Stage 2B (parallel): Lhesper
  Goal: Eliminate Wyrmlord Koth in the Lhespenbog before he flanks Rethmar
  → Success: Lose the black dragon support; lizardfolk may flip to neutral
  → Failure: Koth flanks Rethmar during the final battle; adds +20% horde STR

Stage 3: The Ghostlord's Bargain
  Goal: Deal with the Lich of Vraath Keep
  → Diplomacy (DC 30 with preparation, DC 35 cold): Lich withdraws from the pact → loses 40
    wyverns from horde roster
  → Combat: Kill Wyrm Cultists guarding the lich's phylactery; destroy it; lich destroyed
  → Bad deal: Give him a living lion (his heart, original RHoD), but narrative cost: lich
    remains in the vale post-campaign as a neutral (and unpredictable) power

Stage 4: Battle of Rethmar
  Goal: Survive the assault; defeat Azarr Kul
  → Full victory: Azarr Kul slain; horde fragments; Tiamat's plan set back decades
  → Pyrrhic victory: Kul slain but Rethmar burns; survivors rebuild; vale scarred
  → Partial: Kul escapes; campaign continues with follow-up (see Villain Expansion below)

Rewards (full completion): +6,000 XP/PC; "Defenders of Cannath Vale" title; Vale Council grant
```

---

### ARTIFACT QUEST CHAINS

#### Quest Chain A — The Phylactery of Vraath Keep

```
QUEST: The Lich's Secret Heart
Type: Artifact (Major)
Artifact: Phylactery of the Lich of Vraath Keep
  A glass-and-bone orb, 6 inches diameter, warm to the touch, containing a spark of greenish
  witchfire. If the lich is destroyed while the phylactery exists, he reforms in 1d10 days.
  If destroyed, the lich dies permanently but releases 4d6×10 years of stored necrotic energy
  (everyone within 30 ft takes 10d6 negative energy damage, Fort DC 22 half).

Hook: Found in stage 3 of main quest (Vraath Keep) OR purchased from an underground dealer in
      Cannathgate for 12,000 gp (he doesn't know what it is).

Stage 1: Identify the Phylactery
  → Spellcraft DC 28 or Legend Lore → reveals its nature and the lich's location
  → Branch A: Party wants to destroy it → Stage 2
  → Branch B: Party tries to use it as leverage → Diplomacy branch (see main quest Stage 3)
  → Branch C: Party sells it (!) → The buyer is a Red Wizard agent → Villain hook

Stage 2: The Destruction Ritual
  Goal: The phylactery cannot be destroyed by mundane means. Options:
  → Holy site destruction: Bring it to the Moonwatch Hill and have Sertieren perform a 3-hour
    ritual (req: 500 gp in components, party must defend against 3 waves of lich's undead)
  → Divine request: A cleric of Kelemvor or Torm of 9th+ level can destroy it with a special
    casting of Dispel Evil + Consecrate (combined effect) — costs 1,500 XP
  → Throw it into lava: There's no volcano nearby. Finding one is a separate mini-quest.

Stage 3: Consequence
  → Phylactery destroyed: Lich permanently dead; 500 XP per PC; lich's hoard (7,000 gp
    equivalent in gems and scrolls) now safely accessible in Vraath Keep
  → Lich freed from pact (diplomacy branch): He gives the party one free casting of a 7th-level
    spell (his choice) and withdraws from the vale. The phylactery remains hidden — unknown
    variable in future campaigns.

Connections: Main Quest Stage 3; Faction (Red Wizard agent Branch C)
```

#### Quest Chain B — The Five-Headed Talisman

```
QUEST: Azarr Kul's War-Standard
Type: Artifact (Minor)
Artifact: The Talisman of Five Fangs
  A medallion of black iron inlaid with five gemstones (black, blue, green, red, white)
  arranged like Tiamat's heads. Functions as a minor artifact:
  - +4 CHA to anyone who worships Tiamat (evil only)
  - +2 CHA to all others
  - 3/day: Command (as spell, DC 16) targeting non-Tiamat worshippers
  - 1/day: Cause Fear (DC 15) in a 20-ft burst
  - Curse: Non-evil wearers must make Will DC 18 each week or become increasingly obsessed
    with power and begin making suboptimal choices for personal gain

Hook: Found on Azarr Kul's body at the Battle of Rethmar (if he falls there)
      OR looted from his command tent in the Fane of Tiamat approach

Stage 1: What Is This?
  Identify (Spellcraft DC 25, Legend Lore, or consult Sertieren): Reveals talisman is a
  material anchor — destroying it here weakens Tiamat's direct influence on this crusade but
  does not destroy the horde.
  → Keep it: The curse begins; DM tracks weekly Will saves
  → Consecrate it: 2,000 gp + cleric of Torm/Tyr at 10th+ level; removes curse; item becomes
    a standard +2 CHA item that loses all special properties
  → Destroy it: See Stage 2

Stage 2: Destroying the Anchor
  Options (parallel to phylactery destruction logic):
  → Submerge in blessed water at a temple of Selûne: Temple of Selûne in Cannathgate has a
    blessed spring; 3-hour ritual; Tiamat cultists will try to stop it (8 fanatics + 1 cleric)
  → Counter-ritual at the Shaarcah Forest's heart: Elves offer to unmake it through forest magic;
    req: party to return the elves' stolen sacred idol (Side Quest: The Taken Idol)

Stage 3: Consequence
  → Talisman destroyed: Horde loses morale cohesion bon; in the final battle, EL drops by 2
  → Talisman kept and cursed PC: Eventually acts as a plot driver for a follow-up campaign
  → Talisman given to Red Wizard (mistake): Szass Tam now has a direct Tiamat connection

Connections: Main Quest Stage 4; Side Quest: The Taken Idol; Faction: Tiamat's Cult
```

---

### SECONDARY OBJECTIVE BANK

Use these as "B-plot" sessions, downtime adventures, or parallel tracks:

```
[1] THE TAKEN IDOL
A Shaarcah Forest elf sacred idol (a carved moonwood owl, worth 300 gp, divine focus for Rillifane
Rallathil) was stolen by hobgoblin scouts in Kythorn. The Conclave won't negotiate until it's
returned. The idol is in Wyrmlord Saarvith's tent in the western The Wyrmbones base camp (CR 10 encounter).
Reward: Shaarcah Forest Conclave becomes Allied (provides 12 scouts + forest intel for final battle)

[2] THE CRESSFALL ORPHANS
20 children from burned Drellin's Ferry area are sheltered in Rethmar's mill, under the care of a
traumatized halfling woman (Exp 1). Commander Sorann wants them evacuated to Cannathgate
before the main assault. Escort mission — 3 days on the Old North Road / The Dawn Way, 2 random encounters.
Reward: 600 XP; the halfling's uncle is a fence in Cannathgate who will identify items for free

[3] THE MURKMERE RIVER RUNNERS
A band of lizardfolk (8 warriors, Cpt at Ftr 3) is opportunistically raiding both sides —
they hate the hobgoblins as much as the humans. A PC with Handle Animal or Diplomacy (DC 22)
can recruit them as irregular allies. The catch: they demand 400 gp in "river toll" payment.
Reward (recruited): 800 XP; 8 lizardfolk skirmishers for the Battle of Rethmar (AC 15, 2 attacks)

[4] THE DESERTER'S CACHE
A hobgoblin sergeant named Grakh has deserted. He has his unit's logistical plans (maps of
supply depots, encoded in hobgoblin military script). Tracking him (Survival DC 18) and
convincing him to defect or extracting the plans is worth 2 weeks' advance INT:
DM may reveal one encounter from the next chapter before it occurs.
Reward: 700 XP; pre-knowledge of one upcoming encounter

[5] THE RED WIZARD OBSERVER
A Red Wizard named Zara Vel (Wiz 9, NE, Thay) is in Cannathgate, quietly observing the invasion.
She is NOT helping the horde — she's evaluating whether Thay can exploit the chaos afterward.
Approach options: Ignore (she leaves; no consequence); Confront (she defends herself; CR 9);
Negotiate (she'll share INT on the horde's logistics for a favor owed to Thay — moral
weight here; accepting makes the party indebted to a Red Wizard)
Reward: Varies by approach; intel is worth 600 XP equivalent if extracted diplomatically

[6] THE MOONWATCH HILL RITUAL
Sertieren the Wise is trying to cast a sending to Silverymoon but the hobgoblin warcaster
(Wiz 7 equivalent) is running a magical interference ritual from the The Wyrmbones. The party
must reach and disrupt the interference site (a 2-day climb into the foothills; CR 8 encounter
with the warcaster and 4 gnoll bodyguards) so Sertieren's sending goes through.
Reward: 900 XP; Silverymoon responds with a wand of cure moderate wounds (21 charges) and
a promise to send a 10th-level wizard advisor within 2 weeks

[7] THE CULT OF THE DRAGON ADVANCE AGENT
A half-dragon (human base) Cult of the Dragon agent (Rgr 4 / Dragon Disciple 3) is in the vale,
creating a network of "safe houses" for surviving Wyrmlords to use after the campaign ends.
Finding the network (Investigation over 2 sessions) and dismantling it is a meta-campaign
objective that pays off in reduced difficulty in a potential follow-up campaign.
Reward: 1,000 XP; a Cult communication crystal worth 800 gp as an item; intel on the follow-up

[8] VRAATH HOLD'S VAULT (Exploration)
Vraath Keep is a ruin — but the original owners buried a vault beneath the courtyard. Finding
it req:: Research in Rethmar's mill-archive (Knowledge: History DC 18), then excavation
(8 hours, 4+ people), then bypassing a 100-year-old arcane lock (Disable Device DC 30 or
Knock). Inside: 3,200 gp in old Cormyrean coin, a +2 light fortification breastplate (old
Purple Dragon style), and a partial spellbook (3 2nd-level, 2 3rd-level spells; DM chooses).
```

---

## PART 3 — VILLAIN EXPANSION TEMPLATES

### Template Format
Each villain has a **base** (from RHoD) and an **expansion layer** (FR-integrated, harder).

---

**AZARR KUL — EXPANDED**

Base (RHoD): High Wyrmlord; final boss; Cleric 11 / Fighter 2
FR Expansion:
- **Tiamat's Voice**: 1/day, Azarr Kul can speak as Tiamat's direct mouthpiece; all creatures
  within 60 ft that hear the Voice must save (Will DC 22) or be Shaken for 1 minute
- **Five Aspects**: Each of his five chromatic dragon scale pauldrons grants a 1/day effect:
  Black=Acid Splash (4d6), Blue=Call Lightning (7d6), Green=Suggestion (DC 18),
  Red=Fireball (10d6 DC 19), White=Ice Storm (at CL 12)
- **Escape Contingency**: If reduced below 30 HP, Dimension Door to the Fane of Tiamat
  (inner sanctum); req: the party to fight through the Fane to finish the job
- **If He Escapes**: See follow-up hooks below.

Follow-up hooks if Azarr Kul escapes:
1. He retreats to a black site in the The Wyrmbones; begins rebuilding the horde (6-month timer)
2. He makes contact with Szass Tam — offers Tiamat's blessing in exchange for Thayan military support
3. He sends assassins (Worg-riding hobgoblin Rgr 6 pairs) to eliminate the PCs over the next month

---

**THE LICH OF VRAATH HOLD — EXPANDED**

The original "Ghostlord" was an old lion-themed druid. The Cannath Vale version is a
**Netherese-era lich** who made a pact with Azuth (not Lolth or a demon) for immortality
through an arcane adaptation of lichdom — he is Lawful Neutral, not evil. He was paid in
the promise that his knowledge would never be lost. The horde's Cult of Dragon agent tricked
him into the pact with Azarr Kul by presenting forged documents claiming Mystra endorsed it.

**Personality**: Cold, academic, occasionally sardonic. Not a murderer — just pragmatic.
**Motivation**: He wants his phylactery protected and his knowledge to persist. He would
rather have the party end the horde (disrupting his forced alliance) than continue.

**Expanded Negotiation** (replaces combat if PCs discover the deception):
- DC 15 Diplomacy to open dialogue (he's skeptical of living creatures)
- DC 22 Diplomacy to reveal the forged documents to him (party must find them first — in the
  Fane's war room, a side objective)
- If deception revealed: Lich immediately breaks the pact; withdraws support; tells party
  the Fane's layout in detail (tactical advantage: remove one ambush from the Fane)
- He asks only one thing: the party swears a magical oath (Geas, cast by him) to protect
  his library (100 unique 3rd–8th level arcane scrolls in Vraath Keep's vault)

---

**SAARVITH — EXPANDED (Surviving Wyrmlord)**

If Saarvith survives the campaign (not unusual given his ambush/escape tactics), he becomes
a recurring antagonist:
- Retreats to the Shaarcah Forest's eastern edge; begins a guerrilla campaign
- Recruits the remaining Koth lizardfolk as a small but effective swamp-raider force
- Has a personal grudge against any PC who killed his wyvern
- Will eventually seek employment from the Zhentarim (offers INT on the vale's
  defenses in exchange for protection and resources)
- Can be found and confronted 3 months post-campaign (Survival DC 22 to track into the
  Lhespenbog; CR 12 encounter with 12 lizardfolk + Saarvith at Rgr 8)

---

## PART 4 — FACTION ALLIANCE / OPPOSITION TRACKER

Copy this into each session log and update after major interactions:

```markdown
## Faction Status — Session [N]

| Faction | Standing | Notes |
|---|---|---|
| Vale Council (Rethmar) | Neutral | Need military credibility first |
| Shaarcah Forest Conclave (elves) | Hostile | Will shift if idol returned |
| Lizardfolk (Lhespenbog) | Neutral | Mercenary; 400gp would buy them |
| Red Wizard (Zara Vel) | Neutral | Observing; can be leveraged |
| Zhentarim (Cannathgate agent) | Neutral | Watching; could be enemy or tool |
| The Lich of Vraath Keep | Hostile (pact) | Shift possible if deception revealed |
| Silverymoon (distant) | Friendly | Sertieren's contact; slow to respond |
| Cult of the Dragon (local) | Enemy | Advance agent active; don't know PCs yet |
| Harper Cell (Cannathgate) | Friendly | Overwhelmed; need PC support to act |

Faction Scales: Hostile / Unfriendly / Neutral / Friendly / Allied
Allied factions provide active military or logistical support in the Battle of Rethmar.
```

**Battle of Rethmar modifiers by Allied factions:**
- Vale Council + militia: +50 defenders (included by default)
- Shaarcah Forest Conclave: +12 elf scouts (rng; devastating in the approach)
- Lizardfolk: +8 irregular skirmishers (mel; unreliable; may break if casualties are high)
- Silverymoon wizard: +1 high-level arcane caster (10th level Wiz) for the final battle
- Harper Cell activated: INT on horde's approach route → first round of battle is not a surprise

---

## PART 5 — DM "ADD YOUR OWN" SECTION

### How to Add a New Quest

Copy this template into `campaign/encounters/` or `campaign/sessions/` as `quest-[name].md`:

```markdown
# QUEST: [Name]
**Type**: Main / Side / Artifact / Faction / Villain
**Suggested party level**: [N]
**Status**: Not started / Active / Complete

## Hook
[How do the PCs learn about this? Be specific: who tells them, where, when.]

## Stage 1: [Name]
**Goal**: [What the PCs need to do]
**DC / CR**: [If applicable]

### Branch A: [If PCs succeed / take approach 1]
→ [Consequence + next stage]

### Branch B: [If PCs fail / take approach 2]
→ [Consequence + next stage]

## Stage 2: [Name]
[Repeat as needed]

## Climax
[Final confrontation or resolution scene]

## Rewards
- XP: [N] per PC
- Gold: [N] gp or equivalent
- Items: [Specific items]
- Story: [What changes in the world]

## Connections
- Links to: [Quest names]
- Affects faction: [Faction name + how]
- Unlocks: [If this quest opens another]

## DM Notes
[Private notes; don't share with players]
```

### How to Add a New NPC

Create `campaign/npcs/[name-kebab-case].md`:

```markdown
# [NPC Name]
**Role**: villain / ally / neutral / quest-giver
**Status**: alive / dead / missing / transformed
**Location**: [current known location as of last session]
**Motivation**: [one sentence, specific]
**Secret**: [one thing the PCs don't know]

## Stats (D&D 3.5)
**Race/Class**: [race, class N]
**CR**: [N]
**HP**: [N] | **AC**: [N] | **Initiative**: +[N]
**Attack**: [primary attack +N mel/rng (Nd6+N damage)]
**Saves**: Fort +N / Ref +N / Will +N
**Special**: [key ability]

## Personality
[2-3 sentences: voice, mannerisms, goals]

## Relationship to PCs
[How they know the PCs; attitude; what they want from them]

## Plot hooks attached to this NPC
- [Hook 1]
- [Hook 2]

## DM Notes
[Private; not for player view]
```

### How to Add a New Encounter Location

Create `campaign/encounters/[location-name].md`:

```markdown
# Encounter: [Location Name]
**Map reference**: [link to image file or "hand-drawn"]
**EL**: [N] | **CR breakdown**: [monster list]
**Terrain**: [description]
**Lighting**: [bright / dim / dark]

## Setup / Boxed Text
> [Read-aloud description for players — keep to 3-4 sentences]

## Tactical Map Notes
- [Key features: difficult terrain, cover, elevation]
- [Monster starting positions]
- [Environmental hazards]

## Monster Tactics
[What each group does on Round 1, Round 2, and on when reduced to 25% HP]

## Treasure
[What's here to find after the encounter]

## Adaptations from RHoD
[Any changes from the original module]

## Wayback Machine / Map Source
[If using a WotC Map-A-Week map: orbitalflower archive URL + Wayback link]
```

---

## NOTES ON USING THE ORBITALFLOWER ARCHIVE FOR MAPS

The **Map-A-Week** series from WotC produced hundreds of grid maps (dungeon rooms, wilderness,
encounter sites) in GIF/JPG format, ideal for VTT play.

### Finding and Using a Map

1. Load https://orbitalflower.github.io/rpg/wizards-3e-archive.html
2. Ctrl+F for "Map-A-Week" — find the index section
3. Click the original Wizards URL → paste into Wayback Machine search:
   `https://web.archive.org/web/*/[original-url]`
4. Select a 2003–2006 snapshot → download the GIF/JPG
5. Import into Roll20 or Owlbear Rodeo as the battle map
6. Set grid to match (most WotC maps use 5-ft squares at approximately 50 or 100px/square)

### Recommended Map-A-Week archives for Cannath Vale

Search these terms in the orbitalflower index:
- "swamp" → for Lhespenbog encounters
- "bridge" → for Skull Gorge
- "fortress ruins" → for Vraath Keep
- "town" → for Rethmar scenes
- "mountain pass" → for Nimon Gap
- "forest" → for Shaarcah Forest encounters