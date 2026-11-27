# ADR-0148 — I fatti si verificano con script, e gli agenti con prove fisse

**Stato**: proposta (2026-11-20)
**Data**: 2026-11-20
**Decisione-fonte**: il DM (Jfs), 2026-11-20, nel thread «Aggiungere verificatori deterministici e prove per agente»: contro le allucinazioni, «verificatori deterministici: script che controllano numeri, regole e canone, come verifica_scheda o i test, invece di un altro modello che rilegge» e «casi di prova fissi per agente: si vede subito se un aggiornamento peggiora qualcosa», «in maniera deterministica con test e verifiche vere». Sulla card del 20/11 Jfs affida a questo thread anche l'aggiornamento misurato di agenti, skill e plugin, in un ADR dopo la #510.
**Rapporti**: si appoggia a [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md) (gli agenti) e a [ADR-0114](ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md) (le prove delle skill nella forma di `claude plugin eval`); segue [ADR-0124](ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) (regola, atteso, ha, fonte, file:riga) e i canali di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md). La base è la proposta del thread della #510, `/mnt/project-files/agenti-2026-11-20/PROPOSTA-AGGIORNARE-AGENTI-SKILL-PLUGIN.md`.

## Contesto

Un fatto numerico o di canone nel repo arriva al tavolo in tre modi: un
verificatore lo controlla, un modello lo rilegge, o nessuno lo guarda.
L'inventario del 20/11 (`plans/esperimenti/verificatori-2026-11-20/INVENTARIO.md`)
dice che i numeri delle schede e i fatti già strutturati di `state.yaml` hanno
il loro script, mentre il registro dei PX e i rimandi per sezione no.

Gli agenti della #510 hanno un test di forma (`test_agenti.py`), ma nessuna
prova di quello che producono. Le prove delle skill (ADR-0114) sono 108 giudici,
tutti `type: llm`: ogni esito dipende da un modello che giudica.

## Decisione

1. **Un fatto che si può contare si conta.** Due verificatori nuovi, con
   l'uscita di ADR-0124:
   - `scripts/verifica_px.py`, cancello bloccante in CI da subito (regola del
     DM: ciò che un controllo trova si corregge e il controllo diventa
     cancello): la somma delle righe del registro è il totale (R1); il livello
     dai PX segue la tabella dei PX, che non è nell'SRD [Private source: PHB
     3.5, Table 3–2] (R2); si sale di un livello alla volta [Private source:
     DMG 3.5, cap. 2] e i PX non stanno sotto la soglia del livello al tavolo
     (R3); il livello al tavolo è il livello effettivo di `state.yaml`, l'ECL
     se scritto, altrimenti i livelli di classe più l'LA (SRD, Monsters as
     Races), e ogni PG dei totali ha la sua riga (R4).
   - `scripts/verifica_rimandi.py`, in CI in testing fino al 2026-12-04 (non
     blocca; poi stable se non dà falsi allarmi): un «FILE §N» o un «vedi §N»
     punta a un titolo che esiste. Un rimando che lo script non sa risolvere
     va fra i non verificabili, mai fra le violazioni. Le violazioni già
     portate al DM stanno in `IN_ATTESA` e il cancello boccia solo quelle
     nuove.
2. **Ogni agente ha almeno tre casi di prova** in `.claude/agent-evals/<agente>/<caso>/`,
   nella forma delle skill (`prompt.md`, `case.yaml`, `graders/`), letti da
   `prove_skill.py` esteso e non da uno script nuovo. La cartella sta fuori da
   `.claude/agents/` perché Claude Code non legga i casi come agenti.
3. **Giudici deterministici, e giudici giudicati.** Ogni caso d'agente ha almeno
   un giudice `regex`, `tool_used`, `tool_order` o `file_exists`, i tipi che
   `claude plugin eval` già conosce. Ogni caso porta due esecuzioni fisse,
   `esempi/buona/` ed `esempi/cattiva/`: in CI `prove_skill.py esempi` controlla
   che la buona passi tutti i giudici e la cattiva ne perda almeno uno. Un
   giudice che non distingue le due si vede prima di usarlo.
4. **L'esito si registra con un'impronta.** `prove_skill.py impronta` fa lo
   sha256 del file dell'agente, di tutti i file delle skill che precarica e dei
   suoi casi. `esegui` lancia `claude -p --agent <nome>` sui casi in un worktree
   usa e getta e salva risposta, trace e file prodotti; `registra` valuta
   l'esecuzione con i soli giudici deterministici e scrive una riga in
   `.claude/agent-evals/ESITI.jsonl`, con la versione della CLI `claude`, i
   casi falliti (che valgono 0) e quelli non eseguiti. L'impronta registrata
   è quella dell'agente e delle skill del worktree da cui l'agente ha girato.
   `esegui` passa `allowed_tools` del caso, vieta `git push`, `commit`,
   `reset` e `checkout` e toglie al worktree l'indirizzo di push; dopo ogni
   caso riporta il worktree al commit di partenza. Rifiuta la radice del repo
   come cartella di lavoro; `esegui` e `registra` non partono dal server MCP
   (`mcp_vietati` nel manifest), nemmeno con `--allow-write`.
5. **Cricchetto, prima in testing.** Su una PR che tocca un agente, una skill
   che precarica o i suoi casi, `prove_skill.py cricchetto` chiede un esito con
   l'impronta nuova e un punteggio non sotto il precedente. Per ADR-0099 entra
   in testing: il passo in CI gira già con `--rigoroso`, ma con
   `continue-on-error`, così i rossi si contano senza bloccare; alla
   promozione a stable (14 giorni, 10 run su main, zero falsi allarmi non
   spiegati) si toglie `continue-on-error`. Il confronto è con l'ultimo esito
   di impronta diversa, non con il migliore: un esito peggiore registrato in
   testing abbassa la soglia, e va guardato a mano.

## Alternative considerate

| Opzione | Deterministica? | Scartata perché |
|---|---|---|
| Un modello che rilegge (giudice `llm`) | no | è ciò che Jfs chiede di non usare come prova; resta solo come indicatore accanto ai giudici deterministici |
| Uno script nuovo per gli agenti | sì | una seconda forma dei casi da tenere allineata; `prove_skill.py` c'era già |
| Casi in `.claude/agents/evals/` (la proposta della #510) | — | Claude Code cerca gli agenti anche nelle sottocartelle: i `prompt.md` rischiano di diventare agenti |
| Eseguire gli agenti in CI | no | chiede una chiave e costa token a ogni PR; l'esito cambia da un'esecuzione all'altra |
| Cricchetto bloccante subito | sì | ADR-0099: un cancello nuovo passa da testing |

## Le conseguenze

- Il registro dei PX e i rimandi per sezione non si rileggono più a mano:
  `verifica_px` trova 366 errori inseriti su 366, `verifica_rimandi` 435 su 435,
  e sullo storico dei rimandi 2 rotture vere e 0 falsi allarmi.
- Una regressione di un agente sulle sue trappole (un numero inventato, un
  test disattivato, una data superata, una tabella generata scritta a mano) ha
  un numero prima e dopo.
- Esiti «prima» registrati il 20/11 con gli agenti della #510 e la CLI
  2.1.329: una riga per agente in `.claude/agent-evals/ESITI.jsonl`, media
  0,975, 33 casi su 36 pieni. I tre sotto sono errori veri (un trattino lungo
  in un ADR, un'etichetta fra parentesi in un box, un piano TDD che non apre
  con il test). Alla prima passata due giudici erano falsi negativi di forma
  e sono stati allargati prima di registrare.
- Le revisioni di `regolista`, `custode-canone` e `piattaforma` sul lavoro di
  questo ADR hanno trovato errori veri nei casi stessi (una battaglia non
  giocata data per giocata, un calendario sbagliato, fonti SRD che erano del
  PHB): i casi passano anche loro dai verificatori.

**Quello che si paga.**

- **Un giudice deterministico vede la forma della risposta, non la sua
  verità piena.** «Dice 86.354» è controllabile; «ha ragionato bene» no. Un
  agente può passare un caso per la strada sbagliata, e una trappola nuova si
  scrive a mano.
- **I casi sono pochi e si invecchiano.** 36 casi per 12 agenti: un fatto del
  canone che cambia (una data, una classe) rompe il caso, e il caso va
  aggiornato con il canone. `custode-canone` li ha controllati il 20/11.
  *(Nota del 2026-11-21: con `sincronizzatore-giocato` e i suoi cinque casi
  i casi sono 41 per 13 agenti, [ADR-0149](ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md).)*
- **Eseguire costa.** Una passata dei 36 casi dura circa quaranta minuti e consuma
  chiamate a un modello; l'esito oscilla fra due esecuzioni, quindi il
  cricchetto confronta medie su un'esecuzione per caso e può segnalare un calo
  che è rumore. Per questo resta in testing finché non si misura quanto oscilla.
- **`verifica_rimandi` giudica il 59% dei rimandi.** Il resto (nome ambiguo,
  bersaglio senza sezioni numerate, riga che nomina un altro documento, «§N-bis»)
  non è controllato. La regola sul «§N» senza nome è stata tarata sul repo di
  oggi; le istantanee della storia sono la sola prova fuori campione.
- **`verifica_px` controlla il registro, non la prosa.** I PX e i livelli
  scritti nei master (19 e 13 righe) restano fuori: è il buco 2 dell'inventario.
- **L'impronta non copre tutto ciò che guida un agente.** `.claude/rules/`,
  `CLAUDE.md` e `skills/REGOLE-DORO.md` cambiano il comportamento ma non
  entrano nell'impronta: una loro modifica non chiede un esito nuovo.
- **Il contenimento di `esegui` è una rete, non una gabbia.** I divieti
  coprono push, commit, reset e checkout; un agente con Bash può ancora
  scrivere fuori dal worktree con un percorso assoluto. I casi di oggi
  permettono Read, Glob, Grep e Bash.
- La qualità della prosa resta al voto alla cieca di Jfs (ADR-0093).
