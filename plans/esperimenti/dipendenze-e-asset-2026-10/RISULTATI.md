# Le cinque librerie scartate, rimisurate; gli asset della community per categoria

Seconda misura del 2026-10-08, sera, su richiesta del DM dopo la #227: *«dimmi
perché hai messo fuori resvg-py, hypothesis, networkx, scipy, shapely; misura
cosa apportano e quanto costano»*, e poi *«progetti della community che
aiutano a creare asset e mappe per ogni categoria, uniformando mappe, asset e
resa grafica»*. Segue
[`orientamento-e-dipendenze-2026-10/`](../orientamento-e-dipendenze-2026-10/RISULTATI.md),
che aveva misurato ogni libreria su un solo compito; qui ognuna è misurata sul
compito per cui la si adotterebbe.

| File | Cosa riproduce |
|---|---|
| `bench_grafi.py` | §1, networkx e scipy sui compiti di V7, M1 e M2 |
| `bench_uvtt.py` | §2, shapely sui muri dell'export UVTT |
| `bench_mutanti.py` | §3, hypothesis contro un generatore a seme fisso, su sei mutanti del grafo |

Le librerie si installano in un ambiente a parte (`python3 -m venv`, poi
`pip install networkx scipy shapely hypothesis resvg-py`); gli script non
toccano il repo.

## §1 · networkx e scipy, sul lavoro che farebbero

Corpus: 44 mappe, 45.749 celle percorribili, 168.806 archi con la regola
dell'angolo dell'SRD. Tempi: il migliore di cinque giri.

| Compito | In casa | Con la libreria | Accordo | Peso |
|---|---|---|---|---|
| V7 · strozzature (punti d'articolazione) e anelli μ | Tarjan iterativo, 35 righe: **209 ms** | networkx: **461 ms** | identico su 44 mappe su 44, 370 strozzature | 2,1 MB, 39 dipendenze opzionali |
| M1 + M2 su 38 mappe | il calcolo a mano di prima: **105 ms** | `scipy.ndimage`: **20 ms** | differenza massima 0,000000 | 34 MB |

networkx è **più lenta** del codice in casa: costruire il grafo costa più che
visitarlo. scipy è cinque volte più veloce, e il guadagno assoluto è di 85 ms su
un collaudo che ne dura 2.500.

## §2 · shapely sui muri dell'export UVTT

| | Oggetti `line_of_sight` | Muri che un VTT crea (segmenti) |
|---|---:|---:|
| oggi (`extract_walls` fonde già i lati collineari) | 1.674 | 1.674 |
| `shapely.ops.linemerge` | 175 polilinee | **1.674** |

Le polilinee sono meno oggetti nel file, ma Foundry e Roll20 fanno un muro per
ogni coppia di punti: al tavolo non cambia niente.

## §3 · hypothesis, su mutanti del grafo del collaudo

Tre proprietà (zone invarianti per rotazione, regola dell'angolo, una porta è
un varco), 1.500 griglie per proprietà con ciascun generatore.

| Mutante | Seme fisso, stdlib | hypothesis |
|---|---|---|
| diagonale sempre ammessa | preso | preso |
| angolo: `and` invece di `or` | preso | preso |
| la porta blocca | preso | preso |
| la fossa ferma la diagonale | mancato | mancato |
| un vicino perso | preso | preso |
| componenti senza la coda | preso | preso |
| **totale** | **5 su 6** | **5 su 6** |

hypothesis aggiunge il controesempio ridotto al minimo, che fa risparmiare
qualche minuto di lettura quando un test diventa rosso. Il mutante che tutti e
due mancano chiede un caso scritto dall'SRD (una fossa non ferma la diagonale),
non più esempi a caso.

## §4 · resvg-py a zoom 1

| | Chromium headless (oggi) | resvg-py 0.5.0 |
|---|---:|---:|
| 3 mappe a zoom 1 | **5,6 s** | 30,3 s |
| 8 mappe a zoom 2 | 42 s | circa 37 s a mappa, interrotto |
| determinismo | 8 PNG su 8 identici al byte | — |
| pixel che differiscono oltre 24/255 da Chromium | — | 5,0 %, 5,3 %, 8,7 % |

I filtri della pergamena (`feTurbulence`, `feDisplacementMap`) girano su un
solo filo; il testo cade su un altro font. resvg servirebbe dove manca un
browser, ed è il caso che `export_map_png.py` copre già con Inkscape.

## §5 · Dove la resa non è uniforme, oggi

| Difetto | Misura | Comando |
|---|---|---|
| celle disegnate con l'emoji del font di sistema | **177 celle in 7 SVG su 47**: ☁ 71, 💠 49, 🔷 25, 🔲 15, 🌱 4, 🔺 4, 🛡 2, 🥋 2, 💚 2, 📜 2, ✝ 1 | `grep 'font-size="17"'` sugli SVG di `rendered/` |
| il testo delle mappe | chiede Georgia, che su Linux e in CI diventa **DejaVu Serif**; i volumi usano EB Garamond e Cinzel, già nel repo (`scripts/fonts/`, OFL) | `fc-match Georgia` |
| la categoria delle mappe | **0 su 44** dichiarano `@tipo` (lotto V2) | `collaudo_mappe --json` |
| i simboli universali | 84 su 84 disegnati in casa (59 oggetti, 19 trame, 6 pedine): nessuno dipende dal font | `legend.json` |

I sottoinsiemi di EB Garamond e Cinzel con i 97 caratteri usati nelle mappe
pesano **24 KB e 15 KB** in woff2 (`pyftsubset` di fonttools, MIT, 4.66.1 del
2026-09-29). Incorporati in base64, circa 52 KB a SVG: 2,4 MB in più sui 3,7 di
oggi.

Le emoji locali più usate sono concetti che la legenda universale non ha o ha
diversi: il **cristallo come ostacolo** (💠 e 🔷, 74 celle; `🔮` è «cristalli /
altare magico»), la **stalagmite** (🔺), la **zona aerea** (☁, che è `🌫` della
legenda), le **colonne** (🔲, che è `🟪`), le pedine dei PG con un nome (🛡,
🥋).

## §6 · Asset e generatori della community, licenza letta alla fonte

| Progetto | Che cosa dà | Licenza (fonte) | Vista | Contamina? | Verdetto per il repo |
|---|---|---|---|---|---|
| **game-icons.net** (`game-icons/icons`, 4.239 SVG, aprile 2026) | icone vettoriali monocrome, 35 autori | **CC BY 3.0**, alcune CC0 (`license.txt`) | frontale o di profilo (porta, scale, baule visti di lato) | no, ma chiede il credito per autore | **già nel repo** per gli stemmi del Palio; non per le celle tattiche |
| **Noto Emoji** (`googlefonts/noto-emoji`) | ogni emoji in SVG | immagini **Apache-2.0**, font OFL 1.1 (`README.md`) | come l'emoji | no (NOTICE) | ripiego incorporato per le emoji locali: la stessa resa su ogni macchina |
| Twemoji (`jdecked/twemoji`) | ogni emoji in SVG | **CC BY 4.0** (`LICENSE-GRAPHICS`) | come l'emoji | no, credito | alternativa a Noto |
| OpenMoji | ogni emoji in SVG | **CC BY-SA 4.0** (`LICENSE.txt`) | | **sì** | escluso |
| Kenney (kenney.nl) | migliaia di asset | **CC0** | per lo più pixel art 16×16 e isometrico | no | stile lontano dalla pergamena; utile solo per idee |
| 2-Minute Tabletop | asset dipinti zenitali, di qualità alta | **CC BY-NC 4.0** (`faq/license-and-attribution`) | zenitale | no SA; NC compatibile con ADR-0005 | l'unica libreria zenitale dipinta usabile; raster, uno stile diverso dalla pergamena |
| Forgotten Adventures | asset zenitali | uso personale, **niente redistribuzione** (`/info/`) | zenitale | — | escluso: il repo li ridistribuirebbe |
| Watabou (MFCG, Village, Dwellings, One Page Dungeon) | città, villaggi, interni di edifici, dungeon | le mappe generate *«as you like: copy, modify, include in your commercial rpg adventures»* (pagina itch di MFCG); il codice vecchio `TownGeneratorOS` è GPL-3.0 | zenitale | no per le uscite | già usato per i dungeon (`import_watabou.py`); città, villaggi ed edifici non hanno un importatore |
| Azgaar Fantasy Map Generator | mappe regionali e di mondo | codice **MIT** | regionale | no | per regioni inventate; la geografia di Faerûn è canone e non si genera |
| mapgen4 (Red Blob Games) | terreni procedurali | **Apache-2.0** | regionale | no | idem |
| Tiled | editor di mappe a tessere | GPL-2.0 l'editor, formati liberi | | no (non si include) | non serve: il master è la griglia emoji |

**Cosa contamina cosa.** Un'icona CC BY dentro uno SVG generato porta l'obbligo
del credito in ogni SVG, PNG e PDF che la contiene: si risolve con una riga
nella legenda o nel colophon. Un asset CC BY-SA o GPL renderebbe lo SVG
un'opera con la stessa licenza, e le mappe derivate da *Red Hand of Doom* non
si possono rilicenziare (ADR-0005): esclusi. NC vieta l'uso commerciale, che
ADR-0005 esclude già.

**La regola 5 di `rumblingstone-mapmaking`** («tutta l'arte è procedurale o
fatta in casa, nessun file di terzi») vale **per le mappe**. Nel repo un asset di
terzi c'è già: le figure degli stemmi del Palio sono icone di game-icons.net,
con il loro `CREDITS.md` e le licenze accanto
(`09_…/P2D-Palio-Allegati/stemmi/`). È il modello per ogni asset che entra in
una mappa: licenza nella cartella, credito per autore, modifiche dichiarate.

🔁 **Cosa c'era già, e non era stato fatto.** RICERCA-GENERATORI-MAPPE
(luglio) aveva previsto Azgaar per le regionali e la città di Watabou come
«Fase 3», documentata in `scripts/README-automation.md` e mai eseguita: nessun
file `.map` e nessun export di città nel repo. Aveva anche valutato 2-Minute
Tabletop e scelto di non adottarlo, perché la pergamena procedurale bastava.
Il DM, il 2026-10-08, riapre tutte e tre.

## §7 · Le texture CC0, 2026-10-09

Il DM ha chiesto una strada per mappe più ricche senza problemi di licenza.

- **Licenze, lette alla fonte**: Poly Haven e ambientCG CC0 1.0; le tessere di
  Dungeon Crawl Stone Soup «use freely, no attribution»; 2-Minute Tabletop
  CC BY-NC per i contenuti base, nessuna licenza per i premium.
- **Gli 11 id scelti esistono** nel catalogo di Poly Haven letto il 2026-10-09
  (867 texture, `api.polyhaven.com/assets?t=textures`, via Firecrawl):
  `stone_tiles_02`, `rock_wall_10`, `castle_brick_07`, `dirt_floor`,
  `roof_slates_02`, `leafy_grass`, `forest_ground_04`, `sand_01`,
  `rock_face_03`, `rocks_ground_02`, `monastery_stone_floor`. Il formato degli
  URL e l'MD5 della diffusa 1k vengono da `api.polyhaven.com/files/<id>`.
- **Peso**, con ritagli delle illustrazioni del repo al posto delle texture:
  webp 256 px a qualità 60, mediana 14,8 KB in base64 (128 px: 4,0 KB;
  512 px: 75,9 KB). Le 50 mappe usano 3 terreni in mediana, 6 al massimo:
  circa +2,3 MB se il tema si committa per tutte. Due SVG di prova: 117 e
  127 KB.
- **Rete**: da questo ambiente Poly Haven, ambientCG, OpenGameArt, Kenney,
  Dropbox e Watabou sono bloccati dal proxy; npm e PyPI no, ma i pacchetti
  npm con texture sono ripubblicazioni di terzi, scartate per la provenienza.

## Cosa questa misura non dice

- Se la pergamena con il font dei volumi **si legge meglio** di Georgia: lo
  dice il DM guardando.
- Quanto pesa al tavolo una mappa in stile dipinto rispetto alla pergamena.
- Le uscite di MFCG, Village e Dwellings non sono state scaricate: servono
  esportazioni vere per scrivere un importatore e misurarlo.
