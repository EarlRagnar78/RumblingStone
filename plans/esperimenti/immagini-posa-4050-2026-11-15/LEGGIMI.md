# Immagini in posa sulla RTX 4050 (laboratorio, 2026-11-15)

Copia della pipeline del 29/10 (thread «Immagini dei personaggi in posa con l'AI»,
`/mnt/project-files/immagini-personaggi/pipeline-2026-10-29/kaggle/dati/`), messa nel
repo perché il portatile del DM non vede i file del progetto. Si lancia con
`scripts/prove-4050/immagini.sh`; i passi sono in
[GUIDA-PROVE-PORTATILE-4050](../../../docs/how-to/GUIDA-PROVE-PORTATILE-4050.md) §3.

È una prova, non un'adozione: niente generazione in CI, nessuna immagine prodotta entra
nel repo, e le decisioni D1-D4 di quel thread restano al DM.

## Cosa cambia rispetto al 29/10

Quattro manopole per i 6 GB della 4050, tutte da variabili d'ambiente e spente di serie,
così su Kaggle o su una GPU da 10 GB la pipeline fa quello che faceva:

| Variabile | File | Effetto |
|---|---|---|
| `RS_COMFY_ARGS` | `esegui_gpu.py` | argomenti in più per ComfyUI; `immagini.sh` passa `--lowvram` sul profilo `gpu` e niente sul profilo leggero. Con `--cpu` le opzioni di VRAM si tolgono: ComfyUI le rifiuta insieme |
| `RS_COMFY_DEVICE=gpu` | `esegui_gpu.py` | il profilo leggero `cpu` (SD1.5 + LCM) gira sulla GPU invece che con `--cpu`; `immagini.sh` lo imposta sempre |
| `RS_LIBERA=1` | `pipeline_scena.py` | svuota ComfyUI prima di ogni misura anche sul profilo `gpu` (prima solo su `cpu`) |
| `RS_VLM_DEVICE`, `RS_VLM_GPU` | `misura_immagini.py` | dove va il giudice Qwen3-VL-4B: `auto` con `max_memory` (4 GiB in GPU, il resto in RAM) o `cpu` |

Nessuna delle quattro è stata provata su una GPU: il container non ne ha. La prima corsa
sull'ASUS è anche la prova che funzionano.

## Dentro

- `dati/esegui_gpu.py`: prepara ComfyUI (commit `0df1646`), i due nodi e i pesi, poi lancia le scene.
- `dati/pipeline_scena.py`, `dati/misura_immagini.py`, `dati/rifinitura.py`: le sei fasi e il banco.
- `dati/scene.json`: le dieci scene (otto pose dei quattro PG, due scene nelle caverne di ARC-07).
- `dati/img/`: i riferimenti dei quattro PG, gli scheletri di posa e lo sfondo delle caverne di ARC-07, come erano nel pacchetto per Kaggle.

Il repo ignora i `.webp` (`.gitignore`): lo sfondo delle caverne è diventato
`img/scena_caverne_arc07.png`, ridotto da 3136×1344 a 1568×672 (la pipeline lo porta
comunque a 1536 di lato, e il riquadro è in frazioni). I quattro `intero_*.webp`, che
nessuna scena usa, sono rimasti fuori.
