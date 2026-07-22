# Direzione artistica per handout e splash (Modalità 2)

> **A cosa serve**: dare un vocabolario di prompt per ottenere immagini
> d'atmosfera nel look "manuale fantasy classico anni 2000" (l'idioma visivo
> dei manuali Pathfinder 1E / D&D 3.5 dell'epoca), da usare con l'infra ComfyUI
> locale (`scripts/comfyui-local/`, `hero-map-comfyui.md`).

---

## ⚖️ Confine IP — leggere prima (importante)

La domanda ricorrente è "voglio *esattamente* lo stile dell'illustratore
storico di Pathfinder 1E". **Non lo facciamo, e non con quel metodo**, per due
ragioni:

1. **È un artista vivente.** Costruire un prompt per **replicare lo stile di
   una persona specifica citandone il nome** (o addestrare/derivare dalle sue
   tavole) è eticamente e legalmente problematico, e va contro le regole già
   scritte del repo: `hero-map-comfyui.md` §"Cosa NON fare" ("mai usare
   asset/immagini di terzi come style reference diretto") e
   `plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md`.
2. **Non serve.** Ciò che rende riconoscibile quel look **non è la firma di un
   autore**, ma un insieme di **convenzioni di genere/epoca non tutelabili**:
   pose dinamiche, luce drammatica, armature ornate, palette satura. Quelle si
   possono descrivere e chiedere liberamente.

**Regola operativa**: descrivi le *convenzioni* (sotto), **non** nomi propri di
artisti viventi né titoli di prodotti protetti. Niente `by <nome>`,
niente "in the style of <artista>", niente immagini altrui come reference.
Lo *stile come categoria* è libero; i *file e la firma di una persona* no.

---

## Vocabolario del look "eroico classico da manuale" (convenzioni, non autori)

Componi il prompt scegliendo da queste liste — sono descrizioni di tecnica e
composizione, non riferimenti a opere protette.

**Soggetto / posa**
- `dynamic heroic action pose`, `mid-motion`, `dramatic low camera angle`,
  `foreshortening`, `character bursting toward the viewer`

**Resa / tecnica**
- `painterly digital illustration`, `visible brushwork`, `crisp ink line
  underneath`, `high detail on armor and gear`, `ornate fantasy armor`,
  `weathered leather and metal`

**Luce / colore**
- `dramatic rim lighting`, `strong key light`, `warm-cool contrast`,
  `saturated palette`, `deep shadows`, `glowing magical accents`

**Composizione**
- `single hero focal point`, `simple dark vignette background`,
  `character sheet splash`, `full-body`, `three-quarter view`

**Per panorami / handout d'ambiente** (non personaggi)
- `epic fantasy landscape`, `matte-painting`, `top-down orthographic` (per
  mappe), `atmospheric perspective`, `golden hour`, `banners and campfires of
  an army`

**Negative prompt (sempre)**
- `photo, 3d render, modern clothing, text, watermark, signature, blurry,
  extra limbs, deformed hands` (e, per le battle map, `perspective, isometric`)

### Esempio (splash di un villain della campagna)

> **positive**: `dynamic heroic action pose, dramatic low angle, a hobgoblin
> warlord in ornate red-lacquered fantasy armor raising a curved blade,
> painterly digital illustration with crisp ink lines, dramatic rim lighting,
> saturated warm palette, deep shadows, glowing ember accents, simple dark
> vignette background, full-body character splash`
>
> **negative**: `photo, 3d render, modern, text, watermark, signature, blurry,
> deformed hands, extra limbs`

Nessun nome d'artista, nessun titolo di prodotto: solo tecnica e soggetto.

---

## Coerenza con la banca prompt esistente

I file `campaign/ai-media-prompts/*.md` (uno per arco + `11_PG_E_VILLAIN_*`)
sono già scritti con questa filosofia (stile descritto per convenzioni, con
blocchi `[STILE] [SCENA] [CAMERA] [PALETTE] [NO]`). Quando crei un nuovo
handout, **parti da lì** e riusa palette e "NO"-list dell'arco per tenere
coerente l'intera campagna, aggiungendo il vocabolario qui sopra per il taglio
"eroico da manuale".

## Dove NON usare questo look

- **Le battle map giocabili** (Mod. 1 e 3) restano SVG deterministici in stile
  "pergamena": niente ridipintura txt2img che sposti la geometria. La passata
  pittorica sulle mappe è img2img+ControlNet ancorato al master
  (`hero-map-comfyui.md`), non questo prompt libero.
