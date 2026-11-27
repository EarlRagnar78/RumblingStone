#!/usr/bin/env python3
"""misura_mappe_schede.py — le pedine delle mappe contro le schede (in prova).

Giro di lettura del 2026-11-10: sulla pianta le pedine non dicono quale
scheda sono, quindi nessuno controlla se nello scontro esce la variante
giusta della creatura né se una creatura Grande occupa i suoi quadretti.

Ogni unità di una mappa JSON può dichiarare `scheda`: il file che contiene
il recinto `statblocco`, e dopo `#` il nome della scheda se il file ne ha
più di una. Da lì si misurano:

- **collegate**: unità nemiche con nome proprio che dichiarano la scheda;
- **rotte**: `scheda` che non porta a nessun recinto;
- **taglie_discordi**: la scheda dice Grande o più e la mappa, in quella
  cella, non lo dichiara in `taglie` (o dichiara un'altra taglia). È da
  `taglie` che il collaudo sa se la creatura passa dalle porte;
- **senza_scala**: mappe senza `scale_m_per_square`.

## Uso

    python3 scripts/misura_mappe_schede.py               # tabella
    python3 scripts/misura_mappe_schede.py --proponi     # collegamenti certi, da nome o da id fra parentesi
    python3 scripts/misura_mappe_schede.py --scrivi      # li scrive nei JSON, e allinea `taglie`
    python3 scripts/misura_mappe_schede.py --check       # avvisa se una misura peggiora (non ferma)
    python3 scripts/misura_mappe_schede.py --aggiorna    # riscrive docs/audit/mappe-schede.json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import statblock as S  # noqa: E402

REGISTRO = ROOT / "docs" / "audit" / "mappe-schede.json"
GRANDI = ("Grande", "Enorme", "Mastodontica", "Colossale")
#: I nomi di legenda: dicono che cosa vuol dire il simbolo, non chi c'è.
GENERICI = re.compile(r"^(PG\b|I PG\b|I quattro PG|Nemico standard|Boss / comandante|Incantatore nemico|"
                      r"Creatura speciale|Creatura evocata)", re.I)
ALLEATI = ("🔵",)
MISURE = ("collegate", "nominate", "rotte", "taglie_discordi", "senza_scala")


def _file(schema: str) -> list[str]:
    return [n for n in subprocess.run(["git", "ls-files", "-z", schema], cwd=ROOT, capture_output=True,
                                      text=True, check=True).stdout.split("\0") if n]


def mappe() -> list[Path]:
    fuori = []
    for n in _file("*.json"):
        if "/Mappe/" not in n and "/mappe/" not in n:
            continue
        try:
            d = json.loads((ROOT / n).read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(d, dict) and "units" in d and "map_size" in d:
            fuori.append(ROOT / n)
    return fuori


def _piano(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def indice_schede() -> dict[str, list[tuple[str, S.Statblocco]]]:
    """file → [(nome, scheda)]. Solo i recinti dei file seguiti da git."""
    indice: dict[str, list] = {}
    for n in _file("*.md"):
        # le copie dei booklet (homebrew/) ripetono le schede dei master
        if n.endswith(".hb.md") or "_ARCHIVIO" in n or "/homebrew/" in n \
                or n.startswith(("plans/", "docs/", "skills/")):
            continue
        righe = (ROOT / n).read_text(encoding="utf-8").split("\n")
        i = 0
        while i < len(righe):
            if righe[i].strip() != S.APERTURA:
                i += 1
                continue
            j = next((k for k in range(i + 1, len(righe)) if righe[k].strip() == S.CHIUSURA), None)
            if j is None:
                break
            sb = S.leggi("\n".join(righe[i:j + 1]))
            if sb:
                # nel Bestiario il nome sta nel titolo del file, non nel recinto
                titolo = next((r.lstrip("# ").strip() for r in righe if r.startswith("# ")), Path(n).stem)
                indice.setdefault(n, []).append((sb.nome or titolo, sb))
            i = j + 1
    return indice


def risolvi(scheda: str, indice: dict) -> S.Statblocco | None:
    percorso, _, nome = scheda.partition("#")
    voci = indice.get(percorso.strip(), [])
    if not voci:
        return None
    if nome.strip():
        return next((sb for n, sb in voci if _piano(n) == _piano(nome)), None)
    return voci[0][1] if len(voci) == 1 else None


def proposta(unita: dict, mappa: Path, indice: dict) -> str | None:
    """Un collegamento solo se è certo: l'id del Bestiario fra parentesi, o il
    nome intero di una scheda che apre il nome dell'unità ed è l'unico così.
    A parità si preferisce la scheda dello stesso modulo della mappa."""
    nome = unita.get("name", "")
    for m in re.finditer(r"\(([a-z0-9][a-z0-9-]{4,})\)", nome):
        trovati = [f for f in indice if Path(f).stem == m.group(1)]
        if len(trovati) == 1:
            return trovati[0]
    piano = _piano(nome)
    # la cartella del modulo: quella che contiene «Mappe»
    parti = mappa.relative_to(ROOT).parts
    taglio = next((i for i, x in enumerate(parti) if x.lower() == "mappe"), 1)
    modulo = "/".join(parti[:taglio]) + "/"
    candidati = []
    for f, voci in indice.items():
        for n, _ in voci:
            # senza il numero fra parentesi e le qualifiche dopo la virgola
            chiave = _piano(re.sub(r"\(.*?\)", "", n).split(",")[0])
            if len(chiave) < 6:
                continue
            if piano == chiave or piano.startswith(chiave + " "):
                candidati.append((len(chiave), f, n, len(voci)))
            elif f.startswith(modulo) and chiave.startswith(piano + " ") and len(piano) >= 6:
                # «Chuul avanzato» sulla pianta, «Chuul avanzato a 17 DV» nel modulo
                candidati.append((len(piano), f, n, len(voci)))
    if not candidati:
        return None
    candidati = [c for c in candidati if c[1].startswith((modulo, "Bestiario/"))]
    if not candidati:
        return None
    lungo = max(c[0] for c in candidati)
    migliori = [c for c in candidati if c[0] == lungo]
    # mai la scheda di un altro modulo: stesso modulo, poi il Bestiario
    vicini = [c for c in migliori if c[1].startswith(modulo)] \
        or [c for c in migliori if c[1].startswith("Bestiario/")]
    if not vicini:
        return None
    if len({(c[1], c[2]) for c in vicini}) != 1:
        return None
    _, f, n, quante = vicini[0]
    return f if quante == 1 else f"{f}#{n}"


def misura(mappa: Path, indice: dict) -> dict:
    d = json.loads(mappa.read_text(encoding="utf-8"))
    taglie = {tuple(t["at"]): t["taglia"] for t in d.get("taglie", [])}
    nominate = collegate = 0
    rotte, discordi, da_collegare = [], [], []
    for u in d.get("units", []):
        nome = u.get("name", "")
        if not nome or GENERICI.match(nome):
            continue
        nemica = u.get("token") not in ALLEATI
        if "scheda" not in u:
            if nemica:
                nominate += 1
                da_collegare.append(nome[:60])
            continue
        nominate += nemica
        sb = risolvi(u["scheda"], indice)
        if sb is None:
            rotte.append((nome[:50], u["scheda"]))
            continue
        collegate += nemica
        taglia = S.taglia_canonica(sb.taglia or "")
        if "at" in u:
            sulla_mappa = taglie.get(tuple(u["at"]))
            if taglia in GRANDI and sulla_mappa != taglia:
                discordi.append((nome[:50], f"scheda {taglia}, mappa {sulla_mappa or 'non dichiarata'}"))
            elif taglia not in GRANDI and sulla_mappa:
                discordi.append((nome[:50], f"scheda {taglia or '—'}, mappa {sulla_mappa}"))
    return {"nominate": nominate, "collegate": collegate, "rotte": len(rotte),
            "taglie_discordi": len(discordi), "senza_scala": int("scale_m_per_square" not in d),
            "dettaglio": {"rotte": rotte, "taglie_discordi": discordi, "da_collegare": da_collegare}}


def nei_booklet(indice: dict) -> dict[str, list[tuple[str, str]]]:
    """Per ogni booklet, le unità delle mappe che stampa la cui scheda non c'è.

    Giro del 2026-11-10: nel duello usciva la scheda di un altro drago, e
    guardie e sacerdote della tenda non avevano scheda affatto. Una mappa è
    «stampata» se il sorgente del booklet ne include la pianta; la scheda
    «c'è» se il suo nome compare nel sorgente."""
    import export_booklet_typst as ex
    import misura_statblocchi_booklet as msb
    per_mappa = {}
    for m in mappe():
        d = json.loads(m.read_text(encoding="utf-8"))
        per_mappa[m.stem] = [(u["name"], u["scheda"]) for u in d.get("units", []) if "scheda" in u]
    fuori: dict[str, list] = {}
    for mp in msb.manifesti():
        man = json.loads(mp.read_text(encoding="utf-8"))
        if "chapters" not in man:
            continue
        grezzo = ex.sorgente(man, mp.parent, True, formato=man.get("formato", "a4"))
        piano = _piano(grezzo)
        mancano = []
        for stem, unita in per_mappa.items():
            if f"{stem}_map" not in grezzo:
                continue
            for nome, scheda in unita:
                voci = indice.get(scheda.partition("#")[0], [])
                titolo = scheda.partition("#")[2] or (voci[0][0] if voci else "")
                chiave = _piano(re.sub(r"\(.*?\)", "", titolo).split(",")[0])
                if chiave and chiave not in piano:
                    mancano.append((stem, nome[:50]))
        fuori[mp.relative_to(ROOT).as_posix()] = mancano
    return fuori


def scrivi(mappa: Path, indice: dict) -> tuple[int, int]:
    """Aggiunge i collegamenti certi e porta `taglie` alla taglia della scheda."""
    testo = mappa.read_text(encoding="utf-8")
    d = json.loads(testo)
    # Si riscrive il JSON solo se torna identico a com'era: una mappa scritta
    # con un'altra forma non deve cambiare in ogni riga per un campo in più.
    fedele = json.dumps(d, ensure_ascii=False, indent=2) + "\n" == testo
    righe = testo.split("\n")
    viste: dict[str, int] = {}
    nuovi = taglie_nuove = 0
    for u in d.get("units", []):
        viste[u.get("name", "")] = viste.get(u.get("name", ""), 0) + 1
        nome = u.get("name", "")
        if not nome or GENERICI.match(nome):
            continue
        if "scheda" not in u and (p := proposta(u, mappa, indice)):
            u["scheda"] = p
            nuovi += 1
            if not fedele:
                # la riga del nome di QUESTA unità: l'ennesima con quel nome
                chiave = '"name": ' + json.dumps(nome, ensure_ascii=False)
                dove = [i for i, r in enumerate(righe) if r.strip().rstrip(",") == chiave][viste[nome] - 1]
                rientro = righe[dove][:len(righe[dove]) - len(righe[dove].lstrip())]
                if not righe[dove].rstrip().endswith(","):
                    righe[dove] = righe[dove].rstrip() + ","
                    righe.insert(dove + 1, f'{rientro}"scheda": {json.dumps(p, ensure_ascii=False)}')
                else:
                    righe.insert(dove + 1, f'{rientro}"scheda": {json.dumps(p, ensure_ascii=False)},')
        sb = risolvi(u["scheda"], indice) if "scheda" in u else None
        if sb is None or "at" not in u:
            continue
        taglia = S.taglia_canonica(sb.taglia or "")
        voci = d.setdefault("taglie", []) if taglia in GRANDI else d.get("taglie", [])
        qui = next((t for t in voci if list(t["at"]) == list(u["at"])), None)
        if not fedele:
            continue        # `taglie` di una mappa in altra forma: resta discorde, si corregge a mano
        if taglia in GRANDI and qui is None:
            voci.append({"at": list(u["at"]), "taglia": taglia})
            taglie_nuove += 1
        elif taglia in GRANDI and qui["taglia"] != taglia:
            qui["taglia"] = taglia
            taglie_nuove += 1
    if fedele and (nuovi or taglie_nuove):
        mappa.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif nuovi:
        mappa.write_text("\n".join(righe), encoding="utf-8")
        json.loads(mappa.read_text(encoding="utf-8"))        # resta JSON valido
    return nuovi, taglie_nuove


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--proponi", action="store_true")
    ap.add_argument("--scrivi", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--aggiorna", action="store_true")
    ap.add_argument("--dettaglio", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--booklet", action="store_true",
                    help="per ogni booklet, le unità delle mappe stampate la cui scheda non è nel booklet")
    a = ap.parse_args(argv)
    indice = indice_schede()
    tutte = mappe()
    if a.proponi or a.scrivi:
        for m in tutte:
            if a.scrivi:
                n, t = scrivi(m, indice)
                if n or t:
                    print(f"{m.relative_to(ROOT)}: {n} collegamenti, {t} taglie")
            else:
                d = json.loads(m.read_text(encoding="utf-8"))
                for u in d.get("units", []):
                    if u.get("name") and "scheda" not in u and not GENERICI.match(u["name"]) \
                            and (p := proposta(u, m, indice)):
                        print(f"{m.name}: «{u['name'][:50]}» → {p}")
        if not a.scrivi:
            return 0
    if a.booklet:
        fuori = nei_booklet(indice)
        for nome, mancano in fuori.items():
            if mancano or a.dettaglio:
                print(f"{Path(nome).name}: {len(mancano)} unità senza scheda nel booklet")
            for stem, unita in mancano:
                print(f"    {stem}: {unita}")
        print(f"{len(fuori)} booklet · unità delle mappe stampate senza scheda nel booklet: "
              f"{sum(len(v) for v in fuori.values())}")
        return 0
    risultati = {m.relative_to(ROOT).as_posix(): misura(m, indice) for m in tutte}
    totale = {k: sum(v[k] for v in risultati.values()) for k in MISURE}
    if a.json:
        print(json.dumps({"totale": totale, "mappe": risultati}, ensure_ascii=False, indent=2))
        return 0
    if a.aggiorna:
        REGISTRO.write_text(json.dumps({
            "_cos_e": "Le pedine delle mappe contro le schede (scripts/misura_mappe_schede.py). In prova: "
                      "--check avvisa se «collegate» scende o le altre salgono, senza fermare.",
            "totale": totale,
            "mappe": {n: {k: v[k] for k in MISURE} for n, v in sorted(risultati.items())},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✓ registro riscritto in {REGISTRO.relative_to(ROOT)}")
        return 0
    print(f"{len(tutte)} mappe · unità nemiche con nome proprio {totale['nominate']} · collegate a una scheda "
          f"{totale['collegate']} · collegamenti rotti {totale['rotte']} · taglie discordi "
          f"{totale['taglie_discordi']} · mappe senza scala {totale['senza_scala']}")
    if a.dettaglio:
        for n, v in risultati.items():
            for chiave in ("rotte", "taglie_discordi"):
                for voce in v["dettaglio"][chiave]:
                    print(f"  {Path(n).name}: {chiave}: {voce}")
    if a.check and REGISTRO.is_file():
        prima = json.loads(REGISTRO.read_text(encoding="utf-8"))["totale"]
        peggio = [f"{k} = {totale[k]}, era {prima[k]}" for k in ("rotte", "taglie_discordi", "senza_scala")
                  if totale[k] > prima.get(k, 0)]
        if totale["collegate"] < prima.get("collegate", 0):
            peggio.append(f"collegate = {totale['collegate']}, erano {prima['collegate']}")
        for riga in peggio:
            print(f"⚠ {riga} (in prova, non ferma)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
