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

- GPU **NVIDIA** con il driver proprietario sull'host (`nvidia-smi` risponde).
- **Distrobox** e **Podman**: preinstallati su Bazzite; su **Debian/Ubuntu**
  `sudo apt install distrobox podman` (e il driver: pacchetto `nvidia-driver`).
- Spazio disco: **~15 GB** per ComfyUI, PyTorch CUDA e il checkpoint SDXL. Gli
  script lo controllano e si fermano se manca. Se `/home` è piccolo, metti
  tutto su un altro disco **prima** del setup, e tienilo per ogni comando:

  ```bash
  export COMFYUI_DIR=/srv/comfyui     # vale per setup, scarica-pesi, start, stop
  ```

- VRAM: 8 GB stanno larghi; con **4 GB** (la RTX A2000 misurata il 2026-10-08)
  SDXL con `--lowvram` gira, lento. FLUX non ci sta.

> **Container, non macchina virtuale.** Distrobox usa la GPU dell'host
> direttamente. Una VM di virt-manager o di Vagrant vedrebbe la GPU solo con il
> passthrough PCI (IOMMU e una seconda GPU per l'host), che su un portatile con
> una sola scheda NVIDIA non si fa. Le VM vanno bene per le parti senza GPU.

Verifica rapida sull'host:

```bash
nvidia-smi            # deve elencare la tua GPU
distrobox version     # deve rispondere
df -h /home /srv      # dove c'è posto
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
   `$COMFYUI_DIR`, se l'hai impostata, altrimenti in
   `scripts/comfyui-local/ComfyUI/` (gitignorato: è software di terzi,
   non contenuto di campagna);
4. crea un virtualenv e installa **PyTorch CUDA** + `requirements.txt` di
   ComfyUI (indice ufficiale PyTorch), poi stampa se torch vede la GPU.
   Se stampa `False`, il driver NVIDIA non arriva nel box: fermati lì.

Distrobox condivide col box la home, non il resto del disco. Se `COMFYUI_DIR`
sta fuori dalla home (`/srv/comfyui`), lo script la monta nel box; se un box
creato prima non la vede, lo ricrea.

Prima di partire controlla lo spazio (passo 0). Con `COMFYUI_FORZA=1` procede
lo stesso.

### A.2 — Avvio / arresto

```bash
scripts/comfyui-local/start.sh     # entra nel box e lancia ComfyUI (--lowvram)
# → apri http://127.0.0.1:8188
scripts/comfyui-local/stop.sh      # ferma il box (i modelli restano su disco)
```

> **8 GB di VRAM (es. RTX 4050)**: `start.sh` passa `--lowvram` a ComfyUI. Per
> SDXL su 8 GB va bene; per Flux-dev valuta `--lowvram`/quantizzazioni o resta
> su SDXL. Vedi le note VRAM nel README di ComfyUI.

### A.3 — Pesi (una tantum, con lo script)

ComfyUI non scarica i pesi da solo. Lo fa questo script, per il checkpoint
**SDXL 1.0 base** (OpenRAIL++-M, ammesso da ADR-0019):

```bash
scripts/comfyui-local/scarica-pesi.sh
```

Legge da Hugging Face l'impronta sha256 che il repository pubblica per il file,
scarica ~6,9 GB in `models/checkpoints/` (riprende se si interrompe) e
controlla che l'impronta coincida. Alla fine stampa lo sha256: incollalo nella
chat, entra nella provenienza delle immagini.

Per le **icone degli oggetti** basta il checkpoint. Il ControlNet
(`models/controlnet/`, lineart o canny per SDXL) serve solo alla hero map, e
quello si scarica a mano: vedi `hero-map-comfyui.md`.

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
  `rm -rf "${COMFYUI_DIR:-scripts/comfyui-local/ComfyUI}"` rimuove clone e modelli. L'host
  immutabile resta intatto (non è mai stato modificato).
