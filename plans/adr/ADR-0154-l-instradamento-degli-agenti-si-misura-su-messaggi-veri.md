# ADR-0154 — L'instradamento degli agenti si misura su messaggi veri

**Stato**: proposta (2026-11-27)
**Data**: 2026-11-27
**Decisione-fonte**: il DM (Jfs), 2026-11-27, nel thread «Misurare e migliorare agenti, skill e automatismi»; il canale del cancello lo ha deciso l'agente `piattaforma` nello stesso thread, con le regole di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md).
**Rapporti**: misura l'instradamento di [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md) e ne corregge il numero dichiarato; segue i canali di ADR-0099 e la forma dei cricchetti di [ADR-0148](ADR-0148-i-fatti-si-verificano-con-script-e-gli-agenti-con-prove-fisse.md). Il mancato scatto dell'hook sul primo messaggio del thread lo corregge un altro thread («Garantire che la documentazione si aggiorni da sola», ADR-0153), non questo. L'audit è in `/mnt/project-files/agenti-eval-2026-11-27/AUDIT.md`.

## Contesto

ADR-0146 dichiarava che l'hook di `instradamento_agenti.py` suggerisce il
primo agente giusto in 23 frasi su 33 di `plans/instradamento/casi.json`.
Quelle frasi hanno un'etichetta di skill, non di agente, e in parte sono le
stesse su cui si sono tarati i trigger delle descrizioni: la misura e la
taratura usavano gli stessi casi. La seconda misura promessa, `--riepilogo`
dopo una settimana di thread, non si è mai potuta fare: i registri
`.claude/.uso-*.jsonl` sono in `.gitignore` e vivono nel container, e in un
thread nuovo partono da zero.

Su un set di messaggi veri, etichettato per agente e mai usato per tarare,
l'hook fa peggio di chi risponde sempre «sviluppatore».

## Decisione

1. **Un set d'oro di messaggi veri.** `plans/instradamento/agenti-oro.json`:
   29 messaggi, cioè 28 radici di thread scritte da Jfs e dal coordinatore dal
   10/10 al 27/11 e un resoconto di sottoagente, che l'hook riceve come se
   fosse un messaggio. L'etichetta è il primo agente che il lavoro chiede, o
   «nessuno» se il messaggio non chiede uno specialista. Una seconda
   etichettatura alla cieca, da un sottoagente che non vedeva la prima,
   concorda in 23 casi su 28, kappa di Cohen 0,78; dove le due differiscono,
   l'etichetta di B è fra le accettabili (accuratezza indulgente). Lo split è
   temporale: dev prima del 19/11 (11 casi), test dal 19/11 (18 casi). Le
   regole si tarano solo sul dev.
2. **Le metriche stanno in una libreria.** `scripts/eval_metriche.py`, sola
   stdlib: matrice di confusione, precision, recall e F1 per classe, macro e
   micro F1, accuracy esatta e indulgente, intervallo di Wilson al 95%, kappa
   di Cohen, bootstrap con seme e baseline della classe maggioritaria. Le
   convenzioni sono quelle di scikit-learn (`zero_division=0`, etichette
   sull'unione di oro e predizioni) e i valori sono `Fraction`, così un
   cancello non confronta float. scipy, già stable, serve solo da oracolo di
   Wilson nei test, che si saltano se manca. Nessuna libreria nuova.
   *Emendato il 2026-11-27 da Jfs: le metriche sono di scikit-learn e scipy,
   vedi l'emendamento in fondo.*
3. **La misura è un comando.** `instradamento_agenti.py --eval [--json]`
   confronta il primo agente suggerito con il set d'oro per dev, test e
   tutto; `--oro` sceglie un altro file.
4. **Un cricchetto sul test.** `--check` legge il campo `tetto` del set d'oro
   (giusti 4, giusti indulgenti 4, macro-F1 `107/1155`, misura su main
   `076a74d1`) ed esce 1 se uno dei tre scende sotto; se sale avvisa, e il
   tetto si alza a mano. Non si abbassa.
5. **In CI entra in testing dal merge.** Il passo «Agent routing
   (instradamento_agenti.py --check)» gira con `continue-on-error`. Passa a
   stable non prima di 14 giorni, e solo con tutte queste condizioni insieme:
   1. almeno 14 giorni e almeno 10 esecuzioni su main, contate dai log della
      CI;
   2. almeno 3 esecuzioni su PR che cambiano davvero l'ingresso:
      `instradamento_agenti.py`, `instradamento_skill.py`, il frontmatter di
      `skills/*/SKILL.md`, `.claude/agents/*.md` o il set d'oro;
   3. zero rossi non spiegati: ogni rosso è classificato come regressione
      vera, errore di etichetta o scambio neutro;
   4. le etichette del test confermate dal DM, oppure kappa ≥ 0,6 con una
      seconda etichettatura cieca (oggi 0,78);
   5. il JSON di `--eval` identico byte per byte fra due esecuzioni, e anche
      su Python 3.14;
   6. il passo sotto i 2 s, e il job principale non più lento del 5%;
   7. l'ok del DM sulla PR di promozione.

   Se verso il 2027-02-26 il passo è ancora in testing, la decisione si
   rivede.

## La misura di partenza

Su main `076a74d1`, con `python3 scripts/instradamento_agenti.py --eval`:

| Split | Hook, esatti | Wilson 95% | Macro-F1 | Baseline «sviluppatore» |
|---|---|---|---|---|
| test (18) | 4 | 0,09-0,45 | 107/1155 ≈ 0,093 | 6 esatti, macro-F1 0,0625 |
| tutti (29) | 7 | | | 10 esatti |

Le cause osservate caso per caso, non ancora corrette:

- omonimi nei trigger delle skill: «coordinate» di `rumblingstone-mapmaking`
  pesca «coordinato con il padre» e manda al `cartografo` 6 messaggi su 28;
  «hook» narrativo pesca gli hook tecnici; «master» pesca il DM; lo stesso
  fanno «caso», «corredo», «png», «avventura» e «Canva» in un elenco di
  connettori;
- a parità di voti vince la prosa, per l'ordine di `PRIORITA`;
- l'hook scatta anche sugli avvisi del coordinatore e sui resoconti dei
  sottoagenti, e ci mette una catena sbagliata;
- l'hook non scatta sul primo messaggio del thread, quindi la riga «Catena:»
  d'avvio non si registra e il cancello del push non morde (ADR-0153).

## Alternative considerate

| Opzione | Scartata perché |
|---|---|
| Rimisurare su `casi.json` | etichette di skill e non di agente, e casi usati anche per tarare |
| Aspettare `--riepilogo` dopo una settimana | i registri non sopravvivono al container |
| scikit-learn per le metriche | una dipendenza nuova per poche funzioni; le sue convenzioni si copiano e i test le confrontano. **Ribaltata da Jfs il 2026-11-27**: scikit-learn entra (emendamento in fondo) |
| Cancello bloccante subito | ADR-0099: un cancello nuovo passa da testing, e n = 18 è poco |
| Correggere i trigger nella stessa PR | una tecnica per PR: la correzione (PR 2) si misura contro questa base |

## Le conseguenze

- ADR-0146 ha un numero che si riproduce: 4 su 18 sul test, 7 su 29 in tutto,
  al posto di 23 su 33.
- Una PR che tocca i trigger o gli agenti vede subito se il primo agente
  peggiora sui messaggi veri.
- `eval_metriche` serve anche ai componenti che classificano e non sono
  ancora misurati: l'instradamento delle skill, `vincolo_skill`, i rilevatori
  del cricchetto, il riconoscimento del push (piano
  [`PIANO-MISURA-AGENTI-E-AUTOMATISMI`](../PIANO-MISURA-AGENTI-E-AUTOMATISMI.md)).

**Quello che si paga.**

- **n è piccolo.** 18 casi di test danno un intervallo di Wilson largo 36
  punti: un caso in più o in meno sposta l'accuracy di 5,6 punti. Il
  cricchetto conta interi per questo, e un rosso va guardato a mano prima di
  chiamarlo regressione.
- **Le etichette sono di un agente, non del DM.** Due etichettature cieche
  concordano (kappa 0,78), ma la conferma di Jfs manca; finché non arriva,
  una correzione tarata sul dev può imparare l'opinione dell'etichettatore.
- **La misura dipende dalle descrizioni delle skill.** L'hook riusa i loro
  trigger: chi cambia una descrizione per un'altra ragione può muovere il
  cricchetto. È la condizione 2 della promozione.
- **Nel repo entrano testi veri di Jfs.** Solo le parti scritte da lui:
  niente dati personali, e degli articoli incollati in un messaggio resta
  fuori il testo incollato.
- La misura «dopo una settimana» di ADR-0146 resta impossibile finché i
  registri sono locali; renderli persistenti è un lavoro a parte.

## Come si torna indietro

Togliere il passo «Agent routing» da `.github/workflows/ci.yml` spegne il
cricchetto; `--eval` e il set d'oro restano come misura a mano.

## Come si misura

- `python3 scripts/instradamento_agenti.py --eval` (o `--json`): la tabella
  per split.
- `python3 scripts/instradamento_agenti.py --check`: il cricchetto.
- Promozione: le condizioni del punto 5, contate dai log della CI.

---

## Emendamento del 2026-11-27 — le metriche sono di scikit-learn e scipy

**Stato**: chiesto da Jfs il 2026-11-27 nel thread, prima del merge della PR 1 · **Dettaglio**: `requirements-dev.txt` (la riga di scikit-learn) e §2 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md).

Jfs, alle 07:22: *«Non usare solo la stdlibi ma tutte le librerie utilizzate come standard de facto della community per favore e aggiorna tutto»*. Alle 07:27: *«Se serve usa anche numpy e panda keras e tensorflow se ha senso e segue le best pratices per verificare e risolvere le problematiche e migliora l audit ed i fix da fare nelle varie partindel progetto»*.

Il punto 2 della Decisione diventa questo. `eval_metriche.py` avvolge `sklearn.metrics` (`confusion_matrix`, `precision_recall_fscore_support`, `f1_score`, `accuracy_score`, `cohen_kappa_score`, `classification_report`, sempre con `zero_division=0` e con `labels=` l'unione di oro e predizioni), usa `DummyClassifier(strategy="most_frequent")` per la baseline e `scipy.stats` per l'intervallo di Wilson (`binomtest`) e per il bootstrap. Del repo resta quello che le librerie non danno: l'accuracy indulgente, l'insieme vuoto che sklearn rifiuta, il formato del rapporto e `macro_f1_esatta`, la macro-F1 come frazione ricavata dai conteggi interi della matrice. Un test la confronta con `f1_score`, e il cancello usa lei e non il float. scikit-learn entra fissato a `==1.9.1` in `requirements-dev.txt`, canale testing dal 2026-11-27, licenza BSD-3-Clause; porta con sé joblib, threadpoolctl e narwhals. Sta sul piano di sviluppo di [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md), come tcod: CI e chi sviluppa, mai la catena della sessione. ADR-0037 lo registra nel suo emendamento del 2026-11-27, con scipy, che lì mancava. sklearn e scipy si importano solo in `--eval` e `--check`; l'hook `--prompt` resta a 0,06 s, e un test lo verifica.

La riga «scikit-learn per le metriche» fra le alternative scartate è ribaltata da Jfs. Il motivo scritto allora, una dipendenza nuova per poche funzioni, pesa meno della regola di partire dallo standard di fatto della comunità (regola 6 di «Quando un agente risponde» in [`AGENTS.md`](../../AGENTS.md)).

**I numeri.** Il cancello non si muove: sul test 4 su 18, baseline 6 su 18, macro-F1 107/1155, gli stessi della versione stdlib. Le convenzioni dove sklearn sceglie per noi: il kappa indefinito vale 1 (`replace_undefined_by=1.0`), e lo spareggio della baseline segue l'ordine di `np.unique`, lo stesso che usava la versione stdlib. L'intervallo bootstrap della macro-F1 sul test passa da 0,0222-0,2222 a 0,0185-0,2159, perché `scipy.stats.bootstrap` ricampiona in un altro modo. Siccome dipende dalla versione di numpy, il bootstrap esce dal JSON di `--eval --json` e dal cancello, e resta nel rapporto di testo. 92 test verdi.

**Il deep learning, deciso nel thread.** Keras e TensorFlow per ora no: con 29 casi una rete impara a memoria. Lo ha detto il thread a Jfs alle 07:28, e Jfs può ribaltarlo. L'ordine è quello delle buone pratiche di ML: prima la baseline costante (fatta), poi un modello classico di scikit-learn (M3, PR 3: TF-IDF con `MultinomialNB` o `LogisticRegression`, validazione incrociata sul dev), e una rete solo se il classico non basta e con almeno 200 casi etichettati (PR 4: PyTorch e sentence-transformers, lo standard di fatto per il testo, con un modello di embedding piccolo e multilingue che stia nei 6 GB della RTX 4050; non è ancora stato provato su quella GPU). pandas entra solo se servono le tabelle dell'audit; numpy arriva già con scikit-learn.

**Quello che si paga.**

- `--check` passa da 0,19 s a 1,28 s per l'import di sklearn. Sta ancora sotto i 2 s della condizione 6, con meno margine; quanto pesa sul job principale non è misurato.
- `--eval` in testo ci mette 6,5 s, quasi tutti di bootstrap; `--eval --json` 1,35 s.
- La condizione 5 (JSON identico anche su Python 3.14) ora chiede anche che scikit-learn 1.9.1 si installi su 3.14.
- Un pacchetto in più nell'installazione di sviluppo, con tre dipendenze sue.


## Emendamento del 2026-11-27, pomeriggio: le etichette confermate dal DM

Jfs ha rivisto i 29 casi uno per uno, su card con la consigliata (scelte in `/mnt/project-files/agenti-eval-2026-11-27/SCELTE-JFS.tsv`, regole della cascata in `GUIDA-AGENTI-E-CASCATE.md` nella stessa cartella). Cambiano cinque etichette: lo stack di verifica via MCP passa a piattaforma, la ricerca da salvare accanto al changelog ad autore-documenti, Skullcrusher nel cortile ad autore-master, le best practice di Claude Code a sviluppatore, l'uso reale di connettori e plugin a piattaforma. Esce «Sì grazie», perché senza sapere a cosa risponde non si etichetta. Restano 28 casi (dev 11, test 17).

**I numeri nuovi.** Sul test l'hook fa 3 su 17 (Wilson 95% 0,06-0,41), la baseline 2 su 17. La macro-F1 è 73/924 ≈ 0,079, contro 0,026. Nel dev piattaforma e sviluppatore pareggiano 3 a 3, e la baseline prende piattaforma per l'ordine di `np.unique`: con un caso in più si ribalta. Il tetto è stato rimesso a questi valori. Si è mosso il set, non l'hook: il cricchetto vale da qui.

**Il primo scatto del cricchetto.** Al riallineo con main `77748c5b` la macro-F1 del test è scesa a 11/144: l'agente nuovo custode-memoria (#529, ADR-0151) prende il caso «memoria del progetto oltre il limite», che era etichettato sviluppatore. L'hook aveva ragione e l'etichetta era vecchia: Jfs l'ha cambiata in custode-memoria sulla card del 27/11. Con l'etichetta nuova il test fa 4 su 17 e la macro-F1 41/252 ≈ 0,163, e il tetto sale lì.

**Il kappa.** Dopo la conferma l'accordo con il secondo annotatore sale a 25 su 27 (kappa 0,91), ma non è più una misura indipendente: nei casi di disaccordo il DM ha scelto spesso l'etichetta di B. Il valore che conta resta 0,78, misurato prima.

## Emendamento del 2026-11-27, sera: M2

Due tecniche nella PR 2, una per commit. `testo_di_lavoro()` fa tacere l'hook `--prompt` sui messaggi che non chiedono lavoro (tocchi delle card, inoltri del coordinatore, notifiche, resoconti dei sottoagenti, via libera brevi) e di una busta `<wake>` legge solo i messaggi del principale. `OMONIMI` in `instradamento_skill.py` toglie gli usi di «coordinate», «hook», «caso», «png», «master», «corredo» e «Canva» che parlano d'altro.

**I numeri.** Sul test (n=17) gli esatti restano 4 e gli indulgenti 4; la macro-F1 sale da 41/252 ≈ 0,163 a 58/315 ≈ 0,184, tutta per gli omonimi. Il dev resta a 4 su 11. Il tetto sale a 58/315. La prima tecnica sul set d'oro non conta, perché il set tiene il testo nudo e non la busta: misurata sui 103 prompt veri del thread, presi dalla trascrizione con uno script fuori dal repo, l'hook suggerisce un agente 1 volta invece di 57 (tocchi sulle card da 36 su 39 a 0, messaggi di Jfs da 3 su 10 a 1, che è una richiesta vera). `instradamento_skill.py --check` è invariato: 17 omissioni su 50, 1 violazione.

**Quello che si paga.** La prima tecnica non ha un cricchetto finché non c'è un set di prompt grezzi. Ogni `<relay>` del coordinatore tace anche quando apre lavoro; il cancello del push legge ancora la riga «Catena:» scritta. Le regex degli omonimi sono euristiche, con i falsi positivi possibili nei commenti. Gli errori rimasti nel dev sono parole che mancano ai trigger, non omonimi.
