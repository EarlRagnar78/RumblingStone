---
name: pr-chiusura-e-merge
description: Regola di Jfs (2026-10-23) su chi fa il merge delle PR e come si chiude un filone testato: i thread figli avvisano, il thread padre unisce
metadata:
  type: feedback
  modified: 2026-10-23T13:00:30.731Z
---

Quando una PR è verde e le prove sono concluse, il thread che la porta: (1) manda risultati e test a tutti i thread interessati (send_message), (2) aggiorna le parti rilevanti nei loro file/piani, (3) passa il merge al thread padre «Audit settimanale PR e decisioni» (cmsg_019sykApdKEBBe8D8NJyiFEGUzDsB4hQ7TncCjVE1i2jDW), che tiene la lista di tutte le PR aperte e incomplete in /mnt/project-files/pr-aperte/LISTA-PR.md. I thread figli fanno test, sviluppo, verifiche e aggiornamenti; non uniscono da soli.

**Why:** Jfs vuole un solo posto dove le PR si aggiornano e si uniscono, così tutto resta allineato.
**How to apply:** non chiamare merge_pull_request da un thread figlio; a PR pronta, avvisa i thread interessati e manda al padre il numero della PR, lo stato della CI e cosa va unito prima/dopo (es. #264 prima della #270). Vedi [[weekly-audit-routine-scope]].
