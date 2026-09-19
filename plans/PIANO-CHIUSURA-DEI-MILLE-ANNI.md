# PIANO — La chiusura dei mille anni: cosa il viaggio deve consegnare davvero

> **Cos'è**: portare `ARC07-DEF-4` a consegnare ciò che il **canone dice che il
> viaggio consegna**, e non solo il duello. La riscrittura del 2026-09-18 ha
> sistemato il mestiere; questo piano chiude i **buchi di canone** che il
> mestiere non poteva vedere.
>
> **Stato**: 🔵 pianificato (2026-09-19) · **Decisore**: DM
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

## 1 · I quattro buchi, misurati

### 🔴 G1 — Il Rituale 4 non ha un nome nel posto dove si gioca

Il viaggio **è** il Rituale Legacy 4. La matrice artefatti lo registra come
*Siege of the Eternal Forge*, con esito *«buff forza/coraggio 1/settimana;
Mantle of Stone and Spirit; il Rubino si consuma nel ritorno al 1372 (D16)»* e
stato ⬜ **da giocare**. Nel master quel nome non compare, e nemmeno il
passaggio in cui la Corona **cambia grado**.

**Conseguenza al tavolo**: il DM gioca il duello, torna, e `state.md` gli
chiede di segnare un avanzamento d'artefatto che nel modulo non è mai successo.

### 🔴 G2 — La Senzienza, e il colpo che rimbalza su Aegis Fang

È il buco più grosso, e attraversa tre archi. `PROPOSTA-DONI-RESURREZIONE-HELLA`
§III lo dice per esteso:

> se Thorik dona il **+2 di deflessione** al rito di DEF-3, **la Corona non
> parlerà mai**. Torna dal viaggio con il Rubino e la Corona +3, ma **senza la
> Senzienza**. E il colpo rimbalza: `state.md` dice che il risveglio pieno di
> **Aegis Fang** richiede *«Assedio della Forgia + Corona Senziente»* — una
> delle due condizioni **non si verificherà più**, e ne serve una nuova.

**Quindi**: una scelta fatta in **DEF-3 §5** determina se un potere di **DEF-4**
esiste, e se una quest di **ARC-09** diventa necessaria. Oggi DEF-4 non lo sa,
e `ARC07-CONSEGUENZE-ECHI.md` va verificato.

⚠️ **Questo non lo decido io.** Inventare la quest sostitutiva di ARC-09 è
canone nuovo: è la decisione **D-A** in §5.

### 🟡 G3 — La cucitura del ritorno

Il Rubino *«si consuma nel ritorno al 1372»*, raccordo **D16**. DEF-4 lo cita 5
volte, DEF-5 due. La cucitura probabilmente regge, ma **non è stata verificata
riga per riga** — e le due volte che ho dato per buona una cucitura in questa
campagna, non lo era.

### 🟡 G4 — Il mestiere: quello che la riscrittura di ieri ha lasciato

| | DEF-4 oggi |
|---|---:|
| box read-aloud etichettati | 14 |
| **oltre le 12 righe** | **0** 🟢 |
| con parentesi | 2 🟡 |
| **con più di un nome proprio** | **9** 🔴 |
| box che presuppongono un'azione del giocatore (norma *Dungeon*) | 2 su 41 🟢 |

Nove box su quattordici restano il difetto che la riscrittura di ieri **ha
dichiarato e non ha chiuso**. Va detto che è il più costoso da correggere:
richiede riscrivere prosa buona, non aggiungere apparato.

---

## 2 · Assunzioni dichiarate

1. **Il canone vince sul modulo.** Dove `state.md` e il master divergono, si
   allinea il master — mai il contrario senza decisione del DM (regola 8).
2. **G2 non si chiude scrivendo la quest ARC-09.** Si chiude **scrivendo il
   bivio** dentro DEF-4, con entrambi i rami, e lasciando la quest a una
   decisione. Un piano che inventa canone per chiudere un buco di canone ne
   crea due.
3. **La riscrittura di ieri non si tocca.** I congegni introdotti (regia di
   round, quarta colonna, `[HDYWTDT]`) restano; questo piano **aggiunge**.
4. **Il duello con Skullcrusher è collaudato sulla carta e non al tavolo.**
   Niente qui lo cambia.

---

## FASE 1 — Audit / accertamento

| | Lotto | Cosa produce | Come si verifica |
|---|---|---|---|
| ✅ | **M1.1** Copertura del canone dei −1.000 | la tabella di §0 | fatta: 3 parole su 6 a zero |
| ✅ | **M1.2** Stato del mestiere di DEF-4 | la tabella di G4 | fatta |
| ⬜ | **M1.3** Il ramo Senzienza, tracciato su tre archi | dove la scelta si fa (DEF-3 §5), dove si paga (DEF-4), dove rimbalza (ARC-09 + Aegis Fang) | ogni passaggio o esiste in un file o è un buco elencato |
| ⬜ | **M1.4** La cucitura D16 riga per riga | DEF-4 §9 ↔ DEF-5 §apertura: chi consuma il Rubino, dove atterrano, in che giorno | 🔴 nessuna contraddizione, o la si scrive |
| ⬜ | **M1.5** `ARC07-CONSEGUENZE-ECHI.md` conosce il bivio? | sì/no, misurato | grep + lettura |

## FASE 2 — Sviluppo

L'ordine è quello di esecuzione, ed è scelto perché **ogni lotto rende più
facile il successivo**.

| | Lotto | Cosa fa | Perché qui |
|---|---|---|---|
| ⬜ | **M2.1** §4-quater «Il Rituale della Forgia Eterna» | la scena in cui il Rubino entra nella Corona **durante o dopo il duello**, col nome canonico, e la Corona passa a **+3** | è il buco G1, ed è il pezzo che tutti gli altri presuppongono |
| ⬜ | **M2.2** Il bivio della Senzienza | dentro M2.1: **due rami scritti**, «Thorik ha donato» e «Thorik non ha donato», con cosa cambia **al tavolo** in entrambi | senza, M2.1 vale per metà dei tavoli |
| ⬜ | **M2.3** La riga di rimbalzo su Aegis Fang | nel ramo «ha donato»: la condizione di risveglio si rompe, **e il modulo lo dice al DM** invece di lasciarglielo scoprire in ARC-09 | è un avviso, non una quest: costa tre righe |
| ⬜ | **M2.4** Cucitura D16 | correggere ciò che M1.4 trova | dopo M2.1, perché il Rituale cambia cosa arriva a DEF-5 |
| ⬜ | **M2.5** I nove box | riscrivere i box con più di un nome proprio, **uno alla volta, tenendo il migliore** | ultimo: è l'unico lotto che tocca prosa già buona, e va fatto quando il resto è fermo |
| ⬜ | **M2.6** Echo Ledger | le conseguenze nuove in `state.md` §7.E e in `ARC07-CONSEGUENZE-ECHI.md` | la regola: un'eco che non è nel registro non riemerge |

## FASE 3 — Validazione

| | Criterio | Come si prova |
|---|---|---|
| ⬜ | **V1** Le tre parole del canone hanno un riscontro | `Rituale 4`, `Corona +3`, `Senzienza` compaiono dove si gioca, non solo in `state.md` |
| ⬜ | **V2** Entrambi i rami sono giocabili | un DM che legge solo DEF-4 sa cosa fare **sia** se Thorik ha donato **sia** se no |
| ⬜ | **V3** Nessuna regressione di mestiere | `misura_craft --densita`: nessun congegno di DEF-4 scende |
| ⬜ | **V4** I box migliorano davvero | `--box`: **da 9 a ≤4** con più di un nome proprio, e **0 oltre le 12 righe** |
| ⬜ | **V5** Il canone non si contraddice | `validate_modules` verde · rilettura di `campaign-coherence.md` |
| ⬜ | **V6** Il cancello morde | iniettare una contraddizione col canone → deve emergere in V5 |

---

## 3 · L'ordine che propongo, e perché

1. **M1.3 + M1.4 + M1.5** — un solo giro di lettura, mezz'ora. Senza sapere
   dove il ramo Senzienza tocca terra, M2.2 si scrive al buio.
2. **M2.1 → M2.2 → M2.3** — un commit solo: sono la stessa scena.
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
| 🔵 | **D-A** — Aegis Fang: se la Corona non parlerà mai, la condizione di risveglio si sostituisce con cosa? | è canone nuovo su un artefatto di un PG |
| 🔵 | **D-B** — Il Rituale 4 si gioca **durante** il duello (sotto pressione) o **dopo** (come rito)? | cambia il tono della scena finale dell'arco |
| 🔵 | **D-C** — I nove box: si riscrivono, o il difetto si accetta e si registra? | costa prosa buona, ed è una scelta di gusto |

---

## 6 · Il numero ADR

L'ultimo ADR è **0058**; **0059** è già prenotato dal
[PIANO-MISURA-EDITORIALE-STANDARD](PIANO-MISURA-EDITORIALE-STANDARD.md) §F2.5.
Se D-A produce una decisione strutturale, il suo numero è **0060** — da
riverificare al momento, come prescrive ADR-0009.
