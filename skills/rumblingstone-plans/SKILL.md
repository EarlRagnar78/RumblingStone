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

## 🤖 Enforcement automatico (ADR-0009)

La regola d'oro non è più solo disciplina — `scripts/check_plans_discipline.py`
gira in CI su ogni PR e come hook `pre-push` locale
(`./scripts/install-git-hooks.sh`):

- **Blocca** (rosso in CI, push rifiutato) modifiche a file strutturali
  (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza una
  riga in `plans/CHANGELOG.md` nello stesso range di commit.
- **Promemoria ADR** (warning non bloccante): nuova skill, nuovo script
  top-level o modifica ai workflow CI senza alcun tocco a `plans/adr/` →
  invito esplicito a valutare un ADR. Non bloccante di proposito: «serve
  un ADR?» resta una decisione umana, non di uno script.
- Il contenuto di campagna (`campaign/`, archi `00_`-`09_`, `Bestiario/`,
  `PG/`) è esente: le sessioni giocate non richiedono changelog.
- Bypass locale consapevole: `git push --no-verify` (la CI resta il gate
  finale).

Se una PR è già stata mergiata senza tracciatura (com'è successo alla
PR #40 prima di questa skill): recuperare subito con un commit dedicato
`docs(plans): tracciatura PR #N` — mai lasciare buchi nella storia.

## Note

- Le voci di INDEX/CHANGELOG citano **fatti verificabili** (PR, commit,
  file), mai intenzioni. Gli esiti parziali si dichiarano (🟡 + cosa manca
  + gate), non si arrotondano a ✅.
- I "Prossimi passaggi" di INDEX si lasciano ⬜ finché il tavolo/DM non
  decide: il vuoto dichiarato è informazione, il vuoto implicito no.


## Richieste complesse → piano con routing engine & impegno (regola DM 2026-07-22)

Per OGNI richiesta comprensibilmente complessa (multi-fase, multi-file, più
sessioni di lavoro, o che tocca canone+meccanica+prosa insieme) l'agente
produce PRIMA un piano dettagliato — nel formato `plans/PIANO-<NOME>.md` o
inline se effimero — in cui **ogni fase dichiara**:

1. **Cosa** produce (deliverable + criterio di accettazione);
2. **Engine consigliato** e **livello di impegno**, per ottimizzare il flusso
   e il consumo di token:

| Tipo di fase | Engine | Impegno |
|---|---|---|
| Find/replace, validazioni, rigenerazione cataloghi, lint | **Haiku** (o script deterministico: sempre preferito se esiste) | basso |
| Redazione standard: statblock, tabelle, mappe ASCII, handout | **Sonnet** | medio |
| Consolidamento narrativo, coerenza cross-arc, decisioni di design, audit | **Opus** | alto |
| Ricognizioni larghe del repo (molti file, serve solo la conclusione) | subagent **Explore** | medio |
| Prosa d'autore su scene cardine (solo su richiesta esplicita del DM) | **Fable/Mythos** | alto |

3. **Dieta di contesto** per fase: passare all'engine SOLO i file del lotto
   (mai riletture dell'intero arco — regola anti-spreco dei piani ARC).

**CI/CD**: questa regola NON è un gate bloccante — giudicare la complessità
di una richiesta o la scelta d'engine non è deterministico, e un gate
semantico in CI sarebbe cattiva pratica. Il gate resta ADR-0009 (tracciatura
nel CHANGELOG); la review meccanica dei contenuti è `validate_modules.py`
(token-free). Questa sezione è la disciplina che l'agente applica DA SOLO
quando riceve la richiesta.
