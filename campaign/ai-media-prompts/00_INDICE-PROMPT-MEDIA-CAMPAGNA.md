# 🎬 INDICE GENERALE — PROMPT AI PER MEDIA VISIVI CAMPAGNA RUMBLINGSTONE

## *Video Introduttivi + Immagini di Sessione — Vincolo Lore Faerûn 1372 DR / Shaar / RHoD*

---

> **Scopo:** Questo indice organizza tutti i file di prompt AI per generare video introduttivi e immagini di sessione per ogni arco della campagna RumblingStone. Ogni file è self-contained: include contesto lore, dettagli atmosferici, vincoli narrativi e prompt pronti per copia-incolla in strumenti di generazione AI (Runway, Pika, Sora, Midjourney, DALL-E, etc.).

> **Vincoli globali (applicati a TUTTI i prompt):**
> - **Setting:** Faerûn, 1372 DR, Shining South / Shaar / Channath Vale
> - **Stile visivo:** Dark fantasy realistico: paesaggi in campo lunghissimo con figure minuscole contro orizzonti immensi, luce naturale radente (ora dorata, cieli coperti, torce), materiali consumati e sporchi (armature ammaccate, cuoio, polvere, sangue), grana di pellicola; come ancora, la pittura a olio europea fra Seicento e Ottocento (chiaroscuro, paesaggio e battaglia romantici)
> - **Palette:** Toni caldi desertici (Shaar), pietra scura e lava (dwarven halls), verde profondo (foreste sacre), rosso sangue e nero (Red Hand)
> - **NO:** Nessuna invenzione fuori dal lore di campagna. NO 5e. NO Spellplague. NO elementi post-1385 DR.

> **Promemoria di distribuzione:** le immagini (e i video e l'audio) prodotti con questi prompt, se escono dal repo, vanno etichettati come contenuto generato da IA sulle piattaforme che lo chiedono.

---

## 📁 FILE PER ARCO

| # | Arco | File Prompt | Contenuto |
|---|------|-------------|-----------|
| 00 | Red Hand of Doom — L'Inizio nello Shaar | `01_ARC00_shaar-origins.md` | 1 video intro + 3 immagini sessione |
| 01 | La Miniera — Belkram's Fall | `02_ARC01_la-miniera.md` | 1 video intro + 4 immagini sessione |
| 02 | Scala d'Ossa — Abbathor & Funghi | `03_ARC02_scala-ossa-funghi.md` | 1 video intro + 3 immagini sessione |
| 03 | La Cittadella — Drow & Tempio di Moradin | `04_ARC03_la-cittadella.md` | 1 video intro + 4 immagini sessione |
| 04 | Tomba di Belkram — Cerebromorphosis | `05_ARC04_tomba-belkram.md` | 1 video intro + 3 immagini sessione |
| 05 | Stanza Runica — La Gemma dell'Antico Portatore | `06_ARC05_stanza-runica.md` | 1 video intro + 2 immagini sessione |
| 06 | Corona di Adamantio — Half-Illithid & la Morte di Hella | `07_ARC06_corona-adamantio.md` | 1 video intro + 3 immagini sessione |
| 07 | Portale della Forgia Eterna — Piani Elementali | `08_ARC07_portale-forgia-eterna.md` | 1 video intro + 6 immagini sessione |
| 08 | Battaglia di Hammerfist — La Mano Rossa del Destino | `09_ARC08_battaglia-hammerfist.md` | 1 video intro + 5 immagini sessione |
| 09 | Post-Hammerfist — Quest Personali & Rethmar | `10_ARC09_post-hammerfist.md` | 1 video intro + 16 immagini sessione |
| 10 | Atlante Visivo — Personaggi Giocanti e Villain Principali | `11_PG_E_VILLAIN_PROMPTS.md` | Ritratti e concept art (24 PG/NPC/Creature) |

---

## 🎯 CONVENZIONI PER I PROMPT

### Struttura di ogni file

```
1. CONTESTO LORE (non generativo — fornisce background al DM)
2. VIDEO INTRO ARCO
   - Prompt video (15-30 sec, cinematico)
   - Note su musica/mood consigliati
3. IMMAGINI SESSIONE (1 per sotto-sezione narrativa)
   - Prompt immagine (splash art / key visual)
   - Aspect ratio consigliato
   - Palette e mood specifici
```

### Convenzioni prompt

- **[STILE]** = prefisso di stile (es. "cinematic dark fantasy, realistic lighting, 4K")
- **[LORE]** = vincolo narrativo (es. "Forgotten Realms 1372 DR, Shaar grasslands")
- **[NO]** = negative prompt (es. "no modern elements, no 5th edition aesthetics")
- **[CAMERA]** = movimenti di camera per video (es. "slow dolly forward, crane shot")
- **[DURATA]** = durata target video

### Best Practices per AI Video

- Prompt brevi e visivi (max 150 parole per video prompt)
- Descrivere AZIONE, non lore
- Focus su composizione, luce, e movimento
- Evitare dialoghi — solo visual storytelling

### Best Practices per AI Immagini

- Prompt descrittivi con dettagli ambientali
- Specificare illuminazione, prospettiva, scala
- Mai titoli di opere (film, serie, videogiochi, colonne sonore), nomi di artisti o compositori, marchi: né «in the style of…» né «…-inspired». Si descrivono le convenzioni: luce, palette, scala, camera, materiali, tecnica, epoca; per l'audio strumenti, tempo, registro, dinamica. Le scuole pittoriche storiche in pubblico dominio sono ammesse come ancora (es. "Byzantine icon painting", "Dutch Golden Age chiaroscuro"). Regola: [ADR-0015 §5](../../plans/adr/ADR-0015-standard-prompt-immagine.md)
- Aspect ratio: 16:9 per splash, 4:3 per portrait scene

---

## 📊 RIEPILOGO ASSET

| Tipo | Quantità Totale |
|------|----------------|
| Video Intro (per arco) | 10 |
| Immagini Sessione | ~53 |
| Ritratti PG/NPC/Creature| 24 |
| **Totale Asset** | **~87** |

---

> **Nota:** Tutti i prompt sono vincolati al lore della campagna come documentato nei file di sessione, NPC, ed encounters del repository RumblingStone. Nessun elemento è inventato: ogni scena, personaggio e ambiente è tracciabile ai file sorgente.
