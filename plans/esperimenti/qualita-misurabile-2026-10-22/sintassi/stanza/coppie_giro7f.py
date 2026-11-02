"""Le 16 coppie decise del voto cieco del lotto 7f (riscrittura/), nello
stesso formato di COPPIE-VOTATE.json: con le 38 di prima fanno 54 coppie
(la 55ª, B04, è pari e resta fuori come le altre «=»).

    python3 plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/stanza/coppie_giro7f.py > COPPIE-7F.json
"""
import json
import re
import sys
from pathlib import Path

QM = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(QM.parents[2] / "scripts"))
import misura_craft as mc  # noqa: E402

R = QM / "riscrittura"


def versioni() -> dict:
    """{'B01': {'O': testo, 'V1': testo, ...}} dal file BOX.md."""
    out, box, ver, righe = {}, None, None, []

    def chiudi():
        if box and ver and righe:
            out.setdefault(box, {})[ver] = mc.corpo_del_box([r for r in righe if r.startswith(">")])

    for r in (R / "versioni" / "BOX.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (B\d\d) ", r)
        v = re.match(r"^### (\w+)", r)
        if m or v:
            chiudi()
            righe = []
            if m:
                box, ver = m.group(1), None
            else:
                ver = v.group(1)
            continue
        righe.append(r)
    chiudi()
    return out


def ultima(vs: dict, arm: str) -> str:
    it = sorted(k for k in vs if re.fullmatch(arm + r"\d", k))
    return vs[it[-1]] if it else vs["O"]


def voti(nome: str) -> dict:
    out = {}
    for r in (R / "cieco" / nome).read_text(encoding="utf-8").splitlines():
        p = r.split()
        if len(p) >= 2:
            out[int(p[0])] = p[1]
    return out


def main():
    vs = versioni()
    righe = []
    for parte, chiave, voto, nuovo, vecchio in (
            ("7f-VN", "CHIAVE-V-N.json", "VOTI-1.txt", "N", "V"),
            ("7f-FO", "CHIAVE-F-O.json", "VOTI-2.txt", "F", "O")):
        k = json.loads((R / "chiave" / chiave).read_text(encoding="utf-8"))
        vt = voti(voto)
        for c in k["coppie"]:
            v = vt.get(c["n"])
            if v not in ("A", "B"):
                continue
            b = c["titolo"].split()[-1]
            t_nuovo = vs[b]["F"] if nuovo == "F" else ultima(vs[b], nuovo)
            t_vecchio = vs[b]["O"] if vecchio == "O" else ultima(vs[b], vecchio)
            nuova_vince = v == c["nuova"]
            win, lose = (t_nuovo, t_vecchio) if nuova_vince else (t_vecchio, t_nuovo)
            righe.append({"set": parte, "n": c["n"], "box": b, "vinta": v,
                          "perdente": "B" if v == "A" else "A",
                          "win": win, "lose": lose, "nuova_vince": nuova_vince})
    print(json.dumps(righe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
