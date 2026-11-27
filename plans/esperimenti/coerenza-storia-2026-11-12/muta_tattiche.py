#!/usr/bin/env python3
"""muta_tattiche.py — banco di mutanti per la regola S8 (tattiche contro la scheda).

Per ogni scheda del Bestiario che S8 legge (una scheda sola nel file, con le
«Tattiche») costruisce quattro famiglie di mutanti, uno alla volta, su una copia:

  tolto      la scheda perde un incantesimo o un talento che la tattica usa
             (il nome sparisce da ogni riga fuori dalle «Tattiche»)      → va visto
  cambiato   la tattica usa un incantesimo (in corsivo) o un talento (con le
             maiuscole) che la scheda non ha                             → va visto
  parafrasi  lo stesso intruso, scritto come lo scriverebbe un autore di
             fretta: l'incantesimo senza corsivo, il talento in minuscolo
             (di più parole, e di una parola sola)                       → si misura il limite
  controllo  la tattica cambia un incantesimo con un altro che la scheda ha
                                                                         → non va segnalato

Uso: python3 muta_tattiche.py OUT.json
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import coerenza_campagna as cc  # noqa: E402
import lessico_regole as LR  # noqa: E402
import verifica_scheda as VS  # noqa: E402
import verifica_talenti as VT  # noqa: E402

# intrusi: incantesimi e talenti dell'SRD che nessun gregario del Bestiario ha per caso
INC = ["fermare il tempo", "desiderio", "sciame di meteore", "parola del potere uccidere",
       "disintegrazione", "catena di fulmini", "muro di ferro", "dito della morte"]
TAL = ["Tiro Multiplo", "Deviare Frecce", "Critico Migliorato", "Combattere con Due Armi",
       "Maestria in Combattimento", "Attacco Turbinante", "Pugno Stordente", "Tiro Preciso"]
TAL1 = ["Mobilità", "Fendere", "Robustezza", "Atletico", "Acrobatico"]


def _giudica(testo: str, nome: str, cartella: Path) -> list[dict]:
    q = cartella / nome
    q.write_text(testo, encoding="utf-8")
    return cc.verifica_tattiche([q])["violazioni"]


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else QUI / "misure" / "mutanti-tattiche.json"
    esiti: list[dict] = []
    base = cc.verifica_tattiche(cc.schede_con_tattiche())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for p in cc.schede_con_tattiche():
            testo = p.read_text(encoding="utf-8", errors="replace")
            righe = testo.splitlines()
            f = VS.fatti(p)
            if not f["tattiche"] or len(f["blocchi"]) > 1:
                continue
            sis = f["sistema"]
            if sis != "dnd35":
                continue                      # gli intrusi sono nomi italiani del 3.5
            dentro = {n for t in f["tattiche"] for n in range(t["inizio"], t["fine"] + 1)}
            nomi = VS._liste(sis)[2]
            it = VS._incantesimi_it()
            rel = cc._rel(p)

            def segna(famiglia, cosa, nuovo, atteso_visto, _rel=rel, _p=p):
                v = _giudica(nuovo, _p.name, tmp)
                esiti.append({"file": _rel, "famiglia": famiglia, "cosa": cosa,
                              "visto": bool(v), "atteso": atteso_visto})

            # le menzioni che S8 legge in questa scheda
            inc_m, tal_m = [], []
            for n in sorted(dentro):
                r = cc._S8_TOGLI.sub("", righe[n - 1])
                if r.lstrip().startswith(">"):
                    continue
                for m in cc._S8_CORSIVO.finditer(r):
                    nome = m.group(1).strip(" .,;:")
                    k = LR.norma(nome)
                    k = LR.norma(it[k]) if k in it else k
                    if k in nomi and not cc._S8_ALTRUI.search(r[:m.start()]) and not cc._S8_CONDIVISI.search(r) \
                            and nome not in [x[0] for x in inc_m]:
                        inc_m.append((nome, nomi[k], n))
                for m in cc._S8_MAIUSCOLE.finditer(r.replace("*", "")):
                    x = VT.risolvi(sis, m.group(0))
                    if x and (" " in m.group(0) or x["verificabile"]) and m.group(0) not in [y[0] for y in tal_m]:
                        tal_m.append((m.group(0), x["en"], n))

            # tolto: il nome (italiano e canonico) sparisce fuori dalle Tattiche
            for nome, en, _n in inc_m + tal_m:
                pat = re.compile("|".join(re.escape(x) for x in {nome, en}), re.I)
                nuove = [r if i in dentro else pat.sub("—", r) for i, r in enumerate(righe, 1)]
                if nuove != righe:
                    segna("tolto", nome, "\n".join(nuove) + "\n", True)

            piatto = cc._piatto(testo)
            intruso_i = next((x for x in INC if cc._piatto(x) not in piatto), None)
            intruso_t = next((x for x in TAL if cc._piatto(x) not in piatto), None)
            intruso_1 = next((x for x in TAL1 if cc._piatto(x) not in piatto), None)
            n0 = min(dentro)
            def aggiungi(famiglia, cosa, frase):
                nuove = list(righe)
                nuove[n0 - 1] += frase
                segna(famiglia, cosa, "\n".join(nuove) + "\n", True)

            if intruso_i:
                for famiglia, forma in (("cambiato", "*{}*"), ("parafrasi: incantesimo senza corsivo", "{}")):
                    if inc_m:
                        nome, _en, n = inc_m[0]
                        nuove = list(righe)
                        nuove[n - 1] = nuove[n - 1].replace(f"*{nome}*", forma.format(intruso_i), 1)
                        segna(famiglia, f"incantesimo: {nome} → {intruso_i}", "\n".join(nuove) + "\n", True)
                    else:
                        aggiungi(famiglia, f"incantesimo: + {intruso_i}", " Apre con " + forma.format(intruso_i) + ".")
            if intruso_t:
                aggiungi("cambiato", f"talento: + {intruso_t}", f" Poi usa {intruso_t} sul bersaglio più vicino.")
                aggiungi("parafrasi: talento di più parole in minuscolo", f"talento: + {intruso_t.lower()}",
                         f" Poi usa {intruso_t.lower()} sul bersaglio più vicino.")
            if intruso_1:
                aggiungi("cambiato", f"talento: + {intruso_1}", f" Poi usa {intruso_1} sul bersaglio più vicino.")
                aggiungi("parafrasi: talento di una parola in minuscolo", f"talento: + {intruso_1.lower()}",
                         f" Poi usa {intruso_1.lower()} sul bersaglio più vicino.")

            # controllo: uno scambio fra due incantesimi che la scheda ha
            if len(inc_m) >= 2:
                (a, _ea, na), (b, _eb, _nb) = inc_m[0], inc_m[1]
                nuove = list(righe)
                nuove[na - 1] = nuove[na - 1].replace(f"*{a}*", f"*{b}*", 1)
                segna("controllo", f"{a} → {b}", "\n".join(nuove) + "\n", False)

    def conta(fam):
        x = [e for e in esiti if e["famiglia"] == fam]
        return {"mutanti": len(x), "visti": sum(e["visto"] for e in x)}
    riassunto = {"main": {"violazioni": len(base["violazioni"]), **base["letti"],
                          "non_verificabili": base["non_verificabili"]},
                 **{fam: conta(fam) for fam in dict.fromkeys(e["famiglia"] for e in esiti)}}
    out.write_text(json.dumps({"riassunto": riassunto, "esiti": esiti}, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(json.dumps(riassunto, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
