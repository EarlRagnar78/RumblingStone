# RICERCA — cosa vale la pena prendere dal Libre Graphics Meeting 2026 (RE:wire)

**Aperta**: 2026-09-01
**Domanda-fonte (DM)**: *«given rumblingstone repos and stand alone campaign there in
this page some tools that can be useful to add»*, con un link:
[`libregraphicsmeeting.org/2026/projects/`](https://libregraphicsmeeting.org/2026/projects/)
(LGM 2026, Norimberga, 22-25 aprile; i 21 progetti pubblicati vengono dalle
sottomissioni *State of Libre Graphics*, changelog e roadmap in
`github.com/libregraphicsmeeting/state-of-lg-2026`).

> **La conclusione in tre righe**: dei ventuno progetti **uno solo entra nella catena**,
> ed è già entrato con questa passata — **Inkscape** come rasterizzatore delle mappe
> accanto a Chromium (§2). **Due** valgono un lotto ma non oggi: **Stellarium** per un
> handout che il repo non ha ancora (§3.1) e **Blockbench** come versione economica
> della catena *geometria → depth → ControlNet* già scritta (§3.3). Tutto il resto è
> fuori perimetro, e il §4 dice per ciascuno *quale* perimetro.

**STATO ATTUAZIONE**: §2 **applicato** in questa passata (`export_map_png.py`,
manifest, tre guide, cinque test). §3.1, §3.2, §3.3 sono **proposte**: nessun codice,
nessuna decisione presa.

---

## §0 · Il metro, prima dei nomi

Questa ricerca **non riparte da zero**: applica le quattro soglie che
[`RICERCA-TOOL-ESTERNI-DM-2026-08.md`](RICERCA-TOOL-ESTERNI-DM-2026-08.md) §6 ha
lasciato scritte per esattamente questo caso.

1. la licenza permette l'uso **e** la ridistribuzione di ciò che produce;
2. funziona **offline**, o degrada in modo pulito;
3. sostituisce un attrito **misurato**, non immaginato;
4. se automatizza una cosa che il tavolo faceva a mano, si guarda **due volte**.

Sul panorama LGM la prima soglia però cade quasi sempre da sola, e vale la pena dire
**perché**, perché è il tranello di questa lista: sono tutti strumenti da *produzione
grafica*, e la licenza del software **non tocca ciò che il software disegna**. È la
stessa distinzione di [ADR-0019](adr/ADR-0019-licenza-dei-pesi-non-del-software.md)
(lì i pesi contro il software, qui l'opera contro l'editor). Blockbench la scrive in
chiaro nel proprio README, sotto una GPL-3.0:

> *«All assets created with Blockbench (models, textures, animations, screenshots
> etc.) are your own!»*

Quindi: **su questa lista la licenza non scarta quasi nessuno**, e chi si fa scartare
si fa scartare sulla terza soglia, l'attrito misurato. Da cui la quinta soglia che
questa ricerca aggiunge, ed è la sola cosa davvero nuova del metodo:

> **Una GUI non entra in una pipeline.** Uno strumento senza CLI può essere lo
> strumento di *una persona*, mai un passo di `dm.py`. Fingere il contrario produce
> documentazione che descrive un flusso che nessuno può rieseguire — e questo repo
> vive sul contrario: da testo versionato, per comando, in CI.

Delle ventuno voci, quelle con una CLI vera sono **cinque**: Inkscape, Krita, GIMP,
Glaxnimate, Kdenlive (via `melt`). Le altre sedici sono, per costruzione, strumenti da
mano umana, il che non le rende inutili, le rende **non integrabili**.

---

## §1 · I ventuno progetti, con il verdetto in una riga

| Progetto | Cos'è | CLI? | Verdetto qui |
|---|---|---|---|
| **Inkscape** (GPL) | editor SVG, standard di fatto | ✅ `--export-type` | ✅ **entra** — §2 |
| **Stellarium** (GPL) | planetario, con **sky culture** definibili | parziale (motore di script + plugin *SkyCultureMaker*) | 🟡 **proposta §3.1**: la carta del cielo come handout |
| **Krita** (GPL) | pittura digitale, `krita-ai-diffusion` parla con ComfyUI | ✅ `--export --export-filename` | 🟡 **già previsto** dal §3-ter di agosto: banco di ritocco del DM, mai in CI — §3.2 |
| **Blockbench** (GPL-3.0) | modellazione 3D **low-poly** | ❌ (plugin JS, non headless) | 🟡 **proposta §3.3**: la geometria della stanza a un decimo del costo di Blender |
| **GIMP** (GPL) | fotoritocco | ✅ Script-Fu batch | 🟡 utile **solo** se e quando ci saranno raster da correggere in serie (Lotto 6). Oggi non c'è niente da correggere |
| **Scribus** (GPL) | DTP, CMYK, PDF/X | fragile | ❌ **già valutato e scartato**: [ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) §2 sceglie Typst. Da riaprire solo davanti a una tiratura vera |
| **Graphite** (Apache-2.0) | editor vettoriale **a nodi**, non distruttivo, in alpha | ❌ (web/desktop) | ❌ **oggi**, 👀 **domani**: un grafo di nodi che produce SVG è la forma giusta per una legenda parametrica di mappa. In alpha e senza CLI, non è un candidato: è una cosa da riguardare fra un anno |
| **PixiEditor** (LGPL-3.0) | editor 2D a nodi (pixel/raster/vettoriale) | ❌ | ❌ **fuori perimetro**: token e sprite sono la coda di Lotto 6, e comunque a mano |
| **Glaxnimate** (GPL, KDE) | animazione vettoriale (Lottie/SVG) | ✅ render da riga di comando | ❌ **fuori perimetro**: il repo produce documenti, non animazioni. Vedi §4.2 |
| **Kdenlive** (GPL, KDE) | montaggio video | ✅ via `melt` (MLT) | ❌ idem §4.2 |
| **Friction** (GPL) | motion graphics vettoriale per il web | parziale | ❌ idem §4.2 |
| **Penpot** (web, self-hostabile) | design collaborativo su standard web | ❌ | ❌ **duplicherebbe una fonte di verità**: è l'obiezione fatta a Kanka ad agosto. Il layout qui è generato da manifest, non disegnato |
| **GIMP · Krita · Inkscape · Scribus** | *(la pila classica)* | — | ↑ già sopra |
| **p5.js** (LGPL) | creative coding in JS | ✅ via node/headless | ❌ **fuori perimetro come dipendenza**, 🟡 come **generatore una-tantum** di una texture di pergamena o di un fregio, esportata e poi committata come asset. Non serve un runtime: serve un file |
| **OPENRNDR** (Kotlin) | framework creative coding | ✅ | ❌ come sopra, e in più aggiunge una JVM alla macchina del DM |
| **Coollab** | visual generativi a nodi, real-time | ❌ | ❌ **VJ**, non editoria |
| **TiXL** (MIT) | grafica real-time e VJing | ❌ | ❌ idem |
| **ossia score** | sequencer per installazioni e spettacoli | ✅ (ma per altro) | ❌ idem — e il suono qui resta **descritto**, mai un file (ADR-0014) |
| **L5** (LGPL) | Processing in Lua su LÖVE, permacomputing | ✅ | ❌ come p5.js, con meno diffusione |
| **Our Paint** (GPL) | pittura con modello di colore a pigmenti | ❌ | ❌ strumento d'artista puro: nessun artista in questa catena |
| **Makepad** (Rust) | ambiente di sviluppo applicazioni | — | ❌ nessuna attinenza |
| **Upstage** | palco online per performance dal vivo | — | ❌ nessuna attinenza (e non è un VTT) |
| **Hyper8** | pubblicazione video con generatore di sito statico | ✅ CLI | ❌ **fuori perimetro**, ma vedi §4.2: è l'unica forma *sensata* che avrebbe un video di campagna |
| **Ladrón de Flores** | corto d'animazione + **pipeline 100% libre**, premiato a festival | — | 📌 **non è un tool: è la prova che la pila regge**. Utile da citare, niente da importare |

Licenze: verificate per Inkscape, Blockbench (GPL-3.0), PixiEditor (LGPL-3.0),
Graphite (Apache-2.0); TiXL (MIT) e L5 (LGPL) come dichiarati dalla pagina LGM. Per
gli altri **non ho verificato la versione esatta**, e non serve: nessuno di loro è
scartato per licenza, tutti per perimetro o per assenza di CLI.

---

## §2 · Quello che entra oggi — Inkscape accanto a Chromium

**L'attrito, misurato**: `export_map_png.py` rasterizzava **solo** con Chromium
headless. Il PNG di una mappa è ciò che il DM porta al tavolo stampato, importa a mano
nel VTT e dà in pasto alla passata hero-map di ComfyUI. Quel passo dipendeva quindi da
un browser, che sulla macchina di un DM può non esserci, mentre `render_map_svg.py`,
il pezzo che conta, gira ovunque con la sola stdlib.

E c'è la ragione tecnica, che è quella per cui vale la pena farlo davvero e non solo
per comodità: **Chromium impagina pagine web**. È la stessa frase che ADR-0020 ha
scritto sulla stampa (*«Chromium impagina pagine web, non libri»*) applicata un piano
più sotto: un browser rasterizza l'SVG dentro un viewport, e la scala arriva come
`--force-device-scale-factor`, cioè come zoom di finestra. Inkscape è un renderer SVG
e basta: prende **le misure d'uscita** (`--export-width` / `--export-height`) e
disegna quelle.

**Cosa è cambiato** (in questa passata):

- `scripts/export_map_png.py` ha `--renderer auto|inkscape|browser` (+ `--inkscape`,
  come già `--browser`; e `MAP_PNG_INKSCAPE` come già `MAP_PNG_BROWSER`).
  **`auto` è il default**: Inkscape se c'è, browser altrimenti; nessuna macchina
  esistente cambia comportamento se non installa niente;
- se non c'è **nessuno** dei due, lo script dice quale binario installare ed esce
  `1` **senza lasciare un file a metà**, la regola di degradazione pulita che
  [ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md) chiede e che
  ADR-0020 §3 aveva già applicato a Typst;
- manifest aggiornato (`external_bins: [inkscape, chromium]`, i due argomenti nuovi,
  exit code) e i tre artefatti di `docs/tools/` rigenerati;
- **cinque test** in `scripts/tests/test_export_map_png.py`: quale motore vince in
  `auto`, quali flag riceve Inkscape (misure d'uscita, non viewport), che
  `--renderer browser` resta forzabile, e le due degradazioni pulite.

**Cosa NON risolve, e va detto**:

- il PNG **resta un artefatto locale non committato** e **non diventa deterministico**:
  cambia fra versioni di Inkscape come cambiava fra versioni di Chromium. La riga di
  `determinism.notes` nel manifest è stata aggiornata, non cancellata;
- **la resa dei due motori non è ancora stata confrontata a occhio.** In questo
  ambiente Inkscape non è installato: il ramo Inkscape è verificato **per contratto**
  (binario finto, argomenti registrati), non **per pixel**. Il confronto vero,
  stessa mappa, due motori, differenze su etichette ruotate, tratteggi e pattern, è
  un controllo da fare sulla macchina del DM. Finché non è fatto, la riga onesta è:
  *il default preferisce Inkscape perché è il renderer giusto per il formato*, non
  *perché abbiamo visto che rende meglio*.

---

## §3 · Le tre proposte — nessuna decisa, nessuna gratis

### §3.1 · Stellarium: la carta del cielo come handout

È l'unica idea di questa lista che apre una **cosa che il repo non ha**, invece di
migliorarne una che ha.

Stellarium non serve qui come planetario: serve perché sa caricare **sky culture**
definite dall'utente (costellazioni proprie, con linee, nomi e illustrazioni) e le
versioni recenti hanno perfino un plugin (*SkyCultureMaker*) per disegnarle dentro il
programma invece che a mano nei file. Da lì esce un'immagine di cielo **coerente**:
stesse stelle, stesse posizioni, ogni volta.

**A cosa servirebbe qui, concretamente**: un handout che oggi non esiste in nessuna
forma: la carta del cielo che un personaggio consulta. Serve a tre cose che sono già
scritte nel canone e che oggi si risolvono a parole: la navigazione notturna di un
viaggio, un'ancora temporale («questa configurazione si vede una volta ogni N anni»),
e soprattutto **un indizio di cui non si può falsificare la copia**: il cielo è lo
stesso per tutti, e una carta che *non* combacia col cielo è una carta falsa. Per la
skill `rumblingstone-indagine` è un nodo d'indizio a tre strati bell'e pronto: Fatto
osservabile, Lettura, Nome, con una porta d'ingresso *fisica*, non un tiro di abilità.

⚠️ **La cautela IP, che qui è la parte difficile**: le costellazioni di Faerûn hanno
**nomi di lore WotC**, e [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md)
vale identico. La sky culture si costruisce quindi **con nomi propri del repo** (o
generici) sopra un cielo qualunque: si prende il **meccanismo**, non il catalogo.
È la stessa distinzione del §3-bis di agosto: la tecnica sì, l'opera no.

**Costo**: mezza giornata per la prima carta, quasi tutta manuale. **Non c'è codice da
scrivere**, e questo è il punto a favore: non aggiunge una dipendenza al toolkit,
aggiunge un asset. **Gate**: serve che il DM voglia quell'handout in un modulo
preciso. Farlo «perché è bello» produrrebbe una figura senza posto nel testo, che è
esattamente il difetto che il capitolato del Drappo elenca fra i sei.

### §3.2 · Krita e GIMP: banco del DM, mai passo di catena

Nessuna novità rispetto ad agosto (§3-ter li aveva già nominati), ma la lista LGM
serve a **fissare la regola** che allora era implicita, ed è la quinta soglia del §0:

- **Krita** ha una CLI d'esportazione (`krita file.kra --export --export-filename
  out.png`) ed è il posto giusto per la passata di ritocco su una hero map o un
  ritratto, anche parlando con lo stesso ComfyUI via `krita-ai-diffusion`;
- **GIMP** ha lo Script-Fu batch e servirà quando ci saranno **serie** di raster da
  normalizzare, ma `build_image_derivatives.py` (Pillow) copre già il
  ridimensionamento, che è l'unico batch che oggi esiste davvero.

**Il confine, e va scritto una volta sola**: un file `.kra` o `.xcf` è un **sorgente
d'artista**, non un master del repo. [ADR-0003](adr/ADR-0003-markdown-master-layout-generati.md)
vuole master di testo e layout generati; un binario di Krita in `git` non si diffa, non
si valida e non si rigenera. Entra nel repo **il PNG esportato con la sua riga di
PROVENIENZA** (ADR-0019 §2), mai il progetto.

### §3.3 · Blockbench: la geometria, a un decimo del costo di Blender

Il §3-ter di agosto ha scritto il pezzo più caro della pila: *geometria dal JSON della
mappa → Blender headless → passo di profondità → ControlNet depth*, per ottenere la
cosa che distingue un AP pubblicato: **la tavola e la pianta sono la stessa stanza**.

Blockbench cambia **solo il primo anello**, e in meglio: modellare una locanda
low-poly lì costa una frazione di quanto costa in Blender, l'interfaccia è fatta per
volumi squadrati (cioè per stanze), esporta OBJ/glTF, e ha un'API a plugin JS con cui
un giorno si potrebbe generare la scatola direttamente dal contratto JSON della mappa.

⚠️ **Non toglie Blender dalla catena**: Blockbench non fa render headless, e il passo
di profondità resta a Blender. Quindi non è un'alternativa al piano di agosto: è
**l'anello di modellazione** di quello stesso piano, reso abbordabile. Resta l'ultimo
in ordine di priorità, come già scritto: dopo Typst (fatto) e dopo lo script di batch
su ComfyUI (non fatto).

---

## §4 · Quello che è fuori perimetro — e quale perimetro

### §4.1 · Real-time, VJing, installazioni (Coollab, TiXL, ossia, OPENRNDR, L5, Upstage)

Sono strumenti da **spettacolo dal vivo**. Il repo produce documenti che si stampano
e si leggono al tavolo; un visual generativo proiettato durante la sessione è una cosa
che un DM può fare e che questo repo non ha alcun motivo di **descrivere**, perché non
sarebbe riproducibile da nessun altro DM (soglia 3: attrito immaginato).

### §4.2 · Video (Glaxnimate, Kdenlive, Friction, Hyper8)

Qui la risposta merita una riga in più, perché il repo **ha** una funzione che si
chiama *teaser* (`dm.py`, hype Homebrewery): potrebbe sembrare il posto giusto per un
video. Non lo è: il teaser del repo è **testo spoiler-free** che il DM manda al gruppo
fra una sessione e l'altra, e la sua qualità sta nel *cosa non dice*. Un montaggio
video cambia mestiere, e cambia soprattutto il **costo per sessione**, che per il
teaser oggi è di due minuti.

Se un giorno esistesse materiale video (registrazioni del tavolo, una sigla), la forma
giusta sarebbe **Hyper8** e non YouTube: sito statico, backend locale, niente servizio
terzo che ospita la voce dei giocatori, la stessa preoccupazione di riservatezza che
il §3 di agosto ha applicato alla trascrizione. **Nessun lotto**: è una nota per il
giorno in cui la domanda si porrà.

### §4.3 · Penpot, e perché un editor collaborativo non serve a un repo

Penpot è ottimo e non ha niente che non vada. Semplicemente: il layout di questo repo
**non si disegna**, si genera da un manifest (ADR-0013, ADR-0020). Aprire un secondo
posto dove il layout esiste significa avere due fonti di verità e nessun gate
sull'altra: l'obiezione fatta a Kanka ad agosto, identica.

---

## §5 · E i moduli autoconclusivi? — una riga sola, ed è già applicata

Per **Il Drappo di Tarsilia** e **L'abbazia della Rotta Sicura** cambia esattamente
una cosa, la stessa della campagna: le loro mappe si rasterizzano anche con Inkscape
(§2), e il DM che le stampa non ha più bisogno di un browser installato. Le mappe del
Drappo sono già nel contratto JSON e hanno già gli SVG in `rendered/`: non c'è niente
da migrare.

Il resto **non cambia**, e per una ragione che vale la pena scrivere perché è la
stessa di agosto: quello che manca al Drappo è nel suo capitolato
(`PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`): **immagini raster**, mappa in versione
giocatore, carte da tavolo. Nessuno dei ventuno progetti LGM produce un'immagine al
posto nostro: sono strumenti per **una mano che disegna**. Il giorno in cui quella
mano c'è, Krita e Inkscape sono gli strumenti giusti e sono già documentati (§3.2).

L'unica proposta che tocca davvero un modulo autoconclusivo è la carta del cielo
(§3.1), e per il Drappo sarebbe fuori tono: tre serate, una città, nessun viaggio
notturno. Il suo posto naturale è **la campagna**, in un beat di viaggio.

---

## §6 · Cosa lascia questa ricerca al prossimo che guarda una lista di tool

Il criterio di agosto (§6, quattro soglie) ha retto senza modifiche. Questa passata
aggiunge la quinta, **una GUI non entra in una pipeline**, e un corollario che vale
per tutta la grafica libera:

> Su questa categoria di strumenti **la licenza non discrimina quasi mai**: quello che
> disegni è tuo anche sotto GPL. Discriminano due domande più noiose: *ha una CLI?* e
> *l'attrito che toglie l'ho misurato o l'ho immaginato?* Su ventuno progetti la prima
> ne ha lasciati cinque, la seconda ne ha lasciato uno.

E una nota di proporzione, che è la stessa cosa detta dal §6 di agosto con altre
parole: un elenco di ventuno strumenti bellissimi è la tentazione perfetta per un repo
che ha un solo problema vero, **l'arte**, e ventuno modi di rimandarlo. Nessuno dei
ventuno disegna al posto di nessuno.
