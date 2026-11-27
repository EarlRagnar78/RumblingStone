#!/usr/bin/env python3
"""misura_stampa.py — le misure editoriali di un booklet stampato (piano dello standard di stampa).

## Perché esiste

Il DM, il 2026-10-29: *«uniformare tutti i layout di stampa in modo che usino
la stessa logica, le stesse misure e standard professionali […] con test
concreti e reali che verifichino la correttezza, il miglioramento e
l'aderenza agli standard professionali dell'editoria»*. Fino a oggi la CI
verificava che il volume compilasse e che l'apparato di lavoro non finisse in
stampa (ADR-0070). Nessuno guardava il PDF come lo guarda un tipografo.

Questo script apre il PDF che `export_booklet_typst.py` produce e ne misura
quello che un controllo di prestampa misura, più le schede delle creature:

| misura | come si legge | soglia di partenza |
|---|---|---|
| `font_non_incorporati` | i font del PDF senza file incorporato | 0 |
| `testi_sotto_minimo` | righe con testo sotto 7 pt (i numeri soli esclusi), etichette delle mappe comprese | 0 |
| `corpo_mediano_pt` | il corpo più frequente del testo | 9,5-11 pt (C8 di RIFERIMENTI-AP) |
| `fuori_margine` | righe che escono dall'area di stampa | 0 |
| `immagini_sotto_300dpi` | immagini sotto 300 dpi alla dimensione stampata | 0 |
| `immagini_tagliate` | immagini che escono dal foglio oltre la smarginatura di 3 mm, quindi tagliate in stampa | 0 |
| `schede_spezzate` | riquadri di creatura che cominciano su una pagina e finiscono su un'altra | 0 |
| `rimandi_sbagliati` | «scheda a pagina N» senza la creatura a pagina N, «continua a pagina N» senza «(segue)» a pagina N, «continua nella colonna accanto» senza «(segue)» sulla stessa pagina | 0 |
| `pagine_con_immagine` | quota di pagine con un'immagine raster di almeno un quarto di pagina | da registrare |
| `pagine_con_immagine_decimo` | la stessa quota con la soglia di 1/10 di pagina, dove il piano pone l'obiettivo ≥ 0,3 (Paizo 0,40) | da registrare |
| `parole_ripetute`, `quota_parole_ripetute` | parole che stanno in un passo di almeno 8 parole già stampato prima, testatine escluse | in prova; *Burnt Offerings* 0,011, *Red Hand of Doom* (estratto) 0,004 |

Le schede si riconoscono dai segnaposti `<sb-inizio>` e `<sb-fine>` che il
tema mette in ogni `#statblocco`; si leggono con `typst eval`.

## Cosa NON misura, dichiarato

Le mappe e le griglie vettoriali non contano come immagini (sono
disegni, non raster): `pagine_con_immagine` dice quanta illustrazione c'è,
non quante mappe. Vedove e orfane, il rapporto fra titoli e testo, la bellezza. Le prime due
chiedono di ricostruire i paragrafi dal PDF, e lo farà un passo successivo.
La bellezza la giudica il DM, alla cieca, fra versioni che queste misure
dichiarano senza errori.

## Uso

    python3 scripts/misura_stampa.py MANIFEST [MANIFEST…]       # tabella
    python3 scripts/misura_stampa.py --tutti --json            # ogni booklet, in JSON
    python3 scripts/misura_stampa.py MANIFEST --dettaglio      # cosa sfora, pagina per pagina
    python3 scripts/misura_stampa.py --tutti --check           # nessun booklet sopra i suoi tetti (CI)
    python3 scripts/misura_stampa.py --tutti --aggiorna        # riscrive il registro, tetti solo in giù

Il registro è `docs/audit/stampa-booklet.json`: per ogni booklet il tetto di
ogni misura d'errore e l'ultima misura delle altre, così il miglioramento si
legge nella storia di git.

Compila il booklet in `build/misura-stampa/` (non tocca il PDF accanto al
manifest) **senza i font di sistema**, perché la misura sia la stessa su ogni
macchina: un glifo che i font del repo non hanno esce come casella vuota
anche nella misura, invece di prendere un font diverso a seconda del PC.
Serve typst; senza PyMuPDF esce 2.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import typst_motore  # noqa: E402

CARTELLA = ROOT / "build" / "misura-stampa"
REGISTRO = ROOT / "docs" / "audit" / "stampa-booklet.json"
#: Le misure con un tetto: si scende soltanto. Le altre si registrano e basta.
CON_TETTO = ("testi_sotto_minimo", "fuori_margine", "immagini_sotto_300dpi",
             "schede_spezzate", "font_non_incorporati", "rimandi_sbagliati",
             "immagini_tagliate", "difetti_ordine")
REGISTRATE = ("pagine", "corpo_mediano_pt", "corpo_minimo_pt", "schede", "pagine_con_immagine",
              "pagine_con_immagine_decimo", "parole", "quota_parole_ripetute")
#: Le misure in prova (canale testing, ADR-0099): nate dal giro di lettura del
#: 2026-11-10. Si registrano e `--check` avvisa se salgono, senza fermare.
IN_PROVA = ("sigle_morte", "righe_brevi_incomplete", "titoli_rovinati", "parole_ripetute")
#: Un passo ripetuto è lungo almeno tante parole identiche (w-shingling, Broder
#: 1997: lo standard di fatto per trovare testo riusato).
PASSO_RIPETUTO = 8
#: Un n-gramma che torna su più di tante pagine è una testatina, non una ripetizione.
PAGINE_DI_TESTATINA = 8
#: Quante righe in testa e in coda alla pagina si guardano per togliere le
#: testatine: titolo del volume, capitolo, numero di pagina.
RIGHE_DI_BORDO = 3
MINIMO_PT = 7.0
DPI_MINIMI = 300
#: Quanto un'immagine al vivo può uscire dal foglio: la smarginatura di 3 mm
#: che la tipografia rifila. Oltre, la stampa taglia l'immagine.
SMARGINATURA_PT = 3 * 72 / 25.4 + 1
# Typst appende punteggiatura e trattini nel margine (text.overhang, la
# «sporgenza ottica» dei tipografi): fino a 4 pt fuori è composizione voluta.
TOLLERANZA_PT = 4.0


def compila_misurabile(mp: Path) -> tuple[Path, list[dict], str]:
    """Il .typ e il PDF del booklet, in una cartella di lavoro."""
    man = json.loads(mp.read_text(encoding="utf-8"))
    CARTELLA.mkdir(parents=True, exist_ok=True)
    nome = mp.name.replace(".manifest.json", "")
    typ = mp.parent / f".{nome}.misura.typ"   # accanto al manifest: i percorsi relativi restano validi
    pdf = CARTELLA / f"{nome}.pdf"
    formato = man.get("formato", "a4")
    typ.write_text(ex.sorgente(man, mp.parent, True, formato=formato), encoding="utf-8")
    try:
        esito = compila_senza_font_di_sistema(typ, pdf)
        if esito.returncode != 0:
            raise RuntimeError(f"{mp.name}: typst non compila\n{esito.stderr[-2000:]}")
        # Un'impaginazione che non converge stampa rimandi sbagliati: «scheda a
        # pagina N», «continua a pagina N» presi da un giro precedente. Si
        # guarda l'avviso del numero di pagina, che è quello stampato: fino al
        # 2026-11-19 il controllo leggeva lo stderr, che col typst di PyPI è
        # vuoto, e il volume d'arco di ARC-07 passava con 15 rimandi su 242
        # sbagliati di una pagina.
        instabili = esito.stderr.split("\n") if esito.stderr else []
        if instabili:
            raise RuntimeError(f"{mp.name}: l'impaginazione non converge, i rimandi di pagina "
                               f"possono essere sbagliati\n" + "\n".join(instabili[:6]))
        schede = interroga_schede(typ)
    finally:
        typ.unlink(missing_ok=True)
    # Un volume fatto solo di schede o di carte da tavolo ha la gabbia del
    # foglio sciolto (scheda-pg.typ, carte-tavolo.typ: 1 cm per lato), non
    # quella del libro.
    if man.get("chapters") and all(c.get("layout") in ("schede", "carte") for c in man["chapters"]):
        formato = "scheda"
    return pdf, schede, formato


#: Solo i font del repo (scripts/fonts e quelli dentro typst): i font di
#: sistema cambiano da una macchina all'altra, e con loro i ripieghi per i
#: glifi che i nostri font non hanno. La misura deve dare lo stesso numero sul
#: portatile del DM e in CI.
SOLO_FONT_DEL_REPO = ["--ignore-system-fonts", "--font-path", str(ex.FONTS)]


def compila_senza_font_di_sistema(typ: Path, pdf: Path) -> subprocess.CompletedProcess:
    """Il PDF senza font di sistema. Se compila, lo stderr porta solo gli
    avvisi dei numeri di pagina instabili (`typst_motore.numeri_instabili`)."""
    e = typst_motore.compila(typ, pdf, root=ROOT, font=ex.FONTS, pacchetti=ex.PACCHETTI,
                             solo_font_del_repo=True)
    stderr = e.errore if not e.ok else "\n".join(typst_motore.numeri_instabili(e))
    return subprocess.CompletedProcess(["typst", "compile", str(typ)], 0 if e.ok else 1, "", stderr)


def interroga_schede(typ: Path) -> list[dict]:
    """Inizio e fine di ogni riquadro, dai segnaposti del tema."""
    espressione = ("query(selector(<sb-inizio>).or(<sb-fine>))"
                   ".map(m => (str(m.label), m.value, m.location().page()))")
    return accoppia_segnaposti(typst_motore.valuta(
        typ, espressione, root=ROOT, font=ex.FONTS, pacchetti=ex.PACCHETTI, solo_font_del_repo=True))


def accoppia_segnaposti(segnaposti: list) -> list[dict]:
    """[etichetta, nome, pagina] in ordine di documento → un riquadro per coppia.

    I riquadri non si annidano: dopo un inizio viene la sua fine.
    """
    schede, aperta = [], None
    for etichetta, nome, pagina in segnaposti:
        if etichetta == "sb-inizio":
            aperta = (nome, pagina)
        elif aperta is not None:
            schede.append({"nome": aperta[0], "da": aperta[1], "a": pagina})
            aperta = None
    return schede


# I margini del tema (`libro` in tema-rumblingstone.typ), speculari: la pagina 1
# è una destra, quindi sulle dispari l'interno è a sinistra.
MARGINI_CM = {"a4": {"interno": 2.0, "esterno": 1.5}, "a5": {"interno": 1.5, "esterno": 1.1},
              # la scheda da tavolo: un foglio sciolto, margini uguali sui due lati
              "scheda": {"interno": 1.0, "esterno": 1.0}}
# Testatine e folio stanno nel margine alto e basso: si controlla solo che non
# arrivino al bordo, dove la taglierina o la stampante li mangiano.
BORDO_CM = 0.8


ILLUSTRAZIONE_MINIMA_PT = 2 * 72 / 2.54   # sotto i 2 cm è un'icona, non un'illustrazione


def _stesso_posto(a, b) -> bool:
    return all(abs(x - y) <= 3 for x, y in zip(a, b))


def area_di_stampa(area, pagina: int, formato: str):
    import pymupdf
    pt = 72 / 2.54
    m = MARGINI_CM.get(formato, MARGINI_CM["a4"])
    sinistro, destro = (m["interno"], m["esterno"]) if pagina % 2 else (m["esterno"], m["interno"])
    return pymupdf.Rect(area.x0 + sinistro * pt - TOLLERANZA_PT, area.y0 + BORDO_CM * pt,
                        area.x1 - destro * pt + TOLLERANZA_PT, area.y1 - BORDO_CM * pt)


def misura_pdf(pdf: Path, schede: list[dict], formato: str = "a4") -> dict:
    import pymupdf
    doc = pymupdf.open(pdf)
    corpi: Counter = Counter()
    sotto, fuori, immagini_basse, pagine_illustrate, pagine_illustrate_decimo = [], [], [], 0, 0
    tagliate = []
    minimo = 99.0
    font_mancanti: set[str] = set()
    for n, pagina in enumerate(doc, 1):
        for f in pagina.get_fonts(full=True):
            # estensione «n/a» = nessun file incorporato; i Type3 (le emoji a
            # colori) sono disegnati dentro il PDF, quindi ci sono.
            if f[1] == "n/a" and f[2] != "Type3":
                font_mancanti.add(f[3])
        area = pagina.rect
        dentro = area_di_stampa(area, n, formato)
        for blocco in pagina.get_text("rawdict")["blocks"]:
            for riga in blocco.get("lines", []):
                piccola = None
                for span in riga["spans"]:
                    glifi = [c for c in span["chars"] if c["c"].strip()]
                    if not glifi:
                        continue
                    testo = "".join(c["c"] for c in span["chars"]).strip()
                    corpi[round(span["size"] * 2) / 2] += len(testo)
                    if not testo.isdigit():
                        minimo = min(minimo, span["size"])
                        if span["size"] < MINIMO_PT and piccola is None:
                            piccola = (n, round(span["size"], 1), testo[:40])
                    # Il riquadro dei glifi, non dello span: lo span di una riga
                    # giustificata porta con sé lo spazio finale.
                    inchiostro = pymupdf.Rect(min(c["bbox"][0] for c in glifi), min(c["bbox"][1] for c in glifi),
                                              max(c["bbox"][2] for c in glifi), max(c["bbox"][3] for c in glifi))
                    if not dentro.contains(inchiostro):
                        fuori.append((n, testo[:40]))
                # Si conta la riga, non lo span: un glifo che cade su un font
                # di sistema spezza lo span, e i font di sistema cambiano da
                # una macchina all'altra (in CI la misura per span dava +1/+3).
                if piccola:
                    sotto.append(piccola)
        grande = media = False
        immagini = [(pymupdf.Rect(im["bbox"]), im) for im in pagina.get_image_info(xrefs=True)]
        for r, im in immagini:
            if min(r.width, r.height) < ILLUSTRAZIONE_MINIMA_PT:
                continue        # icone ed emoji delle mappe: non sono illustrazioni
            # Il foglio allargato della smarginatura: un'immagine che ne esce
            # perde in stampa la parte di fuori (il ritratto di Vatore, ARC-07).
            foglio = area + (-SMARGINATURA_PT, -SMARGINATURA_PT, SMARGINATURA_PT, SMARGINATURA_PT)
            if not foglio.contains(r):
                tagliate.append((n, round(max(area.y0 - r.y0, r.y1 - area.y1, area.x0 - r.x0, r.x1 - area.x1))))
            dpi = min(im["width"] / (r.width / 72), im["height"] / (r.height / 72))
            # Typst rasterizza i filtri degli SVG (ombre, sfocature della
            # pergamena) in uno strato a bassa risoluzione sopra l'immagine
            # vera: se allo stesso posto c'è già un'immagine a risoluzione
            # piena, lo strato è un effetto, non un'illustrazione sgranata.
            if dpi < DPI_MINIMI and not any(
                    altra is not im and _stesso_posto(r, ra)
                    and min(altra["width"] / (ra.width / 72), altra["height"] / (ra.height / 72)) >= DPI_MINIMI
                    for ra, altra in immagini):
                immagini_basse.append((n, round(dpi), round(r.width / 72 * 2.54, 1)))
            if r.width * r.height >= area.width * area.height / 4:
                grande = True
            if r.width * r.height >= area.width * area.height / 10:
                media = True
        pagine_illustrate += grande
        pagine_illustrate_decimo += media
    spezzate = [s for s in schede if s["a"] != s["da"]]
    rimandi = rimandi_sbagliati(doc)
    sigle, brevi, titoli = sigle_morte(doc), righe_brevi_incomplete(doc), titoli_rovinati(doc)
    parole, ripetute, passi = parole_ripetute(doc)
    return {
        "pagine": len(doc),
        "font_non_incorporati": sorted(font_mancanti),
        "corpo_mediano_pt": statistics.median(corpi.elements()) if corpi else None,
        "corpo_minimo_pt": round(minimo, 1) if corpi else None,
        "testi_sotto_minimo": len(sotto),
        "fuori_margine": len(fuori),
        "immagini_sotto_300dpi": len(immagini_basse),
        "immagini_tagliate": len(tagliate),
        "schede": len(schede),
        "schede_spezzate": len(spezzate),
        "rimandi_sbagliati": len(rimandi),
        "sigle_morte": len(sigle),
        "righe_brevi_incomplete": len(brevi),
        "titoli_rovinati": len(titoli),
        "parole": parole,
        "parole_ripetute": ripetute,
        "quota_parole_ripetute": round(ripetute / parole, 3) if parole else 0,
        "pagine_con_immagine": round(pagine_illustrate / len(doc), 3) if len(doc) else 0,
        "pagine_con_immagine_decimo": round(pagine_illustrate_decimo / len(doc), 3) if len(doc) else 0,
        "dettaglio": {
            "sotto_minimo": sotto[:30], "fuori_margine": fuori[:30],
            "immagini_basse": immagini_basse[:30], "immagini_tagliate": tagliate[:30],
            "schede_spezzate": spezzate, "rimandi_sbagliati": rimandi[:30],
            "sigle_morte": sigle[:30], "righe_brevi_incomplete": brevi[:30],
            "titoli_rovinati": titoli[:30],
            "passi_ripetuti": passi[:30],
        },
    }


def _piano(testo: str) -> str:
    """Il testo senza trattini morbidi e con gli spazi ridotti: un nome che va a
    capo nel titolo si ritrova lo stesso."""
    return re.sub(r"\s+", " ", testo.replace("\xad", "").replace("\u00ad", "")).strip()


def rimandi_sbagliati(doc) -> list[tuple]:
    """I rimandi di pagina dell'appendice delle creature, controllati sul PDF.

    Un rimando si sbaglia quando l'impaginazione sposta qualcosa dopo che il
    numero è stato scritto. L'appendice ne stampa di tre tipi, e ognuno dice
    dove si deve trovare cosa."""
    testi = [_piano(p.get_text()) for p in doc]
    sbagliati = []
    for n, pagina in enumerate(doc, 1):
        for blocco in pagina.get_text("dict")["blocks"]:
            righe = [[s["text"] for s in r["spans"] if s["text"].strip()] for r in blocco.get("lines", [])]
            for parti in righe:
                testo = _piano(" ".join(parti))
                if m := re.search(r"scheda a pagina (\d+)", testo):
                    # Il nome apre la riga dell'incontro: è il primo pezzo del blocco.
                    nome, dove = _piano(righe[0][0]), int(m.group(1))
                    # senza trattini né spazi: «mezzo-immondo» spezzato a fine riga
                    # nel titolo della scheda torna dal PDF come «mezzo- immondo»
                    stretto = lambda t: re.sub(r"[-\s]", "", t)  # noqa: E731
                    if not (1 <= dove <= len(testi)) or stretto(nome) not in stretto(testi[dove - 1]):
                        sbagliati.append((n, nome[:40], f"scheda a pagina {dove}"))
                elif m := re.search(r"continua a pagina (\d+)", testo):
                    dove = int(m.group(1))
                    if not (1 <= dove <= len(testi)) or "(segue)" not in testi[dove - 1]:
                        sbagliati.append((n, "", f"continua a pagina {dove}"))
                elif "continua nella colonna accanto" in testo and "(segue)" not in testi[n - 1]:
                    sbagliati.append((n, "", "continua nella colonna accanto"))
    return sbagliati


_PAROLA = re.compile(r"[a-zà-ùA-ZÀ-Ù0-9+]+")


def parole_ripetute(doc, passo: int = PASSO_RIPETUTO) -> tuple[int, int, list[tuple]]:
    """Quante parole del volume stanno in un passo già stampato prima.

    Un passo è una sequenza di almeno `passo` parole identiche; si conta dalla
    seconda volta in poi. Le testatine e i piè di pagina non contano: né le
    righe in testa e in coda che tornano uguali su un'altra pagina, né i passi
    presenti su più di `PAGINE_DI_TESTATINA` pagine. Misurato il 2026-11-13
    sui riferimenti di ADR-0122: *Burnt Offerings* 1,1%, l'estratto di *Red
    Hand of Doom* 0,4%; il booklet di serata «La Notte e l'Alba» 11,9%.

    Torna (parole del volume, parole ripetute, passi): ogni passo è
    (pagina, pagina della prima volta, parole, come comincia), dal più lungo.
    """
    # Le righe in testa e in coda che tornano uguali su un'altra pagina sono
    # testatine e piè di pagina: fuori prima di contare, anche nei capitoli
    # corti, dove il conto delle pagine non le riconosce.
    pagine = [pagina.get_text().replace("\xad", "").split("\n") for pagina in doc]
    bordo: dict[str, int] = {}
    for righe in pagine:
        for r in {x.strip() for x in righe[:RIGHE_DI_BORDO] + righe[-RIGHE_DI_BORDO:]}:
            if _PAROLA.search(r):
                bordo[r] = bordo.get(r, 0) + 1
    parole: list[tuple[str, int]] = []
    for n, righe in enumerate(pagine, start=1):
        a, z = 0, len(righe)
        while a < min(RIGHE_DI_BORDO, z) and bordo.get(righe[a].strip(), 0) > 1:
            a += 1
        while z > max(a, len(righe) - RIGHE_DI_BORDO) and (
                bordo.get(righe[z - 1].strip(), 0) > 1 or not righe[z - 1].strip()):
            z -= 1
        testo = re.sub(r"-\n(?=[a-zà-ù])", "", "\n".join(righe[a:z]))
        parole += [(w.lower(), n) for w in _PAROLA.findall(testo)]
    ws = [w for w, _ in parole]
    dove: dict[tuple, list[int]] = {}
    for i in range(len(ws) - passo + 1):
        dove.setdefault(tuple(ws[i:i + passo]), []).append(i)
    ripetuta, testatina = [False] * len(ws), [False] * len(ws)
    for ii in dove.values():
        if len({parole[i][1] for i in ii}) > PAGINE_DI_TESTATINA:
            for i in ii:
                testatina[i:i + passo] = [True] * passo
        for i in ii[1:]:
            ripetuta[i:i + passo] = [True] * passo
    conta = [a and not b for a, b in zip(ripetuta, testatina)]
    passi, i = [], 0
    while i < len(ws):
        if not conta[i]:
            i += 1
            continue
        j = i
        while j < len(ws) and conta[j]:
            j += 1
        prima = dove.get(tuple(ws[i:i + passo]), [i])[0]
        passi.append((parole[i][1], parole[prima][1], j - i, " ".join(ws[i:i + 10])))
        i = j
    passi.sort(key=lambda p: -p[2])
    return len(ws), sum(conta), passi


_SIGLA = re.compile(r"\b[Aa]ppendice\s+([A-Z])(\.\d+(?:-(?:bis|ter))?)?(?![\w-])")


def sigle_morte(doc) -> list[tuple]:
    """I rimandi «Appendice A.3» che nel volume stampato non portano a niente.

    Una sigla è viva se da qualche parte una riga comincia con lei («A.3 …»)
    o con «Appendice A» come titolo. Giro del 2026-11-10: il booklet per
    sezioni stampava sigle dei master che l'appendice del booklet non ha."""
    righe = [(n, _piano(r)) for n, p in enumerate(doc, 1) for r in p.get_text().splitlines() if r.strip()]
    inizi = {r for _, r in righe}
    def viva(lettera: str, numero: str | None) -> bool:
        if numero:
            return any(r.startswith(f"{lettera}{numero} ") or r == f"{lettera}{numero}"
                       or r.startswith(f"{lettera}{numero} ·") for r in inizi)
        return any(re.match(rf"(?i:appendice)\s+{lettera}\b\s*(?:[·:—–-]|$)", r) for r in inizi)
    morte = []
    for n, pagina in enumerate(doc, 1):
        for m in _SIGLA.finditer(_piano(pagina.get_text())):
            if not viva(m.group(1), m.group(2)):
                morte.append((n, m.group(0)))
    return morte


def righe_brevi_incomplete(doc) -> list[tuple]:
    """Le righe d'incontro («scheda a pagina N») senza quello che serve per
    giocare il round: iniziativa, tiri salvezza e almeno un attacco. Giro del
    2026-11-10: con CA e pf soltanto il DM sfoglia a ogni attacco."""
    manca = []
    for n, pagina in enumerate(doc, 1):
        for blocco in pagina.get_text("blocks"):
            testo = _piano(blocco[4])
            if "scheda a pagina" not in testo:
                continue
            cosa = [nome for nome, segno in (("iniziativa", r"\bIniz"), ("TS", r"\bTS\b|\bTemp"),
                                             ("attacco", r"\bMischia\b|\bDistanza\b|\+\d+ \("))
                    if not re.search(segno, testo)]
            if cosa:
                manca.append((n, testo[:40], "manca " + ", ".join(cosa)))
    return manca


_ELISIONE = re.compile(r"\b(DELL|DALL|NELL|SULL|ALL|QUELL|UN|L|D)([AEIOUÀÈÉÌÒÙ][A-ZÀ-Ý]{2,})\b")


def titoli_rovinati(doc) -> list[tuple]:
    """I titoli in maiuscolo che hanno perso l'apostrofo («LALBA» per
    «L'ALBA»): la parola intera non esiste altrove nel volume, la seconda
    metà sì."""
    tutto = " ".join(_piano(p.get_text()) for p in doc)
    parole = Counter(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]+", tutto) if not w.isupper())
    rovinati = []
    for n, pagina in enumerate(doc, 1):
        for m in _ELISIONE.finditer(_piano(pagina.get_text())):
            intera, resto = m.group(0).lower(), m.group(2).lower()
            if parole[resto] and not parole[intera]:
                rovinati.append((n, m.group(0)))
    return rovinati


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", nargs="*", type=Path)
    ap.add_argument("--tutti", action="store_true", help="ogni booklet con manifest")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dettaglio", action="store_true")
    ap.add_argument("--check", action="store_true", help="nessun booklet sopra i suoi tetti")
    ap.add_argument("--aggiorna", action="store_true", help="riscrive il registro, tetti solo verso il basso")
    a = ap.parse_args(argv)
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        print("✗ serve PyMuPDF (pip install -r requirements-dev.txt)", file=sys.stderr)
        return 2
    if a.tutti:
        import misura_statblocchi_booklet as msb
        a.manifest = [m for m in msb.manifesti()
                      if "chapters" in json.loads(m.read_text(encoding="utf-8"))]
    risultati = {}
    for mp in a.manifest:
        mp = mp.resolve()
        pdf, schede, formato = compila_misurabile(mp)
        v = misura_pdf(pdf, schede, formato)
        v["difetti_ordine"], v["dettaglio"]["ordine"] = difetti_ordine(mp, pdf)
        risultati[mp.relative_to(ROOT).as_posix()] = v
    if a.json:
        print(json.dumps(risultati, ensure_ascii=False, indent=2))
        return 0
    registro = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.is_file() else {}
    if a.aggiorna:
        scrivi_registro(registro, risultati)
        print(f"✓ registro riscritto in {REGISTRO.relative_to(ROOT)}")
        return 0
    print(f"{'booklet':<44} {'pag':>4} {'corpo':>5} {'<7pt':>5} {'marg':>5} {'dpi':>4} "
          f"{'font':>4} {'min':>4} {'schede':>6} {'spezz':>5} {'immag':>7} {'ripet':>6}")
    for nome, v in risultati.items():
        print(f"{nome[-44:]:<44} {v['pagine']:>4} {v['corpo_mediano_pt'] or 0:>5} "
              f"{v['testi_sotto_minimo']:>5} {v['fuori_margine']:>5} {v['immagini_sotto_300dpi']:>4} "
              f"{len(v['font_non_incorporati']):>4} {v['corpo_minimo_pt'] or 0:>4} {v['schede']:>6} {v['schede_spezzate']:>5} "
              f"{v['pagine_con_immagine']:>7.0%} {v['quota_parole_ripetute']:>6.1%}")
        if a.dettaglio:
            for chiave, voci in v["dettaglio"].items():
                for voce in voci[:10]:
                    print(f"    {chiave:<16} {voce}")
    if a.check:
        sopra = sopra_il_tetto(registro.get("booklet", {}), risultati)
        for riga in sopra:
            print(f"✗ {riga}", file=sys.stderr)
        for nome, v in risultati.items():
            prima = registro.get("booklet", {}).get(nome, {}).get("in_prova", {})
            for m in IN_PROVA:
                if m in prima and v[m] > prima[m]:
                    print(f"⚠ {nome}: {m} = {v[m]}, era {prima[m]} (in prova, non ferma)", file=sys.stderr)
        if sopra:
            return 1
        print(f"✓ {len(risultati)} booklet, nessuno sopra i suoi tetti di stampa")
    return 0


def difetti_ordine(mp: Path, pdf: Path) -> tuple[int, list]:
    """ADR-0145: i difetti d'ordine del booklet (`misura_ordine.py`), se il
    suo manifest dichiara i ruoli dei capitoli; 0 se non li dichiara, perché
    senza ruoli l'ordine non si misura. Il dettaglio sono le regole violate."""
    import misura_ordine as mo
    man = json.loads(mp.read_text(encoding="utf-8"))
    if not mo.ha_ruoli(man):
        return 0, []
    m, _, n = mo.misura_completa(pdf, mo.regole_per(pdf, mp))
    return n, mo.violazioni(m)


def valore(v: dict, misura: str) -> int:
    x = v[misura]
    return len(x) if isinstance(x, list) else x


def scrivi_registro(registro: dict, risultati: dict) -> None:
    vecchi = registro.get("booklet", {})
    nuovi = dict(vecchi)
    for nome, v in risultati.items():
        prima = vecchi.get(nome, {}).get("tetti", {})
        nuovi[nome] = {
            "tetti": {m: min(valore(v, m), prima.get(m, valore(v, m))) for m in CON_TETTO},
            "misura": {m: v[m] for m in REGISTRATE},
            "in_prova": {m: v[m] for m in IN_PROVA},
        }
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    REGISTRO.write_text(json.dumps({
        "_cos_e": "Le misure di stampa di ogni booklet (scripts/misura_stampa.py). «tetti»: "
                  "errori ammessi oggi, scendono soltanto (--aggiorna non alza); la CI li "
                  "controlla con --check. «misura»: l'ultima lettura delle misure senza tetto.",
        "soglie": {"corpo_minimo_pt": MINIMO_PT, "dpi_minimi": DPI_MINIMI,
                   "sporgenza_ottica_pt": TOLLERANZA_PT, "margini_cm": MARGINI_CM},
        "booklet": dict(sorted(nuovi.items())),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sopra_il_tetto(registrati: dict, risultati: dict) -> list[str]:
    fuori = []
    for nome, v in risultati.items():
        if nome not in registrati:
            fuori.append(f"{nome}: booklet nuovo senza tetti; misuralo e registralo con --aggiorna")
            continue
        tetti = registrati[nome]["tetti"]
        for m in CON_TETTO:
            if valore(v, m) > tetti.get(m, 0):
                fuori.append(f"{nome}: {m} = {valore(v, m)}, il tetto è {tetti.get(m, 0)}")
    return fuori


if __name__ == "__main__":
    sys.exit(main())
