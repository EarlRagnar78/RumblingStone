"""gs.py — il grado di sfida che le regole danno a una scheda (ADR-0126, lotto 5).

Il conto è puro: riceve i livelli di classe, i dadi vita razziali, la creatura
base se c'è, e la tabella `[gs]` della capacità `creature.costruzione` del
sistema. Tre casi, ognuno con la sua regola:

* **solo livelli di classe** (dadi vita razziali 0): livello più lo scarto del
  sistema per classi da PG o da PNG, con le eccezioni di razza che la fonte
  scrive (drow e duergar +1 con classi da PG nell'SRD 3.5); sotto 1 si scende
  per gradini (1/2, 1/3, …). Classi da PG e da PNG mescolate non hanno una
  regola scritta: non verificabile;
* **creatura base più livelli**: una forbice. Ogni livello associato vale +1,
  ogni livello non associato +1/2 finché i livelli non pareggiano i dadi vita
  d'origine. Quali livelli sono associati lo decide chi costruisce, quindi il
  grado scritto è legale se sta fra tutti-non-associati e tutti-associati;
* **creatura base senza livelli**: il grado della base.

Un modello (mezzo-immondo, scheletro…), l'avanzamento per dadi vita o una
cavalcatura nel blocco rendono il grado non ricostruibile da qui: lo dice
`perche` e chi chiama lo mette fra i non verificabili.
"""
from __future__ import annotations

import math
import re
from fractions import Fraction


def frazione(testo) -> "Fraction | None":
    """«1/2», «0,5», 7.0 → Fraction; None se non è un numero."""
    if testo is None:
        return None
    t = str(testo).strip().replace(",", ".")
    try:
        return Fraction(t).limit_denominator(8)
    except (ValueError, ZeroDivisionError):
        return None


def scritto(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def _gradino(valore: int, gradini: "list[str]") -> "Fraction | None":
    """Un grado intero sotto 1 scende di gradino: 0 → 1/2, −1 → 1/3…"""
    if valore >= 1:
        return Fraction(valore)
    i = -valore
    return Fraction(gradini[i]) if i < len(gradini) else None


def razza(dove: str, tabella: dict) -> "tuple[str, dict] | None":
    """La razza con un'eccezione scritta, cercata nel tipo e nel nome della scheda."""
    for nome, voce in (tabella.get("razze") or {}).items():
        if any(re.search(rf"\b{re.escape(n)}\b", dove, re.I) for n in voce.get("nomi", [nome])):
            return nome, voce
    return None


def modello(dove: str, tabella: dict) -> "str | None":
    """La parola che dichiara un modello, un avanzamento o una cavalcatura, o None."""
    for espr in tabella.get("modelli", []):
        m = re.search(espr, dove, re.I)
        if m:
            return m.group(0)
    return None


def modello_noto(dove: str, tabella: dict) -> "tuple[str, dict, str] | None":
    """(nome, voce, testo senza il modello) se `dove` dichiara un solo modello di `[modelli_gs]`
    e nient'altro che cambi il grado di sfida (avanzamento, cavalcatura, un secondo modello)."""
    dati = tabella.get("modelli_gs") or {}
    resto, trovati = dove, []
    for nome in dati.get("ordine", []):
        for espr in dati[nome]["nomi"]:
            if re.search(espr, resto, re.I):
                resto = re.sub(espr, " ", resto, flags=re.I)
                trovati.append(nome)
                break
    for parola in dati.get("neutri", []):
        resto = re.sub(parola, " ", resto, flags=re.I)
    if len(trovati) != 1 or modello(resto, tabella):
        return None
    return trovati[0], dati[trovati[0]], resto


def naturale_col_modello(regola: dict, taglia: "str | None", base: "int | None") -> "dict | None":
    """L'armatura naturale che un modello dà (`naturale` in `[modelli_gs]`): {"esatto": n} se la base
    è nota o non serve, {"minimo": n} se la base non si conosce, None se manca la taglia che serve."""
    if "taglia" in regola:                      # scheletro: il numero sostituisce quello della base
        return {"esatto": regola["taglia"][taglia]} if taglia in regola["taglia"] else None
    if "piu_taglia" in regola:                  # zombi: sopra la base, per taglia
        if taglia not in regola["piu_taglia"]:
            return None
        piu = regola["piu_taglia"][taglia]
    else:
        piu = regola.get("piu", 0)
    if "almeno" in regola:                      # lich: +5 o la base, se è più alta
        return {"esatto": max(base, regola["almeno"])} if base is not None else {"minimo": regola["almeno"]}
    return {"esatto": base + piu} if base is not None else {"minimo": piu}


def caratteristiche_col_modello(regola: dict, base: "dict | None") -> "dict[str, dict]":
    """Le caratteristiche che un modello dà (`caratteristiche` in `[modelli_gs]`), una voce per punteggio:
    {"senza": True} se il modello lo toglie, {"esatto": n} se lo fissa, {"minimo": n} se sta sopra la base
    nota (i dadi vita in più e gli oggetti possono solo alzarlo) o sopra un minimo del modello.
    Senza la `base` restano solo i punteggi tolti, fissati e i minimi."""
    esito: "dict[str, dict]" = {}
    for car in regola.get("senza", []):
        esito[car] = {"senza": True}
    for car, n in (regola.get("fisse") or {}).items():
        esito[car] = {"esatto": n}
    for car, n in (regola.get("almeno") or {}).items():
        esito[car] = {"minimo": max(n, (base or {}).get(car, n))}
    if base:
        for car, piu in (regola.get("piu") or {}).items():
            if car not in esito and car in base:
                esito[car] = {"minimo": base[car] + piu}
    return esito


def _col_modello(noto: "tuple[str, dict, str]", livelli: "dict[str, int]", dv_razziali: int, base: "dict | None",
                 tabella: dict, dichiarata: bool, stessa_taglia: "bool | None") -> dict:
    """Il grado di sfida con un modello dell'SRD: per dadi vita (scheletro, zombi) o base più aumento."""
    nome, voce, resto = noto
    tot = sum(livelli.values())
    if "per_dv" in voce:
        if tot or not dv_razziali:
            return {"perche": f"«{nome}»: il grado viene dai dadi vita, e la scheda ha livelli di classe o non scrive i dadi"}
        g = next((frazione(grado) for fino, grado in voce["per_dv"] if dv_razziali <= fino), None)
        if g is None:
            return {"perche": f"«{nome}» con {dv_razziali} dadi vita: fuori dalla tabella del modello"}
        return {"min": g, "max": g, "regola": "gs.modello.dv", "conto": f"{nome} con {dv_razziali} dadi vita"}
    senza = atteso(livelli, dv_razziali, base, resto, tabella, dichiarata, stessa_taglia)
    if "perche" in senza:
        return senza
    dv = dv_razziali + tot
    piu = voce["piu"] if "piu" in voce else next(a for fino, a in voce["soglie"] if dv <= fino)
    basso, alto = (max(x + piu, Fraction(voce.get("minimo", 0))) for x in (senza["min"], senza["max"]))
    return {"min": basso, "max": alto, "regola": "gs.modello",
            "conto": f"{senza['conto']}; {nome} {piu:+d} con {dv} dadi vita"}


def atteso(livelli: "dict[str, int]", dv_razziali: int, base: "dict | None", dove: str,
           tabella: dict, dichiarata: bool = False, stessa_taglia: "bool | None" = None) -> dict:
    """{"min", "max", "regola", "conto"} oppure {"perche": …} se non si ricostruisce.

    `livelli` ha i nomi inglesi delle classi; `base` è la voce di `creature.base`
    (serve `gs` e `dv`) o None; `dove` è il testo (tipo, titolo) in cui cercare
    razza e modelli. `dichiarata`: la scheda dichiara la base (fonte, o colore ed età di un
    drago), non la si è solo trovata per nome: solo allora i dadi vita in più sono un
    avanzamento della stessa creatura. `stessa_taglia`: la taglia è quella della base.
    """
    m = modello(dove, tabella)
    if m:
        noto = modello_noto(dove, tabella)
        if noto is None:
            return {"perche": f"«{m}» nel tipo o nel titolo: modello, avanzamento o cavalcatura cambiano il grado di sfida"}
        return _col_modello(noto, livelli, dv_razziali, base, tabella, dichiarata, stessa_taglia)
    png = set(tabella.get("classi_png", []))
    l_png = sum(n for c, n in livelli.items() if c in png)
    l_pg = sum(n for c, n in livelli.items() if c not in png)
    tot = l_png + l_pg
    if dv_razziali <= 1 and base is None:
        if not tot:
            return {"perche": "né livelli di classe né creatura base: il grado di sfida non ha un conto"}
        if l_pg and l_png:
            return {"perche": "classi da PG e da PNG insieme: la fonte non scrive come si sommano"}
        fuori = next((n for n in tabella.get("fuori_fonte", []) if re.search(rf"\b{n}\b", dove, re.I)), None)
        if fuori:
            return {"perche": f"«{fuori}»: razza fuori dalla fonte, la sua regola del grado di sfida non è nei dati"}
        if not any(re.search(rf"\b{n}\b", dove, re.I) for n in tabella.get("razze_fonte", [])):
            return {"perche": "razza non riconosciuta fra quelle da un dado vita della fonte: il grado di sfida non si ricostruisce"}
        r = razza(dove, tabella)
        chiave = "pg" if l_pg else "png"
        scarto = (r[1] if r else {}).get(chiave, tabella[chiave])
        g = _gradino(tot + scarto, tabella["gradini"])
        if g is None:
            return {"perche": "il conto scende sotto l'ultimo gradino della tabella"}
        di_chi = f" ({r[0]})" if r and chiave in r[1] else ""
        return {"min": g, "max": g, "regola": f"gs.classi.{chiave}",
                "conto": f"{tot} livelli da {'PG' if l_pg else 'PNG'} {scarto:+d}{di_chi}"}
    if base is None or base.get("gs") is None:
        return {"perche": "dadi vita razziali senza una creatura base riconosciuta: manca il grado di partenza"}
    gs_base = frazione(base["gs"])
    if gs_base is None:
        return {"perche": f"grado di sfida della base illeggibile ({base['gs']})"}
    if isinstance(base.get("dv"), int) and dv_razziali and dv_razziali != base["dv"]:
        ogni = (tabella.get("avanzamento") or {}).get(base.get("tipo", ""))
        if not (dichiarata and ogni and dv_razziali > base["dv"] and not tot):
            return {"perche": f"{dv_razziali} dadi vita razziali contro i {base['dv']} della base: avanzata per dadi vita"}
        # SRD, «Table: Improved Monster CR Increase»: +1 ogni `ogni` dadi vita aggiunti; +1 se cresce di taglia
        in_piu = dv_razziali - base["dv"]
        basso = gs_base + in_piu // ogni
        return {"min": basso, "max": basso + (0 if stessa_taglia else 1), "regola": "gs.base.avanzata",
                "conto": f"base {scritto(gs_base)} con {base['dv']} DV, {in_piu} dadi vita in più: +1 ogni {ogni}"
                         + ("" if stessa_taglia else ", +1 se è cresciuta di taglia")}
    if not tot:
        return {"min": gs_base, "max": gs_base, "regola": "gs.base", "conto": f"la base ha {scritto(gs_base)}"}
    dv = base["dv"] if isinstance(base.get("dv"), int) else dv_razziali
    passo = Fraction(str(tabella.get("non_associato", 0.5)))
    # livelli da PNG sempre non associati; quelli da PG fra tutti non associati e tutti associati
    def non_assoc(n: int) -> Fraction:
        return passo * min(n, dv) + max(0, n - dv)
    basso = gs_base + non_assoc(tot)
    alto = gs_base + l_pg + non_assoc(l_png)
    return {"min": Fraction(math.floor(basso)), "max": max(alto, Fraction(math.floor(basso))),
            "regola": "gs.base.classi",
            "conto": f"base {scritto(gs_base)} con {dv} DV, {tot} livelli: da tutti non associati a tutti associati"}
