#!/usr/bin/env bash
# lettore-coerenza.sh [MODELLO] — il lettore del verificatore della coerenza della storia
# (ADR-0125) su un modello più grande del 3B del container: risponde SÌ/NO alle domande
# già preparate in plans/esperimenti/grafo-eventi-2026-11-12/misure/domande-ollama.json.
# Default qwen2.5:7b (Apache 2.0, ~4,7 GB: sta tutto nei 6 GB della 4050).
# Serve il server di scripts/llm-locale/start.sh acceso in un altro terminale.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra lettore-coerenza "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
MODELLO="${1:-qwen2.5:7b}"
QUI="$RADICE/plans/esperimenti/grafo-eventi-2026-11-12"
DOMANDE="$QUI/misure/domande-ollama.json"
NOME="$(echo "$MODELLO" | tr ':/' '--')"
DEST="$RIS/lettore-coerenza"
[ -f "$DOMANDE" ] || { echo "ERRORE: manca $DOMANDE (git pull?)" >&2; exit 2; }
server_ollama || { echo "ERRORE: Ollama non risponde su $LLM_PORTA. In un altro terminale: scripts/llm-locale/start.sh" >&2; exit 3; }
mkdir -p "$DEST"
n=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$DOMANDE")
echo "==> 1/3 scarico $MODELLO (se non c'è già)"
"$RADICE/scripts/llm-locale/scarica-modello.sh" "$MODELLO"
echo "==> 2/3 $n domande a $MODELLO (si salva ogni 20: se la interrompi, rilanciala e riparte)"
gpu_foto lettore-coerenza "prima"
t0=$(date +%s)
codice=0
python3 "$QUI/leggi_ollama.py" "$DOMANDE" --modello "$MODELLO" --out "$DEST/risposte-$NOME.json" \
  --url "http://127.0.0.1:$LLM_PORTA" || codice=$?
gpu_foto lettore-coerenza "dopo"
# in un file a parte e poi spostato: se Ollama non risponde più non resta un ollama-ps.json vuoto
if curl -fsS "http://127.0.0.1:$LLM_PORTA/api/ps" > "$DEST/ollama-ps.tmp" 2>/dev/null; then
  mv "$DEST/ollama-ps.tmp" "$DEST/ollama-ps.json"
else
  rm -f "$DEST/ollama-ps.tmp"
fi
echo "==> 3/3 esito"
esito lettore-coerenza modello "$MODELLO"
esito lettore-coerenza domande "$n"
esito lettore-coerenza minuti "$(minuti "$t0")"
esito lettore-coerenza testa "$(git -C "$RADICE" rev-parse --short HEAD)"
python3 - "$DEST/risposte-$NOME.json" <<'P' | tee -a "$DEST/esito.txt"
import json, sys
from pathlib import Path
r = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")) if Path(sys.argv[1]).exists() else {}
si = sum(1 for v in r.values() if v.upper().startswith("S"))
no = sum(1 for v in r.values() if v.upper().startswith("N"))
print(f"risposte: {len(r)} (SÌ {si}, NO {no}, altro {len(r) - si - no})")
P
if [ "$codice" -ne 0 ]; then
  echo "ERRORE: il lettore si è fermato (codice $codice). Le risposte avute sono salvate: rilancia lo stesso comando e riparte da lì." >&2
  exit "$codice"
fi
echo "Fatto. Ora: scripts/prove-4050/riporta.sh"
