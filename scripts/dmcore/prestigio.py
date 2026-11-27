"""dmcore.prestigio — i requisiti delle classi di prestigio (ADR-0126, lotto 3-bis).

Una classe di prestigio si prende solo con i requisiti già in mano: quello che
conta è il personaggio **prima** del primo livello della classe. Una scheda
scrive il personaggio com'è adesso, quindi ogni giudizio qui è una condizione
necessaria:

* il bonus di attacco base richiesto si confronta con quello delle altre classi;
* i gradi richiesti non superano il massimo che i dadi vita prima dell'ingresso
  permettono, e l'abilità sta nella scheda con un bonus che li regge;
* i talenti richiesti stanno nella scheda (per nome; la parentesi non si giudica);
* razza e allineamento sono quelli scritti;
* il livello d'incantesimo richiesto lo raggiunge una delle altre classi.

I requisiti che non si riducono a un numero (speciali, divinità, lingue) non
sono nei dati: se ne conosce solo il numero, e la scheda li porta fra i non
verificabili. Qui stanno i giudizi; leggere la scheda è lavoro di
`verifica_scheda.prestigio`.
"""
from __future__ import annotations

import functools
import re

from dmcore import magia as M
from dmcore import sistemi as S

__all__ = ["avanzamento", "requisiti", "classe", "senza_parentesi", "bab_di", "giudica"]


@functools.cache
def requisiti(sistema: str = "dnd35") -> dict:
    """I requisiti del `sistema` (capacità `creature.prestigio`)."""
    return S.dati(sistema, "creature.prestigio")


def classe(nome: str, sistema: str = "dnd35") -> "dict | None":
    return requisiti(sistema)["prestigio"].get(nome.lower())


def senza_parentesi(nome: str) -> str:
    return re.sub(r"\s*\(.*$", "", nome).strip().lower()


def bab_di(gruppi: list) -> int:
    """Il bonus di attacco base che danno quei gruppi di dadi vita."""
    from dmcore import progressione
    return progressione.bab_atteso(gruppi) if gruppi else 0


def _lancia(classi: "dict[str, int]", car: "dict[str, int]", tipo: str, livello: int, sistema: str) -> bool:
    """Una delle `classi` lancia incantesimi di quel tipo e di quel livello? Conta
    anche lo slot che viene solo dagli incantesimi bonus (paladino 8 con Saggezza 14)."""
    for nome in requisiti(sistema)["tipi_di_magia"].get(tipo, ()):
        c, n = M.classe(nome, sistema), classi.get(nome, 0)
        if c is None or n < 1:
            continue
        slot = M.al_giorno(nome, n, car.get(c["caratteristica"], 99), sistema) or []
        if livello < len(slot) and sum(slot[livello]) != 0:
            return True
    return False


def giudica(req: dict, fatti: dict, sistema: str = "dnd35") -> "tuple[list[dict], list[dict]]":
    """(scarti, non verificabili) di una classe di prestigio contro i `fatti`:

    `bab_prima`      il bonus di attacco base delle altre classi, o None
    `gradi_massimi`  il massimo dei gradi con i dadi vita prima dell'ingresso
    `abilita`        {abilità: gradi che il bonus scritto regge al più}, o None se la scheda non ha la riga;
                     `incerte` sono quelle dove una penalità può nascondere dei gradi
    `talenti`        i nomi dei talenti (minuscoli, senza parentesi); `talenti_ignoti` se ce ne sono di non letti
    `razza`          il testo dove cercare la razza; `razze_it` i nomi italiani noti
    `allineamento`   la sigla, o None
    `classi`         {classe: livelli} delle altre classi, `car` i punteggi di caratteristica; `classi_ignote` se qualcuna non si conosce
    """
    scarti, nv = [], []

    def scarto(campo, scritto, atteso, nota):
        scarti.append({"campo": campo, "scritto": scritto, "atteso": atteso, "nota": nota})

    def incerto(campo, nota):
        nv.append({"campo": campo, "nota": nota})

    if "bab" in req:
        if fatti.get("bab_prima") is None:
            incerto("bab", f"serve bonus di attacco base +{req['bab']}: quello delle altre classi non si ricostruisce")
        elif fatti["bab_prima"] < req["bab"]:
            scarto("bab", fatti["bab_prima"], req["bab"],
                   f"le altre classi danno +{fatti['bab_prima']}, per entrare serve +{req['bab']}")
    for gruppo in req.get("abilita", ()):
        troppo = {a: g for a, g in gruppo["fra"].items() if g > fatti["gradi_massimi"]}
        if len(gruppo["fra"]) - len(troppo) < gruppo["quanti"]:
            a, g = sorted(troppo.items())[0]
            scarto("gradi.massimo", fatti["gradi_massimi"], g,
                   f"{a} {g} gradi: prima dell'ingresso il massimo è {fatti['gradi_massimi']}")
            continue
        scritte = fatti.get("abilita")
        if scritte is None:
            incerto("gradi", "la scheda non ha una riga delle abilità leggibile")
            continue
        basi = {}
        for nome, g in scritte.items():
            basi[senza_parentesi(nome)] = max(g, basi.get(senza_parentesi(nome), -99))
        ha = {a: basi.get(senza_parentesi(a)) for a in gruppo["fra"]}
        buone = [a for a, g in gruppo["fra"].items() if ha[a] is not None and ha[a] >= g]
        # un'abilità scritta con un bonus basso può avere gradi nascosti da una penalità; una non scritta no
        forse = [a for a in gruppo["fra"] if a not in buone and ha[a] is not None
                 and senza_parentesi(a) in fatti.get("incerte", ())]
        if len(buone) >= gruppo["quanti"]:
            continue
        mancano = sorted(a for a in gruppo["fra"] if a not in buone)
        testo = ", ".join(f"{a} {gruppo['fra'][a]}" + (" (non scritta)" if ha[a] is None else f" (il bonus ne regge {ha[a]})")
                          for a in mancano)
        if len(buone) + len(forse) >= gruppo["quanti"]:
            incerto("gradi", f"{testo}: una penalità di armatura o di taglia può nascondere i gradi")
        else:
            scarto("gradi", len(buone), gruppo["quanti"],
                   f"servono {gruppo['quanti']} fra {len(gruppo['fra'])} abilità con i gradi richiesti: {testo}")
    for gruppo in req.get("talenti", ()):
        ha = [t for t in gruppo["fra"] if senza_parentesi(t) in fatti["talenti"]]
        if len(ha) >= gruppo["quanti"]:
            continue
        mancano = ", ".join(t for t in gruppo["fra"] if t not in ha)
        if fatti.get("talenti_ignoti"):
            incerto("talenti", f"manca {mancano}, ma la scheda ha talenti che la lettura non conosce")
        else:
            scarto("talenti", len(ha), gruppo["quanti"],
                   f"servono {gruppo['quanti']} fra: {', '.join(gruppo['fra'])}; manca {mancano}"
                   if len(gruppo["fra"]) > 1 else f"manca il talento {mancano}")
    if "razza" in req:
        testo = (fatti.get("razza") or "").lower()
        nomi = [n for r in req["razza"] for n in (r, *fatti.get("razze_it", {}).get(senza_parentesi(r), ()))]
        if any(re.search(rf"\b{re.escape(senza_parentesi(n))}", testo) for n in nomi):
            pass
        elif all(senza_parentesi(r) in fatti.get("razze_it", {}) for r in req["razza"]) and testo:
            scarto("razza", "altra", ", ".join(req["razza"]), f"la classe chiede: {', '.join(req['razza'])}")
        else:
            incerto("razza", f"la classe chiede: {', '.join(req['razza'])}")
    if "allineamento" in req:
        a = fatti.get("allineamento")
        if a is None:
            incerto("allineamento", f"la classe chiede: {', '.join(req['allineamento'])}")
        elif a not in req["allineamento"]:
            scarto("allineamento", a, ", ".join(req["allineamento"]), f"la scheda è {a}")
    for i in req.get("incantesimi", ()):
        if _lancia(fatti.get("classi", {}), fatti.get("car", {}), i["tipo"], i["livello"], sistema):
            pass
        elif fatti.get("classi_ignote"):
            incerto("incantesimi", f"servono incantesimi {i['tipo']} di {i['livello']}°: "
                                   "la scheda ha classi di cui non si conosce la magia")
        else:
            scarto("incantesimi", "nessuna classe", f"{i['tipo']} {i['livello']}°",
                   f"nessuna delle altre classi lancia incantesimi {i['tipo']} di {i['livello']}°")
    if not req.get("non_verificati") and not set(req) & {"bab", "abilita", "talenti", "razza", "allineamento",
                                                         "incantesimi"}:
        incerto("speciali", "i dati non hanno nessun requisito per questa classe: va letta sul manuale")
    if req.get("non_verificati"):
        incerto("speciali", f"{req['non_verificati']} requisiti della classe non si riducono a un numero "
                            "(speciale, divinità, lingua): vanno letti sul manuale")
    return scarti, nv


def avanzamento(classe_che_lancia: str, prestigi: "list[tuple[str, int]]", altre_che_lanciano: "list[str]",
                sistema: str = "dnd35") -> "tuple[int, list[str], str | None]":
    """(livelli in più, come si arriva, dubbio) che le classi di prestigio danno
    alla lista di `classe_che_lancia`.

    `prestigi` = [(classe di prestigio, livelli)]; `altre_che_lanciano` = le altre
    classi con incantesimi che il personaggio ha. Ogni livello della classe di
    prestigio scritto in `avanza.livelli` dà +1 a una classe che si aveva già:
    a questa se il tipo combacia (arcane, divine, both, any, o il suo nome). Il
    dubbio dice perché il conto non è sicuro: avanzamenti che divergono fra due
    libri, o un'altra classe che potrebbe prenderli."""
    dati = requisiti(sistema)
    tipi = dati.get("tipi_di_magia", {})
    mio = next((k for k, v in tipi.items() if classe_che_lancia in v), None)
    piu, parti, dubbio = 0, [], None
    for nome, livelli in prestigi:
        c = classe(nome, sistema) or {}
        a = c.get("avanza")
        if not a:
            if not str(c.get("fonte", "")).startswith(("SRD", "PRD")):
                dubbio = dubbio or f"«{nome}» viene da un manuale e il plugin non ne ha l'avanzamento"
            continue
        if a.get("diverge"):
            dubbio = dubbio or f"l'avanzamento di «{nome}» diverge fra due libri"
            continue
        tipo = a["tipo"]
        if tipo not in ("any", "both", mio, classe_che_lancia):
            continue
        rivali = [x for x in altre_che_lanciano
                  if tipo == "any" or x == tipo or (tipo in tipi and x in tipi[tipo])] if tipo != "both" else \
                 [x for x in altre_che_lanciano if mio and x in tipi.get(mio, [])]
        if rivali:
            dubbio = dubbio or f"i livelli di «{nome}» possono andare anche a {', '.join(rivali)}"
        n = sum(1 for x in a["livelli"] if x <= livelli)
        piu += n
        parti.append(f"{nome} {livelli} (+{n})")
    return piu, parti, dubbio

