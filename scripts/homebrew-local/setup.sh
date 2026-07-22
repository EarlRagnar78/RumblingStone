#!/usr/bin/env bash
# setup.sh — installa The Homebrewery in locale (Lotto K-B4, decisione K-D5).
#
# Wrapper SOTTILE sui comandi della documentazione UFFICIALE
# (naturalcrit/homebrewery README.md, sezione Installation, recuperata
# 2026-07-12): git clone → NODE_ENV=local → npm install. Nessun comando
# inventato; questo script aggiunge solo i controlli dei prerequisiti.
#
# Uso:  ./scripts/homebrew-local/setup.sh
#  (o)  python3 scripts/dm.py hype setup
set -euo pipefail
cd "$(dirname "$0")"

echo "== Homebrewery self-hosted — setup (prerequisiti: node>=16, mongodb, git) =="

# --- prerequisiti (dal README ufficiale) ---------------------------------
command -v git >/dev/null || {
  echo "✗ git mancante — installa da https://git-scm.com/downloads"; exit 1; }

command -v node >/dev/null || {
  echo "✗ Node.js mancante — serve v16+ : https://nodejs.org/en/"; exit 1; }
NODE_MAJOR="$(node -v | sed 's/^v//' | cut -d. -f1)"
if [ "$NODE_MAJOR" -lt 16 ]; then
  echo "✗ Node $(node -v) troppo vecchio — il README ufficiale richiede v16 o superiore"
  exit 1
fi
echo "✓ node $(node -v)"

if command -v mongod >/dev/null; then
  echo "✓ mongod presente"
else
  echo "⚠ mongod non trovato: Homebrewery salva i brew su MongoDB Community."
  echo "  Installa da https://www.mongodb.com/try/download/community"
  echo "  (oppure usa la via Docker: vedi scripts/homebrew-local/README.md §Via B)"
fi

# --- comandi ufficiali ----------------------------------------------------
if [ -d homebrewery/.git ]; then
  echo "✓ clone già presente (scripts/homebrew-local/homebrewery/) — salto il clone"
else
  git clone https://github.com/naturalcrit/homebrewery.git
fi

cd homebrewery
export NODE_ENV=local
npm install

echo ""
echo "== Setup completato =="
echo "Avvia mongod, poi:  python3 scripts/dm.py hype start"
echo "Editor a due pannelli su:  http://localhost:8000"
