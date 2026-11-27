#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/prestigio.toml`: i requisiti delle classi di prestigio.

Uso: python3 estrai_prestigio.py srd <cartella srd-v3.5-md> <pcgen/data/35e> > sistemi/dnd35/dati/prestigio.toml
     python3 estrai_prestigio.py prd <cartella PSRD-Data> > sistemi/pf1e/dati/prestigio.toml

Due fonti, nell'ordine: le sezioni «Requirements» dell'SRD 3.5 (Prestige
Classes) e i tag `PRE…` delle righe `CLASS:` di PCGen per le classi dei manuali.
Un nome dell'SRD vince sempre. Solo nomi e numeri: bonus di attacco base,
talenti, gradi di abilità, razza, allineamento, livello d'incantesimo da saper
lanciare. Un requisito che non si riduce a questo (speciale, divinità, lingua,
regione) non si copia: se ne tiene il numero in `non_verificati`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLINEAMENTI = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]
PAROLE = {"lawful": "L", "chaotic": "C", "good": "G", "evil": "E", "neutral": "N"}


def allineamenti(testo: str) -> "list[str] | None":
    """«Any evil» → LE NE CE; «Lawful good or lawful neutral» → LG LN; None se non si riduce."""
    testo = testo.strip(" .").lower()
    fuori: list[str] = []
    for pezzo in re.split(r",\s*|\s+or\s+", testo):
        pezzo = pezzo.strip()
        m = re.fullmatch(r"any (non)?-?(lawful|chaotic|good|evil|neutral)", pezzo)
        if m:
            lettera = PAROLE[m.group(2)]
            for a in ALLINEAMENTI:
                ha = lettera in a if lettera != "N" else "N" in a
                if ha != bool(m.group(1)):
                    fuori.append(a)
            continue
        if pezzo in ("neutral", "true neutral"):
            fuori.append("N")
            continue
        m = re.fullmatch(r"(lawful|chaotic|neutral) (good|evil|neutral)", pezzo)
        if not m:
            return None
        fuori.append(PAROLE[m.group(1)] + PAROLE[m.group(2)])
    return sorted(set(fuori), key=ALLINEAMENTI.index) or None


def _da_voci(voci: "list[tuple[str, str]]", fonte: str) -> dict:
    """Le voci «Base Attack Bonus: +6», «Skills: Hide 8 ranks, …» di una sezione dei requisiti."""
    c: dict = {"fonte": fonte, "non_verificati": 0}
    for k, v in voci:
        k, v = k.strip().lower(), v.strip()
        if k == "base attack bonus" and re.match(r"\+\d+", v):
            c["bab"] = int(re.match(r"\+(\d+)", v).group(1))
        elif k == "alignment" and allineamenti(v):
            c["allineamento"] = allineamenti(v)
        elif k in ("skills", "skill"):
            gradi = {a.strip().lower(): int(n) for a, n in re.findall(r"([A-Z][^,.]*?) (\d+) ranks?", v)}
            if gradi:
                c.setdefault("abilita", []).append({"quanti": len(gradi), "fra": gradi})
            else:
                c["non_verificati"] += 1
        elif k in ("feats", "feat"):
            for t in re.split(r",\s*(?![^()]*\))", v.strip(" .")):
                scelte = [x.strip().lower() for x in re.split(r"\s+or\s+(?![^()]*\))", t)]
                if any(re.search(r"\b(?:two|three|any|one|either|plus)\b|\[", x) for x in scelte):
                    c["non_verificati"] += 1          # «Spell Focus in two schools»: non è un nome
                else:
                    c.setdefault("talenti", []).append({"quanti": 1, "fra": scelte})
        elif k == "race" and all(re.fullmatch(r"[a-z-]+", x.strip().lower())
                                 for x in re.split(r",\s*|\s+or\s+", v.strip(" ."))):
            c["razza"] = [x.strip().lower() for x in re.split(r",\s*|\s+or\s+", v.strip(" ."))]
        elif k in ("spells", "spellcasting") and re.search(r"cast (?:\d\w\w-level (?:arcane|divine) spells(?: and )?)+", v):
            trovati = re.findall(r"(\d)\w\w-level (arcane|divine) spells", v)
            c["incantesimi"] = [{"tipo": tipo, "livello": int(liv)} for liv, tipo in trovati]
            resto = re.sub(r"(\d)\w\w-level (arcane|divine) spells|\b(?:able|ability|to|cast|and)\b", "", v, flags=re.I)
            if re.search(r"[A-Za-z]{3}", resto):
                c["non_verificati"] += 1          # il resto del requisito («knowledge of…») non è un numero
        else:
            c["non_verificati"] += 1
    return c


def _avanza_da_tabella(html: str) -> "dict | None":
    """I livelli della classe che danno «+1 level of existing … class», dalla
    colonna «Spells per Day» della tabella. tipo: arcane, divine, both (una
    lista arcana e una divina insieme), any."""
    livelli, tipi = [], set()
    for riga in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        celle = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", riga, re.S)]
        m = re.match(r"\s*(\d+)(?:st|nd|rd|th)", celle[0]) if celle else None
        qui = [c for c in celle[1:] if re.search(r"level of existing", c, re.I)]
        if not m or not qui:
            continue
        livelli.append(int(m.group(1)))
        for c in qui:
            tipi |= set(re.findall(r"existing (arcane|divine)", c, re.I)) or {"any"}
    if not livelli:
        return None
    tipi = {x.lower() for x in tipi}
    tipo = "both" if {"arcane", "divine"} <= tipi else "any" if "any" in tipi or len(tipi) != 1 else tipi.pop()
    return {"tipo": tipo, "livelli": livelli}


def dall_srd(radice: Path) -> dict:
    testo = (radice / "basic-rules-and-legal" / "prestige-classes.md").read_text(encoding="utf-8")
    classi = {}
    for m in re.finditer(r"^## (?P<nome>[^\n]+)\n(?P<corpo>.*?)(?=^## |\Z)", testo, re.S | re.M):
        req = re.search(r"^### Requirements\n(.*?)(?=^### )", m.group("corpo"), re.S | re.M)
        if req:
            voci = re.findall(r"^\*\*([^:*]+):\*\*\s*(.+)$", req.group(1), re.M)
            classi[m.group("nome").strip().lower()] = _da_voci(voci, "SRD 3.5, Prestige Classes")
            tab = re.search(r"<table.*?</table>", m.group("corpo"), re.S)
            if tab and (a := _avanza_da_tabella(tab.group(0))):
                classi[m.group("nome").strip().lower()]["avanza"] = a
    return classi


def dal_prd(radice: Path) -> dict:
    """PF1e: le sezioni «Requirements» delle classi di prestigio del Core (PSRD-Data, book-cr)."""
    import sqlite3
    db = sqlite3.connect(radice / "book-cr.db")
    classi = {}
    for sid, nome in db.execute("select section_id, name from sections where type='class' and subtype='prestige'").fetchall():
        r = db.execute("select section_id from sections where parent_id=? and name='Requirements'", (sid,)).fetchone()
        if r:
            voci = [(k, re.sub(r"<[^>]+>", "", v or "")) for k, v in
                    db.execute("select name, body from sections where parent_id=? order by section_id", r)]
            classi[nome.strip().lower()] = _da_voci(voci, "PRD PF1e, Core Rulebook, Prestige Classes")
            tab = db.execute("select body from sections where type='table' and name=?", (f"Table: {nome.strip()}",)).fetchone()
            if tab and (a := _avanza_da_tabella(tab[0])):
                classi[nome.strip().lower()]["avanza"] = a
    return classi


def _virgole(v: str) -> "list[str]":
    return re.split(r",(?![^()]*\))", v)


def da_pcgen(radice: Path) -> dict:
    """Una classe scritta in più libri con requisiti diversi tiene i primi e
    prende `diverge = true`: il verificatore non ne fa una violazione."""
    per_libro: dict[str, list[dict]] = {}
    for f in sorted(radice.rglob("*class*.lst")):
        libro = f.parent.name.replace("_", " ").title()
        prestigio: set[str] = set()
        righe = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for r in righe:
            if r.startswith("CLASS:") and re.search(r"\tTYPE:[^\t]*Prestige", r):
                prestigio.add(r.split("\t")[0][6:].strip())
        qui: dict[str, dict] = {}
        corrente, avanza = None, {}
        for r in righe:
            if r.startswith("CLASS:"):
                corrente = r.split("\t")[0][6:].strip()
            elif corrente in prestigio and (m := re.match(r"(\d+)(?::REPEATLEVEL:(\d+))?\t", r)):
                tipi = re.findall(r"ADD:SPELLCASTER\|([^\t|]*)", r)
                if tipi:
                    da, passo = int(m.group(1)), int(m.group(2) or 0)
                    liv = list(range(da, max(10, da) + 1, passo)) if passo else [da]
                    a = avanza.setdefault(corrente.lower(), {"livelli": set(), "tipi": set()})
                    a["livelli"] |= set(liv)
                    a["tipi"].add("both" if {"Arcane", "Divine"} <= set(tipi) else tipi[0].strip().lower())
        for r in righe:
            if not r.startswith("CLASS:"):
                continue
            campi = r.split("\t")
            nome = campi[0][6:].strip()
            if nome not in prestigio or nome.endswith(".MOD"):
                continue
            c = qui.setdefault(nome.lower(), {"fonte": f"3.5 manuali (PCGen), {libro}", "non_verificati": 0})
            for t in campi[1:]:
                t = t.strip()
                if not re.match(r"!?PRE[A-Z]+:", t):
                    continue
                tag, _, v = t.partition(":")
                if tag == "PRETOTALAB" and v.isdigit():
                    c["bab"] = int(v)
                elif tag == "PREALIGN" and all(x in ALLINEAMENTI or x == "TN" for x in v.split(",")):
                    c["allineamento"] = sorted({"N" if x == "TN" else x for x in v.split(",")}, key=ALLINEAMENTI.index)
                elif tag == "PRESKILL":
                    n, *voci = _virgole(v)
                    gradi = {}
                    for x in voci:
                        a, _, g = x.partition("=")
                        if not g.isdigit() or a.startswith("TYPE"):
                            gradi = {}
                            break
                        gradi[a.strip().lower()] = int(g)
                    if gradi and n.isdigit() and int(n) <= len(gradi):
                        c.setdefault("abilita", []).append({"quanti": int(n), "fra": gradi})
                    else:
                        c["non_verificati"] += 1
                elif tag in ("PREABILITY", "PREFEAT"):
                    n, *voci = _virgole(v)
                    if voci and voci[0].startswith("CATEGORY="):
                        if voci[0] != "CATEGORY=FEAT":
                            c["non_verificati"] += 1
                            continue
                        voci = voci[1:]
                    if not n.isdigit() or not voci or int(n) > len(voci) \
                            or any(x.startswith(("TYPE", "[", "CHECKMULT")) or "=" in x for x in voci):
                        c["non_verificati"] += 1
                        continue
                    c.setdefault("talenti", []).append(
                        {"quanti": int(n), "fra": [re.sub(r"type\.", "", x.strip().lower()) for x in voci]})
                elif tag == "PRERACE":
                    n, *voci = _virgole(v)
                    # il sottotipo («RACESUBTYPE=Dwarf») è la razza scritta fra parentesi nel tipo
                    nomi = [re.sub(r"^racesubtype=", "", x.strip().lower()).rstrip("%") for x in voci]
                    if n == "1" and nomi and all(re.fullmatch(r"[a-z' -]+(?: \([a-z' -]+\))?", x) for x in nomi):
                        c["razza"] = list(dict.fromkeys(c.get("razza", []) + nomi))
                    else:
                        c["non_verificati"] += 1          # tipi, sottotipi, razze escluse: non sono un nome di razza
                elif tag == "PRESPELLTYPE" and re.fullmatch(r"1,(Arcane|Divine)=(\d)", v):
                    s = re.fullmatch(r"1,(Arcane|Divine)=(\d)", v)
                    c.setdefault("incantesimi", []).append({"tipo": s.group(1).lower(), "livello": int(s.group(2))})
                else:
                    c["non_verificati"] += 1
        for nome, c in qui.items():
            a = avanza.get(nome)
            if a and "psionic" not in a["tipi"]:
                # tipi diversi da un livello all'altro: non si sa quale lista avanza
                c["avanza"] = {"tipo": next(iter(a["tipi"])) if len(a["tipi"]) == 1 else "any",
                               "livelli": sorted(a["livelli"])}
            per_libro.setdefault(nome, []).append(c)
    classi = {}
    for nome, versioni in per_libro.items():
        c = dict(versioni[0])
        senza = [{k: v for k, v in x.items() if k not in ("fonte", "avanza")} for x in versioni]
        if any(x != senza[0] for x in senza[1:]):
            c["diverge"] = True
        if any(x.get("avanza") != versioni[0].get("avanza") for x in versioni[1:]):
            c["avanza"] = {"diverge": True}      # due libri danno avanzamenti diversi: il verificatore non giudica
        classi[nome] = c
    return classi


def _valore(v) -> str:
    if isinstance(v, dict):
        return "{ " + ", ".join(f'{_chiave(k)} = {_valore(x)}' for k, x in v.items()) + " }"
    if isinstance(v, list):
        return "[" + ", ".join(_valore(x) for x in v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def _chiave(k: str) -> str:
    return k if re.fullmatch(r"[A-Za-z_]+", k) else _valore(k)


def _stampa(testa: "list[str]", classi: dict) -> None:
    print("# Scritto da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_prestigio.py:")
    print("# non si modifica a mano. Requisiti delle classi di prestigio, solo nomi e numeri.")
    for riga in testa:
        print(f"# {riga}")
    print("# `non_verificati` conta i requisiti che non si riducono a un numero (speciali, divinità, lingue).")
    print("# `avanza` = i livelli della classe che danno +1 livello d'incantatore a una classe che si aveva già")
    print("# (tipo: arcane, divine, both, any, o il nome della classe); senza `avanza` la classe non ne dà.")
    print()
    print("# descrizioni delle classi: chi lancia incantesimi arcani e chi divini")
    print('[tipi_di_magia]')
    print('arcane = ["bard", "sorcerer", "wizard"]')
    print('divine = ["cleric", "druid", "paladin", "ranger"]')
    print()
    print("[prestigio]")
    for nome, c in sorted(classi.items()):
        print(f"{_valore(nome)} = {_valore(c)}")


def main() -> int:
    if sys.argv[1] == "prd":
        classi = dal_prd(Path(sys.argv[2]))
        _stampa([f"{len(classi)} classi dal PRD PF1e (Core Rulebook)."], classi)
        return 0
    srd = dall_srd(Path(sys.argv[2]))
    manuali = {k: v for k, v in da_pcgen(Path(sys.argv[3])).items() if k not in srd}
    _stampa([f"{len(srd)} classi dall'SRD 3.5, {len(manuali)} dai manuali (tag PRE di PCGen); l'SRD vince.",
             f"{sum(1 for c in manuali.values() if c.get('diverge'))} classi dei manuali stanno in più libri con "
             "requisiti diversi (`diverge`):", "tengono i primi e il verificatore non ne fa una violazione."],
            {**manuali, **srd})
    return 0


if __name__ == "__main__":
    sys.exit(main())
