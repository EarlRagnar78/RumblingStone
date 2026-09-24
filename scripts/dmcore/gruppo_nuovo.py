"""Il gruppo nuovo derivato dallo stato di oggi: logica pura, senza terminale (lotto 4f-4).

Decisioni del DM che questo modulo esegue (PIANO-RIPRESA-PR-ABBANDONATE
§4.10.6, D19 e D21 del 2026-09-24):

* **nessun YAML a mano**: il DM risponde, il codice scrive;
* il template e' **derivato** dallo `state.yaml` di oggi, perche' il prodotto
  (archi, villain con le loro agende, artefatti, anagrafica PNG, numeri di
  Rethmar) resta e la partita no (ADR-0050 §7);
* cio' che e' partita per definizione si toglie senza chiedere: le conoscenze
  sul party, i portatori degli artefatti, le note d'arco che raccontano il
  giocato, gli echi, il giorno di marcia;
* cio' che chiede un giudizio arriva **una riga alla volta**, con tre scelte:
  `tieni`, `svuota`, `rivedi`. «Rivedi» diventa una voce `inferred`, lo stesso
  meccanismo che il repo usa per le domande aperte.

⚠️ **Cosa conta come traccia del primo tavolo** (misurato il 2026-09-24, G6):
i nomi dei PG presi dal `party` dello stato stesso, piu' «PG». La parola
«party» NO nelle agende: «Profile party's artifacts» e' un'agenda preparata e
vale per qualunque gruppo. Nelle conoscenze invece si': «The party visited
Hammerfist» e' una cosa successa, e quelle righe si tolgono da sole.

Il contratto verso l'esterno e' il JSON delle risposte (`completa`) e quello
delle domande (`domande_json`): il terminale li usa oggi, una pagina li potra'
usare domani senza toccare questa logica.
"""
from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from datetime import date

CLOCK_NUMERICO = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")
SEGNAPOSTO = "(da definire per il gruppo nuovo)"
NON_GIOCATO = "non giocato da questo gruppo"
SCELTE = ("tieni", "svuota", "rivedi")
MASSIMO_PG = 6
GRUPPO = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")

#: Le righe che possono chiedere un giudizio, e i campi dove si cerca la traccia.
#: Le altre sezioni si trattano senza domande (vedi `deriva`).
DA_CHIEDERE = {
    "villain": ("agenda", "trigger", "dove"),
    "difensori_rethmar": ("contingente", "condizione"),
    "waypoints": ("waypoint",),
}


class RispostaNonValida(ValueError):
    """Una risposta che non si puo' applicare: si dice quale, e non si scrive niente."""


@dataclass(frozen=True)
class Domanda:
    id: str
    sezione: str
    indice: int
    campi: "tuple[str, ...]"
    testo: "dict[str, str]" = field(hash=False, compare=False)
    scelte: "tuple[str, ...]" = SCELTE


def _tracce(stato: dict) -> "tuple[re.Pattern, re.Pattern]":
    """(nomi dei PG o «PG», parola «party»): i due metri, presi dal dato."""
    nomi = [str(p["pg"]).split()[0] for p in stato.get("party", []) if p.get("pg")]
    alternative = [re.escape(n) for n in nomi] + [r"PGs?"]
    return (re.compile(r"\b(?:" + "|".join(alternative) + r")\b"),
            re.compile(r"\bparty\b", re.I))


def _righe(stato: dict, sezione: str) -> list:
    if sezione == "waypoints":
        return stato["march_clock"]["waypoints"]
    return stato[sezione]


def _id(sezione: str, indice: int, riga: dict) -> str:
    if sezione == "villain":
        return f"villain:{riga['png_id']}"
    return f"{sezione}:{indice}"


def deriva(stato: dict) -> "tuple[dict, list[Domanda]]":
    """Lo stato del gruppo nuovo senza le risposte, e le domande una alla volta."""
    s = copy.deepcopy(stato)
    nomi, party = _tracce(stato)

    for a in s["archi"]:
        a["tempo"], a["stato"] = "preparato", "da giocare"
        if a.get("note") and nomi.search(str(a["note"])):
            a["note"] = None
    s["party"] = []
    for a in s["artefatti"]:
        a["portatore"] = "—"
        a["oggi"] = "Senza portatore: da assegnare al gruppo nuovo."
    for v in s["villain"]:
        m = CLOCK_NUMERICO.match(str(v.get("clock", "")))
        if m:
            v["clock"] = f"0/{m.group(2)}"
        v["stato"], v["tempo"] = "attivo", "preparato"
    s["conoscenze"] = [
        dict(c, tempo="preparato") for c in s["conoscenze"]
        if not (nomi.search(f"{c.get('sa_che')} {c.get('come') or ''}")
                or party.search(f"{c.get('sa_che')} {c.get('come') or ''}"))]
    for d in s["difensori_rethmar"]:
        d["tempo"] = "preparato"
    mc = s["march_clock"]
    mc["giorno_corrente"] = 1
    for w in mc["waypoints"]:
        if "✅" in str(w.get("stato")) or "SYNC POINT" in str(w.get("stato")):
            w["stato"] = "⏳ Pending"
    s["echi"] = []
    s["inferred"] = []

    domande: list[Domanda] = []
    for sezione, campi in DA_CHIEDERE.items():
        for i, riga in enumerate(_righe(s, sezione)):
            toccati = tuple(c for c in campi if riga.get(c) and nomi.search(str(riga[c])))
            if toccati:
                domande.append(Domanda(_id(sezione, i, riga), sezione, i, toccati,
                                       {c: str(riga[c]) for c in toccati}))
    return s, domande


def _dove(d: Domanda) -> str:
    """Il percorso nel dato, nella forma che `validate_state` (R2) sa seguire."""
    radice = "march_clock.waypoints" if d.sezione == "waypoints" else d.sezione
    return f"{radice}[{d.indice}].{d.campi[0]}"


def trova(stato: dict, domanda: Domanda) -> dict:
    return _righe(stato, domanda.sezione)[domanda.indice]


def _intero(valore, nome: str, minimo: int, massimo: int) -> int:
    try:
        n = int(valore)
    except (TypeError, ValueError):
        raise RispostaNonValida(f"{nome}: serve un numero, non «{valore}»") from None
    if not minimo <= n <= massimo:
        raise RispostaNonValida(f"{nome}: {n} fuori da {minimo}-{massimo}")
    return n


def _testo(valore, nome: str) -> str:
    t = str(valore or "").strip()
    if not t:
        raise RispostaNonValida(f"{nome}: vuoto")
    return t


def controlla(base: dict, domande: "list[Domanda]", risposte: dict) -> None:
    """Tutti i controlli prima di toccare qualunque cosa. `RispostaNonValida` se no."""
    gruppo = str(risposte.get("gruppo", ""))
    if not GRUPPO.match(gruppo):
        raise RispostaNonValida(f"gruppo: «{gruppo}» — minuscole, cifre e trattini "
                                "(diventa il ramo campaign-group-<gruppo>)")
    archi = [a["arco"] for a in base["archi"]]
    if risposte.get("arco_partenza") not in archi:
        raise RispostaNonValida(f"arco_partenza: «{risposte.get('arco_partenza')}» non e' "
                                "fra gli archi dello stato")
    _intero(risposte.get("livello"), "livello", 1, 20)
    pg = risposte.get("pg") or []
    if not 1 <= len(pg) <= MASSIMO_PG:
        raise RispostaNonValida(f"pg: da 1 a {MASSIMO_PG}, non {len(pg)}")
    for n, p in enumerate(pg, 1):
        for campo in ("nome", "razza", "classe"):
            _testo(p.get(campo), f"pg {n}: {campo}")
        _intero(p.get("livello"), f"pg {n}: livello", 1, 20)
        _intero(p.get("pf"), f"pg {n}: pf", 1, 999)
    ids = {d.id for d in domande}
    for chiave, scelta in (risposte.get("righe") or {}).items():
        if chiave not in ids:
            raise RispostaNonValida(f"righe: «{chiave}» non e' una delle domande")
        if scelta not in SCELTE:
            raise RispostaNonValida(f"righe: «{chiave}» = «{scelta}», le scelte sono "
                                    + ", ".join(SCELTE))


def completa(base: dict, domande: "list[Domanda]", risposte: dict,
             oggi: "str | None" = None) -> dict:
    """Lo stato del gruppo nuovo con le risposte applicate. Non scrive niente."""
    controlla(base, domande, risposte)
    s = copy.deepcopy(base)
    oggi = oggi or date.today().isoformat()
    gruppo = risposte["gruppo"]
    livello = str(int(risposte["livello"]))

    passato = True
    for a in s["archi"]:
        if a["arco"] == risposte["arco_partenza"]:
            a["tempo"], a["stato"], a["pg_livello"] = "in_corso", "in corso", livello
            a["note"] = f"sessione 0 del gruppo {gruppo}"
            passato = False
        elif passato:
            a["stato"] = NON_GIOCATO

    s["party"] = [{
        "pg": p["nome"].strip(),
        "classe": f"{p['classe'].strip()} {int(p['livello'])} ({p['razza'].strip()})",
        "oggi": f"Sessione 0 del gruppo {gruppo}.",
        "hp": str(int(p["pf"])),
        "stato": "attivo",
    } for p in risposte["pg"]]

    scelte = risposte.get("righe") or {}
    for d in domande:
        riga = trova(s, d)
        # Senza risposta vale «rivedi»: niente passa in silenzio e niente si
        # cancella in silenzio, che sono i due modi di sbagliare qui.
        scelta = scelte.get(d.id, "rivedi")
        if scelta == "svuota":
            for c in d.campi:
                riga[c] = SEGNAPOSTO
        elif scelta == "rivedi":
            estratto = " · ".join(d.testo[c] for c in d.campi)[:160]
            s["inferred"].append({
                "id": f"INF-{len(s['inferred']) + 1:03d}",
                "dove": _dove(d),
                "domanda": (f"«{estratto}» porta tracce del primo tavolo: vale per il "
                            "gruppo nuovo, va riscritta, o si toglie?"),
                "a_chi": "DM",
                "aperto_dal": oggi,
                "fonte": "dm.py gruppo nuovo",
            })
    return s


def domande_json(base: dict, domande: "list[Domanda]") -> dict:
    """Il modulo come dato: cosa chiedere e con quali scelte, per chi lo disegna."""
    return {
        "campi": {
            "gruppo": {"tipo": "testo", "formato": GRUPPO.pattern,
                       "nota": "diventa il ramo campaign-group-<gruppo>"},
            "arco_partenza": {"tipo": "scelta", "scelte": [a["arco"] for a in base["archi"]]},
            "livello": {"tipo": "intero", "minimo": 1, "massimo": 20},
            "pg": {"tipo": "elenco", "minimo": 1, "massimo": MASSIMO_PG,
                   "campi": {"nome": "testo", "razza": "testo", "classe": "testo",
                             "livello": "intero 1-20", "pf": "intero 1-999"}},
        },
        "righe": [{"id": d.id, "sezione": d.sezione, "campi": list(d.campi),
                   "testo": d.testo, "scelte": list(d.scelte), "predefinita": "rivedi"}
                  for d in domande],
    }
