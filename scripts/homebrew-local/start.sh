#!/usr/bin/env bash
# start.sh — avvia The Homebrewery locale (Lotto K-B4, decisione K-D5).
#
# Comandi dal README ufficiale (naturalcrit/homebrewery, 2026-07-12):
# NODE_ENV=local + npm start, con mongod in esecuzione → http://localhost:8000
#
# Uso:  ./scripts/homebrew-local/start.sh
#  (o)  python3 scripts/dm.py hype start
set -euo pipefail
cd "$(dirname "$0")"

[ -d homebrewery ] || {
  echo "✗ Homebrewery non installato: lancia prima  python3 scripts/dm.py hype setup"
  exit 1
}

if ! pgrep -x mongod >/dev/null 2>&1; then
  echo "⚠ mongod non sembra in esecuzione. Il README ufficiale prevede il"
  echo "  database attivo: avvia 'mongod' in un altro terminale (o il servizio"
  echo "  di sistema / il container Docker), poi rilancia questo script."
fi

cd homebrewery
export NODE_ENV=local
echo "== Avvio The Homebrewery — editor su http://localhost:8000 (Ctrl+C per fermare) =="
exec npm start
