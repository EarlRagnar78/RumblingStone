#!/bin/bash
# SessionStart hook — RumblingStone skill auto-sync
#
# Rebuilds the canonical skills/ tree and deploys it so the agent always
# reads the CURRENT version of every skill (see AGENTS.md "Supported
# Agents"). Runs:
#   1. scripts/build-skills.sh  → build packages + deploy ~/.<agent>/skills/
#   2. scripts/sync-skills.sh --no-build → in-repo mirrors (.claude/skills/ …)
#
# Idempotent and quiet. A failure must never block the session: we warn
# and exit 0 so Claude can still start (and fix the pipeline if asked).
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

# ── Dependencies (pip only in remote containers; never touch local envs) ──
if ! python3 -c "import yaml" 2>/dev/null; then
  if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
    pip install --quiet pyyaml || true
  fi
fi
if ! python3 -c "import yaml" 2>/dev/null; then
  echo "RumblingStone hook: pyyaml unavailable — skipping skill sync (run scripts/build-skills.sh manually)"
  exit 0
fi
# Test runner for scripts/tests/ (web sessions only; cached after first run)
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  python3 -c "import pytest" 2>/dev/null || pip install --quiet pytest || true
fi

# ── Rebuild + deploy skills ──────────────────────────────────────────────
if ./scripts/build-skills.sh >/tmp/rumblingstone-skill-build.log 2>&1 \
   && ./scripts/sync-skills.sh --no-build >>/tmp/rumblingstone-skill-build.log 2>&1; then
  echo "RumblingStone: skills rebuilt and deployed (canonical skills/ → .claude/skills/ + ~/.claude/skills/ and all agent mirrors)"
else
  echo "RumblingStone hook: skill build FAILED — see /tmp/rumblingstone-skill-build.log; agents may be reading stale skill mirrors"
fi

exit 0
