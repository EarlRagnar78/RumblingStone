# PDF/UA-1 sui booklet — misure del 2026-11-13 (ADR-0129)

Banco: i 19 booklet con manifest (tutti i capitoli, `--all`), compilati con
typst 0.15.2 dal pacchetto PyPI e passati a veraPDF 1.28.2 (greenfield) col
profilo `ua1`. Ricetta e script: `banco_pdfua.py` e `Avvio.java` qui accanto.
Numeri completi, per booklet e per regola: `misure.json`.

## Esito

| | main (837876d6) | ramo |
|---|---:|---:|
| booklet conformi a PDF/UA-1 secondo veraPDF | **0 / 19** | **17 / 19** |
| controlli falliti in totale | **132** | **7** |
| booklet che typst compila con `pdf_standards: ua-1` | 2 / 19 | 19 / 19 |

Controlli falliti per regola (clausola di ISO 14289-1):

| Regola | Che cosa | main | ramo | Di chi era |
|---|---|---:|---:|---|
| 7.3-1 | figura senza testo alternativo | 78 | 0 | nostro: i fregi dei capitoli e i ritratti delle schede PG |
| 7.4.2-1 | un titolo salta un livello | 9 | 0 | nostro: «Chi si incontra in questo capitolo» (`###` sotto il titolo del capitolo) e un `####` sotto `##` nel Palio |
| 5-1 | manca l'identificazione PDF/UA nei metadati XMP | 19 | 0 | di typst fino a 0.13; dalla 0.14 basta chiederlo |
| 7.1-10 | manca `DisplayDocTitle` | 19 | 0 | come sopra |
| 7.21.5-1 | larghezze dei glifi incoerenti nel font | 7 | 7 | **di questa macchina**: vedi sotto |

## Regressioni cercate

- **Misure di stampa** (`misura_stampa.py --tutti --json`, tutte le chiavi di
  tutti i 19 booklet): 0 differenze fra main e ramo.
- **Pixel** (ogni pagina di ogni booklet a 60 dpi, soglia 8 su 255 per
  canale): stesse pagine in tutti i 19 booklet; 15 booklet identici al pixel;
  4 pagine diverse in 3 booklet (Mille anni p. 5, Notte e alba pp. 5 e 7,
  Resurrezione p. 9). Sono pagine d'indice: la voce «Chi si incontra in
  questo capitolo» ora rientra di un livello solo, come vuole la sua
  posizione nel capitolo. Il testo delle pagine è identico.
- **Testo estratto**: il titolo del capitolo esce una volta sola, come prima
  (una prima stesura con un titolo trasparente lo faceva uscire due volte e
  `test_misura_stampa` l'ha visto).
- **Suite**: 2.746 prove in parallelo e 140 in serie, verdi.

## Due configurazioni provate (regola «configurazione rigorosa»)

1. **Titolo trasparente** al posto di `hide(heading(...))`, col titolo
   visibile marcato come artefatto. PDF/UA-1 passa, ma il testo del titolo
   è nel PDF due volte: il titolo invisibile usciva dall'area di stampa nelle
   schede PG (`misura_stampa`: `fuori_margine` 0 → 6) e il titolo del
   capitolo contava due volte nel testo estratto. **Scartata.**
2. **Il titolo visibile è il titolo dei tag** (`titolo-visibile`: fuori
   dall'indice e dai segnalibri, che restano del titolo nascosto), con la
   testatina che legge solo i titoli dell'indice. PDF/UA-1 passa, misure di
   stampa identiche. **Adottata.**

## Cosa resta, dichiarato

- **7.21.5-1, 7 controlli in 2 booklet.** Cinque glifi che i font del repo
  (EB Garamond, Cinzel, Inconsolata) non hanno cadono su Unifont, un font di
  sistema di questa macchina: «⟺» ×3 e «⟶» ×2 a p. 21 e «►» a p. 46 del
  Palio; «🔮» e «🔷» a p. 55 della sessione di Terros (le altre emoji cadono
  su Noto Color Emoji, che veraPDF accetta). È la stessa classe di difetto
  che ADR-0085 ha chiuso per le mappe: il risultato dipende dai font della
  macchina. Non si corregge qui: il Palio sta nella #370, e la scelta
  (sostituire i caratteri nel master o portare un font di simboli nel repo)
  è di contenuto. Su un'altra macchina il numero può essere diverso.
- **veraPDF non va in CI** (le ragioni di costo di ADR-0032 restano: JVM e
  9,5 MB di jar). In CI il cancello è typst stesso: con `pdf_standards: ua-1`
  rifiuta di compilare un titolo che salta un livello o un'immagine senza
  testo alternativo. `scripts/tests/test_pdfua.py` lo tiene.
- **Conformità di macchina, non di lettura.** PDF/UA dice che la struttura è
  quella giusta; non dice che un lettore di schermo legga bene una tabella di
  statistiche. Quello si prova con NVDA o Orca, e qui non è stato fatto.
