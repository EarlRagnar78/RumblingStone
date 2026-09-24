# RumblingStone — DM automation scripts

Zero-burden helpers that read what the DM already writes (session logs,
state.md, Armate atlas) and produce prep material. **Nothing overwrites
canon** — scripts either generate new files or print suggestions for
manual review. Respects `AGENTS.md`: we never invent statblocks; we only
index/compose what exists (or mark `[INFERRED]`).

> **Disambiguazione**: questa cartella `scripts/` è l'automazione DM. I
> convertitori di contenuto (pdf→md, html→md, immagini→webp) vivono in
> `converters/` — vedi ADR-0002 e ADR-0011 in `plans/adr/`.

## One entrypoint: `dm.py`

Everything below is reachable from a single CLI mapped to the Playbook
phases (it *orchestrates* the scripts — they all remain usable directly):

```bash
python3 scripts/dm.py prep --el 13 --env forest   # encounter + map + loot
python3 scripts/dm.py post                        # XP ledger + state.md diff proposal
python3 scripts/dm.py recap --hype                # player recap + Homebrewery V3 version
python3 scripts/dm.py handout --tipo profezia --da <file> --sezione "HANDOUT 1"
python3 scripts/dm.py maps validate               # or: maps render <file.md>
python3 scripts/dm.py bestiario creatura --gs 7 --ruolo bruto   # or: estrai/deriva/attributi/conformita
python3 scripts/dm.py dossier                     # ⚠️ SOLO DM: dossier trame → DM-DOSSIER.hb.md
python3 scripts/dm.py hype setup && dm.py hype start   # Homebrewery locale (localhost:8000)
python3 scripts/dm.py skills build --no-deploy    # rebuild pacchetti skill multi-agente
python3 scripts/dm.py doctor                      # environment diagnosis
```

> 📘 **Vuoi la procedura completa dai master ai PDF in mano ai giocatori?**
> → [`docs/guides/GUIDA-BOOKLET-E-PDF.md`](../docs/guides/GUIDA-BOOKLET-E-PDF.md)
> (prerequisiti per ogni sistema, anatomia del manifest, comandi, container
> opzionali, troubleshooting, checklist di consegna). Qui sotto c'è la
> **mappa degli strumenti**; là c'è il **come si fa**.

> 🎨 **Immagini della campagna** (prompt, generatori, coerenza d'arco):
> [`docs/guides/GUIDA-IMMAGINI.md`](../docs/guides/GUIDA-IMMAGINI.md).

**Sottocomandi `dm.py`** (ognuno inoltra i flag allo script sottostante):

| Sottocomando | Flag | Fa girare | Fase Playbook |
|---|---|---|---|
| `prep` | `--el N` · `--env <amb>` · `--refresh` (rigenera il catalogo) | `suggest_encounter` + `suggest_map` + `suggest_loot` | §2 pre-sessione |
| `maps` | `render`\|`validate` + `files...` | `render_map_svg` / `validate_maps` | prep |
| `post` | `--session <file>` | `update_xp` + `state_sync` | §4 post-sessione |
| `session` | `end`\|`next`\|`recap`\|`status`\|`branch` · `--session <file>` (end; senza → wizard) · `--yes` · `--last-n N` · `--hype` · `--pg <PG>` (recap) · `--group <nome>` | `campaign_branch` + `session_wizard` + `update_xp` + `state_apply` / `next_session` / `session_recap --pg` + `hype_homebrew --pg` | §4 + §7 (branch-per-gruppo, ADR-0007) |
| `recap` | `--last-n N` · `--pdf` · `--hype` | `session_recap` (+ `hype_homebrew`) | §4.6 |
| `handout` | `--tipo T` (obbl.) · `--da <file>` · `--out <file>` | `hype_homebrew --handout` | prep |
| `bestiario` | `estrai`\|`deriva`\|`attributi`\|`creatura`\|`conformita` + i flag dello script (anche `--help`) | `extract_statblocks` / `derive_statblocks` / `genera_attributi` / `genera_creatura` / `conformita_statblocchi` | prep (creature; il codice d'uscita è quello dello script) |
| `hype` | `setup`\|`start`\|`docker`\|`docker-stop` | wrapper `homebrew-local/*.sh` | prep |
| `dossier` | *(nessuno)* | `dm_dossier` | §4 (solo DM) |
| `prompts` | `<arco>` (obbl.) · `-o <file>` · `--list` | `extract_scene_prompts` | prep (prompt immagine dell'arco, ADR-0015) |
| `booklet` | `<manifest.json>` (obbl.) · `--out <file>` · `--format html\|hb\|both` · `--pdf` (pagine ✉) · `--pdf-all` (TUTTE le schede, prefissi pg-/dm-) | `build_booklet_html` (+ `export_booklet_pdf`) | prep (booklet pergamena, ADR-0013: HTML autonomo e/o `.hb.md` per il self-hosted/Docker; PDF A4 per scheda) |
| `skills` | `build`\|`sync` · `--no-deploy` | `build-skills.sh` / `sync-skills.sh` | infra |
| `doctor` | `--ci` (avvisi non fatali) | diagnosi ambiente | infra |

## Tool map

Copre **tutti** gli script della cartella (Scopo · Parametri · Input · Output).
Gli script Python usano solo stdlib; ognuno con argparse espone anche
`python3 scripts/<nome>.py --help`. Positionali senza `--` sono in *corsivo*.

### Prep di sessione (incontri · mappe · tesoro)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `suggest_encounter.py` | 3–5 proposte di incontro per un EL bersaglio | `--el N` · `--env <amb>` · `--factions a,b` / `--faction` · `--alliance <id>` · `--alliance-list` · `--inject-npc n1,n2` · `--narrative` · `--wild` · `--role <r>` · `--size N` (default 5) · `--count N` (default 4) · `--seed N` · `--list-factions`/`--list-environments`/`--list-npcs`/`--list-all` | `monster_catalog.yaml` (+ `.custom`) | tabelle markdown con calcolo CR + link ai file sorgente |
| `suggest_map.py` | Sceglie una griglia tattica ASCII (quadretti da 5 ft) | `--env <amb>` · `--type <tipo>` · `--name <id>` (nome file senza `.yaml`) · `--list` | `scripts/map_templates/*.yaml` (11 inclusi) | griglia pronta da stampare + legenda + note tattiche |
| `suggest_loot.py` | Proposte di tesoro per EL/fazione (solo SRD) | `--el N` · `--from-encounter <file>` · `--proposal N` · `--factions a,b` · `--pcs N` (default 4) · `--wild` · `--no-magic` · `--dense` (+25%) · `--sparse` (−25%) · `--include-fr-themed` · `--seed N` · `--all-proposals` | `loot_tables.yaml` + `magic_items_srd.yaml` | tabelle loot markdown |

### Mappe (renderer "pergamena" · import · export)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `render_map_svg.py` | Renderizza le griglie-emoji in SVG di qualità stampa, stile **"pergamena"** (texture procedurali, bordi inchiostrati, ombre, token stile VTT, coordinate, scala, **bussola/Nord**, legenda — deterministico, zero asset esterni). Direttive `@` opzionali nel blocco (dopo la griglia) aggiungono un overlay professionale + legenda **INDICAZIONI**: `@north` (orientamento), `@path` (rotte/movimenti), `@mark` (callout numerati), `@zone` (aree etichettate) | *files…* (uno o più `.md`) · `-o <dir>` · `--map N` (solo mappa N, 1-based) · `--list` | markdown `*MAPPE*`/`*Ultra-Clear*` con griglie emoji | `rendered/*.svg` accanto al sorgente (il markdown resta il master) |
| `import_watabou.py` | Converte un export JSON di Watabou One Page Dungeon in un master griglia-emoji conforme al template | *json_file* · `-o <file.md>` · `--pad N` (default 1) | JSON da watabou.github.io/dungeon.html | nuovo `*.md` con griglia + scheletro companion |
| `compile_map_json.py` | **Modalità 3**: compila un contratto JSON rigido (schema `scripts/schemas/tactical_map.schema.json`) in un master griglia-emoji. Valida coordinate/simboli/geometria e **rigetta** gli input errati (loop LLM); astrazione per unità/aree occupate (non un token per soldato). Emette le direttive `@` (orientamento `north`, `movements`/rotte, roster numerato, aree etichettate) rese come overlay professionale da `render_map_svg.py` | *spec.json* · `-o <file.md>` · `--validate-only` | JSON prodotto da un LLM (vedi `scripts/examples/`) | nuovo `*.md` griglia + companion (FORZE) + direttive `@` |
| `export_uvtt.py` | Esporta un master griglia-emoji in file **Universal VTT** (`.uvtt`/`.dd2vtt`): muri (`line_of_sight`), porte (`portals`) e luci per **import nativo Foundry VTT / Roll20** | *file.md* · `-o <dir>` · `--map N` · `--ppg N` (default 100) · `--ext uvtt\|dd2vtt` · `--image <png>` · `--list` | markdown con griglie emoji | `rendered/vtt/*.uvtt` (gitignorato — artefatto locale) |
| `import_ultraclear.py` | **Modalità 3 "al contrario"**: importa una mappa **ultra-clear** (griglia emoji + tabelle coordinate + posizioni PG) ed emette una **bozza** del contratto JSON **+ report conflitti** figura↔tabella (registro regole R1-R12; default: la tabella vince). Riusa il parser di `render_map_svg` (single source of truth). Il `--json-report` è consumabile da un editor visuale (contratto `scripts/schemas/map_conflicts.schema.json`: `uid`, `observed`/`expected`, `target` JSON-Pointer, `actions`). **Contratto I/O dettagliato**: `scripts/README-import-ultraclear.md` | *input.md* · `-o <file.json>` · `--conflicts <md>` · `--json-report <json>` · `--emit-md <dir>` · `--map N` · `--strict` · `-q\|-v` | markdown `*Ultra-Clear*` con griglia + tabelle | `*.draft.json` + report; exit 0/1/2 (1 = ERROR → human-in-the-loop) |
| `export_map_png.py` | Rasterizza un SVG renderizzato in PNG hi-res (stampa, VTT, input per la passata ComfyUI "hero map"). Due motori: **Inkscape** (preferito: renderer SVG vero, prende le misure d'uscita senza viewport) e **Chromium/Chrome** headless (storico). Se non c'è nessuno dei due dice quale installare ed esce pulito | *svg* · `-o <file.png>` · `--scale F` (default 2.0) · `--renderer auto\|inkscape\|browser` · `--inkscape <bin>` · `--browser <bin>` | `rendered/*.svg` | PNG locale (gitignorato — mai committato) |
| `validate_maps.py` | Gate CI: coerenza griglie-emoji ↔ SVG renderizzati | `--repo-root <dir>` (default `.`) | markdown `*MAPPE*` + `rendered/*.svg` | exit 0/1 (gira in `.github/workflows/ci.yml`) |

### Post-sessione (canone: XP · state.md)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `update_xp.py` | Registro XP cumulativo per PG | `--check` (mostra il diff, non scrive) | `campaign/sessions/*.md` `## XP awarded` | `campaign/pg/xp-ledger.md` (auto) |
| `state_sync.py` | Propone modifiche al canone di campagna dopo una sessione, **dicendo in quale dei tre master va ciascuna** (ADR-0050) | `--since YYYY-MM-DD` · `--session <file>` | `## World events triggered` nei log | report diff markdown (il DM applica a mano) |
| `state_apply.py` | **Applica** il sottoinsieme meccanico delle proposte — changelog dentro la regione `auto:`, e **in `campaign/state.yaml`** March Clock (D14), clock dei villain e `stato` su morte e fuga (D16) — con diff e conferma per blocco (ADR-0007); rigenera le regioni `gen:state:` dopo aver toccato il master. Legge il **front-matter dei delta** del log (villain per `png_id`, tutto o niente); solo senza ricade sulla regex di `state_sync` | `--migrate` (inserisce i marker, idempotente) · `--session <file>` · `--check` · `--yes` · `--commit` | proposte di `state_sync` + regioni `auto:` + `state.yaml` | `state.yaml`, `state.md` e `state-changelog.md` aggiornati (su conferma; commit dedicato) |
| `render_state.py` | Genera le **otto tabelle** di `state.md` da `state.yaml`: master e vista, mai due master | `--check` (gate CI) · `--stdout` | `campaign/state.yaml` | regioni `<!-- gen:state:… -->` di `campaign/state.md` |
| `next_session.py` | Brief DM + teaser player per la prossima sessione (aggregatore deterministico: hook aperti, finestre §0 vs March Day, party §1, clock villain ≤2 tick) | `--last-n N` · `--hype` (vesti Homebrewery) | `state.md` + `sessions/*.md` | `campaign/next/brief-*-DM.md` (⚠️ SOLO DM) · `teaser-*-PLAYERS.md` (spoiler-safe) · `next/homebrew/*.hb.md` |
| `session_wizard.py` | Wizard guidato di fine sessione: Q&A con default → session log canonico dal template (formato garantito per `update_xp`/`state_sync`), con in testa il **front-matter dei delta** risolti contro `campaign/state.yaml` (`dmcore/delta_sessione.py`, lotto 4e), commit automatico | `--answers <file.json>` (non-interattivo, test/CI) · `--out <nome>` · `--no-commit` · `--no-guard` (solo test) | risposte del DM | `campaign/sessions/YYYY-MM-DD_session-N.md` |
| `campaign_branch.py` | Guardia e gestione del branch-per-gruppo (mai canone su `main`) | `status` · `guard` · `ensure [--group <nome>]` | `campaign/group.yaml` + git | branch `campaign-group-<nome>` attivo / exit code per la guardia |

### Materiali giocatore / DM (Homebrewery V3)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `session_recap.py` | Recap italiano spoiler-safe (tono R.A. Salvatore) | `--last-n N` (default 1) · `--out <file>` · `--pdf` · `--seed N` · `--pg <PG>` (recap personale: + blocchi `## Split` suoi, in `recaps/pg/`) | ultimi N log + righe pubbliche di state.md §0 | `campaign/recaps/recap-YYYY-MM-DD.md` (+ PDF opz.) |
| `hype_homebrew.py` | Impagina recap o handout in layout Homebrewery V3 | `--recap <file>` (default: l'ultimo) · `--pg <PG>` (veste dell'ultimo recap per-PG → `recaps/homebrew/pg/`) · `--handout TIPO` · `--da <file>` · `--sezione <str>` · `--out <file>` · `--cronologia` | recap/handout + `campaign/templates/homebrew/*.hb.md` | `.hb.md` da incollare su homebrewery.naturalcrit.com |
| `dm_dossier.py` | ⚠️ **SOLO DM**: fotografia di tutte le trame da state.md (§0-§7) con cornici stile RHoD, banner SOLO DM | *(nessuno)* | `campaign/state.md` | `campaign/DM-DOSSIER.hb.md` |
| `build_booklet_html.py` | Booklet in stile **«pergamena Homebrewery»** (stile CANONICO, **ADR-0013**): copertina, tab per capitolo, cornici, SVG inline, raster embeddate come data-URI (Pillow opzionale per ricomprimere >600 KB). Doppia via: HTML autonomo e/o sorgente **Homebrewery V3** `.hb.md` per l'editor self-hosted/Docker (`dm.py hype`). CSS di stampa incluso: in stampa resta SOLO la scheda attiva, A4 a piena pergamena (bottone «🖨 Salva PDF», deep-link `#cN`). I markdown restano i master (ADR-0003). Regola player-facing: teaser di sessione SEPARATO e spoiler-free (titolo evocativo, mai il nome dello scontro) | `<manifest.json>` (obbl.) · `--out <file>` · `--format html\|hb\|both` | manifest `*.manifest.json` + i master .md che elenca (es. `07_.../homebrew/sessione-terros/*.manifest.json`, `09_.../homebrew/PALIO-BOOKLET.manifest.json`) | `.html` autonomo (no server/Docker) e/o `.hb.md` V3 |
| `extract_scene_prompts.py` | **Scene illustrabili di un arco → scheletro dei prompt immagine** (ADR-0015): trova i read-aloud dei master, ne ricava fonte/sezione/estratto, censisce le immagini già presenti e scrive una **scheda per scena** da compilare. Rigenerazione **idempotente**: le schede già scritte restano, quelle aggiunte a mano (artefatti, ritratti) vengono riportate in coda | `<arco>` (obbl.) · `-o <file>` · `--list` | i master `.md` dell'arco + `<arco>/Immagini/` | `<arco>/Immagini/PROMPT-IMMAGINI-<TAG>.md` |
| `export_booklet_pdf.py` | **PDF A4 delle schede** di un booklet (ADR-0013 §5-bis): Chromium/Chrome headless sull'HTML già generato, resa identica al browser; default = un PDF per ogni pagina ✉ player (hint/echi/teaser), così ogni giocatore riceve solo la sua | `<manifest.json>` (obbl.) · `--pane cN…` · `--all` · `--list` · `--outdir <dir>` · `--browser <bin>` | manifest + HTML del booklet; binario Chromium/Chrome (PATH, `$BOOKLET_CHROME`, /opt/pw-browsers) | `pdf/NN-<titolo>.pdf` accanto al manifest (gitignored: artefatti locali) |
| `export_booklet_typst.py` | **Edizione da stampa** (ADR-0020): dallo stesso manifest un **volume unico** PDF con tipografia OFL embedded (EB Garamond + Cinzel), due colonne, fregi di capitolo e segnalibri veri — affianca `export_booklet_pdf.py`, non lo sostituisce. Un capitolo marcato `"layout": "schede"` viene invece impaginato come **scheda pregenerata**: una pagina A4 per personaggio, ritratto e statblocco, coi dati letti dai master `PREGEN-*.md` + `FASCICOLO-*.md` (nessuna copia dei numeri). `front_matter: false` toglie frontespizio e indice. `--formato a5` compone il **libretto** a una colonna (9.6 pt) da imporre poi due-su-A4 con `dm volume --imposto` (ADR-0027): imporre un volume già A4 scalerebbe il corpo al 71% | `<manifest.json>` (obbl.) · `--all` · `--per-scheda` · `--carta {avorio,bianca}` · `--formato {a4,a5}` · `--keep-typ` · `--list` | manifest + master .md + `scripts/typst/{tema-rumblingstone,scheda-pg}.typ` + i font OFL di `scripts/fonts/`; binario **typst** (se manca: dice come installarlo ed esce pulito) | `<nome>-STAMPA.pdf` accanto al manifest, e con `--per-scheda` anche `schede/<nome>-N-<pg>.pdf` (gitignored: artefatti) |
| `validate_booklets.py` | **Gate dei booklet**: valida ogni `*.manifest.json` contro `schemas/booklet_manifest.schema.json`, verifica che capitoli, copertina, introduzione e **immagini dei master** esistano, dichiara quali chiavi consuma ciascuna delle due catene, e con `--stampa` **compila davvero** ogni volume controllando che il PDF abbia i segnalibri. È il controllo che mancava: due booklet della campagna non avevano mai compilato | `[manifest…]` · `--stampa` · `--spiega` · `--json` | tutti i `*.manifest.json` del repo + i master citati; binario **typst** solo per `--stampa` (se manca, salta dichiarandolo) | exit 0/1 + elenco errori (gira in CI) |

### Bestiario / catalogo mostri

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `build_monster_catalog.py` | Indicizza ogni statblocco del repo | *(nessuno)* | `Bestiario/` (mostri/villain/png/pregen-pcgen), `*STATBLOCCHI*.md`, cartelle archi | `scripts/monster_catalog.yaml` (+ `monster_catalog.custom.yaml` vuoto per aggiunte DM) |
| `extract_statblocks.py` | **Statblocchi machine-readable** (ADR-0021): ricava dalla prosa delle schede il blocco ` ```statblocco ` e con `--apply` lo scrive **solo dove l'estrazione è completa**; le altre finiscono in un rapporto con scritto cosa manca. `--check` è il gate CI: blocchi leggibili, campi obbligatori, e GS del blocco = GS del nome del file | `[file…]` · `--apply` · `--check` · `--json` | `Bestiario/**/*.md` | i master aggiornati (solo con `--apply`) + rapporto su stdout |
| `validate_prosa.py` | **Misura `italiano-nativo.md`** ([ADR-0025](../plans/adr/ADR-0025-riapertura-prosa-tradotta.md)): calchi a firma inequivocabile *sempre* (`realizzi che`, `assumi che`, `eventualmente`); possessivo sulle parti del corpo e progressivo **solo nel read-aloud**, perché dipendono dal registro; **i tic a densità** — antitesi «non X: è Y» max 1 per documento, maiuscole di portento max 1, trattini lunghi; e la **forma inglese** di un nome che il glossario vuole tradotto (*Anvil of the World* → *Incudine del Mondo*). **Non bloccante** finché il rumore non è a zero | `[file…]` · `--strict` | i `.md` narrativi + `GLOSSARIO-E-LOCALIZZAZIONE.md` | exit 0/1 + elenco (gira in CI, `continue-on-error`) |
| `validate_lingua.py` | **Refusi meccanici dell'italiano** nel contenuto: accenti (`perchè`→perché, `nè`→né, `sè stesso`), `pò`→po', `qual'è`, d eufonica davanti a consonante, spazio prima della punteggiatura, doppi spazi. Salta blocchi di codice, inline, URL, front-matter e **le guide alla pronuncia** (dove l'accento grave è messo apposta). **Non bloccante in CI** finché il rumore non è a zero — poi `--strict` | `[file…]` · `--strict` | i `.md` degli archi, `campaign/`, `Bestiario/`, `PG/`, i moduli | exit 0/1 + elenco (gira in CI, `continue-on-error`) |
| `validate_standalone.py` | **Gate dei moduli autoconclusivi**, in due famiglie. `STANDALONE-*/` (master markdown): file obbligatori, riferimenti incrociati, schede pregenerate, termini 5e vietati, read-aloud minimi, contatori dichiarati, generatori locali (ADR-0017 §4). `10-stand-alone/*/` (moduli scritti **in HTML**, fuori da ADR-0003 e da entrambe le catene di impaginazione): `<title>`, `<h1>`, link relativi risolvibili, ancore che esistono davvero — anche quelle verso un altro file — e `id` non duplicati. La seconda famiglia non aveva **nessun** gate fino al 2026-09-02 | `--dir <cartella>` | `STANDALONE-*/**/*.md` + `10-stand-alone/*/*.html` | exit 0/1 + elenco violazioni (gira in CI) |
| `validate_bestiario.py` | Gate CI della libreria `Bestiario/`: struttura standard, naming `-crN` kebab, header richiesti, CR filename↔header, catalogo in sync. Con `--rules` (warning non bloccante in CI): benchmark PF1e su hp/AC, policy flag `[INFERRED]`, `Boost log:` obbligatorio | `--rules` · `--help` | `Bestiario/{mostri,villain,png}/**/*.md` + `monster_catalog.yaml` | exit 0/1 + lista violazioni (gira in CI) |

### Pipeline skill multi-agente

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `build-skills.sh` | Costruisce i pacchetti skill per-agente (compact.md/machine.json/…) e li deploya in `~/.<agent>/skills/` | `--dry-run` · `--measure` · `--skill <nome>` · `--no-deploy` (build only, per CI) | `skills/*/` | `build/<skill>/*` + mirror per-agente (gitignorati) |
| `sync-skills.sh` | Build + popola i mirror in-repo localmente | `--dry-run` · `--no-build` | `skills/*/` | mirror `.claude/`, `.cursor/`, … (gitignorati) |
| `validate_skills.py` | Gate CI skill: SKILL.md valido, link e dati YAML coerenti | `--repo-root <dir>` (default: root repo) | `skills/**/*.md` + YAML | exit 0/1 + warning (gira in CI) |
| `index_skills.py` | Genera `index.json` per skill compressa | `--input <dir>` · `--build <dir>` · `--output <path>` | skill originali + build | `index.json` |
| `compress_skills.py` | Comprime le skill per gli agenti (riduzione token) | `--input <file\|dir>` · `--output <dir>` · `--measure` | `.md` skill | `.md` compressi (+ report se `--measure`) |
| `measure_tokens.py` | Misura la dimensione in token delle skill | `--tokenizer chars/4\|tiktoken` · `--json` | `skills/**/*.md` | tabella (o JSON) di conteggi token |

### Gestione campagna / orchestrazione

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `dm.py` | **Entrypoint unico** — orchestra tutto per fase del Playbook (vedi tabella sottocomandi sopra) | `<sottocomando>` + flag passthrough | dipende dal sottocomando | ciò che produce lo script sottostante |
| `new-campaign-group.sh` | Reset branch-per-gruppo: nuovo branch di campagna con stato azzerato dai template | *new-group-name* · `--backup-current <current-group-name>` | template `campaign/templates/` | nuovo branch `campaign-group-<nome>` |
| `dmcore/` (libreria) | Logica condivisa dei flussi ADR-0007: `regions` (marker `auto:` con contratto "fuori byte-identici"), `gitio` (guardia branch, commit), `config` (group.yaml), `visibility` (policy per-PG dei blocchi `## Split`), `censimento` (le **tre** forme di statblocco in uso negli archi, e i master che la matrice delle versioni dichiara dentro `_ARCHIVIO/` — ADR-0054) | *(non è un CLI — la importano gli script sopra)* | — | — |
| `tests/` | Suite unittest dei flussi ADR-0007 (regioni, apply, guardia, next) su repo git temporanei | `python3 -m unittest discover -s scripts/tests` | fixture in-memory | verde/rosso (gira anche in CI) |
| `check_plans_discipline.py` | Gate della regola d'oro dei piani (ADR-0009): modifiche strutturali (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza riga in `plans/CHANGELOG.md` → exit 1; promemoria ADR (warning) su nuova skill/nuovo script/workflow CI toccati senza `plans/adr/`. Gira in CI (solo PR) e come hook `pre-push` | `--base <ref>` (default `origin/main`) · `--head <ref>` · `--repo-root <dir>` | diff git base…head | exit 0/1 + report |
| `install-git-hooks.sh` | Installa gli hook git locali: `post-merge` (resync mirror skill dopo `git pull`) e `pre-push` (gate ADR-0009) | *(nessuno)* | — | hook in `.git/hooks/` |

## Typical DM workflow

```bash
python3 scripts/dm.py prep --el 13 --env forest --factions red-hand  # before the session
python3 scripts/dm.py post --session 2026-05-01_session-42.md        # after the session
python3 scripts/dm.py recap --hype                                    # 1-2 days before next
```

## Extending

- **Add a custom monster**: append to `scripts/monster_catalog.custom.yaml`
  (same schema: `id / name / cr / faction / role / environment / source_file`).
  `suggest_encounter.py` merges it automatically.
- **Add a map**: drop a new YAML in `scripts/map_templates/` (copy an
  existing one). `suggest_map.py` picks it up on next run.
- **New trigger for state_sync**: edit the `TRIGGERS` regex list at the top
  of `scripts/state_sync.py`. ⚠️ Serve solo ai log **senza** front-matter: per
  una scrittura meccanica nuova il posto è il delta
  (`scripts/dmcore/delta_sessione.py`), che nomina per `png_id` invece che per
  nome.

## Mappe di qualità professionale (stile "pergamena")

`render_map_svg.py` produce battle map illustrate in stile handout
professionale (benchmark: le mappe ufficiali di *Red Hand of Doom* e gli
export di Dungeon Scrawl/DungeonDraft): regioni terreno **organiche**
(contorni tracciati e smussati, niente scalini), occlusione ambientale
accanto ai muri, variazione tonale anti-ripetizione, e una **libreria di
prop vettoriali originali** (porta, letto, cassa, braciere, albero,
teschio…) al posto degli emoji — disegnati in-house seguendo le
convenzioni della cartografia professionale, mai ricalcati da asset
altrui. Tutta la grafica è **procedurale** (pattern, filtri e simboli
SVG): niente asset esterni, niente vincoli di licenza, output
byte-deterministico (requisito di `validate_maps.py` in CI). La legenda
universale è estesa con i simboli locali più usati negli archi (⛰ montagne
come terreno, ⬇🏛🌋🗿🌉🎯🖼✨⚔) e con il corredo classico da dungeon ed
esterni (⚰🛢🪜🦴🍄🕯🌾⛺🔮🪑🧱) — la tabella `SYMBOLS` nel renderer è la
fonte di verità.

La pipeline completa (vedi `plans/RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md`
per il razionale e le alternative valutate):

1. **Mappe esistenti**: la griglia emoji resta il MASTER; ogni modifica al
   markdown si rigenera con `python3 scripts/render_map_svg.py <file.md>`.
2. **Nuovi dungeon**: generare il layout su
   https://watabou.github.io/dungeon.html → Export JSON →
   `python3 scripts/import_watabou.py dungeon.json -o <arco>/NUOVA-MAPPA.md`
   → adattare la griglia e compilare i companion → renderizzare.
3. **Mappe regionali** (Dalelands/Cannath Vale): Azgaar Fantasy Map
   Generator (https://azgaar.github.io/Fantasy-Map-Generator/, MIT) —
   committare il file `.map` come master + l'export SVG/PNG.
4. **Città** (Rethmar, Palio): Medieval Fantasy City Generator
   (https://watabou.github.io/city-generator/) — committare l'export SVG
   annotando il **seed** nell'URL per la rigenerazione.
5. **Hero map** (opzionale, richiede PC locale con GPU): passata pittorica
   ComfyUI + ControlNet pilotata da Claude via comfyui-mcp, con il render
   del repo come input strutturale — guida completa nella skill
   `skills/rumblingstone-mapmaking/references/hero-map-comfyui.md`.
   Output in `rendered/hero/` (gitignored, fuori CI).

L'intero workflow è codificato nella skill **`rumblingstone-mapmaking`**
(`skills/`): la build pipeline (`./scripts/build-skills.sh`) la distribuisce
a Claude Code/Cursor/Windsurf come le altre skill del repo, così ogni
sessione agente sa creare, modificare e renderizzare mappe senza contesto
aggiuntivo.

## Design rules

- Python 3 stdlib only (no `pip install` required).
- Every script is idempotent and safe to re-run.
- No script writes to `campaign/state.md` or `campaign/sessions/*.md`
  automatically — those remain DM-owned canon.
- All generated files carry an "Auto-generated — do not edit by hand" header.
