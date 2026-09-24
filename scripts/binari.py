"""binari.py — le dipendenze binarie del repo, e la regola di degradazione.

Il repo ha deciso due volte di accettare un eseguibile esterno invece di un
toolchain: `typst` per l'edizione da stampa ([ADR-0020]) e `pdfcpu` per
l'imposizione ([ADR-0027]). Sono decisioni buone — un singolo binario statico,
licenza aperta, nessuna installazione di sistema — a **una** condizione, che è
poi la parte che si dimentica di scrivere:

    se il binario manca, lo script dice come installarlo ed ESCE.
    Non fallisce a meta'.

Fallire a metà è il modo in cui una dipendenza opzionale diventa un problema di
fiducia: un PDF di 40 pagine su 96, un file scritto e poi troncato, un errore che
arriva da `subprocess` in inglese e non dice cosa fare. Chi impagina la sera
prima della sessione non ha modo di sapere se il file che ha in mano e' quello
giusto.

La regola sta qui, in un posto solo, perche' con due copie diventano due regole.

Cosa serve per far girare il repo (lotto D di PIANO-QUALITA-DEL-CODICE)
-----------------------------------------------------------------------
La stessa domanda — *«che cosa devo avere installato?»* — aveva tre risposte che
non coincidevano: `dm.py doctor` accettava Python 3.8, la guida di setup ne
chiedeva 3.11, la CI ne installa 3.11; `doctor` aveva la propria lista di
`pandoc` e `xelatex` che questo file non conosceva; e il manifest dei tool
dichiarava otto binari mentre qui ce n'erano due.

Ora la dichiarazione sta qui e basta: `PYTHON_MINIMO`, `TUTTI` (i binari
accettati con un ADR, quelli che uno script pretende con `esigi()`),
`OPZIONALI` (gli altri, che nessuno pretende e la cui assenza toglie una
funzione senza rompere niente), `LIBRERIE` (le due dipendenze Python, ADR-0037)
e `CATENE`, che dice quale catena di lavoro ha bisogno di cosa. `dm.py doctor`
e la guida di setup leggono da qui.

Codici d'uscita
---------------
`MANCA` (2) e' distinto da 1. Uno script che esce con 2 sta dicendo *«non ho
nemmeno cominciato: manca uno strumento»*, che non e' la stessa cosa di *«ho
provato e non ci sono riuscito»*. La CI puo' distinguerli, e chi legge anche.

Solo stdlib.
"""
from __future__ import annotations

import shutil
import sys
from typing import NamedTuple

MANCA = 2  # exit code: dipendenza assente. Distinto da 1 = fallimento vero.

#: Versione minima di Python. E' quella che la CI installa e quella che la guida
#: di setup chiede: se cambia, cambia qui e i due posti che la leggono seguono.
#: Il 3.11 non e' prudenza, e' un vincolo reale: il codice usa `X | None` nelle
#: annotazioni valutate e `tomllib`, e i test usano `unittest` moderno.
PYTHON_MINIMO = (3, 11)


class Binario(NamedTuple):
    """Un eseguibile esterno accettato con un ADR, e cosa succede senza."""

    nome: str
    a_cosa_serve: str
    licenza: str
    adr: str
    installa: str
    #: Cosa resta possibile senza. Un ripiego dichiarato e' la differenza fra
    #: una dipendenza opzionale e una dipendenza travestita da opzionale.
    ripiego: str


TYPST = Binario(
    nome="typst",
    a_cosa_serve="l'edizione da stampa: un volume unico con segnalibri veri",
    licenza="Apache-2.0",
    adr="ADR-0020",
    installa="""\
  Linux/macOS   curl -sSL https://github.com/typst/typst/releases/latest/download/\\
                  typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
                  sudo install typst-*/typst /usr/local/bin/
  Fedora/Bazzite  brew install typst        (oppure il tarball qui sopra)
  Arch            pacman -S typst
  Windows         winget install --id Typst.Typst""",
    ripiego="`export_booklet_pdf.py` continua a produrre i PDF per capitolo con "
            "Chromium. Questo esportatore serve al volume da stampa.",
)

PDFCPU = Binario(
    nome="pdfcpu",
    a_cosa_serve="l'imposizione: un libretto da piegare, invece di una risma",
    licenza="Apache-2.0",
    adr="ADR-0027",
    installa="""\
  Con Go (qualsiasi sistema)   go install github.com/pdfcpu/pdfcpu/cmd/pdfcpu@v0.11.0
  Linux/macOS   scarica il binario da https://github.com/pdfcpu/pdfcpu/releases
                e mettilo nel PATH — e' un eseguibile statico, niente altro
  Arch          pacman -S pdfcpu
  Windows       winget install pdfcpu""",
    ripiego="il PDF da stampa resta valido e stampabile pagina per pagina: "
            "l'imposizione e' un di piu' per chi rilega, non un passaggio "
            "obbligato della catena.",
)

#: I binari che uno script **pretende** con `esigi()`, ciascuno con il suo ADR.
TUTTI = (TYPST, PDFCPU)


def _opz(nome: str, a_cosa_serve: str, installa: str, ripiego: str) -> Binario:
    """Un binario che nessuno pretende: manca e si perde una funzione, non la catena.

    Non ha un ADR perche' non e' stata una decisione da prendere: `git` c'e'
    ovunque, `chromium` e `pandoc` si installano dal gestore di pacchetti e
    nessuna parte del flusso principale si ferma senza.
    """
    return Binario(nome=nome, a_cosa_serve=a_cosa_serve, licenza="—",
                   adr="—", installa=installa, ripiego=ripiego)


#: Gli altri eseguibili che il repo sa usare. Erano sparsi fra la lista dentro
#: `dm.py doctor`, i campi `external_bins` del manifest e la tabella della guida.
OPZIONALI = (
    _opz("git", "clonare, versionare, il branch di gruppo (ADR-0007)",
         "  Debian/Ubuntu  sudo apt install git\n"
         "  Fedora         sudo dnf install git\n"
         "  macOS          xcode-select --install",
         "senza git il repo non si clona: in pratica c'e' sempre, ed e' l'unico "
         "di questo gruppo che non ha un ripiego vero."),
    _opz("bash", "i cinque script shell: build-skills, sync-skills, "
                 "install-git-hooks, new-campaign-group, Image-to-webp",
         "  Linux/macOS    c'e' gia'\n"
         "  Windows        Git Bash (arriva con Git for Windows) oppure WSL",
         "gli equivalenti in Python esistono per la maggior parte del flusso "
         "(`dm.py skills build`, `dm.py skills sync`); su Windows senza Git Bash "
         "restano fuori i cinque script shell."),
    _opz("chromium", "i PDF dei booklet e i PNG delle mappe",
         "  Debian/Ubuntu  sudo apt install chromium\n"
         "  Fedora         sudo dnf install chromium\n"
         "  Windows        usa Chrome/Edge: set BOOKLET_CHROME=C:\\...\\chrome.exe\n"
         "  cercato in PATH, in $BOOKLET_CHROME e in /opt/pw-browsers",
         "i booklet restano in HTML, che e' il formato che si legge al tavolo; "
         "il PDF e' per chi stampa."),
    _opz("blender", "il render 3D delle mappe (`render_map_blender.py`) e il passo "
                    "di profondita' che alimenta ControlNet",
         "  Debian/Ubuntu  sudo apt install blender\n"
         "  Fedora         sudo dnf install blender\n"
         "  macOS          brew install --cask blender\n"
         "  oppure blender.org/download — poi --blender /percorso/a/blender",
         "la geometria si risolve lo stesso: `--piano-solo` scrive il piano di "
         "scena senza Blender, ed e' quello il pezzo deterministico. Senza il "
         "binario mancano solo il PNG e il passo di profondita', che sono "
         "presentazione e non canone."),
    _opz("inkscape", "i PNG delle mappe con resa SVG fedele (`--renderer inkscape`)",
         "  Debian/Ubuntu  sudo apt install inkscape\n"
         "  Fedora         sudo dnf install inkscape",
         "il PNG esce da Chromium, che rende bene ma non identico: la differenza "
         "si vede sui tratteggi e sui font incorporati."),
    _opz("pandoc", "`dm.py recap --pdf`, il recap in PDF sobrio",
         "  Debian/Ubuntu  sudo apt install pandoc texlive-xetex\n"
         "  Fedora         sudo dnf install pandoc texlive-xetex",
         "il recap resta in markdown e in HTML, che e' come lo si manda ai "
         "giocatori nove volte su dieci."),
    _opz("xelatex", "il motore che pandoc usa per quel PDF",
         "  arriva con texlive-xetex, vedi pandoc",
         "come pandoc: senza, `recap --pdf` non parte e il recap resta testo."),
    _opz("cwebp", "convertire i master delle immagini in WebP",
         "  Debian/Ubuntu  sudo apt install webp\n"
         "  Fedora         sudo dnf install libwebp-tools",
         "le immagini restano PNG: piu' pesanti nel repo, identiche a vedersi."),
    _opz("shellcheck", "il lint degli script shell (in CI non e' bloccante)",
         "  Debian/Ubuntu  sudo apt install shellcheck\n"
         "  Fedora         sudo dnf install ShellCheck",
         "gli script shell del repo sono cinque e corti: senza shellcheck si "
         "leggono a mano."),
)


class Libreria(NamedTuple):
    """Una dipendenza Python. Ce ne sono due, e ADR-0037 dice perche' solo due."""

    nome: str
    modulo: str
    a_cosa_serve: str
    installa: str
    #: `True` se un gate della CI si ferma senza. Il campo esiste perche' la
    #: differenza fra le due e' esattamente questa.
    obbligatoria: bool
    ripiego: str


#: Le uniche due librerie non-stdlib del repo (ADR-0037). `pyyaml` e' un debito
#: dichiarato: sta nel percorso critico della CI, che infatti la installa.
#: `Pillow` no, ed e' il modello di come dovrebbe stare una dipendenza Python.
LIBRERIE = (
    Libreria(
        nome="pyyaml", modulo="yaml",
        a_cosa_serve="il frontmatter delle skill: build, sync, compress, validate",
        installa="  pip install pyyaml",
        obbligatoria=True,
        ripiego="nessuno: `validate_skills.py` e' un gate bloccante e senza "
                "pyyaml esce con 2. E' il debito che ADR-0037 dichiara.",
    ),
    Libreria(
        nome="Pillow", modulo="PIL",
        a_cosa_serve="ricomprimere le immagini grandi e generare i derivati",
        installa="  pip install pillow",
        obbligatoria=False,
        ripiego="`build_booklet_html.py` incorpora l'immagine com'e' (file piu' "
                "pesante, resa identica); `build_image_derivatives.py` esce "
                "dicendo come installarla.",
    ),
)

#: Cosa serve a ciascuna catena di lavoro. La colonna che mancava: sapere che
#: `typst` esiste non dice se serve stasera.
CATENE = {
    "sessione (prep, recap, state)": (),
    "booklet HTML": (),
    "booklet PDF": ("chromium",),
    "edizione da stampa": ("typst",),
    "libretto imposto": ("typst", "pdfcpu"),
    "mappe SVG": (),
    "mappe PNG": ("chromium",),
    "recap in PDF": ("pandoc", "xelatex"),
    "skill per gli agenti": ("pyyaml",),
}


def per_nome(nome: str) -> Binario | Libreria | None:
    """La voce del registro con questo nome, o `None`."""
    for v in (*TUTTI, *OPZIONALI, *LIBRERIE):
        if v.nome == nome:
            return v
    return None


def python_ok() -> bool:
    """Se l'interprete che sta girando basta."""
    return sys.version_info >= PYTHON_MINIMO


def libreria_presente(lib: Libreria) -> bool:
    """Se il modulo si importa. Nessun effetto collaterale oltre l'import."""
    import importlib.util
    return importlib.util.find_spec(lib.modulo) is not None


def disponibile(nome: str) -> bool:
    """Se la voce del registro con questo nome e' installata.

    Una domanda sola per binari e librerie, perche' chi chiede *«la catena
    parte?»* non ha motivo di sapere quale delle due cose sia.
    """
    voce = per_nome(nome)
    if voce is None:
        raise KeyError(f"nessuna dipendenza si chiama {nome!r} nel registro")
    return trova(voce) is not None if isinstance(voce, Binario) else libreria_presente(voce)


def stato_opzionali() -> list[tuple[Binario, str | None]]:
    """Cosa c'e' e cosa manca fra gli opzionali — per `dm.py doctor`."""
    return [(b, trova(b)) for b in OPZIONALI]


def stato_librerie() -> list[tuple[Libreria, bool]]:
    """Cosa c'e' e cosa manca fra le librerie — per `dm.py doctor`."""
    return [(lib, libreria_presente(lib)) for lib in LIBRERIE]


def messaggio(b: Binario) -> str:
    """Il testo che si stampa quando manca. Dice tre cose: cosa, come, e cosa resta."""
    return (
        f"Il binario «{b.nome}» non è nel PATH. Serve a {b.a_cosa_serve}.\n"
        f"È un singolo eseguibile, {b.licenza} ({b.adr}):\n\n"
        f"{b.installa}\n\n"
        f"Niente panico se non lo installi: {b.ripiego}\n"
    )


def trova(b: Binario) -> str | None:
    """Il percorso dell'eseguibile, o `None`. Nessun effetto collaterale."""
    return shutil.which(b.nome)


def esigi(b: Binario) -> str:
    """Il percorso dell'eseguibile, oppure stampa il modo di installarlo ed **esce**.

    È la regola di degradazione pulita, in una riga di chiamata. Si usa **prima**
    di aprire file di destinazione, non dopo: il punto è non lasciare in giro un
    output a metà.
    """
    percorso = trova(b)
    if percorso is None:
        print(messaggio(b), file=sys.stderr)
        raise SystemExit(MANCA)
    return percorso


def stato() -> list[tuple[Binario, str | None]]:
    """Cosa c'è e cosa manca — per `dm.py doctor`."""
    return [(b, trova(b)) for b in TUTTI]


def _riga(simbolo: str, nome: str, coda: str) -> str:
    return f"{simbolo} {nome:12} {coda}"


if __name__ == "__main__":
    import platform

    v = platform.python_version()
    minimo = ".".join(str(n) for n in PYTHON_MINIMO)
    print(_riga("✓" if python_ok() else "✗", "python",
                f"{v}" + ("" if python_ok() else f" — serve >= {minimo}")))

    print("\nBinari accettati con un ADR (uno script li pretende):")
    for b, percorso in stato():
        print(_riga("✓" if percorso else "○", b.nome,
                    percorso or f"assente — {b.ripiego}"))

    print("\nBinari opzionali (senza, si perde una funzione):")
    for b, percorso in stato_opzionali():
        print(_riga("✓" if percorso else "○", b.nome,
                    percorso or f"assente — {b.a_cosa_serve}"))

    print("\nLibrerie Python (ADR-0037):")
    for lib, c_e in stato_librerie():
        etichetta = "obbligatoria" if lib.obbligatoria else "opzionale"
        print(_riga("✓" if c_e else ("✗" if lib.obbligatoria else "○"),
                    lib.nome, f"({etichetta}) " + (lib.a_cosa_serve if c_e
                                                   else f"assente — {lib.ripiego}")))

    print("\nLe catene, e se stasera partono:")
    for catena, servono in CATENE.items():
        mancano = [n for n in servono if not disponibile(n)]
        print(_riga("✓" if not mancano else "○", "",
                    f"{catena:32} " + ("pronta" if not mancano
                                       else "manca " + ", ".join(mancano))))
