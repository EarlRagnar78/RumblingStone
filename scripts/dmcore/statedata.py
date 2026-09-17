"""Scrivere UN campo in `campaign/state.yaml` senza riscrivere il file.

`yaml.safe_dump` rigenererebbe tutte e 502 le righe — commenti di testa
compresi, che qui non sono decorazione ma la spiegazione di ADR-0050 — per
cambiare tre caratteri. Un diff di 502 righe per un clock che passa da 9/18 a
10/18 e' un diff che nessuno rilegge, ed e' esattamente dove il canone si perde.

Quindi: si modifica **la riga**, e poi si **verifica contro il parser** che sia
cambiato esattamente quel campo e nient'altro. La modifica testuale e' veloce e
ingenua; la verifica e' totale e non ingenua. Se la seconda non conferma la
prima, non si scrive niente.

⚠️ pyyaml e' un debito dichiarato (ADR-0037): questo modulo lo importa, i suoi
chiamanti lo importano tardi, e il resto della catena resta stdlib.
"""
from __future__ import annotations

import copy

try:
    import yaml
except ImportError:  # pragma: no cover - dipendenza dichiarata in ADR-0037
    yaml = None  # type: ignore[assignment]


class StateDataError(RuntimeError):
    """La modifica non e' verificabile: non si scrive."""


def _serve_yaml() -> None:
    if yaml is None:  # pragma: no cover
        raise StateDataError("serve pyyaml per scrivere campaign/state.yaml "
                             "(pip install pyyaml)")


def _riga_del_campo_oggetto(testo: str, sezione: str,
                            campo: str) -> "tuple[int, str] | None":
    """Come `_riga_del_campo`, per una sezione che e' un OGGETTO e non una lista.

    `march_clock` (§2.1) ha questa forma: chiavi a rientro di due spazi sotto la
    chiave di primo livello, senza trattini.
    """
    righe = testo.splitlines(keepends=True)
    inizio = next((n for n, r in enumerate(righe)
                   if r.startswith(f"{sezione}:")), None)
    if inizio is None:
        return None
    for n in range(inizio + 1, len(righe)):
        r = righe[n]
        if r.strip() and not r[0].isspace():
            break  # un'altra chiave di primo livello
        if r.startswith("  ") and not r[2:3].isspace() and r[2:].startswith(f"{campo}:"):
            return n, "  "
    return None


def imposta_campo_oggetto(testo: str, sezione: str, campo: str, valore) -> str:
    """Un campo di una sezione-oggetto, con la stessa verifica di `imposta_campo`."""
    _serve_yaml()
    prima = yaml.safe_load(testo)
    if not isinstance(prima, dict) or not isinstance(prima.get(sezione), dict):
        raise StateDataError(f"sezione '{sezione}' assente o non e' un oggetto")
    trovata = _riga_del_campo_oggetto(testo, sezione, campo)
    if trovata is None:
        raise StateDataError(f"campo '{campo}' di {sezione} non trovato su una "
                             "riga propria: modifica a mano")
    return _riscrivi(testo, prima, trovata, campo, valore,
                     lambda d: d[sezione].__setitem__(campo, valore),
                     f"{sezione}.{campo}")


def _riscrivi(testo: str, prima, trovata, campo: str, valore, applica,
              etichetta: str) -> str:
    """La riga si riscrive col parser, e il risultato si verifica col parser.

    🔴 La verifica e' il punto del modulo. Senza, questa e' una sed.
    """
    n, prefisso = trovata
    reso = yaml.safe_dump({campo: valore}, default_flow_style=False,
                          allow_unicode=True, sort_keys=False).rstrip("\n")
    if "\n" in reso:
        raise StateDataError(f"il valore di '{campo}' si serializza su piu' "
                             "righe: modifica a mano")
    righe = testo.splitlines(keepends=True)
    fine = "\n" if righe[n].endswith("\n") else ""
    righe[n] = prefisso + reso + fine
    nuovo = "".join(righe)
    try:
        dopo = yaml.safe_load(nuovo)
    except yaml.YAMLError as exc:
        raise StateDataError(f"il risultato non e' YAML valido: {exc}") from exc
    atteso = copy.deepcopy(prima)
    applica(atteso)
    if dopo != atteso:
        raise StateDataError(
            f"la modifica di {etichetta} ha toccato altro: non si scrive "
            "(confronto contro il parser)")
    return nuovo


def _riga_del_campo(testo: str, sezione: str, indice: int,
                    campo: str) -> "tuple[int, str] | None":
    """(numero di riga, prefisso) del campo, cercando per struttura del blocco.

    Il file e' in stile blocco con rientro di due spazi e il primo campo sulla
    riga del trattino (`- villain: …`): si conta un record per ogni trattino a
    colonna zero, e si cerca il campo dentro il record giusto. Se il campo non
    c'e' — o se il valore e' uno scalare multiriga, che questa ricerca non sa
    leggere — si torna None e la modifica non parte.
    """
    righe = testo.splitlines(keepends=True)
    inizio = next((n for n, r in enumerate(righe)
                   if r.startswith(f"{sezione}:")), None)
    if inizio is None:
        return None
    corrente = -1
    for n in range(inizio + 1, len(righe)):
        r = righe[n]
        if r.strip() and not r[0].isspace() and not r.startswith("- "):
            break  # un'altra chiave di primo livello: la sezione e' finita
        if r.startswith("- "):
            corrente += 1
            resto, prefisso = r[2:], "- "
        elif r.startswith("  ") and not r[2:3].isspace():
            resto, prefisso = r[2:], "  "
        else:
            continue
        if corrente == indice and resto.startswith(f"{campo}:"):
            return n, prefisso
    return None


def imposta_campo(testo: str, sezione: str, indice: int, campo: str,
                  valore) -> str:
    """Il testo di `state.yaml` con UN campo cambiato, tutto il resto identico.

    Rilancia `StateDataError` se il campo non si trova, se il risultato non e'
    YAML valido, o se il parser vede cambiato qualcosa di diverso da quel
    campo. Nessuno dei tre casi scrive.
    """
    _serve_yaml()
    prima = yaml.safe_load(testo)
    if not isinstance(prima, dict) or not isinstance(prima.get(sezione), list):
        raise StateDataError(f"sezione '{sezione}' assente o non e' una lista")
    if not 0 <= indice < len(prima[sezione]):
        raise StateDataError(f"{sezione}[{indice}] fuori intervallo "
                             f"(la sezione ha {len(prima[sezione])} record)")

    trovata = _riga_del_campo(testo, sezione, indice, campo)
    if trovata is None:
        raise StateDataError(
            f"campo '{campo}' di {sezione}[{indice}] non trovato su una riga "
            "propria: potrebbe essere uno scalare multiriga. Modifica a mano.")
    return _riscrivi(testo, prima, trovata, campo, valore,
                     lambda d: d[sezione][indice].__setitem__(campo, valore),
                     f"{sezione}[{indice}].{campo}")


def trova_villain(dati: dict, nome: "str | None" = None,
                  numeratore: "int | str | None" = None,
                  fondo: "int | str | None" = None) -> "int | None":
    """L'indice dell'UNICO villain che corrisponde, oppure None.

    ⚠️ None sia per «nessuno» sia per «piu' d'uno», e la differenza non serve al
    chiamante: in entrambi i casi la proposta resta manuale. Scegliere il primo
    di due candidati vorrebbe dire far avanzare il clock del villain sbagliato,
    che e' canone rotto in silenzio — il danno che ADR-0041 chiama «contare
    quel che e' dichiarato invece di indovinare».
    """
    trovati = []
    for i, rec in enumerate(dati.get("villain") or []):
        clock = str(rec.get("clock") or "")
        if "/" not in clock:
            continue  # «Trigger, non clock numerico»: non e' un contatore
        num, _, den = clock.partition("/")
        if nome is not None and nome.lower() not in str(rec.get("villain", "")).lower():
            continue
        if numeratore is not None and num.strip() != str(numeratore):
            continue
        if fondo is not None and den.strip() != str(fondo):
            continue
        trovati.append(i)
    return trovati[0] if len(trovati) == 1 else None


def fondo_del_clock(dati: dict, indice: int) -> "str | None":
    """Il denominatore del clock di un villain (`4/8` → `8`)."""
    clock = str((dati.get("villain") or [])[indice].get("clock") or "")
    return clock.partition("/")[2].strip() or None
