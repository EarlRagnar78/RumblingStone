# ADR-0114 — Ogni prompt ha una scheda, e ogni skill le sue prove

**Stato**: accettata (2026-11-08): la prova A/B del secondo lotto non peggiora gli inventati senza marca (32 → 30 su 54 consegne, marche complete 74 → 95; [ESITO](../esperimenti/schede-prompt-2026-11-08/ab-lotto2/ESITO.md))
**Data**: 2026-11-08
**Canale (ADR-0099)**: stable dal 2026-11-25, scelta del DM sulla card del 2026-11-25 (*«Tutti e sei, con il codice»*, D8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md)). 0 avvisi della scheda in 168 run su `main` dall'8/11; i rilievi di `check_schede` sono errori di `validate_skills.py` ([misura](../esperimenti/promozioni-2026-11-25/MISURE.md)).
**Decisione-fonte**: il DM (Jfs), 2026-11-08: *«fissiamo uno standard del repo per tutti i prompt magari in schede per limitare le allucinazioni e la direzione di sviluppo in maniera professionale»* *«usa sempre la versione migliore adottata dalla comunità degli sviluppatori e standard de facto migliore»* e *«in ogni indagine il candidato di base è lo standard di fatto della comunità. Una soluzione nostra entra solo se la misura boccia lo standard, e in quel caso il motivo va scritto nell'ADR […] per tutte le parti del progetto ma sempre con misura come decisione»*. Thread «Fissare lo standard dei prompt a schede»: perimetro = skill e brief, AGENTS.md snellito con misura.
**Rapporti**: usa la grammatica e il blocco vincoli di [ADR-0109](ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md), i cancelli di [ADR-0108](ADR-0108-i-cancelli-deterministici-stanno-in-ogni-skill.md), i canali di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md). Lascia i prompt immagine ad [ADR-0015](ADR-0015-standard-prompt-immagine.md). Ricerca e misura in [RICERCA-SCHEDE-PROMPT-2026-11](../RICERCA-SCHEDE-PROMPT-2026-11.md).

## Contesto

Le 18 skill hanno tutte i cancelli, ma il resto varia da una skill all'altra.
Il blocco vincoli c'è in 10. Formato d'uscita e controllo «prima di consegnare»
ci sono in 4. Ci sono 41 date di storia nei corpi. Le prove con trappola
esistono per 10 skill, in un file di esperimento, senza uno script del repo.
I brief agli agenti si scrivono a mano ogni volta. Lo stato dell'arte va in due
direzioni insieme. Anthropic chiede poche sezioni chiare, niente storia, e
almeno tre prove per skill. Gli studi dicono che più istruzioni si seguono peggio,
e che un AGENTS.md lungo non migliora i risultati ma costa di più (ETH, arXiv
2602.11988). Nel repo, l'unica riduzione delle invenzioni misurata è del 43% (A/B
di ADR-0109, p = 0,059).

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Tre schede (skill, brief, prova) con le prove nella forma di `claude plugin eval` (scelta) | è lo standard di fatto delle Agent Skills; un controllo sa cosa cercare; le prove dicono se una riscrittura aiuta | 18 skill da riordinare; le prove costano token |
| Un modello unico, molto dettagliato, per ogni prompt | tutto in un posto | più istruzioni, seguite peggio (IFScale, arXiv 2507.11538) |
| Prove in un file JSON del repo, formato nostro | nessuna dipendenza | nessuno strumento esterno lo legge; il formato di `claude plugin eval` è già documentato |
| Lasciare le skill come sono | nessun lavoro | 8 skill senza nessuna misura delle invenzioni |

## Decisione

**Ogni prompt del repo segue la sua scheda di [GUIDA-SCHEDE-PROMPT](../../docs/reference/GUIDA-SCHEDE-PROMPT.md),
e ogni skill ha almeno tre prove con trappola in `skills/<nome>/evals/`.**

1. **Scheda skill**: frontmatter con «cosa fa e quando», poi `Quando no`,
   `Fonti`, `Vincoli sui fatti` (solo nelle skill di contenuto), `Procedura`,
   `Formato d'uscita`, `Prima di consegnare`, `Cancelli deterministici`. La
   storia delle regole va negli ADR.
2. **Scheda brief**: Obiettivo, Stato vero, Cosa puoi toccare, Vincoli, Formato
   d'uscita, Fatto quando, Se non sai. Le regole si richiamano, non si
   riscrivono.
3. **Scheda prova**: casi nella forma di `claude plugin eval` (`prompt.md`,
   `case.yaml`, `graders/`). Ci sono le 30 consegne di ADR-0109 e 24 nuove per le
   8 skill che non ne avevano. `scripts/prove_skill.py` controlla la forma (in
   CI), prepara la A/B alla cieca e ne scrive l'esito.
4. **Cancello**: `validate_skills.py` avvisa per le sezioni mancanti o fuori
   ordine, per le date nel corpo e per le prove sotto il minimo. Canale testing:
   avvisa e non blocca. L'audit settimanale propone di farlo bloccare due
   settimane dopo che il secondo lotto è su main.
5. **Regola di partenza del progetto** (vale per ogni parte: skill, codice,
   mappe, storia, editoria, booklet). In ogni indagine il candidato di base è
   lo standard di fatto della comunità. Una soluzione nostra entra solo se la
   misura boccia lo standard, e il motivo si scrive nell'ADR, nella tabella
   delle alternative. Questo ADR la applica a sé stesso: le prove hanno la forma
   di `claude plugin eval` e non un formato nostro, e la scheda skill è quella
   delle Agent Skills con le regole di Anthropic.
6. **Adozione a lotti**. Primo lotto: guida, prove, script e cancello. Secondo
   lotto: le 18 skill riordinate e AGENTS.md snellito, ognuno adottato solo se
   `prove_skill.py esito` non peggiora gli inventati senza marca.

## Conseguenze

- Ogni indagine nuova parte con una riga in più fra le alternative: lo standard
  di fatto, e la misura che lo tiene o lo boccia.

- Una riscrittura di skill ha un numero prima e dopo, non un'impressione.
- Ogni agente trova le stesse cose nello stesso posto, in ogni skill.
- Le prove costano: con le scelte di oggi una A/B completa sono 108 esecuzioni
  più il giudice.
- Il giudice è un modello: le sue somme possono sbagliare, e il voto del DM resta
  il riscontro vero.
- Esito del lotto 2: le schede non riducono le invenzioni in modo dimostrato
  (4 casi meglio, 4 peggio, p = 0,64); aumentano le marche scritte nella forma
  giusta. Il guadagno è di ordine e di costo (AGENTS.md −25%), non di verità.
- Gli studi citati misurano compiti di codice e modelli precisi. Per gli altri
  agenti di `agents.conf` (Gemini, Codex…) non abbiamo misure.

**Da rivedere se**: la A/B del secondo lotto peggiora gli inventati senza marca
anche dopo una correzione; oppure `claude plugin eval` cambia formato; oppure,
dopo un mese bloccante, il cancello boccia più PR legittime che schede rotte.
