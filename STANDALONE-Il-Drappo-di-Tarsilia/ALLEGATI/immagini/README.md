# Le immagini del modulo — come si producono

> **Cosa c'è qui**: i prompt ([`PROMPT-RITRATTI-E-TAVOLE.md`](PROMPT-RITRATTI-E-TAVOLE.md)),
> la loro provenienza ([`PROVENIENZA.txt`](PROVENIENZA.txt)) e i PNG quando ci
> saranno. **Questa pagina è la procedura**: dal computer spento all'immagine
> agganciata al booklet.
>
> Finché i raster non ci sono, il modulo **è già stampabile**: i sei
> ritratti-segnaposto vettoriali di `../tavole/` stanno nel fascicolo e i booklet
> si generano lo stesso. I raster li sostituiranno senza toccare una riga di testo.

---

## §1 · Il TL;DR, se hai già tutto installato

```bash
scripts/comfyui-local/start.sh                       # ComfyUI su :8188, con --lowvram
python3 scripts/comfyui_batch.py --lista             # cosa manca
python3 scripts/comfyui_batch.py                     # genera i diciotto mancanti
# … il giorno dopo, il gate di rifiuto:
python3 scripts/comfyui_batch.py --solo ritratto-vanna --reroll 1 --forza
python3 scripts/comfyui_batch.py --solo ritratto-vanna --fissa-seed   # quando ti convince
```

Il resto di questa pagina spiega **perché** i comandi sono in quest'ordine.

---

## §2 · Prima di accendere la GPU: la scelta che non si disfa

**La licenza sta nei pesi, non nel software**
([ADR-0019](../../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)).
ComfyUI è GPL-3.0 e non limita ciò che produce; i pesi sì.

| Pesi | Licenza | Qui |
|---|---|---|
| **SDXL** | OpenRAIL++-M | ✅ **default** — ControlNet e LoRA maturi, gira su 6-8 GB |
| **FLUX.1 [schnell]** | Apache 2.0 | ✅ se serve testo leggibile in-immagine, e solo **quantizzato** su questa macchina |
| **FLUX.1 [dev]** | Non-Commercial v2.0 | ❌ **rifiutato dallo script**, non sconsigliato |

Il rifiuto è codice, non un avvertimento: `comfyui_batch.py` esce con `1` se il
nome del checkpoint contiene `flux1-dev` e simili. La ragione è che l'errore si
scopre **un anno dopo**, quando rifare dieci immagini costa più che accettare
oggi una resa leggermente inferiore.

### La macchina del DM

RTX 4050 Laptop (**6141 MiB** di VRAM), 16 GB di RAM, i7-13650HX, Bazzite. Su
questa configurazione:

- `start.sh` passa già **`--lowvram`**: non toglierlo;
- lo script genera **un'immagine alla volta** (`batch_size` fisso a 1). Un batch
  è il modo più rapido di far uscire ComfyUI per memoria esaurita;
- se ComfyUI dichiara meno di 8 GiB, lo script **te lo dice** all'avvio;
- FLUX schnell in fp16 **non ci sta**: se lo usi, usa una build quantizzata.

---

## §3 · Setup, una volta sola

1. **ComfyUI in container** — `scripts/comfyui-local/README.md` (Distrobox su
   Bazzite: l'OS immutabile non viene toccato).

   ```bash
   scripts/comfyui-local/setup-distrobox.sh
   ```

2. **I pesi**, scaricati a mano in `scripts/comfyui-local/ComfyUI/models/checkpoints/`.
   Il nome atteso dal registro dello script è `sd_xl_base_1.0.safetensors`; se il
   tuo file si chiama diversamente, passa `--checkpoint <nome>` invece di
   rinominarlo.

3. **Prova che risponda**:

   ```bash
   scripts/comfyui-local/start.sh
   curl -s http://127.0.0.1:8188/system_stats | head -c 200
   ```

Se ComfyUI non c'è, lo script **non fallisce a metà**: dice quale comando lo
avvia ed esce pulito, senza lasciare file scritti (ADR-0019 §4).

---

## §4 · La serie: diciotto, non venti

Il capitolato
([`PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`](../../PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md))
ne conta **diciotto**, e la ragione sta nella skill di direzione artistica §8:
*un modulo con sei immagini scelte batte un modulo con venti generate.*

| Quante | Cosa | Formato |
|---|---|---|
| 6 | ritratti dei PG | 832 × 1216 |
| 5 | ritratti PNG: Vesca, Attu, Roncetti, Sfregio, Nonna Grasa | 832 × 1216 |
| 3 | tavole d'ambiente: la Ruota, la Cena, le stalle | 1536 × 864 |
| 1 | il Drappo, come oggetto | 832 × 1216 |
| 1 | copertina | 832 × 1216 |
| 2 | spot: la bilancia dell'Oca, la pagina del registro | 800 × 800 |

Le **due tavole del §8** (Tarsilia dall'alto, la Ruota il giorno prima) sono
marcate `serie=extra`: stanno nel file perché fissano il *patto d'inquadratura*
condiviso con Channathgate, ma **non fanno parte dei diciotto** e si generano
solo con `--serie tutto`.

> Chi aggiunge un diciannovesimo prompt `serie=base` fa **rossa la CI**:
> `test_serie_base_e_diciotto` esiste apposta. Non è un divieto — è un modo di
> obbligare a *decidere* invece di lasciar crescere l'elenco.

**Già fatti e da non rifare**: 19 fregi di capitolo, 8 stemmi, 2 mappe tattiche
(+ la versione giocatore), 4 prop, 6 ritratti-segnaposto vettoriali.

---

## §5 · Generare

```bash
python3 scripts/comfyui_batch.py --lista        # nessun side-effect: cosa c'è e cosa manca
python3 scripts/comfyui_batch.py --dry-run      # i prompt composti, senza rete
python3 scripts/comfyui_batch.py                # genera solo i mancanti
```

Quello che succede a ogni immagine:

1. si legge il prompt **dal markdown** (che resta il master, ADR-0003);
2. si antepone il **look comune** (solo ai ritratti) e l'**ancora storica**
   fiamminga (a tutti) — le due leve che fanno somigliare fra loro immagini
   generate in sessioni diverse;
3. si calcola il **seed**: quello fissato nell'annotazione, o uno derivato
   dall'`id` in modo stabile;
4. si POSTa il workflow a ComfyUI e si aspetta sulla coda;
5. il PNG si scrive **solo a download completo** — niente file troncati;
6. si scrive la riga in `PROVENIENZA.txt`.

**Conta 1,5-2 ore di macchina** per i diciotto: ~1,5-2 minuti a immagine, per il
numero di tentativi che il gate impone (§6). Il collo di bottiglia è il giudizio,
non la GPU.

---

## §6 · Il gate di rifiuto — **il giorno dopo**

Non alla fine della sessione di generazione: **il giorno dopo**. Dopo quaranta
generazioni si tiene tutto quello che è «abbastanza», perché si è stanchi. È il
bias che la skill
[`rumblingstone-art-direction`](../../../skills/rumblingstone-art-direction/SKILL.md) §6
nomina per non subirlo.

Si butta e si rigenera se **anche solo una** è vera:

1. le **mani** sono sbagliate in modo visibile a grandezza di stampa;
2. la **luce** non viene da dove dice il lock;
3. il personaggio **non è riconoscibile** rispetto alla sua scheda del §6 dei prompt;
4. c'è **testo** dentro l'immagine — in un libro stampato è ciò che tradisce
   prima la generazione automatica;
5. la **simmetria è troppo perfetta**: è la firma del modello, non una scelta;
6. l'immagine è **corretta e non dice niente**.

Aspettati di scartare **2-3 generazioni su 4**. Rigenerare:

```bash
python3 scripts/comfyui_batch.py --solo ritratto-vanna --reroll 1 --forza
python3 scripts/comfyui_batch.py --solo ritratto-vanna --reroll 2 --forza
```

`--reroll` cambia il seed **in modo deterministico**: anche il terzo tentativo
è rifacibile. E la regola che rende il gate reale:

> Il set vale quanto il suo pezzo peggiore. Nove immagini buone e una mediocre
> non fanno «nove su dieci»: fanno un libro in cui il lettore si accorge che le
> immagini sono generate. **Meglio otto e due segnaposto vettoriali**, che almeno
> dichiarano cosa sono.

---

## §7 · Fissare il seed — il passo che nessuno fa

Quando un'immagine ti convince:

```bash
python3 scripts/comfyui_batch.py --solo ritratto-vanna --fissa-seed
```

Scrive `seed=<n>` nell'annotazione dentro `PROMPT-RITRATTI-E-TAVOLE.md`. Da quel
momento quell'immagine **si rifà**: fra un anno, con due tavole da rigenerare,
non è un colpo di fortuna perduto.

⚠️ Il seed **non** garantisce il byte identico su un'altra macchina — cambia coi
pesi e con la versione di ComfyUI. Garantisce la cosa che serve: ripartire dallo
stesso punto invece che dal caso.

---

## §8 · Prima di committare

- [ ] **la riga in `PROVENIENZA.txt`** c'è (la scrive lo script). Senza, il file
      non si committa: ADR-0019 §2;
- [ ] il **gate** è stato applicato, e il giorno dopo;
- [ ] il PNG è **ridimensionato** se è enorme — un PNG da 12 MB nel repo resta 12
      MB per sempre (`GUIDA-IMMAGINI.md` §4.2);
- [ ] nessun **testo** dentro l'immagine;
- [ ] **spoiler**: `il-drappo.png` mostra le nove facce del Giorno 3 §8. Sta nel
      booklet del DM, non in quello dei giocatori.

I booklet le pescano da sé, per nome di file: non c'è niente da agganciare a mano.

---

## §9 · Dove sta il resto

| Cosa | Dove |
|---|---|
| I prompt, con le annotazioni leggibili dalla macchina | [`PROMPT-RITRATTI-E-TAVOLE.md`](PROMPT-RITRATTI-E-TAVOLE.md) |
| Il mestiere: coerenza, schede-personaggio, lock, gate | [`rumblingstone-art-direction`](../../../skills/rumblingstone-art-direction/SKILL.md) |
| Quali pesi si possono usare, e cosa si registra | [ADR-0019](../../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md) |
| ComfyUI in container su Bazzite | [`scripts/comfyui-local/README.md`](../../../scripts/comfyui-local/README.md) |
| La procedura generale delle immagini di campagna | [`GUIDA-IMMAGINI.md`](../../../docs/guides/GUIDA-IMMAGINI.md) |
| Come i tool si incastrano fra loro | [`GUIDA-FLUSSO-LOCALE.md`](../../../docs/guides/GUIDA-FLUSSO-LOCALE.md) |
