#!/usr/bin/env python3
"""importa_gemini.py — chat di Gemini esportate → Markdown leggibile, con un indice per lo smistamento.

Due fonti, tutte e due esportate a mano dal DM (nessuna chiamata a Google, nessuna chiave):

  aistudio  i file delle chat di Google AI Studio (la cartella «Google AI Studio» di Drive, scaricata
            o zippata): JSON con `chunkedPrompt.chunks`; i pensieri del modello (`isThought`) si saltano.
  takeout   l'archivio di Google Takeout con «La mia attività → App Gemini» (zip o cartella), in
            JSON (MyActivity.json) o in HTML (MyActivity.html, il formato di serie).

Scrive un .md per chat (AI Studio) o per giorno (Takeout) e `INDICE.md` con data, turni, caratteri
e quante volte compaiono i nomi della campagna, così si sceglie cosa portare nel repo prima di
leggere tutto. Le chat restano fuori dal repo (inventario del 2026-10-23, PR #284): la cartella di
uscita va scelta fuori, e lo script rifiuta una cartella dentro il repo.

  python3 scripts/importa_gemini.py aistudio CARTELLA_O_ZIP --out ~/gemini-md
  python3 scripts/importa_gemini.py takeout takeout-AAAA.zip --out ~/gemini-md [--parole Thorik,Zalkatar]

Il formato di Takeout per «App Gemini» non è documentato da Google: il lettore JSON e quello HTML
sono scritti sui campi noti di «La mia attività» (`title`, `time`, `safeHtmlItem`) e provati su
campioni sintetici. Se su un'esportazione vera esce 0 voci, lo dice ed esce 3.
Uscita: 0 ok · 2 errore d'uso · 3 nessuna chat riconosciuta.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAROLE = ("Hammerfist", "Thorik", "Tordek", "Hella", "Artemis", "Zalkatar", "Azarr Kul", "Red Hand",
          "Mano Rossa", "Belkram", "Drappo", "Palio", "Sethrax", "Brenna", "Terros", "Zog'tar")
PREFISSI_TAKEOUT = ("Prompted ", "Hai inviato il prompt ", "Prompt inviato: ", "Prompt inviato ",
                    "Hai chiesto: ", "Hai chiesto ")


# --- lettura dei file (cartella, zip o file singolo) -----------------------------------------

def file_da(sorgente: Path):
    """(nome, bytes) di ogni file sotto la sorgente, anche dentro uno zip."""
    if sorgente.is_file() and zipfile.is_zipfile(sorgente):
        with zipfile.ZipFile(sorgente) as z:
            for info in z.infolist():
                if not info.is_dir():
                    yield info.filename, z.read(info)
    elif sorgente.is_file():
        yield sorgente.name, sorgente.read_bytes()
    else:
        for p in sorted(sorgente.rglob("*")):
            if p.is_file():
                yield str(p.relative_to(sorgente)), p.read_bytes()


def _json(dati: bytes):
    try:
        return json.loads(dati.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


# --- AI Studio -------------------------------------------------------------------------------

def _testo_chunk(c: dict) -> str:
    if c.get("parts"):
        return "".join(p.get("text", "") for p in c["parts"] if not p.get("thought"))
    return c.get("text", "")


def chat_aistudio(nome: str, dati: bytes) -> dict | None:
    d = _json(dati)
    if not isinstance(d, dict) or "chunkedPrompt" not in d:
        return None
    turni = []
    for c in d["chunkedPrompt"].get("chunks", []):
        if c.get("isThought"):
            continue
        testo = _testo_chunk(c).strip()
        allegato = next((k for k in ("driveImage", "inlineImage", "driveDocument", "inlineFile") if k in c), None)
        if not testo and allegato:
            testo = f"*[allegato: {allegato}]*"
        if testo:
            turni.append(("DM" if c.get("role") == "user" else "Gemini", testo))
    sistema = (d.get("systemInstruction") or {}).get("text", "").strip()
    return {"titolo": Path(nome).name, "fonte": nome, "data": "", "sistema": sistema,
            "modello": (d.get("runSettings") or {}).get("model", ""), "turni": turni}


# --- Takeout ---------------------------------------------------------------------------------

class _Testo(HTMLParser):
    """Testo di un frammento HTML, con un a capo per paragrafo e per voce di elenco."""

    BLOCCHI = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "pre"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pezzi: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCCHI:
            self.pezzi.append("\n")
        if tag == "li":
            self.pezzi.append("- ")

    def handle_data(self, data):
        self.pezzi.append(data)

    def testo(self) -> str:
        return re.sub(r"\n\s*\n+", "\n\n", "".join(self.pezzi)).strip()


def testo_html(frammento: str) -> str:
    t = _Testo()
    t.feed(frammento)
    return t.testo()


def _prompt(titolo: str) -> str:
    for p in PREFISSI_TAKEOUT:
        if titolo.startswith(p):
            return titolo[len(p):].strip()
    return titolo.strip()


def _di_gemini(v: dict) -> bool:
    """Una voce di «La mia attività» è di Gemini? Senza `header` né `products` non si può dire: si tiene."""
    marca = " ".join([str(v.get("header", ""))] + [str(x) for x in v.get("products", [])]).lower()
    return not marca.strip() or "gemini" in marca or "bard" in marca


def voci_takeout_json(dati: bytes) -> list[dict]:
    d = _json(dati)
    if not isinstance(d, list):
        return []
    voci = []
    for v in d:
        if not isinstance(v, dict) or "title" not in v or "time" not in v or not _di_gemini(v):
            continue
        risposta = "\n\n".join(testo_html(h.get("html", "")) for h in v.get("safeHtmlItem", []))
        voci.append({"ora": v["time"], "prompt": _prompt(v["title"]), "risposta": risposta.strip()})
    return voci


class _Celle(HTMLParser):
    """Le «outer-cell» di MyActivity.html: per ognuna il testo della prima «content-cell»."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.celle: list[str] = []
        self._prof = 0
        self._dentro: int | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            if self._dentro is not None and tag in _Testo.BLOCCHI:
                self._buf.append("\n")
            return
        self._prof += 1
        classi = dict(attrs).get("class", "") or ""
        if self._dentro is None and "content-cell" in classi and "mdl-typography--body-1" in classi:
            self._dentro, self._buf = self._prof, []
        elif self._dentro is not None:
            self._buf.append("\n")

    def handle_endtag(self, tag):
        if tag != "div":
            return
        if self._dentro == self._prof:
            self.celle.append(re.sub(r"\n\s*\n+", "\n\n", "".join(self._buf)).strip())
            self._dentro = None
        self._prof -= 1

    def handle_data(self, data):
        if self._dentro is not None:
            self._buf.append(data)


_ORA = re.compile(r"(\d{1,2} \w{3,4} \d{4},? \d{1,2}:\d{2}(?::\d{2})?(?: [A-Z]{2,5})?|"
                  r"\w{3} \d{1,2}, \d{4},? \d{1,2}:\d{2}:\d{2}\s?[AP]M(?: [A-Z]{2,5})?)")


_MESI = {m: i + 1 for i, m in enumerate(("gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"))}
_MESI.update({m: i + 1 for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"))})
_ORA_IT = re.compile(r"(\d{1,2}) (\w{3,4}) (\d{4}),? (\d{1,2}):(\d{2})(?::(\d{2}))?")
_ORA_EN = re.compile(r"(\w{3}) (\d{1,2}), (\d{4}),? (\d{1,2}):(\d{2}):(\d{2})\s?([AP]M)")


def ora_iso(testo: str) -> str:
    """«3 mag 2026, 20:11:00 CEST» o «May 3, 2026, 8:11:00 PM CEST» → «2026-05-03T20:11:00» (ora locale
    dell'esportazione, senza fuso). Se il mese non si riconosce torna la stringa com'è."""
    m = _ORA_IT.search(testo)
    if m and m.group(2).lower()[:3] in _MESI:
        g, mese, anno, h, mi, sec = int(m.group(1)), _MESI[m.group(2).lower()[:3]], int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6) or 0)
        return f"{anno:04d}-{mese:02d}-{g:02d}T{h:02d}:{mi:02d}:{sec:02d}"
    m = _ORA_EN.search(testo)
    if m and m.group(1).lower() in _MESI:
        h = int(m.group(4)) % 12 + (12 if m.group(7) == "PM" else 0)
        return f"{int(m.group(3)):04d}-{_MESI[m.group(1).lower()]:02d}-{int(m.group(2)):02d}T{h:02d}:{m.group(5)}:{m.group(6)}"
    return testo


def voci_takeout_html(dati: bytes) -> list[dict]:
    p = _Celle()
    p.feed(dati.decode("utf-8", errors="replace"))
    voci = []
    for cella in p.celle:
        m = _ORA.search(cella)
        if not m:
            continue
        prima, dopo = cella[:m.start()].strip(), cella[m.end():].strip()
        voci.append({"ora": ora_iso(m.group(0)), "prompt": _prompt(html.unescape(prima)), "risposta": dopo})
    return voci


def chat_takeout(sorgente: Path) -> list[dict]:
    voci = []
    # In un Takeout intero ci sono le attività di tutti i prodotti (Ricerca, YouTube, Maps...): si leggono
    # solo i file sotto una cartella o con un nome di Gemini (o Bard, il nome di prima). Un file dato da
    # solo si legge comunque: l'ha scelto il DM. Il JSON si filtra anche voce per voce (`_di_gemini`).
    uno_solo = sorgente.is_file() and not zipfile.is_zipfile(sorgente)
    for nome, dati in file_da(sorgente):
        basso = nome.lower()
        if not uno_solo and "gemini" not in basso and "bard" not in basso:
            continue
        if basso.endswith(".json"):
            voci += voci_takeout_json(dati)
        elif basso.endswith(".html"):
            voci += voci_takeout_html(dati)
    per_giorno: dict[str, list] = defaultdict(list)
    for v in voci:
        giorno = v["ora"][:10] if re.match(r"\d{4}-\d{2}-\d{2}", v["ora"]) else "senza-data"
        per_giorno[giorno].append(v)
    chat = []
    for giorno, vv in sorted(per_giorno.items()):
        if giorno == "senza-data":
            vv.reverse()  # date non riconosciute: Takeout elenca dalla più recente, si legge dalla più vecchia
        else:
            vv.sort(key=lambda v: v["ora"])
        turni = []
        for v in vv:
            turni.append(("DM", f"*{v['ora']}*\n\n{v['prompt']}"))
            if v["risposta"]:
                turni.append(("Gemini", v["risposta"]))
        chat.append({"titolo": f"gemini-{giorno}", "fonte": str(sorgente.name), "data": giorno,
                     "sistema": "", "modello": "", "turni": turni})
    return chat


# --- uscita ----------------------------------------------------------------------------------

def nome_file(titolo: str, usati: set[str]) -> str:
    base = re.sub(r"[^\w.-]+", "-", titolo, flags=re.UNICODE).strip("-.")[:80] or "chat"
    nome, k = f"{base}.md", 2
    while nome in usati:
        nome, k = f"{base}-{k}.md", k + 1
    usati.add(nome)
    return nome


def markdown(c: dict) -> str:
    righe = [f"# {c['titolo']}", "", f"- Fonte: `{c['fonte']}`"]
    if c["data"]:
        righe.append(f"- Data: {c['data']}")
    if c["modello"]:
        righe.append(f"- Modello: {c['modello']}")
    righe.append(f"- Turni: {len(c['turni'])}")
    if c["sistema"]:
        righe += ["", "## Istruzioni di sistema", "", c["sistema"]]
    for chi, testo in c["turni"]:
        righe += ["", f"## {chi}", "", testo]
    return "\n".join(righe) + "\n"


def conta_parole(testo: str, parole) -> dict[str, int]:
    basso = testo.lower()
    return {p: basso.count(p.lower()) for p in parole if basso.count(p.lower())}


def scrivi(chat: list[dict], out: Path, parole) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    usati: set[str] = set()
    indice = []
    for c in chat:
        md = markdown(c)
        f = nome_file(c["titolo"], usati)
        (out / f).write_text(md, encoding="utf-8")
        indice.append({"file": f, "data": c["data"], "turni": len(c["turni"]), "caratteri": len(md),
                       "parole": conta_parole(md, parole)})
    indice.sort(key=lambda r: (-sum(r["parole"].values()), r["file"]))
    righe = ["# Indice delle chat importate", "",
             "Ordinate per quante volte nominano la campagna: in cima quelle da leggere prima.", "",
             "| File | Data | Turni | Caratteri | Nomi della campagna |", "|---|---|---|---|---|"]
    for r in indice:
        nomi = ", ".join(f"{p} {n}" for p, n in sorted(r["parole"].items(), key=lambda x: -x[1])) or "—"
        righe.append(f"| [{r['file']}]({r['file']}) | {r['data'] or '—'} | {r['turni']} | {r['caratteri']} | {nomi} |")
    (out / "INDICE.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    (out / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    return indice


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fonte", choices=["aistudio", "takeout"])
    ap.add_argument("sorgente", type=Path, help="cartella, zip o file esportato")
    ap.add_argument("--out", type=Path, required=True, help="cartella di uscita, fuori dal repo")
    ap.add_argument("--parole", default=",".join(PAROLE), help="nomi da contare, separati da virgole")
    a = ap.parse_args(argv)
    if not a.sorgente.exists():
        print(f"ERRORE: {a.sorgente} non esiste", file=sys.stderr)
        return 2
    out = a.out.expanduser().resolve()
    if out == REPO or REPO in out.parents:
        print(f"ERRORE: {out} è dentro il repo; le chat restano fuori (PR #284)", file=sys.stderr)
        return 2
    parole = [p.strip() for p in a.parole.split(",") if p.strip()]
    if a.fonte == "aistudio":
        chat = [c for nome, dati in file_da(a.sorgente) if (c := chat_aistudio(nome, dati))]
    else:
        chat = chat_takeout(a.sorgente)
    if not chat:
        print(f"Nessuna chat riconosciuta in {a.sorgente} come «{a.fonte}». Se è un'esportazione vera, "
              "manda la struttura delle cartelle (non il contenuto) e adatto il lettore.", file=sys.stderr)
        return 3
    indice = scrivi(chat, out, parole)
    con_nomi = sum(1 for r in indice if r["parole"])
    print(f"✓ {len(indice)} file in {out}, {con_nomi} nominano la campagna; l'elenco è in {out / 'INDICE.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
