# Esempi — contratti JSON per `compile_map_json.py` (Modalità 3)

File d'esempio del **contratto JSON rigido** che un LLM deve emettere per
progettare una mappa tattica con strutture ed eserciti (vedi
`scripts/schemas/tactical_map.schema.json` e
`skills/rumblingstone-mapmaking/references/tre-modalita-mappe.md`).

| File | Cosa mostra |
|---|---|
| `esempio-accampamento-mano-rossa.json` | Accampamento della Mano Rossa: foresta + strada + guado, palizzata di legno con cancello, tenda di comando, bracieri (luci), fossa-trappola, **unità di esercito per aree occupate** (arcieri/fanteria hobgoblin con `quantity`, Wyrmlord e adepto come token singoli). |
| `campo-drow-1.json` (+ `campo-drow-1.md`, `rendered/…svg`) | Ricostruzione dell'Ultra-Clear **Campo Drow 1** (quest di Hella) con l'**overlay professionale**: `north` (bussola), `movements` (2 rotte pattuglia con `loop`), roster numerato 1-14 dai `name`/`cr` delle unità, 4 zone etichettate (tende/comando/cucina/incineratore). Le coordinate dei token coincidono **esattamente** con quelle dichiarate nel master originale (l'ASCII a mano aveva ~1 quadretto di drift). Master + SVG committati e validati in CI. |
| `esempio-misure-in-metri.json` | Stessa Modalità 3 ma **authoring in metri** (`"units_in": "meters"`): sala 45×33 m → 30×22 quadretti, braciere/portale/lastroni/unità dichiarati in metri reali e convertiti da `compile_map_json.py` (`round(m/1,5)`, edge-snapping sui rect). Chiude il problema **proporzioni/dimensionamento** (distinto dal drift ASCII): le misure non si stimano più a occhio. |
| `hammerfist-L2-assedio.json` (+ `.md`, `rendered/…svg`) | **Caso ASCII→JSON**: ricostruzione della `Hammerfist-L2-REVISED-Ultra-Clear.md` (ARC-08) dai suoi **dati autoritativi** (tabelle coordinate + posizioni PG), NON dal disegno ASCII. Fixa i difetti tipici dell'ultraclear che confondono la pipeline: griglia non uniforme (righe da 34-48 celle su header 120), simbolo `⛰️` fuori legenda, confusione **Dara/Dana** (cecchino sulla torre vs guaritrice nel cortile), drift annotazioni↔coordinate. Risultato: vero 120×80 uniforme, ogni elemento alla coord dichiarata. Master + SVG committati e validati in CI. |

Prova il round-trip completo (nessun file committato: output in una dir a
scelta):

```bash
# 1. valida il contratto
python3 scripts/compile_map_json.py scripts/examples/esempio-accampamento-mano-rossa.json --validate-only

# 2. compila la griglia master
python3 scripts/compile_map_json.py scripts/examples/esempio-accampamento-mano-rossa.json -o /tmp/accampamento.md

# 3. render SVG (stile pergamena)
python3 scripts/render_map_svg.py /tmp/accampamento.md

# 4. export VTT con muri + porte + luci (Foundry/Roll20)
python3 scripts/export_uvtt.py /tmp/accampamento.md
```
