# GS-1c — Il Mercato del Ponte e il pozzo grande (ingresso C)

**Dimensioni**: 45 m × 33 m (30 colonne × 22 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
GS-1c — Il Mercato del Ponte e il pozzo grande (ingresso C)
COLONNE:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD
01 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
02 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
03 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🚪 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
04 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
05 ⬛ ⬛ ⬛ ⬜ ⬜ 📦 ⬜ ⬜ ⬜ ⬜ 📦 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 📦 ⬜ ⬜ ⬜ ⬜ 📦 ⬜ ⬜ ⬛ ⬛ ⬛
06 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
07 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⛲ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⛲ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
08 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
09 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🔴 🔴 ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
10 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧱 🧱 🧱 🧱 🧱 ⬜ ⬜ ⬜ 🔴 🔴 ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
11 ⬛ ⬛ 🚪 🟣 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧱 🕳 🕳 🕳 🧱 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
12 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧱 🕳 🔽 🕳 🧱 🏗 🟢 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
13 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧱 🕳 🕳 🕳 🧱 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
14 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧱 🧱 🧱 🧱 🧱 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
15 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🛢 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🛢 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
16 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
17 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⛲ 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 ⬜ ⬜ ⛲ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
18 ⬛ ⬛ ⬛ ⬜ ⬜ 📦 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🔵 🔵 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 📦 ⬜ ⬜ ⬛ ⬛ ⬛
19 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
20 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🚪 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
21 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
22 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛

@north N
@tipo tattica abitato
@luogo Rethmar, il foro alla testa del ponte (n. 8 e 13 della pianta)
@quota 21 m ; sopra il pavimento della Grande Cisterna, che è la quota 0 del modulo
@dislivello -3 m ; la piazza è in piano, la via della porta del ponte scende di 3 m verso il fiume
@collega O12 ; GSC-2-QUOTA-ALTA.md U13
@mark 1 ; O18 ; I quattro PG
@mark 2 ; V10 ; Uomini di Sal travestiti da facchini (guerriero 6), quattro
@mark 3 ; D11 ; Mira Serani, alla finestra sopra lo speziale (aranea)
@mark 4 ; S12 ; Guardia della gilda all'argano
@mark 5 ; O17 ; Folla in fila per l'acqua razionata (una cinquantina)
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
| PG | I quattro PG | 🔵 | 4 | — | N17–O18 |
| Sal | Uomini di Sal travestiti da facchini (guerriero 6), quattro | 🔴 | 4 | — | U9–V10 |
| Collezionista | Mira Serani, alla finestra sopra lo speziale (aranea) | 🟣 | 1 | — | D11 |
| Rethmar | Guardia della gilda all'argano | 🟢 | 1 | — | S12 |
| Rethmar | Folla in fila per l'acqua razionata (una cinquantina) | 🟢 | 50 | — | I16–T17 |

- **La piazza è piena.** Di giorno c'è la fila per l'acqua razionata: qualunque scontro qui è uno scontro davanti a cinquanta testimoni, e il Morale Cittadino lo registra (scelta 4).
- **Gli uomini di Sal** non attaccano per primi: seguono, contano, riferiscono. Attaccano solo se i PG provano a scendere di notte senza il permesso della gilda, e allora mirano all'argano: tagliare la fune con la gabbia a metà discesa (CA 14, 10 pf, durezza 2) fa cadere chi c'è dentro per 6 m sulle passerelle (2d6).
- **Mira Serani** guarda e basta. Se vede i PG scendere, il Collezionista lo sa prima di sera.

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B · scontro in piazza | i PG attaccano gli uomini di Sal o vengono attaccati | la folla scappa verso i vicoli in 1 round | Morale Cittadino −1 se muore un civile; la guardia cittadina arriva in 2d4 round e chiede conto ai PG |
| C · fune tagliata | un uomo di Sal taglia la fune dell'argano | la gabbia precipita | 2d6 danni per caduta a chi è dentro, Riflessi CD 15 per aggrapparsi alla catena di guida e dimezzare |

> **La piazza misura 36 × 24 m** fra le facciate. Il pozzo grande attraversa 6 m di volta e sbuca sopra le passerelle alte; i quattro pozzi di luce sono grate su condotti di 60 cm, troppo stretti per un Medio senza magia.

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

