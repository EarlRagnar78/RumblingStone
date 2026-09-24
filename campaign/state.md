# Campaign State — Living World Snapshot

> **Purpose**: single source of truth for what is *currently* true in the
> RumblingStone world. Updated at the end of every session. Agents and the DM
> consult this file *first* before describing NPC knowledge, location of
> villains, status of artifacts, or open narrative threads.
>
> **Rule**: if this file disagrees with `campaign-chronicle.md` or any
> `campaign-*.md` reference, **this file wins** (it is the most recent truth).
> If you change a fact here, do not silently rewrite the history files —
> append a new entry to the changelog at the bottom.

---

**Last updated:** 2026-05-01 (session marker — DM updates)
**In-world date:** Flamerule, 1372 DR (piena estate — Valle di Channath; Giorno di Marcia 19 = 19 Flamerule)
**Party APL:** 13 (ARC-07 D8 — livello reale già raggiunto durante l'Arco 07)
**Sessions completed:** Arco 07 **in corso** al tavolo — giocati: Sala
della Forgia Eterna (P1-P2), Piano del Fuoco con Topazio recuperato (P3),
viaggio spirituale di Hella nell'Incudine del Mondo con Durik (P3B-spirito,
registrato); **✅ Piano della Terra (P4) COMPLETATO al tavolo 2026-07-31**:
Terros l'Antico sconfitto, **Smeraldo della Forza forgiato nella Corona**
(rito: **Thorik ha accettato il Peso nel corpo** — −2 DES/+2 COS permanenti, il portatore paga il pegno;
bottino dell'arco **intatto**), Seme-Mercato di Varis
**preso ma mai toccato**; party rientrato nella Sala e **riposato lì**
(orologio Hammerfist a **3g 16h**). **Prossimo: resurrezione di Hella (P3B).**
Restano da giocare: resurrezione fisica di Hella (P3B), viaggio ai
1.000 anni fa (P5), raccordo al 1372 (D16) — **poi** l'Arco 08 (Battaglia
di Hammerfist). **Tutto ciò che questo file dice dell'Arco 08 e
dell'Arco 09 è canone preparato (design), non ancora giocato al tavolo**
(corretto 2026-07-02, piano ARC-08 A0 — vedi changelog).

> **DM workflow**: per la procedura di aggiornamento fine-sessione e per
> far partire un nuovo gruppo senza perdere niente, vedi
> [`campaign/DM-CAMPAIGN-PLAYBOOK.md`](DM-CAMPAIGN-PLAYBOOK.md).

---

## §0 Campaign Status At-a-Glance

Cruscotto sintetico. Aggiornato a fine sessione. Vedi sezioni successive per dettaglio.

<!-- gen:state:archi -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

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
<!-- /gen:state:archi -->

**Legenda**: ✅ completato · 🟡 in corso / imminente · ⬜ non iniziato · ❌ fallito · ⏸ sospeso

---

## 1. Party — Current Position & Condition

> 🕐 **Questa sezione ha due tempi, e fino al 2026-09-12 li mescolava.** La
> regola dell'intestazione — *«tutto ciò che questo file dice dell'Arco 08 e
> dell'Arco 09 è canone preparato, non ancora giocato»* — vale anche qui, e
> qui non era applicata: la tabella collocava i quattro PG **dopo** la
> Battaglia di Hammerfist e in viaggio verso le quest dell'Arco 09, mentre
> §0 marca l'Arco 08 `⬜ NON giocato` e l'Arco 07 `🟡 in corso`. Le due
> colonne separano quel che è vero **adesso al tavolo** da quel che è
> **previsto** dal canone preparato. Nessun contenuto è stato cancellato:
> è stato etichettato *(lotto 4c, D3 — DM 2026-09-11)*.

<!-- gen:state:party -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| PC | Class | Stato | 🟢 Dov'è **adesso** (tavolo, ARC-07 P4 chiuso) | 🔵 Dove lo porta il canone **preparato** (post ARC-08) | HP / status **oggi** | Open personal threads |
|---|---|---|---|---|---|---|
| Thorik | Dwarf Fighter 13 | 🔴 attivo | Sala della Forgia Eterna, dopo il riposo (orologio Hammerfist **3g 16h**) | Hammerfist Holds, war council chamber | Full. **−4 DES / +2 COS / +4 CAR permanenti**, e sono tutto quel che ha pagato: −2 DES dalla Corona quando l'ha indossata, −2 DES / +2 COS / +4 CAR dal rito dello Smeraldo del 2026-07-31 (è il **portatore** ad aver accettato il Peso del Mondo). Ricalcolare CA senz'armatura, Riflessi, iniziativa. ⚠️ **Nessun −2 COS.** Il costo della resurrezione è **non ancora versato**: la scena (`ARC07-DEF-3` §5) non è stata giocata. Quando la giocherà, dona il **+2 di deflessione della Corona** e resta a **−1 CA permanente** — e ogni volta che Hella userà lo **Scudo del Custode**, lui sarà **accelerato 3 round verso chi lei ha protetto**. Può anche **rifiutare**: allora Aegis Fang (Ego 14) lo **giudica** finché non rischia qualcosa di suo per lei | Decide whether to lead defense of Rethmar personally vs. delegate |
| Tordek | Dwarf Fighter 4 / Monk 9 | 🔴 attivo | Sala della Forgia Eterna, dopo il riposo | → Torneo di Dauth | Full; Bracieri Earth phase complete. ✅ **Nessun malus permanente dal rito**: il Peso del Mondo l'ha accettato **Thorik**, il portatore (correzione DM 2026-08-06 — fino a quella data il pegno era attribuito a Tordek per errore). CA senz'armatura, Riflessi, iniziativa e Raffica restano quelli di prima. ⚠️ Il costo della resurrezione è **non ancora versato**, e 🔎 **non sono più i «−500 PE»**: in v4-bis dona **Ancoraggio della Montagna** (2/g), che **lascia i Bracieri per sempre** → Hella ottiene **RD 3/adamantino**. Se rifiuta, i Bracieri **tacciono una settimana** | Tournament of the Eight Gates (3 days, interrupted by Githyanki Day 3) |
| Hella | Dream Dwarf Ranger 1 / Druid 12 | ⚫ morto *(reversibile)* | 🔴 **morta**, corpo nella Sala, semi innestati — la resurrezione (P3B / `ARC07-DEF-3`) è **il prossimo beat da giocare** | Hammerfist → Foresta Sacra, template Ibrido Treant attivo, PG a pieno titolo | n/d finché non torna. Il template Ibrido Treant e i tre Doni **si assegnano al rito**, non prima | Sacred Forest ritual (pass = druid circle ally at Rethmar) |
| Artemis | Human Warlock 13 | 🔴 attivo | Sala della Forgia Eterna, dopo il riposo | → Torre Invisibile (regione di Dauth) | Full; Ring of Chaotic Illumination active, **Eldritch Blast 7d6**. ⚠️ Il costo del rito è **non ancora versato**: dona **1d6 di Eldritch Blast** (7d6 → **6d6**, per sempre) → Hella ottiene **il Rovo Eldritch**, a volontà. Se rifiuta, l'Anello **si spegne 24 ore** | Confront Zalkatar (CR 13 illithid warlock); Ring evolution at stake |
<!-- /gen:state:party -->

**Active companions:**

- **Durik** — Hella's animal companion (male dog, **reforged** into a Stone
  Guardian and evoked via the **3rd seed of the Collana dei Semi Eterni**);
  DR 5/adamantine, Tremorsense, telepathic link within 18 m. (The "rhinoceros"
  seen in play is **Hella herself using the Druid's Wild Shape** to become a
  **living rhinoceros** — NOT a stone/animated creature and NOT a separate
  companion. The earlier "stone rhinoceros, DR 5/adamantine, animated" label
  was a mix-up with Durik. DM clarified 2026-07-03.)
- Therysol (Tiefling Half-Dragon NPC, traveling separately, hunting Il Collezionista's guild)
- **Maestro Tempestas** (Half-elf Bard 12/Arcmage 2, GS 14, recurring messenger of Rethmar; canonized 2026-05-04 as the "bard storm caller" who helped the party escape Lorana's city in Arc 00 — vedi `Bestiario/png/Tempestas/Tempestas.md`). Not constantly present; drops in via *Shadow Walk* every 1–2 sessions with intel.
- **Lirien Amaranti** — «Il Giullare Spezzato» (Mezzelfo CN, Ladro-Scout 4/
  Bardo 1, GS 4; canonizzato 2026-07-20 — vedi `Bestiario/png/Lirien/Lirien.md`).
  NON viaggia col party: PNG ricorrente urbano (Rethmar, quartiere basso —
  mulino dei bambini di giorno, «Ponte Nuovo» di Kellin la sera), max ~1
  scena/sessione urbana col dado dello scompiglio.

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

<!-- gen:state:waypoints -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

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
<!-- /gen:state:waypoints -->

<!-- gen:state:march_clock -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

**Current March Day:** **19**
**Days remaining to Rethmar:** **23** (PG-quest window = Arc 09, Days 20-41)
<!-- /gen:state:march_clock -->

🔵 **Il Giorno 19 è il punto di sincronia previsto, non un giorno già
trascorso.** Terrelton cadrà mentre la Battaglia di Hammerfist si chiude, e la
Battaglia **non è stata giocata**. Il Giorno 19 non è «dove siamo»: è **dove il
calendario tornerà**, perché i PG viaggiano indietro nel tempo nel P5 e
riemergono al Cuore della Montagna al Giorno 3 dell'orologio interno, che è il
March Clock Day 18-19 (`ARC08-00-INDICE` §17-19; `ARC07-DEF-5` §94; §0 riga «Day
19 (target sync)»). *Il calendario avanti non è un difetto: è la Forgia Eterna
che fa il suo mestiere — DM 2026-09-11, D3.*

> ⚠️ I due numeri qui sopra sono **generati** da `campaign/state.yaml`
> (`march_clock.giorno_corrente`): li scrive `state_apply` a fine sessione.
> Questa nota invece è **prosa del DM** e nessuno script la tocca — è la
> separazione decisa con **D14**.

### 2.2 Red Hand of Doom — Horde Composition (Baseline ~10,000)

| Contingent | Baseline | Notes |
|---|---|---|
| Core Hobgoblin (fanteria + veterani + sergenti + Warrior-3 élite) | 4,800 | |
| Ausiliari Goblin/Orchi/Worg Riders | 1,800 | |
| Giganti + Ogre + Ettin | 180 | NO PG alliance — stay with Red Hand |
| Forze Alate (Manticore, Wyvern, Hell Hounds, Chimera) | 140 | |
| Casters Mano Rossa (War Adepts, Blue, Warpriests di Tiamat) | 55 | |
| **Dragons (5 AP-original upscaled)** | 5 | Abithriax (Red adult) / Regiarix (Black young, Rhest) / Ozyrrandion (Blue, Tower) / **Tyrgarun (Blue Old, CR 18 — sky-terror of the battle, NOT Azarr Kul's mount, D11 v2)** / **Fauci di Palude** (Black adult, Hammerfist vanguard — **conditional branch, D10, not yet resolved**: default = flees gravely wounded, may return later as a narrative hook, not guaranteed at Rethmar; PG-kill branch = dies at Hammerfist, −1 dragon, see §2.3) |
| **Draconic spawn = Razorfiend (Tiamat colors)** | 8 | Assigned to Wyrmlord villains upscaled — **tier élite CR 13 «Blackspawn Alfa»** (`Bestiario/mostri/razorfiend-blackspawn-alfa-cr13.md`, DM 2026-07-20); i razorfiend CR 8-9 restano truppa d'ondata |
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

<!-- gen:state:difensori -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

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
<!-- /gen:state:difensori -->

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

<!-- gen:state:scenari -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| Scenario PG | Horde | Difensori | Rapporto |
|---|---|---|---|
| Worst (Ghostlord ostile, Xal'thor allea, 0 quest) | 12,700 | 2,200 | **5.8:1** ☠ |
| Baseline (0 quest) | 9,400 | 2,200 | **4.3:1** |
| Medio (2–3 quest + sabotaggi parziali) | 8,000 | 2,620 | **3.1:1** |
| Ottimale (tutte quest + Rhest + Tower) | 6,800 | 3,770 | **1.80:1** |
| Leggendario (ottimale + Ghostlord redento + Collezionista stop) | 6,400 | 4,370 | **1.46:1** |
<!-- /gen:state:scenari -->

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

## 3. Active Villain Threads (Countdown Clocks)

State machine, not script. Each villain has an agenda that advances each
in-world day **whether or not the party intervenes**. When a clock fills,
the listed consequence triggers.

<!-- gen:state:villain -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| Villain | Stato | Where | Agenda | Clock | Trigger if filled |
|---|---|---|---|---|---|
| Sonjak (Drow Cleric Matrona) — also "Matrona Sajak" in Sal's operative code | 🔴 attivo | Underdark, Cannath Vale border | Subvert dwarven citadel from below; coordinate with Il Collezionista; manage Sal as surface field agent | 4/8 | Drow night-raid on Hammerfist temple (sets up Phase 0 of Rethmar) |
| Salvatore "Sal" della Luna d'Argento | 🔴 attivo | Desert road, Cannath Vale → Rethmar (Shaar) | Profile party's artifacts and magical defenses; plant Sabotage Oil on weapons before Rethmar; deliver living statues to Varis | 0/6 | Sabotage Oil applied — weapon TS failure risk at Phase 3 boss; Phase 4 statue activation proceeds at full strength |
| Il Collezionista (Rakshasa) | 🔴 attivo | Mobile — last seen brokering with drow | Acquire the Crown's spare gem before party can use it; manipulate Conte Valerius | 5/8 | Sponsors anti-party legal pressure; Conte Valerius freezes assets |
| Zalkatar (Illithid Warlock) | 🔴 attivo | Invisible Tower, Dauth region | Mind-strip a captured githyanki for fleet intel | 6/8 | Tower goes mobile; harder to find next session |
| Wyrmlord Saarvith + Regiarix | 🔴 attivo | Lake Rhest ruins | Rebuild dragonrider corps from black dragon spawn | 3/8 | Rhest becomes a fortified war camp; CR +1 to assault |
| Xal'thor (Illithid Coordinator, psionic) | 🔴 attivo | En route with an Illithid invasion force (psionic thralls, larvae, a small core of dominated Githyanki — NOT the free Githyanki dragon-rider force led by Vaereth, which is a separate and hostile faction) | Day 3 fixed assault on the Dauth Tournament to seize Tordek's **Bracieri Gemelli** (planar keys to the Eternal Forge); does NOT target the Orbe delle Otto Porte | Fixed: triggers Day 3 of Tournament regardless | Tournament becomes combat encounter |
| Sethrax il Velato (Illithid emissary, Zalkatar's conclave) | 🔴 attivo | Dauth — infiltrated as tournament finalist "Kethran Mano di Pietra" | Extract a "Seme di Porta" from the Orbe delle Otto Porte during the Tournament's peak resonance, deliver it to Zalkatar at the Invisible Tower | Sync to Tournament (Day 1 = arrival; Day 2 = entered as finalist; Day 3 Round 7 = forced unmasking by Xal'thor's portal) | Sethrax flees to Invisible Tower with the seed → Zalkatar gains +2 effective CR + new orb-derived Mind Blast in P2A finale (Artemis's quest) |
| Azarr Kul (High Wyrmlord) — **Ritual Clock, see §2.0** (NOT the March Clock; the horde's physical approach is tracked separately in §2.1, currently Day 19 of 42) | 🔴 attivo | Fane of Tiamat (Shaar) | Ritual sacrifices/planar conjunctions to summon the Avatar of Tiamat during the Rethmar siege (Day 40-42, Phase 2). Advances only on explicit triggers: +1 per Warpriest élite mass sacrifice (Day 35-38), +2 if Giant Wave ×1 breaches the walls (Phase 1), +3 if Giant Wave ×2 breaches (Phase 3) — see `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §4b | 9/18 | Avatar of Tiamat manifests over Rethmar during Phase 2's 10-round ritual (D8) |
| Conte Valerius (manipulator) | 🔴 attivo | Capital city | Legalize horde funding via "patriotic emergency" loans | 2/8 | Party loses access to legitimate guild merchants |
| **Mira Serani «l'Aranea»** (aranea mutaforma, Red Hand intel) — canonizzata 2026-07-20, `Bestiario/villain/Mira_Serani/` | 🔴 attivo | Mobile — infiltrata nell'onda profughi (Guado → Rethmar) | Raccogliere intel su difese di Rethmar e **artefatti dei PG** per l'orda; spacciarsi per la figlia morta di Lorana (bimba/adolescente); **evitare Lorana** | Trigger, non clock numerico | **Hard counter**: se incrocia Lorana → smascherata a vista, combatte solo per fuggire. Ogni intel raccolta **alimenta i clock esistenti** (Sal/Sonjak/Fase 0-1), non ne apre uno nuovo |
| **Ghaurush «Cenerevento»** (Ogre magi/Stregone 8, GS 16; GS 18 al secondo incontro) — approvato 2026-08-05, `Bestiario/villain/Ghaurush_Cenerevento/` | 🔴 attivo | Retrovie dell'orda, dove ci sono acqua corrente e roccia | Negoziare, o prendere con la forza, le gallerie alte di Hammerfist. **Non serve Tiamat: incassa** | 0/6 | Prende le gallerie alte senza trattare: **+1 CS alla Fase 1 di Rethmar**, e le due lettere che prova i traffici Sonjak↔Collezionista restano inutilizzate |
| **Zin'thara Vel'Ryn «la Voce di Ragnatela»** (Illusionista 9/Danzatrice delle Ombre 2, GS 12) — approvata 2026-08-05, `Bestiario/villain/Zin_thara_Vel_Ryn/` | 🔴 attivo | Campi drow del Sottosuolo, sotto la linea Rethmar | Accumulare prove contro Sonjak per comprarsi un esilio in superficie | 2/8 | Ha prove sufficienti per trattare: si offre al miglior offerente — PG, Il Collezionista o la Mano Rossa. Se non sono i PG, il ramo si chiude |
| **Ushgar «Occhio Reso»** (Orco montano/Barbaro 13, GS 13) — approvato 2026-08-05, `Bestiario/villain/Ushgar_Occhio_Reso/` | 🔴 attivo | Campo degli ausiliari orcheschi, sottovento e fuori dalla palizzata | Ottenere **terra scritta** per i suoi prima che la guerra finisca. **Decisione DM 2026-08-05**: ramo aperto passando prima dall'uscita laterale di Hella | 0/4 | Si prende la terra da solo, da un villaggio che non c'entra niente, e la carta se la fa firmare con le mani |
<!-- /gen:state:villain -->

---

## 4. Open NPC Knowledge State

> Who currently knows what. **Agents must NOT have an NPC reveal something
> they have not learned in-fiction.** Add new rows when an NPC learns
> something; never silently retcon.

<!-- gen:state:conoscenze -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| NPC | Knows that... | Learned how / when |
|---|---|---|
| Sonjak (= Matrona Sajak) | The party freed the Cristal Warriors but does NOT know they have all 3 Crown gems | Drow scouts witnessed the mine assault |
| Ghaurush «Cenerevento» | Che i Custodi Eterni portano **artefatti divini**; **non** sa quali | Rapporti dell'avanguardia della Mano Rossa (2026-08-05) |
| Zin'thara Vel'Ryn | Che i Custodi Eterni hanno liberato i Guerrieri di Cristallo, come Sonjak; **non** sa nulla della Corona | Rete di informatori drow nei campi (2026-08-05) |
| Ushgar «Occhio Reso» | Che i quattro Custodi viaggiano con artefatti; **non** sa quali, **e non gli importa** | Voci di caserma fra gli ausiliari (2026-08-05) |
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
| Norro Wiston (ex-Portavoce del Guado di Drellin, profugo a Rethmar) | The party are the Custodi Eterni; Thorik died and was resurrected at the Guado (he was present, Arco 00) | Direct witness; arrived Rethmar ~Day 16-18 with the refugee wave — canonized 2026-07-20 |
| Sertieren il Saggio (mago halfling profugo, ospite della biblioteca di Pyriel) | His *sending* to Silverymoon is blocked by a ritual interference on the Wyrmbones; does NOT know who runs it | Failed attempts Day 14-18 — canonized 2026-07-20 |
| Lirien Amaranti («Il Giullare Spezzato») | He can recognize the Maestro's hand in the living statues (does NOT know the network leads to Varis/Sal/Il Collezionista); knows the street-talk of the Ponte Nuovo | Apprenticeship trauma + tavern ears — canonized 2026-07-20 |
| Mira Serani «l'Aranea» | The party already met her (disguised as a refugee child) on the road to Hammerfist and let her go; knows fragments of the PCs' artifacts/routes; does NOT know Lorana survived and is at Rethmar | Embedded Red Hand spy since Drellin's Ferry — canonized 2026-07-20 |
| Lorana (hard counter to l'Aranea) | Believes her daughter Mira is dead (carries her brooch); does NOT know the child was murdered and impersonated by an aranea — will recognize the impostor **on sight** if they meet | Grief + the brooch; the truth is a DM secret in `Bestiario/png/Lorana/…/Lorana.md` — canonized 2026-07-20 |
| Tiri Kitor wild elves | Nothing yet — first contact pending Starsong Hill | — |
<!-- /gen:state:conoscenze -->

---

## 5. Open Promises, Debts, Bargains (PG ↔ World)

> Things the PCs are **on the hook for**. Agents must surface these when
> relevant; they create R.A. Salvatore-style internal stakes.

| Owed by | Owed to | What | Consequence if broken |
|---|---|---|---|
| Thorik | Re Thorek Hammerfist | Lead defense at Rethmar OR send Aegis Fang as proxy | Loss of Custode Eterno status; dwarven mercenaries withdraw |
| *(ramo aperto, non ancora contratto)* **Hella**, e solo dopo **Thorik** | Ushgar «Occhio Reso» | Un atto scritto che assegni terra ai suoi ausiliari, in cambio del **ritardo degli orchi nella prima ondata** a Rethmar. **Ordine deciso dal DM 2026-08-05**: si offre prima l'uscita laterale di Hella (il Cerchio non si oppone all'insediamento); la firma di Thorik è il secondo passo, non il primo | Se firma **Hella**: problema con i druidi del Cerchio Sacro, e P1B a rischio se il rituale non è stato fatto. Se firma **Thorik**: si attiva la penale della riga qui sopra — **perdita dello status di Custode Eterno**. Se non si tratta: Ushgar si prende la terra da un villaggio |
| 🔵 *(non ancora contratto — si contrae al rito)* **Thorik** | Hella | Il **+2 di deflessione della Corona** (`ARC07-DEF-3` §5, v4-bis DM 2026-09-12): resta a **−1 CA permanente**, e ogni volta che lei scuda qualcuno **lui scatta verso quella persona**. ⚠️ Fino al 2026-09-12 questa riga diceva *«he sacrificed 2 perm CON»* al passato, per una scena mai giocata | Affects Hella's ethics rolls in arguments with Thorik |
| 🔵 *(non ancora contratto — si contrae al rito)* **Tordek** | Hella | **Ancoraggio della Montagna**, che lascia i Bracieri per sempre (`ARC07-DEF-3` §5). Stessa correzione: i «500 PE» erano registrati come versati e non lo sono | Affects romantic-bond progression at Sacred Forest |
| Tordek | Tournament organizers | Show up at Dauth by **Day 29** (eve of the preliminaries — invite Day 24, arrival Day 28, Tournament Day 1-3 = Day 30-32, HOOKS-INTEGRATION-MASTER §1.1) | Disqualification; 150 Lance di Re Thorek reinforcements lost (D10 — separate from the 300 mercenaries won at the Tournament itself) |
| Artemis | Varis "Seta-Argento" | Deliver one Underdark artifact per quarter · **⚠️ 2026-07-31: ha il Seme-Mercato in mano, non toccato (nessun Marchio). La partita con Varis è aperta e alla pari** | Varis cuts off the Mantello dei Tiri Salvezza supply |
| Artemis | Mask cult (suspected) | Unknown — they've been watching the Ring | Black-bag attempt during a vulnerable moment |
| Hella | Druid Circle | Pass the Sacred Forest ritual within 12 days | Circle will not aid at Rethmar |
| Party (collective) | Therysol | Help him strike Il Collezionista's Dauth cell | Therysol withdraws his combat support |

---

## 6. Artifact State (current powers, not theoretical max)

See `skills/rumblingstone-campaign/references/campaign-artifacts.md` for
full mechanics.

> **Two-times table (T6c, DM-confirmed 2026-07-04)**: the two state columns
> are labelled. **«Today at the table»** = the real table position per §0
> (ARC-07 P4 in progress, canon D8/D16). **«Prepared (ARC-09 entry)»** = the
> forward-written state that becomes true only after P4 → P3B → P5 are
> played. For tonight's session ALWAYS use the "Today" column.

<!-- gen:state:artefatti -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| Artifact | Holder | **Today at the table (ARC-07 P4)** | **Prepared (ARC-09 entry)** |
|---|---|---|---|
| Aegis Fang | Thorik | Pre-full-awakening: +2 Returning Dwarven Waraxe; bonded | Unchanged until the Siege (P5) is won → then Stage 1 full awakening (see Aegis master) |
| Corona di Adamantio | Thorik | ✅ **Topazio + SMERALDO accesi** e **Rituale Legacy 3 «Incudine del Mondo» COMPLETATO** (giocato 2026-07-31). Poteri attivi: Stone's Awareness (incl. traps + comprehend languages), +2 deflection AC, Moradin's Insight, Topazio 1/mese (attivazione 1 ora), **Smeraldo/Terra 1/settimana**, e i due sbloccati dal Rituale 3 — **Adamantine Will** (immune charme/compulsione + 4 razziale vs mentale su pietra) e **Mantle of Stone and Spirit** (**Mind Blank permanente**, RD 5/epico, Comunione 1/mese da un Nodo). ✅ Il pegno del Rituale 3 l'ha versato **Thorik**, il portatore (−2 DES / +2 COS permanenti) — correzione DM 2026-08-06: fino a quella data era attribuito a Tordek per errore. ⚠️ Si somma al **−2 DES** che la Corona gli aveva già preso quando l'ha indossata (`PortaleForgia-P1-REVISED-Corretta.md`, «Limitazioni»). **Totale: −4 al punteggio** (DES 10 → 8 → 6), che sono **−2 al modificatore** (da +0 a −2): −2 a CA, Riflessi, iniziativa e prove di DES. In cambio **+4 CAR** (8 → 12) e **+2 COS**. 🔒 **Non rimovibile volontariamente** finché mancano gemme (DM 2026-09-04): l'unica volta che è uscita dalla testa è stato **per incastonare lo Smeraldo**. Mancano Corona +3, Senzienza e il Rubino: si sbloccano col **Rituale 4** = viaggio a −1.000 | All 3 gems lit: + Emerald earthquake 1/week; Ruby single-use SPENT at the ancient battle (≈372 DR) |
| Ring of Chaotic Illumination | Artemis | Reforged at Eternal Forge: full base powers | Unchanged; awaits further evolution at Invisible Tower |
| Bracieri Gemelli di Moradin | Tordek | Fire ✅ + Earth ✅: Salto Infuocato 3/day, Fire Resist 10, DR 5/adamantine, Jump +10; Benedizione della Forgia active (4 charges/day — permanent, DM 2026-07-04); **Ancoraggio della Montagna 2/day** (immediata, nega il movimento forzato). ⭐ **NUOVO 2026-07-31 — «Diventare una Collina»** sbloccato dalla caduta di Terros: taglia Grande 1 min, 1/giorno, **prima attivazione automatica e gratuita** quando uno scontro con una creatura Enorme+ porta Tordek sotto metà pf; dopo, azione di movimento **solo in condizioni di pericolo** | Unchanged |
| Cintura della Devastazione (custom PG, D17) | Tordek | Active — Devastation Gauntlets (MIC) moved to **belt slot** so wrists stay free for the Bracieri; ~3/day devastation charges (+2d6). Sheet: `PG/Artefatti/Artefatti-Pg/Tordek/00_Cintura_della_Devastazione.md`. Exact values → ARC-07 B5 | Unchanged |
| Collana dei Semi Eterni | Hella (dead — resurrection pending) | Forged, awaiting the P3B ritual; Hella not yet resurrected | Active post-resurrection: Treant summoning (limited), Avatar form (1/day). **I 3 slot-dono hanno una meccanica dal 2026-09-12** (`ARC07-DEF-3` §5, DM): ogni PG dona **un potere del proprio artefatto**, che lo lascia per sempre e **germoglia in un seme** — Thorik il **+2 di deflessione** → *Scudo del Custode*; Tordek l'**Ancoraggio** → *Pelle di Adamantio* RD 3/adamantino; Artemis **1d6 di Eldritch Blast** → *Rovo Eldritch* a volontà. 🌱 E il seme **restituisce** al donatore ciò che ha ricevuto, **una volta sola**, quando Hella decide. Slot **ancora non spesi**: il rito non è stato giocato |
| Cuore di Moradin | Crown set (altar) | Intact — will be expended as catalyst in the P3B ritual | SPENT: single-use expended to resurrect Hella |
| Orbe delle Otto Porte (Githyanki artifact, campaign canon) | Tournament prize, not yet held | Not in play | Awaits Tournament outcome — N/A until Tordek wins |
<!-- /gen:state:artefatti -->

**Spent / single-use already burned** *(per column: Ruby & Cuore are spent
only in the "Prepared" time; at today's table the Cuore is still intact)*:

- Ruby gem of the Crown (used at the battle 1,000 years before, ≈372 DR) —
  spent in both times (the battle is in the past either way once P5 is played)
- Cuore di Moradin (used to resurrect Hella) — **Prepared column only**

If any agent ever has a character "use" one of these again in a time where
they are spent, that is a coherence violation — flag to DM.

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
- **[PROFUGHI]** I sei volti del Guado di Drellin (Norro, Sertieren, Derny, Delora, Iormel, Kellin — `Bestiario/png/Guado_di_Drellin/`) sono a Rethmar o in arrivo: chi di loro incontrano i PG per primo, e in quale stato?
- **[LIRIEN]** Il Giullare Spezzato ha visto qualcosa nelle statue vive — i PG gli daranno retta prima che lo faccia qualcun altro? (`Bestiario/png/Lirien/Lirien.md` §2.1)
- **[ARANEA]** Mira Serani si muove tra i profughi con la faccia della figlia morta di Lorana, raccogliendo intel per l'orda: quando (e come) i PG portano Lorana abbastanza vicino da smascherarla? E cosa fa la verità alla colpa di Lorana? (`Bestiario/villain/Mira_Serani/`)
- **[SEME DEL GHOSTLORD]** `[CANONE — DM 2026-07-23; l'incontro avviene, l'esito si gioca]` Al −1000, durante la prep notturna a Hammerfist, i PG incrociano il **Mastro Costruttore Zeth** (futuro **Ghostlord / Zeth il Murato**) mentre inizia la Consacrazione che un «chierico incappucciato» (mano del **Collezionista** attraverso il tempo) trasforma in **Lichificazione**. I PG assistono, senza saperlo, all'origine del Ghostlord. Paga in ARC-09 come **dilemma etico di Hella** su Zeth. Fonte: `07_.../ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` §1-bis; cross-link `Bestiario/villain/Ghostlord/`.
- **[VATORE/SAL]** `[CANONE — DM 2026-07-23; l'incontro avviene, l'esito si gioca]` Al −1000 i PG incrociano **Vatore**, il "Ladro d'Ombra" che diventerà **Salvatore "Sal"** (villain ARC-09). Ha appena rubato il **Sigillo di Ossidiana** e li osserva con terrore reverenziale. **Non è un innocente ingenuo**: è già **corrotto da avidità e sete di potere** (canone DM), non gli importano le conseguenze — è questa scelta a renderlo Sal. **Sincronizzazione temporale** (`Bestiario/villain/Salvatore/Salvatore.md`): ferirlo/derubarlo/segnarlo a −1000 → eco su Sal nel 1372 (sanguina / manca un asso / li teme / li odia). Il Cronolito garantisce che sopravvive (paradosso auto-consistente). Esito da registrare qui. Fonte: `07_.../ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` §5.
- **[SIGILLO DI OSSIDIANA]** `[CANONE — DM 2026-07-23; se rubato a Vatore]` Artefatto minore allineato a **Shar** (Signora della Notte): **Manto di Notte Assoluta** (sopprime la luce magica ≤2 entro 9 m; *daylight*+ prova CL CD 20) + **Furto della Notte** (1/g, azione furtiva come invisibile/silenzioso 1 round). **Prezzo**: ogni uso **divora un'anima** (1 livello negativo a una creatura toccata nelle 24 h, o un'anima intrappolata); **se non disponibile, consuma il portatore** (livello negativo permanente dopo 24 h) — è ciò che corrompe Vatore in Sal. **Contrasto con l'Anello di Artemis** (scintilla di Lathander, nemesi di Shar): se lo porta Artemis, i due artefatti si annullano (poteri di luce/alba dell'Anello instabili/non disponibili; Sigillo soppresso) → bivio Notte vs Alba per l'ARC-09. Se i PG lo rubano e lo riportano nel presente (Cronolito), Sal si presenta senza il suo asso. Fonte: `07_.../ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` §5 (scheda); `Bestiario/villain/Salvatore/`.
- **[I TRE DONI]** `[CANONE — DM 2026-09-12; si gioca al rito P3B]` Al rito di resurrezione ogni PG può donare **un potere del proprio artefatto**, che lo lascia **per sempre** e **germoglia in un seme della Collana** (`ARC07-DEF-3` §5 — è un **trapianto**, non una tassa: il party non perde la capacità, cambia mano e forma). **Thorik** il **+2 di deflessione** della Corona → resta a **−1 CA permanente**, Hella ottiene lo **Scudo del Custode** (1/g, immediata, prende il danno di un alleato entro 9 m **dimezzato**) e **l'Eco del Custode** — ogni volta che lei lo usa, **lui è accelerato 3 round verso chi è stato protetto**. **Tordek** l'**Ancoraggio della Montagna**, che lascia i Bracieri → **Pelle di Adamantio, RD 3/adamantino** (la **sua unica** RD). **Artemis** **1d6 di Eldritch Blast**, 7d6 → 6d6 → **Rovo Eldritch**, a volontà, 2d6 a 18 m. 🔗 **I tre si moltiplicano**: colpo da 40 → dimezzato → meno la RD → Thorik scatta → e lei non perde il turno. ⚒️ **Gli artefatti reagiscono**, al dono e al rifiuto: Aegis Fang (Ego 14) smette di dubitare di Thorik **o lo giudica**; i Bracieri lo avvertono un round prima **o tacciono una settimana**; l'Anello si illumina di riflesso **o si spegne 24 h**; la Corona si scalda **o resta fredda al Rituale 4** — tutte **reversibili**. 🚪 **Chi rifiuta** lascia il seme **dormiente**, e lo colma **in gioco** in ARC-09 (il dono si attiva **all'indietro**). 🌱 **La Collana restituisce**: una volta sola per seme, **decide Hella**, e il donatore riavvia ciò che aveva dato **per una scena**. **Segna qui la scelta di ciascuno appena il rito è giocato.**
- **[DEBITO DELLA RADICE]** `[CANONE — DM 2026-07-23; il ramo A/B/C si gioca al rito]` Strappare Hella al Sogno della Terra (Via della Radice + Voto del viaggio) lascia un vuoto che l'ordine naturale esige di colmare — filo grigio (non bianco né nero). Al rito appare **la Custode delle Radici** (psicopompo neutrale, NON ostile): chiede un pegno, mai la vita di Hella (Moradin la protegge). Tre risposte del party: (A) accettare un servizio futuro → **quest ARC-09 «Il Cerchio Sacro della Foresta»** (druida Hella; CANONE DM 2026-07-23: la Custode si aggancia al Cerchio Sacro, non al Ghostlord) + Earth Dream 2/g; (B) rifiutare → il vuoto «risale» come nemico ARC-09 (non-morto della terra / crepa fungina di Sonjak); (C) offrire Durik come ponte vivente → Durik risponde al Sogno 1/sessione ma la Collana non perde mai il 3° seme. Fonte/dettagli: `07_.../ARC07-DEF-3-RESURREZIONE-HELLA.md` §6. Paga in ARC-09, non subito.
- **[MARCHIO DI VARIS — ⚠️ NON ATTIVO, MA IL SEME È NELLO ZAINO DI TORDEK]** `[ESITO GIOCATO 2026-07-31: né accettato né rifiutato]` **Aggiornamento**: Artemis ha **estratto il cabochon senza toccarlo** e l'ha fatto mettere **nello zaino di Tordek**. Il Marchio si chiude **col tocco**, quindi **non è attivo**: Varis NON localizza Artemis e non ha crediti da riscuotere; Artemis non ha ottenuto né il Frammento di Mercato né il +1 del rifiuto. Il Seme è **posseduto, integro e ancora tiepido**, e l'offerta **non scade**. ⚠️ **Se lo tocca TORDEK, il Marchio si chiude su di lui** (Varis ricalibra: non offre tesori a un monaco nanico, offre certezze). Varis leggerà la mossa come una **contro-mossa di un pari**, non come una fuga → al #4, Vatore riconosce la firma di un collega, non di un debitore. Dettaglio e conseguenze: `07_.../ARC07-DEF-1-PIANO-TERRA-TERROS.md` §6-bis, blocco CANONE GIOCATO. *(Testo originale della scena, per contesto:)* Sulla riva dell'Oceano di Roccia (Piano della Terra), l'Anello di Artemis capta un **Seme-Mercato** di **Varis "Seta-Argento"** (un cabochon violetto/innesto planare): esca calibrata sull'avidità di Artemis, **privata** (solo il suo giocatore la vede). Varis (telepatico) offre un **affare da predone** — sconto a vita sul Mantello dei TS + canale per piazzare il bottino del Sottosuolo — in cambio dell'incastonare la gemma nell'Anello (Marchio). Bivio grigio stile Andor (avidità vs lealtà), nessuna scelta pulita; funziona anche se il party salta l'incontro dei Cristalli. Se **accetta** → Marchio di Varis + rete di ricettazione, paga in ARC-09 (Varis broker urbano, cross-link `Bestiario/villain/...Varis...`); se **rifiuta** → rispetto guardingo di Varis. Fonte: `07_.../ARC07-DEF-1-PIANO-TERRA-TERROS.md` §6-bis.

### §7.E Echo Ledger (choices the world remembers)

Format and rules: `skills/rumblingstone-narrative-style/references/consequence-echoes.md`.
Arm 1–3 echoes per session from Key decisions; fire ≥1 per session when
fiction allows. Max ~12 armed — prune during prep.

<!-- gen:state:echi -->
<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — non modificare a mano (ADR-0050) -->

| ID | Origin (sess., PC, choice) | Tone | Fuse | Payoff sketch | Status |
|----|----------------------------|------|------|---------------|--------|
| **E-07a** | 2026-07-31 · **Artemis** · prende il Seme-Mercato di Varis ma **non lo tocca**, e lo fa portare a **Tordek** | grigio | lunga (ARC-09) | Varis scopre di essere stato riconosciuto e trattato da pari: apre una **trattativa**, non una riscossione. E il giorno in cui serve un favore, la gemma è già in mano al party — sulla schiena sbagliata | 🔫 armato |
| **E-07b** | 2026-07-31 · **Tordek** · porta nello zaino un innesto planare **senza sapere cosa sia** | grigio/inquieto | media | Il primo che tocca il Seme se ne prende il Marchio. Se è Tordek, Varis gli offre **certezze** invece che tesori — l'esca giusta per un monaco che ha perso una compagna | 🔫 armato |
| **E-07c** | 2026-07-31 · **Thorik** · Al rito dello Smeraldo gli viene chiesto **«un pezzo di te stesso»**, e **non lo delega**: si inginocchia sotto il Peso invece di comprarne l'uscita col bottino dell'arco. −2 DES / +2 COS permanenti. | luminoso, costoso | media | **Ha pagato dove non si vede, e lo applaudono per la metà che si vede.** La DES era già la sua statistica povera — **10 di base**, e la Corona gliene aveva già tolti 2 quando se l'è messa in testa: questi altri due la portano a **6 di punteggio** (−4 in tutto), che al tavolo sono **un punto solo** di CA, Riflessi e iniziativa in più rispetto a ieri. Nessuno al tavolo lo noterà. Il +2 COS invece lo rende *più bravo* nell'unica cosa per cui lo misurano — reggere. Riemerge la prima volta che un nano di Hammerfist (o Re Thorek) lo elogia per quanto sa incassare e **lui non corregge nessuno**: l'unico che sa il prezzo è lui. Poi paga davvero quando al party viene chiesto un altro pegno e **Thorik si muove per primo**, perché adesso conosce il cambio e non si fida a lasciarlo accettare a un altro. | 🔫 armato |
| **E-07e** | 2026-07-31 · **Tordek** · «Guarda il portatore pagare» — eco mai realmente esistita. | — | — | Annullata il 2026-08-09. Nasceva dall'attribuzione sbagliata del pegno — era «il portatore guarda un altro reggere il peso» — e il 2026-08-06 era stata semplicemente rovesciata su Tordek. Ma un'eco registra **una scelta**, e Tordek qui non ne ha fatta nessuna: non gli è stato chiesto niente e non ha rinunciato a niente. Rovesciare un'eco non la rende vera. L'ID **non si riusa**; le righe vive di Tordek restano E-07a/E-07b. Rimpiazzata da E-07f. | ✖ annullata |
| **E-07f** | 2026-07-31 · **Thorik** *(e **Hella**, dall'altra parte)* · Sotto la gravità, mentre le ossa scricchiolano, una **luce verde tenue** gli si stringe alle spalle: *«Non sei solo a portare questo peso. Mai più solo.»* Lui la prende per Moradin. Era Hella, morta, a tre metri da lui nella stessa sala. | intimo | lunga (oltre il #3) | ⚠️ **Non spiegarlo prima della resurrezione (#3)** — è l'asimmetria scritta dal modulo (`ARC07-DEF-1` §9 Fase 1, regia). Paga due volte: **(a)** quando Hella torna e quelle parole tornano con lei — e il momento smette retroattivamente di essere la promessa di un dio e diventa quella di una compagna morta che stava per riportare indietro; **(b)** al Dono 1 del rito di Hella, perché è **questa** frase la ragione per cui Thorik dirà di sì al prezzo, non la devozione a Moradin. Per la giocatrice di Hella è il suo eco dal Sogno della Terra. | 🔫 armato |
| **E-07d** | 2026-07-31 · **Terros** · l'ultimo suono del guardiano è di **assenso** (avevano curato i Cristalli) | luminoso | lunga | La Forgia registra la vittoria **onorata**. Un guardiano che approva è una porta che resta aperta: eco al #4 e nella Cronaca | 🔫 armato |
| **E-08a** | 2026-08-05 · **DM** · approvata l'ala orchesca della Mano Rossa: dentro l'orda c'è **chi paga più di quanto incassa** | grigio | lunga (ARC-09 → dopoguerra) | Qualunque cosa i PG scelgano, la valle avrà orchi **anche dopo la guerra**: la domanda è se con un atto o con un assedio. Riemerge quando si contano i vivi a Rethmar | 🔫 armato |
<!-- /gen:state:echi -->

### §7.R Reputation (Fama / Infamia) + Anointing Threads

Format and rules: `skills/rumblingstone-narrative-style/references/pc-protagonism.md`.

| PC | Fama (epithets, witnessed deeds) | Infamia | Anointing thread (status) |
|----|----------------------------------|---------|---------------------------|
| Thorik | — | — | — (dormant) |
| Tordek | — | — | — (dormant) |
| Hella | — | — | — (dormant) |
| Artemis | — | — | — (dormant) |
| Party | — | — | n/a |

---

## 8. Changelog (append-only)

> 📍 **Lo storico vive in [`state-changelog.md`](state-changelog.md)**, scorporato
> il 2026-09-16 (lotto 4d-2): erano **1.179 righe, il 71%** di questo file.
>
> Ci scrive `scripts/state_apply.py`. Qui non si aggiunge niente a mano: una
> voce scritta in questa sezione invece che nell'altro file sarebbe un secondo
> storico, e due storici divergono.
