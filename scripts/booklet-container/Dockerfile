# Booklet PDF exporter — Chromium headless in container (ADR-0013 §5-bis).
#
# A COSA SERVE: generare i PDF A4 dei booklet SENZA installare Chromium sul
# sistema. Utile su distribuzioni immutabili (Bazzite/Silverblue) o quando
# non si vuole sporcare il PC. Su una distro normale NON serve: basta
# installare chromium e usare `dm.py booklet --pdf`.
#
# Build:  docker build -t rumblingstone/booklet-pdf scripts/booklet-container
# Uso:    scripts/booklet-container/export-pdf-docker.sh <manifest.json> [--all]
#
# Immagine base Debian stable + il pacchetto chromium della distro: nessun
# download di browser fuori dal package manager.
#
# Fissata per numero di versione e digest, non per nome in codice
# (PRATICHE PI-3b, 2026-10-07): Dependabot (`.github/dependabot.yml`, ecosistema
# `docker`) aggiorna il digest quando Debian ripubblica l'immagine con le
# correzioni di sicurezza, e propone il 14 quando esce. Con `bookworm-slim` non
# lo faceva, ed era rimasta su oldstable. Ogni sua PR costruisce l'immagine e
# stampa un PDF di prova in `.github/workflows/dipendenze.yml`.
FROM debian:13-slim@sha256:a29215f6a35e51e22adffa17f89e9d2ef06214e64a2bad10d765c46aea49f11f

RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium \
        python3 \
        fonts-dejavu-core \
        fonts-noto-color-emoji \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Lo script cerca il browser anche in $BOOKLET_CHROME
ENV BOOKLET_CHROME=/usr/bin/chromium

# Il repo viene montato qui a runtime (read-write: i PDF finiscono in pdf/)
WORKDIR /repo

ENTRYPOINT ["python3", "scripts/export_booklet_pdf.py"]
CMD ["--help"]
