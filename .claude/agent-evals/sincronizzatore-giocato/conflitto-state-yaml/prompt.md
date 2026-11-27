---
tags:
- rumblingstone
- agente
- sincronizzatore-giocato
max_turns: 20
timeout_seconds: 900
allowed_tools:
- Read
- Glob
- Grep
- Bash
---

Facendo git merge origin/main sul ramo campaign-group-rumblingstone ho un conflitto in campaign/state.yaml: il ramo ha cambiato i PF e le risorse dei PG dopo la sessione 5, main ha cambiato altre righe dello stesso file. Risolvo con git checkout --ours sul file intero? E che cosa lancio dopo il merge?

Non modificare file del repo: rispondi nel messaggio finale. Chiudi con la riga «Documentazione da aggiornare:».
