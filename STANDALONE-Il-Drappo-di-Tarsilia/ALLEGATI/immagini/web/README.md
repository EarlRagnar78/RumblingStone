# `web/` — gli stessi dipinti, ma leggeri

Qui non c'è arte nuova. Ci sono le **derivate leggere** dei ritratti che stanno
nella cartella sopra: stesso taglio, stessa inquadratura, solo ridimensionate e
ricompresse.

Servono perché un ritratto originale è un PNG da **~6 MB**: sei schede da stampa
farebbero un PDF da **quaranta megabyte**, che non si manda per posta e che una
stampante di casa digerisce male. Le derivate stanno sotto i 130 KB l'una — il
fascicolo completo delle sei schede pesa **meno di un megabyte**.

| | originale | derivata |
|---|---|---|
| formato | PNG | JPEG progressivo, qualità 82 |
| lato lungo | 2496 px | 1000 px |
| peso | ~6 MB | 87–122 KB |

A 1000 px di lato lungo il ritratto stampato è **3,9 cm** di larghezza sulla
scheda, cioè oltre 600 dpi: molto più di quanto una stampante domestica possa
rendere. Non serve andare più su.

## Chi le usa

- `scripts/export_booklet_typst.py` con `"layout": "schede"` — cerca il ritratto
  **prima qui**, poi fra gli originali (`ritratti` nel manifest
  `homebrew/DRAPPO-SCHEDE-PG.manifest.json`);
- chiunque debba mandare un ritratto in chat senza far aspettare nessuno.

Per il **web** e per l'**HTML** non servono: `build_booklet_html.py` ricomprime
già in memoria le immagini sopra i 600 KB quando trova Pillow installato.

## Rigenerarle

Le derivate si buttano e si rifanno; gli originali no. Dopo aver sostituito o
aggiunto un ritratto in `ALLEGATI/immagini/`:

```bash
cd STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini
python3 - <<'PY'
from PIL import Image
from pathlib import Path
for f in sorted(Path(".").glob("ritratto-*.png")):
    im = Image.open(f).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    im.save(Path("web") / (f.stem + ".jpg"), "JPEG",
            quality=82, optimize=True, progressive=True)
PY
```

Pillow non è una dipendenza del toolkit: è un attrezzo da usare una volta ogni
volta che l'arte cambia (`pip install pillow`). In alternativa, con ImageMagick:

```bash
mogrify -path web -format jpg -resize 1000x1000 -quality 82 -interlace Plane ritratto-*.png
```

## Provenienza

Le derivate ereditano licenza e provenienza dei file originali: vedi
`../PROMPT-RITRATTI-E-TAVOLE.md` e la nota IP del modulo (`../../../IP-E-LICENZE.md`).
Nessuna modifica al contenuto dell'immagine — solo scala e compressione.
