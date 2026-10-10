#!/usr/bin/env bash
# comune.sh — shared settings for setup/start/stop/scarica-pesi.
# COMFYUI_DIR sets where the clone, the venv and the weights live (~15 GB).
# Default: inside the repo (gitignored). On a small /home disk use another
# disk, e.g.  export COMFYUI_DIR=/srv/comfyui
BOX="${COMFYUI_BOX:-comfyui}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${COMFYUI_DIR:-$HERE/ComfyUI}"

# spazio_libero <dir> <GB>: warns if fewer than <GB> are free where <dir> will be
spazio_libero() {
  local dir="$1" serve="$2" su
  su="$dir"; while [ ! -d "$su" ]; do su="$(dirname "$su")"; done
  local liberi; liberi=$(df -Pk "$su" | awk 'NR==2{print int($4/1048576)}')
  if [ "$liberi" -lt "$serve" ]; then
    echo "AVVISO: $liberi GB liberi in $su, ne servono ~$serve." >&2
    echo "        Scegli un altro disco:  export COMFYUI_DIR=/srv/comfyui" >&2
    return 1
  fi
  echo "    spazio: $liberi GB liberi in $su (servono ~$serve)"
}
