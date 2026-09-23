#!/usr/bin/env python3
"""impronta_creature.py — che cosa calcolano oggi i quattro script delle creature.

`PIANO-QUALITA-DEL-CODICE` §8, lotto E, sotto-lotto E0.

Il lotto E sposta in `dmcore/` il lettore, la progressione e la scelta delle
caratteristiche che oggi stanno in `genera_attributi`, `conformita_statblocchi`,
`derive_statblocks` e `genera_creatura`. E' uno spostamento: nessun numero deve
cambiare. Questo script scrive **tutti i numeri** che quei quattro producono sul
Bestiario vero, e il test `test_impronta_creature.py` li riconfronta dopo ogni
sotto-lotto.

⚠️ **Il rischio che l'impronta esiste per prendere** e' un'espressione regolare
spostata che perde un flag (`re.M`, `re.I`) e cambia un numero su tre schede su
cento. Per questo l'impronta non registra solo i risultati finali (le
caratteristiche, il giudizio del verificatore) ma anche **ogni lettura
intermedia**, scheda per scheda: dadi vita, `pf-dado` sospetto, sestina della
scheda e della fonte, numeri della fonte, composizione, talenti, tetti dei TS.
Un difetto di lettura cade sulla chiave che lo nomina, non su un conto finale
dove due errori possono compensarsi.

Che cosa c'e' dentro, per chiave:

* ``bestiario`` — per ogni statblocco: le letture, `genera_attributi.genera`
  con e senza la fonte, `conformita_statblocchi.giudica` e `pf_dado_corretto`,
  l'esito di `extract_statblocks.controlla`;
* ``derivazioni`` — per ogni scheda senza blocco: `derive_statblocks.deriva`;
* ``apply_ts`` — `--apply-ts` rifatto in una cartella temporanea su tre schede
  di prova: e' l'unico modo di far girare `con_attributi`, perche' oggi
  nessuna scheda del Bestiario e' scrivibile;
* ``creature`` — `genera_creatura.genera` su GS 1-20 × i sei ruoli × tre forme
  (mostro umanoide, PNG con classe, bestia magica) × `--piu-cattivi`, a seme
  fisso;
* ``gate`` — `--taratura`, `--riepilogo`, `--check` dei due script che ne hanno
  uno, e la proposta di `--correggi-pf-dado`.

Sola lettura: non scrive nel Bestiario. L'uscita e' deterministica (chiavi
ordinate, nessun orologio), e due esecuzioni sullo stesso commit danno lo stesso
file byte per byte.

Uso:

    python3 scripts/impronta_creature.py                # su stdout
    python3 scripts/impronta_creature.py --scrivi       # nella fixture del test
    python3 scripts/impronta_creature.py --confronta    # esce 1 se diverge, e dice dove

Solo stdlib.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import random
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import conformita_statblocchi as C  # noqa: E402
import derive_statblocks as D  # noqa: E402
import extract_statblocks as E  # noqa: E402
import genera_attributi as GA  # noqa: E402
import genera_creatura as GC  # noqa: E402
from dmcore.statblock import rendi  # noqa: E402

FIXTURE = ROOT / "scripts" / "tests" / "fixtures" / "impronta-creature.json"

#: Le tre forme della griglia di `genera_creatura`: il ramo mostri su due tipi,
#: e il ramo PNG, che parte solo con una classe.
FORME = ("umanoide", "png", "bestia magica")


def _dati(x):
    """Tuple, Path e dataclass diventano JSON senza perdere l'ordine delle tuple."""
    if dataclasses.is_dataclass(x) and not isinstance(x, type):
        return {k: _dati(v) for k, v in dataclasses.asdict(x).items()}
    if isinstance(x, dict):
        return {str(k): _dati(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set, frozenset)):
        seq = sorted(x, key=repr) if isinstance(x, (set, frozenset)) else x
        return [_dati(v) for v in seq]
    if isinstance(x, Path):
        return str(x.relative_to(ROOT)) if x.is_relative_to(ROOT) else str(x)
    if isinstance(x, float) and x.is_integer():
        return x
    return x


def _rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def _gs(testo: str) -> "float | None":
    m = re.search(r"^gs:\s*([\d.,]+)", testo, re.M)
    return float(m.group(1).replace(",", ".")) if m else None


def letture(p: Path, testo: str) -> dict:
    """Ogni lettura intermedia che il lotto E sposta, su una scheda."""
    gs = _gs(testo)
    m_tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M) or \
        re.search(r"\*\*Size/Type\*\*:?\s*([^|\n]+)", testo)
    tipo = m_tipo.group(1).strip() if m_tipo else ""
    gruppi, nota = C.composizione(testo, tipo)
    fuori = {
        "taglia": GA.taglia_di(testo),
        "dadi_vita": GA.dadi_vita(testo),
        "pf_dado_sospetto": GA.pf_dado_sospetto(testo),
        "pf_dado_sospetto_col_gs": GA.pf_dado_sospetto(testo, gs),
        "dalla_scheda": GA.dalla_scheda(testo),
        "dalla_fonte": GA.dalla_fonte(p.name, testo),
        "sestine_citate": GA.sestine_citate(testo),
        "numeri_della_fonte": GA.numeri_della_fonte(testo),
        "tetti_dai_ts": GA.tetti_dai_ts(str(p), testo),
        "iniziativa_ambigua": GA.iniziativa_ambigua(testo),
        "senza_note": len(GA.senza_note(testo)),
        "composizione": [gruppi, nota],
        "dv_totali": C.dv_totali(testo),
        "dadi_di_pf": C.dadi_di_pf(testo),
        "talenti": C.talenti(testo),
        "provenienza": C.provenienza(testo),
        "template_dichiarati": C.template_dichiarati(testo),
    }
    if gs is not None:
        fuori["vincoli"] = {f.__name__: f(testo, gs) for f in (
            GA.des_vincolata, GA.des_da_iniziativa, GA.cos_da_pf, GA.for_da_lotta)}
    return fuori


def bestiario() -> dict:
    fuori = {}
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        testo = p.read_text(encoding="utf-8", errors="replace")
        voce = {"controlla": E.controlla(p)}
        if GA.BLOCCO.search(testo):
            voce["letture"] = letture(p, testo)
            gs = _gs(testo)
            ruolo = re.search(r"\*\*Role\*\*:\s*([^\|\n]+)", testo, re.I)
            ruolo = ruolo.group(1).strip() if ruolo else ""
            if gs is not None:
                voce["genera"] = GA.genera(p.name, ruolo, gs, testo)
                voce["genera_senza_fonte"] = GA.genera(p.name, ruolo, gs, testo, usa_fonte=False)
        s = C.leggi(p)
        if s:
            voce["scheda"] = {k: getattr(s, k) for k in (
                "gs", "tipo", "attributi", "provenienza", "gruppi", "composizione_nota",
                "pf", "ts", "bab", "lotta", "mischia")}
            voce["giudica"] = C.giudica(s)
            voce["pf_dado_corretto"] = C.pf_dado_corretto(s)
            voce["pf_dado_corretto_forzato"] = C.pf_dado_corretto(s, forza=True)
        if len(voce) > 1 or voce["controlla"]:
            fuori[_rel(p)] = voce
    return fuori


def derivazioni() -> dict:
    """`derive_statblocks` come lo esegue il suo `main`, senza scrivere."""
    fuori = {}
    for f in E.schede():
        t = f.read_text(encoding="utf-8")
        if E.APERTURA in t or E.e_non_creatura(t):
            continue
        L = D.leggi_scheda(f)
        sb, conti, manca = D.deriva(L)
        voce = {"lettura": L, "blocco": rendi(sb) if sb else None,
                "conti": conti, "manca": manca}
        if sb is not None:
            letto, _ = D.estrai(t)
            derivati = [c for c in ("ca", "pf", "ts", "gs")
                        if not getattr(letto, c) and getattr(sb, c)]
            voce["derivati"] = derivati
            voce["scrivibile"] = bool(derivati == ["ts"] and letto.gs and letto.ca and letto.pf)
        fuori[_rel(f)] = voce
    return fuori


#: Schede in prosa senza blocco: la prima e' quella di
#: `test_derive_scrive_le_caratteristiche`, le altre coprono il tipo senza
#: classi e un PNG di razza con l'armatura di cuoio.
SCHEDE_DI_PROVA = {
    "sergente-prova-cr3.md": """\
# Sergente di Prova
**Faction**: red-hand | **Role**: melee-heavy | **Environment**: any | **CR**: 3

Medium humanoid (hobgoblin), Fighter 3, LE. **hp 28**; **AC 17** (+1 Des, +4 giaco di maglia, \
+2 scudo pesante), touch 11, flat-footed 16. Vel 9 m.
**Mischia** spada lunga +6 (1d8+3).
""",
    "bestia-prova-cr5.md": """\
# Bestia di Prova
**Faction**: wild | **Role**: brute | **Environment**: any | **CR**: 5

Large magical beast, 6d10, N. **hp 51**; **AC 16** (-1 size, +1 Des, +6 natural), touch 10. Vel 12 m.
**Mischia** morso +9 (2d6+6).
""",
    "esploratore-prova-cr4.md": """\
# Esploratore di Prova
**Faction**: red-hand | **Role**: skirmisher | **Environment**: any | **CR**: 4

Small humanoid (goblin), Rogue 4, NE. **hp 18**; **AC 17** (+1 size, +3 Des, +3 studded leather), \
touch 14. Vel 9 m.
**Mischia** spada corta +5 (1d4).
""",
}


def apply_ts() -> dict:
    """`derive_statblocks --apply-ts` rifatto in una cartella temporanea.

    Oggi nessuna scheda del Bestiario e' scrivibile (le due proposte sono
    rimandi), quindi `con_attributi`, la meta' di derive_statblocks che chiama
    genera_attributi, sul Bestiario non girerebbe mai. Si rifa' il percorso su
    tre schede di prova.
    """
    fuori = {}
    with tempfile.TemporaryDirectory() as cartella:
        for nome, t in SCHEDE_DI_PROVA.items():
            f = Path(cartella) / nome
            f.write_text(t, encoding="utf-8")
            L = D.leggi_scheda(f)
            sb, conti, manca = D.deriva(L)
            voce = {"conti": conti, "manca": manca}
            if sb is not None:
                letto, _ = D.estrai(t)
                for campo in ("ca", "pf", "ts", "gs", "tipo", "ca_dettaglio", "velocita",
                              "iniziativa"):
                    if getattr(letto, campo):
                        setattr(sb, campo, getattr(letto, campo))
                voce["con_attributi"] = D.con_attributi(f, sb, L)
            fuori[nome] = voce
    return fuori


def creature() -> dict:
    fuori = {}
    for gs in range(1, 21):
        for ruolo in sorted(GC.RUOLI):
            R = GC.RUOLI[ruolo]
            for forma in FORME:
                for cattivi in (False, True):
                    chiave = f"gs{gs:02d} {ruolo} {forma}{' piu-cattivi' if cattivi else ''}"
                    rng = random.Random(chiave)
                    kw = {"ruolo": ruolo, "piu_cattivi": cattivi, "rng": rng}
                    if forma == "png":
                        kw["classe"] = (R.classe_tipica or "guerriero", gs)
                    elif forma == "bestia magica":
                        kw["tipo"] = "magical beast"
                        kw["taglia"] = "large"
                    sb, conto = GC.genera(gs, **kw)
                    fuori[chiave] = {"blocco": rendi(sb), "conto": conto.righe,
                                     "rincari": conto.rincari}
    return fuori


def gate() -> dict:
    return {
        "taratura": {k: GA.taratura(k) for k in ("fonti", "schede")},
        "genera_attributi_proponi": [
            {"file": r["file"], "riga": r["riga"], "marca": r["marca"],
             "scritta": r["scritta"], "note": r["note"]}
            for r in GA.proponi(rigenera=True)],
        "genera_attributi_controlla": GA.controlla(),
        "conformita_riepilogo": C.riepilogo(C.tutte()),
        "conformita_controlla_pf_dado": C.controlla_pf_dado(),
        "conformita_proponi_pf_dado": C.correggi_pf_dado(scrivi=False),
    }


def impronta() -> dict:
    return _dati({"bestiario": bestiario(), "derivazioni": derivazioni(),
                  "apply_ts": apply_ts(), "creature": creature(), "gate": gate()})


def testo(dati: dict) -> str:
    return json.dumps(dati, ensure_ascii=False, sort_keys=True, indent=1) + "\n"


def differenze(vecchia, nuova, dove: str = "", fuori: "list | None" = None,
               limite: int = 40) -> "list[str]":
    """I percorsi delle chiavi che cambiano, i piu' profondi possibile."""
    fuori = [] if fuori is None else fuori
    if len(fuori) >= limite or vecchia == nuova:
        return fuori
    if isinstance(vecchia, dict) and isinstance(nuova, dict):
        for k in sorted(set(vecchia) | set(nuova)):
            if k not in vecchia or k not in nuova:
                fuori.append(f"{dove}/{k}: {'nuova' if k not in vecchia else 'sparita'}")
            else:
                differenze(vecchia[k], nuova[k], f"{dove}/{k}", fuori, limite)
            if len(fuori) >= limite:
                break
        return fuori
    if isinstance(vecchia, list) and isinstance(nuova, list) and len(vecchia) == len(nuova):
        for i, (a, b) in enumerate(zip(vecchia, nuova)):
            differenze(a, b, f"{dove}[{i}]", fuori, limite)
        return fuori
    corto = lambda v: (s if len(s := json.dumps(v, ensure_ascii=False)) < 160  # noqa: E731
                       else s[:157] + "...")
    fuori.append(f"{dove}: {corto(vecchia)} → {corto(nuova)}")
    return fuori


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scrivi", action="store_true",
                    help=f"scrive l'impronta in {FIXTURE.relative_to(ROOT)}")
    ap.add_argument("--confronta", action="store_true",
                    help="confronta con la fixture: esce 1 e dice dove, se diverge")
    args = ap.parse_args(argv)
    dati = impronta()
    if args.scrivi:
        FIXTURE.write_text(testo(dati), encoding="utf-8")
        print(f"✓ impronta scritta in {FIXTURE.relative_to(ROOT)}")
        return 0
    if args.confronta:
        vecchia = json.loads(FIXTURE.read_text(encoding="utf-8"))
        diff = differenze(vecchia, json.loads(testo(dati)))
        for d in diff:
            print(f"✗ {d}")
        if diff:
            return 1
        print("✓ impronta delle creature identica")
        return 0
    sys.stdout.write(testo(dati))
    return 0


if __name__ == "__main__":
    sys.exit(main())
