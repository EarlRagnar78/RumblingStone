"""pipeline_scena.py — PG, PNG e mostri in posa dentro una scena d'arco, con pulizia e misura.

Gira contro un ComfyUI qualsiasi (a casa del DM, in un notebook Kaggle, su una GPU in affitto):
stessi pesi, stesso seed, stesso workflow → stessa scena. Solo libreria standard + PIL/numpy.

Fasi (ognuna scrive il suo file, così si può riprendere e misurare fase per fase):
  1 genera     SDXL + ControlNet union (posa) + IP-Adapter (identità) [+ IP-Adapter stile], N semi
  2 misura     misura_immagini: si tiene il migliore dei N (posa, identità, glitch)
  3 dettaglio  per ogni mano e volto: ritaglio ingrandito, ridipinto a denoise basso con lo stesso riferimento, reincollato sfumato
  4 scena      scontorno (BiRefNet) e composizione nel riquadro, poi passata img2img a denoise basso che unisce luce e grana
  5 finitura   upscale ×2 (Real-ESRGAN, BSD-3) e armonizzazione della palette verso la bibbia visiva dell'arco
  6 misura     di nuovo, prima/dopo; il cancello decide se la scena va al DM o torna indietro

Profili: «gpu» (SDXL, da 10 GB di VRAM in su) e «cpu» (SD1.5 + LCM-LoRA, 6 passi, 512×768: ultima risorsa
quando non c'è né una GPU adatta né Kaggle; più lento e meno fedele, ma gratuito e senza rete dopo il primo download).

Uso: python pipeline_scena.py scena.json --server http://127.0.0.1:8188 --uscita out/ [--profilo gpu|cpu]
"""
import argparse, io, json, os, time, urllib.request, uuid
from pathlib import Path
from PIL import Image, ImageFilter

PESI = {  # nome file → (repo d'origine, licenza): lo legge il cancello licenze
    "sd_xl_base_1.0.safetensors": ("stabilityai/stable-diffusion-xl-base-1.0", "openrail++"),
    "controlnet-union-sdxl-promax.safetensors": ("xinsir/controlnet-union-sdxl-1.0", "apache-2.0"),
    "ip-adapter-plus_sdxl_vit-h.safetensors": ("h94/IP-Adapter", "apache-2.0"),
    "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors": ("h94/IP-Adapter", "apache-2.0"),
    "RealESRGAN_x2plus.pth": ("xinntao/Real-ESRGAN", "bsd-3-clause"),
}
PESI_CPU = {
    "v1-5-pruned-emaonly.safetensors": ("stable-diffusion-v1-5/stable-diffusion-v1-5", "creativeml-openrail-m"),
    "control_v11p_sd15_openpose_fp16.safetensors": ("lllyasviel/ControlNet-v1-1", "openrail"),
    "ip-adapter-plus_sd15.safetensors": ("h94/IP-Adapter", "apache-2.0"),
    "lcm-lora-sdv1-5.safetensors": ("latent-consistency/lcm-lora-sdv1-5", "openrail++"),
    "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors": ("h94/IP-Adapter", "apache-2.0"),
    "RealESRGAN_x2plus.pth": ("xinntao/Real-ESRGAN", "bsd-3-clause"),
}
PROFILI = {
    "gpu": {"ckpt": "sd_xl_base_1.0.safetensors", "cn": "controlnet-union-sdxl-promax.safetensors", "union": True, "lora": None,
            "ipa": "ip-adapter-plus_sdxl_vit-h.safetensors", "w": 896, "h": 1152, "passi": 30, "passi_dett": 24, "cfg": 6.0,
            "sampler": "dpmpp_2m_sde", "scheduler": "karras", "lato_dett": 1024, "lato_scena": 1536},
    "cpu": {"ckpt": "v1-5-pruned-emaonly.safetensors", "cn": "control_v11p_sd15_openpose_fp16.safetensors", "union": False, "lora": "lcm-lora-sdv1-5.safetensors",
            "ipa": "ip-adapter-plus_sd15.safetensors", "w": 512, "h": 768, "passi": 6, "passi_dett": 5, "cfg": 1.5,
            "sampler": "lcm", "scheduler": "sgm_uniform", "lato_dett": 512, "lato_scena": 768},
}
P = PROFILI[os.environ.get("RS_PROFILO", "gpu")]
NEGATIVO = "text, letters, watermark, signature, extra fingers, fused fingers, missing fingers, extra limbs, deformed hands, distorted face, blurry, lowres, jpeg artifacts"

class Comfy:
    def __init__(self, url): self.url = url.rstrip("/")
    def carica(self, img: Image.Image) -> str:
        nome = f"rs_{uuid.uuid4().hex[:10]}.png"; buf = io.BytesIO(); img.save(buf, "PNG")
        corpo, conf = _multipart({"image": (nome, buf.getvalue())}, {"overwrite": "true"})
        urllib.request.urlopen(urllib.request.Request(self.url + "/upload/image", corpo, {"Content-Type": conf}))
        return nome
    def libera(self):  # scarica i modelli di ComfyUI dalla RAM prima di una misura
        req = urllib.request.Request(self.url + "/free", json.dumps({"unload_models": True, "free_memory": True}).encode(), {"Content-Type": "application/json"})
        urllib.request.urlopen(req)
    def esegui(self, grafo: dict) -> list[Image.Image]:
        req = urllib.request.Request(self.url + "/prompt", json.dumps({"prompt": grafo}).encode(), {"Content-Type": "application/json"})
        pid = json.load(urllib.request.urlopen(req))["prompt_id"]
        while True:
            h = json.load(urllib.request.urlopen(f"{self.url}/history/{pid}"))
            if pid in h:
                if h[pid]["status"].get("status_str") == "error":
                    raise RuntimeError(json.dumps(h[pid]["status"]["messages"])[:2000])
                out = []
                for nodo in h[pid]["outputs"].values():
                    for im in nodo.get("images", []):
                        q = f"filename={im['filename']}&subfolder={im['subfolder']}&type={im['type']}"
                        out.append(Image.open(io.BytesIO(urllib.request.urlopen(f"{self.url}/view?{q}").read())).convert("RGB"))
                return out
            time.sleep(2)

def _multipart(files, fields):
    b = uuid.uuid4().hex; parti = []
    for k, v in fields.items():
        parti.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (fn, data) in files.items():
        parti.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: image/png\r\n\r\n'.encode() + data + b"\r\n")
    return b"".join(parti) + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"

def grafo_pg(rif, posa, prompt, seed, stile=None, w=None, h=None, denoise=1.0, base=None, maschera=None,
             peso_id=0.75, peso_stile=0.5, forza_posa=0.9, passi=None, cfg=None):
    """un solo grafo per generare (base=None) o ridipingere (base + maschera): stesse condizioni, così il dettaglio resta coerente."""
    w, h, passi, cfg = w or P["w"], h or P["h"], passi or P["passi"], cfg or P["cfg"]
    g = {
        "ck": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": P["ckpt"]}},
        "ipm": {"class_type": "IPAdapterModelLoader", "inputs": {"ipadapter_file": P["ipa"]}},
        "cv": {"class_type": "CLIPVisionLoader", "inputs": {"clip_name": "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"}},
        "rif": {"class_type": "LoadImage", "inputs": {"image": rif}},
        "ipa": {"class_type": "IPAdapterAdvanced", "inputs": {"model": ["ck", 0], "ipadapter": ["ipm", 0], "image": ["rif", 0], "clip_vision": ["cv", 0],
                "weight": peso_id, "weight_type": "linear", "combine_embeds": "concat", "start_at": 0.0, "end_at": 1.0, "embeds_scaling": "V only"}},
        "pos": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["ck", 1], "text": prompt}},
        "neg": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["ck", 1], "text": NEGATIVO}},
        "cnl": {"class_type": "ControlNetLoader", "inputs": {"control_net_name": P["cn"]}},
        "cnu": {"class_type": "SetUnionControlNetType", "inputs": {"control_net": ["cnl", 0], "type": "openpose"}},
        "posa": {"class_type": "LoadImage", "inputs": {"image": posa}},
        "cna": {"class_type": "ControlNetApplyAdvanced", "inputs": {"positive": ["pos", 0], "negative": ["neg", 0], "control_net": ["cnu", 0], "image": ["posa", 0],
                "strength": forza_posa, "start_percent": 0.0, "end_percent": 0.8, "vae": ["ck", 2]}},
        "ks": {"class_type": "KSampler", "inputs": {"model": ["ipa", 0], "positive": ["cna", 0], "negative": ["cna", 1], "seed": seed, "steps": passi, "cfg": cfg,
               "sampler_name": P["sampler"], "scheduler": P["scheduler"], "denoise": denoise}},
        "dec": {"class_type": "VAEDecode", "inputs": {"samples": ["ks", 0], "vae": ["ck", 2]}},
        "out": {"class_type": "SaveImage", "inputs": {"images": ["dec", 0], "filename_prefix": "rs"}},
    }
    if P["lora"]:  # LCM: pochi passi a cfg basso, l'unico modo di stare in minuti su CPU
        g["lo"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["ck", 0], "lora_name": P["lora"], "strength_model": 1.0}}
        g["ipa"]["inputs"]["model"] = ["lo", 0]
    if not P["union"]:
        del g["cnu"]; g["cna"]["inputs"]["control_net"] = ["cnl", 0]
    modello = ["ipa", 0]
    if stile:  # secondo IP-Adapter, solo stile: tiene la scena nella bibbia visiva dell'arco
        g["sti"] = {"class_type": "LoadImage", "inputs": {"image": stile}}
        g["ips"] = {"class_type": "IPAdapterAdvanced", "inputs": {"model": ["ipa", 0], "ipadapter": ["ipm", 0], "image": ["sti", 0], "clip_vision": ["cv", 0],
                    "weight": peso_stile, "weight_type": "style transfer", "combine_embeds": "concat", "start_at": 0.0, "end_at": 1.0, "embeds_scaling": "V only"}}
        modello = ["ips", 0]
    g["ks"]["inputs"]["model"] = modello
    if base is None:
        g["lat"] = {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}}
        g["ks"]["inputs"]["latent_image"] = ["lat", 0]
    else:
        g["base"] = {"class_type": "LoadImage", "inputs": {"image": base}}
        g["enc"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["base", 0], "vae": ["ck", 2]}}
        lat = ["enc", 0]
        if maschera:
            g["msk"] = {"class_type": "LoadImageMask", "inputs": {"image": maschera, "channel": "red"}}
            g["nm"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["enc", 0], "mask": ["msk", 0]}}
            lat = ["nm", 0]
        g["ks"]["inputs"]["latent_image"] = lat
    return g

def grafo_upscale(img_nome):
    return {"im": {"class_type": "LoadImage", "inputs": {"image": img_nome}},
            "um": {"class_type": "UpscaleModelLoader", "inputs": {"model_name": "RealESRGAN_x2plus.pth"}},
            "up": {"class_type": "ImageUpscaleWithModel", "inputs": {"upscale_model": ["um", 0], "image": ["im", 0]}},
            "out": {"class_type": "SaveImage", "inputs": {"images": ["up", 0], "filename_prefix": "rs_up"}}}

def dettaglio(c, img, regioni, rif, prompt, seed, lato=None, denoise=0.4, posa_vuota=None):
    """ridipinge ogni regione (mano, volto) a 1024 px e la reincolla con bordo sfumato: il «detailer» dei flussi professionali."""
    out = img.copy(); lato = lato or P["lato_dett"]
    for i, (tipo, (x0, y0, x1, y1)) in enumerate(regioni):
        crop = out.crop((x0, y0, x1, y1)); s = lato / max(crop.size)
        cr = crop.resize((max(64, int(crop.width * s) // 8 * 8), max(64, int(crop.height * s) // 8 * 8)), Image.LANCZOS)
        nero = Image.new("RGB", cr.size)
        testo = f"{prompt}, detailed {'hand with five fingers' if tipo == 'mano' else 'face, symmetric eyes'}"
        g = grafo_pg(rif, c.carica(posa_vuota or nero), testo, seed + i, w=cr.width, h=cr.height, denoise=denoise, base=c.carica(cr), forza_posa=0.0, passi=P["passi_dett"])
        nuovo = c.esegui(g)[0].resize(crop.size, Image.LANCZOS)
        m = Image.new("L", crop.size, 0); bordo = max(4, min(crop.size) // 8)
        m.paste(255, (bordo, bordo, crop.width - bordo, crop.height - bordo)); m = m.filter(ImageFilter.GaussianBlur(bordo / 2))
        out.paste(nuovo, (x0, y0), m)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("scena"); ap.add_argument("--server", default="http://127.0.0.1:8188"); ap.add_argument("--uscita", default="out")
    ap.add_argument("--semi", type=int, default=4); ap.add_argument("--profilo", choices=list(PROFILI), default=os.environ.get("RS_PROFILO", "gpu"))
    a = ap.parse_args(); P = PROFILI[a.profilo]
    LIBERA = a.profilo == "cpu" or os.environ.get("RS_LIBERA") == "1"  # 6 GB di VRAM: un modello alla volta anche sul profilo gpu
    import misura_immagini as M, rifinitura as R
    sc = json.load(open(a.scena)); c = Comfy(a.server); out = Path(a.uscita); out.mkdir(parents=True, exist_ok=True)
    rif = c.carica(Image.open(sc["riferimento"])); posa = c.carica(Image.open(sc["posa_png"]))
    stile = c.carica(Image.open(sc["stile"])) if sc.get("stile") else None
    registro = []
    def misura(caso):  # sul profilo cpu un modello alla volta in RAM: prima si svuota ComfyUI, dopo il banco
        if LIBERA: c.libera()
        r = M.misura(caso)
        if LIBERA: M.libera()
        return r
    candidati = []
    for k in range(a.semi):  # fase 1-2: best-of-N
        seed = sc["seed"] + k
        im = c.esegui(grafo_pg(rif, posa, sc["prompt"], seed, stile))[0]; p = out / f"1_genera_{seed}.png"; im.save(p)
        m = misura({**sc["misura"], "immagine": str(p)}); m["seed"] = seed; candidati.append((M.punteggio(m), p, m)); registro.append(m)
    _, migliore, m0 = max(candidati, key=lambda x: x[0])
    im = Image.open(migliore)
    regioni = R.maschere_glitch(im, M.scheletri(im))  # fase 3
    im = dettaglio(c, im, regioni, rif, sc["prompt"], m0["seed"]); im.save(out / "3_dettaglio.png")
    if sc.get("scena_sfondo"):  # fase 4
        if LIBERA: c.libera()  # BiRefNet e il modello di ComfyUI non stanno insieme in 16 GB
        pg = R.scontorna(im); sfondo = Image.open(sc["scena_sfondo"]).convert("RGB")
        k = min(1.0, P["lato_scena"] / max(sfondo.size))  # la passata di fusione lavora al lato massimo del profilo, poi c'è l'upscale
        sfondo = sfondo.resize((int(sfondo.width * k) // 8 * 8, int(sfondo.height * k) // 8 * 8), Image.LANCZOS)
        comp = R.componi(sfondo, pg, sc["riquadro"]); comp.save(out / "4_composta.png")
        if LIBERA: R.libera()
        posa_c = c.carica(Image.open(sc.get("posa_scena_png", sc["posa_png"])))
        im = c.esegui(grafo_pg(rif, posa_c, sc["prompt_scena"], m0["seed"], stile, w=comp.width // 8 * 8, h=comp.height // 8 * 8, denoise=0.3, base=c.carica(comp), forza_posa=0.5))[0]
        im.save(out / "4_scena.png")
    im = c.esegui(grafo_upscale(c.carica(im)))[0]  # fase 5
    if sc.get("stile"):
        im = R.armonizza(im, Image.open(sc["stile"]), forza=sc.get("forza_stile", 0.4))
    im.save(out / "5_finale.png")
    mf = misura({**sc["misura"], "immagine": str(out / "5_finale.png")}); registro.append(mf)
    json.dump(registro, open(out / "misure.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"migliore": str(migliore), "prima": M.punteggio(m0), "dopo": M.punteggio(mf), "cancello": M.cancello(mf)}, ensure_ascii=False))
