#!/usr/bin/env bash
# setup-distrobox.sh — one-time setup of a GPU-enabled Distrobox for ComfyUI on
# Bazzite (immutable OS). Keeps the whole toolchain OUT of the host system.
# Standard Distrobox + ComfyUI commands (see README.md for official sources).
set -euo pipefail

BOX="comfyui"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HERE/ComfyUI"

command -v distrobox >/dev/null 2>&1 || {
  echo "ERRORE: distrobox non trovato (su Bazzite è preinstallato)." >&2; exit 1; }

if ! nvidia-smi >/dev/null 2>&1; then
  echo "AVVISO: nvidia-smi non risponde sull'host — la GPU potrebbe non essere disponibile nel box." >&2
fi

echo "==> 1/4 creo il box '$BOX' (Ubuntu 24.04 + integrazione NVIDIA host)"
distrobox create --name "$BOX" --image ubuntu:24.04 --nvidia --yes || true

echo "==> 2/4 installo git/python nel box"
distrobox enter "$BOX" -- bash -lc '
  set -e
  sudo apt-get update -qq
  sudo apt-get install -y -qq git python3-venv python3-pip
'

if [ ! -d "$DEST/.git" ]; then
  echo "==> 3/4 clono ComfyUI (ufficiale) in $DEST"
  git clone https://github.com/comfyanonymous/ComfyUI.git "$DEST"
else
  echo "==> 3/4 ComfyUI già presente, aggiorno"
  git -C "$DEST" pull --ff-only || true
fi

echo "==> 4/4 virtualenv + PyTorch CUDA + requirements (nel box)"
distrobox enter "$BOX" -- bash -lc "
  set -e
  cd '$DEST'
  [ -d venv ] || python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
  pip install -r requirements.txt
"

echo
echo "OK. Ora scarica i modelli in $DEST/models/ (checkpoints/, controlnet/)"
echo "poi avvia con:  scripts/comfyui-local/start.sh"
