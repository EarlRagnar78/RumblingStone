#!/usr/bin/env bash
# build-skills.sh — RumblingStone Skill Optimization Pipeline
#
# Pipeline: RAW → COMPRESSED → INDEXED → DEPLOYED
#
# Discovers every skill in skills/* (any directory containing a SKILL.md) and
# builds per-agent packages for each. Replaces the old single-skill loop.
#
# Usage:
#   ./build-skills.sh [--dry-run] [--measure] [--skill <name>] [--no-deploy]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PYTHON="${PYTHON_BIN:-python3}"
SKILL_FILTER="${SKILL:-}"
DRY_RUN=false
MEASURE=false
NO_DEPLOY=false

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
log_step() { echo -e "\n${CYAN}${BOLD}▶ $*${NC}"; }
log_ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}  ⚠${NC} $*"; }

for arg in "$@"; do
  case $arg in
    --dry-run)   DRY_RUN=true ;;
    --measure)   MEASURE=true ;;
    --no-deploy) NO_DEPLOY=true ;;
    --skill=*)   SKILL_FILTER="${arg#--skill=}" ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

$DRY_RUN && log_warn "DRY RUN — no files written"

# ── Discover skills ─────────────────────────────────────────────────────────
declare -a SKILLS=()
for skill_dir in "${REPO_ROOT}/skills"/*/; do
  [[ -f "${skill_dir}SKILL.md" ]] || continue
  name="$(basename "${skill_dir%/}")"
  if [[ -n "${SKILL_FILTER}" && "${name}" != "${SKILL_FILTER}" ]]; then continue; fi
  SKILLS+=("${name}")
done

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "ERROR: no skills found in ${REPO_ROOT}/skills/" >&2
  exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║      RumblingStone — Skill Optimization Pipeline            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "  Skills to build: ${SKILLS[*]}"

# ── Per-agent format preference. Drop entry to skip an agent.
# The legacy index.json is no longer copied into per-agent packages — no
# mainstream agent loader (Claude, Cursor, Windsurf, ChatGPT, Gemini) reads
# it. The index is still produced under build/<skill>/index.json for use by
# scripts and humans. See scripts/README.md for rationale.
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
  ["claude"]="${HOME}/.claude/skills"
  ["codex"]="${HOME}/.codex/skills"
  ["cursor"]="${HOME}/.cursor/skills"
  ["windsurf"]="${HOME}/.windsurf/skills"
)

# Agents that genuinely consume index.json (currently none — leave empty).
# Add an agent name here if/when its loader is documented to read index.json.
declare -A AGENT_INDEX_AWARE=()

# ── Build each skill ────────────────────────────────────────────────────────
for SKILL_NAME in "${SKILLS[@]}"; do
  SKILL_SRC="${REPO_ROOT}/skills/${SKILL_NAME}"
  BUILD_DIR="${REPO_ROOT}/build/${SKILL_NAME}"
  INDEX_FILE="${BUILD_DIR}/index.json"

  echo ""
  echo "── Skill: ${SKILL_NAME} ──"

  log_step "1/4  Validating source"
  if [[ ! -f "${SKILL_SRC}/SKILL.md" ]]; then
    echo "  ERROR: SKILL.md missing from ${SKILL_SRC}" >&2; exit 1
  fi
  FILE_COUNT=$(find "${SKILL_SRC}" -name "*.md" | wc -l)
  TOTAL_SIZE=$(du -sh "${SKILL_SRC}" 2>/dev/null | cut -f1)
  log_ok "Found ${FILE_COUNT} .md files (${TOTAL_SIZE})"

  log_step "2/4  Compressing → compact.md / structured.yaml / machine.json"
  MEASURE_FLAG=""
  $MEASURE && MEASURE_FLAG="--measure"
  if ! $DRY_RUN; then
    $PYTHON "${SCRIPT_DIR}/compress_skills.py" \
      --input "${SKILL_SRC}" --output "${BUILD_DIR}/formats" ${MEASURE_FLAG}
    log_ok "Compression complete → ${BUILD_DIR}/formats/"
  else
    log_warn "[dry] Would compress ${SKILL_SRC}"
  fi

  log_step "3/4  Indexing"
  if ! $DRY_RUN; then
    $PYTHON "${SCRIPT_DIR}/index_skills.py" \
      --input "${SKILL_SRC}" --build "${BUILD_DIR}/formats" --output "${INDEX_FILE}"
    log_ok "Index → ${INDEX_FILE}"
  else
    log_warn "[dry] Would build index"
  fi

  log_step "4/4  Packaging per agent"
  for agent in "${!AGENT_FORMAT[@]}"; do
    fmt="${AGENT_FORMAT[$agent]}"
    pkg_dir="${BUILD_DIR}/packages/${agent}"
    if $DRY_RUN; then
      log_warn "[dry] Would package ${agent} (${fmt}) → ${pkg_dir}"
      continue
    fi

    rm -rf "${pkg_dir}"; mkdir -p "${pkg_dir}/references"
    cp "${SKILL_SRC}/SKILL.md" "${pkg_dir}/SKILL.md"

    if [[ -d "${SKILL_SRC}/references" ]]; then
      for orig_md in "${SKILL_SRC}/references/"*.md; do
        [[ -e "${orig_md}" ]] || continue
        stem="$(basename "${orig_md}" .md)"
        src_file="${BUILD_DIR}/formats/references/${stem}.${fmt}"
        dest_ext="${fmt##*.}"
        if [[ -f "${src_file}" ]]; then
          cp "${src_file}" "${pkg_dir}/references/${stem}.${dest_ext}"
        else
          fallback="${BUILD_DIR}/formats/references/${stem}.compact.md"
          [[ -f "${fallback}" ]] && cp "${fallback}" "${pkg_dir}/references/${stem}.md"
        fi
      done
    fi

    # Only ship index.json to agents whose loader actually reads it.
    if [[ -n "${AGENT_INDEX_AWARE[$agent]:-}" ]]; then
      cp "${INDEX_FILE}" "${pkg_dir}/index.json"
    fi

    log_ok "${agent} package ready (${fmt}) → ${pkg_dir}"
  done

  # Deploy
  if ! $NO_DEPLOY; then
    log_step "Deploying to user-level dirs"
    for agent in "${!AGENT_INSTALL_PATHS[@]}"; do
      pkg="${BUILD_DIR}/packages/${agent}"
      [[ -d "${pkg}" ]] || { log_warn "${agent}: package missing"; continue; }
      $DRY_RUN && { log_warn "[dry] Would deploy ${agent}"; continue; }
      install_root="${AGENT_INSTALL_PATHS[$agent]}"
      mkdir -p "${install_root}" 2>/dev/null || true
      if [[ -d "${install_root}" ]]; then
        rm -rf "${install_root}/${SKILL_NAME}"
        cp -R "${pkg}" "${install_root}/${SKILL_NAME}"
        log_ok "${agent} deployed → ${install_root}/${SKILL_NAME}"
      else
        log_warn "${agent}: install root not writable, skipped"
      fi
    done
  else
    log_warn "Skipping deploy (--no-deploy)"
  fi
done

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Build complete                                              ║"
if ! $DRY_RUN; then
  BUILD_SIZE=$(du -sh "${REPO_ROOT}/build" 2>/dev/null | cut -f1)
  echo "║  Build size:  ${BUILD_SIZE}"
fi
echo "╚══════════════════════════════════════════════════════════════╝"
