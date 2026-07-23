# 🗺️ PIANO — RENDERER MAPPE A FEDELTÀ PIENA (ASCII ultra-clear → SVG senza perdite)

> **Cos'è**: il piano per portare `scripts/render_map_svg.py` a rendere le
> mappe **senza perdere** nulla di ciò che l'ASCII ultra-clear porta con sé —
> posizioni dei token, **annotazioni a lato-riga**, etichette tattiche, quote,
> zone. Finché il renderer non è fedele, **l'ASCII resta lo standard canonico**
> e l'SVG è un artefatto derivato futuro.
>
> **Origine**: audit mappe ARC-07 (2026-07-23) + decisione DM: *«voglio anche
> l'ASCII ultra-clear, perché il render perde posizioni e altri dettagli che
> servono; per ora si resta sull'ASCII std con tutti i dettagli, che in futuro
> verrà reso.»*
>
> **Non duplica** ma **estende** la pipeline esistente
> ([INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md),
> [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md)): quelle
> hanno dato il renderer "pergamena" e le 3 modalità; qui si chiude il **gap di
> fedeltà** emerso al test di rendering dei master DEF.
>
> Skill di dominio: `rumblingstone-mapmaking`. Regola d'oro dei piani: chi chiude
> un lotto aggiorna checklist + `plans/INDEX.md` + `plans/CHANGELOG.md`.

---

## §0 — Decisione permanente (canone DM 2026-07-23)

- **L'ASCII ultra-clear è la fonte MASTER e lo standard da tavolo.** Porta tutti
  i dettagli (coordinate, token, annotazioni, tattiche) in forma leggibile e
  diffabile. **Non si degrada** per farlo entrare nel renderer.
- **L'SVG è un derivato.** Si genera **solo quando** il renderer è fedele al
  100% (questo piano). Fino ad allora, le mappe dei master DEF restano ASCII.
- Le mappe **già rese** (`Mappe/rendered/`, dai master `L1/L2-UltraClear`)
  restano valide: erano scritte al contratto di resa.

---

## §1 — Diagnosi del gap (dal test di rendering, 2026-07-23)

Renderizzando una griglia embedded di un master DEF (Cuore della Montagna) sono
emersi 4 difetti di **fedeltà** (non di estetica — la pergamena è bella):

1. **Annotazioni a lato-riga → colonne fantasma.** Le griglie ultra-clear
   mettono la legenda *a destra della riga* (`… 🪨 🪨   🚪 PORTE DI MITHRAL`).
   Il parser le legge come celle extra → token duplicati e prop fluttuanti a
   destra (nel test: un cluster-PG e un altare in più nelle colonne U-X).
2. **Quote intestazione ≠ celle reali.** L'header dichiara `20 col × 16 righe`
   ma il parser conta `24×10`: nessuna riconciliazione, nessun errore.
3. **Mappe non-rettangolari ignorate.** Griglie **esagonali** o **schematiche**
   (orizzonti, percorsi) non vengono rilevate come rendibili.
4. **Etichette/token semantici persi.** I simboli locali (🧲 magnetite, 🌫️
   zero-G, 🤖 Sentinella) rendono come emoji grezzi «simbolo locale», senza la
   loro **funzione tattica** (copertura, terreno difficile, letale).

**Causa comune**: il renderer tratta la griglia come *solo* matrice di celle e
non ha un canale per **annotazioni/token semantici** separati dalla matrice.

---

## §2 — Verdetto sull'idea «estrarre il layout dalle webp RHoD» (feasibility)

> Il DM ha chiesto: *si può usare qualche webp originale della campagna RHoD
> come esempio standard di buona mappa? Immagino non esista un tool che estragga
> layout architettonico, asset e tipo di mappa per replicarla.*

**Verdetto onesto: corretto, non esiste (in modo affidabile) e non è la strada.**

- Estrarre **muri/stanze/griglia** da un raster `.webp` è un problema di
  *vectorization / semantic segmentation*: esistono ricerche (e strumenti come
  Dungeon Scrawl per il disegno **manuale**, non l'estrazione), ma **nessun tool
  open source affidabile** ricostruisce layout+asset+tipo da un'immagine di
  mappa in un contratto griglia utilizzabile. L'output sarebbe rumoroso e da
  correggere a mano più che ridisegnare.
- Le **webp RHoD restano un BENCHMARK visivo** (il "a che livello puntare"),
  **non un input** da auto-convertire. Le usiamo come riferimento di qualità
  quando un umano/LLM **autora** la griglia ultra-clear, esattamente come già
  fa la skill `rumblingstone-mapmaking`.
- **La strada giusta** è l'opposto: rendere il renderer capace di consumare la
  **nostra** ASCII ricca (che già contiene tutto) **senza perdite** (§3). Il
  dettaglio è già nostro; manca solo un renderer che non lo butti via.

Benchmark disponibili in repo (`00_Red Hand Of Doom/Immagini/Area Map/…/MappeIncontri/`):
`vraath-keep-numbers*.webp`, `Vraath-Keep-Overhead-Players-Battle-Map-Grid*.webp`,
`resh_town_all_new.webp`, `The Fane of Tiamat_lower_battle.webp`, ecc.

---

## §3 — Fasi (con engine consigliato + livello d'impegno)

> Routing engine per fase (regola `rumblingstone-plans`): NON è un gate CI.

| Fase | Obiettivo | Engine | Impegno |
|---|---|---|---|
| **F1 — Contratto ASCII v2 "annotato"** | Formalizzare un formato in cui la **matrice** (celle) è separata dalle **annotazioni** (blocco `# NOTE:` o colonna-delimitata) e dalle **quote**; un token-map locale (simbolo→funzione) dichiarato nel file. Retro-compatibile: le mappe attuali si adeguano senza riscriverle. | Opus (design) | Medio |
| **F2 — Parser fedele** | `render_map_svg.py`: riconoscere il delimitatore di fine-matrice (niente colonne fantasma), **validare header-dims vs celle** (errore se divergono), ignorare le annotazioni come testo. | Sonnet | Medio |
| **F3 — Callout & legenda semantica** | Rendere le annotazioni come **callout ancorati** (freccia dalla nota alla cella), e i token locali con la **funzione** in legenda (copertura +N, terreno difficile, letale) — leggendo il token-map di F1. | Opus (resa) + Sonnet (impl.) | Alto |
| **F4 — Griglie non-rettangolari** | Supporto **esagonale** e **schematico** (o marcatura esplicita `render: none` per le mappe-diagramma che NON vanno rese). | Sonnet | Medio |
| **F5 — Passata ARC-07** | Adeguare le 12 mappe dei master DEF al contratto v2 e **rendere** gli SVG a stampa in `Mappe/rendered/`, con confronto a occhio vs benchmark webp RHoD. | Opus (QA) | Alto |
| **F6 — CI** | Estendere `validate_maps.py`: se una mappa dichiara `render: true`, l'SVG deve esistere ed essere in sync; header-dims obbligatorie e coerenti. | Sonnet | Basso |

---

## §4 — Gate & definizione di "fatto"

- **Fedeltà**: una mappa resa **non perde né aggiunge** alcun token/annotazione
  rispetto all'ASCII (diff semantico manuale su 3 mappe campione, incluse una
  esagonale e una con annotazioni fitte).
- **Qualità**: confronto a occhio con ≥2 benchmark webp RHoD → «pari o meglio».
- **Non-regressione**: i 17 SVG esistenti restano byte-identici (o rigenerati
  volutamente), `validate_maps` verde.
- **Standard invariato**: l'ASCII resta la fonte; l'SVG è generato da essa.

## §5 — Stato

🔵 **APERTO — non iniziato.** È un task **futuro** su richiesta DM: l'ASCII
ultra-clear resta lo standard operativo *ora*; questo piano si esegue quando si
vuole la resa a stampa fedele. Nessun lotto ancora chiuso.
