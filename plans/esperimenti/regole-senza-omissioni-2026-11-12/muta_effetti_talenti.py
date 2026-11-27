#!/usr/bin/env python3
"""Banco del lotto 4 (ADR-0126): il bonus di un talento contato sull'abilità sbagliata.

Prima il controllo dei gradi dava 3 punti di margine a **tutte** le abilità di
una scheda che nomina un talento d'abilità (Allerta, Abilità Focalizzata…). Ora
il bonus va solo alle abilità che il talento nomina, col suo numero.

Per ogni scheda del Bestiario che nomina uno di quei talenti (nella riga dei
talenti o altrove) e per ogni abilità scritta, si alza il bonus al valore più alto che il conto di
prima accettava (un punto sotto la sua soglia). Quel valore chiede più gradi
del massimo, salvo che l'abilità sia proprio quella di un talento da +3:

* `errore`: l'abilità non ha un talento da +3 → la copia è fuori regola, va vista;
* `controllo`: l'abilità ha un talento da +3 (o il bonus vale per tutte) → la
  copia è in regola, **non** deve dare una violazione.

Le schede con classi fuori dal plugin (il conto dei gradi è un dubbio) stanno in
una colonna a parte. Uso: python3 muta_effetti_talenti.py
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

VERO = V._bonus_dei_talenti


def _viste(testo: str, p: Path, prima: bool) -> "tuple[set, bool]":
    V._bonus_dei_talenti = (lambda *a: ({}, 3)) if prima else VERO
    try:
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / p.name
            q.write_text(testo, encoding="utf-8")
            v, n = V.abilita(q)
    finally:
        V._bonus_dei_talenti = VERO
    return ({x["abilita"] for x in v if x["regola"] == "gradi.massimo"},
            any(x["regola"] == "gradi.punti" and "non calcolabili" in x.get("testo", "") for x in n))


def _con_bonus(testo: str, i: int, nome: str, vecchio: str, nuovo: int) -> str:
    righe = testo.split("\n")
    righe[i] = re.sub(rf"({re.escape(nome)}(?:\s*\([^)]*\))?\s*){re.escape(vecchio)}(?!\d)",
                      lambda m: f"{m.group(1)}{nuovo:+d}", righe[i], count=1)
    return "\n".join(righe)


def main() -> int:
    import lessico_regole as LR
    from dmcore import sistemi as S
    conta = {"errore": [0, 0], "controllo": [0, 0]}          # [fatte, viste dopo]
    dubbie, schede, viste_prima, perse = 0, 0, 0, []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        f, s = V.VT.leggi(p) or {"nomi": []}, V.L.leggi(p)
        if s is None:
            continue
        sistema = V.VT.sistema_di(p, s.testo)
        try:
            regole = S.dati(sistema, "creature.gradi")
        except S.ErroreSistemi:
            continue
        chiave = regole["chiave"]
        per, a_tutte = V._talenti_d_abilita(f["nomi"], s.testo, sistema, regole, sum(g.n for g in s.gruppi))
        if not per and not a_tutte:
            continue
        testo = p.read_text(encoding="utf-8")
        i, riga = next(((n, m.group(1)) for n, r in enumerate(testo.split("\n"))
                        if (m := V.RIGA_ABILITA.search(r)) and re.search(r"[+−-]\d", m.group(1))), (None, None))
        if riga is None:
            continue
        schede += 1
        for nome, _, bonus in V.VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
            nome = nome.strip()
            en = V._abilita_it().get(LR.norma(nome), nome.lower())
            en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
            if en is None:
                continue
            b = int(bonus.replace("−", "-"))
            soglia = next((x for x in range(b, b + 60) if en in _viste(_con_bonus(testo, i, nome, bonus, x), p, True)[0]), None)
            if soglia is None or soglia == b:
                continue                                 # non mutabile, o già fuori regola
            mutata = _con_bonus(testo, i, nome, bonus, soglia - 1)
            if mutata == testo and soglia - 1 != b:
                continue
            prima, dubbia = _viste(mutata, p, True)
            dopo, _ = _viste(mutata, p, False)
            if dubbia:
                dubbie += 1
                continue
            viste_prima += en in prima
            tipo = "controllo" if max(per.get(en, 0), a_tutte) >= 3 else "errore"
            conta[tipo][0] += 1
            conta[tipo][1] += en in dopo
            if tipo == "errore" and en not in dopo:
                perse.append(f"{p.name}: {nome}")
    fuori = {"schede_con_un_talento_d_abilita": schede,
             "errori_messi": conta["errore"][0], "errori_visti_prima": viste_prima, "errori_visti_dopo": conta["errore"][1],
             "controlli_in_regola": conta["controllo"][0], "controlli_segnati_a_torto": conta["controllo"][1],
             "mutazioni_in_schede_dubbie": dubbie, "perse": perse}
    (Path(__file__).parent / "misure-effetti-talenti.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(fuori, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
