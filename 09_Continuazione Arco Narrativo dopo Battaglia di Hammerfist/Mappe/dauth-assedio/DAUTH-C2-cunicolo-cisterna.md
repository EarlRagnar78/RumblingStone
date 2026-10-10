# Dauth, Carta C — Il cunicolo della cisterna, sotto il chiostro

**Dimensioni**: 7,5 m × 12 m (5 colonne × 8 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta C — Il cunicolo della cisterna, sotto il chiostro
COLONNE:  A B C D E
01 🏰 🏰 🏰 🏰 🏰
02 🏰 🟤 🔼 🟤 🏰
03 🏰 🟤 💧 🟤 🏰
04 🏰 🟤 💧 🟤 🏰
05 🏰 🟢 💧 🟤 🏰
06 🏰 🟤 💧 🟢 🏰
07 🏰 🟤 🔴 🟤 🏰
08 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica interni
@collega C02 ; DAUTH-C1-chiostro-ospedale.md E06
@mark 1 ; B5 ; Violet Fungus (SRD), solo se le cisterne sono guaste (GS 3)
@mark 2 ; D6 ; Violet Fungus (SRD), solo se le cisterne sono guaste (GS 3)
@mark 3 ; C7 ; Guerriero drow (drow-fighter3-cr4), solo se le cisterne sono guaste (GS 4)
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
| Guastatori | Violet Fungus (SRD), solo se le cisterne sono guaste | 🟢 | 1 | GS 3 | B5 |
| Guastatori | Violet Fungus (SRD), solo se le cisterne sono guaste | 🟢 | 1 | GS 3 | D6 |
| Guastatori | Guerriero drow (drow-fighter3-cr4), solo se le cisterne sono guaste | 🔴 | 1 | GS 4 | C7 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Le tracce di Yssaria, se è fuggita da Dauth (SUBQUEST-Hella), stanno qui. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

