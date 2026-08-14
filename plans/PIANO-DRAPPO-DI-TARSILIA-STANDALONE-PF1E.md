# PIANO — «Il Drappo di Tarsilia»: il Palio come modulo autonomo (Golarion · PF1e)

**Stato**: 🟡 in corso — Lotto 1 chiuso (impianto giocabile completo)
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
| **Si riusa** | il **sistema** del Palio (Tratta, Partiti, Morale/Onore, Mossa, Corsa) — materiale originale dell'autore — e gli **otto stemmi Golarion** già in repo |
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
| **Contrade** | otto, **rinominate da zero**, motti **scritti ex novo**, nessun titolo araldico reale | bonifiche §7.1, §7.2, §7.4 |
| **Immagini** | 8 stemmi SVG (riuso), 2 mappe generate dalla pipeline, prompt-sheet per i ritratti | il repo non genera raster: genera vettoriale e *istruzioni* per ComfyUI locale |

## 3. Lotti

### Lotto 1 — Impianto giocabile ✅ *(chiuso 2026-08-14)*

- [x] `STANDALONE-Il-Drappo-di-Tarsilia/00-HUB-E-QUICKSTART-DM.md` — hub, quickstart,
      contratto del tavolo, cosa stampare, ponte fra le tre sessioni
- [x] `CONTRADE-DI-TARSILIA.md` — le otto contrade: livree, motti nuovi, canti con
      effetti, rivalità, tabella di corrispondenza con gli stemmi SVG
- [x] `REGOLE-DELLA-CORSA-PF1E.md` — il sottosistema: Morale del Rione, Onore del
      Fantino, la Mossa, la Corsa come inseguimento PF1e, il nerbo, il cavallo scosso
- [x] `PREGEN-SEI-SCHEDE-PF1E.md` — sei schede complete (statblock, equipaggiamento,
      ufficio, obiettivo personale, come si gioca in un minuto)
- [x] `01-GIORNO-1-LA-TRATTA.md` · `02-GIORNO-2-I-PARTITI-E-LA-CENA.md` ·
      `03-GIORNO-3-LA-MOSSA-E-LA-CORSA.md` — le tre sessioni
- [x] `STATBLOCCHI-PF1E.md` — PNG, rivali, sicari, cavalli
- [x] `ALLEGATI/mappe/` — 2 mappe dal contratto JSON (piazza, stalle) + render
- [x] `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` — art direction
- [x] `IP-E-LICENZE.md` — CUP Paizo, OGL, quali bonifiche §7 questa edizione chiude
- [x] tracciatura: questo piano + INDEX + CHANGELOG

**Criterio di accettazione**: un DM che non ha mai letto la campagna RumblingStone
apre l'hub, stampa sei schede e gioca tre serate senza aprire nient'altro.

### Lotto 2 — Collaudo al tavolo ⬜ *(gated: serve una sessione vera)*

- [ ] Giocare il Giorno 1 e annotare: durata reale, punti morti, prove che nessuno
      ha usato
- [ ] Tarare i tempi (il sospetto è che il Giorno 2 sia lungo e il Giorno 1 corto)
- [ ] Ritratti: il DM passa i prompt a ComfyUI locale e carica i PNG

### Lotto 3 — Edizione pubblicabile ⬜ *(gated: decisione DM su ADR-0005)*

- [ ] Audit IP dedicato del solo standalone (il tetto WotC qui non si applica:
      va verificato che *davvero* non si applichi, riga per riga)
- [ ] Sostituzione delle figure degli stemmi che restano nel bestiario senese
      (oca, torre, bruco, istrice) — l'ultima criticità §3 aperta
- [ ] Impaginazione Homebrewery + PDF

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
