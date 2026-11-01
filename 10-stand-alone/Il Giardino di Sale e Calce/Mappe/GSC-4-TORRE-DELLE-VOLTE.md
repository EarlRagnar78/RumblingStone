# GS-4 — La Torre delle Volte: l'officina e lo studio di Mastro Tariq (+6 m)

**Dimensioni**: 21 m × 19,5 m (14 colonne × 13 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
GS-4 — La Torre delle Volte: l'officina e lo studio di Mastro Tariq (+6 m)
COLONNE:  A B C D E F G H I J K L M N
01 🏰 🏰 🏰 🏰 🏰 🏰 🪟 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🏰 🟪 ⬜ ⬜ 🏰
03 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🏰 ⬜ ⬜ 🗄 🏰
04 🏰 🏰 🪟 ⬜ ⬜ 🔴 ⬜ ⬜ ⬜ 🔒 ⬜ 🪑 ⬜ 🏰
05 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🏰 ⬜ ⬜ 📚 🏰
06 🏰 🏰 🏰 ⬜ ⬜ ⬜ 🌫 🌫 🌫 🏰 🏰 🏰 🏰 🏰
07 🔽 ⬜ 🚪 🔵 🔵 ⬜ 🌫 🔽 🌫 ⬜ ⬜ ⬜ ⬜ 🏰
08 🏰 🏰 🏰 🔵 🔵 ⬜ 🌫 🌫 🌫 ⬜ ⬜ ⬜ ⬜ 🏰
09 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🛐 ⬜ 🏰
10 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟣 ⬜ 🏰
11 🏰 🏰 🏰 ⬜ 🧰 🔴 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🏰
12 🏰 🏰 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ 🏰
13 🏰 🏰 🏰 🏰 🏰 🏰 🪟 🏰 🏰 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica interni
@luogo Rethmar, la Grande Cisterna, dentro la Torre delle Volte
@collega A07 ; GSC-3-QUOTA-MEDIA-E-FONDO.md AB14
@collega H07 ; GSC-5-SANTUARIO-DI-SALE.md AC07
@mark 1 ; E8 ; I PG, dalla porta
@mark 2 ; L10 ; Mastro Tariq, chierico 13 di Umberlee (GS 13)
@mark 3 ; F4 ; Skum guerriero 8 (GS 10)
@mark 4 ; F11 ; Skum guerriero 8 (GS 10)
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🌫 La tromba della scala | G6 | aperta per 18 m fino al Santuario: chi ci cade o ci viene spinto (gli skum hanno Spingere Migliorato) prende 6d6 |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| PG | I PG, dalla porta | 🔵 | 4 | — | D7–E8 |
| Tariq | Mastro Tariq, chierico 13 di Umberlee (GS 13) | 🟣 | 1 | — | L10 |
| Tariq | Skum guerriero 8 (GS 10) | 🔴 | 1 | — | F4 |
| Tariq | Skum guerriero 8 (GS 10) | 🔴 | 1 | — | F11 |

- **Se la Torre non è allertata**, Tariq è allo scrittoio e gli skum ai lati della porta. **Se è allertata** (Odo ha avvisato, i ragni sono fuggiti, i chuul hanno combattuto), Tariq ha già lanciato *resistenza agli incantesimi*, *libertà di movimento*, *giusto potere* e *camminare nell'aria* (le due *veste magica* sono attive dall'alba), e aspetta dietro la tromba delle scale.
- **Round 1**: *barriera di lame* (CD 22) fra la porta e la tromba, per spezzare il gruppo; gli skum spingono chi passa verso la tromba (Spingere Migliorato). **Round 2**: *blasfemia* se almeno due PG sono a portata; altrimenti *dissolvi magie superiore* sul volatore. **Round 3+**: *ferire* sul guerriero più vicino, *colpo infuocato* sui gruppi.
- **Tariq non muore per Sal.** Sotto i 30 pf scende la scala a chiocciola con *camminare nell'aria* verso Karkator e grida il suo nome: lo scontro finale comincia con Tariq al fianco dell'aboleth. Catturarlo vivo vale la scelta 6.
- **EL 15** (Tariq GS 13 e due skum GS 10).

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B · barriera di lame | Tariq la lancia al round 1 | un muro di lame lungo 6 m fra la porta e la scala | 15d6 danni a chi lo attraversa (Riflessi CD 22 dimezza) |
| C · fuga di Tariq | Tariq sotto i 30 pf | Tariq scende nella tromba | arriva nel Santuario in 2 round e combatte accanto a Karkator: l'EL dello scontro finale sale di 1 |

> **L'officina misura 15 × 16,5 m** di pavimento, dentro mura spesse 1,5 m: fuori la Torre è 18 × 19,5 m, la stessa impronta di GS-3, e due pilastri della cisterna sono murati dentro. Ha tre piani: il fondo con le chiuse, questa officina a +6 m e il terrazzo di guardia a +12 m (non serve una griglia, ci stanno solo due skum di vedetta se la Torre è allertata).

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

