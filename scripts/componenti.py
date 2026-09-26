#!/usr/bin/env python3
"""componenti.py — il master scomposto nei suoi componenti, e rimesso insieme (ADR-0074).

Un master DEF è scritto in prosa, ma dentro ha blocchi con un tipo e una forma
fissa: la scena, il contratto «In scena», il box read-aloud etichettato, la
scheda d'entrata, la tabella delle comparse, la battuta `**NOME:**`, la prova
con la sua CD. Questo script li legge, e ne fa tre cose.

1. **L'indice** (`--json`): scena per scena, dove, chi, box, schede, comparse,
   prove. È il dato su cui si possono fare domande a tutto l'arco.
2. **L'apparato d'uso** (`--apparato`), che `rumblingstone-module-standard`
   §15 chiede e che finora si scriveva a mano: il foglio del cast, l'inserto
   con tutte le CD, l'indice dei read-aloud in ordine di gioco. Si genera nel
   file `APPARATO-<master>.md` accanto al master, e non si tocca a mano.
3. **Le inclusioni** (`--includi`): un blocco scritto una volta sola in un file
   si copia in un altro fra due marcatori,

       <!-- include: Bestiario/villain/x.md#numeri -->
       …testo copiato…
       <!-- /include -->

   dove la fonte delimita il blocco con `<!-- blocco: numeri -->` …
   `<!-- /blocco -->`; `#statblocco` prende invece il recinto ```statblocco
   della scheda (ADR-0021), senza marcatori nella fonte. Il testo copiato resta nel sorgente, così chi apre il
   file senza stamparlo lo legge; la fonte resta una sola, perché lo script lo
   riscrive dalla fonte e la CI boccia una copia che non combacia più.

Uso:
    python3 scripts/componenti.py MASTER.md [--json]     # l'indice
    python3 scripts/componenti.py --apparato [--check]  # l'apparato di ogni master col contratto
    python3 scripts/componenti.py --includi [--check]   # riallinea le copie alle fonti
    python3 scripts/componenti.py --check                # tutte e due le verifiche, per la CI

Solo libreria standard. Exit code: 0 = ok · 1 = apparato o copie non allineati (--check).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import copertura_scene as cs  # noqa: E402  (scene, contratto e schede si leggono in un posto solo)
import misura_craft as mc  # noqa: E402

INTESTAZIONE = ("<!-- generato da scripts/componenti.py --apparato: non modificare a mano, "
                "si rigenera dal master (ADR-0074) -->\n")

_RIGA_SCHEDA = re.compile(r"^\|\s*\*\*(Aspetto|Vuole|Suona|Sa|Teme|Vende)\*\*\s*\|\s*(.+?)\s*\|\s*$", re.M)
#: Ogni «CD N» del testo. L'etichetta non si indovina con una regex sulle parole
#: che la precedono: alla prima misura su DEF-4 quel criterio ne perdeva 13 su 43
#: («FOR o DES grezza», «Conoscenze storia», «Forza o attacco, CD 18»). Qui entra
#: ogni CD, e l'etichetta è la coda della sua cella o frase (_etichetta_prova).
_CD = re.compile(r"\bCD\s*\*{0,2}\s*(\d+)")
_TAGLIO = re.compile(r"[|;:]|[.!?]\s+(?=[A-ZÀ-Ù«\"])|\n\s*(?:>\s*)?(?:\n|[-|])|—|\*\*\s|\bCD\s*\*{0,2}\s*\d+\*{0,2},?")
_INCLUDE = re.compile(r"(<!--\s*include:\s*(?P<src>[^#\s]+)#(?P<nome>[\w-]+)\s*-->\n)(?P<corpo>.*?)"
                      r"(<!--\s*/include\s*-->)", re.S)


# ─── l'indice ────────────────────────────────────────────────────────────────

def _schede(corpo: str) -> "list[dict]":
    out = []
    for m in cs._SCHEDA.finditer(corpo):
        nome = m.group(1).split(",")[0].strip(" *")
        coda = corpo[m.end():]
        fine = re.search(r"\n\s*\n(?!\|)", coda)
        tabella = coda[: fine.start()] if fine else coda
        campi = {k: v for k, v in _RIGA_SCHEDA.findall(tabella)}
        out.append({"nome": nome, **{k.lower(): v for k, v in campi.items()}})
    return out


def _comparse(corpo: str) -> "list[dict]":
    out = []
    for m in re.finditer(r"^\*\*Comparse\*\*.*$", corpo, re.M):
        for riga in corpo[m.end():].lstrip("\n").splitlines():
            if not riga.startswith("|"):
                break
            celle = [c.strip() for c in riga.strip().strip("|").split("|")]
            if len(celle) < 3 or re.match(r"^:?-", celle[0]) or celle[0] == "Chi":
                continue
            out.append({"nome": re.sub(r"[*`]|\[[^\]]*\]", "", celle[0]).strip(),
                        "come": celle[1], "parla": celle[2]})
    return out


def _box(corpo: str) -> "list[dict]":
    out = []
    for b in mc.box_read_aloud(corpo):
        m = re.search(r"\*\*Read-aloud\s*(?:\(([^)]*)\))?\s*(?:—\s*([^*]+?))?\.?\*\*", b[0])
        prima = re.sub(r"^>\s*(\*\*Read-aloud[^*]*\*\*)?\s*", "", b[0]).strip(" *_")
        out.append({"pilastro": (m.group(1) or "").strip() if m else "",
                    "etichetta": (m.group(2) or "").strip() if m else "",
                    "righe": len(b), "attacco": prima[:70]})
    return out


def _etichetta_prova(prima: str) -> str:
    """La coda di testo prima di una CD: dall'ultimo separatore, al più sei parole."""
    tagli = list(_TAGLIO.finditer(prima))
    coda = prima[tagli[-1].end():] if tagli else prima
    coda = re.sub(r"\n\s*>?", " ", coda)  # il nome della prova può andare a capo
    coda = re.sub(r"[*_`>]|\[([^\]]*)\]\([^)]*\)", r"\1", coda)
    coda = re.sub(r"[\s(,]+$", "", re.sub(r"\s+", " ", coda)).strip()
    return " ".join(coda.split()[-6:]).lstrip("(-–, o").strip()


def _prove(corpo: str) -> "list[dict]":
    viste, out = set(), []
    for m in _CD.finditer(corpo):
        chi = _etichetta_prova(corpo[max(0, m.start() - 160):m.start()])
        if not chi:  # «CD 20 (CD 16 se…)»: la seconda è un'alternativa della prima
            chi = f"{out[-1]['prova']}, alternativa" if out else "(senza etichetta)"
        chiave = (chi.lower(), m.group(1))
        if chiave not in viste:
            viste.add(chiave)
            out.append({"prova": chi, "cd": int(m.group(1))})
    return out


def indice(master: Path, profilo: "dict | None" = None) -> dict:
    profilo = profilo or {}
    master = master if master.is_absolute() else (ROOT / master).resolve()
    testo = cs.pulisci(master.read_text(encoding="utf-8"))
    scene = []
    for titolo, corpo in cs.scene(testo, profilo.get("scena", cs.SCENA_DEF), profilo.get("escludi")):
        m = cs._CONTRATTO.search(corpo)
        scene.append({
            "scena": cs.chiave_scena(titolo), "titolo": titolo,
            "dove": cs.voci(m.group("dove")) if m else [],
            "chi": cs.voci(m.group("chi")) if m else [],
            "box": _box(corpo), "schede": _schede(corpo), "comparse": _comparse(corpo),
            "battute": sorted({b.group(1).strip() for b in cs._BATTUTA.finditer(corpo)}),
            "prove": _prove(corpo),
        })
    return {"master": master.relative_to(ROOT).as_posix(), "scene": scene}


# ─── l'apparato ─────────────────────────────────────────────────────────────

def _cella(s: str) -> str:
    return (s or "—").replace("|", "/").replace("\n", " ").strip()


def apparato(idx: dict) -> str:
    righe = [INTESTAZIONE, f"# Apparato d'uso — `{Path(idx['master']).stem}`\n",
             "Il foglio del cast, l'inserto con le CD e l'indice dei read-aloud, "
             "presi dai componenti del master. Per cambiarli si cambia il master.\n",
             "## Il foglio del cast\n",
             "| Chi | Dove si incontra | Vuole | Come parla |", "|---|---|---|---|"]
    visti = set()
    for s in idx["scene"]:
        for p in s["schede"]:
            if p["nome"] in visti:
                continue
            visti.add(p["nome"])
            righe.append(f"| **{_cella(p['nome'])}** | {s['scena']} | {_cella(p.get('vuole'))} "
                         f"| {_cella(p.get('suona'))} |")
        for c in s["comparse"]:
            if c["nome"] in visti:
                continue
            visti.add(c["nome"])
            righe.append(f"| {_cella(c['nome'])} | {s['scena']} | — | {_cella(c['parla'])} |")
    righe += ["", "## L'inserto delle CD\n", "| Scena | Prova | CD |", "|---|---|---:|"]
    for s in idx["scene"]:
        for p in s["prove"]:
            righe.append(f"| {s['scena']} | {_cella(p['prova'])} | {p['cd']} |")
    righe += ["", "## L'indice dei read-aloud, in ordine di gioco\n",
              "| Scena | Luogo o momento | Pilastro | Righe |", "|---|---|---|---:|"]
    for s in idx["scene"]:
        for b in s["box"]:
            righe.append(f"| {s['scena']} | {_cella(b['etichetta'] or b['attacco'])} "
                         f"| {_cella(b['pilastro'])} | {b['righe']} |")
    return "\n".join(righe) + "\n"


def master_col_contratto() -> "list[tuple[Path, dict]]":
    cfg = cs.carica_config()
    return [(ROOT / m["file"], m) for m in cs.moduli(cfg) if m.get("contratto")]


def file_apparato(master: Path) -> Path:
    """`APPARATO-<master>.md`, accanto al master. Il prefisso non è estetica: con
    il suffisso il file combaciava con `ARC*-DEF-*.md`, e quattro strumenti lo
    prendevano per un master (alla prima prova, un `-APPARATO-APPARATO.md`)."""
    return master.with_name("APPARATO-" + master.name)


# ─── le inclusioni ──────────────────────────────────────────────────────────

def blocco(sorgente: Path, nome: str) -> str:
    """Il testo di un blocco nominato. `#statblocco` è il recinto ```statblocco
    della scheda (ADR-0021): un componente che ha già un tipo non ha bisogno
    di un segnaposto in più nel file che lo contiene."""
    testo = sorgente.read_text(encoding="utf-8")
    if nome == "statblocco":
        m = re.search(r"^```statblocco\n.*?^```[ \t]*$", testo, re.S | re.M)
        if not m:
            raise KeyError(f"{sorgente.relative_to(ROOT)}: manca il blocco ```statblocco")
        return m.group(0) + "\n"
    m = re.search(rf"<!--\s*blocco:\s*{re.escape(nome)}\s*-->\n?(.*?)<!--\s*/blocco\s*-->", testo, re.S)
    if not m:
        raise KeyError(f"{sorgente.relative_to(ROOT)}: manca il blocco «{nome}»")
    return m.group(1).rstrip("\n") + "\n"


def riallinea(testo: str) -> str:
    """Ogni copia fra `include` e `/include` riscritta dalla sua fonte. Pura sul testo."""
    return _INCLUDE.sub(lambda m: m.group(1) + blocco(ROOT / m.group("src"), m.group("nome"))
                        + m.group(5), testo)


def file_con_inclusioni() -> "list[Path]":
    fuori = []
    for f in sorted(ROOT.rglob("*.md")):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(("build/", ".claude/", ".git/")) or "_ARCHIVIO/" in rel:
            continue
        try:
            if "<!-- include:" in f.read_text(encoding="utf-8"):
                fuori.append(f)
        except UnicodeDecodeError:
            continue
    return fuori


# ─── main ───────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("master", nargs="?", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--apparato", action="store_true")
    ap.add_argument("--includi", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.master:
        idx = indice(a.master.resolve())
        print(json.dumps(idx, ensure_ascii=False, indent=2) if a.json else apparato(idx))
        return 0

    fare_apparato = a.apparato or (a.check and not a.includi)
    fare_includi = a.includi or (a.check and not a.apparato)
    errori = []
    if fare_includi:
        for f in file_con_inclusioni():
            prima = f.read_text(encoding="utf-8")
            dopo = riallinea(prima)
            if prima != dopo:
                if a.check:
                    errori.append(f"{f.relative_to(ROOT)}: una copia non combacia con la sua fonte "
                                  "— python3 scripts/componenti.py --includi")
                else:
                    f.write_text(dopo, encoding="utf-8")
                    print(f"✎ riallineato {f.relative_to(ROOT)}")
    if fare_apparato:
        for master, profilo in master_col_contratto():
            atteso = apparato(indice(master, profilo))
            dest = file_apparato(master)
            if dest.exists() and dest.read_text(encoding="utf-8") == atteso:
                continue
            if a.check:
                errori.append(f"{dest.relative_to(ROOT)}: non è quello che il master genera "
                              "— python3 scripts/componenti.py --apparato")
            else:
                dest.write_text(atteso, encoding="utf-8")
                print(f"✎ scritto {dest.relative_to(ROOT)}")
    for e in errori:
        print(f"✗ {e}")
    if a.check:
        print("✓ componenti: apparato e copie allineati" if not errori
              else f"✗ componenti: {len(errori)} da rigenerare")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
