#!/usr/bin/env bash
# start.sh — launch ComfyUI inside the Distrobox on http://127.0.0.1:8188
# --lowvram fits 4-8 GB cards (SDXL on 4 GB runs, slowly). Ctrl-C stops the
# app; the box keeps running (stop it with stop.sh).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"

[ -d "$DEST" ] || { echo "ComfyUI non installato in $DEST: esegui prima setup-distrobox.sh" >&2; exit 1; }
ls "$DEST"/models/checkpoints/*.safetensors >/dev/null 2>&1 || \
  echo "AVVISO: nessun checkpoint in $DEST/models/checkpoints: esegui scarica-pesi.sh" >&2

echo "==> avvio ComfyUI su http://127.0.0.1:8188 (Ctrl-C per fermare)"
distrobox enter "$BOX" -- bash -lc "
  cd '$DEST'
  . venv/bin/activate
  python main.py --listen 127.0.0.1 --port 8188 --lowvram
"
