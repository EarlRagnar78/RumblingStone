---
name: standard-prompt-a-schede
description: Thread 2026-11-08 standard a schede per tutti i prompt (skill, brief, prove): misura del repo, fonti, proposta ADR-0112, card a Jfs
metadata:
  type: project
  modified: 2026-11-08T08:10:05.453Z
---

Thread «Fissare lo standard dei prompt a schede» (2026-11-08), richiesta di Jfs: standard del repo per tutti i prompt, in schede, contro le allucinazioni.

Proposta in /mnt/project-files/standard-prompt-2026-11-08/PROPOSTA-STANDARD-PROMPT.md, misura con misura_prompt.py accanto (solo lettura).

Misura 2026-11-08: 18 skill, tutte <500 righe e con Cancelli; Vincoli sui fatti 10/18; formato d'uscita 4/18; «prima di consegnare» 4/18; prove con trappola solo 10 skill × 3 (consegne.json della A/B ADR-0109, nessuno script nel repo); 41 date/storie nei corpi; AGENTS.md 481 righe ~32 KB; brief a subagenti scritti a mano, nessun modello.

Fonti: Anthropic reduce-hallucinations e skill best-practices (≥3 prove per skill, niente info datate), ETH «Evaluating AGENTS.md» arXiv 2602.11988 (file di contesto: nessun guadagno, +20% costo), IFScale arXiv 2507.11538 (più istruzioni = meno rispettate). Firecrawl senza crediti il 2026-11-08 mattina: usato WebSearch + curl (platform.claude.com *.md raggiungibile, agentskills.io 403).

Proposta: ADR-0114 (0112 = motore agnostico dei regolamenti plugin, 0113 = thread typst/pdfcpu): scheda skill a 9 sezioni, MODELLO-BRIEF, prove.json per skill + script A/B, cancello in validate_skills non bloccante 2 settimane; adozione solo se la A/B non peggiora gli inventati ([[decisioni-superate-regressione]]). Card a Jfs su perimetro, AGENTS.md, prove, lingua. Vedi [[standard-marcature-inferred]], [[sistemi-di-gioco-plugin]].

2026-11-08 avanzamento: Jfs (via coordinatore) regola standard de facto → card 1 (skill+brief) e 2 (AGENTS.md snellito con misura) chiuse con la consigliata; aperte card A/B (54 casi ≈108 esecuzioni) e lingua descrizioni. Ramo claude/project-thread-v0no2m, lotto 1: GUIDA-SCHEDE-PROMPT (§0 regola di partenza di progetto: prima lo standard di fatto, nostra solo se la misura lo boccia, motivo nell'ADR), ADR-0114 proposta, 54 casi in skills/*/evals/ nel formato claude plugin eval (prompt.md, case.yaml schema 1.1, graders/), scripts/prove_skill.py controlla/prepara/esito, avvisi check_schede in validate_skills, step CI. Lotto 2 = 18 skill riordinate + AGENTS.md, con A/B. pytest locale: serve venv con requirements-dev (il pytest di uv non ha le dipendenze).

PR #339 unita su main il 2026-11-08 (d0cc674, squash, merge autorizzato da Jfs). ADR-0114 non prenotata (già su main). Restano card A/B e lingua; poi lotto 2.

2026-11-08 lotto 2: PR #343 (bozza). 18 skill nella scheda, AGENTS.md 485→367. A/B alla cieca 54 consegne/108 esecuzioni/18 giudici: inventati 32→30, marche complete 74→95, per caso 4/4/46 (p 0,64): non peggiora, miglioramento non dimostrato. dnd-35-srd 0→3 rimisurata 2×2: 3 a 3 (rumore). ADR-0114 accettata. Risposte in /mnt/project-files/standard-prompt-2026-11-08/ab-lotto2/. Esecutori su copie del repo senza evals/ (git archive). Limite d'uso 5 h colpito a metà workflow: si riprende con resumeFromRunId.
PR #343 unita su main il 2026-11-08. Prossimo: l'audit settimanale propone check_schede bloccante dal 2026-11-22.
