#!/usr/bin/env bash
# claude-progetto.sh — porta la configurazione Claude del repo nella
# cartella in cui parte Claude Code quando il repo NON è la cartella di
# lavoro (ADR-0140).
#
# Perché: nei thread del progetto su claude.ai Claude parte nella cartella
# che CONTIENE il clone (es. /home/user), non nel repo. Lì non trova
# CLAUDE.md, AGENTS.md, .claude/settings.json né .mcp.json: niente hook,
# niente skillOverrides, niente server rumblingstone-tools.
#
# Cosa scrive in <cartella> (default: la cartella che contiene il repo):
#   CLAUDE.md               corto, rimanda al repo (progressive disclosure)
#   .claude/settings.json   quello del repo, con l'hook a percorso assoluto
#   .mcp.json               rumblingstone-tools a percorso assoluto
#   .claude/agents          collegamento agli agenti del repo (ADR-0146)
# Non sovrascrive file che non ha scritto lui (marcatore in
# .claude/.generato-da-rumblingstone). Non tocca mai il repo stesso.
#
# Uso:  RumblingStone/scripts/claude-progetto.sh [cartella]
# Si lancia dallo script d'avvio dell'ambiente cloud, prima della sessione.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$(cd "${1:-${REPO}/..}" && pwd)"

if [ "${DEST}" = "${REPO}" ]; then
  echo "claude-progetto: la cartella è il repo stesso, non serve nulla"
  exit 0
fi

MARCA="${DEST}/.claude/.generato-da-rumblingstone"
mkdir -p "${DEST}/.claude"

# Un file già presente si riscrive solo se l'abbiamo scritto noi.
scrivibile() {
  [ ! -e "$1" ] || { [ -f "${MARCA}" ] && grep -qxF "$(basename "$1")" "${MARCA}"; }
}

scritti=()
utente=()

if scrivibile "${DEST}/CLAUDE.md"; then
  REL="$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "${REPO}" "${DEST}")"
  cat > "${DEST}/CLAUDE.md" << EOF
<!-- Generato da ${REL}/scripts/claude-progetto.sh (ADR-0140): si corregge lo script, non questo file. -->
# Cartella di lavoro: il repository è in \`${REL}/\`

- Lavora dentro \`${REL}/\`: i comandi del repo partono da lì.
- Le regole di \`${REL}/AGENTS.md\` (instradamento delle skill, regole d'oro) arrivano da sole da \`${REL}/.claude/rules/\` quando apri un file del repo, ognuna sui file a cui serve (ADR-0141): non serve leggere AGENTS.md intero.
- Prima di modificare qualunque file del repo: \`python3 scripts/fase1.py <bersagli>\` (regola G6), anche se le regole non sono ancora arrivate.
- Per riprendere un lavoro: \`${REL}/MEMORIA.md\`. Per la storia di una scelta: \`python3 scripts/memoria_storica.py --tema T\` (dal repo).
- I tool del DM sono nel server MCP \`rumblingstone-tools\` (sola lettura, ADR-0030).
- Prima di scrivere testo, chi lo legge? Un giocatore: skill \`rumblingstone-narrative-style\` e i suoi quattro references obbligatori, o l'agente \`autore-prosa-gioco\`; il repo: \`rumblingstone-prosa-documenti\`; codice: nessuna skill di prosa. Poi si sommano quelle del compito (albero: \`${REL}/skills/ORCHESTRAZIONE.md\`, agenti: \`${REL}/.claude/agents/\`). Un hook ferma la prosa di gioco scritta senza la sua skill (ADR-0146).
- Le skill del repo si ricostruiscono all'avvio; lo stato è in \`${REL}/.claude/.skills-sync-status\`.
EOF
  scritti+=("CLAUDE.md")
else
  echo "claude-progetto: ${DEST}/CLAUDE.md esiste e non è nostro, lo lascio"
fi

if scrivibile "${DEST}/.claude/settings.json"; then
  python3 - "${REPO}" "${DEST}/.claude/settings.json" << 'EOF'
import json, os, shlex, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
cfg = json.loads((repo / ".claude" / "settings.json").read_text(encoding="utf-8"))
for gruppi in cfg.get("hooks", {}).values():
    for gruppo in gruppi:
        for h in gruppo.get("hooks", []):
            if h.get("type") == "command":
                h["command"] = h["command"].replace("$CLAUDE_PROJECT_DIR", shlex.quote(str(repo)))
# Le regole Read ancorate («/x») valgono dalla cartella del progetto: qui il
# progetto è la cartella che contiene il repo, quindi si aggiunge il suo nome
# (ADR-0142). Quelle «**/x» valgono a ogni livello e restano come sono.
rel = os.path.relpath(repo, out.parent.parent)
perm = cfg.get("permissions", {})
perm["deny"] = [r.replace("Read(/", f"Read(/{rel}/", 1) if r.startswith("Read(/") else r
                for r in perm.get("deny", [])]
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
  scritti+=("settings.json")
else
  echo "claude-progetto: ${DEST}/.claude/settings.json esiste e non è nostro, lo lascio"
fi

if scrivibile "${DEST}/.mcp.json"; then
  python3 - "${REPO}" "${DEST}/.mcp.json" << 'EOF'
import json, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
cfg = json.loads((repo / ".mcp.json").read_text(encoding="utf-8"))
for srv in cfg.get("mcpServers", {}).values():
    srv["args"] = [str(repo / a) if (repo / a).is_file() else a for a in srv.get("args", [])]
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
  scritti+=(".mcp.json")
else
  echo "claude-progetto: ${DEST}/.mcp.json esiste e non è nostro, lo lascio"
fi

# Livello utente (ADR-0146, misura del 25/11). Dal 22/11 i thread ignorano il
# .claude/settings.json della cartella di partenza: senza questo blocco gli
# hook non scattano, i plugin spenti restano accesi e rumblingstone-tools non
# parte. Il livello utente invece si legge sempre. Si scrive solo un file
# nostro o assente, e di ~/.claude.json si tocca solo la nostra voce.
CASA_CLAUDE="${HOME}/.claude"
MARCA_UTENTE="${CASA_CLAUDE}/.generato-da-rumblingstone"
mkdir -p "${CASA_CLAUDE}"
if [ ! -e "${CASA_CLAUDE}/settings.json" ] || { [ -f "${MARCA_UTENTE}" ] && grep -qxF settings.json "${MARCA_UTENTE}"; }; then
  python3 - "${REPO}" "${CASA_CLAUDE}/settings.json" << 'EOF'
import json, shlex, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
cfg = json.loads((repo / ".claude" / "settings.json").read_text(encoding="utf-8"))
for gruppi in cfg.get("hooks", {}).values():
    for gruppo in gruppi:
        for h in gruppo.get("hooks", []):
            if h.get("type") == "command":
                h["command"] = h["command"].replace("$CLAUDE_PROJECT_DIR", shlex.quote(str(repo)))
# A livello utente «/x» varrebbe dalla cartella ~/.claude: le regole ancorate
# diventano assolute, «//percorso/del/repo/x».
perm = cfg.get("permissions", {})
perm["deny"] = [r.replace("Read(/", f"Read(/{repo}/", 1)
                if r.startswith("Read(/") and not r.startswith("Read(//") else r
                for r in perm.get("deny", [])]
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
  printf 'settings.json\n' > "${MARCA_UTENTE}"
  utente+=("~/.claude/settings.json")
else
  echo "claude-progetto: ${CASA_CLAUDE}/settings.json esiste e le impostazioni non sono nostre, le lascio"
fi

python3 - "${REPO}" "${HOME}/.claude.json" << 'EOF'
import json, sys
from pathlib import Path
repo, stato = Path(sys.argv[1]), Path(sys.argv[2])
dati = json.loads(stato.read_text(encoding="utf-8")) if stato.is_file() else {}
cfg = json.loads((repo / ".mcp.json").read_text(encoding="utf-8"))
for nome, srv in cfg.get("mcpServers", {}).items():
    srv["args"] = [str(repo / a) if (repo / a).is_file() else a for a in srv.get("args", [])]
    dati.setdefault("mcpServers", {})[nome] = srv
stato.write_text(json.dumps(dati, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
utente+=("~/.claude.json")

# Le skill del repo in ~/.claude/skills prima che parta la sessione: l'hook
# d'avvio le ricostruisce in background, e il primo turno non le vedrebbe.
if [ -z "${RS_SALTA_SKILL:-}" ] && python3 -c "import yaml" 2>/dev/null; then
  if (cd "${REPO}" && ./scripts/build-skills.sh >/tmp/rumblingstone-skill-build.log 2>&1); then
    utente+=("skill")
  else
    echo "claude-progetto: skill non costruite, vedi /tmp/rumblingstone-skill-build.log"
  fi
fi

# Gli agenti del repo (ADR-0146): Claude Code li cerca in <progetto>/.claude/agents,
# quindi qui si mette un collegamento alla cartella del repo, che resta viva.
AGENTI="${DEST}/.claude/agents"
if [ -d "${REPO}/.claude/agents" ]; then
  if [ -L "${AGENTI}" ] || [ ! -e "${AGENTI}" ]; then
    ln -sfn "${REPO}/.claude/agents" "${AGENTI}"
    scritti+=("agents")
  else
    echo "claude-progetto: ${AGENTI} esiste e non è un collegamento nostro, lo lascio"
  fi
fi

if [ "${#scritti[@]}" -gt 0 ]; then
  { [ -f "${MARCA}" ] && cat "${MARCA}"; printf '%s\n' "${scritti[@]}"; } | sort -u > "${MARCA}.tmp"
  mv "${MARCA}.tmp" "${MARCA}"
fi
echo "claude-progetto: scritti in ${DEST}: ${scritti[*]:-nessuno}; a livello utente: ${utente[*]:-nessuno}"
