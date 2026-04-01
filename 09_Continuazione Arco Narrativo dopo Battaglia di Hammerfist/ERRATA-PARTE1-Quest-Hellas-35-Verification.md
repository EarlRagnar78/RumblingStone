# ERRATA CORRIGE PARTE 1 - QUEST HELLAS (3.5 Verification)
## Correzioni Statblocks Creature per Conformità D&D 3.5 SRD

---

## SOMMARIO VERIFICHE

**File Analizzati:**
1. Arco-Post-Hammerfist-P1A-Timeline-Quest-Hellas-COMPLETA.md
2. Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO.md
3. Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md
4. SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md

**Status:** ⚠️ MULTIPLE ERRORI TROVATI - Correzioni necessarie

---

## ERRORI GLOBALI (Tutti File)

### 1. ACTION ECONOMY TERMINOLOGY

**ERRORE CRITICO:** Uso inconsistente terminologia azioni

**Termini Sbagliati Trovati:**
- ❌ "Bonus Action" (5e term, NON esiste in 3.5!)
- ❌ "Reaction" (5e term, in 3.5 è "Immediate Action")
- ✅ "Standard Action" (corretto)
- ✅ "Move Action" (corretto)
- ✅ "Full-Round Action" (corretto)

**CORREZIONE GLOBALE NECESSARIA:**
- Sostituire TUTTI "bonus action" → "swift action"
- Sostituire "reaction" → "immediate action"
- Aggiungere note su "free action" quando appropriato

---

### 2. MISSING STATBLOCK ELEMENTS

**Tutti creature mancano:**
- ❌ **Touch AC** (obbligatorio 3.5!)
- ❌ **Flat-Footed AC** (obbligatorio 3.5!)
- ❌ **Base Attack Bonus (BAB)** esplicito
- ❌ **Grapple modifier** esplicito
- ⚠️ **CMB/CMD** (questi NON esistono in 3.5, sono Pathfinder!)

**CORREZIONE:** Aggiungere a TUTTE creature formato:
```
**AC:** X (components), touch X, flat-footed X
**BAB:** +X, **Grapple:** +X
```

---

## CORREZIONI SPECIFICHE PER CREATURE

### PARTE 1A: Drow Pyromancers (EL 9)

**File:** P1A-Timeline-Quest-Hellas-COMPLETA.md

**Statblock Originale (ERRATO):**
```
**Drow Pyromancer** (Wizard 8)
- AC: 18
- HP: 52
- Melee: Dagger +6 (1d4+1)
```

**PROBLEMI:**
1. ❌ Missing Touch AC/Flat-Footed
2. ❌ Attack bonus sbagliato (dovrebbe essere +4 base, non +6!)
3. ❌ Missing spell list completa
4. ❌ Missing SR (Spell Resistance drow!)

**STATBLOCK CORRETTO (SRD 3.5):**

```
**Drow Pyromancer** (Drow Wizard 8)
- **CR:** 9
- **Type:** Humanoid (Elf)
- **Size:** Medium
- **Init:** +2 (Dex +2, Improved Initiative +4)
- **Senses:** Darkvision 120ft, Listen +2, Spot +2

**Defense:**
- **AC:** 16 (+2 Dex, +4 mage armor), touch 12, flat-footed 14
- **HP:** 52 (8d4+24, +8 Con, +8 False Life temp)
- **Fort:** +5, **Ref:** +4, **Will:** +8
- **SR:** 19 (11 + character level, drow racial)
- **Immune:** Sleep effects
- **Resist:** None
- **Weaknesses:** Light Blindness (dazzled in bright light)

**Offense:**
- **Speed:** 30ft (6 squares)
- **Melee:** Dagger +4 (1d4/19-20) OR +5 with poison
- **Ranged:** Ray +6 ranged touch
- **Space:** 5ft, **Reach:** 5ft
- **BAB:** +4, **Grapple:** +4

**Spells Prepared (CL 8th, Spell Focus Evocation):**
- **4th (3+1):** *Fire Shield*, *Wall of Fire* (DC 19), *Greater Invisibility*
- **3rd (4+1):** *Fireball* (DC 18, 8d6), *Dispel Magic*, *Fly*, *Haste*
- **2nd (5+1):** *Scorching Ray* (+6 ranged touch, 4d6 ×2 rays), *Mirror Image*, *Invisibility*, *Resist Energy*, *Web*
- **1st (5+1):** *Burning Hands* (DC 16, 5d4), *Mage Armor* (cast), *Shield*, *Magic Missile* (5 missiles), *Expeditious Retreat*
- **0 (4):** *Ray of Frost*, *Detect Magic*, *Read Magic*, *Prestidigitation*

**Spell-Like Abilities (Sp, CL 8th):**
- 1/day: *Dancing Lights*, *Darkness*, *Faerie Fire*

**Statistics:**
- **Str:** 10 (+0), **Dex:** 14 (+2), **Con:** 16 (+3), **Int:** 18 (+4), **Wis:** 10 (+0), **Cha:** 8 (-1)
- **Base Atk:** +4, **Grapple:** +4
- **Feats:** Spell Focus (Evocation), Greater Spell Focus (Evocation), Improved Initiative, Combat Casting, Scribe Scroll
- **Skills (ranks):** Concentration +14 (11 ranks), Knowledge (arcana) +15 (11 ranks), Spellcraft +17 (11 ranks +2 synergy), Listen +2 (racial), Spot +2 (racial), Search +6 (racial)
- **Languages:** Elven, Undercommon, Common, Draconic, Abyssal

**Gear:**
- Dagger (masterwork, poisoned: Drow poison DC 13 Fort, unconscious 1 minute + 2d4 Str damage)
- Wand of *Scorching Ray* (CL 5th, 20 charges)
- Potion *Cure Moderate Wounds* ×2
- Spell component pouch
- 50gp gems

**Tactics:**
- Pre-combat: Cast *Mage Armor*, *False Life*
- Round 1: *Greater Invisibility* OR *Haste* (if ally melee)
- Round 2-3: *Fireball* clusters, *Scorching Ray* single targets
- Desperate: *Darkness* + retreat (darkvision advantage)
```

---

### PARTE 1B: Treant Corrotto Boss (CR 11)

**File:** P1B-Cerchio-Treant-COMPLETO.md

**PROBLEMI MAGGIORI:**
1. ❌ Treant base stats NON segue SRD (Treant standard è CR 8, Large, 12 HD)
2. ❌ Attack bonuses errati
3. ❌ DR 10/slashing corretto MA vulnerabilità fire NON standard (Treant 3.5 vulnerabili fire ×1.5, ok)
4. ❌ Grab ability non dettagliata correttamente

**STATBLOCK CORRETTO vs SRD:**

**Treant Standard 3.5 (reference):**
- CR 8, Large Plant
- HD: 7d8+35 (HP 66)
- AC: 20 (-1 size, +11 natural), touch 9, flat-footed 20
- Slam +12 melee (2d6+9)
- **DR 10/slashing and bludgeoning** (NOT just slashing!)
- Vulnerable Fire ×1.5

**Treant Corrotto Advanced (CR 11 - Corrected):**

```
**Treant Corrotto "Radiceamara"** (Advanced Corrupted Treant)
- **CR:** 11
- **Type:** Plant (Corrupted)
- **Size:** Huge (4.5m tall, 3m space)
- **Init:** -1 (Dex 8)
- **Senses:** Low-light vision, Tremorsense 60ft, Listen +16, Spot +16

**Defense:**
- **AC:** 22 (-2 size, -1 Dex, +15 natural), touch 7, flat-footed 22
- **HP:** 180 (12d8+120, Toughness feat)
- **Fort:** +18, **Ref:** +3, **Will:** +12
- **DR:** 10/slashing and bludgeoning (both required to bypass!)
- **Immune:** Plant traits (poison, sleep, paralysis, polymorph, stunning, mind-affecting)
- **Resist:** Cold 10
- **Vulnerable:** Fire (×1.5 damage, standard treant)

**Offense:**
- **Speed:** 30ft (6 squares)
- **Melee:** 2 slams +16 (2d6+12/19-20 + grab + 1d6 fire corruption) each
- **Space:** 15ft (3×3 squares), **Reach:** 15ft (3 squares)
- **BAB:** +9 (12 HD plant ¾ BAB), **Grapple:** +29 (+9 BAB +12 Str +8 size)

**Special Attacks:**
- **Improved Grab (Ex):** Hit with slam = free grapple attempt (+29) without AoO
- **Constrict (Ex):** Auto 2d6+12 damage ogni round grappled
- **Animate Trees (Sp):** 1/day, standard action, 2d6 trees within 180ft (as *Animate Objects* CL 12th, last 12 rounds)
- **Trample (Ex):** 2d6+18 damage, Reflex DC 26 half (Str-based DC)
- **Radici Avvinghianti (Su):** Ranged touch +7 (range 60ft), target grappled (+29) if hit, pulled 15ft closer per round

**Corruption Abilities:**
- **Soffio Corrotto (Su):** 30ft cone, recharge 1d4 rounds, 8d6 fire + 4d6 necrotic (half each type), Reflex DC 22 half, also Fort DC 22 or nauseated 1d4 rounds
- **Aura Corruzione (Su):** 15ft radius, natura allies -2 attacks/saves/checks, druid concentration DC 20 to cast
- **Richiamo Elementali (Sp):** 1/every 3 rounds, summon 1d4 Small Fire Elementals (as *Summon Monster IV*, CL 10th, last 10 rounds)

**Statistics:**
- **Str:** 35 (+12), **Dex:** 8 (-1), **Con:** 30 (+10), **Int:** 12 (+1), **Wis:** 16 (+3), **Cha:** 12 (+1)
- **Base Atk:** +9, **Grapple:** +29
- **Feats:** Improved Sunder, Power Attack, Improved Critical (slam), Toughness, Weapon Focus (slam)
- **Skills:** Diplomacy +9, Hide -9 (Huge size), Intimidate +9, Knowledge (nature) +9, Listen +16, Sense Motive +9, Spot +16, Survival +16
- **Languages:** Common, Treant, Sylvan
```

**CORREZIONI CHIAVE:**
1. ✅ BAB +9 (non +12 come scritto) → attack +16 (non +20!)
2. ✅ Grapple +29 (aggiungi +8 size Huge)
3. ✅ DR 10/slashing AND bludgeoning (standard treant)
4. ✅ Touch AC 7, Flat-Footed 22 aggiunti

---

### PARTE 1C: Hell Hounds (CR 5 each)

**File:** P1C-Rituale-COMPLETO-SCALE.md

**STATBLOCK ORIGINALE (Approssimativo):**
```
**Hell Hound**
- AC: 18, HP: 52
- Bite +10 (1d8+6 fire)
- Breath 30ft cone 4d6 fire
```

**STATBLOCK CORRETTO SRD 3.5:**

```
**Hell Hound**
- **CR:** 5 (adjusted for level 13 party)
- **Type:** Outsider (Evil, Extraplanar, Fire, Lawful)
- **Size:** Medium
- **Init:** +5 (Dex +1, Improved Initiative +4)
- **Senses:** Darkvision 60ft, Scent, Listen +7, Spot +7

**Defense:**
- **AC:** 16 (+1 Dex, +5 natural), touch 11, flat-footed 15
- **HP:** 45 (7d8+14)
- **Fort:** +7, **Ref:** +6, **Will:** +5
- **Immune:** Fire
- **Vulnerable:** Cold (×1.5 damage)
- **SR:** None

**Offense:**
- **Speed:** 40ft (8 squares)
- **Melee:** Bite +8 (1d8+4 + 1d6 fire)
- **Space:** 5ft, **Reach:** 5ft
- **BAB:** +7, **Grapple:** +9

**Special Attacks:**
- **Breath Weapon (Su):** 10ft cone (NOT 30ft!), 2d6 fire, Reflex DC 13 half, usable ogni 2d4 rounds
- **Burn (Ex):** Victim catches fire on bite hit (DC 13 Reflex avoid), 1d6 fire/round until extinguished (DC 15 Reflex per round)

**Statistics:**
- **Str:** 15 (+2), **Dex:** 13 (+1), **Con:** 15 (+2), **Int:** 6 (-2), **Wis:** 10 (+0), **Cha:** 6 (-2)
- **Base Atk:** +7, **Grapple:** +9
- **Feats:** Improved Initiative, Run, Track
- **Skills:** Hide +11, Jump +12, Listen +7, Move Silently +11, Spot +7, Survival +7
- **Languages:** Cannot speak, understands Infernal

**Tactics:**
- Charge target (Spring Attack se feat), bite + breath
- Priorità: Flanking per +2 bonus
- Se heavily damaged: Retreat + breath cone defensive
```

**CORREZIONI:**
1. ❌ AC 18 → ✅ AC 16 (SRD standard)
2. ❌ Bite +10 → ✅ Bite +8 (BAB +7, Str +2, -1 multiattack if applicable)
3. ❌ Breath 30ft → ✅ Breath 10ft (SRD correct)
4. ❌ HP 52 → ✅ HP 45 (7d8+14 standard)

---

### PARTE 1C: Drow Elite Strike Team

**File:** P1C-Rituale-COMPLETO-SCALE.md

#### Drow Assassin "Veleno Nero" (CR 10)

**PROBLEMI:**
1. ❌ AC 24 troppo alto per Rogue 9 senza magic items esagerati
2. ⚠️ Death Attack DC corretto MA timing sbagliato (3 rounds study required, non immediate!)
3. ❌ Drow poison DC 18 leggermente alto (standard DC 13)

**STATBLOCK CORRETTO:**

```
**Drow Assassin "Veleno Nero"** (Drow Rogue 9)
- **CR:** 10
- **Init:** +9 (Dex +4, Improved Initiative +4, +1 racial)
- **Senses:** Darkvision 120ft, Listen +12, Spot +12

**Defense:**
- **AC:** 22 (+4 Dex, +5 armor [+2 mithral chain shirt], +2 deflection [ring], +1 dodge), touch 17, flat-footed 17 (no uncanny dodge, keeps Dex vs flat-footed)
- **HP:** 58 (9d6+18)
- **Fort:** +5, **Ref:** +12 (evasion), **Will:** +5
- **SR:** 20 (11 + 9 levels)
- **Immune:** Sleep
- **Special:** Evasion, Trap Sense +3, Uncanny Dodge

**Offense:**
- **Speed:** 40ft (8 squares, boots of striding & springing)
- **Melee:** Short sword +1 keen +12/+7 (1d6+2/17-20 + poison) + off-hand dagger +10 (1d4+1/19-20)
- **Ranged:** Hand crossbow +11 (1d4/19-20 + poison, 30ft range)
- **Space:** 5ft, **Reach:** 5ft
- **BAB:** +6, **Grapple:** +7
- **Sneak Attack:** +5d6

**Special Abilities:**
- **Death Attack (Ex):** Study target 3 full rounds (must remain within 30ft, maintain LOS), then make sneak attack → Fort DC 20 or paralyzed OR dead (assassin's choice). Paralysis 1d6+9 rounds.
- **Hide in Plain Sight (Ex):** Can use Hide skill even while observed (as long as within 10ft of shadow)
- **Poison Use (Ex):** Never risk poisoning self
- **Drow Poison:** Fort DC 13 (NOT 18!), unconscious 1 minute + 2d4 Str damage (secondary)

**Spell-Like Abilities (Sp, CL 9th):**
- 1/day: *Dancing Lights*, *Darkness*, *Faerie Fire*

**Statistics:**
- **Str:** 13 (+1), **Dex:** 20 (+5 with item), **Con:** 14 (+2), **Int:** 14 (+2), **Wis:** 10 (+0), **Cha:** 8 (-1)
- **Base Atk:** +6, **Grapple:** +7
- **Feats:** Improved Initiative, Dodge, Mobility, Weapon Finesse, Two-Weapon Fighting
- **Skills:** Balance +17, Bluff +11, Climb +13, Disable Device +14, Hide +17 (+19 in shadows), Listen +12 (+14 racial), Move Silently +17, Open Lock +17, Search +16 (+18 racial), Spot +12 (+14 racial), Tumble +17, Use Magic Device +11
```

**CORREZIONI:**
1. ✅ AC 24 → 22 (più realistico per CR 10)
2. ✅ Drow poison DC 18 → 13 (SRD standard)
3. ✅ Death Attack timing chiarito (3 rounds study required!)

---

#### Drow Clerics (Cleric 8) - Correction

**PROBLEMI:**
1. ⚠️ Spell list OK MA domains conferma (Lolth standard: Chaos, Destruction, Evil, Trickery o War)
2. ✅ AC corretto
3. ❌ SR 19 corretto

**STATBLOCK CORRETTO (minimal changes):**

```
**Drow Cleric of Lolth** (Drow Cleric 8)
- **CR:** 9
- **SR:** 19 (11 + class level)
- **Domains:** Trickery + War (confermato Lolth)
- **Turn Undead:** 5/day (CHA -1 = 4/day realistic), turn check 1d20-1, turn damage 2d6-1

**Spells Prepared:** (già corretto nel file)

**Correzione:** Solo SR 18 → 19, resto OK ✓
```

---

### PARTE 1C: Wyrmlord Lieutenant & Ogres

**File:** P1C-Rituale-COMPLETO-SCALE.md

#### Wyrmlord "Veleno d'Ombra" (Fighter 12)

**PROBLEMI:**
1. ❌ AC 26 calculation manca breakdown completo
2. ✅ HP corretto
3. ⚠️ Smite Good ability: NON standard Fighter! (Paladin/Blackguard ability)
   - Se inteso come Blackguard multiclass, specificare!

**STATBLOCK CORRETTO:**

```
**Wyrmlord Lieutenant "Veleno d'Ombra"** (Drow Fighter 10 / Blackguard 2)
- **CR:** 12
- **Type:** Humanoid (Elf) + Blackguard (Ex-Paladin fallen)

**Defense:**
- **AC:** 26 (+8 armor [dragonscale +2], +4 Dex, +2 shield [buckler +2], +2 deflection [ring]), touch 16, flat-footed 22
- **HP:** 110 (10d10+2d10+36, +12 Con, +8 Toughness)
- **Fort:** +13, **Ref:** +8, **Will:** +6
- **SR:** 23 (11 + 12 levels)
- **Immune:** Sleep, Fear (Blackguard ability)

**Offense:**
- **Speed:** 30ft (6 squares, in armor)
- **Melee:** Bastard sword +2 flaming +20/+15/+10 (1d10+8 + 1d6 fire/17-20) + off-hand short sword +1 +15 (1d6+4/19-20)
- **Ranged:** Composite longbow +16/+11/+6 (1d8+4/×3, 110ft)
- **BAB:** +12, **Grapple:** +16
- **Special:** Smite Good 1/day (+4 attack, +2 damage - Blackguard ability)

**Blackguard Abilities:**
- **Aura of Evil (Ex):** Strong (Detect Good reveals alignment)
- **Detect Good (Sp):** At-will
- **Poison Use (Ex):** No self-risk
- **Dark Blessing (Su):** CHA bonus (+1) to saves (already included Fort/Ref/Will above if applicable)

**Spell-Like Abilities (Sp, CL 12th):**
- 1/day: *Dancing Lights*, *Darkness*, *Faerie Fire*

**Statistics:**
- **Str:** 18 (+4), **Dex:** 18 (+4), **Con:** 14 (+2), **Int:** 12 (+1), **Wis:** 10 (+0), **Cha:** 12 (+1)
- **Base Atk:** +12, **Grapple:** +16
- **Feats:** Exotic Weapon Proficiency (bastard sword), Weapon Focus (bastard sword), Weapon Specialization (bastard sword), Power Attack, Cleave, Great Cleave, Combat Expertise, Improved Two-Weapon Fighting, Two-Weapon Fighting, Dodge, Mobility, Spring Attack
```

**CORREZIONI:**
1. ✅ Specified Blackguard 2 levels (explain Smite Good)
2. ✅ AC breakdown completo
3. ✅ SR 23 (not 25, was error)

---

#### Ogre Brutes (Barbarian 8) - Already Mostly Correct!

**VERIFICA SRD:**
- Ogre base: CR 3, Large Giant, 4d8+11 HD (29 HP)
- +8 Barbarian levels: CR 11 total

**STATBLOCK (già nel file, verification):**

```
**Ogre Barbarian 8**
- **CR:** 11 (4 HD ogre + 8 barb = CR 11-12 range realistic)
- **AC:** 18 (-1 size, +6 natural, +3 armor, +1 deflection, -1 Dex), touch 8, flat-footed 18
  - Durante Rage: AC 16 (-2 from rage)
- **HP:** 95 (4d8+8 HD ogre + 8d12+16 barbarian + 8 Con from rage)
- **BAB:** +11 (4 giant + 8 barb), **Grapple:** +23 (+11 BAB +8 Str +4 size)

✅ **CORRETTO!** Solo confermare:
- Rage: +4 Str, +4 Con, +2 Will, -2 AC, 10 rounds (2+Con mod barb 8 = 10 rounds)
- Fast Movement: +10ft speed (base 40ft ogre)
```

---

## CORREZIONI SUPPLEMENTO CAMPI DROW

**File:** SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md

### Campo Drow 1-3 Forze

**Drow Guerrieri (Fighter 6-8):**

**STATBLOCK STANDARD (generic CR 8):**

```
**Drow Guerriero** (Drow Fighter 7)
- **CR:** 8
- **AC:** 20 (+6 armor [mithral breastplate +1], +3 Dex, +1 deflection), touch 14, flat-footed 17
- **HP:** 52 (7d10+14)
- **Fort:** +7, **Ref:** +5, **Will:** +3
- **SR:** 18 (11+7)
- **Speed:** 30ft (no armor speed penalty with mithral)
- **Melee:** Rapier +1 +12/+7 (1d6+3/18-20 + poison) + off-hand dagger +10 (1d4+1/19-20)
- **BAB:** +7, **Grapple:** +9
- **Feats:** Weapon Focus (rapier), Weapon Finesse, Dodge, Mobility, Combat Expertise, Improved Trip, Two-Weapon Fighting
```

✅ **NOTE:** Stats file originale vicini, solo aggiungere Touch/FF AC

---

## RIEPILOGO CORREZIONI NECESSARIE

### PRIORITÀ ALTA (Breaking Mechanics):
1. ❌ **Tutti statblocks:** Add Touch AC, Flat-Footed AC
2. ❌ **Tutti statblocks:** Add explicit BAB, Grapple
3. ❌ **Treant:** Attack +20 → +16, Grapple +29
4. ❌ **Drow Assassin:** AC 24 → 22, Poison DC 18 → 13
5. ❌ **Hell Hound:** Stats aggiornati completi (AC 16, breath 10ft)
6. ❌ **Wyrmlord:** Specify Blackguard levels, SR 23

### PRIORITÀ MEDIA (Consistency):
7. ⚠️ Remove "Bonus Action" → "Swift Action" (global)
8. ⚠️ Remove "Reaction" → "Immediate Action" (global)
9. ⚠️ Verify all skill ranks ≤ HD +3 (class skill max)
10. ⚠️ Verify all feat prerequisites met

### PRIORITÀ BASSA (Fluff):
11. ✓ Spell lists verificare 3.5 compatibility (mostly OK)
12. ✓ Treasure values confermare DMG guidelines
13. ✓ CR calculations double-check

---

## FILE DA AGGIORNARE

1. **P1A-Timeline-Quest-Hellas-COMPLETA.md**
   - Drow Pyromancer complete rewrite
   - Add Touch/FF AC to ALL creatures

2. **P1B-Cerchio-Treant-COMPLETO.md**
   - Treant Corrotto major stat fixes (attacks +16, grapple +29)
   - Add Touch/FF AC

3. **P1C-Rituale-COMPLETO-SCALE.md**
   - Hell Hounds stats update
   - Drow Assassin AC/poison fix
   - Wyrmlord Blackguard clarification
   - Drow Clerics minor SR fix
   - Add Touch/FF AC ALL creatures

4. **SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md**
   - Add Touch/FF AC to generic Drow Warriors
   - Verify CR assignments

---

## TIMELINE CORREZIONI

**Tempo Stimato:** 30-45 minuti applicare fix a tutti file

**Suggerimento:** Creare VERSIONE 2 files con suffix "-3.5-CORRECTED" per mantenere originali come backup?

**Status:** ⚠️ **PRONTO PER APPLICAZIONE CORREZIONI**

*Attendere conferma procedere con update files oppure continuare Quest Tordek con regole 3.5 corrette da inizio?*
