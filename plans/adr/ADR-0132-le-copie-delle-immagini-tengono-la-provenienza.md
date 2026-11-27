# ADR-0132 — Le copie delle immagini tengono la dichiarazione di provenienza

**Stato**: proposta (2026-11-13)
**Data**: 2026-11-13
**Decisione-fonte**: il DM (Jfs), 2026-11-13: tecniche di AI generativa e document AI con gli standard di fatto, misurate («continua con le prossime che mancano e che misurate migliorano»).
**Rapporti**: estende [ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md) (ogni immagine generata ha la sua riga in `PROVENIENZA.txt`) dalle righe di testo ai file. Non tocca i master ([ADR-0003](ADR-0003-markdown-master-layout-generati.md): la copia `web/` è un artefatto).

## Contesto

28 master del repo portano un manifesto C2PA firmato da chi li ha generati
(Google, OpenAI), con dentro la «sorgente digitale» IPTC: è il modo standard
di dire che un'immagine è fatta da un modello. Nei booklet però non vanno i
master: vanno le copie leggere di `web/`, che `build_image_derivatives`
ricomprime. La dichiarazione si perdeva lì: 0 copie su 28 la tenevano, e 0
immagini su 89 nei PDF.

## Decisione

1. `scripts/provenienza_immagini.py` legge la sorgente digitale dal manifesto
   C2PA del master e la scrive nella copia JPEG come XMP, campo
   `Iptc4xmpExt:DigitalSourceType` (IPTC Photo Metadata), insieme al nome e
   allo SHA-256 del master.
2. La copia **non si ricomprime**: si aggiunge un segmento al file, i pixel
   restano identici.
3. **Non si indovina**: senza manifesto firmato nel master la copia resta
   senza etichetta, e un'etichetta che il master non giustifica è un errore.
4. `build_image_derivatives` la mette da sé quando rigenera una copia.
5. Cancello: `provenienza_immagini.py --check`, dentro
   `scripts/tests/test_provenienza_immagini.py`.

## Alternative

- **Firmare le copie con C2PA** (`c2pa-python`): è lo standard pieno, ma chiede
  un certificato di un'autorità nella lista di fiducia C2PA. Con uno fatto in
  casa i lettori dicono «non fidato»: peggio di un'etichetta onesta non
  firmata. Scartata.
- **Copiare il manifesto del master nella copia**: il manifesto firma i byte
  del master; su un file ricompresso risulta manomesso. Scartata.
- **Solo `PROVENIENZA.txt`**: c'è già, ma non viaggia col file né col PDF.
- **Etichettare anche le immagini senza manifesto**: sarebbe una
  dichiarazione che nessuno ha firmato. Resta al DM.

## Misura

Dettaglio in `plans/esperimenti/provenienza-immagini-2026-11-13/MISURE.md`:
- copie con master firmato che dichiarano la sorgente: **0/28 → 28/28**;
- immagini JPEG nei 20 booklet PDF che la dichiarano: **0/89 → 36/89**, in 8
  booklet (i cinque del Drappo al completo);
- pixel delle 52 copie: identici; pagine dei booklet: 985 = 985.

## Conseguenze

- Chi estrae un'immagine da un booklet, o la apre con uno strumento che legge
  i metadati IPTC, vede che è generata e da quale master viene.
- 24 copie su 52 restano senza etichetta perché l'origine non è firmata: lo
  strumento le conta a ogni corsa.
- L'etichetta nella copia non è firmata: la prova resta il master.
