#!/usr/bin/env bash
# export-pdf-docker.sh — PDF dei booklet dentro un container (ADR-0013 §5-bis).
#
# Stessa identica resa di `dm.py booklet --pdf`, ma il Chromium sta nel
# container: nulla da installare sul sistema. Serve solo su distro
# immutabili o se non vuoi installare un browser.
#
# Uso:
#   scripts/booklet-container/export-pdf-docker.sh <manifest.json> [opzioni]
#   scripts/booklet-container/export-pdf-docker.sh <manifest.json> --all
#   scripts/booklet-container/export-pdf-docker.sh <manifest.json> --list
#
# Le opzioni sono quelle di scripts/export_booklet_pdf.py (--all, --pane,
# --list, --outdir). L'immagine viene costruita al primo uso.
set -euo pipefail

IMAGE="${BOOKLET_IMAGE:-rumblingstone/booklet-pdf}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

# podman va bene quanto docker (stessa CLI per questo uso)
RUNTIME="${CONTAINER_RUNTIME:-}"
if [ -z "$RUNTIME" ]; then
  if command -v docker >/dev/null 2>&1; then RUNTIME=docker
  elif command -v podman >/dev/null 2>&1; then RUNTIME=podman
  else
    echo "ERRORE: serve docker o podman (oppure installa chromium e usa 'dm.py booklet --pdf')." >&2
    exit 1
  fi
fi

if ! "$RUNTIME" image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "[booklet] costruisco l'immagine $IMAGE (solo la prima volta)…"
  "$RUNTIME" build -t "$IMAGE" "$HERE"
fi

if [ "$#" -eq 0 ]; then
  echo "Uso: $(basename "$0") <manifest.json> [--all|--pane cN…|--list|--outdir DIR]" >&2
  exit 2
fi

# I percorsi passati sono relativi al repo: il repo è montato su /repo.
exec "$RUNTIME" run --rm \
  -v "$REPO:/repo" \
  -w /repo \
  --shm-size=512m \
  -u "$(id -u):$(id -g)" \
  "$IMAGE" "$@"
