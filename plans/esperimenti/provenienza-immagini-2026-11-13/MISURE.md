# L'etichetta di provenienza nelle copie delle immagini — misure del 2026-11-13 (ADR-0132)

Banco: le 52 copie `web/*.jpg` tracciate nel repo (Drappo, ARC-07, PG) e i 20
booklet esportati con `export_booklet_typst.py --all` su main 683480af e sul
ramo. Script: `python3 scripts/provenienza_immagini.py --json` per le copie,
`conta_nei_pdf.py` per le immagini JPEG dentro i PDF. Numeri: `misure.json`.

## Esito

| | main | ramo |
|---|---:|---:|
| copie `web/` il cui master ha un manifesto C2PA firmato | 28 / 52 | 28 / 52 |
| di queste, copie che dichiarano la sorgente digitale IPTC | **0 / 28** | **28 / 28** |
| immagini JPEG nei 20 booklet PDF che la dichiarano | **0 / 89** | **36 / 89** |
| booklet con almeno un'immagine etichettata | 0 | 8 |
| copie con pixel diversi dopo l'etichetta | | 0 / 52 |
| pagine dei 20 booklet | 985 | 985 |

Le 28 etichette: 23 `trainedAlgorithmicMedia` (generata da un modello: i 20
master del Drappo, firmati Google, e 3 ritratti di Hella, firmati OpenAI) e
5 `compositeWithTrainedAlgorithmicMedia` (i ritratti di Durik: il manifesto
Google dichiara una composizione con parti generate).

I cinque booklet del Drappo hanno tutte le immagini etichettate (33 su 33).
Nei booklet di ARC-07 solo 3 su 56.

## Le 24 copie senza etichetta

Restano senza, e lo strumento lo dice:
- 20 di ARC-07: i master sono WebP o PNG senza manifesto. `PROVENIENZA.txt`
  dell'arco dichiara che di molte non si conosce lo strumento;
- 4 ritratti dei PG (Artemis, Hella, Thorick, Tordeck): master WebP senza
  manifesto.

Scriverci «generata» sulla base di una riga di testo, o a occhio, sarebbe una
dichiarazione che nessuno ha firmato. Se il DM sa come sono nate, si può
aggiungere una seconda fonte dichiarata (una riga di `PROVENIENZA.txt` con una
forma fissa): è una sua scelta, non di questo strumento.

## Cosa resta, dichiarato

- L'etichetta nella copia **non è firmata**: è un XMP che chiunque può
  togliere o cambiare. La prova resta il manifesto C2PA del master, e l'XMP
  porta il nome e lo SHA-256 del master per ritrovarlo.
- Firmare le copie con C2PA (`c2pa-python`) chiede un certificato emesso da
  un'autorità nella lista di fiducia C2PA; con un certificato fatto in casa i
  lettori la segnano come non fidata. Scartata.
- La lettura del manifesto cerca i termini IPTC nei byte: non verifica la
  firma crittografica. Per quello serve `c2pa-python` o `c2patool`.
- Nel PDF l'etichetta sta dentro i dati JPEG dell'immagine (typst incorpora il
  JPEG così com'è): la si rilegge estraendo l'immagine, non dalle proprietà
  del PDF.
