# QM-3 — La Grande Cisterna, quota media (+6 m) e fondo: ponte maestro, navate, vasca

**Dimensioni**: 60 m × 40,5 m (40 colonne × 27 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
QM-3 — La Grande Cisterna, quota media (+6 m) e fondo: ponte maestro, navate, vasca
COLONNE:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL AM AN
01 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02 🏰 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🏰
03 🏰 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🧰 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🏰
04 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
05 🏰 🔼 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
06 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
07 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 💧 💧 💧 💧 💧 💧 💧 💧 🔴 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
08 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 💧 💧 💧 💧 💧 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
09 🏰 🌉 💧 💧 💧 🟪 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟪 💧 💧 💧 💧 🌉 💧 💧 💧 💧 🟪 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
10 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🌉 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
11 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🌉 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
12 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🌉 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
13 🏰 🌉 🔵 🔵 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🌉 🟦 🟦 🟦 🟦 🟦 🪜 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
14 🏰 🔼 🔵 🔵 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🌉 🔼 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
15 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🪜 💧 🟦 🟦 🟦 🟦 🟦 🟦 🔽 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
16 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
17 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
18 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
19 🏰 🌉 💧 💧 💧 🟪 💧 💧 💧 🔴 💧 💧 💧 💧 💧 🟪 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟪 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
20 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🟢 🟢 🟢 🟢 🟢 🟢 💧 💧 💧 💧 💧 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰
21 🏰 🌉 💧 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 💧 💧 💧 💧 💧 🟢 🟢 🟢 🟢 🟢 🟢 💧 💧 💧 💧 💧 💧 🔴 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
22 🏰 🌉 💧 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 💧 💧 💧 💧 💧 🟢 🟢 🟢 🟢 🟢 🟢 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
23 🏰 🌉 💧 🟨 🟨 🟨 🟨 💧 🟨 🟨 🟨 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🔼 🏰
24 🏰 🌉 💧 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
25 🏰 🌉 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🌉 🏰
26 🏰 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 💧 🏰
27 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰

@north N
@tipo tattica interni
@luogo Qasr al-Milah, la Grande Cisterna di Tufo sotto la piazza del Pozzo dei Sospiri
@collega AB14 ; QM-4-TORRE-DELLE-VOLTE.md A07
@collega B05 ; QM-2-QUOTA-ALTA.md B05
@collega AM23 ; QM-2-QUOTA-ALTA.md AM23
@collega B14 ; fuori mappa ; murata da tre mesi: abbatterla (durezza 8, 90 pf) fa rumore e allerta la Torre
@collega U15 ; QM-5-SANTUARIO-DI-SALE.md Q04
@taglia J19 ; Enorme
@taglia AC21 ; Enorme
@taglia AD7 ; Enorme
@mark 1 ; D14 ; I PG, dal ponte ovest o dalle scale
@mark 2 ; J19 ; Chuul avanzato (GS 8), sott'acqua nella navata sud
@mark 3 ; AC21 ; Chuul avanzato
@mark 4 ; AD7 ; Chuul avanzato
@mark 5 ; T21 ; Asserviti di Karkator: acquaioli della città, umani popolani, nell'acqua fino al petto (12)
@zone AB8-AM20 ; La Torre delle Volte: sale dal fondo fino a +12 m, 18 × 19,5 m; i due pilastri est sono murati dentro
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 💧 Le navate allagate | H23 | 1 m d'acqua sul fondo: costa 2 quadretti di movimento ogni quadretto, niente carica né corsa (acqua bassa) |
| 🟦 Acqua della vasca | R17 | Nuotare CD 15 (acqua calma); chi la beve o ci si immerge con la bocca aperta rischia il muco di Karkator: Tempra CD 28 o la membrana di muco (1d4 round, −4 Cos) |
| 🟨 Sale affiorato | F22 | Acrobazia CD 12 per muoversi a più di metà velocità |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| PG | I PG, dal ponte ovest o dalle scale | 🔵 | 4 | — | C13–D14 |
| Tariq | Chuul avanzato (GS 8), sott'acqua nella navata sud | 🔴 | 1 | — | J19 |
| Tariq | Chuul avanzato | 🔴 | 1 | — | AC21 |
| Tariq | Chuul avanzato | 🔴 | 1 | — | AD7 |
| Tariq | Asserviti di Karkator: acquaioli della città, umani popolani, nell'acqua fino al petto (12) | 🟢 | 12 | — | Q20–V22 |

- **I chuul stanno sul fondo** e salgono solo su chi scende dalle scalette o cade dal ponte. Dal ponte maestro non arrivano: il ponte è a 6 m. **EL 11** con tutti e tre (GS 8 ciascuno); è uno scontro facoltativo e lo si evita restando sul ponte.
- **Gli asserviti** non combattono: lavorano a raschiare il sale dalle pareti perché Karkator lo vuole. Se i PG li liberano sono 12 uomini da portare su, ed è il conflitto della scena.
- **Il ponte maestro è la strada della Torre**: chi arriva dalla gabbia e scende dalle scale lo percorre per 39 m sotto gli occhi delle feritoie della Torre.

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B · Tariq abbassa l'acqua | Tariq apre le paratoie di scarico dalla Torre | le navate si svuotano, la vasca scende a 3 m | i chuul restano allo scoperto (perdono il bonus sott'acqua) ma il sifone verso il Santuario si apre: Karkator può salire in 2 round |
| C · Karkator sale | rumore di battaglia nella vasca, o Tariq lo chiama | Karkator emerge al centro della vasca | lo scontro finale si sposta qui, con le navate e i ponti come campo: vedi il Santuario per le tattiche |

> **Stessa pianta di QM-2**, 9 m più in basso. I pilastri sono gli stessi: chi scende da una catena di QM-2 arriva nel quadretto corrispondente di questa mappa.

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

