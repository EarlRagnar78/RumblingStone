# RICERCA — Un rilevatore di conformità 3.5/PF1e è fattibile? L'audit di parsabilità

> **Cos'è**: la misura che risponde alla domanda del DM del 2026-09-21 —
> *«ha senso fare dei detector che verificano la conformità 3.5 e PF1e, in modo
> da marcare le sezioni con prove e statblocchi e misurare dove i valori sono
> errati?»*. Non propone un rilevatore: misura **se si può scrivere**, e su
> quanti documenti.
>
> **Perché una ricerca e non un piano**: la domanda era «ha senso?», e la
> risposta onesta richiede di contare prima. Un piano che partisse senza questo
> conto misurerebbe il proprio parser invece del contenuto — è il difetto che
> questo repo ha catalogato venti volte.
>
> **Metodo**: conteggio deterministico su `Bestiario/*/*-cr*.md`, eseguito il
> 2026-09-21. Riproducibile.

## 1 · Cosa questa ricerca NON rifà

- **`PIANO-GENERATORE-CREATURE-E-PNG`** va nella direzione opposta: da
  (GS + ruolo + tipo) **produce** un blocco. Qui si **verifica** un blocco che
  esiste già. I due si incontrano il giorno in cui il generatore usa il
  verificatore come collaudo.
- **`npc-villain-boosting`** e il tetto `EL ≤ APL+4` riguardano la
  **difficoltà dell'incontro**, non l'aritmetica interna di una creatura.
- **`validate_bestiario.py`** presidia già **struttura, naming, GS coerente col
  nome del file e catalogo in sync**. Questa ricerca guarda solo i **numeri**.

---

## 2 · La superficie: 231 file, 110 che portano numeri

| | Quanti | % |
|---|---:|---:|
| file in `Bestiario/` | 231 | |
| statblocchi con GS nel nome | 182 | |
| — di cui **`[POINTER]`**, che per progetto **non portano numeri** | **72** | 40% |
| — di cui **statblocchi veri** | **110** | 60% |

🔎 **I 72 POINTER non sono un buco**: dichiarano che i numeri stanno nel file
d'arco, per non tenerne due copie che divergono alla prima correzione
(ADR-0021). Contarli fra i «non misurabili» gonfierebbe il debito con righe che
si chiudono togliendo una regola giusta.

## 3 · Il formato è strutturato, ed è la buona notizia

Gli statblocchi veri usano un blocco ```` ```statblocco ```` con campi
espliciti. Sui **110**:

| campo | presente in | % |
|---|---:|---:|
| `gs` | 108 | 98% |
| `ca` | 108 | 98% |
| `pf` | 108 | 98% |
| `ts` | 108 | 98% |
| `ca-dettaglio` | 104 | 95% |
| `pf-dado` | 95 | 86% |
| `attacchi` | 65 | 59% |
| **`attributi`** | **14** | **13%** |

Il GS si legge dall'intestazione nel **100%** dei casi.

---

## 4 · 🐛 Il rilevatore esiste già, e legge il campo sbagliato

`validate_bestiario.py --rules` confronta **da luglio** il GS dichiarato con il
benchmark *Monster Statistics by CR* di PF1e. Gira in CI come **avviso, non
cancello**, e stampa **zero avvisi**.

Lo zero non vuol dire che vada tutto bene. Le sue due regex cercano `hp N` e
`ac N`, mentre il formato canonico scrive `pf:` e `ca:`:

| | legge | su 110 |
|---|---:|---:|
| `hp` (cerca `hp N`) | 54 | **49%** |
| CA (cerca `ac N`) | 64 | **58%** |
| il campo canonico `pf:` / `ca:` | 108 | **98%** |

⚠️ **Ma non legge spazzatura, e va detto.** Sui **53** file dove entrambe le
forme compaiono, il numero che estrae **coincide sempre** con il `pf:`
canonico: 53 su 53. Il difetto è **copertura**, non correttezza — vede metà
della libreria e tace sull'altra metà. Ventunesimo caso della famiglia «un
criterio che non pesca si traveste da repo pulito», e il più mite finora.

**Il primo lotto è quindi minuscolo**: far leggere al controllo i campi che il
repo usa davvero porta la copertura dal **49% al 98%** senza scrivere un
rilevatore nuovo. È lo stesso schema di F2.7.

---

## 5 · Cosa si può verificare, e cosa no

La domanda del DM era se le skill `dnd-35-srd` e `pathfinder-1e-srd` possano
servire a un controllo deterministico. ⚠️ **Una skill è testo di riferimento
per un agente, non una tabella leggibile da uno script**: i numeri vanno
estratti in un dato versionato. Fatto quello, ecco cosa regge e cosa no.

| Identità da verificare | Serve | Copertura | Verdetto |
|---|---|---:|---|
| **GS vs benchmark PF1e** (pf e CA nella fascia della sfida) | `gs`, `pf`, `ca` | **98%** | 🟢 **fattibile**, e il codice c'è già |
| **CA interna**: contatto e sprovvista **non superano** la CA | `ca`, `ca-dettaglio` | **95%** | 🟢 **fattibile** — misurato: **0 violazioni** su 104 |
| **pf dai DV e dalla Costituzione** | `attributi` | **13%** | 🔴 **no**: è `SUPERFICIE_VUOTA` (ADR-0062) |
| **TS dalla progressione di classe** | `attributi`, DV | **13%** | 🔴 **no**, stesso prerequisito |
| **attacco = BAB + modificatore + taglia** | `attributi`, `tipo` | **13%** | 🔴 **no**, stesso prerequisito |

🔴 **Il muro è uno solo, ed è un dato che manca: le caratteristiche.** Solo
**14 statblocchi su 110** dichiarano `attributi`. Senza For/Des/Cos non si
ricava nessuna delle tre identità profonde — e scrivere il rilevatore lo stesso
darebbe `0 violazioni` su un insieme vuoto, che è indistinguibile da
`0 violazioni` su una libreria corretta. È esattamente il caso che ADR-0062
esiste per non far ripetere.

---

## 6 · Cosa propone

| | Lotto | Costo | Cosa sblocca |
|---|---|---|---|
| **1** | far leggere a `--rules` i campi `pf:` e `ca:` | **due regex** | copertura **49% → 98%**, senza rilevatori nuovi |
| **2** | la coerenza interna della CA (contatto ≤ CA) | piccolo | oggi **0 violazioni**: nasce verde, presidia le prossime |
| **3** | promuovere `--rules` da **avviso** a **cancello** | una riga di CI | ⚠️ **solo dopo** il lotto 1: promuoverlo adesso renderebbe bloccante un controllo che vede metà libreria |
| **4** | la tabella PF1e in un YAML versionato accanto a `specifiche-qualita.yaml` | medio | il dato esce dal codice, e lo può correggere il DM |
| **5** | 🔵 **decisione del DM**: si dichiarano gli `attributi` nei 96 statblocchi che non li hanno? | **alto, e non è codice** | è l'unica porta verso le tre identità profonde, e verso il **primo `critico`** del punteggio |

🔎 **E il lotto 5 è il vero snodo.** La FASE 3 del `PIANO-MISURA-EDITORIALE` ha
misurato il 2026-09-21 che il κ è **0,0** perché la metrica promuove tutto: le
serve una norma che morda. Una verifica aritmetica su uno statblocco sarebbe
`critico` — un documento con i numeri incoerenti è ingiocabile — e sarebbe la
prima. Ma con `attributi` al 13% morderebbe su tredici documenti su cento.

⚠️ **Il conto onesto del lotto 5**: 96 statblocchi da completare a mano, e le
caratteristiche di una creatura non si indovinano. Dove la fonte è un export
PCGen i numeri esistono e si trascrivono; dove la creatura è originale, le
sceglie il DM. È lavoro di canone, non di codice, e per questo è una decisione
e non un lotto.

---

## 7 · Come si riproduce questa misura

```bash
python3 scripts/validate_bestiario.py --rules   # oggi: 0 avvisi, e §4 spiega perché
grep -c '^pf:' Bestiario/*/*-cr*.md | grep -c ':1'
grep -rl '^attributi:' Bestiario --include='*.md' | wc -l
```
