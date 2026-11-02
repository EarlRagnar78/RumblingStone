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
| D9 | i segreti reggono a una divinazione? (§9) | il modulo intero, dal 9° livello |
| D10 | ogni scontro ha la sua riga di scala (§10) | scena di scontro |
| D15 | un'orda di GS basso non è un dosso (§15) | scena di scontro, dal 9° livello |
| D16 | chi è fuori gioco per un TS sa cosa fa (§16) | scena di scontro |
| D18 | la scena dichiara la sua domanda sì/no (§18) | scena di scontro o sociale |
| D19 | la scelta dice dove se ne vede la conseguenza (§19) | blocco di scelta («Se i PG…», A/B/C) |
| D20 | il boss ha un presagio in due scene prima (§20), indicatore fuori da --check | scena del boss |
| D21 | ogni conclusione ha tre indizi da due nodi (§21) | la rete marcata, dove c'è |

La §7 (i sette modi di stare al tavolo di Robin Laws) **non** si misura: è un
giudizio su chi si diverte, e lo chiede il playtester a freddo. Lo stesso vale
per la §8 e per le §11-§14 (il mostro insostituibile, il pericolo che qualcuno
usa, l'incontro che si spezza, il rinforzo che i PG vedono arrivare): per
rispondere bisogna aver simulato lo scontro.

Le §9-§16 vengono dalla ricerca sulle avventure della community
(`plans/RICERCA-AVVENTURE-COMMUNITY-2026-10.md`, ADR-0092). Il livello del
gruppo sta nel profilo (`apl`); dove manca vale quello della campagna.

Le §18-§21 vengono dalle regole d'architettura della rete
(`plans/RICERCA-QUALITA-MISURABILE-2026-10.md` §4, lotto 7b di
PIANO-AVVENTURE-COMMUNITY). I numeri saltano la §17 e le altre sezioni non
misurate apposta: il codice D è sempre il numero della sezione. La D21 tace
dove la rete degli indizi non è marcata, e il 2026-10-22 non lo è in nessun
master.

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
#: D9 · un master con dei segreti, dal 9° livello: i PG divinano. La risposta
#: è un blocco in forma fissa, «Se lo divinano», non una parola sparsa: alla
#: prima prova «segreto» e «indizio» per scena davano 2 rilievi veri su 7 (la
#: targa di DEF-4 Scena 3 è un indizio da leggere, non un segreto da difendere).
SEGRETI = re.compile(r"(?i)nodo d'indizio|\bsegret[oi]\b")
SE_LO_DIVINANO = re.compile(r"(?i)se (?:lo|la|li|le) divinano|la magia contro (?:i segreti|l'indagine)")
APL_CAMPAGNA = 13
APL_DIVINAZIONE = 9
#: D10 · la riga di scala, nella scena dello scontro (PFS, «Scaling Encounter»).
SCALA = re.compile(r"(?i)scalar\w*|con (?:tre|cinque|sei|3|5|6) PG|se (?:manca|è assente|cade) un PG|"
                   r"PG assent\w+|party (?:più forte|più debole|straripante)|per (?:tre|cinque) PG|"
                   r"tavolo da (?:tre|cinque)|un PG in (?:meno|più)")
#: D15 · un gruppo contato di sei o più nemici: al 9° livello un incantesimo
#: ad area lo cancella, e il testo deve dire cosa lo tiene in vita.
ORDA = re.compile(r"(?i)\b(?:[6-9]|[1-9]\d+|sei|sette|otto|nove|dieci|dodici|quindici|venti|trenta|"
                  r"quaranta|cinquanta|cento)\s+(?:hobgoblin|goblin|orchi|orch[ei]|gnoll|coboldi|bugbear|"
                  r"guerrieri|soldati|nani|scheletri|zombi|non morti|ratti|lupi|worg|sgherri|predoni|"
                  r"banditi|cultisti|mercenari|elementali|guardie|fanti|arcieri|lancieri|razziatori|veterani)\b")
REGGE = re.compile(r"(?i)\bad area\b|\bondat\w+|dispers\w+|sparpagl\w+|\bcopertura\b|a gruppi|"
                   r"formazione|palla di fuoco|\bdoss[oi]\b")
#: D16 · salva o sei fuori. Stordito e frastornato durano di norma un round, e
#: non contano.
FUORI_GIOCO = re.compile(r"(?i)\bdominat\w*|\bdominare\b|paralizz\w+|pietrific\w+|blocca (?:persone|mostri)|"
                         r"\bcharme\b|confusion\w+|incapacitat\w+")
USCITA = re.compile(r"(?i)il giocatore|chi è (?:dominat|paralizzat|pietrificat|confus)\w*|nuovo TS|"
                    r"un altro TS|ogni round[^.\n]{0,30}TS|libertà di movimento|rimuovi paralisi|"
                    r"liberarl\w|spezza(?:re)? (?:il|lo) (?:charme|dominio)")
#: D18 · la domanda drammatica (Angry GM): ogni scena giocabile, di scontro o
#: sociale, dichiara la domanda sì/no a cui risponde. La forma è fissa, come
#: «Se lo divinano» della D9: una riga **Domanda:** o **Posta in gioco:** che
#: finisce col punto di domanda. Si accetta anche la domanda già scritta nella
#: prosa del DM, «la domanda non è X, ma se Y» (DEF-4, Scena 4).
SOCIALE = re.compile(r"\b(?:Diplomazia|Raggirare|Intimidire|Percepire Intenzioni)\b")
DOMANDA = re.compile(r"(?im)^[>\s*-]*\*\*(?:Domanda(?: drammatica)?|Posta in gioco)\s*:?\*\*\s*:?[^\n]*\?"
                     r"|\b[Ll]a domanda (?:della scena )?(?:è se\b|non è[^.\n]{0,80}?\bma se\b)"
                     r"|^#*\s*\*\*Obiettivo\b")
#: D19 · la scelta con una conseguenza che si vede (Wardrip-Fruin et al.,
#: DiGRA 2009). L'unità è il **blocco di scelta**: il paragrafo, o l'elenco di
#: paragrafi attaccati, che apre con «Se i PG…», con un **Se** in grassetto
#: retto dai PG (un nome, «qualcuno», un verbo al plurale), o con le opzioni
#: **A —**, **Via B**, **Opzione C**; un titolo «#### Se i PG…» vale fino al
#: titolo dopo. Il blocco dice dove si vede la conseguenza: un rimando a una
#: scena o a un paragrafo, un'eco, il carry-over, l'Echo Ledger, l'esito della
#: scena, l'orologio, un cambio permanente, o la parola «conseguenza».
#: Alla prima prova un **Se** in grassetto qualunque prendeva anche le
#: condizioni del mondo («Se il corno suona», «Se è pre-allertato»), che non
#: sono scelte dei PG.
_PG = r"(?:Thorik|Tordek|Hella|Artemis)"
SCELTA = re.compile(
    r"^(?:>\s*)?(?:[-*+]\s+|\d+\.\s+)?(?:#+\s*)?(?:"
    r"(?:\*\*)?Se i PG\b"
    rf"|\*\*Se (?:il gruppo|qualcuno|nessuno|uno di loro|(?:la|il) giocat\w+|sono i PG|{_PG}\b"
    r"|(?:non |li |lo |la |le |gli |ne |ci )?[a-zàèéìòù]+(?:ano|ono)\b)"
    r"|\*\*(?:(?:Via|VIA|Opzione|OPZIONE) )?[A-D]\s*[—–:-]\s)")
#: Nelle scene di scontro un **Se** in grassetto è quasi sempre tattica («Se
#: Artemis vola invisibile», «Se attaccano la collina»): la conseguenza si vede
#: al round dopo, e alla prima prova erano 6 rilievi falsi su 8. Lì contano
#: solo «Se i PG…» e le opzioni.
SCELTA_FORTE = re.compile(r"^(?:>\s*)?(?:[-*+]\s+|\d+\.\s+)?(?:#+\s*)?(?:(?:\*\*)?Se i PG\b"
                          r"|\*\*(?:(?:Via|VIA|Opzione|OPZIONE) )?[A-D]\s*[—–:-]\s)")
CONSEGUENZA = re.compile(r"(?i)→|\bScena \d+|§\s?\d|\beco\b|\bechi\b|\becho|carry-over|\besito\b|"
                         r"\bARC-?\d{2}\b|\bDEF-\d|conseguenz\w+|countdown|orologio|permanent\w+|"
                         r"(?:seduta|serata|sessione|scena|giorno) (?:dopo|successiv\w)|prossima sessione|"
                         r"\bdomani\b|\bregistr[oi]\b")
#: D20 · il presagio del cattivo (Bryce Lynch): il boss è nominato o indiziato
#: in almeno due scene prima della sua. I nomi vengono dal titolo della scena
#: del boss; il profilo aggiunge gli indizi che il titolo non porta
#: (`presagi`, per esempio «il drago»).
PRESAGI_MINIMI = 2
SCHEDA_BOSS = re.compile(r"\*\*Scheda d'entrata\s+—\s+([^,*\n]+)")
_NON_NOMI = {"Il", "Lo", "La", "Le", "Gli", "Un", "Una", "Uno", "BOSS", "Boss", "Scena", "SCENA",
             "Duello", "Scontro", "Battaglia", "Atto", "Fase"}
#: D21 · la rete degli indizi (Three Clue Rule, J. Alexander; la norma in
#: `rumblingstone-indagine/references/nodi-e-sei-porte.md` §4). La marcatura è
#: un commento HTML, che il tavolo non vede:
#:     <!-- conclusione C1: la targa parla dei PG -->
#:     <!-- indizio C1 -->            (anche «indizio C1, C3»)
#: Il nodo di un indizio è il titolo «Nodo d'indizio» o «N3 — …» sotto cui
#: sta, altrimenti la scena. Ogni conclusione vuole tre indizi da due nodi.
#: Dove la marcatura non c'è la regola tace: il 2026-10-22 nessun master la usa.
CONCLUSIONE = re.compile(r"<!--\s*conclusione\s+(C\d+)\s*:\s*(.*?)\s*-->")
INDIZIO = re.compile(r"<!--\s*indizio\s+(C\d+(?:\s*,\s*C\d+)*)\s*-->")
TITOLO_NODO = re.compile(r"(?m)^#+\s+(?:.*\bNodo d'indizio\b.*|N\d+\s+—.*)$")
TITOLO = re.compile(r"(?m)^#+\s+.*$")
INDIZI_MINIMI, NODI_MINIMI = 3, 2
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


def blocchi_di_scelta(corpo: str, rx: "re.Pattern" = SCELTA) -> "list[tuple[str, str]]":
    """(la riga che apre la scelta, il testo del blocco) per ogni blocco di scelta.

    Un paragrafo che finisce coi due punti si porta dietro quello dopo: la
    conseguenza sta spesso nell'elenco che annuncia.
    """
    righe = corpo.split("\n")
    paragrafi: "list[list[str]]" = []
    corrente: "list[str]" = []
    for i, riga in enumerate(righe):
        if riga.strip() in ("", ">"):
            if corrente:
                paragrafi.append(corrente)
                corrente = []
            continue
        if rx.match(riga) and riga.lstrip("> ").startswith("#"):
            # un titolo «#### Se i PG…» vale fino al titolo dopo
            livello = len(re.match(r"#+", riga.lstrip("> ")).group(0))
            fine = next((j for j in range(i + 1, len(righe))
                         if re.match(rf"^#{{1,{livello}}}\s", righe[j])), len(righe))
            if corrente:
                paragrafi.append(corrente)
            paragrafi.append(righe[i:fine])
            corrente = []
            for j in range(i + 1, fine):   # le righe sotto il titolo sono già prese
                righe[j] = ""
            continue
        corrente.append(riga)
    if corrente:
        paragrafi.append(corrente)
    blocchi: "list[list[str]]" = []
    prima_era_scelta = False
    annuncia = False
    for p in paragrafi:
        scelta = any(rx.match(r) for r in p)
        if (scelta or annuncia) and prima_era_scelta:
            blocchi[-1] += p
            scelta = True
        elif scelta:
            blocchi.append(list(p))
        prima_era_scelta = scelta
        annuncia = scelta and p[-1].rstrip().endswith(":")
    fuori = []
    for b in blocchi:
        apre = next(r for r in b if rx.match(r))
        fuori.append((apre, "\n".join(b)))
    return fuori


def _incipit(riga: str) -> str:
    """«Se Tordek lo tocca» da «- **Se Tordek lo tocca** (curiosità…»."""
    pulita = re.sub(r"^[>\s#*+\d.-]*", "", riga).replace("**", "")
    return re.split(r"[.,:;(—`]|\s→", pulita)[0].strip()[:60]


def nomi_del_boss(titolo: str) -> "list[str]":
    """I nomi propri nel titolo della scena del boss, dopo il trattino."""
    coda = titolo.split("—", 1)[-1] if "—" in titolo else titolo
    coda = coda.split(":", 1)[-1]
    nomi = re.findall(r"\b[A-ZÀ-Ý][\w'’]{3,}", coda)
    return [n for n in nomi if n not in _NON_NOMI and not n.isupper()]


def rete_degli_indizi(testo: str, scene: "list[tuple[str, str]]") -> "list[tuple[str, str, str]]":
    """D21 · ogni conclusione marcata ha tre indizi da due nodi."""
    conclusioni = {m.group(1): m.group(2) for m in CONCLUSIONE.finditer(testo)}
    indizi = list(INDIZIO.finditer(testo))
    if not conclusioni and not indizi:
        return []
    inizi = []
    pos = 0
    for titolo, corpo in scene:
        start = testo.find(corpo, pos)
        if start >= 0:
            inizi.append((start, start + len(corpo), cs.chiave_scena(titolo)))
            pos = start + len(corpo)

    def nodo(p: int) -> str:
        scena = next((k for a, b, k in inizi if a <= p < b), None)
        titoli = [m for m in TITOLO_NODO.finditer(testo, 0, p)]
        if titoli:
            t = titoli[-1]
            dentro = scena is None or any(a <= t.start() < b and k == scena for a, b, k in inizi)
            if dentro:
                return t.group(0).lstrip("#").strip()
        if scena:
            return scena
        altri = [m for m in TITOLO.finditer(testo, 0, p)]
        return altri[-1].group(0).lstrip("#").strip() if altri else "—"

    per_c: "dict[str, list[str]]" = {}
    fuori = []
    for m in indizi:
        for c in re.split(r"\s*,\s*", m.group(1)):
            if c not in conclusioni:
                fuori.append(("D21", "—", f"indizio per {c}, che nessuna conclusione dichiara"))
                continue
            per_c.setdefault(c, []).append(nodo(m.start()))
    for c, frase in conclusioni.items():
        nodi = per_c.get(c, [])
        if len(nodi) < INDIZI_MINIMI or len(set(nodi)) < NODI_MINIMI:
            fuori.append(("D21", "—", f"conclusione {c} («{frase[:50]}»): {len(nodi)} indizi da "
                          f"{len(set(nodi))} nodi, ne servono {INDIZI_MINIMI} da {NODI_MINIMI}"))
    return fuori


def analizza(testo: str, profilo: "dict | None" = None,
             con_ts: bool = True) -> "list[tuple[str, str, str]]":
    """(regola, scena, dettaglio) per ogni domanda senza risposta nel testo."""
    profilo = profilo or {}
    testo = cs.pulisci(testo)
    scene = cs.scene(testo, profilo.get("scena", cs.SCENA_DEF), profilo.get("escludi"))
    boss = _scene_boss(testo, scene)
    apl = profilo.get("apl", APL_CAMPAGNA)
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
        if SCONTRO.search(corpo):
            if not SCALA.search(corpo):
                fuori.append(("D10", k, "scontro senza la riga di scala (tre o cinque PG, un PG assente)"))
            if apl >= APL_DIVINAZIONE and ORDA.search(corpo) and not REGGE.search(corpo):
                fuori.append(("D15", k, f"«{ORDA.search(corpo).group(0)}»: niente dice cosa li tiene in vita "
                              "contro un incantesimo ad area"))
            if FUORI_GIOCO.search(corpo) and not USCITA.search(corpo):
                fuori.append(("D16", k, f"«{FUORI_GIOCO.search(corpo).group(0)}»: non dice cosa fa il "
                              "giocatore del PG fuori gioco, né come ne esce"))
        if (SCONTRO.search(corpo) or SOCIALE.search(corpo)) and not DOMANDA.search(corpo):
            fuori.append(("D18", k, "scena giocabile senza la domanda sì/no (**Domanda:** … ?)"))
        for apre, blocco in blocchi_di_scelta(corpo, SCELTA_FORTE if SCONTRO.search(corpo) else SCELTA):
            if not CONSEGUENZA.search(blocco):
                fuori.append(("D19", k, f"«{_incipit(apre)}»: la scelta non dice dove si vede la conseguenza"))
        if SKILL_CHALLENGE.search(corpo):
            mancano = [nome for nome, rx in (("quanti successi", SC_QUANTI), ("chi tira", SC_CHI),
                                              ("cosa vale un successo", SC_SUCCESSO),
                                              ("cosa costa un fallimento", SC_FALLIMENTO))
                       if not rx.search(corpo)]
            if not comp._prove(corpo):
                mancano.append("cosa si tira (nessuna CD)")
            if mancano:
                fuori.append(("D6", k, "skill challenge senza: " + ", ".join(mancano)))

    # D20 · il boss ha i suoi presagi nelle scene prima della sua.
    chiavi = [cs.chiave_scena(t) for t, _ in scene]
    for i, (titolo, _) in enumerate(scene):
        if chiavi[i] not in boss:
            continue
        nomi = nomi_del_boss(titolo) + [n for m in SCHEDA_BOSS.finditer(scene[i][1])
                                         for n in nomi_del_boss(m.group(1))]
        nomi = list(dict.fromkeys(nomi + list(profilo.get("presagi", {}).get(chiavi[i], []))))
        if not nomi:
            continue
        rx = re.compile(r"\b(?:" + "|".join(re.escape(n) for n in nomi) + r")\b")
        prima = [chiavi[j] for j in range(i) if rx.search(scene[j][1])]
        if len(prima) < PRESAGI_MINIMI:
            fuori.append(("D20", chiavi[i], f"il boss ({' · '.join(nomi)}) compare in {len(prima)} scene prima "
                          f"della sua, ne servono {PRESAGI_MINIMI}"))

    # D21 · la rete degli indizi, dove è marcata.
    fuori += rete_degli_indizi(testo, scene)

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

    # D9 · due scene con un segreto bastano a fare del master un master con segreti.
    if apl >= APL_DIVINAZIONE and not SE_LO_DIVINANO.search(testo):
        con_segreti = [cs.chiave_scena(t) for t, c in scene if SEGRETI.search(c)]
        if len(con_segreti) >= 2:
            fuori.append(("D9", "—", "segreti in " + ", ".join(con_segreti[:4])
                          + ": manca il blocco «Se lo divinano»"))

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

#: Le regole che si stampano e non bloccano. D20 (il presagio del boss) alla
#: calibrazione del lotto 7b ha dato 0 veri su 2, e sotto cancello trova un boss
#: solo: finché non ha un rilievo vero resta un indicatore, fuori da --check
#: (lotto 7e di PIANO-AVVENTURE-COMMUNITY, 2026-10-22). Non è tolta: un boss
#: senza presagio resta un difetto da leggere.
INDICATORI = frozenset({"D20"})


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
    nuovi = [t for t in trovati if not dichiarato(t) and t[1] not in INDICATORI]
    scaduti = [r for r in residui if r["regola"] not in INDICATORI
               and not any(t[0] == r["file"] and t[1] == r["regola"] and t[2] == r["scena"]
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
            segno = ("~" if regola in INDICATORI
                     else "·" if (f, regola, scena, dettaglio) not in nuovi else "✗")
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
