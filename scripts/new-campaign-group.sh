#!/usr/bin/env bash
# new-campaign-group.sh
#
# Helper to start a new campaign with a new player group, preserving
# all preparation material (archs, PNGs, skills, maps) and only
# resetting the "live state" (state.md + sessions/).
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
[[ -f "campaign/templates/state-blank.md" ]] || \
    err "campaign/templates/state-blank.md not found — cannot reset"

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

# --- reset live state ---
echo "==> Resetting campaign/state.md from template..."
cp campaign/templates/state-blank.md campaign/state.md

echo "==> Clearing campaign/sessions/*.md..."
rm -f campaign/sessions/*.md
# keep a .gitkeep to preserve directory
touch campaign/sessions/.gitkeep

# --- commit ---
git add -A
git commit -m "Campaign group $NEW_GROUP: session 0 (reset from template)"

echo ""
echo "=========================================="
echo "✅ Done. New campaign group '$NEW_GROUP' initialized."
echo ""
echo "Next steps:"
echo "  1. Edit campaign/state.md §1 Party with your new PCs"
echo "  2. Set starting APL and in-world date"
echo "  3. git push -u origin $NEW_BRANCH"
echo "  4. Play session 1, then apply workflow in:"
echo "     campaign/DM-CAMPAIGN-PLAYBOOK.md §4"
echo "=========================================="
