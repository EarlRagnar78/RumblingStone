#!/usr/bin/env bash
# comune.sh — impostazioni comuni di setup/scarica-modello/start/stop/prova.
# Stessa architettura di scripts/comfyui-local/: un Distrobox con la GPU
# dell'host, niente sull'OS immutabile di Bazzite, i dati dove dice LLM_DIR.
#   LLM_DIR    dove stanno i modelli (default: scripts/llm-locale/dati, gitignorato)
#   LLM_BOX    nome del box (default: llm-locale)
#   LLM_PORTA  porta del server (default: 11434, quella di Ollama)
#   LLM_CTX    contesto in token (default: 32768: i prompt veri arrivano a ~25.500)
BOX="${LLM_BOX:-llm-locale}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RADICE="$(cd "$HERE/../.." && pwd)"
DEST="${LLM_DIR:-$HERE/dati}"
PORTA="${LLM_PORTA:-11434}"
CTX="${LLM_CTX:-32768}"
URL="http://127.0.0.1:$PORTA/v1"

spazio_libero() {
  local dir="$1" serve="$2" su
  su="$dir"; while [ ! -d "$su" ]; do su="$(dirname "$su")"; done
  local liberi; liberi=$(df -Pk "$su" | awk 'NR==2{print int($4/1048576)}')
  if [ "$liberi" -lt "$serve" ]; then
    echo "AVVISO: $liberi GB liberi in $su, ne servono ~$serve." >&2
    echo "        Scegli un altro disco:  export LLM_DIR=/srv/llm" >&2
    return 1
  fi
  echo "    spazio: $liberi GB liberi in $su (servono ~$serve)"
}

# consiglia: il modello che sta su questa macchina, da VRAM e RAM totale.
# Le misure sono quelle dei tag di ollama.com/library/gemma4 (2026-10-10):
# e4b-it-qat 6,1 GB · 12b-it-qat 7,2 GB · 26b (MoE, 3,8 miliardi attivi)
# 16-19 GB. Tutti Apache 2.0. Ollama mette in GPU quello che ci sta e il resto
# in RAM. ADR-0089.
consiglia() {
  local vram ram
  vram=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
  vram=$(( ${vram:-0} / 1024 ))
  ram=$(awk '/MemTotal/{print int($2/1048576)}' /proc/meminfo)
  if [ "$ram" -ge 30 ]; then echo "gemma4:26b"        # Dell: esperti in RAM
  elif [ "$vram" -ge 10 ]; then echo "gemma4:12b-it-qat"
  else echo "gemma4:e4b-it-qat"                        # 4-8 GB di GPU
  fi
}

# box_pronto: avvia il box e aspetta che la sua inizializzazione finisca, poi
# torna. Perché non basta `distrobox enter`: a box spento, enter lo avvia e
# segue il log (`podman logs -f`) fino a «container_setup_done». Sull'ASUS del
# DM quel log si ferma su «host's nvidia integration» e enter resta appeso,
# mentre una seconda sessione, a box già acceso, entra subito (2026-10-10 e
# 2026-10-11). Qui si legge il log a intervalli invece di seguirlo; a box
# acceso, enter non aspetta più niente.
box_pronto() {
  local stato t0 i
  stato=$(podman inspect -f '{{.State.Running}}' "$BOX" 2>/dev/null || echo assente)
  [ "$stato" = true ] && return 0
  [ "$stato" = assente ] && { echo "ERRORE: il box '$BOX' non c'è. Lancia setup-distrobox.sh" >&2; return 1; }
  t0=$(date +%s)
  echo "==> avvio il box '$BOX' e aspetto la sua inizializzazione (la prima volta dopo un riavvio: minuti)"
  podman start "$BOX" >/dev/null
  for i in $(seq 1 $(( ${LLM_ATTESA:-180} / 5 ))); do
    if podman logs --since "$t0" "$BOX" 2>&1 | grep -q container_setup_done; then
      echo " pronto"; return 0
    fi
    printf '.'; sleep 5
  done
  echo
  # Sull'ASUS del DM il log non dice mai «finito», ma dopo tre minuti Ollama
  # parte e vede la GPU (2026-10-11): si aspetta tre minuti e si prova.
  echo "AVVISO: dopo ${LLM_ATTESA:-180} s il log del box non dice «finito». Provo lo stesso;" >&2
  echo "        per vederla: podman logs --since $t0 $BOX | tail" >&2
}
