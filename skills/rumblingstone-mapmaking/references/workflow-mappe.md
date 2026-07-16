# Workflow mappe — dalla griglia al risultato professionale

> Razionale e alternative valutate: `plans/RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md`.
> Sintesi operativa: `scripts/README-automation.md` § "Mappe di qualità professionale".

## 1. Modificare una mappa esistente

1. Apri il master (`*MAPPE*.md`, `*Ultra-Clear*.md`): la griglia è nel fenced
   code block, righe numerate `01`, `02`, … + emoji della legenda universale.
2. Modifica le celle (una emoji = un quadretto da 1,5 m).
3. Rigenera: `python3 scripts/render_map_svg.py <file.md>` → aggiorna
   `rendered/<stem>_mapNN_<slug>.svg`.
4. `python3 scripts/validate_maps.py` deve restare verde (SVG committati
   byte-identici al render del master).

## 2. Creare una mappa nuova

- **A mano**: copia `campaign/templates/mappa-tattica-template.md`, disegna la
  griglia, compila i 3 blocchi companion (Ambiente / Tattiche / Evoluzione).
- **Da layout professionale (dungeon)**: genera su
  https://watabou.github.io/dungeon.html → Export JSON →
  `python3 scripts/import_watabou.py dungeon.json -o <arco>/NOME.md` →
  adatta simboli/unità → companion → render.
  Mapping: roccia 🏰, pavimento ⬜, porte 🚪, colonne 🟪, acqua 🟦, note ⭐.

## 3. Qualità del render (cosa fa il renderer, cosa curare nel master)

Il renderer produce da solo: regioni terreno organiche (niente scalini),
occlusione ambientale sui muri, ombre portate, prop illustrati, griglia
leggibile (scura sui terreni chiari + chiara sui terreni scuri), legenda per
categorie, barra di scala. Per un output da manuale cura nel master:

- **Terreni pieni** per le aree (⬜🟩🏰…), non file di icone: le regioni
  contigue diventano forme organiche con bordi inchiostrati.
- **Varietà**: usa il corredo oggetti (🛏📦🛢⚰🪜🦴🍄🕯🌾⛺🔮🪑🧱…) per
  arredare stanze e accampamenti — mappe "vuote" non sembrano professionali.
- **Unità** solo dove servono al primo round: la mappa è uno stato iniziale,
  l'evoluzione sta nel blocco companion.

## 4. Export PNG ad alta risoluzione (stampa / VTT / hero map)

```bash
python3 scripts/export_map_png.py rendered/<mappa>.svg           # 2x (default)
python3 scripts/export_map_png.py rendered/<mappa>.svg --scale 3 # stampa A3
```

Richiede un Chromium/Chrome installato (auto-rilevato). Il PNG è un artefatto
locale: NON si committa (solo gli SVG deterministici stanno nel repo).

## 5. Scale superiori

- **Regionale** (Dalelands/Cannath Vale): Azgaar Fantasy Map Generator
  (https://azgaar.github.io/Fantasy-Map-Generator/, MIT) — committare il
  `.map` come master + export SVG/PNG in `rendered/`.
- **Città** (Rethmar, Palio): Medieval Fantasy City Generator
  (https://watabou.github.io/city-generator/) — committare l'export SVG e
  annotare il seed dell'URL per rigenerare.

## 6. Hero map (opzionale, macchina locale con GPU)

Per le 2-3 mappe chiave si può aggiungere la passata pittorica ComfyUI +
ControlNet: vedi `hero-map-comfyui.md`. Regola: l'output AI va in
`rendered/hero/` (fuori dalla validazione CI) e il master resta la griglia.
