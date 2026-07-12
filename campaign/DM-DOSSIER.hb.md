<!-- Auto-generated — do not edit by hand.
     Sorgente: campaign/state.md (fonte di verità — il dossier ESTRAE, non riscrive)
     Rigenera con: python3 scripts/dm.py dossier
     ⚠️ MATERIALE DM: clock e piani IN CHIARO. Mai ai giocatori. -->

{{frontCover}}

{{logo ![](/assets/naturalCritLogoRed.svg)}}

# RUMBLING STONE
## Dossier del Dungeon Master
___

### Tutti i fili della campagna, in un colpo d'occhio

{{banner ⚠️ SOLO DM}}

{{footnote
  Generato il 2026-07-12 · Mirtul, 1372 DR · 19 Mirtul (Giorno 19 della Marcia) · fonte: campaign/state.md · Red Hand of Doom, Faerûn 1372 DR
}}

\page

# Il quadro della guerra

{{descriptive
*La Valle brucia a sud e le Dale trattengono il fiato. Questo è il punto esatto in cui la storia è arrivata — e ciò che ancora attende, riga per riga, senza veli.*
}}

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
| 07 Portale della Forgia Eterna | 🟡 | **in corso** | — | 13 (D8) | Giocati: Forgia (P1-P2), Piano del Fuoco/Topazio (P3), viaggio spirituale Hella+Durik (P3B-spirito); **in corso: Piano della Terra (P4)** |
| 07 P3B Resurrezione di Hella + P5 Viaggio 1.000 anni | ⬜ | da giocare | — | 13 | Si gioca DOPO la Terra (ARC-07 D2); raccordo D16 (Rubino) riporta i PG al 1372, Cuore della Montagna → ARC-08 |
| 08 Battaglia di Hammerfist | ⬜ | **pianificato — canone preparato, NON giocato** | **Day 19 (target sync)** | 13 (consolida, D9) | Esito atteso: vittoria, Cerimonia 100 Asce, Custodi Eterni (piano ARC-08 §0, E1-E8) |
| 09 P1A Quest Hellas (Cerchio Sacro) | ⬜ | **preparato in anticipo** | Day 20-30 window | 13 | Deadline Day 30 |
| 09 P1B Cerchio Treant | ⬜ | **preparato in anticipo** | Day 22-28 | 13 | — |
| 09 P1C Rituale Hellas | ⬜ | **preparato in anticipo** | Day 25-30 | 13 | — |
| 09 P2 Rhest (Saarvith + Regiarix) | ⬜ | **preparato in anticipo** | Day 25-32 | 13 | -1 drago se fatto |
| 09 P2A Torre Invisibile (Zalkatar) | ⬜ | **preparato in anticipo** | Day 28-35 | 13 | -1 drago se fatto |
| 09 P2B Torneo di Dauth (Tordek) | ⬜ | **preparato in anticipo** | Day 25-34 | 13 | +300 mercenari nani |
| 09 P2C Salvatore Mercante | ⬜ | **preparato in anticipo** | Day 28-36 | 13 | Sal clock 0/6 |
| 09 P3 Starsong Hill (Tiri-Kitor) | ⬜ | **preparato in anticipo** | Day 30-35 | 13-14 | +cavalleria civette |
| 09 P3 Ghostlord | ⬜ | **preparato in anticipo** | Day 25-32 | 13-14 | 3 branch: ostile/neutralizzato/alleato |
| 09 P3 Sabotaggio Campi Drow | ⬜ | **preparato in anticipo** | Day 30-36 | 13-14 | -Fase 0 + -75 esperimenti fungini (45 Servitori + 30 Sporeborn; 8 Guardiani Neri sopravvivono) |
| 09 P3 Missioni Brevi CR12 | ⬜ | **preparato in anticipo** | Day 30-38 | 13-14 | — |
| **09 P3 Battaglia Finale Rethmar** | ⬜ | **preparato in anticipo** | **Day 42** | 14 | Fase 0-4 |

**Legenda**: ✅ completato · 🟡 in corso / imminente · ⬜ non iniziato · ❌ fallito · ⏸ sospeso

---

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# Gli eserciti in movimento

{{descriptive
*Diecimila stendardi rossi marciano al ritmo dei tamburi hobgoblin. Ogni giorno che passa è un villaggio in meno e una decisione in più. I due orologi qui sotto non si fermano mai.*
}}

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
| **Dragons (5 AP-original upscaled)** | 5 | Abithriax (Red adult) / Regiarix (Black young, Rhest) / Ozyrrandion (Blue, Tower) / **Tyrgarun (Blue Old, CR 18 — sky-terror of the battle, NOT Azarr Kul's mount, D11 v2)** / **Fauci di Palude** (Black adult, Hammerfist vanguard — **conditional branch, D10, not yet resolved**: default = flees gravely wounded, may return later as a narrative hook, not guaranteed at Rethmar; PG-kill branch = dies at Hammerfist, −1 dragon, see §2.3) |
| **Draconic spawn = Razorfiend (Tiamat colors)** | 8 | Assigned to Wyrmlord villains upscaled |
| Compagnia Drow di Sonjak | 305 | |
| Githyanki di Vaereth | 375 | |
| Gnoll mercenari (3 tribù: Flinderoso, Abbattitori, Artigli Neri) | 1,100 | |
| Loxo + Centauri corrotti (Shaar) | 480 | ❓ Revolt possible |
| **Compagnia del Teschio Nero** (umani malvagi mercenari, Thay/Mulhorand) | 650 | NEW 2026-05-05 |
| **BASELINE TOTAL** | **~9,900** | ≈ 10,000 ✓ |

**Post-Hammerfist losses (Day 19 sync, default victory scenario — piano
ARC-08 D11):** **−900** total (900-strong Hammerfist vanguard: ~500
morti + ~400 dispersi in rotta; i dispersi NON si ricongiungono
all'orda principale). Same figure as
`00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §3 Day 19 row
and `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md` §Day 19 —
one total propagated everywhere (D11). Current active: **~9,000**.
Other outcome branches (costly victory, defeat) live in piano ARC-08
B1 (not yet written), not in this tracker.

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
| PG kill Fauci di Palude at Hammerfist (D10 alternate branch, before he flees under 50 hp) | −1 dragon (removed from Rethmar pool entirely) |
| Fauci di Palude flees under 50 hp (D10 **default** branch — Hammerfist Schede §1 Tattiche) | No change to horde total; he is simply absent from Rethmar unless a later narrative hook brings him back (piano ARC-08 C2/EVENT-DECK, not yet written) |

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
| **Alleanza Elfi Starsong Hill** | +120 (100 ranger + 20 gufi giganti) | SOLO se P3-Starsong quest OK (D9 — tribù Tiri Kitor ~500 anime, invia 1/5 come forza da guerra) |
| **Nani di Dauth** (torneo vinto) | +300 | SOLO se Tordek vince torneo |
| **Lance di Re Thorek** | +150 | Flusso separato, condizionato da hook politici (sigillo Maewen + lettera Thorik) — max combinato con la riga sopra: **450** (D10) |
| **Druidi Cerchio Sacro + Treant Hella** | +150 | SOLO se P1B Hella ritual OK |
| **Ghostlord redento come alleato** | +600 non-morti buoni | Branch raro |
| Mercenari Salvatore (rischio tradimento) | ±300 | Instabile |

**Nota D13 (piano ARC-08 A11)**: il Capitano Lunapiena e i suoi 12
Ranger Elfici (Hammerfist Arc-08) sono una compagnia **indipendente**
dell'Elsir Vale — **NON** contano in questa tabella, restano di
presidio a Hammerfist. Da non confondere con l'Alleanza Elfi Starsong
Hill (Tiri Kitor, riga sopra) né con Lythiel Alar-Wen (Sacred Forest,
§4).

**Scenari finali (target: PG meaningfully shift balance):** questa tabella
è la vista rapida legacy; per lo scenario **autoritativo e ricalcolato**
sui nuovi totali D9/D10, vedi
`09_Continuazione.../Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md`
§3 (5 scenari worst/baseline/medio/ottimale/leggendario, Orda e
Difensori con la stessa metodologia dual-clock di §2 qui sopra).

| Scenario PG | Horde | Difensori | Rapporto |
|---|---|---|---|
| Worst (Ghostlord ostile, Xal'thor allea, 0 quest) | 12,700 | 2,200 | **5.8:1** ☠ |
| Baseline (0 quest) | 9,400 | 2,200 | **4.3:1** |
| Medio (2–3 quest + sabotaggi parziali) | 8,000 | 2,620 | **3.1:1** |
| Ottimale (tutte quest + Rhest + Tower) | 6,800 | 3,770 | **1.80:1** |
| Leggendario (ottimale + Ghostlord redento + Collezionista stop) | 6,400 | 4,370 | **1.46:1** |

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
| Hammerfist Holds | ✅ Held (+90 survivors; 150 lances conditional) | 0 civilians | +150 ❓ if political hooks land (Maewen seal + Thorik letter, D10 — separate from the 300 tournament mercenaries) |
| Cannathgate | ✅ Not attacked | 0 | +150 ❓ diplomacy |

---

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# Le mani nell'ombra

{{descriptive
*Mentre i Custodi guardano avanti, altri guardano loro. Questi sono i conti alla rovescia dei nemici: quando uno arriva a fondo scala, il mondo cambia — che i PG se ne accorgano o no.*
}}

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

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# Chi sa cosa

{{descriptive
*In Faerûn i segreti pesano più dell'oro. Questa è la contabilità di ciò che ogni PNG sa, sospetta o giura di non aver mai sentito.*
}}

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

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# Promesse, debiti e patti

{{descriptive
*Le parole date hanno radici lunghe. Qui sono elencate tutte: quelle dei PG al mondo, e quelle del mondo ai PG. Nessuna scade in silenzio.*
}}

> Things the PCs are **on the hook for**. Agents must surface these when
> relevant; they create R.A. Salvatore-style internal stakes.

| Owed by | Owed to | What | Consequence if broken |
|---|---|---|---|
| Thorik | Re Thorek Hammerfist | Lead defense at Rethmar OR send Aegis Fang as proxy | Loss of Custode Eterno status; dwarven mercenaries withdraw |
| Thorik | Hella (implicit) | He sacrificed 2 perm CON for her resurrection — she owes a moral debt | Affects Hella's ethics rolls in arguments with Thorik |
| Tordek | Hella | 500 XP sacrificed for her resurrection | Affects romantic-bond progression at Sacred Forest |
| Tordek | Tournament organizers | Show up at Dauth by **Day 29** (eve of the preliminaries — invite Day 24, arrival Day 28, Tournament Day 1-3 = Day 30-32, HOOKS-INTEGRATION-MASTER §1.1) | Disqualification; 150 Lance di Re Thorek reinforcements lost (D10 — separate from the 300 mercenaries won at the Tournament itself) |
| Artemis | Varis "Seta-Argento" | Deliver one Underdark artifact per quarter | Varis cuts off the Mantello dei Tiri Salvezza supply |
| Artemis | Mask cult (suspected) | Unknown — they've been watching the Ring | Black-bag attempt during a vulnerable moment |
| Hella | Druid Circle | Pass the Sacred Forest ritual within 12 days | Circle will not aid at Rethmar |
| Party (collective) | Therysol | Help him strike Il Collezionista's Dauth cell | Therysol withdraws his combat support |

---

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# Il respiro degli artefatti

{{descriptive
*Corona, martello, anello, collana, bracieri: oggetti che ricordano. Questo è il loro stato REALE oggi — poteri accesi, non promesse.*
}}

See `skills/rumblingstone-campaign/references/campaign-artifacts.md` for
full mechanics.

> **Two-times table (T6c, DM-confirmed 2026-07-04)**: the two state columns
> are labelled. **«Today at the table»** = the real table position per §0
> (ARC-07 P4 in progress, canon D8/D16). **«Prepared (ARC-09 entry)»** = the
> forward-written state that becomes true only after P4 → P3B → P5 are
> played. For tonight's session ALWAYS use the "Today" column.

| Artifact | Holder | **Today at the table (ARC-07 P4)** | **Prepared (ARC-09 entry)** |
|---|---|---|---|
| Aegis Fang | Thorik | Pre-full-awakening: +2 Returning Dwarven Waraxe; bonded | Unchanged until the Siege (P5) is won → then Stage 1 full awakening (see Aegis master) |
| Corona di Adamantio | Thorik | **Only Topaz lit** (D8/D16): Stone's Awareness (incl. traps + comprehend languages, DM 2026-07-04), +2 deflection AC, Topaz time-travel 1/month (activation: 1 hour) | All 3 gems lit: + Emerald earthquake 1/week; Ruby single-use SPENT at the ancient battle (≈372 DR) |
| Ring of Chaotic Illumination | Artemis | Reforged at Eternal Forge: full base powers | Unchanged; awaits further evolution at Invisible Tower |
| Bracieri Gemelli di Moradin | Tordek | Fire ✅ + Earth ✅: Salto Infuocato 3/day, Fire Resist 10, DR 5/adamantine, Jump +10; Benedizione della Forgia active (4 charges/day — permanent for the whole campaign, DM 2026-07-04) | Unchanged |
| Cintura della Devastazione (custom PG, D17) | Tordek | Active — Devastation Gauntlets (MIC) moved to **belt slot** so wrists stay free for the Bracieri; ~3/day devastation charges (+2d6). Sheet: `PG/Artefatti/Artefatti-Pg/Tordek/00_Cintura_della_Devastazione.md`. Exact values → ARC-07 B5 | Unchanged |
| Collana dei Semi Eterni | Hella (dead — resurrection pending) | Forged, awaiting the P3B ritual; Hella not yet resurrected | Active post-resurrection: Treant summoning (limited), Avatar form (1/day), party gift slots (unspent: 3) |
| Cuore di Moradin | Crown set (altar) | Intact — will be expended as catalyst in the P3B ritual | SPENT: single-use expended to resurrect Hella |
| Orbe delle Otto Porte (Githyanki artifact, campaign canon) | Tournament prize, not yet held | Not in play | Awaits Tournament outcome — N/A until Tordek wins |

**Spent / single-use already burned** *(per column: Ruby & Cuore are spent
only in the "Prepared" time; at today's table the Cuore is still intact)*:

- Ruby gem of the Crown (used at the battle 1,000 years before, ≈372 DR) —
  spent in both times (the battle is in the past either way once P5 is played)
- Cuore di Moradin (used to resurrect Hella) — **Prepared column only**

If any agent ever has a character "use" one of these again in a time where
they are spent, that is a coherence violation — flag to DM.

---

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}

\page

# I fili aperti del racconto

{{descriptive
*Ogni filo lasciato libero prima o poi si tende. Questa è la tela completa: trame maggiori, sotto-trame, echi in attesa di riemergere.*
}}

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

{{pageNumber,auto}}
{{footnote DOSSIER DEL DM · SOLO DM}}


{{descriptive
##### Come si usa
Rigenera questo dossier dopo ogni sessione (`dm.py post`, poi `dm.py dossier`): è la fotografia di `state.md` — se una riga qui è sbagliata, correggi il canone in state.md, mai questo file. Le prossime scene dell'arco in corso sono nel QUICKSTART di `ARC07-00-INDICE.md`.
}}
