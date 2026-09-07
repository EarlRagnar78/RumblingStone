# Immagini del modulo — direzione artistica e prompt

**Cosa c'è già, generato e committato:**

| Immagine | Dove | Come si rifà |
|---|---|---|
| I due tavoli tattici (la Ruota, le stalle) | `../mappe/rendered/*.svg` | `compile_map_json.py` → `render_map_svg.py` |
| Gli otto stemmi di contrada | serie Golarion, vedi `../../CONTRADE-DI-TARSILIA.md` §7 | `build_golarion_shields.py` |

**Cosa manca e va prodotto dal DM**: i **sei ritratti** e le **tre tavole
d'atmosfera**. Il repo non genera raster: genera vettoriale e *istruzioni*. Questi
prompt sono per l'infrastruttura ComfyUI locale (`scripts/comfyui-local/README.md`);
funzionano uguale su qualsiasi altro generatore.

> ⚖️ **Regola IP del repo** (`references/stile-illustrazione-handout.md`): si
> descrivono le **convenzioni** del look — posa, luce, tecnica — **mai** il nome di
> un illustratore vivente, mai «in the style of», mai tavole altrui come reference.
> Lo stile come categoria è libero; la firma di una persona no.

---

## §1 · Il look comune ai sei ritratti

Blocco da anteporre a ogni prompt, così le sei schede sembrano una serie sola:

<!-- blocco id=look-comune -->
```
painterly digital illustration, crisp ink line underneath, visible brushwork,
three-quarter view, waist-up character sheet portrait, single hero focal point,
simple dark vignette background, warm-cool contrast, dramatic rim lighting,
weathered leather and cloth, muted river-town palette (wet ochre, iron grey,
dyed indigo), late-summer light
```

**Negativi consigliati** — valgono per tutta la serie, ritratti e tavole:

<!-- blocco id=negativi -->
```
modern clothing, plastic sheen, glamour, neon, text, watermark, logo,
oversaturated
```

**L'ancora storica — il pezzo che tiene insieme la serie.** Il blocco qui sopra
descrive il look; quello che fa somigliare fra loro **dieci immagini generate in
sessioni diverse** è aggiungere una **scuola pittorica in pubblico dominio**, che è
una categoria storica e non la firma di nessuno (vedi
`stile-illustrazione-handout.md`, §«L'ancora che invece si può usare»). Per Tarsilia:

<!-- blocco id=ancora-storica -->
```
northern renaissance oil glazing, flemish panel painting light,
egg-tempera restraint in the flesh tones
```

Fissa in un colpo solo palette, resa della luce, trattamento delle mani e profondità
di campo — sono un pacchetto storico, non scelte indipendenti.

> ⚠️ **Non** ancorare a «pittura senese», per quanto calzi: il modulo si sta
> allontanando da Siena per ragioni di diritto (`IP-E-LICENZE.md` §4), e rimetterla
> nella direzione artistica la farebbe rientrare dalla finestra. Si sceglie la
> **tecnica**, non la provincia.

**Formato**: 832 × 1216 (verticale), che è la proporzione giusta per stare in cima a
una scheda stampata.

### §1-bis · Le annotazioni che rendono questo file eseguibile

Sopra ogni blocco di prompt c'è **una riga di commento HTML**. Non si vede quando
il markdown viene reso, non entra nei booklet, e serve a
[`scripts/comfyui_batch.py`](../../../scripts/comfyui_batch.py) per generare la
serie da qui invece che a mano:

```
<!-- img id=<nome-file-senza-estensione> size=<L>x<A> stile=ritratto|tavola serie=base|extra [seed=<n>] -->
```

| Campo | Cosa fa |
|---|---|
| `id` | è **anche** il nome del file prodotto (`<id>.png`) e la chiave in `PROVENIENZA.txt` |
| `size` | la risoluzione, presa da questo file e non dallo script |
| `stile` | `ritratto` antepone **look comune + ancora storica**; `tavola` antepone la **sola ancora** (il look comune dice «waist-up portrait» e rovinerebbe una veduta) |
| `serie` | `base` = i **diciotto** del capitolato; `extra` = oltre il capitolato, si generano solo con `--serie tutto` |
| `seed` | **assente finché non hai scelto**. Lo script ne deriva uno stabile dall'`id`; quando una generazione ti convince, `--fissa-seed` lo scrive qui e da quel momento l'immagine è **rifacibile** |

Il markdown resta il master (ADR-0003): il prompt si corregge **qui**, non nello
script.

---

## §2 · I sei ritratti

**Vanna Corsari — il Capitano**
<!-- img id=ritratto-vanna size=832x1216 stile=ritratto serie=base -->
```
[look comune] + woman in her late thirties, weathered face, short dark hair
cut practical, chainmail shirt over a green-and-brown contrada surcoat, heavy
steel shield slung at the back, longsword at the hip, hands scarred by tree
resin, standing square and unsmiling, torchlit crowd blurred behind her
```
*La cosa che non deve mancare*: le mani. Sono rovinate come quelle di tutti nel
rione, e si devono vedere.

**Nocca Pettirosso — il Fantino**
<!-- img id=ritratto-nocca size=832x1216 stile=ritratto serie=base -->
```
[look comune] + halfling man, mid twenties, wiry and very small, barefoot,
studded leather, a coiled leather riding crop over the shoulder, short sword,
grinning sideways at something off-frame, stable straw and horse flank behind him
```
*La cosa che non deve mancare*: i piedi nudi. Non ha mai posseduto una sella.

**Ombra dei Salici — lo Stalliere**
<!-- img id=ritratto-ombra size=832x1216 stile=ritratto serie=base -->
```
[look comune] + woman in her mid forties, grey-streaked braid, plain leather
armor, small wooden shield, herbalist pouches and a sickle at the belt, one
hand resting flat on a horse's neck, calm and unhurried, lantern light from below
```
*La cosa che non deve mancare*: la mano appoggiata sul collo del cavallo, ferma.

**Tesio Marca — il Tenente**
<!-- img id=ritratto-tesio size=832x1216 stile=ritratto serie=base -->
```
[look comune] + man in his early thirties, ink-stained fingers, plain scribe's
coat over travelling clothes, a raven perched on his forearm, rolled land
registers under one arm, light crossbow on the back, looking slightly away from
the viewer as if listening to someone else's conversation
```
*La cosa che non deve mancare*: il corvo, e lo sguardo che non è sul lettore.

**Berenice «Bruma» Sallo — l'Alfiere**
<!-- img id=ritratto-berenice size=832x1216 stile=ritratto serie=base -->
```
[look comune] + half-elf woman, late twenties, masterwork lute across her back,
chainmail shirt under a stage coat, a folded contrada banner on an ash pole in
one hand, mid-song with her mouth open, banners and lamplight behind her
```
*La cosa che non deve mancare*: sta cantando. Non posa: canta.

**Fra' Melchio Vanzi — il Vicario**
<!-- img id=ritratto-melchio size=832x1216 stile=ritratto serie=base -->
```
[look comune] + man in his early fifties, tonsured grey hair, worn habit over a
mail shirt, silver holy symbol of a stylised sun-and-ankh, a scimitar at the belt
he clearly does not enjoy carrying, an open ledger held against his chest,
tired steady eyes, almshouse cots blurred behind him
```
*La cosa che non deve mancare*: il registro tenuto contro il petto.

---

## §3 · Le tre tavole d'atmosfera

**Tavola 1 — la Ruota, il giorno della corsa** *(copertina del modulo)*
<!-- img id=tavola-la-ruota size=1536x864 stile=tavola serie=base -->
```
epic fantasy matte-painting, high three-quarter aerial view of a medieval
river-town square, a wide ring of packed earth around a large covered grain
market at the centre, eight coloured banners on the outer galleries, dense
crowd pressed against wooden barriers, eight bareback riders mid-turn, dust,
late-summer golden hour, atmospheric perspective, no text
```

**Tavola 2 — la Cena della vigilia** *(handout del Giorno 2)*
<!-- img id=tavola-la-cena size=1536x864 stile=tavola serie=base -->
```
warm night scene, narrow alley filled end to end with long trestle tables,
eighty townsfolk eating under strung banners, resin lamps, a horse being led
between the tables, painterly illustration, deep shadows, glowing lamp light,
intimate rather than epic, no text
```

**Tavola 3 — le stalle, dopo mezzanotte** *(handout del Giorno 2, §6)*
<!-- img id=tavola-le-stalle size=1536x864 stile=tavola serie=base -->
```
tense night interior of a timber stable, hayloft above, lantern on a post, a
horse rearing in its box, four armed men silhouetted in a doorway, dry straw
across the floor, hard rim light and deep darkness, painterly illustration,
no text
```

---

## §4 · Il Drappo

Il telo dipinto è **un oggetto di trama**, non decorazione: al Giorno 3 §8 i
giocatori devono poter **guardare il fondo a destra** e trovarci nove facce.
Se produci una sola immagine di questo modulo, produci questa.

<!-- img id=il-drappo size=832x1216 stile=tavola serie=base -->
```
tall narrow painted cloth banner, vertical composition, a horse race around a
town square in the foreground painted in a naive votive style, and in the lower
right corner a crowd of nine individual faces painted with unusual care and
portrait detail, aged pigment on linen, visible weave, painterly, no text
```

> **Come si usa al tavolo**: stampala, e non dire niente. Se nessuno guarda in
> fondo a destra, la scoperta arriva più tardi — e arriva meglio.

---

## §5 · Dove si mettono i file

Salva i PNG in questa cartella con questi nomi esatti, così i riferimenti dei
documenti li trovano. I nomi **non si scelgono qui**: sono gli `id` delle
annotazioni §1-bis, e `comfyui_batch.py` li scrive già così.

**I diciotto del capitolato** (`serie=base`):

```
ritratto-vanna.png · ritratto-nocca.png · ritratto-ombra.png
ritratto-tesio.png · ritratto-berenice.png · ritratto-melchio.png     ← i 6 PG
ritratto-vesca.png · ritratto-attu.png · ritratto-roncetti.png
ritratto-sfregio.png · ritratto-grasa.png                             ← i 5 PNG
tavola-la-ruota.png · tavola-la-cena.png · tavola-le-stalle.png       ← le 3 tavole
il-drappo.png · copertina.png
spot-bilancia.png · spot-registro.png                                 ← i 2 spot
```

**Oltre il capitolato** (`serie=extra`, §8 — si generano solo se li chiedi):

```
tavola-tarsilia-dallalto.png · tavola-la-ruota-vigilia.png
```

⚠️ **Prima di condividere o stampare fuori dal tavolo**: annota in
`PROVENIENZA.txt` con che modello e che prompt è stata generata ogni immagine.
È la lacuna che il rapporto IP della campagna aveva già segnalato per le tavole
dell'arco di Channathgate (§7.7): qui si evita partendo, non si rincorre dopo.
Con `comfyui_batch.py` la riga la scrive lo script (ADR-0019 §2), e senza quella
riga l'immagine non si committa.

---

## §6 · I cinque PNG che meritano un ritratto

Tutti col blocco del §1 **e l'ancora storica**, formato **832 × 1216**. I tratti
vengono dal foglio del cast (`08-CASSETTA-DEL-DM.md` §1): non inventarne di nuovi,
è la scheda-personaggio della skill `rumblingstone-art-direction` §3.

### 6.1 · Ottavia Vesca — Capitana del Bruco

<!-- img id=ritratto-vesca size=832x1216 stile=ritratto serie=base -->
```
a fifty-year-old woman, dyer's hands stained blue-black to the elbow, close-set
watchful eyes, grey hair pulled back hard, plain indigo work dress with a
guild collar, standing in a dye-house doorway, one hand still wet,
speaks-before-you-finish expression
```
*Colore suo*: **indaco**. *Segno*: le mani macchiate, sempre visibili.

### 6.2 · Gerlando Attu — Capitano dell'Oca

<!-- img id=ritratto-attu size=832x1216 stile=ritratto serie=base -->
```
a forty-two-year-old man, banker's build, dressed exactly half a grade below
what he could afford, close-trimmed beard, a ledger strap across his chest,
counting-house shelves behind him, faint smile that does not reach the eyes
```
*Colore suo*: **marmo e lapis**. *Segno*: la cinghia del registro.

### 6.3 · Vidalia Roncetti — Sovrintendente al Drappo

<!-- img id=ritratto-roncetti size=832x1216 stile=ritratto serie=base -->
```
a magistrate in her sixties, ceremonial sash over sober robes, reading glasses
held not worn, a rolled decree in one hand, standing under a public portico,
the face of someone who has read the article aloud a hundred times
```
*Colore suo*: **grigio ferro e oro spento**. *Segno*: il decreto arrotolato.

### 6.4 · Sfregio — il sicario del Bruco

<!-- img id=ritratto-sfregio size=832x1216 stile=ritratto serie=base -->
```
a wiry man in his thirties, old blade scar from cheekbone to jaw, hood down,
hands relaxed and empty, leaning in a canal alley at dusk, unremarkable
clothes chosen to be forgotten, calm and entirely present
```
*Colore suo*: **nessuno — grigio sporco**. *Segno*: la cicatrice. ⚠️ Niente arma in
vista: la minaccia sta nella calma, non nel coltello.

### 6.5 · Nonna Grasa — l'ospizio dell'Istrice

<!-- img id=ritratto-grasa size=832x1216 stile=ritratto serie=base -->
```
a seventy-one-year-old woman, broad and short, apron over layers, hands folded
over a tally stick, seated by a hospice hearth with beds behind her,
kind face that is also doing arithmetic
```
*Colore suo*: **bruno di terra**. *Segno*: il bastoncino dei conti.

---

## §7 · La copertina e i due spot

### 7.1 · Copertina — 832 × 1216

<!-- img id=copertina size=832x1216 stile=tavola serie=base -->
```
the painted cloth prize hanging above a crowded square at dusk, seen from below,
banners of eight quarters along the rooftops, dust and low sun, no faces
readable, the cloth is the hero of the image
```

### 7.2 · Spot — la bilancia dell'Oca · 800 × 800

<!-- img id=spot-bilancia size=800x800 stile=tavola serie=base -->
```
a public weighing scale of dark iron in a market portico, one pan heaped with
raw resin, the other with counterweights, close crop, morning light
```

### 7.3 · Spot — la pagina del registro · 800 × 800

<!-- img id=spot-registro size=800x800 stile=tavola serie=base -->
```
an open parish register on a wooden lectern, nine names in the same hand in the
right-hand column, candle stub, close crop, no readable text
```

---

## §8 · La città e la piazza — il patto valido anche per Channathgate

Queste due sono le uniche **tavole d'ambiente larghe** (1536 × 864) e seguono un
**patto d'inquadratura** che vale anche per l'illustrazione della piazza di
Channathgate (`09_.../P2D-Palio-Allegati/`), così le due città della stessa
famiglia di materiale si somigliano senza essere la stessa città.

**Il patto, in quattro regole:**

1. **punto di vista alto ma non a volo d'uccello** — da un tetto o da una loggia,
   l'altezza da cui un abitante guarderebbe davvero;
2. **la piazza è vuota al centro e piena ai bordi** — la corsa non è ancora
   cominciata, e il vuoto in mezzo è la promessa;
3. **nessun volto leggibile**: la folla è tessuto e colore, non ritratti;
4. **un solo elemento verticale domina** — il Drappo a Tarsilia, il campanile a
   Channathgate. È la cosa che l'occhio trova per prima e che distingue le due
   città l'una dall'altra.

### 8.1 · Tarsilia dall'alto — 1536 × 864

<!-- img id=tavola-tarsilia-dallalto size=1536x864 stile=tavola serie=extra -->
```
a river town seen from a rooftop at late afternoon, tiled roofs stepping down to
a canal and a wooden bridge, a rectangular market ring at the centre with a
covered market inside it, eight banners on the surrounding roofs, hills of thorn
scrub beyond, no readable faces, warm dust in the air
```

### 8.2 · La Ruota, il giorno prima — 1536 × 864

<!-- img id=tavola-la-ruota-vigilia size=1536x864 stile=tavola serie=extra -->
```
a rectangular racing ring around a covered market, sand freshly laid, wooden
barriers along the north curve, empty in the middle and crowded at the edges,
the painted cloth prize hoisted on a pole above the south side, late summer
light, no readable faces
```

> **Per Channathgate**: stesso patto, stesso formato, **piazza diversa** — geometria
> a conchiglia invece che ad anello, campanile al posto del Drappo, pietra chiara
> invece di intonaco ocra. Il patto tiene insieme la famiglia; i quattro dettagli la
> distinguono.
