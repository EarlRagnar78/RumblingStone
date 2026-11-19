# Riferimento dei booklet: cosa produce la catena, il manifest, la tipografia

> Forma: **riferimento** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)). Descrive cosa esce dalla catena dei booklet, i campi del manifest e cosa fa il tema; la ricetta per una serata sta nella guida. Nato il 2026-11-10 dalle sezioni di riferimento di [GUIDA-BOOKLET-E-PDF](../how-to/GUIDA-BOOKLET-E-PDF.md). Le sezioni tengono il numero che avevano lì, così un rimando scritto prima («GUIDA-BOOKLET-E-PDF §N») resta vero: nella guida, al posto della sezione, c'è un rimando a questo file.

---

## 1. Cosa produce la pipeline

```
   master markdown            manifest JSON              artefatti generati
 (ARC*-DEF-*, hint,   ──▶  (*.manifest.json)  ──▶   ┌── .html   pagina autonoma, immagini incorporate
  teaser, regia…)           elenca i capitoli        ├── .hb.md  sorgente Homebrewery V3 (editor 2 pannelli)
   ← LA VERITÀ                e i metadati           └── pdf/*.pdf  A4, una scheda per file
```

**I markdown sono i master** (ADR-0003): HTML, `.hb.md` e PDF sono
**artefatti rigenerabili**. I PDF non stanno nel repo (`*.pdf` è in
`.gitignore`): si rifanno in un comando quando servono.

| Output | A cosa serve | Serve un browser? |
|---|---|---|
| `.html` | leggere/sfogliare a schermo, condividere un file solo | no |
| `.hb.md` | modificare l'impaginazione nell'editor Homebrewery self-hosted | no (serve il container per l'editor) |
| `pdf/*.pdf` | stampare, o inviare una pagina sola a un giocatore | **sì** (Chromium headless) |

### 1.1 Il soffitto di questa catena — dichiarato, così non lo si cerca invano

Questa pipeline arriva fin dove arriva **il browser**, e Chromium impagina pagine
web, non libri. Restano fuori, e **nessuna quantità di CSS li recupera**:

- il controllo su **vedove e orfane**;
- la **crenatura** fine e la spaziatura ottica;
- un **indice** che diventi una struttura di segnalibri degna;
- i **font embedded** — oggi è Georgia, un font di sistema: su una macchina che
  non ce l'ha il PDF cambia faccia;
- il **volume unico** invece di un file per capitolo.

Non sono difetti del codice: sono il soffitto dello strumento. Per superarlo c'è la **seconda catena**, quella da stampa
([ADR-0020](../../plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md)):

```bash
python3 scripts/export_booklet_typst.py MANIFEST.json --all
```

Legge **lo stesso manifest** e produce **un volume unico** `-STAMPA.pdf` con
tipografia OFL embedded (EB Garamond + Cinzel), due colonne, fregi di capitolo,
tabelle larghe che scavalcano le colonne e **segnalibri PDF veri**. Serve typst
(Apache 2.0): lo standard è il pacchetto PyPI di `requirements.txt`
(`pip install -r requirements.txt`), il ripiego una CLI `typst` nel PATH,
[ADR-0116](../../plans/adr/ADR-0116-typst-si-installa-da-pypi.md). Senza rete:
il rilascio ha un `rumblingstone-offline-<piattaforma>-<tag>.zip` con tutte le
wheel, e `python3 scripts/bundle_offline.py installa <zip>` le installa.
`python3 scripts/typst_motore.py` dice quale dei due compila. Se mancano tutti e
due, lo script dice come installarlo ed esce pulito: **questa catena qui sotto
continua a funzionare da sola**.

Come le due catene si incastrano con tutto il resto:
[GUIDA-FLUSSO-LOCALE](../explanation/GUIDA-FLUSSO-LOCALE.md).

### 1.2 Le schede pregenerate non sono un capitolo

Un capitolo si legge una volta; una **scheda** sta in mano al giocatore per tre
serate. Impaginare le schede come testo corrente — un paragrafo dopo l'altro su
due colonne — le rende illeggibili proprio quando servono: a metà combattimento,
nessuno cerca la CA dentro una frase.

Perciò un capitolo del manifest può dichiararsi **scheda**:

```json
{
  "title": "✉ Le sei schede",
  "file": "../PREGEN-SEI-SCHEDE-PF1E.md",
  "tag": "player",
  "layout": "schede",
  "retro": "../FASCICOLO-SCHEDE-GIOCATORE.md",
  "ritratti": ["../ALLEGATI/immagini/web", "../ALLEGATI/immagini"],
  "footer": "IL DRAPPO DI TARSILIA · PATHFINDER 1E · SCHEDA DA TAVOLO"
}
```

L'esportatore lo impagina con `scripts/typst/scheda-pg.typ`: **una pagina A4 per
personaggio**, con

- in **alto** il nome, classe/livello/razza e il ritratto, più i tre valori che
  si consultano di continuo (iniziativa, percezione, velocità);
- a **sinistra** chi sei — il background in prima persona da leggere ad alta
  voce, l'equipaggiamento, il legame con gli altri personaggi, il tuo problema;
- a **destra** quanto fai — CA, pf, tiri salvezza, la griglia dei sei attributi
  coi modificatori, attacchi, abilità, talenti, incantesimi;
- in **fondo**, a piena larghezza, «come si gioca in un minuto».

| Campo | Cosa fa |
|---|---|
| `layout: "schede"` | accende l'impaginazione a scheda per quel capitolo |
| `file` | il master dei **numeri** (`PREGEN-*.md`) — obbligatorio |
| `retro` | il master della **persona** (`FASCICOLO-*.md`) — facoltativo: senza, esce la sola metà destra |
| `ritratti` | cartelle dove cercare `ritratto-<nome>.<jpg\|png\|webp\|svg>`, in ordine di preferenza |
| `footer` | la riga in fondo alla pagina |
| `front_matter: false` | *(chiave del manifest, non del capitolo)* niente frontespizio né indice — sei fogli e basta |

I dati arrivano **dagli stessi master markdown che il tavolo usa già**: non
esiste una seconda copia dei numeri, quindi non esiste una copia che possa
restare vecchia. Se cambi la CA nel `PREGEN-*.md`, cambia nella scheda stampata.

> **I ritratti pesanti vanno ridotti.** Un PNG da 6 MB per scheda fa un PDF da
> quaranta megabyte. Metti le derivate leggere in una cartella `web/` e
> nominala **per prima** in `ritratti` — vedi
> `10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/web/README.md`.

Esempio completo nel repo:
`10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/DRAPPO-SCHEDE-PG.manifest.json`.

**Un PDF per giocatore**, oltre al fascicolo:

```bash
python3 scripts/export_booklet_typst.py MANIFEST.json --per-scheda
```

Scrive anche `schede/<nome>-<N>-<pg>.pdf`, uno per personaggio, **senza
frontespizio**. Non è una comodità: sulla scheda c'è «la cosa che non dici».
Girare il volume intero nel gruppo brucia i segreti di tutti prima della prima
serata — il fascicolo completo è per il DM e per la stampante, i singoli per i
giocatori.

Ogni scheda viene compilata da un **sorgente suo**, non ritagliata per numero di
pagina: il ritaglio regge finché ogni scheda sta in una pagina sola, cioè finché
qualcuno non allunga un equipaggiamento.

### 1.2-bis Le carte da tavolo di una corsa

Un capitolo `"layout": "carte"` non si legge: si ritaglia. L'esportatore lo
impagina con `scripts/typst/carte-tavolo.typ`: carte da **63 × 88 mm**, nove per
foglio A4 a contatto, con la linea di taglio tratteggiata in comune. Sono la
voce B3 di `plans/RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md`: carte che
rendono visibile lo stato della gara senza spiegarlo.

```json
{
  "title": "✉ Le carte da tavolo",
  "file": "../REGOLE-DELLA-CORSA-PF1E.md",
  "contrade": "../CONTRADE-DI-TARSILIA.md",
  "tag": "player",
  "layout": "carte"
}
```

| Campo | Cosa fa |
|---|---|
| `layout: "carte"` | accende l'impaginazione a carte per quel capitolo |
| `file` | il master delle **regole della corsa**: §4 (patti), §5 (funi e finte), §6 (giri), §6.1 (tratti e CD), §6.2 (posti) |
| `contrade` | il master delle **contrade**: §1 (nome, dèi, livrea, motto), §7 (stemma) |
| `front_matter: false` | *(chiave del manifest)* niente frontespizio né indice |

I mazzetti, nell'ordine dei fogli: un **segnaposto** per contrada (stemma, motto,
livrea, il cavallo da scrivere dopo la Sorte e la griglia delle Lunghezze da
segnare a matita, giro per giro), l'**ordine alle funi** (un numero per cavallo
fra le funi più quello di rincorsa, con le tre finte), i **tratti** in ordine di
corsa (giro, tratto, CD, cosa succede se si sbaglia) e i **posti** dei PG non
fantini; i posti vuoti di un foglio si riempiono di **patti** in bianco.

I dati li legge `scripts/dmcore/carte_tavolo.py` dalle tabelle e da poche frasi
dei master, riportate intere. Se un master cambia forma (una tabella rinominata,
«Sette cavalli entrano fra le funi» riscritto), la lettura si ferma con un
errore invece di stampare carte vecchie. Gli stemmi della serie Golarion portano
nel cartiglio il motto del Palio: le scritte dello scudo si tolgono alla
lettura, il file non si copia.

Esempio nel repo:
`10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/DRAPPO-CARTE-DA-TAVOLO.manifest.json`.

### 1.3 Cosa controlla la CI, e cosa no

| Livello | Chi lo controlla |
|---|---|
| il **markdown** delle schede (sezioni obbligatorie, GS dichiarato) | `validate_standalone.py` §3, in CI |
| i **link** del modulo, immagini comprese | `validate_standalone.py` §2, in CI |
| il **manifest** di ogni booklet (schema, capitoli, copertina, introduzione) | `validate_booklets.py`, in CI |
| le **immagini** citate dai master (esistono davvero?) | `validate_booklets.py`, in CI |
| i **parametri** che l'esportatore passa al template `.typ` | `test_schede.py::TestSorgenteTypst` |
| la **compilazione vera** di tutti i volumi, segnalibri compresi | `validate_booklets.py --stampa`, in CI con `typst` **a versione fissata** |
| le sei **schede singole** | `--per-scheda` in CI (conta che siano sei) |
| le **creature** fuori dal riquadro unico, per booklet | `misura_statblocchi_booklet.py --check`, in CI, tetto che scende soltanto |
| la **prestampa**: corpo sotto 7 pt, testo oltre la gabbia, immagini sotto 300 dpi o tagliate dal bordo del foglio, riquadri spezzati | `misura_stampa.py --tutti --check`, job CI `stampa-misurata` |
| **chi si incontra** nel capitolo (numeri, aspetto, ritratto, chi è, cosa vuole, tattica, mappa) e le **note di lavoro** in stampa | `misura_standard_tavolo.py`: indicatore, con cricchetto nei test sulle note |
| quante **pagine** separano la scena dai numeri di chi c'è | `misura_distanza_pagine.py <PDF>`: indicatore, a mano |
| lo **standard del volume** degli AP (ADR-0122): introduzione di capitolo, chiavi d'area uguali fra testo e mappa, mappa vicina alla descrizione, appendice di regione e PNG, ritratto dei PNG principali | `misura_distanza_pagine.py --volume --tutti --check`, passo non bloccante del job `stampa-misurata` (canale testing); `dm.py volume <manifest> --stampa`, passo `struttura` |
| il **giudizio estetico** | ⚠️ nessuno, e nessuno potrà: si guarda a occhio, in locale |

> 📌 **Dal 2026-08-22 in CI c'è `typst`.** Prima non c'era, e la conseguenza è
> stata misurata: **due booklet della campagna non avevano mai compilato** (il
> fascicolo del Palio e quello di Terros), e le immagini dei master non entravano
> affatto nel volume — `![Stemma Oca](…)` usciva stampato come `!Stemma Oca`.
> Prima di consegnare qualsiasi cosa:
>
> ```bash
> python3 scripts/validate_booklets.py --stampa
> ```

Per guardarla a occhio senza aprire il PDF, le pagine si rendono in PNG:

```bash
python3 scripts/export_booklet_typst.py MANIFEST.json --keep-typ
typst compile --font-path scripts/fonts --root . \
    --format png --ppi 110 <nome>.typ 'pagina{n}.png'
```

> ⚠️ **Le derivate leggere delle immagini sono gitignorate.** `.gitignore` blocca
> `*.jpg` in tutto il repo: se un master punta a `.../web/*.jpg` e quei file non
> sono committati con un'eccezione `!`, il link è rotto in un clone fresco anche
> se sulla tua macchina funziona. `validate_standalone.py` lo segnala e dice
> perché.

---

## 3. Il manifest, campo per campo

Un booklet è descritto da un file `*.manifest.json` messo **accanto ai
capitoli**. Tutti i percorsi sono relativi alla cartella del manifest.

```json
{
  "brand":         "RUMBLING STONE · IL PORTALE DELLA FORGIA ETERNA",
  "title":         "Lo Scontro con Terros l'Antico",
  "subtitle":      "Il Piano della Terra · lo Smeraldo della Forza",
  "banner":        "BOOKLET DI SESSIONE",
  "meta":          "riga piccola in fondo alla copertina",
  "header":        "riga descrittiva sotto il titolo della pagina",
  "footer":        "Lo Scontro con Terros",
  "player_footer": "L'Ultima Porta",
  "cover_tag":     "player",
  "cover_image":   "../../Immagini/camera-nodo-terra.webp",
  "intro_md":      "00-INTRO-DOVE-SIAMO.md",
  "out":           "ARC07-SESSIONE-TERROS-BOOKLET.html",
  "indice_analitico": true,
  "colophon": {
    "edizione":  "Edizione da tavolo",
    "versione":  "v1",
    "data":      "2 settembre 2026",
    "autori":    "G. Samuele",
    "basato_su": "SRD 3.5 e OGL 1.0a",
    "licenza":   "Materiale del DM, uso privato e non commerciale",
    "nota":      "avvertenze di contenuto, se servono"
  },
  "chapters": [
    {"title": "I · Regia della Sessione", "file": "01-REGIA-SESSIONE.md", "tag": "dm"},
    {"title": "✉ Hint — Thorik",          "file": "02-HINT-THORIK.md",    "tag": "player"}
  ]
}
```

| Campo | Cosa fa |
|---|---|
| `brand` / `title` / `subtitle` / `banner` / `meta` | la copertina |
| `header` | riga sotto il titolo nella pagina HTML |
| `footer` | piè di pagina delle schede **DM** |
| `player_footer` | piè di pagina delle schede **✉ player** — **titolo evocativo, MAI quello reale** (ADR-0013 §3: un handout che in fondo dice «Lo Scontro con Terros» brucia l'aspettativa) |
| `cover_tag` | `"player"` se la copertina stessa è il deliverable da inviare (file del gruppo): entra nell'export player e il PDF prende il nome dal `title` |
| `cover_image` | immagine di copertina (SVG inline, oppure PNG/JPG/WEBP incorporate) |
| `intro_md` | markdown mostrato **nella stessa scheda** della copertina |
| `out` | nome del file HTML (i `.hb.md` e i PDF derivano da questo) |
| `colophon` | **la pagina dei crediti**, sul verso del frontespizio ([ADR-0023](../../plans/adr/ADR-0023-colophon-di-edizione.md)): chi ha fatto il volume, che versione è, su cosa si basa e cosa se ne può fare. Senza questa chiave **il volume esce anonimo**. ⚠️ La `data` si **scrive**, non si deduce dall'orologio: un PDF che prende la data dall'ora corrente cambia a ogni compilazione e smette di essere byte-identico. E `autori` **non si inventa mai** |
| `indice_analitico` | aggiunge l'**INDICE ANALITICO** in coda al volume da stampa. Le voci **non si annotano a mano**: le marca l'esportatore prendendo i nomi canonici dal glossario, alla prima occorrenza per volume. Se in quel volume non compare nessun nome del glossario — il caso dei moduli autoconclusivi, che hanno un'ambientazione loro — la pagina **non si aggiunge**: un indice vuoto è peggio di niente. Solo catena di stampa: una pagina web ha la ricerca |
| `schede` | dove esce il riquadro intero delle creature ([ADR-0105](../../plans/adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md)): `"appendice"` (predefinito) mette nell'incontro una riga con nome, GS, CA, pf, rimando e tattica e il riquadro in fondo al volume; `"qui"` lo lascia dove è scritto (volumi per i giocatori); `"entrambe"` lo lascia dove è scritto e aggiunge l'appendice, solo nel PDF |
| `chi_si_incontra` | `true` porta in ogni capitolo, prima di stampare, le persone che vi si incontrano (scheda d'entrata con la riga **Chi è**, ritratto, riquadro con la tattica) e le piante delle mappe che nomina, prese dal master che le ha ([ADR-0107](../../plans/adr/ADR-0107-chi-si-incontra-sta-nel-capitolo.md), `dmcore/chi_si_incontra.py`). Va con `"schede": "entrambe"`. Il master non cambia. Solo catena di stampa |
| `chapters[]` | `title` = etichetta del tab · `file` = markdown · `tag` = `dm` (⚠ SOLO DM) / `player` (✉ HANDOUT) / assente |

---

## 8-bis. La tipografia: cosa fa il tema da solo, e cosa puoi chiedergli

Il tema (`scripts/typst/tema-rumblingstone.typ`) **si tocca lì**, mai nel `.typ`
generato — quello si rifà a ogni compilazione.

- **Capolettera annegato.** L'iniziale del primo paragrafo di ogni capitolo
  scende **tre righe** dentro il testo, che le scorre attorno (pacchetto
  `droplet`, vendorizzato: la build non scarica niente, [ADR-0026](../../plans/adr/ADR-0026-vendoring-pacchetti-typst.md)).
  ⚠️ Vuole almeno tre righe sotto di sé: su un paragrafo corto usa
  `capolettera-versale`, che è il ripiego e resta disponibile apposta.
  Si spegne per capitolo con `"capolettera": false` nel manifest.
- **Indice analitico**: `"indice_analitico": true` (vedi §3).
- **Imposizione in libretto**: `dm.py volume --imposto`, oppure a mano
  `python3 -m pdfimpose saddle --signature 2x1 --output LIBRETTO.pdf VOLUME-STAMPA.pdf`
  (pdfimpose da `requirements.txt`, [ADR-0116](../../plans/adr/ADR-0116-typst-si-installa-da-pypi.md)).
  Non usare `--format A4`: ingrandisce di poco le pagine. ⚠️ Il PDF imposto
  **non si versiona e non si confronta a byte**: due esecuzioni non danno lo
  stesso file, anche se le pagine sono le stesse ([ADR-0027](../../plans/adr/ADR-0027-imposizione-con-pdfcpu.md)).
- **Formato A5** (`--formato a5`, o `"formato": "a5"` nel manifest): compone il
  volume a **una colonna** con corpo 9.6 pt. Va **insieme** all'imposizione, non
  al posto suo: imporre un volume A4 mette due pagine per foglio e le scala al
  71%, cioè porta il corpo a ~7,2 pt — si stampa, non si legge al tavolo.
  Composto in A5, dopo la piega il corpo resta quello di un tascabile.
  In A5 anche l'indice analitico va a una colonna: due sarebbero da 5 cm.
- **Quanto è leggibile**: `python3 scripts/validate_tipografia.py` misura i
  **caratteri per riga** dalle metriche vere del font (oggi **62,1**, dentro la
  finestra 45-75), la **gerarchia dei titoli** — un `h4` sotto un `h2` diventa un
  ramo che non esiste nei segnalibri — e simula le tre dicromazie sulle tavole,
  per trovare i colori che a chi è daltonico diventano lo stesso colore.
