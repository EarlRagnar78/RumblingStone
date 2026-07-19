# Esempi — contratti JSON per `compile_map_json.py` (Modalità 3)

File d'esempio del **contratto JSON rigido** che un LLM deve emettere per
progettare una mappa tattica con strutture ed eserciti (vedi
`scripts/schemas/tactical_map.schema.json` e
`skills/rumblingstone-mapmaking/references/tre-modalita-mappe.md`).

| File | Cosa mostra |
|---|---|
| `esempio-accampamento-mano-rossa.json` | Accampamento della Mano Rossa: foresta + strada + guado, palizzata di legno con cancello, tenda di comando, bracieri (luci), fossa-trappola, **unità di esercito per aree occupate** (arcieri/fanteria hobgoblin con `quantity`, Wyrmlord e adepto come token singoli). |

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
