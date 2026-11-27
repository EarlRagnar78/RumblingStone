#!/usr/bin/env python3
"""estrai_liste_manuali.py — le liste di incantesimi dei manuali 3.5, da PCGen.

L'SRD dà le liste di sette classi (`estrai_liste.py`). I manuali ne aggiungono
altre (warmage, hexblade, assassino…) e allungano quelle dell'SRD. PCGen le
registra nei file `*spells*.lst` (`CLASSES:Bard=3|Sorcerer,Wizard=3`,
`DOMAINS:Storm=3`) e nei file delle classi (`SPELLLEVEL:CLASS|Nome=2|a,b`,
`SPELLLIST:3|Bard|Sorcerer|Wizard` per chi pesca dalle liste altrui).

Dal clone escono **solo nomi e livelli** (decisione del DM, 2026-11-12: fonti non
OGL nel repo solo come nomi e numeri). Dove PCGen e l'SRD danno lo stesso
incantesimo alla stessa classe, la voce non si ripete; dove danno un livello
diverso vince l'SRD e la voce si conta nei divergenti.

Uso:
  python3 -I estrai_liste_manuali.py CLONE_PCGEN            # scrive il toml
  python3 -I estrai_liste_manuali.py CLONE_PCGEN --check    # esce 1 se non aggiornato
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRD = ROOT / "sistemi" / "dnd35" / "dati" / "liste_incantesimi.toml"
ESCE = ROOT / "sistemi" / "dnd35" / "dati" / "liste_incantesimi_manuali.toml"
RADICE = "data/35e/wizards_of_the_coast"
VOCE = re.compile(r"([^=|\[]+)=(\d)(?:\[[^\]]*\])?")


def _senza_pre(testo: str) -> str:
    """Toglie le voci con una condizione fra quadre («Cleric=6[PREDEITY:1,Mystra]»):
    l'incantesimo non è della classe, è di chi soddisfa la condizione."""
    return "|".join(g for g in testo.split("|") if "[" not in g)


def _voci(valore: str):
    for gruppo in _senza_pre(valore).split("|"):
        m = re.fullmatch(r"\s*([^=]+)=(\d)\s*", gruppo)
        if not m:
            continue
        for nome in m.group(1).split(","):
            nome = nome.strip()
            if nome and nome.upper() not in ("ALL", ".CLEARALL"):
                yield nome.lower(), m.group(2)


def leggi(clone: Path) -> "tuple[dict, dict, dict]":
    liste: dict = {}
    domini: dict = {}
    prese: dict = {}
    base = clone / RADICE
    for f in sorted(base.rglob("*.lst")):
        nome_f = f.name.lower()
        di_incantesimi = "spells" in nome_f
        di_classi = "class" in nome_f
        if not (di_incantesimi or di_classi):
            continue
        classe = None
        for riga in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not riga.strip() or riga.startswith("#"):
                continue
            campi = [c for c in riga.split("\t") if c.strip()]
            testa = campi[0].strip()
            if di_incantesimi and ":" not in testa.split(".MOD")[0][:6]:
                nome = re.sub(r"\.(MOD|COPY=.*)$", "", testa).strip()
                for c in campi[1:]:
                    if c.startswith("CLASSES:"):
                        for cl, liv in _voci(c[8:]):
                            liste.setdefault(cl, {}).setdefault(liv, set()).add(nome)
                    elif c.startswith("DOMAINS:"):
                        for d, liv in _voci(c[8:]):
                            domini.setdefault(d, {}).setdefault(liv, set()).add(nome)
            if di_classi:
                if testa.startswith("CLASS:"):
                    classe = re.sub(r"\.MOD$", "", testa[6:]).strip().lower()
                for c in campi:
                    m = re.match(r"SPELLLIST:\d+\|(.+)", c)
                    if m and classe:
                        prese[classe] = sorted({x.strip().lower() for x in m.group(1).split("|")
                                                if x.strip() and not x.startswith("TYPE")})
                    m = re.match(r"SPELLLEVEL:(CLASS|DOMAIN)\|(.+)", c)
                    if m:
                        pezzi = _senza_pre(m.group(2)).split("|")
                        dove = liste if m.group(1) == "CLASS" else domini
                        for chi, cosa in zip(pezzi[0::2], pezzi[1::2]):
                            k = re.fullmatch(r"\s*([^=]+)=(\d)\s*", chi)
                            if not k:
                                continue
                            for cl in k.group(1).split(","):
                                for nome in cosa.split(","):
                                    if nome.strip() and cl.strip():
                                        dove.setdefault(cl.strip().lower(), {}).setdefault(k.group(2), set()).add(nome.strip())
    return liste, domini, prese


def togli_srd(gruppo: dict, srd: dict) -> "tuple[dict, int]":
    """Lascia solo ciò che l'SRD non ha; conta le voci a livello diverso (vince l'SRD)."""
    out: dict = {}
    divergenti = 0
    for classe, livelli in gruppo.items():
        noti = {n.lower().replace("’", "'"): liv for liv, voci in srd.get(classe, {}).items() for n in voci}
        for liv, voci in livelli.items():
            for n in voci:
                suo = noti.get(n.lower().replace("’", "'"))
                if suo is None:
                    out.setdefault(classe, {}).setdefault(liv, set()).add(n)
                elif suo != liv:
                    divergenti += 1
    return out, divergenti


def scrivi(liste: dict, domini: dict, prese: dict, divergenti: int) -> str:
    n = len({x for c in liste.values() for v in c.values() for x in v})
    righe = ["# sistemi/dnd35/dati/liste_incantesimi_manuali.toml — liste di incantesimi dei manuali 3.5 (ADR-0124 §11)",
             "# Generato da plans/esperimenti/incantesimi-35-2026-11-12/estrai_liste_manuali.py dai file",
             "# *spells*.lst e *class*.lst di PCGen (BahamutDragon/pcgen, data/35e/wizards_of_the_coast).",
             "# Solo nomi e livelli. Non si scrive a mano. Ciò che l'SRD ha già non è ripetuto.",
             f"# {n} incantesimi, {len(liste)} classi, {len(domini)} domini, {len(prese)} classi che pescano da liste altrui.",
             f"# {divergenti} voci a livello diverso dall'SRD lasciate fuori: vince l'SRD."]
    for titolo, gruppo in (("liste_manuali", liste), ("domini_manuali", domini)):
        for classe in sorted(gruppo):
            righe += ["", f"[{titolo}.{json.dumps(classe, ensure_ascii=False)}]"]
            for liv in sorted(gruppo[classe]):
                voci = ", ".join(json.dumps(v, ensure_ascii=False) for v in sorted(gruppo[classe][liv]))
                righe.append(f'"{liv}" = [{voci}]')
    righe += ["", "[liste_prese]"]
    for classe in sorted(prese):
        righe.append(f"{json.dumps(classe, ensure_ascii=False)} = {json.dumps(prese[classe], ensure_ascii=False)}")
    return "\n".join(righe) + "\n"


def main(argv: "list[str]") -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    liste, domini, prese = leggi(Path(argv[0]))
    srd = tomllib.loads(SRD.read_text(encoding="utf-8"))
    liste, d1 = togli_srd(liste, srd.get("liste", {}))
    domini, d2 = togli_srd(domini, srd.get("domini", {}))
    testo = scrivi(liste, domini, prese, d1 + d2)
    if "--check" in argv:
        ok = ESCE.exists() and ESCE.read_text(encoding="utf-8") == testo
        print("✓ aggiornato" if ok else "✗ da rigenerare")
        return 0 if ok else 1
    ESCE.write_text(testo, encoding="utf-8")
    print(testo.splitlines()[4], testo.splitlines()[5], sep="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
