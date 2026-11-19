#!/usr/bin/env bash
# prosa.sh [MODELLO] — la prova di ADR-0089 col 12B (default gemma4:12b-it-qat), scelta dal DM
# l'11/10. Usa gli script di scripts/llm-locale/ e alla fine copia corsa e foglio nei risultati.
# Serve il server di scripts/llm-locale/start.sh acceso in un altro terminale.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra prosa "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
MODELLO="${1:-gemma4:12b-it-qat}"
ETICHETTA="$(echo "$MODELLO" | tr -cd 'a-z0-9')"
N="${LLM_RIPETIZIONE:-1}"
DEST="$RIS/prosa"
server_ollama || { echo "ERRORE: Ollama non risponde su $LLM_PORTA. In un altro terminale: scripts/llm-locale/start.sh" >&2; exit 3; }
mkdir -p "$DEST"
"$RADICE/scripts/llm-locale/scarica-modello.sh" "$MODELLO"
gpu_foto prosa "prima"
t0=$(date +%s)
"$RADICE/scripts/llm-locale/prova.sh" "$MODELLO" "$ETICHETTA"
gpu_foto prosa "dopo"
esito prosa modello "$MODELLO"
esito prosa minuti "$(minuti "$t0")"
CORSA="$RADICE/plans/scrittura/corse/L-$ETICHETTA-$N"
FOGLIO="$RADICE/plans/scrittura/prove-locali/foglio-$ETICHETTA-$N.md"
cp -r "$RADICE/plans/scrittura/prove-locali/L-$ETICHETTA-tempi-$N" "$DEST/" 2>/dev/null || true
if [ ! -d "$CORSA" ]; then
  esito prosa corsa "fermata dopo il caso dei tempi"
  echo
  echo "Ti sei fermato dopo il caso dei tempi: i dieci casi non sono girati e il foglio non c'è."
  echo "I tempi sono in $DEST. Per la corsa intera rilancia: scripts/prove-4050/prosa.sh $MODELLO"
  exit 0
fi
cp -r "$CORSA" "$DEST/"
if [ -f "$FOGLIO" ]; then cp "$FOGLIO" "$DEST/"; fi
echo
echo "Il foglio da leggere ad alta voce è $FOGLIO (copia in $DEST)."
echo "Quando l'hai compilato: cp \"$FOGLIO\" \"$DEST/\" && scripts/prove-4050/riporta.sh"
