#!/usr/bin/env python3
"""mcp_server.py — i tool del repo, esposti a un client MCP. Stdio, stdlib, allowlist.

Chiude la promessa di ADR-0012: `scripts/tools.manifest.json` e' la fonte di
verita' dei tool, ne veniva generato un descrittore MCP completo di 48 voci con
`inputSchema`... e **nessuno lo consumava**. Una fonte di verita' senza lettori
non resta vera a lungo: uno schema sbagliato non rompe niente finche' nessuno
prova a usarlo.

Il progetto per esteso — obiettivi, non obiettivi, modello di sicurezza,
tassonomia degli errori — sta in `plans/SPEC-SERVER-MCP.md`. Qui la sostanza:

    Questo processo esegue 48 programmi per conto di un agente.
    E' una superficie d'esecuzione, e va trattata come tale.

Le sei difese, che nel codice qui sotto si chiamano per nome:

    S-1  solo allowlist   — gli unici eseguibili sono quelli del manifest;
                            non esiste un tool «lancia questo comando»
    S-2  niente shell     — argv come lista, shell=False, mai interpolazione
    S-3  schema           — tipo, enum, nessuna chiave sconosciuta; prima di partire
    S-4  percorsi         — ogni `path` risolto e confinato sotto la radice del repo
    S-5  read-only        — chi scrive canone o committa e' ELENCATO ma non parte
                            senza --allow-write (ADR-0007: il canone si scrive su
                            un branch di gruppo, con l'occhio del DM sopra)
    S-6  tempo e taglia   — timeout 120 s, output al massimo 256 KiB

Uso:

    python3 scripts/mcp_server.py                 # read-only (difetto)
    python3 scripts/mcp_server.py --allow-write   # abilita i 5 che scrivono canone
    python3 scripts/mcp_server.py --verbose       # diagnostica su stderr
    python3 scripts/mcp_server.py --self-check    # non parla il protocollo: verifica e basta

⚠️ **stdout e' il canale del protocollo.** Una `print()` di troppo li' dentro
rompe il trasporto: la diagnostica va su stderr, sempre.

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "tools.manifest.json"

sys.path.insert(0, str(ROOT / "scripts"))
from tools_manifest import mcp_eseguibile, mcp_key  # noqa: E402  (le regole, condivise)

PROTOCOLLO = "2025-06-18"
NOME, VERSIONE = "rumblingstone-tools", "1.0.0"

TIMEOUT = 120          # S-6
TETTO_OUTPUT = 256 * 1024

# Errori JSON-RPC
PARSE, RICHIESTA, METODO, PARAMETRI, INTERNO = -32700, -32600, -32601, -32602, -32603


# --------------------------------------------------------------------------
# Il catalogo
# --------------------------------------------------------------------------
def carica(manifest: Path = MANIFEST) -> dict[str, dict]:
    """I tool esponibili, indicizzati per nome MCP. **S-1: questa e' l'allowlist.**"""
    dati = json.loads(manifest.read_text(encoding="utf-8"))
    fuori = {}
    for t in dati["tools"]:
        if not mcp_eseguibile(t):
            continue
        fuori[t["id"].replace("/", "_").replace("-", "_")] = t
    return fuori


def _scrive(t: dict) -> bool:
    se = t.get("side_effects", {})
    return bool(se.get("writes_canon") or se.get("git_commit"))


def descrittore(nome: str, t: dict) -> dict:
    """La voce `tools/list`: schema + **annotazioni**.

    Le annotazioni sono il pezzo che `docs/tools/mcp-tools.json` non aveva, ed e'
    quello che un client legge per sapere cosa sta per succedere: senza,
    `validate_prosa` e `state_apply` si assomigliano.
    """
    _T = {"int": "integer", "float": "number", "bool": "boolean",
          "path": "string", "str": "string", "choice": "string",
          "subcommand": "string"}
    props, obblig = {}, []
    for a in t.get("args", []):
        s: dict[str, Any] = {"type": _T.get(a["type"], "string"), "description": a["desc"]}
        if a.get("choices"):
            s["enum"] = a["choices"]
        if a.get("repeatable"):
            s = {"oneOf": [s, {"type": "array", "items": s}],
                 "description": a["desc"]}
        props[mcp_key(a["name"])] = s
        if a.get("required"):
            obblig.append(mcp_key(a["name"]))
    se = t.get("side_effects", {})
    descr = t["summary"]
    if _scrive(t):
        descr += ("  ⚠️ Scrive contenuto del repo" +
                  (" e fa commit git" if se.get("git_commit") else "") +
                  ": parte solo se il server è stato avviato con --allow-write.")
    return {
        "name": nome,
        "description": descr,
        "inputSchema": {"type": "object", "properties": props,
                        "required": obblig, "additionalProperties": False},
        "annotations": {
            "title": t["id"],
            "readOnlyHint": not _scrive(t),
            "destructiveHint": bool(se.get("git_commit")),
            "idempotentHint": bool(t.get("idempotent")),
            "openWorldHint": bool(se.get("network")),
        },
    }


# --------------------------------------------------------------------------
# Dagli argomenti alla riga di comando
# --------------------------------------------------------------------------
class Rifiuto(ValueError):
    """La chiamata non parte. Il messaggio va all'utente: dice **cosa** e **perche'**."""


def _path_sicuro(valore: str, chiave: str) -> str:
    """**S-4**: un percorso resta dentro il repo. Risolto, non solo guardato."""
    p = Path(valore)
    completo = (p if p.is_absolute() else ROOT / p).resolve()
    try:
        completo.relative_to(ROOT)
    except ValueError:
        raise Rifiuto(f"«{chiave}»: il percorso «{valore}» esce dalla radice del "
                      f"repo. I tool girano solo su file di questo repo.") from None
    return str(completo.relative_to(ROOT))


def _valida(valore: Any, a: dict, chiave: str) -> list[str]:
    """**S-3**: tipo ed `enum`. Restituisce i pezzi gia' pronti come stringa."""
    tipo = a["type"]
    if tipo == "bool":
        if not isinstance(valore, bool):
            raise Rifiuto(f"«{chiave}» vuole vero/falso, non {type(valore).__name__}")
        return []
    valori = valore if isinstance(valore, list) else [valore]
    if len(valori) > 1 and not a.get("repeatable"):
        raise Rifiuto(f"«{chiave}» non è ripetibile")
    fuori = []
    for v in valori:
        if tipo == "int":
            if isinstance(v, bool) or not isinstance(v, int):
                raise Rifiuto(f"«{chiave}» vuole un intero")
        elif tipo == "float":
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise Rifiuto(f"«{chiave}» vuole un numero")
        elif not isinstance(v, (str, int, float)):
            raise Rifiuto(f"«{chiave}» vuole una stringa")
        s = str(v)
        if a.get("choices") and s not in a["choices"]:
            raise Rifiuto(f"«{chiave}»: «{s}» non è fra {', '.join(a['choices'])}")
        fuori.append(_path_sicuro(s, chiave) if tipo == "path" else s)
    return fuori


def costruisci(t: dict, argomenti: dict[str, Any]) -> list[str]:
    """La riga di comando, come **lista** (S-2: mai una stringa, mai una shell)."""
    per_chiave = {mcp_key(a["name"]): a for a in t.get("args", [])}
    sconosciute = set(argomenti) - set(per_chiave)
    if sconosciute:
        raise Rifiuto("argomenti non previsti: " + ", ".join(sorted(sconosciute)))
    for chiave, a in per_chiave.items():
        if a.get("required") and chiave not in argomenti:
            raise Rifiuto(f"manca l'argomento obbligatorio «{chiave}»")

    # ⚠️ **Non** da `invocation`: quella e' una riga d'esempio per gli umani, e
    # mescola il comando con segnaposto e flag di comodo — `MANIFEST.json`,
    # `<cartella>`, `--all`, `--check`. Nove tool su quarantasei ne hanno uno, e
    # passarla verbatim vorrebbe dire lanciare `--all` che nessuno ha chiesto.
    # Il fatto a macchina sono `path` e `language`.
    argv = ([sys.executable] if t["language"] == "python" else []) + [str(ROOT / t["path"])]
    opzioni: list[str] = []
    posizionali: list[str] = []
    for chiave, a in per_chiave.items():          # l'ordine e' quello del manifest
        if chiave not in argomenti:
            continue
        pezzi = _valida(argomenti[chiave], a, chiave)
        flag = a["name"].split("/")[0]
        if not flag.startswith("-"):
            posizionali.extend(pezzi)
            continue
        if a["type"] == "bool":
            if argomenti[chiave]:
                opzioni.append(flag)
            continue
        # `--flag=valore` e non `--flag valore`: un valore che comincia per «-»
        # verrebbe letto come un'altra opzione, ed e' il modo in cui un argomento
        # si trasforma in un comando.
        opzioni.extend(f"{flag}={p}" for p in pezzi)
    argv += opzioni
    if posizionali:
        # `--` chiude le opzioni: da qui in poi sono valori, anche se cominciano
        # per «-». argparse lo capisce, ed e' la stessa difesa di sopra.
        argv.append("--")
        argv.extend(posizionali)
    return argv


# --------------------------------------------------------------------------
# L'esecuzione
# --------------------------------------------------------------------------
def _tronca(s: str, tetto: int) -> tuple[str, int]:
    if len(s) <= tetto:
        return s, 0
    return s[:tetto] + f"\n… [troncato: {len(s) - tetto} byte in più]", len(s) - tetto


def esegui(t: dict, argv: list[str], timeout: int = TIMEOUT,
           tetto: int = TETTO_OUTPUT) -> dict:
    """Lancia e traduce. Un'uscita ≠ 0 e' un **risultato**, non un guasto."""
    inizio = time.monotonic()
    try:
        esito = subprocess.run(                       # S-2: shell=False (difetto)
            argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        return {"isError": True, "content": [{"type": "text", "text":
                f"⏱ «{t['id']}» non ha finito entro {timeout} s ed è stato fermato."}]}
    except FileNotFoundError:
        return {"isError": True, "content": [{"type": "text", "text":
                f"✗ eseguibile non trovato per «{t['id']}»: {argv[0]}"}]}
    durata = time.monotonic() - inizio

    corpo, _ = _tronca(esito.stdout or "", tetto)
    errore, _ = _tronca(esito.stderr or "", tetto // 4)
    testo = corpo
    if errore.strip():
        testo += ("\n" if testo else "") + "— stderr —\n" + errore
    if esito.returncode != 0:
        # Il manifest sa gia' cosa vuol dire il codice 3 di suggest_encounter.
        # Tradurlo e' la differenza fra un agente che ritenta a caso e uno che
        # cambia parametri.
        senso = t.get("exit_codes", {}).get(str(esito.returncode))
        testa = f"uscita {esito.returncode}" + (f" — {senso}" if senso else "")
        testo = f"[{t['id']}: {testa}]\n" + testo
    return {
        "isError": esito.returncode != 0,
        "content": [{"type": "text", "text": testo or f"[{t['id']}: nessun output]"}],
        "_durata": round(durata, 2), "_codice": esito.returncode,
    }


# --------------------------------------------------------------------------
# Il protocollo
# --------------------------------------------------------------------------
class Server:
    def __init__(self, catalogo: dict[str, dict], scrittura: bool = False,
                 verbose: bool = False, timeout: int = TIMEOUT) -> None:
        self.catalogo, self.scrittura, self.verbose = catalogo, scrittura, verbose
        self.timeout = timeout

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[mcp] {msg}", file=sys.stderr, flush=True)

    # -- metodi -----------------------------------------------------------
    def initialize(self, _p: dict) -> dict:
        return {"protocolVersion": PROTOCOLLO,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": NOME, "version": VERSIONE},
                "instructions": (
                    "I tool di RumblingStone, dal manifest di ADR-0012. "
                    "Girano dalla radice del repo. Chi scrive contenuto o fa "
                    "commit è marcato e " +
                    ("è abilitato (--allow-write)." if self.scrittura else
                     "NON parte: il server è read-only."))}

    def tools_list(self, _p: dict) -> dict:
        return {"tools": [descrittore(n, t) for n, t in sorted(self.catalogo.items())]}

    def tools_call(self, p: dict) -> dict:
        nome = p.get("name")
        t = self.catalogo.get(nome)
        if t is None:                                       # S-1
            raise Rifiuto(f"tool sconosciuto: «{nome}». Sono esposti solo i tool "
                          f"dichiarati in scripts/tools.manifest.json.")
        if _scrive(t) and not self.scrittura:               # S-5
            raise Rifiuto(
                f"«{nome}» scrive contenuto del repo"
                + (" e fa commit git" if t["side_effects"].get("git_commit") else "")
                + ". Il server è avviato in sola lettura: il canone si scrive su "
                  "un branch di gruppo con l'occhio del DM sopra (ADR-0007). "
                  "Per abilitarlo: riavviare con --allow-write.")
        argv = costruisci(t, p.get("arguments") or {})
        self._log(f"{nome} → {' '.join(argv)}")
        r = esegui(t, argv, self.timeout)
        self._log(f"{nome} ← codice {r.pop('_codice', '?')} in {r.pop('_durata', '?')} s")
        return r

    # -- ciclo ------------------------------------------------------------
    def gestisci(self, req: dict) -> dict | None:
        mid, metodo = req.get("id"), req.get("method")
        if metodo is None:
            return self._err(mid, RICHIESTA, "richiesta senza «method»")
        if metodo.startswith("notifications/"):
            return None                                     # le notifiche non si rispondono
        tabella = {"initialize": self.initialize, "tools/list": self.tools_list,
                   "tools/call": self.tools_call, "ping": lambda _p: {}}
        fn = tabella.get(metodo)
        if fn is None:
            return self._err(mid, METODO, f"metodo non gestito: {metodo}")
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": fn(req.get("params") or {})}
        except Rifiuto as e:
            return self._err(mid, PARAMETRI, str(e))
        except Exception as e:                              # mai far cadere il server
            self._log(f"eccezione in {metodo}: {type(e).__name__}: {e}")
            return self._err(mid, INTERNO, f"{type(e).__name__}: {e}")

    @staticmethod
    def _err(mid: Any, codice: int, msg: str) -> dict:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": codice, "message": msg}}

    def gira(self, entrata=None, uscita=None) -> int:
        entrata, uscita = entrata or sys.stdin, uscita or sys.stdout
        self._log(f"{len(self.catalogo)} tool · "
                  f"{'scrittura abilitata' if self.scrittura else 'sola lettura'}")
        for riga in entrata:
            riga = riga.strip()
            if not riga:
                continue
            try:
                req = json.loads(riga)
            except json.JSONDecodeError as e:
                self._scrivi(uscita, self._err(None, PARSE, f"JSON non valido: {e}"))
                continue
            for r in ([self.gestisci(x) for x in req] if isinstance(req, list)
                      else [self.gestisci(req)]):
                if r is not None:
                    self._scrivi(uscita, r)
        return 0

    @staticmethod
    def _scrivi(uscita, oggetto: dict) -> None:
        uscita.write(json.dumps(oggetto, ensure_ascii=False) + "\n")
        uscita.flush()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--allow-write", action="store_true",
                    help="abilita i tool che scrivono contenuto o fanno commit")
    ap.add_argument("--verbose", action="store_true", help="diagnostica su stderr")
    ap.add_argument("--timeout", type=int, default=TIMEOUT,
                    help=f"secondi per chiamata (default {TIMEOUT})")
    ap.add_argument("--self-check", action="store_true",
                    help="verifica catalogo e schemi, non parla il protocollo")
    a = ap.parse_args(argv)

    catalogo = carica()
    if a.self_check:
        scrivono = sorted(n for n, t in catalogo.items() if _scrive(t))
        print(f"✓ mcp_server: {len(catalogo)} tool nel catalogo")
        print(f"  {len(scrivono)} scrivono contenuto (bloccati senza --allow-write): "
              f"{', '.join(scrivono)}")
        # Ogni tool si deve poter costruire con i soli obbligatori riempiti, e
        # la riga risultante non deve contenere metacaratteri di shell: se ce ne
        # fosse uno, vorrebbe dire che sta passando per una stringa invece che
        # per la lista argv, ed e' l'unico modo in cui S-2 puo' rompersi.
        finti = {"int": 1, "float": 1.0, "bool": True, "path": "README.md"}
        guasti = 0
        for n, t in catalogo.items():
            d = descrittore(n, t)
            assert d["inputSchema"]["type"] == "object", n
            assert d["annotations"]["readOnlyHint"] is not _scrive(t), n
            arg = {}
            for a in t.get("args", []):
                if not a.get("required"):
                    continue
                arg[mcp_key(a["name"])] = (a["choices"][0] if a.get("choices")
                                           else finti.get(a["type"], "x"))
            try:
                argv = costruisci(t, arg)
            except Rifiuto as e:
                print(f"  ✗ {n}: {e}"); guasti += 1; continue
            if any(c in pezzo for pezzo in argv for c in ";|&`$><\n"):
                print(f"  ✗ {n}: metacarattere di shell in argv: {argv}"); guasti += 1
        print(f"  {len(catalogo) - guasti}/{len(catalogo)} costruiscono una riga "
              f"di comando valida e senza metacaratteri")
        return 1 if guasti else 0
    return Server(catalogo, a.allow_write, a.verbose, a.timeout).gira()


if __name__ == "__main__":
    raise SystemExit(main())
