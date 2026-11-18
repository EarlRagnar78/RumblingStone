#!/usr/bin/env bash
# ospite.sh — su quale sistema girano le prove, e come si entra nel «box» (ADR-0136).
# Lo includono comune.sh di qui, di scripts/llm-locale/ e di scripts/comfyui-local/.
#
#   rs_sistema   bazzite | debian | cachyos | arch | fedora | ubuntu | wsl | flatpak | altro
#   rs_modo      box     (Linux: gli strumenti stanno in un Distrobox con la GPU dell'host)
#                diretto (WSL2 o RS_SENZA_BOX=1: gli strumenti stanno sul sistema stesso)
#   nel_box BOX COMANDO...    esegue COMANDO nel box, o direttamente in modo diretto
#   box_c_e BOX               vero se il box esiste (sempre vero in modo diretto)
#   box_avvia BOX             accende il box se è spento e aspetta la sua inizializzazione
#   box_a_meta BOX            vero se il box c'è ma la sua inizializzazione non è mai finita
#   box_togli BOX             toglie il box (i dati delle prove stanno fuori dai box)
#
# RS_OS_RELEASE e RS_PROC_VERSION servono solo ai test (simulano un altro sistema).

rs_wsl() {
  grep -qiE 'microsoft|wsl' "${RS_PROC_VERSION:-/proc/version}" 2>/dev/null
}

# rs_sandbox — vero dentro una sandbox Flatpak (il terminale di un editor installato da Flathub):
# lì /etc/os-release è quello del runtime (ID=org.freedesktop.platform) e l'host non si vede.
rs_sandbox() {
  [ -e "${RS_FLATPAK_INFO:-/.flatpak-info}" ] && return 0
  grep -q '^ID=org\.freedesktop\.platform' "${RS_OS_RELEASE:-/etc/os-release}" 2>/dev/null
}

# rs_ferma_se_sandbox — le prove vogliono l'host: nvidia-smi, distrobox e podman dalla sandbox non
# si vedono (primo giro del DM sull'ASUS, 2026-11-18: «sistema: altro 25.08»). Esce con 5.
rs_ferma_se_sandbox() {
  rs_sandbox || return 0
  {
    echo "ERRORE: questo terminale gira dentro una sandbox Flatpak (quello di un editor installato da"
    echo "        Flathub, per esempio): da qui il sistema vero, la GPU, distrobox e podman non si vedono."
    echo "        Apri il terminale del sistema (Ptyxis o Konsole dal menu) e rilancia lo stesso comando."
    echo "        Oppure, da qui, se l'applicazione lo permette:  flatpak-spawn --host bash"
  } >&2
  exit 5
}

rs_sistema() {
  if rs_sandbox; then echo flatpak; return; fi
  if rs_wsl; then echo wsl; return; fi
  local f="${RS_OS_RELEASE:-/etc/os-release}" id="" like=""
  if [ -r "$f" ]; then
    id=$(sed -n 's/^ID=//p' "$f" | tr -d '"' | head -1)
    like=$(sed -n 's/^ID_LIKE=//p' "$f" | tr -d '"' | head -1)
  fi
  case "$id" in
    bazzite) echo bazzite ;;
    debian) echo debian ;;
    cachyos) echo cachyos ;;
    arch|endeavouros|manjaro) echo arch ;;
    fedora) echo fedora ;;
    ubuntu|pop|linuxmint) echo ubuntu ;;
    *) case " $like " in
         *" arch "*) echo arch ;;
         *" fedora "*) echo fedora ;;
         *" debian "*|*" ubuntu "*) echo debian ;;
         *) echo altro ;;
       esac ;;
  esac
}

rs_versione() {
  local f="${RS_OS_RELEASE:-/etc/os-release}"
  sed -n 's/^VERSION_ID=//p' "$f" 2>/dev/null | tr -d '"' | head -1
}

rs_modo() {
  if [ -n "${RS_SENZA_BOX:-}" ] || rs_wsl; then echo diretto; else echo box; fi
}

nel_box() {
  local box="$1"; shift
  if [ "$(rs_modo)" = diretto ]; then "$@"; return; fi
  box_avvia "$box" || return 1
  distrobox enter "$box" -- "$@"
}

# box_avvia BOX — a box spento `distrobox enter` lo avvia e segue il log fino a
# «container_setup_done»: sull'ASUS del DM quel log si ferma su «host's nvidia integration» e
# enter resta appeso (2026-10-10, vedi box_pronto in scripts/llm-locale/comune.sh). Qui il box si
# accende con podman e il log si legge a intervalli; a box acceso enter non aspetta più niente.
#   RS_BOX_ATTESA  secondi di attesa al massimo (di serie 300; poi si prova lo stesso)
box_avvia() {
  local box="$1" stato t0 attesa="${RS_BOX_ATTESA:-300}"
  [ "$(rs_modo)" = diretto ] && return 0
  stato=$(podman inspect -f '{{.State.Running}}' "$box" 2>/dev/null || echo assente)
  [ "$stato" = true ] && return 0
  [ "$stato" = assente ] && { echo "ERRORE: il box '$box' non c'è. Una tantum: scripts/prove-4050/installa.sh" >&2; return 1; }
  t0=$(date +%s)
  echo "==> avvio il box '$box' e aspetto la sua inizializzazione (la prima volta: minuti)" >&2
  podman start "$box" >/dev/null || return 1
  while [ $(( $(date +%s) - t0 )) -lt "$attesa" ]; do
    podman logs --since "$t0" "$box" 2>&1 | grep -q container_setup_done && return 0
    # se il box si ferma da solo l'inizializzazione è fallita: inutile aspettare
    [ "$(podman inspect -f '{{.State.Running}}' "$box" 2>/dev/null)" = true ] || {
      echo "ERRORE: il box '$box' si è fermato durante l'avvio. Vedi: podman logs $box | tail" >&2; return 1; }
    sleep 5
  done
  echo "AVVISO: dopo $attesa s il log del box '$box' non dice «finito». Provo lo stesso." >&2
}

box_c_e() {
  [ "$(rs_modo)" = diretto ] && return 0
  podman container exists "$1" 2>/dev/null
}

# box_a_meta BOX — vero se il box è stato creato ma la sua inizializzazione non è mai arrivata in
# fondo (macchina spenta durante il primo avvio, 2026-11-18). Il segno è il log di distrobox, che
# a ogni avvio riuscito scrive «container_setup_done». Un box mai acceso conta come a metà: rifarlo
# costa niente. Un box acceso col log vuoto (driver dei log spento) non si giudica: resta com'è.
box_a_meta() {
  local box="$1" avviato log
  [ "$(rs_modo)" = diretto ] && return 1
  podman container exists "$box" 2>/dev/null || return 1
  log=$(podman logs "$box" 2>&1 || true)
  case "$log" in *container_setup_done*) return 1 ;; esac
  avviato=$(podman inspect -f '{{.State.StartedAt}}' "$box" 2>/dev/null || echo "")
  case "$avviato" in ""|0001-*) return 0 ;; esac
  [ -n "$log" ]
}

# box_togli BOX — distrobox rm, e podman se distrobox non ci riesce (box rimasto a metà)
box_togli() {
  distrobox rm --force "$1" >/dev/null 2>&1 || podman rm -f "$1" >/dev/null 2>&1
}
