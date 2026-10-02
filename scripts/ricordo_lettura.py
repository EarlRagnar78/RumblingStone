#!/usr/bin/env python3
"""ricordo_lettura.py — cosa resta di un modulo il giorno dopo, chiesto al solo diario.

Adattato da `agent_skills/first-reader/scripts/recall.py` e `ask.py` di
awesome-llm-apps (Shubham Saboo, Apache 2.0, commit
4bf51ab704fb2c5b3803cd5191b30d7dcdb51dc2). **Modificato** per il repo
(ADR-0076): le domande sono quelle di un DM che deve condurre, non di un
lettore di blog; l'intenzione contro cui si giudica e' il riquadro *La serata
in tre frasi* del master, o il suo Quickstart; il diario e' quello di
`lettura_a_scene.py`.

Perche'. Il quiz a due agenti (`quiz_lettura.py`) chiede ogni volta una chiave
approvata dal DM. Il DM, il 2026-10-01 (D1 di PIANO-AGENT-SKILLS-ESTERNE): il
ricordo dal diario e' il passo 7 del ciclo per tutti i master, e il quiz resta
dove una chiave approvata c'e' gia'. Il ricordo non chiede chiavi: un agente
**nuovo** riceve solo il diario e risponde alle domande; chi orchestra mette
le risposte accanto all'intenzione del master e giudica. ⚠️ Il quiz ha un
punteggio deterministico, il ricordo no: costa meno e si ripete peggio.

Uso:
    python3 scripts/ricordo_lettura.py domande <corsa>/<lettore>
        → il pacchetto per l'agente nuovo: diario + domande, mai il testo
    python3 scripts/ricordo_lettura.py chiedi <corsa> <lettore|tutti> "<domanda>"
        → il pacchetto per far rispondere un lettore dal suo diario
    python3 scripts/ricordo_lettura.py intenzione <master>
        → l'intenzione del master, per chi giudica

Solo libreria standard.
Exit code: 0 = ok · 1 = corsa o master senza i dati che servono · 2 = errore d'uso.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DOMANDE = (
    ("serata", "In tre frasi: cosa succede stasera?"),
    ("avversario", "Chi si oppone ai PG, e cosa vuole?"),
    ("luoghi", "Da dove partono i PG, e dove arrivano?"),
    ("fallimento", "Cosa succede se falliscono la prova centrale?"),
    ("picco", "Il momento più forte della lettura, e perché."),
    ("fine", "Come finisce?"),
    ("riletto", "Cosa hai dovuto rileggere o cercare, e dove?"),
)

_RIQUADRO = re.compile(r"^>\s*🧭\s*\*\*La serata in tre frasi\.\*\*(.*?)(?=^(?!>)|\Z)", re.M | re.S)
_SEZIONE_ZERO = re.compile(r"^#{2,3}\s+(?:§\s*0\b|.*Quickstart).*$", re.M | re.I)


def carica_diario(cartella: Path) -> "tuple[dict, list[dict]]":
    stato_f, diario_f = cartella / "stato.json", cartella / "diario.jsonl"
    if not stato_f.exists() or not diario_f.exists():
        raise FileNotFoundError(f"{cartella}: mancano stato.json o diario.jsonl (lettura non chiusa?)")
    stato = json.loads(stato_f.read_text(encoding="utf-8"))
    righe = [json.loads(r) for r in diario_f.read_text(encoding="utf-8").splitlines() if r.strip()]
    return stato, righe


def _come_e_andata(stato: dict) -> str:
    n = len(stato["passaggi"])
    return f"si e' fermato al passaggio {stato['smesso_a']} di {n}" if stato.get("smesso_a") \
        else f"ha letto tutti i {n} passaggi"


def _diario_in_chiaro(righe: "list[dict]") -> str:
    return "\n".join(f"[{r['passaggio']} · {r['titolo']}] {'SMESSO ' if r.get('smesso') else ''}{r['diario']}"
                     for r in righe)


def pacchetto_domande(cartella: Path) -> str:
    stato, righe = carica_diario(cartella)
    domande = "\n".join(f"{i}. [{chiave}] {testo}" for i, (chiave, testo) in enumerate(DOMANDE, 1))
    return (
        "Rispondi per un DM che ieri ha letto un modulo una volta sola, una scena alla volta, e "
        "non lo ha piu' davanti. Hai soltanto il diario che ha scritto mentre leggeva. Rispondi "
        "SOLO dal diario: se il diario non basta, scrivi «non e' rimasto niente». E' una risposta "
        "lecita, e dice qualcosa del modulo, non di te.\n\n"
        f"Chi leggeva: {stato['persona']}. Modulo: {stato['master']}. {_come_e_andata(stato)}.\n"
        + "-" * 60 + "\n" + _diario_in_chiaro(righe) + "\n" + "-" * 60 + "\n"
        f"DOMANDE (da una a tre frasi per ognuna; rispondi in JSON con le chiavi fra parentesi quadre):\n{domande}\n"
    )


def pacchetto_domanda(cartella: Path, domanda: str) -> str:
    stato, righe = carica_diario(cartella)
    return (
        f"Sei {stato['persona']}. Ieri hai letto un modulo una scena alla volta e {_come_e_andata(stato)}. "
        "Non hai piu' il testo: hai la memoria della lettura, cioe' le note che prendevi:\n\n"
        + _diario_in_chiaro(righe) + "\n\n"
        f"Il DM ti chiede: {domanda}\n\n"
        "Rispondi da lettore, in meno di 150 parole, solo con quello che hai annotato; cita le tue "
        "note dove rispondono. Non inventare dettagli del modulo che non hai annotato: se le note non "
        "bastano, di' «non l'ho annotato». Non proporre riscritture: di' cosa ti e' successo e cosa "
        "avrebbe dovuto esserci perche' andasse diversamente."
    )


def intenzione(master: Path) -> "tuple[str, str]":
    """(fonte, testo): il riquadro, o il primo paragrafo del Quickstart o del §0."""
    testo = master.read_text(encoding="utf-8")
    m = _RIQUADRO.search(testo)
    if m:
        pulito = " ".join(r.lstrip(">").strip() for r in m.group(1).splitlines())
        return "riquadro «La serata in tre frasi»", pulito.strip()
    s = _SEZIONE_ZERO.search(testo)
    if s:
        dopo = testo[s.end():].strip()
        primo = dopo.split("\n\n", 1)[0]
        return f"primo paragrafo di «{s.group(0).lstrip('#').strip()}»", " ".join(primo.split())
    return "", ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("domande", help="il pacchetto del ricordo: diario + domande")
    p.add_argument("cartella", type=Path, help="<corsa>/<lettore>")
    p = sub.add_parser("chiedi", help="una domanda a un lettore, o a tutti")
    p.add_argument("corsa", type=Path)
    p.add_argument("lettore", help="nome della cartella del lettore, o «tutti»")
    p.add_argument("domanda")
    p = sub.add_parser("intenzione", help="cosa il master dichiara di voler far restare")
    p.add_argument("master", type=Path)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "domande":
            print(pacchetto_domande(a.cartella))
        elif a.cmd == "chiedi":
            nomi = ([d.name for d in sorted(a.corsa.iterdir()) if (d / "stato.json").exists()]
                    if a.lettore == "tutti" else [a.lettore])
            if not nomi:
                print(f"nessun lettore con una lettura chiusa in {a.corsa}")
                return 1
            print("\n\n".join(f"===== lettore: {n} =====\n{pacchetto_domanda(a.corsa / n, a.domanda)}"
                              for n in nomi))
        else:
            fonte, testo = intenzione(a.master)
            if not testo:
                print("RILIEVO: il master non dichiara la sua serata (né il riquadro «La serata in tre "
                      "frasi», né un Quickstart, né un §0): il ricordo non ha contro cosa giudicarsi")
                return 1
            print(f"INTENZIONE ({fonte}):\n{testo}")
    except FileNotFoundError as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
