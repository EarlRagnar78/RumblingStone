#!/usr/bin/env python3
r"""misura_distanza_pagine.py — quante pagine sfoglia il DM per trovare i numeri di chi ha davanti?

## Perché esiste

La prova di ADR-0107 (2026-11-03) ha misurato la distanza fra la scena e lo
statblocco **a mano**: un DM e un playtester hanno letto i due PDF e contato
le pagine («numeri di Zog'tar a +31, mappa a +37»). È la misura che conta al
tavolo, ma una lettura a mano non si ripete a ogni commit.

Questo strumento la rifà sul **PDF stampato**, con PyMuPDF (AGPL, già nella
dotazione di sviluppo per `validate_booklets --stampa`). È una tecnica di
*document AI* nella sua forma più semplice e deterministica: si legge il testo
di ogni pagina, non si indovina niente.

Per ogni persona che ha un riquadro nel repo (`dmcore.chi_si_incontra`):

* **pagine d'azione**: le pagine che la nominano almeno 3 volte;
* **pagine dei numeri**: le pagine che la nominano e hanno sia «CA N» sia «pf N»;
* per ogni pagina d'azione, la distanza dalla pagina dei numeri più vicina.

Il numero che riassume è la **mediana** delle distanze. Il 2026-11-03, sui due
PDF della prova (157 e 172 pagine): Zog'tar 23,5 → 5, Skullcrusher 21 → 4,
Balvar 28,5 → 5,5, Durin 53 → 4,5. Durik peggiora (102,5 → 112): i suoi numeri
stanno solo in appendice, e le pagine in più li allontanano. La misura lo dice.

## Cosa NON misura, dichiarato

* una pagina che nomina la persona senza parlarne (un elenco) conta come
  pagina d'azione se la nomina 3 volte;
* uno statblocco spezzato su due pagine, con CA e pf su pagine diverse, non
  conta come pagina dei numeri;
* le mappe: le piante non hanno testo affidabile da cui riconoscerle.

È un **indicatore**, come `misura_standard_tavolo`: esce 0, o 2 senza PyMuPDF.

## Lo standard del volume (ADR-0122, `--volume`)

Con `--volume` lo stesso lettore di PDF misura la **struttura del volume**
come la misurano gli Adventure Path di carta (schema Paizo, schede in
appendice come *Red Hand of Doom*; decisione del DM del 2026-11-09):

| misura | che cosa conta, sul PDF |
|---|---|
| **S1** introduzione | per ogni capitolo dell'indice del PDF, i caratteri fra il titolo e il primo sottotitolo; e se prima del primo capitolo c'è un antefatto o una sintesi |
| **S2** chiavi | i codici d'area dei titoli nel testo («B6.», «A1 ·») contro quelli stampati sulle mappe, orfani nei due sensi |
| **S3** distanza | le pagine fra la descrizione di un'area e la sua mappa; per i nostri booklet anche fra la pagina che cita una mappa per nome («M7-C», «GS-1») e la mappa |
| **S4** appendice | le pagine in fondo su regione e PNG, sul totale |
| **S5** PNG | i PNG principali con i numeri e un ritratto a una pagina dai numeri |

I riferimenti (*Burnt Offerings* e l'estratto di *RHoD*) hanno le mappe raster
con le etichette calligrafiche: l'OCR non le legge (tesseract 5.3: 4 codici su
23 nella mappa più leggibile). Le chiavi delle mappe e le pagine delle
appendici stanno quindi in un file d'annotazione trascritto a vista una volta
(`--riferimento FILE.json`); il conto, da lì, è lo stesso codice dei nostri.
Le soglie che ne escono stanno in `docs/audit/volume-booklet.json`.

È nel canale **testing** di ADR-0099: `--check` esce 1 sotto soglia, ma in CI
il passo non blocca.

## Uso

    python3 scripts/misura_distanza_pagine.py VOLUME.pdf [ALTRO.pdf ...]
    python3 scripts/misura_distanza_pagine.py --json A.pdf B.pdf
    python3 scripts/misura_distanza_pagine.py --nomi "Zog'tar,Skullcrusher" A.pdf
    python3 scripts/misura_distanza_pagine.py --volume A.pdf [--riferimento ANNOT.json]
    python3 scripts/misura_distanza_pagine.py --volume --tutti [--check] [--json]
    python3 scripts/misura_distanza_pagine.py --volume --manifest MANIFEST.json
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from misura_standard_tavolo import chiave, conta_nome, piega  # noqa: E402

AZIONE = 3
CA = re.compile(r"\bca\s+\d+")
PF = re.compile(r"\bpf\s+\d+")


def pagine(pdf: Path) -> list[str]:
    try:
        import pymupdf  # noqa: PLC0415
    except ImportError:
        print("misura_distanza_pagine: serve PyMuPDF (pip install -r requirements-dev.txt)", file=sys.stderr)
        raise SystemExit(2) from None
    with pymupdf.open(pdf) as doc:
        # l'apostrofo tipografico del PDF («Zog’tar») si piega in «-»: va tolto prima
        return [piega(re.sub(r"[’ʼ‘]", "", p.get_text())) for p in doc]


def distanze(pp: list[str], k: str) -> "dict | None":
    """Le distanze di una persona, o `None` se non ha pagine d'azione o di numeri."""
    numeri = [i for i, t in enumerate(pp) if conta_nome(t, k) and CA.search(t) and PF.search(t)]
    azione = [i for i, t in enumerate(pp) if conta_nome(t, k) >= AZIONE]
    if not numeri or not azione:
        return None
    d = [min(abs(i - j) for j in numeri) for i in azione]
    return {"pagine_azione": len(azione), "pagine_numeri": len(numeri),
            "mediana": statistics.median(d), "massima": max(d),
            "entro_una": sum(x <= 1 for x in d)}


def chiavi_del_repo() -> list[str]:
    from dmcore import chi_si_incontra  # noqa: PLC0415
    idx = chi_si_incontra.indice_del_repo()
    return sorted({chiave(p.nome) or k for k, p in idx.riquadri.items()} - {""})


def misura(pdf: Path, chiavi: list[str]) -> dict:
    pp = pagine(pdf)
    out = {}
    for k in chiavi:
        d = distanze(pp, k)
        if d:
            out[k] = d
    return {"pagine": len(pp), "persone": out}


# ---------------------------------------------------------------------------
# Lo standard del volume (ADR-0122): S1-S5 sul PDF.
# ---------------------------------------------------------------------------

SOGLIE = ROOT / "docs" / "audit" / "volume-booklet.json"

#: Un codice d'area in testa a un titolo: «B6. Ancient Prison», «A1 · La cripta», «D5: Nualia».
CODICE_TITOLO = re.compile(r"^([A-Z]{1,2}\d{1,2}[a-dA-D]?)\s*(?:\.|:|·|—)\s+\S")
#: Una mappa nostra: la riga della scala che il motore stampa sotto il titolo.
SCALA_MAPPA = re.compile(r"quadretto di [\d,]+ m")
#: Il titolo di una mappa nostra: «M7-C — La tenda…», «GS-1 — La cripta…».
ID_MAPPA = re.compile(r"^([A-Z]{1,3}\d*(?:-[A-Z0-9]+)+)\s+—\s")
#: La pagina della legenda che segue ogni pianta (ADR-0106).
LEGENDA = "Luoghi, zone e percorsi"
#: Antefatto e sintesi in testa al volume, nelle due lingue dei riferimenti.
INTRO_VOLUME = re.compile(r"background|synopsis|summary|outline|dove siamo|antefatto|sintesi|in breve|riassunto"
                          r"|la verit[aà]|premessa|panoramica",
                          re.I)
#: Le voci dell'indice che non sono capitoli d'avventura.
NON_CAPITOLO = re.compile(r"^(appendice|indice|dove siamo|colophon|crediti)", re.I)
#: L'appendice di supporto: regione e PNG (S4).
APP_REGIONE = re.compile(r"region|valle|citt[aà]|luoghi|atlante|gazzett|dintorni|zone|terre", re.I)
APP_PNG = re.compile(r"\bpng\b|personaggi|chi [eè] chi|galleria|creature|schede|bestiari", re.I)
#: Testata e piede: le righe nel 6% alto e basso della pagina non sono testo.
MARGINE = 0.06


def _righe(pagina) -> list[tuple[float, str]]:
    h = pagina.rect.height
    out = []
    for b in pagina.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            y = ln["bbox"][1]
            if t and MARGINE * h < y < (1 - MARGINE) * h:
                out.append((y, t))
    return sorted(out)


def _y_del_titolo(pagina, titolo: str, dopo: float = 0.0) -> float:
    """Dove sta il titolo sulla pagina: il primo punto in cui compare dopo `dopo`.
    `dopo` è la destinazione del segnalibro, quando il PDF la dà: lo stesso
    titolo può stare due volte nella pagina (nella serata di ARC-07 «§5 — ATTO
    III · L'ALBA» è sia nel titolo corrente sia nel corpo)."""
    for chiave_ in (titolo[:40], titolo.split(":")[0][:30], titolo.split()[0] if titolo.split() else ""):
        for c in (chiave_, chiave_.upper()):
            if c and (r := [x for x in pagina.search_for(c) if x.y0 >= dopo - 2]):
                return r[0].y0
    return dopo


#: Sopra una tabella mobile il tema stampa una didascalia: il titolo della sezione.
DIDASCALIA = 28.0
#: Un titolo di capitolo, o un capolettera: non è testo dell'introduzione.
CORPO_TITOLO = 14.0


def _righe_in_ordine(pagina) -> list[tuple[float, float, float, str]]:
    """Le righe nell'ordine del flusso del PDF, (y, x, corpo, testo): un PDF
    taggato le scrive nell'ordine di lettura, colonna dopo colonna."""
    h = pagina.rect.height
    out = []
    for b in pagina.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            y = ln["bbox"][1]
            if t and MARGINE * h < y < (1 - MARGINE) * h:
                out.append((y, ln["bbox"][0], max(s["size"] for s in ln["spans"]), t))
    return out


def _fasce_tabelle(pagina, righe) -> list[tuple[float, float]]:
    """Le fasce verticali delle tabelle, con la loro didascalia. Il tema porta
    le tabelle larghe in testa alla pagina, e non sono l'introduzione. Quelle
    che `find_tables` non vede si riconoscono dalle righe con almeno tre celle,
    a cavallo del centro pagina: il testo a due colonne ne ha due."""
    try:
        fasce = [(t.bbox[1] - DIDASCALIA, t.bbox[3]) for t in pagina.find_tables().tables]
    except Exception:  # noqa: BLE001 — una pagina che non si analizza non ha tabelle per la misura
        fasce = []
    centro = pagina.rect.width / 2
    celle: dict[int, list[float]] = {}
    for y, x, _c, _t in righe:
        celle.setdefault(round(y), []).append(x)
    file = sorted(y for y, xs in celle.items()
                  if len({round(x) for x in xs}) >= 3 and min(xs) < centro < max(xs))
    gruppo: list[int] = []
    for y in [*file, None]:
        if gruppo and (y is None or y - gruppo[-1] > 60):
            fasce.append((gruppo[0] - DIDASCALIA, gruppo[-1] + 14))
            gruppo = []
        if y is not None:
            gruppo.append(y)
    return fasce


def _caratteri_intro(doc, a: tuple[int, float], b: tuple[int, float]) -> int:
    """I caratteri dell'introduzione: il testo che nel flusso di lettura viene
    dopo il titolo del capitolo in `a` e prima del primo sottotitolo in `b`
    (pagine da 0), senza titoli, capolettera, tabelle mobili e didascalie."""
    n = 0
    for i in range(a[0], min(b[0], len(doc) - 1) + 1):
        righe = _righe_in_ordine(doc[i])
        fasce = _fasce_tabelle(doc[i], righe)
        for y, _x, corpo, t in righe:
            if i == b[0] and abs(y - b[1]) <= 4:
                return n
            if (i == a[0] and y <= a[1] + 2) or corpo >= CORPO_TITOLO \
                    or any(y0 <= y <= y1 for y0, y1 in fasce):
                continue
            n += len(t)
    return n


def _y_destinazione(voce) -> float:
    """La y (dall'alto) a cui punta un segnalibro di `get_toc(False)`; 0 se non la dà."""
    to = voce[3].get("to") if len(voce) > 3 and isinstance(voce[3], dict) else None
    return float(to.y) if to is not None else 0.0


def capitoli(doc, livello: int = 1, filtro: "str | None" = None) -> list[dict]:
    """I capitoli dall'indice del PDF, con il primo sottotitolo di ciascuno."""
    # la destinazione del segnalibro dice dove comincia il titolo sulla pagina
    toc = [(e[0], e[1].strip(), e[2] - 1, _y_destinazione(e)) for e in doc.get_toc(False) if e[2] >= 1]
    out = []
    for k, (lv, t, p, y) in enumerate(toc):
        if (lv != livello or NON_CAPITOLO.search(t) or INTRO_VOLUME.search(t)
                or (filtro and not re.search(filtro, t, re.I))):
            continue
        figlio = next((v for v in toc[k + 1:] if v[0] <= livello or v[0] == livello + 1), None)
        primo = figlio if figlio and figlio[0] == livello + 1 else None
        out.append({"titolo": t, "pagina": p, "y": y, "primo": primo[1] if primo else None,
                    "pagina_primo": primo[2] if primo else None, "y_primo": primo[3] if primo else 0.0})
    return out


def s1_introduzione(doc, livello: int = 1, filtro: "str | None" = None) -> dict:
    caps = capitoli(doc, livello, filtro)
    for c in caps:
        if c["primo"] is None:
            c["intro"] = None
            continue
        a = (c["pagina"], _y_del_titolo(doc[c["pagina"]], c["titolo"], c["y"]))
        b = (c["pagina_primo"], _y_del_titolo(doc[c["pagina_primo"]], c["primo"], c["y_primo"]))
        c["intro"] = _caratteri_intro(doc, a, b)
    primo_cap = min((c["pagina"] for c in caps), default=len(doc))
    voci = [t for _lv, t, p in doc.get_toc() if p - 1 <= primo_cap]
    return {"capitoli": caps, "intro_volume": any(INTRO_VOLUME.search(t) for t in voci)}


def _pagine_mappa(doc) -> tuple[dict[int, set[str]], set[int]]:
    """Le nostre mappe: {pagina: {id}} e le pagine di legenda."""
    mappe, legende = {}, set()
    for i, p in enumerate(doc):
        t = p.get_text()
        if t.lstrip().split("\n", 3)[-1].startswith(LEGENDA) or f"\n{LEGENDA}\n" in t[:300]:
            legende.add(i)
        if SCALA_MAPPA.search(t):
            ids = {m.group(1) for r in t.splitlines() if (m := ID_MAPPA.match(r.strip()))}
            mappe[i] = ids
    return mappe, legende


#: Le chiavi solo numeriche («1. Sandpoint Cathedral»): solo dove l'annotazione le chiede,
#: perché da noi «1. Che cosa hanno fatto» è un paragrafo numerato, non un'area.
CODICE_NUMERICO = re.compile(r"^(\d{1,2})\.\s+[A-Z]")


def codici_nel_testo(doc, escluse: set[int], annot: "dict | None" = None) -> dict[str, int]:
    """{codice: pagina} dei titoli d'area fuori dalle pagine di mappa e legenda."""
    out: dict[str, int] = {}
    rx = CODICE_NUMERICO if annot and annot.get("codici_numerici") else CODICE_TITOLO
    solo = {p - 1 for a, b in annot.get("pagine_testo", []) for p in range(a, b + 1)} if annot else set()
    for i, p in enumerate(doc):
        if i in escluse or (solo and i not in solo):
            continue
        for r in p.get_text().splitlines():
            if m := rx.match(r.strip()):
                out.setdefault(m.group(1).upper(), i)
    return out


def _distanze(da: list[int], a: list[int]) -> list[int]:
    return [min(abs(i - j) for j in a) for i in da] if a else []


def _riassunto(d: list[int]) -> dict:
    if not d:
        return {"n": 0, "entro_una": None, "mediana": None}
    return {"n": len(d), "entro_una": round(sum(x <= 1 for x in d) / len(d), 3),
            "mediana": statistics.median(d), "massima": max(d)}


def s2_s3(doc, annot: "dict | None") -> dict:
    mappe, legende = _pagine_mappa(doc)
    if annot and "mappe" in annot:
        sulla_mappa = {c.upper(): m["pagina"] - 1 for m in annot["mappe"] for c in m["codici"]}
        pag_mappe = {m["pagina"] - 1 for m in annot["mappe"]}
    else:
        pag_mappe = set(mappe)
        sulla_mappa = {}
        for i in pag_mappe:   # le etichette d'area stampate sulla pianta, se ci sono
            for r in doc[i].get_text().splitlines():
                if re.fullmatch(r"[A-Z]{1,2}\d{1,2}[a-dA-D]?", r.strip()):
                    sulla_mappa.setdefault(r.strip().upper(), i)
    if annot and "mappe" in annot:
        # Le piante di carta lasciano una parte della pagina al testo: si leggono anche quelle.
        testo = codici_nel_testo(doc, set(), annot)
    else:
        # Da noi un codice in testa a una riga è spesso un indizio («A1 · La ricevuta») o un
        # momento («M1 · Il sarcofago»): contano solo i codici dei titoli dell'indice del PDF.
        testo = {}
        for _lv, t, pg in doc.get_toc():
            if (m := CODICE_TITOLO.match(t.strip())) and pg - 1 not in pag_mappe | legende:
                testo.setdefault(m.group(1).upper(), pg - 1)
    solo_testo = sorted(set(testo) - set(sulla_mappa))
    solo_mappa = sorted(set(sulla_mappa) - set(testo))
    comuni = sorted(set(testo) & set(sulla_mappa))
    s2 = {"nel_testo": len(testo), "sulla_mappa": len(sulla_mappa), "comuni": len(comuni),
          "solo_testo": solo_testo, "solo_mappa": solo_mappa,
          "quota_testo_con_mappa": round(len(comuni) / len(testo), 3) if testo else None}
    s3 = _riassunto([abs(testo[c] - sulla_mappa[c]) for c in comuni])
    # Le nostre mappe si citano per nome (M7-C, GS-1): distanza fra chi cita e la mappa.
    per_id: list[int] = []
    for mid in sorted({x for ids in mappe.values() for x in ids}):
        dove = [i for i, ids in mappe.items() if mid in ids]
        rx = re.compile(rf"(?<![\w-]){re.escape(mid)}(?![\w-])")
        citano = [i for i, p in enumerate(doc) if i not in mappe and i not in legende and rx.search(p.get_text())]
        per_id += _distanze(citano, dove)
    s3["per_nome_mappa"] = _riassunto(per_id)
    s3["mappe"] = len(pag_mappe)
    return {"S2": s2, "S3": s3}


def s4_appendice(doc, annot: "dict | None", ultimo_capitolo: int) -> dict:
    n = len(doc)
    if annot and "appendice" in annot:
        ap = annot["appendice"]
        reg = sum(b - a + 1 for a, b in ap.get("regione", []))
        png = sum(b - a + 1 for a, b in ap.get("png", []))
        return {"regione": reg > 0, "png": png > 0, "pagine_regione": reg, "pagine_png": png,
                "quota": round((reg + png) / n, 3), "fonte": "annotazione"}
    voci = [(t, p - 1) for lv, t, p in doc.get_toc() if lv == 1 and p - 1 > ultimo_capitolo]
    voci.append(("", n))
    reg = png = 0
    for (t, p), (_t2, p2) in zip(voci, voci[1:]):
        if APP_REGIONE.search(t):
            reg += p2 - p
        elif APP_PNG.search(t):
            png += p2 - p
    return {"regione": reg > 0, "png": png > 0, "pagine_regione": reg, "pagine_png": png,
            "quota": round((reg + png) / n, 3), "fonte": "indice del PDF"}


def _ha_ritratto(pagina, k: str) -> bool:
    area = pagina.rect.width * pagina.rect.height
    for info in pagina.get_image_info():
        r = pymupdf_rect(info["bbox"]) & pagina.rect
        if not r.is_empty and 0.02 <= r.width * r.height / area <= 0.6:
            return conta_nome(piega(re.sub(r"[’ʼ‘]", "", pagina.get_text())), k) > 0
    return False


def pymupdf_rect(bbox):
    import pymupdf  # noqa: PLC0415
    return pymupdf.Rect(bbox)


def s5_png(doc, annot: "dict | None", chiavi: list[str]) -> dict:
    if annot and "png" in annot:
        a = annot["png"]
        return {"principali": a["principali"], "con_ritratto": a["con_ritratto"],
                "quota": round(a["con_ritratto"] / a["principali"], 3), "fonte": a.get("fonte", "annotazione")}
    pp = [piega(re.sub(r"[’ʼ‘]", "", p.get_text())) for p in doc]
    princ, con = [], []
    for k in chiavi:
        numeri = [i for i, t in enumerate(pp) if conta_nome(t, k) and CA.search(t) and PF.search(t)]
        azione = [i for i, t in enumerate(pp) if conta_nome(t, k) >= AZIONE]
        if not numeri or len(azione) < AZIONE:
            continue
        princ.append(k)
        vicine = {j for i in numeri for j in (i - 1, i, i + 1) if 0 <= j < len(doc)}
        if any(_ha_ritratto(doc[j], k) for j in vicine):
            con.append(k)
    return {"principali": len(princ), "con_ritratto": len(con),
            "quota": round(len(con) / len(princ), 3) if princ else None,
            "senza": sorted(set(princ) - set(con)), "fonte": "PDF"}


def misura_volume(pdf: Path, annot: "dict | None" = None, chiavi: "list[str] | None" = None) -> dict:
    import pymupdf  # noqa: PLC0415
    with pymupdf.open(pdf) as doc:
        cap = annot.get("capitoli", {}) if annot else {}
        s1 = s1_introduzione(doc, cap.get("livello", 1), cap.get("filtro"))
        ultimo = max((c["pagina"] for c in s1["capitoli"]), default=0)
        intro = [c["intro"] for c in s1["capitoli"] if c["intro"] is not None]
        out = {"pagine": len(doc),
               "S1": {"capitoli": len(s1["capitoli"]), "intro_volume": s1["intro_volume"],
                      "intro_caratteri": [c["intro"] for c in s1["capitoli"]],
                      "intro_mediana": statistics.median(intro) if intro else None,
                      "dettaglio": [{"titolo": c["titolo"], "intro": c["intro"], "primo": c["primo"]}
                                    for c in s1["capitoli"]]},
               **s2_s3(doc, annot),
               "S4": s4_appendice(doc, annot, ultimo),
               "S5": s5_png(doc, annot, chiavi or [])}
    soglia_intro = carica_soglie().get("S1_intro_min_caratteri", 0)
    out["S1"]["con_intro"] = sum(1 for x in out["S1"]["intro_caratteri"] if x and x >= soglia_intro)
    return out


def carica_soglie() -> dict:
    return json.loads(SOGLIE.read_text(encoding="utf-8"))["soglie"] if SOGLIE.is_file() else {}


def sotto_soglia(m: dict, s: dict) -> list[str]:
    """Le misure S1-S5 di un booklet sotto le soglie dei riferimenti."""
    f = []
    if m["S1"]["capitoli"] and m["S1"]["con_intro"] / m["S1"]["capitoli"] < s["S1_quota_capitoli_con_intro"]:
        f.append(f"S1 capitoli con introduzione {m['S1']['con_intro']}/{m['S1']['capitoli']}")
    if s.get("S1_intro_volume") and not m["S1"]["intro_volume"]:
        f.append("S1 manca antefatto o sintesi in testa al volume")
    q = m["S2"]["quota_testo_con_mappa"]
    if q is not None and q < s["S2_quota_testo_con_mappa"]:
        f.append(f"S2 codici del testo sulla mappa {q:.0%} (solo testo: {', '.join(m['S2']['solo_testo'][:8])})")
    if len(m["S2"]["solo_mappa"]) > s["S2_solo_mappa_max"]:
        f.append(f"S2 codici solo sulla mappa: {', '.join(m['S2']['solo_mappa'][:8])}")
    for chiave_s3, d in (("codici", m["S3"]), ("nome", m["S3"]["per_nome_mappa"])):
        if d["entro_una"] is not None and d["entro_una"] < s["S3_quota_entro_una"]:
            f.append(f"S3 ({chiave_s3}) descrizioni a una pagina dalla mappa {d['entro_una']:.0%}")
    if s.get("S4_appendice_regione") and not m["S4"]["regione"]:
        f.append("S4 manca l'appendice sulla regione")
    if s.get("S4_appendice_png") and not m["S4"]["png"]:
        f.append("S4 manca l'appendice dei PNG")
    if m["S5"]["quota"] is not None and m["S5"]["quota"] < s["S5_quota_con_ritratto"]:
        f.append(f"S5 PNG principali con ritratto {m['S5']['con_ritratto']}/{m['S5']['principali']}")
    return f


def booklet_del_dm() -> list[Path]:
    import misura_statblocchi_booklet as msb  # noqa: PLC0415
    out = []
    for m in msb.manifesti():
        man = json.loads(m.read_text(encoding="utf-8"))
        if any(c.get("tag") == "dm" for c in man.get("chapters", [])):
            out.append(m)
    return out


def pdf_del_booklet(mp: Path) -> Path:
    """Il PDF compilato da misura_stampa (stessa cartella, stessi font); se manca lo compila."""
    import misura_stampa  # noqa: PLC0415
    pdf = misura_stampa.CARTELLA / (mp.name.replace(".manifest.json", "") + ".pdf")
    if not pdf.is_file():
        pdf = misura_stampa.compila_misurabile(mp)[0]
    return pdf


def stampa_volume(dati: dict) -> None:
    print(f"{'volume':<42}{'pag':>5}{'S1 intro':>10}{'S1 vol':>7}{'S2 cod':>9}{'S3 ≤1p':>8}"
          f"{'S3 nome':>8}{'S4 reg/png':>11}{'S5 ritr':>9}")
    for nome, m in dati.items():
        s1 = f"{m['S1']['con_intro']}/{m['S1']['capitoli']}"
        s2 = f"{m['S2']['comuni']}/{m['S2']['nel_testo']}"
        e = m["S3"]["entro_una"]
        en = m["S3"]["per_nome_mappa"]["entro_una"]
        s4 = f"{m['S4']['pagine_regione']}/{m['S4']['pagine_png']}"
        s5 = f"{m['S5']['con_ritratto']}/{m['S5']['principali']}"
        print(f"{Path(nome).name[-42:]:<42}{m['pagine']:>5}{s1:>10}{'sì' if m['S1']['intro_volume'] else 'no':>7}"
              f"{s2:>9}{'—' if e is None else f'{e:.0%}':>8}{'—' if en is None else f'{en:.0%}':>8}"
              f"{s4:>11}{s5:>9}")


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pdf", nargs="*", type=Path)
    ap.add_argument("--nomi", help="nomi separati da virgola (default: chi ha un riquadro nel repo)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--volume", action="store_true", help="lo standard del volume, S1-S5 (ADR-0122)")
    ap.add_argument("--riferimento", type=Path, help="annotazione di un PDF di riferimento (mappe raster, appendici)")
    ap.add_argument("--tutti", action="store_true", help="con --volume: ogni booklet del DM")
    ap.add_argument("--manifest", type=Path, action="append",
                    help="con --volume: il booklet di questo manifest (compilato come misura_stampa)")
    ap.add_argument("--check", action="store_true", help="con --volume: esce 1 se un booklet è sotto soglia")
    a = ap.parse_args(argv)
    if a.volume:
        return main_volume(a)
    if not a.pdf:
        ap.error("serve almeno un PDF")
    chiavi = [chiave(n) for n in a.nomi.split(",")] if a.nomi else chiavi_del_repo()
    dati = {str(p): misura(p, chiavi) for p in a.pdf}
    if a.json:
        print(json.dumps(dati, ensure_ascii=False, indent=1))
        return 0
    tutte = sorted({k for v in dati.values() for k in v["persone"]})
    print(f"{'persona':<16}" + "".join(f"{Path(p).name[:22]:>24}" for p in dati))
    for k in tutte:
        celle = []
        for v in dati.values():
            d = v["persone"].get(k)
            celle.append(f"{d['mediana']:>6} (max {d['massima']:>3})" if d else "—")
        print(f"{k:<16}" + "".join(f"{c:>24}" for c in celle))
    print("mediana delle pagine fra dove la persona agisce e dove stanno CA e pf "
          "(indicatore, non cancello)")
    return 0


def main_volume(a) -> int:
    try:
        import pymupdf  # noqa: F401, PLC0415
    except ImportError:
        print("misura_distanza_pagine: serve PyMuPDF (pip install -r requirements-dev.txt)", file=sys.stderr)
        return 2
    annot = json.loads(a.riferimento.read_text(encoding="utf-8")) if a.riferimento else None
    chiavi = [chiave(n) for n in a.nomi.split(",")] if a.nomi else ([] if annot else chiavi_del_repo())
    if a.tutti or a.manifest:
        manifesti = booklet_del_dm() if a.tutti else [m.resolve() for m in a.manifest]
        sorgenti = {m.relative_to(ROOT).as_posix(): pdf_del_booklet(m) for m in manifesti}
    else:
        sorgenti = {str(p): p for p in a.pdf}
    dati = {nome: misura_volume(pdf, annot, chiavi) for nome, pdf in sorgenti.items()}
    if a.json:
        print(json.dumps(dati, ensure_ascii=False, indent=1))
    else:
        stampa_volume(dati)
    if not a.check:
        return 0
    s = carica_soglie()
    rossi = 0
    for nome, m in dati.items():
        for riga in sotto_soglia(m, s):
            print(f"✗ {nome}: {riga}")
            rossi += 1
    print(f"{'✗' if rossi else '✓'} standard del volume (ADR-0122, testing): {rossi} misure sotto le soglie dei riferimenti")
    return 1 if rossi else 0


if __name__ == "__main__":
    sys.exit(main())
