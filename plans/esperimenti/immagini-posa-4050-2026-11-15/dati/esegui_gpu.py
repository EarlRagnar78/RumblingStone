"""esegui_gpu.py — prepara ComfyUI con i pesi della pipeline su una GPU qualsiasi e lancia tutte le scene.

È lo stesso script per la macchina del DM, per un notebook Kaggle e per una GPU in affitto.
Uso: python esegui_gpu.py --dati <cartella con scene.json e img/> --lavoro <cartella di lavoro> --uscita <cartella risultati>
"""
import argparse, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

NODI = ["https://github.com/Fannovel16/comfyui_controlnet_aux.git", "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"]
COMFY_COMMIT = "0df1646"  # quello provato il 2026-10-29
PESI_CPU = [  # profilo cpu: SD1.5 + LCM-LoRA, ~5 GB in tutto
    ("checkpoints", "v1-5-pruned-emaonly.safetensors", "stable-diffusion-v1-5/stable-diffusion-v1-5", "v1-5-pruned-emaonly.safetensors"),
    ("controlnet", "control_v11p_sd15_openpose_fp16.safetensors", "comfyanonymous/ControlNet-v1-1_fp16_safetensors", "control_v11p_sd15_openpose_fp16.safetensors"),
    ("ipadapter", "ip-adapter-plus_sd15.safetensors", "h94/IP-Adapter", "models/ip-adapter-plus_sd15.safetensors"),
    ("loras", "lcm-lora-sdv1-5.safetensors", "latent-consistency/lcm-lora-sdv1-5", "pytorch_lora_weights.safetensors"),
    ("clip_vision", "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors", "h94/IP-Adapter", "models/image_encoder/model.safetensors"),
]
PESI = [  # (cartella ComfyUI, nome file, repo HF, file nel repo)
    ("checkpoints", "sd_xl_base_1.0.safetensors", "stabilityai/stable-diffusion-xl-base-1.0", "sd_xl_base_1.0.safetensors"),
    ("controlnet", "controlnet-union-sdxl-promax.safetensors", "xinsir/controlnet-union-sdxl-1.0", "diffusion_pytorch_model_promax.safetensors"),
    ("ipadapter", "ip-adapter-plus_sdxl_vit-h.safetensors", "h94/IP-Adapter", "sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors"),
    ("clip_vision", "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors", "h94/IP-Adapter", "models/image_encoder/model.safetensors"),
]
ESRGAN = ("upscale_models", "RealESRGAN_x2plus.pth", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth")

def sh(*a, **k):
    print("+", " ".join(map(str, a)), flush=True); subprocess.run(a, check=True, **k)

def prepara(lavoro: Path, profilo: str = "gpu"):
    comfy = lavoro / "ComfyUI"
    if not comfy.exists():
        sh("git", "clone", "-q", "https://github.com/comfyanonymous/ComfyUI.git", str(comfy))
        sh("git", "-C", str(comfy), "checkout", "-q", COMFY_COMMIT)
        for n in NODI:
            sh("git", "clone", "-q", "--depth", "1", n, str(comfy / "custom_nodes" / n.rsplit("/", 1)[1][:-4]))
    reqs = [comfy / "requirements.txt", comfy / "custom_nodes/comfyui_controlnet_aux/requirements.txt"]
    import importlib.util, shutil
    pip = [sys.executable, "-m", "pip", "install", "-q"] if importlib.util.find_spec("pip") else ["uv", "pip", "install", "-q", "--python", sys.executable]
    if not importlib.util.find_spec("pip") and not shutil.which("uv"):
        raise SystemExit("serve pip o uv per installare le dipendenze")
    sh(*pip, *sum([["-r", str(r)] for r in reqs], []), "transformers>=5", "accelerate", "rapidocr-onnxruntime", "scikit-image", "huggingface_hub", "timm>=1", "einops", "kornia")
    from huggingface_hub import hf_hub_download
    for cart, nome, repo, f in (PESI_CPU if profilo == "cpu" else PESI):
        dst = comfy / "models" / cart / nome
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            for prova in range(5):  # i file da 4-7 GB a volte cadono a metà: hf_hub_download riprende da dove era
                try:
                    p = hf_hub_download(repo, f); break
                except Exception as e:
                    if prova == 4: raise
                    print(f"download interrotto ({e.__class__.__name__}), riprovo", flush=True); time.sleep(2 ** (prova + 1))
            os.symlink(p, dst)
    dst = comfy / "models" / ESRGAN[0] / ESRGAN[1]
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(ESRGAN[2], dst)
    return comfy

VRAM_COMFY = {"--gpu-only", "--highvram", "--normalvram", "--lowvram", "--novram"}  # con --cpu ComfyUI li rifiuta

def argomenti_comfy(porta: int, cpu: bool, extra: str) -> list:
    """Gli argomenti di main.py. --cpu e le opzioni di VRAM stanno nello stesso gruppo esclusivo di ComfyUI:
    insieme il server non parte, quindi con --cpu quelle di RS_COMFY_ARGS si tolgono."""
    piu = [x for x in extra.split() if not (cpu and x in VRAM_COMFY)]
    return ["main.py", "--listen", "127.0.0.1", "--port", str(porta)] + (["--cpu"] if cpu else []) + piu

def risponde(porta: int) -> bool:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{porta}/system_stats", timeout=2); return True
    except Exception:
        return False

def avvia(comfy: Path, porta=8188, cpu=False):
    if risponde(porta):  # un ComfyUI rimasto acceso (un'altra prova, una corsa interrotta) ha altri pesi e altri argomenti
        raise SystemExit(f"sulla porta {porta} risponde già un ComfyUI: chiudilo (scripts/comfyui-local/stop.sh, o pkill -f 'main.py --listen') e rilancia")
    log = open(comfy.parent / "comfy.log", "w")
    p = subprocess.Popen([sys.executable] + argomenti_comfy(porta, cpu, os.environ.get("RS_COMFY_ARGS", "")), cwd=comfy, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(180):
        if risponde(porta): return p
        if p.poll() is not None:  # uscito subito (argomenti rifiutati, CUDA che manca): inutile aspettare sei minuti
            raise SystemExit(f"ComfyUI è uscito con {p.returncode}: vedi {comfy.parent / 'comfy.log'}")
        time.sleep(2)
    p.terminate()
    raise SystemExit("ComfyUI non parte: vedi comfy.log")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dati", required=True); ap.add_argument("--lavoro", required=True); ap.add_argument("--uscita", required=True)
    ap.add_argument("--semi", type=int, default=4); ap.add_argument("--solo", default="")
    ap.add_argument("--profilo", choices=["gpu", "cpu"], default="gpu")
    a = ap.parse_args(); os.environ["RS_PROFILO"] = a.profilo; os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    dati, lavoro, uscita = Path(a.dati).resolve(), Path(a.lavoro).resolve(), Path(a.uscita).resolve()
    lavoro.mkdir(parents=True, exist_ok=True); uscita.mkdir(parents=True, exist_ok=True)
    # RS_COMFY_DEVICE=gpu: il profilo leggero «cpu» (SD1.5 + LCM) gira sulla GPU invece che con --cpu
    su_cpu = a.profilo == "cpu" and os.environ.get("RS_COMFY_DEVICE") != "gpu"
    t0 = time.time(); comfy = prepara(lavoro, a.profilo); proc = avvia(comfy, cpu=su_cpu)
    sys.path.insert(0, str(dati)); os.environ["RS_AUX"] = str(comfy / "custom_nodes/comfyui_controlnet_aux")
    os.chdir(dati)
    scene = json.load(open("scene.json")); riepilogo = []
    solo = [x.strip() for x in a.solo.split(",") if x.strip()]
    ignote = [x for x in solo if x not in {sc["nome"] for sc in scene}]
    try:
        if ignote:
            raise SystemExit(f"scene sconosciute: {', '.join(ignote)}. Ci sono: {', '.join(sc['nome'] for sc in scene)}")
        for sc in scene:
            if solo and sc["nome"] not in solo: continue
            t = time.time(); out = uscita / sc["nome"]; json.dump(sc, open(dati / "_scena.json", "w"))
            r = subprocess.run([sys.executable, "pipeline_scena.py", "_scena.json", "--uscita", str(out), "--semi", str(a.semi)], capture_output=True, text=True)
            riga = {"scena": sc["nome"], "secondi": round(time.time() - t), "codice": r.returncode, "esito": r.stdout.strip().splitlines()[-1:] if r.returncode == 0 else r.stderr[-1500:]}
            print(json.dumps(riga, ensure_ascii=False), flush=True); riepilogo.append(riga)
            out.mkdir(parents=True, exist_ok=True); (out / "log.txt").write_text(r.stdout + "\n" + r.stderr[-20000:])
            json.dump({"secondi_totali": round(time.time() - t0), "scene": riepilogo}, open(uscita / "riepilogo.json", "w"), indent=1, ensure_ascii=False)
    finally:  # anche su errore o Ctrl-C: un ComfyUI rimasto acceso tiene la VRAM e la porta
        proc.terminate()
        (dati / "_scena.json").unlink(missing_ok=True)
    sys.exit(0 if riepilogo and all(x["codice"] == 0 for x in riepilogo) else 1)
