#!/usr/bin/env python3
"""
riscontro_srd.py — riscontra le regole dei master sull'SRD 3.5 e sul PRD PF1e.

Nato dalla prova di ``plans/esperimenti/ricerca-rete-2026-10-23/`` (§3 di
RICERCA.md): le regole che un giro di lettori controlla «a memoria» si
riscontrano sul testo delle due fonti aperte, e la prova ha trovato una
discordanza vera (la *freccia assassina* di DEF-2). Canale **testing** di
ADR-0099; la decisione è ADR-0103.

Le fonti, entrambe Open Game Content sotto OGL 1.0a:

  - SRD 3.5 in Markdown, ``olimot/srd-v3.5-md`` (Wizards of the Coast; la
    Product Identity è esclusa, vedi ``basic-rules-and-legal/legal-information.md``);
  - PRD di Pathfinder 1e in SQLite, ``devonjones/PSRD-Data`` (Paizo; l'avviso
    è nel libro ``book-ogl.db``).

Si scaricano da ``raw.githubusercontent.com`` a un commit fissato, file per
file, e ogni file si controlla con lo sha256 scritto in
``sistemi/<id>/dati/fonti.toml`` (capacità ``fonti.regole`` del plugin). Stanno in una
cache **fuori dal repo**: ``--cache``, oppure ``$RUMBLINGSTONE_SRD_CACHE``,
oppure ``$XDG_CACHE_HOME/rumblingstone/srd``, oppure
``~/.cache/rumblingstone/srd``. Nel repo non entra niente delle due fonti.

Uso:
    python3 scripts/riscontro_srd.py scarica                 # rete: riempie la cache
    python3 scripts/riscontro_srd.py scarica --da-cartella srd35=DIR pf1=DIR
                                                             # da cloni già fatti
    python3 scripts/riscontro_srd.py scarica --verifica      # rifà gli sha256
    python3 scripts/riscontro_srd.py regola "Slaying Arrow"  # una regola per nome
    python3 scripts/riscontro_srd.py riscontra FILE.yaml [--md OUT] [--json OUT] [--strict]
    python3 scripts/riscontro_srd.py licenza                 # dove sta il testo OGL

Il file dei riscontri (YAML o JSON) ha una chiave ``riscontri``, un elenco.
Ogni voce:

    id, cosa           chi l'ha chiesto e che cosa si controlla
    fonte              srd35 | pf1
    file               (srd35) il file dell'SRD; senza, si cerca in tutti
    libro, sezione     (pf1) il database e il nome della sezione; senza
                       libro, in tutti
    regola             regex che deve stare nella fonte; il gruppo (?P<v>...)
                       è il valore da confrontare
    regola_non         regex che NON deve stare nel passo trovato (facoltativa)
    master             il file del repo che afferma la regola (facoltativo)
    affermazione       regex nel master, con il suo gruppo (?P<v>...); conta
                       ogni occorrenza
    confronto          presenza (default) | numero | termine
    scala              per numero: il valore della fonte si moltiplica per
                       questo (0.3 da piedi a metri)
    tolleranza         per numero, default 1e-6
    equivale           per termine: {valore della fonte: [forme accettate]}

Esiti: **concorda**, **discorda**, **non trovata** (nella fonte o nel master),
ognuno con la citazione: file e riga dell'SRD, oppure libro e sezione del PRD,
e file e riga del master. Il confronto «numero» e «termine» lo fa lo script;
«presenza» dice solo che la regola sta nella fonte e l'affermazione nel master.

Exit: 0 rapporto prodotto (anche con discordanze) · 1 con --strict, una
discordanza o una regola non trovata; oppure uno sha256 che non combacia;
oppure ``regola`` senza risultati · 2 errore d'uso (file dei riscontri
illeggibile, regex sbagliata) · 3 fonti non disponibili: la cache non le ha e
la rete non risponde (o ``--offline``). Lo dice sempre, non tace.

Legge il repo; scrive solo nella cache e in --md/--json. Rete solo per
``scarica`` o quando la cache è incompleta.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ESITO_RETE = 3

URL_RAW = "https://raw.githubusercontent.com/{repo}/{commit}/{path}"


@dataclass
class Fonte:
    chiave: str
    nome: str
    repo: str
    commit: str
    licenza: str
    file_licenza: str
    file: dict[str, str] = field(default_factory=dict)

    def cartella(self, cache: Path) -> Path:
        return cache / f"{self.repo.split('/')[-1]}-{self.commit[:12]}"


def _fonte(sistema: str) -> Fonte:
    """La fonte di un sistema, dalla capacità ``fonti.regole`` del suo plugin.

    URL, commit, licenza e sha256 stanno in ``sistemi/<id>/dati/fonti.toml``
    (ADR-0112, F1): il codice non conosce nessuna fonte. Ogni cambio si
    rivede nel diff di quel file."""
    if str(REPO / "scripts") not in sys.path:
        sys.path.insert(0, str(REPO / "scripts"))
    from dmcore.sistemi import dati
    d = dati(sistema, "fonti.regole", REPO)
    return Fonte(chiave=d["chiave"], nome=d["nome"], repo=d["repo"], commit=d["commit"],
                 licenza=d["licenza"], file_licenza=d["file_licenza"], file=dict(sorted(d["file"].items())))


SRD35 = _fonte("dnd35")
PF1 = _fonte("pf1e")

FONTI = {f.chiave: f for f in (SRD35, PF1)}


class FontiMancanti(Exception):
    """La cache non ha le fonti e non si possono scaricare."""


class ImprontaSbagliata(Exception):
    """Un file scaricato o copiato non ha lo sha256 fissato."""


class ErroreUso(Exception):
    pass


# ---------------------------------------------------------------- cache

def cartella_cache(argomento: str | None) -> Path:
    if argomento:
        return Path(argomento).expanduser()
    if os.environ.get("RUMBLINGSTONE_SRD_CACHE"):
        return Path(os.environ["RUMBLINGSTONE_SRD_CACHE"]).expanduser()
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "rumblingstone" / "srd"


def sha256(percorso: Path) -> str:
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def scarica_url(url: str, destinazione: Path, timeout: float = 60) -> None:
    """Scarica ``url`` in ``destinazione``. Separata per i test."""
    with urllib.request.urlopen(url, timeout=timeout) as r, open(destinazione, "wb") as f:
        shutil.copyfileobj(r, f)


def _metti(fonte: Fonte, cache: Path, rel: str, sorgente) -> None:
    """Porta un file nella cache passando da un temporaneo e dallo sha256."""
    finale = fonte.cartella(cache) / rel
    finale.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=finale.parent, prefix=".scarico-")
    os.close(fd)
    tmp = Path(tmp)
    try:
        sorgente(tmp)
        trovato = sha256(tmp)
        if trovato != fonte.file[rel]:
            raise ImprontaSbagliata(
                f"{fonte.nome}, {rel}: sha256 {trovato[:16]}…, atteso "
                f"{fonte.file[rel][:16]}… (commit {fonte.commit[:8]})")
        os.replace(tmp, finale)
    finally:
        if tmp.exists():
            tmp.unlink()


def mancanti(fonte: Fonte, cache: Path) -> list[str]:
    base = fonte.cartella(cache)
    return [rel for rel in sorted(fonte.file) if not (base / rel).is_file()]


def assicura(fonte: Fonte, cache: Path, rete: bool = True, avvisa=print) -> Path:
    """Restituisce la cartella della fonte, scaricando i file che mancano."""
    da_fare = mancanti(fonte, cache)
    if not da_fare:
        return fonte.cartella(cache)
    if not rete:
        raise FontiMancanti(
            f"{fonte.nome}: {len(da_fare)} file su {len(fonte.file)} non sono in "
            f"{fonte.cartella(cache)} e --offline vieta di scaricarli")
    avvisa(f"{fonte.nome}: scarico {len(da_fare)} file da {fonte.repo}@{fonte.commit[:8]}",
           file=sys.stderr)
    for rel in da_fare:
        url = URL_RAW.format(repo=fonte.repo, commit=fonte.commit, path=rel)
        try:
            _metti(fonte, cache, rel, lambda tmp, u=url: scarica_url(u, tmp))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            raise FontiMancanti(
                f"{fonte.nome}: la rete non risponde scaricando {url} ({e}). "
                f"Senza rete: `scarica --da-cartella {fonte.chiave}=CLONE` da un "
                f"clone di {fonte.repo} al commit {fonte.commit[:8]}") from e
    return fonte.cartella(cache)


def da_cartella(fonte: Fonte, cache: Path, origine: Path) -> int:
    """Copia nella cache i file fissati da un clone locale, con lo sha256."""
    n = 0
    for rel in mancanti(fonte, cache):
        src = origine / rel
        if not src.is_file():
            raise FontiMancanti(f"{fonte.nome}: {src} non c'è")
        _metti(fonte, cache, rel, lambda tmp, s=src: shutil.copyfile(s, tmp))
        n += 1
    return n


def verifica(fonte: Fonte, cache: Path) -> list[str]:
    base = fonte.cartella(cache)
    return [rel for rel in sorted(fonte.file)
            if (base / rel).is_file() and sha256(base / rel) != fonte.file[rel]]


# ---------------------------------------------------------------- lettura

_TAG = re.compile(r"<[^>]+>")


def pulisci(testo: str) -> str:
    """Toglie i tag HTML delle tabelle e comprime gli spazi, per citare."""
    testo = re.sub(r"</t[dh]>\s*<t[dh][^>]*>", " | ", testo)
    testo = _TAG.sub(" ", testo)
    return re.sub(r"\s+", " ", testo).strip()


def taglia(testo: str, centro: int, larghezza: int = 220) -> str:
    inizio = max(0, centro - larghezza // 3)
    pezzo = testo[inizio:inizio + larghezza]
    return ("…" if inizio else "") + pulisci(pezzo) + ("…" if inizio + larghezza < len(testo) else "")


def riga_di(testo: str, pos: int) -> int:
    return testo.count("\n", 0, pos) + 1


@dataclass
class Passo:
    """Un punto di una fonte o del master, con la citazione."""
    citazione: str
    testo: str
    valore: str | None
    estratto: str


def _valore(m: re.Match) -> str | None:
    return m.group("v") if "v" in m.re.groupindex else None


def _punto(m: re.Match) -> int:
    """Dove citare: il valore, se la regex ne ha uno, altrimenti l'inizio."""
    return m.start("v") if "v" in m.re.groupindex and m.group("v") is not None else m.start()


def cerca_srd35(base: Path, fonte: Fonte, regola: re.Pattern, file: str | None) -> Passo | None:
    candidati = [file] if file else sorted(fonte.file)
    for rel in candidati:
        p = base / rel
        if not p.is_file():
            if file:
                raise ErroreUso(f"{rel}: non è un file dell'SRD 3.5 fissato")
            continue
        testo = p.read_text(encoding="utf-8")
        m = regola.search(testo)
        if m:
            # Il «passo» è il paragrafo (o la riga di tabella) che contiene la regola.
            a = testo.rfind("\n", 0, m.start()) + 1
            b = testo.find("\n", m.end())
            b = len(testo) if b < 0 else b
            return Passo(citazione=f"{fonte.nome}, {rel}:{riga_di(testo, _punto(m))}",
                         testo=testo[a:b], valore=_valore(m),
                         estratto=taglia(testo, _punto(m)))
    return None


def sezioni_pf1(db: Path, nome: str) -> list[tuple[str, str, str]]:
    """(fonte, url, testo) di ogni sezione chiamata ``nome``, col suo sottoalbero."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        uscita = []
        for lft, rgt, source, url in con.execute(
                "select lft, rgt, source, url from sections where name = ? collate nocase "
                "order by lft", (nome,)):
            corpi = [c for (c,) in con.execute(
                "select body from sections where lft between ? and ? and body is not null "
                "order by lft", (lft, rgt))]
            uscita.append((source, url or "", pulisci("\n".join(corpi))))
        return uscita
    finally:
        con.close()


def cerca_pf1(base: Path, fonte: Fonte, regola: re.Pattern, libro: str | None,
              sezione: str) -> Passo | None:
    libri = [libro] if libro else sorted(fonte.file)
    for db in libri:
        if db not in fonte.file:
            raise ErroreUso(f"{db}: non è un libro del PRD fissato")
        for source, url, testo in sezioni_pf1(base / db, sezione):
            m = regola.search(testo)
            if m:
                return Passo(citazione=f"{fonte.nome}, {source} › {sezione} ({db})",
                             testo=testo, valore=_valore(m),
                             estratto=taglia(testo, _punto(m)))
    return None


# ---------------------------------------------------------------- confronto

def numero(testo: str, inglese: bool = False) -> float:
    """Un numero scritto all'italiana (master) o all'inglese (fonte).

    Italiano: «4,5» → 4.5, «2.282» → 2282. Inglese: «2,282» → 2282, «1.5» → 1.5.
    """
    t = testo.strip().replace("\u2009", "").replace(" ", "")
    migliaia, decimali = (",", ".") if inglese else (".", ",")
    if re.fullmatch(rf"\d{{1,3}}(\{migliaia}\d{{3}})+", t):
        t = t.replace(migliaia, "")
    return float(t.replace(decimali, "."))


def normalizza(testo: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", testo)).strip().lower()


def confronta(voce: dict, fonte_v: str | None, master_v: str | None) -> bool:
    modo = voce.get("confronto", "presenza")
    if modo == "presenza":
        return True
    if fonte_v is None or master_v is None:
        raise ErroreUso(f"{voce['id']}: «{modo}» vuole il gruppo (?P<v>…) in regola e affermazione")
    if modo == "numero":
        atteso = numero(fonte_v, inglese=True) * float(voce.get("scala", 1))
        return abs(numero(master_v) - atteso) <= float(voce.get("tolleranza", 1e-6))
    if modo == "termine":
        accettati = {normalizza(fonte_v)}
        for chiave, forme in (voce.get("equivale") or {}).items():
            if normalizza(str(chiave)) == normalizza(fonte_v):
                accettati |= {normalizza(str(f)) for f in forme}
        return normalizza(master_v) in accettati
    raise ErroreUso(f"{voce['id']}: confronto «{modo}» sconosciuto (presenza, numero, termine)")


def compila(voce: dict, chiave: str) -> re.Pattern | None:
    if not voce.get(chiave):
        return None
    try:
        return re.compile(voce[chiave], re.MULTILINE)
    except re.error as e:
        raise ErroreUso(f"{voce.get('id', '?')}: «{chiave}» non è una regex valida: {e}") from e


@dataclass
class Esito:
    id: str
    cosa: str
    esito: str              # concorda | discorda | non trovata
    dove: str               # «» | «nella fonte» | «nel master»
    fonte: str              # citazione
    fonte_dice: str
    master: str
    master_dice: str


def riscontra_voce(voce: dict, basi: dict[str, Path], repo: Path) -> Esito:
    for k in ("id", "fonte", "regola"):
        if not voce.get(k):
            raise ErroreUso(f"riscontro senza «{k}»: {voce}")
    fonte = FONTI.get(voce["fonte"])
    if fonte is None:
        raise ErroreUso(f"{voce['id']}: fonte «{voce['fonte']}» sconosciuta (srd35, pf1)")
    regola = compila(voce, "regola")
    if fonte.chiave == "srd35":
        passo = cerca_srd35(basi["srd35"], fonte, regola, voce.get("file"))
    else:
        if not voce.get("sezione"):
            raise ErroreUso(f"{voce['id']}: una regola del PRD vuole «sezione»")
        passo = cerca_pf1(basi["pf1"], fonte, regola, voce.get("libro"), voce["sezione"])
    cosa = voce.get("cosa", "")
    if passo is None:
        dove = voce.get("file") or voce.get("sezione") or "tutta la fonte"
        return Esito(voce["id"], cosa, "non trovata", "nella fonte",
                     f"{fonte.nome}, {dove}", "", voce.get("master") or "", "")
    fonte_dice = passo.estratto
    non = compila(voce, "regola_non")
    if non is not None and non.search(passo.testo):
        return Esito(voce["id"], cosa, "discorda", "", passo.citazione,
                     fonte_dice, "", f"la fonte contiene «{voce['regola_non']}»")
    if not voce.get("master"):
        return Esito(voce["id"], cosa, "concorda", "", passo.citazione, fonte_dice, "", "")
    percorso = repo / voce["master"]
    if not percorso.is_file():
        raise ErroreUso(f"{voce['id']}: il master {voce['master']} non c'è")
    testo = percorso.read_text(encoding="utf-8")
    affermazione = compila(voce, "affermazione")
    if affermazione is None:
        raise ErroreUso(f"{voce['id']}: c'è «master» senza «affermazione»")
    occorrenze = list(affermazione.finditer(testo))
    if not occorrenze:
        return Esito(voce["id"], cosa, "non trovata", "nel master", passo.citazione,
                     fonte_dice, voce["master"], "")
    for m in occorrenze:
        cit = f"{voce['master']}:{riga_di(testo, _punto(m))}"
        if not confronta(voce, passo.valore, _valore(m)):
            dice = taglia(testo, _punto(m), 160)
            if passo.valore is not None:
                dice += f" (valore «{normalizza(_valore(m) or '')}» contro «{passo.valore}»"
                dice += f" × {voce['scala']})" if voce.get("scala") else ")"
            return Esito(voce["id"], cosa, "discorda", "", passo.citazione, fonte_dice, cit, dice)
    m = occorrenze[0]
    righe = ", ".join(str(riga_di(testo, _punto(o))) for o in occorrenze)
    return Esito(voce["id"], cosa, "concorda", "", passo.citazione, fonte_dice,
                 f"{voce['master']}:{righe}", taglia(testo, _punto(m), 160))


def leggi_riscontri(percorso: Path) -> list[dict]:
    try:
        testo = percorso.read_text(encoding="utf-8")
    except OSError as e:
        raise ErroreUso(f"{percorso}: {e}") from e
    if percorso.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as e:
            raise ErroreUso("pyyaml non c'è: usa un file .json o installa requirements.txt") from e
        try:
            dati = yaml.safe_load(testo)
        except yaml.YAMLError as e:
            raise ErroreUso(f"{percorso}: YAML non valido: {e}") from e
    else:
        try:
            dati = json.loads(testo)
        except json.JSONDecodeError as e:
            raise ErroreUso(f"{percorso}: JSON non valido: {e}") from e
    if isinstance(dati, list):
        return dati
    if not isinstance(dati, dict) or not isinstance(dati.get("riscontri"), list):
        raise ErroreUso(f"{percorso}: manca l'elenco «riscontri»")
    return dati["riscontri"]


def _cella(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ") or "—"


def tabella(esiti: list[Esito], fonti: list[Fonte]) -> str:
    righe = ["| id | che cosa | la fonte dice | il master dice | esito |",
             "|---|---|---|---|---|"]
    for e in esiti:
        fonte = f"{e.fonte_dice} ({e.fonte})" if e.fonte_dice else e.fonte
        master = f"{e.master_dice} ({e.master})" if e.master_dice else e.master
        esito = f"**{e.esito}**" if e.esito != "concorda" else e.esito
        if e.dove:
            esito += f" {e.dove}"
        righe.append(f"| {_cella(e.id)} | {_cella(e.cosa)} | {_cella(fonte)} | "
                     f"{_cella(master)} | {esito} |")
    conta = {k: sum(1 for e in esiti if e.esito == k) for k in ("concorda", "discorda", "non trovata")}
    righe += ["", " · ".join(f"{k}: {v}" for k, v in conta.items()), ""]
    righe += [f"Citazioni da {f.nome} ({f.repo}@{f.commit[:8]}): {f.licenza}" for f in fonti]
    return "\n".join(righe) + "\n"


# ---------------------------------------------------------------- comandi

def cmd_scarica(args, cache: Path) -> int:
    if args.verifica:
        cattivi = {f.nome: verifica(f, cache) for f in FONTI.values()}
        for nome, elenco in cattivi.items():
            for rel in elenco:
                print(f"✗ {nome}, {rel}: sha256 diverso da quello fissato")
        for f in FONTI.values():
            m = mancanti(f, cache)
            print(f"{f.nome}: {len(f.file) - len(m)} file su {len(f.file)} in {f.cartella(cache)}")
        return 1 if any(cattivi.values()) else 0
    origini = {}
    for coppia in args.da_cartella or []:
        chiave, _, cartella = coppia.partition("=")
        if chiave not in FONTI or not cartella:
            raise ErroreUso(f"--da-cartella vuole FONTE=CARTELLA, FONTE fra {', '.join(FONTI)}")
        origini[chiave] = Path(cartella).expanduser()
    for f in FONTI.values():
        if args.fonte and f.chiave != args.fonte:
            continue
        if f.chiave in origini:
            n = da_cartella(f, cache, origini[f.chiave])
            print(f"{f.nome}: {n} file copiati da {origini[f.chiave]}, sha256 controllati")
        else:
            assicura(f, cache, rete=not args.offline)
        print(f"{f.nome}: {len(f.file)} file in {f.cartella(cache)} ({f.repo}@{f.commit[:8]})")
    return 0


def cmd_regola(args, cache: Path) -> int:
    nome = args.nome.strip()
    trovate = 0
    if args.fonte in (None, "srd35"):
        base = assicura(SRD35, cache, rete=not args.offline)
        titolo = re.compile(
            # Nell'SRD i titoli dei talenti portano il tipo: «Improved Trip <small>[General]</small>».
            rf"^(?:#{{1,6}}\s*{re.escape(nome)}\s*(?:<small>[^<]*</small>|\[[^\]]*\])?\s*$|"
            rf"\*\*{re.escape(nome)}:?\*\*:?)",
            re.IGNORECASE | re.MULTILINE)
        for rel in sorted(SRD35.file):
            testo = (base / rel).read_text(encoding="utf-8")
            for m in titolo.finditer(testo):
                trovate += 1
                righe = testo[m.start():].split("\n")[:args.righe]
                print(f"## {SRD35.nome}, {rel}:{riga_di(testo, m.start())}\n")
                print("\n".join(pulisci(r) if "<t" in r else r for r in righe).rstrip(), "\n")
    if args.fonte in (None, "pf1"):
        base = assicura(PF1, cache, rete=not args.offline)
        for db in sorted(PF1.file):
            for source, url, testo in sezioni_pf1(base / db, nome):
                trovate += 1
                print(f"## {PF1.nome}, {source} › {nome} ({db})\n")
                print(testo[:args.righe * 80] + ("…" if len(testo) > args.righe * 80 else ""), "\n")
    if not trovate:
        print(f"«{nome}»: nessun titolo con questo nome. Il nome è quello inglese "
              f"dell'SRD (Slaying Arrow, non freccia assassina).", file=sys.stderr)
        return 1
    usate = [f for f in (SRD35, PF1) if args.fonte in (None, f.chiave)]
    print("\n".join(f"Citazioni da {f.nome} ({f.repo}@{f.commit[:8]}): {f.licenza}" for f in usate))
    return 0


def cmd_riscontra(args, cache: Path) -> int:
    voci = leggi_riscontri(Path(args.file))
    servono = sorted({v.get("fonte") for v in voci if v.get("fonte") in FONTI})
    basi = {k: assicura(FONTI[k], cache, rete=not args.offline) for k in servono}
    repo = Path(args.repo).resolve()
    esiti = [riscontra_voce(v, basi, repo) for v in voci]
    testo = tabella(esiti, [FONTI[k] for k in servono])
    print(testo, end="")
    if args.md:
        Path(args.md).write_text(testo, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"fonti": {k: {"repo": FONTI[k].repo, "commit": FONTI[k].commit,
                           "licenza": FONTI[k].licenza} for k in servono},
             "esiti": [e.__dict__ for e in esiti]},
            ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if args.strict and any(e.esito != "concorda" for e in esiti):
        return 1
    return 0


def cmd_licenza(args, cache: Path) -> int:
    for f in FONTI.values():
        print(f"{f.nome} — {f.repo}@{f.commit[:8]}\n  {f.licenza}\n"
              f"  testo completo: {f.cartella(cache) / f.file_licenza}")
    return 0


def costruisci_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="riscontro_srd.py",
        description="Riscontra le regole dei master sull'SRD 3.5 e sul PRD PF1e "
                    "(OGL 1.0a), scaricati a commit fissato in una cache fuori dal repo.",
        epilog="Exit: 0 ok · 1 discordanze con --strict, sha256 sbagliato, regola "
               "non trovata · 2 uso · 3 fonti non disponibili (rete o --offline).")
    p.add_argument("--cache", default=None,
                   help="cartella della cache (default: $RUMBLINGSTONE_SRD_CACHE o "
                        "~/.cache/rumblingstone/srd)")
    p.add_argument("--offline", action="store_true",
                   help="non scaricare: se la cache è incompleta esce 3")
    sub = p.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("scarica", help="riempie la cache a commit fissato, con lo sha256")
    s.add_argument("--fonte", choices=sorted(FONTI), default=None, help="una sola fonte")
    s.add_argument("--da-cartella", nargs="+", metavar="FONTE=DIR", default=None,
                   help="copia da un clone locale invece di scaricare")
    s.add_argument("--verifica", action="store_true",
                   help="rifà lo sha256 dei file in cache, senza scaricare")

    r = sub.add_parser("regola", help="cerca una regola per nome (inglese) nelle due fonti")
    r.add_argument("nome", help="il nome come nell'SRD, es. «Slaying Arrow», «Scent»")
    r.add_argument("--fonte", choices=sorted(FONTI), default=None, help="una sola fonte")
    r.add_argument("--righe", type=int, default=12, help="quante righe mostrare (default 12)")

    c = sub.add_parser("riscontra", help="esegue un file di riscontri (YAML o JSON)")
    c.add_argument("file", help="il file dei riscontri")
    c.add_argument("--repo", default=str(REPO), help="radice per i percorsi dei master")
    c.add_argument("--md", default=None, help="scrive la tabella Markdown anche qui")
    c.add_argument("--json", default=None, help="scrive gli esiti in JSON")
    c.add_argument("--strict", action="store_true",
                   help="esce 1 se resta una discordanza o una regola non trovata")

    sub.add_parser("licenza", help="licenza delle due fonti e dove sta il testo")
    return p


def main(argv: list[str] | None = None) -> int:
    args = costruisci_parser().parse_args(argv)
    cache = cartella_cache(args.cache)
    comandi = {"scarica": cmd_scarica, "regola": cmd_regola,
               "riscontra": cmd_riscontra, "licenza": cmd_licenza}
    try:
        return comandi[args.comando](args, cache)
    except FontiMancanti as e:
        print(f"✗ fonti non disponibili: {e}", file=sys.stderr)
        return ESITO_RETE
    except ImprontaSbagliata as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    except ErroreUso as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
