#!/usr/bin/env python3
"""censimento.py — quali strumenti del repo dipendono dal sistema di gioco.

Misura di partenza per ADR-0111 (regolamenti come plugin). Due parti.

1. **Conta lessicale**, automatica: per ogni script `.py`/`.sh` sotto
   `scripts/` e `converters/` (test, `Old/` e `terzi/` esclusi) conta le
   occorrenze di nove famiglie di espressioni (nucleo d20, caratteristiche,
   termini solo PF1e, solo 3.5, termini 5e vietati, file di dati di regole,
   rilevamento del sistema, ambientazione, tabelle costanti a livello di
   modulo). È un indicatore rumoroso: «GS» in `render_schemi.py` è il
   Giardino di Sale, non il Grado di Sfida. Per questo non decide da sola.
2. **Classificazione a mano**, scritta qui sotto in `CLASSI`, con il motivo
   per riga. Lo script controlla che ogni file con punteggio ≥ 10 sia
   classificato: un file nuovo con molti termini di regole e senza classe fa
   uscire 1.

Fasce:
    A  regole cablate nel codice (tabelle, formule): servono dati per sistema
    B  lessico e termini vietati per sistema: servono liste per sistema
    C  decide quale sistema usa un modulo: deve leggere la configurazione
    D  etichette d20 in stampa o in lettura: oggi uguali in 3.5 e PF1e
    N  neutro: il sistema di gioco non c'entra

    python3 plans/esperimenti/sistemi-plugin-2026-11-07/censimento.py          # tabella
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/censimento.py --json F # dati
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/censimento.py --check  # tutti classificati?

Solo libreria standard; uscita deterministica (file in ordine, nessun seme).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

FAMIGLIE = {
    "d20": r"\b(GS|CA|TS|BAB|DV|CD|LEP|pf|Tempra|Riflessi|Volont[aà]|Lotta|Iniziativa)\b",
    "caratt": r"[\"'](For|Des|Cos|Int|Sag|Car)[\"']",
    "solo_pf1e": r"\b(BMC|DMC|CMB|CMD|PF1e|Pathfinder|pf1|Golarion)\b",
    "solo_35": r"\b(SRD 3\.5|D&D 3\.5|Ascoltare|Osservare|Cercare|Saltare|Equilibrio)\b",
    "vietati_5e": r"\b(vantaggio|svantaggio|riposo breve|riposo lungo|bonus di competenza|azione bonus|lair action)\b",
    "dati_regole": r"(magic_items_srd|pf1e-statistiche|loot_tables|lessico_it|riscontro_srd)",
    "rileva": r"(\*\*Sistema|e_pf1|non_morto_pf1e|\"sistema\"|profilo\.get\(\"sistema)",
    "ambient": r"\b(Faer[uû]n|Forgotten Realms|Golarion|Toril|Vaasa|Damara)\b",
    "tabelle": r"^[A-Z][A-Z0-9_]{2,}\s*(?::[^=\n]+)?=\s*[\{\[\(]",
}
RE = {k: re.compile(v, re.M) for k, v in FAMIGLIE.items()}
PESI = {"d20": 1, "caratt": 2, "solo_pf1e": 1, "solo_35": 1, "rileva": 3}
SOGLIA = 10

#: (fascia, motivo). Le righe si leggono nel codice, non nei commenti di testa.
CLASSI = {
    "scripts/dmcore/tabelle.py": ("A", "TIPI, CLASSI, BAB, TAGLIE, ARMATURE, ELITE/BASIC dal plugin dnd35 (L5a); restano INCANTATORI e i bersagli PF1e per GS"),
    "scripts/dmcore/progressione.py": ("A", "DV di classe, base dei TS (2+L/2, L/3), BAB, classi di prestigio SRD"),
    "scripts/dmcore/caratteristiche.py": ("A", "array del Manuale del DM, razze SRD, profili per ruolo, taglia"),
    "scripts/dmcore/lettura_creatura.py": ("A", "regola NON_MORTO_PF1E cablata (Car al posto di Cos), tetti dei TS"),
    "scripts/dmcore/sistemi.py": ("C", "il rilevamento unico (ADR-0111 L2): sistema_di() da sistemi.toml e la riga «Sistema» controllata contro la configurazione"),
    "scripts/dmcore/creature_pf1e.py": ("A", "formule PF1e cablate (pf, TS buoni/scarsi, BMC/DMC, gradi); i numeri di tipi e taglie dal plugin pf1e (2026-11-07)"),
    "scripts/dmcore/incantesimi.py": ("A", "liste di classe 3.5 e variante PF1e nello stesso dizionario"),
    "scripts/dmcore/statblock.py": ("A", "campi obbligatori gs/ca/pf/ts: lo schema della famiglia d20"),
    "scripts/genera_creatura.py": ("A", "generatore: template Advanced PF1e, tabelle di dmcore"),
    "scripts/genera_attributi.py": ("A", "generatore di caratteristiche su regole 3.5/PF1e"),
    "scripts/derive_statblocks.py": ("A", "derivazione dal GS con il collaudo PF1e Tab. 1-1"),
    "scripts/conformita_statblocchi.py": ("A", "verifica i conti con i template semplici PF1e e le regole SRD"),
    "scripts/validate_bestiario.py": ("A", "benchmark PF1e per GS da pf1e-statistiche-per-gs.yaml"),
    "scripts/suggest_encounter.py": ("A", "EL: la formula 3.5 e la somma dei PE PF1e nel codice (METODI), il metodo e il parametro dal plugin (L4)"),
    "scripts/suggest_loot.py": ("A", "ripartizione del tesoro 3.5 (loot_tables.yaml); il valore per incontro PF1e dal plugin"),
    "scripts/update_xp.py": ("A", "soglie PE dal plugin di ogni sistema (L4); restano livello e PE mancanti come formula"),
    "scripts/build_monster_catalog.py": ("A", "esclude i moduli PF1e dal catalogo per non mescolare i sistemi"),
    "scripts/misura_derivazione.py": ("A", "misura i generatori sulle stesse tabelle"),
    "scripts/impronta_creature.py": ("A", "impronta delle creature sui campi d20"),
    "scripts/riscontro_srd.py": ("B", "fonti per sistema: SRD 3.5 e PRD PF1e in cache (ADR-0103)"),
    "scripts/validate_modules.py": ("B", "termini 5e vietati: dal plugin d20 (termini.vietati, L3) più le 3 voci di canone deprecato"),
    "scripts/validate_standalone.py": ("B", "termini 5e vietati: la stessa lista del plugin d20 (L3), non più una seconda copia"),
    "scripts/validate_prosa.py": ("B", "abilità per sistema dal plugin (lessico.abilita, L3): 3.5 o PF1e secondo il file"),
    "scripts/domande_developer.py": ("C", "sistema da sistemi.toml (L2); ABILITA_ESTRANEE dal plugin (lessico.abilita, L3)"),
    "scripts/lessico_regole.py": ("C", "e_pf1(): il sistema dal percorso o dalla riga Sistema; tabelle dei termini ufficiali (ADR-0110, arrivato il 2026-11-07)"),
    "scripts/dmcore/censimento.py": ("C", "esclude il Drappo perché PF1e, per percorso"),
    "scripts/coerenza_campagna.py": ("B", "CLASSI e RAZZE dal plugin dnd35 (lessico.entita, L3), più il TSV PF1e per i moduli PF1e"),
    "scripts/build_booklet_html.py": ("D", "etichette Iniziativa/CA/pf/TS nel riquadro della creatura"),
    "scripts/export_booklet_typst.py": ("D", "stesse etichette nel riquadro Typst"),
    "scripts/misura_statblocchi_booklet.py": ("D", "conta i campi d20 stampati"),
    "scripts/dmcore/schede.py": ("D", "scheda del PG: For..Car, Tempra/Riflessi/Volontà; PF1e aggiungerebbe BMC/DMC"),
    "scripts/extract_statblocks.py": ("D", "migrazione prosa → statblocco, campi d20"),
    "scripts/componenti.py": ("D", "estrae le CD dal master"),
    "scripts/render_schemi.py": ("N", "falso positivo: GS = Giardino di Sale; pf nelle didascalie"),
    "scripts/misura_distanza_pagine.py": ("D", "distanza fra scena e numeri, cerca i campi d20 nel PDF"),
}
#: Rilevamenti del sistema fuori dagli script (contati da `rilevamenti()`).
DICHIARAZIONE_MASTER = re.compile(r"\*\*Sistema(?::\*\*|\*\*:?|:)\s*([^\n|]{0,40})")


def file_in_esame() -> "list[Path]":
    fuori = {"tests", "Old", "terzi"}
    tutti = [p for p in ROOT.glob("scripts/**/*") if p.suffix in (".py", ".sh")]
    tutti += list(ROOT.glob("converters/**/*.py"))
    return sorted(p for p in tutti if not (fuori & set(p.relative_to(ROOT).parts)))


def conta(p: Path) -> dict:
    t = p.read_text(encoding="utf-8", errors="ignore")
    c = {k: len(r.findall(t)) for k, r in RE.items()}
    c["punteggio"] = sum(c[k] * w for k, w in PESI.items())
    c["righe"] = t.count("\n")
    return c


def rilevamenti() -> dict:
    """I modi in cui oggi si decide il sistema di un modulo."""
    master = sorted(
        str(p.relative_to(ROOT)) for p in ROOT.glob("**/*.md")
        if not {"plans", "skills", "docs", ".git"} & set(p.relative_to(ROOT).parts)
        and DICHIARAZIONE_MASTER.search(p.read_text(encoding="utf-8", errors="ignore")))
    grafie = set()
    for f in master:
        for m in DICHIARAZIONE_MASTER.finditer((ROOT / f).read_text(encoding="utf-8", errors="ignore")):
            g = re.sub(r"[*`]", "", m.group(1)).strip()[:22]
            if g and not g.lower().startswith(("chase", "benedizioni", "definitivo")):
                grafie.add(g)
    profili = json.loads((ROOT / "plans/domande-developer.json").read_text(encoding="utf-8"))
    con_sistema = sorted(k for k, v in profili.get("profili", {}).items() if "sistema" in v)
    return {
        "riga_sistema_nei_master": len(master),
        "grafie_diverse_della_riga": len(grafie),
        "profili_con_sistema_in_domande_developer": len(con_sistema),
        "fuori_da_sistemi_toml": rilevamenti_indipendenti(),
    }


def rilevamenti_indipendenti() -> "list[str]":
    """Gli script che decidono il sistema senza sistemi.toml (misurato, L2).

    Un nome di modulo scritto nel codice («Il-Drappo-di-Tarsilia» fra
    virgolette), o una funzione e_pf1/e_pf1e che non passa da sistema_di()."""
    fuori = []
    for f in sorted((ROOT / "scripts").rglob("*.py")):
        rel = str(f.relative_to(ROOT))
        if "/tests/" in rel or rel == "scripts/dmcore/sistemi.py":
            continue
        codice = "\n".join(r.split("#", 1)[0] for r in f.read_text(encoding="utf-8", errors="ignore").splitlines())
        if (re.search(r"[\"']Il-Drappo-di-Tarsilia[\"']", codice)
                or (re.search(r"def e_pf1e?\b", codice) and "sistema_di" not in codice)):
            fuori.append(rel)
    return fuori


def misure(righe: "list[tuple[str, dict]]") -> dict:
    per_fascia: "dict[str, list[str]]" = {}
    for f, (fa, _) in CLASSI.items():
        per_fascia.setdefault(fa, []).append(f)
    tabelle_a = sum(c["tabelle"] for f, c in righe if CLASSI.get(f, ("N",))[0] == "A")
    copie_5e = sum(1 for f, c in righe if c["vietati_5e"] >= 3 and CLASSI.get(f, ("N",))[0] == "B")
    return {
        "file_esaminati": len(righe),
        "per_fascia": {k: len(v) for k, v in sorted(per_fascia.items())},
        # sistemi.toml, più ogni rilevamento che non lo legge, più i profili con
        # «sistema». Da L0: 3 (percorso, riga «Sistema», profili). Obiettivo di L2: 1.
        "M1_meccanismi_di_rilevamento": 1 + len(rilevamenti_indipendenti())
        + (1 if rilevamenti()["profili_con_sistema_in_domande_developer"] else 0),
        "M2_copie_della_lista_5e": copie_5e,
        "M3_tabelle_costanti_nei_file_A": tabelle_a,
        "M4_file_da_toccare_per_un_sistema_nuovo": sum(len(per_fascia.get(k, [])) for k in "ABC"),
        "rilevamenti": rilevamenti(),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", type=Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    righe = [(str(p.relative_to(ROOT)), conta(p)) for p in file_in_esame()]
    senza = [f for f, c in righe if c["punteggio"] >= SOGLIA and f not in CLASSI]
    m = misure(righe)
    if a.json:
        a.json.write_text(json.dumps({"misure": m, "senza_classe": senza,
                                      "file": {f: {**c, "fascia": CLASSI.get(f, ("N", ""))[0],
                                                   "motivo": CLASSI.get(f, ("", ""))[1]}
                                               for f, c in righe}},
                                     ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                          encoding="utf-8")
    if not a.check:
        print("| Fascia | File | Punteggio | Motivo |\n|---|---|---|---|")
        for f, c in sorted(righe, key=lambda r: (CLASSI.get(r[0], ("Z",))[0], -r[1]["punteggio"], r[0])):
            if f in CLASSI:
                print(f"| {CLASSI[f][0]} | `{f}` | {c['punteggio']} | {CLASSI[f][1]} |")
        print()
        print(json.dumps(m, ensure_ascii=False, indent=1))
    if senza:
        print("Senza classe con punteggio ≥ %d: %s" % (SOGLIA, ", ".join(senza)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
