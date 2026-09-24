# Texture per il render 3D delle mappe — la convenzione

> **La regola in una riga**: le texture **non stanno nel repo**. Qui c'è solo la
> convenzione delle cartelle; i file li mette il DM sulla sua macchina, e il
> render funziona lo stesso se non ce ne sono.

---

## §1 · Come funziona

`costruisci_mappa.py` cerca, per ogni famiglia di superficie, una cartella con
quel nome dentro `scripts/blender/texture/`. Se la trova, usa la prima immagine
che contiene (preferendo quelle col nome che contiene `color`); se non la trova,
usa il **colore piatto** che il renderer SVG assegna a quel simbolo.

```
scripts/blender/texture/
├── terra-battuta/    diff_2k.png       ← usata
├── muratura/         color_2k.jpg      ← usata (preferita: contiene "color")
└── erba/                               ← vuota: si usa il colore piatto
```

Le chiavi previste — sono quelle della tabella `TEXTURE` in
[`render_map_blender.py`](../../render_map_blender.py):

| Chiave | Simboli che la usano |
|---|---|
| `erba` | 🟩 🌿 |
| `fogliame` | 🌲 🌳 |
| `terra-battuta` | 🟫 |
| `sabbia` | 🟨 |
| `pavimento` | ⬜ |
| `muratura` | 🏰 |
| `legno` | ⬛ |
| `pietra-chiara` | 🏛 🟪 |
| `roccia` | ⛰ 🪨 |
| `acqua` | 🟦 🌊 |

Non servono UV: il materiale proietta a **scatola** sulle coordinate oggetto, che
su volumi squadrati è indistinguibile da una mappatura fatta a mano.

---

## §2 · Dove prenderle

**[Poly Haven](https://polyhaven.com/textures)** è la fonte consigliata: è
**CC0** — dominio pubblico, nessuna attribuzione dovuta, uso commerciale
ammesso — ed è esattamente la garanzia che serve qui, perché
[ADR-0019](../../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)
chiede che un asset dentro un artefatto versionato non precluda la
pubblicazione.

⚠️ **Verifica comunque la licenza del singolo file**, non quella del sito. È la
stessa cautela che il repo applica alle collezioni museali: una collezione ad
accesso aperto può contenere un'opera che non lo è.

Bastano le mappe **colore** (`diff` / `albedo`), a **2K**: la camera è
ortografica e lontana, e una 4K raddoppia il tempo di caricamento senza cambiare
un pixel di quello che si vede.

❌ **Da non mettere qui**: qualsiasi asset proprietario (Inkarnate, Dungeon
Scrawl, banche immagini a pagamento) e qualsiasi file di cui non trovi la
licenza. Vale la lista del capitolato del Drappo.

---

## §3 · Perché sono gitignorate

Tre ragioni, in ordine:

1. **il peso** — dieci texture 2K sono ~80 MB, e in git restano per sempre anche
   quando le sostituisci;
2. **sono rigenerabili** — si riscaricano in due minuti da una fonte pubblica,
   quindi sono un artefatto e non un master (ADR-0003);
3. **la catena degrada pulito** — senza texture il render esce comunque, coi
   colori piatti dell'SVG. Chi clona il repo ottiene una mappa leggibile senza
   scaricare niente.

Se ne aggiungi, annota fonte e licenza in `CREDITS.md` — anche per il CC0, che
non **obbliga** all'attribuzione ma non la vieta, e fra un anno la riga serve a
te più che alla licenza.
