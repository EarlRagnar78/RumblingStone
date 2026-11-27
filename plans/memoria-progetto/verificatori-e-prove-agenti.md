---
name: verificatori-e-prove-agenti
description: ADR-0148 (#512, unita il 26/11): verifica_px bloccante, verifica_rimandi in testing al 04/12, 36 casi fissi per agente con esito «prima» 0,975
metadata:
  type: project
  modified: 2026-11-20T15:23:44.365Z
---

PR #512 unita su main il 2026-11-26 (merge 4d3437b5). ADR-0148 (proposta) non prenotato in adr-prenotati.json: segnarlo alla piega; la #508 usa ADR-0147. Voce MS-0229. In plans/contenuti-nei-rami.json il ramo o55i68 è ancora «in-volo»: va portato a «portato» alla piega.

- `scripts/verifica_px.py`: cancello bloccante (R1 somme, R2 soglie PHB Table 3–2 non SRD, R3 un livello alla volta DMG, R4 livello effettivo da state.yaml con ECL/LA).
- `scripts/verifica_rimandi.py`: «FILE §N»; testing fino al 2026-12-04 (CI continue-on-error, test sul repo saltato fino a quella data). Promuovere a stable dopo, se zero falsi allarmi.
- Casi degli agenti in `.claude/agent-evals/<agente>/<caso>/` (generati da plans/esperimenti/verificatori-2026-11-20/genera_casi.py: si modifica il generatore e si rilancia, non i casi a mano). Esito in `.claude/agent-evals/ESITI.jsonl`.
- Esito «prima» (agenti della #510, CLI 2.1.329): media 0,975, 33/36 pieni; cadute vere in autore-documenti (trattino lungo), autore-prosa-gioco (etichetta pilastri fra parentesi nel box), integratore-dm (TDD non apre con il test).
- Per rieseguire: `git worktree add --detach DIR HEAD`, poi `prove_skill.py esegui --agente A --uscita OUT --cartella-lavoro DIR` (~1 min a caso), poi `registra --agente A --esecuzioni OUT --data … --nota …`.

**Why:** Jfs (20/11) vuole verificatori deterministici invece di un modello che rilegge, e casi fissi per vedere subito se un aggiornamento di agenti/skill peggiora.
**How to apply:** chi tocca un agente, una skill precaricata o i casi registra un esito nuovo; il cricchetto resta in testing finché non si misura quanto oscilla un caso fra due esecuzioni (prossimo passo: due esecuzioni per caso). Vedi [[vincolo-skill-prosa]].
