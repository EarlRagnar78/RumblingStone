# Le tavole e i fregi del Drappo

Tutto vettoriale, tutto rigenerabile, **zero dipendenze**: si aprono in qualsiasi
browser e restano nitide in stampa a qualunque ingrandimento.

## Le tavole

| File | Cos'è |
|---|---|
| `tarsilia-citta.svg` | la mappa della città — copertina del booklet giocatori |
| `il-drappo.svg` | il telo dipinto con le nove facce — copertina del booklet DM |
| `ritratto-{vanna,nocca,ombra,tesio,berenice,melchio}.svg` | i sei **segnaposto** dei PG: reggono la stampa finché non arrivano i raster |

Si rigenerano con:

```bash
python3 ALLEGATI/tavole/build_tavole.py
```

## I fregi di capitolo

`fregi/` contiene **19 medaglioni**, uno per capitolo: la ruota per l'hub, l'urna
della Sorte per il Giorno 1, la coppa per la Cena, il traguardo per la Corsa, la
lanterna per la guida del DM, il sigillo per la nota IP.

Sono la scelta editoriale che un manuale pubblicato fa e un documento no: **un
segno che dice al lettore dov'è prima ancora che legga il titolo**. Vanno grandi
in copertina (34 mm) e piccoli accanto al titolo di capitolo (14 mm) — è la
misura a cui sono stati disegnati e verificati.

```bash
python3 ../../scripts/build_chapter_marks.py --serie drappo
```

La serie della campagna (una per arco) è **diversa e non intercambiabile**, e sta
in `docs/assets/fregi/`: due prodotti diversi non condividono i segni.

> **Come sono fatti**: primitive geometriche composte dentro il generatore —
> cerchi, archi, polilinee. Nessun asset di terzi, **nessuna licenza da citare**.
> È il motivo per cui il generatore esiste invece di prendere icone altrove.

> 🔎 **Tre disegni sono stati buttati e rifatti** guardandoli a grandezza reale:
> due coppe affiancate diventavano un «77», il canapo teso una «M», il martello
> di profilo un cartello stradale. La lezione sta scritta nel codice: **a 14 mm
> vince la sagoma, non la fedeltà all'oggetto**.
