# Emoji e simboli del volume dai font del repo — misure del 2026-11-13 (ADR-0130)

Banco: i 20 booklet con manifest (tutti i capitoli, `--all`), esportati con
`export_booklet_typst.py` su main 43d42b96 e sul ramo (le pagine dei booklet
non cambiano su 4fdbd914), poi veraPDF 1.28.2 profilo `ua1` (ricetta in
`../pdfua-2026-11-13/`), il confronto al pixel e `misura_stampa --tutti --json`.
Numeri per booklet: `misure.json`.

## Esito

| | main | ramo |
|---|---:|---:|
| booklet conformi a PDF/UA-1 (veraPDF) | **18 / 20** | **20 / 20** |
| controlli falliti | **7** (7.21.5-1: Unifont nel Palio e in Terros) | **0** |
| font di sistema nei PDF | FreeSans, Inter, Liberation Serif, Unifont, Noto Color Emoji | **nessuno** |
| pagine | 985 | 985, uguali in ogni booklet |

Il conto di ADR-0129 diceva 19 booklet: il banco saltava
`ARC07-NOTTE-E-ALBA-SERATA`, che era già conforme. Su 20 la base è 18.

I caratteri fuori da EB Garamond, Cinzel e Inconsolata erano 80, con 3.172
occorrenze (`/mnt/project-files/glifi-2026-11-13/glifi.json`, fuori dal repo).
Sul ramo escono così:
- le 67 emoji da **Noto Color Emoji**, nel repo: sono le stesse bitmap di prima;
- i 13 simboli che non sono emoji (⬦ ☐ ► ▸ ◂ ✦ ① ② ③ ④ ★ ⟺ ⟶) dai font che
  typst porta con sé: New Computer Modern Math, Libertinus, DejaVu Sans Mono.

## Che cosa cambia sulla pagina

- **Ogni pagina**: il piè di pagina «⬦ n ⬦» e il segno di fine paragrafo
  «⬦» passano da FreeSans a New Computer Modern Math. È lo stesso rombo vuoto,
  con un tratto un po' diverso.
- **83 pagine su 985** cambiano anche sopra il piede, e in 69 di queste una
  riga si sposta di meno di un punto. Viene da ► (49 volte: da Inter, un
  triangolo pieno, a New Computer Modern Math, una freccia più sottile) e
  da ⬦ e ☐ nel testo. Nessuna pagina in più o in meno.
- **Mappe SVG**:
  - le etichette del Palio con «▸» (piazza del Palio, Channathgate, rotta del
    soccorso) chiedono «Georgia, serif». Prima uscivano intere in FreeSans,
    ora escono in un serif;
  - nella legenda della mappa T-3 di Terros «🔮» e «🔷» erano bitmap in bianco
    e nero di Unifont, ora sono a colori;
  - la legenda della Sala della Forgia (ARC-07) è uguale.
- **`misura_stampa`** (che compilava già con i soli font del repo): 1 chiave di
  stampa diversa, `immagini_basse` di Resurrezione, dove la prima immagine
  segnalata passa da p. 59 a p. 60. Su main la sua compilazione non aveva le
  emoji, e la sua impaginazione differiva da quella vera di uno o due righi;
  ora le due coincidono, e nel volume esportato l'immagine sta a p. 60 sia su
  main sia sul ramo. Cambiano di poco anche le parole e le parole ripetute
  (±5 parole per booklet, le emoji ora sono nel testo estratto).

## Configurazioni scartate (regola «configurazione rigorosa»)

1. **Noto Color Emoji vettoriale** (COLRv1, 5 MB, Google Fonts senza la
   tabella SVG): nel testo va bene, ma nelle immagini SVG typst non disegna i
   glifi COLR. «⏳» spariva dalla legenda della Sala della Forgia, e Ritorno
   alla Forgia e Resurrezione uscivano non conformi (glifo `.notdef`).
2. **Noto Sans Symbols 2** per i 13 simboli: ha anche le lettere latine, e
   nelle SVG del Palio typst rendeva intere etichette in quel sans, con le cifre
   prese da un altro font («DC 2 4»). Ridotto ai soli simboli, rompeva «⏳»
   nelle SVG. I font interni di typst coprono già i 13 simboli: non serve.
3. **Altri font a colori** (prova di copertura e veraPDF su una pagina, non su
   20 booklet): Twemoji Mozilla (font OFL, disegni CC BY 4.0, 1,4 MB) passa
   veraPDF ma cambia lo stile e chiede l'attribuzione; OpenMoji (CC BY-SA 4.0)
   non è compatibile con la CC BY-NC-SA del repo; Fluent (MIT) non esiste come
   font; Blobmoji non è aggiornato. Tavola visiva:
   `/mnt/project-files/glifi-2026-11-13/FONT-EMOJI-A-COLORI-CONFRONTO.pdf`.

## Cosa resta, dichiarato

- 11 MB in più nel repo.
- La scelta di stile (icone game-icons.net o Material al posto delle emoji) è
  aperta al DM, con una pagina di prova; non è in questa misura.
- Conformità di macchina, non di lettura: nessuna prova con un lettore di
  schermo.
