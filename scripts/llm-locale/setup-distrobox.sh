#!/usr/bin/env bash
# setup-distrobox.sh — una tantum: un Distrobox con la GPU dell'host e Ollama
# (MIT) dentro. Su Bazzite distrobox e podman ci sono già; su Debian/Ubuntu:
# sudo apt install distrobox podman. Niente tocca l'OS dell'host. ADR-0089.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"

for c in distrobox podman; do
  command -v "$c" >/dev/null 2>&1 || {
    echo "ERRORE: $c non trovato. Su Debian/Ubuntu: sudo apt install distrobox podman" >&2; exit 1; }
done
nvidia-smi >/dev/null 2>&1 || \
  echo "AVVISO: nvidia-smi non risponde: il modello girerà sulla CPU, molto lento." >&2

echo "==> 0/3 i modelli andranno in $DEST"
mkdir -p "$DEST"
spazio_libero "$DEST" 12 || [ "${LLM_FORZA:-}" = 1 ] || {
  echo "        (oppure LLM_FORZA=1 per procedere lo stesso)" >&2; exit 1; }

# Distrobox condivide la home: una LLM_DIR fuori dalla home va montata
# (la stessa lezione di comfyui-local, 2026-10-09).
VOLUME=()
case "$(realpath "$DEST")/" in
  "$(realpath "$HOME")"/*) ;;
  *) VOLUME=(--volume "$(realpath "$DEST"):$(realpath "$DEST"):rw") ;;
esac

if distrobox list --no-color 2>/dev/null | grep -qE "\|\s*$BOX\s*\|"; then
  echo "==> 1/3 il box '$BOX' c'è già"
else
  echo "==> 1/3 creo il box '$BOX' (Ubuntu 24.04 + driver NVIDIA dell'host)"
  distrobox create --name "$BOX" --image ubuntu:24.04 --nvidia "${VOLUME[@]}" --yes
fi

echo "==> 2/3 installo Ollama nel box (script ufficiale di ollama.com)"
echo "    Il primo ingresso nel box lo inizializza: \"host's nvidia integration\""
echo "    può restare fermo diversi minuti. Per vederlo lavorare, da un altro"
echo "    terminale: podman logs -f $BOX"
box_pronto
distrobox enter "$BOX" -- bash -lc '
  set -e
  sudo apt-get update -qq
  sudo apt-get install -y curl ca-certificates zstd pciutils
  if ! command -v ollama >/dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
  fi
  ollama --version
'

echo "==> 3/3 la GPU vista dal box"
distrobox enter "$BOX" -- nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || \
  echo "AVVISO: il box non vede la GPU. Ricrealo: distrobox rm $BOX --force, poi rilancia." >&2

echo
echo "OK. Il modello consigliato per questa macchina: $(consiglia)"
echo "Ora: scripts/llm-locale/start.sh   (in un altro terminale: scarica-modello.sh)"
