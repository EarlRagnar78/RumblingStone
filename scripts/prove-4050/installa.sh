#!/usr/bin/env bash
# installa.sh [--mostra] [--driver] [--senza-box] — prepara la macchina per tutte le prove del kit
# (ADR-0136). Riconosce il sistema da /etc/os-release e fa solo i passi che servono lì:
#
#   Bazzite        niente sull'host (distrobox e podman ci sono già); crea i box
#   Debian 13      apt: distrobox, podman, uidmap, python3, git, curl; crea i box
#   CachyOS/Arch   pacman: distrobox, podman, python, git, curl; crea i box
#   Fedora         dnf: distrobox, podman; crea i box
#   WSL2 (Ubuntu)  niente box: apt (python3-venv, ffmpeg, cmake, CUDA) e Ollama sul sistema
#
# I box (immagine fissa, GPU dell'host con --nvidia, niente installato sull'host):
#   llm-locale  Ubuntu 24.04 + Ollama           (lettore, decodifica vincolata, prosa)
#   comfyui     Ubuntu 24.04 + python3-venv      (immagini in posa, FLUX del Drappo)
#   whisper     Fedora toolbox 43 + Vulkan       (trascrizione su GPU, come la guida della #424)
#
# --mostra     stampa i comandi senza eseguirli (anche per vedere cosa farebbe su un altro sistema)
# --driver     installa anche il driver NVIDIA dove si può fare da qui (Debian, CachyOS). Poi va
#              riavviata la macchina. Su Bazzite il driver viene dall'immagine «-nvidia».
# --senza-box  come su WSL2: tutto sul sistema, niente Distrobox (solo Debian/Ubuntu)
#
# Si può rilanciare quante volte si vuole: i passi già fatti non si rifanno, e un box rimasto a
# metà (macchina spenta durante l'installazione) viene tolto e ricreato. Per ripartire da zero:
# kit.sh pulisci, poi di nuovo kit.sh installa.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra installa "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
MOSTRA=0; DRIVER=0
while [ $# -gt 0 ]; do
  case "$1" in
    --mostra) MOSTRA=1; shift ;;
    --driver) DRIVER=1; shift ;;
    --senza-box) export RS_SENZA_BOX=1; shift ;;
    *) echo "uso: $0 [--mostra] [--driver] [--senza-box]" >&2; exit 2 ;;
  esac
done
SISTEMA="$(rs_sistema)"; MODO="$(rs_modo)"

# esegui COMANDO... — lo esegue, o lo stampa con --mostra
esegui() {
  if [ "$MOSTRA" = 1 ]; then printf '    $ %s\n' "$*"; else "$@"; fi
}

echo "==> sistema: $SISTEMA $(rs_versione) · modo: $MODO"

# 1 · i pacchetti dell'host -------------------------------------------------------------
echo "==> 1/4 pacchetti dell'host"
case "$SISTEMA:$MODO" in
  bazzite:box)
    echo "    niente da installare: distrobox e podman sono nell'immagine"
    [ "$DRIVER" = 1 ] && echo "    driver: su Bazzite viene dall'immagine «bazzite-nvidia» (rpm-ostree rebase), non da qui" ;;
  debian:box|ubuntu:box)
    esegui sudo apt-get update -qq
    esegui sudo apt-get install -y distrobox podman uidmap python3 git curl
    if [ "$DRIVER" = 1 ]; then
      # Debian 13: il driver è in «non-free» (e il firmware in «non-free-firmware»), da abilitare in
      # /etc/apt/sources.list.d/debian.sources se manca: lo script non tocca le sorgenti.
      if [ "$MOSTRA" = 1 ] || apt-cache policy nvidia-driver 2>/dev/null | grep -q 'Candidate: [0-9]'; then
        esegui sudo apt-get install -y linux-headers-amd64 nvidia-driver firmware-misc-nonfree nvidia-smi
        echo "    driver installato: riavvia la macchina, poi rilancia installa.sh"
      else
        echo "ERRORE: nvidia-driver non è tra i pacchetti. Aggiungi «contrib non-free non-free-firmware»" >&2
        echo "        a Components in /etc/apt/sources.list.d/debian.sources, poi apt update e rilancia." >&2
        exit 4
      fi
    fi ;;
  cachyos:box|arch:box)
    esegui sudo pacman -S --needed --noconfirm distrobox podman python git curl
    if [ "$DRIVER" = 1 ]; then
      if [ "$SISTEMA" = cachyos ]; then esegui sudo chwd -a   # rilevamento hardware di CachyOS
      else esegui sudo pacman -S --needed --noconfirm nvidia-open nvidia-utils; fi
      echo "    driver installato: riavvia la macchina, poi rilancia installa.sh"
    fi
    # podman senza root vuole un intervallo di uid: Arch non lo dà agli utenti già esistenti
    if [ "$MOSTRA" = 0 ] && ! grep -q "^$(id -un):" /etc/subuid 2>/dev/null; then
      esegui sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 "$(id -un)"
      esegui podman system migrate
    fi ;;
  fedora:box)
    esegui sudo dnf install -y distrobox podman python3 git curl ;;
  wsl:diretto|debian:diretto|ubuntu:diretto)
    esegui sudo apt-get update -qq
    esegui sudo apt-get install -y python3 python3-venv python3-pip git curl zstd ffmpeg \
      cmake g++ g++-12 libgl1 libglib2.0-0 nvidia-cuda-toolkit
    if [ "$MOSTRA" = 1 ] || ! command -v ollama >/dev/null 2>&1; then
      # lo script ufficiale di ollama.com, lo stesso che setup-distrobox.sh usa nel box
      if [ "$MOSTRA" = 1 ]; then echo '    $ curl -fsSL https://ollama.com/install.sh | sh'
      else curl -fsSL https://ollama.com/install.sh | sh; fi
    fi
    # L'installatore accende un servizio ollama col contesto di serie: il kit vuole accendere il
    # suo, col contesto di ogni prova, sulla stessa porta. Il servizio si spegne.
    if [ "$MOSTRA" = 1 ] || systemctl is-enabled ollama >/dev/null 2>&1; then
      esegui sudo systemctl disable --now ollama
    fi
    [ "$SISTEMA" = wsl ] && echo "    GPU: su WSL2 il driver è quello di Windows; nvidia-smi sta in /usr/lib/wsl/lib" ;;
  *)
    echo "ERRORE: sistema «$SISTEMA» in modo «$MODO» non previsto dal kit." >&2
    echo "        Previsti: Bazzite, Debian 13, CachyOS (e Arch), Fedora, WSL2 con Ubuntu 24.04." >&2
    exit 3 ;;
esac

# 2 · la GPU -----------------------------------------------------------------------------
echo "==> 2/4 GPU"
if [ "$MOSTRA" = 1 ]; then echo "    (con --mostra non controllo)"
elif nvidia-smi >/dev/null 2>&1 || /usr/lib/wsl/lib/nvidia-smi >/dev/null 2>&1; then
  echo "    $(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null \
        || /usr/lib/wsl/lib/nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)"
else
  echo "AVVISO: nvidia-smi non risponde. Senza driver le prove girano sulla CPU o non girano." >&2
  echo "        Debian 13 e CachyOS: rilancia con --driver. Bazzite: immagine bazzite-nvidia." >&2
fi

# 3 · i box (solo in modo box) -------------------------------------------------------------
echo "==> 3/4 box"
if [ "$MODO" = diretto ]; then
  echo "    modo diretto: nessun box"
else
  # un box rimasto a metà (macchina spenta durante il primo avvio) si toglie e si rifà da capo
  if [ "$MOSTRA" = 0 ]; then
    for b in llm-locale comfyui whisper; do
      if box_a_meta "$b"; then
        echo "    il box '$b' c'è ma non ha mai finito di inizializzarsi: lo tolgo e lo rifaccio"
        box_togli "$b" || { echo "ERRORE: non riesco a togliere il box '$b'. Prova: podman rm -f $b" >&2; exit 6; }
      fi
    done
  fi
  # llm-locale: lo script che c'è già (Ollama dentro, ADR-0089)
  esegui "$RADICE/scripts/llm-locale/setup-distrobox.sh"
  # comfyui: basta Python col venv; ComfyUI e i pesi li preparano le prove nella loro cartella
  if [ "$MOSTRA" = 1 ] || ! box_c_e comfyui; then
    esegui distrobox create --name comfyui --image ubuntu:24.04 --nvidia --yes
  fi
  [ "$MOSTRA" = 1 ] || box_avvia comfyui   # il primo ingresso senza restare appesi (vedi ospite.sh)
  esegui distrobox enter comfyui -- bash -lc \
    "sudo dpkg --configure -a && sudo apt-get update -qq && sudo apt-get install -y -qq git python3-venv python3-pip libgl1 libglib2.0-0 ffmpeg"
  # whisper: la ricetta della guida della trascrizione (#424 §2), Vulkan col driver dell'host
  if [ "$MOSTRA" = 1 ] || ! box_c_e whisper; then
    esegui distrobox create --nvidia --name whisper --image registry.fedoraproject.org/fedora-toolbox:43 --yes
  fi
  [ "$MOSTRA" = 1 ] || box_avvia whisper
  esegui distrobox enter whisper -- bash -lc \
    "sudo dnf install -y -q git cmake gcc-c++ ffmpeg-free vulkan-headers vulkan-loader-devel glslc vulkan-tools"
fi

# 4 · il controllo finale ------------------------------------------------------------------
echo "==> 4/4 controllo"
if [ "$MOSTRA" = 1 ]; then echo "    $ scripts/prove-4050/controlla.sh"
else "$HERE/controlla.sh" || true; fi
echo
echo "Fatto. Ora: scripts/prove-4050/kit.sh piano   (poi kit.sh tutte)"
