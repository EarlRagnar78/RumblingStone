# Guida completa — dalle mappe al tavolo (e al VTT)

> **Cosa copre**: tutto il flusso delle mappe, passo per passo. Quale delle
> tre modalità scegliere, come si scrive una mappa da zero, come si importa
> un dungeon già fatto, come si ottengono SVG stampabili, PNG ad alta
> risoluzione e file **importabili in Foundry/Roll20 con muri e luci già
> pronti**, e cosa fare quando la CI diventa rossa.
>
> **Regola d'oro del repo**: la **griglia markdown è il master**, gli SVG in
> `rendered/` sono **artefatti generati** — non si modificano mai a mano
> (lo verifica `validate_maps.py` in CI). Le decisioni dietro la pipeline
> stanno in [ADR-0006](../../plans/adr/ADR-0006-annotazioni-mappa-overlay-professionale.md).

---

## 0. TL;DR — i comandi che userai davvero

```bash
# rendere (o ri-rendere) le mappe di un master markdown → SVG in rendered/
python3 scripts/dm.py maps render "<percorso>/<MASTER>.md"

# controllare che tutti gli SVG del repo siano in sync coi master
python3 scripts/dm.py maps validate

# PNG ad alta risoluzione (stampa / import manuale in un VTT)
python3 scripts/export_map_png.py "<percorso>/rendered/<mappa>.svg" --scale 3

# file per Foundry/Roll20 con muri, porte e luci già dentro
python3 scripts/export_uvtt.py "<percorso>/<MASTER>.md" --ppg 140
```

---

## 1. Quale modalità ti serve?

| Ti serve… | Modalità | Sorgente | Strumento |
|---|---|---|---|
| Una **griglia giocabile** (dungeon, interni, agguato) | **1 — Tattica standard** | griglia emoji scritta a mano, o dungeon importato | `render_map_svg.py`, `import_watabou.py` |
| Un'**immagine d'atmosfera** (handout, splash, copertina) | **2 — Cinematografica** | prompt testuale | ComfyUI locale / generatore esterno |
| Una griglia con **strutture ed eserciti a coordinate precise** (assedi, accampamenti) | **3 — JSON rigido** | contratto JSON validato | `compile_map_json.py` → `render_map_svg.py` |

**Regola pratica**: se la mappa ha meno di ~30 elementi e la disegni tu,
**modalità 1**. Se le posizioni le decide un LLM o ci sono eserciti/strutture
numerose, **modalità 3** (l'LLM non deve MAI disegnare ASCII a mano: dopo
poche righe sbaglia di un quadretto e la griglia si disallinea). Se non
serve giocarci sopra ma guardarla, **modalità 2**.

---

## 2. Modalità 1 — la mappa tattica standard

### 2.1 Dove va il file

La mappa vive **dentro il master markdown dell'arco** (o in un file mappe
dedicato), in un blocco di codice. Gli SVG generati finiscono in una
cartella `rendered/` **accanto** al master:

```
09_Continuazione .../
├── Arco-Post-Hammerfist-P2D-PALIO-MAPPE.md      ← MASTER (lo modifichi tu)
└── rendered/
    └── Arco-…-MAPPE_map01_<slug>.svg            ← GENERATO (mai a mano)
```

### 2.2 Come si scrive una mappa

Parti dal template: **`campaign/templates/mappa-tattica-template.md`** (in
fondo ha un esempio già compilato, «Campo Drow 1»). Ogni mappa ha **quattro
blocchi**, e servono tutti:

| Blocco | Cosa ci va |
|---|---|
| **Griglia** | il blocco di codice con le righe numerate e le celle emoji |
| **🌍 AMBIENTE** | cosa impone il terreno — **regole**, non prosa (copertura, terreno difficile, CD) |
| **⚔️ TATTICHE** | come si comportano i nemici, round per round, con le coordinate |
| **🔄 EVOLUZIONE** | come cambia la mappa — **stati**, non un copione (crolli, rinforzi, allagamenti) |

Formato della griglia: ogni riga comincia con il **numero di riga a due
cifre**, poi le celle emoji (con o senza spazi). Le colonne si contano con
le lettere. Scala fissa: **1,5 m per quadretto**.

```
COL →  A  B  C  D  E  F
01    🏰 🏰 🏰 🏰 🏰 🏰
02    🏰 ⬜ ⬜ 🚪 ⬜ 🏰
03    🏰 ⬜ 🟪 ⬜ ⬜ 🏰
```

### 2.3 La legenda universale (usa SOLO questi simboli)

Il renderer e l'export UVTT riconoscono i simboli **della legenda del repo**:
un simbolo fuori legenda viene disegnato male o ignorato.

| Terreno | | Unità | | Oggetti/pericoli | |
|---|---|---|---|---|---|
| 🏰 | muro / roccia solida | 🔵 | PG / alleati | 🪨 | rocce (copertura +4 CA) |
| ⬜ | pavimento lavorato | 🔴 | nemico standard | 🔥 | fuoco (1d6/round) |
| ⬛ | struttura (tenda, edificio) | ⚫ | boss / comandante | 💥 | esplosione |
| 🟪 | pilastro / mithral | 🟡 | incantatore nemico | 💀 | fossa / trappola |
| 🟩 | pianura | 🟢 | evocazione / bestia | 🕳 | voragine |
| 🟫 | terra battuta | 🟣 | creatura speciale | 🚪 | porta |
| 🌲 | foresta densa | | | 🏮 🕯 | luci (diventano luci nel VTT) |
| 🟦 🌊 | acqua profonda / corrente | | | ⛰ | montagne / creste |

Lista completa: `skills/rumblingstone-mapmaking/references/legenda-universale.md`.

### 2.4 Renderizzare

```bash
python3 scripts/dm.py maps render "07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-DEFINITIVO.md"

# opzioni utili dello script diretto:
python3 scripts/render_map_svg.py <master.md> --list        # elenca le mappe trovate
python3 scripts/render_map_svg.py <master.md> --map 2       # rende solo la 2ª
python3 scripts/render_map_svg.py <master.md> -o <cartella> # output altrove
```

Il renderer produce lo stile «pergamena»: terreni organici, ombre e
occlusione, libreria di props vettoriali originali, token stile VTT, griglia
1,5 m con coordinate, barra di scala, **bussola** e legenda.

### 2.5 Modificare una mappa esistente

1. modifica **la griglia nel master markdown** (mai l'SVG);
2. rilancia `dm.py maps render <master.md>`;
3. `git add` **sia** il master **sia** l'SVG rigenerato;
4. `python3 scripts/dm.py maps validate` prima del commit.

### 2.6 Importare un dungeon già fatto (Watabou)

```bash
# 1) genera su https://watabou.github.io/dungeon.html   2) esporta in JSON
python3 scripts/import_watabou.py dungeon.json -o "<arco>/NUOVA-MAPPA.md"
# 3) compila i blocchi Ambiente / Tattiche / Evoluzione (template)
python3 scripts/dm.py maps render "<arco>/NUOVA-MAPPA.md"
```

Conversione automatica: stanze/corridoi → ⬜, muri esterni → 🏰, porte → 🚪,
colonne → 🟪, acqua → 🟦, note numerate → ⭐ (elencate sotto la griglia).

---

## 3. Modalità 3 — strutture ed eserciti (contratto JSON)

Serve quando le posizioni sono tante o le decide un LLM. **L'LLM emette solo
JSON**; a dipingere la griglia ci pensa lo script, in modo deterministico.

```bash
# 1) scrivi/genera lo spec JSON secondo scripts/schemas/tactical_map.schema.json
# 2) valida senza scrivere nulla
python3 scripts/compile_map_json.py spec.json --validate-only
# 3) compila nel master markdown a griglia emoji
python3 scripts/compile_map_json.py spec.json -o "<arco>/NUOVA-MAPPA.md"
# 4) rendi
python3 scripts/dm.py maps render "<arco>/NUOVA-MAPPA.md"
```

Se il JSON è invalido lo script **lo rifiuta con errori precisi**: si corregge
e si riemette (l'LLM non tocca mai le coordinate sul disegno).

**Esempi funzionanti da copiare** — `scripts/examples/`:
`campo-drow-1.json` (+ il `.md` risultante), `hammerfist-L2-assedio.json`,
`esempio-accampamento-mano-rossa.json`, `esempio-misure-in-metri.json`.

**Authoring in metri**: puoi dichiarare le dimensioni in metri invece che in
quadretti — evita il drift dimensionale (una tenda «6×4 m» resta 6×4 m).

**Overlay professionale** (direttive dentro il blocco griglia, ADR-0006):

| Direttiva | Effetto sul render |
|---|---|
| `@north` | bussola (disegnata sempre) |
| `@path` | rotta di movimento tratteggiata |
| `@mark` | roster numerato sui token |
| `@zone` | zone etichettate + legenda «INDICAZIONI» |

### 3.1 Migrare una vecchia mappa «ultra-clear»

I master ultra-clear mescolano la figura disegnata a mano e le tabelle di
coordinate: quando divergono, **la figura mente**. Lo strumento rende la
divergenza esplicita:

```bash
python3 scripts/import_ultraclear.py "<master-ultra-clear>.md" \
    -o bozza-spec.json --conflicts report-conflitti.md
```

Produce una bozza di spec JSON **e** l'elenco dei conflitti con severità e
suggerimento: risolvi solo i punti segnalati, poi procedi come al §3.

---

## 4. Modalità 2 — immagini cinematografiche (handout, splash)

Non è una griglia: è un'illustrazione d'atmosfera. Due vie:

- **Generatore esterno** (Nano Banana, ChatGPT…): componi il prompt col
  vocabolario di `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md`;
- **ComfyUI in locale** (GPU): `scripts/comfyui-local/` + la reference
  `hero-map-comfyui.md`. Può anche prendere il **PNG di una mappa renderizzata**
  come base strutturale e restituirne una versione «dipinta».

> ⚖️ **Confine IP (ADR-0005)**: si descrivono le **convenzioni** di stile
> (posa, luce, palette, tecnica), **mai** nomi di artisti viventi, «in the
> style of X», né immagini altrui usate come style reference.

---

## 5. Consegna: SVG, PNG, UVTT

| Formato | Comando | Quando |
|---|---|---|
| **SVG** | `dm.py maps render` | il canone nel repo; stampa vettoriale senza perdita |
| **PNG** | `export_map_png.py <svg> --scale 3` | stampa raster, import manuale nel VTT, input hero-map |
| **UVTT / dd2vtt** | `export_uvtt.py <master.md> --ppg 140` | import **nativo** in Foundry/Roll20 |

### Cosa finisce dentro un `.uvtt` (e perché ti fa risparmiare un'ora)

- **muri con blocco della vista** ← ricavati dai bordi fra celle muro (🏰 ⬛ 🟪 🗼 🏛) e non-muro;
- **porte** ← dalle celle 🚪;
- **luci** ← da 🏮 🕯 🔥 🔮 (o dalle `lights` dello spec JSON);
- **griglia e risoluzione** ← da `--ppg` (pixel per quadretto);
- **immagine di sfondo** ← opzionale con `--image mappa.png`.

```bash
# esempio completo: PNG + uvtt con l'immagine incorporata
python3 scripts/export_map_png.py "<arco>/rendered/<mappa>.svg" -o /tmp/mappa.png --scale 3
python3 scripts/export_uvtt.py "<arco>/<MASTER>.md" --ppg 140 --image /tmp/mappa.png -o /tmp/mappa.uvtt
# poi: in Foundry → Scene → Import; in Roll20 → import dd2vtt
python3 scripts/export_uvtt.py "<arco>/<MASTER>.md" --ext dd2vtt --ppg 140
```

**PNG e UVTT sono artefatti locali**: non si committano (in repo resta l'SVG).

---

## 6. La regola d'oro (e perché la CI ti ferma)

`validate_maps.py` (in CI a ogni PR) verifica tre cose:

1. **ben formati** — ogni SVG in `rendered/` è XML valido;
2. **provenienza** — ogni SVG ha il suo master `.md` accanto (niente orfani);
3. **in sync** — ri-renderizzando il master si riottengono **gli stessi byte**.

Se hai modificato la griglia e non hai rigenerato, o hai toccato l'SVG a
mano, la CI diventa rossa. Rimedio: `dm.py maps render <master>` + commit.

---

## 7. Se qualcosa non funziona

| Sintomo | Causa e rimedio |
|---|---|
| `validate_maps` dice **out of sync** | master modificato senza rigenerare → `dm.py maps render <master>` e committa l'SVG |
| `validate_maps` dice **orphan** | c'è un SVG senza master (master rinominato/cancellato) → rinomina o elimina l'SVG |
| `validate_maps` dice **missing** | il master produce una mappa senza SVG committato → rigenera e committa |
| La griglia «slitta» di un quadretto | righe con numero di celle diverso → conta le celle; se la mappa è complessa passa alla **modalità 3** (JSON) |
| Un simbolo non viene disegnato | è fuori legenda → usa quelli del §2.3 |
| Nel VTT mancano i muri | quelle celle non sono simboli-muro riconosciuti (🏰 ⬛ 🟪 🗼 🏛) → correggi la griglia e riesporta |
| `export_map_png` non parte | serve Chromium headless → vedi [GUIDA-BOOKLET-E-PDF §2](GUIDA-BOOKLET-E-PDF.md#2-prerequisiti) o passa `--browser` |
| Mappa enorme illeggibile in stampa | `--scale 2/3/4` sul PNG, oppure spezza la mappa in due scene |

---

## 8. Checklist prima di committare una mappa

- [ ] La griglia usa **solo** simboli della legenda universale
- [ ] Ci sono tutti e quattro i blocchi (Griglia, Ambiente, Tattiche, Evoluzione)
- [ ] `python3 scripts/dm.py maps render <master>` eseguito **dopo** l'ultima modifica
- [ ] `python3 scripts/dm.py maps validate` verde
- [ ] Committati **master + SVG**; PNG/UVTT **non** committati
- [ ] Se è una mappa nuova d'arco: citata dal master del modulo

---

## 9. Dove sta il resto

| Cosa | Dove |
|---|---|
| Legenda universale completa | `skills/rumblingstone-mapmaking/references/legenda-universale.md` |
| Le 3 modalità in dettaglio + system prompt per LLM | `…/references/tre-modalita-mappe.md` |
| Contratto JSON (schema) | `scripts/schemas/tactical_map.schema.json` |
| Hero map con ComfyUI | `…/references/hero-map-comfyui.md` + `scripts/comfyui-local/README.md` |
| Import ultra-clear in dettaglio | `…/references/import-ultraclear.md` |
| Parametri esatti di ogni script | [`scripts/README-automation.md`](../../scripts/README-automation.md) · [`docs/tools/README.md`](../tools/README.md) |
