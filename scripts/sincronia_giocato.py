#!/usr/bin/env python3
"""sincronia_giocato.py — il giocato è arrivato sul ramo di gruppo, e main ci è entrato?

Il 2026-11-21 si è scoperto che `campaign-group-rumblingstone` era fermo al
12/10, 1.387 commit dietro `main`, con quattro patch del giocato ferme dal
05/11, e nessuno se n'era accorto. Questo script è l'occhio che mancava: misura,
non scrive niente (nessun checkout, nessun commit, nessun indice toccato).

Cinque regole, ogni rilievo con codice, livello, ramo e il comando che lo risolve:

- **S1** registro dei rami (`plans/rami-di-gruppo.json`): un ramo
  `campaign-group-*` sul remoto che non è né vivo né morto → 🟡.
- **S2** main indietro: per ogni ramo vivo, quanti commit di main mancano e da
  quanti giorni aspetta il più vecchio. 🔴 oltre `--giorni-rosso` (14: il
  Playbook e ADR-0090 vogliono main dentro prima di ogni preparazione), 🟡 se
  manca anche un solo commit. Clone shallow o storie senza antenato comune →
  ⚪ non misurabile (exit 2), mai un numero sbagliato.
- **S3** patch del giocato ferme nelle cartelle `--scansiona` (fino a
  profondità 3): solo quelle che toccano il canone vivo, cioè i file di partita
  di `dmcore/partita.py` (una lista, un posto). Ognuna si prova contro l'albero
  del ramo con un indice temporaneo: `applicata`, `da applicare` (🔴 se più
  vecchia di `--ore-patch`, 48; 🟡 se più giovane), `in conflitto` (🟡), oppure
  `applicata in altra forma` quando l'oggetto del commit è già nella storia del
  ramo (portata a mano, ritoccata o con un file rinominato).
- **S4** campi aperti al DM sul ramo (`______`, «da compilare», `[INFERRED`)
  in `campaign/sessions/` e `campaign/state.yaml`: domande per il DM, sempre 🟡,
  mai 🔴. Nessuno li riempie al posto suo.
- **S5** ultima sessione registrata sul ramo contro le serate delle patch non
  ancora applicate: una serata più recente dell'ultima registrata → 🔴.

Esito: 1 se c'è almeno un 🔴; altrimenti 2 se qualcosa non è misurabile;
altrimenti 0. `--avviso` (per l'hook) stampa poche righe solo se c'è del
rosso o del giallo ed esce sempre 0.

    python3 scripts/sincronia_giocato.py --check
    python3 scripts/sincronia_giocato.py --aggiorna --check --scansiona /mnt/project-files
    python3 scripts/sincronia_giocato.py --json
    python3 scripts/sincronia_giocato.py --avviso
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.partita import PARTITA  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / "plans" / "rami-di-gruppo.json"

ROSSO, GIALLO, NON_MISURABILE = "🔴", "🟡", "⚪"
GIORNI_ROSSO = 14
ORE_PATCH = 48
PROFONDITA = 3
RIGHE_AVVISO = 4
TEMPO_SCANSIONE = 3.0  # secondi: una cartella di rete lenta non ferma l'hook
ESTENSIONI_PATCH = (".patch", ".mbox", ".diff")
CAMPI_APERTI = r"_{6,}|[Dd]a compilare|\[INFERRED"
_SESSIONE = re.compile(r"campaign/sessions/(\d{4}-\d{2}-\d{2})_session-\d+\.md$")
_DIFF = re.compile(r"^diff --git a/(.+?) b/(.+)$", re.M)
_OGGETTO = re.compile(r"^Subject: (?:\[PATCH[^\]]*\] ?)?(.*(?:\n[ \t].*)*)", re.M)


def _prefissi_canone() -> "tuple[str, ...]":
    """I file di partita di `dmcore/partita.py`: un percorso o il prefisso prima del glob."""
    out = []
    for v in PARTITA:
        p = v.percorso
        out.append(p.split("*", 1)[0] if "*" in p else p)
    return tuple(out)


CANONE = _prefissi_canone()


def e_canone(rel: str) -> bool:
    return any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in CANONE)


# ---------------------------------------------------------------- git

def _git(repo: Path, *args: str, env: "dict | None" = None, timeout: float = 30,
         check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env=env, timeout=timeout, check=check)


def _out(repo: Path, *args: str) -> str:
    return _git(repo, *args).stdout.strip()


def _esiste(repo: Path, ref: str) -> bool:
    return _git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}",
                check=False).returncode == 0


def _ref(repo: Path, remoto: str, ramo: str) -> "str | None":
    for r in (f"refs/remotes/{remoto}/{ramo}", f"refs/heads/{ramo}"):
        if _esiste(repo, r):
            return r
    return None


def rami_di_gruppo(repo: Path, remoto: str) -> "list[str]":
    righe = _out(repo, "for-each-ref", "--format=%(refname)",
                 f"refs/remotes/{remoto}/campaign-group-*", "refs/heads/campaign-group-*")
    nomi = {r.rsplit("/", 1)[-1] if r.startswith("refs/heads/") else r.split("/", 3)[3]
            for r in righe.splitlines() if r}
    return sorted(nomi)


def carica_registro(path: Path) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"vivi": d.get("vivi", []), "morti": d.get("morti", [])}


def _rilievo(codice: str, livello: str, ramo: str, messaggio: str, comando: str,
             **dati) -> dict:
    return {"codice": codice, "livello": livello, "ramo": ramo, "messaggio": messaggio,
            "comando": comando, "dati": dati}


# ---------------------------------------------------------------- regole

def s1(presenti: "list[str]", registro: dict) -> "list[dict]":
    noti = {r["ramo"] for r in registro["vivi"]} | {r["ramo"] for r in registro["morti"]}
    return [_rilievo("S1", GIALLO, n, "ramo di gruppo non registrato",
                     f"aggiungilo a plans/rami-di-gruppo.json fra i vivi o fra i morti (con data e motivo)")
            for n in presenti if n not in noti]


def s2(repo: Path, ramo: str, ref: str, main: str, t_ora: int, giorni_rosso: int,
       shallow: bool) -> "tuple[list[dict], dict]":
    unshallow = "git fetch --unshallow origin (o un clone completo, fetch-depth: 0 in CI)"
    if shallow:
        return [_rilievo("S2", NON_MISURABILE, ramo, "clone shallow: i commit di main che "
                         "mancano non si possono contare", unshallow)], {}
    if _git(repo, "merge-base", ref, main, check=False).returncode != 0:
        return [_rilievo("S2", NON_MISURABILE, ramo, f"{ramo} e main non hanno un antenato "
                         "comune (storie separate o clone incompleto)", unshallow)], {}
    tempi = [int(x) for x in _out(repo, "log", "--format=%ct", f"{ref}..{main}").split()]
    misure = {"main_mancanti": len(tempi)}
    if not tempi:
        return [], misure
    giorni = int((t_ora - min(tempi)) // 86400)
    misure["giorni"] = giorni
    livello = ROSSO if giorni > giorni_rosso else GIALLO
    return [_rilievo("S2", livello, ramo, f"mancano {len(tempi)} commit di main, il più "
                     f"vecchio aspetta da {giorni} giorni (soglia {giorni_rosso})",
                     f"git checkout {ramo} && git merge origin/main (mai rebase, mai push forzato)",
                     commit=len(tempi), giorni=giorni)], misure


def trova_patch(cartelle: "list[Path]", scadenza: float) -> "tuple[list[Path], bool]":
    """I file di patch fino a PROFONDITA livelli; si ferma alla scadenza (completa=False)."""
    trovate: "list[Path]" = []
    for base in cartelle:
        base = Path(base)
        if not base.is_dir():
            continue
        coda = [(base, 0)]
        while coda:
            if time.monotonic() > scadenza:
                return sorted(trovate), False
            d, liv = coda.pop()
            try:
                voci = list(os.scandir(d))
            except OSError:
                continue
            for v in voci:
                try:
                    if v.is_dir(follow_symlinks=False):
                        if liv + 1 < PROFONDITA and not v.name.startswith("."):
                            coda.append((Path(v.path), liv + 1))
                    elif v.name.endswith(ESTENSIONI_PATCH):
                        trovate.append(Path(v.path))
                except OSError:
                    continue
    return sorted(trovate), True


def file_della_patch(testo: str) -> "list[str]":
    out = []
    for a, b in _DIFF.findall(testo):
        for p in (a, b):
            if p not in out:
                out.append(p)
    return out


def oggetti(testo: str) -> "list[str]":
    """Gli oggetti dei commit di un mbox di format-patch, con le righe ripiegate riunite."""
    return [" ".join(o.split()) for o in _OGGETTO.findall(testo)]


def oggetti_del_ramo(repo: Path, ref: str) -> "set[str]":
    return {" ".join(r.split()) for r in _out(repo, "log", "--format=%s", ref).splitlines()}


def classifica(repo: Path, ref: str, patch: Path) -> "tuple[str, str]":
    """applicata | da applicare | in conflitto, contro l'albero di `ref` e senza checkout."""
    with tempfile.TemporaryDirectory() as t:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(t) / "indice"))
        _git(repo, "read-tree", ref, env=env)
        if _git(repo, "apply", "--cached", "--check", "-R", str(patch), env=env,
                check=False).returncode == 0:
            return "applicata", ""
        avanti = _git(repo, "apply", "--cached", "--check", str(patch), env=env, check=False)
        if avanti.returncode == 0:
            return "da applicare", ""
        motivo = next((r for r in avanti.stderr.splitlines() if r.startswith("error:")),
                      avanti.stderr.strip()[:200])
        return "in conflitto", motivo


def s3(repo: Path, ramo: str, ref: str, patch: "list[Path]", t_ora: int,
       ore_patch: float) -> "tuple[list[dict], list[dict], int]":
    rilievi, voci, fuori = [], [], 0
    gia: "set[str] | None" = None
    for f in patch:
        try:
            testo = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        toccati = file_della_patch(testo)
        if not toccati or not any(e_canone(p) for p in toccati):
            fuori += 1
            continue
        stato, motivo = classifica(repo, ref, f)
        if stato != "applicata":
            # portata a mano, con ritocchi o con un altro nome di file (la sessione 5 del
            # 2026-11-20 rinumerata 7): lo stesso oggetto di commit è già nella storia del ramo
            gia = oggetti_del_ramo(repo, ref) if gia is None else gia
            ogg = oggetti(testo)
            if ogg and all(o in gia for o in ogg):
                stato, motivo = "applicata in altra forma", ""
        ore = (t_ora - f.stat().st_mtime) / 3600
        serate = sorted({m.group(1) for p in toccati if (m := _SESSIONE.search(p))})
        voci.append({"file": str(f), "ramo": ramo, "stato": stato, "ore": round(ore, 1), "file_toccati": toccati,
                     "serate": serate, **({"motivo": motivo} if motivo else {})})
        if stato == "da applicare":
            livello = ROSSO if ore > ore_patch else GIALLO
            rilievi.append(_rilievo("S3", livello, ramo, f"patch del giocato ferma da {int(ore)} "
                                    f"ore: {f.name}", f"git checkout {ramo} && git am {f} "
                                    "(o git apply), poi validate_state e render_state --check",
                                    file=str(f), ore=round(ore, 1)))
        elif stato == "in conflitto":
            rilievi.append(_rilievo("S3", GIALLO, ramo, f"patch in conflitto con il ramo: "
                                    f"{f.name} ({motivo})", f"git checkout {ramo} && git apply "
                                    f"--3way {f}, e i conflitti si decidono con il DM",
                                    file=str(f), motivo=motivo))
    return rilievi, voci, fuori


def s4(repo: Path, ramo: str, ref: str) -> "list[dict]":
    r = _git(repo, "grep", "-c", "-E", CAMPI_APERTI, ref, "--", "campaign/sessions",
             "campaign/state.yaml", check=False)
    per_file = {}
    for riga in r.stdout.splitlines():
        nome, _, n = riga.rpartition(":")
        per_file[nome.split(":", 1)[1] if ":" in nome else nome] = int(n)
    totale = sum(per_file.values())
    if not totale:
        return []
    primi = sorted(per_file.items(), key=lambda kv: -kv[1])[:3]
    return [_rilievo("S4", GIALLO, ramo, f"{totale} campi aperti al DM (" +
                     ", ".join(f"{Path(k).name} {v}" for k, v in primi) + ")",
                     "domande per il DM tramite il coordinatore: non si riempiono al posto suo",
                     totale=totale, per_file=per_file)]


def ultima_sessione(repo: Path, ref: str) -> "str | None":
    nomi = _out(repo, "ls-tree", "--name-only", f"{ref}:campaign/sessions/") \
        if _git(repo, "cat-file", "-e", f"{ref}:campaign/sessions", check=False).returncode == 0 else ""
    date = [m.group(1) for n in nomi.splitlines() if (m := _SESSIONE.search("campaign/sessions/" + n))]
    return max(date) if date else None


def s5(ramo: str, ultima: "str | None", voci: "list[dict]") -> "list[dict]":
    serate = sorted({s for v in voci if v["stato"] != "applicata" for s in v["serate"]})
    nuove = [s for s in serate if ultima is None or s > ultima]
    if not nuove:
        return []
    return [_rilievo("S5", ROSSO, ramo, f"serata del {nuove[-1]} non registrata: l'ultima "
                     f"sessione sul ramo è del {ultima or 'nessuna'}",
                     "porta sul ramo la patch della serata (vedi S3) o chiudi la sessione con "
                     "python3 scripts/dm.py session end", serate=nuove, ultima=ultima)]


# ---------------------------------------------------------------- misura

def _t(ora: "str | None") -> int:
    if not ora:
        return int(time.time())
    return int(datetime.fromisoformat(ora.replace("Z", "+00:00")).astimezone(timezone.utc).timestamp())


def misura(repo: Path, registro: Path = REGISTRO, scansiona: "list[Path] | None" = None,
           remoto: str = "origin", giorni_rosso: int = GIORNI_ROSSO,
           ore_patch: float = ORE_PATCH, ora: "str | None" = None,
           campi_aperti: bool = True, tempo_scansione: float = TEMPO_SCANSIONE) -> dict:
    repo = Path(repo)
    t_ora = _t(ora)
    reg = carica_registro(registro)
    rilievi: "list[dict]" = []
    misure: dict = {"rami": {}, "patch": [], "patch_fuori_canone": 0}
    shallow = _out(repo, "rev-parse", "--is-shallow-repository") == "true"
    misure["shallow"] = shallow
    rilievi += s1(rami_di_gruppo(repo, remoto), reg)
    main = _ref(repo, remoto, "main")
    patch, completa = trova_patch(list(scansiona or []), time.monotonic() + tempo_scansione)
    misure["scansione_completa"] = completa
    if not completa:
        rilievi.append(_rilievo("S3", GIALLO, "-", "scansione delle patch interrotta per tempo: "
                                "il conto è parziale", "rilancia senza --avviso"))
    for voce in reg["vivi"]:
        ramo = voce["ramo"]
        ref = _ref(repo, remoto, ramo)
        if not ref:
            rilievi.append(_rilievo("S2", NON_MISURABILE, ramo, "ramo vivo assente in questo clone",
                                    f"git fetch {remoto} {ramo}"))
            continue
        m: dict = {"ref": ref, "sha": _out(repo, "rev-parse", "--short", ref)}
        if main:
            r2, m2 = s2(repo, ramo, ref, main, t_ora, giorni_rosso, shallow)
            rilievi += r2
            m.update(m2)
        else:
            rilievi.append(_rilievo("S2", NON_MISURABILE, ramo, "main assente in questo clone",
                                    f"git fetch {remoto} main"))
        r3, voci, fuori = s3(repo, ramo, ref, patch, t_ora, ore_patch)
        rilievi += r3
        misure["patch"] += voci
        misure["patch_fuori_canone"] = fuori
        if campi_aperti:
            rilievi += s4(repo, ramo, ref)
        m["ultima_sessione"] = ultima_sessione(repo, ref)
        rilievi += s5(ramo, m["ultima_sessione"], voci)
        misure["rami"][ramo] = m
    livelli = {r["livello"] for r in rilievi}
    esito = 1 if ROSSO in livelli else 2 if NON_MISURABILE in livelli else 0
    return {"esito": esito, "rilievi": rilievi, "misure": misure}


def aggiorna(repo: Path, registro: Path, remoto: str, timeout: float = 120) -> "str | None":
    """`git fetch` di main e dei rami vivi; ritorna l'errore, o None."""
    vivi = [r["ramo"] for r in carica_registro(registro)["vivi"]]
    try:
        r = _git(repo, "fetch", "-q", remoto, "main", *vivi, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return f"git fetch oltre {timeout:.0f} s"
    return None if r.returncode == 0 else (r.stderr.strip().splitlines() or ["fetch fallito"])[-1]


def testo(esito: dict) -> str:
    righe = []
    for r in esito["rilievi"]:
        righe.append(f"{r['livello']} {r['codice']} {r['ramo']}: {r['messaggio']}\n   → {r['comando']}")
    for ramo, m in esito["misure"]["rami"].items():
        righe.append(f"   {ramo} @ {m['sha']}: main mancanti {m.get('main_mancanti', '?')}, "
                     f"ultima sessione {m.get('ultima_sessione') or 'nessuna'}")
    p = esito["misure"]
    righe.append(f"   patch del canone {len(p['patch'])}, fuori canone {p['patch_fuori_canone']}")
    gialli = sum(r["livello"] == GIALLO for r in esito["rilievi"])
    righe.append({0: f"✓ sincronia_giocato: nessun rosso ({gialli} gialli)",
                  1: "✗ sincronia_giocato: rosso",
                  2: "⚪ sincronia_giocato: non misurabile"}[esito["esito"]])
    return "\n".join(righe)


def avviso(esito: dict) -> str:
    rilievi = sorted(esito["rilievi"], key=lambda r: [ROSSO, NON_MISURABILE, GIALLO].index(r["livello"]))
    if not rilievi:
        return ""
    righe = [f"{r['livello']} {r['codice']} {r['ramo']}: {r['messaggio']}" for r in rilievi[:RIGHE_AVVISO]]
    extra = len(rilievi) - RIGHE_AVVISO
    righe.append("sincronia del giocato (ADR-0090): " + (f"altri {extra} rilievi, " if extra > 0 else "")
                 + "dettagli con python3 scripts/sincronia_giocato.py --check")
    return "\n".join(righe)


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", type=Path, default=ROOT, help="il clone da misurare")
    ap.add_argument("--registro", type=Path, default=REGISTRO, help="registro dei rami di gruppo")
    ap.add_argument("--remoto", default="origin")
    ap.add_argument("--check", action="store_true", help="esce 1 con un 🔴, 2 se non misurabile")
    ap.add_argument("--json", action="store_true", help="l'esito in JSON")
    ap.add_argument("--avviso", action="store_true",
                    help="modalità hook: poche righe solo se c'è rosso o giallo, esce sempre 0")
    ap.add_argument("--aggiorna", action="store_true", help="git fetch di main e dei rami vivi prima")
    ap.add_argument("--scansiona", type=Path, action="append", default=[], metavar="DIR",
                    help=f"cartella dove cercare patch (fino a profondità {PROFONDITA}); ripetibile")
    ap.add_argument("--giorni-rosso", type=int, default=GIORNI_ROSSO,
                    help=f"S2: giorni di main fuori dal ramo oltre i quali è rosso (default {GIORNI_ROSSO})")
    ap.add_argument("--ore-patch", type=float, default=ORE_PATCH,
                    help=f"S3: ore oltre le quali una patch da applicare è rossa (default {ORE_PATCH})")
    ap.add_argument("--senza-campi-aperti", action="store_true", help="salta S4")
    ap.add_argument("--ora", help="istante della misura in ISO 8601 (per le prove)")
    a = ap.parse_args(argv)
    try:
        errore = aggiorna(a.repo, a.registro, a.remoto) if a.aggiorna else None
        esito = misura(a.repo, a.registro, a.scansiona, a.remoto, a.giorni_rosso, a.ore_patch,
                       a.ora, campi_aperti=not a.senza_campi_aperti,
                       tempo_scansione=TEMPO_SCANSIONE if a.avviso else 600)
        if errore:
            esito["rilievi"].insert(0, _rilievo("S0", GIALLO, "-", f"aggiornamento fallito: {errore}",
                                                f"git fetch {a.remoto} main"))
    except Exception as e:  # noqa: BLE001
        if a.avviso:
            return 0
        print(f"⚪ sincronia_giocato: non misurabile ({type(e).__name__}: {e})", file=sys.stderr)
        return 2
    if a.avviso:
        # nell'hook una scansione a metà usa le patch trovate e non fa rumore
        esito["rilievi"] = [r for r in esito["rilievi"] if not (r["codice"] == "S3" and r["ramo"] == "-")]
        msg = avviso(esito)
        if msg:
            print(msg)
        return 0
    print(json.dumps(esito, ensure_ascii=False, indent=2) if a.json else testo(esito))
    return esito["esito"] if a.check else 0


if __name__ == "__main__":
    sys.exit(main())
