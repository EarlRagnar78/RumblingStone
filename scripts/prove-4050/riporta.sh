#!/usr/bin/env bash
# riporta.sh [GIORNO] — impacchetta i risultati di un giorno di prove in un archivio da caricare
# nel thread del progetto. Dentro: macchina.txt, esiti, tempi, risposte, corse, misure e le
# immagini finali ridotte; fuori: pesi, venv, ComfyUI e le immagini intermedie.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
G="${1:-$GIORNO}"
SRC="$PROVE_DIR/$G"
[ -d "$SRC" ] || { echo "ERRORE: nessun risultato in $SRC" >&2; exit 2; }
ARCHIVIO="$PROVE_DIR/prove-4050-$G.tar.gz"
cd "$PROVE_DIR"
find "$G" -type f \( -name '*.txt' -o -name '*.json' -o -name '*.md' -o -name '*.log' \
  -o -name '5_finale.png' -o -name '1_genera_*.png' \) -size -8M | sort > "$PROVE_DIR/.elenco"
tar -czf "$ARCHIVIO" -T "$PROVE_DIR/.elenco"
rm -f "$PROVE_DIR/.elenco"
echo "Archivio: $ARCHIVIO ($(du -h "$ARCHIVIO" | cut -f1))"
echo "Caricalo nel thread «Preparare le prove sul portatile RTX 4050» (o in quello della prova)."
tar -tzf "$ARCHIVIO" | sed 's/^/  /'
