#!/usr/bin/env bash
# scarica-pesi.sh — download the SDXL 1.0 base checkpoint (OpenRAIL++-M,
# admitted by ADR-0019) into $DEST/models/checkpoints and verify its sha256
# against the one Hugging Face publishes for the file (the LFS oid).
# Resumable: re-run it after an interrupted download. ~6.9 GB.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"

REPO_HF="stabilityai/stable-diffusion-xl-base-1.0"
FILE="sd_xl_base_1.0.safetensors"
CART="$DEST/models/checkpoints"
mkdir -p "$CART"

echo "==> spazio"
spazio_libero "$CART" 8 || [ "${COMFYUI_FORZA:-}" = 1 ] || exit 1

echo "==> impronta pubblicata da Hugging Face per $FILE"
ATTESA=$(curl -fsSL "https://huggingface.co/api/models/$REPO_HF/tree/main" | python3 -c "
import json, sys
for x in json.load(sys.stdin):
    if x.get('path') == '$FILE':
        print(x['lfs']['oid'])
")
[ -n "$ATTESA" ] || { echo "ERRORE: impronta non trovata nell'indice di $REPO_HF" >&2; exit 1; }
echo "    sha256 atteso: $ATTESA"

echo "==> scarico (riprende se interrotto)"
curl -fL -C - -o "$CART/$FILE.part" "https://huggingface.co/$REPO_HF/resolve/main/$FILE"

echo "==> verifico"
OTTENUTA=$(sha256sum "$CART/$FILE.part" | cut -d' ' -f1)
if [ "$OTTENUTA" != "$ATTESA" ]; then
  echo "ERRORE: sha256 $OTTENUTA diverso da $ATTESA. Cancella $CART/$FILE.part e riprova." >&2
  exit 1
fi
mv "$CART/$FILE.part" "$CART/$FILE"
echo "OK: $CART/$FILE"
echo "    sha256 $OTTENUTA  (incollalo nella chat: entra nella provenienza ADR-0019)"
