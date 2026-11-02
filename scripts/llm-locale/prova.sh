#!/usr/bin/env bash
# prova.sh [MODELLO] [ETICHETTA] — la prova di ADR-0089 in tre passi, dall'host
# (serve solo python3, già sull'host):
#   1. un caso solo, per i tempi (non entra nel voto)
#   2. la corsa intera dei dieci casi, se il tempo regge
#   3. il voto, e il foglio alla cieca per il DM
# LLM_RIPETIZIONE sceglie la ripetizione (default 1), LLM_CONTESTO pieno|ridotto.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/comune.sh"
MODELLO="${1:-$(consiglia)}"
ETICHETTA="${2:-$(echo "$MODELLO" | tr -cd 'a-z0-9')}"
N="${LLM_RIPETIZIONE:-1}"
CONTESTO="${LLM_CONTESTO:-pieno}"
cd "$RADICE"
curl -fsS "http://127.0.0.1:$PORTA/api/version" >/dev/null || {
  echo "ERRORE: il server non risponde su $PORTA. Avvia scripts/llm-locale/start.sh" >&2; exit 1; }

echo "==> 1/3 un caso solo (S02, il duello), per i tempi"
# La prova dei tempi è usa e getta (prove-locali/ è fuori da git): si rifà.
rm -rf "plans/scrittura/prove-locali/L-$ETICHETTA-tempi-$N"
python3 scripts/banco_prosa_locale.py corsa --url "$URL" --modello "$MODELLO" \
  --etichetta "$ETICHETTA-tempi" --ripetizione "$N" --contesto "$CONTESTO" --ctx "$CTX" --caso S02
echo "    Il testo è in plans/scrittura/prove-locali/. Leggilo prima di andare avanti."
read -r -p "    Proseguo con i dieci casi? [s/N] " r
[ "$r" = s ] || [ "$r" = S ] || exit 0

echo "==> 2/3 i dieci casi"
python3 scripts/banco_prosa_locale.py corsa --url "$URL" --modello "$MODELLO" \
  --etichetta "$ETICHETTA" --ripetizione "$N" --contesto "$CONTESTO" --ctx "$CTX"

echo "==> 3/3 il voto e il foglio alla cieca"
python3 scripts/voto_scrittura.py --corse
# voti.json va committato insieme alla corsa: la CI lo confronta con corse/.
python3 scripts/voto_scrittura.py --emit
FOGLIO="plans/scrittura/prove-locali/foglio-$ETICHETTA-$N.md"
python3 scripts/banco_prosa_locale.py coppie --a B-con-1 --b "L-$ETICHETTA-$N" --seme "$N" -o "$FOGLIO"
echo
echo "Ora leggi ad alta voce $FOGLIO, scrivi 1, 2 o = dopo ogni «Preferito:», poi:"
echo "  python3 scripts/banco_prosa_locale.py esito $FOGLIO"
echo "Per mandarla: git add plans/scrittura/corse/L-$ETICHETTA-$N plans/scrittura/voti.json && git commit -m 'corsa L-$ETICHETTA-$N' && git push"
