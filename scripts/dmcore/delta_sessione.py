"""Il delta di sessione come dato: il front-matter del log (lotto 4e).

🔴 **Questo modulo esiste per una regex coi nomi scritti nel sorgente.**
`state_sync.TRIGGERS` riconosce i villain per nome, e i nomi sono quelli che
c'erano quando la regex e' stata scritta. Misurato il 2026-09-24 sui tredici
villain di `campaign/state.yaml`: `villain_clock` ne vede **3 su 9**,
`npc_killed` **5 su 13**, e Ghaurush, Zin'thara e Ushgar non li vede nessuno
dei due. Un clock di Ghaurush scritto nel log a fine sessione non diventava
nemmeno una proposta a mano: la riga non veniva riconosciuta.

Il log resta markdown, perche' e' un documento che si legge e che alimenta
recap e booklet. Porta pero' in testa i **delta** che `state_apply` sa
scrivere, e li nomina per `png_id`, la chiave che ogni record `villain` ha
dal lotto 4d-4. Il front-matter lo scrive il wizard: il DM non scrive YAML.

    ---
    delta:
      march_clock: {da: 19, a: 20}
      clock:
      - {png_id: ghaurush, da: 0, a: 1}
      stato:
      - {png_id: ushgar, stato: morto}
    ---

⚠️ **Tutto o niente.** Un delta che non si valida per intero non produce
nessuna operazione: `da` diverso dal valore di oggi vuol dire un log gia'
applicato o scritto su un altro stato, e applicarne meta' lascerebbe il canone
in un punto che nessun log descrive.

⚠️ pyyaml e' un debito dichiarato (ADR-0037), come in `statedata`: lo importa
chi legge. `emetti` e' stdlib, perche' lo usa il wizard.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dipendenza dichiarata in ADR-0037
    yaml = None  # type: ignore[assignment]

SCHEMA = (Path(__file__).resolve().parent.parent
          / "schemas" / "campaign_state.schema.json")

#: I trigger di `state_sync` che il front-matter sostituisce. Con un delta nel
#: log la regex non scrive piu' niente per questi: le due vie insieme
#: applicherebbero due volte lo stesso clock.
MECCANICI = frozenset({"march_clock", "ritual_clock", "villain_clock",
                       "npc_killed", "npc_escaped"})

CHIAVI = ("march_clock", "clock", "stato")
_PNG_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class DeltaError(ValueError):
    """Il delta non e' applicabile: non si scrive niente."""


@dataclass(frozen=True)
class Operazione:
    """Una scrittura in `state.yaml`, gia' risolta e validata."""
    sezione: str
    #: None per una sezione-oggetto (`march_clock`)
    indice: "int | None"
    campo: str
    valore: object
    etichetta: str


def stati_ammessi() -> "tuple[str, ...]":
    """L'enumerazione di `villain.stato`, letta dallo schema e non riscritta."""
    dati = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return tuple(dati["properties"]["villain"]["items"]
                 ["properties"]["stato"]["enum"])


def estrai(testo: str) -> "dict | None":
    """Il blocco `delta` del front-matter, o None se il log non ne ha.

    Un front-matter c'e' se il file comincia con `---` su una riga sua. Se c'e'
    ma non si legge, e' un errore e non un «niente»: ricadere sulla regex in
    silenzio sarebbe proprio il difetto che questo modulo toglie.
    """
    if not testo.startswith("---\n"):
        return None
    fine = testo.find("\n---\n", 3)
    if fine < 0:
        raise DeltaError("front-matter aperto con `---` e mai chiuso")
    if yaml is None:  # pragma: no cover
        raise DeltaError("serve pyyaml per leggere il front-matter (ADR-0037)")
    try:
        dati = yaml.safe_load(testo[4:fine]) or {}
    except yaml.YAMLError as exc:
        raise DeltaError(f"front-matter illeggibile: {exc}") from None
    if not isinstance(dati, dict):
        raise DeltaError("il front-matter non e' un oggetto")
    delta = dati.get("delta")
    if delta is None:
        return None
    if not isinstance(delta, dict):
        raise DeltaError("`delta` non e' un oggetto")
    return delta


def _intero(v, dove: str, problemi: list) -> "int | None":
    if isinstance(v, bool) or not isinstance(v, int):
        problemi.append(f"{dove}: atteso un intero, trovato {v!r}")
        return None
    return v


def _villain(dati: dict, png_id, dove: str, problemi: list) -> "int | None":
    if not isinstance(png_id, str) or not _PNG_ID.match(png_id):
        problemi.append(f"{dove}: `png_id` non valido: {png_id!r}")
        return None
    trovati = [i for i, r in enumerate(dati.get("villain") or [])
               if r.get("png_id") == png_id]
    if len(trovati) != 1:
        problemi.append(f"{dove}: nessun villain con png_id «{png_id}» in "
                        "campaign/state.yaml" if not trovati else
                        f"{dove}: png_id «{png_id}» ripetuto in state.yaml")
        return None
    return trovati[0]


def operazioni(delta: dict, dati: dict) -> "list[Operazione]":
    """Le scritture che il delta chiede, oppure `DeltaError` con TUTTI i motivi.

    Le operazioni che non cambiano niente (`da == a`, un valore che e' gia'
    `a`, uno stato gia' quello) non compaiono: un log applicato due volte non
    scrive la seconda, e non e' un errore. Lo e' un `da` che non corrisponde
    ne' al prima ne' al dopo: il log e' stato scritto su un altro stato.
    """
    problemi: list[str] = []
    ops: list[Operazione] = []

    for k in delta:
        if k not in CHIAVI:
            problemi.append(f"chiave sconosciuta `delta.{k}` "
                            f"(ammesse: {', '.join(CHIAVI)})")

    mc = delta.get("march_clock")
    if mc is not None:
        if not isinstance(mc, dict) or set(mc) != {"da", "a"}:
            problemi.append("delta.march_clock: servono esattamente `da` e `a`")
        else:
            da = _intero(mc["da"], "delta.march_clock.da", problemi)
            a = _intero(mc["a"], "delta.march_clock.a", problemi)
            oggi = (dati.get("march_clock") or {}).get("giorno_corrente")
            if a is not None and oggi == a:
                pass  # gia' applicato: lo stesso log, una seconda volta
            elif da is not None and da != oggi:
                problemi.append(f"delta.march_clock: il log parte dal Day {da}, "
                                f"state.yaml e' al Day {oggi}")
            elif da is not None and a is not None and a != da:
                ops.append(Operazione("march_clock", None, "giorno_corrente", a,
                                      f"March Clock Day {da} → Day {a}"))

    visti: set = set()
    for n, voce in enumerate(delta.get("clock") or []):
        dove = f"delta.clock[{n}]"
        if not isinstance(voce, dict) or set(voce) != {"png_id", "da", "a"}:
            problemi.append(f"{dove}: servono esattamente `png_id`, `da` e `a`")
            continue
        i = _villain(dati, voce["png_id"], dove, problemi)
        da = _intero(voce["da"], f"{dove}.da", problemi)
        a = _intero(voce["a"], f"{dove}.a", problemi)
        if isinstance(voce["png_id"], str):
            if voce["png_id"] in visti:
                problemi.append(f"{dove}: «{voce['png_id']}» compare due volte")
            visti.add(voce["png_id"])
        if i is None or da is None or a is None:
            continue
        clock = str(dati["villain"][i].get("clock") or "")
        num, sep, fondo = clock.partition("/")
        if not sep or not num.strip().isdigit() or not fondo.strip().isdigit():
            problemi.append(f"{dove}: il clock di «{voce['png_id']}» non e' "
                            f"numerico ({clock!r})")
            continue
        if int(num) == a:
            continue  # gia' applicato
        if int(num) != da:
            problemi.append(f"{dove}: il log dice {da}/{fondo.strip()}, "
                            f"state.yaml dice {clock}")
            continue
        if not 0 <= a <= int(fondo):
            problemi.append(f"{dove}: {a} esce dal clock /{fondo.strip()}")
            continue
        if a != da:
            ops.append(Operazione("villain", i, "clock", f"{a}/{fondo.strip()}",
                                  f"clock {voce['png_id']} {da}/{fondo.strip()} → "
                                  f"{a}/{fondo.strip()}"))

    ammessi = stati_ammessi()
    visti = set()
    for n, voce in enumerate(delta.get("stato") or []):
        dove = f"delta.stato[{n}]"
        if not isinstance(voce, dict) or set(voce) != {"png_id", "stato"}:
            problemi.append(f"{dove}: servono esattamente `png_id` e `stato`")
            continue
        i = _villain(dati, voce["png_id"], dove, problemi)
        if voce["stato"] not in ammessi:
            problemi.append(f"{dove}: stato «{voce['stato']}» fuori "
                            f"enumerazione ({' · '.join(ammessi)})")
            continue
        if isinstance(voce["png_id"], str):
            if voce["png_id"] in visti:
                problemi.append(f"{dove}: «{voce['png_id']}» compare due volte")
            visti.add(voce["png_id"])
        if i is None:
            continue
        if dati["villain"][i].get("stato") != voce["stato"]:
            ops.append(Operazione("villain", i, "stato", voce["stato"],
                                  f"{voce['png_id']}: stato → {voce['stato']}"))

    if problemi:
        raise DeltaError("; ".join(problemi))
    return ops


def risolvi_villain(dati: dict, nome: str) -> "tuple[str | None, list[str]]":
    """(`png_id`, candidati) per il nome che il DM ha scritto.

    Prima il `png_id` esatto, poi il nome dentro l'etichetta del villain. Un
    solo candidato → quello; zero o piu' d'uno → None, e i candidati servono a
    dire al DM fra chi scegliere. Si risolve MENTRE il DM risponde, cosi' un
    nome che non aggancia niente lo vede lui, e non `state_apply` a sera finita.
    """
    nome = nome.strip()
    villain = dati.get("villain") or []
    esatti = [r["png_id"] for r in villain if r.get("png_id") == nome.lower()]
    if esatti:
        return esatti[0], esatti
    trovati = [r["png_id"] for r in villain
               if nome and nome.lower() in str(r.get("villain", "")).lower()]
    return (trovati[0] if len(trovati) == 1 else None), trovati


def emetti(delta: dict) -> str:
    """Il front-matter in forma fissa, riga per riga: stdlib, e sempre uguale.

    Scriverlo a mano invece che con `yaml.safe_dump` tiene il wizard senza
    dipendenze e il diff di due log leggibile. `estrai` lo rilegge col parser,
    e un test prova che il giro torna.
    """
    righe = ["---",
             "# delta di sessione: lo scrive il wizard, lo legge state_apply",
             "delta:"]
    mc = delta.get("march_clock")
    if mc:
        righe.append(f"  march_clock: {{da: {int(mc['da'])}, a: {int(mc['a'])}}}")
    for chiave, campi in (("clock", ("da", "a")), ("stato", ("stato",))):
        voci = delta.get(chiave) or []
        if not voci:
            continue
        righe.append(f"  {chiave}:")
        for v in voci:
            if not _PNG_ID.match(str(v["png_id"])):
                raise DeltaError(f"png_id non valido: {v['png_id']!r}")
            if "stato" in campi and v["stato"] not in stati_ammessi():
                raise DeltaError(f"stato fuori enumerazione: {v['stato']!r}")
            resto = ", ".join(
                f"{c}: {int(v[c])}" if c in ("da", "a") else f"{c}: {v[c]}"
                for c in campi)
            righe.append(f"  - {{png_id: {v['png_id']}, {resto}}}")
    if len(righe) == 3:
        return ""
    righe.append("---")
    return "\n".join(righe) + "\n"
