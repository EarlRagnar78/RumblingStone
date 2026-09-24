# PIANO — Pipeline ibride: il grounding, il ponte fra prosa e geometria, e la misura

> **Stato**: 🔵 **proposta, aperta** — scritta il 2026-09-16, nessun lotto eseguito
> **Arrivo su `main`**: 2026-09-24, dalla PR #143 rimasta in bozza per otto
> giorni. Se ne è portato il contenuto, non i commit. L'ADR era nata come
> ADR-0050, numero che nel frattempo era andato a
> [ADR-0050 stato di campagna](adr/ADR-0050-stato-di-campagna-dati-e-prosa.md):
> qui è [ADR-0067](adr/ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md).
> ⚠️ **I numeri di §1 e della misura di rumore (§6, lotto A) sono del 2026-09-16 (`b701d39`) e non sono stati
> rimisurati al porto.** Uno solo è stato riverificato: `dmcore.legenda` non
> ha ancora un accessore per `blocks_movement`, quindi A0 resta il primo lotto.
> **Nasce da**: un documento esterno consegnato dal DM il 2026-09-16
> (`Encanced_with_data_scient_rumblingstone_repos.odt`, 227 righe di trascrizione, quattro
> blocchi di proposte: orchestratore ibrido, pipeline della prosa
> «Differential & Mixer», pipeline cartografica «Asymmetric Mixer», parser
> cartografico dalla prosa).
> **Mandato del DM**: *«Deep audit del documento e crea un PRD pulito basato sul
> documento, integra tutte le parti discusse con la prospettiva di un data
> scientist, di un architetto senior e di uno sviluppatore, per una proposta di
> miglioramento reale del repo. Alla fine un documento onesto e dettagliato con
> insight e piani veri di creazione delle pipeline.»*
>
> **La risposta breve**: il documento sorgente descrive un repo che non esiste
> più. La sua tabella comparativa dà come «stato attuale» quattro cose che sono
> state costruite fra luglio e settembre, e sulle quattro righe **sbaglia
> quattro volte**. Tolta quella tabella, restano **tre idee buone** — e una di
> esse è il vero collo di bottiglia della catena cartografica, che il repo non
> ha mai chiuso. Questo piano tiene le tre, rifiuta le altre con il motivo, e
> mette dei numeri dove il documento ne aveva messi di inventati.

---

## §0 · Prima di leggere

### 0.1 · Cosa manca per rispondere meglio di così

Elencate perché una risposta di questa taglia non va data fingendo di sapere.

| Cosa manca | Perché cambia la risposta | Come si chiude |
|---|---|---|
| **Chi ha scritto il documento sorgente e con quale accesso al repo** | Se l'autore ha letto il repo, la tabella «stato attuale» è un errore di lettura; se ha lavorato per sentito dire, è una ricostruzione a memoria, e allora anche le percentuali vanno lette come atmosfera. I due casi meritano risposte diverse | domanda al DM |
| **Un corpus di riferimento della prosa giudicata buona** | Senza, ogni numero sulla qualità della prosa è un'opinione con un decimale. Il DM è l'unico annotatore possibile: la prosa buona è quella che ha funzionato al tavolo | lotto D, decisione **D4** |
| **Quante mappe nasceranno da zero contro quante trascrivono una planimetria già in testa al DM** | Decide se la generazione procedurale (WFC/BSP) serve o è un utensile per un problema che nessuno ha | osservazione sulle prossime cinque mappe |
| **Se le 18 mappe master di oggi sopravvivono al grounding** | Se il validatore boccia il canone già giocato, non nasce bloccante. Il numero si conosce solo eseguendolo | lotto A, misura di partenza |

### 0.2 · Le assunzioni con cui si procede

1. **Il perimetro è interno.** Questo piano non riguarda la pubblicazione né la
   vendibilità: quelle hanno i loro piani e la loro ADR-0049.
2. **L'italiano è la lingua sorgente** (ADR-0016), anche per gli identificatori
   dei lotti e per i messaggi degli script.
3. **Il tavolo vince sul modello.** Una metrica che dice il contrario di ciò che
   il DM ha giudicato migliore è una metrica sbagliata, e l'ha già dimostrato
   ADR-0036 sulla burstiness.
4. **Il repo di riferimento è quello di `b701d39`** (2026-09-16). Tutti i numeri
   di §1 sono stati presi eseguendo comandi, non stimati; §10 dice come
   rimisurarli.

### 0.3 · Le due domande poste al DM, e le sue risposte

| Domanda | Risposta del DM, 2026-09-16 |
|---|---|
| L'LLM entra negli script o resta client? | **Ibrido a confine dichiarato**: un solo script-ponte opzionale, che fallisce pulito senza rete e non è mai in CI; tutto il resto deterministico. Ratificata in [ADR-0067](adr/ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md) |
| Da dove parte il primo lotto? | **Tre insieme**: grounding delle mappe, parser prosa → JSON, estrattore differenziale dei fatti. Il banco di misura resta, spostato a valle (lotto D) |

---

## §1 · La misura di partenza, presa il 2026-09-16

Nessuno di questi numeri è stimato. La colonna di destra di §10 dice con quale
comando si riprende.

| Cosa | Numero |
|---|---:|
| Script Python in `scripts/` | **52** |
| Moduli condivisi in `scripts/dmcore/` | **12** |
| Righe Python totali | **23.371** |
| Tool nel manifest | **61** |
| Tool dichiarati `stdlib_only` | **50 su 61** |
| Tool con uno smoke test in CI | **36** |
| Test unitari, verdi in ~15 s | **742** (5 saltati) |
| ADR accettate o proposte | **51** |
| Skill | **18** |
| Piani in `plans/` | **38** |
| Mappe: master e SVG generati | **18 master → 40 SVG**, allineati |
| Schede con statblocco leggibile da una macchina | **157 su 157** (124 col blocco, 27 coi numeri altrove, 6 non-creature) |
| Simboli nella legenda funzionale, fonte unica | **63**, di cui 18 `blocks_movement`, 12 `blocks_sight` |
| File markdown scritti a mano | **1.123**, circa **1,89 M parole** |
| Parole in `campaign/` | **~94.000** |
| **File in `campaign/sessions/`** | **2** |
| **Chiamate a un modello linguistico in tutto `scripts/`** | **0** |
| Script che aprono un socket | **1** (`comfyui_batch.py`, verso `127.0.0.1:8188`, immagini) |

Due righe di questa tabella reggono da sole metà dell'audit, e vale la pena
isolarle.

**`campaign/sessions/` contiene due file.** Uno è il log di una sessione, l'altro
è una ricostruzione retroattiva. Il documento sorgente propone di indicizzare
quella cartella in un database vettoriale per «verificare la cronologia degli
eventi». Su due file, l'indice costa più della lettura.

**Zero chiamate a un modello linguistico.** L'intera architettura che il
documento descrive come «stato attuale» presuppone che ci sia un LLM dentro la
catena. Non c'è, e non per dimenticanza: il modello è un client che legge le
skill e chiama i tool via MCP, e i tool restano deterministici perché la sera
della sessione il portatile del DM può non avere rete (ADR-0037).

---

## §2 · L'audit del documento sorgente

### 2.1 · La tabella comparativa, riga per riga

Il cuore del documento è una tabella «Stato Attuale nel Repo» contro «Pipeline
Ibrida Avanzata». Le quattro righe della colonna sinistra sono quattro
affermazioni verificabili. Nessuna regge.

| Riga | Cosa dice il documento | Cosa c'è nel repo, al 2026-09-16 | Verdetto |
|---|---|---|---|
| **Routing** | *«Script manuali + prompt degli agenti isolati»* | [ADR-0002](adr/ADR-0002-cli-unica-dm-orchestratore.md): `scripts/dm.py` è la CLI unica, orchestra e non contiene logica. [ADR-0041](adr/ADR-0041-instradamento-delle-skill-con-un-gate.md): l'instradamento delle skill è un principio **con un gate** che conta le 18 skill e boccia l'elenco che ne dimentica una. [ADR-0045](adr/ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md): ogni lotto dichiara engine, effort e qualità attesa. [ADR-0030](adr/ADR-0030-server-mcp-sui-tool.md): 61 tool esposti a un client MCP con sei difese nominate | ❌ **falso** |
| **Statblock** | *«Testo Markdown inserito a mano o via LLM generico»* | [ADR-0021](adr/ADR-0021-statblocchi-machine-readable.md) + `scripts/schemas/statblock.schema.json`; `extract_statblocks.py --check` è un gate di CI e dà **157 su 157**; `derive_statblocks.py` deriva i numeri dalle tabelle SRD 3.5 con collaudo sul GS, e [ADR-0033](adr/ADR-0033-derivare-e-dichiararlo.md) spiega perché **propone e non scrive** | ❌ **falso** |
| **Mappe** | *«Griglie emoji o export manuale JSON/UVTT»* | `compile_map_json.py` (709 righe) compila un contratto JSON rigido in un master; `render_map_svg.py` (1.480 righe) rende in SVG di qualità di stampa; `export_uvtt.py` esporta muri, porte e luci per Foundry e Roll20; `import_ultraclear.py` (1.215 righe) risale dall'ASCII al JSON con un rapporto di conflitti; `render_map_blender.py` fa il piano di scena 3D, **confrontato byte a byte in CI**. La CI esegue il giro completo JSON → master → SVG → UVTT a ogni PR | ❌ **falso** |
| **Coerenza** | *«Controllo manuale tramite `docs/INDEX.md`»* | `validate_docs.py` è un gate che verifica che ogni percorso citato nei documenti d'ingresso esista; `--sorgenti` lo estende a tutti i markdown scritti a mano; `decisioni_dm.py --check` ([ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md)) fa rossa la CI se l'elenco delle decisioni aperte diverge dai piani; `state_apply.py` scrive il canone solo dentro regioni marcate, col triplo vincolo di [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md) | ❌ **falso** |

Una tabella comparativa è utile quanto è vera la colonna di sinistra. Questa
misura la distanza da un repo di luglio, e il repo di luglio non c'è più.

### 2.2 · Le percentuali

Il documento presenta due tabelle di rendimento atteso: precisione e richiamo per
componente, punteggio F1 per caratteristica tattica. I numeri che cita sono
**100%**, **95-98%**, **85-90%**, **98%**, **~92%**, **~95%**, **80%**.

Nessuno di questi numeri è misurato. Non esiste un corpus di riferimento, non
esiste un protocollo di annotazione, non esiste un annotatore, e il documento non
cita un esperimento. Le due fonti in nota sono un articolo divulgativo sulla mean
Average Precision nella visione artificiale e un blog sui tool di validazione: né
l'uno né l'altro ha visto questo repo.

Il difetto peggiore è di categoria.

**Il «100% garantito da parser Python» non è una statistica.** È un exit code. Un
validatore che rifiuta un input malformato ha una precisione di uno per
costruzione, perché non esiste l'evento «falso positivo» in un dominio dove la
verità è definita dallo schema. Chiamarlo F1 confonde una proprietà con una
misura.

**L'F1 presuppone una verità di riferimento, e sulla prosa generativa non c'è.**
Precisione e richiamo si calcolano contro un insieme atteso. Per una scena di
gioco non esiste l'insieme delle frasi giuste; esiste il giudizio del DM al
tavolo, che è un'annotazione umana e va raccolta, non postulata. Questo repo ci è
già passato: [ADR-0036](adr/ADR-0036-misurare-il-miglioramento-non-lo-stato.md)
racconta una metrica quantitativa ragionevole (la varianza della lunghezza delle
frasi) che **peggiorava sulla versione che il DM aveva giudicato migliore**, e la
decisione che ne è seguita è di misurare la differenza fra due versioni dello
stesso testo invece di fissare soglie assolute.

**La media armonica di due numeri inventati è un terzo numero inventato.** Il
documento sostiene che l'architettura «massimizza l'F1» e lo argomenta con le
percentuali che l'architettura dovrebbe produrre. Il ragionamento si chiude su se
stesso.

⚠️ Questo non toglie nulla all'architettura proposta, che in due punti su quattro
è buona. Toglie il diritto di citarne le prestazioni prima di averle misurate, ed
è la ragione per cui il lotto D di questo piano esiste.

### 2.3 · Tre proposte che il repo ha già valutato e respinto, con l'ADR

Il documento le presenta come novità. Sono domande a cui esiste una risposta
scritta, e ignorarle costerebbe due volte: una per costruire, una per smontare.

**Pydantic e Jsonformer** per vincolare l'output dell'LLM allo schema. Il repo è
stdlib-only per [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md), e il
motivo non è ideologico: *«un `pip install` che fallisce alle 20:45 è un booklet
che non si stampa»*. Le uniche due librerie ammesse sono `pyyaml` e `Pillow`, e
la prima è dichiarata un debito. La validazione contro schema rigido **esiste
già** in `compile_map_json.py` e in `scripts/schemas/*.json`, scritta a mano
proprio per questo.

**Il container headless-chrome per i PDF.** Esiste da luglio
([ADR-0004](adr/ADR-0004-homebrewery-self-hosted.md),
`scripts/booklet-container/`, `scripts/homebrew-local/`), ed è **già stato
superato** sul binario da stampa da Typst
([ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md),
[ADR-0026](adr/ADR-0026-vendoring-pacchetti-typst.md),
[ADR-0027](adr/ADR-0027-imposizione-con-pdfcpu.md)), che compila in CI con la
versione fissata e produce i segnalibri. Proporre headless-chrome come traguardo
è indietro di due ADR.

**Il RAG sulla cartella delle sessioni.** Due file. E un database vettoriale
porterebbe con sé un modello di embedding, cioè dei pesi, cioè
[ADR-0019](adr/ADR-0019-licenza-dei-pesi-non-del-software.md) e la verifica dei
termini, più una dipendenza di rete o un pacchetto Python fuori dalla stdlib. Il
bisogno vero che c'è sotto — *«l'LLM non deve dimenticare i fatti accertati»* —
è reale, ed è il lotto C. Non richiede embedding.

### 2.4 · La generazione procedurale: giusta per un problema che questo repo non ha

Il documento propone Wave Function Collapse o partizione binaria dello spazio per
generare la planimetria. Sono algoritmi solidi, e risolvono *«inventami una
pianta plausibile»*.

Le mappe di questo repo nascono dall'altro verso. La Tomba di Belkram, il Portale
della Forgia Eterna, i campi drow: la planimetria discende dalla scena, e la
scena esiste prima. Il collo di bottiglia non è inventare una pianta, è
**trascrivere la pianta che il DM ha già in testa** senza che scivoli di un
quadretto. Il documento lo scopre da solo più avanti, nel passaggio migliore che
contiene: *«senza questo estrattore intermedio, la pipeline non avrebbe una base
di verità geometrica su cui poggiare»*.

Il WFC resta un utensile possibile per una mappa greenfield, e finisce in §7 fra
i futuri, non fra i lotti.

---

## §3 · Le tre cose che il documento ha visto giuste

### 3.1 · Il ponte fra la prosa e la geometria è il collo di bottiglia vero, e non esiste

È l'osservazione migliore del documento, e arriva nell'ultimo blocco:

> *«Se un DM inserisce un prompt in prosa — "una cripta nanica rettangolare di
> 15x10 metri, con un altare consacrato a Dumathoin sul fondo, protetto da due
> pilastri di pietra che offrono copertura, e una botola nascosta nell'angolo
> est" — un algoritmo deterministico puro non può comprenderlo, e un LLM generico
> farebbe allucinazioni sulle misure.»*

La catena cartografica del repo è completa **a valle** del contratto JSON:
`compile_map_json` dipinge, `render_map_svg` rende, `export_uvtt` esporta,
`import_ultraclear` risale dall'ASCII. **A monte** del contratto non c'è niente.
Chi scrive la spec la scrive a mano, quadretto per quadretto, e quando a scriverla
è un modello il risultato è la classe di difetti che il repo ha già catalogato:
la riga `17` duplicata di `Portale-Forgia-L2` (D12 di `RICERCA-MESTIERE`), la
mappa che dichiarava 40×40 con righe da 24 a 26 celle (D6 di `RIPRESA-PR`).

### 3.2 · Il validatore di grounding non c'è, e da quattro giorni i dati per farlo ci sono

Il documento chiede tre controlli che nessuno script esegue: risoluzione delle
sovrapposizioni, verifica dei flussi di movimento con un A\*, larghezza dei
corridoi per le creature di taglia Grande.

Verificato leggendo il codice: `compile_map_json.validate()` controlla simboli,
limiti della griglia, rettangoli e piazzamenti. Non controlla che due oggetti
solidi non occupino la stessa cella, non controlla che una stanza sia
raggiungibile, non sa cosa sia una taglia. `validate_maps.py` guarda la
tracciabilità e l'allineamento fra master e SVG, non la geometria di gioco.

Il motivo per cui questo lotto arriva **adesso** e non a luglio sta in una data:
il **2026-09-12** la decisione D1 di `PIANO-VENDIBILITA` ha ratificato la legenda
funzionale ([ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md)), e da
allora `scripts/legend.yaml` porta per ognuno dei 63 simboli i campi
`blocks_movement`, `blocks_sight`, `cover`, `obscurement`, `move_cost`. Il
grounding non ha bisogno di inventare un modello del mondo: lo legge da
`dmcore.legenda`, che è già la fonte unica e ha già il suo gate.

### 3.3 · L'estrattore differenziale: la parte buona del RAG, senza il database vettoriale

Il documento la descrive come fase 1 della pipeline della prosa:

> *«Estrae la differenza netta fra ciò che l'LLM deve obbligatoriamente citare —
> la presenza di Capitana Lorana, il countdown dell'orologio dei drow a 4/8 — e le
> regole meccaniche attive… i fatti chiave non sono lasciati alla memoria volatile
> dell'LLM, ma iniettati come vincoli strutturali.»*

Questo è un estrattore deterministico su `campaign/state.md`, che è un file
strutturato con regioni marcate e con il March Clock già mantenuto da
`state_apply.py`. Non serve un embedding per leggere un orologio.

E la seconda metà dell'idea è quella che vale di più: se la lista dei fatti
obbligatori esiste **prima** che il testo sia scritto, allora dopo si può
**verificare** che il testo li contenga. Quello è un richiamo misurabile, sullo
stesso testo, senza corpus di riferimento e senza annotatore. È l'unico dei
numeri del documento che si può rendere vero a costo basso.

---

## §4 · L'architettura, dopo la decisione del DM

```
 [ DM: prosa, vincoli di scena, stato della campagna ]
                       │
                       ▼
 ┌─────────────────────────────────────────────┐
 │  AGENTE (client)  skill + server MCP        │   ← nessuna chiamata dagli script
 │  produce CANDIDATI, mai artefatti           │
 └─────────────────────────────────────────────┘
        │  JSON mappa            │  prosa di scena
        ▼                        ▼
 ┌──────────────────┐     ┌──────────────────────┐
 │ compile_map_json │     │  fatti_scena         │  lotto C
 │  + GROUNDING     │ A   │  --verifica FILE     │
 └──────────────────┘     └──────────────────────┘
        │ rifiuta o accetta            │ elenca i fatti mancanti
        ▼                              ▼
 ┌─────────────────────────────────────────────┐
 │  CATENA DETERMINISTICA (già in casa)        │
 │  master → render_map_svg → export_uvtt      │
 │  validate_prosa · validate_modules · CI     │
 └─────────────────────────────────────────────┘
                       │
                       ▼
            [ artefatto del repo, sotto gate ]

 ┌ ponte opzionale, ADR-0067 ────────────────────────────┐
 │ scripts/llm_bridge.py — mai in CI, degrada pulito,    │  lotto E
 │ produce candidati che rientrano dalla porta normale   │
 └───────────────────────────────────────────────────────┘
```

Rispetto al documento sorgente, il router LLM sparisce, perché
l'instradamento è già un principio con un gate (ADR-0041) e una dichiarazione per
lotto (ADR-0045), e un secondo instradamento a runtime sarebbe una seconda fonte
di verità. Il mixer a tre fasi si riduce a una: l'LLM propone, il codice
convalida, e se il codice boccia il modello riprova sapendo perché. La fase di
critica con un secondo modello resta possibile, e resta un ponte.

---

## §5 · Le tre fasi

| Fase | Cosa risponde | Stato |
|---|---|---|
| **A · Audit e prerequisiti** | Cosa c'è davvero, cosa manca, cosa è già stato deciso contro, e quanto rumore produrrebbe un gate nuovo sul canone di oggi | ✅ **fatta**. §1, §2, §3 e la misura di rumore del lotto A, che ha trovato un difetto vero in un modulo standalone e un prerequisito che il piano non aveva visto (lotto A0) |
| **B · Costruzione** | I lotti A, B, C, E di §6, ognuno con la sua dichiarazione ADR-0045 e il suo collaudo scritto prima di partire | ⬜ da aprire |
| **C · Collaudo e misura** | Il lotto D: il banco che rende vere o false le percentuali del documento sorgente, e il protocollo con cui si rimisurano | ⬜ da aprire |

Le tre fasi non sono sequenziali per intero. Il collaudo di ciascun lotto di fase
B è scritto **prima** del codice, come chiede
[ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md); il lotto D di
fase C misura l'insieme, ed è l'unico che ha bisogno che i lotti precedenti
esistano.

---

## §6 · I lotti

Ogni lotto dichiara engine, effort e qualità attesa (ADR-0045), il collaudo, e
cosa **non** fa. La classe è quella del registro dei lotti: **M** meccanico, **R**
ricognizione, **C** costruzione, **G** giudizio, **K** canone.

### Lotto A · Il grounding geometrico

> **Classe C** · engine: sessione principale, effort medio · **qualità: alta, il
> difetto arriva al tavolo** — una mappa con una stanza irraggiungibile si scopre
> quando quattro giocatori ci sbattono contro.

**Dove vive.** Un modulo nuovo `scripts/dmcore/grounding.py` con funzioni pure, e <!-- validate-docs: futuro -->
due consumatori: `compile_map_json.py --grounding` (prima che la spec diventi un
master) e `validate_maps.py` (sui 18 master esistenti). Il modulo legge le
proprietà dei simboli da `dmcore.legenda`, che è la fonte unica di ADR-0048.
Nessun nuovo set di simboli, nessuna costante cablata.

**I quattro controlli.**

**G1 · Sovrapposizioni.** Due elementi che occupano la stessa cella quando almeno
uno ha `blocks_movement: true`. Oggi `paint()` li sovrascrive in silenzio secondo
l'ordine di precedenza, e il secondo sparisce senza che nessuno lo dica. Il
controllo non ripara: elenca la cella, i due elementi e chi ha vinto.

**G2 · Raggiungibilità.** Visita in ampiezza sulle celle non bloccanti, a partire
dalle celle dichiarate come ingresso (le `units` dei PG, o in mancanza il bordo
transitabile). Ciò che resta non visitato è una sacca isolata: si riporta con
l'elenco delle celle e l'etichetta della regione, se ne ha una. Il documento
sorgente chiede un A\*; per «esiste un cammino da qui a lì» l'A\* è una visita in
ampiezza con un'euristica che non serve, e la visita costa meno codice.
Movimento a 8 direzioni, **con l'eccezione 3.5 della diagonale fra due celle
bloccanti ortogonalmente adiacenti**, che non si attraversa.

**G3 · Larghezza del varco per taglia.** Richiede un campo nuovo e opzionale nel
contratto: `units[].taglia`, con valori `media` (predefinito), `grande`,
`enorme`, `mastodontica`. Il controllo rifà G2 per ogni taglia presente,
erodendo le celle transitabili del raggio richiesto, e dice quale unità non
raggiunge quale zona. È il caso concreto del documento sorgente, che nomina il
rinoceronte infuso di pietra di Hella: una creatura Grande in un corridoio da un
quadretto non passa, e sulla griglia non si vede.

**G4 · Porte che non connettono.** Una cella `door` con meno di due lati
transitabili distinti è quasi sempre un errore di trascrizione. Vale come avviso,
non come errore.

### La misura di rumore: fatta il 2026-09-16, e ha cambiato il lotto

Il piano diceva che il primo atto sarebbe stata una misura. È stata eseguita con
un prototipo usa-e-getta, non committato, su **tutti i 18 master (40 griglie)**.

| Segnale | Conteggio grezzo |
|---|---:|
| Sacche isolate dall'area principale | **97** (1.301 celle) |
| ↳ di cui **con dentro un segnalino di creatura** | **58** |
| ↳ di cui vuote (nicchie, vuoti nella roccia) | 26 |
| ↳ di cui **artefatto della legenda incompleta** | 13 |
| Porte che non connettono due lati | **15** |
| Griglie dove una creatura Grande non attraversa tutto l'aperto | **12** |
| Simboli usati nei master e **assenti dalla legenda** | **14 distinti**, 527 celle |

⚠️ **Il prototipo ha sbagliato due volte prima di dare questi numeri, e le due
volte contano.** Alla prima passata dava **zero** celle bloccanti sulla fortezza
di Hammerfist, cioè un risultato assurdo: `dmcore.legenda.simboli()` espone la
vista **di rendering**, non `function`, e il modulo **non ha un accessore per
`blocks_movement`**. Alla seconda dava **194 porte cieche**: la regola contava
una porta come ostacolo per la porta accanto, e due battenti adiacenti si
bocciavano a vicenda. Corretta, il numero è **15**. Un gate che nascesse
con quei difetti dentro produrrebbe 194 falsi allarmi al primo giro e viene spento la
settimana dopo.

**Il difetto vero, trovato e verificato a mano.**
`STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/mappe/tarsilia-stalle.md` disegna
**tre box da 12 quadretti chiusi su quattro lati** da `🏰` (muratura piena:
blocca vista e movimento), **senza un solo `🚪`**. Dentro due di essi stanno
`🟢` a **H12** e **L12**, che il master stesso nomina: *«H12 box del cavallo»*,
*«Il cavallo della contrada»*, *«Regina, la mula»*. E la tattica scritta nello
stesso file dice che l'obiettivo di Sfregio è *«azzoppare il cavallo con la pasta
corrosiva (1 round intero, cavallo fermo)»*, che richiede di stargli **adiacente**.
Esportata con `export_uvtt.py`, quella mappa mette su Foundry tre muri opachi e
invalicabili attorno all'animale: **la scena centrale dell'incontro non si può
giocare**. Il rimedio è piccolo e la legenda ce l'ha già: `🚪` sul fronte di ogni
box, oppure `🧱` per i divisori, che è `blocks_movement: false` e `cover: half`,
cioè esattamente un separé da stalla.

🔎 **Rimisurato il 2026-09-24, e la causa è più precisa di così.** Una visita in
ampiezza dalla porta sul canale (B9), con `blocks_movement` letto da
`scripts/legend.json`: **220 celle libere, 184 raggiungibili, 36 isolate**, cioè
i tre box da 12, con dentro i due `🟢`. Il master è identico al compilato del
JSON, quindi il difetto sta in `tarsilia-stalle.json`: le cinque linee interne
portano `🏰` e l'etichetta *«Assi di separazione dei box, alte 1,5 m: copertura,
si scavalcano con Acrobazia CD 10»*, la stessa regola che il testo del Giorno 2
§6 scrive per i box. Il simbolo contraddice l'etichetta che gli sta accanto:
`🏰` è alto 4,5 m nel render e blocca tutto, `🧱` è alto **1,5 m** e dà
copertura. Con `🧱` sulle cinque linee le celle isolate vanno a **zero** e
l'export passa da **36 a 20 muri**. La correzione è contenuto del modulo, e
aspetta la conferma del DM.

✅ **Corretta il 2026-09-24, variante B scelta dal DM**: `🧱` sulle cinque
linee interne e una `🚪` sul fronte di ogni box (H10, L10, P10), perché il
testo del Giorno 2 fa «liberare» la mula e un box senza porta non si apre. Si è
toccato solo il JSON; master, SVG, `.uvtt` e booklet del DM sono rigenerati.
Celle isolate **0 su 249**; l'export ha **20 muri e 5 porte**. Il `README` delle
mappe dava 32 muri alle stalle e 24 alla Ruota: erano fermi al 17 agosto, e la
ratifica di ADR-0048 del 12 settembre aveva riesportato gli `.uvtt` senza
aggiornarlo. Oggi dicono 20 e 28.

**Cosa cambia nel lotto.** Il rumore **non** è zero, quindi il gate nasce non
bloccante come `validate_lingua`, `validate_prosa` e `validate_tipografia`. Ma
soprattutto nasce un prerequisito che questo piano non aveva visto.

### Lotto A0 · Chiudere la legenda, prima del gate

I **14 simboli fuori legenda** non hanno `function`, quindi il codice li tratta
come transitabili. Da lì vengono 13 delle 97 sacche: la più vistosa è il
`CORTILE INTERNO` di `ARC07-MAPPE-DEFINITIVO`, dove le prime tre righe sono
`☁` e `🐉` — **il cielo sopra il cortile**, che diventa una «zona irraggiungibile»
perché nessuno ha mai detto al codice cos'è una nuvola.

Entrambe piccole, entrambe prima di G1-G4:

1. I 14 simboli entrano in `scripts/legend.yaml` con la loro `function`, oppure
   il gate della legenda li rifiuta esplicitamente. Un simbolo che sta in una
   griglia e non nella legenda è già oggi un buco di ADR-0048 che nessuno conta.
2. `dmcore.legenda` prende l'accessore che gli manca — il fatto neutro
   `blocks_movement`, accanto a `muri()`, `porte()` e `pericoli()`. Senza, ogni
   consumatore se lo ricalcola dal JSON grezzo, che è la malattia che ADR-0048
   ha curato.

**Collaudo.** Test in `scripts/tests/test_grounding.py`: per ciascuno dei quattro <!-- validate-docs: futuro -->
controlli, una fixture che **deve** essere bocciata e una che **deve** passare
(la forma di `test_gate_bocciano.py`). Più il giro sui 18 master, col conto
riportato nella riga di CHANGELOG.

**Cosa non fa.** Non ripara, non sposta, non sfoltisce. Il documento sorgente
propone *«una regola di sfoltimento o riposizionamento automatico lungo i nodi
liberi del grafo»*: spostare un altare di una cella cambia le distanze di una
scena scritta, e il repo ha già deciso su questa classe di scelte con ADR-0033
(`derive_statblocks` propone e non scrive).

**Costo stimato.** 150-250 righe nel modulo, 100-150 di test, più la riga nel
manifest e il passo in CI. Nessuna dipendenza.

### Lotto B · Il ponte fra la prosa e il contratto geometrico

> **Classe C+G** · engine: sessione principale, effort alto sul contratto,
> **qualità: alta** — è la parte che l'LLM sbaglia per natura, e il collaudo è
> l'unica difesa.

Il documento chiama fase 1 un «LLM Parser di dominio tattico». Con la decisione
del DM su ADR-0067, questo lotto **non è uno script che chiama un modello**. È
tre cose.

**B1 · Il contratto d'estrazione, scritto.** Un riferimento nuovo nella skill
`rumblingstone-mapmaking` che dice al modello esattamente cosa deve produrre
leggendo la prosa del DM: la conversione metri → quadretti al passo di
`scale_m_per_square` (1,5), la mappatura degli oggetti nominati sui simboli della
legenda funzionale, la regola per cui **ciò che non è nella prosa non si
inventa** e finisce in `notes`. Il vincolo è lo schema che esiste già,
`scripts/schemas/tactical_map.schema.json`, non un DSL nuovo.

**B2 · Il ciclo di rifiuto.** `compile_map_json --validate-only` esiste e rifiuta
con errori precisi; il lotto A gli aggiunge il grounding. Il ciclo diventa:
il modello emette JSON, il codice boccia con l'elenco dei difetti, il modello
corregge. Non serve codice nuovo, serve che il ciclo sia **documentato come il
modo normale di lavorare**, in `docs/guides/GUIDA-MAPPE.md` e nella skill.

**B3 · Il banco di prova dell'estrazione.** Cinque prose di riferimento scritte
dal DM, con accanto il JSON che un'estrazione corretta deve produrre, in
`scripts/tests/fixtures/`. Non si confrontano i due JSON byte a byte, perché una
pianta corretta ammette varianti: si confrontano gli **invarianti** che il
documento sorgente nomina bene — dimensioni della griglia, numero di elementi per
classe, proprietà d20 di ciascun elemento, raggiungibilità. È questo che rende
misurabile il richiamo dell'estrazione, e il numero che ne esce sostituisce il
«90%» del documento.

**Collaudo.** Le cinque prose passano B3 con il conto degli invarianti mancati
riportato. Zero significa estrazione completa; qualunque altro numero è il dato
di partenza da migliorare, non un fallimento.

**Cosa non fa.** Non genera la planimetria. La prosa del DM la contiene già.

### Lotto C · L'estrattore differenziale dei fatti

> **Classe C** · engine: sessione principale, effort medio · **qualità: media**,
> perché un fatto dimenticato si vede leggendo e non arriva al tavolo come un
> muro sbagliato.

**Lo script.** `scripts/fatti_scena.py`, stdlib, due modi. <!-- validate-docs: futuro -->

`--per <scena>` legge `campaign/state.md` (le regioni marcate `auto:`, il March
Clock, i PG e i loro artefatti), i log in `campaign/sessions/` e gli archi
dichiarati, ed emette l'elenco dei fatti che una scena **deve** citare: PNG
presenti, orologi attivi con il loro valore, artefatti in gioco, conseguenze
aperte. Uscita in markdown per un umano e in JSON per un agente.

`--verifica FILE` prende un testo già scritto e riporta quali fatti dell'elenco
non compaiono, con la forma sotto cui li ha cercati.

**Perché non è un RAG.** Il corpus sono due file di sessione e un file di stato
strutturato. La domanda non è *«trovami i passaggi rilevanti in un milione di
parole»*, è *«leggi il valore dell'orologio e il nome della capitana»*, e quella è
una lettura, non un recupero.

**Collaudo.** `--verifica` su tre testi di canone già approvati dal DM: l'elenco
dei mancanti deve essere vuoto o spiegabile. Un estrattore che segnala fatti
mancanti su una scena che il DM ha giudicato buona è tarato male, ed è la stessa
prova che ADR-0036 ha applicato alla burstiness.

**Cosa non fa.** Non riscrive e non corregge. Il filtro anti-cliché che il
documento propone come «mixer deterministico» esiste già: è `validate_prosa.py`,
753 righe, e ADR-0036 spiega perché misura la differenza fra due versioni invece
di imporre soglie.

### Lotto D · Il banco di misura

> **Classe G** · engine: sessione principale, effort alto · **qualità: alta** —
> è il lotto che decide se i numeri del repo si possono citare.

Sostituisce le percentuali del documento sorgente con misure che hanno un
protocollo. Tre famiglie, e solo la prima è una statistica vera.

| Famiglia | Cosa si misura | Come | Sostituisce |
|---|---|---|---|
| **Geometria** | conteggio dei difetti per classe sui master | lotto A sui 18 master | il «100%» e il «98%» |
| **Richiamo dei fatti** | fatti obbligatori citati su fatti dovuti | `fatti_scena --verifica` (lotto C) | il «~96%» e l'«80%» |
| **Tic della prosa** | differenza fra due versioni dello stesso testo | `validate_prosa --prima-dopo` (esiste) | il «~90%» e il «bias quasi nullo» |

La quarta famiglia che il documento presuppone, cioè la qualità della prosa
contro un riferimento, **resta fuori** finché non esiste un corpus annotato dal
DM. È la decisione **D4**.

**Collaudo.** Ogni numero pubblicato porta accanto il comando che lo riproduce,
come fa la tabella di §1. Un numero senza comando non entra.

### Lotto E · Il ponte, se serve

> **Classe C** · engine e effort da decidere quando il bisogno esiste ·
> **qualità: alta**, è una superficie d'esecuzione.

`scripts/llm_bridge.py` secondo le sette condizioni di <!-- validate-docs: futuro -->
[ADR-0067](adr/ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md). Il primo uso
sensato è B1: prosa in ingresso, JSON candidato in uscita, `--validate-only` e
grounding come porta.

**Questo lotto non parte finché A, B e C non sono chiusi.** Il motivo è che con A
e B in casa il ciclo funziona già a mano, e allora si saprà se il ponte fa
risparmiare davvero o se automatizza un passaggio che costa trenta secondi. È la
decisione **D3**.

---

## §7 · Quello che non si fa, e perché

| Proposta del documento | Decisione | Motivo |
|---|---|---|
| Vincolare l'output con **Pydantic** o **Jsonformer** | ❌ no | ADR-0037. La validazione contro schema rigido esiste già, scritta a mano, in `compile_map_json.py` e `scripts/schemas/` |
| **Database vettoriale** su `campaign/sessions/` | ❌ no | Due file. Porterebbe pesi (ADR-0019) e una dipendenza fuori stdlib. Il bisogno sotto è il lotto C |
| **Router LLM** a runtime | ❌ no | ADR-0041 (gate sull'instradamento) e ADR-0045 (engine e effort dichiarati per lotto). Un secondo instradamento sarebbe una seconda fonte di verità, ed è la classe di difetto che ADR-0048 ha appena chiuso sulla legenda |
| **Generazione procedurale** WFC/BSP della planimetria | 🔵 futuro, non lotto | Risolve «inventami una pianta». Qui la pianta esiste prima della mappa. Torna utile per una mappa greenfield: si riapre quando ne serve una |
| **Container headless-chrome** come catena PDF | ❌ no, esiste ed è superata | ADR-0004 l'ha costruita a luglio; ADR-0020, 0026 e 0027 l'hanno superata su Typst per il binario da stampa |
| **Riscrittura automatica** della prosa da un LLM critico | ❌ no | ADR-0036. Si misura la differenza fra due versioni; la riscrittura resta di chi firma il testo |
| Pubblicare le **percentuali** del documento | ❌ no | §2.2. Tornano quando il lotto D le ha prodotte, col comando accanto |
| **Mixer a tre fasi** con due modelli in parallelo | 🔵 ridotto a uno | L'LLM propone, il codice convalida. La seconda passata di critica resta possibile come ponte (lotto E), col suo costo visibile |

---

## §8 · I rischi, detti prima

**Il rischio più grande è la superficie.** Il repo ha 61 tool e 742 test. Ogni
script nuovo è manutenzione per sempre, e questo piano ne propone due più un
modulo. La difesa è che nessuno dei tre duplica qualcosa: `grounding.py` legge da
`dmcore.legenda`, `fatti_scena.py` legge da `campaign/state.md` che
`state_apply.py` già mantiene, e il ponte è opzionale per costruzione.

**Il grounding può bocciare il canone.** Le 18 mappe master sono state giocate o
sono pronte per il tavolo. Se G2 trova sacche isolate in una mappa che al tavolo
ha funzionato, il difetto può essere del validatore, della trascrizione o della
mappa, e sono tre rimedi diversi. Per questo la prima misura precede il codice
del gate, e per questo il gate nasce non bloccante. È la decisione **D1**.

**Il banco di misura dipende dal DM.** Il lotto D vale quanto l'annotazione che
lo alimenta, e l'unico annotatore possibile è chi sta al tavolo. Un banco che il
DM non ha tempo di alimentare è un banco che produce numeri vecchi, e i numeri
vecchi sono peggio di nessun numero. È la decisione **D4**.

**Il ponte è una superficie d'esecuzione.** Vale per lui ciò che
`plans/SPEC-SERVER-MCP.md` dice per il server MCP. Le sette condizioni di
ADR-0067 sono un'ipotesi tarata su un precedente solo, `comfyui_batch.py`, e il
lotto E dirà quale ha retto.

**Il documento sorgente potrebbe non essere l'ultimo.** La sua tabella era
indietro di due mesi, e la prossima analisi esterna lo sarà di nuovo. La difesa
non è scrivere questo piano: è che §1 porta i comandi per rimisurare, così una
prossima analisi può partire dai numeri veri invece che dalla memoria.

---

## §9 · Le decisioni che restano al DM

<!-- decisioni-dm: PIPELINE-IBRIDE -->

| # | Fase | Domanda |
|---|---|---|
| D1 | Lotto A | **Cosa fa il grounding quando trova un difetto in una mappa di canone già giocata?** 🔎 **Non è più una domanda astratta: la misura del 2026-09-16 c'è.** 97 sacche isolate su 40 griglie, di cui **58 con dentro un segnalino di creatura**, 15 porte cieche, 12 griglie che una creatura Grande non attraversa. Una sola sacca è stata verificata a mano fino in fondo, ed **era un difetto vero**: i tre box delle stalle di Tarsilia, chiusi da `🏰` senza `🚪`, con dentro il cavallo che la tattica scritta dice di raggiungere. Le altre 57 **non sono state triangolate**, e il conto grezzo non dice quante siano difetti. Le tre risposte restano: (a) **segnala e basta**, gate non bloccante, canone invariato; (b) **segnala e si correggono le mappe**, cioè toccare griglie approvate; (c) **si esenta il canone esistente**, col rischio dell'esenzione silenziosa che ADR-0032 §1 ha già evitato una volta. 🔵 La proposta resta **(a)**, e adesso con un motivo misurato: 58 segnali non triangolati non possono bloccare una CI. Ma Tarsilia va corretta comunque, perché è un modulo standalone destinato a uscire. ✅ **Tarsilia corretta il 2026-09-24** (variante B: `🧱` e una porta per box); la domanda di D1 resta aperta per le altre 57 |
| D2 | Lotto B · B1 | **Dove vive il contratto d'estrazione dalla prosa?** Dentro `skills/rumblingstone-mapmaking/SKILL.md`, dove ogni agente lo vede sempre e paga i token a ogni conversazione, oppure in un file di riferimento caricato solo quando la skill instrada là. `measure_tokens.py` sa dare il costo delle due strade sullo stesso testo: la domanda si può decidere con un numero invece che a occhio |
| D3 | Lotto E | **Il ponte `llm_bridge.py` si costruisce, o ADR-0067 resta scritta e il codice aspetta?** La proposta è aspettare: con A e B chiusi il ciclo funziona a mano, e allora si vedrà se il ponte fa risparmiare davvero. Serve una risposta solo quando A e B sono chiusi |
| D4 | Lotto D | **Quante scene il DM è disposto ad annotare?** Il banco di misura della prosa esiste solo se qualcuno dice quali testi sono buoni, e l'unico che può dirlo è chi li ha visti funzionare al tavolo. Con zero scene annotate il lotto D copre le prime tre famiglie di §6 e la quarta resta fuori, il che è una risposta legittima e va detta invece che rimandata |

---

## §10 · Come si rimisurano i numeri di §1

```bash
ls scripts/*.py | wc -l                       # script top-level
ls scripts/dmcore/*.py | wc -l                # moduli condivisi
cat scripts/*.py scripts/dmcore/*.py | wc -l  # righe Python
python3 scripts/tools_manifest.py --check     # tool, conformita del manifest
python3 -m unittest discover -s scripts/tests # test
ls plans/adr/ADR-0*.md | wc -l                # ADR
ls -d skills/*/ | wc -l                       # skill
python3 scripts/validate_maps.py              # master e SVG
python3 scripts/extract_statblocks.py --check # schede con statblocco
python3 scripts/decisioni_dm.py --check       # decisioni aperte contro i piani
grep -rlE "urllib|http\.client|socket\." scripts/*.py   # chi apre un socket
```

Il conto dei simboli della legenda si legge da `scripts/legend.json`, che è
generato da `scripts/legend.yaml` e confrontato in CI da
`scripts/build_legend.py --check`.

---

## §11 · Traccia delle fonti

**Il documento sorgente** è stato consegnato dal DM il 2026-09-16 come file ODT e
**non è committato**: pesa 3,1 MB, è una trascrizione di conversazione, e il repo
non archivia i sorgenti delle analisi esterne (stessa scelta di
`RICERCA-TOOL-LGM-2026`). Ciò che conta di quel documento è citato qui alla
lettera, fra virgolette, nei punti in cui una parafrasi cambierebbe il senso.

**I numeri di §1** vengono dal checkout a `b701d39`, 2026-09-16, con i comandi di
§10.

**Le ADR citate** sono tutte in `plans/adr/`. Dove questo piano dice che una
proposta è già stata decisa contro, il link porta alla decisione e non a un
riassunto.
