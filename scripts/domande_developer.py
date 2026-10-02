#!/usr/bin/env python3
"""domande_developer.py — le domande del developer, misurate sul testo.

`rumblingstone-module-standard/references/sviluppo-degli-incontri.md` tiene le
sette domande che nei colophon di Paizo e WotC fa il **developer** («si
gioca?»), prese dai due manuali del DM e controllate una per una
(`plans/RICERCA-MANUALE-DEL-MASTER-2026-09.md`). Fino a oggi erano domande che
si ricordava chi scriveva, e le letture a freddo. Questo script ne misura sei
sulla forma del testo, e dice **dove** il problema c'è.

| Regola | La domanda (§ del file di norma) | Unità che si guarda |
|---|---|---|
| D1 | il nemico vola: chi resta a terra cosa fa? (§1) | scena di scontro con un nemico in volo |
| D2 | e se volano? e se sono invisibili? e se sono silenziosi? (§2) | luogo sorvegliato |
| D3 | Tempra, Riflessi e Volontà negli scontri (§3) | il modulo intero |
| D4 | chi sente il rumore, e arriva? (§4) | luogo sorvegliato |
| D5 | il boss ha una soglia in cui cambia (§5) | scena del boss |
| D6 | lo skill challenge è scritto per intero (§6) | scena dello skill challenge |
| D6-5E | abilità 5e con una CD o un bonus (§6) | il modulo intero |

La §7 (i sette modi di stare al tavolo di Robin Laws) **non** si misura: è un
giudizio su chi si diverte, e lo chiede il playtester a freddo.

⚠️ **Sono indicatori, non sentenze.** Lo script vede la forma, non il
senso: «vola» nel testo non dice che il nemico *resta* in quota, e un luogo
con «quattro guardie» può essere una sala del trono. Per questo ogni rilievo
che non è un difetto si dichiara in `plans/domande-developer.json` con la sua
ragione, come fa `copertura_scene`, e un residuo che smette di verificarsi fa
fallire il cancello finché non lo si toglie.

Le scene si leggono con `copertura_scene` (stessi moduli, stessi profili) e le
CD con `componenti`: una norma, un rilevatore.

Uso:
    python3 scripts/domande_developer.py              # il rapporto, modulo per modulo
    python3 scripts/domande_developer.py --check      # cancello CI
    python3 scripts/domande_developer.py --file X.md  # un file qualunque, senza residui
    python3 scripts/domande_developer.py --json

Solo libreria standard. Exit code: 0 = ok · 1 = rilievi non dichiarati o
residui scaduti (--check).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import copertura_scene as cs  # noqa: E402
import componenti as comp  # noqa: E402

CONFIG = ROOT / "plans" / "domande-developer.json"

# ─── le forme ────────────────────────────────────────────────────────────────

_NUM = r"(?:\d+|due|tre|quattro|cinque|sei|sette|otto|dieci|dodici|venti|trenta)"
#: Un luogo sorvegliato: un gruppo contato di guardie, o chi fa la ronda.
#: «Sentinella» con la maiuscola è un nome di creatura (la Sentinella di Mithral
#: di DEF-1), e non conta: la forma è case-sensitive apposta.
SORVEGLIATO = re.compile(
    rf"\b{_NUM}\s+(?:guardie|sentinelle|vedette)\b|\bpattugli\w*|\bsentinell[ae]\b|\bvedett[ae]\b"
    r"|\bdi (?:guardia|ronda)\b|\bsorvegliat\w*")
VOLO = re.compile(r"(?i)\b(?:vol(?:a|ano|are|ando)|in volo|dall'alto|sorvol\w+|in quota|levitaz\w+)\b")
INVISIBILE = re.compile(r"(?i)\binvisibil\w*")
#: «e se sono silenziosi?»: il terzo modo di passare, con *silenzio* o Muoversi
#: Silenziosamente (DM, 2026-09-27: volo, invisibilità e silenzio insieme).
SILENZIO = re.compile(r"(?i)\bsilenzi\w*|muoversi silenziosamente|senza (?:un )?rumore|non fa(?:nno)? rumore")
RUMORE = re.compile(r"(?i)\b(?:allarme|sentono|sente\b|rumore|rinforzi|accorr\w+|corno|"
                    r"(?:entro|in) \w+ round|dà l'allarme|grida)")
SCONTRO = re.compile(r"\bIniziativa\b|\bEL\s*[≈~]?\s*\d|round di sorpresa|\bGS\s*\d+|\bCR\s*\d+")
NEMICO_IN_VOLO = re.compile(r"(?i)\b(?:resta in (?:volo|quota|aria)|in volo|in picchiata|"
                            r"vola\b|volano\b|dall'alto)")
#: La risposta per chi non vola va scritta come tale: «a terra» o «atterra»
#: compaiono in ogni scena lunga con un drago, e alla prima prova la forma larga
#: dichiarava risolta la Scena 11 di DEF-4 che il playtester (#35) aveva trovato
#: senza niente da fare per Tordek.
DA_TERRA = re.compile(r"(?i)chi (?:non vola|resta a terra|è a terra)|senza volo|non (?:vola|volano)\b[^.\n]{0,40}"
                      r"(?:può|possono|fa|fanno)|PG a terra|armi a distanza|(?:lo|la|li) costring\w+ a "
                      r"(?:scendere|atterrare)|(?:abbatterlo|tirarlo giù)|per chi non vola")
SOGLIA = re.compile(r"(?i)(?:\d+\s*pf\b|metà dei (?:suoi )?(?:pf|punti ferita)|un terzo (?:dei|di)|"
                    r"sotto (?:i|la metà|il)\b|quando (?:scende|arriva|resta)|al round \d|dal round \d|"
                    r"\besita\b|si ritira|\bfugge\b|cambia tattica|seconda fase|fase 2)")
BOSS_TITOLO = re.compile(r"(?i)\bboss\b")
#: «Scena 11: Skullcrusher (GS 12) | boss» o «(boss, Scena 11)»: il modulo che
#: dichiara da sé quale scena è il boss.
BOSS_DICHIARATO = re.compile(r"(?i)\bboss\b[^\n|]{0,20}Scena (\d+)|Scena (\d+)[^\n]{0,60}\|\s*boss\b")
SKILL_CHALLENGE = re.compile(r"(?im)^#+ .*skill challenge|\d+\s+successi prima di \d+\s+fallimenti"
                             r"|prova a tappe")
SC_QUANTI = re.compile(r"(?i)\b(?:\d+|tre|quattro|cinque|sei|otto)\s+(?:successi|blocchi)\b")
SC_FALLIMENTO = re.compile(r"(?i)\bfallimenti?\b|\bfallit[oa]\b")
SC_CHI = re.compile(r"(?i)prova di gruppo|tirano tutti|tutti e \w+ i PG|ogni PG|ognuno|ciascun\w* PG|"
                    r"contribuisc\w+|un PG solo")
SC_SUCCESSO = re.compile(r"(?i)\b(?:ogni|un|il) (?:successo|blocco)\b|\briesce se\b|\bsuccesso\s*\(|"
                         r"\*\*\d+ successi\*\*|successo pieno|\bSuccesso\b")
SC_COPPIA = re.compile(r"(\d+)\s+successi\s*(?:prima di|/)\s*(\d+)\s+fallimenti")
#: Le abilità che nel sistema del modulo non esistono. In PF1e Percezione,
#: Furtività e Intuizione ci sono (Perception, Stealth, Sense Motive): alla
#: prima prova il Drappo, che è PF1e, ne risultava pieno.
ABILITA_ESTRANEE = {"3.5": ("Atletica", "Intuizione", "Percezione", "Furtività"),
                    "pf1e": ("Atletica",)}


def _abilita_estranee(sistema: str) -> "re.Pattern":
    nomi = "|".join(ABILITA_ESTRANEE.get(sistema, ABILITA_ESTRANEE["3.5"]))
    return re.compile(rf"\b({nomi})\s*\**\s*(?:\(|CD\b|\+\d)")
TS = {"Tempra": re.compile(r"\bTempra\b\s*\**\s*(?:CD\s*)?\**\s*\d+"),
      "Riflessi": re.compile(r"\bRiflessi\b\s*\**\s*(?:CD\s*)?\**\s*\d+"),
      "Volontà": re.compile(r"\bVolontà\b\s*\**\s*(?:CD\s*)?\**\s*\d+")}


# ─── le regole ───────────────────────────────────────────────────────────────

def _scene_boss(testo: str, scene: "list[tuple[str, str]]") -> "set[str]":
    dichiarate = {n for m in BOSS_DICHIARATO.finditer(testo) for n in m.groups() if n}
    fuori = set()
    for titolo, _ in scene:
        chiave = cs.chiave_scena(titolo)
        numero = re.search(r"\d+", chiave)
        if BOSS_TITOLO.search(titolo) or (chiave.startswith("SCENA") and numero
                                          and numero.group(0) in dichiarate):
            fuori.add(chiave)
    return fuori


def analizza(testo: str, profilo: "dict | None" = None,
             con_ts: bool = True) -> "list[tuple[str, str, str]]":
    """(regola, scena, dettaglio) per ogni domanda senza risposta nel testo."""
    profilo = profilo or {}
    testo = cs.pulisci(testo)
    scene = cs.scene(testo, profilo.get("scena", cs.SCENA_DEF), profilo.get("escludi"))
    boss = _scene_boss(testo, scene)
    fuori: "list[tuple[str, str, str]]" = []

    for titolo, corpo in scene:
        k = cs.chiave_scena(titolo)
        guardie = SORVEGLIATO.findall(corpo)
        if len(guardie) >= 2:
            if not VOLO.search(corpo):
                fuori.append(("D2", k, "luogo sorvegliato: nessuna risposta a «e se volano?»"))
            if not INVISIBILE.search(corpo):
                fuori.append(("D2", k, "luogo sorvegliato: nessuna risposta a «e se sono invisibili?»"))
            if not SILENZIO.search(corpo):
                fuori.append(("D2", k, "luogo sorvegliato: nessuna risposta a «e se sono silenziosi?»"))
            if not RUMORE.search(corpo):
                fuori.append(("D4", k, "luogo sorvegliato: non dice chi sente il rumore e arriva"))
        if SCONTRO.search(corpo) and NEMICO_IN_VOLO.search(corpo) and not DA_TERRA.search(corpo):
            fuori.append(("D1", k, "scontro con un nemico in volo: niente per chi resta a terra"))
        if k in boss and not SOGLIA.search(corpo):
            fuori.append(("D5", k, "boss senza una soglia (pf, round, evento) in cui cambia"))
        if SKILL_CHALLENGE.search(corpo):
            mancano = [nome for nome, rx in (("quanti successi", SC_QUANTI), ("chi tira", SC_CHI),
                                              ("cosa vale un successo", SC_SUCCESSO),
                                              ("cosa costa un fallimento", SC_FALLIMENTO))
                       if not rx.search(corpo)]
            if not comp._prove(corpo):
                mancano.append("cosa si tira (nessuna CD)")
            if mancano:
                fuori.append(("D6", k, "skill challenge senza: " + ", ".join(mancano)))

    # D6 · la regola sta in un posto solo: numeri diversi per lo stesso challenge.
    coppie = sorted({m.groups() for m in SC_COPPIA.finditer(testo)})
    n_sc = sum(1 for _, c in scene if SKILL_CHALLENGE.search(c))
    if len(coppie) > max(1, n_sc):
        fuori.append(("D6", "—", "skill challenge con numeri diversi in punti diversi: "
                      + " · ".join(f"{s}/{f}" for s, f in coppie)))
    sistema = profilo.get("sistema", "3.5")
    for m in _abilita_estranee(sistema).finditer(testo):
        riga = testo.count("\n", 0, m.start()) + 1
        fuori.append(("D6-5E", f"r.{riga}", f"abilità «{m.group(1)}»: in {sistema} non esiste"))

    if con_ts:
        fuori += ts_mancanti(testo, profilo)
    return fuori


def ts_mancanti(testo: str, profilo: dict) -> "list[tuple[str, str, str]]":
    """D3 · il modulo intero; un modulo di rito dichiara i TS che vuole."""
    voluti = profilo.get("ts_voluti", list(TS))
    presenti = {nome for nome, rx in TS.items() if rx.search(testo)}
    return [("D3", "—", f"nessun effetto chiede un TS su {nome}")
            for nome in TS if nome in voluti and nome not in presenti]


# ─── il cancello ────────────────────────────────────────────────────────────

def carica_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def esegui(cfg: dict) -> "tuple[list, list, list]":
    """(tutti i rilievi, i non dichiarati, i residui scaduti)."""
    profili = cfg.get("profili", {})
    trovati = []
    #: Un modulo in più file (il Drappo, un giorno per file) conta i TS
    #: sull'insieme, e li riporta sul primo file del gruppo.
    gruppi: "dict[str, list]" = {}
    for mod in cs.moduli(cs.carica_config()):
        f = ROOT / mod["file"]
        if not f.exists():
            continue
        prof = {**mod, **profili.get(mod["file"], {})}
        testo = f.read_text(encoding="utf-8")
        gruppo = prof.get("modulo")
        for regola, scena, dettaglio in analizza(testo, prof, con_ts=not gruppo):
            trovati.append((mod["file"], regola, scena, dettaglio))
        if gruppo:
            gruppi.setdefault(gruppo, []).append((mod["file"], cs.pulisci(testo), prof))
    for membri in gruppi.values():
        insieme = "\n".join(t for _, t, _ in membri)
        for regola, scena, dettaglio in ts_mancanti(insieme, membri[0][2]):
            trovati.append((membri[0][0], regola, scena, dettaglio + " (sull'intero modulo)"))
    residui = cfg.get("residui", [])

    def dichiarato(t):
        return any(t[0] == r["file"] and t[1] == r["regola"] and t[2] == r["scena"]
                   and r.get("dettaglio", t[3]) == t[3] for r in residui)
    nuovi = [t for t in trovati if not dichiarato(t)]
    scaduti = [r for r in residui
               if not any(t[0] == r["file"] and t[1] == r["regola"] and t[2] == r["scena"]
                          and r.get("dettaglio", t[3]) == t[3] for t in trovati)]
    return trovati, nuovi, scaduti


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="cancello CI")
    ap.add_argument("--file", type=Path, help="un file qualunque, senza residui")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.file:
        righe = analizza(a.file.read_text(encoding="utf-8"))
        if a.json:
            print(json.dumps([dict(zip(("regola", "scena", "dettaglio"), r)) for r in righe],
                             ensure_ascii=False, indent=2))
        else:
            for r in righe:
                print(f"  {r[0]:6} {r[1]:28} {r[2]}")
            print(f"\n  {len(righe)} domande senza risposta nel testo")
        return 0

    cfg = carica_config()
    trovati, nuovi, scaduti = esegui(cfg)
    if a.json:
        print(json.dumps({"tool": "domande_developer",
                          "rilievi": [dict(zip(("file", "regola", "scena", "dettaglio"), t))
                                      for t in trovati],
                          "non_dichiarati": len(nuovi), "scaduti": len(scaduti)},
                         ensure_ascii=False, indent=2))
        return 1 if a.check and (nuovi or scaduti) else 0

    per_file: "dict[str, list]" = {}
    for t in trovati:
        per_file.setdefault(t[0], []).append(t)
    for f, righe in per_file.items():
        print(f"\n{f}")
        for _, regola, scena, dettaglio in righe:
            segno = "·" if (f, regola, scena, dettaglio) not in nuovi else "✗"
            print(f"  {segno} {regola:6} {scena[:28]:28} {dettaglio}")
    for r in scaduti:
        print(f"✗ residuo scaduto: {r['file']} {r['regola']} {r['scena']} — non si verifica più, "
              "toglilo da plans/domande-developer.json")
    conta = {}
    for t in trovati:
        conta[t[1]] = conta.get(t[1], 0) + 1
    print("\n  " + " · ".join(f"{k} {v}" for k, v in sorted(conta.items())) if conta else "\n  nessun rilievo")
    if a.check:
        if nuovi or scaduti:
            print(f"✗ domande_developer: {len(nuovi)} rilievi non dichiarati, {len(scaduti)} residui scaduti")
            return 1
        print(f"✓ domande_developer: {len(trovati)} rilievi, tutti dichiarati con la ragione")
    return 0


if __name__ == "__main__":
    sys.exit(main())
