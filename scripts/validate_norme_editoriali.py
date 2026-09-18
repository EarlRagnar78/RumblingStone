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


def congegni_veri() -> "set[str]":
    testo = (ROOT / "scripts" / "misura_craft.py").read_text(encoding="utf-8")
    return set(re.findall(r'^\s*\("([^"]+)",\s*$', testo, re.M))


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
    return errori


def main() -> int:
    errori = controlla()
    for e in errori:
        print(f"  ✗ {e}")
    if errori:
        print(f"✗ validate_norme_editoriali: {len(errori)} problema/i")
        return 1
    testo = REGISTRO.read_text(encoding="utf-8")
    n = sum(testo.count(x) for x in ("🟢", "🟡", "🔴", "⚪"))
    print(f"✓ validate_norme_editoriali: {n} norme registrate, "
          f"ogni rimando esiste, ogni buco ha una ragione scritta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
