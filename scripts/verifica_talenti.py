#!/usr/bin/env python3
"""verifica_talenti.py — i prerequisiti dei talenti sulle schede che esistono (ADR-0124).

Scopo
  Il generatore sceglie talenti leciti (`dmcore.talenti`), ma nessun cancello
  controllava i talenti delle schede già scritte: il 2026-11-11 erano 30
  violazioni in 19 schede del Bestiario. Questo strumento legge le schede, e per
  ogni talento elencato restituisce il prerequisito che manca con la **regola**,
  il valore **atteso** e quello che la scheda **ha**, più `file:riga`.

  È pensato per essere chiamato da un agente attraverso il server MCP
  (`rumblingstone-tools`): con `--json` l'agente riceve la regola esatta e il
  controesempio, corregge, e richiama finché la scheda è pulita. Sola lettura.

  La regola è una sola, `dmcore.talenti.violazioni`, la stessa del generatore.
  I talenti bonus che una classe concede senza prerequisiti (monaco, stili del
  ranger) non sono violazioni. Un talento che il lessico non riconosce va in
  `ignoti`, e una classe che la scheda non dichiara nel `tipo` o nel titolo non
  si conosce: per questo le violazioni di livello d'incantatore o di classe
  vanno lette con la scheda accanto.

Uso
  python3 scripts/verifica_talenti.py                       # tutto il Bestiario
  python3 scripts/verifica_talenti.py Bestiario/png/x.md    # una scheda o una cartella
  python3 scripts/verifica_talenti.py --json                # uscita per l'agente
  python3 scripts/verifica_talenti.py --check               # esce 1 se c'è una violazione

Exit  0 = misura fatta (o nessuna violazione con --check)
      1 = violazioni, solo con --check
      2 = errore d'uso

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import lettura_creatura as L  # noqa: E402
from dmcore import talenti as T  # noqa: E402

#: La riga dei talenti: «**Talenti:** …», «Feats: …», «- Talenti: …».
RIGA = re.compile(r"^\W*(?:Talenti|Feats)\W*?(?:\*\*\s*)?(?::|：|\*\*)\**\s*(.+)$", re.I)
#: Incantatori e la frazione di livello che dà il livello d'incantatore (3.5:
#: paladino e ranger dal 4°, metà livello).
INCANTATORI = {"wizard": 1, "sorcerer": 1, "cleric": 1, "druid": 1, "bard": 1,
               "paladin": 0.5, "ranger": 0.5}
NON_VERIFICABILI = {"gradi", "altro"}
#: Le competenze che una classe base dà da sé (SRD 3.5, «Weapon and Armor
#: Proficiency» di ogni classe; PF1e uguale): non stanno nella riga dei talenti.
COMPETENZE_DI_CLASSE = {
    "Shield Proficiency": {"barbarian", "cleric", "druid", "fighter", "paladin", "ranger"},
    "Armor Proficiency (Light)": {"barbarian", "bard", "cleric", "druid", "fighter", "paladin",
                                  "ranger", "rogue"},
    "Armor Proficiency (Medium)": {"barbarian", "cleric", "druid", "fighter", "paladin", "ranger"},
    "Armor Proficiency (Heavy)": {"cleric", "fighter", "paladin"},
}
#: I maghi specialisti: nel `tipo` stanno col nome della scuola.
SPECIALISTI = {"abjurer", "conjurer", "diviner", "enchanter", "evoker", "illusionist", "necromancer",
               "transmuter", "abiuratore", "evocatore", "divinatore", "ammaliatore", "invocatore",
               "illusionista", "negromante", "trasmutatore"}
#: Regole che senza classi dichiarate non si possono giudicare.
SERVE_LA_CLASSE = ("lic", "capacita", "classe.")


def pezzi(riga: str) -> "list[str]":
    """I nomi dei talenti di una riga: virgole fuori dalle parentesi, senza markup."""
    riga = re.sub(r"`[^`]*`|\*|_", "", riga)
    riga = re.split(r"\s—\s|\.\s+[A-Z]", riga)[0]
    out, prof, buf = [], 0, ""
    for ch in riga:
        prof += (ch == "(") - (ch == ")")
        if ch == "," and prof == 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [re.sub(r"\s+", " ", x).strip(" .;") for x in out if x.strip()]


def _senza_parentesi(nome: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*", " ", nome).strip(" .;")


def _candidati(nome: str) -> "list[str]":
    """Il nome senza parentesi, poi l'inglese che il DM mette fra parentesi
    («Incidere Rune (Inscribe Rune)»), se ce n'è uno."""
    out = [_senza_parentesi(nome)]
    out += [m.strip() for m in re.findall(r"\(([A-Z][A-Za-z' -]+?)\s*(?:[,;][^)]*)?\)", nome)]
    return [x for x in out if x]


@lru_cache(maxsize=None)
def _lessici() -> "tuple[dict, dict, dict, set]":
    """(italiano 3.5 → inglese, inglese → manuale 3.5, italiano PF1e → inglese, inglesi PF1e)."""
    import lessico_regole as LR
    it35 = {LR.norma(v["it"]): v["srd35"] for v in LR.tabella_35() if v["tipo"] == "talento"}
    for v in LR.tabella_35():
        if v["tipo"] == "talento":
            for x in (v.get("varianti") or "").split("|"):
                if x.strip():
                    it35.setdefault(LR.norma(x), v["srd35"])
    itpf = {k: v["pf1"] for k, v in LR.tabella_pf1().items()}
    return it35, LR.talenti_dei_manuali(), itpf, LR.talenti_pf1_dei_manuali()


def risolvi(sistema: str, nome: str) -> "dict | None":
    """Il talento e la fonte che lo decide, nell'ordine SRD d20 → D&D 3.5 → PF1e
    (DM, 2026-11-12). Una scheda 3.5 cerca prima i dati del suo sistema (SRD 3.5:
    base, mostri, epici, psionici, divini), poi i manuali 3.5, di cui il repo ha
    solo i nomi, poi il PRD PF1e. Una scheda PF1e cerca nel PRD e poi nei manuali
    PF1e. Restituisce {en, sistema, fonte, verificabile} o None."""
    import lessico_regole as LR
    it35, man35, itpf, manpf = _lessici()
    cand = _candidati(nome)
    for c in cand:
        en = T.nome_inglese(sistema, c)
        if en:
            libro = T.dati(sistema)["talenti"][en].get("libro") or sistema
            return {"en": en, "sistema": sistema, "fonte": libro, "verificabile": True}
    if sistema == "dnd35":
        for c in cand:
            en = it35.get(LR.norma(c)) or (man35.get(LR.norma(c)) or {}).get("srd35")
            if not en:
                continue
            noto = T.nome_inglese("dnd35", en)
            if noto:
                return {"en": noto, "sistema": "dnd35",
                        "fonte": T.dati("dnd35")["talenti"][noto].get("libro"), "verificabile": True}
            man = (man35.get(LR.norma(en)) or {}).get("manuale") or "manuale 3.5"
            return {"en": en, "sistema": "dnd35", "fonte": f"3.5 {man}".strip(), "verificabile": False}
    for c in cand:
        en = T.nome_inglese("pf1e", c) or T.nome_inglese("pf1e", itpf.get(LR.norma(c), ""))
        if en:
            libro = T.dati("pf1e")["talenti"][en].get("libro") or "prd"
            return {"en": en, "sistema": "pf1e", "fonte": f"pf1e {libro}", "verificabile": True}
    for c in cand:
        if LR.norma(c) in manpf:
            return {"en": c, "sistema": "pf1e", "fonte": "pf1e manuale", "verificabile": False}
    return None


def sistema_di(p: Path, testo: str) -> str:
    """Il sistema che la scheda dichiara, altrimenti quello del suo percorso (sistemi.toml)."""
    from dmcore import sistemi as S
    dichiarato = S.sistema_dichiarato(testo)
    if dichiarato:
        return dichiarato
    return S.sistema_di(p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.name)


def leggi(p: Path) -> "dict | None":
    """I fatti di una scheda che servono ai prerequisiti, o None se non ha talenti."""
    return leggi_testo(p.read_text(encoding="utf-8", errors="replace"), p)


def leggi_testo(t: str, p: Path) -> "dict | None":
    """Come `leggi`, su un testo già letto: una scheda sola di un file che ne ha più d'una."""
    s = L.leggi_testo(t, p)
    if s is None:
        return None
    righe = s.testo.splitlines()
    n_riga, riga = next(((i + 1, m.group(1)) for i, r in enumerate(righe) if (m := RIGA.match(r))),
                        (None, None))
    if riga is None:
        return None
    sistema = sistema_di(p, s.testo)
    livelli: dict[str, int] = {}
    for n, liv in L.livelli_di_classe(s).items():
        n = T._ALIAS.get(n, n) if n in T.CLASSI_EN_IT.values() else n
        livelli[n] = livelli.get(n, 0) + liv
    # Le classi che il `tipo` nomina e la lettura non conosce (classi di prestigio,
    # specialisti): il mago specialista è un mago; le altre rendono inaffidabili
    # livello d'incantatore, capacità e livelli di classe, che vanno fra i non verificabili.
    ignote = []
    tipo = next((r for r in righe if r.lower().startswith("tipo:")), "")
    for nome, liv in re.findall(r"(?:^|[,/])\s*([A-Za-zÀ-ú' -]+?)\s+(\d+)(?=\s*(?:[,/]|$))", tipo[5:]):
        k = re.sub(r"^ex[- ]", "", nome.strip().lower())  # «ex-Paladin 7»: i livelli restano
        if k in SPECIALISTI:
            livelli["wizard"] = livelli.get("wizard", 0) + int(liv)
        elif not any(x in livelli for c in (k, k.split()[-1]) for x in (c, T._ALIAS.get(c, c))):  # «hobgoblin barbaro 4»
            ignote.append(f"{nome.strip()} {liv}")
    dv = sum(g.n for g in s.gruppi)
    lic = int(max([livelli.get(c, 0) * f if livelli.get(c, 0) >= (4 if f < 1 else 1) else 0
                   for c, f in INCANTATORI.items()] or [0]))
    # SRD, pietra ioun «orange prism»: +1 al livello dell'incantatore di chi la porta.
    if lic and re.search(r"prisma arancione|orange prism", s.testo, re.I):
        lic += 1
    talenti, senza_regole, ignoti = [], [], []
    nomi = []
    for nome in pezzi(riga):
        # «Arma Focalizzata e Arma Specializzata»: due talenti, se le due metà lo sono
        parti = re.split(r"\s+(?:e|and)\s+", nome)
        ok = len(parti) > 1 and risolvi(sistema, nome) is None and all(risolvi(sistema, x) for x in parti)
        nomi += parti if ok else [nome]
    for nome in nomi:
        r = risolvi(sistema, nome)
        if r is None:
            ignoti.append(_senza_parentesi(nome))
        elif r["verificabile"]:
            # «(B)» è il talento bonus della creatura: il Manuale dei Mostri lo dà
            # senza prerequisiti (SRD, Monster Feats, «Bonus Feats»).
            talenti.append({**r, "bonus": True} if re.search(r"\(B\)", nome) else r)
        else:
            senza_regole.append(r)
    return {"file": p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p),
            "riga": n_riga, "sistema": sistema,
            "car": {k: v for k, v in s.attributi.items() if isinstance(v, int)},
            "bab": s.bab, "livelli": livelli, "dv": dv, "lic": lic,
            "talenti": list({r["en"]: r for r in talenti}.values()), "nomi": nomi,
            "senza_regole": senza_regole, "ignoti": ignoti, "classi_ignote": ignote,
            "piu_schede": len(L.BLOCCO.findall(s.testo)) > 1,
            "fonte_ufficiale": bool(re.search(r"^# .*\[TRANSCRIBED — (?!PCGen)", s.testo, re.M)),
            "fisici": fatti_fisici(s)}


# --- i prerequisiti «fisici»: movimento, taglia, tipo, attacchi naturali (ADR-0124 §9) ---

#: taglia → il modificatore di taglia alla CA, che è come `L.taglia_di` la restituisce
_TAGLIE = {"fine": 8, "diminutive": 4, "tiny": 2, "small": 1, "medium": 0, "large": -1,
           "huge": -2, "gargantuan": -4, "colossal": -8}
_MOVIMENTI = {"volo": r"volare|volo|fly", "nuoto": r"nuotare|nuoto|swim",
              "scalare": r"scalare|climb", "scavare": r"scavare|burrow"}
_NATURALI = (r"mors[oi]|artigli[oi]?|coda|al[ai]|schiant[oi]|corn[oai]|incornat[ae]|zoccol[oi]|tentacol[oi]|"
             r"pungiglion[ei]|zann[ae]|sperone|speroni|bites?|claws?|tail(?: slap)?|wings?|slams?|gores?|"
             r"hoo(?:f|ves)|tentacles?|stings?|talons?|rakes?")
_NUMERI = {"one": 1, "two": 2, "three": 3, "four": 4}
_TS_INGLESE = {"fortitude": "temp", "reflex": "rifl", "will": "vol"}


def fatti_fisici(s: "L.Scheda") -> dict:
    """Quello che la scheda scrive di movimento, taglia, tipo e attacchi naturali.

    Un fatto è None quando la scheda non ha la riga da cui leggerlo: allora il
    prerequisito resta non verificabile, non diventa una violazione."""
    testo = s.testo
    riga_vel = re.search(r"^(?:velocita|speed):\s*(.+)$|\*\*Speed\*\*:?\s*([^|\n]+)|\bVel\.?\s+(\d[^·\n]*)",
                         testo, re.M | re.I)
    vel = next((g for g in riga_vel.groups() if g), None) if riga_vel else None
    movimenti = None
    if vel is not None:
        movimenti = {}
        for nome, parole in _MOVIMENTI.items():
            m = re.search(rf"\b(?:{parole})\s+(\d+(?:[.,]\d+)?)\s*(m|ft|feet)\b", vel, re.I)
            if m:
                n = float(m.group(1).replace(",", "."))
                movimenti[nome] = round(n / 1.5 * 5) if m.group(2).lower() == "m" else int(n)
    blocco = re.search(r"^attacchi:\n((?:\s+-.*\n?)+)", testo, re.M)
    riga_att = blocco.group(1) if blocco else next(
        (r for r in testo.splitlines() if re.search(r"\*\*(?:Attacco|Attack|Full Attack|Mischia|Melee)\*\*", r)), None)
    # Gli attacchi naturali si contano dove sono di più: il blocco `attacchi:` a
    # volte porta solo l'attacco singolo. `completo` dice se la scheda scrive
    # l'attacco completo: solo allora un conto basso è una violazione.
    conta = lambda r: sum(int(n or 1) for n, _ in  # noqa: E731
                          re.findall(rf"(?:\b(\d)\s+)?\b({_NATURALI})\b\s*[+-]\d", r, re.I))
    pieno = re.search(r"\*\*(?:Attacco completo|Full Attack)\*\*:?\s*([^\n]*(?:\n(?!\n)[^\n]*){0,2})", testo, re.I)
    fonti_att = [x for x in (riga_att, pieno.group(1) if pieno else None) if x is not None]
    naturali = max(map(conta, fonti_att)) if fonti_att else None
    completo = bool(pieno) or bool(blocco and len(blocco.group(1).strip().splitlines()) > 1)
    ca = re.search(r"^ca-dettaglio:.*$|\*\*(?:AC|CA)\*\*:?[^\n]*", testo, re.M)
    base = None
    if s.composizione_nota and s.gruppi:
        base = L.ts_base(s.gruppi)[0]
    tra_parentesi = re.search(r"\(([^)]*)\)", s.tipo or "")
    sottotipi = {x.strip().lower() for x in tra_parentesi.group(1).split(",")} if tra_parentesi else None
    sigla = re.search(r"(?:,|\s)\s*\**([LNC][GNEBM]|N)\**\s*\.?\s*$", (s.tipo or "").strip())
    allineamento = sigla.group(1).upper().translate(str.maketrans("BM", "GE")) if sigla else None
    return {"sottotipi": sottotipi, "allineamento": allineamento,
            "movimenti": movimenti, "taglia": L.taglia_di(testo) if s.tipo else None,
            "tipo": T_tipo(s.tipo), "attacchi_naturali": naturali, "attacco_completo": completo,
            "armatura_naturale": bool(re.search(r"natural", ca.group(0), re.I)) if ca else None,
            "soffio": bool(re.search(r"\bsoffio\b|breath weapon", testo, re.I)), "ts_base": base}


def T_tipo(tipo: str) -> "str | None":
    return L.T.normalizza_tipo(tipo) if tipo else None


#: le razze che la riga del tipo scrive come sottotipo dell'umanoide, e che si escludono a vicenda
_RAZZE = {"human", "dwarf", "elf", "gnome", "halfling", "orc", "gnoll", "goblinoid", "reptilian"}
_RAZZE_IT = {"umano": "human", "nano": "dwarf", "elfo": "elf", "gnomo": "gnome", "orco": "orc"}
#: i sottotipi dell'SRD che una riga del tipo scrive sempre, se la creatura li ha
_SOTTOTIPI = {"air", "aquatic", "cold", "earth", "fire", "incorporeal", "swarm", "water", "shapechanger"}
_ALLINEAMENTI = {"good": "G", "evil": "E", "lawful": "L", "chaotic": "C"}


def _giudica_razza(t: str, fatti: dict) -> "tuple[bool, str] | None":
    """Razza e sottotipo: si giudicano solo se la riga del tipo scrive i sottotipi."""
    m = re.fullmatch(r"prerace:1,([a-z][a-z' -]*)|([a-z][a-z' -]*?)(?: (sub)?type)?", t)
    if not m:
        return None
    serve = (m.group(1) or m.group(2)).strip()
    suoi = fatti.get("sottotipi")
    if suoi is None or not (serve in _RAZZE or serve in _SOTTOTIPI or serve in suoi):
        return None
    suoi = {_RAZZE_IT.get(x, x) for x in suoi}
    if serve in suoi:
        return True, "sottotipo " + serve
    if serve in _SOTTOTIPI and m.group(3):
        return False, "sottotipi " + ", ".join(sorted(suoi))
    if serve in _RAZZE and fatti.get("tipo") == "humanoid" and suoi & _RAZZE:
        return False, "razza " + ", ".join(sorted(suoi & _RAZZE))
    return None


def _giudica_allineamento(t: str, fatti: dict) -> "tuple[bool, str] | None":
    ha = fatti.get("allineamento")
    m = re.fullmatch(r"prealign:([a-z,]+)", t)
    if m:
        ammessi = {x.upper().replace("TN", "N") for x in m.group(1).split(",")}
        return None if ha is None else (ha in ammessi, "allineamento " + ha)
    m = re.fullmatch(r"(?:any )?(non-?)?\s*(good|evil|lawful|chaotic)(?: alignment)?", t)
    if not m or ha is None:
        return None
    lettera = _ALLINEAMENTI[m.group(2)]
    ce = lettera in (ha[0] if lettera in "LC" else ha[-1]) and ha != "N"
    return (not ce if m.group(1) else ce), "allineamento " + ha


def giudica_altro(prerequisito: str, fatti: dict) -> "tuple[bool, str] | None":
    """(soddisfatto, che cosa ha la scheda) di un prerequisito fisico, o None se non si sa leggere."""
    t = prerequisito.lower().strip()
    for giudice in (_giudica_allineamento, _giudica_razza):
        esito = giudice(t, fatti)
        if esito is not None:
            return esito
    mov = fatti["movimenti"]
    for nome, inglese in (("volo", "fly"), ("nuoto", "swim"), ("scalare", "climb"), ("scavare", "burrow")):
        m = re.fullmatch(rf"{inglese} speed(?: (?:of )?(\d+)(?: ft\.?| feet)?)?(?: or (?:more|higher|better))?", t)
        if m:
            if mov is None:
                return None
            serve = int(m.group(1) or 1)
            return mov.get(nome, 0) >= serve, (f"{nome} {mov[nome]} ft" if nome in mov else f"nessuna velocità di {nome}")
    m = re.fullmatch(r"(?:size )?(\w+) or (larger|smaller)(?: size)?|size (\w+) or (larger|smaller)", t)
    if m:
        nome, verso = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        if nome not in _TAGLIE or fatti["taglia"] is None:
            return None
        ha = fatti["taglia"]
        ok = ha <= _TAGLIE[nome] if verso == "larger" else ha >= _TAGLIE[nome]
        return ok, "taglia " + next(k for k, v in _TAGLIE.items() if v == ha)
    m = re.fullmatch(r"(\w+) or more natural (?:attacks|weapons)|(two) claw attacks|natural (?:weapon|attack)s?", t)
    if m:
        if fatti["attacchi_naturali"] is None:
            return None
        if m.group(2):
            return None   # servono proprio due artigli: il conto degli attacchi non basta
        serve = _NUMERI.get(m.group(1) or "one", None) or (int(m.group(1)) if (m.group(1) or "").isdigit() else None)
        if serve is None:
            return None
        if fatti["attacchi_naturali"] < serve and not fatti.get("attacco_completo"):
            return None
        return fatti["attacchi_naturali"] >= serve, f"{fatti['attacchi_naturali']} attacchi naturali"
    if t == "natural armor":
        return None if fatti["armatura_naturale"] is None else (fatti["armatura_naturale"], "armatura naturale"
                                                                if fatti["armatura_naturale"] else "nessuna armatura naturale")
    if t in ("breath weapon", "breath weapon attack"):
        return (True, "soffio") if fatti["soffio"] else None   # l'assenza della parola non prova niente
    m = re.fullmatch(r"base (fortitude|reflex|will) save(?: bonus)? \+(\d+)", t)
    if m:
        if fatti["ts_base"] is None:
            return None
        ha = fatti["ts_base"][_TS_INGLESE[m.group(1)]]
        return ha >= int(m.group(2)), f"tiro salvezza base +{ha}"
    m = re.fullmatch(r"(\w+(?: \w+)?) type|(aberration|animal|construct|dragon|elemental|fey|giant|humanoid|"
                     r"magical beast|monstrous humanoid|ooze|outsider|plant|undead|vermin)", t)
    if m and fatti["tipo"]:
        return fatti["tipo"] == (m.group(1) or m.group(2)), f"tipo {fatti['tipo']}"
    return None


def verifica(f: dict) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) di una scheda letta da `leggi`.

    Ogni voce porta `fonte`: il libro che ha deciso la regola (srd, srd-mostri,
    srd-epici, …, «pf1e apg»). Un talento dei manuali 3.5 di cui il repo non ha
    i prerequisiti va fra i non verificabili con regola `fonte`: non passa per
    buono e non viene segnato come sbagliato."""
    dalla_classe = [c for c, classi in COMPETENZE_DI_CLASSE.items() if classi & set(f["livelli"])]
    nomi = [r["en"] for r in f["talenti"]] + [r["en"] for r in f["senza_regole"]]
    # «Expeditious Dodge» vale come Dodge per i prerequisiti (talenti_equivalenti.toml)
    for base, sostituti in T.dati(f["sistema"]).get("equivalenti", {}).items():
        if base not in nomi and any(x in nomi for x in sostituti):
            nomi.append(base)
    concessi = talenti_concessi(f["livelli"])
    st = T.Stato(car=f["car"], bab=f["bab"] if f["bab"] is not None else 99,
                 livelli=f["livelli"], lic=f["lic"], talenti=nomi + dalla_classe, dv=f["dv"])
    viol, nv = [], []
    for r in f["senza_regole"]:
        nv.append({"file": f["file"], "riga": f["riga"], "talento": r["en"], "talento_it": r["en"],
                   "regola": "fonte", "atteso": "prerequisiti del manuale", "ha": None,
                   "testo": f"prerequisiti di {r['en']} non nel repo", "fonte": r["fonte"],
                   "nota": "talento di un manuale: il repo ha il nome, non i prerequisiti"})
    for r in f["talenti"]:
        en, sis = r["en"], r["sistema"]
        if T.bonus_senza_prerequisiti(f["sistema"], en, f["livelli"]) or en in concessi:
            continue
        # il talento bonus «(B)» vale solo per chi ha dadi vita razziali: a un PNG
        # fatto solo di classi nessuna regola lo dà
        if r.get("bonus") and (f["dv"] or 0) > sum((f["livelli"] or {}).values()):
            continue
        for v in T.violazioni(sis, en, st):
            if v["regola"] == "bab" and f["bab"] is None:
                continue
            voce = {"file": f["file"], "riga": f["riga"], "talento": en,
                    "talento_it": T.italiano(sis, en), **v, "fonte": r["fonte"]}
            ignote = f.get("classi_ignote") or []
            senza_classe = ((not f["livelli"] or ignote) and v["regola"].startswith(SERVE_LA_CLASSE)
                            and v["regola"] != "classe.character")
            if senza_classe:
                voce["nota"] = ("classi che la lettura non conosce: " + ", ".join(ignote) if ignote else
                                "la scheda non dichiara le classi nel tipo né nel titolo")
            if T.dati(sis)["talenti"].get(en, {}).get("diverge") and v["regola"] not in NON_VERIFICABILI:
                # PCGen e la tabella del manuale non danno gli stessi prerequisiti (ADR-0124 §6)
                nv.append({**voce, "nota": "le due fonti del manuale divergono su questo talento: rileggere sul libro"})
                continue
            if v["regola"] == "altro" and f.get("fisici"):
                esito = giudica_altro(str(v["atteso"]), f["fisici"])
                if esito is not None:
                    if esito[0]:
                        continue
                    voce.update(regola="fisico", ha=esito[1], testo=f"{v['atteso']} (ha: {esito[1]})")
                    viol.append(voce)
                    continue
            (nv if v["regola"] in NON_VERIFICABILI or senza_classe else viol).append(voce)
    # Una violazione non si afferma quando la scheda non è una sola (i talenti letti
    # possono essere di un'altra) o quando ripete una fonte ufficiale così com'è stampata.
    motivo = ("il file ha più schede: classi e talenti letti possono essere di schede diverse"
              if f.get("piu_schede") else
              "uguale alla fonte ufficiale trascritta: il difetto, se c'è, è del manuale"
              if f.get("fonte_ufficiale") else None)
    if motivo:
        nv += [{**v, "nota": motivo} for v in viol]
        viol = []
    return viol, nv


def talenti_concessi(livelli: "dict[str, int]") -> "set[str]":
    """I talenti che le classi dei manuali danno per nome ai livelli che la scheda ha
    (`talenti_concessi` di classi_manuali.toml): si hanno anche senza i prerequisiti."""
    manuali = L.T._DATI.get("classi_manuali", {})
    per_nome = {**manuali, **{v["it"]: v for v in manuali.values() if v.get("it")}}
    out: set = set()
    for classe, n in livelli.items():
        for liv, nomi in (per_nome.get(classe, {}).get("talenti_concessi") or {}).items():
            if int(liv) <= n:
                out.update(nomi)
    return out


def schede(percorsi: "list[Path]") -> "list[Path]":
    out = []
    for p in percorsi:
        out += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    return out


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="*", type=Path, help="schede o cartelle (difetto: Bestiario/)")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    a = ap.parse_args(argv)
    percorsi = [p if p.is_absolute() else ROOT / p for p in (a.percorsi or [Path("Bestiario")])]
    for p in percorsi:
        if not p.exists():
            print(f"verifica_talenti: {p} non esiste", file=sys.stderr)
            return 2
    lette, viol, nv, ignoti = 0, [], [], []
    for p in schede(percorsi):
        f = leggi(p)
        if f is None:
            continue
        lette += 1
        v, n = verifica(f)
        viol += v
        nv += n
        ignoti += [{"file": f["file"], "riga": f["riga"], "nome": x} for x in f["ignoti"]]
    if a.json:
        json.dump({"schede_con_talenti": lette, "violazioni": viol, "non_verificabili": nv,
                   "ignoti": ignoti}, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        for v in viol:
            print(f"{v['file']}:{v['riga']}: {v['talento_it']} ({v['talento']}) — "
                  f"manca {v['testo']}  [regola {v['regola']}, fonte {v['fonte']}]")
        print(f"{'✗' if viol else '✓'} verifica_talenti: {lette} schede con talenti, "
              f"{len(viol)} violazioni in {len({v['file'] for v in viol})} schede, "
              f"{len(nv)} prerequisiti non verificabili, {len(ignoti)} nomi non riconosciuti")
    return 1 if (a.check and viol) else 0


if __name__ == "__main__":
    sys.exit(main())
