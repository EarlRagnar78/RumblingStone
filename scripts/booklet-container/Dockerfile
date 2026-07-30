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
FROM debian:bookworm-slim

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
