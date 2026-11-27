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
| scikit-learn per le metriche | una dipendenza nuova per poche funzioni; le sue convenzioni si copiano e i test le confrontano |
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
