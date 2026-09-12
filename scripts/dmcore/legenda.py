"""
legenda — la legenda dei simboli, letta da una fonte sola (ADR-0048).

Prima di questo modulo la stessa informazione viveva in **cinque** posti:
``SYMBOLS`` in ``render_map_svg.py`` per il rendering, e quattro ``set``
cablati nei consumatori — ``WALL_SYMS``, ``DOOR_SYMS``, ``LIGHT_SYMS`` in
``export_uvtt.py``, ``HAZARD_SYMS`` in ``import_ultraclear.py``.

Al momento della migrazione i cinque **non** erano divergenti in
appartenenza. Il difetto non era un errore presente: era che niente
impediva il prossimo — e il prossimo era già arrivato due volte, ognuna
col suo ADR per rattoppare un sintomo della stessa causa (ADR-0042 sui tre
glifi sotto ``⬛``, ADR-0043 sulle montagne che non erano muri in Foundry).

⚠️ **Perché legge JSON e non YAML.** La fonte scritta a mano è
``scripts/legend.yaml``, che porta i commenti: la memoria di *perché* una
tenda è un muro non sta in un ADR soltanto, sta accanto al dato. Ma
``pyyaml`` è un debito dichiarato (ADR-0037) e non può entrare nel percorso
di rendering, che è ``stdlib_only``. Quindi ``scripts/build_legend.py``
deriva ``scripts/legend.json``, committato e verificato in CI — la forma
che ADR-0048 §2 prescrive, la stessa già in uso per ``docs/tools/``.

Solo stdlib.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

# la convenzione metrica del repo, identica per 3.5, PF1e e 5e (spec §3.5)
METRI_PER_QUADRETTO = 1.5

SORGENTE = Path(__file__).resolve().parent.parent / "legend.yaml"
DERIVATO = Path(__file__).resolve().parent.parent / "legend.json"


@lru_cache(maxsize=1)
def _dati() -> dict:
    return json.loads(DERIVATO.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def simboli() -> dict[str, dict]:
    """La tabella di rendering, nella forma storica che i consumatori leggono.

    Le chiavi sono quelle di sempre — ``mode``, ``pat``, ``prop``, ``fill``,
    ``it`` — perché cinque script e sei test le usano: cambiarle sarebbe un
    secondo lotto travestito da primo.
    """
    fuori: dict[str, dict] = {}
    for sim, voce in _dati()["symbols"].items():
        r = voce["render"]
        spec = {"mode": r["mode"]}
        if "pat" in r:
            spec["pat"] = r["pat"]
        if "prop" in r:
            spec["prop"] = r["prop"]
        spec["fill"] = r["fill"]
        spec["it"] = voce.get("label", "")
        fuori[sim] = spec
    return fuori


@lru_cache(maxsize=1)
def pattern_pesanti() -> frozenset[str]:
    """I pattern che ricevono ombra portata e contorno marcato.

    Indicizzati per **pattern** e non per simbolo perché è così che il ciclo
    di pittura del renderer li interroga.
    """
    return frozenset(v["render"]["pat"] for v in _dati()["symbols"].values()
                     if v["render"].get("heavy") and "pat" in v["render"])


def _con(campo: str) -> frozenset[str]:
    return frozenset(s for s, v in _dati()["symbols"].items()
                     if v.get("function", {}).get(campo))


@lru_cache(maxsize=1)
def altezze() -> dict[str, float]:
    """Estrusione 3D in metri per la catena Blender (negativa = scavo).

    ⚠️ Non è ``elevation_m`` di ``LEGENDA-FUNZIONALE-SPEC`` §2, che è la
    **quota del pavimento** della cella. Questa è l'altezza del volume che si
    alza da quel pavimento: la chioma di un albero, la profondità di una
    voragine. Due geometrie diverse, e confonderle sarebbe il difetto che
    ADR-0048 cura.
    """
    return {s: v["render"]["altezza_m"] for s, v in _dati()["symbols"].items()
            if "altezza_m" in v["render"]}


@lru_cache(maxsize=1)
def piatti() -> frozenset[str]:
    """Restano a quota zero: un varco non è un volume."""
    return frozenset(s for s, v in _dati()["symbols"].items()
                     if v["render"].get("piatto"))


@lru_cache(maxsize=1)
def texture() -> dict[str, str]:
    """Cartella di texture per famiglia di superficie.

    Non è uno slug di Poly Haven: è il nome della cartella che il DM riempie
    con l'asset che sceglie, verificando la licenza del singolo file.
    """
    return {s: v["render"]["texture"] for s, v in _dati()["symbols"].items()
            if "texture" in v["render"]}


@lru_cache(maxsize=1)
def muri() -> frozenset[str]:
    """I simboli che l'export UVTT trasforma in segmento di muro.

    ⚠️ **Non è un campo a sé, ed è deliberato.** Il muro deriva dal fatto
    neutro ``blocks_sight``, meno le **deroghe dichiarate**. Un secondo
    booleano accanto al fatto sarebbe una seconda fonte di verità — la
    malattia esatta che ADR-0048 cura — e diverrebbe in silenzio.

    Una deroga esiste perché il muro del VTT è **binario** e la finzione no:
    un bosco blocca la vista *attraverso* la cella, non *dentro*; un treant è
    una creatura; una porta ha già la sua geometria. Ognuna deve scrivere il
    proprio motivo in ``deroga_uvtt``, e
    ``test_legenda_fonte_unica.TestLeDerogheSonoDichiarate`` le conta: una
    deroga senza motivo è rossa.
    """
    return frozenset(s for s, v in _dati()["symbols"].items()
                     if v.get("function", {}).get("blocks_sight")
                     and not v.get("function", {}).get("deroga_uvtt"))


@lru_cache(maxsize=1)
def deroghe() -> dict[str, str]:
    """``simbolo -> motivo`` per cui il fatto neutro e l'export divergono."""
    return {s: v["function"]["deroga_uvtt"] for s, v in _dati()["symbols"].items()
            if v.get("function", {}).get("deroga_uvtt")}


@lru_cache(maxsize=1)
def porte() -> frozenset[str]:
    return _con("door")


@lru_cache(maxsize=1)
def pericoli() -> frozenset[str]:
    """Classificati come pericolo dall'import, non come struttura.

    ⚠️ ``❄`` porta ``severity: null``: il codice lo tratta da pericolo dal
    primo giorno, la specifica non lo classifica affatto. Tengo la
    classificazione e **non invento la gravità**.
    """
    return _con("hazard")


@lru_cache(maxsize=1)
def luci() -> dict[str, tuple[float, str]]:
    """``simbolo -> (raggio in quadretti, colore esadecimale senza cancelletto)``.

    La legenda lo dichiara in **metri**, come ``LEGENDA-FUNZIONALE-SPEC``
    §4.3 chiede; l'export UVTT ragiona in quadretti, e la conversione sta
    qui, in un posto solo.

    ⚠️ **I valori sono quelli del codice, non quelli della specifica**, ed è
    una decisione presa (DM, 2026-09-12). La spec dava i raggi RAW di 3.5 —
    torcia 20 ft, candela 5 ft — mentre il repo illumina da 1,5 a 3 volte di
    più. Le mappe notturne sono state disegnate e giocate con questa luce:
    dimezzarla per aderenza al manuale le spegnerebbe tutte insieme. La
    divergenza si è chiusa **scrivendo in metri i valori del codice**
    (9 · 7,5 · 6 · 4,5), non cambiandoli.
    """
    fuori = {}
    for sim, voce in _dati()["symbols"].items():
        luce = voce.get("function", {}).get("light")
        if luce:
            fuori[sim] = (round(luce["raggio_m"] / METRI_PER_QUADRETTO, 6),
                          luce["colore"])
    return fuori
