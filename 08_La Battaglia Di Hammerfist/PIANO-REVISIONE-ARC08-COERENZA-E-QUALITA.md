# PIANO DI REVISIONE ARC-08 (La Battaglia di Hammerfist) — Coerenza & Qualità

> **Versione**: v1 (2026-07-02) — prodotto da audit completo dell'arco.
> **Scopo**: documento **autocontenuto** da dare in pasto a un engine AI
> specializzato (o a più sessioni brevi) per eseguire le correzioni **a lotti**,
> senza dover ri-derivare il contesto ogni volta. Ogni task ha: file coinvolti,
> problema con evidenza (file:riga), azione richiesta, criterio di accettazione.
> **Gemello metodologico**: `09_Continuazione.../PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md`
> (stesso formato, stessa disciplina a lotti — già eseguito con successo).
> **Benchmark di qualità**: (interno) `Cerimonia-delle-100-Asce.md` — l'unico
> file dell'arco di generazione corrente: canone citato, CD in italiano 3.5,
> party reale, cross-link — e i deliverable ARC-09 (`EVENT-DECK`, `ERRATA-*`,
> `TESORO-WBL-AUDIT`); (esterno) *Red Hand of Doom* (Jacobs/Wyatt 2006),
> *Heroes of Battle* (3.5), AP Paizo PF1e per formato after-action e handout.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

0. **REGOLA ZERO — QUESTO ARCO È GIÀ STATO GIOCATO.** A differenza di ARC-09
   (revisionato *prima* del gioco), ARC-08 si è concluso al tavolo (state.md §0:
   ✅ completato, Day 19 sync, PG 12→13). La revisione ha quindi **due scopi**,
   non uno: (a) **archivio canonico** — i fatti giocati sono immutabili, i file
   devono raccontarli senza contraddirli; (b) **modulo rigiocabile** — il repo
   supporta il reset per nuovi gruppi (`scripts/new-campaign-group.sh`,
   branch-per-group: vedi `campaign/DM-CAMPAIGN-PLAYBOOK.md`), quindi il
   materiale pre-battaglia resta un modulo e va portato a standard, ma OGNI
   divergenza tra "com'era scritto" e "com'è andata" si risolve a favore del
   giocato. Mai retconnare un esito di sessione.
1. **`campaign/state.md` vince** su qualunque altro file in caso di conflitto
   (regola del repo). Ogni modifica di canone va **appesa al changelog** di
   state.md, mai riscritta nella storia.
2. **Sistema D&D 3.5 SRD only** — niente 5e (no azioni bonus, no vantaggio/
   svantaggio meccanici, no legendary actions), niente lore FR post-1385 DR.
   Ambientazione Faerûn 1372 DR.
3. **Mai inventare** stat, esiti di sessione o conoscenze PNG: se serve un dato
   non presente (es. la sorte di un PNG dopo la battaglia), marcarlo
   `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare
   `skills/rumblingstone-campaign/references/campaign-coherence.md` (che ha già
   una tabella di **eventi bloccati** per l'arco 08, r.50-51) e
   `campaign/state.md` §4 (chi sa cosa) e §6 (stato artefatti).
6. Le mappe tattiche usano scala **1,5 m/quadretto** (convenzione repo) —
   vedi A4 per la sanatoria delle eccezioni.
7. Lingua: **italiano**, con i nomi meccanici 3.5 in italiano (CD non DC,
   Osservare non Spot, Nascondersi non Hide) come da convenzione ARC-09 §0.7.
8. **Non cancellare file** senza decisione esplicita (Q5): il default è il
   banner `> ⚠️ DEPRECATED (2026-07): ...` in testa, come fatto in ARC-09 A12.

### Eventi GIOCATI e bloccati (immutabili — fonte: state.md, campaign-coherence.md §1)

| # | Fatto | Fonte |
|---|---|---|
| E1 | Hammerfist vince l'assedio; l'avanguardia della Mano Rossa è annientata/dispersa e NON si ricongiunge al corpo principale | state.md §2.2 r.132 |
| E2 | **210 nani morti, 90 superstiti** guidati da Re Thorek (difensori iniziali: 300) | coherence.md r.50; state.md §2.5 r.202 |
| E3 | Fine battaglia = **Day 19** del March Clock (= caduta di Terrelton, sync point) | state.md §2.1 r.104 |
| E4 | PG **12→13** durante l'arco | state.md §0 r.40 |
| E5 | I 4 PG sono nominati **Custodi Eterni** da Re Thorek; segue la **Cerimonia delle 100 Asce** | state.md §4 r.246; Cerimonia-delle-100-Asce.md |
| E6 | Struttura a 4 sessioni: Sessioni 1-2 giocate con i **pregen "Eroi di Hammerfist"** (Borin Ferropugno, Dara Occhiolesto, Thorin Runaforte, Nala Cantapietre); i **Rumbling Stones** (party reale) entrano in scena in Sessione 3 (Incontro 3B) e chiudono in Sessione 4 | Guida DM r.460-461, r.2150, r.2294 — struttura **intenzionale**, non errore |
| E7 | Capitana **Lythiel Alar-Wen** presente in Sessione 4 e alla Cerimonia (canonizzata 2026-05-04); consegna la Ghianda a Hella | state.md §4 r.251; Cerimonia §3.2 |
| E8 | Rapporto forze giocato: **900 attaccanti vs 300 difensori** (3:1) | state.md r.185; Guida DM r.628/854 |

### Decisioni di canone GIÀ PRESE (applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | Il drago dell'avanguardia si chiama **Fauci di Palude** (Black adult avanzato, GS 15) | Schede Personaggi §1; state.md §2.2 |
| D2 | Il re di Hammerfist è **Thorek Hammerfist**; il PG guerriero è **Thorik**; il pregen chierico è **Thorin Runaforte**. Tre nomi simili, tre persone diverse — mai fonderli (vedi A10) | state.md §1; Schede §2-3 |
| D3 | La Cerimonia delle 100 Asce è il **file-ponte canonico** verso ARC-09 (già a standard: NON riscriverla, usarla come riferimento) | Cerimonia-delle-100-Asce.md |
| D4 | Le **150 lance di Re Thorek** restano a Hammerfist e partono per Rethmar SOLO se gli hook politici di ARC-09 riescono (sigillo Maewen + lettera; D10 del piano ARC-09) — nessun file ARC-08 deve prometterle incondizionatamente | state.md §2.5 r.202; ARC-09 D10 |
| D5 | **Khorn** è l'ufficiale nanico di Hammerfist designato (in ARC-09) a guidare le 150 lance — è un PNG distinto dai pregen Eroi | HOOKS-Thorik r.135/157; campaign-history.md |

### Decisioni di canone da chiedere al DM (bloccano solo i task marcati)

| # | Domanda | Proposta di default (se il DM non decide diversamente) |
|---|---|---|
| Q1 | **Fauci di Palude è morto o fuggito?** Il ledger `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` r.139 dice "**morto** — rimosso dall'orda; −1 drago"; `campaign-coherence.md` r.51 dice "**fugge gravemente ferito**; può tornare" e r.230 lo conta tra i draghi a Rethmar; state.md §2.2 r.123 lo elenca ancora tra i 5 draghi. Contraddizione secca tra i tre tracker | **Fuggito ferito** (2 fonti su 3 + regola "state.md vince" + il suo statblock dice "fugge sotto i 50 PF" + regge l'eco-nemesi C2). Correggere il ledger. Ma se al tavolo è stato ucciso, vince il tavolo: solo il DM lo sa |
| Q2 | **Quanto ha perso l'orda a Hammerfist?** state.md §2.2 r.132: "−500 → attivi ~9.400". Ledger r.81: "−900 (Hammerfist vanguard intero) → 8.610". I file ARC-08 dicono 900 attaccanti di cui ~400 superstiti in rotta (Atlante-Mappe r.1034). Le tre contabilità non tornano | Formalizzare "**500 morti + 400 dispersi = −900 effettivi** all'orda" (i dispersi non si ricongiungono, E1) e ricalcolare UN solo totale corrente propagandolo a state.md, ledger e ARMATE-SYNC ARC-09 (i 5 scenari difensori dipendono da questo numero) |
| Q3 | **Chi sono i ranger elfici di "Capitano Lunapiena"?** I file battaglia hanno un capitano elfico (Lunapiena) + Signore Ventolesto (gufo celestiale) + Orion Pelleorsa (druido); la Cerimonia canonizza Lythiel (Sacred Forest). Due comandi elfici alla stessa battaglia, mai riconciliati; nessuno ha scheda PNG | Lunapiena = compagnia ranger **indipendente** dell'Elsir Vale (né Tiri Kitor né Sacred Forest), sopravvissuta, resta a presidio di Hammerfist (quindi NON va sommata ai difensori di Rethmar in ARMATE-SYNC). Lythiel resta l'unico canale col Sacred Forest `[INFERRED]` |
| Q4 | **Sorte post-battaglia dei 4 Eroi di Hammerfist (pregen)?** Nessun file lo dice. Sono un asset narrativo pronto: ARC-09 ha PNG nanici senza volto (i 300 mercenari, il presidio) | Tutti e 4 sopravvissuti `[INFERRED]`: Borin campione di Re Thorek a Hammerfist; Dara ed esploratori assorbiti nelle staffette per Thorik (Cerimonia §6.4); Thorin Runaforte officia il culto dei caduti; Nala passa a Dauth (aggancio Torneo). **Khorn resta distinto** (D5) |
| Q5 | **File ridondanti/meta: deprecare o eliminare?** Riguarda le 3 generazioni di atlante doppione (A8), `combat_prompts_guide.md` (guida ai prompt AI usati per generare il sistema — artefatto storico di lavorazione, non materiale di gioco) e i placeholder 01_/03_ (A6) | **Deprecare con banner**, mai eliminare (valore storico, regola §0.8). L'eliminazione fisica solo su ordine esplicito del DM |

---

## §1 — LOTTO A: Incoerenze di canone e igiene dei file (priorità P0)

### A1. Sorte di Fauci di Palude: morto vs fuggito — dipende da Q1
- **Problema**: vedi Q1. È l'unica contraddizione dell'arco che tocca **tre
  tracker strategici** contemporaneamente (state.md §2.2, ledger r.139,
  coherence.md r.51/230) e cambia il conteggio draghi della battaglia di
  Rethmar (ARC-09 ARMATE-SYNC conta i draghi per scenario).
- **Azione**: applicare la decisione Q1 in TUTTI i punti: ledger r.139,
  coherence.md r.51 e r.230, state.md §2.2 r.123 (nota tra parentesi:
  "ferito, in fuga — NON a Rethmar salvo richiamo" oppure "morto a
  Hammerfist"), statblock in `00_Schede_dei_Personaggi...md` §1 (aggiungere
  nota esito giocato in coda alle Tattiche), e conteggio draghi in
  ARMATE-SYNC ARC-09 se cambia. Riga di changelog in state.md.
- **Accettazione**: `grep -rn "Fauci"` sui tracker restituisce UNA sola
  versione della sorte; conteggio draghi Rethmar coerente.

### A2. Contabilità perdite dell'orda a Hammerfist — dipende da Q2
- **Problema**: vedi Q2 (−500 vs −900; attivi ~9.400 vs 8.610). In più i file
  ARC-08 usano internamente 900 attaccanti (Guida DM r.628; Lotto-1 r.281 e
  r.192 "conta precisa 900") e ~400 superstiti in rotta (Atlante-Mappe r.1034)
  — numeri compatibili tra loro ma mai riconciliati con i tracker.
- **Azione**: applicare Q2: una sola formula (proposta: 900 in campo, ~500
  morti, ~400 dispersi che non rientrano) scritta in: state.md §2.2 (nota
  post-Hammerfist), ledger §Day 19 (r.81 e r.139), e un paragrafo "Bilancio
  della battaglia" nel nuovo file ESITI (B1). Ricalcolare il running total
  del ledger dal Day 19 in poi e verificare che ARMATE-SYNC ARC-09 §2 parta
  dal numero giusto.
- **Accettazione**: un solo totale orda post-Day 19 in tutto il repo;
  changelog aggiornato.

### A3. XP e livelli: il testo promette 13°→15°, il canone dice 12→13
- **Problema**: `hammerfist_encounters...-final.md` r.1382-1383: "GRAN TOTALE
  34.400 XP (8.600 per PG) — abbastanza per portare PG da 13° a 15° livello".
  Ma l'arco è stato giocato **da 12° a 13°** (E4) e 8.600 XP non bastano
  comunque per due livelli a quel rango (servono ~12.000 solo per 12°→13°,
  DMG). In più le Sessioni 1-2 le hanno giocate i pregen (E6): l'attribuzione
  degli XP al party va chiarita.
- **Azione**: riscrivere la sezione "RIASSUNTO XP E RICOMPENSE": budget per
  APL 12, nota esplicita "Sessioni 1-2 = XP ai pregen (non cumulano sul
  party); Sessioni 3-4 + bonus narrativo = XP ai Rumbling Stones,
  sufficienti per chiudere il 12°→13° insieme al carry-over dell'Arco 07
  `[INFERRED — needs DM confirmation sui totali reali]`". Stessa passata
  sulla sezione ricompense della Guida DM se duplicata.
- **Accettazione**: nessun riferimento residuo a "13° a 15°"; attribuzione
  pregen/party esplicita; numeri compatibili con E4.

### A4. Scala delle mappe: 3 m vs 1,5 m per quadretto
- **Problema**: `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` dichiara
  "1 quadrato = 3 metri" (r.40, r.79, r.924) ma poi dice "Grid già
  ottimizzato standard D&D (5ft/1,5m)" (r.1234); `Hammerfist-L3-REVISED` è
  dichiarato "Griglie 1.5m"; la convenzione di repo (ARC-09 §0.6) è
  1,5 m/quadretto. Un DM che stampa due mappe di file diversi ottiene scale
  diverse senza saperlo.
- **Azione**: passata su tutti i file `Mappe/*` + sezioni-mappa dei file 00_:
  ogni mappa dichiara la scala in testa; le mappe **tattiche** (per griglia
  da combattimento) vanno normalizzate o ri-etichettate a 1,5 m/quadretto;
  le viste **strategiche/panoramiche** possono restare a 3 m o più MA con
  etichetta esplicita "vista strategica — non per griglia". Dove la scala 3 m
  è strutturale (dimensioni disegnate ASCII), non ridisegnare: etichettare.
- **Accettazione**: `grep -n "quadrat\|1,5\|3 metri" Mappe/*` mostra una
  dichiarazione per mappa; zero mappe tattiche senza scala.

### A5. Terminologia: DC inglesi, skill inglesi, lessico 5e colloquiale
- **Problema**: 36 occorrenze di `DC n` contro la convenzione CD (§0.7),
  concentrate nei file Mappe (es. Lotto-1 r.191-194 "Osservare DC 15/20/25/30"
  — ibrido italiano/inglese; L1-REVISED r.199 "Hide DC 20", r.242
  "(advantage!)"). Skill in inglese sparse (Spot, Hide, Climb, Balance,
  Strength check). Parole "vantaggio/svantaggio/advantage" usate in senso
  colloquiale (Atlante-Mappe r.352, r.902, r.1042, r.1076-1079) che a un
  lettore 3.5/5e-misto suonano meccaniche.
- **Azione**: (1) DC→CD globale nell'arco; (2) skill → nomi italiani 3.5
  (Osservare, Ascoltare, Nascondersi, Muoversi Silenziosamente, Scalare,
  Equilibrio, prova di Forza); (3) riformulare i "vantaggio/advantage"
  colloquiali in termini 3.5 espliciti (es. "+2 di circostanza", "bonus del
  terreno rialzato"), così nessuna riga è ambigua tra sistemi.
- **Accettazione**: `grep -rn "DC [0-9]" '08_La Battaglia Di Hammerfist'` = 0;
  `grep -rni "advantage"` = 0; le occorrenze residue di "vantaggio" sono solo
  prosa non meccanica.

### A6. File placeholder fuori canone: 01_ e 03_
- **Problema** (grave, stessa classe di ARC-09 A12): due file sono stub
  generici in inglese che **contraddicono il canone**.
  `01_MANO_ROSSA_MARCIA_VERSO_HAMMERFIST.md` inventa "Castle Red" (r.7),
  "River Styx" (r.23), "Ruins of Eldor" (r.24), "Forest of Whispers" — la
  marcia canonica parte dal **Fane di Tiamat nel Shaar** con i waypoint di
  state.md §2.1 (Vraath, Skull Gorge, Drellin's Ferry eq., Terrelton).
  `03_SESSIONE_INTERRUTTA_BATTAGLIA_INIZIA.md` è un recap generico senza un
  solo nome della campagna. Manca inoltre qualsiasi file `02_`.
- **Azione**: (1) riscrivere 01_ come vera scheda logistica dell'avanguardia
  di Fauci di Palude (900 unità: da dove si stacca dall'orda, quando, che
  strada fa per Hammerfist, opportunità di interferenza PG che il gruppo
  ricognizione ha davvero — riusare i contenuti di Lotto-1 Ricognizione),
  ancorata al March Clock (vedi B6); (2) deprecare 03_ con banner e
  sostituirlo con i session log veri (B2); (3) risolvere il buco 02_ nello
  schema di rinomina (A9), senza inventare un file solo per riempire il
  numero.
- **Accettazione**: zero toponimi off-canon (`grep -rn "Castle Red\|Styx\|Eldor"`
  = 0 fuori dai banner); i due file o sono canonici o sono marcati DEPRECATED.

### A7. Code conversazionali AI in testa ai file
- **Problema**: 5 file aprono con la risposta dell'assistente che li generò:
  `00_Schede_dei_Personaggi...` r.1 ("Assolutamente. Ecco il documento
  unificato..."), `00_SCHEDE_DI_BATTAGLIA_E_REGISTRO_PERDITE` r.1-5
  ("Certamente. Ho compreso perfettamente la necessità..."),
  `00_ATLANTE VISIVO...md` r.1-3, `00_ATLANTE VISIVO...-complete.md` r.1,
  `00_battle_stats_maps-final.md` r.1-3 ("Certamente. Ho creato...").
  Stessa classe di ARC-09 A12 (code conversazionali).
- **Azione**: rimuovere le code e sostituirle con un'intestazione standard:
  titolo, scopo del file, generazione/stato (canonico | deprecato), data
  revisione. NON toccare il contenuto sottostante in questo lotto.
- **Accettazione**: `grep -rn "^Assolutamente\|^Certamente\|^Perfetto"` = 0
  nell'arco; ogni file 00_ ha un header di stato.

### A8. Quattro generazioni di atlante/mappe sovrapposte — eleggere i master
- **Problema**: il materiale mappe/atlante esiste in 4 strati mai riconciliati:
  (a) `00_battle_stats_maps-final.md` (22 KB) è un **sottoinsieme letterale**
  di (b) `00_ATLANTE VISIVO...md` (29 KB) — stessa intro parola per parola,
  il diff mostra solo aggiunte; (c) `00_ATLANTE VISIVO...-complete.md` (33 KB)
  è una terza generazione con 166 righe di diff da (b); (d)
  `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` (48 KB, "16 mappe") è un quarto
  compendio autonomo. In parallelo, `Mappe/Hammerfist-Lotto-{1,2,3}` e
  `Mappe/Hammerfist-L{1,2,3}-REVISED-Ultra-Clear` sono due generazioni delle
  stesse mappe di sessione ("REVISED" dichiara di correggere le prime).
  Un engine (o un DM) che entra nella cartella non può sapere quale versione
  usare — è il rischio multi-engine già visto in ARC-09 §5.(1).
- **Azione**: (1) compilare una **matrice di contenuto** (mappa × file: dove
  appare, quale versione è più completa); (2) eleggere UN master per
  categoria — proposta: `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` master
  visivo + i tre `L*-REVISED-Ultra-Clear` master tattici di sessione;
  (3) banner DEPRECATED su (a), (b), (c) e sui `Lotto-*` superati, con
  puntatore al master ("superseded by ..."); (4) aggiornare ogni riferimento
  interno dell'arco ai file deprecati. Rispettare Q5 (deprecare, non
  cancellare).
- **Accettazione**: un solo file per contenuto senza banner; la matrice è
  in testa al master o nell'INDICE (B7); zero riferimenti attivi a file
  deprecati.

### A9. Naming dei file: prefissi incoerenti, buco 02_, immagini anonime
- **Problema**: sei file con prefisso `00_`, poi `01_`, poi `03_` (manca
  `02_`); nomi con spazi e maiuscole miste (`00_ATLANTE VISIVO DELLA
  BATTAGLIA DI HAMMERFIST-complete.md`, `hammerfist_encounters-La
  Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md`); 15+ immagini
  `immage_campaign/Generated Image October 03, 2025 - 5_54PM.webp` prive di
  qualsiasi aggancio alla mappa/scena che illustrano (cartella con typo
  "immage").
- **Azione**: schema di rinomina coerente con ARC-09 (`git mv`), es.
  `ARC08-00-INDICE.md`, `ARC08-01-GUIDA-DM.md`, `ARC08-02-SCONTRI.md`, ...,
  aggiornando TUTTI i riferimenti (repo-wide grep: state.md, coherence.md,
  ARC-09, skills). Le immagini si rinominano `hammerfist-sNN-descrizione.webp`
  solo DOPO aver compilato la tabella immagine→mappa (C3) — mai rinominare
  un'immagine non identificata. Cartella `immage_campaign` → `immagini` (o
  lasciare con nota, se i link esterni al repo la usano:
  `[INFERRED — needs DM confirmation]`).
- **Accettazione**: nessun buco di numerazione; uno script di verifica link
  (come ARC-09 A8) passa a zero rotture; ogni immagine rinominata è citata
  da almeno un file.

### A10. Thorin / Thorik / Thorek: tre nomi a una lettera di distanza
- **Problema**: nel solo `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
  convivono 12 "Thorin", 15 "Thorik" e 24 "Thorek". Sono tre personaggi
  diversi (D2: pregen chierico / PG / re) e la probabilità di refuso
  incrociato è altissima — e un refuso qui cambia CHI ha fatto cosa in un
  arco già giocato.
- **Azione**: audit occorrenza-per-occorrenza dei tre nomi in tutto l'arco
  (63+ occorrenze totali): per ciascuna verificare dal contesto quale
  personaggio è inteso (il pregen agisce solo in Sessioni 1-2 e come PNG
  dopo; il PG solo da Sessione 3/Incontro 3B in poi; il re sempre come
  comandante difensore). Correggere i refusi; aggiungere in testa ai 2 file
  master una **nota di disambiguazione** ("Thorin=pregen, Thorik=PG,
  Thorek=re").
- **Accettazione**: audit documentato (tabella occorrenze corrette nel
  commit); nota di disambiguazione presente; nessun pregen che agisce in
  Sessione 4 e nessun PG in Sessione 1-2.

### A11. Due comandi elfici mai riconciliati (Lunapiena vs Lythiel) — dipende da Q3
- **Problema**: vedi Q3. In più nessuno dei PNG alleati della battaglia
  (Lunapiena, Ventolesto, Orion Pelleorsa, Dana Forgiapietra) ha una scheda
  in `PNG/` (la cartella contiene solo PNG ARC-09) né in `campaign/npcs/`
  (che **non esiste** nonostante AGENTS.md la dichiari).
- **Azione**: applicare Q3 nei file dove i due comandi si sfiorano (Guida DM
  §PNG chiave, Schede §2, Sessione 4, Cerimonia già corretta); esplicitare
  in ARMATE-SYNC ARC-09 che i ranger di Lunapiena NON sono tra i difensori
  di Rethmar (o il contrario, se il DM decide diversamente). La creazione
  delle schede PNG è in B3 — qui solo la coerenza dei riferimenti.
- **Accettazione**: un solo assetto dei comandi elfici in tutto il repo;
  nessun doppio conteggio in ARMATE-SYNC.

---

## §2 — LOTTO B: Completamento contenuti (priorità P1)

> Benchmark: la Cerimonia delle 100 Asce (D3) per tono e formato; i
> deliverable ARC-09 (`ERRATA-*`, `TESORO-WBL-AUDIT`, session log del
> playbook) per struttura. Qui si colma ciò che a un arco GIOCATO manca:
> la memoria di quello che è successo.

### B1. ESITI CANONICI / After-Action Report — il file più importante del lotto
- **Evidenza**: l'arco non ha un equivalente di
  `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ESITI-CONSEGUENZE.md`. I fatti
  giocati vivono sparsi in state.md, coherence.md r.50-51 e nella Cerimonia;
  nessun file dell'arco li raccoglie. Chi apre la cartella 08 oggi trova solo
  il "prima" (modulo) e mai il "dopo" (storia).
- **Azione**: creare `ARC08-ESITI-CANONICI.md` con: (1) cronaca sintetica
  delle 4 sessioni giocate (chi, dove, esito — dai log B2, con flag
  [INFERRED] dove la memoria è lacunosa); (2) **bilancio della battaglia**
  con i numeri di A2/Q2 (900 vs 300; 210/90; sorte di Fauci per Q1; sorte di
  Grimjaw e Gorthak `[INFERRED — presumibilmente uccisi, needs DM
  confirmation]`); (3) tabella "cosa lascia l'arco a Rethmar" — 150 lance
  condizionate (D4), Custodi Eterni, staffette, raid drow al tempio come seme
  della Fase 0 (state.md §3 r.215), intel di Tempestas a Brenna; (4) puntatori
  a Cerimonia (D3) e agli HOOKS ARC-09 senza duplicarli.
- **Accettazione**: un DM (o un engine) legge SOLO questo file e sa com'è
  finita la battaglia e cosa ne discende; zero contraddizioni con state.md.

### B2. Session log retroattivi delle 4 sessioni della battaglia
- **Evidenza**: `campaign/sessions/` contiene solo
  `2026-05-03_session-3.md` (post-battaglia, Day 19-20). Le sessioni della
  battaglia stessa non hanno log nel formato del playbook — il surrogato è
  il placeholder 03_ (vuoto di fatti, vedi A6). Ma state.md §4 r.251 cita
  eventi precisi di "Hammerfist Battle Sessione 4": la materia prima esiste.
- **Azione**: scrivere i log retroattivi nel formato AGENTS.md (Summary /
  Key decisions / XP / Loot / Next hooks) — o 4 file o un log consolidato
  "sessioni 1-4" se il DM preferisce — ricostruendo da: Guida DM (struttura
  incontri), state.md §4 (eventi canonizzati), Cerimonia (esiti), coherence
  (eventi bloccati). OGNI fatto non documentato va flaggato
  `[INFERRED — needs DM confirmation]`, non inventato (regola §0.3). Datarli
  con data-placeholder e nota "retro-log, ricostruito 2026-07".
- **Accettazione**: i log esistono, seguono il template, ogni [INFERRED] è
  esplicito; 03_ è deprecato e rimanda a loro.

### B3. Schede PNG mancanti (il cast di Hammerfist non esiste su disco)
- **Evidenza**: nessuna scheda per Re Thorek, Dana Forgiapietra, Grimjaw,
  Gorthak, Fauci di Palude, Lunapiena, Ventolesto, Orion Pelleorsa, né per i
  4 Eroi pregen, né per Khorn (D5, citato in 3+ file ARC-09). `PNG/` ha solo
  il cast ARC-09; `campaign/npcs/` non esiste. Le stat vivono solo dentro le
  appendici dell'arco — introvabili per gli engine che seguono AGENTS.md
  ("Check campaign/npcs/ before describing NPCs").
- **Azione**: creare le schede nel formato AGENTS.md (Role/Status/Location/
  Motivation/CR/Key stats/Notes) in `PNG/` (convenzione di fatto del repo),
  UNA per PNG, con **Status post-battaglia** da Q1/Q4/[INFERRED]. Le stat si
  **puntano** alle appendici dell'arco (fonte unica, come ARC-09 B3 fece col
  Ghostlord), non si duplicano. Aggiornare i file dell'arco perché citino le
  schede.
- **Accettazione**: ogni PNG nominato nell'arco ha scheda con Status;
  `grep` dei nomi in PNG/ trova tutti; nessuna stat duplicata.

### B4. Tesoro/WBL dell'arco (12→13)
- **Evidenza**: le "RICOMPENSE" dell'arco sono note sparse; nessun totale.
  Il WBL 3.5 richiede ~88.000 mo/PG al 12° e ~110.000 al 13°: l'arco deve
  giustificare ~+22.000 mo/PG equivalenti. L'audit ARC-09
  (`Arco-Post-Hammerfist-TESORO-WBL-AUDIT.md`) assume la ricchezza
  d'ingresso al 13° come data — questo lotto la fonda.
- **Azione**: audit del loot effettivamente distribuito (dai log B2 e dalla
  sezione ricompense della guida scontri) + tabella tesoro per incontro in
  stile Paizo; se manca valore, proporre dove sta (armeria di Hammerfist,
  gratitudine di Re Thorek, bottino dell'avanguardia — tutto SRD/DMG, plot
  item flaggati). Chiudere con la riga "ricchezza d'uscita ARC-08 = ricchezza
  d'ingresso ARC-09" agganciata all'audit ARC-09.
- **Accettazione**: totale dichiarato coerente col WBL ±20%; handoff
  esplicito verso TESORO-WBL-AUDIT ARC-09.

### B5. Errata meccanica 3.5 (statblock e regole di massa)
- **Evidenza**: la passata di verifica ARC-09 B5 non copre l'arco 08. Errori
  già individuati a campione in `00_Schede_dei_Personaggi...md`: il Cavaliere
  Hobgoblin (Guerriero 8/Guardia Nera 2) ha "Punire il Bene: +10 (livello) ai
  danni" (r.110) — in 3.5 il bonus è pari al livello di **Guardia Nera**,
  quindi **+2**; ha "Aura di Disperazione" (r.111) che la classe ottiene al
  **3°** livello, non al 2°; Fauci di Palude ha un "Soffio a Cono 1/giorno"
  (r.77) che i draghi neri SRD non hanno (linea only) — da flaggare
  house-rule o rimuovere. Il sistema di massa (AU/DU/PFU/Morale) non è mai
  stato verificato per action economy 3.5.
- **Azione**: produrre `ERRATA-ARC08-35-Verification.md` nello stesso formato
  degli errata ARC-09: BAB/Lotta, CA contatto/impreparato, TS, CD dei poteri,
  progressioni di classe/prestigio, GS dichiarati vs contenuto; per il
  sistema di massa una nota di compatibilità (azioni standard/movimento,
  niente meccaniche 5e). Correzioni in place con nota, poiché l'arco è
  giocato: dove l'errore è già stato giocato così, la correzione è
  **annotata ma non retroattiva** (regola zero).
- **Accettazione**: file errata nuovo; i due errori campione corretti;
  ogni correzione distingue "fix del modulo" da "com'è stato giocato".

### B6. Ancoraggio al March Clock (l'arco precede il sistema a doppio clock)
- **Evidenza**: i file dell'arco contano solo "Giorno 1/2/3" di battaglia
  (+ 4 sessioni); il March Clock (state.md §2.1, canon 2026-05-05) fissa solo
  il punto finale (Day 19 = E3). Il lettore non può collocare ricognizione e
  assedio sul calendario di campagna, e il 01_ riscritto (A6) ne ha bisogno.
- **Azione**: mezza pagina (nell'ESITI B1 o nell'INDICE B7): "Ricognizione ≈
  Day 15-16, assedio Giorni 1-3 ≈ Day 16-18, vittoria e Cerimonia = Day 19
  `[INFERRED — needs DM confirmation]`", con rimando a state.md §2.1 e al
  ledger. Propagare l'ancora nei file master (una riga in testa, non un
  find/replace invasivo).
- **Accettazione**: una sola cronologia Day X-19 dichiarata; nessun file che
  la contraddica.

### B7. INDICE-GENERALE e DM-QUICKSTART dell'arco (replayability)
- **Evidenza**: ARC-09 ha INDICE-GENERALE e DM-QUICKSTART; l'arco 08 non ha
  né l'uno né l'altro — con 19 file markdown su 4 generazioni, è la mappa
  che manca. In ottica branch-per-group (regola zero, scopo b) serve dire a
  un nuovo DM: cosa leggere, in che ordine, cosa è modulo e cosa è storia
  del gruppo 1.
- **Azione**: creare `ARC08-00-INDICE.md`: (1) tabella file → ruolo →
  stato (master/deprecato/storico) — riusa la matrice A8; (2) ordine di
  lettura per DM nuovo (Guida DM → Scontri → Mappe master → Schede →
  Registro); (3) sezione "per rigiocare l'arco con un nuovo gruppo" (reset
  playbook, cosa NON portare: gli esiti del gruppo 1); (4) sezione "cosa è
  successo davvero" → puntatore a ESITI B1. Quickstart di 1 pagina in testa
  all'INDICE stesso (non serve file separato per un arco chiuso).
- **Accettazione**: ogni file dell'arco compare nell'INDICE con uno stato;
  un DM nuovo ha un ordine di lettura; il confine modulo/storia è esplicito.

---

## §3 — LOTTO C: Da "coerente" a "memorabile" (priorità P2)

> L'arco è già stato un successo al tavolo: qui si consolida ciò che ha
> inventato (il primo sistema di massa della campagna) e lo si mette al
> servizio di ARC-09/10. Riferimenti: Heroes of Battle, il Piano ARC-09
> (D13, C1, C7 — che citano Hammerfist come "precedente").

### C1. Consolidare il sistema di combattimento di massa in UNA fonte
- **Evidenza**: le regole di massa vivono in 4 posti: `mass_combat_guide_Dm.md`
  (16 KB), `00_Schede_dei_Personaggi...` §4 ("Guida al Combattimento di
  Massa"), le appendici della Guida DM (§7) e le schede/registro PFU. ARC-09
  D13 e C1 le citano come "il precedente narrativo di Hammerfist" e
  STRUTTURA §9 (Rethmar) vi si ispira — ma non c'è un file canonico da
  puntare.
- **Azione**: eleggere `mass_combat_guide_Dm.md` come fonte unica (o
  estrarne una v2 pulita): filosofia, AU/DU/PFU, tabella Morale, danni
  strutturali, 1 pagina di quick-reference; le altre copie diventano
  puntatori (banner "regole canoniche in ..."). Aggiungere il paragrafo di
  raccordo verso ARC-09: cosa STRUTTURA §9 ha ereditato e cosa ha cambiato
  (VP nascosti, eventi scelti dai PG — D13), così i due sistemi non
  divergono in silenzio.
- **Accettazione**: una sola fonte normativa; le copie puntano ad essa;
  raccordo ARC-09 scritto.

### C2. Tabella degli echi a lungo periodo (formato ARC-09 CONSEGUENZE-ECHI)
- **Evidenza**: gli echi dell'arco esistono ma sparsi: Fauci ferito che può
  tornare (coherence r.51, se Q1=vivo → candidato nemesi/carta evento a
  Rethmar o ARC-10), le 150 lance (D4), i pregen Eroi (Q4), la runa dei
  Custodi Eterni (Cerimonia §2 ne fa un simbolo fisico con effetti — mai
  quantificati meccanicamente), il raid drow al tempio che prefigura la
  Fase 0 di Rethmar (state.md §3).
- **Azione**: sezione "Echi a lungo periodo" in ESITI (B1) nel formato
  della tabella echi del Torneo ARC-09 (evento → eco → quando riemerge →
  file che lo gestisce). Quantificare il beneficio meccanico della runa dei
  Custodi (proposta: +2 di circostanza a Diplomazia con nani del Vale +
  ospitalità a Hammerfist; `[INFERRED — needs DM confirmation]`).
  Se Q1=vivo, proporre la carta-evento "Il ritorno di Fauci di Palude"
  all'EVENT-DECK di Rethmar come S2 (senza scriverla qui: solo l'hook e il
  puntatore, la scrittura spetta a una sessione EVENT-DECK).
- **Accettazione**: tabella echi completa; runa quantificata o flaggata;
  nessun eco che contraddica gli HOOKS ARC-09.

### C3. Atlante immagini: agganciare i 40+ webp alle mappe e scene
- **Evidenza**: `immage_campaign/` contiene ~40 webp di cui 15+ si chiamano
  "Generated Image October 03, 2025 - ...". Gli atlanti contengono i prompt
  con cui furono generate — ma nessuna tabella immagine↔mappa↔prompt. Il
  materiale visivo (raro e costoso) è di fatto inutilizzabile a colpo
  d'occhio.
- **Azione**: tabella nel master visivo (A8) o nell'INDICE: file immagine →
  mappa/scena → sessione → prompt d'origine (se rintracciabile) → "quando
  mostrarla". Poi (e solo poi) la rinomina A9 delle immagini identificate.
  Immagini non riconducibili: sezione "non classificate" con miniatura
  descritta, decisione al DM.
- **Accettazione**: ≥80% delle immagini classificate; ogni mappa master
  indica la sua immagine se esiste.

### C4. Handout retro e memorabilia (benchmark Paizo, formato HANDOUTS ARC-09)
- **Evidenza**: ARC-09 B4 ha creato il file HANDOUTS; l'arco 08, pur chiuso,
  ha due pezzi che i giocatori rivedranno per tutta la campagna: la **runa
  di pietra dei Custodi Eterni** (Cerimonia §2: 5 cm, al collo) e le **100
  asce di adamantio rituale**. In ottica rigiocabilità serve anche la mappa
  giocatore della fortezza (le attuali sono tutte lato DM).
- **Azione**: aggiungere una sezione ARC-08 a
  `Arco-Post-Hammerfist-HANDOUTS.md` (o file gemello nell'arco): (1) la runa
  dei Custodi (descrizione + effetto C2 + disegno ASCII/prompt immagine);
  (2) il canto della cantillazione ("ricordato, ricordato, ricordato") come
  testo da leggere; (3) mappa giocatore della fortezza (versione senza
  informazioni segrete della L2 master). Ogni handout con "quando darlo".
- **Accettazione**: handout stampabili; nessuno rivela info lato DM.

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Esegui **un lotto per sessione**, nell'ordine. Le decisioni Q1-Q4 vanno
chieste al DM PRIMA della sessione 1 (bloccano A1, A2, A11 e colorano B1-B3);
Q5 ha un default sicuro (deprecare) e non blocca nulla.

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | A7 + A6 (code AI, placeholder 01_/03_ banner) | editing mirato | Q5 default |
| 2 | A1 + A2 (Fauci + contabilità perdite, tracker) | editing mirato | **Q1, Q2** |
| 3 | A3 + A5 (XP/livelli + DC→CD/terminologia) | find/replace + editing | — |
| 4 | A8 (matrice contenuti + elezione master + banner) | consolidamento | — |
| 5 | A4 (scale mappe, sui soli master) | editing mirato | A8 |
| 6 | A10 + A11 (Thorin/Thorik/Thorek + comandi elfici) | audit + editing | **Q3** |
| 7 | A9 (rinomina file, git mv, fix riferimenti repo-wide) | meccanico | A8 (per rinominare solo i master) |
| 8 | B2 (session log retroattivi) | generativo | A1-A2 (numeri fissati) |
| 9 | B1 (ESITI CANONICI) + B6 (ancora March Clock) | generativo | B2, **Q1-Q2** |
| 10 | B3 (schede PNG) | generativo | **Q3, Q4** |
| 11 | B5 (errata 3.5) | verifica | — |
| 12 | B4 (tesoro/WBL) | audit+generativo | B2 |
| 13 | B7 (INDICE + quickstart) | consolidamento | A8, A9, B1 |
| 14 | C1 (sistema massa fonte unica + raccordo ARC-09) | consolidamento | — |
| 15 | C2 (tabella echi + runa Custodi) | generativo | B1, **Q1** |
| 16 | C3 (atlante immagini) + coda rinomina immagini di A9 | classificazione | A8 |
| 17 | C4 (handout retro) | generativo | C2 |

**Regole anti-spreco** (identiche ad ARC-09): (1) passa all'engine SOLO questo
file + i file del lotto corrente + state.md §0-§4; (2) niente riletture
dell'intero arco; (3) dopo ogni lotto: `grep` di verifica del criterio di
accettazione, commit, riga di changelog in state.md se il canone è cambiato;
(4) aggiorna la checklist qui sotto.

### Checklist avanzamento

- [ ] A1 · [ ] A2 · [ ] A3 · [ ] A4 · [ ] A5 · [ ] A6 · [ ] A7 ·
  [ ] A8 · [ ] A9 · [ ] A10 · [ ] A11
- [ ] B1 · [ ] B2 · [ ] B3 · [ ] B4 · [ ] B5 · [ ] B6 · [ ] B7
- [ ] C1 · [ ] C2 · [ ] C3 · [ ] C4
- [ ] Q1 · [ ] Q2 · [ ] Q3 · [ ] Q4 · [ ] Q5 — risposte DM

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5**: l'idea registica delle
Sessioni 1-2 coi pregen "Eroi di Hammerfist" e l'ingresso dei Rumbling Stones
a battaglia in corso (E6) — un cold open che nessun modulo ufficiale RHoD ha;
il sistema di massa AU/DU/PFU con registro perdite stampabile (è il seme da
cui ARC-09 ha derivato il suo impianto D13); la Cerimonia delle 100 Asce, che
da sola vale come benchmark di scrittura dell'intero repo; la mole di mappe
ASCII multi-vista con coordinate.

**Cosa lo separa dall'eccellenza**: (1) è un arco **giocato che non ricorda
sé stesso** — nessun ESITI, nessun session log, il cast senza schede: la
memoria vive solo fuori dalla cartella (state.md, coherence, Cerimonia) — è
il gap più grave e il Lotto B esiste per questo; (2) quattro generazioni di
atlanti/mappe mai riconciliate rendono la cartella illeggibile a freddo
(A8-A9); (3) la sorte di Fauci di Palude e la contabilità delle perdite sono
in contraddizione attiva tra i tre tracker strategici — e ARC-09 ci costruisce
sopra i suoi scenari (A1-A2, da chiudere per primi); (4) terminologia ibrida
EN/IT e scale mappe difformi (A4-A5) sotto lo standard che ARC-09 ha ormai
fissato. Con il Lotto A l'arco smette di contraddire la campagna; con B
diventa la memoria canonica di come i Rumbling Stones sono diventati Custodi
Eterni; con C il suo sistema di massa e i suoi cimeli continuano a lavorare
per Rethmar e oltre.
