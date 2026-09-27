# PIANO — I master DEF di ARC-08, ARC-09 e degli stand-alone

> **Cos'è**: il piano per consolidare gli archi che non hanno ancora un master
> definitivo nel formato `ARC*-DEF-*`: la Battaglia di Hammerfist (ARC-08), il
> seguito dopo la Battaglia (ARC-09), e i due stand-alone (il Drappo di
> Tarsilia, l'Abbazia della Rotta Sicura). L'ordine l'ha dato il DM il
> 2026-09-25: *«poi i DEF di ARC-08, poi ARC-09 e tutti gli stand-alone»*.
>
> **Stato**: ⬜ aperto il 2026-09-27, niente eseguito · **Decisore**: DM ·
> **Standard**: [`rumblingstone-module-standard`](../skills/rumblingstone-module-standard/SKILL.md)
> **Gate**: ogni master nuovo passa `validate_modules`, `copertura_scene`
> (profilo severo, contratto «In scena»), `componenti --check`,
> `domande_developer --check`, e una lettura a freddo senza 🔴

---

## 0 · Cosa ho guardato prima di aprirlo (ADR-0044)

| Piano | Cosa copre | Perché non basta |
|---|---|---|
| [`PIANO-REVISIONE-ARC08`](PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA.md) e [`-ARC09`](PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md) | coerenza e qualità dei file, luglio 2026 | ✅ chiusi. Hanno sistemato i file che ci sono, non li hanno fusi in un master |
| [`PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI`](PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI.md) | i congegni di mestiere nelle parti scritte prima, onde S4-S6 su ARC-08 e ARC-09 | porta i congegni dentro i file come sono. **Dipende da una sua decisione aperta (D2)**, la stessa che decide l'ampiezza di questo piano |
| [`PIANO-LETTORE-E-PLAYTESTER`](PIANO-LETTORE-E-PLAYTESTER.md) | F5 (il contratto sugli stand-alone), F6 (i master nuovi nascono sotto il cancello) | dà i cancelli, non il consolidamento |
| [`PIANO-MARCATURA-DEGLI-INCONTRI`](PIANO-MARCATURA-DEGLI-INCONTRI.md) | la forma `**EL**: [N]` negli incontri | prerequisito del tetto EL, non del master |

Nessuno di questi fonde un arco in master. Questo piano sì.

## 1 · Cosa NON rifà

- **Non riscrive i congegni** che MESTIERE-BANCHI porta in ARC-08 e ARC-09. Se
  D2 si chiude con «rifinire», le onde S4-S6 confluiscono qui e MESTIERE-BANCHI
  le segna come portate. Se si chiude con «solo operativo», restano là e
  questo piano si ferma al consolidamento strutturale.
- **Non tocca i quattro master di ARC-07** (`DEF-1`…`DEF-5`): sono F4 di
  PIANO-LETTORE.
- **Non marca gli incontri** con `**EL**:`: è MARCATURA-DEGLI-INCONTRI. Un
  master nuovo però nasce già marcato.
- **L'Abbazia non si riscrive** (MESTIERE-BANCHI D1, 2026-09-18: *«la versione
  nell'Abbazia rimane così com'è»*). Il suo lotto qui è di sola forma, se il DM
  lo conferma (D3 sotto).

## 2 · Da che numero si parte

Misurato il 2026-09-27 con `find … -name "*.md"`, esclusi i file `DEPRECATO`:

| Arco | File | Righe | Forma di oggi |
|---|---:|---:|---|
| ARC-08 Battaglia di Hammerfist | 19 | 8.641 | `ARC08-00…16`: indice, guida DM, schede, registro perdite, marcia, esiti, ponte, cronologia, tesoro, atlante, handout, cue |
| ARC-09 dopo la Battaglia | 111 | 22.579 | `Arco-Post-Hammerfist-P1…P3-*`: una serie di beat, ognuno in TESTO, STATBLOCCHI e MAPPE, più supplementi ed errata |
| Drappo di Tarsilia (PF1e) | 22 | 5.432 | già strutturato (ADR-0017): guida, tre giorni, cassetta del DM |
| Abbazia della Rotta Sicura | 4 md | 1.419 | un modulo e due appendici, con le versioni HTML |

Una sola coppia di file vivi ha paragrafi copiati alla lettera:
`ARC08-01-GUIDA-DM` ⟷ `hammerfist_encounters-…-final`, 37 paragrafi (misura di
ADR-0074). Il master la fonde.

## FASE 1 — Audit / accertamento

**A1 · Quanti master, e dove si taglia** `[engine: Opus, sessione principale · effort: alto · qualità: il DM riconosce la divisione]` — **G**
Per ARC-08 e ARC-09 decidere quanti master DEF e con che confini, sul modello
di ARC-07 (un master per serata o per beat). Si legge l'indice di ogni arco e
`campaign/state.md`, non la prosa. Esce una tabella «master → file fonte →
serate», da far approvare al DM prima di scrivere.

**A2 · Le misure di partenza** `[engine: subagente Explore, Sonnet · effort: basso · qualità: i numeri si riproducono]` — **R**
Su ogni file fonte: `misura_craft --copertura`, `domande_developer --file`,
`copertura_scene --file --contratto`. Serve a sapere cosa manca *prima* di
fondere, così la fusione non lo copre.

**A3 · Il canone di ARC-08 contro lo stato del tavolo** `[engine: Opus · effort: xhigh · qualità: conferma del DM]` — **K**
ARC-08 comincia dove finisce DEF-5, e dipende dal carry-over B4 (Skullcrusher →
Fauci), dal Registro delle Perdite e dagli esiti di DEF-4. Si elencano i punti
in cui il testo di ARC-08 presuppone un esito che al tavolo non è ancora
successo.

## FASE 2 — Sviluppo / attuazione

Un lotto per master, nell'ordine dato dal DM. Ogni lotto è **K** per la parte
di canone e **C** per la struttura, e si chiude in un commit suo con piano,
INDEX e CHANGELOG.

**S1 · ARC-08, i master della Battaglia** `[engine: Opus · effort: xhigh · qualità: tutti i gate + lettura a freddo senza 🔴]`
Fonti: `ARC08-00…16` e `hammerfist_encounters-…-final`. Contratto «In scena» su
ogni scena, schede d'entrata, apparato generato da `componenti.py`, statblocchi
inclusi dal Bestiario con `#statblocco` (ADR-0074).

**S2 · ARC-09, i master del seguito** `[engine: Opus · effort: xhigh · qualità: come S1]`
Fonti: i beat P1-P3. È il lavoro più grande (111 file): se A1 dice più di
quattro master, si spezza in S2a, S2b…

**S3 · Il Drappo** `[engine: Opus · effort: alto · qualità: validate_standalone + contratto]` — PF1e
È già vicino allo standard. Il lotto porta il contratto «In scena» (F5 di
PIANO-LETTORE) e i quattro rilievi aperti di `domande_developer` (Riflessi e
Volontà sull'intero modulo). **Non** diventa un `ARC*-DEF-*`: resta uno
stand-alone ADR-0017.

**S4 · L'Abbazia** `[engine: Opus · effort: medio · qualità: validate_standalone]` — solo se il DM dice sì a D3
Solo forma: il contratto «In scena», e i rilievi di `domande_developer`
(l'invisibilità al corpo di guardia, Riflessi e Volontà), come note del DM e non
come prosa riscritta.

## FASE 3 — Testing / validazione

Per ogni master, prima di chiudere il lotto:

1. i gate in CI verdi: `validate_modules`, `copertura_scene --check` (profilo
   severo), `componenti --check`, `domande_developer --check`, `misura_craft
   --box` senza box oltre le 12 righe;
2. una lettura a freddo (lettore e playtester, `rumblingstone-playtest` §2-bis)
   **su un modulo che la rubrica non ha mai visto**: nessun 🔴;
3. il quiz a due agenti, con la chiave approvata dal DM, leggendo il limite
   scritto nel protocollo (le domande di storia non distinguono il modulo dal
   lettore);
4. per ARC-08, il confronto con lo stato del tavolo (A3) prima della serata.

## Decisioni aperte al DM

<!-- decisioni-dm: MASTER-DEF -->

| # | Fase | Domanda |
|---|---|---|
| D1 | A1 | **Quanti master per ARC-08 e ARC-09, e con che confini?** Proposta: uno per serata, come ARC-07. La tabella la prepara A1 |
| D2 | S1-S2 | **Si chiude qui la D2 di MESTIERE-BANCHI?** L'ordine di fare i DEF presuppone «rifinire», ma la domanda non è mai stata posta così. Proposta: sì, rifinire, e le onde S4-S6 confluiscono in questo piano |
| D3 | S4 | **L'Abbazia entra nel piano?** Il DM ha detto che non si tocca. Proposta: solo il contratto e le note del DM, niente prosa |

## Come si riparte in una chat nuova

1. `python3 scripts/fase1.py "08_La Battaglia Di Hammerfist/ARC08-00-INDICE.md"`
2. leggere questo piano e `plans/STATO-E-ORDINE-DEI-PIANI.md` §4 (le decisioni
   aperte al DM);
3. chiedere al DM D1-D3 di questo piano;
4. cominciare da A1.
