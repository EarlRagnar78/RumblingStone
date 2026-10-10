#!/usr/bin/env bash
# stop.sh — stop the ComfyUI Distrobox (models and venv persist on disk).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
echo "==> fermo il box '$BOX'"
distrobox stop "$BOX" --yes || true
echo "OK (per rimuoverlo del tutto: distrobox rm $BOX --force)"
