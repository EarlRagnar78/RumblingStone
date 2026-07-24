---
name: rumblingstone-automation
description: >
  DM automation for the RumblingStone repo — the single CLI `scripts/dm.py`
  and the session-state pipeline on group branches (ADR-0007). Use WHENEVER
  closing or preparing a session, updating campaign/state.md, generating
  recaps (group or per-PG), briefs, teasers, handouts, Homebrewery output,
  or running/choosing any script in scripts/. Trigger on: "dm.py",
  "fine sessione", "chiudi la sessione", "session end", "wizard",
  "prossima sessione", "brief", "teaser", "recap", "recap per-PG",
  "state.md", "March Clock", "XP ledger", "branch di gruppo",
  "campaign-group", "Homebrewery", "hype", "handout", "dossier",
  "doctor", "doctor --ci", "prep incontro", "suggest_encounter".
---

# RumblingStone — Automazione DM (`dm.py` e pipeline di sessione)

Tutta l'automazione DM passa da **un solo entrypoint**:
`python3 scripts/dm.py <sottocomando>` (solo orchestrazione, ADR-0002).
Gli script sottostanti restano usabili direttamente e usano solo stdlib.

**Fonti di verità (non duplicare, puntare):**

| Cosa | Dove |
|---|---|
| Tool map completa (tutti gli script: scopo, parametri, I/O) | `scripts/README-automation.md` |
| Guida operativa per nuovi DM (~15 min) | `campaign/DM-QUICKSTART-NUOVI-DM.md` |
| Workflow manuale pre/durante/post sessione | `campaign/DM-CAMPAIGN-PLAYBOOK.md` (§2, §4, §7) |
| Perché il CLI è orchestrazione-only | `plans/adr/ADR-0002-cli-unica-dm-orchestratore.md` |
| Perché i layout `.hb.md` sono generati, mai editati | `plans/adr/ADR-0003-markdown-master-layout-generati.md` |
| Quando gli script possono scrivere canone | `plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md` |
| Contratti verificati (31 test in CI) | `scripts/tests/` |

## ⚖️ Regole non negoziabili (ADR-0007, triplo vincolo)

Gli script scrivono canone (`campaign/state.md`, `campaign/sessions/*`)
SOLO se valgono **tutte insieme**:

1. **Branch**: mai su `main`/`master` — il canone vivo di un gruppo sta su
   `campaign-group-<nome>` (guardia `campaign_branch.py`; il branch non si
   mergia mai in `main`).
2. **Conferma**: il DM vede e conferma il **diff esatto, blocco per
   blocco** (`--yes` esiste solo per test/CI).
3. **Regioni marcate**: in `state.md` si scrive solo dentro
   `<!-- auto:begin key=… -->` / `<!-- auto:end key=… -->` (v1: `march-clock`
   §2.1 e `changelog` §8, append-only). Tutto il resto — prosa, tabelle
   villain, §1 party — resta **proposta a video** da applicare a mano.
4. **Reversibilità**: `state.md` pulito in git prima dell'apply, commit
   dedicato subito dopo; l'undo è sempre `git revert`.

Un agente che "aggiorna state.md" a mano fuori dalle regioni marcate, o su
`main`, sta violando l'ADR: fermarsi e proporre il flusso corretto.

## Flusso di sessione (`dm.py session`)

| Comando | Cosa fa | Script sottostanti |
|---|---|---|
| `session end` | wizard guidato fine-sessione (senza `--session`): log canonico in `campaign/sessions/`, blocchi `## Split — <PG> @ <luogo>` se il party si divide, poi ledger XP → diff `state.md` (solo regioni auto) → conferma → commit | `session_wizard` + `update_xp` + `state_apply` |
| `session next [--hype]` | brief ⚠️SOLO-DM (finestre quest, clock ≤2 tick, hook aperti, `❓ forse già giocato`) + teaser player spoiler-safe in `campaign/next/` | `next_session` |
| `session recap [--pg <PG>]` | recap di gruppo o personale per-PG (visibilità: i blocchi Split li vede solo quel PG; `## DM notes (private)` non esce MAI) | `session_recap` + `hype_homebrew --pg` |
| `session status` / `session branch --group <nome>` | stato branch/guardie · setup branch di gruppo + `campaign/group.yaml` | `campaign_branch` |

Setup una-tantum di un nuovo gruppo: `dm.py session branch --group <nome>`
poi `state_apply.py --migrate --commit` (inserisce i marker `auto:`).

## Altri sottocomandi

- `prep --el N --env <amb>` — proposte incontro+mappa+loot (non scrive nulla).
- `post --session <file>` — flusso manuale legacy (ledger + report-only).
- `recap --hype` · `handout --tipo T --da <file>` · `dossier` (⚠️ solo DM) —
  vesti Homebrewery V3: i `.hb.md` sono **generati**, mai editati a mano.
- `hype setup|start|docker` — Homebrewery self-hosted (ADR-0004).
- `maps render|validate` — per il *contenuto* delle mappe caricare
  `rumblingstone-mapmaking` (questa skill copre solo l'invocazione).
- `skills build|sync` — rebuild dei mirror per-agente (generati, gitignored).
- `doctor [--ci]` — diagnosi ambiente: primo comando se qualcosa non va.

## Confini con le altre skill

- Contenuto/qualità mappe → `rumblingstone-mapmaking`.
- Tracciatura piani/lotti/ADR → `rumblingstone-plans`.
- Cosa scrivere nel recap/brief (stile) → `rumblingstone-narrative-style`;
  questa skill governa solo *come* generarli e *dove* finiscono.
- Verità di campagna (PG, archi, coerenza) → `rumblingstone-campaign`.
