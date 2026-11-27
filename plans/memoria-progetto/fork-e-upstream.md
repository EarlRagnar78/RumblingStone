---
name: fork-e-upstream
description: Stato del fork gsamuele78 rispetto a EarlRagnar78/RumblingStone e come si allineano (misura 2026-11-02)
metadata:
  type: project
  modified: 2026-11-02T17:49:49.345Z
---

Misura 2026-11-02: gsamuele78:main (2cf8a0d) ed EarlRagnar78:main (c140e6d) hanno alberi identici; il fork è "747 commit indietro" solo per merge (PR #27-#30 lassù) e storia vecchia di EarlRagnar78 senza contenuto. Nessuna PR di allineamento serviva.

PR aperte su EarlRagnar78 al 2026-11-02: #23 Pillow (superata), #31 Debian e #32 convertitori (doppioni di #303/#304 del fork, Dependabot gira su entrambi i repo e ne aprirà ogni settimana). Jfs ha scelto di unire #31/#32 lassù e chiudere #23. Il fork ha unito #303/#304, poi Jfs ha unito la PR #33 fork→EarlRagnar78 (59ff922, 2026-11-03): alberi identici, nessuna PR aperta lassù. ADR in /mnt/project-files/fork-upstream-2026-11-02/.

Come misurare senza accesso API: `git fetch https://github.com/EarlRagnar78/RumblingStone.git main` funziona; PR aperte = `git ls-remote ... 'refs/pull/*/merge'`. L'API GitHub per EarlRagnar78 non è raggiungibile da una sessione che ha già gsamuele78/RumblingStone (add_repo rifiuta due repo con lo stesso nome).

**Why:** Jfs vuole che il fork sia la fonte e che EarlRagnar78 riceva le PR (vedi indice, voce Fork).
**How to apply:** prima di aprire una PR fork→upstream controlla che il fork sia avanti (`git rev-list --count upstream/main..origin/main`); le scritture su EarlRagnar78 le fa Jfs o un thread nato da quel repo.
