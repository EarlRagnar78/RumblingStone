# Guida completa — dai master ai booklet e ai PDF in mano ai giocatori

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

## 1. Cosa produce la pipeline

```
   master markdown            manifest JSON              artefatti generati
 (ARC*-DEF-*, hint,   ──▶  (*.manifest.json)  ──▶   ┌── .html   pagina autonoma, immagini incorporate
  teaser, regia…)           elenca i capitoli        ├── .hb.md  sorgente Homebrewery V3 (editor 2 pannelli)
   ← LA VERITÀ                e i metadati           └── pdf/*.pdf  A4, una scheda per file
```

**I markdown sono i master** (ADR-0003): HTML, `.hb.md` e PDF sono
**artefatti rigenerabili**. I PDF non stanno nel repo (`*.pdf` è in
`.gitignore`): si rifanno in un comando quando servono.

| Output | A cosa serve | Serve un browser? |
|---|---|---|
| `.html` | leggere/sfogliare a schermo, condividere un file solo | no |
| `.hb.md` | modificare l'impaginazione nell'editor Homebrewery self-hosted | no (serve il container per l'editor) |
| `pdf/*.pdf` | stampare, o inviare una pagina sola a un giocatore | **sì** (Chromium headless) |

### 1.1 Il soffitto di questa catena — dichiarato, così non lo si cerca invano

Questa pipeline arriva fin dove arriva **il browser**, e Chromium impagina pagine
web, non libri. Restano fuori, e **nessuna quantità di CSS li recupera**:

- il controllo su **vedove e orfane**;
- la **crenatura** fine e la spaziatura ottica;
- un **indice** che diventi una struttura di segnalibri degna;
- i **font embedded** — oggi è Georgia, un font di sistema: su una macchina che
  non ce l'ha il PDF cambia faccia;
- il **volume unico** invece di un file per capitolo.

Non sono difetti del codice: sono il soffitto dello strumento. La strada per
superarlo — **un secondo binario, Typst, che affianca questa catena senza
sostituirla** — sta in
[ADR-0020](../../plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md),
oggi **una proposta** in attesa del via libera del DM sulla dipendenza esterna.
Finché è così, quello che leggi qui sotto è tutta la verità operativa.

---

## 2. Prerequisiti

| Cosa | Serve per | Obbligatorio? |
|---|---|---|
| **Python 3.11+** | tutto (gli script sono stdlib-only) | ✅ sì |
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

Un booklet è descritto da un file `*.manifest.json` messo **accanto ai
capitoli**. Tutti i percorsi sono relativi alla cartella del manifest.

```json
{
  "brand":         "RUMBLING STONE · IL PORTALE DELLA FORGIA ETERNA",
  "title":         "Lo Scontro con Terros l'Antico",
  "subtitle":      "Il Piano della Terra · lo Smeraldo della Forza",
  "banner":        "BOOKLET DI SESSIONE",
  "meta":          "riga piccola in fondo alla copertina",
  "header":        "riga descrittiva sotto il titolo della pagina",
  "footer":        "Lo Scontro con Terros",
  "player_footer": "L'Ultima Porta",
  "cover_tag":     "player",
  "cover_image":   "../../Immagini/camera-nodo-terra.webp",
  "intro_md":      "00-INTRO-DOVE-SIAMO.md",
  "out":           "ARC07-SESSIONE-TERROS-BOOKLET.html",
  "chapters": [
    {"title": "I · Regia della Sessione", "file": "01-REGIA-SESSIONE.md", "tag": "dm"},
    {"title": "✉ Hint — Thorik",          "file": "02-HINT-THORIK.md",    "tag": "player"}
  ]
}
```

| Campo | Cosa fa |
|---|---|
| `brand` / `title` / `subtitle` / `banner` / `meta` | la copertina |
| `header` | riga sotto il titolo nella pagina HTML |
| `footer` | piè di pagina delle schede **DM** |
| `player_footer` | piè di pagina delle schede **✉ player** — **titolo evocativo, MAI quello reale** (ADR-0013 §3: un handout che in fondo dice «Lo Scontro con Terros» brucia l'aspettativa) |
| `cover_tag` | `"player"` se la copertina stessa è il deliverable da inviare (file del gruppo): entra nell'export player e il PDF prende il nome dal `title` |
| `cover_image` | immagine di copertina (SVG inline, oppure PNG/JPG/WEBP incorporate) |
| `intro_md` | markdown mostrato **nella stessa scheda** della copertina |
| `out` | nome del file HTML (i `.hb.md` e i PDF derivano da questo) |
| `chapters[]` | `title` = etichetta del tab · `file` = markdown · `tag` = `dm` (⚠ SOLO DM) / `player` (✉ HANDOUT) / assente |

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

---

## 9. Checklist di consegna (prima della sessione)

- [ ] Aggiornato il **canone giocato** nei master (blocchi `✅ CANONE GIOCATO (DM data)`) e la tabella «fotografia della vigilia» nella regia
- [ ] Scritti prima gli **hint per-PG**, poi il **teaser**, poi tolte le ripetizioni (ADR-0013 §3-bis)
- [ ] Verificato che nel materiale ✉ non compaiano **nome dello scontro, CD, pf, clock** — nemmeno nei piè di pagina (`player_footer`)
- [ ] `python3 scripts/dm.py booklet <gruppo> --pdf` → **un** file per la chat di gruppo
- [ ] `python3 scripts/dm.py booklet <booklet DM> --format both --pdf-all` → hint `pg-` (uno a testa, in privato) + schede `dm-` per te
- [ ] `python3 scripts/validate_modules.py` verde se hai toccato un master

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
