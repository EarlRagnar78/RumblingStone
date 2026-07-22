# Hero map — passata pittorica locale (OPZIONALE)

> Questa è l'unica parte della pipeline che richiede installazione locale
> (PC con GPU NVIDIA, ~8 GB+ VRAM). Va usata SOLO per le 2-3 mappe chiave
> ("hero maps": battaglia finale, boss fight) e SOLO se il risultato è
> oggettivamente migliore del render pergamena — giudicare a occhio, non
> per principio. Il master resta la griglia emoji; l'SVG deterministico
> resta l'artefatto canonico in CI.

## Perché funziona (e perché è legalmente pulito)

Il render pergamena del repo fornisce la **struttura completa** (layout,
muri, griglia, zone colore). Con **img2img + ControlNet** il modello ridipinge
le superfici in stile "hand-painted battle map" MA è vincolato alla geometria
dell'input: le stanze restano dove sono, la mappa resta giocabile alle stesse
coordinate. L'immagine di partenza è nostra al 100% (niente asset terzi in
input), i pesi SDXL/Flux sono aperti → nessun problema di licenza per uso
non commerciale.

## Setup (una tantum, sulla propria macchina)

1. **ComfyUI** (gratuito, open source): https://github.com/comfyanonymous/ComfyUI
2. Un checkpoint aperto (SDXL o Flux-dev) + i nodi **ControlNet** con modello
   lineart/canny per SDXL.
3. **Server MCP** per pilotarlo da Claude (scegline uno):
   - https://github.com/artokun/comfyui-mcp (completo, plugin Claude Code)
   - https://github.com/miller-joe/comfyui-mcp (essenziale: img2img,
     ControlNet, upscale)
4. Registra il server in Claude Code: `claude mcp add comfyui -- npx …`
   (vedi il README del server scelto).

## Flusso per una hero map

1. Esporta l'input ad alta risoluzione dal render deterministico:
   `python3 scripts/export_map_png.py rendered/<mappa>.svg --scale 2`
2. In ComfyUI (via MCP o GUI): **img2img** con il PNG come input,
   **ControlNet lineart/canny** sulla stessa immagine (strength 0.7-0.9),
   denoise 0.45-0.6.
3. Prompt di partenza (calibrare a occhio):
   - *positive*: `hand-painted fantasy battle map, top-down orthographic,
     parchment tones, painterly texture, soft global lighting, subtle grid,
     professional TTRPG cartography, muted palette, crisp ink outlines`
   - *negative*: `photo, 3d render, isometric, perspective, text, watermark,
     blurry, characters, miniatures`
4. Upscale 2x (model-based) se serve per la stampa.
5. Salva in `rendered/hero/<slug>.png` — directory **fuori** da
   `validate_maps.py` (output non deterministico, non è il canone).
6. Se la griglia esce degradata: ricomponi sovrapponendo la sola griglia
   dell'SVG originale al PNG dipinto (opacità ~50%).

## Cosa NON fare

- Niente txt2img puro: senza ControlNet il layout non corrisponde al master.
- Mai usare asset/immagini di terzi (Forgotten Adventures, 2MTT, mappe Paizo)
  come input o "style reference" diretto: l'output sarebbe un derivato.
- Non committare PNG hero al posto degli SVG: sono un livello di
  presentazione, non il master.
