#!/usr/bin/env bash
# scripts/sync-skills.sh — OPTIMIZED VERSION
# Syncs canonical skills/ directory to all agent-specific paths inside the repo.
# Replaces blind cp -R with format-aware sync: each agent gets its optimal format.
#
# Usage:
#   ./scripts/sync-skills.sh [--dry-run] [--no-build]
#
# What changed vs. original:
#   OLD: cp -R canonical → every agent path (identical copies, full token load)
#   NEW: build-skills.sh → per-format packages → agent-specific paths

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="dnd-35-rules"
DRY_RUN=false
NO_BUILD=false

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }

for arg in "$@"; do
  case $arg in
    --dry-run)  DRY_RUN=true ;;
    --no-build) NO_BUILD=true ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

$DRY_RUN && warn "DRY RUN mode"

# ── In-repo agent paths (committed to git) ───────────────────────────────────
# Format: agent_id:repo_relative_path:preferred_format
declare -a AGENT_ENTRIES=(
  "claude:.claude/skills/${SKILL_NAME}:compact.md"
  "codex:.agents/skills/${SKILL_NAME}:machine.json"
  "cursor:.cursor/skills/${SKILL_NAME}:machine.json"
  "windsurf:.windsurf/skills/${SKILL_NAME}:compact.md"
  "copilot:.github/copilot/skills/${SKILL_NAME}:compact.md"
  "chatgpt:.chatgpt/skills/${SKILL_NAME}:compact.md"
  "gemini:.gemini/skills/${SKILL_NAME}:structured.yaml"
)

BUILD_DIR="${REPO_ROOT}/build/${SKILL_NAME}"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  RumblingStone — Format-Aware Skill Sync"
echo "══════════════════════════════════════════════════════"

# ── Step 1: Run build pipeline if not skipped ────────────────────────────────
if ! $NO_BUILD; then
  info "Running build pipeline first..."
  BUILD_FLAGS=""
  $DRY_RUN && BUILD_FLAGS="--dry-run"

  if ! $DRY_RUN; then
    bash "${SCRIPT_DIR}/build-skills.sh" --no-deploy ${BUILD_FLAGS} || {
      warn "Build failed — sync aborted. Fix errors above."
      exit 1
    }
  else
    warn "[dry] Would run: build-skills.sh --no-deploy"
  fi
else
  info "Skipping build (--no-build). Using existing ${BUILD_DIR}/packages/"
fi

# ── Step 2: Sync per-format packages to in-repo agent paths ─────────────────
echo ""
info "Syncing agent-specific packages to in-repo paths..."

for entry in "${AGENT_ENTRIES[@]}"; do
  IFS=':' read -r agent rel_path fmt <<< "${entry}"
  dest="${REPO_ROOT}/${rel_path}"
  pkg="${BUILD_DIR}/packages/${agent}"

  if $DRY_RUN; then
    warn "  [dry] ${agent} (${fmt}) → ${rel_path}"
    continue
  fi

  if [[ ! -d "${pkg}" ]]; then
    warn "  ${agent}: package not found at ${pkg} — skipped"
    continue
  fi

  mkdir -p "$(dirname "${dest}")"
  rm -rf "${dest}"
  cp -R "${pkg}" "${dest}"
  info "  ${agent} (${fmt}) → ${rel_path}"
done

echo ""
if ! $DRY_RUN; then
  info "Sync complete. Commit the changes:"
  echo ""
  echo "  git add .claude .agents .cursor .windsurf .github .chatgpt .gemini"
  echo "  git commit -m 'chore: sync optimized skill formats for all agents'"
  echo ""
  info "Token savings vs. raw copy: see build/${SKILL_NAME}/formats/_compression_summary.json"
fi
