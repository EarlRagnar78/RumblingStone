"""Confronta gli statblocchi alternativi della chat Gemini «Organizing D&D
Campaign Info» con le schede canone di ARC08-02 (card INVENTARIO D4).

La chat resta privata su Drive: questo script la legge da un percorso dato
(il testo dei turni del modello, estratto dal JSON di AI Studio saltando i
«pensieri») e stampa solo numeri. Nel repo non entra una riga della chat.

Uso:
    python3 confronta.py CHAT.txt > misure.md

Per ogni PNG: GS, CA, pf, Tempra/Riflessi/Volontà, iniziativa, primo bonus
dell'attacco completo, CD più alta. Per ogni unità: AU, DU (CAU nella chat),
gli altri campi delle unità non si confrontano (vedi misura_unita). Una cella vale ★ quando la chat è più forte del canone.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
CANONE = RADICE / "08_La Battaglia Di Hammerfist" / "ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md"

# nome nella chat → titolo della sezione nel canone (ARC08-02)
PNG = {
    "FAUCA DI PALUDE": "FAUCI DI PALUDE",
    "GORTHAK IL TRIFRONTE": "GORTHAK IL TRIFRONTE",
    "GENERALE GRIMJAW": "GENERALE GRIMJAW",
    "RE THOREK HAMMERFIST": "RE THOREK HAMMERFIST",
    "MADRE SUPERIORA DANA FORGIAPIETRA": "MADRE SUPERIORA DANA FORGIAPIETRA",
    "LE CANTATRICI DELLA PIETRA": "LE CANTITRICI DELLA PIETRA",
    "SIGNORE VENTOLESTO": "SIGNORE VENTOLESTO",
    "ORION PELLEORSA": "ORION PELLEORSA",
    "MAESTRO TEMPESTAS": "MAESTRO TEMPESTAS",
    "BORIN FERROPUGNO": "BORIN FERROPUGNO",
    "DARA OCCHIOLESTO": "DARA OCCHIOLESTO",
    "THORIN RUNAFORTE": "THORIN RUNAFORTE",
    "NALA CANTAPIETRE": "NALA CANTAPIETRE",
    "RANGER ELFICI SUI GUFI": None,
}
UNITA = {
    "ORCHI BERSERKER": "FANTERIA ORCHESCA",
    "HOBGOBLIN FANTI": "FANTERIA HOBGOBLIN",
    "HOBGOBLIN ARCIMAGHI DRACONICI": None,
    "GIGANTI DELLE COLLINE": "GIGANTI DELLE COLLINE",
    "BUGBEAR INFILTRATORI": None,
    "GUERRIERI NANICI VETERANI": "GUERRIERI NANICI VETERANI",
    "BALISTRIERI NANICI": "BALESTRIERI NANICI",
    "GUARDIE D'ÉLITE OROG": "OROG GUARDIE NERE",
    "SCIAMANI DRACONICI HOBGOBLIN": "SHAMANI DRACONICI",
    "RANGER ELFICI A CAVALLO DEI GUFI": None,
    "CAVALIERI DEI GUFI CELESTI": None,
}
CAMPI_PNG = ("gs", "ca", "pf", "temp", "rifl", "vol", "init", "att", "cd")
CAMPI_UNITA = ("au", "du")


def sezioni(testo: str) -> dict[str, str]:
    """Titolo (maiuscolo, senza grassetto né numero) → corpo; vince l'ultima."""
    out: dict[str, str] = {}
    parti = re.split(r"^#{1,4} +(.+)$", testo, flags=re.M)
    ultimo = None
    for titolo, corpo in zip(parti[1::2], parti[2::2]):
        if re.match(r"\*[^*]", titolo.strip()) and ultimo:
            # sottotitolo in corsivo («### *Drago Nero, …, GS 15*»): resta col PNG
            out[ultimo] += titolo + "\n" + corpo
            continue
        t = re.sub(r"[*_]", "", titolo)
        t = re.sub(r"^\d+\.\s*", "", t).split(",")[0].split("(")[0].strip().upper()
        t = re.sub(r"\s*-\s*CONTINUA$", "", t)
        out[t] = titolo + "\n" + corpo
        ultimo = t
    return out


def _num(pat: str, s: str, segno: bool = False) -> int | None:
    m = re.search(pat, s, flags=re.I | re.M)
    if not m:
        return None
    return int(m.group(1))


SEP = r"[\s|*:]*"


def _att(corpo: str) -> int | None:
    """Primo bonus dell'attacco completo (o della mischia): il «+N» seguito da
    «/», da «(» o da «in mischia», non il potenziamento dell'arma («+1*»)."""
    for etichetta in ("Attacco Completo", "Attacco Melee", "Mischia", "Attacco"):
        m = re.search(etichetta + r"[^\n]*", corpo)
        if not m:
            continue
        b = re.search(r"\+(\d+)(?=/|\s*\(|\s*in mischia|\*\*)", m.group(0)[len(etichetta):])
        if b:
            return int(b.group(1))
    return None


def misura_png(corpo: str) -> dict[str, int | None]:
    cds = [int(x) for x in re.findall(r"CD (\d+)", corpo)]
    ini = re.search(r"Iniziativa" + SEP + r"([+−-]\d+)", corpo)
    return {
        "gs": _num(r"GS (\d+)", corpo),
        "ca": _num(r"\*\*CA\b" + SEP + r"(\d+)", corpo),
        "pf": _num(r"\*\*PF\b" + SEP + r"(\d+)", corpo),
        "temp": _num(r"Temp(?:ra)?" + SEP + r"\+(\d+)", corpo),
        "rifl": _num(r"Rifl(?:essi)?" + SEP + r"\+(\d+)", corpo),
        "vol": _num(r"Vol(?:ontà)?" + SEP + r"\+(\d+)", corpo),
        "init": int(ini.group(1).replace("−", "-")) if ini else None,
        "att": _att(corpo),
        "cd": max(cds) if cds else None,
    }


def misura_unita(corpo: str) -> dict[str, int | None]:
    """AU e DU sul d20. I PFU non si confrontano: nella chat sono una riserva
    di danni (10 danni d'area = 10 PFU), nel canone 1 PFU = 1 creatura."""
    lab = r"(?:\s*\([^)]*\))?" + SEP
    au = _num(r"(?:Bonus Attacco Unità|\bAU\b)" + lab + r"\+(\d+)", corpo)
    du = _num(r"(?:CAU|\bDU\b)" + lab + r"(\d+)", corpo)
    return {"au": au, "du": du}


def cella(chat, canone) -> str:
    if chat is None and canone is None:
        return "—"
    if chat is None:
        return f"— / {canone}"
    if canone is None:
        return f"{chat} / —"
    stella = " ★" if chat > canone else ""
    return f"{chat} / {canone}{stella}"


def main(argv: list[str]) -> int:
    chat = sezioni(Path(argv[1]).read_text(encoding="utf-8"))
    canone = sezioni(CANONE.read_text(encoding="utf-8"))
    print("## PNG (chat / canone ARC08-02; ★ = la chat è più forte)\n")
    print("| PNG | " + " | ".join(CAMPI_PNG) + " | ★ |")
    print("|---|" + "---|" * (len(CAMPI_PNG) + 1))
    for nome, can in PNG.items():
        a = misura_png(chat.get(nome, ""))
        c = misura_png(canone[can]) if can else dict.fromkeys(CAMPI_PNG)
        stelle = sum(1 for k in CAMPI_PNG if a[k] is not None and c[k] is not None and a[k] > c[k])
        print(f"| {nome.title()} | " + " | ".join(cella(a[k], c[k]) for k in CAMPI_PNG) + f" | {stelle} |")
    print("\n## Unità (chat / canone; AU e DU sul d20)\n")
    print("| Unità chat | Unità canone | " + " | ".join(CAMPI_UNITA) + " | ★ |")
    print("|---|---|" + "---|" * (len(CAMPI_UNITA) + 1))
    for nome, can in UNITA.items():
        a = misura_unita(chat.get(nome, ""))
        c = misura_unita(canone[can]) if can else dict.fromkeys(CAMPI_UNITA)
        stelle = sum(1 for k in CAMPI_UNITA if a[k] is not None and c[k] is not None and a[k] > c[k])
        print(f"| {nome.title()} | {(can or '—').title()} | " + " | ".join(cella(a[k], c[k]) for k in CAMPI_UNITA) + f" | {stelle} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
