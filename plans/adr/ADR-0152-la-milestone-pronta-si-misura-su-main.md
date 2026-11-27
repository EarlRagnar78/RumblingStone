# ADR-0152 — La milestone pronta si misura su main, e il segnale arriva alla routine del lunedì

**Stato**: accettata (2026-11-27, card di Jfs: «Workflow, issue e routine del lunedì»)
**Data**: 2026-11-27
**Decisione-fonte**: la domanda di Jfs del 2026-11-27 nel thread del progetto: l'agente `piattaforma` scatta da solo quando una milestone è raggiunta? Il modo in cui il segnale arriva a un thread è su una card a Jfs (routine del lunedì, controllo giornaliero, solo hook); Jfs ha scelto la consigliata, la routine del lunedì, sulla card del 2026-11-27.
**Rapporti**: applica [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (lo strumento nuovo entra in testing e sale con i suoi criteri) e [ADR-0100](ADR-0100-il-rilascio-e-una-pr.md) (il rilascio resta una PR, e il tag lo crea solo `release.yml`); segue il modello del workflow del lunedì di [ADR-0149](ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md); riguarda l'agente `piattaforma` di [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md).

> Il numero 0152 non è in `plans/adr-prenotati.json`, che si scrive solo su
> main: 0150 è della #519 e 0151 del thread del custode della memoria, nessuno
> dei due ancora su main. La PR lo dichiara.

## Contesto

Le milestone della roadmap esistono solo su GitHub: cinque, da v1.1.0 a
v1.5.0, tutte aperte il 27/11. I loro criteri d'uscita stanno in prosa nella
descrizione di ognuna e in uno specchio della roadmap fuori dal repo.
L'audit del 27/11 ha trovato che:

- nessuno script valuta quei criteri: per sapere se una milestone è finita
  bisogna rileggerle tutte;
- l'agente `piattaforma` (`.claude/agents/piattaforma.md`) parte solo se il
  messaggio contiene parole come «rilascio» o «roadmap»
  (`PAROLE_AGENTE` in `scripts/instradamento_agenti.py`), cioè quando qualcuno
  ci pensa già;
- l'assegnazione a mano delle PR alle milestone si è fermata: le dieci PR
  unite dal 25/11 (#516-#526) non ne hanno nessuna.

La risposta alla domanda di Jfs era quindi no: niente fa partire l'agente
quando una milestone è pronta, perché niente sa che lo è.

## Alternative considerate

| Opzione | Scartata perché |
|---|---|
| Un hook di Claude Code che controlla le milestone a ogni prompt | gli hook girano solo dentro una sessione: non vedono un merge fatto fuori sessione né un criterio che diventa vero senza merge (una conferma del DM, un tag), e non possono aprire un altro thread |
| Un job in `ci.yml` | `ci.yml` non ha un trigger `schedule`, e aggiungerlo farebbe girare di lunedì tutti i suoi job (lo stesso motivo di ADR-0149) |
| Leggere i criteri dalla descrizione delle milestone su GitHub | è prosa: una macchina non sa dire se «la documentazione è completa»; e in CI il token non sempre legge le milestone |
| Riprendere l'assegnazione a mano delle PR alle milestone | è la regola che si è fermata da sola il 25/11; e una PR assegnata non dice se il criterio è vero |
| Aprire una issue già da oggi | il rilevatore è nuovo; un falso «pronta» manderebbe l'agente a preparare un rilascio che non c'è. ADR-0099 vuole prima il canale testing |

## Decisione

1. **Il registro.** `plans/milestone.json` tiene le cinque milestone (numero
   su GitHub, versione, titolo) con i criteri d'uscita in forma che una
   macchina legge. Tre tipi di criterio:
   - `comando`, vero se esce 0 (dalla radice del repo, con `shlex`, senza
     shell);
   - `file`, una o più regex che devono comparire in ogni file o mancare in
     tutti;
   - `dm`, vero solo se `confermato` porta data e luogo in cui Jfs l'ha
     detto; un `misura_mancante` accanto dice quale comando lo sostituirebbe.

   I criteri della «Definizione di fatto» (regola di Jfs del 2026-11-09) sono
   marcati `comune` e ripetuti per ogni versione. Le milestone restano su
   GitHub: chi cambia la descrizione di una cambia anche il registro.
2. **Il rilevatore.** `scripts/milestone_pronte.py` valuta il registro senza
   scrivere niente. Una milestone è **pronta** se tutti i criteri sono veri
   tranne `fatto-changelog`, `fatto-versione` e `fatto-tag`, che sono il
   rilascio stesso; **rilasciata** se sono veri anche quelli; altrimenti
   **non pronta**, con gli id dei criteri falsi. Esce 2 se il registro è
   rotto (JSON, file citati, regex, id doppi, comando che non esiste), 0
   altrimenti. `--pronte` stampa le versioni pronte, una per riga;
   `--check --solo-integrita` controlla il registro senza lanciare i comandi;
   `--github` confronta numeri e titoli con le milestone di GitHub.
3. **Il workflow.** `.github/workflows/milestone.yml` gira a ogni push su main
   e ogni lunedì alle 06:35 UTC, dopo `sincronia-giocato.yml`. Non gira sulle
   PR e non le blocca. In testing scrive il riepilogo e, per ogni versione
   pronta, la riga «Aprirebbe la issue: milestone vX.Y.Z pronta»; non apre
   issue.
4. **Il segnale arriva alla routine del lunedì** (la consigliata della card).
   L'attività pianificata «Audit settimanale PR e decisioni», lunedì alle
   08:47 ora di Roma, lancia `python3 scripts/milestone_pronte.py --pronte` e,
   per ogni versione pronta, chiede al coordinatore un thread con la catena
   `piattaforma`, poi `sviluppatore`, poi `autore-documenti`.
5. **La promozione a stable.** Il rilevatore sale dopo 14 giorni e 10 run su
   main senza falsi allarmi, con i criteri proposti da `piattaforma`:
   determinismo (due run sullo stesso commit danno lo stesso esito),
   idempotenza (il run non cambia niente nel repo), mutazione (un criterio
   falsificato di proposito si vede) e durata sotto i 2 minuti. Da stable il
   workflow apre anche una issue per versione, con un'etichetta e la versione
   nel titolo, senza doppioni, e prende il permesso `issues: write`.

## Le conseguenze

- Il 27/11 nessuna milestone è pronta. La più vicina è v1.1.0, ferma su tre
  criteri:
  - `readme-adr`: il README dice 123 ADR, sul disco ce ne sono 145 (template
    escluso);
  - `fatto-guide`: la conferma del DM che le guide coprono l'area;
  - `fatto-adr-stato`: ADR-0119, 0120 e 0121 sono ancora «proposta»; i
    controlli dei primi due sono stable dal 25/11 (D8 di
    `PIANO-PIATTAFORMA-DI-SVILUPPO`), la misura del terzo è ancora una prova
    in `plans/esperimenti/`.
- `milestone_pronte.py` impiega 2,6 s sull'albero del 27/11;
  `--check --solo-integrita` 0,06 s. I 26 test nuovi portano i test raccolti
  da 3.579 a 3.605.
- Il prompt della routine del lunedì non sta nel repo: lo cambia il
  coordinatore dopo il sì di Jfs alla card. Finché non lo cambia, il segnale
  si legge solo nel riepilogo del workflow.

**Quello che si paga.**

- **Quali ADR stanno in quale milestone l'ha dedotto `piattaforma`** dalle PR
  assegnate fino al 25/11, non da una lista di Jfs. Un ADR assente dal
  registro non entra in `fatto-adr-stato` e nessuno se ne accorge.
- **Le regex sui passi di `ci.yml` dipendono dal nome del passo.** Il
  criterio `fatto-canali` di v1.3.0 cerca «Standard del volume — non
  bloccante» e vuole che manchi: se il passo cambia nome e resta non
  bloccante, il criterio diventa vero a torto.
- **`comando` gira con `shlex` e senza shell**: niente pipe né `&&`. Un
  criterio che li chiede diventa uno script a parte.
- **I criteri `dm` con `misura_mancante` sono misure da costruire**, e finché
  mancano bloccano la milestone in attesa di una conferma scritta nel
  registro: il controllo del numero di ADR del README in `validate_docs`, un
  `--check` con soglia in `misura_plugin_regole.py`, il test di
  `render_map_svg` senza `--strict`, il campo «del tavolo» nelle decisioni.
  Il criterio «documentazione completa» potrà usare
  `python3 scripts/documentazione_allineata.py --debito --json` del thread
  «Garantire che la documentazione si aggiorni da sola» (ADR-0153) quando
  sarà su main.
- **Il registro e GitHub possono divergere.** `--github` confronta solo
  numeri e titoli; chi cambia i criteri nella descrizione di una milestone e
  non nel registro non lo vede nessuno.
- **Il segnale ha una settimana di ritardo** nel caso peggiore: un criterio
  che diventa vero il martedì arriva alla routine il lunedì dopo. Il push su
  main lo scrive subito nel riepilogo, ma nessuno legge il riepilogo di ogni
  run.
- **L'agente `piattaforma` non conosce ancora il rilevatore.** Il suo
  paragrafo «Roadmap» va aggiornato da chi lavora su `.claude/`.

**Da rivedere se**: Jfs sceglie sulla card il controllo giornaliero o il solo
hook; dopo 14 giorni il rilevatore ha dato un «pronta» falso; una milestone
nuova si apre su GitHub senza la sua voce nel registro; ADR-0153 porta su main
la misura della documentazione, che sostituisce `fatto-guide`.
