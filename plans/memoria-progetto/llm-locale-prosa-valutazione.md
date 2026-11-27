---
name: llm-locale-prosa-valutazione
description: LLM locale per la prosa: ADR-0089, PR #234 (pronta, merge passato al thread padre il 2026-10-23), esito del 4B, prossimo il 12B
metadata:
  type: project
---
[riga riservata · sha256:68c8b67f]
[riga riservata · sha256:fdb99225]
2026-10-23: CI verde su 9c2bb3b, PR tolta da bozza, merge passato al thread padre (vedi [[thread-padre-pr]]).
[riga riservata · sha256:6d39a56f]
Dopo la #264: il banco si chiama anche `dm.py prosa banco` e `dm.py prosa voto`; voto_scrittura resta (lo usa il banco). ADR-0101 lo mette nella catena della prosa, fase unstable.
Gotcha: i prompt crescono con le norme su main (89k caratteri al 23/10); il controllo di contesto stima 3,3 caratteri/token, CTX 32768.
Alla ripresa (regole di Jfs, 2026-11-08): standard di fatto della comunità prima di una soluzione nostra; bundle con requisiti fissati e sha256; (ADR-0113 su mise.lock superata da ADR-0116: niente mise, typst e pdfimpose da requirements.txt; roadmap unica in /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md); prompt e skill secondo GUIDA-SCHEDE-PROMPT (ADR-0114). Per il 12B: Ollama resta lo standard di fatto, ripartire dalla roadmap unica.
**Why:** domanda del DM se conviene un LLM locale per la prosa.
**How to apply:** a corsa del 12B arrivata, registrare in plans/scrittura/RISULTATI.md e ADR-0089.
