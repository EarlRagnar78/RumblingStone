#!/usr/bin/env bash
# ospite.sh — su quale sistema girano le prove, e come si entra nel «box» (ADR-0136).
# Lo includono comune.sh di qui, di scripts/llm-locale/ e di scripts/comfyui-local/.
#
#   rs_sistema   bazzite | debian | cachyos | arch | fedora | ubuntu | wsl | altro
#   rs_modo      box     (Linux: gli strumenti stanno in un Distrobox con la GPU dell'host)
#                diretto (WSL2 o RS_SENZA_BOX=1: gli strumenti stanno sul sistema stesso)
#   nel_box BOX COMANDO...    esegue COMANDO nel box, o direttamente in modo diretto
#   box_c_e BOX               vero se il box esiste (sempre vero in modo diretto)
#
# RS_OS_RELEASE e RS_PROC_VERSION servono solo ai test (simulano un altro sistema).

rs_wsl() {
  grep -qiE 'microsoft|wsl' "${RS_PROC_VERSION:-/proc/version}" 2>/dev/null
}

rs_sistema() {
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
  if [ "$(rs_modo)" = diretto ]; then "$@"; else distrobox enter "$box" -- "$@"; fi
}

box_c_e() {
  [ "$(rs_modo)" = diretto ] && return 0
  podman container exists "$1" 2>/dev/null
}
