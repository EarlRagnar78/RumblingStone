# Hero map — passata pittorica locale (OPZIONALE)

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- Perché funziona (e perché è legalmente pulito)
- Setup (una tantum, sulla propria macchina)
- Flusso per una hero map
- Cosa NON fare
- Finché ComfyUI non è collaudato: la hero map con Canva AI
<!-- /indice -->

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

## Finché ComfyUI non è collaudato: la hero map con Canva AI

Decisione del DM del 2026-09-25, dopo le immagini di ARC-07 (#172). La passata
qui sopra non è ancora stata provata su una macchina vera; fino a quel giorno
una hero map si può chiedere a Canva AI, con confini più stretti, perché un
servizio non ha ControlNet e la geometria non è vincolata a niente.

**Cosa fa Canva AI, e cosa no.**

| | Chi la fa |
|---|---|
| la hero map dipinta, da mostrare ai giocatori | Canva AI |
| la verità tattica: dove sono muri, porte, stanze, accessi | il master a griglia, il suo JSON, l'SVG, `validate_maps`, l'UVTT. Nessun'altra fonte |
| la griglia | **nessun generatore AI**. Se al tavolo serve, si sovrappone quella dell'SVG (passo 6 del flusso qui sopra) |

**Il prompt si scrive dal JSON della mappa**, non dal ricordo della scena. Per
una mappa di Modalità 3 è il file dello schema `tactical_map`; per un master a
griglia è l'export UVTT (`export_uvtt.py`), che ha muri e porte. Dal JSON si
prendono, in quest'ordine:

1. il rapporto larghezza/altezza (`map_size`), che diventa il formato
   dell'immagine: una mappa 40 × 24 non si chiede quadrata;
2. il terreno di base e le regioni, in parole, per terzi dell'immagine con il
   nord in alto («il terzo di sinistra è palude»);
3. le strutture, le stanze e **ogni porta e ogni accesso**, con la loro
   posizione nello stesso modo;
4. la resa: `hand-painted fantasy battle map, top-down orthographic`, la
   tavolozza della bibbia visiva dell'arco, e in coda i negativi che il
   servizio non ha come campo: `no grid, no text, no letters, no characters,
   no miniatures, no perspective`.

Oggi nessuno script scrive questo prompt: si compone a mano seguendo i quattro
punti, e il JSON va citato accanto al prompt nel file dei prompt dell'arco.

**Il gate, prima di tenerla.** Si esporta l'SVG in PNG
(`export_map_png.py`), si mettono le due immagini una sull'altra allo stesso
rapporto, e si confrontano porte, stanze e accessi uno per uno. **Una hero map
che sposta una porta, una stanza o un accesso rispetto all'SVG si butta**, anche
se è bella: i giocatori la guardano e poi muovono le miniature sulla griglia, e
se le due dicono cose diverse il tavolo discute la mappa invece di giocare. Il
motivo va in `SCARTI.txt` dell'arco, come per ogni immagine
(`rumblingstone-art-direction` §6 e §7-bis).

Il file esportato è il sorgente (ADR-0019 §2-bis: il servizio non espone il
seme), va in `rendered/hero/` come quelli di ComfyUI, fuori da `validate_maps`,
e ha la sua riga in `PROVENIENZA.txt`.
