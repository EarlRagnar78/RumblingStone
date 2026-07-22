#!/usr/bin/env bash
# setup-docker.sh — The Homebrewery in container, chiavi in mano (Lotto K-B5).
#
# Sequenza UFFICIALE (repo naturalcrit/homebrewery, recuperata 2026-07-12):
#   - il repo include docker-compose.yml con ENTRAMBI i servizi
#     (mongodb + homebrewery, MONGODB_URI già cablata via env);
#   - il Dockerfile richiede config/docker.json (template dal
#     README.DOCKER.md ufficiale, scritto qui sotto ALLA LETTERA);
#   - build+avvio: docker compose up -d --build
# Questo script aggiunge SOLO i controlli prerequisiti e la stampa finale.
#
# Uso:  ./scripts/homebrew-local/setup-docker.sh
#  (o)  python3 scripts/dm.py hype docker
set -euo pipefail
cd "$(dirname "$0")"

echo "== Homebrewery in container — setup (prerequisito: Docker) =="

command -v git >/dev/null || {
  echo "✗ git mancante — installa da https://git-scm.com/downloads"; exit 1; }

command -v docker >/dev/null || {
  echo "✗ Docker mancante. Istruzioni ufficiali:"
  echo "    Linux (Docker Engine): https://docs.docker.com/engine/install/"
  echo "    Windows/macOS (Docker Desktop): https://docs.docker.com/desktop/"
  echo "  Post-install Linux consigliato dal progetto: uso senza root e avvio al boot:"
  echo "    https://docs.docker.com/engine/install/linux-postinstall/"
  exit 1; }

if docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null; then
  COMPOSE="docker-compose"
else
  echo "✗ Docker Compose mancante (plugin 'docker compose' o binario docker-compose)"
  echo "  https://docs.docker.com/compose/install/"
  exit 1
fi
echo "✓ docker $(docker --version | cut -d, -f1 | awk '{print $3}') · compose: $COMPOSE"

# --- clone del repo ufficiale (contiene docker-compose.yml e Dockerfile) --
if [ -d homebrewery/.git ]; then
  echo "✓ clone già presente — salto il clone"
else
  git clone https://github.com/naturalcrit/homebrewery.git
fi
cd homebrewery

# --- config/docker.json: template UFFICIALE dal README.DOCKER.md ----------
# (la mongodb_uri del template è sovrascritta dalla env MONGODB_URI del
#  docker-compose.yml ufficiale: mongodb://mongodb/homebrewery)
if [ ! -f config/docker.json ]; then
  mkdir -p config
  cat > config/docker.json <<'EOF'
{
"host" : "localhost:8000",
"naturalcrit_url" : "local.naturalcrit.com:8010",
"secret" : "secret",
"web_port" : 8000,
"mongodb_uri": "mongodb://172.17.0.2/homebrewery"
}
EOF
  echo "✓ scritto config/docker.json (template ufficiale)"
else
  echo "✓ config/docker.json già presente"
fi

# --- build + avvio di entrambi i container (compose ufficiale) ------------
$COMPOSE up -d --build

echo ""
echo "== Container attivi =="
$COMPOSE ps
echo ""
echo "Editor a due pannelli:  http://localhost:8000"
echo "Fermare:                python3 scripts/dm.py hype docker-stop"
echo "Log:                    (da scripts/homebrew-local/homebrewery/) $COMPOSE logs -f homebrewery"
echo "Aggiornare (procedura ufficiale): git pull → $COMPOSE up -d --build"
