# Drow Trickster Arcano — «Dita di Ragnatela» (Ladro 3 / Mago 5 / Trickster Arcano 2) [CANONE — DM 2026-09-23]
**Faction**: drow-sonjak | **Role**: caster-subdolo/saboteur | **Environment**: underdark/urban | **CR**: 11 | **Source**: SRD drow + Ladro/Mago + CdP **Trickster Arcano** (SRD) | **Status**: accepted


```statblocco
gs: 11
tipo: Medium humanoid (elf), NE
taglia: Media
spazio: 1,5 m
portata: 1,5 m
ca: 18
ca-dettaglio: (+3 Des, +4 *armatura magica*, +1 anello), contatto 14, colto alla sprovvista 15
pf: 28
pf-dado: 3d6+7d4
ts: Temp +2, Rifl +10, Vol +9
attributi: For 8 Des 16 Cos 11 Int 19 Sag 12 Car 12
velocita: 9 m
attacchi:
  - Mischia stocco perfetto +5 (1d6−1/18-20)
```


> [CANONE — DM 2026-09-23, D4] correzione 3.5 da `scripts/conformita_statblocchi.py`: **D4, deciso dal DM il 2026-09-23: BAB +5**, cioè Ladro 3 (+2), Mago 5 (+2), Trickster Arcano 2 (+1). Lotta +3 → **+4** (For 8, −1). Balestra a mano +9 torna già con +5. Lo stocco con For 8 dà +4: il +5 della scheda è di uno **stocco perfetto** (BAB +5, For −1, +1 perfetto), e il danno è 1d6−1 `[CANONE — regola, ADR-0118]`.

> `attributi` scritti a mano, non generati: serie d'élite della DMG 3.5 p. 110 più la razza drow (SRD), card del DM del 2026-11-20 (vedi il blocco storico in fondo).

Medium humanoid (elf), NE. **DV 3d6 + 7d4**. **hp 28**. **CA 18** (+3 Des, +4 *armatura magica*, +1 anello), contatto 14, colto alla sprovvista 15. Iniziativa +7. Vel 9 m.
**TS** Temp +2, Rifl +10, Vol +9 (+2 razziale vs incantesimi, +2 vs ammaliamenti). **BAB/Lotta** +5/+4. **RI 21**.
**Mischia** stocco perfetto +5 (1d6−1/18-20). **Distanza** balestra a mano +8 (1d4 + **veleno drow**, Tempra CD 13 o incosciente 1 min/2d4 ore).
**Attacco furtivo** +3d6.
**Car** For 8, Des 16, Cos 11, Int 19, Sag 12, Car 12.
**Qualità speciali** Scurovisione 36 m, cecità alla luce solare, **individuazione delle trappole**, schivare prodigioso, **prestidigitazione a distanza**.
**Capacità magiche** (1/giorno, CL 10): *luci danzanti*, *oscurità*, *fuoco fatuo*.
**Talenti** Scrivere Pergamene, Iniziativa Migliorata, Furtivo, Tiro Ravvicinato, Tiro Preciso (*Precise Shot*), Incantesimi Focalizzati (Invocazione).

**Prestidigitazione a Distanza (Str, 1/giorno)**: usa **Rapidità di Mano**, Disattivare Congegni o Scassinare Serrature **a 9 m di distanza**, come azione standard. La prova subisce +5 alla CD e provoca un attacco di opportunità se il DM lo ritiene percepibile.

**Incantesimi da Mago (CL 7; CD 10 + livello + 4)**
| Liv | Al giorno | Tipici (SRD) |
|---|---|---|
| 0 | 4 | *individuazione del magico, lettura del magico, mano magica, luce* |
| 1 | 5 | *armatura magica, dardo incantato, raggio di indebolimento, immagine silenziosa, individuazione del magico* |
| 2 | 4 | **immagine speculare**, *invisibilità*, *raggio rovente*, **polvere scintillante** (CD 16) |
| 3 | 3 | **velo di dislocamento**, **dissolvi magie**, *soffio di vento* |
| 4 | 2 | **porta dimensionale** *(o* **invisibilità superiore** *)* |

**Tattiche**: non apre mai lo scontro allo scoperto. Ordine tipico:
1. *invisibilità* + posizione a 9 m dal bersaglio designato;
2. **prestidigitazione a distanza** per **sfilare un oggetto** — non un artefatto legato (Aegis Fang e la Corona **non si possono rubare**: sono vincolati), ma **pozioni, bacchette, componenti, simboli sacri, e ciò che sta negli zaini**;
3. *raggio di indebolimento* o *raggio rovente* **con attacco furtivo** (+3d6) sul bersaglio colto alla sprovvista;
4. **dissolvi magie** mirato sulle *Ali d'Ombra* di Artemis o sull'*armatura magica* di chi vola;
5. fuga con *porta dimensionale*, mai combattendo oltre il 3° round.

> 🎯 **Aggancio di campagna (E-07b, `campaign/state.md` §7.E)**: il **Seme-Mercato di Varis** viaggia **nello zaino di Tordek**, integro e mai toccato. Un Trickster Arcano che lo sfila a 9 m di distanza è il modo più elegante di far esplodere quell'eco — e di mettere Artemis nella posizione di **dover** rincorrere Varis. *Da usare solo con l'ok del DM: cambia il ramo dell'eco.*

Notes: unità di infiltrazione della compagnia di **Sonjak**, non un ammazza-PG. Il suo valore è **portare via qualcosa** e sparire. Da schierare 1 per incontro (2 al massimo, in un colpo di mano), tipicamente in copertura dietro `drow-warrior-cr1.md`/`drow-fighter3-cr4.md` o insieme a `drow-assassina-lolth-cr10.md`. Da solo è un EL 11: contro il party è un incontro **facile in combattimento e duro in conseguenze**.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12): aggiunto **Tiro Ravvicinato**, prerequisito di Tiro Preciso; la scheda aveva 5 talenti su 6 (4 da 10 DV + 2 da mago), quindi nessun talento è stato tolto.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, lotto 2 di ADR-0126): critico di «Mischia stocco perfetto» scritto (18-20, tabella delle armi dell'SRD).

<!-- storico -->
- era: fino al 2026-11-20 For 8 Des 18 Cos 12 Int 20 Sag 12 Car 14 (acquisto a punti 36 tolta la razza), pf 38 (3d6+7d4+10), CA 19 (contatto 15), iniziativa +4, Temp +5, Rifl +11, balestra a mano +9, CD 10 + livello + 5. Rifatta con la serie d'élite della DMG 3.5 p. 110 più la razza drow (SRD), card del DM del 2026-11-20: Int 15 (+1 al 4° e all'8°), Des 14, Cos 13, Sag 12, Car 10, For 8. Incantesimi al giorno invariati: Mago 7 SRD 4/4/3/2/1 più i bonus di Int 19 dà fino a 4/5/4/3/2, la scheda ne usa meno al 4°. La nota D4 che cita «balestra a mano +9» descrive il conto di allora.
- era: fino al 2026-11-26 iniziativa +3, Temp +4, Vol +8, un incantesimo di 4° al giorno. La verifica del regolista ha rifatto i conti: iniziativa +7 (Des +3, Iniziativa Migliorata +4, che era fra i talenti e non era contata); Tempra +2 (Ladro 3 +1, Mago 5 +1, Trickster Arcano 2 +0, Cos 11 +0: nessun oggetto la alza); Volontà +9 (1 + 4 + 3, Sag +1); due incantesimi di 4° (Mago 7: uno, più uno per Int 19). Card del dm del 2026-11-26 «tutto, anche quelli già su main».
<!-- /storico -->
