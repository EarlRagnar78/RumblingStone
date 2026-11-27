# ADR-0130 — Le emoji del volume da stampa vengono dal repo

**Stato**: proposta (2026-11-13)
**Data**: 2026-11-13
**Decisione-fonte**: il DM (Jfs), 2026-11-13: vuole la versione a colori, con i font importati nel repo «se le licenze sono compatibili», e i font e le emoji che la community usa come standard di fatto, «che non hanno problemi con typst e veraPDF».
**Rapporti**: chiude il residuo di [ADR-0129](ADR-0129-il-volume-da-stampa-e-pdf-ua-1.md) (7 controlli 7.21.5-1 in 2 booklet). Estende all'esportatore la regola di [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) (i font della stampa stanno nel repo), già applicata da `misura_stampa` e `varianti_stampa`. È lo stesso difetto che [ADR-0085](ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md) ha chiuso per le mappe.

## Contesto

I font del repo (EB Garamond, Cinzel, Inconsolata) non hanno emoji né simboli.
Misura su main, 20 booklet: **80 caratteri, 3.172 occorrenze** escono da un
font della macchina che compila. Su questa macchina sono Noto Color Emoji
(emoji a colori), FreeSans e Inter (simboli) e Unifont (bitmap di ripiego). Sul
PC del DM i font di sistema sono altri, quindi il volume cambia faccia da una
macchina all'altra. Unifont è la causa dei 7 controlli che lasciavano non
conformi a PDF/UA-1 il Palio e la sessione di Terros.

## Decisione

1. **Noto Color Emoji entra in `scripts/fonts/`**, con la sua licenza OFL 1.1.
   È la versione bitmap (CBDT) del pacchetto Debian `fonts-noto-color-emoji`
   2.051 (trixie), che è anche il font che dava i colori finora.
2. **`export_booklet_typst` compila con i soli font del repo**
   (`solo_font_del_repo=True`). Si aggiungono quelli che typst porta con sé:
   Libertinus, New Computer Modern (con Math) e DejaVu Sans Mono.
3. Nessun altro font: i 13 simboli che non sono emoji (⬦ ☐ ► ▸ ◂ ✦ ① ② ③ ④ ★ ⟺ ⟶)
   li coprono già i font interni di typst. Restano nel colore del testo, come
   prima.

## Alternative misurate

- **Noto Color Emoji vettoriale (COLRv1, 5 MB, Google Fonts)**: nel testo va
  bene, ma dentro le SVG typst non disegna i glifi COLR. ⏳ sparisce dalla
  legenda di una mappa di ARC-07 e il booklet esce non conforme. **Scartata.**
- **Noto Sans Symbols 2** (OFL) per i simboli: copre anche il latino, e nelle
  SVG del Palio typst rendeva intere etichette in quel sans, con le cifre da un
  altro font. Ridotto ai soli simboli rompeva ⏳ nelle SVG. Non serve:
  **scartato**.
- **Twemoji Mozilla** (font OFL, disegni CC BY 4.0, 1,4 MB): passa veraPDF, ma
  cambia lo stile e chiede l'attribuzione nel colophon. **OpenMoji** (CC BY-SA
  4.0): share-alike non compatibile con la CC BY-NC-SA del repo. **Fluent**
  (MIT): non esiste come font. **Blobmoji**: non aggiornato.
- **Icone al posto delle emoji** (game-icons.net, Material Symbols, Phosphor):
  è una scelta di stile, non di conformità, e la decide il DM, dopo averla
  vista su una pagina di prova (fuori dal repo).

## Misura

20 booklet, main contro ramo (dettaglio in
`plans/esperimenti/glifi-2026-11-13/MISURE.md`):
- veraPDF PDF/UA-1: **18/20 → 20/20**, controlli falliti **7 → 0**;
- font di sistema nei PDF: 5 → **0**;
- pagine: 985 in tutti e due, uguali in ogni booklet;
- 83 pagine su 985 cambiano sopra il piede (► e ⬦ da New Computer Modern
  Math), e in 69 una riga si sposta di meno di un punto;
- `misura_stampa`: una sola chiave di stampa cambia, `immagini_basse` di
  Resurrezione, p. 59 → p. 60. Ora misura con la stessa impaginazione
  dell'export, dove l'immagine sta a p. 60 sia su main sia sul ramo;
- mappe SVG viste a occhio: la legenda della Sala della Forgia (ARC-07) non
  cambia; nella mappa T-3 di Terros 🔮 e 🔷 passano dal bianco e nero di
  Unifont al colore; nel Palio le etichette con ▸ passano da FreeSans al
  serif che la SVG chiede.

## Conseguenze

- Il volume è uguale su ogni macchina che ha il repo: nessuna emoji né simbolo
  esce più da un font di sistema.
- Il repo pesa 11 MB in più. La versione vettoriale ne pesa 5, ma rompe le SVG
  (vedi sopra); si rivaluta quando typst disegnerà i glifi COLR nelle SVG.
- Le emoji nel PDF sono bitmap a 136 px: a 9-10 pt di corpo sono più fini di
  quanto stampi una laser a 600 dpi.
- Un'emoji che Noto Color Emoji non ha (una nuova di Unicode) non esce: typst
  la segnala, e l'esportatore stampa «non è PDF/UA-1».
