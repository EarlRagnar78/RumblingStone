#!/usr/bin/env python3
"""misura_tabelle.py — quanto sono giuste le tabelle dei termini, fonte contro fonte.

Per ogni categoria confronta due fonti indipendenti sulle voci che hanno entrambe,
e conta le concordi e le discordi. Non usa la tabella per giudicare sé stessa:

- incantesimi 3.5: i nomi della tabella prima di Editori Folli (commit 3b6f7f1,
  coppie fatte da miniaturefantasy e Sigil, «doppia fonte») contro l'abbinamento
  per firma di ``abbinamenti/abbina_incantesimi.py`` sul PDF di Editori Folli,
  che non legge i nomi;
- equipaggiamento 3.5: il database bilingue di Mephit contro l'abbinamento per
  firma di ``abbinamenti/abbina_equip.py`` (costo, danni o CA, peso);
- casi del cancello: per ogni categoria almeno 30 nomi della tabella e 10 nomi
  sbagliati noti, passati a ``lessico_regole.controlla_campi``.

Uso (i file scaricati sono dati: si legge con ``python3 -I``)::

    python3 -I abbinamenti/abbina_incantesimi.py > /tmp/x/inc.json
    python3 -I abbinamenti/abbina_equip.py > /tmp/x/equip.json
    python3 -I misura_tabelle.py --incantesimi /tmp/x/inc.json \
        --equip /tmp/x/equip.json --mephit /tmp/x/mephit_test.sql
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

QUI = Path(__file__).resolve().parent
ROOT = QUI.parents[2]


def norma(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("’", "'"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def tabella(testo: str, tipo: str) -> list[list[str]]:
    righe = [r.split("\t") for r in testo.splitlines() if r and not r.startswith("#")]
    return [r for r in righe[1:] if len(r) >= 4 and r[2] == tipo]


def confronta(nome: str, a: dict[str, str], b: dict[str, str]) -> dict:
    """a, b: inglese normalizzato → italiano. Conta solo le voci che hanno tutte e due."""
    comuni = sorted(set(a) & set(b))
    discordi = [(k, a[k], b[k]) for k in comuni if norma(a[k]) != norma(b[k])]
    return {"categoria": nome, "comuni": len(comuni), "concordi": len(comuni) - len(discordi),
            "discordi": discordi}


def incantesimi(file_ef: Path) -> dict:
    prima = subprocess.run(["git", "-C", str(ROOT), "show", "3b6f7f1:scripts/lessico_it_35.tsv"],
                           capture_output=True, text=True, check=True).stdout
    nomi = {norma(r[1]): r[0] for r in tabella(prima, "incantesimo") if r[3] == "doppia fonte"}
    firma = {norma(en): it.capitalize() for it, en in json.loads(file_ef.read_text())["coppie"]}
    return confronta("incantesimo 3.5 (doppia fonte ↔ firma Editori Folli)", nomi, firma)


def equipaggiamento(file_ef: Path, sql: Path) -> dict:
    sys.path.insert(0, str(Path(sql).parent))
    testo = sql.read_text(encoding="utf-8", errors="replace")
    mephit = {}
    for t in ("srd35_weapon", "srd35_armor", "srd35_equipment"):
        m = re.search(r"CREATE TABLE `%s` \((.*?)\n\)" % t, testo, re.S)
        cols = re.findall(r"^\s+`([^`]+)`", m.group(1), re.M)
        for ins in re.finditer(r"INSERT INTO `%s`(?: \([^)]*\))? VALUES\s*(.*?\));\s*\n" % t, testo, re.S):
            for riga in re.findall(r"\((.*?)\)(?:,|;|$)", ins.group(1), re.S):
                campi = re.findall(r"'(?:[^'\\]|\\.|'')*'|NULL|[-0-9.]+", riga)
                if len(campi) != len(cols):
                    continue
                d = dict(zip(cols, [c.strip("'").replace("\\'", "'").replace("''", "'") for c in campi]))
                if d.get("name_en") and d.get("name_it"):
                    mephit[norma(d["name_en"])] = d["name_it"]
    firma = {}
    for parte in json.loads(file_ef.read_text()).values():
        for it, en in parte["coppie"]:
            firma[norma(en)] = it
    return confronta("equipaggiamento 3.5 (Mephit ↔ firma Editori Folli)", mephit, firma)


# Nomi che non sono nelle tabelle italiane 3.5 (5e, PF1e o inventati). La prima lista del 2026-11-07
# conteneva per errore cinque nomi veri (Acrobazia, Mantello elfico, Stivali della velocità e della rapidità, Amuleto
# dell'armatura naturale): il controllo li ha accettati, ed era giusto.
SBAGLIATI = {
    "incantesimo": ["fuoco fatuo", "palla infuocata", "dardo magico", "individuazione magico",
                    "rimuovere paura", "cura ferite lievissime", "scudo magico", "invisibilità superiore minore",
                    "teletrasporto avanzato", "fulmine globulare"],
    "abilità": ["Furtività", "Percezione", "Storia", "Atletica", "Intuizione", "Indagare",
                "Persuasione", "Sopravvivenza in natura", "Arcano", "Inganno"],
    "oggetto magico": ["Guanti della Forza dell'Orco", "Anello dell'invisibilità totale", "Mantello della protezione elfica",
                       "Stivali della corsa rapida", "Borsa conservante", "Bacchetta dei fulmini globulari",
                       "Cintura della forza del gigante di pietra", "Amuleto della corazza naturale",
                       "Anello di resistenza al fuoco totale", "Elmo della telepatia superiore"],
}


GRADI = ("greater", "lesser", "mass", "improved", "minor", "major")


def chiavi_en(en: str) -> list[str]:
    """«greater teleport» e «teleport, greater» sono la stessa voce."""
    e = norma(en)
    out = [e]
    for g in GRADI:
        if e.startswith(g + " "):
            out.append(f"{e[len(g) + 1:]} {g}")
        if e.endswith(" " + g):
            out.append(f"{g} {e[:-len(g) - 1]}")
    return out


def contro_tabella(nome: str, coppie: list, tipo: str) -> dict:
    """Coppie [italiano, inglese] di un'altra fonte contro le righe della tabella 3.5 del tipo."""
    t35 = (ROOT / "scripts/lessico_it_35.tsv").read_text(encoding="utf-8")
    per_en: dict[str, list[str]] = {}
    for r in tabella(t35, tipo):
        per_en.setdefault(norma(re.sub(r"\s*\((Ex|Su|Sp)\)", "", r[1])), []).append(r[0])
    comuni, discordi, fuori = 0, [], 0
    for it, en, *_ in coppie:
        righe = next((per_en[k] for k in chiavi_en(en) if k in per_en), None)
        if righe is None:
            fuori += 1
            continue
        comuni += 1
        if not any(norma(it) == norma(x) for x in righe):
            discordi.append((en, it, righe))
    return {"categoria": nome, "comuni": comuni, "concordi": comuni - len(discordi),
            "discordi": discordi, "non_in_tabella": fuori}


def casi_cancello(n: int = 30, seme: int = 20261107) -> list[dict]:
    """Per ogni categoria: n nomi presi dalla tabella (devono passare) e 10 sbagliati (non devono).

    «prima» = lo stesso controllo senza tabelle italiane, solo con l'indice delle fonti inglesi:
    è com'era prima di questo lotto, quando nessun nome italiano di questi tipi era controllato.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import lessico_regole as L  # noqa: E402
    import riscontro_srd as R  # noqa: E402

    idx = L.carica_indice(R.cartella_cache(None), rete=False)
    t35, tpf = L.tabelle_per_tipo()
    vuote = {k: {} for k in t35}
    rng = random.Random(seme)
    testo35 = (ROOT / "scripts/lessico_it_35.tsv").read_text(encoding="utf-8")
    esiti = []
    for tipo, campo in (("incantesimo", "Incantesimi"), ("abilità", "Abilità"),
                        ("oggetto magico", "Equipaggiamento")):
        nomi = sorted({r[0] for r in tabella(testo35, tipo) if not re.search(r"[,/()+]", r[0])})
        campione = rng.sample(nomi, min(n, len(nomi)))
        for nome, atteso in [(x, True) for x in campione] + [(x, False) for x in SBAGLIATI[tipo]]:
            riga = f"**{campo}**: {nome} +5\n" if tipo == "abilità" else f"**{campo}**: *{nome}*\n"
            dopo = L.controlla_campi(riga, idx, t35, tpf, "prova.md")
            prima = L.controlla_campi(riga, idx, vuote, tpf, "prova.md")
            ok = lambda es: bool(es) and all(e["esito"] in ("tabella", "fonte") for e in es)
            esiti.append({"tipo": tipo, "nome": nome, "atteso": atteso,
                          "dopo": ok(dopo) == atteso, "prima": ok(prima) == atteso, "letto": bool(dopo)})
    return esiti


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--incantesimi", type=Path)
    ap.add_argument("--equip", type=Path)
    ap.add_argument("--mephit", type=Path)
    ap.add_argument("--coppie", action="append", default=[], metavar="NOME:TIPO:FILE",
                    help="coppie [italiano, inglese] di un'altra fonte, contro la tabella 3.5 del tipo")
    ap.add_argument("--uscita", type=Path, default=QUI / "misura-tabelle.json")
    a = ap.parse_args(argv)
    out = {"confronti": [], "casi": []}
    if a.incantesimi:
        out["confronti"].append(incantesimi(a.incantesimi))
    if a.equip and a.mephit:
        out["confronti"].append(equipaggiamento(a.equip, a.mephit))
    for spec in a.coppie:
        nome, tipo, file = spec.split(":", 2)
        out["confronti"].append(contro_tabella(nome, json.loads(Path(file).read_text(encoding="utf-8")), tipo))
    for c in out["confronti"]:
        print(f"{c['categoria']}: {c['concordi']}/{c['comuni']} concordi, {len(c['discordi'])} discordi")
    out["casi"] = casi_cancello()
    for tipo in sorted({e["tipo"] for e in out["casi"]}):
        es = [e for e in out["casi"] if e["tipo"] == tipo]
        print(f"cancello {tipo}: prima {sum(e['prima'] for e in es)}/{len(es)}, "
              f"dopo {sum(e['dopo'] for e in es)}/{len(es)} (letti {sum(e['letto'] for e in es)})")
    a.uscita.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
