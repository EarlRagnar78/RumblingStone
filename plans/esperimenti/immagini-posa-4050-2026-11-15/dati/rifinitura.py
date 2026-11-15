"""rifinitura.py — i passaggi deterministici della pipeline, su CPU.

  maschere_glitch  rettangoli di mani e volti (DWPose) da ridipingere con un passaggio di dettaglio
  armonizza        porta l'immagine verso la palette della bibbia visiva dell'arco (trasferimento Reinhard in Lab)
  scontorna        ritaglia il PG dallo sfondo (BiRefNet, MIT)
  componi          mette il PG ritagliato nella scena, alla scala e nel punto del riquadro, con ombra a terra
"""
import numpy as np
from PIL import Image, ImageFilter
from functools import lru_cache

def maschere_glitch(img, scheletri, margine=0.35):
    W, H = img.size; out = []
    for sk in scheletri:
        for mano in sk["mani"]:
            if len(mano) and (mano[:, 2] > 0.3).sum() > 5:
                pts = mano[mano[:, 2] > 0.3][:, :2] / np.array([W, H]) if mano[:, :2].max() > 2 else mano[mano[:, 2] > 0.3][:, :2]
                out.append(("mano", _box(pts, margine, W, H)))
        viso = sk["corpo"][[0, 14, 15, 16, 17]]
        v = viso[viso[:, 2] > 0.3][:, :2]
        if len(v) >= 2:
            out.append(("volto", _box(v, 1.2, W, H)))
    return out

def _box(p, m, W, H):
    x0, y0 = p.min(0); x1, y1 = p.max(0); s = max(x1 - x0, (y1 - y0) * H / W, 0.04)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; h = s * (1 + m) / 2
    return (int(max(0, cx - h) * W), int(max(0, cy - h * W / H) * H), int(min(1, cx + h) * W), int(min(1, cy + h * W / H) * H))

def armonizza(img, stile, forza=0.6):
    from skimage.color import rgb2lab, lab2rgb
    a = rgb2lab(np.asarray(img.convert("RGB")) / 255.0); s = rgb2lab(np.asarray(stile.convert("RGB").resize((256, 256))) / 255.0)
    ma, sa = a.reshape(-1, 3).mean(0), a.reshape(-1, 3).std(0) + 1e-6
    ms, ss = s.reshape(-1, 3).mean(0), s.reshape(-1, 3).std(0)
    t = (a - ma) / sa * ss + ms
    t[..., 0] = a[..., 0] * (1 - forza * 0.5) + t[..., 0] * forza * 0.5  # la luminanza si sposta meno: tiene i volumi
    out = a * (1 - forza) + t * forza; out[..., 0] = t[..., 0]
    return Image.fromarray((np.clip(lab2rgb(out), 0, 1) * 255).astype("uint8"))

@lru_cache(None)
def _birefnet():
    import torch
    from transformers import AutoModelForImageSegmentation
    return AutoModelForImageSegmentation.from_pretrained("ZhengPeng7/BiRefNet", trust_remote_code=True).eval().float()

def libera():
    import gc; _birefnet.cache_clear(); gc.collect()
    try:
        import ctypes; ctypes.CDLL("libc.so.6").malloc_trim(0)
    except OSError:
        pass

def scontorna(img):
    import torch
    from torchvision import transforms
    m = _birefnet(); im = img.convert("RGB")
    tf = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    with torch.no_grad():
        pred = m(tf(im).unsqueeze(0))[-1].sigmoid()[0, 0]
    alpha = Image.fromarray((pred.numpy() * 255).astype("uint8")).resize(im.size)
    im.putalpha(alpha); return im

def componi(scena, pg_rgba, box, ombra=0.45):
    """box = (x0, y0, x1, y1) in frazioni della scena; il PG si appoggia al bordo basso del riquadro."""
    sc = scena.convert("RGBA"); W, H = sc.size
    bb = pg_rgba.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
    pg = pg_rgba.crop(bb)
    h = int((box[3] - box[1]) * H); w = int(pg.width * h / pg.height)
    pg = pg.resize((w, h), Image.LANCZOS)
    x = int((box[0] + box[2]) / 2 * W - w / 2); y = int(box[3] * H - h)
    sh = Image.new("RGBA", (w, max(8, h // 12)), (0, 0, 0, 0))
    sh_a = Image.new("L", sh.size, 0); sh_a.paste(int(255 * ombra), (w // 8, 0, w - w // 8, sh.height)); sh_a = sh_a.filter(ImageFilter.GaussianBlur(h // 40 + 2))
    sh.putalpha(sh_a); sc.alpha_composite(sh, (x, y + h - sh.height // 2))
    sc.alpha_composite(pg, (x, y)); return sc.convert("RGB")
