#!/usr/bin/env python3
"""lettura_a_scene.py — il master servito una scena alla volta, senza guardare avanti.

Adattato da `agent_skills/first-reader/scripts/feed.py` di awesome-llm-apps
(Shubham Saboo, Apache 2.0, commit 4bf51ab704fb2c5b3803cd5191b30d7dcdb51dc2).
**Modificato** per il repo (ADR-0076): il passaggio e' la scena e non un blocco
di 85 parole (D3 di PIANO-AGENT-SKILLS-ESTERNE); il diario ha i campi fissi
delle rubriche di `rumblingstone-playtest`; alla chiusura sul disco va
l'impronta di ogni scena, mai il testo.

Perche'. Il lettore e il playtester a freddo ricevevano il modulo intero, e
la rubrica gli chiedeva di trovare `L-ORDINE` («un'informazione serve prima
del punto in cui compare») dopo che il punto dopo l'avevano gia' letto. Qui il
testo vive solo nella memoria di un processo su 127.0.0.1: il lettore riceve un
indirizzo con un gettone, mai il percorso del file, e la scena dopo arriva solo
dopo una riga di diario e dopo il tempo minimo per leggerla.

I passaggi, nell'ordine del file: la premessa (tutto cio' che sta prima della
prima scena), ogni scena col titolo del profilo in `plans/copertura-scene.json`
(`### SCENA` per i master), i tratti fra una scena e l'altra, la coda.

Il diario di ogni passaggio, su una riga:

    ago=<-2..+2> | mi aspettavo: … | ho trovato: … | so adesso: … [| codici: L-ORDINE …]

`so adesso` e' cosa sanno i PG a questo punto, e da chi: e' il campo che rende
visibile `L-ORDINE`, perche' il diario di una scena dice «non so X» e X
compare due scene dopo.

⚠️ Il limite, da dire: il lettore ha il repo davanti, e se cerca il master con
`grep` lo trova. Il meccanismo gli toglie il percorso, non la possibilita'. Si
controlla dopo: un diario che cita cose delle scene seguenti ha guardato avanti.

ORCHESTRATORE, in background:
    python3 scripts/lettura_a_scene.py servi <master> --corsa <cartella> \\
        --lettori lettore,playtester --pronto <cartella>/indirizzi.json
LETTORE (READER_FEED=<il suo indirizzo> nell'ambiente):
    python3 scripts/lettura_a_scene.py inizia
    python3 scripts/lettura_a_scene.py avanti --diario "ago=+1 | mi aspettavo: … | ho trovato: … | so adesso: …"
    python3 scripts/lettura_a_scene.py smetti --diario "ago=-2 | … perche' mi fermo"
ORCHESTRATORE, per guardare e chiudere:
    python3 scripts/lettura_a_scene.py progresso --admin <indirizzo-admin>
    python3 scripts/lettura_a_scene.py chiudi --admin <indirizzo-admin>
    python3 scripts/lettura_a_scene.py diario <cartella>/<lettore>

Solo libreria standard, nessuna rete oltre 127.0.0.1.
Exit code: 0 = ok · 1 = diario rifiutato o lettura gia' chiusa · 2 = errore d'uso.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import copertura_scene as cs  # noqa: E402  (il riconoscitore delle scene e' uno solo)

#: Secondi per parola prima che la scena dopo si possa chiedere. Un lettore
#: onesto non se ne accorge (238 parole al minuto sono ~0,25 s), chi corre si'.
TEMPO_PER_PAROLA = 0.08
DIARIO_MINIMO = 25
_AGO = re.compile(r"\bago\s*=\s*([+-]?\d)\b", re.I)
CAMPI_DIARIO = ("mi aspettavo", "ho trovato", "so adesso")


def impronta(testo: str) -> str:
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def profilo_di(relativo: str) -> dict:
    """Il profilo del master in `copertura-scene.json`, o quello dei master DEF."""
    for m in cs.moduli(cs.carica_config()):
        if m["file"] == relativo:
            return m
    return {}


def passaggi(testo: str, profilo: "dict | None" = None) -> "list[tuple[str, str]]":
    """(titolo, testo) nell'ordine del file, senza perdere una riga.

    La premessa e i tratti fra le scene diventano passaggi a se': il lettore
    legge il modulo come il DM al tavolo, dall'inizio alla fine.
    """
    profilo = profilo or {}
    rx = profilo.get("scena", cs.SCENA_DEF)
    trovate = cs.scene(testo, rx, profilo.get("escludi"))
    out, cursore = [], 0
    for titolo, corpo in trovate:
        inizio = testo.find(corpo, cursore)
        if inizio < 0:
            continue
        prima = testo[cursore:inizio]
        if prima.strip():
            out.append(("premessa" if not out else "fra le scene", prima))
        out.append((titolo, corpo))
        cursore = inizio + len(corpo)
    resto = testo[cursore:]
    if resto.strip():
        out.append(("coda" if out else "intero", resto))
    return out


def controlla_diario(voce: str) -> "str | None":
    """None se la riga di diario e' accettabile, altrimenti il motivo del rifiuto."""
    voce = (voce or "").strip()
    if len(voce) < DIARIO_MINIMO:
        return f"diario sotto i {DIARIO_MINIMO} caratteri: cosa e' successo in te leggendo?"
    m = _AGO.search(voce)
    if not m or not -2 <= int(m.group(1)) <= 2:
        return "manca «ago=» fra -2 e +2"
    minuscolo = voce.lower()
    mancanti = [c for c in CAMPI_DIARIO if c not in minuscolo]
    if mancanti:
        return f"mancano i campi: {', '.join(mancanti)}"
    return None


class Lettura:
    """Il testo in memoria, un cursore per lettore, e niente su disco fino alla fine."""

    def __init__(self, master: Path, corsa: Path, nomi: "list[str]", persone: dict,
                 tempo_per_parola: float = TEMPO_PER_PAROLA):
        testo = master.read_text(encoding="utf-8")
        relativo = master.resolve().relative_to(ROOT).as_posix() if master.resolve().is_relative_to(ROOT) else master.name
        self.passaggi = passaggi(testo, profilo_di(relativo))
        self.impronta_master = impronta(testo)
        self.master = relativo
        self.corsa = corsa
        self.tempo = tempo_per_parola
        self.admin = secrets.token_urlsafe(18)
        self.chiusa = False
        self.blocco = threading.Lock()
        self.lettori: "dict[str, dict]" = {}
        for nome in nomi:
            (corsa / nome).mkdir(parents=True, exist_ok=True)
            (corsa / nome / "diario.jsonl").write_text("", encoding="utf-8")
            self.lettori[secrets.token_urlsafe(18)] = {
                "nome": nome, "persona": persone.get(nome, nome), "cursore": 0,
                "iniziato": None, "servito": None, "finito": False, "smesso_a": None}

    def _pagina(self, r: dict) -> dict:
        i = r["cursore"]
        r["servito"] = time.time()
        titolo, corpo = self.passaggi[i]
        resto = sum(len(t.split()) for _, t in self.passaggi[i + 1:])
        return {"intestazione": f"--- PASSAGGIO {i + 1}/{len(self.passaggi)} · {titolo} "
                                f"({resto} parole dopo questo) ---",
                "testo": corpo, "indice": i + 1, "totale": len(self.passaggi),
                "piede": "--- scrivi il diario: avanti --diario \"ago=… | mi aspettavo: … | "
                         "ho trovato: … | so adesso: …\" (o smetti --diario \"…\") ---"}

    def inizia(self, r: dict) -> dict:
        if r["finito"]:
            return {"errore": "lettura gia' finita"}
        if r["iniziato"] is None:
            r["iniziato"] = time.time()
        return self._pagina(r)

    def _scrivi(self, r: dict, voce: str, smesso: bool, controlla_tempo: bool) -> "str | None":
        motivo = controlla_diario(voce)
        if motivo:
            return motivo
        if controlla_tempo and r["servito"] is not None and self.tempo > 0:
            minimo = max(2.0, len(self.passaggi[r["cursore"]][1].split()) * self.tempo)
            trascorso = time.time() - r["servito"]
            if trascorso < minimo:
                return f"troppo presto: servono circa {minimo:.0f} s per questo passaggio, ne sono passati {trascorso:.0f}"
        riga = {"passaggio": r["cursore"] + 1, "titolo": self.passaggi[r["cursore"]][0],
                "smesso": smesso, "diario": voce.strip(), "t": time.time()}
        with (self.corsa / r["nome"] / "diario.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(riga, ensure_ascii=False) + "\n")
        return None

    def avanti(self, r: dict, voce: str) -> dict:
        if r["finito"] or r["iniziato"] is None:
            return {"errore": "prima «inizia»" if r["iniziato"] is None else "lettura gia' finita"}
        motivo = self._scrivi(r, voce, False, True)
        if motivo:
            return {"rifiutato": motivo}
        r["cursore"] += 1
        if r["cursore"] >= len(self.passaggi):
            r["finito"] = True
            r["cursore"] = len(self.passaggi) - 1
            self._forse_chiudi()
            return {"fine": "Fine del modulo. Il diario dell'ultimo passaggio e' registrato."}
        return self._pagina(r)

    def smetti(self, r: dict, voce: str) -> dict:
        if r["finito"] or r["iniziato"] is None:
            return {"errore": "niente da smettere"}
        motivo = self._scrivi(r, voce, True, False)
        if motivo:
            return {"rifiutato": motivo}
        r["finito"], r["smesso_a"] = True, r["cursore"] + 1
        self._forse_chiudi()
        return {"fine": f"Fermato al passaggio {r['smesso_a']}/{len(self.passaggi)}: e' il primo rilievo."}

    def progresso(self) -> dict:
        return {r["nome"]: {"passaggio": r["cursore"] + 1, "di": len(self.passaggi),
                            "finito": r["finito"], "smesso_a": r["smesso_a"]}
                for r in self.lettori.values()}

    def _forse_chiudi(self) -> None:
        if all(r["finito"] for r in self.lettori.values()):
            self.chiudi()

    def chiudi(self) -> None:
        """Sul disco: titoli e impronte. Il testo del master non si copia in `plans/`."""
        for r in self.lettori.values():
            stato = {"master": self.master, "impronta_master": self.impronta_master,
                     "persona": r["persona"], "finito": r["finito"], "smesso_a": r["smesso_a"],
                     "passaggi": [{"titolo": t, "impronta": impronta(c), "parole": len(c.split())}
                                  for t, c in self.passaggi]}
            (self.corsa / r["nome"] / "stato.json").write_text(
                json.dumps(stato, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.chiusa = True


class _Gestore(BaseHTTPRequestHandler):
    lettura: "Lettura | None" = None
    server_ref = None

    def log_message(self, *_):
        pass

    def _invia(self, codice: int, dati: dict) -> None:
        corpo = json.dumps(dati, ensure_ascii=False).encode("utf-8")
        self.send_response(codice)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _instrada(self, metodo: str) -> None:
        parti = [p for p in self.path.split("?")[0].split("/") if p]
        if len(parti) != 2:
            return self._invia(404, {"errore": "non trovato"})
        gettone, azione = parti
        dati = {}
        if metodo == "POST":
            n = int(self.headers.get("Content-Length") or 0)
            try:
                dati = json.loads(self.rfile.read(n) or b"{}") if n else {}
            except json.JSONDecodeError:
                dati = {}
        lt = self.lettura
        with lt.blocco:
            if gettone == lt.admin:
                if azione == "progresso":
                    return self._invia(200, lt.progresso())
                if azione == "chiudi":
                    lt.chiudi()
                    self._invia(200, {"chiusa": True})
                    threading.Thread(target=self.server_ref.shutdown, daemon=True).start()
                    return
                return self._invia(404, {"errore": "non trovato"})
            r = lt.lettori.get(gettone)
            if r is None:
                return self._invia(404, {"errore": "non trovato"})
            azioni = {("inizia", "GET"): lambda: lt.inizia(r),
                      ("avanti", "POST"): lambda: lt.avanti(r, dati.get("diario", "")),
                      ("smetti", "POST"): lambda: lt.smetti(r, dati.get("diario", ""))}
            fare = azioni.get((azione, metodo))
            return self._invia(200, fare()) if fare else self._invia(404, {"errore": "non trovato"})

    def do_GET(self):
        self._instrada("GET")

    def do_POST(self):
        self._instrada("POST")


def avvia_server(lettura: Lettura, porta: int = 0) -> "tuple[ThreadingHTTPServer, str]":
    server = ThreadingHTTPServer(("127.0.0.1", porta), _Gestore)
    _Gestore.lettura, _Gestore.server_ref = lettura, server
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def _chiama(base: str, azione: str, dati: "dict | None" = None) -> dict:
    corpo = json.dumps(dati).encode() if dati is not None else None
    req = urlrequest.Request(base.rstrip("/") + "/" + azione, data=corpo,
                             method="POST" if corpo is not None else "GET",
                             headers={"Content-Type": "application/json"})
    try:
        with urlrequest.urlopen(req, timeout=30) as risposta:
            return json.loads(risposta.read())
    except HTTPError as e:
        raise SystemExit(f"lettura: {e.code} (indirizzo sbagliato, o la lettura e' chiusa)")
    except OSError as e:
        raise SystemExit(f"lettura non raggiungibile a {base}: {e}")


def _stampa(esito: dict) -> int:
    if "rifiutato" in esito:
        print("RIFIUTATO: " + esito["rifiutato"])
        return 1
    if "errore" in esito:
        print(esito["errore"])
        return 1
    if "fine" in esito:
        print(esito["fine"])
        return 0
    print(esito["intestazione"], esito["testo"], esito["piede"], sep="\n")
    return 0


def _indirizzo() -> str:
    base = os.environ.get("READER_FEED")
    if not base:
        raise SystemExit("manca READER_FEED: l'indirizzo lo da' chi orchestra")
    return base


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("servi", help="serve il master ai lettori (in background)")
    s.add_argument("master", type=Path)
    s.add_argument("--corsa", type=Path, required=True, help="cartella della corsa")
    s.add_argument("--lettori", required=True, help="nomi separati da virgola, es. lettore,playtester")
    s.add_argument("--persona", action="append", default=[], help="nome=una riga di persona (ripetibile)")
    s.add_argument("--pronto", type=Path, help="scrive qui gli indirizzi in JSON")
    s.add_argument("--porta", type=int, default=0)
    s.add_argument("--tempo", type=float, default=TEMPO_PER_PAROLA, help="secondi per parola; 0 disattiva")
    sub.add_parser("inizia", help="(lettore) la prima scena, o di nuovo quella corrente")
    for nome in ("avanti", "smetti"):
        p = sub.add_parser(nome, help=f"(lettore) {nome}")
        p.add_argument("--diario", required=True)
    for nome in ("progresso", "chiudi"):
        p = sub.add_parser(nome, help=f"(orchestratore) {nome}")
        p.add_argument("--admin", required=True)
    p = sub.add_parser("diario", help="stampa il diario di un lettore, a lettura chiusa")
    p.add_argument("cartella", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "servi":
        persone = dict(x.split("=", 1) for x in a.persona if "=" in x)
        nomi = [n.strip() for n in a.lettori.split(",") if n.strip()]
        lettura = Lettura(a.master, a.corsa, nomi, persone, a.tempo)
        server, base = avvia_server(lettura, a.porta)
        indirizzi = {"admin": f"{base}/{lettura.admin}",
                     "lettori": {r["nome"]: f"{base}/{t}" for t, r in lettura.lettori.items()}}
        print(f"LETTURA servita: {len(lettura.passaggi)} passaggi, lettori: {', '.join(nomi)}")
        for nome, url in indirizzi["lettori"].items():
            print(f"lettore {nome}: READER_FEED={url}")
        print(f"admin: {indirizzi['admin']}")
        print("A ogni lettore SOLO il suo indirizzo: mai il percorso del master.", flush=True)
        if a.pronto:
            a.pronto.write_text(json.dumps(indirizzi, indent=2) + "\n", encoding="utf-8")
        try:
            server.serve_forever()
        finally:
            if not lettura.chiusa:
                lettura.chiudi()
        return 0
    if a.cmd == "inizia":
        return _stampa(_chiama(_indirizzo(), "inizia"))
    if a.cmd in ("avanti", "smetti"):
        return _stampa(_chiama(_indirizzo(), a.cmd, {"diario": a.diario}))
    if a.cmd == "progresso":
        print(json.dumps(_chiama(a.admin, "progresso"), indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "chiudi":
        print(json.dumps(_chiama(a.admin, "chiudi")))
        return 0
    if a.cmd == "diario":
        stato = json.loads((a.cartella / "stato.json").read_text(encoding="utf-8"))
        esito = "finito" if not stato["smesso_a"] else f"fermato al passaggio {stato['smesso_a']}"
        print(f"DIARIO · {stato['persona']} · {stato['master']} · {esito} di {len(stato['passaggi'])}")
        for riga in (a.cartella / "diario.jsonl").read_text(encoding="utf-8").splitlines():
            v = json.loads(riga)
            print(f"[{v['passaggio']} · {v['titolo']}] {'SMESSO ' if v['smesso'] else ''}{v['diario']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
