# PIANO DI REVISIONE ARC-09 (Post-Hammerfist) — Coerenza & Qualità

> **Versione**: v1 (2026-07-02) — prodotto da audit completo dell'arco.
> **Scopo**: documento **autocontenuto** da dare in pasto a un engine AI
> specializzato (o a più sessioni brevi) per eseguire le correzioni **a lotti**,
> senza dover ri-derivare il contesto ogni volta. Ogni task ha: file coinvolti,
> problema con evidenza, azione richiesta, criterio di accettazione.
> **Benchmark di qualità**: (interno) `Arco-Post-Hammerfist-P2D-PALIO-CHANNATHGATE-*.md`,
> `Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md`, `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md`;
> (esterno) *Red Hand of Doom* (Jacobs/Wyatt 2006), *Heroes of Battle* (3.5),
> AP Paizo PF1e: *Rise of the Runelords*, *Curse of the Crimson Throne*,
> *Kingmaker*, *War for the Crown*.

---

## §0 — REGOLE D'ORO per l'engine esecutore (leggere SEMPRE prima di ogni lotto)

1. **`campaign/state.md` vince** su qualunque altro file in caso di conflitto
   (regola del repo, vedi intestazione di state.md). Non riscrivere la storia:
   ogni modifica di canone va **appesa al changelog** di state.md.
2. **Sistema D&D 3.5 SRD only** — niente 5e (no azioni bonus, no vantaggio/
   svantaggio, no legendary actions), niente lore FR post-1385 DR. Ambientazione
   Faerûn 1372 DR.
3. **Mai inventare** stat, poteri di artefatti o conoscenze PNG: se serve un
   dato non presente, marcarlo `[INFERRED — needs DM confirmation]`.
4. **Un lotto = un commit** con messaggio descrittivo. Non mescolare lotti.
5. Prima di toccare PNG/artefatti consultare
   `skills/rumblingstone-campaign/references/campaign-coherence.md` e
   `campaign/state.md` §4 (chi sa cosa) e §6 (stato artefatti).
6. I file `*-MAPPE*.md` usano scala **1,5 m/quadretto** — mantenerla.
7. Lingua: italiano (nomi meccanici 3.5 come da convenzione dei file esistenti).

### Decisioni di canone GIÀ PRESE (applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| D1 | Il drago nero di Rhest si scrive **Regiarix** | RHoD originale + file RHEST |
| D2 | La città finale è **Rethmar** (mai "Rethman", mai "Damarath") | state.md |
| D3 | La PG druida è **Hella** (usare "Hella"; "Hellas" ammesso solo come nome-quest storico nei titoli file) | state.md §1 |
| D4 | Il PG monaco è **Tordek Durinheart** | campaign-history.md |
| D5 | Xal'thor = comandante **Illithid** (vuole i Bracieri); Vaereth = Githyanki liberi (vogliono l'Orbe); Sethrax = emissario di Zalkatar | state.md changelog 2026-05-03 |
| D6 | March Clock: Day 19 = sync Hammerfist/Terrelton; **Day 40 = Notte dei Drow (Fase 0); Day 42 = assalto a Rethmar (Fasi 1-4)** | state.md §2.1 (vince per regola 1) |
| D7 | Ghostlord: ostile default = +2.400 non morti; neutralizzato = +400; redento = +600 pro-difensori | state.md §2.3 |
| D8 | **Nessun "5° atto" al Fane di Tiamat** (decisione DM 2026-07-02). L'Avatar di Tiamat viene richiamato **durante** la battaglia di Rethmar (che copre ~3 giorni, Day 40-42) tramite il rituale a 10 round dei chierici/ritualisti draconici della Mano Rossa (Fase 2). Il Fane nel Shaar resta solo origine dell'orda e sede del Ritual Clock — non una location giocata | DM, questa revisione |
| D9 | Alleanza Tiri Kitor riuscita = **100 ranger elfici + 20 gufi giganti** a Rethmar (la tribù è ~500 anime: ne invia un quinto come forza da guerra; il resto difende Starsong). Correggere state.md §2.4 (+500 → +120) e INDICE (50+10 → 100+20) | DM 2026-07-02 |
| D10 | Nani a Rethmar: **300 mercenari da Dauth** (torneo vinto) + **150 lance di Re Thorek** come flusso separato condizionato dagli hook politici (sigillo Maewen + lettera Thorik). Totale max 450. Correggere state.md §2.4 (400 → 300) | DM 2026-07-02 |
| D11 **v2** | **Tyrgarun = drago BLU antico (Old), CR 18 — il TERRORE DEI CIELI della battaglia, NON cavalcatura di Azarr Kul.** Non sta "in riserva": è la ragione per cui i difensori non possono tenere i cieli. Script a scalini: **Fase 1** = set-piece di bombardamento (soffio sui bastioni come *hazard* con contromosse — balliste, gufi Tiri Kitor, missione-esca dei PG — NON scontro frontale: a CR 18 in volo è imbattibile per design); **Fasi 2-3** = copertura aerea mobile dei ritualisti (minaccia a orologeria); **Fase 4** = il Mythal completato **lo inchioda a terra** (già canone: P2D-INTEGRAZIONE r.201) → solo allora diventa uccidibile dal party+alleati, oppure fugge (nemesi ARC-10). Azarr Kul combatte comunque a terra con l'Avatar (STRUTTURA §6): il drago è un incontro separato, sbloccato dal Mythal. Correggere INDICE r.27/443 ("monta Tyrgarun" via; "Very Old CR 20" → "Old CR 18") e ARMATE-SYNC §2.1 ("black adult" → "blue old") | DM 2026-07-02, **rivista su obiezione DM: "se il drago non si usa, perché alzare il Mythal? deve essere spaventoso"** |
| D12 | Debito di Tordek (state.md §5): riformulare in **"presentarsi a Dauth entro il Day 29 (vigilia delle preliminari del Torneo)"** — coerente con HOOKS v2 (invito Day 24, arrivo 28, torneo 30-32) | DM 2026-07-02 |
| D13 | **La battaglia di Rethmar si gioca A EVENTI, in stile cinematografico/Critical Role** — remix della catena di eventi della Battle of Brindol (RHoD Parte 4, [Private source]): i PG vivono la battaglia come sequenza di **scene discrete ad alta posta che SCELGONO loro** (menù di crisi simultanee: ne scegli 1-2, le altre si risolvono male off-screen = conseguenza), NON come wargame. **Le crisi SCELTE si giocano dal vero, tatticamente**: incontro completo su griglia 1,5 m/q con statblock, iniziativa e tattiche come ogni altro scontro della campagna — **esito NON predefinito**, deciso dai dadi (vittoria/parziale/sconfitta, ciascuna con conseguenze). L'astrazione off-screen esiste SOLO per le crisi non scelte. **Esclusa** la gestione armate alla Kingmaker/Ultimate Campaign (astrae i PG, sessioni bibliche). Le meccaniche di massa di Hammerfist e i calcoli ARMATE-* restano **solo lato DM** come sfondo strategico che alimenta la narrazione — mai portati al tavolo. I **VP restano ma nascosti**: tracker del DM ("il Fronte") che colora le descrizioni e determina l'esito, mai un punteggio mostrato ai giocatori. Heroes of Battle si riduce a: 1 check di morale per ondata + ruoli di comando PG come azioni di scena | DM 2026-07-02, su domanda "eventi RHoD presenti? VP snatura? Kingmaker o eventi scelti dai PG?" |

### Decisioni di canone da chiedere al DM

**✅ TUTTE RISOLTE (2026-07-02).** Q1→D9 (elfi), Q2→D10 (nani), Q3→D11
(Tyrgarun), Q4→D12 (debito Tordek), Q5→D8 (niente atto al Fane).
Il piano non ha più blocchi: l'engine può eseguire tutti i lotti nell'ordine
di §4 senza ulteriori input dal DM.

---

## §1 — LOTTO A: Incoerenze di canone (priorità P0 — correggere per prime)

### A1. Ortografia del drago nero: Regiarix vs Regiarax
- **Problema**: entrambe le grafie coesistono. "Regiarax": INDICE (4 occorrenze,
  righe 41, 200-212, 557), `P3-Starsong-Hill-ALLEANZA-ELFI-TESTO.md` (2),
  `HOOKS-Hella-SacredForest.md` (1), `P2-RHEST-OVERVIEW.md` (1, "Regiarix/Regiarax"),
  più occorrenze in `campaign/` e `skills/`. "Regiarix" ovunque nei file RHEST.
- **Azione**: sostituire globalmente Regiarax → **Regiarix** (D1) in tutto il repo
  (esclusi i changelog append-only di state.md: lì aggiungere una riga nuova).
- **Accettazione**: `grep -r "Regiarax"` restituisce solo righe di changelog.

### A2. Giorno d'arrivo dell'orda: 38 vs 40 vs 42
- **Problema**: tre versioni. `HOOKS-INTEGRATION-MASTER.md` §6.1 "Giorno 38 Azarr
  Kul arriva a Rethmar" e §1.1 "Day 38-42 Phase 0-4"; `P3-BATTAGLIA-FINALE-RETHMAN-STRUTTURA.md`
  r.12 e `ARMATE-SYNC` §1/§2/Fase 1 dicono "Day 40 arrivo/assedio"; state.md §2.1 e
  INDICE r.573 e `P2D-PALIO-INTEGRAZIONE` r.107 dicono Day 42.
- **Azione**: applicare **D6** (Day 40 = Fase 0 Notte dei Drow; Day 42 = arrivo
  orda + Fasi 1-4). Correggere: HOOKS §1.1 e §6.1, STRUTTURA r.12, ARMATE-SYNC
  §1, §2 (titolo tabella) e §4-Fase1 ("Day 40, alba" → "Day 42, alba").
  Nota: il ledger `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` va
  allineato nello stesso commit.
- **Accettazione**: un solo giorno canonico per ciascuna fase in tutti i file;
  riga aggiunta al changelog di state.md.

### A3. Finestre temporali delle quest (INDICE obsoleto)
- **Problema**: INDICE dichiara Torre Day 21-23 (r.158), Rhest Day 23-25 (r.191),
  Torneo Day 22-24 (r.215); state.md §0 dice Torre 28-35, Rhest 25-32, Torneo
  25-34; HOOKS §1.1 (più recente e dettagliato) dice Torneo 30-32 (arrivo 28),
  Torre/rituale 33-35.
- **Azione**: aggiornare le durate/finestre dell'INDICE alle finestre di
  state.md §0, citando HOOKS §1.1 come cronologia fine. NON toccare HOOKS.
- **Accettazione**: INDICE e state.md §0 coincidono; nessun riferimento residuo
  a Day 21-25 per Torre/Torneo.

### A4. Nomi PG usati come PNG in ESITI-CONSEGUENZE (§7, r.301-318 + monologhi)
- **Problema** (artefatto di generazione, grave): `P3-BATTAGLIA-FINALE-ESITI-CONSEGUENZE.md`
  usa "**Tordek** (Tiri-Kitor)" per il leader elfico, "**Artemis Learmount**
  (Dauth)" per il leader di Dauth (e lo cita parlante nel monologo "Vittoria
  Tattica", r.382), e "**Tordek Tozzefort** (300 nani)" per il comandante nanico.
  Ma Tordek e Artemis sono PG (D4). I leader corretti: Tiri Kitor = **Sellyria
  Starsinger / Killiar Arrowswift** (Starsong TESTO); Dauth = **Magister Veylan**
  `[INFERRED — needs DM confirmation]` o altro PNG di Dauth; comandante dei 300
  nani = PNG senza nome in STATBLOCCHI-EPICI §7 (proporre nome, es. "Khorn"
  già citato in HOOKS-Thorik r.157, oppure crearne uno e marcarlo INFERRED).
- **Azione**: sostituire i tre nomi + monologo; correggere anche i refusi della
  stessa sezione ("gloriosa-mente", "nega-zia", "complètamente", "lo prezzo",
  "stravagato" → "stravolto").
- **Accettazione**: nessun nome di PG usato per PNG; refusi eliminati.

### A5. Numeri Ghostlord non allineati al rescale armate v2
- **Problema**: INDICE r.320 "200 undead in meno" contro state.md §2.3
  (+2.400 / +400 / +600, D7). Anche `P3-Ghostlord-LICH-ALLEANZA-TESTO.md` r.126
  parla genericamente di "CR -1/-2" senza i numeri v2.
- **Azione**: aggiornare INDICE e Ghostlord-TESTO ai numeri D7, con rimando a
  state.md §2.3.
- **Accettazione**: i tre rami (ostile/neutralizzato/redento) con numeri identici
  in INDICE, TESTO e state.md.

### A6. Alleati elfi e nani: numeri contraddittori — RISOLTO da D9/D10
- **Problema**: Elfi: +500 vs 50+10. Nani: 300 vs 400 (+150 lance come flusso
  separato in 5 file HOOKS).
- **Azione**: applicare **D9** (elfi = 100 ranger + 20 gufi giganti) e **D10**
  (nani = 300 Dauth + 150 lance separate) propagando in: state.md §2.4
  (+500→+120; 400→300), INDICE r.302/252/507, STRUTTURA §8, ARMATE-SYNC §2/§3
  (ricalcolare i 5 scenari difensori con i nuovi totali), ESITI,
  STATBLOCCHI-EPICI §7. Riga di changelog in state.md.
- **Accettazione**: un solo numero per fazione in tutto il repo + changelog;
  scenari ARMATE-SYNC ricalcolati.

### A7. Tyrgarun: identità e ruolo incoerenti — RISOLTO da D11 v2
- **Problema**: colore, età, CR 20 vs budget CR 16-18, cavalcatura sì/no.
- **Azione**: applicare **D11 v2** (blue Old CR 18, terrore dei cieli a
  scalini, inchiodato a terra dal Mythal in Fase 4, NON cavalcatura):
  correggere INDICE r.27/443, ARMATE-SYNC §2.1, STRUTTURA §6 (aggiungere
  Tyrgarun alle Fasi 1/2-3/4 secondo lo script D11) e la scheda
  `PNG/Azarr_Kul/Azarr_Kul.md` (rimuovere "monta Tyrgarun"). Le meccaniche
  dettagliate del set-piece (hazard di bombardamento, contromosse, statistiche
  del drago a terra) si scrivono nel lotto **C1 punto (d)** — qui solo la
  coerenza dei riferimenti. Applicare anche **D12** nello stesso lotto:
  riformulare il debito di Tordek in state.md §5 ("entro il Day 29, vigilia
  delle preliminari").
- **Accettazione**: colore/età/CR/ruolo identici ovunque; la Fase 3 boss
  (Azarr Kul + Avatar) resta CR 16-18 senza il drago sommato; debito Tordek
  coerente con la timeline HOOKS v2.

### A8. File citati come "fonte autoritativa" ma INESISTENTI
- **Problema**: `HOOKS-INTEGRATION-MASTER.md` §8 rimanda a
  `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md`
  ("fonte autoritativa di tutti gli echi del Torneo") e §9 a
  `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DM-MASTER-REFERENCE.md`;
  `HOOKS-Thorik-RethmarLetter.md` r.254 rimanda a
  `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-SUBQUEST-Thorik.md`. **Nessuno dei tre
  esiste** nella directory.
- **Azione** (scegliere per file): (a) creare i tre file consolidando i contenuti
  già sparsi nei 17 file P2B (preferito: il DM-MASTER-REFERENCE del torneo
  colmerebbe anche G10), oppure (b) ripuntare i link a file esistenti
  (`MINIMAPPA-TIMELINE-ALLEANZE`, `HOOKS-INTEGRATION-MASTER` §8).
- **Accettazione**: zero link rotti (verificare con uno script: ogni `Arco-*.md`
  citato esiste su disco).

### A9. File vuoto + file "da integrare"
- **Problema**: `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO-Description.md` = 0 byte;
  `P2B-Torneo-Tordek-PARTE1-to-Be_integrated.md` è marcato ⚠️ in INDICE e
  contiene 5e-ismi ("attacco con vantaggio posizione", "Riflessi DC 16" — in
  3.5 si scrive CD) e contenuto duplicato con PARTE1/OTTO-PORTE.
- **Azione**: (1) riempire il file Description con le descrizioni narrative dei
  3 campi drow (il file gemello COMPLETO ha già mappe e tattiche) o eliminarlo
  aggiornando INDICE; (2) fondere il to-Be_integrated nei file PARTE1/OTTO-PORTE
  definitivi, convertendo la terminologia a 3.5 puro, poi marcarlo DEPRECATED
  in testa o eliminarlo.
- **Accettazione**: nessun file 0-byte; nessun ⚠️ residuo in INDICE; zero
  occorrenze di "vantaggio/svantaggio/bonus action" fuori da note ERRATA.

### A10. Fane di Tiamat: contraddizione e semantica dei clock
- **Problema**: `ESITI-CONSEGUENZE` §6 (r.287) dice che in caso di vittoria la
  Red Hand "inizia a costruire **un** Fane di Tiamat", ma il Fane **esiste già**
  (state.md §2.1 Day 1: "Horde leaves Fane of Tiamat (Shaar)"). Inoltre state.md
  §2.0 definisce il Ritual Clock come "rituali al Fane, indipendenti dalla
  marcia" mentre §3 descrive il clock di Azarr Kul come "Reach Rethmar in 18
  in-world days" (9/18) — countdown di marcia e clock rituale si confondono.
- **Azione**: correggere ESITI ("rifortifica il Fane nel Shaar / ne erige uno
  nuovo avanzato"); in state.md §3 rinominare la riga di Azarr Kul in "March
  countdown (18 giorni)" o spostare il 9/18 sotto il Ritual Clock con trigger
  espliciti (quali eventi lo avanzano). Richiede 1 riga di changelog.
- **Accettazione**: definizione univoca dei due clock; nessun riferimento a un
  Fane "da costruire".

### A11. INDICE: finale del Torneo ancora pre-fix fazioni
- **Problema**: INDICE r.247-249 "Githyanki Red Dragon attack! ... Xal'thor
  Illithid Commander" fonde le due fazioni che il fix 2026-05-03 (state.md
  changelog) ha separato (D5).
- **Azione**: riscrivere il bullet: Day 3 = assalto di **Xal'thor** (invasione
  illithid, obiettivo Bracieri) + arrivo di **Vaereth** (Githyanki liberi su
  draghi rossi, obiettivo Orbe) + smascheramento di **Sethrax** (Round 7).
- **Accettazione**: INDICE coerente con state.md §3 e PARTE3-Giorno3.

### A12. File legacy con canone superato
- **Problema**: `inizio.md` e `Quest 1 – Druida Hellas: Il Cerchio Sacro della
  Foresta.md` contengono il brainstorm originale: finale a "**Damarath**"/Dauth,
  Githyanki genericamente su draghi rossi, e code conversazionali AI ("Dimmi se
  vuoi approfondire...", "Dove preferisci iniziare?").
- **Azione**: aggiungere in testa a entrambi un banner
  `> ⚠️ DEPRECATED (2026-07): brainstorm storico. Canone corrente: INDICE-GENERALE + state.md.`
  Ripulire le code conversazionali. NON cancellare (valore storico).
- **Accettazione**: banner presente; INDICE li etichetta "storico/deprecato".

### A13. "Rethman" e rinomina file
- **Problema**: refuso "Rethman" nel body di ~10 file P3 e nel filename
  `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAN-STRUTTURA.md`.
- **Azione**: sostituire Rethman → Rethmar ovunque; `git mv` del file in
  `...-RETHMAR-STRUTTURA.md` aggiornando TUTTI i riferimenti (INDICE, state.md
  §2 nota, ARMATE-SYNC r.3, DM-QUICKSTART-ARC09, ecc.).
- **Accettazione**: `grep -ri "rethman"` = 0 risultati; link tutti validi.

---

## §2 — LOTTO B: Completamento contenuti sotto-standard (priorità P1)

> Benchmark: ogni quest deve avere il "pacchetto Palio" — struttura a giorni/fasi,
> skill challenge con CD esplicite per APL 13, fazioni con agende, read-aloud,
> conseguenze quantificate sull'assedio, checklist DM, mappa in scala.

### B1. Rhest è scheletrico (il gap più grande dell'arco)
- **Evidenza**: i 5 file FASE sono da 1,0-2,4 KB l'uno contro i 18-25 KB del
  Palio o della Torre. Rhest in RHoD originale è mezzo capitolo (pp. 54-80).
- **Azione** — portare ogni fase allo standard, in 5 mini-lotti (uno per file):
  1. FASE1 Blackfens: tabella incontri palude d12 (già solo citata), viaggio
     esagoni, read-aloud arrivo, aggancio Tiri Kitor (se Starsong già fatta:
     guide elfiche = vantaggio meccanico esplicito).
  2. FASE2 Razorfiend: tattiche del nido, terreno acquitrinoso 3.5 (movimento,
     nuotare, visibilità), 2 read-aloud.
  3. FASE3 intrusione: mappa rovine sommerse con scala, regole subacquee SRD
     (trattenere il fiato, combattimento sott'acqua, incantesimi), infiltrazione
     alternativa stealth/diplomazia (prigionieri lucertoloidi).
  4. FASE4 boss: arena su 3 quote (acqua/superficie/volo), fasi del drago
     (Regiarix usa hit-and-run e Darkness come da RHoD), trigger fuga Saarvith,
     sinergia coi poteri attuali degli artefatti (state.md §6).
  5. CONSEGUENZE: collegare esplicitamente a state.md §2.3 (-1 drago, -2
     Razorfiend), intel ottenibile (piani d'assedio → -1 CR a una fase di
     Rethmar a scelta), eco Tiri Kitor (vendetta di Lanikar → +VP alleanza).
- **Accettazione**: ogni file ≥ standard Palio per struttura; CD sempre esplicite;
  zero meccaniche 5e; conseguenze numeriche allineate a state.md.

### B2. Starsong Hill: strutturare la diplomazia
- **Evidenza**: TESTO r.? "prove Charisma/Wisdom" generiche; in RHoD il funerale
  di Lanikar è la scena-cardine emotiva.
- **Azione**: skill challenge formale stile Palio §2.1 (3 atti: arrivo/festa
  funebre/consiglio; CD 20-26 per APL 13; successi richiesti 3/5; fallimento =
  quest di prova più dura, non vicolo cieco), scena del funerale con read-aloud,
  tabella "cosa impressiona i Tiri Kitor" per classe PG.
- **Accettazione**: la quest è giocabile senza improvvisare CD; esiti a 3 rami
  con numeri (alleanza piena / parziale / rifiuto) → riflessi in ARMATE-SYNC.

### B3. Ghostlord: pacchetto completo della scelta morale
- **Evidenza**: TESTO buono ma statblock thin (3,3 KB) e mancano le conseguenze
  a lungo termine per ciascuno dei 3 rami (filatteria: restituire/distruggere/
  vincolare) sul dopo-campagna.
- **Azione**: statblock 3.5 verificato del Lich druido CR 14 (o rimando a scheda
  `PNG/Ghostlord/Ghostlord.md` come unica fonte), mappa lair "leone di pietra"
  con scala, tabella conseguenze per ramo (Rethmar + epilogo + hook ARC-10),
  read-aloud del santuario interiore.
- **Accettazione**: un'unica fonte autoritativa per le stat; 3 rami quantificati.

### B4. Handout giocatore (benchmark Paizo)
- **Evidenza**: la lettera di Brenna (hook Thorik) non ha testo integrale;
  mancano handout fisici in tutto l'arco.
- **Azione**: creare `Arco-Post-Hammerfist-HANDOUTS.md` con: (1) testo integrale
  della lettera sigillata di Brenna (contenuto già specificato in HOOKS-Thorik
  r.8: split 3-4 del Consiglio, Halveth corrotto, Lorana viva, richiesta lance);
  (2) sigillo/invito del Torneo di Maewen; (3) mappa in pelle di Tempestas
  (descrizione + cosa mostra); (4) bracket del torneo compilabile; (5) volantino
  del Palio con le 7 contrade; (6) i 3 esiti della divinazione di Saraah come
  carte-visione.
- **Accettazione**: file unico stampabile, ogni handout con nota "quando darlo".

### B5. Verifica meccanica 3.5 estesa a P2/P3 (oggi copre solo P1)
- **Evidenza**: `ERRATA-PARTE1-Quest-Hellas-35-Verification.md` esiste solo per
  la Parte 1. Azarr Kul (STATBLOCCHI-EPICI §1) ha ~119 pf e CA 28 a CR 15: per
  un party APL 14 con 5 artefatti è un boss da 2 round — sotto il benchmark
  (il Kul originale RHoD era già ~112 pf per party di livello 10-12).
- **Azione**: passata di verifica su STATBLOCCHI di P2A/P2B/P2-RHEST/P3:
  BAB/grapple, CA contatto/impreparato, TS, slot incantesimi, action economy
  (solo standard/movimento/round completo/swift/immediate), e **upscale del
  boss finale** (proposta: Chierico 12/Guerriero 4, pf ~150-170, buff pre-cast
  listati, 2 contingency; mantenere CR scena 17-18 con Avatar). Produrre
  `ERRATA-PARTE2-3-35-Verification.md` nello stesso formato della P1.
- **Accettazione**: file errata nuovo; statblock corretti in place con nota.

### B6. Economia del tesoro (WBL 3.5) — gap strutturale
- **Evidenza**: INDICE §Statistiche dichiara ~50.000 mo + 15-20 oggetti per
  l'intero arco 13→16. Il WBL 3.5 (DMG) richiede ~110k mo/PG al 13° e ~210k al
  16°: per 4 PG servono **~+400k mo equivalenti**, non 50k. (Gli artefatti
  legacy compensano solo in parte.)
- **Azione**: audit del loot per quest; creare tabella tesoro per encounter
  (stile Paizo: dove, cosa, valore) distribuendo ~300-400k mo equivalenti
  sull'arco, con pesatura verso Rhest (tesoro del drago — da benchmark il hoard
  di un adult black è il veicolo naturale), Torre (oggetti di Zalkatar), Torneo
  (premi), Rethmar (ricompense civiche/titoli). Aggiornare INDICE §Loot.
- **Accettazione**: totale dichiarato coerente col WBL ±20%; niente oggetti
  inventati fuori SRD senza flag.

### B7. Tabelle incontri casuali di viaggio (benchmark RHoD)
- **Evidenza**: RHoD ha tabelle per regione; qui esiste solo un accenno in
  RHEST-FASE1. I viaggi Day 20-40 (Sacred Forest, strada del deserto, Dauth,
  Thornwaste) sono senza tabelle.
- **Azione**: creare `Arco-Post-Hammerfist-INCONTRI-VIAGGIO-CANNATH-VALE.md`:
  d% per 4 macro-zone × 2 finestre temporali (Day 20-30 / 31-42, l'orda avanza
  → tabelle più cattive), EL 9-13, 30% incontri non-combat (profughi, disertori
  gnoll, mercanti di Sal, pattuglie drow da interrogare). Riusare gli incontri
  già pronti delle MISSIONI-BREVI come voci della tabella.
- **Accettazione**: ogni tratta di viaggio dell'arco ha la sua tabella; EL
  dichiarato; almeno 1/3 delle voci con opzione non violenta.

---

## §3 — LOTTO C: Meccanismi mancanti per renderla "magnifica" (priorità P2)

> Qui si passa da "coerente" a "memorabile". Riferimenti: Heroes of Battle
> (assedio), CotCT (morale cittadino), Kingmaker (ricompense di dominio),
> War for the Crown (sandbox politico — già parzialmente coperto dal Palio).

### C1. Cornice leggera d'assedio (Heroes of Battle ridotto — al servizio di C7)
- Oggi le ondate di Fase 1 sono "blocchi narrativi" (STATBLOCCHI-EPICI §9).
- **Vincolo D13**: questa cornice è **sfondo lato DM**, non un wargame al
  tavolo. Massimo 1 pagina; tutto ciò che i giocatori vedono passa per gli
  eventi di C7.
- **Azione**: 1 pagina di regole in STRUTTURA: (a) **Victory Points** già
  esistenti → collegarli a check di **Morale** per ondata (difensori tirano
  1d20 + VP correnti vs CD ondata; fallimento = un settore cede) — **VP
  nascosti**: il DM li traccia, i giocatori sentono solo le conseguenze
  narrate; (b) **ruoli di comando PG** per round di battaglia (Comandante/Campione/Fulcro Arcano/
  Salvatore — azioni da 10 minuti con effetti quantificati, es. Thorik
  Comandante: +2 morale a un settore); (c) tabella d12 **eventi di battaglia**
  per fase (breccia, incendio, eroismo PNG, duello richiesto...). Riusa il
  precedente di Hammerfist ("meccaniche massa combattimento Hammerfist style",
  INDICE r.414) come base dichiarata; (d) **set-piece Tyrgarun (D11 v2)** —
  il benchmark è Abithriax sulle mura di Brindol in RHoD: in Fase 1 il drago
  è un *hazard* di bombardamento (passate di soffio 16d8 elettricità sui
  bastioni, CD Riflessi ~28, con contromosse quantificate: nidi di balliste
  CD/pf, squadroni gufi Tiri Kitor che gli negano le passate, missione-esca
  PG), in Fasi 2-3 clock di copertura aerea sui ritualisti, in Fase 4 il
  Mythal lo **inchioda a terra** (canone P2D-INTEGRAZIONE r.201): statblock
  3.5 del blue Old CR 18 *a terra* (niente volo = niente flyby/kiting → CR
  effettivo ~16-17, epico ma battibile da party APL 14 + alleati), oppure
  fuga = nemesi per campagne future.
- **Accettazione**: il DM può risolvere Fase 1 senza improvvisare; i VP hanno
  effetto meccanico continuo, non solo a fine battaglia.

### C2. Track del Morale/Paura di Rethmar (benchmark CotCT)
- Il Consiglio (3 sedute) esiste; manca il **polso della popolazione**.
- **Azione**: contatore Morale Cittadino 0-10 in `PNG/Consiglio_Rethmar/`:
  eventi che lo muovono (arrivo profughi, notizie di Talar, vittorie PG,
  esecuzione di Halveth...), effetti a soglie (7+: +150 miliziani volontari;
  3-: diserzioni, -1 ai VP di Fase 1; 0: resa civile anticipata). Collegarlo
  alle sedute del Consiglio e alla Riserva di Lorana.
- **Accettazione**: tabella eventi→delta + 3 soglie con effetti numerici.

### C3. Contingenze "se falliscono / se muoiono" per quest (benchmark Paizo)
- Gli echi coprono il "se saltano la quest"; manca il "se la falliscono a metà"
  e il protocollo morte PG (APL 13: raise disponibili? dove? costo narrativo?).
- **Azione**: sidebar "SE FALLISCONO" in coda a P1C, P2A-PARTE4, P2B-PARTE3,
  RHEST-FASE4, Ghostlord (esiti già parziali → uniformare); più una nota unica
  in DM-QUICKSTART: risorse di resurrezione nel Vale (il precedente esiste:
  Hella è già stata resuscitata col Cuore di Moradin, ora speso — state.md §6).
- **Accettazione**: nessun vicolo cieco; ogni fallimento produce storia (costo,
  non stop).

### C4. Scene "spotlight" dei 4 PG nella battaglia finale — VERIFICA
- `P3-BATTAGLIA-FINALE-MYTHAL-FOCUS-PG-SCENA-EROICA.md` esiste (11 KB, buono).
- **Azione**: solo audit di coerenza: le scene usano i poteri attuali degli
  artefatti (state.md §6) e gli esiti dei rami (es. Tordek con/senza Porta 4,
  Hella in forma elementale sì/no)? Aggiungere le varianti mancanti.
- **Accettazione**: ogni scena ha variante per i 2-3 stati possibili del PG.

### C5. Epilogo giocabile dentro/dopo Rethmar (D8: niente atto al Fane)
- In RHoD la chiusura è il colpo al Fane; qui per decisione DM (D8) il climax
  equivalente è **già dentro la battaglia**: il rituale a 10 round della Fase 2
  che richiama l'Avatar è il "Fane portato in campo". Il post-vittoria però
  resta solo narrato (monologhi ESITI).
- **Azione**: (1) potenziare la Fase 2 perché regga il peso di "quinto atto":
  l'altare campale dei ritualisti come mini-location mappata (3 anelli di
  guardie, foci distruttibili con pf/CD, l'Artefatto Maligno di Fase 0 come
  focus se rubato), scelta tattica esplicita per i PG (interrompere il rituale
  vs tenere le mura — non si può fare entrambe senza alleati); (2) espandere
  la cerimonia-epilogo post-battaglia con una scena giocata per ciascun PG
  (già abbozzate in ESITI §7-8) + un'ultima decisione collettiva sul destino
  del Fane nel Shaar lasciata come hook narrato per campagne future.
- **Accettazione**: la Fase 2 ha mappa/statistiche/costi di scelta espliciti;
  la campagna ha una chiusura giocata, non solo letta.

### C6. Ricompense di dominio/titolo (benchmark Kingmaker)
- ESITI §7-8 accenna a titoli/ambasciate; nessuna meccanica.
- **Azione**: mezza pagina in ESITI: per esito A/B, cosa ottiene concretamente
  ogni PG (titolo, terra, seggio, scuola monastica di Tordek, cerchio di Hella)
  con 1 beneficio meccanico ciascuno (es. "Custode di Rethmar: ospitalità +
  10 PNG di servizio + 1.000 mo/mese di rendita") — utile per ARC-10.
- **Accettazione**: tabella esito×PG compilata.

### C7. IL MAZZO EVENTI DI RETHMAR — la battaglia a scene scelte dai PG (D13)
- **Gap**: la Battle of Brindol originale (RHoD Parte 4, [Private source]) non
  è "ondate": è una **catena di eventi discreti** — combattimenti di strada,
  il drago sulle mura, l'assassino che punta al comandante della città, la
  difesa della cappella/ospedale, la breccia, il duello col Wyrmlord — con
  pause di recupero scandite. Nei file attuali di Rethmar esiste lo scheletro
  a Fasi 0-4 (i macro-eventi) ma la Fase 1-2 è a ondate generiche: **gli
  eventi in stile Brindol non ci sono ancora**. Questo lotto li porta,
  potenziati, sui 3 giorni (Day 40-42).
- **Azione**: creare `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-EVENT-DECK.md`:
  1. **12-16 carte evento** distribuite sui 3 giorni (Fase 0 → 4). Ogni carta
     è un **incontro tattico completo, da giocare dal vero** (regola D13):
     trigger (quando/dove), read-aloud di 3 righe, **mappa tattica su griglia
     1,5 m/q** (nuova o riuso di una mappa P3 esistente), **statblock 3.5 o
     puntatore a STATBLOCCHI-EPICI**, EL dichiarato (13-17 a seconda della
     campana), tattiche nemiche, posta in gioco, **spotlight PG designato**,
     e **3 esiti aperti** (vittoria / parziale / sconfitta — l'esito lo
     decidono i dadi, mai la trama) ognuno con conseguenza su Fronte/VP;
     più la conseguenza "ignorata" se la carta non viene scelta.

     **REGOLA DELLE TRE SORGENTI (vincolante — riusa > espandi > inventa):**
     ogni carta dichiara la propria sorgente in testa:
     - **[S1 — RHoD upscalato]** (~5-6 carte): gli eventi della Battle of
       Brindol originale, presi dalla copia del DM ([Private source], mai
       riprodurre testo), **espansi a APL 14 e riallineati all'esercito
       RumblingStone v2** (10k orda, 5 draghi, drow di Sonjak, Githyanki,
       Teschio Nero): la breccia, il drago sulle mura (→ carta Tyrgarun,
       C1.d), il cecchino sul comandante, la difesa della cappella/ospedale,
       il duello col Wyrmlord, i combattimenti di strada coi civili.
     - **[S2 — echi di campagna]** (~5-6 carte): eventi in cui i PG
       interagiscono con ciò che l'arco ha GIÀ costruito — materiale
       esistente, mai doppiato: l'Olio di Sabotaggio di Sal che cede al
       momento peggiore (clock Sal, state.md §3), le statue vive/Mythal
       (Fase 4 + filiera Sal→Varis), il tradimento di Halveth se non
       rimosso (Consiglio), il convoglio-riserva di Lorana, Zalkatar
       wildcard se fuggito dalla Torre (<10% pf), l'eco di Sethrax/Orbe,
       Therysol contro la cellula del Collezionista, Tempestas caster
       volante (se investito), i leoni spettrali del Ghostlord (ramo).
     - **[S3 — nuove, solo per i buchi]** (~2-4 carte): inventate SOLO dove
       né S1 né S2 coprono un momento necessario del ritmo dei 3 giorni
       (es. una carta di crisi civile Day 41), mantenendo lo stesso piglio:
       PG protagonisti nel bene e nel male, posta personale, esito ai dadi.
     L'engine deve compilare una **tabella di mappatura carta→sorgente→file
     riusato** in testa all'EVENT-DECK: se una carta S3 duplica qualcosa di
     esistente, è un errore da correggere. Rifare in chiave Rethmar gli archetipi Brindol
     (mapparli dalla copia RHoD del DM, non riprodurre testo): barricate di
     strada coi civili, **il cecchino/assassino che punta a Lady Kaal o
     Brenna** (eco di Halveth se non rimosso), la breccia da richiudere,
     la difesa del Tempio-ospedale (eco Fase 0), il duello chiamato dal
     Wyrmlord Karruk, il salvataggio del convoglio di Lorana, il set-piece
     Tyrgarun (già in C1.d — qui solo la carta), il crollo del campanile,
     i sotterranei drow riaperti (eco Sabotaggio). Eventi in più rispetto a
     Brindol = i punti dove l'assedio di 3 giorni è PIÙ grande dell'originale.
  2. **Menù di crisi (anti-dispersione)**: a ogni "campana" (2-3 per giorno)
     il DM presenta 3-4 crisi simultanee → i PG ne scelgono 1-2 (possono
     dividersi); le non scelte si risolvono **off-screen con la tabella delle
     conseguenze** (perdite, morale, -CR o +CR alle fasi successive). Nessun
     evento è obbligatorio: la pressione nasce dallo scegliere a chi non
     rispondere. È la struttura che rende la battaglia "Critical Role":
     il DM monta in croce le scene, ma quando la scena parte è **combattimento
     tattico vero** con poste personali ed esito incerto — l'epica nasce dal
     rischio reale, non dalla regia.
  3. **Ritmo dei 3 giorni**: Day 40 notte (Fase 0) = 2-3 carte infiltrazione;
     Day 41 (arrivo orda in vista, ultimi preparativi) = carte di crisi civile
     e sabotaggio interno + 1 riposo lungo scandito; Day 42 (Fasi 1-4) =
     campane serrate, riposi solo brevi, carte sempre più gravi. Tenere il
     conteggio risorse onesto (slot, pf) — la scarsità è parte del climax.
  4. **Cosa NON fare (D13)**: niente sistema armate alla Kingmaker; niente
     griglia con 200 miniature; la battaglia Hammerfist resta il precedente
     narrativo ma il suo impianto di massa NON si porta al tavolo — l'engine
     deve anzi estrarne le 3-4 scene migliori e convertirle in carte evento.
- **Accettazione**: file EVENT-DECK con ≥12 carte complete; ogni carta ≤ 1
  pagina + mappa; **ogni carta è giocabile come incontro tattico senza
  preparazione aggiuntiva** (mappa in scala + statblock/puntatore + tattiche);
  ogni carta ha i 3 esiti aperti + la conseguenza off-screen se ignorata;
  ogni PG ha ≥2 carte spotlight; **tabella carta→sorgente→file riusato
  presente, con mix ~S1:5-6 / S2:5-6 / S3:2-4 e nessun doppione di materiale
  esistente**; STRUTTURA e FASE1/FASE2-TESTO aggiornati per puntare al deck
  (le ondate diventano lo sfondo tra le campane).

---

## §4 — ORDINE DI ESECUZIONE E BUDGET (per non bruciare crediti)

Esegui **un lotto per sessione**, nell'ordine. I lotti A sono meccanici e
brevi; B/C sono generativi e vanno spezzati.

| Sessione | Task | Tipo | Dipendenze |
|---|---|---|---|
| 1 | A1 + A13 (rename globali) | find/replace + git mv | — |
| 2 | A2 + A10 (clock e Fane) | editing mirato | D6 |
| 3 | A3 + A5 + A11 (INDICE refresh) | editing mirato | sessione 2 |
| 4 | A4 + A12 (nomi PNG, deprecati) | editing mirato | — |
| 5 | A8 + A9 (link rotti, file vuoti/da fondere) | consolidamento | — |
| 6 | A6 + A7 (+D12) | editing mirato | — (D9-D12 già decise) |
| 7-11 | B1 (Rhest, 1 fase per sessione) | generativo | A1 |
| 12 | B2 (Starsong) | generativo | Q1 |
| 13 | B3 (Ghostlord) | generativo | A5 |
| 14 | B4 (Handouts) | generativo | — |
| 15 | B5 (Errata 3.5 P2/P3 + boss upscale) | verifica | — |
| 16 | B6 (tesoro/WBL) | audit+generativo | B1 |
| 17 | B7 (incontri viaggio) | generativo | — |
| 18 | C1 + C2 (assedio + morale) | generativo | A2 |
| 19 | C3 + C4 | editing | — |
| 20 | C5 + C6 | generativo | A2 (fasi Day 40-42 fissate) |
| 21-22 | **C7 (Event Deck Rethmar, 6-8 carte per sessione)** | generativo — il lotto più importante del Lotto C | C1, C5, D13; il DM tiene sottomano la sua copia RHoD Parte 4 per mappare gli archetipi eventi |

**Regole anti-spreco**: (1) passa all'engine SOLO questo file + i file del
lotto corrente + state.md §0-§3; (2) niente riletture dell'intero arco;
(3) dopo ogni lotto: `grep` di verifica del criterio di accettazione, commit,
riga di changelog in state.md se il canone è cambiato; (4) aggiorna la
checklist qui sotto.

### Checklist avanzamento

- [x] A1 · [x] A2 · [x] A3 · [x] A4 · [x] A5 · [x] A6 · [x] A7 ·
  [x] A8 · [x] A9 · [x] A10 · [x] A11 · [x] A12 · [x] A13 —
  **Lotto A completo (2026-07-02).** A8 chiuso con l'**opzione (a)
  preferita**: creati DAUTH-DM-MASTER-REFERENCE (HUB), DAUTH-CONSEGUENZE-
  ECHI-LUNGO-PERIODO e DAUTH-SUBQUEST-Thorik consolidando contenuti
  esistenti. I 5 riferimenti orfani a sotto-quest mai scritte
  (SUBQUEST-Artemis/Hella, DAY3-CITY-SIEGE) sono stati ripuntati ai
  file che portano il materiale (HUB §5 con flag [INFERRED — Lotto B]),
  **senza inventare sotto-quest nuove**. Verifica: `grep` di ogni
  `Arco-*.md` citato → **zero link rotti operativi** (restano solo i
  riferimenti del piano stesso ai deliverable futuri B4/B7/C7 e alla
  nota storica del rename RETHMAN→RETHMAR).
  **Aggiornamento (2026-07-02) — orfani sotto-quest scritti.** I 3
  riferimenti orfani sono ora **file autonomi a standard Palio**, non più
  solo ripuntati: `...DAUTH-SUBQUEST-Artemis.md` (Beriah / culto della
  Maschera), `...DAUTH-SUBQUEST-Hella.md` (boschetto morente / Spora-Madre
  di Sonjak), `...DAUTH-DAY3-CITY-SIEGE.md` (assedio Vanguard di Dauth,
  carte-crisi D13 — prototipo dell'EVENT-DECK C7). HUB §5, SUBQUEST-Thorik
  §4, INDICE e changelog di state.md allineati; nessun bonus in conflitto
  con gli hook sorgente (le sub-quest ne sono la *sorgente giocata*).
- [x] B1.1 · [x] B1.2 · [x] B1.3 · [x] B1.4 · [x] B1.5 · [x] B2 · [x] B3 ·
  [x] B4 · [x] B5 · [x] B6 · [x] B7 — **LOTTO B COMPLETO (2026-07-02).**
  **B1 (Rhest) completo (2026-07-02)**: 5 file FASE portati da scheletro
  (~1–4 KB) a standard Palio (read-aloud, viaggio a esagoni, tabella
  incontri d12, regole subacquee SRD, arena a 3 quote, sinergia artefatti
  state.md §6, conseguenze allineate a state.md §2.3 −1 drago/−2 Razorfiend,
  eco Lanikar/+VP, intel −1 CR). Statblock delegati ai file ENCOUNTER
  esistenti. CD (non DC) come da §0.7.
  **B2 (Starsong) completo (2026-07-02)**: skill challenge formale a 3 atti
  (arrivo/funerale di Lanikar/consiglio, 3 successi su 3 fallimenti, CD
  20–26), read-aloud del funerale, tabella "cosa impressiona i Tiri‑Kitor"
  per classe PG, esiti a 3 rami con numeri D9 (piena 100+20 / parziale
  ~40+6 / rifiuto 0) mappati sugli scenari ARMATE-SYNC §3, sinergia con
  l'eco Lanikar di Rhest (B1.5).
  **B3 (Ghostlord) completo (2026-07-02)**: fonte-stat unica = `PNG/Ghostlord/
  Ghostlord.md` (STATBLOCCHI declassato ad annesso subordinato, riconciliazione
  a B5); read-aloud del santuario interiore (audizione morale, scena di Hella,
  leoni = anime di Hammerfist); tabella conseguenze a lungo termine per i 3 rami
  della filatteria (restituire/vincolare/distruggere + default ostile) con
  Rethmar D7 / epilogo / hook ARC-10; scala 1,5 m/quadretto esplicitata in MAPPE.
  **B4 (Handouts) completo (2026-07-02)**: creato `Arco-Post-Hammerfist-HANDOUTS.md`
  con 6 handout stampabili in testo integrale (lettera Brenna, invito Maewen,
  mappa in pelle Tempestas, bracket Torneo, volantino Palio a 8 contrade — nota:
  il piano diceva 7, pre-espansione —, 3 carte-visione di Saraah), ognuno con
  "quando darlo". Prossimo: B5 (errata 3.5 P2/P3 + boss upscale).
  **B5 (Errata 3.5 P2/P3 + boss upscale) completo (2026-07-02)**: creato
  `ERRATA-PARTE2-3-35-Verification.md` (gemello della P1). **Boss finale
  upscalato in place**: Azarr Kul da Chierico 10/Guerriero 4 (~119 pf, CR 15)
  a **Chierico 12/Guerriero 4 (~155 pf, CR 17)** con tabella buff pre-cast
  (durate a CL 14) e 2 effetti a innesco; scena con l'Avatar resta CR 18 (CR
  non additivi). Verifiche puntuali: attacchi naturali di Regiarix (morso +29,
  secondari a −5, coda 1d8+12), taglia Piccola di Saarvith (CA 23/contatto 15,
  Lotta +8), CA contatto/colto mancanti in P2A/P2B, RI non cumulativa (Zalkatar),
  pointer PNG per Xal'thor/Sethrax. **Catch di coerenza**: rimosso "mounts
  Tyrgarun" da `azarr-kul-final-cr15.md` (contraddiceva D11 v2/A7). Prossimo: B6.
  **B6 (Tesoro/WBL) completo (2026-07-02)**: creato
  `Arco-Post-Hammerfist-TESORO-WBL-AUDIT.md`. Corretto il gap ~8× dell'INDICE
  §Loot (~50k → **~380.000 mo equivalenti** distribuiti, coerente WBL 13→16
  ±20%). Tabella tesoro per quest/incontro (stile Paizo): pesatura su Rhest
  hoard (~90k), Torre di Zalkatar (~70k), Torneo (~45k), Rethmar/bottino +
  ricompense civiche (~45k), resto sulle side-quest. Dettaglio dei due
  contenitori-chiave (hoard di Regiarix, laboratorio di Zalkatar) tutto
  SRD/DMG; plot item marcati [INFERRED]. Chiarito che i 5 artefatti legacy
  sono ricchezza d'ingresso (non colmano il delta) e che rendite/titoli di
  dominio (C6) si contano a parte. INDICE §Loot riscritto. Prossimo: B7.
  **B7 (Incontri di viaggio) completo (2026-07-02)**: creato
  `Arco-Post-Hammerfist-INCONTRI-VIAGGIO-CANNATH-VALE.md`. 4 macro-zone
  (Witchwood/Sacred Forest, Strada del Deserto/Shaar, Vale Centrale/Dauth,
  Thornwaste) × 2 finestre (Day 20-30 / 31-42, la seconda più cattiva con
  meno civili — March Clock D6). Tabelle d% con EL dichiarato (9-13) e
  **≥1/3 voci non-combat** (profughi, Sal, disertori gnoll, pattuglie da
  interrogare, emissari Ghostlord). Riusa MISSIONI-BREVI (MB-1…6) e gli
  statblock di Armate-UNITA-NUOVE (tutti verificati esistenti); echi agli
  archi esistenti (Sal, Lorana, Therysol, Collezionista, Zalkatar wildcard).
- [x] C1 · [x] C2 · [x] C3 · [x] C4 · [ ] C5 · [ ] C6 · [ ] C7 (event deck)
  **C3+C4 (sessione 19) completo (2026-07-02).** **C3**: sidebar uniforme
  "SE FALLISCONO" in coda a P1C-Rituale-SCALE, P2A-Torre-PARTE4-Boss-Zalkatar,
  P2B-PARTE3-Giorno3, P2-RHEST-FASE4, Ghostlord-TESTO (i 3 rami già presenti in
  Rhest/Ghostlord **uniformati** al formato); più la nota unica
  **§8.5 "Risorse di resurrezione nel Vale"** in DM-QUICKSTART-ARC09 (tabella
  fonti raise nel Vale — Rethmar/Ilmater-Maewen/Circolo *reincarnate*; regola
  "in 3.5 in battaglia non si resuscita"; ogni raise = debito). Nessun vicolo
  cieco: ogni fallimento produce storia (costo, non stop); Cuore di Moradin
  ribadito speso (§6). **C4**: MYTHAL-FOCUS §8 "Varianti per stato del PG" — per
  ciascuno dei 4 PG-focus 2-3 varianti che rispettano i poteri attuali (§6) e i
  rami (Orbe/4ª Porta, Anello evoluto sì/no, forma d'Avatar spesa/disponibile,
  Sacred Forest sì/no); catch di coerenza sui single-use spesi (Rubino Corona,
  Cuore di Moradin). Prossimo: C5+C6.
  **C1+C2 (sessione 18) completo (2026-07-02).** **C1**: aggiunta STRUTTURA §9
  "Cornice leggera d'assedio" — (a) VP → **il Fronte** (tracker nascosto DM) +
  check di Morale per ondata (1d20+Fronte vs CD 15/20/25); (b) 4 ruoli di comando
  PG (Comandante/Campione/Fulcro Arcano/Salvatore) con effetti quantificati; (c)
  tabella d12 eventi di battaglia per fase; (d) **set-piece Tyrgarun D11 v2** a
  scalini (hazard Fase 1 con 4 contromosse quantificate, clock aereo Fasi 2-3,
  inchiodato dal Mythal in Fase 4). Coerente col prototipo DAY3-CITY-SIEGE.
  **Fix di coerenza (residuo A7)**: rinominato statblock
  `tyrgarun-black-adult-cr13.md` → **`tyrgarun-blue-old-cr18.md`** e riscritto a
  blue Old CR 18 (profilo aereo + profilo a terra ~16-17); aggiornati i 3
  riferimenti (monster_catalog.yaml, Armate-COMPOSIZIONE-DETTAGLIATA, UNITA-NUOVE
  README). **C2**: contatore **Morale Cittadino di Rethmar 0-10** in
  `PNG/Consiglio_Rethmar/` (tabella eventi→Δ + 3 soglie: 7+ = +150 volontari/+1
  Fronte, 3- = −1 Fronte/diserzioni, 0 = resa civile), agganciato a Sedute del
  Consiglio, Riserva di Lorana e Fronte militare. Prossimo: C3+C4.
- [x] Q1 (→D9) · [x] Q2 (→D10) · [x] Q3 (→D11) · [x] Q4 (→D12) ·
  [x] Q5 (→D8) — **tutte le risposte DM acquisite 2026-07-02**

---

## §5 — GIUDIZIO SINTETICO (per il DM, non per l'engine)

**Cosa è già a livello dei migliori moduli 3.5/PF1e**: l'architettura a doppio
clock con conseguenze quantificate (migliore del RHoD originale), gli hook
personali v2 con fonti plausibili e rami morali, il Palio P2D (degno di *War
for the Crown*), il tracker armate a 5 scenari, il principio "la battaglia è
persa senza i PG" che rende ogni quest un moltiplicatore misurabile.

**Cosa la separa dall'eccellenza**: (1) l'INDICE e alcuni file P3 sono rimasti
indietro di 2 generazioni di canone (numeri, nomi, date) — è il rischio classico
dei repo multi-engine e si risolve col Lotto A; (2) Rhest è un'ossatura in mezzo
a capitoli completi; (3) l'economia del tesoro è sotto il WBL di un fattore ~8;
(4) l'assedio finale ha ottimi numeri strategici ma nessun sotto-sistema
tattico al tavolo; (5) il "quinto atto" di RHoD qui è per scelta (D8) il
rituale di evocazione dell'Avatar in Fase 2 — va potenziato perché regga quel
peso, e serve un epilogo giocato oltre i monologhi. Con i lotti A+B l'arco è
solido; con C diventa il tipo di finale che i giocatori raccontano per anni.
