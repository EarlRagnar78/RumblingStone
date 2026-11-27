---
name: documentazione-allineata-adr0153
description: ADR-0153 (#530, 27/11): cancello CI documentazione_allineata.py, --attiva per la routine del lunedì, e il difetto della Catena nel messaggio di avvio (isMeta)
metadata:
  type: project
  modified: 2026-11-27T06:30:11.867Z
---

PR #530 unita il 27/11/2026 (merge 5b89093e), ADR-0153, voce MS-0237.

- Difetto trovato: il messaggio di avvio di un thread (con la riga «Catena:» del coordinatore) è una riga `type:"user"` `isMeta: true`; UserPromptSubmit non scatta, quindi dalla #510 alla #530 il blocco di push e PR non fermava i thread nuovi. Con la #530 il cancello legge la catena dalla trascrizione.
- `scripts/documentazione_allineata.py`: `--rispetto-a REF` in CI sulle PR (agente → AGENTS.md, script/workflow → docs/INDEX.md, hook → GUIDA-CONFIGURAZIONE-CLAUDE.md, ADR → validate_docs); `--debito --check` cricchetto (tetto in plans/debito-documentazione.json, 106 il 27/11); `--attiva --json` dice se chiamare autore-documenti.
- Scelta di Jfs (card 27/11): B «attivata in modo smart»: CI a zero token + la routine «Audit settimanale PR e decisioni» (trig_011DUKCyBhX5WJyNwK2XNm4h) lancia `--attiva` e solo se attiva chiede un thread con catena autore-documenti. Costo misurato di un'attivazione grossa: 174.239 token; piccola non misurata.
- Registri `.claude/.uso-*.jsonl` locali al container: nessuna prova storica delle chiamate agli agenti.

**How to apply:** il prompt della routine del lunedì si cambia solo dal thread audit: passo 5 in /mnt/project-files/documentazione-automatica-2026-11-27/PASSO-ROUTINE-LUNEDI.md, girato al coordinatore il 27/11; quando la #528 (ADR-0152) è su main, frase su milestone_pronte.py in .claude/agents/piattaforma.md. Vedi [[vincolo-skill-prosa]] [[documentazione-a-ogni-milestone]].
