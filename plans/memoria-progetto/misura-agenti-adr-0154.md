---
name: misura-agenti-adr-0154
description: ADR-0154 (#531, bozza 27/11): set d'oro dell'instradamento degli agenti, metriche scikit-learn, cancello in testing; PR 2-4 da fare
metadata:
  type: project
  modified: 2026-11-27T06:43:02.628Z
---

Thread «Misurare e migliorare agenti, skill e automatismi» (27/11/2026). PR #531 in bozza, ramo claude/project-thread-2yp4ga, voce MS-0236 (rinumerare se #527 entra prima). ADR-0154 non prenotato su main.

- Set d'oro `plans/instradamento/agenti-oro.json`: 29 messaggi veri, kappa 0,78 con etichettatura cieca, split dev <19/11 (11) / test ≥19/11 (18). Card a Jfs per confermare le etichette (D1).
- Misura su main: hook 4/18 sul test, baseline costante «sviluppatore» 6/18; macro-F1 107/1155 contro 0,0625. ADR-0146 diceva 23/33 su frasi in parte di taratura.
- Cause: omonimi nei trigger («coordinate» pesca «coordinato con il padre», «hook», «master», «caso», «corredo», «png»); l'hook scatta su avvisi del coordinatore e resoconti dei sottoagenti; registri `.claude/.uso-*.jsonl` locali al container.
- scikit-learn ==1.9.1 in testing (scelta di Jfs del 27/11, vedi [[feedback-standard-di-fatto]]); l'hook non la importa. Keras/TensorFlow no con 29 casi; PR 4 neurale (PyTorch + sentence-transformers) solo con ≥200 casi.
- Prossimi: PR 2 omonimi (tarare sul dev), PR 3 TF-IDF+NB/LogReg, set etichettati per vincolo_skill, rilevatori del cricchetto, push, pass^k delle prove degli agenti. Audit in /mnt/project-files/agenti-eval-2026-11-27/AUDIT.md.

**Why:** Jfs vuole F1/precision/accuracy con metodi standard su ogni componente che decide.
**How to apply:** ogni tecnica nuova si misura con `instradamento_agenti.py --eval` contro il tetto del set d'oro; vedi [[vincolo-skill-prosa]].
