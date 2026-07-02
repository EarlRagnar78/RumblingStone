# PIANO DI REVISIONE ARC-08 (La Battaglia di Hammerfist) — Coerenza & Qualità

> **Versione**: v3 FINALE (2026-07-02) — audit completo dell'arco con TUTTE
> le decisioni del DM incorporate (D1-D14). **Il piano non ha domande
> aperte bloccanti: l'engine può eseguire tutti i lotti nell'ordine di §4
> senza ulteriori input dal DM** (D10-D14 sono default vincolanti che il DM
> può emendare a posteriori).
> **Scopo**: documento **autocontenuto** da dare in pasto a un engine AI
> specializzato (o a più sessioni brevi) per eseguire le correzioni **a
> lotti**. Ogni task ha: file coinvolti, problema con evidenza (file:riga),
> azione richiesta, criterio di accettazione.
> **Gemelli metodologici**: `09_Continuazione.../PIANO-REVISIONE-ARC09-...md`
> (eseguito) e `07_il Portale Della Forgia Eterna/PIANO-REVISIONE-ARC07-...md`
> (v2) — i punti di contatto sono marcati **[CROSS-ARC]**.
> **Benchmark di qualità**: (interno) `Cerimonia-delle-100-Asce.md` —
> l'unico file dell'arco di generazione corrente: canone citato, CD in
> italiano 3.5, party reale, cross-link — e i deliverable ARC-09
> (`EVENT-DECK`, `ERRATA-*`, `TESORO-WBL-AUDIT`); (esterno) *Red Hand of
> Doom* (Jacobs/Wyatt 2006), *Heroes of Battle* (3.5), AP Paizo PF1e per
> contingenze e handout.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

0. **REGOLA ZERO — QUESTO ARCO NON È ANCORA STATO GIOCATO.** Nonostante
   state.md §0 lo segni "✅ completato", il tavolo è fermo all'**Arco 07**
   (Piano della Terra in corso); seguono: resurrezione di Hella (ARC-07
   P3B), viaggio a 1.000 anni fa (ARC-07 P5), salto del Rubino al Cuore
   della Montagna (ARC-07 D16) e POI questa battaglia. Tutto ciò che
   state.md, coherence.md e i log dicono dell'arco 08 in poi è **canone
   preparato** (design): bersaglio di progetto, con gli esiti di battaglia
   **aperti ai dadi** (principio D13 del piano ARC-09: la preparazione
   quantifica le conseguenze di ogni ramo, mai il copione). La correzione
   del disallineamento è il task **A0, da eseguire per primo**.
1. **`campaign/state.md` vince** su qualunque altro file. Ogni modifica di
   canone va **appesa al changelog**, mai riscritta nella storia. (Dopo A0
   state.md distinguerà "giocato" da "preparato": la regola vale per
   entrambi i livelli.)
2. **Sistema D&D 3.5 SRD only** — niente 5e (no azioni bonus, no
   vantaggio/svantaggio meccanici, no legendary actions), niente lore FR
   post-1385 DR. Ambientazione Faerûn 1372 DR.
3. **Mai inventare** stat, poteri o conoscenze PNG: se serve un dato non
   presente, marcarlo `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare
   `skills/rumblingstone-campaign/references/campaign-coherence.md` e
   `campaign/state.md` §4 e §6 — ricordando che le righe sull'arco 08
   (es. coherence r.50-51) sono canone preparato, che si blocca davvero
   solo quando viene giocato. Gli artefatti canonici vivono in
   `PG/Artefatti/` (ARC-07 D9); Tordek porta anche la **Cintura della
   Devastazione** (ARC-07 D17: custom, slot cintura, funzione =
   Devastation Gauntlets).
6. Le mappe tattiche usano scala **1,5 m/quadretto** (convenzione repo) —
   vedi A4 per la sanatoria delle eccezioni.
7. Lingua: **italiano**, nomi meccanici 3.5 in italiano (CD non DC,
   Osservare non Spot, Nascondersi non Hide).
8. **Non cancellare file**: il default è il banner
   `> ⚠️ DEPRECATED (2026-07): ...` in testa (D12).

### Canone PREPARATO dell'arco (design da rispettare — si blocca al gioco)

| # | Elemento di design | Fonte |
|---|---|---|
| E1 | Hammerfist deve reggere l'assedio dell'avanguardia della Mano Rossa; l'esito atteso (su cui ARC-09 è costruito) è la **vittoria dei difensori** con avanguardia annientata/dispersa. I gradi dell'esito restano ai dadi (B1) | state.md §2.2 r.132; tutto ARC-09 |
| E2 | Bilancio atteso: **210 nani morti, 90 superstiti** guidati da Re Thorek (difensori iniziali: 300) | coherence.md r.50; state.md §2.5 r.202 |
| E3 | Fine battaglia = **Day 19** del March Clock (= caduta di Terrelton, sync point con ARC-09) | state.md §2.1 r.104 |
| E4 | **Il party arriva GIÀ al 13°** (ARC-07 D8) e **Hammerfist CONSOLIDA il 13°** (D9): il 14° arriva alla Battaglia di Rethmar, dove ARC-09 già lo prevede | DM 2026-07-02 |
| E5 | Alla vittoria: i 4 PG nominati **Custodi Eterni** da Re Thorek + **Cerimonia delle 100 Asce** (scena già scritta e a standard, D3) | state.md §4 r.246; Cerimonia-delle-100-Asce.md |
| E6 | **Struttura a due tempi (D6+D9)**: quasi tutta la battaglia si gioca col **flashback dei pregen "Eroi di Hammerfist"** (Borin Ferropugno, Dara Occhiolesto, Thorin Runaforte, Nala Cantapietre) — ricognizione e giorni d'assedio, che producono **BONUS per il finale, non PX**; i PG reali (**Rumbling Stones**) giocano **SOLO il finale**, riemergendo al **Cuore della Montagna al Giorno 3** (salto del Rubino, ARC-07 D16) come **artefici della riscossa** | DM 2026-07-02; Guida DM r.460-461, r.2150, r.2294; P6 ARC-07 r.621-660 |
| E7 | Capitana **Lythiel Alar-Wen** compare nella sessione finale e alla Cerimonia; consegna la Ghianda a Hella | state.md §4 r.251; Cerimonia §3.2 |
| E8 | Rapporto forze: **900 attaccanti vs 300 difensori** (3:1) | state.md r.185; Guida DM r.628/854 |

### Decisioni di canone GIÀ PRESE (D1-D14 — applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | Il drago dell'avanguardia si chiama **Fauci di Palude** (Black adult avanzato, GS 15) | Schede Personaggi §1; state.md §2.2 |
| D2 | **Thorek** = re di Hammerfist; **Thorik** = PG guerriero; **Thorin Runaforte** = pregen chierico. Tre persone diverse — mai fonderle (A10) | state.md §1; Schede §2-3 |
| D3 | La Cerimonia delle 100 Asce è il **file-ponte canonico** verso ARC-09 (già a standard: NON riscriverla) | Cerimonia-delle-100-Asce.md |
| D4 | Le **150 lance di Re Thorek** restano a Hammerfist e partono per Rethmar SOLO se gli hook politici di ARC-09 riescono (D10 del piano ARC-09) — nessun file ARC-08 le prometta incondizionatamente | state.md §2.5 r.202 |
| D5 | **Khorn** = ufficiale nanico designato (in ARC-09) a guidare le 150 lance — PNG distinto dai pregen | HOOKS-Thorik r.135/157 |
| D6 | Il flashback dei pregen è di **QUALCHE SETTIMANA prima** (la battaglia di 1.000 anni fa è ARC-07 P5, altra cosa); esiste perché i Rumbling Stones arrivano solo al finale — senza i pregen i giocatori perderebbero l'intero assedio. Ogni file che presenta i pregen deve dire quando si gioca il passaggio pregen→PG | DM 2026-07-02 |
| D7 | **state.md va corretto al giocato reale** (Arco 07 🟡 in corso, 08 ⬜ pianificato, 09 ⬜ preparato in anticipo) → task A0 | DM 2026-07-02 |
| D8 | **La resurrezione di Hella avviene TRA Forgia Eterna e Hammerfist** (ARC-07 P3B): all'inizio dell'arco 08 Hella ha il template Ibrido Treant + Collana dei Semi Eterni (con Durik nel terzo seme), Thorik ha il −2 CON, il Cuore di Moradin è speso, la Corona ha 3 gemme | DM 2026-07-02; ARC-07 D2/D16 |
| D9 | **Hammerfist consolida il 13°**: le sessioni pregen **NON danno PX ai Rumbling Stones — danno BONUS** quantificati per il finale (tabella di conversione in B1); il finale assegna PX da APL 13 dosati per NON scattare il 14° prima di Rethmar | DM 2026-07-02 |
| D10 | **Sorte di Fauci di Palude = RAMI CONDIZIONALI** (stile Ghostlord ARC-09 D7), MAI un fatto: ramo default = *fugge sotto i 50 pf* (statblock, hook nemesi); ramo alternativo = *ucciso dai PG* → −1 drago a Rethmar. Il carry-over dall'antenato Skullcrusher (ARC-07 B4) modifica i suoi numeri di partenza | default vincolante 2026-07-02 (dal Q1 v2) |
| D11 | **Contabilità perdite orda (scenario vittoria)**: 900 in campo, **~500 morti + ~400 dispersi = −900 effettivi** all'orda (i dispersi non si ricongiungono); UN solo totale corrente propagato a state.md, ledger e ARMATE-SYNC ARC-09 | default vincolante 2026-07-02 (dal Q2 v2) |
| D12 | File ridondanti/meta: **DEPRECARE con banner**, mai eliminare | DM 2026-07-02 (stessa policy ARC-07 D10) |
| D13 | **Lunapiena** = compagnia ranger **indipendente** dell'Elsir Vale (né Tiri Kitor né Sacred Forest), sopravvissuta, resta a presidio di Hammerfist → NON si somma ai difensori di Rethmar in ARMATE-SYNC. Lythiel resta l'unico canale col Sacred Forest | default vincolante `[INFERRED]` (dal Q3 v2) — il DM può emendare |
| D14 | **Eroi di Hammerfist post-battaglia** (se sopravvivono al giocato): Borin campione di Re Thorek a Hammerfist; Dara nelle staffette per Thorik (Cerimonia §6.4); Thorin Runaforte officia il culto dei caduti; Nala passa a Dauth (aggancio Torneo). **Khorn resta distinto** (D5) | default vincolante `[INFERRED]` (dal Q4 v2) — si blocca al gioco |

### Decisioni da chiedere al DM

**✅ NESSUNA bloccante.** D10-D14 sono default vincolanti già applicabili;
se il DM li emenda, l'engine aggiorna nel lotto successivo. Ogni dettaglio
mancante che emerga si flagga `[INFERRED — needs DM confirmation]`.

---

## §1 — LOTTO A: Incoerenze di canone e igiene dei file (priorità P0)

### A0. state.md (e satelliti) scritti in avanti rispetto al tavolo — D7, eseguire per primo
- **Problema** (il più grave del repo): state.md §0 segna 00-08
  "✅ completato", "Sessions completed: post-Hammerfist", March Clock
  "Day 19"; `campaign/sessions/2026-05-03_session-3.md` racconta una
  sessione post-Hammerfist mai giocata (Day 19-20, con giocatori
  presenti); coherence.md r.50-51 elenca l'esito della battaglia tra i
  "locked events". Il giocato reale è fermo all'Arco 07 (D7). Qualunque
  engine che segua "state.md vince" tratta il futuro come passato.
- **Azione**: (1) correggere il cruscotto §0: Arco 07 🟡 in corso (Piano
  della Terra), riga propria "Resurrezione di Hella + viaggio 1.000 anni"
  (ARC-07 D2), 08 ⬜ pianificato, tutte le righe 09 ⬜ "preparato in
  anticipo"; (2) intestazione: "Party APL" = **13** (ARC-07 D8),
  "Sessions completed" reale; (3) banner "⚠️ SCRITTO IN ANTICIPO —
  sessione non giocata" sul log 2026-05-03 (o spostarlo in
  `campaign/templates/`); (4) annotare in coherence.md che le righe 08+
  sono canone preparato; (5) riga di changelog che spiega l'intera
  correzione. NON toccare il materiale 08-09: resta preparazione valida.
- **Accettazione**: state.md §0 riflette il tavolo reale; nessun file
  marca come "giocato/locked" eventi non giocati; changelog scritto.

### A1. Sorte di Fauci di Palude scritta come fatto invece che come ramo — applicare D10
- **Problema**: quattro versioni contraddittorie, tutte come fatto
  compiuto, per una battaglia mai giocata: il ledger
  `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` r.139 lo dà
  "**morto** — rimosso dall'orda; −1 drago"; `campaign-coherence.md` r.51
  "**fugge gravemente ferito**; può tornare" e r.230 lo conta tra i draghi
  a Rethmar; state.md §2.2 r.123 lo elenca tra i 5 draghi; ARC-07
  `PortaleForgia-P6-INTEGRAZIONE` r.869 lo dà "Morto" a **GS 12** in un
  finale superato (piano ARC-07 A3).
- **Azione**: applicare **D10**: riscrivere le voci nei tracker in **forma
  condizionale a rami** (default: fugge sotto i 50 pf → ferito, può
  tornare; alternativa: ucciso → −1 drago a Rethmar); aggiungere la riga
  alla tabella "Conditional Additives" di state.md §2.3 (dove vivono i
  rami Ghostlord/Regiarix); allineare lo statblock in
  `00_Schede_dei_Personaggi...md` §1 (le Tattiche già prevedono la fuga)
  e predisporre il gancio per il carry-over ARC-07 B4 (A12). Changelog.
- **Accettazione**: `grep -rn "Fauci"` sui tracker mostra UNA sola logica
  (a rami, identica ovunque); nessun tracker afferma un esito come già
  avvenuto.

### A2. Contabilità perdite dell'orda: due aritmetiche di design — applicare D11
- **Problema**: state.md §2.2 r.132 "−500 → attivi ~9.400"; ledger r.81
  "−900 (vanguard intero) → 8.610". I file ARC-08 usano internamente 900
  attaccanti (Guida DM r.628; Lotto-1 r.281 e r.192 "conta precisa 900")
  e ~400 superstiti in rotta (Atlante-Mappe r.1034) — compatibili tra loro
  ma mai riconciliati coi tracker.
- **Azione**: applicare **D11** (900 in campo; ~500 morti; ~400 dispersi
  che non rientrano = −900 effettivi) in: state.md §2.2 (nota
  post-Hammerfist, scenario default), ledger §Day 19 (r.81 e r.139), e
  matrice esiti B1. Ricalcolare il running total del ledger dal Day 19 in
  poi; verificare che ARMATE-SYNC ARC-09 §2 parta dal numero giusto. Gli
  altri rami (vittoria costosa, caduta) vivono in B1, non nei tracker.
- **Accettazione**: un solo totale orda post-Day 19 (scenario default) in
  tutto il repo; changelog aggiornato.

### A3. XP e livelli: il testo promette 13°→15°, il canone è "13° consolidato" — applicare D9
- **Problema**: `hammerfist_encounters...-final.md` r.1382-1383: "GRAN
  TOTALE 34.400 XP (8.600 per PG) — abbastanza per portare PG da 13° a 15°
  livello". Il canone (E4/D9) è: il party ARRIVA al 13° e **Hammerfist lo
  consolida**; quasi tutta la battaglia la giocano i pregen (E6), che per
  D9 **non producono PX ma BONUS**.
- **Azione**: riscrivere la sezione "RIASSUNTO XP E RICOMPENSE" secondo
  D9: (1) sessioni-flashback coi pregen = **zero PX ai Rumbling Stones**;
  ogni obiettivo del flashback produce un **bonus quantificato per il
  finale** (rimando alla tabella di conversione B1); (2) il finale dei
  Rumbling Stones assegna PX da APL 13 **dosati per non scattare il 14°**
  prima di Rethmar, con riserva narrativa esplicita ("il grosso
  dell'esperienza matura nelle quest personali di ARC-09"); (3) stessa
  passata sulla sezione ricompense della Guida DM se duplicata; (4)
  verificare che gli EL del finale reggano ad APL 13 con artefatti
  (precedente: ARC-06 usava EL 17 su party di 13° — villans.md r.1).
- **Accettazione**: zero riferimenti a "13° a 15°" o "12→13"; zero PX
  alle sessioni pregen; il totale PX del finale non porta al 14°.

### A4. Scala delle mappe: 3 m vs 1,5 m per quadretto
- **Problema**: `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` dichiara
  "1 quadrato = 3 metri" (r.40, r.79, r.924) ma anche "Grid già
  ottimizzato standard D&D (5ft/1,5m)" (r.1234); `Hammerfist-L3-REVISED` è
  dichiarato "Griglie 1.5m"; la convenzione di repo è 1,5 m/quadretto. Un
  DM che stampa due mappe di file diversi ottiene scale diverse senza
  saperlo.
- **Azione**: passata su tutti i `Mappe/*` + sezioni-mappa dei file 00_:
  ogni mappa dichiara la scala in testa; le mappe **tattiche** normalizzate
  o ri-etichettate a 1,5 m/quadretto; le viste **strategiche** possono
  restare a 3 m+ MA etichettate "vista strategica — non per griglia". Dove
  la scala 3 m è strutturale (ASCII), non ridisegnare: etichettare.
- **Accettazione**: `grep -n "quadrat\|1,5\|3 metri" Mappe/*` mostra una
  dichiarazione per mappa; zero mappe tattiche senza scala.

### A5. Terminologia: DC inglesi, skill inglesi, lessico 5e colloquiale
- **Problema**: 36 occorrenze di `DC n` contro la convenzione CD,
  concentrate nei file Mappe (Lotto-1 r.191-194 "Osservare DC 15/20/25/30"
  — ibrido; L1-REVISED r.199 "Hide DC 20", r.242 "(advantage!)"); skill in
  inglese sparse (Spot, Hide, Climb, Balance, Strength check);
  "vantaggio/svantaggio/advantage" colloquiali (Atlante-Mappe r.352,
  r.902, r.1042, r.1076-1079) ambigui per un lettore 3.5/5e-misto.
- **Azione**: (1) DC→CD globale nell'arco; (2) skill → nomi italiani 3.5;
  (3) riformulare i "vantaggio/advantage" colloquiali in termini 3.5
  espliciti ("+2 di circostanza", "bonus del terreno rialzato").
- **Accettazione**: `grep -rn "DC [0-9]"` = 0 nell'arco;
  `grep -rni "advantage"` = 0; i "vantaggio" residui sono solo prosa.

### A6. File placeholder fuori canone: 01_ e 03_
- **Problema** (stessa classe di ARC-09 A12): due stub generici in inglese
  che **contraddicono il canone**. `01_MANO_ROSSA_MARCIA_VERSO_HAMMERFIST.md`
  inventa "Castle Red" (r.7), "River Styx" (r.23), "Ruins of Eldor" (r.24)
  — la marcia canonica parte dal Fane di Tiamat nel Shaar coi waypoint di
  state.md §2.1. `03_SESSIONE_INTERRUTTA_BATTAGLIA_INIZIA.md` è un recap
  generico di una sessione mai avvenuta. Manca qualsiasi `02_`.
- **Azione**: (1) riscrivere 01_ come vera scheda logistica
  dell'avanguardia di Fauci di Palude (900 unità: dove si stacca
  dall'orda, quando, che strada fa, opportunità di interferenza per il
  gruppo-ricognizione del flashback D6 — riusare Lotto-1 Ricognizione),
  ancorata al March Clock (B6); (2) deprecare 03_ con banner (D12); (3)
  risolvere il buco 02_ nello schema di rinomina (A9) senza inventare
  file riempitivi.
- **Accettazione**: `grep -rn "Castle Red\|Styx\|Eldor"` = 0 fuori dai
  banner; i due file o sono canonici o marcati DEPRECATED.

### A7. Code conversazionali AI in testa ai file
- **Problema**: 5 file aprono con la risposta dell'assistente che li
  generò: `00_Schede_dei_Personaggi...` r.1 ("Assolutamente. Ecco..."),
  `00_SCHEDE_DI_BATTAGLIA_E_REGISTRO_PERDITE` r.1-5 ("Certamente. Ho
  compreso..."), `00_ATLANTE VISIVO...md` r.1-3,
  `00_ATLANTE VISIVO...-complete.md` r.1, `00_battle_stats_maps-final.md`
  r.1-3.
- **Azione**: rimuovere le code e sostituirle con header standard: titolo,
  scopo, stato (canonico | deprecato), data revisione. NON toccare il
  contenuto sottostante in questo lotto.
- **Accettazione**: `grep -rn "^Assolutamente\|^Certamente\|^Perfetto"` = 0
  nell'arco; ogni file 00_ ha un header di stato.

### A8. Quattro generazioni di atlante/mappe sovrapposte — eleggere i master
- **Problema**: (a) `00_battle_stats_maps-final.md` (22 KB) è un
  **sottoinsieme letterale** di (b) `00_ATLANTE VISIVO...md` (29 KB) —
  stessa intro parola per parola; (c) `00_ATLANTE VISIVO...-complete.md`
  (33 KB) è una terza generazione (166 righe di diff da b); (d)
  `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` (48 KB, "16 mappe") è un
  quarto compendio. In parallelo `Mappe/Hammerfist-Lotto-{1,2,3}` vs
  `Mappe/Hammerfist-L{1,2,3}-REVISED-Ultra-Clear` sono due generazioni
  delle stesse mappe. Nessuno può sapere quale versione usare — e il DM
  dovrà giocarci.
- **Azione**: (1) **matrice di contenuto** (mappa × file); (2) eleggere UN
  master per categoria — proposta: `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
  master visivo + i tre `L*-REVISED-Ultra-Clear` master tattici; (3)
  banner DEPRECATED su (a), (b), (c) e sui `Lotto-*` superati, con
  puntatore al master; (4) aggiornare ogni riferimento interno. (D12:
  deprecare, non cancellare.)
- **Accettazione**: un solo file per contenuto senza banner; matrice in
  testa al master o nell'INDICE (B7); zero riferimenti attivi a file
  deprecati.

### A9. Naming dei file: prefissi incoerenti, buco 02_, immagini anonime
- **Problema**: sei file `00_`, poi `01_`, poi `03_` (manca `02_`); nomi
  con spazi e maiuscole miste; 15+ immagini
  `immage_campaign/Generated Image October 03, 2025 - ....webp` prive di
  aggancio alla mappa/scena (cartella con typo "immage").
- **Azione**: schema di rinomina coerente (`git mv`), es.
  `ARC08-00-INDICE.md`, `ARC08-01-GUIDA-DM.md`, `ARC08-02-SCONTRI.md`, …,
  aggiornando TUTTI i riferimenti (repo-wide). Le immagini si rinominano
  `hammerfist-sNN-descrizione.webp` solo DOPO la tabella immagine→mappa
  (C3). Cartella `immage_campaign` → `immagini` (o nota, se link esterni
  la usano: `[INFERRED]`).
- **Accettazione**: nessun buco di numerazione; script di verifica link a
  zero rotture; ogni immagine rinominata è citata da almeno un file.

### A10. Thorin / Thorik / Thorek: tre nomi a una lettera di distanza — applicare D2
- **Problema**: nel solo `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
  convivono 12 "Thorin", 15 "Thorik" e 24 "Thorek" — tre personaggi
  diversi (D2), refuso incrociato quasi certo, e un refuso qui mette in
  scena il personaggio sbagliato nel tempo sbagliato del racconto a due
  tempi (E6).
- **Azione**: audit occorrenza-per-occorrenza (63+ totali): il pregen
  agisce solo nel flashback e come PNG dopo; il PG solo dal finale; il re
  sempre come comandante difensore. Correggere i refusi; nota di
  disambiguazione in testa ai 2 file master ("Thorin=pregen, Thorik=PG,
  Thorek=re").
- **Accettazione**: audit documentato (tabella nel commit); nota presente;
  nessun pregen in scena nel finale e nessun PG nel flashback.

### A11. Due comandi elfici mai riconciliati (Lunapiena vs Lythiel) — applicare D13
- **Problema**: i file battaglia hanno il capitano elfico **Lunapiena** +
  Signore Ventolesto (gufo celestiale) + Orion Pelleorsa (druido); la
  Cerimonia canonizza **Lythiel** (Sacred Forest). Due comandi elfici alla
  stessa battaglia, mai riconciliati; nessuno ha scheda PNG (`PNG/` ha
  solo il cast ARC-09; `campaign/npcs/` non esiste).
- **Azione**: applicare **D13** (Lunapiena = compagnia indipendente
  dell'Elsir Vale, resta a Hammerfist, NON conta per Rethmar) nei file
  dove i due comandi si sfiorano (Guida DM §PNG, Schede §2, finale,
  Cerimonia già corretta); esplicitare in ARMATE-SYNC ARC-09 l'esclusione.
  Le schede PNG sono in B3.
- **Accettazione**: un solo assetto dei comandi elfici nel repo; nessun
  doppio conteggio in ARMATE-SYNC.

### A12. Eredità di Skullcrusher: "la Forgia ricorda le ferite" — [CROSS-ARC con ARC-07]
- **Problema**: nell'ARC-07 P5 i PG duellano con **Skullcrusher**
  (antenato di Fauci) e Moradin promette che ogni ferita inflitta
  all'antenato "la Forgia la ricorderà" contro il discendente
  (P5-DEFINITIVO-PARTE2 r.285); Aegis Fang "sente" il sangue (P6 r.746).
  **Nessun file ARC-08 lo implementa**.
- **Azione**: quando ARC-07 B4 consegna la **tabella di carry-over**
  (esito del duello → effetto quantificato su Fauci nel 1372), integrarla:
  nota nello statblock di Fauci (Schede §1) con puntatore, riga nella
  matrice esiti B1, menzione nel read-aloud del primo avvistamento (il
  "flashback genetico" di P2 ARC-07 r.1132). Non inventare i valori qui:
  la fonte è ARC-07 B4.
- **Accettazione**: lo statblock di Fauci rimanda alla tabella; ogni esito
  del P5 ha un effetto visibile a Hammerfist; zero valori duplicati tra i
  due archi.
- **➡️ ARC-07 B4 CONSEGNATO (2026-07-02)**: la tabella di carry-over esiste
  (`07_.../PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`) e lo **statblock
  di Fauci (Schede §FAUCI) rimanda già ad essa**. Restano da fare, lato
  ARC-08: la riga nella matrice esiti **B1** e la menzione nel read-aloud del
  primo avvistamento. I valori sono in ARC-07 B4 (non duplicarli qui),
  `[INFERRED]` in attesa di validazione DM.

---

## §2 — LOTTO B: Completamento contenuti per il gioco (priorità P1)

> Benchmark: la Cerimonia delle 100 Asce (D3) per tono e formato; i
> deliverable ARC-09 per struttura. Qui si prepara ciò che serve PRIMA di
> portare l'arco al tavolo: rami d'esito, ponte d'arrivo, cast su scheda,
> tesoro.

### B1. Matrice ESITI-ATTESI, contingenze e conversione flashback→bonus — il file più importante
- **Evidenza**: tutto ARC-09 assume la vittoria (E1), ma nessun file dice
  cosa succede se la battaglia va storta o costa più del previsto — il
  "SE FALLISCONO" che ARC-09 C3 ha standardizzato. E la meccanica D9
  (pregen → bonus) non ha ancora una tabella.
- **Azione**: creare `ARC08-ESITI-E-CONTINGENZE.md`: (1) **Vittoria
  piena** (design default: numeri D11, 90 superstiti, Custodi Eterni,
  Cerimonia D3); (2) **Vittoria costosa** (es. <50 superstiti, Re Thorek
  morto `[INFERRED]` → varianti su Cerimonia, 150 lance, hook ARC-09);
  (3) **Caduta di Hammerfist** (contingenza: evacuazione per i Passaggi
  Antichi — la mappa L3 esiste —, la Mano Rossa guadagna una base, delta
  sugli scenari ARMATE-SYNC); più i **rami di Fauci** (D10) col gancio
  carry-over (A12). (4) **Tabella di conversione D9 "esiti del flashback
  pregen → bonus al finale"**: per ogni obiettivo delle sessioni pregen
  (ricognizione riuscita, difese preparate, breccia contenuta, comandanti
  nemici logorati…) un bonus concreto per i Rumbling Stones (posizioni,
  PNG vivi, risorse, −CR a un incontro, intel), MAI PX. Ogni ramo con
  conseguenze numeriche su ARC-09; nessun ramo "game over".
- **Accettazione**: il DM arbitra qualunque esito senza improvvisare; ogni
  ramo aggancia i tracker con numeri; la tabella D9 copre tutti gli
  obiettivi del flashback; il ramo default coincide con E1-E8.

### B2. Ponte d'arrivo: dal Rubino al Cuore della Montagna (D8+D16) — [CROSS-ARC]
- **Evidenza**: la resurrezione vive in ARC-07 (master P3B, suo B2 — NON
  riscriverla qui). Il salto d'arrivo è verificato (ARC-07 D16): alla
  vittoria antica il **Rubino** riporta i PG al 1372 (P5-DEF §4.3) e i
  Rumbling Stones **riemergono al Cuore della Montagna, Giorno 3
  dell'assedio** (P6 r.621-660, Incontro 3B: Re Thorek morente a 8 pf, 90
  guerrieri, porte di mithral che cedono). Ma la **cucitura Sala della
  Forgia → Cuore della Montagna non è scritta da nessuna parte**, e
  nessun file dice come si gioca il passaggio dai pregen ai PG.
- **Azione**: creare `ARC08-PONTE-ARRIVO.md` (snello): (1) puntatore al
  master P3B ARC-07 = `07_.../PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md`
  (eletto in ARC-07 B2, §INTEGRAZIONE B2) — stato in uscita: Hella viva col
  template Ibrido Treant e la Collana/Durik (doni pieni del viaggio), Thorik
  −2 CON, Cuore di Moradin speso, Corona a 3 gemme; (2) la **cucitura D16**:
  il salto col Rubino come motore, il
  riemergere al Cuore della Montagna al momento più nero (regia
  dell'Incontro 3B, riusando P6 r.621-753 come fonte); (3) la regia del
  **passaggio pregen→PG** (D6): quando i giocatori lasciano gli Eroi,
  cosa sanno i PG di ciò che i pregen hanno visto, i bonus D9 maturati, e
  l'ingresso "da riscossa" (E6) con uno spotlight per ciascun PG (Durik
  compreso). È il momento registico più delicato dell'arco.
- **Accettazione**: la sequenza D8→D16→E6 è giocabile senza improvvisare;
  nessuna duplicazione col P3B ARC-07; meccaniche 3.5 esplicite; ogni
  invenzione flaggata.

### B3. Schede PNG mancanti (il cast di Hammerfist non esiste su disco)
- **Evidenza**: nessuna scheda per Re Thorek, Dana Forgiapietra, Grimjaw,
  Gorthak, Fauci di Palude, Lunapiena, Ventolesto, Orion Pelleorsa, i 4
  pregen, Khorn (D5, citato in 3+ file ARC-09). `PNG/` ha solo il cast
  ARC-09; `campaign/npcs/` non esiste. Le stat vivono solo nelle appendici
  dell'arco — introvabili per gli engine che seguono AGENTS.md.
- **Azione**: schede nel formato AGENTS.md (Role/Status/Location/
  Motivation/CR/Key stats/Notes) in `PNG/`, UNA per PNG, con Status
  pre-battaglia e campo "esiti possibili" (rami D10/D14/B1). Le stat si
  **puntano** alle appendici (fonte unica), non si duplicano. Aggiornare i
  file dell'arco perché citino le schede.
- **Accettazione**: ogni PNG nominato ha scheda; `grep` dei nomi in PNG/
  trova tutti; nessuna stat duplicata.

### B4. Tesoro/WBL dell'arco (party al 13° consolidato)
- **Evidenza**: le "RICOMPENSE" sono note sparse; nessun totale. Col party
  che entra ED esce al 13° (D9), il WBL di riferimento è ~110.000 mo/PG:
  l'arco deve dichiarare quanto mette in campo. L'audit ARC-09
  (`TESORO-WBL-AUDIT`) assume la ricchezza d'ingresso al 13° come data —
  questo lotto la fonda.
- **Azione**: audit del loot previsto + tabella tesoro per incontro in
  stile Paizo; se manca valore, proporre dove sta (armeria di Hammerfist,
  gratitudine di Re Thorek, bottino dell'avanguardia, equipaggiamento dei
  comandanti — tutto SRD/DMG, plot item flaggati). Chiudere con "ricchezza
  d'uscita ARC-08 = ingresso ARC-09" agganciata all'audit ARC-09.
- **Accettazione**: totale coerente col WBL ±20%; handoff esplicito.

### B5. Errata meccanica 3.5 (statblock e regole di massa)
- **Evidenza**: errori a campione in `00_Schede_dei_Personaggi...md`: il
  Cavaliere Hobgoblin (Guerriero 8/Guardia Nera 2) ha "Punire il Bene: +10
  (livello) ai danni" (r.110) — in 3.5 il bonus è il livello di **Guardia
  Nera**, quindi **+2**; "Aura di Disperazione" (r.111) si ottiene al
  **3°** livello di Guardia Nera, non al 2°; Fauci ha un "Soffio a Cono
  1/giorno" (r.77) che i draghi neri SRD non hanno (linea only) — flag
  house-rule o rimuovere. Il sistema di massa (AU/DU/PFU/Morale) non è mai
  stato verificato per action economy 3.5. Correggere ORA costa zero:
  l'arco non è giocato.
- **Azione**: produrre `ERRATA-ARC08-35-Verification.md` nel formato
  ARC-09: BAB/Lotta, CA contatto/impreparato, TS, CD, progressioni di
  classe/prestigio, GS dichiarati; **i 4 pregen verificati e pronti da
  stampare** (i giocatori li useranno direttamente, D6); il gear di
  Tordek aggiornato (Bracieri ai polsi + **Cintura della Devastazione**,
  ARC-07 D17); nota di compatibilità del sistema di massa (niente
  meccaniche 5e). Correzioni in place con nota.
- **Accettazione**: file errata nuovo; i due errori campione corretti;
  pregen verificati; gear di Tordek coerente con D17.

### B6. Ancoraggio al March Clock
- **Evidenza**: i file contano solo "Giorno 1/2/3" di battaglia; il March
  Clock fissa solo il punto finale (Day 19 = E3). Flashback, assedio e
  riemersione dei Rumbling Stones vanno collocati sul calendario, e il 01_
  riscritto (A6) e il ponte B2 ne hanno bisogno.
- **Azione**: mezza pagina (in B1 o nell'INDICE B7): "flashback pregen ≈
  Day 12-16 (ricognizione e primi giorni), assedio Giorni 1-3 ≈ Day 16-18,
  riemersione Rumbling Stones = Giorno 3 ≈ Day 18-19, vittoria e Cerimonia
  = Day 19 `[INFERRED — needs DM confirmation]`", con rimando a state.md
  §2.1 e al ledger. Scriverla UNA volta e puntarla da ARC-07 B6 (stessa
  tabella).
- **Accettazione**: una sola cronologia Day X-19 condivisa 07→08; nessun
  file che la contraddica; coerente con la finestra D6.

### B7. INDICE-GENERALE e DM-QUICKSTART dell'arco
- **Evidenza**: ARC-09 ha INDICE e QUICKSTART; l'arco 08 non ha né l'uno
  né l'altro — con 19 file markdown su 4 generazioni è la mappa che manca,
  e serve al DM PRIMA della prima sessione.
- **Azione**: creare `ARC08-00-INDICE.md`: (1) tabella file → ruolo →
  stato (master/deprecato/storico) dalla matrice A8; (2) **quickstart 1
  pagina**: la struttura a due tempi D6/D9 (flashback pregen con bonus →
  riemersione e finale dei RS), ordine di lettura (Guida DM → Scontri →
  Mappe master → Schede → Registro → Ponte B2 → Esiti B1), cosa stampare
  (pregen, registro perdite, mappe); (3) posizione nella campagna (dopo
  ARC-07 D2/D16, sync Day 19); (4) nota branch-per-group per gruppi
  futuri.
- **Accettazione**: ogni file compare con uno stato; il DM ha un percorso
  di preparazione completo in una pagina.

---

## §3 — LOTTO C: Da "coerente" a "memorabile" (priorità P2)

> L'arco ha già un'idea registica forte (i due tempi D6/D9) e il primo
> sistema di massa della campagna. Qui si consolidano al servizio del
> tavolo e di ARC-09/10.

### C1. Consolidare il sistema di combattimento di massa in UNA fonte
- **Evidenza**: le regole di massa vivono in 4 posti: `mass_combat_guide_Dm.md`
  (16 KB), `00_Schede_dei_Personaggi...` §4, le appendici della Guida DM
  (§7), le schede/registro PFU. ARC-09 D13/C1 le citano come "il
  precedente di Hammerfist" — ma non c'è un file canonico da puntare, e il
  DM dovrà arbitrarle dal vivo.
- **Azione**: eleggere `mass_combat_guide_Dm.md` come fonte unica (o
  estrarne una v2 pulita): filosofia, AU/DU/PFU, tabella Morale, danni
  strutturali, 1 pagina di quick-reference da tavolo; le altre copie
  diventano puntatori. Aggiungere il raccordo verso ARC-09: cosa STRUTTURA
  §9 ha ereditato e cosa ha cambiato (VP nascosti, eventi scelti dai PG),
  così i due sistemi non divergono in silenzio.
- **Accettazione**: una sola fonte normativa; copie che puntano ad essa;
  quick-reference stampabile; raccordo ARC-09 scritto.

### C2. Tabella delle conseguenze a lungo periodo (formato ARC-09 CONSEGUENZE-ECHI)
- **Evidenza**: conseguenze attese sparse: Fauci ferito che può tornare
  (D10, ramo default → candidato carta S2 all'EVENT-DECK di Rethmar o
  nemesi ARC-10, con l'**uovo di Fauci** di ARC-07 C3 come eco gemella),
  le 150 lance (D4), i pregen Eroi (D14), la **runa dei Custodi Eterni**
  (Cerimonia §2: simbolo fisico mai quantificato), il raid drow al tempio
  che prefigura la Fase 0 di Rethmar (state.md §3).
- **Azione**: sezione "Conseguenze a lungo periodo" in B1 nel formato
  della tabella echi del Torneo ARC-09 (evento → eco → quando riemerge →
  file che lo gestisce), con varianti per ramo d'esito. Quantificare la
  runa dei Custodi (proposta: +2 di circostanza a Diplomazia coi nani del
  Vale + ospitalità a Hammerfist `[INFERRED]`). Per il ramo "Fauci fugge",
  proporre la carta-evento "Il ritorno di Fauci di Palude" all'EVENT-DECK
  come S2 (solo hook e puntatore).
- **Accettazione**: tabella completa con varianti per ramo; runa
  quantificata o flaggata; nessun eco contraddice gli HOOKS ARC-09.

### C3. Atlante immagini: agganciare i 40+ webp alle mappe e scene
- **Evidenza**: `immage_campaign/` contiene ~40 webp di cui 15+ "Generated
  Image October 03, 2025 - ...". Gli atlanti contengono i prompt d'origine
  — ma nessuna tabella immagine↔mappa↔prompt: il materiale visivo è
  inutilizzabile a colpo d'occhio, proprio per l'arco da mostrare ai
  giocatori.
- **Azione**: tabella nel master visivo (A8) o nell'INDICE: file immagine
  → mappa/scena → sessione → prompt d'origine (se rintracciabile) →
  "quando mostrarla". Poi (solo poi) la rinomina A9 delle immagini
  identificate. Non riconducibili: sezione "non classificate", decisione
  al DM.
- **Accettazione**: ≥80% delle immagini classificate; ogni mappa master
  indica la sua immagine se esiste.

### C4. Handout giocatore (benchmark Paizo, formato HANDOUTS ARC-09)
- **Evidenza**: pezzi perfetti da dare in mano ai giocatori: le **schede
  dei 4 pregen** (che useranno nel flashback D6), la **runa di pietra dei
  Custodi Eterni** (Cerimonia §2: 5 cm, al collo), le **100 asce di
  adamantio rituale**, e manca una mappa giocatore della fortezza (le
  attuali sono tutte lato DM).
- **Azione**: sezione ARC-08 in `Arco-Post-Hammerfist-HANDOUTS.md` (o
  gemello nell'arco): (1) i 4 pregen stampabili 1 pagina l'uno (dopo B5);
  (2) la runa dei Custodi (descrizione + effetto C2 + prompt immagine);
  (3) il canto della cantillazione ("ricordato, ricordato, ricordato");
  (4) mappa giocatore della fortezza (L2 master senza informazioni
  segrete). Ogni handout con "quando darlo".
- **Accettazione**: handout stampabili; nessuno rivela info lato DM; i
  pregen giocabili senza aprire i file 00_.

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Esegui **un lotto per sessione**, nell'ordine. **A0 è primo e non
negoziabile** (sblocca la lettura corretta del repo per tutti gli engine).
Nessun lotto è bloccato: D10-D14 sono default vincolanti.

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | **A0 (state.md al giocato reale)** | editing mirato + changelog | — |
| 2 | A7 + A6 (code AI, placeholder 01_/03_) | editing mirato | — |
| 3 | A1 + A2 (rami Fauci D10 + contabilità D11) | editing mirato | A0 |
| 4 | A3 + A5 (XP/D9 + DC→CD/terminologia) | find/replace + editing | — |
| 5 | A8 (matrice contenuti + master + banner) | consolidamento | — |
| 6 | A4 (scale mappe, sui soli master) | editing mirato | A8 |
| 7 | A10 + A11 (Thorin/Thorik/Thorek + comandi elfici D13) | audit + editing | — |
| 8 | A9 (rinomina file, git mv, fix riferimenti repo-wide) | meccanico | A8 |
| 9 | B1 (matrice esiti + tabella conversione D9) | generativo | A1-A2 |
| 9b | A12 (eredità Skullcrusher su Fauci) | editing mirato | **ARC-07 B4 consegnato** |
| 10 | B2 (ponte d'arrivo D16 + regia pregen→PG) | generativo | **ARC-07 B2** (master P3B); B6 utile insieme |
| 11 | B6 + B7 (cronologia + INDICE/quickstart) | consolidamento | A8, A9, B1 |
| 12 | B5 (errata 3.5, pregen + Cintura D17) | verifica | — |
| 13 | B3 (schede PNG) | generativo | — |
| 14 | B4 (tesoro/WBL) | audit+generativo | — |
| 15 | C1 (sistema massa fonte unica + raccordo ARC-09) | consolidamento | — |
| 16 | C2 (conseguenze lungo periodo + runa Custodi) | generativo | B1 |
| 17 | C3 (atlante immagini) + coda rinomina immagini | classificazione | A8 |
| 18 | C4 (handout: pregen stampabili, runa, mappa giocatore) | generativo | B5, C2 |

**Regole anti-spreco** (identiche ad ARC-09): (1) passa all'engine SOLO
questo file + i file del lotto corrente + state.md §0-§4; (2) niente
riletture dell'intero arco; (3) dopo ogni lotto: `grep` di verifica del
criterio di accettazione, commit, riga di changelog in state.md se il
canone è cambiato; (4) aggiorna la checklist qui sotto.

### Checklist avanzamento

- [ ] A0 · [ ] A1 · [ ] A2 · [ ] A3 · [ ] A4 · [ ] A5 · [ ] A6 · [ ] A7 ·
  [ ] A8 · [ ] A9 · [ ] A10 · [ ] A11 · [ ] A12 (attende ARC-07 B4)
- [ ] B1 · [ ] B2 (attende ARC-07 B2) · [ ] B3 · [ ] B4 · [ ] B5 ·
  [ ] B6 · [ ] B7
- [ ] C1 · [ ] C2 · [ ] C3 · [ ] C4
- [x] D1…D14 — **tutte le decisioni DM acquisite (2026-07-02); nessuna
  domanda aperta bloccante** (D13-D14 sono default [INFERRED] emendabili)

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5**: l'idea registica del
racconto a due tempi (D6/D9) — i giocatori vivono l'assedio con i pregen
"Eroi di Hammerfist", accumulando bonus invece che PX, e poi riemergono
coi loro PG dal Cuore della Montagna come la riscossa in persona: un cold
open che nessun modulo ufficiale RHoD ha, saldato ad ARC-07 dal salto del
Rubino; il sistema di massa AU/DU/PFU con registro perdite stampabile (il
seme dell'impianto D13 di ARC-09); la Cerimonia delle 100 Asce, benchmark
di scrittura dell'intero repo; la mole di mappe ASCII multi-vista.

**Cosa lo separa dall'eccellenza**: (1) il repo **crede che l'arco sia già
stato giocato** — state.md, coherence e perfino un session log raccontano
un futuro mai avvenuto: finché A0 non li corregge, ogni engine legge il
canone al contrario; (2) gli esiti sono scritti come fatti invece che come
rami — e i tracker si contraddicono pure tra loro su Fauci di Palude e
sulle perdite (A1-A2, ora risolti da D10-D11 ma da propagare); (3) mancano
i pezzi che si usano al tavolo la sera stessa: il ponte d'arrivo col
Rubino (B2/D16), la tabella flashback→bonus (B1/D9), i pregen verificati e
stampabili (B5/C4), l'INDICE che dica quale delle quattro generazioni di
mappe usare (A8/B7); (4) terminologia ibrida EN/IT e scale mappe difformi
(A4-A5) sotto lo standard che ARC-09 ha fissato. Con A0+Lotto A il repo
torna a dire la verità; con B l'arco si porta al tavolo senza
improvvisare; con C il suo sistema di massa e i suoi cimeli lavorano per
Rethmar e oltre.
