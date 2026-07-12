# PIANO DM-TOOLKIT — CLI unica · Hype Homebrewery · Archivio Piani

> **Versione**: v1 (2026-07-10) — nasce dalle 3 domande del DM:
> (1) *quali tool servono per preparare bene una sessione? sono sparsi,
> si possono consolidare in modo più organico?* (2) *si può usare
> <https://dungeons-and-pi.github.io/homebrewery-templates/> per dare un
> layout bello ai materiali di hype pre-sessione?* (3) *vale la pena una
> cartella-archivio dei piani eseguiti con % di completamento, passaggi
> futuri lasciati in bianco, changelog coerente e ADR?*
> **Scopo**: documento autocontenuto in stile
> `PIANO-REVISIONE-TRASVERSALE-...md` — ogni task ha evidenza, azione,
> criterio di accettazione e assegnazione engine (§6). **Nessun lotto è
> stato eseguito**: il DM approva questo piano sul PR, poi si parte.
> **Differenza dai piani-gemelli**: questo piano è **solo infrastruttura**
> (tool, layout, archivio) — non tocca il canone di gioco.

---

## §0 — REGOLE D'ORO (leggere prima di ogni lotto)

1. **Niente canone**: nessun task di questo piano modifica `campaign/state.md`
   §0-§7, sessioni, PNG o archi. Se un task scopre un'incoerenza di canone,
   la segnala al DM — non la corregge (appartiene ai piani REVISIONE).
2. **Design rules degli script esistenti** (da `scripts/README-automation.md`,
   vincolanti anche per i tool nuovi): Python 3 **stdlib only**, idempotenti,
   nessuna scrittura automatica su `state.md`/`sessions/*.md`, header
   "Auto-generated — do not edit by hand" sui file generati.
3. **Non cancellare file** (regola 5 del piano trasversale): gli spostamenti
   in `plans/` lasciano al vecchio percorso un **file-puntatore** di ~3 righe.
4. **Un lotto = un commit** descrittivo. Dopo ogni lotto: verifica del
   criterio di accettazione + aggiornamento della checklist §7 (con la %).
5. **Spoiler-safe**: ogni output destinato ai giocatori (recap-hype, handout,
   booklet) passa dallo stesso filtro di `session_recap.py` — le sezioni
   `## DM notes (private...)`, i clock dei villain e le Fasi non giocate
   **non entrano mai** nel materiale player-facing.
6. **Markdown è il MASTER, i layout sono artefatti** (stessa regola delle
   mappe SVG, T-D2): i file `.hb.md` per Homebrewery e gli eventuali PDF
   sono **generati**; si rigenerano, non si editano a mano.
7. **Priorità d'esecuzione proposta**: K-A (archivio, rischio zero) →
   K-C1 (CLI) → K-B1 (recap-hype) → K-B2 (handout) → K-C2/C3 (docs+CI) →
   K-B3 (booklet, a lotti). Il DM può riordinare in approvazione.

### Decisioni prese (K-D1…K-D4 — acquisite 2026-07-10, applicarle e non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| K-D1 | **CLI unica `scripts/dm.py`** a sottocomandi che orchestra gli script esistenti per fase (prep / tavolo / post / recap); gli script restano dove sono, zero rotture di path | DM 2026-07-10 (domanda 1) |
| K-D2 | **Hype Homebrewery in 3 ondate, in quest'ordine**: ① recap/hype pre-sessione → ② handout giocatori (lettere, profezie, schede artefatto, avvisi torneo) → ③ booklet per arco in stile modulo 3.5 (grosso, a lotti) | DM 2026-07-10 (domanda 2) |
| K-D3 | **Archivio piani = `plans/`** con `INDEX.md` (stato + % + lotti rimanenti + gate), `CHANGELOG.md` coerente, `adr/` per le decisioni architetturali; i `PIANO-*` esistenti si **spostano** lasciando puntatori | DM 2026-07-10 (domanda 3) |
| K-D4 | **Prima il piano scritto, poi l'esecuzione**: i lotti partono solo dopo approvazione DM di questo documento sul PR | DM 2026-07-10 (domanda 4) |
| K-D5 | **Homebrewery self-hosted in locale** (opzione B) per l'editor due-pannelli "stessa qualità": comandi SOLO dalla documentazione ufficiale naturalcrit, mai inventati → Lotto K-B4, ADR-0004. Chiude la domanda aperta Q2 | DM 2026-07-12 |

### Vincolo emerso in fase di stesura

- ⚠️ `dungeons-and-pi.github.io` è risultato **bloccato dalla network policy**
  dell'ambiente di stesura (proxy 403): il contenuto esatto del template pack
  è `[INFERRED — needs DM confirmation]`. Il gate **K-B0** chiede al DM di
  verificarlo (o di eseguire quel lotto in un ambiente con accesso).
  **Fallback già solido**: The Homebrewery (naturalcrit) è software **MIT,
  self-hostabile**, e i suoi *snippet* V3 nativi (front cover, note box,
  monster frame, `\page`, due colonne) bastano da soli per le ondate ①-②.

---

## §1 — AUDIT: lo stato attuale dei tool (risposta alla domanda "sono sparsi?")

**Sì, sono sparsi su due famiglie con nomi quasi identici** — è il difetto
principale, non la quantità (la copertura è già buona):

### Famiglia 1 — `scripts/` (minuscolo): automazione DM, 15+ tool

| Fase | Tool | Cosa fa |
|---|---|---|
| Prep | `build_monster_catalog.py` | indicizza ogni statblock del repo → `monster_catalog.yaml` |
| Prep | `suggest_encounter.py` | 3-5 proposte di incontro per EL target (env/fazione/ruolo) |
| Prep | `suggest_map.py` + `map_templates/` (11 YAML) | griglia tattica pronta da stampare |
| Prep | `suggest_loot.py` + `loot_tables.yaml` + `magic_items_srd.yaml` | proposte di bottino |
| Prep | `render_map_svg.py` | griglia emoji → SVG di qualità stampa (master = markdown) |
| Prep/CI | `validate_maps.py` | lint delle griglie (già in `ci.yml`) |
| Post | `update_xp.py` | ledger XP cumulativo per PG |
| Post | `state_sync.py` | propone (mai applica) diff a `state.md` dai trigger di sessione |
| Hype | `session_recap.py` | recap italiano spoiler-safe, tono R.A. Salvatore, `--pdf` |
| Reset | `new-campaign-group.sh` | branch-per-gruppo per rigiocare la campagna |
| Skill | `build-skills.sh`, `sync-skills.sh`, `compress/index/measure/validate` | pipeline skill multi-agente |

### Famiglia 2 — `Script/` (maiuscolo): convertitori di contenuto, 3 tool

| Tool | Cosa fa |
|---|---|
| `pdf-to-md-engine/` (+ `tools/md2pdf.sh`) | PDF → markdown (e ritorno md → PDF) |
| `Html_to_markdown/` | HTML → markdown |
| `Image-to-webp/` | immagini → webp |

### Lacune identificate (cosa manca per una prep di sessione "organica")

1. **Nessun punto d'ingresso unico**: il DM deve ricordare 8+ comandi e il
   loro ordine (il flusso esiste solo come prosa nel Playbook §2/§4).
2. **Collisione di nomi** `Script/` vs `scripts/` — confonde umani e agenti.
3. **Nessuna pipeline hype/layout**: `session_recap.py` produce md/PDF
   sobrio; non esiste l'output "trailer bello da mandare ai giocatori".
4. **Piani sparsi**: 4 `PIANO-*` tra root e 3 cartelle-arco, senza indice,
   senza % e senza changelog unificato (→ domanda 3 del DM, Lotto K-A).
5. *(minore)* `scripts/Old/` contiene 2 script superati senza banner.

**Verdetto**: non servono tool *nuovi* per la prep meccanica — serve
**orchestrazione** (K-C), **layout** (K-B) e **memoria dei piani** (K-A).

### Censimento piani esistenti (per l'INDEX di K-A2 — % verificate sulle checklist)

| Piano | Percorso attuale | Stato | % | Rimane (in bianco finché non giocato/deciso) |
|---|---|---|---|---|
| REVISIONE ARC-07 | `07_.../PIANO-REVISIONE-ARC07-...md` | 🟡 quasi completo | ~95% | B1 parziale: date/XP/loot **reali** dei log ricostruiti |
| REVISIONE ARC-08 | `08_.../PIANO-REVISIONE-ARC08-...md` | ✅ completo | 100% | — (arco ⬜ da giocare: il piano è chiuso, il gioco no) |
| REVISIONE ARC-09 | `09_.../PIANO-REVISIONE-ARC09-...md` | ✅ completo | 100% | — (idem) |
| REVISIONE TRASVERSALE | `PIANO-REVISIONE-TRASVERSALE-...md` | 🟡 gated dal tavolo | ~95% | T8 (gate: quest ARC-09 giocata) · T9 chiusura post-P3B · SVG dei 16 narrativi (opzionale). *T6c chiuso in sessione 11 (T-D10): censimento corretto in K-A* |
| DM-TOOLKIT (questo) | `plans/` | 🟡 in esecuzione | vedi §7 | vedi §7 |

---

## §2 — LOTTO K-A: Archivio piani `plans/` (P0 — rischio zero, engine: Sonnet 5)

### K-A1. Creazione `plans/` + spostamento con puntatori
- **Evidenza**: 4 piani in 4 posti diversi (§1); nessuna vista d'insieme.
- **Azione**: creare `plans/`; spostarci i 4 `PIANO-REVISIONE-*` + questo
  piano (nomi invariati). In ogni vecchio percorso lasciare un file-puntatore:
  ```markdown
  # ⚠️ SPOSTATO → plans/PIANO-REVISIONE-ARC07-COERENZA-E-QUALITA.md
  Questo piano vive nell'archivio piani. Indice: plans/INDEX.md
  ```
  `grep -rn` dei riferimenti ai vecchi path (README, AGENTS.md, piani
  gemelli, indici arco) e aggiornarli.
- **Accettazione**: `grep` dei vecchi path = solo file-puntatore; ogni piano
  raggiungibile sia dal vecchio percorso (via puntatore) sia da `plans/`.

### K-A2. `plans/INDEX.md` — la vista con le percentuali
- **Azione**: tabella = censimento §1 (piano · arco · stato · % · lotti
  rimanenti · **gate**), più una sezione per piano **"Prossimi passaggi"
  volutamente in bianco** (righe `- ⬜ _(da definire al tavolo / dal DM)_`)
  come richiesto dal DM. Regola di manutenzione in testa: *chi chiude un
  lotto aggiorna la riga* (stessa convenzione delle checklist §5 dei piani).
- **Accettazione**: le 5 righe ci sono; le % coincidono con le checklist dei
  rispettivi piani (verifica incrociata a campione).

### K-A3. `plans/CHANGELOG.md` — changelog coerente
- **Azione**: formato *Keep-a-Changelog adattato*: una riga per lotto chiuso
  (`data · piano · lotto · commit · esito`). Semina retroattiva dai commit
  `docs(plan): ...` / `docs(T5x): ...` già in history (`git log --oneline`),
  così la storia dei lotti 2026-07-02→07-04 non va persa. In avanti: la riga
  si aggiunge **nello stesso commit** che chiude il lotto (regola d'oro 4).
- **Accettazione**: ogni lotto ✅ dei 4 piani esistenti ha la sua riga; le
  date coincidono con le checklist.

### K-A4. `plans/adr/` — decisioni architetturali
- **Azione**: `ADR-0000-template.md` (Contesto/Decisione/Conseguenze/Stato) +
  3 ADR iniziali che canonizzano decisioni già prese:
  **ADR-0001** archivio piani con puntatori (K-D3, regola 3);
  **ADR-0002** CLI unica `dm.py` come orchestratore, mai come logica (K-D1);
  **ADR-0003** markdown master / layout generati — vale per SVG (T-D2) e
  per Homebrewery (regola 6).
- **Accettazione**: i 3 ADR citano la decisione-fonte (K-D*/T-D*) e la data.

---

## §3 — LOTTO K-B: Hype & layout Homebrewery (ordine DM: ①→②→③)

> **Cos'è Homebrewery**: renderer web (naturalcrit) che trasforma markdown
> "V3" in pagine in stile Manuale del Giocatore (due colonne, box note,
> cornici mostro, copertine). Licenza **MIT**, self-hostabile. Il flusso
> minimo è *copia-incolla* del markdown sul sito → condividi link o PDF.

### K-B0. Gate: verifica del template pack dungeons-and-pi 🔶
- **Evidenza**: sito bloccato dalla network policy in stesura (vedi §0);
  contenuti/licenza del pack non verificati di prima mano.
- **Azione (DM, 10 min)**: aprire il sito e rispondere a 3 domande:
  (a) i template sono markdown V3 incollabili? (b) licenza/attribuzione?
  (c) quali template piacciono per recap e handout? In alternativa:
  autorizzare il dominio nella network policy dell'ambiente e delegare
  la ricognizione all'engine.
- **Accettazione**: risposta del DM registrata qui come K-D5; se il pack
  non convince → si procede con gli snippet V3 nativi (fallback, §0).

### K-B1. Ondata ① — `scripts/hype_homebrew.py`: recap-hype pre-sessione
- **Evidenza**: `session_recap.py` produce già il recap giusto (spoiler-safe,
  tono Salvatore) ma in layout sobrio; il DM vuole il "trailer" bello.
- **Azione**: nuovo script stdlib-only che **riusa** il recap (import o
  lettura di `campaign/recaps/recap-*.md` — mai duplicare il filtro spoiler)
  e lo avvolge in markdown Homebrewery V3: copertina con titolo sessione e
  data, colonne, box-nota per "Nella prossima sessione..." (hook), eventuale
  immagine da `campaign/ai-media-prompts/` come art di copertina (path
  locale → il DM la carica sul brew). Output:
  `campaign/recaps/homebrew/recap-YYYY-MM-DD.hb.md` con header
  "Auto-generated". Uso: `dm.py recap --hype` (K-C1) o standalone.
- **Accettazione**: incollato su Homebrewery, il brew rende senza errori di
  sintassi V3; nessuna sezione DM-private presente (grep `DM notes` = 0);
  rigenerabile in modo deterministico.

### K-B2. Ondata ② — Handout giocatori
- **Evidenza**: gli handout esistono come contenuto (`ARC07-HANDOUTS.md`,
  schede `00_*-SCHEDA-GIOCATORE-STATO-ATTUALE.md`, avvisi torneo ARC-09) ma
  senza layout consegnabile al tavolo.
- **Azione**: `campaign/templates/homebrew/` con 4 template V3:
  `lettera.hb.md`, `profezia.hb.md`, `avviso-torneo.hb.md`,
  `scheda-artefatto-giocatore.hb.md` (quest'ultimo mappato sui campi delle
  schede STATO-ATTUALE, regola dei 3 documenti T-D3). Generatore:
  `dm.py handout --tipo lettera --da <file.md>` che riversa il contenuto nel
  template. Pilota: 1 handout reale per tipo, scelti dall'imminente (ARC-07
  P4 / P3B), sottoposti al DM prima di generarne in serie.
- **Accettazione**: 4 template + 4 piloti renderizzano su Homebrewery; le
  schede artefatto non introducono numeri nuovi (solo layout del master).

### K-B3. Ondata ③ — Booklet per arco (grosso, a lotti, dopo ①-②)
- **Evidenza**: gli archi hanno già indici (`ARC07-00-INDICE.md`) e
  companion in stile RHoD — la spina dorsale del booklet esiste.
- **Azione**: pilota su **ARC-07** (arco al tavolo): assemblare
  indice → parti → mappe (SVG) → companion → handout in un unico
  `.hb.md` per capitoli, un lotto per Parte (P1-P2, P3, P3B, P4, P5-P6).
  Solo materiale **già canone**; le Fasi non giocate restano fuori dalla
  versione condivisa coi giocatori (versione-DM separata).
- **Accettazione (per lotto)**: il capitolo rende su Homebrewery; zero
  divergenze dal master markdown (il booklet **cita**, non riscrive).
- **Nota dimensione**: Homebrewery soffre su brew molto lunghi → un brew
  per Parte, non per arco intero. Da riverificare al primo pilota.

### K-B4. Homebrewery self-hosted in locale (K-D5, aggiunto 2026-07-12)
- **Evidenza**: il DM vuole l'editor a due pannelli (markdown + anteprima
  PHB live) "con la stessa qualità" ma in casa propria; il sito pubblico
  ospiterebbe contenuto RHoD privato su server terzi (Q2 del piano).
- **Azione**: guida `scripts/homebrew-local/README.md` con i comandi
  **ripresi alla lettera dalla documentazione ufficiale** di
  naturalcrit/homebrewery (README.md *Installation* + README.DOCKER.md,
  recuperati 2026-07-12): via nativa (Node ≥16 + MongoDB + git →
  `git clone` → `NODE_ENV=local` → `npm install` → `npm start` →
  `http://localhost:8000`) e via Docker. Wrapper sottili `setup.sh` /
  `start.sh` + sottocomando `dm.py hype setup|start`; clone gitignorato.
  Razionale in **ADR-0004**.
- **Accettazione**: `bash -n` sui wrapper ok; `dm.py hype start` senza
  install → errore parlante che rimanda a `hype setup`; nessun comando
  d'installazione inventato (tutti tracciabili alle due fonti ufficiali);
  prova end-to-end sul PC del DM (Node/Mongo non installabili nel
  container di lavoro — network policy e ambiente effimero).

### K-B5. Container Docker chiavi-in-mano (richiesta DM 2026-07-12)
- **Evidenza**: il DM vuole "provare il container non appena deployato",
  con TUTTE le istruzioni per crearlo in locale.
- **Azione**: il repo ufficiale naturalcrit include `docker-compose.yml`
  con **entrambi** i servizi (mongodb + homebrewery, `MONGODB_URI`
  cablata) — verificato scaricando compose e Dockerfile il 2026-07-12.
  Quindi: `setup-docker.sh` (check Docker/Compose → clone → scrive
  `config/docker.json` col template ufficiale → `docker compose up -d
  --build`) e `stop-docker.sh`; sottocomandi `dm.py hype docker` /
  `docker-stop`; guida §Via B riscritta "da zero al container" (link
  ufficiali d'installazione Docker, gestione, log, update, note AVX/ARM).
- **Accettazione**: nel container di lavoro lo script arriva fino al
  confine del demone Docker (clone ✓, config ✓, invocazione compose ✓ —
  il demone non può girare qui); sul PC del DM `dm.py hype docker` deve
  portare a `http://localhost:8000` in un comando.

---

## §4 — LOTTO K-C: CLI unica `scripts/dm.py` (K-D1)

### K-C1. Lo scheletro a sottocomandi (engine: Opus 4.8)
- **Evidenza**: 8+ comandi da ricordare in ordine (lacuna 1, §1).
- **Azione**: `scripts/dm.py` stdlib-only (argparse + subprocess), **solo
  orchestrazione** (ADR-0002): zero logica duplicata dagli script.
  Sottocomandi mappati sulle fasi del Playbook:

  | Comando | Orchestra | Fase Playbook |
  |---|---|---|
  | `dm.py prep [--el N --env X ...]` | catalog refresh se stantio → suggest_encounter → suggest_map → suggest_loot | §2 pre-session |
  | `dm.py maps [render\|validate] [file]` | render_map_svg / validate_maps | prep |
  | `dm.py post [--session file]` | update_xp → state_sync → stampa checklist §4 del Playbook | §4 post-session |
  | `dm.py recap [--hype] [--pdf] [--last-n N]` | session_recap (+ hype_homebrew se `--hype`) | §4.6 |
  | `dm.py handout --tipo T --da file` | template homebrew (K-B2) | prep |
  | `dm.py skills [build\|sync]` | build-skills.sh / sync-skills.sh | manutenzione |
  | `dm.py doctor` | verifica python3, pandoc (opz.), catalogo fresco, path attesi | tutte |

- **Accettazione**: ogni sottocomando produce lo stesso output dello script
  sottostante lanciato a mano; `dm.py <cmd> --help` documenta la fase;
  gli script restano invocabili singolarmente (zero rotture).

### K-C2. Documentazione (engine: Sonnet 5)
- **Azione**: riscrivere `scripts/README-automation.md` attorno a `dm.py`
  (il "Typical DM workflow" diventa 3 righe); aggiornare Playbook §2 e §4
  coi comandi nuovi; riga in AGENTS.md; banner ⚠️ SUPERATO sui 2 file di
  `scripts/Old/` (lacuna 5). La collisione `Script/` vs `scripts/`
  (lacuna 2) si risolve **senza spostare nulla**: nota di disambiguazione
  in testa a entrambi i README (spostare i convertitori = rompere i loro
  README/DEPLOYMENT interni; non ne vale la pena ora — eventualmente ADR
  futuro).
- **Accettazione**: un DM nuovo arriva alla prep leggendo solo Playbook §2.

### K-C3. CI smoke test (engine: Sonnet 5)
- **Azione**: step in `.github/workflows/ci.yml`: `python3 scripts/dm.py
  --help` + `dm.py doctor --ci` (exit 0 senza pandoc/catalogo: in CI segnala,
  non fallisce).
- **Accettazione**: CI verde sul branch del lotto.

---

## §5 — Cosa NON si fa (e perché — anticipa obiezioni)

- **Niente fusione `Script/`+`scripts/`**: il DM ha scelto "CLI unica, script
  dove sono" (K-D1); la fusione toccherebbe decine di path interni per un
  beneficio estetico. Se in futuro servirà: ADR dedicato.
- **Niente battlemap raster da AI** nei brew: resta T-D2 (griglie emoji +
  SVG generati). Homebrewery impagina, non genera mappe.
- **Niente LLM negli script**: `session_recap.py` è deterministico per
  scelta di progetto; `hype_homebrew.py` eredita la scelta.
- **Niente auto-scrittura del canone**: `dm.py post` *propone* (state_sync),
  il DM applica — invariato.

## §6 — Assegnazione engine per lotto (convenzione T-D5)

| Lotto | Natura | Engine |
|---|---|---|
| K-A1…K-A4 | esecutivo/ripetitivo (spostamenti, indici, semina changelog) | **Sonnet 5** |
| K-B1 | generativo con vincoli (script + layout) | **Opus 4.8** |
| K-B2 | generativo (template + piloti) | **Opus 4.8** |
| K-B3 | assemblaggio a lotti su canone esistente | **Opus 4.8** (Sonnet 5 per i capitoli ripetitivi) |
| K-C1 | design CLI | **Opus 4.8** |
| K-C2, K-C3 | esecutivo (docs, CI) | **Sonnet 5** |
| Arbitrati di canone | non previsti da questo piano | — (🔶 Fable solo se emergono) |

## §7 — Checklist avanzamento (aggiornare a ogni lotto — regola d'oro 4)

**Completamento piano: 100% — PIANO COMPLETO (2026-07-12).** Code da
tavolo fuori conteggio: verifica visiva dei brew al collaudo del
container; 2 piloti handout (lettera/avviso-torneo) in attesa di testo
canone dal DM. (Piano approvato col merge del PR #28, 2026-07-10.)

- [x] **K-A** (archivio piani): [x] K-A1 · [x] K-A2 · [x] K-A3 · [x] K-A4 — **4/4 — LOTTO COMPLETO (2026-07-10)**
- [x] **K-B** (hype Homebrewery): [x] K-B0 (2026-07-12: chiuso col **default dichiarato** — snippet V3 nativi; sito del pack inaccessibile dall'ambiente e mandato DM "completa tutto"; riapribile come lotto estetico se il DM indicherà template specifici) · [x] K-B1 (2026-07-10) · [x] K-B2 (2026-07-10; piloti canone: profezia Cronache + scheda Collana; piloti lettera/avviso-torneo in attesa di testo canone dal DM) · [x] K-B3 (2026-07-12: **Fascicoli I-V completi** — P1-P2, P3, P4+Viaggio, P3B, P5+ponte; verifica visiva su Homebrewery in carico al DM al collaudo del container) · [x] K-B4 (2026-07-12, K-D5) · [x] K-B5 (2026-07-12, container turnkey) — **6/6 — LOTTO COMPLETO**
- [x] **K-C** (CLI dm.py): [x] K-C1 (2026-07-10) · [x] K-C2 (2026-07-10) · [x] K-C3 (2026-07-10) — **3/3 — LOTTO COMPLETO**
- [x] K-D1…K-D5 — decisioni acquisite (2026-07-10/12)
- [x] **K-B6** *(manutenzione post-collaudo, 2026-07-12)*: primo feedback
  DM sul recap recepito — clock/villain → voci vaghe (Conoscenze locali),
  mai numeri/deadline ai giocatori; tabella archi = solo cammino vissuto,
  futuri → sussurri §V; **Giorno di Marcia** in testata (ancora Harptos
  configurabile: `MARCH_DAY1_HARPTOS` in session_recap.py) e cronologia
  handout auto-generata `campaign/recaps/homebrew/00-CRONOLOGIA.hb.md`
- [x] **K-B7** *(manutenzione post-collaudo, 2026-07-12)*: **Dossier del DM**
  (`dm.py dossier` → `campaign/DM-DOSSIER.hb.md`, SOLO DM: tutti i fili da
  state.md con cornici stile RHoD) + ancora Harptos fissata a **1 Mirtul
  1372** → **AGGIORNATA in K-B8 (2026-07-12): 1 Flamerule 1372**, DM ha
  confermato la piena estate nella Valle di Channath (house-rules aveva
  ragione; state.md corretto con changelog §8 — [INFERRED] risolto)

### Domande aperte per il DM (da chiudere in approvazione del PR)

| # | Domanda | Default se non risponde |
|---|---|---|
| Q1 | ~~Template pack dungeons-and-pi (K-B0)~~ **CHIUSA (2026-07-12): applicato il default — snippet V3 nativi** (sito inaccessibile dall'ambiente; riapribile come rifinitura estetica) | — |
| Q2 | ~~Flusso Homebrewery: copia-incolla o self-host?~~ **CHIUSA → K-D5 (2026-07-12): self-host locale, Lotto K-B4, ADR-0004** | — |
| Q3 | Lingua dei materiali player-facing: italiano come i recap? | italiano |
| Q4 | Ordine lotti proposto in §0.7: confermato? | confermato |
