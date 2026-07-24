# 🖥️ PIANO — Editor visuale di mappe tattiche (progetto separato, round-trip col contratto JSON)

> **Cos'è**: il piano per un **editor visuale a griglia** — un front-end di
> authoring che si apre nel browser, permette di disegnare/spostare terreno,
> muri, strutture, hazard, unità e overlay **sulla griglia 1,5 m**, e **salva un
> JSON conforme** a `scripts/schemas/tactical_map.schema.json`. L'editor edita
> *dati* e mostra una *figura* live; il render "vero" a stampa resta
> `render_map_svg.py`. È la **vera alternativa domain-fit a FreeCAD**: leggero,
> con la semantica di gioco nativa, senza CAD 3D.
>
> **Vincolo cardine (richiesta DM 2026-07-23)**: alla fine deve essere **un
> progetto diverso e completo** — un sotto-progetto self-contained (propria
> toolchain, proprio build, propri test, proprio README), non due funzioni
> appese agli script Python del repo. Precedente architetturale: Homebrewery
> self-hosted (software di terze parti isolato, wrapper sottili, [ADR-0004](adr/ADR-0004-homebrewery-self-hosted.md)).
>
> **Regola d'oro invariata**: l'editor è un **front-end**, non un secondo master.
> Il master resta il **JSON contratto** (e la griglia compilata da esso); l'SVG
> canonico resta prodotto da `render_map_svg.py`. L'editor non deve mai diventare
> una terza fonte di verità.
>
> Engine: Opus (architettura/ADR) + Sonnet (impl. front-end/test) · Skill di
> dominio: `rumblingstone-mapmaking`. Regola d'oro dei piani: chi chiude un lotto
> aggiorna checklist + `plans/INDEX.md` + `plans/CHANGELOG.md`.

---

## §0 — TL;DR + verdetto

Serve un **editor visuale**, non un CAD. Requisiti non negoziabili: (a) **snap
alla griglia 1,5 m** per costruzione → niente drift; (b) usa **solo la legenda
universale**; (c) **round-trip col contratto** (`tactical_map.schema.json`);
(d) gira **offline** (privacy dei materiali di campagna, come Homebrewery);
(e) l'anteprima è funzionale ma il **render canonico resta `render_map_svg.py`**
(un solo renderer di verità). Per rispettare (a)-(e) e il vincolo "progetto
completo", l'editor vive in un **sotto-progetto isolato** con la sua toolchain
web, agganciato al repo solo da (1) la **legenda condivisa** `legend.json` e
(2) il **contratto JSON**.

---

## §1 — Obiettivo & principi

1. **Authoring visuale** di tutte le primitive del contratto: `regions`
   (rect/polygon), `structures` (at/line/rect/center+radius), `hazards`, `units`
   (single `at` / `area.rect` + `quantity`), overlay (`north`, `movements`,
   `zone`/`mark` via label).
2. **Snap 1,5 m sempre**: ogni oggetto nasce già allineato → il drift è
   impossibile per costruzione (è la cura strutturale al problema originario).
3. **Import**: (i) JSON contratto esistente, (ii) Watabou One Page Dungeon (riuso
   della logica di `import_watabou.py`), (iii) **bozza da `import_ultraclear.py`**
   (vedi [PIANO-IMPORT-ULTRACLEAR](PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md)) —
   così una ultra-clear rotta entra come bozza e si corregge a mano nell'editor.
4. **Export**: JSON contratto (download) → poi la pipeline standard
   (`compile_map_json.py` → `render_map_svg.py` → `export_uvtt.py`).
5. **Un solo renderer di verità**: l'anteprima dell'editor è schematica/funzionale
   (per posizionare), **non** reimplementa la resa "pergamena". Evita il drift tra
   due renderer.

---

## §2 — Perché progetto separato (e quale ADR serve)

Il repo è **Python stdlib + markdown**, con gate CI che valorizzano determinismo e
zero-dipendenze. Un editor web introduce una **toolchain diversa** (JS/TS, bundler,
eventuale Node). Mescolarla agli script degraderebbe entrambi. Isolarla:

- **Sotto-progetto** in `tools/map-editor/` (o repo separato — lo decide l'ADR),
  con proprio `package.json`/build/test, **gitignorato per gli artefatti** e
  committato per i sorgenti; il repo principale resta puro.
- **Precedenti**: [ADR-0004](adr/ADR-0004-homebrewery-self-hosted.md) (Homebrewery self-hosted: terze parti isolate,
  offline, wrapper sottili), [ADR-0010](adr/ADR-0010-vendoring-skill-terzi.md) (vendoring skill terzi), [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md)
  (confini IP: nessun asset/artista di terzi come style reference).
- **ADR nuovo richiesto (E0)**: «Editor mappe come sotto-progetto separato» —
  fissa: repo-in-repo vs repo separato; stack (vanilla vs TS+Vite); politica
  offline/privacy; confine "front-end non è master"; strategia di test (Playwright,
  già disponibile in questo ambiente con Chromium preinstallato).

---

## §3 — Architettura del progetto

```
tools/map-editor/                     (progetto separato, self-contained)
├── README.md            avvio, build, uso, confini
├── package.json         toolchain propria (build statico, offline)
├── src/
│   ├── model/           stato = oggetto tactical_map (unica sorgente in-app)
│   ├── legend/          consuma legend.json (generato dal repo, §4)
│   ├── canvas/          griglia 1,5 m, layer, snap, hit-testing
│   ├── tools/           terreno · muri · strutture · hazard · unità · overlay
│   ├── io/              import (contratto/Watabou/bozza) · export (contratto)
│   └── validate/        specchio dei vincoli schema (bounds/simboli/geometrie)
├── tests/               unit (model/io) + e2e Playwright
└── dist/                build statico self-contained  (gitignorato)
```

**Decisioni di progetto**:

- **Stato = il contratto**: l'app tiene in memoria *esattamente* l'oggetto
  `tactical_map`; ogni azione dell'utente muta quell'oggetto. Import/export sono
  serializzazioni banali → nessun formato intermedio, nessun drift.
- **Layer** allineati alle chiavi dello schema: `regions` sotto, poi `structures`,
  poi `hazards`, poi `units` (stesso ordine di pittura di `compile_map_json.paint`)
  + un layer `overlay` (north/movements/zone/mark).
- **Snap e coordinate**: canvas in quadretti; opzione **input in metri** coerente
  con `units_in: "meters"` (la conversione `round(m/1,5)` è la stessa del
  compilatore) — così l'editor parla entrambe le unità già supportate.
- **Validazione live**: replica *client-side* dei check di `compile_map_json.validate`
  (bounds, simbolo in legenda, rect>0…) con messaggi inline; ma **l'autorità
  resta lo script Python** (l'export passa comunque da `compile_map_json`).
- **Anteprima non-canonica**: rende icone/colori schematici dalla legenda; il
  bottone "Render pergamena" mostra le **istruzioni CLI** (compile→render), non
  un secondo renderer.

---

## §4 — La colla: legenda condivisa `legend.json`

Oggi la legenda vive solo in `render_map_svg.SYMBOLS` (Python). L'editor (JS) non
deve **duplicarla** (diventerebbe una seconda verità che diverge). Soluzione:

- **`scripts/export_legend_json.py`**: dumpa `SYMBOLS` → `scripts/schemas/legend.json`
  (simbolo, `mode`, testo it, categoria). Sorgente unica = `SYMBOLS`.
- **Gate CI**: `validate_maps`/uno smoke test verifica che `legend.json` sia
  **in sync** con `SYMBOLS` (rigenerato = byte-identico), come già si fa per gli SVG.
- L'editor **importa `legend.json`**; anche `import_ultraclear.py` (Piano 1) vi si
  può agganciare. Una legenda, tre consumatori.

Questo lotto (E1) è il **prerequisito tecnico** dell'editor e ha valore anche da
solo (interop schema/editor/tool).

---

## §5 — Fasi (engine consigliato + impegno)

> Routing engine per fase (regola `rumblingstone-plans`): NON è un gate CI.

| Fase | Obiettivo | Engine | Impegno |
|---|---|---|---|
| **E0 — ADR + scaffold** | ADR «editor come sotto-progetto separato» (stack, offline, confini, test); scaffold `tools/map-editor/` con build statico e README | Opus | Medio |
| **E1 — Legenda condivisa** | `export_legend_json.py` → `legend.json` + gate CI di sync (vale anche da solo) | Sonnet | Basso |
| **E2 — Canvas + data model** | Griglia 1,5 m con snap; stato = oggetto contratto; pan/zoom; righello coordinate A1 come il master | Sonnet | Alto |
| **E3 — Strumenti base** | Terreno (rect/polygon), muri (polilinea snap), strutture (porta/torre/tenda), hazard | Sonnet | Alto |
| **E4 — Unità + overlay** | Unità singola (`at`) e di massa (`area.rect`+`quantity`); `north`, `movements` (path+loop+color), `zone`/`mark` da label | Sonnet | Alto |
| **E5 — Import** | JSON contratto; Watabou (riuso logica `import_watabou`); **bozza `import_ultraclear`** (sinergia Piano 1) | Sonnet | Medio |
| **E6 — Validazione live + export** | Specchio dei vincoli schema con messaggi inline; export JSON contratto (`units_in` squares o meters) | Sonnet | Medio |
| **E7 — Round-trip e2e** | Documentare e testare: editor → JSON → `compile_map_json` → `render_map_svg` → `export_uvtt`; il JSON esportato **ricompila** al master atteso | Opus (QA) + Sonnet | Medio |
| **E8 — Packaging self-contained** | Build statico offline avviabile in locale (pattern Homebrewery: `dm.py mapeditor start`? o `README` con `npm run build && open dist/`); artefatti gitignorati | Sonnet | Medio |
| **E9 — Test** | Unit (model/serializzazione/validate) + **e2e Playwright** (disegna → esporta → il JSON combacia); usare il Chromium preinstallato dell'ambiente | Sonnet | Alto |
| **E10 — Doc** | `references/editor-visuale.md` nella skill mapmaking; voce in `tre-modalita-mappe.md`; README del sotto-progetto; nota in `MAPPE-CENSIMENTO.md` | Sonnet | Basso |

---

## §6 — Gate & definizione di "fatto"

- **Round-trip fedele**: un JSON esportato dall'editor, passato a
  `compile_map_json.py`, produce **lo stesso master** che si otterrebbe scrivendo
  quel JSON a mano (test e2e).
- **Una sola verità della legenda**: `legend.json` in sync con `SYMBOLS`
  (gate CI); l'editor non ha simboli propri.
- **Un solo renderer**: l'editor **non** committa SVG «suoi»; il canonico resta
  `render_map_svg.py` (nessun secondo renderer nel repo principale).
- **Offline & privacy**: l'app gira senza rete; nessun materiale di campagna esce
  dal PC (come [ADR-0004](adr/ADR-0004-homebrewery-self-hosted.md)).
- **Progetto completo**: `tools/map-editor/` ha README, build riproducibile, test
  verdi propri; il repo principale resta puro-stdlib e i suoi gate restano verdi.
- **IP-safe** ([ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md)): nessun asset di terzi; icone procedurali/originali.

---

## §7 — Rischi / attenzioni

- **Drift tra due renderer**: il rischio maggiore. Mitigazione: l'anteprima
  dell'editor è dichiaratamente schematica; la resa "vera" è **solo**
  `render_map_svg.py`. Non ricreare la pergamena nell'editor.
- **Duplicazione della legenda**: eliminata da `legend.json` (§4). Se qualcuno
  aggiunge un simbolo solo nell'editor, il gate di sync fallisce.
- **Scope creep verso un VTT completo** (fog of war, iniziativa…): fuori ambito.
  L'editor **autora** mappe; a *giocarle* pensano Foundry/Roll20 via UVTT.
- **Toolchain JS in un repo Python**: isolata nel sotto-progetto; la CI del repo
  principale **non** dipende dal build dell'editor (job separato/opzionale).
- **Manutenzione**: preferire stack minimale e dipendenze poche/stabili; valutare
  vanilla+canvas prima di framework pesanti (decisione in E0).
- **Alternativa `mipui`** (MIT, già censito): editor a griglia esistente, ma non
  parla il nostro contratto/legenda. Se adottato, serve un **adapter** e il
  vendoring per [ADR-0010](adr/ADR-0010-vendoring-skill-terzi.md); un mini-editor nostro resta più pulito sul round-trip.

---

## §8 — Relazione con il Piano `import_ultraclear.py`

I due piani sono **complementari e sinergici**:

```
ultra-clear.md ──(import_ultraclear.py, Piano 1)──▶ bozza JSON + report conflitti
                                                        │
                                          (E5 import)   ▼
                                              EDITOR VISUALE (questo piano)
                                                        │  correggi i conflitti a mano, sulla griglia
                                                        ▼
                                              JSON contratto PULITO
                                                        │
                                    compile_map_json → render_map_svg → export_uvtt
```

L'importer fa il lavoro sporco (estrae + diagnostica); l'editor fa il lavoro fine
(riconciliazione visuale). Insieme migrano le ~30 ultra-clear al formato corretto
senza riscriverle a mano.

## §9 — UX essenziale (senza cui l'editor non è usabile)

Un editor senza queste feature è un prototipo, non uno strumento:
- **Undo/redo** via **command pattern** (ogni azione = comando reversibile) —
  requisito non negoziabile, incluso nell'MVP.
- **Selezione** (singola/multipla), **copia/incolla/duplica**, **elimina**,
  **sposta** con snap.
- **Zoom/pan**, **toggle snap**, **visibilità/lock per layer**, righello A1.
- **Scorciatoie da tastiera** + palette strumenti; **a11y**: navigabilità da
  tastiera, focus visibile, contrasto.
- **Palette color-blind-safe** per i token/terreni (rif. skill `dataviz`).
- **Autosave locale** (localStorage) + import/export file espliciti.

## §10 — NFR & strategia tecnica

- **Performance**: mappe fino a `200×200` (40k celle) → **un solo `<canvas>`**
  con redraw a **dirty-rect**, non 40k nodi DOM; render a `requestAnimationFrame`.
- **Data model & serializzazione**: lo stato è l'oggetto contratto; l'export usa
  un **ordinamento canonico delle chiavi/liste** identico a quello atteso da
  `compile_map_json`, così il round-trip è **idempotente e byte-stabile**.
- **Offline/privacy**: nessuna rete a runtime; File System Access API o
  download/upload; **CSP restrittiva**, **niente telemetria**, niente CDN.
- **Supply-chain**: dipendenze **poche, fissate con lockfile, vendored**, con
  **check licenze** in CI del sotto-progetto; preferire vanilla+canvas (decisione
  E0). Bundle target ragionevole (<500 KB gz) e avviabile da `file://` o statico.
- **i18n**: UI in italiano (coerente col repo), stringhe centralizzate.
- **Browser target**: ultime 2 versioni Chromium/Firefox (Playwright usa il
  Chromium preinstallato dell'ambiente).

## §11 — Anteprima fedele vs statico (la resa "vera")

Nodo UX aperto: come far vedere all'utente la **resa pergamena** (`render_map_svg`)
senza reimplementarla. Tre opzioni (decisione in E0):
- **(A) Watch-helper locale** `dm.py mapeditor` che, al salvataggio del JSON,
  esegue `compile_map_json → render_map_svg` e ricarica l'SVG in un pannello —
  anteprima **fedele**, resta offline, un solo renderer. *(Raccomandata.)*
- **(B) Statico puro**: l'editor mostra solo anteprima schematica + le istruzioni
  CLI per rendere. Più semplice, meno immediato.
- **(C) Renderer in-browser** (portare `render_map_svg` a Pyodide/JS): **scartata**
  — creerebbe il secondo renderer che vogliamo evitare (rischio drift).

## §12 — Integrazione col report conflitti (Piano 1)

L'editor **consuma il `.conflicts.json`** di `import_ultraclear.py` (Piano 1, §7):
importa la bozza, **evidenzia le celle/coordinate in conflitto** con severità e
suggerimento, e permette di risolverle a mano sulla griglia. È il flusso che
trasforma una ultra-clear rotta in un contratto pulito senza riscriverla.

## §13 — MVP / walking skeleton

Fetta verticale minima (dà valore e prova il round-trip prima di costruire i tool):
> **E1 (legenda condivisa)** + un canvas che **importa un JSON contratto**, lo
> mostra sulla griglia, permette **undo/redo** e lo **ri-esporta byte-stabile**.
> Se il JSON esportato ricompila identico al master atteso, il cuore (data model +
> round-trip) è provato; solo allora si aggiungono gli strumenti di disegno
> (E3/E4), l'import Watabou/bozza (E5) e l'anteprima fedele (§11).

## §14 — Decisioni aperte (input per l'ADR E0)

1. **Layout**: sotto-cartella `tools/map-editor/` (proposta) vs repo separato.
2. **Stack**: vanilla+canvas (proposta, minima manutenzione) vs TS+Vite.
3. **Anteprima**: opzione A/B/C di §11 (proposta: A watch-helper).
4. **CI**: job separato per il build/test dell'editor, **non bloccante** per la
   pipeline principale (proposta).

## §15 — Stato

🔵 **PIANIFICATO** (2026-07-23). Primo gate = **E0 (ADR)**: senza la decisione
architetturale «progetto separato + stack + anteprima» non si scrive front-end.
E1 (legenda condivisa) è il prerequisito tecnico e ha valore autonomo, quindi è
candidato a partire per primo anche prima dell'editor vero e proprio.
