#!/usr/bin/env python3
"""validate_norme_editoriali.py — una norma senza misura deve almeno avere un nome.

🔴 **Il difetto che questo cancello presidia, e che è già successo.**

Il 2026-09-18 si è scoperto che `references/read-aloud-adulti.md` dichiarava da
agosto **box ≤ 12 righe, un solo nome proprio nuovo, niente parentesi**, e che
**nessuno strumento del repo lo guardava**. `ADR-0014` («regia sensoriale
obbligatoria», luglio) era stato applicato a **un documento su cento**: la
chiusura su «Che fate?», prescritta per *ogni* box di combattimento, esisteva
**una volta in tutto il repo**.

Nessuno se n'era accorto perché **una norma non misurata non fa rumore quando
viene ignorata**. E la scopribilità non c'entrava: tutti e 56 i file
`references/` sono citati dal loro `SKILL.md` — un cancello sulla citazione
sarebbe verde e inutile.

## Cosa controlla, quindi

1. **Copertura**: ogni file della superficie normativa sta in
   `skills/REGISTRO-NORME-EDITORIALI.md`. Aggiungerne uno senza registrarlo è
   rosso — è così che una norma torna a nascondersi.
2. **Onestà dei rimandi**: ogni `misura_craft` citato dal registro nomina un
   congegno che **esiste davvero** in `scripts/misura_craft.py`, e ogni script
   citato è un file che esiste. È ADR-0053 applicato al registro stesso: un
   rimando inventato è peggio di un buco dichiarato, perché sembra copertura.
3. **Ragione scritta**: ogni riga 🔴 porta un perché dopo il trattino. Un
   «non misurato» nudo non è una decisione, è una dimenticanza con un'icona.
4. **Severità dichiarata** (lotto F1.1 di `PIANO-MISURA-EDITORIALE-STANDARD`):
   ogni norma dice **quanto costa violarla** — `critico` 25, `maggiore` 5,
   `minore` 1 — oppure porta una ragione scritta per non avere un peso. Senza
   questa colonna il punteggio di ADR-0059 deve indovinare, e una metrica che
   indovina i pesi misura il suo autore.
5. **Accordo con `specifiche-qualita.yaml`**: le norme che hanno un rilevatore
   portano la loro **chiave** accanto alla severità, e la severità nel registro
   deve essere quella nello YAML. È lo stesso disegno di `decisioni_dm --check`
   (ADR-0047): **una casa sola** per il dato, e un cancello che fa rossa la CI
   quando le due copie divergono.
6. **Il conto è derivato, non scritto**: la tabella «il conto onesto» del §4 si
   confronta con le righe vere. 🐛 Scritta a mano, diceva **16+9+12+3 = 40** su
   **39** righe e il testo accanto parlava di *«undici norme su trentaquattro»*
   — tre numeri, tre verità diverse, nessuna esatta. Diciannovesimo caso della
   famiglia «un numero scritto a mano invecchia in silenzio».

⚠️ **Cosa NON controlla**: se le norme siano *rispettate*. Quello lo dicono
`misura_craft`, `validate_modules`, `validate_prosa` — e in dieci casi su
trentuno, oggi, **niente**. Il registro serve a rendere quel dieci **visibile**.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md"

#: La superficie normativa: dove vivono le regole di prosa, stile e linea
#: editoriale. Le altre skill (SRD, lore, mappe) non ci entrano: non dettano
#: norme di scrittura.
SUPERFICIE = (
    "skills/rumblingstone-narrative-style/references",
    "skills/rumblingstone-indagine/references",
)

#: Gli ADR che dettano norme di scrittura e che quindi vanno registrati.
ADR_NORMATIVI = ("ADR-0014",)

_CONGEGNO = re.compile(r"congegno `([^`]+)`")
_SCRIPT = re.compile(r"`(validate_\w+\.py|misura_craft[^`]*)`")
_ROSSO = re.compile(r"^\|.*🔴\s*(?:non misurato)?\s*(.*?)\s*\|\s*$", re.M)

#: Le tre severità di ADR-0059, e i loro pesi. Vivono nello YAML: qui si
#: controlla solo che il registro non ne inventi una quarta.
SEVERITA = ("critico", "maggiore", "minore")
SPECIFICHE = ROOT / "scripts" / "specifiche-qualita.yaml"
#: La riga di una norma: file | norma | severità | stato.
_COLONNE_NORMA = 4


def congegni_veri() -> "set[str]":
    testo = (ROOT / "scripts" / "misura_craft.py").read_text(encoding="utf-8")
    return set(re.findall(r'^\s*\("([^"]+)",\s*$', testo, re.M))


def righe_norma(testo: str) -> "list[list[str]]":
    """Le righe di norma del registro, spezzate in celle.

    Una riga di norma comincia con un file o un ADR fra backtick. Le righe di
    intestazione e i separatori non passano di qui.
    """
    fuori = []
    for riga in testo.splitlines():
        if not riga.startswith("| `"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        fuori.append(celle)
    return fuori


def severita_dello_yaml() -> "dict[str, str]":
    """chiave della norma -> severità, letta da `specifiche-qualita.yaml`.

    Lettura a mano invece che con `yaml`: questo cancello gira in CI, dove
    `pyyaml` non e' garantito (ADR-0037, stdlib-only). Il formato del file e'
    noto e piatto, e un parser di due righe e' onesto quanto una dipendenza in
    piu'. Se il file cambia forma, il test lo dice.
    """
    if not SPECIFICHE.exists():
        return {}
    fuori, chiave, dentro = {}, None, False
    for riga in SPECIFICHE.read_text(encoding="utf-8").splitlines():
        if riga.startswith("norme:"):
            dentro = True
            continue
        if dentro and riga and not riga.startswith((" ", "#")):
            break
        if not dentro or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^  (\w+):\s*$", riga)
        if m:
            chiave = m.group(1)
            continue
        m = re.match(r"^    severita:\s*(\w+)\s*$", riga)
        if m and chiave:
            fuori[chiave] = m.group(1)
    return fuori


def conto_vero(testo: str) -> "dict[str, int]":
    """Quante norme per stato, contate sulle righe e non sulle emoji.

    🐛 Il conto stampato in fondo contava le **occorrenze delle emoji in tutto
    il file**, prosa compresa: dava 47 dove le norme sono 39.
    """
    conto = {"🟢": 0, "🟡": 0, "🔴": 0, "⚪": 0}
    for celle in righe_norma(testo):
        stato = celle[-1]
        for e in conto:
            if stato.startswith(e) or f" {e}" in stato[:4]:
                conto[e] += 1
                break
    return conto


def controlla() -> "list[str]":
    errori: "list[str]" = []
    if not REGISTRO.exists():
        return [f"manca {REGISTRO.relative_to(ROOT)}"]
    testo = REGISTRO.read_text(encoding="utf-8")

    # 1 · copertura: ogni file normativo è nominato
    for cartella in SUPERFICIE:
        d = ROOT / cartella
        if not d.is_dir():
            errori.append(f"superficie dichiarata inesistente: {cartella}")
            continue
        for f in sorted(d.glob("*.md")):
            if f.name not in testo:
                errori.append(
                    f"norma non registrata: {cartella}/{f.name} — aggiungila a "
                    "REGISTRO-NORME-EDITORIALI.md con la sua norma e chi la misura")
    for adr in ADR_NORMATIVI:
        if adr not in testo:
            errori.append(f"ADR normativo non registrato: {adr}")

    # 2 · onestà: i rimandi nominano cose che esistono
    #
    # ⚠️ Solo sulle righe che AFFERMANO una misura. Una riga 🔴 può nominare
    # uno script inesistente **apposta**: è successo alla prima stesura, dove
    # la riga di ADR-0022 cita `validate_pg.py` per dire che non esiste. Un
    # cancello che bocciasse anche quello impedirebbe di scrivere il vero.
    veri = congegni_veri()
    for riga in testo.splitlines():
        if not riga.startswith("|") or "🔴" in riga:
            continue
        for nome in set(_CONGEGNO.findall(riga)):
            if nome not in veri:
                errori.append(
                    f"il registro cita il congegno «{nome}», che non esiste in "
                    "misura_craft.py — un rimando inventato sembra copertura (ADR-0053)")
        for s in set(_SCRIPT.findall(riga)):
            base = s.split()[0].split("--")[0].strip()
            if base and not base.endswith(".py"):
                base += ".py"          # il registro cita «misura_craft --box»
            if base and not (ROOT / "scripts" / base).exists():
                errori.append(f"il registro cita lo script «{base}», che non esiste")

    # 3 · ogni 🔴 porta il suo perché
    for i, riga in enumerate(testo.splitlines(), 1):
        if "🔴" not in riga or not riga.startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        stato = celle[-1]
        if "🔴" in stato and "—" not in stato:
            errori.append(
                f"r.{i}: «non misurato» senza una ragione dopo il trattino — "
                "una riga nuda non è una decisione")

    # 4 · ogni norma dichiara quanto costa violarla (F1.1)
    righe = righe_norma(testo)
    for celle in righe:
        if len(celle) != _COLONNE_NORMA:
            errori.append(
                f"«{celle[1][:50]}»: la riga ha {len(celle)} colonne invece di "
                f"{_COLONNE_NORMA} — manca la severità (F1.1)")
            continue
        sev = celle[2]
        if not any(s in sev for s in SEVERITA):
            if not sev.startswith("—") or len(sev) < 4:
                errori.append(
                    f"«{celle[1][:50]}»: severità assente o inventata — "
                    "dev'essere critico / maggiore / minore, oppure «— » con la "
                    "ragione per cui la norma non si pesa")

    # 5 · registro e specifiche non divergono (lo stesso disegno di ADR-0047)
    yaml_sev = severita_dello_yaml()
    viste = set()
    for celle in righe:
        if len(celle) != _COLONNE_NORMA:
            continue
        m = re.search(r"`(\w+)`", celle[2])
        if not m:
            continue
        chiave = m.group(1)
        viste.add(chiave)
        if chiave not in yaml_sev:
            errori.append(
                f"il registro dichiara la chiave «{chiave}», che "
                "specifiche-qualita.yaml non conosce — un rimando inventato "
                "sembra copertura (ADR-0053)")
        elif yaml_sev[chiave] not in celle[2]:
            errori.append(
                f"«{chiave}»: il registro dice «{celle[2]}», lo YAML dice "
                f"«{yaml_sev[chiave]}» — il dato ha una casa sola (ADR-0047)")
    for chiave in sorted(set(yaml_sev) - viste):
        errori.append(
            f"«{chiave}» pesa nel punteggio ma nessuna riga del registro la "
            "rivendica: una norma che conta senza essere registrata e' il "
            "difetto che ADR-0056 presidia, al contrario")

    # 6 · il conto del §4 e' quello vero
    conto = conto_vero(testo)
    for emoji, atteso in re.findall(r"^\|\s*(🟢|🟡|🔴|⚪)[^|]*\|\s*(\d+)\s*\|$",
                                    testo, re.M):
        if conto[emoji] != int(atteso):
            errori.append(
                f"«il conto onesto» dice {atteso} righe {emoji}, e sono "
                f"{conto[emoji]} — il conto si deriva, non si ricorda")
    return errori


def main() -> int:
    errori = controlla()
    for e in errori:
        print(f"  ✗ {e}")
    if errori:
        print(f"✗ validate_norme_editoriali: {len(errori)} problema/i")
        return 1
    testo = REGISTRO.read_text(encoding="utf-8")
    conto = conto_vero(testo)
    n = sum(conto.values())
    pesate = len(severita_dello_yaml())
    print(f"✓ validate_norme_editoriali: {n} norme registrate "
          f"({conto['🟢']} 🟢 · {conto['🟡']} 🟡 · {conto['🔴']} 🔴 · "
          f"{conto['⚪']} ⚪), ogni rimando esiste, ogni buco ha una ragione, "
          f"ogni norma una severità — {pesate} entrano nel punteggio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
