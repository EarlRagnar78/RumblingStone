# ADR-0050 — Lo stato di campagna: dati validati per i fatti, markdown per la prosa

**Stato**: accettata — decisione DM del 2026-08-05, **rinumerata e attuata il 2026-09-16**

> ⚠️ **Perché il numero è cambiato, ed è la terza volta.** Questa decisione
> nacque come **ADR-0050** nella PR #99 (5 agosto 2026), rimasta bozza. Nel
> frattempo `ADR-0050` su `main` è stato preso da un'altra decisione — *moduli
> autoconclusivi e classe di artefatto* — e il numero non si riusa.
>
> È lo stesso schema già visto due volte: ex-0016 → [ADR-0039](ADR-0039-profili-regole-multisistema.md)
> ed ex-0017 → [ADR-0040](ADR-0040-separazione-prodotto-e-toolkit-estraibile.md)
> dalla #72, ed ex-0014 → [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md)
> nel lotto 4b. **Una PR lasciata aperta perde i propri numeri**, e questa è
> ormai una regolarità del repo più che un incidente.

**Data**: 2026-08-05 (corpo) · 2026-09-16 (recupero, riverifica e attuazione)
**Attuazione**: lotto **4d-1** di [`PIANO-RIPRESA-PR-ABBANDONATE`](../PIANO-RIPRESA-PR-ABBANDONATE.md) §4.8
**Decisione-fonte**: domanda DM 2026-08-05 — *«non sarebbe meglio trovare un
formato più opportuno e meno prono alle allucinazioni, JSON con manifest da
rispettare, mettendo i changelog in un altro file separato?»*
**Lotto**: G2-bis di [`PIANO-RIPRESA-PR-ABBANDONATE`](../PIANO-RIPRESA-PR-ABBANDONATE.md) §4.8

## Contesto

Il finding **C1** dell'audit 2026-08 non era un refuso: `campaign/state.md` §1
collocava i quattro PG **dopo** una battaglia mai giocata, con Hella già risorta
e Thorik che aveva già pagato il prezzo di quella resurrezione. Il lotto G1 l'ha
corretto **per convenzione** — colonne etichettate «Oggi al tavolo» / «Preparato»,
banner in testa alle sezioni.

Una convenzione, però, si può dimenticare. Era già successo: il pattern a due
tempi esisteva in §6 dal 2026-07-04, **DM-confermato**, e nessuno l'aveva esteso
a §1 per un mese. Nulla impediva che succedesse di nuovo alla prossima sessione.

Tre misure hanno inquadrato la decisione:

| Misura | Valore |
|---|---|
| `state.md` totale | 1677 righe |
| di cui §8 changelog | **1150 (68%)** |
| contenuto vivo | 527 righe — di cui **215 tabellari**, **234 prosa e banner** |

## Alternative considerate

**A. Conversione integrale a dati** (la proposta letterale: tutto in JSON con
manifest). Scartata: il 44% del contenuto vivo è prosa — il ramo di Ushgar, il
Marchio di Varis, il Debito della Radice. In JSON diventano stringhe: si perde la
leggibilità al tavolo e **non si guadagna nulla contro le allucinazioni**, perché
uno schema vincola la forma e non la verità.

**B. Solo lo split del changelog**, formato invariato. Scartata come insufficiente:
risolve il 68% del *volume* e lo 0% del problema C1.

**C. Ibrido** — dati validati per i fatti tabellari, markdown per la prosa, vista
generata. **Scelta.**

**JSON o YAML?** YAML, per tre ragioni concrete: JSON **non ammette commenti**, e
questo file è fatto di annotazioni datate («DM clarified 2026-07-03»); YAML regge
le stringhe multilinea della prosa lunga; il repo ha già cinque file dati YAML e
un `load_yaml` stdlib. Lo schema si applica identico — si valida l'oggetto dopo
il parsing, come già si fa per le mappe.

## Decisione

**I fatti di canone tabellari vivono in `campaign/state.yaml`, validato da uno
schema. La prosa resta in `campaign/state.md`, scritta a mano. Le tabelle di
`state.md` sono generate dai dati. Lo storico sta in un file a parte.**

### 1. Il vincolo che conta

Nello schema, `oggi` e `preparato` sono **chiavi**, e `oggi` è **obbligatoria**.
Per gli archi, `tempo: giocato | in_corso | preparato` è obbligatorio.

> **Un fatto senza tempo dichiarato non è esprimibile.** Non è una linea guida da
> ricordare: è un file che non passa il gate.

È la differenza fra «ci siamo dimenticati di dire che quella riga era futura» e
«quella riga non poteva esistere».

### 2. Il limite, dichiarato

Uno schema vincola la **forma**, non la **verità**. Un agente può ancora scrivere
un fatto falso in un file perfettamente valido. Ciò che questo contratto rende
impossibile è più ristretto e più utile: scriverlo **senza dire a quale tempo
appartiene**. Chi si aspetta che lo schema impedisca le allucinazioni resterà
deluso; chi si aspetta che impedisca *quella specifica classe* di errore — quella
che è già costata un mese di canone ambiguo — sarà servito.

### 3. Un master, mai due

`state.yaml` è il master dei fatti di §0, §1, §6. Le tabelle corrispondenti in
`state.md` stanno fra marcatori `<!-- gen:state:NOME -->` e sono **rigenerate**
da `scripts/render_state.py`; `--check` è un gate CI.

Questo punto non è negoziabile ed è la ragione per cui il lotto è stato eseguito
tutto insieme: creare `state.yaml` **senza** il rendering avrebbe prodotto una
seconda fonte di verità, cioè esattamente il finding **C2** appena chiuso
(`state.md` e `campaign-history.md` che si dichiaravano entrambi sorgente unica).

### 4. Cosa NON diventa dati

**Estensione del 2026-08-05 (lotto G2-ter, decisione DM)**: la migrazione è
arrivata anche a **§3** (clock dei villain), **§4** (chi sa cosa) e ai **numeri
di §2.4** (contingenti e scenari di Rethmar). Sono dati per la stessa ragione
degli altri: portano numeri e stato, e un errore lì cambia una sessione.

Restano markdown a mano, e **ci si ferma qui**: §5 (promesse e debiti), §7 (fili
narrativi ed Echo Ledger), la prosa di §2 e tutti i banner. Il criterio non è
«quanto manca da convertire» ma il rendimento: dove il contenuto è giudizio — il
dilemma di Hella sul Ghostlord — uno schema non lo migliora, lo irrigidisce. Per
un progetto editoriale con un DM solo, ogni sezione strutturata è uno schema più
un renderer più dei test da mantenere per sempre: se aggiungere una riga a §7
costasse un giro di YAML, si smetterebbe di scrivere, e il valore di questo repo
è il materiale, non l'infrastruttura.

### 4-bis. Una sola via di scrittura (G2-ter)

Il log di sessione **resta markdown** — è un documento, si legge, alimenta recap
e booklet — ma porta in testa un **front-matter** con i delta:

```
session log (markdown + front-matter dei delta)
        └─ state_apply
             ├─ clock villain → state.yaml → render_state → state.md
             ├─ March Clock    → state.md          (regione auto:)
             └─ riga storico   → state-changelog.md (regione auto:)
```

Il DM non scrive il front-matter: lo emette `session_wizard`, che quelle risposte
le raccoglieva già in forma strutturata. Il guadagno non è estetico — prima i
delta si estraevano con **regex sulla prosa**, e i clock dei villain con una
**lista di nomi cablata nel sorgente**: Ghaurush, canonizzato il 2026-08-05, non
sarebbe stato visto. Un log **senza** front-matter continua a funzionare via
regex: nessuna sessione già scritta va riscritta.

**Attuazione (2026-09-24, lotto 4e di `PIANO-RIPRESA-PR-ABBANDONATE` §4.9).**
Lo schema qui sopra è quello della #99, e D14 l'ha superato in un punto: il
March Clock non va più in una regione `auto:` di `state.md` ma nel campo
`march_clock.giorno_corrente` di `state.yaml`, come i clock. Oggi la via è:

```
session log (markdown + front-matter `delta:`, villain per png_id)
        └─ state_apply            tutto o niente, diff e conferma per voce
             ├─ March Clock, clock, stato → state.yaml → render_state → state.md
             └─ riga storico              → state-changelog.md (regione auto:)
```

Il front-matter lo scrive `session_wizard`, che risolve i nomi contro
`state.yaml` mentre il DM risponde. Il codice è `scripts/dmcore/delta_sessione.py`.
La misura che lo giustifica, presa lo stesso giorno sui tredici villain: la
regex ne vedeva **3 clock su 9** e **5 morti su 13**.

### 5. `[INFERRED]` come record

Non più una stringa da cercare col grep, ma una voce con `id`, `dove`, `domanda`,
`a_chi`, `aperto_dal`. La domanda è formulata perché il DM possa rispondere senza
rileggere i file. Questo cambia il progetto del lotto G4: l'inventario si legge
dai dati, non si estrae dal markdown.

### 6. Rapporto con ADR-0003 e ADR-0007

- **ADR-0003** («markdown master, layout generati») **non è contraddetto ma
  ristretto**: vale per i *documenti* — moduli, booklet, handout, dove il
  markdown è la sorgente e l'impaginazione l'artefatto. Per lo *stato*, che è
  una base di fatti e non un documento, la direzione si inverte: dati master,
  markdown vista. Il criterio è: **se una cosa si valida, è dato; se si legge, è
  documento.**
- **ADR-0007** (triplo vincolo sulle scritture di canone) resta pieno. Le regioni
  `gen:state:` sono generate da dati che un umano ha scritto e una PR ha
  rivisto; non sono scritture automatiche di canone.
  **Correzione (2026-08-05, stesso giorno)**: la prima stesura di questo ADR
  diceva che `state_apply.py` «non è toccato». **Era falso.** Le sue regioni
  `auto:` sono due — `march-clock` (§2.1 di `state.md`) e `changelog` (§8) — e
  spostando lo storico ho rotto la seconda: `--migrate` falliva con
  *«sezione '## 8. Changelog' non trovata»*. La CI non l'ha visto perché
  `test_state_apply.py` gira su una fixture in memoria: **nessun test toccava i
  file reali**. Corretto nello stesso lotto — la regione `changelog` ora vive in
  `campaign/state-changelog.md` e `state_apply` la segue lì, con due test nuovi
  che eseguono la migrazione **sui file veri** invece che su una fixture.
  La semantica ADR-0007 è invariata: stesse regioni, stessa conferma, stesso
  triplo vincolo — cambia solo il file che ospita lo storico.

### 7. Prodotto e partita (G2-quater)

La domanda che ha aperto il lotto: *«un DM nuovo deve poter partire pulito senza
sporcare l'originale»*. Verificando, il meccanismo **perdeva**:
`new-campaign-group.sh` azzerava solo `state.md` e `sessions/`, quindi un gruppo
nuovo ereditava `state.yaml` (643 righe), `state-changelog.md` (1165),
`campaign-history.md` (517) e i recap del gruppo precedente. Le prime due falle
le ha aperte questo stesso ADR, introducendo file di stato senza aggiornare il
reset.

**La regola, ora esplicita e testata**:

| | Cos'è | Al reset |
|---|---|---|
| **Prodotto** | archi, Bestiario, mappe, skill, `campaign-premise.md`, house rules | **resta** |
| **Partita** | `state.yaml`, `state.md`, `state-changelog.md`, `campaign-chronicle.md`, `sessions/`, `recaps/` | **si azzera da template** |

Da qui lo split di `campaign-history.md`, che mescolava i due: la **premessa**
(AP, ambientazione, grafo dei villain, riferimenti) è prodotto e resta; la
**cronaca** (party, timeline degli archi, catena dei dungeon con gli eventi di
*questi* PG) è partita e si azzera.

Il presidio non è la disciplina ma un test: `test_new_group.py` verifica che
**ogni** file di stato sia coperto dal reset e che i template non contengano
tracce del primo gruppo. La falla si riapre solo ignorando un test rosso.

**Cosa questo lotto NON decide**: se il multi-gruppo debba restare
*branch-per-gruppo* o diventare *directory-per-gruppo* (`groups/<nome>/`). La
seconda è strutturalmente migliore — `main` tornerebbe a essere solo prodotto e
`git pull` non conflitterebbe mai con la partita — ma costa rendere group-aware
~10 script, e **la scelta dipende dal PRD** (lotto G5): se il destinatario è un
solo tavolo, il branch basta; se il repo va ereditato da DM terzi, non regge.

## Conseguenze

**Positive**

- La classe di errore C1 diventa strutturalmente impossibile.
- `state.md` passa da **1677 a 546 righe**: quello che il DM apre a sessione è
  ora quasi solo ciò che gli serve.
- L'inventario `[INFERRED]` è gratuito e porta con sé le domande.
- Due gate nuovi (`validate_state`, `render_state --check`), entrambi bloccanti.

**Negative, dichiarate**

- Una dipendenza in più sul percorso critico: `pyyaml` (già usato da
  `validate_skills`, già installato in CI, con lo stesso fallback a exit 2).
- Chi modifica i fatti deve toccare `state.yaml` e rigenerare: un passaggio in
  più rispetto a editare il markdown. Il banner nelle regioni lo dice a chi ci
  finisce sopra.
- Il repo ha ora **due formati** per lo stato. Mitigazione: il confine è scritto
  qui e ripetuto in testa a `state.yaml` — si valida → dato; si legge → documento.

## Verifica

```bash
python3 scripts/validate_state.py          # schema + 5 regole di coerenza
python3 scripts/render_state.py --check     # state.md in sync con state.yaml
```


---

## Riverifica e attuazione — 2026-09-16

Recuperata da `refs/pull/99/head` e riverificata contro il codice di oggi, come
si fece per ADR-0039, ADR-0040 e ADR-0048. **La diagnosi regge**; tre cose che
diceva non sono più vere, e una promessa va ridimensionata.

| Cosa diceva il 5 agosto | Oggi |
|---|---|
| `state.md` 1.677 righe, §8 il 68% | **1.625 righe**, §8 il **72%** (1.178) |
| 215 righe tabellari | **183** |
| il changelog esce in `state-changelog.md` | ⬜ **non ancora**: è il lotto **4d-2** |
| `state.yaml` recuperabile dal ramo | 🔴 **no** — vedi sotto |

🔴 **I dati non si sono potuti portare, e questo è il fatto centrale.** Il ramo
della #99 è **384 commit indietro**. Confrontando la parte viva dei due
`state.md`: **229 righe** che il ramo ha e `main` no, **103** che `main` ha e il
ramo no. Il canone del 2026-09-11 e 09-12 — D3, D4, D11, D13, i Tre Doni, la
Collana, i due tempi di 4c — nel ramo **non esiste**. Portare il suo
`state.yaml` avrebbe annullato cinque settimane di canone in silenzio.

Si è recuperata la **macchina** (`render_state.py`, `validate_state.py`, lo
schema, i test) e si sono **estratti i valori da `state.md` di oggi**, con la
byte-identità come rete.

⚠️ **Anche la macchina è stata riscritta, e per la stessa ragione.** Il
generatore del ramo emetteva una forma di tabella **diversa** — colonna `Tempo`
in §3 e §4, intestazioni italiane in §1 e §6 — perché era del 10 agosto, mentre
il lotto 4c ha ridisegnato quelle sezioni il 12 settembre. Adottarla avrebbe
riportato indietro la *presentazione* del canone come portare i dati ne avrebbe
riportato indietro i *fatti*. Le otto tabelle sono ora **specifiche dichiarate**
(`TABELLE` in `render_state.py`), copiate alla lettera dal file vero, e un test
le confronta con `state.md`.

### 🔴 La promessa che va ridimensionata

Questa decisione diceva: *«`oggi` e `tempo` obbligatori → un fatto senza tempo
dichiarato non è esprimibile»*. Misurando si è scoperto che **il canone non lo
dichiara ovunque**:

| Dove | Come il tempo è dichiarato |
|---|---|
| §0 archi | ✅ per riga, colonna `Fase` |
| §1 party · §6 artefatti | ✅ come **due colonne** (`oggi` / `preparato`) |
| §3 villain · §4 conoscenze · §2.4 Rethmar | ❌ **non dichiarato** — 58 righe |

Il generatore del ramo risolveva aggiungendo una colonna; qui quella colonna
non c'è più. Assegnare un tempo riga per riga sarebbe **dedurlo**, cioè
inventare canone dentro un lotto di infrastruttura — l'esatto contrario di ciò
che questa decisione esiste per impedire.

**Quindi il campo è opzionale in quelle quattro sezioni, e la regola R7 di
`validate_state.py` le CONTA a ogni esecuzione**: oggi **58**. Un numero che si
vede non cresce in silenzio, e il giorno in cui il DM dichiara quei tempi scende
da sé. È la forma di [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md):
contare ciò che non è dichiarato vale più che indovinarlo.

### Cosa resta fuori, dichiarato

| | Cosa | Dove va |
|---|---|---|
| ⬜ | lo split di §8 in `state-changelog.md` e la via di scrittura | lotto **4d-2** |
| ⬜ | `confine` e `inferred` come dati (27 marcatori, dentro la prosa di §5 e §7) | opzionali nello schema, col motivo scritto |
| 🔵 | i 58 tempi non dichiarati | **decisione del DM** |
| 🔵 | «🔫 armato» (maschile) e «✖ annullata» (femminile) convivono negli echi | una parola, **al DM** |
| ⬜ | §5 promesse e §7 fili narrativi | restano **prosa**, ed è una scelta: sono le sezioni che il DM riscrive di più a mano |
