#!/usr/bin/env bash
# immagini.sh [--solo SCENA[,SCENA]] [--semi N] [--profilo gpu|cpu] — la pipeline dei personaggi
# in posa (thread «Immagini dei personaggi in posa») sulla GPU del portatile.
# La pipeline è quella del 29/10, copiata in plans/esperimenti/immagini-posa-4050-2026-11-15/dati/
# con tre manopole per i 6 GB: RS_COMFY_ARGS (default --lowvram sul profilo gpu, niente sul
# profilo leggero), RS_LIBERA (default 1: un modello alla volta), RS_VLM_DEVICE (default auto:
# il giudice Qwen3-VL-4B in parte in VRAM, in parte in RAM).
# --profilo cpu è il profilo leggero del 29/10 (SD1.5 + LCM): qui gira sulla GPU, non sulla CPU.
# Usa il box «comfyui» di scripts/comfyui-local/ (lo crea setup-distrobox.sh); ComfyUI, i nodi e i
# pesi li prepara esegui_gpu.py in $PROVE_DIR/immagini-lavoro (~25 GB la prima volta).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra immagini "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
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
case "$PROFILO" in gpu|cpu) ;; *) echo "ERRORE: --profilo vuole gpu o cpu, non '$PROFILO'" >&2; exit 2 ;; esac
case "$SEMI" in ''|*[!0-9]*|0) echo "ERRORE: --semi vuole un numero da 1 in su, non '$SEMI'" >&2; exit 2 ;; esac
DATI="$RADICE/plans/esperimenti/immagini-posa-4050-2026-11-15/dati"
LAVORO="${IMMAGINI_LAVORO:-$PROVE_DIR/immagini-lavoro}"
DEST="$RIS/immagini-$PROFILO"
BOX="${COMFYUI_BOX:-comfyui}"
# SDXL nei 6 GB vuole --lowvram; SD1.5 del profilo leggero ci sta largo e va senza
if [ "$PROFILO" = gpu ]; then COMFY_ARGS="${RS_COMFY_ARGS---lowvram}"; else COMFY_ARGS="${RS_COMFY_ARGS-}"; fi
LIBERA="${RS_LIBERA:-1}"
# L'indice cu124 si ferma a PyTorch 2.6; il ComfyUI fissato (0df1646) dà la 2.7 come minimo e chiede
# la 2.8 per la gestione dinamica della VRAM. cu126 ha le versioni correnti (2.14 il 2026-11-18).
TORCH_INDEX="${RS_TORCH_INDEX:-https://download.pytorch.org/whl/cu126}"
VLM="${RS_VLM_DEVICE:-auto}"
box_c_e "$BOX" || {
  echo "ERRORE: il box '$BOX' non c'è. Una tantum: scripts/comfyui-local/setup-distrobox.sh" >&2; exit 3; }
mkdir -p "$LAVORO" "$DEST"
esito "immagini-$PROFILO" scene "${SOLO:-tutte}"
esito "immagini-$PROFILO" semi "$SEMI"
esito "immagini-$PROFILO" comfyui "${COMFY_ARGS:-(nessun argomento in più)}"
esito "immagini-$PROFILO" giudice "$VLM"
gpu_foto "immagini-$PROFILO" "prima"
t0=$(date +%s)
# Un venv tutto suo dentro il box, con PyTorch CUDA: non tocca quello di comfyui-local.
codice=0
nel_box "$BOX" bash -lc "
  set -e
  cd '$LAVORO'
  [ -f venv/bin/activate ] || { rm -rf venv; python3 -m venv venv; }   # un venv rimasto a metà si rifà
  . venv/bin/activate
  # manca, o è la 2.6 di un venv fatto prima del 18/11: si (ri)installa dall'indice giusto
  python -c 'import torch, torchvision; v = tuple(int(x) for x in torch.__version__.split(\".\")[:2]); raise SystemExit(v < (2, 8))' 2>/dev/null \\
    || pip install -q --upgrade torch torchvision --index-url '$TORCH_INDEX'
  python -c 'import torch; print(\"    torch\", torch.__version__, \"· GPU vista da torch:\", torch.cuda.is_available())'
  export HF_HUB_DISABLE_XET=1 RS_LIBERA='$LIBERA' RS_COMFY_DEVICE=gpu
  export RS_COMFY_ARGS='$COMFY_ARGS' RS_VLM_DEVICE='$VLM'
  python '$DATI/esegui_gpu.py' --dati '$DATI' --lavoro '$LAVORO' --uscita '$DEST' \
    --semi '$SEMI' --solo '$SOLO' --profilo '$PROFILO'
" 2>&1 | tee "$DEST/console.log" || codice=$?
# anche se la pipeline è andata in errore: la foto della GPU, i minuti e il log di ComfyUI dicono perché
gpu_foto "immagini-$PROFILO" "dopo"
esito "immagini-$PROFILO" minuti "$(minuti "$t0")"
esito "immagini-$PROFILO" codice "$codice"
cp "$LAVORO/comfy.log" "$DEST/" 2>/dev/null || true
if [ "$codice" -ne 0 ]; then
  echo "ERRORE: la pipeline è uscita con $codice. Guarda $DEST/console.log e $DEST/comfy.log; l'archivio si fa lo stesso con scripts/prove-4050/riporta.sh" >&2
  exit "$codice"
fi
echo "Fatto: $DEST (riepilogo.json e una cartella per scena). Ora: scripts/prove-4050/riporta.sh"
