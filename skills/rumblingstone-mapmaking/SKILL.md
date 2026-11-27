---
name: rumblingstone-mapmaking
description: >
  Pipeline delle mappe tattiche di RumblingStone (battle map): crea, modifica e
  rende le mappe a qualità AP (riferimento Red Hand of Doom / Paizo). Copre le
  3 modalità di mappa, il master a griglia emoji, il contratto JSON, la
  legenda, il renderer a pergamena, l'export VTT e la hero map ComfyUI
  facoltativa. Da usare per "mappa", "battle map", "griglia tattica",
  "battlemap", "render SVG", "nuova mappa", "import watabou", "hero map",
  "mappa regionale", "mappa città", "mappa esercito", "assedio",
  "accampamento", "coordinate", "JSON mappa", "contratto JSON",
  "compile_map_json", "export UVTT", "uvtt", "dd2vtt", "Foundry", "Roll20",
  "muri e luci", "mappa cinematografica", "handout", "audit mappe", "atlante
  mappe", "mappe definitive", "parity pass mappe", "consolidamento mappe",
  "MAPPE-DEFINITIVO", "posizionamenti canonici", per i file *MAPPE* o
  *Ultra-Clear*, e per render_map_svg, import_watabou, compile_map_json,
  export_uvtt, validate_maps.
---

# RumblingStone — Pipeline delle mappe

Ogni mappa tattica è una **griglia emoji in markdown** (il MASTER: leggibile,
confrontabile, giocabile) resa in SVG **«pergamena»** da stampa da
`scripts/render_map_svg.py` (terreni organici, ambient occlusion, oggetti
vettoriali originali, griglia da 1,5 m/quadretto, legenda, barra di scala). Gli
SVG in `rendered/`, accanto al master, sono **generati: mai a mano**; la CI
(`scripts/validate_maps.py`) li vuole deterministici, identici byte per byte.

## Quando no

Impaginare il volume: `rumblingstone-editoria` §4 (qui solo colonna o A4,
regola 7). Le altre forme d'uscita: `editoria` · `edizione` · `art-direction`
(riga L3 di `AGENTS.md`).

## Fonti

Guida passo passo per umani (modalità, comandi, export VTT, problemi):
[`docs/how-to/GUIDA-MAPPE.md`](../../docs/how-to/GUIDA-MAPPE.md); questa skill
è la reference operativa per gli agenti.

| Compito | Reference |
|---|---|
| **Audit/consolidamento mappe di un arco** (atlante definitivo, fonti canoniche, add-on DM, render+verifica) | `references/audit-mappe-workflow.md` |
| Le 3 modalità, contratto JSON, system prompt LLM | `references/tre-modalita-mappe.md` |
| **Migrare un ultra-clear esistente → bozza JSON + report conflitti** (`import_ultraclear.py`) | `references/import-ultraclear.md` |
| Flusso completo: mappa nuova, modifica, render, validazione, import di dungeon, regionale/città | `references/workflow-mappe.md` |
| Legenda universale: ogni simbolo di terreno, unità, oggetto, col significato | `references/legenda-universale.md` |
| **Collaudo**: la mappa si gioca? lo strumento, le direttive `@`, il ruolo del collaudatore a freddo | `references/collaudo-mappe.md` |
| **Standard di qualità**: la mappa è plausibile e buona? regole misurabili con fonti, quota e contesto, misure vere di fortezze e città, il punteggio | `references/standard-qualita-mappe.md` |
| Direzione artistica di handout/splash (convenzioni + confini IP) | `references/stile-illustrazione-handout.md` |
| «Hero map» pittorica locale facoltativa (ComfyUI + ControlNet + MCP), e quella Canva AI finché ComfyUI non è collaudato | `references/hero-map-comfyui.md` |

## Regole d'oro

1. Il master è la griglia markdown; dopo OGNI modifica rigenera l'SVG:
   `python3 scripts/render_map_svg.py <file.md>`
2. Scala **1,5 m/quadretto**, dichiarata nell'intestazione del file.
3. SOLO i simboli della legenda universale (`references/legenda-universale.md`);
   `scripts/legend.yaml` è la fonte di verità (ADR-0048) per renderer, export
   UVTT, importer e catena Blender. Un simbolo locale si dichiara nel file e si
   rende con l'SVG Noto Emoji di `scripts/emoji-noto/` (ADR-0085), uguale su ogni
   macchina: dopo averlo aggiunto, `python3 scripts/build_emoji_noto.py`.
   Diventa universale solo se significa la stessa cosa in ogni mappa.
4. Ogni mappa esce con i tre blocchi Ambiente / Tattiche / Evoluzione di
   `campaign/templates/mappa-tattica-template.md`.
5. **Arte procedurale/interna per default.** Un file di terzi entra solo
   secondo ADR-0085: licenza che permette la ridistribuzione senza imporsi
   (CC0, CC BY, CC BY-NC, Apache-2.0, OFL, MIT; mai CC BY-SA o GPL), con licenza
   e `CREDITS.md` (autore, modifiche) nella sua cartella. Niente ricalco. Il
   testo delle mappe usa i font dei volumi, incorporati (`scripts/fonts/mappe/`,
   `build_font_mappe.py`).
   **Le mappe più ricche passano solo per CC0** (D13-D15 di RESA-ASSET): il tema
   texture riempie i terreni con texture CC0 di Poly Haven
   (`build_texture_cc0.py`, `scripts/texture-cc0/`), committate in
   `rendered-texture/` accanto alla pergamena e controllate da `validate_maps`.
   Gli oggetti diventano tessere webp rese dall'alto in Blender da modelli 3D CC0
   (Poly Haven; Quaternius Fantasy Props MegaKit solo **Standard**), con un solo
   blocco di camera, sole e impronta per il set (`build_oggetti_cc0.py`,
   `scripts/oggetti-cc0/`, D17-D22); i modelli restano sulla macchina del DM.
   Fuoco, effetti, porte, finestre, grate, sbarre, segnalini, creature e scale
   restano glifi (`render.tessera_cc0: false` in `legend.yaml`), e così ogni
   simbolo senza tessera; la pergamena tiene ogni glifo. **Una sostituzione
   entra solo se misurata e preferita** (ADR-0086, D23): `misura_resa.py`
   (contrasto di contorno WCAG 1.4.11, SSIM col simbolo più vicino, ΔE2000 dalla
   palette di casa) non peggiora, e il DM la sceglie nella pagina di scelta
   (`misura_resa.py coppie [--anche DIR]` per gli oggetti, `terreni-scelta` per
   le texture dei terreni, poi `voti`): riquadri etichettati, opzioni identiche
   tolte e dette, «nessuna va bene» butta l'immagine per quel simbolo, «non vedo
   differenze» tiene la più economica. `misura_resa.py --check` in CI blocca
   ogni misura di resa che cala più del 5%; `misura_resa.py tara` ritara alone e
   velo per terreno del tema texture. 2-Minute Tabletop è un extra facoltativo
   per il solo tavolo del DM, fuori da git (`asset-esterni/`,
   `dm.py asset installa <zip> --categoria base|premium`); un pacchetto **premium** (Plus,
   Patron Packs, token, anche pagati) non ha licenza oltre il tavolo e
   `dm.py asset controlla` fallisce (GUIDA-MAPPE §5.1-§5.2).
   **Il tema «pianta»** (ADR-0102) disegna la griglia nello stile delle piante di
   città: roccia tratteggiata a bordi frastagliati (≤ 0.24 cella, celle
   calpestabili invariate), lastricato a corsi, pannello «Luoghi» dalle righe
   `@mark`, legenda sotto. Si adotta per cartella: dove esiste `rendered-pianta/`,
   `validate_maps` lo vuole completo e allineato (ARC-07 lo ha). Le piante
   canoniche di Rethmar, Dauth e Channathgate escono da `scripts/piante/`
   (shapely, requirements-dev): si cambia il programma, mai l'SVG, poi
   `dm.py maps citta <città>`; `--check` confronta i byte.
6. **Contratto di fedeltà** (piano RENDER-MAPPE-FEDELTÀ): le annotazioni a lato
   di una riga di griglia cominciano dopo **≥3 spazi** (o un `│` staccato
   preceduto da ≥2 spazi, o box-drawing): il parser non le legge mai come celle,
   neanche con emoji. L'intestazione `N col × M righe · S m` è una
   **dichiarazione validata**: le discordanze avvisano (`--strict` fallisce) e la
   scala dichiarata guida sottotitolo e barra di scala. `<!-- render: none -->`
   subito prima del fence marca schemi/diagrammi da NON rendere. La riga
   `LEGENDA · 🧲 descrizione · …` nel fence si legge da sola: i simboli locali
   hanno la loro descrizione nella legenda SVG (i SYMBOLS universali tengono il
   testo canonico).
7. **Una mappa in un volume o sta in una colonna o prende una pagina A4.** Una
   colonna tiene 48 celle, una pagina A4 a una colonna 110 (un'emoji conta 2.5).
   Le sezioni di mappa vanno in un'appendice fra `<!-- pagina: una-colonna -->`
   e `<!-- /pagina -->`; ogni riga di griglia, annotazione e riga `LEGENDA` sta
   entro 110 celle, per stampare a 9 pt pieni. L'esportatore typst divide da
   solo colonna/A4 (`rumblingstone-editoria` §4, punto 4), ma una riga di
   legenda da 180 celle rimpicciolisce tutta la mappa: accorcia l'annotazione,
   mai la griglia.
   **La mappa resa in un volume è sempre la stampa «pianta»** (ADR-0106): ogni
   `rendered/` ha il gemello `rendered-stampa-pianta/` con la mappa e la sua
   `_legenda` (`render_map_svg.py --tutti-i-master --tema pianta --stampa`), e
   il master del volume punta a entrambe, ciascuna seguita da
   `<!-- nuova-pagina -->`. Testo mai sotto 7.4 pt, niente filtri, voci di
   legenda intere. `validate_maps` segnala file mancanti o vecchi;
   `validate_booklets` ferma un SVG pergamena, una mappa senza legenda, una
   griglia stampata e ogni diagramma box-drawing stampato fuori dall'apparato.
   La griglia ASCII di una mappa rendibile non si stampa mai: resta nel master
   fra `<!-- apparato -->` e `<!-- /apparato -->`, dopo la pianta. Una vista che
   non è una griglia (sezione, panoramica fuori scala) diventa uno schema in
   stile pianta da `scripts/render_schemi.py` (`--check` in CI); una linea del
   tempo o un flusso ASCII diventa una tabella.
8. **Hero map da un servizio (Canva AI), finché la passata ComfyUI locale non è
   collaudata.** Canva AI dipinge **solo** la hero map per i giocatori, con il
   prompt scritto **dal JSON della mappa** (contratto della Modalità 3, o export
   UVTT di un master emoji): proporzioni, terreno, stanze, porte e accessi a
   parole, nord in alto. La verità tattica resta master, JSON, SVG,
   `validate_maps` e UVTT: una hero map che sposta una porta, una stanza o un
   accesso rispetto all'SVG si **butta**, anche se è bella. **Nessun generatore
   AI disegna la griglia**: se serve, si sovrappone dall'SVG. Procedura:
   `references/hero-map-comfyui.md`, «Finché ComfyUI non è collaudato».
9. **Una mappa è fatta quando si gioca, non quando si rende** (ADR-0082). Ogni
   mappa tattica nuova o ridisegnata passa `scripts/collaudo_mappe.py` con zero
   rilievi di classe E (o `@deroga` scritta con la ragione), dichiara
   `@north`, collega ogni scala o botola alla gemella con `@collega`, e poi va
   al **collaudatore a freddo**. Porte, grate e finestre stanno in un muro; le
   porte segrete mai nella versione giocatori (`@vista giocatori`). Una chiusura
   prende l'asse del muro dai quattro vicini (ADR-0083), e da lì il renderer
   gira il glifo e l'export UVTT il portale: la direzione non si disegna, si
   scrive `@verso <cell> ; NS|EO` solo dove il collaudo trova i vicini
   ambigui. Il collaudo vuole `tcod` (`pip install -r requirements-dev.txt`, ADR-0084).
   Prima di un simbolo locale, quelli di `legend.yaml` (porte per tipo, sbarre,
   scale su/giù, pavimento di grotta, acqua bassa, fogna, detriti, mobili).
   Procedura e rubrica: `references/collaudo-mappe.md`. Poi
   `scripts/qualita_mappe.py` la misura contro lo standard di qualità
   (ADR-0098): si prepara nell'ordine funzione, flusso, scala, tattica; le mappe
   d'esterno, d'insediamento e strategiche dichiarano `@quota` e `@dislivello`
   (e `@luogo` se un'altra mappa mostra lo stesso punto).
   Regole, soglie e fonti: `references/standard-qualita-mappe.md`.

## Procedura

1. **Scegli la modalità**: stesso MASTER a griglia emoji, *sorgente* diversa
   (dettaglio e «system prompt» dell'LLM: `references/tre-modalita-mappe.md`):
   - **Tattica standard**: griglia scritta a mano o dungeon importato
     (`import_watabou.py`) → `render_map_svg.py`.
   - **Cinematografica / scenica**: l'LLM fa il *prompt engineer*; atmosfera
     con ComfyUI locale (`scripts/comfyui-local/`,
     `references/hero-map-comfyui.md`), banca prompt in
     `campaign/ai-media-prompts/`.
   - **Tattica con strutture ed eserciti**: l'LLM emette **solo JSON rigido**
     (`scripts/schemas/tactical_map.schema.json`), `compile_map_json.py` valida
     e dipinge la griglia. Un LLM non disegna MAI arte ASCII di mappe.
2. Scrivi il master (regole 2-4, 6) e rendi (regola 1).
3. Collauda e misura (regola 9).
4. Dove servono: temi e stampa (regole 5, 7), hero map (regola 8), tavole di
   supporto (sotto).

### Le tavole di supporto: quando dall'alto non basta

Le tre modalità sono **zenitali**: giuste per le miniature, sbagliate per tre
domande che arrivano sempre:

| Domanda | Vista che risponde |
|---|---|
| «Cosa vediamo arrivando?» | **veduta**: prospettica, dal punto da cui i PG arrivano davvero (dal mare, dalla strada, dal crinale) |
| «Quanto è alto? Si può scendere di lì?» | **profilo laterale**: sezione con **quote**, e le vie verticali segnate |
| «Quanto ci mettiamo?» | il profilo con i **tempi di percorrenza** annotati sui tratti, non solo le distanze |

**La regola**: una tavola di supporto si aggiunge **quando risponde a una
domanda che la griglia non può**, non per completezza: tre viste dello stesso
cortile sono tre file da allineare, una veduta del promontorio raggiunto in
barca risparmia cinque minuti di descrizione a ogni gruppo. Stessa serie, con
una lettera: `Tavola I` (zenitale), `Tavola I-a` (veduta), `Tavola I-b`
(profilo), cioè **lo stesso luogo visto in un altro modo**. ⚠️ **Non
sostituiscono la griglia**: niente coordinate, quadretti o legenda tattica.
Restano SVG originali (ADR-0005). Esemplare: `10-stand-alone/L'abbazia Della Rotta Sicura/`,
Tavola I-a «il promontorio, veduta dal mare» e Tavola I-b «profilo laterale:
quote, distanze e tempi».

## Comandi

```bash
python3 scripts/render_map_svg.py <file.md>        # render all maps in file
python3 scripts/render_map_svg.py <file.md> --list # list maps found
python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md
python3 scripts/compile_map_json.py spec.json -o <arco>/NUOVA-MAPPA.md  # Mod. 3: JSON → master
python3 scripts/compile_map_json.py spec.json --validate-only           # solo validazione
python3 scripts/import_ultraclear.py ULTRACLEAR.md -o OUT.draft.json --json-report OUT.conflicts.json  # migra un ultra-clear
python3 scripts/export_map_png.py rendered/<mappa>.svg   # hi-res PNG (print / hero input)
python3 scripts/export_uvtt.py <file.md>           # .uvtt/.dd2vtt (Foundry/Roll20: muri+luci)
python3 scripts/validate_maps.py                   # CI gate (run before commit)
python3 scripts/collaudo_mappe.py <file.md>        # does it play? (ADR-0082)
python3 scripts/qualita_mappe.py <file.md>         # how good is it? score and findings (ADR-0098)
python3 scripts/qualita_mappe.py --classifica      # the whole corpus, worst first
python3 scripts/dm.py asset texture && python3 scripts/dm.py maps texture   # CC0 texture theme, all maps
.venv/bin/python scripts/build_oggetti_cc0.py --prova   # CC0 3D props for the texture theme (Blender or bpy), GUIDA-MAPPE §5.1.1
python3 scripts/misura_resa.py --check               # the rendering did not get worse (ADR-0086), GUIDA-MAPPE §5.1.2
python3 scripts/dm.py asset installa <zip> --categoria base   # 2-Minute Tabletop, optional, table only
python3 scripts/dm.py maps citta <scheda>.watabou.json --export svg  # a Watabou city plan from a committed seed (R5)
python3 scripts/dm.py maps pianta <file.md>        # «pianta» theme → rendered-pianta/ (ADR-0102)
python3 scripts/render_map_svg.py --tutti-i-master --tema pianta --stampa   # print mode of every map (ADR-0106)
python3 scripts/dm.py maps citta [rethmar|dauth|channathgate] [--check]  # the repo's own city plans
```

## Formato d'uscita

Un master markdown: intestazione `N col × M righe · S m`, griglia nel fence con
la riga `LEGENDA`, direttive `@` del collaudo, tre blocchi Ambiente / Tattiche /
Evoluzione; accanto `rendered/` (e, dove adottati, `rendered-texture/`,
`rendered-pianta/`, `rendered-stampa-pianta/`). Modello:
`campaign/templates/mappa-tattica-template.md`.

## Prima di consegnare

- SVG rigenerato e identico? `python3 scripts/validate_maps.py`
- Si gioca? `python3 scripts/collaudo_mappe.py <file.md>`: zero classe E o
  `@deroga`, poi il collaudatore a freddo (regola 9).
- È buona? `python3 scripts/qualita_mappe.py <file.md>`
- Glifo o texture sostituiti? `python3 scripts/misura_resa.py --check` e la
  scelta del DM (regola 5).
- La hero map sposta porte, stanze o accessi rispetto all'SVG? Si butta.

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/validate_booklets.py`: pianta da stampa e legenda per ogni mappa (ADR-0106).
- `python3 scripts/misura_standard_tavolo.py`: la mappa sta vicino alla scena dello scontro.
