# ADR-0032 — Misurare la leggibilità, e perché veraPDF resta fuori dalla CI

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: lotto **G2** di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md)
**Riguarda**: [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md)
(i segnalibri) · [ADR-0028](ADR-0028-abbazia-master-markdown.md) (dove i salti di
titolo sono nati)

## Contesto

Le due catene controllano che un volume **compili**. Nessuna controlla che sia
**leggibile**, e sono cose diverse: un exit code zero non dice niente su una
colonna troppo stretta, su un albero dei segnalibri rotto o su una mappa in cui
il rosso del pericolo e il bruno del terreno sono lo stesso colore per una persona
su dodici.

## Decisione

**`scripts/validate_tipografia.py`** — tre misure, stdlib, non bloccante alla
prima passata come `validate_lingua`.

### 1. Gerarchia dei titoli

Un `h4` sotto un `h2` salta l'`h3`: nei **segnalibri del PDF** — che sono la
ragione per cui ADR-0020 esiste — diventa un ramo dell'albero che non esiste.

**Il perimetro è la decisione.** La prima passata segnalava **142** salti su tutto
il markdown del repo, compresi i `#####` dei `.hb.md`, che nello stile Homebrewery
sono **etichette piccole e non titoli**: punirli avrebbe voluto dire punire una
convenzione, che è il difetto in cui questo repo è già inciampato due volte. Il
controllo guarda solo i **capitoli dichiarati da un manifest**, perché un file che
non entra in nessuna catena non ha segnalibri. Da 142 a **4**.

Tre dei quattro sono handout-oggetto (`PROP-*`: un contratto, una pagina di
registro, un decreto) dove un `######` è un espediente grafico che imita il
documento vero. Restano **segnalati e non esentati**: sembrano deliberati, ma è
una chiamata del DM, non mia, e un'esenzione silenziosa è il modo in cui un gate
smette di trovare i difetti veri.

### 2. Caratteri per riga

45-75 per colonna è la finestra classica: sotto, il testo si legge a singhiozzi;
sopra, l'occhio perde la riga di ritorno.

**Non si stima: si calcola.** Larghezza di colonna dal tema (A4 meno i margini
speculari, meno la gronda, diviso due) e **avanzate reali dei glifi**, lette con
`struct` dalle tabelle `head`, `cmap` e `hmtx` del font che stiamo davvero
incorporando, su un campione di **prosa italiana del repo** — non un pangramma,
perché le frequenze contano.

**Esito: 62,1 caratteri per riga.** Il tema era giusto; adesso è *misurato*, e un
font cambiato o un corpo ritoccato lo sposteranno sotto gli occhi di qualcuno
invece che in copisteria.

### 3. Daltonismo

Circa un uomo su dodici non distingue rosso e verde. Si simulano le tre
dicromazie (Viénot/Brettel, via LMS) e si cercano le coppie **distinte in visione
normale** che sotto una dicromia collassano. I risultati sono raggruppati per
coppia di colori e non per file: le tavole condividono la palette, e senza
raggruppare la stessa coppia esce dodici volte — che è il modo in cui un gate
utile si fa disattivare.

**Esito: 21 coppie, e una che si ripete.** L'alizarina `#c0392b` — il rosso dei
marcatori di pericolo — collassa sui **bruni del terreno** in protanopia (Δ62 →
Δ18) su cinque tavole, e sulle **tinte pergamena** in tritanopia. Su una mappa da
battaglia i marcatori rossi sono la cosa più densa d'informazione che ci sia.

## veraPDF: valutato, fatto funzionare, e lasciato fuori

Il piano lo chiedeva. È stato **procurato e messo in funzione davvero** — Maven
Central, `greenfield-apps` 1.28.2, più una classe Java di avvio, perché il fat jar
**non registra da sé il proprio provider** e la CLI muore con *«No provider with
URI:http://foundry.verapdf.org#default»*.

Sul volume dell'Abbazia, PDF/UA-1: **FAIL**, tre rilievi.

| Rilievo | Di chi è |
|---|---|
| **7.4.2-1** «Heading level 3 is skipped» ×3 | **nostro** — ed è lo stesso difetto che il controllo §1 trova nel markdown, sugli **stessi tre punti**. Due misure indipendenti, stesso numero |
| **5-1** manca lo schema XMP di identificazione PDF/UA | **di Typst**: non è emesso, e dal tema non lo si aggiunge |
| **7.1-10** manca `ViewerPreferences /DisplayDocTitle` | **di Typst**: `set document(title:)` c'è, ma la CLI 0.15.1 non espone le ViewerPreferences |

**Decisione: non entra in CI.** Non per pigrizia — gira, e sopra c'è il suo
referto. Perché:

1. **l'unico rilievo azionabile lo troviamo meglio prima.** Il controllo sulla
   gerarchia lo trova nel **master markdown**, dove si corregge; veraPDF lo trova
   nel PDF, dove non si corregge;
2. **gli altri due non sono nostri** e resterebbero rossi per sempre — cioè un
   gate che nessuno guarda più;
3. **il costo non è quello di un binario**: JVM, 9,5 MB di jar e una classe di
   avvio scritta da noi. ADR-0020 ha accettato `typst` e ADR-0027 `pdfcpu` perché
   erano *un eseguibile statico*. Questo non lo è.

Si rivaluta quando Typst emetterà l'identificazione PDF/UA: allora il referto
diventerebbe azionabile per intero. La ricetta per rifarlo sta qui sopra, così la
prossima persona non deve riscoprire la storia del provider.

## Conseguenze

**Buone.** Tre difetti che nessun exit code vedeva ora hanno un numero. La
tipografia del tema è verificata invece che creduta. E la gerarchia dei titoli è
controllata **nel master**, che è l'unico posto dove correggerla costa poco.

**Il prezzo, dichiarato.**
- **Le costanti del tema sono duplicate in Python**: un `.typ` non si importa. Un
  test le riconfronta col file, così un tema cambiato rende il controllo **rosso**
  invece che bugiardo — ma resta una duplicazione, e va saputa.
- **La simulazione delle dicromazie è un modello**, non un occhio. Dice *«questi
  due colori collassano»*, non *«questa mappa è illeggibile»*: forma, tratteggio e
  posizione possono salvare una tavola che qui risulta ambigua.
- **21 rilievi di colore sono contenuto esistente**, non un difetto introdotto
  oggi: rifare la palette delle mappe è un lavoro a sé, e questo ADR non lo apre.
