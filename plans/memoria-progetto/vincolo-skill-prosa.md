---
name: vincolo-skill-prosa
description: ADR-0146 (#510): hook che ferma la prosa di gioco senza narrative-style, dodici agenti in tre classi, cricchetto MQM bloccante in CI
metadata:
  type: project
---

PR #510 unita su main il 21/11/2026, merge 14085a370484. ADR-0146 è su main (ultima MS: MS-0221). Hook e agenti valgono solo nei thread partiti dopo, o dopo aver rilanciato claude-progetto.sh. Misura dopo il merge: list_events sui primi 5 thread nuovi (≥150 chiamate); conta skill invocate e letture di skills/ per 100 chiamate (baseline 0/188), chiamate Agent fra i 12 e quota che segue il primo agente suggerito o la riga «Catena:», blocchi di prosa e di push, deroghe.

- Hook PreToolUse `scripts/vincolo_skill.py`: prosa pura (volumi homebrew/volume-*/NN-*.md, handout, recap, appendici) bloccata senza `rumblingstone-narrative-style`; file misti solo se il testo nuovo ha un box; documenti con promemoria. Registro `.claude/.uso-skill.jsonl`, misura con `--riepilogo`.
- Dodici agenti in `.claude/agents/`: Autori (autore-prosa-gioco, autore-master, autore-documenti), Tecnici (sviluppatore, integratore-dm, piattaforma, cartografo, impaginatore, art-director, regolista), Verificatori in sola lettura (lettore-a-freddo, custode-canone). Un agente non ne lancia altri: le catene le guida il thread; ogni resoconto chiude con «Documentazione da aggiornare:» e autore-documenti lavora da lì e dal diff. Mappa e catene per il coordinatore: /mnt/project-files/agenti-2026-11-20/GUIDA-COORDINATORE.md.
- Scelte di Jfs del 20/11: integratore-dm in TDD a piccoli incrementi; le librerie già nel repo sono standard, quelle nuove (standard di fatto della comunità) entrano per i canali ADR-0099; agente piattaforma a parte (card).
- Hook `instradamento_agenti.py`: suggerisce agente e catena dal prompt; se le istruzioni hanno una riga «Catena: a → b», push e PR si fermano finché mancano quelle chiamate Agent e autore-documenti (deroga `--deroga "motivo"`).
- Card del 20/11: l'aggiornamento misurato di agenti, skill e plugin (eval per agente, A/B, canali) va in un ADR e una PR a parte dopo la #510; proposta in /mnt/project-files/agenti-2026-11-20/PROPOSTA-AGGIORNARE-AGENTI-SKILL-PLUGIN.md.
- Cricchetto `scripts/cricchetto_prosa.py` bloccante sulle PR: nessuna norma MQM peggiora sui file di gioco cambiati.

**Why:** baseline del 20/11 su 5 thread: zero invocazioni di skill su 188 chiamate. Jfs ha scelto il cricchetto bloccante superando «niente cancelli di prosa nuovi» («la misura da sola non obbliga all'utilizzo»).
**How to apply:** dopo il merge e una settimana di thread, rimisurare con `vincolo_skill.py --riepilogo` contro lo zero. Le prove del repo vanno scritte come unittest.TestCase (test_i_test_girano_in_ci le esige). Vedi [[claude-config-nei-thread]].
- Misura del 27/11 (primi 5 thread dopo #518, 439 chiamate): 12 chiamate ad agenti del repo, «Catena:» seguita 4/4, skill dirette 2 (0,46/100; baseline 0/188), 0 blocchi e 0 deroghe; voce in coda memoria storica. Tre P2 di Codex sulla #510 aperti (virgolette hook, HINT/ECHI in vincolo_skill, contesto PF1e nel cricchetto), passati al thread «Misurare e migliorare agenti, skill e automatismi».
- 25/11: dal 22/11 i thread ignorano /home/user/.claude/settings.json (hook, plugin, MCP non arrivavano; gli agenti sì). Correzione #518 unita il 25/11 (879f0284, MS-0223): claude-progetto.sh scrive anche ~/.claude/settings.json e la voce MCP in ~/.claude.json, costruisce le skill prima dell'avvio; spenti superpowers, agentic-council, ai-mentor, frontend-design, skill-creator. Prova: sessione headless `claude -p ... --output-format stream-json --verbose` in /home/user, legge gli eventi hook_response e init (mcp_servers, skills, plugins). Un plugin nuovo dell'account si accende da solo: rimisurare.
