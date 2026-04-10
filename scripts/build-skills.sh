#!/usr/bin/env bash
# build-skills.sh — RumblingStone Skill Optimization Pipeline
#
# Pipeline: RAW → NORMALIZED → COMPRESSED → INDEXED → DEPLOYED
#
# Usage:
#   ./build-skills.sh [--dry-run] [--measure] [--skill dnd-35-rules] [--no-deploy]
#
# Produces per-agent format files and a retrieval index for selective loading.
# Token savings target: 50-70% vs raw markdown.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ── Config ──────────────────────────────────────────────────────────────────
SKILL_NAME="${SKILL:-dnd-35-rules}"
SKILL_SRC="${REPO_ROOT}/skills/${SKILL_NAME}"
BUILD_DIR="${REPO_ROOT}/build/${SKILL_NAME}"
INDEX_FILE="${BUILD_DIR}/index.json"
PYTHON="${PYTHON_BIN:-python3}"

DRY_RUN=false
MEASURE=false
NO_DEPLOY=false

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
BOLD='\033[1m'; NC='\033[0m'

log_step() { echo -e "\n${CYAN}${BOLD}▶ $*${NC}"; }
log_ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}  ⚠${NC} $*"; }

for arg in "$@"; do
  case $arg in
    --dry-run)   DRY_RUN=true ;;
    --measure)   MEASURE=true ;;
    --no-deploy) NO_DEPLOY=true ;;
    --skill=*)   SKILL_NAME="${arg#--skill=}" ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

$DRY_RUN && log_warn "DRY RUN — no files written"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║      RumblingStone — Skill Optimization Pipeline            ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Skill:   ${SKILL_NAME}"
echo "║  Source:  ${SKILL_SRC}"
echo "║  Build:   ${BUILD_DIR}"
echo "╚══════════════════════════════════════════════════════════════╝"

# ── Step 1: Validate source ──────────────────────────────────────────────────
log_step "1/5  Validating source skill"

if [[ ! -d "${SKILL_SRC}" ]]; then
  echo "  ERROR: Skill source not found: ${SKILL_SRC}" >&2
  exit 1
fi
if [[ ! -f "${SKILL_SRC}/SKILL.md" ]]; then
  echo "  ERROR: SKILL.md missing from ${SKILL_SRC}" >&2
  exit 1
fi

FILE_COUNT=$(find "${SKILL_SRC}" -name "*.md" | wc -l)
TOTAL_SIZE=$(du -sh "${SKILL_SRC}" 2>/dev/null | cut -f1)
log_ok "Found ${FILE_COUNT} .md files (${TOTAL_SIZE})"

# ── Step 2: Compress ─────────────────────────────────────────────────────────
log_step "2/5  Compressing → compact.md / structured.yaml / machine.json"

MEASURE_FLAG=""
$MEASURE && MEASURE_FLAG="--measure"

if ! $DRY_RUN; then
  $PYTHON "${SCRIPT_DIR}/compress_skills.py" \
    --input "${SKILL_SRC}" \
    --output "${BUILD_DIR}/formats" \
    ${MEASURE_FLAG}
  log_ok "Compression complete → ${BUILD_DIR}/formats/"
else
  log_warn "[dry] Would compress ${SKILL_SRC} → ${BUILD_DIR}/formats/"
fi

# ── Step 3: Build retrieval index ────────────────────────────────────────────
log_step "3/5  Building retrieval index"

if ! $DRY_RUN; then
  $PYTHON "${SCRIPT_DIR}/index_skills.py" \
    --input  "${SKILL_SRC}" \
    --build  "${BUILD_DIR}/formats" \
    --output "${INDEX_FILE}"
  log_ok "Index written → ${INDEX_FILE}"
else
  log_warn "[dry] Would build index → ${INDEX_FILE}"
fi

# ── Step 4: Generate agent-specific deploy packages ──────────────────────────
log_step "4/5  Packaging per-agent distributions"

declare -A AGENT_FORMAT=(
  ["claude"]="compact.md"
  ["gemini"]="structured.yaml"
  ["codex"]="machine.json"
  ["chatgpt"]="compact.md"
  ["cursor"]="machine.json"
  ["windsurf"]="compact.md"
  ["copilot"]="compact.md"
)

declare -A AGENT_INSTALL_PATHS=(
  ["claude"]="${HOME}/.claude/skills/${SKILL_NAME}"
  ["codex"]="${HOME}/.codex/skills/${SKILL_NAME}"
  ["cursor"]="${HOME}/.cursor/skills/${SKILL_NAME}"
  ["windsurf"]="${HOME}/.windsurf/skills/${SKILL_NAME}"
)

for agent in "${!AGENT_FORMAT[@]}"; do
  fmt="${AGENT_FORMAT[$agent]}"
  pkg_dir="${BUILD_DIR}/packages/${agent}"

  if $DRY_RUN; then
    log_warn "[dry] Would package ${agent} (format: ${fmt}) → ${pkg_dir}"
    continue
  fi

  mkdir -p "${pkg_dir}"

  # Copy SKILL.md root (always markdown, it's the entry point)
  cp "${SKILL_SRC}/SKILL.md" "${pkg_dir}/SKILL.md"

  # Copy references in agent-preferred format
  if [[ -d "${SKILL_SRC}/references" ]]; then
    mkdir -p "${pkg_dir}/references"
    for orig_md in "${SKILL_SRC}/references/"*.md; do
      stem="$(basename "${orig_md}" .md)"
      src_file="${BUILD_DIR}/formats/references/${stem}.${fmt}"
      dest_ext="${fmt##*.}"  # md, yaml, or json
      if [[ -f "${src_file}" ]]; then
        cp "${src_file}" "${pkg_dir}/references/${stem}.${dest_ext}"
      else
        # Fallback to compact.md if agent format not available
        fallback="${BUILD_DIR}/formats/references/${stem}.compact.md"
        [[ -f "${fallback}" ]] && cp "${fallback}" "${pkg_dir}/references/${stem}.md"
      fi
    done
  fi

  # Always include the index
  cp "${INDEX_FILE}" "${pkg_dir}/index.json"

  log_ok "${agent} package ready (${fmt}) → ${pkg_dir}"
done

# ── Step 5: Deploy to user-level agent directories ───────────────────────────
log_step "5/5  Deploying to agent directories"

if $NO_DEPLOY; then
  log_warn "Skipping deploy (--no-deploy flag set)"
else
  for agent in "${!AGENT_INSTALL_PATHS[@]}"; do
    dest="${AGENT_INSTALL_PATHS[$agent]}"
    pkg="${BUILD_DIR}/packages/${agent}"

    if [[ ! -d "${pkg}" ]] && ! $DRY_RUN; then
      log_warn "${agent}: package missing, skipping"
      continue
    fi

    if $DRY_RUN; then
      log_warn "[dry] Would deploy ${agent} → ${dest}"
      continue
    fi

    parent_dir="$(dirname "${dest}")"
    [[ ! -d "${parent_dir}" ]] && mkdir -p "${parent_dir}" 2>/dev/null || true

    if [[ -d "${parent_dir}" ]]; then
      rm -rf "${dest}"
      cp -R "${pkg}" "${dest}"
      log_ok "${agent} deployed → ${dest}"
    else
      log_warn "${agent}: target dir not found (${parent_dir}) — skipped"
    fi
  done
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Build complete                                              ║"
echo "╠══════════════════════════════════════════════════════════════╣"

if ! $DRY_RUN; then
  BUILD_SIZE=$(du -sh "${BUILD_DIR}" 2>/dev/null | cut -f1)
  PKG_COUNT=$(find "${BUILD_DIR}/packages" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
  echo "║  Build dir:   ${BUILD_DIR}"
  echo "║  Build size:  ${BUILD_SIZE}"
  echo "║  Packages:    ${PKG_COUNT} agents"
  echo "║  Index:       ${INDEX_FILE}"
fi

echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Next steps:                                                 ║"
echo "║    Measure savings:  ./build-skills.sh --measure            ║"
echo "║    Skip deploy:      ./build-skills.sh --no-deploy          ║"
echo "║    Dry run first:    ./build-skills.sh --dry-run            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
