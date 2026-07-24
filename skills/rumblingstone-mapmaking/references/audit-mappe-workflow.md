# Audit & consolidamento mappe di un arco — workflow codificato

> **Perché esiste**: codifica il lavoro fatto sull'ARC-07 (2026-07-23, PR #61)
> così ogni agente lo ripete con la stessa precisione **senza rifarlo a mano**:
> audit → fonti canoniche → atlante definitivo con add-on DM → contratto di
> fedeltà → render → verifica visiva. Usalo per QUALSIASI richiesta del tipo
> «audit delle mappe dell'arco X», «atlante mappe definitivo», «rigenera le
> mappe alla qualità migliore», «passata di parità mappe».

---

## STEP 1 — Censimento (prima di scrivere qualunque griglia)

1. Trova TUTTE le griglie esistenti del perimetro: nei master dell'arco
   (`ARC*-DEF-*`), in `<arco>/Mappe/*.md`, nelle cartelle `Immagini/`, e nelle
   **generazioni storiche** (file deprecati/`_ARCHIVIO/` — spesso la mappa
   GIOCATA è lì).
2. Identifica il **gold standard interno**: il documento-mappe più ricco del
   repo per struttura e dettaglio (oggi: `08_.../Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
   — matrice di contenuto + add-on tattici per mappa; e i `*-REVISED-UltraClear.md`).
   Confronta per righe/sezioni, non a sensazione.
3. Benchmark esterno di dettaglio: le battle map RHoD
   (`00_Red Hand Of Doom/Immagini/Area Map/…/MappeIncontri/*.webp`) — griglia
   + indicazioni DM per posizioni, ambiente e tattiche di PNG/villain/mostri.
   Sono un **riferimento visivo**, MAI un input da auto-convertire (non esiste
   estrazione affidabile layout/asset da raster — verdetto in
   `plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md §2`).

## STEP 2 — Fonti canoniche: la regola d'oro dei posizionamenti

⚠️ **La geometria GIOCATA è canone.** Se una stanza/scena è già stata giocata
(anche in un arco precedente), la mappa dell'incontro originale è la fonte:
- **NON inventare** geometrie nuove (dais, pilastri, dimensioni) per una stanza
  che ha già una mappa giocata: **eleva la qualità SENZA spostare nulla**.
- Cerca la fonte in `06_*/`, `08_*/` ecc. (`Tactics_and_maps.md`, `maps.md`,
  atlanti d'arco) e **chiedi al DM** se hai due candidate.
- Se il file-fonte è marcato DEPRECATED con un master vivo indicato in testa,
  usa il **master vivo** (di norma ha scala/dettagli in più) e cita entrambi.
- Registra la fonte nella **matrice di contenuto** dell'atlante
  (colonna «Master (fonte griglia)»).
- Errori REALI già commessi e corretti (non ripeterli): dais +1,5 m inventato
  nella Stanza della Corona (la fonte ARC-06 non lo ha); header `24 m × 16
  righe` su una griglia da 10 righe; griglia T-6 «compressa» nell'atlante
  mentre il master l'aveva piena.

## STEP 3 — L'Atlante di arco (il documento definitivo delle mappe)

Un file per arco: `<arco>/Mappe/ARC<NN>-MAPPE-DEFINITIVO.md`. Struttura:
1. **Header**: standard adottato, decisione ASCII-master, stato rese SVG.
2. **📖 Matrice di contenuto**: mappa → beat → fonte griglia → tipo → stato.
3. **📑 Indice** per master/beat.
4. **Per OGNI mappa**, griglia ultra-clear + add-on DM in quest'ordine:
   - **Tipo / scala** (tattica/strategica/scenica; dimensioni; scala);
   - **Terreno & altitudini** (quote, coperture, hazard, gravità/luce);
   - **Posizioni** di PG / PNG / villain (coordinate lettera+numero);
   - **Tattiche PG** (come si vince, Shine Time, contro-momenti);
   - **Tattiche nemico round-per-round** (soglie pf, morale, ondate — stile
     RHoD, dal punto di vista del nemico);
   - **Evoluzione** (come cambia la scena: crolli, ondate, climax);
   - **Riferimento** (sezioni § del master).
5. Le griglie dell'atlante e quelle embedded nei master **devono essere
   identiche** (l'atlante aggiunge gli add-on). Ogni master punta all'atlante
   dalla sua sezione MAPPE; l'INDICE d'arco e i **booklet homebrew** citano
   l'atlante (così le mappe entrano nella generazione dei fascicoli).

## STEP 4 — Contratto di fedeltà (golden rule 6 di SKILL.md)

- Header griglia: `NOME — L m × H m (N col × M righe · S m)` — il validatore
  confronta con le celle lette (`render_map_svg.py --strict`): **la griglia è
  la verità**, correggi l'header, mai le posizioni.
- Annotazioni a lato-riga: dopo **≥3 spazi** (o `│` staccato ≥2 spazi); possono
  contenere emoji senza diventare celle fantasma.
- Riga `LEGENDA · 🧲 descrizione · …` in-fence: i simboli locali ereditano la
  descrizione nella legenda SVG. I simboli **universali** (SYMBOLS) tengono il
  testo canonico: se un universale è semanticamente sbagliato per l'uso locale
  (es. 🕳️ «voragine» usato per un'alcova) **cambia simbolo**, non la legenda.
- Righe elencate in ordine **decrescente** (nord = riga alta del documento):
  aggiungi `@north S` così la bussola del render è coerente.
- Scala ≠ 1,5 m: dichiarala nell'header (`· 3 m`) con nota A4 — il render la
  onora; non ridisegnare mappe canoniche per cambiare scala.
- Mappe **schematiche** (sezioni, esagoni, viste strategiche, diagrammi):
  `<!-- render: none -->` prima del fence; restano solo-ASCII per scelta.
- Geometrie complesse (cerchi, anelli, raggi in metri): **genera la griglia via
  script Python** (scratchpad), non a mano — i cerchi a mano sbagliano.

## STEP 5 — Render & verifica (il loop che NON si salta)

```bash
python3 scripts/render_map_svg.py "<atlante>.md" --list --strict  # dims check
python3 scripts/render_map_svg.py "<atlante>.md" --strict         # SVG
python3 scripts/export_map_png.py "<rendered>.svg"                # PNG locale
# → ISPEZIONE VISIVA del PNG (obbligatoria: leggi l'immagine, confronta i
#   token con la griglia ASCII cella per cella — è così che si trovano le
#   celle fantasma e le scale sbagliate)
python3 scripts/validate_maps.py                                  # byte-identity
python3 scripts/build_monster_catalog.py                          # sync catalogo
```
I PNG sono artefatti locali (non committarli); gli SVG in `rendered/` SÌ.

## STEP 6 — Tracciatura

Riga in `plans/CHANGELOG.md` (gate ADR-0009); `campaign/state.md §8` SOLO se
cambia canone (geometrie/posizioni canonizzate); INDICE d'arco aggiornato.

---

## Tool esterni valutati (2026-07) — verdetto onesto

| Categoria | Esempi | Verdetto per QUESTO repo |
|---|---|---|
| Generatori AI di battle map | CharGen, Dungeon Alchemist, BattleForge, Dungeon Map Builder | Producono **arte raster** generica: non sanno nulla di posizioni canoniche giocate, add-on DM, tattiche 3.5. Utili al più come *hero map* estetica — ruolo già coperto (meglio, IP-safe) dal pass ComfyUI locale opzionale |
| MCP server Foundry VTT | `adambdooley/foundry-vtt-mcp` (Foundry MCP Bridge), `laurigates/foundryvtt-mcp` | **L'unica integrazione sensata**: parlano col mondo Foundry (scene, actor, journal). Interessante SOLO se il DM adotta Foundry al tavolo — il repo esporta già `.uvtt` (`export_uvtt.py`), quindi il ponte c'è senza dipendenze nuove. Non fanno rendering né add-on |
| Moduli procedurali Foundry | `slaguru666/mapwright` (BSP→muri→SVG) | Buon generatore di *layout nuovi casuali* — inutile per mappe **canoniche** già giocate, che è il nostro caso d'uso principale |
| Skill D&D per Claude Code | «D&D Dungeon Master», «Mimir DM», `claude-dnd-skill`, marketplace SkillsMP | Tutte **5e-centric** e generiche: regole 5e (vietate qui), nessuna nozione del canone RumblingStone. Le skill interne del repo sono più specifiche e già a mirror per tutti gli agenti |

**Conclusione**: nessun tool community sostituisce questo workflow — il valore
(posizioni canoniche, tattiche, add-on DM) è **contenuto di campagna**, non
tecnologia. La pipeline interna (griglia emoji → renderer pergamena → UVTT) +
questa reference SONO lo strumento. Riesaminare solo se il DM adotta Foundry
(→ valutare Foundry MCP Bridge come connettore di sessione).
