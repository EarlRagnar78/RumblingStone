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
BUILD_DIR="${REPO_ROOT}/build"
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

# ── Radici degli specchi nel repo (gitignorate): da scripts/agents.conf,
# la stessa matrice che usa build-skills.sh. Ogni skill diventa <radice>/<skill>/.
# shellcheck source=agents.conf
source "${SCRIPT_DIR}/agents.conf"

# Discover all skills (any skills/* with a SKILL.md)
declare -a SKILL_NAMES=()
for d in "${REPO_ROOT}/skills"/*/; do
  [[ -f "${d}SKILL.md" ]] && SKILL_NAMES+=("$(basename "${d%/}")")
done

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

# Ordinati per nome: un array associativo non ha ordine, e il log deve essere lo stesso ogni volta.
for agent in $(printf '%s\n' "${!AGENT_REPO_ROOTS[@]}" | sort); do
  rel_root="${AGENT_REPO_ROOTS[$agent]}"
  fmt="${AGENT_FORMAT[$agent]}"
  for skill_name in "${SKILL_NAMES[@]}"; do
    dest="${REPO_ROOT}/${rel_root}/${skill_name}"
    pkg="${REPO_ROOT}/build/${skill_name}/packages/${agent}"

    if $DRY_RUN; then
      warn "  [dry] ${agent} (${fmt}) ${skill_name} → ${rel_root}/${skill_name}"
      continue
    fi

    if [[ ! -d "${pkg}" ]]; then
      warn "  ${agent}/${skill_name}: package not found at ${pkg} — skipped"
      continue
    fi

    mkdir -p "$(dirname "${dest}")"
    rm -rf "${dest}"
    cp -R "${pkg}" "${dest}"
    info "  ${agent} (${fmt}) ${skill_name} → ${rel_root}/${skill_name}"
  done
done

echo ""
if ! $DRY_RUN; then
  info "Sync complete (local mirrors only — these are gitignored)."
  info "To deploy to user-level agent dirs: ./scripts/build-skills.sh"
fi
