# Cronaca della campagna — gruppo corrente

> **Cos'è**: ciò che è **successo a questo tavolo**, arco per arco. È **partita**:
> il reset di un gruppo nuovo la riporta al template
> `campaign/templates/chronicle-blank.md` (ADR-0050 §7).
>
> ⚠️ **Non è la fonte di verità sullo stato corrente**: quella è
> `campaign/state.yaml` per i fatti e `campaign/state.md` per la prosa, e dove
> questo file dice altro vince lo stato. Qui si racconta *come ci si è arrivati*.
> Molti paragrafi descrivono in avanti archi **preparati e non ancora giocati**
> (il confine è in `state.md` §0): la tabella del party qui sotto, per esempio,
> dà Hella «Alive» come sarà **dopo** il rito, mentre al tavolo è morta dall'Arco
> 06 (`state.md` §1).
>
> **Da dove viene**: da `campaign-history.md`, diviso il 2026-09-24 (lotto 4f-2,
> decisione D20): le righe sono quelle di allora, spostate e non riscritte.
> La **premessa condivisa** (AP, ambientazione, grafo dei villain, riferimenti)
> sta in [`campaign-premise.md`](campaign-premise.md) e non si azzera.

---

# RumblingStone Campaign — Complete History & Narrative Reference

Last updated: 1372 DR, Flamerule (in-world) / 2026-03-31 (real world)

This file is the **single source of truth** for the RumblingStone campaign narrative.

## Il gruppo

**Party Name:** The Rumbling Stone — a group of mostly dwarves who make heavy sounds and are not stealthy
**Current Level:** 13 | **Party Size:** 4 PCs

### The Party

| PC | Race | Class | Level | Artifacts | Status |
|---|---|---|---|---|---|
| **Thorik** | Shield Dwarf (M) | Fighter 13 | 13 | Aegis Fang (axe), Corona di Adamantio (crown) | ✅ Alive (died once, resurrected) |
| **Tordek Durinheart** | Shield Dwarf (M) | Fighter 4 / Monk 9 | 13 | Bracieri Gemelli di Moradin (gauntlets) | ✅ Alive |
| **Hella Oakenshield** | Shield/Gold Dwarf (F) | Ranger 1 / Druid 12 | 13 (post-resurrection) | Collana dei Semi Eterni (necklace) | ✅ Alive (died in arc 06, resurrected as Treant Hybrid) |
| **Artemis** | Human (M) | Warlock 13 | 13 | Ring of Chaotic Illumination (reforged) | ✅ Alive (survived cerebromorphosis) |

### No-Rogue Strategy

The party has no rogue. They handle traps via Tordek's high Monk saves, arcane utility via Artemis's warlock/ring powers, divine magic via Hella's druid spells, and raw tankiness via Thorik.

---

## PART 2: ADVENTURE ARC TIMELINE (Chronological)

### Phase A: Red Hand of Doom — Opening (Levels 4–6)

**Arc 00 — Drellin's Ferry & the Red Hand**

- Source: `00_Red Hand Of Doom/`
- The party begins on the Dawn Way. The Red Hand horde invades Cannath Vale.
- **Drellin's Ferry Assault:** The town is attacked and ultimately destroyed by the horde.
- **Thorik dies** defending Drellin's Ferry. He is resurrected through divine intervention of Moradin and bonds with the artifact **Aegis Fang** (a dwarven waraxe adapted from FR lore).
- **Capitana Lorana's garrison falls** during the same opening assault wave. The party meets Lorana there for the first time. **A travelling half-elf bard, Maestro Tempestas (canonized 2026-05-04)**, is caught in the assault while passing through on diplomatic business for Rethmar. He uses *Shadow Walk* and *Sleep* to help the party + Lorana evacuate ~23 civilians from a collapsing district. Tempestas considers himself in **lifelong debt** to the party from this moment. He reappears as a recurring messenger NPC in Arc 09 (post-Hammerfist hooks). See `Bestiario/png/Tempestas/Tempestas.md`.
- Source files: `00_Red Hand Of Doom/`, `PG/Artefatti/Artefatti-Pg/Aegis Fang/`, `Bestiario/png/Lorana/Lorana/Lorana.md`, `Bestiario/png/Tempestas/Tempestas.md`

### Phase B: Hammerfist Hills & The Quest for the Corona (Levels 6–8)

After Drellin's Ferry, the party travels to **Hammerfist Holds** in The North Wall mountains. There, dwarven clerical oracles — guided by visions from Moradin — explain that an ancient artifact, the **Corona di Adamantio**, must be found to save the dwarven kingdom from the imminent horde battle. The **Hammerfist King** gives the party a quest to descend into the Underdark and recover it.

### Phase C: Underdark Descent (Levels 8–12, Arcs 01–06)

The party descends through a chain of connected underground locations:

#### Earth Node Transit (Pre-Arc 01, unnumbered) `[DM 2026-07-26]`

- **Location:** a **private chamber inside Hammerfist Holds**
- **What happens:** **clerics and druids of Moradin** open a connection through
  an **earth node**, and send the party into the Underdark. This is the party's
  entry point — they do not walk down.
- **Arrival:** the **fungi zone**, which is **under attack by the minotaurs at
  that very moment**. The attack in progress *is* the hook: it triggers the
  Minotaur Lair quest.
- **Significance:** the descent is a **sending**, not an expedition. The party
  is deposited into someone else's war already in progress, with no route home.

#### The Drow Market of Sonjak (Pre-Arc 01, unnumbered) `[DM 2026-07-26]`

- **Location:** a **fork in the Underdark road, on the way to the Minotaur
  Lair** — encountered *before* the lair
- **The descent:** a long, steep stair cut into the rock leads down from the fork
- **The stair is guarded, and the party does not know it:**
  - **invisible drow** watch the entire descent
  - **invisible spiders** hang from the vault above
  - **only Artemis sees them**, using his powers — and uses that knowledge to
    **restrain the party's swagger**
- **The market:** at the bottom the stair opens into a **wide cavern with three
  tents**. The drow **do not attack — they trade**, at extortionate prices:
  **potions, weapons, and slaves**
- **Faction:** a party under **Matrona Sonjak**
- **Significance:** a drow encounter that is *not* a fight. The danger is the
  **misstep**, not the battle — and only one PC knows it. The money the party
  spends here **funds Sonjak**.

#### Minotaur Lair (Pre-Arc 01, unnumbered)

- **Location:** Below Hammerfist Holds, first Underdark area
- **Source:** Adapted from *Expedition to Undermountain* (p.165) and *Underdark* sourcebook
- **Villains:**
  - **Maur** — Underdark native creature, **CR 11** (defeated) — the DM's XP ledger:
    *«il capo dei minotauri maur cr 11»*. The old «CR ~10» was the Collezionista's
    («un rakasa (il collezionista fuggito cr 10)», same ledger line).
  - **Il Collezionista** — A Rakshasa who uses a bonded basilisk to turn enemies into macabre statues and sells them to evil clients as trophies. **ESCAPED** — recurring villain.
- **Key Events:**
  - Il Collezionista escaped the battle. He later formed a hook/alliance with the drow faction, providing them with strange and pure evil artifacts — possibly the same artifacts the drow seek during the Battle of Rethmar.
  - **How he escaped** `[DM 2026-07-26]`: he **turned invisible**. By then every
    PC was down **except the monk (Tordek)**, who could not see where he went.
    He carried away an **obsidian pendant** (or comparable magic item) that moved
    him elsewhere — another location in Faerûn, or another plane, temporarily.
    → **Proposed resolution `[INFERRED — needs DM confirmation]`: the Plane of
    Fire, the salamander forge where his guild trades.** Rationale: his guild
    *already* has a canonical planar route (Therysol was sold "to salamanders in
    the Fire Elemental plane, forced to serve at the forge"); obsidian is already
    tied to the Fire Plane in campaign canon; and it plants Arc 07 three arcs
    early. ⚠️ Must remain **distinct from and lesser than** the *Sigillo di
    Ossidiana* (Shar-aligned artifact, `[CANONE — DM 2026-07-23]`).
  - **The monk is the only witness** — he knows the Collezionista vanished, and
    does **not** know where. Live hook until Arc 07.
  - **Encounter composition** (from the XP ledger, `CalcoloPuntiEperienza-current.ods`):
    *"Il capo dei minotauri **maur** cr 11, una **gorgone** cr 8, un **rakasa**
    (il Collezionista)"*. ⚠️ The ledger records a **gorgon**; the DM and this
    document record a **bonded basilisk**. **Basilisk stands**: the DM named it
    explicitly on 2026-07-26 (*«maur, basilisk e rachasa»*, recorded in
    `plans/SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05.md` §9.3).
  - Source: *Underdark* p.95 (Maur), p.93 (Cristal Warriors)

#### Gardens of Resplendent Hues (Pre-Arc 02, unnumbered) `[DM 2026-07-26]`

- **Adapted from:** *Drow of the Underdark* p.189
- **Discovered:** thanks to **Hella and the fungi**, after the Minotaur Lair
- **The trials:** **Hella passes them**, and gains the ability to **travel the
  mycelium**, carrying the rest of the party with her
  - the other PCs must make a **Fortitude save DC 17** or be **nauseated**
  - **Artemis fails it**
- **Why it matters mechanically:** the trials are **not a reward — they are the
  means**. Without the mycelium the party would have had no way of reaching the
  Fungi Tower at all.
- **The condition nobody stated:** the gift carries an unspoken condition. It is
  **revoked in Arc 05** — see there.

#### Neverlight Grove (Fungi Tower) (Pre-Arc 02, unnumbered)

- **Adapted from:** *Out of the Abyss* (D&D 5e) Neverlight Grove, converted to 3.5 rules
- **Key Content:**
  - Giant mushroom tower with crazed myconid inhabitants
  - Second level infested by web spiders and drow-modified creatures
  - Specialized drow researchers conducting experiments mixing fungi and aberrations
  - Connection to **Sonjak** (Drow Matrona) and **Mother of Fungi** — undiscovered by party
  - *Expedition to the Demonweb Pits* (p.67) creatures used by the drow researchers
  - Portal to deeper levels (used by escaping drow, and later by the party)
- **Party missed:** The connection between Mother of Fungi, drow architect Sonjak, and Il Collezionista
- **Zuggtmoy is canon** `[DM 2026-07-26]` — the Queen of Fungi. The XP ledger
  records a *"maledizione di yuggtmoy"* on the corpses in the tower; she is the
  reason the myconids are crazed and the chamberlain is demonic. She is believed
  to **know the location of the ancient dwarven mine**.
- **Sonjak's pact with Zuggtmoy** `[DM 2026-07-26]`: Sonjak reshaped the tower
  **in both structure and space** — by **agreement with Zuggtmoy**, in exchange
  for permission to run her **aberration experiments** there. The tower is not a
  dungeon: it is a **laboratory paid for with a bargain**.
- **The audience never taken** `[DM 2026-07-26]`: **Hella wanted to meet
  Zuggtmoy**, without truly knowing what awaited her — *madness, at minimum*.
  The party instead chose to **chase the fleeing drow through the portal**,
  without knowing where it led. By luck, it was the right direction.
  → Zuggtmoy is therefore **never met on screen**, exactly like Sonjak. Two
  powers, no faces: only their works are ever seen.
  → Hella's wish stays **unfulfilled**; she dies in Arc 06 without it.
- **The one-way portal** `[DM 2026-07-26]`: located **inside the Fungi Tower**.
  It dumps both the **fleeing drow** and the **party** into the zone near the
  mine, where they meet the **crystal monster** (the *Cristal Warriors*,
  *Underdark* p.93).

#### Arc 01 — La Miniera (Ancient Dwarven Mine)

- **Source:** `01_LaMiniera/`
- **Enemies:** Grell Necromancer lair, Grell Patriarch (aberration, defeated)
- **Cristal Warriors** — Encountered in this area (source: *Underdark* p.93)
- **Notes:** First part of the ancient dwarven mine. Cristal Warriors encountered in early rooms after portal arrival to the mine complex.
- **Arrival** `[DM 2026-07-26]`: the party reaches this area through the **one-way
  portal in the Fungi Tower**, while chasing fleeing drow. The **crystal monster**
  is the first thing they meet on the other side.
- ⚠️ **Do not conflate** the *Cristal Warriors* here with the **elder xorn**
  encountered much later, near Belkram's Tomb (XP ledger: *"1 mostro a 3 gambe —
  un elder xorn"*). Two different creatures, two different moments.

#### Arc 02 — Scaladossa /

- **Source:** `02_scaladossa-abbattor-funghi/`
- **Adapted from:** *Expedition to Undermountain* — Belkram's Fall section SKeletal Scaffold sections (p.123)
- **Enemies:** evil dwarwen of abador necromancer
- **Key Events:** after defeating the necromancer, the party finds the ring of Chaotic Illumination that it bonds with Artemis .
  
#### Arc 03 — La Cittadella (Abandoned Citadel)

- **Source:** `03_la Cittadella/`
- **Adapted from:** *Expedition to Undermountain* — Belkram's Fall section the Citadel (p.122) and *Expedition to Undermountain* — Belkram's Fall section the Dwuarf Temple (p.140)
- **Key Content:**
  - Moradin Temple with Undead Beholder (CR ~13, defeated)
  - Runic frescoes containing clues about the Corona di Adamantio
  - Abandoned dwarven citadel with lore about the ancient kingdom
  - Encounter with a group of drow slavers and their leader, a drow sorcerer, who are also looking for the Corona di Adamantio and command a retriever monster (defeated)

#### Arc 04 — Tomba di Belkram (Belkram's Tomb)

- **Source:** `04_tomba_di_Belkram/`, `04_tomba_di_Belkram/00_Celebromorfosi/`
- **Adapted from:** *Expedition to Undermountain* — Belkram's Fall section (p.117)
- **Key Content:**
  - Xorn encounters, Gelatinous Cubes, gargoyle turrets
  - **Illithid worm encounter** → Artemis suffers cerebromorphosis crisis
  - **Ring of Chaotic Illumination** first major activation — Dawn's Defiance (crisis power) saves Artemis
  - **Artemis REJECTS the Lord of Sun and Shadow prestige class** offered by Lathander and Mask, choosing to remain a warlock and forge his own chaotic path
  - Ring absorbs dual divine essences differently due to the rejection
  - Source: `PG/Artefatti/Artefatti-Pg/PrestigeClass/lord_sun_shadow/`, `PG/Artefatti/Artefatti-Pg/Artemis/Cerebromorphosis/`

#### Arc 05 — Stanza Runica (Runic Room)

- **Source:** `05_aa-stanza-runica/`
- Ancient dwarven runic puzzle room
- **La Quest della Gemma dell'Antico Portatore** — spiritual plane (5,800 XP per
  PC, the single largest award in the ledger)
- **HELLA LOSES THE MYCELIUM GIFT** `[DM 2026-07-26]` — the pivotal consequence
  of this arc:
  - the party **burns the fungi** present in the room, provoking the
    **fungal wrath**
  - the gift granted in the *Gardens of Resplendent Hues* is **revoked**
  - **it was never a price — it was a condition**, and the party violated it
    without knowing it existed
  - **the culprit is the party, not an enemy.** Hella pays for someone else's
    decision
- **Who knows what** — keep these three levels apart when running or writing it:
  | Party | Knowledge |
  |---|---|
  | **The DM** | the truth: burned fungi → fungal wrath |
  | **Hella** | that the power is **gone**. She **felt** it and **formed
    suppositions** — she has no confirmation |
  | **The group** | may not know they are the cause |
- **How to run it:** nothing is announced. The loss is a **sensory beat** — the
  mycelium simply stops answering: a silence where a voice used to be.
- **Escalation of offence** `[DM 2026-07-26]`: the party first **declined the
  Queen's audience** (Fungi Tower), then **burned her fungi** here. The fungal
  wrath is the **second** slight, not a caprice — it has a progression.
- **Still live:** Hella dies in Arc 06 and returns in Arc 07. Confirmation of
  *why* she lost the gift can therefore arrive **after her resurrection**.

#### Arc 06 — Stanza Corona di Adamantio (Crown Chamber)

- **Source:** `06_Stanza-corona-di-adamantio/`
- **Key Events:**
  - Boss battle for the Corona di Adamantio — Thorik passes the trial and wears the Crown
  - **Hella Oakenshield DIES** during this battle
  - Hella's corpse is preserved by the party
  - Party opens the portal to the Eternal Forge

### Phase D: The Eternal Forge (Levels 12–13, Arc 07)

#### Arc 07 — Il Portale Della Forgia Eterna (Eternal Forge Portal)

- **Source:** `07_il Portale Della Forgia Eterna/` (20+ files)
- **Structure:**

```
[Sala della Forgia Eterna (Hub Room)]
    ├── Altare del Cuore di Moradin (Heart of Moradin artifact)
    ├── Fire Plane Portal (Part 3) ── Gemma Topazio ACTIVATED
    │   ├── Elemental fire combats
    │   ├── Rituale Gemma del Tempo → TOPAZ activated
    │   ├── Tordek finds Bracieri Gemelli di Moradin (Fire Phase)
    │   └── Party finds NPC Therysol
    ├── Earth Plane Portal (Part 4) ── Gemma Smeraldo ACTIVATED
    │   ├── Forest of Living Crystal ← CURRENT PARTY LOCATION
    │   ├── Tordek completing Bracieri Earth awakening
    │   └── Rituale Gemma Terra → EMERALD activated
    ├── Hella Resurrection Ritual (Part 3B)
    │   ├── Moradin's divine intervention + party sacrifices
    │   ├── Thorik sacrifices 2 permanent HP
    │   ├── Tordek sacrifices 500 XP
    │   ├── Artemis sacrifices invocation slot for 24h
    │   └── Hella returns as Treant Hybrid (-1 level → restored by story XP)
    └── Temporal Portal (Part 5, requires Topaz + Emerald active)
        ├── Portal to Year -1000 DR
        ├── Battle at ancient Hammerfist
        └── RUBY gem activates at dawn during temporal battle
```

#### Eternal Forge — Gem Activation Chronology (Definitive)

1. **"Il Momento del Risveglio"** (COMPLETED) — Thorik passes trial, wears Corona. All 3 gems present but ALL DARK.
2. **Sala Forgia Eterna (Part 2)** — Entry, exploration, preparation
3. **Piano Fuoco (Part 3)** — Elemental fire combats → **TOPAZ ACTIVATED** via Rituale Gemma del Tempo
4. Return to Sala → **Rituale Cuore di Moradin** (between Parts 3 and 4) — Activates Cuore di Moradin artifact (separate). **HELLA RESURRECTION** possible (-1 level)
5. **Piano Terra (Part 4)** — Elemental earth combats → **EMERALD ACTIVATED** via Rituale Gemma Terra
6. Return to Sala → **Temporal Portal opens** (requires Topaz + Emerald)
7. **Viaggio Temporale (Part 5)** — Battle at year -1000 DR → At dawn → **RUBY ACTIVATED** (3rd gem)
8. **Ritorno Presente e Battaglia Finale (Part 6)** — Return to present, all gems active

#### NPC Therysol (Found in Fire Plane)

- **Source:** `Bestiario/png/Therysol/`
- **Background:** Was a slave (with her brother) sold by drow traders affiliated with Il Collezionista's guild to salamanders in the Fire Elemental plane, forced to serve at the forge. Her brother died and left a crystal that fused with her, transforming her into the being she is now — an unicum.
- **Motivation:** Hates salamanders and the elemental plane. Helped the party during Fire Node quests.
- **Current Status:** Was guarding Hella's corpse in the Sala della Forgia Eterna. After Hella's resurrection, she goes deeper underground seeking the origin of her destiny — which is Il Collezionista's drow guild — to find revenge.
- **Future Hook:** Can appear as NPC ally during the Notte dei Drow assault on Rethmar (arc 09, Phase 0), attacking drow from within.
- **Source files:** `Bestiario/png/Therysol/`

### Phase E: Return to RHoD Mainline (Level 13+, Arcs 08–09)

#### Arc 08 — La Battaglia di Hammerfist (4 Sessions)

- **Source:** `08_La Battaglia Di Hammerfist/` (9 files + 2 subdirectories: Mappe/, immagini/)
- **Main DM Guide:** `ARC08-01-GUIDA-DM.md` (168KB, 3312 lines)
- **Supplementary files:**
  - `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` — Visual atlas with tactical maps (master, piano ARC-08 A8; supersedes `00_ATLANTE VISIVO...-complete.md` and `ARC08-90-DEPRECATO-battle-stats-maps.md`, both DEPRECATED)
  - `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` — Unit & character sheets
  - `ARC08-03-REGISTRO-PERDITE.md` — Loss tracking sheets
  - `hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md` — Encounter guide
  - `mass_combat_guide_Dm.md` — Mass combat mechanics
  - `combat_prompts_guide.md` — Prompt sequence for mass combat

**Army Composition:**

| Force | Units | Commander(s) |
|---|---|---|
| **Red Hand Army** | 900 (7:1 numerical advantage) | Fauci di Palude (Black Dragon CR 15), Generale Grimjaw (Orog Fighter 10/Warlord 3, CR 14), Gorthak il Trifronte (3-Headed Ettin, CR 12) |
| **Hammerfist Dwarves** | 300 | Re Thorek Hammerfist (Fighter 15/Noble 2, CR 16), Madre Superiora Dana Forgiapietra (Cleric 12/Divine Singer 3, CR 14) |
| **External Allies** | ~20 | Signore Ventolesto (Celestial Giant Owl, CR 8), 12 Ranger Elfici su Gufi (CR 8 each), Orion Pelleorsa (Druid 14, CR 14), Maestro Tempestas (Bard 12/Archmage 2, CR 14) |

**Red Hand Structure:** 4 assault lines — 1st Wave (450 hobgoblin/orc infantry), 2nd Wave (233 heavy infantry + sergeants), 3rd Line (45 giants/artiglieria + mages), 4th Line (66 command/reserve), Aerial (Fauci di Palude + rider), Flanks (50 Worg Riders)

**Session Structure (4 Sessions):**

- **Session 1 — L'Ombra sulla Montagna:**
  - Players control **4 temporary dwarven PNGs**: Borin Ferropugno (Fighter 10/Champion 3, CR 13), Dara Occhiolesto (Ranger 8/Mountain Scout 4, CR 12), Thorin Runaforte (Cleric 9/Runepriest 3, CR 12), Nala Cantapietre (Bard 8/Spymaster 4, CR 12)
  - Reconnaissance mission, Council of War, fortify defenses
  - PNG actions determine initial battle bonuses/maluses

- **Session 2 — Tre Giorni di Sangue e Ferro:**
  - **Day 1:** Assault on outer walls — Hobgoblin waves + Gorthak charges gate
  - **Day 2:** La Breccia nella Roccia — Commander duels, protect the Cantitrici della Pietra (5 Cleric 8/Bard 4 singers, CR 11 each — group ability "Coro della Montagna": Earthquake/Mass Cure/Greater Shout)
  - **Day 3:** Il Soffio della Disperazione — Fauci di Palude dragon attack (acid breath + acid cone variant), desperate retreat into mountain depths

- **Session 3 — Dalle Profondità della Terra:**
  - Last stand at the Heart of the Mountain (Cuore della Montagna)
  - **★ INCONTRO 3C: Il Miracolo della Sfera** — A sphere of molten metal materializes at the altar of Moradin. It explodes in golden sparks → **the Rumbling Stones emerge from the forge-fire**
  - PNG transition: PNGs become DM-controlled, players take over their real PCs
  - **Corona di Adamantio presence effect:** All dwarves heal 2d4+4 HP, +6 morale, Remove Fear, all dwarven weapons become +1, Daylight + Bless
  - Enemy terror: Orcs TS Will DC 20 or Frightened 10 rounds
  - **★ INCONTRO 3B: L'ARRIVO DEI RUMBLING STONES** — Controffensiva epica through 3 phases (Counterattack → Pursuit → Reconquest)
  - Each PC gets a unique heroic action (Lancio Leggendario, Risveglio della Montagna, Terremoto del Pugno, Esplosione Caotica)
  - **Grimjaw arrives** for final showdown if still alive (Round 14–15)

- **Session 4 — La Tempesta e la Vittoria Finale:**
  - **Incontro 4A: La Battaglia Aerea Suprema** — Signore Ventolesto + Owl Riders + Orion + Tempestas vs Fauci di Palude
  - **Incontro 4B: La Carica Finale** — Final push, remaining bosses (Grimjaw/Gorthak last stand)
  - **La Vittoria Agrodolce** — Victory with heavy losses

**Outcome & Casualties:**

| Side | Initial | Casualties | Survivors |
|---|---|---|---|
| Red Hand | 900 | 850+ killed/wounded | 20–30 orcs fled; **Fauci di Palude ESCAPED** (gravely wounded) |
| Hammerfist | 300 | 210 killed | 90 dwarves + Re Thorek alive |
| External Allies | ~20 | 5 rangers wounded, 2 owls wounded | No deaths among aerial allies |

**Transition Mechanics (PNG → PC):**

- Borin → Fighter PC: +2 morale to attacks with dwarven weapons (permanent)
- Dara → Druid/Ranger: +4 competence to Survival/Spot in mountains (permanent)
- Thorin → Monk/Paladin: +2 sacred AC when defending ally (permanent)
- Nala → Warlock/Rogue: 1/day *Invisibility* as swift action (permanent)

**Rewards:** 50,000gp each in gems, Thane titles, personal fortress, legendary fame across Faerûn

**Epilogue — L'Eredità della Battaglia:**

- Hammerfist rebuilt with draconic steel (from Fauci di Palude's scales)
- **Cerimonia delle 100 Asce** (Day 21 post-Hammerfist, canonical closing event of Arc 08): Re Thorek formally honors the 210 dead with 100 ceremonial adamantine axes (one per unit/notable warrior), pronounces all 210 names with elder cantillation, and concludes with the Giuramento delle 90 (the surviving 90 + 9 of Drellin's Ferry + 92 from prior months). The 4 PCs are publicly recognized as **Custodi Eterni** with rune di pietra di adamantio. Three external visitors arrive coordinated but discreet: **Maestro Tempestas** (Rethmar intelligence agent, brings Brenna Sorvane's private letter to Thorik + intel exchange mission), **Capitana Lythiel** (Sacred Forest druid-ranger, presents Saraah's Acorn of the Circle to Hella post-cerimonia). During Atto 3 of the rite (rune handover), **Artemis's Ring of Chaotic Illumination vibrates** — Zalkatar at the Invisible Tower is preparing the monthly relocation; the Ring senses its previous owner. **Lathander + Mask** subsequently appear in Artemis's dream (Notte 22-23) revealing Zalkatar's identity (3-century ex-cleric of Mask turned Mind Flayer by choice) and movente (lettura sperimentale, not killing). Detail file: `08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md`. **Tordek's Tournament invitation does NOT arrive at the Cerimonia** — it arrives later at the Sacred Forest from **Sorella Maewen** (Confraternita Monastica di Dauth, see `Bestiario/png/Maewen/Maewen.md`).
- Fauci di Palude alive = future threat hook
- Red Hand remnants may seek revenge
- Re Thorek names PCs "Custodi Eterni di Hammerfist"

#### Arc 09 — Continuazione Arco Narrativo (Post-Hammerfist)

- **Source:** `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/` (74 markdown files + 6 images)
- **Master Index:** `INDICE-GENERALE-COMPLETO-CAMPAGNA.md`
- **Structure:**

##### Part 1 (P1): Hella's Personal Quest — Il Cerchio Sacro della Foresta

- Bosco Sacro dei Druidi: Hella undertakes the ritual to become Avatar della Natura
- 3 phases with escalating drow attacks (EL 9 → EL 11 → EL 12)
- Success: Druid Circle offers nature help for Battle of Rethmar (animal invocations, shapeshifting like Beorn in The Hobbit)
- Source: `Arco-Post-Hammerfist-P1A/P1B/P1C-*` (7 files + 2 supplements + 1 errata)

##### Part 2A (P2A): Artemis's Personal Quest — Torre Invisibile

- Artemis confronts **Zalkatar**, the previous Ring of Chaotic Illumination owner
- **Zalkatar** is an ancient Illithid Warlock Drow (CR 13) — boss of the Invisible Tower
- 4-level tower with golem defenders, arcane puzzles, and dimensional portals
- Ring powers undergo further awakening (Ultimate Chaos abilities)
- Source: `Arco-Post-Hammerfist-P2A-Torre-*` (12 files)

##### Part 2 — Rhest: Città Sommersa & Drago Nero

- **Source:** Red Hand pag 67–80, adapted to Cannath Vale
- Lake Rhest exploration — sunken city ruins, boat/underwater mechanics
- Razorfiend encounters in the swamp
- **Wyrmlord Saarvith** (CR 12, fighter/dragon disciple) commands the area
- Boss: **Regiarix** Adult Black Dragon (CR 13)
- Consequences: Slows horde 3 days, critical intelligence gathered
- Source: `Arco-Post-Hammerfist-P2-RHEST-*` (8 files)

##### Part 2B (P2B): Tordek's Personal Quest — Torneo Epico di Dauth

- Dragon Ball / Naruto-style martial arts tournament lasting 3 days
- **Orbe delle Otto Porte** (Orb of Eight Gates) — scenic artifact with Naruto-style chakra gate mechanics:
  - Each gate: free action, +2 STR/DEX morale, +2 saves for 1 round
  - Cost: cumulative 1d4 CON temporary damage + fatigued condition
  - When total CON drain reaches current CON, character collapses
  - Concentration DC 20 + gates already used to activate safely
- **Day 1:** Preliminaries — 3 rapid 1v1 fights. Dynamic rotating platform arena.
- **Day 2:** Semifinals — Mistress of Mirrors (illusionist), Pillar Golems, floating columns, mirror labyrinth
- **Day 3 Finale:** vs Grandmaster Rihan (Monk 14) → **INTERRUPTED by Githyanki Red Dragon aerial attack**
  - Githyanki mounted on red dragons attack to steal the sage monk's artifact
  - Xal'thor Illithid Commander (psionic, multi-phase boss) joins the chaos
  - The arena becomes a battlefield: PCs must protect the public AND destroy the psionic nucleus
- **Tordek's Chakra Enlightenment:** Through the tournament and Orb interaction, Tordek gains martial spiritual awareness (7 soul gates of jujitsu combat, Naruto-inspired, powers with physical costs and strain to the final power that if and when used leads to disintegration of Tordek)
- Source: `Arco-Post-Hammerfist-P2B-Torneo-*` (16 files)

##### Part 3 (P3): Battle of Rethmar (Final Battle)

- **Multiple Phases:**
  - **Phase 0 — Notte dei Drow:** Night infiltration by drow + fungal aberrations → attack Rethmar temple to steal evil artifact. Connection to Sonjak/Il Collezionista/Mother of Fungi faction. Therysol may appear as ally here.
  - **Phase 1 — Assedio Esterno:** Red Hand horde (hobgoblins, ogres, bugbears, Giants, etc) + Githyanki red dragon faction (if not defeated at Dauth) + drow faction. Multiple dragon colors.
  - **Phase 2 — Ritualisti Draconici:** 10-round ritual to summon Avatar of Tiamat + Azarr Kul
  - **Phase 3 — Azarr Kul & Avatar of Tiamat:** Epic boss fight. Azarr Kul (CR 15 Cleric 10/Fighter 4, half-blue-dragon hobgoblin), fighting on foot — **Tyrgarun** (Old Blue Dragon, CR 18) is NOT his mount (D11 v2); it's a separate sky-terror encounter, grounded and killable only once the Phase 4 Mythal completes
  - **Phase 4 — Circolo degli Otto & Mythal:** 8 archmages create mythal barrier in 7 rounds, animate city statues as stone golems (à la Harry Potter Battle of Hogwarts)
- **Allied reinforcements (conditional):**
  - Hammerfist dwarves: 90 survivors of Arc 08 + Re Thorek
  - 150 dwarf mercenaries (if Tordek wins tournament)
  - Circle of Eight Mages (mythal barrier + animated statues)
  - Druid Circle (if Hella passes ritual): animal summons + shapeshifting warriors
  - Tiri Kitor elves on giant owls (if Starsong Hill quest completed)
  - Ghostlord's spectral lions (if negotiated)
- Source: `Arco-Post-Hammerfist-P3-*` (24+ files)

---

## PART 3: UNDERDARK DUNGEON CHAIN (Corrected Order)

The party's path from the surface through the Underdark, into the Eternal Forge,
and back to the surface for the Red Hand campaign mainline.

```
[Hammerfist Holds (Surface)] ← Quest from Hammerfist King: find Corona di Adamantio
        ↓
[EARTH NODE TRANSIT — private chamber inside Hammerfist]   `[DM 2026-07-26]`
  ├── clerics + druids of Moradin open the connection
  └── the party is SENT, not walked → arrives in the fungi zone
        ↓
[FUNGI ZONE — under minotaur attack, in progress]
  └── the attack IS the hook: it triggers the Minotaur Lair quest
        ↓
[THE DROW MARKET OF SONJAK — fork on the road to the lair] `[DM 2026-07-26]`
  ├── steep stair; INVISIBLE drow on the descent, INVISIBLE spiders above
  ├── only Artemis sees them → restrains the party's swagger
  ├── wide cavern, 3 tents: potions, weapons, SLAVES at extortionate prices
  └── no combat. The danger is the misstep. The money funds Sonjak
        ↓
[Minotaur Lair — Pre-Arc 01, unnumbered]
  ├── Source: Expedition to Undermountain (p.165), Underdark sourcebook
  ├── Maur (Underdark native, CR 11, defeated)
  ├── Il Collezionista (Rakshasa + bonded basilisk, ESCAPED)
  │   └── Later allies with Sonjak's drow guild → provides evil artifacts
  └── Cristal Warriors (Underdark p.93) — also encountered in 01
        ↓
[GARDENS OF RESPLENDENT HUES — the trials]                 `[DM 2026-07-26]`
  ├── Source: Drow of the Underdark p.189
  ├── Hella passes the trials → MYCELIUM TRAVEL, party in tow
  ├── others: Fort DC 17 or nauseated — ARTEMIS FAILS
  └── NOT a reward: it is the MEANS. Without it, no way to reach the Tower
        ↓
[Neverlight Grove — Pre-Arc 02, unnumbered]
  ├── Source: Out of the Abyss (5e→3.5 conversion), Expedition to Demonweb Pits (p.67)
  ├── Dir: 02_scaladossa-abbattor-funghi/ (shared directory)
  ├── Fungi Tower (2+ levels): drow-modified myconid research lab
  ├── Web spider infestations, drow aberration researchers
  ├── Demonweb Pits creatures (p.67) used by researchers
  ├── Connection to Sonjak + Mother of Fungi (UNDISCOVERED by party)
  ├── ZUGGTMOY is canon — Queen of Fungi; "maledizione di yuggtmoy" in the ledger
  ├── SONJAK'S PACT: she reshaped the tower in structure AND SPACE, by agreement
  │   with Zuggtmoy, in exchange for her aberration experiments
  ├── THE AUDIENCE NEVER TAKEN: Hella wanted to meet Zuggtmoy (madness at
  │   minimum); the party chased the drow instead → Zuggtmoy never seen, like
  │   Sonjak. Two powers, no faces — only their works
  └── ONE-WAY PORTAL (inside the Tower): dumps fleeing drow AND the party near
      the mine → first thing they meet is the CRYSTAL MONSTER
        ↓
[01_LaMiniera — Ancient Dwarven Mine]
  ├── Source: 01_LaMiniera/
  ├── Grell Necromancer lair, Grell Patriarch (aberration, defeated)
  ├── Cristal Warriors encountered in early rooms (Underdark p.93)
  └── First part of ancient dwarven mine complex after portal arrival
        ↓
[02_Scaladossa — Skeletal Scaffold]
  ├── Source: 02_scaladossa-abbattor-funghi/
  ├── Adapted from: Expedition to Undermountain — Belkram's Fall, Skeletal Scaffold (p.123)
  ├── Enemies: evil dwarven necromancer of Abbathor
  └── ★ KEY EVENT: Ring of Chaotic Illumination found → bonds with Artemis
        ↓
[03_la Cittadella — Abandoned Citadel]
  ├── Source: 03_la Cittadella/
  ├── Adapted from: Expedition to Undermountain — Belkram's Fall, The Citadel (p.122)
  │   + Dwarf Temple section (p.140)
  ├── Moradin Temple with Undead Beholder (CR ~13, defeated)
  ├── Runic frescoes (Corona di Adamantio clues)
  ├── Abandoned dwarven citadel with ancient kingdom lore
  └── ★ Drow slavers encounter: drow sorcerer + retriever monster (defeated)
      └── Drow also searching for Corona di Adamantio
        ↓
[04_tomba_di_Belkram — Belkram's Tomb]
  ├── Source: 04_tomba_di_Belkram/, 04_tomba_di_Belkram/00_Celebromorfosi/
  ├── Adapted from: Expedition to Undermountain — Belkram's Fall (p.117)
  ├── Xorn, Gelatinous Cubes, gargoyle turrets
  ├── ★ Illithid worm encounter → Artemis cerebromorphosis crisis
  ├── ★ Ring of Chaotic Illumination first major activation (Dawn's Defiance)
  └── ★ Artemis REJECTS Lord of Sun and Shadow prestige class → stays warlock
        ↓
[05_aa-stanza-runica — Runic Room]
  └── Ancient dwarven rune puzzle (prerequisite for Crown Chamber)
        ↓
[06_Stanza-corona-di-adamantio — Crown Chamber]
  ├── ★ Boss battle: Thorik passes trial, wears Corona di Adamantio
  ├── ★ Hella Oakenshield DIES during this battle (corpse preserved)
  └── Party opens portal to Eternal Forge
        ↓
[07_il Portale Della Forgia Eterna — Eternal Forge]
  ├── Sala della Forgia Eterna (hub room)
  ├── Altare del Cuore di Moradin (divine relic, enables resurrection)
  ├── Fire Plane Portal (Part 3) → TOPAZ gem activated
  │   ├── Elemental fire combats, Tordek finds Bracieri Gemelli
  │   └── NPC Therysol found (slave freed from salamanders)
  ├── Hella Resurrection Ritual (Part 3B) → Hella returns as Treant Hybrid
  ├── Earth Plane Portal (Part 4) → EMERALD gem activated
  │   └── Forest of Living Crystal, Bracieri Earth awakening
  ├── Temporal Portal (Part 5) → requires Topaz + Emerald
  │   └── Battle at year -1000 DR → RUBY gem activated at dawn
  └── Return to Present (Part 6) → all 3 gems active
        ↓
[Hammerfist Holds (Surface Return)] ← Party emerges Level 13
        ↓
[08_La Battaglia Di Hammerfist — Battle of Hammerfist]
  ├── Pre-battle: dwarven PNGs fight early siege phases
  ├── ★ INCONTRO 3B: L'ARRIVO DEI RUMBLING STONES — party joins mid-battle
  ├── Mass combat using adapted RHoD mechanics
  └── First use of Corona + Bracieri + Ring artifact synergies
        ↓
[09_Continuazione Arco Narrativo — Post-Hammerfist]
  ├── P1: Hella's Quest — Cerchio Sacro della Foresta
  ├── P2A: Artemis's Quest — Torre Invisibile (vs Zalkatar)
  ├── P2B: Tordek's Quest — Torneo Epico di Dauth
  ├── P2 Rhest: Città Sommersa & Regiarix (Black Dragon)
  ├── P3 Alliances: Starsong Hill, Ghostlord, Sabotaggio Drow
  └── P3 FINALE: Battle of Rethmar (5 phases → Azarr Kul + Avatar of Tiamat)
```
