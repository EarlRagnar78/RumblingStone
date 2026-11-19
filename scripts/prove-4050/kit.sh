#!/usr/bin/env bash
# kit.sh — il kit unico delle prove sulla RTX 4050 (ADR-0136). Un comando per sistema operativo
# a installare, uno a lanciare tutte le prove in fila, uno a verificarle e impacchettarle.
#
#   kit.sh installa [--mostra] [--driver]   prepara la macchina (vedi installa.sh)
#   kit.sh piano                            elenca le prove, il thread che le aspetta, lo stato di oggi
#   kit.sh tutte [--salta ID,ID]            lancia tutte le prove di prove.json, nell'ordine
#   kit.sh esegui ID [ID...]                lancia solo quelle
#   kit.sh verifica [GIORNO]                controlla i risultati (verifica.py) → verifica.md
#   kit.sh riporta [GIORNO]                 verifica, poi l'archivio da caricare nel thread
#   kit.sh pulisci [--si] [BOX...]          toglie i box (chiede conferma); modelli e risultati restano
#
# Il server Ollama lo accende e lo spegne il kit, col contesto che vuole ogni prova
# (server_ctx in prove.json). Se l'hai già acceso tu, il kit usa il tuo e lo lascia acceso.
# Una prova che fallisce non ferma le altre: il codice d'uscita finisce in <giorno>/kit.tsv.
#
# Log: tutto quello che il kit e le prove scrivono, uscita ed errori, va anche in <giorno>/log/:
# kit-<comando>-<ora>.log è il giro intero, <prova>.log è la parte di una prova (con il codice
# d'uscita in coda), avvisi.txt raccoglie errori, avvisi e traceback con file e riga. «riporta» li
# mette nell'archivio. piano e aiuto leggono soltanto e non scrivono log.
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
MANIFESTO="$HERE/prove.json"
export PROVE_GIORNO="$GIORNO"   # tutte le prove di questo giro scrivono nella cartella di partenza
SERVER_PID=""; SERVER_CTX=""

ids_del_manifesto() {
  python3 -c "import json,sys; print(' '.join(p['id'] for p in json.load(open(sys.argv[1]))['prove']))" "$MANIFESTO"
}

# campo ID CHIAVE — un campo della prova nel manifesto («» se null)
campo() {
  python3 - "$MANIFESTO" "$1" "$2" <<'P'
import json, sys
p = {x["id"]: x for x in json.load(open(sys.argv[1]))["prove"]}.get(sys.argv[2])
if p is None:
    sys.exit(2)
v = p.get(sys.argv[3])
print("" if v is None else str(v).lower() if isinstance(v, bool) else v)
P
}

# terminale_a_posto — «distrobox enter» mette il terminale in modalità grezza e, se il server
# viene spento con kill, non lo rimette com'era: le righe dopo escono a scaletta (primo giro
# sull'ASUS, 2026-11-19). Solo se l'uscita è un terminale.
# Col log aperto stdout è la pipe verso tee: il terminale vero è in RS_FD_TERMINALE (comune.sh).
terminale_a_posto() {
  local fd="${RS_FD_TERMINALE:-1}"
  if [ -t "$fd" ]; then stty sane <&"$fd" 2>/dev/null || true; fi
}

ferma_server() {
  [ -n "$SERVER_PID" ] || return 0
  echo "==> spengo il server Ollama (contesto $SERVER_CTX)"
  kill -- -"$SERVER_PID" 2>/dev/null || kill "$SERVER_PID" 2>/dev/null || true
  nel_box llm-locale pkill -f "ollama serve" 2>/dev/null || true
  for _ in $(seq 1 20); do server_ollama || break; sleep 1; done
  SERVER_PID=""; SERVER_CTX=""
  terminale_a_posto
}
trap 'codice_kit=$?; ferma_server; rs_fine_registro "$codice_kit"' EXIT

# server_con_ctx CTX — un server Ollama col contesto CTX, acceso dal kit se serve
server_con_ctx() {
  local ctx="$1"
  [ "$SERVER_CTX" = "$ctx" ] && server_ollama && return 0
  [ -n "$SERVER_PID" ] && ferma_server
  if server_ollama; then
    echo "    Ollama è già acceso (da te): lo uso così com'è, il contesto $ctx non è garantito"
    return 0
  fi
  mkdir -p "$RIS"
  echo "==> accendo Ollama col contesto $ctx (log in $RIS/ollama-ctx$ctx.log)"
  LLM_CTX="$ctx" setsid "$RADICE/scripts/llm-locale/start.sh" > "$RIS/ollama-ctx$ctx.log" 2>&1 &
  SERVER_PID=$!; SERVER_CTX="$ctx"
  # il primo avvio del box dopo un riavvio può chiedere minuti (box_pronto aspetta fino a 3)
  for _ in $(seq 1 120); do
    server_ollama && { echo "    pronto"; return 0; }
    kill -0 "$SERVER_PID" 2>/dev/null || break
    sleep 3
  done
  echo "ERRORE: Ollama non risponde. Vedi $RIS/ollama-ctx$ctx.log" >&2
  return 1
}

esegui_una() {
  local id="$1" script ctx t0 codice
  script=$(campo "$id" script) || { echo "ERRORE: prova «$id» non è in prove.json" >&2; return 2; }
  ctx=$(campo "$id" server_ctx)
  echo
  echo "################ $id · $(campo "$id" thread) · stima $(campo "$id" minuti_stimati) min"
  if [ -n "$ctx" ]; then server_con_ctx "$ctx" || { registra "$id" 3 0; return 3; }
  else ferma_server; fi
  t0=$(date +%s)
  mkdir -p "$RIS/log"
  printf '# %s · %s\n' "$id" "$(date '+%F %T')" >> "$RIS/log/$id.log"
  rs_con_log "$RIS/log/$id.log" "$HERE/$script"; codice=$?
  printf '# uscita %s · %s\n' "$codice" "$(date '+%F %T')" >> "$RIS/log/$id.log"
  registra "$id" "$codice" "$(minuti "$t0")"
  [ "$codice" -eq 0 ] || echo "!! $id è uscita con $codice: vado avanti con le altre" >&2
  return 0
}

registra() {
  mkdir -p "$RIS"
  printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$(date +%T)" >> "$RIS/kit.tsv"
}

piano() {
  echo "Sistema: $(rs_sistema) $(rs_versione) · modo $(rs_modo) · risultati in $RIS"
  echo
  python3 "$HERE/verifica.py" "$RIS" --quiet >/dev/null 2>&1 || true
  python3 - "$MANIFESTO" "$RIS/verifica.json" <<'P'
import json, sys
from pathlib import Path
prove = json.load(open(sys.argv[1]))["prove"]
v = json.loads(Path(sys.argv[2]).read_text()) if Path(sys.argv[2]).exists() else {}
print(f"{'prova':<18} {'min':>4}  {'oggi':<14} thread")
for p in prove:
    stato = v.get(p["id"], {}).get("stato", "non fatta")
    extra = " (chiede te)" if p["interattiva"] else ""
    print(f"{p['id']:<18} {p['minuti_stimati']:>4}  {stato:<14} {p['thread']}{extra}")
print(f"\nTotale stimato: {sum(p['minuti_stimati'] for p in prove)} minuti (stime, non misure sulla 4050)")
P
}

# pulisci [--si] [BOX...] — toglie i box del kit (tutti, o quelli nominati) dopo una conferma.
# Non tocca niente fuori dai box: i modelli di Ollama (scripts/llm-locale/dati o LLM_DIR), i pesi
# e i risultati in $PROVE_DIR restano dove sono, e un nuovo «installa» li ritrova.
pulisci() {
  local si=0 box risposta tutti="llm-locale comfyui whisper" scelti="" presenti=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --si) si=1 ;;
      llm-locale|comfyui|whisper) scelti="$scelti $1" ;;
      *) echo "uso: $0 pulisci [--si] [llm-locale] [comfyui] [whisper]" >&2; return 2 ;;
    esac
    shift
  done
  if [ "$(rs_modo)" = diretto ]; then
    echo "Modo diretto (WSL2 o --senza-box): non ci sono box da togliere."
    return 0
  fi
  for box in ${scelti:-$tutti}; do
    podman container exists "$box" 2>/dev/null && presenti="$presenti $box"
  done
  if [ -z "$presenti" ]; then
    echo "Nessun box da togliere (cercati: ${scelti:-$tutti}). Ora: $0 installa"
    return 0
  fi
  echo "Tolgo questi box:$presenti"
  echo "Restano dove sono: i modelli di Ollama (${LLM_DIR:-$RADICE/scripts/llm-locale/dati}),"
  echo "i pesi e i risultati delle prove ($PROVE_DIR)."
  if [ "$si" = 0 ]; then
    [ -t 0 ] || { echo "ERRORE: serve una conferma. Da uno script: $0 pulisci --si" >&2; return 2; }
    printf 'Confermi? Scrivi «si» e premi Invio: '
    read -r risposta
    case "$risposta" in si|sì|SI|Sì|s|S) ;; *) echo "Non ho tolto niente."; return 1 ;; esac
  fi
  ferma_server
  for box in $presenti; do
    if box_togli "$box"; then echo "    tolto: $box"
    else echo "ERRORE: non riesco a togliere '$box'. Prova: podman rm -f $box" >&2; return 1; fi
  done
  echo "Fatto. Ora: $0 installa"
}

cmd="${1:-piano}"; shift || true
case "$cmd" in
  tutte|esegui|verifica|riporta|pulisci) rs_registra "kit-$cmd" "$@" ;;
esac
case "$cmd" in
  installa) exec "$HERE/installa.sh" "$@" ;;
  piano) piano ;;
  tutte)
    SALTA=""
    [ "${1:-}" = --salta ] && { SALTA=",$2,"; shift 2; }
    for id in $(ids_del_manifesto); do
      case "$SALTA" in *",$id,"*) echo "(salto $id)"; continue ;; esac
      esegui_una "$id"
    done
    ferma_server; terminale_a_posto
    python3 "$HERE/verifica.py" "$RIS" ;;
  esegui)
    [ $# -gt 0 ] || { echo "uso: $0 esegui ID [ID...]   (gli id: $(ids_del_manifesto))" >&2; exit 2; }
    for id in "$@"; do esegui_una "$id"; done
    ferma_server; terminale_a_posto
    python3 "$HERE/verifica.py" "$RIS" ;;
  verifica) python3 "$HERE/verifica.py" "$PROVE_DIR/${1:-$GIORNO}" ;;
  riporta)  "$HERE/riporta.sh" "${1:-$GIORNO}" ;;
  pulisci)  pulisci "$@" ;;
  -h|--help|aiuto) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//' ;;
  *) echo "comando sconosciuto: $cmd (installa, piano, tutte, esegui, verifica, riporta, pulisci)" >&2; exit 2 ;;
esac
