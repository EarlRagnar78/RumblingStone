#!/usr/bin/env bash
# stop.sh — ferma il box (i modelli restano su disco).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
distrobox stop "$BOX" --yes || true
echo "OK (per togliere tutto: distrobox rm $BOX --force; rm -rf $DEST)"
