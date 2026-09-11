# PIANO — La ripresa delle quattro PR abbandonate

> **Stato**: 🔵 **approvato dal DM, non ancora eseguito** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«R8 ok, in un'altra chat; qui fai il
> piano completo con tutte le fasi, che poi si mergia»*.
> **Esecuzione**: in sessioni dedicate, **una fase alla volta**. Questo documento
> è il contratto: chi apre quella sessione legge qui cosa fare e come si verifica.

## Che cos'è, e che cosa non è

Quattro PR aperte contengono lavoro **valido e non superato**: nessuno le ha
riprese, ma il contenuto è ancora l'unico che quei problemi abbia.
`PIANO-RICONCILIAZIONE-PR-APERTE` le ha giudicate una per una, **verificandole
sul codice di oggi** invece di leggerne il corpo. Questo piano dice **in che
ordine** e **con che criterio** si portano dentro.

**Non è** un piano per mergiare quattro branch. Tre di quelle PR hanno una base
vecchia di mesi, e in due casi il valore sta nel **contenuto**, non nei commit.
La domanda operativa non è «si mergia?» ma **«cosa di questo vale, e come lo
porto su `main` in modo verificabile?»** — e la risposta cambia per ognuna.

**Ordine approvato dal DM**: **#63 → #52 → #106 → #99**. Non è cronologico né per
dimensione: è per **rapporto fra ciò che sblocca e ciò che rischia**.

| | PR | Cosa sblocca | Rischio | Costo misurato |
|---|---|---|---|---|
| F0 | — | ✅ **chiusa il 2026-09-04**: `⛰` è un muro, e nessun master esce dal controllo | — | ADR-0043 |
| F1 | **#63** | 14 griglie tattiche che al tavolo mancano | basso | contenuto pronto, SVG **già byte-identici** |
| F2 | **#52** | l'overlay `@` su master scritti a mano | basso | **una rinominazione** |
| F3 | **#106** | catena raster riproducibile + Blender | medio | serve la **GPU del DM** per l'ultimo passo |
| F4 | **#99** | i dati di campagna come dati | **alto** | 88 file, tocca il canone |

---

## FASE 0 — Audit e prerequisiti

Da fare **una volta**, prima di F1, e vale per tutte e quattro.

### 0.1 · Quello che è già misurato, e non va rifatto

| Fatto | Come è stato verificato |
|---|---|
| Gli SVG di #63 si rigenerano **byte-identici** con lo script di oggi | rigenerato il master L3 dalla PR con `render_map_svg.py` corrente e confrontato byte a byte: 5 su 5 uguali, nonostante **222 commit** e un rifacimento del renderer |
| Su `main` i tre master Ultra-Clear hanno **un `map01` ciascuno** | `ls` di `08_…/Mappe/rendered/`: 3 mappe su 17 |
| La **3Y Ponte Sospeso** non ha griglia in tutto il repo | `grep -rn "3Y"`: compare solo nell'atlante e nel `Lotto-3` deprecato |
| #63 cancella 7 SVG di master che **tiene** | i master `Lotto-*` della PR generano ancora 7 mappe: verificato rigenerandoli |
| `validate_maps` **non se ne accorge** | rende solo i markdown con almeno un SVG committato: togliendoli tutti, il master esce dal controllo |
| 2 SVG su 3 di #52 sono **byte-identici**; il terzo cambia **solo di nome** | rigenerati e confrontati: `…grid-6553-scal` → `…grid-65-53-sca`, contenuto identico |
| `comfyui_batch.py` e `render_map_blender.py` **non esistono** su `main` | `ls scripts/` |
| Su `main` non c'è **nessuna** direttiva `@` sulle due mappe di #52, né la scena «Foresta in Fiamme» | `grep -n "@compass\|@path\|@zone\|@mark"` |

### 0.2 · Il prerequisito ✅ CHIUSO il 2026-09-04, insieme al bug di `⛰`

Il DM ha messo `⛰` in cima alla coda — *«aprilo assolutamente come bug da fixare
prima di tutti»* — e i due difetti sono usciti insieme perché sono la stessa
famiglia: **cose che il codice dava per buone senza che nessuno le contasse**.
Entrambi chiusi da
[ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md).

**`⛰` non è un muro nell'export** — 2.423 celle in 21 file. La `Hammerfist-L1`
ha 338 celle di montagna e produceva **8 segmenti**: tutta la catena invisibile
al VTT. Adesso **20**.

**Il punto cieco di `validate_maps`** — rendeva solo i markdown con almeno un SVG
committato, quindi cancellarli tutti faceva **sparire il master dal controllo**.
Adesso un master che genera mappe e non ha nessun SVG è un **errore**, salvo che
si dichiari nel proprio testo con
`<!-- validate_maps: non-renderizzato — motivo -->`.

🔎 **Il gate ha trovato due casi già in `main`** appena acceso: due master di
ARC-09 con quattro mappe mai renderizzate. Renderizzate: **31 SVG / 17 master**
(erano 27 e 15).

⚠️ **Cosa cambia per F1.** La #63 **non può più** cancellare i sette SVG dei
master `Lotto-*` in silenzio: o si rigenerano, o quei master si archiviano, o si
dichiarano. La decisione D1 resta, ma adesso è **forzata dalla CI** invece che
affidata a chi legge il diff.

### 0.3 · Il vincolo che si applica a tutte

- **Nessuna PR si mergia per il numero.** Se il contenuto vale, entra; se non
  vale, la PR si chiude con la motivazione scritta. Il conteggio delle PR aperte
  non è un obiettivo.
- **Ogni fase è un commit che passa tutti i gate**, con piano + `INDEX` +
  `CHANGELOG` nello stesso commit (regola d'oro).
- **La base è vecchia: si porta il contenuto, non i commit**, salvo dove il
  branch si rebasa pulito. In entrambi i casi il criterio di accettazione è che
  gli artefatti si **rigenerino** dal sorgente, non che il diff applichi.

---

## FASE 1 — #63: le 14 griglie tattiche di Hammerfist

> **Taglio dei lotti** (ADR-0045). La fase mescola due classi e si divide:
>
> | | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|---|
> | **1a** ✅ | **D1**: archiviare i `Lotto-*` o tenerne gli SVG | **G** giudizio | `[Opus 5, sessione principale · alto · il DM conferma la scelta]` — **chiuso 2026-09-05: archiviazione** |
> | **1b** ✅ | portare i tre master markdown e i quattro file di puntamento | **M** meccanico | `[inline · basso · i link risolvono, `validate_modules` verde]` — **chiuso 2026-09-05** |
> | **1c** ✅ | risolvere i conflitti sui file di puntamento (3 commit di drift) | **C** costruzione | `[Sonnet 5 · medio · nessun riferimento perso rispetto a prima]` — **chiuso 2026-09-05: un solo conflitto vero** |
> | **1d** ✅ | rigenerare gli SVG da zero | **M** meccanico | `[inline · basso · byte-identici a quelli della PR — già provato su L3]` — **chiuso 2026-09-05: 11 SVG, 7 byte-identici e 4 diversi solo nella legenda/nel nome** |
>
> ⚠️ **1a viene prima di tutto**: dopo ADR-0043 la CI **forza** quella decisione,
> quindi 1b non parte finché 1a non è presa.

**Perché per prima.** È l'unica delle quattro che si sente **al tavolo**: oggi
un DM che gioca ARC-08 ha tre mappe su diciassette, e l'incontro del Ponte
Sospeso non ha una griglia da nessuna parte. Il contenuto è pronto e verificato,
e il costo è quasi zero.

### 1.1 · Cosa entra

| Artefatto | Cosa |
|---|---|
| `Hammerfist-L1-REVISED-Ultra-Clear.md` | da 1 a **3** mappe (torrione di vedetta, sentiero nascosto, campo della Mano Rossa) |
| `Hammerfist-L2-REVISED-Ultra-Clear.md` | da 1 a **3** (fortezza top-down, disposizione Giorno 1, attacco del drago) |
| `Hammerfist-L3-REVISED-Ultra-Clear.md` | da 1 a **5** (cortile sfondato, **3Y ponte sospeso**, 3Z incrocio silenzioso, cuore della montagna, battaglia finale terrestre) |
| `ARC08-00-INDICE`, `ARC08-01-GUIDA-DM`, `ARC08-04-MARCIA`, `Atlante` | puntamenti riallineati alle mappe nuove |

### 1.2 · Cosa NON entra così com'è

🐛 **La cancellazione dei 7 SVG dei master `Lotto-*` deprecati.** Con il
controllo di 0.2 attivo, quella cancellazione **fa rossa la CI** — ed è giusto
così. Due strade, e la scelta è del DM:

- **(a)** si tengono i 7 SVG. I master deprecati restano rigenerabili e
  tracciabili; costo: 7 file che nessuno guarda;
- **(b)** i tre master `Lotto-*` finiscono in `_ARCHIVIO/` con la stessa
  procedura già usata per i 16 sorgenti assorbiti di ARC-07 (`git mv` +
  riscrittura controllata dei riferimenti + `README.md` che documenta la
  politica). Allora la cancellazione degli SVG è **conseguente**, non silenziosa.

✅ **Deciso dal DM il 2026-09-05: la (b), archiviazione** — eseguita in
`08_…/Mappe/_ARCHIVIO/`, con una variante che costa zero e non perde niente:
**i sette SVG sono venuti dietro ai loro master invece di essere cancellati**.
`validate_maps` cerca ogni `**/rendered/*.svg`, quindi `_ARCHIVIO/rendered/`
resta **dentro** il suo raggio: i sette restano rigenerabili e in sincrono, il
conteggio non si muove (**31 SVG / 17 master**, come prima), e non serve nessuna
riga di opt-out. L'obiettivo della (b) — togliere tre master deprecati dalla
cartella dove stanno i tre definitivi — è raggiunto lo stesso.

🐛 **Il costo era sottostimato in questo piano, e va detto.** §1.1 diceva «il
riferimento in `L2-REVISED`», al singolare. I riferimenti erano **quattordici in
cinque file**: `MAPPE-CENSIMENTO` (7 righe), `ARC08-00-INDICE` (3), `ARC08-01-GUIDA-DM`
(1 — e punta a **MAPPA 3Z Incrocio Silenzioso**, che è una delle cinque mappe che
il lotto 1b deve portare dentro `L3`), `Atlante-…-COMPLETE` (1), `L2-REVISED` (1),
più due in `campaign/state.md` **lasciati intatti** perché è un log append-only.
Tutti riscritti a `_ARCHIVIO/…`. **È lo stesso errore di R5**: un conteggio fatto
leggendo invece che con un `grep`, in un piano scritto *prima* che ADR-0045
avesse la sua quarta regola.

📌 **Proposta originale**: la **(b)**. Il repo ha già la procedura, i `Lotto-*` sono
sorgenti assorbiti esattamente come quelli di ARC-07, e lasciare in `Mappe/` tre
master deprecati accanto ai tre definitivi è la condizione che genera il prossimo
errore di puntamento.

### 1.2-bis · La coda `⬛` si accorcia

Archiviare `Hammerfist-Lotto-3-FINALE` toglie **1.256 celle** dalla coda di
riclassificazione di `LEGENDA-FUNZIONALE-SPEC` §6.2: la coda viva passa da
**8.216 in 24 file** a **6.960 in 23**. La riga è barrata, non cancellata, e il
totale del 2026-09-04 resta scritto com'era — era vero allora.

### 1.3 · Come si porta dentro

Il branch ha **222 commit** di distanza dalla base. Non si rebasa: si **porta il
contenuto**, e lo si riverifica.

1. Estrarre dal branch i **tre master markdown** e i quattro file di puntamento.
2. Applicarli su un branch nuovo da `main`, risolvendo a mano i conflitti sui
   quattro file di puntamento (che nel frattempo sono cambiati: `ARC08-01-GUIDA-DM`
   ha avuto tre commit, fra cui la reintegrazione dell'Incontro 2F).
3. **Rigenerare gli SVG da zero** con `render_map_svg.py`. Non copiare quelli
   della PR: si rigenerano, e devono venire identici — è già stato provato su L3.
4. Eseguire la scelta 1.2 (archiviazione o mantenimento).

### 1.3-bis · Com'è andata (2026-09-05)

**I tre master.** `L1` e `L3` erano **intatti** su `main` dal merge-base, quindi
sono entrati per intero dal branch; `L2` aveva una sola riga di differenza — la
mia, del lotto 1a — e le è stata riapplicata sopra. Da **1 mappa ciascuno** a
**3 · 3 · 5 = 11**, e la **3Y Ponte Sospeso** adesso esiste.

**I quattro file di puntamento** si sono fusi a tre vie sul merge-base: tre
puliti, **un conflitto solo**, ed è esattamente quello che avevo segnalato
chiudendo 1a — il puntatore 3Z di `ARC08-01-GUIDA-DM`. Risolto tenendo la
versione della PR, che nomina `L3-REVISED` come **griglia canonica** invece del
master deprecato, e correggendole il path storico verso `_ARCHIVIO/`. La drift
di `main` è sopravvissuta: l'Incontro 2F è ancora lì.

**Gli 11 SVG rigenerati da zero.** Sette **byte-identici** a quelli della PR.
Tre differiscono, e uno cambia nome — tutti e quattro per un motivo solo, che ho
verificato riga per riga: **zero differenze fuori dal blocco legenda**.

| Cosa | Perché |
|---|---|
| 3 SVG con legenda diversa | [ADR-0042](adr/ADR-0042-tre-glifi-per-tre-cose.md), mergiata **dopo** la #63: `⬛ — Struttura (tenda, edificio, dais)` è diventato `⬛ — Edificio / corpo di fabbrica`, e `⛺ — Tenda` ha guadagnato la sua chiosa |
| 1 SVG che cambia solo nome | `…drago-sui-.svg` → `…drago-sui.svg`: la `slug` corretta dal lotto A di `PIANO-QUALITA-DEL-CODICE`, **la stessa correzione** che aspetta la #52 |

⚠️ **La riga del piano diceva «byte-identici», ed era vera per il disegno, non
per il file.** Vale la pena tenerla scritta così: quando un renderer migliora,
«identico» smette di essere il collaudo giusto — quello giusto è *«identico
fuori dai punti in cui il repo è migliorato, e su quelli spiegabile»*.

**I tre master archiviati** hanno preso l'intestazione migliore della PR — quella
che manda a `L1/L2/L3-REVISED` *tutte* le griglie, non solo una — **senza** la
frase «gli SVG di questo file sono stati rimossi», che dopo 1a sarebbe falsa.

### 1.3-ter · Il test che si è rotto, e perché non era una regressione

`test_import_ultraclear` ha due test sul **golden case**, e il golden case
**era il master vivo** `Hammerfist-L2-REVISED-Ultra-Clear.md`. Portando dentro
la #63 sono diventati rossi:

- **R1 non più riportato** — la #63 ha reso **uniforme** la griglia che il test
  si aspettava difettosa. Il difetto è stato corretto: buona notizia;
- **Dara Occhiolesto non più fra le unità** — il file è passato da **1 mappa a
  3**, quindi il blocco di annotazioni non appartiene più a `maps[0]`.

Nessuna regressione dell'importatore: **si è mosso il campione**. Il rimedio è
congelarlo — `scripts/tests/fixtures/ultraclear/golden-hammerfist-L2-2026-07.md`,
il master com'era su `main` il 2026-09-05, con in testa il commento che dice
perché sta lì. Verificato che riproduce **tutti e quattro** i difetti-tipo
(R1, R3, R5, R4) e Dara a `[8, 61]` col token 🟢: nessuna asserzione tolta.

⚠️ **Che cosa si perde.** Prima il test toccava un file vero, e un file vero che
cambia sotto un collaudo lo fa suonare. Adesso non suona più — e il file vivo
non ha nessun test che lo guardi. È un compromesso, non un miglioramento netto:
**un campione di collaudo deve stare fermo, e un documento di campagna non sta
fermo**; ma chi domani rompesse l'importatore *sul formato nuovo* a tre mappe non
lo saprebbe da qui. Se serve coprirlo, è un lotto **C** a sé, non questo.

### 1.4 · Validazione

- `validate_maps` verde **col controllo nuovo di 0.2 attivo**
- `validate_modules` sui master ARC-08
- ogni link relativo nei quattro file di puntamento risolve
- **conteggio**: 17 mappe tattiche presenti, la **3Y** fra queste
- `pytest`, `dm.py doctor --ci`, `check_plans_discipline`

**Definizione di fatto**: un DM che apre `ARC08-01-GUIDA-DM` e cerca un incontro
qualsiasi trova la griglia, e nessun link punta a un master archiviato.

---

## FASE 2 — #52: l'overlay professionale sulle mappe degli incendi drow

> **Taglio dei lotti** (ADR-0045). Fase quasi interamente meccanica: il
> giudizio l'ha già fatto ADR-0006, qui si applica.
>
> | | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|---|
> | **2a** ✅ | portare i due master con le direttive `@` e il JSON della scena nuova | **M** meccanico | `[inline · basso · `grep` trova i due master fra quelli che usano `@`]` — **chiuso 2026-09-05: fusione pulita su entrambi** |
> | **2b** ✅ | rigenerare i tre SVG | **M** meccanico | `[inline · basso · 2 su 3 byte-identici, il terzo cambia **solo** nome]` — **chiuso 2026-09-05: la rinominazione era già su `main`** |
> | **2c** ✅ | la scena «Foresta in Fiamme» passa lo standard di modulo | **C** costruzione | `[Sonnet 5 · medio · `validate_modules` verde, scala 1,5 m/quadretto]` — **chiuso 2026-09-05** |

**Perché per seconda.** Costa **una rinominazione** e chiude una dimostrazione
che serve al metodo, non solo a quella scena.

### 2.1 · Cosa entra, e perché il valore non è il disegno

Il pezzo che conta è la **prova che le direttive `@` di
[ADR-0006](adr/ADR-0006-annotazioni-mappa-overlay-professionale.md) funzionano
sui master scritti a mano**, non solo su quelli compilati da JSON — e **in
place**, senza ricostruire la griglia, quindi senza perdere il disegno
esistente. Oggi i 14 master che usano le direttive sono tutti generati.

| Artefatto | Cosa |
|---|---|
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | direttive `@` su **Campo Drow 2**: bussola, rotte di pattuglia/assalto/squadre incendiarie, zone etichettate, landmark (Wyrmlord, tesoro, prigioni) |
| `…P1B-Cerchio-Treant-COMPLETO-maps.md` | direttive `@` sul **Cerchio Sacro** + **primo SVG committato** per quella mappa |
| `…P1B-Foresta-In-Fiamme` (`.json` + master + SVG) | scena nuova: piromanti drow, **fronte del fuoco** (vento da est), avanzata PG, treant alleato di Hella, ritirata drow, e gli **stati di propagazione** nel blocco EVOLUZIONE |

### 2.2 · L'unico intoppo, ed è meccanico

Il terzo SVG cambia nome: `…grid-6553-scal.svg` → `…grid-65-53-sca.svg`.
Non è marciume: è la **`slug` corretta** dal lotto A di
`PIANO-QUALITA-DEL-CODICE`, che aveva trovato sette implementazioni diverse e
**tutte e sette** incollavano `65×53` in `6553`. Si rigenera e il nome giusto
esce da solo.

### 2.3 · Come si porta dentro, e la verifica

Come F1: contenuto, non commit. Estrarre i master e il JSON, applicarli su
`main`, **rigenerare tutti gli SVG**.

- `validate_maps` verde (attesi **+3** SVG, di cui uno rinominato)
- gli SVG rigenerati coincidono con quelli della PR **tranne** il nome del terzo
- la scena nuova passa `validate_modules`
- la scala della campagna è rispettata: **1,5 m/quadretto**

**Definizione di fatto**: `grep` delle direttive `@` trova i due master scritti
a mano fra quelli che le usano, e la scena «Foresta in Fiamme» ha un SVG.

### 2.4 · Com'è andata (2026-09-05)

✅ **Definizione di fatto soddisfatta.** `grep '^@north\|^@mark\|^@path\|^@zone'`
trova adesso **tre** master scritti a mano fra quelli che usano le direttive —
i due previsti più la scena nuova — e «Foresta in Fiamme» ha il suo SVG.
`validate_maps`: **40 SVG / 18 master**.

**Nessun conflitto.** Entrambi i master si sono fusi puliti: la PR aggiunge solo
blocchi `@` in coda alle griglie, e non tocca niente di ciò che è cambiato dopo.

⚠️ **Due previsioni del piano erano sbagliate, tutte e due in meglio.**

| Il piano diceva | Com'è davvero |
|---|---|
| «costo: **una rinominazione**» | **già fatta**: `main` porta `…grid-65-53-sca` dal lotto A di `PIANO-QUALITA-DEL-CODICE`, e il rigenerato ci è caduto sopra da solo. Costo zero |
| «attesi **+3** SVG» | **+1**. Il `Cerchio Sacro` e la `map01` dei campi drow **esistono già** su `main`: li ha renderizzati il gate di [ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md), che il 4 settembre ha trovato «due master di ARC-09 con quattro mappe mai renderizzate». Quindi qui **due SVG guadagnano l'overlay** e **uno solo nasce** |

**I quattro SVG rigenerati**: uno byte-identico a quello della PR («Foresta in
Fiamme»), tre diversi — e come in F1, **zero differenze fuori dal blocco
legenda**: è la riscrittura di ADR-0042, che sposta `⬛` in cima e lo chiama
`Edificio / corpo di fabbrica`. La `map01` dei campi drow si è rigenerata
**identica a quella committata su `main`**: non compare nemmeno fra i file
modificati.

📌 **La dimostrazione che serviva al metodo è fatta**: le direttive `@` di
ADR-0006 funzionano su master **scritti a mano**, in place, senza ricostruire la
griglia — il disegno esistente non si è perso in nessuno dei tre.

---

## FASE 3 — #106: la catena dei raster e Blender come geometria

> **Taglio dei lotti** (ADR-0045). È la fase con più classi diverse, ed è il
> caso in cui il taglio serve davvero.
>
> | | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|---|
> | **3a** ✅ | portare i due script e i loro 418 test | **M** meccanico | `[inline · basso · i test passano com'erano]` — **chiuso 2026-09-05: non passavano, e la ragione era buona** |
> | **3b** ✅ | `SCARTI.txt` — il registro di cosa si butta e perché | **C** costruzione | `[Sonnet 5 · medio · un test che prova che un `--reroll` senza motivo **non** passa]` — **chiuso 2026-09-05: 7 test, e il gate morde anche in CI** |
> | **3c** ✅ | gli smoke in CI e il controllo di determinismo del piano di scena | **C** costruzione | `[Sonnet 5 · medio · il controllo boccia un piano non deterministico]` — **chiuso 2026-09-05** |
> | **3d** | 🖥 generare i diciotto raster e sceglierli | **G** giudizio | `[**il DM**, sulla sua macchina · — · diciotto immagini che lui tiene]` |
>
> ⚠️ **3d non è un lotto di agente.** Il collo di bottiglia è **il giudizio, non
> la GPU**: ~1,5-2 ore, e quasi tutte sono scegliere quale variante tenere.

**Perché per terza.** Vale molto e non è urgente al tavolo: nessuna sessione si
blocca perché mancano i diciotto raster del Drappo. E l'ultimo passo **non si può
fare qui**: serve la macchina del DM.

### 3.1 · Cosa entra

**`comfyui_batch.py`** (567 righe, 216 di test). Il markdown resta il master
(ADR-0003) e diventa **eseguibile**: un commento HTML sopra ogni blocco di
prompt porta `id`, `size`, `stile`, `serie`, `seed`. Il prompt si corregge **nel
documento, mai nello script**.

**`render_map_blender.py`** (381 righe + 346 nello script Blender, 202 di test).
Risolve la geometria con la **stessa `paint()`** che alimenta l'SVG: non è una
comodità, è la garanzia che le due catene **non possano** divergere.

### 3.2 · Misurato contro la pratica dell'illustrazione AI-aided: cinque su sei

| Requisito | #106 |
|---|---|
| Prompt, seed, modello e risoluzione **fuori dal codice** | ✅ annotazione in commento HTML, invisibile nel rendering |
| **Determinismo prima della scelta** | ✅ seed derivato dall'`id` con SHA-256, non sorteggiato: due macchine partono dalle stesse diciotto immagini. `--reroll N` cambia tentativo in modo altrettanto ripetibile |
| **Provenienza scritta** | ✅ `PROVENIENZA.txt` con file · modello e versione · **licenza dei pesi** · seed · data · chi — e **nasce prima** delle immagini |
| **Igiene di licenza sui pesi** | ✅ **exit 1 nel codice**, non un avvertimento, se il checkpoint contiene `flux1-dev` e varianti — e *prima* di ogni scrittura e di ogni chiamata di rete (ADR-0019: la licenza è dei pesi, non del software) |
| **Condizionamento da geometria reale** | ✅ `--profondita`: il pass Z alimenta ControlNet depth, coi due passi scritti nel codice perché non li salti — **normalizza** (il pass Z è in metri, un PNG no) e **inverti** (ControlNet vuole il vicino chiaro): saltare l'inversione dà un'immagine che *sembra* giusta e guida il modello al contrario |
| **Il giudizio umano nel ciclo** | ⚠️ **manca** |

### 3.3 · Il sesto requisito, e il deliverable che F3 aggiunge

`--fissa-seed` registra **la scelta**, ma non c'è dove scrivere **cosa è stato
scartato e perché**. `rumblingstone-art-direction` dice che un'immagine **si
butta** invece di tenerla perché «è già venuta» — e quel giudizio, che è il
lavoro vero, oggi non lascia traccia.

**Deliverable 3.3**: un `SCARTI.txt` accanto a `PROVENIENZA.txt`, con la stessa
forma — `id · seed · reroll · motivo`. Il motivo è **testo libero e obbligatorio**:
serve a chi rifà la serie fra un anno per non ripercorrere gli stessi vicoli
ciechi. È il file che trasforma diciotto immagini scelte in **una serie
motivata**.

### 3.4 · Le tre decisioni di `render_map_blender.py` che si vedono solo nel risultato

1. **Nessun piano di appoggio** — ogni cella è un solido, terreno compreso: con
   un piano sotto, una voragine resterebbe coperta e il passo di profondità la
   leggerebbe **piatta**, cioè proprio l'informazione per cui il passo esiste.
2. **Le celle uguali si fondono in rettangoli** — la Ruota passa da **2.944 cubi
   a 38 solidi**.
3. **L'asse Y si ribalta** — quello di Blender sale, quello della griglia scende:
   senza il ribaltamento la mappa esce **speculare**, l'errore che non si nota
   finché qualcuno non cerca la curva nord a sud.

### 3.5 · Il taglio: cosa si fa qui e cosa sulla macchina del DM

| | Dove |
|---|---|
| Gli **script**, i test, i gate, `SCARTI.txt`, la documentazione | ✅ **qui** |
| I **diciotto raster** | 🖥 **macchina del DM** — questo ambiente non ha GPU (`nvidia-smi` assente) e ComfyUI non è in ascolto |
| Il **render Blender** | 🖥 **macchina del DM** — il binario non c'è |

⚠️ **Il collo di bottiglia è il giudizio, non la GPU**: ~1,5-2 ore, e quasi tutte
sono scegliere quale delle quattro varianti tenere.

### 3.5-bis · Com'è andata (2026-09-05) — 3a, 3b, 3c

**3d resta al DM**, come previsto: qui non c'è GPU, Blender non è installato e
ComfyUI non è in ascolto. Tutto il resto è dentro.

#### 3a — «i test passano com'erano». Non passavano.

Dieci test rossi su `render_map_blender`, per una ragione sola:
`render_map_svg.slugify` **su `main` si chiama `nome_mappa`**. È la rinominazione
del lotto A di `PIANO-QUALITA-DEL-CODICE` — **la terza volta** che quel lotto si
presenta in questa ripresa: in F1 come nome di file SVG, in F2 come la
«rinominazione» che era già stata fatta, qui come chiamata rotta. Una riga, e i
**52 test** dei due script passano.

🔎 **Il criterio del piano era ingenuo, e vale scriverlo.** «I test passano
com'erano» presuppone che l'ambiente attorno sia fermo. A 222 commit di distanza
non lo è mai: il criterio giusto per un lotto di trapianto è *«i test passano
dopo aver riallineato le chiamate a ciò che il repo espone oggi, e il
riallineamento è meccanico»*.

⚠️ **E c'era una mina, che il piano non poteva vedere.** La PR committa un
`PROVENIENZA.txt` che avrebbe **cancellato venti righe di provenienza vera** —
le immagini che il DM ha generato il 2026-08-15 con Gemini, col C2PA, le
dimensioni, e l'avvertenza che **il seed non è esposto dal servizio**, quindi
quella serie non è rigenerabile e il PNG *è* l'artefatto. Proprio il contenuto
che ADR-0019 esiste per proteggere, cancellato dallo strumento che serve a
proteggerlo. Il file di `main` è stato **ripristinato** e gli si è aggiunto in
testa il blocco che descrive la catena ComfyUI: le due convenzioni convivono, e
si distinguono perché nelle righe nuove **il seed c'è**.
🔎 Verificato che il *codice* invece era a posto: `scrivi_provenienza` conserva
il file e sostituisce solo la riga omonima. Il pericolo era il file committato,
non lo script — e sono due cose che si controllano separatamente.

**Il manifest ha cambiato forma** dal merge-base: `use_case` è entrato, e
`ci_smoke`/`consumes_schema`/`produces_schema`/`docs`/`tests` sono usciti. I tre
descrittori sono stati **convertiti** alla forma di oggi, non incollati, e i tre
registri derivati (`registry.json`, `docs/tools/README.md`, `mcp-tools.json`)
**rigenerati** con `--emit-all` invece che fusi a mano. **57 tool conformi.**

**Un contratto che non tornava**, trovato da un test e non da noi:
`test_ambiente` pretende che ogni binario dichiarato nel manifest stia nel
registro di `binari.py`, e **`blender` non c'era**. Senza, `dm.py doctor` non
avrebbe mai potuto dire che manca. Registrato, con la degradazione scritta:
*la geometria si risolve lo stesso — `--piano-solo` scrive il piano senza
Blender, ed è quello il pezzo deterministico; mancano il PNG e il passo di
profondità, che sono presentazione e non canone.*

#### 3b — il sesto requisito

`SCARTI.txt` accanto a `PROVENIENZA.txt`, forma `id · seed · reroll · motivo`,
intestazione che spiega la regola. `--motivo` è **obbligatorio con `--reroll`**:
senza, exit **2** *prima* di leggere, scrivere o chiamare la rete — un rifiuto
che non si sa spiegare non deve nemmeno cominciare. La scrittura è idempotente
sulla coppia `(id, reroll)`, come già `scrivi_provenienza` sulla scelta.

📌 **Lo scarto si registra prima di rigenerare**, non dopo: il tentativo di ieri
è stato buttato comunque, anche se quello di oggi fallisce.

**Sette test**, di cui tre provano che il gate **morde**: reroll senza motivo
esce 2 e **non crea nessun file**; un motivo di soli spazi non conta; e
`--reroll 0` non chiede niente, perché il gate riguarda il rifiuto e non la
generazione — chiedere un motivo dove non c'è nulla da buttare sarebbe attrito
senza scopo.

#### 3c — la CI prova che i cancelli mordono

Agli smoke si aggiungono `--help`, `--lista` e `--dry-run` della catena raster,
più **due passi che un `--help` non prova**:

| Passo | Cosa boccia |
|---|---|
| **i cancelli mordono** | un `flux1-dev` che *passasse* fa rossa la CI; un `--reroll` senza motivo che *passasse* pure |
| **piano 3D deterministico** | due giri di `--piano-solo` che non danno lo stesso file |

⚠️ Il secondo è scritto al contrario di come viene naturale: **fallisce se il
comando riesce**. È l'unico modo di provare un divieto — e senza, un gate che un
giorno smette di funzionare non lo dice a nessuno, che è la stessa classe di
difetto di ADR-0043.

Entrambi i passi sono stati **eseguiti in locale** prima di scriverli nel
workflow: `✓ pesi vietati rifiutati, reroll senza motivo rifiutato` e
`✓ piano 3D byte-identico su due giri` (48 solidi da 660 celle).

### 3.6 · Validazione

- `pytest` sui due file di test (218 test fra i due, già scritti)
- smoke in CI: `--help`, `--lista`, `--dry-run`, più il **controllo di
  determinismo** del piano di scena 3D
- `test_serie_base_e_diciotto` — il capitolato dice diciotto, i prompt sono
  venti: le due tavole in più sono `serie=extra` e la CI si fa rossa al
  diciannovesimo. **Non è un divieto: è un modo di obbligare a decidere**
- `tools_manifest --check` con i due tool nuovi
- verifica esplicita del divieto: un checkpoint `flux1-dev` **esce 1 prima** di
  scrivere qualsiasi cosa

---

## FASE 4 — #99: i dati di campagna come dati

> **Taglio dei lotti** (ADR-0045). Gli otto lotti di §4.2 non sono della stessa
> classe, ed è il motivo per cui vanno presi uno alla volta.
>
> | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|
> | **4a** ✅ `validate_docs` | **C** costruzione | `[Sonnet 5 · medio-alto · il gate boccia una cartella documentata e inesistente, e **non** boccia i 4 falsi positivi noti]` — **chiuso 2026-09-07: 6 difetti veri, zero falsi positivi** |
> | **4b** ✅ link, path locali e un ADR | **K** canone (era **M**) | `[Opus 5 · alto · `python3 scripts/validate_docs.py --sorgenti` esce 0 su **701 documenti**; ADR-0048 riverificato riga per riga contro il codice di oggi]` — **chiuso 2026-09-10: 22 difetti veri, 9 falsi positivi corretti nel validatore** |
> | **4c** i due tempi di `state.md` | **K** canone | `[**Opus 5, mai delegato** · xhigh · nessun contenuto cancellato, solo etichettato; **due domande al DM** poste, non indovinate]` |
> | **4d** `state.yaml` (ADR-0017) | **K** canone | `[**Opus 5** · xhigh-max · `state.md` **rigenerato è identico** a quello committato]` |
> | **4e** una sola via di scrittura | **C** costruzione | `[Sonnet 5 · alto · un test **sui file veri**, non su fixture — vedi §4.4]` |
> | **4f** prodotto e partita | **C** costruzione | `[Sonnet 5 · alto · un test che dimostra che il reset **non eredita niente**]` |
> | **4g** schede PG a dati | **K** canone | `[**Opus 5** · alto · le schede generate combaciano con quelle scritte a mano]` |
> | **4h** `groups/<slug>/` | **G** giudizio | `[Opus 5 · xhigh · **PR dedicata**, come dice la #99 stessa]` |
>
> ⚠️ **Quattro lotti su otto sono K o G.** È la misura di quanto questa fase
> tocchi il canone, e la ragione per cui **non si mergia in blocco**.

**Perché per ultima.** È la più grossa (88 file, +14.078 / −4.931) e tocca la
parte più delicata del repo — **il canone**. E il suo corpo lo dice da sé:
*«è nata read-only, la riga originale non vale più»*.

### 4.1 · Il vincolo che governa tutta la fase

🔴 **Non si mergia in blocco.** La PR ha già i lotti separati nel corpo, e si
prendono **uno alla volta**, ciascuno col suo commit e i suoi gate.

⚠️ **La correzione del Peso è già uscita** e non va riportata: è il lotto R1 di
`PIANO-RICONCILIAZIONE-PR-APERTE`, già su `main`.

### 4.2 · L'ordine dei lotti, dal meno al più invasivo

| # | Lotto | Cosa porta | Perché in questa posizione |
|---|---|---|---|
| 4a | **G2** — `validate_docs.py` | gate bloccante sulla deriva doc↔realtà | **Indipendente da tutto.** Chiude un difetto reale: `AGENTS.md` documentava `campaign/npcs/`, `locations/`, `encounters/` — **nessuna delle tre è mai esistita**. Ed è progettato attorno ai falsi positivi: alla prima esecuzione **9 hit di cui 4 falsi**, corretti nel validatore e non nei documenti |
| 4b | **G3** — link, path locali e un ADR | **22 difetti veri** (la stima «18 su 241» era di un mese prima e sbagliata in tutte le cifre) · 7 file con path dentro un checkout personale | ⚠️ **non era igiene pura**: uno dei link rotti citava una decisione mai registrata, e recuperarla ha reso il lotto **K** |
| 4c | **G1** — i due tempi di `state.md` | §1 collocava i PG **dopo Hammerfist** mentre §0 marca l'arco 08 `⬜ NON giocato` | ⚠️ tocca il canone, ma **non cancella niente: etichetta**. Estende la tabella a due tempi che §6 aveva già, DM-confermata. Porta con sé **due domande al DM** (il −2 COS di Thorik, il Giorno di Marcia 19 vs ~15) |
| 4d | **G2-bis** — ADR-0017, `state.yaml` | i fatti come dati, `state.md` **generato** | il pezzo grosso. Vedi 4.3 |
| 4e | **G2-ter** — una sola via di scrittura | clock villain, «chi sa cosa», numeri di Rethmar migrati a dati; il log di sessione prende un front-matter coi delta | dipende da 4d |
| 4f | **G2-quater** — prodotto e partita | il reset per gruppo nuovo **perdeva**: azzerava `state.md` e `sessions/` e lasciava `state.yaml`, `state-changelog.md`, `campaign-history.md` e i recap al gruppo dopo | dipende da 4d/4e |
| 4g | schede PG a dati | `PG/schede/*.yaml` + `.md` generati | oggi le schede PG **non esistono come dato** da nessuna parte |
| 4h | ADR-0018 — `groups/<slug>/` | multi-gruppo per directory invece che per branch | **PR dedicata**, come dice la #99 stessa |

### 4.2-bis · Com'è andato 4a (2026-09-07)

Portato `validate_docs.py` dalla #99 e giudicato **sul repo di oggi**, un mese
dopo che è stato scritto: trova **sei percorsi citati e inesistenti**, e li ho
verificati uno per uno prima di toccare i documenti — **nessun falso positivo**.

| Dove | Cosa asseriva |
|---|---|
| `AGENTS.md` 24-26 | l'albero di `campaign/` elencava `npcs/`, `locations/`, `encounters/` |
| `AGENTS.md` 161-162 | convenzioni di nome per due di quelle cartelle |
| `AGENTS.md` 210 | `campaign/lore/rhod-adaptations.md`, che non esiste in nessun posto |
| `AGENTS.md` 225 | *«Check `campaign/npcs/` before describing NPCs»* |
| `README.md` 54 | i PNG «dettagliati in» una cartella che non c'è |

⚠️ **Il peggiore è il quarto**, e non è un refuso: è una **istruzione** nel
documento che un agente legge per primo, che lo manda a cercare in una cartella
mai esistita. I PNG vivono in `Bestiario/png/` (32 file) e `Bestiario/villain/`.

**Corretti puntando alla realtà, non cancellando**: l'albero adesso elenca le
cartelle vere (`recaps/`, `ai-media-prompts/`) e dice a chiare lettere dove
stanno davvero PNG, luoghi e incontri; gli adattamenti di RHoD puntano a
`campaign-coherence.md`, che è dove sono per davvero.

🔎 **Due gate hanno trovato roba da soli, mentre chiudevo il lotto.**

1. `tools_manifest --check` si è accorto che il tool nuovo **non aveva un
   descrittore** — scritto nella forma di oggi, non copiato dalla #99 che ha
   un'altra forma. **59 tool**.
2. `test_nessuno_script_legge_dal_mirror` ha bocciato una riga dei test di
   `validate_docs`: `_is_generated_mirror(".claude/skills/x")`. ⚠️ **Falso
   positivo**, e della **stessa famiglia** di quello che quel test aveva già
   incontrato una volta — il suo commento dice *«un guardiano che accusa sé
   stesso è un guardiano che verrà spento»*. Una stringa **passata a** una
   funzione che riconosce il mirror non lo legge: gli chiede se lo è, ed è il
   codice che serve a **escluderlo**. Aggiunta l'esenzione mirata, e verificato
   che la regola morde ancora su un file che legge davvero dal mirror.

### 4.2-ter · Com'è andato 4b (2026-09-10)

**La stima era sbagliata in tutte e tre le cifre**, ed è la quarta volta in
questa campagna. Il piano diceva *«18 link rotti su 241 · 4 file con
`/home/…`»*; il repo di oggi ne dà **26 su 558**, e i file sono **7**. Ma il
numero conta meno della scomposizione, perché è la scomposizione che ha
cambiato la classe del lotto.

| Classe | N | Cos'era davvero |
|---|---|---|
| Falsi positivi **del validatore** | 9 | `paths_from_links` catturava `![alt](path)` scritto **dentro i backtick** |
| Rinomine con prova nel repo | 14 | slug di ADR cambiati a numero invariato, prefisso `plans/` raddoppiato, `.webp`→`.png`, `file:///` → link relativo |
| Vendored, fuori scopo | 2 | `scripts/typst/packages/…`, ADR-0026 |
| **Una decisione mai registrata** | 1 | ed è il motivo per cui 4b non è più **M** |

🔎 **Il falso positivo più bello**: fra le nove righe c'era, per intero, la riga
di `plans/CHANGELOG.md` che descriveva *proprio questo difetto* nel convertitore
markdown→Typst. Il gate ha ripetuto l'errore che quella riga documentava.
Corretto nel validatore — `senza_code_span` — **senza toccare un documento**.

⚠️ **Il difetto vero non era un link rotto.**
`docs/guides/LEGENDA-FUNZIONALE-SPEC.md:26` citava
`ADR-0014-legenda-funzionale-fonte-unica.md`, che non esiste in nessun posto:
era l'ADR-0014 della **PR #72**, e il commit `82e1c16` dice che di quella PR se
ne recuperarono **due** (ex-0016 → ADR-0039, ex-0017 → ADR-0040) perché
*«i numeri ADR 0014-0018 erano stati occupati da altre decisioni nel
frattempo»*. Il terzo era rimasto indietro. Decisione DM: **recuperarlo** →
[ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md).

🔴 **Il costo del ritardo si misura**, e l'ADR lo dice: `⛰` è entrato in
`WALL_SYMS` con ADR-0043 e `⛺` con ADR-0042 — **due ADR separati per due
sintomi della stessa causa**, perché la fonte unica non c'era. Ognuno era
corretto; nessuno poteva togliere la causa. L'ADR nasce **«accettata, non
attuata»**: l'attuazione è il lotto 1.1 di `PIANO-VENDIBILITA`, ⬜.

**Il cancello, e i suoi due errori di taratura trovati misurando.**
`validate_docs` cresce di tre cose: la correzione sui backtick, il modo
`--sorgenti` (enumera da `git ls-files`, **quarta regola di ADR-0045**) e il
controllo sui percorsi assoluti.

1. ⚠️ **Il primo regex era troppo largo.** Cercava `/home/<utente>/` e ha
   segnalato **undici righe di `converters/*/DEPLOYMENT.md`** — `User=htmlconverter`
   in una unit systemd, `ENV PATH=/home/converter/…` in un Dockerfile, il path
   standard di Homebrew su Linux. Tutte **corrette**: sono destinazioni di
   deploy su un server, non la scrivania di chi scrive. Il segno che distingue
   le due cose è **il nome del repo dentro il percorso**. Limite dichiarato: un
   path personale che non nomina il repo non viene visto.
2. 🔎 **Poi il cancello ha morso il proprio file di test** — il fixture contiene
   il difetto per costruzione. È il caso per cui la direttiva d'uscita esiste, e
   ha richiesto di farla funzionare **anche fuori dai markdown** (dentro un
   commento della lingua ospite).

**`--sorgenti` gira solo sui link**, non su alberi e path inline: quelli sono
tarati sui tre documenti d'ingresso, e scatenarli su 700 file aprirebbe una
superficie di falsi positivi che nessuno ha misurato. È l'errore che 4a aveva
evitato apposta.

**I due script di `Tordek/` resi portabili** (decisione DM). 🔎 E rendendoli
portabili si è visto che i path di `generate_therysol.py` erano rotti **due
volte**: oltre alla macchina, puntavano a una cartella che nel frattempo si era
spostata di un livello. Finché il path era assoluto e irraggiungibile, la
seconda rottura **non era visibile**. ⚠️ Ora però partono, e partendo
sovrascrivono HTML editato a mano: il README lo dice.

**I due ADR rimasti della #72, giudicati prima di proporli** (⚠️ e non dopo: era
il rilievo del DM — *«bisogna valutare se sono superati prima di marcarli
recuperabili»*, che è ADR-0044 applicata a sé stessa).

**ex-0015 — dipendenze a livelli e pacchettizzazione. 🔴 Contraddetto, non
superato: non si recupera.** Proponeva tre livelli di dipendenza, con un
livello 1 che ammetteva `numpy` · `scipy` · `networkx` · `tcod` per un linter di
progettazione. Il 3 settembre **ADR-0037** ha deciso l'opposto, e con il DM:
*«gli script Python di questo repo usano la sola libreria standard; le dipendenze
esterne ammesse sono binari, non pacchetti Python»*, perché gli strumenti girano
sul portatile del DM la sera della sessione. Recuperare ex-0015 significherebbe
**riaprire ADR-0037**, non colmare un vuoto. E le due gambe su cui stava in piedi
non ci sono più: il consumatore che giustificava il livello 1
(`scripts/lint_map_design.py`) **non è mai stato scritto**, e l'audit che ne
misurava il guadagno non è nel repo. L'unica parte viva — la pacchettizzazione,
`pyproject.toml` assente e **24** `sys.path.insert` — ha già casa in **ADR-0040**
e nel lotto 0.2 di `PIANO-VENDIBILITA`.

**ex-0018 — l'edizione commerciale come AP originale. 🟡 Non superato: la
conclusione sì, la misura no.** Diventa **D11**, con i suoi due avvertimenti
scritti nella domanda: l'ADR è una *proposta* con gate legale, e l'audit da cui
dipende non è in repo.

**L'indice degli ADR, chiuso nello stesso lotto.** `docs/INDEX.md` §4 si era
fermato ad **ADR-0020** mentre `plans/adr/` era arrivata a **0048**: **28
assenze**, invisibili a tutto quello che 4b aveva costruito fin lì, perché
nessun link era rotto — i percorsi citati esistevano tutti, mancavano le righe.
È la forma esatta delle 13 skill su 18 di ADR-0041. Le 28 righe sono scritte a
mano, perché la colonna «Tema» è editoriale; ma **la completezza no**: un terzo
controllo di `--sorgenti` conta gli ADR **dalla cartella** e boccia se l'indice
ne salta uno. Scriverle e basta, sapendo che ridriverebbero, era l'errore che
questo repo continua a registrare.

**Lasciato fuori, dichiarato**: i **51 link rotti su 51** nei booklet generati,
che sono un difetto del generatore e non della documentazione. Un lotto nuovo,
non 4b.

### 4.3 · Il lotto 4d, e perché vale la pena

Misurato **prima** di decidere: `state.md` era **1.677 righe, di cui 1.150 (68%)
di changelog**; delle 527 vive, 215 tabellari e 234 di prosa. Da lì l'**ibrido**
invece della conversione integrale — e **YAML invece di JSON**, perché JSON non
ammette commenti e un file di canone senza commenti è un file che nessuno
correggerà mai.

**Il vincolo che chiude alla radice il difetto dei due tempi**: `oggi` e `tempo`
**obbligatori** nello schema. Un fatto senza tempo dichiarato **non è
esprimibile**.

**Un master, mai due**: le tabelle di `state.md` diventano generate. Il file
passa da 1.677 a **546 righe**; lo storico esce in `state-changelog.md`.

⚠️ **Il limite, dichiarato dall'ADR stesso e da tenere in vista**: lo schema
vincola la **forma**, non la **verità**. Un fatto sbagliato con un tempo giusto
passa.

### 4.4 · La regressione da non ripetere

🔁 La #99 racconta una sua regressione: lo split dello storico aveva rotto
`state_apply --migrate`, e **la CI non l'aveva vista** perché quei test girano su
fixture. Ha aggiunto due test **sui file veri**.

**Vincolo per 4d/4e**: ogni lotto che tocca `state_apply` o `render_state`
aggiunge almeno un test **sul file vero**, non solo su fixture. È il punto in cui
questo piano può fallire più silenziosamente.

### 4.5 · La misura da guardare in faccia

La #99 la scrive nel suo audit, ed è il motivo per cui questa fase esiste:

> *«La pipeline che avrebbe prevenuto questi difetti è costruita, ha 31 test, è
> al ~98% — e non è mai stata accesa.»*

Il difetto trasversale che l'audit trova è uno solo: **la qualità vive nelle
regole scritte e non negli automatismi**, e ogni regola senza gate si è già
staccata dalla realtà di qualche misura.

### 4.6 · Validazione

Oltre ai gate soliti, per ogni lotto di F4:

- `validate_state` · `render_state --check` · `validate_pg` (dove pertinente)
- **`state.md` rigenerato dev'essere identico a quello committato** — è il
  controllo che tiene in piedi «un master, mai due»
- per 4c e 4f: **nessun contenuto preparato cancellato**, solo etichettato
- per 4f: un test che dimostri che il reset per gruppo nuovo **non eredita
  niente** — è la falla che quel lotto chiude, e due delle sue perdite le aveva
  aperte l'agente stesso

---

## Piano di validazione trasversale

Vale per **ogni** commit di **ogni** fase.

| Gate | Comando |
|---|---|
| test | `python3 -m pytest scripts/tests/ -q` |
| skill e instradamento (ADR-0041) | `python3 scripts/validate_skills.py` |
| mappe | `python3 scripts/validate_maps.py` |
| moduli | `python3 scripts/validate_modules.py` |
| bestiario | `python3 scripts/validate_bestiario.py` |
| manifest dei tool | `python3 scripts/tools_manifest.py --check` |
| ambiente | `python3 scripts/dm.py doctor --ci` |
| disciplina dei piani | `python3 scripts/check_plans_discipline.py` |

**Invarianti che nessuna fase può violare** (ereditate dalla #99 e da ADR-0041):

- nessuna invenzione di canone — quello che non è attestato si marca
  `[INFERRED — needs DM confirmation]`
- nessun contenuto preparato cancellato: **si etichetta**
- i nomi esistenti non si uniformano
- **nessun gate nuovo nasce non bloccante**
- ogni lotto chiuso aggiorna checklist + `INDEX` + `CHANGELOG` **nello stesso
  commit**

---

## Le decisioni che restano al DM

<!-- decisioni-dm: RIPRESA-PR -->

| # | Fase | Domanda |
|---|---|---|
| ~~D1~~ | F1 | ✅ **decisa 2026-09-05: archiviazione.** I tre master e i loro 7 SVG in `_ARCHIVIO/`; gli SVG non cancellati, così la cartella resta dentro il raggio di `validate_maps` |
| D2 | F3 | I diciotto raster si generano **sulla tua macchina** — quando? La fase si chiude senza, ma la catena resta non collaudata sul risultato vero |
| D3 | F4 · 4c | Le due domande di G1: il **−2 COS di Thorik** e il **Giorno di Marcia 19 vs ~15** |
| D4 | F4 | I **13 stemmi e mappe** del `PALIO-BOOKLET` che la #99 lascia in sospeso: si producono o si tolgono i riferimenti? |
| D11 | F4 · 4b | **L'ADR ex-0018 della #72 si recupera?** Decide che, *se e quando* si pubblica, si pubblica un **AP originale autonomo**, mai un'espansione di RHoD — e porta con sé il **perimetro della v1** (archi 07+08 dentro, 195.739 parole dell'arco 09 fuori, arco 06 da riscrivere, `campaign/` privato per sempre), il vincolo sui marchi, e la regola che *rinominare non basta*. ⚠️ **La conclusione ce l'hai già** (`PIANO-VENDIBILITA` C1 e §5 linea 4); quello che non esiste da nessuna parte è **la misura per arco** e il perimetro. 🔴 **Due cose da sapere prima di dire sì**: l'ADR è in stato **«proposta — gate: decisione DM + verifica di un avvocato IP»**, quindi recuperarlo apre una domanda, non la chiude; e l'audit su cui poggia (`AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`) **non è nel repo**, quindi andrebbe rifatto o il perimetro resta un'asserzione senza prova. 🔎 Rimisurato oggi, il debito è **cresciuto**: `Belkram` era in 49 file, ora **82**; `Moradin` da 1.502 a **1.680** occorrenze; e le fonti WotC dichiarate in `campaign/lore/campaign-history.md` compaiono anche **dentro le skill**, che l'ADR non aveva guardato |
| ~~D5~~ | ~~fuori piano~~ | ✅ **deciso e fatto il 2026-09-04**: il DM l'ha messo in cima alla coda, ed è chiuso insieme al punto cieco di `validate_maps` (ADR-0043) |
| ~~D6~~ | F1 | ✅ **decisa 2026-09-04: ridisegnata.** `…P1C` mappa 3 dichiarava 40×40 e aveva righe da 24 a 26 celle: rifatta **26×29**, nessuna coordinata del testo cambiata |

---

## Cosa resta dopo 4b (2026-09-11)

> Scritto perché ne resti traccia su `main`, non in una chat. Due tabelle,
> divise per **chi aspetta chi**: la prima non aspetta nessuno, la seconda
> aspetta te.
>
> ⚠️ Le domande **non sono ricopiate qui**. Vivono nella tabella marcata di §«Le
> decisioni che restano al DM», e l'elenco unico è
> [STATO-E-ORDINE §4](STATO-E-ORDINE-DEI-PIANI.md), generato da
> `decisioni_dm.py` ([ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md)).
> Un secondo elenco a mano accanto a quello generato è **esattamente** lo
> sfasamento che quell'ADR esiste per impedire: qui ci sono solo i numeri.

### Il lavoro che non aspetta nessuno

| Cosa | Dove vive | Classe |
|---|---|---|
| **Attuazione di ADR-0048** — `scripts/legend.yaml` e i consumatori che ne derivano. L'ADR è *accettata, non attuata*: una decisione **senza cancello** finché il lotto non si chiude | lotto **1.1** di [`PIANO-VENDIBILITA`](PIANO-VENDIBILITA.md) | C |
| **I 51 link rotti su 51 nei booklet generati** — il generatore copia link relativi alla radice dentro file tre livelli più in basso. Si aggiusta la sorgente, non l'artefatto | `build_booklet_html.py` · `hype_homebrew.py` | M |
| **4e** una sola via di scrittura · **4f** prodotto e partita | §4.2, dipendono da 4d | C |
| **`validate_prosa`: 161 rilievi in 340 file** (non bloccante). ⚠️ Il piano diceva «13»: era una misura vecchia e di un altro validatore | `scripts/validate_prosa.py` | M |

### Il lavoro fermo su una tua decisione

| Cosa | Aspetta | Perché non posso deciderlo io |
|---|---|---|
| **3d** — i diciotto raster | **D2** | serve la tua macchina, e il collo di bottiglia è il giudizio sulle immagini, non il tempo GPU |
| **4c** — i due tempi di `state.md` | **D3** | è canone: due fatti del tavolo che solo tu sai |
| I 13 stemmi e mappe del `PALIO-BOOKLET` | **D4** | si producono o si tolgono i riferimenti: è una scelta di prodotto |
| Recuperare l'ADR ex-0018 della #72 | **D11** | ed è una *proposta* con gate legale, non una decisione tecnica |
| **4d** `state.yaml` · **4g** schede PG a dati · **4h** `groups/<slug>/` | 4c prima | K e G: si prendono uno alla volta, e 4h vuole una PR dedicata |

### ⚠️ Quattro PR aperte col contenuto già su `main`

È il rischio da cui questa ripresa è partita — *«non vorrei piani e PR che si
sovrappongono o che sono parzialmente obsolete ma che per sbaglio le mergio»* — e
**oggi è ancora aperto**:

| PR | Stato reale | Cosa succede se si mergia per sbaglio |
|---|---|---|
| **#63** | contenuto portato (F1: lotti 1a-1d) | riporta indietro 11 SVG e i puntatori a tre vie già risolti |
| **#52** | contenuto portato (F2: lotti 2a-2c) | idem sugli overlay `@` |
| **#67** | giudicata **superata** in R9 | reintroduce un handout fuori pipeline che **detta tattica al giocatore** |
| **#106** | aperta **solo** per 3d | il resto è già su `main` |
| **#99** | in corso, lotto per lotto | 4a e 4b sono dentro; il resto no |

🔴 **Nessuna di queste va mergiata.** #63, #52 e #67 si **chiudono** (il contenuto
è già dove serve); #106 e #99 restano aperte come segnaposto di ciò che manca.
Chiuderle è un'azione sul tuo repo e aspetta una tua parola.

---

## Come si misura che il piano è finito

Non «quattro PR chiuse». Queste:

1. Un DM che gioca **ARC-08** trova la griglia di ogni incontro, **3Y compresa**.
2. Le direttive `@` funzionano su master scritti a mano, e c'è **una mappa che lo
   dimostra** oltre a quelle generate.
3. La serie dei diciotto raster si **rifà da capo** su un'altra macchina, e si sa
   **cosa era stato scartato e perché**.
4. Un fatto di canone **senza tempo dichiarato non è esprimibile**, e `state.md`
   si rigenera identico dal suo `state.yaml`.

⚠️ E una cosa che il piano **non** promette: che il canone sia vero. I gate
verificano forma, copertura e coerenza fra artefatti. La verità di quello che è
successo al tavolo la sa solo il DM.
