# Lotto 7e · prima e dopo il ritiro delle misure obsolete

Fonte delle voci: `INVENTARIO-MISURE-OBSOLETE.md` (qualità misurabile, 2026-10-22).
Si applicano le voci senza ⚖️; quelle con ⚖️ restano patch in questa cartella, per il DM.
Misure prese in locale, 4 core, mediana di tre corse per i passi brevi e una corsa per
compilazioni e suite. «Prima» è il commit c501c98c, «dopo» è il ramo `obsolete-lotto7`
col merge del lotto 7f (66c50e14), che non tocca gli strumenti.

## La tabella

| Misura | Prima | Dopo |
|---|---:|---:|
| **Tempo dei passi di CI toccati** (s) | | |
| validate_prosa, passo non bloccante | 6,42 | tolto |
| validate_prosa `--foglio --strict` | 2,33 | 2,42 |
| validate_lingua (uscita in righe) | 4,23 (22) | 4,19 (2) |
| domande_developer `--check` | 0,48 | 0,47 |
| validate_norme_editoriali | 0,32 | 0,19 |
| superficie_norme `--check` | 0,33 | dentro il precedente |
| verifica_sezione6 `--check` | 4,76 | 2,74 |
| MQM (punteggio, tetto EL, registro) | 8,12 | 8,48 |
| passo dei booklet in CI | 131,3 (17 volumi) | **54,8** (13 volumi; i 4 del corredo li compila il passo dopo) |
| validate_corredo `--stampa --rigoroso` | 103,9 | 100,8 |
| pytest, suite intera | 211,4 | 201,0 |
| unittest, suite intera | 198,8 | 203,2 |
| **Somma dei passi toccati** | **672,4** | **578,3** (−94 s, −14%) |
| **Righe degli strumenti di qualità** (codice / test) | 11.592 / 3.467 | 11.071 / 3.273 (−521 / −194) |
| **Registro**: righe-norma (🟢 · 🟡 · 🔴 · ⚪) | 112 (47 · 35 · 26 · 4) | 95 (43 · 39 · 13 · 0) |
| norme che entrano nel punteggio MQM | 13 | 13 |
| **MQM**: rilievi / pesati | 544 / 756 | 544 / 756 (uguale, voluto: nessuna norma pesata è toccata) |
| **`ciclo_prosa segnala`** su ARC-07 DEF e ARC-08 (22 file) | 107 | 107 |
| **Congegni** di `misura_craft` | 23 | 15 |
| opzioni di `misura_craft` | 10 | 9 |
| prove (pytest) | 2.043 verdi, 3 rosse d'ambiente | 1.994 verdi, 2 rosse d'ambiente; 10 saltate per l'ambiente (typst fuori dal PATH, bpy, clone poco profondo) |

I tempi del «dopo» sono della corsa sul commit WIP, prima del ritorno di
`--costrutto-italiano`, che non tocca nessuno di questi passi. Una seconda corsa
dopo il merge, con la macchina carica, ha dato tempi più alti per tutti i passi
lunghi (booklet interi 160 s, pytest 247 s): le due corse della tabella sono state fatte
a poca distanza, con la macchina scarica, e sono quelle da confrontare.

Le tre prove rosse di pytest sono le stesse prima e dopo, tutte d'ambiente: il clone
poco profondo (`test_fase1::TestRamiAccanto`), typst assente dal PATH della prova
(`test_pacchetti_typst`), il percorso del worktree che contiene `.claude`
(`test_superficie_norme::test_l_insieme_dei_file…`).

## Le voci applicate

Ogni riga dice cosa, perché (col dato dell'inventario), il guadagno misurato e il rischio.

**Tolte**

- **Calco «assumi che»** da `validate_prosa.CALCHI_SEMPRE`. Perché: zero scatti in tutto il repo. Guadagno: una regola e il suo test in meno. Rischio: nessuno; se il calco torna, si riaggiunge in una riga.
- **Watchlist dei tic minori** da `ciclo_prosa.DEBOLI`. Perché: zero scatti, e la regex non vedeva le forme frequenti. La lista resta in `italiano-nativo.md` per chi rilegge. Rischio: nessuno.
- **Otto congegni di `misura_craft`** (spotlight per PG, tattiche round-per-round, orologio, nodo d'indizio, ADR interni, battute di dialogo; più «se i PG…» e «scalare lo scontro», fusi sotto). Perché: i sei contavano una parola senza norma (spotlight 8.869 scatti = ogni nome di PG, battute 6.760 = ogni virgoletta); gli altri due hanno un rilevatore migliore in `domande_developer`. Guadagno: congegni 23 → 15, misura_craft 1.161 → 1.074 righe. Rischio: le colonne spariscono dalle tabelle storiche; nessuna norma le usava.
- **`misura_craft --discriminante`**. Perché: ha già risposto (23 congegni su 23 «separano») e non può dire niente sulla qualità. Guadagno: un'opzione, `test_potere_discriminante.py` (80 righe). Rischio: nessuno.
- **Il passo non bloccante di `validate_prosa`** in CI (la regola resta: gira dentro MQM e nel foglio). Perché: stampava senza fermare niente e MQM rilegge gli stessi rilievi. Guadagno: 6,42 s per corsa. Rischio: chi leggeva il log del passo ora legge MQM.
- **Quattro righe ⚪ del registro** che non erano norme (ordine del box, living-world e quest-design, spezia del banco, sigle ADR-0060). Rischio: nessuno.

**Declassate**

- **D20 fuori da `domande_developer --check`**, stampata come indicatore («~»). Perché: non calibrata, un boss solo sotto cancello. Guadagno: un cancello che non può più fermare un master per un falso; un test nuovo lo fissa. Rischio: un presagio mancante non ferma più la CI.
- **`validate_lingua`**: gli avvisi diventano un conto per tipo, l'elenco esce con `--avvisi`. Perché: 2.442 avvisi fermi da un mese. Guadagno: uscita da 22 righe a 2. Rischio: nessuno, l'elenco c'è a richiesta.
- **Tre righe 🟢 → 🟡** (PILASTRO, chiusura su decision point, regia di round). Perché: il congegno conta la marca o una frase fissa, non la norma.
- **Undici righe di giudizio e fuori dominio** spostate nel nuovo §5 del registro, fuori dal conto delle misurabili (le nove letture dell'agente, il congegno che scatta al tavolo, la hero map fedele all'SVG). Perché: «un cancello su un giudizio sarebbe rumore», lo diceva già la riga. Guadagno: il conto dice quello che si misura. Rischio: restano leggibili, ma nessuno le conta più.

**Fuse**

- **I quattro volumi del corredo compilati una volta**: `validate_booklets --stampa --salta-corredo` in CI, perché `validate_corredo --stampa` li compila e li misura. I controlli del guscio e dei segnalibri stanno in una funzione sola che usano tutti e due. Guadagno: il passo dei booklet da 131,3 s a 54,8 s. Rischio: un volume del corredo è controllato solo da `validate_corredo`, che è bloccante.
- **`voto_scrittura.py` tolto** *(2026-10-23: rimesso dal merge con main, perché `banco_prosa_locale.py` di ADR-0089 lo usa; tiene il rilevatore preso da `validate_prosa` e la correzione per il possessivo, il guadagno di righe non c'è più)*: `SEMBRA` e `sembra_esitanti` passano in `validate_prosa`, il banco L11 esce. Perché: B-con al 100% (soffitto), ogni controllo era già in MQM. I dati di `plans/scrittura/` restano come archivio. Guadagno: 329 + 164 righe. Rischio: l'etichetta del rilevatore in `specifiche-qualita.yaml` è cambiata (`validate_prosa.sembra_esitanti`): è una riga del file del DM, rinomina e basta, soglie e pesi uguali.
- **«sembra/pare» su una superficie**: la norma `box_sembra_pare` di MQM, che `ciclo_prosa segnala` riporta box per box; fuori da DEBOLI, dove contava anche fuori dai box (87 scatti contro 10 box veri).
- **`superficie_norme.py` dentro `validate_norme_editoriali.py`** (`--superficie`, `--json`): stesso file, stesse righe 🔴, un passo di CI in meno. Guadagno: 473 righe di script tolte, 299 → 584 nel validatore, 0,33 s di passo. Rischio: chi chiamava `superficie_norme.py` deve usare l'opzione nuova; manifest e documenti aggiornati.
- **Le tre norme dei nodi d'indagine** (≥3 porte, 6-9 nodi, ≤9 elementi) in una riga, sbloccate insieme da I6.
- **«Scalare lo scontro» con D10** e **«se i PG» con D19**: la riga del registro rimanda a `domande_developer --check`, calibrata.

**Tenuta per voto del DM**

- **`misura_craft --costrutto-italiano`** era nell'elenco da togliere. Il voto cieco del 2026-10-22 sulla riscrittura di prova dice che il «c'è» presentativo non ha perso (sei vincitori su otto lo portavano): l'opzione resta com'era, 🟡 nel registro e fuori dal punteggio.

## Le voci non fatte

- **P1 `read_aloud_presuppone` a indicatore**: era fra le voci senza ⚖️, ma toglierla dal punteggio vuol dire togliere la norma da `specifiche-qualita.yaml`, che è del DM. È una patch (`patch-p1-read-aloud-presuppone.diff`).
- **`--copertura` fusa in `--mancanti`** e la riga «appunti in 400 parole»: non erano nell'elenco del lotto.
- La tabella «Le severità» del registro era già incoerente prima del lotto (57 contro 112): non è toccata.
- `plans/esperimenti/qualita-misurabile-2026-10-22/riscrittura/esegui.py` (lotto 7f) importa `voto_scrittura`: misura la catena com'era a 66c50e14 e lo dice nella docstring; per rifarlo si torna a quel commit.

## Le patch ⚖️ per il DM

Ognuna si applica da sola sul ramo (`git apply <patch>`); misure prese con la patch applicata.

| Patch | Cosa | Guadagno misurato | Tocca |
|---|---|---|---|
| `patch-nomi-propri.diff` | `box_piu_di_un_nome_proprio` fuori dal punteggio, `ciclo_prosa` non segnala più i nomi | MQM 544/756 → **343/555** (−201 rilievi, −201 punti pesati); `segnala` 107 → **44**; registro 42 🟢 · 40 🟡; 12 norme nel punteggio | `specifiche-qualita.yaml`, baseline dei punteggi |
| `patch-p1-read-aloud-presuppone.diff` | P1 indicatore, fuori dal punteggio | MQM → **513/725** (−31/−31); registro 42 🟢 · 40 🟡 | `specifiche-qualita.yaml`, baseline |
| `patch-possessivo-calchi.diff` | il possessivo sulle parti del corpo diventa un indicatore senza peso (ADR-0093) | MQM → **520/732** (−24/−24; l'inventario stimava ~35) | `validate_prosa`, `punteggio_mqm` |
| `patch-stile-gerundio-mente.diff` | `--stile` senza gerundio in coda e -mente (ADR-0093/0097: 0/0/38 e 2/0/36 nella calibrazione) | misura_craft −71 righe, test −29; tempo uguale (1,1-1,3 s); rompe `calibra_prosa.py` e `riscrittura/esegui.py`, archivi | `misura_craft`, test |
| `patch-ciclo-prosa-deboli.diff` | DEBOLI conta antitesi e trattino con le soglie di `validate_prosa` (ADR-0077) | «tic minori in gruppo» 11 → **1**; `segnala` 107 → 97; due test nuovi | `ciclo_prosa`, test |
| `patch-due-corridori.diff` | la CI gira solo pytest; la parità resta presidiata da `test_i_test_girano_in_ci.py` | **−200 s** a ogni push (la corsa di unittest) | `ci.yml`, `gate_locale.py` |
| `patch-campioni-kappa.diff` | `campioni_kappa.py` e il suo test tolti; campioni e voti restano in `campaign/misure/` | −366 righe; test 13,5 s per corridore (27 s con due) | manifest, documenti |

Non hanno patch, perché sono note e non codice: D16 non calibrata (ADR-0092) e
`verdetto_misurato` (ADR-0093) restano come sono finché il DM non le riapre.
