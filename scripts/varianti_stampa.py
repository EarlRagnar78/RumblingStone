#!/usr/bin/env python3
"""varianti_stampa.py — le varianti di impaginazione di un booklet, misurate e
messe alla cieca (piano dello standard di stampa, D3 e I6).

Compila lo stesso booklet una volta per variante, passando al tema i valori
con ``typst compile --input``; misura ogni PDF con ``misura_stampa`` e scarta
la variante che peggiora una misura con tetto rispetto al libro di sempre.
Con le varianti rimaste prepara il fascicolo per la scelta alla cieca del DM:
coppie di pagine con lo stesso testo, una per versione, in ordine casuale, e
la chiave in un file a parte.

    python3 scripts/varianti_stampa.py MANIFEST.json --out CARTELLA [--seme N]

Le varianti sono in ``VARIANTI``; una variante nuova si aggiunge lì e nel tema
(`VARIANTE` in tema-rumblingstone.typ).
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import misura_stampa as ms  # noqa: E402

#: nome → (valori per il tema, cosa cambia rispetto al libro di sempre, quali pagine mostrare)
VARIANTI: dict[str, tuple[dict[str, str], str, str]] = {
    "base": ({}, "il libro di sempre: interlinea 1,30, box da leggere nel riquadro", "testo"),
    "interlinea-stretta": ({"interlinea": "0.42em"},
                           "interlinea stretta, vicina a Red Hand of Doom (1,10)", "testo"),
    "leggi-colore": ({"leggi": "colore"},
                     "box da leggere senza riquadro, in corsivo colorato", "leggi"),
}

#: Le misure che una variante non può peggiorare (le stesse con tetto in CI).
MISURE_CON_TETTO = ("testi_sotto_minimo", "fuori_margine", "schede_spezzate", "font_non_incorporati",
                    "rimandi_sbagliati")

def compila_variante(mp: Path, nome: str, valori: dict[str, str], cartella: Path) -> Path:
    man = json.loads(mp.read_text(encoding="utf-8"))
    typ = mp.parent / f".{mp.name.replace('.manifest.json', '')}.{nome}.typ"
    pdf = cartella / f"{nome}.pdf"
    typ.write_text(ex.sorgente(man, mp.parent, True, formato=man.get("formato", "a4")),
                   encoding="utf-8")
    ingressi = [x for k, v in valori.items() for x in ("--input", f"{k}={v}")]
    try:
        cmd = ["typst", "compile", *ms.SOLO_FONT_DEL_REPO, *ingressi, "--root", str(ROOT),
               "--package-path", str(ex.PACCHETTI)]
        esito = subprocess.run(cmd + [str(typ), str(pdf)], capture_output=True, text=True)
        if esito.returncode != 0 and "internal error" in esito.stderr:
            esito = subprocess.run(cmd + ["--no-pdf-tags", str(typ), str(pdf)],
                                   capture_output=True, text=True)
        if esito.returncode != 0:
            raise RuntimeError(f"{nome}: typst non compila\n{esito.stderr[-1500:]}")
        schede = schede_con(typ, ingressi)
        pagine_leggi = interroga(typ, ingressi, "query(<leggi>).map(m => m.location().page())")
    finally:
        typ.unlink(missing_ok=True)
    misura = ms.misura_pdf(pdf, schede, man.get("formato", "a4"))
    misura["interlinea"] = interlinea(pdf)
    misura["pagine_leggi"] = sorted(set(pagine_leggi))
    (cartella / f"{nome}.json").write_text(
        json.dumps({k: v for k, v in misura.items() if k != "dettaglio"}, indent=1,
                   ensure_ascii=False), encoding="utf-8")
    return pdf


def interroga(typ: Path, ingressi: list[str], espressione: str):
    """Un `typst eval` sul documento, con gli stessi --input della variante."""
    cmd = ["typst", "eval", "--in", str(typ), *ms.SOLO_FONT_DEL_REPO, *ingressi,
           "--root", str(ROOT), "--package-path", str(ex.PACCHETTI), espressione]
    esito = subprocess.run(cmd, capture_output=True, text=True)
    if esito.returncode != 0:
        raise RuntimeError(f"typst eval: {esito.stderr[-1000:]}")
    return json.loads(esito.stdout or "[]")


def schede_con(typ: Path, ingressi: list[str]) -> list[dict]:
    """Come ``misura_stampa.interroga_schede``, con gli stessi --input della variante."""
    return ms.accoppia_segnaposti(interroga(typ, ingressi, (
        "query(selector(<sb-inizio>).or(<sb-fine>))"
        ".map(m => (str(m.label), m.value, m.location().page()))")))


def interlinea(pdf: Path) -> float | None:
    """La distanza mediana fra due righe del corpo, diviso il corpo."""
    import pymupdf
    salti = []
    corpo = None
    for pagina in pymupdf.open(pdf):
        righe = []
        for b in pagina.get_text("dict")["blocks"]:
            for r in b.get("lines", []):
                sp = [s for s in r["spans"] if s["text"].strip()]
                if sp and len("".join(s["text"] for s in sp)) > 40:
                    dim = max(sp, key=lambda s: len(s["text"]))["size"]
                    righe.append((round(r["bbox"][0]), r["bbox"][3], dim))
        if not righe:
            continue
        corpo = corpo or statistics.mode(round(d, 1) for _, _, d in righe)
        for x in {x for x, _, _ in righe}:
            ys = sorted(y for xx, y, d in righe if abs(xx - x) < 30 and abs(d - corpo) < 0.3)
            salti += [b - a for a, b in zip(ys, ys[1:]) if 0 < b - a < corpo * 2]
    return round(statistics.median(salti) / corpo, 2) if salti and corpo else None


def peggiora(base: dict, variante: dict) -> list[str]:
    return [m for m in MISURE_CON_TETTO
            if ms.valore(variante, m) > ms.valore(base, m)]


def pagine_campione(pdf: Path, pagine: list[int] | None, quante: int, seme: int) -> list[str]:
    """Una riga di testo di alcune pagine: l'ancora con cui ritrovare la stessa
    pagina nelle altre versioni. ``pagine``: solo fra queste (i box da leggere)."""
    import pymupdf
    doc = pymupdf.open(pdf)
    candidate = []
    for n, pagina in enumerate(doc, 1):
        if n < 4 or n > len(doc) - 3 or (pagine is not None and n not in pagine):
            continue
        testo = [s["text"].strip() for b in pagina.get_text("dict")["blocks"]
                 for r in b.get("lines", []) for s in r["spans"]
                 if len(s["text"].strip()) > 50 and ". . ." not in s["text"]]
        if len(testo) > 20:
            candidate.append(testo[len(testo) // 2][:45])
    random.Random(seme).shuffle(candidate)
    return candidate[:quante]


def pagina_con(pdf: Path, ancora: str) -> int | None:
    import pymupdf
    for n, pagina in enumerate(pymupdf.open(pdf)):
        if pagina.search_for(ancora):
            return n
    return None


def fascicolo_cieco(coppie: list[tuple[str, Path, Path, str]], out: Path, seme: int) -> dict:
    """Un PDF a coppie affiancate e la chiave: quale lato è quale versione."""
    import pymupdf
    rnd = random.Random(seme)
    doc = pymupdf.open()
    chiave = {}
    for i, (variante, base_pdf, var_pdf, ancora) in enumerate(coppie, 1):
        pagine = [(base_pdf, "base"), (var_pdf, variante)]
        rnd.shuffle(pagine)
        sorgenti = [(pymupdf.open(p), pagina_con(p, ancora), nome) for p, nome in pagine]
        if any(n is None for _, n, _ in sorgenti):
            continue
        w, h = sorgenti[0][0][0].rect.width, sorgenti[0][0][0].rect.height
        foglio = doc.new_page(width=2 * w + 20, height=h + 40)
        foglio.insert_text((20, 26), f"Coppia {len(chiave) + 1}: sinistra o destra?", fontsize=14)
        for lato, (d, n, _) in enumerate(sorgenti):
            foglio.show_pdf_page(pymupdf.Rect(lato * (w + 20), 40, lato * (w + 20) + w, 40 + h), d, n)
        chiave[str(len(chiave) + 1)] = {"sinistra": sorgenti[0][2], "destra": sorgenti[1][2],
                                        "ancora": ancora}
    doc.save(out)
    return chiave


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest")
    ap.add_argument("--out", required=True, help="cartella del fascicolo cieco (fuori dal repo)")
    ap.add_argument("--seme", type=int, default=20261029)
    ap.add_argument("--coppie", type=int, default=4, help="coppie per variante")
    args = ap.parse_args(argv)
    mp, out = Path(args.manifest), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pdf, misure = {}, {}
    for nome, (valori, _, _) in VARIANTI.items():
        pdf[nome] = compila_variante(mp, nome, valori, out)
        misure[nome] = json.loads((out / f"{nome}.json").read_text(encoding="utf-8"))
    print(f"{'variante':22} {'pag':>4} {'interl':>6} {'<7pt':>5} {'marg':>5} {'spezz':>5}  esito")
    tenute = []
    for nome, (_, descrizione, _) in VARIANTI.items():
        m = misure[nome]
        peggio = [] if nome == "base" else peggiora(misure["base"], m)
        esito = "scartata: peggiora " + ", ".join(peggio) if peggio else "tenuta"
        print(f"{nome:22} {m['pagine']:>4} {m['interlinea'] or '-':>6} {m['testi_sotto_minimo']:>5} "
              f"{m['fuori_margine']:>5} {m['schede_spezzate']:>5}  {esito}")
        if nome != "base" and not peggio:
            tenute.append(nome)
    coppie = []
    for nome in tenute:
        pagine = misure["base"]["pagine_leggi"] if VARIANTI[nome][2] == "leggi" else None
        for ancora in pagine_campione(pdf["base"], pagine, args.coppie, args.seme):
            coppie.append((nome, pdf["base"], pdf[nome], ancora))
    random.Random(args.seme).shuffle(coppie)
    chiave = fascicolo_cieco(coppie, out / "CIECO.pdf", args.seme)
    (out / "CHIAVE.json").write_text(json.dumps(
        {"varianti": {n: VARIANTI[n][1] for n in VARIANTI}, "coppie": chiave,
         "misure": misure}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"✓ {len(chiave)} coppie in {out / 'CIECO.pdf'}; la chiave in CHIAVE.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
