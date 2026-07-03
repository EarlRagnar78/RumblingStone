# PIANO DI REVISIONE ARC-07 (Il Portale della Forgia Eterna) — Coerenza & Qualità

> **Versione**: v2 FINALE (2026-07-02) — audit completo dell'arco + artefatti
> (`PG/Artefatti/`) + PNG, con TUTTE le decisioni del DM già incorporate
> (D1-D17). **Il piano non ha domande aperte: l'engine può eseguire tutti i
> lotti nell'ordine di §4 senza ulteriori input dal DM.**
> **Scopo**: documento **autocontenuto** da dare in pasto a un engine AI
> specializzato (o a più sessioni brevi) per eseguire le correzioni **a
> lotti**. Ogni task ha: file coinvolti, problema con evidenza (file:riga),
> azione richiesta, criterio di accettazione.
> **Gemelli metodologici**: `09_Continuazione.../PIANO-REVISIONE-ARC09-...md`
> (eseguito) e `08_La Battaglia Di Hammerfist/PIANO-REVISIONE-ARC08-...md`
> — i punti di contatto ARC-07↔ARC-08 sono marcati **[CROSS-ARC]**.
> **Benchmark di qualità**: (interno) `PortaleForgia-P5-DEFINITIVO-PARTE2.md`
> per scrittura delle scene, `Terros.md` per metodo di ricalibrazione,
> `...IL-VIAGGIO-NELL'INCUDINE-DEL-MONDO-risultati.md` per formato dei
> canoni giocati; (esterno) *Red Hand of Doom* (Jacobs/Wyatt 2006), moduli
> planari 3.5, AP Paizo PF1e per contingenze e handout.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

0. **REGOLA ZERO — QUESTO ARCO È GIOCATO A METÀ.** P1-P3 e il viaggio dello
   spirito di Hella sono GIOCATI (fatti immutabili, tabella G qui sotto);
   il P4 è IN CORSO; P3B (resurrezione), P5 (viaggio a 1.000 anni fa) e il
   raccordo verso l'ARC-08 sono DA GIOCARE (esiti aperti ai dadi, mai
   copioni — principio D13 del piano ARC-09). Ogni fatto di tavolo non
   documentato va marcato `[INFERRED — needs DM confirmation]`, mai
   inventato.
1. **`campaign/state.md` vince** su qualunque altro file — MA state.md è
   scritto in avanti rispetto al tavolo (segna concluso perfino questo
   arco): il task **A0 del piano ARC-08** lo corregge; eseguirlo per primo
   se non è già fatto. Ogni modifica di canone va **appesa al changelog**
   di state.md, mai riscritta nella storia.
2. **Sistema D&D 3.5 SRD only** — niente 5e (no azioni bonus, no
   vantaggio/svantaggio meccanici), niente lore FR post-1385 DR.
   Ambientazione Faerûn 1372 DR, più il viaggio temporale a **1.000 anni
   prima (≈372 DR)** (D7).
3. **Mai inventare** stat, poteri di artefatti o fatti di sessione: flag
   `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare `campaign/state.md` §4 (chi sa
   cosa) e §6 (artefatti), `campaign-artifacts.md`, e i file canonici in
   `PG/Artefatti/` (D9). I PDF dell'arco (`SinergieArteFattiQuickReference.pdf`,
   `BenedizioniDiMoradin.pdf`) sono materiale valido.
6. Le mappe tattiche usano scala **1,5 m/quadretto** (già rispettata da
   `Mappe/TACTICAL-GRIDS-COMPLETE.md` r.8-9 — mantenerla).
7. Lingua: **italiano**, nomi meccanici 3.5 in italiano (CD non DC,
   Osservare non Spot, Nascondersi non Hide).
8. **Non cancellare file**: il default è il banner
   `> ⚠️ DEPRECATED (2026-07): ...` in testa (D10). Unica eccezione
   ammessa: `temp_sinergie.txt` (temporaneo del PDF), rimozione fisica
   consentita.

### Stato GIOCATO / DA GIOCARE (canone DM 2026-07-02 — immutabile)

| # | Elemento | Stato |
|---|---|---|
| G0 | **Hella Oakenshield è MORTA nell'ARC-06** (Stanza della Corona): uccisa nello scontro con le **Yochlol half-illithid mandate da Sonjak** per prendere la Corona (Urialle CR 14, EL 17 — `06_.../villans.md`); il vecchio portatore **Belkram**, dominato e maledetto dai drow (morte negata), si è **ravveduto nel momento della sua morte definitiva**. **Belkram e Urialle sono entrambi MORTI** (D13). Già canone scritto: coherence.md r.47, campaign-history.md r.26. **L'intero ARC-07 esiste per rendere epica la resurrezione di Hella** | ✅ giocato (ARC-06) |
| G1 | P1-P2: ingresso e Sala della Forgia Eterna (affreschi, prove); il corpo di Hella è custodito nella Sala da **Therysol** (history r.176) | ✅ giocato — fatti da raccogliere (B1) |
| G2 | P3: Piano del Fuoco — **Topazio del Tempo recuperato** (unica gemma attiva oggi) | ✅ giocato |
| G2b | **Viaggio dello spirito di Hella nell'Incudine del Mondo — GIOCATO e REGISTRATO** in `PortaleForgia-P4-PianoTerra-P3B-HELLA-IL-VIAGGIO-NELL'INCUDINE-DEL-MONDO-risultati.md`: compagno = **DURIK (maschio)**; Verità Piena / Ferita Aperta / Via della Radice; **tutti i TS e la prova Conoscenze (religioni) superati** → doni in versione piena; aspetto di Durik = "Protegge Hella" (mithral e pietra scura, occhi di topazio); riga tavola v2 §7: Resist freddo 15, Regen 1 (terra), Percepire Intenzioni +2, vuln. fuoco, Durik Riforgiato 12 DV | ✅ giocato e registrato |
| G3 | P4: Piano della Terra — **IN CORSO** (Smeraldo in palio; boss Terros/Mithral Golem). **Composizione reale (D15)**: **3 PG di 13°** — Artemis (Ring of Chaotic Illumination; tentazioni Lathander/Mask SOLO sue), Tordek (Bracieri Gemelli + Cintura della Devastazione D17), Thorik (Aegis Fang + Corona col solo Topazio). **Therysol NON presente** (veglia il corpo); **nessun inviato del Collezionista incontrato** | 🟡 in corso |
| G4 | P3B: rituale di resurrezione di Hella — si gioca **dopo la Terra** (D2), nonostante la sigla "3B" | ⬜ da giocare |
| G5 | P5: viaggio temporale all'assedio di Hammerfist di **1.000 anni prima** (D7), duello con **Skullcrusher** (D6) — da giocare **VELOCE** (D1) | ⬜ da giocare |
| G6 | Raccordo: vittoria antica → il **Rubino** si accende e riporta i PG al 1372 → riemersione al **Cuore della Montagna** (ARC-08) — vedi D16 | ⬜ da giocare (la sezione "1372" di P6 è superata: A3) |

### Decisioni di canone GIÀ PRESE (D1-D17 — applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | **P5 si gioca in maniera VELOCE**: una sessione cinematografica, non un dungeon completo (formato B3) | DM 2026-07-02 |
| D2 | **Ordine di gioco**: P4 Terra (in corso) → P3B resurrezione → P5 viaggio → raccordo → ARC-08. Coerente con ARC-08 D8 | DM 2026-07-02 |
| D3 | Il nemico del viaggio è **l'antenato di Fauci di Palude**; l'esito del duello alimenta il ponte "la Forgia ricorda le ferite" (B4) **[CROSS-ARC]** | DM 2026-07-02; P5-DEFINITIVO-PARTE2 r.285 |
| D4 | La struttura a due tempi dell'ARC-08 (pregen + finale dei Rumbling Stones) resta ad ARC-08; la sezione "Anno 1372" di P6 è la sua bozza storica (A3) | DM 2026-07-02; piano ARC-08 D6/D9 |
| D5 | Il portale temporale si apre con **Topazio + Smeraldo**; il **Rubino** si accende ALLA FINE del viaggio ("Cuore della Leggenda") | P5-RICALIBRATO r.19-21; P5-DEFINITIVO-PARTE2 §4.2 |
| D6 | L'antenato si chiama **SKULLCRUSHER**. "Skulldark" e "Infernotooth Giovane" vanno sostituiti (o dichiarati epiteti una-tantum nel master P5) | DM 2026-07-02 |
| D7 | La battaglia antica è **1.000 ANNI PRIMA** (≈372 DR), NON "Anno −1000 DR": correggere "2.372 anni dopo" (P5-DEF-P2 r.283), "500 anni fa" (P6 r.350), "millenni fa" (P2 r.1119) e l'etichetta ovunque | DM 2026-07-02 |
| D8 | **Il party reale è di livello 13.** Artefatti al tavolo: Bracieri di Tordek RISVEGLIATI (Fuoco+Terra), Corona IN RISVEGLIO (solo Topazio), Aegis Fang pre-risveglio pieno, Anello riforgiato. Bilanciare le parti future su questo | DM 2026-07-02 |
| D9 | **`PG/Artefatti/` è la fonte canonica degli artefatti**; le copie altrove (cartella Corona in ARC-06) sono snapshot storici da marcare | DM 2026-07-02 |
| D10 | File ridondanti/meta: **DEPRECARE con banner**, mai eliminare (eccezione: `temp_sinergie.txt`) | DM 2026-07-02 |
| D11 | Il cognome di Hella è **Oakenshield** | DM 2026-07-02 |
| D12 | Gli esiti del viaggio dello spirito sono canonizzati nel file `...-risultati.md` (G2b) — completo, zero flag residui | DM 2026-07-02 → file creato |
| D13 | **Belkram e Urialle sono ENTRAMBI MORTI** (stato finale post-ARC-06) | DM 2026-07-02 |
| D14 | Il compagno di Hella è **DURIK (maschio)** — rinominare "Nymeria" ovunque (A11) | DM 2026-07-02 |
| D15 | **Composizione P4 = 3 PG senza Therysol** (veglia il corpo, deciso dai PG); tentazioni divine solo su Artemis; nessun inviato del Collezionista. ⚠️ `Terros.md` assume "3 PC + 1 NPC Therysol Support": **sbagliato**, ricalibrare (A5/B5) | DM 2026-07-02 |
| D16 | **Sequenza gemme (verificata sui file)**: Topazio ✅ (dal Fuoco) → Smeraldo nel P4 → **Rubino alla VITTORIA della battaglia antica** = *Gem of Immutable Time*, motore del ritorno al 1372 (P5-DEF-P2 §4.3 r.361-363); i Rumbling Stones **riemergono al Cuore della Montagna, Giorno 3 dell'assedio** (P6 r.621-660, Incontro 3B). **CUCITURA MANCANTE**: il salto *Sala della Forgia → Cuore della Montagna* non è scritto in nessun file → si scrive nel ponte **ARC-08 B2** con questo D16 come fonte | DM 2026-07-02 + verifica file |
| D17 | **La Cintura della Devastazione ESISTE ed è canone**: oggetto **custom creato dal PG**, identico nel funzionamento ai *Devastation Gauntlets* ma spostato allo **slot cintura** perché Tordek potesse indossare i Bracieri Gemelli ai polsi. La menzione "Devastation Gauntlets" di P2 r.482 va corretta in "Cintura della Devastazione"; l'oggetto va documentato in `PG/Artefatti/Artefatti-Pg/Tordek/` e aggiunto a state.md §6 (changelog) | DM 2026-07-02 |

### Decisioni da chiedere al DM

**✅ NESSUNA. Tutte risolte (D1-D17, 2026-07-02).** L'engine esegue i lotti
nell'ordine di §4 senza input ulteriori; ogni dettaglio mancante che emerga
in corso d'opera si flagga `[INFERRED — needs DM confirmation]` e non blocca.

---

## §1 — LOTTO A: Incoerenze di canone e igiene dei file (priorità P0)

### A1. L'antenato con tre nomi — applicare D6 (Skullcrusher)
- **Problema**: il boss del P5 (che il tavolo giocherà a breve, D1) cambia
  nome a seconda del file: **Skulldark** (P5-DEFINITIVO ×20,
  P5-RICALIBRATO), **Skullcrusher** (FINAL-P5, P6 ×10, TACTICAL-GRIDS,
  CORREZIONE-Boss-Fauci), **Infernotooth Giovane** (P1 r.747, P2 r.1119) —
  e `P5-DEFINITIVO-PARTE1.md` r.229 usa due nomi nella stessa riga.
- **Azione**: **Skullcrusher** in tutti i file dell'arco (P1, P2, FINAL-P5,
  DEFINITIVO ×2, RICALIBRATO, P6, CORREZIONE, TACTICAL-GRIDS); un eventuale
  epiteto ("il Nero") si dichiara alla prima occorrenza del master P5.
  Riga di changelog in state.md (il nome entra nel canone: l'ARC-08 lo
  eredita nel ponte B4).
- **Accettazione**: `grep -rn "Skulldark\|Infernotooth"` = 0 fuori da
  banner e note storiche; un solo nome (+epiteto dichiarato) ovunque.
- **✅ FATTO (2026-07-02, sessione 2)**: `grep` = 0 in tutto l'arco (fuori
  dal testo di questo piano). Sostituiti "Skulldark" (P5-DEFINITIVO ×2,
  RICALIBRATO) e "Infernotooth Giovane" (P1, P2) con **Skullcrusher il
  Nero**. Risolto il doppio-drago di P5-DEFINITIVO-PARTE1 r.234-236 (Skulldark
  "padre" vs Skullcrusher "discendente" → un solo drago, Skullcrusher, che è
  il capostipite della stirpe di Fauci). Epiteto "il Nero" usato in forma
  piena come nome. Changelog in state.md.

### A2. Profondità temporale — applicare D7 (1.000 anni prima, ≈372 DR)
- **Problema**: i file dicono quattro cose diverse: "Anno −1000" come data
  assoluta DR con "2.372 anni dopo" (P5-DEFINITIVO-PARTE2 r.283), "500
  anni fa" (P6 r.350, canto di Aegis Fang), "millenni fa" (P2 r.1119) —
  contro il canone D7 (**1.000 anni prima**).
- **Azione**: normalizzare l'etichetta "Anno −1000" (titoli e testo di
  P5/P6/P2 e **state.md §6**, che dice "year -1000 battle") in "1.000 anni
  prima (≈372 DR)" — o mantenere "Anno −1000" SOLO se ridefinito una volta
  nel master P5 come conteggio relativo nanico; correggere r.283 ("2.372
  anni dopo" → "1.000 anni dopo"), P6 r.350, P2 r.1119; uniformare la
  genealogia del drago (quante generazioni tra Skullcrusher e Fauci in
  1.000 anni — detto una sola volta) e la collocazione di **Thorgrim
  Barbadiferro** (P1 r.704-751, P2 r.858, P5, P6 r.977).
- **Accettazione**: una sola profondità temporale (1.000 anni) e una sola
  genealogia in tutto il repo; changelog in state.md.
- **✅ FATTO (2026-07-02, sessione 2)**: corretti tutti i valori in
  conflitto — "2.372 anni" (FINAL-P5 r.15/r.37, DEFINITIVO-PARTE1 r.22,
  DEFINITIVO-PARTE2 r.288), "500 anni fa" + "bis-bisnonno" (FINAL-P5 r.380,
  P6 r.350) → **1.000 anni** / capostipite. Etichetta "Anno -1000" mantenuta
  ma **ridefinita una volta** nei file P5 (conteggio nanico relativo = 1.000
  anni prima del 1372, ≈372 DR). Le occorrenze figurate di "millenni" (forgia
  che arde, corona che attende) restano: non riguardano la profondità del
  viaggio. Normalizzati anche state.md §6 e campaign-artifacts.md
  ("-1000 DR"/"year -1000" → "1,000 years before, ≈372 DR"). Genealogia
  unica: Skullcrusher capostipite → Fauci discendente diretto. Changelog in
  state.md.

### A3. P6 contiene una "battaglia finale 1372" superata dagli Archi 08-09 — [CROSS-ARC]
- **Problema** (il più importante dell'arco):
  `Portaleforgia-P6-INTEGRAZIONE-Completa.md` fu scritto quando la campagna
  doveva FINIRE qui: la sezione "ANNO 1372: BATTAGLIA FINALE HAMMERFIST"
  (r.598-946) mette in scena la battaglia con **Fauci di Palude a GS 12**
  (r.813 "CR 12 vs Party 14"), lo dà **"Morto"** a esito fisso (r.869) e
  chiude con "🏁 FINE CAMPAGNA" (r.947) e un "PARTE 7 PREVIEW" (r.853).
  Tutto superato: la battaglia è ora **l'ARC-08 intero** (Fauci GS 15,
  esiti a rami). `CORREZIONE-Boss-Fauci.md` r.16 mantiene il doppio
  profilo "GS 15 (Anno 1372), GS 12 versione Parte 6".
- **Azione**: (1) banner DEPRECATED sulla sola sezione 1372 di P6 (la
  sezione battaglia antica r.9-597 resta materiale vivo del P5) con
  puntatore all'ARC-08; (2) **estrarre ciò che sopravvive**: la regia
  dell'arrivo dei Rumbling Stones al Cuore della Montagna (r.621-753) è la
  fonte di ARC-08 E6/B2 (citarla, non doppiarla); l'hook dell'**uovo di
  Fauci** (r.958) → C3; il canto di Aegis Fang "sangue Skullcrusher"
  (r.746) → ponte B4; (3) correggere CORREZIONE-Boss-Fauci: profilo GS 12
  marcato "versione storica P6, superata — nel 1372 vale il GS 15 dei file
  ARC-08"; (4) verificare che nessun file punti a "Parte 7".
- **Accettazione**: chi apre P6 capisce subito cosa è vivo (battaglia
  antica) e cosa è storia di progetto (1372); un solo profilo di Fauci per
  il 1372 nel repo; zero riferimenti attivi a "Parte 7"/"fine campagna".
- **✅ FATTO (2026-07-02, sessione 7)**: banner DEPRECATED sulla sezione
  "ANNO 1372" di P6 (r.605+), con puntatore all'ARC-08 (Fauci GS 15, esiti
  aperti) e all'elenco di ciò che sopravvive. **Estrazioni marcate**: Incontro
  3B (arrivo al Cuore della Montagna) = fonte viva per ARC-08 B2/E6; uovo di
  Fauci = hook vivo → C3; canto Aegis Fang → B4. Profilo Fauci "CR 12 vs Party
  14" marcato SUPERATO inline (vale GS 15 ARC-08 + carry-over B4). Neutralizzati
  i due puntatori attivi a "Parte 7" in CORREZIONE-Boss-Fauci (→ epilogo
  ARC-08/09). Gli altri "Parte 7" restano solo dentro la sezione deprecata.

### A4. Gemme della Corona: attivazioni e cucitura del ritorno — applicare D5+D16
- **Problema**: `PortaleForgia-P2-REVISED-Corretta-PARTE1.md` r.1007
  promette "Quando Rubino attiva → portale aperto" e r.1072 attribuisce il
  viaggio al Rubino; il design recente (D5/D16) fa aprire il portale a
  **Topazio+Smeraldo** e accende il **Rubino solo alla vittoria antica**,
  come motore del ritorno al 1372. Inoltre P5 riporta i PG alla *Sala
  della Forgia* mentre P6 li fa arrivare al *Cuore della Montagna* — il
  passaggio tra i due non è scritto (D16).
- **Azione**: correggere la tabella affreschi/attivazioni di P2
  (r.982-1007, r.1072) al modello D5/D16; la **cucitura** Sala della
  Forgia → Cuore della Montagna si scrive nel ponte **ARC-08 B2** (qui
  solo il rimando); verificare la coerenza con
  `PG/Artefatti/LaCorona_di_Adamantio-DM.md` (citato da P5-DEF-P2 r.361) e
  con state.md §6 / `campaign-artifacts.md` (ARC-09 C4 tratta il Rubino
  come single-use SPESO dopo questo arco: la catena deve tornare).
  Changelog se il canone artefatti cambia.
- **Accettazione**: una sola sequenza di attivazione delle 3 gemme nel
  repo; la Corona arriva ad ARC-08/09 nello stato che ARC-09 assume; il
  ponte ARC-08 B2 cita D16.
- **✅ FATTO (2026-07-02, sessione 8)**: corretta l'unica riga che
  attribuiva l'apertura del portale al Rubino (P2-PARTE1, tabella nitidezza)
  → modello **D5/D16**: portale aperto da **Topazio+Smeraldo** dopo il Piano
  Terra, **Rubino si accende SOLO alla vittoria antica** come motore del
  ritorno. Aggiunto blocco-canone con rimando a `LaCorona_di_Adamantio-DM.md`,
  state.md §6, `campaign-artifacts.md` (Rubino single-use, già coerenti) e al
  ponte ARC-08 B2 (cucitura Sala→Cuore, D16). Il P5-FASTPLAY Scena 6 già
  esprime la stessa sequenza. Una sola sequenza in tutto il repo.

### A5. Livello e composizione del party — applicare D8+D15
- **Problema**: le dichiarazioni cambiano da file a file (P3B "livello
  13", La_Piramide "Livello 13", P5-RICALIBRATO "Livello 14+ (God Mode)",
  P6 "Party 14", Terros "Party Level 14"), mentre state.md §0 assegnava
  all'arco il livello 12. Il canone è **13°** (D8). In più `Terros.md`
  assume "3 PCs **+ 1 NPC (Therysol Lv 8 Support)**" — sbagliato (D15:
  Therysol veglia il corpo di Hella).
- **Azione**: uniformare le intestazioni di TUTTI i file a "13°";
  ricontrollare i budget GS delle parti future col metodo di Terros
  corretto da D15 (**3 PG, APL effettivo 12, NESSUN supporto** finché
  Hella non torna; APL 13 pieno dal P5); annotare lo stato artefatti D8
  nelle intestazioni dei master (è ciò che giustifica gli EL alti — il
  precedente: EL 17 dell'ARC-06 su party di 13°, villans.md r.1). Le parti
  giocate NON si ribilanciano: si annota il livello a cui furono giocate.
  Propagare il 13° a state.md §0 (via ARC-08 A0) — la cascata su ARC-08 è
  già decisa (suo D9: Hammerfist consolida il 13°).
- **Accettazione**: una sola dichiarazione di livello per parte; Terros
  ricalibrato per 3 PG senza supporto; budget delle parti future annotati.
- **✅ FATTO (2026-07-02, sessione 8)**: `state.md §0` riga ARC-07 → **13°**
  (e stato "in corso", il "completato" era scritto in avanti → A0).
  `La_Piramide` r.417 "Livello 14" → 13° + nota D15 su Therysol (che veglia
  il corpo). `P3-PianoFuoco-PARTE2` r.1097 (party al 14° "durante Parte 6") →
  resta 13° per l'arco, il 14° matura nell'ARC-08. **Terros** ricalibrato
  nella base: da "Livello 14, 3 PC + Therysol Support" a **13°, 3 PG senza
  supporto, APL effettivo 12** (numeri finali del boss → B5). Aggiunta la
  nota stato-artefatti **D8** all'intestazione del master P4 (giustifica gli
  EL alti). Le due ricalibrazioni "Livello 14" (P4-RICALIBRATO, P5-RICALIBRATO)
  hanno già il banner A6 che le riporta al 13° canonico. Dadi-soglia "14+"
  lasciati (non sono livelli). Le parti giocate non ribilanciate.

### A6. Generazioni multiple mai riconciliate (P3B ×2, P4 ×4, P5 ×4 + 3 doc di ricalibrazione)
- **Problema**: il tavolo ci sta giocando DENTRO e i file si sovrappongono:
  P5 in 4 versioni (`FINAL-P5`, `DEFINITIVO-PARTE1/2`, `RICALIBRATO`) con
  nomi del boss diversi (A1); P4 in 4 (`COMPLETO-alternative`,
  `RICALIBRATO`, `HELLA-IL-VIAGGIO...` v1 e v2); P3B in 2 (`COMPLETO`,
  `RICALIBRATO-alternative`); tre documenti di ricalibrazione
  (`La_Piramide_Ricalibrata` = finale P3, `RicalibrazioneScontriPianoDelFuoco`,
  `Terros`) correggono i file-base senza che i file-base lo dichiarino.
- **Azione**: (1) matrice contenuto × versione; (2) eleggere UN master per
  parte — per le parti GIOCATE il master è la versione usata al tavolo
  `[INFERRED — needs DM confirmation]`; per P3B e P5 (future) l'ultima
  generazione integrata con le ricalibrazioni; (3) banner sugli altri
  (D10); (4) nei master, banner inverso "ricalibrato da: ..." così la
  catena è esplicita.
- **Accettazione**: un master per parte; ogni doc di ricalibrazione citato
  dal master che corregge; zero versioni orfane senza stato.
- **✅ FATTO (2026-07-02, sessione 3)**: creata `ARC07-MATRICE-VERSIONI.md`
  (matrice parte × file × stato). Master eletti: P1, P2 (unici); P3 base
  (ricalibrato da RicalibrazioneScontri + La_Piramide); P4 COMPLETO-alt
  `[INFERRED]` (ricalibrato da Terros + RICALIBRATO); viaggio v2 (fonte del
  file risultati). Banner applicati: DEPRECATO su FINAL-P5 e viaggio-v1;
  *ricalibrazione* su La_Piramide, Terros, CORREZIONE-Boss-Fauci,
  P4-RICALIBRATO; *annesso* su Interludio; reverse-banner "ricalibrato da"
  sui master P3 e P4; MASTER-lungo su P5-DEFINITIVO, sintesi su P5-RICALIBRATO,
  MASTER-parziale su P6. **P3B e P5**: master formale eletto nei task
  dedicati **B2** e **B3** (qui registrati i candidati). Nessuna versione
  orfana.

### A7. Igiene: file vuoto, file temporaneo, coda AI, nomi file rotti
- **Problema**: `Mappe/Atlante-Visivo-Mappe.md` è **0 byte**;
  `temp_sinergie.txt` è un temporaneo del PDF;
  `RicalibrazioneScontriPianoDelFuoco.md` apre con coda conversazionale AI
  ("Perfetto! Ora ho tutti i dettagli necessari...");
  `PG/Artefatti/LaCorona_di_Adamantio-DM.md` apre con residuo di
  conversione ("OnlineMarkdown.com https://onlinemarkdown.com/"); il
  filename `PortaleForgia-P4-PianoTerra-P3B-HELLA-IL-VIAGGIO-NELL'INCUDINE-DEL- MONDO.md`
  contiene **uno spazio dopo "DEL-"**; `Portaleforgia-P6-...` ha la F
  minuscola contro la convenzione `PortaleForgia-*`.
- **Azione**: deprecare o riempire il file vuoto (l'indice-mappe vero
  nasce in B8/C1); rimuovere `temp_sinergie.txt` (D10, eccezione
  ammessa); ripulire le code AI/conversione sostituendole con header di
  stato; `git mv` dei filename rotti (spazio, casing) aggiornando i
  riferimenti repo-wide.
- **Accettazione**: zero file 0-byte, zero `temp_*`, zero code AI;
  `grep -rn "OnlineMarkdown"` = 0; nessun filename con spazi interni
  anomali; link tutti validi.
- **✅ FATTO (2026-07-02, sessione 1)**: `Atlante-Visivo-Mappe.md` è ora uno
  stub con puntatore a B8/C1; `temp_sinergie.txt` rimosso;
  `RicalibrazioneScontriPianoDelFuoco.md` e
  `LaCorona_di_Adamantio-DM.md` ripuliti (coda AI e 17 blocchi di
  watermark `OnlineMarkdown.com` da conversione PDF); `git mv` di
  `PortaleForgia-P4-...-DEL- MONDO.md`/`-v2.md` (spazio rimosso) e
  `Portaleforgia-P6-INTEGRAZIONE-Completa.md` → `PortaleForgia-P6-...`
  (F maiuscola), riferimenti aggiornati in questo file, nel file
  `...-risultati.md`, nel file v2 e nel piano ARC-08. Trovato in più un
  file duplicato non censito qui (stesso contenuto, casing diverso):
  `PortaleForgia-P4-pianoTerra-P3b-...-risultati.md` (minuscolo) — appunti
  grezzi del DM, ora marcato deprecato con puntatore al canonico (D10: non
  cancellato).

### A8. Terminologia: 53 `DC` inglesi + file interamente in inglese
- **Problema**: 53 occorrenze di `DC n` contro la convenzione CD (§0.7);
  `Terros.md` e `Mappe/TACTICAL-GRIDS-COMPLETE.md` sono in inglese
  (accettabile come specifica tecnica, ma i termini che il DM legge al
  tavolo devono essere 3.5-italiano).
- **Azione**: DC→CD globale; skill in italiano 3.5; per Terros e
  TACTICAL-GRIDS tradurre almeno intestazioni di scena, nomi di prova e
  condizioni (il corpo tecnico può restare inglese con nota).
- **Accettazione**: `grep -rn "DC [0-9]"` = 0 nell'arco; le prove al
  tavolo sono leggibili in italiano.
- **✅ FATTO (2026-07-02, sessione 10)**: **DC → CD** (word-boundary) su tutte
  le 59 occorrenze (P4-COMPLETO, viaggio v1/v2, Terros, mappe L1/L2,
  TACTICAL-GRIDS). `grep "DC [0-9]"` = 0. Verificato che ogni "DC" era Classe
  Difficoltà (anche "DC: Hide 18", "Climb DC +5"). I file di prova rivolti al
  tavolo (viaggio, P3B, P4, P5) sono già in italiano con nomi di skill 3.5
  italiani. Per i file tecnici in inglese (Terros, TACTICAL-GRIDS) aggiunto un
  **glossario italiano** delle prove in testa (Hide=Nascondersi, Spot=
  Osservare, …), lasciando il corpo tecnico in inglese come consentito.

### A9. Numerazione fuori ordine: P3B si gioca dopo P4 — applicare D2
- **Problema**: la sigla "P3B" precede "P4", ma l'ordine di gioco (D2) è
  Terra → resurrezione → viaggio. I file fusi P4+P3B testimoniano
  l'intreccio (lo spirito viaggia MENTRE il party attraversa la Terra —
  e infatti il viaggio è già stato giocato, G2b) ma nessun file dichiara
  l'ordine al lettore.
- **Azione**: dichiarare l'ordine D2 in testa ai master di P3B, P4 e P5
  (una riga "si gioca dopo/prima di..."); nell'INDICE (B8) la tabella
  delle parti segue l'ordine di GIOCO con nota sulla numerazione storica.
  NON rinumerare i file (troppi riferimenti).
- **Accettazione**: nessun lettore può sbagliare l'ordine; INDICE coerente
  con D2 e con ARC-08 D8.
- **✅ FATTO (2026-07-02, sessione 1)**: riga D2 aggiunta in testa a
  entrambe le versioni P3B (COMPLETO, RICALIBRATO-alternative), a tutte e
  4 le versioni P4 (COMPLETO-alternative, RICALIBRATO, e i due file fusi
  v1/v2 del viaggio) e a tutte e 4 le versioni P5 (FINAL, DEFINITIVO
  PARTE1/2, RICALIBRATO) — l'elezione del master (A6) non è ancora
  avvenuta, quindi la riga è su ogni generazione per non doverla rifare.
  L'INDICE (B8) resta da fare.

### A10. Artefatti: fonte unica, duplicazioni, Cintura della Devastazione — applicare D9+D17
- **Problema**: (1) la cartella `00-La Corona di Adamantio-ogetto&Prove/`
  esiste **in due copie divergenti** (dentro l'ARC-06 e in
  `PG/Artefatti/Artefatti-Pg/`) con set di file diversi e file omonimi dal
  contenuto diverso (la copia PG ha in più le schede Fase 2 e gli HTML
  `01/02/03_Corona_N_Gemme`); (2) il Ring of Chaotic Illumination ha 3
  generazioni (`Ring of Chaotic Illumination.md`,
  `Ring_of_chaotic_illumination-master.md`, cartella con Revised + `Old/`);
  (3) refusi nei nomi file (`achede _avveimenti_corona_diAdamantio.md` —
  spazio interno e refuso doppio); (4) **D17**: P2 r.482 cita i
  "Devastation Gauntlets" ma l'oggetto canonico è la **Cintura della
  Devastazione** (custom del PG, slot cintura, funzionamento identico ai
  Gauntlets, creata per liberare i polsi per i Bracieri) — P5-DEF-P2 r.371+
  la chiama già "Cintura", ma NON esiste né scheda né riga in state.md §6.
- **Azione**: applicare D9 (PG/Artefatti canonico): riconciliare le due
  cartelle Corona (portare in PG ciò che l'ARC-06 ha in più, poi banner
  "snapshot storico" sulla copia ARC-06); eleggere il master del Ring
  (proposta: `..._Revised.md`); `git mv` dei filename con refusi;
  verificare che lo stato dichiarato nei master corrisponda a D8/D16
  (**solo Topazio acceso oggi**). Applicare D17: correggere P2 r.482
  (Gauntlets → Cintura), creare
  `PG/Artefatti/Artefatti-Pg/Tordek/00_Cintura_della_Devastazione.md`
  (oggetto custom: slot cintura, poteri = Devastation Gauntlets, nota
  d'origine "spostati per indossare i Bracieri"), aggiungere la riga a
  state.md §6 con changelog.
- **Accettazione**: un solo file canonico per artefatto; copie marcate;
  la Cintura ha scheda + riga in §6; `grep -rn "Devastation Gauntlets"`
  = 0 fuori dalle note storiche; stato gemme coerente col tavolo ovunque.
- **✅ FATTO (2026-07-02, sessione 9)**: **D17 Cintura** — creata la scheda
  `PG/Artefatti/Artefatti-Pg/Tordek/00_Cintura_della_Devastazione.md` (slot
  cintura, poteri = Devastation Gauntlets, nota d'origine) + riga in state.md
  §6 (changelog); tutte le ~20 menzioni attive "Devastation Gauntlets"
  nell'arco (P1, P2×2, P3-Fuoco) → **Cintura della Devastazione** (restano
  solo le note d'etimologia "formerly/riforgiati/MIC pag 93"); reimpostata
  l'immagine "mani guantate" del rito P2 come Cintura alla vita (i Bracieri
  restano alle mani). **D9 Corona** — copiate in PG le 2 immagini che aveva
  solo l'ARC-06; banner `_SNAPSHOT-STORICO.md` nella copia ARC-06 (near-dup
  `.md` flaggati [INFERRED] per il DM, non fusi). **Ring** — master eletto
  `..._Revised.md` (banner), `Old/` deprecata con `_DEPRECATED-SNAPSHOT.md`.
  **Refusi** — `git mv` di `achede _avveimenti_...md` → `..._-ALT.md` in
  entrambe le cartelle. Stato gemme (solo Topazio oggi) coerente con A4/D16.

### A11. Rinomina del compagno di Hella: Nymeria → Durik (maschio) — applicare D14
- **Problema**: al tavolo il cane di Hella è **Durik, maschio** (D14); i
  file di design (fusi v1/v2 del viaggio, ~50 occorrenze incluse
  "L'Impronta di Nymeria", "Nymeria Riforgiato" e la scheda 3.5 di v2 §10)
  usano "Nymeria" al femminile.
- **Azione**: propagare nome e genere (articoli, pronomi, aggettivi) in
  v1/v2 del viaggio, nel master P3B (B2) e in ogni file che citi il
  compagno; la fonte della rinomina è `...-risultati.md` §0. NON
  rinominare i file di design (solo il testo).
- **Accettazione**: `grep -rn "Nymeria"` = 0 fuori dai banner/note
  storiche; genere coerente ovunque.
- **✅ FATTO (2026-07-02, sessione 4)**: `Nymeria` → `Durik` propagato in
  v1 e v2 del viaggio (55/57 occorrenze), in `campaign-party.md` (skills +
  mirror copilot), in `index.json` copilot. Genere: il testo era già in gran
  parte maschile ("il cane", "compagno", "Riforgiato", "morto"); i possessivi
  italiani ("la sua testa", "la polvere dispersa") concordano col nome
  posseduto, non col cane → nessuna correzione spuria. Residui "Nymeria" solo
  nelle note di rinomina (risultati §0, Collana r.69). `grep` pulito.

---

## §2 — LOTTO B: Completamento contenuti per il gioco (priorità P1)

> Metà arco è dietro il tavolo, metà davanti: memoria per ciò che è stato
> giocato, preparazione per P3B/P5/raccordo. **B2→B3→B4 è il materiale
> della prossima sessione: priorità assoluta.**

### B1. Session log delle sessioni REALMENTE giocate (ARC-06 finale → P4 in corso)
- **Evidenza**: `campaign/sessions/` non ha alcun log del giocato reale
  (solo il log anticipato/fittizio del 2026-05-03, vedi ARC-08 A0). La
  morte di Hella è fissata come evento (coherence r.47) ma la sessione che
  l'ha prodotta non ha log — e nemmeno P1-P3, il viaggio dello spirito, il
  P4 in corso.
- **Azione**: intervista breve al DM → log retroattivi nel formato
  AGENTS.md (Summary / Key decisions / XP / Loot / Next hooks) per: (1) il
  finale dell'ARC-06 (Urialle e le Yochlol, la morte di Hella, la
  redenzione di Belkram — G0, con gli stati D13); (2) ingresso+Sala Forgia;
  (3) Piano del Fuoco (Topazio); (4) il viaggio dello spirito (G2b —
  agganciare il file-risultati); (5) Piano della Terra fin dove è arrivato
  (composizione D15). OGNI lacuna → `[INFERRED]`. Aggiornare il cruscotto
  post-A0 di state.md man mano.
- **Accettazione**: ogni sessione giocata ha un log; la morte di Hella ha
  data, luogo e causa IN un log; zero invenzioni non flaggate.
- **✅ FATTO parziale (2026-07-02, sessione 11)**: creato
  `campaign/sessions/RETROATTIVI-ARC07-INFERRED.md` con 5 log retroattivi in
  formato AGENTS.md — R0 finale ARC-06 (morte di Hella: Yochlol di Sonjak +
  Urialle, Belkram redento; luogo = Stanza della Corona; causa registrata),
  R1 Sala Forgia, R2 Fuoco/Topazio, R3 viaggio dello spirito (agganciato al
  file-risultati, **canone non-INFERRED**), R4 Terra in corso (D15). Ogni
  lacuna marcata `[INFERRED]`. ⚠️ **Resta l'intervista al DM** per date,
  giocatori, XP/loot reali (l'engine non può inventarli): il file è una
  ricostruzione dichiarata, da validare. Nodo aperto flaggato: compagno
  animale (rinoceronte/orso/Durik).

### B2. Master della resurrezione di Hella (P3B) — [CROSS-ARC]
- **Evidenza**: quattro trattamenti della stessa scena-cardine
  (`P3B-...COMPLETO` 22 KB, `P3B-...RICALIBRATO-alternative` 4,7 KB, i due
  fusi P4+P3B da 34 e 44 KB), nessuno eletto. Il ponte ARC-08 B2 assume che
  la scena viva qui.
- **Azione**: eleggere il master (proposta: il fuso v2 per lo spirito +
  la parte rituale del COMPLETO `[INFERRED — needs DM]`); applicare A5
  (livello), A11 (Durik), D2 (posizione) e **integrare i risultati
  canonici del viaggio** (file `...-risultati.md`: doni pieni, aspetto di
  Durik "Protegge Hella"); verificare la meccanica 3.5 del rituale
  (componenti, costi, il −2 CON permanente di Thorik come scelta ONSCREEN,
  il template Ibrido Treant — coerente con state.md §1) e il **Cuore di
  Moradin SPESO** dopo il rito (state.md §6). Chiudere con Hella viva e il
  party pronto al P5.
- **Accettazione**: un solo master P3B; risultati del viaggio integrati;
  stato artefatti in uscita = quello che ARC-08/09 assumono; ARC-08 B2
  punta qui.
- **✅ FATTO (2026-07-02, sessione 4)**: eletto master =
  `PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md` (banner ⭐ MASTER;
  l'alternativa RICALIBRATO deprecata). Aggiunta la sezione **INTEGRAZIONE
  B2** che riporta i **doni pieni** del viaggio giocato (Resist Freddo 15,
  Marchio della Veritade, Radice Silenziosa, Radici del Mondo, Durik
  "Protegge Hella") sovrascrivendo i doni generici del testo storico.
  Correzioni inline: Thorik **−2 CON** permanente (era "−2 pf"), **Cuore di
  Moradin SPESO** (era "ritornato nell'Altare"), **Cintura della
  Devastazione** (era "Devastation Gauntlets"), timing **D2** (era "tra P5 e
  P6"), classe Hella Ranger 1/Druida 12, Resist Freddo 15 nei due punti del
  testo. `ARC-08 B2` ora punta al file per nome. ⚠️ Flag [INFERRED]:
  discrepanza compagno animale (rhinoceros/orso/Durik) da chiudere in A0/B1.
- **Evidenza**: il P5 esiste come atto completo (DEFINITIVO ×2 = 52 KB) e
  come sintesi "God Mode" (RICALIBRATO, 5,9 KB). La decisione D1 è
  giocarlo VELOCE: serve il formato di mezzo.
- **Azione**: creare `PortaleForgia-P5-FASTPLAY.md` (≤6 pagine): (1)
  scaletta a 5-6 scene (arrivo e Cronache dei Quattro Eroi; incontro con
  Thorgrim Barbadiferro e gli antenati; le mura sotto assalto; **duello
  con Skullcrusher** su griglia — l'unico scontro tattico completo, mappa
  da TACTICAL-GRIDS; il Rubino e il ritorno), ciascuna con read-aloud di 3
  righe, prova/scontro ed **esito registrato** (per B4); (2) regola di
  montaggio: tutto ciò che non è il duello si risolve a prove di gruppo
  con CD fisse (APL 13, party di 4 — Hella è tornata); (3) **esiti aperti
  del duello** (Skullcrusher ucciso / ferito grave / fuggito) — MAI un
  esito fisso; (4) puntatori al DEFINITIVO per la versione lunga.
- **Accettazione**: P5 giocabile in una sessione senza aprire altri file;
  il duello ha mappa+statblock+3 esiti; ogni scena produce un dato per B4.
- **✅ FATTO (2026-07-02, sessione 5)**: creato
  `PortaleForgia-P5-FASTPLAY.md` (~6 pagine, master da tavolo D1). 6 scene
  (Cronache → Thorgrim → infiltrazione+Zog'tar → mura → **duello
  Skullcrusher** su MAP 7 → Rubino/ritorno), ognuna con read-aloud di 3 righe,
  prova/scontro ed **► Esito registrato**. Regola di montaggio (prove di
  gruppo CD fisse, party di 4/APL 13). Duello = unico scontro tattico:
  mappa (MAP 7 TACTICAL-GRIDS), statblock giocabile GS 12 `[verifica B5]`, **3
  esiti aperti** (ucciso/ferito grave/fuggito) + conteggio ferite per B4.
  Puntatori al DEFINITIVO. La Cintura rifiuta di spendere cariche (coerenza
  Fauci 1372).

### B4. Il ponte meccanico "La Forgia ricorda le ferite" — [CROSS-ARC, il task più importante]
- **Evidenza**: P5-DEFINITIVO-PARTE2 r.285: *"Ogni ferita che infliggi ora
  all'antenato, la mia Forgia la ricorderà quando affronterai il
  discendente"*; P6 r.746: Aegis Fang canta "sangue Skullcrusher chiama".
  **Nessun file ARC-08 lo implementa**: lo statblock di Fauci di Palude
  (ARC-08, Schede §1) ignora il viaggio. Il piano ARC-08 (A12) aspetta
  questo deliverable.
- **Azione**: creare la **tabella di carry-over** (in coda al FASTPLAY B3
  o file proprio): esito del duello → effetto quantificato su Fauci di
  Palude nel 1372 — proposte da validare, es.: Skullcrusher ucciso = Fauci
  parte con la cicatrice ancestrale attiva, −10% pf e Presenza
  Terrificante CD −2 contro i portatori degli artefatti; ferito grave =
  −1 uso del soffio; fuggito = Fauci sa chi siete, +2 iniziativa ma morale
  fragile sotto i 50 pf (tutte `[INFERRED — needs DM confirmation]`); più
  il gancio inverso: Aegis Fang "sente" Fauci (bonus di circostanza
  definito, non 5e). Propagare: nota nello statblock ARC-08 di Fauci +
  chiusura di ARC-08 A12.
- **Accettazione**: ogni esito possibile del P5 ha un effetto scritto e
  quantificato sul boss dell'ARC-08; lo statblock ARC-08 rimanda alla
  tabella; zero meccaniche ambigue tra sistemi.
- **✅ FATTO (2026-07-02, sessione 6)**: creato
  `PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`. Tabella esito→effetto
  quantificata **sullo statblock reale di Fauci** (GS 15, 312 PF): UCCISO =
  −10% PF (→281) + Presenza CD 25→23 vs portatori; FERITO GRAVE = −1 uso
  soffio (cono indisponibile) + CD −2 al primo soffio; FUGGITO = +2 iniz. a
  Fauci ma ritirata a 75 PF invece di 50. Bonus per N ferite ancestrali
  (+1 TxC o +1d6, cap 3) + cicatrice d'ala (−2 Volare, +2 circostanza in
  volo). Gancio inverso: Aegis Fang "sente" Fauci = +2 circostanza a Thorik
  + preavviso del soffio. Tutti bonus 3.5 tipizzati, **niente 5e**; tutto
  `[INFERRED]`. Lo **statblock ARC-08 di Fauci rimanda alla tabella**; ARC-08
  A12 annotato "consegnato".

### B5. Errata meccanica 3.5 dell'arco
- **Evidenza**: a campione: `CORREZIONE-Boss-Fauci.md` r.334 assegna a un
  GS 12 "8.000 XP (2.000/PG)" — la tabella DMG per PG di 13° vs GS 12 dà
  ~2.925 PE a testa (~11.700 totali): il valore dichiarato è sotto di
  ~30% e va ricalcolato; il doppio
  profilo GS 15/GS 12 si risolve con A3; i boss ricalibrati
  (Terros/Mithral Golem, Elder Fire CR 14, Skullcrusher) non hanno mai
  avuto verifica formale BAB/TS/CD; **Terros va ricalibrato per la
  composizione D15** (3 PG di 13°, nessun supporto); le "prove God Mode"
  del P5 vanno riportate a CD 3.5 esplicite.
- **Azione**: produrre `ERRATA-ARC07-35-Verification.md` nel formato degli
  errata ARC-09/08: XP per incontro (APL 13/D15), statblock dei 4 boss,
  CD delle prove, action economy, poteri della Corona vs
  `campaign-artifacts.md`, poteri della Cintura della Devastazione (D17) =
  Devastation Gauntlets con slot cambiato. Correzioni in place con nota;
  per le parti giocate, annotare "giocato con i valori vecchi" senza
  retcon.
- **Accettazione**: file errata nuovo; XP corretti; un solo profilo per
  boss; Terros a misura di D15; nessuna correzione retroattiva sul giocato.
- **✅ FATTO (2026-07-02, sessione 13)**: creato
  `ERRATA-ARC07-35-Verification.md` (formato errata ARC-09): action economy
  3.5, **XP per incontro APL 13/D15** (con la correzione dell'errore 8.000→
  ~2.925 di CORREZIONE, annotata anche in place), statblock dei 4 boss (Elder
  Fire, **Terros ricalibrato per APL 12/target CR 14-15**, Skullcrusher GS 12,
  Fauci = pointer al GS 15 ARC-08), CD delle prove (fast-play + viaggio),
  poteri Corona vs `campaign-artifacts.md`, Cintura = Devastation Gauntlets
  slot-cambiato. Nota "giocato coi valori vecchi" per le parti giocate (nessun
  retcon). Valori non attestati `[INFERRED]`.

### B6. Ancoraggio al March Clock e viaggio verso Hammerfist
- **Evidenza**: l'arco non nomina mai il March Clock (state.md §2.1); la
  battaglia di Hammerfist finisce al Day 19 e le parti restanti
  (P4→P3B→P5→raccordo) devono stare nei giorni giusti perché il sync
  tenga.
- **Azione**: mezza pagina nell'INDICE (B8): proposta di collocazione
  `[INFERRED — needs DM confirmation]` — es. uscita dalla Forgia ≈ Day
  14-15, salto D16 al Cuore della Montagna = Giorno 3 dell'assedio ≈ Day
  18-19. Coordinare con ARC-08 B6 (stessa tabella, scritta UNA volta e
  puntata).
- **Accettazione**: una sola cronologia condivisa 07→08; nessuna
  contraddizione col Day 19 (ARC-08 E3).
- **✅ FATTO (2026-07-02, sessione 14)**: cronologia B6 scritta come sezione
  dell'INDICE (`ARC07-00-INDICE.md` §Cronologia): proposta `[INFERRED]`
  (uscita Forgia ≈ Day 14-15, P3B+P5 ≈ Day 15-17, raccordo D16/Cuore della
  Montagna ≈ Day 18-19, sync col Day 19 ARC-08), con la nota che il viaggio è
  **tempo soggettivo** (il March Clock reale avanza poco). Da coordinare con
  ARC-08 B6 (stessa tabella).

### B7. Tesoro/WBL dell'arco (al 13°)
- **Evidenza**: l'arco assegna artefatti maggiori (gemme, benedizioni,
  Collana) ma il tesoro "ordinario" non è mai stato contato; il WBL del
  13° (~110.000 mo/PG, DMG) va verificato PRIMA di Hammerfist, perché
  ARC-08 B4 fonda lì la ricchezza d'ingresso e ARC-09 l'ha già auditata a
  valle.
- **Azione**: audit del loot per parte (giocate: dai log B1; future: dai
  master) + tabella per incontro; artefatti/benedizioni contati come da
  audit ARC-09 (ricchezza speciale, non colmano il delta ordinario).
  Chiudere con "ricchezza d'uscita ARC-07 = ingresso ARC-08".
- **Accettazione**: totale coerente col WBL ±20%; handoff esplicito ai due
  audit a valle.
- **✅ FATTO (2026-07-02, sessione 15)**: creato `ARC07-TESORO-WBL-AUDIT.md`
  (metodo ARC-09): WBL 13° ~110.000 mo/PG; **ricchezza speciale** (artefatti/
  benedizioni) contata a parte (non colma il delta ordinario); loot ordinario
  per parte (~15.600 mo attribuibili dal gear di Hella + `[INFERRED]` per
  P3/P4/P5). **Verdetto**: arco povero di loot ordinario, ricco di artefatti —
  il delta di WBL si colma a **Hammerfist (ARC-08 B4)**, non qui. Handoff
  esplicito "uscita ARC-07 = ingresso ARC-08", nessun doppio conteggio degli
  artefatti tra i tre archi.

### B8. INDICE-GENERALE e DM-QUICKSTART dell'arco
- **Evidenza**: 20+ file markdown su 3-4 generazioni, 2 PDF, musica,
  immagini — e nessun indice; il file che doveva esserlo
  (`Mappe/Atlante-Visivo-Mappe.md`) è vuoto (A7). Il DM ci sta giocando
  DENTRO: la mappa serve subito.
- **Azione**: creare `ARC07-00-INDICE.md`: (1) tabella file → parte →
  stato (master/deprecato/ricalibrazione/annesso) dalla matrice A6; (2)
  quickstart 1 pagina: dove siete (G3, composizione D15), cosa viene dopo
  (D2: resurrezione → viaggio veloce → salto D16 → ARC-08), cosa stampare
  (mappa duello, TACTICAL-GRIDS relative, benedizioni, scheda Collana);
  (3) l'ordine di gioco D2 con la nota sulla numerazione (A9); (4)
  cronologia B6; (5) puntatori a `...-risultati.md` e alla scheda Collana.
- **Accettazione**: ogni file compare con uno stato; il DM ha il percorso
  della prossima sessione in una pagina; risultati del viaggio e Collana
  raggiungibili in un click.
- **✅ FATTO (2026-07-02, sessione 14)**: creato `ARC07-00-INDICE.md` —
  quickstart 1 pagina (dove sei G3/D15, cosa viene dopo D2, cosa stampare,
  promemoria canone), tabella file→parte→stato (dalla matrice A6), nota
  numerazione A9, cronologia B6, puntatori a risultati/Collana/Cintura/
  Corona/log/ponte ARC-08. Ogni file dell'arco ha uno stato raggiungibile.

### B9. Artefatti e PNG: i buchi residui dell'audit
- **Evidenza**: già FATTI (2026-07-02): la scheda della **Collana dei Semi
  Eterni** (`PG/Artefatti/Artefatti-Pg/Hella/01_Collana_dei_Semi_Eterni.md`,
  formato Bracieri — il DM validi i punti [INFERRED]) e il file-risultati
  del viaggio (D12). Restano: (1) la scheda `PNG/Sonjak/` **non menziona
  il raid della Stanza della Corona** che lei ha ordinato (G0); (2) né
  Belkram né Urialle hanno una scheda PNG con lo stato finale (**morti**,
  D13); (3) i collegamenti al file-risultati da INDICE/B2/B1; (4) la
  scheda della **Cintura della Devastazione** (D17 — azione in A10).
- **Azione**: (1) aggiornare PNG/Sonjak ("ha ordinato il furto della
  Corona: Urialle + Yochlol half-illithid, fallito, Hella uccisa — il
  party POTREBBE non sapere ancora che il mandante è lei `[verify con
  state.md §4]`"); (2) schede PNG post-mortem per **Belkram (morto,
  redento in punto di morte)** e **Urialle (morta)** nel formato
  AGENTS.md; (3) collegamenti (si chiudono con B8).
- **Accettazione**: la scheda di Sonjak racconta il raid; nessun PNG di G0
  senza stato; 5 artefatti + Cintura documentati e linkati.
- **✅ FATTO (2026-07-02, sessione 12)**: `PNG/Sonjak/Sonjak.md` ora ha la
  sezione "IL RAID DELLA STANZA DELLA CORONA (ARC-06) — mandante" (Urialle +
  Yochlol, fallito, Hella uccisa, i PG forse non sanno ancora che è lei
  `[verify state.md §4]`). Create schede post-mortem `PNG/Belkram/Belkram.md`
  (**morto, redento** in punto di morte) e `PNG/Urialle/Urialle.md` (**morta**,
  uccisora di Hella), formato AGENTS.md, con link incrociati e al log R0.
  Cintura documentata in A10. Con questo **B9 è completo** (Collana e
  file-risultati erano già fatti). I link dall'INDICE si chiudono con B8.

---

## §3 — LOTTO C: Da "coerente" a "memorabile" (priorità P2)

### C1. Atlante di immagini, musica e PDF
- **Evidenza**: `Immagini/` ha 19 file GIÀ ben nominati (raro nel repo),
  `Musica/LaCanzoneDellePietre.mp3` esiste ma nessun file dice **quando**
  suonarla, i 2 PDF (Sinergie artefatti, Benedizioni di Moradin) non sono
  indicizzati da nessun markdown.
- **Azione**: tabella nell'INDICE (B8): asset → scena/parte → "quando
  usarlo" (es. la Canzone delle Pietre alla resurrezione di Hella o alla
  cantillazione `[INFERRED]`; Hella_elementale.png al risveglio;
  ilCuoreDiMoradin.png al rituale). Correggere il typo "Mitrtrsl Golem"
  nel filename immagine.
- **Accettazione**: ogni asset ha un momento d'uso; zero asset orfani.
- **✅ FATTO (2026-07-02, sessione 16)**: creato `ARC07-ATLANTE-ASSET.md`
  (asset → scena/parte → "quando usarlo"): Canzone delle Pietre alla
  resurrezione/cantillazione, Hella_elementale al risveglio, ilCuoreDiMoradin
  al rituale, immagini di Fuoco/Terra/boss mappate, 2 PDF indicizzati.
  `git mv` del typo `Mitrtrsl Golem…` → `Mithral Golem…` (residuo `MitralGolem`
  segnalato [INFERRED], non rinominato per non rompere riferimenti). INDICE
  punta qui.

### C2. Handout giocatore (formato HANDOUTS ARC-09)
- **Evidenza**: materiale-handout naturale mai formalizzato: le **Cronache
  dei Quattro Eroi** ("Le Cronache dicono che 'Quattro Eroi' salvarono
  Hammerfist... Siete VOI." — P5-RICALIBRATO r.19), gli **8 affreschi
  divini** della Sala (P2), le **Benedizioni di Moradin** (il PDF è di
  fatto un handout), la visione della sovrapposizione temporale (P2
  r.982-1007).
- **Azione**: sezione ARC-07 nel file HANDOUTS (o gemello): (1) la pagina
  delle Cronache (da consegnare PRIMA del viaggio — i giocatori scoprono
  di essere la profezia); (2) la tavola degli 8 affreschi con l'A6
  evidenziato; (3) le Benedizioni in formato carta singola per PG; (4) la
  carta-visione della sovrapposizione. Ogni handout con "quando darlo".
- **Accettazione**: handout stampabili; nessuno spoilera il carry-over B4.
- **✅ FATTO (2026-07-02, sessione 16)**: creato `ARC07-HANDOUTS.md` (formato
  ARC-09, una pagina per handout): (1) **Cronache dei Quattro Eroi** da dare
  PRIMA del viaggio; (2) tavola degli **8 affreschi** con **A6 evidenziato**;
  (3) **carta-visione** delle due traiettorie; (4) **Benedizioni di Moradin**
  come carte singole per PG. Ogni handout ha "quando darlo". **Nota
  anti-spoiler B4** esplicita: nessun handout rivela il carry-over
  Skullcrusher→Fauci.

### C3. Conseguenze a lungo periodo (tabella echi)
- **Evidenza**: ganci che nessuna tabella raccoglie: l'**uovo di Fauci di
  Palude** (P6 r.958 — vendetta futura, perfetto per ARC-10 qualunque sia
  l'esito ARC-08), l'**eco "nessuna pietà" del Rubino** (P5-DEF-P2 r.167 —
  il tono della Corona cambia in base a come finisce il duello), le
  Cronache come fama crescente presso i nani (aggancia i Custodi Eterni di
  ARC-08 E5), Thorgrim Barbadiferro da far riecheggiare nella Cerimonia
  delle 100 Asce.
- **Azione**: tabella echi nel formato ARC-09 (evento → eco → quando
  riemerge → file che lo gestisce), con varianti per esito del duello;
  cross-link alla tabella echi ARC-08 (C2) perché uovo e Rubino
  attraversano entrambi gli archi; l'uovo riceve un custode designato
  (dove sta? chi lo cova?) `[INFERRED — needs DM confirmation]`.
- **Accettazione**: tabella completa; nessun eco contraddice ARC-08/09.
- **✅ FATTO (2026-07-02, sessione 17)**: creato `ARC07-CONSEGUENZE-ECHI.md`
  (formato echi ARC-09): tabella evento→eco→quando riemerge→file per uovo di
  Fauci, eco "nessuna pietà" del Rubino, Cronache (→ Custodi Eterni ARC-08 E5),
  Thorgrim (→ Cerimonia 100 Asce). **Varianti per esito del duello** (tono del
  Rubino UCCISO/FERITO/FUGGITO, distinte dal carry-over meccanico B4).
  **Custode designato dell'uovo** `[INFERRED]` (Blackfens, servitore
  superstite → nemesi ARC-10). Cross-link a ARC-08 C2. Nessun eco contraddice
  ARC-08/09 (Rubino resta single-use speso). **LOTTO C completo.**

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Prerequisito: **A0 del piano ARC-08** (state.md al giocato reale) se non già
eseguito. **Nessun lotto è bloccato** (D1-D17 tutte decise). Il tavolo sta
per arrivare a P3B/P5: **la priorità di consegna è B2→B3→B4**, quindi il
lotto A si esegue in parallelo solo dove non li blocca. A11 (Durik)
conviene eseguirlo INSIEME a B2 (stesso file master).

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | A7 (igiene) + A9 (ordine dichiarato D2) | editing mirato | — |
| 2 | A1 + A2 (Skullcrusher, 1.000 anni prima) | find/replace + editing | — |
| 3 | A6 (matrice generazioni + master) | consolidamento | — |
| 4 | **B2 (master resurrezione Hella) + A11 (Durik)** | consolidamento+verifica | A6; D12 (file risultati) |
| 5 | **B3 (P5 fast-play)** | generativo | A1, A2, A6 |
| 6 | **B4 (ponte "la Forgia ricorda" + statblock ARC-08)** | generativo — il task più importante | B3; **[CROSS-ARC]** ARC-08 A12 |
| 7 | A3 (P6 sezione 1372 deprecata + estrazioni) | editing mirato | B4 (per ricollocare il canto di Aegis Fang) |
| 8 | A4 (gemme/cucitura D16) + A5 (livello 13/D15) | editing mirato | A0 |
| 9 | A10 (artefatti: fonte unica D9 + Cintura D17) | consolidamento | — |
| 10 | A8 (DC→CD, inglese) | find/replace | — |
| 11 | B1 (session log del giocato, ARC-06 finale incluso) | intervista DM + scrittura | A0 |
| 12 | B9 residuo (Sonjak + schede Belkram/Urialle morti) | generativo | B1 |
| 13 | B5 (errata 3.5, Terros ricalibrato D15) | verifica | A3, A5 |
| 14 | B6 + B8 (cronologia + INDICE/quickstart) | consolidamento | A6, A9; coord. ARC-08 B6 |
| 15 | B7 (tesoro/WBL al 13°) | audit | B1 |
| 16 | C1 + C2 (asset + handout) | classificazione+generativo | B3 |
| 17 | C3 (tabella echi) | generativo | B4, A3 |

**Regole anti-spreco** (identiche ad ARC-09): (1) passa all'engine SOLO
questo file + i file del lotto corrente + state.md §0-§4 (+ il file
`...-risultati.md` per i lotti B2/B3/B4); (2) niente riletture dell'intero
arco; (3) dopo ogni lotto: `grep` di verifica del criterio di accettazione,
commit, riga di changelog in state.md se il canone è cambiato; (4) aggiorna
la checklist qui sotto.

### Checklist avanzamento

- [x] A1 · [x] A2 · [x] A3 · [x] A4 · [x] A5 · [x] A6 · [x] A7 ·
  [x] A8 · [x] A9 · [x] A10 · [x] A11 — **LOTTO A COMPLETO**
- [~] B1 (log ricostruiti; attende intervista DM) · [x] B2 · [x] B3 ·
  [x] B4 · [x] B5 · [x] B6 · [x] B7 · [x] B8 · [x] B9 — Collana ✅,
  file-risultati ✅, Sonjak-raid ✅, schede Belkram/Urialle ✅, Cintura ✅
- [x] C1 · [x] C2 · [x] C3 — **LOTTO C COMPLETO**
- [x] D1…D17 — **tutte le decisioni DM acquisite (2026-07-02); nessuna
  domanda aperta**

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5**: l'idea del viaggio
temporale come **profezia autoavverante** ("Siete sempre stati voi") con la
battaglia antica che semina meccanicamente quella moderna; la scrittura
delle scene del P5-DEFINITIVO (il Rubino, le due traiettorie sovrapposte di
Skullcrusher e Fauci); il viaggio dello spirito di Hella — tre prove
morali con costi permanenti scelti dalla giocatrice, ora canonizzate nel
file risultati; il metodo di ricalibrazione di Terros.md; le TACTICAL-GRIDS
già in scala; gli asset (musica, immagini nominate, PDF) — nessun altro
arco li ha così curati.

**Cosa lo separa dall'eccellenza**: (1) il boss imminente aveva tre nomi e
tre profondità temporali — ora decisi (Skullcrusher, 1.000 anni: D6-D7) ma
da propagare (A1-A2); (2) P6 trascina una "fine campagna" del 1372 superata
dagli Archi 08-09, con un Fauci GS 12 "morto per copione" che contraddice
il GS 15 a esiti aperti (A3); (3) il gancio più bello — *la Forgia ricorda
le ferite* — non è implementato (B4), e la cucitura del ritorno (Rubino →
Cuore della Montagna, D16) non è scritta; (4) quattro generazioni di file
per parte col tavolo in mezzo al guado, e nessun indice (A6, B8); (5) il
boss del P4 in corso è calibrato su un party che non esiste (Terros con
Therysol: D15). Con A+B2-B4 la prossima sessione è coperta; col resto di B
l'arco tiene i conti; con C il viaggio di 1.000 anni diventa la leggenda
che le Cronache dei Quattro Eroi promettono ai giocatori.
