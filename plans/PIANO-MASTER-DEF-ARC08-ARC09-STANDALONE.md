# PIANO — I master DEF di ARC-08, ARC-09 e degli stand-alone

> **Cos'è**: il piano per consolidare gli archi che non hanno ancora un master
> definitivo nel formato `ARC*-DEF-*`: la Battaglia di Hammerfist (ARC-08), il
> seguito dopo la Battaglia (ARC-09), e i due stand-alone (il Drappo di
> Tarsilia, l'Abbazia della Rotta Sicura). L'ordine l'ha dato il DM il
> 2026-09-25: *«poi i DEF di ARC-08, poi ARC-09 e tutti gli stand-alone»*.
>
> **Stato**: 🟡 D1-D3 decise, A1 approvato e A2 misurato il 2026-09-27; prima di A3 va chiuso F4 di PIANO-LETTORE (ARC-07 al ciclo completo) · **Decisore**: DM ·
> **Standard**: [`rumblingstone-module-standard`](../skills/rumblingstone-module-standard/SKILL.md)
> **Gate**: ogni master fa i **sette passi del ciclo completo** di
> `rumblingstone-module-standard` (scene `### SCENA`, contratto «In scena»,
> componenti, developer, box al metro, lettore e playtester a freddo, quiz),
> [ADR-0075](adr/ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md)

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

## 1-bis · Cosa deve essere chiuso prima, fuori da questo piano (ADR-0075)

Il DM, il 2026-09-27, prima di A3: *«l'arco 07 è davvero completo anche con le
nuove regole?»*. Misurato: no. Le regole nuove sul master sono state applicate
a DEF-4 soltanto (tabella in F4 di PIANO-LETTORE). Da qui due prerequisiti, che
restano nei loro piani e qui si citano:

| Prima di | Serve | Dove sta | Perché |
|---|---|---|---|
| **A3** | ARC-07 al ciclo completo, DEF-5 per primo | PIANO-LETTORE **F4** | ARC-08 comincia dove finisce DEF-5, e il canone che A3 confronta sta nei master di ARC-07 |
| **S1** | il cancello che segnala un master senza scene | PIANO-LETTORE **F6-a** ✅ (2026-09-27) | senza, un master di ARC-08 scritto con titoli diversi da `### SCENA` passerebbe i cancelli senza essere guardato |

⚠️ **Il riposo, nei sorgenti.** Dal 2026-09-27 `validate_modules` boccia
«riposo breve/lungo» nei master DEF. Nei sorgenti di ARC-09 compare ancora
(l'event deck della battaglia finale, il Cerchio dei Treant, il Rituale, il
Torneo, i ganci): il lotto che li porta in un master scrive al suo posto quante
ore e cosa danno, con la tabella di `dnd-35-srd` (combat.md, *Rest and
recovery*). Il cancello lo ricorda da solo, al primo DEF.

**Gli altri piani, controllati lo stesso giorno.** Il ciclo è entrato dove un
lotto aperto scrive o rifinisce contenuto di gioco: PIANO-LETTORE (F4 allargato,
F6-a nuovo), MESTIERE-BANCHI (S4 su DEF-5 passa a F4; S1-S3 aspettano la
conversione di F4), INDAGINE (I5), MARCATURA (M2, solo passo 3), DRAPPO (Lotto
3). Esclusi perché i loro lotti aperti non toccano la prosa dei moduli:
REVISIONE-ARC07 (B1, i log), TRASVERSALE (artefatti e `state.md`), CICLO-DI-SESSIONE,
LEVEL-DESIGN, EDITOR-VISUALE, PIPELINE-IBRIDE e MESTIERE-CARTOGRAFO (mappe),
MISURA-EDITORIALE (misura), RIPRESA-PR, RICONCILIAZIONE-PR e PRATICHE-DI-INGEGNERIA
(infrastruttura), VENDIBILITA (non autorizzato).

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

## A1 · La divisione in master — ✅ approvata dal DM il 2026-09-27

**Le risposte del DM** alle sette domande della pagina di revisione:

| # | Domanda | Risposta |
|---|---|---|
| Q1 | ARC-08 in quattro master, uno per sessione | ✅ ok |
| Q2 | la Cerimonia delle 100 Asce entra in DEF-4 senza riscriverla | *«controlla prima e se serve la riscrivi»*: in S1 si misura contro lo standard, e si riscrive solo dove non lo regge |
| Q3 | ARC-09 in dodici master, uno per beat | ✅ sì |
| Q4 | il Torneo in due: Giorni 1-2, poi Giorno 3 e invasione | ✅ ok |
| Q5 | la Battaglia Finale in due: P2C con le Fasi 0-1, poi le Fasi 2-4 | ✅ ok |
| Q6 | il Palio consolida la prosa, il sistema di gara resta com'è | ✅ ok |
| Q7 | quante serate per la quest di Hella | *«spezzato in due se troppo lungo»*: restano i due master DEF-01 e DEF-02; le serate si misurano al tavolo |


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
| `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA` | Sessione 1 · Day ~12-16 | pregen | Guida DM §1-§3 e «PNG giocabili» (righe 103-634) più la Sessione 1 (943-1178), scontri 1A-1B, `ARC08-04-MARCIA`, `Mappe/…L1` |
| `ARC08-DEF-2-TRE-GIORNI-DI-SANGUE` | Sessione 2 · Day 16-18 | pregen | Guida DM, Sessione 2 e Giorni 1-3 (1179-1901), scontri 2A-2B, `Mappe/…L2`, `mass_combat_guide_Dm` |
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

⚠️ **La Cerimonia delle 100 Asce** era canone fissato da non riscrivere (D3 di
REVISIONE-ARC08). Il DM il 2026-09-27 (Q2): *«controlla prima e se serve la
riscrivi»*. In S1 la si misura (`misura_craft --box`, contratto «In scena»);
dove regge entra com'è, dove non regge si riscrive. Gli **eventi** della
Cerimonia (Day 21, il riconoscimento dei Custodi Eterni, l'hook di ARC-09)
restano canone: si riscrive la forma, non cosa succede.

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

## A2 · Le misure di partenza — ✅ 2026-09-27

Misurato sulle fonti di ogni master della tabella A1, con i rilevatori del
repo importati da uno script di sola lettura (`misura_craft.misura`,
`box_read_aloud`, `difetti_dei_box`, `domande_developer.analizza`). Nessuna
regex nuova. Per ARC-08 le fonti sono le fasce di righe della Guida DM e
degli scontri scritte in A1.

🐛 **Una fascia di A1 era sbagliata, e la misura l'ha trovata.** La Sessione 1
della Guida DM sta alle righe 943-1178, e DEF-1 non la prendeva. Corretto nella
tabella di A1: DEF-1 prende 103-634 e 943-1178, DEF-2 parte da 1179.

| Master | File | Righe | Congegni | Box | Read-aloud | Battute | Vie non comb. | Contingenze |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ARC08-DEF-1 | 5 | 1.748 | 9/23 | 19 | 20 | 17 | 7 | 1 |
| ARC08-DEF-2 | 4 | 2.471 | 7/23 | 19 | 19 | 19 | 3 | 3 |
| ARC08-DEF-3 | 3 | 1.024 | 7/23 | 12 | 13 | 11 | 0 | 0 |
| ARC08-DEF-4 | 5 | 2.122 | 10/23 | 32 | 35 | 44 | 0 | 5 |
| ↳ Cerimonia da sola | 1 | 208 | 6/23 | 1 | — | — | — | — |
| ARC09-DEF-01 | 5 | 1.154 | 8/23 | 4 | 8 | 32 | 0 | 4 |
| ARC09-DEF-02 | 5 | 1.886 | 7/23 | **0** | **0** | 14 | 0 | 3 |
| ARC09-DEF-03 | 13 | 1.501 | 14/23 | 8 | 18 | 11 | 4 | 6 |
| ARC09-DEF-04 | 13 | 2.619 | 10/23 | 1 | 5 | 8 | 1 | 4 |
| ARC09-DEF-05 | 9 | 2.420 | 13/23 | 7 | 9 | 25 | 1 | 5 |
| ARC09-DEF-06 | 15 | 3.095 | 11/23 | 40 | 41 | 26 | 1 | 27 |
| ARC09-DEF-07 | 8 | 1.159 | 10/23 | 8 | 8 | **0** | 5 | 11 |
| ARC09-DEF-08 | 3 | 357 | 8/23 | 2 | 2 | 2 | 4 | 4 |
| ARC09-DEF-09 | 4 | 650 | 9/23 | 2 | 6 | 6 | 1 | 17 |
| ARC09-DEF-10 | 6 | 608 | 3/23 | **0** | **0** | **0** | 0 | 2 |
| ARC09-DEF-11 | 8 | 1.488 | 9/23 | 2 | 5 | 13 | 6 | 12 |
| ARC09-DEF-12 | 10 | 2.160 | 7/23 | **0** | **0** | 15 | 0 | 7 |

Nessun box supera le 12 righe, in nessun master.

⚠️ **Gli hook gonfiano i numeri di ARC-09.** Senza gli `HOOKS-*`, la **Torre**
(DEF-03) ha zero box, zero read-aloud e zero battute, come diceva
MESTIERE-BANCHI; tutto quello che la tabella le dà viene dall'hook di Artemis.
Lo stesso per il **Torneo, Giorni 1-2** (DEF-04: zero, zero, zero) e il
**Cerchio del Treant** (DEF-01: zero box, zero read-aloud). Il Ghostlord e la
Battaglia Finale I scendono a un box ciascuno. Fra le fonti di ARC-09 i box
veri stanno nel Palio, a Rhest e negli hook.

**Otto congegni sono a zero in tutti e sedici i master**: scalare lo scontro,
PILASTRO dichiarato, chiusura su decision point, regia di round, `[HDYWTDT]`,
assorbi e rilancia, ADR interni, quarta colonna sensoriale. Sono le cose che
lo standard DEF chiede e che nessuna fonte porta: si scrivono da zero in S1-S2.

**Cosa dicono gli altri due strumenti, e cosa non possono dire.**
`copertura_scene` e la parte per scene di `domande_developer` riconoscono una
scena solo dal titolo `### SCENA`, che nessuna fonte usa: su di loro danno zero
rilievi perché non vedono scene, non perché le scene sono a posto. Il
controllo che vale sull'intero testo trova due cose:

- **nomi di abilità della 5ª edizione** in 7 master su 16, 13 rilievi:
  «Intuizione» 8, «Furtività» 3, «Percezione» 2. Il Palio, che è uno dei due banchi
  dello stile, ne ha quattro. In 3.5 sono Percepire Intenzioni, Muoversi
  Silenziosamente o Nascondersi, Osservare o Ascoltare;
- **tiri salvezza mai chiesti** su Tempra, Riflessi o Volontà in 7 master. Su
  un master parziale non è per forza un difetto; lo diventa se manca ancora a
  master scritto.

**La Cerimonia delle 100 Asce** (per la Q2 del DM): 208 righe, un solo box
read-aloud, con più di un nome proprio nuovo, e 6 congegni su 23. Sotto lo
standard di read-aloud: in S1 se ne riscrive la forma.

**Le due mappe del Torneo si completano.** `-2` è la versione estesa
(terreno, coperture, trofeo, città, fuga dei civili); la regola del fuori ring
coincide in tutti i file. L'unica differenza è la fascia di partenza dei
duellanti: colonne 16-20 nella prima, 18-22 nella seconda. Solo la seconda è
centrata sulla griglia 40×40, e in DEF-04 si tiene quella. Nessuna delle due è
una griglia (`MAPPE-CENSIMENTO`, nota 8).

## FASE 2 — Sviluppo / attuazione

Un lotto per master, nell'ordine dato dal DM. Ogni lotto è **K** per la parte
di canone e **C** per la struttura, e si chiude in un commit suo con piano,
INDEX e CHANGELOG.

**S1 · ARC-08, i master della Battaglia** `[engine: Opus · effort: xhigh · qualità: ciclo del master, passi 1-7, su ognuno dei quattro]`
Un sotto-lotto per master (S1a-S1d), nell'ordine delle sessioni. Fonti nella
tabella A1. Statblocchi inclusi dal Bestiario con `#statblocco` (ADR-0074). In
S1d la Cerimonia delle 100 Asce si misura prima (Q2 del DM) e si riscrive solo
nella forma.

**S2 · ARC-09, i master del seguito** `[engine: Opus · effort: xhigh · qualità: ciclo del master, passi 1-7, su ognuno dei dodici]`
Fonti nella tabella A1. Un sotto-lotto per master (S2a-S2l). Qui confluiscono S5
(la Torre) e S6 (la Battaglia Finale) di MESTIERE-BANCHI. I nomi di abilità
della 5ª edizione trovati in A2 si correggono nel master che li contiene.

**S3 · Il Drappo** `[engine: Opus · effort: alto · qualità: validate_standalone + ciclo del master, passi 1-2 e 4-7]` — PF1e
È già vicino allo standard. Il lotto porta il contratto «In scena» (F5 di
PIANO-LETTORE) e i quattro rilievi aperti di `domande_developer` (Riflessi e
Volontà sull'intero modulo). **Non** diventa un `ARC*-DEF-*`: resta uno
stand-alone ADR-0017.

**S4 · L'Abbazia** `[engine: Opus · effort: medio · qualità: validate_standalone + ciclo del master, passi 1, 2 e 4 come note]` — confermato dal DM (D3, 2026-09-27). Salta i passi 3 e 5-7: la prosa non cambia, e quei passi misurano la prosa
Solo forma: il contratto «In scena», e i rilievi di `domande_developer`
(l'invisibilità al corpo di guardia, Riflessi e Volontà), come note del DM e non
come prosa riscritta.

## FASE 3 — Testing / validazione

Per ogni master, prima di chiudere il lotto:

1. i sette passi del **ciclo completo** di `rumblingstone-module-standard`
   (ADR-0075). I passi 1-5 hanno un comando; i passi 6-7 (lettore e
   playtester a freddo su un modulo che la rubrica non ha visto, quiz con la
   chiave approvata dal DM) sono letture di un agente e non si saltano;
2. `validate_modules` verde, come per ogni `ARC*-DEF-*`;
3. per ARC-08, il confronto con lo stato del tavolo (A3) prima della serata.

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
3. D1-D3 sono decise, la tabella A1 è approvata e A2 è misurato
   (2026-09-27). Prima di A3 va chiuso **F4 di PIANO-LETTORE** (ARC-07 al
   ciclo del master, DEF-5 per primo). **F6-a** (il cancello che vede un master
   senza scene), che serviva prima di S1, è ✅ dal 2026-09-27. Vedi §1-bis.
