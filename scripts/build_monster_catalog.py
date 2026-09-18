#!/usr/bin/env python3
"""
build_monster_catalog.py — Scansiona la campagna e produce monster_catalog.yaml.

Sorgenti (in ordine di priorità):
  1. Bestiario/{mostri,villain,png}/**/*.md   (libreria standard, header strutturato)
  2. Bestiario/pregen-pcgen/**/*.htm|*.html|*.pcg|*.pdf  (sorgenti storiche PCGen/web)
  3. 08_La Battaglia Di Hammerfist/00_Schede_dei_Personaggi_Unita*.md  (parsing sezioni)
  4. 09_Continuazione.../Arco-*STATBLOCCHI*.md
  5. 04_tomba_di_Belkram/**, 01_LaMiniera/**, 02_*/**, 06_*/**, 07_*/** (tutte le .txt/.md/.htm con statblock)

Output:
  scripts/monster_catalog.yaml   (generated, non committare modifiche a mano)
  scripts/monster_catalog.custom.yaml  (NON sovrascritto; append-only user)

Schema record:
  - id: slug unico (fname-without-ext + short hash)
    name: display name
    cr: float o int o null
    faction: red-hand|drow-sonjak|gnoll|loxo-centaur-corrupted|githyanki-vaereth|teschio-nero-thay|rakshasa|ghostlord-undead|rethmar-defender|dauth-defender|cerchio-druid|aberration|zhentarim|unknown
    role: melee|ranged|caster|mount|leader|boss|fodder|...
    environment: any|underdark|forest|urban|aerial|...
    source_file: path relativo al root
    aliases: [list]
    notes: str
"""

import re
import hashlib
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.testo import slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "monster_catalog.yaml"
CUSTOM = Path(__file__).resolve().parent / "monster_catalog.custom.yaml"

# Heuristic CR extraction
CR_PATTERNS = [
    re.compile(r'\*\*CR\*\*[:\s]*([\d./]+)', re.IGNORECASE),
    re.compile(r'\bCR[:\s]*([\d./]+)', re.IGNORECASE),
    re.compile(r'\bGS[:\s]*([\d./]+)', re.IGNORECASE),  # italian "Grado di Sfida"
    re.compile(r'-cr(\d+)', re.IGNORECASE),             # filename cr7
    re.compile(r'cr(\d+)\b', re.IGNORECASE),
]
# Priority-ordered: first-match wins. Narrow/unique keywords (dragons, aberrations,
# named NPCs) go BEFORE broad ones (red-hand) so e.g. "Abithriax" / "Retriever"
# don't get swallowed by the hobgoblin horde.
FACTION_KEYWORDS = {
    "dragon": ["abithriax", "arbitrax", "regiarix", "ozyrrandion", "tyrgarun", "fauci di palude", "razorfiend", "drago rosso", "drago nero", "drago verde", "drago blu", "dragon adult", "dragon young", "wyrmling", "drago "],
    # I due conclavi illithid vanno PRIMA di `aberration`, che altrimenti se li
    # prende tutti con `mind flayer`/`illithid`. Sono fazioni distinte e ostili
    # fra loro (canone: Xal'thor chiama Zalkatar «biologo da torre», Zalkatar
    # chiama lui «cacciatore di mandria»), e il DM ha dichiarato il 2026-09-17
    # che Zalkatar e' «il Padrone delle Menti» del laboratorio di ARC-04.
    "illithid-zalkatar": ["zalkatar", "sethrax", "kethran", "torre invisibile",
                          "padrone delle menti", "spettri di conoscenza",
                          "golem bibliotecario", "guardiano di luce"],
    "illithid-xal-thor": ["xal'thor", "xal thor", "xal-thor", "zarim",
                          "schiavo psionico", "forma del nucleo"],
    "aberration": ["myconid", "beholder", "bebilith", "retriever", "grell", "xorn", "black pudding", "cubo gelatinoso", "celebromorf", "phantom fungus", "antenato nanico", "mind flayer", "illithid"],
    "ghostlord-undead": ["ghostlord", "bone naga", "deathlock", "skeletal", "spectre", "allip", "lich", "ghost lion"],
    "rakshasa": ["rakshasa", "collezionista"],
    "drow-sonjak": ["drow", "sonjak", "sajak", "underdark cleric", "deep warden", "runecaster"],
    "githyanki-vaereth": ["githyanki", "gith ", "vaereth"],
    "gnoll": ["gnoll", "flind", "hyenodon", "yeenoghu"],
    "loxo-centaur-corrupted": ["loxo", "centaur", "centauro"],
    "teschio-nero-thay": ["thayan", "red wizard", "teschio nero"],
    "starsong-elf": ["starsong", "tiri-kitor", "lythiel", "maewen", "owl cavalry"],
    "cerchio-druid": ["hella", "cerchio sacro", "druida", "druid", "treant"],
    "rethmar-defender": ["rethmar", "valerius", "lorana"],
    "dauth-defender": ["dauth", "thorek", "dwarf defender", "tordek", "morlin", "rurik"],
    # Le due fazioni del ~372 DR: l'assedio antico di Hammerfist e' mille anni
    # prima della Mano Rossa, e tenerli insieme farebbe proporre incontri che
    # mescolano due ere. `orda-antica-372dr` esisteva gia' per Balvar
    # Fuocospento; `hammerfist-372dr` e' il suo simmetrico difensivo.
    "orda-antica-372dr": ["zog'tar", "zogtar", "balvar fuocospento",
                          "skullcrusher il nero"],
    "hammerfist-372dr": ["thorek i", "durin hammerfist", "thorgrim barbadiferro"],
    # Gli alleati dei PG che non appartengono a un gruppo nominato. Prima erano
    # due fazioni da un membro solo (`rhod-allies`, `rakshasa-hunter`) che
    # descrivevano uno **scopo**, non uno schieramento: quello sta in `Role`.
    "alleati-del-vale": ["jorr natherson", "therysol", "therisol"],
    "hammerfist-hero": ["borin ferropugno", "dara occhiolesto", "thorin runaforte", "nala cantapietre", "tempestas", "dana forgiapietra", "lunapiena", "ventolesto", "orion pelleorsa"],
    "red-hand": ["hobgoblin", "red hand", "mano rossa", "wyrmlord", "goblin", "worg", "bugbear", "orc", "ogre", "ettin", "hell hound", "kulkor", "draxoksus", "koth", "azarr kul", "tiamat", "saarvith"],
    # ⚠️ «zalkatar» stava in questo elenco: e' un illithid warlock della
    # Torre Invisibile, non un comandante della Mano Rossa.
}


ENV_KEYWORDS = {
    "underdark": ["underdark", "deep", "ainin", "dovil", "brieyn", "drow"],
    "forest": ["druid", "treant", "cerchio", "hella", "starsong", "ranger"],
    "urban": ["militia", "city guard", "valerius", "rethmar"],
    "aerial": ["dragon", "drago", "wyvern", "manticore", "gufo"],
    "swamp": ["razorfiend", "black dragon", "drago nero", "fauci", "regiarix", "rhest"],
    "dungeon": ["belkram", "miniera", "duergar", "tomba"],
    "plain": ["gnoll", "centaur", "loxo", "shaar"],
    "mountain": ["hill giant", "giant", "eagis", "hammerfist"],
}

# Priority-ordered: first-match wins. "flier" goes first so dragons/manticores
# aren't mis-tagged as caster/boss.
ROLE_KEYWORDS = {
    "flier": ["dragon", "drago", "manticore", "wyvern", "gufo celestiale"],
    "caster-arcane": ["wizard", "sorcerer", "runecaster", "red wizard", "stregone", "arcimago"],
    "caster-divine": ["cleric", "priest", "druid", "shaman", "warpriest", "chierico", "druida", "arci-druido"],
    "boss": ["wyrmlord", "matrona", "chieftain", "commander", "captain", "capo ", "signore", " boss"],
    "mount": ["mount ", "cavalcatura"],
    "melee-heavy": ["fighter", "barbarian", "knight", "defender", "greatsword", "greataxe"],
    "ranged": ["ranger", "archer", "longbow", "crossbow"],
    "fodder": ["warrior", "regular", "militia", "fanteria"],
}

# --- il valore DICHIARATO vince su quello indovinato ------------------------
#
# 🔴 Fino al 2026-09-17 questo builder **indovinava** fazione, ruolo e ambiente
# da euristiche su parole chiave, e **ignorava le intestazioni** che ogni
# statblocco dichiara e che `validate_bestiario` pretende. Due valori per lo
# stesso fatto: quello che il DM scrive nel file, e quello che finisce nel
# catalogo — e nel catalogo finiva il secondo.
#
# Si e' visto aggiungendo la fazione `zhentarim` ai combattenti del Torneo di
# Dauth: l'intestazione diceva `zhentarim`, il catalogo registrava
# `dauth-defender`, e nessuno se ne accorgeva perche' il file *sembrava* giusto.
#
# Adesso l'euristica resta, ma solo come **ripiego** per i documenti che non
# dichiarano niente (i .txt e i moduli d'arco). E' la forma di ADR-0041:
# contare quel che e' dichiarato vale piu' che indovinarlo.
DICH_FACTION = re.compile(r"\*\*Faction\*\*:\s*([A-Za-z0-9_-]+)")
DICH_ROLE = re.compile(r"\*\*Role\*\*:\s*([A-Za-z0-9_-]+)")
DICH_ENV = re.compile(r"\*\*Environment\*\*:\s*([A-Za-z0-9_-]+)")


#: Sinonimi esatti, non giudizi: prima della correzione l'euristica normalizzava
#: tutto sulla lista chiusa, e leggere le intestazioni **spaccherebbe** una
#: fazione in due nomi. `mano-rossa` e' l'italiano di `red-hand`, e le sei
#: creature che lo dichiarano sono comandanti della Mano Rossa (Ushgar,
#: Ghaurush, il Chierico di Gruumsh): `suggest_encounter --faction red-hand`
#: deve continuare a trovarle.
#:
#: ⚠️ Qui ci vanno SOLO i sinonimi certi. `underdark` usato come fazione, o
#: `rhod-allies`, non sono sinonimi di niente: restano come sono, visibili, e
#: consolidarli e' una decisione di vocabolario che spetta al DM.
ALIAS_FACTION = {"mano-rossa": "red-hand"}


def dichiarato(rx, testo):
    """Il valore scritto nell'intestazione, o None se il file non lo dichiara.

    ⚠️ Per `Environment` si prende il PRIMO valore: qualche scheda ne dichiara
    due separati da virgola (`forest,mountain`), e i filtri di
    `suggest_encounter` confrontano un ambiente solo.
    """
    m = rx.search(testo)
    return m.group(1).strip().lower() if m else None


def short_hash(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:6]

def guess_faction(text):
    t = text.lower()
    for fac, kws in FACTION_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return fac
    return "unknown"

def guess_env(text):
    t = text.lower()
    for env, kws in ENV_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return env
    return "any"

def guess_role(text):
    t = text.lower()
    for role, kws in ROLE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return role
    return "generalist"

def extract_cr(text, fname=""):
    for pat in CR_PATTERNS:
        m = pat.search(text)
        if m:
            val = m.group(1)
            try:
                if '/' in val:
                    num, den = val.split('/')
                    return float(num) / float(den)
                return float(val)
            except ValueError:
                continue
    # fallback: filename
    for pat in CR_PATTERNS[-2:]:
        m = pat.search(fname)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                continue
    return None

# --- D18: un documento con piu' creature vale piu' di un record ---------------
#
# 🔴 **Il difetto misurato il 2026-09-17.** Questo builder produceva **un record
# per file** e prendeva il primo GS che trovava. Un documento d'arco con dodici
# creature diventava quindi **una voce sola**, intitolata al documento e con un
# GS arbitrario: «Parte 2A – Torre Invisibile», GS 10. Erano **19 record** cosi',
# e in `suggest_encounter --el 10` comparivano come se fossero mostri.
#
# Non era un buco di copertura — le creature della Torre hanno tutte voce propria
# nel Bestiario — ma rumore che il DM vedeva al tavolo.
#
# Decisione del DM (D18): **spezzarli per intestazione, verificando che non
# esistano gia'.**
#
# ⚠️ **La deduplica e' la parte delicata, ed e' ancorata a un fatto dichiarato.**
# Confrontare nomi per somiglianza e' esattamente l'errore che ADR-0053 vieta.
# Qui il confronto si fa **solo dentro l'insieme delle voci del Bestiario che
# citano QUESTO file come `Source`** — cioe' un legame che qualcuno ha scritto,
# non indovinato. Fuori da quell'insieme non si confronta niente.

#: Un'intestazione che nomina una creatura porta il suo GS: «## 3. Guardiano di
#: Luce (Elementale/Costrutto, CR 10)». Senza GS non e' un soggetto giocabile.
SEZIONE = re.compile(
    r"^#{2,4}\s+(?P<titolo>[^\n]*?\b(?:CR|GS)\s*~?\s*(?P<cr>\d+(?:[.,]\d+)?)"
    r"(?:\s*[-–]\s*\d+)?[^\n]*)$",
    re.M | re.IGNORECASE)

#: Sotto questa soglia il documento descrive UNA creatura, e il record di file
#: e' gia' quello giusto: spezzare non guadagnerebbe niente.
MIN_SEZIONI = 2

_RUMORE = re.compile(r"\b(?:cr|gs|ciascuno|ciascuna|circa|modello|versione|"
                     r"avanzata?|media?|xp|px|el)\b|[0-9]", re.IGNORECASE)


def _parole(titolo):
    """Le parole che identificano un soggetto, senza la punteggiatura e i numeri."""
    pulito = _RUMORE.sub(" ", titolo)
    return {p for p in re.split(r"[^\wàèéìòù']+", pulito.lower()) if len(p) > 2}


def sezioni_creatura(content):
    """Le intestazioni che nominano una creatura con il suo GS.

    Restituisce `[(titolo_pulito, cr), ...]`. Il titolo perde la numerazione
    d'elenco («3. ») e la coda fra parentesi che porta solo il GS.
    """
    fuori = []
    for m in SEZIONE.finditer(content):
        # ⚠️ La numerazione e' **multi-livello** nel Palio («### 3.2 Drow
        # Chierica»): togliere solo `\d+[.)]` lasciava «2 Drow Chierica», cioe'
        # un nome che comincia per cifra. Misurato su otto voci.
        titolo = re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s+", "", m.group("titolo")).strip()
        # «Guardiano di Luce (Elementale/Costrutto, CR 10)» → si tiene tutto
        # tranne il pezzo che ripete il GS, che diventa un campo a se'.
        titolo = re.sub(r"[(,—–-]\s*(?:CR|GS)\s*~?\s*[\d.,\s–-]+\)?\s*$", "",
                        titolo, flags=re.IGNORECASE).strip(" (,—–-")
        # Se la coda tagliata ha lasciato una parentesi che non chiude piu'
        # («Aldemar Vosk (LN»), si taglia da li': un nome a meta' e' peggio di
        # un nome corto.
        if titolo.count("(") > titolo.count(")"):
            titolo = titolo[:titolo.rfind("(")].strip(" ,—–-")
        if not titolo:
            continue
        try:
            cr = float(m.group("cr").replace(",", "."))
        except ValueError:
            continue
        fuori.append((titolo, cr))
    return fuori


def gia_nel_bestiario(titolo, cr, coperti):
    """Il soggetto ha gia' una voce che punta a questo stesso file?

    `coperti` sono **solo** le voci del Bestiario che dichiarano questo file
    come fonte. Dentro quell'insieme il confronto per parole e' sicuro: il
    legame documento↔voce e' gia' stato affermato da qualcuno, e qui si decide
    soltanto *quale* delle sue voci corrisponde a *quale* intestazione.
    """
    mie = _parole(titolo)
    if not mie:
        return True          # un titolo senza parole proprie non si sa dedurre
    for nome, cr_voce in coperti:
        sue = _parole(nome)
        if not sue:
            continue
        if sue <= mie or mie <= sue:
            return True
        # nomi diversi ma stesso GS e meta' delle parole in comune: e' la
        # stessa creatura scritta due volte (p.es. «Grell» / «Grell (Torre)»)
        if cr_voce == cr and len(mie & sue) >= max(1, min(len(mie), len(sue)) // 2):
            return True
    return False


def extract_name(content, fname):
    # First try H1 markdown
    m = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if m:
        name = m.group(1).strip()
        name = re.sub(r'\[.*?\]', '', name).strip()  # strip [INFERRED] tag
        return name
    # fallback: filename cleaned
    base = Path(fname).stem
    return base.replace('-', ' ').replace('_', ' ').title()

def read_file_safe(path):
    for enc in ('utf-8', 'latin-1', 'cp1252'):
        try:
            return path.read_text(encoding=enc, errors='ignore')
        except Exception:
            continue
    return ""

def should_skip(path):
    # 'docs' = documentazione (guide, ADR renderizzati, contratti tool): può
    # CITARE uno statblock d'esempio, non ne è mai la fonte — indicizzarla
    # inquinerebbe il catalogo (es. GUIDA-BESTIARIO.md letta come mostro CR 10).
    # 'STANDALONE-*' = moduli autoconclusivi (altro sistema, altra ambientazione):
    # i loro statblock sono locali al modulo e non appartengono al Bestiario della
    # campagna — indicizzarli mescolerebbe PF1e e 3.5 nello stesso catalogo.
    # '_ARCHIVIO' = istantanee e sorgenti assorbiti: sono COPIE di file vivi, e
    # indicizzarle duplica ogni statblock che contengono. Trovato il 2026-09-12,
    # nel momento esatto in cui si archiviarono 12 file: il catalogo passo' a
    # 311 record e `validate_bestiario` divento' rosso con un doppione di
    # «Battaglia Finale – Fase 0». E' la forma del rischio che D10 aveva
    # dichiarato — «una copia crea un secondo master» — comparsa al primo giro.
    # `validate_modules.py` escludeva gia' `_ARCHIVIO` per la stessa ragione.
    skip_dirs = {'.git', 'node_modules', '.claude', '.cursor', '.windsurf', '.gemini', '.chatgpt', '.agents', '.github', 'Immagini', 'immage_campaign', 'Mappe', 'Musica', 'skills', 'Script', 'Old', 'png_La_mano_rossa_del_destino_files', 'tokens', 'homebrew', 'docs', 'campaign',
                 '_ARCHIVIO', 'STANDALONE-Il-Drappo-di-Tarsilia'}
    for part in path.parts:
        if part in skip_dirs or part.endswith('_files'):
            return True
    # 'docs' e 'campaign' = documentazione e diari: CITANO statblock (esempi,
    # tabelle di GS, log di sessione) ma non ne sono la fonte. Le fonti sono
    # Bestiario/ e le cartelle d'arco.
    # .hb.md = artefatti di layout Homebrewery (ADR-0003), mai fonti di statblock
    if path.name.endswith('.hb.md'):
        return True
    return False

#: Da quali righe una voce del Bestiario dichiara il proprio bersaglio.
#: ⚠️ Una riga puo' citarne **piu' di uno** — Skullcrusher il Nero ha i numeri
#: nel FASTPLAY e la verifica nell'ERRATA. La prima stesura si fermava al primo
#: percorso, e il secondo file restava scoperto: risultato, due voci per lo
#: stesso drago. Trovato dal cancello di D18 al primo giro.
_RIGA_FONTE = re.compile(r"^\*\*(?:Source|Key stats)\*\*.*$", re.M)
_PERCORSO = re.compile(r"`([^`]+\.md)`")
_NOME_VOCE = re.compile(r"^#\s+(.+?)(?:\s*\[|$)", re.M)


def _fonti_dichiarate(testo):
    """Tutti i percorsi citati nelle righe `**Source**` / `**Key stats**`."""
    return {c for riga in _RIGA_FONTE.findall(testo) for c in _PERCORSO.findall(riga)}


def copertura_del_bestiario(root):
    """`{file d'arco: [(nome della voce, GS), ...]}` — chi copre gia' che cosa.

    Serve alla deduplica di D18 e **solo** a quella: dice, per un dato
    documento, quali soggetti hanno gia' una scheda che lo cita. E' un legame
    dichiarato nel file, non dedotto da una somiglianza di nomi.
    """
    fuori = {}
    for p in sorted((root / "Bestiario").rglob("*.md")):
        testo = read_file_safe(p)
        m = _NOME_VOCE.search(testo)
        if not m:
            continue
        nome = re.sub(r"\[.*?\]", "", m.group(1)).strip()
        cr = extract_cr(testo, p.name)
        for citato in _fonti_dichiarate(testo):
            for base in (root, p.parent, p.parent.parent):
                if (base / citato).exists():
                    rel = str((base / citato).resolve().relative_to(root.resolve()))
                    fuori.setdefault(rel, []).append((nome, cr))
                    break
    return fuori


def _superate_dal_gemello(root):
    """I file del `Bestiario/` il cui gemello porta lo stesso soggetto — e che
    quindi non devono produrre un secondo record.

    🔴 **Il difetto misurato il 2026-09-17.** Tredici soggetti avevano **due**
    record nel pool: una scheda canonica (`Xal_thor/Xal_thor.md`) e un POINTER
    `-crN` accanto (`xal-thor-illithid-commander-cr14.md`), nato quando lo
    scanner non raggiungeva ancora i file annidati. Adesso li raggiunge
    entrambi, e `suggest_encounter` puo' proporre lo stesso villain due volte.

    ⚠️ **E non erano due copie uguali.** In ogni coppia **uno dichiara le
    intestazioni e l'altro le fa indovinare**, e in **sei** casi il risultato
    diverge: Tyrgarun era `dragon` da una parte e `red-hand` dall'altra,
    l'Avatar di Tiamat `rethmar-defender` contro `red-hand`, Therysol
    `rakshasa-hunter` contro `unknown`. Il Conte Valerius aveva perfino **due
    GS**, 14 e 6.

    Quindi la scelta non e' «tengo il canonico»: e' **tengo quello che
    dichiara**, che e' ADR-0041 applicato a una coppia. A parita' (entrambi
    dichiarano, o nessuno dei due) vince il file che **non** e' il POINTER.

    🔵 Vale **solo** fra due file del `Bestiario/`. Un POINTER che rimanda a un
    file d'arco resta indicizzato: li' e' l'unica cosa che tiene la creatura
    nel pool, ed e' tutto il senso del lotto 4d-5.
    """
    perse = set()
    for p in sorted((root / "Bestiario").rglob("*.md")):
        testo = read_file_safe(p)
        testa = testo.split("\n", 1)[0]
        if "[POINTER" not in testa and "[RIMANDO]" not in testa:
            continue
        rel = str(p.relative_to(root))
        for citato in _fonti_dichiarate(testo):
            bersaglio = None
            for base in (root, p.parent, p.parent.parent):
                if (base / citato).exists():
                    bersaglio = str((base / citato).resolve().relative_to(root.resolve()))
                    break
            if not bersaglio or bersaglio == rel or not bersaglio.startswith("Bestiario/"):
                continue
            io_dichiaro = DICH_FACTION.search(testo) is not None
            lui_dichiara = DICH_FACTION.search(read_file_safe(root / bersaglio)) is not None
            if io_dichiaro and not lui_dichiara:
                perse.add(bersaglio)
            elif lui_dichiara and not io_dichiaro:
                perse.add(rel)
            else:
                perse.add(rel)          # a parita', il POINTER cede
    return perse


def scan_directory(root):
    records = []
    copertura = copertura_del_bestiario(root)
    superate = _superate_dal_gemello(root)
    valid_ext = {'.md', '.txt', '.htm', '.html', '.pcg'}
    # sorted() => walk deterministico su ogni filesystem/checkout (il CI gate
    # "catalogo in sync" confronta byte-per-byte)
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        if should_skip(path.relative_to(ROOT)):
            continue
        if str(path.relative_to(ROOT)) in superate:
            continue   # il gemello porta lo stesso soggetto e dichiara di piu'
        if path.suffix.lower() not in valid_ext:
            continue
        # Only include files that look like statblocks
        content = read_file_safe(path)
        # Una scheda che si dichiara NON-CREATURA (ADR-0033) non entra nel
        # catalogo dei mostri: un organo collegiale di sette seggi o una
        # popolazione di profughi non si incontrano, e `suggest_encounter`
        # non deve poterli proporre. Il marcatore sta in testa al file.
        if "[NON-CREATURA]" in "\n".join(content.split("\n")[:8]):
            continue
        rel = str(path.relative_to(ROOT))
        rel_lower = rel.lower()

        # Hard blocklist: non-monster paths/filenames that leak via CR-in-text
        BLOCK_SUBSTR = [
            'build/',
            # I piani e le decisioni architetturali PARLANO di statblocchi e ne
            # mostrano esempi: ADR-0021 ne contiene uno intero. Un documento che
            # spiega il formato non è un mostro.
            'plans/',
            'docs/',
            'campaign-party',
            'treasure&xp',
            'treasure_xp',
            'villans.md',
            'readme',
            'indice',
            'overview',
            'house-rules',
            'campaign-coherence',
            'dm-player-strategy',
            'regolamento',
            'atlante visivo',
            'guida-agli-scontri',
            # L'APPARATO D'USO (ADR-0018) cita i GS nel foglio del cast — «Terros,
            # guardiano del Nodo di Terra, GS 15» — ma è una pagina di regia, non
            # la fonte di uno statblock. Senza questa riga la cassetta di ARC-07
            # entrava nel catalogo come un mostro di GS 15, col titolo del file.
            'cassetta-del-dm',
            'cue-sonori',
            'to-be_integrated',
            'sidemissions',
            'cheat-sheet',
            'minimappa',
            'hooks',
            'mappe-',
            '-mappe',
            '-mappa.md',
            'censimento',
            'piano-revisione',
            'timeline',
            'consequenze', 'conseguenze', 'esiti',
        ]
        if any(b in rel_lower for b in BLOCK_SUBSTR):
            continue

        is_statblock_folder = any(k in rel for k in [
            'Bestiario/', 'STATBLOCCHI', 'Schede_dei_Personaggi',
            'LaMiniera', 'Belkram', 'Celebromorfosi',
        ])
        # Strict statblock signature: need BOTH an HP-like stat AND an AC-like stat
        # (or an explicit CR token). Avoids false positives from narrative docs
        # that only happen to mention "HP" or "CR" in prose.
        head = content[:4000]
        has_hp = re.search(r'\b(HP|PF|hp|Hit Points|Punti Ferita)[:\s]*\d+', head) is not None
        has_ac = re.search(r'\b(AC|CA|Armor Class|Classe Armatura)[:\s]*\d+', head) is not None
        has_cr_explicit = re.search(r'(\*\*CR\*\*|\bCR[:\s]+\d|\bGS[:\s]+\d|Challenge Rating)', head, re.IGNORECASE) is not None
        has_stat = (has_hp and has_ac) or has_cr_explicit
        if not (is_statblock_folder or has_stat):
            continue
        cr = extract_cr(content, path.name)
        if cr is None:
            continue  # no CR → can't use in encounter builder
        name = extract_name(content, path.name)
        testa = content[:600]
        faction = dichiarato(DICH_FACTION, testa) or guess_faction(
            name + " " + rel + " " + content[:500])
        faction = ALIAS_FACTION.get(faction, faction)
        env = dichiarato(DICH_ENV, testa) or guess_env(content[:500] + " " + rel)
        role = dichiarato(DICH_ROLE, testa) or guess_role(content[:500] + " " + name)
        rec_id = f"{slug(name, max_len=80)}-{short_hash(rel)}"
        notes_m = re.search(r'\*\*Notes\*\*[:\s]*(.+?)$', content, re.MULTILINE)
        notes = notes_m.group(1).strip() if notes_m else ""

        # D18 — un documento d'arco con piu' creature si spezza per intestazione.
        # Le schede del `Bestiario/` non si toccano: una scheda e' gia' un
        # soggetto solo, e le sue sezioni interne sono capacita', non creature.
        sezioni = [] if rel.startswith("Bestiario/") else sezioni_creatura(content)
        if sezioni:
            coperti = copertura.get(rel, [])
            scoperte = [(t, c) for t, c in sezioni if not gia_nel_bestiario(t, c, coperti)]
            if len(sezioni) >= MIN_SEZIONI:
                for titolo, cr_sez in scoperte:
                    records.append({
                        "id": f"{slug(titolo, max_len=80)}-{short_hash(rel + titolo)}",
                        "name": titolo,
                        "cr": cr_sez,
                        "faction": faction,
                        "role": dichiarato(DICH_ROLE, testa) or guess_role(titolo),
                        "environment": env,
                        "source_file": rel,
                        "notes": notes[:200],
                    })
            # 🔴 Il record intitolato al DOCUMENTO sparisce **solo** quando ogni
            # creatura che il documento nomina ha gia' una voce propria. Se ne
            # resta anche una scoperta, il record di file e' l'unica cosa che la
            # tiene nel pool, e toglierlo sarebbe il difetto opposto a D18:
            # meno rumore e **meno creature**.
            if not scoperte:
                continue
            if len(sezioni) >= MIN_SEZIONI:
                continue

        records.append({
            "id": rec_id,
            "name": name,
            "cr": cr,
            "faction": faction,
            "role": role,
            "environment": env,
            "source_file": rel,
            "notes": notes[:200],
        })
    return records

def to_yaml(records):
    """Minimal YAML writer (no external deps)."""
    lines = ["# Auto-generated by scripts/build_monster_catalog.py",
             "# Do NOT edit by hand. Add custom monsters in monster_catalog.custom.yaml",
             f"# Total records: {len(records)}",
             "monsters:"]
    # source_file nella chiave: i duplicati a pari faction/cr/name non
    # dipendono dall'ordine di scansione
    for r in sorted(records, key=lambda x: (x['faction'], x['cr'] or 0, x['name'], x['source_file'])):
        lines.append(f"  - id: {r['id']}")
        lines.append(f"    name: {json.dumps(r['name'], ensure_ascii=False)}")
        lines.append(f"    cr: {r['cr'] if r['cr'] is not None else '~'}")
        lines.append(f"    faction: {r['faction']}")
        lines.append(f"    role: {r['role']}")
        lines.append(f"    environment: {r['environment']}")
        lines.append(f"    source_file: {json.dumps(r['source_file'], ensure_ascii=False)}")
        if r['notes']:
            lines.append(f"    notes: {json.dumps(r['notes'], ensure_ascii=False)}")
    return "\n".join(lines) + "\n"

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Indicizza gli statblocchi del repo in scripts/monster_catalog.yaml.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="dry-run: confronta col catalogo esistente, non scrive "
                         "(exit 1 se disallineato)")
    ap.add_argument("-o", "--output", type=Path, default=OUT,
                    help=f"percorso del catalogo (default: {OUT.name})")
    args = ap.parse_args(argv)

    print(f"[catalog] Scanning {ROOT} ...", file=sys.stderr)
    records = scan_directory(ROOT)
    print(f"[catalog] Found {len(records)} monster records.", file=sys.stderr)
    rendered = to_yaml(records)

    if args.check:
        current = args.output.read_text(encoding='utf-8') if args.output.exists() else None
        if current == rendered:
            print(f"[catalog] ✓ {args.output.name} in sync ({len(records)} record)")
            return 0
        print(f"[catalog] ✗ {args.output.name} disallineato — esegui senza --check "
              f"per rigenerare", file=sys.stderr)
        return 1

    args.output.write_text(rendered, encoding='utf-8')
    print(f"[catalog] Wrote {args.output}", file=sys.stderr)
    if not CUSTOM.exists():
        CUSTOM.write_text(
            "# monster_catalog.custom.yaml — user-edited append-only list.\n"
            "# Same schema as monster_catalog.yaml. Merged at read-time by\n"
            "# suggest_encounter.py. Not overwritten by build_monster_catalog.py.\n"
            "monsters: []\n", encoding='utf-8')
        print(f"[catalog] Created empty {CUSTOM}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
