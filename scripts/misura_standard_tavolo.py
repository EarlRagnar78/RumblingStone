#!/usr/bin/env python3
"""misura_standard_tavolo.py — il DM trova chi ha davanti nel capitolo dove lo incontra?

## Perché esiste

La sera del 2026-11-02, al tavolo con il booklet di *Notte e Alba*, il DM ha
cercato Zog'tar nel capitolo del barile e non c'era niente: la descrizione
stava a p. 54, in un altro capitolo, e la scheda in appendice aveva solo i
numeri. Le mappe del capitolo stavano in un'appendice di un altro capitolo.
Tutti i validatori erano verdi. Poi ha fissato lo standard minimo:

> *«per ogni capitolo accanto alla scheda una descrizione, una sua immagine e
> chi è e cosa vuole credo sia il minimo standard sindacale da adottare»*

Questo script misura quello standard sul booklet **così come va in stampa**,
capitolo per capitolo. È la stessa idea della *control panel* di Questing
Beast e del *Universal NPC Roleplaying Template* dell'Alexandrian (aspetto,
battuta, come si interpreta, cosa sa, statistiche: una scheda sola, nel
punto in cui serve). Le fonti e il confronto stanno in
`plans/RICERCA-USABILITA-AL-TAVOLO-2026-11.md`.

## Cosa conta

Per ogni booklet del DM (i manifest con capitoli `"tag": "dm"`) e per ogni
capitolo, le **persone** che ci compaiono: un PNG o un cattivo con un nome
(ha una *Scheda d'entrata* da qualche parte nel repo, o un dossier in
`Bestiario/png` o `Bestiario/villain`, e un riquadro ```statblocco o una
scheda d'entrata nel booklet). Compare in un capitolo se il suo nome vi
ricorre almeno `--soglia` volte (3). Per ciascuna coppia capitolo × persona:

| colonna | c'è se, nello stesso capitolo… |
|---|---|
| `num` | il riquadro ```statblocco della persona; in un volume con le schede solo in appendice (ADR-0105 §7) conta come `rimando`; con `"schede": "qui"` o `"entrambe"` (ADR-0107) come `qui` |
| `asp` | una riga o sezione **Aspetto** (scheda d'entrata o dossier) dopo il nome |
| `img` | un'immagine con il nome nella didascalia o nel file |
| `chi` | una riga o sezione **Chi è** / **In breve** / **Ruolo** |
| `vuole` | una riga o sezione **Vuole** / **Cosa vuole** / **Motivation** |
| `tatt` | le **Tattiche** del suo riquadro, o una tabella o un paragrafo di tattiche col suo nome |

`completa` vuol dire tutte e sei (con `num` anche come `rimando`).
Per ogni capitolo con uno scontro (un riquadro, o le parole *iniziativa* o
*tattiche*), la colonna `mappa` dice se c'è una mappa (un'immagine da
`Mappe/`) nel capitolo vicino a dove la nomina, una mappa stampata nel
capitolo ma lontana (`lontana`: più di 200 righe del master dopo, come
l'Appendice D di un master), solo un rimando («Mappa M7-C», «Appendice D») o
niente.

## Cosa NON misura, dichiarato

- La qualità: una riga «Aspetto» di tre parole conta come una di tre righe.
  Se la descrizione si capisce al volo lo dice solo la lettura da DM.
- La comparsa è contata sul nome: un pronome, un epiteto («il generale»)
  o un nome scritto diverso non contano. Una persona citata tre volte in un
  capitolo dove non si incontra conta lo stesso: per questo il numero è un
  indicatore da leggere col dettaglio, non un cancello a zero.
- Le creature senza nome (guardie, wyvern) non hanno «chi è» né «cosa
  vuole»: stanno fuori dalla tabella delle persone e contano solo nella
  colonna `mappa`.
- Il volume dei giocatori e i capitoli `"layout": "schede"` non contano.

## Uso

    python3 scripts/misura_standard_tavolo.py                 # una riga per booklet
    python3 scripts/misura_standard_tavolo.py --dettaglio     # capitolo × persona, con cosa manca
    python3 scripts/misura_standard_tavolo.py --manifest PATH # un booklet solo
    python3 scripts/misura_standard_tavolo.py --json

Exit: 0 sempre (è un indicatore; il cancello, se il DM lo vorrà, è un altro passo).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import chi_si_incontra  # noqa: E402
from dmcore.testo import (  # noqa: E402
    capitoli_del_volume, leggi_per_la_stampa, piega_ascii, togli_storico, traduci_rimandi,
)

CAMPI = ("num", "asp", "img", "chi", "vuole", "tatt")

# Titoli e parole che stanno davanti al nome e non lo distinguono.
_TITOLI = {
    "re", "regina", "principe", "principessa", "sorella", "fratello", "padre", "madre",
    "mastro", "maestra", "maestro", "costruttore", "capitano", "capitana", "lord", "lady",
    "ser", "sir", "dama", "gran", "grande", "sommo", "somma", "alto", "alta", "il", "la",
    "lo", "gli", "le", "i", "l", "conte", "contessa", "duca", "generale", "sacerdote",
    "sacerdotessa", "vecchio", "vecchia", "giovane", "zio", "zia", "nonno", "nonna",
}

# Nomi propri che non sono una persona da incontrare: divinità citate, oggetti
# con un nome («Aegis» di Aegis-fang), gruppi. Si allunga a mano, e il
# rapporto lo dice.
_NON_PERSONE = {"moradin", "abbathor", "gruumsh", "lolth", "dumathoin", "clangeddin",
                "berronar", "tymora", "torm", "tempus", "helm", "lathander", "mystra",
                "kossuth", "maglubiyet", "hruggek", "aegis",
                # i dossier di gruppo, che ADR-0091 §3 tiene fuori dalle schede
                "consiglio", "secondo", "profughi", "witchwood", "tiri", "zhentarim",
                # il segnaposto del modello di scheda d'entrata
                "nome"}

# I capitoli di consultazione (regia, cast, introduzione, appendici) non sono
# il punto in cui si incontra qualcuno: le coppie si contano negli altri.
_CONSULTAZIONE = chi_si_incontra.CONSULTAZIONE

_SCHEDA_ENTRATA = re.compile(r"\*\*Scheda d'entrata\s*[—–-]\s*([^*]+?)\*\*")
_NOME_BLOCCO = re.compile(r"^nome:\s*(.+)$", re.M)
_IMMAGINE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_RIGA_CAMPO = r"(?:^\|\s*\*\*{k}\*\*|^\*\*{k}\b|^#{{2,4}}\s*{k}\b|^-\s*\*\*{k}\b)"
_ASPETTO = re.compile(_RIGA_CAMPO.format(k=r"(?:Aspetto|Descrizione|Com'è)"), re.M | re.I)
_CHI = re.compile(_RIGA_CAMPO.format(k=r"(?:Chi è|In breve|Ruolo|Role)"), re.M | re.I)
_VUOLE = re.compile(_RIGA_CAMPO.format(k=r"(?:Vuole|Cosa vuole|Motivation|Motivazione)"), re.M | re.I)
_TATTICHE = re.compile(r"Tattic", re.I)
_SCONTRO = re.compile(r"```statblocco|\binizia(?:tiva)\b|\btattic", re.I)
_RIMANDO_MAPPA = re.compile(r"\bMappa\s+M\d|\bAppendice\s+D\b|\bmappa\b[^.\n]{0,40}\b(?:pagina|p\.|appendice)", re.I)


def chiave(nome: str) -> str:
    """La parola che distingue una persona: la prima che non è un titolo.

    >>> chiave("Zog'tar Deatheye, il generale")
    'zogtar'
    >>> chiave("Re Thorek I, il re di una fortezza giovane")
    'thorek'
    >>> chiave("Mastro Costruttore Zeth")
    'zeth'
    >>> chiave("Skullcrusher il Nero, il Primo Nero")
    'skullcrusher'
    """
    testa = nome.split(",")[0]
    for parola in re.findall(r"[\w'’]+", testa):
        p = piega_ascii(parola).lower().replace("'", "").replace("’", "")
        if p and p not in _TITOLI and len(p) > 2:
            return p
    return ""


def piega(s: str) -> str:
    return piega_ascii(s).lower().replace("'", "").replace("’", "")


def conta_nome(testo_piegato: str, k: str) -> int:
    return len(re.findall(rf"(?<![a-z0-9]){re.escape(k)}(?![a-z0-9])", testo_piegato))


def persone_con_nome() -> set[str]:
    """Le chiavi di chi ha un nome: una scheda d'entrata nel repo o un dossier PNG/villain."""
    chiavi: set[str] = set()
    for f in ROOT.rglob("*.md"):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(("build/", "node_modules/")) or "_ARCHIVIO" in rel:
            continue
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in _SCHEDA_ENTRATA.finditer(testo):
            if (k := chiave(m.group(1))):
                chiavi.add(k)
    for sotto in ("png", "villain"):
        for f in (ROOT / "Bestiario" / sotto).rglob("*.md"):
            nome = re.sub(r"-cr\d+.*$", "", f.stem).replace("_", " ").replace("-", " ")
            if (k := chiave(nome)):
                chiavi.add(k)
    return chiavi


def chiavi_dei_pg() -> set[str]:
    """I PG del tavolo (PG/schede): sono al tavolo, non hanno bisogno di una scheda d'entrata."""
    return {piega(f.stem) for f in (ROOT / "PG" / "schede").glob("*.yaml")}


def nome_proprio(nome: str, testo: str) -> bool:
    """Un nome di riquadro è una persona se la sua parola chiave non compare
    mai minuscola nel booklet: «Karkator», «Cerbo» sì; «Fantino», «Ragno» no.

    >>> nome_proprio("Cerbo, guardiano del magazzino", "Cerbo apre. Cerbo dorme.")
    True
    >>> nome_proprio("Ragno delle Catene", "Il Ragno scende: un ragno enorme.")
    False
    """
    k = chiave(nome)
    if not k:
        return False
    parole = [piega_ascii(w).replace("'", "").replace("’", "")
              for w in re.findall(r"[\w'’]+", testo)]
    simili = [w for w in parole if w.lower() == k]
    return bool(simili) and all(w[0].isupper() for w in simili)


def pulisci(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", togli_storico(md), flags=re.S)


def blocchi(md: str) -> list[tuple[str, str]]:
    """(nome, corpo) di ogni ```statblocco, col testo delle righe ADR-0091 che lo seguono."""
    fuori = []
    righe = md.split("\n")
    i = 0
    while i < len(righe):
        if righe[i].strip() == "```statblocco":
            j = i + 1
            while j < len(righe) and not righe[j].strip().startswith("```"):
                j += 1
            corpo = "\n".join(righe[i + 1:j])
            k = j + 1
            while k < len(righe) and not righe[k].startswith("#") and not righe[k].strip().startswith("```"):
                if righe[k].startswith("**Tattiche**") or righe[k].startswith("**Difesa**") \
                        or righe[k].startswith("**Attacco**") or righe[k].startswith("**Statistiche**") \
                        or righe[k].startswith("**Capacità") or righe[k].startswith("**Iniziativa"):
                    corpo += "\n" + righe[k]
                    k += 1
                    continue
                break
            m = _NOME_BLOCCO.search(corpo)
            if m:
                fuori.append((m.group(1), corpo))
            i = j + 1
            continue
        i += 1
    return fuori


def campo_dopo_nome(md: str, k: str, campo: re.Pattern, finestra: int = 150) -> bool:
    r"""Il campo compare nel blocco della persona: dopo il titolo della sua
    scheda d'entrata o un'intestazione col suo nome, fino alla prossima
    intestazione di scena (`##`/`###`) o alla scheda d'entrata di un altro,
    e al massimo `finestra` righe dopo.
    Una riga in grassetto che la nomina soltanto («**Vuole** … Balvar») non
    apre il blocco: era un falso positivo della prima misura.

    >>> campo_dopo_nome("**Scheda d'entrata — Balvar, il runaio**\n\n#### Chi è\nun nano", "balvar", _CHI)
    True
    >>> campo_dopo_nome("**Vuole** | Balvar\n#### Chi è\nun nano", "balvar", _CHI)
    False
    >>> campo_dopo_nome("### Balvar\n\n### Scena 9\n#### Chi è", "balvar", _CHI)
    False
    >>> campo_dopo_nome("**Scheda d'entrata — Zog'tar**\n**Scheda d'entrata — Balvar**\n#### Chi è", "zogtar", _CHI)
    False
    """
    righe = md.split("\n")
    for i, r in enumerate(righe):
        if not (r.startswith("#") or "Scheda d'entrata" in r) or not conta_nome(piega(r), k):
            continue
        j = i + 1
        while j < len(righe) and j - i < finestra and not re.match(r"^#{2,3}\s", righe[j]) \
                and "Scheda d'entrata" not in righe[j]:
            j += 1
        if campo.search("\n".join(righe[i:j])):
            return True
    return False


def ha_immagine(md: str, k: str) -> bool:
    for alt, path in _IMMAGINE.findall(md):
        if "Mappe/" in path:
            continue
        if conta_nome(piega(alt), k) or k in piega(path).replace("-", "").replace("_", ""):
            return True
    return False


def ha_tattica(md: str, k: str, bl: list[tuple[str, str]]) -> bool:
    for nome, corpo in bl:
        if chiave(nome) == k and "**Tattiche**" in corpo:
            return True
    for r in md.split("\n"):
        if _TATTICHE.search(r) and conta_nome(piega(r), k):
            return True
        # una riga di tabella di tattiche che comincia col nome in grassetto
        if r.startswith("| **") and conta_nome(piega(r.split("|")[1]), k) and len(r) > 120:
            return True
    return False


def mappa_lontana(md: str) -> bool:
    r"""Il capitolo stampa le sue mappe, ma lontano da dove le nomina: una
    mappa nominata dal testo ha la sua pianta solo più di
    `chi_si_incontra.LONTANO` righe dopo il punto dove serve (il paragrafo
    «**Mappa …**» della scena, o la prima volta che il testo la nomina). È l'Appendice D
    di un master, quaranta pagine dopo la scena.

    >>> mappa_lontana("**Mappa M1-A** qui.\n\n![M1-A — x](Mappe/a.svg)")
    False
    >>> mappa_lontana("**Mappa M1-A** qui." + "\n" * 400 + "![M1-A — x](Mappe/a.svg)")
    True
    """
    righe = md.split("\n")
    piante: dict[str, list[int]] = {}
    for i, r in enumerate(righe):
        m = re.match(r"^!\[(M\d+-[A-Z]{1,2})\b[^\]]*\]\(([^)]*Mappe/[^)]*)\)", r)
        if m:
            piante.setdefault(m.group(1), []).append(i)
    for c, i in chi_si_incontra.punti_delle_mappe(righe, set(piante)).items():
        # stessa regola del generatore: la pianta sta prima del punto o poco dopo
        if not any(p - i < chi_si_incontra.LONTANO for p in piante[c]):
            return True
    return False


#: Le note di lavoro che il generatore lascia in stampa di proposito, perché
#: avvisano il DM: un numero senza fonte (`[INFERRED]`), un riscontro da fare.
#: Al tavolo sono un buco: il DM le ha lette ad alta voce il 2026-11-03 (la
#: lettura alla cieca della prova ADR-0107). Il bersaglio è zero, e il
#: cricchetto sta in `test_misura_standard_tavolo.py`.
NOTA_DI_LAVORO = re.compile(
    r"\[INFERRED[^\]\n]{0,80}\]?|va riscontrat[oa][^.\n]{0,40}|da riscontrare|\(da verificare\)"
    r"|\bTODO\b|\bTBD\b")


def manifesti_dm() -> list[Path]:
    fuori = []
    for p in sorted(ROOT.rglob("*.manifest.json")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("build/") or "_ARCHIVIO" in rel or p.name == "tools.manifest.json":
            continue
        man = json.loads(p.read_text(encoding="utf-8"))
        if any(c.get("tag") == "dm" for c in man.get("chapters", [])):
            fuori.append(p)
    return fuori


def misura_booklet(mp: Path, nomi: set[str], soglia: int = 3, prova: bool = False,
                   indice: "chi_si_incontra.Indice | None" = None) -> dict:
    """`prova` misura il booklet come se il manifest dicesse
    `"schede": "entrambe", "chi_si_incontra": true` (ADR-0107): il capitolo
    arricchito da `dmcore.chi_si_incontra`, come lo stampa l'esportatore."""
    man = json.loads(mp.read_text(encoding="utf-8"))
    base = mp.parent
    modo = "entrambe" if prova else man.get("schede", "appendice")
    arricchisci = prova or bool(man.get("chi_si_incontra"))
    # «entrambe» (ADR-0107): il riquadro nel capitolo e anche nell'appendice
    appendice = modo == "appendice"
    if arricchisci and indice is None:
        indice = chi_si_incontra.indice_del_repo()
    nel_volume = capitoli_del_volume(base, man)
    volume = {"capitolo": "", "persone": {}, "mappe": {}, "native": {}} if modo == "prima-volta" else None
    if volume is not None:
        for cap in man.get("chapters", []):
            f = (base / cap["file"]).resolve()
            if f.is_file() and cap.get("tag") == "dm":
                m_ = re.match(r"^\s*([IVXLC]+)\s*·", cap.get("title", ""))
                for c in chi_si_incontra.mappe_stampate(leggi_per_la_stampa(f, nel_volume, cap.get("sezioni"))):
                    volume["native"].setdefault(c, f"capitolo {m_.group(1)}" if m_ else "capitolo")
    capitoli, note = [], []
    for cap in man.get("chapters", []):
        if cap.get("tag") != "dm" or cap.get("layout") == "schede":
            continue
        f = (base / cap["file"]).resolve()
        if not f.is_file():
            continue
        md = leggi_per_la_stampa(f, nel_volume, cap.get("sezioni"))
        if arricchisci and not _CONSULTAZIONE.search(cap.get("title", "")):
            if volume is not None:
                m_ = re.match(r"^\s*([IVXLC]+)\s*·", cap.get("title", ""))
                volume["capitolo"] = f"capitolo {m_.group(1)}" if m_ else "capitolo"
            md, _ = chi_si_incontra.arricchisci(md, f, indice, chiavi_dei_pg(), volume=volume)
            md = traduci_rimandi(md, f, nel_volume)
        note += [{"capitolo": cap.get("title", f.stem), "testo": m.group(0)}
                 # l'apparato e lo storico non vanno in stampa (ADR-0069): li toglie
                 # l'esportatore, e li toglie la misura
                 for m in NOTA_DI_LAVORO.finditer(re.sub(r"<!--.*?-->", "", togli_storico(md), flags=re.S))]
        capitoli.append((cap.get("title", f.stem), pulisci(md)))

    # chi ha un nome: una scheda (riquadro o scheda d'entrata) in questo
    # booklet, oppure una scheda d'entrata o un dossier altrove nel repo
    tutto = re.sub(r"\]\([^)]*\)|`[^`]*`|\(\.\.?/[^)]*\)", " ", "\n".join(md for _, md in capitoli))
    pg = chiavi_dei_pg()
    nel_booklet: dict[str, str] = {}
    for _, md in capitoli:
        for nome, _ in blocchi(md):
            k = chiave(nome)
            if k in nomi or nome_proprio(nome, tutto):
                nel_booklet.setdefault(k, nome.split(",")[0].strip())
        for m in _SCHEDA_ENTRATA.finditer(md):
            k = chiave(m.group(1))
            if k:
                nel_booklet.setdefault(k, m.group(1).split(",")[0].strip())
    for k in nomi - set(nel_booklet) - pg:
        if any(conta_nome(piega(md), k) >= soglia for _, md in capitoli) \
                and nome_proprio(k, tutto):
            nel_booklet[k] = k.capitalize()
    for k in pg | _NON_PERSONE:
        nel_booklet.pop(k, None)

    righe, mappe = [], []
    gia_stampati: set[str] = set()   # «prima-volta»: la scheda intera esce una volta sola
    for titolo, md in capitoli:
        mp_ = piega(md)
        bl = blocchi(md)
        if _SCONTRO.search(md):
            if any("Mappe/" in p for _, p in _IMMAGINE.findall(md)):
                mappa = "lontana" if mappa_lontana(md) else "qui"
            elif _RIMANDO_MAPPA.search(md):
                mappa = "rimando"
            else:
                mappa = "manca"
            mappe.append({"capitolo": titolo, "mappa": mappa})
        if _CONSULTAZIONE.search(titolo):
            continue
        for k, nome in sorted(nel_booklet.items()):
            n = conta_nome(mp_, k)
            if n < soglia:
                continue
            ha_blocco = any(chiave(b) == k for b, _ in bl)
            dopo = modo == "prima-volta" and k in gia_stampati
            if ha_blocco:
                gia_stampati.add(k)
            v = {
                "num": ("rimando" if appendice or dopo else "qui") if ha_blocco else "manca",
                "asp": campo_dopo_nome(md, k, _ASPETTO),
                "img": ha_immagine(md, k),
                "chi": campo_dopo_nome(md, k, _CHI),
                "vuole": campo_dopo_nome(md, k, _VUOLE),
                "tatt": ha_tattica(md, k, bl),
            }
            presenti = sum(1 for c in CAMPI if (v[c] if c != "num" else v[c] != "manca"))
            righe.append({"capitolo": titolo, "persona": nome, "citazioni": n, **v,
                          "presenti": presenti, "completa": presenti == len(CAMPI)})
    return {"schede_in": modo,
            "coppie": righe, "mappe": mappe, "note_di_lavoro": note}


def riassunto(d: dict) -> dict:
    c = d["coppie"]
    n = len(c) or 1
    return {
        "coppie": len(c),
        "complete": sum(r["completa"] for r in c),
        **{f"{k}%": round(100 * sum(1 for r in c if (r[k] if k != "num" else r[k] != "manca")) / n)
           for k in CAMPI},
        "num_qui%": round(100 * sum(1 for r in c if r["num"] == "qui") / n),
        "scontri": len(d["mappe"]),
        "mappa_qui": sum(1 for m in d["mappe"] if m["mappa"] == "qui"),
        "note_di_lavoro": len(d.get("note_di_lavoro", [])),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dettaglio", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--soglia", type=int, default=3, help="citazioni minime per dire che una persona compare (3)")
    ap.add_argument("--prova", action="store_true",
                    help="misura come se il manifest avesse «entrambe» e «chi_si_incontra» (ADR-0107)")
    a = ap.parse_args(argv)

    nomi = persone_con_nome()
    mani = [a.manifest.resolve()] if a.manifest else manifesti_dm()
    indice = chi_si_incontra.indice_del_repo() if a.prova else None
    dati = {mp.relative_to(ROOT).as_posix() if mp.is_relative_to(ROOT) else str(mp):
            misura_booklet(mp, nomi, a.soglia, a.prova, indice) for mp in mani}
    for v in dati.values():
        v["riassunto"] = riassunto(v)
    if a.json:
        print(json.dumps(dati, ensure_ascii=False, indent=2))
        return 0

    tot = {"coppie": 0, "complete": 0, **{c: 0 for c in CAMPI}, "num_qui": 0, "scontri": 0, "mappa_qui": 0}
    print(f"{'booklet':<48} {'schede':>10} {'coppie':>6} {'compl.':>6} "
          + " ".join(f"{c:>5}" for c in CAMPI) + f" {'mappa':>7}")
    for nome, v in dati.items():
        r = v["riassunto"]
        print(f"{nome.split('/')[-1][:48]:<48} {v['schede_in']:>10} {r['coppie']:>6} {r['complete']:>6} "
              + " ".join(f"{r[c + '%']:>4}%" for c in CAMPI)
              + f" {r['mappa_qui']:>3}/{r['scontri']:<3}")
        for row in v["coppie"]:
            tot["coppie"] += 1
            tot["complete"] += row["completa"]
            tot["num_qui"] += row["num"] == "qui"
            for c in CAMPI:
                tot[c] += bool(row[c] if c != "num" else row[c] != "manca")
        tot["scontri"] += r["scontri"]
        tot["mappa_qui"] += r["mappa_qui"]
        if a.dettaglio:
            for row in v["coppie"]:
                manca = [c for c in CAMPI if not (row[c] if c != "num" else row[c] != "manca")]
                segno = "✓" if row["completa"] else "·"
                print(f"   {segno} {row['capitolo'][:34]:<34} {row['persona'][:26]:<26} "
                      f"×{row['citazioni']:<3} num={row['num']:<7} manca: {', '.join(manca) or '—'}")
            for m in v["mappe"]:
                if m["mappa"] != "qui":
                    print(f"   ⌖ {m['capitolo'][:34]:<34} mappa: {m['mappa']}")
    n = tot["coppie"] or 1
    print(f"{'TOTALE':<48} {'':>10} {tot['coppie']:>6} {tot['complete']:>6} "
          + " ".join(f"{round(100 * tot[c] / n):>4}%" for c in CAMPI)
          + f" {tot['mappa_qui']:>3}/{tot['scontri']:<3}")
    print(f"numeri stampati nel capitolo (non in appendice): {tot['num_qui']}/{tot['coppie']}")
    note = {n: v["riassunto"]["note_di_lavoro"] for n, v in dati.items() if v["riassunto"]["note_di_lavoro"]}
    print(f"note di lavoro che vanno in stampa: {sum(note.values())}"
          + "".join(f"\n   {k}: {n}" for k, n in note.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
