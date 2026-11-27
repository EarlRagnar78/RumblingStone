"""Abbina le righe delle tabelle italiane del tesoro (GDM 3.5) alle tabelle dell'SRD inglese.

Fonte italiana: la scheda «Tesoro e oggetti magici» di Mindbender (PDF amatoriale con le
tabelle del GDM italiano e il numero di pagina). Non usa i nomi: una riga si abbina se
tabella, intervalli di d% e prezzo sono uguali, e la chiave è unica nelle due tabelle.

Uso: python3 -I abbina_tesoro.py <tesoro.txt> > coppie.json
"""
import json, re, sys, html
from pathlib import Path
from collections import defaultdict

SRD = next((Path.home() / ".cache/rumblingstone/srd").glob("srd-v3.5-md-*")) / "magic-items"

TABELLE = {  # titolo italiano (inizio) -> didascalia SRD
    "CAPACITÀ SPECIALI DELLE ARMATURE": "Armor Special Abilities",
    "CAPACITÀ SPECIALI DEGLI SCUDI": "Shield Special Abilities",
    "CAPACITÀ SPECIALI DELLE ARMI DA MISCHIA": "Melee Weapon Special Abilities",
    "CAPACITÀ SPECIALI DELLE ARMI A DISTANZA": "Ranged Weapon Special Abilities",
    "POZIONI E OLI": "Potions and Oils",
    "ANELLI": "Rings", "VERGHE": "Rods", "BASTONI": "Staffs", "BACCHETTE": "Wands",
    "PERGAMENE DEGLI INCANTESIMI ARCANI": "Arcane Spell Scrolls",
    "PERGAMENE DEGLI INCANTESIMI DIVINI": "Divine Spell Scrolls",
    "OGGETTI MERAVIGLIOSI MINORI (GDM PAG 247)": "Minor Wondrous Items",
    "OGGETTI MERAVIGLIOSI MEDI": "Medium Wondrous Items",
    "OGGETTI MERAVIGLIOSI MINORI (GDM PAG 251)": "Major Wondrous Items",
}
DADO = r"(?:\d{2,3}[–-]\d{2,3}|\d{2,3}|—)"
PREZZO = r"(\+\d+ bonus|[\d.,]+ m[op])"


def prezzo(s):
    s = s.strip().lower()
    m = re.match(r"\+(\d+) bonus", s)
    if m:
        return "+" + m.group(1)
    m = re.match(r"\+([\d.,]+)\s*gp", s)
    if m:
        return re.sub(r"[.,]", "", m.group(1))
    m = re.match(r"\+(\d+) bonus", s)
    if m:
        return "+" + m.group(1)
    m = re.match(r"([\d.,]+)\s*(?:gp|mo|mp)", s)
    if m:
        return re.sub(r"[.,]", "", m.group(1))
    return s


def dadi(celle):
    return tuple("—" if c in ("-", "—") else (c.replace("-", "–").lstrip("0") or "0") for c in celle)


CAPACITA = re.compile(r"^\s*((?:(?:\d{2,3}(?:[–-]\d{2,3})?|-)\s+){2,3})(\S.*?\S)\s{2,}.*?"
                      r"(Bonus \+\d|\+[\d.]+ mo)\S*\s+\d+[sd]")


def prezzo_capacita(s):
    m = re.match(r"Bonus \+(\d)", s)
    return "+" + m.group(1) if m else prezzo(s.lstrip("+"))


def srd_tabelle():
    out = {}
    for f in sorted(SRD.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"<caption>Table: ([^<]+)</caption>(.*?)</table>", t, re.S):
            righe = []
            for tr in re.findall(r"<tr>(.*?)</tr>", m.group(2), re.S):
                celle = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
                n = 0
                while n < len(celle) and re.fullmatch(DADO, celle[n]):
                    n += 1
                if len(celle) >= 3 and 0 < n < len(celle) - 1:
                    righe.append((dadi(celle[:n]), celle[n], prezzo(celle[-1])))
            out.setdefault(m.group(1).strip(), []).extend(righe)
    return out


def it_tabelle(testo):
    out, cur = defaultdict(list), None
    riga_re = re.compile(rf"((?:{DADO}\s+)+)(\S.*?\S)\s+{PREZZO}(?:\s+\d+[sd])?")
    for linea in testo.splitlines():
        if "TABELLA" in linea:
            cur = None
            for k, v in TABELLE.items():
                if k in linea:
                    cur = v
            continue
        if cur and "Special Abilities" in cur:
            m = CAPACITA.match(linea)
            if m:
                nome = re.sub(r"\d*P(\s+P)*$", "", m.group(2)).strip()
                out[cur].append((dadi(m.group(1).split()), nome, prezzo_capacita(m.group(3))))
        elif cur:
            for m in riga_re.finditer(linea):
                out[cur].append((dadi(m.group(1).split()), m.group(2).strip(), prezzo(m.group(3))))
    return out


def main():
    it = it_tabelle(Path(sys.argv[1]).read_text(encoding="utf-8"))
    en = srd_tabelle()
    coppie, dubbi, senza = [], [], []
    for tab, righe in it.items():
        ke = defaultdict(list)
        for d, n, p in en.get(tab, []):
            ke[(d, p)].append(n)
        ki = defaultdict(list)
        for d, n, p in righe:
            ki[(d, p)].append(n)
        for k, nomi in ki.items():
            if len(nomi) == 1 and len(ke.get(k, [])) == 1:
                coppie.append({"tabella": tab, "it": nomi[0], "en": ke[k][0]})
            elif k in ke:
                dubbi.append({"tabella": tab, "it": nomi, "en": ke[k]})
            else:
                senza.append({"tabella": tab, "it": nomi})
        print(tab, "it", len(righe), "en", len(en.get(tab, [])), file=sys.stderr)
    print("coppie", len(coppie), "dubbi", len(dubbi), "senza", len(senza), file=sys.stderr)
    json.dump({"coppie": coppie, "dubbi": dubbi, "senza": senza}, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
