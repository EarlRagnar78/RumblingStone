"""typst_motore.py — un solo modo di compilare e interrogare un `.typ` (ADR-0116).

Lo standard è il pacchetto PyPI `typst` (typst-py, Apache-2.0), fissato in
`requirements.txt`. È il compilatore ufficiale dentro un modulo Python: non
passa da GitHub Releases, lo aggiorna Dependabot e va nel bundle insieme alle
altre wheel. Misura: `plans/esperimenti/typst-pip-2026-11-08/MISURE.md`, cioè
19 booklet e 856 pagine con testo e pixel identici alla CLI.

Una CLI `typst` nel PATH resta il **ripiego**: si usa se il modulo manca,
oppure se `RUMBLINGSTONE_TYPST=cli` lo chiede. `RUMBLINGSTONE_TYPST=pypi`
vieta il ripiego. La CLI non e' piu' fissata da nessuna parte (mise e
`strumenti.py` sono usciti con ADR-0116): se la sua versione non e' quella di
`requirements.txt`, i PDF non sono quelli della CI.

Ogni chiamante passa di qui: `export_booklet_typst`, `misura_stampa`,
`varianti_stampa`, `validate_booklets`, `validate_corredo`. Se lo facesse
ognuno per conto suo, le regole diventerebbero due e una invecchierebbe in
silenzio, come dice `binari.py`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import binari

try:  # opzionale, con ripiego dichiarato (ADR-0037)
    import typst as _typst
except ImportError:  # pragma: no cover - dipende dall'ambiente
    _typst = None
# Con scripts/ nel sys.path, senza il pacchetto PyPI `import typst` trova la
# cartella scripts/typst/ (tema e pacchetti vendorizzati) come namespace
# package: non è il compilatore, quindi si ripiega.
if _typst is not None and not hasattr(_typst, "compile"):
    _typst = None

VARIABILE = "RUMBLINGSTONE_TYPST"


class Esito(NamedTuple):
    ok: bool
    errore: str
    #: True se ha dovuto ricompilare senza tag PDF (bug di typst 0.15.1
    #: «internal error: parent group» su float annidati: i tag sono
    #: accessibilità, non impaginazione, e il chiamante lo dice).
    senza_tag: bool
    #: True se il PDF è PDF/UA-1 (ISO 14289-1), chiesto con `pdfua=True`.
    #: Typst verifica da sé gli obblighi che dipendono dal documento (titoli
    #: senza salti, testo alternativo, lingua, titolo) e rifiuta di compilare
    #: se ne manca uno: allora si ricompila senza, e il chiamante lo dice.
    pdfua: bool = False
    #: perché il PDF/UA-1 non c'è (il messaggio di typst), vuoto se c'è
    motivo_pdfua: str = ""
    #: il livello PDF/A del PDF («a-2a»), chiesto con `pdfa=`; vuoto se non c'è
    pdfa: str = ""
    #: perché il PDF/A non c'è (il messaggio di typst), vuoto se c'è
    motivo_pdfa: str = ""
    #: gli avvisi di typst, uno per riga (messaggio e suggerimenti). Prima
    #: del 2026-11-19 il ramo PyPI li buttava via, e il controllo di
    #: misura_stampa su «did not converge» non vedeva niente.
    avvisi: tuple[str, ...] = ()


#: L'avviso che dice che un numero di pagina STAMPATO è cambiato fra l'ultimo
#: giro di impaginazione e il precedente: il rimando «p. N» può essere
#: sbagliato. Gli altri avvisi di convergenza (una misura, una posizione)
#: dicono che Typst ha esitato, non che sulla pagina c'è un numero sbagliato.
NUMERO_INSTABILE = "value of the page counter did not converge"


def numeri_instabili(e: Esito) -> list[str]:
    """Gli avvisi di `e` per cui un numero di pagina stampato può essere sbagliato."""
    return [a for a in e.avvisi if a.startswith(NUMERO_INSTABILE)]


def motore() -> str | None:
    """«pypi», «cli», oppure None se non c'è né l'uno né l'altro."""
    scelta = os.environ.get(VARIABILE, "").strip().lower()
    if scelta == "cli":
        return "cli" if binari.trova(binari.TYPST) else None
    if _typst is not None:
        return "pypi"
    if scelta == "pypi":
        return None
    return "cli" if binari.trova(binari.TYPST) else None


def disponibile() -> bool:
    return motore() is not None


MESSAGGIO = """\
✗ typst non c'è: serve per l'edizione da stampa (ADR-0020, ADR-0116).

  Standard       pip install -r requirements.txt     (il pacchetto «typst» di PyPI)
  Ripiego        una CLI typst nel PATH (github.com/typst/typst/releases)

Niente panico se non lo installi: `export_booklet_pdf.py` continua a produrre i
PDF per capitolo con Chromium. Questo esportatore serve al volume da stampa.
"""


def esigi() -> str:
    """Il motore, oppure stampa come installarlo ed esce con `binari.MANCA`."""
    m = motore()
    if m is None:
        print(MESSAGGIO, file=sys.stderr)
        raise SystemExit(binari.MANCA)
    return m


def _opzioni_cli(root: Path, font: Path, pacchetti: Path, solo_font_del_repo: bool,
                 ingressi: dict[str, str] | None) -> list[str]:
    opz = ["--font-path", str(font), "--root", str(root), "--package-path", str(pacchetti)]
    if solo_font_del_repo:
        opz.insert(0, "--ignore-system-fonts")
    for k, v in (ingressi or {}).items():
        opz += ["--input", f"{k}={v}"]
    return opz


def _opzioni_py(root: Path, font: Path, pacchetti: Path, solo_font_del_repo: bool,
                ingressi: dict[str, str] | None) -> dict:
    return dict(root=str(root), font_paths=[str(font)], package_path=str(pacchetti),
                ignore_system_fonts=solo_font_del_repo, sys_inputs=dict(ingressi or {}))


def _data() -> int | None:
    """La data di creazione del PDF: quella di SOURCE_DATE_EPOCH, come fa la CLI."""
    v = os.environ.get("SOURCE_DATE_EPOCH", "").strip()
    return int(v) if v.isdigit() else None


def _e_bug_dei_tag(testo: str) -> bool:
    return "internal error" in testo and "tag" in testo


def _e_rifiuto_pdfua(testo: str) -> bool:
    return "PDF/UA-1 error" in testo


def _e_rifiuto_pdfa(testo: str) -> bool:
    return "PDF/A" in testo and "error" in testo


def _prima_riga(testo: str) -> str:
    return testo.strip().splitlines()[0] if testo.strip() else "rifiutato"


def compila(typ: Path, pdf: Path, *, root: Path, font: Path, pacchetti: Path,
            solo_font_del_repo: bool = False, ingressi: dict[str, str] | None = None,
            pdfua: bool = False, pdfa: str = "") -> Esito:
    """`typst compile`, col ripiego senza tag PDF quando typst inciampa lì.

    `pdfua=True` chiede PDF/UA-1 (ISO 14289-1, lo standard dell'accessibilità
    dei PDF): se typst lo rifiuta si ricompila come prima e l'esito dice
    perché (`motivo_pdfua`). ADR-0032 aveva lasciato fuori veraPDF perché due
    rilievi su tre erano di typst; da typst 0.14 non lo sono più.

    `pdfa="a-2a"` chiede in più PDF/A (ISO 19005, l'archiviazione, ADR-0131),
    insieme a PDF/UA-1. Se typst rifiuta il PDF/A si ricompila col solo
    PDF/UA-1 e l'esito dice perché (`motivo_pdfa`).
    """
    kw = dict(root=root, font=font, pacchetti=pacchetti,
              solo_font_del_repo=solo_font_del_repo, ingressi=ingressi)
    motivo_pdfa = ""
    if pdfua and pdfa:
        e = _compila(typ, pdf, standard=["ua-1", pdfa], **kw)
        if e.ok:
            return e._replace(pdfua=True, pdfa=pdfa)
        if not (_e_rifiuto_pdfa(e.errore) or _e_rifiuto_pdfua(e.errore)):
            return e
        motivo_pdfa = _prima_riga(e.errore)
    if pdfua:
        e = _compila(typ, pdf, standard=["ua-1"], **kw)
        if e.ok:
            return e._replace(pdfua=True, motivo_pdfa=motivo_pdfa)
        if not _e_rifiuto_pdfua(e.errore):
            return e
        return _compila(typ, pdf, **kw)._replace(motivo_pdfua=_prima_riga(e.errore),
                                                 motivo_pdfa=motivo_pdfa)
    return _compila(typ, pdf, **kw)


def _compila(typ: Path, pdf: Path, *, root: Path, font: Path, pacchetti: Path,
             solo_font_del_repo: bool, ingressi: dict[str, str] | None,
             standard: list[str] | None = None) -> Esito:
    m = esigi()
    if m == "pypi":
        opz = _opzioni_py(root, font, pacchetti, solo_font_del_repo, ingressi)
        ts = _data()
        if ts is not None:
            opz["timestamp"] = ts
        if standard:
            opz["pdf_standards"] = standard
        for tag in (True, False) if not standard else (True,):
            try:
                _, avvisi = _typst.compile_with_warnings(str(typ), output=str(pdf), pdf_tags=tag, **opz)
                return Esito(True, "", not tag, avvisi=tuple(
                    " · ".join([a.message, *(a.hints or [])]).replace("\n", " ") for a in avvisi))
            except _typst.TypstError as e:
                if not (tag and _e_bug_dei_tag(str(e))):
                    return Esito(False, str(e), not tag)
    cmd = [binari.esigi(binari.TYPST), "compile",
           *_opzioni_cli(root, font, pacchetti, solo_font_del_repo, ingressi)]
    for st in standard or ():
        cmd += ["--pdf-standard", st]
    r = subprocess.run(cmd + [str(typ), str(pdf)], capture_output=True, text=True)
    if r.returncode != 0 and _e_bug_dei_tag(r.stderr) and not standard:
        r = subprocess.run(cmd + ["--no-pdf-tags", str(typ), str(pdf)], capture_output=True, text=True)
        return Esito(r.returncode == 0, r.stderr, True, avvisi=_avvisi_cli(r.stderr))
    return Esito(r.returncode == 0, r.stderr, False, avvisi=_avvisi_cli(r.stderr))


def _avvisi_cli(stderr: str) -> tuple[str, ...]:
    """Le righe «warning: …» della CLI, come quelle del ramo PyPI."""
    return tuple(r.split("warning:", 1)[1].strip() for r in stderr.splitlines()
                 if r.lstrip().startswith("warning:"))


def valuta(typ: Path, espressione: str, *, root: Path, font: Path, pacchetti: Path,
           solo_font_del_repo: bool = False, ingressi: dict[str, str] | None = None):
    """`typst eval --in typ espressione`, decodificato da JSON. Alza RuntimeError."""
    if esigi() == "pypi":
        try:
            uscita = _typst.eval(str(typ), espressione,
                                 **_opzioni_py(root, font, pacchetti, solo_font_del_repo, ingressi))
        except _typst.TypstError as e:
            raise RuntimeError(f"typst eval: {str(e)[-1000:]}") from e
        if isinstance(uscita, bytes):
            uscita = uscita.decode("utf-8")
        return json.loads(uscita or "[]")
    cmd = [binari.esigi(binari.TYPST), "eval", "--in", str(typ),
           *_opzioni_cli(root, font, pacchetti, solo_font_del_repo, ingressi), espressione]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"typst eval: {r.stderr[-1000:]}")
    return json.loads(r.stdout or "[]")


def versione() -> str:
    """Per `dm.py doctor` e per i rapporti: chi compila, e quale versione."""
    m = motore()
    if m == "pypi":
        from importlib import metadata  # noqa: PLC0415
        return f"pypi typst {metadata.version('typst')}"
    if m == "cli":
        r = subprocess.run([binari.trova(binari.TYPST), "--version"], capture_output=True, text=True)
        return f"cli {r.stdout.strip()}"
    return "assente"


if __name__ == "__main__":
    print(f"typst: {versione()}")
    sys.exit(0 if disponibile() else binari.MANCA)
