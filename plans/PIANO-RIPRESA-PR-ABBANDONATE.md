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
> | **3d** | 🖥 **collaudare la catena e confrontare**, non generare diciotto | **G** giudizio | `[**il DM**, sulla sua macchina · ~20 min · due o tre immagini SDXL messe accanto a quelle di Gemini, e una scelta presa **guardando**]` — riformulato 2026-09-11, vedi §3.6 |
>
> ⚠️ **3d non è un lotto di agente**, e non è più da 1,5-2 ore: le diciotto
> immagini **esistono già** (§3.6). Il collo di bottiglia resta il giudizio, ma
> ora si esercita su un confronto di due o tre immagini, non su una serie intera.

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

### 3.6 · 3d riformulato (2026-09-11): le immagini ci sono già

🔎 **Il lotto 3d è stato scritto su un fatto che oggi è falso.** Diceva
«generare i diciotto raster», e i diciotto **esistono tutti** — più le due
`serie=extra`. Li ha generati il DM **con Gemini** il 2026-08-15, sono montati
nel modulo con i loro derivati web, `PROVENIENZA.txt` è compilato e
`validate_standalone` è verde. È la **quinta stima invecchiata** di questa
ripresa, e l'unica che stava per costare al DM due ore di lavoro inutile.

**Perché lo strumento diceva il contrario.** `comfyui_batch --lista` dava «sei
da fare»: cinque ritratti e una tavola. Non mancavano — avevano un **nome
diverso** da quello che la specifica si aspettava:

| La specifica diceva | Il file è | Chi ha ragione |
|---|---|---|
| `ritratto-vesca` · `ritratto-attu` · `ritratto-roncetti` · `ritratto-sfregio` · `ritratto-grasa` | `png-vesca` · `png-attu` · `png-roncetti` · `png-sfregio` · `png-nonna-grasa` | **il file** |
| `tavola-tarsilia-dallalto` | `tavola-tarsilia-citta` | **il file** |

Il nome giusto è quello dei file per due ragioni indipendenti: i documenti del
modulo ci puntano già (`![Ottavia Vesca](…/web/png-vesca.jpg)`), e `png-` è la
convenzione del repo per i **personaggi non giocanti** (`Bestiario/png/`) — la
stessa distinzione che l'elenco §5 della specifica fa due righe più sotto, «i 6
PG» contro «i 5 PNG». Allineati gli `id`: **18 su 18 già presenti**.

⚠️ Cambiare un `id` cambia il seed derivato, ma nessuna di quelle sei aveva un
seed fissato e nessuna è mai stata generata con questa catena: non si perde
niente.

### 3.6-bis · La decisione vera, e cosa ha scelto il DM

L'arte del Drappo è di **Gemini**; la catena costruita in F3 genera con **SDXL
in locale**. Quale delle due è il canone del modulo? ADR-0019 §2 aveva già
inquadrato il caso:

| | Gemini (quello che c'è) | SDXL locale (quello che la catena fa) |
|---|---|---|
| Riproducibilità | **nessun seed esposto**: irripetibile, il PNG *è* la sorgente | seed → identica su qualsiasi macchina |
| Licenza | contratto di servizio, **cambia**; e verificato su fonti **secondarie** | OpenRAIL++-M, **perpetua** |
| Provenienza | **firmata C2PA**, verificabile — qui Gemini è migliore | la scrivi tu |
| Qualità | conosciuta, e il DM la giudica buona | **mai vista** |

⚠️ Una cosa che **non** discrimina: un'immagine puramente generata con ogni
probabilità non è tutelabile da copyright. Vale per entrambe.

✅ **Scelta del DM (2026-09-11): collaudo prima di scegliere.** *«Voglio fare
prima un collaudo con 2 o 3 immagini e vedere davvero la qualità prima di
buttare quelle di Gemini, che sono carine»*. Sul suo computer, con ComfyUI in
ascolto:

```bash
python3 scripts/comfyui_batch.py \
  --solo ritratto-vanna --solo tavola-la-ruota \
  --out /tmp/confronto-sdxl
```

🔴 **`--out` su una cartella a parte è la parte importante**: nessuna immagine
attuale viene toccata, e il confronto si fa affiancandole. Se una variante non
convince, `--reroll 1 --motivo "…"` — e il motivo finisce in `SCARTI.txt`
(ADR-0046), che è il punto: la serie diventa **motivata**, non solo scelta.

**Cosa si ottiene comunque, quale che sia l'esito**: la catena raster viene
provata contro un ComfyUI vero per la prima volta. È il buco dichiarato di F3 —
il sesto requisito su sei — e si chiude al costo di due immagini invece che
diciotto.

**Quando D2 si chiude**: quando il DM ha guardato il confronto e ha detto **A**
(le Gemini restano canone) o **B** (si rigenera la serie con SDXL). Non prima.

---

## FASE 4 — #99: i dati di campagna come dati

> **Taglio dei lotti** (ADR-0045). Gli otto lotti di §4.2 non sono della stessa
> classe, ed è il motivo per cui vanno presi uno alla volta.
>
> | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|
> | **4a** ✅ `validate_docs` | **C** costruzione | `[Sonnet 5 · medio-alto · il gate boccia una cartella documentata e inesistente, e **non** boccia i 4 falsi positivi noti]` — **chiuso 2026-09-07: 6 difetti veri, zero falsi positivi** |
> | **4b** ✅ link, path locali e un ADR | **K** canone (era **M**) | `[Opus 5 · alto · `python3 scripts/validate_docs.py --sorgenti` esce 0 su **701 documenti**; ADR-0048 riverificato riga per riga contro il codice di oggi]` — **chiuso 2026-09-10: 22 difetti veri, 9 falsi positivi corretti nel validatore** |
> | **4c** ✅ i due tempi di `state.md` | **K** canone | `[**Opus 5, mai delegato** · xhigh · nessun contenuto cancellato, solo etichettato; l'insieme si conta con `grep -n "resurrection\|resurrezione" campaign/state.md` — **15 righe**, di cui 4 al tempo sbagliato e 6 nel changelog append-only, lasciate intatte]` — **chiuso 2026-09-12: 4 asserzioni al tempo sbagliato, 2 costi mai versati, 1 verbo al passato** |
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
| 4c ✅ | **G1** — i due tempi di `state.md` | §1 collocava i PG **dopo Hammerfist** mentre §0 marca l'arco 08 `⬜ NON giocato` | ⚠️ tocca il canone, ma **non cancella niente: etichetta**. Chiuso il 2026-09-12 — vedi **§4.2-quater**: due costi risultavano **versati senza essere stati giocati**, e il ridisegno dei Doni che ne è nato è una **proposta separata**, non canone |
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

### 4.5-bis · D3 risposta dal DM (2026-09-11): una domanda su due si scioglie

**Il calendario non era un difetto.** L'apparente contraddizione — `state.md`
dice Giorno di Marcia **19** mentre l'arco 08 è ⬜ **non giocato** — è il
**viaggio nel tempo**, ed è già scritto in due master:

| Dove | Cosa dice |
|---|---|
| `ARC08-00-INDICE` righe 17-19 | i PG *«riemergono al Cuore della Montagna al **Giorno 3** e chiudono la battaglia al **March Clock Day 19** (sync con la caduta di Terrelton)»* |
| `ARC07-DEF-5` §94 | *«siete arrivati al **Giorno 3** (≈ March Clock Day 18-19): il **sync** con l'ARC-08»* |
| `state.md` riga 54 | lo chiama già **«Day 19 (target sync)»** |

Il Giorno 3 è il terzo giorno **dell'assedio**, il Day 19 è il **March Clock**:
due orologi diversi, e il documento li allinea. Quel che resta è **una parola**:
la riga 136 dice *«Current March Day: 19 (Terrelton just fell…)»* al passato,
come se fosse già successo, mentre è il bersaglio a cui il salto del Rubino
consegna i PG. Si corregge il tempo verbale, non il numero.

🔎 **Ottavo presupposto invecchiato.** Il piano dava «19 vs ~15» per una
contraddizione di canone da far decidere al DM. Non lo era: era una domanda a
cui il repo aveva **già** risposto in due posti, e che nessuno aveva collegato.

**Il COS di Thorik invece è un difetto vero, e all'incontrario.** Il DM: *«non
ha ancora giocato la parte della resurrezione di Hella»*. Quindi `state.md` riga
76 non ha un'ambiguità: **registra come pagato un prezzo mai pagato** — *«−2 perm
CON sacrificed for Hella's resurrection (NEVER restored)»*. Oggi Thorik ha
**−4 DES e +2 COS**, e basta. È il vero «secondo tempo» del file, e sta sulla
scheda di un PG, non sul calendario.

### 4.5-ter · Le tre strade di Thorik esistono già, e il documento sa di essere sbilanciato

Il DM ha chiesto se esista un'alternativa migliore al −2 COS.
[`ARC07-DEF-3`](../07_il%20Portale%20Della%20Forgia%20Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md)
§5 ne ha **tre**, più il rifiuto, e la regola d'oro dice che *«la resurrezione
non è in ostaggio: col Cuore, Hella torna comunque. I sacrifici comprano la
qualità del ritorno»*.

| Strada | Costo | Peso vero a livello 13 |
|---|---|---|
| **Il Sangue della Stirpe** (base) | −2 COS permanente | −13 pf, −1 Tempra, **per sempre** |
| **La Memoria della Battaglia** | −3.000 PE | ≈ **23%** di un livello (13→14 costa 13.000 PE) |
| **Il Filo dell'Ascia** | Aegis Fang perde *Returning* fino al pieno risveglio | si sente **ogni round** di ARC-08, e finisce |
| Rifiuto | — | Hella senza RD 3/−; allo Step 5 servono 3 successi su 3 |

⚠️ **E il difetto che il DM ha visto è reale — il documento lo ammette da solo**,
con la nota *«il più pesante dei tre — cade sul PG più carico di artefatti»*.
Misurati accanto, gli altri due doni **non costano niente**: Tordek paga **−500
PE** (≈ 4% di un livello) e Artemis **uno slot per 24 h**.

🔴 **Quindi la sproporzione non si risolve alleggerendo Thorik.** Qualunque cosa
paghi lui, finché gli altri due pagano una cifra simbolica il tema del prezzo non
regge. Le due leve sono indipendenti, e vanno mosse insieme.

### 4.2-quater · Com'è andato 4c (2026-09-12)

**Il lotto ha trovato più di quel che cercava, e la parte in più era la peggiore.**
Cercava «i due tempi»; ha trovato **due costi registrati come pagati per una
scena mai giocata**.

#### Le cinque correzioni, e le sei righe non toccate

| Dove | Cosa diceva | Cosa dice adesso |
|---|---|---|
| §1 tabella party | i quattro PG **dopo Hammerfist**, in viaggio verso le quest dell'ARC-09 | **due colonne**: «adesso al tavolo» (Sala della Forgia, P4 chiuso) e «canone preparato». Nessun contenuto tolto |
| §1 riga Thorik | *«−2 perm CON sacrificed for Hella's resurrection (NEVER restored)»* | **−4 DES / +2 COS / +4 CAR**, e basta. Il costo del rito è marcato **non ancora versato** |
| §1 riga Hella | *«Full; Treant Hybrid template active post-resurrection»* | 🔴 **morta**, corpo nella Sala. Il template si assegna **al rito** |
| §7 debiti | Thorik *«he sacrificed 2 perm CON»* e Tordek *«500 XP sacrificed»*, al passato | *«non ancora contratto — si contrae al rito»* |
| §2.1 orologio | *«Day 19 (Terrelton just fell as Hammerfist ended)»* | il Giorno 19 è il **punto di sincronia** a cui il calendario tornerà, non un giorno trascorso (D3) |

🟢 **Le sei righe del changelog append-only che citano il «−2 COS» sono rimaste
intatte**: sono quel che i piani dicevano il 2026-07-02 e il 2026-07-23, e §8 di
`state.md` dice di sé *«never delete entries — they become campaign history»*.
La correzione si registra in coda, non si retrodata.

#### La riga che non si era sfasata, e perché conta

`state.md` §6 diceva già la verità sulla Collana dei Semi Eterni:
*«Hella (dead — resurrection pending) … Hella not yet resurrected»*. Due
sezioni dello stesso file, sullo stesso fatto, in due tempi diversi — e la
sezione **onesta** era quella degli artefatti, che nessuno legge per sapere chi
è vivo. 🔎 **Nessun cancello poteva vederlo**: entrambe le righe erano
sintatticamente perfette e i percorsi che citano esistono tutti.
`validate_docs` vede la deriva doc↔filesystem, non la deriva fra due frasi.

#### Il ridisegno dei Doni è **fuori dal master**, ed è voluto

Il DM ha chiesto di togliere il −2 COS, di rendere adeguati i doni di Tordek e
Artemis, e di **confrontare il nuovo col vecchio prima di approvare**. Il
risultato è [`PROPOSTA-DONI-RESURREZIONE-HELLA`](PROPOSTA-DONI-RESURREZIONE-HELLA.md),
🔵 **proposta**: `ARC07-DEF-3` §5 **non è stato toccato**.

Due cose che la misura ha aggiunto a §4.5-ter, e che spostano la diagnosi:

1. 🔴 **Il costo di Artemis non è «leggero»: non esiste.** *«1 slot invocazione
   alto per 24 h»* è vocabolario da incantatore preparato applicato a un
   **Warlock 13** (`state.md` §1), le cui invocazioni sono **a volontà**. Non è
   una sproporzione, è un errore di sistema: il rapporto fra il prezzo più alto
   e il più basso non è largo, è **indefinito** (∞ contro 0).
2. 🔴 **Il difetto vero non è il prezzo, è che le tre strade danno lo stesso
   dono.** Tutte e tre le strade di Thorik comprano `Pelle di Adamantio (RD
   3/−)`: non sono una scelta, sono un **listino**, e chi ragiona prende la più
   economica. Ne segue che **il −2 COS lo paga solo chi interpreta contro il
   proprio interesse** — il design mette una tassa sulla buona fede. Cambiare i
   numeri non lo toglie.

#### 🔁 v2 bocciata, v3 scritta (2026-09-12, stesso giorno)

Il DM ha letto la v2 e l'ha respinta su **tre punti, tutti fondati**:

| Il rilievo | Cos'era davvero |
|---|---|
| *«non hai proposto nulla né per Artemis né per Tordek che siano davvero adeguati»* | avevo tolto il −2 COS e **pareggiato verso il basso**: ad Artemis spegnevo quattro poteri 1/giorno **proteggendogli esplicitamente Ali d'Ombra e Passo d'Ombra**, cioè la roba buona; a Tordek prendevo `Ancoraggio` e `Salto Infuocato`, **due poteri periferici su quindici** |
| *«che conseguenze hanno per Hella, per i suoi poteri e per l'artefatto»* | 🔴 **nessuna, sull'artefatto.** I nove doni erano **abilità sciolte**. Non toccavano la **Collana dei Semi Eterni**, che ha tre semi e ha scritto dentro di sé che *«custodiscono i sacrifici che i compagni offrirono al rituale»*. Il gancio era nel repo e non l'avevo usato |
| *«per gli altri non deve essere gratis o facile»* | in v2 **due registri su tre erano temporanei**. Una rinuncia che scade non è una scelta |

🌱 **v3 cambia la domanda.** Da *«quanto sei disposto a pagare?»* a **«che pezzo
di te lasci crescere in lei?»**. Il dono è un **trapianto**: un potere lascia
l'artefatto del donatore **per sempre** e germoglia in un seme della Collana,
dove diventa druidico. Il party non perde la capacità — cambia mano e forma.

Tre gradi (**Scheggia** un potere giornaliero · **Ramo** un potere continuo ·
**Radice** la voce dell'artefatto o il suo futuro), **tutti permanenti**. Thorik
porta più peso in tre modi verificabili, e uno **lo dice `state.md`**: il
risveglio pieno di Aegis Fang richiede *«Corona Senziente»*, quindi il suo grado
III è l'unico che ricade su un **secondo** artefatto.

🌱 **E la v3 chiude un `[da definire col DM]` che non era suo**: il potere **#6**
della Collana (`I Doni dei Semi`) è marcato così da quando l'artefatto esiste.
§2.7 lo definisce **con le parole della scheda stessa** — *«restituire quel
sacrificio nel momento del bisogno»* — una volta sola, per una scena, e **decide
Hella**. È anche la riga che rende v3 etica invece che punitiva.

⚠️ **Quel che v3 peggiora, dichiarato**: tocca **quattro** schede-artefatto
invece di una; il grado III di Thorik implica una quest nuova per Aegis Fang; e
🔴 **il grado III di Artemis fa pagare una cosa che il giocatore non può
valutare** — «ciò che dorme nell'Anello», di cui non sa niente. Va avvertito in
privato o tolto: è l'unica riga della proposta che **non posso decidere io**.

#### 🐛 «Quali sono i poteri, e sono bilanciati?» — la domanda che ha trovato tre difetti

Il DM: *«mica l'hai detto, cosa decido se non li conosco. E un'altra cosa: sono
bilanciati?»*. Aveva ragione due volte, e verificare la seconda ne ha trovati
altri due.

1. 🔴 **La v3 non metteva mai in fila cosa ottiene Hella.** Descriveva i costi in
   prosa; la colonna che serve per decidere non c'era. → **§2.5-bis**, le otto
   strade su una pagina.
2. 🔴 **«Sono bilanciati?» non aveva risposta misurata**, e la risposta onesta è
   **«in parte»** → **§2.10**. Dentro ogni PG i gradi sono coerenti e la strada
   dominante di v1 non c'è, **ma non sono tre scelte pari**: sono un listino a
   tre prezzi con tre merci diverse. Il criterio **V1 diceva il contrario ed è
   stato corretto**.
3. 🐛 **Due errori miei**, trovati leggendo le schede invece di ricordarle:
   avevo scritto che i Bracieri sono *«l'unico artefatto del party che parla
   davvero»* — **falso, Aegis Fang è senziente Ego 14**; e «Il Richiamo del
   Legno» — richiamare **armi** a una **druida che non ne lancia** — era il dono
   peggiore delle otto. Sostituito con «Il Guardiano che Torna».
4. 🔴 **La collisione vera (§2.11)**: il grado II di Thorik **è già canone, ed è
   temporaneo**. Due schede-artefatto scrivono che col «Filo dell'Ascia» l'ascia
   perde il Ritornante *«fino al Risveglio pieno»*, e lo Stadio 1 è **«+4 Holy
   *Returning*»** — torna per progetto. Renderlo permanente contraddice la
   progressione dichiarata. Diventa la **domanda 0** di D13.

🔎 **La forma è quella di tutta questa campagna**: avevo *ricordato* le schede
invece di rileggerle, e due asserzioni su tre erano false. È ADR-0044 applicato
al contenuto invece che ai piani.

#### 🐛 E scrivendo D13, il gate delle decisioni ha mostrato un punto cieco

Ho scritto la riga nuova come `restato **verde a 12 decisioni**. Non l'ha rifiutata: l'ha **saltata in
silenzio**. `RIGA` pretendeva la cella dell'id esattamente `D13` o `~~D13~~`,
e con l'enfasi la riga non era più una decisione — era una riga di tabella
qualsiasi.

🔴 **È il modo peggiore in cui un gate può fallire**: non dà un errore da
correggere, dà un **conto plausibile**. L'aggregato risultava «allineato» e non
conteneva la decisione. È esattamente il difetto che ADR-0047 esiste per
impedire, nella forma in cui il gate non lo vedeva — e la seconda volta in due
lotti che un cancello di questa fase ha trovato una taratura sbagliata **sua**
(4b: gli 11 falsi positivi sui deploy dei convertitori, poi il proprio file di
test).

**Corretto**: la cella dell'id tollera enfasi e fregi, e il barrato si legge da
un gruppo suo invece che dal prefisso della stringa. Due test, **in coppia**
come per i backtick di 4b: uno prova che `**D1**`, `**D2** 🆕`, `_D3_` e
`~~**D4**~~` adesso contano; l'altro che allargarla **non ha spento il
controllo** — `vedi D2`, `D3-bis` e una cella vuota restano fuori. Il conto
è passato a **13 decisioni, 4 aperte**.

#### ⚠️ E un errore mio, che è costato lavoro

Provando che il gate mordesse ho modificato la riga di D13 nel piano e poi ho
rimesso a posto con `git checkout` — **su un file che conteneva tutto il lavoro
non committato di questo lotto**, che è sparito e ho dovuto riscrivere. Il
backup che avevo lanciato nella stessa riga di comando non era stato scritto,
e non me n'ero accorto perché ne avevo silenziato l'errore.

**Le due regole che ne restano**, e valgono oltre questo lotto: `git checkout`
su un file con lavoro non committato **non è un annulla**, è una perdita; e un
backup conta solo se se ne **verifica** la scrittura. La prova rifatta come si
deve — riga di D13 tolta, gate **rosso** con uscita 1, riga rimessa, gate verde
— è in §4.6.

### 4.2-quinquies · L'attuazione dei Doni (2026-09-12) — **D13 chiusa**

Il DM ha approvato la **v4-bis** con un'ultima taratura sua (**−1 CA invece di
−2** per Thorik) e ha detto di eseguire. Portato nel canone in **17 file**.

#### Cosa è entrato

| Chi | Dona — esce dall'artefatto **per sempre** | 🌱 Hella riceve |
|---|---|---|
| 🛡️ **Thorik** | il **+2 di deflessione** della Corona → **−1 CA permanente** | **Scudo del Custode** (1/g, immediata: prende il danno di un alleato entro 9 m **dimezzato**) + 🔄 **l'Eco del Custode** |
| ⚒️ **Tordek** | **Ancoraggio della Montagna** (2/g), dai Bracieri | **Pelle di Adamantio — RD 3/adamantino** |
| 🔮 **Artemis** | **1d6 di Eldritch Blast**, 7d6 → 6d6 | **Il Rovo Eldritch** — a volontà, 2d6 a 18 m |

🔄 **L'Eco del Custode è l'idea del DM, e chiude un anello**: quando Hella usa lo
Scudo, Thorik **scatta verso chi lei ha appena protetto**, accelerato 3 round. La
protezione data **torna al donatore, trasformata in velocità** — è il principio
del «seme restituisce», reso continuo e visibile a ogni scontro. E la direzione
*«verso la persona»* — sempre sua — è quel che lo rende **giocabile in una
frase** e **autotarato**: in 3.5 non si fa attacco completo dopo un movimento.

#### Le tre cose in più che il DM ha chiesto, e che non c'erano

1. ⚒️ **Le reazioni degli artefatti, positive *e* negative.** Non servivano premi
   né punizioni inventati: **tutti e quattro hanno già una personalità in
   scheda**. Aegis Fang (**Ego 14**, *«serve il popolo nanico prima del
   portatore»*) 🟢 smette di dubitare di Thorik o 🔴 **lo giudica**; i Bracieri
   🟢 lo avvertono un round prima o 🔴 **tacciono una settimana**; l'Anello
   🟢 si illumina di riflesso o 🔴 **si spegne 24 h**; la Corona 🟢 si scalda o
   🔴 arriva **fredda** al Rituale 4. **Tutte reversibili**: nessuna è un malus.
2. 🌱 **Le conseguenze su Hella e sul suo artefatto.** Ogni dono **germoglia in un
   seme**; un seme non donato resta **dormiente**; e il potere **#6** della
   Collana — marcato `[da definire col DM]` **da quando l'artefatto esiste** — ha
   finalmente una meccanica: **il seme restituisce** al donatore ciò che ha
   ricevuto, una volta sola, per una scena, **e decide Hella**.
3. 🧊 **L'archivio.** Dodici istantanee dei file com'erano prima, in
   `07_.../_ARCHIVIO/doni-v1-2026-09-12/`, ognuna col cartello «non è canone» e
   la direttiva d'esclusione, più un README che dice cosa è cambiato per file.
   ⚠️ **Col precedente contrario dichiarato**: a **D10** si scelse di *non*
   copiare i master modificati perché una copia crea **un secondo master**. Qui
   si è fatto lo stesso, su richiesta, e il presidio è **umano** — `validate_modules`
   esclude `_ARCHIVIO` per costruzione, quindi nessuno strumento verificherà mai
   quelle copie. È voluto: sono istantanee, devono restare ferme.

#### 🐛 Corollario: gli archivi non si indicizzano — e non vale per tutti i gate

**L'archivio ha rotto il bestiario nel momento stesso in cui è nato.** Le dodici
istantanee hanno fatto passare il catalogo mostri da **305 a 311 record** e reso
rosso `validate_bestiario` con un doppione di *«Battaglia Finale – Fase 0»*: è la
forma esatta del rischio che **D10** aveva dichiarato — *«una copia crea un
secondo master»* — comparsa al primo giro di archiviazione vera. Il DM ha chiesto
di chiuderla come corollario di questo lotto.

⚠️ **Ma la correzione giusta non è «escludere gli archivi ovunque»**, e questa è
la cosa che valeva la pena misurare. Su sette gate, la regola si divide in due:

| | Cosa fa il gate | Cosa deve fare con gli archivi |
|---|---|---|
| 🗂️ **chi indicizza** — `build_monster_catalog`, e per assicurazione `validate_bestiario` | costruisce un catalogo | 🔴 **saltarli**: una copia diventa un **record doppio** |
| 👁️ **chi sorveglia** — `validate_maps` | verifica che nessun master sfugga al controllo | 🟢 **includerli**, ed è **la decisione D1**: gli SVG furono lasciati in `_ARCHIVIO/` proprio *«così la cartella resta dentro il raggio di `validate_maps`»*. Escluderla **disferebbe una decisione del DM** |

Le cartelle d'archivio nel repo sono **due**, contate: `_ARCHIVIO` (44
occorrenze) e `Old` (11). `Old` era già nella lista del costruttore; `_ARCHIVIO`
no, ed è per questo che è successo.

🔴 **E provando a rovescio è emersa una cosa peggiore del difetto.** Tolta
l'esclusione dal costruttore, il catalogo si inquina di nuovo **ma
`validate_bestiario` resta verde**: confronta il catalogo committato con una
scansione fatta *dallo stesso costruttore*, quindi se entrambi i lati indicizzano
le copie *«in sync»* è vero e inutile. **La prima volta lo prese solo perché il
catalogo su disco era ancora quello pulito.** La rete vera è il test nuovo —
`scripts/tests/test_archivi_non_indicizzati.py`, **6 test** — e nella prova a
rovescio sono andati rossi i due che contano: quello sulla lista d'esclusione e
quello che cerca record da copie nel catalogo vero. Test totali: **691** (erano 685).

#### 🔎 Cosa ha trovato la verifica di coerenza

| | Trovato leggendo, non ricordando |
|---|---|
| 🐛 | **L'eco «Filo dell'Ascia» era canone in tre file** (scheda Aegis Fang, master DM, MATRICE) e **contraddiceva il profilo dello Stadio 1**, che è *«+4 Sacra **Ritornante**»*. Sostituito: il Ritornante **resta** |
| 🐛 | **Un eco dell'ARC-09 poggiava su *Timeless Body*** (`…FASE0-NOTTE-DEI-DROW`), dono che **nessuno versa più**. Riscritto sul dono vero: senza l'Ancoraggio di Tordek, Hella affronta i drow **di lama, a danno pieno** |
| 🐛 | **Due reference di skill** (`campaign-artifacts`, `campaign-party`) elencavano ancora i doni di v1 **come se fossero già stati pagati** |
| ✅ | **Verificato che la RD non si sovrappone**: Hella non ha RD di base, e la **Via della Guardia** (RD 2/−) **non è la strada che ha scelto** — ha preso la Via della Radice, il cui prezzo è la **vulnerabilità al fuoco ×1,5** che nessuno dei tre doni copre, per scelta del DM |
| ⚠️ | `dnd-35-srd/references/classes.md` cita *Timeless Body*: è la **capacità di classe del druido**, non il dono. **Non toccato** |

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

**Fatto in 4c (2026-09-12)**, e i cancelli si provano **a rovescio**, come da
inizio campagna:

| Prova | Esito |
|---|---|
| `pytest scripts/tests -q` | ✅ **685 passati**, 5 saltati, 2.095 sotto-test (erano 683: +2 sul gate delle decisioni) |
| `validate_docs.py` · `--sorgenti` | ✅ 3 documenti · ✅ **704 documenti**, nessun percorso inesistente né assoluto |
| `decisioni_dm.py --check` | ✅ **13 decisioni, 4 aperte**, aggregato allineato |
| `check_plans_discipline.py` · `tools_manifest.py --check` · `validate_maps.py` | ✅ · ✅ 59 tool · ✅ |
| 🔴 **il gate morde**: riga di D13 **tolta** dal piano | ✅ `decisioni_dm --check` **rosso, uscita 1**; riga rimessa → verde |
| 🔴 **il gate morde**: D13 **aggiunta e non emessa** | ✅ rosso al primo `--check`, verde dopo `--emit` |
| 🔴 **la regex allargata non ha spento il controllo** | ✅ `vedi D2`, `D3-bis` e una cella vuota **restano fuori** (test in coppia) |
| `git diff --stat` | ✅ nessun `.svg`, `.png`, `.uvtt` toccato: 4c non rigenera artefatti |

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
| D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM **con Gemini** il 2026-08-15, montati nel modulo, `validate_standalone` verde. `comfyui_batch --lista` dava «6 da fare» per un **disallineamento di nomi**, corretto in questo lotto. La domanda vera è: **l'arte del Drappo è di Gemini, la catena di F3 genera con SDXL in locale — quale delle due è il canone del modulo?** Le differenze che contano (ADR-0019 §2, che questo caso l'aveva previsto): Gemini **non espone il seed**, quindi la serie è irripetibile e il PNG è la sorgente; i suoi termini sono un **contratto che cambia**, verificato per di più su fonti secondarie; SDXL è OpenRAIL++-M, **perpetua**. Di contro la provenienza di Gemini è **firmata C2PA**, e SDXL su queste immagini **nessuno l'ha visto**. 🔵 **Metodo scelto dal DM il 2026-09-11: collaudo prima di scegliere** — la decisione **resta aperta**, si chiude quando il DM ha visto il confronto. Il DM: *«voglio fare prima un collaudo con 2 o 3 immagini e vedere davvero la qualità prima di buttare quelle di Gemini, che sono carine»*. Si generano **due o tre** immagini con SDXL in una cartella a parte, si mettono accanto alle attuali, e A (tenere Gemini) o B (rigenerare tutto) si sceglie **guardando**. Il collaudo chiude anche il buco vero di F3 — la catena mai provata contro un ComfyUI reale — al costo di due immagini invece che diciotto |
| ~~D3~~ | F4 · 4c | ✅ **chiusa il 2026-09-12, eseguita nello stesso commit in cui e' stata dichiarata chiusa** (la lezione di D4). Il DM ha risposto il 2026-09-11 e il lotto 4c ha applicato entrambe le risposte: il **Giorno di Marcia 19** e' il punto di sincronia a cui il calendario torna col viaggio nel tempo — non un difetto, un tempo verbale, corretto; il **-2 COS di Thorik** era registrato come versato per una scena mai giocata, tolto dal presente insieme ai **-500 PE di Tordek**, che avevano lo stesso difetto e che nessuno aveva notato. 🔎 **E il lotto ha trovato il resto della stessa crepa**: §1 collocava tutti e quattro i PG dopo Hammerfist e dava **Hella viva**, mentre §6 dello stesso file la dava *«dead — resurrection pending»*. Vedi **§4.2-quater** |
| ~~D13~~ | F4 · 4c | ✅ **DECISA E ATTUATA il 2026-09-12, nello stesso commit.** Il DM ha approvato la **v4-bis**, con l'ultima taratura sua: **−1 CA invece di −2** per Thorik. 🛡️ **Thorik** dona il **+2 di deflessione della Corona** → **Scudo del Custode** (1/g, immediata: Hella prende il danno di un alleato entro 9 m **dimezzato**) + **l'Eco del Custode**, che e' l'idea del DM: quando lei scuda qualcuno **lui e' accelerato 3 round e si muove verso chi e' stato protetto** — l'anello si chiude, la protezione data torna al donatore trasformata in velocita'. ⚒️ **Tordek** dona **Ancoraggio della Montagna** → **Pelle di Adamantio RD 3/adamantino**. 🔮 **Artemis** dona **1d6 di Eldritch Blast** (7d6 → 6d6) → **Rovo Eldritch** a volonta': il DM ha visto che il dono precedente **si sovrapponeva** a quello di Thorik (stessa casella, dare tempo a un altro). ⚒️ **Reazioni degli artefatti al dono e al rifiuto**, tutte reversibili e tutte fondate sulla personalita' gia' in scheda. 🌱 **E il potere #6 della Collana non e' piu' `[da definire col DM]`**: il seme **restituisce** al donatore, una volta sola, e decide Hella. **Attuato in 17 file** + **12 istantanee** in `_ARCHIVIO/doni-v1-2026-09-12/`. Vedi **§4.2-quinquies** |
| ~~D4~~ | F4 | ✅ **chiusa il 2026-09-11: non era una domanda.** Misurato invece di ricordare: il `PALIO-BOOKLET` cita **14 file** — 8 stemmi, 4 mappe, 2 immagini — ed **esistono tutti e 14**. SVG veri da 2,7-5,4 KB, due PNG da ~2 MB, e `CREDITS.md` con l'attribuzione **CC BY 3.0** a game-icons.net già in regola. Niente da produrre, niente da togliere. 🔎 Settimo presupposto invecchiato di questa campagna, e la chiusura era rimasta indietro di un giro: annunciata il 2026-09-11 e non eseguita nello stesso commit |
| D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un **AP originale autonomo**, mai un'espansione di RHoD, e porta il **perimetro della v1**. ✅ **I due avvertimenti che bloccavano la domanda sono tolti**: l'audit mancante è stato **rifatto da zero** ([`AUDIT-DERIVAZIONE-IP-CAMPAGNA`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md)), e la tesi **regge sul repo di oggi** — archi 07+08 a **0,2** e **0,7** occorrenze RHoD per 1.000 parole contro il **5,6** dell'arco 09. 🔎 **E la misura ha aggiunto due cose che la #72 non sapeva**: il **`Bestiario/` è a 3,0** e **esce col modulo** — un perimetro che tace su di lui lascia fuori il conto una dipendenza vera — e i **moduli autoconclusivi sono già puliti** (`10-stand-alone` e il Drappo a **0,0**), quindi su quest'asse il prodotto della linea 3 di `PIANO-VENDIBILITA` è pronto. 🔴 **Cosa resta da decidere al DM**: (a) si adotta il perimetro così com'è? (b) il **bestiario** sta dentro o fuori? (c) l'ADR resta proposta finché non c'è la **verifica di un avvocato IP**, che l'audit non sostituisce — conta i nomi, non la struttura |
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
| 🆕 **I salti di titolo nei booklet** — `HB_TAGS` emette un `#####` sotto un `#`: veraPDF lo rifiuta (PDF/UA 7.4.2-1), e due booklet **non sono committabili** finché non si corregge. Trovato chiudendo E1; il test che lo prende guarda **solo** `10-stand-alone/` | `build_booklet_html.py` | C |
| ~~**I 51 link rotti nei booklet generati**~~ | ✅ **chiuso 2026-09-12, lotto E1** (§4.7). Erano **44**, non 51 — nono presupposto invecchiato — e non erano un difetto solo: **41 di profondità** nel generatore, **3 falsi positivi** del validatore. Adesso **0** | C |
| **4e** una sola via di scrittura · **4f** prodotto e partita | §4.2, dipendono da 4d | C |
| **`validate_prosa`: 161 rilievi in 340 file** (non bloccante). ⚠️ Il piano diceva «13»: era una misura vecchia e di un altro validatore | `scripts/validate_prosa.py` | M |

### 4.7 · Lotto **E1** — i link dei booklet generati `[✅ chiuso 2026-09-12]`

`[C costruzione · Opus 5 · medio · l'insieme si conta con
`git ls-files -z '*.hb.md'` → **34 artefatti**, e il criterio d'uscita è
**0 link rotti** su tutti e 34, non solo sugli 8 di oggi]`

#### FASE 1 — Audit, e la stima era vecchia un'altra volta

🔎 Il piano diceva **«51 link rotti su 51»**. Rimisurati oggi: **44 su 34
artefatti**, concentrati in **8 file**. **Nono presupposto invecchiato** di
questa campagna.

| File | Link rotti |
|---|---|
| `DRAPPO-BOOKLET-DM.hb.md` | 14 |
| `PALIO-BOOKLET.hb.md` | 13 |
| `DRAPPO-BOOKLET-GIOCATORI` · `DRAPPO-FASCICOLO-SCHEDE` | 6 + 6 |
| `ARC07-SESSIONE-TERROS-BOOKLET` | 2 |
| `ARC07-BOOKLET-FASCICOLO-1` · `PALIO-BOOKLET-FASCICOLO-P2D` · `recap-2026-05-05` | 1 ciascuno |

**E non è un difetto solo, sono due.** Classificati uno per uno:

| N | Classe | Cos'è |
|---|---|---|
| **41** | 🔴 **profondità** | il difetto vero. Il sorgente sta in `07_il Portale…/X.md`, dove `../plans/adr/…` risolve **giusto** sulla radice del repo; il generatore lo copia in `07_il Portale…/homebrew/sessione-terros/`, cioè **due livelli più in basso**, e il link diventa `…/homebrew/plans/adr/…`, che non esiste |
| **3** | 🟡 ~~segnaposto `URL`~~ → 🔴 **falso positivo del validatore** | 🔎 **La classificazione di questa riga era sbagliata, e l'ha smentita il lavoro stesso.** Non sono buchi di contenuto: sono `![bg](URL)` scritti **dentro un commento HTML** che spiega al DM la sintassi da usare. Un commento non viene reso da nessun lettore markdown, quindi **non può contenere un riferimento vivo**. È la **terza famiglia di falsi positivi** di questo gate, e ha la stessa forma delle due di 4b |

⚠️ **Il difetto è nel generatore, non negli artefatti**: `build_booklet_html.py`
e `hype_homebrew.py` **concatenano il markdown sorgente alla lettera**, senza
riscalare i link relativi alla profondità del file che producono.

#### FASE 2 — Sviluppo

1. **Un solo posto**: `dmcore/testo.py` — è già la casa delle trasformazioni di
   stringhe condivise, e nacque per lo stesso motivo (sette `slug` divergenti).
   Nuova funzione che, dato il testo, la cartella del **sorgente** e quella
   della **destinazione**, riscrive ogni link **relativo** perché continui a
   puntare allo stesso file.
2. **Cosa non si tocca**, ed è la parte che decide se la correzione è sicura:
   URL assoluti (`http`, `https`, `mailto`), àncore (`#…`), percorsi assoluti
   (`/…`) e i segnaposto tipo `URL` — un segnaposto **non si inventa**, resta
   rotto e si conta a parte.
3. **I due generatori** la chiamano nel punto in cui incorporano un sorgente.
4. **Gli 8 artefatti si rigenerano**, non si correggono a mano.

#### FASE 3 — Validazione

| Prova | Criterio |
|---|---|
| il gate morde **a rovescio** | un link relativo giusto nel sorgente, dopo la copia in una cartella più profonda, deve risultare **rotto** senza la correzione e **sano** con |
| non spegne niente | URL assoluti, àncore e percorsi assoluti **non si toccano**: test in coppia |
| sul repo vero | `validate_docs` sui 34 `.hb.md` → **0 link rotti**, tranne i 3 segnaposto `URL`, che restano **contati e dichiarati** |
| rigenerazione | il `.hb.md` rigenerato differisce dal committato **solo nei link** |

#### Com'è andata — **44 → 0**

| | |
|---|---|
| **41 di profondità** | corretti **nel generatore**: `dmcore/testo.py` ha `riscala_link`, e i due generatori la chiamano nel punto in cui incorporano un sorgente. Gli **8 artefatti rigenerati dai manifest**, non corretti a mano |
| **3 nei commenti** | corretti **nel validatore**: `senza_commenti_html` svuota i commenti prima di cercare i link, come `senza_code_span` fa coi backtick |

✅ **Il diff della rigenerazione è pulito**: **48 righe cambiate, tutte con un
link dentro**, zero effetti collaterali su 5 file. Era il criterio di §Fase 3 e
regge.

✅ **Le prove a rovescio**, tutte e due fatte togliendo la correzione:
· senza `riscala_link` il booklet rigenerato torna rotto e
`test_nessun_link_rotto_nei_booklet` va **rosso**;
· i test dei commenti HTML sono **in coppia** — quattro provano che un link
dentro un commento non conta, due che fuori conta ancora e che i **numeri di
riga restano veri**.

⚠️ **E una verifica che valeva la pena fare**: le direttive
`<!-- validate-docs: ignore -->` **sono anch'esse commenti**. Svuotarli
nell'estrattore dei link non le rende cieche, perché `ignored_lines` legge il
**testo grezzo** — e adesso c'è un test che lo dice.

**Test: 691 → 710** (+13 sul riscalatore, +6 sui commenti HTML).

#### 🐛 E rigenerando è caduto fuori un difetto che non c'entrava

Il primo giro ho rigenerato **tutti** i manifest, non solo i cinque che
servivano, e sono comparsi **due `.hb.md` mai tracciati** — l'abbazia di
`10-stand-alone/` e le schede PG del Drappo. Quello dell'abbazia ha fatto
**rosso `test_tipografia`**: i suoi quattro `⚠ SOLO DM` sono `#####` messi
subito dopo un `#`, cioè un **salto di titolo da 1 a 5** — quel che veraPDF
rifiuta in PDF/UA 7.4.2-1, e per cui quel test esiste.

⚠️ **I due file sono stati tolti**: non erano nel perimetro del lotto, e
committarli avrebbe allargato il lavoro di due artefatti nuovi per un effetto
collaterale. Ma il difetto **è vero e resta**: `HB_TAGS` in
`build_booklet_html.py` emette un livello 5 sotto un livello 1, quindi **quei
due booklet oggi non sono committabili**. → lotto suo, non E1.

🔎 Il test scandisce **solo** `10-stand-alone/`: gli altri booklet hanno lo
stesso salto e nessuno li guarda. È la forma di ADR-0041 — un controllo che
esiste su una cartella sola.

🔴 **Il limite dichiarato**: i `.hb.md` si incollano in Homebrewery, dove un
link relativo **non risolve comunque**. Questa correzione serve a chi li legge
**nel repo o su GitHub**, non al brew. Sistemarli è giusto lo stesso — un link
rotto è un link rotto — ma non aspettarsi che cambi qualcosa al tavolo.

### Il lavoro fermo su una tua decisione

| Cosa | Aspetta | Perché non posso deciderlo io |
|---|---|---|
| **3d** — il collaudo e il confronto (non più i diciotto: ci sono già) | **D2** | serve la tua macchina, e il giudizio è tuo: guardare due immagini SDXL accanto alle Gemini e dire quale resta canone |
| ~~**4c**~~ | ~~D3~~ | ✅ **fatto il 2026-09-12** |
| **I Tre Doni v2** — approvare, ridurre al minimo di §5.4, o restare a v1 | **D13** | è canone e regolamento insieme: quanto deve costare un dono al *tuo* tavolo lo sai solo tu, e una delle tre domande (*si gioca il danno alle caratteristiche?*) decide se metà della proposta regge |
| I 13 stemmi e mappe del `PALIO-BOOKLET` | **D4** | si producono o si tolgono i riferimenti: è una scelta di prodotto |
| Recuperare l'ADR ex-0018 della #72 | **D11** | ed è una *proposta* con gate legale, non una decisione tecnica |
| **4d** `state.yaml` · **4g** schede PG a dati · **4h** `groups/<slug>/` | 4c prima | K e G: si prendono uno alla volta, e 4h vuole una PR dedicata |

### Le PR: da sei a due (chiuse il 2026-09-11)

Il rischio da cui questa ripresa è partita — *«non vorrei piani e PR che si
sovrappongono o che sono parzialmente obsolete ma che per sbaglio le mergio»* —
**non è più aperto**. Tre PR il cui contenuto era già su `main` sono state
chiuse su decisione del DM, ognuna con la sua motivazione scritta nel thread.

| PR | Esito | Perché |
|---|---|---|
| ~~#63~~ | 🔒 **chiusa** | contenuto portato dalla F1 (1a-1d). Mergiarla avrebbe riportato indietro 11 SVG rigenerati e tre file di puntamento già fusi a tre vie |
| ~~#52~~ | 🔒 **chiusa** | contenuto portato dalla F2 (2a-2c): le direttive `@` girano su tre master scritti a mano |
| ~~#67~~ | 🔒 **chiusa, superata** | l'oggetto esiste su `main` dal 31 luglio come booklet da manifest, e la versione della PR **detta tattica al giocatore** — contraria alla norma di oggi, non solo vecchia |
| **#106** | 🟡 aperta | resta **solo** per 3d, che aspetta **D2**. Tutto il resto della catena raster è su `main` |
| **#99** | 🟡 aperta | segnaposto della F4: 4a e 4b sono dentro, da 4c in poi no |

⚠️ **Le due che restano non vanno mergiate**: sono segnaposto di lavoro che
manca, non rami da integrare. Si chiuderanno quando l'ultimo lotto che le
riguarda sarà su `main` — 3d per la #106, 4h per la #99.

### Cosa manca per dire che questa revisione è finita (agg. 2026-09-11)

Le decisioni aperte sono scese **da 8 a 5**, e la forma del residuo è cambiata:
**quasi tutto quel che resta aspetta il DM**, non la macchina.

| | Cosa | Chi | Stato |
|---|---|---|---|
| 1 | **3d** — il collaudo di 2-3 immagini SDXL accanto a quelle di Gemini, poi la #106 si chiude | DM (**D2**) | 🟡 metodo scelto, **rimandato dal DM** |
| 2 | ~~**4c**~~ — i due tempi di `state.md` | — | ✅ **chiuso 2026-09-12** (§4.2-quater). Sblocca **4d · 4g · 4h** |
| 2-bis | **D13** — i Tre Doni v2: approvare, ridurre al minimo, o restare a v1 | DM | 🔵 **decidibile**: la proposta e il confronto sono scritti, il master **non** è stato toccato |
| 3 | **D11** — il perimetro dell'AP originale, e se il **bestiario** ci sta dentro | DM | 🟢 **decidibile**: l'audit che mancava è stato rifatto |
| 4 | **D12** — la riga `17` duplicata nell'arena circolare di `L2` | DM | 🟢 piccola, ma indovinarla sposterebbe celle |
| 5 | **4d → 4h** — il canone come dato, uno alla volta; poi la #99 si chiude | macchina | 🟢 **sbloccati**: il 2 è chiuso |
| 6 | Le code dichiarate: attuazione di **ADR-0048**, i **51 link** dei booklet generati, i **161 rilievi** di prosa | macchina, quando si vuole | ⬜ |

✅ **Chiuse dall'ultima revisione di questa sezione**: D4 (era morta — gli
allegati del Palio esistono tutti), D7, D8, D9 e D10.

🔴 **Il collo di bottiglia non è cambiato: sono le decisioni.** Le voci 1-4 non
hanno alcun ostacolo tecnico. La 5 dipende dalla 2. Solo la 6 è libera da subito,
ed è la meno importante.

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
