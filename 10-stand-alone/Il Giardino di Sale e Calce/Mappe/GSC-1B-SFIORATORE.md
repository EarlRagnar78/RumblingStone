# GS-1b — Lo sfioratore calishita sotto la riva del Cannath (ingresso B, nascosto)

**Dimensioni**: 39 m × 21 m (26 colonne × 14 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
GS-1b — Lo sfioratore calishita sotto la riva del Cannath (ingresso B, nascosto)
COLONNE:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
01 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
03 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
04 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 💧 💧 💧 💧 💧 💧 💧 🏰
05 🌊 🌊 🌊 🌊 🌊 ⛓ 🟤 🟤 🟤 🟤 🟤 🟤 🟤 🟤 🟤 🟤 🟤 🟤 💧 💧 💧 🟤 🟤 🟤 🧰 🏰
06 🌊 🌊 🔵 🔵 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 💧 💧 💧 🟤 🟤 🟤 🟤 🏰
07 🌊 🌊 🔵 🔵 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 💧 💧 💧 🟤 🔽 🟣 🟣 🏰
08 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 💧 💧 💧 🟤 🟤 🟣 🟣 🏰
09 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 💧 💧 💧 🟤 🟤 🕯 🟤 🏰
10 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 💧 💧 💧 💧 💧 💧 💧 🏰
11 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 💧 💧 💧 💧 💧 💧 💧 🏰
12 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
13 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
14 🌊 🌊 🌊 🌊 🌊 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica caverna
@luogo Rethmar, riva sud del Cannath, a valle del Ponte (n. 7 della pianta)
@collega W07 ; GSC-6-GALLERIA-DI-DRENAGGIO.md AM08
@mark 1 ; D7 ; I quattro PG, arrivati dal fiume
@mark 2 ; Y8 ; Pattuglia drow di passaggio (2 esploratori, ranger 6), solo con il clock di Sonjak a 5 o più
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🌊 La corrente del Cannath | B3 | acqua agitata: Nuotare CD 15 per tenersi; con un fallimento di 5 o più la corrente porta via 6 m verso valle |
| 🌊 Corrente rovesciata | K7 | si cammina con l'acqua alla cintura a metà velocità; chi cade va trascinato 3 m verso il fiume a round (Forza CD 12 per fermarsi). La corrente esce perché Tariq fa sfogare la cisterna: è l'acqua che manca alla città |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| PG | I quattro PG, arrivati dal fiume | 🔵 | 4 | — | C6–D7 |
| Sonjak | Pattuglia drow di passaggio (2 esploratori, ranger 6), solo con il clock di Sonjak a 5 o più | 🟣 | 2 | — | X7–Y8 |

- **Lo sfioratore si scopre, non si trova per caso** (vedi gli indizi nel capitolo «Gli ingressi»). Senza indizio, dal fiume si vede solo il pilone.
- **I drow non combattono qui.** Se il clock di Sonjak è a 5 o più, due esploratori stanno chiudendo la paratoia; al primo segno dei PG fuggono nella galleria e avvisano il campo sotto la linea di Rethmar. Catturarne uno vale l'indizio della scelta 12.
- **Indizi sulla banchina**: Sopravvivenza CD 18 mostra impronte di piedi palmati (skum) e di stivali morbidi (drow) che vanno nella stessa direzione; Cercare CD 20 trova un gettone d'osso con il ragno di Sonjak.

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B · paratoia chiusa | i PG chiudono la paratoia con l'argano (Forza CD 18, 2 round) | la corrente del canale si ferma | la cisterna smette di sfogare: in tre giorni l'acqua della città torna a salire (scelta 9). Tariq se ne accorge in 1 ora |

> **Il canale è lungo 22,5 m** in pianta, ma l'intero sfioratore dal fiume alla galleria è lungo 60 m: quello che conta è la camera della paratoia, dove i PG decidono se chiuderla.

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

