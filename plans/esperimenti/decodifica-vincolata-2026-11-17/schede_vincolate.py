#!/usr/bin/env python3
"""schede_vincolate.py — la decodifica vincolata misurata sulle «Tattiche» delle schede.

La tecnica 3 del thread «Applicare Document AI e Explainable AI» (PIANO.md qui
accanto). genera_creatura.py fa già i numeri giusti da tabelle; quello che un
modello locale sbaglia è il testo che rimanda alla scheda: le tattiche nominano
un incantesimo o un talento che la creatura non ha. Il controllo S8 di
coerenza_campagna.py lo trova; qui si misura se il vincolo lo previene.

Due bracci, stesso modello, stesse schede, stesso seme per ripetizione:
  libero     il modello scrive le tattiche in Markdown;
  vincolato  il modello risponde col campo `format` di Ollama, uno schema JSON
             in cui l'azione di ogni passo è un enum delle voci della scheda
             (incantesimi, talenti, attacchi) più poche azioni comuni; lo
             script la scrive in Markdown.
Poi S8 su ogni scheda (verifica_tattiche, la stessa funzione del cancello) e un
secondo conto che non dipende dal corsivo: i nomi di incantesimi e talenti del
plugin dnd35 che compaiono nelle tattiche e non nella scheda.

Solo stdlib, più gli script del repo. Le risposte si salvano a ogni scheda:
una corsa interrotta riparte da dove era.

  python3 schede_vincolate.py --modello qwen2.5:7b --out DIR [--ripetizioni 3]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parent.parent.parent
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))

# Dodici PNG umanoidi a semi fissi: sette classi da incantatore e due marziali,
# GS 4-12. Le schede sono di genera_creatura.py, quindi i numeri tornano per
# costruzione e la prova guarda solo le tattiche.
CAMPIONE = [
    ("mago:7", 7, "controllore", 11), ("chierico:8", 8, "controllore", 3),
    ("stregone:9", 9, "blaster", 5), ("druido:6", 6, "controllore", 7),
    ("bardo:8", 8, "comandante", 5), ("ranger:8", 8, "schermagliatore", 5),
    ("paladino:10", 10, "bruto", 5), ("guerriero:8", 8, "bruto", 5),
    ("mago:12", 12, "blaster", 2), ("chierico:5", 5, "comandante", 9),
    ("stregone:6", 6, "controllore", 4), ("guerriero:4", 4, "tiratore", 6),
]
AZIONI_COMUNI = ["avanzare", "ritirarsi", "combattere sulla difensiva", "prendere copertura",
                 "proteggere un alleato", "fuggire", "arrendersi"]
FASI = [("prima", "Prima del combattimento"), ("durante", "Durante il combattimento"),
        ("morale", "Morale")]
SISTEMA = ("Sei un Dungeon Master esperto di D&D 3.5. Scrivi le tattiche di una creatura "
           "in italiano, usando SOLO gli incantesimi, i talenti e gli attacchi della sua scheda.")
# Tetto dei token della risposta. Il vincolato al massimo sono 12 passi da ~90 token
# (azione, bersaglio fino a 60 caratteri, perché fino a 140): con 700 un JSON pieno
# si troncava e la risposta contava come non valida per colpa del tetto, non del modello.
GETTONI = 1500
VERDETTO = ("migliora se, sulle stesse schede: (1) il vincolato ha meno violazioni S8 per scheda "
            "del libero, (2) tutte le sue risposte sono valide, (3) la sua copertura delle voci "
            "della scheda è almeno l'80% di quella del libero e almeno 1 voce per risposta")


def _dividi(testo: str) -> list[str]:
    """Divide sulle virgole fuori dalle parentesi: «Incantesimi focalizzati (bene, caos)»."""
    out, liv, cur = [], 0, ""
    for c in testo:
        liv += (c == "(") - (c == ")")
        if c == "," and liv == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += c
    if cur.strip():
        out.append(cur.strip())
    return [x for x in out if x]


def voci(blocco: str) -> dict:
    """Incantesimi, talenti e attacchi scritti nel blocco di genera_creatura."""
    inc, tal, att = [], [], []
    for r in blocco.splitlines():
        r = r.strip().lstrip("- ").strip()
        m = re.match(r"(?:Preparati|Conosciuti)\s+—\s+(.*)", r)
        if m:
            for liv in m.group(1).split("·"):
                inc += _dividi(re.sub(r"^\s*\d+°:\s*", "", liv))
        elif r.startswith("Talenti:"):
            tal = _dividi(r.split(":", 1)[1])
        else:
            m = re.match(r"(Mischia|Distanza)\s+(.+?)\s+[+-]\d", r)
            if m:
                att.append(f"attacco con {m.group(2)}")
    return {"incantesimi": list(dict.fromkeys(inc)), "talenti": tal, "attacchi": att}


def genera(classe: str, gs: int, ruolo: str, seme: int) -> str:
    r = subprocess.run([sys.executable, str(SCRIPTS / "genera_creatura.py"), "--gs", str(gs),
                        "--tipo", "umanoide", "--classe", classe, "--ruolo", ruolo,
                        "--seed", str(seme), "--json"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)[0]["blocco"]


def schema(v: dict) -> dict:
    azioni = v["incantesimi"] + v["talenti"] + v["attacchi"] + AZIONI_COMUNI
    passo = {"type": "object", "additionalProperties": False,
             "required": ["azione", "bersaglio", "perche"],
             "properties": {"azione": {"type": "string", "enum": azioni},
                            "bersaglio": {"type": "string", "maxLength": 60},
                            "perche": {"type": "string", "maxLength": 140}}}
    return {"type": "object", "additionalProperties": False, "required": [k for k, _ in FASI],
            "properties": {k: {"type": "array", "minItems": 1, "maxItems": 4, "items": passo}
                           for k, _ in FASI}}


def prompt(blocco: str, vincolato: bool) -> str:
    base = (f"Scheda:\n{blocco}\n\nScrivi le tattiche in tre fasi: prima del combattimento, "
            "durante il combattimento, morale (quando fugge o si arrende). ")
    if vincolato:
        return base + ("Rispondi in JSON: per ogni fase da 1 a 4 passi, ognuno con l'azione "
                       "scelta fra quelle permesse, il bersaglio e il perché in una frase.")
    return base + ("Rispondi solo con tre righe Markdown, così:\n"
                   "- *Prima del combattimento*: ...\n- *Durante il combattimento*: ...\n"
                   "- *Morale*: ...\nScrivi gli incantesimi in corsivo, come *dissolvi magie*.")


def chiedi(url: str, modello: str, utente: str, seme: int, fmt: dict | None, timeout: float) -> dict:
    corpo = {"model": modello, "stream": False,
             "messages": [{"role": "system", "content": SISTEMA}, {"role": "user", "content": utente}],
             "options": {"temperature": 0.7, "seed": seme, "num_predict": GETTONI}}
    if fmt is not None:
        corpo["format"] = fmt
    req = urllib.request.Request(f"{url}/api/chat", data=json.dumps(corpo).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        # Un Ollama più vecchio della 0.5 rifiuta lo schema nel campo `format`
        raise SystemExit(f"ERRORE: Ollama risponde {e.code} a /api/chat: "
                         f"{e.read().decode('utf-8', 'replace')[:300]}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise SystemExit(f"ERRORE: Ollama non ha risposto entro {timeout:.0f} s ({e}). "
                         "Le risposte già avute sono salvate: rilancia la prova.") from e
    return {"testo": d["message"]["content"], "secondi": round(time.time() - t0, 2),
            "token": d.get("eval_count"), "ns": d.get("eval_duration"),
            "fine": d.get("done_reason")}


def in_markdown(testo: str, v: dict) -> tuple[str | None, str]:
    """Le tattiche del vincolato in Markdown; None e il motivo se il JSON non va."""
    try:
        d = json.loads(testo)
    except json.JSONDecodeError as e:
        return None, f"JSON non valido: {e.msg}"
    permesse = set(v["incantesimi"] + v["talenti"] + v["attacchi"] + AZIONI_COMUNI)
    righe = []
    for k, titolo in FASI:
        passi = d.get(k) if isinstance(d, dict) else None
        if not isinstance(passi, list) or not passi:
            return None, f"manca la fase «{k}»"
        frasi = []
        for p in passi:
            a = p.get("azione") if isinstance(p, dict) else None
            if not isinstance(a, str) or a not in permesse:
                return None, f"azione fuori dallo schema: {a!r}"
            ber, per = p.get("bersaglio", ""), p.get("perche", "")
            if not isinstance(ber, str) or not isinstance(per, str):
                return None, "bersaglio o perché non sono testo"
            # Su una riga sola: un a capo nel testo libero spezzerebbe la voce dell'elenco
            ber, per = " ".join(ber.split()), " ".join(per.split())
            nome = f"*{a}*" if a in v["incantesimi"] else a
            frasi.append(f"{nome} su {ber}: {per}" if ber else f"{nome}: {per}")
        righe.append(f"- *{titolo}*: " + "; ".join(frasi) + ".")
    return "\n".join(righe), ""


def valido_libero(testo: str) -> tuple[str | None, str]:
    """Tutto quello che il modello ha scritto, una voce d'elenco per riga. Si
    tolgono solo i segni che nasconderebbero il testo a S8: titoli, numeri
    d'elenco, recinti di codice e il grassetto (che `verifica_scheda` legge come
    l'inizio di un'altra sezione, e le tattiche finirebbero lì). Il corsivo resta
    com'è. Così il libero non perde violazioni per come ha impaginato."""
    righe = []
    for r in testo.splitlines():
        r = r.strip()
        if not r or r.startswith("```"):
            continue
        r = re.sub(r"^(?:#+\s*|\d+[.)]\s+|[-•]\s+|\*\s+)+", "", r)
        r = re.sub(r"\*\*|__", "*", r).strip()
        if r.strip("*: "):
            righe.append(f"- {r}")
    if not righe:
        return None, "risposta vuota"
    return "\n".join(righe), ""


def _pt(t: str) -> str:
    import coerenza_campagna as C
    return C._piatto(t)


def fuori_lista(tattiche: str, v: dict) -> list[str]:
    """Il conto che non dipende dal corsivo: nomi del plugin dnd35 (incantesimi in
    italiano di due parole o 9 lettere, talenti di più parole) che le tattiche
    nominano e la scheda no. Gli incantesimi di una parola sotto le 9 lettere
    («luce», «sonno», «comando») restano fuori apposta: sono anche parole comuni
    e darebbero falsi allarmi. Questo conto quindi non li vede, se non in corsivo."""
    import lessico_regole as LR
    import verifica_scheda as VS
    import verifica_talenti as VT
    it, nomi = VS._incantesimi_it(), VS._liste("dnd35")[2]
    ha_inc = {it.get(LR.norma(x), nomi.get(LR.norma(x))) for x in v["incantesimi"]}
    ha_tal = {(VT.risolvi("dnd35", x) or {}).get("en") for x in v["talenti"]}
    t = _pt(tattiche)
    out = []
    for k, en in it.items():
        if (" " in k or len(k) >= 9) and f" {k} " in t and en not in ha_inc:
            out.append(f"incantesimo {k}")
    for k in VT._lessici()[0]:
        if " " in k and f" {k} " in t:
            x = VT.risolvi("dnd35", k)
            if x and x["en"] not in ha_tal:
                out.append(f"talento {k}")
    return sorted(set(out))


def copertura(tattiche: str, v: dict) -> int:
    t = _pt(tattiche)
    return sum(1 for x in v["incantesimi"] + v["talenti"] if _pt(re.sub(r"\(.*?\)", "", x)) in t)


def riassumi(righe: list[dict]) -> dict:
    out = {}
    for b in ("libero", "vincolato"):
        rr = [r for r in righe if r["braccio"] == b]
        ok = [r for r in rr if r["valida"]]
        n = len(rr) or 1
        out[b] = {"risposte": len(rr), "valide": len(ok),
                  "violazioni_s8": sum(r["s8"] for r in ok),
                  "s8_per_scheda": round(sum(r["s8"] for r in ok) / (len(ok) or 1), 3),
                  "schede_con_s8": sum(1 for r in ok if r["s8"]),
                  "troncate": sum(1 for r in rr if r.get("troncata")),
                  "fuori_lista": sum(len(r["fuori_lista"]) for r in ok),
                  "menzioni_s8": sum(r["menzioni"] for r in ok),
                  "copertura_media": round(sum(r["copertura"] for r in ok) / (len(ok) or 1), 2),
                  "secondi_medi": round(sum(r["secondi"] for r in rr) / n, 2),
                  "token_al_secondo": round(sum(r["token"] or 0 for r in rr)
                                            / ((sum(r["ns"] or 0 for r in rr) / 1e9) or 1), 1)}
    lib, vin = out["libero"], out["vincolato"]
    out["migliora"] = bool(vin["s8_per_scheda"] < lib["s8_per_scheda"]
                           and vin["valide"] == vin["risposte"]
                           and vin["copertura_media"] >= max(0.8 * lib["copertura_media"], 1.0))
    out["regola"] = VERDETTO
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modello", default="qwen2.5:7b")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--url", default="http://127.0.0.1:11434")
    ap.add_argument("--ripetizioni", type=int, default=3)
    ap.add_argument("--quante", type=int, default=len(CAMPIONE), help="le prime N schede del campione")
    ap.add_argument("--timeout", type=float, default=600)
    a = ap.parse_args(argv)
    import coerenza_campagna as C

    a.out.mkdir(parents=True, exist_ok=True)
    cache_p = a.out / "risposte.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    righe = []
    for i, (classe, gs, ruolo, seme) in enumerate(CAMPIONE[:a.quante]):
        blocco = genera(classe, gs, ruolo, seme)
        v = voci(blocco)
        sid = f"{i + 1:02d}-{classe.replace(':', '')}"
        for rip in range(a.ripetizioni):
            for b in ("libero", "vincolato"):
                k = f"{a.modello}|{sid}|{b}|{rip}"
                if k not in cache:
                    cache[k] = chiedi(a.url, a.modello, prompt(blocco, b == "vincolato"), rip,
                                      schema(v) if b == "vincolato" else None, a.timeout)
                    cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
                r = cache[k]
                tatt, motivo = in_markdown(r["testo"], v) if b == "vincolato" else valido_libero(r["testo"])
                riga = {"scheda": sid, "braccio": b, "ripetizione": rip, "valida": tatt is not None,
                        "motivo": motivo, "secondi": r["secondi"], "token": r["token"], "ns": r["ns"],
                        "troncata": r.get("fine") == "length",
                        "s8": 0, "menzioni": 0, "violazioni": [], "fuori_lista": [], "copertura": 0}
                if tatt is not None:
                    f = a.out / b / f"{sid}-r{rip}.md"
                    f.parent.mkdir(exist_ok=True)
                    f.write_text(f"# {sid}\n\n{blocco}\n\n**Tattiche**\n{tatt}\n", encoding="utf-8")
                    s = C.verifica_tattiche([f])
                    riga.update(s8=len(s["violazioni"]), menzioni=s["letti"]["menzioni"],
                                violazioni=[x["atteso"] for x in s["violazioni"]],
                                fuori_lista=fuori_lista(tatt, v), copertura=copertura(tatt, v))
                righe.append(riga)
        print(f"  {sid}: fatto", file=sys.stderr, flush=True)
    sintesi = riassumi(righe)
    sintesi["modello"] = a.modello
    sintesi["ripetizioni"] = a.ripetizioni
    sintesi["schede"] = min(a.quante, len(CAMPIONE))
    (a.out / "misure.json").write_text(json.dumps({"sintesi": sintesi, "righe": righe},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(sintesi, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
