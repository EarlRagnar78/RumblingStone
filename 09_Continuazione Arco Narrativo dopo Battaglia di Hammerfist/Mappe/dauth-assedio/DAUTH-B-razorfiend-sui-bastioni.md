# Dauth, Carta B — Il Razorfiend sui bastioni (Giorno 3)

**Dimensioni**: 24 m × 6 m (16 colonne × 4 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Dauth, Carta B — Il Razorfiend sui bastioni (Giorno 3)
COLONNE:  A B C D E F G H I J K L M N O P
01 🔽 ⬜ ⬜ 🔵 🔵 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🔵 🔵 ⬜ ⬜ 🔽
02 ⬜ ⬜ ⬜ ⬜ 🎯 ⬜ ⬜ ⬜ ⚫ ⬜ ⬜ 🎯 ⬜ ⬜ ⬜ ⬜
03 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
04 🧱 ⬜ 🧱 ⬜ 🧱 🔴 🧱 ⬜ 🧱 🔴 🧱 ⬜ 🧱 ⬜ 🧱 ⬜

@north N
@tipo tattica abitato
@collega A01 ; fuori mappa ; la città sotto il bastione non ha una griglia: la carta si gioca sul camminamento e in cielo
@collega P01 ; fuori mappa ; la città sotto il bastione non ha una griglia: la carta si gioca sul camminamento e in cielo
@mark 1 ; I2 ; Razorfiend rosso, in volo basso a 9 m (razorfiend-red-cr9) (GS 9)
@mark 2 ; E1 ; Serventi della balista 1
@mark 3 ; M1 ; Serventi della balista 2
@mark 4 ; F4 ; Cavalcatore gnoll col rampino, solo se il party è numeroso (gnoll-hyenodon-rider-cr4) (GS 4)
@mark 5 ; J4 ; Cavalcatore gnoll col rampino, solo se il party è numeroso (gnoll-hyenodon-rider-cr4) (GS 4)
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🎯 Balista 1 | E2 | Arma d'assedio riusabile dai PG (Artiglieria): colpo 4d6, TS Riflessi; danneggiabile (la carta) |
| 🎯 Balista 2 | L2 | Arma d'assedio riusabile dai PG (Artiglieria): colpo 4d6, TS Riflessi; danneggiabile (la carta) |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| Vanguard della Mano Rossa | Razorfiend rosso, in volo basso a 9 m (razorfiend-red-cr9) | ⚫ | 1 | GS 9 | I2 |
| Dauth | Serventi della balista 1 | 🔵 | 2 | — | D1–E1 |
| Dauth | Serventi della balista 2 | 🔵 | 2 | — | L1–M1 |
| Vanguard della Mano Rossa | Cavalcatore gnoll col rampino, solo se il party è numeroso (gnoll-hyenodon-rider-cr4) | 🔴 | 1 | GS 4 | F4 |
| Vanguard della Mano Rossa | Cavalcatore gnoll col rampino, solo se il party è numeroso (gnoll-hyenodon-rider-cr4) | 🔴 | 1 | GS 4 | J4 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Le quote della carta: camminamento, volo basso a 9 m, volo alto. La griglia è il camminamento; il Razorfiend la attraversa a passate. | [effetto] |
| B | [trigger] | Merli in riga 04 (copertura bassa, +4 CA) alternati alle feritoie aperte da cui salgono i rampini. Esiti e Fronte: Carta B di DAY3-CITY-SIEGE. | [effetto] |
| B | [trigger] | Fonte: Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

