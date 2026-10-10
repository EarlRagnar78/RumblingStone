# Prompt — gli oggetti di scena zenitali generati in locale (D25 di RESA-ASSET)

Il giro di prova di ComfyUI per il tema texture: otto simboli, quattro semi
ciascuno, gli stessi del giro di prova dei modelli CC0 (più i detriti 🪵, che il
DM ha citato come un glifo che oggi vince). Le immagini passano poi da
`build_oggetti_cc0.py --da-immagini` (sfondo tolto, stessa impronta nella
cella) e da `misura_resa.py candidati` e `coppie`, contro il glifo e contro il
modello CC0. Si generano sulla macchina del DM:

```bash
python3 scripts/comfyui_batch.py --prompts plans/esperimenti/oggetti-cc0-2026-10/comfyui/PROMPT-OGGETTI-ZENITALI.md --serie tutto --modello sdxl --out asset-esterni/oggetti-comfyui
```

La licenza sta nei pesi (ADR-0019): SDXL 1.0 base, OpenRAIL++-M. Il campo
`simbolo` delle annotazioni dice quale glifo l'immagine vuole sostituire;
`comfyui_batch.py` lo ignora, `build_oggetti_cc0.py` lo legge.

## §1 · L'ancora di stile, e i negativi

Lo stile è quello della casa, non una fotografia: inchiostro e acquerello come i
glifi della pergamena, vista dall'alto, sfondo bianco piatto perché lo sfondo
si toglie senza scontornare a mano.

<!-- blocco id=ancora-storica -->
```
top-down orthographic view from directly above, tabletop battle map icon,
hand-inked cartographer's illustration, confident dark ink outline, flat
watercolor wash, muted parchment palette (umber, slate grey, ochre),
soft shadow falling to the lower right, centered, isolated on a plain white background
```

<!-- blocco id=negativi -->
```
perspective, isometric, side view, photo, photorealistic, 3d render, text,
watermark, logo, frame, border, multiple objects, cropped, people, hands
```

## §2 · Le immagini

<!-- img id=zenitale-1faa8-a size=1024x1024 stile=tavola serie=extra simbolo=🪨 -->
```
a small cluster of three weathered grey boulders and rubble
```

<!-- img id=zenitale-1faa8-b size=1024x1024 stile=tavola serie=extra simbolo=🪨 -->
```
a small cluster of three weathered grey boulders and rubble
```

<!-- img id=zenitale-1faa8-c size=1024x1024 stile=tavola serie=extra simbolo=🪨 -->
```
a small cluster of three weathered grey boulders and rubble
```

<!-- img id=zenitale-1faa8-d size=1024x1024 stile=tavola serie=extra simbolo=🪨 -->
```
a small cluster of three weathered grey boulders and rubble
```

<!-- img id=zenitale-1f5ff-a size=1024x1024 stile=tavola serie=extra simbolo=🗿 -->
```
a stone statue of a robed and hooded figure on a square plinth, seen from directly above
```

<!-- img id=zenitale-1f5ff-b size=1024x1024 stile=tavola serie=extra simbolo=🗿 -->
```
a stone statue of a robed and hooded figure on a square plinth, seen from directly above
```

<!-- img id=zenitale-1f5ff-c size=1024x1024 stile=tavola serie=extra simbolo=🗿 -->
```
a stone statue of a robed and hooded figure on a square plinth, seen from directly above
```

<!-- img id=zenitale-1f5ff-d size=1024x1024 stile=tavola serie=extra simbolo=🗿 -->
```
a stone statue of a robed and hooded figure on a square plinth, seen from directly above
```

<!-- img id=zenitale-1f3ee-a size=1024x1024 stile=tavola serie=extra simbolo=🏮 -->
```
an iron brazier bowl on three short legs, filled with glowing embers, no flames
```

<!-- img id=zenitale-1f3ee-b size=1024x1024 stile=tavola serie=extra simbolo=🏮 -->
```
an iron brazier bowl on three short legs, filled with glowing embers, no flames
```

<!-- img id=zenitale-1f3ee-c size=1024x1024 stile=tavola serie=extra simbolo=🏮 -->
```
an iron brazier bowl on three short legs, filled with glowing embers, no flames
```

<!-- img id=zenitale-1f3ee-d size=1024x1024 stile=tavola serie=extra simbolo=🏮 -->
```
an iron brazier bowl on three short legs, filled with glowing embers, no flames
```

<!-- img id=zenitale-1f3fa-a size=1024x1024 stile=tavola serie=extra simbolo=🏺 -->
```
a large clay storage urn with two handles, seen from directly above, open round mouth
```

<!-- img id=zenitale-1f3fa-b size=1024x1024 stile=tavola serie=extra simbolo=🏺 -->
```
a large clay storage urn with two handles, seen from directly above, open round mouth
```

<!-- img id=zenitale-1f3fa-c size=1024x1024 stile=tavola serie=extra simbolo=🏺 -->
```
a large clay storage urn with two handles, seen from directly above, open round mouth
```

<!-- img id=zenitale-1f3fa-d size=1024x1024 stile=tavola serie=extra simbolo=🏺 -->
```
a large clay storage urn with two handles, seen from directly above, open round mouth
```

<!-- img id=zenitale-1f6cf-a size=1024x1024 stile=tavola serie=extra simbolo=🛏 -->
```
a simple wooden bed frame with a straw mattress and a rough wool blanket
```

<!-- img id=zenitale-1f6cf-b size=1024x1024 stile=tavola serie=extra simbolo=🛏 -->
```
a simple wooden bed frame with a straw mattress and a rough wool blanket
```

<!-- img id=zenitale-1f6cf-c size=1024x1024 stile=tavola serie=extra simbolo=🛏 -->
```
a simple wooden bed frame with a straw mattress and a rough wool blanket
```

<!-- img id=zenitale-1f6cf-d size=1024x1024 stile=tavola serie=extra simbolo=🛏 -->
```
a simple wooden bed frame with a straw mattress and a rough wool blanket
```

<!-- img id=zenitale-1fa91-a size=1024x1024 stile=tavola serie=extra simbolo=🪑 -->
```
a rectangular rough wooden table with two stools
```

<!-- img id=zenitale-1fa91-b size=1024x1024 stile=tavola serie=extra simbolo=🪑 -->
```
a rectangular rough wooden table with two stools
```

<!-- img id=zenitale-1fa91-c size=1024x1024 stile=tavola serie=extra simbolo=🪑 -->
```
a rectangular rough wooden table with two stools
```

<!-- img id=zenitale-1fa91-d size=1024x1024 stile=tavola serie=extra simbolo=🪑 -->
```
a rectangular rough wooden table with two stools
```

<!-- img id=zenitale-1f9f1-a size=1024x1024 stile=tavola serie=extra simbolo=🧱 -->
```
a short straight segment of a dry-stone low wall, stones stacked, running left to right
```

<!-- img id=zenitale-1f9f1-b size=1024x1024 stile=tavola serie=extra simbolo=🧱 -->
```
a short straight segment of a dry-stone low wall, stones stacked, running left to right
```

<!-- img id=zenitale-1f9f1-c size=1024x1024 stile=tavola serie=extra simbolo=🧱 -->
```
a short straight segment of a dry-stone low wall, stones stacked, running left to right
```

<!-- img id=zenitale-1f9f1-d size=1024x1024 stile=tavola serie=extra simbolo=🧱 -->
```
a short straight segment of a dry-stone low wall, stones stacked, running left to right
```

<!-- img id=zenitale-1fab5-a size=1024x1024 stile=tavola serie=extra simbolo=🪵 -->
```
fallen broken wooden beams and splintered planks lying in a heap
```

<!-- img id=zenitale-1fab5-b size=1024x1024 stile=tavola serie=extra simbolo=🪵 -->
```
fallen broken wooden beams and splintered planks lying in a heap
```

<!-- img id=zenitale-1fab5-c size=1024x1024 stile=tavola serie=extra simbolo=🪵 -->
```
fallen broken wooden beams and splintered planks lying in a heap
```

<!-- img id=zenitale-1fab5-d size=1024x1024 stile=tavola serie=extra simbolo=🪵 -->
```
fallen broken wooden beams and splintered planks lying in a heap
```
