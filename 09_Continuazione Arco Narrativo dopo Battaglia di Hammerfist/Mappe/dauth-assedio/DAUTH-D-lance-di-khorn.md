# Dauth, Carta D — Le lance di Khorn sulle mura ovest (Giorno 3)

**Dimensioni**: 21 m × 9 m (14 colonne × 6 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta D — Le lance di Khorn sulle mura ovest (Giorno 3)
COLONNE:  A B C D E F G H I J K L M N
01 🏰 🏰 🏰 🪟 🏰 🏰 🪟 🏰 🏰 🪟 🏰 🏰 🪟 🏰
02 🗼 ⬜ 🔼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🔼 ⬜ 🗼
03 ⬜ ⬜ ⬜ ⬜ ⬜ 🔵 🔵 🔵 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
04 ⬜ ⬜ ⬜ ⬜ ⬜ 🔵 🔵 🔵 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
05 ⬜ ⬜ ⬜ ⬜ ⬜ 🔵 🔵 🔵 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
06 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜

@north E
@tipo tattica abitato
@collega C02 ; fuori mappa ; il camminamento delle mura ovest non ha una griglia: la carta D è di comando, non uno scontro
@collega L02 ; fuori mappa ; il camminamento delle mura ovest non ha una griglia: la carta D è di comando, non uno scontro
@mark 1 ; G4 ; Le 150 lance di Re Thorek, al comando di Khorn Spada-di-Fuoco: asset, +2 al morale del settore
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| Luce | … | [luce/oscurità, scurovisione a X m] |
| Terreno | … | [difficile ×2, copertura +4 CA, occultamento 20%…] |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| Dauth (alleati) | Le 150 lance di Re Thorek, al comando di Khorn Spada-di-Fuoco: asset, +2 al morale del settore | 🔵 | 150 | — | F3–H5 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Il nord è a destra: in alto c'è l'ovest, il fossato e la cavalleria gnoll, fuori dalla griglia. | [effetto] |
| B | [trigger] | Non è un incontro obbligatorio: Thorik, o Tordek se è libero, decide dove mandare le lance. Lance in tempo, in ritardo o assenti: Carta D di DAY3-CITY-SIEGE e SUBQUEST-Thorik §4. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

