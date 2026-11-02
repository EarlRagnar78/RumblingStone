# Ushgar «Occhio Reso» — Capo-guerra degli ausiliari orcheschi (Orco, Barbaro 13) [ACCEPTED — DM-canon]
**Faction**: mano-rossa (ausiliari orcheschi) | **Role**: mini-boss melee/politico | **Environment**: hills/underground | **CR**: 13 | **Source**: SRD *Orc* + Barbaro 13 (SRD PHB); culto di Gruumsh da `skills/forgotten-realms-lore/references/fr-deities-complete.md` | **Status**: accepted


```statblocco
gs: 13
tipo: Medium humanoid (orc), CE
ca: 21
ca-dettaglio: (+7 cotta di maglia +2, +2 Des, +1 anello, +1 armatura naturale), contatto 13, colto alla sprovvista 19
pf: 140
pf-dado: 13d12+55
ts: Temp +14, Rifl +8, Vol +8
attributi: For 22 Des 14 Cos 18 Int 6 Sag 10 Car 6
velocita: 15 m (movimento veloce, stivali degli scatti e dei salti)
attacchi:
  - Mischia ascia bipenne +1 +20/+15/+10 (1d12+10/×3)
```

> [GENERATO] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

**Iniziativa** +6 · **Sensi** scurovisione 18 m; Osservare e Cercare −2 (Occhio Reso)

**Difesa** CA 21 (+7 cotta di maglia +2, +2 Des, +1 anello, +1 armatura naturale), contatto 13, colto alla sprovvista 19 · **pf 140** (DV 13d12) · **TS** Temp +14, Rifl +8, Vol +8 (mantello di resistenza +2 incluso) · **RD 3/—**; schivare prodigioso migliorato, intuizione delle trappole +4 · **Debolezza** sensibilità alla luce

**Attacco** Vel 15 m (movimento veloce, stivali degli scatti e dei salti) · **Mischia** ascia bipenne +1 **+20/+15/+10** (1d12+10/×3) · **Attacchi speciali** ira furente 4/giorno

**Statistiche** For 22, Des 14, Cos 18, Int 6, Sag 10, Car 6 · **BAB/Lotta** +13/+19 · **Talenti** Attacco Poderoso, Robustezza, Volontà di Ferro, Iniziativa Migliorata, **Combattere alla Cieca** · **Qualità speciali** movimento veloce · **Equipaggiamento** ascia bipenne +1, cotta di maglia +2, anello di protezione +1, amuleto dell'armatura naturale +1, mantello di resistenza +2, stivali degli scatti e dei salti, 2 pozioni di *cura ferite critiche*

**Capacità speciali**
- **Ira furente (4/giorno, 10 round)**: For 28, Cos 24 → **hp 179**, ascia **+23/+18/+13 (1d12+14)**, **CA 19**, Temp +17, Vol +11.
- **Occhio Reso**: si è cavato l'occhio destro da solo, davanti ai suoi, come offerta a Gruumsh. **−2 a Osservare e Cercare** in permanenza — e **Combattere alla Cieca**, che è il modo in cui ha imparato a non pagarlo. Buio, fumo, *oscurità* drow, invisibilità: perde metà dei malus che chiunque altro subirebbe.
- **Sensibilità alla luce**: abbagliato in piena luce solare (−1 ai tiri per colpire). Combatte all'alba e al crepuscolo per scelta, mai a mezzogiorno.

**Tattiche**
- *Prima del combattimento*: entra **già in ira**.
- *Durante il combattimento*: punta l'incantatore e non cambia bersaglio. Con gli stivali copre 30 m in una carica e arriva addosso al round 1 — è tutto il suo piano, e contro un gruppo abituato ad avere un round di preparazione funziona una volta. Con Attacco Poderoso a −5 fa **1d12+24** a colpo contro le CA che riesce a bucare.
- *Morale*: se scende sotto ~40 pf beve, se scende di nuovo **non fugge**: Gruumsh non contempla la ritirata, e questo è un dato tattico, non di colore.

**Benchmark PF T1-1 riga 13 (CA 28, 180 pf, att. +22, danno 60, CD 21)**: attacco **+23** ✓ (sopra), danno con attacco completo in ira **≈61** ✓, **CA 21 → 19 in ira** ✗ (molto sotto), **pf 140 → 179 in ira** ≈ (sotto/in scala). Traduzione onesta: **colpisce come un GS 13 e sopravvive come un GS 11**. Contro CA ~30 e quattro PG di livello 13 dura **2-3 round**. Va usato **con corpi intorno** (`chierico-gruumsh-cr11.md` dietro, `bruto-deforme-sottosuolo-cr11.md` a fianco) o come **secondo tempo** di uno scontro già cominciato, mai come boss solitario di fine arco.

**Combinazioni (EL già calcolati)**
| Incontro | EL | Riga di taratura |
|---|---|---|
| Ushgar + Chierico di Gruumsh + Bruto Deforme | **15,0** | APL+2 — set-piece dell'ala orchesca |
| Ushgar + Chierico di Gruumsh | **14,2** | APL+1 — scontro standard d'arco |
| Ushgar da solo | **13,0** | mini-boss, 2-3 round |
| Ushgar + Ghaurush | **16,9** | tetto APL+4 — solo se il DM vuole chiudere l'ala orchesca in una scena sola |

Notes: comanda una parte dei **1.800 ausiliari orcheschi** della Mano Rossa (`campaign/state.md` §2.2). Non adora Tiamat e non finge di farlo: dossier e ramo politico in `Ushgar_Occhio_Reso.md` (questa cartella). Rivale naturale del **Generale Grimjaw** (Orog, `campaign/ai-media-prompts/09_ARC08_battaglia-hammerfist.md`), che è orco quanto lui e ha scelto la parte opposta della faglia.

Boost log: creato a GS 13 come personaggio classato (SRD *Orc* + Barbaro 13, classe da PG ⇒ GS = livello). Nessun template applicato. Benchmark PF T1-1 GS 13 dichiarato sopra: sopra su attacco/danno, sotto su CA/pf — mitigazione per composizione dell'incontro, non per ritocco dei numeri.

> **Conti rifatti sul SRD**: la scheda scriveva «giaco di maglia +2» ma contava +7 all'armatura, che è la **cotta di maglia** +2 (armatura media, Des massima +2: il movimento veloce vale ancora). Si tiene la CA 21 e cambia il nome dell'armatura. Gli stivali degli scatti e dei salti danno +3 m alla velocità: 15 m, 30 m in carica. Il Barbaro 13 ha **RD 3/—** (2/— è del 10°), e l'ira furente dura 3 + mod Cos in ira (24 → +7) = **10 round**, non 11. `pf-dado` con la Cos e Robustezza: 13d12 + 52 + 3.

Boost log: correzione dei conti sul SRD — GS 13 → 13 — RD 3/— al 13°, velocità 15 m con gli stivali che la scheda già portava, ira di 10 round; la CA 21 resta, con la cotta di maglia al posto del giaco.

<!-- storico -->
era: armatura «giaco di maglia +2» contata +7, da questa scheda (ADR-0091).
era: velocità 12 m e carica di 24 m, senza gli stivali nel conto, da questa scheda.
era: RD 2/— e ira furente di 11 round, da questa scheda.
era: `pf-dado` 13d12, senza Cos né Robustezza, da questa scheda.
era: il primo Boost log portava la data di creazione, 2026-08-02, e il Benchmark la riga 13 trascritta a memoria (att. +21, danno 61).
<!-- /storico -->
