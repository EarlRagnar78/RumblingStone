#!/usr/bin/env bash
# drappo-flux.sh [--solo ID[,ID]] [--semi N] — il collaudo della D2 (arte del Drappo, PIANO-RIPRESA-PR-
# ABBANDONATE): due o tre tavole del Drappo generate in locale con FLUX.2 [klein] 4B (Apache 2.0, seed
# fisso) accanto a quelle di Gemini, per scegliere A (tenere Gemini) o B (rigenerare) guardando.
# Pesi per i 6 GB: transformer fp8 (4,07 GB) + Qwen3-4B fp4 (3,85 GB) + VAE, ComfyUI con --lowvram.
# BFL dichiara ~13 GB di VRAM in bf16: qui si misura se e quanto regge su 6 (picchi in riepilogo.json).
# Usa il box «comfyui» e la cartella di lavoro di immagini.sh (stesso ComfyUI, stesso venv).
# Le immagini del modulo non vengono toccate: tutto finisce in $PROVE_DIR/<giorno>/drappo-flux/.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
SOLO="ritratto-vanna,tavola-la-ruota,il-drappo"; SEMI=2
while [ $# -gt 0 ]; do
  case "$1" in
    --solo) SOLO="$2"; shift 2 ;;
    --semi) SEMI="$2"; shift 2 ;;
    *) echo "uso: $0 [--solo ID[,ID]] [--semi N]" >&2; exit 2 ;;
  esac
done
LAVORO="${IMMAGINI_LAVORO:-$PROVE_DIR/immagini-lavoro}"
DEST="$RIS/drappo-flux"
BOX="${COMFYUI_BOX:-comfyui}"
COMFY_ARGS="${RS_COMFY_ARGS:---lowvram}"
podman container exists "$BOX" 2>/dev/null || {
  echo "ERRORE: il box '$BOX' non c'è. Una tantum: scripts/comfyui-local/setup-distrobox.sh" >&2; exit 3; }
mkdir -p "$LAVORO" "$DEST"
esito drappo-flux tavole "$SOLO"
esito drappo-flux semi "$SEMI"
esito drappo-flux comfyui "$COMFY_ARGS"
esito drappo-flux testa "$(git -C "$RADICE" rev-parse --short HEAD)"
gpu_foto drappo-flux "prima"
t0=$(date +%s)
distrobox enter "$BOX" -- bash -lc "
  set -e
  cd '$LAVORO'
  [ -d venv ] || python3 -m venv venv
  . venv/bin/activate
  python -c 'import torch' 2>/dev/null || pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu124
  python -c 'import torch; print(\"    GPU vista da torch:\", torch.cuda.is_available())'
  export HF_HUB_DISABLE_XET=1 RS_COMFY_ARGS='$COMFY_ARGS'
  python '$RADICE/scripts/prove-4050/drappo_flux.py' --lavoro '$LAVORO' --uscita '$DEST' \
    --solo '$SOLO' --semi '$SEMI'
" 2>&1 | tee "$DEST/console.log"
gpu_foto drappo-flux "dopo"
esito drappo-flux minuti "$(minuti "$t0")"
echo "Fatto: apri $DEST/confronto.html (Gemini a sinistra, FLUX a destra). Poi: scripts/prove-4050/riporta.sh"
