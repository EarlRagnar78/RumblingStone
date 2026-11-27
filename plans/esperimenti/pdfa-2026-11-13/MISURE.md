# I booklet in PDF/A-2a — misure del 2026-11-13 (ADR-0131)

Banco: i 20 booklet con manifest (tutti i capitoli, `--all`), esportati con
`export_booklet_typst.py` su main 683480af e sul ramo. Poi veraPDF 1.28.2 con
tre profili: `ua1` (PDF/UA-1), `2a` e `2b` (PDF/A-2, livello a e b). La ricetta
di veraPDF è quella di `../pdfua-2026-11-13/` (`Avvio.java`, specchio
repo.maven.apache.org). Script: `banco_pdfa.py` (veraPDF) e
`confronto_pagine.py` (pagine, testo, pixel a 40 dpi). Numeri per booklet:
`misure.json`.

## Esito

| | main | ramo |
|---|---:|---:|
| PDF/A-2a conformi (veraPDF) | **0 / 20** | **20 / 20** |
| PDF/A-2a controlli falliti | **544** | **0** |
| PDF/A-2b conformi | 0 / 20 | 20 / 20 |
| PDF/UA-1 conformi | 20 / 20 | 20 / 20 |
| pagine | 985 | 985, uguali in ogni booklet |
| pagine col testo estratto diverso | | 0 |
| peso dei 20 PDF | 75,2 MB | 75,3 MB |

I 544 controlli falliti su main:
- 6.2.10-2 ×484: pagine con trasparenza senza gruppo di trasparenza né intento
  d'uscita (OutputIntent). Il ramo dichiara l'intento d'uscita sRGB, e basta
  quello;
- 6.6.4-1 ×20: il file non si dichiara PDF/A nei metadati XMP;
- 6.6.2.3.1-1 e -2 ×20 ciascuno: proprietà XMP fuori dagli schemi PDF/A.

## Che cosa cambia sulla pagina

Nulla di visibile. 86 pagine su 985 hanno pixel diversi a 40 dpi, ma lo scarto
massimo è di 3 livelli su 255 (in media 1): è la gestione del colore che segue
l'intento d'uscita sRGB. Il testo estratto è identico in tutte le 985 pagine.

## Perché A-2a e non altro

- **PDF/A-4** (ISO 19005-4) chiede PDF 2.0, PDF/UA-1 chiede PDF 1.7: typst
  rifiuta di combinarli («mutually incompatible»). PDF/UA-2 non c'è ancora in
  typst 0.15.
- **PDF/A-3** ammette file allegati, che i booklet non hanno.
- **A-2a** contro **A-2b/A-2u**: la «a» chiede la struttura logica e il testo
  Unicode, che il volume ha già per PDF/UA-1. È il livello più alto che qui si
  ottiene gratis.

## Cosa resta, dichiarato

- `misura_stampa` e `varianti_stampa` compilano senza PDF/A: misurano
  l'impaginazione, che non cambia.
- Il ripiego: se typst rifiuta il PDF/A per un booklet, l'esportatore
  ricompila col solo PDF/UA-1 e lo stampa («⚠ non è PDF/A»). Su 20 booklet non
  succede; il test lo prova con un rifiuto finto.
- Conformità di macchina: veraPDF è il validatore di riferimento per PDF/A
  (PDF Association), ma nessuna prova con un archivio vero.
