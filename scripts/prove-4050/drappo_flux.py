"""drappo_flux.py — il collaudo della D2 (arte del Drappo): FLUX.2 [klein] 4B accanto a Gemini.

Gira dentro il box «comfyui» (lo lancia drappo-flux.sh). Prepara ComfyUI al commit già provato
dalla pipeline delle immagini (in una cartella sua, «ComfyUI-flux»), scarica tre pesi Apache 2.0 verificandone lo sha256, avvia ComfyUI
con --lowvram, genera le tavole scelte con scripts/comfyui_batch.py (prompt dal markdown del modulo,
seed fisso derivato dall'id) e misura per ogni immagine secondi, picco di VRAM e picco di RAM.
Alla fine mette ogni tavola accanto a quella di Gemini in una pagina HTML e, se c'è Pillow, in un
JPEG affiancato da caricare nel thread. Le immagini del modulo non vengono toccate.

Uso: python drappo_flux.py --lavoro DIR --uscita DIR [--solo id,id] [--semi N] [--cpu]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent.parent
sys.path.insert(0, str(RADICE / "scripts"))
import comfyui_batch as cb  # noqa: E402

COMFY_COMMIT = "0df1646"  # lo stesso di immagini-posa-4050 (provato il 2026-10-29); ha già FLUX.2
MODELLO = "flux2-klein-4b"
# (cartella di ComfyUI, nome atteso dal grafo, repo HF, file nel repo, sha256 pubblicato, byte)
PESI = [
    ("diffusion_models", "flux-2-klein-4b-fp8.safetensors", "black-forest-labs/FLUX.2-klein-4b-fp8",
     "flux-2-klein-4b-fp8.safetensors",
     "97ed34fe0567e436200f2faee3939b88f2b5d99f8af2a4dc16532c4245c0ccb6", 4070624520),
    ("text_encoders", "qwen_3_4b_fp4_flux2.safetensors", "Comfy-Org/Flux-2-Klein-4B",
     "split_files/text_encoders/qwen_3_4b_fp4_flux2.safetensors",
     "3eab03a77adb0ee5304a4e677d5c10ac22f9049c1d7c894adca4f8bb39206ca8", 3848213998),
    ("vae", "flux2-vae.safetensors", "Comfy-Org/Flux-2-Klein-4B",
     "split_files/vae/flux2-vae.safetensors",
     "868fe7b343cc8f3a19dbcfcafbc3d5f888802be3f89bd81b65b3621a066ce8f3", 336211292),
]
# Una per tipo: un ritratto, una tavola d'ambiente orizzontale, l'oggetto. Tre è il «due o tre» del DM.
SOLO_DEFAULT = "ritratto-vanna,tavola-la-ruota,il-drappo"
GEMINI = RADICE / "10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini"


def sh(*a, **k):
    print("+", " ".join(map(str, a)), flush=True)
    subprocess.run(a, check=True, **k)


def sha256(percorso: Path) -> str:
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 22), b""):
            h.update(blocco)
    return h.hexdigest()


def peso_verificato(percorso: Path, atteso: str) -> bool:
    """Vero se il file ha lo sha256 atteso. Il risultato si ricorda in <file>.sha256 (4 GB si leggono una volta)."""
    if not percorso.exists():
        return False
    nota = percorso.with_name(percorso.name + ".sha256")
    firma = f"{atteso} {percorso.stat().st_size} {int(percorso.stat().st_mtime)}"
    if nota.exists() and nota.read_text().strip() == firma:
        return True
    if sha256(percorso) != atteso:
        return False
    nota.write_text(firma + "\n")
    return True


def prepara(lavoro: Path) -> Path:
    # Un clone suo, non «ComfyUI»: quello è di esegui_gpu.py (immagini.sh), che vi mette i suoi nodi
    # solo quando lo crea. Se questa prova lo creasse per prima, senza nodi, immagini.sh si romperebbe.
    comfy = lavoro / "ComfyUI-flux"
    if not comfy.exists():
        sh("git", "clone", "-q", "https://github.com/comfyanonymous/ComfyUI.git", str(comfy))
        sh("git", "-C", str(comfy), "checkout", "-q", COMFY_COMMIT)
    nodi = (comfy / "comfy_extras" / "nodes_flux.py").read_text(encoding="utf-8")
    if "EmptyFlux2LatentImage" not in nodi:
        raise SystemExit(f"ComfyUI in {comfy} non conosce FLUX.2: git -C {comfy} checkout {COMFY_COMMIT}")
    sh(sys.executable, "-m", "pip", "install", "-q", "-r", str(comfy / "requirements.txt"), "huggingface_hub")
    from huggingface_hub import hf_hub_download

    for cart, nome, repo, f, atteso, _ in PESI:
        dst = comfy / "models" / cart / nome
        if peso_verificato(dst, atteso):
            print(f"    {nome}: c'è, sha256 giusto", flush=True)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        for prova in range(5):  # i file da 4 GB a volte cadono a metà: hf_hub_download riprende
            try:
                p = Path(hf_hub_download(repo, f))
                break
            except Exception as e:  # noqa: BLE001 — rete: si riprova e poi si alza
                if prova == 4:
                    raise
                print(f"download interrotto ({e.__class__.__name__}), riprovo", flush=True)
                time.sleep(2 ** (prova + 1))
        if dst.is_symlink() or dst.exists():
            dst.unlink()
        os.symlink(p, dst)
        if not peso_verificato(dst, atteso):
            raise SystemExit(f"{nome}: sha256 diverso da quello pubblicato ({atteso}). Cancella {p} e rilancia.")
        print(f"    {nome}: scaricato, sha256 giusto", flush=True)
    return comfy


def avvia(comfy: Path, porta: int, cpu: bool) -> subprocess.Popen:
    # --lowvram e --cpu si escludono in ComfyUI: sulla CPU non c'è VRAM da risparmiare
    argomenti = [] if cpu else os.environ.get("RS_COMFY_ARGS", "--lowvram").split()
    log = open(comfy.parent / "comfy-flux.log", "w")
    p = subprocess.Popen([sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(porta)]
                         + (["--cpu"] if cpu else []) + argomenti,
                         cwd=comfy, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(180):
        if p.poll() is not None:
            raise SystemExit(f"ComfyUI è uscito subito: vedi {comfy.parent / 'comfy-flux.log'}")
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{porta}/system_stats", timeout=2)
            return p
        except Exception:  # noqa: BLE001
            time.sleep(2)
    p.terminate()
    raise SystemExit(f"ComfyUI non risponde: vedi {comfy.parent / 'comfy-flux.log'}")


class Picchi(threading.Thread):
    """Ogni secondo: memoria usata della GPU (nvidia-smi) e RAM del processo di ComfyUI (VmRSS)."""

    def __init__(self, pid: int):
        super().__init__(daemon=True)
        self.pid, self.fermo = pid, threading.Event()
        self.vram_mib = 0
        self.ram_mib = 0
        self.gpu = shutil.which("nvidia-smi") is not None

    def run(self):
        while not self.fermo.is_set():
            if self.gpu:
                try:
                    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                         capture_output=True, text=True, timeout=5).stdout
                    self.vram_mib = max(self.vram_mib, int(out.split()[0]))
                except Exception:  # noqa: BLE001
                    pass
            try:
                for riga in Path(f"/proc/{self.pid}/status").read_text().splitlines():
                    if riga.startswith("VmRSS:"):
                        self.ram_mib = max(self.ram_mib, int(riga.split()[1]) // 1024)
            except OSError:
                pass
            self.fermo.wait(1)


def genera(ident: str, seme: int, cartella: Path, porta: int, pid: int, attesa: int) -> dict:
    argomenti = ["--modello", MODELLO, "--solo", ident, "--out", str(cartella), "--forza",
                 "--server", f"http://127.0.0.1:{porta}", "--attesa-max", str(attesa),
                 "--autore", "DM, collaudo D2 sul portatile 4050"]
    if seme:  # il seme 0 è quello derivato dall'id; gli altri sono varianti, non scarti
        argomenti += ["--reroll", str(seme), "--motivo", f"collaudo D2: variante di seme {seme}, non uno scarto"]
    picchi = Picchi(pid)
    picchi.start()
    t0 = time.time()
    uscita = cb.main(argomenti)
    picchi.fermo.set()
    picchi.join()
    png = cartella / f"{ident}.png"
    return {"id": ident, "seme": seme, "esito": "ok" if uscita == 0 and png.exists() else "fallita",
            "secondi": round(time.time() - t0, 1), "vram_picco_mib": picchi.vram_mib,
            "ram_comfyui_picco_mib": picchi.ram_mib, "file": str(png.relative_to(cartella.parent.parent))
            if png.exists() else None}


def affianca(gemini: Path, flux: list[Path], dest: Path) -> bool:
    """Gemini a sinistra, FLUX a destra, stessa altezza, JPEG. Senza Pillow si salta: c'è la pagina HTML."""
    try:
        from PIL import Image, ImageDraw, PngImagePlugin
    except ImportError:
        return False
    # Le PNG di Gemini portano il manifesto C2PA in un blocco di testo più grande del limite di Pillow
    PngImagePlugin.MAX_TEXT_CHUNK = 64 * 1024 * 1024
    alt = 1024
    tavole = []
    for p in [gemini, *flux]:
        im = Image.open(p).convert("RGB")
        tavole.append(im.resize((round(im.width * alt / im.height), alt)))
    larg = sum(t.width for t in tavole) + 16 * (len(tavole) - 1)
    tela = Image.new("RGB", (larg, alt + 40), "white")
    x = 0
    disegno = ImageDraw.Draw(tela)
    for i, t in enumerate(tavole):
        tela.paste(t, (x, 40))
        disegno.text((x + 8, 12), "A · Gemini (oggi nel modulo)" if i == 0 else f"B · FLUX.2 klein 4B, seme {i - 1}",
                     fill="black")
        x += t.width + 16
    tela.save(dest, quality=88)
    return True


def pagina(righe: list[dict], uscita: Path, solo: list[str], semi: int) -> None:
    corpo = []
    for ident in solo:
        gem = GEMINI / f"{ident}.png"
        celle = [f'<figure><img src="{html.escape(gem.as_uri())}"><figcaption>A · Gemini</figcaption></figure>']
        for r in (r for r in righe if r["id"] == ident):
            if r["file"]:
                celle.append(f'<figure><img src="{html.escape(r["file"])}"><figcaption>B · FLUX.2 klein 4B, '
                             f'seme {r["seme"]} · {r["secondi"]} s</figcaption></figure>')
            else:
                celle.append(f'<figure><figcaption>B · seme {r["seme"]}: fallita</figcaption></figure>')
        corpo.append(f"<h2>{html.escape(ident)}</h2><div class=riga>{''.join(celle)}</div>")
    (uscita / "confronto.html").write_text(
        "<!doctype html><meta charset=utf-8><title>D2 · Gemini contro FLUX.2 klein</title>"
        "<style>body{font-family:sans-serif;margin:16px}.riga{display:flex;gap:12px;overflow-x:auto}"
        "img{height:70vh}figure{margin:0}</style>"
        f"<h1>D2 · arte del Drappo: A (Gemini) o B (FLUX.2 klein 4B, locale)</h1>"
        f"<p>{len(solo)} tavole, {semi} semi ciascuna. Si sceglie guardando: il gate di rifiuto del README delle "
        "immagini, §6, il giorno dopo.</p>" + "".join(corpo), encoding="utf-8")


def versione_torch() -> str:
    try:
        import torch
        return torch.__version__
    except ImportError:
        return "assente"


def torch_vecchio(versione: str) -> bool:
    """Sotto la 2.8 ComfyUI rinuncia alla gestione dinamica della VRAM, che su 6 GB conta."""
    try:
        maggiore, minore = (int(x) for x in versione.split("+")[0].split(".")[:2])
    except ValueError:
        return False
    return (maggiore, minore) < (2, 8)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lavoro", required=True, type=Path)
    ap.add_argument("--uscita", required=True, type=Path)
    ap.add_argument("--solo", default=SOLO_DEFAULT, help=f"id separati da virgola (default {SOLO_DEFAULT})")
    ap.add_argument("--semi", type=int, default=2, help="semi per tavola (default 2)")
    ap.add_argument("--cpu", action="store_true", help="solo per provare il grafo senza GPU: lentissimo")
    ap.add_argument("--porta", type=int, default=8189, help="8189, per non urtare un ComfyUI già acceso su 8188")
    ap.add_argument("--attesa-max", type=int, default=1800)
    a = ap.parse_args()
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    solo = [s for s in a.solo.split(",") if s]
    noti = {img.ident for img in cb.leggi_immagini(cb.PROMPTS_DEFAULT.read_text(encoding="utf-8"))}
    ignoti = [s for s in solo if s not in noti]
    if ignoti:
        raise SystemExit(f"id sconosciuti: {', '.join(ignoti)} (vedi python3 scripts/comfyui_batch.py --lista)")
    uscita = a.uscita.resolve()
    uscita.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch_v = versione_torch()
    if torch_vecchio(torch_v) and not a.cpu:
        print(f"AVVISO: PyTorch {torch_v} nel venv. Sotto la 2.8 ComfyUI gestisce la VRAM alla vecchia maniera "
              "e su 6 GB può non bastare. Per aggiornarlo, dentro il venv: pip install -U torch torchvision "
              "--index-url https://download.pytorch.org/whl/cu126", flush=True)
    comfy = prepara(a.lavoro.resolve())
    proc = avvia(comfy, a.porta, a.cpu)
    righe = []
    try:
        for seme in range(a.semi):
            for ident in solo:
                print(f"==> {ident}, seme {seme}", flush=True)
                r = genera(ident, seme, uscita / "flux" / f"seme-{seme}", a.porta, proc.pid, a.attesa_max)
                print(f"    {r['esito']} in {r['secondi']} s · VRAM picco {r['vram_picco_mib']} MiB · "
                      f"RAM di ComfyUI picco {r['ram_comfyui_picco_mib']} MiB", flush=True)
                righe.append(r)
    finally:
        proc.terminate()
        proc.wait(30)
    shutil.copy(comfy.parent / "comfy-flux.log", uscita / "comfy-flux.log")
    # Prima le misure, poi i confronti: un'immagine che Pillow non apre non deve costare il riepilogo
    riepilogo = {"modello": cb.MODELLI[MODELLO]["etichetta"], "comfyui": COMFY_COMMIT, "torch": torch_v,
                 "argomenti_comfyui": os.environ.get("RS_COMFY_ARGS", "--lowvram"), "cpu": a.cpu,
                 "pesi": [{"file": n, "repo": r, "sha256": s} for _, n, r, _, s, _ in PESI],
                 "minuti_totali": round((time.time() - t0) / 60, 1), "immagini": righe}
    (uscita / "riepilogo.json").write_text(json.dumps(riepilogo, indent=2, ensure_ascii=False), encoding="utf-8")
    pagina(righe, uscita, solo, a.semi)
    for ident in solo:
        flux = [uscita / r["file"] for r in righe if r["id"] == ident and r["file"]]
        if flux and (GEMINI / f"{ident}.png").exists():
            try:
                affianca(GEMINI / f"{ident}.png", flux, uscita / f"confronto-{ident}.jpg")
            except Exception as e:  # noqa: BLE001 — il JPEG affiancato è un comodo, la pagina HTML c'è già
                print(f"AVVISO: confronto-{ident}.jpg non fatto ({e.__class__.__name__}: {e})", flush=True)
    fallite = sum(r["esito"] != "ok" for r in righe)
    print(f"{len(righe) - fallite} fatte, {fallite} fallite. Apri {uscita / 'confronto.html'}")
    return 1 if fallite else 0


if __name__ == "__main__":
    raise SystemExit(main())
