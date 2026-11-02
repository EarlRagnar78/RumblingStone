# Misure della piattaforma di sviluppo, 2026-10-23

Le misure da cui partono [ADR-0099](../../adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)
e [PIANO-PIATTAFORMA-DI-SVILUPPO](../../PIANO-PIATTAFORMA-DI-SVILUPPO.md).
Prese su `main` a `17d0b33` (PR #272), in un container Linux x86_64 a 4 core
con Python 3.13.16 di sistema, e sui tempi della CI di GitHub del run
39801886667 (lo stesso commit).

Ogni numero dice come è stato preso. Dove una misura dipende dalla rete del
container la riga lo dice, perché la rete della CI è un'altra.

## 1 · La versione di Python, a oggi

| Fonte | Cosa dice | Come l'ho letta |
|---|---|---|
| Debian 13 (trixie), stable | `python3` 3.13.5 | elenchi dei pacchetti di trixie (mirror aptpeek.dev) |
| Debian forky, testing | `python3` 3.14.6 | elenco di packages.debian.org per forky |
| python.org, ciclo di vita | 3.13 è uscita a ottobre 2024; correzioni di bug fino a ottobre 2026, poi solo sicurezza fino a ottobre 2029. 3.14 in correzioni di bug fino a ottobre 2027. 3.15 annunciata per ottobre 2026 | devguide.python.org/versions, letta tramite ricerca: la pagina non era raggiungibile dal container |
| Librerie del repo | numpy 2.5 e scipy 1.18 chiedono Python ≥ 3.12; `bpy` 5.2 vuole 3.13 esatto | `requirements-dev.txt`, `requirements-completo.txt` |
| SPEC 0 (scientific Python) | una versione di Python si supporta per 3 anni dall'uscita: 3.13 fino a ottobre 2027 circa | regola nota della comunità; **non riletta oggi**, va verificata prima di usarla come data |

La lettura onesta: 3.13 resta la scelta giusta con la regola di Debian, perché
è la Python di Debian stable e Debian la mantiene con le sue correzioni di
sicurezza per tutta la vita di trixie. Da questo mese però upstream non
rilascia più correzioni di bug per 3.13, solo di sicurezza. È la stessa
situazione del kernel di una stable Debian: congelato, e corretto solo dove
serve. La data che conta per salire è l'uscita di Debian 14 (forky, oggi con
3.14), attesa per il 2027. La data che può costringere prima è il ritiro di
3.13 dalle librerie scientifiche (numpy, scipy, scikit-image), che con SPEC 0
cade intorno a ottobre 2027.

## 2 · Dove il repo esce da 3.13

`grep` su versioni di Python in `*.py *.toml *.yml *.sh *.txt *.json Dockerfile`,
escluse le cartelle generate.

| Dove | Cosa | Stato |
|---|---|---|
| `.github/workflows/ci.yml`, `dipendenze.yml` | `python-version: "3.13"` (4 posti) | in linea |
| `scripts/binari.py` | `PYTHON_MINIMO = (3, 13)` | in linea, ma è un **minimo**: accetta 3.14 e 3.15 senza dirlo |
| `.github/dependabot.yml` | la regola «si sale quando sale Debian» nel commento | in linea, ma è solo un commento: nessun controllo la fa rispettare |
| `scripts/booklet-container/Dockerfile` | `debian:13-slim` per digest, `python3` di sistema | in linea (3.13) |
| `requirements-completo.txt` | `bpy … python_version == "3.13"` | in linea |
| `converters/pdf-to-md-engine/` | `requires-python = ">=3.9"`, `target-version = ['py39']`, `setup.py` e `intelligent_install.py` cercano `python3.12`, `activate.sh` stampa 3.12.12 | **fuori linea**. È il «mondo a parte» di AGENTS.md e di PRATICHE D9 |
| `converters/Html_to_markdown/` | nessuna versione dichiarata | indefinito |
| `.serena/project.yml` | un link alla documentazione di 3.11 in un commento | irrilevante |
| hook git | nessuno installato (A4 di AMBIENTE non è fatto) | — |
| venv locali | non tracciati; `ambiente.py` crea `.venv` con l'interprete che lo lancia | non controllato |
| skill e loro script | nessuna versione dichiarata; girano col Python di chi le esegue | non controllato |

## 3 · Gli strumenti candidati

### ruff (MIT) — linter

Versione 0.16.9. Tempo su `scripts/` e `converters/`, a freddo: **0,08 s**.

| Insieme di regole | Rilievi | Di cui difetti veri |
|---|---|---|
| tutte quelle attive di default | 1.672 | non contato: quasi tutto stile |
| E4, E7, E9, F (il vecchio default) | 424 | la gran parte è `if x: y` su una riga e import non usati, scritti così di proposito |
| B (bugbear) | 77 | **B023: 20 falsi allarmi su 20** (chiusure usate dentro il giro, mai dopo); B905, B007, B904 sono stile |
| E9, F63, F7, F82, F811, F841, PLE (scelto) | 17 su `scripts/`, 10 su `converters/` | vedi sotto |

Sull'insieme scelto, uno per uno:

- `scripts/`: 13 × F821 in `dmcore/testo.py`, tutti `"Path"` nelle annotazioni
  senza import (a runtime non rompe niente grazie a `from __future__ import
  annotations`, ma `typing.get_type_hints` fallirebbe); 2 × F841 (una
  variabile morta in `import_ultraclear.py`, una in `misura_craft.py` che la
  PR #264 toglie già); 2 × PLE2515 per uno spazio di larghezza zero dentro un
  docstring, voluto. **Zero bug a runtime.**
- `converters/`: **3 bug veri**. `fallback_manager.py` usa `Tuple` senza
  importarlo in un'annotazione valutata subito: il modulo non si importa su
  nessuna Python fino a 3.13. `intelligent_install.py:650` incrementa
  `success_count` mai inizializzato: NameError alla fine dell'installazione.
  `ai_enhancer.py:105` chiama `language_tool_python` mai importato, dentro un
  `except Exception`: la correzione grammaticale non funziona e non lo dice.
- Mutazione: un file con `return nome_mai_definito` passa `python -m
  compileall` (il passo di oggi in CI) e ruff lo boccia.

Conclusione: su `scripts/` il cancello oggi non trova bug, perché i test e i
cancelli del repo li trovano prima. Il valore è preventivo e costa 0,08 s. Su
`converters/`, che non ha test né CI, trova tre bug su dieci rilievi.

### mypy (MIT) — tipi

Versione 2.3.1, `--ignore-missing-imports --python-version 3.13` su `scripts/`:
**328 errori in 85 file, 8,6 s**. Ho letto 41 rilievi delle classi più
probabili (`attr-defined`, `call-arg`, `name-defined`, `return-value`,
`call-overload`): nessun bug a runtime; sono annotazioni imprecise
(`tuple[int, ...]` dichiarata `tuple[int, int, int]`, `"sys.NoReturn"` invece
di `typing.NoReturn`) o inferenze sbagliate su dizionari eterogenei. Costo di
adozione: annotare o silenziare circa 300 righe in 85 file, per un guadagno
che il campione non mostra. **Non si adotta.** pyright non è stato misurato
(serve Node).

### uv (MIT o Apache-2.0) — installazione e lock

Versione 0.11.32, `requirements-dev.txt` (58 pacchetti, 188 MB di ruote), in un
venv nuovo con `/usr/bin/python3.13`:

| | pip 26.2 | uv |
|---|---|---|
| a freddo, senza cache | 33,2 s · 33,1 s · **9 min 12 s** (bloccato sulla rete) | 3,6 s · 4,1 s |
| con la cache calda | 20,7 s · 21,1 s | 0,09 s · 0,19 s |
| bloccati | 2 su 7 giri (uno oltre 10 minuti, interrotto) | 0 su 5 |

I blocchi di pip possono dipendere dal proxy del container, non da pip: li
riporto e non li uso come argomento. In CI l'installazione con pip costa
**22 s** su 914 del job principale (2,4%): il guadagno di tempo in CI è
piccolo. Il guadagno vero di uv è altrove: `uv pip compile --generate-hashes`
fa il lock con hash di A3 senza aggiungere pip-tools, e `uv python install
3.13` dà la stessa 3.13 su Ubuntu 24.04 e su Bazzite senza il PPA deadsnakes.
Queste due cose **non** sono misurate oggi.

### pytest-xdist (MIT) — test in parallelo

Vedi §4.

### pre-commit (il framework, MIT)

Non misurato, e non proposto: A4 di AMBIENTE ha già deciso gli hook (D11) in
`.githooks/` senza dipendenze, e il framework scarica gli hook dalla rete al
primo uso, che è ciò che ADR-0037 evita sul portatile del DM.

## 4 · La CI e i test

Run 39801886667 su `main`, job «Validate skills & scripts»: **914 s** (15 min
14 s). I passi più lunghi:

| Passo | Secondi | Quota |
|---|---|---|
| Unit tests, unittest | 222 | 24% |
| Unit tests, pytest | 220 | 24% |
| Resa delle mappe (`misura_resa --check`) | 136 | 15% |
| Edizione da stampa (typst) | 126 | 14% |
| Corredo della serata | 99 | 11% |
| Installazione delle dipendenze | 22 | 2% |
| tutti gli altri 50 passi | 89 | 10% |

**Gli stessi test girano due volte, ed è metà del tempo della CI.** La
parità fra i due corridori, che è la ragione per cui girano entrambi (il
difetto del 2026-09-21), la controlla già
`test_i_test_girano_in_ci.py` contando le prove dei due senza eseguirle.

Suite locale, `pytest scripts/tests`, in serie e con `-n auto` (4 core):

| | tempo | prove |
|---|---|---|
| `pytest scripts/tests` in serie | **219 s** | 2.013 passate, 26 saltate |
| `pytest scripts/tests -n auto` (pytest-xdist, 4 processi) | **67 s** (−69%) | 2.014 passate, 26 saltate |

Il tempo in serie in locale (219 s) è lo stesso della CI (220 s), quindi il
confronto vale anche lì: i runner pubblici di GitHub hanno 4 core. Un giro solo
per parte: per dire che non ci sono test instabili in parallelo servono i 14
giorni di testing (D3).

I fallimenti dei due giri, letti uno per uno, non vengono da xdist:
`test_fase1` vuole un clone completo e il container ne ha uno *shallow* (la CI
fa `fetch-depth: 0`); gli altri erano `validate_docs`, `decisioni_dm` e
`memoria` che vedevano questo piano a metà scrittura, e passano dopo
`decisioni_dm.py --emit` e `memoria.py` (109 su 109 sui sei file toccati).

Con i due cambi insieme (D2 e D3) il passo dei test va da 442 s a circa 70: il
job principale da 914 s a circa 540, **−40%**. È una stima da sommare, non una
misura in CI: la misura la fa il lotto P4.

Un'ultima cosa trovata per strada: in serie pytest dava **120 avvisi**, tutti
`DeprecationWarning` di un `re.split(r":", s, 1)` in `import_ultraclear.py`.
Passare `maxsplit` per posizione è deprecato da Python 3.13; ruff lo trova
con B034, che per questo è entrato nell'insieme di regole.

## 5 · Prima e dopo, sulla qualità del progetto

Dopo le risposte del DM (D1-D6, stesso giorno). Ogni riga si rifà col comando
indicato; dove la misura la fa la CI della PR, la riga lo dice.

| Misura | Prima (`main`, 17d0b33) | Dopo (PR #273) | Come |
|---|---|---|---|
| bug veri aperti trovati da ruff | 3 (in `converters/`) | **0** | `ruff check` (regole di `ruff.toml`) |
| rilievi di ruff, regole-bug, su `scripts/` e `converters/` | 28 | **0** (3 dichiarati in `ruff.toml`, con la ragione) | idem |
| `DeprecationWarning` nella suite | 120 | **0** | `pytest scripts/tests/test_import_ultraclear.py` |
| moduli del motore PDF che si importano, senza torch | 12 su 20 | **13 su 20** (`fallback_manager` non si importava su nessuna Python) | script di import in un venv con le dipendenze leggere |
| moduli del motore PDF che si importano, con tutte le dipendenze | non misurato | primo run della CI: **11 su 20**. `pdfplumber` mancava da `requirements.txt` (c'era solo in `pyproject.toml`) e `src/config.py` vuole `INPUT_DIR` e `OUTPUT_DIR` già all'import; corretti tutti e due | job `convertitori` della CI (qui `download.pytorch.org` non è raggiungibile) |
| file che dichiarano una Python diversa da 3.13 | 6 (tutti in `converters/`) | **0** | `grep` di §2 |
| controlli che guardano `converters/` | `compileall` | `compileall`, ruff, import su 3.13, Dependabot | `ci.yml`, `dependabot.yml` |
| esecuzioni complete della suite in CI | 2 (unittest e pytest) | **1** (più quella in parallelo del job `testing`, non bloccante) | `ci.yml` |
| prove raccolte da pytest | 2.017 più 26 saltate | 2.017 più 26 saltate (la parità dei corridori resta controllata) | `test_i_test_girano_in_ci.py` |
| tempo del job principale | 914 s | lo misura la CI della PR | tempi dei passi del run |

### Un test instabile in parallelo, trovato dal canale testing

Rieseguendo con `-n auto` un sottoinsieme della suite, tre test di
`test_validate_docs.py` sono falliti due volte su due e passano in serie.
Altri test **scrivono file finti dentro il repo vero** (per esempio
un ADR finto con un numero già usato, o un file citato come
`futuro`) e li tolgono alla fine; se nello stesso momento un altro processo
scandisce il repo, li vede. Sull'intera suite, al primo giro, non era
successo: dipende da come xdist distribuisce i test. È esattamente ciò che il
canale testing deve trovare prima che xdist blocchi la CI. Per salire a
stable (P4) quei test devono scrivere in una cartella temporanea, oppure
finire nello stesso processo con `--dist loadfile`.

**Seguito, stesso giorno.** Il job `testing` della PR ha bocciato un quarto
test (`test_verifica_sezione6`, che esegue `validate_docs --sorgenti` mentre un
altro processo aveva un ADR finto in `plans/adr/`). Chi scrive nel repo vero
l'ha detto una misura, non una ricerca nel codice: un audit hook di Python su
`open` in scrittura, caricato con un `sitecustomize.py` messo in `PYTHONPATH`,
che annota il test in corso (`PYTEST_CURRENT_TEST`) e il file, durante l'intera
suite in serie. Fuori dalle cartelle temporanee scrivono cinque moduli:
`test_validate_docs`, `test_norme_editoriali`, `test_orchestrazione_skill`,
`test_archivi_non_indicizzati` e `test_dm_volume` (91 prove). Prendono il
marcatore `scrive_nel_repo` in `scripts/tests/conftest.py`, e il job `testing`
li esegue in serie dopo il giro in parallelo. Risultato in locale: tre giri di
`-n auto -m "not scrive_nel_repo"` uguali (1.925 passate, sempre lo stesso
fallimento di `test_fase1`, che dipende dal clone superficiale), 70 s, più 15 s
per le 91 in serie. Il conto dei 14 giorni per promuovere xdist riparte da qui.

