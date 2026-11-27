"""Chi si incontra sta nel capitolo dove lo si incontra (ADR-0107).

Il booklet stampa un capitolo così come il master lo scrive. Il master però
scrive la persona una volta sola: la scheda d'entrata nella scena dove entra,
il riquadro in un'appendice del master, la mappa in un'altra. Un capitolo preso
da un altro master (il barile di *Notte e Alba*) non ha niente. Con
`"chi_si_incontra": true` nel manifest (di solito con `"schede": "entrambe"`), prima di convertire il capitolo, questo
modulo:

1. non inventa la riga **Chi è**: presa dal titolo («il generale») ripeteva
   il titolo e basta (lettura cieca da DM, 2026-11-03). Va scritta nel master;
2. mette il riquadro ```statblocco della persona (con le righe di ADR-0091 e
   la sua **Tattica**) subito dopo la scheda d'entrata e il ritratto, se non
   è già lì vicino. Se il riquadro stava più in basso nello stesso capitolo,
   lo sposta e lascia una riga di rimando; se sta in un altro file, lo copia.
   L'appendice del volume li riporta comunque tutti;
3. dove una persona con una scheda si incontra (la riga **In scena … Chi:**
   di ADR-0073, o, in un capitolo senza quelle righe, il nome citato almeno
   `SOGLIA_CAPITOLO` volte) ma il capitolo non ha la sua scheda, porta scheda,
   ritratto e riquadro dal master che li ha;
4. dove il capitolo nomina una mappa («Mappa M7-C») e non la stampa, mette la
   pianta (e la sua legenda) dopo il paragrafo che la nomina la prima volta.

Lo usano l'esportatore (`export_booklet_typst.py`) e la misura
(`misura_standard_tavolo.py`): misurano lo stesso testo che va in stampa.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from dmcore.testo import piega_ascii

ROOT = Path(__file__).resolve().parents[2]

# Una persona si porta nel capitolo senza riga «In scena» solo se il capitolo
# la nomina almeno tante volte: sotto, è citata, non incontrata.
SOGLIA_CAPITOLO = 10

# Una mappa stampata più di tante righe del master dopo la scena che la usa è
# «in appendice»: al tavolo vuol dire girare decine di pagine.
LONTANO = 200

# I capitoli di consultazione (regia, cassetta, cast, appendici): nominano
# tutto, ma non è lì che si incontra qualcuno o si combatte.
CONSULTAZIONE = re.compile(r"regia|foglio della serata|cassetta|\bcast\b|introduzione|dove siamo|indice|glossario|appendice|ponte",
                           re.I)

_TITOLI = {
    "re", "regina", "principe", "principessa", "sorella", "fratello", "padre", "madre",
    "mastro", "maestra", "maestro", "costruttore", "capitano", "capitana", "lord", "lady",
    "ser", "sir", "dama", "gran", "grande", "sommo", "somma", "alto", "alta", "il", "la",
    "lo", "gli", "le", "i", "l", "conte", "contessa", "duca", "generale", "sacerdote",
    "sacerdotessa", "vecchio", "vecchia", "giovane", "zio", "zia", "nonno", "nonna",
}

_ENTRATA = re.compile(r"^\*\*Scheda d'entrata\s*[—–-]\s*(?P<nome>[^*]+?)\*\*(?P<resto>.*)$")
_IMMAGINE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
_IN_SCENA = re.compile(r"^\*\*In scena\*\*.*?Chi:\s*(?P<chi>.+)$")
_ETICHETTE_SB = ("**Iniziativa", "**Difesa", "**Attacco", "**Statistiche",
                 "**Capacità", "**Tattic", "**Sensi")
_CODICE_MAPPA = re.compile(r"(?<![\w/-])(M\d+-[A-Z]{1,2})(?![\w-])")
_SCONTRO = re.compile(r"```statblocco|\binizia(?:tiva)\b|\btattic", re.I)
_ALT_MAPPA = re.compile(r"^(M\d+-[A-Z]{1,2})\b")


def chiave(nome: str) -> str:
    """La parola che distingue una persona: la prima che non è un titolo.

    >>> chiave("Zog'tar Deatheye, il generale")
    'zogtar'
    >>> chiave("Mastro Costruttore Zeth")
    'zeth'
    """
    testa = nome.split(",")[0]
    for parola in re.findall(r"[\w'’]+", testa):
        p = piega_ascii(parola).lower().replace("'", "").replace("’", "")
        if p and p not in _TITOLI and len(p) > 2:
            return p
    return ""


def piega(s: str) -> str:
    return piega_ascii(s).lower().replace("'", "").replace("’", "")


def conta(testo: str, k: str) -> int:
    return len(re.findall(rf"(?<![a-z0-9]){re.escape(k)}(?![a-z0-9])", piega(testo)))


# ── i pezzi del master ───────────────────────────────────────────────────────

@dataclass
class Pezzo:
    """Righe [inizio, fine) di un file, col file da cui vengono."""
    file: Path
    inizio: int
    fine: int
    righe: list[str]
    nome: str = ""


def _fine_titolo(righe: list[str], i: int) -> int:
    """Il titolo di una scheda d'entrata può andare a capo: «*(statistiche:\\nAppendice A)*»."""
    j = i
    while j + 1 < len(righe) and righe[j + 1].strip() and not righe[j + 1].startswith("|") \
            and j - i < 3:
        j += 1
    return j


def _segno_di_blocco(riga: str) -> bool:
    """`<!-- blocco: nome -->` o `<!-- /blocco -->` di `componenti.py --includi`.

    >>> _segno_di_blocco("<!-- blocco: zogtar-chi -->"), _segno_di_blocco("<!-- /blocco -->")
    (True, True)
    >>> _segno_di_blocco("| **Aspetto** | mezzo-ogre |")
    False
    """
    r = riga.strip()
    return r.startswith("<!--") and r.endswith("-->") and "blocco" in r


def schede_entrata(righe: list[str], f: Path) -> list[Pezzo]:
    """Ogni scheda d'entrata: titolo, tabella e il ritratto che la segue."""
    fuori = []
    for i, r in enumerate(righe):
        m = _ENTRATA.match(r)
        if not m:
            continue
        j = _fine_titolo(righe, i) + 1
        # le righe vuote e i segni di blocco (`<!-- blocco: zogtar-chi -->`,
        # che `componenti.py --includi` usa per copiare la tabella) non contano
        while j < len(righe) and (not righe[j].strip() or _segno_di_blocco(righe[j])):
            j += 1
        if j >= len(righe) or not righe[j].startswith("|"):
            continue
        while j < len(righe) and righe[j].startswith("|"):
            j += 1
        if j < len(righe) and _segno_di_blocco(righe[j]):
            j += 1
        # il ritratto, se viene subito dopo
        k = j
        while k < len(righe) and not righe[k].strip():
            k += 1
        if k < len(righe) and _IMMAGINE.match(righe[k]) and "Mappe/" not in righe[k]:
            j = k + 1
        fuori.append(Pezzo(f, i, j, righe[i:j], m.group("nome").strip()))
    return fuori


def statblocchi(righe: list[str], f: Path) -> list[Pezzo]:
    """Ogni ```statblocco con le righe di ADR-0091 che lo seguono (Difesa … Tattiche)."""
    fuori = []
    i = 0
    while i < len(righe):
        if righe[i].strip() != "```statblocco":
            i += 1
            continue
        j = i + 1
        while j < len(righe) and not righe[j].strip().startswith("```"):
            j += 1
        nome = next((r.split(":", 1)[1].strip() for r in righe[i + 1:j] if r.startswith("nome:")), "")
        j += 1
        fine = j
        k = j
        while k < len(righe):
            r = righe[k]
            if not r.strip():
                k += 1
                continue
            if r.startswith(_ETICHETTE_SB) or (k > fine and r.startswith(("- ", "  ")) and fine > j):
                # una sezione: fino alla riga vuota
                while k < len(righe) and righe[k].strip():
                    k += 1
                fine = k
                continue
            break
        fuori.append(Pezzo(f, i, fine, righe[i:fine], nome))
        i = fine
    return fuori


@dataclass
class Indice:
    entrate: dict[str, Pezzo] = field(default_factory=dict)
    riquadri: dict[str, Pezzo] = field(default_factory=dict)
    mappe: dict[str, list[tuple[str, Path]]] = field(default_factory=dict)


def _priorita(f: Path, root: Path = ROOT) -> int:
    """I master prima delle copie: un booklet .hb.md o un piano ricopiano il master."""
    rel = f.relative_to(root).as_posix()
    if rel.startswith("plans/") or "_ARCHIVIO" in rel or rel.startswith("build/"):
        return 3
    if f.name.endswith(".hb.md") or "/homebrew/" in rel:
        return 2
    if rel.startswith("Bestiario/"):
        return 1
    return 0


def indice_del_repo(root: Path = ROOT) -> Indice:
    """Schede d'entrata, riquadri di chi ha un nome e mappe con un codice, dal master che li ha."""
    idx = Indice()
    file = []
    for f in root.rglob("*.md"):
        rel = f.relative_to(root).as_posix()
        if rel.startswith(("build/", "node_modules/", ".git/")) or "_ARCHIVIO" in rel:
            continue
        file.append(f)
    file.sort(key=lambda f: (_priorita(f, root), f.as_posix()))
    for f in file:
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "Scheda d'entrata" not in testo and "```statblocco" not in testo and "Mappe/" not in testo:
            continue
        righe = testo.split("\n")
        for p in schede_entrata(righe, f):
            k = chiave(p.nome)
            if k:
                idx.entrate.setdefault(k, p)
        for p in statblocchi(righe, f):
            k = chiave(p.nome)
            if k:
                idx.riquadri.setdefault(k, p)
        for r in righe:
            m = _IMMAGINE.match(r)
            if m and "Mappe/" in m.group(2):
                c = _ALT_MAPPA.match(m.group(1))
                dove = (f.parent / m.group(2)).resolve()
                # solo piante che esistono e da un master o un booklet, non da un piano
                if c and dove.is_file() and _priorita(f, root) < 3:
                    lst = idx.mappe.setdefault(c.group(1), [])
                    if dove not in [d for _, d in lst]:
                        lst.append((m.group(1), dove))
    # un riquadro vale per una persona solo se quella persona ha un nome
    # (una scheda d'entrata): «Guardia hobgoblin» non è nessuno
    idx.riquadri = {k: v for k, v in idx.riquadri.items() if k in idx.entrate}
    return idx


# ── il capitolo arricchito ───────────────────────────────────────────────────

def _riscrivi_percorsi(righe: list[str], da: Path, a: Path) -> list[str]:
    """Le immagini di un pezzo preso da `da` puntano giuste anche da `a`."""
    if da.parent.resolve() == a.parent.resolve():
        return list(righe)

    def sost(m: re.Match) -> str:
        p = m.group(2)
        if re.match(r"^[a-z]+://", p) or p.startswith("/"):
            return m.group(0)
        assoluto = (da.parent / p).resolve()
        return f"![{m.group(1)}]({os.path.relpath(assoluto, a.parent.resolve())})"
    return [re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", sost, r) for r in righe]


def _statistiche_qui(titolo: list[str]) -> list[str]:
    testo = "\n".join(titolo)
    testo = re.sub(r"\*\(statistiche:[^)]*\)\*", "*(statistiche: qui sotto)*", testo, flags=re.S)
    return testo.split("\n")


def _altrove(volume: "dict | None", k: str) -> bool:
    """Presentato in un capitolo prima di questo (stato di «prima-volta»)."""
    return volume is not None and volume["persone"].get(k) not in (None, volume["capitolo"])


def _rimando_persona(nome: str, dove: str, entrata: list[str] | None = None) -> list[str]:
    """La persona già presentata, come il paragrafo «Creature» di un AP:
    l'aspetto e quel che vuole in due righe, il resto dov'è.

    >>> _rimando_persona("Durin, la pattuglia", "capitolo II",
    ...                  ["| **Aspetto** | veterano |", "| **Vuole** | tornare |", "| **Sa** | x |"])[:2]
    ["**Scheda d'entrata — Durin, in breve** *(intera, con chi è e ritratto, nel capitolo II)*", '']
    """
    corto = nome.split(",")[0].strip()
    campi = []
    for r in entrata or []:
        m = re.match(r"^\|\s*\*\*(Aspetto|Vuole)\*\*\s*\|\s*(.*?)\s*\|?\s*$", r)
        if m:
            # la prima frase: un promemoria, non la scheda ripetuta
            frase = m.group(2) if len(m.group(2)) <= 160 else \
                re.split(r"(?<=[.!?»])\s+(?=[A-ZÀ-Ú«*])", m.group(2), maxsplit=1)[0]
            frase = frase.rstrip(" .")
            campi += [f"**{m.group(1)}** {frase}.", ""]
    if not campi:
        return [f"*{corto}: chi è, aspetto e ritratto nel {dove}; "
                f"qui sotto la riga per il tavolo e la tattica di questo incontro.*", ""]
    return [f"**Scheda d'entrata — {corto}, in breve** *(intera, con chi è e ritratto, nel {dove})*",
            "", *campi]


def _solo_riquadro(k: str, idx: Indice, f: Path, volume: "dict | None" = None) -> list[str]:
    # «prima-volta»: il riquadro è quello con cui la persona è stata
    # presentata nel volume (il drago di stasera, non quello del master)
    if volume is not None and k in volume.get("riquadri", {}):
        righe, da = volume["riquadri"][k]
        return _riscrivi_percorsi(righe, da, f) + [""]
    if k not in idx.riquadri:
        return []
    q = idx.riquadri[k]
    return _riscrivi_percorsi(q.righe, q.file, f) + [""]


def mappe_stampate(md: str) -> list[str]:
    """I codici delle mappe che un capitolo stampa di suo (un'immagine da `Mappe/`)."""
    fuori = []
    for r in md.split("\n"):
        m = _IMMAGINE.match(r)
        if m and "Mappe/" in m.group(2) and (c := _ALT_MAPPA.match(m.group(1))):
            if c.group(1) not in fuori:
                fuori.append(c.group(1))
    return fuori


def arricchisci(md: str, f: Path, idx: Indice, pg: set[str] = frozenset(),
                soglia: int = SOGLIA_CAPITOLO, volume: "dict | None" = None) -> tuple[str, list[str]]:
    """Il capitolo con chi si incontra e le mappe che nomina. Torna anche un
    elenco di quel che ha fatto, una riga per mossa, per il rapporto.

    `volume` (manifest con `"schede": "prima-volta"`, ADR-0122): lo stato del
    volume, `{"capitolo": "cap. V", "persone": {chiave: capitolo},
    "mappe": {codice: capitolo}}`. Chi è già stato presentato in un capitolo
    prima non si ripresenta: una riga di rimando e il riquadro, che il tema
    stampa come riga con la pagina e la tattica. Una mappa già stampata prima
    non si copia: una riga dice dove sta. Senza `volume`, ADR-0107 com'era.

    Non si chiama sui capitoli di consultazione (`CONSULTAZIONE`): la regia e
    la cassetta nominano tutti, ma lì non si incontra nessuno."""
    f = f.resolve()
    righe = md.split("\n")
    fatto: list[str] = []

    # 2. ogni scheda d'entrata del capitolo: il riquadro accanto
    entrate = schede_entrata(righe, f)
    riquadri = {chiave(p.nome): p for p in statblocchi(righe, f)}
    inserimenti: list[tuple[int, list[str]]] = []   # (dopo la riga, righe nuove)
    sostituzioni: dict[int, Pezzo] = {}             # pezzi da rimpiazzare
    rimandi: dict[int, tuple[int, list[str]]] = {}
    for p in entrate:
        k = chiave(p.nome)
        if not k or k in pg:
            continue
        p2 = Pezzo(p.file, p.inizio, p.fine, p.righe, p.nome)
        sostituzioni[p.inizio] = p2
        if _altrove(volume, k):
            sb = riquadri.get(k)
            p2.righe = _rimando_persona(p.nome, volume["persone"][k], p.righe) + \
                ([] if sb is not None else _solo_riquadro(k, idx, f, volume))
            fatto.append(f"già presentato, rimando: {p.nome.split(',')[0]}")
            continue
        if volume is not None:
            volume["persone"].setdefault(k, volume["capitolo"])
        nuovo = list(p.righe)
        sb = riquadri.get(k)
        vicino = sb is not None and 0 <= sb.inizio - p.fine < 60
        if not vicino:
            if sb is not None:
                # più in basso nello stesso capitolo: si sposta accanto
                rimandi[sb.inizio] = (sb.fine, [f"*{sb.nome.split(',')[0]}: il riquadro è accanto alla "
                                                  f"sua scheda d'entrata.*", ""])
                blocco = sb.righe
                fatto.append(f"riquadro spostato accanto alla scheda: {p.nome.split(',')[0]}")
            elif k in idx.riquadri:
                q = idx.riquadri[k]
                blocco = _riscrivi_percorsi(q.righe, q.file, f)
                fatto.append(f"riquadro copiato da {q.file.name}: {p.nome.split(',')[0]}")
            else:
                blocco = []
            if blocco:
                testa = _fine_titolo(nuovo, 0) + 1
                nuovo = _statistiche_qui(nuovo[:testa]) + nuovo[testa:] + [""] + blocco
        if nuovo != p.righe:
            p2.righe = nuovo

    # «prima-volta»: chi ha il riquadro in questo capitolo è presentato qui
    # (il capitolo «Chi c'è stanotte» ha le schede senza titolo d'entrata)
    if volume is not None:
        for k, sb in riquadri.items():
            if k and k not in pg:
                volume["persone"].setdefault(k, volume["capitolo"])
                volume.setdefault("riquadri", {}).setdefault(k, (list(sb.righe), sb.file))

    # 3. chi si incontra e non ha la scheda nel capitolo
    nel_capitolo = {chiave(p.nome) for p in entrate}
    portati: set[str] = set()
    for i, r in enumerate(righe):
        m = _IN_SCENA.match(r)
        if not m:
            continue
        nuovi: list[str] = []
        for nome in re.split(r"\s*·\s*", m.group("chi")):
            k = chiave(nome)
            if not k or k in pg or k in nel_capitolo or k in portati or k not in idx.entrate:
                continue
            portati.add(k)
            if _altrove(volume, k):
                nuovi += _rimando_persona(idx.entrate[k].nome, volume["persone"][k],
                                          idx.entrate[k].righe) + \
                    ([] if k in riquadri else _solo_riquadro(k, idx, f, volume))
                fatto.append(f"già presentato, rimando nella scena: {idx.entrate[k].nome.split(',')[0]}")
                continue
            if volume is not None:
                volume["persone"].setdefault(k, volume["capitolo"])
            nuovi += _pezzo_portato(k, idx, f)
            fatto.append(f"scheda portata nella scena: {idx.entrate[k].nome.split(',')[0]}")
        if nuovi:
            inserimenti.append((i, [""] + nuovi))
    if not any(_IN_SCENA.match(r) for r in righe):
        candidati = sorted((k for k in idx.entrate
                            # chi ha già il riquadro nel capitolo c'è già (il
                            # capitolo «Chi c'è stanotte» della #305)
                            if k not in pg and k not in nel_capitolo and k not in riquadri
                            and conta(md, k) >= soglia),
                           key=lambda k: -conta(md, k))
        if candidati:
            testa = next((i for i, r in enumerate(righe) if r.startswith("# ")), -1)
            blocco = ["", "### Chi si incontra in questo capitolo", ""]
            for k in candidati:
                if _altrove(volume, k):
                    blocco += _rimando_persona(idx.entrate[k].nome, volume["persone"][k],
                                               idx.entrate[k].righe) + \
                        _solo_riquadro(k, idx, f, volume)
                    continue
                if volume is not None:
                    volume["persone"].setdefault(k, volume["capitolo"])
                blocco += _pezzo_portato(k, idx, f) + [""]
                fatto.append(f"scheda portata in testa al capitolo: {idx.entrate[k].nome.split(',')[0]}")
            inserimenti.append((testa, blocco))

    # 4. le mappe nominate e non stampate, o stampate lontano (l'Appendice D
    # di un master sta quaranta pagine dopo la scena). Va dopo il paragrafo
    # «**Mappa M7-C**» della scena, se c'è; se no dopo la prima volta che il
    # capitolo la nomina.
    stampata_a: dict[str, int] = {}
    for i, r in enumerate(righe):
        m = _IMMAGINE.match(r)
        if m and "Mappe/" in m.group(2) and (c := _ALT_MAPPA.match(m.group(1))):
            stampata_a.setdefault(c.group(1), i)
    dove_va = punti_delle_mappe(righe, set(idx.mappe)) if _SCONTRO.search(md) else {}
    if volume is not None:
        for c in stampata_a:
            volume["mappe"].setdefault(c, volume["capitolo"])
    for c, i in sorted(dove_va.items(), key=lambda x: x[1]):
        # già stampata prima del punto, o poco dopo: niente copia
        if c in stampata_a and stampata_a[c] - i < LONTANO:
            continue
        nativa = (volume or {}).get("native", {}).get(c)
        if volume is not None and c not in stampata_a and nativa and nativa != volume["capitolo"]:
            # la mappa ha il suo posto in un altro capitolo del volume, anche
            # più avanti (la pianta del duello accanto al duello): lì e basta
            j = i
            while j + 1 < len(righe) and righe[j + 1].strip():
                j += 1
            inserimenti.append((j, ["", f"*La mappa {c} è nel {nativa}, e intera "
                                        f"nell'appendice delle mappe in fondo.*"]))
            fatto.append(f"mappa {c}: rimando al {nativa}")
            continue
        if volume is not None and c in volume["mappe"] and c not in stampata_a:
            j = i
            while j + 1 < len(righe) and righe[j + 1].strip():
                j += 1
            inserimenti.append((j, ["", f"*La mappa {c} è nel {volume['mappe'][c]}, e intera "
                                        f"nell'appendice delle mappe in fondo.*"]))
            fatto.append(f"mappa {c}: rimando al {volume['mappe'][c]}")
            continue
        if volume is not None:
            volume["mappe"].setdefault(c, volume["capitolo"])
        j = i
        while j + 1 < len(righe) and righe[j + 1].strip():
            j += 1
        nuove = [""]
        for alt, dove in idx.mappe[c]:
            nuove += [f"![{alt}]({os.path.relpath(dove, f.parent)})", ""]
        inserimenti.append((j, nuove))
        fatto.append(f"mappa {c} nel capitolo" + (" (copia: l'originale è lontano)" if c in stampata_a else ""))

    # il testo nuovo, in un passo solo
    dopo: dict[int, list[str]] = {}
    for i, nuove in inserimenti:
        dopo.setdefault(i, []).extend(nuove)
    fuori: list[str] = []
    if -1 in dopo:
        fuori += dopo[-1]
    i = 0
    while i < len(righe):
        if i in sostituzioni:
            p = sostituzioni[i]
            fuori += p.righe
            i = p.fine
            if i - 1 in dopo:
                fuori += dopo[i - 1]
            continue
        if i in rimandi:
            fine, testo = rimandi[i]
            fuori += testo
            i = fine
            continue
        fuori.append(righe[i])
        if i in dopo:
            fuori += dopo[i]
        i += 1
    if volume is not None:
        fuori = tattiche_locali(fuori, f, fatto)
    return "\n".join(fuori), fatto


_TITOLO_TATTICA = re.compile(
    r"^(?:#{2,6}\s+(?P<h>.*?(?:[Tt]attic|[Cc]ome (?:si )?combatte).*?)\s*$"
    r"|\*\*(?P<b>(?:[Tt]attic|[Cc]ome (?:si )?combatte)[^*]*)\*\*)")


def _tattiche_del_capitolo(righe: list[str], f: Path) -> list[tuple[str, str]]:
    """I paragrafi di tattica scritti nella scena (non le righe «**Tattiche**»
    dei riquadri): (titolo, testo fino al titolo dopo, al massimo 15 righe).

    >>> _tattiche_del_capitolo(["**Come combatte sulla breccia**. Zog'tar sale."], Path("x.md"))
    [('Come combatte sulla breccia', "**Come combatte sulla breccia**. Zog'tar sale.")]
    """
    dentro: set[int] = set()
    for sb in statblocchi(righe, f):
        dentro.update(range(sb.inizio, sb.fine))
    fuori = []
    for i, r in enumerate(righe):
        if i in dentro or (m := _TITOLO_TATTICA.match(r)) is None:
            continue
        titolo = re.sub(r"[^\w'’»«)(—,. -]", "", m.group("h") or m.group("b")).strip(" .:—")
        titolo = re.sub(r"\s*\((?:stile|aggancio)[^)]*\)", "", titolo).strip()
        # il paragrafo fino al titolo dopo (una tabella «Chi | Round 1 …» compresa)
        j = i + 1
        while j < len(righe) and j < i + 16 and not righe[j].startswith("#"):
            j += 1
        fuori.append((titolo, "\n".join(righe[i:j])))
    return fuori


def tattiche_locali(righe: list[str], f: Path, fatto: list[str] | None = None) -> list[str]:
    """«prima-volta» (ADR-0122): nella riga per il tavolo la tattica deve
    essere quella di QUESTO incontro, come negli Adventure Path. Se il
    capitolo ha un paragrafo di tattica che nomina la creatura, la riga
    «**Tattiche**» del suo riquadro rimanda lì invece di ripetere quella
    generale della scheda (che resta intera nell'appendice).

    >>> r = ["```statblocco", "nome: Zog'tar Deatheye", "```",
    ...      "**Tattiche** La tenda della Scena 8.", "", "**Come combatte sulla breccia**",
    ...      "Zog'tar sale."]
    >>> tattiche_locali(r, Path("x.md"))[3]
    '**Tattiche** In questo incontro: «Come combatte sulla breccia», qui sotto nel capitolo.'
    """
    locali = _tattiche_del_capitolo(righe, f)
    if not locali:
        return righe
    fuori = list(righe)
    for sb in statblocchi(righe, f):
        k = chiave(sb.nome)
        if not k:
            continue
        titolo = next((t for t, testo in locali
                       if k in piega_ascii(testo).lower().replace("'", "").replace("’", "")), None)
        if titolo is None:
            continue
        riga = f"**Tattiche** In questo incontro: «{titolo}», qui sotto nel capitolo."
        posto = next((i for i in range(sb.inizio, sb.fine) if fuori[i].startswith("**Tattic")), None)
        if posto is None:
            fine = sb.fine
            while fine > sb.inizio and not fuori[fine - 1].strip():
                fine -= 1
            fuori.insert(fine, "")
            fuori.insert(fine + 1, riga)
            # le posizioni dopo si spostano di due: si rifà il giro
            return tattiche_locali(fuori, f, fatto) if fatto is None else \
                _ancora(fuori, f, fatto, sb.nome)
        if fuori[posto] != riga:
            fuori[posto] = riga
            if fatto is not None:
                fatto.append(f"tattica di questo incontro: {sb.nome.split(',')[0]} → «{titolo}»")
    return fuori


def _ancora(righe: list[str], f: Path, fatto: list[str], nome: str) -> list[str]:
    fatto.append(f"tattica di questo incontro: {nome.split(',')[0]} (aggiunta)")
    return tattiche_locali(righe, f, fatto)


def punti_delle_mappe(righe: list[str], codici: set[str]) -> dict[str, int]:
    """Per ogni mappa nominata dal testo, la riga dove serve: il paragrafo
    «**Mappa M7-C**» della scena, se c'è; se no la prima volta che la nomina.
    Le tabelle, le immagini e i recinti non contano; una citazione conta solo
    se comincia col rimando alla mappa.

    >>> punti_delle_mappe(["vedi M1-A.", "", "**Mappa M1-A** (App. D)."], {"M1-A"})
    {'M1-A': 2}
    >>> punti_delle_mappe(["vedi M1-B.", "", "> **Mappa M1-B.** Il drago entra."], {"M1-B"})
    {'M1-B': 2}
    """
    dove: dict[str, int] = {}
    for i, r in enumerate(righe):
        if r.startswith(("![", "|", "```")):
            continue
        for c in _CODICE_MAPPA.findall(r):
            if c not in codici:
                continue
            # «**Mappa M7-C**», «> **Mappa M7-B.**», «> Mappa **M7-A**»: il
            # rimando della scena, anche dentro una citazione, vince
            if re.match(rf"^(?:>\s*)?(?:\*\*Mappa\s+\**{re.escape(c)}\b|Mappa\s+\*\*{re.escape(c)}\*\*)", r):
                dove[c] = i
            elif not r.startswith(">"):
                dove.setdefault(c, i)
    return dove


def _pezzo_portato(k: str, idx: Indice, f: Path) -> list[str]:
    e = idx.entrate[k]
    pezzo = _riscrivi_percorsi(e.righe, e.file, f)
    if k in idx.riquadri:
        q = idx.riquadri[k]
        testa = _fine_titolo(pezzo, 0) + 1
        pezzo = _statistiche_qui(pezzo[:testa]) + pezzo[testa:] + [""] + \
            _riscrivi_percorsi(q.righe, q.file, f)
    return pezzo + [""]
