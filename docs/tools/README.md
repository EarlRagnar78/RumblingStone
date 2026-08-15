<!-- AUTO-GENERATO da scripts/tools_manifest.py — non modificare a mano.
     Fonte: scripts/tools.manifest.json. Rigenera: python3 scripts/tools_manifest.py --emit-all -->

# Registro dei tool — RumblingStone

> Vista umana del contratto machine-readable [`registry.json`](registry.json). Fonte di verita': `scripts/tools.manifest.json`.

**41 tool** · convenzione exit code `0=ok · 1=errore-dominio · 2=errore-uso`.

## A · Session Prep (incontri · mappe · tesoro)

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `suggest_encounter.py` | Genera 3-5 proposte di incontro D&D 3.5 per un EL bersaglio, con calcolo CR combinato, per fazione/alleanza o 'wild'. | --el · --env · --factions · --alliance · --inject-npc · --wild · --seed · --list-all | ✔ | — | — | `0` · `2` · `3` · `4` |
| `suggest_loot.py` | Generatore di tesoro standalone (SRD 3.5) per EL/fazione, consuma l'output di suggest_encounter o flag diretti. | --el · --from-encounter · --factions · --pcs · --wild · --seed · --all-proposals | ✔ | — | — | `0` · `2` · `3` |
| `suggest_map.py` | Sceglie una griglia tattica ASCII (quadretti da 5 ft) da scripts/map_templates/*.yaml per ambiente/tipo. | --env · --type · --name · --list | ✔ | — | — | `0` · `2` · `3` · `4` |

## B · Maps Pipeline (render · import · export · validate)

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `compile_map_json.py` | Modalita' 3: compila un contratto JSON rigido in un master griglia-emoji, validando geometria e simboli e rigettando input errati. | spec · -o/--output · --validate-only | ✔ | — | — | `0` · `1` · `2` |
| `export_map_png.py` | Rasterizza un SVG renderizzato in PNG hi-res via Chromium headless (stampa, VTT, input hero-map ComfyUI). | **svg** · -o/--out · --scale · --browser | — | — | — | `0` · `1` |
| `export_uvtt.py` | Esporta un master griglia-emoji in file Universal VTT (.uvtt/.dd2vtt) con muri, porte e luci per import nativo in Foundry/Roll20. | file · -o/--output · --map · --ppg · --ext | ✔ | — | — | `0` · `1` · `2` |
| `import_ultraclear.py` | Modalita' 3 'al contrario': da mappa ultra-clear a bozza del contratto JSON + report conflitti figura vs tabella (regole R1-R12). | **input** · -o/--output · --json-report · --strict · --map | ✔ | — | — | `0` · `1` · `2` |
| `import_watabou.py` | Converte un export JSON di Watabou One Page Dungeon in un master griglia-emoji conforme al template. | **json_file** · -o/--out · --pad | ✔ | — | — | `0` · `1` |
| `render_map_svg.py` | Renderizza le griglie-emoji dei master mappa in SVG stampa-quality stile 'pergamena', deterministico e senza asset esterni. | **files** · -o/--outdir · --map · --list · --strict | ✔ | — | — | `0` · `1` |
| `validate_maps.py` | Gate CI: coerenza fra le griglie-emoji master e gli SVG renderizzati (i master sono la fonte, gli SVG artefatti). | --repo-root · --json | ✔ | — | — | `0` · `1` |

## C · Post-Session Canon (XP · state.md · branch)

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `campaign_branch.py` | Guardia e gestione del branch-per-gruppo campaign-group-<nome>: il canone vivo si scrive solo li' (ADR-0007). | **status|guard|ensure** · --group | ✔ | — | — | `0` · `1` · `2` |
| `next_session.py` | Aggregatore deterministico: brief DM (SOLO DM) + teaser player spoiler-safe per la prossima sessione. Non inventa nulla (AGENTS.md). | --last-n · --hype | ✔ | — | — | `0` · `1` |
| `session_wizard.py` | Wizard di fine sessione: Q&A con default -> session log canonico conforme al template, committato subito (ADR-0007). | --answers · --out · --no-commit | ✔ | ✔ | ✔ | `0` · `1` · `130` |
| `state_apply.py` | Applica il sottoinsieme meccanico delle proposte di state_sync SOLO nelle regioni marcate 'auto:' di state.md, con diff e conferma (ADR-0007). | --migrate · --session · --check · --yes · --commit | ✔ | ✔ | ✔ | `0` · `1` · `2` |
| `state_sync.py` | Propone (mai applica) diff a campaign/state.md dai trigger nei session log; report markdown per revisione DM. | --since · --session | ✔ | — | — | `0` · `2` |
| `update_xp.py` | Registro XP cumulativo per PG dai blocchi '## XP awarded' dei session log; scrive campaign/pg/xp-ledger.md. | --check | ✔ | — | — | `0` |

## D · Materiali giocatore / DM (Homebrewery V3)

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `build_booklet_html.py` | Booklet in stile 'pergamena Homebrewery' (stile canonico, ADR-0013) da manifest JSON di capitoli markdown: HTML autonomo (SVG inline, raster data-URI) e/o sorgente Homebrewery V3 .hb.md per il self-hosted/Docker; i .md restano i master (ADR-0003). | **manifest** · --out · --format | ✔ | — | — | `0` · `2` |
| `dm_dossier.py` | SOLO DM: fotografia di tutte le trame da state.md (sezioni 0-7) in veste Homebrewery V3, contenuto estratto alla lettera. | -o/--output | ✔ | — | — | `0` · `1` |
| `export_booklet_pdf.py` | PDF A4 delle schede di un booklet pergamena (ADR-0013): un PDF per pagina via Chromium/Chrome headless, resa identica al browser (CSS di stampa canonico). Default: solo pagine player (hint/echi/teaser). | **manifest** · --pane · --all · --list · --outdir · --browser | — | — | — | `0` · `1` · `2` |
| `extract_scene_prompts.py` | Estrae le scene illustrabili di un arco (read-aloud + copertura immagini) e genera lo scheletro del file dei prompt immagine (ADR-0015); rigenerazione idempotente che non perde le schede gia compilate. | **arc** · -o/--output · --list | ✔ | — | — | `0` · `1` · `2` |
| `hype_homebrew.py` | Impagina recap o handout in layout Homebrewery V3, senza mai duplicare il filtro spoiler di session_recap. | --recap · --pg · --handout · --da · --sezione | ✔ | — | — | `0` · `1` |
| `session_recap.py` | Recap italiano spoiler-safe (tono R.A. Salvatore) dagli ultimi N session log; taglia sempre le note private DM. | --last-n · --out · --pdf · --seed · --pg | ✔ | — | — | `0` · `1` |

## E · Bestiario / Catalogo mostri

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `build_monster_catalog.py` | Indicizza ogni statblocco del repo (Bestiario/, archi, STATBLOCCHI) in scripts/monster_catalog.yaml. | --check · -o/--output | ✔ | — | — | `0` · `1` |
| `validate_bestiario.py` | Gate CI della libreria Bestiario/: struttura, naming, header, CR filename-vs-header, catalogo in sync. Con --rules aggiunge warning PF1e non bloccanti. | --rules · --json | ✔ | — | — | `0` · `1` |

## F · Pipeline skill multi-agente

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `build-skills.sh` | Costruisce i pacchetti skill per-agente (compact.md/structured.yaml/machine.json) e li deploya in ~/.<agent>/skills/. | --no-deploy · --skill · --measure · --dry-run | ✔ | — | — | `0` · `1` |
| `compress_skills.py` | Comprime le skill per gli agenti (riduzione token), producendo compact.md/structured.yaml/machine.json. | **--input/-i** · **--output/-o** · --measure/-m | ✔ | — | — | `0` · `1` |
| `index_skills.py` | Genera index.json per una skill compressa (per retrieval selettivo). | **--input/-i** · **--build/-b** · **--output/-o** | ✔ | — | — | `0` · `2` |
| `measure_tokens.py` | Misura la dimensione in token delle skill (tiktoken se disponibile, altrimenti chars/4). | --tokenizer · --json | ✔ | — | — | `0` |
| `sync-skills.sh` | Build + popola i mirror in-repo delle skill (.claude/, .cursor/, ...), tutti gitignorati. | --dry-run · --no-build | ✔ | — | — | `0` · `1` |
| `validate_skills.py` | Gate CI skill: SKILL.md valido (frontmatter), link e dati YAML coerenti. | --repo-root · --json | ✔ | — | — | `0` · `1` · `2` |

## G · Orchestrazione & Governance

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `check_plans_discipline.py` | Gate ADR-0009: modifiche strutturali (scripts/, skills/, converters/, .github/, plans/adr/) senza riga in plans/CHANGELOG.md -> exit 1. | --base · --head · --json | ✔ | — | — | `0` · `1` |
| `dm.py` | Entrypoint unico: orchestra tutti gli script per fase del Playbook (prep/post/session/recap/handout/maps/hype/dossier/skills/doctor). ADR-0002. | **prep|post|session|recap|handout|maps|hype|dossier|skills|doctor** | ✔ | ✔ | ✔ | `0` · `1` · `2` |
| `install-git-hooks.sh` | Installa gli hook git locali: post-merge (resync mirror skill) e pre-push (gate ADR-0009). | — | ✔ | — | — | `0` · `1` |
| `new-campaign-group.sh` | Reset branch-per-gruppo: nuovo branch di campagna con stato azzerato dai template. | **new-group-name** · --backup-current | ✔ | ✔ | ✔ | `0` · `1` |
| `tools_manifest.py` | Fonte di verita' -> artefatti: valida scripts/tools.manifest.json contro lo schema, verifica la copertura degli script e genera registry.json, README.md e mcp-tools.json. | --check · --emit-all · --render-md · --emit-mcp | ✔ | — | — | `0` · `1` · `2` |
| `validate_modules.py` | Gate CI: verifica i master ARC*-DEF-* contro la checklist della skill rumblingstone-module-standard. | --verbose · --json | ✔ | — | — | `0` · `1` |
| `validate_standalone.py` | Gate CI per i moduli autoconclusivi STANDALONE-*: file obbligatori, riferimenti incrociati, schede pregenerate, termini 5e vietati, read-aloud minimi e contatori dichiarati. | --dir | ✔ | — | — | `0` · `1` |

## I · Convertitori di contenuto

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `Html_to_markdown` | Convertitore di contenuto HTML -> Markdown. Isolato dal toolkit DM. | — | — | — | — | `0` · `1` |
| `Image-to-webp` | Convertitore batch immagini -> WebP con archiviazione degli originali (cwebp). Isolato dal toolkit DM. | — | — | — | — | `0` · `1` |
| `pdf-to-md-engine` | Convertitore di contenuto PDF -> Markdown (toolchain esterna). Isolato dal toolkit DM. | — | — | — | — | `0` · `1` |

## Librerie (non-CLI)

| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |
|---|---|---|:--:|:--:|:--:|---|
| `dmcore` | Libreria condivisa ADR-0007: regions (marker auto:), gitio (guardia branch/commit), config (group.yaml), visibility (policy per-PG). Non e' un CLI. | — | ✔ | — | — | — |

---

Aggiungere un tool? Vedi [`../guides/TOOL-AUTHORING-STANDARD.md`](../guides/TOOL-AUTHORING-STANDARD.md).
