# Le mappe del Drappo

Due tavoli tattici, prodotti con la pipeline del repo. **Il sorgente è il JSON**: il
master emoji-grid e l'SVG sono generati e non si modificano a mano.

| Mappa | Sorgente | Master stampabile | SVG da tavolo |
|---|---|---|---|
| **La Ruota** (piazza e pista) | `tarsilia-la-ruota.json` | `tarsilia-la-ruota.md` | `rendered/tarsilia-la-ruota_map01_tarsilia-la-ruota-pista-del-drappo.svg` |
| **Le stalle dei Boschispini** | `tarsilia-stalle.json` | `tarsilia-stalle.md` | `rendered/tarsilia-stalle_map01_tarsilia-le-stalle-dei-boschispini-assalto-nottu.svg` |

## Rigenerare

```bash
python3 scripts/compile_map_json.py <mappa>.json -o <mappa>.md
python3 scripts/render_map_svg.py <mappa>.md
python3 scripts/validate_maps.py            # gate di CI
```

Per stampare o portarle su un VTT:

```bash
python3 scripts/export_map_png.py rendered/<file>.svg --scale 3   # artefatto locale, non committare
python3 scripts/export_uvtt.py <mappa>.md -o <cartella>           # Foundry / Roll20
```

## Coordinate

Le griglie sono **lettera × numero** e partono da **A01** in alto a sinistra. Le
coordinate citate nei testi delle sessioni sono quelle stampate sulla mappa:
le stalle usano **B9** (porta sul canale), **G4** (botola del fienile), **H12** (box
del cavallo), **O3** (finestra alta).

Scala: **1,5 m per quadretto** su entrambe.
