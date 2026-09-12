# Legenda universale delle mappe

> **Fonte di verità**: `scripts/legend.yaml` (ADR-0048). Le tabelle qui sotto
> sono **generate** da lì con `python3 scripts/build_legenda_skill.py`, e la CI
> le confronta: se divergono, la build fallisce. Non si correggono a mano.
> Simboli NON in legenda: rendono come emoji "locale" e vanno dichiarati nel
> blocco griglia del master.

<!-- legenda:auto-begin -->

## Terreni (fill — regioni organiche texturizzate)

| Simbolo | Significato | Muro |
|---|---|---|
| 🌲 | Foresta densa (Furtività +5, copertura) | — |
| 🌿 | Vegetazione bassa | — |
| 🟩 | Pianura / area aperta | — |
| 🟫 | Terra battuta / sentiero | — |
| 🟨 | Sabbia / area segnalata | — |
| 🟧 | Lava raffreddata / pericolo | — |
| 🟥 | Zona letale | — |
| 🟦 | Acqua profonda | — |
| 🌊 | Acqua / corrente | — |
| ⬛ | Edificio / corpo di fabbrica (muratura piena: blocca vista e movimento) | **sì** |
| 🔳 | Dais / pedana rialzata (ci si sale sopra: NON e' un muro) | — |
| ⬜ | Pavimento lavorato | — |
| 🏰 | Muro / roccia solida | **sì** |
| 🟪 | Pilastro / mithral | **sì** |
| ⛰ | Montagne / creste rocciose | **sì** |

## Unità (token con gradiente e anello)

| Simbolo | Significato | Muro |
|---|---|---|
| 🔵 | PG / alleati | — |
| 🔴 | Nemico standard | — |
| ⚫ | Boss / comandante | — |
| 🟡 | Incantatore nemico | — |
| 🟢 | Creatura evocata / bestia | — |
| 🟣 | Creatura speciale | — |

## Oggetti (prop vettoriali illustrati, originali in-house)

| Simbolo | Significato | Muro |
|---|---|---|
| 🪨 | Rocce/macerie (copertura +4 CA, terreno difficile) | — |
| 🔥 | Fuoco (1d6 fuoco/round) | — |
| 💥 | Fiamme / esplosione | — |
| 💀 | Fossa / trappola | — |
| 🕳 | Voragine / buco | — |
| 🌳 | Treant / creatura vegetale | — |
| ⭐ | Obiettivo primario | — |
| 🚪 | Porta / ingresso | — |
| 🗼 | Torre / struttura alta | **sì** |
| 🏺 | Contenitore / bottino | — |
| 🔔 | Allarme / trappola sonora | — |
| 💎 | Tesoro / oggetto magico | — |
| 👑 | Trono / Corona | — |
| 🏮 | Braciere / fonte di luce | — |
| 🪓 | Rastrelliera / armi | — |
| 🛏 | Giaciglio | — |
| 📦 | Casse / rifornimenti | **sì** |
| 🐴 | Cavalcature | — |
| 🕸 | Ragnatele (terreno difficile) | — |
| ❄ | Ghiaccio | — |
| ⚡ | Energia / pericolo magico | — |
| 🌀 | Portale / vortice | — |
| ⬇ | Discesa / pendenza | — |
| 🏛 | Edificio / tempio | **sì** |
| 🌋 | Bocca vulcanica / fumarola | — |
| 🗿 | Statua | **sì** |
| 🌉 | Ponte / passerella | — |
| 🎯 | Obiettivo tattico | — |
| 🖼 | Affresco / quadro | — |
| ✨ | Effetto magico attivo | — |
| ⚔ | Zona di scontro | — |
| ⚰ | Sarcofago / bara | — |
| 🛢 | Barile | — |
| 🪜 | Scale / rampa | — |
| 🦴 | Ossa / resti | — |
| 🍄 | Funghi giganti | — |
| 🕯 | Candele / rituale | — |
| 🌾 | Erba alta / cespugli (occultamento) | — |
| ⛺ | Tenda (telo teso: blocca la vista, si abbatte) | **sì** |
| 🔮 | Cristalli / altare magico | — |
| 🪑 | Tavolo e sedie | — |
| 🧱 | Muretto / copertura bassa (+4 CA) | — |

`⬛ 🏰 🟪 ⛰` sono "solidi": ombra portata, contorno a inchiostro marcato,
occlusione ambientale sul terreno adiacente, griglia chiara sopra.

<!-- legenda:auto-end -->

> ⚠️ **ADR-0042 — i tre glifi che stavano sotto ⬛.** Fino al 2026-09-04 `⬛`
> valeva insieme *«tenda, edificio, dais»*, e l'export UVTT li trattava tutti da
> muro pieno. Sono tre cose diverse: un edificio è un muro, una **tenda** è un
> telo che blocca la vista ma si abbatte, un **dais** non è un muro affatto —
> ci si sale sopra. Adesso hanno un glifo ciascuno: **⬛ edificio · ⛺ tenda ·
> 🔳 dais**. Se stai disegnando una mappa nuova, usa quello giusto: `⬛` non è
> più il jolly.

Gli oggetti ereditano il terreno della cella più vicina nella riga (prima a
sinistra, poi a destra); 🌳 e 🪨 hanno 2 varianti di forma alternate in modo
deterministico per rompere la ripetizione.
