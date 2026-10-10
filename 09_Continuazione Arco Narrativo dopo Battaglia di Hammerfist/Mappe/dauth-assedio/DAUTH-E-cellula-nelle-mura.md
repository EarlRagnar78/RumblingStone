# Dauth, Carta E — La cellula nelle mura: corpo di guardia e poterna

**Dimensioni**: 12 m × 12 m (8 colonne × 8 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta E — La cellula nelle mura: corpo di guardia e poterna
COLONNE:  A B C D E F G H
01 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02 🏰 🛏 ⬜ ⬜ 🔼 🏰 🔻 🏰
03 🏰 ⬜ 🪑 ⬜ ⬜ 🏰 ⬜ 🏰
04 🏰 ⬜ ⬜ ⬜ 🪓 🏰 ⬜ 🏰
05 🏰 🏰 🚪 🏰 🏰 🏰 ⬜ 🏰
06 🔒 🔴 🔴 🔴 ⬜ ⬜ ⬜ 🏰
07 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
08 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica interni
@collega G02 ; fuori mappa ; dove porta la botola la carta non lo dice [INFERRED — needs DM confirmation]
@collega E02 ; fuori mappa ; il camminamento nord, da cui si sente raspare, non ha una griglia
@mark 1 ; B6 ; Sabotatore con la chiave (Ladro 7) [INFERRED — needs DM confirmation]
@mark 2 ; D6 ; Guerriero drow (drow-fighter3-cr4); in alternativa un deathlock-cr8 (GS 4)
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
| Guastatori | Sabotatore con la chiave (Ladro 7) [INFERRED — needs DM confirmation] | 🔴 | 1 | — | B6 |
| Guastatori | Guerriero drow (drow-fighter3-cr4); in alternativa un deathlock-cr8 | 🔴 | 2 | GS 4 | C6–D6 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Se Artemis ha il patto GRAY-A, la cellula del Mascherato le indica la poterna: +2 alle prove per intercettarli. Con DARK nessun aiuto. | [effetto] |
| B | [trigger] | Se la poterna si apre, la cavalleria gnoll entra nel quartiere ovest. Esiti e Fronte: Carta E di DAY3-CITY-SIEGE. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

