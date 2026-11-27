"""Abbina l'equipaggiamento di Editori Folli all'SRD inglese per firma, sezione per sezione.

Le tabelle hanno le stesse sezioni nello stesso ordine, ma dentro la sezione le
righe sono in ordine alfabetico di ciascuna lingua: si abbina per firma (costo,
danni, critico, gittata, peso, tipo; per le armature CA, Des massima, penalità,
fallimento), e vale solo una firma unica nella sezione da tutte e due le parti.
"""
import re, html, json, sys
from collections import defaultdict
from pathlib import Path
C = next((Path.home() / ".cache/rumblingstone/srd").glob("srd-v3.5-md-*")) / "basic-rules-and-legal/equipment.md"
E = Path.home() / ".cache/rumblingstone/editorifolli"
UNITA = {"gp": 1, "mo": 1, "sp": .1, "ma": .1, "cp": .01, "mr": .01, "pp": 10, "mp": 10}


def costo(s):
    s = s.replace(".", "").replace(",", ".").strip()
    m = re.match(r"([\d.]+)\s*(gp|sp|cp|pp|mo|ma|mr|mp)\b", s)
    return round(float(m.group(1)) * UNITA[m.group(2)], 2) if m else None


def peso(s):
    s = s.replace(",", ".")
    m = re.match(r"([\d.]+)\s*(lb|kg)", s)
    if not m:
        return "—"
    v = float(m.group(1)); return round(v / 2 if m.group(2) == "lb" else v, 2)


def gittata(s):
    m = re.match(r"([\d.,]+)\s*(ft|m)", s.replace(",", "."))
    if not m:
        return "—"
    v = float(m.group(1)); return round(v * 0.3 if m.group(2) == "ft" else v, 1)


TIPO = {"bludgeoning": "B", "piercing": "P", "slashing": "S", "contundente": "B", "perforante": "P", "tagliente": "S"}


def tipo(s):
    return "".join(sorted({TIPO[w] for w in re.findall(r"[a-z]+", s.lower()) if w in TIPO})) or "—"


def pulisci(s):
    return re.sub(r"\d$", "", re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip())


def firma_arma(c, r, g, p, t):
    return ("A", c, re.sub(r"\d(?=$)", "", r[0]), re.sub(r"\d(?=$)", "", r[1]), r[2].replace("×", "x"), gittata(g), peso(p), tipo(t))


def en_tabella(caption, tipo_tab):
    t = C.read_text(encoding="utf-8")
    i = t.index(f"<caption>Table: {caption}</caption>")
    tab = t[i:t.index("</table>", i)]
    sez, out = -1, []
    for tr in re.findall(r"<tr>(.*?)</tr>", tab, re.S):
        celle = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if len(celle) == 1 or (len(celle) >= 2 and not any(celle[1:])) or (celle and celle[0] in ("Item",)):
            if celle and celle[0] not in ("Item",):
                sez += 1
            continue
        if len(celle) < 2:
            continue
        c = costo(celle[1])
        if c is None:
            continue
        if tipo_tab == "armi" and len(celle) >= 8:
            f = firma_arma(c, celle[2:5], celle[5], celle[6], celle[7])
        elif tipo_tab == "armature" and len(celle) >= 6:
            f = ("R", c, celle[2].replace("+", ""), celle[3].replace("+", ""), celle[4].replace("–", "-"), celle[5])
        else:
            f = ("G", c, peso(celle[2]) if len(celle) > 2 else "—")
        out.append((max(sez, 0), pulisci(celle[0]), f))
    return out


def it_tabella(nome, tipo_tab):
    sez, out = -1, []
    righe = (E / nome).read_text(encoding="utf-8").splitlines()
    for k, r in enumerate(righe):
        if not r.strip():
            continue
        dopo = righe[k + 1].strip() if k + 1 < len(righe) else ""
        cont = re.split(r"\s{2,}", dopo)[0] if dopo else ""
        if cont and (cont[0].islower() or cont[0] == "(") and len(cont) < 25 and costo(dopo) is None:
            r = re.sub(r"^(\s*\S.*?)(\s{2,})", lambda m: m.group(1) + " " + cont + m.group(2), r, count=1)
        col = re.split(r"\s{2,}", r.strip())
        c = costo(col[1]) if len(col) > 1 else None
        if c is None:
            if len(col) == 1 and len(r.strip()) < 50 and re.match(r"^[A-ZÀ-Ù]", r.strip()) and not r.strip().endswith("."):
                sez += 1
            continue
        if tipo_tab == "armi" and len(col) >= 8:
            f = firma_arma(c, col[2:5], col[5], col[6], col[7])
        elif tipo_tab == "armature" and len(col) >= 6:
            f = ("R", c, col[2].replace("+", ""), col[3].replace("+", ""), col[4].replace("–", "-"), col[5])
        else:
            f = ("G", c, peso(col[2]) if len(col) > 2 else "—")
        out.append((max(sez, 0), pulisci(col[0]), f))
    return out


def abbina(en, it):
    ke, ki = defaultdict(list), defaultdict(list)
    for s, n, f in en:
        ke[f].append(n)
    for s, n, f in it:
        ki[f].append(n)
    coppie, dubbi = [], []
    for f, nomi in ki.items():
        if f in ke:
            if len(nomi) == 1 and len(ke[f]) == 1:
                coppie.append((nomi[0], ke[f][0]))
            else:
                dubbi.append((nomi, ke[f]))
    return coppie, dubbi


if __name__ == "__main__":
    out = {}
    for cap, f, tt in [("Weapons", "srd35_06_01_equipaggiamento_armi.txt", "armi"),
                       ("Armor and Shields", "srd35_06_01_equipaggiamento_armature.txt", "armature"),
                       ("Goods and Services", "srd35_06_01_equipaggiamento_merciservizi.txt", "merci")]:
        en, it = en_tabella(cap, tt), it_tabella(f, tt)
        coppie, dubbi = abbina(en, it)
        out[cap] = {"coppie": coppie, "dubbi": dubbi}
        print(cap, "en", len(en), "it", len(it), "coppie", len(coppie), "dubbi", len(dubbi), file=sys.stderr)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
