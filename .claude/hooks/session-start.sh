#!/bin/bash
# SessionStart hook — RumblingStone skill auto-sync (ASYNC)
#
# Rebuilds the canonical skills/ tree and deploys it so the agent always
# reads the CURRENT version of every skill (see AGENTS.md "Supported
# Agents"). Async: the session starts immediately while the build runs in
# background. The race window (agent reading stale mirrors before the
# build finishes) is handled by the status-file protocol below + the
# AGENTS.md rule: before generating campaign content, Claude checks the
# status file and, if the sync isn't "ok", ASKS THE USER whether to
# update now — on yes it runs the two build commands inline, then the
# conversation continues.
#
# Status file: .claude/.skills-sync-status (gitignored)
#   syncing <utc-timestamp>          build in progress
#   ok <git-sha> <utc-timestamp>     mirrors current as of <git-sha>
#   failed <utc-timestamp>           build failed — see log
#
# A failure must never block the session: we warn and exit 0.
set -uo pipefail

echo '{"async": true, "asyncTimeout": 300000}'

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
STATUS_FILE=".claude/.skills-sync-status"
mkdir -p .claude
echo "syncing $(date -u +%FT%TZ)" > "${STATUS_FILE}"

# ── Dependencies (pip only in remote containers; never touch local envs) ──
if ! python3 -c "import yaml" 2>/dev/null; then
  if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
    pip install --quiet pyyaml || true
  fi
fi
if ! python3 -c "import yaml" 2>/dev/null; then
  echo "failed $(date -u +%FT%TZ)" > "${STATUS_FILE}"
  echo "RumblingStone hook: pyyaml unavailable — skill sync skipped (run scripts/build-skills.sh manually)"
  exit 0
fi
# Test runner for scripts/tests/ (web sessions only; cached after first run)
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  python3 -c "import pytest" 2>/dev/null || pip install --quiet pytest || true
fi

# ── Rebuild + deploy skills ──────────────────────────────────────────────
if ./scripts/build-skills.sh >/tmp/rumblingstone-skill-build.log 2>&1 \
   && ./scripts/sync-skills.sh --no-build >>/tmp/rumblingstone-skill-build.log 2>&1; then
  echo "ok $(git rev-parse --short HEAD 2>/dev/null || echo unknown) $(date -u +%FT%TZ)" > "${STATUS_FILE}"
  echo "RumblingStone: skills rebuilt and deployed (canonical skills/ → .claude/skills/ + ~/.claude/skills/ and all agent mirrors)"
else
  echo "failed $(date -u +%FT%TZ)" > "${STATUS_FILE}"
  echo "RumblingStone hook: skill build FAILED — see /tmp/rumblingstone-skill-build.log; agents may be reading stale skill mirrors"
fi

exit 0
