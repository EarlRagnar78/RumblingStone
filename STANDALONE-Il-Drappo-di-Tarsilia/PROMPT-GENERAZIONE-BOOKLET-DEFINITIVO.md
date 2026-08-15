# Il prompt per generare il booklet definitivo

> **A cosa serve questo file.** Il modulo è completo come **testo** e come
> **impaginazione**, ma non come **libro illustrato**. Qui c'è l'inventario esatto di
> cosa esiste e cosa manca, e — nel §3 — **il prompt da incollare in una nuova
> sessione** per portarlo al livello di un'avventura pubblicata.
>
> È scritto per essere autosufficiente: chi lo riceve non deve aver letto questa
> conversazione.

---

## §1 · Cosa esiste già (non va rifatto)

| Ambito | Stato | Dove |
|---|---|---|
| **Testo del modulo** | ✅ completo — 14 file, ~5.000 righe | la cartella |
| **Apparato d'uso** | ✅ cast, pronuncia, indice read-aloud, schermo, suoni, accessibilità | `08-CASSETTA-DEL-DM.md` |
| **Prop stampabili** | ✅ 4 sorgenti Homebrewery + note DM | `ALLEGATI/handout/` |
| **Mappe tattiche** | ✅ 2, JSON → master → SVG → UVTT | `ALLEGATI/mappe/` |
| **Tavole vettoriali** | ✅ mappa città, il Drappo, 6 ritratti-segnaposto | `ALLEGATI/tavole/` |
| **Stemmi** | ✅ 8, serie Golarion | arco 09, citati per percorso |
| **Booklet impaginati** | ✅ 4 (DM 18 capitoli · Giocatori · Fascicolo · Prop) + ~40 PDF A4 | `homebrew/` |
| **Collaudo** | ✅ audit 18 rilievi + dry-run + 9 correzioni applicate | `PLAYTEST-ALFA.md` |
| **Gate CI** | ✅ `validate_standalone.py` | `scripts/` |

## §2 · Cosa manca per arrivare al livello Paizo/WotC

Onestamente, e in ordine di impatto visivo:

| # | Manca | Perché conta | Difficoltà |
|---|---|---|---|
| **1** | **Illustrazioni raster** — zero. Un'avventura pubblicata ha una tavola a piena pagina, 6-10 spot e i ritratti dei pregen | è la differenza fra un documento e un libro | media (serve una GPU o un servizio) |
| **2** | **Tipografia embedded** — i booklet usano **Georgia**, che è un font di sistema: su una macchina che non ce l'ha, il PDF cambia faccia | un libro si riconosce dal carattere prima che dal testo | bassa |
| **3** | **Mappa in versione giocatore** — la Ruota mostra token, hazard e note tattiche: è la versione del DM. Manca quella pulita da mettere in mano | standard di ogni AP | bassa |
| **4** | **PDF unico con segnalibri** — oggi è un file per capitolo | un lettore vuole **un** file con l'indice cliccabile | bassa |
| **5** | **Copertina vera** — oggi è la tavola del Drappo | — | media |
| **6** | **Carte da tavolo** — segnaposto contrada, ordine di corsa | rende visibile lo stato della gara | bassa |

## §3 · Il prompt — da incollare in una sessione nuova

> Copia **tutto** il blocco che segue. È scritto per un agente che lavora sul repo
> RumblingStone e non ha letto niente di questa conversazione.

```text
Lavori sul repo RumblingStone, branch claude/golarion-pathfinder-campaign-xbyvzt.

OBIETTIVO
Portare il modulo autoconclusivo STANDALONE-Il-Drappo-di-Tarsilia/ da "completo come
testo" a "libro illustrato di livello Paizo/WotC", e produrre il booklet definitivo.
Il testo NON va riscritto: è collaudato (PLAYTEST-ALFA.md) e validato in CI.

PRIMA DI TOCCARE QUALSIASI COSA — leggi in quest'ordine:
1. STANDALONE-Il-Drappo-di-Tarsilia/00-HUB-E-QUICKSTART-DM.md  (cos'è il modulo)
2. STANDALONE-Il-Drappo-di-Tarsilia/PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md §1-§2
   (cosa esiste e cosa manca: è l'inventario da cui parti)
3. plans/adr/ADR-0017 (moduli autoconclusivi) e ADR-0018 (apparato d'uso obbligatorio)
4. plans/adr/ADR-0015 (standard dei prompt immagine) e ADR-0013 (standard booklet)
5. skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md
   (⚠️ il confine IP sull'arte: si descrivono le CONVENZIONI, mai un artista vivente)
6. STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md
   (la bibbia visiva già scritta: palette, età, segni distintivi, formati)

VINCOLI NON NEGOZIABILI
- Lingua sorgente italiana (ADR-0016). L'inglese non si usa nei file di gioco.
- Nessun nome di illustratore vivente nei prompt, nessuna immagine altrui come style
  reference (ADR-0005 + la skill di stile). Si descrivono tecnica e composizione.
- Solo asset con licenza verificabile. Ogni asset importato porta la sua riga di
  provenienza in ALLEGATI/immagini/PROVENIENZA.txt: fonte, licenza, autore, modifiche.
- Niente dipendenze nuove in scripts/ senza voce nel manifest (ADR-0012). I generatori
  locali al modulo seguono ADR-0017 §4: stdlib-only, docstring, citati in un .md,
  compilano.
- Il gate scripts/validate_standalone.py deve restare verde.
- Non toccare i file della campagna (00_-09_, campaign/, Bestiario/, PG/).

I SEI LAVORI, in ordine di priorità

[1] ILLUSTRAZIONI RASTER — il lavoro principale
    Servono, con questi nomi esatti in ALLEGATI/immagini/:
      ritratto-vanna.png ritratto-nocca.png ritratto-ombra.png
      ritratto-tesio.png ritratto-berenice.png ritratto-melchio.png   (832x1216)
      tavola-la-ruota.png tavola-la-cena.png tavola-le-stalle.png     (1536x864)
      il-drappo.png                                                   (832x1216)
    I prompt esistono già in ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md.
    Il tuo compito: (a) verificarli contro la bibbia visiva e RENDERLI COERENTI fra
    loro — stessa palette, stessa luce, stesso trattamento — aggiungendo un blocco di
    stile condiviso e un seed suggerito; (b) aggiungere i prompt MANCANTI per i PNG
    che meritano un ritratto ma non ce l'hanno: Ottavia Vesca, Gerlando Attu, Vidalia
    Roncetti, Sfregio, Nonna Grasa (elenco completo e tic vocali in
    08-CASSETTA-DEL-DM.md §1); (c) scrivere in ALLEGATI/immagini/README.md la
    procedura esatta con scripts/comfyui-local/ (il repo ha già l'infrastruttura).
    Se hai accesso a un generatore: producile. Se no, consegna i prompt finiti e
    lascia i segnaposto vettoriali, che sono già stampabili.

[2] TIPOGRAFIA EMBEDDED
    I booklet usano Georgia (font di sistema): su una macchina che non ce l'ha, il PDF
    cambia faccia. Sostituirlo con caratteri OFL embeddabili — candidati da VERIFICARE
    tu, non fidarti di questo elenco: EB Garamond (testo), Cinzel o Alegreya SC
    (titoli), IM Fell English (frontespizio). Vanno inlineati come base64 nel CSS di
    scripts/build_booklet_html.py.
    ⚠️ Quel file impagina TUTTI i booklet del repo, campagna compresa: è una modifica
    trasversale. Serve un ADR (formato: plans/adr/ADR-00NN-*.md) e la rigenerazione
    dei brew esistenti. Se il DM non vuole toccare la campagna, fallo come tema
    opzionale attivabile da manifest ("theme": "libro") e lascia il default com'è.

[3] MAPPA IN VERSIONE GIOCATORE
    ALLEGATI/mappe/tarsilia-la-ruota.json contiene token, hazard e note tattiche: è la
    versione del DM. Produci la gemella pulita — stessa geometria, senza units, senza
    hazards, senza le note che spoilerano — come tarsilia-la-ruota-giocatori.json, e
    rendila con la pipeline (compile_map_json.py -> render_map_svg.py). Aggiungila al
    booklet dei giocatori e a ALLEGATI/mappe/README.md.

[4] PDF UNICO CON SEGNALIBRI
    Oggi scripts/export_booklet_pdf.py produce un A4 per capitolo. Serve anche il
    volume unico con indice cliccabile. Due strade: (a) estendere l'esportatore
    perché stampi l'HTML intero in un solo PDF con outline; (b) unire i PDF esistenti
    con una libreria. Preferisci (a): niente dipendenze nuove, e il browser headless
    genera già i segnalibri dagli heading. Aggiorna la voce nel manifest dei tool.

[5] CARTE DA TAVOLO
    Otto segnaposto di contrada (livree in CONTRADE-DI-TARSILIA.md §1) e una traccia
    dell'ordine di corsa, in SVG, generati da ALLEGATI/tavole/build_tavole.py
    (estendi il generatore esistente: NON crearne un altro).

[6] COPERTINA
    Frontespizio vero: titolo, sottotitolo, sistema, numero di giocatori, livello,
    durata. Vettoriale se non hai un generatore raster.

STRUMENTI DEL REPO — usa questi, non reinventarli
  scripts/compile_map_json.py      JSON mappa -> master emoji-grid
  scripts/render_map_svg.py        master -> SVG pergamena
  scripts/export_map_png.py        SVG -> PNG (Chromium headless, già installato)
  scripts/export_uvtt.py           master -> Foundry/Roll20
  scripts/build_booklet_html.py    manifest -> HTML + sorgente Homebrewery
  scripts/export_booklet_pdf.py    manifest -> PDF A4 per capitolo
  scripts/extract_scene_prompts.py scene illustrabili -> scheletro prompt (ADR-0015)
  scripts/comfyui-local/           infrastruttura ComfyUI in container
  ALLEGATI/tavole/build_tavole.py  le tavole vettoriali del modulo
  scripts/validate_standalone.py   il gate: deve restare verde

STRUMENTI ESTERNI — solo se la licenza regge, e verificala tu
  · Homebrewery (self-hosted): il repo ha già scripts/homebrew-local/
  · game-icons.net: CC BY 3.0, già usato per gli stemmi, attribuzione in CREDITS.md
  · Watabou (generatori di città/dungeon): il repo ha già scripts/import_watabou.py
  · Collezioni museali ad accesso aperto (es. Rijksmuseum, Met): molte opere in
    pubblico dominio o CC0 — ottime per texture, cornici e fregi d'epoca senza
    generazione. VERIFICA la licenza della singola opera, non della collezione.
  · Font OFL da Google Fonts / Open Font Library.
  ❌ Da NON importare: qualsiasi asset proprietario (Inkarnate, Dungeon Scrawl,
    banche immagini a pagamento), e qualsiasi immagine di cui non trovi la licenza.

CRITERI DI ACCETTAZIONE
1. scripts/validate_standalone.py, validate_skills.py, validate_maps.py,
   tools_manifest.py --check e i test unitari sono verdi.
2. Ogni immagine ha una riga in ALLEGATI/immagini/PROVENIENZA.txt.
3. I quattro booklet si rigenerano da zero con i comandi in homebrew/README.md.
4. Il booklet del DM contiene tutti i capitoli del modulo (oggi 18): se aggiungi
   file, aggiorna il manifest — è l'errore che ho già commesso una volta.
5. Tracciatura obbligatoria (ADR-0009): piano + plans/INDEX.md + plans/CHANGELOG.md
   nello stesso commit. Il piano è plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md
   e questo lavoro è il suo Lotto 6.
6. Nessun file della campagna modificato.

COSA NON FARE
- Non riscrivere il testo del modulo: è collaudato.
- Non rinominare le contrade: la decisione del DM è di tenere i nomi senesi per ora
  (IP-E-LICENZE.md §4, bonifica §7.1 sospesa).
- Non aggiungere dipendenze Python senza manifest e senza ADR.
- Non generare immagini che imitino lo stile di un illustratore identificabile.
```

## §4 · Se vuoi solo le immagini, senza il resto

Il pezzo minimo che cambia di più l'aspetto sono **i sei ritratti**. Prompt già
pronti in `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` §2, con il blocco di stile
condiviso al §1: si passano a ComfyUI locale
(`scripts/comfyui-local/README.md`) e si salvano coi nomi esatti del §3, punto [1].
Il resto del modulo non cambia di una riga: i booklet li pescano automaticamente.

## §5 · Cosa resta comunque fuori portata

Due cose che un modulo Paizo ha e questo non avrà, ed è giusto dirlo:

- **Un art director**: la coerenza fra dieci illustrazioni generate resta il punto
  debole di qualsiasi pipeline automatica. Il blocco di stile condiviso e il seed
  fisso aiutano; non risolvono.
- **Il collaudo su decine di tavoli**: qui il ciclo è alfa → beta → collaudato su
  **due** gruppi (`rumblingstone-playtest`). È già molto più di quanto fa la maggior
  parte del materiale amatoriale, ed è molto meno di quanto fa un editore.
