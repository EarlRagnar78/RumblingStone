#!/usr/bin/env python3
"""extract_statblocks.py — dal Bestiario in prosa al blocco statistiche (ADR-0021).

Cosa fa. Legge le schede di `Bestiario/`, prova a ricavare dai loro numeri il
blocco `statblocco` (vedi `dmcore/statblock.py`) e — con `--apply` — lo scrive
in testa alla scheda **solo dove l'estrazione è completa**. Le altre finiscono
in un rapporto con scritto cosa manca.

È lo stesso mestiere di `import_ultraclear.py` per le mappe: una migrazione
semi-automatica che non inventa. Una scheda migrata a metà, con un numero
dedotto, sarebbe peggio di una scheda non migrata — al tavolo ci si fida di
quello che c'è scritto.

Uso:
    python3 scripts/extract_statblocks.py                 # rapporto, non tocca niente
    python3 scripts/extract_statblocks.py --apply         # scrive i blocchi completi
    python3 scripts/extract_statblocks.py --check         # i blocchi esistenti sono validi?
    python3 scripts/extract_statblocks.py --json          # rapporto machine-readable

`--check` è il gate: verifica che ogni blocco già presente si legga, che i suoi
campi obbligatori ci siano e che il **GS dichiarato nel blocco coincida** con
quello del nome del file (`-crN.md`) — che è il modo tipico in cui una scheda
potenziata resta indietro.

Dipendenze: stdlib.
Exit code: 0 = ok · 1 = `--check` ha trovato blocchi rotti · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.statblock import (  # noqa: E402
    APERTURA, Statblocco, StatblockError, estrai, leggi, rendi,
)

ROOT = Path(__file__).resolve().parent.parent
BESTIARIO = ROOT / "Bestiario"
CR_NEL_NOME = re.compile(r"-cr(\d{1,2})\.md$", re.I)
# `-cr05.md` nel nome vuole dire GS 1/2: la convenzione del repo evita il punto
# nei nomi di file, e confrontarlo alla lettera darebbe due falsi allarmi.
FRAZIONI = {"05": "1/2", "025": "1/4"}


def gs_numerico(v: str) -> float | None:
    """«1/2», «0.5» e «05» sono lo stesso grado di sfida, scritto in tre modi."""
    v = v.strip().replace(" ", "")
    v = FRAZIONI.get(v, v)
    try:
        if "/" in v:
            a, _, b = v.partition("/")
            return float(a) / float(b)
        return float(v)
    except (ValueError, ZeroDivisionError):
        return None


#: Il marcatore che dice «questa scheda NON e' una creatura». Va in testa al
#: file, nella riga di intestazione, e toglie la scheda dal conto del debito.
#:
#: Serve perche' il Bestiario contiene anche cose che una creatura non sono, e
#: forzarci sopra `gs/ca/pf/ts` vorrebbe dire **inventare un mostro che non
#: esiste**: un organo collegiale con sette seggi, una popolazione di profughi,
#: un'ondata di combattimento di massa che e' un aggregato di altre schede, un
#: dossier che punta agli statblocchi che vivono altrove. Finche' non c'era
#: questo marcatore, quelle cinque schede risultavano «da migrare» per sempre —
#: debito che nessuno poteva estinguere, che e' il modo in cui un numero smette
#: di significare qualcosa.
NON_CREATURA = "[NON-CREATURA]"

#: Il marcatore che dice «i numeri di questa creatura stanno ALTROVE, e
#: duplicarli qui sarebbe peggio».
#:
#: È un caso diverso da NON-CREATURA, e tenerli distinti conta. Dieci dossier di
#: PNG e otto di villain non hanno un blocco perché **non devono averlo**: le
#: statistiche sono già scritte, per esteso, dentro i documenti d'arco — le
#: schede stampabili dei pregen in `ARC08-02`, i PNG alleati in `ARC08-01` — e
#: quattro di quelle schede lo dicono a lettere maiuscole: *NON duplicare*.
#: Copiarle qui creerebbe una seconda copia che diverge alla prima errata, ed è
#: esattamente il difetto che ADR-0021 esiste per evitare.
#:
#: ⚠️ **Ma un marcatore che toglie schede dal conto è un marcatore che può
#: nascondere il debito invece di estinguerlo.** Perciò questo, a differenza di
#: NON-CREATURA, **è verificabile**: la riga deve dire dove sono i numeri, e
#: `--check` va a vedere che quel posto esista davvero. Un rimando che punta al
#: vuoto è un errore, non una scheda a posto.
RIMANDO = "[RIMANDO]"


def e_non_creatura(testo: str) -> bool:
    """Vero se la scheda si dichiara non-creatura (nelle prime righe)."""
    return NON_CREATURA in "\n".join(testo.split("\n")[:8])


def e_rimando(testo: str) -> bool:
    """Vero se la scheda dichiara che i suoi numeri stanno altrove."""
    return RIMANDO in "\n".join(testo.split("\n")[:8])


def bersaglio_del_rimando(testo: str) -> str | None:
    """Il file citato dal rimando, se c'è.

    Il formato è quello che le schede usano già: una riga `**Key stats**: → …`
    con il percorso fra apici inversi. Non ne invento uno nuovo — le schede lo
    scrivono così da prima che questo marcatore esistesse.
    """
    # ⚠️ Sulla RIGA, non sul documento. Con `re.S` la ricerca proseguiva oltre la
    # riga fino al primo apice inverso del file: una scheda che scriveva «Key
    # stats: vedi statblock» senza dire quale passava il controllo agganciandosi
    # a un percorso citato trenta righe piu' giu'. Un controllo che si accontenta
    # e' peggio di nessun controllo, perche' fa credere che qualcuno abbia
    # guardato.
    for riga in testo.split("\n"):
        if "**Key stats**" in riga:
            m = re.search(r"`([^`]+)`", riga)
            return m.group(1) if m else None
    return None


def rimando_valido(f: Path, testo: str) -> str | None:
    """`None` se il rimando è a posto, altrimenti il problema.

    Un rimando che non dice dove, o che dice un posto che non esiste, è un modo
    per far sparire il debito dal conto senza estinguerlo. Vale la pena essere
    severi qui: è l'unica cosa che rende il marcatore onesto.
    """
    bersaglio = bersaglio_del_rimando(testo)
    if not bersaglio:
        return f"{f.name}: {RIMANDO} senza una riga «**Key stats**: → `dove`»"
    # I percorsi delle schede sono abbreviati («08_.../ARC08-01-GUIDA-DM.md»):
    # si cerca per nome del file, che è quello che identifica davvero.
    nome = Path(bersaglio.replace("\\", "/")).name
    if not nome.endswith(".md"):
        return None          # rimando a una sezione, non a un file: passa
    if not any(ROOT.rglob(nome)):
        return f"{f.name}: il rimando punta a «{nome}», che non esiste"
    return None


def schede() -> list[Path]:
    return sorted(
        p for p in BESTIARIO.rglob("*.md")
        if not p.name.startswith("README") and "pregen-pcgen" not in p.as_posix()
        and "INDICE" not in p.name
    )


def inserisci(testo: str, sb: Statblocco) -> str:
    """Il blocco va **dopo** il titolo e la riga di intestazione, prima della prosa.

    Sopra il titolo sarebbe un file che non si apre più come una scheda; in
    fondo sarebbe un dato che nessuno vede. Dopo l'intestazione è il posto dove
    un lettore umano si aspetta i numeri.
    """
    if APERTURA in testo or e_non_creatura(testo) or e_rimando(testo):
        return testo
    righe = testo.split("\n")
    taglio = 0
    for i, r in enumerate(righe[:6]):
        if r.startswith("#") or r.startswith("**Faction**"):
            taglio = i + 1
    while taglio < len(righe) and not righe[taglio].strip():
        taglio += 1
    return "\n".join(righe[:taglio] + ["", rendi(sb), ""] + righe[taglio:])


#: Le righe che non sono prosa della scheda ma note su di lei: le marche
#: `[INFERRED]` e le errata. 🐛 Ghaurush porta «CA 23 → **25**» in una marca, e
#: il lettore la prendeva per la CA della prosa.
NOTA = re.compile(r"^\s*(?:>|- ⚠|fonte:)")
#: «GS 17-19»: una forbice non e' un valore da confrontare (Il Collezionista ha
#: 18 nel blocco, ed e' scelto apposta, ADR-0034).
FORBICE_GS = re.compile(r"(?:\bGS\b|\bCR\b|Grado di Sfida)[^\n\d]{0,24}\d{1,2}\s*[-–—]\s*\d{1,2}\b")
NUMERI = re.compile(r"[+-]?\d+")
#: Una sezione che descrive **un'altra** serie di statistiche della stessa
#: creatura: la forma umana di un druido che combatte in forma d'orso (D7), una
#: variante. I suoi numeri sono diversi per definizione, e non sono la prosa del
#: blocco. Si taglia dall'intestazione alla successiva di pari livello o piu' alta.
ALTRA_FORMA = re.compile(r"^(#{2,4})\s+(?:Forma|Variante)\b", re.I)


def senza_altre_forme(testo: str) -> str:
    fuori, livello = [], None
    for riga in testo.splitlines():
        m = re.match(r"^(#{1,6})\s", riga)
        if livello is not None and m and len(m.group(1)) <= livello:
            livello = None
        a = ALTRA_FORMA.match(riga)
        if a:
            livello = len(a.group(1))
        if livello is None:
            fuori.append(riga)
    return "\n".join(fuori)


def diverge_dalla_prosa(testo: str, sb: Statblocco) -> list[str]:
    """I campi del blocco che la prosa della STESSA scheda scrive diversi.

    🐛 **Perche' esiste** (2026-09-23): il 2 settembre `derive_statblocks
    --apply-ts` ha scritto i TS di sei dossier con una matrice sua, perche' il
    lettore non vedeva ancora la forma «- **Tempra:** +7». Il giorno dopo il
    lettore l'ha imparata, e nessuno ha riletto i sei blocchi: Salvatore e'
    rimasto tre settimane con Riflessi +6 dove il DM aveva scritto +13. Nessun
    cancello confrontava il blocco con la prosa accanto.

    Si confrontano solo i numeri: pf, CA e GS per il primo, i TS tutti e tre.
    Dove la prosa scrive una forbice il campo si salta. Il verso della
    correzione non lo decide questo controllo: dice solo che uno dei due e'
    rimasto indietro.
    """
    from dmcore.statblock import togli_blocco
    prosa = "\n".join(r for r in senza_altre_forme(togli_blocco(testo)).splitlines()
                      if not NOTA.match(r))
    try:
        letto, _ = estrai(prosa)
    except Exception:          # un lettore che crolla non e' una divergenza
        return []
    fuori = []
    for campo in ("pf", "ca", "gs", "ts"):
        b, p = getattr(sb, campo, ""), getattr(letto, campo, "")
        if not (b and p):
            continue
        if campo == "gs":
            if FORBICE_GS.search(prosa) or gs_numerico(b) == gs_numerico(p):
                continue
        elif campo == "ts":
            if NUMERI.findall(b)[:3] == NUMERI.findall(p)[:3]:
                continue
        elif NUMERI.findall(b)[:1] == NUMERI.findall(p)[:1]:
            continue
        fuori.append(f"`{campo}` del blocco «{b}», la prosa della scheda scrive «{p}»")
    return fuori


def controlla(f: Path) -> list[str]:
    """I problemi del blocco di UNA scheda (lista vuota = tutto bene)."""
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    testo = f.read_text(encoding="utf-8")
    if e_rimando(testo):
        guasto = rimando_valido(f, testo)
        return [f"{rel}: {guasto.split(': ', 1)[1]}"] if guasto else []
    try:
        sb = leggi(testo)
    except StatblockError as e:
        return [f"{rel}: {e}"]
    if sb is None:
        return []
    problemi = []
    m = CR_NEL_NOME.search(f.name)
    atteso = FRAZIONI.get(m.group(1), m.group(1)) if m else None
    if atteso and sb.gs and gs_numerico(sb.gs) != gs_numerico(atteso):
        problemi.append(f"{rel}: il blocco dice GS {sb.gs} e il nome del file dice "
                        f"GS {atteso} — uno dei due è rimasto indietro")
    for d in diverge_dalla_prosa(testo, sb):
        problemi.append(f"{rel}: {d} — uno dei due è rimasto indietro")
    return problemi


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", nargs="*", help="schede da trattare (default: tutto il Bestiario)")
    ap.add_argument("--apply", action="store_true",
                    help="scrive il blocco nelle schede dove l'estrazione è COMPLETA")
    ap.add_argument("--check", action="store_true",
                    help="verifica i blocchi già presenti (gate CI); non scrive niente")
    ap.add_argument("--json", action="store_true", help="rapporto machine-readable")
    args = ap.parse_args()

    elenco = [Path(x).resolve() for x in args.file] or schede()
    for f in elenco:
        if not f.is_file():
            print(f"✗ scheda non trovata: {f}", file=sys.stderr)
            return 2

    if args.check:
        problemi = [p for f in elenco for p in controlla(f)]
        testi = {f: f.read_text(encoding="utf-8") for f in elenco}
        conblocco = sum(1 for f in elenco if APERTURA in testi[f])
        nrimandi = sum(1 for f in elenco if e_rimando(testi[f]))
        nnoncreature = sum(1 for f in elenco if e_non_creatura(testi[f]))
        # Il conto che conta: quante schede sono SISTEMATE, non quante hanno il
        # blocco. Una scheda-rimando verificata è sistemata quanto una col
        # blocco — i numeri esistono, stanno dove la scheda dice.
        sistemate = conblocco + nrimandi + nnoncreature
        if args.json:
            print(json.dumps({"schede": len(elenco), "con_blocco": conblocco,
                              "rimandi": nrimandi, "non_creature": nnoncreature,
                              "sistemate": sistemate,
                              "problemi": problemi}, ensure_ascii=False, indent=2))
        else:
            for p in problemi:
                print(f"  ✗ {p}", file=sys.stderr)
            stato = "✓" if not problemi else "✗"
            coda = ""
            if nrimandi or nnoncreature:
                pezzi = []
                if nrimandi:
                    pezzi.append(f"{nrimandi} coi numeri altrove")
                if nnoncreature:
                    pezzi.append(f"{nnoncreature} non-creature")
                coda = f" (+ {', '.join(pezzi)} → {sistemate}/{len(elenco)} sistemate)"
            print(f"{stato} extract_statblocks --check: {conblocco}/{len(elenco)} schede "
                  f"hanno il blocco{coda}, {len(problemi)} problemi")
        return 1 if problemi else 0

    completi, parziali, gia, non_creature, rimandi = [], [], [], [], []
    for f in elenco:
        testo = f.read_text(encoding="utf-8")
        if e_non_creatura(testo):
            non_creature.append(f)
            continue
        if e_rimando(testo):
            rimandi.append(f)
            continue
        if APERTURA in testo:
            gia.append(f)
            continue
        sb, mancanti = estrai(testo)
        if mancanti:
            parziali.append((f, mancanti))
        else:
            completi.append((f, sb))

    if args.apply:
        for f, sb in completi:
            f.write_text(inserisci(f.read_text(encoding="utf-8"), sb), encoding="utf-8")

    rel = lambda f: str(f.relative_to(ROOT))  # noqa: E731
    if args.json:
        print(json.dumps({
            "schede": len(elenco),
            "gia_migrate": [rel(f) for f in gia],
            "non_creature": [rel(f) for f in non_creature],
            "rimandi": [rel(f) for f in rimandi],
            "completi": [rel(f) for f, _ in completi],
            "parziali": {rel(f): m for f, m in parziali},
            "applicato": bool(args.apply),
        }, ensure_ascii=False, indent=2))
        return 0

    verbo = "scritti" if args.apply else "pronti (nessuna scrittura: manca --apply)"
    print(f"  {len(gia)} schede hanno già il blocco")
    if non_creature:
        print(f"  {len(non_creature)} non sono creature e non ne devono avere uno "
              f"(marcate {NON_CREATURA})")
    if rimandi:
        print(f"  {len(rimandi)} hanno i numeri altrove e non vanno duplicati "
              f"(marcate {RIMANDO}; --check verifica che il bersaglio esista)")
    print(f"  {len(completi)} blocchi {verbo}")
    print(f"  {len(parziali)} schede da fare a mano — la prosa non dice tutto:")
    conteggio: dict[str, int] = {}
    for _, m in parziali:
        for c in m:
            conteggio[c] = conteggio.get(c, 0) + 1
    for campo, n in sorted(conteggio.items(), key=lambda x: -x[1]):
        print(f"      manca «{campo}» in {n}")
    for f, m in parziali[:12]:
        print(f"      · {rel(f)} → manca {', '.join(m)}")
    if len(parziali) > 12:
        print(f"      … e altre {len(parziali) - 12} (usa --json per l'elenco intero)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
