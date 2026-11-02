#!/usr/bin/env python3
"""
confronta_versioni.py — due versioni della stessa mappa, misurate e affiancate.

Prova del 2026-10-22 (RICERCA-STRUMENTI-MAPPE.md §3). In sola lettura sul repo;
scrive solo dove dice --out.

Misure, tutte deterministiche:
  - Hamming sui simboli e sulle classi di cella (quote sul totale);
  - Jaccard per classe (muro, percorribile, copertura, creature, porte);
  - matrice delle transizioni di classe (es. M→. = muro diventato pavimento);
  - NCD, normalized compression distance con lzma (Li et al. 2004), sulla
    griglia come testo;
  - delta delle metriche e del voto di qualita_mappe.py, e dei rilievi
    comparsi o spariti;
  - con --profonde, anche il delta di metriche_nuove.py (VGA, simmetria, pattern).

L'SVG affianca le due rese del renderer vero, con le celle cambiate cerchiate
sulle due: rosso dove compare un blocco, verde dove sparisce, ambra il resto.

Uso:
    python3 confronta_versioni.py VECCHIA.md[:N] NUOVA.md[:N] [--out DIR] [--profonde]
"""
from __future__ import annotations

import argparse
import json
import lzma
import re
import sys
from collections import Counter
from pathlib import Path

from _comune import C, Q, R, REPO, collaudo, griglia_classi, impronta, mappe_di

CELL, MARGIN, OY = R.CELL, R.MARGIN, 58 + 22
BLOCCHI = set("MO")
PERCORRIBILE = set(".KHUPS")


def leggi(arg: str):
    p, _, n = arg.partition(":")
    f = Path(p) if Path(p).is_absolute() else (Path.cwd() / p if (Path.cwd() / p).exists() else REPO / p)
    mappe = mappe_di(f)
    i = int(n) if n else 1
    return f, i, mappe[i - 1]


def misura(f, i, g):
    q = Q.Qualita(collaudo(f, i, g)).esegui()
    ril = sorted({f"{r['codice']}@{r['cella']}" for r in q.rilievi + q.c.rilievi if not r["deroga"]})
    return q, ril


def ncd(a: str, b: str) -> float:
    z = lambda s: len(lzma.compress(s.encode("utf-8"), preset=9))  # noqa: E731
    ca, cb, cab = z(a), z(b), z(a + "\n" + b)
    return round((cab - min(ca, cb)) / max(ca, cb), 4)


def confronta(A, B, profonde=False) -> dict:
    (fa, ia, ga), (fb, ib, gb) = A, B
    GA, GB = C.Griglia(ga), C.Griglia(gb)
    W, H = max(GA.W, GB.W), max(GA.H, GB.H)
    ka = [r.ljust(W, "V") for r in griglia_classi(GA)] + ["V" * W] * (H - GA.H)
    kb = [r.ljust(W, "V") for r in griglia_classi(GB)] + ["V" * W] * (H - GB.H)
    cambi, trans, simboli_diversi = [], Counter(), 0
    for y in range(H):
        for x in range(W):
            sa, sb = GA.at(x, y), GB.at(x, y)
            if sa != sb:
                simboli_diversi += 1
                cambi.append((x, y, ka[y][x], kb[y][x]))
            if ka[y][x] != kb[y][x]:
                trans[f"{ka[y][x]}→{kb[y][x]}"] += 1
    tot = W * H

    def insieme(K, classi):
        return {(x, y) for y in range(H) for x in range(W) if K[y][x] in classi}

    jac = {}
    for nome, cl in (("muro", "M"), ("blocco", "MO"), ("percorribile", PERCORRIBILE), ("copertura", "K"),
                     ("creature", "U"), ("porte", "P"), ("pericolo", "H")):
        a, b = insieme(ka, set(cl)), insieme(kb, set(cl))
        jac[nome] = None if not (a | b) else round(len(a & b) / len(a | b), 4)
    qa, ra = misura(fa, ia, ga)
    qb, rb = misura(fb, ib, gb)
    delta = {}
    for k in sorted(set(qa.m) | set(qb.m)):
        va, vb = qa.m.get(k), qb.m.get(k)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and va != vb:
            delta[k] = {"prima": va, "dopo": vb, "delta": round(vb - va, 3)}
    out = {
        "vecchia": {"file": str(fa.relative_to(REPO)) if fa.is_relative_to(REPO) else fa.name, "mappa": ia, "dimensioni": [GA.W, GA.H], "voto": qa.voto()},
        "nuova": {"file": str(fb.relative_to(REPO)) if fb.is_relative_to(REPO) else fb.name, "mappa": ib, "dimensioni": [GB.W, GB.H], "voto": qb.voto()},
        "stesse_dimensioni": (GA.W, GA.H) == (GB.W, GB.H),
        "hamming_simboli": {"celle": simboli_diversi, "quota": round(simboli_diversi / tot, 4)},
        "hamming_classi": {"celle": sum(trans.values()), "quota": round(sum(trans.values()) / tot, 4)},
        "transizioni": dict(sorted(trans.items(), key=lambda kv: (-kv[1], kv[0]))),
        "jaccard": jac,
        "ncd_lzma": ncd("\n".join(" ".join(GA.at(x, y) or "" for x in range(GA.W)) for y in range(GA.H)),
                        "\n".join(" ".join(GB.at(x, y) or "" for x in range(GB.W)) for y in range(GB.H))),
        "voto": {"prima": qa.voto(), "dopo": qb.voto(), "delta": qb.voto() - qa.voto()},
        "metriche_delta": delta,
        "rilievi_spariti": sorted(set(ra) - set(rb)),
        "rilievi_comparsi": sorted(set(rb) - set(ra)),
        "_cambi": cambi,
    }
    if profonde:
        import metriche_nuove as MN
        rif = MN.corpus_pattern()
        ma, mb = MN.metriche(fa, ia, ga, rif), MN.metriche(fb, ib, gb, rif)
        out["profonde"] = {"prima": ma, "dopo": mb}
    return out


def _prefissa(svg: str, p: str) -> str:
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', svg)
    return re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', svg)


def svg_affiancato(A, B, esito) -> str:
    (fa, _, ga), (fb, _, gb) = A, B
    sa = _prefissa(R.render_svg(ga, fa.name), "a_")
    sb = _prefissa(R.render_svg(gb, fb.name), "b_")
    dim = lambda s: tuple(float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', s).groups())  # noqa: E731
    wa, ha = dim(sa)
    wb, hb = dim(sb)
    gap, testa = 30, 70
    W, H = wa + gap + wb, max(ha, hb) + testa
    righe = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}" height="{H:g}" viewBox="0 0 {W:g} {H:g}" '
             'font-family="sans-serif">', f'<rect width="{W:g}" height="{H:g}" fill="#ffffff"/>']
    v, n = esito["voto"]["prima"], esito["voto"]["dopo"]
    righe.append(f'<text x="12" y="26" font-size="18" font-weight="bold">Prima (voto {v}) · Dopo (voto {n}) · '
                 f'{esito["hamming_simboli"]["celle"]} celle cambiate ({esito["hamming_simboli"]["quota"]:.1%}) · '
                 f'NCD {esito["ncd_lzma"]}</text>')
    righe.append('<text x="12" y="50" font-size="13">rosso: compare un blocco · verde: sparisce un blocco · '
                 'ambra: altro cambio. Le celle sono cerchiate su entrambe le versioni.</text>')
    for dx, s in ((0, sa), (wa + gap, sb)):
        corpo = re.sub(r"^<svg[^>]*>", "", s.strip())
        corpo = re.sub(r"</svg>\s*$", "", corpo)
        righe.append(f'<g transform="translate({dx:g},{testa})">{corpo}')
        for x, y, ka, kb in esito["_cambi"]:
            col = "#d62728" if kb in BLOCCHI and ka not in BLOCCHI else (
                "#2ca02c" if ka in BLOCCHI and kb not in BLOCCHI else "#ff9f1a")
            righe.append(f'<rect x="{MARGIN + x * CELL + 1.5}" y="{OY + y * CELL + 1.5}" width="{CELL - 3}" '
                         f'height="{CELL - 3}" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="3"/>')
        righe.append("</g>")
    righe.append("</svg>")
    return "\n".join(righe)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("vecchia")
    ap.add_argument("nuova")
    ap.add_argument("--out", help="cartella per confronto.json e confronto.svg")
    ap.add_argument("--profonde", action="store_true")
    a = ap.parse_args(argv)
    A, B = leggi(a.vecchia), leggi(a.nuova)
    esito = confronta(A, B, a.profonde)
    pub = {k: v for k, v in esito.items() if not k.startswith("_")}
    pub["impronta"] = impronta(pub)
    testo = json.dumps(pub, ensure_ascii=False, indent=1, default=str)
    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "confronto.json").write_text(testo + "\n", encoding="utf-8")
        (out / "confronto.svg").write_text(svg_affiancato(A, B, esito), encoding="utf-8")
    print(testo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
