"""derive_statblocks.py — la derivazione dalle tabelle, e perché PROPONE e non scrive.

ADR-0033, che emenda ADR-0021.

`extract_statblocks.py` **trascrive**: legge i numeri dalla prosa. Questo script
doveva fare l'altra metà — **derivarli** dalle tabelle, con la gerarchia di fonti
scelta dal DM: **SRD 3.5 prima**, contenuto libero Pathfinder 1e solo dove il SRD
non ha un equivalente.

    dai DV e dal tipo di creatura   →  dado dei DV, BAB, TS buoni e cattivi   [SRD]
    dai livelli di classe           →  TS base per classe, dado dei DV        [SRD]
    dalla matrice elite/standard    →  le caratteristiche (15,14,13,12,10,8)  [SRD]
    dalla taglia                    →  armatura naturale, modificatore di CA  [SRD]
    dall'equipaggiamento nominato   →  bonus d'armatura e scudo               [SRD]
    dal GS                          →  il COLLAUDO                       [PF1e T.1–1]

⚠️ **Non esiste un `--apply`, ed è il risultato del lotto H, non una mancanza.**
Esiste `--apply-ts`, e dal 2026-09-23 (D11) scrive i TS **insieme alle
caratteristiche da cui vengono**, prese da `genera_attributi`: la prima volta
che ha scritto, il 2 settembre, i suoi TS venivano da una matrice che le
caratteristiche scritte poi accanto contraddicevano.

Provato: con quelle tabelle e quel collaudo, **nessuna** delle schede rimaste
produce numeri che superino il proprio controllo di sanità. Le schede sono
documenti in prosa, non dati: una espressione regolare ci trova sempre qualcosa
di plausibile, e il modo in cui sbaglia non è rumoroso — è «CA 11 per un mostro
di GS 9», che ha l'aria di un conto e non di un errore. Un numero così entra nel
canone e ci resta fino al tavolo.

Perciò lo strumento **propone**, mostrando il conto per esteso, e la mano che
scrive resta quella del DM. È la stessa disciplina di `import_ultraclear.py` per
le mappe — bozza più rapporto — e la stessa ragione: **una scheda con un numero
dedotto in silenzio è peggio di una scheda non migrata** (ADR-0021 §3).

La tabella per GS di Pathfinder è usata **come guardia, non come fonte**: non
fornisce valori, rifiuta i nostri quando sono assurdi. È il ruolo per cui serve
davvero, ed è anche il motivo per cui non ne prendiamo i numeri: sono tarati su
PF1e, che a parità di GS è più duro del 3.5 su cui questa campagna gira.

Uso:

    python3 scripts/derive_statblocks.py                 # il rapporto
    python3 scripts/derive_statblocks.py --json          # machine-readable
    python3 scripts/derive_statblocks.py <file>...       # solo queste schede

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BESTIARIO = ROOT / "Bestiario"
sys.path.insert(0, str(ROOT / "scripts"))
from dmcore.statblock import Statblocco, rendi  # noqa: E402
from dmcore.statblock import estrai  # noqa: E402
from extract_statblocks import APERTURA, e_non_creatura, inserisci, schede  # noqa: E402

# ===========================================================================
# Le tabelle. Stanno in dmcore/tabelle.py, con la provenienza riga per riga.
# ===========================================================================
# Stavano qui, ed erano l'unica copia finché il generatore non ha avuto bisogno
# delle stesse righe. Due copie delle stesse tabelle divergono: e' successo al
# manifest dei tool, e li' se n'e' accorto un lettore nuovo. Qui il lettore nuovo
# e' `genera_creatura.py`.
from dmcore.tabelle import (  # noqa: E402
    ALIAS_TIPO, ARMATURE, BASIC, CLASSI, ELITE, PER_GS as _PER_GS_PIENA,
    PER_GS_VERIFICATE, RUOLI_ELITE, SCUDI, TAGLIE, TIPI,
    media_dado, mod, ts_buono, ts_cattivo,  # noqa: F401 (ts_*: li legge test_bestiario_h)
)
from dmcore.progressione import ts_base_di  # noqa: E402

#: Il collaudo usa due sole colonne della riga per GS: CA e pf. Le altre
#: (attacco, danno, CD, tiri salvezza) servono al generatore, non a chi legge.
PER_GS = {gs: (riga[0], riga[1]) for gs, riga in _PER_GS_PIENA.items()}


# ===========================================================================
# Leggere la scheda
# ===========================================================================
_CLASSI_RE = re.compile(r"\b(" + "|".join(sorted(CLASSI, key=len, reverse=True))
                        + r")\s*(\d{1,2})\b", re.I)
_DV_RE = re.compile(r"\b(\d{1,2})\s*d\s*(4|6|8|10|12)\b", re.I)
_GS_RE = re.compile(r"\*\*CR\*\*:\s*(\d{1,2})|\bGS\s*(\d{1,2})\b|-cr(\d{1,2})\b", re.I)
_RUOLO_RE = re.compile(r"\*\*Role\*\*:\s*([^|\n]+)", re.I)


@dataclass
class Lettura:
    """Quello che la scheda dice davvero, senza inventare niente."""
    nome: str
    gs: int | None = None
    dv: int | None = None
    dado: int | None = None
    tipo: str | None = None
    taglia: str = "medium"
    classi: list[tuple[str, int]] = field(default_factory=list)
    armatura: tuple[int, int] | None = None
    scudo: int = 0
    elite: bool = False
    manca: list[str] = field(default_factory=list)
    #: la base dei TS che `deriva` calcola, senza caratteristiche: serve a
    #: `--apply-ts` per rifare il conto con gli `attributi` di genera_attributi
    base_ts: dict = field(default_factory=dict)


def leggi_scheda(f: Path) -> Lettura:
    t = f.read_text(encoding="utf-8")
    testa = t[:4000]
    L = Lettura(nome=f.stem)

    m = _GS_RE.search(testa) or _GS_RE.search(f.name)
    if m:
        L.gs = int(next(g for g in m.groups() if g))

    ruolo = _RUOLO_RE.search(testa)
    testo_ruolo = (ruolo.group(1) if ruolo else "") + " " + f.stem
    L.elite = any(r in testo_ruolo.lower() for r in RUOLI_ELITE)

    # ⚠️ Deduplicare, e per (classe, livello). «Orco Regular (Warrior 4)» nel
    # titolo e «Warrior 4» nella prosa sono LA STESSA cosa detta due volte: la
    # prima versione contava 8 DV invece di 4, e poi ci sommava i «4d8» della
    # frase dei pf — dodici DV per un orco di GS 3, e 48 pf.
    visti = set()
    for nome, liv in _CLASSI_RE.findall(testa):
        chiave = (nome.lower(), int(liv))
        if chiave not in visti:
            visti.add(chiave)
            L.classi.append(chiave)
    # ⚠️ La STESSA classe con due livelli diversi vuol dire che la scheda
    # descrive la build in due modi — «Chierico 10 / Prestige …» piu' avanti
    # «Chierico 13, con domini Lolth» — e da fuori non si sa quale sia il
    # totale. Sommarli dava 23 DV e Tempra +17 per un GS 13. Non e' un caso da
    # indovinare: e' un caso da rifiutare.
    doppie = {c for c, _ in L.classi if sum(1 for x, _ in L.classi if x == c) > 1}
    if doppie:
        L.manca.append("la scheda descrive la build in due modi (classe «"
                       + "», «".join(sorted(doppie)) + "» con livelli diversi): "
                       "quale sia il totale non si deduce")
        L.classi = []

    m = _DV_RE.search(testa)
    if m:
        n, d = int(m.group(1)), int(m.group(2))
        # I DV razziali si sommano ai livelli di classe SOLO se non sono gli
        # stessi: «Warrior 4 … 4d8+8» e' un modo di scrivere lo stesso numero.
        if not any(liv == n for _, liv in L.classi):
            L.dv, L.dado = n, d

    basso = testa.lower()
    for alias, tipo in list(ALIAS_TIPO.items()) + [(k, k) for k in TIPI]:
        if alias in basso:
            L.tipo = tipo
            break
    for taglia in TAGLIE:
        if re.search(rf"\b{taglia}\b", basso):
            L.taglia = taglia
            break
    for nome, val in ARMATURE.items():
        if nome in basso:
            L.armatura = val
            break
    for nome, val in SCUDI.items():
        if nome in basso:
            L.scudo = val
            break
    return L


# ===========================================================================
# Derivare
# ===========================================================================
def deriva(L: Lettura) -> tuple[Statblocco | None, list[str], list[str]]:
    """(blocco, conti, cosa manca). Se manca qualcosa, il blocco e' None."""
    manca, conti = list(L.manca), []
    if manca:
        return None, conti, manca
    arr = ELITE if L.elite else BASIC
    matrice = "elite" if L.elite else "standard"

    dv_tot = sum(n for _, n in L.classi)
    if L.dv:
        dv_tot += L.dv
    if not dv_tot:
        manca.append("DV o livelli di classe")
        return None, conti, manca
    # ⚠️ Il tipo o una classe devono essere DETTI. Senza, il dado dei DV e i TS
    # buoni sarebbero una scelta nostra, non una lettura — e da li' in poi ogni
    # numero sarebbe inventato con l'aria di essere calcolato.
    if not L.classi and not L.tipo:
        manca.append("tipo di creatura (senza, dado dei DV e TS buoni sono una scelta)")
        return None, conti, manca

    # --- caratteristiche: la matrice, assegnata per priorita' di ruolo -----
    # Ordine SRD per un combattente: For, Cos, Des, Sag, Car, Int. Non e' un
    # giudizio: e' l'ordine che il SRD usa per i PNG guerrieri, ed e' scritto
    # qui perche' chiunque lo possa rifare uguale.
    forza, cos, des = arr[0], arr[1], arr[2]
    # +1 a una caratteristica ogni 4 DV (SRD)
    bonus = dv_tot // 4
    cos += bonus // 2
    forza += bonus - bonus // 2
    conti.append(f"caratteristiche: matrice {matrice} {arr} + {bonus} da DV/4 "
                 f"→ For {forza}, Cos {cos}, Des {des}")

    # --- pf ---------------------------------------------------------------
    if L.classi:
        pezzi = [(c, n, CLASSI[c][0]) for c, n in L.classi]
        somma = sum(media_dado(d) * n for _, n, d in pezzi)
        det = " + ".join(f"{n}d{d}" for _, n, d in pezzi)
    elif L.dado or L.tipo:
        d = L.dado or TIPI[L.tipo][0]
        somma = media_dado(d) * dv_tot
        det = f"{dv_tot}d{d}"
    else:
        manca.append("pf (né classe né tipo: il dado dei DV è ignoto)")
        return None, conti, manca
    pf = int(somma + mod(cos) * dv_tot)
    conti.append(f"pf: {det} media {somma:.1f} + Cos {mod(cos):+d}×{dv_tot} = {pf}")

    # --- TS ---------------------------------------------------------------
    base = {"temp": 0, "rifl": 0, "vol": 0}
    if L.classi:
        for c, n in L.classi:
            per_classe = ts_base_di(n, CLASSI[c][1])
            for k in base:
                base[k] += per_classe[k]
        det_ts = "somma dei TS base di ogni classe (SRD: multiclasse si sommano)"
    else:
        buoni = TIPI[L.tipo][2] if L.tipo else ()
        base = ts_base_di(dv_tot, buoni)
        det_ts = f"tipo «{L.tipo}», TS buoni {buoni or '—'}"
    L.base_ts = dict(base)
    temp = base["temp"] + mod(cos)
    rifl = base["rifl"] + mod(des)
    vol = base["vol"] + mod(arr[3])          # Sag dalla matrice
    conti.append(f"TS: {det_ts} → Temp {temp:+d}, Rifl {rifl:+d}, Vol {vol:+d}")

    # --- CA ---------------------------------------------------------------
    nat, size_mod = TAGLIE[L.taglia]
    pezzi_ca = [f"10", f"taglia {size_mod:+d}", f"Des {mod(des):+d}"]
    ca = 10 + size_mod + mod(des)
    if nat:
        ca += nat
        pezzi_ca.append(f"naturale +{nat} ({L.taglia})")
    if L.armatura:
        bonus_arm, max_des = L.armatura
        # il massimo Des dell'armatura puo' tagliare il bonus
        taglio = min(mod(des), max_des) - mod(des)
        ca += bonus_arm + taglio
        pezzi_ca.append(f"armatura +{bonus_arm}"
                        + (f" (max Des {max_des}: {taglio:+d})" if taglio else ""))
    if L.scudo:
        ca += L.scudo
        pezzi_ca.append(f"scudo +{L.scudo}")
    if not L.armatura and not nat:
        manca.append("ca (nessuna armatura nominata e nessuna armatura naturale "
                     "dalla taglia: il numero sarebbe inventato)")
        return None, conti, manca
    conti.append(f"CA: {' + '.join(pezzi_ca)} = {ca}")

    # --- collaudo sul GS --------------------------------------------------
    # La tabella per GS e' una **guardia**, non una fonte: non fornisce numeri,
    # rifiuta i nostri quando sono assurdi. E' cio' che serve davvero, perche' il
    # modo in cui questa derivazione sbaglia non e' rumoroso — e' «CA 80 per un
    # PNG di GS 8», che ha l'aria di un conto e non di un errore.
    # La guardia **annota**, non sopprime. Sopprimere produceva zero proposte, e
    # uno strumento che non dice niente non aiuta nessuno a correggere niente:
    # una proposta con scritto sopra «fuori bersaglio» si guarda e si giudica.
    collaudo = ""
    if L.gs in PER_GS:
        ca_att, pf_att = PER_GS[L.gs]
        dca, dpf = ca - ca_att, pf - pf_att
        verif = L.gs in PER_GS_VERIFICATE
        if abs(dca) > 6 or abs(dpf) > max(15, pf_att * 0.5):
            collaudo = (f" ⚠ FUORI BERSAGLIO per GS {L.gs}: la tabella attende "
                        f"CA {ca_att} e pf {pf_att} ({dca:+d} / {dpf:+d})"
                        + ("" if verif else ", su una riga che ho interpolato io"))
        conti.append(f"collaudo GS {L.gs} [PF1e Tab. 1–1"
                     + ("" if verif else ", riga interpolata") + f"]: atteso CA "
                     f"{ca_att}, pf {pf_att} → {dca:+d} CA, {dpf:+d} pf{collaudo}")

    sb = Statblocco(
        gs=str(L.gs) if L.gs is not None else "",
        ca=str(ca),
        pf=str(pf),
        ts=f"Temp {temp:+d}, Rifl {rifl:+d}, Vol {vol:+d}",
        # `collaudo` sta gia' dentro `conti`: aggiungerlo qui lo stampava due
        # volte di fila nello stesso campo.
        fonte="derivato-SRD — " + " · ".join(conti),
    )
    return sb, conti, manca


# ===========================================================================
def con_attributi(f: Path, sb: Statblocco, L: Lettura) -> str:
    """Il testo con il blocco scritto: i TS **e le caratteristiche da cui vengono**.

    🔴 **D11, deciso dal DM il 2026-09-23**: *«tienila, ma deve scrivere anche le
    caratteristiche da cui deriva, perché non contraddica genera_attributi»*.
    Il 2 settembre questa opzione ha scritto i TS di otto schede con una matrice
    sua (For, Cos, Des in ordine fisso), e poi `genera_attributi` ha messo
    accanto caratteristiche **diverse**: il razorfiend verde aveva TS da Cos 13
    e `attributi` con Cos 18, mentre la formula del DM diceva Cos 20.

    Adesso le caratteristiche non le sceglie piu' questo script: vengono da
    `dmcore.caratteristiche.genera` (quella di `genera_attributi`), la stessa funzione con gli stessi strati (la
    prosa della scheda, la fonte citata, i vincoli, l'array), e i TS si
    ricalcolano da quelle sulla base di `deriva`. Il blocco porta la marca di
    `genera_attributi`, quindi il suo `--check` lo verifica come uno suo.
    """
    # la scelta e il lettore stanno in `dmcore` (ADR-0066): prima questa
    # funzione importava `genera_attributi` e `conformita_statblocchi`
    from dmcore import caratteristiche as CAR
    from dmcore import lettura_creatura as LC
    # il blocco provvisorio da cui `genera` sceglie **non ha TS**: quelli della
    # matrice non sono un dato, e il tetto dei TS li leggerebbe come tali
    from dataclasses import replace
    testo = inserisci(f.read_text(encoding="utf-8"), replace(sb, ts="", fonte=""))
    ruolo = re.search(r"\*\*Role\*\*:\s*([^|\n]+)", testo, re.I)
    gs = float(str(L.gs or sb.gs).replace(",", "."))
    v, note = CAR.genera(f.name, ruolo.group(1).strip() if ruolo else "", gs, testo)
    extra = LC.talenti(testo)
    ts = {k: L.base_ts[k] + mod(v[c]) + extra.get(n, 0) if isinstance(v[c], int)
          else L.base_ts[k] + extra.get(n, 0)
          for k, c, n in (("temp", "Cos", "Temp"), ("rifl", "Des", "Rifl"), ("vol", "Sag", "Vol"))}
    sb.ts = f"Temp {ts['temp']:+d}, Rifl {ts['rifl']:+d}, Vol {ts['vol']:+d}"
    sb.attributi = CAR.riga_attributi(v).split(": ", 1)[1]
    sb.fonte = (f"derivati dalle tabelle: ts, attributi (il resto è letto dalla prosa) — "
                f"caratteristiche da `genera_attributi` ({note[0]}) · TS: base "
                f"{L.base_ts['temp']:+d}/{L.base_ts['rifl']:+d}/{L.base_ts['vol']:+d} "
                f"+ Cos/Des/Sag → {sb.ts}")
    testo = inserisci(f.read_text(encoding="utf-8"), sb)
    coda = (LC.CODA_SCHEDA if note[0].startswith("letta dalla riga")
            else LC.CODA_FONTE if note[0].startswith("trascritt") else LC.CODA_ARRAY)
    marca = LC.MARCA + coda + "".join(" " + n for n in note if n.startswith("⚠"))
    m = LC.BLOCCO.search(testo)
    fine = testo.index("```", m.end(1)) + 3
    return testo[:fine] + "\n\n" + marca + testo[fine:]


def main(argv: list[str] | None = None) -> int:
    # ⚠️ `allow_abbrev=False`: senza, argparse accetta `--apply` come
    # abbreviazione di `--apply-ts`, e chi lo scrive aspettandosi la scrittura
    # larga (quella che NON esiste) si ritrova una scrittura comunque.
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("file", nargs="*", type=Path)
    # ⚠️ NON esiste un `--apply`, ed e' il risultato del lotto H, non una
    # mancanza. Provato: con le tabelle SRD, le matrici e il collaudo sul GS,
    # **nessuna** delle 60 schede produce numeri che superino il proprio
    # controllo di sanita'. Il modo in cui questa derivazione sbaglia non e'
    # rumoroso — e' «CA 11 per un mostro di GS 9», che ha l'aria di un conto.
    # Quindi propone, e la mano che scrive resta quella del DM.
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--apply-ts", action="store_true",
                    help="scrive i TS e le caratteristiche da cui vengono (quelle di "
                         "genera_attributi), solo dove tutto il resto è letto dalla prosa")
    a = ap.parse_args(argv)

    elenco = [f if f.is_absolute() else ROOT / f for f in a.file] or schede()
    fatti, fermi, saltate, scrivibili = [], {}, 0, []
    for f in elenco:
        t = f.read_text(encoding="utf-8")
        if APERTURA in t or e_non_creatura(t):
            saltate += 1
            continue
        # ⚠️ Il principio: **la prosa vince sempre.** Si legge prima cosa la
        # scheda dice gia', si deriva solo il buco, e un numero scritto non si
        # tocca mai. Derivare sopra un valore del DM vorrebbe dire sostituire
        # un numero vero con uno calcolato — il danno esatto che ADR-0021 teme.
        letto, _ = estrai(t)
        L = leggi_scheda(f)
        sb, conti, manca = deriva(L)
        rel = str(f.relative_to(ROOT))
        if sb is None:
            fermi[rel] = manca
            continue
        derivati = []
        for campo in ("ca", "pf", "ts", "gs"):
            if getattr(letto, campo):
                setattr(sb, campo, getattr(letto, campo))
            elif getattr(sb, campo):
                derivati.append(campo)
        if not derivati:
            continue                      # non c'era niente da derivare
        for campo in ("tipo", "ca_dettaglio", "velocita", "iniziativa"):
            if getattr(letto, campo):
                setattr(sb, campo, getattr(letto, campo))
        # ⚠️ Nella `fonte` va SOLO il conto di ciò che è stato scritto. Metterci
        # anche la derivazione di CA e pf che abbiamo scartato in favore dei
        # numeri del DM produce un blocco che si contraddice — «ca: 24» accanto
        # a «CA: … = 11» — e chi lo legge fra sei mesi non sa a quale credere.
        etichette = {"ts": "TS:", "pf": "pf:", "ca": "CA:"}
        pertinenti = [c for c in conti
                      if c.startswith("caratteristiche:")
                      or any(c.startswith(etichette[d]) for d in derivati)]
        sb.fonte = (f"derivati dalle tabelle: {', '.join(derivati)} "
                    f"(il resto è letto dalla prosa) — " + " · ".join(pertinenti))
        fatti.append((f, sb, conti))
        # La scrittura ristretta: **solo i TS, e solo se tutto il resto era
        # scritto dal DM.** È il caso difendibile, e l'unico.
        #
        # I TS sono la cosa più meccanica del sistema: la base è esatta dalle
        # tabelle SRD (progressione di classe, o tipo di creatura + DV), e
        # l'unica incertezza è il modificatore di caratteristica, che viene
        # dalla matrice dichiarata. Non è un numero indovinato: è un numero
        # calcolato con una convenzione scritta, su una scheda di cui GS, CA e
        # pf li ha scritti il DM — quindi c'è di che accorgersi se stona.
        #
        # CA e pf NON si scrivono mai: la CA dipende dall'equipaggiamento e i pf
        # dalla Costituzione, e nessuno dei due si legge da una scheda in prosa
        # con affidabilità sufficiente. Lì lo strumento resta un proponitore.
        if derivati == ["ts"] and letto.gs and letto.ca and letto.pf:
            scrivibili.append((f, sb, L))

    if a.json:
        print(json.dumps({
            "derivabili": {str(f.relative_to(ROOT)): {"ca": sb.ca, "pf": sb.pf, "ts": sb.ts}
                           for f, sb, _ in fatti},
            "fermi": fermi,
        }, ensure_ascii=False, indent=2))
        return 0

    if a.apply_ts:
        for f, sb, L in scrivibili:
            f.write_text(con_attributi(f, sb, L), encoding="utf-8")
        print(f"  {len(scrivibili)} schede scritte (TS e le caratteristiche da cui "
              f"vengono; GS, CA e pf erano già scritti dal DM)")
    print(f"  {len(fatti)} proposte col conto per esteso "
          f"(senza --apply-ts questo strumento non scrive)")
    if not a.apply_ts and scrivibili:
        print(f"      di cui {len(scrivibili)} scrivibili con --apply-ts: manca "
              f"solo «ts», il resto è letto dalla prosa")
    for f, sb, _ in fatti[:8]:
        print(f"      · {f.name:48} CA {sb.ca}  pf {sb.pf}  {sb.ts}")
    if len(fatti) > 8:
        print(f"      … e altre {len(fatti) - 8}")
    print(f"  {len(fermi)} schede su cui NON si deriva (il numero sarebbe inventato):")
    perche: dict[str, int] = {}
    for m in fermi.values():
        for x in m:
            k = x.split("(")[0].strip()
            perche[k] = perche.get(k, 0) + 1
    for k, n in sorted(perche.items(), key=lambda x: -x[1]):
        print(f"      {n:3}× {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
