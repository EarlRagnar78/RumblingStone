#!/usr/bin/env python3
"""
confronta_mappe.py — due o piu' versioni delle stesse mappe, misurate e affiancate.

Il collaudo (``collaudo_mappe.py``) e la qualita' (``qualita_mappe.py``) dicono
com'e' una mappa. Questo strumento dice quanto e' cambiata da una versione
all'altra, cella per cella, e con quale effetto sul voto. Nato come prova del
2026-10-22 (``plans/esperimenti/mappe-strumenti-2026-10-22/confronta_versioni.py``).

Misure, tutte deterministiche:

  - celle cambiate: simboli diversi e classi diverse, in numero e in quota
    sull'area comune (la griglia piu' grande delle due);
  - Jaccard per classe di cella (M muro, O ostacolo, P porta, S scala, H
    pericolo, K copertura, U creatura, . pavimento) e per i gruppi blocco
    (M+O) e percorribile (il resto);
  - transizioni di classe, dalla piu' frequente (``M→.`` = muro diventato
    pavimento);
  - NCD con lzma (Li et al. 2004) sulla griglia come testo;
  - voto di ``qualita_mappe.py`` prima e dopo, penalita' e rilievi non
    derogati spariti e comparsi (``codice@cella``); i derogati a parte, perche'
    un rilievo sparito per deroga non e' un rilievo corretto;
  - dimensioni in quadretti, scala (come la legge ``qualita_mappe.py``, e se
    la riga DIMENSIONI sta dentro la griglia), quota e dislivello dichiarati.

Il voto si calcola come lo calcola ``qualita_mappe.py``: tutte le mappe dei
file della stessa versione insieme, con il controllo delle quote fra mappe
dello stesso ``@luogo``. Un ``@collega`` verso un altro file si risolve sul
file del repo, non sulla sua versione storica.

L'SVG affianca le rese del renderer vero (``render_map_svg.py``) e cerchia le
celle cambiate: rosso dove compare un blocco, verde dove sparisce, ambra ogni
altro cambio di simbolo.

Uso:
    # una coppia: due file, con il numero della mappa (da 1, default 1)
    python3 scripts/confronta_mappe.py VECCHIA.md[:N] NUOVA.md[:N] [--json OUT] [--svg OUT]

    # piu' versioni git degli stessi master, ciascuna contro la base
    python3 scripts/confronta_mappe.py --versioni A=d726e6a2 B=9359a0af C=HEAD \\
        --base C --estrai DIR --out DIR FILE.md [...]

Con ``--versioni`` ogni file si estrae con ``git show <ref>:<file>`` in
``--estrai`` (default: una cartella temporanea). Le mappe si abbinano per
titolo identico, poi per codice (``MAPPA 1A-3``), poi per posizione fra quelle
rimaste. In ``--out`` vanno ``confronto.json`` e ``svg/<file>-<n>-<codice>.svg``,
un pannello per versione. Il JSON ha le chiavi ordinate e nessun dato che
dipenda dalla macchina o dall'ora: le versioni si identificano con il blob git
del file, che non cambia se il contenuto non cambia.

Exit: 0 confronto prodotto · 1 con --strict, una mappa senza corrispondente in
qualche versione · 2 errore d'uso (file o ref inesistente, mappa fuori numero,
dipendenze mancanti). Legge il repo, scrive solo in --json, --svg, --out ed
--estrai.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
sys.path.insert(0, str(RADICE))
import collaudo_mappe as C  # noqa: E402
import qualita_mappe as Q  # noqa: E402

R, F, MODO, FUORI = C.R, C.F, C.MODO, C.FUORI
CLASSI = "MOPSHKU."
BLOCCHI = set("MO")
PERCORRIBILE = set(".KHUPS")
CODICE = re.compile(r"MAPPA\s+([0-9A-Z][0-9A-Za-z]*(?:-[0-9A-Za-z]+)*)")
ROSSO, VERDE, AMBRA = "#d62728", "#2ca02c", "#ff9f1a"


# --- lettura ---------------------------------------------------------------

def classe(c) -> str:
    """La classe di una cella. M muro · O ostacolo che non ferma la vista ·
    P porta · S scala o botola · H pericolo · K copertura senza blocco ·
    U creatura · . pavimento · V fuori griglia."""
    if c in (None, FUORI):
        return "V"
    f = F.get(c, {})
    if MODO.get(c) == "unit":
        return "U"
    if f.get("door"):
        return "P"
    if f.get("posa") == "fra_livelli":
        return "S"
    if f.get("blocks_movement") and f.get("blocks_sight"):
        return "M"
    if f.get("blocks_movement"):
        return "O"
    if f.get("hazard"):
        return "H"
    if f.get("cover") in ("half", "three_quarters", "total"):
        return "K"
    return "."


def codice_di(titolo: str) -> str | None:
    m = CODICE.search(titolo or "")
    return m.group(1).upper() if m else None


def misura_file(files: list[Path]) -> dict:
    """{(file, n): Qualita} per tutte le mappe dei file, come qualita_mappe.py
    le misura in un giro solo (quote fra mappe dello stesso @luogo comprese)."""
    corpus: dict = {}
    esiti, chiavi = [], []
    for f in files:
        qs = Q.misura(f, corpus)
        esiti += qs
        chiavi += [(f, i) for i in range(1, len(qs) + 1)]
    Q.confronta_luoghi(esiti)
    return dict(zip(chiavi, esiti))


def rilievi(q) -> list[str]:
    return sorted({f"{r['codice']}@{r['cella'] or '-'}" for r in q.rilievi + q.c.rilievi if not r["deroga"]})


def scheda(q) -> dict:
    """Quello che serve di una versione: titolo, misure, voto, rilievi."""
    G, g = q.c.G, q.c.G.g
    return {
        "titolo": g.get("title"),
        "codice": codice_di(g.get("title")),
        "dimensioni_quadretti": [G.W, G.H],
        "scala_m": q.m.get("scala_m"),
        "scala_nella_griglia": g.get("scale_m") is not None,
        "dimensioni_dichiarate": g.get("declared_dims"),
        "quota": q.m.get("quota"),
        "dislivello": q.m.get("dislivello"),
        "voto": q.voto(),
        "penalita": dict(sorted(q.penalita().items())),
        "rilievi": rilievi(q),
        "rilievi_derogati": sorted({f"{r['codice']}@{r['cella'] or '-'}" for r in q.rilievi + q.c.rilievi
                                    if r["deroga"]}),
    }


# --- misure ----------------------------------------------------------------

def _testo(G) -> str:
    return "\n".join(" ".join(G.at(x, y) or "" for x in range(G.W)) for y in range(G.H))


def ncd(a: str, b: str) -> float:
    def z(s):
        return len(lzma.compress(s.encode("utf-8"), preset=9))
    ca, cb, cab = z(a), z(b), z(a + "\n" + b)
    return round((cab - min(ca, cb)) / max(ca, cb), 4)


def _jaccard(ka, kb, W, H, classi) -> float | None:
    a = {(x, y) for y in range(H) for x in range(W) if ka[y][x] in classi}
    b = {(x, y) for y in range(H) for x in range(W) if kb[y][x] in classi}
    return None if not (a | b) else round(len(a & b) / len(a | b), 4)


def confronta(qa, qb) -> dict:
    """Le misure fra due versioni gia' collaudate (qa prima, qb dopo).
    La chiave ``_cambi`` (celle cambiate con le classi) serve all'SVG."""
    GA, GB = qa.c.G, qb.c.G
    W, H = max(GA.W, GB.W), max(GA.H, GB.H)
    ka = [[classe(GA.at(x, y)) for x in range(W)] for y in range(H)]
    kb = [[classe(GB.at(x, y)) for x in range(W)] for y in range(H)]
    cambi, trans, simboli = [], Counter(), 0
    for y in range(H):
        for x in range(W):
            if GA.at(x, y) != GB.at(x, y):
                simboli += 1
                cambi.append((x, y, ka[y][x], kb[y][x]))
            if ka[y][x] != kb[y][x]:
                trans[f"{ka[y][x]}→{kb[y][x]}"] += 1
    area = W * H
    n_classi = sum(trans.values())
    ra, rb = rilievi(qa), rilievi(qb)
    delta_metriche = {}
    for k in sorted(set(qa.m) | set(qb.m)):
        va, vb = qa.m.get(k), qb.m.get(k)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and not isinstance(va, bool) \
                and va != vb:
            delta_metriche[k] = {"prima": va, "dopo": vb, "delta": round(vb - va, 3)}
    return {
        "area_quadretti": area,
        "stesse_dimensioni": (GA.W, GA.H) == (GB.W, GB.H),
        "celle_cambiate": {"simboli": simboli, "quota_simboli": round(simboli / area, 4),
                           "classi": n_classi, "quota_classi": round(n_classi / area, 4)},
        "jaccard_classi": {k: _jaccard(ka, kb, W, H, {k}) for k in CLASSI},
        "jaccard_gruppi": {"blocco": _jaccard(ka, kb, W, H, BLOCCHI),
                           "percorribile": _jaccard(ka, kb, W, H, PERCORRIBILE)},
        "transizioni": [[k, v] for k, v in sorted(trans.items(), key=lambda kv: (-kv[1], kv[0]))],
        "ncd_lzma": ncd(_testo(GA), _testo(GB)),
        "voto": {"prima": qa.voto(), "dopo": qb.voto(), "delta": qb.voto() - qa.voto()},
        "metriche_delta": delta_metriche,
        "rilievi_spariti": sorted(set(ra) - set(rb)),
        "rilievi_comparsi": sorted(set(rb) - set(ra)),
        "_cambi": cambi,
    }


def pubblico(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


# --- SVG -------------------------------------------------------------------

def _prefissa(svg: str, p: str) -> str:
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', svg)
    return re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', svg)


def _colore(ka: str, kb: str) -> str:
    if kb in BLOCCHI and ka not in BLOCCHI:
        return ROSSO
    if ka in BLOCCHI and kb not in BLOCCHI:
        return VERDE
    return AMBRA


def svg_affiancato(pannelli: list[tuple[str, object, list]], titolo: str, note: str = "") -> str:
    """pannelli: (etichetta, Qualita, celle da cerchiare). Un pannello per
    versione, da sinistra a destra, con la resa del renderer vero."""
    rese = []
    for k, (etichetta, q, cambi) in enumerate(pannelli):
        s = _prefissa(R.render_svg(q.c.G.g, etichetta), f"p{k}_")
        w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', s).groups())
        rese.append((etichetta, q, cambi, s, w, h))
    gap, testa = 30, 96
    W = sum(r[4] for r in rese) + gap * (len(rese) - 1)
    H = max(r[5] for r in rese) + testa
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}" height="{H:g}" viewBox="0 0 {W:g} {H:g}" '
           'font-family="sans-serif">', f'<rect width="{W:g}" height="{H:g}" fill="#ffffff"/>',
           f'<text x="12" y="26" font-size="18" font-weight="bold">{_xml(titolo)}</text>',
           '<text x="12" y="48" font-size="13">rosso: compare un blocco · verde: sparisce un blocco · '
           'ambra: altro cambio di simbolo</text>']
    if note:
        out.append(f'<text x="12" y="68" font-size="13">{_xml(note)}</text>')
    dx = 0.0
    for etichetta, q, cambi, s, w, _ in rese:
        G = q.c.G
        primo = G.righe[0]
        corpo = re.sub(r"</svg>\s*$", "", re.sub(r"^<svg[^>]*>", "", s.strip()))
        # una cella che in questa versione non esiste (griglia piu' piccola) non si cerchia qui
        visibili = [c for c in cambi if G.at(c[0], c[1]) != FUORI]
        out.append(f'<text x="{dx + 12:g}" y="{testa - 8}" font-size="15" font-weight="bold">'
                   f'{_xml(etichetta)} · voto {q.voto()} · {len(visibili)} celle cerchiate</text>')
        out.append(f'<g transform="translate({dx:g},{testa})">{corpo}')
        oy = 58 + 22  # header_h + 22 in render_map_svg.render_svg
        for x, y, ka, kb in visibili:
            col = _colore(ka, kb)
            cx = R.MARGIN + x * R.CELL + R.CELL / 2
            cy = oy + (G.righe[y] - primo) * R.CELL + R.CELL / 2
            out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R.CELL / 2 - 2:g}" fill="{col}" '
                       f'fill-opacity="0.15" stroke="{col}" stroke-width="2.5"/>')
        out.append("</g>")
        dx += w + gap
    out.append("</svg>")
    return "\n".join(out) + "\n"


def _xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- abbinamento -----------------------------------------------------------

def abbina(vecchie: list[str], nuove: list[str]) -> tuple[dict, list[int], list[int]]:
    """Abbina i titoli delle mappe: {indice nuova: (indice vecchia, metodo)},
    piu' le nuove e le vecchie rimaste sole. Indici da 1. Prima il titolo
    identico, poi il codice MAPPA se e' unico in tutte e due, poi la posizione
    fra quelle rimaste."""
    coppie: dict = {}
    libere_v = list(range(1, len(vecchie) + 1))
    for j, t in enumerate(nuove, 1):
        if t in vecchie and vecchie.index(t) + 1 in libere_v:
            i = vecchie.index(t) + 1
            coppie[j] = (i, "titolo")
            libere_v.remove(i)
    cod_v = Counter(codice_di(t) for t in vecchie)
    cod_n = Counter(codice_di(t) for t in nuove)
    for j, t in enumerate(nuove, 1):
        c = codice_di(t)
        if j in coppie or not c or cod_v[c] != 1 or cod_n[c] != 1:
            continue
        i = [codice_di(v) for v in vecchie].index(c) + 1
        if i in libere_v:
            coppie[j] = (i, "codice")
            libere_v.remove(i)
    rimaste_n = [j for j in range(1, len(nuove) + 1) if j not in coppie]
    for j in list(rimaste_n):
        if j in libere_v:
            coppie[j] = (j, "ordine")
            libere_v.remove(j)
            rimaste_n.remove(j)
    return coppie, rimaste_n, libere_v


# --- modi ------------------------------------------------------------------

def _risolvi(p: str) -> Path:
    f = Path(p)
    if f.is_absolute():
        return f
    return Path.cwd() / f if (Path.cwd() / f).exists() else REPO / f


def coppia(a: argparse.Namespace) -> int:
    lati = []
    for arg in (a.vecchia, a.nuova):
        p, _, n = arg.rpartition(":") if re.search(r":\d+$", arg) else (arg, "", "1")
        f = _risolvi(p)
        if not f.exists():
            print(f"✗ file non trovato: {p}", file=sys.stderr)
            return 2
        lati.append((f, int(n)))
    misure = {}
    for f in sorted({f for f, _ in lati}):
        misure.update(misura_file([f]))
    q = []
    for f, n in lati:
        if (f, n) not in misure:
            print(f"✗ {f.name} non ha la mappa #{n}", file=sys.stderr)
            return 2
        q.append(misure[(f, n)])
    esito = confronta(q[0], q[1])
    pub = {"prima": scheda(q[0]), "dopo": scheda(q[1]), "confronto": pubblico(esito)}
    testo = json.dumps(pub, ensure_ascii=False, indent=1, sort_keys=True)
    if a.json:
        Path(a.json).write_text(testo + "\n", encoding="utf-8")
    if a.svg:
        cel = esito["celle_cambiate"]
        Path(a.svg).write_text(svg_affiancato(
            [("prima", q[0], esito["_cambi"]), ("dopo", q[1], esito["_cambi"])],
            f"{q[1].c.G.g.get('title')} · {cel['simboli']} celle cambiate ({cel['quota_simboli']:.1%})"),
            encoding="utf-8")
    print(testo)
    return 0


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def _nome_svg(rel: str, n: int, codice: str | None) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "-", Path(rel).stem).strip("-")
    return f"{stem}-{n:02d}-{(codice or 'senza-codice').lower()}.svg"


def versioni(a: argparse.Namespace) -> int:
    refs = []
    for v in a.versioni:
        nome, sep, ref = v.partition("=")
        if not sep or not nome or not ref:
            print(f"✗ --versioni vuole NOME=REF, non «{v}»", file=sys.stderr)
            return 2
        refs.append((nome, ref))
    nomi = [n for n, _ in refs]
    if a.base not in nomi or len(set(nomi)) != len(nomi):
        print("✗ --base deve essere uno dei nomi di --versioni, e i nomi devono essere diversi", file=sys.stderr)
        return 2
    rels = []
    for f in a.files:
        p = _risolvi(f).resolve()
        try:
            rels.append(p.relative_to(REPO).as_posix())
        except ValueError:
            print(f"✗ {f} non sta nel repo", file=sys.stderr)
            return 2
    estrai = Path(a.estrai) if a.estrai else Path(tempfile.mkdtemp(prefix="confronta_mappe_"))
    blob: dict = {}
    percorsi: dict = {}
    for nome, ref in refs:
        for rel in rels:
            try:
                blob[(nome, rel)] = _git("rev-parse", f"{ref}:{rel}").strip()
                testo = _git("show", f"{ref}:{rel}")
            except subprocess.CalledProcessError:
                print(f"✗ {rel} non esiste in {ref}", file=sys.stderr)
                return 2
            dest = estrai / nome / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(testo, encoding="utf-8")
            percorsi[(nome, rel)] = dest
    misure = {nome: misura_file([percorsi[(nome, rel)] for rel in rels]) for nome, _ in refs}

    def q_di(nome, rel, n):
        return misure[nome][(percorsi[(nome, rel)], n)]

    def titoli(nome, rel):
        return [q.c.G.g.get("title") or "" for (f, _), q in sorted(misure[nome].items(), key=lambda kv: kv[0][1])
                if f == percorsi[(nome, rel)]]

    out = Path(a.out)
    (out / "svg").mkdir(parents=True, exist_ok=True)
    mappe, soli = [], []
    for rel in rels:
        tb = titoli(a.base, rel)
        abbinate = {}
        for nome, _ in refs:
            if nome == a.base:
                continue
            coppie, sole_n, sole_v = abbina(titoli(nome, rel), tb)
            abbinate[nome] = coppie
            for j in sole_n:
                soli.append({"file": rel, "mappa": j, "titolo": tb[j - 1], "manca_in": nome})
            for i in sole_v:
                soli.append({"file": rel, "mappa_vecchia": i, "titolo": titoli(nome, rel)[i - 1],
                             "sparita_in": a.base, "versione": nome})
        for j in range(1, len(tb) + 1):
            qb = q_di(a.base, rel, j)
            voce = {"file": rel, "mappa": j, "titolo": tb[j - 1], "codice": codice_di(tb[j - 1]),
                    "versioni": {a.base: dict(scheda(qb), mappa=j)}, "confronti": {}}
            pannelli = []
            for nome, _ in refs:
                if nome == a.base:
                    continue
                if j not in abbinate[nome]:
                    continue
                i, metodo = abbinate[nome][j]
                qa = q_di(nome, rel, i)
                esito = confronta(qa, qb)
                voce["versioni"][nome] = dict(scheda(qa), mappa=i, abbinata_per=metodo)
                voce["confronti"][f"{nome}→{a.base}"] = pubblico(esito)
                pannelli.append((f"{nome} ({dict(refs)[nome]})", qa, esito["_cambi"]))
            # la base cerchia i cambi rispetto all'ultima versione che la precede
            ultimo = [n for n, _ in refs if n != a.base and j in abbinate[n]]
            cambi_base = confronta(q_di(ultimo[-1], rel, abbinate[ultimo[-1]][j][0]), qb)["_cambi"] if ultimo else []
            pannelli.append((f"{a.base} ({dict(refs)[a.base]})", qb, cambi_base))
            nome_svg = _nome_svg(rel, j, voce["codice"])
            voce["svg"] = f"svg/{nome_svg}"
            righe_voto = " · ".join(f"{n} {voce['versioni'][n]['voto']}" for n in nomi if n in voce["versioni"])
            nota = ("Pannelli vecchi: celle diverse dalla base. Base: celle diverse dalla versione "
                    f"{ultimo[-1]}." if ultimo else "Nessuna versione precedente abbinata.")
            (out / "svg" / nome_svg).write_text(
                svg_affiancato(pannelli, f"{tb[j - 1]} · voti {righe_voto}", nota), encoding="utf-8")
            mappe.append(voce)
    risultato = {
        "schema": "map_versions/1",
        "strumento": "scripts/confronta_mappe.py",
        "base": a.base,
        "versioni": {n: {"ref": r, "blob": {rel: blob[(n, rel)] for rel in rels}} for n, r in refs},
        "mappe": mappe,
        "senza_corrispondente": soli,
    }
    testo = json.dumps(risultato, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    (out / "confronto.json").write_text(testo, encoding="utf-8")
    impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()[:16]
    print(f"confronta_mappe: {len(mappe)} mappe · {len(soli)} senza corrispondente · "
          f"{out / 'confronto.json'} (sha256 {impronta})")
    for s in soli:
        print(f"  ! {s}")
    return 1 if a.strict and soli else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Exit: 0 confronto · 1 mappa senza corrispondente con --strict · "
                                        "2 errore d'uso")
    ap.add_argument("posizionali", nargs="*",
                    help="VECCHIA.md[:N] NUOVA.md[:N], oppure con --versioni i master da confrontare")
    ap.add_argument("--json", metavar="OUT", help="coppia: scrive il confronto in JSON")
    ap.add_argument("--svg", metavar="OUT", help="coppia: scrive l'SVG affiancato")
    ap.add_argument("--versioni", nargs="+", metavar="NOME=REF", help="versioni git, es. A=d726e6a2 C=HEAD")
    ap.add_argument("--base", help="con --versioni: la versione contro cui si confronta ogni altra")
    ap.add_argument("--estrai", metavar="DIR", help="con --versioni: dove mettere i file estratti")
    ap.add_argument("--out", metavar="DIR", help="con --versioni: cartella di confronto.json e svg/")
    ap.add_argument("--strict", action="store_true", help="esce 1 se una mappa resta senza corrispondente")
    a = ap.parse_args(argv)
    try:
        C._dipendenze()
    except ImportError:
        print("✗ confronta_mappe ha bisogno di tcod, scipy e numpy (ADR-0084): "
              "pip install -r requirements-dev.txt", file=sys.stderr)
        return 2
    if a.versioni:
        if not (a.base and a.out and a.posizionali):
            print("✗ --versioni vuole --base, --out e almeno un master", file=sys.stderr)
            return 2
        a.files = a.posizionali
        return versioni(a)
    if len(a.posizionali) != 2:
        ap.print_usage(sys.stderr)
        print("✗ servono due mappe, VECCHIA.md[:N] NUOVA.md[:N]", file=sys.stderr)
        return 2
    a.vecchia, a.nuova = a.posizionali
    return coppia(a)


if __name__ == "__main__":
    sys.exit(main())
