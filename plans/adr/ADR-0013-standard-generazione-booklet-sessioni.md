# ADR-0013 — Standard di generazione dei booklet (stile pergamena, struttura, doppia via HTML/Homebrewery)

**Stato**: accettata
**Data**: 2026-07-24
**Decisione-fonte**: richiesta DM 2026-07-24 (review del booklet «Lo Scontro
con Terros» + booklet del Palio di Channathgate come esemplare); lotti
K-B9/K-B10/K-B11 del piano DM-TOOLKIT.

## Contesto

I booklet (d'arco come il Palio, di sessione come Terros) erano nati come
redazioni una-tantum: lo stile HTML «pergamena Homebrewery» viveva fuori dal
repo, la struttura variava da booklet a booklet, e il materiale player-facing
rischiava di bruciare l'aspettativa (un titolo come «Lo Scontro con Terros»
in mano ai giocatori uccide l'hype prima della sessione). Serviva uno
standard unico che valesse per OGNI generazione futura, su entrambe le vie
di resa (HTML autonomo e Homebrewery self-hosted/Docker).

## Decisione

**Ogni booklet si genera dal builder canonico via manifest, con questa
struttura obbligatoria e su doppia via di output.**

### 1. Stile e strumento (unica fonte)

- Lo stile «pergamena» è definito UNA volta, nel CSS incorporato di
  `scripts/build_booklet_html.py`. Niente HTML artigianale, niente CSS
  copiati: chi tocca lo stile tocca il builder (e quindi tutti i booklet).
- Ogni booklet è descritto da un manifest `*.manifest.json` committato
  accanto ai capitoli (`brand/title/subtitle/banner/meta/intro_md/
  cover_image/chapters[{title,file,tag}]`). I capitoli sono markdown e
  restano i MASTER (ADR-0003): l'HTML/.hb.md sono artefatti rigenerabili.
- Comando: `python3 scripts/dm.py booklet <manifest> [--format html|hb|both]`.

### 2. Struttura obbligatoria di un booklet di SESSIONE

| Sezione | Tag | Contenuto |
|---|---|---|
| Copertina + «Dove siamo» | — | read-aloud d'apertura + fotografia della vigilia |
| ✉ Teaser giocatori | `player` | **file e manifest SEPARATI** (inviabile così com'è): recap lampo delle parti giocate + invito evocativo |
| Regia della sessione | `dm` | ordine di gioco, **canone giocato** registrato con data, guard-rail di canone, cosa stampare |
| Master integrale/i | `dm` | i master `ARC*-DEF-*` citati per intero — zero numeri nuovi |
| ✉ Hint/Echi per-PG | `player` | UNA pagina per PG, consegnata in privato; i contro-momenti come sussurri degli artefatti, mai CD/statistiche del nemico |

I booklet d'ARCO (es. Palio) seguono lo stesso schema senza la regia di
serata: teaser giocatori + capitoli master integrali.

### 3. Regola anti-spoiler del materiale player-facing (vale per TUTTE le sessioni)

- Il **nome della sessione visto dai giocatori è sempre evocativo e mai
  descrittivo dell'incontro** (es. «L'Ultima Porta», non «Lo Scontro con
  Terros»). Il titolo vero resta nel booklet DM.
- Il teaser contiene SOLO: fatti già vissuti al tavolo (recap veloce) e
  prospettive vaghe/ispirazionali (coerente con la policy recap
  player-safe di K-B6: fatti accaduti descritti, futuro nebbioso).
- Mai nel materiale giocatori: nomi di boss/antagonisti non ancora
  incontrati, CD, pf, soglie, clock, deadline.

### 4. Canone giocato

Gli esiti giocati al tavolo (oggetti ottenuti/spesi, scene risolte in
variante) si registrano **nel master** come blocchi
`✅ CANONE GIOCATO (DM data)` nel punto esatto della scena, e si
riassumono nella tabella «fotografia della vigilia» della regia. Il master
resta l'unica fonte dei numeri (esemplare: Frequenza/Diapason in
`ARC07-DEF-1` §6/§7a/§7b/§8).

### 5. Doppia via di output (lo «switch»)

- `--format html` (default): UN file `.html` autonomo — immagini
  incorporate (SVG inline, raster data-URI), zero server, condivisibile.
- `--format hb`: sorgente **Homebrewery V3** `.hb.md` dallo STESSO
  manifest, per l'editor a due pannelli self-hosted (nativo o Docker,
  `dm.py hype` / ADR-0004); le immagini restano riferimenti relativi.
- `--format both`: entrambi. Le due vie sono equivalenti e mantenute:
  nessuna delle due è deprecata.

## Conseguenze

- Più facile: generare booklet coerenti in un comando; rigenerare dopo ogni
  correzione di canone; inviare il teaser senza paura di spoiler; passare
  da HTML a Homebrewery senza riscrivere nulla.
- Più difficile / rinunce: niente booklet «a mano» fuori standard; il
  teaser è un file in più da scrivere per ogni sessione (costo accettato:
  è il pezzo che crea l'hype).
- Da rivisitare: se Homebrewery V3 cambia sintassi (frontCover/banner),
  aggiornare `build_hb()`; se lo stile evolve, versionare il CSS nel
  builder con nota nel CHANGELOG dei piani.

## Esemplari

- Sessione: `07_.../homebrew/sessione-terros/` (booklet DM + teaser
  separato `ARC07-TEASER-GIOCATORI.manifest.json`).
- Arco: `09_.../homebrew/PALIO-BOOKLET.manifest.json` (+ teaser
  «Novanta Secondi»).
