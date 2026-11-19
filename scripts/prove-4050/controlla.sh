#!/usr/bin/env bash
# controlla.sh — la macchina è pronta per le prove? Non installa niente.
# Scrive $PROVE_DIR/<giorno>/macchina.txt e esce 1 se manca qualcosa di bloccante.
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra controlla "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
mkdir -p "$RIS"
OUT="$RIS/macchina.txt"; : > "$OUT"
bloccanti=0
riga() { printf '%-3s %-26s %s\n' "$1" "$2" "$3" | tee -a "$OUT"; }

riga "✓" "sistema" "$(rs_sistema) $(rs_versione), modo $(rs_modo) (ADR-0136)"
if nvidia-smi >/dev/null 2>&1; then
  gpu=$(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader | head -1)
  riga "✓" "GPU" "$gpu"
else
  riga "✗" "GPU" "nvidia-smi non risponde: senza driver NVIDIA nessuna prova va sulla GPU"; bloccanti=1
fi
ram=$(awk '/MemTotal/{print int($2/1048576)}' /proc/meminfo)
lib=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
segno="✓"; [ "$lib" -lt 8 ] && segno="!"
riga "$segno" "RAM" "$ram GB, liberi $lib GB (sotto 8 liberi: chiudi Steam e Firefox)"
servono="python3 git curl"
[ "$(rs_modo)" = box ] && servono="distrobox podman $servono"
for c in $servono; do
  if command -v "$c" >/dev/null 2>&1; then riga "✓" "$c" "$(command -v "$c")"
  else riga "✗" "$c" "manca"; bloccanti=1; fi
done
py=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null || echo "?")
riga "✓" "python3 dell'host" "$py (alle prove basta la libreria standard)"
casa=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
segno="✓"; [ "$casa" -lt 30 ] && segno="!"
riga "$segno" "disco in \$HOME" "$casa GB liberi (lettore ~5, prosa ~8, immagini ~25)"
ramo=$(git -C "$RADICE" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
testa=$(git -C "$RADICE" rev-parse --short HEAD 2>/dev/null || echo "?")
sporco=$(git -C "$RADICE" status --porcelain 2>/dev/null | wc -l)
riga "✓" "repo" "ramo $ramo, testa $testa, $sporco file modificati"
if [ "$(rs_modo)" = box ]; then
  for box in llm-locale comfyui whisper; do
    if box_c_e "$box"; then riga "✓" "box $box" "c'è"
    else riga "·" "box $box" "non c'è ancora (lo crea scripts/prove-4050/installa.sh)"; fi
  done
else
  if command -v ollama >/dev/null 2>&1; then riga "✓" "ollama" "$(command -v ollama)"
  else riga "·" "ollama" "manca (lo installa scripts/prove-4050/installa.sh)"; fi
fi
if server_ollama; then riga "✓" "Ollama" "risponde su $LLM_PORTA"
else riga "·" "Ollama" "spento (kit.sh lo accende da sé; a mano: scripts/llm-locale/start.sh)"; fi

echo
if [ "$bloccanti" -eq 0 ]; then echo "Pronta. Il riepilogo è in $OUT"; else echo "Manca qualcosa (✗ sopra). Riepilogo in $OUT"; fi
exit "$bloccanti"
