#!/usr/bin/env bash
# new-campaign-group.sh
#
# Helper to start a new campaign with a new player group, preserving
# the PRODUCT (arcs, Bestiario, maps, skills, house rules) and resetting
# the PARTITA (ADR-0050 §7). What counts as partita is NOT listed here:
# it is data in scripts/dmcore/partita.py, executed by
# scripts/azzera_partita.py and checked by scripts/tests/test_new_group.py.
#
# Usage:
#   ./scripts/new-campaign-group.sh <new-group-name> [--backup-current <current-group-name>]
#
# Examples:
#   # Backup current group "alpha" and start "beta"
#   ./scripts/new-campaign-group.sh beta --backup-current alpha
#
#   # Just start "beta" (assumes main has the template/previous state)
#   ./scripts/new-campaign-group.sh beta
#
# See: campaign/DM-CAMPAIGN-PLAYBOOK.md §7

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

err() { echo "ERROR: $*" >&2; exit 1; }

# --- parse args ---
NEW_GROUP="${1:-}"
BACKUP_CURRENT=""
if [[ "${2:-}" == "--backup-current" ]]; then
    BACKUP_CURRENT="${3:-}"
    [[ -z "$BACKUP_CURRENT" ]] && err "--backup-current requires a group name"
fi

[[ -z "$NEW_GROUP" ]] && err "Usage: $0 <new-group-name> [--backup-current <current-group-name>]"

# --- sanity checks ---
command -v git >/dev/null || err "git not found"
[[ -d ".git" ]] || err "not a git repo"
[[ -f "scripts/azzera_partita.py" ]] || \
    err "scripts/azzera_partita.py not found — cannot reset"

# --- check clean working tree ---
if ! git diff-index --quiet HEAD --; then
    err "working tree is not clean — commit or stash first"
fi

echo "==> Current branch: $(git branch --show-current)"
echo "==> New group name: $NEW_GROUP"
[[ -n "$BACKUP_CURRENT" ]] && echo "==> Backup current as: campaign-group-$BACKUP_CURRENT"

read -p "Proceed? [y/N] " CONFIRM
[[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]] && { echo "Aborted."; exit 0; }

# --- backup current group ---
if [[ -n "$BACKUP_CURRENT" ]]; then
    BACKUP_BRANCH="campaign-group-$BACKUP_CURRENT"
    echo "==> Creating backup branch: $BACKUP_BRANCH"
    git checkout -b "$BACKUP_BRANCH"
    echo "==> Pushing backup branch to origin..."
    git push -u origin "$BACKUP_BRANCH" || echo "WARN: push failed — do it manually later"
    git checkout main
fi

# --- create new group branch ---
NEW_BRANCH="campaign-group-$NEW_GROUP"
echo "==> Creating new branch: $NEW_BRANCH"
git checkout -b "$NEW_BRANCH"

# --- reset partita (the list lives in scripts/dmcore/partita.py) ---
# azzera_partita.py validates the new state BEFORE writing and checks the
# regenerated state.md after: if it fails, nothing is committed.
echo "==> Resetting the partita (state, changelog, sessions, recaps)..."
python3 scripts/azzera_partita.py || err "reset failed — nothing committed, fix and rerun"

# --- commit ---
git add -A
git commit -m "Campaign group $NEW_GROUP: session 0 (reset from template)"

echo ""
echo "=========================================="
echo "✅ Done. New campaign group '$NEW_GROUP' initialized."
echo ""
echo "Next steps:"
echo "  1. Fill campaign/state.yaml: party, first villains, confine"
echo "     (NOT the tables of state.md: they are generated)"
echo "  2. python3 scripts/render_state.py && python3 scripts/validate_state.py"
echo "  3. python3 scripts/dm.py session branch --group $NEW_GROUP   # group.yaml"
echo "  4. git push -u origin $NEW_BRANCH"
echo "  5. Play session 1, then: python3 scripts/dm.py session end"
echo "=========================================="
