#!/usr/bin/env python3
"""estrai_creature_base.py — le creature base dell'SRD 3.5 per il plugin (ADR-0126, lotto 5).

Legge i blocchi di statistiche di `monsters/*.md` dell'SRD in cache (tabelle
HTML, una colonna per creatura), o la tabella `creature_details` dei Bestiary di
PSRD-Data, e scrive `sistemi/<sistema>/dati/creature_base.toml`: taglia, tipo,
sottotipi, dadi vita razziali, armatura naturale, caratteristiche, attacchi
naturali col dado, modificatore di livello (solo 3.5) e grado di sfida.

Uso:  python3 -I estrai_creature_base.py srd <cartella monsters dell'SRD> > sistemi/dnd35/dati/creature_base.toml
      python3 -I estrai_creature_base.py prd <cartella di PSRD-Data>      > sistemi/pf1e/dati/creature_base.toml

Solo numeri e nomi: nessun testo descrittivo. Le colonne «N°-Level Classe» sono
personaggi d'esempio con livelli di classe, non creature base, e si saltano.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

TAGLIE = ("Fine", "Diminutive", "Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal")
TIPI = ("aberration", "animal", "construct", "dragon", "elemental", "fey", "giant", "humanoid",
        "magical beast", "monstrous humanoid", "ooze", "outsider", "plant", "undead", "vermin")
#: i nomi degli attacchi naturali dell'SRD (singolare); il resto sono armi
NATURALI = ("bite", "claw", "slam", "gore", "tail slap", "tail", "sting", "wing", "tentacle", "hoof", "talon",
            "slap", "pincer", "butt", "ram", "rake", "tongue", "arm", "tendril", "stamp", "snake bite",
            "tail sweep", "crush", "kick", "horn", "antler", "beak", "foreclaw", "vine")
_PLURALI = {"claws": "claw", "slams": "slam", "tentacles": "tentacle", "hooves": "hoof", "talons": "talon",
            "wings": "wing", "pincers": "pincer", "bites": "bite", "stings": "sting", "arms": "arm",
            "tendrils": "tendril", "tails": "tail", "tail slaps": "tail slap", "gores": "gore", "slaps": "slap",
            "snake bites": "snake bite", "kicks": "kick", "horns": "horn", "antlers": "antler",
            "foreclaws": "foreclaw", "vines": "vine", "snakes": "snake"}
CAR = (("Str", "for"), ("Dex", "des"), ("Con", "cos"), ("Int", "int"), ("Wis", "sag"), ("Cha", "car"))


def _celle(riga: str) -> "list[str]":
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip().replace("–", "-").replace("—", "-")
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, flags=re.S)]


def _attacchi(testo: str) -> "dict[str, dict]":
    out: dict[str, dict] = {}
    for n, nome, dado in re.findall(r"(?:(\d+) )?([A-Za-z][A-Za-z ]*?) [+-]\d+(?:/[+-]\d+)* (?:melee|ranged)(?: touch)? "
                                    r"\((\d+d\d+)", testo):
        k = re.sub(r"^(?:and|or|plus) ", "", nome.strip().lower())
        k = _PLURALI.get(k, k)
        if k in NATURALI and k not in out:
            out[k] = {"dado": dado, "n": int(n) if n else 1}
    return out


def creature(cartella: Path) -> "dict[str, dict]":
    out: dict[str, dict] = {}
    for f in sorted(cartella.glob("*.md")):
        testo = f.read_text(encoding="utf-8")
        for m_tab in re.finditer(r"<table.*?</table>", testo, flags=re.S):
            tab = m_tab.group(0)
            if "Hit Dice" not in tab:
                continue
            righe = [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", tab, flags=re.S)]
            righe = [r for r in righe if r]
            if len(righe) < 3 or righe[0][0] != "":
                continue
            if any(re.match(t + r"\b", c) for c in righe[0][1:] for t in TAGLIE):
                # una creatura sola: la tabella parte dalla riga del tipo, il nome è il titolo sopra
                titoli = re.findall(r"^#{1,6} +(.+?) *$", testo[:m_tab.start()], flags=re.M)
                if not titoli or len(righe[0]) != 2:
                    continue
                righe.insert(0, ["", titoli[-1]])
            per = {r[0].rstrip(":").lower(): r[1:] for r in righe[2:] if r[0]}
            for i, nome in enumerate(righe[0][1:]):
                if not nome or re.search(r"\d+(?:st|nd|rd|th)-Level", nome):
                    continue

                def v(chiave: str) -> str:
                    c = per.get(chiave, [])
                    return c[i] if i < len(c) else ""
                tipo_riga = righe[1][i + 1] if i + 1 < len(righe[1]) else ""
                taglia = next((t for t in TAGLIE if re.match(t + r"\b", tipo_riga)), None)
                tipo = next((t for t in sorted(TIPI, key=len, reverse=True) if t in tipo_riga.lower()), None)
                dv = re.match(r"(\d+|1/2|1/4)d(\d+)", v("hit dice"))
                if not (taglia and tipo and dv):
                    continue
                voce: dict = {"taglia": taglia, "tipo": tipo}
                sotto = re.search(r"\(([^)]*)\)", tipo_riga)
                if sotto:
                    voce["sottotipi"] = [s.strip().lower() for s in sotto.group(1).split(",")]
                voce["dv"] = dv.group(1) if "/" in dv.group(1) else int(dv.group(1))
                voce["dado"] = int(dv.group(2))
                nat = re.search(r"\+(\d+) natural", v("armor class"))
                voce["naturale"] = int(nat.group(1)) if nat else 0
                car = {it: int(m.group(1)) for en, it in CAR
                       if (m := re.search(en + r" (\d+)", v("abilities")))}
                if car:
                    voce["car"] = car
                att = _attacchi(v("full attack") or v("attack"))
                if att:
                    voce["attacchi"] = att
                mdl = re.match(r"\+(\d+)", v("level adjustment"))
                if mdl:
                    voce["mdl"] = int(mdl.group(1))
                if "character class" in v("advancement").lower():
                    voce["avanza"] = "classe"
                gs = re.match(r"(\d+(?:/\d+)?)", v("challenge rating"))
                if gs:
                    voce["gs"] = gs.group(1) if "/" in gs.group(1) else int(gs.group(1))
                voce["fonte"] = f.name
                out.setdefault(nome.lower(), voce)
    return out


def draghi(cartella: Path) -> "dict[str, dict]":
    """La tabella «Dragon Space/Reach, Attacks, and Damage»: il dado per taglia dei draghi veri."""
    out: dict[str, dict] = {}
    for f in sorted(cartella.glob("*.md")):
        m = re.search(r"<table[^>]*>(?:(?!</table>).)*Dragon Space/Reach, Attacks, and Damage.*?</table>",
                      f.read_text(encoding="utf-8"), flags=re.S)
        if not m:
            continue
        righe = [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", m.group(0), flags=re.S)]
        colonne = [re.sub(r"^\d+ ?", "", c).lower() for c in righe[1][2:]]
        colonne = [_PLURALI.get(c, c) for c in colonne]
        for r in righe[2:]:
            if r and r[0] in TAGLIE:
                out[r[0]] = {c: {"dado": d, "n": 2 if c in ("claw", "wing") else 1}
                             for c, d in zip(colonne, r[2:]) if re.fullmatch(r"\d+d\d+", d)}
    return out


def creature_prd(cartella: Path) -> "dict[str, dict]":
    """Le creature dei Bestiary PF1e (PSRD-Data, tabella `creature_details` di book-b1…b4.db)."""
    import sqlite3
    out: dict[str, dict] = {}
    for f in sorted(cartella.glob("book-b[1-4].db")):
        con = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        for r in con.execute("select s.name as nome, d.* from creature_details d "
                             "join sections s on s.section_id = d.section_id"):
            taglia = next((t for t in TAGLIE if (r["size"] or "").strip() == t), None)
            tipo = (r["creature_type"] or "").strip().lower()
            dv = re.search(r"\((\d+)d(\d+)", r["hp"] or "")
            if not (taglia and tipo in TIPI and dv) or r["level"] or r["super_race"]:
                continue               # con livelli di classe non è una creatura base
            voce: dict = {"taglia": taglia, "tipo": tipo}
            if r["creature_subtype"]:
                voce["sottotipi"] = [s.strip().lower() for s in r["creature_subtype"].split(",")]
            voce["dv"], voce["dado"] = int(dv.group(1)), int(dv.group(2))
            nat = re.search(r"\+(\d+) natural", r["ac"] or "")
            voce["naturale"] = int(nat.group(1)) if nat else 0
            car = {it: int(r[col]) for col, it in (("strength", "for"), ("dexterity", "des"), ("constitution", "cos"),
                                                   ("intelligence", "int"), ("wisdom", "sag"), ("charisma", "car"))
                   if (r[col] or "").strip().isdigit()}
            if car:
                voce["car"] = car
            att = _attacchi(re.sub(r" ([+-]\d+(?:/[+-]\d+)*) \(", r" \1 melee (", (r["melee"] or "").replace("–", "-")))
            if att:
                voce["attacchi"] = att
            gs = re.match(r"(\d+(?:/\d+)?)", r["cr"] or "")
            if gs:
                voce["gs"] = gs.group(1) if "/" in gs.group(1) else int(gs.group(1))
            voce["fonte"] = f.name
            out.setdefault(r["nome"].strip().lower(), voce)
        con.close()
    return out


def _toml(v) -> str:
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k if re.fullmatch(r'[a-z_]+', k) else chr(34) + k + chr(34)} = {_toml(x)}"
                                for k, x in v.items()) + " }"
    if isinstance(v, list):
        return "[" + ", ".join(_toml(x) for x in v) + "]"
    return str(v) if isinstance(v, int) else '"' + str(v).replace('"', "'") + '"'


def main(argv: "list[str]") -> int:
    if len(argv) != 3 or argv[1] not in ("srd", "prd"):
        print(__doc__, file=sys.stderr)
        return 2
    srd = argv[1] == "srd"
    cr = creature(Path(argv[2])) if srd else creature_prd(Path(argv[2]))
    dove = "sistemi/dnd35" if srd else "sistemi/pf1e"
    print(f"# {dove}/dati/creature_base.toml — le creature base "
          + ("dell'SRD 3.5" if srd else "dei Bestiary PF1e") + " (ADR-0126, lotto 5)")
    print("#\n# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_creature_base.py")
    print("# sui blocchi di statistiche di monsters/*.md dell'SRD 3.5 (OGL). Non si corregge a mano." if srd else
          "# sulla tabella creature_details di book-b1…b4.db di PSRD-Data (PRD PF1e, OGL). Non si corregge a mano.")
    print("# dv/dado = dadi vita razziali; naturale = bonus di armatura naturale; attacchi = attacchi")
    print("# naturali col dado della creatura e quanti; mdl = modificatore di livello; gs = grado di sfida.")
    if srd:
        print("# avanza = \"classe\": la riga «Advancement» dice «By character class» (SRD, «Improving Monsters»:")
        print("# solo queste creature hanno l'equipaggiamento di un PNG; le altre hanno un tesoro).")
    print(f"# {len(cr)} creature.\n\n[creature_base]")
    for nome in sorted(cr):
        print(f'"{nome}" = {_toml(cr[nome])}')
    if srd:
        print("\n# I draghi veri (cromatici e metallici): il dado degli attacchi naturali viene dalla taglia,")
        print("# tabella «Dragon Space/Reach, Attacks, and Damage» di monsters-dr-dw.md.\n[draghi]")
        for taglia, att in draghi(Path(argv[2])).items():
            print(f'{taglia} = {_toml(att)}')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
