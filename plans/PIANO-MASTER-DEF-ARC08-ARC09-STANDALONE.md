# PIANO — I master DEF di ARC-08, ARC-09 e degli stand-alone

> **Cos'è**: il piano per consolidare gli archi che non hanno ancora un master
> definitivo nel formato `ARC*-DEF-*`: la Battaglia di Hammerfist (ARC-08), il
> seguito dopo la Battaglia (ARC-09), e i due stand-alone (il Drappo di
> Tarsilia, l'Abbazia della Rotta Sicura). L'ordine l'ha dato il DM il
> 2026-09-25: *«poi i DEF di ARC-08, poi ARC-09 e tutti gli stand-alone»*.
>
> **Stato**: 🟡 D1-D3 decise il 2026-09-27; A1 scritto come proposta, attende l'OK del DM · **Decisore**: DM ·
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

- **I congegni di MESTIERE-BANCHI su ARC-08 e ARC-09 si fanno qui, dentro i
  master** (D2 decisa: rifinire). Confluiscono **S5** (la Torre parla) e **S6**
  (i read-aloud della Battaglia Finale). ⚠️ **S4 no**: nonostante la dicitura
  «S4-S6» usata finora, S4 sono i read-aloud di ARC07-DEF-4 e DEF-5, e ARC-07
  qui non si tocca. Resta a MESTIERE-BANCHI. La sidebar «Scalare lo scontro»
  (S1) è obbligatoria dello standard, quindi i master nascono con lei: S1 si
  chiude per ARC-08/09 quando i master esistono.
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

## A1 · La divisione in master — proposta del 2026-09-27, attende l'OK del DM

Costruita dagli indici e dalle intestazioni dei file, senza leggere la prosa:
`ARC08-00-INDICE` §2-§3, `ARC08-12-CRONOLOGIA`, i titoli di `ARC08-01-GUIDA-DM`
e di `hammerfist_encounters-…-final`, e per ARC-09 `INDICE-GENERALE-COMPLETO-CAMPAGNA`
con le sue durate. Le righe sono contate con `wc -l` sui file fonte.

### ARC-08 · quattro master, uno per sessione

⚠️ **Il taglio proposto nelle domande era sbagliato, e le fonti lo correggono.**
Avevo detto «DEF-3 il Giorno 3 dei pregen, DEF-4 il finale dei PG col ponte».
Ma la cronologia (§2) mette il passaggio di testimone **dentro** la Sessione 3:
l'incontro 3A lo giocano i pregen, il 3B i Rumbling Stones. Tagliare lì vorrebbe
dire chiudere un master a metà serata. I master restano quattro, come deciso, e
si tagliano sulle sessioni che la guida e gli scontri già usano.

| Master | Serata | Chi gioca | Fonti |
|---|---|---|---|
| `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA` | Sessione 1 · Day ~12-16 | pregen | Guida DM §1-§3 e «PNG giocabili» (righe 103-634), scontri 1A-1B, `ARC08-04-MARCIA`, `Mappe/…L1` |
| `ARC08-DEF-2-TRE-GIORNI-DI-SANGUE` | Sessione 2 · Day 16-18 | pregen | Guida DM «Giorno 1-3» (1180-1901), scontri 2A-2B, `Mappe/…L2`, `mass_combat_guide_Dm` |
| `ARC08-DEF-3-DALLE-PROFONDITA` | Sessione 3 · Day 18-19 | pregen → PG | Guida DM «Il Ritorno degli Eroi» (1902-2447), scontri 3A-3B, `ARC08-11-PONTE-ARRIVO`, `Mappe/…L3` (Mappa 5) |
| `ARC08-DEF-4-TEMPESTA-E-VITTORIA` | Sessione 4 · Day 19-21 | PG | Guida DM «Sessione 4» (2448-3007), scontro 4A ed epilogo, `ARC08-10-ESITI`, `Cerimonia-delle-100-Asce`, `Mappe/…L3` |

**Materiale comune dell'arco**, che resta nei suoi file e i master richiamano:
`ARC08-02` schede e regolamento di massa, `ARC08-03` registro delle perdite,
`ARC08-12` cronologia, `ARC08-13` tesoro, `ARC08-14` atlante, `ARC08-15`
handout, `ARC08-16` cue, e gli eserciti della Guida DM (righe 635-942). Gli
`APPARATO-ARC08-DEF-*` li genera `componenti.py` (ADR-0074), non si scrivono.

**Fuori dai master**: `ARC08-90…93` (deprecati), i due `ERRATA-ARC08-*` (si
verifica che siano applicati e basta), `combat_prompts_guide` (prompt d'immagine,
casa in `campaign/ai-media-prompts/`), lo stub `PIANO-REVISIONE-ARC08`.

⚠️ **La Cerimonia delle 100 Asce** è canone fissato da non riscrivere (D3 di
REVISIONE-ARC08). Entra in DEF-4 come **inclusione**, non come prosa rifatta:
la regia e i read-aloud nuovi le stanno intorno.

### ARC-09 · dodici master, uno per beat

Le durate sono quelle dichiarate da `INDICE-GENERALE`; dove l'indice non ne
dichiara una, lo scrivo.

| Master | Beat | Serate (INDICE) | File · righe | Fonti principali |
|---|---|---|---:|---|
| `ARC09-DEF-01-CERCHIO-DEL-TREANT` | P1A-P1B · Hella | non dichiarate | 4 · 919 | P1A, P1B (testo, mappe, Foresta in fiamme), `HOOKS-Hella` |
| `ARC09-DEF-02-IL-RITUALE` | P1C · Hella | non dichiarate | 7 · 2.381 | P1C (testo, fight), `SUPPLEMENTO-P1C-*`, `P1-MAPPE` |
| `ARC09-DEF-03-TORRE-INVISIBILE` | P2A · Artemis | 2-3 | 12 · 1.182 | le quattro parti con mappe e statblocchi, `HOOKS-Artemis` |
| `ARC09-DEF-04-TORNEO-GIORNI-1-2` | P2B · Tordek | 2-3 in tutto | ~11 · ~2.400 | PARTE1, PARTE2, Otto Porte e Orbe, cheat sheet, `HOOKS-Tordek` |
| `ARC09-DEF-05-TORNEO-FINALE-E-INVASIONE` | P2B · Tordek | *(stesse)* | ~10 · ~2.400 | PARTE3, DAY3-CITY-SIEGE, le tre subquest, conseguenze ed echi |
| `ARC09-DEF-06-PALIO-DI-CHANNATHGATE` | P2D | 3-4 | 15 · 3.066 | P2D, allegati, booklet in `homebrew/` |
| `ARC09-DEF-07-RHEST` | Rhest | 2-3 | 8 · 1.144 | P2-RHEST fasi 1-4, nido, esiti |
| `ARC09-DEF-08-STARSONG-HILL` | P3 · alleanza | 1-2 | 3 · 352 | Starsong testo, mappe, statblocchi |
| `ARC09-DEF-09-GHOSTLORD` | P3 · alleanza | 2 | 3 · 412 | Ghostlord testo, mappe, statblocchi, `HOOKS-Ghostlord` |
| `ARC09-DEF-10-SABOTAGGIO-E-MISSIONI` | P3 · secondarie | 1 per missione | 6 · 597 | Sabotaggio (con Upscale CR12), Missioni brevi |
| `ARC09-DEF-11-BATTAGLIA-FINALE-I` | P2C + P3 · Fasi 0-1 | 1 (P2C) + 4-6 in tutto | ~7 · ~1.550 | **P2C Salvatore** come apertura (la strada per Rethmar), Rethmar struttura, Armate sync, Fase 0 e 1, `HOOKS-Thorik` |
| `ARC09-DEF-12-BATTAGLIA-FINALE-II` | P3 · Fasi 2-4 | *(stesse)* | ~10 · ~1.800 | Fasi 2-4, Mythal e scena eroica, event deck, statblocchi epici, esiti |

La colonna «File · righe» conta i file del beat, senza gli `HOOKS-*` (fra 194 e 294 righe l'uno) e senza la bozza deprecata del Torneo. Le righe con `~` sono stime: la divisione file per file dei due beat spezzati
(Torneo, Battaglia Finale) la fa A2, perché dipende da cosa c'è dentro i file
comuni come `STATBLOCCHI-COMPLETO` o `DM-MASTER-REFERENCE`.

**Materiale comune dell'arco**: `HOOKS-INTEGRATION-MASTER` (la cronologia fine
§1.1), `INCONTRI-VIAGGIO-CANNATH-VALE`, `TESORO-WBL-AUDIT`, `HANDOUTS`,
`INDICE-GENERALE`, `ESPANSIONE NARRATIVA`.

**Fuori dai master**: `inizio.md`, `Quest 1 – Druida Hellas…` e
`P2B-Torneo-Tordek-PARTE1-to-Be_integrated` (deprecati dal loro stesso
banner), i due `ERRATA-*` (da verificare applicati).

### Cosa ho trovato guardando, e va deciso prima di S2

1. 🐛 `P2B-Torneo-MAPPE-COMPLETO.md` (88 righe) e `…-COMPLETO-2.md` (240)
   hanno lo stesso titolo e **differiscono in 304 righe di diff**. Una delle
   due è una versione vecchia, o sono complementari: lo dice A2 leggendole.
2. **Il Palio ha già un booklet** (`homebrew/PALIO-BOOKLET.*`) e condivide il
   sistema di gara col Drappo. Il master DEF-07 non può cambiare le regole
   della corsa senza toccare lo stand-alone: si consolida la prosa, il
   sistema resta com'è.
3. **P2C entra in `ARC09-DEF-11`, non in Rhest** (DM, 2026-09-27: *«se è
   integrato col resto ci entra, altrimenti rimane un master a parte»*).
   Integrato lo è, ma con Rethmar: Sal attiva il Circolo delle Statue nella
   Fase 4, il suo olio è la carta 4 dell'event deck, il suo clock sta in
   `state.md` §3, e la scena ha una tabella «Conseguenze per Rethmar». Con
   Rhest non ha legami: l'unico «Salvatore» nei file di Rhest è lo stile di
   R.A. Salvatore. Apre il master come la strada per Rethmar (Day 28-32),
   prima della fase politica al Consiglio (Day 30-35).
4. **I master sono dodici** perché Torneo e Battaglia Finale si tagliano in due
   e P2C entra nella Battaglia Finale. Un master sopra le 2.500
   righe fonte, rifinito nello stile, supera quello che DEF-1 di ARC-07 regge
   al tavolo (2.277 righe).

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

**S4 · L'Abbazia** `[engine: Opus · effort: medio · qualità: validate_standalone]` — confermato dal DM (D3, 2026-09-27)
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
| ~~D1~~ | A1 | ✅ **Decisa il 2026-09-27.** ARC-08: **quattro master**; ARC-09: **uno per beat**, circa dodici. Le fonti hanno spostato il taglio di ARC-08 rispetto alla proposta (il passaggio pregen → PG cade a metà della Sessione 3, non fra due master): la tabella in «A1» taglia per sessione, e attende l'OK |
| ~~D2~~ | S1-S2 | ✅ **Decisa il 2026-09-27: rifinire.** I master nascono completi di read-aloud, battute, contingenze e vie non combattive. Chiude anche la D2 di MESTIERE-BANCHI: confluiscono qui S5 e S6. S4 resta là perché riguarda ARC-07 (vedi §1) |
| ~~D3~~ | S4 | ✅ **Decisa il 2026-09-27: sì, solo forma.** Il contratto «In scena» e i rilievi di `domande_developer` come note del DM; nessuna riga di prosa cambiata, coerente con la D1 di MESTIERE-BANCHI |

## Come si riparte in una chat nuova

1. `python3 scripts/fase1.py "08_La Battaglia Di Hammerfist/ARC08-00-INDICE.md"`
2. leggere questo piano e `plans/STATO-E-ORDINE-DEI-PIANI.md` §4 (le decisioni
   aperte al DM);
3. D1-D3 sono decise (2026-09-27). Se il DM ha approvato la tabella «A1»,
   si prosegue con A2 sui file fonte della tabella; se no, si corregge la
   tabella prima di tutto il resto.
