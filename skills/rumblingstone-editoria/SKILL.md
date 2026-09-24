---
name: rumblingstone-editoria
description: >
  Il mestiere del layout designer e del tipografo applicato ai volumi di
  RumblingStone: quando una tabella scavalca le due colonne, quando un'immagine
  è a piena larghezza, quale dei tre riquadri si usa (read-aloud, regia DM,
  regola opzionale), come si fa un blocco statistiche, e soprattutto **dove si
  tocca** — nel tema, mai nel `.typ` generato. Use WHENEVER si impagina, si
  genera o si corregge un booklet o un PDF: "booklet", "manifest",
  "impaginazione", "edizione da stampa", "il PDF viene male", "la tabella si
  spezza", "l'immagine è piccola", "capolettera", "font", "tipografia",
  "segnalibri", "copertina", "carta bianca", "typst", "tema", "validate_booklets",
  "stampa la sessione", "PDF per i giocatori", "statblocco in stampa".
---

# RumblingStone — Editoria

L'art direction ([`rumblingstone-art-direction`](../rumblingstone-art-direction/SKILL.md))
decide **cosa** si vede. Questa skill decide **come sta sulla pagina**. È il
mestiere che nel repo vive dentro un tema Typst di trecento righe, e che prima
del 2026-08-22 non era scritto da nessuna parte: il risultato è che due booklet
della campagna erano rimasti inservibili per settimane senza che nessuno lo
sapesse.

> **La riga da ricordare**: il markdown è il libro, il `.typ` è un artefatto.
> Se ti trovi a correggere a mano un file generato, stai correggendo il posto
> sbagliato — la correzione va nel tema o nel convertitore, altrimenti alla
> prossima rigenerazione sparisce.

---

## §1 · Le due catene, e quale usare

| Serve… | Catena | Comando |
|---|---|---|
| leggere a schermo, mandarlo nel gruppo, impaginare altrove | **HTML** (ADR-0013) | `python3 scripts/build_booklet_html.py M.manifest.json` |
| **il volume**: un file, segnalibri, tipografia embedded, stampa | **Typst** (ADR-0020) | `python3 scripts/export_booklet_typst.py M.manifest.json --all` |
| una pagina sola a un giocatore | HTML → stampa dal browser | `export_booklet_pdf.py` |
| una scheda a testa, senza bruciare i segreti degli altri | Typst | `… --per-scheda` |

Le due catene leggono **lo stesso manifest**. Non si sostituiscono: un booklet
HTML si apre ovunque e un PDF no.

**Prima di consegnare qualsiasi cosa**: `python3 scripts/validate_booklets.py --stampa`.

---

## §2 · Le decisioni di impaginazione, già prese

Non si ridiscutono a ogni volume. Se una serve diversa, si cambia **il tema**.

| Elemento | Regola | Perché |
|---|---|---|
| **Tabella** | ≥ 4 colonne → scavalca le due colonne | in una colonna da 8 cm si spezzano perfino le parole del titolo |
| **Immagine** | orizzontale (larghezza ≥ 1.25 × altezza) → piena larghezza; verticale → dentro la colonna | un'illustrazione ridotta a francobollo non è un'illustrazione |
| **Riquadro** | `#leggi` = si legge ad alta voce · `#nota` = regia del DM · `#riquadro` = regola opzionale | tre casi diversi che a occhio nudo devono restare diversi |
| **Titolo** | `sticky`: non resta in fondo alla colonna senza il suo testo | è il difetto che si nota per primo sfogliando |
| **Apertura di capitolo** | fregio + titolo a piena larghezza, e un **versale** sul primo paragrafo | dice dove sei prima che tu legga il titolo |
| **Statistiche** | `#statblocco()`, mai prosa ([ADR-0021](../../plans/adr/ADR-0021-statblocchi-machine-readable.md)) | a metà combattimento la CA non si cerca dentro un paragrafo |
| **Margini** | speculari (`inside` 2.0 cm / `outside` 1.5 cm) | rilegato, il margine interno finisce nella piega |
| **Colophon** | `colophon` nel manifest → pagina sul **verso del frontespizio**, senza testatina ([ADR-0023](../../plans/adr/ADR-0023-colophon-di-edizione.md)) | due PDF dello stesso capitolo stampati a un mese di distanza erano indistinguibili sul tavolo |
| **Fondo** | avorio; `--carta bianca` per stampare in casa | sessanta pagine di fondo pieno sono una cartuccia |
| **Formato** | A4 due colonne; `--formato a5` per il libretto, **poi** `--imposto` | imporre un A4 scala il corpo al 71%: si compone in A5 e si piega, non il contrario |

---

## §3 · Dove si tocca cosa

```
manifest.json ──┬─► build_booklet_html.py ──► .html + .hb.md
                └─► export_booklet_typst.py ─► .typ ──► typst ──► PDF
                          │                     ▲
                          │                     └── scripts/typst/tema-rumblingstone.typ
                          └── scripts/typst/scheda-pg.typ   (capitoli "layout": "schede")
```

- **la forma di un elemento** (colori, spaziature, un riquadro nuovo) →
  `scripts/typst/tema-rumblingstone.typ`;
- **come il markdown diventa quell'elemento** (una sintassi nuova) →
  `md_to_typ()` in `scripts/export_booklet_typst.py`;
- **quali capitoli, con che copertina** → il manifest, che ha un contratto:
  `scripts/schemas/booklet_manifest.schema.json`;
- **i crediti, la licenza, la versione e la data** → la chiave `colophon` del
  manifest. ⚠️ **La data si scrive lì e non si deduce mai**: un volume che la
  prende dall'orologio cambia a ogni compilazione e smette di essere
  byte-identico, che è la proprietà su cui poggia il gate di stampa in CI.
  L'ordine delle voci è fisso e **identico nelle due catene** (`VOCI_COLOPHON`),
  e un test lo verifica: crediti ordinati diversamente sono due edizioni diverse;
- **i caratteri** → `scripts/fonts/` (mai un font di sistema: il PDF cambierebbe
  faccia altrove). Il nome del font si dichiara una volta sola, in cima al tema.

---

## §4 · I tre modi in cui questa catena si è rotta davvero

Sono qui perché sono i tre da cercare per primi quando «il PDF viene male».

1. **La sintassi che cade in un'altra regola.** La sintassi dell'immagine finiva nella regola
   dei link e usciva stampato come `!alt`: tredici righe nel booklet del Palio.
   *Sintomo*: nel PDF compare un testo che nel master era altro.
   → si guarda l'ordine delle regole in `md_to_typ`.
2. **Il delimitatore che dipende dal contesto.** `**Seggio**/Deputazione` chiudeva
   male e Typst rispondeva «unclosed delimiter» — a trecento righe di distanza.
   *Sintomo*: un errore di compilazione che indica un punto innocente.
   → l'enfasi si emette come `#strong[...]`, mai come `*...*`. Non tornare
   indietro «perché è più leggibile»: il `.typ` è un artefatto, non lo legge
   nessuno.
3. **Il gate che non c'era.** Nessuno compilava in CI, quindi due booklet erano
   rotti da settimane. *Sintomo*: nessuno — ed è il punto.
   → qualunque cosa aggiungi al tema, aggiungi **il caso** a
   `scripts/tests/test_booklets.py`, e ricorda che `validate_booklets --stampa`
   è ciò che rende vera la frase «funziona».

---

## §5 · Il livello editoriale: dove siamo e cosa manca

Il riferimento è un manuale stampato (Paizo / Wizards), non una pagina web.
L'audit del 2026-08 ha misurato il divario voce per voce; quello che **resta**
fuori è dichiarato, non dimenticato:

Chiuso il 2026-09-02 (lotto B del `PIANO-CHIUSURA-CATENA-EDITORIALE`): **il
colophon**, che era il divario più grosso — i volumi uscivano anonimi, senza
licenza, senza data e senza versione. Restano fuori:

- **capolettera annegato** (il testo che scorre attorno alla lettera): il tema usa
  un versale. Farlo annegato richiede il pacchetto `droplet`, che Typst scarica
  dalla rete: prima va deciso se si vendorizzano i pacchetti nel repo;
- **imposizione** (A5 piegato su A4, punto metallico): richiede uno strumento che
  manipoli un PDF già fatto, cioè una dipendenza nuova da decidere;
- **indice analitico**: richiede una convenzione di marcatura nei master;
- **CMYK / PDF-X**: rinuncia dichiarata in ADR-0020 — si riapre il giorno di una
  tiratura vera, e quel giorno si valuta Scribus.

Non trattarli come lavoro «da fare quando c'è tempo»: sono **decisioni**, e
ognuna ha già scritto dove va presa.

---

## §6 · Quando NON impaginare

- Un master che cambia ancora ogni sera: si impagina **prima della sessione**, non
  durante la scrittura. Ogni PDF generato a metà è un file che qualcuno stamperà.
  🔎 Da ADR-0023 questa regola morde meno: con `versione` e `data` sul colophon,
  chi ha in mano una stampa vecchia **lo vede scritto**. Impaginare un master vivo
  resta sconsigliato, ma non è più cieco.
- Un booklet con dentro le note del DM da mandare ai giocatori: senza `--all` esce
  solo ciò che è marcato `player`, ed è così che deve restare.
- Le sei schede pregenerate in un fascicolo unico da girare nel gruppo: brucia i
  segreti di tutti insieme. `--per-scheda`, uno a testa.
