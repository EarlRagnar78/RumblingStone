# PIANO DI REVISIONE TRASVERSALE — Rituale P3B · Mappe · Artefatti

> **Versione**: v1 (2026-07-03) — nasce dalle 3 domande del DM sui piani
> ARC-07/08/09 completati: (1) il costo della resurrezione di Hella deve
> essere una scelta giocabile, (2) tutte le mappe alla qualità delle mappe
> drow ARC-09 / degli AP 3.5-PF1e (con companion DM stile RHoD), (3)
> chiarezza degli artefatti vivi per DM e giocatori (modello: cartella
> Tordek). **Scopo**: documento autocontenuto da dare in pasto a engine AI
> a **lotti**; ogni task ha evidenza, azione, criterio di accettazione e
> **assegnazione engine** (§4). I task **T1-T4 sono GIÀ ESEGUITI** (sessione
> 1, 2026-07-03) e fanno da **esemplari di qualità** per i lotti restanti.
> **Gemelli metodologici**: `07_.../PIANO-REVISIONE-ARC07-...md`,
> `08_.../PIANO-REVISIONE-ARC08-...md`, `09_.../PIANO-REVISIONE-ARC09-...md`
> — le loro regole d'oro valgono anche qui.
> **Benchmark**: (interno) `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`
> per le mappe, cartella `PG/Artefatti/Artefatti-Pg/Tordek/` per gli
> artefatti; (esterno) *Red Hand of Doom* per i companion tattici, AP Paizo
> PF1e per handout e struttura.

---

## §0 — REGOLE D'ORO (identiche ai piani ARC — leggere prima di ogni lotto)

1. **`campaign/state.md` §0 vince** per la posizione del tavolo (OGGI:
   ARC-07 P4 in corso, solo Topazio acceso — D8/D16); §1/§6 sono "scritti
   in avanti" (stato preparato ARC-09): vedi
   `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md` [T4-a]. Canone modificato
   ⇒ riga di changelog in state.md §8, mai riscrivere la storia.
2. **D&D 3.5 SRD only**, italiano meccanico (CD, Osservare, Nascondersi).
   Niente 5e, niente FR post-1385 DR.
3. **Mai inventare** stat/poteri/fatti: flag `[INFERRED — needs DM
   confirmation]`. Le proposte di design nuove si marcano `[PROPOSTA —
   needs DM confirmation]` (es. sinergie future §3 del file SINERGIE).
4. **Un lotto = un commit** descrittivo. Dopo ogni lotto: grep del
   criterio di accettazione + aggiornare la checklist §5.
5. **Non cancellare file**: banner ⚠️ DEPRECATED/SUPERATA (D10). Eccezioni
   (temporanei Word `~$`, `~WRL*.tmp`) solo con conferma DM.
6. Mappe: scala **1,5 m/quadretto** dichiarata; la griglia markdown è il
   MASTER, gli SVG in `rendered/` sono artefatti generati (mai a mano).
7. **Esiti aperti (D13 ARC-09)**: trigger ai dadi e alle scelte dei PG,
   mai copioni — vale per il ramo del rifiuto e per gli stati EVOLUZIONE.

### Decisioni prese (T-D1…T-D5 — applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| T-D1 | La resurrezione di Hella **non è mai in ostaggio**: i sacrifici comprano i DONI, non la vita. Il rifiuto è giocabile (alternative equivalenti + conseguenze + echi) | DM 2026-07-03 (domanda 1) → P3B §2-BIS |
| T-D2 | Qualità mappe = **griglia emoji master** (leggibile da umano) **+ SVG generato** (`scripts/render_map_svg.py`) **+ companion 3 blocchi** (Ambiente/Tattiche/Evoluzione). NO battlemap generate con AI raster (griglie inaffidabili); per estetica extra: Dungeon Alchemist/Dungeondraft come layer opzionale | DM 2026-07-03 (domanda 2) |
| T-D3 | Artefatti = **regola dei 3 documenti** (SCHEDA-DM con tabella di progressione · SCHEDA-GIOCATORE-STATO-ATTUALE · riga state.md §6), modello Tordek, censimento in ARTEFATTI-MATRICE-VERSIONI.md | DM 2026-07-03 (domanda 3) |
| T-D4 | Le **sinergie della Collana (Hella)** si sbloccano in gioco (quest ARC-09); restano [PROPOSTA] finché il DM non le convalida al tavolo | DM 2026-07-03 |
| T-D5 | **Assegnazione engine per lotto** (§4): esecutivo/ripetitivo → **Sonnet 5**; consolidamento/generativo/bilanciamento → **Opus 4.8**; **Fable** SOLO per i casi speciali marcati 🔶 (arbitrati di canone multi-file) | DM 2026-07-03 |

---

## §1 — LOTTO T-A: Fondazioni ed esemplari (✅ ESEGUITO, sessione 1)

### T1. P3B: il ramo del rifiuto — ✅ FATTO (2026-07-03)
- **Evidenza**: il rituale aveva costi fissi senza ramo "e se un PG
  rifiuta?" — agency limitata (domanda 1 del DM).
- **Fatto**: aggiunto **§2-BIS "Il ramo del rifiuto"** a
  `PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md`: 3 strade per PG
  (dono/alternativa/rifiuto), tabelle di alternative equivalenti (Thorik:
  −2 COS / −3.000 XP / Aegis Fang senza Returning; Tordek e Artemis
  analoghe), conseguenze per Hella (dono mancante = assente), rifiuto
  totale → **3 slot-dono vuoti sulla Collana colmabili in gioco (quest
  ARC-09)**, reazioni di Moradin, varianti del risveglio, tabella echi
  formato ARC-09, nota di bilanciamento sull'asimmetria voluta dei costi.
  Banner "Agency (T1)" in testa al master.
- **Accettazione** ✅: nessun esito forzato; meccaniche solo SRD/canone;
  la scelta ONSCREEN di B2 resta il default.

### T2. Renderer SVG delle mappe — ✅ FATTO (2026-07-03)
- **Evidenza**: mappe in stili diversi tra archi; le emoji-grid revised
  sono lo standard più chiaro ma non stampabili "da AP".
- **Fatto**: `scripts/render_map_svg.py` (Python puro, zero dipendenze):
  parsa le griglie emoji nei fence markdown (righe numerate, intervalli
  `01-05`, righe saltate = ripetizione della precedente, marcate in
  grigio), palette uniforme (terreni pieni, token-cerchio per unità,
  icone per oggetti), coordinate A../01.., barra di scala 1,5 m, legenda
  italiana. Testato: **5 SVG generati e validati** (Campo Drow 1-2 ARC-09,
  Stanza della Corona + Sala Forgia ARC-07, Dirupo Mortale ARC-08) in
  `rendered/` accanto ai sorgenti; screenshot verificati a occhio.
  Documentato in `scripts/README-automation.md`.
- **Accettazione** ✅: `python3 scripts/render_map_svg.py <file> --list`
  trova le mappe; XML valido; leggibile da un umano senza il file sorgente.

### T3. Template companion mappa (Ambiente/Tattiche/Evoluzione) — ✅ FATTO
- **Evidenza**: solo le mappe drow e le FASI della Battaglia Finale hanno
  tattiche/evoluzione; RHoD lo fa per ogni mappa (domanda 2).
- **Fatto**: `campaign/templates/mappa-tattica-template.md` — regole di
  compilazione (scala, legenda universale, SRD, master markdown → SVG),
  3 blocchi obbligatori con struttura a tabella, **esempio compilato**
  consolidato dal Campo Drow 1 (stati A-D: routine → allarme → campo in
  fiamme → rotta; zero dati inventati, gli aggiunti flaggati [INFERRED]),
  checklist di adozione in 7 punti per i lotti T5.
- **Accettazione** ✅: template autosufficiente; l'esemplare non contraddice
  il file sorgente.

### T4. Artefatti: matrice + template + esemplari — ✅ FATTO
- **Evidenza**: cartella Corona con ~20 file senza gerarchia; scheda
  giocatore ferma alla "Fase 2"; sinergie senza data né Hella; state.md §6
  su due tempi non dichiarati (domanda 3).
- **Fatto**: (1) `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md` — censimento
  completo per artefatto con master eletti, ruoli, flag [T6] e nota
  [T4-a] sul doppio tempo di state.md; (2)
  `campaign/templates/artefatto-vivo-template.md` — regola dei 3
  documenti + struttura SCHEDA-DM con tabella di progressione; (3)
  esemplare Corona: `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` a **2
  snapshot etichettati** (oggi = solo Topazio; ingresso ARC-09 = 3 gemme,
  Rubino SPESO) + banner SUPERATA sulle 3 schede giocatore vecchie +
  banner di navigazione sul master DM; (4)
  `PG/Artefatti/SINERGIE-ARTEFATTI-MASTER.md` versionato — sinergie
  canone S1-S4, oggetti spesi, **sinergie future F1-F4 della Collana
  [PROPOSTA]** legate alle quest ARC-09 e agli slot-dono del ramo T1
  (riusano solo poteri già canonici), procedura di aggiornamento export.
- **Accettazione** ✅: un master per artefatto o flag esplicito; la scheda
  giocatore non spoilera; nessun potere nuovo spacciato per canone.

---

## §2 — LOTTO T-B: Mappe di tutta la campagna (T5)

### T5a. Rendering di massa + censimento — ✅ FATTO (sessione 2, 2026-07-03)
- **Azione**: eseguire il renderer su TUTTI i file-mappa degli archi
  00-09 (`*MAPPE*`, `*Ultra-Clear*`, `*Lotto*`, `TACTICAL-GRIDS*`,
  `*FASE*-MAPPA*`, atlanti); committare gli SVG in `rendered/`; produrre
  `MAPPE-CENSIMENTO.md` (repo root): per ogni mappa — file, parte/scena,
  scala dichiarata sì/no, griglia parsabile sì/no, companion presente
  (nessuno/parziale/completo), SVG ok/KO con motivo.
- **Fatto**: 34 file censiti (repo root: `MAPPE-CENSIMENTO.md`); **16 SVG**
  generati/rigenerati in 9 file sorgente (5 preesistenti dall'esemplare T2 +
  11 nuovi: Portale-Forgia L2, Hammerfist L2/L3, Hammerfist Lotto 1-3); 22
  mappe/file KO catalogati in 4 categorie di motivo (griglia ASCII non-emoji,
  diagrammi box-drawing pre-Ultra-Clear già deprecati, 16 file narrativi
  ARC-09 P2/P3 mai stati in formato griglia, atlanti/indici senza griglia
  per costruzione) — zero fix di contenuto in questo lotto.
- **Accettazione** ✅: censimento completo; ogni mappa parsabile ha il suo
  SVG; i KO hanno la riga di diagnosi (niente fix in questo lotto).

### T5b. Companion per mappe CON tattiche esistenti (engine: **Sonnet 5**)
- **Azione**: per le mappe che già hanno sezioni tattiche/statblock
  sparse (censimento T5a), riorganizzare nei 3 blocchi del template —
  SOLO consolidamento, zero invenzioni; aggiunte inevitabili flaggate
  [INFERRED]. Ordine: prima le mappe delle parti DA GIOCARE (P3B, P5,
  ARC-08 assedio, ARC-09 quest imminenti), poi il resto.
- **Accettazione**: checklist ①-⑦ del template soddisfatta per ogni mappa
  trattata; nessun dato nuovo non flaggato.

### T5c. Companion generativi + griglie mancanti (engine: **Opus 4.8**)
- **Evidenza**: Campo Drow 2 ha griglia volutamente abbreviata
  (`[continues...]`); `SUPPLEMENTO-P1C-...-Description.md` è **0 byte**
  (task ARC-09 §161 aperto); molte mappe ARC-07/08 non hanno né tattiche
  né evoluzione.
- **Azione**: completare la griglia del Campo Drow 2 (80×53 dichiarato)
  coerente con le posizioni testuali; riempire o deprecare il file 0
  byte; scrivere i blocchi TATTICHE/EVOLUZIONE dove non esistono, con
  bilanciamento EL/GS coerente coi ricalibrati (metodo `Terros.md`) e
  morale/contromosse stile RHoD; statblock SOLO per riferimento a file
  esistenti o catalogo.
- **Accettazione**: zero mappe senza companion negli archi 07-09; EL
  dichiarati; esiti aperti (D13); [INFERRED] su ogni scelta di design.

## §3 — LOTTO T-C: Artefatti di tutti i PG (T6-T8) e propagazione rituale (T9)

### T6a. Igiene meccanica cartelle artefatti (engine: **Sonnet 5**)
- **Azione**: applicare i flag `[T6]` della matrice — banner 📸 sui 2 file
  Ring top-level; deprecare le copie html doppie della scheda Bracieri
  (`copy 2`, `Final`); `git mv` `Avvneture_per_nani.txt` (refuso);
  spostare/marcare il tooling locale di Tordek (`apply_styles.py` ecc.);
  chiedere al DM (flag, non agire) la rimozione dei temporanei Word.
- **Accettazione**: ogni file della matrice ha lo stato che la matrice
  dichiara; matrice aggiornata; zero contenuti modificati.

### T6b. Consolidamenti Corona/Aegis/Cerebromorphosis (engine: **Opus 4.8**)
- **Azione**: (1) fondere i near-dup Corona (`000_Corona_adamantio_ogetto`
  → assorbito nel master DM; eleggere una delle 2 `Schede_avvenimenti`);
  (2) estrarre il **master .md di Aegis Fang** dal docx/pdf (tabella di
  progressione inclusa: pre-risveglio → risveglio pieno post-Siege, fonte
  `05_Aegis_Fang_Final_Awakening.html`); (3) eleggere il master del
  sistema Cerebromorphosis di Artemis (IT vs EN, md vs pdf); (4) sync
  della sezione Corona di `campaign-artifacts.md` (oggi ferma al pre-P3).
- **Accettazione**: regola dei 3 documenti rispettata per Corona, Aegis,
  Ring, Bracieri+Cintura, Collana; `grep` degli oggetti spesi (Rubino,
  Cuore di Moradin) = 0 usi attivi.

### T6c. 🔶 state.md §6 a due tempi (engine: **Opus 4.8**; arbitrati → **Fable**)
- **Evidenza**: nota [T4-a] della matrice — §0 al tavolo reale, §1/§6 allo
  stato preparato: ambiguo per chiunque prepari la sessione di stasera.
- **Azione**: proporre al DM la doppia colonna in §6 ("oggi al tavolo" /
  "preparato ARC-09") o due tabelle etichettate; applicare SOLO dopo
  conferma; changelog §8. 🔶 **Se emergono contraddizioni di canone**
  tra §6, i piani ARC e i master (es. poteri dei Rituali 3-4 della
  Corona), l'arbitrato multi-file è il caso speciale da dare a **Fable**:
  richiede di tenere insieme state.md + 3 piani + master artefatti senza
  perdere nessun vincolo.
- **Accettazione**: un lettore capisce da §6 cosa vale STASERA senza
  leggere [T4-a]; nessuna riga di storia riscritta.

### T7. Schede giocatore STATO-ATTUALE per tutti (engine: **Sonnet 5**)
- **Azione**: dal template T4, generare le schede per **Aegis Fang** (dal
  master T6b), **Ring** (dal Revised: poteri costanti+attivati, crisis
  powers SOLO lato DM), **Bracieri+Cintura** (allineare la
  `05_..._Scheda_PG_Completa.md` al formato, aggiungendo il registro
  sblocchi), **Collana** (dalla scheda Hella, con i 3 slot-dono e lo stato
  post-rituale che il tavolo produrrà). Due snapshot dove serve (come la
  Corona).
- **Accettazione**: ogni PG ha UNA scheda stampabile senza spoiler; le
  vecchie marcate SUPERATA; matrice aggiornata.

### T8. Convalida sinergie Collana dopo la quest di Hella (engine: **Sonnet 5**, al momento giusto)
- **Azione**: quando il tavolo gioca Foresta Sacra/slot-dono: spostare le
  [PROPOSTA] F1-F4 convalidate in §1 del file SINERGIE, aggiornare
  state.md §6 + scheda giocatore Hella, rigenerare HTML/PDF con nuova
  data-versione, changelog §8.
- **Accettazione**: zero [PROPOSTA] attive in §1; export sincronizzati.

### T9. Propagazione del ramo del rifiuto (engine: **Sonnet 5**)
- **Azione**: cross-link della tabella echi T1 nei file bersaglio
  (`ARC08-03-REGISTRO-PERDITE.md`, hooks ARC-09, DM-QUICKSTART-ARC09):
  una riga "se al rituale è successo X, qui vale Y" per ciascun eco;
  dopo che P3B è GIOCATO: registrare l'esito reale in state.md
  (changelog) e chiudere i rami non presi con banner "non accaduto".
- **Accettazione**: ogni eco della tabella ha il suo aggancio nel file
  bersaglio; nessun eco orfano.

---

## §4 — ORDINE DI ESECUZIONE, ENGINE E BUDGET

> **Criterio T-D5**: Sonnet 5 esegue ciò che è **meccanico e verificabile
> col grep** (rendering, banner, consolidamenti 1:1, cross-link); Opus 4.8
> ciò che **crea o bilancia** (tattiche nuove, fusioni di generazioni,
> statistiche, negoziazione col canone); **Fable non serve di norma** —
> riservarlo ai 🔶 (arbitrati di canone multi-file, tipo T6c se esplode).
> Regole anti-spreco identiche ai piani ARC: passare all'engine SOLO questo
> file + i file del lotto + state.md §0/§6 (+ template pertinente);
> niente riletture di interi archi; un lotto = un commit.

| Sessione | Task | Tipo | Engine | Dipendenze |
|---|---|---|---|---|
| 1 | **T1+T2+T3+T4** | fondazioni + esemplari | ✅ eseguito (Fable, sessione 2026-07-03) | — |
| 2 | T5a (rendering di massa + censimento) | esecutivo | **Sonnet 5** | T2 |
| 3 | T6a (igiene artefatti) | esecutivo | **Sonnet 5** | T4 |
| 4 | T5b (companion da consolidare — parti DA GIOCARE prima) | consolidamento | **Sonnet 5** | T3, T5a |
| 5 | T6b (consolidamenti Corona/Aegis/Cerebro + sync reference) | consolidamento pesante | **Opus 4.8** | T6a |
| 6 | T5c (companion generativi + griglia Campo Drow 2 + 0-byte) | generativo/bilanciamento | **Opus 4.8** | T5a, T5b |
| 7 | T7 (schede giocatore tutti i PG) | derivativo | **Sonnet 5** | T6b |
| 8 | T6c (state.md §6 due tempi) | canone, delicato | **Opus 4.8** → 🔶 Fable se conflitti | T6b; conferma DM |
| 9 | T9 (propagazione echi rifiuto) | cross-link | **Sonnet 5** | T1; (post-P3B giocato per la chiusura) |
| 10 | T8 (convalida sinergie Hella) | canone leggero | **Sonnet 5** | quest ARC-09 giocata; T-D4 |

## §5 — Checklist avanzamento

- [x] T1 · [x] T2 · [x] T3 · [x] T4 — **LOTTO T-A COMPLETO (2026-07-03)**
- [x] T5a (sessione 2, 2026-07-03) · [ ] T5b · [ ] T5c — lotto mappe
- [ ] T6a · [ ] T6b · [ ] T6c — lotto artefatti
- [ ] T7 · [ ] T8 · [ ] T9 — schede, sinergie, propagazione
- [x] T-D1…T-D5 — decisioni acquisite (2026-07-03); domande aperte:
  SOLO le conferme DM inline (T6c colonne §6; rimozione temporanei Word)

---

## §6 — GIUDIZIO SINTETICO (per il DM)

**Domanda 1 (risolta al 100% in T1)**: il rituale ora è una scena a
decisioni — default invariato per chi accetta, alternative per chi
negozia, conseguenze giocabili (mai punitive-morali: la resurrezione non è
in ostaggio) per chi rifiuta, e il rifiuto totale genera quest invece di
punizioni. Gli echi sono nel formato che ARC-09 già usa.

**Domanda 2 (fondazioni fatte, volume nei lotti)**: la filiera è
markdown-master → SVG generato → companion 3 blocchi. I 5 SVG esemplari
mostrano il punto d'arrivo: stesso stile per TUTTA la campagna, leggibile
da un umano, rigenerabile in un comando. Il grosso del lavoro restante è
meccanico (T5a/T5b, Sonnet) tranne le mappe senza tattiche (T5c, Opus).

**Domanda 3 (struttura fatta, consolidamenti nei lotti)**: la regola dei 3
documenti + la matrice rendono la Corona navigabile OGGI (il giocatore ha
la sua pagina, il DM il suo master, tutto il resto è censito). Il debito
residuo è la fusione dei near-dup (T6b) e l'ambiguità dei "due tempi" di
state.md (T6c) — quest'ultimo è l'unico punto dove potrebbe servire Fable.
Le sinergie di Hella esistono come [PROPOSTA] pronte da convalidare quando
lei, viva, si guadagna il suo posto nel cerchio — come chiesto.
