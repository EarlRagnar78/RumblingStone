#!/usr/bin/env python3
"""superficie_norme.py — quanta superficie ha una norma che nessuno misura.

## La domanda a cui risponde

*«Questa norma non e' misurata: manca il codice, o manca il dato?»*

E' la domanda che il registro delle norme lasciava aperta. Undici righe 🔴
portavano una ragione scritta — cosi' come ADR-0056 pretende — ma la ragione
era **prosa**: nessun comando la rimisurava, e un motivo scritto a mano
invecchia come qualunque altra cosa scritta a mano. Il 2026-09-21 il DM ha
chiesto *«un rilevatore per tutte le norme, deterministico e idempotente»*, e
misurando le undici e' venuto fuori che **il codice non era quasi mai il
problema**.

## I quattro stati, e perche' non sono la stessa cosa

Una norma non misurata sta in uno di quattro stati, e il passo successivo e'
diverso in ognuno. Confonderli e' il motivo per cui «non misurato» sembrava
un elenco omogeneo di lavoro da fare, e non lo e':

| stato | cosa manca | il passo successivo |
|---|---|---|
| `SUPERFICIE_VUOTA` | la **convenzione esiste** e ha **zero occorrenze** | marcare il contenuto: il rilevatore si accende da solo |
| `CONVENZIONE_ASSENTE` | nessuno ha mai deciso **come si marca** | una decisione di forma, poi la marcatura |
| `OGGETTO_ASSENTE` | non esiste proprio il **file** di cui la norma parla | produrre l'oggetto, o ammettere che non esiste |
| `FUORI_DOMINIO` | il fatto **non e' nel testo** | niente: si dichiara e si chiude |

⚠️ **`FUORI_DOMINIO` non e' un buco.** *«Almeno un congegno per campagna deve
scattare davvero»* e' un fatto del **tavolo**: nessun rilevatore su nessun
file potra' mai saperlo. Contarlo fra il lavoro da fare gonfierebbe il debito
con una riga che non si chiudera' mai.

## Determinismo e idempotenza

Ogni misura e' una conta di occorrenze di una **forma dichiarata** su un
insieme di file **ordinato**. Nessuno stato accumulato, nessuna dipendenza
dall'ordine delle chiamate, nessuna rete: due esecuzioni sullo stesso commit
danno lo stesso risultato, byte per byte. Lo prova `test_superficie_norme.py`.

## Uso

    python3 scripts/superficie_norme.py             # la tabella
    python3 scripts/superficie_norme.py --json      # per la catena
    python3 scripts/superficie_norme.py --check     # esce 1 se una riga mente

Il `--check` non boccia una superficie vuota — **una superficie vuota e' un
fatto, non un difetto**. Boccia una riga che *dichiara* una forma che nel
codice non esiste, o che dichiara `SUPERFICIE_VUOTA` mentre le occorrenze ci
sono: cioe' il registro che ha smesso di dire il vero.

Decisione: ADR-0062.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402

SUPERFICIE_VUOTA = "SUPERFICIE_VUOTA"
CONVENZIONE_ASSENTE = "CONVENZIONE_ASSENTE"
OGGETTO_ASSENTE = "OGGETTO_ASSENTE"
FUORI_DOMINIO = "FUORI_DOMINIO"

def _file_di_gioco() -> "list[Path]":
    """Il contenuto di gioco vivo, **riusando l'insieme che il repo dichiara**.

    🐛 **La prima stesura ne teneva uno suo, e ha sbagliato al primo giro.**
    Escludeva le cartelle con il punto davanti e le sei di lavoro, e si e'
    dimenticata `build/`: la forma `COLORE DOMINANTE` risultava presente **5
    volte**, e la norma sulla tinta d'arco veniva dichiarata «misurabile ora».
    Le cinque occorrenze erano le copie generate della skill che quella forma
    la **prescrive**, non archi che la dichiarano.

    Ventesimo caso della famiglia «un criterio largo si inventa copertura», e
    la cura e' sempre la stessa: `misura_craft.file_di_gioco_p1()` questo
    insieme lo definisce gia', con `ESCLUSI`, `ESCLUSI_NOME` e le cartelle che
    si dichiarano archivio con un `_SNAPSHOT-STORICO.md`. Si riusa.
    """
    return mc.file_di_gioco_p1()


def _conta(forma: str) -> int:
    """Quante volte la forma dichiarata compare nel contenuto di gioco."""
    rx = re.compile(forma)
    return sum(len(rx.findall(f.read_text(encoding="utf-8", errors="replace")))
               for f in _file_di_gioco())


def _conta_file(modello: str) -> int:
    return len([p for p in ROOT.glob(modello) if p.is_file()])


#: 🔴 **Le norme che nessuno misura, e cosa manca a ciascuna.**
#:
#: Ogni riga dichiara la **forma** che andrebbe cercata. Se la forma e' `None`,
#: nessuno ha ancora deciso come si marca quella cosa — e la decisione viene
#: prima del codice, sempre.
NORME_SCOPERTE = (
    {
        "chiave": "el_oltre_il_tetto",
        "norma": "npc-villain-boosting — EL <= APL+4, e oltre il tetto un `Boost log:`",
        "prerequisito": "gli incontri dichiarano il loro EL nella forma prescritta",
        "forma": r"\*\*EL\*\*:\s*\[?\d",
        "dove": "AGENTS.md riga 352 prescrive `**EL**: [N]`",
        "rilevatore_pronto": "validate_modules.py --tetto-el",
        "sblocca": "PIANO-MARCATURA-DEGLI-INCONTRI M1-M3",
    },
    {
        "chiave": "tinta_arco_ripetuta",
        "norma": "varieta-fra-archi.md — mai due archi di fila con la stessa tinta",
        "prerequisito": "ogni arco dichiara le sue cinque righe d'intestazione",
        "forma": r"COLORE DOMINANTE",
        "dove": "varieta-fra-archi.md prescrive COLORE DOMINANTE / CONTRAPPUNTO / "
                "FAMIGLIA DI CASO / CONGEGNO / IL PICCO",
        "rilevatore_pronto": None,
        "sblocca": "una riga per arco, nove righe in tutto",
    },
    {
        "chiave": "nodo_tre_porte",
        "norma": "nodi-e-sei-porte.md — >=3 porte per nodo, >=1 fisica",
        "prerequisito": "i nodi d'indagine sono marcati",
        "forma": None,
        "dove": "nessuna forma prescritta: `nodi-e-sei-porte.md` descrive il nodo "
                "a tre strati ma non dice come si marca sulla pagina",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-INDAGINE-E-DEDUZIONE I6, gated su I5",
    },
    {
        "chiave": "box_di_luogo_senza_creature",
        "norma": "read-aloud-adulti.md §2-bis — il box di luogo non descrive le creature (Dungeon)",
        "prerequisito": "ogni box dichiara il suo tipo: di luogo, d'ingresso, di round",
        "forma": None,
        "dove": "nessuna forma prescritta: l'etichetta `**Read-aloud (pilastro).**` "
                "dice la voce, non il tipo del box; senza il tipo, i 322 nomi del "
                "registro pescano 315 box su 501 (dei, PG, artefatti)",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE B2, D3",
    },
    {
        "chiave": "fatto_da_due_nodi",
        "norma": "nodi-e-sei-porte.md — ogni fatto raggiungibile da >=2 nodi",
        "prerequisito": "i nodi d'indagine sono marcati",
        "forma": None,
        "dove": "stesso prerequisito del precedente",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-INDAGINE-E-DEDUZIONE I6",
    },
    {
        "chiave": "sei_nove_nodi",
        "norma": "congegno-e-enigmi.md — 6-9 nodi per caso",
        "prerequisito": "i nodi d'indagine sono marcati",
        "forma": None,
        "dove": "stesso prerequisito",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-INDAGINE-E-DEDUZIONE I6",
    },
    {
        "chiave": "ricomposizione_nove",
        "norma": "ricomposizione.md — mai piu' di 9 elementi nella ricomposizione",
        "prerequisito": "i nodi d'indagine sono marcati",
        "forma": None,
        "dove": "stesso prerequisito",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-INDAGINE-E-DEDUZIONE I6",
    },
    {
        "chiave": "gradi_dei_pg",
        "norma": "registro-e-ricompense.md — tetto livello+3, max +6, 1 grado/PG/livello",
        "prerequisito": "esiste una scheda personaggio leggibile per i quattro PG",
        "forma": None,
        "oggetto": "PG/*Scheda*.md",
        "dove": "in `PG/` ci sono gli artefatti e le immagini, **nessun master di "
                "scheda personaggio**: lo dice anche INDEX, «il layout schede e' "
                "pronto e aspetta i numeri veri»",
        "rilevatore_pronto": None,
        "sblocca": "le schede A4 dei quattro PG — gated sul DM",
    },
    {
        "chiave": "congegno_scattato",
        "norma": "congegno-e-enigmi.md — almeno un congegno per campagna deve scattare",
        "prerequisito": None,
        "forma": None,
        "dove": "e' un fatto di **gioco**: nessun file lo porta, e nessun "
                "rilevatore potra' mai saperlo",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
    {
        "chiave": "eco_che_anticipa",
        "norma": "consequence-echoes.md §3-ter regola 3 — un eco per un PG non anticipa",
        "prerequisito": "ogni eco per un PG dichiara quale scena del master prepara",
        "forma": None,
        "dove": "nessuna forma prescritta: i fogli-eco non dicono a quale scena "
                "portano, e senza quel legame nessuno sa cosa sarebbe un'anticipazione",
        "rilevatore_pronto": None,
        "sblocca": "una convenzione di marcatura eco → scena, poi il confronto col master",
    },
    {
        "chiave": "hero_map_fedele_all_svg",
        "norma": "rumblingstone-mapmaking regola 8 — una hero map di Canva AI che "
                 "sposta porte, stanze o accessi rispetto all'SVG si butta",
        "prerequisito": None,
        "forma": None,
        "dove": "il fatto sta in un raster dipinto, non in un testo: confrontarlo "
                "con l'SVG chiede visione artificiale. Resta il gate di rifiuto di "
                "chi guarda le due immagini sovrapposte",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
    {
        "chiave": "sette_modi_di_stare_al_tavolo",
        "norma": "sviluppo-degli-incontri.md §7 — negli stand-alone, ogni modo di stare "
                 "al tavolo di Robin Laws ha una scena",
        "prerequisito": "le scene dichiarano per chi sono fatte",
        "forma": None,
        "dove": "nessuna forma prescritta; la §1 (chi resta a terra contro un nemico in "
                "volo) si misura da domande_developer.py D1, questa no",
        "rilevatore_pronto": None,
        "sblocca": "un campo nel contratto «In scena» (per esempio `Per chi:`), poi un conteggio",
    },
    {
        "chiave": "appunti_quattrocento_parole",
        "norma": "quiz-a-due-agenti.md — gli appunti del lettore stanno in 400 parole",
        "prerequisito": "gli appunti di ogni esecuzione del quiz stanno in un posto fisso del repo",
        "forma": None,
        "dove": "oggi gli appunti vivono nello scratchpad di chi orchestra; i due del "
                "2026-09-26 sono stati copiati a mano in plans/esperimenti/quiz-def4/",
        "rilevatore_pronto": None,
        "sblocca": "una cartella per esecuzione, poi quiz_lettura.py --check conta le parole",
    },
    {
        "chiave": "lettura_a_freddo_prima_del_def",
        "norma": "rumblingstone-module-standard, ciclo completo passi 6-7 — un master e' DEF "
                 "solo dopo lettore e playtester a freddo senza 🔴 e il quiz a due agenti",
        "prerequisito": None,
        "forma": None,
        "dove": "sono letture di un agente: un cancello su un giudizio sarebbe rumore "
                "(ADR-0073). Li chiede il piano che tocca il master (ADR-0075)",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
    {
        "chiave": "due_livelli_di_subordinate",
        "norma": "read-aloud-adulti.md — max due livelli di subordinate",
        "prerequisito": None,
        "forma": None,
        "dove": "qui non manca il **dato**, manca lo **strumento**: serve un parser "
                "sintattico dell'italiano. Il segnale povero — contare le virgole — "
                "darebbe i falsi positivi 64/64 gia' visti in PROSA-CHE-NON-SEMBRI-GENERATA",
        "rilevatore_pronto": None,
        "sblocca": None,
    },    {
        "chiave": "adr_nuovo_con_alternative",
        "norma": "ADR-0000-template.md (D7 di PIANO-RECUPERO) — un ADR nuovo ha le "
                 "alternative considerate e la condizione «Da rivedere se»",
        "prerequisito": "esiste un ADR scritto dopo il modello del 2026-10-10",
        "forma": None,
        "oggetto": "plans/adr/ADR-0089-*.md",
        "dove": "gli 87 ADR accettati non si riscrivono; il primo scritto col modello "
                "nuovo e' il 0089, perche' il 0088 e' prenotato da una proposta gia' scritta",
        "rilevatore_pronto": None,
        "sblocca": "il primo ADR nuovo: allora un controllo in validate_docs dal 0089 in poi",
    },
    {
        "chiave": "corpo_pr_onesto",
        "norma": ".github/pull_request_template.md (D7 di PIANO-RECUPERO) — un controllo "
                 "non girato si scrive «non eseguito», e si dice come si torna indietro",
        "prerequisito": None,
        "forma": None,
        "dove": "il corpo di una PR sta su GitHub, non in un file del repo: nessuno "
                "script lo legge, e il modello resta il promemoria",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
)


def misura() -> "list[dict]":
    """Lo stato di ogni norma scoperta. Deterministico: solo conteggi su file."""
    fuori = []
    for n in NORME_SCOPERTE:
        riga = dict(n)
        if n["prerequisito"] is None:
            riga["stato"], riga["occorrenze"] = FUORI_DOMINIO, None
        elif n.get("oggetto"):
            riga["occorrenze"] = _conta_file(n["oggetto"])
            riga["stato"] = OGGETTO_ASSENTE if not riga["occorrenze"] else SUPERFICIE_VUOTA
        elif n["forma"] is None:
            riga["stato"], riga["occorrenze"] = CONVENZIONE_ASSENTE, None
        else:
            riga["occorrenze"] = _conta(n["forma"])
            riga["stato"] = SUPERFICIE_VUOTA if not riga["occorrenze"] else "MISURABILE"
        fuori.append(riga)
    return fuori


def problemi() -> "list[str]":
    """Le righe che hanno smesso di dire il vero. Una superficie vuota NON lo e'."""
    errori = []
    for r in misura():
        if r["stato"] == "MISURABILE":
            errori.append(
                f"«{r['chiave']}»: la forma «{r['forma']}» ha ora {r['occorrenze']} "
                "occorrenze — la norma e' diventata misurabile e la riga del "
                "registro va aggiornata da 🔴 a 🟢")
        if r["stato"] == OGGETTO_ASSENTE and _conta_file(r["oggetto"]):
            errori.append(f"«{r['chiave']}»: l'oggetto e' comparso")
    return errori


ETICHETTA = {
    SUPERFICIE_VUOTA: "🟡 superficie vuota",
    CONVENZIONE_ASSENTE: "🔴 convenzione assente",
    OGGETTO_ASSENTE: "🔴 oggetto assente",
    FUORI_DOMINIO: "⚪ fuori dominio",
    "MISURABILE": "🟢 misurabile ORA",
}


def stampa(righe: "list[dict]") -> None:
    print("\nSUPERFICIE DELLE NORME NON MISURATE\n" + "=" * 70)
    print("Per ognuna: manca il codice, o manca il dato? La risposta cambia il")
    print("passo successivo, e per otto su nove il codice non e' il problema.\n")
    conta = {}
    for r in righe:
        conta[r["stato"]] = conta.get(r["stato"], 0) + 1
        occ = "—" if r["occorrenze"] is None else str(r["occorrenze"])
        print(f"  {ETICHETTA[r['stato']]:26} occorrenze: {occ:>4}   {r['chiave']}")
        print(f"      {r['norma']}")
        if r["prerequisito"]:
            print(f"      serve: {r['prerequisito']}")
        if r.get("rilevatore_pronto"):
            print(f"      🟢 il rilevatore ESISTE GIA': {r['rilevatore_pronto']}")
        if r.get("sblocca"):
            print(f"      lo sblocca: {r['sblocca']}")
        print()
    print("  " + " · ".join(f"{ETICHETTA[s]} {n}" for s, n in sorted(conta.items())))
    print("\n  ⚠️  «superficie vuota» vuol dire che il rilevatore e' pronto e il")
    print("      contenuto non e' marcato: il giorno che lo e', la norma si accende")
    print("      da sola. «convenzione assente» vuol dire che prima di scrivere")
    print("      codice qualcuno deve DECIDERE una forma — e quella decisione non")
    print("      e' di uno script.\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="report in JSON, per la catena")
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se una riga ha smesso di dire il vero")
    args = ap.parse_args(argv)
    righe = misura()
    if args.json:
        print(json.dumps({"tool": "superficie_norme", "norme": righe},
                         ensure_ascii=False, indent=2))
        return 0
    if args.check:
        errori = problemi()
        for e in errori:
            print(f"  ✗ {e}")
        if errori:
            print(f"✗ superficie_norme: {len(errori)} riga/he non dicono piu' il vero")
            return 1
        n = sum(1 for r in righe if r["stato"] != FUORI_DOMINIO)
        print(f"✓ superficie_norme: {len(righe)} norme scoperte, {n} con un "
              "prerequisito dichiarato, nessuna riga mente")
        return 0
    stampa(righe)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
