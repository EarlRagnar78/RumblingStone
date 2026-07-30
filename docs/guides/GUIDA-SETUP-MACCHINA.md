# Guida completa — preparare una macchina nuova (o un secondo DM)

> **Cosa copre**: dal repo appena clonato a «funziona tutto», passo per
> passo. Cosa serve davvero e cosa è opzionale, come si attivano le skill
> per gli agenti, come si prepara il flusso di sessione con il branch di
> gruppo, e come si verifica di non aver dimenticato niente.
>
> **Tempo**: ~10 minuti per il minimo indispensabile, ~25 con tutti gli
> extra (PDF, container, secondo gruppo).

---

## 0. TL;DR — il minimo per lavorare

```bash
git clone <url-del-repo> RumblingStone && cd RumblingStone
python3 --version                     # serve 3.11 o superiore
python3 scripts/dm.py doctor          # diagnosi: dice cosa manca
./scripts/build-skills.sh             # se usi agenti AI (Claude Code, Cursor, …)
```

Se `doctor` chiude con **`tutto ok`**, puoi già preparare sessioni,
generare booklet HTML, renderizzare mappe e usare il bestiario.

---

## 1. Cosa serve davvero (e cosa no)

| Componente | Serve per | Obbligatorio? |
|---|---|---|
| **Python 3.11+** | tutto: gli script sono **stdlib-only** (nessun `pip install`, nessun `requirements.txt`) | ✅ sì |
| **git** | clonare, versionare, branch di gruppo | ✅ sì |
| **Chromium / Chrome** | PDF dei booklet, PNG delle mappe | solo per quegli export |
| **Pillow** (`pip install pillow`) | ricomprimere immagini grandi nell'HTML dei booklet | opzionale |
| **pandoc + xelatex** | `dm.py recap --pdf` (il recap in PDF «sobrio») | opzionale |
| **Docker / Podman** | editor Homebrewery, container PDF, ComfyUI | opzionale |
| **shellcheck** | lint degli script shell (in CI è non bloccante) | opzionale |

> Nota: `doctor` segnala pandoc/xelatex assenti come **`○`** (pallino, non
> errore). È normale: sono opzionali e non impediscono nulla del flusso
> principale.

---

## 2. Passo 1 — Clonare e verificare

```bash
git clone <url-del-repo> RumblingStone
cd RumblingStone
python3 scripts/dm.py doctor
```

`doctor` controlla, nell'ordine: versione di Python, presenza di
`campaign/state.md`, `campaign/sessions/`, `campaign/templates/`,
`scripts/map_templates/`, `plans/INDEX.md`, **freschezza del catalogo
mostri**, e lo stato del flusso branch-di-gruppo.

Legenda dell'output: **✓** a posto · **○** opzionale o non ancora attivato
· **✗** da sistemare.

---

## 3. Passo 2 — Skill per gli agenti AI

Le skill vivono in `skills/` (versionate). Ogni agente però le legge da un
percorso suo: i **mirror per-agente NON sono committati**, si generano in
locale.

```bash
./scripts/build-skills.sh     # costruisce i pacchetti e li installa nei path per-agente
./scripts/sync-skills.sh      # ri-sincronizza soltanto (più veloce, dopo un pull)
```

Equivalente dalla CLI: `python3 scripts/dm.py skills build` /
`python3 scripts/dm.py skills sync`.

### Se NON usi Claude Code

Claude Code risincronizza da solo a ogni avvio di sessione (hook
`.claude/hooks/session-start.sh`). **Gli altri agenti** (Cursor, Windsurf,
Codex, Copilot…) no: installa l'hook git che lo fa dopo ogni `git pull`.

```bash
./scripts/install-git-hooks.sh    # installa un hook post-merge, non blocca mai git
```

> Verifica: `python3 scripts/validate_skills.py` deve essere verde.

---

## 4. Passo 3 — Il flusso di sessione (branch di gruppo)

Le scritture di canone non si fanno su `main` e non si fanno a mano: c'è un
**branch per gruppo di gioco** (ADR-0007). Se questa macchina serve a
condurre partite, attivalo:

```bash
# crea/attiva il branch del gruppo e il file campaign/group.yaml
python3 scripts/dm.py session branch --group <nome-gruppo>

# inserisce i marker auto: in state.md (idempotente: si può rilanciare)
python3 scripts/state_apply.py --migrate --commit

# controllo
python3 scripts/dm.py session status
```

Finché non lo fai, `doctor` mostra due **○** («`campaign/group.yaml`
assente», «marker `auto:` assenti»): non è un errore — significa solo che
il flusso automatico di chiusura sessione non è ancora attivo su questa
copia.

**Un secondo gruppo che rigioca la campagna da capo**: `scripts/new-campaign-group.sh`
(vedi `campaign/DM-CAMPAIGN-PLAYBOOK.md` §7 — «Reset per nuovo gruppo»).

---

## 5. Passo 4 — Gli extra, quando ti servono

### PDF dei booklet e PNG delle mappe → serve Chromium

```bash
sudo apt install chromium      # Debian/Ubuntu   (Fedora: dnf, Arch: pacman)
brew install --cask chromium   # macOS
# Windows: usa Chrome/Edge già installati →  set BOOKLET_CHROME=C:\...\chrome.exe
```

Dettagli e alternative (container, stampa dal browser):
[GUIDA-BOOKLET-E-PDF §2 e §7](GUIDA-BOOKLET-E-PDF.md).

### Immagini grandi nei booklet → Pillow

```bash
pip install pillow    # opzionale: senza, le immagini vengono incorporate non compresse
```

### Recap in PDF «sobrio» → pandoc

```bash
sudo apt install pandoc texlive-xetex    # solo se usi `dm.py recap --pdf`
```

### Container

| Cosa | Dove |
|---|---|
| Editor Homebrewery (due pannelli, `localhost:8000`) | [`scripts/homebrew-local/README.md`](../../scripts/homebrew-local/README.md) |
| PDF senza installare un browser (distro immutabili) | [`scripts/booklet-container/README.md`](../../scripts/booklet-container/README.md) |
| Hero map con GPU | [`scripts/comfyui-local/README.md`](../../scripts/comfyui-local/README.md) |

---

## 6. Passo 5 — Verifica finale

```bash
python3 scripts/dm.py doctor                  # ✓ ovunque (i ○ opzionali vanno bene)
python3 -m pytest scripts/tests -q            # la suite del repo
python3 scripts/validate_skills.py            # skill ben formate
python3 scripts/validate_maps.py              # SVG in sync coi master
python3 scripts/validate_bestiario.py         # libreria mostri conforme
python3 scripts/validate_modules.py           # master d'arco conformi
python3 scripts/tools_manifest.py --check     # contratto dei tool allineato
```

Sono **gli stessi controlli della CI**: se passano qui, la tua PR non
diventerà rossa per motivi ambientali.

---

## 7. Prova che tutto funziona (5 minuti)

```bash
# 1. proposte di incontro (non scrive niente)
python3 scripts/dm.py prep --el 13 --env underground

# 2. genera un booklet esistente in HTML
python3 scripts/dm.py booklet "07_il Portale Della Forgia Eterna/homebrew/sessione-terros/ARC07-GRUPPO-CAMMINO.manifest.json"

# 3. ri-renderizza una mappa e verifica che resti in sync
python3 scripts/dm.py maps validate
```

Se i tre comandi girano, la macchina è pronta.

---

## 8. Se qualcosa non funziona

| Sintomo | Causa e rimedio |
|---|---|
| `python3: command not found` o versione < 3.11 | installa Python 3.11+; su Debian/Ubuntu `sudo apt install python3` |
| `doctor` segnala **✗ monster_catalog** o «catalogo vecchio» | `python3 scripts/build_monster_catalog.py` |
| Un agente non «vede» le skill aggiornate | `./scripts/sync-skills.sh` (e, se non usi Claude Code, `./scripts/install-git-hooks.sh` una volta sola) |
| `validate_maps` rosso appena clonato | qualcuno ha committato un SVG disallineato: `python3 scripts/dm.py maps render <master>` e ricommitta ([GUIDA-MAPPE §6](GUIDA-MAPPE.md)) |
| `ERRORE: nessun Chromium/Chrome trovato` | vedi §5, o usa il container, o stampa dal browser |
| `git push` rifiutato sul branch di gruppo | il flusso ADR-0007 protegge `main`: lavora sul branch del gruppo (`dm.py session branch`) |
| I PDF compaiono in `git status` | non dovrebbero: `*.pdf` è gitignored — controlla di non aver modificato `.gitignore` |

---

## 9. Dopo il setup: dove andare

| Vuoi… | Documento |
|---|---|
| Condurre la tua prima sessione | [`campaign/DM-QUICKSTART-NUOVI-DM.md`](../../campaign/DM-QUICKSTART-NUOVI-DM.md) |
| Il ciclo completo prima/durante/dopo | [`campaign/DM-CAMPAIGN-PLAYBOOK.md`](../../campaign/DM-CAMPAIGN-PLAYBOOK.md) |
| Fare booklet e PDF | [`GUIDA-BOOKLET-E-PDF.md`](GUIDA-BOOKLET-E-PDF.md) |
| Fare mappe | [`GUIDA-MAPPE.md`](GUIDA-MAPPE.md) |
| Aggiungere mostri/PNG/villain | [`GUIDA-BESTIARIO.md`](GUIDA-BESTIARIO.md) |
| Capire regole e convenzioni del repo | [`AGENTS.md`](../../AGENTS.md) |
| Sapere cosa fa ogni script | [`scripts/README-automation.md`](../../scripts/README-automation.md) |
