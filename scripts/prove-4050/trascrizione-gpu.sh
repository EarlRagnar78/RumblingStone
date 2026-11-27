#!/usr/bin/env bash
# trascrizione-gpu.sh — whisper.cpp sulla GPU, su un audio pubblico e non personale (ADR-0136).
# Risponde alla domanda lasciata aperta dalla PR #424 (ADR-0135): la RTX 4050 si vede dal box, e
# quante volte il tempo reale va? La prova sulla serata vera resta quella della #424: qui non si
# registra nessuno.
#
# Parametri chiesti dal thread della trascrizione: large-v3-turbo-q8_0, `-l it -mc 0`, senza VAD
# (sullo stesso audio il VAD porta q8_0 da 2,3% a 8,6% di parole sbagliate: ne perde 62 nei buchi);
# audio = le prime 40 righe di FLEURS it_it/dev (Google, CC BY 4.0). Riferimento sulla CPU del
# container: 2,3% di parole sbagliate (MISURE.md della #424). La GPU deve dare lo stesso testo.
#
#   RS_WHISPER_BACKEND  vulkan (di serie nel box) | cuda (di serie su WSL2) | cpu
#   RS_WHISPER_COMMIT   il commit di whisper.cpp (di serie quello misurato nel container)
#   RS_FLEURS_RIGHE     quante righe di FLEURS (di serie 40)
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
rs_registra trascrizione-gpu "$@"; trap 'rs_fine_registro $?' EXIT   # log in $RIS/log (comune.sh)
BOX="${WHISPER_BOX:-whisper}"
LAVORO="${WHISPER_LAVORO:-$PROVE_DIR/whisper-lavoro}"
COMMIT="${RS_WHISPER_COMMIT:-5922450}"
RIGHE="${RS_FLEURS_RIGHE:-40}"
MODELLO=large-v3-turbo-q8_0
if [ -n "${RS_WHISPER_BACKEND:-}" ]; then BACKEND="$RS_WHISPER_BACKEND"
elif [ "$(rs_modo)" = box ]; then BACKEND=vulkan
else BACKEND=cuda; fi
DEST="$RIS/trascrizione-gpu"
FLEURS=https://huggingface.co/datasets/google/fleurs/resolve/main/data/it_it
box_c_e "$BOX" || {
  echo "ERRORE: il box '$BOX' non c'è. Una tantum: scripts/prove-4050/installa.sh" >&2; exit 3; }
mkdir -p "$LAVORO" "$DEST"
esito trascrizione-gpu modello "$MODELLO"
esito trascrizione-gpu backend "$BACKEND"
esito trascrizione-gpu whisper_commit "$COMMIT"
esito trascrizione-gpu testa "$(git -C "$RADICE" rev-parse --short HEAD)"

echo "==> 1/4 audio: le prime $RIGHE righe di FLEURS it_it/dev (CC BY 4.0, ~290 MB la prima volta)"
cd "$LAVORO"
[ -f dev.tsv ] || curl -fsSL -o dev.tsv "$FLEURS/dev.tsv"
if [ ! -f dev.tar.gz ]; then
  curl -fL --retry 3 -# -o dev.tar.gz.part "$FLEURS/audio/dev.tar.gz" && mv dev.tar.gz.part dev.tar.gz
fi
# Colonna 2 il file, colonna 3 la frase com'è scritta. L'ordine è quello del file: l'audio si
# incolla nello stesso ordine del riferimento, altrimenti la misura delle parole non torna.
head -n "$RIGHE" dev.tsv | cut -f2 > scelti.txt
head -n "$RIGHE" dev.tsv | cut -f3 > "$DEST/riferimento.txt"
rm -rf audio && mkdir audio
sed 's|^|*/|' scelti.txt > modelli-tar.txt
tar -xzf dev.tar.gz -C audio --wildcards -T modelli-tar.txt
: > concat.txt
while read -r f; do
  p=$(find audio -name "$f" -print -quit)
  [ -n "$p" ] || { echo "ERRORE: $f non è nell'archivio di FLEURS" >&2; exit 4; }
  echo "file '$LAVORO/$p'" >> concat.txt
done < scelti.txt

echo "==> 2/4 whisper.cpp $COMMIT con $BACKEND (nel box '$BOX'; la prima volta qualche minuto)"
case "$BACKEND" in
  vulkan) FLAG="-DGGML_VULKAN=1" ;;
  cuda)   FLAG="-DGGML_CUDA=1 -DCMAKE_CUDA_HOST_COMPILER=g++-12" ;;
  cpu)    FLAG="" ;;
  *) echo "ERRORE: RS_WHISPER_BACKEND=$BACKEND (vulkan, cuda o cpu)" >&2; exit 2 ;;
esac
gpu_foto trascrizione-gpu "prima"
nel_box "$BOX" bash -lc "
  set -e
  cd '$LAVORO'
  [ -d whisper.cpp ] || git clone -q https://github.com/ggml-org/whisper.cpp
  cd whisper.cpp && git fetch -q origin && git checkout -q '$COMMIT'
  cmake -B 'build-$BACKEND' $FLAG -DCMAKE_BUILD_TYPE=Release >/dev/null
  cmake --build 'build-$BACKEND' -j --config Release --target whisper-cli >/dev/null
  [ -f models/ggml-$MODELLO.bin ] || sh models/download-ggml-model.sh $MODELLO
  cd '$LAVORO'
  ffmpeg -v error -y -f concat -safe 0 -i concat.txt -ar 16000 -ac 1 -c:a pcm_s16le fleurs.wav
" 2>&1 | tee "$DEST/compila.log"

echo "==> 3/4 trascrizione (-l it -mc 0)"
# Il portatile ha due schede: Vulkan può scegliere quella integrata e il log le elenca tutte e due.
# La prova che ha lavorato la NVIDIA è la sua memoria che sale mentre whisper gira.
vram_ora() { { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null || true; } | head -1 | tr -cd "0-9"; }
vram_prima=$(vram_ora); : > "$DEST/vram-durante.txt"
( while :; do vram_ora >> "$DEST/vram-durante.txt"; echo >> "$DEST/vram-durante.txt"; sleep 2; done ) &
CAMPIONA=$!
trap 'c=$?; kill "$CAMPIONA" 2>/dev/null || true; rs_fine_registro "$c"' EXIT
t0=$(date +%s.%N)
nel_box "$BOX" bash -lc "
  cd '$LAVORO'
  whisper.cpp/build-$BACKEND/bin/whisper-cli -m whisper.cpp/models/ggml-$MODELLO.bin \
    -l it -mc 0 -f fleurs.wav -otxt -of '$DEST/grezza'
" > "$DEST/whisper.log" 2>&1 || { echo "ERRORE: whisper-cli è uscito con errore, vedi $DEST/whisper.log" >&2; }
t1=$(date +%s.%N)
kill "$CAMPIONA" 2>/dev/null || true
gpu_foto trascrizione-gpu "dopo"
vram_picco=$(grep -E '^[0-9]+$' "$DEST/vram-durante.txt" | sort -n | tail -1 || true)

echo "==> 4/4 esito"
secondi=$(python3 -c "print(round($t1 - $t0, 1))")
audio=$(nel_box "$BOX" bash -lc "ffprobe -v error -show_entries format=duration -of csv=p=0 '$LAVORO/fleurs.wav'" 2>/dev/null || echo 0)
# Che dispositivo ha usato: le righe di avvio di ggml (Vulkan0/CUDA0 col nome della scheda)
grep -iE 'ggml_vulkan: [0-9]|ggml_cuda_init|Device [0-9]|using .* backend|NVIDIA|GeForce|no GPU|whisper_backend_init|system_info' \
  "$DEST/whisper.log" | head -8 > "$DEST/dispositivo.txt" || true
esito trascrizione-gpu secondi "$secondi"
esito trascrizione-gpu secondi_audio "$audio"
esito trascrizione-gpu volte_tempo_reale "$(python3 -c "s=$secondi; a=float('${audio:-0}' or 0); print(round(a/s, 1) if s else 0)")"
esito trascrizione-gpu vram_prima_mib "${vram_prima:-}"
esito trascrizione-gpu vram_picco_mib "${vram_picco:-}"
esito trascrizione-gpu dispositivo "$(head -1 "$DEST/dispositivo.txt" 2>/dev/null || echo '?')"
# La misura delle parole è quella della #424: se lo script c'è (PR unita), la faccio qui
if python3 "$RADICE/scripts/transcribe_session.py" misura --help >/dev/null 2>&1; then
  python3 "$RADICE/scripts/transcribe_session.py" misura "$DEST/grezza.txt" "$DEST/riferimento.txt" \
    | tee "$DEST/misura.txt"
else
  echo "misura: dopo la #424 (transcribe_session.py misura non è ancora su questo ramo)" | tee "$DEST/misura.txt"
fi
cat "$DEST/esito.txt"
echo "Fatto: $DEST. Ora: scripts/prove-4050/riporta.sh"
