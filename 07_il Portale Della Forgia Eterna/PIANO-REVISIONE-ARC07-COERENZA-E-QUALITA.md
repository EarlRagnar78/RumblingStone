# PIANO DI REVISIONE ARC-07 (Il Portale della Forgia Eterna) — Coerenza & Qualità

> **Versione**: v1.1 (2026-07-02) — prodotto da audit completo dell'arco,
> esteso ad artefatti (`PG/Artefatti/`) e PNG su richiesta del DM. Le
> risposte DM del 2026-07-02 (Skullcrusher; 1000 anni prima; party al 13°;
> Hella morta nell'ARC-06; viaggio dello spirito già giocato) sono
> incorporate come decisioni D6-D9.
> **Scopo**: documento **autocontenuto** da dare in pasto a un engine AI
> specializzato (o a più sessioni brevi) per eseguire le correzioni **a lotti**,
> senza dover ri-derivare il contesto ogni volta. Ogni task ha: file coinvolti,
> problema con evidenza (file:riga), azione richiesta, criterio di accettazione.
> **Gemelli metodologici**: `09_Continuazione.../PIANO-REVISIONE-ARC09-...md`
> (eseguito) e `08_La Battaglia Di Hammerfist/PIANO-REVISIONE-ARC08-...md` (v2)
> — i tre piani condividono regole d'oro e formato; i punti di contatto
> ARC-07↔ARC-08 sono marcati **[CROSS-ARC]**.
> **Benchmark di qualità**: (interno) `PortaleForgia-P5-DEFINITIVO-PARTE2.md`
> per scrittura delle scene, `Terros.md` per metodo di ricalibrazione;
> (esterno) *Red Hand of Doom* (Jacobs/Wyatt 2006), moduli planari 3.5,
> AP Paizo PF1e per contingenze e handout.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

0. **REGOLA ZERO — QUESTO ARCO È GIOCATO A METÀ.** Il tavolo è dentro
   l'arco: **P1-P2 (Sala della Forgia) e P3 (Piano del Fuoco) sono giocati**;
   il **P4 (Piano della Terra) è IN CORSO**; devono ancora essere giocati:
   il **P3B (resurrezione di Hella)**, il **P5 (viaggio temporale all'assedio
   di Hammerfist dell'Anno −1000, da giocare VELOCE — decisione DM D1)** e il
   raccordo verso l'Arco 08. Quindi: per le parti giocate vale la regola
   dell'arco giocato (i fatti del tavolo sono immutabili, i file li devono
   raccontare — ma i fatti vanno **raccolti dal DM**, non dedotti); per le
   parti future vale la regola pre-gioco (esiti aperti ai dadi, contingenze).
   Ogni fatto di tavolo non documentato va marcato
   `[INFERRED — needs DM confirmation]`.
1. **`campaign/state.md` vince** su qualunque altro file — MA state.md è
   scritto in avanti rispetto al tavolo (segna concluso perfino questo arco):
   il task **A0 del piano ARC-08** lo corregge; questo piano lo assume
   eseguito (se non lo è, eseguirlo per primo da lì). Ogni modifica di canone
   va **appesa al changelog** di state.md.
2. **Sistema D&D 3.5 SRD only** — niente 5e, niente lore FR post-1385 DR.
   Ambientazione Faerûn 1372 DR (più il viaggio temporale a **1.000 anni
   prima, ≈372 DR** — D7).
3. **Mai inventare** stat, poteri di artefatti o fatti di sessione: flag
   `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare
   `skills/rumblingstone-campaign/references/campaign-artifacts.md`,
   `campaign/state.md` §6 e i PDF dell'arco
   (`SinergieArteFattiQuickReference.pdf`, `BenedizioniDiMoradin.pdf`).
6. Le mappe tattiche usano scala **1,5 m/quadretto** (già rispettata da
   `Mappe/TACTICAL-GRIDS-COMPLETE.md` r.8-9 — mantenerla).
7. Lingua: **italiano**, nomi meccanici 3.5 in italiano (CD non DC, Osservare
   non Spot). I file oggi in inglese (Terros, TACTICAL-GRIDS) vanno
   uniformati almeno nei termini meccanici.
8. **Non cancellare file** senza decisione esplicita (Q4): default = banner
   `> ⚠️ DEPRECATED (2026-07): ...` in testa.

### Stato GIOCATO / DA GIOCARE (fonte: DM 2026-07-02)

| # | Elemento | Stato |
|---|---|---|
| G0 | **Hella Oakenshield è MORTA nell'ARC-06** (Stanza della Corona): uccisa nello scontro con le **Yochlol half-illithid mandate da Sonjak** per prendere la Corona (Urialle CR 14, EL 17 — `06_.../villans.md`); il **vecchio portatore Belkram**, dominato e maledetto dai drow (morte negata, stato di maledizione), si è **ravveduto nel momento della sua morte definitiva**. Già canone scritto: coherence.md r.47 ("Hella dies in Crown Chamber, 06"), campaign-history.md r.26. **L'intero ARC-07 esiste per rendere epica la sua resurrezione** | ✅ giocato (ARC-06) — DM 2026-07-02 |
| G1 | P1-P2: ingresso e Sala della Forgia Eterna (affreschi, prove); il corpo di Hella è custodito nella Sala (da Therysol — history r.176) | ✅ giocato — fatti da raccogliere (B1) |
| G2 | P3: Piano del Fuoco — Topazio del Tempo recuperato | ✅ giocato |
| G2b | **Il viaggio dello spirito di Hella nell'Incudine del Mondo è GIÀ GIOCATO** (le prove dello spirito): esiste un file col **risultato del viaggio** — individuarlo e collegarlo (B9); i file di design sono i fusi `P4-...-HELLA-IL-VIAGGIO...` v1/v2 | ✅ giocato — DM 2026-07-02 |
| G3 | P4: Piano della Terra — **IN CORSO al tavolo** (Smeraldo della Forza in palio; boss Terros/Mithral Golem; Therysol PNG di supporto) | 🟡 in corso |
| G4 | P3B: rituale di resurrezione di Hella (il corpo + lo spirito provato dal viaggio) — si gioca **dopo la Terra** (D2), nonostante la numerazione "3B" | ⬜ da giocare |
| G5 | P5: viaggio temporale, assedio di Hammerfist di **1.000 anni prima** (D7), antenato di Fauci di Palude — **da giocare in modo VELOCE** (D1) | ⬜ da giocare |
| G6 | P6/raccordo: ritorno al 1372 e transizione verso l'Arco 08 | ⬜ da giocare (sezione 1372 di P6 superata da ARC-08: vedi A3) |

### Decisioni di canone GIÀ PRESE (applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | **Il viaggio temporale (P5) si gioca in maniera VELOCE**: una sessione cinematografica, non un dungeon completo. Il materiale lungo (DEFINITIVO ×2) resta come annesso; il formato da tavolo è il fast-play di B3 | DM 2026-07-02 |
| D2 | **Ordine di gioco**: P4 Terra (in corso) → P3B resurrezione di Hella → P5 viaggio Anno −1000 → raccordo → Arco 08. Coerente con D8 del piano ARC-08 (resurrezione tra Forgia e Hammerfist) | DM 2026-07-02 |
| D3 | Il nemico del viaggio è **l'antenato di Fauci di Palude** all'assedio antico di Hammerfist; l'esito del duello alimenta il ponte meccanico verso l'Arco 08 ("la Forgia ricorda le ferite", B4) **[CROSS-ARC]** | DM 2026-07-02; P5-DEFINITIVO-PARTE2 r.285 |
| D4 | **La struttura a due tempi dell'Arco 08 resta ad ARC-08**: il prequel coi pregen "Eroi di Hammerfist" (settimane prima) e l'arrivo dei Rumbling Stones quasi alla fine come artefici della riscossa vivono nei file ARC-08; la sezione "Anno 1372" di P6 è la bozza storica di quell'idea (vedi A3) | DM 2026-07-02; piano ARC-08 D6 |
| D5 | Il portale temporale si apre con **Topazio + Smeraldo** (le prime due gemme); il **Rubino** non apre nulla: si accende ALLA FINE del viaggio come "Cuore della Leggenda" (terza gemma) | P5-RICALIBRATO r.19-21; P5-DEFINITIVO-PARTE2 §4.2 r.328-371 — le due generazioni recenti concordano; P2 va corretto (A4) |
| D6 | **L'antenato di Fauci di Palude si chiama SKULLCRUSHER** (ex-Q1). "Skulldark" e "Infernotooth Giovane" vanno sostituiti (o dichiarati epiteti una-tantum nel master P5) | DM 2026-07-02 (risposta diretta) |
| D7 | **La battaglia antica è 1.000 ANNI PRIMA** (≈ 372 DR), NON Anno −1000 DR (ex-Q2): l'etichetta "Anno −1000" nei file va reinterpretata/normalizzata come "1.000 anni prima (≈372 DR)" — e la riga "2.372 anni dopo" (P5-DEFINITIVO-PARTE2 r.283), il "500 anni fa" (P6 r.350) e i "millenni fa" (P2 r.1119) vanno tutti corretti a 1.000 anni | DM 2026-07-02 (risposta diretta) |
| D8 | **Il party reale è ORA di livello 13** (ex-Q3). Stato artefatti al tavolo: **Bracieri Gemelli di Tordek RISVEGLIATI** (Fuoco+Terra), **Corona di Adamantio IN RISVEGLIO attraverso i viaggi temporali**, Aegis Fang pre-risveglio pieno, Anello riforgiato alla Forgia. Le parti future si bilanciano su APL 13 (metodo Terros: −1 con 3 PG finché Hella non torna) | DM 2026-07-02 (risposta diretta); state.md §6 (quadro forward-written da riallineare con A0) |
| D9 | **Fonte canonica degli artefatti = `PG/Artefatti/`** (LaCorona_di_Adamantio-DM.md, cartelle per PG). Le copie altrove (es. la cartella Corona dentro l'ARC-06) sono snapshot storici da marcare | DM 2026-07-02 ("controlla anche gli artefatti"); struttura repo |

### Decisioni di canone da chiedere al DM (bloccano solo i task marcati)

| # | Domanda | Proposta di default |
|---|---|---|
| Q4 | **File ridondanti/meta: deprecare o eliminare?** Riguarda le generazioni doppione (A6), il file vuoto e `temp_sinergie.txt` (A7) | **Deprecare con banner**, mai eliminare (§0.8). `temp_sinergie.txt` è l'unico candidato a rimozione fisica (è un temporaneo del PDF): chiedere conferma |
| Q5 | **Cognome di Hella**: il DM scrive "Oakshield", campaign-history.md r.26 scrive "**Oakenshield**" | Tenere **Oakenshield** (forma già scritta nel canone) salvo diversa indicazione; nessun find/replace fino a conferma |
| Q6 | **Qual è il file col RISULTATO del viaggio dello spirito di Hella?** Il DM conferma che esiste, ma la ricerca (`grep "Incudine del Mondo"`) trova solo i file di design (fusi v1/v2) e il lore della Corona | Farselo indicare dal DM e collegarlo in B9; candidati: il fuso v2 (se annotato post-sessione) o un file fuori dall'arco non ancora individuato |

> **Nota risoluzioni**: le ex-Q1/Q2/Q3 della v1 sono diventate D6/D7/D8
> (risposte DM 2026-07-02). I task A1, A2, A5 non sono più bloccati.

---

## §1 — LOTTO A: Incoerenze di canone e igiene dei file (priorità P0)

### A1. L'antenato con tre nomi — applicare D6 (Skullcrusher)
- **Problema**: il boss del P5 (che il tavolo giocherà a breve, D1) cambia
  nome a seconda del file aperto — **Skulldark** (P5-DEFINITIVO ×20,
  P5-RICALIBRATO), **Skullcrusher** (FINAL-P5, P6 ×10, TACTICAL-GRIDS,
  CORREZIONE-Boss-Fauci), **Infernotooth Giovane** (P1 r.747, P2 r.1119) —
  e `PortaleForgia-P5-DEFINITIVO-PARTE1.md` r.229 usa due nomi nella stessa
  riga.
- **Azione**: applicare **D6**: Skullcrusher in tutti i file dell'arco (P1,
  P2, FINAL-P5, DEFINITIVO ×2, RICALIBRATO, P6, CORREZIONE, TACTICAL-GRIDS);
  se si mantiene un epiteto ("il Nero"), dichiararlo alla prima occorrenza
  del master P5. Riga di changelog in state.md (il nome entra nel canone:
  l'Arco 08 lo eredita nel ponte B4).
- **Accettazione**: `grep -rn "Skulldark\|Infernotooth"` = 0 fuori da banner
  e note storiche; un solo nome (+epiteto dichiarato) ovunque.

### A2. Profondità temporale — applicare D7 (1.000 anni prima, ≈372 DR)
- **Problema**: i file dicono quattro cose diverse: "Anno −1000" come data
  assoluta DR con "2.372 anni dopo" (P5-DEFINITIVO-PARTE2 r.283), "500 anni
  fa" (P6 r.350, canto di Aegis Fang), "millenni fa" (P2 r.1119), e il
  canone deciso dal DM è **1.000 anni prima** (D7).
- **Azione**: applicare **D7**: la battaglia antica è 1.000 anni prima del
  1372 DR (≈ 372 DR). Normalizzare l'etichetta "Anno −1000" (titoli e testo
  di P5/P6/P2, state.md §6 che dice "year -1000 battle") in "1.000 anni
  prima (≈372 DR)" — o mantenere "Anno −1000" SOLO se ridefinito
  esplicitamente come conteggio relativo nanico, una volta, nel master P5;
  correggere r.283 ("2.372 anni dopo" → "1.000 anni dopo"), P6 r.350, P2
  r.1119; uniformare la genealogia del drago (antenato → Fauci: quante
  generazioni in 1.000 anni, detto una sola volta) e la collocazione di
  **Thorgrim Barbadiferro** (P1 r.704-751, P2 r.858, P5, P6 r.977).
- **Accettazione**: una sola profondità temporale (1.000 anni) e una sola
  genealogia in tutto il repo; changelog in state.md (il §6 cita la data).

### A3. P6 contiene una "battaglia finale 1372" superata dagli Archi 08-09 — [CROSS-ARC]
- **Problema** (il più importante dell'arco): `Portaleforgia-P6-INTEGRAZIONE-Completa.md`
  fu scritto quando la campagna doveva FINIRE qui: la sezione "ANNO 1372:
  BATTAGLIA FINALE HAMMERFIST" (r.598-946) mette in scena la battaglia di
  Hammerfist con **Fauci di Palude a GS 12** (r.813 "CR 12 vs Party 14"),
  lo dà **"Morto"** a esito fisso (r.869), e chiude con "🏁 FINE CAMPAGNA —
  OPZIONI FUTURE" (r.947) e un "PARTE 7 PREVIEW" (r.853). Tutto questo è
  superato: la battaglia di Hammerfist è ora **l'Arco 08 intero** (Fauci
  GS 15, esiti a rami — piano ARC-08 Q1/E-table), seguito dall'Arco 09.
  `CORREZIONE-Boss-Fauci.md` r.16 mantiene però il doppio profilo
  "GS 15 (Anno 1372), GS 12 versione Parte 6", perpetuando l'ambiguità.
- **Azione**: (1) banner DEPRECATED sulla sezione 1372 di P6 (non sul file
  intero: la sezione "ANNO −1000: BATTAGLIA FINO ALL'ALBA" r.9-597 resta
  materiale vivo del P5) con puntatore all'Arco 08; (2) **estrarre ciò che
  sopravvive** e ricollocarlo: la regia dell'"arrivo dei Rumbling Stones
  quasi alla fine" (r.621-753) è l'origine dichiarata di E6/D6 del piano
  ARC-08 — va citata lì come fonte, non doppiata; l'hook dell'**uovo di
  Fauci** (r.958) va in C3; il canto di Aegis Fang "sangue Skullcrusher"
  (r.746) va nel ponte B4; (3) correggere CORREZIONE-Boss-Fauci: il profilo
  GS 12 va marcato "versione storica P6, superata — a Hammerfist 1372 vale
  il GS 15 dei file ARC-08"; (4) verificare che nessun altro file punti alla
  "Parte 7".
- **Accettazione**: un lettore che apre P6 capisce subito cosa è vivo (Anno
  −1000) e cosa è storia di progetto (1372); un solo profilo di Fauci di
  Palude per il 1372 in tutto il repo; zero riferimenti attivi a "Parte 7"
  o "fine campagna".

### A4. Quale gemma apre il portale temporale — applicare D5
- **Problema**: `PortaleForgia-P2-REVISED-Corretta-PARTE1.md` r.1007 promette
  "Quando Rubino attiva → 100% + portale aperto Anno −1000" e r.1072
  attribuisce il viaggio al Rubino; ma il design recente (D5) fa aprire il
  portale a **Topazio + Smeraldo** (P5-RICALIBRATO r.19-21) e accende il
  **Rubino solo alla fine del viaggio** come Cuore della Leggenda
  (P5-DEFINITIVO-PARTE2 §4.2). Il Rubino ha anche un'eco morale ("nessuna
  pietà", r.167) che il P2 ignora.
- **Azione**: correggere la tabella affreschi/attivazioni di P2 (r.982-1007,
  r.1072) al modello D5; verificare la coerenza con
  `LaCorona_di_Adamantio-DM.md` (citato da P5-DEFINITIVO-PARTE2 r.361) e con
  `campaign-artifacts.md`/state.md §6 (il piano ARC-09 C4 tratta già il
  "Rubino Corona" come single-use SPESO dopo questo arco: la catena
  P5→ARC-09 deve tornare). Nota di changelog se il canone artefatti cambia.
- **Accettazione**: una sola sequenza di attivazione delle 3 gemme in tutto
  il repo; la Corona arriva all'ARC-08/09 nello stato che ARC-09 assume.

### A5. Livello del party dichiarato: 12 vs 13 vs 14 "God Mode" — applicare D8 (livello 13)
- **Problema**: le dichiarazioni cambiano da file a file (P3B "livello 13",
  La_Piramide "Livello 13", P5-RICALIBRATO "Livello 14+ (God Mode)", P6
  "Party 14", Terros "Party Level 14... effective APL 13"), mentre state.md
  §0 assegna all'arco il livello 12. Il canone deciso (D8) è: **party al
  13°**. Per le parti ancora da giocare (P3B, P5) il numero sbagliato =
  incontri sbagliati.
- **Azione**: applicare **D8**: uniformare le intestazioni di TUTTI i file
  dell'arco a "13°" e ricontrollare i budget GS delle parti future col
  metodo di Terros (APL effettivo 12 con 3 PG finché Hella non torna;
  +Therysol come supporto; APL 13 pieno dal P5 con Hella "DMPC completa").
  Annotare lo stato artefatti D8 (Bracieri risvegliati, Corona in risveglio)
  nelle intestazioni dei master, perché è ciò che giustifica gli EL alti
  (l'EL 17 dell'ARC-06 contro un party di 13° era già questo pattern).
  Le parti già giocate NON si ribilanciano: si annota il livello a cui
  furono giocate. Propagare il 13° a state.md §0 (via A0) e segnalare la
  **cascata sui piani a valle**: ARC-08 assumeva ingresso al 12° (suo E4) —
  vedi Q6 del piano ARC-08.
- **Accettazione**: una sola dichiarazione di livello per parte; budget GS
  delle parti future ricalcolati; cascata ARC-08/09 registrata nei
  rispettivi piani.

### A6. Generazioni multiple mai riconciliate (P3B ×2, P4 ×4, P5 ×4 + 3 doc di ricalibrazione)
- **Problema**: come ARC-08 A8, ma qui pesa di più perché **il tavolo ci sta
  giocando dentro**: P5 esiste in 4 versioni (`FINAL-P5`, `DEFINITIVO-PARTE1`,
  `DEFINITIVO-PARTE2`, `RICALIBRATO`) con nomi del boss diversi (A1); P4 in 4
  (`COMPLETO-alternative`, `RICALIBRATO`, `HELLA-IL-VIAGGIO...` v1 e v2); P3B
  in 2 (`COMPLETO`, `RICALIBRATO-alternative`); e tre documenti di
  ricalibrazione (`La_Piramide_Ricalibrata` = finale P3, `RicalibrazioneScontriPianoDelFuoco`,
  `Terros`) correggono i file-base senza che i file-base lo dichiarino.
- **Azione**: (1) matrice contenuto × versione (quale generazione è più
  recente/completa, cosa aggiunge ognuna); (2) eleggere UN master per parte
  — proposta: per le parti GIOCATE il master è la versione effettivamente
  usata al tavolo `[needs DM confirmation]`; per P3B e P5 (future) il master
  è l'ultima generazione (RICALIBRATO / DEFINITIVO) integrata con le
  ricalibrazioni; (3) banner sugli altri + puntatore; (4) nei master,
  banner inverso: "ricalibrato da: Terros.md / La_Piramide / Ricalibrazione..."
  così la catena è esplicita.
- **Accettazione**: un master per parte; ogni doc di ricalibrazione è
  citato dal master che corregge; zero versioni "orfane" senza stato.

### A7. Igiene: file vuoto, file temporaneo, coda AI, nomi file rotti
- **Problema**: `Mappe/Atlante-Visivo-Mappe.md` è **0 byte**;
  `temp_sinergie.txt` è un temporaneo (il contenuto vive in
  `SinergieArteFattiQuickReference.pdf`); `RicalibrazioneScontriPianoDelFuoco.md`
  apre con coda conversazionale AI ("Perfetto! Ora ho tutti i dettagli
  necessari..."); il filename `PortaleForgia-P4-PianoTerra-P3B-HELLA-IL-VIAGGIO-NELL'INCUDINE-DEL- MONDO.md`
  contiene **uno spazio dopo "DEL-"** e un apostrofo (fragile per script e
  link); `Portaleforgia-P6-...` ha la F minuscola contro la convenzione
  `PortaleForgia-*` di tutti gli altri.
- **Azione**: riempire o deprecare il file vuoto (l'indice-mappe vero nasce
  in B8/C1); rimuovere `temp_sinergie.txt` previa conferma (Q4); ripulire la
  coda AI sostituendola con header di stato; `git mv` dei filename rotti
  (spazio, apostrofo, casing) aggiornando i riferimenti repo-wide.
- **Accettazione**: zero file 0-byte, zero `temp_*`, zero code AI; nessun
  filename con spazi interni anomali; link tutti validi.

### A8. Terminologia: 53 `DC` inglesi + file interamente in inglese
- **Problema**: 53 occorrenze di `DC n` contro la convenzione CD (§0.7);
  `Terros.md` e `Mappe/TACTICAL-GRIDS-COMPLETE.md` sono in inglese
  (quest'ultimo va bene come specifica tecnica, ma i termini meccanici che
  il DM legge al tavolo devono essere 3.5-italiano come nel resto del repo).
- **Azione**: DC→CD globale; skill in italiano 3.5; per Terros e
  TACTICAL-GRIDS tradurre almeno intestazioni di scena, nomi di prova e
  condizioni (il corpo tecnico può restare in inglese con nota).
- **Accettazione**: `grep -rn "DC [0-9]"` = 0 nell'arco; le prove al tavolo
  sono leggibili in italiano.

### A9. Numerazione fuori ordine: P3B si gioca dopo P4 — applicare D2
- **Problema**: la sigla "P3B" (resurrezione) precede "P4" (Terra), ma
  l'ordine di gioco deciso (D2) è Terra → resurrezione → viaggio. I file
  fusi `P4-PianoTerra-P3B-HELLA-IL-VIAGGIO...` (v1/v2) testimoniano
  l'intreccio (lo spirito di Hella viaggia nell'Incudine del Mondo MENTRE il
  party attraversa la Terra) ma nessun file dichiara l'ordine al lettore.
- **Azione**: dichiarare l'ordine di gioco D2 in testa ai master di P3B, P4
  e P5 (una riga: "si gioca dopo/prima di..."); nell'INDICE (B8) la tabella
  delle parti segue l'ordine di GIOCO, con nota sulla numerazione storica.
  Non rinumerare i file (troppi riferimenti): basta dichiararlo.
- **Accettazione**: nessun lettore può sbagliare l'ordine; INDICE coerente
  con D2 e col piano ARC-08 (D8).

### A10. Artefatti: fonte unica, cartelle duplicate e divergenti, generazioni — applicare D9
- **Problema** (dall'audit artefatti richiesto dal DM): (1) la cartella
  `00-La Corona di Adamantio-ogetto&Prove/` esiste **in due copie
  divergenti** — dentro l'ARC-06 e dentro `PG/Artefatti/Artefatti-Pg/` —
  con set di file diversi e file omonimi dal contenuto diverso
  (`00_corona_di_adamantio_completa_italiano.md` differisce; la copia PG ha
  in più le schede Fase 2 e gli HTML `01/02/03_Corona_N_Gemme`); (2)
  `PG/Artefatti/LaCorona_di_Adamantio-DM.md` apre con residuo di
  conversione ("OnlineMarkdown.com https://onlinemarkdown.com/"); (3) il
  Ring of Chaotic Illumination ha 3 generazioni (`Ring of Chaotic
  Illumination.md`, `Ring_of_chaotic_illumination-master.md`, cartella
  `ringOfChaoticIllumination/` con Revised + `Old/`); (4) refusi nei nomi
  file (`achede _avveimenti_corona_diAdamantio.md` — spazio interno e
  refuso doppio).
- **Azione**: applicare **D9**: `PG/Artefatti/` è la fonte canonica —
  riconciliare le due cartelle Corona (portare in PG ciò che l'ARC-06 ha in
  più, poi banner "snapshot storico — canonico in PG/Artefatti" sulla copia
  ARC-06); eleggere il master del Ring (proposta: `..._Revised.md`, con
  `Old/` e i file sciolti marcati); ripulire il residuo OnlineMarkdown;
  `git mv` dei filename con refusi; verificare che lo stato dichiarato nei
  master corrisponda a D8 (Bracieri Fuoco+Terra ✅; Corona: gemme accese =
  quelle realmente giocate, non le 3 del §6 forward-written) e che i
  puntatori di state.md §6 e `campaign-artifacts.md` risolvano sui master.
- **Accettazione**: un solo file canonico per artefatto; le copie marcate;
  `grep -rn "OnlineMarkdown"` = 0; stato gemme/bracieri coerente col tavolo
  in tutto il repo.

---

## §2 — LOTTO B: Completamento contenuti per il gioco (priorità P1)

> Metà arco è dietro il tavolo, metà davanti: il lotto B serve entrambe —
> memoria per ciò che è stato giocato, preparazione per P3B/P5/raccordo.

### B1. Session log delle sessioni REALMENTE giocate (ARC-06 finale → P4 in corso)
- **Evidenza**: `campaign/sessions/` non ha alcun log del giocato reale
  (contiene solo il log anticipato/fittizio del 2026-05-03, vedi ARC-08 A0).
  La **morte di Hella** è fissata come evento (coherence r.47: Crown
  Chamber, ARC-06) ma la sessione che l'ha prodotta non ha log — e nemmeno
  le sessioni della Forgia (P1-P3, viaggio dello spirito G2b, P4 in corso).
- **Azione**: intervista breve al DM (o note sue) → log retroattivi nel
  formato AGENTS.md (Summary / Key decisions / XP / Loot / Next hooks) per:
  (1) il finale dell'ARC-06 (lo scontro della Stanza della Corona: Urialle
  e le Yochlol half-illithid, la morte di Hella, la redenzione di Belkram
  in punto di morte — G0); (2) ingresso+Sala Forgia; (3) Piano del Fuoco
  (Topazio); (4) il viaggio dello spirito di Hella (G2b — qui si aggancia
  il file-risultato di Q6/B9); (5) Piano della Terra fin dove è arrivato.
  OGNI lacuna → `[INFERRED — needs DM confirmation]`. Aggiornare il
  cruscotto post-A0 di state.md man mano.
- **Accettazione**: ogni sessione giocata ha un log; la morte di Hella ha
  data, luogo e causa canoniche IN un log (non solo nella tabella eventi);
  zero invenzioni non flaggate.

### B2. Master della resurrezione di Hella (P3B) — [CROSS-ARC]
- **Evidenza**: esistono `P3B-ResurrezioneHella-COMPLETO.md` (22 KB) e
  `P3B-...-RICALIBRATO-alternative.md` (4,7 KB) più i due file fusi P4+P3B
  (34 e 44 KB): quattro trattamenti della stessa scena-cardine, nessuno
  eletto. Il piano ARC-08 (B2) costruisce il suo "ponte 07→08" ASSUMENDO che
  la scena viva qui: serve un puntatore stabile.
- **Azione**: eleggere il master (proposta: il fuso v2, che integra il
  viaggio dello spirito nell'Incudine, con la parte rituale del COMPLETO;
  `[needs DM]`), applicare A5 (livello) e D2 (posizione), banner sugli
  altri; verificare la meccanica 3.5 del rituale (componenti, costi, il
  −2 CON permanente di Thorik come scelta ONSCREEN, il template Ibrido
  Treant risultante — coerente con state.md §1) e il costo del **Cuore di
  Moradin** (dopo il rito è SPESO: è ciò che ARC-09 assume, state.md §6).
  Il ponte narrativo verso Hammerfist resta compito di ARC-08 B2: qui si
  chiude con Hella viva e il party pronto al P5.
- **Accettazione**: un solo master P3B; meccanica verificata; stato
  artefatti in uscita = stato che ARC-08/09 assumono; ARC-08 B2 punta qui.

### B3. Fast-play del viaggio Anno −1000 (P5) — applicare D1
- **Evidenza**: il P5 esiste come dungeon/atto completo (DEFINITIVO ×2 =
  52 KB) e come sintesi "God Mode" (RICALIBRATO, 5,9 KB). La decisione DM
  (D1) è giocarlo VELOCE: serve il formato di mezzo — una sessione
  cinematografica con scontri veri ma montaggio serrato (lo stesso passo
  del "menù di crisi" di ARC-09 D13).
- **Azione**: creare `PortaleForgia-P5-FASTPLAY.md` (≤6 pagine): (1) scaletta
  a 5-6 scene (arrivo e Cronache dei Quattro Eroi; incontro con Thorgrim
  Barbadiferro e gli antenati; le mura durante l'assalto; **duello con
  l'antenato di Fauci** su griglia — l'unico scontro tattico completo,
  mappa da TACTICAL-GRIDS; il Rubino e il ritorno), ciascuna con read-aloud
  di 3 righe, prova/scontro, e **esito registrato** (per B4); (2) regola di
  montaggio: tutto ciò che non è il duello si risolve a prove di gruppo CD
  fisse (livello Q3); (3) esiti aperti del duello (vittoria/pareggio/fuga)
  — MAI un esito fisso; (4) puntatori al DEFINITIVO per chi vuole la
  versione lunga.
- **Accettazione**: il P5 è giocabile in una sessione senza aprire altri
  file; il duello ha mappa+statblock+3 esiti; ogni scena produce un dato
  per il ponte B4.

### B4. Il ponte meccanico "La Forgia ricorda le ferite" — [CROSS-ARC, il task più importante]
- **Evidenza**: P5-DEFINITIVO-PARTE2 r.285: *"Moradin sussurra: 'Ogni ferita
  che infliggi ora all'antenato, la mia Forgia la ricorderà quando
  affronterai il discendente'"* — e P6 r.746 fa cantare Aegis Fang "sangue
  Skullcrusher chiama". È IL gancio che salda i due archi… e **nessun file
  ARC-08 lo implementa**: lo statblock di Fauci di Palude
  (ARC-08, Schede §1) non ha alcuna traccia del viaggio. Il piano ARC-08
  (task A12) aspetta questo deliverable.
- **Azione**: creare la **tabella di carry-over** (in coda al FASTPLAY B3 o
  file proprio): esito del duello Anno −1000 → effetto quantificato su Fauci
  di Palude nel 1372 (proposte da validare col DM, es.: antenato ucciso =
  Fauci parte con la cicatrice ancestrale attiva, −10% pf e Presenza
  Terrificante CD −2 contro i portatori degli artefatti; antenato ferito
  gravemente = −1 al soffio; antenato fuggito = Fauci sa chi siete: +2
  iniziativa ma morale fragile sotto i 50 pf; tutte `[INFERRED — needs DM
  confirmation]`); più il gancio inverso: Aegis Fang "sente" Fauci
  (vantaggio di circostanza definito, non 5e). Propagare: nota nello
  statblock ARC-08 di Fauci + riga nel piano ARC-08 A12.
- **Accettazione**: ogni esito possibile del P5 ha un effetto scritto e
  quantificato sul boss dell'ARC-08; lo statblock ARC-08 rimanda alla
  tabella; zero meccaniche ambigue tra sistemi.

### B5. Errata meccanica 3.5 dell'arco
- **Evidenza**: a campione: `CORREZIONE-Boss-Fauci.md` r.334 assegna a un
  GS 12 "8.000 XP (2.000/PG)" — per 4 PG di 12° un GS 12 vale 19.200 PE
  (4.800/PG, DMG); il doppio profilo GS 15/GS 12 dello stesso drago (r.16,
  r.40, r.60) va risolto con A3; i boss ricalibrati (Terros/Mithral Golem,
  Elder Fire Elemental CR 14, Skullcrusher) non hanno mai avuto una
  verifica formale BAB/TS/CD; le "prove God Mode" del P5 vanno riportate a
  CD 3.5 esplicite.
- **Azione**: produrre `ERRATA-ARC07-35-Verification.md` nel formato degli
  errata ARC-09/08: XP per incontro (col livello Q3), statblock dei 4 boss,
  CD delle prove, action economy, poteri della Corona vs
  `campaign-artifacts.md`. Correzioni in place con nota; per le parti già
  giocate, annotare "giocato con i valori vecchi" senza retcon.
- **Accettazione**: file errata nuovo; XP corretti; un solo profilo per
  boss; nessuna correzione retroattiva sulle parti giocate.

### B6. Ancoraggio al March Clock e viaggio verso Hammerfist
- **Evidenza**: l'arco non nomina mai il March Clock (state.md §2.1); la
  battaglia di Hammerfist finisce al Day 19 e l'orda marcia dal Day 1: le
  parti restanti dell'arco (P4→P5→raccordo) e il viaggio fino a Hammerfist
  devono stare nei giorni giusti perché il sync tenga.
- **Azione**: mezza pagina nell'INDICE (B8): proposta di collocazione
  `[INFERRED — needs DM confirmation]` — es. uscita dalla Forgia ≈ Day
  14-15, viaggio ≈ Day 15-16, aggancio col prequel pregen ARC-08 (che copre
  la ricognizione e i primi giorni d'assedio) e arrivo dei Rumbling Stones
  quasi alla fine (Day 18-19). Coordinare con ARC-08 B6 (stessa tabella,
  due piani: scriverla UNA volta e puntarla).
- **Accettazione**: una sola cronologia condivisa 07→08; nessuna
  contraddizione col Day 19 (E3 di ARC-08).

### B7. Tesoro/WBL dell'arco
- **Evidenza**: l'arco assegna artefatti maggiori (gemme della Corona,
  benedizioni) ma il tesoro "ordinario" non è mai stato contato; il WBL del
  livello Q3 (~66k mo/PG all'11°, ~88k al 12°, ~110k al 13°, DMG) va
  verificato PRIMA di Hammerfist, perché ARC-08 B4 fonda lì la ricchezza
  d'ingresso e ARC-09 l'ha già auditata a valle.
- **Azione**: audit del loot per parte (giocate: dai log B1; future: dai
  master) + tabella per incontro; gli artefatti/benedizioni si contano come
  da audit ARC-09 (ricchezza speciale, non colmano il delta ordinario).
  Chiudere con "ricchezza d'uscita ARC-07 = ingresso ARC-08".
- **Accettazione**: totale coerente col WBL ±20%; handoff esplicito ai due
  audit a valle.

### B8. INDICE-GENERALE e DM-QUICKSTART dell'arco
- **Evidenza**: 20+ file markdown su 3-4 generazioni, 2 PDF, musica,
  immagini — e nessun indice; il file che doveva esserlo
  (`Mappe/Atlante-Visivo-Mappe.md`) è vuoto (A7). Il DM ci sta giocando
  DENTRO: la mappa serve subito.
- **Azione**: creare `ARC07-00-INDICE.md`: (1) tabella file → parte → stato
  (master/deprecato/ricalibrazione/annesso) dalla matrice A6; (2) quickstart
  1 pagina: dove siete (G3), cosa viene dopo (D2: resurrezione → viaggio
  veloce → Hammerfist), cosa stampare (mappa duello, TACTICAL-GRIDS
  relative, benedizioni); (3) l'ordine di gioco D2 con la nota sulla
  numerazione (A9); (4) cronologia B6.
- **Accettazione**: ogni file compare con uno stato; il DM ha il percorso
  della prossima sessione in una pagina.

### B9. Artefatti e PNG: i buchi trovati dall'audit richiesto dal DM
- **Evidenza**: (1) la **Collana dei Semi Eterni** (l'artefatto di Hella,
  state.md §6) è l'UNICO dei cinque artefatti-PG senza documentazione in
  `PG/Artefatti/` (Corona, Ring, Bracieri e Aegis Fang ce l'hanno o sono
  tracciati; la Collana esiste solo come riga nelle tabelle) — ed è proprio
  l'artefatto che si attiva alla resurrezione, cioè alla prossima sessione;
  (2) la scheda `PNG/Sonjak/` **non menziona il raid della Stanza della
  Corona** che lei stessa ha ordinato (Urialle, le Yochlol half-illithid,
  la dominazione di Belkram — G0): il "chi sa cosa" di state.md §4 perde il
  suo evento fondativo; (3) il **file col risultato del viaggio dello
  spirito** (G2b) non è collegato da nessun indice (Q6); (4) né Belkram
  (vecchio portatore, redento in morte) né Urialle hanno una scheda PNG
  con lo stato finale post-ARC-06.
- **Azione**: (1) creare `PG/Artefatti/Artefatti-Pg/Hella/01_Collana_dei_Semi_Eterni.md`
  (formato dei file Bracieri: lore, stati di risveglio, poteri attuali vs
  potenziali, aggancio alla resurrezione P3B) — contenuti da state.md §6 e
  `campaign-artifacts.md`, invenzioni flaggate; (2) aggiornare PNG/Sonjak
  (riga "ha ordinato il furto della Corona: Urialle + Yochlol
  half-illithid, fallito, Hella uccisa — il party POTREBBE non sapere
  ancora che il mandante è lei `[verify chi-sa-cosa con state.md §4]`");
  (3) collegare il file-risultato del viaggio (Q6) da INDICE, master P3B e
  log B1; (4) schede PNG post-mortem per Belkram (redento) e Urialle
  (morta/fuggita? `[INFERRED — needs DM]`) in PNG/ o nel formato AGENTS.md.
- **Accettazione**: 5 artefatti su 5 documentati in PG/Artefatti; la scheda
  di Sonjak racconta il raid; il risultato del viaggio è raggiungibile in
  un click dall'INDICE; nessun PNG di G0 senza stato.

---

## §3 — LOTTO C: Da "coerente" a "memorabile" (priorità P2)

### C1. Atlante di immagini, musica e PDF
- **Evidenza**: `Immagini/` ha 19 file GIÀ ben nominati (raro nel repo),
  `Musica/LaCanzoneDellePietre.mp3` esiste ma nessun file dice **quando**
  suonarla, i 2 PDF (Sinergie artefatti, Benedizioni di Moradin) non sono
  indicizzati da nessun markdown.
- **Azione**: tabella nell'INDICE (B8): asset → scena/parte → "quando
  usarlo" (es. la Canzone delle Pietre alla resurrezione di Hella o alla
  cantillazione delle Cantitrici `[INFERRED]`; Hella_elementale.png al
  risveglio; ilCuoreDiMoradin.png al rituale). Correggere il typo
  "Mitrtrsl Golem" nel filename immagine.
- **Accettazione**: ogni asset ha un momento d'uso; zero asset orfani.

### C2. Handout giocatore (formato HANDOUTS ARC-09)
- **Evidenza**: l'arco ha materiale-handout naturale mai formalizzato: le
  **Cronache dei Quattro Eroi** ("Le Cronache dicono che 'Quattro Eroi'
  salvarono Hammerfist nell'Anno −1000. Siete VOI." — P5-RICALIBRATO r.19),
  gli **8 affreschi divini** della Sala (P2), le **Benedizioni di Moradin**
  (il PDF è di fatto un handout), la visione della sovrapposizione
  temporale (P2 r.982-1007).
- **Azione**: sezione ARC-07 nel file HANDOUTS (o gemello): (1) la pagina
  delle Cronache (testo antico da consegnare PRIMA del viaggio — i giocatori
  scoprono di essere la profezia); (2) la tavola degli 8 affreschi con l'A6
  evidenziato; (3) le Benedizioni in formato carta singola per PG; (4) la
  carta-visione della sovrapposizione. Ogni handout con "quando darlo".
- **Accettazione**: handout stampabili, nessuno spoilera il carry-over B4.

### C3. Conseguenze a lungo periodo (tabella echi)
- **Evidenza**: l'arco semina ganci che nessuna tabella raccoglie: l'**uovo
  di Fauci di Palude** (P6 r.958 — vendetta futura, perfetto per ARC-10
  qualunque sia l'esito ARC-08), l'**eco "nessuna pietà" del Rubino**
  (P5-DEFINITIVO-PARTE2 r.167 — il tono della Corona cambia in base a come
  finisce il duello), le Cronache come fama crescente dei PG presso i nani
  (aggancia i Custodi Eterni di ARC-08 E5), Thorgrim Barbadiferro come
  antenato/founder da far riecheggiare nella Cerimonia delle 100 Asce.
- **Azione**: tabella echi nel formato ARC-09 (evento → eco → quando
  riemerge → file che lo gestisce), con varianti per esito del duello;
  cross-link alla tabella echi ARC-08 (C2) perché uovo e Rubino attraversano
  entrambi gli archi.
- **Accettazione**: tabella completa; nessun eco contraddice ARC-08/09;
  l'uovo ha un custode designato (dove sta? chi lo cova?) `[INFERRED]`.

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Prerequisito: **A0 del piano ARC-08** (state.md al giocato reale) se non già
eseguito. D6-D9 sono già decise; restano Q4 (default sicuro), Q5 e Q6
(puntatori, non bloccanti). Il tavolo sta per arrivare a P3B/P5: **la
priorità di consegna è B2→B3→B4** (il materiale che si gioca la prossima
sessione), quindi il lotto A si esegue in parallelo solo dove non li blocca.

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | A7 (igiene) + A9 (ordine dichiarato D2) | editing mirato | Q4 default |
| 2 | A1 + A2 (Skullcrusher, 1.000 anni prima) | find/replace + editing | D6, D7 (decise) |
| 3 | A6 (matrice generazioni + master) | consolidamento | — |
| 4 | **B2 (master resurrezione Hella)** | consolidamento+verifica | A6; D2; Q6 utile |
| 5 | **B3 (P5 fast-play)** | generativo | A1, A2, A6; D1 |
| 6 | **B4 (ponte "la Forgia ricorda" + statblock ARC-08)** | generativo — il task più importante | B3; **[CROSS-ARC]** con ARC-08 A12 |
| 7 | A3 (P6 sezione 1372 deprecata + estrazioni) | editing mirato | B4 (per ricollocare il canto di Aegis Fang) |
| 8 | A4 (gemme della Corona) + A5 (livello 13, D8) | editing mirato | D8 (decisa); A0 |
| 9 | A10 (artefatti: fonte unica D9) | consolidamento | — |
| 10 | A8 (DC→CD, inglese) | find/replace | — |
| 11 | B1 (session log del giocato, ARC-06 finale incluso) | intervista DM + scrittura | A0; **Q6** per il viaggio |
| 12 | B9 (Collana + Sonjak + PNG di G0) | generativo | B1; **Q6** |
| 13 | B5 (errata 3.5) | verifica | A3, D8 |
| 14 | B6 + B8 (cronologia + INDICE/quickstart) | consolidamento | A6, A9; coord. ARC-08 B6 |
| 15 | B7 (tesoro/WBL, al 13°) | audit | B1 |
| 16 | C1 + C2 (asset + handout) | classificazione+generativo | B3 |
| 17 | C3 (tabella echi) | generativo | B4, A3 |

**Regole anti-spreco** (identiche ad ARC-08/09): (1) passa all'engine SOLO
questo file + i file del lotto corrente + state.md §0-§4; (2) niente
riletture dell'intero arco; (3) dopo ogni lotto: `grep` di verifica del
criterio di accettazione, commit, riga di changelog in state.md se il canone
è cambiato; (4) aggiorna la checklist qui sotto.

### Checklist avanzamento

- [ ] A1 · [ ] A2 · [ ] A3 · [ ] A4 · [ ] A5 · [ ] A6 · [ ] A7 ·
  [ ] A8 · [ ] A9 · [ ] A10
- [ ] B1 · [ ] B2 · [ ] B3 · [ ] B4 · [ ] B5 · [ ] B6 · [ ] B7 ·
  [ ] B8 · [ ] B9
- [ ] C1 · [ ] C2 · [ ] C3
- [x] D1 · [x] D2 · [x] D3 · [x] D4 · [x] D5 · [x] D6 (Skullcrusher) ·
  [x] D7 (1.000 anni) · [x] D8 (livello 13, artefatti) · [x] D9
  (PG/Artefatti canonico) — decisioni acquisite 2026-07-02
- [ ] Q4 (deprecare, default sicuro) · [ ] Q5 (Oakenshield?) ·
  [ ] Q6 (file risultato viaggio spirito)

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5**: l'idea del viaggio
temporale come **profezia autoavverante** ("Siete sempre stati voi") con la
battaglia antica che semina meccanicamente quella moderna — è il tipo di
struttura che i moduli ufficiali non osano; la scrittura delle scene del
P5-DEFINITIVO (il Rubino, le due traiettorie sovrapposte di Skulldark e
Fauci); il metodo di ricalibrazione di Terros.md (analisi APL onesta, non a
occhio); le TACTICAL-GRIDS già in scala 1,5 m; perfino gli asset (musica,
immagini nominate, PDF) — nessun altro arco li ha così curati.

**Cosa lo separa dall'eccellenza**: (1) il boss che il tavolo sta per
incontrare aveva **tre nomi e tre profondità temporali** a seconda del file
— ora decisi (Skullcrusher, 1.000 anni prima: D6-D7) ma da propagare
(A1-A2); (2) P6 trascina una "fine campagna" del 1372 che gli Archi 08-09
hanno superato — con un Fauci di Palude GS 12 "morto per copione" che
contraddice il GS 15 a esiti aperti dell'ARC-08 (A3); (3) il gancio più
bello dell'arco — *la Forgia ricorda le ferite* — non è implementato da
nessuna parte (B4); (4) quattro generazioni di file per parte, col tavolo
già in mezzo al guado, e nessun indice (A6, B8); (5) la morte di Hella
(ARC-06) e il viaggio del suo spirito — gli eventi più pesanti mai giocati
— non hanno un log, e il file col risultato del viaggio non è collegato da
nessun indice (B1, B9/Q6); (6) l'artefatto che si attiva alla prossima
sessione, la Collana dei Semi Eterni, è l'unico dei cinque senza
documentazione (B9). Con A+B2-B4 la prossima sessione è coperta; col resto
di B l'arco tiene i conti; con C il viaggio di 1.000 anni diventa la
leggenda che i giocatori si raccontano — che è esattamente ciò che le
Cronache dei Quattro Eroi promettono loro.
