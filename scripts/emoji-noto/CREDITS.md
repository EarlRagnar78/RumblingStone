# Crediti — il ripiego Noto per le emoji locali delle mappe

Gli SVG di questa cartella vengono dal progetto **Noto Emoji** di Google
(<https://github.com/googlefonts/noto-emoji>, commit `e20cbc2` del 2026-09-24,
cartella `2D/svg/`). Le immagini sono sotto **Apache License 2.0**: il testo è in
`LICENSE` qui accanto, copiato da `2D/svg/LICENSE` dello stesso commit.

Servono a una cosa sola (ADR-0085): disegnare in modo uguale su ogni macchina le
emoji che una mappa dichiara nella sua riga `LEGENDA` e che la legenda universale
non conosce. I simboli universali sono disegnati in casa e non passano di qui.

## Le modifiche, come chiede la licenza

`scripts/build_emoji_noto.py` scarica il file e **rinomina ogni `id` interno**
aggiungendo il prefisso `nt<codice>_` (per esempio `Layer_2` → `nt1f4a0_Layer_2`),
e aggiorna i riferimenti `url(#…)` e `href="#…"`. Serve perché due emoji nella
stessa mappa non condividano un gradiente con lo stesso nome. Il disegno non
cambia. Il renderer poi toglie l'involucro `<svg>` e usa il contenuto come
`<symbol>`.

## Quali, e perché

`indice.json` elenca le emoji presenti, con quante celle del corpus le usano.
Si rigenera con `python3 scripts/build_emoji_noto.py`, e
`python3 scripts/build_emoji_noto.py --check` fallisce se una mappa usa
un'emoji locale senza il suo file.
