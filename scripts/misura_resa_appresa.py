#!/usr/bin/env python3
"""
misura_resa_appresa.py — il secondo parere: le metriche apprese della community
sulle celle esportate da `misura_resa.py --celle` (D26 di RESA-ASSET).

Gira sulla macchina del DM, non in CI: vuole torch e `piq` (Apache-2.0), e i
pesi che `piq` scarica al primo uso da GitHub. Le misure:

- **CLIP-IQA** (Wang et al. 2023): qualità percepita senza riferimento, 0-1;
- **LPIPS** (Zhang et al. 2018) e **DISTS** (Ding et al. 2020): distanza
  percettiva fra una cella e la stessa cella della pergamena, cioè quanto la
  resa si allontana dallo stile della casa (più bassa, più vicina).

⚠️ Sono tarate su fotografie, non su icone da 28 px: **non bloccano niente**.
Entrano nella scheda come secondo parere, e diventano un cancello solo se
concordano con le preferenze del DM nel confronto alla cieca (κ ≥ 0,6).

Una volta, sulla macchina del DM (torch solo CPU, circa 200 MB):

    .venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
    .venv/bin/pip install "piq>=0.8"

I pesi (circa 700 MB, nella cache di torch) si scaricano al primo uso, oppure
prima, da soli, con l'impronta di ogni file da incollare nella chat:

    .venv/bin/python scripts/misura_resa_appresa.py --scarica-pesi

Poi:

    .venv/bin/python scripts/misura_resa.py glifi --celle /tmp/celle -o /tmp/glifi.json
    .venv/bin/python scripts/misura_resa_appresa.py /tmp/celle -o /tmp/appresa.json

e il JSON si incolla nella chat o si passa a `misura_resa.py appresa`.
L'uscita registra le versioni e lo sha256 di ogni file di pesi usato.

Exit: 0 ok · 1 cartella vuota o illeggibile · 2 torch o piq assenti.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _carica():
    try:
        import torch
        import piq
        from PIL import Image
    except ImportError as e:
        print(f"✗ manca {e.name}: vedi l'intestazione dello script per l'installazione",
              file=sys.stderr)
        return None
    return torch, piq, Image


def _metriche(piq):
    """CLIP-IQA, LPIPS e DISTS di piq 0.8, senza i suoi avvisi di deprecazione.

    Vengono da dentro piq e non da qui: `torch.jit.load` (CLIP-IQA) e
    `pretrained=` di torchvision (la VGG16 di LPIPS e DISTS). Correggerli spetta
    a piq; il filtro tace solo quei tre messaggi e solo mentre le metriche si
    costruiscono, così un avviso nuovo resta visibile."""
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=r"`torch\.jit\.load` is deprecated", category=FutureWarning)
        warnings.filterwarnings("ignore", message=r"The parameter 'pretrained' is deprecated", category=UserWarning)
        warnings.filterwarnings("ignore", message=r"Arguments other than a weight enum", category=UserWarning)
        return piq.CLIPIQA(), piq.LPIPS(), piq.DISTS()


def _pesi(torch) -> dict[str, str]:
    """sha256 dei file di pesi nella cache di torch: cosa si è usato davvero."""
    out = {}
    cartella = Path(torch.hub.get_dir()) / "checkpoints"
    for f in sorted(cartella.glob("*")) if cartella.exists() else []:
        out[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("celle", type=Path, nargs="?", help="la cartella scritta da misura_resa.py --celle")
    ap.add_argument("-o", "--uscita", type=Path)
    ap.add_argument("--scarica-pesi", action="store_true",
                    help="scarica soltanto i pesi delle tre metriche e ne stampa lo sha256")
    args = ap.parse_args(argv)
    if not args.scarica_pesi and not (args.celle and args.uscita):
        ap.error("servono la cartella delle celle e -o, oppure --scarica-pesi")
    lib = _carica()
    if lib is None:
        return 2
    torch, piq, Image = lib
    if args.scarica_pesi:
        _metriche(piq)
        print(f"torch {torch.__version__} · piq {piq.__version__} · cache {torch.hub.get_dir()}")
        for nome, sha in _pesi(torch).items():
            print(f"  {sha}  {nome}")
        return 0
    file = sorted(args.celle.glob("*.png"))
    if not file:
        print(f"✗ nessuna cella in {args.celle}", file=sys.stderr)
        return 1

    def tensore(p: Path):
        im = Image.open(p).convert("RGB").resize((224, 224), Image.BICUBIC)
        # np.asarray e non getdata(), deprecato da Pillow 12 (via in Pillow 14)
        t = torch.from_numpy(np.asarray(im, dtype=np.float32) / 255.0)
        return t.permute(2, 0, 1).unsqueeze(0)

    import numpy as np
    clip_iqa, lpips, dists = _metriche(piq)
    # nome: <tema>-<ambiente>-<codice>-<fonte>.png; il riferimento è la pergamena col glifo
    misure, riferimenti = {}, {}
    for p in file:
        tema, amb, codice, fonte = p.stem.split("-", 3)
        if tema == "pergamena" and fonte == "glifo":
            riferimenti[(amb, codice)] = tensore(p)
    with torch.no_grad():
        for p in file:
            tema, amb, codice, fonte = p.stem.split("-", 3)
            x = tensore(p)
            voce = {"clip_iqa": round(float(clip_iqa(x)), 4)}
            rif = riferimenti.get((amb, codice))
            if rif is not None and not (tema == "pergamena" and fonte == "glifo"):
                voce["lpips_dalla_pergamena"] = round(float(lpips(x, rif)), 4)
                voce["dists_dalla_pergamena"] = round(float(dists(x, rif)), 4)
            misure[p.stem] = voce
    uscita = {"strumento": "misura_resa_appresa.py", "torch": torch.__version__,
              "piq": piq.__version__, "pesi": _pesi(torch), "misure": misure}
    args.uscita.write_text(json.dumps(uscita, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✓ {len(misure)} celle misurate in {args.uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
