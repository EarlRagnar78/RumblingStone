"""Abbina gli incantesimi di Editori Folli (SRD 3.5 in italiano) ai titoli dell'SRD inglese.

Chiave: scuola + insieme dei livelli (classi e domini tradotti) + componenti.
Non usa i nomi: l'abbinamento si misura poi contro la tabella esistente.
"""
import json, re, sys, unicodedata
from pathlib import Path
from collections import defaultdict

EF = Path.home() / ".cache/rumblingstone/editorifolli"
SRD = next((Path.home() / ".cache/rumblingstone/srd").glob("srd-v3.5-md-*")) / "spells"
TSV = Path(__file__).resolve().parents[4] / "scripts" / "lessico_it_35.tsv"

SCUOLE = {"abiurazione": "abjuration", "ammaliamento": "enchantment", "divinazione": "divination",
          "evocazione": "conjuration", "illusione": "illusion", "invocazione": "evocation",
          "necromanzia": "necromancy", "trasmutazione": "transmutation", "universale": "universal"}
CLASSI = {"brd": "brd", "chr": "clr", "drd": "drd", "mag/str": "sor/wiz", "str/mag": "sor/wiz",
          "pal": "pal", "rgr": "rgr"}
DOM = {}
for r in TSV.read_text(encoding="utf-8").splitlines():
    c = r.split("\t")
    if len(c) >= 3 and c[2] == "dominio":
        DOM[c[0].lower()] = c[1].replace(" Domain", "").lower()


def norma(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower().strip()


def livelli(testo, it):
    out = set()
    for pezzo in re.split(r",\s*", testo.strip().rstrip(".")):
        m = re.match(r"(.+?)\s+(\d)\b", pezzo.strip())
        if not m:
            continue
        k, n = m.group(1).strip().lower(), m.group(2)
        if it:
            k = CLASSI.get(k) or DOM.get(k) or ("?" + k)
        out.add(f"{k} {n}")
    return frozenset(out)


def componenti(testo, it):
    t = testo.upper().replace(" ", "")
    if it:
        t = t.replace("FD", "DF").replace("PE", "XP")
    return frozenset(re.split(r"[,]", t))


def tratti(campi, it):
    """Raggio, TS, RI e tempo di lancio ridotti a categorie confrontabili fra le lingue."""
    g = lambda *k: next((campi[x] for x in k if x in campi), "").lower()
    r = g("raggio di azione", "range")
    raggio = next((v for k, v in [("personale", "pers"), ("personal", "pers"), ("contatto", "touch"),
                   ("touch", "touch"), ("vicino", "close"), ("close", "close"), ("medio", "med"),
                   ("medium", "med"), ("lungo", "long"), ("long", "long"), ("illimitat", "unl"),
                   ("unlimited", "unl"), ("vedi testo", "see"), ("see text", "see")] if k in r), r[:6])
    ts = g("tiro salvezza", "saving throw")
    tipo = next((v for k, v in [("volont", "will"), ("will", "will"), ("riflessi", "ref"), ("reflex", "ref"),
                 ("tempra", "fort"), ("fortitude", "fort"), ("nessun", "none"), ("none", "none")] if k in ts), "?")
    ri = g("resistenza agli incantesimi", "spell resistance")
    ri = "si" if ri.startswith(("sì", "si", "yes")) else ("no" if ri.startswith("no") else "?")
    tl = g("tempo di lancio", "casting time")
    lancio = next((v for k, v in [("standard", "std"), ("round complet", "fr"), ("full round", "fr"),
                   ("1 round", "fr"), ("immediat", "imm"), ("veloce", "swift"), ("swift", "swift"),
                   ("minut", "min"), ("ora", "h"), ("hour", "h")] if k in tl), tl[:4])
    return (raggio, tipo, ri, lancio)


def campi_it(blocco):
    c = {}
    for b in blocco:
        if ":" in b:
            k, v = b.split(":", 1)
            c[k.strip().lower()] = v.strip()
    return c


def campi_en(blocco):
    c = {}
    for b in blocco:
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", b)
        if m:
            c[m.group(1).strip().lower()] = m.group(2).strip()
    return c


def leggi_it():
    voci = []
    for f in sorted(EF.glob("srd35_10_01_incantesimi_*.txt")):
        righe = [r.rstrip() for r in f.read_text(encoding="utf-8").splitlines()]
        for i, r in enumerate(righe):
            if i + 1 < len(righe) and r and r.upper() == r and re.search(r"[A-ZÀ-Ù]{3}", r) \
                    and not r.startswith("INCANTESIMI (") and "OPEN GAME" not in r:
                scuola = righe[i + 1].strip().split(" ")[0].lower()
                if scuola not in SCUOLE:
                    continue
                blocco = righe[i + 1:i + 14]
                liv = next((b.split(":", 1)[1] for b in blocco if b.startswith("Livello:")), "")
                comp = next((b.split(":", 1)[1] for b in blocco if b.startswith("Componenti:")), "")
                voci.append({"it": r.strip(), "scuola": SCUOLE[scuola], "liv": livelli(liv, True),
                             "comp": componenti(comp, True) if comp else None,
                             "tratti": tratti(campi_it(blocco), True)})
    return voci


def leggi_en():
    voci = []
    for f in sorted(SRD.glob("spells-*.md")):
        righe = f.read_text(encoding="utf-8").splitlines()
        for i, r in enumerate(righe):
            if r.startswith("## "):
                blocco = [b for b in righe[i + 1:i + 32] if b.strip()]
                stop = next((k for k, b in enumerate(blocco) if b.startswith('## ')), len(blocco))
                blocco = blocco[:stop]
                if not blocco:
                    continue
                scuola = blocco[0].split(" ")[0].lower()
                if scuola not in SCUOLE.values():
                    continue
                liv = next((b.split(":**", 1)[1] for b in blocco if b.startswith("**Level:**")), "")
                comp = next((b.split(":**", 1)[1] for b in blocco if b.startswith("**Components:**")), "")
                voci.append({"en": r[3:].strip(), "scuola": scuola, "liv": livelli(liv, False),
                             "comp": componenti(comp, False) if comp else None,
                             "tratti": tratti(campi_en(blocco), False)})
    return voci


def main():
    it, en = leggi_it(), leggi_en()
    print("it", len(it), "en", len(en), file=sys.stderr)
    per_chiave = defaultdict(list)
    for e in en:
        if e["liv"]:
            per_chiave[(e["scuola"], e["liv"])].append(e)
    coppie, ambigui, senza = [], [], []
    for v in it:
        cand = per_chiave.get((v["scuola"], v["liv"]), []) if v["liv"] else []
        if len(cand) > 1 and v["comp"]:
            stretti = [c for c in cand if c["comp"] == v["comp"]]
            cand = stretti or cand
        if len(cand) > 1:
            uguali = lambda a, b: all(x == y or "?" in (x, y) for x, y in zip(a, b))
            stretti = [c for c in cand if uguali(c["tratti"], v["tratti"])]
            cand = stretti or cand
        if len(cand) == 1:
            coppie.append((v["it"], cand[0]["en"]))
        elif cand:
            ambigui.append((v["it"], [c["en"] for c in cand]))
        else:
            senza.append(v["it"])
    json.dump({"coppie": coppie, "ambigui": ambigui, "senza": senza}, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
