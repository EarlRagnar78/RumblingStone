# ComfyUI locale in container su Bazzite (hero map · Modalità 2 cinematografica)

> **Cosa ottieni**: un'istanza locale di **ComfyUI** (open source, GPU NVIDIA)
> su `http://127.0.0.1:8188`, **isolata in un container** così l'OS immutabile
> di **Bazzite** (Fedora Atomic / `rpm-ostree`) **non viene toccato**: niente
> pacchetti stratificati sul sistema, niente `pip install` sull'host. Serve
> **solo** per la passata pittorica opzionale ("hero map", Modalità 2) — vedi
> `skills/rumblingstone-mapmaking/references/hero-map-comfyui.md`. Il master
> resta la griglia emoji; l'SVG deterministico resta il canone in CI.
>
> **Perché in container (e non nativo)**: Bazzite è immutabile — il modo
> pulito di installare toolchain di sviluppo è dentro **Distrobox** (Podman)
> o **Docker/Podman**, non con `rpm-ostree install`. Le GPU NVIDIA di Bazzite
> sono già configurate sull'host e vengono esposte al container.
>
> **Fonti ufficiali** (recuperate il 2026-07-19 — comandi standard, non
> inventati; verifica sempre il link per la tua versione):
> - ComfyUI: <https://github.com/comfyanonymous/ComfyUI> (sezione *Manual Install* / *Running*)
> - Distrobox: <https://distrobox.it/> · `distrobox create --nvidia`
>   <https://github.com/89luca89/distrobox/blob/main/docs/usage/distrobox-create.md>
> - Bazzite (immutabile, Distrobox preinstallato): <https://docs.bazzite.gg/>
> - PyTorch (indice CUDA per `pip`): <https://pytorch.org/get-started/locally/>

---

## Prerequisiti

- **Bazzite** con GPU NVIDIA funzionante sull'host (`nvidia-smi` risponde).
- **Distrobox** (preinstallato su Bazzite) e **Podman** (idem), *oppure*
  Docker/Podman se preferisci la Via B.
- Spazio disco: ~10–15 GB per un checkpoint SDXL + i modelli ControlNet.

Verifica rapida sull'host:

```bash
nvidia-smi            # deve elencare la tua GPU (es. RTX 4050)
distrobox version     # deve rispondere
```

---

## Via A — Distrobox (consigliata su Bazzite: un box isolato con GPU)

Distrobox crea un container che **condivide home e GPU** con l'host ma tiene
tutta la toolchain (Python, PyTorch, ComfyUI) fuori dal sistema immutabile.

### A.1 — Setup (una tantum), wrapper di questo repo

```bash
scripts/comfyui-local/setup-distrobox.sh
```

Fa, nell'ordine (tutti passi standard Distrobox + ComfyUI):

1. `distrobox create --name comfyui --image ubuntu:24.04 --nvidia --yes`
   — crea il box con l'integrazione driver NVIDIA dell'host (flag `--nvidia`);
2. dentro il box: installa `git`, `python3-venv`, `python3-pip`;
3. clona `https://github.com/comfyanonymous/ComfyUI.git` in
   `scripts/comfyui-local/ComfyUI/` (gitignorato: è software di terzi,
   non contenuto di campagna);
4. crea un virtualenv e installa **PyTorch CUDA** + `requirements.txt` di
   ComfyUI (indice ufficiale PyTorch).

### A.2 — Avvio / arresto

```bash
scripts/comfyui-local/start.sh     # entra nel box e lancia ComfyUI (--lowvram)
# → apri http://127.0.0.1:8188
scripts/comfyui-local/stop.sh      # ferma il box (i modelli restano su disco)
```

> **8 GB di VRAM (es. RTX 4050)**: `start.sh` passa `--lowvram` a ComfyUI. Per
> SDXL su 8 GB va bene; per Flux-dev valuta `--lowvram`/quantizzazioni o resta
> su SDXL. Vedi le note VRAM nel README di ComfyUI.

### A.3 — Modelli (una tantum, scaricati a mano)

ComfyUI non scarica i pesi da solo. Metti i file in
`scripts/comfyui-local/ComfyUI/models/`:

- `checkpoints/` → un checkpoint **aperto** (SDXL base o un fine-tune permissivo);
- `controlnet/` → un modello **ControlNet lineart/canny** per SDXL.

Solo pesi con licenza d'uso compatibile (SDXL/Flux-dev sono aperti). Vedi i
vincoli IP in `hero-map-comfyui.md` (§"Cosa NON fare") e in
`plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md`.

---

## Via B — Docker/Podman Compose (alternativa)

Se preferisci un'immagine container gestita a parte (non condivisa con la
home), usa un `compose` con una community image di ComfyUI e il runtime NVIDIA
(`nvidia-container-toolkit`, già presente su Bazzite). Schema minimo:

```yaml
# docker-compose.yml (adatta l'immagine alla community image che scegli)
services:
  comfyui:
    image: <community/comfyui-image>
    ports: ["127.0.0.1:8188:8188"]
    deploy:
      resources:
        reservations:
          devices: [{ driver: nvidia, count: 1, capabilities: [gpu] }]
    volumes:
      - ./ComfyUI/models:/app/models
      - ./ComfyUI/output:/app/output
```

```bash
podman compose up -d      # oppure: docker compose up -d
podman compose down
```

> Le immagini ComfyUI su registry sono **community**, non ufficiali: verifica
> Dockerfile e licenza prima di usarle. La Via A (Distrobox + repo ufficiale)
> è la più trasparente.

---

## Come si collega alla pipeline mappe

1. Genera/rende la mappa deterministica del repo ed esporta il PNG hi-res:
   `python3 scripts/export_map_png.py rendered/<mappa>.svg --scale 2`
2. Avvia ComfyUI (`start.sh`) e usa **img2img + ControlNet lineart** con quel
   PNG come input (la geometria resta vincolata: stanze e coordinate non si
   spostano). Prompt e parametri: `hero-map-comfyui.md`.
3. Per pilotare ComfyUI **da Claude** invece che dalla GUI, registra un
   server MCP ComfyUI (vedi `hero-map-comfyui.md`, §Setup).
4. Salva l'output in `rendered/hero/<slug>.png` (fuori da `validate_maps.py`:
   è un livello di presentazione, non il master).

## Note

- Nessun file di questa cartella viene eseguito in CI: `ComfyUI/` è
  gitignorato e i pesi non entrano mai nel repo.
- Disinstallazione pulita: `distrobox rm comfyui --force` rimuove il box;
  `rm -rf scripts/comfyui-local/ComfyUI` rimuove clone e modelli. L'host
  immutabile resta intatto (non è mai stato modificato).
