"""dmcore.sistemi — i sistemi di gioco come plugin di dati (ADR-0111).

Il caricatore unico di `sistemi.toml` e dei plugin in `sistemi/<id>/sistema.toml`.
Risponde a tre domande e non ne fa altre:

    sistema_di(percorso)          quale sistema usa questo file
    attivi() / plugin(id)         quali sistemi ci sono e cosa dichiarano
    capacita(id, nome)            come un sistema copre una capacità, seguendo
                                  l'eredità fino in fondo
    regole_diverse(id, strumento) quali capacità di uno strumento 3.5 il
                                  sistema `id` legge da altri dati (F4)

Una capacità si dichiara in quattro modi (`sistemi/catalogo.toml`): `dati`,
`codice` (ancora cablata, con il lotto che la migra), `eredita` (con il
motivo) o `non_supportato` (con il motivo). **Nessuna eredità implicita**: una
capacità non dichiarata è un buco, e `problemi()` lo dice.

Solo libreria standard (`tomllib`, Python 3.11+). Nessuna scrittura, nessuna
rete: stesso albero, stesso risultato.
"""
from __future__ import annotations

import importlib.util
import inspect
import re
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = "sistemi.toml"
CARTELLA = "sistemi"
CATALOGO = "sistemi/catalogo.toml"
MODI = ("dati", "codice", "eredita", "non_supportato")
CAMPI_PLUGIN = ("id", "nome", "tipo", "licenza", "fonti", "skill", "capacita")
TIPI_PLUGIN = ("sistema", "famiglia")


class ErroreSistemi(RuntimeError):
    """Configurazione o plugin illeggibile: lo strumento non deve indovinare."""


@dataclass(frozen=True)
class Copertura:
    """Come un sistema copre una capacità, dopo l'eredità."""

    sistema: str          # il sistema chiesto
    capacita: str
    modo: str             # dati · codice · non_supportato · mancante
    da: str               # il plugin che la dichiara davvero
    catena: tuple         # i plugin attraversati, compreso `sistema`
    voci: tuple           # i file o i file:NOME
    nota: str             # motivo o lotto

    @property
    def utilizzabile(self) -> bool:
        return self.modo in ("dati", "codice")


def _leggi(f: Path) -> dict:
    try:
        return tomllib.loads(f.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise ErroreSistemi(f"manca {f}") from e
    except tomllib.TOMLDecodeError as e:
        raise ErroreSistemi(f"{f}: TOML non valido ({e})") from e


@lru_cache(maxsize=8)
def _carica(root: Path) -> "tuple[dict, dict, dict]":
    """(configurazione, catalogo, {id: plugin}). Messo in cache per radice."""
    cfg = _leggi(root / CONFIG)
    cat = _leggi(root / CATALOGO).get("capacita", {})
    plug = {}
    for f in sorted((root / CARTELLA).glob("*/sistema.toml")):
        p = _leggi(f)
        p["_cartella"] = f.parent.name
        plug[p.get("id", f.parent.name)] = p
    return cfg, cat, plug


def carica(root: "Path | None" = None) -> "tuple[dict, dict, dict]":
    return _carica((root or ROOT).resolve())


def progetto(root: "Path | None" = None) -> dict:
    return carica(root)[0].get("progetto", {})


def attivi(root: "Path | None" = None) -> "list[str]":
    return list(progetto(root).get("attivi", []))


def predefinito(root: "Path | None" = None) -> str:
    p = progetto(root).get("predefinito")
    if not p:
        raise ErroreSistemi(f"{CONFIG}: manca [progetto] predefinito")
    return p


def plugin(id_: str, root: "Path | None" = None) -> dict:
    plug = carica(root)[2]
    if id_ not in plug:
        raise ErroreSistemi(f"nessun plugin «{id_}» in {CARTELLA}/")
    return plug[id_]


def sistema_di(percorso: "str | Path", root: "Path | None" = None) -> str:
    """Il sistema di un file: il percorso più lungo di [moduli] che lo contiene."""
    r = (root or ROOT).resolve()
    p = Path(percorso)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(r)
        except ValueError:
            pass
    parti = p.parts
    migliore, lung = None, -1
    for chiave, sis in carica(r)[0].get("moduli", {}).items():
        pezzi = Path(chiave).parts
        if parti[:len(pezzi)] == pezzi and len(pezzi) > lung:
            migliore, lung = sis, len(pezzi)
    return migliore or predefinito(r)


def ambientazione_di(percorso: "str | Path", root: "Path | None" = None) -> str:
    """L'ambientazione di un file (ADR-0111, D4): il percorso più lungo di
    [ambientazioni.moduli] che lo contiene, altrimenti il predefinito."""
    r = (root or ROOT).resolve()
    amb = carica(r)[0].get("ambientazioni", {})
    p = Path(percorso)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(r)
        except ValueError:
            pass
    migliore, lung = None, -1
    for chiave, a in amb.get("moduli", {}).items():
        pezzi = Path(chiave).parts
        if p.parts[:len(pezzi)] == pezzi and len(pezzi) > lung:
            migliore, lung = a, len(pezzi)
    return migliore or amb.get("predefinito", "nessuna")


def capacita(id_: str, nome: str, root: "Path | None" = None) -> Copertura:
    """Come `id_` copre `nome`, seguendo `eredita`. Un ciclo è un errore."""
    _, _, plug = carica(root)
    catena, corrente = [], id_
    while True:
        if corrente in catena:
            raise ErroreSistemi(f"eredità circolare per «{nome}»: {' → '.join(catena + [corrente])}")
        catena.append(corrente)
        voce = plug.get(corrente, {}).get("capacita", {}).get(nome)
        if voce is None:
            return Copertura(id_, nome, "mancante", corrente, tuple(catena), (), "")
        modo = next((m for m in MODI if m in voce), None)
        if modo == "eredita":
            corrente = voce["eredita"]
            continue
        if modo == "dati":
            return Copertura(id_, nome, "dati", corrente, tuple(catena), tuple(voce["dati"]), voce.get("nota", ""))
        if modo == "codice":
            return Copertura(id_, nome, "codice", corrente, tuple(catena), tuple(voce["codice"]), voce.get("lotto", ""))
        if modo == "non_supportato":
            return Copertura(id_, nome, "non_supportato", corrente, tuple(catena), (), voce["non_supportato"])
        return Copertura(id_, nome, "mancante", corrente, tuple(catena), (), "modo sconosciuto")


#: La riga con cui un modulo dichiara il proprio sistema: «**Sistema:** …»,
#: «**Regole**: …», anche in un elenco o in una citazione, nelle prime righe.
DICHIARAZIONE = re.compile(
    r"^\s*(?:[-*>]\s*)?\*\*(?:Sistema|Regole|System)(?:\*\*\s*:|:\*\*)\s*(.+)$", re.I | re.M)
TESTA = 3000


def sistema_dichiarato(testo: str, root: "Path | None" = None) -> "str | None":
    """Il sistema che il testo dichiara nella riga «**Sistema:**», o None.

    Ogni plugin dice con `riconosci` come si scrive il suo nome; vince quello
    che compare per primo nella riga («D&D 3.5 (max PF1e)» è 3.5)."""
    m = DICHIARAZIONE.search(testo[:TESTA])
    if not m:
        return None
    valore, migliore = m.group(1), None
    for i, p in carica(root)[2].items():
        for pat in p.get("riconosci", []):
            t = re.search(pat, valore, re.I)
            if t and (migliore is None or t.start() < migliore[0]):
                migliore = (t.start(), i)
    return migliore[1] if migliore else None


def dichiarazioni_divergenti(root: "Path | None" = None) -> "list[tuple[str, str, str]]":
    """(file, sistema dichiarato, sistema di sistemi.toml) dove i due non coincidono.

    Si leggono i markdown delle cartelle d'arco e degli stand-alone (`0*`, `1*`),
    fuori da `homebrew/` (booklet generati) e `_ARCHIVIO/` (copie)."""
    r = (root or ROOT).resolve()
    fuori = []
    for base in sorted(list(r.glob("0*")) + list(r.glob("1*"))):
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*.md")):
            rel = f.relative_to(r)
            if "homebrew" in rel.parts or "_ARCHIVIO" in rel.parts:
                continue
            d = sistema_dichiarato(f.read_text(encoding="utf-8", errors="replace"), r)
            if d is not None:
                c = sistema_di(rel, r)
                if d != c:
                    fuori.append((str(rel), d, c))
    return fuori


def dati(id_: str, nome: str, root: "Path | None" = None) -> dict:
    """I dati TOML con cui `id_` copre `nome`, dopo l'eredità.

    Fonde i file `.toml` elencati in `dati = [...]`, nell'ordine. Se la
    capacità non è in modo «dati» è un errore: lo strumento deve usare il
    suo codice (modo «codice») o dire che il sistema non è supportato."""
    r = (root or ROOT).resolve()
    c = capacita(id_, nome, r)
    if c.modo != "dati":
        raise ErroreSistemi(f"{id_}: «{nome}» è {c.modo}" + (f" ({c.nota})" if c.nota else ""))
    out: dict = {}
    for v in c.voci:
        if v.endswith(".toml"):
            out.update(_leggi(r / v))
    return out


@dataclass(frozen=True)
class Regole:
    """Il contesto esplicito di un sistema (F2 di ADR-0112).

    Chi ha bisogno delle regole le chiede con `regole(id)` **quando gli
    servono**, non all'import: così il sistema lo sceglie il chiamante (il
    file, `sistema_di`), non l'ordine in cui Python carica i moduli."""

    id: str
    root: Path

    def dati(self, nome: str) -> dict:
        return dati(self.id, nome, self.root)

    def capacita(self, nome: str) -> Copertura:
        return capacita(self.id, nome, self.root)


@lru_cache(maxsize=16)
def _regole(id_: str, root: Path) -> Regole:
    plugin(id_, root)  # un id sconosciuto fallisce qui, non al primo dato
    return Regole(id_, root)


def regole(id_: str, root: "Path | None" = None) -> Regole:
    """Le regole del sistema `id_`, come contesto da passare a chi calcola."""
    return _regole(id_, (root or ROOT).resolve())


def regole_di(percorso: "str | Path", root: "Path | None" = None) -> Regole:
    """Le regole del sistema che usa questo file (`sistema_di`)."""
    return regole(sistema_di(percorso, root), root)


MANIFEST = "scripts/tools.manifest.json"


@lru_cache(maxsize=4)
def _manifest(root: Path) -> "dict[str, tuple[str, ...]]":
    import json
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    return {t["id"]: tuple(t["sistema"]["capacita"]) for t in m["tools"] if t.get("sistema")}


def capacita_chieste(strumento: str, root: "Path | None" = None) -> "tuple[str, ...]":
    """Le capacità che `strumento` chiede nel suo campo `sistema.capacita` del manifest."""
    return _manifest((root or ROOT).resolve()).get(strumento, ())


def regole_diverse(id_: str, strumento: str, scritto_per: str = "dnd35",
                   root: "Path | None" = None) -> "list[str]":
    """Le capacità di `strumento` che `id_` legge da dati diversi da `scritto_per` (F4 di ADR-0112).

    Uno strumento scritto sulle tabelle di `scritto_per` può lavorare su un file
    di `id_` solo se, per ogni capacità che chiede, i due sistemi arrivano agli
    stessi dati (eredità compresa). Vuoto = può lavorare; altrimenti salta il
    file e dice quali regole mancano, invece di usare quelle di un altro
    sistema senza dirlo.
    """
    fuori = []
    for nome in capacita_chieste(strumento, root):
        a, b = capacita(id_, nome, root), capacita(scritto_per, nome, root)
        if not a.utilizzabile or (a.da, a.voci) != (b.da, b.voci):
            fuori.append(nome)
    return fuori


#: F5 di ADR-0112 (indagine I3): il codice di un plugin sta in
#: `sistemi/<id>/codice/` ed è registrato per nome in `[moduli]` del suo
#: `sistema.toml`, come «modulo:funzione». Nomi semplici, niente punti né dunder.
CODICE = "codice"
_NOME_MODULO = re.compile(r"^[a-z_][a-z0-9_]*$")


@lru_cache(maxsize=64)
def _risolvi(id_: str, rif: str, root: Path):
    """La funzione di `rif` («modulo:funzione») dentro `sistemi/<id>/codice/`.

    Rifiuta, prima di eseguire qualunque file, ogni riferimento che esce dalla
    cartella: `..`, percorsi assoluti, moduli della libreria standard, symlink
    verso fuori. Il modulo prende un nome unico per sistema
    (`rs_plugin.<id>.<modulo>`), così due plugin con un `incontri.py` non si
    scambiano il codice. ⚠️ Il file del plugin viene eseguito: è codice Python
    rivisto in PR come il nucleo, non una sandbox.
    """
    mod, sep, fun = (rif or "").partition(":")
    if not sep or not _NOME_MODULO.match(mod) or not _NOME_MODULO.match(fun) or fun.startswith("__"):
        raise ErroreSistemi(f"{id_}: modulo «{rif}»: serve «modulo:funzione» con nomi semplici")
    cartella = (root / CARTELLA / plugin(id_, root)["_cartella"] / CODICE).resolve()
    file = (cartella / f"{mod}.py").resolve()  # resolve() segue i symlink
    if file.parent != cartella or not file.is_file():
        raise ErroreSistemi(f"{id_}: modulo «{rif}»: {mod}.py non è in {CARTELLA}/{id_}/{CODICE}/")
    spec = importlib.util.spec_from_file_location(f"rs_plugin.{id_.replace('-', '_')}.{mod}", file)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    f = getattr(modulo, fun, None)
    if not inspect.isfunction(f) or f.__module__ != modulo.__name__:
        raise ErroreSistemi(f"{id_}: modulo «{rif}»: {fun} non è una funzione definita in {mod}.py")
    return f


@lru_cache(maxsize=64)
def _modulo(id_: str, nome: str, root: Path):
    for i in _catena_moduli(id_, root):
        rif = plugin(i, root).get("moduli", {}).get(nome)
        if rif is not None:
            return _risolvi(i, rif, root)
    noti = ", ".join(moduli(id_, root)) or "nessuno"
    raise ErroreSistemi(f"{id_}: nessun modulo «{nome}» nel plugin né nella famiglia (ci sono: {noti})")


def _catena_moduli(id_: str, root: Path) -> "list[str]":
    """Il plugin e poi la sua famiglia: dove si cerca un modulo per nome."""
    catena, corrente = [], id_
    while corrente and corrente not in catena:
        catena.append(corrente)
        corrente = plugin(corrente, root).get("famiglia")
    return catena


def modulo(id_: str, nome: str, root: "Path | None" = None):
    """La funzione registrata come `nome` in `[moduli]` del plugin `id_` o della sua famiglia."""
    return _modulo(id_, nome, (root or ROOT).resolve())


def moduli(id_: str, root: "Path | None" = None) -> "list[str]":
    """I nomi dei moduli che `id_` vede, suoi e della famiglia."""
    r = (root or ROOT).resolve()
    return sorted({n for i in _catena_moduli(id_, r) for n in plugin(i, r).get("moduli", {})})


def termini_vietati(id_: str | None = None, root: "Path | None" = None) -> "list[tuple[str, str]]":
    """(regex, perché) dei termini vietati in un sistema (capacità termini.vietati).

    Senza `id_` vale il predefinito. È la lista sola che validate_modules e
    validate_standalone leggono (ADR-0111, L3)."""
    voci = dati(id_ or predefinito(root), "termini.vietati", root).get("vietato", [])
    return [(v["regex"], v["perche"]) for v in voci]


def abilita(id_: str | None = None, root: "Path | None" = None) -> dict:
    """{"nomi": [...], "estranee": [...]} di un sistema (capacità lessico.abilita).

    I file `.toml` danno le liste; un `.tsv` del lessico (italiano, inglese,
    tipo) aggiunge ai `nomi` le righe di tipo «abilità», in minuscolo."""
    r = (root or ROOT).resolve()
    id_ = id_ or predefinito(r)
    c = capacita(id_, "lessico.abilita", r)
    if c.modo != "dati":
        raise ErroreSistemi(f"{id_}: «lessico.abilita» è {c.modo}")
    out = {"nomi": [], "estranee": []}
    for v in c.voci:
        if v.endswith(".toml"):
            d = _leggi(r / v)
            for k in out:
                out[k] += [x for x in d.get(k, []) if x not in out[k]]
        elif v.endswith(".tsv"):
            for riga in (r / v).read_text(encoding="utf-8").splitlines():
                campi = riga.split("\t")
                if len(campi) >= 3 and campi[2] == "abilità" and not riga.startswith("#"):
                    nome = campi[0].lower()
                    if nome not in out["nomi"]:
                        out["nomi"].append(nome)
    return out


def opzione(id_: str, chiave: str, default=None, root: "Path | None" = None):
    """Un'opzione di campagna del sistema, da `[opzioni.<id>]` in sistemi.toml."""
    return carica(root)[0].get("opzioni", {}).get(id_, {}).get(chiave, default)


def skill_da_installare(root: "Path | None" = None) -> "list[str]":
    """Le skill dei sistemi attivi e di quelli di rinforzo, e delle loro famiglie (D5)."""
    pr = progetto(root)
    _, _, plug = carica(root)
    ids = list(dict.fromkeys(list(pr.get("attivi", [])) + list(pr.get("rinforzo", []))))
    fuori: "list[str]" = []
    for i in ids:
        for j in (i, plug.get(i, {}).get("famiglia")):
            for s in plug.get(j, {}).get("skill", []) if j else []:
                if s not in fuori:
                    fuori.append(s)
    return fuori


def etichette(id_: str | None = None, root: "Path | None" = None) -> "dict[str, str]":
    """Le sigle stampate nel riquadro della creatura (capacità stampa.etichette, L7).

    Senza `id_` vale il predefinito: chi stampa un file passa `sistema_di(file)`."""
    return dict(dati(id_ or predefinito(root), "stampa.etichette", root).get("etichette", {}))


def skill_escluse(root: "Path | None" = None) -> "list[str]":
    """Le skill di un sistema che non è né attivo né di rinforzo (ADR-0111, L6).

    Sono le sole che build-skills.sh e sync-skills.sh saltano: una skill che
    nessun plugin dichiara (campagna, prosa, mappe, ambientazione) si installa
    sempre, perché non dipende dal sistema di gioco."""
    _, _, plug = carica(root)
    tenute = set(skill_da_installare(root))
    fuori: "list[str]" = []
    for i in sorted(plug):
        for s in plug[i].get("skill", []):
            if s not in tenute and s not in fuori:
                fuori.append(s)
    return fuori


_NOME_IN_CODICE = r"^(?:def\s+{n}\b|class\s+{n}\b|{n}\s*(?::[^=\n]+)?=)"


def problemi(root: "Path | None" = None, strumenti: "dict[str, list[str]] | None" = None) -> "list[str]":
    """Tutto quello che rende la configurazione inaffidabile. Vuoto = verde.

    `strumenti` è {id strumento: [capacità chieste]}, dal manifest dei tool.
    """
    r = (root or ROOT).resolve()
    try:
        cfg, cat, plug = carica(r)
    except ErroreSistemi as e:
        return [str(e)]
    fuori = []
    pr = cfg.get("progetto", {})
    att = list(pr.get("attivi", []))
    if not att:
        fuori.append(f"{CONFIG}: [progetto] attivi è vuoto")
    if pr.get("predefinito") not in att:
        fuori.append(f"{CONFIG}: il predefinito «{pr.get('predefinito')}» non è fra gli attivi")
    for i in att + list(pr.get("rinforzo", [])):
        if i not in plug:
            fuori.append(f"{CONFIG}: «{i}» non ha un plugin in {CARTELLA}/{i}/sistema.toml")
        elif plug[i].get("tipo") != "sistema":
            fuori.append(f"{CONFIG}: «{i}» è una {plug[i].get('tipo')}, non un sistema attivabile")
    for chiave, sis in cfg.get("moduli", {}).items():
        if not (r / chiave).exists():
            fuori.append(f"{CONFIG} [moduli]: la cartella «{chiave}» non esiste")
        if sis not in att:
            fuori.append(f"{CONFIG} [moduli]: «{chiave}» usa «{sis}», che non è attivo")
    amb = cfg.get("ambientazioni", {})
    elenco = amb.get("elenco", {})
    if amb and amb.get("predefinito") not in elenco:
        fuori.append(f"{CONFIG} [ambientazioni]: il predefinito «{amb.get('predefinito')}» non è nell'elenco")
    for chiave, a in amb.get("moduli", {}).items():
        if not (r / chiave).exists():
            fuori.append(f"{CONFIG} [ambientazioni.moduli]: la cartella «{chiave}» non esiste")
        if a not in elenco:
            fuori.append(f"{CONFIG} [ambientazioni.moduli]: «{chiave}» usa «{a}», che non è nell'elenco")
    for a, voce in elenco.items():
        for s in voce.get("skill", []):
            if not (r / "skills" / s / "SKILL.md").is_file():
                fuori.append(f"{CONFIG} [ambientazioni.elenco]: la skill «{s}» di «{a}» non esiste in skills/")
    for i, p in sorted(plug.items()):
        dove = f"{CARTELLA}/{p['_cartella']}/sistema.toml"
        for campo in CAMPI_PLUGIN:
            if campo not in p:
                fuori.append(f"{dove}: manca «{campo}»")
        if p.get("id") != p["_cartella"]:
            fuori.append(f"{dove}: id «{p.get('id')}» diverso dalla cartella")
        if p.get("tipo") not in TIPI_PLUGIN:
            fuori.append(f"{dove}: tipo «{p.get('tipo')}» non è uno di {TIPI_PLUGIN}")
        fam = p.get("famiglia")
        if fam and plug.get(fam, {}).get("tipo") != "famiglia":
            fuori.append(f"{dove}: la famiglia «{fam}» non è un plugin di tipo famiglia")
        for s in p.get("skill", []):
            if not (r / "skills" / s / "SKILL.md").is_file():
                fuori.append(f"{dove}: la skill «{s}» non esiste in skills/")
        for nome, voce in p.get("capacita", {}).items():
            if nome not in cat:
                fuori.append(f"{dove}: capacità «{nome}» non è nel catalogo")
            modi = [m for m in MODI if m in voce] if isinstance(voce, dict) else []
            if len(modi) != 1:
                fuori.append(f"{dove}: «{nome}» deve avere uno e un solo modo fra {MODI}")
                continue
            m = modi[0]
            if m == "eredita":
                if voce["eredita"] not in plug:
                    fuori.append(f"{dove}: «{nome}» eredita da «{voce['eredita']}», che non esiste")
                if not voce.get("motivo"):
                    fuori.append(f"{dove}: «{nome}» eredita senza motivo")
            elif m == "dati":
                for f in voce["dati"]:
                    if not (r / f).is_file():
                        fuori.append(f"{dove}: «{nome}»: il file «{f}» non esiste")
            elif m == "codice":
                if not voce.get("lotto"):
                    fuori.append(f"{dove}: «{nome}» è nel codice senza il lotto che lo migra")
                for v in voce["codice"]:
                    f, _, n = v.partition(":")
                    if not (r / f).is_file():
                        fuori.append(f"{dove}: «{nome}»: il file «{f}» non esiste")
                    elif not n or not re.search(_NOME_IN_CODICE.format(n=re.escape(n)),
                                                (r / f).read_text(encoding="utf-8"), re.M):
                        fuori.append(f"{dove}: «{nome}»: «{n}» non è definito in {f}")
            elif not voce.get("non_supportato"):
                fuori.append(f"{dove}: «{nome}» non supportato senza motivo")
    for i in sorted(plug):
        for nome in cat:
            try:
                capacita(i, nome, r)
            except ErroreSistemi as e:
                fuori.append(str(e))
        for nome, rif in sorted(plug[i].get("moduli", {}).items()):
            try:
                _risolvi(i, rif, r)
            except ErroreSistemi as e:
                fuori.append(f"{CARTELLA}/{plug[i]['_cartella']}/sistema.toml [moduli] {nome}: {e}")
    for sid, chieste in sorted((strumenti or {}).items()):
        for nome in chieste:
            if nome not in cat:
                fuori.append(f"tools.manifest.json «{sid}»: capacità «{nome}» non è nel catalogo")
                continue
            for i in att:
                c = capacita(i, nome, r)
                if c.modo == "mancante":
                    fuori.append(f"«{sid}» chiede «{nome}», che «{i}» non dichiara: "
                                 "dichiararla (dati, codice, eredita o non_supportato)")
    for f, d, c in dichiarazioni_divergenti(r):
        fuori.append(f"{f}: la riga «Sistema» dice «{d}», {CONFIG} [moduli] dice «{c}»: "
                     "correggere la riga o aggiungere la cartella a [moduli]")
    return fuori
