# 🏔️ Terros Boss Fight — CR Analysis & Recalibration

## Analysis Context

| Factor | Value |
|---|---|
| **Party Level** | 14 (as per RICALIBRATO file header) |
| **Party Size** | 3 PCs + 1 NPC (Therysol Lv 8 Support) |
| **Active Artifact** | Corona di Adamantio (Topaz ✅, Emerald ✅ after this fight) |
| **Hella** | ❌ **NOT present** (dead, body carried, spirit only) |
| **Effective Party Strength** | ~3.5 PCs (Therysol is -4 TxC in melee, ranged/heal only) |
| **APL Calculation** | Level 14, 3 PCs = APL 14 − 1 (for 3-man) = **effective APL 13** |

---

## 1. Is CR 16 Correct? — VERDICT

> [!WARNING]
> **CR 16 is TOO HIGH for this party configuration.** A CR 16 encounter against an effective APL 13 party is EL = APL + 3, classified as **"nearly fatal"** by the DMG encounter guidelines. With Hella absent (no primary healer, no summons buffer, no divine casting), this crosses into **TPK territory**.

### The Math

| Factor | Impact |
|---|---|
| APL 13 vs CR 16 | EL = APL +3 = **Nearly Fatal** |
| No healer (Hella out) | Party sustain drops ~60% — no Cure Critical, no Heal, no restoration |
| No summons | Can't absorb boss attention with summoned creatures |
| Therysol at −4 melee | Effectively ranged support only; light crossbow + minor healing |
| Artifact synergies | Divine Trinity **IMPOSSIBLE** (needs Crown + Ring + Bracieri within 30 ft, but no 4th person to coordinate). Dark Dawn Strike still works. |
| Gravity 2x environment | Movement penalized even with Blessing; caster positioning harder |

### Recommended CR

> [!IMPORTANT]
> **Target CR: 14–15** (EL = APL +1 to +2 = "High" to "Severe"). This is the sweet spot for a dramatic, challenging boss fight that won't TPK a healer-less 3-man party. **CR 15 recommended** for "Hard Mode" feel.

---

## 2. Current Stat Block Problems (RICALIBRATO version)

| Issue | Current Value | Problem |
|---|---|---|
| **HP 380** | Way above any SRD elemental | Elder Earth Elemental (SRD) has 24d8+120 = **228 HP**. Even with 36 HD advancement the math doesn't reach 380. |
| **DR 15/—** | Overpowered | SRD Elder Earth = DR 10/—. DR 15/— makes the boss nearly impervious to Tordek (who deals ~9 per hit before DR). |
| **CA 28** | Inconsistent | File says "(−4 Taglia, +22 Naturale)" = 28, but Colossal is −8 not −4. If Huge (SRD Elder) it's −2 size. The +22 natural is way above SRD's +15 for Elder Earth. |
| **Attack +32** | Over-inflated | SRD Elder Earth (24 HD, STR 29) = +27. To get +32 you need STR 40+ which isn't justified. |
| **Damage 4d10+16** | Doubled from SRD | SRD Elder = 2d10+11. This doubles the die and ups the STR bonus. |
| **6 Lair Actions** | Action economy overload | Having Gravity Pulse, Petrification Aura, Earth Mastery, Gravità Inversa, Stalactite Rain, AND Absorb is essentially 6 special powers stacked on top of full attack. This is 5e lair action design bolted onto 3.5 — it breaks action economy. |
| **Petrification Aura DC 24** | Party-killer without healer | DEX drain → instant statue at DEX 0 = Save-or-die with no Restoration available (Hella absent!). **This ability alone can TPK the party.** |
| **Push +36** | No save escape | STR check +36 automatically pins anyone against walls. No PC can contest this. |

---

## 3. Story-Appropriate Powers for the Earth Plane

### What the Earth Plane Should Represent at This Story Point

The Earth Plane ritual is **"Anvil of the World"** — about **endurance, weight, sacrifice, and foundation**. Unlike the Fire Plane (passion, destruction, rebirth), Earth powers should feel:

- **Unyielding** — resistant, tanky, punishing for frontal assault
- **Gravitational** — the boss should control the battlefield via gravity and positioning
- **Geologic** — slow, inevitable, crushing force — not flashy, not many attacks
- **Breakable via intelligence** — sonic weakness, positioning tricks, the Cristalli Viventi help

### Recommended Power Set (4 powers, not 6)

| Power | Thematic Source | Mechanical Role |
|---|---|---|
| **Gravity Pulse** | Earth Plane = weight of mountains | Battlefield repositioning (push/pull) |
| **Earth Glide** | SRD Earth Elemental ability | Hit-and-run through walls/altar |
| **Tremor** | SRD Push + Earth Mastery | Knockdown + zone control |
| **Stalactite Rain** (recharge) | Geologic violence | AoE damage, punish ranged |

> [!TIP]
> **DROP the Petrification Aura entirely.** Without Hella to cast *Restoration* or *Stone to Flesh*, DEX drain = unrecoverable death sentence. Replace it with a thematic debuff that's strong but not permanent-save-or-die.

---

## 4. What Each Elemental Plane Could Contribute

This section answers what powers best fit the **Plane of Earth** specifically, and contrasts with what the other planes offer, so you can ensure each plane's boss feels unique.

| Plane | Thematic Core | Boss Power Signature | Example Ability |
|---|---|---|---|
| **🔥 Fire** (already done) | Passion, destruction, rebirth | Burn damage, area denial, aura of flame | Fire aura, line breath, ignite objects |
| **🏔️ Earth** (this boss) | Weight, endurance, gravity, foundations | Gravity manipulation, terrain control, DR, tremors | Gravity Pulse, Earth Glide, Tremor, Stalactite Rain |
| **💨 Air** (hypothetical) | Speed, freedom, suffocation, lightning | Whirlwind, flying superiority, lightning, vacuum zones | Whirlwind Form, Chain Lightning, Air Theft (suffocate) |
| **💧 Water** (hypothetical) | Pressure, adaptability, drowning, cold | Drowning aura, ice, pressure crush, flow control | Vortex, Pressure Cage, Ice Prison, Tidal Slam |
| **⏳ Temporal** (Part 5) | Time, entropy, paradox | Slow/haste, aging, time stop fragments | Temporal Stasis, Aging Touch, Rewind (heal self) |

### Best Powers for Earth Specifically

1. **Gravity Control** — This is THE signature. Earth Plane = weight of the world. Terros should be able to change gravity direction and intensity. This forces tactical movement.
2. **Earth Glide** — SRD canonical. Makes the boss feel like fighting the mountain itself — it can disappear into stone and emerge anywhere.
3. **Seismic Tremor** — Knockdown + stun. Punishes standing on solid ground (creates tension: stand on Altar = Earth Mastery bonus for boss, but also where you take Tremor).
4. **Regeneration on contact with stone** — Rewards the party for keeping boss airborne (tactical puzzle, not just DPS race).

> [!NOTE]
> The current file gives Terros "Volare 18m (perfetta)" which contradicts Earth Elemental flavor. Earth Elementals CANNOT FLY per SRD. In zero-G he should be able to push off surfaces and Earth Glide through stone, but not fly freely. This makes him vulnerable when knocked into open zero-G space — a tactical lever for the party.

---

## 5. TERROS L'ANTICO — Complete Recalibrated Stat Block (CR 15)

### Design Philosophy

- **Base creature**: Elder Earth Elemental (24 HD) **advanced to 30 HD** for CR 15
- **Thematic adjustments**: Custom Lair Actions (max 3, using SRD action economy)
- **Removals**: No Petrification Aura (party-killing without healer), no free fly speed
- **Additions**: Gravity Pulse and Stalactite Rain as limited-use powers via SRD's "1/1d4 rounds" mechanic
- **Sonic vulnerability preserved**: Keeps the Cristalli Viventi reward meaningful

---

```
============================================================
   TERROS L'ANTICO — L'Incudine del Mondo
   Elementale della Terra Avanzato (Guardiano)
============================================================

Tipo:         Elementale (Terra, Extraplanare)
Taglia:       Enorme (Huge) — 4.5m × 4.5m, altezza 6m
               (Non Colossale — mantiene Huge per bilancio)
Allineamento: Neutrale
CR:           15

------------------------------------------------------------
STATISTICHE BASE
------------------------------------------------------------
Dadi Vita:    30d8 + 210 (HP 345)
              (30 HD × d8 = 135 avg, CON +7 × 30 = 210, tot = 345)

Iniziativa:   −1 (DES 8)
Velocità:     6m (20 ft); Earth Glide 6m (attraverso pietra)
              ** NON può volare — in zero-G si muove spingendosi
                 da superfici (Move action, DC 10 Balance) **

CA:           26 (−2 taglia, +18 armatura naturale), 
              touch 8, flat-footed 26

BAB/Lotta:    +22 / +40  
              (BAB +22 [Outsider/Elemental full BAB for 30 HD],
               +10 STR, +2 size = Grapple +40... 
               Wait — Huge is +2 grapple. Let me recalc.
               Actually Elemental BAB = ¾ HD per SRD.
               BAB = 30 × ¾ = +22. Grapple = +22 BAB +10 STR 
               +8 size (Huge) = +40 ✓)

Attacchi:
  Schianto:   +30 mischia (2d10+10, crit 19-20/×2)
              (+22 BAB +10 STR −2 size = +30)
  Full Attack: 2 schianti +30/+30 (2d10+10 ciascuno)
  
  Lancio Roccia (distanza 60 ft): +19 (2d8+10)
              (+22 BAB −2 size −1 DEX = +19)

Portata:      4.5m (15 ft)

------------------------------------------------------------
CARATTERISTICHE
------------------------------------------------------------
  FOR 31 (+10)   |   DES  8 (−1)   |   COS 25 (+7)
  INT 10 (+0)   |   SAG 15 (+2)   |   CAR 11 (+0)

------------------------------------------------------------
TIRI SALVEZZA
------------------------------------------------------------
  Tempra: +24  (base +17 [30 HD good] + COS +7)
  Riflessi: +9  (base +10 [30 HD poor]... 
             Actually Elemental: Fort/Ref vary by subtype.
             Earth: Good save = Fort. Ref = poor, Will = poor.
             Fort: +17 +7 = +24 ✓
             Ref: +10 −1 = +9
             Will: +10 +2 = +12)
  Volontà: +12  (base +10 + WIS +2)

------------------------------------------------------------
QUALITÀ SPECIALI (Difensive)
------------------------------------------------------------
• DR 10/—  (SRD standard per Elder Earth)
• Immunità: Acido, Veleno, Sonno, Paralisi, Stun, Critici,
            Flanking (Elementale), effetti di forma
• Debolezza: SONICO — danni sonori ×1.5
             (La Frequenza dei Cristalli Viventi infligge
              danni sonici bonus!)
• Darkvision 60 ft
• Percezione Tremore (Tremorsense) 60 ft

------------------------------------------------------------
ATTACCHI SPECIALI
------------------------------------------------------------
1. EARTH MASTERY (Ex) — COSTANTE
   +1 attacco e danni vs bersagli che toccano terra/pietra.
   −4 attacco e danni vs bersagli in aria/volo.
   * L'Altare conta come "terra." Stare sull'Altare = 
     Earth Mastery bonus per Terros ma anche stabilità per PG.
     Tattica: PG devono decidere tra stabilità (Altare) 
     e evitare il bonus del boss (zero-G). *

2. PUSH (Ex) — ad ogni schianto
   Ogni colpo riuscito: bersaglio TS Forza CD 25 o spinto
   3m indietro. Se in zero-G = sbatte contro muro (2d6).
   (CD = 10 + ½ HD + STR mod = 10 + 15 + 10 = 35... 
    troppo alto! Aggiustiamo a CD 25 per bilancio giocabile.
    Thorik con FOR ~18 = +4, serve 21 = difficile ma possibile.)

3. EARTH GLIDE (Ex) — movimento
   Passa attraverso pietra/terra come un pesce nell'acqua.
   Non lascia tunnel. Move Earth lo stordisce (Fort DC 15).
   * Tattica: Terros entra nell'Altare di mithral, emerge
     alle spalle del caster. Usare Ready Actions per 
     colpirlo quando emerge! *

------------------------------------------------------------
LAIR ACTIONS (Azioni del Covo) — MAX 1 PER ROUND
------------------------------------------------------------
Terros usa UNA Lair Action per round all'iniziativa 20.
Queste SOSTITUISCONO il turno di iniziativa 20, non si 
sommano al suo turno normale.

A. GRAVITY PULSE (Pulsazione Gravitazionale)
   Ricarica: Ogni 1d4 round (dopo l'uso)
   Effetto: Terros sceglie una direzione. La gravità nella 
            camera cambia in quella direzione per 1 round.
   Meccanica: Tutti i PG "cadono" 9m (30 ft) in quella 
              direzione. TS Riflessi CD 22 o schianto contro
              superficie = 4d6 contundenti + prono.
              (CD = 10 + ½ Lair CR + COS = 10 + 7 + 7 = 24,
               ridotto a 22 per bilancio senza healer)
   
   * Momento tattico: Se spinti FUORI dall'Altare, i PG
     perdono stabilità e devono trovare modo di tornare.
     Tordek (Monk speed + Jump +10) migliore per rientrare.
     Thorik usa Aegis Fang Returning come gancio.
     Artemis vola (Wings of Shadow dal Ring). *

B. PIOGGIA DI STALATTITI (Stalactite Rain)
   Ricarica: 5-6 su d6
   Effetto: Esplosione di frammenti di pietra dalla camera.
   Meccanica: Area 9m (30 ft) raggio, centrata su un punto
              a scelta. 8d6 contundenti + perforanti.
              TS Riflessi CD 22 dimezza.
   
   * Punisce raggruppamento. Forza dispersione.
     Artemis in volo è bersaglio privilegiato ma può 
     Shadow Step per evitare. *

C. TREMORE DEL FORGIATORE (Tremor)  
   Ricarica: Ogni 1d3 round
   Effetto: Terros colpisce l'Altare (se lo tocca) o una 
            superficie. Onda sismica.
   Meccanica: Tutti entro 6m su superficie solida:
              TS Riflessi CD 22 o cadere proni + 2d6.
              Chi è in zero-G: NON influenzato (vantaggio 
              posizionale del volo).
   
   * Sinergia: Earth Mastery dà bonus vs chi tocca terra,
     E Tremor punisce chi sta a terra. Il boss VUOLE che 
     i PG stiano a terra (Earth Mastery +1) ma anche li 
     punisce (Tremor). Dilemma tattico elegante. *

------------------------------------------------------------
RIGENERAZIONE TERRESTRE (Su) — PASSIVA
------------------------------------------------------------
Se Terros è in contatto con l'Altare o una superficie di 
pietra: rigenera 15 HP per round.

* CONTROMISURA: I PG devono tenerlo IN ARIA (zero-G) o
  staccarlo dalla pietra. Metodi:
  - Tordek: Pugno Frana spinge indietro (Bracieri Earth)
  - Thorik: Bull Rush / Push con Aegis Fang
  - Artemis: Eldritch Blast knockback (se invocazione scelta)
  - Diapason Armonico (se ottenuto dalla Skill Challenge): 
    Stun 1 round, cade in zero-G *

------------------------------------------------------------
TALENTI (11 talenti per 30 HD)
------------------------------------------------------------
1. Attacco Poderoso (Power Attack)
2. Incalzare (Cleave)  
3. Fendente Poderoso (Great Cleave)
4. Spinta Migliorata (Improved Bull Rush)
5. Critico Migliorato — schianto (Improved Critical)
6. Spaccare Migliorato (Improved Sunder)
7. Volontà di Ferro (Iron Will)
8. Colpo Terrificante (Awesome Blow)
9. Allerta (Alertness)
10. Robustezza (Toughness)
11. Resistenza Epica — non standard, replace with 
    Arma Focalizzata (Weapon Focus — slam)

------------------------------------------------------------
ABILITÀ
------------------------------------------------------------
Listen +20, Spot +20, Intimidate +15

------------------------------------------------------------
TATTICHE (Round-by-Round)
------------------------------------------------------------
Round 1: Gravity Pulse (init 20) verso soffitto per 
         separare party dall'Altare. Poi carica Thorik
         con 2 schianti (tank = minaccia primaria).

Round 2: Earth Glide nell'Altare. Emerge dietro Artemis 
         (attacco sorpresa, ready action dei PG lo ferma
         se preparati). Rigenera 15 HP se tocca Altare.

Round 3: Se PG dispersi in zero-G, usa Stalactite Rain su
         gruppo più numeroso. Se PG concentrati sull'Altare,
         usa Tremor.

Round 4+: Alterna Earth Glide hit-and-run con Gravity Pulse.
          Se HP < 50%, combatte sulla difensiva sull'Altare
          (rigenerando) forzando i PG ad avvicinarsi.

Mai fugge. Guardiano fino alla morte.

============================================================
```

---

## 6. Encounter Budget Verification (CR 15 vs 3 PCs Lv 14)

| Metric | Value | Status |
|---|---|---|
| **Party APL** | 14 (3 PCs) → adjusted APL 13 (−1 for 3 PCs) | — |
| **Boss CR** | 15 | — |
| **EL** | APL + 2 = **Severe** | ✅ Right difficulty for "Hard Mode" |
| **XP Award** (CR 15, EL 15 for 3 PCs) | ~5,400 XP per PC | Fair |
| **Expected rounds** | 4–6 | ✅ Epic feel, not slog |
| **TPK Risk** | Low-Moderate (no save-or-die abilities) | ✅ |
| **Resource drain** | High (HP, charges, Ring uses) | ✅ Sets up tense ritual |

### DPR Analysis (Party vs Boss)

| PC | Avg Damage/Round vs AC 26 | Notes |
|---|---|---|
| **Thorik** (Aegis Fang +21 mischia vs AC 26) | ~22 after DR 10 | Needs 5+ to hit. 1d10+7+3d6 sacred = ~28, minus DR 10 = ~18 |
| **Tordek** (Flurry +12/+12/+7/+2 vs AC 26) | ~12 after DR 10 | Bracieri fire/earth damage helps bypass DR somewhat. Jump charge helps. DR 10 brutal vs monk. |
| **Artemis** (Eldritch Blast +16 touch vs Touch 8) | ~38 (auto-hits touch) | 8d6+1d6 fire+1d6 cold = ~33. If sonic mode: ×1.5 = ~49! **Star damage dealer this fight.** |
| **Therysol** (crossbow) | ~5 | Token contribution |
| **Combined party DPR** | ~77/round | ✅ Boss (345 HP) dies in ~4.5 rounds |

### Boss DPR vs Party

| Target | Boss Avg Damage/Round | Lethal? |
|---|---|---|
| **Thorik** (AC ~28 with Corona) | 2 slams auto-hit = 2×(2d10+10) = ~42/round + push | Thorik ~145 HP = ~3.5 rounds to kill. **Manageable.** |
| **Tordek** (AC ~27 Monk) | Similar, but Push knocks into zero-G | Tordek ~80 HP = ~2 rounds. **Dangerous without healing.** |
| **Artemis** (AC ~16, flying) | Earth Mastery −4 penalty vs airborne = rarely hits | Artemis safe in air, but Stalactite Rain threatens. |

> [!TIP]
> **Key balance lever**: Artemis with Wings of Shadow is nearly untouchable (Earth Mastery gives boss −4 vs airborne). This is INTENTIONAL — it rewards smart Ring usage and makes Artemis the star DPS while Earth specialist Terros focuses the dwarves touching ground.

---

## 7. Sonic Vulnerability — The Skill Challenge Reward That Matters

The Cristalli Viventi skill challenge rewards (from the COMPLETO version) remain critical:

| Reward | Mechanical Impact |
|---|---|
| **Frequenza Confusione** | Round 1: Terros −4 attack/AC (nauseated). Huge opener. |
| **Diapason Armonico** (Critical Success) | 1-time stun, no save. Can break Regeneration cycle by forcing boss off Altar. |
| **Sonic Vulnerability** (inherent) | Artemis sonic-tuned Eldritch Blast = ~49 DPR. This is the designed "kill combo." |

---

## 8. Summary of Changes from Current RICALIBRATO

| Aspect | Current (RICALIBRATO) | Proposed (CR 15) | Reason |
|---|---|---|---|
| CR | 16 | **15** | APL+2 = Severe (better for 3-man no-healer) |
| HP | 380 | **345** | 30 HD × d8 + CON 7 × 30 = SRD-legal |
| CA | 28 | **26** | Huge (−2) + Natural 18 = balanced hittable |
| DR | 15/— | **10/—** | SRD standard, doesn't annihilate Tordek |
| Attack | +32 | **+30** | SRD math: BAB 22 + STR 10 − size 2 |
| Damage | 4d10+16 | **2d10+10** | SRD Earth Elemental scaling |
| Fly | 18m perfect | **None** (Earth Glide + push off walls) | SRD: Earth Elementals don't fly |
| Lair Actions | 6 total | **3 rotating** (1/round at init 20) | Prevents action economy overload |
| Petrification Aura | DC 24 DEX drain | **REMOVED** | Unrecoverable without Hella's Restoration |
| Push DC | 36 (impossible) | **25** (hard but possible) | Thorik can contest with STR + Blessing |
| Regeneration | 20 HP/round | **15 HP/round** | Still forces tactical play, not unbeatable |
| Stalactite Rain | 10d6 | **8d6** | Slightly reduced to account for no AoE healing |

---
