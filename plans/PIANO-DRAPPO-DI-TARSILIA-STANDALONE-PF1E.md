# PIANO — «Il Drappo di Tarsilia»: il Palio come modulo autonomo (Golarion · PF1e)

**Stato**: 🟡 in corso — Lotti 1, 2 e 5 chiusi (impianto · profondità AP · apparato d'uso e governance)
**Aperto**: 2026-08-14
**Richiesta-fonte (DM, 2026-08-14)**: *«dato il palio di Channathgate possiamo fare
una variante per sessioni di qualche ora, per 6 persone, per 3 giorni, ambientata a
Golarion per Pathfinder 1e non remastered, con 6 PG massimo con schede pregenerate e
immagini, sulla falsa riga delle avventure Paizo "We Be Goblins"? Si può gestire come
sessioni a sé stanti e svincolate dai Forgotten Realms?»*

**Risposta breve**: sì, e non è un ripiego — è la strada che
[ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) aveva già indicato
(«riambientare fuori da Forgotten Realms») e che
[ADR-0016](adr/ADR-0016-lingua-sorgente-e-edizioni.md) §2 aveva messo in coda come
*«l'unico materiale realmente pubblicabile: il sistema del Palio riambientato fuori
da Faerûn»*. La serie di stemmi Golarion (PR #100–#102) era già il primo pezzo.

---

## 1. Cosa si costruisce, e cosa NON si tocca

| | |
|---|---|
| **Si costruisce** | un modulo **autonomo**: città originale, sei PG pregenerati, tre giorni di gioco, regole PF1e, allegati propri |
| **Si riusa** | il **sistema** del Palio (Sorte, Partiti, Morale/Onore, Stacco, Corsa) — materiale originale dell'autore — e gli **otto stemmi Golarion** già in repo |
| **NON si tocca** | l'arco P2D di Channathgate: resta com'è, in 3.5, dentro la campagna. Nessun file dell'arco 09 viene modificato |
| **NON si eredita** | Faerûn, il Red Hand of Doom, i quattro PG della campagna, il Collezionista, Rethmar, la Cronaca Vivente |

Il vincolo di partenza è quello che rende il lavoro sensato: **due copie non
divergono se una non dipende dall'altra**. Il modulo standalone cita l'arco P2D
nel piano e nelle note di provenienza, e nient'altro.

## 2. Le decisioni prese (e perché)

| Decisione | Scelta | Motivo |
|---|---|---|
| **Ambientazione** | **Tarsilia**, città-stato originale nel **Regno dei Fiumi**, sul Sellen | il Regno dei Fiumi è canone Paizo *fatto apposta* per ospitare staterelli inventati (le Sei Libertà). Città originale = zero canone Paizo da rispettare, aggancio geografico plausibile |
| **Sistema** | **PF1e (non remastered)**, Core Rulebook | è la richiesta; il Core basta e riduce il rischio di regole rese male |
| **Livello / party** | **6 PG di 3°**, 20 punti acquisto | sei uffici della contrada = sei schede; il 3° dà risorse per intrigo *e* combattimento |
| **Durata** | **3 sessioni da 3–4 ore**, una per giornata di corsa | la richiesta; la struttura del Palio è già a giornate |
| **Avanzamento** | **pietre miliari** (4° a fine Giorno 2) | con la traccia media servirebbero ~24.000 px totali: un modulo d'intrigo non li produce e non deve provarci |
| **Nome dell'evento** | «il **Drappo**», non «il Palio di X» | bonifica §7.6 del rapporto IP: *palio* resta nome comune, l'identità senese no |
| **Contrade** | otto, **nomi senesi** (decisione DM 2026-08-15: *«poi bonificheremo anche quelli»*), motti **scritti ex novo**, nessun titolo araldico reale | §7.2 e §7.4 chiuse, **§7.1 sospesa** → Lotto 4 |
| **Immagini** | 8 stemmi SVG (riuso) · 2 mappe tattiche dalla pipeline · **mappa città, il Drappo e 6 ritratti** da `build_tavole.py` · prompt-sheet per l'edizione raster | il repo non genera raster: genera **vettoriale** e *istruzioni* per ComfyUI locale |

## 3. Lotti

### Lotto 1 — Impianto giocabile ✅ *(chiuso 2026-08-14)*

- [x] `STANDALONE-Il-Drappo-di-Tarsilia/00-HUB-E-QUICKSTART-DM.md` — hub, quickstart,
      contratto del tavolo, cosa stampare, ponte fra le tre sessioni
- [x] `CONTRADE-DI-TARSILIA.md` — le otto contrade: livree, motti nuovi, canti con
      effetti, rivalità, tabella di corrispondenza con gli stemmi SVG
- [x] `REGOLE-DELLA-CORSA-PF1E.md` — il sottosistema: Morale del Rione, Onore del
      Fantino, lo Stacco, la Corsa a nove tratti, lo scudiscio, il cavallo scosso
- [x] `PREGEN-SEI-SCHEDE-PF1E.md` — sei schede complete (statblock, equipaggiamento,
      ufficio, obiettivo personale, come si gioca in un minuto)
- [x] `01-GIORNO-1-LA-SORTE.md` · `02-GIORNO-2-I-PARTITI-E-LA-CENA.md` ·
      `03-GIORNO-3-LO-STACCO-E-LA-CORSA.md` — le tre sessioni
- [x] `STATBLOCCHI-PF1E.md` — PNG, rivali, sicari, cavalli
- [x] `ALLEGATI/mappe/` — 2 mappe dal contratto JSON (piazza, stalle) + render
- [x] `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` — art direction
- [x] `IP-E-LICENZE.md` — CUP Paizo, OGL, quali bonifiche §7 questa edizione chiude
- [x] tracciatura: questo piano + INDEX + CHANGELOG

**Criterio di accettazione**: un DM che non ha mai letto la campagna RumblingStone
apre l'hub, stampa sei schede e gioca tre serate senza aprire nient'altro.

### Lotto 2 — Profondità da modulo AP ✅ *(chiuso 2026-08-15)*

Nato dall'audit del DM: *«ci sono eventi per i personaggi? come entrano nelle
contrade? ci sono osterie e botteghe? un master ha tutto sotto controllo o ha bisogno
di un'AI? c'è stata una sessione alfa di playtest?»* — sei «no» onesti, e questo lotto
li chiude.

- [x] **Nomi senesi ripristinati** su decisione DM (Oca, Torre, Bruco, Istrice, Drago,
      Civetta, Leocorno, Onda) con gli scudi Golarion; nota IP riscritta **onesta**:
      6 bonifiche su 8 chiuse, 1 sospesa, 1 chiusa altrove
- [x] `04-LUOGHI-E-INTRIGO.md` — quindici luoghi giocabili, il mercato delle
      informazioni della Civetta, le dicerie (1d6), tre luoghi che non servono a niente
- [x] `05-INIZIAZIONE-E-EVENTI-PG.md` — come si entra in una contrada, **il rito
      d'Investitura** come scena d'apertura, **diciotto eventi personali** (3 per PG)
      con griglia di controllo
- [x] `06-VILLAIN-E-AGENDE.md` — agende **ora per ora** di Vesca, Sfregio, Salle e
      Attu; il giro del mondo se i PG stanno fermi; le contromosse; **incontri
      scalabili 4/5/6/7 giocatori** e la variante di 5° livello
- [x] `07-GUIDA-DM-PASSO-PASSO.md` — la regia: 45 minuti di preparazione, le tre
      serate minuto per minuto, otto rilanci, le voci dei PNG, le sei cose da non fare
- [x] `FASCICOLO-SCHEDE-GIOCATORE.md` — sei background in prima persona + **matrice
      dei legami 6×6**
- [x] `ALLEGATI/tavole/build_tavole.py` — mappa della città, il Drappo, sei ritratti,
      tutti vettoriali e rigenerabili
- [x] `PLAYTEST-ALFA.md` — audit meccanico (18 rilievi) + dry-run cronometrato delle
      tre serate + **nove correzioni applicate al modulo**
- [x] `homebrew/` — **tre booklet** (DM, Giocatori, Fascicolo) in HTML pergamena +
      sorgente Homebrewery + **22 PDF A4** esportati

**Criterio di accettazione**: un DM che non ha mai letto il modulo apre
`07-GUIDA-DM-PASSO-PASSO.md`, spende quarantacinque minuti, e gioca tre serate senza
inventare niente di strutturale.

### Lotto 5 — Apparato d'uso, collaudo e governance ✅ *(chiuso 2026-08-15)*

Nato dalla domanda del DM *«cosa manca davvero perché sia memorabile per i giocatori e
bello da masterizzare?»* e dalla ricerca che ne è uscita
([`RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE`](RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md)).
La risposta: non mancava contenuto, mancava **l'apparato d'uso**.

- [x] `08-CASSETTA-DEL-DM.md` — foglio del cast (28 PNG con il tic vocale), guida
      alla **pronuncia**, indice dei **15 read-aloud**, inserto per lo schermo, i
      **suoni**, il **momento da fotografare**, accessibilità
- [x] `ALLEGATI/handout/` — **quattro prop stampabili**: il contratto di Vesca (piegato
      in tre, che i giocatori possono non aprire mai), la pagina del registro dei morti
      con i nove nomi, la ricevuta `C·S·M`, il decreto affisso
- [x] `STATO-DEL-MODULO.md` — la memoria fra le tre serate: contatori, patti scritti,
      sette scelte che cambiano il finale, **Echo Ledger**, conteggio dello spotlight
- [x] `PLAYTEST-SCHEDA-FEEDBACK.md` — scheda giocatore (le tre domande che misurano
      davvero), debrief del DM con **due metriche numeriche**, ciclo alfa→beta→collaudato
- [x] **skill nuova** `rumblingstone-playtest` — le tre passate, come si legge il
      feedback, come si scrive una correzione. **Vale anche per la campagna**
- [x] **script nuovo** `scripts/validate_standalone.py` — gate CI per i moduli
      `STANDALONE-*`: file obbligatori, riferimenti incrociati, schede, termini 5e,
      read-aloud minimi, contatori. Registrato nel manifest, in CI
- [x] `rumblingstone-module-standard` §15-16 — l'apparato d'uso e i prop entrano
      nella checklist
- [x] **[ADR-0017](adr/ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md)** — i
      moduli autoconclusivi sono una classe a sé: cosa non possono fare, cosa devono avere
- [x] **[ADR-0018](adr/ADR-0018-apparato-uso-obbligatorio.md)** — l'apparato d'uso è
      parte del contenuto, non un extra. Vale per il modulo **e** per la campagna
- [x] `ALLEGATI/mappe/uvtt/` — le due mappe esportate per Foundry/Roll20

**Criterio di accettazione**: il debrief del DM misura **zero improvvisazioni
strutturali** e **meno di cinque ricerche sopra i trenta secondi** a serata. Si verifica
al Lotto 3, non prima.

### Lotto 3 — Collaudo al tavolo ⬜ *(gated: serve una sessione vera)*

- [ ] Giocare il Giorno 1 e annotare durata reale, punti morti, prove mai usate
- [ ] Rispondere alle sei domande aperte di `PLAYTEST-ALFA.md` §5
- [ ] Ritratti raster: il DM passa i prompt a ComfyUI locale
- [ ] Aggiungere il §6 al playtest → il modulo passa da **alfa** a **beta**

### Lotto 4 — Edizione pubblicabile ⬜ *(gated: decisione DM su ADR-0005)*

- [ ] Rinominare le contrade (bonifica §7.1, oggi **sospesa per scelta del DM**)
- [ ] Sostituire almeno quattro figure su otto negli stemmi
- [ ] Rigenerare i cartigli degli scudi coi motti nuovi
- [ ] Audit IP dedicato del solo standalone

### Lotto 6 — Edizione illustrata ⬜ *(pronto a partire: il capitolato è scritto)*

Il modulo è completo come **testo** e come **impaginazione**; non è ancora un **libro
illustrato**. Il divario è misurato e il capitolato d'appalto sta in
`STANDALONE-Il-Drappo-di-Tarsilia/PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`, che
contiene anche il prompt autosufficiente da passare a una sessione nuova.

- [x] Inventario di cosa esiste, e i sei divari verso il livello Paizo/WotC (§1-§2)
- [x] Prompt d'appalto con vincoli IP, strumenti del repo, criteri di accettazione (§3)
- [ ] **[1]** Illustrazioni raster: 6 ritratti + 3 tavole + il Drappo, e i prompt
      mancanti per i cinque PNG che meritano un ritratto
- [ ] **[2]** Tipografia OFL embedded — ⚠️ tocca `build_booklet_html.py`, che impagina
      **tutti** i booklet del repo: serve un ADR, o un tema opt-in da manifest
- [ ] **[3]** `tarsilia-la-ruota-giocatori.json`: la mappa senza token, hazard e note
- [ ] **[4]** PDF unico con segnalibri (estendendo `export_booklet_pdf.py`)
- [ ] **[5]** Carte da tavolo: otto segnaposto contrada + ordine di corsa, estendendo
      `ALLEGATI/tavole/build_tavole.py`
- [ ] **[6]** Frontespizio vero

**Criterio di accettazione**: i quattro booklet si rigenerano da zero, ogni immagine
ha la sua riga in `PROVENIENZA.txt`, e nessun file della campagna risulta modificato.

## 4. Engine e impegno per fase (regola DM 2026-07-22)

| Fase | Engine | Impegno | Dieta di contesto |
|---|---|---|---|
| Decisioni di ambientazione, IP, struttura d'arco | Opus | alto | ADR-0005/0016, rapporto IP §3/§7 |
| Redazione sessioni, statblock, tabelle | Sonnet | medio | solo il file del giorno + contrade + regole corsa |
| Mappe JSON, render, validazione | script deterministici | basso | `compile_map_json.py`, `render_map_svg.py` |
| Passata di lingua sui read-aloud | Opus | alto | `italiano-nativo.md`, `read-aloud-adulti.md` |

## 5. Rischi noti

| Rischio | Mitigazione |
|---|---|
| **Deriva fra le due edizioni** (Channathgate 3.5 ↔ Tarsilia PF1e) | non c'è dipendenza: l'unico asset condiviso sono gli stemmi, che restano **generati** dalla loro pipeline e citati per percorso relativo, mai copiati |
| **Regole PF1e rese male** su classi fuori Core | il modulo usa **solo il Core Rulebook**. Ogni deroga è marcata `[INFERRED — needs DM confirmation]` |
| **Sei giocatori, tre ore**: si arriva a metà giornata | ogni sessione ha una **linea di taglio** dichiarata («se sono le 23, salta a…») |
| **Il modulo diventa "il Palio ma peggio"** | i sei uffici della contrada sono i sei PG: qui la dirigenza *è* il party, non un ruolo aggiunto |

## 6. Provenienza

Sistema e impianto derivano da `09_Continuazione Arco Narrativo dopo Battaglia di
Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-*.md` (materiale originale dell'autore).
Le bonifiche applicate sono quelle del §7 di
`...P2D-PALIO-VERIFICA-LEGALE-IP.md`; il dettaglio di quali sono chiuse e quali
restano aperte sta in `STANDALONE-Il-Drappo-di-Tarsilia/IP-E-LICENZE.md`.
