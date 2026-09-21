# 🥇 Le regole d'oro — quando scattano, cosa producono, chi le verifica

> **Cos'è**: le sei regole d'oro come **dato**, ordinate per il momento in cui
> scattano invece che per la data in cui sono state aggiunte, con il comando
> che le esegue e il cancello che le verifica.
>
> **Gate**: `python3 scripts/validate_skills.py` —
> [ADR-0061](../plans/adr/ADR-0061-le-regole-d-oro-sono-un-dato-ordinato-per-momento.md)
>
> La **narrazione** — perché ogni regola esiste, quale fallimento l'ha
> generata, cosa costa saltarla — resta in [`AGENTS.md`](../AGENTS.md). Qui c'è
> la struttura, e solo quella.

---

## ⚠️ Il difetto che ha generato questo file, misurato

Il 2026-09-20 il DM: *«le Golden rule si sovrappongono o entrano in conflitto?
Quale è il miglior modo per organizzarle?»*. Misurato su `AGENTS.md` prima di
rispondere:

| Difetto | La misura |
|---|---|
| **Le sei regole hanno tre forme diverse** | G1-G3 sono voci di un elenco numerato (righe 109-115); G4-G6 sono un titolo `####` più un blockquote (128-211). **Nessun pattern le estrae tutte e sei** |
| **Il numero «4» significa tre cose** | `AGENTS.md` contiene **tre** elenchi che partono da `1.` (righe 109, 301, 363) e la locuzione *«regola 8»* compare due volte riferita al **terzo**. Un agente che legge *«la regola 4»* non sa quale |
| **L'ordine dei numeri non è l'ordine di esecuzione** | G5 decide **quali** skill caricare, G1 dice di leggerne i `references/`. G1 non è eseguibile prima di G5, ma viene prima nel numero |
| **Nessun cancello le guardava** | ed è la condizione esatta di [ADR-0056](../plans/adr/ADR-0056-una-norma-senza-misura-non-esiste.md), applicata alle regole che quella ADR ha generato |

🔎 **La cura è quella che ha funzionato per le skill** ([ADR-0058](../plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md)):
una gerarchia che esisteva sparsa nella prosa diventa una tabella con un gate.
Qui l'asse non è lo strato, è il **momento del ciclo**.

---

## 1 · Le sei regole, ordinate per momento

<!-- regole-doro: tabella -->

| id | Momento | Quando scatta | Cosa produce | Comando | Chi lo verifica |
|---|---|---|---|---|---|
| **G5** | 🟦 PRIMA | sto per aprire qualunque skill | l'elenco delle skill dovute, per strati | [`skills/ORCHESTRAZIONE.md`](ORCHESTRAZIONE.md) | `scripts/validate_skills.py` |
| **G6** | 🟦 PRIMA | sto per **modificare** un file | i quattro passi in sola lettura sui bersagli | `python3 scripts/fase1.py <bersagli>` | `scripts/fase1.py` (`--check` esce 1 su un archivio) |
| **G1** | 🟦 PRIMA | ho scelto le skill e sto per scrivere | i `references/` letti per intero, non elencati | — *(lettura: nessun comando)* | `scripts/validate_norme_editoriali.py` (che le norme esistano e siano registrate) |
| **G2** | 🟨 DURANTE | sto per **affermare** qualcosa sullo stato del repo | il numero, accanto all'affermazione | `python3 scripts/misura_craft.py [--box\|--copertura\|--spotlight]` | `scripts/misura_craft.py` |
| **G4** | 🟥 DOPO | sto per **consegnare** prosa di gioco | le sette domande della self-check, eseguite | `python3 scripts/misura_craft.py --box` *(domande 1, 2, 7)* | `scripts/misura_craft.py` |
| **G3** | 🟥 DOPO | ho introdotto una **norma** nuova | la riga nel registro, con chi la misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](REGISTRO-NORME-EDITORIALI.md) | `scripts/validate_norme_editoriali.py` |

⚠️ **I numeri restano quelli storici**, perché sono citati in ADR, piani e
messaggi di commit già scritti. Cambia la **lettera**: `G` li separa una volta
per tutte dalle altre due liste numerate di `AGENTS.md` — la *Rules
Adjudication Policy* (1-11, quella di *«regola 8: la coerenza batte lo stile»*)
e *«Quando un agente risponde»* (1-5).

---

## 2 · Dove stanno le misure, e in che stato sono

G2, G4 e G6 dicono tutte e tre «misura». La domanda del DM — *«il file con le
misure dovrebbe essere `PIANO-MISURA-EDITORIALE-STANDARD`, giusto?»* — ha una
risposta a tre voci, e confonderle è il modo in cui un meccanismo smette di
essere deterministico:

| Cosa | Dove | Stato oggi |
|---|---|---|
| **Quali norme esistono, e chi le guarda** | [`REGISTRO-NORME-EDITORIALI.md`](REGISTRO-NORME-EDITORIALI.md) | 🟢 **in vigore** — 44 norme, gate bloccante |
| **Come si misura una cosa** | gli script: `misura_craft.py` (23 congegni), `validate_prosa.py`, `validate_booklets.py`, `validate_modules.py` | 🟢 **in vigore** |
| **Quanto vale un difetto, e qual è la soglia** | [`PIANO-MISURA-EDITORIALE-STANDARD`](../plans/PIANO-MISURA-EDITORIALE-STANDARD.md) — MQM adattato, severità 1 / 5 / **25**, soglie tarate sul repo, κ ≥ 0,6 | 🔵 **pianificato, 0%** — `scripts/punteggio_mqm.py` e `specifiche-qualita.yaml` **non esistono** |

> **Quindi la risposta onesta è: sì e non ancora.** `PIANO-MISURA-EDITORIALE-STANDARD`
> è il posto giusto per il **punteggio**, e il giorno in cui la sua FASE 2 è
> chiusa diventa il terzo pilastro del meccanismo. Oggi nominarlo come *la*
> fonte delle misure indicherebbe un'intenzione, e un meccanismo deterministico
> che punta a un file non scritto è peggio di uno che dichiara il buco.

🔎 **Per questo `fase1.py` lo stampa con il suo stato**, invece di nominarlo e
basta: l'agente vede in output che il punteggio pesato non c'è ancora, e non lo
cita come se ci fosse.

---

## 3 · Sovrapposizioni e conflitti, con il vincitore dichiarato

<!-- regole-doro: conflitti -->

| # | Fra | Verdetto | Perché |
|---|---|---|---|
| **R1** | **G5 vs G1** | **G5 prima** | non si leggono i `references/` di una skill che non si è deciso di caricare. È l'unica **precedenza obbligata** del gruppo, e l'ordine dei numeri la nasconde |
| **R2** | **G6 vs G2** | **complementari, trigger diversi** | G2 scatta su un'**affermazione**, G6 su una **modifica**. Stesso strumento (`misura_craft`), due momenti. Non si fondono: si può affermare senza modificare, e capita spesso |
| **R3** | **G4 domanda 7 vs G2** | **stessa misura, due usi** | «un box è cresciuto oltre il tetto?» si risponde con `--box`, che è lo strumento di G2. G4 la **esegue**, G2 la **impone**: chi consegna senza misurare viola entrambe |
| **R4** | **G3 vs G6 passo 1** | **due direzioni dello stesso oggetto** | G3 **scrive** nel registro, G6 lo **legge**. Senza G3 il registro invecchia; senza G6 nessuno lo apre. Nessun conflitto |
| **R5** | **G1 vs G5** *(tensione, non conflitto)* | **vince G5** | G1 dice *«leggi tutti i `references/` che la riga della tabella ti assegna»*, e la tabella per compito può assegnare una skill che l'algoritmo a strati non aprirebbe. ⚠️ Quando le due divergono, **decide l'algoritmo**: caricare per sicurezza è il danno che [ADR-0058](../plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md) descrive |

🔎 **Conflitti veri: uno (R5), e adesso ha un vincitore.** Gli altri quattro
sono **sovrapposizioni utili** — due regole che guardano lo stesso oggetto da
momenti diversi. Eliminarle accorcerebbe l'elenco e toglierebbe presidio: il
difetto del 2026-09-18 (`read-aloud-adulti.md` inapplicato per tre settimane) è
passato **sia** da G1 non eseguita **sia** da G2 non eseguita, e una sola delle
due non l'avrebbe fermato.

⛔ **Cosa NON si fonde, e perché.** La tentazione naturale è fondere G2 dentro
G6 («misurare è il passo 4 della FASE 1»). Sarebbe l'errore misurato sulle
skill: una regola che copre due momenti diventa vaga, e si smette di applicarla
a quello meno evidente. G2 si applica anche quando **non** si tocca un file, ed
è il caso in cui è stata violata di più.

---

## 4 · Il ciclo, in una riga

```
🟦 PRIMA    G5 quali skill  →  G6 FASE 1 sui bersagli  →  G1 leggi i references
🟨 DURANTE  G2 misura prima di affermare                (vale anche senza modifiche)
🟥 DOPO     G4 self-check   →  G3 registra la norma nuova
```

⚠️ **Il ciclo non è una formalità di apertura.** G6 scatta a **ogni**
modifica, non una volta per sessione: un secondo lotto su bersagli nuovi è una
FASE 1 nuova.
