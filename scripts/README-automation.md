# RumblingStone — DM automation scripts

Zero-burden helpers that read what the DM already writes (session logs,
state.md, Armate atlas) and produce prep material. **Nothing overwrites
canon** — scripts either generate new files or print suggestions for
manual review. Respects `AGENTS.md`: we never invent statblocks; we only
index/compose what exists (or mark `[INFERRED]`).

> **Disambiguazione**: questa cartella `scripts/` (minuscolo) è
> l'automazione DM. La cartella `Script/` (maiuscolo) contiene invece i
> convertitori di contenuto (pdf→md, html→md, immagini→webp) — vedi
> ADR-0002 in `plans/adr/`.

## One entrypoint: `dm.py`

Everything below is reachable from a single CLI mapped to the Playbook
phases (it *orchestrates* the scripts — they all remain usable directly):

```bash
python3 scripts/dm.py prep --el 13 --env forest   # encounter + map + loot
python3 scripts/dm.py post                        # XP ledger + state.md diff proposal
python3 scripts/dm.py recap --hype                # player recap + Homebrewery V3 version
python3 scripts/dm.py handout --tipo profezia --da <file> --sezione "HANDOUT 1"
python3 scripts/dm.py maps validate               # or: maps render <file.md>
python3 scripts/dm.py dossier                     # ⚠️ SOLO DM: dossier trame → DM-DOSSIER.hb.md
python3 scripts/dm.py hype setup && dm.py hype start   # Homebrewery locale (localhost:8000)
python3 scripts/dm.py skills build --no-deploy    # rebuild pacchetti skill multi-agente
python3 scripts/dm.py doctor                      # environment diagnosis
```

**Sottocomandi `dm.py`** (ognuno inoltra i flag allo script sottostante):

| Sottocomando | Flag | Fa girare | Fase Playbook |
|---|---|---|---|
| `prep` | `--el N` · `--env <amb>` · `--refresh` (rigenera il catalogo) | `suggest_encounter` + `suggest_map` + `suggest_loot` | §2 pre-sessione |
| `maps` | `render`\|`validate` + `files...` | `render_map_svg` / `validate_maps` | prep |
| `post` | `--session <file>` | `update_xp` + `state_sync` | §4 post-sessione |
| `session` | `end`\|`next`\|`status`\|`branch` · `--session <file>` · `--yes` · `--last-n N` · `--hype` · `--group <nome>` | `campaign_branch` + `update_xp` + `state_apply` / `next_session` | §4 + §7 (branch-per-gruppo, ADR-0007) |
| `recap` | `--last-n N` · `--pdf` · `--hype` | `session_recap` (+ `hype_homebrew`) | §4.6 |
| `handout` | `--tipo T` (obbl.) · `--da <file>` · `--out <file>` | `hype_homebrew --handout` | prep |
| `hype` | `setup`\|`start`\|`docker`\|`docker-stop` | wrapper `homebrew-local/*.sh` | prep |
| `dossier` | *(nessuno)* | `dm_dossier` | §4 (solo DM) |
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
| `export_map_png.py` | Rasterizza un SVG renderizzato in PNG hi-res (stampa, VTT, input per la passata ComfyUI "hero map") via Chromium/Chrome locale | *svg* · `-o <file.png>` · `--scale F` (default 2.0) · `--browser <bin>` | `rendered/*.svg` | PNG locale (gitignorato — mai committato) |
| `validate_maps.py` | Gate CI: coerenza griglie-emoji ↔ SVG renderizzati | `--repo-root <dir>` (default `.`) | markdown `*MAPPE*` + `rendered/*.svg` | exit 0/1 (gira in `.github/workflows/ci.yml`) |

### Post-sessione (canone: XP · state.md)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `update_xp.py` | Registro XP cumulativo per PG | `--check` (mostra il diff, non scrive) | `campaign/sessions/*.md` `## XP awarded` | `campaign/pg/xp-ledger.md` (auto) |
| `state_sync.py` | Propone modifiche a `campaign/state.md` dopo una sessione | `--since YYYY-MM-DD` · `--session <file>` | `## World events triggered` nei log | report diff markdown (il DM applica a mano) |
| `state_apply.py` | **Applica** il sottoinsieme meccanico delle proposte (March Clock, changelog §8) SOLO dentro le regioni marcate `auto:` di state.md, con diff e conferma per blocco (ADR-0007) | `--migrate` (inserisce i marker, idempotente) · `--session <file>` · `--check` · `--yes` · `--commit` | proposte di `state_sync` + regioni `auto:` | `campaign/state.md` aggiornato (su conferma; commit dedicato) |
| `next_session.py` | Brief DM + teaser player per la prossima sessione (aggregatore deterministico: hook aperti, finestre §0 vs March Day, party §1, clock villain ≤2 tick) | `--last-n N` · `--hype` (vesti Homebrewery) | `state.md` + `sessions/*.md` | `campaign/next/brief-*-DM.md` (⚠️ SOLO DM) · `teaser-*-PLAYERS.md` (spoiler-safe) · `next/homebrew/*.hb.md` |
| `campaign_branch.py` | Guardia e gestione del branch-per-gruppo (mai canone su `main`) | `status` · `guard` · `ensure [--group <nome>]` | `campaign/group.yaml` + git | branch `campaign-group-<nome>` attivo / exit code per la guardia |

### Materiali giocatore / DM (Homebrewery V3)

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `session_recap.py` | Recap italiano spoiler-safe (tono R.A. Salvatore) | `--last-n N` (default 1) · `--out <file>` · `--pdf` · `--seed N` | ultimi N log + righe pubbliche di state.md §0 | `campaign/recaps/recap-YYYY-MM-DD.md` (+ PDF opz.) |
| `hype_homebrew.py` | Impagina recap o handout in layout Homebrewery V3 | `--recap <file>` (default: l'ultimo) · `--handout TIPO` · `--da <file>` · `--sezione <str>` · `--out <file>` · `--cronologia` | recap/handout + `campaign/templates/homebrew/*.hb.md` | `.hb.md` da incollare su homebrewery.naturalcrit.com |
| `dm_dossier.py` | ⚠️ **SOLO DM**: fotografia di tutte le trame da state.md (§0-§7) con cornici stile RHoD, banner SOLO DM | *(nessuno)* | `campaign/state.md` | `campaign/DM-DOSSIER.hb.md` |

### Bestiario / catalogo mostri

| Script | Scopo | Parametri | Input | Output |
|---|---|---|---|---|
| `build_monster_catalog.py` | Indicizza ogni statblocco del repo | *(nessuno)* | `Bestiario/` (mostri/villain/png/pregen-pcgen), `*STATBLOCCHI*.md`, cartelle archi | `scripts/monster_catalog.yaml` (+ `monster_catalog.custom.yaml` vuoto per aggiunte DM) |
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
| `dmcore/` (libreria) | Logica condivisa dei flussi ADR-0007: `regions` (marker `auto:` con contratto "fuori byte-identici"), `gitio` (guardia branch, commit), `config` (group.yaml) | *(non è un CLI — la importano gli script sopra)* | — | — |
| `tests/` | Suite unittest dei flussi ADR-0007 (regioni, apply, guardia, next) su repo git temporanei | `python3 -m unittest discover -s scripts/tests` | fixture in-memory | verde/rosso (gira anche in CI) |

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
  of `scripts/state_sync.py`.

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
