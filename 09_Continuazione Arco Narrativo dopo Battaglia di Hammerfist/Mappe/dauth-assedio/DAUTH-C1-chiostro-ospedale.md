# Dauth, Carta C — Il chiostro-ospedale (Giorno 3)

**Dimensioni**: 15 m × 15 m (10 colonne × 10 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta C — Il chiostro-ospedale (Giorno 3)
COLONNE:  A B C D E F G H I J
01 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02 🏰 🛏 ⬜ ⬜ ⬜ 🔵 ⬜ ⬜ 🛏 🏰
03 🏰 🛏 ⬜ 🟪 ⬜ ⬜ 🟪 ⬜ 🛏 🏰
04 🏰 🛏 ⬜ 🌿 🌿 🌿 🌿 ⬜ 🛏 🏰
05 🏰 🛏 ⬜ 🌿 🌿 🌿 🌿 ⬜ 🛏 🚪
06 🏰 🛏 ⬜ 🌿 🔽 ⛲ 🌿 ⬜ 🛏 🏰
07 🏰 🛏 ⬜ 🌿 🌿 🌿 🌿 ⬜ 🛏 🏰
08 🏰 🛏 ⬜ 🟪 ⬜ ⬜ 🟪 ⬜ 🛏 🏰
09 🏰 🛏 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🛏 🏰
10 🏰 🏰 🏰 🏰 🚪 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica interni
@collega E06 ; DAUTH-C2-cunicolo-cisterna.md C02
@mark 1 ; F2 ; Il chierico che ferma Hella, e i feriti
@zone B2-B9 ; Barelle
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🛏 Barelle | B2–B9 | Terreno ingombro (la carta) [INFERRED — needs DM confirmation: costa doppio come il terreno difficile] |
| 🛏 Giaciglio | I2–I9 | Terreno ingombro (la carta) [INFERRED — needs DM confirmation: costa doppio come il terreno difficile] |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| Dauth | Il chierico che ferma Hella, e i feriti | 🔵 | 1 | — | F2 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Cisterne salve: nessun nemico, è uno skill challenge di triage (Guarire o Concentrazione CD 16-20). Cisterne guaste: i guastatori escono dal cunicolo (mappa C2) per la scala in E06. | [effetto] |
| B | [trigger] | Esiti e Fronte: Carta C di DAY3-CITY-SIEGE, legata a SUBQUEST-Hella. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

