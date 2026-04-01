#!/usr/bin/env bash
# scripts/deploy-skills.sh
# Installs/updates D&D 3.5 skills to user-level directories for all supported agents.
# Run once per machine after cloning. Re-run to update after changes.
#
# Usage: ./scripts/deploy-skills.sh [--dry-run] [--force]
#
# Supports: Claude Code, OpenAI Codex, Cursor, Windsurf, GitHub Copilot (VS Code)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SRC="${REPO_ROOT}/skills/dnd-35-rules"
SKILL_NAME="dnd-35-rules"
DRY_RUN=false
FORCE=false

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()    { echo -e "${GREEN}[+]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
error()   { echo -e "${RED}[E]${NC} $*" >&2; }

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --force)   FORCE=true ;;
    *) error "Unknown argument: $arg"; exit 1 ;;
  esac
done

$DRY_RUN && warn "DRY RUN mode — no files will be written"

# ── Agent user-level skill directories ─────────────────────────────────────
declare -A AGENT_PATHS=(
  ["claude"]="${HOME}/.claude/skills/${SKILL_NAME}"
  ["codex"]="${HOME}/.codex/skills/${SKILL_NAME}"
  ["cursor"]="${HOME}/.cursor/skills/${SKILL_NAME}"
  ["windsurf"]="${HOME}/.windsurf/skills/${SKILL_NAME}"
  ["copilot_vscode"]="${HOME}/.vscode/extensions/github.copilot-skills/${SKILL_NAME}"
)

install_skill() {
  local agent="$1"
  local dest="$2"

  if [[ ! -d "$(dirname "$dest")" ]]; then
    if $DRY_RUN; then
      warn "  [dry] Would create: $dest"
      return
    fi
    mkdir -p "$(dirname "$dest")"
  fi

  if [[ -d "$dest" ]] && ! $FORCE; then
    warn "  ${agent}: already installed at ${dest} (use --force to overwrite)"
    return
  fi

  if $DRY_RUN; then
    info "  [dry] Would install ${agent} → ${dest}"
    return
  fi

  if [[ -L "$dest" ]]; then
    rm "$dest"
  fi

  # Use symlink if on same filesystem, else rsync copy
  if [[ "$(stat -c %d "$SKILL_SRC" 2>/dev/null)" == "$(stat -c %d "$(dirname "$dest")" 2>/dev/null)" ]]; then
    ln -sfn "$SKILL_SRC" "$dest"
    info "  ${agent}: symlinked → ${dest}"
  else
    rsync -a --delete "${SKILL_SRC}/" "${dest}/"
    info "  ${agent}: copied → ${dest}"
  fi
}

echo ""
echo "══════════════════════════════════════════════════════"
echo "  RumblingStone — D&D 3.5 Skills Deployer"
echo "══════════════════════════════════════════════════════"
echo "  Source: ${SKILL_SRC}"
echo ""

for agent in "${!AGENT_PATHS[@]}"; do
  dest="${AGENT_PATHS[$agent]}"
  install_skill "$agent" "$dest"
done

echo ""
info "Done. Restart your AI agent/IDE to pick up the new skill."
echo ""
echo "  Verify in Claude Code:  /skills"
echo "  Verify in Codex CLI:    codex --list-skills"
echo "  Verify in Cursor:       Ctrl+Shift+P → 'Skills: List'"
echo ""
