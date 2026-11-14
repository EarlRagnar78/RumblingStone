#!/usr/bin/env python3
"""Scrive `sistemi/pf1e/dati/codex.toml`: l'equipaggiamento dei PNG dell'NPC Codex e del
Monster Codex di PF1e, per classe e livello, e `sistemi/pf1e/dati/oggetti.toml`: il valore
dell'equipaggiamento di un PNG per livello (Core Rulebook, Tabella 14-9) (ADR-0134).

Uso: python3 -I estrai_codex.py [<cartella di PSRD-Data>]            # scrive il file
     python3 -I estrai_codex.py --check [<cartella di PSRD-Data>]    # 1 se il file non è aggiornato

Dal PRD PF1e (PSRD-Data@76ea4784, OGL), tabella `creature_details` di book-npc.db e book-mc.db:
il nome del PNG, razza, classi e livelli («human barbarian 1»), il grado di sfida e gli elenchi
«Gear», «Combat Gear» e «Other Gear», un oggetto per voce. Le monete («55 gp») vanno a parte.
La Tabella 14-9 viene dalla sezione «Table: NPC Gear» di book-cr.db.
Deterministico: stesso ingresso, stessi byte.

`--cerca CLASSE LIVELLO` (nomi inglesi: fighter, cleric, warrior…) elenca i PNG dei Codex di
quella classe e livello col prezzo 3.5 di ogni oggetto che `ricchezza` conosce e il tetto della
Tabella 4-23; non legge la cache.
"""
from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "pf1e" / "dati" / "codex.toml"
DEST_PNG = ROOT / "sistemi" / "pf1e" / "dati" / "oggetti.toml"
COLONNE = {"Weapons": "armi", "Protection": "protezione", "Magic": "magia", "Limited Use": "uso_limitato",
           "Gear": "attrezzatura"}
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "PSRD-Data-76ea47846041"
LIBRI = (("npc", "NPC Codex"), ("mc", "Monster Codex"))
_CLASSE = re.compile(r"([a-z][a-z' -]*?) (\d+)(?=/|$)")


def _voci(testo: "str | None") -> "list[str]":
    """Gli oggetti dell'elenco: divisi alle virgole fuori dalle parentesi, senza punto finale."""
    if not testo:
        return []
    voci, livello, pezzo = [], 0, ""
    for c in re.sub(r"<[^>]+>", "", testo).replace("’", "'"):
        livello += (c == "(") - (c == ")")
        if c in ",;" and livello == 0:
            voci.append(pezzo)
            pezzo = ""
        else:
            pezzo += c
    return [re.sub(r"\s+", " ", v).strip(" .") for v in voci + [pezzo] if v.strip(" .")]


def _classi(razza_classe: str) -> "tuple[str, dict[str, int]]":
    """«half-orc barbarian 3/fighter 2» → («half-orc», {barbarian: 3, fighter: 2})."""
    pezzi = razza_classe.lower().split("/")
    primo = _CLASSE.search(pezzi[0])
    if not primo:
        return razza_classe.lower(), {}
    parole = primo.group(1).split()
    # la classe è l'ultima parola del primo pezzo (due per «arcane archer» e simili non servono:
    # la chiave resta il testo intero in `chi`)
    classi = {parole[-1]: int(primo.group(2))}
    for p in pezzi[1:]:
        m = _CLASSE.search(p.strip())
        if m:
            classi[m.group(1).strip()] = int(m.group(2))
    return " ".join(parole[:-1]), classi


def png(cartella: Path) -> "list[dict]":
    out = []
    for sigla, _ in LIBRI:
        db = sqlite3.connect(f"file:{cartella / f'book-{sigla}.db'}?mode=ro", uri=True)
        for nome, chi, gs, gear, combat, altro in db.execute(
                "select s.name, cd.super_race, cd.cr, cd.gear, cd.combat_gear, cd.other_gear "
                "from creature_details cd join sections s on s.section_id = cd.section_id "
                "order by s.section_id"):
            razza, classi = _classi(chi or "")
            voci_combat, voci_altro = _voci(combat), _voci(gear) + _voci(altro)
            if not classi or not (voci_combat or voci_altro):
                continue
            monete = [v for v in voci_altro if re.fullmatch(r"[\d,]+ [gsc]p", v)]
            mo = sum(int(v.split()[0].replace(",", "")) for v in monete if v.endswith("gp"))
            out.append({"nome": nome, "libro": sigla, "chi": chi.lower(), "razza": razza, "classi": classi,
                        "livello": sum(classi.values()), "gs": gs or "",
                        "combattimento": voci_combat, "altro": [v for v in voci_altro if v not in monete], "mo": mo})
        db.close()
    return out


def _s(v: str) -> str:
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def testo(cartella: Path) -> str:
    righe = [
        "# sistemi/pf1e/dati/codex.toml — l'equipaggiamento dei PNG dell'NPC Codex e del Monster Codex",
        "# di PF1e, per classe e livello (ADR-0134)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_codex.py",
        "# sulla tabella creature_details di book-npc.db e book-mc.db di PSRD-Data (PRD PF1e, OGL).",
        "# Non si corregge a mano. `mo` sono le monete d'oro dell'elenco; i prezzi degli oggetti sono",
        "# quelli di PF1e e non stanno qui.",
        "",
    ]
    tutti = png(cartella)
    for p in tutti:
        righe += ["[[codex]]", f"nome = {_s(p['nome'])}", f"libro = {_s(p['libro'])}", f"chi = {_s(p['chi'])}",
                  f"razza = {_s(p['razza'])}",
                  "classi = { " + ", ".join(f"{_s(k)} = {v}" for k, v in p["classi"].items()) + " }",
                  f"livello = {p['livello']}", f"gs = {_s(p['gs'])}",
                  "combattimento = [" + ", ".join(_s(v) for v in p["combattimento"]) + "]",
                  "altro = [" + ", ".join(_s(v) for v in p["altro"]) + "]", f"mo = {p['mo']}", ""]
    return "\n".join(righe).rstrip("\n") + "\n"


def testo_png(cartella: Path) -> str:
    """La Tabella 14-9: una riga per livello di PNG base (1-20) più l'ultima, il 20° eroico. Il PNG
    eroico (classi da PG) di livello N usa la riga del PNG base di livello N + 1."""
    db = sqlite3.connect(f"file:{cartella / 'book-cr.db'}?mode=ro", uri=True)
    (corpo,) = db.execute("select body from sections where name = 'Table: NPC Gear' and type = 'table'").fetchone()
    db.close()
    righe = [[re.sub(r"<[^>]+>", "", c).replace("&mdash;", "—").strip()
              for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", corpo, re.S)]
    testa, dati = righe[0], righe[1:]
    assert len(dati) == 21 and testa[:3] == ["Basic Level", "Heroic Level", "Total gp Value"], (len(dati), testa)

    def mo(c: str) -> int:
        return 0 if c == "—" else int(c.replace(",", "").replace(" gp", ""))
    assert [r[0] for r in dati[:20]] == [str(i) for i in range(1, 21)] and dati[20][1] == "20"
    totale = [mo(r[2]) for r in dati]
    fuori = [
        "# sistemi/pf1e/dati/oggetti.toml — il valore dell'equipaggiamento di un PNG per livello (ADR-0134)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_codex.py",
        "# dalla sezione «Table: NPC Gear» di book-cr.db di PSRD-Data (PRD PF1e, Core Rulebook,",
        "# Tabella 14-9, OGL). Non si corregge a mano. Valori in mo.",
        "",
        "[oggetti.png]",
        "# base = PNG con classi da PNG, dal 1° al 20° livello; eroico = PNG con classi da PG, dal 1° al 20°",
        f"base = {totale[:20]}",
        f"eroico = {totale[1:]}",
        "",
        "[oggetti.png.categorie]",
        "# una voce per riga della tabella (21): la riga del PNG base di livello N è la N-esima, quella",
        "# dell'eroico di livello N è la (N + 1)-esima",
    ]
    for inglese, nome in COLONNE.items():
        fuori.append(f"{nome} = {[mo(r[testa.index(inglese)]) for r in dati]}")
    return "\n".join(fuori) + "\n"


def cerca(classe: str, livello: int) -> int:
    """I PNG dei Codex di quella classe e livello, coi prezzi del 3.5 dove `ricchezza` li conosce.

    Un oggetto senza prezzo («?») o non c'è nel 3.5 o `ricchezza` non lo riconosce: lo decide il DM
    su una card (punto 7 della regola, ADR-0134). Il totale è quindi un minimo."""
    import tomllib
    sys.path.insert(0, str(ROOT / "scripts"))
    import verifica_scheda as V
    from dmcore import sistemi as S
    d = S.dati("dnd35", "creature.costruzione")["oggetti"]
    tetto = d["png"]["per_livello"]
    png = [x for x in tomllib.loads(DEST.read_text(encoding="utf-8"))["codex"]
           if classe.lower() in x["classi"] and x["livello"] == livello]
    for x in png:
        print(f"{x['nome']} ({x['chi']}; {'NPC' if x['libro'] == 'npc' else 'Monster'} Codex; GS {x['gs']})")
        totale = x["mo"]
        for gruppo in ("combattimento", "altro"):
            for voce in x[gruppo]:
                prezzi = V._oggetti_col_prezzo(voce, d, "dnd35")
                mo = sum(m for _, m in prezzi)
                totale += mo
                print(f"  {gruppo:13} {voce}: {str(mo) + ' mo' if prezzi else '?'}")
        print(f"  monete {x['mo']} mo; totale 3.5 almeno {totale} mo; Tabella 4-23 al {livello}° livello: "
              f"{tetto[min(livello, len(tetto)) - 1]} mo")
    if not png:
        print(f"nessun PNG di classe «{classe}» e livello {livello} nei Codex: budget per categorie della "
              f"Tabella 14-9 e oggetti su card (punto 6)")
    return 0


def main(argv: "list[str]") -> int:
    if "--cerca" in argv:
        i = argv.index("--cerca")
        if len(argv) != i + 3 or not argv[i + 2].isdigit():
            print("uso: estrai_codex.py --cerca CLASSE LIVELLO", file=sys.stderr)
            return 2
        return cerca(argv[i + 1], int(argv[i + 2]))
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    cartella = Path(resto[0]) if resto else CACHE
    if not (cartella / "book-npc.db").is_file():
        print(f"estrai_codex: manca {cartella}/book-npc.db", file=sys.stderr)
        return 2
    nuovo, nuovo_png = testo(cartella), testo_png(cartella)
    if check:
        vecchi = [f for f, n in ((DEST, nuovo), (DEST_PNG, nuovo_png))
                  if not f.is_file() or f.read_text(encoding="utf-8") != n]
        for f in vecchi:
            print(f"estrai_codex: {f.relative_to(ROOT)} non è aggiornato", file=sys.stderr)
        return 1 if vecchi else 0
    DEST.write_text(nuovo, encoding="utf-8")
    DEST_PNG.write_text(nuovo_png, encoding="utf-8")
    print(f"estrai_codex: scritto {DEST.relative_to(ROOT)} ({nuovo.count('[[codex]]')} PNG)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
