#!/usr/bin/env python3
"""estrai_prd_pf1e.py — le tabelle numeriche PF1e dei plugin, dal PRD in cache.

Scrive i dati del plugin `sistemi/pf1e/dati/` leggendo il PRD di Pathfinder 1e
(`devonjones/PSRD-Data@76ea4784`, scaricato con `riscontro_srd.py scarica`).
Niente numeri a mano: ogni valore viene da una tabella del PRD, citata per
libro, id della sezione e nome. Rilanciato sulla stessa cache, riscrive gli
stessi byte (con `--check` esce 1 se i file sul disco sono diversi).

    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py           # scrive
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py --check   # confronta

Tabelle (Open Game Content, OGL 1.0a; il testo della licenza è in OGL.txt):
    book-cr 2743  Character Advancement and Level-Dependent Bonuses  → pe.toml
    book-cr 3655  Experience Point Awards                            → incontri.toml
    book-cr 3653  Encounter Design                                   → incontri.toml
    book-cr 3661  Treasure Values per Encounter                      → tesoro.toml
    book-b1 116   Creature Statistics by Type                        → creature.toml
    book-b1 160   Size Bonuses and Penalties                         → creature.toml
    book-cr/apg/acg/uc/um  le tabelle delle classi (BAB e TS)       → conformita_prd.toml
    book-b1 361-385, 405-423  sensi dei tipi e dei sottotipi        → conformita_prd.toml
    book-b1…b4  i sensi degli umanoidi del Bestiario                → conformita_prd.toml
    book-b1 1112  Corrupt Water (drago nero)                        → conformita_prd.toml
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sqlite3
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "pf1e" / "dati"
COMMIT = "76ea47846041"
PRD = f"PSRD-Data-{COMMIT}"


def cache() -> Path:
    for c in (os.environ.get("RUMBLINGSTONE_SRD_CACHE"),
              os.path.join(os.environ.get("XDG_CACHE_HOME", ""), "rumblingstone", "srd")
              if os.environ.get("XDG_CACHE_HOME") else None,
              str(Path.home() / ".cache" / "rumblingstone" / "srd")):
        if c and (Path(c) / PRD).is_dir():
            return Path(c) / PRD
    sys.exit("manca il PRD in cache: python3 scripts/riscontro_srd.py scarica")


class _Righe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.righe, self._riga, self._cella = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._riga = []
        elif tag in ("td", "th") and self._riga is not None:
            self._cella = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cella is not None:
            self._riga.append(re.sub(r"\s+", " ", "".join(self._cella)).strip())
            self._cella = None
        elif tag == "tr" and self._riga is not None:
            self.righe.append(self._riga)
            self._riga = None

    def handle_data(self, data):
        if self._cella is not None:
            self._cella.append(data)


def tabella(base: Path, libro: str, sid: int, nome: str) -> "list[list[str]]":
    c = sqlite3.connect(base / f"book-{libro}.db")
    r = c.execute("select name, body from sections where section_id=?", (sid,)).fetchone()
    if not r or r[0] != nome:
        sys.exit(f"book-{libro} {sid}: atteso «{nome}», trovato «{r and r[0]}»")
    p = _Righe()
    p.feed(html.unescape(r[1]))
    return [x for x in p.righe if x]


def numero(s: str) -> int:
    s = s.replace(",", "").replace("gp", "").replace("–", "-").replace("–", "-").strip()
    return int(s)


def fonte(libro: str, sid: int, nome: str) -> str:
    return f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}, book-{libro}.db sezione {sid} «{nome}»"'


def pe(base: Path) -> str:
    nome = "Table: Character Advancement and Level-Dependent Bonuses"
    righe = tabella(base, "cr", 2743, nome)
    tracce = {"lenta": {}, "media": {}, "veloce": {}}
    for r in righe:
        m = re.match(r"^(\d+)(st|nd|rd|th)$", r[0])
        if not m:
            continue
        liv = int(m.group(1))
        for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
            tracce[k][liv] = 0 if liv == 1 else numero(v)
    out = ["# sistemi/pf1e/dati/pe.toml — i PE per livello, tre tracce (generato da estrai_prd_pf1e.py)",
           fonte("cr", 2743, nome), ""]
    for k in ("lenta", "media", "veloce"):
        out.append(f"[soglie.{k}]")
        out += [f'"{liv}" = {v}' for liv, v in sorted(tracce[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tracce.values())
    return "\n".join(out)


def incontri(base: Path) -> str:
    n1 = "Table: Experience Point Awards"
    righe = tabella(base, "cr", 3655, n1)
    px = {}
    for r in righe:
        if re.fullmatch(r"\d+(/\d+)?", r[0]) and len(r) >= 2:
            px[r[0]] = numero(r[1])
    n2 = "Table: Encounter Design"
    diff = {}
    for r in tabella(base, "cr", 3653, n2):
        if len(r) == 2 and r[1].startswith("APL"):
            d = r[1].replace("APL", "").replace("–", "-").replace("–", "-").strip() or "0"
            diff[r[0]] = int(d)
    out = ["# sistemi/pf1e/dati/incontri.toml — PE per GS e difficoltà (generato da estrai_prd_pf1e.py)",
           "# Un incontro PF1e vale la somma dei PE delle creature; il suo GS è il più alto",
           "# il cui valore in PE non supera la somma («Designing Encounters», book-cr 3652).",
           fonte("cr", 3655, n1), f'fonte_difficolta = "book-cr.db sezione 3653 «{n2}»"',
           'metodo = "somma_px"  # letto da suggest_encounter (ADR-0111, L4)', "", "[px_per_gs]"]
    def chiave(g):
        a, _, b = g.partition("/")
        return int(a) / int(b) if b else int(a)
    out += [f'"{g}" = {v}' for g, v in sorted(px.items(), key=lambda kv: chiave(kv[0]))]
    out += ["", "[difficolta]  # GS dell'incontro = APL + scarto"]
    out += [f'"{k.lower()}" = {v}' for k, v in diff.items()]
    assert len(px) == 30 and diff
    return "\n".join(out) + "\n"


def tesoro(base: Path) -> str:
    nome = "Table: Treasure Values per Encounter"
    out = ["# sistemi/pf1e/dati/tesoro.toml — mo per incontro per APL (generato da estrai_prd_pf1e.py)",
           fonte("cr", 3661, nome), ""]
    tr = {"lenta": {}, "media": {}, "veloce": {}}
    for r in tabella(base, "cr", 3661, nome):
        if re.fullmatch(r"\d+", r[0]) and len(r) >= 4:
            for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
                tr[k][int(r[0])] = numero(v)
    for k in ("lenta", "media", "veloce"):
        out.append(f"[mo_per_incontro.{k}]")
        out += [f'"{a}" = {v}' for a, v in sorted(tr[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tr.values())
    return "\n".join(out)


def creature(base: Path) -> str:
    n1 = "Table: Creature Statistics by Type"
    bab = {"HD × 3/4 (Medium BAB)": 0.75, "HD (Fast BAB)": 1.0, "HD × 1/2 (Slow BAB)": 0.5}
    ts = {"Fort": "temp", "Ref": "rifl", "Will": "vol"}
    tipi = []
    for r in tabella(base, "b1", 116, n1):
        if len(r) == 5 and r[1].startswith("d"):
            buoni = [ts[x.strip()] for x in r[3].split(",") if x.strip() in ts]
            var = re.search(r"any (one|two)", r[3])
            tipi.append((r[0].lower(), int(r[1][1:]), bab[r[2]], buoni,
                         {"one": 1, "two": 2}[var.group(1)] if var else 0,
                         int(re.match(r"(\d+)", r[4]).group(1))))
    n2 = "Table: Size Bonuses and Penalties"
    taglie = []
    for r in tabella(base, "b1", 160, n2):
        if len(r) == 5 and r[0] in ("Fine", "Diminutive", "Tiny", "Small", "Medium", "Large",
                                    "Huge", "Gargantuan", "Colossal"):
            taglie.append((r[0].lower(), numero(r[1]), numero(r[2])))
    out = ["# sistemi/pf1e/dati/creature.toml — tipi e taglie PF1e (generato da estrai_prd_pf1e.py)",
           fonte("b1", 116, n1), f'fonte_taglie = "book-b1.db sezione 160 «{n2}»"', "",
           "# tipo = { dv = faccia del dado, bab = per DV, ts_buoni, ts_a_scelta (umanoide 1, esterno 2), gradi = per DV + Int }",
           "[tipi]"]
    for nome, dv, b, buoni, scelta, gradi in tipi:
        lista = ", ".join(f'"{x}"' for x in buoni)
        out.append(f'"{nome}" = {{ dv = {dv}, bab = {b}, ts_buoni = [{lista}], ts_a_scelta = {scelta}, gradi = {gradi} }}')
    out += ["", "# taglia = { ca_attacco, bmc_dmc }", "[taglie]"]
    out += [f'"{n}" = {{ ca_attacco = {a}, bmc_dmc = {c} }}' for n, a, c in taglie]
    assert len(tipi) == 13 and len(taglie) == 9
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# conformita_prd.toml: le regole PF1e che conformita_statblocchi controlla
# sulle schede (BAB e TS per classe, sensi per tipo, sottotipo e razza).
# ---------------------------------------------------------------------------
LIBRI_CLASSI = ("cr", "apg", "acg", "uc", "um")
#: Le progressioni PF1e: si verifica livello per livello che la tabella del PRD
#: sia una di queste, altrimenti la classe non entra (e il generatore lo dice).
BAB = {1.0: lambda L: L, 0.75: lambda L: 3 * L // 4, 0.5: lambda L: L // 2}
TS = {"buono": lambda L: 2 + L // 2, "scarso": lambda L: L // 3,
      "buono_prestigio": lambda L: (L + 1) // 2, "scarso_prestigio": lambda L: (L + 1) // 3}
#: piedi → metri, alla scala del progetto (1,5 m per 5 piedi)
METRI = {30: 9, 60: 18, 90: 27, 120: 36}


def _ordinale(s: str) -> "int | None":
    m = re.match(r"(\d+)(st|nd|rd|th)$", s)
    return int(m.group(1)) if m else None


def _lessico(*categorie: str) -> "dict[str, str]":
    """{inglese: italiano} dal lessico PF1e del repo (prima voce vince)."""
    import csv
    out: "dict[str, str]" = {}
    for f in ("lessico_it_pf1.tsv", "lessico_it_35.tsv"):
        with open(ROOT / "scripts" / f, encoding="utf-8") as fh:
            for r in csv.reader(fh, delimiter="\t"):
                if len(r) >= 3 and r[2] in categorie:
                    out.setdefault(r[1], r[0])
    return out


def _classi(base: Path):
    fuori, scartate = [], []
    for libro in LIBRI_CLASSI:
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.section_id, s.name, s.subtype, s.lft, s.rgt from sections s "
             "join class_details cd on cd.section_id = s.section_id order by s.section_id")
        for sid, nome, tipo, lft, rgt in c.execute(q).fetchall():
            # la prima tabella della classe con «Level» in testa; lo Swashbuckler
            # (book-acg 1145) ha le teste «Bonus, Save, Save, Save»: l'ordine è
            # quello di tutte le altre (BAB, Tempra, Riflessi, Volontà)
            t, col = None, None
            for tid, corpo in c.execute("select section_id, body from sections where type = 'table' "
                                        "and lft > ? and rgt < ? order by lft", (lft, rgt)).fetchall():
                p = _Righe()
                p.feed(html.unescape(corpo or ""))
                testa = next((r for r in p.righe if r and r[0] == "Level"), None)
                if not testa:
                    continue
                if any(h.startswith("Base Attack") for h in testa):
                    col = [next(i for i, h in enumerate(testa) if h.startswith(k))
                           for k in ("Base Attack", "Fort", "Ref", "Will")]
                elif testa[1:5] == ["Bonus", "Save", "Save", "Save"]:
                    col = [1, 2, 3, 4]
                else:
                    continue
                t = (tid, corpo)
                break
            if not t:
                scartate.append(f"{nome} (book-{libro} {sid}: nessuna tabella)")
                continue
            righe = set()
            for r in p.righe:
                if r and _ordinale(r[0]) and len(r) > max(col):
                    try:
                        righe.add((_ordinale(r[0]),) + tuple(int(r[i].split("/")[0]) for i in col))
                    except ValueError:
                        pass
            righe = sorted(righe)
            bab = next((k for k, f in BAB.items() if all(x[1] == f(x[0]) for x in righe)), None)
            ts = [next((k for k, f in TS.items() if all(x[i] == f(x[0]) for x in righe)), None)
                  for i in (2, 3, 4)]
            if bab is None or None in ts or len(righe) not in (10, 20):
                scartate.append(f"{nome} (book-{libro} {t[0]}: progressione fuori formula)")
                continue
            fuori.append((nome.lower(), bab, ts, tipo, libro, t[0]))
    return fuori, scartate


def _sensi_di(testo: str) -> "tuple[int, bool]":
    dv = re.search(r"[Dd]arkvision (\d+) feet", testo)
    return (METRI[int(dv.group(1))] if dv else 0), bool(re.search(r"[Ll]ow-light vision", testo))


def _sensi_regole(base: Path, primo: int, ultimo: int):
    c = sqlite3.connect(base / "book-b1.db")
    fuori = []
    for sid, nome in c.execute("select section_id, name from sections where section_id between ? and ? "
                               "and type = 'section' and url like 'pfsrd://Bestiary/Rules/Creature Types/%' "
                               "order by section_id", (primo, ultimo)).fetchall():
        corpi = [c.execute("select body from sections where section_id = ?", (sid,)).fetchone()[0] or ""]
        corpi += [b or "" for (b,) in c.execute("select body from sections where parent_id = ?", (sid,))]
        testo = re.sub(r"<[^>]+>", " ", " ".join(corpi))
        dv, ll = _sensi_di(testo)
        if dv or ll:
            fuori.append((nome.replace(" Subtype", "").lower(), dv, ll, sid))
    return fuori


def _sensi_razze(base: Path):
    it = _lessico("mostro", "razza")
    fuori = {}
    for libro in ("b1", "b2", "b3", "b4"):
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.section_id, s.name, cd.senses from sections s join creature_details cd "
             "on cd.section_id = s.section_id where cd.creature_type = 'Humanoid' order by s.section_id")
        for sid, nome, sensi in c.execute(q):
            dv = re.search(r"darkvision (\d+) ft", sensi or "")
            ll = "low-light vision" in (sensi or "")
            ita = it.get(nome)
            if not (dv or ll) or not ita or "(" in nome or ita.startswith("Archetipo") or ita in fuori:
                continue
            fuori[ita] = (nome, METRI[int(dv.group(1))] if dv else 0, ll, libro, sid)
    return fuori


def conformita_prd(base: Path) -> str:
    classi, scartate = _classi(base)
    it = {k.lower(): v for k, v in _lessico("classe", "classe di prestigio").items()}
    out = ["# sistemi/pf1e/dati/conformita_prd.toml — le regole PF1e che conformita_statblocchi",
           "# controlla sulle schede (generato da estrai_prd_pf1e.py, non si scrive a mano).",
           f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}: tabelle delle classi, '
           'Bestiary «Creature Types», creature del Bestiario 1-4"', "",
           "# classe = { bab per livello, ts = [Tempra, Riflessi, Volontà], tabella del PRD }",
           "# buono = 2 + L/2, scarso = L/3; *_prestigio = (L+1)/2 e (L+1)/3 (classi di prestigio)",
           "[classi]"]
    for nome, bab, ts, tipo, libro, tid in classi:
        lista = ", ".join(f'"{x}"' for x in ts)
        out.append(f'"{nome}" = {{ bab = {bab}, ts = [{lista}], tipo = "{tipo}", tabella = "book-{libro} {tid}" }}')
    out += ["", "# nome italiano (lessico_it_pf1.tsv, classi PNG da lessico_it_35.tsv) = classe del PRD",
            "[alias_classi]"]
    alias = {}
    for nome, *_ in classi:
        if nome in it:
            alias[it[nome].lower()] = nome
    out += [f'"{k}" = "{v}"' for k, v in sorted(alias.items())]
    if scartate:
        out += ["", "# fuori: " + " · ".join(scartate)]
    out += ["", "# scurovisione in metri (0 = no), visione crepuscolare; book-b1 «Creature Types»",
            "[sensi.tipi]"]
    for nome, dv, ll, sid in _sensi_regole(base, 361, 386):
        out.append(f'"{nome}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, sezione = {sid} }}')
    out += ["", "[sensi.sottotipi]"]
    for nome, dv, ll, sid in _sensi_regole(base, 388, 433):
        out.append(f'"{nome}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, sezione = {sid} }}')
    out += ["", "# umanoidi del Bestiario 1-4 con sensi propri, per nome italiano (lessico_it_pf1.tsv)",
            "[sensi.razze]"]
    for ita, (nome, dv, ll, libro, sid) in sorted(_sensi_razze(base).items()):
        out.append(f'"{ita.lower()}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, '
                   f'prd = "{nome}", fonte = "book-{libro} {sid}" }}')
    c = sqlite3.connect(base / "book-b1.db")
    testo = c.execute("select body from sections where section_id = 1112").fetchone()[0]
    assert "DC equal to the dragon's frightful presence" in testo, "Corrupt Water cambiato"
    out += ["", "[corrompere_acqua]",
            '# «Liquid-based magic items … must succeed on a Will save (DC equal to the dragon\'s',
            "# frightful presence) or become ruined» — la stessa regola dell'SRD 3.5",
            'cd = "presenza_terrificante"', 'fonte = "book-b1 1112 «Corrupt Water»"']
    assert len(classi) >= 40 and "fighter" in alias.values()
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# classi.toml: dado vita, BAB, TS, gradi e griglie degli incantesimi di ogni
# classe del PRD (ADR-0119, lotto 2). Le progressioni di BAB e TS sono le
# stesse di `_classi`: una lettura sola delle tabelle.
# ---------------------------------------------------------------------------
COL_LIVELLO = {"0": 0, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5,
               "6th": 6, "7th": 7, "8th": 8, "9th": 9}
GRUPPO = {"core": "base", "base": "base", "hybrid": "ibrida", "npc": "png", "prestige": "prestigio"}
#: L'antipaladino (book-apg 2726) è «npc» nel PRD ma è una classe alternativa
#: di venti livelli, e il suo dado vita sta nel testo e non in class_details.
GRUPPO_DI = {"antipaladin": "alternativa"}
TS_SIGLA = ("temp", "rifl", "vol")


def _righe(corpo: str) -> "list[list[str]]":
    p = _Righe()
    p.feed(html.unescape(corpo or ""))
    return [r for r in p.righe if r]


def _slot(cella: str) -> "tuple[int | None, bool]":
    """«3» → (3, False); «1+1» → (1, True), il +1 è lo slot di dominio; «—» → (None, False)."""
    m = re.match(r"^(\d+)(\+1)?$", cella.strip())
    return (int(m.group(1)), bool(m.group(2))) if m else (None, False)


def _griglia(righe: "list[list[str]]", livelli: "list[int]") -> "tuple[dict, bool]":
    """{livello di classe: [slot per livello d'incantesimo da 0]}: le ultime
    len(livelli) celle di ogni riga. Dove la classe non ha il livello 0 la prima
    cifra è uno 0 che tiene l'indice allineato (come nel plugin 3.5)."""
    out, dominio = {}, False
    for r in righe:
        n = _ordinale(r[0])
        if not n or len(r) < len(livelli) + 1:
            continue
        celle = [_slot(c) for c in r[-len(livelli):]]
        dominio = dominio or any(d for _, d in celle)
        riga = [0] * (max(livelli) + 1)
        ultimo = -1
        for lv, (v, _) in zip(livelli, celle):
            if v is not None:
                riga[lv], ultimo = v, lv
        if ultimo >= 0:
            out[n] = riga[:ultimo + 1]
    return out, dominio


def _tabelle_di_classe(c, lft: int, rgt: int):
    return c.execute("select section_id, name, body from sections where type = 'table' "
                     "and lft > ? and rgt < ? order by lft", (lft, rgt)).fetchall()


def _dati_di_classe(base: Path):
    """Per ogni classe di `_classi`: dado vita, gradi, griglie. Chi non ha un
    dato dichiarato nel PRD esce in `scartate`, non con un numero inventato."""
    prog, scartate = _classi(base)
    out = []
    for nome, bab, ts, tipo, libro, tid in prog:
        c = sqlite3.connect(base / f"book-{libro}.db")
        sid, lft, rgt, dv = c.execute(
            "select s.section_id, s.lft, s.rgt, cd.hit_die from sections s join class_details cd "
            "on cd.section_id = s.section_id where lower(s.name) = ? order by s.section_id", (nome,)).fetchone()
        if not dv:
            r = c.execute("select body from sections where lft > ? and rgt < ? and name = 'Hit Die' "
                          "order by lft", (lft, rgt)).fetchone()
            m = r and re.search(r"\bd(\d+)\b", re.sub("<[^>]+>", "", r[0]))
            dv = m and "d" + m.group(1)
        g = c.execute("select body from sections where lft > ? and rgt < ? and name like 'Skill Ranks%' "
                      "order by lft", (lft, rgt)).fetchone()
        m = g and re.match(r"\s*(\d+) \+ Int", re.sub("<[^>]+>", "", g[0]))
        if not dv or not m:
            scartate.append(f"{nome} (book-{libro} {sid}: dado vita o gradi non dichiarati)")
            continue
        righe = _righe(c.execute("select body from sections where section_id = ?", (tid,)).fetchone()[0])
        testa = next(r for r in righe if r[0] == "Level")
        sotto = righe[righe.index(testa) + 1]
        voce = {"nome": nome, "dv": int(dv[1:]), "bab": bab, "gradi": int(m.group(1)),
                "ts_buoni": [k for k, x in zip(TS_SIGLA, ts) if x.startswith("buono")],
                "gruppo": GRUPPO_DI.get(nome, GRUPPO[tipo]), "libro": libro, "tabella": tid,
                "livelli": max(_ordinale(r[0]) or 0 for r in righe)}
        ultima = testa[-1]
        if all(x in COL_LIVELLO for x in sotto) and ultima.endswith(("Spells per Day", "Extracts per Day")):
            griglia, dominio = _griglia(righe, [COL_LIVELLO[x] for x in sotto])
            voce.update(griglia=griglia, slot_di_dominio=dominio, estratti=ultima.startswith("Extracts"),
                        livello_zero=COL_LIVELLO[sotto[0]] == 0)
        elif ultima.endswith(("Spells per Day", "Extracts per Day")):
            # classi di prestigio: «+1 level of existing class» ai livelli che avanzano
            voce["avanza_incantatore"] = sorted(
                _ordinale(r[0]) for r in righe if _ordinale(r[0]) and r[-1].startswith("+1 level"))
        for xid, xnome, corpo in _tabelle_di_classe(c, lft, rgt):
            chiave = ("conosciuti" if (xnome or "").endswith("Spells Known") else
                      "preparati" if (xnome or "").endswith("Spells Prepared") else None)
            if not chiave:
                continue
            r2 = _righe(corpo)
            t2 = r2[1] if r2[0] == ["Level", "Spells Known"] else r2[0][1:]
            voce[chiave], _ = _griglia(r2, [COL_LIVELLO[x] for x in t2])
            voce[chiave + "_tabella"] = xid
            # il bardo e l'arcanista hanno il livello 0 solo in questa tabella
            voce["livello_zero"] = voce.get("livello_zero", False) or t2[0] == "0"
        out.append(voce)
    return out, scartate


def _toml_lista(xs) -> str:
    return "[" + ", ".join(f'"{x}"' if isinstance(x, str) else str(x) for x in xs) + "]"


def classi(base: Path) -> str:
    dati, scartate = _dati_di_classe(base)
    it = {k.lower(): v for k, v in _lessico("classe", "classe di prestigio").items()}
    out = ["# sistemi/pf1e/dati/classi.toml — le classi PF1e (generato da estrai_prd_pf1e.py, non si scrive a mano).",
           f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}: la tabella di ogni classe, '
           '«Hit Die» e «Skill Ranks per Level»"', "",
           "# classe = { dv = faccia del dado vita, bab = per livello, ts_buoni, gradi = per livello + Int,",
           "#   gruppo = base | ibrida | png | prestigio | alternativa, livelli, libro e tabella del PRD }",
           "# BAB e TS buoni sono verificati livello per livello contro la formula (vedi conformita_prd.toml).",
           "[classi]"]
    for v in dati:
        out.append(f'"{v["nome"]}" = {{ dv = {v["dv"]}, bab = {v["bab"]}, ts_buoni = {_toml_lista(v["ts_buoni"])}, '
                   f'gradi = {v["gradi"]}, gruppo = "{v["gruppo"]}", livelli = {v["livelli"]}, '
                   f'libro = "{v["libro"]}", tabella = {v["tabella"]} }}')
    out += ["", "# classe = { griglia, conosciuti e preparati = chiavi delle tabelle sotto;",
            "#   livello_zero = la classe ha trucchetti o orazioni (in PF1e sono A VOLONTÀ: la cifra d'indice 0",
            "#     della griglia è quanti se ne preparano o se ne conoscono, non slot che si consumano);",
            "#   slot_di_dominio = +1 slot per livello d'incantesimo dal 1° (il «+1» della tabella, non contato nella griglia);",
            "#   estratti = la tabella è «Extracts per Day» (alchimista, investigatore) }",
            "# La caratteristica di lancio sta in conformita.toml [incantesimi.caratteristica], scelta a mano.",
            "[incantatori]"]
    for v in dati:
        if "griglia" not in v:
            continue
        campi = [f'griglia = "{v["nome"]}"']
        campi += [f'{k} = "{v["nome"]}"' for k in ("conosciuti", "preparati") if k in v]
        campi += [f'livello_zero = {str(v["livello_zero"]).lower()}',
                  f'slot_di_dominio = {str(v["slot_di_dominio"]).lower()}',
                  f'estratti = {str(v["estratti"]).lower()}']
        out.append(f'"{v["nome"]}" = {{ {", ".join(campi)} }}')
    out += ["", "# classi di prestigio: i livelli in cui la tabella dice «+1 level of existing class»",
            "[avanza_incantatore]"]
    out += [f'"{v["nome"]}" = {_toml_lista(v["avanza_incantatore"])}' for v in dati if v.get("avanza_incantatore")]
    for chiave, titolo in (("griglia", "incantesimi (o estratti) al giorno"),
                           ("conosciuti", "incantesimi conosciuti"), ("preparati", "incantesimi preparati")):
        tab = {"griglia": "griglie"}.get(chiave, chiave)
        out += ["", f"# --- {titolo}: livello di classe = [per livello d'incantesimo, da 0]",
                "# Dove la classe non ha il livello 0 la prima cifra è uno 0 d'allineamento."]
        for v in dati:
            if chiave not in v:
                continue
            sorgente = v["tabella"] if chiave == "griglia" else v[chiave + "_tabella"]
            out += ["", f'[{tab}."{v["nome"]}"]  # book-{v["libro"]} {sorgente}']
            out += [f'"{n}" = {_toml_lista(r)}' for n, r in sorted(v[chiave].items())]
    out += ["", "# nome italiano (lessico_it_pf1.tsv, classi PNG da lessico_it_35.tsv) = classe del PRD",
            "[alias]"]
    alias = {it[v["nome"]].lower(): v["nome"] for v in dati if v["nome"] in it}
    out += [f'"{k}" = "{v}"' for k, v in sorted(alias.items())]
    senza = sorted(v["nome"] for v in dati if v["nome"] not in it)
    if senza:
        out += ["", "# senza nome italiano nel lessico: " + ", ".join(senza)]
    if scartate:
        out += ["", "# fuori: " + " · ".join(scartate)]
    g = {v["nome"]: v for v in dati}
    # àncore: righe note del Core Rulebook, perché un cambio di lettura si veda qui
    assert g["wizard"]["griglia"][1] == [3, 1] and g["wizard"]["griglia"][20] == [4] * 10
    assert g["cleric"]["griglia"][1] == [3, 1] and g["cleric"]["slot_di_dominio"]
    assert g["paladin"]["griglia"][4] == [0, 0] and g["paladin"]["griglia"][20] == [0, 4, 4, 3, 3]
    assert g["bard"]["conosciuti"][1] == [4, 2] and g["sorcerer"]["conosciuti"][20] == [9, 5, 5, 4, 4, 4, 3, 3, 3, 3]
    assert g["fighter"]["dv"] == 10 and g["rogue"]["gradi"] == 8 and len(dati) >= 50
    return "\n".join(out) + "\n"


def _armature(base: Path):
    nome = "Table: Armor and Shields"
    it = {k.lower(): v.lower() for k, v in _lessico("equipaggiamento").items()}
    arm, scu, gruppo = [], [], None
    for r in tabella(base, "cr", 2955, nome):
        if len(r) == 1 and r[0] in ("Light armor", "Medium armor", "Heavy armor", "Shields", "Extras"):
            gruppo = r[0]
            continue
        if gruppo in (None, "Extras") or len(r) < 9:
            continue
        en = r[0].lower()
        # «+43» sullo scudo torre: il 3 è il richiamo della nota 3 della tabella
        ca = int(re.match(r"\+(\d)", r[2]).group(1))
        prova = int(r[4].replace("–", "-").replace("−", "-"))
        fallimento = int(r[5].rstrip("%"))
        if gruppo == "Shields":
            scu.append((en, ca, None if r[3] == "—" else int(r[3]), prova, fallimento, it.get(en)))
        else:
            arm.append((en, ca, int(r[3]), prova, fallimento,
                        {"Light armor": "leggera", "Medium armor": "media", "Heavy armor": "pesante"}[gruppo],
                        it.get(en)))
    assert len(arm) == 12 and len(scu) == 6 and ("full plate", 9, 1, -6, 35, "pesante") == arm[-1][:6]
    return arm, scu


#: Le taglie del PRD con la chiave che hanno in `[taglie]` (inglese minuscolo).
TAGLIE_COSTRUTTI = tuple((t, t.lower()) for t in (
    "Fine", "Diminutive", "Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"))


#: La tabella «Construct Size / Bonus Hit Points» del tipo costrutto, come la
#: pubblica il PRD di Paizo (legacy.aonprd.com/bestiary/creatureTypes.html,
#: Construct, letta il 2026-11-10): «—» per Fine, Diminutive e Tiny. Nel PSRD-Data
#: in cache manca (book-b1 sezione 366 la annuncia senza riportarla). Serve per le
#: taglie che nessuna scheda prova; per le altre deve concordare con le schede.
TABELLA_COSTRUTTI_PRD = {"fine": 0, "diminutive": 0, "tiny": 0, "small": 10, "medium": 20,
                         "large": 30, "huge": 40, "gargantuan": 60, "colossal": 80}
FONTE_TABELLA_COSTRUTTI = "legacy.aonprd.com/bestiary/creatureTypes.html, Construct"


def _pf_bonus_costrutti(base: Path) -> tuple[dict, list]:
    """I pf bonus dei costrutti per taglia, ricavati dalle schede dei Bestiary 1-4.

    La tabella del tipo costrutto (book-b1 sezione 366, «as shown on the
    following table») nel PRD non c'è. Il numero è il «+X» di `hp N (NdF+X)`
    delle schede di tipo construct senza Robustezza, senza Costituzione e non
    mitiche: lì il bonus di taglia è l'unico addendo. Una taglia entra solo se
    tutte le sue schede dicono lo stesso numero; le altre restano fuori."""
    per_taglia: dict[str, dict[int, list[str]]] = {}
    escluse = []
    for libro in ("b1", "b2", "b3", "b4"):
        c = sqlite3.connect(base / f"book-{libro}.db")
        for sid, nome, taglia, pf, tal, cos, mr in c.execute(
                "select s.section_id, s.name, d.size, d.hp, d.feats, d.constitution, d.mr "
                "from sections s join creature_details d on d.section_id = s.section_id "
                "where lower(d.creature_type) like '%construct%' order by s.section_id"):
            m = re.search(r"\((\d+)d(\d+)([+-]\d+)?\)", pf or "")
            motivo = ("pf illeggibili" if not m else
                      "mitica" if mr else
                      "Robustezza" if "toughness" in (tal or "").lower() else
                      "ha la Costituzione" if (cos or "").strip() not in ("", "-", "—", "–") else "")
            if motivo:
                escluse.append((libro, sid, nome, motivo))
                continue
            per_taglia.setdefault(taglia, {}).setdefault(int(m.group(3) or 0), []).append(
                f"{nome} {m.group(0)[1:-1]} (book-{libro} {sid})")
    return per_taglia, escluse


def creature_e_armature(base: Path) -> str:
    arm, scu = _armature(base)
    per_taglia, escluse = _pf_bonus_costrutti(base)
    out = [creature(base).rstrip("\n"), "",
           "# --- pf bonus dei costrutti per taglia. La tabella del tipo costrutto (book-b1",
           "# sezione 366, «as shown on the following table») nel PSRD-Data in cache non c'è:",
           "# il numero è ricavato dalle schede dei Bestiary 1-4, come «+X» di `hp N (NdF+X)`",
           "# nei costrutti senza Robustezza, senza Costituzione e non mitici, e deve concordare",
           f"# con la tabella del PRD pubblicato ({FONTE_TABELLA_COSTRUTTI}). Le taglie che",
           "# nessuna scheda prova prendono il valore della tabella («—» = 0).",
           "[pf_bonus_costrutti]"]
    for en, it in TAGLIE_COSTRUTTI:
        voci = per_taglia.get(en, {})
        tabella = TABELLA_COSTRUTTI_PRD[it]
        if len(voci) == 1:
            (bonus, schede), = voci.items()
            if bonus != tabella:
                raise SystemExit(f"costrutto {it}: le schede dicono +{bonus}, la tabella del PRD +{tabella}")
            quante = "1 scheda sola" if len(schede) == 1 else f"{len(schede)} schede concordi"
            out.append(f"{it} = {bonus}  # {quante}, come la tabella del PRD; prova: {schede[0]}")
        elif voci:
            raise SystemExit(f"costrutto {it}: schede discordi " + "; ".join(
                f"+{k} {v[0]}" for k, v in sorted(voci.items())))
        else:
            out.append(f"{it} = {tabella}  # tabella del PRD («—»); nessuna scheda di costrutto nel PSRD-Data")
    out.append(f"# schede escluse dal conto: {len(escluse)} ("
               + "; ".join(f"{n} {m}" for _l, _s, n, m in escluse) + ")")
    out += ["",
           "# --- armature e scudi: book-cr.db sezione 2955 «Table: Armor and Shields»",
           "# armatura = { ca, des_max, prova = penalità di armatura alla prova, fallimento = % arcano, categoria, it }",
           "# `it` è il nome italiano del lessico PF1e, quando c'è.",
           "[armature]"]
    for en, ca, des, prova, fall, cat, ita in arm:
        coda = f', it = "{ita}"' if ita else ""
        out.append(f'"{en}" = {{ ca = {ca}, des_max = {des}, prova = {prova}, fallimento = {fall}, '
                   f'categoria = "{cat}"{coda} }}')
    out += ["", "# scudo = { ca, des_max (solo lo scudo torre), prova, fallimento, it }", "[scudi]"]
    for en, ca, des, prova, fall, ita in scu:
        mezzo = f", des_max = {des}" if des is not None else ""
        coda = f', it = "{ita}"' if ita else ""
        out.append(f'"{en}" = {{ ca = {ca}{mezzo}, prova = {prova}, fallimento = {fall}{coda} }}')
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# liste_incantesimi.toml: la lista di classe di ogni incantatore PF1e, dalla
# tabella `spell_lists` dei libri del PRD (ADR-0119, lotto 3).
# ---------------------------------------------------------------------------
#: I libri del PRD che hanno incantesimi, nell'ordine in cui si leggono.
LIBRI_INCANTESIMI = ("cr", "apg", "um", "uc", "acg", "arg", "mc", "ma", "tech")


def _toml_testo(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def liste_incantesimi(base: Path) -> str:
    import csv
    dati = {v["nome"]: v for v in _dati_di_classe(base)[0] if "griglia" in v}
    classi_inc = set(dati)
    liste: "dict[str, dict[int, set[str]]]" = {}
    libro_di: "dict[str, str]" = {}
    scartate: "dict[str, int]" = {}
    mitici = 0
    for libro in LIBRI_INCANTESIMI:
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.name, s.subtype, sl.level, sl.class from spell_lists sl "
             "join sections s on s.section_id = sl.section_id order by sl.spell_list_id")
        for nome, sotto, livello, classe in c.execute(q).fetchall():
            if sotto == "mythic_spell":
                mitici += 1
                continue
            chiave = classe.lower()
            if chiave not in classi_inc:
                scartate[classe] = scartate.get(classe, 0) + 1
                continue
            assert libro_di.setdefault(nome, libro) == libro, f"{nome} in due libri"
            liste.setdefault(chiave, {}).setdefault(livello, set()).add(nome)
    # Il PRD dà al warpriest la lista del chierico fino al 9°, ma la classe lancia
    # fino al 6°: i livelli sopra la griglia non sono suoi e non entrano.
    oltre: "dict[str, int]" = {}
    for classe, livelli in liste.items():
        tetto = max(len(r) for r in dati[classe]["griglia"].values()) - 1
        for livello in [x for x in livelli if x > tetto]:
            oltre[classe] = oltre.get(classe, 0) + len(livelli.pop(livello))
    usati_ora = {n for livelli in liste.values() for voci in livelli.values() for n in voci}
    libro_di = {n: x for n, x in libro_di.items() if n in usati_ora}
    # Il livello 0 che `spell_lists` non ha, la pagina della lista lo scrive in chiaro
    # («0-Level Shaman Spells: arcane mark, bleed, …», ACG): si legge da lì
    # (lotto 4 delle regole complete, 2026-11-10).
    dal_testo: "dict[str, int]" = {}
    for classe in sorted(k for k in liste if dati[k]["livello_zero"] and 0 not in liste[k]):
        for libro in LIBRI_INCANTESIMI:
            c = sqlite3.connect(base / f"book-{libro}.db")
            r = c.execute("select coalesce(body, description) from sections where lower(name)=?",
                          (f"0-level {classe} spells",)).fetchone()
            if not r or not r[0]:
                continue
            testo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(r[0])))
            for pezzo in testo.split(","):
                nome = pezzo.strip().rstrip(".").strip()
                for lb in LIBRI_INCANTESIMI:
                    trovato = sqlite3.connect(base / f"book-{lb}.db").execute(
                        "select name from sections where type='spell' and lower(name)=?", (nome.lower(),)).fetchone()
                    if trovato:
                        liste.setdefault(classe, {}).setdefault(0, set()).add(trovato[0])
                        libro_di.setdefault(trovato[0], lb)
                        dal_testo[classe] = dal_testo.get(classe, 0) + 1
                        break
            break
    senza_zero = sorted(k for k in liste if dati[k]["livello_zero"] and 0 not in liste[k])
    it: "dict[str, str]" = {}
    with open(ROOT / "scripts" / "lessico_it_pf1.tsv", encoding="utf-8") as fh:
        for r in csv.reader(fh, delimiter="\t"):
            if len(r) >= 3 and r[2] == "incantesimo":
                it.setdefault(r[1].lower(), r[0])
    out = ["# sistemi/pf1e/dati/liste_incantesimi.toml — le liste di classe degli incantesimi PF1e",
           "# (generato da estrai_prd_pf1e.py, non si scrive a mano).",
           f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}: tabella spell_lists di '
           + ", ".join(f"book-{x}" for x in LIBRI_INCANTESIMI) + '"', "",
           "# [liste.\"classe\"] \"livello\" = [nomi del PRD, così come li scrive il PRD]",
           "# Le chiavi di classe sono quelle di classi.toml [incantatori].",
           "# «Sorcerer» e «Wizard» hanno nel PRD una riga ciascuno: le due liste sono uguali, e stanno tutte e due.",
           f"# Fuori: le versioni mitiche ({mitici} righe) e le liste che non sono una classe di classi.toml: "
           + ", ".join(f"{k} ({n} righe)" for k, n in sorted(scartate.items())) + ".",
           "# Tolti i livelli sopra la griglia della classe (il PRD copia la lista del chierico intera): "
           + (", ".join(f"{k} ({n} righe)" for k, n in sorted(oltre.items())) or "nessuno") + ".",
           "# Classi con trucchetti o orazioni di cui il PRD non elenca il livello 0 (buco della fonte, non riempito): "
           + (", ".join(senza_zero) or "nessuna") + ".",
           "# Livello 0 letto dal testo della lista di classe (spell_lists non lo ha): "
           + (", ".join(f"{k} ({n} voci)" for k, n in sorted(dal_testo.items())) or "nessuno") + ".",
           "# Una classe senza righe nel PRD non compare: " +
           (", ".join(sorted(classi_inc - set(liste))) or "nessuna") + "."]
    for classe in sorted(liste):
        out += ["", f'[liste."{classe}"]']
        for livello in sorted(liste[classe]):
            nomi = ", ".join(_toml_testo(n) for n in sorted(liste[classe][livello]))
            out.append(f'"{livello}" = [{nomi}]')
    usati = sorted(libro_di)
    out += ["", "# il libro del PRD di ogni incantesimo: chi costruisce può fermarsi al Core Rulebook (cr)", "[libro]"]
    out += [f"{_toml_testo(n)} = \"{libro_di[n]}\"" for n in usati]
    out += ["", "# nome italiano dal lessico PF1e (scripts/lessico_it_pf1.tsv, righe «incantesimo»), solo dove c'è;",
            "# il confronto ignora le maiuscole, perché il PRD scrive «Breath Of Life» e il lessico «Breath of Life»",
            "[nomi_it]"]
    out += [f"{_toml_testo(n)} = {_toml_testo(it[n.lower()])}" for n in usati if n.lower() in it]
    senza = [n for n in usati if n.lower() not in it]
    out += ["", f"# senza nome italiano nel lessico: {len(senza)} su {len(usati)}"]
    # la scuola di ogni incantesimo (spell_details.school del suo libro): serve a
    # Incantesimi focalizzati nel generatore (ADR-0126, 2026-11-18)
    scuola_di: "dict[str, str]" = {}
    for libro in LIBRI_INCANTESIMI:
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.name, d.school from spell_details d join sections s on s.section_id = d.section_id "
             "where s.subtype is null or s.subtype != 'mythic_spell' order by d.spell_detail_id")
        for nome, scuola in c.execute(q).fetchall():
            if libro_di.get(nome) == libro:
                assert scuola_di.setdefault(nome, scuola.lower()) == scuola.lower(), f"{nome}: due scuole"
    assert set(scuola_di) == set(usati), sorted(set(usati) - set(scuola_di))[:5]
    out += ["", "# la scuola di ogni incantesimo, dal PRD (spell_details.school); «universal» non è una scuola",
            "# che si possa focalizzare, e resta scritta com'è", "[scuole]"]
    out += [f"{_toml_testo(n)} = \"{scuola_di[n]}\"" for n in usati]
    assert scuola_di["Fireball"] == "evocation" and scuola_di["Linebreaker"] == "transmutation"
    assert liste["sorcerer"] == liste["wizard"] and len(liste) >= 20
    assert "Magic Missile" in liste["wizard"][1] and "Cure Light Wounds" in liste["cleric"][1]
    assert "Fireball" in liste["wizard"][3] and "Bless" in liste["paladin"][1]
    return "\n".join(out) + "\n"


FILE = {"pe.toml": pe, "incontri.toml": incontri, "tesoro.toml": tesoro, "creature.toml": creature_e_armature,
        "conformita_prd.toml": conformita_prd, "classi.toml": classi,
        "liste_incantesimi.toml": liste_incantesimi}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    base = cache()
    diversi = []
    for nome, f in FILE.items():
        testo = f(base)
        dest = DEST / nome
        if a.check:
            if not dest.is_file() or dest.read_text(encoding="utf-8") != testo:
                diversi.append(nome)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(testo, encoding="utf-8")
            print(f"scritto {dest.relative_to(ROOT)}")
    for d in diversi:
        print(f"🔴 {d} diverso dal PRD")
    return 1 if diversi else 0


if __name__ == "__main__":
    sys.exit(main())
