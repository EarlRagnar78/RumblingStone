#!/usr/bin/env python3
"""raccogli_casi_agenti.py — ogni thread nuovo porta un caso al set d'oro degli agenti (ADR-0154).

Il limite vero della misura di ``instradamento_agenti.py --eval`` è n. Scelta di Jfs del
2026-11-27: ogni thread nuovo aggiunge un caso, raccolto da solo dalla routine del lunedì,
e Jfs ne conferma l'etichetta una volta a settimana sulle card. La CI non legge i thread:
questo script lavora sui messaggi che la routine esporta.

    proponi IN.json --coda DIR   scarta duplicati e testi con segreti o email, etichetta
                                 ogni caso con la predizione dell'hook («proposta») e scrive
                                 DIR/AAAA-Www.json e DIR/CARD.md (una card per caso)
    cieco DIR/AAAA-Www.json      scrive DIR/CIECO-AAAA-Www.tsv: id e testo dei casi del DM,
                                 senza la proposta, per un annotatore cieco
    annota DIR/AAAA-Www.json ANNOTAZIONI.tsv
                                 la consigliata di ogni caso è l'etichetta dell'annotatore
                                 cieco (``id_messaggio<TAB>etichetta``); stampa l'accordo
                                 con l'hook e la kappa di Cohen. La consigliata non è mai la
                                 proposta dell'hook: sarebbe ancoraggio sulla cosa misurata
    applica DIR/AAAA-Www.json SCELTE.tsv
                                 aggiunge i casi confermati al set d'oro, split per hash
                                 sha256 dell'id (50/50 dev/test), rimette il tetto con l'hook
                                 invariato e stampa la misura prima e dopo
    --check                      la forma del set d'oro: esce 1 se non va

SCELTE.tsv: ``id_messaggio<TAB>atteso<TAB>accettabili<TAB>azione``, accettabili separati da
virgola (vuoto se nessuno), azione ``tieni`` o ``togli``; la prima riga può essere
l'intestazione.

Exit: 0 ok · 1 set non in forma, o scelte che non tornano (niente scritto) · 2 ingresso
malformato.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import instradamento_agenti as ia  # noqa: E402

NESSUNO = ia.NESSUNO
AGENTI = tuple(sorted(ia.CATENE))
ETICHETTE = set(AGENTI) | {NESSUNO}
TIPI = ("dm", "coordinatore", "sottoagente")
SPLIT_OK = ("dev", "test")
CAMPI_CASO = ("data", "fonte", "tipo", "testo", "atteso", "accettabili", "split")
CAMPI_IN = ("data", "fonte", "tipo", "testo", "id_messaggio")
CAMPI_TETTO = ("giusti", "giusti_indulgenti", "macro_f1")
AZIONI = ("tieni", "togli")
ABBREVIA = 320

NOTA_HASH = (" Dal 2026-11-27 i casi raccolti ogni settimana dai thread nuovi "
             "(raccogli_casi_agenti.py, etichetta confermata da Jfs su card) portano "
             "id_messaggio e hanno lo split per hash: sha256 dell'id, pari dev e dispari test, "
             "come gli split stabili di TFDS e Hugging Face, che non si rimescolano quando il "
             "set cresce.")
_RIMESSA = re.compile(r"\s*Ultima rimessa \(raccogli_casi_agenti\.py applica\):.*$", re.S)

# Segreti ed email: nessun controllo così nel repo. Le regole sono un sottoinsieme di quelle
# di default di gitleaks (chiavi con prefisso noto, chiavi private, password assegnate); un
# percorso /home/<nome> o C:\Users\<nome> porta un nome utente (ADR-0127, dati personali).
SEGRETI = (
    ("indirizzo email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*"
                                   r"\.[A-Za-z]{2,}")),
    ("token GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
    ("chiave API (sk-)", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}")),
    ("chiave AWS", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("token Slack", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("chiave Google", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("chiave privata", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("password assegnata", re.compile(r"(?i)\b(?:password|passwd|pwd|secret|token|api[_-]?key)"
                                      r"\s*[:=]\s*\S{4,}")),
    ("percorso con nome utente", re.compile(r"(?:/home/(?!user\b)[a-z_][\w.-]*|"
                                            r"/Users/[\w.-]+|[A-Za-z]:\\Users\\[\w.-]+)")),
)


def normalizza(testo: str) -> str:
    """Il testo per i duplicati: NFKC, minuscolo, solo lettere e cifre, spazi singoli."""
    t = unicodedata.normalize("NFKC", testo).casefold()
    t = "".join(ch if ch.isalnum() else " " for ch in t)
    return " ".join(t.split())


def motivo_scarto(testo: str) -> "str | None":
    """Perché un testo non può entrare nel repo, o None."""
    for nome, rx in SEGRETI:
        if rx.search(testo):
            return f"contiene un dato da non pubblicare ({nome})"
    return None


def split_di(id_messaggio: str) -> str:
    """Split stabile: sha256 dell'id, pari dev e dispari test."""
    return "dev" if int(hashlib.sha256(id_messaggio.encode("utf-8")).hexdigest(), 16) % 2 == 0 \
        else "test"


def settimana_di(oggi: str) -> str:
    a, s, _ = dt.date.fromisoformat(oggi).isocalendar()
    return f"{a}-W{s:02d}"


def _leggi(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _scrivi_json(p: Path, dati) -> None:
    """Scrittura atomica, nella forma del set d'oro (indent 1, a capo finale)."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=f".{p.name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(dati, ensure_ascii=False, indent=1) + "\n")
    os.replace(tmp, p)


def _catena(agente: str) -> "list[str]":
    return list(ia.CATENE.get(agente, ()))


def _settimane(coda: Path) -> "list[Path]":
    return sorted(Path(coda).glob("[0-9][0-9][0-9][0-9]-W[0-9][0-9].json"))


def _alternative(consigliata: "str | None", proposta: str, secondo: "str | None") -> dict:
    opzioni = []
    for o in (consigliata, proposta, secondo, NESSUNO):
        if o and o not in opzioni:
            opzioni.append(o)
    # senza consigliata le opzioni sono tutte alternative: nessuna è messa avanti
    alt = opzioni[1:] if consigliata else opzioni
    return {"alternative": alt, "catene": {o: _catena(o) for o in opzioni}}


def _opzioni(testo: str, tipo: str, scegli_, voti_) -> dict:
    proposta = ia.predici(testo, scegli_)
    v = voti_(testo)
    ordine = sorted(v, key=lambda a: (-v[a], ia.PRIORITA.index(a) if a in ia.PRIORITA else 99))
    # Un avviso del coordinatore o un resoconto di sottoagente non chiede lavoro (R4 di
    # ADR-0154). Per i messaggi del DM la consigliata NON è la predizione dell'hook: sarebbe
    # ancoraggio, perché la card mostrerebbe a Jfs proprio ciò che si misura. La mette
    # l'annotatore cieco con ``annota``; fino ad allora resta vuota.
    consigliata = None if tipo == "dm" else NESSUNO
    secondo = next((a for a in ordine if a not in (proposta, consigliata)), None)
    return {"proposta": proposta, "consigliata": consigliata, "secondo": secondo,
            **_alternative(consigliata, proposta, secondo)}


def _valida_in(messaggi) -> None:
    if not isinstance(messaggi, list):
        raise ValueError("IN.json dev'essere un elenco di messaggi")
    for i, m in enumerate(messaggi):
        if not isinstance(m, dict):
            raise ValueError(f"messaggio {i}: non è un oggetto")
        manca = [k for k in CAMPI_IN if k not in m]
        if manca:
            raise ValueError(f"messaggio {i}: mancano {', '.join(manca)}")
        if m["tipo"] not in TIPI:
            raise ValueError(f"messaggio {i}: tipo «{m['tipo']}» non è fra {', '.join(TIPI)}")
        dt.date.fromisoformat(str(m["data"]))


def proponi(ingresso: Path, coda: Path, oro: Path = ia.ORO, oggi: "str | None" = None,
            scegli_=None, voti_=None) -> dict:
    """Le proposte della settimana; solleva ValueError su un ingresso malformato."""
    scegli_ = scegli_ or ia.scegli
    voti_ = voti_ or ia.voti
    oggi = oggi or dt.date.today().isoformat()
    messaggi = _leggi(ingresso)
    _valida_in(messaggi)
    coda = Path(coda)
    casi_oro = _leggi(oro)["casi"]
    testi_oro = {normalizza(c["testo"]) for c in casi_oro}
    id_oro = {c["id_messaggio"] for c in casi_oro if c.get("id_messaggio")}
    testi_coda: "set[str]" = set()
    id_coda: "set[str]" = set()
    for p in _settimane(coda):
        for c in _leggi(p).get("casi", []):
            testi_coda.add(normalizza(c["testo"]))
            id_coda.add(c["id_messaggio"])
    nome = settimana_di(oggi)
    p_sett = coda / f"{nome}.json"
    sett = _leggi(p_sett) if p_sett.exists() else {
        "settimana": nome,
        "nota": "Casi da confermare per il set d'oro degli agenti (ADR-0154). «proposta» è la "
                "predizione dell'hook; «consigliata» la mette un annotatore cieco, che non vede "
                "la proposta (raccogli_casi_agenti.py cieco e annota), ed è «nessuno» per gli "
                "avvisi del coordinatore e i resoconti dei sottoagenti. Si conferma con "
                "raccogli_casi_agenti.py applica.",
        "casi": []}
    proposti, scartati = [], []
    visti_id, visti_testo = set(), set()
    for m in messaggi:
        id_, testo = str(m["id_messaggio"]), str(m["testo"])
        chiave = normalizza(testo)
        motivo = None
        if not chiave:
            motivo = "testo vuoto"
        elif id_ in id_oro or chiave in testi_oro:
            motivo = "già nel set d'oro"
        elif id_ in id_coda or chiave in testi_coda:
            motivo = "già in coda"
        elif id_ in visti_id or chiave in visti_testo:
            motivo = "duplicato nell'ingresso"
        else:
            motivo = motivo_scarto(testo)
        visti_id.add(id_)
        if chiave:
            visti_testo.add(chiave)
        if motivo:
            scartati.append({"id_messaggio": id_, "motivo": motivo})
            continue
        caso = {"id_messaggio": id_, "data": str(m["data"]), "fonte": str(m["fonte"]),
                "tipo": m["tipo"], "testo": testo.strip()}
        caso.update(_opzioni(testo, m["tipo"], scegli_, voti_))
        caso["stato"] = "da confermare"
        proposti.append(caso)
    sett["casi"].extend(proposti)
    _scrivi_json(p_sett, sett)
    (coda / "CARD.md").write_text(card(sett), encoding="utf-8")
    print(f"{len(proposti)} casi proposti in {p_sett}, {len(scartati)} scartati")
    for s in scartati:
        print(f"  scartato {s['id_messaggio']}: {s['motivo']}")
    return {"proposti": proposti, "scartati": scartati, "settimana": str(p_sett)}


def _abbrevia(testo: str, n: int = ABBREVIA) -> str:
    t = " ".join(testo.split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _riga_catena(o: str, catene: dict) -> str:
    c = catene.get(o) or []
    return " → ".join(c) if c else "nessuna catena"


def card(sett: dict) -> str:
    """Il testo da cui la routine pubblica una card per caso, con la consigliata."""
    da = [c for c in sett["casi"] if c.get("stato") == "da confermare"]
    r = [f"# Casi da confermare · settimana {sett['settimana']}", "",
         "Una card per caso (ADR-0154): la domanda è «quale agente doveva chiamare questo "
         "messaggio?», le opzioni sono la consigliata e le alternative, più «togli» se il "
         "caso non si etichetta. Le risposte vanno in SCELTE.tsv, poi "
         "`python3 scripts/raccogli_casi_agenti.py applica "
         f"{sett['settimana']}.json SCELTE.tsv`.", "",
         "La consigliata viene da un annotatore cieco, che ha letto il testo e le regole della "
         "cascata senza vedere la proposta dell'hook. Un caso «da annotare» non ha ancora "
         "una consigliata.", ""]
    if not da:
        r += ["Nessun caso da confermare.", ""]
    for i, c in enumerate(da, 1):
        r += [f"## {i} · {c['id_messaggio']}", "",
              f"{c['fonte']} · {c['data']} · {c['tipo']}", "",
              "> " + _abbrevia(c["testo"]), "",
              (f"- **Consigliata: {c['consigliata']}** · catena: "
               f"{_riga_catena(c['consigliata'], c['catene'])}" if c.get("consigliata")
               else "- **Consigliata: da annotare** (manca l'annotatore cieco)"),
              f"- Proposta dell'hook: {c['proposta']}"]
        for a in c["alternative"]:
            r.append(f"- Alternativa: {a} · catena: {_riga_catena(a, c['catene'])}")
        r.append("")
    r += ["## Modello di SCELTE.tsv", "", "```tsv", "id_messaggio\tatteso\taccettabili\tazione"]
    r += [f"{c['id_messaggio']}\t{c.get('consigliata') or ''}\t\ttieni" for c in da]
    r += ["```", ""]
    return "\n".join(r)


def _da_annotare(sett: dict) -> "list[dict]":
    return [c for c in sett["casi"] if c.get("stato") == "da confermare" and c["tipo"] == "dm"]


def cieco(settimana: Path) -> Path:
    """Scrive per l'annotatore cieco id e testo dei casi del DM, senza la proposta dell'hook."""
    settimana = Path(settimana)
    sett = _leggi(settimana)
    uscita = settimana.with_name(f"CIECO-{settimana.stem}.tsv")
    righe = ["id_messaggio\ttesto"]
    righe += [f"{c['id_messaggio']}\t{' '.join(c['testo'].split())}" for c in _da_annotare(sett)]
    uscita.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print(f"{len(righe) - 1} casi da annotare alla cieca in {uscita}: l'annotatore legge "
          f"solo questo file e GUIDA-AGENTI-E-CASCATE, poi scrive id_messaggio<TAB>etichetta")
    return uscita


def annota(settimana: Path, annotazioni: Path) -> int:
    """La consigliata dall'annotatore cieco; stampa l'accordo con l'hook. 1 se non torna."""
    import eval_metriche as em
    settimana = Path(settimana)
    sett = _leggi(settimana)
    per_id = {c["id_messaggio"]: c for c in sett["casi"] if c.get("stato") == "da confermare"}
    errori, scelte = [], {}
    for n, riga in enumerate(Path(annotazioni).read_text(encoding="utf-8").splitlines(), 1):
        campi = [x.strip() for x in riga.split("\t")]
        if not campi[0] or (n == 1 and campi[0] == "id_messaggio"):
            continue
        if len(campi) < 2 or campi[1] not in ETICHETTE:
            errori.append(f"riga {n}: etichetta «{campi[1] if len(campi) > 1 else ''}» "
                          f"non è un agente né «{NESSUNO}»")
        elif campi[0] not in per_id:
            errori.append(f"riga {n}: «{campi[0]}» non è un caso da confermare")
        else:
            scelte[campi[0]] = campi[1]
    if errori:
        print("\n".join(f"✗ annota: {e}" for e in errori))
        return 1
    for id_, etichetta in scelte.items():
        c = per_id[id_]
        c["consigliata"], c["annotatore"] = etichetta, "cieco"
        c.update(_alternative(etichetta, c["proposta"], c.get("secondo")))
    _scrivi_json(settimana, sett)
    settimana.with_name("CARD.md").write_text(card(sett), encoding="utf-8")
    if scelte:
        cieche = list(scelte.values())
        hook = [per_id[i]["proposta"] for i in scelte]
        k = sum(a == b for a, b in zip(cieche, hook))
        kappa = em.kappa_cohen(cieche, hook)
        print(f"{len(scelte)} consigliate dall'annotatore cieco; accordo hook-cieco "
              f"{k}/{len(scelte)}, kappa di Cohen {kappa:.3f}")
    return 0


def _leggi_scelte(p: Path) -> "list[tuple[str, str, list[str], str]]":
    righe = []
    for n, riga in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        col = riga.split("\t")
        if col[0].strip() == "id_messaggio":
            continue
        if len(col) != 4:
            raise ValueError(f"SCELTE riga {n}: servono 4 colonne separate da tab, sono {len(col)}")
        id_, atteso, acc, azione = (x.strip() for x in col)
        accettabili = [a.strip() for a in acc.split(",") if a.strip() and a.strip() != "-"]
        righe.append((id_, atteso, accettabili, azione))
    return righe


def _misura(percorso: Path, scegli_) -> dict:
    v = ia.valuta(percorso, scegli_, campioni=0)
    return {s: {"n": v[s]["n"], "giusti": v[s]["giusti"],
                "giusti_indulgenti": v[s]["giusti_indulgenti"],
                "macro_f1": v[s]["macro_f1"]["frazione"]} for s in ia.SPLIT}


def _riga_misura(m: dict) -> str:
    return (f"giusti {m['giusti']}/{m['n']}, indulgenti {m['giusti_indulgenti']}/{m['n']}, "
            f"macro-F1 {m['macro_f1']}")


def applica(settimana: Path, scelte: Path, oro: Path = ia.ORO, oggi: "str | None" = None,
            scegli_=None) -> int:
    scegli_ = scegli_ or ia.scegli
    oggi = oggi or dt.date.today().isoformat()
    settimana, oro = Path(settimana), Path(oro)
    sett = _leggi(settimana)
    dati = _leggi(oro)
    per_id = {c["id_messaggio"]: c for c in sett["casi"]}
    errori = []
    try:
        righe = _leggi_scelte(scelte)
    except ValueError as e:
        errori, righe = [str(e)], []
    for id_, atteso, acc, azione in righe:
        if id_ not in per_id:
            errori.append(f"{id_}: non è nella settimana {settimana.name}")
        if azione not in AZIONI:
            errori.append(f"{id_}: azione «{azione}» non è tieni o togli")
        if azione == "tieni":
            if atteso not in ETICHETTE:
                errori.append(f"{id_}: atteso «{atteso}» non è un agente né «nessuno»")
            for a in acc:
                if a not in ETICHETTE:
                    errori.append(f"{id_}: accettabile «{a}» non è un agente né «nessuno»")
            if atteso in acc:
                errori.append(f"{id_}: l'atteso «{atteso}» è anche fra gli accettabili")
    if errori:
        print("\n".join(f"✗ {e}" for e in errori), file=sys.stderr)
        print("niente scritto", file=sys.stderr)
        return 1
    id_oro = {c.get("id_messaggio") for c in dati["casi"]}
    testi_oro = {normalizza(c["testo"]) for c in dati["casi"]}
    nuovi, tolti = [], []
    for id_, atteso, acc, azione in righe:
        c = per_id[id_]
        if c.get("stato") != "da confermare" or id_ in id_oro:
            continue
        if azione == "togli":
            c["stato"] = "tolto"
            tolti.append(id_)
            continue
        if normalizza(c["testo"]) in testi_oro:
            c["stato"] = "tolto"
            tolti.append(id_)
            continue
        nuovi.append({"data": c["data"], "fonte": c["fonte"], "tipo": c["tipo"],
                      "testo": c["testo"], "atteso": atteso, "accettabili": acc,
                      "annotatore_b": None, "split": split_di(id_), "id_messaggio": id_})
        c["stato"] = "applicato"
    prima = _misura(oro, scegli_)
    if nuovi:
        dati["casi"].extend(nuovi)
        if NOTA_HASH.strip() not in dati.get("nota", ""):
            dati["nota"] = dati.get("nota", "") + NOTA_HASH
        fd, tmp = tempfile.mkstemp(dir=oro.parent, prefix=".oro.", suffix=".json")
        os.close(fd)
        tmp = Path(tmp)
        try:
            _scrivi_json(tmp, dati)
            dopo = _misura(tmp, scegli_)["test"]
            t = dati.setdefault("tetto", {})
            p = prima["test"]
            t["giusti"] = dopo["giusti"]
            t["giusti_indulgenti"] = dopo["giusti_indulgenti"]
            t["macro_f1"] = dopo["macro_f1"]
            base = _RIMESSA.sub("", t.get("nota", ""))
            t["nota"] = (base + f" Ultima rimessa (raccogli_casi_agenti.py applica): "
                         f"{oggi}, entrati {len(nuovi)} casi confermati da Jfs; è cambiato il "
                         f"set, non l'hook (prima sul test giusti {p['giusti']}/{p['n']}, "
                         f"indulgenti {p['giusti_indulgenti']}/{p['n']}, macro-F1 "
                         f"{p['macro_f1']}). Il tetto si rimette solo con applica, che misura "
                         f"l'hook invariato sul set nuovo: a mano non si abbassa.")
            _scrivi_json(tmp, dati)
            err = controlla_forma(tmp)
            if err:
                print("\n".join(f"✗ {e}" for e in err), file=sys.stderr)
                print("niente scritto", file=sys.stderr)
                return 1
            os.replace(tmp, oro)
        finally:
            tmp.unlink(missing_ok=True)
    _scrivi_json(settimana, sett)
    (settimana.parent / "CARD.md").write_text(card(sett), encoding="utf-8")
    finale = _misura(oro, scegli_)
    print(f"entrati {len(nuovi)} casi, tolti {len(tolti)}; tetto "
          f"{'rimesso' if nuovi else 'invariato'}")
    for s in ia.SPLIT:
        print(f"  {s:<5} prima: {_riga_misura(prima[s])}")
        print(f"  {s:<5} dopo:  {_riga_misura(finale[s])}")
    if nuovi:
        print("Aggiorna i numeri di test_oro_del_repo_numeri_di_oggi "
              "(scripts/tests/test_instradamento_agenti.py) con la riga «test dopo».")
    return 0


def _data_ok(v) -> bool:
    if not isinstance(v, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return False
    try:
        dt.date.fromisoformat(v)
    except ValueError:
        return False
    return True


def controlla_forma(percorso: Path = ia.ORO) -> "list[str]":
    """I difetti di forma del set d'oro; vuoto se va."""
    try:
        dati = _leggi(percorso)
    except (OSError, json.JSONDecodeError) as e:
        return [f"set d'oro illeggibile: {e}"]
    errori = []
    if not isinstance(dati, dict) or not isinstance(dati.get("casi"), list):
        return ["il set d'oro dev'essere un oggetto con l'elenco «casi»"]
    tetto = dati.get("tetto")
    if not isinstance(tetto, dict) or any(k not in tetto for k in CAMPI_TETTO):
        errori.append(f"tetto mancante o senza {', '.join(CAMPI_TETTO)}")
    testi: "dict[str, int]" = {}
    ids: "dict[str, int]" = {}
    for i, c in enumerate(dati["casi"], 1):
        dove = f"caso {i}"
        if not isinstance(c, dict):
            errori.append(f"{dove}: non è un oggetto")
            continue
        for k in CAMPI_CASO:
            if k not in c:
                errori.append(f"{dove}: manca il campo {k}")
        testo = c.get("testo")
        if not isinstance(testo, str) or not normalizza(testo):
            errori.append(f"{dove}: testo vuoto")
        else:
            chiave = normalizza(testo)
            if chiave in testi:
                errori.append(f"{dove}: testo duplicato del caso {testi[chiave]}")
            testi.setdefault(chiave, i)
            m = motivo_scarto(testo)
            if m:
                errori.append(f"{dove}: il testo {m}")
        if "split" in c and c["split"] not in SPLIT_OK:
            errori.append(f"{dove}: split «{c['split']}» non è dev o test")
        if "tipo" in c and c["tipo"] not in TIPI:
            errori.append(f"{dove}: tipo «{c['tipo']}» non è fra {', '.join(TIPI)}")
        if "data" in c and not _data_ok(c["data"]):
            errori.append(f"{dove}: data «{c['data']}» non è AAAA-MM-GG")
        if "atteso" in c and c["atteso"] not in ETICHETTE:
            errori.append(f"{dove}: atteso «{c['atteso']}» non è un agente né «nessuno»")
        acc = c.get("accettabili", [])
        if not isinstance(acc, list) or any(a not in ETICHETTE for a in acc):
            errori.append(f"{dove}: accettabili non è un elenco di agenti")
        elif c.get("atteso") in acc:
            errori.append(f"{dove}: accettabili contiene l'atteso")
        b = c.get("annotatore_b")
        if b is not None and b not in ETICHETTE:
            errori.append(f"{dove}: annotatore_b «{b}» non è un agente né «nessuno»")
        id_ = c.get("id_messaggio")
        if id_ is not None:
            if id_ in ids:
                errori.append(f"{dove}: id_messaggio duplicato del caso {ids[id_]}")
            ids.setdefault(id_, i)
            if c.get("split") in SPLIT_OK and c["split"] != split_di(str(id_)):
                errori.append(f"{dove}: split «{c['split']}» diverso da quello dell'hash "
                              f"dell'id_messaggio")
    return errori


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="la forma del set d'oro: esce 1 se non va")
    ap.add_argument("--oro", type=Path, default=ia.ORO, help="il set d'oro")
    sub = ap.add_subparsers(dest="comando")
    comuni = argparse.ArgumentParser(add_help=False)
    comuni.add_argument("--oro", type=Path, default=argparse.SUPPRESS, help="il set d'oro")
    comuni.add_argument("--oggi", default=None, help="la data di oggi, AAAA-MM-GG")
    p = sub.add_parser("proponi", parents=[comuni], help="le proposte della settimana")
    p.add_argument("ingresso", type=Path, help="IN.json, i messaggi esportati dalla routine")
    p.add_argument("--coda", type=Path, required=True, help="la cartella della coda")
    c_ = sub.add_parser("cieco", help="id e testo per l'annotatore cieco, senza la proposta")
    c_.add_argument("settimana", type=Path, help="DIR/AAAA-Www.json")
    n_ = sub.add_parser("annota", help="le consigliate dall'annotatore cieco")
    n_.add_argument("settimana", type=Path, help="DIR/AAAA-Www.json")
    n_.add_argument("annotazioni", type=Path, help="id_messaggio<TAB>etichetta")
    a_ = sub.add_parser("applica", parents=[comuni], help="i casi confermati nel set d'oro")
    a_.add_argument("settimana", type=Path, help="DIR/AAAA-Www.json")
    a_.add_argument("scelte", type=Path, help="SCELTE.tsv")
    a = ap.parse_args(argv)
    if a.check:
        errori = controlla_forma(a.oro)
        if errori:
            print("\n".join(f"✗ raccogli_casi_agenti: {e}" for e in errori))
            return 1
        n = len(_leggi(a.oro)["casi"])
        print(f"✓ raccogli_casi_agenti: set d'oro in forma, {n} casi")
        return 0
    if a.comando == "proponi":
        try:
            proponi(a.ingresso, a.coda, oro=a.oro, oggi=a.oggi)
        except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
            print(f"ingresso malformato: {e}", file=sys.stderr)
            return 2
        return 0
    if a.comando == "cieco":
        cieco(a.settimana)
        return 0
    if a.comando == "annota":
        return annota(a.settimana, a.annotazioni)
    if a.comando == "applica":
        return applica(a.settimana, a.scelte, oro=a.oro, oggi=a.oggi)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
