# Ricerca: una marcatura sola per le parti inferite, e se le guardie servono

**Data**: 2026-11-07 · **Richiesta del DM** (Jfs): marcare le parti INFERRED in
modo che il DM decida cosa diventa canone; per regole, skill e agent vale la
regola più stringente; evitare duplicazioni; misurare se le guardie servono
davvero; cercare in rete le tecniche migliori di scrittura di skill vincolate e
di guardrail contro le allucinazioni, e vedere dove si applicano nel repo.

**Fonti**: Firecrawl (ricerca web e articoli), storia git del repo. Decisione
in [ADR-0109](adr/ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md),
grammatica in [GUIDA-MARCATURE](../docs/reference/GUIDA-MARCATURE.md).

## In breve

- **Le guardie servono.** Sulla storia del repo, 171 righe sono passate da
  INFERRED a CANONE: il DM ne ha confermate 141 (82%) e cambiate 30 (18%), 16
  con un numero diverso (la piana di Hammerfist da 870 a 520 m sul mare).
- **Il difetto è la forma**: 4 modi di scrivere INFERRED, 5 di scrivere
  canone, la regola in 6 posti, l'86% delle marche (761 su 883) senza domanda.
- **La rete** conferma la strada del repo e aggiunge due correzioni: una parola
  per concetto, e nessun grado di fiducia dichiarato dall'AI.
- **Cosa non è misurato**: le invenzioni non marcate. Le misura la prova A/B
  (§7).

## 1. Cosa c'è oggi nel repo

| Cosa | Dove | Quante (tutto il repo, storia compresa) |
|---|---|---|
| `[INFERRED]` nudo | ovunque | 536 |
| `[INFERRED — needs DM confirmation]` | AGENTS.md §5, skill | 225 |
| `[INFERRED — <nota>]`, `[INFERRED: …]`, `[INFERRED da D46]` | moduli, piani | ~120 |
| `[CANONE — DM <data>, <codice>]` | moduli, Bestiario, piani | 1.356 |
| `[CANONE GIOCATO <data>]`, `[CANONE <data>]`, `[CANONE]` | moduli | ~25 |
| `[ACCEPTED — DM-canon]` | intestazione schede ADR-0091 | modello |
| «(decisione DM …)», «(CANONE DM …)» | prosa vecchia | ADR-0069 le cita |
| `[GENERATO]` | numeri calcolati da script | 143 |
| `[Private source — …]`, `⚠ **Non SRD**` | fonti fuori SRD | ~220 |
| `<!-- storico -->` | storia delle scelte, tolta in stampa (ADR-0069) | 229 blocchi |

**Gli strumenti che già esistono:**
- `inventory_inferred.py --check`: conta gli aperti e fallisce se salgono. In CI è **non bloccante** (canale testing, `continue-on-error`).
- `misura_standard_tavolo`: impedisce che una nota di lavoro («[INFERRED…]», «da verificare») arrivi nel PDF del tavolo. È un cancello vero.
- `decisioni_dm.py`: raccoglie le decisioni aperte dalle tabelle `<!-- decisioni-dm -->` dei piani.
- `togli_storico`: toglie la storia dalla stampa.
- ADR-0103: le regole si riscontrano sull'SRD in cache. ADR-0108: i cancelli deterministici stanno in ogni skill.

**Dove la regola è scritta:** AGENTS.md §5 («Non inventare mai… Marca `[INFERRED — needs DM confirmation]`»), `npc-villain-boosting`, `pathfinder-1e-srd`, `rumblingstone-module-standard` (due volte), `rumblingstone-playtest`, ADR-0091. Sei testi, sei formulazioni. Le altre ~15 skill non la ripetono e non la richiamano.

## 2. La misura: le guardie servono davvero?

**Metodo.** Script su `git log -p` di tutti i `.md`: per ogni riga tolta con `[INFERRED…]` cerco la riga aggiunta più simile nello stesso punto, tolgo le marche e confronto il testo e i numeri. Righe uguali ripetute nei volumi contate una volta sola.

| Esito | Righe uniche | Quota |
|---|---|---|
| INFERRED → CANONE, testo identico | 141 | 82% |
| INFERRED → CANONE, testo cambiato | 30 | 18% |
| … di cui con un numero cambiato | 16 | 9% |
| INFERRED tolto senza marca nella riga | 61 | — |
| Riga riscritta o spostata (non confrontabile) | 98 | — |

**Cosa vuol dire.**
- Una ipotesi su cinque non sopravvive alla lettura del DM. È un filtro che lavora, non una formalità.
- Le 61 «tolte senza marca» le ho controllate a campione (10 su 61): sono tutte nei volumi di stampa `.hb.md`, dove la marca si toglie apposta, o in commit «scelte del DM» con il file DECISIONI accanto. La decisione è tracciata, ma **fuori dalla riga**: chi legge il modulo non sa che quel numero l'ha scelto il DM. Questo è il punto da correggere.
- L'86% dei marcatori (761 su 883) non porta la domanda. Per decidere, il DM o l'agente deve ricostruire il dubbio da capo. Le card di P16 lo hanno fatto a mano, riga per riga.

**Cosa non dice.** Non misura le invenzioni senza marca, e non misura se un agente con lo standard nuovo sbaglia meno. Per questo serve la prova della scheda 7.

## 3. Cosa dice la ricerca in rete

| Fonte | Cosa dice | Nel repo | Cosa cambierebbe |
|---|---|---|---|
| Anthropic, *Reduce hallucinations* (platform.claude.com) | Dare il permesso di dire «non so»; citare la fonte parola per parola; dopo la stesura, ricontrollare ogni affermazione e **togliere e marcare** quella senza fonte | Il permesso c'è (INFERRED). La verifica dopo la stesura no: oggi si marca mentre si scrive, non si ricontrolla | Un passo fisso «rileggi ogni numero: fonte o marca» alla fine di ogni skill che scrive contenuto |
| Anthropic, *Skill authoring best practices* | Una sola parola per ogni concetto in tutta la skill; vincoli stretti dove il compito è fragile; checklist con verifica che rimanda indietro; prove prima di scrivere la skill | Parole diverse per lo stesso concetto (ACCEPTED/CANONE/decisione DM); checklist presenti in alcune skill | Una grammatica sola, scritta in un posto, richiamata dalle skill |
| *Authoring Agent Skills: a software-engineering approach* (UCL, arXiv 2607.25032) | Quello che deve succedere **ogni volta** va in un hook o in un controllo, non in prosa | ADR-0108 va già in questa direzione | Le regole di marcatura diventano controlli in CI, la prosa della skill rimanda a loro |
| W3C PROV-O | La provenienza di un dato si descrive con tre cose: **chi** l'ha attribuito, **da cosa** deriva, **quale attività** l'ha prodotto | `[CANONE — DM <data>]` ha chi e quando; manca «da cosa deriva» | Il marcatore porta la base dell'ipotesi («base: SRD Jump», «base: mappa M7-C»), così il DM vede su cosa poggia |
| *Humans overrely on overconfident language models* (arXiv 2507.06306) e *What verbalized uncertainty is missing* (arXiv 2507.10587) | La fiducia che l'LLM dichiara («credo», «probabilmente») non segue l'esattezza, e le persone si fidano lo stesso | Il repo non usa gradi di fiducia: bene | **Non** aggiungere «fiducia alta/media/bassa» al marcatore: sarebbe rumore che sembra informazione |

## 4. La proposta, in forma di ADR breve

**Contesto.** Le guardie INFERRED filtrano davvero (18% delle ipotesi cambiate dal DM), ma la forma è dispersa: 4 varianti di INFERRED, 5 di canone, 6 testi della regola, l'86% delle marche senza domanda, e le decisioni a volte tracciate solo fuori dalla riga.

**Decisione (proposta).**
1. **Una grammatica**, tre stati e due etichette di fonte:
   - `[INFERRED — <domanda al DM>; base: <su cosa poggia>]` — la domanda è obbligatoria, la base anche.
   - `[CANONE — DM <AAAA-MM-GG>, <codice decisione>]` — il DM ha deciso.
   - `[CANONE GIOCATO <AAAA-MM-GG>]` — è successo al tavolo.
   - `[GENERATO — <script>]` — numero calcolato.
   - Fonti: `[SRD: <voce>]`, `[Private source — <manuale, p.>]`, `⚠ **Non SRD**` restano come sono.
   - Un'ipotesi scartata dal DM va in `<!-- storico -->` con la sua data, e sotto c'è il fatto nuovo.
2. **Un posto solo**: la grammatica sta in un file (`docs/reference/GUIDA-MARCATURE.md`); AGENTS.md, le skill e gli agent la richiamano con una riga e non la riscrivono. Un test lo controlla.
3. **Un blocco vincoli uguale in ogni skill che scrive contenuto**: permesso di dire «non so», ordine delle fonti (3.5 → PF1e → SRD, versione più forte), divieto di inventare statblocchi e poteri, e il passo finale «rileggi ogni numero: fonte, GENERATO o INFERRED».
4. **Cancelli**: niente `[INFERRED]` senza domanda nelle righe nuove; niente INFERRED tolto da un sorgente senza CANONE, GENERATO o storico nello stesso commit.

**Conseguenze.** Più lavoro per l'agente quando marca (una domanda e una base, ogni volta). Meno lavoro per il DM quando decide, e card che si costruiscono da sole dal testo. Una migrazione una tantum delle forme vecchie fuori da `plans/`. Rischio: un cancello troppo stretto blocca PR legittime; per questo propongo di partire non bloccante e promuovere dopo due settimane (canali di ADR-0099).

**Da rivedere se** la prova della scheda 7 non mostra miglioramento, o se dopo un mese le card del DM non diventano più rapide.

## 5. Piano in tre fasi

**Audit (fatto in parte, da chiudere)**
- Inventario delle forme fuori da `plans/` (moduli, Bestiario, PG, campaign, skill), con il conto per forma.
- Elenco delle skill e degli agent che scrivono contenuto e devono avere il blocco vincoli.
- Attendere il merge della #313.

**Sviluppo**
1. ADR nuovo (numero da `validate_docs.py --prossimo-adr`, prenotato in `plans/adr-prenotati.json`).
2. `GUIDA-MARCATURE.md` con la grammatica, esempi giusti e sbagliati.
3. AGENTS.md §5 e le 6 formulazioni sostituite da un rimando.
4. Blocco vincoli nelle skill scelte (scheda 5).
5. `inventory_inferred.py`: riconosce la grammatica, segnala le marche senza domanda, classifica come «meta» le righe di regola (le 25 di P16).
6. Controllo nuovo sul diff: INFERRED tolto senza traccia.
7. Migrazione delle forme vecchie (scheda 2), con prima e dopo contati.

**Prova e validazione**
- Test unitari della grammatica: 20 righe giuste e 20 sbagliate, prese dal repo.
- Prova A/B con agenti (scheda 7): stesse consegne con fatti mancanti noti, skill vecchia contro skill nuova; si contano invenzioni non marcate, marche senza domanda, marche con domanda e base. Si adotta solo se la nuova non peggiora nessuna delle tre.
- CI verde, baseline invariata o scesa, nessun PDF del tavolo con note di lavoro.
- A CI verde avviso il thread P16 e passo il merge al thread padre.

## 6. Le scelte del DM (2026-11-07)

| Scheda | Domanda | Scelta |
|---|---|---|
| 1 | forma del marcatore | A: domanda e base obbligatorie |
| 2 | forme vecchie di canone | A: migrate fuori da `plans/` |
| 3 | dove sta la regola | A: un file solo, richiamato |
| 4 | cancelli | A: non bloccanti due settimane, poi bloccanti |
| 5 | blocco vincoli | A: nelle skill che scrivono contenuto |
| 6 | 25 righe di regola di P16 | A: diventano meta |
| 7 | prova A/B | **B: 30 consegne × 2 versioni** |
| 8 | grado di fiducia | A: no |

## 7. La prova A/B

Da fare prima di rendere standard il blocco vincoli: 30 consegne con fatti
mancanti noti, ognuna fatta da un agente con la skill di `main` e da uno con la
skill del ramo. Protocollo e risultati in
[`esperimenti/marcature-2026-11-07/`](esperimenti/marcature-2026-11-07/).

## Fonti

- Anthropic, *Reduce hallucinations*: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Anthropic, *Skill authoring best practices*: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic, *Equipping agents for the real world with Agent Skills*: https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
- *Authoring Agent Skills: A Software-Engineering Approach* (UCL): https://arxiv.org/html/2607.25032v1
- W3C, *PROV-O*: https://www.w3.org/TR/prov-o/
- *Humans overrely on overconfident language models, across languages*: https://arxiv.org/html/2507.06306v1
- *What Verbalized Uncertainty in Language Models is Missing*: https://arxiv.org/html/2507.10587v1
- Script della misura: [`esperimenti/marcature-2026-11-07/misura_transizioni.py`](esperimenti/marcature-2026-11-07/misura_transizioni.py).
