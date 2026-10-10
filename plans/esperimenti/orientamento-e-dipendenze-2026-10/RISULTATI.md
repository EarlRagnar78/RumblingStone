# Orientamento delle chiusure, asset di Wesnoth, dipendenze in deroga — la misura

Audit in sola lettura del 2026-10-08, sera, per V2-quater di
[PIANO-COLLAUDO-E-GENERAZIONE-MAPPE](../../PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md).
Decisioni che ne sono uscite: D13-D16 del piano,
[ADR-0083](../../adr/ADR-0083-l-asse-delle-chiusure-si-ricava-dai-vicini.md) e
[ADR-0084](../../adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md).

| File | Cosa riproduce |
|---|---|
| `misura_assi.py` → `misura-assi-2026-10-08.txt` | §1, gli assi del corpus e chi li sbagliava (solo stdlib) |
| `bench_m4.py` → `bench-m4-2026-10-08.txt` | §3, M4 su tutte le celle, stdlib contro `tcod` |

I numeri di §2 e §4 vengono da comandi a una riga, scritti qui accanto a ogni
tabella. Corpus: quello di `collaudo_mappe.py`, 44 mappe (38 del 2026-10-08
più le sei della #225).

## §1 · Le chiusure del corpus, e tre risposte diverse

```
python3 -I plans/esperimenti/orientamento-e-dipendenze-2026-10/misura_assi.py
```

| | Prima | Dopo (`dmcore/chiusure.py`) |
|---|---:|---:|
| chiusure nel corpus | 125, tutte `🚪` | uguale |
| in un muro est-ovest | 60 | 60 |
| in un muro nord-sud | 36, **disegnate di traverso** dal renderer | 36, glifo ruotato |
| ambigue (portone 2×2 sul bordo del Portale) | 2, nessuno lo sapeva | 2, avviso `posa/asse-ambiguo` |
| senza muro intorno | 27 | 27 (già errore `posa/nel-muro`) |
| portali UVTT girati, sulle 96 porte con un asse | **13** | 0 |
| mappe con almeno una chiusura nord-sud | 11 | — |
| SVG rigenerati | — | 13: 10 del corpus (4 sono D28 della #225) e 3 di `_ARCHIVIO` |

I 13 portali UVTT sbagliati stanno tutti in file di porte con il muro da un
lato solo (Hammerfist mappe 2, 4, 5; Campo Drow): la regola vecchia, «muro
sopra *o* sotto», li leggeva nord-sud. Guardati a vista uno per uno: la regola
nuova ha ragione in tutti e 13.

Confronto a vista: la porta doppia nel muro est della Fucina Grande (M7-F del
372, colonna AB, righe 11-12), prima due travi di traverso nel varco, dopo due
battenti nel filo del muro.

## §2 · Battle for Wesnoth

```
git clone --filter=blob:none --no-checkout --depth 1 https://github.com/wesnoth/wesnoth.git
git ls-tree -r --name-only HEAD data/core/images | cut -d/ -f4 | sort | uniq -c
```

Commit `9ec35a2f` del 2026-10-06.

| Domanda | Risposta |
|---|---|
| Licenza del codice | GPL-2.0-or-later (`COPYING`, `README.md`) |
| Licenza dell'arte | «la maggior parte» GPL-2.0+, i contributi nuovi CC BY-SA 4.0 (`README.md`) |
| Crediti per file | `copyrights.csv`: 396 righe, **tutte audio** (343 GPL v2+, 48 CC BY-SA 4.0, 5 CC0). Per le 14.456 immagini di `data/core/images` non c'è un elenco: la licenza di un PNG si ricostruisce dalla storia git |
| Forma | PNG 72×72, vista obliqua, griglia di esagoni; l'orientamento sta nel nome (`gate-rusty-se`, `gate-rusty-sw`) |
| Cosa c'è di utile per noi | `items/` (128) e `scenery/` (141): gabbie, bare, incudini, bracieri, botole, pozzi, balle di fieno, cerchi di evocazione, barche. Quasi tutti già nella legenda, disegnati in casa |
| Cosa chiede il corpus | 0. Le 13 voci di legenda locale che non sono universali: stalagmiti, colonne parallele, cristalli, zona aerea, i PG, una postazione |

**Cosa contaminerebbe cosa.** Un PNG GPL o CC BY-SA dentro uno SVG generato fa
dello SVG un'opera derivata con la stessa licenza; il PDF che contiene lo SVG
la eredita per la parte grafica. Le mappe derivano da *Red Hand of Doom* e non
si possono rilicenziare (ADR-0005). In più la regola 5 di
`rumblingstone-mapmaking` vieta i file di terzi. «Trarre ispirazione» qui vuol
dire ridisegnare da zero, ed è quello che la legenda ha già fatto con quei
concetti.

L'idea che resta: Wesnoth sceglie la variante di un muro o di un cancello
guardando le tessere vicine (le regole di terreno). `dmcore/chiusure.py` fa la
stessa cosa per l'asse di una porta, scritta dalla descrizione e non dal
codice.

## §3 · M4 esatta, libreria standard contro `tcod`

```
pip install -r requirements-dev.txt
python3 plans/esperimenti/orientamento-e-dipendenze-2026-10/bench_m4.py
```

| | Tempo, 43.423 celle | Note |
|---|---:|---|
| shadowcasting simmetrico in stdlib, pendenze come `Fraction` | circa 435 s (62 s su una cella ogni sette) | prima stesura, scartata |
| lo stesso, pendenze in aritmetica intera | **69,9 s** | `bench_m4.py` |
| `tcod.map.compute_fov`, `FOV_SYMMETRIC_SHADOWCAST` | **0,6 s** | |
| accordo sulle celle campione | 414 su 470 insiemi identici, Jaccard **0,9999** | le differenze sono celle di bordo |

Il collaudo intero, con M4 su tutte le mappe tattiche di almeno 12×12: da 1,3
a **2,5 s**. M4 sul corpus: 38 mappe, mediana 0,72, minimo 0,11, massimo 1,00;
27 oltre la soglia euristica di 0,45.

## §4 · Gli altri candidati

| Candidato | Comando | Risultato |
|---|---|---|
| `resvg-py` 0.5.0 (MIT) contro Chromium per i PNG | `export_map_png.py --renderer browser --scale 2` su 8 mappe, poi `resvg_py.svg_to_bytes(zoom=2)` | Chromium 42 s per 8 mappe e 8 PNG identici al byte in due giri; resvg circa 150 s per 4 mappe (filtri `feTurbulence` e `feDisplacementMap` su un solo filo), interrotto |
| `hypothesis` 6.168 (MPL-2.0) | quattro mutanti dell'asse; 3.000 esempi per proprietà, contro un generatore `random.Random(20261008)` di 3.000 griglie | entrambi colgono 3 su 4 (solo nord, `or` sui muri, spareggio rovesciato); entrambi mancano il bordo trattato come vuoto, che è simmetrico e richiede un caso scritto. Il test del bordo è in `test_chiusure.py` |
| `networkx`, `scipy`, `shapely` | — | nessun problema misurato da risolvere: collaudo a 1,3 s, muri UVTT già fusi |

Licenze, rilasci e pesi da PyPI il 2026-10-08 (`pip download --no-deps
--only-binary=:all:`): `networkx` 3.7 BSD-3 2,1 MB · `scipy` 1.18.1 34 MB ·
`tcod` 21.2.1 BSD-2 8,2 MB · `shapely` 2.2.0 BSD-3 2,2 MB · `hypothesis`
6.168.5 MPL-2.0 1,2 MB · `resvg-py` 0.5.0 MIT 1,4 MB.

## Cosa questa misura non dice

- Se una porta ruotata **si legge meglio al tavolo**: il ritaglio della Fucina
  Grande lo fa pensare, ma il giudizio è del DM (D10 resta aperta per i glifi).
- Se M4 sopra 0,45 è un difetto: la soglia viene dall'audit di luglio e non è
  calibrata.
- Le scale (`🔼`, `🔽`) hanno anche loro un verso, e non sono state misurate.
