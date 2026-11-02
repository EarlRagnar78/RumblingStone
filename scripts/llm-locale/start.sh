#!/usr/bin/env bash
# start.sh — avvia il server Ollama nel box su http://127.0.0.1:$PORTA.
# Ctrl-C lo ferma. Il contesto lungo (LLM_CTX) serve perché le skill di prosa
# mettono fino a ~25.500 token nel prompt: con meno, il server taglia il
# prompt a metà e il modello scrive senza una parte delle norme, senza dirlo.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
mkdir -p "$DEST"
echo "==> Ollama su $URL · contesto $CTX token · modelli in $DEST (Ctrl-C per fermare)"
box_pronto
distrobox enter "$BOX" -- env \
  OLLAMA_HOST="127.0.0.1:$PORTA" \
  OLLAMA_MODELS="$DEST" \
  OLLAMA_CONTEXT_LENGTH="$CTX" \
  OLLAMA_FLASH_ATTENTION=1 \
  OLLAMA_KEEP_ALIVE=30m \
  ollama serve
