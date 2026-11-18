#!/usr/bin/env bash
# comune.sh — impostazioni comuni delle prove sul portatile con la RTX 4050.
# Guida: docs/how-to/GUIDA-PROVE-PORTATILE-4050.md
#   PROVE_DIR  dove finiscono i risultati (default: ~/rumblingstone-prove-4050,
#              fuori dal repo: dentro ci sono anche immagini e tempi della macchina)
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034  # RADICE la usano gli script che includono questo file
RADICE="$(cd "$HERE/../.." && pwd)"
PROVE_DIR="${PROVE_DIR:-$HOME/rumblingstone-prove-4050}"
# PROVE_GIORNO lo esporta kit.sh: un giro che passa la mezzanotte resta in una cartella sola
GIORNO="${PROVE_GIORNO:-$(date +%F)}"
RIS="$PROVE_DIR/$GIORNO"
LLM_PORTA="${LLM_PORTA:-11434}"
# shellcheck source=ospite.sh
. "$HERE/ospite.sh"
# Su WSL2 nvidia-smi viene dal driver di Windows e sta fuori dal PATH di serie
[ -x /usr/lib/wsl/lib/nvidia-smi ] && PATH="$PATH:/usr/lib/wsl/lib"

# esito PROVA CHIAVE VALORE — una riga «chiave: valore» nel file esito della prova
esito() {
  mkdir -p "$RIS/$1"
  printf '%s: %s\n' "$2" "$3" >> "$RIS/$1/esito.txt"
}

# gpu_foto PROVA ETICHETTA — memoria della GPU in quel momento (dice se il modello sta tutto in VRAM)
gpu_foto() {
  mkdir -p "$RIS/$1"
  { echo "## $2 · $(date +%T)"
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv 2>&1
  } >> "$RIS/$1/gpu.txt" || true   # senza nvidia-smi la foto dice perché, e la prova va avanti
}

# server_ollama — vero se il server di scripts/llm-locale/start.sh risponde
server_ollama() {
  curl -fsS "http://127.0.0.1:$LLM_PORTA/api/version" >/dev/null 2>&1
}

minuti() { echo $(( ( $(date +%s) - $1 + 59 ) / 60 )); }
