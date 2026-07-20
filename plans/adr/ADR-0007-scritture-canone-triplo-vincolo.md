# ADR-0007 — Scritture di canone da parte degli script: permesse col triplo vincolo

**Stato**: accettata
**Data**: 2026-07-20
**Decisione-fonte**: piano [AUTOMAZIONE-STATO-SESSIONI](../PIANO-AUTOMAZIONE-STATO-SESSIONI-BRANCH-GRUPPO.md) §6-§8 (domande approvate dal DM 2026-07-20)

## Contesto

La regola storica del toolkit — «gli script non scrivono mai
`campaign/state.md` o `campaign/sessions/*.md`» — nasce per proteggere il
canone da automazioni cieche, e ha già un'eccezione di fatto
(`update_xp.py` scrive il ledger). Il costo è che il DM ricopia a mano in
`state.md` modifiche meccaniche che gli script hanno già calcolato
(March Clock, changelog §8). Il DM ha chiesto di automatizzare il flusso
di fine sessione mantenendo `main` pulito (branch-per-gruppo).

## Decisione

Gli script POSSONO scrivere canone solo se valgono, insieme:

1. **Branch**: il branch corrente non è protetto (`main`/`master`) e, se
   `campaign/group.yaml` è configurato, coincide con
   `campaign-group-<group>` (guardia: `dmcore.gitio.guard_canon_branch`,
   CLI `campaign_branch.py`).
2. **Conferma**: il DM ha visto e confermato il diff esatto, blocco per
   blocco (`--yes` esiste per test/CI, non per il flusso reale).
3. **Regioni marcate**: per `state.md` le scritture avvengono SOLO dentro
   `<!-- auto:begin key=… -->` / `<!-- auto:end key=… -->`
   (`dmcore.regions`, che garantisce byte-identici i contenuti esterni);
   i file creati ex-novo dagli script (session log del wizard, artefatti
   in `campaign/next/`) non necessitano marker.
4. **Reversibilità**: `state.md` deve essere pulito in git prima
   dell'applicazione e viene committato subito dopo — l'undo è sempre
   `git revert`.

Regioni gestite in v1: `march-clock` (§2.1) e `changelog` (§8,
append-only). Tutto il resto di `state.md` (prosa, tabelle villain, §1
party) resta proposta a video da applicare a mano.

## Conseguenze

- Il canone resta curato dal DM (conferma per blocco); la prosa è
  strutturalmente intoccabile (contratto verificato dai test
  `scripts/tests/test_regions.py` / `test_state_apply.py`).
- `state_sync.py` resta utilizzabile in modalità solo-report; il flusso
  manuale del Playbook §4 continua a funzionare identico.
- La docstring storica di `dm.py` è aggiornata: la regola «mai scrivere»
  è sostituita da questo ADR.
- Costo: `state.md` contiene marker HTML-comment (invisibili nel
  rendering); ogni nuova regione gestita va aggiunta a `--migrate`, ai
  test e a questo elenco.
