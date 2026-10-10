# PIANO — La resa e gli asset delle mappe, uguali su ogni macchina e per ogni categoria

> **Stato**: 🟡 in corso (2026-10-08), D1-D8 decise dal DM il 2026-10-08, D9-D22 il 2026-10-09: le texture CC0 strada principale (R4-bis fatto, velatura 0,30), gli oggetti dai modelli 3D CC0 (R4-ter: codice fatto, tessere vere dal DM), R4 una prova su una mappa (installatore fatto, aspetta il pacchetto), R5 parte da Dauth (sei mappe dell'assedio fatte), R6 in attesa · **Classe**: C per R1-R3, G poi C per R4-R6
> **Nasce da**: la richiesta del DM della sera del 2026-10-08, dopo la #227:
> *«verifica se ci sono progetti best community valuated che possono essere
> importati andando in deroga alla std lib e che migliorano o aiutano a creare
> asset e mappe per ogni categoria necessaria, in modo da avere gli asset per
> ogni necessità e le mappe migliori possibili, categorizzando bene,
> uniformando tutte le mappe, gli asset e la resa grafica delle mappe»*.
> **Decisione**: [ADR-0085](adr/ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md) (accettata). Le dipendenze: [ADR-0084](adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md) e il suo emendamento.
> **Misura riproducibile**: [`esperimenti/dipendenze-e-asset-2026-10/`](esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md).

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

Regola di apertura (ADR-0044): letti `plans/INDEX.md` e i piani e le ricerche
che parlano di mappe; `fase1.py` sui file toccati, nessun archivio fra i
bersagli (gli SVG di `_ARCHIVIO` si rigenerano come derivati, sul precedente
di ADR-0070).

| Documento | Cosa copre | Rapporto con questo piano |
|---|---|---|
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | il censimento di luglio: Watabou, Azgaar, mipui, 2-Minute Tabletop | la sua **Fase 3** (Azgaar per le regionali, la città di Watabou) è documentata e mai eseguita: la eseguono R5 e R6. Aveva scartato 2-Minute Tabletop; il DM lo riapre (R4) |
| [RICERCA-TOOL-ESTERNI-DM](RICERCA-TOOL-ESTERNI-DM-2026-08.md) | le tre soglie per far entrare un tool | ogni lotto qui le passa per scritto |
| [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | il collaudo come grafo, il generatore di bozze | **non rifà niente** di quello: la categoria `@tipo` (D18) e scipy (D17) sono suoi |
| [EDITOR-VISUALE-MAPPE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) | un editor a griglia | non si tocca |
| [LEVEL-DESIGN](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) | il disegno delle mappe e l'inquadratura | non si tocca: qui si parla di resa, non di disegno |
| `rumblingstone-art-direction` | le immagini, la hero map | il tema dipinto (R4) è per le mappe a griglia, non per la hero map |

## §2 · La misura, in breve

Tutto in [RISULTATI](esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md);
qui i numeri che hanno deciso i lotti.

| Difetto | Prima | Dopo R1-R3 |
|---|---:|---:|
| celle disegnate con l'emoji del font di sistema | 177 in 7 SVG | **0** |
| font del testo | Georgia → DejaVu Serif in CI | EB Garamond e Cinzel incorporati |
| titoli fuori dal foglio | sì, sulle mappe strette | **0** (1 compresso con `textLength`) |
| mappe con la categoria dichiarata | 0 su 44 | **44 su 44** (D18) |
| peso dei 47 SVG | 3,77 MB | 5,85 MB |

## §3 · I lotti

### R0 · Audit ✅

Le cinque librerie scartate in V2-quater, rimisurate sul loro compito vero;
dove la resa non è uniforme; gli asset e i generatori della community con la
licenza letta alla fonte.

### R1 · I font dei volumi dentro le mappe ✅

`[engine: Opus, sessione principale · effort: alto · qualità: 0 testi al font di sistema nei 47 SVG; titoli dentro il foglio; validate_maps verde]` · **C**

`scripts/build_font_mappe.py` (fonttools, solo sviluppo) → `scripts/fonts/mappe/`;
il renderer incorpora i due woff2 e stringe i titoli con le larghezze di
`copertura.json`.

### R2 · Due universali nuovi ✅

`[engine: Opus · effort: medio · qualità: glifo diverso dai vicini (🔮, 🪨), verificato sul PNG]` · **C**

`🔺` stalagmite e `🔷` cristallo gigante in `legend.yaml`, glifi in casa.

### R3 · Il ripiego Noto per le emoji locali ✅

`[engine: Opus · effort: medio · qualità: build_emoji_noto --check verde; nessun id ripetuto in un SVG]` · **C**

`scripts/build_emoji_noto.py` → `scripts/emoji-noto/` (Apache-2.0, `CREDITS.md`).

### R4 · Il tema dipinto per le mappe dei giocatori

`[engine: Opus per le scelte, Sonnet per il codice · effort: alto · qualità: una mappa nel tema dipinto che il DM approva accanto alla pergamena; i crediti CC BY-NC nel colophon e nella mappa]` · **G → C**

- Una seconda resa dello stesso master con gli asset zenitali di
  2-Minute Tabletop (CC BY-NC 4.0), per la vista dei giocatori e i VTT. La
  pergamena resta la vista del DM; il master resta la griglia.
- Prima del codice: quali pacchetti, e se gli asset entrano nel repo o restano
  sulla macchina del DM (D6). Un pacchetto pesa decine di MB di PNG.
- Ogni asset per simbolo della legenda: una tabella `simbolo → file`, con la
  stessa regola di posa e lo stesso asse delle chiusure (ADR-0083).
- **Fatto il 2026-10-09** (D9): `scripts/asset_2mtt.py` e `dm.py asset
  installa|stato|controlla`. Il DM scarica lo zip, perché il sito manda i link
  per email anche a 0 $; l'installatore estrae in `asset-esterni/`, ignorata da
  git, e registra la categoria. La licenza (letta il 2026-10-09) divide i
  pacchetti in `base`, a offerta libera e CC BY-NC, e `premium`, senza
  licenza: `controlla` boccia la tabella che usa un premium. Guida:
  `docs/guides/GUIDA-MAPPE.md` §5.2. Resta la tabella sui nomi veri dei file,
  e la mappa di prova.

### R4-bis · Il tema texture CC0 (la strada principale)

`[engine: Opus · effort: medio · qualità: 11 texture CC0 con MD5 verificato; il tema texture di ogni mappa in rendered-texture/, allineato in validate_maps; colori leggibili come in pergamena]` · **C**

- Decise D13-D15 il 2026-10-09: texture CC0 di Poly Haven nei terreni,
  committate accanto alla pergamena, glifi in casa per gli oggetti.
- **Fatto il 2026-10-09**: `build_texture_cc0.py` (scarica, verifica l'MD5
  contro l'API, riduce a tessere webp da 256 px), il tema `texture` in
  `render_map_svg.py` (`--tema`, `--tutti-i-master`), `validate_maps` che
  pretende il gemello texture quando le texture ci sono, `dm.py asset texture`
  e `dm.py maps texture`, `doctor`, guida §5.1, test con texture finte.
- **Fatto il 2026-10-09, dal DM**: le 11 texture scaricate e verificate
  (90 KB di tessere) e i 53 SVG del tema, committati; la velatura tarata a 0,30
  (D16) guardando M7-D e il canyon di Hammerfist L1. Peso misurato: 7,6 MB
  per i 53 SVG del tema, contro i 6,2 MB della pergamena.
- **Dopo** (D15): gli oggetti di scena generati con l'IA locale.

### R4-ter · Gli oggetti di scena del tema texture (in una PR nuova, D18)

`[engine: Opus · effort: medio · qualità: ogni tessera da un modello CC0 con la sua impronta; stessa luce e scala; il DM approva una mappa]` · **C**

- Misurato il 2026-10-09: 46 simboli-oggetto usati su 61; i più presenti
  sono fuoco, rocce, fiamme e porte; i mobili sono rari (🪑 15 celle, 🛏 29).
- Poly Haven, 521 modelli CC0: rocce, alberi, statue, barili, casse,
  forziere, tavoli, panche, letto, librerie, vasi, candelabri. Mancano
  incudine, fontana, trono, altare, tenda, ossa, funghi: li copre Quaternius
  (Fantasy Props MegaKit, CC0, 60-70% gratuito; da verificare la licenza della
  parte a pagamento prima di usarlo).
- Script che scarica i modelli (il DM, come per le texture), Blender che li
  rende dall'alto con luce e scala fisse, tessere webp committate; il tema
  texture le usa al posto dei glifi. Restano glifi: fuoco ed effetti, porte,
  finestre e sbarre (ruotano con l'asse del muro).
- **Fatto il 2026-10-09, il codice** (questa PR, D18): l'audit in
  [`esperimenti/oggetti-cc0-2026-10/`](esperimenti/oggetti-cc0-2026-10/RISULTATI.md);
  `build_oggetti_cc0.py` (scarica i glTF 1k con l'MD5 di ogni file verificato
  contro l'API, quattro MD5 fissati, estrae Quaternius dallo zip Standard con
  impronta e licenza verificate, rende con Blender o con il modulo `bpy`, scrive
  tessere webp da 96 px e l'indice); `scripts/blender/rendi_oggetti.py` con un
  lock solo per il set; il renderer, che nel tema texture usa la tessera dove
  c'è e il glifo dove no (`render.tessera_cc0: false` in `legend.yaml`, il muretto orientabile, la fiammella
  sopra il braciere); `dm.py asset oggetti`, `doctor`, manifest, 26 test,
  guida §5.1.1, secondo emendamento di ADR-0085, una norma nel registro.
- **Misurato**: dei 61 simboli-oggetto il corpus ne usa 46; delle 3.386 celle
  che li portano, Poly Haven ne copre 800 (24%), Quaternius al più 138 (4%),
  e il 72% resta glifo per scelta (fuoco, pendenze, fiamme, porte).
- **Restano al DM** (la rete dell'ambiente non raggiunge né Poly Haven né
  Quaternius, D19): il giro di prova con i modelli veri, il confronto
  glifi/oggetti su M7-D (interni) e sul cortile interno di ARC07 (esterno), la
  misura dello stile e del peso; poi tutti i modelli; poi lo zip Standard di
  Quaternius, da cui si scrive la tabella sui nomi veri.

### R8 · La resa misurata, e una sostituzione entra solo se migliora (D23-D27)

`[engine: Opus · effort: alto · qualità: ogni misura del livello A almeno pari alla pergamena, o scritta come difetto noto; il cancello in CI morde; il DM approva alla cieca]` · **C + G**

- Nasce dalla richiesta del DM del 2026-10-09: ogni sostituzione dev'essere
  migliorativa e misurata con algoritmi, glifo per glifo, comprese le texture
  della #227. [ADR-0086](adr/ADR-0086-una-sostituzione-nella-resa-entra-solo-se-misurata-e-preferita.md),
  [esperimento](esperimenti/misura-resa-2026-10/RISULTATI.md).
- **Fatto il 2026-10-09**: `misura_resa.py` (livello A, cancello in CI),
  `misura_resa_appresa.py` (livello B, secondo parere), confronto alla cieca
  (`coppie`, `voti`); `build_oggetti_cc0 --check` vuole verdetto e preferenza;
  `tara` per alone e velature, `tara --candidati` per le texture; la scheda
  committata (244 misure di simboli, 20 di terreni).
- **Misurato sulla #227 e corretto**: contrasto mediano dei glifi nel tema
  texture da 4,46 a 7,78 negli interni (pergamena 7,90), sotto 3:1 da 17 a 6;
  il tema texture pesa 8,44 MB, +0,85 MB per l'alone.
- **Recuperato il 2026-10-09** (il DM: *«tutto quello presente qui sarà
  riportato nel repo?»*). Questi strumenti erano stati usati per decidere, in
  questa sessione e in quella della #227, ma non erano mai stati messi nel repo:
  - `misura_resa.py velature`: la griglia delle velature con cui il DM aveva
    scelto 0,30 (D16);
  - `misura_resa.py affianca`: la mappa com'era a una revisione e com'è, una
    accanto all'altra, con la quota di pixel cambiati;
  - `build_texture_cc0.py --cerca`: il criterio di scelta delle texture
    (parole chiave sul catalogo, poi i download), che prima non era scritto;
  - `test_blender_vero.py`: la prova della scena con Blender vero su modelli
    procedurali, senza rete;
  - `gate_locale.py`: i gate della CI letti da `ci.yml` ed eseguiti in locale.

  L'inventario completo è in STATO-E-ORDINE §2-ter.
- **Sulla macchina del DM, il 2026-10-09 pomeriggio:**
  - **`tara --candidati`** propone ⛰ → `lichen_rock` (ΔE dal vicino da 1,48 a
    7,6) e 🔳 → `plank_flooring` (da 2,29 a 5,47). Per ⬛ tiene
    `roof_slates_02`: il candidato migliore arrivava a 5,16, contro 5,53.
    Prima di entrare in `TEXTURE` le due texture aspettano l'occhio del DM
    (D27).
  - **Il livello B** è girato: `--scarica-pesi` ha preso i tre file di pesi di
    `piq` (impronte nel registro di `misura_resa_appresa`), e 244 celle sono
    misurate in `appresa.json`. Manca `misura_resa.py appresa` che le porta
    nella scheda.
  - **Il giro di prova degli oggetti** si è fermato al render: `comando_blender`
    sceglieva il Blender di Debian (4.3, compilato senza OpenImageDenoise)
    invece del `bpy` 5.2 del `.venv`. Corretto in due modi: il modulo viene
    prima del programma, e la scena spegne il denoise dove la build non ce l'ha,
    dicendolo.
  - Corretti anche `voti`, che cercava la chiave accanto a `voti.json` (in
    `~/Scaricati`) e non accanto alla pagina, e due traceback diventati
    messaggi (`voti` senza file, `--adotta` senza tessere).
  - Nel codice del repo c'era un solo avviso di deprecazione: `getdata` di
    Pillow, sostituito. I tre avvisi di `piq` (`torch.jit.load`,
    `pretrained=` di torchvision) vengono dalla libreria: si filtrano solo
    quelli, solo mentre le metriche si costruiscono.
  - ComfyUI è installato, torch vede la GPU, e il checkpoint SDXL è verificato
    (sha256 `31e35c80…`, ora nel registro dei modelli di `comfyui_batch`).
- **Resta**: le texture nuove per ⛰ e 🔳 (D27, l'occhio del DM); il confronto
  alla cieca dell'alone e di ogni tessera (D23); il livello B nella scheda
  (D26); la prima immagine di ComfyUI.

### R4-quinquies · ComfyUI come terza fonte, in prova (D25)

- Il banco dei prompt (8 simboli × 4 semi, stile a inchiostro e acquerello, sfondo
  bianco) in `esperimenti/oggetti-cc0-2026-10/comfyui/`, e
  `build_oggetti_cc0.py --da-immagini` che ne fa tessere candidate.
- **L'installazione, rivista il 2026-10-09** dopo la domanda del DM *«gli script
  configurano ComfyUI? i passi ci sono?»*. Non del tutto: gli script di
  `scripts/comfyui-local/` erano scritti per Bazzite, ma la macchina del DM è
  Debian. Mettevano tutto in `/home`, dove restano 11 GB contro i ~15 che
  servono, e i pesi andavano scaricati a mano. Adesso:
  - `COMFYUI_DIR` sceglie il disco, e un controllo dello spazio ferma il setup
    prima di riempirlo;
  - se mancano Distrobox e Podman, il setup dice come installarli su Debian;
  - alla fine stampa se torch vede la GPU;
  - `scarica-pesi.sh` scarica SDXL 1.0 base e ne verifica lo sha256 contro
    quello che Hugging Face pubblica.

  Gli script restano **mai provati su una macchina vera**: la rete di questo
  ambiente non raggiunge né Hugging Face né una GPU. *(Il 2026-10-09 il DM li
  ha lanciati da `ambiente.py installa --con comfyui`. Il box si crea con la
  GPU e il clone riesce, ma il passo 4 si fermava, perché distrobox non monta
  `/srv`. Corretto; il secondo giro è in corso.)*
- **L'adozione dopo i voti**: `build_oggetti_cc0.py --adotta [DIR]` tiene solo le
  tessere che la misura non boccia e che il DM ha preferito. Senza `DIR`
  sfoltisce le CC0, con `DIR` copia le candidate di ComfyUI e stampa le righe di
  `GENERATE`. Prima mancava: `--check` (D23) bocciava le tessere perdenti e
  nessun comando le toglieva. GUIDA-MAPPE §5.1.2 ha la trafila *«da zero, in
  ordine»*, dal ramo al commit.
- **Resta al DM**: la generazione sulla sua GPU; poi misura e coppie.

### R5 · Città, villaggi ed edifici da Watabou

`[engine: Sonnet · effort: medio · qualità: un'esportazione vera per tipo, importata, collaudata a zero errori, con il seme scritto]` · **C**

- `import_watabou.py` sa leggere i dungeon. Mancano le città (Medieval
  Fantasy City Generator), i villaggi e gli edifici (Dwellings), le cui mappe
  il generatore permette di usare *«as you like»*, anche commercialmente.
- Serve qualche esportazione JSON vera di ciascuno (D7): senza, l'importatore
  si scriverebbe su un formato indovinato.
- Le mappe importate escono con `@tipo tattica abitato` o `interni`.
- **Fatto il 2026-10-09** (D10): le cinque carte dell'assedio di Dauth
  (`DAY3-CITY-SIEGE`) in sei griglie da contratto JSON, in
  `09_…/Mappe/dauth-assedio/` (il chiostro e il suo cunicolo sono due mappe
  collegate da `@collega`), collaudate a zero errori e zero avvisi. La pianta
  della città: la scheda `dauth-pianta.watabou.json` con seme e parametri, e
  `dm.py maps citta`, che ne ricava l'URL (`watabou_citta.py`). La rete di
  questo ambiente non raggiunge Watabou: l'esportazione la fa il DM.

### R6 · Le regionali con Azgaar

`[engine: Sonnet · effort: medio · qualità: un file .map committato come master, l'SVG esportato accanto, il seme scritto]` · **C**

- Azgaar Fantasy Map Generator (MIT) per una **regione inventata**: la
  geografia di Faerûn è canone e non si genera (`forgotten-realms-lore`).
- Quale regione è la D8.

### R7 · I residui, dichiarati

- Le emoji ripetute come testo nelle righe di legenda restano al font di
  sistema: incorporarle costerebbe 3,7 MB (ADR-0085).
- `☁` (71 celle) e `🔲` (15) hanno già un universale (`🌫`, `🟪`); `💠` resta
  locale. Cambiarle su mappe giocate è V3 di COLLAUDO-MAPPE, col DM.

## §4 · La validazione

| Lotto | Cosa lo dice chiuso |
|---|---|
| R1 | `build_font_mappe.py --check` e `validate_maps` verdi; nessun `<text>` delle mappe resta al font di sistema, salvo le emoji delle righe di legenda (R7) |
| R2 | `test_resa_mappe.py`: glifi diversi da `🔮` e `🪨`, nessuna chiave doppia nei dizionari del renderer |
| R3 | `build_emoji_noto.py --check` verde in `test_resa_mappe.py`; licenza e crediti nella cartella |
| R4 | il DM approva una mappa nel tema dipinto; il colophon porta il credito |
| R4-bis | `build_texture_cc0.py --check` e `validate_maps` verdi con le texture vere; il DM approva una mappa nel tema texture accanto alla pergamena |
| R4-ter | `build_oggetti_cc0.py --check` e `validate_maps` verdi con le tessere vere; `--misura-stile` scritto in RISULTATI §4; il DM approva M7-D e il cortile di ARC07 accanto alla versione a glifi, prima di estendere; il peso degli SVG misurato |
| R5 | un'esportazione per tipo importata e collaudata a zero errori |
| R6 | il master `.map` committato e l'SVG rigenerabile |

---

## §7 · Le decisioni del DM

<!-- decisioni-dm: RESA-ASSET -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | R1 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **Il testo delle mappe come lo uniformo ai volumi?** Proposta: font OFL incorporati in sottoinsieme (+52 KB stimati a SVG; misurati 43) |
| ~~D2~~ | R2, R3 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto, tutte e due.** Era: **Le 177 celle a emoji di sistema?** Proposta: nuovi universali in casa dove il significato è uno, e il ripiego Noto per il resto. game-icons.net per le legende non scelto |
| ~~D3~~ | R4 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un tema «dipinto» con 2-Minute Tabletop?** Proposta mia: non raccomandata (lavoro grosso, deroga alla regola 5); il DM l'ha scelta |
| ~~D4~~ | R5 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un importatore Watabou per città, villaggi, edifici?** |
| ~~D5~~ | R6 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Azgaar FMG per le regionali?** Solo per regioni inventate |
| ~~D6~~ | R4 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: come proposto.** Era: **Quali pacchetti di 2-Minute Tabletop, e dove stanno?** Proposta: si comincia con un pacchetto solo, quello dei dungeon; i PNG restano sulla macchina del DM (cartella ignorata da git) e il repo tiene solo la tabella `simbolo → file` e i crediti, perché un pacchetto pesa decine di MB |
| ~~D7~~ | R5 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: R5 si rimanda** finché non ci sono le esportazioni vere. Era: **Le esportazioni di Watabou da cui partire.** Servono una città, un villaggio e un edificio esportati in JSON dal DM, con il loro seme: l'importatore si scrive su file veri |
| ~~D8~~ | R6 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: nessuna per ora**, come proposto. Era: **Quale regione inventata con Azgaar?** Proposta: nessuna finché un arco non ne chiede una; il lotto resta pronto |
| ~~D9~~ | R4 | ✅ **Decisa il 2026-10-09, il DM: una prova su una mappa.** Era: **R4 come procede?** Il DM aveva chiesto a cosa serve e se valeva un download automatico; la misura: il pacchetto gratuito dei dungeon ha 131 tessere e copre circa 10-15 degli 86 simboli, i link arrivano per email dopo una cassa a 0 $, la rete dell'ambiente non raggiunge Dropbox. Proposta: un installatore (`dm.py asset installa <zip>`) con guida e controllo in `doctor`, poi una sola mappa di interni nel tema dipinto, da confrontare con la pergamena |
| ~~D10~~ | R5 | ✅ **Decisa il 2026-10-09, il DM: si parte da Dauth.** Era: **R5 come procede?** Proposta: la guida per esportare da Watabou la pianta di Dauth assediata, da usare come immagine; le cinque mappe tattiche dell'assedio (carte A-E di `DAY3-CITY-SIEGE`) col contratto JSON; l'importatore di città ed edifici solo se le esportazioni vere lo meritano. Sostituisce il «rimandato» di D7 |
| ~~D11~~ | R6 | ✅ **Decisa il 2026-10-09, il DM: resta in attesa**, come proposto. La Cannath Vale è la Elsir Vale di *Red Hand of Doom* rinominata: è canone e non si genera. Nessun codice finché un arco non porta i PG in una regione inventata |
| ~~D12~~ | R4 | ✅ **Risposta del DM il 2026-10-09: al tavolo usa Foundry.** Era: **Usi un VTT?** Decide il valore di R4: la resa dipinta va nell'export UVTT come immagine di sfondo |
| ~~D13~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: sì, CC0 principale**, come proposto. Era: **Le texture CC0 (Poly Haven, ambientCG) diventano la strada principale per mappe più ricche, e 2-Minute Tabletop un extra opzionale solo per il tavolo?** Il DM aveva chiesto una strada senza problemi di licenza; le licenze lette alla fonte: Poly Haven e ambientCG CC0 1.0 |
| ~~D14~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: committate accanto alla pergamena**, non come proposto. Era: **Le mappe con texture dove finiscono?** Proposta: solo in locale. Scelto: un secondo SVG per ogni mappa in `rendered-texture/`, controllato da `validate_maps`; stima +2,3 MB sui 50 SVG |
| ~~D15~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: glifi ora, IA locale dopo.** Era: **Gli oggetti di scena da dove vengono?** I glifi in casa restano sopra le texture; un lotto futuro genera oggetti zenitali con ComfyUI e pesi a licenza permissiva (ADR-0019), col gate di rifiuto di `rumblingstone-art-direction` |
| ~~D16~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: velatura 0,30**, come proposto, dopo il confronto 0,45 / 0,30 / 0,20 sulle texture vere (M7-D per gli interni, Hammerfist L1 per l'esterno). Era: **Quale velatura per il tema texture?** A 0,45 erba e sentiero sembravano tinte piatte; a 0,20 muri e pavimenti degli interni si avvicinavano di tono |
| ~~D17~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: modelli 3D di Poly Haven e Quaternius**, non come proposto (solo Poly Haven). Era: **Gli oggetti di scena nel tema texture da dove vengono?** Modelli 3D CC0 renderizzati dall'alto con Blender in tessere webp, solo per il tema texture; Quaternius (Fantasy Props MegaKit, CC0, solo la parte gratuita) per ciò che Poly Haven non ha. Sostituisce l'IA locale di D15 |
| ~~D18~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: in una PR nuova, dopo il merge della #227**, non come proposto (nella #227) |
| ~~D19~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: sulla sua macchina**, come proposto. Era: **I modelli 3D (2,5-6 MB l'uno, 50-70 MB in tutto) dove stanno, e chi li rende?** Restano in `asset-esterni/oggetti-cc0/`, ignorata da git; il DM scarica e rende con `bpy` nel `.venv` o con il binario Blender; nel repo entrano solo le tessere e l'indice. Scartate: nel ramo solo per il render, nel repo per sempre |
| ~~D20~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: impronta uguale**, come proposto. Era: **Che scala hanno gli oggetti nella cella?** Il lato lungo di ogni modello al 76% della cella, come i glifi; l'indice tiene la misura vera e il fattore. Scartata: la scala vera (1 cella = 1,5 m) |
| ~~D21~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: sì, ma 🧱 diventa un modello**, non come proposto. Era: **Restano glifi anche segnali, creature, strutture in scala di mappa, scale e buchi, muretto, affresco e gru?** Il muretto (94 celle) è un oggetto orientabile, con due tessere rese girando il modello |
| ~~D22~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: focolare con la fiamma glifo sopra**, come proposto. Era: **Il braciere 🏮: Poly Haven ha solo un focolare spento.** Scartate: solo il focolare, resta glifo |
| ~~D23~~ | R8 | ✅ **Decisa il 2026-10-09, il DM: misura e preferenza, tutte e due**, come proposto. Era: **Quando una sostituzione (tessera da modello CC0, da ComfyUI, o una texture) prende il posto di un glifo o di un terreno?** Le misure del livello A non peggiorano (contrasto del contorno ≥ 3:1 o ≥ 90% del glifo, WCAG 1.4.11; non si confonde di più col vicino, SSIM; resta nella tavolozza, ΔE2000) **e** il DM la preferisce nel confronto a coppie alla cieca; in CI un cancello blocca chi peggiora la scheda committata oltre il 5%. Scartate: solo la preferenza, solo la misura |
| ~~D24~~ | R8 | ✅ **Decisa il 2026-10-09, il DM: correggo e rimisuro**, come proposto. Era: **Il tema texture della #227 misurato contro la pergamena: glifi che perdono contrasto, ⛰ e 🔳 indistinguibili, ⬛ vicino al suo vicino, il segnalino su ⬜ che sparisce.** Nel solo tema texture un alone chiaro sotto glifi e segnalini e velature per terreno, tarati da `misura_resa.py tara` finché ogni misura è almeno pari alla pergamena. Scartate: velatura più alta per tutti, lasciare com'è |
| ~~D25~~ | R4-quinquies | ✅ **Decisa il 2026-10-09, il DM: sì, giro di prova**, come proposto. Era: **ComfyUI in locale come terza fonte di oggetti?** Sulla GPU del DM, gli otto simboli del giro di prova, SDXL (ADR-0019), quattro semi ciascuno, sfondo tolto, gate di rifiuto di art-direction; ogni tessera passa da `misura_resa.py` e dalle coppie, contro glifo e modello CC0 |
| ~~D26~~ | R8 | ✅ **Decisa il 2026-10-09, il DM: secondo parere**, come proposto. Era: **Le metriche apprese (LPIPS, DISTS, CLIP-IQA di piq) che ruolo hanno?** Girano sulla macchina del DM con `misura_resa_appresa.py`, i pesi restano lì, il JSON entra nella scheda e non blocca; diventano cancello solo se concordano con le preferenze del DM (κ ≥ 0,6). Scartate: cancello subito, non servono |
| ~~D27~~ | R8 | ✅ **Decisa il 2026-10-09, il DM: cambio texture, le scarica lui**, come proposto. Era: **Con l'alone a 0,75 i glifi tornano al livello della pergamena; restano ⛰/🔳 a ΔE 1,48 e ⬛/🔳 a 2,29, più ⛰/⬛ e ⛰/🟤, che la velatura non separa senza cancellare la foto.** Tre candidati CC0 per ⛰ 🔳 ⬛ (`build_texture_cc0.py --candidati`), scelti da `misura_resa.py tara --candidati`; nel frattempo alone 0,75 e velature minime committati, le quattro coppie come difetto noto. Scartate: velature alte, tinte diverse |
| ~~D28~~ | R8 | ✅ **Decisa il 2026-10-09, il DM: le texture si tengono solo dopo una scelta vera**, non come proposto. Il DM: *«le tengo se tengono conto di queste obiezioni e quindi mi fanno davvero scegliere oppure buttare quell'immagine per quella tipologia se non c'è nessuna valida»*. Le obiezioni: la prima pagina alla cieca non diceva a cosa si riferiva ogni immagine, aveva molte coppie identiche, non permetteva di rispondere «nessuna» e non distingueva ComfyUI dalle altre fonti. Era: **Le texture della fase 2 (⛰ roccia con licheni, 🔳 assi): le tieni dopo averle viste?** Fatto: una pagina di scelta per oggetti (`coppie`, più fonti con `--anche`) e terreni (`terreni-scelta`), riquadri con il nome, opzioni identiche tolte e dichiarate, «nessuna va bene» e «non vedo differenze», alla cieca o `--aperta`; `voti` rivela le fonti; `build_oggetti_cc0 --check` e `build_texture_cc0 --check` fanno valere la scelta |
| ~~D29~~ | — | ✅ **Decisa il 2026-10-09, il DM: «sì, assolutamente»**, come proposto. Era: **M7-C: correggo i 18 rilievi del collaudatore in questa PR o in una nuova?** In questa PR. Fatto: i 18 rilievi applicati alla mappa, il master DEF-4 resta canone, le celle non scritte nel testo marcate `[PROPOSTA]`; il collaudo dà 0 errori e 0 avvisi |
| ~~D30~~ | — | ✅ **Decisa il 2026-10-09, il DM: «vedi di correggere la griglia se possibile»**, non come proposto il 2026-09-11 (D10 di RICERCA-MESTIERE: «completare è progettazione»). Era: **PF-4 dichiara 33×33 con 25 righe; il Campo Drow 1 del P1C dichiara 53×40 con 33 colonne: va corretta la dichiarazione o completata la griglia?** Completata dove la geometria scritta lo permette: PF-4 per specchio attorno alla riga 17 più le passerelle delle POSIZIONI; il Campo Drow 1 dal SUPPLEMENTO-P1C (25 righe su 40), completato e copiato nel P1C. Le righe ricostruite sono `[PROPOSTA]` |

<!-- eco: RESA-ASSET 2026-10-08 -->
- **Decise**: D1 i font dei volumi incorporati · D2 universali in casa e ripiego Noto · D3 il tema dipinto con 2-Minute Tabletop · D4 l'importatore Watabou · D5 Azgaar per le regionali
- **Aperte**: D6 quali pacchetti e dove stanno, D7 le esportazioni di Watabou, D8 quale regione
- **Cambiate**: D3, dove avevo sconsigliato il tema dipinto, e scipy (D17 di COLLAUDO-MAPPE), dove avevo proposto di non ammettere nessuna libreria
- **Dedotto da me**: che i nuovi universali siano solo i concetti che hanno lo stesso significato in ogni mappa (`🔺`, `🔷`), e che `💠` resti locale; che il ripiego Noto valga per le celle e non per le emoji ripetute nelle righe di legenda, che costerebbero 3,7 MB; che il corsivo dei font si lasci fuori per il peso; che il tema dipinto sia una seconda resa per i giocatori e non sostituisca la pergamena del DM
- **Decise** (terzo messaggio): D6 un pacchetto solo, quello dei dungeon, con i PNG fuori dal repo · D7 R5 rimandato finché non ci sono esportazioni vere · D8 nessuna regione per ora
- **Aperte** (terzo messaggio): nessuna
- **Dedotto da me** (terzo messaggio): che R4 non parta finché il DM non ha scaricato il pacchetto: la tabella `simbolo → file` si scrive sui nomi veri dei file, non su nomi indovinati

<!-- eco: RESA-ASSET 2026-10-09 -->
- **Decise**: D9 R4 come prova su una mappa, con l'installatore · D10 R5 a partire da Dauth · D11 R6 in attesa · D12 il DM usa Foundry
- **Aperte**: nessuna
- **Cambiate**: D7, da «R5 rimandato» a «R5 parte da Dauth»
- **Dedotto da me**: che l'installatore non scarichi niente da solo, perché i link del pacchetto arrivano per email dopo la cassa e la licenza chiede di mandare chi vuole i file al sito; che le cinque mappe dell'assedio stiano in `Mappe/` dell'arco 09 e le prenda il futuro `ARC09-DEF-05` di MASTER-DEF, senza scrivere il master qui; che la pianta della città resti un'immagine esportata da Watabou e non diventi una griglia
- **Decise** (secondo messaggio): D13 le texture CC0 strada principale, 2-Minute Tabletop extra opzionale · D14 il tema texture committato accanto alla pergamena · D15 glifi ora, oggetti generati con l'IA locale in un lotto futuro
- **Aperte** (secondo messaggio): nessuna
- **Cambiate** (secondo messaggio): D14, dove avevo proposto il tema texture solo in locale; e R4, che da strada principale diventa un extra per il tavolo
- **Dedotto da me** (secondo messaggio): che le texture vengano da Poly Haven sola, perché ha un'API con l'MD5 di ogni file (ambientCG resta ammessa, non usata); che il bosco fitto, l'acqua, la lava e i pilastri restino vettoriali; che il muro scelga roccia o muratura dall'ambiente di `@tipo`; che il tema texture diventi obbligatorio per `validate_maps` solo dopo il commit delle texture
- **Decise** (terzo messaggio): D16 la velatura 0,30, scelta guardando le texture vere
- **Aperte** (terzo messaggio): nessuna
- **Dedotto da me** (terzo messaggio): che il peso vada riscritto con la misura vera: i 53 SVG del tema texture pesano 7,6 MB, contro i 6,2 MB della pergamena; la stima di +2,3 MB contava solo le texture e non il resto di ogni SVG
- **Decise** (quarto messaggio): D17 gli oggetti di scena del tema texture dai modelli 3D CC0 di Poly Haven e Quaternius · D18 il lotto in una PR nuova dopo la #227
- **Aperte** (quarto messaggio): nessuna
- **Cambiate** (quarto messaggio): D15, l'IA locale per gli oggetti, sostituita da D17; D17 aggiunge Quaternius alla proposta; D18 sposta il lotto fuori dalla #227
- **Dedotto da me** (quarto messaggio): che Quaternius si usi solo per i simboli che Poly Haven non copre, e solo nella parte gratuita, dopo aver letto se la licenza CC0 vale anche per la parte a pagamento; che fuoco, effetti, porte, finestre e sbarre restino glifi
- **Decise** (quinto messaggio, R4-ter): D19 i modelli sulla macchina del DM · D20 l'impronta uguale nella cella · D21 i glifi che restano, e il muretto che diventa un modello · D22 il braciere come focolare con la fiamma glifo sopra
- **Aperte** (quinto messaggio): nessuna
- **Cambiate** (quinto messaggio): D21, dove avevo proposto il muretto fra i glifi; quindi un lotto in più nel codice, le tessere orientabili
- **Decise** (sesto messaggio, R8 e R4-quinquies): D23 misura e preferenza del DM, con un cancello in CI · D24 il tema texture corretto e rimisurato · D25 ComfyUI come terza fonte, in prova · D26 le metriche apprese come secondo parere
- **Aperte** (sesto messaggio): nessuna
- **Cambiate** (sesto messaggio): nessuna; la D15 («IA locale»), superata da D17, torna come fonte in prova con D25, accanto ai modelli CC0 e non al loro posto
- **Dedotto da me** (sesto messaggio): che il DM, dicendo che letti e detriti sembrano più belli come glifi, chiedesse una regola e non un'eccezione per due simboli, quindi la misura vale per ogni sostituzione, texture della #227 comprese; che la misura giusta di un'icona sia il contrasto del suo contorno contro ciò che le sta intorno, con la maschera della figura sola, perché la prima versione misurava il terreno sotto l'alone e dava l'alone peggiorativo; che il giro ComfyUI chieda lo stile della casa (inchiostro e acquerello) e non una fotografia, perché è lì che può battere i modelli CC0; che i pesi delle metriche apprese restino sulla macchina del DM come i modelli 3D (D19), invece di passare in chat; che una tessera generata entri con la provenienza di ADR-0019 al posto della licenza CC0

<!-- eco: RESA-ASSET 2026-10-09 -->
- **Decise** (settimo messaggio): D27 texture nuove per ⛰ 🔳 ⬛, scaricate dal DM
- **Aperte** (settimo messaggio): nessuna; il confronto alla cieca dell'alone resta al DM, con l'immagine di M7-D mandata in chat
- **Cambiate** (settimo messaggio): la taratura delle velature, dalla prima versione che velava fino a 0,80 alla seconda che si ferma dove la distanza non cresce
- **Dedotto da me** (settimo messaggio): che la taratura debba alzare la velatura solo dove la distanza cresce davvero, perché la prima versione aveva portato quattro terreni a 0,80 senza separare ⛰ da 🟤; che i candidati si scelgano per tonalità diversa da quella dei vicini (legno o marmo per la pedana, tetti caldi per l'edificio), non per somiglianza col materiale di oggi
- **Decise** (ottavo messaggio): D28 le texture e le tessere solo dopo una scelta vera, con «nessuna» · D29 M7-C corretta in questa PR · D30 le griglie di PF-4 e del Campo Drow 1 completate
- **Aperte** (ottavo messaggio): le celle `[PROPOSTA]` di M7-C, PF-4 e Campo Drow 1, da confermare guardando le mappe
- **Cambiate** (ottavo messaggio): D10 di RICERCA-MESTIERE, dove le griglie incomplete si marcavano senza completarle; la pagina alla cieca di D23, che diventa una pagina di scelta
- **Dedotto da me** (ottavo messaggio): che le coppie identiche venissero dai simboli che la legenda tiene glifo o senza webp, non da una cache del renderer, perché il renderer rilegge l'indice a ogni banco; che «nessuna va bene» per un terreno voglia dire togliere la texture finché non se ne trova un'altra, e che «senza texture» vada mostrata come opzione accanto alle altre; che la fonte di una tessera sia quella dichiarata nel suo indice e non la cartella, altrimenti una tessera ComfyUI adottata in `scripts/oggetti-cc0/` cambierebbe nome; che il secondo «17» di PF-4 (D12 di RICERCA-MESTIERE) fosse una didascalia con 3 celle e non una riga duplicata
- **Dedotto da me** (quinto messaggio): che Poly Haven non avendo muretti, il candidato per 🧱 sia `namaqualand_rocks_01`, una fila di pietre, da giudicare nel giro di prova; che il muretto occupi la cella intera sul lato lungo, perché due tratti vicini devono toccarsi; che la tessera nord-sud si scelga dai muretti vicini, senza una direttiva nuova; che la licenza della versione Pro di Quaternius non sia scritta abbastanza da usarla (il sito dice «free to use», non «CC0»), quindi solo la Standard, come chiedeva D17; che il confronto per il DM non si faccia sulle forme procedurali della prova della catena, che porterebbero a giudicare la resa su oggetti finti

## §8 · Lo stato di ogni voce (2026-10-09, dopo il merge della #227)

Richiesto dal DM con R4-ter: per ogni lotto e ogni decisione, se è **fatto**,
**superato** da una decisione dopo, **ancora da fare** o **obsoleto**, con il
commit, il file o la decisione che lo dice. I commit sono quelli della #227
(merge `f40ffeb`).

| Voce | Stato | Prova |
|---|---|---|
| R0 audit | ✅ fatto | `69930a2`; [`esperimenti/dipendenze-e-asset-2026-10/`](esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md) |
| R1 font dei volumi nelle mappe (D1) | ✅ fatto | `69930a2`; `build_font_mappe.py --check` verde |
| R2 `🔺` `🔷` universali (D2) | ✅ fatto | `69930a2`; `test_resa_mappe.py` |
| R3 ripiego Noto (D2) | ✅ fatto | `69930a2`; `build_emoji_noto.py --check` verde |
| R4 installatore 2-Minute Tabletop, `dm.py asset`, doctor, guida §5.2 (D6, D9) | ✅ fatto | `b8423c1` |
| R4 come strada per mappe più ricche (D3) | ⏭ superato da D13 | `c630264`: 2-Minute Tabletop diventa un extra per il tavolo del DM, la strada principale sono le texture CC0 |
| R4 tabella `simbolo → file` e la mappa di prova nel tema dipinto | ⏳ da fare, solo se il DM scarica il pacchetto base | D9; la tabella si scrive sui nomi veri dei file |
| R4 sfondo dipinto nell'export UVTT per Foundry (D12) | ⏭ superato: per Foundry lo sfondo è il PNG del tema texture | `c630264`, GUIDA-MAPPE §5.1: `export_map_png.py` sull'SVG di `rendered-texture/`, poi `export_uvtt.py --image`. Il tema dipinto resterebbe un secondo sfondo possibile, non uno che manca |
| R4-bis tema texture CC0 (D13, D14, D16) | ✅ fatto | `260210e` codice, `476287e` `.gitignore`, `1bbf7bf` 11 tessere e 53 SVG, `32ee061` velatura 0,30 |
| R4-bis oggetti con l'IA locale (D15) | ⏭ superato da D17 | `ef0c492`: modelli 3D CC0 al posto delle immagini generate |
| R4-ter codice, audit, guida, ADR (D17-D22) | ✅ fatto | questa PR; [`esperimenti/oggetti-cc0-2026-10/`](esperimenti/oggetti-cc0-2026-10/RISULTATI.md) |
| R4-ter giro di prova, confronto, misura dello stile e del peso | ⏳ da fare, il DM | GUIDA-MAPPE §5.1.1; RISULTATI §4 e §6 aspettano i numeri |
| R4-ter tutti i modelli Poly Haven | ⏳ da fare, dopo il confronto | D17: «prima di estenderla» |
| R4-ter Quaternius | ⏳ da fare: lo zip Standard dal DM, poi la tabella sui nomi veri | `QUATERNIUS = ()` in `build_oggetti_cc0.py` |
| R5 le sei griglie dell'assedio di Dauth (D10) | ✅ fatto | `b8423c1`; collaudate a zero errori |
| R5 scheda della pianta e `dm.py maps citta` | ✅ fatto | `b8423c1`; `watabou_citta.py` |
| R5 la pianta di Dauth esportata da Watabou | ⏳ da fare, il DM | la rete dell'ambiente non raggiunge Watabou |
| R5 importatore di città, villaggi, edifici (D4) | ⏳ da fare solo con esportazioni vere | D7, poi D10 |
| R5 i tre `[INFERRED]` delle griglie di Dauth | ⏳ da fare, il DM | C1: barelle e giacigli come terreno ingombro che costa doppio; E: dove porta la botola in G02; E: il sabotatore con la chiave, Ladro 7, in B6. Un quarto sta nella scheda della pianta: la piazza dell'arena del Torneo |
| R6 Azgaar per una regione inventata (D5) | ⏸ in attesa | D8, D11: nessuna regione finché un arco non la chiede |
| R7 residui (`☁`, `🔲`, `💠`, emoji nelle righe di legenda) | ⏳ da fare in V3 di COLLAUDO-MAPPE | §3, R7 |
| D7 «R5 rimandato» | ⏭ superato da D10 | `b8423c1` |

Le voci dei documenti più vecchi che la #227 ha reso inutili stanno in
[STATO-E-ORDINE-DEI-PIANI](STATO-E-ORDINE-DEI-PIANI.md), §2-bis: è un
inventario che attraversa più piani, e lì si legge una volta sola.

---

## Checklist di avanzamento

```
Fase A — Audit
☑ R0  librerie rimisurate, resa non uniforme misurata, asset e licenze (2026-10-08)

Fase S — Sviluppo
☑ R1  i font dei volumi dentro le mappe (2026-10-08: 47 SVG, +2,08 MB)
☑ R2  🔺 e 🔷 universali, glifi in casa (2026-10-08)
☑ R3  il ripiego Noto, 12 emoji locali (2026-10-08: 177 celle → 0)
□ R4  il tema dipinto: una prova su una mappa (D9); ☑ installatore, `dm.py asset`, doctor e guida (2026-10-09) · □ la tabella simbolo → file e la mappa di prova, quando il DM ha scaricato il pacchetto base
□ R4-bis il tema texture CC0 (D13-D16): ☑ script, tema, gate e guida · ☑ le 11 texture scaricate dal DM e i 53 gemelli committati (7,6 MB) · ☑ la velatura tarata a 0,30 (D16) (2026-10-09) · ~~gli oggetti con l'IA locale (D15)~~, sostituita da R4-ter (D17)
□ R4-ter gli oggetti di scena dai modelli 3D CC0 (D17-D22): ☑ audit, script, scena Blender, renderer, gate, guida e ADR (2026-10-09, PR nuova come da D18) · □ il giro di prova e il confronto del DM sui modelli veri · □ tutti i modelli Poly Haven · □ Quaternius, dallo zip Standard
□ R8  la resa misurata (D23-D28): ☑ misura, cancello in CI, confronto alla cieca, taratura, scheda (2026-10-09) · ☑ alone 0,75, glifi del tema texture alla pari della pergamena · ☑ la pagina di scelta al posto delle coppie (D28): oggetti con più fonti, terreni con `terreni-scelta`, «nessuna va bene» e «non vedo differenze», i due `--check` che la fanno valere (2026-10-09) · □ la scelta del DM sulle texture di ⛰ 🔳 ⬛ (D27) e sulle tessere CC0 · □ il livello B
□ R4-quinquies ComfyUI in prova (D25): ☑ banco dei prompt e conversione · ☑ installazione per Debian, `COMFYUI_DIR`, `scarica-pesi.sh`, `--adotta`, trafila da zero · ☑ installato sulla macchina del DM, GPU vista, SDXL verificato (2026-10-09) · □ la generazione sulla GPU del DM, poi misura e `coppie … --anche` accanto alle CC0
□ R5  Watabou, a partire da Dauth (D10): ☑ le mappe dell'assedio, cinque carte in sei griglie collaudate a zero (2026-10-09) · ☑ la scheda e `dm.py maps citta` per la pianta · □ la pianta esportata dal DM · □ l'importatore, solo con esportazioni vere
□ R6  le regionali con Azgaar: in attesa (D8, D11), nessun codice
□ R7  i residui: in V3 di COLLAUDO-MAPPE

Fase V — Validazione: la tabella di §4
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna, nello stesso
> commit, questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
