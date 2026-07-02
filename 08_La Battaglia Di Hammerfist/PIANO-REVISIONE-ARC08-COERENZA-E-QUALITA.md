# PIANO DI REVISIONE ARC-08 (La Battaglia di Hammerfist) — Coerenza & Qualità

> **Versione**: v2.2 (2026-07-02) — prodotto da audit completo dell'arco.
> v2.2: recepisce ARC-07 D8 (party GIÀ al 13° — E4 superato, nuova Q6 sulla
> progressione) e i fatti ARC-06 (morte di Hella nella Stanza della Corona).
> La v1 assumeva l'arco già giocato (perché state.md lo segna ✅ completato);
> il DM ha chiarito (2026-07-02) che **il giocato reale è fermo all'Arco 07**
> (parte della Terra, Forgia Eterna) e che state.md è stato scritto in
> anticipo. La v2 reimposta il piano come revisione **pre-gioco**; la v2.1
> aggiunge i raccordi con l'audit dell'Arco 07 (vedi
> `07_il Portale Della Forgia Eterna/PIANO-REVISIONE-ARC07-COERENZA-E-QUALITA.md`,
> punti **[CROSS-ARC]**: eredità dell'Anno −1000, ponte resurrezione, P6).
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
> *Heroes of Battle* (3.5), AP Paizo PF1e per formato contingenze e handout.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

0. **REGOLA ZERO — QUESTO ARCO NON È ANCORA STATO GIOCATO.** Nonostante
   state.md §0 lo segni "✅ completato" e la campagna "post-Hammerfist", il
   tavolo è fermo all'**Arco 07** (Forgia Eterna, parte della Terra); seguono,
   nell'ordine: **resurrezione di Hella** (ponte 07→08, D8), poi la Battaglia
   di Hammerfist. Tutto ciò che state.md, coherence.md e i log dicono
   dell'arco 08 in poi è **canone preparato** (design), non esito giocato:
   va trattato come bersaglio di progetto, riscrivibile dal DM e — dove è un
   esito di battaglia — da lasciare **aperto ai dadi** (principio D13 del
   piano ARC-09: l'esito lo decide il tavolo, la preparazione quantifica le
   conseguenze di ogni ramo). La correzione di questo disallineamento è il
   task **A0**, da eseguire per primo.
1. **`campaign/state.md` vince** su qualunque altro file in caso di conflitto
   (regola del repo). Ogni modifica di canone va **appesa al changelog** di
   state.md, mai riscritta nella storia. (Dopo A0 state.md distinguerà
   "giocato" da "preparato": la regola si applica a entrambi i livelli.)
2. **Sistema D&D 3.5 SRD only** — niente 5e (no azioni bonus, no vantaggio/
   svantaggio meccanici, no legendary actions), niente lore FR post-1385 DR.
   Ambientazione Faerûn 1372 DR.
3. **Mai inventare** stat, poteri o conoscenze PNG: se serve un dato non
   presente, marcarlo `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare
   `skills/rumblingstone-campaign/references/campaign-coherence.md` e
   `campaign/state.md` §4 (chi sa cosa) e §6 (stato artefatti) — ricordando
   che le righe sull'arco 08 (es. coherence r.50-51) sono canone preparato,
   che si blocca davvero solo quando viene giocato.
6. Le mappe tattiche usano scala **1,5 m/quadretto** (convenzione repo) —
   vedi A4 per la sanatoria delle eccezioni.
7. Lingua: **italiano**, con i nomi meccanici 3.5 in italiano (CD non DC,
   Osservare non Spot, Nascondersi non Hide) come da convenzione ARC-09 §0.7.
8. **Non cancellare file** senza decisione esplicita (Q5): il default è il
   banner `> ⚠️ DEPRECATED (2026-07): ...` in testa, come fatto in ARC-09 A12.

### Canone PREPARATO dell'arco (design da rispettare — si blocca al gioco)

| # | Elemento di design | Fonte |
|---|---|---|
| E1 | Hammerfist deve reggere l'assedio dell'avanguardia della Mano Rossa; l'esito atteso (su cui ARC-09 è costruito) è la **vittoria dei difensori** con avanguardia annientata/dispersa. I gradi dell'esito restano ai dadi (vedi B1) | state.md §2.2 r.132; tutto ARC-09 |
| E2 | Bilancio atteso: **210 nani morti, 90 superstiti** guidati da Re Thorek (difensori iniziali: 300) | coherence.md r.50; state.md §2.5 r.202 |
| E3 | Fine battaglia = **Day 19** del March Clock (= caduta di Terrelton, sync point con ARC-09) | state.md §2.1 r.104 |
| E4 **v2.2** | ~~PG 12→13~~ **SUPERATO dal canone DM (2026-07-02): il party è GIÀ al 13°** durante l'ARC-07 (Bracieri risvegliati, Corona in risveglio — piano ARC-07 D8). La progressione di Hammerfist va rideterminata: vedi **Q6** | DM 2026-07-02; state.md §0 r.40 era forward-written e sbagliato |
| E5 | Alla vittoria: i 4 PG nominati **Custodi Eterni** da Re Thorek + **Cerimonia delle 100 Asce** (scena già scritta e a standard) | state.md §4 r.246; Cerimonia-delle-100-Asce.md |
| E6 | **Struttura a due tempi (D6)**: le prime sessioni sono un **flashback di qualche settimana prima** giocato dai giocatori con i pregen "Eroi di Hammerfist" (Borin Ferropugno, Dara Occhiolesto, Thorin Runaforte, Nala Cantapietre) — ricognizione e primi giorni d'assedio; i PG reali (**Rumbling Stones**) arrivano **quasi alla fine della battaglia** e sono gli **artefici della riscossa** dei nani. Origine della regia: ARC-07 P6-INTEGRAZIONE r.621-753 ("L'ARRIVO DEI RUMBLING STONES") | DM 2026-07-02; Guida DM r.460-461, r.2150, r.2294 |
| E7 | Capitana **Lythiel Alar-Wen** compare nella sessione finale e alla Cerimonia; consegna la Ghianda a Hella | state.md §4 r.251; Cerimonia §3.2 |
| E8 | Rapporto forze: **900 attaccanti vs 300 difensori** (3:1) | state.md r.185; Guida DM r.628/854 |

### Decisioni di canone GIÀ PRESE (applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | Il drago dell'avanguardia si chiama **Fauci di Palude** (Black adult avanzato, GS 15) | Schede Personaggi §1; state.md §2.2 |
| D2 | Il re di Hammerfist è **Thorek Hammerfist**; il PG guerriero è **Thorik**; il pregen chierico è **Thorin Runaforte**. Tre nomi simili, tre persone diverse — mai fonderli (vedi A10) | state.md §1; Schede §2-3 |
| D3 | La Cerimonia delle 100 Asce è il **file-ponte canonico** verso ARC-09 (già a standard: NON riscriverla, usarla come riferimento) | Cerimonia-delle-100-Asce.md |
| D4 | Le **150 lance di Re Thorek** restano a Hammerfist e partono per Rethmar SOLO se gli hook politici di ARC-09 riescono (sigillo Maewen + lettera; D10 del piano ARC-09) — nessun file ARC-08 deve prometterle incondizionatamente | state.md §2.5 r.202; ARC-09 D10 |
| D5 | **Khorn** è l'ufficiale nanico di Hammerfist designato (in ARC-09) a guidare le 150 lance — è un PNG distinto dai pregen Eroi | HOOKS-Thorik r.135/157; campaign-history.md |
| D6 | **Il flashback dei pregen è di QUALCHE SETTIMANA prima, non di 1000 anni** (la battaglia dell'Anno −1000 è un'altra cosa: si gioca nell'ARC-07 P5, coi PG reali nel passato — vedi piano ARC-07). Il prequel coi pregen esiste perché **i Rumbling Stones arrivano quasi alla fine della battaglia** (artefici della riscossa): senza i pregen i giocatori si perderebbero l'intero assedio. Ogni file che presenta i pregen deve dire chiaramente quando si gioca il passaggio pregen→PG | DM 2026-07-02 (risposta diretta, precisata) |
| D7 | **state.md va corretto al giocato reale**: Arco 07 🟡 in corso (parte della Terra), 08 ⬜ pianificato, 09 ⬜ preparato in anticipo. Il materiale 08-09 resta valido come preparazione | DM 2026-07-02 → task A0 |
| D8 | **La resurrezione di Hella avviene TRA la Forgia Eterna e Hammerfist** (ponte 07→08): all'inizio dell'arco 08 Hella ha già il template Ibrido Treant, Thorik ha già il −2 CON permanente, il Cuore di Moradin è già speso | DM 2026-07-02 (risposta diretta) |

### Decisioni di canone da chiedere al DM (bloccano solo i task marcati)

| # | Domanda | Proposta di default (se il DM non decide diversamente) |
|---|---|---|
| Q1 | **Sorte di Fauci di Palude**: i tracker si contraddicono già ORA come design — il ledger `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` r.139 lo dà "**morto** — rimosso dall'orda; −1 drago" come fatto compiuto; `campaign-coherence.md` r.51 dice "**fugge gravemente ferito**; può tornare" e r.230 lo conta tra i draghi a Rethmar; state.md §2.2 r.123 lo elenca tra i 5 draghi. **Quarta versione [CROSS-ARC]**: ARC-07 `Portaleforgia-P6-INTEGRAZIONE` r.869 lo dà "Morto" a **GS 12** in un finale-campagna superato dagli Archi 08-09 (vedi piano ARC-07 A3) | Trattarlo **a rami condizionali** stile Ghostlord (ARC-09 D7), perché l'esito lo decideranno i dadi: ramo default di design = *fugge sotto i 50 PF* (come da statblock, hook nemesi per Rethmar/ARC-10); ramo alternativo = *ucciso dai PG* → −1 drago a Rethmar. Tutti i tracker riscritti in forma condizionale; il profilo GS 12 di P6 marcato storico (piano ARC-07 A3) |
| Q2 | **Contabilità perdite dell'orda** in caso di vittoria: state.md §2.2 r.132 dice "−500 → attivi ~9.400"; il ledger r.81 dice "−900 (vanguard intero) → 8.610". I file ARC-08 dicono 900 attaccanti e ~400 superstiti in rotta (Atlante-Mappe r.1034) | Formalizzare "**~500 morti + ~400 dispersi = −900 effettivi** all'orda" (i dispersi non si ricongiungono) e ricalcolare UN solo totale corrente propagandolo a state.md, ledger e ARMATE-SYNC ARC-09 (i 5 scenari difensori dipendono da questo numero) |
| Q3 | **Chi sono i ranger elfici di "Capitano Lunapiena"?** I file battaglia hanno un capitano elfico (Lunapiena) + Signore Ventolesto (gufo celestiale) + Orion Pelleorsa (druido); la Cerimonia canonizza Lythiel (Sacred Forest). Due comandi elfici alla stessa battaglia, mai riconciliati; nessuno ha scheda PNG | Lunapiena = compagnia ranger **indipendente** dell'Elsir Vale (né Tiri Kitor né Sacred Forest), che a fine battaglia resta a presidio di Hammerfist (quindi NON va sommata ai difensori di Rethmar in ARMATE-SYNC). Lythiel resta l'unico canale col Sacred Forest `[INFERRED]` |
| Q4 | **Ruolo post-battaglia previsto per i 4 Eroi di Hammerfist (pregen)?** Dopo il flashback (D6) restano PNG vivi sul campo: nessun file dice che ne è di loro. Sono un asset narrativo pronto: ARC-09 ha PNG nanici senza volto (i 300 mercenari, il presidio) | Se sopravvivono al giocato: Borin campione di Re Thorek a Hammerfist; Dara ed esploratori assorbiti nelle staffette per Thorik (Cerimonia §6.4); Thorin Runaforte officia il culto dei caduti; Nala passa a Dauth (aggancio Torneo). **Khorn resta distinto** (D5). Da preparare come proposta, si blocca al gioco `[INFERRED]` |
| Q5 | **File ridondanti/meta: deprecare o eliminare?** Riguarda le 3 generazioni di atlante doppione (A8), `combat_prompts_guide.md` (guida ai prompt AI usati per generare il sistema — artefatto storico di lavorazione, non materiale di gioco) e i placeholder 01_/03_ (A6) | **Deprecare con banner**, mai eliminare (valore storico, regola §0.8). L'eliminazione fisica solo su ordine esplicito del DM |
| Q6 | **Progressione di livello a Hammerfist (cascata da ARC-07 D8)**: il party arriva alla battaglia **già al 13°**, ma tutto il canone preparato a valle assumeva 12→13 qui e APL 13 all'inizio di ARC-09 (i cui lotti B5/B6 sono già stati auditati su 13→16) | Due opzioni: (a) **Hammerfist = 13→14** e ARC-09 slitta di +1 (richiede una passata di ri-budget su ARC-09: quest a 14, Rethmar a 15 — costosa); (b) **Hammerfist consolida il 13°** (XP calibrati perché il 14° arrivi dove ARC-09 già lo prevede, alla Battaglia di Rethmar) — **consigliata**: preserva l'intero impianto ARC-09 già verificato. In entrambi i casi A3 riscrive gli XP di conseguenza |

---

## §1 — LOTTO A: Incoerenze di canone e igiene dei file (priorità P0)

### A0. state.md (e satelliti) scritti in avanti rispetto al tavolo — D7, eseguire per primo
- **Problema** (il più grave del repo, non solo dell'arco): state.md §0 segna
  00-08 "✅ completato", "Sessions completed: post-Hammerfist", March Clock
  "Day 19"; `campaign/sessions/2026-05-03_session-3.md` racconta una sessione
  post-Hammerfist (Day 19-20, pattuglia del Ghostlord) con tanto di giocatori
  presenti; coherence.md r.50-51 elenca l'esito della battaglia tra i "locked
  events". Ma il giocato reale è fermo all'Arco 07 (D7). Qualunque engine che
  segua la regola "state.md vince" sta trattando il futuro come passato.
- **Azione**: (1) correggere il cruscotto state.md §0: Arco 07 🟡 in corso
  (parte della Terra), ponte "Resurrezione di Hella" (D8) come riga propria,
  08 ⬜ pianificato, tutte le righe 09 ⬜ "preparato in anticipo"; (2)
  aggiornare l'intestazione ("Sessions completed", "Party APL" = **13**,
  canone DM 2026-07-02 — ARC-07 D8); (3) marcare il session log
  2026-05-03 con banner "⚠️ SCRITTO IN ANTICIPO — sessione non giocata,
  esempio/preparazione" (o spostarlo in `campaign/templates/`); (4) annotare
  in coherence.md che le righe 08+ sono canone preparato; (5) riga di
  changelog che spiega l'intera correzione. NON toccare il materiale 08-09:
  resta preparazione valida.
- **Accettazione**: state.md §0 riflette il tavolo reale; nessun file marca
  come "giocato/locked" eventi non giocati; changelog scritto.

### A1. Sorte di Fauci di Palude scritta come fatto invece che come ramo — Q1
- **Problema**: vedi Q1. Tre tracker strategici (state.md §2.2, ledger r.139,
  coherence.md r.51/230) danno TRE versioni della sorte del drago — e tutte e
  tre come **fatto compiuto**, per una battaglia mai giocata. Il conteggio
  draghi di Rethmar (ARMATE-SYNC ARC-09) dipende da qui.
- **Azione**: applicare Q1: riscrivere le voci nei tre tracker in **forma
  condizionale a rami** (default design: fugge sotto i 50 PF → ferito, può
  tornare; alternativa: ucciso → −1 drago a Rethmar), aggiungere la riga
  corrispondente alla tabella "Conditional Additives" di state.md §2.3 (dove
  già vivono i rami Ghostlord/Regiarix), e allineare lo statblock in
  `00_Schede_dei_Personaggi...md` §1 (le Tattiche già prevedono la fuga).
  Riga di changelog in state.md.
- **Accettazione**: `grep -rn "Fauci"` sui tracker mostra UNA sola logica (a
  rami, identica ovunque); nessun tracker afferma un esito come già avvenuto.

### A2. Contabilità perdite dell'orda: due aritmetiche di design — Q2
- **Problema**: vedi Q2 (−500 vs −900; attivi ~9.400 vs 8.610). In più i file
  ARC-08 usano internamente 900 attaccanti (Guida DM r.628; Lotto-1 r.281 e
  r.192 "conta precisa 900") e ~400 superstiti in rotta (Atlante-Mappe r.1034)
  — numeri compatibili tra loro ma mai riconciliati con i tracker.
- **Azione**: applicare Q2: una sola formula per lo scenario-vittoria
  (proposta: 900 in campo, ~500 morti, ~400 dispersi che non rientrano)
  scritta in: state.md §2.2 (nota post-Hammerfist), ledger §Day 19 (r.81 e
  r.139), e nella matrice esiti di B1. Ricalcolare il running total del
  ledger dal Day 19 in poi e verificare che ARMATE-SYNC ARC-09 §2 parta dal
  numero giusto. Gli altri rami della matrice B1 (vittoria costosa, caduta)
  avranno le loro varianti dichiarate lì, non nei tracker.
- **Accettazione**: un solo totale orda post-Day 19 (scenario default) in
  tutto il repo; changelog aggiornato.

### A3. XP e livelli: il testo promette 13°→15°, il canone reale è "ingresso al 13°" — dipende da Q6
- **Problema**: `hammerfist_encounters...-final.md` r.1382-1383: "GRAN TOTALE
  34.400 XP (8.600 per PG) — abbastanza per portare PG da 13° a 15° livello".
  Il canone reale (E4 v2.2, ARC-07 D8) è: il party ARRIVA al 13°; la
  progressione in uscita dipende da Q6 (consigliata: consolidare il 13°,
  livello 14 alla Battaglia di Rethmar come ARC-09 già prevede). In più le
  prime sessioni le giocano i pregen (D6/E6): l'attribuzione degli XP al
  party va chiarita.
- **Azione**: riscrivere la sezione "RIASSUNTO XP E RICOMPENSE": budget per
  **APL 13**, nota esplicita "sessioni-flashback = XP ai pregen (non
  cumulano sul party); sessioni col party reale + bonus narrativo = XP ai
  Rumbling Stones, dimensionati secondo **Q6**
  `[needs DM confirmation sui totali]`". Stessa passata sulla sezione
  ricompense della Guida DM se duplicata; ricontrollare che gli EL degli
  incontri del party reale reggano ad APL 13 con artefatti (il precedente:
  ARC-06 usava EL 17 su party di 13° — villans.md r.1).
- **Accettazione**: nessun riferimento residuo a "13° a 15°" né a "12→13";
  attribuzione pregen/party esplicita; numeri compatibili con Q6 risolta.

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
  solo nome della campagna (e descrive una sessione mai avvenuta). Manca
  inoltre qualsiasi file `02_`.
- **Azione**: (1) riscrivere 01_ come vera scheda logistica dell'avanguardia
  di Fauci di Palude (900 unità: da dove si stacca dall'orda, quando, che
  strada fa per Hammerfist, opportunità di interferenza per il gruppo
  ricognizione del flashback D6 — riusare i contenuti di Lotto-1
  Ricognizione), ancorata al March Clock (vedi B6); (2) deprecare 03_ con
  banner (Q5); (3) risolvere il buco 02_ nello schema di rinomina (A9),
  senza inventare un file solo per riempire il numero.
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
  usare — è il rischio multi-engine già visto in ARC-09 §5.(1). E qui il DM
  dovrà **giocarci**: la confusione costa al tavolo.
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
  lasciare con nota, se link esterni al repo la usano:
  `[INFERRED — needs DM confirmation]`).
- **Accettazione**: nessun buco di numerazione; uno script di verifica link
  (come ARC-09 A8) passa a zero rotture; ogni immagine rinominata è citata
  da almeno un file.

### A10. Thorin / Thorik / Thorek: tre nomi a una lettera di distanza
- **Problema**: nel solo `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
  convivono 12 "Thorin", 15 "Thorik" e 24 "Thorek". Sono tre personaggi
  diversi (D2: pregen chierico / PG / re) e la probabilità di refuso
  incrociato è altissima — e un refuso qui mette in scena il personaggio
  sbagliato nel tempo sbagliato del racconto a due tempi (D6).
- **Azione**: audit occorrenza-per-occorrenza dei tre nomi in tutto l'arco
  (63+ occorrenze totali): per ciascuna verificare dal contesto quale
  personaggio è inteso (il pregen agisce solo nel flashback e come PNG dopo;
  il PG solo dall'ingresso dei Rumbling Stones in poi; il re sempre come
  comandante difensore). Correggere i refusi; aggiungere in testa ai 2 file
  master una **nota di disambiguazione** ("Thorin=pregen, Thorik=PG,
  Thorek=re").
- **Accettazione**: audit documentato (tabella occorrenze corrette nel
  commit); nota di disambiguazione presente; nessun pregen in scena dopo il
  passaggio ai PG reali e viceversa.

### A11. Due comandi elfici mai riconciliati (Lunapiena vs Lythiel) — dipende da Q3
- **Problema**: vedi Q3. In più nessuno dei PNG alleati della battaglia
  (Lunapiena, Ventolesto, Orion Pelleorsa, Dana Forgiapietra) ha una scheda
  in `PNG/` (la cartella contiene solo PNG ARC-09) né in `campaign/npcs/`
  (che **non esiste** nonostante AGENTS.md la dichiari).
- **Azione**: applicare Q3 nei file dove i due comandi si sfiorano (Guida DM
  §PNG chiave, Schede §2, sessione finale, Cerimonia già corretta);
  esplicitare in ARMATE-SYNC ARC-09 che i ranger di Lunapiena NON sono tra i
  difensori di Rethmar (o il contrario, se il DM decide diversamente). La
  creazione delle schede PNG è in B3 — qui solo la coerenza dei riferimenti.
- **Accettazione**: un solo assetto dei comandi elfici in tutto il repo;
  nessun doppio conteggio in ARMATE-SYNC.

### A12. Eredità dell'Anno −1000: "la Forgia ricorda le ferite" — [CROSS-ARC con ARC-07]
- **Problema**: nell'ARC-07 P5 i PG combattono l'**antenato di Fauci di
  Palude** all'assedio antico di Hammerfist, e Moradin promette: *"Ogni
  ferita che infliggi ora all'antenato, la mia Forgia la ricorderà quando
  affronterai il discendente"* (P5-DEFINITIVO-PARTE2 r.285); Aegis Fang
  "sente" il sangue del discendente (P6 r.746). **Nessun file ARC-08 lo
  implementa**: lo statblock di Fauci di Palude (Schede §1) ignora il
  viaggio temporale.
- **Azione**: quando il piano ARC-07 consegna la **tabella di carry-over**
  (suo task B4: esito del duello antico → effetto quantificato su Fauci nel
  1372), integrarla qui: nota nello statblock di Fauci (Schede §1) con
  puntatore alla tabella, riga nella matrice esiti B1, e menzione nel
  read-aloud del primo avvistamento del drago (il "flashback genetico" di
  P2 r.1132). Non inventare i valori qui: la fonte è ARC-07 B4.
- **Accettazione**: lo statblock di Fauci rimanda alla tabella carry-over;
  ogni esito del P5 ha un effetto visibile nella battaglia di Hammerfist;
  zero valori duplicati tra i due archi.

---

## §2 — LOTTO B: Completamento contenuti per il gioco (priorità P1)

> Benchmark: la Cerimonia delle 100 Asce (D3) per tono e formato; i
> deliverable ARC-09 (`ERRATA-*`, `TESORO-WBL-AUDIT`, sidebar "SE
> FALLISCONO") per struttura. Qui si prepara ciò che serve PRIMA di portare
> l'arco al tavolo: rami d'esito, ponte narrativo, cast su scheda, tesoro.

### B1. Matrice ESITI-ATTESI e contingenze — il file più importante del lotto
- **Evidenza**: tutto ARC-09 assume la vittoria a Hammerfist (E1), ma
  nell'arco non esiste alcun file che dica cosa succede se la battaglia va
  storta o costa più del previsto — il "SE FALLISCONO" che ARC-09 C3 ha già
  standardizzato per le sue quest. Per una battaglia che si gioca ai dadi è
  il pezzo mancante più pericoloso.
- **Azione**: creare `ARC08-ESITI-E-CONTINGENZE.md` con la matrice a rami
  (formato ESITI ARC-09): (1) **Vittoria piena** (design default: numeri
  Q2, 90 superstiti, Custodi Eterni, Cerimonia D3); (2) **Vittoria costosa**
  (es. <50 superstiti, Re Thorek ferito/morto `[INFERRED]` → varianti su
  Cerimonia, 150 lance, hook ARC-09); (3) **Caduta di Hammerfist**
  (contingenza: i PG evacuano i civili per i Passaggi Antichi — la mappa
  L3 esiste già —, la Mano Rossa guadagna una base, delta quantificato sugli
  scenari ARMATE-SYNC di Rethmar); più i rami di Fauci di Palude (Q1). Ogni
  ramo con conseguenze numeriche su ARC-09, nessun ramo "game over".
- **Accettazione**: il DM può arbitrare qualunque esito senza improvvisare;
  ogni ramo aggancia i tracker con numeri; il ramo default coincide col
  canone preparato (E1-E8).

### B2. Ponte 07→08: dall'uscita della Forgia all'arrivo a Hammerfist (D8) — [CROSS-ARC]
- **Evidenza**: per D8 la sequenza è: fine Forgia Eterna → **resurrezione di
  Hella** → Battaglia di Hammerfist. La scena della resurrezione **esiste
  già nell'ARC-07** (file `P3B-ResurrezioneHella-*`, in 4 versioni: la sua
  elezione a master è il task B2 del piano ARC-07 — NON riscriverla qui).
  Quello che manca lato ARC-08 è il **raccordo**: nessun file dice come i
  Rumbling Stones arrivano alla battaglia quasi conclusa (E6) né come si
  gioca il passaggio dai pregen ai PG reali.
- **Azione**: creare `ARC08-PONTE-ARRIVO.md` (snello): (1) puntatore al
  master P3B di ARC-07 per la resurrezione (stato in uscita: Hella viva con
  template Treant, Thorik −2 CON, Cuore di Moradin speso, Corona a 3 gemme);
  (2) il viaggio e l'aggancio con l'assedio in corso (perché arrivano
  proprio allora — le visioni della Forgia? il canto di Aegis Fang che
  "sente" Fauci? `[INFERRED — needs DM confirmation]`); (3) la regia del
  **passaggio pregen→PG** (D6): quando i giocatori lasciano gli Eroi, come
  il flashback si salda al presente, cosa sanno i PG di ciò che i pregen
  hanno visto, e l'ingresso "da riscossa" (E6) con spotlight per ciascun PG.
  È il momento registico più delicato dell'arco.
- **Accettazione**: la sequenza D8→E6 è giocabile senza improvvisare;
  nessuna duplicazione col P3B di ARC-07; meccaniche 3.5 esplicite; ogni
  invenzione flaggata.

### B3. Schede PNG mancanti (il cast di Hammerfist non esiste su disco)
- **Evidenza**: nessuna scheda per Re Thorek, Dana Forgiapietra, Grimjaw,
  Gorthak, Fauci di Palude, Lunapiena, Ventolesto, Orion Pelleorsa, né per i
  4 Eroi pregen, né per Khorn (D5, citato in 3+ file ARC-09). `PNG/` ha solo
  il cast ARC-09; `campaign/npcs/` non esiste. Le stat vivono solo dentro le
  appendici dell'arco — introvabili per gli engine che seguono AGENTS.md
  ("Check campaign/npcs/ before describing NPCs").
- **Azione**: creare le schede nel formato AGENTS.md (Role/Status/Location/
  Motivation/CR/Key stats/Notes) in `PNG/` (convenzione di fatto del repo),
  UNA per PNG, con Status pre-battaglia e campo "esiti possibili" (rami Q1/
  Q4/B1). Le stat si **puntano** alle appendici dell'arco (fonte unica, come
  ARC-09 B3 fece col Ghostlord), non si duplicano. Aggiornare i file
  dell'arco perché citino le schede.
- **Accettazione**: ogni PNG nominato nell'arco ha scheda; `grep` dei nomi
  in PNG/ trova tutti; nessuna stat duplicata.

### B4. Tesoro/WBL dell'arco (party al 13°, Q6)
- **Evidenza**: le "RICOMPENSE" dell'arco sono note sparse; nessun totale.
  Col party che ENTRA al 13° (E4 v2.2), il WBL 3.5 di riferimento è
  ~110.000 mo/PG al 13° (→~150.000 al 14° se Q6 = opzione a): l'arco deve
  dichiarare quanto mette in campo. L'audit ARC-09
  (`Arco-Post-Hammerfist-TESORO-WBL-AUDIT.md`) assume la ricchezza
  d'ingresso al 13° come data — questo lotto la fonda.
- **Azione**: audit del loot previsto (sezione ricompense della guida
  scontri) + tabella tesoro per incontro in stile Paizo; se manca valore,
  proporre dove sta (armeria di Hammerfist, gratitudine di Re Thorek,
  bottino dell'avanguardia, equipaggiamento dei comandanti nemici — tutto
  SRD/DMG, plot item flaggati). Chiudere con la riga "ricchezza d'uscita
  ARC-08 = ricchezza d'ingresso ARC-09" agganciata all'audit ARC-09.
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
  stato verificato per action economy 3.5. Correggere ORA costa zero:
  l'arco non è stato giocato (D7).
- **Azione**: produrre `ERRATA-ARC08-35-Verification.md` nello stesso formato
  degli errata ARC-09: BAB/Lotta, CA contatto/impreparato, TS, CD dei poteri,
  progressioni di classe/prestigio, GS dichiarati vs contenuto (anche per i
  4 pregen, che i giocatori useranno direttamente — D6); per il sistema di
  massa una nota di compatibilità (azioni standard/movimento, niente
  meccaniche 5e). Correzioni in place con nota.
- **Accettazione**: file errata nuovo; i due errori campione corretti; i 4
  pregen verificati e pronti da stampare.

### B6. Ancoraggio al March Clock (l'arco precede il sistema a doppio clock)
- **Evidenza**: i file dell'arco contano solo "Giorno 1/2/3" di battaglia
  (+ sessioni); il March Clock (state.md §2.1, canon 2026-05-05) fissa solo
  il punto finale (Day 19 = E3). Il lettore non può collocare flashback,
  ricognizione e assedio sul calendario di campagna, e il 01_ riscritto (A6)
  e il ponte B2 ne hanno bisogno.
- **Azione**: mezza pagina (in B1 o nell'INDICE B7): "flashback pregen ≈
  Day 12-16 (ricognizione e primi giorni), arrivo Rumbling Stones ≈ Day
  17-18, vittoria e Cerimonia = Day 19 `[INFERRED — needs DM confirmation]`",
  con rimando a state.md §2.1 e al ledger. Propagare l'ancora nei file
  master (una riga in testa, non un find/replace invasivo).
- **Accettazione**: una sola cronologia Day X-19 dichiarata; nessun file che
  la contraddica; coerente con la finestra del flashback D6 ("qualche
  settimana prima").

### B7. INDICE-GENERALE e DM-QUICKSTART dell'arco
- **Evidenza**: ARC-09 ha INDICE-GENERALE e DM-QUICKSTART; l'arco 08 non ha
  né l'uno né l'altro — con 19 file markdown su 4 generazioni, è la mappa
  che manca. E poiché l'arco va ancora giocato, serve al DM PRIMA della
  prima sessione.
- **Azione**: creare `ARC08-00-INDICE.md`: (1) tabella file → ruolo →
  stato (master/deprecato/storico) — riusa la matrice A8; (2) **quickstart
  di 1 pagina**: la struttura a due tempi D6 (flashback pregen → PG reali),
  ordine di lettura (Guida DM → Scontri → Mappe master → Schede → Registro
  → Ponte B2 → Esiti B1), cosa stampare (pregen, registro perdite, mappe);
  (3) posizione dell'arco nella campagna (dopo D8, sync Day 19 con ARC-09);
  (4) nota branch-per-group per eventuali gruppi futuri.
- **Accettazione**: ogni file dell'arco compare nell'INDICE con uno stato;
  un DM ha un percorso di preparazione completo in una pagina.

---

## §3 — LOTTO C: Da "coerente" a "memorabile" (priorità P2)

> L'arco ha già un'idea registica forte (il racconto a due tempi D6) e il
> primo sistema di massa della campagna. Qui si consolidano e si mettono al
> servizio del tavolo e di ARC-09/10. Riferimenti: Heroes of Battle, il
> Piano ARC-09 (D13, C1, C7 — che citano Hammerfist come "precedente").

### C1. Consolidare il sistema di combattimento di massa in UNA fonte
- **Evidenza**: le regole di massa vivono in 4 posti: `mass_combat_guide_Dm.md`
  (16 KB), `00_Schede_dei_Personaggi...` §4 ("Guida al Combattimento di
  Massa"), le appendici della Guida DM (§7) e le schede/registro PFU. ARC-09
  D13 e C1 le citano come "il precedente narrativo di Hammerfist" e
  STRUTTURA §9 (Rethmar) vi si ispira — ma non c'è un file canonico da
  puntare, e il DM dovrà arbitrarle dal vivo.
- **Azione**: eleggere `mass_combat_guide_Dm.md` come fonte unica (o
  estrarne una v2 pulita): filosofia, AU/DU/PFU, tabella Morale, danni
  strutturali, 1 pagina di quick-reference da tavolo; le altre copie
  diventano puntatori (banner "regole canoniche in ..."). Aggiungere il
  paragrafo di raccordo verso ARC-09: cosa STRUTTURA §9 ha ereditato e cosa
  ha cambiato (VP nascosti, eventi scelti dai PG — D13), così i due sistemi
  non divergono in silenzio.
- **Accettazione**: una sola fonte normativa; le copie puntano ad essa;
  quick-reference stampabile; raccordo ARC-09 scritto.

### C2. Tabella delle conseguenze a lungo periodo (formato ARC-09 CONSEGUENZE-ECHI)
- **Evidenza**: le conseguenze attese dell'arco esistono ma sparse: Fauci
  ferito che può tornare (Q1, ramo default → candidato carta evento S2
  all'EVENT-DECK di Rethmar o nemesi ARC-10), le 150 lance (D4), i pregen
  Eroi (Q4), la runa dei Custodi Eterni (Cerimonia §2 ne fa un simbolo
  fisico — mai quantificato meccanicamente), il raid drow al tempio che
  prefigura la Fase 0 di Rethmar (state.md §3).
- **Azione**: sezione "Conseguenze a lungo periodo" in B1 nel formato della
  tabella echi del Torneo ARC-09 (evento → eco → quando riemerge → file che
  lo gestisce), con varianti per ramo d'esito. Quantificare il beneficio
  meccanico della runa dei Custodi (proposta: +2 di circostanza a Diplomazia
  con i nani del Vale + ospitalità a Hammerfist;
  `[INFERRED — needs DM confirmation]`). Per il ramo "Fauci fugge",
  proporre la carta-evento "Il ritorno di Fauci di Palude" all'EVENT-DECK
  di Rethmar come S2 (solo hook e puntatore: la scrittura spetta a una
  sessione EVENT-DECK).
- **Accettazione**: tabella completa con varianti per ramo; runa
  quantificata o flaggata; nessun eco che contraddica gli HOOKS ARC-09.

### C3. Atlante immagini: agganciare i 40+ webp alle mappe e scene
- **Evidenza**: `immage_campaign/` contiene ~40 webp di cui 15+ si chiamano
  "Generated Image October 03, 2025 - ...". Gli atlanti contengono i prompt
  con cui furono generate — ma nessuna tabella immagine↔mappa↔prompt. Il
  materiale visivo (raro e costoso) è di fatto inutilizzabile a colpo
  d'occhio, proprio per l'arco che andrà mostrato ai giocatori.
- **Azione**: tabella nel master visivo (A8) o nell'INDICE: file immagine →
  mappa/scena → sessione → prompt d'origine (se rintracciabile) → "quando
  mostrarla". Poi (e solo poi) la rinomina A9 delle immagini identificate.
  Immagini non riconducibili: sezione "non classificate" con descrizione,
  decisione al DM.
- **Accettazione**: ≥80% delle immagini classificate; ogni mappa master
  indica la sua immagine se esiste.

### C4. Handout giocatore (benchmark Paizo, formato HANDOUTS ARC-09)
- **Evidenza**: ARC-09 B4 ha creato il file HANDOUTS; l'arco 08 ha pezzi
  perfetti da dare in mano ai giocatori: le **schede dei 4 pregen** (che i
  giocatori useranno nel flashback D6), la **runa di pietra dei Custodi
  Eterni** (Cerimonia §2: 5 cm, al collo), le **100 asce di adamantio
  rituale**, e manca una mappa giocatore della fortezza (le attuali sono
  tutte lato DM).
- **Azione**: aggiungere una sezione ARC-08 a
  `Arco-Post-Hammerfist-HANDOUTS.md` (o file gemello nell'arco): (1) i 4
  pregen in formato stampabile 1 pagina l'uno (dopo la verifica B5);
  (2) la runa dei Custodi (descrizione + effetto C2 + prompt immagine);
  (3) il canto della cantillazione ("ricordato, ricordato, ricordato") come
  testo da leggere; (4) mappa giocatore della fortezza (versione senza
  informazioni segrete della L2 master). Ogni handout con "quando darlo".
- **Accettazione**: handout stampabili; nessuno rivela info lato DM; i
  pregen sono giocabili senza aprire i file 00_.

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Esegui **un lotto per sessione**, nell'ordine. A0 è primo e non negoziabile
(sblocca la lettura corretta del repo per tutti gli engine). Q1-Q4 hanno
default proposti; solo una risposta DM contraria li cambia. Q5 ha default
sicuro (deprecare).

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | **A0 (state.md al giocato reale)** | editing mirato + changelog | D7 (decisa) |
| 2 | A7 + A6 (code AI, placeholder 01_/03_ banner) | editing mirato | Q5 default |
| 3 | A1 + A2 (rami Fauci + contabilità perdite, tracker) | editing mirato | A0; Q1-Q2 default |
| 4 | A3 + A5 (XP/livelli + DC→CD/terminologia) | find/replace + editing | — |
| 5 | A8 (matrice contenuti + elezione master + banner) | consolidamento | — |
| 6 | A4 (scale mappe, sui soli master) | editing mirato | A8 |
| 7 | A10 + A11 (Thorin/Thorik/Thorek + comandi elfici) | audit + editing | Q3 default |
| 8 | A9 (rinomina file, git mv, fix riferimenti repo-wide) | meccanico | A8 (per rinominare solo i master) |
| 9 | B1 (matrice esiti e contingenze) | generativo | A1-A2 (numeri fissati) |
| 9b | A12 (eredità Anno −1000 su Fauci) | editing mirato | **ARC-07 B4 consegnato** |
| 10 | B2 (ponte arrivo + regia pregen→PG) | generativo | D8; **ARC-07 B2** (master P3B eletto); B6 utile prima o insieme |
| 11 | B6 (ancora March Clock) + B7 (INDICE + quickstart) | consolidamento | A8, A9, B1 |
| 12 | B5 (errata 3.5, pregen inclusi) | verifica | — |
| 13 | B3 (schede PNG) | generativo | Q3, Q4 default |
| 14 | B4 (tesoro/WBL) | audit+generativo | — |
| 15 | C1 (sistema massa fonte unica + raccordo ARC-09) | consolidamento | — |
| 16 | C2 (conseguenze lungo periodo + runa Custodi) | generativo | B1, Q1 |
| 17 | C3 (atlante immagini) + coda rinomina immagini di A9 | classificazione | A8 |
| 18 | C4 (handout: pregen stampabili, runa, mappa giocatore) | generativo | B5, C2 |

**Regole anti-spreco** (identiche ad ARC-09): (1) passa all'engine SOLO questo
file + i file del lotto corrente + state.md §0-§4; (2) niente riletture
dell'intero arco; (3) dopo ogni lotto: `grep` di verifica del criterio di
accettazione, commit, riga di changelog in state.md se il canone è cambiato;
(4) aggiorna la checklist qui sotto.

### Checklist avanzamento

- [ ] A0 · [ ] A1 · [ ] A2 · [ ] A3 · [ ] A4 · [ ] A5 · [ ] A6 · [ ] A7 ·
  [ ] A8 · [ ] A9 · [ ] A10 · [ ] A11 · [ ] A12 (attende ARC-07 B4)
- [ ] B1 · [ ] B2 (attende ARC-07 B2) · [ ] B3 · [ ] B4 · [ ] B5 ·
  [ ] B6 · [ ] B7
- [ ] C1 · [ ] C2 · [ ] C3 · [ ] C4
- [x] D6 (v2.1: riscossa quasi a fine battaglia) · [x] D7 · [x] D8 —
  decisioni DM acquisite 2026-07-02
- [ ] Q1 · [ ] Q2 · [ ] Q3 · [ ] Q4 · [ ] Q5 · [ ] **Q6 (progressione
  livello, consigliata opzione b)** — default proposti; il DM può
  confermarli o cambiarli prima delle sessioni indicate

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5**: l'idea registica del
racconto a due tempi (D6) — i giocatori vivono la ricognizione e i primi
giorni d'assedio con i pregen "Eroi di Hammerfist" e poi entrano coi loro
PG a battaglia in corso: un cold open che nessun modulo ufficiale RHoD ha;
il sistema di massa AU/DU/PFU con registro perdite stampabile (è il seme da
cui ARC-09 ha derivato il suo impianto D13); la Cerimonia delle 100 Asce,
già scritta e degna di benchmark per l'intero repo; la mole di mappe ASCII
multi-vista con coordinate.

**Cosa lo separa dall'eccellenza**: (1) il repo **crede che l'arco sia già
stato giocato** — state.md, coherence e perfino un session log raccontano un
futuro mai avvenuto: finché A0 non li corregge, ogni engine leggerà il
canone al contrario; (2) gli esiti sono scritti come fatti invece che come
rami — per una battaglia che si giocherà ai dadi servono le contingenze di
B1 (e i tracker si contraddicono pure tra loro su Fauci di Palude e sulle
perdite: A1-A2); (3) mancano i pezzi che si usano al tavolo la sera stessa:
il ponte della resurrezione di Hella (B2/D8), i pregen verificati e
stampabili (B5/C4), l'INDICE che dica quale delle quattro generazioni di
mappe usare (A8/B7); (4) terminologia ibrida EN/IT e scale mappe difformi
(A4-A5) sotto lo standard che ARC-09 ha ormai fissato. Con A0+Lotto A il
repo torna a dire la verità; con B l'arco si può portare al tavolo senza
improvvisare; con C il suo sistema di massa e i suoi cimeli lavorano per
Rethmar e oltre.
