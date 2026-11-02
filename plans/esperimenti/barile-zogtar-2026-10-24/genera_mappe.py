#!/usr/bin/env python3
"""Rifà i contratti JSON di M7-C (lo spiazzo del capo) e M7-H (il campo attorno).

Il DM, 2026-10-24, in due tempi. Prima: la tenda e il campo devono essere
coerenti, senza tende attaccate a quella di Zog'tar. Poi: niente steccato,
sono barbari, orchi e hobgoblin; il modello è il campo di un capo nomade, il
khalasar di un khal, l'ordo di un khan, il campo di una banda gota.

- M7-C resta la mappa dello scontro e tiene la tenda dov'era (stesse coordinate
  di tutte le scene). Attorno c'è lo spiazzo del capo, terra battuta senza
  recinto: il fuoco del consiglio ridotto a brace davanti alla soglia, i pali
  dei trofei, il bottino ammucchiato, e sul bordo un anello largo di tende dei
  servi, staccate l'una dall'altra; la tenda del turno dopo resta a X4-Y5.
- M7-H è il campo attorno, 66 × 60 m: oltre lo spiazzo, a 20-30 m dal telo, le
  lance della Guardia della Mano, quattro tende attorno a un fuoco, a gruppi
  staccati; a ovest i clan degli orchi coi ripari storti; vie battute che
  partono a raggiera dallo spiazzo, niente file diritte.

Lo script parte dal contratto di M7-C com'è su disco ed è idempotente: toglie
quello che ha messo lui (o lo steccato della PR #261) e lo rimette.

Uso (dalla radice del repo):
    python3 plans/esperimenti/barile-zogtar-2026-10-24/genera_mappe.py
    python3 scripts/compile_map_json.py <json> -o <md>   # per ciascuna mappa
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
MAPPE = RADICE / "07_il Portale Della Forgia Eterna" / "Mappe"
M7C = MAPPE / "ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.json"
M7H = MAPPE / "ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.json"

LARGH, ALT = 27, 23          # M7-C: lo spiazzo del capo
DX, DY = 8, 8                # dove sta M7-C dentro M7-H
H_LARGH, H_ALT = 44, 40      # M7-H

LUCE = "Luce: intensa entro 6 m, fioca fino a 12 m, come una torcia dell'SRD"
SUPPLEMENTO = "il supplemento «Il barile sulla tenda»"

# Le tende dei servi, sul bordo dello spiazzo: staccate, a 7,5-12 m dal telo.
TENDE_SERVI = [[1, 1, 2, 2], [6, 0, 2, 2], [19, 0, 2, 2], [24, 7, 2, 2], [24, 15, 2, 2],
               [21, 20, 2, 2], [9, 21, 2, 2], [3, 19, 2, 2], [0, 14, 2, 2], [0, 5, 2, 2]]


def e_della_tenda(s: dict) -> bool:
    """I pezzi della tenda del comando, che non si toccano."""
    if s["type"] != "🎪":
        return True
    return "line" in s or "Telo" in s.get("label", "")


def rifai_m7c(d: dict) -> dict:
    d = copy.deepcopy(d)
    interno = next(r for r in d["regions"] if r["terrain"] == "⬜")
    d["regions"] = [
        {"terrain": "🟫", "rect": [6, 2, 15, 19],
         "label": "Lo spiazzo del capo: terra battuta dagli zoccoli e dai piedi, senza recinto"},
        {"terrain": "🟫", "rect": [4, 4, 19, 15]},
        {"terrain": "🟫", "rect": [2, 7, 23, 9]},
        {"terrain": "🟫", "rect": [12, 0, 3, 2], "label": "La via battuta verso la fortezza"},
        {"terrain": "🟫", "rect": [13, 21, 3, 2], "label": "La via battuta verso le colline"},
        {"terrain": "🟫", "rect": [25, 10, 2, 3], "label": "La via battuta verso est"},
        {"terrain": "🟫", "rect": [0, 10, 2, 3], "label": "La via battuta verso i clan degli orchi"},
        interno,
    ]
    tenuti = [s for s in d["structures"]
              if s["type"] not in ("🧱", "🗿", "📦") and e_della_tenda(s)]
    servi = [{"type": "🎪", "rect": r} for r in TENDE_SERVI]
    servi[0]["label"] = "Tende dei servi e del bottino del capo: dentro non ci sono soldati"
    d["structures"] = tenuti + servi + [
        {"type": "🎪", "rect": [23, 3, 2, 2], "label": "Tenda del turno dopo"},
        {"type": "🗿", "at": [10, 5],
         "label": "Palo dei trofei: teschi di nani, code di lupo, lo stendardo della Mano Rossa"},
        {"type": "🗿", "at": [16, 5], "label": "Palo dei trofei"},
        {"type": "📦", "at": [5, 7],
         "label": "Il bottino della valle, ammucchiato davanti al capo perché i capiclan lo vedano"},
    ]
    hz = [h for h in d["hazards"]
          if h["type"] != "🔥" or h.get("label") == "Falò della guardia"]
    hz[1:1] = [
        {"type": "🔥", "at": [13, 4], "label": "Il fuoco del consiglio",
         "effect": "davanti alla soglia, dove il capo parla ai capiclan; a notte fonda è brace: "
                   "chi entra nella cella prende 1d6 da fuoco, la luce è fioca e solo entro 3 m"},
        {"type": "🔥", "at": [3, 11], "label": "Fuoco delle sentinelle ovest",
         "effect": f"due sentinelle sulla via battuta: chi entra nella cella prende 1d6 da fuoco. {LUCE}"},
        {"type": "🔥", "at": [23, 11], "label": "Fuoco delle sentinelle est",
         "effect": f"due sentinelle sulla via battuta: chi entra nella cella prende 1d6 da fuoco. {LUCE}"},
    ]
    d["hazards"] = hz
    for m in d["movements"]:
        if m["name"].startswith("Le due guardie del turno dopo"):
            m["path"] = [[23, 5], [20, 16], [14, 15]]
    sost = [
        ("nella loro tenda, V11–W12", "nella loro tenda, X4–Y5, a 9 m dal telo"),
        ("passano lo steccato, fanno quadrato nella piazza attorno al telo",
         "entrano nello spiazzo, fanno quadrato attorno al telo"),
        ("Le frecce dei varchi sono una proposta", "Le frecce delle vie battute sono una proposta"),
    ]
    tt = []
    for t in d["tattiche"]:
        for a, b in sost:
            t = t.replace(a, b)
        tt.append(t)
    d["tattiche"] = tt
    d["notes"] = [n for n in d["notes"] if not n.startswith("Com'è fatto il campo")]
    d["notes"].append(
        "Com'è fatto il campo qui attorno: come il campo di un capo nomade, senza recinto. La tenda "
        "sta sola in mezzo allo spiazzo del capo, terra battuta larga una quarantina di metri; davanti "
        "alla soglia il fuoco del consiglio, ridotto a brace, e i due pali dei trofei. Sul bordo, "
        "staccate l'una dall'altra, le tende dei servi e del bottino, senza soldati, e quella del "
        "turno dopo, a 9 m dal telo. Le lance della Guardia della Mano dormono più in là, a 20-30 m, "
        "attorno ai loro fuochi, e i clan degli orchi a ovest: sono su M7-H.")
    d["evoluzione"] = [e for e in d["evoluzione"] if not e["stato"].startswith("I ·")]
    d["evoluzione"].append({
        "stato": "I · il barile",
        "trigger": "i PG lasciano cadere dall'alto il barile d'olio con le fiale della fenice",
        "griglia": "dove cade (1d8 per la direzione, 1d4−1 quadretti dalla verticale): l'olio "
                   "copre tutto il pavimento della tenda, il telo si squarcia; se prende un palo o "
                   "il colmo (riga 12) la tenda crolla subito",
        "effetto": "oggetto in caduta 15d6 su chi sta nella casella; due palle di fuoco da 6d6 "
                   f"(Riflessi CD 14); olio in fiamme, fumo, crollo: le regole sono in {SUPPLEMENTO}"})
    return d


def sposta(p: list[int]) -> list[int]:
    return [p[0] + DX, p[1] + DY]


def sposta_voce(v: dict) -> dict:
    v = copy.deepcopy(v)
    if "at" in v:
        v["at"] = sposta(v["at"])
    if "rect" in v:
        v["rect"] = sposta(v["rect"][:2]) + v["rect"][2:]
    if "line" in v:
        v["line"] = [sposta(p) for p in v["line"]]
    if "area" in v and "rect" in v["area"]:
        v["area"]["rect"] = sposta(v["area"]["rect"][:2]) + v["area"]["rect"][2:]
    if "path" in v:
        v["path"] = [sposta(p) for p in v["path"]]
    return v


# Le lance della Guardia della Mano: quattro tende da otto attorno al fuoco della
# lancia, a gruppi staccati, sul bordo dello spiazzo. Ogni gruppo è (cx, cy, lati),
# dove i lati dicono quali delle quattro tende ci sono (o, e, n, s).
LANCE = [
    (13, 4, "oen"), (29, 4, "oen"), (39, 4, "oen"),
    (39, 12, "oens"), (39, 26, "oens"),
    (13, 35, "oes"), (30, 35, "oes"), (39, 36, "n"),
]
VIE = (range(19, 24), range(17, 22))  # colonne della via nord/sud, righe della via est/ovest


def lance_hobgoblin() -> tuple[list[dict], list[dict]]:
    """Tende 3 × 3 m attorno al fuoco della lancia, con 3 m di vuoto fra il fuoco e il telo."""
    tende, fuochi = [], []
    for i, (cx, cy, lati) in enumerate(LANCE):
        pos = {"o": (cx - 4, cy - 1), "e": (cx + 3, cy - 1), "n": (cx - 1, cy - 4), "s": (cx - 1, cy + 3)}
        for lato in lati:
            x, y = pos[lato]
            tende.append({"type": "🎪", "rect": [x, y, 2, 2]})
        fuochi.append({"type": "🔥", "at": [cx, cy], "label": "Fuoco della lancia" if i else
                       "Fuoco della lancia della Guardia della Mano",
                       "effect": f"attorno dormono otto hobgoblin per tenda: chi entra nella cella prende "
                                 f"1d6 da fuoco. {LUCE}"})
    tende[0]["label"] = "Tende della Guardia della Mano, otto hobgoblin per tenda, a gruppi attorno al fuoco"
    return tende, fuochi


def clan_orchi() -> tuple[list[dict], list[dict]]:
    """Quattro bande d'orchi a ovest: ripari storti attorno al fuoco, vuoto fra un clan e l'altro."""
    ripari, fuochi = [], []
    clan = [
        ("Fuoco della banda della Zanna", (3, 3), [(0, 1, 2, 1), (5, 0, 1, 2), (1, 5, 2, 1), (5, 5, 1, 1)]),
        ("Fuoco della banda del Corvo", (3, 12), [(0, 10, 1, 2), (2, 9, 2, 1), (5, 11, 1, 2), (1, 15, 2, 1)]),
        ("Fuoco della banda dell'Ascia Rotta", (3, 25), [(0, 23, 2, 1), (5, 22, 1, 2), (0, 27, 1, 2), (4, 28, 2, 1)]),
        ("Fuoco della banda dei Teschi", (3, 35), [(0, 33, 2, 1), (5, 34, 1, 2), (1, 38, 2, 1), (4, 37, 1, 2)]),
    ]
    for i, (nome, (fx, fy), rs) in enumerate(clan):
        fuochi.append({"type": "🔥", "at": [fx, fy], "label": nome,
                       "effect": "il fuoco comune di una banda d'orchi: chi entra nella cella prende "
                                 "1d6 da fuoco. Luce: intensa entro 6 m, fioca fino a 12 m. Attorno "
                                 "dormono una ventina d'orchi e lo sciamano della banda"})
        for j, (x, y, w, h) in enumerate(rs):
            v = {"type": "🎪", "rect": [x, y, w, h]}
            ripari.append(v)
    return ripari, fuochi


def costruisci_m7h(c: dict) -> dict:
    h = {
        "schema_version": "1.0",
        "title": "M7-H — Il campo del capo: lo spiazzo, la Guardia della Mano e i clan (notte, ≈372 DR)",
        "scale_m_per_square": 1.5,
        "map_size": [H_LARGH, H_ALT],
        "base_terrain": "🟩",
        "north": "N",
        "tipo": "tattica",
        "ambiente": "esterno",
        "luogo": c["luogo"],
        "quota": c["quota"],
        "dislivello": c["dislivello"],
    }
    regioni = [sposta_voce(r) for r in c["regions"] if "label" not in r or "via battuta" not in r["label"]]
    regioni += [
        {"terrain": "🟫", "rect": [20, 0, 3, 8], "label": "La via battuta verso la fortezza"},
        {"terrain": "🟫", "rect": [21, 31, 3, 9], "label": "La via battuta verso le colline"},
        {"terrain": "🟫", "rect": [35, 18, 9, 3], "label": "La via battuta verso est"},
        {"terrain": "🟫", "rect": [0, 18, 8, 3], "label": "La via battuta fra i clan degli orchi"},
    ]
    h["regions"] = regioni
    tende, fuochi_lance = lance_hobgoblin()
    ripari, fuochi_clan = clan_orchi()
    h["structures"] = [sposta_voce(s) for s in c["structures"]] + tende + ripari + [
        {"type": "🐴", "at": [18, 38], "label": "I lupi da guerra della Guardia, legati ai picchetti"},
        {"type": "📦", "at": [25, 1], "label": "Carri del bottino, senza buoi, lasciati dove si sono fermati"},
        {"type": "📦", "at": [26, 1]},
        {"type": "🗿", "at": [5, 17], "label": "Il palo degli sciamani degli orchi"},
    ]
    h["hazards"] = [sposta_voce(z) for z in c["hazards"] if z["type"] in ("🔥", "🏮", "🟪")] \
        + fuochi_lance + fuochi_clan
    unita = [sposta_voce(u) for u in c["units"] if not u["name"].startswith("I quattro PG")]
    unita.insert(0, {"faction": "PG", "name": "I PG in volo, invisibili, a 48 m sopra la tenda",
                     "token": "🔵", "at": [22, 18], "quantity": 4})
    unita += [
        {"faction": "Orda", "name": "Una lancia della Guardia della Mano, otto per tenda", "token": "🔴",
         "at": [29, 6], "quantity": 24, "cr": "Guerriero 4"},
        {"faction": "Orda", "name": "Una lancia della Guardia della Mano", "token": "🔴",
         "at": [30, 33], "quantity": 24, "cr": "Guerriero 4"},
        {"faction": "Orda", "name": "Banda d'orchi del Corvo, attorno al fuoco", "token": "🔴",
         "at": [2, 13], "quantity": 20, "cr": "GS ½"},
        {"faction": "Orda", "name": "Le sentinelle della via est", "token": "🔴",
         "at": [37, 20], "quantity": 2, "cr": "Guerriero 4"},
    ]
    h["units"] = unita
    h["movements"] = [
        {"name": "Le ronde di orchi dalla via ovest (1d4+2 round)", "path": [[0, 19], [8, 19]], "color": "#e85d04"},
        {"name": "Le lance della Guardia dalla via sud (2d4+2 round)", "path": [[22, 39], [22, 31]], "color": "#9d0208"},
        {"name": "Le lance della Guardia dalla via nord (2d4+2 round)", "path": [[21, 0], [21, 8]], "color": "#9d0208"},
        {"name": "Le sentinelle della via est", "path": [[37, 19], [34, 19]], "color": "#d62828"},
        {"name": "Le due guardie del turno dopo", "path": [[31, 13], [28, 24], [22, 23]], "color": "#7b2cbf"},
    ]
    h["notes"] = [
        "M7-H è M7-C con il campo attorno: lo spiazzo è lo stesso e le sue coordinate sono quelle "
        "di M7-C spostate di otto colonne e otto righe (la N12 di M7-C qui è V20).",
        "Il modello è il campo di un capo nomade, non il castrum romano: niente recinto e niente file "
        "diritte. La tenda del capo sta sola in mezzo allo spiazzo; attorno, a 20-30 m, le lance "
        "della Guardia della Mano, quattro tende da otto attorno al fuoco della lancia, a gruppi "
        "staccati; a ovest i clan degli orchi, ripari storti attorno al fuoco della banda, con il "
        "vuoto fra un clan e l'altro. Le vie sono solo terra battuta, a raggiera dallo spiazzo.",
        "Le misure: tende da otto di 3 × 3 m, 3 m di vuoto fra il fuoco e il telo, almeno 4,5 m fra "
        "un gruppo e l'altro (plans/esperimenti/mappe-campo-2026-10-21/RICERCA-ACCAMPAMENTI.md, la "
        "parte sui campi mongoli e d'avventura).",
        f"Il barile: i PG volano a 48 m, invisibili. La deviazione, la caduta, l'olio e il fuoco sono in "
        f"{SUPPLEMENTO}. All'aperto le palle di fuoco arrivano a 6 m dall'impatto e l'olio a 7: "
        "nessuna tenda della Guardia è così vicina al telo del comando.",
    ]
    h["tattiche"] = [
        "**Il campo si sveglia** (Scena 8): il boato si sente in tutto il campo. Le sentinelle dei "
        "fuochi gridano e restano al loro posto; le ronde d'orchi arrivano dalla via ovest in 1d4+2 "
        "round, le lance della Guardia dalle vie nord e sud in 2d4+2, il tempo di svegliarsi e "
        "armarsi. Finché Zog'tar è in piedi non vanno addosso alla tenda: fanno quadrato nello "
        "spiazzo, a una decina di metri dal telo, e portano acqua e pelli bagnate.",
        "**Chi guarda in alto**: nessuno, al primo round. Dal secondo gli sciamani dei clan cercano "
        "chi ha lanciato, e chi ha *vedere invisibilità* guarda il cielo; a 48 m la scurovisione "
        "(18 m) non arriva, e le stelle non bastano per vedere un invisibile che non si muove.",
    ]
    h["evoluzione"] = [
        {"stato": "I · il barile", "trigger": "il barile cade sulla tenda",
         "griglia": "la tenda brucia; lo spiazzo attorno resta sgombro",
         "effetto": "allarme in tutto il campo; i rinforzi arrivano per le vie battute"},
        {"stato": "J · i barilotti", "trigger": "i PG lasciano cadere uno dei barilotti da 10 litri",
         "griglia": "l'olio copre i quadretti entro 3 m da dove cade",
         "effetto": "su una via dove si ammassano i rinforzi, su una lancia che si sveglia, o sulla "
                    f"tenda del turno dopo: le regole sono in {SUPPLEMENTO}"},
    ]
    h["note_dm"] = [
        "**Il campo qui misura 66 × 60 m**: lo spiazzo del capo, con attorno la Guardia della Mano e "
        "i primi clan. Oltre il bordo il campo continua per mezzo chilometro in ogni direzione (M7-A)."]
    h["taglie"] = [{"at": sposta(t["at"]), "taglia": t["taglia"]} for t in c.get("taglie", [])]
    return h


def main() -> None:
    c = json.loads(M7C.read_text(encoding="utf-8"))
    nuovo = rifai_m7c(c)
    M7C.write_text(json.dumps(nuovo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    M7H.write_text(json.dumps(costruisci_m7h(nuovo), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("scritti", M7C.name, M7H.name)


if __name__ == "__main__":
    main()
