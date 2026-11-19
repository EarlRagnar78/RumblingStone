#!/usr/bin/env bash
# install-git-hooks.sh — one-time setup of two git hooks:
#   post-merge  rebuilds and syncs the skill mirrors after every `git pull`
#               that touches skills/ (for non-Claude agents; Claude Code
#               already syncs at session start);
#   pre-push    runs the blocking, fast CI gates (gate_locale --pre-push,
#               ADR-0143), via pre-commit when it is installed.
#
# In Claude Code cloud sessions .claude/hooks/session-start.sh runs this
# script; on your own machine run it once. Idempotent.
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

# pre-push: i gate bloccanti e veloci della CI (ADR-0143), fra cui la regola
# d'oro dei piani (ADR-0009). Con pre-commit installato (requirements-dev.txt)
# il hook è quello del framework, che legge .pre-commit-config.yaml; senza, o
# con RS_HOOK_NATIVO=1, un hook nativo lancia lo stesso comando.
if [ -z "${RS_HOOK_NATIVO:-}" ] && python3 -c "import pre_commit" 2>/dev/null \
   && [ -f "${REPO_ROOT}/.pre-commit-config.yaml" ]; then
  (cd "${REPO_ROOT}" && python3 -m pre_commit install --hook-type pre-push --overwrite >/dev/null)
else
  cat > "${HOOKS_DIR}/pre-push" << 'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install-git-hooks.sh (ADR-0143): i gate bloccanti
# e veloci della CI prima del push. Bypass consapevole: git push --no-verify
REPO_ROOT="$(git rev-parse --show-toplevel)"
if ! python3 "${REPO_ROOT}"/scripts/gate_locale.py --pre-push; then
  echo "[pre-push] Push bloccato: un gate della CI è rosso (scripts/gate_locale.py --pre-push)."
  echo "[pre-push] Correggi, oppure bypass consapevole: git push --no-verify"
  exit 1
fi
EOF
  chmod +x "${HOOKS_DIR}/pre-push"
fi

echo "Installed: ${HOOKS_DIR}/post-merge"
echo "Skill mirrors will now auto-sync after every git pull that touches skills/."
echo "Installed: ${HOOKS_DIR}/pre-push"
echo "Every push now runs the blocking, fast CI gates first (gate_locale --pre-push, ADR-0143)."
