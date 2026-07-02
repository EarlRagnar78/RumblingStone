# Campaign State — Living World Snapshot

> **Purpose**: single source of truth for what is *currently* true in the
> RumblingStone world. Updated at the end of every session. Agents and the DM
> consult this file *first* before describing NPC knowledge, location of
> villains, status of artifacts, or open narrative threads.
>
> **Rule**: if this file disagrees with `campaign-history.md` or any
> `campaign-*.md` reference, **this file wins** (it is the most recent truth).
> If you change a fact here, do not silently rewrite the history files —
> append a new entry to the changelog at the bottom.

---

**Last updated:** 2026-05-01 (session marker — DM updates)
**In-world date:** Mirtul, 1372 DR
**Party APL:** 13
**Sessions completed:** post-Hammerfist, pre-Rethmar (Arc 09 in progress)

> **DM workflow**: per la procedura di aggiornamento fine-sessione e per
> far partire un nuovo gruppo senza perdere niente, vedi
> [`campaign/DM-CAMPAIGN-PLAYBOOK.md`](DM-CAMPAIGN-PLAYBOOK.md).

---

## §0 Campaign Status At-a-Glance

Cruscotto sintetico. Aggiornato a fine sessione. Vedi sezioni successive per dettaglio.

| Arc | Fase | Stato | March Clock | PG Lv | Note |
|---|---|---|---|---|---|
| 00 Setup RHoD | ✅ | completato | Day 0 | 5 | — |
| 01 Miniera | ✅ | completato | — | 6 | — |
| 02 Scaladossa-abbattor-funghi | ✅ | completato | — | 7 | — |
| 03 La Cittadella | ✅ | completato | — | 8 | — |
| 04 Tomba di Belkram | ✅ | completato | — | 9 | — |
| 05 Stanza Runica | ✅ | completato | — | 10 | — |
| 06 Corona di Adamantio | ✅ | completato | — | 11 | — |
| 07 Portale della Forgia Eterna | ✅ | completato | — | 12 | — |
| 08 Battaglia di Hammerfist | ✅ | completato | **Day 19 (sync)** | 12→13 | Cerimonia 100 Asce, Custodi Eterni |
| 09 P1A Quest Hellas (Cerchio Sacro) | 🟡 | in arrivo | Day 20-30 window | 13 | Deadline Day 30 |
| 09 P1B Cerchio Treant | 🟡 | pianificato | Day 22-28 | 13 | — |
| 09 P1C Rituale Hellas | 🟡 | pianificato | Day 25-30 | 13 | — |
| 09 P2 Rhest (Saarvith + Regiarix) | ⬜ | non iniziato | Day 25-32 | 13 | -1 drago se fatto |
| 09 P2A Torre Invisibile (Zalkatar) | ⬜ | non iniziato | Day 28-35 | 13 | -1 drago se fatto |
| 09 P2B Torneo di Dauth (Tordek) | ⬜ | non iniziato | Day 25-34 | 13 | +300 mercenari nani |
| 09 P2C Salvatore Mercante | ⬜ | non iniziato | Day 28-36 | 13 | Sal clock 0/6 |
| 09 P3 Starsong Hill (Tiri-Kitor) | ⬜ | non iniziato | Day 30-35 | 13-14 | +cavalleria civette |
| 09 P3 Ghostlord | ⬜ | non iniziato | Day 25-32 | 13-14 | 3 branch: ostile/neutralizzato/alleato |
| 09 P3 Sabotaggio Campi Drow | ⬜ | non iniziato | Day 30-36 | 13-14 | -Fase 0 + -75 esperimenti fungini (45 Servitori + 30 Sporeborn; 8 Guardiani Neri sopravvivono) |
| 09 P3 Missioni Brevi CR12 | ⬜ | non iniziato | Day 30-38 | 13-14 | — |
| **09 P3 Battaglia Finale Rethmar** | ⬜ | target | **Day 42** | 14 | Fase 0-4 |

**Legenda**: ✅ completato · 🟡 in corso / imminente · ⬜ non iniziato · ❌ fallito · ⏸ sospeso

---

## 1. Party — Current Position & Condition

| PC | Class | Location | HP / status | Open personal threads |
|---|---|---|---|---|
| Thorik | Dwarf Fighter 13 | Hammerfist Holds, war council chamber | Full; -2 perm CON sacrificed for Hella's resurrection (NEVER restored) | Decide whether to lead defense of Rethmar personally vs. delegate |
| Tordek | Dwarf Fighter 4 / Monk 9 | Hammerfist → traveling to Dauth Tournament | Full; Bracieri Earth phase complete | Tournament of the Eight Gates (3 days, interrupted by Githyanki Day 3) |
| Hella | Dream Dwarf Ranger 1 / Druid 12 | Hammerfist → traveling to Sacred Forest | Full; Treant Hybrid template active post-resurrection | Sacred Forest ritual (pass = druid circle ally at Rethmar) |
| Artemis | Human Warlock 13 | Hammerfist → traveling to Invisible Tower (Dauth region) | Full; Ring of Chaotic Illumination active | Confront Zalkatar (CR 13 illithid warlock); Ring evolution at stake |

**Active companions:**

- Hella's stone rhinoceros companion (DR 5/adamantine, animated post-resurrection)
- Therysol (Tiefling Half-Dragon NPC, traveling separately, hunting Il Collezionista's guild)
- **Maestro Tempestas** (Half-elf Bard 12/Arcmage 2, GS 14, recurring messenger of Rethmar; canonized 2026-05-04 as the "bard storm caller" who helped the party escape Lorana's city in Arc 00 — vedi `PNG/Tempestas/Tempestas.md`). Not constantly present; drops in via *Shadow Walk* every 1–2 sessions with intel.

---

## 2. Active Forces — Live Army Tracker (v2 — Dual Clock)

> **Cross-reference:** Full calculations in
> `00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md`,
> march/attrition waypoint log in
> `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md`, and the
> five PG-scenario force-balance table in
> `09_Continuazione.../Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md`.
> **Update this section at the end of every session.**

### 2.0 Dual-Clock Separation (canon 2026-05-05)

Two independent clocks drive Arc 09:

1. **MARCH CLOCK** — the official AP (RHoD) campaign timeline for the
   physical march of the horde. Deterministic waypoints (except where
   PG have already shifted them). Runs **Day 1 → Day 42**.
2. **RITUAL CLOCK (Azarr Kul)** — rituals at the Fane of Tiamat,
   independent of marching distance. Still `/18`. **Does NOT advance
   with march days.** Advances only on ritual triggers (see §3).

### 2.1 March Clock — Official AP Waypoints

| Day | Waypoint | Status |
|---|---|---|
| 1 | Horde leaves Fane of Tiamat (Shaar) | ✅ Past |
| 6 | Vraath Keep (Channath Vale equivalent) occupied | ✅ Past |
| 8–9 | **Skull Gorge bridge** — crossed intact (PG did NOT sabotage, confirmed) | ✅ Past |
| 12–13 | Drellin's Ferry equivalent falls (burned) | ✅ Past |
| **19** | **Terrelton equivalent falls** | 🎯 **SYNC POINT = End of Battle of Hammerfist** |
| 25 | Marth Fen / Blackfens (Rhest area) | ⏳ Pending |
| 33–35 | Elsir Crossroads / Channath Crocevia | ⏳ Pending |
| 35-37 | **Sonjak halt** — aberrazioni experiments + supply convoy wait | ⏳ Pending |
| 40 | Notte dei Drow / advance scout phase (Fase 0 begins) | ⏳ Pending |
| **42** | **Horde arrives at Rethmar (ex-Brindol) and encamps** | 🎯 **Rethmar assault begins** |

**Current March Day:** **19** (Terrelton just fell as Hammerfist ended).
**Days remaining to Rethmar:** **23** (PG-quest window = Arc 09, Days 20-41).

### 2.2 Red Hand of Doom — Horde Composition (Baseline ~10,000)

| Contingent | Baseline | Notes |
|---|---|---|
| Core Hobgoblin (fanteria + veterani + sergenti + Warrior-3 élite) | 4,800 | |
| Ausiliari Goblin/Orchi/Worg Riders | 1,800 | |
| Giganti + Ogre + Ettin | 180 | NO PG alliance — stay with Red Hand |
| Forze Alate (Manticore, Wyvern, Hell Hounds, Chimera) | 140 | |
| Casters Mano Rossa (War Adepts, Blue, Warpriests di Tiamat) | 55 | |
| **Dragons (5 AP-original upscaled)** | 5 | Abithriax (Red adult) / Regiarix (Black young, Rhest) / Ozyrrandion (Blue, Tower) / Tyrgarun (reserve) / **Fauci di Palude** (Black adult, Hammerfist vanguard) |
| **Draconic spawn = Razorfiend (Tiamat colors)** | 8 | Assigned to Wyrmlord villains upscaled |
| Compagnia Drow di Sonjak | 305 | |
| Githyanki di Vaereth | 375 | |
| Gnoll mercenari (3 tribù: Flinderoso, Abbattitori, Artigli Neri) | 1,100 | |
| Loxo + Centauri corrotti (Shaar) | 480 | ❓ Revolt possible |
| **Compagnia del Teschio Nero** (umani malvagi mercenari, Thay/Mulhorand) | 650 | NEW 2026-05-05 |
| **BASELINE TOTAL** | **~9,900** | ≈ 10,000 ✓ |

**Post-Hammerfist losses (Day 19 sync):** −500 (Fauci di Palude detachment
annientato/disperso; does NOT rejoin main body). Current active:
**~9,400**.

### 2.3 Conditional Additives (apply at Rethmar if triggered)

| Condition | Effect on Horde |
|---|---|
| Ghostlord **NOT neutralized** (default hostile) | +2,400 undead wave at Phase 2 |
| Ghostlord **neutralized by PG** | Only +400 undead (pre-deployed detachment) |
| Ghostlord **redento/alleato** (rare branch) | +600 "good" undead among DEFENDERS instead |
| Xal'thor allies with Red Hand | +400 Illithid thralls |
| Il Collezionista intervenes | +300 Rakshasa cultists |
| PG destroy Skull Gorge bridge | (N/A — already crossed intact) |
| PG sabotage Centaur/Loxo → revolt | −480 horde |
| PG defeat Regiarix at Rhest | −1 dragon, −2 Razorfiend |
| PG defeat Ozyrrandion at Tower | −1 dragon |

**Worst-case horde at Rethmar:** ~12,700 | **Best-case (all PG
sabotages):** ~7,200

### 2.4 Rethmar Defenders — PG-Dependent Balance

**Baseline (no PG quests completed):** ~2,200 → ratio **4.5:1** → sconfitta
quasi certa.

| Contingent | Count | Condition |
|---|---|---|
| Guarnigione Rethmar (Valerius + milizia) | 1,200 | Fixed |
| Rifugiati armati (Elsir/Channath Vale) | 600 | +150/villaggio evacuato in tempo |
| Truppe Consiglio Rethmar | 400 | Via Thorik/Brenna letter |
| **Alleanza Elfi Starsong Hill** | +500 | SOLO se P3-Starsong quest OK |
| **Nani di Dauth** (Tordek torneo) | +400 | SOLO se Tordek vince torneo |
| **Druidi Cerchio Sacro + Treant Hella** | +150 | SOLO se P1B Hella ritual OK |
| **Ghostlord redento come alleato** | +600 non-morti buoni | Branch raro |
| Mercenari Salvatore (rischio tradimento) | ±300 | Instabile |

**Scenari finali (target: PG meaningfully shift balance):**

| Scenario PG | Horde | Difensori | Rapporto |
|---|---|---|---|
| Worst (Ghostlord ostile, Xal'thor allea, 0 quest) | 12,700 | 2,200 | **5.8:1** ☠ |
| Baseline (0 quest) | 9,400 | 2,200 | **4.3:1** |
| Medio (2–3 quest + sabotaggi parziali) | 8,000 | 3,100 | **2.6:1** |
| Ottimale (tutte quest + Rhest + Tower) | 6,800 | 4,100 | **1.66:1** |
| Leggendario (ottimale + Ghostlord redento + Collezionista stop) | 6,400 | 4,700 | **1.36:1** |

**Riferimento Hammerfist:** 900/300 = **3:1** (battaglia vinta con
sacrifici — baseline narrativo).

### 2.5 Infiltratori / Refugee Ledger

**Infiltrators in refugee wave:** 3-5 agents (2 hobgoblin + 1 drow + 2
gnoll disguised). Detect: Sense Motive CD 18 / Detect Magic. If caught:
−2 CR Phase 0. If not: +1 CR + 20 defenders poisoned.

| Settlement | Status (Day 19 sync) | Refugees → Rethmar | Armed +Rethmar |
|---|---|---|---|
| Vraath Keep | ✅ Fallen (Day 6) | ~180 fled | +25 |
| Drellin's Ferry eq. | ✅ Burned (Day 12-13) | ~1,500 fled | +110 |
| **Terrelton eq.** | ✅ **Just fallen (Day 19 sync)** | ~1,600 fleeing | +65 (in transit) |
| Talar | ⏳ Under threat (Day 20-22) | ~400 | +35 |
| Witchcross | ⏳ Under threat (Day 22-25) | ~1,200 (druids stay) | +60 |
| Marth Fen area | ⏳ Day 25 sweep | ~300 | +50 |
| Hammerfist Holds | ✅ Held (+90 survivors; 150 lances conditional) | 0 civilians | +150 ❓ if Tordek wins Dauth |
| Cannathgate | ✅ Not attacked | 0 | +150 ❓ diplomacy |

---

## 3. Active Villain Threads (Countdown Clocks)

State machine, not script. Each villain has an agenda that advances each
in-world day **whether or not the party intervenes**. When a clock fills,
the listed consequence triggers.

| Villain | Where | Agenda | Clock | Trigger if filled |
|---|---|---|---|---|
| Sonjak (Drow Cleric Matrona) — also "Matrona Sajak" in Sal's operative code | Underdark, Cannath Vale border | Subvert dwarven citadel from below; coordinate with Il Collezionista; manage Sal as surface field agent | 4/8 | Drow night-raid on Hammerfist temple (sets up Phase 0 of Rethmar) |
| Salvatore "Sal" della Luna d'Argento | Desert road, Cannath Vale → Rethmar (Shaar) | Profile party's artifacts and magical defenses; plant Sabotage Oil on weapons before Rethmar; deliver living statues to Varis | 0/6 | Sabotage Oil applied — weapon TS failure risk at Phase 3 boss; Phase 4 statue activation proceeds at full strength |
| Il Collezionista (Rakshasa) | Mobile — last seen brokering with drow | Acquire the Crown's spare gem before party can use it; manipulate Conte Valerius | 5/8 | Sponsors anti-party legal pressure; Conte Valerius freezes assets |
| Zalkatar (Illithid Warlock) | Invisible Tower, Dauth region | Mind-strip a captured githyanki for fleet intel | 6/8 | Tower goes mobile; harder to find next session |
| Wyrmlord Saarvith + Regiarix | Lake Rhest ruins | Rebuild dragonrider corps from black dragon spawn | 3/8 | Rhest becomes a fortified war camp; CR +1 to assault |
| Xal'thor (Illithid Coordinator, psionic) | En route with an Illithid invasion force (psionic thralls, larvae, a small core of dominated Githyanki — NOT the free Githyanki dragon-rider force led by Vaereth, which is a separate and hostile faction) | Day 3 fixed assault on the Dauth Tournament to seize Tordek's **Bracieri Gemelli** (planar keys to the Eternal Forge); does NOT target the Orbe delle Otto Porte | Fixed: triggers Day 3 of Tournament regardless | Tournament becomes combat encounter |
| Sethrax il Velato (Illithid emissary, Zalkatar's conclave) | Dauth — infiltrated as tournament finalist "Kethran Mano di Pietra" | Extract a "Seme di Porta" from the Orbe delle Otto Porte during the Tournament's peak resonance, deliver it to Zalkatar at the Invisible Tower | Sync to Tournament (Day 1 = arrival; Day 2 = entered as finalist; Day 3 Round 7 = forced unmasking by Xal'thor's portal) | Sethrax flees to Invisible Tower with the seed → Zalkatar gains +2 effective CR + new orb-derived Mind Blast in P2A finale (Artemis's quest) |
| Azarr Kul (High Wyrmlord) — **Ritual Clock, see §2.0** (NOT the March Clock; the horde's physical approach is tracked separately in §2.1, currently Day 19 of 42) | Fane of Tiamat (Shaar) | Ritual sacrifices/planar conjunctions to summon the Avatar of Tiamat during the Rethmar siege (Day 40-42, Phase 2). Advances only on explicit triggers: +1 per Warpriest élite mass sacrifice (Day 35-38), +2 if Giant Wave ×1 breaches the walls (Phase 1), +3 if Giant Wave ×2 breaches (Phase 3) — see `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §4b | 9/18 | Avatar of Tiamat manifests over Rethmar during Phase 2's 10-round ritual (D8) |
| Conte Valerius (manipulator) | Capital city | Legalize horde funding via "patriotic emergency" loans | 2/8 | Party loses access to legitimate guild merchants |

---

## 4. Open NPC Knowledge State

> Who currently knows what. **Agents must NOT have an NPC reveal something
> they have not learned in-fiction.** Add new rows when an NPC learns
> something; never silently retcon.

| NPC | Knows that... | Learned how / when |
|---|---|---|
| Sonjak (= Matrona Sajak) | The party freed the Cristal Warriors but does NOT know they have all 3 Crown gems | Drow scouts witnessed the mine assault |
| Sonjak | Sal is operating on the desert road toward Rethmar; does NOT know Sal's temporal identity (Vatore) | Standard briefing to field agent |
| Ghostlord / Zeth il Murato | Party existence unknown; aware of Red Hand using his lair as undead factory | Sensed via lair's magical senses |
| Conte Valerius | The party visited Hammerfist; does NOT know about the Crown or Sal | Public dispatches — updated 2026-05-02 |
| Azarr Kul | Party are Custodi Eterni; does NOT know artifact details | General intelligence from Red Hand scouts |
| Xal'thor | Tordek carries the Twin Braziers (planar keys to Eternal Forge) | Planar observation; cross-referenced with Forgia Eterna records |
| Zalkatar (via Sethrax) | The Orbe delle Otto Porte at Dauth Tournament has Githyanki planar origin and emits a "Seme di Porta" extractable at peak resonance | Telepathic dispatch from Sethrax (covert) — refreshed daily; updated 2026-05-03 |
| Sethrax il Velato | Tordek is the orb's primary attuned monk; the orb's first opening triggers a Githyanki "Eco delle Fenditure" vision; does NOT yet know Xal'thor's separate invasion plan | Direct observation Day 1–2 of Tournament |
| Varis "Seta-Argento" | Some statues might be alive; does NOT know Sal is the supplier chain origin | Involuntary observation 3 months ago |
| Il Collezionista | Artemis carries the Ring of Chaotic Illumination | Witnessed at minotaur lair; sent guild operatives to track |
| Il Collezionista | Therysol is alive and hunting him | Inferred from missing guild operatives in Underdark |
| Re Thorek Hammerfist | The party are now Custodi Eterni; he has named them so | Awarded post-siege |
| Maestro Varis "Seta-Argento" | Artemis is a buyer of Underdark relics; willing to broker | Three transactions to date |
| Salvatore "Sal" | The party are Custodi Eterni carrying major divine artifacts; knows their names, abilities, and routes | Briefed by Il Collezionista before deploying to desert road |
| Conte Valerius | The party visited Hammerfist; does NOT yet know about the Crown | Public dispatches |
| Druid Circle of the Sacred Forest | Hella is approaching for the ritual; reserves judgment | Hella's letter, sent two days ago |
| Capitana Lythiel Alar-Wen (Wood Elf Ranger 8, Sacred Forest scout, GS 8) | Hella is the druidess Saraah promised the Acorn of the Circle to | Direct recognition during Hammerfist Battle Sessione 4; canonized 2026-05-04 |
| Maestro Tempestas (Half-elf Bard 12/Arcmage 2, GS 14, Rethmar **intelligence agent** — NOT delivery service) | The party survived Lorana's city (Arco 00); they are Custodi Eterni; he carries **only one letter** (Brenna Sorvane → Thorik) on Day 21 + intel exchange mission; intercepted drow conversation 3 weeks ago about "il dottore della torre invisibile vuole il portatore dell'anello caotico" + "fine Mirtul, poi la torre cammina" — relevance recognized only when Artemis's Ring vibrates | Intercepted via accidental Shadow Walk side-emergence near Cannath Vale Nord (fiume con tre rapide); revised v2 2026-05-04 (Tempestas role narrowed to intel agent; he no longer delivers Tordek/Hella/Artemis personal hooks) |
| Sorella Maewen "Pugno-di-Cedro" (Mezza-elfa Monk 9/Cleric 2 of Ilmater, GS 10, monk-courier of Confraternita Monastica di Dauth) | Aeleth Verdebronzo is dead (will discover on arrival); Tordek matches the description of the 4th tournament invitee "Pugno di Pietra del Nord" (recognizable by Custode Eterno rune) | Travels Cannath Vale with 5 tournament invites; arrives Sacred Forest Day 24 looking for Aeleth; canonized 2026-05-04 |
| Lathander + Mask (divine, divinatory) | Artemis rejected the Lord of Sun and Shadow PrC at Belkram (Arco 04); the Ring he carries is Zalkatar's research instrument; Zalkatar is a 3-century-old ex-cleric of Mask who became Mind Flayer by choice; both deities OBSERVE without intervening unless Artemis explicitly requests post-Tower "courtesy" | Direct divine awareness; activates as dream visitation Notte 22-23 of post-Hammerfist; canonized 2026-05-04 |
| Brenna Sorvane (Consigliere militare Rethmar) | Hammerfist defeated Red Hand vanguard; Custodi Eterni include Thorik who is a battle-tested commander; Halveth is corrupt by Conte Valerius; Lorana is alive in Rethmar | Reports from Tempestas (her primary messenger); canonized 2026-05-04 via her sealed letter to Thorik |
| Therysol | Il Collezionista's guild has a hidden cell in Dauth | Captured guild operative interrogated |
| Tiri Kitor wild elves | Nothing yet — first contact pending Starsong Hill | — |

---

## 5. Open Promises, Debts, Bargains (PG ↔ World)

> Things the PCs are **on the hook for**. Agents must surface these when
> relevant; they create R.A. Salvatore-style internal stakes.

| Owed by | Owed to | What | Consequence if broken |
|---|---|---|---|
| Thorik | Re Thorek Hammerfist | Lead defense at Rethmar OR send Aegis Fang as proxy | Loss of Custode Eterno status; dwarven mercenaries withdraw |
| Thorik | Hella (implicit) | He sacrificed 2 perm CON for her resurrection — she owes a moral debt | Affects Hella's ethics rolls in arguments with Thorik |
| Tordek | Hella | 500 XP sacrificed for her resurrection | Affects romantic-bond progression at Sacred Forest |
| Tordek | Tournament organizers | Show up at Dauth within 5 in-world days | Disqualification; 150 mercenary reinforcements lost |
| Artemis | Varis "Seta-Argento" | Deliver one Underdark artifact per quarter | Varis cuts off the Mantello dei Tiri Salvezza supply |
| Artemis | Mask cult (suspected) | Unknown — they've been watching the Ring | Black-bag attempt during a vulnerable moment |
| Hella | Druid Circle | Pass the Sacred Forest ritual within 12 days | Circle will not aid at Rethmar |
| Party (collective) | Therysol | Help him strike Il Collezionista's Dauth cell | Therysol withdraws his combat support |

---

## 6. Artifact State (current powers, not theoretical max)

See `skills/rumblingstone-campaign/references/campaign-artifacts.md` for
full mechanics. This table is current truth only.

| Artifact | Holder | State | Currently usable powers |
|---|---|---|---|
| Aegis Fang | Thorik | Pre-full-awakening | +2 Returning Dwarven Waraxe; bonded |
| Corona di Adamantio | Thorik | All 3 gems lit | Stone's Awareness, +2 deflection AC, Topaz time-travel 1/month, Emerald earthquake 1/week, Ruby (single-use already spent at -1000 DR battle) |
| Ring of Chaotic Illumination | Artemis | Reforged at Eternal Forge | Full base powers; awaits further evolution at Invisible Tower |
| Bracieri Gemelli di Moradin | Tordek | Fire ✅ + Earth ✅ | Salto Infuocato 3/day, Fire Resist 10, DR 5/adamantine, Jump +10 |
| Collana dei Semi Eterni | Hella | Active post-resurrection | Treant summoning (limited), Avatar form (1/day), party gift slots (unspent: 3) |
| Cuore di Moradin | Crown set (altar) | Activated | Resurrection ritual catalyst — single-use, expended for Hella |
| Orbe delle Otto Porte (Githyanki artifact, campaign canon) | Tournament prize, not yet held | Awaits Tournament outcome | N/A until Tordek wins |

**Spent / single-use already burned:**

- Ruby gem of the Crown (used at year -1000 battle)
- Cuore di Moradin (used to resurrect Hella)

If any agent ever has a character "use" one of these again, that is a
coherence violation — flag to DM.

---

## 7. Open Narrative Threads (DM tracker)

Bullet list of unresolved questions. When a thread closes, move it to the
changelog with the resolution.

- Will the party defend the Hammerfist temple (Phase 0 of Rethmar) before or after personal quests?
- Will the party encounter Sal on the desert road (Day 28–32) and identify him before he plants his sabotage traps?
- If the party frees Sal's living statues, the nano di Hammerfist recognizes Sal as Vatore — will the party connect Sal's past to his present identity?
- Does Tordek's chakra enlightenment carry into the Battle of Rethmar?
- Does the Ghostlord become ally or enemy at Rethmar (depends on Sacred Forest outcome)?
- Conte Valerius — political defeat path vs. assassination path?
- Does Artemis confront the Mask cult before the Ring fully evolves?
- **[TORNEO ↔ TORRE]** Will the party unmask Sethrax (a.k.a. "Kethran Mano di Pietra") at Dauth before Day 3 Round 7? (If unmasked early or killed: Zalkatar's clock slows; if Sethrax escapes with the "Seme di Porta": Zalkatar gains +2 effective CR for Artemis's P2A finale)
- **[TORNEO]** Will Tordek interpret the "Eco delle Fenditure" vision and warn Artemis (or vice versa) of the Githyanki–Illithid–Illithid triangle around the Orbe?
- **[CONSIGLIO]** Will the party remove Halveth before Day 33 Seduta 2? (If not: +1 CR Phase 0, resa vote passes by Kaal's double vote)
- **[CONSIGLIO]** Can the party convince Lady Kaal with a credible military plan? (Diplomacy CD 22 + allied faction list required)
- **[LORANA]** Will the party reconnect with Lorana and use her field intel for Thorik's Rethmar defense plan? (-1 CR Phase 1 if yes)
- **[LORANA]** Will the party ask Lorana to mobilize the refugees as emergency reserve? (Moral cost — requires face-to-face before the request)
- **[HOOKS ↔ HELLA]** Will Hella plant Lythiel's Ghianda del Cerchio at the Cerchio della Quercia Vecchia during her ritual? Without it: ritual at default CDs and no second Druid Circle reinforcement at Rethmar Phase 1. With it: −4 CDs + reinforcement (3 druids + 6 minor Treants).
- **[HOOKS ↔ HELLA]** Will Hella accept Tempestas's Shadow Walk shortcut to the Sacred Forest on Day 22 (−1 to all rolls for first 12h + Tempestas mental erosion tick) or travel by foot/cavalry (3 days; 4 peripheral nodes of the Circle fall during transit, reducing Acorn rigenerazione by −1 Cos)?
- **[HOOKS ↔ TORDEK]** Does Tordek accept the official Dauth seal from Tempestas? Refusal cancels the political cover for the 150 King Thorek lances; they remain at Hammerfist; Wyrmlord Karruk gains +1 effective CR at Phase 1 of Rethmar.
- **[HOOKS ↔ ARTEMIS]** Does Artemis accept Tempestas's drow-camp map? Branches: early Tower (skip Beriah / Tournament sub-quest) / Dauth-then-Tower / split via Shadow Walk on Day 33. Each affects intel, sub-quest eligibility, and the "Tower walks" timing of Zalkatar.
- **[HOOKS ↔ THORIK]** Does Thorik accept Brenna Sorvane's letter and bring an alliance proposal to King Thorek? Determines Halveth's grip on the Rethmar Council, Lorana's reception of the party, and Phase 0 (Notte dei Drow) baseline difficulty.
- **[HOOKS ↔ TEMPESTAS]** Will the party invest in Tempestas as long-term ally (defending him from drow assassins, acknowledging the Lorana debt, supporting his mental erosion)? Affects whether the Polvere di Tonante 5-charge channel stays usable and whether he appears as flying caster ally at Rethmar Phase 1 (Cantata della Tempesta Tonante 1/incontro narrativo).

---

## 8. Changelog (append-only)

Every state change goes here with date and one-line reason. Never delete
entries — they become campaign history.

```
2026-05-01  Initial state.md created (extracted from campaign-story-arcs.md
            + post-Hammerfist arc notes). Baseline = end of Hammerfist battle,
            party at Hammerfist Holds, Custodi Eterni granted.
2026-05-02  Added Salvatore "Sal" della Luna d'Argento as active villain thread
            (clock 0/6). Added to NPC knowledge table and open narrative threads.
            Files: PNG/Salvatore/Salvatore.md,
            09_Continuazione.../Arco-Post-Hammerfist-P2C-Salvatore-Mercante-TESTO.md
2026-05-02  Full PNG audit: created dedicated character sheets for all major
            villains/NPCs previously missing from PNG/. Files created:
            PNG/Azarr_Kul/Azarr_Kul.md (GS 15, boss Rethmar Phase 3),
            PNG/Sonjak/Sonjak.md (GS 13, Drow Matrona; clarified = Matrona Sajak),
            PNG/Conte_Valerius/Conte_Valerius.md (GS 6 combat / GS 14 political),
            PNG/Varis_Seta_Argento/Varis_Seta_Argento.md (CR 6, urban broker),
            PNG/Ghostlord/Ghostlord.md (GS 13, Lich druidico Thornwaste),
            PNG/Xal_thor/Xal_thor.md (GS 14, Illithid Githyanki commander).
            NPC knowledge table and open threads updated accordingly.
2026-05-03  DM confirmation: the Orbe delle Otto Porte is established
            as a **Githyanki artifact** (campaign canon, RumblingStone —
            not SRD/RHoD). [INFERRED — needs DM confirmation] markers
            removed from OTTO-PORTE-e-ORBE §2.1.1/2.1.2/2.1.3 and PARTE1.
            Origin promoted to canon in
            skills/rumblingstone-campaign/references/campaign-artifacts.md
            and §5 of state.md. All downstream mechanics (Vaereth's claim,
            Sethrax's "seme di Porta" extraction, Githyanki clock-advance
            rule, Eco delle Fenditure vision) are now established
            campaign canon.
2026-05-03  Code-review fixes on the Tournament ↔ Torre integration:
            - Typos in PNG/Sethrax_il_Velato/Sethrax.md (article gender,
              "priorità alla ritirata").
            - Sethrax's *Psionic Dimension Door* aligned to **3/giorno**
              across PARTE2 (was inconsistently 1/giorno) — PNG card and
              STATBLOCCHI now agree.
            - Xal'thor's role and motivation clarified in PNG/Xal_thor,
              state.md, PARTE3, and OTTO-PORTE-e-ORBE: he commands an
              **Illithid** invasion (psionic thralls + a small core of
              dominated Githyanki), NOT the free Githyanki dragon-rider
              force (that's Vaereth — separate and hostile). His unique
              tournament target is the **Bracieri Gemelli** of Tordek;
              he is NOT interested in the Orbe (that's Sethrax/Zalkatar
              and Vaereth) — removes the duplicate-motivation issue.
            - All inferred lore flagged with [INFERRED — needs DM
              confirmation] per AGENTS.md policy: Orb's Githyanki origin
              (OTTO-PORTE §2.1.1), the "Eco delle Fenditure" vision and
              the clock-advance rule (PARTE1 + OTTO-PORTE §2.1.2/2.1.3).
            - Consolidation: Sethrax.md is now the authoritative source
              for unmask triggers, psionic power limits, and cross-arc
              outcome table; OTTO-PORTE-e-ORBE §2.1.3 is the authoritative
              source for the Githyanki clock-advance rule. PARTE1, PARTE2,
              PARTE3, MINIMAPPA, STATBLOCCHI voce 10 now point to those
              sources instead of duplicating mechanics.
2026-05-03  Tournament ↔ Torre Invisibile integration. Added:
            - "Visione Githyanki — Eco delle Fenditure" mechanic (Day 1
              first-Porta-opening cutscene foreshadowing Day 3 Vaereth arrival)
              in PARTE1-Giorno1-Preliminari.md.
            - Orb's Githyanki planar origin lore (it was a ki-psionic resonator
              for Githyanki dragon-riders) in OTTO-PORTE-e-ORBE.md §2.1.1.
            - New PNG: Sethrax il Velato (CR 12, Mind Flayer Psion 5,
              Zalkatar's emissary), infiltrated as masked finalist "Kethran
              Mano di Pietra". Files: PNG/Sethrax_il_Velato/Sethrax.md,
              statblock in STATBLOCCHI-COMPLETO.md voce 10, hooks in
              PARTE2-Giorno2-Semifinali.md (introduction + clues),
              PARTE3-Giorno3-Finale-e-Invasione.md (auto-unmask Round 7,
              triangle of factions), MINIMAPPA-TIMELINE-ALLEANZE.md.
            - Updated PNG/Xal_thor/Xal_thor.md with rival illithid faction
              section (two illithid conclaves do NOT collaborate at Dauth).
            - New villain clock: Sethrax (sync to Tournament).
            - New NPC knowledge rows (Zalkatar via Sethrax; Sethrax's
              own observations of Tordek + Orb).
            - New open narrative thread: cross-arc Tournament ↔ Torre
              Invisibile (Sethrax's fate determines Zalkatar's CR for
              Artemis's P2A finale).
2026-05-04  Post-Hammerfist hooks integration. Canonized two recurring NPCs
            and four PG-personal hook scenes that tie each PG's quest
            track into the Red Hand of Doom timeline (anchored to Azarr
            Kul Clock 9/18 and the Vanguard distaccamento Day 28→33).
            Files added (09_Continuazione.../):
            - HOOKS-INTEGRATION-MASTER.md (DM canonical schedule:
              Hammerfist → Day 22 4 letters → Day 23 split → Day 33
              double climax → Day 38 Rethmar; Sal explicitly NOT used
              as messenger to avoid leak to Sonjak)
            - HOOKS-Hella-SacredForest.md (Lythiel Day 19 Acorn drop +
              Tempestas Day 22 white ash + 3 travel choices)
            - HOOKS-Tordek-DauthInvitation.md (Tempestas delivers
              official Dauth Tournament seal from Magister Veylan +
              Sovrintendente Tordek; refusal cancels 150 lances)
            - HOOKS-Artemis-TorreInvisibile.md (Tempestas's leather
              map of Cannath Vale north + intercepted drow chatter
              about "il dottore della torre invisibile" wanting "il
              portatore dell'anello caotico"; deliberately avoids
              Day 3 overload — keeps Beriah/Mask cult only at Dauth)
            - HOOKS-Thorik-RethmarLetter.md (Brenna Sorvane's private
              sealed letter: 3-4 Council split, Halveth corrupt,
              Lorana alive, request for King Thorek alliance + 150
              lances + Thorik in person)
            New PNG cards:
            - PNG/Tempestas/Tempestas.md (canonized as the "bard
              storm caller" who helped the party escape Lorana's
              city in Arco 00; multi-arc messenger via Shadow Walk;
              GS 14; Cantata della Tempesta Tonante; mental erosion
              vulnerability; 5-charge Polvere di Tonante channel)
            - PNG/Lythiel/Lythiel.md (Wood Elf Ranger 8, Sacred
              Forest druidess-mancata, one of the 12 elven rangers
              on giant owls at Hammerfist Sessione 4 final phase;
              keeper of Saraah's Acorn for Hella; CR 8)
            New active companion entry in §1: Tempestas (recurring,
            not constant). New NPC knowledge rows in §3 (Lythiel,
            Tempestas, Brenna). New open narrative threads in §6:
            6 [HOOKS ↔ *] threads.
            Decision documented: Salvatore "Sal" is NOT used as
            tournament-invitation messenger because he is compromised
            (employed by Il Collezionista + Sonjak); Tempestas serves
            that role exclusively.
2026-05-04  Hooks integration v2 — major refactor of motivation
            and delivery (per DM critique: "why would Tempestas
            deliver letters that aren't his job?"). Changes:
            - Tempestas's mission narrowed: he is an INTELLIGENCE
              AGENT for Rethmar (Brenna Sorvane), not a delivery
              service. Carries ONLY one letter (Brenna → Thorik).
              Primary mission at Hammerfist: honor the dead +
              gather Red Hand intel from Thorik (bidirectional
              exchange: he offers Halveth corruption + Lorana alive
              in return). The drow chatter intel (intercepted 3
              weeks ago in Shadow Walk, Cannath Vale Nord) is
              MAINTAINED but reframed as material confirmation
              for Artemis's Ring vibration, surfaced only when
              Artemis asks OR when Tempestas notes the Ring glow
              at the cena di Hammerfist (Sapienza Magica CD 14).
            - Tordek hook RELOCATED: invitation no longer comes
              from Tempestas at Hammerfist. Comes from new NPC
              Sorella Maewen "Pugno-di-Cedro" (Mezza-elfa Monk 9/
              Cleric 2 of Ilmater, GS 10) — Confraternita
              Monastica di Dauth courier who arrives at Sacred
              Forest Day 24 looking for Aeleth Verdebronzo (dead),
              recognizes Tordek by Custode Eterno rune as the
              4th invitee on her list. Tournament reframed as
              MYTHIC: once every 100 years at Iride star
              alignment, 4 days notice, open to all valorous
              warriors who pass monastic preliminaries (non-
              monks at disadvantage with documented CD modifiers).
              Files: PNG/Maewen/Maewen.md (full PNG card with
              5-invitee list as worldbuilding datapoints).
            - Artemis hook fully INTERNAL: Ring of Chaotic
              Illumination vibrates during Cerimonia delle 100
              Asce Atto 3 (Re Thorek hands runa di pietra). Voice
              "Lui sta camminando. Vieni." in drow antico. Plus
              new SOGNO DELLA DOPPIA MASCHERA Notte 22-23: both
              Lathander and Mask appear in dream with insight on
              Zalkatar (3-century ex-cleric of Mask, became Mind
              Flayer by choice, wants to READ Artemis not kill
              him). Mechanical bonus: +2 TS Vol vs Zalkatar
              psionics; +1d6 first attack each round Phase 3 of
              Tower fight (+2d6 if Atto 2 sub-quest done).
              Tempestas drow chatter MAINTAINED as material
              confirmation. Saraah druidic divination at Sacred
              Forest is third optional confirmation.
            - Hella hook EXTENDED: Lythiel Acorn at Cerimonia
              (canon, kept) + Saraah's RITO DI DIVINAZIONE Day 25
              at Sacred Forest revealing 3 visions (Red Hand base
              at Rhest with Wyrmlord/black dragon; dark shadow
              under the Quercia Vecchia = Mother of Fungi spore
              by Sonjak's drow; Talar in fiamme = already
              destroyed). Optional Mother of Fungi descent
              encounter EL 11. Bonus narrative: Sacred Forest
              ritual base bonus DOUBLES if MoF purified.
            - NEW: HOOKS-Ghostlord-Refugees.md — refugee caravan
              from Loccatella (fled Lich's undead waves out of
              Thornwaste) heads to Talar not knowing it's been
              sacked. 4 PG-party choices (escort to safe city /
              investigate Thornwaste = early Ghostlord arc /
              partial aid / ignore). Echoes: +30 to Lorana's
              Riserva at Rethmar; possible Joran ex-druid CR 5
              ally; Tobi child as RP callback.
            - Master Integration v2: 3 architectures (PATH-A
              split / PATH-B together-sequential / PATH-C hybrid)
              with explicit costs. No railroad. Cerimonia delle
              100 Asce becomes the canonical landing zone for
              Hella + Thorik + Artemis hooks (3 of 4); Tordek's
              landing zone is Sacred Forest.
            - Cerimonia delle 100 Asce canonized as Day 21 closing
              event of Arc 08, file in 08_La Battaglia Di
              Hammerfist/Cerimonia-delle-100-Asce.md (210 dead
              honored with 100 ceremonial axes; party formally
              recognized as Custodi Eterni with rune di pietra).
            New NPC knowledge rows in §3: Maewen, Lathander+Mask
            divine awareness. Tempestas row revised. New PNG
            cards: PNG/Maewen/Maewen.md.
2026-05-05  Army sync v2 — DM realignment: horde baseline rescaled from
            6.161 (AP-original) to ~10.000 (coherent with scaled Channath
            Vale cities); ratio target 3:1-like from Hammerfist (900/300)
            up to max 6:1 worst case / 1.55:1 legendary; PG choices now
            meaningfully shift balance. Introduced DUAL CLOCK separation:
              - MARCH CLOCK (official AP): Day 1 → Day 40 Rethmar
                encampment. Current sync point: **Day 19 = Terrelton
                falls = end of Battle of Hammerfist**.
              - RITUAL CLOCK AZARR KUL: /18 independent (rituals only,
                does NOT advance with march).
            Dragon contingent set at 5 AP-original upscaled: Abithriax
            (Red adult), Regiarix (Black young — Rhest), Ozyrrandion
            (Blue — Tower), Tyrgarun (reserve), Fauci di Palude (Black
            adult, Hammerfist vanguard). Draconic spawn = 8 Razorfiend
            (Tiamat colors) assigned to Wyrmlord villains upscaled.
            NEW: "Compagnia del Teschio Nero" — 650 evil human
            mercenaries (Thay/Mulhorand) joining for power/money.
            Gnoll mercenaries expanded to 1.100 (3 tribes).
            Ghostlord logic: if neutralized by PG → only 400 undead
            already pre-deployed remain; default hostile → +2.400
            undead wave at Rethmar Phase 2.
            No PG interference at Skull Gorge bridge (confirmed). No
            giant alliance PG-side (giants stay with Red Hand).
            Files created/replaced:
            - 00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md
              (rescaled 10k + dragons + Razorfiend + Teschio Nero +
              conditional additives table)
            - 00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md
              (AP March Clock Day 1→40 waypoint ledger)
            - 09_Continuazione.../Arco-Post-Hammerfist-P3-BATTAGLIA-
              FINALE-ARMATE-SYNC.md (5 PG scenarios, force balance)
            §2 Active Forces tracker replaced with dual-clock version.
2026-05-05  Added §2 Active Forces — Live Army Tracker to state.md as the
            session-by-session source of truth for force sizes. Created:
            - 00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md:
              full initial composition (6,161 total), deployment table
              (Hammerfist 793/Dauth 575), dynamic march attrition by week,
              defender coalition scenarios, Dauth multi-faction breakdown.
            - 00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md:
              battle log waypoint-by-waypoint (Nimon Gap ✅ → Drellin ✅ →
              Skull Gorge 🔄 → Talar/Terrelton/Witchcross ⏳), refugee flow
              table (~5.300 civili + ~495 armati verso Rethmar), cumulative
              loss table per scenario (3.783–5.053 MR a Rethmar), session
              checklist, infiltrati nell'onda rifugiati.
            - 00_Red Hand Of Doom/Armate-AGGIORNATO.ods: now 9 sheets
              (aggiunti Registro Battaglie, Rifugiati Rethmar, Tracker
              Dinamico). Forza garantita Rethmar aggiornata a 1.746
              (include rifugiati armati da Nimon+Drellin già arrivati).
            Current confirmed losses MR: −308 (Days 1-9, Nimon+Drellin
            +attrition). Main body: 4.793 → 4.485 active.
2026-05-05  Created DM-CAMPAIGN-PLAYBOOK.md (operational DM guide):
            pre/during/post-session workflow with 2 worked examples
            (session file + state.md diff), dual-clock quick reference,
            reset procedure for new groups (branch-per-group strategy),
            red flags. Added §0 Campaign Status At-a-Glance dashboard
            to state.md. Created templates (state-blank.md,
            session-template.md) and helper script
            scripts/new-campaign-group.sh for one-command group reset.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 1 (A1+A13): global
            spelling fixes, no canon change. "Regiarax" → "Regiarix"
            (D1) across campaign/, skills/, PNG/, 09_Continuazione/.
            "Rethman" → "Rethmar" (D2) across all P3 files; renamed
            Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAN-STRUTTURA.md
            → ...-RETHMAR-STRUTTURA.md and updated all references.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 2 (A2+A10): clock
            coherence, no canon change (D6 already won via state.md §2,
            propagated to files that still disagreed). "Day 38/40"
            arrival-of-horde references → Day 42 in HOOKS-INTEGRATION-
            MASTER §1.1/§6.1, P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA r.12,
            ARMATE-SYNC §1/§2/§4-Fase1, Armate-SINCRONIZZAZIONE-CAMPAGNA
            §4b (Fase 1-3 all land on Day 42 per D13's compressed 3-day
            rhythm), DM-QUICKSTART-ARC09. A10: ESITI-CONSEGUENZE §6
            reworded ("costruire un Fane" → "rifortifica il Fane nel
            Shaar + avamposto avanzato", since the Fane already exists
            per §2.1 Day 1). §3 Azarr Kul row relabeled as the Ritual
            Clock (was ambiguously worded as a march countdown) with
            explicit advance triggers cross-referenced to Armate-
            SINCRONIZZAZIONE-CAMPAGNA §4b.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 3 (A3+A5+A11):
            INDICE-GENERALE refresh, no canon change (all values already
            correct in state.md, only INDICE was stale). A3: Torre/Rhest/
            Torneo durata windows updated to match state.md §0 (Day
            28-35 / 25-32 / 25-34), citing HOOKS-INTEGRATION-MASTER §1.1
            for detailed chronology. A5: Ghostlord numbers in INDICE and
            Ghostlord-LICH-ALLEANZA-TESTO §6 updated to D7 (+2,400
            ostile / +400 neutralizzato / +600 pro-difensori se redento).
            A11: INDICE "Finale improvviso" del Torneo riscritto per
            separare le due fazioni Day-3 fuse per errore (Xal'thor
            Illithid vs Vaereth Githyanki, D5), aggiunto lo smascheramento
            di Sethrax al Round 7.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 4 (A4+A12): no canon
            change. A4: ESITI-CONSEGUENZE §7 usava nomi di PG (Tordek,
            Artemis) come PNG — artefatto di generazione. Sostituiti con
            Sellyria Starsinger/Killiar Arrowswift (leader Tiri-Kitor,
            già canonici in Starsong-TESTO), Magister Veylan [INFERRED]
            (Dauth) e Borin Tozzefort [INFERRED] (comandante 300 nani
            mercenari), incluso il monologo "Vittoria Tattica" che citava
            "Artemis Learmount" come parlante. Corretti anche i refusi
            della sezione (gloriosa-mente, nega-zia, complètamente, lo
            prezzo, stravagato). A12: banner DEPRECATED aggiunto a
            inizio.md e Quest 1 – Druida Hellas (brainstorm storico
            pre-canone, code conversazionali AI rimosse), INDICE li
            etichetta "storico/deprecato".
```
