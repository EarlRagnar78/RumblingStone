---
name: claude-config-nei-thread
description: Nei thread Claude parte in /home/user, non nel repo: la config Claude del repo arriva solo via scripts/claude-progetto.sh (ADR-0140)
metadata:
  type: project
  modified: 2026-11-19T06:28:25.654Z
---

Nei thread del progetto Claude Code parte in `/home/user` (la cartella che contiene il clone). Senza altro, AGENTS.md, l'hook SessionStart, gli skillOverrides e il server `rumblingstone-tools` del repo NON arrivano (misurato il 19/11/2026: niente `.claude/.skills-sync-status`, dnd-35-rules legacy presente, rumblingstone-tools assente). Contesto iniziale di un thread misurato: 131.128 token, di cui circa 113.000 caratteri da plugin e connettori dell'account estranei al progetto.

[riga riservata · sha256:e5414bb4]

Misure del 19/11 da tenere: le skill del repo all'avvio sono le sole copie utente (~5,3k token); le `RumblingStone:*` annidate arrivano dopo il primo file letto, quasi tutte solo nome (~0,7k): la doppia copia NON vale 5k, niente da correggere. Il plugin engineering porta 7 server MCP che non si collegano (proxy) e datadog senza login: zero token, solo rumore. Il clone dei thread può essere shallow (test di fase1 rosso solo lì). Hook pre-push in arrivo con ADR-0143 (gate_locale --pre-push, ~45 s, via pre-commit con hook locali): nei thread lo installa session-start.sh.

**Why:** una regola scritta in AGENTS.md o in `.claude/settings.json` non vale nei thread finché questa catena non funziona.
**How to apply:** misurare il contesto e i tool di un thread con `claude -p --output-format stream-json --verbose` dalla cartella di prova (evento init e `usage` del result). Plugin da spegnere solo per il progetto: `enabledPlugins: {"x@synced": false}` nel settings del repo. Vedi [[piattaforma-di-sviluppo]] [[memoria-storica-repo]].
