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

```
painterly digital illustration, crisp ink line underneath, visible brushwork,
three-quarter view, waist-up character sheet portrait, single hero focal point,
simple dark vignette background, warm-cool contrast, dramatic rim lighting,
weathered leather and cloth, muted river-town palette (wet ochre, iron grey,
dyed indigo), late-summer light
```

**Negativi consigliati**: `modern clothing, plastic sheen, glamour, neon, text,
watermark, logo, oversaturated`.

**Formato**: 832 × 1216 (verticale), che è la proporzione giusta per stare in cima a
una scheda stampata.

---

## §2 · I sei ritratti

**Vanna Corsari — il Capitano**
```
[look comune] + woman in her late thirties, weathered face, short dark hair
cut practical, chainmail shirt over a green-and-brown contrada surcoat, heavy
steel shield slung at the back, longsword at the hip, hands scarred by tree
resin, standing square and unsmiling, torchlit crowd blurred behind her
```
*La cosa che non deve mancare*: le mani. Sono rovinate come quelle di tutti nel
rione, e si devono vedere.

**Nocca Pettirosso — il Fantino**
```
[look comune] + halfling man, mid twenties, wiry and very small, barefoot,
studded leather, a coiled leather riding crop over the shoulder, short sword,
grinning sideways at something off-frame, stable straw and horse flank behind him
```
*La cosa che non deve mancare*: i piedi nudi. Non ha mai posseduto una sella.

**Ombra dei Salici — lo Stalliere**
```
[look comune] + woman in her mid forties, grey-streaked braid, plain leather
armor, small wooden shield, herbalist pouches and a sickle at the belt, one
hand resting flat on a horse's neck, calm and unhurried, lantern light from below
```
*La cosa che non deve mancare*: la mano appoggiata sul collo del cavallo, ferma.

**Tesio Marca — il Tenente**
```
[look comune] + man in his early thirties, ink-stained fingers, plain scribe's
coat over travelling clothes, a raven perched on his forearm, rolled land
registers under one arm, light crossbow on the back, looking slightly away from
the viewer as if listening to someone else's conversation
```
*La cosa che non deve mancare*: il corvo, e lo sguardo che non è sul lettore.

**Berenice «Bruma» Sallo — l'Alfiere**
```
[look comune] + half-elf woman, late twenties, masterwork lute across her back,
chainmail shirt under a stage coat, a folded contrada banner on an ash pole in
one hand, mid-song with her mouth open, banners and lamplight behind her
```
*La cosa che non deve mancare*: sta cantando. Non posa: canta.

**Fra' Melchio Vanzi — il Vicario**
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
```
epic fantasy matte-painting, high three-quarter aerial view of a medieval
river-town square, a wide ring of packed earth around a large covered grain
market at the centre, eight coloured banners on the outer galleries, dense
crowd pressed against wooden barriers, eight bareback riders mid-turn, dust,
late-summer golden hour, atmospheric perspective, no text
```

**Tavola 2 — la Cena della vigilia** *(handout del Giorno 2)*
```
warm night scene, narrow alley filled end to end with long trestle tables,
eighty townsfolk eating under strung banners, resin lamps, a horse being led
between the tables, painterly illustration, deep shadows, glowing lamp light,
intimate rather than epic, no text
```

**Tavola 3 — le stalle, dopo mezzanotte** *(handout del Giorno 2, §6)*
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
documenti li trovano:

```
ritratto-vanna.png · ritratto-nocca.png · ritratto-ombra.png
ritratto-tesio.png · ritratto-berenice.png · ritratto-melchio.png
tavola-la-ruota.png · tavola-la-cena.png · tavola-le-stalle.png
il-drappo.png
```

⚠️ **Prima di condividere o stampare fuori dal tavolo**: annota in
`PROVENIENZA.txt` con che modello e che prompt è stata generata ogni immagine.
È la lacuna che il rapporto IP della campagna aveva già segnalato per le tavole
dell'arco di Channathgate (§7.7): qui si evita partendo, non si rincorre dopo.
