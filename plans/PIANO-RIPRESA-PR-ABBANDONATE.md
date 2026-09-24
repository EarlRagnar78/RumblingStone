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
> | **4d** ✅ `state.yaml` (ADR-0017) | **K** canone | `[**Opus 5** · xhigh-max · `state.md` **rigenerato è identico** a quello committato]` — **chiuso 2026-09-16/17 (4d-1 … 4d-8), riverificato il 2026-09-24** (§4.9.0) |
> | **4e** ✅ una sola via di scrittura | **C** costruzione | `[Sonnet 5 · alto · un test **sui file veri**, non su fixture — vedi §4.4]` — **chiuso 2026-09-24** (§4.9): il front-matter coi delta, 8 mutazioni su 8 rosse |
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
| 4a | **G2** — `validate_docs.py` | gate bloccante sulla deriva doc↔realtà | **Indipendente da tutto.** Chiude un difetto reale: `AGENTS.md` documentava `campaign/npcs/`, `locations/`, `encounters/` — **nessuna delle tre è mai esistita**. Ed è progettato attorno ai falsi positivi: alla prima esecuzione **9 hit di cui 4 falsi**, corretti nel validatore e non nei documenti <!-- validate-docs: ignore --> |
| 4b | **G3** — link, path locali e un ADR | **22 difetti veri** (la stima «18 su 241» era di un mese prima e sbagliata in tutte le cifre) · 7 file con path dentro un checkout personale | ⚠️ **non era igiene pura**: uno dei link rotti citava una decisione mai registrata, e recuperarla ha reso il lotto **K** |
| 4c ✅ | **G1** — i due tempi di `state.md` | §1 collocava i PG **dopo Hammerfist** mentre §0 marca l'arco 08 `⬜ NON giocato` | ⚠️ tocca il canone, ma **non cancella niente: etichetta**. Chiuso il 2026-09-12 — vedi **§4.2-quater**: due costi risultavano **versati senza essere stati giocati**, e il ridisegno dei Doni che ne è nato è una **proposta separata**, non canone |
| 4d | **G2-bis** — ADR-0017, `state.yaml` | i fatti come dati, `state.md` **generato** | il pezzo grosso. Vedi 4.3 |
| 4e | **G2-ter** — una sola via di scrittura | clock villain, «chi sa cosa», numeri di Rethmar migrati a dati; il log di sessione prende un front-matter coi delta | dipende da 4d |
| 4f | **G2-quater** — prodotto e partita | il reset per gruppo nuovo **perdeva**: azzerava `state.md` e `sessions/` e lasciava `state.yaml`, `state-changelog.md`, `campaign-history.md` e i recap al gruppo dopo | dipende da 4d/4e |
| 4g | schede PG a dati | `PG/schede/*.yaml` + `.md` generati | oggi le schede PG **non esistono come dato** da nessuna parte |
| 4h | ADR-0018 — `groups/<slug>/` | multi-gruppo per directory invece che per branch | **PR dedicata**, come dice la #99 stessa |
| 4i | **G3-bis** — rimandi fra backtick e contenuti rimasti nei rami | il gate vede i percorsi citati fra backtick in tutti i sorgenti; un registro dà un posto a ogni file che esiste in un ramo e mai su `main` | richiesto dal DM il 2026-09-24, indipendente da 4f-4…4h. Vedi §4.11 |

### 4.2-bis · Com'è andato 4a (2026-09-07)

Portato `validate_docs.py` dalla #99 e giudicato **sul repo di oggi**, un mese
dopo che è stato scritto: trova **sei percorsi citati e inesistenti**, e li ho
verificati uno per uno prima di toccare i documenti — **nessun falso positivo**.

| Dove | Cosa asseriva |
|---|---|
| `AGENTS.md` 24-26 | l'albero di `campaign/` elencava `npcs/`, `locations/`, `encounters/` |
| `AGENTS.md` 161-162 | convenzioni di nome per due di quelle cartelle |
| `AGENTS.md` 210 | `campaign/lore/rhod-adaptations.md`, che non esiste in nessun posto <!-- validate-docs: ignore --> |
| `AGENTS.md` 225 | *«Check `campaign/npcs/` before describing NPCs»* <!-- validate-docs: ignore --> |
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
(`scripts/lint_map_design.py`) **non è mai stato scritto**, e l'audit che ne <!-- validate-docs: ignore -->
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
| ~~D14~~ | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM: *«la riga va in state.yml e poi riportata in state.md»*. Misurata, la risposta regge: la tabella dei waypoint è **dato puro** (10 righe) e il March Day è **un campo** (`march_clock.giorno_corrente`); il paragrafo di cinque righe che spiega perché il Giorno 19 è un bersaglio e non un passato resta **prosa, sotto e fuori** dalla regione generata. Separati, la macchina riscrive la sua riga a ogni sessione senza mai toccare la nota del DM — che era il nodo. ⚠️ La regione `auto:march-clock` **sparisce**, e marcarla oggi sarebbe *peggio* di prima: una regione dentro una `gen:state:` sono due scrittori sullo stesso testo. Sparisce anche `RETHMAR_DAY = 42`, cablato in `state_apply`: era la seconda fonte di verità più piccola del repo, e sopravviveva perché nessuno aveva mai eseguito il tool. Vedi **§4.8.9** e [ADR-0052](adr/ADR-0052-cosa-e-dato-e-cosa-e-prosa.md) |
| ~~D16~~ | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM ha scelto l'enumerazione **con il compagno**: `attivo · latitante · neutralizzato · morto · ignoto`, più `reversibile`. ⚒️ `neutralizzato` copre il caso più frequente al tavolo — sconfitto ma non morto — e senza di lui il DM dovrebbe scrivere `morto` per non scrivere `attivo`. 🔴 **E `reversibile` è la metà che conta**: in questa campagna un morto torna (il Ghostlord nasce da un morto, Sal è protetto da un paradosso auto-consistente, Hella è morta in attesa del rito), quindi registrare «morto» senza dire se è definitivo è registrare **meno di quel che il canone sa**. La regola **R9** lo pretende. ⚠️ `state_apply` scrive `stato` ma **non** `reversibile`: il primo è la lettura letterale del log, il secondo è una decisione narrativa, e R9 la chiede al DM alla prima esecuzione — provato sul canone vero. 🔎 **§4 conoscenze è stata esclusa dopo averla misurata**, benché il DM avesse chiesto di includerla: tre righe non sono persone e tre persone compaiono sotto due nomi, quindi `stato` lì vorrebbe dire un valore privo di senso in tre casi e due copie divergenti in altri tre. Va nell'anagrafica del lotto della chiave. Vedi **§4.8.9** |
| ~~D17~~ | F4 · 4d-4 | ✅ **CHIUSA il 2026-09-17 — e la domanda aveva una premessa falsa, trovata dal DM.** Era posta come «i due villain senza scheda: si scrivono, si contano o escono da §3?». 🐛 **Tre delle quattro voci che avevo dichiarato senza scheda ce l'avevano.** Il DM: *«controlla bene negli archi o nel bestiario se c'è qualcosa magari annegato come prosa»*. **Zalkatar** ha uno statblocco a **GS 13** (14d4+70, CA 24) in `09_…/P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md`; **Saarvith + Regiarix** ne hanno uno a **GS 13** in `09_…/P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md`, e il file `FASE4` accanto dichiara esplicitamente *«le statistiche sono lì; questo è la regia dello scontro»*; il **Cerchio Druidico** ne ha uno in `Bestiario/mostri/cerchio-druid7-cr7.md`, marcato [ACCEPTED — DM-canon 2026-05-05]. L'errore non è stato non trovarle: ho cercato **solo dentro `Bestiario/`**, e allargando la ricerca ho **troncato l'output a sei righe** concludendo da una lista tagliata. ✅ Non c'era niente da scrivere né da togliere: c'era da **cercare meglio**. Resta **un** buco su 28 (`lathander-mask`), ed è corretto. ⚠️ **Conseguenza di progetto**: una scheda non vive per forza nel `Bestiario/`, e un cancello tarato lì avrebbe continuato a dare per mancanti due boss da GS 13. Nasce **R13**, che mette alla prova ogni buco dichiarato contro tutto il repo. Vedi **§4.8.10** e [ADR-0053](adr/ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) |\n| ~~D6~~ | F1 | ✅ **decisa 2026-09-04: ridisegnata.** `…P1C` mappa 3 dichiarava 40×40 e aveva righe da 24 a 26 celle: rifatta **26×29**, nessuna coordinata del testo cambiata |
| ~~D18~~ | F4 · 4d-6 | ✅ **DECISA E ATTUATA il 2026-09-17, nello stesso commit.** Il DM: *«spezzarli per intestazione verificando che non esistano già»*. Il catalogo portava **19 record intitolati al documento** invece che alla creatura, perché `build_monster_catalog.py` faceva **un record per file** e prendeva il primo GS: «Parte 2A – Torre Invisibile», GS 10. **19 → 8**, pool **372 → 397**. 🔎 Quel che ne è uscito non sono comparse: gli **otto fantini del Palio**, i **Sicari di Sonjak**, il Gonfaloniere Aldemar Vosk, la Drow Chierica di Lolth, gli esempi d'onda di Rethmar — tutti chiusi dentro un record solo. ⚠️ **La deduplica è ancorata a un fatto dichiarato**: si confrontano i nomi **solo** dentro l'insieme delle voci del Bestiario che citano *quel* documento come `Source`. È il modo di rispettare ADR-0053 (un matcher permissivo traveste l'ignoranza) senza rinunciare a dedurre: il legame documento↔voce l'ha scritto qualcuno, la somiglianza sceglie solo *quale* voce sta per *quale* intestazione. 🔴 **E il rischio opposto ha il suo presidio**: il record di file sparisce solo quando **ogni** creatura che il documento nomina ha già la sua voce — gli otto che restano sono quelli dove non è vero, e toglierli significherebbe meno rumore e **meno creature**. 🐛 Due difetti nei nomi generati, trovati misurando: la numerazione del Palio è **multi-livello** (`### 3.2 Drow Chierica`) e lasciava nomi che cominciavano per cifra, e la coda tagliata lasciava parentesi mai chiuse («Aldemar Vosk (LN»). 🔎 **E il cancello nuovo ha trovato un errore mio al primo giro**: contava **due** «Skullcrusher il Nero», perché la voce che avevo appena scritto puntava al file che il drago lo *nomina* soltanto — i numeri stanno in `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`. Correggendo il puntamento è poi caduto fuori che `P6-INTEGRAZIONE` restava scoperto, e dentro c'erano **Re Thorek I** (Grr 16, il re di mille anni prima che si inginocchia davanti alla Corona) e **Durin Hammerfist**, l'antenato di Othrek: due PNG di canone che non aveva nessuno. Vedi **§4.8.12** e [ADR-0054](adr/ADR-0054-un-archivio-non-e-una-copia.md) |
| ~~D19~~ | F4 · 4f | ✅ **Risposta del DM il 2026-09-24, ed è un principio più largo della domanda**: *«la procedura dovrebbe essere quanto più automatizzata possibile: un DM normalmente non tocca affatto i file yml, al massimo se ha un'interfaccia scrive dei campi o seleziona i valori da un form già impostato»*. Quindi né lo scheletro da compilare né il derivato da rivedere a mano: il template è **derivato in automatico** dal prodotto, e ciò che resta di giudizio passa da un **modulo** a scelte. Procedura in §4.10.6, il via è **D21** |
| D21 | F4 · 4f | **Si procede come in §4.10.6?** Il gruppo nuovo parte con un comando solo e un modulo a campi e scelte. Le proposte di fine sessione che oggi dicono «scrivi in `state.yaml`» diventano domande dello stesso modulo. Le risposte stanno in un JSON, e il modulo è solo la sua faccia: oggi il terminale, domani una pagina, senza toccare la logica. 🔵 Proposta: sì, con prima 4f-4 (il gruppo nuovo) e poi 4f-5 (le proposte di fine sessione), ognuno col suo commit |
| D22 | F4 · 4i | **Cosa si fa dei file rimasti nei rami senza un posto?** Misurati in §4.11.2. Per ognuno si può **portarlo** su `main` com'era, datato; **dichiararlo superato**, scrivendo da cosa; **lasciarlo** nel ramo, scrivendo perché. Il caso che pesa è il `SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05` della #72: 773 righe sulla catena degli archi 01-05, sei revisioni con risposte del DM, e nessun documento su `main` lo nomina. La proposta è portarlo com'era in `campaign/lore/`, come per l'audit di level design. Per `agents.conf` la proposta è rifarlo sul codice di oggi, perché la matrice duplicata c'è ancora |
| D23 | F4 · 4i | **Si attiva su `main` la protezione «Require branches to be up to date before merging»?** È l'unico pezzo della regola che hai chiesto di valutare (§4.11.4) che non sta nel repo: la CI di una PR gira sul `main` del momento del push, e se `main` cambia dopo la PR resta verde su una base che non c'è più. Con la protezione, prima del merge GitHub chiede di riallineare la PR e la CI rigira. Costo: un clic su «Update branch» prima di ogni merge, e un giro di CI in più. Si attiva in *Settings → Branches* del repository; da qui non si può né attivare né verificare |
| ~~D20~~ | F4 · 4f-2 | ✅ **DECISA E ATTUATA il 2026-09-24, nello stesso commit.** Il DM: *«D20 ok ma non tralasciare nulla»*. Split per sezione come in §4.10.4: **528 righe su 528** ritrovate nelle due metà (controllate contro git da un test), nessuna duplicata, una sola parola spostata («ESCAPED», che la cronaca racconta già tre volte). Tredici rimandi aggiornati in undici file; restano sul nome vecchio i documenti datati (`plans/`, l'audit IP, la baseline del 21 settembre), come registro di quando sono stati scritti |

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
| ~~**4e** una sola via di scrittura~~ ✅ chiuso 2026-09-24 (§4.9) · **4f** prodotto e partita | §4.2, dipendono da 4d | C |
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

### 4.8 · Lotto **4d** — `state.yaml` `[4d-1 ✅ · 4d-2 ✅ — chiusi il 2026-09-16]`

> `[K canone · Opus 5 · xhigh · `python3 scripts/render_state.py --check` esce 0:
> `state.md` **rigenerato è byte-identico** a quello committato]`

#### 4.8.0 · Informazioni mancanti e assunzioni

**Cosa non so, e come procedo**

1. **Non so se i fatti in `state.md` siano veri.** Lo schema vincola la forma;
   la verità la sa il DM. → **assunzione**: `state.md` di oggi è la verità di
   riferimento, e il lotto la trasferisce senza giudicarla. È anche il motivo
   per cui il criterio d'uscita è la **byte-identità** e non «sembra giusto».
2. **Non so se le §5 e §7 debbano diventare dati.** Le otto regioni del
   generatore della #99 non le coprono. → **assunzione**: restano prosa, e il
   lotto lo **dichiara** invece di lasciarlo scoprire a qualcuno fra sei mesi.

**Assunzioni di progetto**

3. **I dati NON si recuperano dal ramo.** Vedi §4.8.1: sono una fotografia del
   10 agosto. Si recupera la **macchina**; `state.yaml` si scrive da
   `state.md` di **oggi**.
4. **Il lotto si spezza in due**, e non è prudenza generica: **4d-1** non tocca
   la via di scrittura del canone, **4d-2** sì — e su quella la #99 ha già
   registrato una regressione propria.

#### 4.8.1 · Audit: il ramo #99 è **384 commit indietro**, ed è il fatto che decide tutto

| Cosa | Misura sul repo di oggi (`b701d39`) |
|---|---|
| `state.md` | **1.625 righe** — §8 changelog **1.178 (72%)**, parte viva **447** |
| righe tabellari | **183** in tutto il file |
| chi tocca `state.md` | **20 file**: 12 script + 8 test |
| marcatori di regione in `state.md` | 🔴 **zero** |

Il ramo `refs/pull/99/head` (`fce0490`, **10 agosto**) porta:

| File | Righe | Stato su `main` |
|---|---:|---|
| `campaign/state.yaml` | 766 | non esiste |
| `campaign/state-changelog.md` | 1.423 | non esiste |
| `scripts/render_state.py` | 249 | non esiste |
| `scripts/validate_state.py` | 234 | non esiste |
| `scripts/schemas/campaign_state.schema.json` | 475 | non esiste |
| `scripts/tests/test_state_data.py` | 257 | non esiste |
| `scripts/state_apply.py` | 387 | esiste, **140 righe divergenti** |
| `scripts/state_sync.py` | 154 | esiste, 27 divergenti |
| `scripts/tests/test_state_apply.py` | 136 | esiste, 39 divergenti |

🔴 **E i dati non si possono portare.** Confrontando la parte **viva** dei due
`state.md`: **229 righe** che il ramo ha e `main` no, **103** che `main` ha e il
ramo no. Il canone del **2026-09-11 e 2026-09-12** — D3, D4, D11, D13, i Tre
Doni, la Collana, i due tempi di 4c — nel ramo **non esiste**. Portare il suo
`state.yaml` sarebbe **annullare cinque settimane di canone in silenzio**, e la
byte-identità lo direbbe subito.

#### 4.8.2 · 🔴 Il fatto che riorienta il lotto: la via di scrittura è **già inerte**

`state.md` non ha **nessun** marcatore di regione, e `state_apply.py` ne ha
bisogno. Eseguito sul repo di oggi:

```
[apply] ⚠ march_clock non applicabile (regione 'march-clock' assente
        — lancia `state_apply.py --migrate` … regioni presenti: nessuna)
[apply] proposte NON meccaniche — applicale a mano in state.md
```

**Nessuna scrittura automatica funziona**, né il March Clock né il changelog:
degrada con eleganza e dice al DM di fare a mano. Quindi 4d **non sostituisce
una via di scrittura che funziona con una migliore**: accende una via che non è
mai stata accesa. Cambia il rischio — non c'è un comportamento buono da
preservare — e cambia il criterio: quel che va protetto è il **contenuto** del
file, non il flusso.

#### 4.8.3 · L'ADR ha il numero occupato — **terza volta**

Il ramo porta `plans/adr/ADR-0017-stato-dati-e-prosa.md` (211 righe). Su `main` <!-- validate-docs: ignore -->
**ADR-0017 è «moduli autoconclusivi e classe di artefatto»**: un'altra
decisione, presa nel frattempo.

🔎 È lo **stesso identico schema** già visto due volte: ex-0016 → **ADR-0039**,
ex-0017 → **ADR-0040** (dalla #72), ex-0014 → **ADR-0048** (lotto 4b). Una PR
lasciata aperta perde i suoi numeri. → il recupero diventa **ADR-0050**, con la
nota di rinumerazione e la riverifica riga per riga contro il codice di oggi,
come si è fatto per le altre tre.

#### 4.8.4 · Cosa coprono le otto regioni, e cosa **no**

| Regione | Sezione di `main` | Righe tabellari |
|---|---|---:|
| `archi` | §0 dashboard | 23 |
| `party` | §1 | 5 |
| `difensori` · `scenari` | §2 (parziale) | 62 |
| `villain` | §3 | 14 |
| `conoscenze` | §4 | 32 |
| `artefatti` | §6 | 9 |
| `echi` | sparsi | — |
| **nessuna** | **§5 promesse** | **10** |
| **nessuna** | **§7 thread narrativi** | **14** |

⚠️ **§5 e §7 restano prosa**, ed è una scelta dichiarata: sono le due sezioni
che il DM riscrive di più a mano, e modellarle adesso vorrebbe dire indovinare
uno schema per contenuto che cambia forma ogni sessione.

#### 4.8.5 — FASE 2 · Sviluppo, in due lotti

**4d-1 — la macchina e i dati** *(non tocca la via di scrittura)*

1. Portare `render_state.py`, `validate_state.py`, lo schema JSON e
   `test_state_data.py`, **riverificati** contro il codice di oggi.
2. Scrivere `campaign/state.yaml` **da `state.md` di oggi**, sezione per
   sezione. È la parte grossa e non si può automatizzare: la struttura viene
   dal ramo, i **valori** dal canone attuale.
3. Inserire le otto coppie di marcatori `<!-- gen:state:… -->` in `state.md`.
4. **ADR-0050**, recuperato e rinumerato.
5. Gate `render_state --check` in CI.

**4d-2 — lo storico e la via di scrittura** *(lotto separato)*

Lo split di §8 in `campaign/state-changelog.md` e `state_apply` che scrive lì.
⚠️ È il punto in cui la #99 registra una **regressione propria**: *«lo split
dello storico aveva rotto `state_apply --migrate`. La CI non l'aveva vista
perché quei test girano su fixture»*. I due test **sui file veri** si portano
**prima** della modifica, non dopo.

#### 4.8.5-bis · Com'è andata (2026-09-16) — **4d-1 chiuso**

**Il criterio d'uscita è stato raggiunto**: `state.md` rigenerato torna
byte-identico. Il diff contro il file di partenza è di **32 righe, tutte
marcatori** — 8 regioni × (apertura + banner + riga vuota) + 8 chiusure. Zero
righe di contenuto toccate.

`state.yaml` porta **99 record** in 8 sezioni, estratti da `state.md` di oggi:
22 archi · 31 conoscenze · 13 villain · 9 difensori · 8 artefatti · 7 echi ·
5 scenari · 4 PG.

🔴 **La promessa dell'ADR andava ridimensionata, e misurarlo è stato il punto.**
ADR-0050 diceva *«un fatto senza tempo dichiarato non è esprimibile»*. Il canone
il tempo lo dichiara in **due forme diverse** — per riga in §0, come **due
colonne** in §1 e §6 — e in **quattro sezioni non lo dichiara affatto**: §3, §4
e le due tabelle di Rethmar, **58 righe**. Il generatore della #99 risolveva
aggiungendo una colonna `Tempo`; quella forma è del 10 agosto e 4c l'ha superata.

Assegnarne uno riga per riga sarebbe **dedurlo**, cioè inventare canone dentro
un lotto di infrastruttura. Quindi il campo è opzionale lì e la regola **R7**
di `validate_state.py` le **conta a ogni esecuzione**. Un numero che si vede non
cresce in silenzio; il giorno che il DM li dichiara, scende da sé.

🐛 **E ho trovato un difetto mio, già mergiato.** `ADR-0049` era **già occupato**
dall'edizione commerciale (arrivato con la #138, lotto 4c) quando gli ho dato lo
stesso numero per il margine del bosco nella #141: non l'ho controllato. È
esattamente la regolarità che questo lotto stava documentando — *una PR lasciata
aperta perde i propri numeri* — e stavolta l'ho causata io in due giorni.
Rinumerato in **ADR-0051** e corretto in **9 file**.

🔎 **Altre due àncore invecchiate**, trovate eseguendo i test del ramo: cercavano
`MORTA` in maiuscolo, mentre il canone di oggi scrive `🔴 **morta**`. Un'ancora
è una citazione del canone, quindi invecchia col canone.

#### 4.8.7 · Lotto **4d-2** — lo storico e la via di scrittura

> `[C costruzione · Opus 5 · alto · le 1.179 righe spostate sono **identiche
> byte per byte**, e `state_apply` scrive davvero nel file nuovo — provato sul
> file vero, non su fixture]`

##### Audit, misurato su `14694c4`

| | |
|---|---:|
| `state.md` | **1.657 righe** |
| di cui §8 changelog | **1.179 (71%)** |
| blocchi fenced dentro §8 | **tre**, consecutivi — `state_apply` appende all'ultimo |
| consumatori della **regione** changelog | **due** |

🔎 **Il raggio d'azione è molto più piccolo di quanto «71% del file» faccia
temere.** Cercando `changelog` in sei script, quattro lo nominano solo in
commenti che parlano di `plans/CHANGELOG.md`, un altro file. Chi tocca davvero
la regione è:

- `state_apply.py` — la scrive (`append_changelog`, `--migrate`);
- `dm.py` §doctor — verifica che i marcatori `march-clock` e `changelog`
  esistano in `state.md`.

##### 🔴 La via di scrittura è a **un comando** dall'essere accesa

`state_apply.py --migrate` eseguito sul repo di oggi inserisce i marcatori e
tocca **4 righe**. Non è mai stato lanciato: per questo `state_apply` degrada
dicendo al DM di fare a mano (§4.8.2). 4d-2 la accende, ed è metà del suo senso.

##### La regressione da non ripetere, e come

⚠️ La #99 registra un difetto **proprio**: *«lo split dello storico aveva rotto
`state_apply --migrate`. La CI non l'aveva vista perché quei test girano su
fixture»*. È il motivo per cui 4d-2 è stato separato da 4d-1, e il rimedio non è
attenzione: i test di questo lotto girano **sui file veri del repo**, non su un
fixture costruito per passare.

##### Assunzioni dichiarate

1. **Il contenuto si sposta alla lettera.** Nessuna riga riscritta, riordinata o
   ricompattata: il criterio d'uscita è la **byte-identità** delle 1.179 righe
   spostate. Un changelog è append-only per decisione, e riscriverlo mentre lo
   si sposta renderebbe impossibile dire cosa è cambiato.
2. **§8 non sparisce da `state.md`: diventa un puntatore.** Chi apre il file e
   cerca lo storico dev'essere mandato dove è finito, non trovare un buco.
3. **Il reset per gruppo nuovo resta fuori.** `campaign/templates/state-blank.md`
   esiste ma **nessuno script lo legge**: il reset automatico non c'è ancora, e
   la perdita che la #99 descriveva non è viva su `main`. Diventa un vincolo per
   il lotto **4f**, che dovrà conoscere `state.yaml` e `state-changelog.md`.

##### Com'è andata — **chiuso**, con un difetto trovato accendendo la luce

**Lo split è pulito**: `state.md` da **1.657 a 486 righe**, e le **1.177 righe**
spostate sono **identiche byte per byte** — confrontate contro `git`, non contro
una copia fatta al momento. §8 resta come **puntatore**, non come buco.

**La via di scrittura è cablata e accesa**: `state_apply` legge e scrive due
file, `--migrate` marca in entrambi, `dm.py doctor` cerca ogni regione dove
adesso vive. Il changelog è marcato e l'append funziona — provato sul **file
vero**, in memoria, senza toccarlo.

🔴 **E accendendola è saltato fuori un difetto che sarebbe costato canone.**
`migrate()` presumeva che «`**Current March Day:**`» fosse una riga a sé; il
lotto 4c l'ha resa l'**inizio di un paragrafo di cinque righe**. Marcandone solo
la prima, `apply_march_clock` l'avrebbe sostituita lasciando le altre quattro
**orfane a metà frase**. Non era mai emerso perché `--migrate` non era mai stato
eseguito.

Il lotto **rifiuta di indovinare**: la marcatura è bloccata con un errore che
dice perché, e — seconda correzione — **una regione insicura non blocca più
quella sicura**, perché punire il changelog per la prosa di `state.md` sarebbe
punire il file sbagliato. Dove vada la riga della macchina è la **decisione
D14**; finché è aperta il March Clock resta manuale, com'è sempre stato.

##### Validazione

| Prova | Criterio |
|---|---|
| **byte-identità dello spostamento** | le righe del nuovo file combaciano con quelle tolte, carattere per carattere |
| **la via di scrittura funziona** | `state_apply --migrate` poi `--check`: i marcatori ci sono e la proposta è applicabile |
| **sui file veri** | i test leggono `campaign/state-changelog.md`, non un fixture — è la lezione della #99 |
| **il puntatore regge** | `validate_docs --sorgenti` verde: §8 di `state.md` cita un percorso che esiste |
| **non-regressione** | `dm.py doctor`, `render_state --check`, 763 test |

#### 4.8.8 · Lotto **4d-2** (seguito) — i tre master, e la trappola che 4d-1 aveva aperto

[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests -q` → 799 test;
`render_state.py --check` verde dopo un `state_apply` andato a buon fine; sei
cancelli nuovi **provati all'indietro**, tutti rossi]

##### Il difetto, misurato prima di scrivere una riga

Da quando le otto tabelle di `state.md` sono generate (4d-1), `state.md` è
**insieme master e vista**, e la differenza la fanno i marcatori
`<!-- gen:state:… -->`. `state_apply` però chiudeva ogni sessione stampando:

> `[apply] proposte NON meccaniche — applicale a mano in state.md:`

Per metà delle proposte quella era l'istruzione per **perderle**. Provato sul
repo vero: cambiando «Dwarf Fighter 13» in «14» dentro `state.md`,
`render_state --check` diventa rosso e la modifica **sparisce** alla
rigenerazione successiva. Non esiste una via md → yaml: il flusso è a senso
unico.

La stessa riga stava in `state_sync.py` («*apply by hand to `campaign/state.md`*»),
e sbagliava per lo stesso motivo.

##### Dove vive ogni fatto — `scripts/dmcore/masters.py`

| Master | Cosa ci sta | Trigger che ci finiscono |
|---|---|---|
| `campaign/state.yaml` | i fatti tabellari di §0, §1, §2.4, §3, §4, §6, §7.E | `ritual_clock` · `villain_clock` · `npc_killed` · `npc_escaped` |
| `campaign/state.md` | §2 waypoint e orda, §5, §7, i banner dei due tempi | `march_clock` · `alliance` |
| `campaign/state-changelog.md` | lo storico, append-only | (ci scrive solo la macchina) |

La copertura è un **cancello**: un trigger nuovo senza la sua riga fa rossa la
CI, perché senza destinazione la proposta tornerebbe al messaggio generico.

##### Cosa diventa meccanico, e cosa **no**

Scrive da sé: i **clock dei villain** (§3), che sono un numero in un campo
dichiarato. Il record si trova per nome e numeratore; **zero corrispondenze o
più d'una lasciano la proposta a mano**, senza ripiego. Con tredici villain in
tabella, sceglierne uno a caso è canone rotto in silenzio.

⚠️ **Morte e fuga restano proposte, e non è una dimenticanza**: i record
`villain` non hanno un campo `stato`. Dichiararne uno è una modifica di
**schema** — si decide e si documenta, non si deduce da una riga di log a fine
sessione. Diventa la decisione **D16**.

Anche `Sethrax` resta a mano, ed è il caso che mostra che la regola funziona: il
suo clock è «*Sync to Tournament (Day 1 = arrivo…)*», non `n/m`. Non è un
contatore e il tool non finge che lo sia.

##### Come si scrive in uno YAML senza riscriverlo

`yaml.safe_dump` rigenererebbe tutte e **502** le righe — commenti di testa
compresi, che lì non sono decorazione ma la spiegazione di ADR-0050 — per
cambiare tre caratteri. Un diff di 502 righe per un clock che passa da `9/18` a
`10/18` è un diff che nessuno rilegge.

Quindi `dmcore/statedata.py` modifica **la riga**, e poi **verifica contro il
parser** che sia cambiato esattamente quel campo e nient'altro: carica prima e
dopo, applica la modifica attesa alla struttura caricata, e confronta. La
modifica testuale è veloce e ingenua; la verifica è totale. Se la seconda non
conferma la prima, non si scrive niente. Misurato sul file vero: **una riga su
502**, commenti intatti.

E dopo il master, la vista: `state_apply` rigenera le regioni `gen:state:`
nello stesso giro. Senza, un `state_apply` andato a buon fine lascerebbe il
repo in uno stato che `render_state --check` boccia in CI. Se i marcatori
mancano, **non si scrive nemmeno il master**: o tutti e due, o nessuno.

##### Validazione

| Prova | Criterio |
|---|---|
| **sul repo vero** | `state_apply` eseguito davvero sul canone: 1 riga in `state.yaml`, 1 in `state.md`, 1 nel changelog — poi `git checkout` |
| **la vista segue il master** | `render_state --check` verde **dopo** l'apply, non prima |
| **i cancelli mordono** | 6 sabotaggi (destinazione tolta, destinazione sbagliata, vista non rigenerata, nome non catturato, riga sbagliata, messaggio generico) → **tutti rossi** |
| **si degrada, non si rompe** | senza `state.yaml` il clock resta una proposta a mano, exit 0 |
| **la guardia copre i tre file** | era tarata solo su `state.md`; adesso un `state.yaml` sporco blocca la scrittura |
| **non-regressione** | 799 test, `validate_state`, `dm.py doctor` |

#### 4.8.9 · Lotto **4d-3** — cosa è dato e cosa è prosa (D14 e D16 chiuse)

[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests -q` → 814 test;
`render_state.py --check` verde dopo un `state_apply` sul canone vero; **sette**
cancelli nuovi provati all'indietro, di cui **uno non mordeva e il giro l'ha
scoperto**]

##### FASE 1 · Audit — cosa c'è davvero in `state.md`

| Misura | Numero |
|---|---|
| righe totali | **486** |
| dentro le regioni generate | **131** in 8 regioni |
| **righe-dati tabellari ancora FUORI da `state.yaml`** | **56** in 6 tabelle |
| §7 fili narrativi | **24 bullet**, semi-strutturati (tag, fonte, conseguenza) — payload in prosa |

Le sei tabelle non modellate: §2.1 March Clock (10) · §2.2 orda (13) ·
§2.3 additivi condizionali (11) · §2.5 infiltratori (8) · §5 promesse (9) ·
§7.R reputazione (5).

🔎 **E il pezzo che cambia la risposta alla domanda del DM**: i dati di PNG e
villain **esistono già**, altrove e fatti meglio — `Bestiario/` ha **32 PNG** e
**35 villain**, `validate_bestiario` conta **115 statblock validi**, e
`scripts/monster_catalog.yaml` è un indice macchina di **305 voci**
(`id · name · cr · faction · role · environment · source_file`).

🔴 **Quel che manca non è il dato: è la chiave.** Misurato riga per riga:
**11 villain su 13** e **23 PNG su 31** di `state.yaml` si agganciano a una
cartella del `Bestiario/` **solo per somiglianza di stringa**, e **Zalkatar** e
**Saarvith/Regiarix** lì **non esistono affatto**. Un algoritmo deterministico
non può seguire un collegamento che nessuno ha dichiarato; un LLM lo indovina,
che è peggio.

##### FASE 2 · Sviluppo

**D16 — lo stato vivo è un dato.** `stato`
(`attivo · latitante · neutralizzato · morto · ignoto`) e `reversibile`,
obbligatorio appena lo stato non è `attivo`. Su **§3 villain (13)** e
**§1 party (4)**.

⚠️ **§4 conoscenze è stata esclusa dopo averla misurata, e il DM aveva chiesto
di includerla.** Guardandola riga per riga: **tre righe non sono persone**
(«Druid Circle of the Sacred Forest», «Lathander + Mask», «Tiri Kitor wild
elves») e **tre persone compaiono sotto due nomi diversi** (Sonjak, Varis,
Zalkatar/Sethrax). Mettere `stato` lì vorrebbe dire un valore privo di senso in
tre casi e **due copie divergenti** in altri tre — cioè ricreare il difetto C2
dentro la sua stessa correzione. La casa giusta è l'anagrafica dei PNG, che è il
lotto della chiave: §4 ci si aggancia invece di duplicare.

**D14 — il tempo della macchina.** Risposta del DM: *«la riga va in state.yaml e
poi riportata in state.md»*. Misurata, regge: la tabella dei waypoint è **dato
puro** (10 righe) e il March Day è **un campo**. Il paragrafo di cinque righe
resta **prosa, sotto e fuori** dalla regione generata.

Conseguenze: la regione `auto:march-clock` **sparisce**, e marcarla oggi sarebbe
*peggio* di prima — una regione dentro una regione `gen:state:` sono due
scrittori sullo stesso testo. Sparisce anche `RETHMAR_DAY = 42`, cablato in
`state_apply`: era la seconda fonte di verità più piccola del repo, e
sopravviveva perché **nessuno aveva mai eseguito il tool**.

##### FASE 3 · Validazione

| Prova | Criterio |
|---|---|
| **sul canone vero** | `state_apply` eseguito davvero con March Clock, morte, fuga e clock: 4 scritture nel master, vista rigenerata, poi ripristino |
| **la consegna macchina → DM funziona** | dopo la scrittura di `stato`, **R9 scatta** e chiede al DM se è definitivo: è il punto di passaggio, non un errore |
| **i cancelli mordono** | 7 sabotaggi → 7 rossi |
| **byte-identità della prosa** | fuori dalle regioni generate, `state.md` non cambia di un carattere |
| **non-regressione** | 814 test, `validate_state`, `validate_docs --sorgenti`, `dm.py doctor` |

🐛 **Un cancello non mordeva, e il giro dei sabotaggi l'ha scoperto.** Il test
sui «giorni mancanti derivati» confrontava il reso col valore atteso **sui dati
di oggi**: 42 − 19 fa 23, quindi cablare `**23**` nel renderer lo faceva passare
lo stesso. Un test che concorda col difetto che dovrebbe trovare non prova
niente. Rifatto: adesso **muove il dato** su tre giorni diversi e verifica che il
reso lo segua — un numero cablato resta fermo mentre il dato cambia, ed è
l'unica differenza osservabile fra derivato e scritto due volte.

🐛 **E ho di nuovo inventato il nome di un file ADR** citando ADR-0041 — la
quarta volta in questa campagna. `validate_docs --sorgenti` l'ha ripreso prima
del commit, che è esattamente il lavoro per cui esiste.

##### Cosa resta aperto

| | Cosa | Numero |
|---|---|---|
| ⬜ | **la chiave verso `Bestiario/`** — campo `scheda:` + cancello che verifica il percorso; è il lotto successivo, deciso dal DM | 2 villain e 8 PNG da risolvere a mano |
| 🔵 | le tabelle ancora non modellate (§2.2, §2.3, §2.5, §5, §7.R) | **46 righe**: non un residuo, sono **prosa dichiarata** (verificato il 2026-09-24, §4.9.0) |
| ⬜ | §7 fili narrativi: semi-strutturati, e modellarli adesso vorrebbe dire indovinare uno schema | 24 bullet |

#### 4.8.10 · Lotto **4d-4** — la chiave verso il Bestiario (D17 chiusa)

[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests -q` → 833 test;
`render_state.py --check` **byte-identico** dopo tutto il lotto; sei cancelli
nuovi provati all'indietro, tutti rossi]

##### FASE 1 · Audit — e il numero di ieri era ottimista

ADR-0052 aveva misurato **11 villain su 13** e **23 righe di §4 su 31**
agganciabili per somiglianza. Rimisurando prima di costruire, quel confronto era
**severo**: pretendeva tutte le parole del nome della cartella, e produceva solo
silenzi. Allentandolo, le righe agganciate salgono — e le nuove risposte sono
**sbagliate**:

| Riga in `state.yaml` | Cosa aggancia un confronto permissivo | |
|---|---|---|
| `Zalkatar (Illithid Warlock)` | `Xal_thor` **oppure** `Zarim` | due illithid diversi |
| `Wyrmlord Saarvith + Regiarix` | `Wyrmlord_Karruk` | un altro wyrmlord |
| `Zalkatar (via Sethrax)` | `Sethrax_il_Velato` | ma chi **sa** è Zalkatar |
| `Druid Circle of the Sacred Forest` | `druid-bear-ally-cr12.md` | l'orso alleato |

🔴 **È la misura che decide l'architettura.** Un matcher più generoso non riduce
l'ignoranza: la **traveste**. Il quarto caso è il peggiore perché «Sethrax» è un
PNG che esiste davvero — il collegamento sbagliato supera qualunque controllo di
esistenza.

🔎 **Seconda cosa emersa misurando**: il `Bestiario/` non ha un file per persona.
La scheda canonica sta in `X/X/X.md` o `X/X.md`, il `*-crN.md` in cima è spesso
un **puntatore**, e Brenna Sorvane, Sertieren e Norro Wiston vivono come
**sezione dentro un file di gruppo**. Nessuna derivazione dal nome può saperlo.

##### FASE 2 · Sviluppo

Sezione `png` in `state.yaml`: **28 voci** (`id` · `nome` · `tipo` · `scheda`),
e `png_id` sulle **13** righe di §3 e le **31** di §4. Tre regole nuove in
`validate_state`: **R10** (l'id risolve, è unico, e un buco porta il perché),
**R11** (la scheda esiste sul filesystem), **R12** (i buchi si contano).

**D17 — e la premessa era falsa.** 🐛 La prima stesura dichiarava **quattro**
voci senza scheda. Tre ce l'avevano, e il DM l'ha fatto notare: *«controlla bene
negli archi o nel bestiario se c'è qualcosa magari annegato come prosa»*.

L'errore non è stato non trovarle, è stato **come ho concluso**: ho cercato solo
dentro `Bestiario/`, e allargando la ricerca ho troncato l'output con `head -6`
— dichiarando «non esistono» da una lista tagliata, in cui le righe mancanti
erano proprio i file cercati.

| | Dove la scheda era davvero |
|---|---|
| `zalkatar` | `09_…/P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` — **GS 13**, 14d4+70, CA 24 |
| `saarvith-regiarix` | `09_…/P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` — **GS 13** |
| `cerchio-sacro` | `Bestiario/mostri/cerchio-druid7-cr7.md` — [ACCEPTED — DM-canon 2026-05-05] |
| `lathander-mask` | nessuna, **e va bene**: due divinità non sono una creatura |

Non c'era niente da scrivere né da togliere: c'era da **cercare meglio**. Resta
**un** buco su 28. ⚠️ E la conseguenza di progetto: una scheda **non vive per
forza nel `Bestiario/`** — due boss da GS 13 stanno in un arco.

##### FASE 3 · Validazione

| Prova | Criterio |
|---|---|
| **le schede esistono** | 24 percorsi verificati contro il filesystem, non contro una lista |
| **la chiave corregge il matcher** | un test riproduce i quattro errori e verifica che l'anagrafica **non** li segua |
| **il DM non paga niente** | `render_state --check` byte-identico: `png_id` non compare in `state.md` |
| **R13, il cancello nato dall'errore** | rimettendo `zalkatar` a «senza scheda» — lo stato in cui l'anagrafica è nata — il cancello diventa **rosso** |
| **i cancelli mordono** | 7 sabotaggi → 7 rossi |
| **non-regressione** | 833 test, `validate_docs --sorgenti`, `dm.py doctor` |

##### Cosa resta

| | Cosa | |
|---|---|---|
| ⬜ | `stato` sale dall'anagrafica: allora anche i PNG di §4 ne hanno uno | il `tipo` esiste già per quel giorno |
| 🔵 | tabelle non modellate (§2.2, §2.3, §2.5, §5, §7.R) | 46 righe, **prosa dichiarata** (§4.9.0) |

#### 4.8.11 · Lotto **4d-5** — i PNG d'arco che nessuno strumento raggiungeva

[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests -q` → 839 test;
catalogo da **305 a 352** voci; il cancello nuovo ha trovato da solo **tre file**
che la mia ricerca a mano aveva saltato]

##### FASE 1 · Audit

Richiesta del DM: *«verifica se in tutta la prosa degli archi ci sono altri PNG,
villain e mostri che non sono presenti nel bestiario png e villain, e aggiungili»*.

| Misura | |
|---|---:|
| documenti d'arco con statblocchi **in prosa** (Taglia/Tipo, DV, CA, TS) | **19** |
| soggetti con statistiche estratti | **47 + 14** nominati con classe e livello |
| già raggiungibili dagli strumenti | 10 |
| 🔴 **con statistiche scritte e invisibili a ogni strumento** | **47** |

🔴 **Il difetto, in una riga**: `build_monster_catalog.py` e
`suggest_encounter.py` costruiscono il pool degli incontri scansionando i file
che hanno **la forma** dello statblocco, e la forma d'arco spesso non la ha. Il
campione del Torneo di Dauth (Monk 14), il boss dei campi drow (GS 13) e il
Drago Rosso che guida l'invasione (GS 15) erano **scritti e irraggiungibili**.

##### FASE 2 · Sviluppo — POINTER, non copie

Quarantasette voci nuove col pattern **già in uso** nel repo
(`capitana-lorana-cr7.md`): una voce che **rimanda** al file d'arco. Le
statistiche restano dove il DM le ha scritte, perché duplicarle creerebbe la
seconda copia che **ADR-0021** vieta.

- **PNG nominati** (13): Grandmaster Rihan · Tetsu «Serpente di Vento» · Lady
  Koryn · Ironclad Bruiser · Mistress of Mirrors · Thrain Ironfist · Grom
  Skullcrusher · Zhen Windwhisper · Kira · Maestra Shen · Killiar Arrowswift
- **Villain** (5): Xilthra Vel'ssin · Saarvith & Regiarix · Kragar il Re delle
  Catene · Il Campione Caduto · Xal'thor «Forma del Nucleo»
- **Creature** (29): la Torre Invisibile (golem, oblex, grell, sciami), i campi
  drow, la colonia fungina, i comprimari dell'arena

⚠️ **Grom Skullcrusher non è l'Ogre Skullcrusher**: barbaro GS 14 contro ogre
GS 5. È la forma d'errore che 4d-4 aveva documentato, e un test la fissa.

##### FASE 3 · Validazione

| Prova | Criterio |
|---|---|
| **il pool è cresciuto** | `suggest_encounter` passa da **305 a 352** creature |
| **il cancello trova da solo** | ha segnalato **3 file** che la ricerca a mano aveva saltato: i villain iconici del torneo, le comparse dell'arena, i nemici della Quest di Hella |
| **i POINTER non copiano** | un test boccia una voce POINTER che porti statistiche: sarebbe la seconda copia |
| **due vie di raggiungibilità** | il criterio è «gli strumenti ci arrivano», non «esiste una voce»: `build_monster_catalog` raggiunge già alcuni file d'arco direttamente |
| **non-regressione** | 839 test, `validate_bestiario` (162 statblock), nove gate verdi |

🐛 **E il cancello è nato sbagliato due volte, in un modo istruttivo.** Prima
cercava l'aggancio nel campo `source_file` del catalogo — che però registra il
file **scansionato**, cioè la voce del Bestiario, non l'arco a cui rimanda: dava
per scoperti quattro file agganciati. Poi ignorava la seconda via, quella
diretta. Il criterio giusto non è «esiste una voce nel Bestiario»: è **«gli
strumenti ci arrivano»**.

##### 4.8.11-bis · Il DM ha dato la fazione, e trovando dove metterla è saltato fuori un difetto peggiore

Il lotto aveva lasciato `faction: unknown` sui comprimari del Torneo. Il DM
l'ha chiusa il 2026-09-17: *«sono emissari al soldo degli Zhentarim; gli
interessano gli scambi commerciali di merci del mercato nero extraplanare,
venuti per il Torneo di Dauth, e in parte minacciati anche loro dall'avanzata
della Mano Rossa»*.

Combacia con la lore canonica già in repo — *«THE ZHENTARIM (The Black
Network) — Goals: economic and political domination of all Faerûn trade
routes»* — quindi la fazione `zhentarim` nasce **dichiarata**, non inventata.
**15 voci**, più il dossier `Bestiario/villain/Zhentarim_Dauth/`.

⚠️ **E la mia frase precedente era imprecisa**: avevo scritto «sedici
comprimari del Torneo», ma le voci con `faction: unknown` erano **27**, di cui
15 del Torneo. Le altre sono la Torre di Zalkatar (7), gli illithid di Xal'thor
(2) e l'Erinni, che è finita a `red-hand` perché il suo stesso file la colloca
nell'onda epica di Rethmar.

🔴 **Il difetto vero, trovato applicando la fazione.**
`build_monster_catalog.py` **indovinava** fazione, ruolo e ambiente da euristiche
su parole chiave, e **ignorava le intestazioni** che ogni statblocco dichiara e
che `validate_bestiario` pretende. Due valori per lo stesso fatto: quello nel
file, e quello nel catalogo — e negli strumenti finiva il secondo. L'ho visto
perché l'intestazione diceva `zhentarim` e il catalogo registrava
`dauth-defender`, mentre il file *sembrava* giusto a chiunque lo aprisse.

| Campo | Record in cui il catalogo contraddiceva il file |
|---|---:|
| `faction` | **56** |
| `role` | **138** |
| `environment` | **77** |

Esempi: «Aberrazione Fungina Alfa» marcata `drow-sonjak` perché la parola
«drow» compariva nel testo; il Grell della Torre Invisibile marcato `mountain`.

**Corretto**: il valore dichiarato vince, l'euristica resta come ripiego per i
documenti che non dichiarano niente (i `.txt`, i moduli d'arco). È ADR-0041
applicato a questo tool.

⚠️ **Una regressione evitata di misura**: prima l'euristica *normalizzava* tutto
su una lista chiusa. Leggendo le intestazioni, le **6** creature che dichiarano
`mano-rossa` si sarebbero separate dalle **68** che dichiarano `red-hand` — e
`suggest_encounter --faction red-hand` avrebbe smesso di trovare Ushgar e
Ghaurush. Un alias dichiarato per l'unico sinonimo certo, e nient'altro.

##### Cosa resta

| | | |
|---|---|---:|
| 🔵 | **9 voci ancora `unknown`**: la Torre di Zalkatar e gli illithid di Xal'thor. Il DM non ne ha parlato, e derivare `zalkatar-torre` dal pattern `<padrone>-<dominio>` sarebbe una mia scelta | 9 |
| 🔵 | **vocabolario da consolidare**: `underdark` è usato come fazione (è un ambiente), e `rhod-allies` sta accanto a `red-hand` | 4 valori |

#### 4.8.12 · Lotto **4d-6** — il censimento conosceva una forma su tre, e gli archivi erano master

`[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests/test_censimento_forme.py scripts/tests/test_png_archi_nel_bestiario.py` verde su 3 cancelli provati all'indietro; `validate_bestiario` in sync su 372 record; 130 citazioni POINTER tutte risolte]`

Il DM, il 2026-09-17: *«considera tutta la prosa davvero negli archi, vedi
nell'arco la Torre di Zalkatar se c'è qualcosa non detto, vedi anche negli
archivi se è stato tralasciato qualcosa»*. Rimisurando **senza troncare
l'output** — la lezione esplicita di D17 — il cancello scritto il giorno prima
si è rivelato sbagliato in tre modi indipendenti.

##### FASE 1 · Accertamento

| Cosa | Misura |
|---|---:|
| Forme di statblocco in uso nel repo | **3** (il matcher ne conosceva **1**) |
| Documenti d'arco con statistiche, rimisurati | **23 → 38** |
| File d'archivio con statblocchi che la matrice dichiara **MASTER** | **5 su 5** |
| Citazioni POINTER abbreviate (`08_.../ARC08-01-…`) | **11** |
| Citazioni POINTER con percorso sbagliato di un livello | **6** |
| Record del catalogo intitolati al documento invece che alla creatura | **19** |

🔴 **Il caso che decide il lotto.** Il matcher pretendeva il trattino (`- CA:`);
`10-stand-alone/L'Abbazia della Rotta Sicura` scrive `**CA** 15`, quindi valeva
**zero marche su zero**. Un'avventura stand-alone **intera** — 1.419 righe, con
un appendice di statblocchi tutto suo — era fuori dal censimento in silenzio, e
non aveva una sola voce nel Bestiario.

🔎 **E la Torre di Zalkatar era coperta**, contrariamente al sospetto: tutte e
nove le creature hanno voce propria. Quel che non era detto sta altrove — vedi
D18 sotto.

##### FASE 2 · Sviluppo

1. **`scripts/dmcore/censimento.py`** (nuovo): le tre forme, la soglia, e
   `master_archiviati()` che legge `ARC07-MATRICE-VERSIONI.md` invece di
   indovinare dal nome della cartella. L'inline resta **stretto** apposta.
2. **20 voci POINTER nuove**: il cast dell'Abbazia (9), i master d'archivio
   dell'ARC-07 (Terros GS 15, Skullcrusher il Nero, Zog'tar Deatheye, lo Xorn
   Anziano, l'Elementale Anziano, Thorgrim Barbadiferro), l'ARC-06 (Yochlol
   half-illithid, Dire Worg corrotto), l'ARC-04 (Grimlock Ceremorfo, Drow
   Psionica, Carcassa Vivente). Pool: **352 → 372**.
3. **17 percorsi POINTER corretti**, e il criterio d'aggancio passa da
   «sottostringa» a «`Path.exists()`».
4. **`FUORI_RAGGIO`**: cinque documenti che portano numeri ma non creature (le
   schede dei PG, il sistema di combattimento di massa, le guide della Corona),
   ognuno **con il motivo scritto**.

##### FASE 3 · Validazione

| Prova | Esito |
|---|---|
| Rimettere l'esclusione cieca di `_ARCHIVIO` | 🔴 rosso (`Terros.md` esce dal raggio) |
| Restringere il matcher alla forma col trattino | 🔴 rosso (9 test) |
| Riabbreviare un percorso a `08_.../…` | 🔴 rosso |
| `python3 -m pytest scripts/tests -q` | ✅ **843 → 853** passati (2.832 → 2.938 subtest) |
| `validate_bestiario` · `validate_state` · `validate_docs --sorgenti` · `tools_manifest --check` | ✅ tutti verdi |

⚠️ **Non tocca** `test_archivi_non_indicizzati.py`: i master d'archivio
diventano **raggiungibili** via POINTER, non **indicizzati**. Ogni
`source_file` resta dentro `Bestiario/`, quindi la regola dei doppioni
(305 → 311 nell'incidente del 2026-09-12) continua a valere.

Vedi [ADR-0054](adr/ADR-0054-un-archivio-non-e-una-copia.md).

##### 4.8.12-bis · D18 decisa — un documento con dodici creature non è una voce sola

Il DM ha chiuso D18 nella forma proposta: *«spezzarli per intestazione
verificando che non esistano già»*.

| Misura | Prima | Dopo |
|---|---:|---:|
| Record intitolati al documento | **19** | **8** |
| Voci nel pool degli incontri | 372 | **397** |
| Test | 853 | **865** |

Gli **otto** che restano non sono un residuo da ripulire: sono i documenti in
cui almeno una creatura non ha ancora una voce propria, e il record di file è
l'unica cosa che la tiene nel pool. Toglierli darebbe meno rumore e **meno
creature** — il difetto opposto a quello che D18 chiude.

⚠️ **Dove poteva far danno.** Confrontare nomi per somiglianza è l'errore che
ADR-0053 vieta. Qui il confronto è lecito perché ristretto alle voci che citano
**quel** documento come `Source`: il legame l'ha scritto qualcuno, la
somiglianza sceglie solo *quale* voce sta per *quale* intestazione.

🔎 **Il cancello ha trovato un errore mio al primo giro**, e ne è venuta fuori
una catena: contava due «Skullcrusher il Nero» → la voce puntava al file che il
drago lo *nomina* soltanto → ripuntandola a `P5-FASTPLAY` il `P6-INTEGRAZIONE`
è rimasto scoperto → dentro c'erano **Re Thorek I** (Grr 16) e **Durin
Hammerfist**, l'antenato di Othrek. Due PNG di canone che nessuno strumento
raggiungeva, trovati da una correzione di percorso.

#### 4.8.13 · Lotto **4d-7** — il Padrone delle Menti ha un nome, e gli illithid una fazione

`[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests/test_catalogo_una_voce_per_creatura.py` verde; 871 test; `validate_bestiario` in sync su 397 record]`

Il DM, il 2026-09-17: *«sì, è Zalkatar il Padrone delle Menti»*. Una riga, e
chiude la quarta domanda di 4d-6 — *«gli illithid di Xal'thor cosa facevano?»*

##### La risposta era che la domanda riguardava l'altro conclave

Le due ipotesi del DM erano **l'Anello del Caos** e **lo scambio di schiavi con
Sonjak**. Misurate contro il canone scritto:

| Ipotesi | Esito |
|---|---|
| Xal'thor cerca l'Anello | ❌ la sua scheda dichiara *«**unico bersaglio** al Torneo: i Bracieri Gemelli»* e rifiuta esplicitamente l'Orbe. Un terzo obiettivo gli toglierebbe l'unica cosa che lo rende **il villain di Tordek** |
| Scambio di schiavi con Sonjak | ✅ **non è un'ipotesi: è già giocato e mai spiegato.** I Grimlock Ceremorphi di ARC-04 sono **«ex-schiavi drow»**, e le Yochlol half-illithid del raid alla Corona portano un template che *qualcuno* ha innestato |

🔴 **Ma il compratore non poteva essere Xal'thor, e il canone lo dice con le sue
parole.** I due conclavi si disprezzano proprio su questo: Xal'thor chiama
Zalkatar *«biologo da torre, ossessionato da esperimenti sterili»*; Zalkatar
chiama lui *«cacciatore di mandria»*. Un vivaio di girini con celle d'innesto
**è** il biologo da torre.

E c'era una terza prova che nessuno aveva letto insieme alle altre: il **Ring of
Chaotic Illumination si risveglia in quel laboratorio**
(`campaign-artifacts.md`), quando Artemis rifiuta la classe di prestigio. Il
conclave che gestiva quella stanza ha una ragione **documentata** per inseguire
Artemis — e l'arco di Artemis **è già** la Torre di Zalkatar.

##### Cosa è entrato

- **`Bestiario/villain/Zalkatar/Zalkatar.md`** — dossier `[NON-CREATURA]` che
  registra il canone con le sue quattro prove, e il filo Sonjak → laboratorio →
  Anello → Torre.
- **Due fazioni dichiarate**: `illithid-zalkatar` (13 voci: la Torre, Sethrax, i
  custodi) e `illithid-xal-thor` (6: Xal'thor, la Forma del Nucleo, Zarim, gli
  schiavi psionici). Le **9 voci `unknown`** che 4d-6 aveva lasciato al DM sono
  chiuse.
- **Cross-riferimenti** nei tre punti dove il DM li cercherà: i due file del
  laboratorio ARC-04, la scheda di Sonjak, quella di Urialle.

🐛 **Quel che la misura ha trovato per strada.** Prima di questo canone gli
illithid stavano su **quattro** etichette diverse: **Zarim** era marcato
`red-hand` mentre la sua stessa scheda dice *«legato alla fazione di Xal'thor»*,
Xal'thor era `aberration`, la sua Forma del Nucleo `unknown`. E
`build_monster_catalog.py` teneva la parola **`zalkatar` nell'elenco di parole
chiave di `red-hand`**: un illithid warlock classificato come Mano Rossa.

⚠️ **E scrivere il cross-riferimento ha spostato una fazione da solo.** Citare
Zalkatar nella scheda di **Urialle** ha fatto passare l'euristica da
`aberration` a `illithid-zalkatar` — ma Urialle combatte per **Sonjak**: lui le
ha solo innestato il template. La correzione non è stata togliere la citazione,
è stata **dichiarare** la sua fazione (ADR-0041): un valore dichiarato non lo
sposta una menzione.

🔎 **E il marcatore `[NON-CREATURA]` è una stringa esatta, non prosa.** La prima
stesura del dossier scriveva `[NON-CREATURA — dossier di fazione]`, e il
builder cerca la forma letterale: Zalkatar era finito nel pool degli incontri
come un mostro da GS 13. L'ha visto il cancello delle non-creature, che tiene un
elenco **deliberatamente chiuso** — *«aggiungerne una è una riga qui e una
scelta»*.

#### 4.8.14 · Lotto **4d-8** — una fazione dice da che parte stai, non dove vivi

`[M igiene · Opus 5 · medio · `python3 -m pytest scripts/tests/test_vocabolario_delle_fazioni.py` verde; 883 test; 27 → 26 valori di `faction`; 397 → 384 record]`

Il DM: *«fai il vocabolario delle fazioni e cerchiamo di mergiare o droppare
questi doppioni»*. Misurando, le due voci di coda si sono rivelate **lo stesso
problema visto da due lati**: il campo `faction` conteneva cose che non sono
schieramenti, e lo stesso soggetto ne portava due valori diversi.

##### 1 · Tre valori non erano fazioni

| Valore | N | Cos'era |
|---|---:|---|
| `underdark` | 3 | un **ambiente** — e i tre file lo dichiaravano *anche* in `Environment` |
| `rhod-allies` | 1 | un contenitore da un membro |
| `rakshasa-hunter` | 1 | uno **scopo**, che sta già in `Role` |

🔴 **Perché un ambiente come fazione fa danno**: l'asse delle alleanze
(`faction_alliances.yaml`) si costruisce **sulle** fazioni, e un valore che
descrive il posto non può entrare in nessuna alleanza. `--faction underdark`
dava tre creature arbitrarie dove `--env underdark` le dà tutte.

I tre file sono trascrizioni PCGen di RHoD **mai collocate in un arco**:
l'alleanza non è stabilita, e dichiararne una sarebbe inventarla → `unknown`,
col perché scritto nel file. I due singoletti diventano **`alleati-del-vale`**.

##### 2 · Tredici soggetti avevano due record, e sei si contraddicevano

Una scheda canonica più un POINTER `-crN` accanto, nato quando lo scanner non
raggiungeva i file annidati. Adesso li raggiunge entrambi.

⚠️ **Non erano copie uguali**: in ogni coppia **uno dichiara le intestazioni e
l'altro le fa indovinare**. Tyrgarun era `dragon` da una parte e `red-hand`
dall'altra; l'Avatar di Tiamat `rethmar-defender` contro `red-hand`; il **Conte
Valerius** aveva **due GS**, 14 e 6.

La regola non è «tengo il canonico» ma **tengo quello che dichiara** — ADR-0041
applicato a una coppia. Sei contraddizioni risolte in favore del valore scritto
a mano. 🔵 Vale **solo** fra due file del `Bestiario/`: un POINTER verso un file
d'arco resta, perché lì è l'unica cosa che tiene la creatura nel pool.

##### 3 · E due fazioni d'epoca — un errore mio, trovato dal censimento

🔎 Avevo messo **Skullcrusher il Nero** e **Zog'tar Deatheye** in `red-hand`, ma
il loro assedio è del **~372 DR**, mille anni prima della Mano Rossa — ed
esisteva **già** `orda-antica-372dr` per **Balvar Fuocospento**, consigliere
della stessa orda. Senza la correzione `--faction red-hand` poteva proporre un
drago di mille anni fa accanto a un hobgoblin del 1372.

Simmetrico: **`hammerfist-372dr`** per i difensori di quell'assedio (Re Thorek I,
Durin, Thorgrim), distinti da `hammerfist-hero` che sono gli eroi del **1372**.

##### Validazione

| Sabotaggio | Esito |
|---|---|
| spegnere la deduplica dei gemelli | 🔴 tornano i 13 doppioni, e Tyrgarun due fazioni |
| rimettere un ambiente come fazione | 🔴 3 test |
| far tornare Skullcrusher Mano Rossa | 🔴 le due ere si mescolano |

⚠️ **Una soglia che SCENDE va motivata**: il pool passa da 397 a 384 e questa è
l'unica volta in cui quel numero cala. Non è una perdita — sono i 13 soggetti
doppi ridotti a uno: **tredici record in meno, zero creature in meno**.

#### 4.8.6 — FASE 3 · Validazione

| Prova | Criterio |
|---|---|
| **Byte-identità** | `render_state.py --check` → `state.md` rigenerato **identico** a quello committato |
| **Il gate morde** | cambiare un valore in `state.yaml` senza rigenerare → rosso |
| **Lo schema morde** | un fatto **senza `oggi`/`tempo`** → rosso. È il vincolo che chiude C1 alla radice |
| **Nessuna perdita** | ogni riga tabellare delle sei sezioni coperte ha un record in `state.yaml`, contata nei **due sensi** |
| **Non-regressione** | i **20 file** che toccano `state.md` — 737 test verdi, `dm.py doctor --ci`, `next_session`, `session_recap` |

### 4.9 · Lotto **4e** — una sola via di scrittura `[✅ chiuso il 2026-09-24 · 4e-0 · 4e-1 · 4e-2 · 4e-3]`

> `[C costruzione · Opus 5, sessione principale (il piano diceva Sonnet 5) · alto ·
> un test **sui file veri** (§4.4): i tredici villain di `campaign/state.yaml`
> si raggiungono tutti dal log di sessione, e un delta vecchio o un `png_id`
> inesistente **non scrive niente**]`

#### 4.9.0 · FASE 1 · 4d è chiuso davvero? (2026-09-24, in sola lettura)

Richiesta DM: *«verifica con fase1.py che 4d sia davvero chiuso (il piano
dichiara 46 righe di tabelle non modellate come residuo)»*. `fase1.py --check`
sui sette file della via di scrittura: nessun archivio, uscita 0.

| Prova del contratto di 4d | Esito oggi |
|---|---|
| `render_state.py --check` | ✅ `state.md` allineato a `state.yaml` |
| `validate_state.py` | ✅ valido; R7 conta **58** righe senza tempo, R12 **1** voce senza scheda (`lathander-mask`), come dichiarato |
| i test di §4.8.6 (byte-identità, gate che morde, nessuna perdita nei due sensi, schema che morde) | ✅ esistono in `test_state_data.py`; i 75 test di stato passano |

**Le 46 righe, rimisurate** sulle tabelle fuori dalle regioni `gen:state:`:

| Tabella | Righe | Chi la dichiara |
|---|---:|---|
| §2.2 composizione dell'orda | 13 | `dmcore/masters.py`: §2 «waypoint e orda» è **prosa**, e *«modellarle è un lotto suo»* |
| §2.3 additivi condizionali | 11 | idem |
| §2.5 infiltrati e profughi | 8 | idem (è sotto §2) |
| §5 promesse | 9 | §4.8.4: **resta prosa, scelta dichiarata** |
| §7.R reputazione | 5 | §4.8.4: §7 resta prosa |
| **totale** | **46** | |

**Verdetto: 4d è chiuso sul suo contratto.** Le 46 righe non sono un residuo di
4d: stanno fuori dalle otto regioni che 4d aveva promesso, e il repo le dichiara
prosa in due posti. Il difetto era nel piano, che le elencava come ⬜ in due
tabelle «Cosa resta» senza dire di chi fossero. Da qui non sono un lotto di
questo piano. Modellarle sarebbe un lotto **K** e una decisione del DM: la
colonna «Status (Day 19 sync)» di §2.5 è la stessa forma dei due tempi che 4c ha
dovuto separare.

#### 4.9.1 · FASE 1 · Cosa resta di 4e sul codice di oggi

La #99 definiva 4e (commit `df9d74b`, 2026-08-06) in due parti:

1. **i dati**: clock dei villain, «chi sa cosa», numeri di Rethmar. ✅ **Già su
   `main`**, portati da 4d-1…4d-3: `villain.clock`, `villain.stato`, la regione
   `conoscenze`, `difensori_rethmar` e `scenari_rethmar`, `march_clock`.
2. **la via**: il log di sessione porta in testa un **front-matter coi delta**,
   emesso dal wizard, e `state_apply` legge quello invece di cercare con regex
   nella prosa. ⬜ **Non esiste.**

La seconda parte non è estetica. Misurato oggi, prendendo ogni villain di
`state.yaml` col nome breve che un DM scriverebbe nel log:

| Trigger di `state_sync` | Villain che vede | Chi manca |
|---|---:|---|
| `villain_clock` (9 clock numerici, il rituale a parte) | **3 su 9** | Zalkatar, Saarvith, Valerius, **Ghaurush, Zin'thara, Ushgar**. Il Collezionista si vede solo se il log scrive «Rakshasa» |
| `npc_killed` | **5 su 13** | Sal, il Collezionista, Xal'thor, Valerius, Mira Serani, **Ghaurush, Zin'thara, Ushgar** |
| `npc_escaped` | 13 su 13 | nessuno, perché accetta **qualunque** parola maiuscola. Lo salva `_stato_villain`, che scarta i nomi non univoci |

I nomi stanno **scritti nel sorgente** della regex. I tre villain canonizzati il
2026-08-05 non ci sono mai entrati: un loro clock o una loro morte a fine
sessione **non produce nemmeno la proposta a mano**, perché la riga non viene
riconosciuta. È il difetto che la #99 aveva previsto per Ghaurush.

La chiave c'è già, ed è di 4d-4: ogni record `villain` ha un `png_id`
obbligatorio. Il front-matter nomina il villain per `png_id`, non per somiglianza
di stringa.

**Fuori da 4e, dichiarato:** le tre righe di §4 che fanno sapere dei «Custodi
Eterni» a Ghaurush, Zin'thara e Ushgar prima che l'arco 08 sia giocato (la
domanda nuova della #99). Sono canone, non via di scrittura, e R7 le conta già
fra le 31 conoscenze senza tempo.

#### 4.9.2 · FASE 2 · Sviluppo, in tre sotto-lotti

| | Sotto-lotto | Cosa produce | Qualità |
|---|---|---|---|
| **4e-1** | il delta come dato | `dmcore/delta_sessione.py`: legge il front-matter, lo valida contro `state.yaml` (`png_id` esistente, `da` uguale al valore di oggi, `stato` nell'enumerazione dello schema) e lo emette in forma deterministica. `state_apply` lo usa **al posto** della regex per le quattro scritture meccaniche; senza front-matter si ricade sulla regex di oggi | test sui file veri: i 13 villain raggiungibili, un delta vecchio e un `png_id` ignoto **non scrivono**, un log con front-matter **e** righe di prosa non applica due volte |
| **4e-2** | il wizard lo scrive | `session_wizard` risolve i nomi contro `state.yaml` **mentre il DM risponde**, gli mostra a chi ha agganciato cosa e scrive il front-matter. Il DM non scrive YAML | un nome che non si risolve lo dice subito e resta prosa; il file del wizard è letto da `state_apply` senza regex |
| **4e-3** | documenti e chiusura | template di sessione, skill `rumblingstone-automation`, `README-automation`, docstring di `state_sync`, tracciatura | `validate_docs --sorgenti`, `validate_skills`, `tools_manifest --check` |

**Assunzioni dichiarate.**

1. **La regex resta** per i log senza front-matter. L'unico log in
   `campaign/sessions/` è scritto in anticipo e non ne ha; toglierla romperebbe
   la lettura dei log vecchi per guadagnare niente.
2. **Il front-matter porta solo ciò che `state_apply` sa scrivere**: March
   Clock, clock dei villain (rituale compreso), `stato`. Alleanze e prosa
   restano nella sezione *World events triggered*, come proposta a mano.
3. **`reversibile` non si scrive**, come oggi: lo dice il DM, e R9 glielo chiede.
4. **pyyaml** resta il debito dichiarato di ADR-0037: `state_apply` lo importa
   già. Il wizard lo usa solo per risolvere i nomi, e senza pyyaml scrive il log
   senza front-matter e lo dice.

#### 4.9.3 · FASE 3 · Validazione

| Prova | Criterio |
|---|---|
| **sui file veri** | `state.md`, `state.yaml` e `state-changelog.md` del repo copiati in un repo temporaneo; `state_apply` con un log a front-matter scrive il campo giusto, rigenera la vista e `render_state --check` resta verde |
| **i tredici** | ogni `png_id` di `villain` è raggiungibile dal front-matter; la regex resta com'è e un test dice quanti ne vede |
| **i cancelli mordono** | `da` diverso dal valore di oggi, `png_id` inesistente, `stato` fuori enumerazione: nessuna scrittura, uscita non zero, e il motivo a video |
| **una via sola** | front-matter più la stessa riga in prosa: una scrittura, non due |
| **non-regressione** | pytest completo, `dm.py doctor --ci`, `check_plans_discipline`, `validate_docs --sorgenti` |

#### 4.9.4 · Com'è andato 4e-1 (2026-09-24) — il delta come dato

`scripts/dmcore/delta_sessione.py` legge il front-matter, lo valida contro
`state.yaml` e lo trasforma in operazioni già risolte; `state_apply` le applica
con lo stesso diff e la stessa conferma di prima. Con un front-matter, i
trigger meccanici della regex si ignorano e **si stampano uno per uno**, perché
una riga aggiunta a mano che il delta non ha deve restare visibile.

**Le scelte prese durante il lotto**, che il piano non aveva visto:

- **Il rituale non è un caso a parte.** Azarr Kul ha un `png_id` e un clock
  `9/18` come gli altri: il delta lo muove con `clock`, e il riconoscimento
  «è l'unico su diciotto» che la regex deve fare non serve più.
- **Un log già applicato non è un errore.** Se il valore di oggi è già `a`, la
  voce non produce niente; se non è né `da` né `a`, il log è stato scritto su un
  altro stato e il delta intero si rifiuta. La via di oggi era idempotente, e
  questa lo resta.

| Prova | Esito |
|---|---|
| i tredici, su `state.yaml` vero | ✅ i 10 clock numerici si muovono e i 13 villain ricevono uno stato, ognuno sul suo indice |
| sui file veri, end-to-end | ✅ `state.md`, `state.yaml`, `state-changelog.md` copiati: il delta scrive, la vista rigenerata coincide, il secondo giro non scrive, un `png_id` ignoto lascia i tre file **identici** con uscita 1 |
| una via sola | ✅ un clock di Sonjak scritto solo in prosa **non** passa |
| il recap non vede il delta | ✅ nessuna sezione pubblica contiene `png_id` |
| 🔴 i cancelli mordono | ✅ **5 mutazioni su 5** rosse: regex non filtrata (1 test), niente tutto-o-niente (9), `da` del March Clock ignorato (1), niente idempotenza (2), `png_id` per somiglianza (16) |
| non-regressione | ✅ **1.229** test, `dm.py doctor --ci`, `tools_manifest --check` |

#### 4.9.5 · Com'è andato 4e-2 (2026-09-24) — il wizard scrive il delta

Le domande del wizard non cambiano: March Clock, Ritual Clock, clock toccati,
cambi di stato dei PNG. Cambia cosa succede alla risposta. `session_wizard`
legge `campaign/state.yaml`, risolve ogni nome col `png_id` e valida **ogni
voce da sola** contro lo stato di oggi. Quella che torna entra nel
front-matter; quella che non torna esce con il suo motivo a video e resta
nella prosa del log.

La validazione per voce è la differenza rispetto a `state_apply`, che fa tutto
o niente. Lì un delta sbagliato arriva a sera finita e non deve scrivere a
metà; qui il DM è davanti al terminale, e una voce sbagliata non deve buttare
via le altre che ha appena dato.

| Prova | Esito |
|---|---|
| le risposte diventano dati | ✅ Ghaurush e il Ritual Clock vanno a `ghaurush` e `azarr-kul`, «Ushgar morto» a uno `stato`; un nome inesistente produce un avviso e nessuna voce |
| una voce che non torna | ✅ esce da sola con «state.yaml dice», le altre restano |
| un nome ambiguo | ✅ «Illithid» aggancia più villain e non ne sceglie nessuno |
| dal wizard a `state_apply`, sui master veri | ✅ il log comincia col front-matter, `state_apply` scrive i quattro campi senza regex |
| senza `state.yaml` | ✅ il log esce senza front-matter, come prima di 4e |
| 🔴 i cancelli mordono | ✅ **3 mutazioni su 3** rosse: voce non validata da sola, nome ambiguo che sceglie il primo, front-matter non scritto |
| non-regressione | ✅ **1.234** test, `dm.py doctor --ci`, `tools_manifest --check` |

#### 4.9.6 · 4e-3 e la chiusura del lotto (2026-09-24)

I documenti che descrivevano la via di scrittura di prima, e cosa dicono ora:

| Documento | Diceva | Dice |
|---|---|---|
| skill `rumblingstone-automation` | «diff `state.md` (solo regioni auto)»; `--migrate` «inserisce i marker `auto:`» | il front-matter, il diff di `state.yaml` e della vista; `--migrate` marca solo lo storico |
| `DM-CAMPAIGN-PLAYBOOK` §4 | «March Clock e changelog §8 nelle regioni marcate `auto:`» di `state.md` | il wizard scrive i delta, `state_apply` li porta in `state.yaml` |
| `tools.manifest.json` (e `docs/tools/`) | `state_apply` scrive «SOLO nelle regioni `auto:` di state.md» | scrive in `state.yaml` e legge il front-matter; il wizard dichiara `state.yaml` come ingresso facoltativo |
| ADR-0050 §4-bis | lo schema della #99, col March Clock in una regione `auto:` | una nota d'attuazione con lo schema di oggi (D14 l'aveva superato) |
| `session-template.md`, `README-automation`, docstring di `state_sync` | niente sul front-matter | dove sta, chi lo scrive, e che la regex vale solo senza |

**Nessuna ADR nuova.** La decisione c'era già, ADR-0050 §4-bis, scritta per la
#99 il 6 agosto: questo lotto l'attua.

**Come si sa che 4e è finito**, contro il criterio di §4.9: i tredici villain
di `state.yaml` si raggiungono tutti dal log (10 clock numerici e 13 stati,
ciascuno sul suo record), un delta vecchio o un `png_id` inesistente lasciano i
tre master identici, e la prova gira sui file veri. **8 mutazioni su 8** fanno
rosso fra 4e-1 e 4e-2.

**Cosa resta di F4**: **4f** (prodotto e partita: il reset per gruppo nuovo
dovrà conoscere `state.yaml`, `state-changelog.md` e adesso anche il
front-matter), **4g** (schede PG a dati), **4h** (`groups/<slug>/`, PR
dedicata).

### 4.10 · Lotto **4f** — prodotto e partita `[4f-0 ✅ audit · 4f-1 ✅ · 4f-2 ✅ · 4f-3 ⬜ · 4f-4 e 4f-5 attendono D21]`

> `[C costruzione, con un sotto-lotto K (4f-2) · Opus, sessione principale ·
> alto · un test che esegue il reset su una copia dei file veri e dimostra che
> il gruppo nuovo **non eredita niente** della partita, e che la CI resta verde]`

#### 4.10.0 · FASE 1 · Cosa eredita oggi un gruppo nuovo (2026-09-24)

`scripts/new-campaign-group.sh` eseguito in un clone usa-e-getta, sul `main` di
oggi:

| Dopo il reset | Esito |
|---|---|
| `state.md` | copiato da `templates/state-blank.md`, che **non ha nessuno** dei 10 marcatori `gen:state:` → `render_state --check` **rosso**: la CI del gruppo nuovo fallisce al primo push |
| `state.yaml` | **non toccato**: 750 righe del primo tavolo, 22 archi, 4 PG, 8 artefatti, 13 villain, e `validate_state` le dà per valide |
| `state-changelog.md` | **non toccato**: 1.195 righe di storico del primo tavolo |
| `lore/campaign-history.md` | **non toccato**: 630 righe, metà premessa e metà cronaca |
| `recaps/` | **non toccati**: un recap e due `.hb.md`, compresa la cronologia |
| `DM-DOSSIER.hb.md` | **non toccato**: è generato da `state.md` del primo tavolo |
| `sessions/` | ✅ svuotato |

🔴 **E ADR-0050 §7 dice il contrario.** L'ADR, accettata e recuperata in 4d-1,
fissa la regola (il **prodotto** resta, la **partita** si azzera da template),
decide lo split di `campaign-history.md` in premessa e cronaca, e nomina il
presidio: *«`test_new_group.py` verifica che ogni file di stato sia coperto dal
reset»*. Su `main` quel test **non esiste**, come i template e lo split. Il
recupero di 4d-1 ha portato l'ADR e non il lotto che la attuava (G2-quater della
#99, `c825d6d`).

**Fuori da 4f, dichiarato:**

- `PG/` (schede e immagini dei quattro PG) è partita, ma è il lotto **4g**.
- Gli archi e il Bestiario sono scritti **per questi quattro PG**: artefatti col
  nome del portatore, missioni personali. È prodotto e il reset non lo tocca. Un
  gruppo con altri personaggi ha un problema di contenuto, non di infrastruttura.
- `campaign/misure/` (i campioni del κ) è uno strumento del repo, non partita.

#### 4.10.1 · Il taglio

| | Sotto-lotto | Classe | Cosa produce |
|---|---|---|---|
| **4f-1** | la partita come dato | C | un elenco unico dei file di partita e del loro template, letto dallo script di reset e dal test; `state-blank.md` coi marcatori, `state-blank.yaml`, `state-changelog-blank.md`; il reset che rigenera e **valida prima di dichiararsi finito**; `test_new_group.py`, il presidio che l'ADR promette |
| **4f-2** | lo split di `campaign-history.md` | **K** | `campaign-premise.md` (prodotto) e `campaign-chronicle.md` (partita), con la regola di ADR-0050 §7 applicata sezione per sezione e nessuna riga persa; i rimandi aggiornati |
| **4f-3** | documenti e chiusura | M | quickstart, playbook §7, manifest (anche `state_apply`, che non dichiara `state.yaml` e `state-changelog.md` fra le uscite), tracciatura |

#### 4.10.2 · La domanda che resta al DM: D19

`state.yaml` mescola prodotto e partita dentro lo stesso record. `png` è prodotto puro
(id, nome, scheda nel Bestiario) e passa al gruppo nuovo com'è. Le agende dei
villain, i waypoint del March Clock e le righe degli archi sono **testo del
primo tavolo**: «Skull Gorge bridge, crossed intact (PG did NOT sabotage)».

- **Scelta di default in 4f-1**: lo **scheletro** della #99. `png` resta, ogni
  altra sezione riparte da un record segnaposto dichiarato come tale, March Day
  1, arrivo a Rethmar al Day 42. È la lettura di ADR-0050 §7 e l'unica che non
  inventa canone.
- **D19**: preferisci un template **derivato**, che tenga le agende preparate
  dei 13 villain coi clock a zero, e gli archi tutti «da giocare»? Costa una
  revisione riga per riga (classe **K**), perché ogni agenda va ripulita da ciò
  che il primo tavolo ha già cambiato.

#### 4.10.3 · Com'è andato 4f-1 (2026-09-24) — la partita come dato

L'elenco di cosa è partita sta in `scripts/dmcore/partita.py`: tre master da
template, cinque modelli di file da svuotare (sessioni, recap di gruppo e per
PG, `.hb.md`, brief), tre file generati da togliere (`xp-ledger`, dossier,
`group.yaml`, che porta il nome del gruppo di prima). `campaign-history.md` sta
in un elenco a parte, `PENDENTI`, e il reset lo stampa a ogni esecuzione finché
4f-2 non lo chiude. Lo esegue `scripts/azzera_partita.py`, che
`new-campaign-group.sh` chiama al posto del suo `cp` e del suo `rm`.

**L'ordine conta.** Il reset costruisce il nuovo `state.yaml` e lo passa a
`validate_state` **prima di scrivere qualunque file**: se non torna, non tocca
niente e il branch non si committa. Per poterlo fare, i controlli di
`validate_state` sono diventati una funzione, `errori()`: con due elenchi, il
giorno che se ne aggiunge uno il reset lo salterebbe.

Il template di `state.yaml` è lo scheletro (D19 resta aperta per il derivato):
i dieci archi e il Ritual Clock a 0/18 vengono da `state-blank.md`, il Day 42
dall'AP, e `png` dallo `state.yaml` di prima perché è prodotto. Il template di
`state.md` ora ha i 10 marcatori; diceva ancora «Day 40» per l'arrivo a
Rethmar, e il canone è 42.

| Prova | Esito |
|---|---|
| lo script vero, in un clone con git | ✅ branch, reset, commit: 10 file, 3.056 righe tolte; `render_state --check`, `validate_state`, `validate_docs --sorgenti` verdi sul gruppo nuovo |
| sui file veri (`test_new_group.py`, 10 test) | ✅ CI verde; nessun nome dei quattro PG nei tre master; `png` identico; `house-rules.md` intatto; il primo `session end` del gruppo nuovo scrive e la vista segue; rifarlo dà lo stesso risultato |
| l'elenco copre ogni uscita | ✅ ogni file che il manifest dichiara scritto sotto `campaign/` è in `PARTITA` o in `PENDENTI` |
| 🔴 i cancelli mordono | ✅ **5 mutazioni su 5** rosse. 🐛 La prima (una voce tolta dall'elenco) **passava**: il test confrontava i percorsi con `fnmatch`, dove `*` attraversa le cartelle e `recaps/*.md` copriva anche `recaps/homebrew/`. Ora confronta come `Path.glob`, e conta i recap direttamente |
| non-regressione | ✅ **1.244** test, `dm.py doctor --ci`, `tools_manifest --check` (74 tool) |

#### 4.10.4 · 4f-2, la proposta di split (in attesa del DM: D20)

`campaign-history.md` (630 righe) diviso secondo ADR-0050 §7, **spostando
righe senza riscriverle**. La **premessa** comprende AP, ambientazione, grafo
dei villain e riferimenti; la **cronaca** comprende il party, la timeline degli
archi e la catena dei dungeon.

| Parte (righe di oggi) | Va in | Perché |
|---|---|---|
| intestazione e PART 1: AP, Setting, System, Party Name, Theme (1-16, 18) | `campaign-premise.md` | «AP, ambientazione» |
| «Current Level: 13» (17) | `campaign-chronicle.md` | è lo stato di questo tavolo |
| The Party, No-Rogue Strategy (20-33) | cronaca | «il party» |
| PART 2, timeline degli archi (35-434) | cronaca | «timeline degli archi» |
| PART 3, catena dei dungeon (435-554) | cronaca | «con gli eventi di *questi* PG» |
| PART 4, grafo dei villain (555-587) | premessa, **tranne una parola** | «Il Collezionista (Rakshasa, **ESCAPED**)» è un evento del primo tavolo: nella premessa resta «(Rakshasa)», e la fuga passa nella cronaca con il rimando |
| PART 5 e indice dei rimandi (588-630) | premessa | «riferimenti» |

**I rimandi.** Undici file fuori da `plans/` citano `campaign-history.md`: le
quattro pagine della skill `rumblingstone-campaign`, tre file dell'arco 09, la
Cerimonia delle 100 Asce, `Belkram.md`, `dm-player-strategy.md`, `state.md`.
Due citano **un numero di riga** (`RETROATTIVI-ARC07-INFERRED.md` «r.26» e
`Belkram.md`), che dopo lo split punta altrove. I documenti di `plans/` restano
com'erano, perché sono il registro di quando sono stati scritti.

**Il cancello**: le righe delle due metà, messe insieme, sono quelle di oggi
(tranne la parola spostata), e un test verifica che la premessa non nomini i
quattro PG fuori dai titoli degli artefatti. Dopo lo split `campaign-history.md`
esce dai `PENDENTI` e la cronaca entra nella partita, con un suo template.

#### 4.10.5 · Com'è andato 4f-2 (2026-09-24) — premessa e cronaca

Il DM: *«D20 ok ma non tralasciare nulla»*.

| File | Righe | Contenuto |
|---|---:|---|
| `campaign/lore/campaign-premise.md` | 110 | intestazione nuova; AP, Setting, System, Theme; i due rimandi di testa; PART 4 (grafo dei villain) e PART 5 (riferimenti); l'indice dei rimandi |
| `campaign/lore/campaign-chronicle.md` | 564 | intestazione nuova; titolo e «single source» originali; Party Name e Current Level; The Party e No-Rogue Strategy; PART 2 e PART 3 |
| `campaign/templates/chronicle-blank.md` | — | la cronaca vuota per un gruppo nuovo; la premessa non ha template perché non si azzera |

**Niente tralasciato, e come si sa.** Le righe non banali del file di prima
erano **528**: sono tutte in una delle due metà, nessuna in entrambe.
`test_nessuna_riga_persa_nello_split` lo verifica **contro git**, cercando
l'ultimo commit in cui `campaign-history.md` esisteva, e non contro una copia
fatta al momento. L'unica riga cambiata è quella del grafo dei villain, «(Rakshasa,
ESCAPED)» → «(Rakshasa)». La fuga resta nella cronaca, che la raccontava già alle
righe 92, 94 e 459 del file di prima.

**I rimandi**: tredici, in undici file. Le quattro pagine della skill
`rumblingstone-campaign` (compresa la gerarchia delle fonti, dove la cronaca e
la premessa prendono insieme il terzo posto), tre file dell'arco 09, la
Cerimonia delle 100 Asce, `Belkram.md` e `RETROATTIVI-ARC07-INFERRED.md`
(«r.26» diventa «r.39», la stessa riga della tabella del party),
`dm-player-strategy.md`, la regola in testa a `state.md`, `AGENTS.md`.
**Restano sul nome vecchio, di proposito**, i documenti datati: `plans/`, l'audit
IP del settembre, la baseline dei punteggi del 21 settembre (lo strumento conta
già i file «spariti»), e un commento storico in `render_state.py`.

⚠️ **Un difetto di canone trovato e non corretto.** La tabella del party dà
Hella «✅ Alive (died in arc 06, resurrected as Treant Hybrid)»: è lo stato
**preparato**. Al tavolo Hella è morta (`state.yaml`, `stato: morto`). La #99
l'aveva marcato il 6 agosto e la correzione non è mai arrivata su `main`. Lo
split sposta righe e non le riscrive: la cronaca lo dichiara in testa, e la
riga si corregge nel lotto del canone, non qui.

| Prova | Esito |
|---|---|
| i test della #99, portati | ✅ i due file esistono e il vecchio no; la premessa non racconta eventi (sei stringhe, che la cronaca deve contenere tutte); la cronaca contiene i quattro PG |
| il reset | ✅ la cronaca si azzera dal suo template, la premessa resta identica; `PENDENTI` è vuoto |
| 🔴 i cancelli mordono | ✅ **3 mutazioni su 3** rosse: una riga persa, «ESCAPED» di nuovo nel grafo (la prima prova la metteva nell'intestazione, che il test esclude: era la mutazione a sbagliare), la cronaca tolta dall'elenco della partita |
| non-regressione | ✅ **1.248** test; `validate_skills` dopo il build, `validate_docs` e `--sorgenti`, `validate_modules`, `validate_bestiario`, `validate_state`, `render_state --check` |

#### 4.10.6 · D19, dopo la risposta del DM: nessun YAML a mano

**Il principio** (DM, 2026-09-24): il DM non scrive YAML. Al massimo compila
campi o sceglie valori da un modulo già impostato.

**Dove il repo lo viola oggi**, misurato:

| Posto | Cosa dice al DM |
|---|---|
| `new-campaign-group.sh` (scritto in 4f-1) | «Fill `campaign/state.yaml`: party, first villains» |
| `dmcore/masters.py`, nota di `DATI` | ogni proposta non meccanica di fine sessione va scritta in `state.yaml`, poi `render_state` |
| skill `rumblingstone-automation`, tabella dei tre master | `state.yaml`: «**qui**, poi `render_state.py`» |

**Perché il template non può essere derivato del tutto in automatico.** Nello
`state.yaml` di oggi, cercando i nomi dei PG, i giorni di marcia e i verbi di
esito, portano tracce del primo tavolo **9 agende villain su 13**, **4 righe di
difensori su 9**, **4 artefatti su 8** e **3 archi su 22** (conto euristico,
con falsi positivi possibili). Quelle righe hanno bisogno di un giudizio, e il
giudizio resta del DM. Si può però ridurlo a una scelta.

**La procedura proposta:**

| | Sotto-lotto | Cosa fa | Il DM |
|---|---|---|---|
| **4f-4** | il gruppo nuovo da un modulo | `dm.py gruppo nuovo` fa il branch, il reset e il modulo della sessione 0. Il template è **derivato**: villain con agenda, trigger e `png_id` preparati, clock a zero, `stato: attivo`; archi tutti da giocare; numeri di Rethmar come preparati; artefatti senza portatore. Le righe con tracce del primo tavolo si presentano **una alla volta**, con tre scelte: tieni, svuota il campo, segna da rivedere. «Da rivedere» diventa una voce `inferred`, il meccanismo che il repo usa già per le domande aperte | scrive il nome del gruppo e i PG (nome, classe, livello); **sceglie** arco di partenza e risposte |
| **4f-5** | le proposte diventano domande | le proposte non meccaniche di `state_apply` (alleanze, party, conoscenze) non dicono più «scrivi in `state.yaml`»: diventano domande dello stesso modulo, con i valori possibili già elencati e la scrittura validata come quella del delta | sceglie |
| — | documenti | le tre righe della tabella qui sopra | — |

**Il contratto è il JSON delle risposte, non il modulo.** È la forma che
`session_wizard --answers` usa già: il modulo in terminale lo produce oggi, e
una pagina locale potrà produrlo domani senza toccare la logica. È anche ciò che
rende tutto testabile senza tastiera.

⚠️ **Quello che l'automazione non toglie**: le nove agende restano un giudizio
del DM. Il modulo gli risparmia di aprire un file e di scrivere YAML, non di
decidere se l'agenda di Xal'thor, *«to seize Tordek's Bracieri Gemelli»*, vale
anche per un tavolo dove Tordek non c'è.

### 4.11 · Lotto **4i** — i rimandi fra backtick, e il contenuto rimasto nei rami `[✅ chiuso il 2026-09-24 · 4i-1 · 4i-2 · il destino dei file è D22, la protezione del ramo è D23]`

> **Classe R** (ricognizione) per la misura, **M** per le correzioni con una
> sola risposta possibile. Le righe il cui destino è un giudizio sul contenuto
> vanno al DM e non si toccano. Richiesta del DM del 2026-09-24: *«verifica
> perché validate docs non controlla i rimandi rotti […] controlla che non si
> sia perso in tutte le PR, anche quelle chiuse»*.

#### 4.11.0 · FASE 1 · Perché il gate non l'ha visto

Il lotto 4f-2 ha tolto `campaign-history.md`, e tre piani che lo citavano fra
backtick sono rimasti verdi. `validate_docs --sorgenti` controllava i **link**
markdown su tutto il repo, ma i percorsi fra backtick solo sui tre documenti
d'ingresso. L'esclusione era scritta in §4.2-ter con un motivo onesto: «una
superficie di falsi positivi che nessuno ha misurato». Nessuno l'ha mai
misurata.

🔎 **Il controllo era già esistito.** `scripts/validate_skill_paths.py`, scritto <!-- validate-docs: ignore -->
il 2026-05-02 nella review della PR #1, faceva proprio questo sulle skill. È
stato spinto sul ramo `optimize-skills-agent-folders` **dopo** il merge della
PR, insieme a `scripts/agents.conf`: nessuno dei due è mai arrivato su `main`. <!-- validate-docs: ignore -->

**Misurato il 2026-09-24**, prima di scrivere il controllo: **180 percorsi**
inesistenti in **823** documenti. I falsi positivi erano 45, in quattro famiglie
che il repo sa già riconoscere senza una lista a mano:

| Famiglia | Da dove viene la risposta |
|---|---|
| segnaposto (`…`, `...`, `a\|b`) | il testo stesso |
| file che uno script crea quando gira (recap, brief, ledger) | `tools.manifest.json` (uscite) e `dmcore/partita.py` |
| cloni locali di terzi (ComfyUI, Homebrewery) | `git check-ignore` |
| numero di riga attaccato (`file.py:42`) | il testo stesso |

Il resto erano rimandi rotti veri, quasi tutti al Bestiario di prima del
riordino in `mostri/`, `villain/`, `png/`.

#### 4.11.1 · 4i-1 · Com'è andato (2026-09-24)

**Il controllo.** `percorsi_inline()` in `validate_docs.py`, chiamato da
`--sorgenti`, quindi già in CI senza un job nuovo. Resta fuori chi fa da
registro: `plans/adr/`, `docs/audit/`, `CHANGELOG`, `REGISTRO-LOTTI`,
`state-changelog.md`, gli `_ARCHIVIO/`. I loro link restano controllati.

**Il marcatore nuovo, `<!-- validate-docs: futuro -->`**, per il piano che
nomina un file che ancora non c'è. Scade da solo: quando il file arriva, la
riga diventa rossa, perché il piano sta dicendo «da fare» di una cosa fatta.
Chi nomina un percorso per dire che non esiste (`campaign/npcs/` «non è mai <!-- validate-docs: ignore -->
esistita») usa la direttiva `ignore` che c'era già.

**Le correzioni**: 122 righe in 32 file, più il documento recuperato.

- **96 percorsi** risolti da un criterio solo: il nome del file compare
  **una volta sola** nel repo. Nessuna scelta fra due candidati.
- **Due errori di taratura del controllo**, corretti nel validatore e non nei
  documenti: `git check-ignore` non riconosce come cartella una cartella che non
  esiste, e le voci `ComfyUI/` e `homebrewery/` di `.gitignore` non scattavano.
- **Rimandi vivi riscritti**: `rhod-adaptations.md` (mai esistito) diventa
  `campaign-coherence.md`, che `AGENTS.md` regola 5 dà come sede canonica;
  `campaign/npcs/` e `campaign/encounters/` escono da due skill; <!-- validate-docs: ignore -->
  `campaign-history.md` diventa `campaign-chronicle.md` in quattro piani, con la
  metà verificata sul testo (la tabella del party e le linee dell'orda stanno
  nella cronaca).
- **Cose superate nei piani, riallineate**: il lotto E1 di
  `PIANO-EDITOR-VISUALE-MAPPE` (la legenda esportata in JSON con un gate di
  sincronia) era fatto dal 2026-09-12 per altra via, con ADR-0048, e il piano e
  `INDEX.md` lo davano da fare. La ricerca sui font citava `scripts/typst/fonts/`, <!-- validate-docs: ignore -->
  oggi `scripts/fonts/`.
- **Un documento recuperato**: `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md`
  della PR #72. ADR-0040, ADR-0048 e `LEGENDA-FUNZIONALE-SPEC` ne citano delle
  sezioni, e il file non c'era. Portato com'era, con una testata che lo
  dichiara datato; le misure del 26 luglio non sono rifatte.
- **Futuri dichiarati**: quattro file di `PIANO-PIPELINE-IBRIDE`, uno di
  `RICERCA-TOOL-ESTERNI`, uno di `house-rules.md`.

**Validazione.** Nove test nuovi in `test_validate_docs.py`, fra cui il caso di
`campaign-history.md` preso com'era e il cablaggio in `main()`. **7 mutazioni
su 7** rosse: controllo muto, `main` che non lo chiama, `futuro` che non scade,
niente barra finale, datati allargati a tutto `plans/`, numero di riga non
tolto, uscite di partita dimenticate.

🐛 **Un errore mio di 4f-2, trovato da questo lotto.** Correggere un percorso
nella cronaca ha fatto cadere `test_nessuna_riga_persa_nello_split`: il test
confrontava lo split con i file **di oggi**, e la cronaca è partita, cambia a
ogni sessione. Sarebbe caduto alla prima sessione giocata. Adesso legge i due
file com'erano nel commit dello split; la mutazione (tolta la riga spostata)
lo fa ancora rosso. E la stessa correzione nella scheda di Tyrgarun ha mosso
l'impronta delle creature: rigenerata **in un commit suo**, come chiede il test,
con la sola chiave che cambia.

⚠️ **Limite dichiarato**: il controllo vede un percorso con almeno una barra e
la prima cartella esistente. Un nome di file nudo (`campaign-history.md` senza
cartella) non lo vede. Cercati a mano nei documenti vivi: due erano rimandi, nei
piani di ARC-07 e ARC-09, e sono riscritti; gli altri raccontano la storia dello
split e restano. `campaign/misure/baseline-punteggi.json` lo nomina ancora ed è
una misura datata: resta com'è.

#### 4.11.2 · 4i-2 · Il contenuto rimasto nei rami

Misurato il 2026-09-24 su **217 riferimenti** (rami e teste di PR, chiuse
comprese): i file che esistono in un ramo e **non sono mai esistiti su `main`**
né col loro nome né col loro contenuto. Sono **61 percorsi**. Quasi tutti hanno
già un posto: la #99 aperta (4g, 4h), questa PR, la #143 (portata come
ADR-0067), la #42 e la #109 chiuse con motivazione, la #67 giudicata in
`RICONCILIAZIONE-PR` R5, il ramo di gruppo del primo tavolo (partita, per
ADR-0007). **Senza posto**:

| Dove | File | Stato |
|---|---|---|
| ramo della PR #1, dopo il merge | `scripts/validate_skill_paths.py` | superato da 4i-1 per i markdown <!-- validate-docs: ignore --> |
| ramo della PR #1, dopo il merge | `scripts/agents.conf` | ⚠️ **il difetto che correggeva c'è ancora**: la matrice degli agenti è duplicata in `build-skills.sh` e `sync-skills.sh` <!-- validate-docs: ignore --> |
| PR #72 | `SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05.md`, 773 righe, sei revisioni con risposte del DM | 🔴 **nessun documento lo nomina**. Dice di sé: gli archi 01, 02, 03, 05 non hanno un solo markdown, e la catena «se si perde, si perde dalla testa del DM». La sua integrazione in `campaign-history` (133 righe) **è arrivata**; il soggetto no |
| PR #72 | `plans/PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md` | ADR-0048 lo nomina come fonte del proprio lotto A1 <!-- validate-docs: ignore --> |
| ramo `review-tournament-integration` | una versione di maggio del Giorno 3 di Dauth (228 righe) | il file su `main` è stato riscritto da zero a luglio (ARC09 lotto A, «i tre orfani»); le due versioni non sono mai state confrontate |

Il destino di queste righe è la **D22**.

#### 4.11.3 · 4i-2 · Com'è andato (2026-09-24)

**Lo strumento.** `scripts/contenuti_nei_rami.py` rifà la misura qui sopra in
quattro secondi. Un file è «mai arrivato» se su `main` non c'è mai stato né il
suo percorso né il suo contenuto: un ADR rinumerato col testo identico non
conta come perso, un file riscritto con un altro nome sì. `--fetch` scarica le
teste di tutte le PR, chiuse comprese.

**Il registro**, `plans/contenuti-nei-rami.json`, dà un posto a ogni riga: per
ramo intero (la #99 e questa PR in volo, la #42 rifiutata, la #67 e la #109
superate, la #143 portata, i rami di gruppo che sono partita) o per file (i
quattro ADR della #72 portati con altri numeri, l'ADR-0015 rifiutato, i due
piani commerciali assorbiti da `PIANO-VENDIBILITA`). Oggi: **65 file, 0 senza
posto, 4 in attesa del DM**. `--check` esce 1 se ne compare uno nuovo senza
posto; una voce che non trova più niente viene segnalata come scaduta, perché
il file è arrivato o il ramo non c'è più.

**Dove si vede senza cercarlo.** `fase1.py`, al passo 3, mostra i file ancora
aperti nella stessa cartella del bersaglio. Provato sul piano dell'editor: esce
`PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md` della #72, che è esattamente il
lavoro che un piano nuovo sull'editor rischierebbe di riscrivere da zero.

🐛 **Un test ha mentito al primo giro.** Il default di `leggi_registro()` era
legato alla definizione, quindi `main()` leggeva sempre il registro del repo:
il test «rosso senza posto» passava per il motivo sbagliato, e l'ha scoperto il
test gemello «verde col posto». Dodici test, **7 mutazioni su 7** rosse sullo
strumento e una sul filtro di `fase1.py`.

⚠️ **Limiti dichiarati.** Vede i file, non le modifiche: un commit spinto dopo
il merge che corregge un file già su `main` non compare (il commit `b5e04d2`
della PR #1 toccava `AGENTS.md` e `sync-skills.sh`, ed è di questo tipo). E non
è un gate di CI, di proposito: i rami cambiano per conto loro, e una PR
diventerebbe rossa per il lavoro di un'altra.

#### 4.11.4 · La regola chiesta dal DM: ha senso?

La domanda: *«vedi se ha senso aggiungere questa nuova regola in modo che tutte
le PR sono aggiornate con l'avanzamento dei piani, evitando regressioni o
overdrive»*.

**Una regola d'oro nuova no.** Ogni via da cui il difetto entrava ha adesso un
meccanismo che non chiede disciplina:

| Come si perdeva | Cosa lo vede adesso |
|---|---|
| una PR cita un file che un'altra PR ha tolto | `validate_docs --sorgenti` (4i-1), in CI su ogni PR |
| un file resta su un ramo chiuso, o spinto dopo il merge | `contenuti_nei_rami.py` e il suo registro (4i-2) |
| un piano nuovo riscrive lavoro che stava in una PR | `fase1.py` passo 3, cioè G6, che è già obbligatoria prima di toccare |

Resta un buco che nessuno script del repo può chiudere. La CI di una PR gira
sul `main` del momento del push: se `main` cambia dopo, la PR resta verde su
una base che non c'è più, e il merge porta dentro la regressione. È successo a
questa PR in piccolo: lo split di 4f-2 ha rotto tre rimandi che la CI non
poteva vedere. Su GitHub la cura è un'impostazione del ramo `main`,
*«Require branches to be up to date before merging»*: prima del merge la PR va
riallineata e la CI rigira. Si attiva dalle impostazioni del repository, e da
qui non si può né attivare né verificare. È la **D23**.

L'«overdrive», cioè una PR che fa più di quanto il suo piano dichiara, ha già
la sua regola: piano, `INDEX` e `CHANGELOG` nello stesso commit, bloccata in
CI da `check_plans_discipline.py`. Non serve altro.

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
