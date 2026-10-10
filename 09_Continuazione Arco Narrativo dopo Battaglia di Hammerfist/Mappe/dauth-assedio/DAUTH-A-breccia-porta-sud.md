# Dauth, Carta A — La breccia della Porta Sud (Giorno 3)

**Dimensioni**: 18 m × 13,5 m (12 colonne × 9 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta A — La breccia della Porta Sud (Giorno 3)
COLONNE:  A B C D E F G H I J K L
01 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
02 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
03 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
04 ⬜ ⬜ ⬜ ⬜ ⬜ 🪨 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
05 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
06 🔼 ⬜ ⬜ 🪨 ⬜ ⬜ ⬜ ⬜ 🪨 ⬜ ⬜ 🔼
07 🏰 🏰 🏰 🏰 ⬜ ⬜ ⬜ 🏰 🏰 🏰 🏰 🏰
08 🏰 🏰 🏰 🏰 🪵 ⬜ 🪵 🏰 🏰 🏰 🏰 🏰
09 🟫 🟫 🟫 🟫 🔴 ⚫ 🔴 🟫 🟫 🟫 🟫 🟫

@north N
@tipo tattica abitato
@collega A06 ; fuori mappa ; il camminamento sopra la porta non ha una griglia: la carta lo dice solo «sui lati»
@collega L06 ; fuori mappa ; il camminamento sopra la porta non ha una griglia: la carta lo dice solo «sui lati»
@mark 1 ; F9 ; Comandante del Vanguard (hobgoblin-captain-cr8) (GS 8)
@mark 2 ; E9 ; Sergente hobgoblin (hobgoblin-sergente-cr5) (GS 5)
@mark 3 ; G9 ; Sergente hobgoblin (hobgoblin-sergente-cr5) (GS 5)
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🪨 Macerie | D6 | Terreno difficile; copertura +4 CA (la carta) |
| 🪨 Macerie | I6 | Terreno difficile; copertura +4 CA (la carta) |
| 🪨 Macerie | F4 | Terreno difficile; copertura +4 CA (la carta) |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| Vanguard della Mano Rossa | Comandante del Vanguard (hobgoblin-captain-cr8) | ⚫ | 1 | GS 8 | F9 |
| Vanguard della Mano Rossa | Sergente hobgoblin (hobgoblin-sergente-cr5) | 🔴 | 1 | GS 5 | E9 |
| Vanguard della Mano Rossa | Sergente hobgoblin (hobgoblin-sergente-cr5) | 🔴 | 1 | GS 5 | G9 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Il varco è l'androne, 3 quadretti (E07-G08): l'imbuto della carta. La fanteria a testuggine resta sfondo, fuori dal bordo sud. | [effetto] |
| B | [trigger] | Posta: tenere il varco finché i difensori lo rimurano, 3 round di lavoro, 1 se Thorik comanda i genieri. Esiti e Fronte: Carta A di DAY3-CITY-SIEGE. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

