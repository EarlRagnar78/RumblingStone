# Container PDF dei booklet (opzionale)

> **Serve solo se non vuoi installare Chromium sul sistema** — per esempio su
> distribuzioni immutabili (Bazzite, Silverblue). Su una distro normale il
> container **non serve**: installa `chromium` e usa
> `python3 scripts/dm.py booklet <manifest> --pdf`.

**Guida completa** (prerequisiti, manifest, comandi, troubleshooting):
[`docs/guides/GUIDA-BOOKLET-E-PDF.md`](../../docs/guides/GUIDA-BOOKLET-E-PDF.md) §7.2.

## Uso

```bash
# costruisce l'immagine al primo lancio, poi esporta i PDF
scripts/booklet-container/export-pdf-docker.sh <manifest.json>          # pagine ✉ player
scripts/booklet-container/export-pdf-docker.sh <manifest.json> --all    # tutte le schede
scripts/booklet-container/export-pdf-docker.sh <manifest.json> --list   # elenco schede
```

- Funziona con **docker** o **podman** (rilevati automaticamente; forzabili
  con `CONTAINER_RUNTIME=podman`).
- Il repo è montato in `/repo`; i PDF escono in `<cartella manifest>/pdf/`
  coi permessi del tuo utente (`-u $(id -u):$(id -g)`).
- Nome immagine personalizzabile con `BOOKLET_IMAGE`.

## Cosa c'è dentro

Debian stable + il pacchetto `chromium` della distro + Python 3 + font
DejaVu e Noto Color Emoji (servono alle mappe emoji e alla pergamena).
L'entrypoint è lo stesso script del flusso nativo
(`scripts/export_booklet_pdf.py`): **stessa resa**, solo un browser diverso.

## Stato di collaudo

⚠️ Dockerfile e wrapper usano comandi standard, ma **non sono stati eseguiti
end-to-end** nell'ambiente di sviluppo (daemon Docker non disponibile).
Sintassi dello script verificata. Segnala qualsiasi intoppo al primo uso reale.
