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
Per una serata, il volume è un pezzo del corredo, e il comando è
`python3 scripts/dm.py corredo <SERATA>.corredo.json --stampa`
(`rumblingstone-automation`, «Il corredo della serata»).

---

## §2 · Le decisioni di impaginazione, già prese

Non si ridiscutono a ogni volume. Se una serve diversa, si cambia **il tema**.

| Elemento | Regola | Perché |
|---|---|---|
| **Tabella** | scavalca le due colonne, in cima o in fondo alla pagina dove è citata, se ha ≥ 4 colonne **o** se in colonna diventa più alta di 1,8 volte quanto sarebbe a tutta pagina (lo misura il tema). Porta con sé il titolo della sezione. L'autore decide con `<!-- tabella: larga -->` o `<!-- tabella: colonna -->` sopra la tabella | in una colonna da 8 cm una tabella a due o tre colonne con frasi va a capo in ogni cella: nei volumi della #169 erano 100 su 125 |
| **Immagine** | orizzontale (larghezza ≥ 1.25 × altezza) → piena larghezza; verticale → dentro la colonna | un'illustrazione ridotta a francobollo non è un'illustrazione |
| **Mappa** | entra in colonna (≤ 48 celle) o va su una **pagina A4 a una colonna**, col suo titolo. Mai a capo, mai rimpicciolita dentro la colonna. Vale per la griglia e per la mappa disegnata verticale | una mappa che va a capo è una fila di simboli; in una colonna da 8 cm una pianta non si legge |
| **Schema o comando largo** | non è una mappa: scende di corpo in colonna fino a 5,5 pt, oltre le 78 celle scavalca le due colonne | una pagina A4 per una riga di `bash` lascia mezza colonna vuota |
| **Riquadro** | `#leggi` = si legge ad alta voce · `#nota` = regia del DM · `#riquadro` = regola opzionale | tre casi diversi che a occhio nudo devono restare diversi |
| **Titolo** | `sticky`: non resta in fondo alla colonna senza il suo testo | è il difetto che si nota per primo sfogliando |
| **Apertura di capitolo** | fregio + titolo a piena larghezza, e un **versale** sul primo paragrafo | dice dove sei prima che tu legga il titolo |
| **Statistiche** | `#statblocco()`, mai prosa ([ADR-0021](../../plans/adr/ADR-0021-statblocchi-machine-readable.md)) | a metà combattimento la CA non si cerca dentro un paragrafo |
| **Margini** | speculari (`inside` 2.0 cm / `outside` 1.5 cm) | rilegato, il margine interno finisce nella piega |
| **Colophon** | `colophon` nel manifest → pagina sul **verso del frontespizio**, senza testatina ([ADR-0023](../../plans/adr/ADR-0023-colophon-di-edizione.md)) | due PDF dello stesso capitolo stampati a un mese di distanza erano indistinguibili sul tavolo |
| **Fondo** | avorio; `--carta bianca` per stampare in casa | sessanta pagine di fondo pieno sono una cartuccia |
| **Formato** | A4 due colonne; `--formato a5` per il libretto, **poi** `--imposto` | imporre un A4 scala il corpo al 71%: si compone in A5 e si piega, non il contrario |

---

## §2-bis · Come si fa un booklet: la tecnica, in ordine

Canone dal 2026-09-25. Mette in fila le regole nate al lavoro sulla serata
della resurrezione (#169) e sul controllo di tutti i volumi che è venuto dopo,
perché il prossimo volume nasca già così invece di essere corretto dopo.

| # | Passo | Dove sta la regola | Chi lo controlla |
|---|---|---|---|
| 1 | **Il master si legge in avanti**: il corpo nell'ordine in cui si gioca, e ogni PNG entra con la sua scheda d'entrata nella scena in cui i PG lo incontrano | `rumblingstone-module-standard`, «Corpo e appendici» | `validate_modules.py` sulle sezioni, il DM sull'ordine |
| 2 | **Statistiche e mappe in appendici** fra `<!-- pagina: una-colonna -->` e `<!-- /pagina -->`, cioè su pagine A4 a una colonna | §4.4 | l'esportatore |
| 3 | **Dove i giocatori ricevono un foglio**, una riga «✉ Si consegna qui» | `rumblingstone-module-standard` | a vista |
| 4 | **Apparato, storia e istruzioni di consegna non vanno in stampa** ([ADR-0069](../../plans/adr/ADR-0069-la-storia-delle-scelte-resta-nel-sorgente.md), [ADR-0070](../../plans/adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md)): i metadati del repo in `<!-- apparato -->`, la storia in `<!-- storico -->`, l'istruzione di consegna in `<!-- consegna -->`; lo stato al tavolo si riscrive come fatto; i rimandi si scrivono `DEF-N` e li traduce l'esportatore | §4.6, §4.8 | `test_storico.py` sui sorgenti; sul PDF `validate_booklets --stampa`, con un tetto per volume in `scripts/apparato-residui.json` |
| 5 | **Una mappa entra in colonna** (≤ 48 celle) **o va su A4**, e non va mai a capo; oltre 110 celle si accorcia l'annotazione | §2, §4.4 | l'esportatore, `TestMappeCheNonEntranoInColonna` |
| 6 | **Ogni capitolo apre una pagina** | il tema, `capitolo-aperto` | automatico |
| 7 | **Un'immagine** fuori da una pagina dedicata resta sotto i 16 cm, su una pagina A4 sotto i 21, **misurando** l'immagine | §4.5 | `TestFiguraSuPaginaCompilata` |
| 8 | **Niente esce dalla colonna**: codice in linea, righe da compilare e tabelle lunghe si sistemano da soli | §4.5 | `TestCioCheEsceDallaColonna` |
| 8-bis | **Una tabella che in colonna va a capo in ogni cella scavalca le due colonne**, da sola; l'autore la forza con `<!-- tabella: larga -->` o `<!-- tabella: colonna -->` | §2, §4.7 | `TestTabelleLargheCompilate` |
| 9 | **Prima di consegnare**: `validate_booklets --stampa`, poi il controllo a vista prima e dopo | §4, «Il controllo a vista» | chi consegna |
| 10 | **Il booklet non esce da solo**: è un pezzo del corredo della serata, con il volume dei fogli ✉, gli echi, le carte e i prompt. «Genera il booklet» vuol dire `dm.py corredo <SERATA>.corredo.json --stampa` | `rumblingstone-automation`, «Il corredo della serata» | `validate_corredo.py`, che misura anche il PDF (sovrapposizioni, margini, box ≤ 12 righe) |

Il passo 10 è la misura del «controllo a vista» di §4 fatta da uno script: le
sovrapposizioni e il testo sul bordo li conta `validate_corredo.py --pdf`, quando
PyMuPDF c'è. Le pagine con le mappe restano da guardare.

I passi 5-8 li fanno il tema e l'esportatore: chi scrive il master non deve
ricordarseli, e se un volume li viola si corregge il tema. I passi 1-4 sono di
chi scrive, e nessuna macchina li fa al posto suo.

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

## §4 · I modi in cui questa catena si è rotta davvero

Sono qui perché sono i primi da cercare quando «il PDF viene male».

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
4. **La mappa che va a capo.** Nel volume della serata del 2026-09-25 le due
   mappe della Sala di `DEF-2`, larghe 72 celle, stavano nel corpo a due
   colonne. Una colonna ne tiene 48: sono uscite a brandelli, e nessun gate se
   n'è accorto perché il PDF compilava. *Sintomo*: una mappa ASCII con le righe
   spezzate in due, o una legenda che scende a pagina dopo.
   → la decisione non è più a mano. `md_to_typ` misura ogni blocco
   preformattato (`larghezza_visiva`, un emoji vale 2,5 celle) e porta su una
   pagina A4 a una colonna, col suo titolo, ogni mappa più larga di
   `CELLE_COLONNA`; il tema (`#griglia`) non la manda mai a capo. Nei master
   la forma buona resta quella esplicita: le mappe in un'appendice fra
   `<!-- pagina: una-colonna -->` e `<!-- /pagina -->`, come `DEF-2`, `DEF-3`
   e `DEF-4`. Una riga oltre `CELLE_PAGINA` (110) scende sotto i 9 pt anche su
   A4, e l'esportatore lo dice: si accorcia l'annotazione, non si stringe la
   mappa. I casi sono in `TestMappeCheNonEntranoInColonna`.
5. **Ciò che esce dalla colonna.** Trovati il 2026-09-25 compilando tutti i
   quindici volumi prima e dopo la regola del punto 4. Tre forme, e due
   c'erano da mesi:
   - un percorso in `codice` o una parola come `PortaleDellaForgiaEterna` è
     una parola sola, non va a capo e si stampa sopra la colonna accanto
     (otto pagine in quattro volumi). → il tema spezza il codice in linea dopo
     `/ _ . -` e fra minuscola e maiuscola;
   - una riga da compilare `______` fa lo stesso (le schede di feedback del
     Drappo). → l'esportatore la spezza ogni otto trattini, e lo fa lui e
     non il tema, perché una regola del tema toccherebbe anche le mappe;
   - una tabella da quattro colonne in su è un float, e un float non si
     spezza: l'indice delle 48 aree dell'Abbazia usciva dal fondo e si
     stampava sopra se stesso. → oltre 30 righe va su una pagina A4 a una
     colonna, dove scorre (`RIGHE_TABELLA_FLOTTANTE`).

   Il punto 4 ne ha portato una quarta: una figura su pagina A4 riservava
   **sempre** 21 cm, anche per una mappa da 16, e la coda della pagina
   scivolava sola alla successiva (una riga a pagina 4 del Palio, un fregio a
   pagina 62). → il tetto si applica misurando l'immagine, come per i 16 cm.
   I casi sono in `TestCioCheEsceDallaColonna` e `TestFiguraSuPaginaCompilata`.
6. **La storia delle scelte in stampa.** «✏️ Allineato il 2026-09-24 su
   decisione del DM», «il box di prima diceva…», `[CANONE — DM 2026-07-31]`, un
   §9 «Cosa è cambiato»: servono nel repo e al tavolo sono rumore. Il
   2026-09-25 erano 257 righe nei quindici PDF. → nel sorgente restano, e le
   due catene le saltano con `dmcore.testo.togli_storico`
   ([ADR-0069](../../plans/adr/ADR-0069-la-storia-delle-scelte-resta-nel-sorgente.md)).
   Chi scrive usa tre forme:

   | Forma | Per |
   |---|---|
   | `<!-- storico -->` e `<!-- /storico -->`, ciascuno su una riga sua | un paragrafo o un riquadro |
   | gli stessi marcatori dentro la riga | una frase o un inciso |
   | `<!-- storico: riga -->` dentro una cella | una riga di tabella, che due marcatori spezzerebbero su GitHub |

   Le attribuzioni di forma fissa (`[CANONE …]`, «(decisione DM data)»,
   `[verif. ✓ …]`, «(ADR-NNNN)») se ne vanno da sole. Quando storia e fatto
   stanno nella stessa frase, la frase vecchia va nel blocco storico e sotto se
   ne scrive una che dice solo il fatto. `test_storico.py` fa da tetto: 15
   righe dichiarate, file per file, e una in più è rossa.

   **Il foglio ✉ non dice quando si consegna.** «Si consegna al risveglio»,
   «Il DM te la consegna dopo che hai scelto», «Da mostrare subito dopo il
   box» sono istruzioni per il DM: stanno nella riga **✉ Si consegna qui** del
   master o nella regia della serata, e sul foglio che il giocatore tiene in
   mano si chiudono fra `<!-- consegna -->` e `<!-- /consegna -->`, con la
   stessa funzione. Prima di chiuderle si controlla che la regia dica tutto
   quello che dicevano. `TestIFogliDeiGiocatori` boccia un capitolo `player`
   che le stampa ancora; non vede «Per il giocatore di…», che su alcuni fogli
   è un'istruzione al giocatore e non al DM.

7. **La tabella che in colonna va a capo in ogni cella.** Fino al 2026-09-25
   scavalcavano le due colonne solo le tabelle da quattro colonne in su. Una
   da due o tre con frasi nelle celle restava in 8 cm e diventava alta il
   doppio: misurate con Typst sui tre volumi della #169, **100 su 125**
   (la peggiore: 22,8 cm in colonna, 6,3 a tutta pagina). → il tema misura la
   tabella in colonna e a tutta pagina, e se il rapporto supera 1,8 la fa
   scavalcare. Nel punto esatto non si può: Typst 0.15 non bilancia le
   colonne, e un blocco a due colonne interrotto a metà pagina riempie solo
   quella di sinistra. La tabella va quindi in cima o in fondo alla pagina
   (`auto`), come in un manuale stampato, e porta una riga col titolo della
   sezione, perché può finire sopra il suo titolo o alla pagina dopo. Su tutti
   i volumi: 330 tabelle larghe, 60% nella stessa pagina del loro testo, 34%
   nella successiva, 6% più lontano. Una da due o tre colonne più alta di
   20 cm a tutta pagina resta in colonna, perché un float non si spezza.

8. **L'apparato di lavoro in stampa** ([ADR-0070](../../plans/adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md)).
   Tolta la storia, nei PDF della serata di ARC-07 restavano 150 occorrenze
   nel booklet e 87 nel volume del −1000: «MASTER DEFINITIVO … Sostituisce e
   fonde», nomi di file, «master #3», «MAI 5e», la didascalia «fonte: X.md»
   in fondo a ogni mappa. Chi scrive usa quattro classi:

   | Classe | In stampa | Chi scrive fa |
   |---|---|---|
   | **A** metadati del repo | mai | l'intestazione del master in un blocco `<!-- apparato -->`, uno per file; un percorso isolato con gli stessi marcatori in linea. La riga del Bestiario, la parentesi di soli percorsi e `*(Fonte: …)*` se ne vanno da sole |
   | **B** storia | mai | `<!-- storico -->`, e sotto il fatto senza storia |
   | **C** stato al tavolo | sì | lo riscrive come fatto: «Quando si gioca», «Com'è il mondo a quel punto» |
   | **D** rimandi | tradotti | scrive `DEF-N §x`, meglio fra parentesi dopo il nome della cosa. L'esportatore lo fa diventare «cap. IV §x» se il master è nel volume, il titolo del master se non c'è |

   E **una pagina si stampa una volta**: i fogli ✉ stanno solo nel volume dei
   giocatori, e lo stesso capitolo non sta in due volumi dello stesso corredo
   (`validate_corredo.py`). Il rilevatore legge il testo del PDF, perché la
   stessa riga si stampa in un volume e non in un altro; ogni volume ha il suo
   tetto, col perché, in `scripts/apparato-residui.json`, e il bersaglio è zero.

### Il controllo a vista, prima di consegnare

Un PDF che compila non è un PDF giusto: il difetto 4 compilava. Prima di
mandare un volume, si guardano **le pagine con le mappe**. Le trova Typst
stesso: una sonda `query(raw.where(block: true))` e `query(image)` in coda a
una copia del `.typ` (dentro il repo, per via di `--root`) dà il numero di
pagina di ogni griglia e di ogni immagine, e
`typst compile --pages N,M --ppi 70` le rende in PNG da guardare.

Quando si tocca il tema o l'esportatore, le pagine da guardare sono tutte, e
non si trovano a occhio. Si compilano i volumi **prima e dopo** la modifica
(il prima da un `git worktree` sul commit di partenza) e si confrontano tre
numeri per volume, leggendo il PDF con PyMuPDF:

| Si conta | Che cosa dice |
|---|---|
| le pagine | un salto grande (il Palio da 52 a 64) chiede di guardare dove |
| le pagine con meno di 120 caratteri di corpo e nessuna immagine | una riga o un fregio rimasti soli |
| le coppie di righe di testo che si sovrappongono, e il testo oltre i 30 pt dal bordo del foglio | ciò che esce dalla colonna, punto 5 |

Il 2026-09-25, su `main` dopo la #169, la terza riga contava 1.474
sovrapposizioni in quattro volumi (1.462 nella sola tabella dell'Abbazia) e
otto pagine oltre il bordo; dopo la correzione, zero e zero. Resta un falso
positivo noto: una parola maiuscola che tocca il bordo della sua cella senza
uscirne (Drappo, pagina 31). PyMuPDF è fra le dipendenze di sviluppo dal 2026-09-25 (AGPL,
si usa senza modifiche per verificare; D7 di `PIANO-CICLO-DI-SESSIONE-E-MENU`),
e `validate_corredo.py --stampa` conta sovrapposizioni e testo sul bordo del
corredo in CI. Sugli altri volumi resta un controllo che si fa a mano: il Drappo
delle schede ne ha 185, fra layout e falsi positivi, e nessuno li ha ancora
guardati.

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
