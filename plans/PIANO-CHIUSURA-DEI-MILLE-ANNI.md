# PIANO — La chiusura dei mille anni: cosa il viaggio deve consegnare davvero

> **Cos'è**: portare `ARC07-DEF-4` a consegnare ciò che il **canone dice che il
> viaggio consegna**, e non solo il duello. La riscrittura del 2026-09-18 ha
> sistemato il mestiere; questo piano chiude i **buchi di canone** che il
> mestiere non poteva vedere.
>
> **Stato**: ✅ **completo** (2026-09-19) · **Decisore**: DM
> **Gate**: `validate_modules` verde, `misura_craft` senza regressioni, e le
> tre righe di `state.md` sul Rituale 4 trovano un riscontro nel master

---

## 0 · Il perno, in una riga

`state.md` §5 dice che **mancano Corona +3, Senzienza e il Rubino, e «si
sbloccano col Rituale 4 = viaggio a −1.000»**. La matrice degli artefatti gli
dà anche un nome: **«Siege of the Eternal Forge»**.

Misurato su `ARC07-DEF-4` (1.325 righe):

| Parola del canone | Occorrenze nel master |
|---|---:|
| Rubino | 26 🟢 |
| Skullcrusher | 58 🟢 |
| 372 DR | 32 🟢 |
| **Rituale 4** | **0** 🔴 |
| **Corona +3** | **0** 🔴 |
| Senzienza | **1** 🔴 |

> **Il master consegna un duello. Il canone dice che consegna anche il
> completamento della Corona.** Non è una svista di stile: è un pezzo di
> canone che esiste in `state.md` e non esiste dove si gioca.

---

## 1 · I cinque buchi, misurati — **quattro chiusi, uno era del metro**

### 🔴 G1 — Il Rituale 4 non ha un nome nel posto dove si gioca

Il viaggio **è** il Rituale Legacy 4. La matrice artefatti lo registra come
*Siege of the Eternal Forge*, con esito *«buff forza/coraggio 1/settimana;
Mantle of Stone and Spirit; il Rubino si consuma nel ritorno al 1372 (D16)»* e
stato ⬜ **da giocare**. Nel master quel nome non compare, e nemmeno il
passaggio in cui la Corona **cambia grado**.

**Conseguenza al tavolo**: il DM gioca il duello, torna, e `state.md` gli
chiede di segnare un avanzamento d'artefatto che nel modulo non è mai successo.

### 🔴 G2 — Il viaggio **è** l'Assedio, e l'Assedio sveglia Aegis Fang

> 🔴 **CORREZIONE (2026-09-19, FASE 1).** La prima stesura di questo piano —
> commit `3a7238a`, già spinto — diceva che donando il +2 di deflessione **la
> Corona non parlerà mai** e che si **rompe** la condizione di risveglio di
> Aegis Fang, *«Assedio della Forgia + Corona Senziente»*. **Era falso**, e la
> FASE 1 l'ha preso al primo controllo.
>
> | Avevo scritto | Il canone corrente |
> |---|---|
> | la Corona non parlerà mai | `state.md` §456: *«la Corona si scalda **o resta fredda al Rituale 4** — tutte **reversibili**»*, e `ARC07-DEF-3` §5 lo conferma su entrambi i rami |
> | Aegis Fang richiede «Corona Senziente» | **«Corona Senziente» ha 0 occorrenze in `state.md`.** La riga vera è: *«Unchanged until the **Siege (P5)** is won → then Stage 1 full awakening»* |
>
> **Da dove veniva l'errore**: da `PROPOSTA-DONI-RESURREZIONE-HELLA` §III, che
> è una versione **superata** del disegno dei Doni — quella in cui il dono III
> *era* la Senzienza stessa. Nel canone v4-bis Thorik dona il **+2 di
> deflessione**, e la Senzienza non è in gioco. Avevo letto un documento di
> proposta come se fosse canone: è l'errore che la regola 8 esiste per
> impedire, e l'ho fatto nel piano che la cita.

**Il buco vero, verificato, è più semplice e più grosso.** Il viaggio a −1.000
**è** l'Assedio (P5). `state.md` dice che vincerlo sveglia **Aegis Fang allo
Stage 1**. Misurato su DEF-4: «Aegis» compare **14 volte**, il suo **risveglio
zero**.

| Cosa il canone attribuisce al viaggio | DEF-4 lo consegna? |
|---|---|
| Rubino acceso | 🟢 sì, 26 occorrenze |
| Corona a tre gemme | 🟢 sì, nel §9 |
| **Corona +3 / Rituale 4** | 🔴 **no**, zero |
| **Senzienza, calda o fredda secondo il ramo di DEF-3 §5** | 🔴 **no**, una menzione |
| **Aegis Fang → Stage 1** | 🔴 **no**, zero |

**Quindi**: DEF-3 §5 fa una **promessa** — *«al Rituale 4 la Senzienza si
sveglierà avendo già una cosa da dire su di lui»*, oppure *«arriva fredda»* —
e DEF-4 **non la incassa**. Il bivio esiste già nel canone; manca il posto
dove si paga.

### 🟢 G3 — La cucitura del ritorno: **verificata, regge**

Il Rubino **si accende** a −1.000 alla vittoria (DEF-4 §636-638) e **si
consuma** nel ritorno al 1372 (DEF-5 §3). I quattro riemergono al **Cuore
della Montagna, Giorno 3 dell'assedio**: DEF-4 §9 e l'apertura di DEF-5 dicono
la stessa cosa con le stesse parole. La scala mappa di CM-1 eredita
dichiaratamente i 3 m della geometria ARC-08. **Nessuna contraddizione.**

### 🔴 G5 — «−2 COS»: sei righe che il canone ha smentito, e nessuno le ha tolte

🔎 **Trovato da M1.4, cercando altro.** `state.md` riga 93 dice, in grassetto e
con l'avviso: **«⚠️ Nessun −2 COS.»** Thorik ha **+2 COS** dal rito dello
Smeraldo, e il costo della resurrezione **non è ancora versato**.

Tre master d'arco dicono il contrario, in **sei punti**:

| File | Dove | Cosa dice |
|---|---|---|
| `ARC07-00-INDICE.md` | r. 41 | «Thorik **−2 COS**» nel canone in uscita |
| `ARC07-DEF-4` | r. 318 | «Cosa NON guarisce: i **−2 COS permanenti** di Thorik» |
| `ARC07-DEF-5` | r. 26 · 92 · 127 · 370 | quattro volte, incluso il **canone in uscita** dell'arco |

**Chi è più recente**: `git log -S` dice che «Nessun −2 COS» è entrato in
`state.md` il **2026-09-12** col commit `d4eea53` — il redesign dei **Doni v2**,
quello il cui titolo di lotto era testualmente *«3 scelte per PG, niente −2
COS»*. `state.md` e DEF-3 furono aggiornati; **i file a valle no**.

⚠️ **Non è un refuso, è un costo permanente su un PG** che tre documenti
attribuiscono e uno nega. Un DM che prepara DEF-5 applica −2 COS a Thorik.

### 🟢 G4 — Il mestiere: **il difetto era nel metro, non nei box**

> 🔴 **CORREZIONE (2026-09-19, M2.5).** Avevo pubblicato «**9 box su 14** con
> più di un nome proprio» per DEF-4, «**13 su 16**» per DEF-3, e la stessa
> cifra nel corpo della PR #151. **Erano gonfiate fino a tre volte.**
>
> Il rilevatore contava come nomi propri le **maiuscole d'inizio frase** —
> «Conoscete», «Quando», «Prima», «Notte», «Quei», «Nessun», «Silenzio» —
> perché i due lookbehind che dovevano escluderle non arrivavano mai al testo:
> il prefisso `>`, l'asterisco del corsivo e l'etichetta si frappongono fra il
> punto e la maiuscola.
>
> **Tre patch di posizione hanno solo spostato l'errore**, perché in italiano
> una maiuscola segue anche il trattino, i due punti e l'apertura di un
> dialogo. La cura non è una regex più furba né una lista scritta da me: è il
> **registro che il repo già possiede** — i nomi dei file del `Bestiario` e la
> prima colonna delle tabelle di `state.md`. **322 nomi**, presi dai dati.

| | DEF-4, col metro corretto |
|---|---:|
| box read-aloud | 18 |
| **oltre le 12 righe** | **0** 🟢 |
| con parentesi | 2 🟡 |
| **con più di un nome proprio** | **3** *(non 9)* |
| box che presuppongono un'azione del giocatore (*Dungeon*) | 2 su 41 🟢 |

🔎 **E i tre non sono violazioni.** Sono *«Mano Rossa»* + *«Skullcrusher»*
dentro la profezia incisa, *«Cuore della Leggenda»* + *«Hammerfist»*, e
*«Anello»* + *«Artemis»*: due su tre sono **un nome solo spezzato in due
parole**, e tutti sono nomi **noti da sei sessioni**. La norma dice «un solo
nome proprio **NUOVO**», e *nuovo* dipende dall'ordine di lettura: una
macchina non lo sa, e il metro ora lo **dichiara**.

---

## 2 · Assunzioni dichiarate

1. **Il canone vince sul modulo.** Dove `state.md` e il master divergono, si
   allinea il master — mai il contrario senza decisione del DM (regola 8).
2. **G2 non si chiude inventando canone.** Il bivio **esiste già** in DEF-3 §5
   e in `state.md`: qui si scrive solo **dove si incassa**. ⚠️ E vale la
   correzione di G2: prima di usare una riga come canone, si verifica che sia
   in `state.md` e non in un documento di **proposta** superato.
3. **La riscrittura di ieri non si tocca.** I congegni introdotti (regia di
   round, quarta colonna, `[HDYWTDT]`) restano; questo piano **aggiunge**.
4. **Il duello con Skullcrusher è collaudato sulla carta e non al tavolo.**
   Niente qui lo cambia.

---

## FASE 1 — Audit / accertamento ✅ **chiusa**

| | Lotto | Cosa produce | Come si verifica |
|---|---|---|---|
| ✅ | **M1.1** Copertura del canone dei −1.000 | la tabella di §0 | fatta: 3 parole su 6 a zero |
| ✅ | **M1.2** Stato del mestiere di DEF-4 | la tabella di G4 | fatta |
| ✅ | **M1.3** Il ramo Senzienza, tracciato su tre archi — **ha trovato l'errore di G2** | dove la scelta si fa (DEF-3 §5), dove si paga (DEF-4), dove rimbalza (ARC-09 + Aegis Fang) | ogni passaggio o esiste in un file o è un buco elencato |
| ✅ | **M1.4** La cucitura D16 riga per riga | 🟢 **regge** (G3) — ma cercando ha trovato **G5**: sei «−2 COS» che `state.md` smentisce | fatta |
| ✅ | **M1.5** `ARC07-CONSEGUENZE-ECHI.md` conosce il bivio? | **no**: Senzienza 0 · deflessione 0 · Rituale 4 0 · Corona +3 0 · Aegis Fang 1 | misurato |

## FASE 2 — Sviluppo

L'ordine è quello di esecuzione, ed è scelto perché **ogni lotto rende più
facile il successivo**.

| | Lotto | Cosa fa | Perché qui |
|---|---|---|---|
| ✅ | **M2.0** 🔴 **Le sei righe «−2 COS»** *(chiuso 2026-09-19, D-D confermata)* | allineare `ARC07-00-INDICE`, `DEF-4` r.318 e `DEF-5` (4 punti) a `state.md` — con la ragione scritta e il rimando al commit `d4eea53` | **primo, e prima di scrivere qualunque riga nuova**: lasciare una contraddizione viva dentro il file che sto per ampliare vuol dire rischiare di ripeterla |
| ✅ | **M2.1** §4-quater «Il Rituale della Forgia Eterna» | la scena in cui il Rubino entra nella Corona **durante o dopo il duello**, col nome canonico, e la Corona passa a **+3** | è il buco G1, ed è il pezzo che tutti gli altri presuppongono |
| ✅ | **M2.2** Il bivio della Senzienza | dentro M2.1: **due rami scritti**, «Thorik ha donato» e «Thorik non ha donato», con cosa cambia **al tavolo** in entrambi | senza, M2.1 vale per metà dei tavoli |
| ✅ | **M2.3** Il risveglio di **Aegis Fang** *(riscritto dopo la correzione di G2)* | vincere l'Assedio porta l'ascia allo **Stage 1**: il master lo deve **consegnare**, non lasciarlo a `state.md`. E l'Ego 14 ha una cosa da dire su Thorik, diversa nei due rami di DEF-3 §5 | è l'altro avanzamento che il canone attribuisce a questo viaggio e che il modulo non nomina |
| ⬜ | **M2.4** Cucitura D16 | correggere ciò che M1.4 trova | dopo M2.1, perché il Rituale cambia cosa arriva a DEF-5 |
| ✅ | **M2.5** ~~I nove box~~ → **verificato: non ha senso riscriverli** *(D-C, 2026-09-19)* | la verifica che il DM ha chiesto ha trovato che i nove erano **tre**, e che i tre non violano la norma. Il lotto si chiude **correggendo il metro**, non la prosa | il guadagno misurato è zero: riscrivere prosa buona per inseguire un numero sbagliato sarebbe stato il danno |
| ✅ | **M2.6** Echo Ledger | le conseguenze nuove in `state.md` §7.E e in `ARC07-CONSEGUENZE-ECHI.md` | la regola: un'eco che non è nel registro non riemerge |

## FASE 3 — Validazione ✅ **chiusa (2026-09-19)**

| | Criterio | Come si prova |
|---|---|---|
| ✅ | **V1** Le tre parole del canone hanno un riscontro | `Rituale 4`, `Corona +3`, `Senzienza` compaiono dove si gioca, non solo in `state.md` · 🟢 **superata**: Rituale Legacy 4 ×3 · Siege of the Eternal Forge ×1 · Corona +3 ×2 · Senzienza ×4 · Stage 1 ×4 |
| ✅ | **V2** Entrambi i rami sono giocabili | un DM che legge solo DEF-4 sa cosa fare **sia** se Thorik ha donato **sia** se no · 🟢 «ha donato» ×4 · «ha rifiutato» ×3, con la battuta della Corona e quella dell'ascia in tutti e due |
| ✅ | **V3** Nessuna regressione di mestiere | `misura_craft --densita`: nessun congegno di DEF-4 scende · 🟢 **zero congegni scesi** rispetto a `6ae0b0c`, confrontati uno per uno |
| ✅ | **V4** I box migliorano davvero | `--box`: **da 9 a ≤4** con più di un nome proprio, e **0 oltre le 12 righe** · ⚠️ **riformulata**: il bersaglio «da 9 a ≤4» era tarato su una cifra sbagliata. Il criterio che regge è **zero box oltre le 12 righe** → **0** 🟢 |
| ✅ | **V5** Il canone non si contraddice | `validate_modules` verde · rilettura di `campaign-coherence.md` · 🟢 `validate_modules` 5 master 0 errori · zero «−2 COS» residui |
| ✅ | **V6** Il cancello morde | iniettare una contraddizione col canone → deve emergere in V5 · 🟢 **tre sabotaggi, tre rossi**: box gonfiato a 15 righe → rilevato · «Rituale 4» rimosso → V1 fallisce · «−2 COS» reintrodotto → ricompare. File ripristinato identico |

---

## 3 · L'ordine che propongo, e perché

1. ✅ **FASE 1 chiusa.** Ha prodotto due cose che nessuno cercava: la
   **correzione di G2** e il ritrovamento di **G5**.
2. **M2.0** — le sei righe «−2 COS», da sole e per prime. È igiene di canone,
   non richiede decisioni, e va fatta prima di ampliare quei file.
3. **M2.1 → M2.2 → M2.3** — un commit solo: sono la stessa scena.
3. **M2.4** — piccolo, e chiude l'arco verso DEF-5.
4. **M2.6** — le eco, mentre il contenuto è fresco.
5. **M2.5** — i nove box, per ultimo e **da solo**, perché è l'unico lotto in
   cui si può peggiorare qualcosa che funziona.

⚠️ **Perché M2.5 va per ultimo e non per primo**: riscrivere prosa buona è il
lavoro in cui è più facile perdere qualcosa senza accorgersene. Farlo quando
l'apparato è fermo permette di misurare **solo** l'effetto della prosa.

---

## 4 · Cosa questo piano NON fa

- **Non inventa la quest sostitutiva di ARC-09** (vedi D-A).
- **Non tocca il duello con Skullcrusher**: è collaudato sulla carta, e
  cambiarlo qui vorrebbe dire ricollaudarlo.
- **Non gioca il bivio**: la scelta di Thorik si fa a DEF-3 §5, al tavolo.

---

## 5 · Decisioni aperte del DM

| | Decisione | Perché serve il DM |
|---|---|---|
| ✅ | **D-A** — il risveglio Stage 1 di **Aegis Fang** si gioca **come scena** | **decisa dal DM 2026-09-19** |
| ✅ | **D-B** — Il Rituale 4 si gioca **DOPO il combattimento**, all'esito dell'incontro, e **senza ulteriori costi** | **decisa dal DM 2026-09-19** |
| ✅ | **D-C** — verificato: **non si riscrivono** | i nove erano **tre**, e i tre sono nomi noti o un nome spezzato in due parole. Il difetto stava nel metro, ed è corretto |
| ✅ | **D-D** — allineare i tre master a `state.md` (**niente −2 COS**) | **confermata dal DM 2026-09-19** → M2.0 chiuso |

---

## 6 · Il numero ADR

L'ultimo ADR è **0058**; **0059** è già prenotato dal
[PIANO-MISURA-EDITORIALE-STANDARD](PIANO-MISURA-EDITORIALE-STANDARD.md) §F2.5.
Se D-A produce una decisione strutturale, il suo numero è **0060** — da
riverificare al momento, come prescrive ADR-0009.
