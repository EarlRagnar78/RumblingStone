---
paths:
  - ".claude/**"
  - ".mcp.json"
  - "scripts/mcp_server.py"
  - "scripts/claude-progetto.sh"
  - "scripts/tools.manifest.json"
  - "scripts/regole_claude.py"
---
<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->
## Strumenti esterni: server MCP e skill dei plugin

La configurazione di Claude Code per questo repo sta in `.claude/settings.json`
e `.mcp.json`: sono accesi solo gli strumenti esterni che servono davvero, il
resto è spento o caricato su richiesta.

**Caricati su richiesta, senza chiedere al DM.** I tool MCP sono differiti
(`ENABLE_TOOL_SEARCH`): un agente che ne ha bisogno li carica con `ToolSearch`
e li usa. Le skill generiche (`engineering:*`, `docs:*`, `reflexion:*`,
`anthropic-skills:*`) compaiono solo per nome: si invocano con `Skill` quando
il compito lo chiede, e le skill `rumblingstone-*` hanno sempre la precedenza.

| Server MCP | Quando si usa |
|---|---|
| `rumblingstone-tools` | i tool di `scripts/tools.manifest.json` (quanti sono lo dice `python3 scripts/tools_manifest.py --check`) ([ADR-0030](plans/adr/ADR-0030-server-mcp-sui-tool.md)). Gira in sola lettura: i tool che scrivono canone restano bloccati (ADR-0007) |
| Canva, Fonts | immagini e tipografia (`rumblingstone-art-direction`, `rumblingstone-editoria`) |
| Context7 | documentazione di librerie e di Typst |
| Firecrawl | ricerche di lore e regole sul web |
| Unstructured Transform | conversione da PDF a markdown, in alternativa a `converters/` |
| Hugging Face | modelli e licenze dei pesi per la hero map ([ADR-0019](plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)) |
| draw.io, tldraw | diagrammi |
| Serena | navigazione del codice |

**Spenti in questo progetto**: Gmail, Google Drive, Tavily, arxiv, bioRxiv,
r-btw. Gmail, Google Drive, Channel3, Clipkit, Mobbin, Microsoft Learn, MDN,
Shutterstock, bioRxiv e pg-aiguide sono negati da `permissions.deny` di
`.claude/settings.json`, che toglie i loro tool dal contesto (scelta del DM del
2026-11-19, ADR-0140). Se un compito ne richiede uno, l'agente lo dice al DM,
che lo riaccende con `/mcp` o togliendo la regola. I plugin dell'account che il
repo non ha mai usato sono spenti con `enabledPlugins: false`: restano accesi
`pdf-viewer`, `review` e `tdd`, più i nove di metodo di sviluppo (`sdd`, `sadd`,
`engineering`, `reflexion`, `docs`, `fpf`, `ddd`, `recursive-decomposition`,
`mcp`) riaccesi su scelta del DM (ADR-0140, punto 5). Lo stesso vale per i plugin spenti a livello globale: un agente non
può accenderli da solo.

**File generati e vendorizzati**: `.claudeignore` elenca ciò che l'agente non
deve leggere, ma Claude Code non lo legge da solo: `scripts/claudeignore_deny.py`
lo traduce in regole `Read(...)` di `permissions.deny` (ADR-0142), che valgono
anche per Grep e Glob. Le scelte e come tornare indietro sono in
`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`.

---

