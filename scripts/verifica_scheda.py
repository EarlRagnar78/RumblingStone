#!/usr/bin/env python3
"""verifica_scheda.py — tutte le verifiche di regola di una scheda, in una chiamata (ADR-0124).

Scopo
  Un agente che scrive o corregge una scheda chiede al server MCP
  (`rumblingstone-tools`) «che cosa non torna?» e riceve, per ogni difetto,
  la **regola**, il valore **atteso**, quello che la scheda **ha**, la
  **fonte** che decide e `file:riga`. Corregge e richiama finché è pulita.
  Sola lettura: non scrive mai il canone.

  Mette insieme i verificatori che esistono, più il controllo dei gradi:
    talenti  prerequisiti dei talenti (`verifica_talenti`: SRD d20 → manuali
             3.5 → PF1e)
    numeri   pf nella fascia dei dadi vita, BAB, tiri salvezza, lotta,
             attacco, iniziativa (`conformita_statblocchi.giudica`)
    abilita  gradi delle abilità: massimo per abilità e punti disponibili
             (capacità `creature.gradi` del plugin; 3.5 e PF1e)
    incantesimi  ogni incantesimo scritto per livello è nella lista della classe
             (o in un dominio) e non sotto il suo livello (capacità
             `creature.liste_incantesimi`; 3.5 dall'SRD, PF1e dal PRD)
    incantatori  incantesimi al giorno (tabella della classe, incantesimi
             bonus, slot di dominio o di scuola), conosciuti, livello massimo
             lanciabile e CD (capacità `creature.incantatori`; ADR-0126, lotto 3)
    prestigio  i requisiti delle classi di prestigio: bonus di attacco base
             delle altre classi, gradi (massimo prima dell'ingresso e abilità
             scritta), talenti, razza, allineamento, livello d'incantesimo
             (capacità `creature.prestigio`; ADR-0126, lotto 3-bis)
    creatura_base  dadi vita razziali e armatura naturale della creatura base
             che la fonte della scheda dichiara («SRD *Ogre* + …»), e il dado
             dei suoi attacchi naturali nel conto del danno (capacità
             `creature.base`; ADR-0126, lotto 5)
    grado_di_sfida  il grado di sfida scritto contro livelli di classe (da PG o
             da PNG), eccezioni di razza e creatura base (tabella `[gs]` della
             capacità `creature.costruzione`; ADR-0126, lotto 5)
    velocita  la velocità a terra scritta contro razza, movimento veloce di barbaro e
             monaco, armatura media o pesante (tabella `[movimento]` della capacità
             `creature.costruzione`; ADR-0126, lotto 7)
    difese    resistenza agli incantesimi (razza + livelli di classe, monaco) e
             riduzione del danno del barbaro (tabella `[difese]` della capacità
             `creature.costruzione`; ADR-0126, lotto 7)
    linguaggi i linguaggi automatici della razza e il Druidico del druido nella riga
             dei linguaggi (tabella `[linguaggi]` della capacità
             `creature.costruzione`; ADR-0126, lotto 7)
    ricchezza il valore minimo dell'equipaggiamento (oggetti dal prezzo certo)
             contro quello di un PNG del suo livello effettivo (tabella
             `[oggetti]` della capacità `creature.costruzione`; ADR-0126, lotto 8)
    numero_talenti  quanti talenti: per dadi vita, bonus di classe, umano; fuori
             dal conto quelli concessi dalla classe e quelli dichiarati
             («(B)», «(razziale)», «(dominio)», «(difetto)») (ADR-0126, lotto 4)

  Le regole sono quelle del plugin del sistema della scheda (`sistemi/<id>`).
  Un conto che il plugin non sa fare non compare: `non_verificabili` dice che
  cosa resta fuori e perché.

Uso
  python3 scripts/verifica_scheda.py Bestiario/png/x.md           # una scheda
  python3 scripts/verifica_scheda.py Bestiario/villain --json     # una cartella, per l'agente
  python3 scripts/verifica_scheda.py x.md --check                 # esce 1 se c'è una violazione
  python3 scripts/verifica_scheda.py x.md --fatti                 # non giudica: talenti, incantesimi,
                                                                  # capacità speciali e righe di «Tattiche»
                                                                  # e «Descrizione», in JSON (ADR-0126);
                                                                  # `blocchi`: una voce per scheda del file

Exit  0 = misura fatta (o nessuna violazione con --check)
      1 = violazioni, solo con --check
      2 = errore d'uso

Solo stdlib.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verifica_talenti as VT  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402
from dmcore import bonus as B  # noqa: E402

#: campo di conformita_statblocchi → riga della scheda dove cercarlo
ETICHETTE = {"BAB": ("bab", "base attack"), "lotta": ("lotta", "grapple", "bmc"),
             "Temp": ("temp", "fort"), "Rifl": ("rifl", "ref"), "Vol": ("vol", "will"),
             "pf": ("pf", "hp"), "iniziativa": ("iniz", "init"), "attacco": ("attacc", "attack", "melee", "mischia")}


def _riga(testo: str, campo: str) -> "int | None":
    chiavi = ETICHETTE.get(campo, (campo.lower(),))
    for i, r in enumerate(testo.splitlines(), 1):
        if any(k in r.lower() for k in chiavi):
            return i
    return None


#: Tolleranza zero su tiri salvezza e attacco (DM, 2026-11-12). `--tolleranza`
#: la rimette com'era: TS fino a +4 sopra l'atteso, attacco fra −1 e +2.
SEVERO = True


def numeri(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei numeri di una scheda."""
    import conformita_statblocchi as C
    with contextlib.redirect_stdout(io.StringIO()):
        s = L.leggi(p)
        if s is None:
            return [], []
        if not C.del_sistema(p):
            sis = VT.sistema_di(p, s.testo)
            return [], [{"file": VT_rel(p), "riga": None, "verifica": "numeri", "regola": "sistema",
                         "testo": f"i conti di scheda non coprono il sistema {sis}", "fonte": sis}]
        g = C.giudica(s, severo=SEVERO)
    viol, nv = [], []
    dichiarati = B.dichiarati(L.senza_note(s.testo))
    ignote = (VT.leggi(p) or {}).get("classi_ignote") or []
    if not g["verificabile"]:
        nv.append({"file": g["file"], "riga": None, "verifica": "numeri", "regola": "lettura",
                   "testo": "dadi vita o caratteristiche non leggibili: nessun conto parte", "fonte": "srd"})
    for campo, (scritto, atteso, scarto) in g["scarti"].items():
        voce = {"file": g["file"], "riga": _riga(s.testo, campo), "verifica": "numeri",
                "regola": f"numero.{campo}", "atteso": atteso, "ha": scritto,
                "testo": f"{campo} {scritto}, la regola dà {atteso} (scarto {scarto:+d})"
                if isinstance(scarto, int) else f"{campo} {scritto}, la regola dà {atteso}",
                "fonte": "srd"}
        if campo in B.CAMPI_TS or campo == "attacco":
            contate = B.somma(dichiarati.get(campo, []))[1]
            voce["bonus_contati"] = [{"valore": v.valore, "tipo": v.tipo, "sorgente": v.sorgente}
                                     for v in contate]
            voce["testo"] += ("; bonus dichiarati e contati: "
                              + ", ".join(f"+{v.valore} {v.tipo.replace('_', ' ')} ({v.sorgente})"
                                          for v in contate) if contate
                              else "; la scheda non dichiara nessun bonus su questo numero")
        if "-cr" not in p.name:
            # conformita_statblocchi è collaudato sulle schede `*-cr*.md`; nei dossier
            # («BAB/Lotta: +8 / +10») la lettura prende il numero sbagliato
            voce["nota"] = "scheda a dossier: la lettura dei numeri non è collaudata su questo formato"
        elif ignote:
            voce["nota"] = "classi che la lettura non conosce: " + ", ".join(ignote)
        if g["template"]:
            voce["nota"] = f"lo scarto si spiega col template {g['template']}"
        if campo in g["come_la_fonte"]:
            voce["nota"] = "uguale alla fonte trascritta"
        if g["decisione"]:
            voce["nota"] = f"decisione aperta al DM: {g['decisione']}"
        (nv if "nota" in voce else viol).append(voce)
    return viol, nv


def VT_rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)


def talenti(p: Path) -> "tuple[list[dict], list[dict], list[dict]]":
    f = VT.leggi(p)
    if f is None:
        return [], [], []
    v, nv = VT.verifica(f)
    for x in v + nv:
        x["verifica"] = "talenti"
    ign = [{"file": f["file"], "riga": f["riga"], "verifica": "talenti", "regola": "nome",
            "testo": f"«{n}» non è un talento di nessuna fonte", "fonte": None} for n in f["ignoti"]]
    return v, nv, ign


#: riga delle abilità: «**Abilità**: Ascoltare +12, …», «Skills: Hide +5, …»
RIGA_ABILITA = re.compile(r"(?:^|[\s*·])(?:Abilit[àa]|Skills)\**:?\**\s+(?=[A-ZÀ-Ý])(.+?)(?=\s·\s|\s\*\*[A-ZÀ-Ý]|$)")
VOCE_ABILITA = re.compile(r"([A-Za-zÀ-ú' ]+?)(?:\s*\(([^)]*)\))?\s*([+\-−]\d+)")
#: talenti che danno +2 a due abilità o +3 a una, nominati fuori dalla riga dei talenti:
#: lì non si sa su quale abilità, e il margine vale per tutte
TALENTI_ABILITA = re.compile(r"Skill Focus|Abilità Focalizzata|Alertness|Allerta|Acrobatic|Agile|Athletic|Atletico|"
                             r"Deceitful|Deft Hands|Diligent|Investigator|Magical Aptitude|Negotiator|Nimble Fingers|"
                             r"Persuasive|Persuasivo|Self-Sufficient|Stealthy|Furtivo|Animal Affinity", re.I)


@lru_cache(maxsize=None)
def _abilita_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {LR.norma(v["it"]): v["srd35"].lower() for v in LR.tabella_35() if v["tipo"] == "abilità"}


@lru_cache(maxsize=None)
def _classi_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {v["it"].lower(): v["srd35"].lower() for v in LR.tabella_35()
            if v["tipo"] in ("classe", "classe di prestigio")}


def _punti_di_classe(regole: dict, classe: str) -> "int | None":
    v = regole.get("classi", {}).get(classe)
    if v is None:   # le classi dei manuali 3.5 fuori SRD (classi_manuali.toml)
        m = regole.get("classi_manuali", {}).get(classe) or {}
        return None if "punti" in (m.get("diverge") or ()) else m.get("punti")
    return v.get("gradi") if isinstance(v, dict) else v


def _bonus_dei_talenti(nomi: "list[str]", sistema: str, effetti: dict, chiave: dict,
                       dv: int) -> "tuple[dict[str, int], int]":
    """({abilità: bonus}, bonus su tutte) che i talenti scritti danno alle abilità.

    I numeri sono del plugin (`effetti_talenti`): +2 a due abilità, +3 a una
    scelta. L'abilità scelta sta fra parentesi accanto al talento; se non si
    legge, il bonus vale per tutte (il conto resta una condizione necessaria).
    Dove il bonus cresce coi gradi (PF1e) si prende il più alto che i dadi vita
    permettono. Bonus di talenti diversi sulla stessa abilità si sommano."""
    import lessico_regole as LR
    per: dict[str, int] = {}
    a_tutte = 0
    for nome in nomi:
        r = VT.risolvi(sistema, nome)
        e = effetti.get((r or {}).get("en", "").lower())
        if not e:
            continue
        b = e["bonus_con_gradi"] if dv >= e.get("con_gradi", 10 ** 6) else e["bonus"]
        if e.get("a_scelta"):
            m = re.search(r"[(:]\s*([^)]+)", nome)
            en = _abilita_it().get(LR.norma(m.group(1).strip()), m.group(1).strip().lower()) if m else None
            en = next((k for k in chiave if en and (en == k or en.startswith(k + " "))), None)
            if en is None:
                a_tutte = max(a_tutte, b)
            else:
                per[en] = per.get(en, 0) + b
            continue
        for a in e.get("abilita", []):
            k = next((k for k in chiave if a == k or a.startswith(k + " ")), a)
            per[k] = per.get(k, 0) + b
    return per, a_tutte


def _talenti_d_abilita(nomi: "list[str]", testo: str, sistema: str, regole: dict,
                       dv: int) -> "tuple[dict[str, int], int]":
    """Il bonus dei talenti sulle abilità: dalla riga dei talenti, e se lì non ce
    n'è da dove il testo li nomina («Allerta dal famiglio», una riga dei talenti
    che la lettura non trova): valgono lo stesso, sulle loro abilità."""
    effetti, chiave = regole.get("effetti_talenti", {}), regole["chiave"]
    per, a_tutte = _bonus_dei_talenti(nomi, sistema, effetti, chiave, dv)
    if not per and not a_tutte:
        altrove = [m.group(0) for m in re.finditer(rf"(?:{TALENTI_ABILITA.pattern})(?:\s*\([^)]*\))?", testo, re.I)]
        per, a_tutte = _bonus_dei_talenti(list(dict.fromkeys(altrove)), sistema, effetti, chiave, dv)
    return per, a_tutte



_MEZZOSANGUE = re.compile(r"half[- ]?(?:elf|orc)|mezz['’ ]?(?:elf|orc)|\w+\s*/\s*human|human\s*/\s*\w+", re.I)


def _e_umano(testo: str, nomi) -> bool:
    """Umano, non mezzosangue: il mezzelfo «(elf/human)» e il mezzorco hanno
    sangue umano ma non il talento né i punti abilità in più dell'umano (SRD)."""
    if _MEZZOSANGUE.search(testo):
        return False
    return bool(re.search(rf"\b(?:{'|'.join(nomi)})\b", testo, re.I))


def _razza_srd(dove: str, regole: dict) -> "str | None":
    """Quale delle razze di `[razze]` è la scheda, o None: una sola deve
    combaciare, e nessuna delle «altre» (un duergar è «umanoide (nano)» ma i
    suoi bonus alle abilità non sono quelli del nano)."""
    nomi = regole.get("razze_nomi") or {}
    if any(re.search(rf"\b(?:{n})\b", dove, re.I) for n in nomi.get("altre", [])):
        return None
    if _MEZZOSANGUE.search(dove):
        trovate = [r for r in ("half-elf", "half-orc")
                   if any(re.search(rf"\b(?:{n})\b", dove, re.I) for n in nomi.get(r, []))]
    else:
        trovate = [r for r, v in nomi.items() if r != "altre" and not r.startswith("half-")
                   and any(re.search(rf"\b(?:{n})\b", dove, re.I) for n in v)]
    return trovate[0] if len(trovate) == 1 else None


_RIGA_CA = re.compile(r"^(?:ca-dettaglio:|\W*(?:CA|AC)\b)", re.I)
_MATERIALI = (("mithral", re.compile(r"\bmithr[ai]l", re.I)),
              ("legnoscuro", re.compile(r"\b(?:legno\s*scuro|darkwood)", re.I)))


def _oggetti_della_ca(testo: str, sistema: str) -> "list[list[tuple]]":
    """Per ogni riga della CA con un'armatura o uno scudo della tabella del plugin, le sue voci:
    (tipo, nome, bonus base, Des massima, testo della voce)."""
    from dmcore import classe_armatura as CA
    armature, scudi = CA.tabelle(sistema)
    righe = []
    for riga in testo.splitlines():
        if not _RIGA_CA.search(riga):
            continue
        voci = []
        for v in CA.leggi(riga if "(" in riga else f"({riga})", sistema):
            if v.tipo in ("armatura", "scudo"):
                o = CA._oggetto(v.testo, scudi if v.tipo == "scudo" else armature)
                if o is not None:
                    voci.append((v.tipo, o[0], o[1], o[2], v.testo))
        if voci:
            righe.append(voci)
    return righe


def _penalita_di_prova(testo: str, regole: dict, sistema: str) -> "tuple[int, str]":
    """(penalità minima, da cosa) che armatura e scudo della scheda danno alle prove.

    Si legge la riga della CA, e solo se il file ne ha una sola con un'armatura o
    uno scudo della tabella: con due schede non si sa di chi è la riga delle
    abilità. La penalità è la più bassa possibile: ogni oggetto si conta perfetto
    (−1, ogni armatura magica lo è), il mithral e il legnoscuro tolgono la loro
    parte. Il carico, che può solo alzarla, non si conta."""
    pp = regole.get("penalita_di_prova")
    if not pp:
        return 0, ""
    per_armatura = {(v["ca"], v["des_max"]): v["penalita"] for v in pp["armature"].values()}
    per_scudo = {v["ca"]: v["penalita"] for v in pp["scudi"].values()}
    trovate = []
    for voci in _oggetti_della_ca(testo, sistema):
        tot, nomi = 0, []
        for tipo, nome, ca, des_max, voce in voci:
            piena = per_scudo.get(ca) if tipo == "scudo" else per_armatura.get((ca, des_max))
            if piena is None:
                continue
            meno = next((pp[m] for m, r in _MATERIALI if r.search(voce)), pp["perfetta"])
            tot += max(0, piena - meno)
            nomi.append(nome)
        if nomi:
            trovate.append((tot, ", ".join(nomi)))
    return trovate[0] if len(trovate) == 1 else (0, "")


def abilita(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei gradi delle abilità.

    La scheda scrive il bonus totale, non i gradi: i gradi **minimi** che un
    bonus chiede sono bonus − modificatore della caratteristica chiave − margine
    (sinergia +2, razza) − il bonus dei talenti su quell'abilità. Due regole, tutte e due condizioni necessarie:
      gradi.massimo  i gradi minimi di un'abilità non superano il massimo
                     (3.5: dadi vita + 3; PF1e: dadi vita, più 3 d'abilità di classe)
      gradi.punti    la somma dei gradi minimi non supera i punti abilità che
                     classi e dadi vita razziali danno
    e, per chi ha soltanto livelli di classe tutti con l'elenco nel plugin (3.5):
      gradi.massimo.fuori_classe  un'abilità che non è di nessuna delle sue
                     classi ha il massimo dimezzato, e i suoi gradi costano il doppio
    La penalità di armatura alla prova (lotto 6): l'armatura e lo scudo della riga della CA
    abbassano il bonus scritto delle abilità di forza e destrezza che la subiscono, quindi
    alzano i gradi minimi; si conta la più bassa possibile (oggetti perfetti).
    Con margini larghi vede gli errori grossi, non quelli di un punto."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    f = VT.leggi(p) or {}
    s = L.leggi(p)
    if s is None:
        return [], []
    n_riga, riga = next(((i + 1, m.group(1)) for i, r in enumerate(s.testo.splitlines())
                         if (m := RIGA_ABILITA.search(r)) and re.search(r"[+−-]\d", m.group(1))), (None, None))
    if riga is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    rel = VT_rel(p)
    try:
        regole = S.dati(sistema, "creature.gradi")
    except S.ErroreSistemi as e:
        return [], [{"file": rel, "riga": n_riga, "verifica": "abilita", "regola": "sistema",
                     "testo": str(e), "fonte": sistema}]
    car = {k: v for k, v in s.attributi.items() if isinstance(v, int)}
    dv = sum(g.n for g in s.gruppi)
    livelli = f.get("livelli") or {k: v for k, v in L.livelli_di_classe(s).items()}
    ignote = f.get("classi_ignote") or []
    base = {"file": rel, "riga": n_riga, "verifica": "abilita",
            "fonte": "srd" if sistema == "dnd35" else f"{sistema} prd"}
    if not dv or "Int" not in car:
        return [], [{**base, "regola": "lettura", "testo": "dadi vita o Intelligenza non leggibili"}]
    r = regole["regole"]
    intel = (car["Int"] - 10) // 2
    # il tipo sta nella riga `tipo:` (o «Type»); il più lungo che combacia, perché
    # «monstrous humanoid» contiene «humanoid»
    riga_tipo = next((x for x in s.testo.splitlines() if re.match(r"\W*(?:tipo|type)\b", x, re.I)), s.testo[:400])
    alias = S.dati(sistema, "creature.costruzione").get("alias_tipo", {})
    nomi_tipo = {**{t: t for t in regole["tipi"]}, **{it: en for it, en in alias.items() if en in regole["tipi"]}}
    tipo = next((nomi_tipo[t] for t in sorted(nomi_tipo, key=len, reverse=True)
                 if re.search(rf"\b{re.escape(t)}\b", riga_tipo, re.I)), None)
    # le classi che la lettura dei livelli non conosce ma il plugin dei gradi sì («Druid 9»)
    livelli = dict(livelli)
    for voce in ignote:
        nome, _, n = voce.rpartition(" ")
        livelli[nome] = livelli.get(nome, 0) + int(n)
    razziali = max(0, dv - sum(livelli.values()))
    quote, sconosciute = [], []
    # le abilità di classe (lotto 6 di ADR-0126): si giudica «fuori classe» solo chi ha
    # soltanto livelli di classe, tutti con l'elenco nel plugin; un chierico può avere
    # quelle di ogni dominio, perché i domini non si leggono qui
    elenchi, fuori = regole.get("di_classe") or {}, regole.get("fuori_classe") or {}
    sue: "set[str] | None" = set() if elenchi and fuori and livelli else None
    for classe, n in livelli.items():
        k = classe.lower()
        nomi_classe = (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k))
        elenco = next((elenchi[c] for c in nomi_classe if c in elenchi), None)
        if sue is not None:
            sue = None if elenco is None else sue | set(elenco)
        if sue is not None and "cleric" in nomi_classe:
            sue |= {a for v in (regole.get("di_dominio") or {}).values() for a in v}
        pt = next((x for x in (_punti_di_classe(regole, c) for c in nomi_classe)
                   if x is not None), None)
        if pt is None:
            sconosciute.append(f"{classe} {n}")
        else:
            quote.append((n, pt))
    if razziali:
        if tipo is None:
            sconosciute.append("tipo della creatura")
        else:
            quote.append((razziali, regole["tipi"][tipo]))
    per_dado = [max(r["minimo_per_dado"], pt + intel) for _, pt in quote]
    punti = sum(n * q for (n, _), q in zip(quote, per_dado)) + (r["primo_dado"] - 1) * max(per_dado, default=0)
    umano = _e_umano(s.testo[:1500], ("human", "umano", "umana"))
    punti += (dv + r["primo_dado"] - 1) * r["umano_per_livello"] if umano else 0
    massimo = dv + r["massimo_piu"] + r.get("bonus_di_classe", 0)
    # margine: sinergia o oggetto +2; razza +2 (mostri: +4, o +8 se la scheda parla di bonus razziali).
    # Il bonus dei talenti non è margine: va solo alle abilità che il talento nomina.
    margine = 2 + (8 if re.search(r"razzial|racial", s.testo, re.I) else 4 if razziali else 2)
    chiave = regole["chiave"]
    da_talento, a_tutte = _talenti_d_abilita(f.get("nomi") or [], s.testo, sistema, regole, dv)
    viol, nv, somma, lette = [], [], 0, 0
    voci = []
    for nome, _, bonus in VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
        nome = nome.strip()
        en = _abilita_it().get(LR.norma(nome), nome.lower())
        en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
        if en is not None:
            voci.append((nome, en, bonus))
    # il margine vero (lotto 6 di ADR-0126): per chi ha soltanto livelli di classe ed è di una
    # delle razze dell'SRD, razza e sinergie si contano voce per voce invece del margine fisso
    preciso, scritte = None, {en for _, en, _ in voci}
    if sue is not None and not razziali and regole.get("margine"):
        razza_ = _razza_srd(" ".join((riga_tipo, s.testo.split("\n", 1)[0], p.stem.replace("-", " "))), regole)
        if razza_ is not None and not re.search(r"razzial|racial", s.testo, re.I):
            preciso = regole["razze"].get(razza_, {})
    pp = regole.get("penalita_di_prova") or {}
    penalita, da_armatura = _penalita_di_prova(s.testo, regole, sistema)
    for nome, en, bonus in voci:
        lette += 1
        mod = (car.get(chiave[en], 10) - 10) // 2 if chiave[en] else 0
        talento = max(da_talento.get(en, 0), a_tutte)
        if preciso is not None:
            fonti = [x for x in regole.get("sinergie", {}).get(en, []) if x in scritte]
            margine = regole["margine"]["oggetto"] + preciso.get(en, 0) + regole["margine"]["sinergia"] * len(fonti)
        pen = penalita * (2 if en in pp.get("doppia", ()) else 1) if en in pp.get("abilita", ()) else 0
        minimi = int(bonus.replace("−", "-")) - mod - margine - talento + pen
        if sue is not None and not razziali and not any(a == en or a.startswith(en + " (") for a in sue):
            # fuori classe: il massimo è la metà e ogni grado costa il doppio (SRD, «Skills Summary»)
            tetto = massimo / fuori["massimo_diviso"]
            somma += max(0, minimi) * fuori["costo"]
            if minimi > tetto:
                viol.append({**base, "regola": "gradi.massimo.fuori_classe", "abilita": en,
                             "atteso": f"{tetto:g}", "ha": minimi,
                             "testo": f"{nome} {bonus}: servono almeno {minimi} gradi "
                                      f"(tolti {mod:+d} di caratteristica, {margine} di margine"
                                      + (f" e {talento} dei talenti" if talento else "")
                                      + (f", aggiunti {pen} di penalità di {da_armatura}" if pen else "")
                                      + f"), ma non è un'abilità di nessuna delle sue classi: il massimo è {tetto:g}"})
            continue
        somma += max(0, minimi)
        if minimi > massimo:
            viol.append({**base, "regola": "gradi.massimo", "abilita": en, "atteso": massimo, "ha": minimi,
                         "testo": f"{nome} {bonus}: servono almeno {minimi} gradi "
                                  f"(tolti {mod:+d} di caratteristica, {margine} di margine"
                                  + (f" e {talento} dei talenti" if talento else "")
                                  + (f", aggiunti {pen} di penalità di {da_armatura}" if pen else "")
                                  + f"), il massimo è {massimo}"})
    if sconosciute:
        nv.append({**base, "regola": "gradi.punti", "testo": "punti abilità non calcolabili: "
                   + ", ".join(sconosciute) + " fuori dalle regole del plugin"})
        nv += [{**v, "nota": "classi che la lettura non conosce: il massimo può essere più alto"} for v in viol]
        return [], nv
    if lette and somma > punti:
        viol.append({**base, "regola": "gradi.punti", "atteso": punti, "ha": somma,
                     "testo": f"le abilità scritte chiedono almeno {somma} gradi, "
                              f"classi e dadi vita ne danno {punti}"})
    return viol, nv


# --- incantesimi: sono nella lista della classe, al livello scritto? (ADR-0124 §10) ---

#: «- 5° (3+1): *colpo infuocato* (CD 19), …», «Level 3: Dispel Magic, …», «**2°** — *aiuto*»
RIGA_LIVELLO = re.compile(r"^\s*(?:[-*•]\s*)?\**(?:Level\s+|Livello\s+)?(\d)(?:°|º|st|nd|rd|th)?\**\s*"
                          r"(?:\([^)]*\))?\s*\**\s*[:—–-]\s*(\S.*)$", re.I)
#: come una scheda nomina la classe che lancia
CLASSI_INCANTATRICI = {"chieric": "cleric", "cleric": "cleric", "clr": "cleric", "mag[oa]\\b": "wizard", "wizard": "wizard",
                       "wiz": "wizard", "stregon": "sorcerer", "sorcerer": "sorcerer", "sor\\b": "sorcerer",
                       "bard": "bard", "brd": "bard", "druid": "druid", "drd": "druid", "paladin": "paladin",
                       "pal\\b": "paladin", "ranger": "ranger", "rgr": "ranger"}
TESTA_INCANTESIMI = re.compile(r"incantesimi|spells", re.I)


@lru_cache(maxsize=None)
def _incantesimi_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {LR.norma(v["it"]): v["srd35"] for v in LR.tabella_35() if v["tipo"] == "incantesimo"}


@lru_cache(maxsize=None)
def _liste(sistema: str) -> "tuple[dict, dict, dict, dict]":
    """(classe → {nome normalizzato: livello}, dominio → idem, nome normalizzato →
    nome della fonte, classe → nomi che vengono dai manuali).

    Ordine delle fonti (DM, 2026-11-12): prima la lista dell'SRD, poi quella dei
    manuali 3.5 (`liste_manuali`, da PCGen: solo nomi e livelli). Una classe che
    pesca dalle liste altrui (`liste_prese`: anima prescelta → chierico, accordo
    sublime → bardo, stregone, mago) eredita quelle liste."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    d = S.dati(sistema, "creature.liste_incantesimi")
    nomi: dict = {}

    def piatta(gruppo: dict) -> dict:
        out: dict = {}
        for chiave, livelli in gruppo.items():
            for liv, voci in livelli.items():
                for n in voci:
                    k = LR.norma(n)
                    nomi.setdefault(k, n)
                    out.setdefault(chiave, {})[k] = min(int(liv), out.get(chiave, {}).get(k, 9))
        return out
    liste, domini = piatta(d.get("liste", {})), piatta(d.get("domini", {}))
    dai_manuali: dict = {}
    for chiave, voci in piatta(d.get("liste_manuali", {})).items():
        for k, liv in voci.items():
            if k not in liste.setdefault(chiave, {}):
                liste[chiave][k] = liv
                dai_manuali.setdefault(chiave, set()).add(k)
    # I domini dei manuali hanno un prefisso: valgono solo dove la scheda segna
    # l'incantesimo come di dominio. Senza il segno, un chierico prenderebbe per
    # buono qualunque incantesimo che uno dei 102 domini dei manuali concede.
    for chiave, voci in piatta(d.get("domini_manuali", {})).items():
        for k, liv in voci.items():
            domini.setdefault("manuali:" + chiave, {}).setdefault(k, liv)
    for chiave, altre in d.get("liste_prese", {}).items():
        if chiave in liste and chiave not in altre:
            continue          # ha una lista sua
        for altra in altre:
            for k, liv in liste.get(altra, {}).items():
                if altra == chiave:
                    continue
                mia = liste.setdefault(chiave, {})
                mia[k] = min(liv, mia.get(k, 9))
                if k in dai_manuali.get(altra, ()):
                    dai_manuali.setdefault(chiave, set()).add(k)
    return liste, domini, nomi, dai_manuali


@lru_cache(maxsize=None)
def _classi_dei_manuali(sistema: str) -> "list[tuple[re.Pattern, str]]":
    """Le classi con una lista che l'SRD non ha, come le nomina una scheda: il nome
    inglese e, dove il lessico lo dà, quello italiano. Le più lunghe per prime
    («savage bard» prima di «bard»)."""
    from dmcore import sistemi as S
    try:
        liste = _liste(sistema)[0]
    except S.ErroreSistemi:
        return []
    srd = set(CLASSI_INCANTATRICI.values())
    it = {k: v.get("it") for k, v in (L.T._DATI.get("classi_manuali") or {}).items()} if sistema == "dnd35" else {}
    out = []
    for nome in sorted(liste, key=len, reverse=True):
        if nome in srd or len(nome) < 5 or not re.fullmatch(r"[a-z' -]+", nome):
            continue
        for forma in filter(None, (nome, it.get(nome))):
            # una parola sola («adept», «innato») è anche una parola comune: vale
            # solo con il livello dopo («Adept 5») o come «Healer Spells»
            coda = r"(?!\w)" if " " in forma else r"(?=\s*\**\s*\d|\s+spells\b)"
            out.append((re.compile(r"(?<!\w)" + re.escape(forma) + coda, re.I), nome))
    return out


def _classi_nella_riga(riga: str, sistema: str) -> "set[str]":
    trovate = {v for k, v in CLASSI_INCANTATRICI.items() if re.search(r"\b" + k, riga, re.I)}
    for rx, nome in _classi_dei_manuali(sistema):
        m = rx.search(riga)
        if m:
            # «savage bard» non è anche «bard»
            trovate -= {v for v in trovate if v in m.group(0).lower()}
            return trovate | {nome}
    return trovate


#: quante righe non vuote possono stare fra l'intestazione e la lista («Livello
#: incantatore 14…», «Esempio di preparazione:»)
FRA_TESTA_E_LISTA = 4
CLASSE_CON_LIVELLO = r"\s*\**\s*\d{1,2}\b"


def _classe_che_lancia(righe: "list[str]", i: int, sistema: str = "dnd35") -> "str | None":
    """La classe che lancia la riga i: quella nominata dall'intestazione degli
    incantesimi più vicina sopra; se l'intestazione non la nomina («Prepared
    Spells:»), l'unica classe incantatrice scritta con il suo livello più sopra
    nello stesso blocco («Chierico 12»)."""
    testa = None
    altro = 0
    for j in range(i, max(-1, i - 20), -1):
        r = righe[j]
        if j != i and RIGA_LIVELLO.match(r):
            continue                                   # un'altra riga della lista
        if TESTA_INCANTESIMI.search(r):
            testa = j
            break
        if j != i and r.strip():
            altro += 1
            if altro > FRA_TESTA_E_LISTA or r.lstrip().startswith("#"):
                return None                            # fra la lista e l'intestazione c'è dell'altro
    if testa is None:
        return None
    riga = righe[testa] if testa != i else righe[testa].split("—")[0]
    trovate = _classi_nella_riga(riga, sistema)
    if trovate:
        # «Bardo 8 + Accordo Sublime 1»: la lista è l'unione delle due
        return "+".join(sorted(trovate))
    for j in range(testa - 1, max(-1, testa - 40), -1):
        r = righe[j]
        if re.match(r"\s*(?:---+|\*\*\*+)\s*$", r):
            return None                                # finisce il blocco della creatura
        con_livello = {c for c in _classi_nella_riga(r, sistema)
                       if any(re.search(rx.pattern + CLASSE_CON_LIVELLO, r, re.I)
                              for rx, n in _classi_dei_manuali(sistema) if n == c)
                       or any(re.search(r"\b" + k + r"[a-z]*" + CLASSE_CON_LIVELLO, r, re.I)
                              for k, v in CLASSI_INCANTATRICI.items() if v == c)}
        if con_livello:
            return "+".join(sorted(con_livello))
        if r.lstrip().startswith("#") and j < testa - 1:
            return None
    return None


def incantesimi(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) degli incantesimi scritti per livello.

    Regole: `incantesimo.lista` (l'incantesimo non è nella lista della classe né
    in un dominio), `incantesimo.livello` (è scritto a un livello più basso del
    suo; più alto si accetta, è uno slot superiore o un talento di metamagia).
    Un nome che le liste non hanno (manuali, nomi propri) non è verificabile."""
    testo = p.read_text(encoding="utf-8", errors="replace")
    sistema = VT.sistema_di(p, testo)
    from dmcore import sistemi as S
    try:
        liste, domini, nomi, dai_manuali = _liste(sistema)
    except S.ErroreSistemi:   # il sistema non ha liste di classe
        return [], []
    import lessico_regole as LR
    it = _incantesimi_it() if sistema == "dnd35" else {}
    righe = testo.splitlines()
    viol, nv = [], []
    for i, riga in enumerate(righe):
        m = RIGA_LIVELLO.match(riga)
        if not m or "*" not in m.group(2) and not re.search(r"\bLevel\b", riga):
            continue
        if re.match(r"\d", m.group(2)):      # «1–4: cura, …» è un intervallo, non un livello
            continue
        classe = _classe_che_lancia(righe, i, sistema)
        if classe is None or not all(c in liste for c in classe.split("+")):
            continue
        sua: dict = {}
        for c in classe.split("+"):
            for nome_k, liv in liste[c].items():
                sua[nome_k] = min(liv, sua.get(nome_k, 9))
        manuale = set().union(*(dai_manuali.get(c, set()) for c in classe.split("+")))
        scritto = int(m.group(1))
        di_dominio = False
        for pezzo in re.split(r"[,;]", re.sub(r"\((?:CD|DC)[^)]*\)", "", m.group(2))):
            if re.search(r"\bdomini[oa]\b|\bdomain\b", pezzo, re.I):
                di_dominio = True
            dominio = di_dominio or bool(re.search(r"\((?:D|d)\)|\bD\b\s*$", pezzo))
            nome = re.sub(r"\b(?:domini[oa]|domain)\s*:?|\([^)]*\)|[×x]\s*\d+\b|\bD\s*$", "", pezzo).strip(" *_.·")
            k = LR.norma(nome)
            if not k or len(k) < 3 or re.fullmatch(r"[\d+ /]+", k):
                continue
            k = LR.norma(it[k]) if k in it else k
            base = {"file": VT_rel(p), "riga": i + 1, "verifica": "incantesimi", "incantesimo": nome,
                    "fonte": "prd" if sistema != "dnd35" else
                    "3.5 manuali (PCGen)" if k in manuale else "srd"}
            if k not in nomi:
                nv.append({**base, "regola": "incantesimo.nome", "atteso": None, "ha": None,
                           "testo": f"«{nome}» non è nelle liste del plugin {sistema}"})
                continue
            suo = sua.get(k)
            da_dominio = min((d[k] for n_d, d in domini.items()
                              if k in d and (dominio or not n_d.startswith("manuali:"))), default=None)
            if suo is None and da_dominio is not None and "cleric" in classe.split("+"):
                suo = da_dominio
            elif suo is not None and dominio and da_dominio is not None:
                suo = min(suo, da_dominio)
            if suo is None:
                viol.append({**base, "regola": "incantesimo.lista", "atteso": f"lista {classe}", "ha": "fuori lista",
                             "testo": f"{nomi[k]} non è nella lista {classe}"})
            elif scritto < suo:
                viol.append({**base, "regola": "incantesimo.livello", "atteso": suo, "ha": scritto,
                             "testo": f"{nomi[k]} è di {suo}° livello per {classe}, la scheda lo scrive al {scritto}°"})
    return viol, nv


_LI = re.compile(r"(?:\bLI|\bCL|incantatore di|livello (?:dell['’]\s*)?incantatore)\s*(\d{1,2})", re.I)
_SPECIALISTA = re.compile(r"specialist|scuol[ae] proibit|prohibited school|\b(?:abiurator|ammaliator|divinator|evocator|"
                          r"illusionist|invocator|necromant|trasmutator)", re.I)
_CAR = {"Sag": r"(?:Sag|Wis)", "Int": r"Int", "Car": r"(?:Car|Cha)"}


def _testa_della_lista(righe: "list[str]", i: int) -> "int | None":
    """L'intestazione degli incantesimi sopra la riga i (come `_classe_che_lancia`)."""
    altro = 0
    for j in range(i, max(-1, i - 20), -1):
        r = righe[j]
        if j == i or RIGA_LIVELLO.match(r):
            continue                 # una riga della lista non è l'intestazione, anche se nomina «incantesimi»
        if TESTA_INCANTESIMI.search(r):
            return j
        if r.strip():
            altro += 1
            if altro > FRA_TESTA_E_LISTA or r.lstrip().startswith("#"):
                return None
    return None


def _livello_scritto(riga: str, classe: str) -> "int | None":
    """Il livello di `classe` scritto nella riga. «conosciuti e al giorno da
    stregone 9» vince su «Stregone 6»: è la scheda che dice con quale riga
    della tabella lancia (un mostro che somma i livelli innati)."""
    nomi = [k for k, v in CLASSI_INCANTATRICI.items() if v == classe]
    for k in nomi:
        m = re.search(r"(?:conosciuti|al giorno)[^;:)]*?\bda\s+" + k + r"[a-z]*\s*(\d{1,2})\b", riga, re.I)
        if m:
            return int(m.group(1))
    for k, v in CLASSI_INCANTATRICI.items():
        if v == classe:
            m = re.search(r"\b" + k + r"[a-z]*\s*(?:di\s*)?\**\s*(\d{1,2})\b", riga, re.I)
            if m:
                return int(m.group(1))
    return None


def _punteggio_che_lancia(righe: "list[str]", testa: int, car: str) -> "int | None":
    """Il punteggio della caratteristica: quello che l'intestazione dichiara
    («con Sag 24»), altrimenti la riga delle caratteristiche più vicina nella
    stessa sezione, sopra e poi sotto. Le righe «era:» sono numeri vecchi."""
    rx = re.compile(r"\b" + _CAR[car] + r"\b\s*\**:?\s*(\d{1,2})\b", re.I)
    pezzo = righe[testa][TESTA_INCANTESIMI.search(righe[testa]).start():]
    m = rx.search(pezzo)
    if m:
        return int(m.group(1))
    intera = re.compile(r"\b(?:For|Str)\b\s*\**:?\s*\d", re.I)
    for passo, limite in ((-1, 80), (1, 40)):
        j = testa
        for _ in range(limite):
            j += passo
            if not 0 <= j < len(righe) or righe[j].lstrip().startswith("#"):
                break
            m = rx.search(righe[j])
            if m and intera.search(righe[j]) and not re.search(r"\bera\b", righe[j][:m.start()]):
                return int(m.group(1))
    return None


def incantatori(p: Path) -> "tuple[list[dict], list[dict]]":
    """Incantesimi al giorno, conosciuti, livello massimo e CD (ADR-0126, lotto 3).

    Regole `numero.incantesimi.al_giorno`, `.conosciuti`, `.livello`, `.cd`. Una
    lista di cui non si legge la classe, il livello o la caratteristica torna fra
    i non verificabili, una volta per lista."""
    from dmcore import magia as M
    from dmcore import sistemi as S
    testo = p.read_text(encoding="utf-8", errors="replace")
    sis = VT.sistema_di(p, testo)
    try:
        M.tabelle(sis)
    except S.ErroreSistemi:
        return [], []
    righe = testo.splitlines()
    viol, nv = [], []
    liste: "dict[int, dict | None]" = {}
    fonte = "srd" if sis == "dnd35" else "prd"

    def nota(riga: int, perche: str) -> None:
        nv.append({"file": VT_rel(p), "riga": riga + 1, "verifica": "incantatori", "regola": "numero.incantesimi",
                   "fonte": fonte, "testo": perche})

    for i, riga in enumerate(righe):
        m = M.RIGA.match(riga)
        if not m or "*" not in m.group("resto") or re.match(r"\d", m.group("resto")):
            continue
        testa = _testa_della_lista(righe, i)
        if testa is None:
            continue
        if testa not in liste:
            liste[testa] = None
            classe = _classe_che_lancia(righe, i, sis)
            if classe is None:
                nota(testa, "non si legge quale classe lancia questa lista")
                continue
            if M.classe(classe, sis) is None:
                nota(testa, f"«{classe}» non ha una tabella degli incantesimi nel plugin {sis}")
                continue
            dati = M.classe(classe, sis)
            t = righe[testa]
            pezzo = t[TESTA_INCANTESIMI.search(t).start():]
            li = _LI.search(pezzo)
            livello = _livello_scritto(pezzo, classe) or (int(li.group(1)) if li else None)
            # una classe di prestigio alza il livello con cui la lista si lancia (ADR-0126, lotto 3-ter)
            pr = _prestigio_nel_tipo(righe, testa, classe, sis)
            if pr and not (livello and _livello_scritto(pezzo, classe) is None and classe in ("paladin", "ranger")):
                base, piu, parti, dubbio = pr
                come = f"{classe} {base} + " + " + ".join(parti) if parti else f"{classe} {base}, nessun livello in più"
                if dubbio:
                    if livello != base + piu:
                        nota(testa, f"livello d'incantatore non giudicabile ({come}): {dubbio}")
                elif livello is None:
                    livello = base + piu
                elif livello != base + piu:
                    viol.append({"file": VT_rel(p), "riga": testa + 1, "verifica": "incantatori", "fonte": fonte,
                                 "regola": "numero.incantesimi.livello_incantatore", "atteso": base + piu, "ha": livello,
                                 "testo": f"la lista si lancia da {classe} {livello}, le classi danno {base + piu} ({come})"})
            if livello is None:
                for j in range(testa - 1, max(-1, testa - 40), -1):
                    if righe[j].lstrip().startswith("#") or re.match(r"\s*(?:---+|\*\*\*+)\s*$", righe[j]):
                        break
                    livello = _livello_scritto(righe[j], classe)
                    if livello:
                        break
            if not livello:
                nota(testa, f"non si legge il livello di {classe}")
                continue
            punti = _punteggio_che_lancia(righe, testa, dati["caratteristica"])
            if punti is None:
                nota(testa, f"non si legge {dati['caratteristica']}, la caratteristica che lancia")
                continue
            intorno = "\n".join(righe[max(0, testa - 60):testa + 60])
            foc = (2 if re.search(r"Focalizzat[oi] Superior|Greater Spell Focus", intorno, re.I)
                   else 1 if re.search(r"Incantesimi Focalizzati|Spell Focus", intorno, re.I) else 0)
            spec = classe == "wizard" and bool(_SPECIALISTA.search(intorno))
            var = dati.get("variante_del_dm")
            liste[testa] = {"classe": classe, "livello": livello, "punti": punti, "foc": foc, "testa": testa,
                            "prove": [(M.al_giorno(classe, livello, punti, x, spec), M.conosciuti(classe, livello, x), [])
                                      for x in ([sis, var] if var else [sis])],
                            "variante": var, "car": dati["caratteristica"]}
            scritti = M.leggi_al_giorno(pezzo)
            if scritti:
                da_zero = dati["al_giorno"]["20"][0] >= 0
                for attesi, _, scarti in liste[testa]["prove"]:
                    scarti += [(testa, {"campo": "incantesimi.al_giorno", "scritto": x["scritto"], "atteso": x["atteso"],
                                        "nota": f"incantesimi al giorno di {x['livello']}°, tabella più incantesimi bonus"})
                               for x in M.giudica_dichiarati(scritti, attesi, da_zero)]
        lista = liste[testa]
        if lista is None:
            continue
        for attesi, noti, scarti in lista["prove"]:
            scarti += [(i, x) for x in M.giudica_riga(int(m.group("liv")), m.group("par") or "", m.group("resto"),
                                                      attesi, noti, lista["punti"], lista["foc"])]
    for lista in filter(None, liste.values()):
        scarti = lista["prove"][0][2]
        chi = f"{lista['classe']} {lista['livello']}, {lista['car']} {lista['punti']}"
        if lista["variante"] and scarti and not [x for _, x in lista["prove"][1][2] if x["campo"] != "incantesimi.cd"]:
            # la scheda segue la tabella che il DM ha scelto per questa classe: è una forma
            # ibrida dichiarata, va nel registro delle regole custom (D-B-ter, lotto 11)
            if any(x["campo"] != "incantesimi.cd" for _, x in scarti):
                nv.append({"file": VT_rel(p), "riga": lista["testa"] + 1, "verifica": "incantatori", "fonte": fonte,
                           "regola": "numero.incantesimi.variante",
                           "testo": f"{chi}: gli slot e i conosciuti seguono la tabella {lista['variante']} scelta dal DM "
                                    f"per questa classe, non quella del {sis}: forma ibrida da registrare"})
            scarti = [(r, x) for r, x in scarti if x["campo"] == "incantesimi.cd"]
        for r, x in scarti:
            viol.append({"file": VT_rel(p), "riga": r + 1, "verifica": "incantatori", "fonte": fonte,
                         "regola": f"numero.{x['campo']}", "atteso": x["atteso"], "ha": x["scritto"],
                         "testo": f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']}; {chi})"})
    return viol, nv


def _prestigio_nel_tipo(righe: "list[str]", testa: int, classe: str,
                        sistema: str) -> "tuple[int, int, list[str], str | None] | None":
    """(livelli di `classe`, livelli in più, come, dubbio) dalla riga `tipo:` sopra
    la lista, se nomina `classe` e almeno una classe di prestigio. None altrimenti."""
    from dmcore import prestigio as PR
    tipo = next((righe[j] for j in range(testa, -1, -1) if righe[j].lstrip().lower().startswith("tipo:")), None)
    if tipo is None:
        return None
    base, prestigi, altre = 0, [], []
    for pezzo in re.split(r"[,/]", tipo.split(":", 1)[1]):
        m = re.match(r"\s*([A-Za-zÀ-ú' -]+?)\s+(\d{1,2})\b", pezzo)
        if not m:
            continue
        nome, n = m.group(1).strip(), int(m.group(2))
        en = _prestigio_en(nome, sistema)
        if en:
            prestigi.append((en, n))
            continue
        k = nome.lower()
        lancia = "wizard" if k in VT.SPECIALISTI else next(
            (v for rx, v in CLASSI_INCANTATRICI.items() if re.match(rx, k)), None)
        if lancia == classe:
            base += n
        elif lancia:
            altre.append(lancia)
    if not prestigi or not base:
        return None
    return (base, *PR.avanzamento(classe, prestigi, altre, sistema))


def _prestigio_en(nome: str, sistema: str) -> "str | None":
    """Il nome inglese della classe di prestigio, se il plugin ne ha i requisiti."""
    from dmcore import prestigio as PR
    k = nome.strip().lower()
    return next((c for c in (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k)) if PR.classe(c, sistema)), None)


def _gradi_che_il_bonus_regge(s: "L.Scheda", sistema: str) -> "tuple[dict[str, int], set[str]] | None":
    """{abilità: bonus scritto − modificatore di caratteristica} e le abilità di
    Forza e Destrezza, dove la penalità di armatura può nascondere dei gradi."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    from dmcore.magia import mod as M_mod
    riga = next((m.group(1) for r in s.testo.splitlines()
                 if (m := RIGA_ABILITA.search(r)) and re.search(r"[+−-]\d", m.group(1))), None)
    if riga is None:
        return None
    chiave = S.dati(sistema, "creature.gradi")["chiave"]
    car = {k: v for k, v in s.attributi.items() if isinstance(v, int)}
    regge: dict[str, int] = {}
    for nome, _, bonus in VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
        en = _abilita_it().get(LR.norma(nome.strip()), nome.strip().lower())
        en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
        if en is None:
            continue
        mod = M_mod(car.get(chiave[en], 10)) if chiave[en] else 0
        regge[en] = max(regge.get(en, -99), int(bonus.replace("−", "-")) - mod)
    return regge, {k for k, c in chiave.items() if c in ("For", "Des")}


def prestigio(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei requisiti delle classi di prestigio
    (ADR-0126, lotto 3-bis). Regole `prestigio.bab`, `.gradi.massimo`, `.gradi`,
    `.talenti`, `.razza`, `.allineamento`, `.incantesimi`; i requisiti che non
    si riducono a un numero vanno fra i non verificabili (`prestigio.speciali`)."""
    import lessico_regole as LR
    from dmcore import prestigio as PR
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    f = VT.leggi(p) or {}
    sistema = VT.sistema_di(p, s.testo)
    livelli = dict(f.get("livelli") or L.livelli_di_classe(s))
    ignote = []
    for voce in f.get("classi_ignote") or []:
        nome, _, n = voce.rpartition(" ")
        livelli[nome.lower()] = livelli.get(nome.lower(), 0) + int(n)
        ignote.append(nome.lower())
    righe = s.testo.splitlines()
    n_riga = next((i + 1 for i, r in enumerate(righe) if r.lower().startswith("tipo:")), 1)
    base = {"file": VT_rel(p), "riga": n_riga, "verifica": "prestigio"}
    try:
        dati = PR.requisiti(sistema)
    except S.ErroreSistemi:
        dati = None
    costruzione = S.dati(sistema, "creature.costruzione")
    di_prestigio = {**costruzione.get("prestigio", {}),
                    **{k: v for k, v in costruzione.get("classi_manuali", {}).items() if v.get("prestigio")}}
    viol, nv = [], []
    for nome, n in livelli.items():
        k = nome.lower()
        en = _prestigio_en(nome, sistema) if dati else None
        if en is None:
            if any(c in di_prestigio for c in (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k))):
                nv.append({**base, "regola": "prestigio", "fonte": sistema,
                           "testo": f"{nome} {n}: classe di prestigio senza requisiti nel plugin {sistema}"})
            continue
        req = PR.classe(en, sistema)
        tot = max(sum(g.n for g in s.gruppi), sum(livelli.values()))
        altri = [g for g in s.gruppi if g.nome.lower() != k]
        bab_prima = None
        if s.composizione_nota and len(altri) == len(s.gruppi) - 1 and sum(g.n for g in s.gruppi) == tot <= 20:
            bab_prima = PR.bab_di(altri)
        gradi = _gradi_che_il_bonus_regge(s, sistema)
        scritti = (f.get("talenti") or []) + (f.get("senza_regole") or [])
        fatti = {
            "bab_prima": bab_prima,
            "gradi_massimi": tot - n + S.dati(sistema, "creature.gradi")["regole"]["massimo_piu"],
            "abilita": gradi[0] if gradi else None, "incerte": gradi[1] if gradi else (),
            "talenti": {PR.senza_parentesi(x["en"]) for x in scritti}
                       | {PR.senza_parentesi(x) for x in VT.talenti_concessi({c: v for c, v in livelli.items() if c != nome})},
            "talenti_ignoti": bool(f.get("ignoti")) or not f,
            "razza": s.tipo or "",
            "razze_it": {v["srd35"].lower(): (v["it"].lower(),) for v in LR.tabella_35() if v["tipo"] == "razza"},
            "allineamento": (f.get("fisici") or VT.fatti_fisici(s))["allineamento"],
            "classi": {x: v for c, v in livelli.items() if c != nome for x in (c, VT.T._ALIAS.get(c, c))},
            "car": {k: v for k, v in s.attributi.items() if isinstance(v, int)},
            "classi_ignote": any(c in ignote or c in di_prestigio or _classi_it().get(c, c) in di_prestigio
                                 for c in livelli if c != nome),
        }
        scarti, incerti = PR.giudica(req, fatti, sistema)
        chi = f"{nome} {n}"
        if req.get("diverge"):      # più libri danno requisiti diversi: lo scarto è un dubbio
            incerti = [{**x, "nota": x["nota"] + " (la classe ha requisiti diversi in più manuali)"}
                       for x in scarti] + incerti
            scarti = []
        for x in scarti:
            viol.append({**base, "fonte": req["fonte"], "regola": f"prestigio.{x['campo']}",
                         "atteso": x["atteso"], "ha": x["scritto"], "testo": f"{chi}: {x['nota']}"})
        for x in incerti:
            nv.append({**base, "fonte": req["fonte"], "regola": f"prestigio.{x['campo']}",
                       "testo": f"{chi}: {x['nota']}"})
    return viol, nv


#: un talento che la scheda dichiara fuori dal conto per livello: «(B)» del mostro,
#: «(razziale)», «[dominio]», «(difetto)», «(tratto)»
_FUORI_CONTO = re.compile(r"\(B\)|razzial|racial|domini|domain|difett|flaw|tratt[oi]\b|\btrait", re.I)


def numero_talenti(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) del numero dei talenti (ADR-0126, lotto 4).

    I talenti scritti, tolti quelli che la classe concede per nome e quelli che
    la scheda dichiara fuori dal conto, devono essere quanti ne danno i dadi
    vita e i talenti bonus delle classi (`dmcore.talenti`), più quello
    dell'umano. Regola `numero.talenti`: di più è una violazione, di meno pure
    (uno slot non speso). Con una classe di cui il plugin non conosce i talenti
    bonus il conto resta un dubbio."""
    from dmcore import sistemi as S
    f = VT.leggi(p)
    s = L.leggi(p)
    if f is None or s is None:
        return [], []
    sistema, T = f["sistema"], VT.T
    costruzione = S.dati(sistema, "creature.costruzione")
    in_piu = costruzione.get("talenti_in_piu", {})
    bonus = T.dati(sistema)["bonus"]
    livelli: dict[str, int] = {}
    for k, v in f["livelli"].items():
        k = k if k in bonus else T._ALIAS.get(k, k) if T._ALIAS.get(k, k) in bonus else k
        livelli[k] = livelli.get(k, 0) + v
    note = set(costruzione.get("classi", {})) | set(bonus)
    ignote = list(f["classi_ignote"]) + [k for k in livelli if k not in note and T._ALIAS.get(k, k) not in note]
    tot = max(f["dv"], L.dv_totali(s.testo) or 0, sum(livelli.values()))
    # la composizione dei dadi vita non letta, o un umanoide con più di tre dadi «razziali» e
    # nessuna classe: sono livelli di una classe che la lettura non ha visto
    if not s.composizione_nota or any(g.nome == "classe non dichiarata" for g in s.gruppi) or (
            not livelli and any(g.nome == "humanoid" and g.n > 3 for g in s.gruppi)):
        ignote.append("una classe non letta")
    en_di = {c: (c if c in T.CLASSI_EN_IT else T._ALIAS.get(c, c)) for c in livelli}
    concessi = {PR_senza(t) for _, t in T.concessi(sistema, livelli)} | {PR_senza(t) for t in VT.talenti_concessi(livelli)}
    for d in in_piu.get("domini", {}).values():
        if any(livelli.get(c) or livelli.get(T._ALIAS.get(c, c)) for c in d["classi"]) and re.search(
                rf"(?:domin\w+|domains?)\b[^\n]*\b(?:{'|'.join(d['nomi'])})\b", s.testo, re.I):
            concessi |= {PR_senza(t) for t in d["talenti"]}
    contati, fuori, ignoti = 0, 0, 0
    for nome in f["nomi"]:
        r = VT.risolvi(sistema, nome)
        if _FUORI_CONTO.search(nome):
            fuori += 1
        elif r and PR_senza(r["en"]) in concessi:
            fuori += 1
        elif r is None and (len(nome.split()) > 6 or re.search(r"[.:;«»]|\b(?:era|sono|non|che)\b", nome)):
            ignoti += 1          # prosa finita nella riga, non un nome: il conto resta un dubbio
        else:
            contati += 1         # anche un nome che la lettura non conosce è un talento scritto
    minimo = T.generali(sistema, tot) + len(T.bonus_di_classe(sistema, livelli))
    umano = _e_umano(s.tipo or "", in_piu.get("razza_umana", ["human"]))
    minimo += in_piu.get("umano", 0) if umano else 0
    massimo = minimo + sum(1 for c, n in livelli.items()
                           for lv in in_piu.get("capacita_o_talento", {}).get(en_di[c], ()) if lv <= n)
    base = {"file": f["file"], "riga": f["riga"], "verifica": "numero_talenti", "regola": "numero.talenti",
            "fonte": "srd" if sistema == "dnd35" else f"{sistema} prd"}
    atteso = str(minimo) if minimo == massimo else f"{minimo}-{massimo}"
    come = (f"{T.generali(sistema, tot)} per {tot} dadi vita, {len(T.bonus_di_classe(sistema, livelli))} bonus di classe"
            + (", 1 da umano" if umano and in_piu.get("umano") else "")
            + (f"; {fuori} fuori dal conto (concessi dalla classe o dichiarati)" if fuori else ""))
    if minimo <= contati <= massimo:
        return [], []
    testo = (f"la scheda conta {contati} talenti, la regola ne dà {atteso} ({come})")
    if ignote:
        return [], [{**base, "testo": testo + f"; i talenti bonus di {', '.join(ignote)} non sono nel plugin"}]
    if ignoti:
        return [], [{**base, "testo": testo + f"; la riga ha {ignoti} voci di prosa che non si contano"}]
    if contati > massimo:
        testo += "; un talento fuori dal conto va dichiarato accanto al nome: (B), (razziale), (dominio), (difetto)"
    return [{**base, "atteso": atteso, "ha": contati, "testo": testo}], []


def PR_senza(nome: str) -> str:
    return re.sub(r"\s*\(.*$", "", nome).strip().lower()


def classe_armatura(p: Path) -> "tuple[list[dict], list[dict]]":
    """La CA dei recinti della scheda, ricostruita dalle sue voci (ADR-0126, lotto 1-bis)."""
    import conformita_statblocchi as C
    from dmcore import classe_armatura as CA
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    if sis != "dnd35":
        return [], []          # il PF1e ha già contatto, sprovvista e DMC nel cancello dei moduli
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    righe = testo.split("\n")
    for b in blocchi:
        sb = b["sb"]
        riga = next((i + 1 for i in range(b["riga"] - 1, min(len(righe), b["riga"] + 40))
                     if righe[i].startswith("ca:")), b["riga"])
        scarti, non = CA.giudica(C._int(sb.ca), sb.ca_dettaglio or "",
                                 C._mod_caratteristica(sb.attributi or "", "Des"), testo, sis)
        base = {"file": VT_rel(p), "riga": riga, "verifica": "numeri", "fonte": "srd"}
        for x in scarti:
            viol.append(dict(base, regola=f"numero.{x['campo']}", atteso=x["atteso"], ha=x["scritto"],
                             testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
        for x in non:
            nv.append(dict(base, regola="numero.CA", testo=x["nota"]))
        # sensi e CD: gli stessi conti che il cancello dei moduli fa sui recinti dei master
        for x in C.conti_del_recinto(b, {}, sis):
            if x["campo"] == "sensi" or x["campo"].startswith("CD"):
                campo = x["campo"].replace(" ", "_")
                viol.append(dict(base, riga=b["riga"], regola=f"numero.{campo}", atteso=x["atteso"],
                                 ha=x["scritto"],
                                 testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
    return viol, nv


_FONTE_SCHEDA = re.compile(r"\*\*(?:Source|Fonte)\*\*\s*:?\s*([^|\n]*)", re.I)
_TAGLIE_IT = {"minuscola": "Fine", "minuta": "Diminutive", "piccolissima": "Tiny", "piccola": "Small",
              "media": "Medium", "grande": "Large", "enorme": "Huge", "mastodontica": "Gargantuan",
              "colossale": "Colossal"}
_TIPI_IT = {"gigante": "giant", "umanoide mostruoso": "monstrous humanoid", "umanoide": "humanoid",
            "bestia magica": "magical beast", "animale": "animal", "aberrazione": "aberration",
            "esterno": "outsider", "non morto": "undead", "costrutto": "construct", "drago": "dragon",
            "elementale": "elemental", "folletto": "fey", "melma": "ooze", "vegetale": "plant",
            "parassita": "vermin"}


def _base_del_blocco(testo: str, sb, un_blocco: bool, sistema: str) -> "tuple[str, dict, bool] | None":
    """(nome, voce, stessa taglia) della creatura base che la scheda dichiara, o None.

    La dichiara la riga della fonte («SRD *Ogre* + …», solo se il file ha un
    blocco solo). Il sottotipo non basta: un flind è «umanoide (gnoll)» e non è
    uno gnoll. Un drago vero (col colore scritto) ha per base la sua taglia.
    Vale solo se il tipo della base è quello del blocco: «MM Rakshasa + Rogue 3»
    su un umanoide è il cultista di un rakshasa, non un rakshasa."""
    from dmcore import creature_base as CB
    tipo_ = (sb.tipo or "").lower()
    for it, en in _TIPI_IT.items():
        tipo_ = tipo_.replace(it, en)
    dove = (sb.taglia or "").lower() + " " + tipo_
    taglia = next((en for it, en in _TAGLIE_IT.items() if re.search(rf"\b{it}\b", dove)), None) or next(
        (t for t in _TAGLIE_IT.values() if re.search(rf"\b{t.lower()}\b", dove)), None)
    trovata = None
    if un_blocco:
        m = _FONTE_SCHEDA.search(testo)
        trovata = CB.dichiarata(m.group(1), sistema) if m else None
    if trovata is None and ("dragon" in tipo_ or (not tipo_ and un_blocco)):
        # un drago vero: il colore sta nel tipo o, con un blocco solo, nel titolo della scheda
        trovata = CB.drago((sb.tipo or "") + (" " + testo.split("\n", 1)[0] if un_blocco else ""), taglia, sistema)
        if trovata:
            return trovata[0], trovata[1], True
    if trovata is None or trovata[1]["tipo"] not in tipo_:
        return None
    return trovata[0], trovata[1], taglia == trovata[1]["taglia"]


def creatura_base(p: Path) -> "tuple[list[dict], list[dict]]":
    """Dadi vita razziali e armatura naturale della creatura base dichiarata (ADR-0126, lotto 5)."""
    import conformita_statblocchi as C
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    for b in blocchi:
        sb = b["sb"]
        trovata = _base_del_blocco(testo, sb, len(blocchi) == 1, sis)
        if trovata is None:
            continue
        nome, voce, stessa = trovata
        if "dv" not in voce:
            continue               # un drago vero: dalla taglia vengono solo gli attacchi
        base = {"file": VT_rel(p), "riga": b["riga"], "verifica": "creatura_base", "fonte": "srd"}
        # dadi vita razziali: «4d8» dell'ogre deve stare nei dadi scritti
        dadi = " ".join(x for x in (sb.pf_dado or "", sb.tipo or "") if x)
        scritti = re.findall(r"(\d+)d(\d+)", dadi)
        if scritti and isinstance(voce["dv"], int):
            if (str(voce["dv"]), str(voce["dado"])) not in scritti:
                viol.append(dict(base, regola="numero.dv.razziali", atteso=f"{voce['dv']}d{voce['dado']}",
                                 ha="+".join(f"{n}d{f}" for n, f in scritti),
                                 testo=f"dadi vita {'+'.join(f'{n}d{f}' for n, f in scritti)}: la creatura base "
                                       f"{nome} porta {voce['dv']}d{voce['dado']} razziali"))
        elif not scritti:
            nv.append(dict(base, regola="numero.dv.razziali",
                           testo=f"la scheda non scrive i dadi vita: i {voce['dv']}d{voce['dado']} di {nome} non si riscontrano"))
        # armatura naturale: la base, se la taglia è la stessa
        nat = re.search(r"([+-]?\d+)\s*(?:naturale|natural|nat\b)", (sb.ca_dettaglio or "").replace("−", "-"), re.I)
        if nat and stessa:
            ha = int(nat.group(1))
            if ha != voce["naturale"]:
                viol.append(dict(base, regola="numero.CA.naturale", atteso=voce["naturale"], ha=ha,
                                 testo=f"armatura naturale {ha:+d}: la creatura base {nome} ha {voce['naturale']:+d} "
                                       f"(un bonus in più va dichiarato con la sua sorgente)"))
        elif nat and not stessa:
            nv.append(dict(base, regola="numero.CA.naturale",
                           testo=f"taglia diversa da quella di {nome} ({voce['taglia']}): l'armatura naturale non si riscontra"))
    return viol, nv


def grado_di_sfida(p: Path) -> "tuple[list[dict], list[dict]]":
    """Il grado di sfida scritto contro quello che danno livelli, razza e creatura base (ADR-0126, lotto 5)."""
    import conformita_statblocchi as C
    from dmcore import gs as GS
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    # il grado si legge dalla riga del blocco: «1/2» resta una frazione
    m = re.search(r"^\s*gs\s*:\s*(\d+\s*/\s*\d+|\d+(?:[.,]\d+)?)\s*$", s.testo, re.M | re.I)
    ha = GS.frazione(m.group(1).replace(" ", "")) if m else None
    if ha is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    tabella = S.dati(sistema, "creature.costruzione").get("gs")
    if not tabella:
        return [], []
    righe = s.testo.splitlines()
    n_riga = next((i + 1 for i, r in enumerate(righe) if re.match(r"\s*gs\s*:", r, re.I)), 1)
    base = {"file": VT_rel(p), "riga": n_riga, "verifica": "grado_di_sfida", "fonte": sistema}
    f = VT.leggi(p) or {}
    it = _classi_it()
    livelli: dict[str, int] = {}
    for nome, n in dict(f.get("livelli") or L.livelli_di_classe(s)).items():
        en = it.get(nome.lower(), nome.lower())
        livelli[en] = livelli.get(en, 0) + n
    for voce in f.get("classi_ignote") or []:
        nome, _, n = voce.rpartition(" ")
        livelli[nome.lower()] = livelli.get(nome.lower(), 0) + int(n)
    # le classi che il `tipo` nomina e nessuna tabella conosce (di prestigio, dei manuali): livelli da PG
    tipo = (s.tipo or "")
    for nome, n in re.findall(r"(?:^|[,/])\s*([A-Za-zÀ-ú' -]+?)\s+(\d+)(?=\s*(?:[,/(]|$))", tipo):
        k = re.sub(r"^ex[- ]", "", nome.strip().lower())
        en = "wizard" if k in VT.SPECIALISTI else it.get(k, VT.T._ALIAS.get(k, k))
        if en not in livelli and k not in livelli and k.split()[-1] not in livelli and it.get(k.split()[-1]) not in livelli:
            livelli[en] = int(n)
    if not s.composizione_nota:
        return [], [dict(base, regola="numero.gs",
                         testo="la scheda non scrive la composizione dei dadi vita: il grado di sfida non si ricostruisce")]
    classi_nei_gruppi = sum(g.n for g in s.gruppi
                            if it.get(g.nome.lower(), L._P.ABBREVIAZIONI.get(g.nome.lower(), g.nome.lower())) in livelli
                            or g.nome.lower() in livelli)
    dv_razziali = sum(g.n for g in s.gruppi) - classi_nei_gruppi
    # una classe che la lettura dei dadi non conosce lascia i suoi dadi al tipo: sono livelli, non dadi razziali
    dv_razziali = max(0, dv_razziali - max(0, sum(livelli.values()) - classi_nei_gruppi))
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(s.testo))
    trovata = _base_del_blocco(s.testo, blocchi[0]["sb"], len(blocchi) == 1, sistema) if blocchi else None
    dove = " ".join((s.tipo or "", righe[0] if righe else "", p.stem.replace("-", " ")))
    voce = trovata[1] if trovata else None
    if voce is None and dv_razziali > 1:
        # per il grado di sfida basta il nome: lo confermano il tipo e, in `GS.atteso`, i dadi vita razziali
        from dmcore import creature_base as CB
        tipo_en = (s.tipo or "").lower()
        for it_, en_ in _TIPI_IT.items():
            tipo_en = tipo_en.replace(it_, en_)
        for come, chiave in CB._nomi(sistema):
            v = CB.tabella(sistema)[chiave]
            if re.search(rf"\b{re.escape(come)}s?\b", dove, re.I) and v.get("tipo") and v["tipo"] in tipo_en \
                    and "dv" in v and v.get("gs") is not None:
                voce = v
                break
    esito = GS.atteso(livelli, dv_razziali, voce, dove, tabella)
    if "perche" in esito:
        return [], [dict(base, regola="numero.gs", testo=esito["perche"])]
    if esito["min"] <= ha <= esito["max"]:
        return [], []
    atteso = GS.scritto(esito["min"]) if esito["min"] == esito["max"] else (
        f"da {GS.scritto(esito['min'])} a {GS.scritto(esito['max'])}")
    return [dict(base, regola="numero.gs", atteso=atteso, ha=GS.scritto(ha),
                 testo=f"grado di sfida {GS.scritto(ha)}, la regola dà {atteso} ({esito['conto']}); "
                       f"uno scarto va dichiarato con la sua ragione")], []


def danno(p: Path) -> "tuple[list[dict], list[dict]]":
    """Dado, bonus e critico delle armi della tabella (ADR-0126, lotto 2)."""
    import conformita_statblocchi as C
    from dmcore import danno as D
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    if sis != "dnd35":
        return [], []          # le armi del PF1e fuori dal manuale base arrivano col lotto 10
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    righe = testo.split("\n")
    for i, b in enumerate(blocchi):
        sb = b["sb"]
        # i talenti stanno nel recinto o nella prosa che lo segue: fino al recinto dopo
        fine = blocchi[i + 1]["riga"] - 1 if i + 1 < len(blocchi) else len(righe)
        intorno = testo if len(blocchi) == 1 else "\n".join(righe[b["riga"] - 1:fine])
        scudo = bool(re.search(r"scudo|shield|buckler|brocchiere", sb.ca_dettaglio or "", re.I))
        mod_for = C._mod_caratteristica(sb.attributi or "", "For")
        for att in sb.attacchi:
            riga = next((n + 1 for n in range(b["riga"] - 1, min(len(righe), b["riga"] + 60))
                         if att.strip()[:40] in righe[n]), b["riga"])
            base = {"file": VT_rel(p), "riga": riga, "verifica": "numeri", "fonte": "srd"}
            trovata = _base_del_blocco(testo, sb, len(blocchi) == 1, sis)
            scarti, non = D.giudica(att, mod_for, sb.tipo or "", intorno, scudo, sb.ca_dettaglio or "", sis,
                                    creatura=trovata[:2] if trovata and trovata[2] else None)
            for x in scarti:
                viol.append(dict(base, regola=f"numero.{x['campo']}", atteso=x["atteso"], ha=x["scritto"],
                                 testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
            for x in non:
                nv.append(dict(base, regola="numero.danno", testo=x["nota"]))
    return viol, nv


#: «**Vista cieca (Str)**», «- **Aura di paura (Sop)**:», «Spell Resistance (Su)»
_CAPACITA = re.compile(r"(?:\*{1,2}|_{1,2})\s*([^*_()]{2,70}?)\s*\((Str|Sop|Mag|Ex|Su|Sp)\)\s*(?:\*{1,2}|_{1,2})|"
                       r"(?:\*{1,2}|_{1,2})\s*([^*_()]{2,70}?)\s*(?:\*{1,2}|_{1,2})\s*\((Str|Sop|Mag|Ex|Su|Sp)\)|"
                       r"^#{1,6}\s*([^*_()#]{2,70}?)\s*\((Str|Sop|Mag|Ex|Su|Sp)\)")
#: l'etichetta di una sezione di prosa: titolo («### Tattiche») o grassetto a inizio riga («**Tattiche**:»)
_SEZIONE = re.compile(r"^\s*(?:[-*•]\s+)?(?:#{1,6}\s*|\*\*\s*)(Tattiche|Tactics|Descrizione|Description)\b", re.I)
_TITOLO = re.compile(r"^\s*(?:#{1,6}\s|---+\s*$)")
_ALTRA_SEZIONE = re.compile(r"^\s*(?:#{1,6}\s|\*\*[A-ZÀ-Ý][^*]{1,40}\*\*|---+\s*$)")


def fatti(p: Path) -> dict:
    """I fatti di una scheda che un controllo di coerenza può incrociare con la
    prosa (ADR-0126; chiesti dal controllo di coerenza della storia, regola S8):
    talenti, incantesimi e capacità speciali con il nome canonico e la riga, e
    le righe di inizio e fine di ogni «Tattiche» e «Descrizione» del file (un
    booklet ne ha più d'una). Sola lettura: non giudica nulla. Un nome che il
    plugin non conosce ha `canonico` nullo. I talenti sono quelli della prima
    riga «Talenti» del file, come nel resto dello strumento; `blocchi` dà una
    voce per scheda del file (titolo, righe di inizio e fine, talenti): un
    incantesimo, una capacità o una «Tattiche» è della scheda che ne contiene
    la riga (`blocco_di`)."""
    import lessico_regole as LR
    from dmcore import magia as M
    from dmcore import sistemi as S
    testo = p.read_text(encoding="utf-8", errors="replace")
    righe = testo.splitlines()
    sistema = VT.sistema_di(p, testo)
    f = VT.leggi(p)
    scheda = L.leggi(p) is not None
    if f is None:    # un file che la lettura delle schede non riconosce: resta la riga «Talenti»
        n, riga = next(((i + 1, m.group(1)) for i, r in enumerate(righe) if (m := VT.RIGA.match(r))), (None, ""))
        f = {"riga": n, "nomi": list(VT.pezzi(riga)) if n else []}
    talenti_ = [{"nome": n, "canonico": (VT.risolvi(sistema, n) or {}).get("en"), "riga": f.get("riga")}
                for n in f.get("nomi") or []]
    try:
        nomi = _liste(sistema)[2]
    except S.ErroreSistemi:
        nomi = {}
    it = _incantesimi_it() if sistema == "dnd35" else {}
    incantesimi_, capacita, sezioni = [], [], {}
    for i, riga in enumerate(righe):
        m = M.RIGA.match(riga)
        if m and "*" in m.group("resto") and not re.match(r"\d", m.group("resto")):
            della_riga = []
            for pezzo in re.split(r"[,;]", re.sub(r"\([^()]*\)|\[[^\]]*\]|[(\[].*$", "", m.group("resto"))):
                volte = re.search(r"[×x]\s*(\d+)\b", pezzo)
                nome = re.sub(r"\b(?:domini[oa]|domain)\s*:?|\([^)]*\)|[×x]\s*\d+\b|\bD\s*$", "", pezzo).strip(" *_.·")
                k = LR.norma(nome)
                if not k or len(k) < 3 or re.fullmatch(r"[\d+ /]+", k):
                    continue
                k = LR.norma(it[k]) if k in it else k
                della_riga.append({"nome": nome, "canonico": nomi.get(k), "livello": int(m.group("liv")),
                                   "usi": m.group("par") or None, "volte": int(volte.group(1)) if volte else 1,
                                   "riga": i + 1})
            # Fuori da una scheda riconosciuta «1° …» è spesso un elenco di prosa: la riga
            # conta solo se almeno un nome è un incantesimo che il plugin conosce.
            if scheda or any(x["canonico"] for x in della_riga):
                incantesimi_ += della_riga
        for c in _CAPACITA.finditer(riga):
            capacita.append({"nome": (c.group(1) or c.group(3) or c.group(5)).strip(" -:·"),
                             "tipo": c.group(2) or c.group(4) or c.group(6), "riga": i + 1})
        s = _SEZIONE.match(riga)
        if s:
            chiave = "tattiche" if s.group(1).lower().startswith("ta") else "descrizione"
            if not any(v["inizio"] <= i + 1 <= v["fine"] for v in sezioni.get(chiave, [])):
                # Un titolo si chiude al titolo dopo (dentro ha i suoi grassetti: «**Round 1**»);
                # un'etichetta in grassetto si chiude all'etichetta dopo.
                ferma = _TITOLO if riga.lstrip().startswith("#") else _ALTRA_SEZIONE
                fine = i
                for j in range(i + 1, len(righe)):
                    if ferma.match(righe[j]):
                        break
                    if righe[j].strip():
                        fine = j
                sezioni.setdefault(chiave, []).append({"inizio": i + 1, "fine": fine + 1})
    blocchi = _blocchi_dei_fatti(righe, sistema)
    return {"file": VT_rel(p), "sistema": sistema, "talenti": talenti_, "incantesimi": incantesimi_,
            "capacita_speciali": capacita, "tattiche": sezioni.get("tattiche", []),
            "descrizione": sezioni.get("descrizione", []), "blocchi": blocchi}


def blocco_di(blocchi: "list[dict]", riga: int) -> "int | None":
    """L'indice del blocco di `fatti()["blocchi"]` che contiene la riga, o None."""
    return next((k for k, b in enumerate(blocchi) if b["inizio"] <= riga <= b["fine"]), None)


_RECINTO_SB = re.compile(r"^```statblocco\s*$")
_INTESTAZIONE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def _blocchi_dei_fatti(righe: "list[str]", sistema: str) -> "list[dict]":
    """Le schede di un file, una per blocco: titolo, righe di inizio e fine, talenti.

    Un blocco comincia a ogni recinto ```statblocco``` e, fuori dai recinti, a
    ogni riga «Talenti» che ha un titolo fra sé e l'inizio del blocco prima (un
    secondo «Talenti» sotto lo stesso titolo è la stessa scheda riscritta, e una
    riga citata con «>» è una nota). Il blocco parte dal titolo che lo precede e
    finisce dove parte il successivo (gli stessi talenti riscritti più sotto non
    aprono un blocco); con una scheda sola il blocco è tutto il
    file. Un recinto senza talenti seguito dai talenti in prosa è una scheda
    sola. I talenti sono quelli della prima riga «Talenti» non citata del blocco."""
    partenze: "list[int]" = []          # indice (da 0) della riga che apre un blocco
    dentro, ultimo, suoi = False, -1, None          # `suoi`: i talenti del blocco aperto, o None
    for i, r in enumerate(righe):
        m = None if r.lstrip().startswith(">") else VT.RIGA.match(r)
        nomi = {x.lower() for x in VT.pezzi(m.group(1))} if m else None
        if _RECINTO_SB.match(r):
            dentro, suoi = True, None
            partenze.append(i)
            ultimo = i
        elif dentro:
            dentro = r.strip() != "```"
            suoi = nomi if suoi is None and m else suoi
            ultimo = i
        elif m:
            # un recinto senza talenti seguito dai talenti in prosa è una scheda sola, e
            # gli stessi talenti riscritti più sotto sono ancora la stessa scheda
            if not partenze or (suoi is not None and not nomi <= suoi
                                and any(_INTESTAZIONE.match(x) for x in righe[ultimo + 1:i])):
                partenze.append(i)
                suoi = nomi
            suoi = nomi if suoi is None else suoi
            ultimo = i
    inizi = []
    for k, i in enumerate(partenze):
        prima = partenze[k - 1] if k else -1
        t = next((j for j in range(i, prima, -1) if _INTESTAZIONE.match(righe[j])), None)
        # con una scheda sola il blocco è il file; con più schede parte dal suo titolo
        inizi.append(0 if len(partenze) == 1 else (t if t is not None else i))
    fuori = []
    for k, i in enumerate(inizi):
        fine = (inizi[k + 1] if k + 1 < len(inizi) else len(righe)) - 1
        t = next((m.group(1) for j in range(partenze[k], i - 1, -1) if (m := _INTESTAZIONE.match(righe[j]))),
                 fuori[-1]["titolo"] if fuori else "")
        n, riga = next(((j + 1, m.group(1)) for j in range(i, fine + 1)
                        if not righe[j].lstrip().startswith(">") and (m := VT.RIGA.match(righe[j]))), (None, ""))
        fuori.append({"titolo": re.sub(r"[*#`]", "", t).strip() if k >= len(fuori) else t, "inizio": i + 1, "fine": fine + 1,
                      "talenti": [{"nome": x, "canonico": (VT.risolvi(sistema, x) or {}).get("en"), "riga": n}
                                  for x in (VT.pezzi(riga) if n else [])]})
    return fuori


_RIGA_VELOCITA = re.compile(r"^velocita:\s*(\d+(?:[.,]\d+)?)\s*(m|ft)\b(.*)$", re.M | re.I)
#: ciò che cambia la velocità e che il conto non sa: oggetti e incantesimi nominati nella scheda…
_ALTRA_VELOCITA = re.compile(r"stivali del(?:la velocit|l'andatura)|boots of (?:speed|striding)|\bhaste\b|\*velocit[àa]\*|"
                             r"longstrider|passo veloce|expeditious|ritirata rapida", re.I)
#: …e ciò che la riga stessa della velocità dichiara fra parentesi
_NOTA_VELOCITA = re.compile(r"stivali|boots|sella|mount|carico|encumb|armored|armatura|corazza", re.I)


def velocita(p: Path) -> "tuple[list[dict], list[dict]]":
    """La velocità a terra scritta contro razza, classe e armatura (ADR-0126, lotto 7).

    Solo per chi ha soltanto livelli di classe ed è di una delle razze di
    `[movimento.razze]`: velocità della razza, più il movimento veloce del
    barbaro (non in armatura pesante) o del monaco (senza armatura né scudo),
    ridotta dall'armatura media o pesante se la razza rallenta. Il mithral conta
    una categoria più leggera. Chi nomina stivali della velocità o un incantesimo che la cambia, o
    scrive una nota nella riga stessa, non è una violazione: è un non verificabile."""
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    try:
        mv = S.dati(sistema, "creature.costruzione").get("movimento")
        gradi = S.dati(sistema, "creature.gradi")
    except S.ErroreSistemi:
        return [], []
    righe = list(_RIGA_VELOCITA.finditer(s.testo))
    if not mv or len(righe) != 1:
        return [], []
    m = righe[0]
    n_riga = s.testo[:m.start()].count("\n") + 1
    base = {"file": VT_rel(p), "riga": n_riga, "verifica": "velocita", "fonte": sistema}
    numero = float(m.group(1).replace(",", "."))
    ha = round(numero * mv["piedi_per_metro_e_mezzo"] / 1.5) if m.group(2).lower() == "m" else round(numero)
    f = VT.leggi(p) or {}
    livelli: dict[str, int] = {}
    it = _classi_it()
    for nome, n in dict(f.get("livelli") or L.livelli_di_classe(s)).items():
        en = it.get(nome.lower(), nome.lower())
        livelli[en] = livelli.get(en, 0) + n
    ignote = f.get("classi_ignote") or []
    if not livelli or sum(g.n for g in s.gruppi) != sum(livelli.values()) + sum(
            int(v.rpartition(" ")[2]) for v in ignote):
        return [], []                                   # dadi vita razziali: la velocità è della creatura
    razza = _razza_srd(" ".join((s.tipo or "", s.testo.split("\n", 1)[0], p.stem.replace("-", " "))), gradi)
    if razza is None or razza not in mv["razze"]:
        return [], []
    if ignote:
        return [], [{**base, "regola": "numero.velocita",
                     "testo": "velocità non ricostruibile: " + ", ".join(ignote) + " fuori dalle regole del plugin"}]
    oggetti = _oggetti_della_ca(s.testo, sistema)
    if len(oggetti) > 1:
        return [], [{**base, "regola": "numero.velocita",
                     "testo": "velocità non ricostruibile: più di una riga della CA con un'armatura"}]
    per_armatura = {(a["ca"], a["des_max"]): a["categoria"] for a in mv["armature"].values()}
    ordine = ["leggera", "media", "pesante"]
    categoria, scudo, nome_armatura = None, False, ""
    for tipo, nome, ca, des_max, voce in (oggetti[0] if oggetti else []):
        if tipo == "scudo":
            scudo = True
            continue
        c = per_armatura.get((ca, des_max))
        if c is None:
            continue
        if _MATERIALI[0][1].search(voce):               # mithral: una categoria più leggera
            c = ordine[max(0, ordine.index(c) - 1)]
        categoria, nome_armatura = c, nome
    atteso, perche = mv["razze"][razza], [f"{razza} {mv['razze'][razza]}"]
    barbaro = mv["classi"].get("barbarian") or {}
    if livelli.get("barbarian") and barbaro and categoria not in barbaro.get("non_in", []):
        atteso += barbaro["piu"]
        perche.append(f"barbaro +{barbaro['piu']}")
    monaco = (mv["classi"].get("monk") or {}).get("per_livello") or []
    if livelli.get("monk") and monaco and categoria is None and not scudo:
        piu = monaco[min(livelli["monk"], len(monaco)) - 1]
        if piu:
            atteso += piu
            perche.append(f"monaco +{piu}")
    if categoria in mv["rallentano"] and razza not in mv["non_rallenta"]:
        atteso = mv["ridotta"].get(str(atteso), atteso)
        perche.append(f"ridotta da {nome_armatura} ({categoria})")
    if ha == atteso:
        return [], []
    testo = f"velocità {m.group(1)} {m.group(2)} ({ha} piedi), la regola dà {atteso} piedi ({', '.join(perche)})"
    if _ALTRA_VELOCITA.search(s.testo) or _NOTA_VELOCITA.search(m.group(3)):
        return [], [{**base, "regola": "numero.velocita",
                     "testo": testo + "; la scheda nomina un oggetto, un incantesimo o una nota che la cambia"}]
    return [{**base, "regola": "numero.velocita", "atteso": atteso, "ha": ha, "testo": testo}], []


_SCRITTA_RI = re.compile(r"(?<![\w/])(?:RI|SR|resistenza agli incantesimi|spell resistance)\b[\s:*]*(\d+)([^|·\n]{0,60})",
                         re.I)
_SCRITTA_RD = re.compile(r"(?<![\w/])(?:RD|DR|riduzione del danno|damage reduction)\b[\s:*]*(\d+)\s*/\s*(?:—|–|-)(?![\w])",
                         re.I)
#: righe che raccontano la storia della scheda, non la scheda: citazioni, «era:», registri delle correzioni
_RIGA_DI_STORIA = re.compile(r"^\s*(?:>|[-*]\s*era\b|era\b|boost log|changelog)", re.I)
#: ciò che dà o cambia la resistenza agli incantesimi e che il conto non sa
_ALTRA_RI = re.compile(r"(?:manto|mantello|mantle|veste|robe) (?:della|of) (?:resistenza agli incantesimi|spell resistance)|"
                       r"\*(?:resistenza agli incantesimi|spell resistance)\*|holy aura|unholy aura|aura (?:sacra|sacrilega)",
                       re.I)


def difese(p: Path) -> "tuple[list[dict], list[dict]]":
    """Resistenza agli incantesimi e riduzione del danno contro razza e classe (ADR-0126, lotto 7).

    RI: la razza di `[difese.ri.razze]` dà N + i livelli di classe; il monaco dà
    livello + 10 dal 13°; vale la più alta. RD: il barbaro ha N/— per livello.
    Chi dovrebbe averla e non la scrive è una violazione. Una nota accanto al
    numero, o un oggetto o un incantesimo che la dà, fanno di uno scarto un non
    verificabile. Più numeri diversi nella scheda: non verificabile."""
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    try:
        d = S.dati(sistema, "creature.costruzione").get("difese")
    except S.ErroreSistemi:
        return [], []
    if not d:
        return [], []
    try:
        creature = S.dati(sistema, "creature.base").get("creature_base", {})
    except S.ErroreSistemi:
        creature = {}
    f = VT.leggi(p) or {}
    livelli: dict[str, int] = {}
    it = _classi_it()
    for nome, n in dict(f.get("livelli") or L.livelli_di_classe(s)).items():
        en = it.get(nome.lower(), nome.lower())
        livelli[en] = livelli.get(en, 0) + n
    dadi_vita = sum(g.n for g in s.gruppi)
    dove = " ".join((s.tipo or "", s.testo.split("\n", 1)[0], p.stem.replace("-", " ")))
    righe = [(i + 1, r) for i, r in enumerate(s.testo.split("\n")) if not _RIGA_DI_STORIA.match(r)]
    base = {"file": VT_rel(p), "verifica": "difese", "fonte": sistema}
    viol, nv = [], []

    # resistenza agli incantesimi: la razza conta i livelli di classe, cioè i dadi vita oltre quelli della
    # razza (una razza che la tabella delle creature non ha, come il drow, non ne ha di suoi)
    attese = []
    razze = [r for r, nomi in d["ri"]["nomi"].items()
             if any(re.search(rf"\b(?:{n})\b", dove, re.I) for n in nomi)
             and re.search(rf"\b{creature.get(r, {}).get('tipo', 'humanoid')}\b", s.tipo or "", re.I)]
    if len(razze) == 1:
        suoi = creature.get(razze[0], {}).get("dv", 0)
        di_classe = dadi_vita - suoi if dadi_vita >= suoi and dadi_vita else sum(livelli.values())
        attese.append((d["ri"]["razze"][razze[0]] + di_classe,
                       f"{razze[0]} {d['ri']['razze'][razze[0]]} + {di_classe} livelli di classe"))
    for classe, v in d["ri"]["classi"].items():
        if livelli.get(classe, 0) >= v["dal"]:
            attese.append((livelli[classe] + v["piu"], f"{classe} {livelli[classe]} + {v['piu']}"))
    if attese:
        atteso, perche = max(attese)
        scritte = [(n, int(m.group(1)), m.group(2)) for n, r in righe for m in _SCRITTA_RI.finditer(r)]
        numeri = sorted({x[1] for x in scritte})
        riga = scritte[0][0] if scritte else 1
        b = {**base, "riga": riga, "regola": "numero.RI"}
        if not scritte:
            viol.append({**b, "atteso": atteso, "ha": None,
                         "testo": f"senza resistenza agli incantesimi, la regola dà RI {atteso} ({perche})"})
        elif len(numeri) > 1:
            nv.append({**b, "testo": f"RI non ricostruibile: la scheda ne scrive più d'una ({', '.join(map(str, numeri))})"})
        elif numeri[0] != atteso:
            testo = f"RI {numeri[0]}, la regola dà {atteso} ({perche})"
            if _ALTRA_RI.search(s.testo) or re.match(r"\s*\**\s*\(", scritte[0][2]):
                nv.append({**b, "testo": testo + "; la scheda nomina un oggetto, un incantesimo o una nota che la cambia"})
            else:
                viol.append({**b, "atteso": atteso, "ha": numeri[0], "testo": testo})

    # riduzione del danno N/—
    for classe, v in d["rd"]["classi"].items():
        n = livelli.get(classe, 0)
        if not n:
            continue
        atteso = v["per_livello"][min(n, len(v["per_livello"])) - 1]
        scritte = [(i, int(m.group(1))) for i, r in righe for m in _SCRITTA_RD.finditer(r)]
        numeri = sorted({x[1] for x in scritte})
        b = {**base, "riga": scritte[0][0] if scritte else 1, "regola": "numero.RD"}
        perche = f"{classe} di {n}° livello"
        if not scritte and atteso:
            viol.append({**b, "atteso": atteso, "ha": None,
                         "testo": f"senza riduzione del danno, la regola dà RD {atteso}/— ({perche})"})
        elif len(numeri) > 1:
            nv.append({**b, "testo": f"RD non ricostruibile: la scheda ne scrive più d'una ({', '.join(f'{x}/—' for x in numeri)})"})
        elif scritte and numeri[0] != atteso:
            viol.append({**b, "atteso": atteso, "ha": numeri[0],
                         "testo": f"RD {numeri[0]}/—, la regola dà {atteso}/— ({perche})"})
    viol_i, nv_i = _immunita_del_tipo(s, d.get("immunita") or {}, righe, base)
    return viol + viol_i, nv + nv_i


def _immunita_del_tipo(s, dati: dict, righe: "list[tuple[int, str]]", base: dict) -> "tuple[list[dict], list[dict]]":
    """Le immunità che il tipo dà (SRD, tratti dei tipi) devono stare nella scheda: o la
    formula «tratti dei non morti» / «undead traits», o ogni immunità nominata in una riga
    che dice «immune». Chi ha un punteggio di Intelligenza non è «mindless»: l'immunità
    all'influenza mentale gli si chiede solo se il tipo la dà da sola (vegetali, non morti)."""
    if not dati:
        return [], []
    prima = re.split(r"[(,/]", s.tipo or "", maxsplit=1)[0]
    tipi = [k for k in dati["tipi"]
            if re.search(rf"(?<![\w-])(?<!mezzo )(?:{k}|{dati['nomi'][k]})\b", prima, re.I)]
    if len(tipi) != 1:
        return [], []
    tipo = tipi[0]
    nome = dati["nomi"][tipo]
    testo = "\n".join(r for _, r in righe)
    if re.search(rf"tratti\s+(?:(?:de[il]|dei|degli|da|del tipo)\s+)?(?:{nome})|\b{tipo} traits\b", testo, re.I):
        return [], []
    attese = list(dati["tipi"][tipo])
    senza_mente = tipo in ("construct", "ooze", "vermin")
    if senza_mente and re.search(r"\bInt\.?\s+\d", testo):
        attese = [x for x in attese if x != "influenza mentale"]
    di_immunita = " ".join(r for _, r in righe if re.search(r"immun", r, re.I))
    mancano = [x for x in attese if not re.search(dati["parole"][x], di_immunita, re.I)]
    if not mancano:
        return [], []
    riga = next((n for n, r in righe if re.search(r"immun", r, re.I)), 1)
    return [{**base, "riga": riga, "regola": "tratti.immunita", "atteso": attese, "ha": None,
             "testo": f"il tipo «{tipo}» dà immunità che la scheda non scrive: {', '.join(mancano)} "
                      f"(basta «tratti del tipo»; SRD, tratti dei tipi)"}], []


_RIGA_LINGUAGGI = re.compile(r"(?:^|[.·|]\s*)\W*(?:linguaggi|lingue|languages)\b\W*:?\**\s*([^·|\n]*)", re.I)


def linguaggi(p: Path) -> "tuple[list[dict], list[dict]]":
    """I linguaggi che razza e classe danno da soli stanno nella riga dei linguaggi (ADR-0126, lotto 7).

    Solo per chi scrive una riga «Linguaggi» (una sola, fuori dalle righe di
    storia): una delle sette razze dell'SRD ha i suoi linguaggi automatici, il
    druido ha il Druidico. Quanti linguaggi in più si possono avere non si
    giudica: dipende da regione e gradi che la scheda non scrive."""
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    try:
        d = S.dati(sistema, "creature.costruzione").get("linguaggi")
        gradi = S.dati(sistema, "creature.gradi")
    except S.ErroreSistemi:
        return [], []
    if not d:
        return [], []
    trovate = [(n + 1, m.group(1)) for n, r in enumerate(s.testo.split("\n")) if not _RIGA_DI_STORIA.match(r)
               for m in _RIGA_LINGUAGGI.finditer(r)]
    if len(trovate) != 1:
        return [], []
    n_riga, scritti = trovate[0]
    attesi, perche = [], []
    razza = _razza_srd(" ".join((s.tipo or "", s.testo.split("\n", 1)[0], p.stem.replace("-", " "))), gradi)
    if razza in d["razze"]:
        attesi += d["razze"][razza]
        perche.append(razza)
    f = VT.leggi(p) or {}
    it = _classi_it()
    for nome in dict(f.get("livelli") or L.livelli_di_classe(s)):
        en = it.get(nome.lower(), nome.lower())
        if en in d["classi"]:
            attesi += [x for x in d["classi"][en] if x not in attesi]
            perche.append(en)
    mancano = [x for x in attesi if not re.search(rf"\b(?:{d['nomi'][x]})\b", scritti, re.I)]
    if not mancano:
        return [], []
    return [{"file": VT_rel(p), "riga": n_riga, "verifica": "linguaggi", "fonte": sistema,
             "regola": "tratti.linguaggi", "atteso": attesi, "ha": scritti.strip(),
             "testo": f"la riga dei linguaggi non ha {', '.join(mancano)}, che {' e '.join(perche)} dà da sé "
                      f"(SRD, linguaggi automatici)"}], []


_TESTA_EQUIP = re.compile(r"^\W*(?:equipaggiamento|altro equipaggiamento|equipment|possessions|(?:combat |other )?gear|"
                          r"oggetti magici|magic items)\b", re.I)
#: «· **Equipaggiamento** …» dentro la riga delle Statistiche (la forma di ADR-0091): fino alla voce dopo
_EQUIP_NELLA_RIGA = re.compile(r"·\s*\*\*((?:altro\s+)?equipaggiamento(?:\s+da\s+combattimento)?)\*\*:?\s*(.+?)"
                               r"(?=\s·\s+\*\*|$)", re.I)
_FINE_EQUIP = re.compile(r"^\s*(?:#{1,6}\s|---+\s*$|\*\*[^*|]{2,60}\*\*\s*:?\s*$|```)")


def _righe_dell_equipaggiamento(testo: str) -> "list[tuple[int, str]]":
    """Le righe che elencano l'equipaggiamento: quella che comincia con «Equipaggiamento» (o «Gear»,
    «Possessions»…) e, se è un titolo o finisce lì, l'elenco o la tabella che la segue."""
    out, dentro = [], False
    for n, r in enumerate(testo.split("\n"), 1):
        if _TESTA_EQUIP.match(r) and not _RIGA_DI_STORIA.match(r):
            resto = _TESTA_EQUIP.sub("", r, count=1).strip(" *:#")
            dentro = len(resto) < 12 or r.lstrip().startswith("#")
            if not dentro:
                out.append((n, r))
        elif dentro:
            if _FINE_EQUIP.match(r):
                dentro = False
            elif r.strip() and not _RIGA_DI_STORIA.match(r):
                out.append((n, r))
        elif "·" in r and not _RIGA_DI_STORIA.match(r):
            out += [(n, m.group(2)) for m in _EQUIP_NELLA_RIGA.finditer(r)]
    return out


def _senza_la_copia(testo: str, oggetti: "list[tuple[int, tuple[str, int]]]") -> "list[tuple[int, tuple[str, int]]]":
    """Una scheda scrive l'equipaggiamento due volte, nel recinto `statblocco` e nella prosa sotto:
    è lo stesso equipaggiamento, e si conta una volta sola, dalla parte che ne riconosce di più."""
    nel_recinto, dentro = set(), False
    for n, r in enumerate(testo.split("\n"), 1):
        if r.lstrip().startswith("```"):
            dentro = not dentro
        elif dentro:
            nel_recinto.add(n)
    blocco = [o for o in oggetti if o[0] in nel_recinto]
    prosa = [o for o in oggetti if o[0] not in nel_recinto]
    if not blocco or not prosa:
        return oggetti
    return blocco if sum(o[1][1] for o in blocco) >= sum(o[1][1] for o in prosa) else prosa


_PREFISSI_OGGETTO = (("ring of ", "anell[oi]"), ("rod of ", "vergh?[ae]"), ("staff of ", "baston[ei]"))
_NUMERI_IT = {"un": 1, "una": 1, "uno": 1, "due": 2, "tre": 3, "quattro": 4, "cinque": 5, "sei": 6}
_QUANTI = r"(?:(\d+|un[ao]?|due|tre|quattro|cinque|sei)\s+)?"
_PREP = r"(?:di|del|dello|della|dei|degli|delle|dell['’]|of)\s*"


def _schema_del_nome(nome: str) -> str:
    """Il nome di un oggetto come espressione regolare: spazi liberi, la virgola del lessico facoltativa."""
    return r"\s+".join(re.escape(x) for x in nome.replace(",", " ").split()).replace("'", "['’]")


@lru_cache(maxsize=None)
def _oggetti_del_lessico(sistema: str) -> "tuple[tuple[re.Pattern, str], ...]":
    """(schema, chiave del prezzo senza «+N») dei nomi italiani e inglesi del lessico che hanno un
    prezzo nel plugin. Un anello, una verga o un bastone che il lessico chiama col solo effetto
    («Protezione») vuole davanti la parola dell'oggetto."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    prezzi = S.dati(sistema, "creature.costruzione")["oggetti"]["prezzi"]
    basi = {re.sub(r"\s*\+\d+$", "", k) for k in prezzi}
    out = []
    for v in LR.tabella_35():
        if v["tipo"] != "oggetto magico":
            continue
        en = v["srd35"].lower().replace("’", "'").strip()
        # un nome di una parola sola vale solo se è quello inglese: «Ventaglio» (wind fan) in una
        # riga dell'equipaggiamento può essere un ventaglio qualunque
        nomi = [n for n in [v["it"], v["srd35"]] + (v.get("varianti") or "").split("|")
                if len(n) >= 6 and (" " in n.strip() or n == v["srd35"])]
        if en in basi:
            out += [(re.compile(rf"(?<!\w){_schema_del_nome(n)}(?!\w)", re.I), en) for n in nomi]
            continue
        for prefisso, parola in _PREFISSI_OGGETTO:
            if prefisso + en in basi:
                out += [(re.compile(rf"(?<!\w)(?:{parola}|{prefisso.split()[0]}s?)\s+{_PREP}{_schema_del_nome(n)}(?!\w)",
                                    re.I), prefisso + en) for n in nomi]
    return tuple(sorted(out, key=lambda x: -len(x[0].pattern)))


_MATERIALE = r"mithr[ai]l|adamantin[eoa]|adamantio"
_PERFETTA = r"perfett[oaie]|masterwork|mwk"
_MATERIALE_DOPO = re.compile(rf"\s*(?:(?:di|in|d['’])\s*)?(?<!\w)({_MATERIALE})(?!\w)", re.I)
_MATERIALE_PRIMA = re.compile(rf"(?<!\w)({_MATERIALE})\s+$", re.I)


@lru_cache(maxsize=None)
def _bastoni_del_lessico(sistema: str) -> "dict[str, str]":
    """Nome italiano o inglese dell'effetto («fuoco», «fire») → chiave del prezzo («staff of fire»).
    La parola «bastone» davanti la chiede chi cerca: qui un nome corto non è un rischio."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    prezzi = S.dati(sistema, "creature.costruzione")["oggetti"]["prezzi"]
    out = {k[len("staff of "):]: k for k in prezzi if k.startswith("staff of ")}
    for v in LR.tabella_35():
        chiave = "staff of " + v["srd35"].lower().strip()
        if v["tipo"] == "oggetto magico" and chiave in prezzi:
            for n in [v["it"]] + (v.get("varianti") or "").split("|"):
                if n.strip():
                    out.setdefault(n.strip().lower(), chiave)
    return out


@lru_cache(maxsize=None)
def _capacita_del_lessico(sistema: str) -> "dict[str, tuple[tuple[re.Pattern, dict], ...]]":
    """Per armi e armature, (schema, {bonus} o {mo}) delle capacità speciali coi nomi del lessico.
    L'ultima vocale è libera: «affilata» e «affilato» sono la stessa capacità."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    cap = S.dati(sistema, "creature.costruzione")["oggetti"].get("capacita") or {}
    nomi: dict[str, set[str]] = {}
    for v in LR.tabella_35():
        if v["tipo"] in ("oggetto magico", "proprietà magica"):
            en = re.sub(r"\s*\((?:ex|su|sp)\)$", "", v["srd35"].lower().replace("’", "'").strip())
            nomi.setdefault(en, {en}).update(n.lower() for n in [v["it"]] + (v.get("varianti") or "").split("|") if n)
    out = {}
    for che, voci in cap.items():
        schemi = []
        for en, valore in voci.items():
            for n in nomi.get(en, {en}):
                s = _schema_del_nome(n)
                s = re.sub(r"[aoei]$", "[aoei]", s) if n != en else s
                schemi.append((re.compile(rf"(?<!\w){s}(?!\w)", re.I), valore, en))
        out[che] = tuple(sorted(schemi, key=lambda x: -len(x[0].pattern)))
    return out


def _oggetti_col_prezzo(riga: str, d: dict, sistema: str) -> "list[tuple[str, int]]":
    """Gli oggetti della riga che hanno un prezzo certo: quelli di `[[oggetti.nomi]]` e del lessico,
    armature, scudi e armi «+N» con le capacità speciali scritte accanto, pozioni e pergamene di
    un incantesimo, bacchette con le cariche scritte. Ogni tratto della riga conta una volta."""
    from dmcore import classe_armatura as CA
    from dmcore import sistemi as S
    trovati, presi = [], []

    def libero(a: int, b: int) -> bool:
        return all(b <= x or a >= y for x, y in presi)

    def quanti(parola: "str | None") -> int:
        return 1 if not parola else int(parola) if parola.isdigit() else _NUMERI_IT.get(parola.lower(), 1)

    for voce in d["nomi"]:
        for m in re.finditer(voce["schema"], riga, re.I):
            nome = voce["nome"].replace("N", m.group(1)) if "N" in voce["nome"] else voce["nome"]
            if nome in d["prezzi"] and libero(*m.span()):
                presi.append(m.span())
                trovati.append((nome, d["prezzi"][nome]))
    # armature, scudi e armi: potenziamento più le capacità speciali del tratto fino alla virgola
    armature, scudi = CA.tabelle(sistema)
    armi = [n for a in S.dati(sistema, "creature.armi").get("armi", []) for n in a["nomi"]]
    capacita = _capacita_del_lessico(sistema)
    categorie = {(v["ca"], v["des_max"]): v["categoria"]
                 for v in S.dati(sistema, "creature.costruzione").get("movimento", {}).get("armature", {}).values()}

    comuni, perfetta = d.get("comuni") or {}, d.get("perfetta") or {}
    inglesi = {(v["ca"], v["des_max"]): k
               for k, v in S.dati(sistema, "creature.costruzione").get("movimento", {}).get("armature", {}).items()}
    prezzo_arma = {n: comuni.get("armi", {}).get(a["nome"].lower(), 0)
                   for a in S.dati(sistema, "creature.armi").get("armi", []) for n in a["nomi"]}

    def base(nome: str, che: str) -> int:
        """Il prezzo dell'oggetto comune: l'arma di taglia Media, l'armatura, lo scudo meno caro col suo bonus."""
        if che == "arma":
            return 0 if nome in scudi or nome in armature else prezzo_arma.get(nome, 0)
        if nome in scudi:
            return comuni.get("scudi", {}).get(str(scudi[nome][0]), 0)
        return comuni.get("armature", {}).get(inglesi.get(armature.get(nome), ""), 0)

    def in_piu(materiale: "str | None", nome: str, che: str) -> "tuple[int, str]":
        """Quanto costa in più l'oggetto di adamantio o di mithral, se la tabella ha la sua categoria."""
        if not materiale:
            return 0, ""
        chiave = "mithral" if materiale.lower().startswith("mith") else "adamantine"
        if che == "arma" and (nome in scudi or nome in armature):
            return 0, ""                                # uno scudo fra le armi: la tabella non lo prezza
        categoria = "arma" if che == "arma" else "scudo" if nome in scudi else categorie.get(armature.get(nome))
        mo = (d.get("materiali") or {}).get(chiave, {}).get(categoria, 0)
        return mo, f" di {chiave.replace('adamantine', 'adamantio')}" if mo else ""
    for nomi, tabella, che in ((list(armature) + list(scudi), d["potenziamento"]["armatura"], "armatura"),
                               (armi, d["potenziamento"]["arma"], "arma")):
        for nome in sorted(set(nomi), key=len, reverse=True):
            # «spada lunga infuocata +1 …» oppure, all'inglese, «+1 flaming longsword»
            for m in re.finditer(rf"(?<!\w){re.escape(nome)}(?!\w)((?:\s+[^\W\d]+(?:['’][^\W\d]+)?){{0,3}})\s*\+(\d+)(?!\d)([^,;|()]*)"
                                 rf"|(?<![\w+])\+(\d+)\s+((?:[^\W\d]+\s+){{0,3}}?){re.escape(nome)}(?!\w)", riga, re.I):
                n = int(m.group(2) or m.group(4))
                if not (1 <= n <= len(tabella) and libero(*m.span())):
                    continue
                # una capacità conta solo se sta attaccata al nome o al bonus («spadone sacrilego +2»,
                # «spada lunga +1 infuocata e affilata»): più in là può essere un nome proprio
                bonus, mo, dette = 0, 0, []
                # il materiale conta come le capacità: attaccato al nome o al bonus, prima o dopo
                tratti = [m.group(1), m.group(3)] if m.group(2) else [m.group(5), ""]
                materiale = None
                for i, tratto in enumerate(tratti):
                    mm = _MATERIALE_DOPO.match(tratto) if i else _MATERIALE_DOPO.search(tratto)
                    if mm and not materiale:
                        materiale, tratti[i] = mm.group(1), tratto[:mm.start()] + tratto[mm.end():]
                prima = _MATERIALE_PRIMA.search(riga[:m.start()])
                materiale = materiale or (prima.group(1) if prima else None)
                for tratto in tratti:
                    resto = tratto
                    while True:
                        resto = re.sub(r"^\s*(?:e\s+|and\s+)?", "", resto)
                        c = next(((s.match(resto), v, en) for s, v, en in capacita.get(che, ()) if s.match(resto)), None)
                        if c is None:
                            break
                        resto = resto[c[0].end():]
                        bonus += c[1].get("bonus", 0)
                        mo += c[1].get("mo", 0)
                        dette.append(c[2])
                if n + bonus > len(tabella):
                    bonus, mo, dette = 0, 0, []     # oltre la tabella: resta il solo potenziamento
                piu, detto = in_piu(materiale, nome, che)
                presi.append(m.span())
                # un oggetto magico è di fattura perfetta: prezzo comune, fattura, potenziamento. Il mithral
                # e l'adamantio hanno la fattura già nel loro prezzo
                fattura = 0 if piu else perfetta.get(che, 0) if base(nome, che) else 0
                trovati.append((f"{nome} +{n}{detto}{''.join(' ' + x for x in dette)} ({che})",
                                tabella[n + bonus - 1] + mo + piu + base(nome, che) + fattura))
    # lo stesso senza il «+N» dopo il nome: «mithral chainmail», «+1 mithral full plate», «ascia di adamantio»
    for nomi, tabella, che in ((list(armature) + list(scudi), d["potenziamento"]["armatura"], "armatura"),
                               (armi, d["potenziamento"]["arma"], "arma")):
        for nome in sorted(set(nomi), key=len, reverse=True):
            for m in re.finditer(rf"(?:\+(\d+)\s+)?(?<!\w)({_MATERIALE})\s+{re.escape(nome)}(?!\w)"
                                 rf"|(?<!\w){re.escape(nome)}\s+(?:di|in|d['’])\s*({_MATERIALE})(?!\w)", riga, re.I):
                piu, detto = in_piu(m.group(2) or m.group(3), nome, che)
                n = int(m.group(1) or 0)
                if not piu or n > len(tabella) or not libero(*m.span()):
                    continue
                presi.append(m.span())
                trovati.append((f"{nome}{f' +{n}' if n else ''}{detto} ({che})",
                                piu + base(nome, che) + (tabella[n - 1] if n else 0)))
    # pozioni e pergamene di un incantesimo, bacchette con le cariche scritte
    incantesimi = _incantesimi_it()
    for parole, prefisso, tabella in ((r"pozion[ei]|oli[oi]|potions?|oils?", "potion of ", d["prezzi"]),
                                      (r"pergamen[ae]|scrolls?", "", d.get("pergamene", {})),
                                      (r"bacchett[ae]|wands?", "wand of ", d["prezzi"])):
        for m in re.finditer(rf"(?<!\w){_QUANTI}(?:{parole})\s+{_PREP}[*_]*([^*_,;|()×]+?)[*_]*\s*"
                             rf"(?:[×x]\s*(\d+)\s*)?(?:\((\d+)\s+cariche\)|\(|[,;|.]|$)", riga, re.I):
            import lessico_regole as LR
            detto = m.group(2).strip()
            en = incantesimi.get(LR.norma(detto), detto).lower().replace("’", "'")
            # più voci per lo stesso incantesimo (livello dell'incantatore diverso): vale la meno cara
            chiavi = sorted((k for k in tabella if k == prefisso + en or k.startswith(f"{prefisso}{en} (")),
                            key=lambda k: tabella[k])
            if not chiavi or not libero(*m.span()):
                continue
            if prefisso == "wand of ":
                if not m.group(4):
                    continue
                mo, n = tabella[chiavi[0]] * min(int(m.group(4)), 50) // 50, 1
            else:
                mo, n = tabella[chiavi[0]], quanti(m.group(1)) * int(m.group(3) or 1)
            presi.append(m.span())
            trovati.append((f"{n} × {chiavi[0]}" if n > 1 else chiavi[0], mo * n))
    # bastoni: solo con le cariche scritte, in proporzione alle 50 di un bastone nuovo
    for m in re.finditer(rf"(?<!\w)(?:baston[ei]|staffs?)\s+{_PREP}[*_]*([^*_,;|()]+?)[*_]*\s*"
                         rf"\([^()]*?(\d+)\s+(?:cariche|charges)\)", riga, re.I):
        chiave = _bastoni_del_lessico(sistema).get(re.sub(r"\s+", " ", m.group(1).strip().lower()))
        if chiave and libero(*m.span()):
            presi.append(m.span())
            trovati.append((f"{chiave} ({m.group(2)} cariche)", d["prezzi"][chiave] * min(int(m.group(2)), 50) // 50))
    # gli altri oggetti che il lessico nomina
    for schema, chiave in _oggetti_del_lessico(sistema):
        for m in schema.finditer(riga):
            piu = re.match(r"\s*\+(\d+)", riga[m.end():])
            nome = f"{chiave} +{piu.group(1)}" if piu and f"{chiave} +{piu.group(1)}" in d["prezzi"] else chiave
            if nome in d["prezzi"] and libero(*m.span()):
                presi.append(m.span())
                trovati.append((nome, d["prezzi"][nome]))
    # armi, armature e scudi comuni, con la fattura perfetta se sta scritta accanto. Un nome corto
    # («pelle», «rete») conta solo se è di fattura perfetta: da solo può essere un'altra cosa
    for nomi, che in ((list(armature) + list(scudi), "armatura"), (armi, "arma")):
        for nome in sorted(set(nomi), key=len, reverse=True):
            mo = base(nome, che)
            if mo < 1:
                continue
            for m in re.finditer(rf"(?<!\w)(?:({_PERFETTA})\s+)?{re.escape(nome)}(?!\w)"
                                 rf"(?:\s+(?:[^\W\d]+\s+){{0,2}}?(?:di\s+fattura\s+)?({_PERFETTA})(?!\w))?", riga, re.I):
                fine = bool(m.group(1) or m.group(2))
                if (len(nome) < 6 and not fine) or not libero(*m.span()):
                    continue
                presi.append(m.span())
                trovati.append((f"{nome}{' perfetta' if fine else ''} ({che})", mo + (perfetta.get(che, 0) if fine else 0)))
    return trovati


_MODELLO = re.compile(r"half[- ]|mezzo?[- ]?(?:drag|immond|celest)|vampir|lich\b|licantrop|lycanthrop|\bwere|mannar|"
                      r"fantasma|ghost|scheletr|skelet|zombi|celestial|fiendish|immondo|template|modello|archetip", re.I)


def _tipo_en(tipo: str) -> str:
    tipo = tipo.lower()
    for it, en in _TIPI_IT.items():
        tipo = tipo.replace(it, en)
    return tipo


#: La riga con cui il DM dichiara che l'equipaggiamento supera la tabella per scelta sua
_SOPRA_LA_TABELLA = re.compile(r"^>?\s*equipaggiamento (?:sopra|oltre) la tabella[^\n]*\b(?:DM|ADR-\d+)\b", re.I | re.M)


def ricchezza(p: Path) -> "tuple[list[dict], list[dict]]":
    """Il valore dell'equipaggiamento contro quello di un PNG del suo livello (ADR-0126, lotto 8).

    Si sommano solo gli oggetti dal prezzo certo (oggetti con un nome del
    lessico, armi e armature «+N» con le capacità speciali attaccate, pozioni,
    pergamene, bacchette con le cariche scritte), quindi la somma è un minimo:
    se il minimo supera il valore della tabella dei PNG per il livello, la
    scheda ha più equipaggiamento di quello che il suo GS conta. Il livello è
    quello effettivo: dadi vita più il modificatore di livello della creatura
    base, o della razza senza dadi vita razziali (`[mdl]`: hobgoblin, drow,
    orco…); se né razza né base si conoscono, o la scheda nomina un modello,
    uno scarto è un non verificabile. Sotto la tabella non si dice niente.
    Una creatura base che non avanza per classe («Advancement» dell'SRD) e
    senza livelli di classe ha un tesoro, non l'equipaggiamento di un PNG
    (SRD, «Improving Monsters»): lo scarto è un non verificabile
    `equipaggiamento.da_png` e la tabella non la giudica. Una riga
    «Equipaggiamento sopra la tabella: … DM …» dichiara lo scarto come scelta
    del DM, e la verifica tace."""
    import conformita_statblocchi as C
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    try:
        d = S.dati(sistema, "creature.costruzione").get("oggetti")
        gradi = S.dati(sistema, "creature.gradi")
    except S.ErroreSistemi:
        return [], []
    if not d or "per_livello" not in d.get("png", {}):
        # PF1e ha la Tabella 14-9 ma non ancora i prezzi dei suoi oggetti: non si giudica
        return [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(s.testo))
    if len(blocchi) > 1:
        return [], []
    righe = _righe_dell_equipaggiamento(s.testo)
    oggetti = _senza_la_copia(s.testo, [(n, o) for n, r in righe for o in _oggetti_col_prezzo(r, d, sistema)])
    dadi_vita = sum(g.n for g in s.gruppi)
    if not oggetti or not dadi_vita:
        return [], []
    totale = sum(o[1] for _, o in oggetti)
    tabella = d["png"]["per_livello"]
    base = {"file": VT_rel(p), "riga": oggetti[0][0], "verifica": "ricchezza", "fonte": sistema,
            "regola": "equipaggiamento.valore"}
    elenco = ", ".join(f"{nome} {mo}" for _, (nome, mo) in oggetti)
    if totale <= tabella[min(dadi_vita, len(tabella)) - 1]:
        return [], []
    dove = " ".join((s.tipo or "", s.testo.split("\n", 1)[0], p.stem.replace("-", " ")))
    mdl = 0 if _razza_srd(dove, gradi) else None
    if mdl is None:
        # una razza senza dadi vita razziali (hobgoblin, drow, orco…): il suo modificatore di livello
        senza_dv = S.dati(sistema, "creature.costruzione").get("mdl") or {"razze": {}, "nomi": {}}
        sue = [r for r, rx in senza_dv["nomi"].items() if re.search(rf"(?<![\w-])(?:{rx})(?![\w-])", dove, re.I)
               and re.search(rf"\b{senza_dv['razze'][r]['tipo']}\b", _tipo_en(s.tipo or ""), re.I)]
        if len(sue) == 1 and not _MODELLO.search(dove):
            mdl = senza_dv["razze"][sue[0]]["mdl"]
    if mdl is None and blocchi:
        trovata = _base_del_blocco(s.testo, blocchi[0]["sb"], True, sistema)
        if trovata and trovata[1].get("avanza") != "classe" and not L.livelli_di_classe(s):
            # SRD, «Improving Monsters»: l'equipaggiamento di un PNG spetta solo a chi avanza per classe
            return [], [dict(base, regola="equipaggiamento.da_png",
                             testo=f"equipaggiamento per almeno {totale} mo ({elenco}), ma «{trovata[0]}» non avanza "
                                   f"per classe e la scheda non ha livelli di classe: per l'SRD («Improving "
                                   f"Monsters») ha un tesoro, non l'equipaggiamento di un PNG, e la Tabella 4-23 "
                                   f"non la giudica")]
        if trovata and isinstance(trovata[1].get("mdl"), int):
            mdl = trovata[1]["mdl"]
    if mdl is None:
        return [], [dict(base, testo=f"equipaggiamento per almeno {totale} mo ({elenco}) contro i "
                                     f"{tabella[min(dadi_vita, len(tabella)) - 1]} mo di un PNG di {dadi_vita} dadi "
                                     f"vita, ma il modificatore di livello della razza non si conosce")]
    livello = dadi_vita + mdl
    if livello > len(tabella):
        return [], [dict(base, testo=f"livello effettivo {livello}: la tabella dei PNG si ferma al {len(tabella)}°")]
    limite = tabella[livello - 1]
    if totale <= limite or _SOPRA_LA_TABELLA.search(s.testo):
        return [], []
    return [dict(base, atteso=f"al più {limite} mo", ha=f"almeno {totale} mo",
                 testo=f"equipaggiamento per almeno {totale} mo ({elenco}) contro i {limite} mo di un PNG di "
                       f"livello effettivo {livello} (DMG 3.5, Tabella 4-23): l'equipaggiamento in più va "
                       f"dichiarato e conta nel GS")], []


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="+", type=Path, help="schede o cartelle")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    ap.add_argument("--fatti", action="store_true",
                    help="non giudica: stampa in JSON, per scheda, talenti, incantesimi, capacità speciali "
                         "e le righe di «Tattiche» e «Descrizione»")
    ap.add_argument("--tolleranza", action="store_true",
                    help="rimette la tolleranza di prima su tiri salvezza (+4) e attacco (−1…+2)")
    a = ap.parse_args(argv)
    global SEVERO
    SEVERO = not a.tolleranza
    percorsi = [p if p.is_absolute() else ROOT / p for p in a.percorsi]
    for p in percorsi:
        if not p.exists():
            print(f"verifica_scheda: {p} non esiste", file=sys.stderr)
            return 2
    if a.fatti:
        tutti = [fatti(p) for p in VT.schede(percorsi)]
        json.dump([f for f in tutti if any(f[k] for k in f if k not in ("file", "sistema"))], sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
        return 0
    viol, nv, lette = [], [], 0
    for p in VT.schede(percorsi):
        tv, tn, ti = talenti(p)
        nvv, nn = numeri(p)
        av, an = abilita(p)
        iv, inn = incantesimi(p)
        cv, cn = classe_armatura(p)
        dv, dn = danno(p)
        mv, mn = incantatori(p)
        pv, pn = prestigio(p)
        qv, qn = numero_talenti(p)
        bv, bn = creatura_base(p)
        gv, gn = grado_di_sfida(p)
        ev, en_ = velocita(p)
        fv, fn = difese(p)
        lv, ln = linguaggi(p)
        rv, rn = ricchezza(p)
        lette += bool(tv or tn or ti or nvv or nn or av or an or iv or inn or cv or cn or dv or dn or mv or mn
                      or pv or pn or L.leggi(p))
        viol += tv + nvv + cv + dv + av + iv + mv + pv + qv + bv + gv + ev + fv + lv + rv
        nv += tn + ti + nn + cn + dn + an + inn + mn + pn + qn + bn + gn + en_ + fn + ln + rn
    if a.json:
        json.dump({"schede": lette, "violazioni": viol, "non_verificabili": nv}, sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
    else:
        for v in viol:
            dove = f"{v['file']}:{v['riga']}" if v.get("riga") else v["file"]
            nome = f"{v['talento_it']} — manca " if v["verifica"] == "talenti" else ""
            print(f"{dove}: [{v['verifica']}] {nome}{v['testo']}  [regola {v['regola']}, fonte {v['fonte']}]")
        print(f"{'✗' if viol else '✓'} verifica_scheda: {lette} schede, {len(viol)} violazioni in "
              f"{len({v['file'] for v in viol})} schede, {len(nv)} voci non verificabili")
    return 1 if (a.check and viol) else 0


if __name__ == "__main__":
    sys.exit(main())
