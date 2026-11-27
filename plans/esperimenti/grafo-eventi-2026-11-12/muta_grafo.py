#!/usr/bin/env python3
"""muta_grafo.py — mutanti di «chi sa cosa» e di origine dei fatti, tutti in una copia degli archi.

Ogni mutante è UNA riga falsa in un file diverso (così i numeri di riga non si
spostano a vicenda), scritta in due forme: piana (le parole chiave del grafo, un
solo PNG, un verbo di conoscenza) e parafrasi (come la scriverebbe un autore).
Per ognuno si conosce la regola attesa (T0, T1, T1 per catena, T3).

Uso
  python3 muta_grafo.py prepara CARTELLA     # copia gli archi e inserisce i mutanti
  python3 muta_grafo.py valuta CARTELLA VIOLAZIONI.json [--etichetta NOME]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import grafo  # noqa: E402

A7, A8, A9 = grafo.ARCHI
# (id, regola attesa, forma, file, riga)
MUTANTI = [
    ("T0-p1", "T0", "piana", f"{A7}/APPARATO-ARC07-DEF-2-RITORNO-E-AFFRESCHI.md",
     "Il gruppo, ormai per tutti i Custodi Eterni, attraversa la sala delle forge."),
    ("T0-p2", "T0", "piana", f"{A7}/APPARATO-ARC07-DEF-3-RESURREZIONE-HELLA.md",
     "I nani di guardia salutano i Custodi Eterni con l'ascia alzata."),
    ("T0-p3", "T0", "piana", f"{A8}/ARC08-03-REGISTRO-PERDITE.md",
     "Il Seme di Porta pulsa già dentro l'Orbe di Dauth."),
    ("T0-p4", "T0", "piana", f"{A8}/ARC08-00-INDICE.md",
     "Nei campi si parla del Seme di Porta estratto dall'Orbe."),
    ("T0-a1", "T0", "parafrasi", f"{A7}/ARC07-00-INDICE.md",
     "I nani li salutano col titolo che il re darà loro: guardiani per sempre di Hammerfist."),
    ("T0-a2", "T0", "parafrasi", f"{A7}/APPARATO-ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md",
     "Sulla porta della sala è già incisa la runa dei protettori eterni della rocca."),
    ("T0-a3", "T0", "parafrasi", f"{A8}/APPARATO-ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md",
     "Dall'Orbe delle Otto Porte qualcuno ha già ricavato il germe del varco planare."),
    ("T1-p1", "T1", "piana", f"{A8}/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md",
     "Sethrax sa già che l'Orbe genera un Seme di Porta."),
    ("T1-p2", "T1", "piana", f"{A7}/APPARATO-ARC07-DEF-5-RITORNO-HAMMERFIST.md",
     "Azarr Kul sa che i Custodi Eterni sono in marcia verso sud."),
    ("T1-p3", "T1", "piana", f"{A7}/APPARATO-ARC07-DEF-1-PIANO-TERRA-TERROS.md",
     "Re Thorek dice ai suoi consiglieri che sono i Custodi Eterni."),
    ("T1-p4", "T1", "piana", f"{A7}/ARC07-CONSEGUENZE-ECHI.md",
     "Ushgar sa che i Custodi Eterni viaggiano armati."),
    ("T1-a1", "T1", "parafrasi", f"{A8}/APPARATO-ARC08-DEF-2-TRE-GIORNI-DI-SANGUE.md",
     "Sethrax intuisce il germe planare che l'Orbe libererà al suo apice."),
    ("T1-a2", "T1", "parafrasi", f"{A7}/ARC07-DEF-1-PIANO-TERRA-TERROS.md",
     "Il generale della Mano Rossa ha già saputo che i quattro sono i protettori nominati dal re."),
    ("T1-a3", "T1", "parafrasi", f"{A7}/ARC07-DEF-2-RITORNO-E-AFFRESCHI.md",
     "Ghaurush ha capito chi sono i quattro eroi a cui il re darà il titolo."),
    ("R-p1", "T1", "piana", f"{A8}/ARC08-01-GUIDA-DM.md",
     "Zalkatar sa che il Seme di Porta è pronto."),
    ("R-p2", "T1", "piana", f"{A8}/ARC08-04-MARCIA-MANO-ROSSA.md",
     "Brenna sa che i Custodi Eterni hanno salvato Hammerfist."),
    ("R-a1", "T1", "parafrasi", f"{A8}/ARC08-11-PONTE-ARRIVO.md",
     "La mente della Torre ha già in pugno il segreto del varco nell'Orbe."),
    ("R-a2", "T1", "parafrasi", f"{A8}/ARC08-15-HANDOUTS-GIOCATORE.md",
     "La signora del porto ha già letto nei rapporti che i quattro sono stati nominati guardiani."),
    ("T3-p1", "T3", "piana", f"{A9}/Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md",
     "Sonjak sa che il gruppo ha tutte e tre le gemme."),
    ("T3-p2", "T3", "piana", f"{A9}/Arco-Post-Hammerfist-P3-Sabotaggio-Campi-Drow-TESTO.md",
     "Mira Serani scopre che Lorana è viva."),
    ("T3-p3", "T3", "piana", f"{A9}/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-EVENT-DECK.md",
     "Lorana scopre che sua figlia è stata uccisa e sostituita da un'aranea."),
    ("T3-p4", "T3", "piana", f"{A9}/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DM-MASTER-REFERENCE.md",
     "Sethrax conosce il piano d'invasione."),
    ("T3-a1", "T3", "parafrasi", f"{A9}/Arco-Post-Hammerfist-P3-Starsong-Hill-ALLEANZA-ELFI-TESTO.md",
     "Gli elfi di Witchwood accolgono i quattro col titolo nanico che già conoscono."),
    ("T3-a2", "T3", "parafrasi", f"{A9}/Arco-Post-Hammerfist-P2C-Salvatore-Mercante-TESTO.md",
     "Il Conte, nei suoi dispacci, parla già del diadema di adamantio che i quattro hanno recuperato."),
    ("T3-a3", "T3", "parafrasi", f"{A9}/Arco-Post-Hammerfist-P3-Sabotaggio-Campi-Drow-Upscale-CR12.md",
     "Zin'thara, informata dalle sue ragnatele, sa del diadema che il nano porta in testa."),
]


def prepara(dest: Path) -> list[dict]:
    if dest.exists():
        shutil.rmtree(dest)
    for a in grafo.ARCHI:
        shutil.copytree(grafo.REPO / a, dest / a)
    usati = set()
    out = []
    for mid, regola, forma, rel, testo in MUTANTI:
        assert rel not in usati, rel
        usati.add(rel)
        p = dest / rel
        righe = p.read_text(encoding="utf-8").splitlines()
        pos = next((i for i in range(5, len(righe)) if righe[i].strip() == "" and not
                    sum(1 for r in righe[:i] if r.lstrip().startswith("```")) % 2), len(righe))
        righe = righe[:pos + 1] + [testo, ""] + righe[pos + 1:]
        p.write_text("\n".join(righe) + "\n", encoding="utf-8")
        out.append({"id": mid, "regola": regola, "forma": forma, "file": rel, "riga": pos + 2, "testo": testo})
    (dest / "mutanti.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def valuta(dest: Path, viol: list[dict], etichetta: str) -> dict:
    mut = json.loads((dest / "mutanti.json").read_text(encoding="utf-8"))
    presi = {(v["regola"][:2], v["file"], v["riga"]) for v in viol}
    righe_mut = {(m["file"], m["riga"]) for m in mut}
    esiti = []
    for m in mut:
        esiti.append({**m, "preso": (m["regola"], m["file"], m["riga"]) in presi})
    altri = [v for v in viol if (v["file"], v["riga"]) not in righe_mut and v["file"] != "eventi.yaml"]
    tab = {}
    for e in esiti:
        k = f"{e['regola'] if not e['id'].startswith('R') else 'T1 catena'} {e['forma']}"
        a, b = tab.get(k, (0, 0))
        tab[k] = (a + e["preso"], b + 1)
    return {"etichetta": etichetta, "per_gruppo": {k: f"{a}/{b}" for k, (a, b) in sorted(tab.items())},
            "piana": f"{sum(e['preso'] for e in esiti if e['forma'] == 'piana')}/{sum(1 for e in esiti if e['forma'] == 'piana')}",
            "parafrasi": f"{sum(e['preso'] for e in esiti if e['forma'] == 'parafrasi')}/{sum(1 for e in esiti if e['forma'] == 'parafrasi')}",
            "rilievi_fuori_dai_mutanti": len(altri), "esiti": esiti}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepara")
    p.add_argument("dest", type=Path)
    v = sub.add_parser("valuta")
    v.add_argument("dest", type=Path)
    v.add_argument("violazioni", type=Path, nargs="+", help="più file = unione (estrattori integrati)")
    v.add_argument("--etichetta", default="regex")
    a = ap.parse_args(argv)
    if a.cmd == "prepara":
        for m in prepara(a.dest):
            print(m["id"], m["file"].split("/")[-1], m["riga"])
        return 0
    viol = [x for f in a.violazioni for x in json.loads(f.read_text(encoding="utf-8"))["violazioni"]]
    r = valuta(a.dest, viol, a.etichetta)
    print(json.dumps({k: v for k, v in r.items() if k != "esiti"}, ensure_ascii=False, indent=1))
    for e in r["esiti"]:
        print(f"  {'✓' if e['preso'] else '·'} {e['id']:<6} {e['testo'][:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
