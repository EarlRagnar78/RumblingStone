#!/usr/bin/env python3
"""copertura_scene.py — il DM trova scritto chi e dove incontra i PG? (ADR-0073)

Il 2026-09-25, al tavolo, il DM ha dovuto inventare sette cose che
`ARC07-DEF-4` non diceva: stanze in cui i PG entravano e persone con cui
parlavano. Tutti i validatori erano verdi. Nessuno misurava la norma che
`rumblingstone-module-standard` scrive da luglio: **la scheda d'entrata del
PNG sta nella scena in cui i PG lo incontrano**.

Questo script è la metà deterministica dello strumento *lettore e playtester*.
L'altra metà sono due letture a freddo fatte da un agente, con una rubrica
fissa (`skills/rumblingstone-playtest/references/`). La lettura trova i buchi
la prima volta; lo script impedisce che lo stesso tipo di buco torni.

Le regole, e cosa controllano:

  C1 · scena senza box — una scena giocabile senza nemmeno un read-aloud.
  C2 · parla senza scheda — un'etichetta di battuta `**NOME:**` per un PNG che
       non ha una `Scheda d'entrata` nel modulo.
  C3 · il contratto «In scena» — nei moduli che lo adottano, ogni scena apre con

           **In scena** — Dove: luogo · luogo — Chi: persona · persona

       e ogni *Dove* ha un box con quel luogo nell'etichetta, ogni *Chi* ha una
       scheda d'entrata o una riga nella tabella **Comparse** della scena.
  C4 · fuori dal contratto — una scheda d'entrata o un'etichetta di battuta in
       una scena, per qualcuno che il suo *Chi* non elenca.

Quello che lo script **non** vede, dichiarato: una persona o un luogo che il
testo non nomina affatto. Un capitano che nessuno ha scritto non ha
un'etichetta né una scheda. Per quello c'è il lettore a freddo; il contratto
serve a costringere chi scrive a fare l'elenco, e C4 a tenerlo onesto.

I moduli, i loro profili e i residui dichiarati (con la ragione) stanno in
`plans/copertura-scene.json`. Un master `ARC*-DEF-*` che il file non elenca
prende il profilo più severo, contratto compreso: i master nuovi nascono sotto
il cancello. Un residuo che non si verifica più è un errore anche lui: va tolto.

Uso:
    python3 scripts/copertura_scene.py                  # rapporto su tutti i moduli
    python3 scripts/copertura_scene.py --check          # cancello CI: esce 1 sui rilievi non dichiarati
    python3 scripts/copertura_scene.py --file X.md [--contratto]   # un file qualunque, senza residui

Solo libreria standard. Exit code: 0 = ok · 1 = rilievi non dichiarati o residui scaduti.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402  (il rilevatore dei box è uno solo)

CONFIG = ROOT / "plans" / "copertura-scene.json"
GLOB_MASTER = "ARC*-DEF-*.md"
SCENA_DEF = r"^###\s+SCENA\b"

_STORICO = re.compile(r"<!--\s*storico\s*-->.*?<!--\s*/storico\s*-->", re.S)
#: `**DURIN:**`, `**DURIN (rotto):**`, `> **BALVAR:**` — solo maiuscole: è la
#: forma prescritta da `editorial-standards.md` §2 per chi parla.
_BATTUTA = re.compile(r"^(?:>\s*)?\*\*([A-ZÀ-Ù][A-ZÀ-Ù' ]{1,40}?)\s*(?:\([^)]*\))?:\*\*", re.M)
_SCHEDA = re.compile(r"^\*\*Scheda d'entrata\s+—\s+([^*\n]+)", re.M)
_CONTRATTO = re.compile(r"^\*\*In scena\*\*\s*—\s*Dove:\s*(?P<dove>.*?)\s*—\s*Chi:\s*(?P<chi>.*)$", re.M)
_ETICHETTA_BOX = re.compile(r"\*\*Read-aloud[^*\n]*?—\s*([^*\n]+?)\.?\*\*", re.I)
_ARTICOLI = re.compile(r"^(?:il|lo|la|i|gli|le|l'|un|una|uno)\s*", re.I)


def norm(s: str) -> str:
    """Minuscolo, senza parentesi, markdown e articolo iniziale."""
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[*_`\[\]]", "", s).strip().lower()
    return _ARTICOLI.sub("", s).strip(" .,;:")


def voci(campo: str) -> "list[str]":
    campo = campo.strip()
    if campo.lower() in ("", "nessuno", "—", "-"):
        return []
    return [v.strip() for v in campo.split("·") if v.strip()]


def pulisci(testo: str) -> str:
    return _STORICO.sub("", testo)


def scene(testo: str, rx_scena: str, rx_escludi: "str | None") -> "list[tuple[str, str]]":
    """(titolo, corpo) per ogni scena; la scena finisce alla prossima scena o a un `##`."""
    inizi = [m for m in re.finditer(rx_scena, testo, re.M)]
    out = []
    for i, m in enumerate(inizi):
        fine = inizi[i + 1].start() if i + 1 < len(inizi) else len(testo)
        corpo = testo[m.start():fine]
        livello = len(re.match(r"#+", corpo).group(0))
        primo_a_capo = corpo.find("\n") + 1
        dopo = (re.search(rf"^#{{1,{livello - 1}}}\s", corpo[primo_a_capo:], re.M)
                if livello > 1 else None)
        if dopo:
            corpo = corpo[:primo_a_capo + dopo.start()]
        titolo = corpo.splitlines()[0].lstrip("#").strip()
        if rx_escludi and re.search(rx_escludi, titolo):
            continue
        out.append((titolo, corpo))
    return out


def chiave_scena(titolo: str) -> str:
    """«SCENA 5 — La notte…» → «SCENA 5»; altrimenti il titolo intero."""
    m = re.match(r"(SCENA\s+\d+)", titolo, re.I)
    return m.group(1).upper() if m else titolo


def nomi_schede(testi: "list[str]") -> "list[str]":
    """Le intestazioni delle schede d'entrata, normalizzate, più la prima
    colonna delle tabelle di cast (per gli stand-alone)."""
    out = []
    for t in testi:
        out += [norm(m.group(1).split(",")[0]) for m in _SCHEDA.finditer(t)]
    return out


def righe_cast(testi: "list[str]") -> "list[str]":
    """I nomi di un foglio del cast: la prima cella di ogni riga di tabella, e
    ogni cella in grassetto (il Drappo mette un simbolo nella prima colonna e
    il nome nella seconda)."""
    out = []
    for t in testi:
        for riga in t.splitlines():
            if not riga.startswith("|") or re.match(r"^\|\s*:?-", riga):
                continue
            celle = riga.strip("|").split("|")
            if celle and celle[0].strip():
                out.append(norm(celle[0]))
            out += [norm(g) for c in celle for g in re.findall(r"\*\*([^*]+)\*\*", c)]
    return [c for c in out if len(c) > 2]


def coperto(voce: str, candidati: "list[str]") -> bool:
    v = norm(voce)
    if not v:
        return True
    return any(v in c or (c and c in v) for c in candidati)


def comparse(corpo: str) -> "list[str]":
    """Prima colonna delle tabelle che seguono `**Comparse**` nella scena."""
    out = []
    for m in re.finditer(r"^\*\*Comparse\*\*.*$", corpo, re.M):
        for riga in corpo[m.end():].lstrip("\n").splitlines():
            if not riga.startswith("|"):
                if out or riga.strip():
                    break
                continue
            if re.match(r"^\|\s*:?-", riga):
                continue
            out.append(norm(riga.strip("|").split("|")[0]))
    return out


def etichette_box(corpo: str) -> "list[str]":
    out = []
    for box in mc.box_read_aloud(corpo):
        m = _ETICHETTA_BOX.search(box[0])
        if m:
            out.append(norm(m.group(1)))
    return out


def analizza(testo: str, profilo: dict, schede_extra: "list[str]") -> "list[tuple[str, str, str]]":
    """Rilievi come (regola, scena, voce)."""
    testo = pulisci(testo)
    rilievi = []
    fonti_schede = [testo] + schede_extra
    schede = nomi_schede(fonti_schede)
    # Una comparsa si descrive dove la si incontra la prima volta, e vale per
    # le scene dopo: come la scheda d'entrata, si cerca in tutto il modulo.
    compar = comparse(testo)
    cast = righe_cast(schede_extra) if profilo.get("cast") else []
    elenco = schede + cast

    for titolo, corpo in scene(testo, profilo.get("scena", SCENA_DEF), profilo.get("escludi")):
        k = chiave_scena(titolo)
        if "C1" in profilo["regole"] and not mc.box_read_aloud(corpo):
            rilievi.append(("C1", k, "nessun box read-aloud"))

        parlanti = {m.group(1).strip() for m in _BATTUTA.finditer(corpo)}
        if "C2" in profilo["regole"]:
            for p in sorted(parlanti):
                if not coperto(p, elenco):
                    rilievi.append(("C2", k, p))

        if not profilo.get("contratto"):
            continue
        m = _CONTRATTO.search(corpo)
        if not m:
            rilievi.append(("C3", k, "manca la riga **In scena**"))
            continue
        labels = etichette_box(corpo)
        for luogo in voci(m.group("dove")):
            if not coperto(luogo, labels):
                rilievi.append(("C3", k, f"Dove: {luogo} — nessun box con quel luogo nell'etichetta"))
        chi = voci(m.group("chi"))
        for persona in chi:
            if not coperto(persona, elenco + compar):
                rilievi.append(("C3", k, f"Chi: {persona} — né scheda d'entrata né riga fra le Comparse"))
        chi_n = [norm(c) for c in chi]
        for s in nomi_schede([corpo]) + [norm(p) for p in parlanti]:
            if not coperto(s, chi_n):
                rilievi.append(("C4", k, s))
    return rilievi


def carica_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def moduli(cfg: dict) -> "list[dict]":
    """I profili dichiarati, più ogni master DEF non dichiarato col profilo severo."""
    dichiarati = {m["file"] for m in cfg["moduli"]}
    out = list(cfg["moduli"])
    for f in sorted(ROOT.glob(f"**/{GLOB_MASTER}")):
        rel = f.relative_to(ROOT).as_posix()
        if any(p in rel for p in ("_ARCHIVIO/", "build/", ".claude/")) or rel in dichiarati:
            continue
        out.append({"file": rel, "regole": ["C1", "C2"], "contratto": True,
                    "nota": "master non dichiarato: profilo severo"})
    return out


def esegui(cfg: dict) -> "tuple[list, list, list]":
    trovati = []
    for mod in moduli(cfg):
        f = ROOT / mod["file"]
        if not f.exists():
            trovati.append((mod["file"], "C0", "—", "file dichiarato e assente"))
            continue
        extra = [pulisci((ROOT / s).read_text(encoding="utf-8")) for s in mod.get("schede_in", [])]
        for r, k, v in analizza(f.read_text(encoding="utf-8"), mod, extra):
            trovati.append((mod["file"], r, k, v))
    residui = cfg.get("residui", [])
    def dichiarato(t):
        return any(t[0] == r["file"] and t[1] == r["regola"] and t[2] == r["scena"]
                   and norm(r["voce"]) == norm(t[3]) for r in residui)
    nuovi = [t for t in trovati if not dichiarato(t)]
    scaduti = [r for r in residui
               if not any(t[0] == r["file"] and t[1] == r["regola"] and t[2] == r["scena"]
                          and norm(r["voce"]) == norm(t[3]) for t in trovati)]
    return trovati, nuovi, scaduti


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="cancello CI")
    ap.add_argument("--file", help="analizza un file qualunque (niente residui)")
    ap.add_argument("--contratto", action="store_true", help="con --file: applica anche C3/C4")
    a = ap.parse_args()

    if a.file:
        prof = {"regole": ["C1", "C2"], "contratto": a.contratto}
        ril = analizza(Path(a.file).read_text(encoding="utf-8"), prof, [])
        for r, k, v in ril:
            print(f"  {r} · {k} · {v}")
        print(f"{len(ril)} rilievi")
        return 0

    cfg = carica_config()
    trovati, nuovi, scaduti = esegui(cfg)
    if not a.check:
        per_file: "dict[str, list]" = {}
        for t in trovati:
            per_file.setdefault(t[0], []).append(t)
        for mod in moduli(cfg):
            ril = per_file.get(mod["file"], [])
            stato = "contratto" if mod.get("contratto") else "senza contratto"
            print(f"\n{mod['file']}  [{stato}] — {len(ril)} rilievi")
            for _, r, k, v in ril:
                seg = "   " if (mod["file"], r, k, v) not in nuovi else " ✗ "
                print(f"{seg}{r} · {k} · {v}")
    for t in nuovi:
        print(f"✗ {t[0]}: {t[1]} · {t[2]} · {t[3]}")
    for r in scaduti:
        print(f"✗ residuo scaduto, va tolto da {CONFIG.relative_to(ROOT)}: "
              f"{r['file']} {r['regola']} · {r['scena']} · {r['voce']}")
    if nuovi or scaduti:
        print(f"✗ copertura_scene: {len(nuovi)} rilievi non dichiarati, {len(scaduti)} residui scaduti")
        return 1 if a.check else 0
    print(f"✓ copertura_scene: {len(trovati)} rilievi, tutti dichiarati con la ragione")
    return 0


if __name__ == "__main__":
    sys.exit(main())
