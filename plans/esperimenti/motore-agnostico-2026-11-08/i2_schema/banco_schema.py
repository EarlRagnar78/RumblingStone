#!/usr/bin/env python3
"""banco_schema.py — indagine I2 di PIANO-MOTORE-AGNOSTICO-D20: con che cosa si valida un plugin.

Punteggio di mutazione. Dai file veri (4 descrittori `sistema.toml`,
`sistemi.toml`, `pe.toml` di 3.5 e PF1e, `incontri.toml` di 3.5 e PF1e,
`stampa.toml`) genera in modo deterministico ogni mutazione di sette tipi,
poi chiede a ogni validatore se la prende:

    togli       una chiave richiesta sparisce
    tipo        un valore cambia tipo (numero → testo, lista → testo, testo → numero)
    estranea    una chiave in più accanto alle altre (`chiave_sconosciuta`)
    refuso      una chiave scritta male (`skill` → `skil`)
    valore      un valore fuori dominio (numero negativo, metodo inesistente)
    ordine      le soglie dei PE non più crescenti (scambio di due livelli)
    vuoto       una lista o una tabella richiesta resa vuota

Validatori:
    attuale     quello che c'è oggi: `dmcore.sistemi.problemi()` per descrittori
                e configurazione; per i file di dati, lo strumento che li usa
                (update_xp.soglie_di, suggest_encounter.combinatore,
                sistemi.etichette): «presa» se si ferma con un errore
    jsonschema  gli schemi JSON Schema 2020-12 in schemi/ (standard del W3C de
                facto per JSON, letti anche da taplo e dagli editor)
    pydantic    modelli Pydantic v2 equivalenti, più i controlli che JSON
                Schema non sa esprimere (soglie crescenti)

Per ogni presa conta anche se il messaggio indica il percorso della chiave.

    python3 banco_schema.py --json RISULTATI.json

Deterministico: nessun seme, mutazioni in ordine di file e di chiave.
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[3]
sys.path.insert(0, str(REPO / "scripts"))

BERSAGLI = {
    "sistemi/d20/sistema.toml": "sistema", "sistemi/dnd35/sistema.toml": "sistema",
    "sistemi/pf1e/sistema.toml": "sistema", "sistemi.toml": "sistemi",
    "sistemi/dnd35/dati/pe.toml": "pe", "sistemi/pf1e/dati/pe.toml": "pe",
    "sistemi/dnd35/dati/incontri.toml": "incontri", "sistemi/pf1e/dati/incontri.toml": "incontri",
    "sistemi/d20/dati/stampa.toml": "stampa",
}
_bersaglio_finto = "sistemi/prova/sistema.toml"
if (REPO / "sistemi" / "prova" / "sistema.toml").exists():  # pragma: no cover
    BERSAGLI[_bersaglio_finto] = "sistema"
RICHIESTE = {
    "sistema": ["id", "nome", "tipo", "licenza", "fonti", "skill", "capacita"],
    "sistemi": ["progetto", "progetto.predefinito", "progetto.attivi"],
    "pe": ["fonte", "soglie"], "incontri": ["fonte", "metodo"],
    "stampa": ["etichette", "etichette.ca", "etichette.gs"],
}


# ------------------------------------------------------------ le mutazioni

def _foglie(d, prefisso=()):
    for k, v in d.items():
        yield prefisso + (k,), v
        if isinstance(v, dict):
            yield from _foglie(v, prefisso + (k,))


def _prendi(d, percorso):
    for k in percorso[:-1]:
        d = d[k]
    return d


def mutazioni(rel: str, dati: dict) -> list[tuple[str, str, dict]]:
    """[(tipo, descrizione, dati mutati)], in ordine fisso."""
    tipo_file = BERSAGLI[rel]
    out = []

    def aggiungi(t, descr, f):
        m = copy.deepcopy(dati)
        f(m)
        out.append((t, descr, m))

    for chiave in RICHIESTE[tipo_file]:
        p = tuple(chiave.split("."))
        aggiungi("togli", chiave, lambda m, p=p: _prendi(m, p).pop(p[-1]))
        aggiungi("refuso", chiave, lambda m, p=p: _prendi(m, p).__setitem__(p[-1] + "x", _prendi(m, p).pop(p[-1])))
    for p, v in _foglie(dati):
        if len(p) > 3:
            continue
        if isinstance(v, bool):
            continue
        if isinstance(v, int):
            aggiungi("tipo", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], "dodici"))
            aggiungi("valore", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], -7))
        elif isinstance(v, str):
            aggiungi("tipo", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], 12))
            if p[-1] in ("metodo", "tipo", "predefinito"):
                aggiungi("valore", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], "inesistente"))
        elif isinstance(v, list):
            aggiungi("tipo", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], "una-stringa"))
            if v and p[-1] in ("attivi", "dati", "codice"):
                aggiungi("vuoto", ".".join(p), lambda m, p=p: _prendi(m, p).__setitem__(p[-1], []))
        elif isinstance(v, dict) and len(p) <= 2:
            aggiungi("estranea", ".".join(p), lambda m, p=p: _prendi(m, p + ("x",)).__setitem__("chiave_sconosciuta", 1))
    aggiungi("estranea", "(radice)", lambda m: m.__setitem__("chiave_sconosciuta", 1))
    if tipo_file == "pe":
        for traccia in sorted(dati["soglie"]):
            aggiungi("ordine", f"soglie.{traccia} 5↔6",
                     lambda m, t=traccia: m["soglie"][t].update({"5": m["soglie"][t]["6"], "6": m["soglie"][t]["5"]}))
    if tipo_file == "sistema":
        for nome in sorted(dati.get("capacita", {}))[:3]:
            aggiungi("refuso", f"capacita.{nome} modo", lambda m, n=nome: m["capacita"].__setitem__(
                n, {("dato" if k == "dati" else k + "x" if k in ("eredita", "codice", "non_supportato") else k): v
                    for k, v in m["capacita"][n].items()}))
    return out


# ------------------------------------------------------------ i validatori

def _scrivi_toml(percorso: Path, dati: dict) -> None:
    import tomli_w
    percorso.write_text(tomli_w.dumps(dati), encoding="utf-8")


class Attuale:
    nome = "attuale (problemi() e gli strumenti)"

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        shutil.copytree(REPO / "sistemi", self.root / "sistemi")
        shutil.copy2(REPO / "sistemi.toml", self.root / "sistemi.toml")
        from tests.test_sistemi_prova_del_nove import _file_dei_plugin
        for rel in _file_dei_plugin() | {"scripts/tools.manifest.json"}:
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, self.root / rel)
        for d in (REPO / "skills").iterdir():
            if (d / "SKILL.md").is_file():
                (self.root / "skills" / d.name).mkdir(parents=True)
                (self.root / "skills" / d.name / "SKILL.md").write_text("", encoding="utf-8")
        for cartella in tomllib.loads((REPO / "sistemi.toml").read_text(encoding="utf-8")).get("moduli", {}):
            (self.root / cartella).mkdir(parents=True, exist_ok=True)

    def prova(self, rel: str, tipo_file: str, dati: dict) -> tuple[str, str]:
        from dmcore import sistemi as S
        import sistemi as CLI
        import update_xp as UX
        import suggest_encounter as SE
        originale = (self.root / rel).read_bytes()
        _scrivi_toml(self.root / rel, dati)
        vero = S.ROOT
        S.ROOT = self.root
        S._carica.cache_clear()
        try:
            if tipo_file in ("sistema", "sistemi"):
                prob = S.problemi(self.root, CLI.strumenti(self.root))
                return ("presa", prob[0]) if prob else ("sfuggita", "")
            sis = rel.split("/")[1]
            if tipo_file == "pe":
                UX.soglie_di(sis, "media" if sis == "pf1e" else None)
            elif tipo_file == "incontri":
                SE.combinatore(sis, self.root)([5, 5])
            elif tipo_file == "stampa":
                S.etichette("dnd35", self.root)
            return "sfuggita", ""
        except SystemExit as ex:  # gli strumenti si fermano con un messaggio: è una presa pulita
            return "presa", str(ex)[:200]
        except Exception as ex:  # noqa: BLE001  un traceback: presa, ma come crash
            return "crash", f"{type(ex).__name__}: {ex}"[:200]
        finally:
            S.ROOT = vero
            S._carica.cache_clear()
            (self.root / rel).write_bytes(originale)


class ConJsonschema:
    nome = "jsonschema (JSON Schema 2020-12)"

    def __init__(self):
        import jsonschema
        self.m = jsonschema
        self.schemi = {p.name.split(".")[0]: json.loads(p.read_text(encoding="utf-8"))
                       for p in sorted((QUI / "schemi").glob("*.schema.json"))}

    def prova(self, rel, tipo_file, dati):
        v = self.m.Draft202012Validator(self.schemi[tipo_file], format_checker=self.m.FormatChecker())
        errori = sorted(v.iter_errors(dati), key=lambda e: list(e.absolute_path))
        if not errori:
            return "sfuggita", ""
        e = errori[0]
        return "presa", f"{'/'.join(map(str, e.absolute_path)) or '(radice)'}: {e.message}"[:200]


class ConFastjsonschema:
    """Gli stessi schemi, con un validatore in puro Python (BSD-3, nessuna dipendenza) che si può portare
    dentro il pacchetto. Conosce le bozze 4, 6 e 7: gli schemi usano solo parole che la 7 ha già."""
    nome = "fastjsonschema (stessi schemi, bozza 7)"

    def __init__(self):
        import fastjsonschema
        self.Errore = fastjsonschema.JsonSchemaValueException
        self.v = {}
        for p in sorted((QUI / "schemi").glob("*.schema.json")):
            schema = json.loads(p.read_text(encoding="utf-8"))
            schema["$schema"] = "http://json-schema.org/draft-07/schema#"
            self.v[p.name.split(".")[0]] = fastjsonschema.compile(schema)

    def prova(self, rel, tipo_file, dati):
        try:
            self.v[tipo_file](dati)
            return "sfuggita", ""
        except self.Errore as e:  # si ferma al primo errore
            return "presa", f"{'/'.join(map(str, e.path[1:])) or '(radice)'}: {e.message}"[:200]


class ConPydanticDaSchema:
    """Pydantic guidato dai dati del plugin: i modelli si GENERANO dagli stessi JSON Schema con
    datamodel-code-generator (MIT, lo standard di fatto per JSON Schema → pydantic), senza scriverli a mano.
    Misura se il nucleo compilato di pydantic, nutrito con i dati del plugin, prende più difetti."""
    nome = "pydantic generato dagli schemi (datamodel-code-generator)"

    def __init__(self):
        import importlib.util
        import inspect
        import tempfile
        import warnings
        from datamodel_code_generator import DataModelType, InputFileType, generate
        from pydantic import BaseModel, ValidationError
        self.Errore = ValidationError
        self.modelli = {}
        self._tmp = tempfile.TemporaryDirectory()
        for p in sorted((QUI / "schemi").glob("*.schema.json")):
            nome = p.name.split(".")[0]
            out = Path(self._tmp.name) / f"m_{nome}.py"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                generate(p.read_text(encoding="utf-8"), input_file_type=InputFileType.JsonSchema,
                         output=out, output_model_type=DataModelType.PydanticV2BaseModel,
                         strict_types=["str", "int", "bool"], use_annotated=True, disable_timestamp=True)
            spec = importlib.util.spec_from_file_location(f"generato_{nome}", out)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            classi = [c for c in vars(mod).values()  # vars() tiene l'ordine del file
                      if inspect.isclass(c) and issubclass(c, BaseModel) and c.__module__ == mod.__name__]
            radice = classi[-1]  # l'ultima del file è la radice
            radice.model_rebuild(_types_namespace=vars(mod))
            self.modelli[nome] = radice
        self.righe_generate = sum(len((Path(self._tmp.name) / f).read_text().splitlines())
                                  for f in sorted(x.name for x in Path(self._tmp.name).glob("*.py")))

    def prova(self, rel, tipo_file, dati):
        try:
            self.modelli[tipo_file].model_validate(dati)
            return "sfuggita", ""
        except self.Errore as e:
            p = e.errors()[0]
            return "presa", f"{'/'.join(map(str, p['loc'])) or '(radice)'}: {p['msg']}"[:200]


class ConPydantic:
    nome = "pydantic v2 (modelli + validatori)"

    def __init__(self):
        from typing import Annotated, Literal
        from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator, field_validator, ValidationError
        self.Errore = ValidationError
        Rigido = ConfigDict(extra="forbid", strict=True)
        Testo = Annotated[str, StringConstraints(min_length=1)]

        class Voce(BaseModel):
            model_config = Rigido
            dati: list[Testo] | None = Field(None, min_length=1)
            codice: list[Annotated[str, StringConstraints(pattern=r"^[^:]+:[A-Za-z_]\w*$")]] | None = Field(None, min_length=1)
            eredita: Testo | None = None
            non_supportato: Testo | None = None
            motivo: Testo | None = None
            lotto: Annotated[str, StringConstraints(pattern=r"^L\d+[a-z]?$")] | None = None
            nota: str | None = None

            @model_validator(mode="after")
            def un_modo(self):
                modi = [m for m in ("dati", "codice", "eredita", "non_supportato") if getattr(self, m) is not None]
                if len(modi) != 1:
                    raise ValueError(f"serve uno e un solo modo, trovati {modi}")
                if self.eredita and not self.motivo:
                    raise ValueError("eredita senza motivo")
                if self.codice and not self.lotto:
                    raise ValueError("codice senza lotto")
                return self

        class Sistema(BaseModel):
            model_config = Rigido
            id: Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]*$")]
            nome: Testo
            tipo: Literal["sistema", "famiglia"]
            famiglia: str | None = None
            licenza: Testo
            fonti: list[str]
            riconosci: list[str] = []
            skill: list[Annotated[str, StringConstraints(pattern=r"^[a-z0-9-]+$")]]
            capacita: dict[Annotated[str, StringConstraints(pattern=r"^[a-z]+\.[a-z_]+$")], Voce]

        class Progetto(BaseModel):
            model_config = Rigido
            predefinito: str
            attivi: list[str] = Field(min_length=1)
            rinforzo: list[str] = []

            @model_validator(mode="after")
            def predefinito_attivo(self):
                if self.predefinito not in self.attivi:
                    raise ValueError("il predefinito non è fra gli attivi")
                return self

        Velocita = Literal["lenta", "media", "veloce"]

        class OpzioniPf1e(BaseModel):
            model_config = Rigido
            traccia_pe: Velocita | None = None
            velocita_tesoro: Velocita | None = None

        class Opzioni(BaseModel):  # come lo schema JSON: pf1e chiuso, gli altri liberi
            model_config = ConfigDict(extra="allow", strict=True)
            pf1e: OpzioniPf1e | None = None

        class Sistemi(BaseModel):
            model_config = Rigido
            progetto: Progetto
            moduli: dict[str, str] = {}
            opzioni: Opzioni = Opzioni()
            ambientazioni: dict = {}

        Livelli = dict[Annotated[str, StringConstraints(pattern=r"^([1-9]|1\d|20)$")], Annotated[int, Field(ge=0)]]

        class Pe(BaseModel):
            model_config = Rigido
            fonte: Testo
            etichetta: str | None = None
            soglie: dict[Literal["unica", "lenta", "media", "veloce"], Livelli] = Field(min_length=1)

            @field_validator("soglie")
            @classmethod
            def crescenti(cls, v):
                for nome, t in v.items():
                    if len(t) != 20:
                        raise ValueError(f"{nome}: servono 20 livelli, ce ne sono {len(t)}")
                    valori = [t[str(i)] for i in range(1, 21)]
                    if valori != sorted(valori) or len(set(valori)) != 20:
                        raise ValueError(f"{nome}: le soglie non crescono")
                return v

        class Incontri(BaseModel):
            model_config = Rigido
            fonte: Testo
            fonte_difficolta: str | None = None
            metodo: Literal["potenze", "somma_px"]
            raddoppio: Annotated[int, Field(ge=2)] | None = None
            px_per_gs: dict[Annotated[str, StringConstraints(pattern=r"^(1/[2-8]|[1-9]\d?)$")], Annotated[int, Field(ge=1)]] | None = None
            difficolta: dict[str, int] | None = None

            @model_validator(mode="after")
            def parametri(self):
                if self.metodo == "potenze" and self.raddoppio is None:
                    raise ValueError("potenze senza raddoppio")
                if self.metodo == "somma_px" and not self.px_per_gs:
                    raise ValueError("somma_px senza px_per_gs")
                return self

        class Etichette(BaseModel):
            model_config = Rigido
            ca: Testo
            pf: Testo
            ts: Testo
            vel: Testo
            gs: Testo
            iniziativa: Testo
            sensi: Testo

        class Stampa(BaseModel):
            model_config = Rigido
            etichette: Etichette

        self.modelli = {"sistema": Sistema, "sistemi": Sistemi, "pe": Pe, "incontri": Incontri, "stampa": Stampa}

    def prova(self, rel, tipo_file, dati):
        try:
            self.modelli[tipo_file].model_validate(dati)
            return "sfuggita", ""
        except self.Errore as e:
            p = e.errors()[0]
            return "presa", f"{'/'.join(map(str, p['loc'])) or '(radice)'}: {p['msg']}"[:200]


def _con_percorso(msg: str, descr: str) -> bool:
    """Il messaggio nomina la chiave toccata (o la sua ultima parte)?"""
    ultima = descr.split(" ")[0].split(".")[-1]
    return ultima in msg or descr == "(radice)" and "chiave_sconosciuta" in msg


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    validatori = [Attuale(), ConJsonschema(), ConFastjsonschema(), ConPydanticDaSchema(), ConPydantic()]
    # i file veri devono passare tutti
    falsi_allarmi = {v.nome: [] for v in validatori}
    casi = []
    for rel, tipo_file in BERSAGLI.items():
        dati = tomllib.loads((REPO / rel).read_text(encoding="utf-8"))
        for v in validatori:
            esito, msg = v.prova(rel, tipo_file, dati)
            if esito != "sfuggita":
                falsi_allarmi[v.nome].append(f"{rel}: {msg}")
        for t, descr, m in mutazioni(rel, dati):
            riga = {"file": rel, "tipo": t, "dove": descr}
            for v in validatori:
                esito, msg = v.prova(rel, tipo_file, m)
                riga[v.nome] = {"esito": esito, "con_chiave": esito == "presa" and _con_percorso(msg, descr),
                                "messaggio": msg}
            casi.append(riga)
    tot = len(casi)
    sintesi = {}
    for v in validatori:
        conta = {e: sum(c[v.nome]["esito"] == e for c in casi) for e in ("presa", "crash", "sfuggita")}
        per_tipo = {}
        for c in casi:
            d = per_tipo.setdefault(c["tipo"], [0, 0])
            d[0] += c[v.nome]["esito"] == "presa"
            d[1] += 1
        sintesi[v.nome] = {**conta, "su": tot, "punteggio_prese_pulite": round(100 * conta["presa"] / tot, 1),
                           "con_chiave": sum(c[v.nome]["con_chiave"] for c in casi),
                           "falsi_allarmi_sui_file_veri": falsi_allarmi[v.nome],
                           "per_tipo": {k: f"{a}/{b}" for k, (a, b) in sorted(per_tipo.items())}}
    sfuggite = {v.nome: [f"{c['file']} · {c['tipo']} · {c['dove']}" for c in casi if c[v.nome]["esito"] == "sfuggita"]
                for v in validatori}
    ris = {"mutazioni": tot, "sintesi": sintesi, "sfuggite": sfuggite, "casi": casi}
    if a.json:
        Path(a.json).write_text(json.dumps(ris, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{tot} mutazioni su {len(BERSAGLI)} file\n")
    for n, s in sintesi.items():
        print(f"{n:40} prese {s['presa']:>3}/{s['su']} ({s['punteggio_prese_pulite']}%)  crash {s['crash']:>3}  "
              f"sfuggite {s['sfuggita']:>3}  messaggio con la chiave {s['con_chiave']:>3}  falsi allarmi {len(s['falsi_allarmi_sui_file_veri'])}")
        print("    " + "  ".join(f"{k} {v}" for k, v in s["per_tipo"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
