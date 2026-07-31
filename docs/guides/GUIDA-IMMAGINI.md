# Guida completa — generare le immagini della campagna

> **Cosa copre**: dal «mi servirebbe un'illustrazione di questa scena» fino
> all'immagine incorporata nel booklet. Quale generatore usare per cosa, come
> si scrive un prompt che funziona davvero, come si prepara l'intero arco in
> un comando, dove salvare i risultati e come agganciarli, e cosa fare quando
> il modello sbaglia.
>
> **Regole dietro**: [ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md)
> (standard dei prompt) · [ADR-0005](../../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md)
> (confini IP) · [ADR-0013 §3](../../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md)
> (spoiler). Le **mappe tattiche** non stanno qui: sono
> [GUIDA-MAPPE](GUIDA-MAPPE.md) (questa guida copre le immagini *d'atmosfera*).

---

## 0. TL;DR

```bash
# 1. prepara le schede-prompt di tutto l'arco (estrae le scene dai master)
python3 scripts/dm.py prompts "07_il Portale Della Forgia Eterna"

# 2. apri il file generato, scrivi i prompt nelle schede che ti servono
#    07_.../Immagini/PROMPT-IMMAGINI-07ILP.md

# 3. genera: PRIMA la scena-madre, poi le altre agganciate ad essa
# 4. salva in <arco>/Immagini/, registra nell'atlante asset, e usa
```

---

## 1. Quale generatore, per cosa

Nessuno è «il migliore»: cambiano per come reagiscono al prompt.

| Generatore | Va forte su | Debolezze | Come parlargli |
|---|---|---|---|
| **Nano Banana 2 / Gemini** | scene complesse con molti elementi; **ritocchi a parole** («stessa immagine ma il verde più freddo») | a volte addolcisce i toni cupi | regge **prompt lunghi**: incollalo tutto, comprese le note di scala |
| **ChatGPT / GPT Image** | oggetti singoli, carte, artefatti, ritratti puliti | tende a **scrivere testo** dove non serve; prompt lunghi lo confondono | accorcia: togli le note tecniche finali, aggiungi sempre *«no text anywhere in the image»* |
| **ComfyUI locale** ([setup](../../scripts/comfyui-local/README.md)) | partire da una **mappa già renderizzata** e «dipingerla»; controllo totale, nessun costo per immagine | serve una GPU; curva di apprendimento | vedi `hero-map-comfyui.md` nella skill mapmaking |

**Regola pratica**: scene → Gemini · oggetti e carte → GPT Image · hero map da
una mappa esistente → ComfyUI.

---

## 2. Come si scrive un prompt che funziona

### 2.1 La struttura: due paragrafi, sempre

1. **La scena** — cosa si vede, in prosa concreta;
2. **La direzione artistica** — resa, luce, palette, mood, composizione.

In **inglese** (i modelli lo seguono meglio); note e commenti in italiano.

### 2.2 Un esempio smontato

Dal prompt della soglia di Terros, pezzo per pezzo — e *perché* ogni pezzo c'è:

| Frammento | A cosa serve |
|---|---|
| *«a chamber as wide as a market square»* | **scala per paragone**: il modello non sa cosa siano «60 m», ma sa quanto è grande una piazza |
| *«three small silhouettes stand at the near edge for scale, backs to the viewer»* | **figure di scala**: senza, il modello disegna una stanzetta |
| *«beyond the slab's rim there is no floor at all — only void»* | **cosa è sbagliato** nel posto: è il dettaglio che rende memorabile una scena |
| *«geodes drift past like fish too large for the lantern they circle»* | una similitudine concreta batte tre aggettivi |
| *«it does not move. It does not breathe.»* | dice al modello cosa **non** fare: qui serve ambiguità, non un mostro |
| *«lighting from two sources only: …»* | vincolare le sorgenti di luce è ciò che rende le immagini di un arco **coerenti** |

### 2.3 I tre trucchi che hanno fatto la differenza

1. **Scala per paragone, mai metrature.** «Larga quanto la sala di una
   locanda» funziona; «Ø 60 m» no. (È la stessa regola dei read-aloud,
   ADR-0014: descrivi da avventuriero, non da architetto.)
2. **La posa racconta il carattere.** Per Durik non ho chiesto «un cane
   guardiano»: ho chiesto che si mettesse **di traverso fra qualcuno e il
   pericolo**, *prima ancora di guardarsi intorno*. Il canone («Protegge
   Hella») entra nell'immagine come **gesto**, non come didascalia.
3. **Dì cosa NON è.** «Non è un costrutto: è QUALCUNO», «niente piastre,
   niente ingranaggi, niente giunti». I negativi dentro la prosa pesano più
   della lista `Da evitare`.

### 2.4 La lista dei negativi

Sempre presente, sempre almeno: `text, letters, watermark, signature,
modern objects, cartoon`. Poi i negativi **specifici della scena** (per
Durik: `golem, robot, mechanical joints, collar, snarling, cute cartoon dog`).

### 2.5 Formati

| Uso | Aspect ratio |
|---|---|
| splash / apertura di scena | **16:9** |
| handout, carta artefatto | **3:4** |
| token, ritratto PNG | **1:1** |
| copertina booklet | **2:3** o 3:4 |

---

## 3. Preparare un arco intero

```bash
python3 scripts/dm.py prompts "<cartella dell'arco>"          # genera/aggiorna le schede
python3 scripts/dm.py prompts "<cartella dell'arco>" --list   # solo l'elenco delle scene
```

Lo script estrae **tutti i read-aloud** dei master (ARC-07: 46 scene), ne
ricava fonte, sezione ed estratto, censisce le immagini già presenti, e
scrive una **scheda per scena** in `<arco>/Immagini/PROMPT-IMMAGINI-<TAG>.md`.
I prompt li scrivi tu (o li chiedi a un agente: *«compila la scheda 14»*).

**Rigenerare non ti fa perdere niente**: le schede già scritte restano dove
sono, quelle che hai aggiunto a mano (artefatti, ritratti — scene senza
read-aloud) vengono riportate in coda, e a parità di contenuto il file esce
identico byte per byte.

### 3.1 La bibbia visiva e la scena-madre (il pezzo che rende un set)

In testa al file c'è la **bibbia visiva** dell'arco: palette, sorgenti di
luce, resa. Compilala una volta.

Poi scegli la **scena-madre** — l'ambiente più rappresentativo — e:

1. genera **quella per prima**, iterando finché non è giusta;
2. per tutte le altre, aggiungi al prompt:
   *«same world, same palette and lighting as the previous image»*;
3. nelle schede, annota a quale scena si agganciano.

Per ARC-07 la scena-madre è la **soglia della camera di Terros** (scheda 10):
fissa mithral + verde smeraldo + nero-violetto, e le due sole sorgenti di luce.

### 3.2 Chi può vedere cosa

Ogni scheda ha il campo **Destinatario**:

- **`pg`** — mostrabile ai giocatori: ritrae qualcosa che hanno già vissuto,
  o è deliberatamente ambiguo (la soglia di Terros è `pg` perché il guardiano
  sembra ancora solo roccia);
- **`dm`** — spoiler: non esce prima del suo momento (il ritorno di Durik).

Un'immagine mostrata troppo presto brucia una scena esattamente come un
titolo rivelatore: vale la stessa disciplina degli handout (ADR-0013 §3).

---

## 4. Cosa fare del risultato

### 4.1 Dove va e come si chiama

```
<arco>/Immagini/<scena-descrittiva>.webp        # o .png
```

Nomi **descrittivi**, non `image_final_2.png`: seguono lo stile di quelli già
in repo (`camera-nodo-terra.webp`, `ilCuoreDiMoradin.png`).

### 4.2 Alleggerire prima di committare

I generatori sfornano PNG enormi. Due strade:

```bash
# ridimensiona (Pillow) — 1600px di lato lungo è più che sufficiente per stampa A4
python3 -c "from PIL import Image; im=Image.open('in.png'); im.thumbnail((1600,1600), Image.LANCZOS); im.save('out.png', optimize=True)"

# oppure converti in webp (batch, ImageMagick)
bash converters/Image-to-webp/conver_webp_new.sh <cartella>
```

> Nota: nei **booklet** ci pensa il builder — un'immagine oltre 600 KB viene
> ricompressa in JPEG a 1400px **solo per l'embed** (nel repo resta
> l'originale). Ma un PNG da 12 MB nel repo resta 12 MB per sempre: ridimensiona.

### 4.3 Agganciarla dove serve

| Dove | Come |
|---|---|
| **Atlante asset dell'arco** | aggiungi la riga in `ARC*-ATLANTE-ASSET.md`: file · scena/parte · **quando mostrarla** |
| **Copertina di un booklet** | campo `"cover_image"` nel manifest ([GUIDA-BOOKLET-E-PDF §3](GUIDA-BOOKLET-E-PDF.md)) |
| **Dentro un capitolo o un handout** | `![Didascalia](percorso/relativo/immagine.png)` nel markdown — il builder la incorpora da sé |
| **La scheda del prompt** | segna lo stato ✅ e il nome del file generato: così sai cos'è già fatto |

Esempio reale di handout con immagine:
`09_…/homebrew/HANDOUT-MAPPA-CHANNATHGATE.hb.md`.

---

## 5. Se il risultato non va

| Sintomo | Perché e cosa fare |
|---|---|
| **Scrive testo / rune illeggibili** | tipico di GPT Image → aggiungi *«no text anywhere in the image»* e metti `text, letters` nei negativi |
| **Le immagini non sembrano un set** | non hai agganciato alla scena-madre → rigenera con *«same world, same palette and lighting as the previous image»*, e vincola le sorgenti di luce nel prompt |
| **La stanza sembra piccola** | mancano i riferimenti di scala → aggiungi il paragone («grande come una piazza») **e** figure umane di spalle in primo piano |
| **Il soggetto «posa» invece di agire** | descrivi il **gesto** e il suo motivo, non l'aspetto: «si mette fra X e Y prima ancora di guardarsi intorno» |
| **Anatomia sbagliata** (creature) | dì di che *tipo* è («legge come un levriero che corre: petto profondo, gambe lunghe») e come sono fatti i materiali («il mithral segue le linee dei tendini») |
| **Troppo colorato / da videogioco** | vincola la palette a 3 colori e chiedi *«muted palette, painterly, visible brushwork»* |
| **Il modello mette un mostro dove serviva ambiguità** | scrivilo esplicito: *«it does not move, it does not breathe»* + negativo `creature clearly alive` |
| **Immagine bella ma inutilizzabile in stampa** | rigenerala nel formato giusto (§2.5): un 16:9 non entra in una carta 3:4 |

---

## 6. Checklist prima di mostrare o committare

- [ ] **Spoiler**: la scheda dice `pg`? Se dice `dm`, è il suo momento?
- [ ] **IP** (ADR-0005): nessun nome di artista vivente nel prompt, nessuna
      immagine altrui usata come reference
- [ ] Nome file descrittivo, in `<arco>/Immagini/`
- [ ] Ridimensionata (≤ ~2 MB) prima del commit
- [ ] Riga aggiunta all'**atlante asset** con «quando mostrarla»
- [ ] Scheda del prompt aggiornata a ✅ col nome del file
- [ ] Se va in un booklet: rigenerato con `dm.py booklet <manifest>`

---

## 7. Dove sta il resto

| Cosa | Dove |
|---|---|
| Lo standard dei prompt (anatomia, bibbia visiva, spoiler) | [ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md) |
| Esemplare compilato (46 scene, 3 prompt scritti) | `07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md` |
| Vocabolario di stile e confini IP | `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md` |
| Hero map da una mappa renderizzata (GPU) | `skills/rumblingstone-mapmaking/references/hero-map-comfyui.md` · [`scripts/comfyui-local/README.md`](../../scripts/comfyui-local/README.md) |
| Mappe tattiche (tutt'altro flusso) | [GUIDA-MAPPE](GUIDA-MAPPE.md) |
| Incorporare le immagini nei booklet | [GUIDA-BOOKLET-E-PDF](GUIDA-BOOKLET-E-PDF.md) |
| Cosa si può condividere | [GUIDA-CONDIVISIONE-IP](GUIDA-CONDIVISIONE-IP.md) |
