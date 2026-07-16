---
name: rumblingstone-plans
description: >
  Plan-archive discipline for the RumblingStone repo — where work plans and
  research docs live and how their completion is tracked. Use WHENEVER
  creating, updating, completing, or merging a piano/lotto/ricerca/iniziativa,
  opening or closing a PR that implements one, or when asked "dov'è il piano",
  "aggiorna il changelog", "traccia le modifiche", "archivio piani",
  "che stato ha il piano X". Trigger on: "piano", "lotto", "PIANO-*",
  "RICERCA-*", "plans/", "INDEX", "CHANGELOG", "ADR", "chiudi/completa il
  piano", "merge della PR". Enforces the repo's golden rule: every closed
  lotto updates plan checklist + plans/INDEX.md + plans/CHANGELOG.md in the
  SAME commit.
---

# RumblingStone — Archivio Piani (disciplina di tracciatura)

Ogni lavoro strutturato del repo (revisioni, infrastruttura, ricerche) è
tracciato in **`plans/`**. Senza questa disciplina le modifiche restano
sparse nelle PR mergiate e la storia si frammenta. Fonte delle regole:
`plans/PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md` (Lotto K-A) e l'header di
`plans/INDEX.md`.

## Dove vivono le cose

| Cosa | Dove |
|---|---|
| Piani di lavoro (con lotti/checklist) | `plans/PIANO-<NOME>.md` |
| Ricerche/valutazioni (input di futuri piani) | `plans/RICERCA-<NOME>.md` |
| Decisioni architetturali (il "perché") | `plans/adr/` |
| Vista d'insieme: stato, %, lotti rimanenti, gate | `plans/INDEX.md` |
| Storia: una riga per lotto chiuso | `plans/CHANGELOG.md` |

## ⚖️ Regola d'oro (obbligatoria, non opzionale)

**Chi chiude un lotto/piano/iniziativa aggiorna — NELLO STESSO COMMIT:**

1. la **checklist del piano** (o la nota "STATO ATTUAZIONE" di una ricerca);
2. la **riga del piano in `plans/INDEX.md`** (stato, %, lotti rimanenti,
   gate) e la sua sezione "Prossimi passaggi";
3. **una riga in `plans/CHANGELOG.md`**:
   `| data | piano | lotto | riferimento (PR #N / commit) | esito |`.

## ✅ Rituale di chiusura PR (checklist per l'agente)

Prima di aprire (o dichiarare pronta) una PR che completa lavoro pianificato:

- [ ] Il documento del lavoro esiste in `plans/` (PIANO o RICERCA)? Se il
      lavoro è nato "spontaneo" da una richiesta, creare almeno la voce di
      tracciatura (non serve un piano formale per tutto — serve la riga).
- [ ] `plans/INDEX.md`: riga di stato aggiornata + "Prossimi passaggi"
      (anche solo ⬜ opzionali/gated).
- [ ] `plans/CHANGELOG.md`: riga aggiunta con riferimento alla PR.
- [ ] Se la PR introduce tooling/script: `scripts/README-automation.md`
      (tool map) aggiornato.
- [ ] Se la PR introduce/tocca una skill: `./scripts/build-skills.sh
      --no-deploy` e `python3 scripts/validate_skills.py` verdi.
- [ ] Nuova convenzione o scelta strutturale? → ADR in `plans/adr/`.

Se una PR è già stata mergiata senza tracciatura (com'è successo alla
PR #40 prima di questa skill): recuperare subito con un commit dedicato
`docs(plans): tracciatura PR #N` — mai lasciare buchi nella storia.

## Note

- Le voci di INDEX/CHANGELOG citano **fatti verificabili** (PR, commit,
  file), mai intenzioni. Gli esiti parziali si dichiarano (🟡 + cosa manca
  + gate), non si arrotondano a ✅.
- I "Prossimi passaggi" di INDEX si lasciano ⬜ finché il tavolo/DM non
  decide: il vuoto dichiarato è informazione, il vuoto implicito no.
