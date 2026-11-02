# Strumenti liberi per misurare, confrontare e generare le mappe

**Data**: 2026-10-22 · **Richiesta**: il DM (Jfs), due messaggi dello stesso
giorno: strumenti e tecniche gratuiti e open source che rendano le mappe
misurabili in modo deterministico secondo standard accettati; poi anche
generatori, o combinazioni di generatori e riparatori deterministici, che
alzino la qualità e la coerenza misurate dallo standard.
**Stato**: esperimento. Niente è entrato in `scripts/` né nello standard; gli
script stanno in questa cartella e non sono committati.

Le affermazioni hanno il link della fonte. Quello che è dedotto da chi scrive
porta **[INFERRED]**.

## In breve

- **Il confronto fra due versioni** della stessa mappa è quello che manca di
  più e costa meno: `confronta_versioni.py` dà Hamming e Jaccard sulle classi
  di cella, le transizioni (muro→pavimento…), la NCD, il delta del voto e dei
  rilievi, e un SVG con le due rese affiancate e le celle cambiate cerchiate.
  Nessuna dipendenza nuova. **Da adottare.**
- **Le metriche di space syntax** (profondità media e integrazione sul grafo di
  movimento e su quello di visibilità, intelligibilità) sono lo standard
  accettato in architettura e urbanistica e sono state applicate ai livelli dei
  videogiochi; si calcolano con `tcod` e `scipy`, che il repo ha già, in 60
  righe. **Da adottare come metriche senza soglia**, come vuole il metodo di
  Smith e Whitehead; non nel voto.
- **Generatore + riparatore + misura** funziona sui luoghi nuovi: sei bozze a
  seme fisso, voto da 90-97 a 95-100, due giri identici al byte. Sulla mappa di
  canone il riparatore alza il voto (95→98) **peggiorando la coerenza**: posa
  una catasta che il testo approvato (D48) non prevede. Lì la risposta giusta è
  una `@deroga`, non la riparazione.
- Il riparatore ha trovato **un difetto dello standard**: due varchi nella
  stessa stanza valgono «due ingressi». Va corretto in `qualita_mappe.py`.
- **Non valgono il costo**, oggi: OR-Tools (80 MB più pandas, stesso risultato
  dell'avido sul caso provato), clingo, WFC, depthmapX, i framework PCG di
  ricerca, networkx e shapely (già rifiutati da ADR-0084).
- **Non si misurano** in modo accettato: il divertimento, l'estetica, la
  coerenza con il testo del modulo e con il canone, la plausibilità della
  funzione di un luogo.

## 1. Cosa c'era già

Per non ripetere il lavoro, prima di cercare si è letto:

- lo standard (`skills/rumblingstone-mapmaking/references/standard-qualita-mappe.md`)
  e [ADR-0098](../../adr/ADR-0098-la-qualita-delle-mappe-si-misura-con-uno-standard.md):
  le fonti di Jaquays, Dormans, Smith e Whitehead, Liapis e altri, Mawhorter,
  NSS, Paizo, Reynolds sono già citate; `qualita_mappe.py` misura anelli,
  ingressi, vicoli, fila indiana, copertura, distanza fra le fazioni, scala,
  densità dei simboli e quota. Smith e Whitehead sono citati, ma *leniency* e
  *linearity* non sono calcolate;
- [ADR-0084](../../adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md)
  e `esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md`: `tcod`, `scipy`,
  `numpy` sono entrate; `networkx` (più lenta del Tarjan in casa, 461 ms contro
  209) e `shapely` (nessun effetto al tavolo) sono state misurate e rifiutate;
  Watabou, Azgaar, mapgen4, Tiled hanno già la licenza letta (§6);
- `PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md`: LDtk e Tiled valutati come schema e
  non come dipendenza (§2.5-bis); WFC rifiutato (ADR-0082: manca un set di
  tessere con le regole d'adiacenza); **V9** (generatore BSP e automi
  cellulari) e **V10** (riparazione proposta in diff) decisi con D4 e mai
  scritti («nessun codice»);
- il collaudo calcola già **M4**, la frazione media del percorribile visibile
  da ogni cella con lo shadowcasting di `tcod`: è l'isovista media. Non è una
  metrica nuova e qui non si ripropone.

Quello che manca, quindi: la misura della **configurazione** (quanto un punto
è profondo rispetto al resto), il **confronto fra versioni**, la **simmetria**,
la **diversità dei pattern**, e il pezzo che genera o ripara.

## 2. Gli strumenti, con la licenza letta alla fonte

«Det.» = dà lo stesso risultato a ogni esecuzione con lo stesso input.
«Provato» = installato o già presente, ed eseguito in questa ricerca.

### Misura e analisi

| Strumento | Licenza (fonte) | Cosa fa per le mappe | Det. | pip senza GPU | Provato | Chi lo usa o cita |
|---|---|---|---|---|---|---|
| `tcod` 21.2.1 | BSD-2 ([ADR-0084](../../adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md)) | shadowcasting simmetrico: il grafo di visibilità della VGA | sì | sì, già nel repo | **sì** | il collaudo (M4) |
| `scipy.sparse.csgraph` 1.18.1 | BSD-3 (già nel repo) | cammini minimi non pesati sul grafo: profondità media, integrazione | sì | sì, già nel repo | **sì** | il collaudo (M1, M2) |
| `scikit-image` 0.26 | BSD ([PyPI](https://pypi.org/project/scikit-image/)) | SSIM e differenza di pixel fra due PNG | sì | sì, già nel repo | no (manca un rasterizzatore su questa macchina) | `misura_resa.py` |
| `networkx` 3.7 | BSD-3 ([PyPI](https://pypi.org/project/networkx/)) | centralità, cicli, articolazioni | sì | sì | no | rifiutata da ADR-0084 per prestazioni; non serve alla VGA |
| `shapely` 2.2 | BSD-3 ([PyPI](https://pypi.org/project/shapely/)) | geometria di poligoni | sì | sì | no | rifiutata da ADR-0084 |
| `pathfinding` 1.0.22 | MIT ([LICENSE](https://raw.githubusercontent.com/brean/python-pathfinding/main/LICENSE), [PyPI](https://pypi.org/project/pathfinding/)) | A*, Dijkstra su griglia | sì | sì | no | doppione: il collaudo ha Dijkstra 5-10-5 e `tcod` ha A* |
| **depthmapX** | GPL-3 ([README](https://github.com/SpaceGroupUCL/depthmapX)) | VGA, analisi assiale e di segmento, agenti: l'implementazione di riferimento della space syntax | sì [INFERRED] | no (C++/Qt) | no | UCL Bartlett ([pagina](https://www.ucl.ac.uk/bartlett/architecture/research/space-syntax/depthmapx)); [Wikipedia, VGA](https://en.wikipedia.org/wiki/Visibility_graph_analysis) |
| `alcyon` (R) | GPL-3 ([CRAN](https://cran.r-project.org/web/packages/alcyon/index.html)) | la libreria `sala` di depthmapX da R: VGA, isoviste, assiale | sì [INFERRED] | no (R) | no | Koutsolampros, Turner, Varoudis e altri |
| `topologicpy` 0.9.86 | LGPL-3 ([LICENSE](https://raw.githubusercontent.com/wassimj/topologicpy/main/LICENSE)) | modellazione spaziale per l'architettura, VGA | sì [INFERRED] | sì, ma pesante | no | citato in [Wikipedia, VGA](https://en.wikipedia.org/wiki/Visibility_graph_analysis) |
| `VisiLibity` 1.0.10 | LGPL ([PyPI](https://pypi.org/project/VisiLibity/)) | visibilità esatta in poligoni | sì | sì | no | serve a piante vettoriali, non a griglie |
| `momepy` 1.0 | BSD-3 ([PyPI](https://pypi.org/project/momepy/)) | morfologia urbana (isolati, strade, tessuto) | sì | sì | no | utile solo per le mappe di città [INFERRED] |
| Isovist_App ([isovists.org](https://isovists.org/user-guide/4-2-4-occlusivity/)) | «All Rights Reserved» | isoviste di Benedikt (area, perimetro, occlusività, drift) | — | no | no | escluso dalla licenza |
| **ETPKLDiv** | MIT ([LICENSE](https://raw.githubusercontent.com/amidos2006/ETPKLDiv/master/LICENSE), [README](https://github.com/amidos2006/ETPKLDiv)) | divergenza KL fra le distribuzioni di pattern di tessere (Lucas e Volz 2019) | sì | no (C# e JS) | **riscritta in Python**, 30 righe | [Lucas e Volz 2019](https://arxiv.org/pdf/1905.05077) |
| `pcg_benchmark` | MIT ([README](https://github.com/amidos2006/pcg_benchmark)) | qualità, diversità, controllabilità su 12 problemi (Zelda, regole arcade…) | sì [INFERRED] | da git, numpy e PIL | no | [Khalifa et al. 2025](https://arxiv.org/pdf/2503.21474) |
| `gym-pcgrl` | MIT ([LICENSE](https://raw.githubusercontent.com/amidos2006/gym-pcgrl/master/LICENSE)) | ambienti RL per livelli, con metriche (regioni, cammino) | sì per le metriche | sì, con gym | no | [PCGRL](https://arxiv.org/pdf/2001.09212) |

### Generazione e riparazione

| Strumento | Licenza (fonte) | Cosa fa | Det. | pip senza GPU | Provato | Chi lo usa o cita |
|---|---|---|---|---|---|---|
| **OR-Tools** 9.15 (CP-SAT) | Apache-2.0 ([LICENSE](https://raw.githubusercontent.com/google/or-tools/stable/LICENSE), [PyPI](https://pypi.org/project/ortools/)) | solver a vincoli: piazzare porte, coperture, blocchi con vincoli duri | sì con 1 thread, seme e **tempo deterministico** | sì, 80 MB più pandas | **sì** | Google |
| `clingo` 5.8.2 (ASP) | MIT ([LICENSE](https://raw.githubusercontent.com/potassco/clingo/master/LICENSE.md), [PyPI](https://pypi.org/project/clingo/)) | answer set programming: lo spazio delle mappe valide descritto per regole | sì [INFERRED] | sì, 6,8 MB | installato, import verificato, **non provato**, poi disinstallato | [Smith e Mateas 2011](https://course.ccs.neu.edu/cs5150f14/readings/smith_asp4pcg.pdf) |
| `python-constraint` 1.4 | BSD ([LICENSE](https://raw.githubusercontent.com/python-constraint/python-constraint/main/LICENSE), [PyPI](https://pypi.org/project/python-constraint/)) | CSP piccoli, puro Python | sì | sì | no | — |
| `python-sat` | MIT ([PyPI](https://pypi.org/project/python-sat/)) | SAT; è il motore tipico dei generatori a vincoli | sì | sì | no | — |
| **Sturgeon** | MIT ([LICENSE](https://raw.githubusercontent.com/crowdgames/sturgeon-pub/main/LICENSE), [repo](https://github.com/crowdgames/sturgeon-pub)) | livelli a tessere da vincoli appresi e progettati, con raggiungibilità | — | da git | no | [Cooper, AIIDE 2022](https://ojs.aaai.org/index.php/AIIDE/article/view/21944), [MKIII](https://www.pcgworkshop.com/archive/cooper2023sturgeon.pdf) |
| **WaveFunctionCollapse** | MIT ([LICENSE](https://raw.githubusercontent.com/mxgmn/WaveFunctionCollapse/master/LICENSE)) | sintesi da un esempio per pattern N×N e vincoli d'adiacenza | sì a seme fisso | no (C#) | no | *Bad North*, *Caves of Qud*, *Townscaper* ([README](https://github.com/mxgmn/WaveFunctionCollapse)) |
| `wfc_2019f` | MIT ([LICENSE](https://raw.githubusercontent.com/ikarth/wfc_2019f/master/LICENSE)) | WFC in Python, di ricerca (Karth) | sì a seme fisso | no (git e conda, non PyPI) | no | — |
| DeBroglie | MIT ([LICENSE](https://raw.githubusercontent.com/BorisTheBrave/DeBroglie/master/LICENSE.txt)) | WFC con vincoli di cammino e conteggio | sì | no (C#) | no | Boris the Brave |
| BSP, automi cellulari 4-5 | tecniche, nessuna licenza | interni a stanze e corridoi; caverne | sì a seme fisso | — | **sì, scritti qui** | [Jeremy Kun](https://www.jeremykun.com/2012/07/29/the-cellular-automaton-method-for-cave-generation/), V9 del piano |
| Generazione ciclica (*Unexplored*) | tecnica | anello grande fra ingresso e meta, regole di riscrittura, chiave e serratura, grafo poi griglia | sì a seme fisso | — | no | [Boris the Brave](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/), [Game Developer](https://www.gamedeveloper.com/design/unexplored-s-secret-cyclic-dungeon-generation-) |
| Grammatiche di missione e spazio (Dormans) | tecnica; il suo Ludoscope non è libero | missione come grafo, poi spazio | sì a seme fisso | — | no | [Dormans 2010](https://www.pcgworkshop.com/archive/dormans2010adventures.pdf) |

### Generatori e programmi di mappe della community

| Strumento | Licenza (fonte) | Nota |
|---|---|---|
| Watabou (MFCG, Mansion, One Page Dungeon) | uscite libere anche per uso commerciale, credito gradito ma non obbligatorio ([watabou su itch](https://watabou.itch.io/procgen-mansion/comments?before=5)); il codice attuale non è pubblicato; il vecchio `TownGeneratorOS` è GPL-3 ([LICENSE](https://raw.githubusercontent.com/watabou/TownGeneratorOS/master/LICENSE)) | non deterministico per noi: il seme sta nel sito; si importa il JSON (`import_watabou.py`) |
| Azgaar Fantasy Map Generator | MIT ([LICENSE](https://raw.githubusercontent.com/azgaar/Fantasy-Map-Generator/master/LICENSE)) | regioni inventate; Faerûn è canone e non si genera |
| mapgen4 (Red Blob Games) | Apache-2.0 ([LICENSE](https://raw.githubusercontent.com/redblobgames/mapgen4/master/LICENSE)) | come sopra |
| Dungeon Scrawl | proprietario e gratuito ([AlternativeTo](https://alternativeto.net/software/dungeon-scrawl/about)); l'export UVTT è per gli abbonati Pro ([blog](https://blog.dungeonscrawl.com/uvtt-export)) | non è open source |
| DungeonFog | proprietario, abbonamento 5-10 $ al mese ([AlternativeTo](https://alternativeto.net/software/dungeonfog/about)) | escluso |
| dungeon-revealer | ISC ([LICENSE](https://raw.githubusercontent.com/dungeon-revealer/dungeon-revealer/master/LICENSE)) | nebbia di guerra al tavolo; non genera né misura |

### Formati aperti e validatori

| Formato | Licenza (fonte) | Validatore | Per il repo |
|---|---|---|---|
| Universal VTT (`.uvtt`, `.dd2vtt`, `.df2vtt`) | nessuna specifica pubblicata trovata; Roll20 descrive i campi (muri, portali aperti/chiusi, barriere, luci, risoluzione) e rimanda ad Arkenforge senza link ([Roll20](https://help.roll20.net/hc/en-us/articles/41643201127831-Universal-Virtual-Tabletop-UVTT-Support)) | nessuno trovato | `export_uvtt.py` c'è già. Uno schema JSON scritto in casa servirebbe solo se un import fallisce [INFERRED] |
| LDtk | MIT ([LICENSE](https://raw.githubusercontent.com/deepnight/ldtk/master/LICENSE)) | schema JSON ufficiale, pensato anche per validare ([ldtk.io](https://ldtk.io/docs/game-dev/json-overview/json-schema/)) | idea già presa come schema (PIANO, §2.5-bis); nessun motivo nuovo per esportare |
| Tiled TMX/JSON | editor GPL, `libtiled` e i visualizzatori BSD-2 ([COPYING](https://raw.githubusercontent.com/mapeditor/tiled/master/COPYING)); formato documentato ([JSON](https://doc.mapeditor.org/en/latest/reference/json-map-format/)) | `pytiled-parser` MIT ([PyPI](https://pypi.org/project/pytiled-parser/)), `pytmx` LGPL-3 ([PyPI](https://pypi.org/project/pytmx/)) | non serve: il master è la griglia emoji |

pip raggiunge l'indice: le licenze dei pacchetti sono lette dall'API JSON di
PyPI, quelle dei repository dal file `LICENSE` grezzo.

## 3. La prova delle metriche nuove

`metriche_nuove.py` calcola, su tre mappe fuori da ARC-08, quello che
`qualita_mappe.py` non calcola. Le mappe: PF-3 *Corridoio del Fuoco*
(`Portale-Forgia-L2-REVISED-UltraClear.md`), M7-F *La fucina grande, 372*
(`hammerfist-372-1372/`), M7-C *La tenda del comando*. Risultati in
`out/metriche-prova.json`.

### Le formule

- **VGA** ([Turner et al. 2001](https://discovery.ucl.ac.uk/id/eprint/160/);
  [Wikipedia](https://en.wikipedia.org/wiki/Visibility_graph_analysis)): nodi
  le celle percorribili, archi fra le celle che si vedono (shadowcasting
  simmetrico di `tcod`, la stessa trasparenza di M4). Connettività = celle
  visibili; profondità media MD = Σd/(k−1). Formule da
  [Ostwald 2011](https://link.springer.com/content/pdf/10.1007/s00004-011-0075-3.pdf):
  RA = 2(MD−1)/(k−2), RRA = RA/D_k, integrazione = 1/RRA. Il D_k è la formula
  di Krüger, riportata da memoria e verificata solo sul valore D_7 = 0,34 di
  Ostwald **[INFERRED]**. Clustering di Turner: archi fra i vicini visibili su
  k(k−1).
- **Intelligibilità**: r² fra connettività e integrazione; «un sistema
  intelligibile è quello in cui gli spazi ben connessi sono anche ben
  integrati» (Hillier 1996, citato da
  [Dalton e Bafna 2003](https://discovery-pp.ucl.ac.uk/1104/1/SIC.pdf.pdf)).
- **Integrazione d'accesso**: le stesse formule sul grafo di movimento del
  collaudo (diagonale che non passa l'angolo). La correlazione fra le due
  integrazioni rende la *visibility/accessibility discrepancy* che
  [Martin 2014](https://nottingham-repository.worktribe.com/output/722027/a-spatial-analysis-of-the-jba-headquarters-in-splinter-cell-double-agent)
  usa sui livelli di *Splinter Cell* **[INFERRED: l'abstract non dà la
  formula]**.
- **Simmetria** (una delle metriche di
  [Summerville et al. 2017](https://webdocs.cs.ualberta.ca/~santanad/papers/2017/summervilleMSOL17.pdf)):
  quota di celle uguali allo specchio orizzontale, verticale e alla rotazione,
  sulle classi di cella (muro, ostacolo, porta, scala, pericolo, copertura,
  creatura, pavimento).
- **Pattern 2×2** ([Lucas e Volz 2019](https://arxiv.org/pdf/1905.05077)):
  distribuzione delle finestre, entropia in bit, KL simmetrizzata 0,5/0,5
  contro il corpus come in ETPKLDiv, epsilon 10⁻⁶.
- **Leniency adattata** ([Smith e Whitehead 2010](https://www.pcgworkshop.com/archive/smith2010analyzing.pdf):
  +1 buchi, nemici, cadute; −0,5 piattaforme mobili): qui +1 nemico e pericolo
  maggiore, +0,5 pericolo minore, −0,5 copertura, per 100 celle **[INFERRED:
  traduzione dal platform alla tattica, non validata]**.

### I numeri

| Misura | PF-3 Corridoio del Fuoco | M7-F Fucina grande 372 | M7-C Tenda del comando |
|---|---:|---:|---:|
| celle percorribili | 667 | 362 | 493 |
| voto di `qualita_mappe.py` | 100 | 95 | 97 |
| VGA, profondità media | 1,12 | 1,24 | 1,74 |
| VGA, intelligibilità r² | 0,83 | 0,68 | 0,87 |
| VGA, clustering medio | 0,94 | 0,80 | 0,73 |
| accesso, profondità media (passi) | 18,7 | 9,8 | 13,7 |
| accesso, integrazione media | 0,40 | 0,71 | 0,51 |
| correlazione vista/accesso (VAD) | 0,36 | 0,72 | 0,35 |
| isovista media (m²) | 1.315 | 618 | 434 |
| simmetria orizz. / vert. / rot. | 0,95 / 0,88 / 0,89 | 0,89 / 0,92 / 0,82 | 0,86 / 0,84 / 0,82 |
| pattern 2×2 distinti, entropia (bit) | 75 · 3,70 | 54 · 3,47 | 72 · 4,20 |
| KL contro il corpus | 2,01 | 1,21 | 1,45 |
| leniency per 100 celle | 49,2 | −0,6 | −3,1 |

**Determinismo.** `python3 metriche_nuove.py --prova` calcola tutto due volte
nello stesso processo; due esecuzioni da shell danno lo stesso file al byte
(`cmp`, impronta `12430bd6c15787a7`). Le tre mappe e la scansione del corpus
richiedono 9 s; CM-2, 814 celle, 5 s.

**Che cosa dicono.** La tenda (M7-C) è la più profonda alla vista (1,74: c'è
da girare attorno ai teli) e la più intelligibile; il Corridoio del Fuoco è un
grande vuoto visivo (si vede quasi tutto da ovunque) ma il più profondo a piedi
(18,7 passi: la lava costringe ai ponti), e lo dice la VAD bassa (0,36):
quello che si vede non è quello che si raggiunge. La fucina è simmetrica al
90% su entrambi gli assi; la checklist alla Jaquays chiede piante
«asimmetriche», ma una fucina nanica regolare è plausibile [INFERRED]. La
leniency di PF-3 esplode perché ogni cella di lava conta come pericolo: per le
mappe con terreno letale esteso la traduzione non regge.

**Limiti misurati.**

- L'integrazione HH della VGA cresce con il numero di celle (94,9 su 667
  celle, 9,5 su 493): il D_k è tarato sui grafi assiali piccoli. Fra mappe
  diverse si confronta la profondità media, non l'integrazione HH [INFERRED].
  Sulla stessa mappa in due versioni l'integrazione resta confrontabile.
- La KL dipende dal corpus del momento: la prima versione dello script contava
  anche le bozze di questa cartella e la KL della fucina passava da 1,20 a
  0,85. Ora `plans/esperimenti/` è escluso; il numero è riproducibile **a
  corpus fermo**, e va registrato con l'impronta del corpus [INFERRED].
- L'isovista media è M4 del collaudo scritta in m²: non è nuova.

## 4. Il confronto fra due versioni

### Il metodo

`confronta_versioni.py VECCHIA.md[:N] NUOVA.md[:N] --out DIR [--profonde]`

| Misura | Che cosa dice | Fonte |
|---|---|---|
| Hamming sui simboli e sulle classi, in celle e quota | quanto è cambiato; le due differiscono quando si cambia un simbolo con un altro della stessa funzione | distanza di Hamming, definizione |
| Jaccard per classe (muro, blocco, percorribile, copertura, creature, porte, pericolo) | quale parte è cambiata: con il muro a 1,0 e le creature a 0 è cambiata la disposizione, non la pianta | indice di Jaccard, definizione; già usato in `orientamento-e-dipendenze-2026-10/RISULTATI.md` |
| transizioni di classe (M→., .→M, .→U…) | in che verso: un muro aperto, una copertura posata, una creatura spostata | — |
| NCD con lzma | distanza d'informazione fra le due griglie come testo, senza scegliere le classi | Li et al. 2004, *The similarity metric* [INFERRED: citato da memoria] |
| delta del voto, delle metriche e dei rilievi di `qualita_mappe.py` | se la nuova è migliore secondo lo standard, e quale rilievo è sparito o comparso | ADR-0098 |
| con `--profonde`, delta di `metriche_nuove.py` | se la configurazione è cambiata (profondità, simmetria, pattern) | §3 |
| SVG affiancato | le due rese del renderer vero, celle cambiate cerchiate sulle due: rosso dove compare un blocco, verde dove sparisce, ambra il resto | — |

Le due rese sono gli SVG di `render_map_svg.render_svg`, annidati con gli id
prefissati perché i pattern non si scontrino; i riquadri stanno sulla
geometria del renderer (cella 28 px, margine 46, griglia a 80 px dall'alto).
Gli SVG sono XML valido; su questa macchina non c'è né Chrome né Inkscape né
`rsvg-convert`, quindi il PNG e il diff di pixel (SSIM di `scikit-image`) non
sono stati provati. Dove c'è un rasterizzatore, `export_map_png.py` più SSIM
sulle due PNG darebbe la mappa delle differenze visive, compresi i cambi di
tema e di resa che la griglia non vede [INFERRED].

### Tre confronti veri

| Coppia | Voto | Celle cambiate | Jaccard (muro · percorribile · copertura · creature) | Transizioni | Profondità a piedi |
|---|---|---:|---|---|---|
| M7-F 372 → M7-F 1372 (stessa sala, mille anni dopo) | 95 → 95 | 46 (7,0%) | 1,00 · 1,00 · 0,33 · 0,00 | U→. 20, .→U 18, .→K 8 | 9,77 → 9,77 |
| M7-F 372 → M7-F riparata (§5) | 95 → 98 | 8 (1,2%) | 0,97 · 0,98 · 1,00 · 1,00 | .→M 8 | 9,77 → 9,96 |
| bozza BSP seme 1 → riparata | 93 → 100 | 6 (0,9%) | 0,99 · 0,97 · — · 1,00 | M→. 6 | 17,35 → 15,12 |

La prima riga mostra che il confronto distingue da solo una riedizione di
pianta da una di scena: fra il 372 e il 1372 la fucina è la stessa al muro, e
cambiano le creature (da 20 PG a 8 PG e 10 nemici) e otto coperture. Il voto
non lo vede (95 e 95); il Jaccard sì.

### Come presentarle

1. In cima il riepilogo in una riga: voti prima e dopo, celle cambiate, rilievi
   spariti e comparsi.
2. Le due rese affiancate con le celle cerchiate (`confronto.svg`).
3. La tabella delle transizioni e dei delta delle metriche, solo le righe che
   cambiano.
4. Per la versione per i giocatori, lo stesso confronto sulla vista
   `@vista giocatori`, perché un cambio del DM non scopra un segreto.

## 5. Generatore + riparatore deterministico + misura

### La pipeline

```
seme ─► GENERATORE ─► bozza ─► RIPARATORE ─► mappa ─► MISURA
        BSP o grotta            salita sul voto,       voto, rilievi,
        (solo luoghi nuovi)     celle di canone        delta, SVG
                                fisse
```

`genera_ripara.py` mette insieme i tre pezzi.

- **Generatore.** `bsp`: partizione binaria, stanze nelle foglie, corridoi
  sull'albero ricoprente minimo dei centri (Prim con i pareggi decisi dalle
  coordinate). Esce un albero, senza anelli, apposta: il primo anello lo deve
  mettere il riparatore, come chiede Dormans. `grotta`: automa 4-5, 45% di
  riempimento, cinque passi, la regione più grande. Il caso viene da
  `random.Random(seme)`; PG a ovest, nemici nella stanza più lontana a passi,
  obiettivo accanto.
- **Riparatore.** Salita (hill climbing) sul voto di `qualita_mappe.py`. Le
  mosse sono poche e ordinate: scavare un passaggio dritto di 1-4 celle di
  muro fra due tratti distanti almeno 8 passi (la scorciatoia di Jaquays);
  aprire un ingresso sulla cornice; posare un blocco 4×2, 2×4 o 3×3 staccato
  da tutto; posare una copertura dove non ce n'è entro 2 quadretti; chiudere
  un vicolo vuoto. A ogni passo si prova ogni mossa, si tiene quella con il
  voto più alto e, a parità, con meno celle; una mossa che fa comparire un
  errore si scarta. Le celle di canone (creature, oggetti, porte, scale, e con
  `--canone` anche il pavimento a contatto con loro) non si toccano.
- **Il plateau.** Il voto si muove a scatti: «un solo ingresso» resta un
  rilievo finché gli ingressi non sono due, quindi il primo passo non alza il
  voto e la salita si ferma. Il riparatore ordina le mosse a parità di voto con
  un secondo numero, quanto la mappa si è avvicinata alle soglie (ingressi
  fino a 2, un anello strutturale, distanza fra le fazioni sotto 54 m, vicoli
  vuoti, copertura) **[INFERRED: scelta di progetto, non una metrica
  pubblicata]**. Il voto resta il primo criterio e non può scendere.

### I risultati

`python3 genera_ripara.py prova` fa tutto il giro due volte in due cartelle
(`out/pipeline/giro1`, `giro2`): rapporti con la stessa impronta
(`532b58d1fc8b467f`) e file identici al byte; 36 s per i due giri.

| Bozza | Voto prima | Voto dopo | Rilievi risolti | Mosse | Valutazioni |
|---|---:|---:|---|---|---:|
| BSP seme 1 | 93 | **100** | fazioni/lontane, un-ingresso | scava 4, due ingressi | 48 |
| BSP seme 2 | 97 | **100** | un-ingresso | due ingressi, scava 2 | 56 |
| BSP seme 3 | 93 | **100** | fazioni/lontane, un-ingresso | scava 2, due ingressi | 68 |
| grotta seme 1 | 97 | **100** | un-ingresso | due ingressi, una copertura | 128 |
| grotta seme 2 | 90 | **98** | m2/vuoto, senza-anelli, un-ingresso (resta m4) | un blocco 3×3, due ingressi, due blocchi 4×2 | 117 |
| grotta seme 3 | 95 | 95 | nessuno | un ingresso, due blocchi | 80 |
| **M7-F 372, canone** | 95 | 98 | senza-anelli (resta m4) | una catasta 📦 4×2 in I11-L12 | 26 |

Sulla grotta del seme 3 un secondo ingresso a 10 passi dal primo non c'è, e
il voto resta 95. Il riparatore però ha cambiato la mappa lo stesso: un
ingresso (U01) e sedici stalagmiti in due blocchi, tutti a voto invariato,
tenuti solo perché alzano il numero di avvicinamento (la copertura). È un
difetto del prototipo: a fine giro le mosse che non hanno portato a un voto più
alto vanno tolte, e la versione per il repo deve farlo [INFERRED].

### Il solver a vincoli

`coperture_cpsat.py` scrive come vincoli il problema delle coperture: la
quota di percorribile con una copertura entro 2 quadretti (M1 del collaudo)
sopra una soglia, nessuna copertura nuova a contatto con un'altra, densità di
icone sotto il 30%, minimo numero di coperture. CP-SAT con un thread, seme 0 e
**tempo deterministico** (5 unità, non secondi d'orologio: con il tetto in
secondi la soluzione dipende dalla macchina, ed è il primo errore fatto in
questa prova).

| Grotta seme 2 | M1 prima | Coperture CP-SAT | Avido | M1 dopo | M2 prima → dopo | Voto |
|---|---:|---:|---:|---:|---|---|
| soglia 0,85 | 0,64 | 4 (J06 K11 P14 Y16) | 4 | 0,85 | 0,37 → 0,07 | 90 → 92 |
| soglia 0,95 | 0,64 | 7 | 7 | 0,95 | 0,37 → 0,02 | 90 → 92 |

Due giri, stesse celle. CP-SAT chiude «FEASIBLE», non «OPTIMAL», e trova lo
stesso numero dell'avido. Sul compito provato **non migliora niente** e costa
80 MB più pandas.

### Dove il generatore e il riparatore peggiorano le cose

1. **La fucina di canone.** Il riparatore toglie il rilievo `senza-anelli`
   posando una catasta di casse 4×2 in mezzo alla sala. Il voto sale da 95 a
   98, e la mappa peggiora: il testo dice «Misure, pilastri e numero di forge
   sono quelli di questa griglia, approvati con D48», e nella sala di lavoro
   c'è ora un ingombro che nessuno ha scritto. Anche lo space syntax lo vede:
   la profondità a piedi sale da 9,77 a 9,96 e l'isovista media scende da 618
   a 521 m². Una sala a colonne si gira attorno ai pilastri: è il caso della
   `@deroga` che PF-2 e CM-2 già hanno («sala ottagonale aperta…»). Il
   riparatore sul canone serve a **proporre**, come chiede V10, mai ad
   applicare.
2. **Il voto si può ingannare.** La prima versione del riparatore apriva due
   varchi a due quadretti l'uno dall'altro nella stessa stanza (L01 e N01 della
   BSP seme 1): per `qualita_mappe.py` sono due «tratti» del bordo, quindi due
   ingressi, e il rilievo `struttura/un-ingresso` spariva. Per Jaquays è un
   ingresso solo. Ora il riparatore chiede 10 passi fra un ingresso nuovo e
   quelli che ci sono; **lo standard va corretto allo stesso modo**. Lo stesso
   vale per il numero di avvicinamento: sulla grotta del seme 3 ha fatto posare
   sedici stalagmiti senza alzare il voto di un punto.
3. **Le bozze non hanno una funzione.** BSP e automi fanno stanze e caverne
   senza un perché: niente dormitorio, cucina, acqua, aria. Il primo passo del
   giro dello standard («la funzione») non lo fa nessun generatore; la bozza è
   uno spazio da riempire, non un luogo.
4. **Il testo del modulo.** Un generatore non legge il read-aloud: una porta
   scavata dal riparatore può contraddire la descrizione dell'area, e nessuna
   metrica se ne accorge. Il collaudatore a freddo (V11-bis) è il controllo.

## 6. Raccomandazioni

### Da adottare

1. **`confronta_mappe.py`** in `scripts/`, da `confronta_versioni.py`: nessuna
   dipendenza nuova, risponde alla richiesta di vedere vecchia e nuova
   affiancate. Il PNG con SSIM si aggiunge dove c'è un rasterizzatore.
2. **Metriche di configurazione senza soglia** nel JSON di
   `qualita_mappe.py`, dietro un'opzione `--profonde` (la VGA è quadratica:
   5 s su 814 celle): profondità media a piedi e alla vista, intelligibilità,
   VAD, simmetria, entropia dei pattern 2×2. Si usano per confrontare le mappe
   fra loro e le versioni, come vuole Smith e Whitehead; nel voto no, perché
   nessuna fonte dà una soglia per le battlemap.
3. **La correzione di `struttura/un-ingresso`**: due tratti di bordo aperti
   contano come ingressi distinti solo se distano almeno 10 passi a piedi (o
   danno su componenti diverse). È un difetto trovato, non un'opinione.
4. **V9 e V10 dal prototipo**: `genera_ripara.py` è una base già
   deterministica per il generatore di bozze dei luoghi nuovi (arco 09,
   incontri casuali) e per la riparazione proposta, con l'uscita in diff (il
   confronto del punto 1) e mai scritta su un master.

### Da non adottare, per ora

| Che cosa | Perché |
|---|---|
| OR-Tools | stesso risultato dell'avido sul caso provato; 80 MB più pandas. Riaprire se i vincoli si moltiplicano (porte + coperture + blocchi insieme) |
| clingo, python-constraint, python-sat, Sturgeon | stessa ragione: nessun problema misurato che l'avido o la salita non risolvano |
| WFC (mxgmn, wfc_2019f, DeBroglie) | manca il set di tessere con le regole (ADR-0082); da un esempio WFC copierebbe le mappe del corpus, comprese quelle derivate da *Red Hand of Doom* |
| depthmapX, alcyon, topologicpy | la VGA che serve sta in 60 righe con `tcod` e `scipy`; depthmapX resta il riferimento con cui verificare i numeri una volta [INFERRED] |
| `pcg_benchmark`, `gym-pcgrl` | framework per confrontare generatori fra ricercatori, sui loro problemi |
| networkx, shapely, python-pathfinding | già misurati e rifiutati (ADR-0084), o doppioni di `tcod` |
| export LDtk o Tiled | il master è la griglia; UVTT basta ai VTT del tavolo |

### Che cosa diventerebbe obsoleto

Niente, misurabilmente. L'isovista media sarebbe un doppione di M4 e non va
aggiunta. Il confronto a occhio fra due PNG diventa superfluo quando c'è
`confronta_mappe.py`, ma non era uno strumento del repo.

### Che cosa non si misura in modo accettato

- **Il divertimento e la difficoltà percepita.** Sui livelli di *Mario*
  [Summerville et al. 2017](https://webdocs.cs.ualberta.ca/~santanad/papers/2017/summervilleMSOL17.pdf)
  trovano metriche vicine all'accordo fra due giudici umani per difficoltà e
  divertimento (il numero di nemici: ρ = 0,72 e 0,42), ma su un platform e con
  giudizi raccolti apposta. Per le battlemap nessuno l'ha fatto.
- **L'estetica.** Nello stesso studio è il criterio più lontano dall'accordo
  umano (ρ = 0,23 la metrica migliore).
- **La coerenza con il testo del modulo e con il canone**, e la
  **plausibilità della funzione** (chi dorme dove, da dove arriva l'acqua).
  Restano alla lista dei controlli a vista dello standard, al collaudatore a
  freddo e al DM.
- **Lo space syntax** è accettato in architettura, urbanistica, archeologia
  ([Wikipedia](https://en.wikipedia.org/wiki/Space_syntax)) e applicato ai
  videogiochi (Martin 2014), ma le sue correlazioni con il comportamento sono
  state misurate su persone che camminano in edifici e città, non su miniature
  in turni. È una misura accettata della configurazione; non è una prova che
  la mappa giochi meglio [INFERRED].

## 7. I file di questa cartella

| File | Che cosa fa |
|---|---|
| `_comune.py` | lettura delle griglie con il parser del renderer, classi di cella, voto in memoria |
| `metriche_nuove.py` | §3; `--prova` per le tre mappe e il controllo dei due giri |
| `confronta_versioni.py` | §4; JSON e SVG affiancato |
| `genera_ripara.py` | §5; `prova` per i due giri completi |
| `coperture_cpsat.py` | §5, il solver a vincoli (richiede `ortools`) |
| `out/` | i risultati: `metriche-prova.json`, `pipeline/` (bozze, riparate, copie della fucina e delle gallerie, `esito.json`), `confronto-*/` (JSON e SVG) |

Le copie di M7-F e M7-E in `out/pipeline/` servono perché `@collega` trovi la
gemella; gli originali non sono stati toccati.

**Pacchetti installati.** `ortools` 9.15 (con `pandas`, `protobuf`, `absl-py`)
è rimasto installato nell'ambiente di questa sessione per `coperture_cpsat.py`;
`clingo` 5.8.2 è stato installato e poi tolto senza essere usato. `networkx` e
`scikit-image` c'erano già. Nessun file del repo dichiara le dipendenze nuove.

## Fonti

- Turner, Doxa, O'Sullivan, Penn, *From isovists to visibility graphs*, 2001: https://discovery.ucl.ac.uk/id/eprint/160/ · https://en.wikipedia.org/wiki/Visibility_graph_analysis
- Ostwald, *The Mathematics of Spatial Configuration*, 2011: https://link.springer.com/content/pdf/10.1007/s00004-011-0075-3.pdf
- Dalton e Bafna, *The syntactical image of the city*, 2003: https://discovery-pp.ucl.ac.uk/1104/1/SIC.pdf.pdf
- Space syntax, campi d'uso: https://en.wikipedia.org/wiki/Space_syntax
- Martin, *A spatial analysis of the JBA headquarters in Splinter Cell: Double Agent*, 2014: https://nottingham-repository.worktribe.com/output/722027/a-spatial-analysis-of-the-jba-headquarters-in-splinter-cell-double-agent
- Benedikt, occlusività (Isovist_App): https://isovists.org/user-guide/4-2-4-occlusivity/
- depthmapX: https://github.com/SpaceGroupUCL/depthmapX · https://www.ucl.ac.uk/bartlett/architecture/research/space-syntax/depthmapx · alcyon: https://cran.r-project.org/web/packages/alcyon/index.html
- Lucas e Volz, *Tile Pattern KL-Divergence*, 2019: https://arxiv.org/pdf/1905.05077 · ETPKLDiv: https://github.com/amidos2006/ETPKLDiv
- Summerville et al., *Understanding Mario*, 2017: https://webdocs.cs.ualberta.ca/~santanad/papers/2017/summervilleMSOL17.pdf
- Smith e Whitehead, 2010: https://www.pcgworkshop.com/archive/smith2010analyzing.pdf
- Khalifa et al., *The PCG Benchmark*, 2025: https://arxiv.org/pdf/2503.21474 · https://github.com/amidos2006/pcg_benchmark
- PCGRL: https://arxiv.org/pdf/2001.09212 · https://github.com/amidos2006/gym-pcgrl
- Smith e Mateas, ASP per la PCG, 2011: https://course.ccs.neu.edu/cs5150f14/readings/smith_asp4pcg.pdf
- Sturgeon: https://ojs.aaai.org/index.php/AIIDE/article/view/21944 · https://www.pcgworkshop.com/archive/cooper2023sturgeon.pdf · https://github.com/crowdgames/sturgeon-pub
- WFC: https://github.com/mxgmn/WaveFunctionCollapse · wfc_2019f: https://raw.githubusercontent.com/ikarth/wfc_2019f/master/LICENSE
- *Unexplored*: https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/ · https://www.gamedeveloper.com/design/unexplored-s-secret-cyclic-dungeon-generation-
- Automi cellulari per caverne: https://www.jeremykun.com/2012/07/29/the-cellular-automaton-method-for-cave-generation/
- Dormans, 2010: https://www.pcgworkshop.com/archive/dormans2010adventures.pdf
- Licenze dei pacchetti: https://pypi.org/project/ortools/ · https://pypi.org/project/clingo/ · https://pypi.org/project/networkx/ · https://pypi.org/project/scikit-image/ · https://pypi.org/project/shapely/ · https://pypi.org/project/pathfinding/ · https://pypi.org/project/momepy/ · https://pypi.org/project/VisiLibity/ · https://pypi.org/project/pytmx/ · https://pypi.org/project/pytiled-parser/ · https://pypi.org/project/python-constraint/ · https://pypi.org/project/python-sat/
- Watabou: https://watabou.itch.io/procgen-mansion/comments?before=5 · Azgaar: https://raw.githubusercontent.com/azgaar/Fantasy-Map-Generator/master/LICENSE · mapgen4: https://raw.githubusercontent.com/redblobgames/mapgen4/master/LICENSE
- Dungeon Scrawl: https://alternativeto.net/software/dungeon-scrawl/about · https://blog.dungeonscrawl.com/uvtt-export · DungeonFog: https://alternativeto.net/software/dungeonfog/about
- UVTT in Roll20: https://help.roll20.net/hc/en-us/articles/41643201127831-Universal-Virtual-Tabletop-UVTT-Support
- LDtk: https://ldtk.io/docs/game-dev/json-overview/json-schema/ · Tiled: https://doc.mapeditor.org/en/latest/reference/json-map-format/ · https://raw.githubusercontent.com/mapeditor/tiled/master/COPYING
