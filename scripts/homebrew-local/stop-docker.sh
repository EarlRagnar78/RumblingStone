#!/usr/bin/env bash
# stop-docker.sh — ferma i container Homebrewery+MongoDB (Lotto K-B5).
# I dati dei brew restano nel volume docker 'mongodata' (compose ufficiale).
#
# Uso:  ./scripts/homebrew-local/stop-docker.sh
#  (o)  python3 scripts/dm.py hype docker-stop
set -euo pipefail
cd "$(dirname "$0")"

[ -d homebrewery ] || { echo "✗ nessuna installazione: niente da fermare"; exit 1; }
cd homebrewery

if docker compose version >/dev/null 2>&1; then
  docker compose down
else
  docker-compose down
fi
echo "✓ container fermati (i brew restano nel volume 'mongodata')"
