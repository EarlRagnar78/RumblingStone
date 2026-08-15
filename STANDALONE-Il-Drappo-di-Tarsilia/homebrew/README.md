# I tre booklet del Drappo

Impaginati con il motore del repo (lo stesso del booklet del Palio di Channathgate e
della sessione della Forgia Eterna): stile pergamena, tab DM/giocatore, mappe e
stemmi vettoriali inline, **niente dipendenze esterne**.

| Booklet | A chi va | Cosa contiene |
|---|---|---|
| **`DRAPPO-BOOKLET-DM.html`** | ⚠️ solo DM | tutto: regia, luoghi, agende dei villain, le tre giornate, statblocchi, playtest, stato del modulo, feedback, IP — 18 capitoli |
| **`DRAPPO-BOOKLET-GIOCATORI.html`** | ✉ giocatori | benvenuti a Tarsilia + i sei background. **Zero spoiler**: si può mandare prima della prima serata |
| **`DRAPPO-FASCICOLO-SCHEDE.html`** | ✉ giocatori | le sei schede (numeri) + il retro (background, legami, ritratto). Da stampare fronte-retro |
| **`DRAPPO-PROP.html`** | ✉ da consegnare | i quattro prop: il contratto, il registro, la ricevuta, il decreto. Una pagina l'uno |

Accanto a ogni `.html` c'è il gemello **`.hb.md`**: è il sorgente da incollare in
[Homebrewery](https://homebrewery.naturalcrit.com/) se preferisci impaginare là.

---

## Rigenerare

```bash
cd STANDALONE-Il-Drappo-di-Tarsilia/homebrew

# HTML + sorgente Homebrewery
python3 ../../scripts/build_booklet_html.py DRAPPO-BOOKLET-DM.manifest.json --format both
python3 ../../scripts/build_booklet_html.py DRAPPO-BOOKLET-GIOCATORI.manifest.json --format both
python3 ../../scripts/build_booklet_html.py DRAPPO-FASCICOLO-SCHEDE.manifest.json --format both
python3 ../../scripts/build_booklet_html.py DRAPPO-PROP.manifest.json --format both
```

## L'edizione da stampa — un volume solo

Accanto ai PDF per capitolo c'è la **seconda catena** (ADR-0020): stesso
manifest, un volume unico con tipografia embedded, fregi di capitolo e
segnalibri veri.

```bash
python3 ../../scripts/export_booklet_typst.py DRAPPO-BOOKLET-DM.manifest.json --all
```

Produce `DRAPPO-BOOKLET-DM-STAMPA.pdf` — **63 pagine, un file**. Serve il binario
`typst` (Apache 2.0): se manca, lo script dice come installarlo ed esce pulito.

## I PDF per capitolo

```bash
python3 ../../scripts/export_booklet_pdf.py DRAPPO-BOOKLET-DM.manifest.json --all
python3 ../../scripts/export_booklet_pdf.py DRAPPO-BOOKLET-GIOCATORI.manifest.json --all
python3 ../../scripts/export_booklet_pdf.py DRAPPO-FASCICOLO-SCHEDE.manifest.json --all
python3 ../../scripts/export_booklet_pdf.py DRAPPO-PROP.manifest.json --all
```

Finiscono in `pdf/`, un file A4 per capitolo (**una quarantina**: 19 per il DM, 3 per i
giocatori, 3 per il fascicolo, 5 per i prop, copertine incluse).

> ⚠️ **I PDF non sono committati**: `.gitignore` esclude `*.pdf` in tutto il repo,
> perché sono **artefatti rigenerabili** e pesano. I due comandi qui sopra li
> ricreano in meno di un minuto — servono solo un Chromium/Chrome sulla macchina, che
> l'esportatore trova da solo.

## Se cambi il contenuto

I booklet **non hanno testo proprio**: assemblano i file `.md` del modulo. Modifica il
capitolo alla fonte (per esempio `../06-VILLAIN-E-AGENDE.md`) e rigenera. Le due sole
pagine che vivono qui dentro sono:

- `DRAPPO-BOOKLET-INTRO.md` — la presentazione in copertina del booklet del DM;
- `DRAPPO-VOLANTINO-GIOCATORI.md` — il ✉ *Benvenuti a Tarsilia*, spoiler-free.

## Le copertine

Vengono dalle tavole vettoriali (`../ALLEGATI/tavole/`) e sono **inlined come SVG**,
non come immagini: restano nitide a qualsiasi ingrandimento e in stampa.

| Booklet | Copertina |
|---|---|
| DM | `il-drappo.svg` — il telo dipinto, con le nove facce |
| Giocatori | `tarsilia-citta.svg` — la mappa della città |
| Fascicolo | `ritratto-vanna.svg` |
