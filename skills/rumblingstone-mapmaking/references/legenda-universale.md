# Legenda universale delle mappe

> Fonte di verità: la tabella `SYMBOLS` in `scripts/render_map_svg.py`.
> Questa pagina è la vista umana; se diverge, vince il codice (e questa
> pagina va aggiornata). Simboli NON in legenda: rendono come emoji "locale"
> e vanno dichiarati nel blocco griglia del master.

## Terreni (fill — regioni organiche texturizzate)

| Simbolo | Significato |
|---|---|
| 🌲 | Foresta densa (Furtività +5, copertura) |
| 🌿 | Vegetazione bassa |
| 🟩 | Pianura / area aperta |
| 🟫 | Terra battuta / sentiero |
| 🟨 | Sabbia / area segnalata |
| 🟧 | Lava raffreddata / pericolo |
| 🟥 | Zona letale |
| 🟦 | Acqua profonda |
| 🌊 | Acqua / corrente |
| ⬛ | Struttura (tenda, edificio, dais) |
| ⬜ | Pavimento lavorato |
| 🏰 | Muro / roccia solida |
| 🟪 | Pilastro / mithral |
| ⛰ | Montagne / creste rocciose |

`🏰 ⬛ 🟪 ⛰` sono "solidi": ombra portata, contorno a inchiostro marcato,
occlusione ambientale sul terreno adiacente, griglia chiara sopra.

## Unità (token con gradiente e anello)

| Simbolo | Significato |
|---|---|
| 🔵 | PG / alleati |
| 🔴 | Nemico standard |
| ⚫ | Boss / comandante |
| 🟡 | Incantatore nemico |
| 🟢 | Creatura evocata / bestia |
| 🟣 | Creatura speciale |

## Oggetti (prop vettoriali illustrati, originali in-house)

| Simbolo | Significato |
|---|---|
| 🪨 | Rocce/macerie (copertura +4 CA, terreno difficile) |
| 🔥 | Fuoco (1d6 fuoco/round) |
| 💥 | Fiamme / esplosione |
| 💀 | Fossa / trappola |
| 🕳 | Voragine / buco |
| 🌳 | Treant / creatura vegetale |
| ⭐ | Obiettivo primario |
| 🚪 | Porta / ingresso |
| 🗼 | Torre / struttura alta |
| 🏺 | Contenitore / bottino |
| 🔔 | Allarme / trappola sonora |
| 💎 | Tesoro / oggetto magico |
| 👑 | Trono / Corona |
| 🏮 | Braciere / fonte di luce |
| 🪓 | Rastrelliera / armi |
| 🛏 | Giaciglio |
| 📦 | Casse / rifornimenti |
| 🐴 | Cavalcature |
| 🕸 | Ragnatele (terreno difficile) |
| ❄ | Ghiaccio |
| ⚡ | Energia / pericolo magico |
| 🌀 | Portale / vortice |
| ⬇ | Discesa / pendenza |
| 🏛 | Edificio / tempio |
| 🌋 | Bocca vulcanica / fumarola |
| 🗿 | Statua |
| 🌉 | Ponte / passerella |
| 🎯 | Obiettivo tattico |
| 🖼 | Affresco / quadro |
| ✨ | Effetto magico attivo |
| ⚔ | Zona di scontro |
| ⚰ | Sarcofago / bara |
| 🛢 | Barile |
| 🪜 | Scale / rampa |
| 🦴 | Ossa / resti |
| 🍄 | Funghi giganti |
| 🕯 | Candele / rituale |
| 🌾 | Erba alta / cespugli (occultamento) |
| ⛺ | Tenda |
| 🔮 | Cristalli / altare magico |
| 🪑 | Tavolo e sedie |
| 🧱 | Muretto / copertura bassa (+4 CA) |

Gli oggetti ereditano il terreno della cella più vicina nella riga (prima a
sinistra, poi a destra); 🌳 e 🪨 hanno 2 varianti di forma alternate in modo
deterministico per rompere la ripetizione.
