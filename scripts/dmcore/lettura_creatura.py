"""dmcore.lettura_creatura — che cosa dice una scheda del Bestiario, letto una volta sola.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Il lettore degli statblocchi e della loro prosa: le espressioni regolari del
blocco, i dadi vita e il sospetto su `pf-dado`, le sestine delle caratteristiche
scritte nella scheda o nella fonte citata, i numeri della fonte, la composizione
dei DV, i talenti, la provenienza delle caratteristiche, e i **tetti** che un TS
scritto mette ai modificatori.

🔴 **Lo usa anche il verificatore** (D1, deciso dal DM il 2026-09-23): una
scheda si legge con lo stesso codice da chi genera e da chi verifica. Per questo
questo modulo non importa mai `dmcore.caratteristiche`, e
`test_grafo_import_creature.py` lo verifica. Quello che qui si ricava da un
numero scritto e' un limite, non una scelta: chi usa il limite per scegliere e'
`dmcore.caratteristiche`.

Solo stdlib.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from dmcore import tabelle as T
from dmcore.progressione import DADO_DI_CLASSE

__all__ = [
    "ORDINE", "TAGLIA", "BLOCCO", "CLASSE_NEL_TIPO", "taglia_di", "PF_DADO",
    "DV_DICHIARATI", "PEZZO_DADO", "BONUS_DADO", "MOD_MINIMO", "plausibile",
    "FORMULA_DV", "dadi_vita", "ROBUSTEZZA", "ROBUSTEZZA_MIGLIORATA", "robustezza",
    "pf_dado_sospetto", "CITAZIONE", "SESTINA", "PCG_STAT", "parole_del_file",
    "INTESTAZIONE", "sestine_citate", "dalla_scheda", "BAB_SCRITTO", "LOTTA_SCRITTA",
    "LOTTA_TAGLIA", "LOTTA_MIGLIORATA", "numeri_della_fonte", "INIZIATIVA_SCRITTA",
    "INIZIATIVA_MIGLIORATA", "senza_note", "MARCA", "CODA_FONTE", "CODA_SCHEDA",
    "CODA_ARRAY"
]

ROOT = Path(__file__).resolve().parents[2]


ORDINE = ("For", "Des", "Cos", "Int", "Sag", "Car")
#: I modificatori di taglia alla CA, per ricavare la Destrezza dalla CA di contatto.
TAGLIA = {nome: ca for nome, (_, ca) in T.TAGLIE.items()}
BLOCCO = re.compile(r"```statblocco\n(.*?)```", re.S)
#: Se il `tipo` nomina una classe, lo statblocco e' un PNG e gli array del
#: Manuale del DM sono lo strumento giusto. Se no, e' una creatura.
CLASSE_NEL_TIPO = re.compile(
    r"\b(" + "|".join(sorted(map(re.escape, DADO_DI_CLASSE), key=len, reverse=True))
    + r")\w*\s*\d+", re.I)


def taglia_di(testo: str) -> int:
    # 🐛 le schede di maggio scrivono la taglia in «**Size/Type**», non in
    # `tipo`: leggendo solo il campo, una creatura Grande pesava come Media, e
    # la Forza ricavata dalla lotta del razorfiend rosso usciva 30 invece di 22
    tipo = (re.search(r"^tipo:\s*(.+)$", testo, re.M)
            or re.search(r"\*\*Size/Type\*\*:?\s*([^|\n]+)", testo))
    if not tipo:
        # se nessuno la scrive, la dice il dettaglio della CA: «(-1 size, …)».
        # 🐛 Non la prosa: il primo «Medium …» del loxo sciamano e' il suo
        # compagno animale, e la creatura e' Grande.
        m = re.search(r"^ca-dettaglio:.*?([+-]\d)\s*(?:size|taglia)\b", testo, re.M | re.I)
        return int(m.group(1)) if m else 0
    basso = tipo.group(1).lower()
    for nome, val in TAGLIA.items():
        if re.search(rf"\b{nome}\b", basso):
            return val
    return 0


PF_DADO = re.compile(r"^pf-dado:\s*(.+)$", re.M)
DV_DICHIARATI = re.compile(r"\((\d+)\s*(?:HD|DV)\)|^tipo:.*?\b(\d+)\s*(?:HD|DV)\b", re.M)
PEZZO_DADO = re.compile(r"(\d+)d(\d+)")
BONUS_DADO = re.compile(r"([+-]\s*\d+)")
#: Sotto questo il modificatore non e' una Costituzione ma un `pf` scritto male.
MOD_MINIMO = -2


def plausibile(m: int, gs: float) -> bool:
    """Un modificatore **derivato** e' credibile solo se il GS lo regge.

    🐛 **La prima guardia era cieca al GS** (`-2 … +12`) e lasciava passare tre
    Costituzioni da 34: un duergar mago da GS 4, un loxo da GS 4, un ogre da
    GS 8. Tutti e tre per la stessa ragione — `pf-dado` registra solo i DV
    razziali di una creatura che ha anche livelli di classe — e tutti e tre
    con un +12 che nessuna creatura di quella sfida ha. Il tetto `3 + GS/2`
    lascia passare il +8 del bruto da GS 11 (`14d8`, 172 pf: e' vero) e
    respinge i tre.
    """
    return MOD_MINIMO <= m <= 3 + gs / 2


#: La formula dei DV scritta dal DM: «**DV 4d8 + 6d12**», «HD 2d8+2d8+8»,
#: «**HD**: 10d10+80». E' il dato piu' affidabile, perche' e' l'unico che
#: nomina **tutti** i dadi: in parecchi file `pf-dado` registrava i soli DV
#: razziali (`4d8` per un ogre con sei livelli da barbaro).
FORMULA_DV = re.compile(
    r"\b(?:DV|HD)\**:?\**\s*(\d+d\d+(?:\s*\+\s*\d+d\d+)*)(\s*[+-]\s*\d+(?!\s*d))?")


def dadi_vita(testo: str) -> "tuple[list, int | None, str] | None":
    """([(n, faccia)], bonus o None, da dove) — i dadi vita della creatura.

    In quest'ordine: la formula scritta, poi `pf-dado` se non e' sospetto.
    None se nessuno dei due c'e': ricostruirli dalle classi e' un altro
    passo, e chi lo fa lo deve dichiarare.
    """
    m = FORMULA_DV.search(testo)
    if m:
        dadi = [(int(a), int(b)) for a, b in PEZZO_DADO.findall(m.group(1))]
        bonus = int(m.group(2).replace(" ", "")) if m.group(2) else None
        return dadi, bonus, "formula scritta"
    md = PF_DADO.search(testo)
    if md and not pf_dado_sospetto(testo):
        dadi = [(int(a), int(b)) for a, b in PEZZO_DADO.findall(md.group(1))]
        resto = BONUS_DADO.findall(PEZZO_DADO.sub("", md.group(1)))
        return dadi, (sum(int(x.replace(" ", "")) for x in resto) if resto else None), "pf-dado"
    return None


ROBUSTEZZA = re.compile(r"\b(?:Toughness|Robustezza)\b(?!\s+Migliorata)", re.I)
ROBUSTEZZA_MIGLIORATA = re.compile(r"\b(?:Improved Toughness|Robustezza Migliorata)\b", re.I)


def robustezza(testo: str, dv: int) -> int:
    """I pf fissi dei talenti: Robustezza +3, Robustezza Migliorata +1 per DV.

    🐛 Contarle come lo stesso talento dava al duergar guerriero un bonus di 9
    invece di 8, e da quel 9 diviso per 2 DV usciva Cos 18 dove la fonte dice 16.
    """
    migliorata = ROBUSTEZZA_MIGLIORATA.search(testo)
    semplice = ROBUSTEZZA.search(ROBUSTEZZA_MIGLIORATA.sub("", testo))
    return (3 if semplice else 0) + (dv if migliorata else 0)


def pf_dado_sospetto(testo: str, gs: "float | None" = None) -> "str | None":
    """Perche' `pf-dado` **non** registra i dadi vita, o None se sembra farlo.

    🐛 **Il campo non sempre registra i dadi vita.** In 20 statblocchi su 95
    `pf-dado` porta **il danno dell'arma** — `1d8+7` accanto a «hp 93 (12
    HD)» e' il martello di Morlin — e la prima stesura del generatore ne
    ricavava Cos 24. Tre controlli, dal piu' certo al piu' indiziario; lo usa
    anche `validate_bestiario --rules`, perche' una norma ha un rilevatore.
    """
    md = PF_DADO.search(testo)
    if not md:
        return None
    pezzi = PEZZO_DADO.findall(md.group(1))
    dv = sum(int(a) for a, _ in pezzi)
    if not dv:
        return None
    if gs is None:
        # 🐛 chi chiamava senza GS saltava il terzo controllo, e `1d8+2` di un
        # chierico di 3° passava per dadi vita. Il GS sta nel blocco: si legge.
        mg = re.search(r"^gs:\s*([\d.,]+)", testo, re.M)
        gs = float(mg.group(1).replace(",", ".")) if mg else None
    # 0 · la formula scritta nomina altri dadi: il campo e' parziale o e' un'arma
    f = FORMULA_DV.search(testo)
    if f:
        scritti = sorted((int(a), int(b)) for a, b in PEZZO_DADO.findall(f.group(1)))
        if sorted((int(a), int(b)) for a, b in pezzi) != scritti:
            return (f"pf-dado «{md.group(1).strip()}» non ha i dadi della formula scritta "
                    f"«{f.group(1).strip()}»")
    # 1 · il testo dichiara i DV, e non tornano coi dadi
    dichiarati = DV_DICHIARATI.search(testo)
    if dichiarati:
        n = int(next(g for g in dichiarati.groups() if g))
        if n != dv:
            return (f"pf-dado «{md.group(1).strip()}» ha {dv} dad{'o' if dv == 1 else 'i'}, "
                    f"il testo dichiara {n} DV")
    # 2 · l'umanoide senza DV razziali tira solo il dado delle sue classi (SRD)
    tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M)
    if tipo and re.search(r"\bhumanoid|umanoide", tipo.group(1), re.I):
        attesi = {DADO_DI_CLASSE[c.lower()] for c in CLASSE_NEL_TIPO.findall(tipo.group(1))}
        facce = {int(b) for _, b in pezzi}
        if attesi and not (facce & attesi):
            return (f"pf-dado «{md.group(1).strip()}» in d{'/d'.join(map(str, sorted(facce)))}, "
                    f"ma le classi del tipo tirano d{'/d'.join(map(str, sorted(attesi)))}")
    # 3 · un dado solo a GS 2 o piu' e' quasi sempre un'arma (indizio, non prova)
    if gs is not None and dv == 1 and gs >= 2 and not dichiarati:
        return f"pf-dado «{md.group(1).strip()}» ha un dado solo a GS {gs:g}"
    return None


# ---------------------------------------------------------------------------
# La fonte citata in `Bestiario/pregen-pcgen/` (lo strato 0 di genera_attributi)
# ---------------------------------------------------------------------------
#: 🔴 **Lo strato che la prima stesura non aveva.** 42 dei 94 statblocchi
#: senza `attributi` citano un export in `Bestiario/pregen-pcgen/`, e 41 di
#: quelle fonti portano le sei caratteristiche in chiaro. Per quei file i
#: numeri **esistono**: generarli era inventare quello che bastava copiare.
CITAZIONE = re.compile(r"pregen-pcgen/[^)`|\]\n]*?\.(?:html?|pcg|txt)")
_V = r"(\d+|—|-(?!\s*\d))"     # un punteggio, o «—»; «-4» e' un modificatore, e si scarta
#: La sestina, in inglese (SRD, PCGen) **e in italiano** (le schede del DM:
#: «For 31, Des 13, Cos 23, Int 10, Sag 12, Car 11»). 🐛 La prima stesura
#: capiva solo l'inglese, e il bruto deforme, che scrive in italiano, finiva
#: all'array con la Forza ricavata da una lotta che dimentica un talento.
_SEP = r"\s*[,;]?\s*"
#: 🐛 **La parentesi dopo il punteggio.** L'ogre micelio scrive «For 25 (21
#: base +4 innesto), Des 8» e Zin'thara «Int 22 (20 + *fascia* +2)»: la regola
#: di prima non ammetteva niente fra il numero e la virgola, e le due schede
#: finivano all'array — Zin'thara, una maga, con Car 21 e Int 11. La
#: parentesi spiega il numero e non lo sostituisce: si salta, e il numero resta.
_NOTA = r"(?:\s*\([^)\n]{0,60}\))?"
SESTINA = re.compile(
    r"\b(?:Str|For)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"(?:Dex|Des)\w*\s*:?\s*" + _V + _NOTA +
    _SEP + r"(?:Con|Cos)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"Int\w*\s*:?\s*" + _V + _NOTA +
    _SEP + r"(?:Wis|Sag)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"(?:Cha|Car)\w*\s*:?\s*" + _V, re.I)
PCG_STAT = re.compile(r"^STAT:(STR|DEX|CON|INT|WIS|CHA)\|SCORE:(\d+)", re.M)
_PCG = ("STR", "DEX", "CON", "INT", "WIS", "CHA")


def _testo_fonte(p: Path) -> str:
    """Il testo della fonte, **con gli a capo**: servono a trovare le intestazioni."""
    t = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix in (".htm", ".html"):
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return t


def _punteggio(v: str):
    return "—" if v in ("—", "-") else int(v)


def _parole(testo: str) -> frozenset:
    """Le parole di un nome, senza numeri e senza plurale inglese."""
    fuori = set()
    for w in re.findall(r"[a-zà-ù]+", testo.lower()):
        if len(w) > 4 and w.endswith("s"):
            w = w[:-1]
        fuori.add(w)
    return frozenset(fuori)


def parole_del_file(nome_file: str) -> frozenset:
    radice = re.sub(r"-cr[\d.]+$", "", Path(nome_file).stem)
    return _parole(" ".join(t for t in radice.split("-") if not re.search(r"\d", t)))


INTESTAZIONE = re.compile(r"^\s*\d+[.)]\s+([A-Za-z][A-Za-z ,'-]{2,60}?)\s*$", re.M)


def sestine_citate(testo: str) -> "list[tuple[str, tuple, bool, frozenset]]":
    """(fonte, sestina in ORDINE, dedicata?, parole dell'intestazione) per fonte.

    *Dedicata* vuol dire che la fonte porta **una** sola sestina: e' la scheda
    di quella creatura, non un file che ne raccoglie parecchie. Per le altre
    conta l'**ultima intestazione numerata** prima della sestina («2. Myconid
    Elite Guards»): e' l'unico modo di sapere di chi e' senza indovinare.
    """
    fuori = []
    for rel in sorted(set(CITAZIONE.findall(testo))):
        p = ROOT / "Bestiario" / rel
        if not p.is_file():
            continue
        if p.suffix == ".pcg":
            s = dict(PCG_STAT.findall(p.read_text(encoding="utf-8", errors="replace")))
            if len(s) == 6:
                fuori.append((rel, tuple(int(s[k]) for k in _PCG), True, frozenset()))
            continue
        t = _testo_fonte(p)
        trovate = []
        for m in SESTINA.finditer(t):
            sestina = tuple(_punteggio(v) for v in m.groups())
            capi = INTESTAZIONE.findall(t, 0, m.start())
            trovate.append((sestina, _parole(capi[-1]) if capi else frozenset()))
        distinte = {x for x, _ in trovate}
        fuori += [(rel, x, len(distinte) == 1, capo) for x, capo in trovate]
    return fuori


def dalla_scheda(testo: str) -> "tuple[dict, str] | None":
    """Strato 0a: le caratteristiche **scritte nella scheda stessa**.

    🔴 **Lo strato che mancava anche alla seconda stesura**, trovato il
    2026-09-23 correggendo `pf-dado`: il sergente hobgoblin scrive
    «**Abilities**: Str 14, Dex 12, Con 14, Int 10, Wis 10, Cha 8» nella sua
    prosa, e il generatore gli aveva dato Car 17. **27 dei 55** file che ADR-0064
    contava come «scelti» avevano i numeri del DM scritti due righe sotto il
    blocco. Sono i numeri che si giocano: battono la fonte e battono i vincoli.

    Si legge fuori dal blocco e fuori dalle righe di marca, e solo se la
    scheda porta **una** sestina: due (una variante, un'ira) sono una scelta.
    """
    fuori = BLOCCO.sub("", testo)
    fuori = "\n".join(r for r in fuori.splitlines() if not r.startswith("> [INFERRED"))
    trovate = {tuple(_punteggio(v) for v in m) for m in SESTINA.findall(fuori)}
    if len(trovate) != 1:
        return None
    return dict(zip(ORDINE, trovate.pop())), "letta dalla riga delle caratteristiche della scheda stessa"


BAB_SCRITTO = re.compile(r"(?:\bBAB|Attacco base)(?:/(?:Grapple|Lotta))?\**:?\**\s*([+-]\d+)")
LOTTA_SCRITTA = re.compile(r"(?:\b(?:Lotta|Grapple)\**:?\**\s*([+-]\d+))|"
                           r"(?:BAB/(?:Grapple|Lotta)\**:?\**\s*[+-]\d+/\**([+-]\d+))")
#: SRD 3.5, modificatore speciale di taglia alla lotta.
LOTTA_TAGLIA = {8: -16, 4: -12, 2: -8, 1: -4, 0: 0, -1: 4, -2: 8, -4: 12, -8: 16}
LOTTA_MIGLIORATA = re.compile(r"\b(?:Improved Grapple|Lotta Migliorata|Lottare Migliorato)\b", re.I)


def numeri_della_fonte(testo: str) -> dict:
    """pf, TS, BAB e lotta come li scrive la prima fonte citata che li porta."""
    out = {}
    for rel in sorted(set(CITAZIONE.findall(testo))):
        p = ROOT / "Bestiario" / rel
        if not p.is_file():
            continue
        f = re.sub(r"\s+", " ", _testo_fonte(p))
        m = re.search(r"Fort\w*\s*:?\s*([+-]\d+),?\s*Ref\w*\s*:?\s*([+-]\d+),?\s*Will\s*:?\s*([+-]\d+)", f)
        if m:
            out.update(zip(("Temp", "Rifl", "Vol"), (int(x) for x in m.groups())))
        m = re.search(r"(?:Base Atk|Base Attack(?:/Grapple)?)\s*:?\s*([+-]\d+)(?:\s*/\s*([+-]\d+))?", f)
        if m:
            out["BAB"] = int(m.group(1))
            if m.group(2):
                out["lotta"] = int(m.group(2))
        m = re.search(r"\bGrp\s*([+-]\d+)", f)
        if m:
            out["lotta"] = int(m.group(1))
        m = re.search(r"\bhp\s*(\d+)", f)
        if m:
            out["pf"] = int(m.group(1))
        m = re.search(r"\bInit(?:iative)?\s*:?\s*([+-]?\d+)", f)
        if m:
            out["iniziativa"] = int(m.group(1))
        # PCGen: «+3 (1d10+3, Sword, bastard, Masterwork)» e' il primo attacco
        m = re.search(r"([+-]\d+)\s*\(\d+d\d+(?:[+-]\d+)?,\s*[A-Z]", f)
        if m:
            out["attacco"] = int(m.group(1))
    return out


INIZIATIVA_SCRITTA = re.compile(r"^iniziativa:\s*([+-]?\d+)", re.M)
INIZIATIVA_MIGLIORATA = re.compile(
    r"\b(?:Improved Initiative|Iniziativa(?:/[\w ]+?)? Migliorat[ao])\b", re.I)


def senza_note(testo: str) -> str:
    """Il testo senza le righe di marca, le errata e le note di fonte.

    🐛 Una marca che scrive «BAB +1 → **+0**» veniva letta come il BAB, e le
    errata del retriever («la prosa diceva BAB +10») pure. I numeri di una
    scheda si leggono solo dove la scheda li dichiara.
    """
    return "\n".join(r for r in testo.splitlines()
                     if not r.lstrip().startswith(("- ⚠", "fonte:", ">")))


#: La riga che marca un blocco **scritto da `genera_attributi`**. E' specifica: un
#: `[INFERRED` generico gia' presente nel file non basta, perche' parla
#: d'altro, e `--check` e `--rigenera` devono ritrovare esattamente i blocchi
#: suoi. La coda dice **da dove** vengono i numeri, file per file.
MARCA = "> [INFERRED — needs DM confirmation] `attributi` "
CODA_FONTE = ("trascritti dalla fonte citata in `Bestiario/pregen-pcgen/` da "
              "`scripts/genera_attributi.py`. Confermali o correggili.")
CODA_SCHEDA = ("copiati dalla riga delle caratteristiche di questa stessa scheda "
               "da `scripts/genera_attributi.py`.")
CODA_ARRAY = ("generati da `scripts/genera_attributi.py`: array del Manuale del DM "
              "con taglia e razza SRD, vincolati da CA e pf dove il file li "
              "dichiara. Confermali o correggili.")
