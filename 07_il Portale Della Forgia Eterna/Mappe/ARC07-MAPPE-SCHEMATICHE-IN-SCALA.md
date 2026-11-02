# ARC-07 — Le mappe schematiche, in scala

Le mappe che nei master erano solo schemi ASCII, ridisegnate su una griglia in
scala perché escano nei booklet come piante (ADR-0106, scelta di Jfs del
2026-10-30). Le misure sono quelle scritte negli schemi; dove lo schema non le
dava, la scelta è segnata nella nota della mappa. Gli schemi originali restano
nei master: T-5 in DEF-1 e nell'Atlante, R-1 in DEF-3 e nell'Atlante.

Si modifica la griglia e si rigenera:
`python3 scripts/render_map_svg.py --tema pianta --stampa "<questo file>"`.

## T-5 — L'Anticamera della Magnetite (DEF-1 §7b)

L'esagono ha i lati nord e sud dritti e le punte a ovest e a est: 18 m da
punta a punta, 16,5 m fra i lati dritti. Thorik e Artemis stanno contro la
parete nord, come nello schema; la Sentinella al centro, Tordek davanti a lei.

```
════════════════════════════════════════════════════════════════════════
 T-5 · ANTICAMERA DELLA MAGNETITE — esagono Ø 18 m (12 col × 11 righe · 1,5 m)
 Nord in alto (parete dove resta incollato Thorik) · porta sigillata a SUD
════════════════════════════════════════════════════════════════════════
COL →   A  B  C  D  E  F  G  H  I  J  K  L
01     🏰 🏰 🏰 🧲 🧲 🧲 🧲 🧲 🧲 🏰 🏰 🏰
02     🏰 🏰 🧲 ⬜ ⬜ 🔵 🔵 ⬜ ⬜ 🧲 🏰 🏰
03     🏰 🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰 🏰
04     🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰
05     🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰
06     🧲 ⬜ ⬜ ⬜ ⬜ 🤖 ⬜ ⬜ ⬜ ⬜ ⬜ 🧲
07     🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰
08     🏰 🧲 ⬜ ⬜ ⬜ 🔵 ⬜ ⬜ ⬜ ⬜ 🧲 🏰
09     🏰 🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰 🏰
10     🏰 🏰 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 🏰 🏰
11     🏰 🏰 🏰 🧲 🧲 🚪 🚪 🧲 🧲 🏰 🏰 🏰
LEGENDA · 🧲 parete di magnetite: incolla chi porta metallo · 🤖 la Sentinella
════════════════════════════════════════════════════════════════════════
@north N
@tipo tattica caverna
@mark 1 ; F2 ; Thorik, incollato alla parete nord dall'armatura: immobilizzato
@mark 2 ; G2 ; Artemis, prono accanto a Thorik (gravità 10×)
@mark 3 ; F6 ; La Sentinella, al centro: RD 15/adamantio e contundente, solo i Bracieri passano; 3 crepe e il guscio si infrange (Geode di Smeraldo)
@mark 4 ; F8 ; Tordek, l'unico in piedi (il pavimento a gravità 2× lo regge solo lui)
@zone F11-G11 ; Porta sigillata (sud)
```

## R-1 — Il cerchio del rito (DEF-3, Appendice B)

Questa mappa è a **1 m per quadretto**, non a 1,5 m: così l'Altare (2 × 2 m)
sta su quattro quadretti interi e il cerchio di 3 m di raggio cade sulla
griglia. I tre officianti stanno sul cerchio, a nord, est e ovest; sul
quadretto il centro è spostato di mezzo metro, quindi le distanze vere sono
fra 2,5 e 3,5 m. Il sud resta vuoto.

```
════════════════════════════════════════════════════════════════════════
 R-1 · IL CERCHIO DEL RITO — 10 m × 10 m (10 col × 10 righe · 1 m)
 Cerchio rituale Ø 6 m attorno all'Altare (2 × 2 m) · il SUD resta VUOTO
════════════════════════════════════════════════════════════════════════
COL →   A  B  C  D  E  F  G  H  I  J
01     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
02     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
03     ⬜ ⬜ ⬜ ✨ 🔵 ✨ ✨ ⬜ ⬜ ⬜
04     ⬜ ⬜ ✨ ⬜ ⬜ ⬜ ⬜ ✨ ⬜ ⬜
05     ⬜ ⬜ ✨ ⬜ ⭐ ⭐ ⬜ 🔵 ⬜ ⬜
06     ⬜ ⬜ 🔵 ⬜ ⭐ ⭐ ⬜ ✨ ⬜ ⬜
07     ⬜ ⬜ ✨ ⬜ ⬜ ⬜ ⬜ ✨ ⬜ ⬜
08     ⬜ ⬜ ⬜ ✨ ✨ ✨ ✨ ⬜ ⬜ ⬜
09     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
10     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
LEGENDA · ✨ il cerchio del rito, a 3 m dal centro dell'Altare · ⭐ l'Altare con il Cuore di Moradin, 2 × 2 m
════════════════════════════════════════════════════════════════════════
@north N
@tipo rituale
@mark 1 ; E5 ; L'Altare: il Cuore di Moradin posato sul cuore di Hella, il corpo supino, i 3 semi sulla mano sinistra, sulla mano destra e sulla fronte
@mark 2 ; E3 ; Thorik a nord (Corona e Aegis Fang): Conoscenze (religioni) CD 15
@mark 3 ; H5 ; Tordek a est (ki): Concentrazione CD 20
@mark 4 ; C6 ; Artemis a ovest (anello): Usare Oggetti Magici CD 18
@mark 5 ; F8 ; Il sud resta vuoto: da qui fluisce l'energia, e qui appare la Custode delle Radici allo step 5 (§6)
@zone A1-J1 ; Therysol veglia ai margini: testimone, non officiante
```

## S-1 — La Sala della Forgia Eterna dopo la Terra (DEF-2)

La pianta è quella di PF-2 (ridisegnata il 2026-10-23), per scelta di Jfs del
2026-10-30: una Sala sola in tutti i booklet. Sopra ci sono gli affreschi e la
gente come li mette DEF-2, assegnati per punto cardinale. Le differenze con lo
schema di DEF-2, per il DM:

- PF-2 ha 8 pilastri adamantini; lo schema di DEF-2 ne aveva 4 (uno di mithral
  a nord e tre di adamantio). Vale la pianta.
- In PF-2 il portale a est (X-Y16-17) è detto del Fuoco e a sud c'era un
  portale della Terra. In DEF-2 il Fuoco è a ovest (A4, chiuso), la Terra a
  est (A5, si chiude) e a sud c'è l'affresco A8, senza portale: qui il
  portale sud è tolto e quello est è la Terra.
- Il portale P1 per la Stanza della Corona è a nord, sull'affresco A1.

```
════════════════════════════════════════════════════════════════════════
 S-1 · LA SALA DELLA FORGIA ETERNA dopo la Terra — Ø 40 m (27 col × 27 righe · 1,5 m)
 La pianta di PF-2, con gli affreschi come stanno in DEF-2 · Zona sicura
════════════════════════════════════════════════════════════════════════
COL →   A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z  AA
01     🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
02     🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬛ 🖼 🖼 🖼 ⬛ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
03     🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰
04     🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰
05     🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰
06     🏰 🏰 🏰 🏰 ⬛ ⬛ 🖼 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🖼 🖼 ⬛ ⬛ 🏰 🏰 🏰 🏰
07     🏰 🏰 🏰 ⬛ ⬛ 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🖼 ⬛ ⬛ 🏰 🏰 🏰
08     🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰
09     🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰
10     ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
11     ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛
12     ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛
13     ⬛ 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⭐ ⭐ ⭐ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛
14     ⬛ 🖼 ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⭐ 🔥 ⭐ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬛ ⬛
15     ⬛ 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⭐ ⭐ ⭐ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛
16     ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🌀 🌀 🖼 ⬛
17     ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🌀 🌀 🖼 ⬛
18     ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛
19     🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰
20     🏰 🏰 ⬛ ⬛ ⬛ 🌀 🌀 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰
21     🏰 🏰 🏰 ⬛ ⬛ 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🟪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🖼 ⬛ ⬛ 🏰 🏰 🏰
22     🏰 🏰 🏰 🏰 ⬛ ⬛ 🖼 🖼 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🖼 🖼 ⬛ ⬛ 🏰 🏰 🏰 🏰
23     🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰
24     🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰
25     🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰
26     🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬛ 🖼 🖼 🖼 ⬛ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
27     🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
════════════════════════════════════════════════════════════════════════
@north N
@tipo tattica interni
@luogo Portale della Forgia Eterna, Sala della Forgia (hub dei Piani)
@deroga struttura/senza-anelli ; sala ottagonale aperta: il giro si fa attorno all'altare e fra i pilastri, nessun blocco di muro serve
@mark 1 ; N2 ; A1 «L'Alba del Mondo»: statico, Moradin forgia la Corona. Qui c'è il portale P1 per la Stanza della Corona, sempre aperto
@mark 2 ; G6 ; A2 «I quattro eroi» all'80%: la quarta figura, Hella, prende contorno
@mark 3 ; U6 ; A3 «Visione» (Thorik)
@mark 4 ; B14 ; A4 «Fuoco»: chiuso
@mark 5 ; Z16 ; A5 «Terra»: si chiude («Forza Sostenuta»), e il portale davanti si spegne
@mark 6 ; G22 ; A6 «Tempo» all'80%: il portale davanti (F-G20) pulsa
@mark 7 ; U22 ; A7 «Hammerfist»: vivo, ⏳ circa 3 giorni e 20 ore, con il Bane di Aegis Fang
@mark 8 ; N26 ; A8 «Ritorno Trionfale» al 60%: davanti c'è Therysol solo per la manifestazione
@mark 9 ; N10 ; Dove arrivano i PG, a 6 m dall'Altare
@mark 10 ; N16 ; Il corpo di Hella, accanto all'Altare dal lato sud
@mark 11 ; M17 ; Therysol, che veglia il corpo
@mark 12 ; O17 ; Durik, fra il corpo e il pericolo
```
