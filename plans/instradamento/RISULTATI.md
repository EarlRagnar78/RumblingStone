# Instradamento delle skill: le frasi vere del DM, misurate

L8 di [`PIANO-AGENT-SKILLS-ESTERNE`](../PIANO-AGENT-SKILLS-ESTERNE.md), 2026-10-01.
Lo strumento è `scripts/instradamento_skill.py`; i casi sono in `casi.json`.

## Il metodo

Trenta frasi del DM, copiate da `plans/`, `skills/` e `AGENTS.md` dove sono
citate fra «». Per ognuna l'insieme delle skill **obbligatorie** secondo
ORCHESTRAZIONE §4: L0 se tocca il canone, una L1, le L2 che si applicano. Le
L3, L4 e LR non contano, perché non sono obbligatorie. Gli insiemi li ha
scritti l'agente e vanno confermati (D10).

Una skill obbligatoria è **raggiunta** se almeno un trigger fra virgolette
della sua descrizione compare nella frase (intero, o per una parola sola al
plurale o al femminile italiano). Le frasi sono divise a metà: con le
«taratura» si sono scelti i trigger nuovi, le «verifica» non sono state
guardate.

## I conti

| | prima | dopo |
|---|---:|---:|
| omissioni, taratura | 19 su 23 | 5 su 23 |
| omissioni, **verifica** | 19 su 23 | **8 su 23** |
| skill obbligatorie raggiunte senza essere attese | 2 | 7 |
| conflitti fra le due L1 | 0 | 0 |

«Prima» e «dopo» usano lo stesso matcher. Le prime misure, con un matcher che
non staccava le elisioni né riconosceva i plurali, davano 42 su 46: due
difetti dello strumento, corretti prima di toccare le descrizioni.

## Cosa dicono

**Le descrizioni erano scritte per un altro lettore.** I trigger di
`campaign` erano cinque, tutti inglesi tranne il nome del repo; quelli di
`module-standard` erano parole del gergo del repo («master definitivo»,
«consolidamento»), non del DM («modulo», «avventura», «stanze»). Il DM scrive
in italiano e nomina i PG: «Trigger on PC names» c'era, ma senza i nomi.

**Il guadagno regge sulle frasi non usate:** in verifica le omissioni scendono
da 19 a 8. Sulle frasi di taratura scendono di più (a 5), ed è la differenza
che ci si aspetta da una taratura.

**Il prezzo sono le skill in più**, da 2 a 7: «arco» e «PNG» fanno scattare
`campaign` anche su frasi generiche, «prosa» fa scattare `narrative-style` su
una frase che parla della prosa degli archi come di un posto dove cercare. Una
skill obbligatoria in più costa contesto, una in meno costa il difetto
silenzioso di ORCHESTRAZIONE §4; il cricchetto conta solo le seconde.

**Un instradamento sbagliato tolto prima che succedesse.** `narrative-style`
aveva il trigger «documento», che voleva dire il documento *in gioco* (ADR,
Eco). Una frase come «deep audit del documento» l'avrebbe fatta scattare,
cioè la L1 sbagliata. Ora è «documento in gioco».

## Cosa resta

Le otto omissioni in verifica sono frasi che non nominano niente del lessico
della skill: «se le carte si danno prima, i PG sanno tutto» è narrativa e
canone senza una parola chiave. Per quelle un controllo lessicale non basta,
e il tetto non va spinto a zero aggiungendo trigger su misura delle frasi:
sarebbe imparare la prova a memoria.

## D10 · il campione verificato e confrontato (2026-10-01, sera)

Il DM ha chiesto di non confermare gli insiemi a mano, ma di verificarli con
dei test e di confrontarli con quello che fa la comunità.

### Cosa hanno trovato i test sul campione

- **Una frase non era del DM.** «scorrendo il master, so cosa succede
  stasera?» l'avevo scritta io nel piano, dopo le parole «il DM a freddo:», e
  la regex di raccolta l'aveva presa per una citazione. Tolta. Ora un test
  controlla che ogni frase sia letterale nella sua fonte e che, poco prima, ci
  sia il DM e non «il DM a freddo».
- **Una frase era composta da due citazioni.** Ridotta alla prima.
- **Le fonti** erano scritte a memoria («plans/»): ora ognuna è il file esatto.
- **I nomi propri**: ogni frase che nomina uno dei 322 nomi della campagna
  (`misura_craft._registro_dei_nomi`, lo stesso di `fase1.py`) ha `campaign`
  fra le attese. Il test passa senza correzioni.

### Il confronto

Tre riferimenti, letti per intero:
[agentskills.io, «Optimizing skill descriptions»](https://agentskills.io/skill-creation/optimizing-descriptions),
la skill `skill-creator` di Anthropic (Apache 2.0: `run_eval.py`,
`run_loop.py`, `improve_description.py`) e `evals/tools/run_trigger_evals.py`
di awesome-llm-apps (Apache 2.0, ADR-0076), che a sua volta riprende il modello
a livelli di addyosmani/agent-skills. Nessun codice copiato: si adottano le
idee.

| Pratica | agentskills.io | skill-creator | run_trigger_evals | qui, prima | qui, ora |
|---|---|---|---|---|---|
| casi negativi vicini («near-miss») | sì, 8-10 su 20 | sì | sì, con margine 1,15 | no | **10 quasi-casi** e il campo «escluse» |
| due metà, una sola per tarare | 60/40 | holdout stratificato | no | 50/50 | 50/50, ognuna con casi e quasi-casi (test) |
| più corse, tasso di attivazione | 3, soglia 0,5 | in parallelo | no | no | **3 agenti, maggioranza** (`--comportamentale`) |
| controllo lessicale in CI | no | no | sì | sì | sì, con le escluse e un secondo tetto |
| collisioni fra descrizioni | no | no | oltre il 50% del vocabolario | no | **sì**: nessuna; la più vicina `forgotten-realms-lore` ↔ `campaign` al 32% |
| la skill giusta per prima | — | — | sì | — | **non adottato**: qui una frase vuole un *insieme*, le righe si sommano |
| riscrittura automatica della descrizione | — | sì, con un LLM | — | — | **non adottato**: chiede `claude -p` in CI e una chiave; la riscrittura resta a mano |

### La prova comportamentale

Tre agenti nuovi ricevono solo nome e descrizione delle diciotto skill, come
all'avvio di una sessione, e le 39 frasi senza etichette. Una skill è
«caricata» se la sceglie la maggioranza.

| | lessicale | agenti, prima | agenti, dopo il confine |
|---|---:|---:|---:|
| obbligatorie caricate | 32 su 47 | 40 su 47 | 40 su 47 |
| escluse caricate | 1 | 1 | **0** |

«Prima» sono le corse in `comportamentale/`, «dopo» quelle in
`comportamentale-v2/`. Fra le due è cambiata una frase della descrizione di
`narrative-style` («Non per gli script che controllano la prosa»), scelta su un
fallimento della metà di taratura, come chiede agentskills.io: non si
aggiungono parole delle frasi sbagliate, si dice cosa la skill non fa. Con tre
corse la differenza su una sola frase è debole.

⚠️ **Due etichette sono state corrette guardando le corse**, e quindi il «41»
che si leggerebbe con le etichette nuove sulle corse vecchie non è
indipendente: la frase su Umberto Eco vuole anche `indagine` (AGENTS.md regola
11), e la domanda sui passi per il PDF non chiede di scrivere niente. Le altre
sei differenze fra agenti ed etichette restano aperte, nel campo dei casi:

| # | Frase | Agenti | Etichetta |
|---|---|---|---|
| 1 | il PDF della parte DM | `editoria` | `campaign` (nomina la Forgia) |
| 6 | i misteri della mini campagna | `indagine` sola | anche `narrative-style`, che resta il fondo (C3) |
| 12 | le statistiche di D5 | consultazione SRD e PF1e | anche `campaign` |
| 17 | stanze e PNG inventati al tavolo | `module-standard`, `narrative-style` | anche `campaign` |
| 18 | eventi e osterie del Drappo | `campaign` (due su tre) | il Drappo **non** è la campagna |
| 22 | il gruppo d'incontro contro incantatori | `automation`, SRD | `module-standard` |

La #18 è la più istruttiva: la descrizione di `campaign` non dice che il Drappo
ne è fuori, e gli agenti ci cascano. È nella metà di verifica: non l'ho usata
per tarare.

## D11 · il confine sul Drappo, e cinque frasi nuove (2026-10-01, notte)

Il DM ha approvato D11. Due cose fatte insieme:

- **Cinque frasi nuove** del DM, prese dai suoi messaggi di oggi e mai usate
  per tarare (`frasi-del-dm-2026-10-01.md`, `"insieme": "verifica-2"`).
- **Il confine** nella descrizione di `campaign`: «Not for the standalone
  Drappo di Tarsilia, which is outside this campaign».

Tre agenti nuovi, sulle 44 frasi (`comportamentale-v3/`):

| | v2 | v3 |
|---|---:|---:|
| obbligatorie caricate | 40 su 47 | 45 su 50 |
| escluse caricate | 0 | 0 |
| frasi nuove (verifica-2): obbligatorie caricate | — | 3 su 3 |

**Il confine non ha avuto effetto**, e la ragione è nella frase: «ci sono
eventi per i personaggi? come entrano nelle contrade? ci sono osterie e
botteghe?…» non nomina il Drappo. Il contesto era nella conversazione con il
DM, non nella frase, e nessuna descrizione lo può indovinare: tre agenti su tre
caricano `campaign`. Era l'etichetta a chiedere troppo, non la descrizione a
dire troppo poco; agentskills.io lo prevede («the issue may be with the
queries … poorly labeled»). La frase resta nel campione con `campaign` tolta
dalle escluse e la correzione scritta nel caso. Il confine resta nella
descrizione: è vero, e servirà a una frase che il Drappo lo nomina.
