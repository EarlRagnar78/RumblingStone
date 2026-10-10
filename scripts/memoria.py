#!/usr/bin/env python3
"""memoria.py — la memoria del lavoro in un posto solo, generata dal repo.

Il DM, il 2026-10-10: *«creare un progetto così tutta la memoria si raccoglie
in un posto e il lavoro si aggiorna senza perdere parti o decisioni»*. Scelta
del DM: nel repo, generata (ADR-0087).

Le sessioni d'agente sono effimere: lo scratchpad si perde, la chat si
riassume. Quello che resta è git. Questo script non scrive niente di nuovo:
**legge** le fonti che il repo ha già, ognuna con la sua casa, e le mette in
fila in `MEMORIA.md`, nella radice:

* le decisioni aperte al DM, da `decisioni_dm` (le tabelle nei piani);
* la lista viva di `STATO-E-ORDINE-DEI-PIANI.md` §0, per stato (▶ 🙋 ⬜ 🟡);
* i documenti di revisione ancora da approvare (`plans/scrittura/**`), quelli
  che `ciclo_prosa.py applica` può ancora applicare;
* le ultime righe del `CHANGELOG`;
* il registro dei miglioramenti della prosa.

Nessuna data di generazione e nessuna rete: lo stesso repo dà lo stesso file,
byte per byte, ed è il presupposto del `--check` in CI. Se un piano cambia e
`MEMORIA.md` no, la CI è rossa: la memoria non può restare indietro.

    python3 scripts/memoria.py           # rigenera MEMORIA.md
    python3 scripts/memoria.py --check   # il cancello: esce 1 se è indietro

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / "scripts"))

import ciclo_prosa as cp  # noqa: E402
import decisioni_dm as dd  # noqa: E402

USCITA = RADICE / "MEMORIA.md"
STATO = RADICE / "plans" / "STATO-E-ORDINE-DEI-PIANI.md"
CHANGELOG = RADICE / "plans" / "CHANGELOG.md"
ULTIME = 12          # righe del CHANGELOG mostrate
TAGLIO = 220         # caratteri di una cella, oltre si taglia

#: L'ordine in cui si legge la lista viva: prima cosa si fa, poi cosa aspetta.
STATI = (("▶", "In corso: da qui si riparte"),
         ("🙋", "Aspetta il DM"),
         ("⬜", "Da fare, nell'ordine dei piani"),
         ("🟡", "Fatto a metà"))


_LINK = re.compile(r"\]\((?!https?:|#|/)([^)\s]+)\)")


def _dalla_radice(s: str, base: str = "plans") -> str:
    """I link relativi di un testo preso da `plans/`, riscritti dalla radice."""
    import posixpath
    return _LINK.sub(lambda m: "](" + posixpath.normpath(posixpath.join(base, m.group(1))) + ")", s)


def _corto(s: str, n: int = TAGLIO) -> str:
    s = _dalla_radice(" ".join(s.split())).replace("|", "\\|")
    if len(s) <= n:
        return s
    s = s[:n - 1]
    if s.rfind("[") > s.rfind(")"):        # non si taglia un link a metà
        s = s[:s.rfind("[")]
    if s.count("`") % 2:                   # né il codice in linea
        s = s[:s.rfind("`")]
    return s.rstrip() + "…"


def _celle(riga: str) -> "list[str]":
    """Le celle di una riga di tabella, senza spezzare dentro il codice in linea."""
    corpo = riga.strip().strip("|")
    celle, cur, codice = [], "", False
    for i, ch in enumerate(corpo):
        if ch == "`":
            codice = not codice
        if ch == "|" and not codice and (i == 0 or corpo[i - 1] != "\\"):
            celle.append(cur.strip())
            cur = ""
        else:
            cur += ch
    celle.append(cur.strip())
    return celle


def lista_viva(testo: str) -> "dict[str, list[list[str]]]":
    """Le righe di STATO §0 che non sono ✅, raggruppate per stato."""
    i = testo.index("## 0 ·")
    j = testo.index("\n## ", i + 5)
    righe = {s: [] for s, _ in STATI}
    for r in testo[i:j].splitlines():
        if not r.startswith("| "):
            continue
        c = _celle(r)
        if c and c[0] in righe:
            righe[c[0]].append(c[1:])
    return righe


def revisioni_in_attesa() -> "list[tuple[str, str, int, int]]":
    """(documento, originale, modifiche, già spuntate) delle revisioni ancora applicabili.

    Una revisione è in attesa se il testo «prima» che porta è ancora quello
    dell'originale: `applica` la può applicare. Se l'originale è cambiato è
    stata applicata, o è superata: allora non aspetta più nessuno (e se serve
    ancora, `ciclo_prosa.py rigenera` la riporta sul testo di oggi).
    """
    fuori = []
    for rev in sorted((RADICE / "plans" / "scrittura").rglob("REVISIONE-*.md")):
        t = rev.read_text(encoding="utf-8")
        m = cp._TESTA.search(t)
        if not m:
            continue
        orig = cp._assoluto(m.group("o"))
        if not orig.exists():
            continue
        prima, _ = cp.dal_markup(cp._marcato_del_documento(t))
        if prima != orig.read_text(encoding="utf-8"):
            continue
        righe = [r for r in t.splitlines() if cp._SPUNTA.match(r)]
        fuori.append((cp._rel(rev), m.group("o"), len(righe), len(cp.accettate(t))))
    return fuori


def ultime_del_changelog(testo: str, n: int = ULTIME) -> "list[list[str]]":
    righe = [r for r in testo.splitlines() if re.match(r"^\| \d{4}-\d{2}-\d{2}", r)]
    righe.sort(key=lambda r: _celle(r)[0])          # in ordine di data, stabile
    return [_celle(r) for r in righe[-n:]][::-1]


def registro_prosa() -> "tuple[int, int, float] | None":
    if not cp.REGISTRO.exists():
        return None
    voci = json.loads(cp.REGISTRO.read_text(encoding="utf-8"))
    ds = sum(v["segnalazioni"][1] - v["segnalazioni"][0] for v in voci)
    dq = sum(v["mqm"][1] - v["mqm"][0] for v in voci if v.get("mqm"))
    return len(voci), ds, round(dq, 2)


def rendi() -> str:
    decisioni, _ = dd.leggi_fonti(RADICE)
    aperte = [d for d in decisioni if d.aperta]
    stato = STATO.read_text(encoding="utf-8")
    viva = lista_viva(stato)
    revisioni = revisioni_in_attesa()

    r = ["# 🧠 MEMORIA — il lavoro su RumblingStone in un posto solo", "",
         "> **Generata da `scripts/memoria.py`: non si scrive a mano** "
         "([ADR-0087](plans/adr/ADR-0087-la-memoria-del-lavoro-e-generata.md)). "
         "Ogni riga viene da una fonte che ha la sua casa, e il link porta lì: si corregge "
         "la fonte, poi `python3 scripts/memoria.py`. La CI boccia questo file se resta "
         "indietro.", "",
         "## Come si riparte, in una sessione nuova", "",
         "```bash",
         "git fetch --prune origin",
         "python3 scripts/memoria.py --check      # questa pagina è allineata?",
         "python3 scripts/decisioni_dm.py --check # le decisioni aperte",
         "python3 scripts/fase1.py <file>         # sempre, prima di toccare",
         "```", "",
         "Poi si legge questa pagina dall'alto: prima cosa aspetta il DM, poi da dove "
         "riparte l'agente. Le regole di lavoro stanno in [`AGENTS.md`](AGENTS.md).", "",
         f"## Aspetta il DM: {len(aperte)} decisioni aperte", "",
         "Fonte: le tabelle `decisioni-dm` dei piani, aggregate in "
         "[STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col "
         "numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.", "",
         "| Piano | # | Ambito | Domanda |", "|---|---|---|---|"]
    for d in aperte:
        r.append(f"| `{d.piano}` | {d.ident} | {_corto(d.ambito, 40)} | {_corto(d.testo)} |")

    r += ["", f"### Revisioni della prosa da approvare: {len(revisioni)}", "",
          "Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py "
          "applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi "
          "interi.", ""]
    if revisioni:
        r += ["| Documento | Originale | Modifiche | Spuntate |", "|---|---|---:|---:|"]
        for doc, orig, n, ok in revisioni:
            r.append(f"| [`{Path(doc).name}`]({doc}) | `{orig}` | {n} | {ok} |")
    else:
        r.append("Nessuna.")

    for simbolo, titolo in STATI:
        righe = viva[simbolo]
        r += ["", f"## {simbolo} {titolo}: {len(righe)}", "",
              "Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.", ""]
        if not righe:
            r.append("Nessuna.")
            continue
        r += ["| Cosa | Dove sta il dettaglio | Da dove si parte |", "|---|---|---|"]
        for c in righe:
            cosa = c[0] if c else ""
            dove = c[2] if len(c) > 2 else ""
            parte = c[3] if len(c) > 3 else ""
            r.append(f"| {_corto(cosa)} | {_corto(dove, 120)} | {_corto(parte, 160)} |")

    r += ["", f"## Fatto di recente: le ultime {ULTIME} righe del CHANGELOG", "",
          "Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.", "",
          "| Data | Piano | Lotto | Esito |", "|---|---|---|---|"]
    for c in ultime_del_changelog(CHANGELOG.read_text(encoding="utf-8")):
        esito = c[4] if len(c) > 4 else ""
        r.append(f"| {c[0]} | {_corto(c[1], 40)} | {_corto(c[2], 80)} | {_corto(esito, 160)} |")

    reg = registro_prosa()
    r += ["", "## Le misure che si portano dietro", ""]
    r.append(f"- **Decisioni**: {len(aperte)} aperte, {len(decisioni) - len(aperte)} chiuse "
             f"(`decisioni_dm.py`).")
    if reg:
        r.append(f"- **Prosa**: {reg[0]} revisioni applicate, segnalazioni {reg[1]:+d}, "
                 f"MQM {reg[2]:+.2f} punti (`ciclo_prosa.py registro`).")
    r += ["", "## Dove vive ogni cosa", "",
          "| Cosa | Casa unica |", "|---|---|",
          "| Lo stato del mondo di gioco | [`campaign/state.md`](campaign/state.md), "
          "e il canone si scrive sul ramo del gruppo (ADR-0007) |",
          "| Cosa si fa e in che ordine | [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md) |",
          "| Le decisioni del DM | le tabelle `decisioni-dm` dentro ogni piano (ADR-0047) |",
          "| Cosa è successo | [`plans/CHANGELOG.md`](plans/CHANGELOG.md) |",
          "| Che piani esistono | [`plans/INDEX.md`](plans/INDEX.md) |",
          "| Perché si è deciso così | [`plans/adr/`](plans/adr/) |",
          "| Le norme e chi le misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) |",
          "| Le regole per gli agenti | [`AGENTS.md`](AGENTS.md) |",
          "| Questa pagina | `scripts/memoria.py`, mai a mano |", ""]
    return "\n".join(r)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="il cancello: esce 1 se MEMORIA.md non è quella che il repo genera")
    a = ap.parse_args(argv)
    nuovo = rendi()
    if a.check:
        vecchio = USCITA.read_text(encoding="utf-8") if USCITA.exists() else ""
        if vecchio != nuovo:
            print("✗ memoria: MEMORIA.md è indietro rispetto al repo. "
                  "`python3 scripts/memoria.py` e committala.")
            return 1
        print("✓ memoria: MEMORIA.md allineata al repo")
        return 0
    USCITA.write_text(nuovo, encoding="utf-8")
    print(f"✓ scritta {USCITA.relative_to(RADICE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
