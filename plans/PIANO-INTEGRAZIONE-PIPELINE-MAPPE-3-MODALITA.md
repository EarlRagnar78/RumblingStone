# 🗺️ PIANO — INTEGRAZIONE PIPELINE MAPPE (3 MODALITÀ) + INFRA CONTAINER

> **Cos'è**: analisi + implementazione dell'integrazione richiesta dal DM
> (2026-07-19) per portare a un risultato *professionale* la generazione mappe,
> partendo da una conversazione esterna che proponeva: 3 modalità di pipeline,
> validazione JSON rigida (vs arte ASCII instabile), export VTT nativo
> (Foundry/Roll20), infra container per l'IA immagini locale su Bazzite, e la
> direzione artistica "stile manuale Pathfinder 1E".
>
> **Metodo**: prima **analisi** (cosa esiste già nel repo, cosa manca, cosa
> della proposta è valido vs superato), poi **implementazione** dei soli pezzi
> mancanti e coerenti con l'architettura esistente.
>
> Engine: Opus 4.8 · Sessione: 2026-07-19 · Branch: `claude/map-generation-pipeline-7ka5a7`.

---

## 0. Sintesi per il DM (TL;DR)

La proposta esterna era per lo più **corretta come principi** ma **assumeva un
repo vuoto**: dava per mancanti cose che RumblingStone ha già da tempo (renderer
SVG deterministico, import Watabou, export PNG, homebrewery self-hosted, prompt
AI cinematografici, gate CI). Il vero valore aggiunto era **3 pezzi**:

1. **Contratto JSON rigido + validatore** al posto dell'arte ASCII (Modalità 3).
2. **Export UVTT/dd2vtt** per import nativo in Foundry/Roll20 (muri + luci).
3. **Infra container** per l'IA immagini locale senza toccare l'OS immutabile.

Questi 3 sono stati implementati. La "direzione artistica Wayne Reynolds" è
stata reinterpretata **entro i confini IP** (convenzioni di genere, non clone di
un artista vivente). Un solo scostamento dalla proposta: **niente dipendenza
`pydantic`** — la validazione è in stdlib puro, come tutto il resto del repo.

---

## 1. Analisi — cosa esiste GIÀ (e non va rifatto)

La pipeline mappe è matura (censita in `plans/RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md`
e in `MAPPE-CENSIMENTO.md`). Stato al 2026-07-19:

| Pezzo | Dove | Stato |
|---|---|---|
| Formato MASTER griglia emoji → SVG "pergamena" deterministico | `scripts/render_map_svg.py` (1200+ righe) | ✅ maturo |
| Export PNG hi-res (stampa/VTT/input hero) | `scripts/export_map_png.py` | ✅ |
| Import generatori gratuiti (Watabou One Page Dungeon JSON) | `scripts/import_watabou.py` | ✅ |
| Suggeritore template tattici | `scripts/suggest_map.py` + `map_templates/*.yaml` | ✅ |
| Gate CI coerenza master↔SVG (deterministico) | `scripts/validate_maps.py` | ✅ in `ci.yml` |
| Prompt AI **cinematografici** per handout/video (per arco) | `campaign/ai-media-prompts/*.md` | ✅ |
| Passata pittorica "hero map" (img2img+ControlNet+MCP) | `skills/.../hero-map-comfyui.md` | ✅ documentata |
| Homebrewery self-hosted (nativo + Docker) | `scripts/homebrew-local/`, `dm.py hype` | ✅ (ADR-0004) |
| Confini IP (uso non commerciale) | `plans/adr/ADR-0005-*` | ✅ |

**Conseguenza**: le affermazioni della conversazione esterna del tipo "i tuoi
script falliscono perché fai il parsing dell'ASCII" **non si applicano** a
questo repo — qui il master è griglia emoji strutturata, non ASCII libera, ed è
già validato in CI. La proposta di "sostituire il parser di stringhe" era già
realizzata di fatto.

---

## 2. Analisi — cosa MANCAVA davvero (i gap reali)

| Gap | Perché serve | Modalità |
|---|---|---|
| **G1 — Contratto JSON + validatore** per far progettare mappe a un LLM senza slittamenti | Un LLM che scrive la griglia emoji a mano può ancora sbagliare una cella; un JSON validato con coordinate/simboli/geometria elimina la classe di errori e crea il loop "rigetta → correggi" | 3 |
| **G2 — Astrazione per unità/aree** per gli eserciti | Posizionare ogni soldato satura il contesto; i moduli Paizo (e le armate ARC-00/08 del repo) ragionano per unità | 3 |
| **G3 — Export UVTT/dd2vtt** | Il repo produce SVG/PNG ma non il JSON nativo che Foundry/Roll20 importano con muri (LOS) e luci già pronti | 1 e 3 |
| **G4 — Infra container IA immagini su Bazzite** | `hero-map-comfyui.md` diceva "installa ComfyUI" ma non come farlo su un OS **immutabile** senza stratificare pacchetti | 2 |
| **G5 — Modello mentale "3 modalità"** esplicito | I 3 flussi esistevano sparsi; mancava un unico riferimento "quale uso quando" + system prompt per LLM | tutte |
| **G6 — Direzione artistica "manuale PF1e"** IP-safe | Domanda del DM; va data come *convenzioni*, non clone di artista vivente | 2 |

**Non-gap (scartati con motivo)**:

- **Dipendenza `pydantic`**: superflua e contraria alla filosofia del repo
  (stdlib puro, `ci.yml` installa solo `pyyaml`). Validazione fatta in stdlib.
- **Sostituire il formato master** con `.uvtt`/proprietari: romperebbe
  censimento, `validate_maps.py`, companion T3 e diffabilità (già escluso nella
  RICERCA §2.3). L'UVTT è un *export*, non il master.
- **Generatori AI di battle map end-to-end**: output non deterministico,
  incoerente con la griglia 1,5 m (già escluso). La passata IA resta ancorata
  al master (hero map, img2img+ControlNet).
- **Watabou/Donjon/MFCG come "novità"**: Watabou è già integrato; Donjon/MFCG
  restano tappe esterne documentate (RICERCA §2.1, §3 Fase 3).

---

## 3. Implementazione (questa PR)

### Lotto M1 — Contratto JSON + compilatore (G1, G2) ✅
- `scripts/schemas/tactical_map.schema.json` — schema draft-07 del contratto
  (map_size, regions, structures, hazards, lights, units, notes).
- `scripts/compile_map_json.py` — validatore **stdlib** (coordinate in bounds,
  simboli nella legenda universale, geometria) + compilatore JSON → master
  griglia-emoji con i 3 blocchi companion e tabella **FORZE** (astrazione per
  unità: `area` + `quantity`, non un token per soldato). `--validate-only`
  implementa il loop "rigetta → correggi".
- `scripts/examples/esempio-accampamento-mano-rossa.json` (+ README) — esempio
  giocabile della campagna (accampamento Mano Rossa).

### Lotto M2 — Export UVTT/dd2vtt (G3) ✅
- `scripts/export_uvtt.py` — dal master emoji estrae **muri** (edge-tracing
  cella-per-cella + merge di run collineari → `line_of_sight`), **porte**
  (`portals`), **luci** (da bracieri/candele/fuochi o dalle `lights` esplicite),
  `resolution` con `pixels_per_grid`. Riusa il parser di `render_map_svg.py`.
  Output `.uvtt`/`.dd2vtt` per **import nativo Foundry/Roll20**.

### Lotto M3 — Infra container IA immagini su Bazzite (G4) ✅
- `scripts/comfyui-local/` (mirror di `homebrew-local/`): `README.md` con Via A
  **Distrobox `--nvidia`** (consigliata su OS immutabile) e Via B Docker/Podman;
  `setup-distrobox.sh` / `start.sh` / `stop.sh` (wrapper sottili, comandi
  ufficiali). Clone e pesi **gitignorati**, host immutabile mai toccato.

### Lotto M5 — Overlay professionale mappe (bussola, movimenti, callout, zone) ✅
> Follow-up del 2026-07-19: richiesta DM di rendere "professionale" l'output —
> posizioni, movimenti, leggende e **orientamento a Nord** — sulle mappe drow
> Ultra-Clear (quest di Hella).
- `render_map_svg.py`: direttive `@` opzionali nel blocco griglia (dopo le
  righe) → **bussola** (sempre, `@north` la ruota), **rotte di movimento**
  tratteggiate con freccia (`@path`), **roster numerato** sui token (`@mark`),
  **zone etichettate** (`@zone`), più una legenda **INDICAZIONI**. Deterministico,
  XML valido. Cfr. **ADR-0006**.
- `compile_map_json.py` + schema: nuovi campi `north` e `movements`; il
  compilatore emette le direttive dal JSON (roster dai `name`/`cr`, zone dai
  `label`). Coordinate esatte per costruzione (nessun drift ASCII).
- Esempio committato + validato: `scripts/examples/campo-drow-1.*`
  (ricostruzione "Campo Drow 1"): token alle coordinate dichiarate (14/14),
  mentre l'ASCII a mano originale ne aveva 4/14 (drift ~1 quadretto).
- Tutti i 16 SVG committati rigenerati (bussola globale); `validate_maps` verde.

### Lotto M4 — Documentazione e modello mentale (G5, G6) ✅
- `skills/rumblingstone-mapmaking/references/tre-modalita-mappe.md` — le 3
  modalità, il contratto JSON, il **system prompt per l'LLM**, i formati di
  consegna (SVG/PNG/UVTT).
- `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md` —
  direzione artistica per convenzioni + **box confini IP** (no clone di artisti
  viventi; coerente con ADR-0005 e hero-map §"Cosa NON fare").
- Aggiornati `SKILL.md` (3 modalità, tool, trigger), `scripts/README-automation.md`
  (righe tabella), `.gitignore` (clone ComfyUI + export vtt/png), `ci.yml`
  (smoke test dei nuovi script).

---

## 4. Checklist

- [x] M1 — schema JSON + `compile_map_json.py` + esempio (round-trip testato: JSON→master→SVG)
- [x] M2 — `export_uvtt.py` (testato: 20 muri / 1 porta / 2 luci sull'esempio)
- [x] M3 — `scripts/comfyui-local/` (README + 3 wrapper, syntax-checked)
- [x] M4 — 2 reference skill + aggiornamenti SKILL.md/README-automation/.gitignore/ci.yml
- [x] M5 — overlay professionale (bussola/movimenti/callout/zone) in renderer+compilatore; ADR-0006; esempio `campo-drow-1.*`; 16 SVG rigenerati
- [x] Gate locali verdi: `compileall`, `validate_maps.py`, `validate_skills.py`
- [ ] **Collaudo al tavolo (DM, gated)**: (a) generare una mappa Mod. 3 reale
      da JSON per un incontro di ARC-08/09 e renderla; (b) importare un `.uvtt`
      in Foundry e verificare muri/luci; (c) collaudo container ComfyUI su
      Bazzite con GPU (setup-distrobox → hero map su una mappa chiave).

## 5. Rischi / attenzioni

- **UVTT è un export, non il master** — non committarlo, non validarlo in CI
  (gitignorato). Il master resta la griglia emoji.
- **`pixels_per_grid`**: default 100 nel `.uvtt`; se si incorpora un PNG di
  sfondo, esportarlo alla stessa risoluzione (`export_map_png.py --scale`) e
  passare `--ppg` coerente, altrimenti la griglia Foundry non combacia.
- **Confini IP** (ADR-0005): la direzione artistica descrive convenzioni, mai
  cloni di artisti viventi né asset di terzi come style reference.
- **Pesi/modelli IA**: mai nel repo (gitignorati). Solo checkpoint aperti
  (SDXL/Flux-dev) per uso non commerciale.
