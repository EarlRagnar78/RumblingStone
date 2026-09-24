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
   (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza
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

---

## Aggiornamento 2026-09-16 — la quinta voce: **prima di creare**, non solo prima di chiudere

Le quattro voci originali riguardano chi **chiude** un lotto. Ne mancava una per
chi **apre** un documento, e l'assenza è costata un errore vero.

🐛 **`ADR-0049` è stato assegnato due volte in due giorni**: all'edizione
commerciale (PR #138) e poi al margine del bosco (PR #141). Chi scriveva il
secondo non ha guardato la cartella, e **nessuno dei controlli poteva vederlo** —
nessun link era rotto, nessun ADR mancava da `docs/INDEX.md`, che si limitava a
mostrare due righe con lo stesso numero.

**Il numero di un ADR è la sua identità.** Si cita nei commit, nei piani, nel
codice e nei changelog, e il repo ne ha centinaia di riferimenti: due decisioni
che condividono un numero rendono ambigua ogni citazione **all'indietro**, su
documenti già scritti e già mergiati.

**La regola**, e ha due metà perché una sola non basterebbe:

| | Cosa | Quando |
|---|---|---|
| **preventiva** | `python3 scripts/validate_docs.py --prossimo-adr` | **prima** di scrivere l'ADR: stampa l'ultimo numero e il primo libero, ed esce 1 se una collisione esiste già |
| **esigibile** | `validate_docs --sorgenti` boccia due file con lo stesso numero | in CI, **dopo** che il file esiste |

Il numero si conta da `plans/adr/`, non da `docs/INDEX.md` — quarta regola di
[ADR-0045](ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md), e qui l'indice era
proprio il documento che non se n'era accorto.

**Per un piano nuovo** il numero non esiste, ma la regola ha già la sua
decisione: si legge `plans/INDEX.md` prima di aprirlo
([ADR-0044](ADR-0044-prima-si-guardano-i-piani-che-ci-sono.md)). Un piano
duplicato non rompe le citazioni; divide il lavoro in due posti che divergono,
ed è già costato sei settimane con la PR #72.

⚠️ **Il limite, dichiarato.** La metà preventiva funziona solo se la si esegue:
non è un cancello all'ingresso, è un comando da ricordarsi. Quello vero arriva
in CI, cioè **dopo** che il file è stato scritto e i riferimenti sparsi — e
rinumerare allora costa quel che è costato qui: **9 file da correggere**. Un
cancello che prende tardi è meglio di nessuno, e peggio di uno che prende
subito; chiudere anche quella metà vorrebbe dire un hook, e un hook si può
saltare.
