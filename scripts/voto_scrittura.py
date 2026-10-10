#!/usr/bin/env python3
"""voto_scrittura.py — il voto deterministico sui testi delle skill di scrittura.

L11 di PIANO-AGENT-SKILLS-ESTERNE. Il metodo e' quello di L8 e di D10
sull'instradamento, portato dalla scelta della skill alla sua uscita: casi in
due meta' (taratura e verifica), corse con e senza skill, le skill si
correggono solo sui fallimenti di taratura e il miglioramento si legge sulla
verifica. Lo schema dei casi viene da evals.json di skill-creator (Anthropic,
Apache 2.0): prompt, uscita attesa, aspettative. Qui le aspettative sono
CONTROLLI, e ognuno chiama un rilevatore che esiste gia'
(«una norma, un rilevatore», REGISTRO-NORME-EDITORIALI):

    misura_craft   box_read_aloud · difetti_dei_box · box_con_p1 ·
                   metrature_nei_box · CONGEGNI · _ETICHETTA
    validate_prosa rilievi (calchi, antitesi, maiuscole, trattino, ancore) ·
                   prosa_documento · conteggi_annunciati · ANTITESI · TRATTINO

Una sola regex e' nuova, ed e' di una norma nuova: «sembra» e «pare» nei box
(Shawn Merwin, D13 del 2026-10-01). Fino alla decisione era un indizio che si
stampava e non pesava; ora e' il controllo `box_senza_sembra`, registrato.

Un controllo dice se una norma registrata e' rispettata, non se il testo e'
bello. Il giudizio sulla voce resta alla lettura ad alta voce
(`passate-redazionali.md`, 2a passata).

    python3 scripts/voto_scrittura.py FILE --caso S01   # i controlli su un file
    python3 scripts/voto_scrittura.py --corse           # la tabella delle corse
    python3 scripts/voto_scrittura.py --emit            # scrive voti.json
    python3 scripts/voto_scrittura.py --check           # esce 1 se voti.json e' vecchio
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import misura_craft as mc  # noqa: E402
import validate_prosa as vp  # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "plans" / "scrittura"
CASI = CARTELLA / "casi.json"
CORSE = CARTELLA / "corse"
VOTI = CARTELLA / "voti.json"

_CONGEGNI = {nome: rx for nome, rx, _ in mc.CONGEGNI}
_DECISIONE = _CONGEGNI["chiusura su decision point"]
_DIALOGO = _CONGEGNI["dialogo nella forma dichiarata"]
_HDYWTDT = _CONGEGNI["[HDYWTDT] il finisher al giocatore"]

#: La norma di Merwin, «evitare sembra e pare» (D13). «Come se» resta fuori: e'
#: un paragone, non un'esitazione. Misurata sui 501 box dei file di gioco il
#: 2026-10-01: 34 box con una di queste forme.
#: ⚠️ Il 2026-10-02 la prima prova di `ciclo_prosa` ha trovato «ti è sembrato»
#: in un box che il metro dava pulito: mancavano il participio e il passato
#: remoto, che nella prosa al passato sono le forme più comuni.
#: ⚠️ Lo stesso giorno, leggendo i 34 box uno per uno per il lotto: «appare» era
#: nel rilevatore ma non nella norma, che dice «sembra» e «pare». E nei file di
#: gioco vuol dire quasi sempre «diventa visibile» («Hella appare
#: nell'affresco»): quattro box su quattro. Tolto, e il conto scende da 34 a 30.
SEMBRA = re.compile(r"\b(sembr(?:a|ano|ava|avano|are|ato|ata|ati|ate|ò|arono)|"
                    r"pa(?:re|iono|reva|revano|rso|rsa|rsi|rse|rve|rvero))\b", re.I)

#: D17 (2026-10-03): «sembra» seguito dalla smentita è lecito. «Quella che
#: sembrava una parete — è una palpebra»: lì il narratore non esita, prepara il
#: colpo. Il confine è stretto apposta: la smentita deve arrivare entro la frase
#: dopo, con «invece», «non lo è», «si rivela» o un trattino seguito da «è».
#: Un «è» da solo non basta: c'è in quasi ogni frase, e salverebbe tutto.
SMENTITA = re.compile(r"\b(?:invece|non lo (?:è|era|sono|erano)|"
                      r"si rivel(?:a|ano|ava|avano|ò|arono))\b|\s[—–-]\s*(?:è|era)\b", re.I)
_FINE_FRASE = re.compile(r"[.!?…]+")


def sembra_esitanti(corpo: str) -> "list[re.Match]":
    """I «sembra» e «pare» di un box che la norma vieta: tutti, tranne quelli
    smentiti entro la frase dopo (D17)."""
    fuori = []
    for m in SEMBRA.finditer(corpo):
        dopo = corpo[m.end():]
        fini = list(_FINE_FRASE.finditer(dopo))
        limite = fini[1].end() if len(fini) > 1 else len(dopo)
        if not SMENTITA.search(dopo[:limite]):
            fuori.append(m)
    return fuori


def _rilievi(testo: str, per_i_giocatori: bool) -> "set[str]":
    """Le chiavi di `validate_prosa.rilievi` sul testo, come se fosse un file.

    Il nome del file e' l'unico modo in cui `validate_prosa` sa che un testo e'
    per i giocatori: un handout si chiama HANDOUT-, il resto no.
    """
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / ("HANDOUT-prova.md" if per_i_giocatori else "prova.md")
        f.write_text(testo, encoding="utf-8")
        return {k for k, _ in vp.rilievi(f)}


def _corpi(testo: str) -> "list[str]":
    return [mc._ETICHETTA.sub("", " ".join(b)) for b in mc.box_read_aloud(testo)]


def _box_etichettati(testo: str) -> int:
    """Quanti box hanno l'etichetta di regia sulla prima riga o subito sopra.

    `editorial-standards` §2 prescrive `**Read-aloud (pilastro lead).**` e non
    dice su che riga stia. `misura_craft.box_read_aloud` riconosce il box solo
    dalla riga in corsivo, quindi un'etichetta su una riga sua (dentro la
    citazione o appena fuori) restava esclusa dal box e il box risultava
    senza. Trovato sulla tornata B di L11: tre bocciature su tre erano questa
    forma, e la norma la ammette.
    """
    righe = testo.splitlines()
    inizi = []
    for b in mc.box_read_aloud(testo):
        # l'indice della prima riga del box nel testo: si cerca in avanti,
        # dopo l'inizio precedente, perche' due box possono avere righe uguali
        da = inizi[-1] + 1 if inizi else 0
        inizi.append(next(i for i in range(da, len(righe)) if righe[i] == b[0]))
    n = 0
    for i in inizi:
        if mc._ETICHETTA.search(righe[i]):
            n += 1
            continue
        j = i - 1
        while j >= 0 and righe[j].strip().lstrip(">").strip() == "":
            j -= 1
        # Il paragrafo subito sopra, non la sua ultima riga: l'etichetta va a
        # capo quando porta una condizione («**Read-aloud (X).** *Da leggere
        # solo se…*»). Trovato sulla tornata C, due bocciature su tre.
        paragrafo = []
        while j >= 0 and righe[j].strip().lstrip(">").strip() != "":
            paragrafo.append(righe[j])
            j -= 1
        if any(mc._ETICHETTA.search(r) for r in paragrafo):
            n += 1
    return n


def _doc_trattini(testo: str) -> "tuple[bool, str]":
    # La soglia per mille di validate_prosa --documenti, senza il pavimento delle
    # quaranta righe: un corpo di PR ne ha quindici, e li' la densita' si legge
    # lo stesso. Un trattino solo passa sempre (prosa-documenti: «se in un
    # paragrafo ne servono due, il paragrafo va riscritto»).
    righe = vp.prosa_documento(testo)
    n = len(vp.TRATTINO.findall("\n".join(righe)))
    per_mille = n * 1000 // max(len(righe), 1)
    return n <= 1 or per_mille <= vp.SOGLIE_DOC["trattino_per_mille"], f"{n} in {len(righe)} righe"


def controlli(testo: str, genere: str) -> "dict[str, tuple[bool, str]]":
    """Tutti i controlli calcolabili sul testo: (rispettato, dettaglio)."""
    box = mc.box_read_aloud(testo)
    corpi = _corpi(testo)
    difetti = mc.difetti_dei_box(testo)
    giocatori = genere == "per un giocatore"
    chiavi = _rilievi(testo, giocatori)
    prosa_doc = "\n".join(vp.prosa_documento(testo))
    p1 = mc.box_con_p1(testo)
    metr = mc.metrature_nei_box(testo)
    senza_etichetta = len(box) - _box_etichettati(testo)
    return {
        "box_presente": (bool(box), f"{len(box)} box"),
        "box_tetto_righe": (difetti["oltre 12 righe"] == 0, f"{difetti['oltre 12 righe']} oltre 12 righe"),
        "box_un_nome": (difetti[">1 nome proprio"] == 0, f"{difetti['>1 nome proprio']} con piu' nomi"),
        "box_senza_parentesi": (difetti["con parentesi"] == 0, f"{difetti['con parentesi']} con parentesi"),
        "box_senza_sembra": (not any(sembra_esitanti(c) for c in corpi),
                             ", ".join(sorted({m.group(0).lower() for c in corpi
                                               for m in sembra_esitanti(c)})) or "-"),
        "box_p1": (not p1, ", ".join(v for v, _ in p1) or "-"),
        "box_senza_metrature": (not metr, ", ".join(m for m, _ in metr) or "-"),
        "box_etichettato": (bool(box) and senza_etichetta == 0, f"{senza_etichetta} senza etichetta"),
        "chiude_che_fate": (any(_DECISIONE.search(c) for c in corpi), "-"),
        "hdywtdt": (bool(_HDYWTDT.search(testo)), "-"),
        "dialogo_forma": (bool(_DIALOGO.search(testo)), f"{len(_DIALOGO.findall(testo))} battute"),
        "calchi": ("calco_dall_inglese" not in chiavi, "-"),
        "tic_gioco": (not chiavi & {"antitesi_ripetuta", "maiuscole_di_enfasi", "trattino_come_respiro"},
                      ", ".join(sorted(chiavi & {"antitesi_ripetuta", "maiuscole_di_enfasi",
                                                 "trattino_come_respiro"})) or "-"),
        "ancore": ("testo_giocatori_senza_ancore" not in chiavi, "-"),
        "doc_senza_box": (not box, f"{len(box)} box"),
        "doc_trattini": _doc_trattini(testo),
        "doc_conteggi": (len(vp.conteggi_annunciati(prosa_doc)) <= vp.SOGLIE_DOC["conteggio"],
                         f"{len(vp.conteggi_annunciati(prosa_doc))}"),
        "doc_antitesi": (len(vp.ANTITESI.findall(prosa_doc)) <= vp.SOGLIE_DOC["antitesi"],
                         f"{len(vp.ANTITESI.findall(prosa_doc))}"),
    }


def indizi(testo: str) -> "dict[str, int]":
    """Numeri che si stampano e non pesano."""
    corpi = _corpi(testo)
    return {
        "box senza c'e'/dislocazione": len(mc.box_senza_costrutto_italiano(testo)),
        "parole nei box": sum(len(c.split()) for c in corpi),
    }


def leggi_casi(percorso: Path = CASI) -> "list[dict]":
    return json.loads(percorso.read_text(encoding="utf-8"))["casi"]


def vota(testo: "str | None", caso: dict) -> "dict[str, bool]":
    """I controlli del caso. Un testo che manca li fallisce tutti."""
    if testo is None:
        return {c: False for c in caso["controlli"]}
    tutti = controlli(testo, caso["genere"])
    return {c: tutti[c][0] for c in caso["controlli"]}


def condizione(nome_corsa: str) -> str:
    """`A-con-2` -> `A-con`: le ripetizioni della stessa corsa si sommano."""
    return re.sub(r"-\d+$", "", nome_corsa)


def voti_delle_corse(corse: Path = CORSE, casi: "list[dict] | None" = None) -> dict:
    casi = casi if casi is not None else leggi_casi()
    out: dict = {}
    # Una cartella senza nemmeno un testo e' una corsa che non e' partita (un
    # limite dell'API, un agente fermato): contarla darebbe zero a tutti i
    # controlli. Un caso che manca in una corsa partita, invece, fallisce.
    cartelle = sorted(p for p in corse.iterdir() if p.is_dir() and any(p.glob("*.md"))) \
        if corse.is_dir() else []
    for d in cartelle:
        out[d.name] = {}
        # Una tornata puo' girare su un insieme solo (la C, sulla sola
        # verifica): l'insieme di cui la corsa non ha scritto nemmeno un caso
        # non e' stato chiesto, e non vale zero.
        scritti = {c["insieme"] for c in casi if (d / f"{c['id']}.md").is_file()}
        for caso in casi:
            if caso["insieme"] not in scritti:
                continue
            f = d / f"{caso['id']}.md"
            testo = f.read_text(encoding="utf-8") if f.is_file() else None
            out[d.name][caso["id"]] = vota(testo, caso)
    return out


def riepilogo(voti: dict, casi: "list[dict]") -> "dict[str, dict[str, list[int]]]":
    """condizione -> insieme -> [rispettati, controlli]."""
    insieme = {c["id"]: c["insieme"] for c in casi}
    out: "dict[str, dict[str, list[int]]]" = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for corsa, per_caso in voti.items():
        for cid, esiti in per_caso.items():
            r = out[condizione(corsa)][insieme[cid]]
            r[0] += sum(esiti.values())
            r[1] += len(esiti)
    return {k: dict(v) for k, v in out.items()}


def fallimenti(voti: dict, insieme_: str, casi: "list[dict]") -> "dict[str, dict[str, int]]":
    """condizione -> controllo -> quante volte fallisce, sull'insieme dato."""
    insieme = {c["id"]: c["insieme"] for c in casi}
    out: "dict[str, dict[str, int]]" = defaultdict(lambda: defaultdict(int))
    for corsa, per_caso in voti.items():
        for cid, esiti in per_caso.items():
            if insieme[cid] != insieme_:
                continue
            for c, ok in esiti.items():
                if not ok:
                    out[condizione(corsa)][c] += 1
    return {k: dict(v) for k, v in out.items()}


def stampa(voti: dict, casi: "list[dict]") -> None:
    rie = riepilogo(voti, casi)
    print("| condizione | taratura | verifica |")
    print("|---|---:|---:|")
    for cond in sorted(rie):
        celle = []
        for ins in ("taratura", "verifica"):
            ok, tot = rie[cond].get(ins, [0, 0])
            celle.append(f"{ok}/{tot} ({100 * ok // tot}%)" if tot else "—")
        print(f"| {cond} | {celle[0]} | {celle[1]} |")
    for ins in ("taratura", "verifica"):
        print(f"\nFallimenti in {ins}:")
        for cond, per_c in sorted(fallimenti(voti, ins, casi).items()):
            dettaglio = ", ".join(f"{c} {n}" for c, n in sorted(per_c.items(), key=lambda x: -x[1]))
            print(f"  {cond}: {dettaglio or '-'}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", nargs="?", type=Path, help="un testo da votare")
    ap.add_argument("--caso", help="l'id del caso da usare per il file (S01…)")
    ap.add_argument("--corse", action="store_true", help="la tabella delle corse")
    ap.add_argument("--emit", action="store_true", help="scrive plans/scrittura/voti.json")
    ap.add_argument("--check", action="store_true", help="esce 1 se voti.json non torna")
    a = ap.parse_args(argv)
    casi = leggi_casi()

    if a.file:
        caso = next((c for c in casi if c["id"] == a.caso), None)
        genere = caso["genere"] if caso else "apertura"
        testo = a.file.read_text(encoding="utf-8")
        tutti = controlli(testo, genere)
        scelti = caso["controlli"] if caso else list(tutti)
        for c in scelti:
            ok, det = tutti[c]
            print(f"{'✓' if ok else '✗'} {c}: {det}")
        for k, v in indizi(testo).items():
            print(f"  · {k}: {v}")
        return 0

    voti = voti_delle_corse(casi=casi)
    if a.emit:
        VOTI.write_text(json.dumps(voti, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✓ scritto {VOTI.relative_to(RADICE)}: {len(voti)} corse")
        return 0
    if a.check:
        salvati = json.loads(VOTI.read_text(encoding="utf-8")) if VOTI.is_file() else None
        if salvati != voti:
            print("✗ voto_scrittura: voti.json non corrisponde alle corse; "
                  "riesegui con --emit e aggiorna RISULTATI.md")
            return 1
        print(f"✓ voto_scrittura: {len(voti)} corse, voti.json allineato")
        return 0
    stampa(voti, casi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
