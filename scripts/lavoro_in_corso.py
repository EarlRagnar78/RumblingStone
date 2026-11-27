#!/usr/bin/env python3
"""lavoro_in_corso.py — il lavoro in sviluppo che non è ancora su `main`, in una pagina.

Il 2026-11-27 il DM non trovava il lavoro aperto: stava sparso fra PR in bozza,
rami, `plans/contenuti-nei-rami.json`, le cartelle condivise dei thread cloud
(`/mnt/project-files`, che sul suo PC non c'è) e i thread di progetto.
`MEMORIA.md` racconta ciò che è su `main` ed è un cancello deterministico di CI:
questo script non la tocca e non la ripete. Fa l'istantanea dal vivo di ciò che
sta FUORI da main, e la scrive in `plans/LAVORO-IN-CORSO.md`.

Le fonti, ognuna con la sua casa:

* il registro curato dei filoni, `plans/lavoro-in-corso.json`: un filone è un
  pezzo di lavoro con il suo thread, le sue PR, i suoi rami, le sue cartelle
  condivise, che cosa aspetta e il passo dopo;
* le PR aperte, dalla REST di GitHub (`/pulls`, senza GraphQL e senza `gh`), o
  da un file con `--pr-json` (formato REST, o `gh pr list --json
  number,title,headRefName,isDraft,updatedAt,url,body`). Una PR si attacca a un
  filone se il suo numero è nel registro, se il suo ramo lo è, o se il corpo
  porta `thread=cmsg_…` uguale al `thread_id` del filone;
* i rami di `origin` (`git for-each-ref`), con la data dell'ultimo commit;
* le cartelle di primo livello della cartella condivisa (`--mnt`), con il primo
  titolo del loro LEGGIMI.md o README.md. Mai il contenuto dei file;
* il canale di ogni componente della piattaforma (ADR-0099), dalle tabelle di
  §2 di `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md`, scritte a mano finché il
  lotto P1 non porta il canale in `binari.py` (`canali_piattaforma`).

La pagina segnala cosa non ha un posto (PR, rami `claude/*` recenti, cartelle
recenti) e cosa va aggiornato (PR del registro non più aperte, PR ferme da oltre
30 giorni, filoni con `aggiornato` più vecchio di 14 giorni).

⚠️ Limiti dichiarati:
  * la pagina dipende da rete, clone e macchina: NON è un cancello di CI e non
    deve diventarlo. In CI entra solo `--check`, che valida il registro offline;
  * vede i rami che il clone conosce: `--fetch` scarica prima i rami di origin;
  * le date delle cartelle sono gli mtime del filesystem: una cartella copiata
    di peso può sembrare recente;
  * i thread non si leggono da qui (stanno su claude.ai): il registro li nomina,
    e il legame con le PR passa dal `thread=` scritto nel loro corpo.

Uso:
    python3 scripts/lavoro_in_corso.py                 # rigenera plans/LAVORO-IN-CORSO.md
    python3 scripts/lavoro_in_corso.py --fetch         # prima aggiorna i rami di origin
    python3 scripts/lavoro_in_corso.py --stdout        # la pagina a video, niente file
    python3 scripts/lavoro_in_corso.py --json
    python3 scripts/lavoro_in_corso.py --offline       # senza rete: niente PR
    python3 scripts/lavoro_in_corso.py --pr-json prs.json --mnt DIR
    python3 scripts/lavoro_in_corso.py --check         # valida solo il registro (CI)

Exit code: 0 = pagina fatta (anche con la rete giù: lo dice la pagina) o
registro valido · 1 = registro malformato · 2 = uso errato.

Solo stdlib.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
REGISTRO = RADICE / "plans" / "lavoro-in-corso.json"
CONTENUTI = RADICE / "plans" / "contenuti-nei-rami.json"
USCITA = RADICE / "plans" / "LAVORO-IN-CORSO.md"
PIANO_PIATTAFORMA = RADICE / "plans" / "PIANO-PIATTAFORMA-DI-SVILUPPO.md"
MNT = Path("/mnt/project-files")

GIORNI = 14        # finestra dei rami e delle cartelle, ed età massima di un filone
FERMA = 30         # oltre, una PR senza attività è ferma (regola del progetto)
TAGLIO = 160       # caratteri di una cella, oltre si taglia

#: Gli stati ammessi di un filone, e cosa vogliono dire. Uno stato nuovo si aggiunge qui.
STATI = {
    "in-corso": "qualcuno ci lavora: thread aperto o PR che si muove",
    "aspetta-jfs": "fermo su una decisione, una prova o una revisione del DM",
    "in-prova": "su main o quasi, in canale testing: si misura prima di dirlo finito",
    "fermo": "nessuno ci lavora: da riprendere, chiudere o portare",
}

CAMPI_TESTO = ("id", "titolo", "stato", "thread", "aspetta", "prossimo", "aggiornato", "canale")

#: I canali di ADR-0099 che un filone può dichiarare (facoltativo; vuoto = non si sa).
CANALI_FILONE = ("stable", "testing", "unstable")
#: I canali in cui si normalizza l'ultima colonna delle tabelle di §2, nell'ordine della pagina.
CANALI = ("stable", "testing", "unstable", "uscito", "non-si-adotta", "altro")
_CANALE_RE = re.compile(r"^\W*(stable|testing|unstable|uscito|non si adotta)\b", re.I)
_DAL_RE = re.compile(r"\bdal (\d{4}-\d{2}-\d{2})\b")
CAMPI_LISTA = ("pr", "rami", "mnt", "repo")
OBBLIGATORI = ("id", "titolo", "stato", "aggiornato")

THREAD_RE = re.compile(r"thread=(cmsg_[A-Za-z0-9]+)")
THREAD_ID = re.compile(r"^cmsg_[A-Za-z0-9]+$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


# --- il registro --------------------------------------------------------------

def leggi_registro(percorso: "Path | None" = None) -> dict:
    return json.loads((percorso or REGISTRO).read_text(encoding="utf-8"))


def leggi_contenuti(percorso: "Path | None" = None) -> dict:
    """Il registro di contenuti_nei_rami: un ramo che ha un posto lì non è sciolto."""
    p = percorso or CONTENUTI
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _data_iso(s: object) -> "date | None":
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def valida(dati: object, radice: Path = RADICE) -> "list[str]":
    """Gli errori del registro: offline, deterministico, è il `--check` di CI."""
    if not isinstance(dati, dict):
        return ["il registro non è un oggetto JSON"]
    errori: list[str] = []
    filoni = dati.get("filoni")
    if not isinstance(filoni, list):
        return ["manca la lista «filoni»"]
    visti: set = set()
    for i, f in enumerate(filoni):
        if not isinstance(f, dict):
            errori.append(f"filone {i}: non è un oggetto")
            continue
        nome = f.get("id") or f"#{i}"
        for c in OBBLIGATORI:
            if not f.get(c):
                errori.append(f"{nome}: manca «{c}» (o è vuoto)")
        for c in CAMPI_TESTO:
            if c in f and not isinstance(f[c], str):
                errori.append(f"{nome}: «{c}» deve essere una stringa")
        for c in CAMPI_LISTA:
            if c in f and not isinstance(f[c], list):
                errori.append(f"{nome}: «{c}» deve essere una lista")
        ignoti = set(f) - set(CAMPI_TESTO) - set(CAMPI_LISTA) - {"thread_id"}
        if ignoti:
            errori.append(f"{nome}: campi non previsti: {', '.join(sorted(ignoti))}")
        if isinstance(f.get("id"), str):
            if not SLUG.match(f["id"]):
                errori.append(f"{nome}: id non è uno slug (minuscole, cifre, trattini)")
            if f["id"] in visti:
                errori.append(f"{nome}: id ripetuto")
            visti.add(f["id"])
        if f.get("stato") and f.get("stato") not in STATI:
            errori.append(f"{nome}: stato «{f.get('stato')}» non ammesso ({', '.join(STATI)})")
        if "aggiornato" in f and _data_iso(f["aggiornato"]) is None:
            errori.append(f"{nome}: aggiornato «{f['aggiornato']}» non è una data AAAA-MM-GG")
        if "thread_id" in f and not (isinstance(f["thread_id"], str)
                                     and THREAD_ID.match(f["thread_id"])):
            errori.append(f"{nome}: thread_id «{f['thread_id']}» non è un id cmsg_…")
        for n in f.get("pr") or []:
            if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
                errori.append(f"{nome}: pr «{n}» non è un numero intero")
        for c in ("rami", "mnt", "repo"):
            for v in f.get(c) or []:
                if not isinstance(v, str) or not v:
                    errori.append(f"{nome}: {c}: voce vuota o non stringa")
        for v in f.get("mnt") or []:
            if isinstance(v, str) and (v.startswith("/") or ".." in Path(v).parts):
                errori.append(f"{nome}: mnt «{v}» va scritta relativa alla cartella condivisa")
        for v in f.get("repo") or []:
            if isinstance(v, str) and v and not (radice / v).exists():
                errori.append(f"{nome}: repo «{v}» non esiste nel repo")
        testo = json.dumps(f, ensure_ascii=False)
        if EMAIL.search(testo):
            errori.append(f"{nome}: contiene un indirizzo email (niente dati personali)")
    for f in filoni:
        if isinstance(f, dict) and f.get("canale") not in (None, "", *CANALI_FILONE):
            errori.append(f"{f.get('id') or '?'}: canale «{f['canale']}» non ammesso "
                          f"({', '.join(CANALI_FILONE)}, o vuoto)")
    if "stati" in dati and set(dati["stati"] or {}) != set(STATI):
        errori.append("«stati» del registro diversi da STATI dello script "
                      f"({', '.join(STATI)}): uno stato nuovo si aggiunge in tutti e due")
    for i, s in enumerate(dati.get("servizio") or []):
        if not (isinstance(s, dict) and s.get("cartella") and s.get("perche")):
            errori.append(f"servizio {i}: serve {{\"cartella\", \"perche\"}}")
    return errori


# --- i canali della piattaforma (ADR-0099) -----------------------------------

def _celle(riga: str) -> "list[str]":
    """Le celle di una riga di tabella: un «|» dentro il codice o scritto «\\|» non spezza."""
    celle, cur, codice, i = [], "", False, 0
    corpo = riga.strip()
    corpo = corpo[1:] if corpo.startswith("|") else corpo
    while i < len(corpo):
        c = corpo[i]
        if c == "\\" and i + 1 < len(corpo) and corpo[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if c == "`":
            codice = not codice
        if c == "|" and not codice:
            celle.append(cur.strip())
            cur = ""
        else:
            cur += c
        i += 1
    if cur.strip():
        celle.append(cur.strip())
    return celle


def _canale(cella: str) -> str:
    m = _CANALE_RE.match(cella.replace("*", ""))
    return m.group(1).lower().replace(" ", "-") if m else "altro"


def canali_piattaforma(piano: "Path | None" = None) -> "list[dict] | None":
    """Il canale di ogni componente, dalle tabelle di §2 di PIANO-PIATTAFORMA-DI-SVILUPPO.

    È l'UNICA lettura della fonte: oggi tabelle scritte a mano; quando il lotto P1
    del piano porta il canale in `binari.py`, si sostituisce questa funzione con
    `binari.py --canali` e il resto non cambia. Offline e deterministica.
    Il canale è la prima parola dell'ultima colonna («stable in HTML, testing in
    PDF» conta stable); ciò che non comincia con un canale è «altro».
    None se il piano non c'è.
    """
    p = piano or PIANO_PIATTAFORMA
    try:
        righe = p.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    fuori, dentro, sezione, intestazione = [], False, "", False
    for n, riga in enumerate(righe, 1):
        if riga.startswith("## "):
            dentro = riga.startswith("## §2")
            continue
        if not dentro:
            continue
        if riga.startswith("### "):
            sezione, intestazione = riga[4:].strip(), True
            continue
        if not riga.lstrip().startswith("|"):
            intestazione = True
            continue
        if intestazione:                       # la riga dei nomi delle colonne
            intestazione = False
            continue
        celle = _celle(riga)
        if len(celle) < 2 or re.fullmatch(r"[-: ]+", celle[0] or "-"):
            continue
        ultima = celle[-1]
        m = _DAL_RE.search(ultima)
        fuori.append({"componente": celle[0], "sezione": sezione, "canale": _canale(ultima),
                      "dal": m.group(1) if m else None,
                      "stato": " ".join(ultima.replace("**", "").split()), "riga": n})
    return fuori


def riassunto_canali(righe: "list[dict] | None") -> "dict | None":
    if righe is None:
        return None
    conteggio = {c: 0 for c in CANALI}
    for r in righe:
        conteggio[r["canale"]] += 1
    return {"fonte": PIANO_PIATTAFORMA.relative_to(RADICE).as_posix(), "conteggio": conteggio,
            "righe": righe}


# --- le PR --------------------------------------------------------------------

def _dt(s: "str | None") -> "datetime | None":
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def normalizza_pr(lista: list) -> "list[dict]":
    """Le PR nel formato REST di /pulls o in quello di `gh pr list --json`."""
    fuori = []
    for p in lista:
        if "headRefName" in p:                                   # gh
            ramo, bozza, agg, url = p["headRefName"], p.get("isDraft"), p.get("updatedAt"), p.get("url")
        else:                                                    # REST
            ramo = (p.get("head") or {}).get("ref", "")
            bozza, agg, url = p.get("draft"), p.get("updated_at"), p.get("html_url")
        corpo = p.get("body") or ""
        m = THREAD_RE.search(corpo)
        fuori.append({"numero": int(p["number"]), "titolo": p.get("title") or "",
                      "ramo": ramo, "bozza": bool(bozza), "aggiornata": agg,
                      "url": url or "", "thread_id": m.group(1) if m else None})
    return sorted(fuori, key=lambda x: -x["numero"])


def owner_repo_da_url(url: str) -> "tuple[str, str] | None":
    url = url.strip()
    m = re.match(r"^[\w.-]+@[\w.-]+:(.+)$", url)                # git@github.com:o/r.git
    percorso = m.group(1) if m else re.sub(r"^\w+://[^/]+/", "", url)
    parti = [x for x in percorso.split("/") if x]
    if len(parti) < 2:
        return None
    return parti[-2], re.sub(r"\.git$", "", parti[-1])


def pr_dalla_rete(owner: str, repo: str, timeout: float = 20) -> "tuple[list | None, str | None]":
    """(PR aperte, None) oppure (None, errore). Il repo è pubblico: il token è facoltativo."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    tutte: list = []
    for pagina in range(1, 11):
        url = (f"https://api.github.com/repos/{owner}/{repo}/pulls"
               f"?state=open&per_page=100&page={pagina}")
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json", "User-Agent": "lavoro-in-corso"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                blocco = json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError) as exc:
            return None, f"{type(exc).__name__}: {exc}"
        tutte.extend(blocco)
        if len(blocco) < 100:
            break
    return tutte, None


# --- rami e cartelle ----------------------------------------------------------

def _git(radice: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=radice, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def fetch(radice: Path) -> None:
    _git(radice, "fetch", "--quiet", "origin", "+refs/heads/*:refs/remotes/origin/*")


def rami_remoti(radice: Path) -> "list[dict]":
    """I rami di origin, senza `origin/`, con la data dell'ultimo commit."""
    try:
        righe = _git(radice, "for-each-ref", "--format=%(refname:short)\t%(committerdate:iso-strict)",
                     "refs/remotes/origin").splitlines()
    except RuntimeError:
        return []
    fuori = []
    for riga in righe:
        nome, _, quando = riga.partition("\t")
        if not nome.startswith("origin/") or nome == "origin/HEAD" or nome == "origin":
            continue
        fuori.append({"nome": nome[len("origin/"):], "data": quando})
    return sorted(fuori, key=lambda x: x["nome"])


def _titolo(cartella: Path) -> str:
    """Il primo titolo Markdown di LEGGIMI.md o README.md: solo quella riga."""
    for nome in ("LEGGIMI.md", "README.md"):
        p = cartella / nome
        try:
            with p.open(encoding="utf-8", errors="replace") as fh:
                for _, riga in zip(range(40), fh):
                    if riga.startswith("#"):
                        return riga.lstrip("#").strip()
        except OSError:
            continue
    return ""


def _ultima_modifica(cartella: Path, tetto: int = 5000) -> float:
    """L'mtime più recente fra la cartella e ciò che contiene (solo stat, al più `tetto` voci)."""
    piu = cartella.stat().st_mtime
    visti = 0
    for base, dirs, files in os.walk(cartella):
        for n in dirs + files:
            visti += 1
            if visti > tetto:
                return piu
            try:
                piu = max(piu, os.lstat(os.path.join(base, n)).st_mtime)
            except OSError:
                pass
    return piu


def cartelle(mnt: "Path | None", giorni: int, ora: datetime) -> "list[dict] | None":
    """Le cartelle di primo livello toccate negli ultimi `giorni`; None se `mnt` non c'è."""
    if mnt is None or not mnt.is_dir():
        return None
    soglia = ora.timestamp() - giorni * 86400
    fuori = []
    for d in sorted(mnt.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        quando = _ultima_modifica(d)
        if quando < soglia:
            continue
        fuori.append({"nome": d.name, "titolo": _titolo(d),
                      "modificata": datetime.fromtimestamp(quando, timezone.utc).strftime("%Y-%m-%d")})
    return fuori


# --- l'abbinamento ------------------------------------------------------------

def _giorni(da: "str | None", ora: datetime) -> "int | None":
    d = _dt(da)
    return None if d is None else (ora - d).days


def rapporto(registro: dict, prs_grezze: "list | None", pr_errore: "str | None",
             rami: "list[dict]", cart: "list[dict] | None", contenuti: dict,
             ora: datetime, giorni: int = GIORNI, canali: "list[dict] | None" = None) -> dict:
    filoni = registro.get("filoni", [])
    servizio = {s["cartella"] for s in registro.get("servizio", []) if isinstance(s, dict)}
    prs = normalizza_pr(prs_grezze) if prs_grezze is not None else None
    for p in prs or []:
        p["giorni"] = _giorni(p["aggiornata"], ora)

    usate: set = set()
    voci = []
    for f in filoni:
        aperte = []
        for p in prs or []:
            per_numero = p["numero"] in (f.get("pr") or [])
            per_ramo = p["ramo"] in (f.get("rami") or [])
            per_thread = bool(f.get("thread_id")) and p["thread_id"] == f.get("thread_id")
            if per_numero or per_ramo or per_thread:
                aperte.append(dict(p, via_thread=per_thread and not per_numero and not per_ramo))
                usate.add(p["numero"])
        voci.append({**f, "pr_aperte": aperte})

    aperti = {p["numero"] for p in prs or []}
    teste = {p["ramo"] for p in prs or []}
    pr_chiuse = []
    if prs is not None:
        pr_chiuse = [{"filone": f["id"], "pr": n} for f in filoni
                     for n in f.get("pr") or [] if n not in aperti]
    pr_ferme = [{"numero": p["numero"], "titolo": p["titolo"], "giorni": p["giorni"]}
                for p in prs or [] if p["giorni"] is not None and p["giorni"] > FERMA]
    filoni_vecchi = []
    for f in filoni:
        d = _data_iso(f.get("aggiornato"))
        if d and (ora.date() - d).days > giorni:
            filoni_vecchi.append({"filone": f["id"], "aggiornato": f["aggiornato"],
                                  "giorni": (ora.date() - d).days})

    nel_registro = {r for f in filoni for r in f.get("rami") or []}
    modelli = []
    for v in contenuti.get("rami", []):
        modelli.extend(v["ref"] if isinstance(v.get("ref"), list) else [v.get("ref", "")])

    def ha_posto(nome: str) -> bool:
        return (nome in teste or nome in nel_registro
                or any(fnmatch.fnmatchcase(f"origin/{nome}", m) or fnmatch.fnmatchcase(nome, m)
                       for m in modelli if m))

    rami_sciolti = []
    for r in rami:
        g = _giorni(r["data"], ora)
        if r["nome"].startswith("claude/") and g is not None and g <= giorni and not ha_posto(r["nome"]):
            rami_sciolti.append({"nome": r["nome"], "giorni": g})

    mnt_registro = {Path(m).parts[0] for f in filoni for m in f.get("mnt") or [] if m}
    cartelle_sciolte = [c for c in cart or [] if c["nome"] not in mnt_registro
                        and c["nome"] not in servizio]

    return {
        "ora": ora.strftime("%Y-%m-%d %H:%M UTC"),
        "giorni": giorni,
        "filoni": voci,
        "pr": prs,
        "pr_errore": pr_errore,
        "rami": len(rami),
        "cartelle": cart,
        "senza_filone": {
            "pr": [p for p in prs or [] if p["numero"] not in usate],
            "rami": rami_sciolti,
            "cartelle": cartelle_sciolte,
        },
        "da_aggiornare": {"pr_chiuse": pr_chiuse, "pr_ferme": pr_ferme,
                          "filoni_vecchi": filoni_vecchi},
        "canali": riassunto_canali(canali),
    }


# --- la pagina ----------------------------------------------------------------

def _cella(s: str, n: int = TAGLIO) -> str:
    s = " ".join(str(s).split()).replace("|", "\\|")
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def _codici(voci: "list[str]") -> str:
    return "<br>".join(f"`{v}`" for v in voci) or "—"


def _pr_cella(p: dict) -> str:
    stato = "bozza" if p["bozza"] else "pronta"
    g = p.get("giorni")
    g = "?" if g is None else ("oggi" if g == 0 else f"{g} g fa")
    via = " (dal thread)" if p.get("via_thread") else ""
    return f"[#{p['numero']}]({p['url']}) {stato}, {g}{via}" if p["url"] else f"#{p['numero']} {stato}, {g}{via}"


def _sezione_canali(c: "dict | None") -> "list[str]":
    out = ["## Canali della piattaforma (ADR-0099)", ""]
    if c is None:
        return out + ["Non letti: il piano della piattaforma non c'è in questo clone.", ""]
    nome = Path(c["fonte"]).name
    out += [f"Il canale di ogni componente viene da `{c['fonte']}` §2: per ora la fonte è",
            "scritta a mano, finché il lotto P1 del piano non porta il canale in",
            "`binari.py`. unstable, poi testing (versione fissata, CI non bloccante,",
            "misura prima e dopo), poi stable dopo 14 giorni e 10 run su `main` con",
            "l'ok del DM.", "",
            " · ".join(f"{k} **{v}**" for k, v in c["conteggio"].items()), ""]
    vivi = [x for x in c["righe"] if x["canale"] in ("testing", "unstable")]
    if vivi:
        out += ["| Componente | Canale | Dal | Che cosa dice il piano | Riga |", "|---|---|---|---|---|"]
        for x in sorted(vivi, key=lambda x: (CANALI.index(x["canale"]), x["riga"])):
            out.append(f"| {_cella(x['componente'], 90)} | `{x['canale']}` | {x['dal'] or '—'} | "
                       f"{_cella(x['stato'], 140)} | [{x['riga']}]({nome}#L{x['riga']}) |")
        out.append("")
    out += [f"Gli stable sono {c['conteggio']['stable']} e stanno nel piano, con le loro misure.", ""]
    return out


def pagina(r: dict) -> str:
    out = [
        "<!-- generata da scripts/lavoro_in_corso.py: non si scrive a mano.",
        "     Fonte curata: plans/lavoro-in-corso.json. Rigenera: python3 scripts/lavoro_in_corso.py -->",
        "",
        "# Lavoro in corso",
        "",
        f"Istantanea del {r['ora']}, generata da `scripts/lavoro_in_corso.py`: non si",
        "scrive a mano. Si corregge il registro `plans/lavoro-in-corso.json`, poi si",
        "rigenera con `python3 scripts/lavoro_in_corso.py` (`--fetch` per aggiornare",
        "prima i rami, `--offline` senza rete). Dipende da rete, clone e macchina: è",
        "una fotografia, non un cancello. Ciò che è già su `main` sta in `MEMORIA.md`.",
        "",
    ]
    if r["pr"] is None:
        out += [f"> ⚠ PR non lette: {r['pr_errore']}. Le colonne delle PR sono vuote.", ""]
    if r["cartelle"] is None:
        out += ["> ○ La cartella condivisa dei thread non c'è su questa macchina (es. il PC",
                "> del DM): le cartelle elencate vengono dal registro, non da una misura.", ""]

    out += ["## Filoni", "",
            "| Filone | Stato | Canale | PR | Rami | Cartelle condivise | Thread | Aspetta | Prossimo |",
            "|---|---|---|---|---|---|---|---|---|"]
    for f in r["filoni"]:
        if r["pr"] is None:
            prc = ", ".join(f"#{n}" for n in f.get("pr") or []) or "—"
        else:
            prc = "<br>".join(_pr_cella(p) for p in f["pr_aperte"]) or "—"
        out.append("| " + " | ".join([
            f"**{_cella(f['titolo'])}**<br>`{f['id']}`",
            f"`{f['stato']}`",
            f"`{f['canale']}`" if f.get("canale") else "—",
            prc,
            _codici(f.get("rami") or []),
            _codici(f.get("mnt") or []),
            _cella(f.get("thread") or "—"),
            _cella(f.get("aspetta") or "—"),
            _cella(f.get("prossimo") or "—"),
        ]) + " |")
    out += ["", "Stati: " + " · ".join(f"`{k}` {v}" for k, v in STATI.items()) + ".", ""]

    s = r["senza_filone"]
    out += ["## Senza filone", "",
            "Ciò che si muove e il registro non nomina: o entra in un filone, o si chiude.", ""]
    out += ["### PR aperte", ""]
    if r["pr"] is None:
        out += [f"Non misurate: {r['pr_errore']}.", ""]
    elif s["pr"]:
        out += ["| PR | Titolo | Ramo |", "|---|---|---|"]
        out += [f"| {_pr_cella(p)} | {_cella(p['titolo'])} | `{p['ramo']}` |" for p in s["pr"]]
        out.append("")
    else:
        out += ["Nessuna.", ""]
    out += [f"### Rami `claude/*` con commit negli ultimi {r['giorni']} giorni, senza PR aperta né posto", ""]
    if s["rami"]:
        out += [f"- `{x['nome']}`: ultimo commit {x['giorni']} giorni fa" for x in s["rami"]]
        out.append("")
    else:
        out += ["Nessuno." if r["rami"] else "Il clone non conosce rami di origin (`--fetch`).", ""]
    out += [f"### Cartelle condivise toccate negli ultimi {r['giorni']} giorni", ""]
    if r["cartelle"] is None:
        out += ["Non misurate: la cartella non c'è su questa macchina.", ""]
    elif s["cartelle"]:
        out += ["| Cartella | Toccata | Titolo del LEGGIMI |", "|---|---|---|"]
        out += [f"| `{c['nome']}` | {c['modificata']} | {_cella(c['titolo']) or '—'} |"
                for c in s["cartelle"]]
        out.append("")
    else:
        out += ["Nessuna.", ""]

    d = r["da_aggiornare"]
    out += ["## Da aggiornare o ferme", ""]
    righe = [f"- `{x['filone']}`: la PR #{x['pr']} non è più aperta, il filone va aggiornato"
             for x in d["pr_chiuse"]]
    righe += [f"- PR #{x['numero']} ferma da {x['giorni']} giorni (oltre {FERMA}): "
              f"{_cella(x['titolo'], 90)}" for x in d["pr_ferme"]]
    righe += [f"- `{x['filone']}`: aggiornato il {x['aggiornato']}, {x['giorni']} giorni fa"
              for x in d["filoni_vecchi"]]
    out += (righe or ["Niente."]) + [""]

    out += _sezione_canali(r.get("canali"))

    out += ["## Dove guardare", "",
            "- `MEMORIA.md`: ciò che è già su `main`, decisioni aperte e lista viva dei piani.",
            "- `plans/contenuti-nei-rami.json` e `python3 scripts/contenuti_nei_rami.py --fetch`:",
            "  i file che stanno in un ramo e mai su `main`.",
            "- I thread cloud: claude.ai/code. Le cartelle `mnt` della tabella stanno in",
            "  `/mnt/project-files` sulla macchina dei thread, non sul PC del DM.",
            "- Le sessioni locali di Claude Code: `claude --resume`. OpenCode tiene le sue",
            "  sessioni per conto suo (`opencode`, elenco delle sessioni).",
            ""]
    return "\n".join(out)


# --- main ---------------------------------------------------------------------

def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="valida solo il registro, offline; esce 1 sugli errori")
    ap.add_argument("--pr-json", type=Path, metavar="FILE",
                    help="PR aperte da file (REST /pulls o gh pr list --json) invece della rete")
    ap.add_argument("--offline", action="store_true", help="niente rete: le PR non si leggono")
    ap.add_argument("--fetch", action="store_true", help="prima scarica i rami di origin")
    ap.add_argument("--mnt", type=Path, default=None,
                    help=f"la cartella condivisa dei thread (default {MNT} se esiste)")
    ap.add_argument("--giorni", type=int, default=GIORNI,
                    help=f"finestra di rami e cartelle, età massima di un filone (default {GIORNI})")
    ap.add_argument("--stdout", action="store_true", help="la pagina a video, senza scrivere")
    ap.add_argument("--json", action="store_true", help="il rapporto in JSON, senza scrivere")
    ap.add_argument("--uscita", type=Path, default=USCITA, help=argparse.SUPPRESS)
    ap.add_argument("--registro", type=Path, default=REGISTRO, help=argparse.SUPPRESS)
    ap.add_argument("--contenuti", type=Path, default=CONTENUTI, help=argparse.SUPPRESS)
    ap.add_argument("--radice", type=Path, default=RADICE, help=argparse.SUPPRESS)
    ap.add_argument("--piano", type=Path, default=PIANO_PIATTAFORMA, help=argparse.SUPPRESS)
    ap.add_argument("--ora", default=None, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    try:
        registro = leggi_registro(args.registro)
    except (OSError, ValueError) as exc:
        print(f"✗ lavoro_in_corso: registro illeggibile: {exc}", file=sys.stderr)
        return 1
    errori = valida(registro, args.radice)
    if errori:
        print("✗ lavoro_in_corso: registro malformato:\n  · " + "\n  · ".join(errori),
              file=sys.stderr)
        return 1
    if args.check:
        print(f"✓ lavoro_in_corso: registro valido, {len(registro['filoni'])} filoni")
        return 0

    ora = _dt(args.ora) if args.ora else datetime.now(timezone.utc).replace(second=0, microsecond=0)
    if args.fetch:
        try:
            fetch(args.radice)
        except RuntimeError as exc:
            print(f"○ lavoro_in_corso: fetch non riuscito ({exc}); misuro i rami che ci sono",
                  file=sys.stderr)

    prs, errore = None, None
    if args.pr_json:
        try:
            prs = json.loads(args.pr_json.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errore = f"--pr-json illeggibile: {exc}"
    elif args.offline:
        errore = "modo --offline"
    else:
        try:
            coppia = owner_repo_da_url(_git(args.radice, "remote", "get-url", "origin"))
        except RuntimeError as exc:
            coppia, errore = None, f"nessun remote origin ({exc})"
        if coppia:
            prs, errore = pr_dalla_rete(*coppia)
        elif errore is None:
            errore = "l'URL di origin non dice owner e repo"

    mnt = args.mnt if args.mnt is not None else (MNT if MNT.is_dir() else None)
    r = rapporto(registro, prs, errore, rami_remoti(args.radice),
                 cartelle(mnt, args.giorni, ora), leggi_contenuti(args.contenuti),
                 ora, args.giorni, canali=canali_piattaforma(args.piano))

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    testo = pagina(r)
    if args.stdout:
        print(testo, end="")
        return 0
    args.uscita.write_text(testo, encoding="utf-8")
    s, d = r["senza_filone"], r["da_aggiornare"]
    npr = "?" if r["pr"] is None else len(s["pr"])
    ncart = "?" if r["cartelle"] is None else len(s["cartelle"])
    print(f"✓ lavoro_in_corso: {args.uscita.name} · {len(r['filoni'])} filoni · senza filone: "
          f"{npr} PR, {len(s['rami'])} rami, {ncart} cartelle · da aggiornare: "
          f"{len(d['pr_chiuse']) + len(d['pr_ferme']) + len(d['filoni_vecchi'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
