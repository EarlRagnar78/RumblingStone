"""Abbina le trappole del GDM italiano (scheda «Trappole» di Mindbender) alle trappole dell'SRD 3.5.

Non usa i nomi: una trappola si abbina se GS, CD di Cercare, CD di Disattivare Congegni e prezzo
(o costo) sono uguali, e la chiave è unica nelle due liste.

Uso: python3 -I abbina_trappole.py <trappole.txt> > coppie.json
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

SRD = next((Path.home() / ".cache/rumblingstone/srd").glob("srd-v3.5-md-*")) / "basic-rules-and-legal/traps.md"


def num(s):
    return re.sub(r"[.,]", "", s)


def chiave(gs, cerca, disatt, prezzo):
    return (gs, cerca, disatt, num(prezzo))


def srd():
    out = defaultdict(list)
    for m in re.finditer(r"\*\*([^*]+?):\*\*\s*CR (\d+);(.*?)(?:Market Price|Cost):_?\s*([\d,]+) gp", SRD.read_text(encoding="utf-8")):
        c = re.search(r"Search DC (\d+)", m.group(3)); d = re.search(r"Disable Device DC (\d+)", m.group(3))
        if c and d:
            out[chiave(m.group(2), c.group(1), d.group(1), m.group(4))].append(m.group(1).strip())
    return out


def italiano(testo):
    # Le due colonne del PDF si separano sugli spazi lunghi; poi ogni colonna si legge di seguito.
    sx, dx = [], []
    for linea in testo.splitlines():
        parti = re.split(r"\s{6,}", linea.strip(), maxsplit=1)
        sx.append(parti[0]); dx.append(parti[1] if len(parti) > 1 else "")
    flusso = " ".join(sx + dx)
    out = defaultdict(list)
    for m in re.finditer(r"([A-ZÀ-Ú][^:;.]{2,60}?): GS (\d+);(.*?)(?:Prezzo di mercato|Costo):\s*([\d.]+) mo", flusso):
        c = re.search(r"Cercare CD (\d+)", m.group(3)); d = re.search(r"Disattivare\s+Congegni\s+CD (\d+)", m.group(3))
        if c and d:
            out[chiave(m.group(2), c.group(1), d.group(1), m.group(4))].append(m.group(1).strip())
    return out


def main():
    it, en = italiano(Path(sys.argv[1]).read_text(encoding="utf-8")), srd()
    coppie, dubbi = [], []
    for k, nomi in it.items():
        if len(nomi) == 1 and len(en.get(k, [])) == 1:
            coppie.append({"it": nomi[0], "en": en[k][0], "gs": k[0]})
        elif k in en:
            dubbi.append({"it": nomi, "en": en[k]})
    print("it", sum(map(len, it.values())), "en", sum(map(len, en.values())),
          "coppie", len(coppie), "dubbi", len(dubbi), file=sys.stderr)
    json.dump({"coppie": coppie, "dubbi": dubbi}, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
