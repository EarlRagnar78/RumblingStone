# PIANO — La piattaforma di sviluppo: una versione stabile, componenti misurati

> **Stato**: 🟡 in corso (2026-10-23), P0 e P9 fatti, D1-D6 decise il giorno stesso · **Classe**: G per la regola, C per i lotti
> **Nasce da**: tre messaggi del DM del 2026-10-23 (citati in
> [ADR-0099](adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)): una
> versione sola di Python, stabile e supportata, scelta come Debian sceglie il
> kernel; librerie e strumenti standard de facto solo se migliorano il
> progetto, con la misura; la stessa regola per tutti gli strumenti, la CI, i
> test, le skill e le pipeline (mappe, prosa, struttura), con un meccanismo di
> selezione e migrazione come quello di Debian.
> **Decisione**: [ADR-0099](adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md), accettata (D1).
> **Misure**: [plans/esperimenti/piattaforma-2026-10-23/MISURE.md](esperimenti/piattaforma-2026-10-23/MISURE.md).
>
> **In breve**: la piattaforma c'è quasi tutta (CI come standard, `binari.py`,
> Python 3.13, Dependabot, pytest). Manca la regola per far entrare, salire,
> aggiornare e uscire un componente. ADR-0099 la dà con tre canali (unstable,
> testing, stable) e criteri numerici. Questo piano la applica a ogni
> componente del repo, comincia da ruff in testing e porta al DM quattro
> scelte misurate, la più grossa delle quali toglie 222 secondi su 914 alla CI.

---

## §1 · Cosa c'è già, e cosa questo piano non rifà

| Già nel repo | Cosa copre | Qui |
|---|---|---|
| [ADR-0081](adr/ADR-0081-il-contratto-d-ambiente.md) e [PIANO-AMBIENTE-RIPRODUCIBILE](PIANO-AMBIENTE-RIPRODUCIBILE.md) | la macchina combacia con la CI: registro con versione e checksum (A1), Python 3.13 e tre piattaforme (A2), lock con hash (A3), hook (A4), `dm.py ambiente` (A5) | **non si rifà**. ADR-0099 aggiunge i canali sopra il contratto. Il test «una Python sola» è il resto di A2, il lock è A3: questo piano li usa e non li duplica |
| [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md) | ciò che il DM esegue resta stdlib più tre eccezioni | vincolo: uno strumento di sviluppo può entrare, una dipendenza del DM no senza un emendamento |
| [PIANO-PRATICHE-DI-INGEGNERIA](PIANO-PRATICHE-DI-INGEGNERIA.md) | Dependabot a gruppi, `pip-audit`, `converters/` fuori (D9) | si tiene, tranne `converters/`, che entra con D6 di questo piano (P9) |
| ADR-0084, 0085, 0086 | le misure con cui tcod, scipy, fonttools, torch e piq sono entrati | sono le promozioni fatte prima della regola: restano valide |
| PR #264 e #270 | spaCy e Stanza per la prosa, in esperimenti | in unstable: non si toccano le loro dipendenze; il thread della #264 è avvisato |

## §2 · Il censimento: ogni componente e il suo canale

Il canale proposto è quello che i fatti di oggi dicono. «stable» vuol dire
bloccante in CI con la versione fissata; dove la versione non è fissata, la
colonna lo dice e il lotto che la fissa è A1 o A3 di AMBIENTE.

### Interprete, CI, contenitori

| Componente | Versione oggi | Fissata? | Chi lo usa | Canale proposto |
|---|---|---|---|---|
| Python | 3.13 (CI, Docker, `binari.py`) | sì in CI; `PYTHON_MINIMO` è un minimo | tutto | **stable** (3.13 fino a Debian 14) |
| runner `ubuntu-24.04` | 24.04 | sì | CI | **stable**; 26.04 con una PR (D8 di AMBIENTE) |
| `actions/checkout`, `setup-python`, `upload-artifact` | v7 | per versione maggiore, non per SHA | CI | **stable** |
| immagine `debian:13-slim` | per digest | sì | `booklet-container` | **stable** |
| Dependabot | 3 ecosistemi, a gruppi | — | aggiornamenti | **stable** |

### Strumenti di sviluppo e test

| Componente | Versione | Fissata? | Misura | Canale proposto |
|---|---|---|---|---|
| pytest | ≥ 9.1.1 | pavimento | corridore dei test | **stable** |
| unittest (secondo corridore) | stdlib | — | 222 s su 914 per rieseguire gli stessi test | stable, **da togliere** come esecuzione completa (D2) |
| pip-audit | ≥ 2.10.1 | pavimento | CVE nelle dipendenze | **testing** (non bloccante dal 2026-09-24, non è mai salito) |
| shellcheck | del runner | no | 4 avvisi in 2 file (audit AMBIENTE) | **testing** (`|| true`); stable con A6 di AMBIENTE |
| `compileall` | stdlib | — | solo errori di sintassi | **stable**; ruff lo copre e lo supera (§3) |
| ruff | 0.16.9 | no | 0,08 s; 3 bug veri in `converters/`, 0 in `scripts/` | **testing** da questa PR (D5) |
| pytest-xdist | — | — | suite 219 s → 67 s su 4 core | unstable → testing se D3 |
| uv | 0.11.32 | — | installazione 33 s → 4 s a freddo, 21 s → 0,2 s a caldo | unstable → testing se D4 |
| mypy | 2.3.1 | — | 328 rilievi, 0 bug nel campione di 41 | **unstable**, non si adotta |
| pyright | — | — | non misurato | unstable |
| pre-commit (framework) | — | — | non misurato; A4 ha già deciso hook senza dipendenze | **non si adotta** |
| riscontro SRD (`riscontro_srd.py` con l'SRD 3.5 e il PRD PF1e in cache, OGL 1.0a) | commit fissati, sha256 per file | sì | 53 regole di ARC-08 in 0,25 s, 3 discordanze vere (RISCONTRO-ARC08) | **testing** da questa PR (P11, ADR-0103) |

### Librerie Python

| Libreria | Versione | Chi la usa | Canale |
|---|---|---|---|
| pyyaml | ≥ 6.0.3 | stato di campagna, skill (obbligatoria per il DM) | **stable** |
| Pillow | ≥ 13.0.0 | immagini dei booklet | **stable** |
| tiktoken | ≥ 0.14.0 | conteggio dei token delle skill | **stable** |
| pymupdf (AGPL, solo verifica) | ≥ 1.28.2 | misura dei PDF stampati | **stable** |
| tcod, numpy | ≥ 21.2.1, ≥ 2.5.3 | collaudo delle mappe | **stable** |
| scipy | ≥ 1.18.1 | collaudo delle mappe | **stable** |
| scikit-image | ≥ 0.25 | resa delle mappe | **stable** |
| fonttools | ≥ 4.66.1 | font delle mappe | **stable** |
| shapely | = 2.2.0 | piante delle città, `scripts/piante/` (ADR-0102) | **testing** dal 2026-10-23 |
| bpy, torch, piq | `requirements-completo.txt` | 3D e seconda misura della resa, fuori CI | **testing** locale (non girano in CI: ADR-0084) |
| spaCy, Stanza | — | `misura_sintassi` (PR #264, #270) | **unstable** |
| `import fitz` di pymupdf | — | deprecato: pymupdf avvisa che sparirà | da migrare a `import pymupdf` prima che salga la versione maggiore |

### Binari e servizi locali

| Componente | Versione | Fissata? | Pipeline | Canale |
|---|---|---|---|---|
| typst | 0.15.1 | in `ci.yml`, non nel registro | edizione da stampa | **stable**; nel registro con A1 |
| pdfcpu | 0.11.0 in locale | no, e non in CI | libretto imposto | **testing** (non provato in CI) |
| Chromium | del sistema | no | PDF dei booklet, PNG delle mappe | **testing** finché non c'è Chrome for Testing fissato (D10 di AMBIENTE) |
| pandoc, xelatex | — | no | recap in PDF | **unstable** (catena non pronta) |
| LanguageTool, java, mvn | — | no | secondo lettore della prosa | **unstable** (facoltativo) |
| Blender | di sistema | no | render 3D, tessere degli oggetti | **unstable** fuori CI; il piano di scena è stdlib e stable |
| ComfyUI, distrobox | — | no | immagini | **unstable** fuori CI |
| LLM locale per la prosa | gemma4 bocciato | — | ADR-0089, PR #234 | **unstable** |

### Le pipeline

Ogni pipeline usa i componenti sopra. Una pipeline è stable quando lo sono
tutti i componenti che la fanno passare in CI.

| Pipeline | Componenti di terzi | Stato |
|---|---|---|
| sessione (`dm.py`, stato, recap) | Python, pyyaml | stable |
| booklet HTML e PDF | Python, Pillow, Chromium | stable in HTML, testing in PDF |
| edizione da stampa e corredo | typst, pymupdf | stable |
| libretto imposto | typst, pdfcpu | testing |
| mappe: SVG, contratto JSON, UVTT | Python | stable |
| mappe: collaudo, qualità, resa | tcod, numpy, scipy, scikit-image | stable |
| mappe: piante delle città | shapely, numpy, scipy | testing |
| mappe: 3D e immagini | Blender, ComfyUI, torch, piq | unstable |
| prosa: lingua, MQM, foglio di stile | Python | stable |
| prosa: sintassi | spaCy, Stanza | unstable |
| bestiario e statblocchi | Python, pyyaml | stable |
| skill: build, validazione, scanner | Python, pyyaml, tiktoken, bash | stable |
| piani e documenti | Python, git | stable |
| server MCP | Python | stable |
| `converters/` | PyMuPDF, docling, torch, EasyOCR, magika | **testing** dal 2026-10-23 (D6, P9): Python 3.13, ruff, Dependabot, import di ogni modulo in CI |

## §3 · Lotti

Ogni lotto ha un ramo e una PR sua.

### P0 · Audit, misure, regola ✅
`[engine: Opus 5.5 · effort: alto · qualità: ogni numero ha il comando o la fonte; nessun canale assegnato senza un fatto]`
Questo documento, [MISURE](esperimenti/piattaforma-2026-10-23/MISURE.md),
ADR-0099. ruff in testing con otto gruppi di regole che cercano bug
(`ruff.toml`), passo non bloccante in CI. I 18 rilievi di `scripts/` letti uno
per uno: 13 annotazioni senza import corrette in `dmcore/testo.py`; in
`import_ultraclear.py` una variabile morta tolta e un `re.split` con
`maxsplit` posizionale, deprecato in 3.13, corretto (120 avvisi in meno nei
test); gli altri tre lasciati, con la ragione, in due righe di `ruff.toml`.

### P1 · Il canale sta nel registro ⬜
`[engine: Sonnet 5.5 · effort: medio · qualità: un test boccia se un pacchetto dei requirements o un passo CI non ha una voce nel registro col canale]`
- `binari.py` prende il campo `canale` (`unstable`, `testing`, `stable`) e la
  data di ingresso nel canale, per binari, librerie e strumenti di sviluppo.
  Non un file nuovo: ADR-0081 vuole una dichiarazione sola.
- `python3 scripts/binari.py --canali` stampa la tabella di §2, che da quel
  momento si genera e non si scrive a mano.
- Un test: ogni riga di `requirements*.txt` ha una voce, ogni voce stable ha la
  versione fissata, nessun passo CI bloccante usa un componente testing.

### P2 · La misura della piattaforma diventa un comando ⬜
`[engine: Sonnet 5.5 · effort: medio · qualità: il comando rifà la tabella di MISURE §4 da un run qualsiasi; due esecuzioni sullo stesso run danno lo stesso JSON]`
- `scripts/misura_piattaforma.py RUN_ID` legge i tempi dei passi con
  `gh run view --json jobs` e scrive un JSON con: secondi per passo, totale
  del job, numero di prove, rilievi di ruff, componenti fuori versione.
- La routine settimanale lo esegue sull'ultimo run di `main` e lo confronta
  col precedente: è il «nessuna misura peggiora» del criterio di promozione.

### P3 · ruff da testing a stable ⬜
`[engine: Haiku 5.5 · effort: basso · qualità: i criteri di ADR-0099 §3 verificati e scritti qui]`
- Dopo 14 giorni e 10 run su `main` con zero falsi allarmi non spiegati, si
  toglie `continue-on-error` e si toglie il passo `compileall`, che ruff
  copre (E9).
- Una regola nuova entra solo se, sul repo di quel giorno, i suoi rilievi
  sono difetti veri almeno una volta su due.

### P4 · I test girano una volta, e in parallelo ⬜
`[engine: Sonnet 5.5 · effort: medio · qualità: stesso numero di prove eseguite prima e dopo; il test di parità resta e morde]`
- Se D2: il passo `python -m unittest discover` esce; `test_i_test_girano_in_ci.py`
  continua a contare le prove dei due corridori senza eseguirle, che è ciò
  che il difetto del 2026-09-21 chiedeva. Guadagno atteso: 222 s su 914.
- Se D3: pytest-xdist in testing, prima in un job parallelo non bloccante che
  misura tempo e test instabili per 14 giorni.

### P5 · uv per installare, fare il lock e dare la Python ⬜
`[engine: Sonnet 5.5 · effort: medio · qualità: stesso insieme di pacchetti installati, verificato con pip freeze; il lock con hash si installa con pip --require-hashes]`
- Se D4: `uv pip install --system` al posto di `pip install` in CI (testing,
  confronto dei pacchetti installati per 14 giorni); `uv pip compile
  --generate-hashes` come generatore del lock di A3 al posto di pip-tools;
  `uv python install 3.13` come alternativa al PPA deadsnakes su Ubuntu e al
  distrobox su Bazzite, da misurare in A5b.
- Da misurare prima: se Dependabot aggiorna un lock scritto da `uv pip
  compile` (A3 già lo chiedeva per pip-compile).

### P6 · Una Python sola, controllata ⬜
Lo fa **A2 di AMBIENTE** (il test che confronta `ci.yml` col registro), con
una correzione da ADR-0099 §7: la versione è esatta, non un minimo, e il test
guarda anche `dipendenze.yml`, il Dockerfile e `dependabot.yml`.

### P7 · Le skill e le guide sanno la regola ⬜
`[engine: Haiku 5.5 · effort: basso · qualità: validate_skills e validate_docs verdi]`
- Una riga in `rumblingstone-automation` e in `rumblingstone-debugging`: prima
  di proporre una libreria o uno strumento, il canale e la misura (ADR-0099).
- `rumblingstone-edizione` resta il gate della licenza all'ingresso in testing.

### P9 · I convertitori entrano nella piattaforma ✅ in testing
`[engine: Opus 5.5 · effort: medio · qualità: ruff a zero su converters/; ogni modulo si importa su 3.13 nel job della CI]`
D6, DM 2026-10-23: *«D6 b»*. Corretti i tre bug (`Tuple` non importato:
`fallback_manager` non si importava; `success_count` mai inizializzato;
`language_tool_python` mai importato nel metodo che lo usa) e gli altri sette
rilievi (quattro variabili morte, tre import ripetuti). Python 3.13 in
`pyproject.toml`, `setup.py`, `intelligent_install.py`, `activate.sh` e nel
README, al posto di 3.9 e 3.12; `magika>=1.0.3` senza il marcatore che lo
escludeva da 3.13 (la 1.0.3 ha la ruota per 3.13, e l'API usata
`identify_stream(...).prediction.output.mime_type` risponde
`application/pdf` su un PDF vero). Dependabot ha una voce `pip` per le due
cartelle, con gruppi suoi. Job CI `convertitori`, non bloccante.
Resta: i test del motore leggono PDF fuori dal repo.

### P10 · Il rilascio è una PR ✅ in testing
`[engine: Opus 5.5 · effort: medio · qualità: la PR di rilascio unita crea tag, rilascio, archivio riproducibile e attestazione senza passi a mano]`
DM 2026-10-23: *«iniziare il tag e release come fatto nel progetto
iemod-fetch»*. [ADR-0100](adr/ADR-0100-il-rilascio-e-una-pr.md): CHANGELOG.md
di progetto alla radice (Keep a Changelog, italiano), `__version__` in
`scripts/dmcore/__init__.py` letto da `dm.py --version`, workflow
`release.yml` con `scripts/release_plan.py` e `scripts/release_notes.py`
ripresi da iemod-fetch (MIT, stesso autore), guida in
[docs/RILASCIO.md](../docs/RILASCIO.md). Il primo rilascio è 1.0.0 (D7). Il
workflow sale a stable dopo tre rilasci senza interventi a mano.

### P11 · Il riscontro delle regole sull'SRD ✅ in testing
`[engine: Opus 5.5 · effort: alto · qualità: nessun test usa la rete; uno sha256 sbagliato o la rete assente si dicono con un codice d'uscita loro]`
DM 2026-10-23: *«aggiungi se ci sono tools skills pipeline plugin e tools che
non sono presenti nel repo aggiungili ed integrali […] in un flusso
coerente»*. L'unico candidato che la [ricerca in rete](esperimenti/ricerca-rete-2026-10-23/RICERCA.md)
raccomanda. [ADR-0103](adr/ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md):
`scripts/riscontro_srd.py` scarica l'SRD 3.5 in Markdown e il PRD PF1e in
SQLite a commit fissato, con lo sha256 di ogni file, in
`~/.cache/rumblingstone/srd/`, e riscontra un file di regole (concorda,
discorda, non trovata, con la citazione). Job CI `riscontro-srd` non
bloccante; il flusso di tutti gli strumenti di qualità in
[ARCHITETTURA](../docs/ARCHITETTURA.md) §18. Primo uso su DEF-1 e DEF-2:
[RISCONTRO-ARC08](esperimenti/ricerca-rete-2026-10-23/RISCONTRO-ARC08.md), 53
regole, 3 discordanze lasciate al DM. Sale a stable non prima del 2026-11-06.

### P8 · La prova generale della prossima migrazione ⬜
`[engine: Sonnet 5.5 · effort: medio · qualità: un job non bloccante su Python 3.14 verde per un mese prima del salto]`
- Parte quando Debian 14 entra nel congelamento (atteso nel 2027): un job CI
  non bloccante su 3.14 con gli stessi test. Dopo il salto, 3.13 resta
  oldstable per tre mesi.
- Prima, se una libreria stable annuncia l'abbandono di 3.13: decisione del
  DM fra fermarla e anticipare (ADR-0099 §6).

## §4 · Validazione

| Cosa | Atteso | Come si prova |
|---|---|---|
| ruff in testing | verde su `main`; un NameError nuovo appare nel passo | mutazione fatta in P0 (MISURE §3) |
| nessun peggioramento | tempo del job principale entro +5% di 914 s | P2, sul run della PR e su quelli dopo |
| promozioni | ogni componente stable ha data, misura e ok del DM | P1, test del registro |
| una Python sola | un `python-version` diverso in un workflow boccia la CI | P6 / A2 |
| la CI di `main` | resta verde | sempre |

## §5 · Decisioni

<!-- decisioni-dm: PIATTAFORMA -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | tutti | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«D1-d5 ok»*). **Accetti la regola dei tre canali di ADR-0099?** unstable (a mano), testing (in CI non bloccante, versione fissata), stable (bloccante); si sale dopo 14 giorni e 10 run senza falsi allarmi né peggioramenti, con il tuo ok; Python e runner migrano quando migra Debian, con la vecchia versione tenuta tre mesi |
| ~~D2~~ | P4 | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«D1-d5 ok»*). **Togliamo la seconda esecuzione completa dei test con `unittest`?** Costa 222 s su 914 della CI e riesegue le stesse prove; la parità dei due corridori la controlla già `test_i_test_girano_in_ci.py` senza eseguire niente. Proposta: sì |
| ~~D3~~ | P4 | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«D1-d5 ok»*). **pytest-xdist in testing?** Licenza MIT, solo sviluppo. La suite in locale passa da 219 s a 67 s su 4 core (−69%), stesse prove (MISURE §4). Proposta: sì, prima in un job non bloccante per 14 giorni per vedere se qualche test è instabile in parallelo |
| ~~D4~~ | P5 | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«D1-d5 ok»*). **uv in testing per installare in CI e fare il lock di A3?** MIT o Apache-2.0. Installazione 33 s → 4 s a freddo; in CI il guadagno è circa 20 s su 914, il valore vero è il lock con hash senza pip-tools e la stessa 3.13 su Ubuntu e Bazzite senza PPA. Proposta: sì, in testing |
| ~~D5~~ | P3 | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«D1-d5 ok»*). **ruff resta in testing con gli otto gruppi di regole che cercano bug, e sale dopo 14 giorni?** Le regole di stile restano fuori (1.672 rilievi, quasi tutti scelte volute del repo). Proposta: sì |
| ~~D6~~ | P9 | ✅ **Decisa il 2026-10-23, risposta del DM: B** (*«D6 b»*, dopo la spiegazione: correggere e portare `converters/` nella piattaforma). **I tre bug che ruff ha trovato in `converters/` si correggono?** Un modulo che non si importa, un NameError a fine installazione, una correzione grammaticale che non parte e non lo dice. `converters/` è fuori dalla piattaforma (PRATICHE D9). Proposta: tre righe in una PR a parte, senza portare `converters/` in CI |
| ~~D7~~ | P10 | ✅ **Decisa il 2026-10-23, risposta del DM: sì, la consigliata** (*«1.0.0, solo le skill»*). **Il primo rilascio è 1.0.0, con dentro solo i pacchetti delle skill?** Lo 0.1.0 scritto nel codice non è mai uscito; 1.0.0 dice «la piattaforma di ADR-0099 è la base». Il repo è pubblico, quindi il rilascio lo è: esce solo ciò che il repo mostra già (pacchetti delle skill, sorgenti del tag), i PDF dei booklet no finché non passano dal gate di `rumblingstone-edizione`. Proposta: sì, 1.0.0, solo le skill |

<!-- eco: PIATTAFORMA 2026-10-23 -->
- **Decise**: D1 la regola dei tre canali · D2 un corridore solo per i test · D3 pytest-xdist in testing · D4 uv in testing · D5 ruff in testing, stable dopo 14 giorni · D6 B, `converters/` dentro la piattaforma · D7 primo rilascio 1.0.0 con solo le skill
- **Aperte**: nessuna
- **Cambiate**: D6 dalla proposta A (correggere e lasciare fuori) a B (correggere e portare dentro)
- **Dedotto da me**: che D3 e D4 in testing si provino nello stesso job non bloccante (uv installa, xdist esegue), per pagare un job solo invece di due; che «se sono migliorative poi diventano standard» del DM sia la regola di promozione di ADR-0099 §3, e non un sì anticipato alla promozione; che lo stesso concetto del kernel Linux in Debian» voglia dire i canali unstable, testing e stable con promozione a tempo e senza regressioni, e la migrazione a ogni rilascio di Debian (lettura confermata dalla nota del coordinatore); che le soglie (14 giorni, 10 run, +5%, tre mesi di oldstable) siano mie e da tarare; che «le skill» nella piattaforma vogliano dire che le skill conoscono la regola, non che le skill diventino componenti con un canale

## §6 · Ordine

P0 → D1 → P9 → P10 → P11 → P1 → P2 → P3 e P4 (indipendenti) → P5 dopo A3 di AMBIENTE → P6 con
A2 → P7 → P8 quando Debian 14 si congela.

## Checklist di avanzamento

- [x] P0 · audit, misure, ADR-0099, ruff in testing
- [ ] P1 · il canale nel registro, la tabella generata
- [ ] P2 · `misura_piattaforma.py`
- [ ] P3 · ruff stable (D5 ✅; in testing dal 2026-10-23, non prima del 2026-11-06)
- [~] P4 · test una volta sola (D2 ✅, 2026-10-23: il passo unittest è uscito dalla CI); xdist (D3) in testing nel job `testing` dal 2026-10-23, stable non prima del 2026-11-06
- [~] P5 · uv (D4): installazione in testing nel job `testing` dal 2026-10-23, con il confronto dei pacchetti contro pip; il lock aspetta A3
- [ ] P6 · una Python sola, controllata (con A2 di AMBIENTE)
- [ ] P7 · skill e guide
- [ ] P8 · prova generale della migrazione a 3.14
- [x] P9 · `converters/` nella piattaforma, in testing (D6)
- [x] P10 · il rilascio è una PR (ADR-0100), workflow in testing; primo rilascio 1.0.0 (D7 ✅)
- [x] P11 · il riscontro SRD (ADR-0103) in testing, job `riscontro-srd`; stable non prima del 2026-11-06
