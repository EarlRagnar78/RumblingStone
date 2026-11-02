# Wyrmlord Karruk [ACCEPTED — DM-canon 2026-05-05]
**Faction**: red-hand | **Role**: melee-commander | **Environment**: battlefield | **CR**: 13 | **Source**: AP RHoD Karruk (Hill Giant barbarian) base + campaign upscale | **Status**: inferred

```statblocco
gs: 13
ca: 23
ca-dettaglio: (-1 size, +8 natural, +6 +1 breastplate)
pf: 181
pf-dado: 13d8+5d12+90
ts: Temp +17, Rifl +5, Vol +6
attributi: For 24 Des 10 Cos 20 Int 10 Sag 12 Car 10
velocita: 12 m (9 m in corazza media, +3 m movimento veloce)
iniziativa: +0
attacchi:
  - Mischia randello pesante +2 +23/+18/+13 (2d8+12)
```

> [CANONE — DM 2026-09-23, D9] correzione 3.5 da `scripts/conformita_statblocchi.py`: su decisione del DM (D9) lo statblocco è ora **fuori ira**, con i tre stati in tabella. La scheda mescolava i numeri: caratteristiche, Volontà +8, squartare e roccia erano in ira; pf, CA e il bonus di `pf-dado` fuori. Tempra +18, lotta +28, attacco +24 e danno 2d8+13 non tornavano con nessuno dei due stati. E il BAB passa da +16 a **+14**: gigante 12 DV (+9) più Barbaro 5 (+5), come dicono i tre attacchi iterativi (con +16 sarebbero quattro).


**Size/Type**: Large giant, gigante delle colline 13 DV / Barbaro 5

**Iniziativa** +0

**Difesa** **AC**: 23 (-1 size, +8 natural, +6 +1 breastplate) · **HD**: 13d8+5d12+90 (181 HP) · **Saves**: Fort +17, Ref +5, Will +6

**Attacco** **Speed**: 12 m (il gigante ha 12 m, la corazza media lo porta a 9 m, il movimento veloce del barbaro aggiunge 3 m)
**Attack**: +2 greatclub +23 melee (2d8+12)
**Full**: +2 greatclub +23/+18/+13 (2d8+12), o 2 schianti +20 (1d4+7) e squartare
**Ranged**: roccia +13 (2d6+7), 36 m

**Statistiche** **Abilities**: Str 24, Dex 10, Con 20, Int 10, Wis 12, Cha 10 · **BAB/Grapple**: +14/+25
**Feats**: Power Attack, Cleave, Great Cleave, Improved Sunder, Weapon Focus (greatclub), Intimidating Rage `[Private source — Complete Warrior]`, Leadership — sette, quanti ne danno 18 DV

**Capacità speciali**
**Special**: Rage 2/day (+4 Str/Con, +2 Will, -2 AC, 10 rounds; fatigued afterwards), rock throwing (36 m, 2d6+7), afferrare rocce, schivare prodigioso migliorato, percepire trappole +1, Red Hand command aura (+1 morale to hobgoblin 30 ft; non SRD, canone del DM 2026-10-18).
- **Squartare (Str)**: se colpisce con tutti e due gli schianti, 2d6+10. Un gigante delle colline non ha artigli: la scheda lo dava «con gli artigli»; si tiene sugli schianti come capacità speciale aggiunta (SRD, *Improving Monsters*: attacco speciale minore, +1 GS). PF1e: *rend* è una regola universale dei mostri che vuole due attacchi naturali, e gli schianti lo sono — si avvicina, non stravolge.
- **Ira intimidatoria** `[Private source — Complete Warrior]`: entrando in ira, un nemico che lo vede è scosso finché l'ira dura (Volontà nega). PF1e: il potere d'ira *intimidating glare* fa la stessa cosa con Intimidire — si avvicina.
> ⚠ Prerequisito: sette talenti chiedono 18 DV; la scheda ne contava 17. Il gigante passa da 12 a 13 DV razziali (dentro l'avanzamento SRD del gigante delle colline, 13-18 DV Grande; +1 DV non cambia il GS) e tiene così anche Comandare.

**I tre stati dell'ira** (D9, decisione del DM 2026-09-23). Lo statblocco sopra è Karruk **fuori ira**; la scheda precedente mescolava i tre stati.

| Stato | For · Des · Cos | pf | CA | Temp · Rifl · Vol | Lotta | Randello +2 | Roccia | Squartare | Iniz. |
|---|---|---|---|---|---|---|---|---|---|
| **Fuori ira** | 24 · 10 · 20 | 181 | 23 | +17 · +5 · +6 | +25 | +23/+18/+13 (2d8+12) | 2d6+7 | 2d6+10 | +0 |
| **In ira** (2/giorno, 10 round) | 28 · 10 · 24 | 217 | 21 | +19 · +5 · +8 | +27 | +25/+20/+15 (2d8+15) | 2d6+9 | 2d6+13 | +0 |
| **Affaticato**, finita l'ira | 22 · 8 · 20 | 181 | 22 | +17 · +4 · +6 | +24 | +22/+17/+12 (2d8+11) | 2d6+6 | 2d6+9 | −1 |

Affaticato: niente corsa né carica fino alla fine dell'incontro (SRD, barbaro). In ira i pf salgono di +36 (Cos +2 × 18 DV) e li perde quando l'ira finisce.

**Tattiche**
- *Prima del combattimento*: sfida il campione dei difensori in pubblico, sui gradini della breccia (Carta 13 del mazzo degli eventi della battaglia finale). Non entra in ira prima del duello: la tiene per quando il campione lo ferisce, perché l'ira intimidatoria colpisce meglio a vista.
- *Durante il combattimento*: round 1, attacco completo col randello e Attacco Poderoso a −5 se il campione ha CA sotto 25; contro un PG che brandisce Aegis Fang o un'arma magica tenta Spezzare Migliorato. Round 2, quando è ferito, entra in ira (217 pf, randello +25/+20/+15, 2d8+15) e chiunque lo veda deve resistere all'ira intimidatoria. Round 3 e seguenti, Incalzare e Incalzare Potenziato sui soldati che il campione si porta dietro. Contro chi vola o resta a distanza scaglia rocce (+13, 2d6+7). Combatte d'onore finché è in vantaggio; se perde, **bara**: sotto metà dei pf fischia al razorfiend Alfa che lo segue, e la scorta entra nel duello.
- *Morale*: sotto 60 pf, o quando l'ira finisce e lui è affaticato, ripiega verso le sue linee in sella al razorfiend (12 m, scavare): il duello resta «inconcluso» e il settore non cambia di grado. Se è circondato e non può fuggire, combatte fino alla morte; non si arrende a un nano.


Benchmark: PF T1-1 riga 13: CA 23 sotto (28) / pf 181 in linea (180; 217 in ira) / attacco +23 sopra (+22) / danno pieno ~58 sotto (60) / TS buono +17 sopra (16). Per l'SRD gigante delle colline (GS 7) + 5 livelli di barbaro associati + squartare = GS 13; la Carta 13 mette lo scontro a EL 12-14.

**Notes**: Guida assalto Rethmar Fase 1. Cavalca un razorfiend Alfa GS 13 (la scheda «Blackspawn Alfa», variante rossa: fuoco), come i Wyrmlord upscalati di `state.md`; i 2 razorfiend rossi GS 9 e i 300 hobgoblin sono la truppa del suo assalto. Dossier: `Wyrmlord_Karruk.md`.

Boost log: avanzamento di 1 DV razziale (SRD, gigante delle colline 13-18 DV) e conti rifatti — GS 10 → 13 — 17 DV non reggevano i sette talenti della scheda; pf alla media dei dadi; squartare spostato sugli schianti.

> <!-- storico -->
> era: 12d8+5d12+85 (168 pf; la media di quei dadi era 171), 202 pf in ira, velocità «40 ft» scritta senza la corazza media (che la porta a 30 ft) né il movimento veloce (+10 ft): i due si annullano, 12 m.
> era: squartare «sugli artigli» su un gigante che non ne ha; Razorfiend scritto «2 Red» qui e «Blackspawn Alfa» nel dossier.
> <!-- /storico -->
