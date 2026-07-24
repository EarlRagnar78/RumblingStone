# ADR-0009 — Gate automatico di tracciatura: CHANGELOG obbligatorio e promemoria ADR prima del merge

**Stato**: accettata
**Data**: 2026-07-20
**Decisione-fonte**: richiesta DM in PR #56 («regola changelog+ADR prima di mergiare, automatica se possibile»)

## Contesto

La regola d'oro dei piani (chi chiude un lotto aggiorna checklist + INDEX +
CHANGELOG nello stesso commit — skill `rumblingstone-plans`) era pura
disciplina: funzionava finché l'agente o il DM se ne ricordavano. È già
successo che una PR mergiasse senza tracciatura (PR #40, recuperata a
posteriori). Il DM chiede che la regola diventi automatica dove possibile.

## Decisione

Il rispetto della regola d'oro è verificato da
`scripts/check_plans_discipline.py`, che gira in due punti:

1. **CI** (`.github/workflows/ci.yml`, solo su `pull_request`, contro il
   base ref con `fetch-depth: 0`): una PR che modifica file **strutturali**
   (`scripts/`, `skills/`, `Script/`, `.github/`, `plans/adr/`) senza
   toccare `plans/CHANGELOG.md` **fallisce** (exit 1) — quindi non si
   mergia rossa.
2. **Hook `pre-push` locale** (installato da
   `scripts/install-git-hooks.sh`): stesso check contro `origin/main`
   prima di ogni push; bypass consapevole con `git push --no-verify`.

Limite dichiarato (onestà del gate): **l'obbligo di ADR non è bloccante.**
«Questa modifica è una scelta architetturale?» non è decidibile da uno
script; il gate emette un **promemoria** (warning) quando il range
contiene segnali forti — nuova skill, nuovo script top-level, modifica ai
workflow CI — senza alcun tocco a `plans/adr/`. La decisione se scrivere
l'ADR resta umana, ma non può più passare inosservata.

Il contenuto di campagna (`campaign/`, archi `00_`-`09_`, `Bestiario/`,
`PG/`) è **esente**: chiudere una sessione al tavolo non richiede
changelog di infrastruttura (i branch `campaign-group-*`, ADR-0007,
pushano canone senza attriti).

## Conseguenze

- La tracciatura non dipende più dalla memoria: una PR strutturale senza
  riga di CHANGELOG diventa un rosso in CI, visibile prima del merge.
- Falso positivo possibile (es. refactoring banale di uno script): il
  costo è una riga di changelog — voluto, la riga è comunque informazione.
- Il promemoria ADR può essere ignorato: accettato per non generare ADR
  di facciata; il warning in CI resta agli atti della PR.
- Da rivisitare: se i falsi positivi diventassero rumore, introdurre una
  lista di esenzioni nel gate (con questo ADR da aggiornare).
