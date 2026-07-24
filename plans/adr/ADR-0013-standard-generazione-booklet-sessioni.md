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
- **Anche i piè di pagina contano** *(fix DM 2026-07-24)*: le pagine ✉
  usano il campo manifest `player_footer` (titolo evocativo) — MAI il
  `footer`/titolo reale del booklet DM. Un handout con scritto sotto
  «Lo Scontro con Terros» brucia l'aspettativa quanto un titolo. Il
  builder lo applica da solo: basta valorizzare `player_footer` in ogni
  manifest di sessione.

### 3-bis. Non-ridondanza teaser ↔ hint (regola DM 2026-07-24)

**Il teaser e gli hint si spartiscono la storia: mai lo stesso fatto in
entrambi.** Se il teaser ripete ciò che c'è negli hint, leggere l'hint
personale perde valore.

- **Teaser** = SOLO la **storia comune** vissuta da tutto il tavolo
  insieme, e SOLO le parti non coperte da alcun hint personale (es. la
  scala cantata: c'erano tutti, nessun hint la racconta).
- **Hint per-PG** = i momenti **personali**: scene in cui quel PG è stato
  il protagonista, voci/visioni dei SUOI artefatti, percezioni che solo
  lui ha avuto. Questi fatti **non si ripetono MAI nel teaser** — al
  massimo un **rimando obliquo** che crea curiosità senza raccontare
  (es. *«il resto di quel duello appartiene a chi l'ha combattuto: è nel
  suo hint»*).
- **Citazioni testuali** (le battute degli artefatti, i sogni): vivono in
  UN solo posto — l'hint del PG a cui appartengono.
- **Procedura per l'agente (qualunque modello)**: scrivere PRIMA gli hint
  per-PG, POI il teaser; quindi un **passaggio di dedup** — per ogni frase
  del teaser chiedersi «questo fatto è già in un hint?»: se sì, toglierlo
  o ridurlo a rimando obliquo.

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

## Appendice — Ricetta operativa per l'agente (qualunque modello)

Questa checklist rende la generazione riproducibile da qualsiasi agente
che segua il repo (le skill instradano la QUALITÀ: prosa →
`rumblingstone-narrative-style`; profondità dei master →
`rumblingstone-module-standard`; comandi → `rumblingstone-automation`;
tracciatura → `rumblingstone-plans`).

1. **Raccogli gli input**: il/i master `ARC*-DEF-*` del beat; lo stato
   della vigilia dal DM (cosa è stato giocato: oggetti ottenuti/spesi,
   scene risolte); `campaign/state.md` §0 per data/countdown.
2. **Registra il canone giocato** nei master (blocchi
   `✅ CANONE GIOCATO (DM data)` nel punto esatto — mai riscrivere i
   numeri) e verifica con `python3 scripts/validate_modules.py`.
3. **Crea/aggiorna la cartella di sessione** `<arco>/homebrew/sessione-*/`:
   `00-INTRO` (dove siamo), `01-REGIA` (ordine di gioco + tabella vigilia
   + guard-rail di canone), poi **in quest'ordine**: PRIMA
   `0N-HINT-<PG>.md` (uno per PG: sussurri degli artefatti, zero CD) e
   `0N-ECHI-<PG assente>.md`, POI `0N-TEASER-GIOCATORI.md` (SOLO storia
   comune non coperta dagli hint + invito evocativo — regola §3-bis).
4. **Due manifest**: booklet DM (titolo vero, `player_footer` evocativo,
   capitoli `dm` + pagine `player`) e teaser separato (titolo evocativo,
   solo contenuto player) — il teaser è il file che si INVIA.
5. **Genera**: `python3 scripts/dm.py booklet <manifest> --format both`.
6. **Controlli sul materiale player**: (a) anti-spoiler — niente nome
   dello scontro (nemmeno nel piè di pagina), niente CD/pf/clock, futuro
   solo evocativo, fatti SOLO vissuti al tavolo; (b) **dedup teaser↔hint
   (§3-bis)** — nessun fatto degli hint ripetuto nel teaser: ogni frase
   del teaser che compare anche in un hint va tolta o ridotta a rimando
   obliquo.
7. **Traccia**: riga in `plans/CHANGELOG.md` nello stesso commit
   (ADR-0009); checklist del piano se è un lotto.
