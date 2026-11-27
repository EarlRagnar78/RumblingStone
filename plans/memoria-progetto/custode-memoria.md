---
name: custode-memoria
description: ADR-0151 (#529, d8005593): specchio a istantanee della memoria, memoria_custode.py verifica/archivia/cerca/redigi, hook di merge bloccante, agente custode-memoria
metadata:
  type: project
  modified: 2026-11-27T08:03:57.543Z
---

#529 unita il 27/11/2026 (merge d8005593), ADR-0151 accettata, voce MS-0238. Scelte di Jfs sulle card del 27/11: copia della memoria redatta nel repo (`plans/memoria-progetto/`, 25 righe riservate) e completa in `/mnt/project-files/memoria-progetto-specchio/` (istantanee, prima del 27/11 06:17 UTC; termini riservati in RISERVATI.txt, mai nel repo); merge bloccante se una riga tolta non è archiviata.

- Nei thread la memoria è la cartella `/tmp/claude/memory/team/silo` (da CLAUDE_COWORK_MEMORY_PATH_OVERRIDE e CLAUDE_MEMORY_STORES): i thread la leggono e scrivono come file. Le scritture del coordinatore le vede solo la verifica successiva.
- Prima di toccare MEMORY.md e prima di un merge: `python3 scripts/memoria_custode.py verifica`; se fallisce `archivia` (coda `memoria-del-progetto-righe-tolte.md`). `cerca parole` risponde da memoria + file storico + coda. `redigi --uscita plans/memoria-progetto` in PR di sola storia.
- Hook: `--hook-merge` blocca (solo righe non archiviate o MEMORY.md > 16 KB; tetto 12 KB solo avviso); `--hook-scrittura` solo avviso (testing, promozione non prima del 12/12 con ≥10 eventi in `.claude/.custode-memoria.jsonl`, `--riepilogo`).
- Buchi: `gh pr merge` da Bash e merge da GitHub non passano dall'hook; hook in timeout lascia passare; confronto per parole.
- Residui: messaggio S-7 di mcp_server.py falso per questo tool (integratore-dm); prove dell'agente con `claude -p` mai girate. Offerta a Jfs (senza risposta al 27/11): far seguire al custode i `[[link]]` fra note e segnalare quelli rotti.

**Why:** il 27/11 il coordinatore ha tolto righe senza archiviare e nessuno strumento poteva vederlo.
**How to apply:** usa `custode-memoria` per domande sulla memoria; dopo un merge bloccato lancia `archivia`, non aggirare l'hook. Vedi [[memoria-storica-repo]].
