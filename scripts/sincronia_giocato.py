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
  del ramo con un indice temporaneo, nell'ordine: si applica al contrario, o il
  suo `git patch-id --stable` è quello di un commit del ramo → `applicata`;
  l'oggetto del commit è nella storia del ramo e ogni riga aggiunta ai file di
  canone c'è ancora (o il file è cambiato dopo quel commit) → `applicata in
  altra forma`; con righe che mancano → `da verificare` (🟡, con il numero di
  righe, domanda al DM); si applica in avanti → `da applicare` (🔴 se più
  vecchia di `--ore-patch`, 48; 🟡 se più giovane); altrimenti `in conflitto` (🟡).
- **S4** campi aperti al DM sul ramo, in `campaign/sessions/` e
  `campaign/state.yaml`: `[INFERRED` (con i criteri di `inventory_inferred.py`),
  `______`, «da compilare», «da confermare», «da decidere», «da tirare», «non
  ancora tirati». Conta le occorrenze, non le righe, e salta le intestazioni.
  Sono domande per il DM: sempre 🟡, mai 🔴. Nessuno li riempie al posto suo.
- **S5** ultima sessione registrata sul ramo contro le serate delle patch non
  ancora applicate: una serata più recente dell'ultima registrata → 🔴.
- **S6** campi chiusi senza decisione del DM: una patch (o, con `--ref`, il
  diff fra il ramo remoto e REF) che fa scendere i campi aperti, dove una riga
  che chiude un campo non cita una decisione del DM con la data, per esempio
  «(DM, 2026-11-21)». Una patch → 🟡, domanda al DM; un REF da spingere → 🔴.
- **S7** (`--dopo-merge`) righe di main perse nel merge: ogni riga che main ha
  aggiunto ai file di partita dalla base comune deve esserci nel risultato.

Esito: 1 se c'è almeno un 🔴; altrimenti 2 se qualcosa non è misurabile;
altrimenti 0. `--avviso` (per l'hook) stampa poche righe solo se c'è del
rosso o del giallo ed esce sempre 0.

    python3 scripts/sincronia_giocato.py --check
    python3 scripts/sincronia_giocato.py --aggiorna --check --scansiona /mnt/project-files
    python3 scripts/sincronia_giocato.py --json
    python3 scripts/sincronia_giocato.py --avviso
    python3 scripts/sincronia_giocato.py --ref HEAD --check     # prima del push
    python3 scripts/sincronia_giocato.py --dopo-merge           # dopo git merge origin/main
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import difflib
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.partita import PARTITA  # noqa: E402
import inventory_inferred as inv  # noqa: E402  (i criteri dei [INFERRED]: una norma, un rilevatore)

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / "plans" / "rami-di-gruppo.json"

ROSSO, GIALLO, NON_MISURABILE = "🔴", "🟡", "⚪"
GIORNI_ROSSO = 14
ORE_PATCH = 48
PROFONDITA = 3
RIGHE_AVVISO = 4
TEMPO_SCANSIONE = 2.0  # secondi: una cartella di rete lenta non ferma l'hook
ESTENSIONI_PATCH = (".patch", ".mbox", ".diff")
_ALTRI_CAMPI = re.compile(r"_{6,}|\bda\s+(?:compilare|confermare|decidere|tirare)\b|"
                         r"\bnon\s+ancora\s+tirat\w*", re.I)
_INTESTAZIONE = re.compile(r"^\s*#{1,6}\s")
_DECISIONE_DM = re.compile(r"\b(?:DM|Jfs)\b[^\n]{0,60}?\d{4}-\d{2}-\d{2}|"
                           r"\d{4}-\d{2}-\d{2}[^\n]{0,20}?\b(?:DM|Jfs)\b")
FILE_S4 = ("campaign/sessions", "campaign/state.yaml")
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


def campi_riga(riga: str) -> int:
    """I campi aperti al DM in una riga; un'intestazione non ne ha."""
    if _INTESTAZIONE.match(riga):
        return 0
    n = 0
    for m in inv.MARCATORE.finditer(riga):
        nota = inv.NOTA.match(" ".join(m.group("coda").split()))
        if inv.cita_la_convenzione(riga[:m.start()]) or (
                nota and inv.SCHEMA.match(nota.group("testo").strip())):
            continue
        n += 1
    resto = inv.MARCATORE.sub(" ", riga)
    n += resto.count("[INFERRED")  # una marca che va a capo
    return n + len(_ALTRI_CAMPI.findall(resto))


def conta_campi(testo: str) -> int:
    return sum(campi_riga(r) for r in testo.splitlines())


_HUNK = re.compile(r"^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@")


def _blocchi_diff(testo: str):
    """(file, righe vecchie, righe nuove) per ogni hunk di un diff o di un mbox di format-patch.

    Le righe si contano con l'intestazione dell'hunk, così la firma «-- » e la patch
    successiva dell'mbox non entrano mai fra le righe tolte.
    """
    file_ = None
    righe = testo.splitlines()
    i = 0
    while i < len(righe):
        m = _DIFF.match(righe[i])
        if m:
            file_ = m.group(2)
        h = _HUNK.match(righe[i])
        if not (h and file_):
            i += 1
            continue
        resto_v = int(h.group(1) or 1)
        resto_n = int(h.group(2) or 1)
        vecchie, nuove = [], []
        i += 1
        while i < len(righe) and (resto_v > 0 or resto_n > 0):
            r = righe[i]
            if r.startswith("\\"):
                i += 1
                continue
            segno, corpo = (r[:1], r[1:]) if r else (" ", "")
            if segno == "-":
                vecchie.append(corpo)
                resto_v -= 1
            elif segno == "+":
                nuove.append(corpo)
                resto_n -= 1
            else:
                vecchie.append(corpo)
                nuove.append(corpo)
                resto_v -= 1
                resto_n -= 1
            i += 1
        yield file_, vecchie, nuove


def chiusure(testo: str) -> dict:
    """Quanti campi aperti chiude un diff e quante chiusure non citano una decisione datata del DM."""
    chiusi = senza = tolti = messi = 0
    per_file: "dict[str, int]" = {}
    for file_, vecchie, nuove in _blocchi_diff(testo):
        if not (file_.startswith(FILE_S4[0] + "/") or file_ == FILE_S4[1]):
            continue
        tolti += sum(campi_riga(r) for r in vecchie)
        messi += sum(campi_riga(r) for r in nuove)
        sm = difflib.SequenceMatcher(None, vecchie, nuove, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag not in ("replace", "delete"):
                continue
            prima = sum(campi_riga(r) for r in vecchie[i1:i2])
            dopo = sum(campi_riga(r) for r in nuove[j1:j2])
            if prima <= dopo:
                continue
            chiusi += prima - dopo
            nuove_righe = [r for r in nuove[j1:j2] if r.strip() and not campi_riga(r)]
            mancano = (min(prima - dopo, sum(1 for r in nuove_righe if not _DECISIONE_DM.search(r)))
                       if nuove_righe else prima - dopo)
            senza += mancano
            if mancano:
                per_file[file_] = per_file.get(file_, 0) + mancano
    # Un file spostato o rinumerato (la sessione 5 diventata 7) toglie i campi da una parte e
    # li rimette dall'altra: conta solo ciò che la patch fa scendere davvero, nel complesso.
    netto = max(0, tolti - messi)
    return {"chiusi": min(chiusi, netto), "senza_decisione": min(senza, netto),
            "per_file": per_file if netto else {}}


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


def rami_morti(registro: Path = REGISTRO) -> "set[str]":
    """I rami di gruppo che non si toccano (ADR-0090); vuoto se il registro manca."""
    try:
        return {r["ramo"] for r in carica_registro(registro)["morti"]}
    except (OSError, ValueError, KeyError):
        return set()


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


def _patch_id(repo: Path, testo: str) -> "set[str]":
    r = subprocess.run(["git", "-C", str(repo), "patch-id", "--stable"], input=testo,
                       capture_output=True, text=True, timeout=30)
    return {riga.split()[0] for riga in r.stdout.splitlines() if riga.strip()}


class Ramo:
    """Ciò che serve sapere della storia di un ramo, calcolato una volta sola."""

    def __init__(self, repo: Path, ref: str) -> None:
        self.repo, self.ref = repo, ref
        self._oggetti: "dict[str, str] | None" = None
        self._ids: "set[str] | None" = None

    @property
    def oggetti(self) -> "dict[str, str]":
        if self._oggetti is None:
            self._oggetti = {}
            for riga in reversed(_out(self.repo, "log", "--format=%H%x00%s", self.ref).splitlines()):
                sha, _, ogg = riga.partition("\0")
                self._oggetti[" ".join(ogg.split())] = sha  # vince il più recente
        return self._oggetti

    @property
    def patch_id(self) -> "set[str]":
        if self._ids is None:
            shas = _out(self.repo, "log", "--no-merges", "--format=%H", self.ref, "--",
                        *CANONE).split()
            testo = _out(self.repo, "show", "--format=commit %H", *shas) if shas else ""
            self._ids = _patch_id(self.repo, testo) if testo else set()
        return self._ids

    def contenuto(self, rel: str) -> "str | None":
        r = _git(self.repo, "show", f"{self.ref}:{rel}", check=False)
        return r.stdout if r.returncode == 0 else None

    def cambiato_dopo(self, sha: str, rel: str) -> bool:
        return bool(_out(self.repo, "log", "--format=%H", f"{sha}..{self.ref}", "--", rel))


def righe_aggiunte(testo: str) -> "dict[str, list[str]]":
    out: "dict[str, list[str]]" = {}
    for file_, vecchie, nuove in _blocchi_diff(testo):
        sm = difflib.SequenceMatcher(None, vecchie, nuove, autojunk=False)
        for tag, _i1, _i2, j1, j2 in sm.get_opcodes():
            if tag in ("replace", "insert"):
                out.setdefault(file_, []).extend(r for r in nuove[j1:j2] if r.strip())
    return out


def classifica(ramo: Ramo, patch: Path, testo: str) -> "tuple[str, str, int]":
    """(stato, motivo, righe di canone che mancano) contro l'albero del ramo, senza checkout."""
    repo, ref = ramo.repo, ramo.ref
    with tempfile.TemporaryDirectory() as t:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(t) / "indice"))
        _git(repo, "read-tree", ref, env=env)
        if _git(repo, "apply", "--cached", "--check", "-R", str(patch), env=env,
                check=False).returncode == 0:
            return "applicata", "", 0
        avanti = _git(repo, "apply", "--cached", "--check", str(patch), env=env, check=False)
    ids = _patch_id(repo, testo)
    if ids and ids <= ramo.patch_id:
        return "applicata", "", 0
    ogg = oggetti(testo)
    if ogg and all(o in ramo.oggetti for o in ogg):
        # portata a mano, ritoccata o con un file rinominato: si guarda riga per riga
        sha = ramo.oggetti[ogg[-1]]
        mancano = 0
        for rel, righe in righe_aggiunte(testo).items():
            if not e_canone(rel):
                continue
            attuale = ramo.contenuto(rel)
            presenti = {r.strip() for r in (attuale or "").splitlines()}
            perse = [r for r in righe if r.strip() not in presenti]
            if perse and not ramo.cambiato_dopo(sha, rel):
                mancano += len(perse)
        if not mancano:
            return "applicata in altra forma", "", 0
        return "da verificare", f"{mancano} righe di canone della patch non sono nel ramo", mancano
    if avanti.returncode == 0:
        return "da applicare", "", 0
    motivo = next((r for r in avanti.stderr.splitlines() if r.startswith("error:")),
                  avanti.stderr.strip()[:200])
    return "in conflitto", motivo, 0


def s3(repo: Path, ramo_nome: str, ref: str, patch: "list[Path]", t_ora: int,
       ore_patch: float) -> "tuple[list[dict], list[dict], int]":
    rilievi, voci, fuori = [], [], 0
    ramo = Ramo(repo, ref)
    for f in patch:
        try:
            testo = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        toccati = file_della_patch(testo)
        if not toccati or not any(e_canone(p) for p in toccati):
            fuori += 1
            continue
        stato, motivo, mancano = classifica(ramo, f, testo)
        ore = (t_ora - f.stat().st_mtime) / 3600
        serate = sorted({m.group(1) for p in toccati if (m := _SESSIONE.search(p))})
        ch = chiusure(testo)
        voci.append({"file": str(f), "ramo": ramo_nome, "stato": stato, "ore": round(ore, 1),
                     "file_toccati": toccati, "serate": serate, "campi_chiusi": ch["chiusi"],
                     **({"motivo": motivo} if motivo else {})})
        if stato == "da applicare":
            livello = ROSSO if ore > ore_patch else GIALLO
            rilievi.append(_rilievo("S3", livello, ramo_nome, f"patch del giocato ferma da {int(ore)} "
                                    f"ore: {f.name}", f"git checkout {ramo_nome} && git am {f} "
                                    "(o git apply), poi validate_state e render_state --check",
                                    file=str(f), ore=round(ore, 1)))
        elif stato == "in conflitto":
            rilievi.append(_rilievo("S3", GIALLO, ramo_nome, f"patch in conflitto con il ramo: "
                                    f"{f.name} ({motivo})", f"git checkout {ramo_nome} && git apply "
                                    f"--3way {f}, e i conflitti si decidono con il DM",
                                    file=str(f), motivo=motivo))
        elif stato == "da verificare":
            rilievi.append(_rilievo("S3", GIALLO, ramo_nome, f"patch con lo stesso oggetto di un commit "
                                    f"del ramo ma {mancano} righe di canone mancano: {f.name}",
                                    "da verificare con il DM tramite il coordinatore: quelle righe "
                                    "erano scelte sue?", file=str(f), righe_mancanti=mancano))
        if ch["senza_decisione"]:
            rilievi.append(_rilievo("S6", GIALLO, ramo_nome, f"chiude campi senza decisione del DM: "
                                    f"{ch['senza_decisione']} su {ch['chiusi']} in {f.name}",
                                    ("è già sul ramo: chiedi conferma al DM tramite il coordinatore"
                                     if stato.startswith("applicata") else "non portarla: domanda al DM "
                                     "tramite il coordinatore") + "; ogni campo chiuso cita «[CANONE — DM AAAA-MM-GG, codice]»",
                                    file=str(f), stato=stato, **ch))
    return rilievi, voci, fuori


def campi_aperti_di(repo: Path, ref: str) -> "dict[str, int]":
    nomi = _out(repo, "ls-tree", "-r", "--name-only", ref, "--", *FILE_S4).splitlines()
    per_file = {}
    for rel in nomi:
        r = _git(repo, "show", f"{ref}:{rel}", check=False)
        n = conta_campi(r.stdout) if r.returncode == 0 else 0
        if n:
            per_file[rel] = n
    return per_file


def s4(ramo: str, per_file: "dict[str, int]") -> "list[dict]":
    totale = sum(per_file.values())
    if not totale:
        return []
    primi = sorted(per_file.items(), key=lambda kv: -kv[1])[:3]
    return [_rilievo("S4", GIALLO, ramo, f"{totale} campi aperti al DM (" +
                     ", ".join(f"{Path(k).name} {v}" for k, v in primi) + ")",
                     "domande per il DM tramite il coordinatore: non si riempiono al posto suo",
                     totale=totale, per_file=per_file)]


def s6_ref(repo: Path, ramo: str, remoto_ref: str, ref: str) -> "list[dict]":
    """Il diff che REF porterebbe sul ramo remoto chiude campi senza decisione datata? → 🔴."""
    if _git(repo, "merge-base", remoto_ref, ref, check=False).returncode != 0:
        return []
    diff = _out(repo, "diff", f"{remoto_ref}...{ref}", "--", *FILE_S4)
    ch = chiusure(diff)
    if not ch["senza_decisione"]:
        return []
    return [_rilievo("S6", ROSSO, ramo, f"{ref} chiude {ch['senza_decisione']} campi aperti senza "
                     "una decisione datata del DM: non spingere",
                     "riporta i campi a «da compilare» o fai citare a ogni riga «[CANONE — DM AAAA-MM-GG, codice]» "
                     "della decisione mostrata al DM", ref=ref, **ch)]


def dopo_merge(repo: Path, risultato: str = "HEAD", prima: str = "ORIG_HEAD",
               main: str = "origin/main") -> dict:
    """S7: ogni riga che main ha aggiunto ai file di partita dalla base comune c'è nel risultato?"""
    base = _out(repo, "merge-base", prima, main)
    diff = _out(repo, "diff", base, main, "--", *CANONE)
    rilievi = []
    for rel, righe in righe_aggiunte(diff).items():
        r = _git(repo, "show", f"{risultato}:{rel}", check=False)
        presenti = {x.strip() for x in r.stdout.splitlines()} if r.returncode == 0 else set()
        perse = [x.strip() for x in righe if x.strip() not in presenti]
        if perse:
            rilievi.append(_rilievo("S7", ROSSO, risultato, f"{len(perse)} righe di main perse nel "
                                    f"merge in {rel}", "rimettile blocco per blocco (dal png e dalle "
                                    "correzioni di canone di main vince main); se lo stesso record è "
                                    "cambiato anche nel ramo, fermati e chiedi al DM",
                                    file=rel, righe=perse))
    return {"esito": 1 if rilievi else 0, "rilievi": rilievi,
            "misure": {"base": base[:9], "main": main, "risultato": risultato, "rami": {},
                       "patch": [], "patch_fuori_canone": 0}}


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
           campi_aperti: bool = True, tempo_scansione: float = TEMPO_SCANSIONE,
           ref: "str | None" = None) -> dict:
    """Le regole S1-S6 sui rami vivi. Con `ref` (per esempio HEAD prima del push) si misura
    quell'albero al posto del ramo remoto, e S6 guarda il diff fra il remoto e `ref`."""
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
        remoto_ref = _ref(repo, remoto, ramo)
        mio = ref or remoto_ref
        if not mio or not _esiste(repo, mio):
            rilievi.append(_rilievo("S2", NON_MISURABILE, ramo, "ramo vivo assente in questo clone",
                                    f"git fetch {remoto} {ramo}"))
            continue
        m: dict = {"ref": mio, "sha": _out(repo, "rev-parse", "--short", mio)}
        if ref and remoto_ref:
            rilievi += s6_ref(repo, ramo, remoto_ref, mio)
        if main:
            r2, m2 = s2(repo, ramo, mio, main, t_ora, giorni_rosso, shallow)
            rilievi += r2
            m.update(m2)
        else:
            rilievi.append(_rilievo("S2", NON_MISURABILE, ramo, "main assente in questo clone",
                                    f"git fetch {remoto} main"))
        r3, voci, fuori = s3(repo, ramo, mio, patch, t_ora, ore_patch)
        rilievi += r3
        misure["patch"] += voci
        misure["patch_fuori_canone"] = fuori
        aperti = campi_aperti_di(repo, mio)
        m["campi_aperti"] = sum(aperti.values())
        if campi_aperti:
            rilievi += s4(ramo, aperti)
        m["ultima_sessione"] = ultima_sessione(repo, mio)
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
    ap.add_argument("--ref", help="misura questo albero (es. HEAD prima del push) al posto del ramo "
                    "remoto; S6 guarda il diff fra il remoto e REF")
    ap.add_argument("--dopo-merge", action="store_true",
                    help="S7: le righe che main ha aggiunto ai file di partita ci sono nel risultato")
    ap.add_argument("--prima", default="ORIG_HEAD", help="con --dopo-merge: il ramo prima del merge")
    ap.add_argument("--main", help="con --dopo-merge: il main fuso (default <remoto>/main)")
    a = ap.parse_args(argv)
    try:
        errore = aggiorna(a.repo, a.registro, a.remoto) if a.aggiorna else None
        if a.dopo_merge:
            esito = dopo_merge(a.repo, a.ref or "HEAD", a.prima, a.main or f"{a.remoto}/main")
        else:
            esito = misura(a.repo, a.registro, a.scansiona, a.remoto, a.giorni_rosso, a.ore_patch,
                           a.ora, campi_aperti=not a.senza_campi_aperti,
                           tempo_scansione=TEMPO_SCANSIONE if a.avviso else 600, ref=a.ref)
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
