# RumblingStone — DM automation scripts

Zero-burden helpers that read what the DM already writes (session logs,
state.md, Armate atlas) and produce prep material. **Nothing overwrites
canon** — scripts either generate new files or print suggestions for
manual review. Respects `AGENTS.md`: we never invent statblocks; we only
index/compose what exists (or mark it INFERRED with a question and a base, see `docs/reference/GUIDA-MARCATURE.md`).

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
> → [`docs/how-to/GUIDA-BOOKLET-E-PDF.md`](../docs/how-to/GUIDA-BOOKLET-E-PDF.md)
> (prerequisiti per ogni sistema, anatomia del manifest, comandi, container
> opzionali, troubleshooting, checklist di consegna). Qui sotto c'è la
> **mappa degli strumenti**; là c'è il **come si fa**.

> 🎨 **Immagini della campagna** (prompt, generatori, coerenza d'arco):
> [`docs/how-to/GUIDA-IMMAGINI.md`](../docs/how-to/GUIDA-IMMAGINI.md).

**Sottocomandi `dm.py`** (ognuno inoltra i flag allo script sottostante):

| Sottocomando | Flag | Fa girare | Fase Playbook |
|---|---|---|---|
| `prep` | `--el N` · `--env <amb>` · `--refresh` (rigenera il catalogo) | `suggest_encounter` + `suggest_map` + `suggest_loot` | §2 pre-sessione |
| `maps` | `render`\|`validate` + `files...` | `render_map_svg` / `validate_maps` | prep |
| `post` | `--session <file>` | `update_xp` + `state_sync` | §4 post-sessione |
| `session` | `end`\|`next`\|`recap`\|`status`\|`branch` · `--session <file>` (end; senza → wizard) · `--yes` · `--last-n N` · `--hype` · `--pg <PG>` (recap) · `--group <nome>` | `campaign_branch` + `session_wizard` + `update_xp` + `state_apply` / `next_session` / `session_recap --pg` + `hype_homebrew --pg` | §4 + §7 (branch-per-gruppo, ADR-0007) |
| `gruppo` | `nuovo` · `--answers <json>` · `--domande` (il modulo come JSON) · `--dry-run` | `gruppo_nuovo` (+ `azzera_partita`) | §7 gruppo nuovo |
| `recap` | `--last-n N` · `--pdf` · `--hype` | `session_recap` (+ `hype_homebrew`) | §4.6 |
| `handout` | `--tipo T` (obbl.) · `--da <file>` · `--out <file>` | `hype_homebrew --handout` | prep |
| `bestiario` | `estrai`\|`deriva`\|`attributi`\|`creatura`\|`conformita` + i flag dello script (anche `--help`) | `extract_statblocks` / `derive_statblocks` / `genera_attributi` / `genera_creatura` / `conformita_statblocchi` | prep (creature; il codice d'uscita è quello dello script) |
| `sistemi` | i flag di `sistemi.py` (anche `--help`): nessuno = sistemi attivi e matrice strumenti × sistemi · `--di FILE` · `--check` · `--json` · `--skill` · `--skill-escluse` | `sistemi` | tutte (ADR-0111; guida in [`GUIDA-SISTEMI-DI-GIOCO`](../docs/how-to/GUIDA-SISTEMI-DI-GIOCO.md)) |
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
| `collaudo_mappe.py` | **Collaudo delle mappe come grafo** (ADR-0082): simboli ignoti, legende locali che rovesciano un universale, nord obbligatorio nelle tattiche, porte nel muro, scale con la loro gemella (`@collega`), porte segrete fuori dalla vista dei giocatori (`@vista giocatori`), unità e obiettivi raggiungibili con le regole SRD (niente diagonale oltre l'angolo di un muro), ingombro dei Grandi (`@taglia`), l'asse di porte, grate e sbarre (ADR-0083, `@verso` per i casi ambigui), M1, M2 e M4 esatta come avvisi. Classi E (errore) e A (avviso), `@tipo` e `@deroga` nella griglia. Richiede `tcod` (`requirements-dev.txt`, ADR-0084) | *files…* (default: il corpus) · `--json <out>` · `--strict` · `--solo-errori` | markdown con griglie emoji + `scripts/legend.json` | rapporto testo o JSON (`scripts/schemas/map_findings.schema.json`); exit 0/1/2, sola lettura |
| `confronta_mappe.py` | **Due o più versioni delle stesse mappe, misurate cella per cella**: celle cambiate (simboli e classi), Jaccard per classe di cella, transizioni di classe, NCD, voto di `qualita_mappe.py` prima e dopo con i rilievi spariti e comparsi, dimensioni, scala e quote. Con `--versioni` estrae i master da git e abbina le mappe per titolo, codice o posizione; SVG affiancato con le celle cambiate cerchiate. Richiede `tcod` | *VECCHIA.md[:N] NUOVA.md[:N]* · `--json <out>` · `--svg <out>` · oppure `--versioni A=REF … --base A --out <dir> [--estrai <dir>] FILE…` · `--strict` | markdown con griglie emoji, ref git | JSON a chiavi ordinate + SVG; exit 0/1/2, non tocca le mappe |
| `validate_maps.py` | Gate CI: coerenza griglie-emoji ↔ SVG renderizzati | `--repo-root <dir>` (default `.`) | markdown `*MAPPE*` + `rendered/*.svg` | exit 0/1 (gira in `.github/workflows/ci.yml`) |

### Post-sessione (canone: XP · state.md)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `update_xp.py` | Registro XP cumulativo per PG | `--check` (mostra il diff, non scrive) | `campaign/sessions/*.md` `## XP awarded` | `campaign/pg/xp-ledger.md` (auto) |
| `verifica_px.py` | **Il registro dei PX torna?** (ADR-0148): R1 la somma delle righe è il totale; R2 il livello dai PX segue la tabella dei PX del PHB, Table 3–2 (non è nell'SRD); R3 si sale di un livello alla volta (DMG cap. 2) e i PX non stanno sotto la soglia del livello al tavolo; R4 il livello al tavolo è quello effettivo di `state.yaml` (ECL se scritto, altrimenti classi più LA) e ogni PG dei totali ha la sua riga. Uscita nella forma di ADR-0124 (regola, atteso, ha, fonte, file:riga). Cancello bloccante in CI | *registro* (default `campaign/REGISTRO-PX.md`) · `--state <file>` · `--json` | `campaign/REGISTRO-PX.md` + `campaign/state.yaml` | exit 0/1 + violazioni (gira in CI) |
| `state_sync.py` | Propone modifiche al canone di campagna dopo una sessione, **dicendo in quale dei tre master va ciascuna** (ADR-0050) | `--since YYYY-MM-DD` · `--session <file>` | `## World events triggered` nei log | report diff markdown (il DM applica a mano) |
| `state_apply.py` | **Applica** il sottoinsieme meccanico delle proposte — changelog dentro la regione `auto:`, e **in `campaign/state.yaml`** March Clock (D14), clock dei villain e `stato` su morte e fuga (D16) — con diff e conferma per blocco (ADR-0007); rigenera le regioni `gen:state:` dopo aver toccato il master. Legge il **front-matter dei delta** del log (villain per `png_id`, tutto o niente); solo senza ricade sulla regex di `state_sync` | `--migrate` (inserisce i marker, idempotente) · `--session <file>` · `--check` · `--yes` · `--commit` | proposte di `state_sync` + regioni `auto:` + `state.yaml` | `state.yaml`, `state.md` e `state-changelog.md` aggiornati (su conferma; commit dedicato) |
| `render_state.py` | Genera le **otto tabelle** di `state.md` da `state.yaml`: master e vista, mai due master | `--check` (gate CI) · `--stdout` | `campaign/state.yaml` | regioni `<!-- gen:state:… -->` di `campaign/state.md` |
| `next_session.py` | Brief DM + teaser player per la prossima sessione (aggregatore deterministico: hook aperti, finestre §0 vs March Day, party §1, clock villain ≤2 tick) | `--last-n N` · `--hype` (vesti Homebrewery) | `state.md` + `sessions/*.md` | `campaign/next/brief-*-DM.md` (⚠️ SOLO DM) · `teaser-*-PLAYERS.md` (spoiler-safe) · `next/homebrew/*.hb.md` |
| `session_wizard.py` | Wizard guidato di fine sessione: Q&A con default → session log canonico dal template (formato garantito per `update_xp`/`state_sync`), con in testa il **front-matter dei delta** risolti contro `campaign/state.yaml` (`dmcore/delta_sessione.py`, lotto 4e), commit automatico | `--answers <file.json>` (non-interattivo, test/CI) · `--out <nome>` · `--no-commit` · `--no-guard` (solo test) | risposte del DM | `campaign/sessions/YYYY-MM-DD_session-N.md` |
| `azzera_partita.py` | Azzera la **partita** per un gruppo nuovo (stato, storico, sessioni, recap, brief, dossier) e lascia il **prodotto** (ADR-0050 §7). L'elenco è un dato, `dmcore/partita.py`; valida il nuovo `state.yaml` **prima** di scrivere e rigenera `state.md`. Lo chiama `new-campaign-group.sh` | `--check` (elenca, non scrive) | i template in `campaign/templates/`, l'anagrafica `png` dello `state.yaml` di prima | i tre master azzerati; sessioni, recap e file generati tolti |
| `gruppo_nuovo.py` | Il **gruppo nuovo da un modulo** (lotto 4f-4, D19/D21): deriva lo stato dal prodotto di oggi, chiede gruppo, arco, livello e PG, poi le righe con tracce del primo tavolo una alla volta (tieni/svuota/rivedi); valida prima di scrivere, crea il ramo, chiama `azzera_partita` e committa. La logica è in `dmcore/gruppo_nuovo.py` | `--answers <json>` · `--domande` · `--dry-run` | `campaign/state.yaml` di oggi, le risposte del DM | ramo `campaign-group-<nome>` con stato, `state.md` e `group.yaml` nuovi |
| `campaign_branch.py` | Guardia e gestione del branch-per-gruppo (mai canone su `main`; `guard` rifiuta anche un ramo morto di `plans/rami-di-gruppo.json`) | `status` · `guard` · `ensure [--group <nome>]` | `campaign/group.yaml` + git | branch `campaign-group-<nome>` attivo / exit code per la guardia |
| `sincronia_giocato.py` | **Misura**, senza scrivere niente, se il giocato è arrivato sul ramo di gruppo e se `main` ci è entrato (ADR-0149): S1 rami non registrati, S2 main indietro, S3 patch ferme, S4 campi aperti al DM, S5 serata non registrata, S6 campi chiusi senza «(DM, AAAA-MM-GG)», S7 righe di main perse nel merge | `--check` · `--aggiorna` · `--scansiona DIR` · `--ref HEAD` (prima del push) · `--dopo-merge` · `--avviso` (hook) · `--json` | git, `plans/rami-di-gruppo.json`, le cartelle scansionate | rilievi 🔴/🟡/⚪ con il comando che li risolve; exit 1 con un rosso, 2 se non misurabile |

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
| `validate_booklets.py` | **Gate dei booklet**: valida ogni `*.manifest.json` contro `schemas/booklet_manifest.schema.json`, verifica che capitoli, copertina, introduzione e **immagini dei master** esistano, dichiara quali chiavi consuma ciascuna delle due catene, e con `--stampa` **compila davvero** ogni volume controllando che il PDF abbia i segnalibri e non stampi apparato di lavoro oltre il tetto del volume (ADR-0070). È il controllo che mancava: due booklet della campagna non avevano mai compilato | `[manifest…]` · `--stampa` · `--spiega` · `--json` | tutti i `*.manifest.json` del repo + i master citati; binario **typst** solo per `--stampa` (se manca, salta dichiarandolo) | exit 0/1 + elenco errori (gira in CI) |
| `validate_corredo.py` | **Il corredo della serata** (norma in `rumblingstone-automation`): da un `*.corredo.json` controlla che ci siano booklet del DM, volume dei fogli, echi di ogni PG, carte e handout, che i fogli ✉ stiano solo nel volume dei giocatori e nessun capitolo in due volumi (ADR-0070), che ogni immagine dei prompt esista e abbia la sua riga nel confronto immagine-scheda, e che nessun box superi le 12 righe. Con `--stampa` compila ogni volume e misura il PDF (sovrapposizioni, testo a meno di 30 pt dal bordo, apparato di lavoro contro `apparato-residui.json`; PyMuPDF in `requirements-dev.txt`). `dm.py corredo` lo chiama prima e dopo i volumi | `[corredo…]` · `--stampa` · `--pdf` · `--rigoroso` · `--json` | i `*.corredo.json` del repo e ciò che citano; **typst** per `--stampa`, **PyMuPDF** facoltativo (se manca, la misura del PDF si dichiara saltata) | exit 0/1/2 + elenco dei difetti (gira in CI) |

### Bestiario / catalogo mostri

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `build_monster_catalog.py` | Indicizza ogni statblocco del repo | *(nessuno)* | `Bestiario/` (mostri/villain/png/pregen-pcgen), `*STATBLOCCHI*.md`, cartelle archi | `scripts/monster_catalog.yaml` (+ `monster_catalog.custom.yaml` vuoto per aggiunte DM) |
| `extract_statblocks.py` | **Statblocchi machine-readable** (ADR-0021): ricava dalla prosa delle schede il blocco ` ```statblocco ` e con `--apply` lo scrive **solo dove l'estrazione è completa**; le altre finiscono in un rapporto con scritto cosa manca. `--check` è il gate CI: blocchi leggibili, campi obbligatori, e GS del blocco = GS del nome del file | `[file…]` · `--apply` · `--check` · `--json` | `Bestiario/**/*.md` | i master aggiornati (solo con `--apply`) + rapporto su stdout |
| `validate_prosa.py` | **Misura `italiano-nativo.md`** ([ADR-0025](../plans/adr/ADR-0025-riapertura-prosa-tradotta.md)): calchi a firma inequivocabile *sempre* (`realizzi che`, `assumi che`, `eventualmente`); possessivo sulle parti del corpo e progressivo **solo nel read-aloud**, perché dipendono dal registro; **i tic a densità** — antitesi «non X: è Y» max 1 per documento, maiuscole di portento max 1, trattini lunghi; e la **forma inglese** di un nome che il glossario vuole tradotto (*Anvil of the World* → *Incudine del Mondo*). **Non bloccante** finché il rumore non è a zero | `[file…]` · `--strict` | i `.md` narrativi + `GLOSSARIO-E-LOCALIZZAZIONE.md` | exit 0/1 + elenco (gira in CI, `continue-on-error`) |
| `validate_lingua.py` | **Refusi meccanici dell'italiano** nel contenuto: accenti (`perchè`→perché, `nè`→né, `sè stesso`), `pò`→po', `qual'è`, d eufonica davanti a consonante, spazio prima della punteggiatura, doppi spazi. Salta blocchi di codice, inline, URL, front-matter e **le guide alla pronuncia** (dove l'accento grave è messo apposta). **Non bloccante in CI** finché il rumore non è a zero — poi `--strict` | `[file…]` · `--strict` | i `.md` degli archi, `campaign/`, `Bestiario/`, `PG/`, i moduli | exit 0/1 + elenco (gira in CI, `continue-on-error`) |
| `validate_standalone.py` | **Gate dei moduli autoconclusivi**, in due famiglie, tutte e due in `10-stand-alone/`. Moduli con master markdown, riconosciuti dall'hub `00-*.md`: file obbligatori, riferimenti incrociati, schede pregenerate, termini 5e vietati, read-aloud minimi, contatori dichiarati, generatori locali (ADR-0017 §4). moduli scritti **in HTML**, con le pagine al primo livello (fuori da ADR-0003 e da entrambe le catene di impaginazione): `<title>`, `<h1>`, link relativi risolvibili, ancore che esistono davvero — anche quelle verso un altro file — e `id` non duplicati. La seconda famiglia non aveva **nessun** gate fino al 2026-09-02 | `--dir <cartella>` | `STANDALONE-*/**/*.md` + `10-stand-alone/*/*.html` | exit 0/1 + elenco violazioni (gira in CI) |
| `validate_bestiario.py` | Gate CI della libreria `Bestiario/`: struttura standard, naming `-crN` kebab, header richiesti, CR filename↔header, catalogo in sync. Con `--rules` (warning non bloccante in CI): benchmark PF1e su hp/AC, policy flag `[INFERRED]`, `Boost log:` obbligatorio | `--rules` · `--help` | `Bestiario/{mostri,villain,png}/**/*.md` + `monster_catalog.yaml` | exit 0/1 + lista violazioni (gira in CI) |

### Pipeline skill multi-agente

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `build-skills.sh` | Costruisce i pacchetti skill per-agente (compact.md/machine.json/…) e li deploya in `~/.<agent>/skills/` | `--dry-run` · `--measure` · `--skill <nome>` · `--no-deploy` (build only, per CI) | `skills/*/` | `build/<skill>/*` + mirror per-agente (gitignorati) |
| `sync-skills.sh` | Build + popola i mirror in-repo localmente | `--dry-run` · `--no-build` | `skills/*/` | mirror `.claude/`, `.cursor/`, … (gitignorati) |
| `validate_skills.py` | Gate CI skill: SKILL.md valido, link e dati YAML coerenti | `--repo-root <dir>` (default: root repo) | `skills/**/*.md` + YAML | exit 0/1 + warning (gira in CI) |
| `index_skills.py` | Genera `index.json` per skill compressa | `--input <dir>` · `--build <dir>` · `--output <path>` | skill originali + build | `index.json` |
| `compress_skills.py` | Comprime le skill per gli agenti (riduzione token) | `--input <file\|dir>` · `--output <dir>` · `--measure` | `.md` skill | `.md` compressi (+ report se `--measure`) |
| `measure_tokens.py` | Misura la dimensione in token delle skill; per ogni domanda somma anche il preload obbligatorio che il `SKILL.md` dichiara nel suo «load order» (lotto 4j-3), e dice MISSING se un file del preload non esiste | `--tokenizer chars/4\|tiktoken` · `--json` | `skills/**/*.md` | tabella (o JSON) di conteggi token |
| `prove_skill.py` | **Le prove fisse delle skill e degli agenti** (ADR-0114, ADR-0148). Casi delle skill in `skills/<nome>/evals/`, degli agenti in `.claude/agent-evals/<agente>/<caso>/`. `controlla [--agenti]` la forma dei casi; `prepara` ed `esito` la prova alla cieca vecchia/nuova di una skill; `valuta` i giudici deterministici su un'esecuzione registrata; `esempi` controlla che l'esempio buono di ogni caso passi tutti i giudici e il cattivo ne perda almeno uno; `impronta` lo sha256 di agente, skill precaricate e casi; `esegui` lancia `claude -p --agent` sui casi in un git worktree usa e getta e pulito, riportato al commit di partenza dopo ogni caso (costa token, rifiuta la radice del repo, passa `allowed_tools` e vieta push, commit, reset e checkout); `registra` scrive una riga in `.claude/agent-evals/ESITI.jsonl` con l'impronta del worktree, la versione della CLI, i casi falliti (contano 0) e quelli non eseguiti; né `esegui` né `registra` partono dal server MCP; `cricchetto` segnala un agente toccato senza un esito con l'impronta nuova, o con un punteggio sotto il precedente | `<sottocomando>` · `--agente <nome>` · `--caso <id>` (ripetibile) · `--uscita <dir>` · `--cartella-lavoro <worktree>` · `--esecuzioni <dir>` · `--data AAAA-MM-GG` · `--base <ref>` · `--rigoroso` | i casi, `.claude/agents/`, le skill precaricate; CLI `claude` solo per `esegui` | exit 0/1; in CI `controlla`, `controlla --agenti` ed `esempi` bloccanti, `cricchetto --rigoroso` non bloccante (solo PR) |

### Gestione campagna / orchestrazione

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `dm.py` | **Entrypoint unico** — orchestra tutto per fase del Playbook (vedi tabella sottocomandi sopra) | `<sottocomando>` + flag passthrough | dipende dal sottocomando | ciò che produce lo script sottostante |
| `new-campaign-group.sh` | Reset branch-per-gruppo: nuovo branch di campagna con stato azzerato dai template | *new-group-name* · `--backup-current <current-group-name>` | template `campaign/templates/` | nuovo branch `campaign-group-<nome>` |
| `dmcore/` (libreria) | Logica condivisa dei flussi ADR-0007: `regions` (marker `auto:` con contratto "fuori byte-identici"), `gitio` (guardia branch, commit), `config` (group.yaml), `visibility` (policy per-PG dei blocchi `## Split`), `censimento` (le **tre** forme di statblocco in uso negli archi, e i master che la matrice delle versioni dichiara dentro `_ARCHIVIO/` — ADR-0054) | *(non è un CLI — la importano gli script sopra)* | — | — |
| `tests/` | Suite unittest dei flussi ADR-0007 (regioni, apply, guardia, next) su repo git temporanei | `python3 -m unittest discover -s scripts/tests` (in CI: `pytest`, che vede le stesse prove) | fixture in-memory | verde/rosso (gira anche in CI) |
| `verifica_rimandi.py` | **I rimandi per sezione puntano a un titolo che esiste?** (ADR-0148): «FILE §N» e «vedi §N» nei `.md` del repo. Un rimando che non sa risolvere (nome ambiguo, bersaglio senza sezioni numerate, riga che nomina un altro documento) va fra i non verificabili, mai fra le violazioni; quelle già portate al DM stanno in `IN_ATTESA` e non bloccano. In CI in testing fino al 2026-12-04 (`continue-on-error`) | *percorsi…* (default il repo) · `--check` · `--json` | i `.md` del repo | conteggi (tornano, violazioni, in attesa, non verificabili); exit 1 con `--check` su una violazione nuova |
| `instradamento_agenti.py` | Gli hook dei thread di **ADR-0146**: suggerisce agente e catena dal messaggio (tace su card, inoltri del coordinatore, notifiche, resoconti dei sottoagenti e via libera brevi: `testo_di_lavoro`, M2 di ADR-0154; gli omonimi dei trigger li toglie `OMONIMI` di `instradamento_skill.py`), ferma push e PR senza gli agenti della «Catena:» scritta, registra a fine turno. **La misura (ADR-0154)**: `--eval` confronta il primo agente suggerito con il set d'oro di messaggi veri per split dev, test e tutto (accuracy con Wilson, indulgente, macro-F1, baseline maggioritaria, matrice; il bootstrap solo nel testo, non nel JSON); `--check` è il cricchetto sul test contro il `tetto` del file, in CI in testing | `--prompt` · `--stop` · `--cancello` · `--deroga` · `--prova` · `--riepilogo` · `--eval` · `--check` · `--json` · `--oro <file>` | stdin degli hook · `plans/instradamento/agenti-oro.json` | contesto dell'hook · `.claude/.uso-agenti.jsonl` (locale) · tabella o JSON · exit 0/1/2 |
| `raccogli_casi_agenti.py` | **Ogni thread nuovo porta un caso al set d'oro degli agenti** (ADR-0154, M2-bis): sui messaggi che la routine esporta, `proponi` scarta duplicati e testi con email o segreti e mette la predizione dell'hook come «proposta»; `cieco` scrive id e testo per un annotatore cieco; `annota` prende le sue etichette come consigliate delle card (mai la proposta dell'hook) e stampa accordo e kappa; `applica` porta i casi confermati da Jfs nel set d'oro, split per sha256 dell'id, e rimette il tetto con l'hook invariato; `--check` la forma del set | `proponi IN.json --coda DIR` · `cieco DIR/AAAA-Www.json` · `annota DIR/AAAA-Www.json ANNOTAZIONI.tsv` · `applica DIR/AAAA-Www.json SCELTE.tsv` · `--check` · `--oro <file>` · `--oggi AAAA-MM-GG` | messaggi esportati in `/mnt/project-files/instradamento-coda/` (mai nel repo) · `plans/instradamento/agenti-oro.json` | `AAAA-Www.json`, `CARD.md`, `CIECO-AAAA-Www.tsv` nella coda · set d'oro e tetto · exit 0/1/2 |
| `eval_metriche.py` (libreria) | Le metriche di un classificatore contro un set d'oro (ADR-0154, emendamento del 27/11): involucro di `sklearn.metrics` (matrice di confusione, P/R/F1 per classe, macro e micro F1, accuracy, kappa di Cohen, `zero_division=0`), `DummyClassifier` per la baseline maggioritaria, `scipy.stats` per Wilson al 95% e bootstrap con seme. Del repo: accuracy indulgente, insieme vuoto, formato e `macro_f1_esatta` (frazione dai conteggi interi, quella che usano i cancelli). scikit-learn `==1.9.1` da `requirements-dev.txt`, importato solo dentro le funzioni | *(nessuno)*: da sola stampa l'esempio dei test | — | JSON su stdout |
| `check_plans_discipline.py` | Gate della regola d'oro dei piani (ADR-0009): modifiche strutturali (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza riga in `plans/CHANGELOG.md` → exit 1; promemoria ADR (warning) su nuova skill/nuovo script/workflow CI toccati senza `plans/adr/`. Gira in CI (solo PR) e come hook `pre-push` | `--base <ref>` (default `origin/main`) · `--head <ref>` · `--repo-root <dir>` | diff git base…head | exit 0/1 + report |
| `memoria_custode.py` | La memoria del progetto dei thread ha uno specchio e un custode (ADR-0151): `specchia` scrive un'istantanea completa fuori dal repo; `verifica` controlla che ogni riga tolta dall'ultima istantanea sia archiviata nel repo, nel file storico o in coda (esce 1 se no, o se `MEMORY.md` supera 16 KB); `archivia` scrive in coda le righe tolte; `cerca` risponde dalle tre fonti e aggiunge le note collegate con `[[nome]]` (fonte `memoria-link`); `archivia` e `redigi` escono 1 senza un `RISERVATI.txt` leggibile e non vuoto; `redigi` copia la memoria con le righe riservate sostituite da un'impronta. Due hook in testing: merge (strumento MCP, `gh pr merge` e `gh api -X PUT .../pulls/N/merge` da Bash) e scrittura; dal server MCP solo `cerca` e `verifica` | `specchia` · `verifica [--json]` · `archivia [--thread T]` · `cerca PAROLE [--tema T] [--senza-link] [--json]` · `redigi --uscita DIR` · `--hook-merge` · `--hook-scrittura` · `--riepilogo` | la cartella della memoria, `plans/MEMORIA-STORICA.md`, la coda, `RISERVATI.txt` dello specchio | istantanee in `/mnt/project-files/memoria-progetto-specchio/`, voce di coda, `.claude/.custode-memoria.jsonl`; exit 0/1, 2 negli hook |
| `lavoro_in_corso.py` | Il lavoro in sviluppo che non è ancora su `main` (ADR-0157): incrocia il registro curato `plans/lavoro-in-corso.json` con le PR aperte (REST pubblica di GitHub, token facoltativo), i rami di origin e le cartelle di `/mnt/project-files`, e scrive `plans/LAVORO-IN-CORSO.md` con i filoni, ciò che sta senza filone e ciò che è fermo. Non è un cancello: in CI gira solo `--check`, che valida il registro offline. Comando `/lavoro-in-corso` in Claude Code e OpenCode | `--fetch` · `--offline` · `--stdout` · `--json` · `--pr-json FILE` · `--mnt DIR` · `--giorni N` · `--check` | il registro, `plans/contenuti-nei-rami.json`, PR, rami, cartelle condivise (solo nome, data, titolo del LEGGIMI) | `plans/LAVORO-IN-CORSO.md`; exit 0 anche con la rete giù, 1 registro malformato, 2 uso errato |
| `contenuti_nei_rami.py` | I file che esistono in un ramo o in una PR, **chiuse comprese**, e mai su `main` né per nome né per contenuto. Ognuno deve avere un posto nel registro `plans/contenuti-nei-rami.json` (in volo, portato, superato, rifiutato, partita, da decidere). Lotto 4i-2; non è un gate di CI, perché i rami cambiano per conto loro. `fase1.py` ne mostra le righe aperte accanto al bersaglio. Con `--righe RAMO…` confronta riga per riga e vede anche le correzioni a file che `main` ha già (lotto 4j-5) | `--fetch` · `--check` · `--base` · `--json` · `--righe` | i rami del clone, il registro | report; exit 1 con `--check` se una riga non ha posto, con `--righe` se un ramo ha righe mai arrivate |
| `milestone_pronte.py` | **Quale milestone della roadmap è pronta per il rilascio?** (ADR-0152): valuta i criteri di `plans/milestone.json` (comando che esce 0, regex che compare o manca in un file, conferma del DM con data e luogo). Pronta = tutto vero tranne `fatto-changelog`, `fatto-versione`, `fatto-tag`; rilasciata = vero anche quelli. Non scrive niente; lo lancia `.github/workflows/milestone.yml` su main e di lunedì (testing) | `--json` · `--pronte` · `--check` · `--solo-integrita` · `--github` (confronta con le milestone di GitHub via `gh`) · `--registro` · `--radice` · `--timeout` (300 s) | `plans/milestone.json`, git, i comandi dei criteri | tabella per milestone con i criteri falsi; exit 0 con il registro integro (anche se niente è pronto), 2 se è rotto |
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
