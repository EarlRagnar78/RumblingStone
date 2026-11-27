#!/usr/bin/env python3
"""memoria_custode.py — la memoria del progetto ha uno specchio e un custode (ADR-0151).

Nei thread la memoria del progetto è una cartella di file (MEMORY.md, l'indice,
più una nota per argomento) che la piattaforma sincronizza. Non ha storia:
nessuno strumento sa quale riga c'era ieri, quindi la regola «archivia prima
di togliere» (ADR-0127) non la misurava nessuno. Questo script le dà una storia
(lo specchio, istantanee complete fuori dal repo) e la controlla:

    python3 scripts/memoria_custode.py specchia
        istantanea della memoria, solo se è cambiata dall'ultima
    python3 scripts/memoria_custode.py verifica [--json]
        ogni riga tolta dall'ultima istantanea è archiviata? (esce 1 se no);
        se passa, l'istantanea avanza
    python3 scripts/memoria_custode.py archivia [--thread "Titolo"]
        scrive in coda una voce con le righe tolte non archiviate
    python3 scripts/memoria_custode.py cerca PAROLE... [--tema T] [--json]
        una risposta da memoria del progetto, file storico e coda
    python3 scripts/memoria_custode.py redigi --uscita DIR
        copia della memoria con le righe riservate sostituite da un'impronta
    python3 scripts/memoria_custode.py --hook-merge       # PreToolUse sul merge di una PR
    python3 scripts/memoria_custode.py --hook-scrittura   # PreToolUse su Write/Edit/MultiEdit
    python3 scripts/memoria_custode.py --riepilogo [--json]

Una riga tolta è archiviata se (a) ogni suo gettone (`memoria_storica._gettoni`:
PR, ADR, MS, SHA, percorsi) compare nel repo, nel file storico, nella coda o
nella memoria nuova, e (b) le sue parole di contenuto (almeno 5 lettere) che non
compaiono più nella memoria nuova sono al più 2, oppure una sola voce del file
storico o della coda ne contiene almeno il 70%. Una riga con un termine di
`<specchio>/RISERVATI.txt` (fuori dal repo, un termine per riga) o con un
indirizzo email resta solo nello specchio: conta come archiviata lì, e
`archivia` non la copia in coda.

Le cartelle: `--memoria` / MEMORIA_PROGETTO_DIR (altrimenti
$CLAUDE_COWORK_MEMORY_PATH_OVERRIDE/team/<mount> dal primo store di
$CLAUDE_MEMORY_STORES), `--specchio` / MEMORIA_SPECCHIO_DIR, `--coda` /
MEMORIA_CODA_DIR, `--radice` per il repo. Nei modi hook una cartella della
memoria assente esce 0 con un messaggio.

Cosa non vede: le scritture del coordinatore non passano dagli hook del repo;
le vede la prima `verifica` dopo, al merge di un thread. Il confronto è per
righe intere e per parole: non capisce se una riga riscritta dice ancora la
stessa cosa con parole diverse (le parole sparite contano come fatti persi).

Solo stdlib, nessuna rete. Import pigri: l'hook di scrittura scatta su ogni Edit.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SPECCHIO = Path("/mnt/project-files/memoria-progetto-specchio")
CODA = Path("/mnt/project-files/memoria-storica-coda")
REGISTRO_REL = Path(".claude") / ".custode-memoria.jsonl"
THREAD_PREDEFINITO = "Memoria del progetto: righe tolte"
TITOLO_VOCE = "Righe tolte dalla memoria del progetto"
ORIGINE = "riga tolta dalla memoria del progetto"

#: Parole di contenuto: almeno tante lettere (dopo minuscole e senza accenti).
LETTERE_MIN = 5
#: Parole sparite dalla memoria che una riga può perdere senza essere archiviata.
MANCANTI_MAX = 2
#: Quota delle parole sparite che una sola voce deve contenere.
COPERTURA_MIN = 0.70
#: Il proprietario e il repo dei merge che l'hook guarda (senza distinzione di maiuscole).
OWNER, REPO = "gsamuele78", "rumblingstone"
ADR = "ADR-0151"


# --------------------------------------------------------------------- cartelle

def cartella_memoria(esplicita: "str | None" = None) -> "Path | None":
    if esplicita:
        return Path(esplicita)
    if os.environ.get("MEMORIA_PROGETTO_DIR"):
        return Path(os.environ["MEMORIA_PROGETTO_DIR"])
    base = os.environ.get("CLAUDE_COWORK_MEMORY_PATH_OVERRIDE")
    if not base:
        return None
    try:
        stores = json.loads(os.environ.get("CLAUDE_MEMORY_STORES") or "[]")
        mount = next(s["mount"] for s in stores if isinstance(s, dict) and s.get("mount"))
    except (ValueError, StopIteration, TypeError):
        return None
    return Path(base) / "team" / mount


def _dentro(p: Path, cartella: Path) -> bool:
    try:
        p.resolve().relative_to(cartella.resolve())
        return True
    except (ValueError, OSError):
        return False


# --------------------------------------------------------------------- testo

def _piano(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


def parole(s: str) -> "set[str]":
    import re
    return {w for w in re.findall(r"[a-z]+", _piano(s)) if len(w) >= LETTERE_MIN}


_EMAIL = None


def ha_email(riga: str) -> bool:
    global _EMAIL
    if _EMAIL is None:
        import re
        _EMAIL = re.compile(r"[\w.%+-]+@[\w-]+(?:\.[\w-]+)+")
    return bool(_EMAIL.search(riga))


def riservati(specchio: Path) -> "list[str]":
    f = specchio / "RISERVATI.txt"
    try:
        righe = f.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [_piano(r.strip()) for r in righe if r.strip() and not r.lstrip().startswith("#")]


def e_riservata(riga: str, termini: "list[str]") -> bool:
    p = _piano(riga)
    return ha_email(riga) or any(t in p for t in termini)


def leggi_memoria(cartella: Path) -> "dict[str, str]":
    return {f.name: f.read_text(encoding="utf-8", errors="replace")
            for f in sorted(cartella.glob("*.md")) if f.is_file()}


def _significativa(r: str) -> bool:
    s = r.strip()
    return bool(s) and s != "---"


def righe_tolte(vecchia: "dict[str, str]", nuova: "dict[str, str]") -> "list[dict]":
    """Le righe della memoria vecchia che non stanno più in nessun file della nuova.

    Una riga spostata in un altro file non è tolta; una riga riscritta sì.
    """
    presenti = {r.strip() for t in nuova.values() for r in t.splitlines()}
    fuori = []
    for nome, testo in sorted(vecchia.items()):
        for n, r in enumerate(testo.splitlines(), 1):
            if _significativa(r) and r.strip() not in presenti:
                fuori.append({"file": nome, "riga": n, "testo": r.strip(),
                              "file_tolto": nome not in nuova})
    return fuori


# --------------------------------------------------------------------- fonti

def voci_storiche(radice: Path) -> "tuple[list, str]":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_storica as ms
    f = radice / "plans" / "MEMORIA-STORICA.md"
    testo = f.read_text(encoding="utf-8") if f.is_file() else ""
    return ms.leggi(testo), testo


def voci_coda(coda: "Path | None") -> "tuple[list[dict], list[str], str]":
    """Le voci della coda (con file e testo), i difetti di forma, il testo intero."""
    if coda is None or not coda.is_dir():
        return [], [f"cartella della coda assente: {coda}"], ""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_coda as mc
    per_file, errori = mc.controlla_coda(coda)
    voci = []
    for nome, vv in per_file.items():
        for v in vv:
            voci.append({"file": nome + ".md", "riga": v["riga"], "data": v["data"],
                         "titolo": v["titolo"], "campi": v["campi"],
                         "testo": v["titolo"] + "\n" + "\n".join(v["righe"])})
    testo = "\n".join((coda / f).read_text(encoding="utf-8", errors="replace")
                      for f in sorted(os.listdir(coda)) if f.endswith(".md"))
    return voci, errori, testo


class Contesto:
    """Le fonti dell'archiviazione, lette una volta e solo quando servono."""

    def __init__(self, radice: Path, coda: "Path | None", nuova: "dict[str, str]"):
        self.radice, self.coda, self.nuova = radice, coda, nuova
        self._storiche = self._coda = self._corpo = self._parole_voci = None
        self.parole_nuove = set().union(*(parole(t) for t in nuova.values())) if nuova else set()
        self.testo_nuovo = "\n".join(nuova.values())

    def storiche(self):
        if self._storiche is None:
            self._storiche = voci_storiche(self.radice)
        return self._storiche

    def coda_(self):
        if self._coda is None:
            self._coda = voci_coda(self.coda)
        return self._coda

    def parole_voci(self) -> "list[tuple[str, set[str]]]":
        if self._parole_voci is None:
            self._parole_voci = ([(v.id, parole(v.testo_md)) for v in self.storiche()[0]]
                                 + [(f"coda:{v['file']}:{v['riga']}", parole(v["testo"]))
                                    for v in self.coda_()[0]])
        return self._parole_voci

    def gettone_noto(self, g: str) -> bool:
        import re

        def c(testo: str) -> bool:
            if g not in testo:
                return False
            return re.search(re.escape(g) + r"(?!\d)", testo) is not None if g[-1].isdigit() else True
        if c(self.testo_nuovo) or c(self.coda_()[2]) or c(self.storiche()[1]):
            return True
        if self._corpo is None:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import memoria_storica as ms
            self._corpo = ms._corpo_del_repo(self.radice)
        return c(self._corpo)


def classifica(riga: dict, ctx: Contesto, termini: "list[str]") -> dict:
    """Aggiunge a una riga tolta lo stato: specchio, archiviata o non_archiviata."""
    if e_riservata(riga["testo"], termini):
        return {**riga, "stato": "specchio"}
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_storica as ms
    gettoni_mancanti = [g for g in ms._gettoni(riga["testo"]) if not ctx.gettone_noto(g)]
    mancanti = sorted(parole(riga["testo"]) - ctx.parole_nuove)
    voce = None
    ok_parole = len(mancanti) <= MANCANTI_MAX
    if not ok_parole:
        for ident, pv in ctx.parole_voci():
            if len(set(mancanti) & pv) >= COPERTURA_MIN * len(mancanti):
                voce, ok_parole = ident, True
                break
    stato = "archiviata" if ok_parole and not gettoni_mancanti else "non_archiviata"
    return {**riga, "stato": stato, "gettoni_mancanti": gettoni_mancanti,
            "parole_mancanti": [] if voce else mancanti, "voce": voce}


# --------------------------------------------------------------------- specchio

class Lucchetto:
    def __init__(self, cartella: Path):
        self.f = cartella / ".lucchetto"

    def __enter__(self):
        import fcntl
        self.f.parent.mkdir(parents=True, exist_ok=True)
        self.h = open(self.f, "a")
        fcntl.flock(self.h, fcntl.LOCK_EX)
        return self

    def __exit__(self, *_):
        import fcntl
        fcntl.flock(self.h, fcntl.LOCK_UN)
        self.h.close()


def _sha(testo: str) -> str:
    import hashlib
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def ultima_istantanea(specchio: Path) -> "tuple[str | None, dict[str, str]]":
    """Il nome e i file dell'ultima istantanea (None, {} se non c'è)."""
    try:
        nome = (specchio / "ULTIMA.txt").read_text(encoding="utf-8").strip()
    except OSError:
        return None, {}
    d = specchio / "istantanee" / nome
    if not nome or not d.is_dir():
        return None, {}
    return nome, {f.name: f.read_text(encoding="utf-8", errors="replace")
                  for f in sorted(d.glob("*.md"))}


def specchia(memoria: "dict[str, str]", specchio: Path, sorgente: Path) -> "tuple[str, bool]":
    """Scrive un'istantanea se il contenuto differisce dall'ultima. (nome, scritta?)"""
    impronte = {n: _sha(t) for n, t in memoria.items()}
    with Lucchetto(specchio):
        nome, _ = ultima_istantanea(specchio)
        if nome:
            try:
                prima = json.loads((specchio / "istantanee" / nome / "MANIFEST.json")
                                   .read_text(encoding="utf-8"))["file"]
            except (OSError, ValueError, KeyError):
                prima = None
            if prima == impronte:
                return nome, False
        base = specchio / "istantanee"
        base.mkdir(parents=True, exist_ok=True)
        stampo = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        nuovo, k = stampo, 1
        while (base / nuovo).exists():
            k += 1
            nuovo = f"{stampo}-{k}"
        tmp = base / f".tmp-{nuovo}-{os.getpid()}"
        tmp.mkdir()
        for n, t in memoria.items():
            (tmp / n).write_text(t, encoding="utf-8")
        (tmp / "MANIFEST.json").write_text(json.dumps(
            {"creata": nuovo, "sorgente": str(sorgente), "file": impronte},
            ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        os.rename(tmp, base / nuovo)
        t_ultima = specchio / f".ULTIMA.{os.getpid()}.tmp"
        t_ultima.write_text(nuovo + "\n", encoding="utf-8")
        os.replace(t_ultima, specchio / "ULTIMA.txt")
        return nuovo, True


# --------------------------------------------------------------------- verifica

def verifica(memoria_dir: Path, specchio: Path, coda: "Path | None", radice: Path,
             avanza: bool = True) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_storica as ms
    nuova = leggi_memoria(memoria_dir)
    nome, vecchia = ultima_istantanea(specchio)
    ctx = Contesto(radice, coda, nuova)
    termini = riservati(specchio)
    righe = [classifica(r, ctx, termini) for r in righe_tolte(vecchia, nuova)] if nome else []
    non = [r for r in righe if r["stato"] == "non_archiviata"]
    avvisi, sopra_limite, byte = [], False, None
    if (memoria_dir / "MEMORY.md").is_file():
        m = ms.misura_memoria(memoria_dir)
        byte, sopra_limite = m["byte"], m["sopra_limite"]
        if m["sopra_limite"]:
            avvisi.append(f"MEMORY.md {m['byte']} byte, oltre il limite {m['limite']}: "
                          "la piattaforma taglia l'indice (blocca)")
        elif m["sopra_tetto"]:
            avvisi.append(f"MEMORY.md {m['byte']} byte, sopra il tetto {m['tetto']} (ADR-0139)")
    _, errori_coda, _ = ctx.coda_()
    if errori_coda:
        avvisi.append(f"coda della memoria storica: {len(errori_coda)} difetti di forma "
                      f"(memoria_coda.py --check), il primo: {errori_coda[0]}")
    passa = not non and not sopra_limite
    istantanea, scritta = nome, False
    if passa and avanza:
        istantanea, scritta = specchia(nuova, specchio, memoria_dir)
    return {"esito": "passa" if passa else "fallisce", "prima_volta": nome is None,
            "istantanea_confronto": nome, "istantanea": istantanea, "istantanea_nuova": scritta,
            "righe_tolte": len(righe), "archiviate": [r for r in righe if r["stato"] == "archiviata"],
            "solo_specchio": [{k: r[k] for k in ("file", "riga")} for r in righe
                              if r["stato"] == "specchio"],
            "non_archiviate": non, "byte_memory": byte, "sopra_limite": sopra_limite,
            "avvisi": avvisi}


def _descrivi(r: dict) -> str:
    perso = []
    if r.get("parole_mancanti"):
        perso.append("parole sparite: " + ", ".join(r["parole_mancanti"][:8]))
    if r.get("gettoni_mancanti"):
        perso.append("gettoni che nessuno ha: " + ", ".join(r["gettoni_mancanti"]))
    return (f"{r['file']} riga {r['riga']}{' (file tolto)' if r.get('file_tolto') else ''}: "
            f"«{r['testo'][:120]}» ({'; '.join(perso)})")


def stampa_verifica(v: dict) -> None:
    if v["prima_volta"]:
        print(f"✓ prima verifica: istantanea {v['istantanea']} scritta, nessun confronto")
    for r in v["non_archiviate"]:
        print(f"✗ {_descrivi(r)}")
    for a in v["avvisi"]:
        print(f"⚠ {a}")
    if v["esito"] == "passa":
        if not v["prima_volta"]:
            print(f"✓ {v['righe_tolte']} righe tolte dall'istantanea {v['istantanea_confronto']}, "
                  f"tutte archiviate ({len(v['solo_specchio'])} solo nello specchio); "
                  f"istantanea {'nuova ' if v['istantanea_nuova'] else ''}{v['istantanea']}")
    else:
        if v["non_archiviate"]:
            print(f"✗ {len(v['non_archiviate'])} righe tolte senza archivio. Rimedio: "
                  "`python3 scripts/memoria_custode.py archivia`, poi di nuovo `verifica`.")


# --------------------------------------------------------------------- archivia

def voce_di_coda(righe: "list[dict]", data: str, titolo: str) -> str:
    pezzi = " · ".join(f"`{r['file']}` riga {r['riga']}: «{r['testo']}»" for r in righe)
    return (f"### MS-???? · {data} · {titolo}\n\n"
            f"- **Data:** {data}\n- **PR:** —\n- **ADR:** —\n- **Temi:** memoria\n"
            f"- **Origine:** {ORIGINE}\n"
            f"- **Testo:** Righe tolte dalla memoria del progetto, archiviate con "
            f"`memoria_custode.py archivia` prima che l'istantanea avanzasse: {pezzi}\n")


def archivia(memoria_dir: Path, specchio: Path, coda: Path, radice: Path, thread: str) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_coda as mc
    v = verifica(memoria_dir, specchio, coda, radice, avanza=False)
    nome, vecchia = ultima_istantanea(specchio)
    termini = riservati(specchio)
    tolte = righe_tolte(vecchia, leggi_memoria(memoria_dir)) if nome else []
    rifiutate = [r for r in tolte if e_riservata(r["testo"], termini)]
    da_scrivere = v["non_archiviate"]
    file_coda = coda / (mc.nome_file(thread) + ".md")
    scritta = None
    if da_scrivere:
        data = time.strftime("%Y-%m-%d", time.gmtime())
        coda.mkdir(parents=True, exist_ok=True)
        with Lucchetto(coda):
            esistente = file_coda.read_text(encoding="utf-8") if file_coda.is_file() else ""
            voci, _ = mc.leggi_coda(esistente)
            titolo, k = TITOLO_VOCE, 1
            while any(x["data"] == data and x["titolo"] == titolo for x in voci):
                k += 1
                titolo = f"{TITOLO_VOCE} ({k})"
            testo = voce_di_coda(da_scrivere, data, titolo)
            _, difetti = mc.leggi_coda(testo)
            if difetti:
                raise ValueError(f"voce di coda scritta male: {difetti}")
            sep = "" if not esistente else ("\n" if esistente.endswith("\n") else "\n\n")
            with file_coda.open("a", encoding="utf-8") as h:
                h.write(sep + testo)
        scritta = titolo
    return {"file_coda": str(file_coda), "voce": scritta, "righe_scritte": len(da_scrivere),
            "rifiutate": [{k: r[k] for k in ("file", "riga")} for r in rifiutate]}


# --------------------------------------------------------------------- cerca

def cerca(memoria_dir: "Path | None", coda: "Path | None", radice: Path,
          chiavi: "list[str]", tema: "str | None") -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import memoria_storica as ms
    piane = [_piano(p) for p in chiavi]
    risultati, dove = [], {}
    # 1. memoria del progetto: righe; il tema vale come parola in più
    parole_mem = piane + ([_piano(tema)] if tema else [])
    n = 0
    if memoria_dir and memoria_dir.is_dir():
        for nome, testo in leggi_memoria(memoria_dir).items():
            for i, r in enumerate(testo.splitlines(), 1):
                if r.strip() and all(p in _piano(r) for p in parole_mem):
                    risultati.append({"fonte": "memoria", "file": nome, "riga": i, "testo": r.strip()})
                    n += 1
        dove["memoria"] = n
    else:
        dove["memoria"] = None
    # 2. file storico, con i filtri di memoria_storica
    voci, _ = voci_storiche(radice)
    trovate = ms.filtra(voci, chiavi, tema=tema)
    for v in trovate:
        risultati.append({"fonte": "storica", "id": v.id, "data": v.data, "titolo": v.titolo,
                          "file": "plans/MEMORIA-STORICA.md", "riga": v.riga,
                          "testo": v.campi.get("Testo", "")})
    dove["storica"] = len(trovate)
    # 3. coda
    vc, _, _ = voci_coda(coda)
    n = 0
    if coda and coda.is_dir():
        for v in vc:
            corpo = _piano(v["testo"])
            if all(p in corpo for p in piane) and (
                    not tema or _piano(tema) in {_piano(t) for t in v["campi"].get("Temi", "").split()}):
                risultati.append({"fonte": "coda", "file": v["file"], "riga": v["riga"],
                                  "data": v["data"], "titolo": v["titolo"],
                                  "testo": v["campi"].get("Testo", "")})
                n += 1
        dove["coda"] = n
    else:
        dove["coda"] = None
    return {"parole": chiavi, "tema": tema, "per_fonte": dove, "risultati": risultati}


def stampa_cerca(r: dict) -> None:
    for x in r["risultati"]:
        if x["fonte"] == "memoria":
            print(f"[memoria] {x['file']}:{x['riga']}  {x['testo'][:160]}")
        elif x["fonte"] == "storica":
            print(f"[storica] {x['id']} · {x['data']} · {x['titolo']} (riga {x['riga']})")
        else:
            print(f"[coda] {x['file']}:{x['riga']} · {x['data']} · {x['titolo']}")
    for fonte, n in r["per_fonte"].items():
        if n is None:
            print(f"○ {fonte}: cartella assente, non cercata")
        elif n == 0:
            print(f"○ {fonte}: nessun risultato")


# --------------------------------------------------------------------- redigi

LEGGIMI = """# Memoria del progetto, copia redatta

Generata da `python3 scripts/memoria_custode.py redigi` ({ADR}) il {quando}, dalla
cartella della memoria del progetto dei thread ({n} file). Ogni riga che contiene un
termine riservato (`RISERVATI.txt`, che sta solo nello specchio, fuori dal repo) o
un indirizzo email è sostituita da `[riga riservata · sha256:<8 hex>]`, l'impronta
della riga intera: il testo vero resta solo nelle istantanee dello specchio.

Questa cartella non si modifica a mano: si corregge la memoria e si rigenera.
"""


def redigi(memoria_dir: Path, specchio: Path, uscita: Path) -> dict:
    termini = riservati(specchio)
    if not termini:
        raise ValueError(f"{specchio / 'RISERVATI.txt'} manca o è vuoto: senza l'elenco dei "
                         "termini riservati una copia nel repo porterebbe dati personali")
    memoria = leggi_memoria(memoria_dir)
    uscita.mkdir(parents=True, exist_ok=True)
    marcatore = uscita / "LEGGIMI.md"
    if marcatore.is_file() and "memoria_custode.py redigi" in marcatore.read_text(encoding="utf-8"):
        for f in uscita.glob("*.md"):
            if f.name not in memoria and f.name != "LEGGIMI.md":
                f.unlink()
    sostituite = 0
    for nome, testo in memoria.items():
        righe = []
        for r in testo.splitlines():
            if r.strip() and e_riservata(r, termini):
                righe.append(f"[riga riservata · sha256:{_sha(r)[:8]}]")
                sostituite += 1
            else:
                righe.append(r)
        (uscita / nome).write_text("\n".join(righe) + ("\n" if testo.endswith("\n") else ""),
                                   encoding="utf-8")
    marcatore.write_text(LEGGIMI.format(ADR=ADR, quando=time.strftime("%Y-%m-%d", time.gmtime()),
                                        n=len(memoria)), encoding="utf-8")
    return {"file": len(memoria), "righe_sostituite": sostituite, "uscita": str(uscita)}


# --------------------------------------------------------------------- hook

def _registra(radice: Path, riga: dict) -> None:
    try:
        f = radice / REGISTRO_REL
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a", encoding="utf-8") as h:
            h.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **riga},
                               ensure_ascii=False) + "\n")
    except OSError:
        pass


def applica_edit(testo: str, vecchio: str, nuovo: str, tutti: bool) -> str:
    return testo.replace(vecchio, nuovo) if tutti else testo.replace(vecchio, nuovo, 1)


def contenuto_nuovo(strumento: str, inp: dict, attuale: str) -> str:
    if strumento == "Write":
        return str(inp.get("content", ""))
    if strumento == "Edit":
        return applica_edit(attuale, str(inp.get("old_string", "")), str(inp.get("new_string", "")),
                            bool(inp.get("replace_all")))
    if strumento == "MultiEdit":
        t = attuale
        for e in inp.get("edits") or []:
            t = applica_edit(t, str(e.get("old_string", "")), str(e.get("new_string", "")),
                             bool(e.get("replace_all")))
        return t
    return attuale


def hook_merge(grezzo: str, a) -> int:
    t0 = time.perf_counter()
    try:
        ev = json.loads(grezzo or "{}")
        inp = ev.get("tool_input") or {}
        if (str(inp.get("owner", "")).lower(), str(inp.get("repo", "")).lower()) != (OWNER, REPO):
            _registra(a.radice, {"modo": "merge", "esito": "fuori",
                                 "durata_ms": round((time.perf_counter() - t0) * 1000, 1)})
            return 0
        mem = cartella_memoria(a.memoria)
        if mem is None or not mem.is_dir():
            print(f"memoria_custode: cartella della memoria del progetto assente ({mem}), "
                  "merge lasciato passare", file=sys.stderr)
            _registra(a.radice, {"modo": "merge", "esito": "senza memoria",
                                 "durata_ms": round((time.perf_counter() - t0) * 1000, 1)})
            return 0
        v = verifica(mem, a.specchio, a.coda, a.radice)
    except Exception as e:  # noqa: BLE001 — un hook rotto non ferma il lavoro
        print(f"memoria_custode: errore interno ({e}), merge lasciato passare", file=sys.stderr)
        return 0
    esito = "passa" if v["esito"] == "passa" else "blocca"
    _registra(a.radice, {"modo": "merge", "esito": esito, "pr": inp.get("pullNumber"),
                         "non_archiviate": len(v["non_archiviate"]), "avvisi": len(v["avvisi"]),
                         "durata_ms": round((time.perf_counter() - t0) * 1000, 1)})
    if esito == "blocca":
        righe = "; ".join(_descrivi(r) for r in v["non_archiviate"][:5])
        altre = len(v["non_archiviate"]) - 5
        motivo = (f"Merge fermato ({ADR}): ")
        if v["non_archiviate"]:
            motivo += (f"{len(v['non_archiviate'])} righe tolte dalla memoria del progetto "
                       f"dall'istantanea {v['istantanea_confronto']} non sono archiviate né nel "
                       f"repo né in coda: {righe}" + (f"; e altre {altre}" if altre > 0 else "")
                       + ". Lancia `python3 scripts/memoria_custode.py archivia` (scrive la voce "
                       "in coda; le righe con dati riservati restano solo nello specchio), poi "
                       "rilancia il merge.")
        if v["sopra_limite"]:
            motivo += (f" MEMORY.md è {v['byte_memory']} byte, oltre il limite di 16384: "
                       "archivia e togli righe di cronologia, poi rilancia il merge.")
        print(motivo, file=sys.stderr)
        return 2
    return 0


def hook_scrittura(grezzo: str, a) -> int:
    t0 = time.perf_counter()
    try:
        ev = json.loads(grezzo or "{}")
        inp = ev.get("tool_input") or {}
        fp = inp.get("file_path")
        mem = cartella_memoria(a.memoria)
        if not fp or mem is None or not _dentro(Path(fp), mem):
            return 0
        if not mem.is_dir():
            return 0
        f = Path(fp)
        attuale = f.read_text(encoding="utf-8", errors="replace") if f.is_file() else ""
        nuovo = contenuto_nuovo(ev.get("tool_name", ""), inp, attuale)
        if nuovo == attuale or f.suffix != ".md":
            return 0
        prima = {f.name: attuale}
        nuova = leggi_memoria(mem)
        nuova[f.name] = nuovo
        tolte = righe_tolte(prima, nuova)
        if not tolte:
            _registra(a.radice, {"modo": "scrittura", "esito": "passa", "file": f.name,
                                 "durata_ms": round((time.perf_counter() - t0) * 1000, 1)})
            return 0
        ctx = Contesto(a.radice, a.coda, nuova)
        termini = riservati(a.specchio)
        non = [r for r in (classifica(r, ctx, termini) for r in tolte) if r["stato"] == "non_archiviata"]
    except Exception as e:  # noqa: BLE001
        print(f"memoria_custode: errore interno ({e}), scrittura lasciata passare", file=sys.stderr)
        return 0
    _registra(a.radice, {"modo": "scrittura", "esito": "avvisa" if non else "passa", "file": f.name,
                         "righe_tolte": len(tolte), "non_archiviate": len(non),
                         "durata_ms": round((time.perf_counter() - t0) * 1000, 1)})
    if non:
        elenco = "; ".join(_descrivi(r) for r in non[:6])
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": (
            f"Custode della memoria ({ADR}, canale testing: non blocca): questa scrittura toglie "
            f"{len(non)} righe dalla memoria del progetto che non sono archiviate né nel repo né "
            f"in coda: {elenco}. Prima di toglierle archiviale (ADR-0127): dopo la scrittura "
            "lancia `python3 scripts/memoria_custode.py archivia`, che le scrive in coda "
            "dall'ultima istantanea, oppure scrivi tu una voce MS-???? nel file di coda del "
            "thread. Il merge del thread si ferma finché non sono archiviate.")}},
            ensure_ascii=False))
    return 0


def riepilogo(radice: Path) -> dict:
    righe = []
    try:
        for r in (radice / REGISTRO_REL).read_text(encoding="utf-8").splitlines():
            try:
                righe.append(json.loads(r))
            except ValueError:
                continue
    except OSError:
        pass

    def p95(xs):
        xs = sorted(xs)
        return xs[min(len(xs) - 1, int(round(0.95 * (len(xs) - 1))))] if xs else None
    merge = [r for r in righe if r.get("modo") == "merge" and r.get("esito") != "fuori"]
    scr = [r for r in righe if r.get("modo") == "scrittura"]
    return {"merge_visti": len(merge), "blocchi": sum(r.get("esito") == "blocca" for r in merge),
            "scritture_viste": len(scr), "avvisi": sum(r.get("esito") == "avvisa" for r in scr),
            "p95_ms": {"merge": p95([r["durata_ms"] for r in merge if "durata_ms" in r]),
                       "scrittura": p95([r["durata_ms"] for r in scr if "durata_ms" in r])}}


# --------------------------------------------------------------------- main

COMANDI = ("specchia", "verifica", "archivia", "cerca", "redigi")


def main(argv: "list[str] | None" = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", nargs="?", choices=COMANDI, help="Che cosa fare.")
    ap.add_argument("parole", nargs="*", help="Con cerca: le parole, tutte presenti (senza badare "
                    "a maiuscole e accenti).")
    ap.add_argument("--tema", help="Con cerca: un tema (campo Temi nel file storico e in coda; "
                    "una parola in più nella memoria).")
    ap.add_argument("--json", action="store_true", help="Uscita per un agente.")
    ap.add_argument("--thread", default=THREAD_PREDEFINITO,
                    help=f"Con archivia: il titolo del thread, cioè il file di coda "
                         f"(predefinito «{THREAD_PREDEFINITO}»).")
    ap.add_argument("--uscita", help="Con redigi: la cartella dove scrivere la copia redatta.")
    ap.add_argument("--memoria", default=None, help="La cartella della memoria del progetto "
                    "(o MEMORIA_PROGETTO_DIR, o dalle variabili della piattaforma).")
    ap.add_argument("--specchio", default=os.environ.get("MEMORIA_SPECCHIO_DIR", str(SPECCHIO)),
                    help=f"La cartella dello specchio (o MEMORIA_SPECCHIO_DIR; predefinita {SPECCHIO}).")
    ap.add_argument("--coda", default=os.environ.get("MEMORIA_CODA_DIR", str(CODA)),
                    help=f"La cartella della coda (o MEMORIA_CODA_DIR; predefinita {CODA}).")
    ap.add_argument("--radice", default=str(RADICE), help="La radice del repo.")
    ap.add_argument("--hook-merge", action="store_true", help="PreToolUse sul merge di una PR "
                    "(evento su stdin): esce 2 se la verifica fallisce.")
    ap.add_argument("--hook-scrittura", action="store_true", help="PreToolUse su Write, Edit e "
                    "MultiEdit (evento su stdin): avvisa, non blocca.")
    ap.add_argument("--riepilogo", action="store_true", help="I conti del registro degli hook.")
    a = ap.parse_intermixed_args(argv)
    a.specchio, a.coda, a.radice = Path(a.specchio), Path(a.coda), Path(a.radice)

    if a.hook_scrittura:
        return hook_scrittura(sys.stdin.read(), a)
    if a.hook_merge:
        return hook_merge(sys.stdin.read(), a)
    if a.riepilogo:
        r = riepilogo(a.radice)
        print(json.dumps(r, ensure_ascii=False, indent=None if a.json else 1))
        return 0
    if a.comando is None:
        ap.print_help()
        return 2

    mem = cartella_memoria(a.memoria)
    if a.comando == "cerca":
        if not a.parole and not a.tema:
            print("cerca vuole almeno una parola o --tema", file=sys.stderr)
            return 2
        r = cerca(mem, a.coda, a.radice, a.parole, a.tema)
        print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else stampa_cerca(r)
        return 0
    if mem is None or not mem.is_dir():
        print(f"cartella della memoria del progetto assente: {mem} (--memoria o "
              "MEMORIA_PROGETTO_DIR)", file=sys.stderr)
        return 2
    if a.comando == "specchia":
        nome, scritta = specchia(leggi_memoria(mem), a.specchio, mem)
        print(f"✓ istantanea {'nuova ' if scritta else 'invariata, '}{nome}")
        return 0
    if a.comando == "verifica":
        v = verifica(mem, a.specchio, a.coda, a.radice)
        print(json.dumps(v, ensure_ascii=False, indent=1)) if a.json else stampa_verifica(v)
        return 0 if v["esito"] == "passa" else 1
    if a.comando == "archivia":
        r = archivia(mem, a.specchio, a.coda, a.radice, a.thread)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            if r["voce"]:
                print(f"✓ {r['righe_scritte']} righe in «{r['voce']}», {r['file_coda']}")
            else:
                print("✓ nessuna riga da archiviare in coda")
            for x in r["rifiutate"]:
                print(f"○ {x['file']} riga {x['riga']}: dati riservati o email, rifiutata: "
                      "resta solo nello specchio")
        return 0
    if a.comando == "redigi":
        if not a.uscita:
            print("redigi vuole --uscita DIR", file=sys.stderr)
            return 2
        try:
            r = redigi(mem, a.specchio, Path(a.uscita))
        except ValueError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1
        print(json.dumps(r, ensure_ascii=False) if a.json else
              f"✓ {r['file']} file in {r['uscita']}, {r['righe_sostituite']} righe riservate sostituite")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
