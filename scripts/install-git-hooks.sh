#!/usr/bin/env bash
# install-git-hooks.sh — one-time setup for non-Claude agents (Cursor,
# Windsurf, Codex, Copilot, …): installs a git post-merge hook that
# rebuilds and syncs the skill mirrors after every `git pull`, so every
# agent always reads the current version of skills/*.
#
# Claude Code does NOT need this: .claude/hooks/session-start.sh runs the
# same sync automatically at session start.
#
# Usage:  ./scripts/install-git-hooks.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
HOOKS_DIR="$(git -C "${REPO_ROOT}" rev-parse --git-path hooks)"

mkdir -p "${HOOKS_DIR}"
cat > "${HOOKS_DIR}/post-merge" << 'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install-git-hooks.sh — resync skill mirrors
# after every merge/pull so agents read current skills/. Never blocks git.
REPO_ROOT="$(git rev-parse --show-toplevel)"
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q '^skills/'; then
  echo "[post-merge] skills/ changed — resyncing agent mirrors…"
  (cd "${REPO_ROOT}" && ./scripts/sync-skills.sh >/dev/null 2>&1) \
    && echo "[post-merge] skill mirrors updated" \
    || echo "[post-merge] WARNING: skill sync failed — run ./scripts/sync-skills.sh manually"
fi
exit 0
EOF
chmod +x "${HOOKS_DIR}/post-merge"

cat > "${HOOKS_DIR}/pre-push" << 'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install-git-hooks.sh — gate della regola d'oro
# dei piani (ADR-0009): modifiche strutturali senza riga in
# plans/CHANGELOG.md bloccano il push. Bypass consapevole: git push --no-verify
REPO_ROOT="$(git rev-parse --show-toplevel)"
git rev-parse --verify -q origin/main >/dev/null 2>&1 || exit 0
if ! python3 "${REPO_ROOT}/scripts/check_plans_discipline.py" --base origin/main --repo-root "${REPO_ROOT}"; then
  echo "[pre-push] Push bloccato dalla regola d'oro dei piani (ADR-0009)."
  echo "[pre-push] Aggiungi la riga a plans/CHANGELOG.md, oppure bypass consapevole: git push --no-verify"
  exit 1
fi
exit 0
EOF
chmod +x "${HOOKS_DIR}/pre-push"

echo "Installed: ${HOOKS_DIR}/post-merge"
echo "Skill mirrors will now auto-sync after every git pull that touches skills/."
echo "Installed: ${HOOKS_DIR}/pre-push"
echo "Structural pushes now require a plans/CHANGELOG.md row (ADR-0009)."
