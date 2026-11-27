#!/usr/bin/env bash
# schede-vincolate.sh [MODELLO] — la tecnica 3 di Document AI (decodifica vincolata):
# le «Tattiche» di 12 schede di genera_creatura.py scritte dal modello locale in due modi,
# libero e vincolato con lo schema JSON del campo `format` di Ollama, poi il controllo S8.
# Piano e regola del verdetto: plans/esperimenti/decodifica-vincolata-2026-11-17/PIANO.md
# Default qwen2.5:7b (lo stesso del lettore: Apache 2.0, sta tutto nei 6 GB).
# Serve il server di scripts/llm-locale/start.sh acceso in un altro terminale.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra schede-vincolate "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
MODELLO="${1:-qwen2.5:7b}"
RIP="${RS_RIPETIZIONI:-3}"
QUI="$RADICE/plans/esperimenti/decodifica-vincolata-2026-11-17"
DEST="$RIS/schede-vincolate"
server_ollama || { echo "ERRORE: Ollama non risponde su $LLM_PORTA. In un altro terminale: scripts/llm-locale/start.sh" >&2; exit 3; }
mkdir -p "$DEST"
echo "==> 1/3 scarico $MODELLO (se non c'è già)"
"$RADICE/scripts/llm-locale/scarica-modello.sh" "$MODELLO"
echo "==> 2/3 12 schede × 2 bracci × $RIP ripetizioni (si salva a ogni risposta: se la interrompi, rilanciala)"
gpu_foto schede-vincolate "prima"
t0=$(date +%s)
python3 "$QUI/schede_vincolate.py" --modello "$MODELLO" --out "$DEST" --ripetizioni "$RIP" \
  --url "http://127.0.0.1:$LLM_PORTA"
gpu_foto schede-vincolate "dopo"
echo "==> 3/3 esito"
esito schede-vincolate modello "$MODELLO"
esito schede-vincolate ripetizioni "$RIP"
esito schede-vincolate minuti "$(minuti "$t0")"
esito schede-vincolate testa "$(git -C "$RADICE" rev-parse --short HEAD)"
echo
echo "Fatto. Le misure sono in $DEST/misure.json. Ora: scripts/prove-4050/riporta.sh"
