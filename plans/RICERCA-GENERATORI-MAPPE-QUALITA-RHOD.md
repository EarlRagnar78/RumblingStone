# 🗺️ RICERCA — GENERATORI DI MAPPE OPEN SOURCE PER QUALITÀ "RHoD"

> **Cos'è**: censimento ragionato (2026-07-12) dei progetti GitHub/open source
> in grado di produrre o migliorare mappe di gioco con qualità paragonabile
> alle battle map ufficiali di *Red Hand of Doom* e delle migliori app
> D&D/Pathfinder (DungeonDraft, Dungeon Scrawl, DungeonFog), e valutazione di
> **quali sono integrabili nella pipeline mappe di RumblingStone**.
>
> **Non è un piano**: è l'input di ricerca per un eventuale futuro
> `PIANO-UPGRADE-QUALITA-MAPPE`. Nessun lotto, nessuna checklist.
>
> Engine: Fable 5 · Sessione: 2026-07-12.

---

## 1. Punto di partenza — la pipeline attuale

La pipeline mappe del repo (censita in `MAPPE-CENSIMENTO.md`) è:

1. **Master**: griglie emoji in fenced code block dentro i file Markdown
   (`*Ultra-Clear*.md`, `*MAPPE*.md`, …) — leggibili, diffabili, usabili al
   tavolo.
2. **Renderer**: `scripts/render_map_svg.py` (Python puro, zero dipendenze)
   → SVG con palette piatta, griglia 1,5 m/quadretto, coordinate, legenda,
   scala.
3. **Regola d'oro**: il Markdown è il master, l'SVG è un artefatto generato e
   **mai** editato a mano.

Il gap rispetto alle mappe RHoD ufficiali (illustrate a colori, texture
disegnate a mano, ombre, profondità) è quindi **tutto nel renderer e negli
asset grafici**, non nel formato dati: le griglie contengono già terreno,
strutture, unità e pericoli cella per cella. Qualsiasi soluzione che
sostituisse il formato master romperebbe censimento, validazione
(`validate_maps.py`), companion T3 e diffabilità — ed è da scartare a priori.

---

## 2. Progetti censiti

### 2.1 Generatori di layout / mappe

| Progetto | Licenza | Cosa produce | Qualità output | Integrabilità in RumblingStone |
|---|---|---|---|---|
| [Watabou One Page Dungeon](https://watabou.github.io/dungeon.html) ([itch.io](https://watabou.itch.io/one-page-dungeon)) | Freeware, **non** open source, ma con export **JSON/SVG/PNG documentato** | Layout dungeon completi (stanze, corridoi, porte, note) in stile hand-drawn | ⭐⭐⭐⭐ molto vicino alle mappe "one page" professionali | **Alta** — il JSON è una semplice lista di rettangoli+porte; convertitore JSON→griglia-emoji fattibile in ~200 righe Python |
| [Azgaar/Fantasy-Map-Generator](https://github.com/Azgaar/Fantasy-Map-Generator) | **MIT** | Mappe regionali/mondo interattive (fiumi, biomi, città, stati, etichette) | ⭐⭐⭐⭐⭐ per scala overland — livello atlante professionale | **Media** — perfetto per la mappa regionale (Dalelands/Cannath Vale), non fa battle map; export SVG/PNG/JSON |
| [watabou/TownGeneratorOS](https://github.com/watabou/TownGeneratorOS) (+ [versione web](https://watabou.github.io/city-generator/)) | Sorgente open (Haxe); versione web più ricca ma chiusa, con export SVG/PNG/JSON | Piante di città/villaggi medievali con quartieri, mura, strade | ⭐⭐⭐⭐ | **Media** — ideale per Rethmar, il Palio (P2D) e i centri abitati; la versione web basta come tool esterno |
| [Adrian104/Dungeon-Generator](https://github.com/Adrian104/Dungeon-Generator) | Open source (C++) | Layout BSP geometrici (stanze+percorsi, solo coordinate) | ⭐⭐ solo geometria, nessuna estetica | Bassa — non aggiunge nulla rispetto a scrivere griglie a mano con un LLM |
| [amishne/mipui](https://github.com/amishne/mipui) | **MIT** | Editor collaborativo di mappe a griglia (web); importa il JSON di Watabou | ⭐⭐⭐ stile pulito ma schematico | Bassa come generatore (è un editor); utile solo come tappa manuale |
| [MapTool (RPTools)](https://www.rptools.net/toolbox/maptool/) | Open source | VTT completo (fog of war, token, luci) | n/a (non genera mappe) | Fuori scope — serve per *giocare* le mappe, non per generarle |
| [Dungeon Scrawl](https://www.dungeonscrawl.com/) | Gratuito ma **closed** (ora Roll20) | Battle map stile inchiostro/hatching di alta qualità; importa il JSON di Watabou | ⭐⭐⭐⭐⭐ | Bassa per automazione (solo GUI) — buon passo manuale opzionale |

Convertitori esistenti del JSON di One Page Dungeon (dimostrano che il formato
è stabile e facilmente parsabile — utili come riferimento):

- [TarkanAl-Kazily/one-page-parser](https://github.com/TarkanAl-Kazily/one-page-parser) — modulo FoundryVTT che costruisce scene dal JSON+PNG di Watabou.
- [Dungeondraft Watabou Integration (GitLab)](https://gitlab.com/gull-rock-maps/dungeondraft-watabou-integration) — JSON Watabou → file mappa DungeonDraft.
- [Import Watabou One Page Dungeon (CartographyAssets)](https://cartographyassets.com/assets/52353/import-watabou-one-page-dungeon/) — idem, tool free.

### 2.2 Asset grafici con licenza compatibile (per alzare la qualità del renderer)

| Fonte | Licenza | Stile | Note |
|---|---|---|---|
| [Kenney — Roguelike Caves & Dungeons](https://kenney.nl/assets/roguelike-caves-dungeons) (520 tile) e [Roguelike/RPG pack](https://kenney.nl/assets/roguelike-rpg-pack) (1.700 tile) | **CC0** | Pixel/flat pulito | Zero vincoli: committabili nel repo, incorporabili negli SVG come data-URI. Stile però "videogame", non RHoD |
| [2-Minute Tabletop — asset gratuiti](https://2minutetabletop.com/product-category/free/) ([licenza](https://2minutetabletop.com/faq/license-and-attribution/)) | **CC BY-NC 4.0** | **Hand-drawn painterly — il più vicino in assoluto alle mappe RHoD ufficiali** | OK per una campagna non commerciale con attribuzione visibile accanto alla mappa; da NON usare se il repo diventasse commerciale |
| Texture procedurali SVG (`<pattern>`, `<filter feTurbulence>`, hatching) | n/a (generate dal nostro codice) | Carta/pergamena, pietra, acqua, erba | Nessun asset esterno, nessun vincolo, pesa pochi KB; qualità "Dungeon Scrawl-like" raggiungibile |

### 2.3 Scartati e perché

- **DungeonDraft / Wonderdraft / DungeonFog / Inkarnate**: qualità massima ma
  commerciali, closed source, asset non ridistribuibili → non integrabili in
  una pipeline rigenerabile da repo.
- **Generatori AI di battle map** (tt-rpg.app e simili): output non
  deterministico, non rigenerabile, licenze d'uso incerte, nessuna coerenza
  con la griglia tattica 1,5 m — incompatibili con la regola "il Markdown è
  il master".
- **Sostituire il formato master** con qualunque formato proprietario:
  romperebbe censimento T5, validazione CI e companion T3.

---

## 3. Raccomandazione

Nessun progetto esterno, da solo, produce battle map RHoD-quality *a partire
dalle griglie emoji esistenti* — quel pezzo non esiste su GitHub e va fatto in
casa. La combinazione più efficace è **ibrida, in 3 fasi indipendenti**
(ordinate per rapporto qualità/sforzo):

### Fase 1 — Upgrade grafico di `render_map_svg.py` (impatto massimo)

Evolvere il renderer da "fill piatti" a battle map illustrata, mantenendo
identici master, CLI e output path (tutte le ~30 mappe censite si rigenerano
da sole):

- texture per i 13+ simboli terreno via `<pattern>` SVG: procedurali
  (feTurbulence per pietra/terra/acqua, hatching per muri) e/o tile CC0
  Kenney incorporati come data-URI;
- bordi morbidi tra terreni adiacenti (merge di celle contigue in path unici,
  angoli smussati), ombre portate su muri/strutture, vignettatura pergamena;
- token unità con anello colorato + iniziale (stile VTT professionale) invece
  del cerchio piatto;
- opzionale `--style 2mtt` che usa asset 2-Minute Tabletop (CC BY-NC, con
  blocco attribuzione automatico nella legenda) per il look hand-drawn RHoD.

### Fase 2 — `scripts/import_watabou.py` (nuovi dungeon di qualità)

Convertitore **JSON One Page Dungeon → griglia emoji Markdown** conforme a
`campaign/templates/mappa-tattica-template.md` (scala dichiarata, righe
numerate, blocchi companion vuoti da compilare). Riferimento implementativo:
`one-page-parser` (il JSON è una lista di rect+porte). Così i nuovi dungeon
nascono con layout professionale ma restano nel toolchain del repo
(validazione, censimento, rendering Fase 1).

### Fase 3 — Mappe di scala superiore (overland e città)

- **Azgaar Fantasy-Map-Generator** (MIT) per la mappa regionale del
  Cannath Vale / Dalelands — file `.map` committato come master +
  export SVG/PNG in `rendered/`;
- **Medieval Fantasy City Generator** (Watabou, sorgente `TownGeneratorOS`)
  per Rethmar e le location urbane (Palio P2D) — export SVG committato con
  seed annotato per la rigenerazione.

### Rischi / attenzioni

- **Licenze**: solo CC0 (Kenney, texture procedurali) può entrare nel repo
  senza condizioni; CC BY-NC 4.0 (2MTT) richiede attribuzione e vieta uso
  commerciale; gli asset Forgotten Adventures free NON sono ridistribuibili
  in un repo pubblico.
- **Peso repo**: incorporare texture come data-URI negli SVG li ingrossa;
  mitigazione: pattern definiti una volta sola per file + `Image-to-webp`
  già presente in `Script/` per eventuali raster.
- **Watabou 1PD non è open source**: si dipende dal formato JSON (stabile da
  anni, con 3 convertitori terzi attivi), non dal codice.
