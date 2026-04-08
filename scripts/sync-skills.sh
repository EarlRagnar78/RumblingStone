#!/usr/bin/env bash
# scripts/sync-skills.sh
# Syncs the canonical skills/ directory to all agent-specific paths inside the repo.
# Run after editing skills/dnd-35-rules/ to propagate changes.
# Commit the result — all agent paths stay up to date in git.
#
# Usage: ./scripts/sync-skills.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="${REPO_ROOT}/skills/dnd-35-rules"
SKILL_NAME="dnd-35-rules"
DRY_RUN=false

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }

[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true && warn "DRY RUN mode"

# In-repo agent paths (relative to repo root, committed to git)
AGENT_DIRS=(
  ".claude/skills/${SKILL_NAME}"
  ".agents/skills/${SKILL_NAME}"
  ".cursor/skills/${SKILL_NAME}"
  ".windsurf/skills/${SKILL_NAME}"
  ".github/copilot/skills/${SKILL_NAME}"
)

echo ""
echo "══════════════════════════════════════════════════════"
echo "  RumblingStone — Skill Sync (canonical → agent paths)"
echo "══════════════════════════════════════════════════════"
echo "  Canonical source: ${CANONICAL}"
echo ""

for rel in "${AGENT_DIRS[@]}"; do
  dest="${REPO_ROOT}/${rel}"
  if $DRY_RUN; then
    warn "  [dry] Would sync → ${rel}"
    continue
  fi
  mkdir -p "$dest"
  rm -rf "${dest}"
  cp -R "${CANONICAL}" "${dest}"
  info "  Synced → ${rel}"
done

echo ""
info "Sync complete. Stage and commit the changes:"
echo "  git add .claude .agents .cursor .windsurf .github"
echo "  git commit -m 'chore: sync dnd-35-rules skill to agent paths'"
echo ""
