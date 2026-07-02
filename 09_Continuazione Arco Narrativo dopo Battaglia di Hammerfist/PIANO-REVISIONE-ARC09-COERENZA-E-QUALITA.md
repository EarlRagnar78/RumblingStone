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

### Decisioni di canone DA CHIEDERE AL DM (l'engine NON deve deciderle da solo)

| # | Questione | Opzioni in conflitto |
|---|---|---|
| Q1 | **Quanti elfi Tiri Kitor** arrivano a Rethmar? | +500 (state.md §2.4) vs 50 ranger + 10 gufi giganti (INDICE r.302). Proposta: 500 = popolazione totale (Starsong TESTO r.53), forza inviata = **100 ranger + 20 gufi** (via di mezzo credibile per una tribù di 500) |
| Q2 | **Quanti nani** dal Torneo di Dauth? | 300 mercenari (quasi tutti i file) vs +400 (state.md §2.4). Le **150 lance di Re Thorek** sono un flusso separato (hook Thorik/Maewen). Proposta: canonizzare **300 (Dauth) + 150 (lance Hammerfist)** e correggere state.md §2.4 in 300 |
| Q3 | **Tyrgarun**: che drago è? | "Very Old Blue CR 20 cavalcato da Azarr Kul" (INDICE r.443) vs "black adult, riserva aerea" (ARMATE-SYNC §2.1) vs assente dalla Fase 3 (STRUTTURA §6, STATBLOCCHI-EPICI). Con APL 14, un CR 20 in groppa al boss rompe il budget CR 16-18. Proposta: **blue adult CR 15 in riserva aerea, NON cavalcatura** — Azarr Kul combatte a terra con Avatar come da STRUTTURA |
| Q4 | Il debito di Tordek "presentarsi a Dauth entro 5 giorni" (state.md §5) è compatibile col torneo che inizia Day 30 (HOOKS §1.1)? Proposta: riformulare in "entro il Day 29 (vigilia delle preliminari)" |
| Q5 | Epilogo giocabile post-Rethmar (mini-Fane di Tiamat nel Shaar, stile RHoD Parte 5) — lo si vuole come ARC-10? (vedi G8) |

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

### A6. Alleati elfi e nani: numeri contraddittori
- **Problema**: vedi Q1/Q2. Elfi: +500 vs 50+10. Nani: 300 vs 400 (+150 lance
  come flusso separato in 5 file HOOKS).
- **Azione**: BLOCCATO da Q1/Q2 — chiedere al DM, poi propagare il numero scelto
  in: state.md §2.4, INDICE r.302/252/507, STRUTTURA §8, ARMATE-SYNC §2/§3,
  ESITI, STATBLOCCHI-EPICI §7.
- **Accettazione**: un solo numero per fazione in tutto il repo + changelog.

### A7. Tyrgarun: identità e ruolo incoerenti
- **Problema**: vedi Q3 (colore, età, CR 20 vs budget CR 16-18, cavalcatura sì/no).
- **Azione**: BLOCCATO da Q3 — poi correggere INDICE r.27/443, ARMATE-SYNC §2.1,
  STRUTTURA §6 e la scheda `PNG/Azarr_Kul/Azarr_Kul.md`.
- **Accettazione**: colore/età/CR/ruolo identici ovunque; Fase 3 resta CR 16-18.

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

### C1. Sotto-sistema d'assedio formalizzato (Heroes of Battle)
- Oggi le ondate di Fase 1 sono "blocchi narrativi" (STATBLOCCHI-EPICI §9).
- **Azione**: 1 pagina di regole in STRUTTURA: (a) **Victory Points** già
  esistenti → collegarli a check di **Morale** per ondata (difensori tirano
  1d20 + VP correnti vs CD ondata; fallimento = un settore cede); (b) **ruoli
  di comando PG** per round di battaglia (Comandante/Campione/Fulcro Arcano/
  Salvatore — azioni da 10 minuti con effetti quantificati, es. Thorik
  Comandante: +2 morale a un settore); (c) tabella d12 **eventi di battaglia**
  per fase (breccia, incendio, eroismo PNG, duello richiesto...). Riusa il
  precedente di Hammerfist ("meccaniche massa combattimento Hammerfist style",
  INDICE r.414) come base dichiarata.
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

### C5. Epilogo giocabile (benchmark RHoD Parte 5) — dipende da Q5
- RHoD non finisce a Brindol: il colpo finale al Fane dà chiusura. Qui il
  post-vittoria è solo narrato (monologhi ESITI).
- **Azione** (se Q5 = sì): stub di ARC-10 `ARC10-STUB-FANE-DEL-SHAAR.md`:
  3 pagine — viaggio nel Shaar, Fane rifortificato, ultimo Wyrmlord/erede di
  Kul, distruzione dell'altare di Tiamat; aggancio ai future hooks già elencati
  (INDICE §Epilogo, ESITI §8). Se Q5 = no: espandere la cerimonia-epilogo con
  una scena giocata per PG (già abbozzate in ESITI §7-8).
- **Accettazione**: la campagna ha una chiusura giocata, non solo letta.

### C6. Ricompense di dominio/titolo (benchmark Kingmaker)
- ESITI §7-8 accenna a titoli/ambasciate; nessuna meccanica.
- **Azione**: mezza pagina in ESITI: per esito A/B, cosa ottiene concretamente
  ogni PG (titolo, terra, seggio, scuola monastica di Tordek, cerchio di Hella)
  con 1 beneficio meccanico ciascuno (es. "Custode di Rethmar: ospitalità +
  10 PNG di servizio + 1.000 mo/mese di rendita") — utile per ARC-10.
- **Accettazione**: tabella esito×PG compilata.

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
| 6 | A6 + A7 | editing mirato | **risposte DM Q1-Q3** |
| 7-11 | B1 (Rhest, 1 fase per sessione) | generativo | A1 |
| 12 | B2 (Starsong) | generativo | Q1 |
| 13 | B3 (Ghostlord) | generativo | A5 |
| 14 | B4 (Handouts) | generativo | — |
| 15 | B5 (Errata 3.5 P2/P3 + boss upscale) | verifica | — |
| 16 | B6 (tesoro/WBL) | audit+generativo | B1 |
| 17 | B7 (incontri viaggio) | generativo | — |
| 18 | C1 + C2 (assedio + morale) | generativo | A2 |
| 19 | C3 + C4 | editing | — |
| 20 | C5 + C6 | generativo | **risposta DM Q5** |

**Regole anti-spreco**: (1) passa all'engine SOLO questo file + i file del
lotto corrente + state.md §0-§3; (2) niente riletture dell'intero arco;
(3) dopo ogni lotto: `grep` di verifica del criterio di accettazione, commit,
riga di changelog in state.md se il canone è cambiato; (4) aggiorna la
checklist qui sotto.

### Checklist avanzamento

- [ ] A1 · [ ] A2 · [ ] A3 · [ ] A4 · [ ] A5 · [ ] A6 (Q1/Q2) · [ ] A7 (Q3) ·
  [ ] A8 · [ ] A9 · [ ] A10 · [ ] A11 · [ ] A12 · [ ] A13
- [ ] B1.1 · [ ] B1.2 · [ ] B1.3 · [ ] B1.4 · [ ] B1.5 · [ ] B2 · [ ] B3 ·
  [ ] B4 · [ ] B5 · [ ] B6 · [ ] B7
- [ ] C1 · [ ] C2 · [ ] C3 · [ ] C4 · [ ] C5 (Q5) · [ ] C6
- [ ] Q1 · [ ] Q2 · [ ] Q3 · [ ] Q4 · [ ] Q5 — **risposte DM**

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
tattico al tavolo; (5) manca il "quinto atto" giocabile che in RHoD chiude il
cerchio. Con i lotti A+B l'arco è solido; con C diventa il tipo di finale che i
giocatori raccontano per anni.
