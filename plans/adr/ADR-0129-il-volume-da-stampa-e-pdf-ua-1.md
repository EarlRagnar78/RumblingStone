# ADR-0129 — Il volume da stampa è PDF/UA-1

**Stato**: proposta (2026-11-13)
**Data**: 2026-11-13
**Decisione-fonte**: il DM (Jfs), 2026-11-13: quali tecniche di document AI, explainable AI e AI generativa, con gli standard e le librerie standard di fatto, migliorano in modo misurabile il repo e i contenuti generati; applicarle misurando prima in testing e poi approvando secondo lo schema del repo. Questa è la prima: lo standard di fatto dei documenti accessibili.
**Rapporti**: rivaluta la parte veraPDF di [ADR-0032](ADR-0032-misurare-la-leggibilita.md), che diceva «si rivaluta quando Typst emetterà l'identificazione PDF/UA». Usa il compilatore di [ADR-0116](ADR-0116-typst-si-installa-da-pypi.md). Canale testing di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md).

## Contesto

PDF/UA-1 (ISO 14289-1) è lo standard dei PDF accessibili; il validatore di
riferimento è veraPDF, che segue il Matterhorn Protocol. ADR-0032 l'aveva
provato sull'Abbazia: tre rilievi, di cui due di typst (metadati XMP e
`DisplayDocTitle`) che dal tema non si correggevano. Da typst 0.14 il
compilatore emette PDF/UA-1 se lo si chiede (`pdf_standards: ["ua-1"]`) e
verifica da sé, rifiutando di compilare, gli obblighi che dipendono dal
documento.

Misura su main (837876d6), 19 booklet, veraPDF 1.28.2: **0 conformi, 132
controlli falliti**. Typst con `ua-1` ne compilava 2 su 19. Le cause nostre:
78 figure senza testo alternativo (i fregi dei capitoli e i ritratti delle
schede PG), 9 titoli che saltano un livello, e i titoli nascosti con `hide`,
che escono dall'albero dei tag.

## Decisione

1. `export_booklet_typst` chiede PDF/UA-1 a ogni compilazione
   (`typst_motore.compila(..., pdfua=True)`). Se typst lo rifiuta, ricompila
   come prima e lo **dice** con il motivo: il volume non manca mai per
   questo.
2. Il tema: il titolo visibile di un capitolo e il nome di una scheda PG sono
   il titolo che leggono i tag (`titolo-visibile`, fuori dall'indice e dai
   segnalibri, che restano al titolo nascosto); la testatina legge solo i
   titoli dell'indice; il fregio è un artefatto; il ritratto ha il testo
   alternativo «Ritratto di …».
3. Un titolo che nel master salta un livello sale al livello giusto
   nell'albero dei tag e si disegna come prima (`titoli_senza_salti`,
   etichetta `<come-N>`); sotto la profondità dell'indice resta fuori
   dall'indice.
4. Il cancello in CI è typst stesso, tenuto da `scripts/tests/test_pdfua.py`
   (tema, convertitore, un booklet vero). veraPDF resta fuori dalla CI per le
   ragioni di costo di ADR-0032 e si usa come banco
   (`plans/esperimenti/pdfua-2026-11-13/`).

Standard di fatto e alternative: typst è già il compilatore del repo;
veraPDF è il validatore di riferimento della PDF Association. Una libreria in
più non serve: nessuna dipendenza nuova.

## Misura

Ramo contro main, stessi 19 booklet: **17/19 conformi, 7 controlli falliti**
(da 0/19 e 132). Typst compila tutti i 19 come PDF/UA-1. Misure di stampa
(`misura_stampa --tutti`) identiche su ogni chiave; pagine identiche al pixel
tranne 4 pagine d'indice in 3 booklet, dove la voce «Chi si incontra in
questo capitolo» rientra di un livello in meno. Dettagli e la configurazione
scartata in `plans/esperimenti/pdfua-2026-11-13/MISURE.md`.

## Conseguenze

- Un master con un'immagine senza alt (o un altro obbligo che typst
  verifica) continua a produrre il volume, ma l'esportatore stampa «non è PDF/UA-1» e
  il motivo. Nei 19 booklet di oggi le immagini dei master hanno tutte l'alt.
- **Restano 7 controlli in 2 booklet** (7.21.5-1): glifi che i font del repo
  non hanno («⟺», «⟶», «►» nel Palio; «🔮», «🔷» in Terros) cadono su un font
  di sistema. Dipende dalla macchina; la correzione è di contenuto o un font
  di simboli nel repo, e va al DM.
- Conformità di macchina non vuol dire lettura buona: la prova con un lettore
  di schermo (NVDA, Orca) non è stata fatta.
- Una PR che cambia il tema o il convertitore e rompe PDF/UA-1 è rossa in
  `test_pdfua.py`.
