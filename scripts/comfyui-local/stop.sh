#!/usr/bin/env bash
# stop.sh — stop the ComfyUI Distrobox (models and venv persist on disk).
set -euo pipefail
BOX="comfyui"
echo "==> fermo il box '$BOX'"
distrobox stop "$BOX" --yes || true
echo "OK (per rimuoverlo del tutto: distrobox rm $BOX --force)"
