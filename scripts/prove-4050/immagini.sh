#!/usr/bin/env bash
# immagini.sh [--solo SCENA[,SCENA]] [--semi N] [--profilo gpu|cpu] — la pipeline dei personaggi
# in posa (thread «Immagini dei personaggi in posa», ADR-0115 proposta) sulla GPU del portatile.
# La pipeline è quella del 29/10, copiata in plans/esperimenti/immagini-posa-4050-2026-11-15/dati/
# con tre manopole per i 6 GB: RS_COMFY_ARGS (default --lowvram), RS_LIBERA=1 (un modello alla
# volta), RS_VLM_DEVICE (default auto: il giudice Qwen3-VL-4B in parte in VRAM, in parte in RAM).
# Usa il box «comfyui» di scripts/comfyui-local/ (lo crea setup-distrobox.sh); ComfyUI, i nodi e i
# pesi li prepara esegui_gpu.py in $PROVE_DIR/immagini-lavoro (~25 GB la prima volta).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
SOLO="thorik_posa_artemis"; SEMI=2; PROFILO=gpu
while [ $# -gt 0 ]; do
  case "$1" in
    --solo) SOLO="$2"; shift 2 ;;
    --tutte) SOLO=""; shift ;;
    --semi) SEMI="$2"; shift 2 ;;
    --profilo) PROFILO="$2"; shift 2 ;;
    *) echo "uso: $0 [--solo SCENA | --tutte] [--semi N] [--profilo gpu|cpu]" >&2; exit 2 ;;
  esac
done
DATI="$RADICE/plans/esperimenti/immagini-posa-4050-2026-11-15/dati"
LAVORO="${IMMAGINI_LAVORO:-$PROVE_DIR/immagini-lavoro}"
DEST="$RIS/immagini-$PROFILO"
BOX="${COMFYUI_BOX:-comfyui}"
COMFY_ARGS="${RS_COMFY_ARGS:---lowvram}"
VLM="${RS_VLM_DEVICE:-auto}"
box_c_e "$BOX" || {
  echo "ERRORE: il box '$BOX' non c'è. Una tantum: scripts/comfyui-local/setup-distrobox.sh" >&2; exit 3; }
mkdir -p "$LAVORO" "$DEST"
esito "immagini-$PROFILO" scene "${SOLO:-tutte}"
esito "immagini-$PROFILO" semi "$SEMI"
esito "immagini-$PROFILO" comfyui "$COMFY_ARGS"
esito "immagini-$PROFILO" giudice "$VLM"
gpu_foto "immagini-$PROFILO" "prima"
t0=$(date +%s)
# Un venv tutto suo dentro il box, con PyTorch CUDA: non tocca quello di comfyui-local.
nel_box "$BOX" bash -lc "
  set -e
  cd '$LAVORO'
  [ -d venv ] || python3 -m venv venv
  . venv/bin/activate
  python -c 'import torch' 2>/dev/null || pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu124
  python -c 'import torch; print(\"    GPU vista da torch:\", torch.cuda.is_available())'
  export HF_HUB_DISABLE_XET=1 RS_LIBERA=1
  export RS_COMFY_ARGS='$COMFY_ARGS' RS_VLM_DEVICE='$VLM'
  python '$DATI/esegui_gpu.py' --dati '$DATI' --lavoro '$LAVORO' --uscita '$DEST' \
    --semi '$SEMI' --solo '$SOLO' --profilo '$PROFILO'
" 2>&1 | tee "$DEST/console.log"
gpu_foto "immagini-$PROFILO" "dopo"
esito "immagini-$PROFILO" minuti "$(minuti "$t0")"
cp "$LAVORO/comfy.log" "$DEST/" 2>/dev/null || true
echo "Fatto: $DEST (riepilogo.json e una cartella per scena). Ora: scripts/prove-4050/riporta.sh"
