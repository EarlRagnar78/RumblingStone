---
name: merge-dal-thread-padre
description: Jfs 2026-10-23: i thread figli sviluppano e testano; quando sono verdi avvisano i thread interessati e il merge lo fa il thread padre che tiene la lista delle PR
metadata:
  type: feedback
  modified: 2026-10-23T13:00:04.802Z
---

Jfs, 2026-10-23 (thread ARC-08): quando una PR è verde e i test sono conclusi, il thread figlio avvisa i thread che il risultato può interessare, con il test e i numeri, così aggiornano le parti loro. Il merge non lo fa il figlio: lo fa il thread padre (coordinatore), che tiene la lista di tutte le PR aperte e di quelle non ancora complete, in un solo posto. I figli fanno test, sviluppo, verifiche e aggiornamenti.

**Why:** tenere tutto allineato in un solo thread e chiudere ogni strada testata una volta sola.

Thread padre: «Audit settimanale PR e decisioni» (cmsg_019sykApdKEBBe8D8NJyiFEGUzDsB4hQ7TncCjVE1i2jDW), lista in /mnt/project-files/pr-aperte/LISTA-PR.md.

**How to apply:** a PR verde, chiedere al coordinatore il merge (send_message al coordinatore con PR, hash, CI, cosa contiene) e mandare ai thread interessati una nota coi risultati. Il sì di Jfs per il merge resta necessario: lo raccoglie il padre. Vedi [[ramo-di-gruppo-campagna]].
