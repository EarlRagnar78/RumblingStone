# Immagini della serata del 30/11 — il rito, il Rubino, il salto

**Cos'è.** Le tre tavole della serata del 2026-11-30, chieste da Jfs il
2026-11-27: il rito della Forgia Eterna e il Rubino che si accende
(`ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`, Scene 12 e 13), e il salto verso
l'ARC-08 (`ARC07-DEF-5-RITORNO-HAMMERFIST.md` §3, Scena 1). Il formato e lo
stile sono quelli del Drappo di Tarsilia
(`10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`)
e di `PROMPT-RITRATTI-E-TAVOLE-ARC07.md`, perché le tavole devono sembrare
della stessa mano di quelle già nel volume.

Ogni tavola ha **due versioni** da confrontare:

| Versione | Regola | Perché |
|---|---|---|
| **A** | nessun volto dei PG si legge: la Corona, l'incudine, le mani, la luce, le sagome di spalle | regge anche se il modello sbaglia le facce, e non fissa un volto che i giocatori hanno in testa diverso |
| **B** | i PG si riconoscono, con le schede di §2 copiate dai riferimenti del repo | il tavolo si vede dentro la scena |

I file dei casi per FLUX stanno accanto a questo:
`CASI-FLUX-SERATA-2026-11-30.json` (prompt composti, seme, negativi, segni da
misurare e, per le B con immagine guida, la ricetta del foglio di riferimento).
Il testo da dare al modello sta **qui**, ed è la copia che vale: il JSON si
rigenera da questo file, non si corregge a mano.

> ⚖️ **Regola IP del repo**: si descrivono le convenzioni del look, mai il nome
> di un illustratore vivente, mai «in the style of». L'ancora è una scuola
> pittorica in pubblico dominio. Nei prompt non c'è il nome di nessuna persona
> reale: Thorik, Tordek, Hella e Artemis sono i nomi dei personaggi.

> 🔒 **Le immagini dei PG non escono dal progetto.** I riferimenti di
> `PG/Immagini/` si usano solo in locale (FLUX in CPU, foglio di guida
> costruito nel container). Su Canva vanno solo prompt di testo, e le tavole B
> entrano, se Jfs le sceglie, sul ramo `campaign-group-rumblingstone` e non su
> `main`; le A possono andare su `main`.

---

## §1 · Ancora, negativi e lock tecnici

Le tavole prendono **solo l'ancora storica**, come nel Drappo e nell'ARC-07: il
look comune dice «waist-up portrait» e rovinerebbe una veduta.

<!-- blocco id=ancora-storica -->
```
northern renaissance oil glazing, flemish panel painting light,
egg-tempera restraint in the flesh tones
```

<!-- blocco id=negativi -->
```
modern clothing, plastic sheen, glamour, neon, text, letters, runes,
watermark, logo, oversaturated, 3D render, photograph
```

Su Canva i negativi non hanno un campo: vanno in coda al prompt come «no text,
no letters, no readable runes, no watermark…». Con FLUX.2 [klein] a cfg 1 il
ramo negativo non viene calcolato (lo dice `scripts/comfyui_batch.py`,
`workflow_flux2`): i negativi entrano nel grafo e non cambiano l'immagine, e
il divieto di testo deve stare anche nel positivo.

**I lock** (`rumblingstone-art-direction` §4), uguali per le tre tavole:

| Lock | Valore | Nota |
|---|---|---|
| Seme | `tavola-rito-forgia-eterna` 372012 · `tavola-rubino-acceso` 372013 · `tavola-salto-sei-gemme` 1372001; **stesso seme per A e B** della stessa tavola | così il confronto A/B cambia il prompt e non il caso. Canva non espone il seme: lì il file è il sorgente (ADR-0019 §2-bis) |
| Luce | grigia e fredda dall'alto a sinistra, la luce del mattino dopo la battaglia; **il rosso del Rubino è l'unica fonte calda** | il rito si fa dopo il duello (Scena 12, «dopo il combattimento»), che si chiude all'alba; nella tavola 3 il grigio è il cielo del passaggio e il rosso è la corrente |
| Camera | leggermente sopra l'altezza degli occhi nelle tavole 1 e 2; **alta**, verso il basso, nella 3 | la 3 deve far vedere la fortezza sotto |
| Formato | 1536 × 864; su Canva `LANDSCAPE_16_9` | come le tavole larghe dell'ARC-07 |

### §1-bis · Le annotazioni

Le righe `<!-- img id=… -->` sono le stesse del Drappo e le legge
`scripts/comfyui_batch.py`: `stile=tavola` antepone l'ancora, `size` è la
risoluzione. Qui `seed` c'è già, contro l'uso del Drappo, perché A e B
della stessa tavola devono partire dallo stesso rumore: senza, lo script ne
ricava uno diverso dall'`id` e il confronto cambierebbe due cose insieme. Le varianti con
l'immagine guida non hanno l'annotazione, perché `comfyui_batch.py` non carica
immagini: girano dal JSON dei casi (§5).

---

## §2 · Le schede-personaggio delle versioni B

Cinque righe a testa, nel modello di `rumblingstone-art-direction` §3, prese dai
riferimenti del repo e non inventate. Nei prompt sono copiate parola per
parola. Fonti: i ritratti di `PG/Immagini/` (`Thorick.webp`, `Tordeck.webp`,
`Hella.webp`, `Artemis.webp`, `durik2.png`), gli oggetti di
`PG/Artefatti/Artefatti-Pg/` (la Corona con le gemme attive, i Bracieri
completi, la Collana, l'Anello riforgiato), le schede di
`campaign/ai-media-prompts/11_PG_E_VILLAIN_PROMPTS.md` §2 e i prompt di Hella
e Durik già usati in `PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §3.

```
THORIK — nano dello scudo, anziano · largo e pesante
VOLTO      viso segnato dalle battaglie, sguardo fermo
CAPELLI    barba grigia lunga
INDOSSA    armatura piena d'acciaio scuro con una gemma blu sul pettorale,
           mantello ROSSO RUGGINE
SEGNO      la Corona di Adamantio; Aegis Fang, ascia nanica a doppia mezzaluna con rune
```
```
TORDEK — nano adulto · compatto, molto muscoloso
VOLTO      cipiglio feroce
CAPELLI    testa rasata, barba nera folta
INDOSSA    veste da monaco ARANCIO ZAFFERANO con fascia scura, braccia nude
SEGNO      i Bracieri Gemelli: due guanti d'acciaio, il sinistro a fuoco verde,
           il destro a fuoco rosso-arancio
```
```
HELLA — nana, risorta · bassa, tarchiata, spalle larghe
VOLTO      occhi ambra e oro, orecchie a punta come foglie giovani
CAPELLI    biondi chiari, mossi, con piccole foglie verdi
INDOSSA    armatura di pietra grigia crepata e foglie di quercia, VERDE MUSCHIO
SEGNO      la Collana dei Semi Eterni; un tenue bagliore di rubino a forma di cuore
           sullo sterno; Durik accanto
```
```
DURIK — levriero di pietra
           muso lungo e stretto, torace profondo e stretto, vita sottile,
           zampe lunghe, non un lupo, niente pelo; pietra scura e porosa con
           nastri di mithral lungo i tendini, occhi di topazio
```
```
ARTEMIS — umano adulto · snello
VOLTO      mezzo sorriso furbo
CAPELLI    scuri, spettinati
INDOSSA    lungo cappotto NERO, grandi ali nere piumate
SEGNO      l'Anello dell'Illuminazione Caotica alla mano sinistra:
           anello nero con pietra viola, scintille bianco-azzurre
```

**Lo stato di oggi**, dai master: la Corona ha **Topazio e Smeraldo accesi** e
il terzo incasso vuoto finché il Rubino non entra (Scena 12, Momento 1); dopo,
**tre gemme** (Scena 13, «Corona ora a 3 gemme accese»). Hella è risorta
(`ARC07-DEF-3` §7) con Durik levriero di pietra.

**Dove la fonte manca o si contraddice** (marcature di
`docs/reference/GUIDA-MARCATURE.md`):

- `[INFERRED — Domanda: la Corona è d'argento o d'oro? Base: l'oggetto in
  PG/Artefatti/…/corona-di-adamantio-e-gemme-attive.webp è argento-adamantio
  con le gemme gialla, verde e rossa; il ritratto Thorick.webp e
  11_PG_E_VILLAIN_PROMPTS.md la fanno d'oro. Scelto l'argento dell'oggetto,
  perché è l'artefatto e il nome dice adamantio.]` Le gemme «yellow, purple,
  blue» di `11_PG_E_VILLAIN_PROMPTS.md` §2.1 sono superate dai master
  (Topazio, Smeraldo, Rubino) e non si usano.
- `[INFERRED — Domanda: la Collana è il ciondolo a ghianda del ritratto o il
  torque di radici con i semi verdi dell'oggetto? Base: Hella.webp contro
  collana-dei-semi-eterni.jpg. Scelto l'oggetto.]`
- `[INFERRED — Domanda: il rubino sullo sterno di Hella resta dopo il rito?
  Base: il box del risveglio (ARC07-DEF-3 §7) lo fa svanire; la richiesta del
  27/11 lo dà come stato di oggi. Tenuto, ma «faint».]`
- `[INFERRED — Domanda: Durik attraversa il salto con Hella? Base: nessun box
  di DEF-5 Scena 1 né del ponte lo nomina. Lasciato fuori dalla tavola 3.]`
- `[INFERRED — Domanda: Aegis Fang ha una o due lame? Base: nessuna immagine
  dell'ascia nel repo (immagini-artefatti.json, «mancanti»); il ritratto e
  11_PG la fanno a doppia mezzaluna. Tenuta la doppia.]`
- `[INFERRED — Domanda: l'anello è viola o nero? Base: l'Anello riforgiato
  in PG/Artefatti è a pietra viola; il ritratto Artemis.webp lo mostra scuro
  con fulmini bianco-azzurri. Scelta la pietra viola con le scintille.]`

---

## §3 · Le tre tavole

### 3.1 · Il rito della Forgia Eterna (DEF-4, Scena 12)

**Funzione** (§5 della skill): mostra una relazione, cioè ottocento nani feriti
che arretrano davanti a una pietra che nessuno ha portato. Il testo dice «nessuno
spiega niente»; l'immagine fa vedere il passo indietro.
**Quando si mostra**: dopo il box «l'incudine, e l'incasso che si chiude», mai
prima: la pietra che compare è il colpo della scena.
**La cosa che non deve mancare**: la pietra rossa piccola sul ferro nudo, e
nessuna mano che la tocca.

<!-- img id=tavola-rito-forgia-eterna-A size=1536x864 stile=tavola serie=base seed=372012 -->
```
wide stone courtyard of a young dwarven fortress with freshly cut pale walls,
on a grey morning after a battle; at the centre an ancient iron anvil used as
an altar, its face scarred by countless hammer blows, and on the bare iron a
single red stone the size of a walnut, glowing hot as if just out of the fire,
nobody touching it; hundreds of wounded dwarves in battered armour and
bandages around it, the nearest ones taking one step back; in the foreground,
seen from behind so that his face is not visible, a broad dwarf in dark plate
and a rust-red cloak wearing a silver-grey adamantine crown with short spikes
and engraved abstract knotwork, a yellow topaz and a green emerald lit in it
and a third socket, the empty third socket catching a red reflection; every
face turned away or in shadow, no face readable; cool grey morning daylight
from the upper left as the single daylight source, the red of the ruby the
only warm light; camera slightly above eye level; solemn, silent, smoke and
dust
```

<!-- img id=tavola-rito-forgia-eterna-B size=1536x864 stile=tavola serie=base seed=372012 -->
```
wide stone courtyard of a young dwarven fortress with freshly cut pale walls,
on a grey morning after a battle; at the centre an ancient iron anvil used as
an altar, its face scarred by countless hammer blows, and on the bare iron a
single red stone the size of a walnut, glowing hot, nobody touching it; behind
the anvil, facing the viewer in three-quarter view, Thorik, an older shield
dwarf, broad and heavy, weathered battle-scarred face, long grey beard, heavy
dark steel full plate with a blue gem in the breastplate and a rust-red cloak,
wearing the adamantine crown, a double-crescent runic dwarven waraxe in his
hand, the crown being a silver-grey adamantine crown with short spikes and
engraved abstract knotwork, a yellow topaz and a green emerald lit in it and a
third socket; at his left Tordek, an adult dwarf, compact and very muscular,
fierce frown, shaved bald head and a thick black beard, a saffron-orange monk
robe with a dark sash and bare arms, on his hands two heavy steel gauntlets,
the left burning with green fire, the right with orange-red forge fire; at his
right Hella, a short stocky broad-shouldered dwarf woman, sturdy dwarven
proportions, amber-gold eyes, light wavy blonde hair with small green leaves,
pointed ears like young leaves, armour of cracked grey stone and overlapping
green oak leaves, a necklace of braided roots set with green seed-stones, a
faint heart-shaped ruby glow on her breastbone, beside her a greyhound-like
sighthound, long narrow snout, deep narrow chest, thin tucked waist, long thin
legs, not a wolf, no fur, made of dark porous stone braided with ribbons of
mithral along the tendons, topaz eyes; a step apart Artemis, a slender human
man, sly half-smile, dark messy hair, a long black coat, large black feathered
wings folded behind him, on his left hand a black ring with a violet stone
crackling with small white-blue sparks; behind them an ancient dwarf king with
a very long white beard in four braids, a dark blue cloak and a plain iron
crown with no gems and wounded dwarves stepping back; cool grey morning
daylight from the upper left as the single daylight source, the red of the
ruby the only warm light; camera slightly above eye level; solemn, silent,
smoke and dust
```

### 3.2 · Il Rubino acceso (DEF-4, Scena 13)

**Funzione**: dice un tono, la profezia compiuta, con il gesto che il box
mette a margine: un nano vicino alla forgia si toglie l'elmo e non sa perché.
**Quando si mostra**: dopo il box «3 di 3: la voce». Moradin non si vede: la
voce «è nei denti», e una faccia nel cielo la tradirebbe.
**La cosa che non deve mancare**: il fuoco rosso e oro esce dalla Corona, non
dall'incudine.

<!-- img id=tavola-rubino-acceso-A size=1536x864 stile=tavola serie=base seed=372013 -->
```
the stone courtyard of a young dwarven fortress at the end of a battle; a
dwarf seen from behind and slightly below, standing at an ancient iron anvil,
and from the front of his silver adamantine crown a red-and-gold fire blazes
upward like a forge flame that does not burn, the crown holding three gems,
yellow, green and a blazing red one; three companions beside him only as dark
silhouettes against the glow, faces not visible; in the foreground near a
forge a dwarf soldier slowly takes off his helmet, his face turned away;
beyond the pale walls, far below on the plain, the enemy horde scattering like
sand; dust and embers rising and pulling upward as if the light began to draw
everything toward the sky; cool grey morning daylight from the upper left as
the single daylight source, the red of the ruby the only warm light; camera
slightly above eye level; no god, no giant face in the sky
```

<!-- img id=tavola-rubino-acceso-B size=1536x864 stile=tavola serie=base seed=372013 -->
```
the stone courtyard of a young dwarven fortress at the end of a battle; at an
ancient iron anvil, facing the viewer, Thorik, an older shield dwarf, broad
and heavy, weathered battle-scarred face, long grey beard, heavy dark steel
full plate with a blue gem in the breastplate and a rust-red cloak, wearing
the adamantine crown, a double-crescent runic dwarven waraxe in his hand, eyes
closed, and from the front of his crown a red-and-gold fire blazes upward like
a forge flame that does not burn, the crown holding three gems, yellow, green
and a blazing red one; around him in the red light, their feet just leaving
the ground, Tordek, an adult dwarf, compact and very muscular, fierce frown,
shaved bald head and a thick black beard, a saffron-orange monk robe with a
dark sash and bare arms, on his hands two heavy steel gauntlets, the left
burning with green fire, the right with orange-red forge fire; Hella, a short
stocky broad-shouldered dwarf woman, sturdy dwarven proportions, amber-gold
eyes, light wavy blonde hair with small green leaves, pointed ears like young
leaves, armour of cracked grey stone and overlapping green oak leaves, a
necklace of braided roots set with green seed-stones, a faint heart-shaped
ruby glow on her breastbone, beside her a greyhound-like sighthound, long
narrow snout, deep narrow chest, thin tucked waist, long thin legs, not a
wolf, no fur, made of dark porous stone braided with ribbons of mithral along
the tendons, topaz eyes; Artemis, a slender human man, sly half-smile, dark
messy hair, a long black coat, large black feathered wings folded behind him,
on his left hand a black ring with a violet stone crackling with small
white-blue sparks; in the foreground near a forge a dwarf soldier slowly takes
off his helmet; beyond the pale walls the enemy horde scattering like sand on
the plain; cool grey morning daylight from the upper left as the single
daylight source, the red of the ruby the only warm light; camera slightly
above eye level; no god, no giant face in the sky
```

### 3.3 · Il salto delle sei gemme (DEF-5 §3, Scena 1, e il ponte verso l'ARC-08)

**Funzione**: dà al DM un appiglio da descrivere, la fortezza che cresce sotto
di loro e il fuoco del Rubino che si apre in sei.
**Direzione visiva**: la direzione di Jfs del 25/11 sul ponte (luce rossa che
strappa anima e corpo attraverso le ere, dal 372 al 1372 DR, sei fasci, sei
gemme), letta nei testi del ponte fuori dal repo e qui non copiata.
`[INFERRED — Domanda: vale il verso in avanti del ponte o il box di DEF-5
Scena 1, che riavvolge la battaglia? Base: il box del master va all'indietro
(«le cose accadono al contrario»), la direzione del 25/11 in avanti. La tavola
segue la direzione del 25/11; se resta il box del master, va rifatta.]`
**Quando si mostra**: dopo l'ultimo box della caduta, quando le pietre sono già
sul tavolo.
**Il segreto**: in fondo ai fasci ci sono **solo le gemme**. Nessun nano, nessun
luogo, nessun indizio di chi le aspetta: l'abbinamento gemma-nano è solo del DM.
**La cosa che non deve mancare**: sei fasci di sei colori, a distanza uguale,
ognuno chiuso da una gemma piccola e dura (bianca, azzurra, viola, rame, grigio
fumo, bruna: i colori delle pietre del tavolo).

<!-- img id=tavola-salto-sei-gemme-A size=1536x864 stile=tavola serie=base seed=1372001 -->
```
an immense stream of red light carrying four small dark figures, seen from
behind and far away, through a sky where day and night flicker past as pale
and dark bands; far below, a dwarven mountain fortress changing through the
centuries in one view: pale walls turning grey then soot-black, new towers and
spires rising from the rock, a wing collapsing and rebuilt wider, a single
weathered king statue in a widening courtyard; ahead of the figures the red
light thins, cools and splits into six beams fanning out at equal angles,
white, pale blue, violet, copper, smoke grey and earth brown, each beam ending
in one small hard faceted gem hanging in the dark void; beyond the six gems
there is nothing at all, no people, no places; faces not visible; camera high,
looking down past the figures
```

<!-- img id=tavola-salto-sei-gemme-B size=1536x864 stile=tavola serie=base seed=1372001 -->
```
an immense stream of red light carrying four figures through a sky where day
and night flicker past as pale and dark bands, seen in three-quarter view from
slightly behind and above: Thorik, an older shield dwarf, broad and heavy,
weathered battle-scarred face, long grey beard, heavy dark steel full plate
with a blue gem in the breastplate and a rust-red cloak, wearing the
adamantine crown, a double-crescent runic dwarven waraxe in his hand, the
crown holding three gems with the red one dimming; Tordek, an adult dwarf,
compact and very muscular, fierce frown, shaved bald head and a thick black
beard, a saffron-orange monk robe with a dark sash and bare arms, on his hands
two heavy steel gauntlets, the left burning with green fire, the right with
orange-red forge fire; Hella, a short stocky broad-shouldered dwarf woman,
sturdy dwarven proportions, amber-gold eyes, light wavy blonde hair with small
green leaves, pointed ears like young leaves, armour of cracked grey stone and
overlapping green oak leaves, a necklace of braided roots set with green
seed-stones, a faint heart-shaped ruby glow on her breastbone; Artemis, a
slender human man, sly half-smile, dark messy hair, a long black coat, large
black feathered wings folded behind him, on his left hand a black ring with a
violet stone crackling with small white-blue sparks, wings spread; far below,
a dwarven mountain fortress changing through the centuries in one view: pale
walls turning grey then soot-black, new towers and spires rising, a wing
collapsing and rebuilt wider, a single weathered king statue in a widening
courtyard; ahead of them the red light thins, cools and splits into six beams
fanning out at equal angles, white, pale blue, violet, copper, smoke grey and
earth brown, each beam ending in one small hard faceted gem hanging in the
dark void; beyond the six gems there is nothing at all, no people, no places;
camera high
```

### 3.4 · La riga in più per le B con immagine guida

Con FLUX.2 [klein] e un'immagine guida (il kit del 27/11, nodi `ReferenceLatent`)
il prompt B si apre con questa riga, e il foglio di riferimento è composto in
locale dai quattro ritratti di `PG/Immagini/` (ricetta nel JSON, campo
`immagine_guida`). Il modello tende a ricopiare il riferimento: la riga gli
chiede di prendere solo volti, capelli, abiti e oggetti.

```
the reference image is a character sheet of four heroes, from left to right
Thorik, Tordek, Hella and Artemis: keep only their faces, hair, clothing and
items, and repaint them inside one new scene as a single oil painting with one
light, not a row of portraits and not the backgrounds of the sheet; the new
scene:
```

---

## §4 · Il gate di rifiuto

Si applica a piena risoluzione e il giorno dopo (`rumblingstone-art-direction`
§6). Si butta la tavola se anche una sola di queste è vera:

1. mani sbagliate in modo che si nota a grandezza di stampa;
2. la luce non viene da sinistra in alto, o c'è una seconda fonte calda oltre al
   Rubino (i Bracieri di Tordek e l'anello di Artemis sono ammessi: sono fuochi
   piccoli e loro);
3. in B, un PG non si riconosce dal suo segno (§2);
4. testo, lettere o rune leggibili, anche sulla Corona e sull'incudine;
5. simmetria da modello: folla clonata, composizione specchiata, i quattro in
   fila come in posa;
6. la tavola non dice la sua riga di funzione (§3);
7. **solo tavola 3**: dietro le gemme compare qualcosa (un volto, una figura,
   un luogo): è uno spoiler e si butta anche se è bella;
8. **solo versione A**: un volto dei PG si legge.

Il conto A contro B usa i requisiti scritti prima di guardare, in
`/mnt/project-files/tavole-serata-2026-11-30/MISURA-DICHIARATA.md`.

---

## §5 · Come si generano

| Motore | Cosa fa qui | Seme | Immagine guida | Licenza |
|---|---|---|---|---|
| **FLUX.2 [klein] 4B** fp8, ComfyUI `0df1646`, in CPU nel container | A, B e B con guida, 4 passi, cfg 1, euler | sì, §1 | sì, in locale | Apache-2.0 (pesi), sha256 verificati come in `comfyui_batch.py` |
| **Canva AI** `generate-image` | solo testo, prompt = ancora + soggetto + negativi in coda | no: il file è il sorgente | **no**: i PG non si caricano, la B è somigliante solo da descrizione | termini di servizio Canva; il modello non è dichiarato |
| Kaggle (T4) | lo stesso JSON, quando la coda lo permette | sì | sì | come FLUX |

Per rilanciare in locale, dal JSON:

```
python3 esegui_flux.py CASI-FLUX-SERATA-2026-11-30.json OUT --solo <id,id>
python3 esegui_flux.py CASI-FLUX-SERATA-2026-11-30.json OUT --solo <id>-B --guida foglio-pg-guida.png --suffisso -guida
```

Il lanciatore e il foglio di guida stanno con le candidate, in
`/mnt/project-files/tavole-serata-2026-11-30/strumenti/`, finché Jfs non
sceglie. Le candidate non entrano nel repo prima della scelta.

---

## §6 · Esecuzione e confronto

_Da compilare._

---

## §7 · Confronto immagine-scheda

_Da compilare._
