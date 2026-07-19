# Le 3 modalità di mappa — quale pipeline usare e perché

> **A cosa serve**: dare un modello mentale unico alle mappe della campagna.
> Tutte e tre le modalità **esistono già** nel repo con strumenti diversi;
> questo file dice *quale* usare, *quando*, e *come far agire un LLM* senza che
> "sbagli a caso". La regola d'oro che le attraversa tutte:
>
> > **Un LLM non disegna MAI arte ASCII di una mappa.** L'arte ASCII scritta
> > token-per-token slitta di un quadretto dopo poche righe e distrugge
> > l'allineamento. L'LLM produce **dati strutturati** (JSON validato) oppure
> > **prompt testuali**; a disegnare/renderizzare ci pensano gli script
> > deterministici del repo.

---

## Colpo d'occhio

| # | Modalità | Quando | Sorgente autoriale | Strumento | Output |
|---|---|---|---|---|---|
| 1 | **Tattica standard** (dungeon, interni, agguati) | serve una griglia giocabile 1,5 m | griglia emoji scritta a mano **o** dungeon importato | `render_map_svg.py` · `import_watabou.py` | SVG (+ PNG, +UVTT) |
| 2 | **Cinematografica / scenica** (handout, splash, video-intro) | serve un'immagine d'atmosfera, non una griglia | prompt testo (LLM come *prompt engineer*) | `ai-media-prompts/` + ComfyUI hero-map | PNG artistico |
| 3 | **Tattica con strutture ed eserciti** (assedi, accampamenti, battaglie a coordinate) | serve una griglia con posizionamenti precisi decisi da un LLM | **contratto JSON rigido** | `compile_map_json.py` → `render_map_svg.py` (+UVTT) | SVG + PNG + UVTT |

Le tre si combinano: una battaglia (Mod. 3) può avere un handout di apertura
(Mod. 2) e riusare pezzi di una tattica standard (Mod. 1).

---

## Modalità 1 — Tattica standard

**Cos'è**: la spina dorsale del repo. La mappa è una **griglia emoji** in un
fenced code block (il MASTER, umano-leggibile e diffabile), renderizzata in SVG
"pergamena" deterministico.

**Come procede l'LLM**: scrive/edita direttamente la griglia emoji seguendo la
legenda universale (`legenda-universale.md`) e il template companion, oppure
**non scrive la griglia affatto** e parte da un layout generato:

- generatore gratuito → **Watabou One Page Dungeon** (export JSON) →
  `python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md`.
- Poi `render_map_svg.py`, si compilano i 3 blocchi companion, si valida.

**Dettaglio operativo completo**: `workflow-mappe.md`.

---

## Modalità 2 — Cinematografica / scenica

**Cos'è**: un'immagine d'atmosfera (non una griglia di gioco) — copertina di
sessione, handout per i giocatori, panorama della fortezza, ritratto
dell'esercito. Qui l'LLM è un **ingegnere dei prompt**, non un disegnatore.

**Come procede l'LLM**:

1. Scrive un prompt testuale ricco a partire dal lore. La **banca prompt della
   campagna** è già pronta in `campaign/ai-media-prompts/` (un file per arco,
   con scene, palette, "NO"-list, mood musicale). Riusa e adatta quelli.
2. Il prompt va a un generatore di immagini locale. L'infra container è
   `scripts/comfyui-local/` (ComfyUI in Distrobox su Bazzite, GPU NVIDIA,
   senza toccare l'OS immutabile).
3. Direzione artistica (look "manuale fantasy classico"): vedi
   `stile-illustrazione-handout.md` — con i **confini IP** (niente cloni di
   artisti viventi).

**Variante "hero map"**: se l'immagine deve restare *giocabile* (una battle map
dipinta, non un semplice quadro), non è txt2img puro: è **img2img + ControlNet**
sul PNG di una mappa deterministica del repo, così la geometria resta fissa.
Procedura completa: `hero-map-comfyui.md`.

---

## Modalità 3 — Tattica con strutture ed eserciti (il pezzo nuovo)

**Cos'è**: la modalità in cui gli LLM "sbagliavano l'ASCII". Serve una griglia
tattica dove **un LLM** decide dove vanno palizzate, tende, torri, trappole e
**unità di esercito** a coordinate precise (assedio di Rethmar, accampamento
della Mano Rossa, Battaglia di Hammerfist).

**La correzione**: l'LLM emette **solo un JSON rigido** conforme a
`scripts/schemas/tactical_map.schema.json`; lo script lo valida e compila la
griglia in modo deterministico.

```
[LLM]  --(solo JSON valido)-->  compile_map_json.py  -->  MASTER griglia-emoji
                                                              │
   render_map_svg.py (SVG) · export_map_png.py (PNG) · export_uvtt.py (Foundry/Roll20)
```

**Passi**:

1. L'LLM produce il JSON (vedi il template sotto e l'esempio
   `scripts/examples/esempio-accampamento-mano-rossa.json`).
2. `python3 scripts/compile_map_json.py spec.json -o <arco>/MAPPA.md`
   - valida **coordinate, simboli, geometria**; se qualcosa non torna
     **rigetta con l'elenco degli errori** → l'LLM corregge e reinvia
     (è il loop `--validate-only`);
   - se valido, dipinge regioni → strutture → pericoli → **unità**, ed emette
     il master con i 3 blocchi companion pre-compilati (tabella FORZE inclusa).
3. `python3 scripts/render_map_svg.py <arco>/MAPPA.md` → SVG.
4. `python3 scripts/export_uvtt.py <arco>/MAPPA.md` → `.uvtt` con **muri
   (line_of_sight), porte (portals) e luci** già pronti per Foundry/Roll20.

### Astrazione per unità (evita la saturazione del contesto)

Non si posiziona un token per ogni soldato: **un'unità = un blocco**. Nel JSON
un reparto di 50 arcieri è *una* voce con `area` (l'ingombro sulla griglia) e
`quantity: 50`. Il compilatore timbra l'area come footprint del reparto e mette
il numero nella **tabella FORZE** del companion. È lo stesso ragionare "per
Unità / Aree Occupate" dei moduli Paizo (le armate di ARC-00/ARC-08 sono già
descritte così in `00_Red Hand Of Doom/Armate-*`).

### Template minimo del contratto JSON

```json
{
  "title": "Nome della mappa",
  "scale_m_per_square": 1.5,
  "map_size": [30, 22],
  "base_terrain": "🟩",
  "regions":    [ {"terrain": "🌲", "rect": [0,0,6,22]} ],
  "structures": [ {"type": "🏰", "line": [[10,3],[10,19]]},
                  {"type": "🚪", "at": [10,11]},
                  {"type": "⛺", "center": [20,11], "radius": 2, "label": "Tenda comando"} ],
  "hazards":    [ {"type": "💀", "at": [12,11], "effect": "Osservare CD 20; 2d6"} ],
  "units":      [ {"faction": "Mano Rossa", "name": "Arcieri hobgoblin",
                   "token": "🔴", "area": {"rect": [13,5,3,2]}, "quantity": 24} ]
}
```

Coordinate: `[x, y]` con **x = colonna** (0-based, sinistra→destra) e
**y = riga** (0-based, alto→basso). Simboli ammessi: solo quelli della legenda
universale (`SYMBOLS` in `render_map_svg.py`) — il validatore rifiuta il resto.

### "System prompt" da dare all'LLM per la Modalità 3

> Sei un cartografo tattico per D&D 3.5 / Pathfinder 1E. **Non** produrre mai
> arte ASCII di mappe. Quando ti chiedo un accampamento, un assedio o un
> posizionamento di trappole/eserciti, rispondi **esclusivamente** con un
> blocco JSON conforme allo schema `tactical_map.schema.json`: `map_size`,
> `regions`, `structures`, `hazards`, `units`. Usa solo i simboli della legenda
> universale, coordinate `[x,y]` dentro `map_size`, e ragiona per **unità/aree
> occupate** (`area` + `quantity`), mai un token per creatura. Se non sei
> sicuro di una coordinata, lascia l'elemento fuori e segnalalo a parole dopo
> il JSON.

---

## Formati di consegna (tutte le modalità)

| Formato | Da dove | Uso |
|---|---|---|
| **SVG** | `render_map_svg.py` | canone in repo, stampa vettoriale senza perdita |
| **PNG** | `export_map_png.py` | stampa raster, import manuale VTT, input hero map |
| **UVTT/dd2vtt** | `export_uvtt.py` | import **nativo** Foundry/Roll20 con muri+luci |
| **PNG artistico** | ComfyUI (Mod. 2) | handout, splash, copertine — *non* il master |

SVG = canone versionato. PNG e UVTT sono **artefatti locali** (gitignorati,
fuori da `validate_maps.py`): si rigenerano dal master quando servono.
