# Immagini della serata e del −1000 — prompt eseguibili

**Cos'è.** I ritratti e le tavole che mancano alla serata della resurrezione e al
volume del viaggio a mille anni fa, scritti **nello stesso formato e nello stesso
stile del Drappo di Tarsilia**
(`STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`),
su richiesta del DM del 2026-09-24: le immagini devono sembrare della stessa mano.

Si generano con la stessa pipeline:

```
python3 scripts/comfyui_batch.py --prompts "07_il Portale Della Forgia Eterna/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md" --lista
python3 scripts/comfyui_batch.py --prompts "07_il Portale Della Forgia Eterna/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md" --serie tutto
```

I PNG escono accanto a questo file. Le schede-scena con il contesto narrativo
(fonte, destinatario, spoiler) restano in `PROMPT-IMMAGINI-07ILP.md`: **il testo
da dare al modello sta qui**, e c'è una copia sola.

> ⚖️ **Regola IP del repo**: si descrivono le convenzioni del look, mai il nome
> di un illustratore vivente, mai «in the style of». L'ancora è una scuola
> pittorica in pubblico dominio.

---

## §1 · Il look comune

**Identico al Drappo, tranne la tavolozza.** Le prime cinque righe (tecnica,
inquadratura, luce, materiali) sono le stesse parola per parola. L'ultima riga
del Drappo diceva *«muted river-town palette (wet ochre, iron grey, dyed
indigo), late-summer light»*: è la tavolozza di una città di fiume, e qui siamo
in una fortezza nanica e nella sua forgia. Cambia solo quella.

<!-- blocco id=look-comune -->
```
painterly digital illustration, crisp ink line underneath, visible brushwork,
three-quarter view, waist-up character sheet portrait, single hero focal point,
simple dark vignette background, warm-cool contrast, dramatic rim lighting,
weathered leather and cloth, muted mountain-hold palette (slate grey, forge
gold, moss green), torch and forge light
```

**L'ancora storica**, identica al Drappo:

<!-- blocco id=ancora-storica -->
```
northern renaissance oil glazing, flemish panel painting light,
egg-tempera restraint in the flesh tones
```

**Negativi**, identici al Drappo:

<!-- blocco id=negativi -->
```
modern clothing, plastic sheen, glamour, neon, text, watermark, logo,
oversaturated
```

**Formati**: ritratti **832 × 1216** (verticali, come le schede del Drappo),
tavole **1536 × 864**. I tratti del volto stanno nelle schede-personaggio di
`PROMPT-IMMAGINI-07ILP.md` e sono canone: li fissano i ritratti in
`Immagini/ritratti/`. Un prompt qui sotto si cambia solo insieme alla sua scheda.

---

## §2 · I sette ritratti del cast di mille anni fa

I file vanno poi copiati in `Immagini/ritratti/` col nome dell'`id` senza il
prefisso `ritratto-` (es. `ritratto-balvar-fuocospento.png` →
`ritratti/balvar-fuocospento.jpg`), e nella scheda del cast la riga «Ritratto
da generare» diventa l'immagine.

**Balvar Fuocospento — il runaio esiliato** *(si genera per primo: è il volto che conta di più)*
<!-- img id=ritratto-balvar-fuocospento size=832x1216 stile=ritratto serie=base -->
```
[look comune] + old shield dwarf seated on a workshop stool at the back of a
war tent of black hide, white beard dusted grey with slate powder, calm
unhurried eyes, leather workshop apron over a quilted dark green tunic, a slab of slate on his knees and an
iron stylus in his right hand, engraving slowly, he has just looked up
```
*La cosa che non deve mancare*: la punta di ferro sull'ardesia. Non smette di incidere.

**Zog'tar Deatheye — il generale**
<!-- img id=ritratto-zogtar-deatheye size=832x1216 stile=ritratto serie=base -->
```
[look comune] + huge half-ogre warlord, face lit strongly by a torch from the
left, left eye normal, in place of his RIGHT eye a smooth polished black
obsidian stone set into the socket, glossy, with a sharp highlight and a faint
living gleam like a pupil, no eyepatch, short tusks, old scars, blackened full
plate with rust-red cloth, two-handed greataxe resting on his shoulder,
counting on his fingers, dwarven bones hanging from the tent behind him
```
*La cosa che non deve mancare*: la pietra nera al posto dell'occhio destro.

**Re Thorek I — il re di una fortezza giovane**
<!-- img id=ritratto-re-thorek-i size=832x1216 stile=ritratto serie=base -->
```
[look comune] + ancient dwarf king, very long white beard in four braids,
heavy grey eyes, mithral armour, dark blue cloak, plain iron crown with no
gems, a great axe of pale blue-white steel with frost patterns along the
blade in his right hand, a war map on a stone table, freshly cut white walls
```
*La cosa che non deve mancare*: Frostcleaver in pugno, anche al tavolo.

**Thorgrim Barbadiferro — l'antenato**
<!-- img id=ritratto-thorgrim-barbadiferro size=832x1216 stile=ritratto serie=base -->
```
[look comune] + old dwarf warrior seated on a stone bench, head tilted back,
looking up at a golden light falling from above out of frame, iron-grey beard,
eyes wet without him noticing, empty hands open and raised toward the light,
palms turned up, the thick callus of an axe grip visible across the right palm, a
single-bladed dwarven war axe with a haft worn smooth leaning beside him, he
holds nothing
```
*La cosa che non deve mancare*: il callo sul palmo. È lo stesso di Thorik.

**Durin Rocciadura — la pattuglia**
<!-- img id=ritratto-durin-rocciadura size=832x1216 stile=ritratto serie=base -->
```
[look comune] + dwarf veteran guard at night in a pine forest, long brown
beard gathered in a single braid, eyes that keep moving, dented dark full
plate, green hood, round shield rimmed in dark blue on his back, a double-headed axe
held too tightly in both hands, torches of six other dwarves blurred behind
```
*La cosa che non deve mancare*: le mani strette sull'ascia. Ha paura.

**Mastro Costruttore Zeth — il seme del Ghostlord**
<!-- img id=ritratto-zeth-mastro-costruttore size=832x1216 stile=ritratto serie=base -->
```
[look comune] + thin half-elf master builder in a narrow torchlit mining
tunnel, high cheekbones, feverish bright eyes, a few days of stubble, rock
dust up to the elbows on an ochre work tunic, drawing runes on the wall with
chalk, one rune half erased by his thumb, a stone lion faintly carved behind
```
*La cosa che non deve mancare*: la speranza sul viso. È quella che mette a disagio.

**Vatore — il ladro che diventerà Sal**
<!-- img id=ritratto-vatore size=832x1216 stile=ritratto serie=base -->
```
[look comune] + lean man in his forties between two dark tents of a vast night
camp, grey silk clothes of a close dark-elven cut, hood half raised, no
ornaments, cold calculating eyes, clutching a cloth bundle to his chest,
reverent terror badly hidden, looking at something that should not exist
```
*La cosa che non deve mancare*: il fagotto stretto al petto.

---

## §3 · Le sei tavole

Le tavole prendono **solo l'ancora storica** (il look comune dice «waist-up
portrait» e rovinerebbe una veduta), come nel Drappo.

**Il portale del Tempo** *(scheda 22; sostituisce `PortaleDellaForgiaEterna.webp`, che è un'immagine di testo)*
<!-- img id=tavola-portale-del-tempo size=1536x864 stile=tavola serie=base -->
```
epic fantasy matte-painting, a fresco as tall as three men in a frame of gold
and adamantine on the wall of a dark octagonal hall, its liquid-glass surface
showing two scenes at once like a double exposure: a young white-walled
dwarven fortress with a young black dragon diving on it, and the same
fortress centuries older and soot-black under a much larger black dragon, a
vertical oval of gold light pulsing where they overlap, a dwarf seen from
behind wearing a crown with two lit gems and one empty socket, no text
```

**La Custode delle Radici** *(scheda 28 · solo DM fino allo Step 5)*
<!-- img id=tavola-custode-delle-radici size=832x1216 stile=tavola serie=base -->
```
a tall figure shaped like a woman but made of braided dark roots and
lichen-grey rock, two old knots of wood for eyes, standing perfectly still at
the empty southern edge of a glowing ritual circle in a basalt and gold hall,
the gold light thinning around her feet, three small kneeling figures out of
focus, solemn and neutral, a patient official waiting for a signature, no text
```

**Il Cuore di Moradin, il reliquiario che si apre** *(scheda 27 · `serie=extra`: l'immagine esistente `ilCuoreDiMoradin` lo mostra già appoggiato sull'Altare; questa è la versione fedele al testo di `DEF-3` §3)*
<!-- img id=tavola-cuore-di-moradin size=1536x864 stile=tavola serie=extra -->
```
a seamless altar of mithral at the centre of a dark octagonal hall opening
like a metal flower, its petals folding back to reveal a small inner chamber,
and suspended in golden light inside it a crystal of blood-red ruby the size
of a fist carved in the exact shape of a dwarven heart, four chambers and
its vessels visible through the transparent stone, a dwarf's gauntleted hands
resting on the altar's rim, warmth rising from it, no text
```

**Il risveglio di Hella** *(scheda 29 · ai giocatori solo dopo il rito)*
<!-- img id=tavola-risveglio-di-hella size=1536x864 stile=tavola serie=base -->
```
a short stocky broad-shouldered dwarf woman, sturdy dwarven proportions,
lying on a mithral altar at the instant she breathes in again after death, chest lifting, eyes just opened and amber-gold, light wavy
blonde hair with small green leaves and a thin vein of bark, pointed ears
like young leaves, a fist-sized ruby shaped like a heart fading on her
breastbone, thin golden roots running from her hands into the altar, three
armoured figures kneeling at the edge of a ritual circle, a greyhound-like
sighthound of dark porous stone and mithral with topaz eyes waiting at the
altar's edge, long narrow snout, deep narrow chest, thin tucked waist, long
thin legs, not a wolf, no fur, warm gold light from below, no text
```

**Durik e Hella** *(scheda 31 · dopo il risveglio)*
<!-- img id=tavola-durik-e-hella size=832x1216 stile=tavola serie=base -->
```
a large greyhound-like sighthound, long narrow snout, deep narrow chest, thin
tucked waist, long thin legs, not a wolf, no fur, made of dark porous stone
braided with ribbons of mithral along the tendons, topaz eyes half closed,
resting his long head on the chest of a short stocky dwarf woman just
returned from death, sitting up on an altar, one
trembling hand between his ears, her light blonde hair with small leaves,
pointed ears like young leaves, no collar, no mechanical joints, tender and
quiet, warm light from below left, no text
```

**La fortezza giovane** *(scheda 33 · all'arrivo a −1000)*
<!-- img id=tavola-hammerfist-giovane size=1536x864 stile=tavola serie=base -->
```
medieval epic fantasy matte-painting, a young dwarven stronghold carved into
a rocky mountainside at dusk, seen from high on the mountain above its gate,
crenellated walls and square towers of freshly cut pale limestone with sharp
unweathered edges, wooden stonemasons' scaffolding lashed against one tower,
a single king's statue in the courtyard, a freshly engraved bronze plaque of
abstract ornament on the iron-bound gate with bronze shavings beneath it,
below on the right a wide dark valley plain with a besieging camp of hide
tents, hundreds of small orange campfires like embers and thin columns of
grey smoke, low warm sunset, no modern buildings, no city lights, no text
```

**Skullcrusher nel cortile** *(scheda 41 · solo DM fino al duello)*
<!-- img id=tavola-skullcrusher-nel-cortile size=1536x864 stile=tavola serie=base -->
```
a huge lean black dragon landing in the stone courtyard of a young dwarven
fortress at dawn, long neck, narrow horned skull, wings half open from the
dive, matte black scales with an oily green sheen, acid dripping from closed
jaws and smoking on the flagstones, hundreds of dwarves on the walls looking
up, four small figures seen from behind facing him: a dwarf with a crown and a
great axe, a bare-handed dwarf monk with glowing braziers on his wrists, a
caster wreathed in light and shadow, a blonde dwarf woman with a stone hound,
cold grey dawn light, low camera, no text
```

---

## §4 · Prima esecuzione con Canva AI (2026-09-25)

Il DM ha chiesto di provare questi prompt con **Canva AI** invece che con
`comfyui_batch.py`. Sono state generate tutte e quattordici le immagini, una per
blocco `img`, e stanno nella libreria Canva del DM. **I PNG non sono ancora in
questa cartella**: la sessione che le ha generate non raggiungeva `canva.com`
(politica di rete dell'ambiente), quindi non poteva esportarle. Si esportano da
Canva col nome dell'`id` e si committano insieme alla loro riga, che è già in
`PROVENIENZA.txt`.

### Cosa cambia rispetto a ComfyUI

| | ComfyUI (§1-§3) | Canva AI |
|---|---|---|
| Seme | sì, l'immagine si rifà identica | **nessuno**: il file esportato è il sorgente (ADR-0019 §2-bis) |
| Negativi | campo separato | nessun campo: sono scritti in coda al prompt come «no text, no watermark…», e tengono meno |
| Formato | 832 × 1216 e 1536 × 864 | rapporti fissi: **2:3** per i ritratti e per le due tavole verticali, **16:9** per le altre |
| Riferimenti | LoRA / IP-Adapter | immagini di riferimento: per le due tavole di Hella si sono usati `PG/Immagini/web/Hella4.jpg` e `durik2.jpg` |
| Licenza | pesi SDXL, OpenRAIL++-M | termini di servizio Canva; il modello non è dichiarato. Si rileggono prima di pubblicare |

### Come si è composto il prompt

- **Ritratti**: `look comune` + `ancora storica` + soggetto + negativi, in
  quest'ordine, in un solo testo.
- **Tavole**: `ancora storica` + soggetto + negativi, senza il look comune,
  come dice §3.
- **Tavole di Hella**: in più, la richiesta di tenere il volto del primo
  riferimento e il segugio del secondo, **resi a olio e non in 3D**. `Hella4` è
  un render 3D e senza quella riga lo stile del riferimento vince su quello del
  set.
- **Fortezza giovane**: la targa di bronzo chiede «solo ornamento, nessuna
  lettera leggibile», perché senza il campo dei negativi il testo è il rischio
  più alto.

### Le quattordici immagini

La tabella è aggiornata alla seconda passata. La colonna *Prima lettura* è fatta **sulla miniatura** restituita da Canva
(circa 130 × 200 pixel). Non sostituisce il gate di rifiuto di
`rumblingstone-art-direction` §6, che va fatto a piena risoluzione sulla «cosa
che non deve mancare» di ogni scheda.

| id | Media Canva | Prima lettura |
|---|---|---|
| `ritratto-balvar-fuocospento` | [MAHWLw8QnOo](https://www.canva.com/M/MAHWLw8QnOo) | **nel repo** come `ritratti/balvar-fuocospento.jpg`, verificato a 533 × 800: la punta tocca l'ardesia. È la copia ridotta arrivata in chat |
| `ritratto-zogtar-deatheye` | [MAHWL_YsfgQ](https://www.canva.com/M/MAHWL_YsfgQ) | sostituita dalla **terza versione** mandata dal DM (`ritratti/zogtar-deatheye.webp`, 1033 × 1523): pietra nell'occhio destro senza specchiare, ossa naniche alla tenda. Strumento da confermare |
| `ritratto-re-thorek-i` | [MAHWLyU_oPo](https://www.canva.com/M/MAHWLyU_oPo) | **nel repo** come `ritratti/re-thorek-i.jpg`: corona di ferro senza gemme, Frostcleaver in pugno, mappa sul tavolo |
| `ritratto-thorgrim-barbadiferro` | [MAHWMYEg1KY](https://www.canva.com/M/MAHWMYEg1KY) | **nel repo** come `ritratti/thorgrim-barbadiferro.jpg`: guarda in alto la luce, mani vuote a palmi in su, ascia accanto alla panca. Il callo non è un segno a sé, ma il palmo è in piena vista. Rigenerata perché il DM non trovava `MAHWLyX0Wa0`; la prima, con la reliquia, è scartata |
| `ritratto-durin-rocciadura` | [MAHWLxfub5Q](https://www.canva.com/M/MAHWLxfub5Q) | **nel repo** come `ritratti/durin-rocciadura.jpg`: mani strette sull'ascia, scudo blu, torce dietro |
| `ritratto-zeth-mastro-costruttore` | [MAHWLzJWJXI](https://www.canva.com/M/MAHWLzJWJXI) | **nel repo** come `ritratti/zeth-mastro-costruttore.jpg`: gesso in mano, runa sotto il pollice, il leone di pietra dietro |
| `ritratto-vatore` | [MAHWL25-bj4](https://www.canva.com/M/MAHWL25-bj4) | **nel repo** come `ritratti/vatore.jpg`: il fagotto stretto al petto, le tende di notte |
| `tavola-portale-del-tempo` | [MAHWLyz44U8](https://www.canva.com/M/MAHWLyz44U8) | **nel repo** come `tavola-portale-del-tempo.jpg`, in `DEF-4` Scena 1: le due fortezze e i due draghi si leggono, l'ovale d'oro al centro, la Corona con due gemme accese e un incasso vuoto |
| `tavola-custode-delle-radici` | [MAHWL6WcCpw](https://www.canva.com/M/MAHWL6WcCpw) | **nel repo** come `tavola-custode-delle-radici.jpg`, in `DEF-3` §6 |
| `tavola-cuore-di-moradin` | [MAHWLy0nGm4](https://www.canva.com/M/MAHWLy0nGm4) | **nel repo** come `tavola-cuore-di-moradin.jpg` e **scelta al posto di `ilCuoreDiMoradin`** per il §3: il Cuore sta dentro il reliquiario aperto, come dice il box |
| `tavola-risveglio-di-hella` | [MAHWL21y19U](https://www.canva.com/M/MAHWL21y19U) | **nel repo** come `tavola-risveglio-di-hella.jpg`, in `DEF-3` §7 dopo il box del risveglio |
| `tavola-durik-e-hella` | [MAHWL6svafI](https://www.canva.com/M/MAHWL6svafI) | **nel repo** come `tavola-durik-e-hella.jpg`, copertina di `08-SCHEDA-DURIK`. Scelta fra le due versioni: qui Durik è il levriero di `durik2`, nella prima è sdraiato e massiccio |
| `tavola-hammerfist-giovane` | [MAHWLwYjXcE](https://www.canva.com/M/MAHWLwYjXcE) | **nel repo** come `tavola-hammerfist-giovane.jpg`, in `DEF-4` Scena 1. La prima versione (`MAHWL9hrJvc`) è nel repo per la Scena 3: vedi sotto |
| `tavola-skullcrusher-nel-cortile` | [MAHWL-laBHk](https://www.canva.com/M/MAHWL-laBHk) | **nel repo** come `tavola-skullcrusher-nel-cortile.webp`, in `DEF-4`. **Il cane di Hella è sbagliato**: una bestia massiccia di pietra, non il levriero. Tenuta perché è l'unica e si vede di spalle; candidata a una seconda passata |

Il **portale** va ancora verificato a piena risoluzione. Se il DM scarta
un'immagine, il motivo va in `SCARTI.txt` come fa `comfyui_batch.py --reroll`,
e l'immagine si rigenera: con Canva non c'è seme da cambiare, si corregge il
prompt.

### Seconda passata: le cinque scartate

Il DM ha scartato le cinque candidate della prima passata. Ogni motivo è in
`SCARTI.txt`, e la correzione è entrata **nei blocchi di §2 e §3**, perché vale
per qualunque modello e non solo per Canva:

| id | Difetto | Correzione del prompt |
|---|---|---|
| `ritratto-zogtar-deatheye` | la pietra nell'occhio non si vedeva | inquadratura più stretta, luce da sinistra sul volto, occhio sinistro normale e destro di pietra detti entrambi, «no eyepatch» |
| `ritratto-thorgrim-barbadiferro` | teneva la reliquia in mano | mani vuote a palmi in su, lo sguardo verso una luce fuori campo, «he holds nothing» |
| `tavola-risveglio-di-hella` | Durik sembrava un lupo | il levriero descritto per forma (muso lungo, torace stretto, vita sottile), «not a wolf, no fur»; Hella «short, stocky» |
| `tavola-durik-e-hella` | come sopra, e Hella elfa | stesse due correzioni |
| `tavola-hammerfist-giovane` | niente fuochi sulla piana | punto di vista dall'alto sopra la porta, il campo di tende a destra nella valle. La seconda prova, sulla miniatura, sembrava una città moderna; la terza aggiunge «medieval», le merlature e «no modern buildings, no city lights» |

⚠️ **Correzione del 2026-09-25.** Qui c'era scritto che la seconda prova della
fortezza era «una città moderna al tramonto», e che il motivo era la mancanza
dei negativi. **Era sbagliato.** Il giudizio era fatto sulla miniatura di 200 ×
113 pixel; a piena risoluzione (`MAHWL7ajay0`, arrivata dal DM) è una fortezza
medievale fedele al prompt: parapetto bianco, targa, statua, impalcatura, fuochi
sulla piana. Resta scartata, ma per un'altra ragione: è un render 3D
fotografico, e il set è dipinto a olio. La lezione vera è quella del gate di
rifiuto: **un'immagine si scarta a piena risoluzione, mai sulla miniatura.**

### Terza consegna del DM: le tre fortezze e i due risvegli

Il DM ha mandato a piena vista tutte e tre le fortezze e i due risvegli.

| id | Scelta | Perché |
|---|---|---|
| `tavola-risveglio-di-hella` | la **seconda** (`MAHWL21y19U`) | il levriero, gli occhi d'ambra, il rubino sullo sterno, le radici d'oro dalle mani: tutto il box di `DEF-3` §7. La prima ha di nuovo il lupo |
| `tavola-hammerfist-giovane` | la **terza** (`MAHWLwYjXcE`), per la Scena 1 | la fortezza vista da lontano e i fuochi dell'orda sulla piana: è il box «la fortezza, da lontano» |
| `tavola-hammerfist-giovane-porta` | la **prima** (`MAHWL9hrJvc`), ripescata per la Scena 3 | scartata perché mancavano i fuochi, è invece esattamente il box «la porta e la targa»: pietra bianca appena tagliata, una sola statua di re, la targa di bronzo e i trucioli sul selciato |
| — | la seconda (`MAHWL7ajay0`) resta fuori | render 3D fotografico, fuori dall'ancora a olio del set |

---

## §5 · Confronto immagine-scheda

Il passo 4 della procedura di `rumblingstone-art-direction` §7-bis: ogni immagine
tenuta si guarda **a piena vista** accanto alla sua scheda-personaggio
(`PROMPT-IMMAGINI-07ILP.md`) o al box che illustra. Sui tratti del volto vince il
ritratto, e la scheda si allinea; l'arma resta quella dello statblocco. Le
decisioni del DM sono del 2026-09-25 (`plans/STATO-E-ORDINE-DEI-PIANI.md`
§12.1-ter). `validate_corredo.py` boccia un blocco `img` senza la sua riga qui.

| id | Confrontata con | Cosa non coincideva | Esito |
|---|---|---|---|
| `ritratto-balvar-fuocospento` | scheda R5 | la casacca è verde sotto il grembiule, la scheda diceva grigio ardesia | tenuta; vale il ritratto, scheda allineata |
| `ritratto-zogtar-deatheye` | scheda R6 | niente, nella terza versione del DM | tenuta; le prime due scartate (`SCARTI.txt`) |
| `ritratto-re-thorek-i` | scheda R2 | quattro trecce invece di tre | tenuta; vale il ritratto |
| `ritratto-thorgrim-barbadiferro` | scheda R3 e box di `DEF-4` Scena 4 | mani aperte verso la luce, il box le voleva sulle ginocchia | tenuta; corretto il box di `DEF-4` e la scheda d'entrata |
| `ritratto-durin-rocciadura` | scheda R1 e statblocco | barba lunga in una treccia, nessun naso rotto, cappuccio verde; ascia a una lama | tenuta; vale il ritratto sul volto, l'ascia resta doppia come nello statblocco |
| `ritratto-zeth-mastro-costruttore` | scheda R4 | niente | tenuta |
| `ritratto-vatore` | scheda R7 | niente; il volto non si confronta con Sal, che nel repo non ha un'immagine | tenuta |
| `tavola-portale-del-tempo` | box di `DEF-4` Scena 1 | niente sulla miniatura: da riguardare a piena risoluzione (§4) | tenuta, con la verifica aperta |
| `tavola-custode-delle-radici` | box di `DEF-3` §6 | niente | tenuta |
| `tavola-cuore-di-moradin` | box di `DEF-3` §3 | niente: il Cuore sta nel reliquiario aperto, come dice il box | tenuta, al posto di `ilCuoreDiMoradin` |
| `tavola-risveglio-di-hella` | scheda di Hella e di Durik, box di `DEF-3` §7 | niente nella seconda; nella prima Durik era un lupo | tenuta la seconda |
| `tavola-durik-e-hella` | scheda di Hella e di Durik | niente nella seconda; nella prima Durik sdraiato e massiccio, Hella elfa | tenuta la seconda |
| `tavola-hammerfist-giovane` | box di `DEF-4` Scena 1 e Scena 3 | la prima non ha i fuochi, la seconda è un render 3D | tenuta la terza per la Scena 1; la prima ripescata per la Scena 3 come `tavola-hammerfist-giovane-porta` |
| `tavola-skullcrusher-nel-cortile` | scheda di Durik | il cane di Hella è una bestia massiccia di pietra, non il levriero | tenuta con riserva: è l'unica e Durik si vede di spalle; candidata a una seconda passata |
