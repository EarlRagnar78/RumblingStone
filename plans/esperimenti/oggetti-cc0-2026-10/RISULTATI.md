# Gli oggetti di scena dai modelli 3D CC0 — audit e prova della catena (2026-10-09)

Esperimento di R4-ter di
[PIANO-RESA-E-ASSET-DELLE-MAPPE](../../PIANO-RESA-E-ASSET-DELLE-MAPPE.md), decisioni
D17 e D18, poi D19-D22. Sola lettura sul corpus; i numeri si rifanno con:

```bash
python3 plans/esperimenti/oggetti-cc0-2026-10/misura_simboli.py          # tabella
python3 plans/esperimenti/oggetti-cc0-2026-10/misura_simboli.py --json   # → misura-simboli.json
```

## 1 · Quali simboli-oggetto usa il corpus

Contati sulle griglie dei 31 master che hanno un gemello in `rendered-texture/`
(53 mappe). Un simbolo-oggetto è un simbolo della legenda con un glifo (`prop`):
sono 61, e il corpus ne usa **46**, come misurato il 2026-10-09 per D17.

| Destino | Simboli | Usati | Celle | Quota delle celle-oggetto |
|---|---:|---:|---:|---:|
| modello Poly Haven | 15 | 10 | 800 | 24% |
| modello Quaternius, se la Standard lo ha | 13 | 9 | 138 | 4% |
| resta glifo | 33 | 27 | 2.448 | 72% |
| **totale** | **61** | **46** | **3.386** | |

Il 72% resta glifo per scelta, e quella quota la fanno quattro simboli: 🔥 655
celle, ⬇ 603, 💥 423, 🚪 261. Fuoco ed effetti non sono oggetti, ⬇ è un segno di
pendenza, le porte ruotano con il muro (ADR-0083). **Il tema texture cambierà
faccia sugli oggetti, non sulla maggior parte dei simboli**: va detto prima che
il DM si aspetti mappe trasformate.

I simboli che restano glifi, con la ragione (D21, il DM il 2026-10-09):

| Gruppo | Simboli | Perché |
|---|---|---|
| fuoco ed effetti | 🔥 💥 ⚡ ✨ ⭐ 🌀 ❄ 🕸 🌋 | non sono oggetti (D17) |
| chiusure | 🚪 🔒 ❔ 🥅 🪟 ⛓ | ruotano con l'asse del muro, ADR-0083 (D17) |
| segnali | 🎯 ⚔ 💀 🔔 💎 | obiettivo, zona, trappola, allarme, tesoro: dicono una regola, non un mobile |
| creature | 🌳 🐴 | 🌳 nella legenda è «Treant / creatura vegetale», non un albero |
| scala di mappa | 🗼 🏛 🌉 | un edificio intero in una cella da 1,5 m |
| scale e buchi | ⬇ 🪜 🔼 🔽 🔻 🕳 | frecce e aperture: un modello dall'alto non dice sale o scende |
| altro | 🖼 🏗 | l'affresco sta sul muro; la gru non ha un modello medievale |

Il muretto 🧱 (94 celle in 7 mappe) stava nel gruppo «altro» della proposta; il
DM l'ha voluto modello (D21). È orientabile: due tessere, est-ovest e nord-sud.

## 2 · Poly Haven

**Licenza letta alla fonte** (`polyhaven.com/license`, 2026-10-09): tutti gli
asset, «HDRIs, textures and 3D models», sono CC0; uso anche commerciale,
nessun credito obbligatorio, ridistribuzione permessa. I termini del sito
vietano lo scraping senza permesso e rimandano a termini separati per l'API
pubblica: lo script interroga l'API una volta per modello, come
`build_texture_cc0.py`, e non raschia pagine.

**Catalogo**: 521 modelli (`api.polyhaven.com/assets?t=models`, letto via
Firecrawl). Ogni modello ha un glTF 1k con `.bin` e texture; l'API dà URL e MD5
di ogni file (`api.polyhaven.com/files/<id>`, chiave `gltf.1k.gltf`).

| Simbolo | Modello | Misura vera | Perché questo |
|---|---|---|---|
| 🪨 | `boulder_01` | 127×183×100 cm | masso con licheni, dall'alto si legge roccia |
| 🪨 variante | `namaqualand_boulders_01` | 106×59×25 cm | gruppo di pietre basse, la seconda variante come `pr_rocks_b` |
| 🗿 | `gothic_statue` | 148×156×174 cm | figura velata con corona e spada: l'unica statua non moderna né animale |
| 🏮 | `stone_fire_pit` | 145×143×39 cm | focolare di pietre; la fiamma resta glifo sopra (D22) |
| 🛏 | `GothicBed_01` | 149×204×153 cm | letto a baldacchino in legno, «medieval-inspired» |
| 🏺 | `ceramic_pot` | 66×50×37 cm | orcio con anse e smalto consumato |
| 🪑 | `WoodenTable_01` | 180×66×55 cm | tavolo di legno; le sedie non ci sono |
| 🛢 | `wine_barrel_01` | 74×76×87 cm | botte di rovere con cerchi di ferro |
| 📦 | `wooden_crate_02` | 117×53×46 cm | cassa di assi |
| 🪵 | `dead_tree_trunk_02` | 405×106×106 cm | tronco caduto: le travi crollate non ci sono |
| 🧰 | `treasure_chest` | 96×52×62 cm | forziere con bande di ferro |
| 📚 | `wooden_bookshelf_worn` | 137×58×206 cm | libreria di legno; dall'alto se ne vede il cielo, da guardare |
| 🗄 | `GothicCabinet_01` | 172×113×236 cm | armadio gotico intagliato |
| 🕯 | `brass_candleholders` | 105×36×84 cm | candelabri di ottone con candele |
| 🌾 | `fern_02` | 197×172×43 cm | quattro cespi di felce |
| 🧱 | `namaqualand_rocks_01` | 145×22×15 cm | fila di pietre: il muretto a secco più vicino; Poly Haven non ha muretti |

Scartati, perché il catalogo è soprattutto moderno: `Barrel_01` (le sue varianti
sono «explosive», «radiation», «oxide»), `Barrel_02` (plastica blu), `barrel_03`
(acciaio verniciato), `old_bed_frame` (ferro e rete metallica),
`outdoor_table_chair_set_01` (sedie pieghevoli da caffè), `worn_metal_rack`
(scaffale industriale), `antique_ceramic_vase_01` (decoro blu da porcellana
inglese), `modular_fort_01` (71 m: un forte intero, non un muretto).

**MD5 fissati** (glTF 1k, letti dall'API il 2026-10-09; per gli altri modelli
l'MD5 si legge dall'API allo scaricamento e finisce nell'indice):

| Modello | glTF | `.bin` | diffusa 1k |
|---|---|---|---|
| `boulder_01` | `26e2eef4a1f68c9557c65cd375b21d6c` | `27a19fa031d8b4c3a09261f19c444dc5` | `25f8a843f13369d56d37f49db05ea8c3` |
| `namaqualand_boulders_01` | `904c7349856f65f757b7f6fd36f57641` | `58ed8a29120ad0807320ce49a9d14c2a` | `1ed791727bbb6f26f77246e5de17d901` |
| `gothic_statue` | `4fb49ae8f4278a0f5f1c7ca89a416f69` | `64ff6a07591c56042e01c780dce7685b` | `a8110eba7602d4d3ff00b05abf25397e` |
| `stone_fire_pit` | `f3a23e45ee66802ccc7a5462a9371ae3` | `1652ba5fb374b6c15cddb64445a0bb5b` | `a7ec1828062280c20e265d2c99497d1d` |

Peso dei quattro, glTF 1k con `.bin`, diffusa, normale e ARM: 2,5-5,7 MB l'uno.
Per i 16 modelli la stima è 50-70 MB: è il numero che ha deciso D19.

## 3 · Quaternius, Fantasy Props MegaKit

**Licenza letta alla fonte** il 2026-10-09:

- `quaternius.com/packs/fantasypropsmegakit.html`: campo «License: CC0» per il
  pacchetto; versione Standard «Free to use in personal, educational and
  commercial projects»; versione Pro «An extra 30-40% of a pack […] All still
  free to use in personal, educational and commercial projects». **La pagina
  non dice «CC0» della Pro**: dice «free to use».
- `quaternius.itch.io/fantasy-props-megakit`: «Asset license: Creative Commons
  Zero v1.0 Universal» per la pagina, che vende tre file: Standard (143 MB,
  prezzo libero), Pro (249 MB, 9,99 $), Source (545 MB, 14,99 $).
- `store.godotengine.org`: «This is the STANDARD free version with a portion of
  the models».

**Esito**: per la Standard la CC0 è chiara su tutte e tre le pagine. Per la Pro
è molto probabile, perché la pagina itch dichiara CC0 per tutto ciò che vende,
ma non è scritta per la Pro. Come chiedeva D17, **si usa solo la Standard**;
lo script ne fissa l'impronta e pretende nello zip un file di licenza che dica
CC0. Quali dei 13 simboli cercati ci siano davvero (⛺ ⚒ 🛐 👑 ⚰ 🦴 🍄 ⛲ 🧪 🪓 🔮
🔷 🔺) non si sa finché il DM non scarica lo zip: le immagini della pagina
mostrano letti, barili, tavoli, casse, bancarelle, armi; tende, cristalli e
stalagmiti probabilmente non ci sono. La tabella si scrive sui nomi veri
(`build_oggetti_cc0.py --elenca-quaternius`), non su nomi indovinati.

## 4 · La coerenza fra fotografico e low-poly

Da misurare sulle tessere vere, con `build_oggetti_cc0.py --misura-stile`: per
ogni tessera luminanza media, contrasto (deviazione della luminanza),
saturazione e dettaglio (gradiente medio fra pixel vicini), sui soli pixel
opachi, con la media per fonte. Il dettaglio è la grandezza che separa i due
stili: una texture fotografica ha gradiente alto ovunque, un low-poly a tinte
piatte è quasi zero dentro le facce.

**Non misurata qui**: la rete di questo ambiente blocca Poly Haven e Quaternius,
e nessun modello vero è arrivato. Il confronto si fa sul giro di prova del DM,
e i numeri vanno in questa sezione prima di estendere a tutte le mappe (D17).

## 5 · La prova della catena

Blender 5.2.2 LTS è installabile da PyPI come modulo (`pip install bpy`, ruota
da 400 MB, solo Python 3.13): in questo ambiente PyPI è raggiungibile, Poly
Haven no. La catena è stata provata con **modelli procedurali** (un cilindro, un
parallelepipedo, un icosaedro deformato, una fila stretta) al posto dei glTF di
Poly Haven, con la stessa struttura di cache e di `fonte.json`:

| Passo | Esito |
|---|---|
| render di 9 tessere (8 del giro di prova, più il muretto nord-sud), Cycles su CPU, 64 campioni, 192 px | 18 s in tutto |
| tessere webp da 96 px con trasparenza | 2,0-2,8 KB l'una (forme piatte: le vere peseranno di più) |
| M7-D nel tema texture | letti, braciere, tavolo, rocce e muretto diventano tessere; porte, fuoco e 🔮 restano glifi |
| il muretto | tratto nord-sud dove i vicini 🧱 stanno sopra e sotto, est-ovest altrimenti |
| il braciere | la fiammella del glifo 🔥 resta sopra il focolare, ridotta |
| validate_maps senza tessere | verde: i 53 SVG del tema non cambiano finché le tessere non ci sono |

Due difetti trovati e corretti nella prova, prima del commit:

- con sole a 60° e impronta all'82% l'ombra di un oggetto alto usciva dalla
  cella e veniva tagliata; con 65° e 76% resta dentro;
- con fondo a 0,35 l'ombra era quasi nera, più scura di ogni ombra della
  pergamena; con fondo a 0,9 e sole a 2,2 si legge come le altre.

Il PNG della prova non va al DM come confronto: sono forme di prova, e
giudicare la resa su quelle porterebbe a una decisione sbagliata. Il confronto
vero lo fa il DM con i modelli veri, `GUIDA-MAPPE.md` §5.1.1.

## 6 · Il peso

Non misurabile senza le tessere vere. Il calcolo per il dopo: ogni SVG
incorpora una volta sola ogni tessera che usa, in base64 (+33%). Con tessere da
3-8 KB e 1-8 tessere per mappa, l'aumento sta fra 4 e 85 KB a SVG, cioè fra 0,2
e 4,5 MB sui 53 SVG del tema, oggi 7,6 MB. È una forbice, non una stima: nella
#227 la stima del peso era sbagliata per difetto (2,3 MB stimati, 7,6 misurati),
e il numero vero si scrive solo dopo `dm.py maps texture` con le tessere vere.
