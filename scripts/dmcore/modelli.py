"""dmcore/modelli.py — i modelli semplici di PF1e su un blocco finito (lotto J).

Un modello semplice («simple template» del Bestiary di PF1e) è una manciata di
modificatori applicati a una creatura già costruita. I numeri stanno nel plugin
(`sistemi/pf1e/dati/modelli.toml`, con la fonte per riga); qui c'è solo il conto,
fatto con le regole di ricostruzione («Rebuild Rules») e non con quelle rapide.

Due funzioni: `applica` cambia il blocco e restituisce la traccia di ciò che ha
fatto; `disfa` rifà il conto al contrario con quella traccia e riporta il blocco
a com'era. Il grado di sfida scritto nel blocco non cambia mai: il modello dice
in una voce quanto vale davvero.

Limiti dichiarati: il tetto di Destrezza dell'armatura non si ricalcola; i dadi
di danno seguono la tabella delle armi, e un dado che la tabella non ha resta
com'è e finisce nella traccia; gli archetipi di classe non sono modelli e qui
non entrano.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from fractions import Fraction

from . import sistemi as S
from . import statblock as SB
from . import tabelle as T

#: le taglie nell'ordine della tabella, col nome che il generatore scrive
ORDINE = ("fine", "diminutive", "tiny", "small", "medium", "large", "huge",
          "gargantuan", "colossal")
_TS = (("Temp", "Cos"), ("Rifl", "Des"), ("Vol", "Sag"))
_DADO = re.compile(r"^(\d+d\d+|\d+)([+-]\d+)?(.*)$")
_PF_DADO = re.compile(r"(\d+)d(\d+)([+-]\d+)?")


class ModelloVietato(ValueError):
    """Il modello non si applica a questa creatura (taglia o tipo esclusi)."""


@dataclass
class Traccia:
    """Che cosa un modello ha fatto a un blocco: basta a disfarlo."""
    modello: str
    gs_reale: str = ""
    caratteristiche: dict[str, int] = field(default_factory=dict)
    naturale: int = 0
    taglia: int = 0
    dadi: list[tuple[str, str]] = field(default_factory=list)
    dadi_fermi: list[str] = field(default_factory=list)
    compositi: list[bool] = field(default_factory=list)
    ca_dettaglio_prima: str = ""
    voci: list[str] = field(default_factory=list)
    sensi_aggiunti: str = ""
    righe: list[str] = field(default_factory=list)


def dati() -> dict:
    return S.dati("pf1e", "creature.costruzione")


def nomi() -> list[str]:
    return sorted(dati()["modelli"])


def modello(nome: str) -> dict:
    tutti = dati()["modelli"]
    chiave = nome.strip().lower()
    for k, v in tutti.items():
        if chiave in (k, v["nome"].lower()):
            return {"chiave": k, **v}
    raise KeyError(f"modello ignoto: {nome}. Noti: {', '.join(nomi())}")


# ── leggere e scrivere i pezzi del blocco ───────────────────────────────────
def _mod(punteggio: int) -> int:
    return T.mod(punteggio)                # la formula sta nei dati del plugin


def leggi_attributi(testo: str) -> dict[str, int | str]:
    attr: dict[str, int | str] = {}
    pezzi = testo.split()
    for nome, valore in zip(pezzi[::2], pezzi[1::2]):
        attr[nome] = int(valore) if re.fullmatch(r"-?\d+", valore) else valore
    return attr


def _scrivi_attributi(attr: dict) -> str:
    return " ".join(f"{k} {v}" for k, v in attr.items())


def taglia_di(sb) -> str:
    """La taglia del blocco, col nome inglese della tabella."""
    for testo in (sb.taglia, sb.tipo):
        for parola in re.findall(r"[^\W\d_]+", testo or ""):
            p = parola.lower()
            if p in ORDINE:
                return p
            canonica = SB.taglie()["alias"].get(p)
            if canonica:
                return SB.taglie()["taglie"][canonica]["srd"].lower()
    return "medium"


def dadi_vita(sb) -> int:
    m = _PF_DADO.search(sb.pf_dado or sb.tipo or "")
    return int(m.group(1)) if m else 1


def _naturale(dettaglio: str) -> int | None:
    m = re.search(r"([+-]\d+) naturale", dettaglio)
    return int(m.group(1)) if m else None


def _passo(dado: str, verso: int, regole: dict) -> str | None:
    tabella = regole["armi_su"] if verso > 0 else regole["armi_giu"]
    return tabella.get(dado)


def _sposta_bonus(testo: str, delta: int) -> str:
    return re.sub(r"[+-]\d+", lambda m: f"{int(m.group(0)) + delta:+d}", testo)


# ── il conto, in un verso o nell'altro ──────────────────────────────────────
def _muovi(sb, car: dict[str, int], naturale: int, passi_taglia: int,
           compositi: list[bool] | None = None) -> dict[str, int]:
    """Sposta i numeri del blocco: punteggi, pf, CA, TS, iniziativa, attacchi.
    I dadi di danno e il dettaglio della CA li cura chi chiama. Restituisce le
    variazioni dei modificatori."""
    attr = leggi_attributi(sb.attributi)
    dm: dict[str, int] = {}
    for nome, delta in car.items():
        prima = attr.get(nome)
        if not isinstance(prima, int):
            dm[nome] = 0
            continue
        attr[nome] = prima + delta
        dm[nome] = _mod(prima + delta) - _mod(prima)
    sb.attributi = _scrivi_attributi(attr)

    dv = dadi_vita(sb)
    delta_pf = dm.get("Cos", 0) * dv
    if delta_pf:
        sb.pf = str(max(dv, int(sb.pf) + delta_pf))
        # `pf-dado` registra i dadi e i bonus che non vengono dalla Costituzione:
        # il bonus di Costituzione sta nella riga del tipo, ed è quello che cambia
        # (solo se la riga lo scrive: quella di un PNG porta i dadi e basta)
        sb.tipo = _PF_DADO.sub(
            lambda m: f"{m.group(1)}d{m.group(2)}"
                      + (f"{int(m.group(3)) + delta_pf:+d}" if m.group(3) else ""),
            sb.tipo, count=1)

    taglia = taglia_di(sb)
    nuova = ORDINE[ORDINE.index(taglia) + passi_taglia]
    d_taglia = T.TAGLIE[nuova][1] - T.TAGLIE[taglia][1]
    if passi_taglia:
        _scrivi_taglia(sb, taglia, nuova)

    sb.ca = str(int(sb.ca) + naturale + dm.get("Des", 0) + d_taglia)
    ts = dict(re.findall(r"(Temp|Rifl|Vol) ([+-]\d+)", sb.ts))
    if ts:
        for nome, chiave in _TS:
            if nome in ts:
                ts[nome] = f"{int(ts[nome]) + dm.get(chiave, 0):+d}"
        sb.ts = re.sub(r"(Temp|Rifl|Vol) [+-]\d+", lambda m: f"{m.group(1)} {ts[m.group(1)]}", sb.ts)
    if dm.get("Des") and re.match(r"[+-]\d+", sb.iniziativa or ""):
        sb.iniziativa = re.sub(r"^[+-]\d+", lambda m: f"{int(m.group(0)) + dm['Des']:+d}",
                               sb.iniziativa)
    compositi = compositi or [None] * len(sb.attacchi)
    sb.attacchi = [_muovi_attacco(a, dm, d_taglia, c) for a, c in zip(sb.attacchi, compositi)]
    return {**dm, "taglia": d_taglia}


def _ha_forza_nel_danno(riga: str) -> bool:
    """Un attacco a distanza che somma la Forza al danno (arco composito, arma
    da lancio): lo dice il modificatore scritto dopo il dado."""
    return bool(re.search(r"\((?:\d+d\d+|\d+)[+-]\d+", riga))


def _muovi_attacco(riga: str, dm: dict[str, int], d_taglia: int,
                   composito: bool | None = None) -> str:
    m = re.match(r"^(\W*)(Mischia|Distanza)\b(.*?)((?:[+-]\d+)(?:/[+-]\d+)*) \(([^)]*)\)(.*)$", riga)
    if not m:
        return riga
    testa, forma, arma, bonus, danno, coda = m.groups()
    colpire = (dm.get("For", 0) if forma == "Mischia" else dm.get("Des", 0)) + d_taglia
    bonus = _sposta_bonus(bonus, colpire)
    d = _DADO.match(danno.strip())
    if d:
        dado, mod, resto = d.groups()
        ha_mod = mod is not None if composito is None else composito
        if forma == "Mischia" or ha_mod:
            nuovo = int(mod or 0) + dm.get("For", 0)
            mod = f"{nuovo:+d}" if nuovo else ""
        danno = f"{dado}{mod or ''}{resto}"
    return f"{testa}{forma}{arma}{bonus} ({danno}){coda}"


def _dadi_degli_attacchi(sb) -> list[str]:
    fuori = []
    for riga in sb.attacchi:
        m = re.search(r"\((\d+d\d+|\d+)(?=[+-]|\)|\s|/)", riga)
        fuori.append(m.group(1) if m else "")
    return fuori


def _cambia_dadi(sb, nuovi: list[str]) -> None:
    righe = []
    for riga, dado in zip(sb.attacchi, nuovi):
        if dado:
            riga = re.sub(r"\((\d+d\d+|\d+)(?=[+-]|\)|\s|/)", f"({dado}", riga, count=1)
        righe.append(riga)
    sb.attacchi = righe


def _scrivi_taglia(sb, vecchia: str, nuova: str) -> None:
    tabella = SB.taglie()
    per_srd = {v["srd"].lower(): k for k, v in tabella["taglie"].items()}
    if sb.tipo:
        sb.tipo = re.sub(rf"\b{vecchia}\b", lambda m: nuova.capitalize()
                         if m.group(0)[0].isupper() else nuova, sb.tipo, count=1, flags=re.I)
        sb.tipo = re.sub(rf"\b{per_srd[vecchia]}\b", per_srd[nuova], sb.tipo, count=1)
    if sb.taglia:
        sb.taglia = per_srd[nuova]
        riga = tabella["taglie"][per_srd[nuova]]
        if sb.spazio:
            sb.spazio = _metri(riga["spazio"])
        if re.fullmatch(r"[\d,\.]+ m", sb.portata or ""):
            sb.portata = _metri(riga["alta"])


def _metri(x: float) -> str:
    return (f"{x:g}".replace(".", ",")) + " m"


def _dettaglio_ca(dettaglio: str, dm_des: int, naturale: int, d_taglia: int) -> str:
    """Riscrive Des, naturale e taglia nel dettaglio della CA."""
    corpo = dettaglio.strip()
    if not (corpo.startswith("(") and corpo.endswith(")")):
        return dettaglio
    pezzi = [p.strip() for p in corpo[1:-1].split(",") if p.strip()]

    def sposta(etichetta: str, delta: int) -> None:
        if not delta:
            return
        for i, p in enumerate(pezzi):
            m = re.fullmatch(rf"([+-]\d+) {etichetta}", p)
            if m:
                nuovo = int(m.group(1)) + delta
                if nuovo or etichetta != "taglia":
                    pezzi[i] = f"{nuovo:+d} {etichetta}"
                else:
                    del pezzi[i]            # una taglia Media non scrive il suo +0
                return
        pezzi.append(f"{delta:+d} {etichetta}")

    sposta("Des", dm_des)
    sposta("naturale", naturale)
    sposta("taglia", d_taglia)
    return "(" + ", ".join(pezzi) + ")"


# ── applicare e disfare ─────────────────────────────────────────────────────
def gs_reale(gs: str, m: dict, dv: int) -> str:
    delta = m["gs"] if dv >= m.get("gs_da_dv", 0) else 0
    valore = Fraction(str(gs).strip()) + delta
    if valore < 1 and delta < 0:
        # sotto GS 1 si scende per frazioni: 1 → 1/2 → 1/3 → 1/4 …
        valore = Fraction(1, 2) if Fraction(str(gs).strip()) == 1 else Fraction(
            1, Fraction(str(gs).strip()).denominator + 1)
    return str(valore)


def applica(sb, nome: str) -> Traccia:
    """Applica un modello al blocco e dice che cosa ha fatto."""
    m = modello(nome)
    regole = dati()["modelli_regole"]
    taglia = taglia_di(sb)
    tipo = (sb.tipo or "").lower()
    if taglia in m.get("vietato_taglie", ()):
        raise ModelloVietato(f"il modello {m['nome']} non si applica a una creatura {taglia}")
    for vietato in m.get("vietato_tipi", ()):
        if re.search(rf"\b{vietato}\b", tipo) or (vietato == "dragon" and "drago" in tipo):
            raise ModelloVietato(f"il modello {m['nome']} non si applica al tipo {vietato}")
    dv = dadi_vita(sb)
    t = Traccia(modello=m["chiave"], gs_reale=gs_reale(sb.gs, m, dv),
                ca_dettaglio_prima=sb.ca_dettaglio)

    attr = leggi_attributi(sb.attributi)
    for car, delta in m.get("caratteristiche", {}).items():
        prima = attr.get(car)
        if not isinstance(prima, int):
            continue                       # chi non ha il punteggio non lo guadagna
        if car == "Int" and prima < m.get("int_minima", 0):
            continue
        t.caratteristiche[car] = max(1, prima + delta) - prima
    nat_prima = _naturale(sb.ca_dettaglio) or 0
    t.naturale = max(0, nat_prima + m.get("naturale", 0)) - nat_prima
    t.taglia = m.get("taglia", 0)

    t.compositi = [_ha_forza_nel_danno(a) for a in sb.attacchi]
    dm = _muovi(sb, t.caratteristiche, t.naturale, t.taglia)
    sb.ca_dettaglio = _dettaglio_ca(sb.ca_dettaglio, dm.get("Des", 0), t.naturale, dm["taglia"])

    if m.get("dadi"):
        prima = _dadi_degli_attacchi(sb)
        dopo = []
        for dado in prima:
            nuovo = _passo(dado, m["dadi"], regole) if dado else None
            if dado and nuovo is None:
                t.dadi_fermi.append(dado)
            dopo.append(nuovo or dado)
            t.dadi.append((dado, nuovo or dado))
        _cambia_dadi(sb, dopo)

    if "resistenze" in m:
        fascia = [f for f in dati()["modelli_difese"] if dv >= f["da"]][-1]
        if "scurovisione" not in (sb.sensi or "").lower():
            t.sensi_aggiunti = f"scurovisione {m['scurovisione']} m"
            sb.sensi = f"{sb.sensi}, {t.sensi_aggiunti}" if sb.sensi else t.sensi_aggiunti
        t.voci.append("Resistenze: " + ", ".join(
            f"{r} {fascia['resistenza']}" for r in m["resistenze"]))
        if fascia["rd"]:
            t.voci.append(f"RD {fascia['rd']}/{m['rd']}")
        ri = Fraction(t.gs_reale) + regole["ri_oltre_il_gs"]
        t.voci.append(f"RI {int(ri)}")
        t.voci.append(
            f"Punire {m['punire']} {regole['punire_al_giorno']}/giorno (azione veloce): "
            f"aggiunge il bonus di Carisma ai tiri per colpire e +{dv} ai danni contro "
            f"creature {m['contro']}, finché il bersaglio muore o la creatura riposa")

    if m["chiave"] == "advanced":
        avviso = ("⚠ template Advanced (PF1e) applicato SENZA alzare il GS: "
                  f"vale in realtà GS {t.gs_reale}")
    elif t.gs_reale == str(sb.gs).strip():
        avviso = (f"⚠ modello {m['nome']} (PF1e) applicato: con {dv} DV non cambia il GS, "
                  f"che resta {sb.gs}")
    else:
        avviso = (f"⚠ modello {m['nome']} (PF1e) applicato SENZA cambiare il GS: "
                  f"vale in realtà GS {t.gs_reale}")
    t.voci.append(avviso)
    sb.voci.extend(t.voci)

    delta_pf = dm.get("Cos", 0) * dv
    pezzi = []
    if t.caratteristiche:
        pezzi.append(", ".join(f"{k} {v:+d}" for k, v in t.caratteristiche.items())
                     + f" (→ {delta_pf:+d} pf, {dm.get('Des', 0):+d} CA da Des)")
    if t.naturale:
        pezzi.append(f"{t.naturale:+d} armatura naturale")
    if t.taglia:
        pezzi.append(f"taglia {taglia} → {taglia_di(sb)} ({dm['taglia']:+d} a CA e attacco)")
    if t.dadi:
        pezzi.append("dadi di danno " + ", ".join(f"{a} → {b}" for a, b in t.dadi if a))
    if t.dadi_fermi:
        pezzi.append("dadi fuori tabella, lasciati com'erano: " + ", ".join(t.dadi_fermi))
    if "resistenze" in m:
        pezzi.append("; ".join(v for v in t.voci[:-1]))
    t.righe.append(f"modello {m['nome']}: " + "; ".join(pezzi))
    t.righe.append(f"fonte: {m['fonte']}")
    if t.gs_reale != str(sb.gs).strip():
        t.righe.append(f"il modello vale GS {m['gs']:+d} e NON è stato contato: la creatura "
                       f"è venduta come GS {sb.gs} ma vale un GS {t.gs_reale}")
    return t


def disfa(sb, t: Traccia) -> None:
    """Rifà il conto al contrario: il blocco torna com'era prima di `applica`."""
    for voce in t.voci:
        if voce in sb.voci:
            sb.voci.remove(voce)
    if t.sensi_aggiunti:
        sb.sensi = re.sub(rf"(, )?{re.escape(t.sensi_aggiunti)}$", "", sb.sensi)
    if t.dadi:
        _cambia_dadi(sb, [prima for prima, _ in t.dadi])
    _muovi(sb, {k: -v for k, v in t.caratteristiche.items()}, -t.naturale, -t.taglia,
           t.compositi)
    sb.ca_dettaglio = t.ca_dettaglio_prima
