# ADR-0131 — Il volume da stampa è anche PDF/A-2a

**Stato**: proposta (2026-11-13)
**Data**: 2026-11-13
**Decisione-fonte**: il DM (Jfs), 2026-11-13: tecniche di document AI con gli standard di fatto, misurate prima in prova e poi approvate secondo lo schema del repo («continua con le prossime che mancano e che misurate migliorano»). PDF/A-2 era la seconda dell'ordine consigliato.
**Rapporti**: si aggiunge ad [ADR-0129](ADR-0129-il-volume-da-stampa-e-pdf-ua-1.md) (PDF/UA-1) e ad [ADR-0130](ADR-0130-le-emoji-del-volume-vengono-dal-repo.md) (font del repo), che lo rendono possibile: senza i font di sistema ogni glifo è incorporato.

## Contesto

I booklet sono il prodotto che resta della campagna: si stampano, si passano,
si rileggono anni dopo. PDF/A (ISO 19005) è lo standard per i PDF da
conservare: font incorporati, colore dichiarato, metadati che dicono cosa sono,
niente che dipenda dalla macchina che li apre. Su main nessuno dei 20 booklet
lo era: 544 controlli falliti con veraPDF, quasi tutti per il colore non
dichiarato.

## Decisione

1. `export_booklet_typst` chiede a typst **PDF/A-2a insieme a PDF/UA-1**
   (`typst_motore.compila(..., pdfua=True, pdfa="a-2a")`).
2. Se typst rifiuta il PDF/A, ricompila col solo PDF/UA-1 e lo dice
   (`⚠ non è PDF/A`), come fa già per PDF/UA-1.
3. `misura_stampa` e `varianti_stampa` restano come sono: misurano
   l'impaginazione, che il PDF/A non cambia.

## Alternative

- **PDF/A-4**: chiede PDF 2.0 ed è incompatibile con PDF/UA-1 (typst lo
  rifiuta). Si rivaluta quando typst avrà PDF/UA-2.
- **PDF/A-3**: serve per i file allegati, che non ci sono.
- **PDF/A-2b o 2u**: livelli più bassi. La struttura logica che chiede la «a»
  c'è già per PDF/UA-1.
- **Convertire dopo** (Ghostscript `-dPDFA`): rifà il PDF, perde i tag PDF/UA
  ed è un binario in più. Scartata senza misura: typst lo fa alla fonte.

## Misura

20 booklet, main 683480af contro ramo (dettaglio in
`plans/esperimenti/pdfa-2026-11-13/MISURE.md`):
- veraPDF PDF/A-2a: **0/20 → 20/20**, controlli falliti **544 → 0**;
- PDF/UA-1: 20/20 su tutti e due;
- pagine 985 = 985, testo estratto identico in ogni pagina;
- 86 pagine con pixel diversi di al più 3 livelli su 255 (colore sRGB
  dichiarato), invisibili;
- peso dei 20 PDF: 75,2 → 75,3 MB.

## Conseguenze

- Il volume si può depositare in un archivio e si apre uguale fra anni.
- Un booklet che typst non riesce a fare PDF/A esce lo stesso, col solo
  PDF/UA-1, e l'esportatore lo dice.
- La conformità è di macchina (veraPDF): nessuna prova con un archivio vero.
