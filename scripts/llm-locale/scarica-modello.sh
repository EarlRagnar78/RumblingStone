#!/usr/bin/env bash
# scarica-modello.sh [MODELLO] — scarica i pesi (default: quello consigliato
# per questa macchina). Va lanciato con start.sh già acceso. Licenza: Gemma 4
# è Apache 2.0 (ADR-0019 vale per i pesi: un modello con licenza non OSI non si
# usa per il repo).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
MODELLO="${1:-$(consiglia)}"
curl -fsS "http://127.0.0.1:$PORTA/api/version" >/dev/null || {
  echo "ERRORE: il server non risponde su $PORTA. Avvia prima scripts/llm-locale/start.sh" >&2; exit 1; }
echo "==> scarico $MODELLO in $DEST"
box_pronto
distrobox enter "$BOX" -- env OLLAMA_HOST="127.0.0.1:$PORTA" ollama pull "$MODELLO"
distrobox enter "$BOX" -- env OLLAMA_HOST="127.0.0.1:$PORTA" ollama show "$MODELLO" --license 2>/dev/null | head -3 || true
echo "OK: $MODELLO. Ora: scripts/llm-locale/prova.sh $MODELLO"
