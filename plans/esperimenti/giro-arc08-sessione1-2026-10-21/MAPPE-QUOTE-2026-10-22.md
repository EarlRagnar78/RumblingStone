# Mappe di ARC-08: quote e standard ADR-0098 (2026-10-22)

Origine: le decisioni del DM del 2026-10-22 sulle quote di Hammerfist e la
richiesta di portare le mappe di ARC-08 allo standard di
`skills/rumblingstone-mapmaking/references/standard-qualita-mappe.md`,
misurato con `scripts/qualita_mappe.py`. La geometria resta quella della
tabella MISURE in testa a `Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md`,
salvo dove le decisioni del DM la cambiano.

## Le decisioni del DM applicate

1. **Gradoni.** Fronte sud e cortile esterno a +80 m sulla piana, cortile
   interno a +100, torri nord e cittadella a +120. Fra un ripiano e l'altro
   una scarpa di 20 m. Dal ponte una strada a tornanti scende alla piana.
   Gli accampamenti dell'assedio stanno a 500 m-1 km, fuori tiro d'arco
   lungo composito (~330 m). La ritirata notturna «a 200 m» è diventata la
   ritirata agli accampamenti. I giganti (incremento 36 m, al massimo 180 m)
   salgono la strada fino al gomito a ~100 m per tirare.
2. **Quote assolute.** Piana 870 m, cancello 950 m s.l.m., tutte
   `[INFERRED]`. Ogni mappa all'aperto ha `@luogo`, `@quota` e
   `@dislivello`; la 2A e la MAPPA 1 della L2 condividono il luogo
   «Hammerfist, porta principale» alla stessa quota (950 m).
3. **La fortezza del 372.** Cortile a +100 e torre nord a +120 (B2); il
   ripiano a +80 era la spianata degli arieti. Detto nella L2 (MISURE, «Le
   quote»), nell'Atlante (2C) e nella guida (`ARC08-01`, vista C). Le mappe
   e i master di ARC-07 non sono toccati.
4. **Le mappe peggiori prima**: 3Z, 2B, 3Y, MAPPA 5, MAPPA 4, 1A-3, 1A-1.
5. **Truppe.** 300 nani: 270 alle postazioni, 30 di riserva nel cortile
   esterno che il DM manda alla breccia. Nelle mappe (2A, MAPPA 2 della L2),
   in `ARC08-01` (veterani da 15 a 13 unità, due sono le Guardie Reali; lo
   schema ASCII della MAPPA 2, in tutte e due le copie), in `ARC08-18` §1 e
   in `ARC08-19`.
6. **Il Re il Giorno 3.** Al corno del drago sale sulla piattaforma sopra
   il cancello per tenere i nani ai posti, e il soffio lo prende lì. La 2A
   (POSIZIONI), la 2B-CORRETTA, `ARC08-01` (Giorno 3, Incontro 2B) e
   l'Atlante lo mettono nello stesso punto.
7. Le brecce est e ovest della H3-1 restano.

## Voti prima e dopo

`python3 scripts/qualita_mappe.py` sui tre master e su DEF-1. Nessun
rilievo E, prima e dopo; gli avvisi A sono passati da 34 a 0 non derogati.

| Mappa | Prima | Dopo | Cosa è cambiato |
|---|---|---|---|
| 3Z Incrocio Silenzioso (L3) | 43 | 98 | rifatta da contratto (`HF-3Z-incrocio-silenzioso.json`): caverna ottagonale di ~40 m, sei tunnel senza porte, pilastro di roccia al centro che fa l'anello, anello di 60 veterani e 20 balestrieri (i numeri di `ARC08-01`), bugbear nelle bocche est e ovest. Corretti GS 9, furtivo +4d6, Nascondersi +17 dalla scheda del Bestiario |
| 3Y Ponte Sospeso (L3) | 78 | 94 | rifatta da contratto: quattro colonne di roccia sulle due sponde (anelli), uscita nord senza porta, ponte di 15 m |
| MAPPA 5 Cuore della Montagna (L3) | 81 | 94 | quattro pilastri, il canale della sorgente, porta di mithral a 6 m; deroghe per la cattedrale oltre il tavolo e il portale |
| MAPPA 4 Battaglia finale (L3) | 85 | 100 | il pendio sotto le mura (prima roccia), la strada a tornanti, quote 950 → ~890; tabella 4X riscritta |
| H3-1 Cortile sfondato (L3) | 87 | 94 | scarpa di 20 m con due scale e pianerottolo; l'orda sale la scala ovest; B1/B2 a +120; deroghe per gli incendi e il portone |
| 2A Fortezza (L2) | 93 | 100 | scarpa, scale e pianerottolo; riserva di 30 nel cortile esterno al posto dei 50 «di riserva» nel cortile interno; ritirata per le scale |
| 2B-CORRETTA (L2) | 93 | 94 | Fauci Enorme su 3 × 3 (`taglie`), il Re sul cancello, quote |
| MAPPA 1 Disposizione (L2) | 96 | 100 | il pendio da 950 a 870 m, la strada a tornanti coi cinque gomiti, rotta dei giganti, tende di Grimjaw tolte dal pendio |
| 1A-3 Campo della Mano Rossa (L1) | 83 | 100 | rifatta da contratto (`HF-1A3-campo-mano-rossa.json`) sul modello della M7-C di ARC-07: 60 × 60 a 3 m, sei centurie di 12 tende vere in file con corsie e vie, piazza del comando con la tenda nera isolata, clan degli orchi, recinto dei worg, parco d'assedio, palude |
| 1A-1 Sentiero Nascosto (L1) | 87 | 94 | quote; deroghe motivate per la distanza della pattuglia e lo spazio (la scena è la risalita furtiva) |
| 1A-2 Torrione (L1) | 93 | 94 | quote |
| 1D Pendio (L1 e copia in DEF-1) | 97 | 98 | quote |
| **Media** | **85** | **97** | |

## Le quote

| Mappa | `@luogo` | `@quota` | `@dislivello` |
|---|---|---|---|
| 1A-3 | Campo della Mano Rossa, piana di Hammerfist | 870 m | 0 m |
| 1A-1 | Sentiero Nascosto, canyon di Hammerfist | 900 m | +30 m |
| 1A-2 | Torrione di Vedetta, valle di Hammerfist | 930 m | +60 m |
| MAPPA 4 (L3) | Hammerfist, pendio sud | 920 m | +50 m |
| 1D | Hammerfist, pendio sotto le mura | 945 m | +75 m |
| 2A, MAPPA 1 (L2) | Hammerfist, porta principale | 950 m | +80 m |
| 2B-CORRETTA | Hammerfist, bastioni sud | 965 m | +15 m sul cortile esterno |
| H3-1 | Hammerfist, cortile interno | 970 m | +20 m sul cortile esterno |

Tutte le quote s.l.m. sono `[INFERRED]` (decisione del DM sui valori di
piana e cancello, il resto ricavato).

## Cosa ho deciso io (`[INFERRED]`)

- Le quote s.l.m. dei ripiani: 870, 950, 970, 990.
- La scarpa di 20 m con due scale di 30 m larghe 3 m e il pianerottolo
  davanti alla Porta Interna; il ripiano a +120 sono B1, B2 e la cittadella,
  raggiunta da una scala interna dietro il portale dell'atrio; B2 è la torre
  nord del 372.
- La strada: larga 6 m, al 15%, ~530 m, gomiti AW16, M35, AW54, M73, AD90
  sulla MAPPA 1; il pendio ~27% su 300 m in pianta.
- I giganti tirano dal gomito M35 (~100 m), a −4.
- La composizione della riserva (2 unità di balestrieri e 1 di veterani) e
  la regola del libretto: entra come terzo reparto nel settore che cede e
  non torna indietro (`ARC08-19`, tabella delle versioni).
- 3Z: la geometria dell'anello e il pilastro dell'incrocio. 3Y: le colonne
  di roccia. MAPPA 5: i quattro pilastri, il canale, la porta di 6 m.
- MAPPA 4: la linea hobgoblin a ~920 m. 1A-1, 1A-2, 1D: le quote.
- 1A-3: la disposizione del campo. Nella Sessione 1 il campo è a qualche
  miglio dalle mura (come dice DEF-1) e a 400 m dal Torrione; nell'assedio
  l'orda si riaccampa con lo stesso ordine a 500 m-1 km.

## Correzioni trovate per strada

- Cadute: 1d6 ogni 3 m (SRD), non 1d6 al metro e non 2d6 ogni 3 m: L2 (2C),
  L3 (H3-1), Atlante (2C).
- Balista: incremento di gittata 36 m, non «gittata 120 m» (`ARC08-01`,
  `ARC08-02`, L2).
- Giganti: incremento 36 m, al massimo 180 m, non «gittata 120 m» (Atlante,
  `ARC08-01`, `ARC08-19`).
- Bugbear della 3Z: GS 9, furtivo +4d6, Nascondersi +17 (scheda del
  Bestiario) nella L3 e nell'Atlante.
- L'Atlante dava 3 m o 2 m per quadretto a 1A-1, 1A-2, 2A e 3Z, che sono a
  1,5 m.

## `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md`

Toccato solo dove le nuove mappe rendevano falso un numero:

- la scala della 1A-3, da «6 m» a «3 m» (riga 27, la nota della Fase 3) e
  da «40 × 50 a 6 m» a «60 × 60 a 3 m» (Appendice B);
- la copia della 1D nell'Appendice B ha le stesse tre righe `@luogo`,
  `@quota`, `@dislivello` della L1.

Il campo a 400 m dal torrione, la cresta a 400 m e «a molte miglia» dalle
mura restano veri.

## Cosa resta aperto (va chiesto al DM)

- **Il TS del soffio nella 2B**: la guida dice Riflessi CD 29, la 2B CD 25.
- **Fauci «a 45 m, fuori gittata delle baliste»** (L2, MAPPA 3; Atlante):
  con incremento 36 m le baliste a 45 m tirano, a −2. O il drago vola più
  alto, o le baliste lo possono colpire.
- **Il secondo accesso della MAPPA 5**: nella caverna si entra solo dalla
  porta di mithral (più il canale della sorgente). Se il DM vuole un secondo
  ingresso, per esempio una galleria laterale per i bugbear, va disegnato.
- **La 1A-1** è in deroga per spazio e distanza: va bene così, o la si
  accorcia al tratto della pattuglia?
- **`taglie` nel compilatore**: in modalità metri `taglie.at` non viene
  convertito; nella 2B uso le coordinate in quadretti. È di
  `compile_map_json.py`, segnalato al coordinatore.
- Restano nei master toccati alcuni id `(Dnn)` nudi di prima (L2 riga 451,
  L3 righe 176, 696, 700, 718): non li ho aggiunti io, ma per ADR-0070 vanno
  sciolti.

## Controlli

- `python3 scripts/qualita_mappe.py --strict` sulle mappe toccate: 0 errori,
  0 avvisi non derogati, media 97.
- `python3 scripts/collaudo_mappe.py`: 0 errori (avvisi M1/M2/M4 euristici).
- `python3 scripts/validate_maps.py`: 55 SVG ben formati e allineati.
- Test delle mappe (`scripts/tests/test_*mapp*`, `test_qualita_mappe.py`,
  `test_collaudo_*`, `test_resa_mappe.py`, ...): 135 passati.
- SVG rigenerati con `scripts/render_map_svg.py`, tema pergamena e texture;
  la 1A-3 ha cambiato nome (titolo nuovo) e i due SVG vecchi sono tolti.
