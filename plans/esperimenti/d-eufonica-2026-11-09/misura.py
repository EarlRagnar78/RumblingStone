"""La *d* eufonica: il rilevatore del repo contro LanguageTool (CODA D3).

LanguageTool ha la regola della norma (ST_03_001: *ad*/*ed* solo davanti alla
stessa vocale, *ad esempio* ammesso). È lo standard di fatto; questo script
misura se il rilevatore regex di `validate_lingua.py` trova le stesse righe sui
file di contenuto, perché la CI non ha Java né il server.

Uso (server LOCALE, `scripts/avvia_languagetool.sh`; il testo non esce dalla
macchina):
    python3 plans/esperimenti/d-eufonica-2026-11-09/misura.py http://127.0.0.1:8081

Stampa, per i soli file di contenuto e le sole righe che LanguageTool legge
(`ciclo_prosa.testo_piano` svuota tabelle e codice): concordi, solo
LanguageTool, solo regex, con le righe in disaccordo.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RADICE / "scripts"))
import ciclo_prosa  # noqa: E402
import validate_lingua as V  # noqa: E402

REGOLA = "ST_03_001"


def lt_righe(testo: str, url: str) -> dict[int, int]:
    piano = ciclo_prosa.testo_piano(testo)
    dati = urllib.parse.urlencode({"text": piano, "language": "it", "enabledOnly": "true",
                                   "enabledRules": REGOLA}).encode()
    with urllib.request.urlopen(url.rstrip("/") + "/v2/check", dati, timeout=300) as r:
        risposta = json.load(r)
    u = piano.encode("utf-16-le")
    out: dict[int, int] = {}
    for m in risposta.get("matches", []):
        riga = u[:2 * m["offset"]].decode("utf-16-le", "replace").count("\n") + 1
        out[riga] = out.get(riga, 0) + 1
    return out, piano.split("\n")


def regex_righe(testo: str) -> dict[int, int]:
    out: dict[int, int] = {}
    for n, _ in V.d_eufonica_righe(V.righe_da_controllare(testo)):
        out[n] = out.get(n, 0) + 1
    return out


def main(argv: list[str]) -> int:
    url = argv[1] if len(argv) > 1 else "http://127.0.0.1:8081"
    host = urllib.parse.urlsplit(url).hostname
    if host not in ("localhost", "127.0.0.1", "::1"):
        print("solo un server locale")
        return 2
    conc = solo_lt = solo_re = 0
    disaccordi: list[str] = []
    for f in V.file_di_contenuto():
        testo = f.read_text(encoding="utf-8", errors="ignore")
        lt, piano = lt_righe(testo, url)
        rx = regex_righe(testo)
        righe = testo.split("\n")
        for n in sorted(set(lt) | set(rx)):
            if n > len(piano) or not piano[n - 1].strip():
                continue            # riga che LanguageTool non legge (tabella, codice)
            a, b = lt.get(n, 0), rx.get(n, 0)
            conc += min(a, b)
            if a != b:
                solo_lt += max(0, a - b)
                solo_re += max(0, b - a)
                rel = f.relative_to(RADICE)
                disaccordi.append(f"{rel}:{n}: LT {a}, regex {b} — «{righe[n-1].strip()[:90]}»")
    print(f"concordi {conc} · solo LanguageTool {solo_lt} · solo regex {solo_re}")
    for d in disaccordi:
        print("  " + d)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
