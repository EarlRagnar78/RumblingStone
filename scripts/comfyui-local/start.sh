#!/usr/bin/env bash
# start.sh — launch ComfyUI inside the Distrobox on http://127.0.0.1:8188
# --lowvram is friendly to 8 GB cards (e.g. RTX 4050). Ctrl-C to stop the app;
# the box keeps running (stop it with stop.sh).
set -euo pipefail
BOX="comfyui"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HERE/ComfyUI"

[ -d "$DEST" ] || { echo "ComfyUI non installato: esegui prima setup-distrobox.sh" >&2; exit 1; }

echo "==> avvio ComfyUI su http://127.0.0.1:8188 (Ctrl-C per fermare)"
distrobox enter "$BOX" -- bash -lc "
  cd '$DEST'
  . venv/bin/activate
  python main.py --listen 127.0.0.1 --port 8188 --lowvram
"
