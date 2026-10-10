#!/usr/bin/env python3
"""
ambiente.py — l'ambiente di sviluppo completo, installato col registro e tolto col rollback.

È la parte A5c e A5d di PIANO-AMBIENTE-RIPRODUCIBILE (D1: «un registro di cosa
è installato, così si può disinstallare con sudo»), anticipata il 2026-10-09
perché il DM, installando su Debian 13, ha chiesto anche Blender, ComfyUI e
typst, e un modo per pulire il sistema.

    python3 scripts/ambiente.py piano  [--con blender,comfyui,typst]
    python3 scripts/ambiente.py installa [--con ...] [--si]
    python3 scripts/ambiente.py stato
    python3 scripts/ambiente.py rimuovi [--venv] [--si]
    python3 scripts/ambiente.py adotta --apt-dal 2026-10-09 [--si]

Cosa installa, e come lo ricorda. Ogni passo scrive nel registro
(`$XDG_STATE_HOME/rumblingstone/<id del clone>/stato.json`) **prima** di
passare al successivo, così un'installazione interrotta si toglie lo stesso.
- **pacchetti di sistema** (Debian e Ubuntu): `dpkg` fotografato prima e dopo
  `apt-get install`; il registro possiede la differenza, cioè i pacchetti
  chiesti più le dipendenze che sono arrivate con loro. Un pacchetto che c'era
  già non diventa mai nostro.
- **il `.venv`**: `requirements-completo.txt` (bpy, torch per CPU, piq);
  possiede i pacchetti Python che prima non c'erano.
- **typst** (`--con typst`, solo se manca): la versione fissata dalla CI, in
  `~/.local/bin`, con lo sha256 del file scritto nel registro.
- **ComfyUI** (`--con comfyui`): `scripts/comfyui-local/setup-distrobox.sh`
  nella cartella `COMFYUI_DIR`; il registro sa se il box e la cartella
  esistevano già.

Come toglie. `rimuovi` ripercorre il registro all'indietro e toglie solo ciò
che è suo:
- il box e la cartella di ComfyUI, se li ha creati lui;
- typst, se il file è ancora quello installato;
- i pacchetti Python posseduti, oppure con `--venv` tutto il `.venv`;
- i pacchetti di sistema posseduti, dopo averti mostrato la simulazione di
  `apt-get -s remove`.

Mai `autoremove` e mai `purge`, che toglierebbero anche ciò che non è nostro.
Un pacchetto posseduto da cui ora dipende un pacchetto non nostro resta, e lo
dice. `apt` non ha un *undo*: il registro è quello che lo sostituisce.

Ciò che si è installato a mano prima che esistesse questo script si adotta da
`/var/log/apt/history.log` con `adotta --apt-dal DATA`: entrano nel registro le
transazioni di quel giorno e dei successivi che hanno installato pacchetti oggi
presenti, e che c'erano prima di quella data no.

Exit: 0 fatto · 1 un passo fallito (il registro dice cosa c'è) · 2 piattaforma
o ambiente non adatti (niente apt, niente .venv).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CI = REPO / ".github" / "workflows" / "ci.yml"
COMPLETO = REPO / "requirements-completo.txt"
COMFYUI = REPO / "scripts" / "comfyui-local"

#: I pacchetti di sistema del profilo completo, su Debian 13 e Ubuntu 24.04.
#: Sono i binari di `binari.py` che il gestore di pacchetti fornisce; typst e
#: pdfcpu non ci sono e hanno la loro strada.
APT_BASE = ("chromium", "pandoc", "texlive-xetex", "maven", "default-jre",
            "webp", "inkscape", "shellcheck")
APT_CON = {"blender": ("blender",), "comfyui": ("distrobox", "podman")}
MODULI = ("blender", "comfyui", "typst")


class Sistema:
    """Tutto ciò che tocca la macchina passa di qui: i test ne usano uno finto."""

    def esegui(self, cmd: list[str], *, cattura: bool = True, env: dict | None = None):
        return subprocess.run(cmd, capture_output=cattura, text=True, env=env)

    def os_release(self) -> dict[str, str]:
        p = Path("/etc/os-release")
        if not p.exists():
            return {}
        out = {}
        for riga in p.read_text(encoding="utf-8").splitlines():
            if "=" in riga:
                k, v = riga.split("=", 1)
                out[k] = v.strip('"')
        return out

    def dpkg(self) -> dict[str, str]:
        """{pacchetto: versione} dei pacchetti installati."""
        r = self.esegui(["dpkg-query", "-W", "-f=${Package}\t${Version}\t${db:Status-Status}\n"])
        out = {}
        for riga in r.stdout.splitlines():
            parti = riga.split("\t")
            if len(parti) == 3 and parti[2] == "installed":
                out[parti[0]] = parti[1]
        return out

    def dipendono_da(self, pacchetto: str) -> set[str]:
        """I pacchetti installati che dipendono davvero (Depends, PreDepends) da questo."""
        r = self.esegui(["apt-cache", "rdepends", "--installed", "--no-recommends",
                         "--no-suggests", "--no-conflicts", "--no-breaks", "--no-replaces",
                         "--no-enhances", pacchetto])
        return {r_.strip().lstrip("|") for r_ in r.stdout.splitlines()[2:] if r_.strip()}

    def pip(self) -> dict[str, str]:
        r = self.esegui([sys.executable, "-m", "pip", "list", "--format=json"])
        return {d["name"].lower(): d["version"] for d in json.loads(r.stdout or "[]")}

    def chiedi(self, domanda: str) -> bool:
        try:
            return input(f"{domanda} [s/N] ").strip().lower() in ("s", "si", "sì", "y", "yes")
        except EOFError:
            return False

    def scarica(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": "RumblingStone ambiente.py"})
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()

    def history_apt(self) -> str:
        p = Path("/var/log/apt/history.log")
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


# ── il registro ──────────────────────────────────────────────────────────────

def percorso_stato(repo: Path = REPO) -> Path:
    base = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")
    ident = hashlib.sha256(str(repo.resolve()).encode()).hexdigest()[:12]
    return base / "rumblingstone" / ident / "stato.json"


def leggi_stato(p: Path) -> dict:
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"repo": str(REPO), "passi": []}


def scrivi_stato(p: Path, stato: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(stato, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(p)


def aggiungi(p: Path, passo: dict) -> None:
    stato = leggi_stato(p)
    passo["quando"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    stato["passi"].append(passo)
    scrivi_stato(p, stato)


# ── che cosa serve ───────────────────────────────────────────────────────────

def pacchetti_apt(con: set[str]) -> list[str]:
    out = list(APT_BASE)
    for m in sorted(con):
        out += APT_CON.get(m, ())
    return out


def versione_typst() -> str:
    m = re.search(r'TYPST_VERSION:\s*"([^"]+)"', CI.read_text(encoding="utf-8"))
    if not m:
        raise ValueError("TYPST_VERSION non trovata in ci.yml")
    return m.group(1)


def in_venv() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def piano(sis: Sistema, con: set[str]) -> dict:
    installati = sis.dpkg() if shutil.which("dpkg-query") else {}
    apt = pacchetti_apt(con)
    return {
        "piattaforma": sis.os_release().get("PRETTY_NAME", "?"),
        "apt_mancanti": [p for p in apt if p not in installati],
        "apt_presenti": [p for p in apt if p in installati],
        "venv": in_venv(),
        "typst": shutil.which("typst"),
        "comfyui_dir": os.environ.get("COMFYUI_DIR"),
    }


# ── installa ─────────────────────────────────────────────────────────────────

def installa_apt(sis: Sistema, pacchetti: list[str], stato_p: Path, si: bool) -> int:
    prima = sis.dpkg()
    mancanti = [p for p in pacchetti if p not in prima]
    if not mancanti:
        print("✓ pacchetti di sistema: già tutti presenti, niente diventa nostro")
        return 0
    print(f"==> pacchetti di sistema da installare: {' '.join(mancanti)}")
    sim = sis.esegui(["apt-get", "-s", "install", "--no-install-recommends", *mancanti])
    arrivano = [r.split()[1] for r in sim.stdout.splitlines() if r.startswith("Inst ")]
    print(f"    con le dipendenze: {len(arrivano)} pacchetti")
    if not si and not sis.chiedi("Installo con sudo apt-get?"):
        print("○ pacchetti di sistema: saltati")
        return 0
    r = sis.esegui(["sudo", "apt-get", "install", "-y", "--no-install-recommends", *mancanti],
                   cattura=False)
    dopo = sis.dpkg()
    posseduti = {p: v for p, v in dopo.items() if p not in prima}
    aggiungi(stato_p, {"tipo": "apt", "chiesti": mancanti, "posseduti": posseduti})
    print(f"{'✓' if r.returncode == 0 else '✗'} pacchetti di sistema: {len(posseduti)} nel registro")
    return 0 if r.returncode == 0 else 1


def installa_pip(sis: Sistema, stato_p: Path) -> int:
    prima = sis.pip()
    r = sis.esegui([sys.executable, "-m", "pip", "install", "-r", str(COMPLETO)], cattura=False)
    dopo = sis.pip()
    posseduti = sorted(n for n in dopo if n not in prima)
    aggiungi(stato_p, {"tipo": "pip", "venv": sys.prefix, "posseduti": posseduti})
    print(f"{'✓' if r.returncode == 0 else '✗'} .venv: {len(posseduti)} pacchetti Python nel registro")
    return 0 if r.returncode == 0 else 1


def installa_typst(sis: Sistema, stato_p: Path) -> int:
    if shutil.which("typst"):
        print(f"✓ typst: già presente in {shutil.which('typst')}, non diventa nostro")
        return 0
    v = versione_typst()
    url = f"https://github.com/typst/typst/releases/download/v{v}/typst-x86_64-unknown-linux-musl.tar.xz"
    print(f"==> typst {v} (la versione della CI) in ~/.local/bin")
    with tarfile.open(fileobj=io.BytesIO(sis.scarica(url)), mode="r:xz") as tar:
        membro = next(m for m in tar.getmembers() if m.name.endswith("/typst") and m.isfile())
        dati = tar.extractfile(membro).read()
    dest = Path.home() / ".local" / "bin" / "typst"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(dati)
    dest.chmod(0o755)
    sha = hashlib.sha256(dati).hexdigest()
    aggiungi(stato_p, {"tipo": "typst", "file": str(dest), "sha256": sha, "versione": v})
    print(f"✓ typst {v}: {dest} (sha256 {sha[:16]}…)")
    return 0


def installa_comfyui(sis: Sistema, stato_p: Path, si: bool) -> int:
    cartella = os.environ.get("COMFYUI_DIR")
    if not cartella:
        print("✗ ComfyUI: imposta prima la cartella, es. export COMFYUI_DIR=/srv/comfyui", file=sys.stderr)
        return 1
    box = os.environ.get("COMFYUI_BOX", "comfyui")
    elenco = sis.esegui(["distrobox", "list", "--no-color"]).stdout
    box_c_era = re.search(rf"\|\s*{re.escape(box)}\s*\|", elenco) is not None
    dir_c_era = Path(cartella, ".git").exists()
    passo = {"tipo": "comfyui", "dir": cartella, "dir_creata": not dir_c_era,
             "box": box, "box_creato": not box_c_era}
    aggiungi(stato_p, passo)  # prima del setup: un setup interrotto si toglie lo stesso
    r = sis.esegui(["bash", str(COMFYUI / "setup-distrobox.sh")], cattura=False)
    if r.returncode != 0:
        print("✗ ComfyUI: il setup si è fermato; il registro lo sa, `rimuovi` pulisce")
        return 1
    if si or sis.chiedi("Scarico anche il checkpoint SDXL (~6,9 GB)?"):
        sis.esegui(["bash", str(COMFYUI / "scarica-pesi.sh")], cattura=False)
    print(f"✓ ComfyUI in {cartella}, box «{box}»")
    return 0


# ── rimuovi ──────────────────────────────────────────────────────────────────

def da_togliere_apt(sis: Sistema, posseduti: set[str]) -> tuple[list[str], dict[str, set[str]]]:
    """I pacchetti posseduti che si possono togliere, e quelli che restano perché
    un pacchetto non nostro ne dipende."""
    installati = set(sis.dpkg())
    candidati = posseduti & installati
    restano = {}
    for p in sorted(candidati):
        estranei = {d for d in sis.dipendono_da(p) if d in installati and d not in posseduti}
        if estranei:
            restano[p] = estranei
    return sorted(candidati - set(restano)), restano


def rimuovi(sis: Sistema, stato_p: Path, si: bool, venv: bool) -> int:
    stato = leggi_stato(stato_p)
    if not stato["passi"]:
        print("○ il registro è vuoto: niente da togliere")
        return 0
    errori = 0
    for passo in reversed(list(stato["passi"])):
        tipo, fatto = passo["tipo"], True
        if tipo == "comfyui":
            if passo.get("box_creato"):
                sis.esegui(["distrobox", "rm", passo["box"], "--force"], cattura=False)
            if passo.get("dir_creata") and Path(passo["dir"]).exists():
                if si or sis.chiedi(f"Cancello {passo['dir']} (clone e pesi di ComfyUI)?"):
                    shutil.rmtree(passo["dir"])
                else:
                    fatto = False
            print(f"{'✓' if fatto else '○'} ComfyUI: box e cartella")
        elif tipo == "typst":
            f = Path(passo["file"])
            if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == passo["sha256"]:
                f.unlink()
                print(f"✓ typst: tolto {f}")
            else:
                print(f"○ typst: {f} non c'è più o è cambiato, lo lascio")
        elif tipo == "pip":
            if venv:
                print("○ pacchetti Python: li toglie --venv con tutto il .venv")
            elif passo["posseduti"]:
                r = sis.esegui([sys.executable, "-m", "pip", "uninstall", "-y", *passo["posseduti"]],
                               cattura=False)
                fatto = r.returncode == 0
                print(f"{'✓' if fatto else '✗'} pacchetti Python: {len(passo['posseduti'])}")
        elif tipo == "apt":
            togli, restano = da_togliere_apt(sis, set(passo["posseduti"]))
            for p, chi in restano.items():
                print(f"○ {p} resta: ne dipende {', '.join(sorted(chi))}, che non è nostro")
            if togli:
                sim = sis.esegui(["apt-get", "-s", "remove", *togli])
                via = {r.split()[1] for r in sim.stdout.splitlines() if r.startswith("Remv ")}
                estranei = via - set(passo["posseduti"])
                if estranei:
                    print(f"✗ apt toglierebbe anche {', '.join(sorted(estranei))}: mi fermo")
                    errori += 1
                    continue
                print(f"==> da togliere ({len(togli)}): {' '.join(togli)}")
                if si or sis.chiedi("Tolgo con sudo apt-get remove?"):
                    r = sis.esegui(["sudo", "apt-get", "remove", "-y", *togli], cattura=False)
                    fatto = r.returncode == 0
                else:
                    fatto = False
                print(f"{'✓' if fatto else '○'} pacchetti di sistema")
        if fatto:
            stato["passi"].remove(passo)
            scrivi_stato(stato_p, stato)
        else:
            errori += 1
    if venv:
        cartella = Path(sys.prefix) if in_venv() else REPO / ".venv"
        if cartella.is_relative_to(REPO) and cartella.exists():
            shutil.rmtree(cartella)
            print(f"✓ .venv: tolto {cartella} (si ricrea con python3 -m venv .venv)")
    return 1 if errori else 0


# ── adotta ───────────────────────────────────────────────────────────────────

def adotta_apt(sis: Sistema, testo_history: str, dal: str) -> dict[str, str]:
    """I pacchetti installati da transazioni apt dal giorno `dal` in poi, che ci
    sono ancora: chi li ha installati a mano prima di questo script li affida al
    registro."""
    installati = sis.dpkg()
    out = {}
    for blocco in testo_history.split("\n\n"):
        m = re.search(r"^Start-Date: (\d{4}-\d{2}-\d{2})", blocco, re.M)
        inst = re.search(r"^Install: (.+)$", blocco, re.M)
        if not m or not inst or m.group(1) < dal:
            continue
        for voce in re.finditer(r"([^\s,:]+)(?::[a-z0-9]+)? \(([^,)]+)", inst.group(1)):
            nome = voce.group(1)
            if nome in installati:
                out[nome] = installati[nome]
    return out


# ── main ─────────────────────────────────────────────────────────────────────

def main(argv=None, sis: Sistema | None = None, stato_p: Path | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("azione", choices=["piano", "installa", "stato", "rimuovi", "adotta"])
    ap.add_argument("--con", default="", help="moduli in più: blender, comfyui, typst (separati da virgole)")
    ap.add_argument("--si", action="store_true", help="non chiede conferma (i comandi sudo chiedono la password)")
    ap.add_argument("--venv", action="store_true", help="rimuovi: toglie tutto il .venv del repo")
    ap.add_argument("--apt-dal", metavar="AAAA-MM-GG", help="adotta: le transazioni apt da questa data")
    args = ap.parse_args(argv)
    sis = sis or Sistema()
    stato_p = stato_p or percorso_stato()
    con = {c.strip() for c in args.con.split(",") if c.strip()}
    ignoti = con - set(MODULI)
    if ignoti:
        ap.error(f"moduli sconosciuti: {', '.join(sorted(ignoti))} (ci sono: {', '.join(MODULI)})")
    apt_ok = sis.os_release().get("ID") in ("debian", "ubuntu") or "debian" in sis.os_release().get("ID_LIKE", "")

    if args.azione == "stato":
        stato = leggi_stato(stato_p)
        print(f"registro: {stato_p}")
        for passo in stato["passi"]:
            n = len(passo.get("posseduti", [])) or ""
            print(f"  {passo['quando']}  {passo['tipo']:8} {n} {passo.get('dir') or passo.get('file') or ''}")
        if not stato["passi"]:
            print("  vuoto")
        return 0
    if args.azione == "piano":
        pi = piano(sis, con)
        print(f"piattaforma: {pi['piattaforma']}")
        print(f"pacchetti di sistema da installare: {' '.join(pi['apt_mancanti']) or 'nessuno'}")
        print(f"già presenti, non diventano nostri: {' '.join(pi['apt_presenti']) or 'nessuno'}")
        print(f".venv attivo: {'sì' if pi['venv'] else 'NO: attivalo prima di installa'}")
        print(f"typst: {pi['typst'] or ('si installa' if 'typst' in con else 'manca, --con typst')}")
        if "comfyui" in con:
            print(f"ComfyUI in: {pi['comfyui_dir'] or 'COMFYUI_DIR non impostata'}")
        print(f"registro: {stato_p}")
        return 0
    if args.azione == "rimuovi":
        return rimuovi(sis, stato_p, args.si, args.venv)
    if args.azione == "adotta":
        if not args.apt_dal:
            ap.error("adotta vuole --apt-dal AAAA-MM-GG")
        trovati = adotta_apt(sis, sis.history_apt(), args.apt_dal)
        if not trovati:
            print("○ nessuna transazione apt da adottare")
            return 0
        print(f"==> {len(trovati)} pacchetti installati dal {args.apt_dal}: {' '.join(sorted(trovati))}")
        if args.si or sis.chiedi("Li metto nel registro, così rimuovi li toglie?"):
            aggiungi(stato_p, {"tipo": "apt", "chiesti": [], "posseduti": trovati,
                               "adottati_dal": args.apt_dal})
            print("✓ adottati")
        return 0

    # installa
    if not in_venv():
        print("✗ attiva prima il .venv del repo: source .venv/bin/activate", file=sys.stderr)
        return 2
    rc = 0
    if apt_ok:
        rc |= installa_apt(sis, pacchetti_apt(con), stato_p, args.si)
    else:
        print("○ niente apt su questa piattaforma: i pacchetti di sistema sono in scripts/binari.py")
    rc |= installa_pip(sis, stato_p)
    if "typst" in con:
        rc |= installa_typst(sis, stato_p)
    if "comfyui" in con:
        rc |= installa_comfyui(sis, stato_p, args.si)
    print(f"\nregistro: {stato_p}\npoi: python scripts/dm.py doctor")
    return rc


if __name__ == "__main__":
    sys.exit(main())
