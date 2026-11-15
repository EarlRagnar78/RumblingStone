"""misura_immagini.py — banco di misura per un PG in posa dentro una scena.

Sei misure, tutte con pesi a licenza libera, tutte su CPU:
  posa      DWPose (Apache-2.0): somiglianza degli angoli degli arti fra la posa chiesta e quella ottenuta
  identita  DINOv2 (Apache-2.0): coseno fra il riferimento canone del PG e il PG ritagliato nell'immagine
  testo     SigLIP2 (Apache-2.0): quanto l'immagine corrisponde alla descrizione (il CLIP-T dei benchmark)
  segni     SigLIP2: per ogni segno della scheda, «c'è» contro «non c'è»
  glitch    giudice VLM Qwen3-VL (Apache-2.0) con una lista fissa di domande sì/no + OCR RapidOCR per il testo spurio
  stile     distanza della palette (k-means in Lab) dalla bibbia visiva dell'arco

Uso: python misura_immagini.py caso.json   →  stampa JSON con le misure e il verdetto per soglia
"""
import json, math, sys, time
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image

AUX = Path(__import__("os").environ.get("RS_AUX", str(Path(__file__).resolve().parent.parent / "ComfyUI/custom_nodes/comfyui_controlnet_aux")))
sys.path.insert(0, str(AUX / "src"))

# --- posa ------------------------------------------------------------------
OSSA = [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11), (11, 12), (12, 13), (1, 0)]

@lru_cache(None)
def _dwpose():
    from custom_controlnet_aux.dwpose import DwposeDetector
    import custom_controlnet_aux.dwpose as m
    return m.DwposeDetector.from_pretrained("yzd-v/DWPose", det_filename="yolox_l.onnx", pose_filename="dw-ll_ucoco_384.onnx", torchscript_device="cpu")

def scheletri(img: Image.Image):
    """se il rilevatore di persone non vede nessuno (succede con figure stilizzate), stima la posa sull'immagine intera e lo segna."""
    det = _dwpose()
    _, js = det(np.array(img.convert("RGB")), detect_resolution=768, include_hand=True, include_face=True, image_and_json=True, output_type="np")
    if not js["people"]:
        wb = det.dw_pose_estimation; salva = wb.det; wb.det = None
        try:
            _, js = det(np.array(img.convert("RGB")), detect_resolution=768, include_hand=True, include_face=True, image_and_json=True, output_type="np")
        finally:
            wb.det = salva
        for p in js["people"]:
            p["_senza_rilevatore"] = True
    W, H = js["canvas_width"], js["canvas_height"]
    out = []
    for p in js["people"]:
        k = np.array(p["pose_keypoints_2d"]).reshape(-1, 3)
        k[:, 0] /= W; k[:, 1] /= H
        out.append({"senza_rilevatore": p.get("_senza_rilevatore", False), "corpo": k, "mani": [np.array(p.get(h) or []).reshape(-1, 3) for h in ("hand_left_keypoints_2d", "hand_right_keypoints_2d")]})
    return out

def somiglianza_posa(a, b):
    """media del coseno fra le direzioni degli arti visibili in entrambe (1 = identica, 0 = ortogonale)."""
    cos = []
    for i, j in OSSA:
        if min(a[i, 2], a[j, 2], b[i, 2], b[j, 2]) <= 0.3:
            continue
        va, vb = a[j, :2] - a[i, :2], b[j, :2] - b[i, :2]
        na, nb = np.linalg.norm(va), np.linalg.norm(vb)
        if na and nb:
            cos.append(float(va @ vb / (na * nb)))
    return (sum(cos) / len(cos), len(cos)) if cos else (0.0, 0)

def riquadro(sk, img, margine=0.12):
    k = sk["corpo"][sk["corpo"][:, 2] > 0.3][:, :2]
    if not len(k):
        return img
    W, H = img.size
    x0, y0 = k.min(0); x1, y1 = k.max(0)
    dx, dy = (x1 - x0) * margine + 0.03, (y1 - y0) * margine + 0.03
    return img.crop((int(max(0, x0 - dx) * W), int(max(0, y0 - dy) * H), int(min(1, x1 + dx) * W), int(min(1, y1 + dy) * H)))

# --- identità e testo --------------------------------------------------------
@lru_cache(None)
def _dino():
    from transformers import AutoImageProcessor, AutoModel
    return AutoImageProcessor.from_pretrained("facebook/dinov2-base"), AutoModel.from_pretrained("facebook/dinov2-base").eval()

def dino(img):
    import torch
    pr, m = _dino()
    with torch.no_grad():
        o = m(**pr(images=img.convert("RGB"), return_tensors="pt"))
    v = o.last_hidden_state[:, 0]
    return torch.nn.functional.normalize(v, dim=-1)[0]

@lru_cache(None)
def _siglip():
    from transformers import AutoModel, AutoProcessor
    n = "google/siglip2-so400m-patch14-384"
    return AutoProcessor.from_pretrained(n), AutoModel.from_pretrained(n).eval()

def siglip(img, testi):
    import torch
    pr, m = _siglip()
    with torch.no_grad():
        o = m(**pr(text=testi, images=img.convert("RGB"), padding="max_length", max_length=64, return_tensors="pt"))
    return torch.sigmoid(o.logits_per_image[0]).tolist(), o.logits_per_image[0].tolist()

# --- glitch -------------------------------------------------------------------
DOMANDE = [
    ("mani", "Do all visible hands have a natural shape with five fingers and no fused, missing or extra fingers?"),
    ("arti", "Does every person have the correct number of arms and legs, with no extra or missing limbs?"),
    ("volto", "Is every face undistorted, with symmetric eyes and no melted or doubled features?"),
    ("oggetti", "Are all held objects and weapons whole, straight where they should be, and correctly gripped?"),
    ("testo", "Is the image free of any text, letters, signature or watermark?"),
]

@lru_cache(None)
def _vlm():
    from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
    n = "Qwen/Qwen3-VL-4B-Instruct"
    import os, torch
    dove = os.environ.get("RS_VLM_DEVICE") or ("cuda" if torch.cuda.is_available() else "cpu")
    extra = {"max_memory": {0: os.environ.get("RS_VLM_GPU", "4GiB"), "cpu": "12GiB"}} if dove == "auto" else {}
    # 4B in fp16 sono ~8,5 GB: su 6 GB di VRAM (RTX 4050) va «auto» (in parte in RAM) o «cpu»
    return AutoProcessor.from_pretrained(n), Qwen3VLForConditionalGeneration.from_pretrained(n, dtype=(torch.float16 if dove != "cpu" else torch.bfloat16), device_map=dove, **extra).eval()

def giudice(img, segni):
    """chiede al VLM un sì/no per ogni domanda; restituisce la probabilità di «Yes» (logit del primo token)."""
    import torch
    pr, m = _vlm()
    im = img.convert("RGB"); im.thumbnail((640, 640))
    domande = DOMANDE + [(f"segno:{s}", f"Is this clearly visible in the image: {s}?") for s in segni]
    si, no = pr.tokenizer.encode("Yes")[0], pr.tokenizer.encode("No")[0]
    esiti = {}
    for chiave, d in domande:
        msg = [{"role": "user", "content": [{"type": "image", "image": im}, {"type": "text", "text": d + " Answer Yes or No."}]}]
        inp = pr.apply_chat_template(msg, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt").to(m.device)
        with torch.no_grad():
            lg = m(**inp).logits[0, -1].float()
        p = torch.softmax(lg[[si, no]], 0)[0].item()
        esiti[chiave] = round(p, 3)
    return esiti

@lru_cache(None)
def _ocr():
    from rapidocr_onnxruntime import RapidOCR
    return RapidOCR()

def testo_spurio(img):
    r, _ = _ocr()(np.array(img.convert("RGB")))
    return [t[1] for t in (r or []) if t[2] > 0.6 and len(t[1].strip()) >= 2]

# --- stile ---------------------------------------------------------------------
def palette(img, k=6):
    from skimage.color import rgb2lab
    a = np.asarray(img.convert("RGB").resize((96, 96))) / 255.0
    lab = rgb2lab(a).reshape(-1, 3)
    rng = np.random.default_rng(0); c = lab[rng.choice(len(lab), k, replace=False)]
    for _ in range(20):
        lab_c = ((lab[:, None] - c[None]) ** 2).sum(-1).argmin(1)
        c = np.array([lab[lab_c == i].mean(0) if (lab_c == i).any() else c[i] for i in range(k)])
    return c

def distanza_palette(a, b):
    d = np.sqrt(((a[:, None] - b[None]) ** 2).sum(-1))
    return float((d.min(1).mean() + d.min(0).mean()) / 2)  # ΔE medio simmetrico

# --- caso ----------------------------------------------------------------------
def misura(caso):
    t0 = time.time(); r = {"immagine": caso["immagine"]}
    img = Image.open(caso["immagine"]); rif = Image.open(caso["riferimento"])
    sk = scheletri(img); r["persone"] = len(sk); r["persona_riconosciuta"] = bool(sk) and not sk[0]["senza_rilevatore"]
    if caso.get("posa") and sk:
        tgt = json.load(open(caso["posa"]))[0]["people"][0]["pose_keypoints_2d"]
        tgt = np.array(tgt).reshape(-1, 3); tgt[:, 0] /= 1; 
        t = json.load(open(caso["posa"]))[0]; tgt[:, 0] /= t["canvas_width"]; tgt[:, 1] /= t["canvas_height"]
        r["posa"], r["arti_confrontati"] = [round(x, 3) if isinstance(x, float) else x for x in somiglianza_posa(tgt, sk[0]["corpo"])]
    crop = riquadro(sk[0], img) if sk else img
    sk_r = scheletri(rif); crop_r = riquadro(sk_r[0], rif) if sk_r else rif
    r["identita"] = round(float(dino(crop) @ dino(crop_r)), 3)
    p, lg = siglip(img, [caso["descrizione"]]); r["testo"] = round(lg[0], 2)
    segni = {}
    for s in caso.get("segni", []):
        sp, _ = siglip(crop, [f"a character with {s}", f"a character without {s}"]); segni[s] = round(sp[0] / (sp[0] + sp[1] + 1e-9), 3)
    r["segni_siglip"] = segni
    if caso.get("giudice", True):
        r["giudice"] = giudice(img, caso.get("segni", []))
    r["ocr"] = testo_spurio(img)
    if caso.get("stile"):
        r["stile_dE"] = round(distanza_palette(palette(img), palette(Image.open(caso["stile"]))), 1)
    r["secondi"] = round(time.time() - t0, 1)
    return r

if __name__ == "__main__":
    casi = json.load(open(sys.argv[1]))
    for c in casi:
        print(json.dumps(misura(c), ensure_ascii=False), flush=True)

# --- punteggio e cancello (soglie PROVVISORIE: si tarano sui voti ciechi del DM, come ADR-0093 per la prosa) ---
SOGLIE = {"posa": 0.85, "identita": 0.60, "glitch": 0.70, "segno": 0.60}

def libera():
    """svuota i modelli del banco: sul profilo cpu ComfyUI e il giudice non stanno insieme in 16 GB di RAM."""
    import gc
    for f in (_vlm, _siglip, _dino):
        f.cache_clear()
    gc.collect()
    try:  # restituisce al sistema la memoria che glibc tiene da parte (Linux)
        import ctypes; ctypes.CDLL("libc.so.6").malloc_trim(0)
    except OSError:
        pass

def punteggio(m):
    g = m.get("giudice", {})
    glitch = [v for k, v in g.items() if not k.startswith("segno:")]
    segni = [v for k, v in g.items() if k.startswith("segno:")]
    parti = [(m.get("posa", 1.0), 0.25), (m.get("identita", 0.0), 0.25),
             (min(glitch) if glitch else 1.0, 0.30), (sum(segni) / len(segni) if segni else 1.0, 0.15),
             (0.0 if m.get("ocr") else 1.0, 0.05)]
    return round(sum(v * w for v, w in parti), 3)

def cancello(m):
    motivi = []
    if "posa" in m and m["posa"] < SOGLIE["posa"]: motivi.append(f"posa {m['posa']}")
    if m.get("identita", 1) < SOGLIE["identita"]: motivi.append(f"identità {m['identita']}")
    for k, v in m.get("giudice", {}).items():
        if v < (SOGLIE["segno"] if k.startswith("segno:") else SOGLIE["glitch"]): motivi.append(f"{k} {v}")
    if m.get("ocr"): motivi.append(f"testo nell'immagine {m['ocr']}")
    if not m.get("persona_riconosciuta", True): motivi.append("figura non riconosciuta dal rilevatore di persone")
    return {"passa": not motivi, "motivi": motivi}
