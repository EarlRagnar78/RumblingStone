#!/usr/bin/env python3
"""verifica_storia.py — i fatti della prosa contro il canone strutturato di state.yaml.

Prototipo della misura del 2026-11-12 (thread «Verificare la coerenza della
storia»). Applica alla storia il pattern di ADR-0124: un verificatore
deterministico che, per ogni violazione, restituisce `regola`, `atteso`, `ha`
e `file:riga`, così che chi ha scritto (un LLM o il DM) sappia cosa correggere.

La differenza con `scripts/coerenza_campagna.py fatti` è l'àncora.
`coerenza_campagna` confronta la prosa con la prosa: trova due valori diversi e
non sa quale è giusto. Qui il valore giusto è in `campaign/state.yaml` (il
master dei fatti, ADR-0050), quindi la violazione ha un `atteso`.

Regole (ognuna legge un campo strutturato e lo cerca in prosa):
  S1  giorno d'arrivo dell'orda a Rethmar   = march_clock.giorno_arrivo
  S2  giorno dei waypoint della marcia       ∈ march_clock.waypoints[].giorno
  S3  finestra delle quest di ARC-09         ⊆ archi[].march_clock della quest
  S4  livello del party dentro un arco       ∈ archi[].pg_livello dell'arco
  S5  chi porta quale artefatto              = artefatti[].portatore
  S6  modifiche permanenti alle caratteristiche di un PG: stesso segno del
      canone in party[].hp, e nessuna caratteristica che il canone non tocca
  S7  ogni eco `armato` ha almeno un file fuori da state.* che lo cita per ID
      (una promessa senza scena che la paga è il difetto A12 di ARC-08)

Fuori di proposito, e contato: «chi sa cosa» (§4 conoscenze) non ha un tempo
per riga, quindi non si può dire «X non può saperlo al giorno N». Il conteggio
esce in `non_verificabili`.

Prudenza: come coerenza_campagna salta le righe di storico (→, «prima della
correzione», barrato) e le frasi condizionali strette (se, qualora, ramo,
ritardo). Le esclusioni dei file sono le stesse (ESCLUDI_FILE).

Uso
  python3 verifica_storia.py [--state PATH] [--radice DIR] [--archi DIR ...] [--json]
  python3 verifica_storia.py --ancore ANCORE.json ...   # replay su commit senza state.yaml

Exit 0 = nessuna violazione · 1 = violazioni · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import coerenza_campagna as cc  # noqa: E402  (stesse esclusioni, stesso estrattore del portatore)

PG = cc.PG
STAT = {"FOR": "FOR", "DES": "DES", "COS": "COS", "INT": "INT", "SAG": "SAG", "CAR": "CAR",
        "STR": "FOR", "DEX": "DES", "CON": "COS", "WIS": "SAG", "CHA": "CAR"}
# condizionale STRETTO: la marcia si può ritardare, una quest si può anticipare
COND = re.compile(r"\bse\b|\bqualora\b|\bram[oi]\b|alternativ|ritard|rallent|anticip|"
                  r"\bdelay|\bslow|\bif\b|\bunless\b|\boppure\b|\bin caso\b|\bnel caso\b|"
                  r"\bdefault\b|\?|\bsenza\b|\bfallisc|\bfail", re.I)
GIORNO = re.compile(r"\b(?:day|giorno|g\.)\s*\**\s*(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\b", re.I)
LOCALE = re.compile(r"da giorni|days ago|dell'assedio|d'assedio|di battaglia|del torneo|of the siege|"
                    r"giorno\s+\d\s+(?:del|di)\b", re.I)
RETHMAR = re.compile(r"\b(rethmar|rethman|brindol)\b", re.I)
ARRIVO = re.compile(r"arriv|giung|reach|encamp|accamp|si accampa|alle porte|under siege|"
                    r"cinge d'assedio|inizia l'assedio|assault begins|arrives", re.I)
ORDA = re.compile(r"\b(orda|horde|azarr|mano rossa|red hand|armata|army|hobgoblin)\b", re.I)

WAYPOINT_CHIAVI = {
    "Vraath": r"vraath", "Skull Gorge": r"skull gorge|gola del teschio",
    "Drellin": r"drellin", "Terrelton": r"terrelton",
    "Marth Fen / Blackfens": r"marth fen|blackfens", "Elsir": r"elsir crossroads|crocevia",
}
QUEST_CHIAVI = {  # arco di ARC-09 -> parola che lo nomina in prosa
    "P2A Torre": r"torre invisibile", "P2 Rhest": r"\brhest\b",
    "P2B Torneo": r"\btorneo\b", "P3 Starsong": r"starsong", "P3 Ghostlord": r"ghostlord",
}
LIVELLO = [
    re.compile(r"\b(?:party|gruppo|pg|personaggi|eroi)\b[^.;:|]{0,25}?\b(?:di\s+)?"
               r"(?:livello|level|lv\.?|liv\.)\s*(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\b(?![,.]\d)", re.I),
    re.compile(r"\b(?:party|gruppo|pg|personaggi|eroi)\b[^.;:|]{0,20}?\b(?:al|di|del)\s+(\d{1,2})\s*°", re.I),
    re.compile(r"\bparty\s+(?:level\s+)?(\d{1,2})\b", re.I),
]
# l'APL non è il livello: tre PG di 13° hanno APL 12 (Terros, D15)
STORICO = cc.STORICO_RIGA


def _intervallo(s) -> tuple[int, int] | None:
    nums = [int(x) for x in re.findall(r"\d{1,2}", str(s or ""))]
    if not nums:
        return None
    return (min(nums), max(nums))


def ancore_da_state(path: Path) -> dict:
    d = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    mc = d.get("march_clock") or {}
    an = {"giorno_arrivo": mc.get("giorno_arrivo"), "waypoint": {}, "quest": {}, "livelli": {},
          "portatori": {}, "modifiche": {}, "echi": [], "conoscenze_senza_tempo": 0,
          "fonte": str(path)}
    for w in mc.get("waypoints") or []:
        for nome, rx in WAYPOINT_CHIAVI.items():
            if re.search(rx, str(w.get("waypoint", "")), re.I):
                an["waypoint"][nome] = _intervallo(w.get("giorno"))
    for a in d.get("archi") or []:
        arco = str(a.get("arco", "")).strip("* ")
        num = arco[:2]
        liv = _intervallo(a.get("pg_livello"))
        if liv and num.isdigit():
            lo, hi = an["livelli"].get(num, liv)
            an["livelli"][num] = (min(lo, liv[0]), max(hi, liv[1]))
        for q, rx in QUEST_CHIAVI.items():
            if num == "09" and re.search(rx, arco, re.I):
                an["quest"][q] = _intervallo(a.get("march_clock"))
    for a in d.get("artefatti") or []:
        port = str(a.get("portatore", ""))
        pg = next((p for p in PG if re.match(p + r"\b", port)), None)
        if pg:
            an["portatori"][str(a.get("artefatto", "")).split(" (")[0]] = pg
    for p in d.get("party") or []:
        mods = {}
        # separatore «/» obbligatorio fra le voci: nessuna ambiguità, nessun backtracking
        # esponenziale (CodeQL py/redos sulla forma con «\s*/?\s*» ripetuta)
        voce = r"[+−-] ?\d ?(?:FOR|DES|COS|INT|SAG|CAR)"
        m = re.search(r"(" + voce + r"(?: ?/ ?" + voce + r")*)\**\s*permanent",
                      str(p.get("hp", "")))
        if m:
            for seg, val, stat in re.findall(r"([+−-])\s*(\d)\s*(FOR|DES|COS|INT|SAG|CAR)", m.group(1)):
                mods[stat] = (-1 if seg in "−-" else 1) * int(val)
        elif re.search(r"nessun malus permanente", str(p.get("hp", "")), re.I):
            mods = {}
        else:
            continue
        an["modifiche"][p["pg"]] = mods
    for e in d.get("echi") or []:
        if e.get("stato") == "armato":
            an["echi"].append({"id": e["id"], "miccia": e.get("miccia")})
    an["conoscenze_senza_tempo"] = sum(1 for c in d.get("conoscenze") or [] if "tempo" not in c)
    an["conoscenze"] = len(d.get("conoscenze") or [])
    return an


def _frasi(riga: str) -> list[str]:
    return [f for f in re.split(r"(?<=[.;!])\s+|\s+\|\s+", riga) if f.strip()]


def file_da_leggere(radice: Path, archi: list[str]) -> list[Path]:
    out = []
    for a in archi:
        d = radice / a
        if d.is_dir():
            for p in sorted(d.rglob("*.md")):
                rel = str(p.relative_to(radice))
                if not cc.ESCLUDI_FILE.search(rel):
                    out.append(p)
    return out


def verifica(radice: Path, archi: list[str], an: dict) -> dict:
    viol: list[dict] = []
    files = file_da_leggere(radice, archi)

    def v(regola, atteso, ha, p, n, testo):
        viol.append({"regola": regola, "atteso": atteso, "ha": ha,
                     "file": str(p.relative_to(radice)), "riga": n, "testo": testo.strip()[:240]})

    for p in files:
        rel = str(p.relative_to(radice))
        arco_num = rel[:2] if rel[:2].isdigit() else None
        righe = p.read_text(encoding="utf-8", errors="replace").splitlines()
        fence = False
        titolo = ""
        for n, riga in enumerate(righe, 1):
            if riga.lstrip().startswith("```"):
                fence = not fence
                continue
            # giro 3: le cronologie stanno spesso in un blocco ``` (si leggono per
            # S1-S3), e il titolo di sezione è il contesto della riga
            if not fence and cc.HEADING.match(riga):
                titolo = riga
            if STORICO.search(riga) or "~~" in riga:
                continue
            for fr in _frasi(riga):
                if COND.search(fr):
                    continue
                gg = [(int(m.group(1)), int(m.group(2) or m.group(1)), m) for m in GIORNO.finditer(fr)
                      if not LOCALE.search(fr[m.start():m.end() + 20])]
                # S1 arrivo dell'orda
                ga = an.get("giorno_arrivo")
                if ga and gg and (RETHMAR.search(fr) or RETHMAR.search(titolo) or RETHMAR.search(rel)) \
                        and ARRIVO.search(fr) and (ORDA.search(fr) or ORDA.search(titolo)):
                    for lo, hi, _m in gg:
                        if lo == hi and lo >= 30 and lo != ga and not any(x[0] == ga for x in gg):
                            v("S1 arrivo dell'orda", f"Giorno {ga}", f"Giorno {lo}", p, n, riga)
                # S2 waypoint
                for nome, rx in WAYPOINT_CHIAVI.items():
                    att = an["waypoint"].get(nome)
                    if att and gg and re.search(rx, fr, re.I):
                        m0 = re.search(rx, fr, re.I)
                        vicini = [g for g in gg if abs(g[2].start() - m0.start()) < 60]
                        for lo, hi, _m in vicini[:1]:
                            if lo < att[0] - 0 or hi > att[1]:
                                v("S2 giorno del waypoint", f"{nome}: Giorno {att[0]}"
                                  + (f"-{att[1]}" if att[1] != att[0] else ""),
                                  f"Giorno {lo}" + (f"-{hi}" if hi != lo else ""), p, n, riga)
                # S3 finestre delle quest (solo ARC-09 e il quadro di campagna)
                if arco_num in ("09", None):
                    for q, rx in QUEST_CHIAVI.items():
                        att = an["quest"].get(q)
                        if not att or not gg:
                            continue
                        m0 = re.search(rx, fr, re.I)
                        if m0:
                            vicini = [g for g in gg if 0 <= g[2].start() - m0.start() < 50
                                      or 0 <= m0.start() - g[2].end() < 25]
                        elif re.search(rx, titolo, re.I) and not any(
                                re.search(r2, fr, re.I) for r2 in QUEST_CHIAVI.values()):
                            vicini = gg
                        else:
                            continue
                        for lo, hi, _m in vicini[:1]:
                            if lo >= 15 and (lo < att[0] or hi > att[1]):
                                v("S3 finestra della quest", f"{q}: Giorno {att[0]}-{att[1]}",
                                  f"Giorno {lo}" + (f"-{hi}" if hi != lo else ""), p, n, riga)
                if fence:
                    continue
                # S4 livello del party nell'arco
                att = an["livelli"].get(arco_num) if arco_num else None
                if att:
                    for rx in LIVELLO:
                        for m in rx.finditer(fr):
                            liv = int(m.group(1))
                            fino = int(m.group(2)) if m.re.groups > 1 and m.group(2) else liv
                            # un intervallo che tocca il canone non lo contraddice
                            if 5 <= liv <= 20 and (fino < att[0] or liv > att[1]):
                                v("S4 livello del party", f"{att[0]}" + (f"-{att[1]}" if att[1] != att[0] else ""),
                                  str(liv), p, n, riga)
                            break
                # S6 modifiche permanenti
                for pg, mods in an["modifiche"].items():
                    if not re.search(r"\b" + pg + r"\b", fr) or not re.search(r"permanent", fr, re.I):
                        continue
                    altri = [x for x in PG if x != pg and re.search(r"\b" + x + r"\b", fr)]
                    if altri:
                        continue
                    for seg, val, st in re.findall(r"([+−-])\s*(\d)\s*(FOR|DES|COS|INT|SAG|CAR|STR|DEX|CON|WIS|CHA)\b", fr):
                        st = STAT[st]
                        x = (-1 if seg in "−-" else 1) * int(val)
                        c = mods.get(st)
                        if c is None or (c > 0) != (x > 0) or abs(x) > abs(c):
                            v("S6 modifica permanente", f"{pg}: " + (" / ".join(f"{k} {'+' if w > 0 else '−'}{abs(w)}"
                              for k, w in mods.items()) or "nessuna"), f"{st} {'+' if x > 0 else '−'}{abs(x)}",
                              p, n, riga)
    # S5 portatore, con l'estrattore di coerenza_campagna (stesse forme)
    rac = cc.Raccolta()
    for p in files:
        cc.estrai_prosa(p, rac, {k.lower(): k for k in PG})
    for (ent, attr), valori in rac.occ.items():
        if attr != "portatore":
            continue
        nome = rac.nomi.get(ent, ent)
        att = next((pg for art, pg in an["portatori"].items() if art.lower().startswith(nome.lower()[:12])), None)
        if not att:
            continue
        for val, occ in valori.items():
            if val != att:
                for o in occ:
                    v("S5 portatore dell'artefatto", f"{nome}: {att}", val, radice / o["file"]
                      if not Path(o["file"]).is_absolute() else Path(o["file"]), o["riga"], o["testo"])
    # S7 echi armati senza sito
    if an["echi"]:
        corpus = []
        for a in archi:
            d = radice / a
            if d.is_dir():
                corpus += [q for q in d.rglob("*.md")]
        testi = {}
        for q in corpus:
            if q.name.startswith("state") or "changelog" in q.name.lower():
                continue
            try:
                testi[q] = q.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
        for e in an["echi"]:
            rx = re.compile(r"(?<![\w-])" + re.escape(e["id"]) + r"(?![\w])")
            dove = [q for q, t in testi.items() if rx.search(t)]
            if not dove:
                viol.append({"regola": "S7 eco armato senza scena", "atteso":
                             f"{e['id']} citato in almeno un file d'arco (miccia: {e['miccia']})",
                             "ha": "0 file", "file": "campaign/state.yaml", "riga": 0, "testo": ""})
    for x in viol:
        if Path(x["file"]).is_absolute():
            x["file"] = str(Path(x["file"]).relative_to(radice))
    return {"violazioni": viol, "file_letti": len(files),
            "non_verificabili": {"conoscenze senza tempo (chi sa cosa)": an.get("conoscenze_senza_tempo", 0)},
            "ancore": {k: an[k] for k in ("giorno_arrivo", "waypoint", "quest", "livelli", "portatori", "modifiche")}}


ARCHI_DEFAULT = ["07_il Portale Della Forgia Eterna", "08_La Battaglia Di Hammerfist",
                 "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist", "campaign"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--radice", type=Path, default=REPO)
    ap.add_argument("--state", type=Path)
    ap.add_argument("--ancore", type=Path, help="JSON con le àncore (replay su commit senza state.yaml)")
    ap.add_argument("--archi", nargs="+", default=ARCHI_DEFAULT)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.ancore:
        an = json.loads(a.ancore.read_text(encoding="utf-8"))
        for k in ("waypoint", "quest", "livelli", "portatori", "modifiche"):
            an.setdefault(k, {})
        an.setdefault("echi", [])
        for k in ("waypoint", "quest", "livelli"):
            an[k] = {x: tuple(y) for x, y in an[k].items()}
    else:
        an = ancore_da_state(a.state or (a.radice / "campaign" / "state.yaml"))
    r = verifica(a.radice, a.archi, an)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        for x in r["violazioni"]:
            print(f"✗ {x['regola']} · atteso {x['atteso']} · ha {x['ha']} · {x['file']}:{x['riga']}")
            if x["testo"]:
                print(f"    {x['testo'][:160]}")
        print(f"== {len(r['violazioni'])} violazioni su {r['file_letti']} file · non verificabili: "
              f"{r['non_verificabili']}")
    return 1 if r["violazioni"] else 0


if __name__ == "__main__":
    sys.exit(main())
