#!/usr/bin/env python3
"""Banco del lotto 8 (ADR-0126): un oggetto troppo caro aggiunto apposta.

A ogni scheda del Bestiario che il verificatore legge, con un blocco solo e
coi dadi vita scritti, si aggiunge in fondo una riga «Equipaggiamento» con un
*anello di protezione +5* e un *mantello della resistenza +5* (75.000 mo), che
supera il valore di un PNG fino al 15° livello. La copia conta come trovata se
compare una violazione `equipaggiamento.valore`, come non verificabile se la
razza non ha un modificatore di livello noto o il livello passa il 20°. Le
schede dal 16° livello effettivo in su non si possono giudicare con questa
aggiunta e si contano a parte.

Seconda prova (lotto 8, seconda parte): uno «spadone +3 sacrilego» e sei pozioni
di cura ferite gravi (54.500 mo; col solo potenziamento 18.000). Conta le sole
violazioni: misura quanto pesa leggere le capacità speciali e le pozioni.

Terza prova (lotto 8, terza parte): un'armatura completa +1 di adamantio, un'ascia
bipenne di adamantio e un bastone del fuoco con 40 cariche (33.200 mo; senza
materiali e bastoni 1.000). Conta le sole violazioni.

Quarta prova (lotto 8, quarta parte, ADR-0134): gli stessi oggetti della prima scritti
nella forma di ADR-0091, dentro la riga delle Statistiche e nelle due voci «Equipaggiamento
da combattimento» e «Altro equipaggiamento». Conta le sole violazioni: misura se la
verifica legge l'equipaggiamento dove le schede lo scrivono.

Uso: python3 muta_ricchezza.py  (scrive misure-ricchezza.json accanto)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

AGGIUNTA = "\n\n**Equipaggiamento** *anello di protezione +5*, *mantello della resistenza +5*\n"
#: seconda prova (lotto 8, seconda parte): un'arma il cui prezzo sta quasi tutto nella capacità speciale
#: (+3 sacrilega = +5, 50.000 mo; il solo +3 ne vale 18.000) e sei pozioni
SPECIALE = "\n\n**Equipaggiamento** spadone +3 sacrilego, 6 pozioni di *cura ferite gravi*\n"
#: terza prova (lotto 8, terza parte): il prezzo sta nei materiali e nel bastone
MATERIALI = ("\n\n**Equipaggiamento** armatura completa +1 di adamantio, ascia bipenne di adamantio, "
             "bastone del fuoco (40 cariche)\n")


#: quarta prova (lotto 8, quarta parte): la forma di ADR-0091 e le due voci
NELLA_RIGA = ("\n\n**Statistiche** For 10 · **Equipaggiamento da combattimento** 2 pozioni di *cura ferite gravi* · "
              "**Altro equipaggiamento** *anello di protezione +5*, *mantello della resistenza +5* · **Linguaggi** Comune\n")


def main() -> int:
    conto = {"schede lette": 0, "con equipaggiamento dal prezzo certo": 0, "già fuori regola": 0,
             "sopra il 15° livello": 0}
    esito = {"violazione": 0, "non verificabile": 0, "niente": 0}
    perse = []
    speciale = {"violazione": 0, "scritte": 0}
    materiali = {"violazione": 0, "scritte": 0}
    nella_riga = {"violazione": 0, "scritte": 0}
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        s = V.L.leggi(p)
        if s is None or not sum(g.n for g in s.gruppi):
            continue
        conto["schede lette"] += 1
        v0, n0 = V.ricchezza(p)
        if v0:
            conto["già fuori regola"] += 1
            continue
        from dmcore import sistemi as S
        d = S.dati("dnd35", "creature.costruzione")["oggetti"]
        testo = p.read_text(encoding="utf-8")
        if any(V._oggetti_col_prezzo(r, d, "dnd35") for _, r in V._righe_dell_equipaggiamento(testo)):
            conto["con equipaggiamento dal prezzo certo"] += 1
        with tempfile.TemporaryDirectory() as t:
            q = Path(t) / p.name
            q.write_text(testo + SPECIALE, encoding="utf-8")
            vs, _ = V.ricchezza(q)
            speciale["violazione"] += bool(vs)
            speciale["scritte"] += 1
            q.write_text(testo + MATERIALI, encoding="utf-8")
            materiali["violazione"] += bool(V.ricchezza(q)[0])
            materiali["scritte"] += 1
            q.write_text(testo + NELLA_RIGA, encoding="utf-8")
            nella_riga["violazione"] += bool(V.ricchezza(q)[0])
            nella_riga["scritte"] += 1
            q.write_text(testo + AGGIUNTA, encoding="utf-8")
            v, n = V.ricchezza(q)
        if v:
            esito["violazione"] += 1
        elif len(n) > len(n0) or (n and n != n0):
            esito["non verificabile"] += 1
        elif sum(g.n for g in s.gruppi) > 15:
            conto["sopra il 15° livello"] += 1
        else:
            esito["niente"] += 1
            perse.append(str(p.relative_to(ROOT)))
    fuori = {"conto": conto, "esito": esito, "perse": perse, "capacità speciale e pozioni": speciale,
             "materiali e bastone": materiali, "nella riga delle statistiche": nella_riga}
    (Path(__file__).parent / "misure-ricchezza.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, n in {**conto, **esito}.items():
        print(f"{k:40} {n}")
    for x in perse:
        print("  persa:", x)
    print(f"{'arma con capacità speciale e pozioni':40} {speciale['violazione']}/{speciale['scritte']}")
    print(f"{'materiali speciali e bastone':40} {materiali['violazione']}/{materiali['scritte']}")
    print(f"{'nella riga delle Statistiche':40} {nella_riga['violazione']}/{nella_riga['scritte']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
