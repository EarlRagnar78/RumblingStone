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

### T5b. Companion per mappe CON tattiche esistenti (engine: **Sonnet 5**) — ✅ FATTO (mappe da giocare; sessioni 4+9, 2026-07-03/04)
- **Azione**: per le mappe che già hanno sezioni tattiche/statblock
  sparse (censimento T5a), riorganizzare nei 3 blocchi del template —
  SOLO consolidamento, zero invenzioni; aggiunte inevitabili flaggate
  [INFERRED]. Ordine: prima le mappe delle parti DA GIOCARE (P3B, P5,
  ARC-08 assedio, ARC-09 quest imminenti), poi il resto.
- **Fatto (sessione 4)**: le 2 mappe **ARC-09 quest imminenti** (Campo
  Drow 1 e 2, `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`) e la mappa
  canonica dell'**ARC-08 assedio** (`Hammerfist-L2-REVISED-Ultra-Clear.md`)
  hanno ora i 3 blocchi AMBIENTE/TATTICHE/EVOLUZIONE inline, consolidati
  dalle sezioni sparse preesistenti (Tattiche Raid/Sabotaggio, Posizioni
  PG, Distanze, Punti Deboli) — zero dati inventati, [INFERRED] sulle
  soglie di morale/evoluzione non esplicite nei file originali.
- **Fatto (sessione 9)**: aggiunti i 3 blocchi AMBIENTE/TATTICHE/EVOLUZIONE
  a tutte le mappe REVISED delle parti da giocare mancanti — **ARC-07 Forgia**:
  PF-1 Stanza della Corona (boss Belkram), PF-2 Sala della Forgia (hub
  rituale P4→P3B→P5), PF-3 Corridoio del Fuoco, PF-4 Forgia Adamantina (boss
  Elder Fire Elemental); **ARC-08**: Hammerfist-L1 (ricognizione/Torrione),
  Hammerfist-L3 (evacuazione/Passaggi Antichi). Consolidati dalle sezioni
  sparse (POSIZIONI/TATTICA/DISTANZE/HAZARD/LIGHTING), zero invenzioni,
  [INFERRED] sulle soglie non esplicite. Griglie/SVG invariati (validate_maps
  verde).
- **Non serve companion** (già hanno tattiche organizzate per mappa):
  `Portale-Forgia-L3-FINALE-REVISED.md` (Xorn Fauci di Diamante, skill
  challenge, Terros CR 16 — ha già SCHEMA TATTICO per mappa; il suo SVG
  manca solo per il formato a lettere, censito nota 2) e
  `Hammerfist-Lotto-3-FINALE.md` (SCHEMA TATTICO per ognuna delle 5 mappe,
  in gran parte doppioni delle REVISED già trattate).
- **Fuori priorità**: `Hammerfist-Lotto-1` (⚠️ DEPRECATED) e `Lotto-2`
  (variante della L2-REVISED già fatta) — non parti da giocare canoniche.
- **Accettazione** ✅ (per le mappe da giocare): checklist ①-⑦ del template
  soddisfatta su ogni mappa REVISED trattata; nessun dato nuovo non flaggato.

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
- **Stato (sessione 9)**: ⏳ **scoped/rinviato alle parti imminenti** (la
  regola T5c è "solo per le parti effettivamente imminenti al tavolo"; oggi
  il tavolo è ad **ARC-07 P4**, state.md §0). Punti chiusi/coperti:
  - **Parti imminenti (ARC-07/08)**: coperte da T5b (companion su tutte le
    REVISED da giocare); `Portale-Forgia-L3-FINALE` (Camera Sferica Boss /
    Terros CR 16, il climax P5) **ha già tattiche organizzate** — nessuna
    generazione necessaria, solo l'SVG manca per il formato a lettere
    (censito nota 2; riscrittura a griglia-emoji o estensione del parser
    resta opzionale).
  - **File 0-byte**: già risolto — `SUPPLEMENTO-P1C-...-Description.md` ha
    contenuto (censimento nota 7), riferimento nel piano superato.
  - **Griglia Campo Drow 2** ✅ **FATTA (sessione 10, 2026-07-04)**: era
    abbreviata (`[continues...]` + righe interne saltate); ora **completa** —
    53 righe, larghezza uniforme 65 colonne, strutture posizionate secondo le
    annotazioni (palizzata/cancelli/torretta/recinto ogre/tenda Wyrmlord/
    tesoro/prigioni), generata con script per uniformità, SVG rigenerato
    (validate_maps verde). ⚠️ Discrepanza dimensioni 65 col disegnate vs 80
    dichiarate flaggata `[needs DM confirmation]` nel sorgente (completata
    coerente con le posizioni, non allargata a foresta vuota).
  - **Rinviato (ARC-09 NON imminente)**: scrivere griglie/tattiche ex-novo per
    i **16 file narrativi ARC-09 P2/P3** (Torre, Torneo, Palio, Battaglia
    Finale FASE0-4, ecc.): lavoro generativo Opus da fare quando l'arco
    diventa imminente al tavolo, non ora (evita di generare in anticipo
    materiale che il DM potrebbe rimodellare). I companion di Campo Drow 1-2
    esistono già (T5b, PR#23).
- **Accettazione**: zero mappe senza companion **negli archi imminenti** (✅);
  il generativo ARC-09 non imminente è dichiaratamente rinviato; EL/CR
  dichiarati, esiti aperti (D13), [INFERRED] su ogni scelta di design.

## §3 — LOTTO T-C: Artefatti di tutti i PG (T6-T8) e propagazione rituale (T9)

### T6a. Igiene meccanica cartelle artefatti — ✅ FATTO (sessione 3, 2026-07-03)
- **Azione**: applicare i flag `[T6]` della matrice — banner 📸 sui 2 file
  Ring top-level; deprecare le copie html doppie della scheda Bracieri
  (`copy 2`, `Final`); `git mv` `Avvneture_per_nani.txt` (refuso);
  spostare/marcare il tooling locale di Tordek (`apply_styles.py` ecc.);
  chiedere al DM (flag, non agire) la rimozione dei temporanei Word.
- **Fatto**: banner 📸 aggiunti a `Ring of Chaotic Illumination.md` e
  `Ring_of_chaotic_illumination-master.md` (top-level, puntano al MASTER
  *Reforged*); banner 📸 in testa alle 2 copie HTML duplicate della scheda
  Bracieri (`... Final.html`, `... copy 2.html`); `Avvneture_per_nani.txt`
  (refuso, byte-identico al canonico) rinominato via `git mv` in
  `DEPRECATO-Avvneture_per_nani-refuso-duplicato.txt` con nota in testa;
  tooling locale di Tordek marcato in `README-tooling-locale.md` (path
  hardcoded alla macchina originale, non spostato in `scripts/` per non
  farlo passare per tool generico del repo); temporanei Word **non
  toccati** (restano flag `🗑️ in attesa di conferma DM`, coerente con la
  domanda aperta già in checklist §5). `ARTEFATTI-MATRICE-VERSIONI.md`
  aggiornata per ogni riga toccata. Zero contenuti narrativi/meccanici
  modificati.
- **Accettazione** ✅: ogni file della matrice ha lo stato che la matrice
  dichiara; matrice aggiornata; zero contenuti modificati.

### T6b. Consolidamenti Corona/Aegis/Cerebromorphosis — ✅ FATTO (sessioni 6-8, 2026-07-04)
- **Azione**: (1) fondere i near-dup Corona (`000_Corona_adamantio_ogetto`
  → assorbito nel master DM; eleggere una delle 2 `Schede_avvenimenti`);
  (2) estrarre il **master .md di Aegis Fang** dal docx/pdf (tabella di
  progressione inclusa: pre-risveglio → risveglio pieno post-Siege, fonte
  `05_Aegis_Fang_Final_Awakening.html`); (3) eleggere il master del
  sistema Cerebromorphosis di Artemis (IT vs EN, md vs pdf); (4) sync
  della sezione Corona di `campaign-artifacts.md` (oggi ferma al pre-P3).
- **Fatto (sessione 6)**:
  - **(2) Aegis Fang** ✅ — creato `00_Aegis_Fang-MASTER-DM.md` transcrivendo
    fedelmente il `.docx` (stadio base: +2 Returning Dwarven Waraxe
    *Dragondoom*, Ego 14, poteri inferiori) e `05_..._Final_Awakening.html`
    (Stadio 1, risveglio pieno post-Assedio: +4 Holy Returning, Ego 20,
    Ritornante inesorabile, Taglio del Cacciatore, Condotto Divino di
    Moradin). Tabella di progressione a 2 stadi; stato corrente = Stadio 0
    (state.md §6 conferma *pre-full-awakening*). Eco T9 «Filo dell'Ascia»
    riportato in § Costi. `[INFERRED]` su ogni mappatura SRD non esplicita.
    `.docx`/`.pdf` declassati a 📸 export storico. Matrice aggiornata.
  - **(3) Cerebromorphosis** ✅ — eletto `Italiano/cerebromorphosis_italian-final.md`
    come ⭐ MASTER (banner in testa); classificati gli altri: 📸 generazione
    inglese (`cerebromorphosis_system.md`, doppia byte-identica) · *annesso*
    il sottosistema party-intervention (`party_intervention_system.md`,
    `moradin_divine_guidance_italian.md`) · 📸 i PDF. Matrice §3 aggiornata.
- **Fatto (sessione 8) — Corona**:
  - **(1) near-dup**: `000_Corona_adamantio_ogetto.md` bannerato 📸 ASSORBITO
    nel master (il master prevale sui dati divergenti, es. prereq BAB);
    eletta `00_Schede_avvenimenti_...-ALT.md` (formulazione più chiara), la
    gemella 📸 SUPERATA. Matrice §1 aggiornata.
  - **Riconciliazione HTML gemme ↔ master/scheda**: aggiunto alla scheda
    giocatore il **+2 intuizione CA** di *Stone's Awareness* (era omesso;
    presente in master e HTML). **2 dubbi lasciati al DM** `[needs DM
    confirmation]` (banner nel master DM): Trappole↔Comprendere Linguaggi;
    Topazio 10 min↔1 ora. Resto coerente.
  - **(4) sync `campaign-artifacts.md`**: *Moradin's Insight* → "Active
    Powers" (Rituale 2 completato); +2 CA su *Stone's Awareness*; sblocchi
    corretti (Mantle = Rituale 3, aggiunta *Aura of the Eternal Forge* =
    Rituale 4) allineati al master. Matrice §7 marcata ✅.
- **Accettazione** ✅: regola dei 3 documenti rispettata per Corona, Aegis,
  Ring, Bracieri+Cintura, Collana; master eletto per Cerebromorphosis; `grep`
  oggetti spesi (Rubino, Cuore di Moradin) = **0 usi attivi**. Le poche
  divergenze HTML↔master irrisolvibili senza il DM sono flaggate, non
  indovinate.

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

### T7. Schede giocatore STATO-ATTUALE per tutti — ✅ FATTO (sessione 7, 2026-07-04)
- **Azione**: dal template T4, generare le schede per **Aegis Fang** (dal
  master T6b), **Ring** (dal Revised: poteri costanti+attivati, crisis
  powers SOLO lato DM), **Bracieri+Cintura** (allineare la
  `05_..._Scheda_PG_Completa.md` al formato, aggiungendo il registro
  sblocchi), **Collana** (dalla scheda Hella, con i 3 slot-dono e lo stato
  post-rituale che il tavolo produrrà). Due snapshot dove serve (come la
  Corona).
- **Fatto**:
  - **Aegis Fang** ✅ — `00_Aegis_Fang-SCHEDA-GIOCATORE-STATO-ATTUALE.md`
    (Stadio 0 pre-risveglio; Pagina 2 "Risveglio pieno" gated, non stampare
    prima dell'Assedio; conditional T9 «Filo dell'Ascia»).
  - **Ring** ✅ — `ringOfChaoticIllumination/00_Ring-SCHEDA-GIOCATORE-STATO-ATTUALE.md`
    (poteri costanti + 6 attivati in IT meccanico; **poteri di crisi tenuti
    lato DM**, solo accennati).
  - **Bracieri+Cintura** ✅ — `Tordek/05_..._Scheda_PG_Completa.md` allineata
    (banner STATO-ATTUALE + registro sblocchi; Cintura già integrata nel
    cheat sheet come «Cariche Devastazione»).
  - **Collana** ✅ — estratto l'handout standalone
    `Hella/00_Collana-SCHEDA-GIOCATORE-STATO-ATTUALE.md` dal file combinato
    (Radicata attuale = Pagina 1; Fiorita/Foresta-che-Cammina = Pagina 2
    gated ARC-09); il file combinato `01_...` resta master DM con banner
    «non consegnare al giocatore». Slot-dono legati al ramo del rifiuto (T9).
  Matrice §2-§5 aggiornata (una scheda giocatore per artefatto). Corona già
  aveva la sua da T4.
- **Riconciliazione HTML↔md (2026-07-04, richiesta DM)**: le schede HTML
  contengono le modifiche ai poteri avvenute durante la Forgia Eterna → i
  loro valori sono i validi. Controllate contro le `.md`:
  - **Bracieri** ⚠️→✅: l'handout `.md` aveva **RD 3** (obsoleto) mentre
    master `01_`, stadio `03_` e HTML danno **RD 5/adamantio** → corretto.
    Aggiunti dall'HTML (assenti dalla bozza `.md`): **Frantumare (Shatter)**
    1/giorno su critico e la **Benedizione della Forgia Eterna** (contatto
    con l'Altare del Cuore di Moradin → 3→**4 cariche**/giorno + carica
    gratis su 18-20), già confermata in `00_Cintura_della_Devastazione.md`.
    Ricarica allineata ad "alba/8h" (HTML). `[dubbio → DM]`: durata della
    Benedizione ("fino a fine avventura" = solo ARC-07 o campagna intera?).
  - **Ring** ✅: HTML = export della `.md` Revised (numeri identici), nessuna
    variazione.
  - **Aegis** ✅: le modifiche dell'HTML (`05_..._Final_Awakening`) sono lo
    **Stadio 1** post-Assedio (P5), già gated in Pagina 2 e nel master;
    coerente con state.md §6 (*pre-full-awakening*). `[dubbio → DM]`: se il
    DM ritiene l'Assedio già avvenuto, promuovere allo Stadio 1.
  - **Corona** ⏳: le schede HTML `02_/03_ Gemme` sono stati futuri; la loro
    riconciliazione col master DM rientra nel **T6b residuo** (near-dup
    Corona + sync `campaign-artifacts.md`) — vedi §T6b.
- **Accettazione** ✅: ogni PG ha UNA scheda stampabile senza spoiler (gli
  stadi futuri/crisi sono su pagine gated o lato DM); valori allineati alle
  schede HTML della Forgia dove differivano; dubbi marcati `[needs DM
  confirmation]`; matrice aggiornata.

### T8. Convalida sinergie Collana dopo la quest di Hella (engine: **Sonnet 5**, al momento giusto)
- **Azione**: quando il tavolo gioca Foresta Sacra/slot-dono: spostare le
  [PROPOSTA] F1-F4 convalidate in §1 del file SINERGIE, aggiornare
  state.md §6 + scheda giocatore Hella, rigenerare HTML/PDF con nuova
  data-versione, changelog §8.
- **Accettazione**: zero [PROPOSTA] attive in §1; export sincronizzati.

### T9. Propagazione del ramo del rifiuto — ✅ FATTO (parte cross-link)
- **Azione**: cross-link della tabella echi T1 nei file bersaglio
  (`ARC08-03-REGISTRO-PERDITE.md`, hooks ARC-09, DM-QUICKSTART-ARC09):
  una riga "se al rituale è successo X, qui vale Y" per ciascun eco;
  dopo che P3B è GIOCATO: registrare l'esito reale in state.md
  (changelog) e chiudere i rami non presi con banner "non accaduto".
- **Fatto**: tutti e **5 gli echi** della tabella T1 hanno ora un box
  «↩ Eco/i del rituale P3B (T9)» nel file bersaglio, con default esplicito
  (rituale non giocato = doni pieni, nessun eco attivo) e link alla fonte
  (§2-BIS): (1) Thorik/sangue + (3) Artemis/scintilla →
  `08_.../ARC08-03-REGISTRO-PERDITE.md`; (2) Tordek/respiro →
  `09_.../...FASE0-NOTTE-DEI-DROW-TESTO.md`; (4) Rifiuto totale/slot-dono →
  `09_.../Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md` §2 + cross-link
  §9; (5) Filo dell'Ascia/Aegis Fang → `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md`
  §2 (l'ancora della cartella Aegis Fang, in attesa del master `.md` T6b).
  Aggiunto anche un carry-over nell'intestazione di `DM-QUICKSTART-ARC09.md`.
  Path verificati (tutti risolvono); nessuna meccanica nuova (solo puntatori
  agli effetti già scritti nella tabella T1).
- **Resta da fare** (gated, post-gioco): quando P3B è GIOCATO al tavolo,
  registrare l'esito reale in `state.md` §8 (changelog) e chiudere i rami
  non presi con banner "non accaduto". Non eseguibile finché il rituale non
  è giocato (regola d'oro §0.1: mai riscrivere la storia in avanti).
- **Accettazione** ✅ (parte cross-link): ogni eco della tabella ha il suo
  aggancio nel file bersaglio; nessun eco orfano.

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
- [x] T5a (sessione 2) · [x] T5b (sessioni 4+9: companion su tutte le mappe REVISED da giocare — ARC-07 PF-1..4, ARC-08 L1/L2/L3, ARC-09 Campo Drow 1-2) · ⏳ T5c rinviato alle parti imminenti (generativo ARC-09 non imminente; tavolo ad ARC-07 P4) — lotto mappe
- [x] T6a (sessione 3, 2026-07-03) · [x] T6b (sessioni 6-8, 2026-07-04: Aegis master + Cerebro eletto + Corona consolidata/riconciliata + campaign-artifacts sync) · [ ] T6c (gated: conferma DM) — lotto artefatti
- [x] T7 (sessione 7, 2026-07-04: schede Aegis/Ring/Bracieri/Collana) · [ ] T8 (gated: quest ARC-09 giocata) · [x] T9 cross-link (sessione 5, 2026-07-04; chiusura post-gioco P3B ancora gated) — schede, sinergie, propagazione
- [x] T-D1…T-D5 — decisioni acquisite (2026-07-03); domande aperte:
  SOLO le conferme DM inline (T6c colonne §6; rimozione temporanei Word)

### Infrastruttura CI (a supporto del lotto mappe)

- [x] **`scripts/validate_maps.py`** + step in `.github/workflows/ci.yml`
  (sessione 5, 2026-07-04): gate che fa rispettare in CI la regola d'oro
  §0.6 (griglia markdown = MASTER, SVG in `rendered/` = artefatti generati,
  mai a mano). Controlla, ad ogni push/PR: ogni `**/rendered/*.svg` è XML
  ben formato con radice `<svg>`; ogni SVG risale a un master `<stem>.md`
  (niente orfani); il re-render in memoria di ogni master riproduce
  byte-identici gli SVG committati (intercetta master modificati senza
  rigenerare o SVG editati a mano); rendering deterministico. Aggiunto anche
  `render_map_svg.py --help` allo smoke test dei tool DM. Così i lotti T5b/T5c
  che aggiungono mappe sono protetti da regressioni: chi tocca un master e
  dimentica `python3 scripts/render_map_svg.py <file>` rompe la CI.

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
