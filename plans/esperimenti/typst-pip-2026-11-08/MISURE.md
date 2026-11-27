# typst da PyPI contro la CLI di mise.lock — misura del 2026-11-08

**Perché.** Il 2026-11-08 GitHub Releases ha risposto 504 per ore a typst, pdfcpu e mise (ADR-0113, «Dopo i 504»). Jfs ha chiesto perché non installare typst con pip. Ha scelto: «Prova pip in testing, poi decidi». Regola del progetto: lo standard di fatto resta finché una misura non lo boccia, e si cambia solo se l'uscita non peggiora.

**Cosa si confronta.**
- **A:** la CLI ufficiale `typst` 0.15.1 da `mise.lock` (sha256 29273eaa…).
- **B:** il pacchetto PyPI `typst` 0.15.2 ([messense/typst-py](https://github.com/messense/typst-py), Apache-2.0). È un binding Python che incorpora il compilatore. La wheel `cp39-abi3-manylinux2014_x86_64` ha sha256 `99fe0916…87a1`.
- Il `Creator` nei PDF di B è «Typst 0.15.1»: la 0.15.2 è la versione del binding, il compilatore dentro è lo stesso della CLI.

**Come.** Lo script è [`misura_typst_pip.py`](misura_typst_pip.py), che gira anche in CI nel job `typst-pip` (testing, non bloccante).
1. Per ognuno dei 19 manifest dei booklet si esegue `export_booklet_typst.py --all --keep-typ`, che compila con la CLI.
2. Lo stesso `.typ` si ricompila con `typst.compile()`, con stessi font, radice, pacchetti e `SOURCE_DATE_EPOCH`.
3. PyMuPDF confronta pagine, testo per pagina e pixel per pagina (72 dpi in grigio).

## Esito nel container (Python 3.13, linux-x64)

| misura | esito |
|---|---|
| booklet | 19, tutti compilati con A e con B |
| pagine | 856 da una parte e dall'altra |
| testo diverso | 0 pagine |
| pixel diversi a 72 dpi | 0 pagine |
| pixel diversi a 150 dpi (3 booklet: SERATA-RESURREZIONE 172 pp, DRAPPO-BOOKLET-DM 87, giardino PF1e 25) | 0 pagine |
| byte identici | 1 su 19. Gli altri cambiano solo nella compressione Flate delle immagini: stessi pixel, oggetti di lunghezza diversa |
| `typst eval` con la query dei riquadri di `misura_stampa` (SERATA-RESURREZIONE) | 60 segnaposti, identici |
| CLI deterministica (due compilazioni) | sì, 19 su 19 |
| tempo di compilazione | la CLI ~51 s in tutto, B ~35 s (in processo, senza avviare un binario) |

Rapporto completo: [`esito-container.json`](esito-container.json).

## Decisione

Letta la misura, il DM ha scelto «applicalo se funziona come standard»: [ADR-0116](../../adr/ADR-0116-typst-si-installa-da-pypi.md). Il punto «il codice» qui sotto è fatto (`scripts/typst_motore.py`), e senza la CLI passano in locale tutti i cancelli di stampa della CI.

## Cosa NON dice ancora

- **La CI.** Il job `typst-pip` ripete la misura sui runner a ogni PR: è il controllo che resta acceso dopo la scelta.
- **macOS e Windows.** Sono misurati solo su linux-x64. Esistono wheel per macOS e Windows, ma non sono provate.
- **Il bundle.** Senza binario typst, il bundle del rilascio porterebbe la wheel al posto dell'archivio. Va rifatto e rimisurato.
- **pdfcpu.** Non è su PyPI, quindi resta comunque a mise e GitHub Releases.
- **Il rischio.** typst-py è di un manutentore singolo, molto usato, ma non dell'organizzazione typst. Se smette di seguire i rilasci, si torna alla CLI, che resta in `mise.lock`.

## Seguito (2026-11-08): l'imposizione con pdfimpose, e mise esce

Scelta del DM sulla card «Misura pdfimpose, poi decidi». Su tutti i 19 booklet
A5 del repo (1.590 pagine), `pdfcpu booklet` v0.11.0 contro `pdfimpose saddle`
2.10.0, con [`confronta_imposizione.py`](confronta_imposizione.py); righe in
[`esito-imposizione.txt`](esito-imposizione.txt):

- **stesse coppie di pagine** su ogni mezza facciata in 19 booklet su 19,
  Jaccard minimo 0,99;
- stesso foglio fisico A4: pdfcpu lo scrive verticale (595 × 842 pt, pagine una
  sopra l'altra), pdfimpose con `--signature 2x1` orizzontale (839,1 × 595,3 pt,
  pagine affiancate), A5 a grandezza vera;
- con `--format A4` (la prima prova, quella del file di esito) pdfimpose
  ingrandisce le pagine dell'1,4% (851 × 599,7 pt): `dm.py` usa `--signature 2x1`;
- due esecuzioni di pdfimpose non danno gli stessi byte, come pdfcpu.

Il bundle offline (`scripts/bundle_offline.py`) è stato costruito per
linux-x64 (28 wheel, ~150 MB: PyMuPDF 2.x porta onnxruntime) e installato in un
`.venv` vuoto senza proxy: `import typst, pdfimpose` riuscito. Le note qui sopra
su `typst-pip`, sul bundle e su pdfcpu valgono per la prima parte: dopo
ADR-0116 seconda parte il job `typst-pip` non c'è più, perché la CLI non è più
fissata da nessuna parte.
