---
name: weekly-audit-routine-scope
description: Weekly Monday audit routine on gsamuele78/RumblingStone covers PRs, open plans, changelogs, then starts one plan-closure thread at a time
metadata:
  type: project
---

Routine "Audit settimanale PR e decisioni" (trig_011DUKCyBhX5WJyNwK2XNm4h, Mondays 06:47 UTC) audits gsamuele78/RumblingStone read-only.
Since 2026-10-10 it covers: open PRs (stale >30d, red CI), open plans (plans/INDEX.md, plans/REGISTRO-LOTTI.md, plans/PIANO-*.md), changelogs (plans/CHANGELOG.md, campaign/state-changelog.md, scripts/check_plans_discipline.py), open DM decisions.
Since 2026-10-12 (Jfs request): it ranks open plans by urgency (blockers > red CI/canon issues > closest to done > stalest) and asks the coordinator to start ONE "Chiusura piano <NOME>" thread; next one only after the previous is resolved. Closure threads follow ADR-0075 and ADR-0009 (plan, INDEX, REGISTRO-LOTTI, CHANGELOG in the same commit), open a draft PR, ask Jfs for DM decisions.

**Why:** the user wants plans closed progressively, most urgent first, without parallel sprawl.
**How to apply:** keep audit read-only; only closure threads write, via draft PRs.

2026-10-23 Jfs: i merge li fa solo il thread padre «Audit settimanale PR e decisioni» (cmsg_019sykApdKEBBe8D8NJyiFEGUzDsB4hQ7TncCjVE1i2jDW), che tiene la lista delle PR aperte e incomplete in /mnt/project-files/pr-aperte/LISTA-PR.md. I thread figli sviluppano, testano e verificano. Quando la loro PR è verde e i test sono finiti, avvisano con test e risultati i thread interessati e il padre, e lasciano a lui il merge.

Dal 2026-11-08 (allineamento del coordinatore, /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md) l'audit controlla anche: (1) ogni scelta nuova parte dallo standard di fatto della comunità, una soluzione nostra solo se una misura lo boccia, con il motivo nell'ADR; (2) le skill sono in bundle con tutti i requisiti (versione, sha256 e licenza fissati, niente pip a runtime), come iemod-fetch; (3) i prompt seguono ADR-0114 (GUIDA-SCHEDE-PROMPT, almeno 3 casi in evals/ per skill, prove_skill.py in CI); (4) avanzamento della roadmap del motore (passo 0: #338 e #340; poi F1-F6) e decisioni aperte di ADR-0111/0112/0113. Il merge delle PR del motore lo fa il thread padre di quel filone.
Calendario proposte dell'audit (nota del 2026-11-08): dal 2026-11-09 la promozione a stable dei canali di ADR-0099; dal 2026-11-22 il cancello check_schede bloccante (ADR-0114). La promozione di mise non c'è più: ADR-0116 (#342) l'ha tolta, typst e pdfimpose arrivano da requirements.txt e li aggiorna Dependabot.
Dal 2026-11-08 roadmap unica del progetto: /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md, tenuta dal thread «Rendere i regolamenti plugin attivabili» (cmsg_019sykApdKEBBe8D8NJyiFEGBED6JNagtf8DRLZd7a8aM2). L'audit non ne tiene una seconda: manda le sue voci a quel thread.
