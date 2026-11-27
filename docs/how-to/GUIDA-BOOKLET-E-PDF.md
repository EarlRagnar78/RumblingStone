# Guida completa — dai master ai booklet e ai PDF in mano ai giocatori

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

> **Cosa copre**: tutta la catena, dall'inizio alla fine. Come si genera un
> booklet in stile «pergamena», come escono i PDF A4 da stampare o inviare,
> quali programmi servono (e come installarli su ogni sistema), quali
> container servono **e quando non servono affatto**, e cosa fare quando
> qualcosa non funziona.
>
> **Regole dietro le quinte**: [ADR-0013](../../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md)
> (standard dei booklet: struttura, anti-spoiler, doppia via HTML/Homebrewery,
> PDF) e [ADR-0014](../../plans/adr/ADR-0014-regia-sensoriale-obbligatoria.md)
> (regia sensoriale obbligatoria nei master).

---

## 0. TL;DR — i tre comandi che servono davvero

```bash
# 1) Il file unico da mandare al GRUPPO (copertina + «il cammino fin qui»)
python3 scripts/dm.py booklet "<arco>/homebrew/sessione-<nome>/<NOME>-GRUPPO-CAMMINO.manifest.json" --pdf

# 2) Il booklet del DM + gli handout: tutte le schede in HTML, .hb.md e PDF
python3 scripts/dm.py booklet "<arco>/homebrew/sessione-<nome>/<NOME>-BOOKLET.manifest.json" --format both --pdf-all

# 3) Se vuoi solo l'HTML sfogliabile (nessun browser headless richiesto)
python3 scripts/dm.py booklet "<manifest>.json"
```

I PDF finiscono in `<cartella del manifest>/pdf/`, con **prefisso `pg-`**
(si possono inviare ai giocatori) o **`dm-`** (restano al DM).

---

### 0.0-bis · `dm.py volume` — la catena dei mestieri in ordine

Quando il volume è **finito** e lo vuoi portare in stampa, c'è un comando solo che
li chiama tutti nell'ordine giusto ([ADR-0031](../../plans/adr/ADR-0031-dm-volume-ordine-dei-mestieri.md)):

```bash
python3 scripts/dm.py volume MANIFEST.json                    # fino allo schermo
python3 scripts/dm.py volume MANIFEST.json --stampa           # + l'edizione Typst
python3 scripts/dm.py volume MANIFEST.json --stampa --imposto # + il libretto da piegare
```

    prosa → lingua → manifest → colophon → schermo → stampa → imposizione

I passi **non hanno lo stesso peso**, ed è deliberato: `prosa` e `lingua`
**misurano e non bloccano**; `manifest` e `schermo` sono **guasti duri** e fermano
la catena (compilare da un manifest non valido produce un artefatto sbagliato con
l'aria di essere andato bene); `stampa` e `imposizione` **degradano pulito** se
il modulo `typst` o `pdfimpose` mancano. `--solo <passo>` e `--salta <passo>` per rifarne uno.

⚠️ In coda, **comunque sia andata**, il comando ti ricorda il cancello d'uscita
§7 di [`GUIDA-CONDIVISIONE-IP.md`](GUIDA-CONDIVISIONE-IP.md). Non è
automatizzabile e non finge di esserlo — ma è il momento in cui un volume sta per
uscire.

---

### 0.1 Le tre opzioni che si dimenticano sempre

```bash
# il volume da stampare in casa: niente fondo avorio, cioè niente cartuccia bruciata
python3 scripts/export_booklet_typst.py MANIFEST.json --all --carta bianca

# il libretto: composto in A5 a una colonna, poi imposto due pagine per foglio
python3 scripts/export_booklet_typst.py MANIFEST.json --all --formato a5
python3 scripts/dm.py volume MANIFEST.json --stampa --imposto

# un booklet HTML leggero (57 KB invece di 460): senza caratteri incorporati,
# ma su una macchina senza EB Garamond cambia faccia
python3 scripts/build_booklet_html.py MANIFEST.json --no-font-embed
```

## 1. Cosa produce la pipeline

→ Ora in [RIFERIMENTO-BOOKLET §1](../reference/RIFERIMENTO-BOOKLET.md#1-cosa-produce-la-pipeline), che è un riferimento.

---

## 2. Prerequisiti

| Cosa | Serve per | Obbligatorio? |
|---|---|---|
| **Python 3.13+** | tutto (gli script sono stdlib-only) | ✅ sì |
| **Chromium / Google Chrome** | i PDF | solo per `--pdf` / `--pdf-all` |
| **Pillow** (`pip install pillow`) | ricomprimere le immagini > 600 KB nell'HTML | opzionale (senza, l'immagine viene incorporata così com'è) |
| **Docker / Podman** | editor Homebrewery, o PDF senza installare un browser | opzionale |

### Installare Chromium (solo se vuoi i PDF)

```bash
# Debian / Ubuntu / Mint
sudo apt install chromium            # (su alcune versioni: chromium-browser)

# Fedora
sudo dnf install chromium

# Arch
sudo pacman -S chromium

# macOS (Homebrew)
brew install --cask chromium         # va bene anche Google Chrome già installato

# Windows: va bene Chrome o Edge già installati — indica il percorso:
#   set BOOKLET_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe
```

Lo script cerca il browser in quest'ordine: variabile **`$BOOKLET_CHROME`** →
`chromium`, `chromium-browser`, `google-chrome`, `google-chrome-stable`,
`chrome` nel PATH → `/opt/pw-browsers/chromium` (installazioni Playwright).

> **Distribuzione immutabile** (Bazzite, Silverblue…) o non vuoi installare
> nulla? Salta l'installazione e usa il **container PDF** del §7.2.

---

## 3. Il manifest, campo per campo

→ Ora in [RIFERIMENTO-BOOKLET §3](../reference/RIFERIMENTO-BOOKLET.md#3-il-manifest-campo-per-campo), che è un riferimento.

---

## 4. Ricetta per una nuova sessione

Struttura consigliata (esemplare vivo: `07_il Portale Della Forgia Eterna/homebrew/sessione-terros/`):

```
<arco>/homebrew/sessione-<nome>/
├── 00-INTRO-DOVE-SIAMO.md            read-aloud d'apertura + fotografia della vigilia
├── 01-REGIA-SESSIONE.md              ⚠ DM: ordine di gioco, canone giocato, cosa stampare
├── 02-HINT-<PG>.md … 05-ECHI-<PG>.md ✉ una pagina per PG (semi, non istruzioni — ADR-0013 §3-ter)
├── 06-TEASER-GIOCATORI.md            ✉ «il cammino fin qui» + invito evocativo
├── <NOME>-BOOKLET.manifest.json      booklet DM (contiene tutto)
└── <NOME>-GRUPPO-CAMMINO.manifest.json   file unico da inviare al gruppo
```

**Ordine di scrittura** (ADR-0013 §3-bis): prima gli **hint per-PG**, poi il
**teaser** — e poi togli dal teaser tutto ciò che è già in un hint.

Il manifest del **file gruppo** è minimale: copertina + intro nella stessa
scheda, nessun capitolo.

```json
{
  "brand": "RUMBLING STONE · …", "title": "L'Ultima Porta",
  "subtitle": "Il cammino fin qui · e ciò che vi aspetta oltre la soglia",
  "banner": "PER IL GRUPPO", "footer": "L'Ultima Porta",
  "player_footer": "L'Ultima Porta", "cover_tag": "player",
  "cover_image": "../../Immagini/<tavola>.webp",
  "intro_md": "06-TEASER-GIOCATORI.md",
  "out": "<NOME>-GRUPPO-CAMMINO.html",
  "chapters": []
}
```

---

## 5. Generare

```bash
# HTML autonomo (default)
python3 scripts/dm.py booklet <manifest>

# sorgente Homebrewery V3 (.hb.md) — per l'editor a due pannelli
python3 scripts/dm.py booklet <manifest> --format hb

# entrambi
python3 scripts/dm.py booklet <manifest> --format both

# + PDF A4 delle sole pagine ✉ player (quelle da inviare)
python3 scripts/dm.py booklet <manifest> --pdf

# + PDF A4 di TUTTE le schede (copertina, regia, master…)
python3 scripts/dm.py booklet <manifest> --pdf-all
```

Export selettivo (script diretto):

```bash
# quali schede esistono e come si chiamano
python3 scripts/export_booklet_pdf.py <manifest> --list

# solo alcune schede
python3 scripts/export_booklet_pdf.py <manifest> --pane c2 c4

# cartella di output diversa / browser specifico
python3 scripts/export_booklet_pdf.py <manifest> --outdir /tmp/pdf --browser /usr/bin/chromium
```

---

## 6. PDF senza script: dal browser

Funziona sempre, anche senza Chromium installato a riga di comando:

1. apri il file `.html` nel browser;
2. clicca la **scheda** che ti serve (o usa il link diretto `file.html#c4`);
3. premi **«🖨 Salva PDF»** in basso a destra (o `Ctrl+P`);
4. destinazione **«Salva come PDF»**, formato **A4**, margini **Nessuno**,
   **«Grafica di sfondo» attiva**.

In stampa spariscono da soli testata, barra dei tab e bottone: esce **solo la
scheda aperta**, a piena pergamena.

---

## 7. Container — quando servono (e quando no)

### 7.1 Editor Homebrewery self-hosted — per modificare l'impaginazione

Serve solo se vuoi lavorare i `.hb.md` nell'editor a due pannelli con
anteprima live. Guida e comandi ufficiali:
[`scripts/homebrew-local/README.md`](../../scripts/homebrew-local/README.md).

```bash
python3 scripts/dm.py hype docker        # su http://localhost:8000
python3 scripts/dm.py hype docker-stop
```

### 7.2 Container PDF — per non installare Chromium

Serve solo su distro immutabili o se non vuoi installare un browser.
**Sui sistemi normali non serve**: installa chromium (§2) e usa `--pdf`.

```bash
# build (solo la prima volta) + export, stessa resa dello script nativo
scripts/booklet-container/export-pdf-docker.sh <manifest.json>
scripts/booklet-container/export-pdf-docker.sh <manifest.json> --all
scripts/booklet-container/export-pdf-docker.sh <manifest.json> --list
```

Funziona con **docker o podman** (rilevati da soli; forzabili con
`CONTAINER_RUNTIME=podman`). Il repo viene montato in `/repo`, i PDF escono
nella solita cartella `pdf/` con i permessi del tuo utente.

> ⚠️ **Stato di collaudo**: Dockerfile e wrapper sono scritti con comandi
> standard (Debian stable + pacchetto `chromium` della distro) ma **non sono
> stati eseguiti end-to-end** nell'ambiente di sviluppo, dove il daemon
> Docker non è disponibile. Al primo uso reale, segnala qualsiasi intoppo.

---

## 8. Se qualcosa non funziona

| Sintomo | Causa e rimedio |
|---|---|
| `ERRORE: nessun Chromium/Chrome trovato` | non è installato o non è nel PATH → §2, oppure `BOOKLET_CHROME=/percorso/al/browser`, oppure container §7.2, oppure stampa dal browser §6 |
| `ERRORE: HTML non trovato` | stai esportando i PDF prima di generare l'HTML → lancia `dm.py booklet <manifest>` (o usa `--pdf`, che fa entrambi) |
| Riquadro tratteggiato «la tavola apparirà qui…» | il file immagine citato non esiste a quel percorso → controlla `cover_image` / il link nel markdown (i percorsi sono relativi alla cartella del **capitolo**) |
| HTML enorme (decine di MB) | immagini grandi non ricompresse → `pip install pillow` e rigenera (sopra i 600 KB vengono convertite in JPEG per l'embed; nel repo restano gli originali) |
| PDF con la pergamena bianca | nella stampa manuale manca **«Grafica di sfondo»** → attivala (lo script headless la attiva da solo) |
| Mappe ASCII tagliate sul lato | in stampa i blocchi `pre` si riducono da soli; se resta tagliata, la mappa è troppo larga: accorcia le righe nel master |
| Emoji delle mappe non renderizzate nel container | manca il font emoji → l'immagine include `fonts-noto-color-emoji`; se hai personalizzato il Dockerfile, rimettilo |
| `git status` mostra i PDF | non dovrebbe: `*.pdf` è gitignored. Se compaiono, hai un `.gitignore` modificato |
| `⚠ non è PDF/UA-1` dopo `export_booklet_typst` | il volume c'è, ma un lettore di schermo lo legge peggio (ADR-0129). Il motivo è nella riga dopo: `missing alt text` = un'immagine del master con `![](…)` senza testo fra le parentesi quadre, da scrivere; un altro motivo va riportato come difetto del tema |

---

## 8-bis. La tipografia: cosa fa il tema da solo, e cosa puoi chiedergli

→ Ora in [RIFERIMENTO-BOOKLET §8-bis](../reference/RIFERIMENTO-BOOKLET.md#8-bis-la-tipografia-cosa-fa-il-tema-da-solo-e-cosa-puoi-chiedergli), che è un riferimento.

---

## 9. Checklist di consegna (prima della sessione)

- [ ] Aggiornato il **canone giocato** nei master (blocchi `✅ CANONE GIOCATO (DM data)`) e la tabella «fotografia della vigilia» nella regia
- [ ] Scritti prima gli **hint per-PG**, poi il **teaser**, poi tolte le ripetizioni (ADR-0013 §3-bis)
- [ ] Verificato che nel materiale ✉ non compaiano **nome dello scontro, CD, pf, clock** — nemmeno nei piè di pagina (`player_footer`)
- [ ] `python3 scripts/dm.py booklet <gruppo> --pdf` → **un** file per la chat di gruppo
- [ ] `python3 scripts/dm.py booklet <booklet DM> --format both --pdf-all` → hint `pg-` (uno a testa, in privato) + schede `dm-` per te
- [ ] `python3 scripts/validate_modules.py` verde se hai toccato un master
- [ ] `python3 scripts/misura_standard_tavolo.py --manifest <booklet DM>`: chi si incontra ha scheda, riquadro e mappa nel capitolo
- [ ] `python3 scripts/misura_distanza_pagine.py --volume --manifest <booklet DM>`: le misure S1-S5 contro le soglie degli AP di riferimento (ADR-0122; avvisano, non bloccano)
- [ ] Letto il booklet da DM, scena per scena: i validatori verdi non bastano (serata del 2026-11-02)

---

## 10. Dove sta scritto cosa

| Domanda | Documento |
|---|---|
| Cosa fa ogni script, con quali parametri | [`scripts/README-automation.md`](../../scripts/README-automation.md) |
| Perché i booklet sono fatti così (struttura, anti-spoiler, PDF) | [ADR-0013](../../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md) |
| Perché ogni scena ha la sua regia e le stanze si descrivono così | [ADR-0014](../../plans/adr/ADR-0014-regia-sensoriale-obbligatoria.md) |
| Editor Homebrewery in locale (nativo o Docker) | [`scripts/homebrew-local/README.md`](../../scripts/homebrew-local/README.md) |
| Ciclo di sessione completo (recap, brief, state.md) | skill `rumblingstone-automation` + [`campaign/DM-CAMPAIGN-PLAYBOOK.md`](../../campaign/DM-CAMPAIGN-PLAYBOOK.md) |
| Contratto macchina dei tool (argomenti, input/output, exit code) | [`docs/tools/README.md`](../tools/README.md) |
