#!/usr/bin/env python3
"""
azzera_partita.py — azzera la PARTITA per un gruppo nuovo, e il prodotto resta.

Lo chiamano `scripts/gruppo_nuovo.py` (`dm.py gruppo nuovo`, con lo stato
derivato dalle risposte del DM) e `scripts/new-campaign-group.sh` (col template
vuoto), sul branch del gruppo nuovo. L'elenco
di cosa e' partita non sta qui: sta in `dmcore/partita.py`, che e' anche quello
che `test_new_group.py` confronta con i file scritti dagli script (ADR-0050 §7,
lotto 4f).

Cosa fa, nell'ordine:
  1. `state.yaml` dal template, con l'anagrafica `png` del gruppo di prima
     (e' prodotto: le chiavi verso il Bestiario);
  2. `state.md` e `state-changelog.md` dai loro template;
  3. svuota sessioni, recap, brief; toglie i file generati dallo stato vecchio;
  4. rigenera le tabelle di `state.md` dal nuovo `state.yaml`;
  5. **valida prima di dichiararsi finito**: `validate_state` senza errori e
     `state.md` gia' allineato, cioe' la CI del gruppo nuovo e' verde.

Uso:
    python3 scripts/azzera_partita.py            # esegue
    python3 scripts/azzera_partita.py --check    # dice cosa farebbe, non scrive

Non fa niente con git: il branch e il commit sono di chi lo chiama.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore.partita import PARTITA, PENDENTI  # noqa: E402


class ResetError(RuntimeError):
    """Il gruppo nuovo non sarebbe coerente: il reset si ferma e lo dice."""


def _yaml():
    try:
        import yaml
    except ImportError:  # pragma: no cover - dipendenza dichiarata in ADR-0037
        raise ResetError("serve pyyaml (ADR-0037): pip install pyyaml") from None
    return yaml


def stato_nuovo(template: str, vecchio: "str | None") -> str:
    """Il testo del nuovo `state.yaml`: il template, piu' `png` del gruppo di prima."""
    yaml = _yaml()
    png = (yaml.safe_load(vecchio) or {}).get("png") if vecchio else None
    if not png:
        raise ResetError("lo state.yaml di prima non ha l'anagrafica `png`: "
                         "e' prodotto, e senza il gruppo nuovo perde le chiavi "
                         "verso il Bestiario")
    corpo = yaml.safe_dump({"png": png}, allow_unicode=True, sort_keys=False,
                           default_flow_style=False)
    return template.rstrip("\n") + "\n\n" + corpo


def piano(radice: Path) -> "list[tuple[str, Path]]":
    """(azione, file) per ogni file che il reset tocca, senza toccarne nessuno."""
    out: list[tuple[str, Path]] = []
    for v in PARTITA:
        if v.azione == "svuota":
            out += [("svuota", p) for p in sorted(radice.glob(v.percorso))]
        elif v.azione == "rimuovi":
            if (radice / v.percorso).exists():
                out.append(("rimuovi", radice / v.percorso))
        else:
            out.append((v.azione, radice / v.percorso))
    return out


def azzera(radice: Path, testo_stato: "str | None" = None) -> "list[str]":
    """Esegue il reset sotto `radice` e ritorna il resoconto; `ResetError` se no.

    `testo_stato` e' lo `state.yaml` gia' pronto del gruppo nuovo, quando lo
    costruisce `gruppo_nuovo.py` dalle risposte del DM (lotto 4f-4). Senza, si
    parte dal template vuoto piu' l'anagrafica `png`, come prima. In entrambi i
    casi si valida PRIMA di scrivere.
    """
    yaml = _yaml()
    import render_state
    import validate_state

    resoconto: list[str] = []
    for v in PARTITA:
        if v.azione in ("stato", "template") and not (radice / v.sorgente).exists():
            raise ResetError(f"template mancante: {v.sorgente}")

    # 🔴 Prima si costruisce e si valida il nuovo stato, POI si scrive. Un reset
    # che scopre un errore a meta' lascerebbe il branch del gruppo nuovo con
    # mezza partita vecchia e mezza nuova, che e' peggio di non averlo fatto.
    (voce_stato,) = [v for v in PARTITA if v.azione == "stato"]
    dest_stato = radice / voce_stato.percorso
    if testo_stato is None:
        testo_stato = stato_nuovo(
            (radice / voce_stato.sorgente).read_text(encoding="utf-8"),
            dest_stato.read_text(encoding="utf-8") if dest_stato.exists() else None)
    dati = yaml.safe_load(testo_stato)
    errori = validate_state.errori(dati, radice)
    if errori:
        raise ResetError("il nuovo state.yaml non passerebbe validate_state, "
                         "e non si e' scritto niente:\n  · " + "\n  · ".join(errori))

    for v in PARTITA:
        dest = radice / v.percorso
        if v.azione == "stato":
            dest.write_text(testo_stato, encoding="utf-8")
            resoconto.append(f"azzerato  {v.percorso}  ({v.nota})")
        elif v.azione == "template":
            testo = (radice / v.sorgente).read_text(encoding="utf-8")
            # La prima data segnaposto e' «quando e' partito il gruppo»: oggi.
            dest.write_text(testo.replace("YYYY-MM-DD", date.today().isoformat(), 1),
                            encoding="utf-8")
            resoconto.append(f"azzerato  {v.percorso}")
        elif v.azione == "svuota":
            tolti = sorted(radice.glob(v.percorso))
            for p in tolti:
                p.unlink()
            if tolti:
                resoconto.append(f"svuotato  {v.percorso}  ({len(tolti)} file)")
        elif v.azione == "rimuovi":
            if dest.exists():
                dest.unlink()
                resoconto.append(f"rimosso   {v.percorso}  ({v.nota})")
        else:  # pragma: no cover - l'elenco e' un dato: un'azione ignota e' un refuso
            raise ResetError(f"azione sconosciuta «{v.azione}» per {v.percorso}")

    sessions = radice / "campaign" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / ".gitkeep").touch()

    md_path = radice / "campaign" / "state.md"
    md, mancanti = render_state.apply_regions(md_path.read_text(encoding="utf-8"), dati)
    if mancanti:
        raise ResetError("il template di state.md non ha le regioni: "
                         + ", ".join(mancanti))
    md_path.write_text(md, encoding="utf-8")

    if render_state.apply_regions(md, dati)[0] != md:  # pragma: no cover
        raise ResetError("state.md non e' allineato dopo la rigenerazione")
    resoconto.append("verificati validate_state (prima di scrivere) e "
                     "render_state --check (dopo): verdi")
    return resoconto


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Azzera la partita per un gruppo nuovo (ADR-0050 §7).")
    ap.add_argument("--check", action="store_true",
                    help="elenca cosa verrebbe azzerato, senza scrivere")
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    radice = args.repo_root.resolve()

    if args.check:
        for azione, p in piano(radice):
            print(f"[partita] {azione:9s} {p.relative_to(radice)}")
    else:
        try:
            for riga in azzera(radice):
                print(f"[partita] ✓ {riga}")
        except ResetError as exc:
            print(f"[partita] ✗ {exc}", file=sys.stderr)
            return 1
    for percorso, perche in PENDENTI.items():
        # In vista a ogni esecuzione: una falla nota non si dimentica.
        print(f"[partita] ⚠ {percorso} NON si azzera ancora: {perche}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
