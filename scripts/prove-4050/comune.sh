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
rs_ferma_se_sandbox   # dentro una sandbox Flatpak nessuna prova può girare: si dice subito
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

# ---- il log di ogni esecuzione (richiesta del DM, 2026-11-19) --------------------------------
# rs_registra NOME [ARG...] — da qui in poi tutto quello che lo script scrive, uscita ed errori,
# va anche in $RIS/log/NOME-<ora>.log: sul terminale resta tutto come prima (tee), e stderr resta
# stderr. Un giro, un log: se lo script parte da un altro che registra già (kit.sh lancia le prove),
# non ne apre un secondo, perché la sua uscita finisce già nel log di chi l'ha lanciato.
# Chi chiama rs_registra mette rs_fine_registro nella sua trap EXIT, col codice d'uscita.
RS_REGISTRO_MIO=0
rs_registra() {
  [ -n "${RS_LOG:-}" ] && return 0
  local nome="$1"; shift
  mkdir -p "$RIS/log" 2>/dev/null || return 0
  RS_LOG="$RIS/log/$nome-$(date +%H%M%S).log"
  RS_REGISTRO_MIO=1
  export RS_LOG
  export PYTHONUNBUFFERED=1           # Python dietro una pipe scriverebbe a blocchi, a fine prova
  exec 9>&1 8>&2                      # il terminale vero: per stty e per chiudere il log
  export RS_FD_TERMINALE=9
  printf '# %s · %s · %s %s · %s\n# comando: %s %s\n' "$nome" "$(date '+%F %T')" \
    "$(rs_sistema)" "$(rs_versione)" "$(git -C "$RADICE" rev-parse --short HEAD 2>/dev/null || echo '?')" \
    "$0" "$*" >> "$RS_LOG"
  exec > >(tee -a "$RS_LOG"); RS_TEE_OUT=$!
  exec 2> >(tee -a "$RS_LOG" >&8); RS_TEE_ERR=$!
}

# Le righe che contano dopo un giro: errori, avvisi, traceback, uscite diverse da zero.
RS_AVVISI_RE="${RS_AVVISI_RE:-errore|error|avviso|attenzione|warn|traceback|exception|fatal|failed|fallit|non riesco|uscita [1-9]|uscita con [1-9]|killed|out of memory}"

# rs_avvisi CARTELLA_LOG — scrive CARTELLA_LOG/avvisi.txt: «file:riga: testo» di ogni riga che
# combacia con RS_AVVISI_RE. I log delle prove vengono prima di quelli di sessione del kit, e una
# riga uguale si scrive una volta sola, col file della prova da cui viene.
rs_avvisi() {
  local d="$1" f; local -a file=()
  [ -d "$d" ] || return 0
  for f in "$d"/*.log; do [ -e "$f" ] || continue; case "${f##*/}" in kit-*) ;; *) file+=("$f") ;; esac; done
  for f in "$d"/kit-*.log; do [ -e "$f" ] && file+=("$f"); done
  [ ${#file[@]} -gt 0 ] || { : > "$d/avvisi.txt"; return 0; }
  grep -HniE "$RS_AVVISI_RE" "${file[@]}" 2>/dev/null \
    | sed "s|^$d/||" \
    | awk '{t=$0; sub(/^[^:]*:[0-9]*:/, "", t); if (!(t in visto)) {visto[t]=1; print}}' > "$d/avvisi.txt" || true
}

# rs_fine_registro CODICE — chiude il log aperto da rs_registra (solo da chi l'ha aperto): avvisi,
# dove trovare tutto, codice d'uscita in coda. Aspetta i tee, così l'ultima riga non si perde.
rs_fine_registro() {
  local c="${1:-0}" n
  [ "$RS_REGISTRO_MIO" = 1 ] || return 0
  RS_REGISTRO_MIO=0
  rs_avvisi "$(dirname "$RS_LOG")"
  n=$(wc -l < "$(dirname "$RS_LOG")/avvisi.txt" 2>/dev/null || echo 0)
  echo "Log di questo giro: $RS_LOG ($n righe di errori e avvisi in $(dirname "$RS_LOG")/avvisi.txt)"
  exec 1>&9 2>&8
  wait "$RS_TEE_OUT" "$RS_TEE_ERR" 2>/dev/null || true
  echo "# uscita $c · $(date '+%F %T')" >> "$RS_LOG"
}

# rs_con_log FILE COMANDO... — esegue il comando con uscita ed errori anche in FILE (stderr resta
# stderr), aspetta che FILE sia scritto tutto e ritorna il codice del comando.
rs_con_log() {
  local f="$1"; shift
  ( "$@" 2> >(tee -a "$f" >&2); c=$?; wait $! 2>/dev/null; exit $c ) | tee -a "$f"
  return "${PIPESTATUS[0]}"
}
