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
| ⬛ | edificio (muratura piena) | ⚫ | boss / comandante | 💥 | esplosione |
| ⛺ | tenda (blocca la vista, si abbatte) | 🔳 | dais / pedana (**non** è muro) | 🧱 | muretto (+4 CA) |
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

Non è una griglia: è un'illustrazione d'atmosfera.

> 📘 **Guida dedicata**: [`GUIDA-IMMAGINI.md`](GUIDA-IMMAGINI.md) — quale
> generatore usare, come si scrive un prompt, coerenza d'arco, troubleshooting.
>
> 🎨 **I prompt di un intero arco in un comando** (ADR-0015):
> `python3 scripts/dm.py prompts "<cartella dell'arco>"` estrae tutte le scene
> con read-aloud e prepara una **scheda-prompt per scena** in
> `<arco>/Immagini/PROMPT-IMMAGINI-*.md` (i prompt li scrivi tu o l'agente).
> Esemplare compilato: `07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md`.

Due vie per generarle:

- **Generatore esterno** (Nano Banana, ChatGPT…): componi il prompt col
  vocabolario di `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md`;
- **ComfyUI in locale** (GPU): `scripts/comfyui-local/` + la reference
  `hero-map-comfyui.md`. Può anche prendere il **PNG di una mappa renderizzata**
  come base strutturale e restituirne una versione «dipinta».

> ⚖️ **Confine IP (ADR-0005)**: si descrivono le **convenzioni** di stile
> (posa, luce, palette, tecnica), **mai** nomi di artisti viventi, «in the
> style of X», né immagini altrui usate come style reference.

### 4.1 Far combaciare l'illustrazione con la pianta — Blender come geometria

C'è un divario che nessun prompt colma. In un modulo pubblicato **la tavola
della locanda e la pianta della locanda sono la stessa stanza**; qui erano due
cose scollegate, perché la pianta nasce da un contratto JSON e l'illustrazione da
una descrizione, e nessuno garantiva che la curva nord fosse a nord.

```bash
python3 scripts/render_map_blender.py mappa.json --piano-solo   # la geometria, senza Blender
python3 scripts/render_map_blender.py mappa.json                # veduta ortografica
python3 scripts/render_map_blender.py mappa.json --profondita   # ← il pezzo che conta
```

`render_map_blender.py` risolve la geometria con **lo stesso `paint()`** che
alimenta l'SVG — quindi il 3D non può divergere dalla pianta —, fonde le celle
uguali in solidi, e la fa rendere a Blender (GPL) in ortografica.

Il secondo uso vale più del primo: **`--profondita`** produce il passo di
profondità, che si dà a **ControlNet depth** in ComfyUI. L'illustrazione generata
eredita la pianta reale invece di inventarsela.

Tre cose da sapere prima di usarlo:

- **Blender qui non disegna**: per un ritratto un generatore fa meglio e costa
  meno. Serve alla geometria, che è l'unica cosa che un generatore non sa fare;
- **il livello tattico resta fuori**: unità e insidie non sono geometria, sono
  note del DM — la stessa ragione per cui esiste la mappa in versione giocatore.
  Le insidie si tengono con `--con-insidie`;
- **le texture sono opzionali e CC0**: convenzione e fonte in
  [`scripts/blender/texture/README.md`](../../scripts/blender/texture/README.md).
  Senza, il render esce coi colori piatti dell'SVG.

Se `blender` non è installato, il tool dice come si installa, **lascia scritto il
piano di scena** ed esce pulito: quando lo installi, il render riparte da lì.

---

## 5. Consegna: SVG, PNG, UVTT

| Formato | Comando | Quando |
|---|---|---|
| **SVG** | `dm.py maps render` | il canone nel repo; stampa vettoriale senza perdita |
| **PNG** | `export_map_png.py <svg> --scale 3` | stampa raster, import manuale nel VTT, input hero-map. Usa **Inkscape** se installato, altrimenti Chromium (`--renderer` per forzare) |
| **UVTT / dd2vtt** | `export_uvtt.py <master.md> --ppg 140` | import **nativo** in Foundry/Roll20 |

### Cosa finisce dentro un `.uvtt` (e perché ti fa risparmiare un'ora)

- **muri con blocco della vista** ← ricavati dai bordi fra celle muro (🏰 ⬛ ⛺ ⛰ 🟪 🗼 🏛 🗿) e non-muro — 🔳 dais e 🪨 macerie esclusi di proposito: sul dais ci si sale, le macerie sono copertura **parziale**;
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

### 5.1 Il tema texture: materiali veri, licenza CC0

Ogni mappa ha una seconda resa accanto alla pergamena, in `rendered-texture/`:
stessi terreni, stessi contorni, stessi glifi, ma il pavimento è lastricato,
il muro è roccia o muratura, la terra è terra. Le texture vengono da
**Poly Haven**, licenza **CC0 1.0** (letta alla fonte il 2026-10-09): uso
anche commerciale, ridistribuzione permessa, nessun credito obbligatorio.
Stanno nel repo e possono uscirne. È la strada principale per mappe più ricche
(D13-D15 di [PIANO-RESA-E-ASSET](../../plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md)).

| Terreno | Texture | Terreno | Texture |
|---|---|---|---|
| ⬜ pavimento | `stone_tiles_02` | 🟩 pianura | `leafy_grass` |
| 🏰 muro, caverna ed esterno | `rock_wall_10` | 🌿 vegetazione | `forest_ground_04` |
| 🏰 muro, interni e abitato | `castle_brick_07` | 🟨 sabbia | `sand_01` |
| 🟫 terra | `dirt_floor` | ⛰ creste | `rock_face_03` |
| ⬛ edificio | `roof_slates_02` | 🟤 caverna | `rocks_ground_02` |
| 🔳 pedana | `monastery_stone_floor` | | |

Restano vettoriali il bosco fitto (dall'alto è una chioma), l'acqua, la lava,
la fogna, il vuoto, la zona letale e i pilastri. Quale muro usare lo decide
`@tipo`: è la categoria che ogni mappa già dichiara.

```bash
# 1) una volta: scarica le 11 texture (rete) e costruisce le tessere da 256 px
python3 scripts/dm.py asset texture
#    oppure, se le hai scaricate a mano (<id>_diff_1k.jpg):
python3 scripts/build_texture_cc0.py --da-cartella ~/Scaricati/polyhaven
# 2) il tema texture di tutte le mappe che hanno già la pergamena
python3 scripts/dm.py maps texture
# 3) controlla e committa scripts/texture-cc0/ e le cartelle rendered-texture/
python3 scripts/validate_maps.py
```

Lo script confronta l'MD5 di ogni file con quello che dichiara l'API di Poly
Haven, e l'indice (`scripts/texture-cc0/indice.json`) tiene fonte, URL e
impronte. Dopo il primo commit delle texture, `validate_maps` pretende il
gemello texture di ogni mappa e lo rigenera per confronto, come la pergamena.
Per Foundry: `export_map_png.py` sull'SVG di `rendered-texture/`, poi
`export_uvtt.py --image`.

La velatura, cioè quanto colore della pergamena copre la texture, è 0,30:
l'ha scelta il DM confrontando 0,45, 0,30 e 0,20 sulle texture vere (D16).
I 53 SVG del tema pesano 7,6 MB, contro i 6,2 MB della pergamena.

#### 5.1.1 Gli oggetti di scena: modelli 3D CC0 resi dall'alto (R4-ter)

Nel tema texture rocce, statue, letti, botti e muretti possono essere tessere
rese con Blender da modelli 3D CC0, al posto dei glifi; la pergamena tiene i
glifi. Ogni modello è reso con la stessa camera zenitale, lo stesso sole da
nord-ovest e la stessa impronta nella cella (D20), così il set ha una luce sola.
Restano glifi il fuoco e gli effetti, le porte, le finestre, le grate e le
sbarre, i segnali, le creature, le scale e i buchi (D21): sono i simboli con
`tessera_cc0: false` in `scripts/legend.yaml`, più le chiusure. Il braciere è un focolare di pietre con la
fiammella del glifo sopra (D22). Il muretto ha due tessere, est-ovest e
nord-sud, e il renderer sceglie quella giusta dai muretti vicini.

| Fonte | Licenza (letta il 2026-10-09) | Cosa dà |
|---|---|---|
| Poly Haven | CC0 1.0 | 16 modelli per 15 simboli, con l'MD5 di ogni file verificato contro l'API |
| Quaternius, Fantasy Props MegaKit **Standard** | CC0 1.0 | i simboli che Poly Haven non ha, se ci sono: si scopre dallo zip |

I modelli restano sulla tua macchina, in `asset-esterni/oggetti-cc0/` (D19):
pesano 50-70 MB. Nel repo entrano solo le tessere e l'indice.

```bash
# 0) una volta: Blender come modulo nel venv del repo (bpy vuole Python 3.13)
.venv/bin/python --version
.venv/bin/pip install bpy
#    la scena funziona? due modelli procedurali resi davvero, senza rete (~10 s)
.venv/bin/python -m pytest -q scripts/tests/test_blender_vero.py
#    se il venv non è 3.13, usa il Blender di sistema e aggiungi ai comandi sotto
#    --blender 'flatpak run org.blender.Blender'   (o il percorso del binario)

# 1) il giro di prova: scarica gli 8 modelli delle due mappe del confronto,
#    verifica l'MD5 di ogni file, li rende (meno di un minuto su CPU)
.venv/bin/python scripts/build_oggetti_cc0.py --prova

# 2) la misura dello stile e il tema texture con le tessere
.venv/bin/python scripts/build_oggetti_cc0.py --misura-stile
python3 scripts/dm.py maps texture

# 3) le due mappe del confronto in PNG, da guardare accanto alla versione a glifi
python3 scripts/export_map_png.py '07_il Portale Della Forgia Eterna/Mappe/hammerfist-372-1372/rendered-texture/M7-D-livello-1-1372_map01_m7-d-1372-il-corridoio-della-fucina-livello-1-gi.svg' -o /tmp/M7-D-oggetti.png
python3 scripts/export_map_png.py '07_il Portale Della Forgia Eterna/Mappe/rendered-texture/ARC07-MAPPE-DEFINITIVO_map05_cortile-interno-36-m-27-m-24-col-18-righe-1-5-m.svg' -o /tmp/ARC07-cortile-oggetti.png

# 4) se la prova va, tutti i modelli di Poly Haven, poi di nuovo il tema
.venv/bin/python scripts/build_oggetti_cc0.py
python3 scripts/dm.py maps texture

# 5) prima del commit la tua scelta (D23): senza i tuoi voti --check
#    boccia ogni tessera. I passi esatti sono in §5.1.2, «Da zero, in ordine»
python3 scripts/misura_resa.py candidati scripts/oggetti-cc0 --registra
python3 scripts/misura_resa.py coppie scripts/oggetti-cc0 -o /tmp/scelta.html
python3 scripts/misura_resa.py voti ~/Scaricati/voti.json
python3 scripts/build_oggetti_cc0.py --adotta          # tiene solo le preferite
python3 scripts/dm.py maps texture

# 6) controlli e commit: tessere, indice e i gemelli texture rigenerati
python3 scripts/build_oggetti_cc0.py --check && python3 scripts/validate_maps.py
git add scripts/oggetti-cc0 scripts/scheda-resa.json scripts/texture-cc0
git add -- '*rendered-texture/*.svg'
git commit -m "RESA-ASSET R4-ter: le tessere degli oggetti di scena"
```

Quaternius si aggiunge dopo, e solo con lo zip **Standard** (su itch.io a
prezzo libero, anche 0 $; la Pro e la Source non si usano):

```bash
# a) impronta, licenza e nomi dei modelli: incolla l'uscita nella PR
.venv/bin/python scripts/build_oggetti_cc0.py --elenca-quaternius ~/Scaricati/'Fantasy Props MegaKit[Standard].zip'
# b) quando la tabella QUATERNIUS e l'impronta sono nello script
.venv/bin/python scripts/build_oggetti_cc0.py --rendi --quaternius ~/Scaricati/'Fantasy Props MegaKit[Standard].zip'
```

Le tessere si fanno una volta e si committano: chi non ha Blender legge le
tessere e basta, e dove una tessera manca resta il glifo. `--check` boccia una
tessera che non combacia con l'indice, una licenza che non è CC0, un modello non
verificato e un simbolo che deve restare glifo. Se Poly Haven cambia uno dei
modelli fissati, lo scaricamento si ferma e lo dice.

#### 5.1.2 La resa misurata: una sostituzione entra solo se migliora (ADR-0086)

Una tessera nuova (da un modello CC0, da ComfyUI) o una texture prende il posto
di un glifo o di un terreno solo se **la misura non la boccia** e **tu la
preferisci nella pagina di scelta** (D23). Lo strumento è
`scripts/misura_resa.py`: posa ogni simbolo su un banco di prova reso dal
renderer vero, nei due temi e su due terreni, e misura cella per cella.

| Misura | Cosa dice | Fonte |
|---|---|---|
| contrasto del contorno | quanto l'oggetto si stacca da ciò che ha intorno; sotto 3:1 non si riconosce | WCAG 2.1 §1.4.11 |
| bordo | quanto è netto il contorno | Sobel |
| somiglianza col vicino | con quale altro simbolo si confonde, e quanto | SSIM |
| distanza dalla tavolozza | quanto i colori escono da quelli della casa | ΔE CIEDE2000 |
| terreni: ΔE dal vicino | se due terreni si distinguono (sotto 2,3 l'occhio non li separa) | ΔE CIEDE2000 |

```bash
# la scheda committata e il cancello della CI
python3 scripts/misura_resa.py --check            # nessuna misura peggiorata oltre il 5%
python3 scripts/misura_resa.py --aggiorna         # dopo un cambiamento voluto: riscrive la scheda

# una cartella di tessere candidate (con indice.json) contro i glifi
python3 scripts/misura_resa.py candidati CAND --registra
# la scelta: apri la pagina, scegli in ogni riquadro, scarica voti.json
python3 scripts/misura_resa.py coppie CAND [--anche CAND2] -o /tmp/scelta.html [--aperta]
python3 scripts/misura_resa.py voti ~/Scaricati/voti.json

# il tema texture si ritara da solo quando cambiano texture o renderer
python3 scripts/misura_resa.py tara && python3 scripts/dm.py maps texture
# a occhio: la stessa mappa con più velature (come per D16), e prima/dopo un cambiamento
python3 scripts/misura_resa.py velature '07_il Portale Della Forgia Eterna/Mappe/hammerfist-372-1372/M7-D-livello-1-1372.md' -o /tmp/velature.png
python3 scripts/misura_resa.py affianca MAPPA.svg --rispetto-a origin/main -o /tmp/prima-dopo.png
# cercare texture nuove nel catalogo di Poly Haven, dalla più scaricata
python3 scripts/build_texture_cc0.py --cerca roof slate
# i terreni che la velatura non separa (D27): candidati CC0 e scelta misurata
.venv/bin/python scripts/build_texture_cc0.py --candidati
python3 scripts/misura_resa.py tara --candidati asset-esterni/texture-candidate
```

**La pagina di scelta.** Ogni riquadro dice che cosa mostra: il simbolo, il
suo nome nella legenda e il terreno su cui è posato (per i terreni, il terreno
a sinistra e quello con cui si confonde a destra). Le opzioni identiche non
entrano, e la pagina dice quali ha tolto e perché: un simbolo che la legenda
tiene glifo, o una tessera senza webp, sarebbe la copia del glifo. Oltre alle
immagini ci sono due risposte:

- **Nessuna va bene**: quell'immagine si butta per quel simbolo. `--adotta` la
  toglie, e la elenca fra quelle da rifare (un'altra immagine di ComfyUI, un
  altro modello CC0); per un terreno, `--check` vuole che la texture sparisca
  da `TEXTURE` finché non se ne trova un'altra.
- **Non vedo differenze**: resta quella che costa meno, il glifo o la texture
  di oggi.

Con `--anche` la stessa pagina mette a confronto più fonti, per esempio le
tessere CC0 e quelle di ComfyUI accanto al glifo: è così che si vede se
ComfyUI migliora qualcosa. Alla cieca le immagini hanno solo una lettera, e le
fonti le rivela `voti` dopo che hai scelto; con `--aperta` la fonte e le misure
stanno sotto ogni immagine, per quando vuoi capire e non giudicare.

Il **secondo parere** (D26) sono le metriche apprese della community: CLIP-IQA,
LPIPS e DISTS di `piq`. Girano sulla tua macchina, perché vogliono torch e pesi
da scaricare, e non bloccano niente: sono tarate su fotografie, non su icone da
28 px.

```bash
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install "piq>=0.8"
.venv/bin/python scripts/misura_resa.py glifi --celle /tmp/celle -o /tmp/glifi.json
.venv/bin/python scripts/misura_resa_appresa.py /tmp/celle -o /tmp/appresa.json
python3 scripts/misura_resa.py appresa /tmp/appresa.json
```

**ComfyUI** (D25) è una terza fonte in prova. Il banco dei prompt chiede icone a
inchiostro e acquerello, lo stile della casa, su sfondo bianco:

```bash
python3 scripts/comfyui_batch.py --prompts plans/esperimenti/oggetti-cc0-2026-10/comfyui/PROMPT-OGGETTI-ZENITALI.md --serie tutto --out asset-esterni/oggetti-comfyui
python3 scripts/build_oggetti_cc0.py --da-immagini asset-esterni/oggetti-comfyui --variante a -o /tmp/cand-comfyui-a
python3 scripts/misura_resa.py candidati /tmp/cand-comfyui-a --registra
python3 scripts/misura_resa.py coppie scripts/oggetti-cc0 --anche /tmp/cand-comfyui-a -o /tmp/scelta.html
```

**Da zero, in ordine.** Tutto quello che tocca a te, sulla tua macchina, dal
ramo alla PR. I file scaricati vanno in `asset-esterni/` e nella cartella di
ComfyUI, che git ignora: restano lì anche se cambi ramo.

```bash
# 1) il ramo: gli strumenti stanno qui finché le PR #229 e #230 non entrano in main
git fetch origin resa-asset-misura-della-resa
git switch resa-asset-misura-della-resa
git status                     # se hai modifiche tue, prima: git stash

# 2) l'ambiente del repo (una volta): venv, dipendenze di sviluppo, Chrome per le misure
#    Debian 13: sudo apt install python3-venv chromium   (Python è già 3.13: bpy si installa)
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
python3 scripts/dm.py doctor   # deve trovare un Chromium o Chrome
.venv/bin/pip install bpy      # solo con Python 3.13; altrimenti --blender, §5.1.1

# 3) le texture dei terreni che si confondono (D27): scarica, misura, scegli tu
.venv/bin/python scripts/build_texture_cc0.py --candidati
python3 scripts/misura_resa.py tara --candidati asset-esterni/texture-candidate   # la misura propone
python3 scripts/misura_resa.py terreni-scelta asset-esterni/texture-candidate -o /tmp/terreni.html
#    apri /tmp/terreni.html: per ogni terreno la texture di oggi, le candidate e
#    «senza texture», ognuna accanto al terreno con cui si confonde; scarica voti.json
python3 scripts/misura_resa.py voti ~/Scaricati/voti.json
#    voti dice che riga mettere in TEXTURE (o togliere); build_texture_cc0 --check la fa valere

# 4) gli oggetti CC0: giro di prova e misura (§5.1.1); la scelta la fai al passo 6,
#    insieme alle icone di ComfyUI, oppure subito senza --anche se ComfyUI non c'è
.venv/bin/python -m pytest -q scripts/tests/test_blender_vero.py   # prima: la scena gira?
.venv/bin/python scripts/build_oggetti_cc0.py --prova
python3 scripts/misura_resa.py candidati scripts/oggetti-cc0 --registra

# 5) ComfyUI (D25), una volta: container, pesi, avvio. Se /home è piccolo,
#    prima export COMFYUI_DIR=/srv/comfyui (vale per tutti e quattro gli script)
scripts/comfyui-local/setup-distrobox.sh     # Debian: prima sudo apt install distrobox podman
scripts/comfyui-local/scarica-pesi.sh        # SDXL 1.0 base, ~6,9 GB, sha256 verificato
scripts/comfyui-local/start.sh               # in un altro terminale; resta acceso

# 6) le icone generate: 32 prompt; poi una pagina sola, glifo contro CC0 contro ComfyUI
python3 scripts/comfyui_batch.py --prompts plans/esperimenti/oggetti-cc0-2026-10/comfyui/PROMPT-OGGETTI-ZENITALI.md --serie tutto --modello sdxl --out asset-esterni/oggetti-comfyui
python3 scripts/build_oggetti_cc0.py --da-immagini asset-esterni/oggetti-comfyui --variante a -o /tmp/cand-comfyui-a
python3 scripts/misura_resa.py candidati /tmp/cand-comfyui-a --registra
python3 scripts/misura_resa.py coppie scripts/oggetti-cc0 --anche /tmp/cand-comfyui-a -o /tmp/scelta.html
#    apri /tmp/scelta.html, scegli in ogni riquadro (o «nessuna», o «non vedo differenze»)
python3 scripts/misura_resa.py voti ~/Scaricati/voti.json     # il browser può chiamarlo «voti (1).json»
#    voti rivela che cosa c'era dietro ogni lettera: lì vedi se ComfyUI ha vinto
python3 scripts/build_oggetti_cc0.py --adotta /tmp/cand-comfyui-a   # copia le ComfyUI scelte
python3 scripts/build_oggetti_cc0.py --adotta                       # sfoltisce le CC0 non scelte
#    --adotta stampa le righe di GENERATE e quelle da rifare: incollale nella chat

# 7) il secondo parere, facoltativo (D26): i comandi sopra, «secondo parere»
#    i pesi prima, da soli:  .venv/bin/python scripts/misura_resa_appresa.py --scarica-pesi

# 8) la verifica e il commit
python3 scripts/dm.py maps texture
.venv/bin/python scripts/gate_locale.py --rapido      # i gate della CI, in locale
python3 scripts/build_oggetti_cc0.py --check && python3 scripts/misura_resa.py --check && python3 scripts/validate_maps.py
git add scripts/oggetti-cc0 scripts/scheda-resa.json scripts/texture-cc0
git add -- '*rendered-texture/*.svg'
git commit -m "RESA-ASSET: tessere e texture adottate dopo la scelta del DM"
git push
```

Ci si può fermare dopo ogni passo, ma prima del passo 8 il repo non è pronto
per un commit: le tessere nuove cambiano gli SVG texture, e `validate_maps`
passa solo dopo `maps texture`. Il passo 5 non è mai stato provato su una
macchina vera. Se `setup-distrobox.sh` si ferma,
incolla l'errore nella chat.

### 5.2 Il tema dipinto con 2-Minute Tabletop (opzionale, solo per il tuo tavolo)

È una seconda resa della stessa mappa con tessere dipinte a mano, per i
giocatori e per Foundry. Non è la strada principale (lo è §5.1): la licenza
non permette di pubblicarla. Il DM ha deciso di provarla su una mappa sola
prima di farne un lotto (D9 di
[PIANO-RESA-E-ASSET](../../plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md)).

**Cosa si può usare.** La licenza (pagina «General Licensing and Attribution»
del sito, letta il 2026-10-09) divide i pacchetti in due categorie, e pagare
non sposta un pacchetto dall'una all'altra:

| Categoria | Esempi | Licenza | Uso |
|---|---|---|---|
| `base` | *Dungeon Map Tiles* a offerta libera, anche a 0 $ | CC BY-NC 4.0 | tavolo privato; progetti gratuiti col credito su ogni pagina in cui compare la mappa |
| `premium` | pacchetto *Plus* da 5 $, Patron Pack, avventure, token | nessuna licenza | solo al tavolo e in video; niente che esca dal repo |

L'unica eccezione commerciale dell'autore riguarda i moduli scritti in cui le
mappe sono un supplemento (una ogni 2.000 parole circa), col credito su ogni
pagina e, per un progetto preciso, un suo permesso scritto.

**Il download lo fai tu.** Anche i pacchetti gratuiti passano dalla cassa del
sito e i link arrivano per email: nessuno script li scarica. I file restano
sulla tua macchina, in `asset-esterni/`, che git ignora.

```bash
# 1) scarica dal sito il pacchetto base dei dungeon (Dungeon Map Tiles, 0 $)
# 2) installalo dichiarando la categoria
python3 scripts/dm.py asset installa ~/Scaricati/Dungeon-Map-Tiles.zip --categoria base
# 3) cosa c'è
python3 scripts/dm.py asset stato
# 4) dopo aver scritto la tabella simbolo → file in scripts/asset-2mtt.json
python3 scripts/dm.py asset controlla
```

L'installatore estrae solo immagini e testi di licenza, e rifiuta uno zip con
percorsi assoluti, `..` o link. `controlla` boccia la tabella se un simbolo
punta a un pacchetto `premium` o a un file che non c'è. `dm.py doctor` dice
quali pacchetti hai.

**Cosa manca ancora.** La tabella `scripts/asset-2mtt.json` è vuota: si scrive
sui nomi veri dei file, dopo la prima installazione. Poi viene la mappa di
prova, che in Foundry entra come immagine di sfondo dell'export UVTT
(`--image`), con muri, porte e luci di sempre.

### 5.3 La pianta di una città con Watabou (R5)

Il Medieval Fantasy City Generator di Watabou fa la pianta d'insieme di una
città: un'immagine per il DM o per i giocatori, non una griglia tattica. Le sue
mappe si usano liberamente, anche a scopo commerciale. Il generatore legge seme
e parametri dall'URL, e una scheda committata li conserva, così la pianta si
rifà identica.

```bash
# l'URL della pianta di Dauth assediata, con l'esportazione in SVG
python3 scripts/dm.py maps citta "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Mappe/dauth-assedio/dauth-pianta.watabou.json" --export svg
```

Apri l'URL nel browser: il generatore disegna la città ed esporta l'SVG. Salvalo
dove dice la scheda (`salva_in`). Se la città non ti piace, cambia `seed` nella
scheda e rigenera: il seme nuovo resta scritto. Nella scheda, `perche` dice da
quale carta dell'assedio viene ogni parametro e quali il canone non fissa.

Le cinque mappe tattiche dell'assedio (carte A-E) sono griglie del repo, in
`Mappe/dauth-assedio/`, compilate dai loro contratti JSON e collaudate.

---

## 6. La regola d'oro (e perché la CI ti ferma)

`validate_maps.py` (in CI a ogni PR) verifica tre cose:

1. **ben formati**: ogni SVG in `rendered/` è XML valido;
2. **provenienza**: ogni SVG ha il suo master `.md` accanto (niente orfani);
3. **in sync**: ri-renderizzando il master si riottengono **gli stessi byte**.

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
| Nel VTT mancano i muri | quelle celle non sono simboli-muro riconosciuti (🏰 ⬛ ⛺ ⛰ 🟪 🗼 🏛 🗿) → correggi la griglia e riesporta |
| `export_map_png` non parte | serve **uno** fra Inkscape (`dnf`/`apt install inkscape`) e Chromium headless → vedi [GUIDA-BOOKLET-E-PDF §2](GUIDA-BOOKLET-E-PDF.md#2-prerequisiti), o passa `--inkscape`/`--browser` |
| Il PNG ha etichette storte o tratteggi sbagliati | è il browser che impagina l'SVG come pagina web → `--renderer inkscape` (rasterizzatore SVG vero) |
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
