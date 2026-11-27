#!/usr/bin/env python3
"""lessico_regole.py — i termini ufficiali di D&D 3.5 e PF1e, e chi li usa male.

Il problema
  Un agente che scrive «talento *Spezzaferro Nanico*» o «*Arma Specializzata*»
  quando il modulo accanto dice «Specializzazione in un'Arma» non ha modo di
  sapere, senza aprire l'SRD, se il termine esiste e come si chiama. La ricerca
  per nome di ``riscontro_srd.py regola`` non trovava nemmeno i talenti 3.5,
  perché nell'SRD il titolo è «Improved Trip <small>[General]</small>».

Cosa fa
  - ``indice``: genera dall'SRD 3.5 e dal PRD PF1e in cache (quelli di
    ``riscontro_srd.py``, ADR-0103) l'elenco dei termini ufficiali, con il tipo
    e il punto della fonte. L'elenco sta nella cache, non nel repo.
  - ``cerca NOME``: un termine, in inglese o in italiano, nelle due fonti.
  - ``controlla FILE...``: legge le righe dei talenti dei file e segnala ogni
    talento che non è né nella tabella italiana né nelle fonti, e non è
    marcato come fonte privata, non SRD, PF1e o regola della casa sulla
    stessa riga.
  La tabella italiano → SRD 3.5 → PF1e è ``scripts/lessico_it.yaml``.

Uso
  python3 scripts/lessico_regole.py indice
  python3 scripts/lessico_regole.py cerca "Sbilanciare migliorato"
  python3 scripts/lessico_regole.py controlla Bestiario/ PG/ [--json] [--check]
  python3 scripts/lessico_regole.py controlla --tutto --campi   # anche incantesimi, abilità, oggetti

Exit 0 ok · 1 con --check, almeno un termine sconosciuto non marcato · 2 uso
"""
from __future__ import annotations

import argparse
import functools
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import riscontro_srd as R  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TABELLA = ROOT / "scripts" / "lessico_it.yaml"
TABELLA_PF1 = ROOT / "scripts" / "lessico_it_pf1.tsv"
TABELLA_35 = ROOT / "scripts" / "lessico_it_35.tsv"
# Gli oggetti unici della campagna: un nome qui non è un termine sconosciuto (DM, 2026-11-07).
# I nomi inglesi dei talenti di tutti i manuali 3.5 (indici crystalkeep e realmshelps, solo nomi).
TALENTI_MANUALI = ROOT / "scripts" / "talenti_manuali_35.tsv"
TALENTI_PF1 = ROOT / "scripts" / "talenti_manuali_pf1.tsv"
OGGETTI_CAMPAGNA = ROOT / "campaign" / "OGGETTI-DELLA-CAMPAGNA.md"
# Un modulo è PF1e se lo dice il percorso o l'intestazione: lì vale la tabella
# diretta italiano PF1e → PRD, mai il passaggio per la 3.5 (DM, 2026-11-07).
MODULO_PF1 = re.compile(r"PF1e|Pathfinder", re.I)

# Il tipo di un titolo dell'SRD 3.5 si ricava dal file.
TIPI_SRD = (
    ("feats", "talento"), ("spells/spells-", "incantesimo"), ("epic-spells", "incantesimo"),
    ("skills", "abilità"), ("monsters/", "mostro"), ("epic-monsters", "mostro"),
    ("magic-items", "oggetto"), ("classes", "classe"), ("psionic-powers", "potere"),
)
TIPI_PF1 = {"feat": "talento", "spell": "incantesimo", "skill": "abilità",
            "item": "oggetto", "creature": "mostro", "class": "classe",
            "trap": "trappola", "affliction": "afflizione"}

TITOLO = re.compile(r"^#{2,4}\s+(?P<n>[^\n]+?)\s*$", re.M)
GRASSETTO = re.compile(r"^\*\*_?(?P<n>[A-Z][^*_\n]{1,60}?):?_?\*\*:?", re.M)
# Le condizioni dell'SRD sono voci in grassetto corsivo («**_Confused:_**») in questo file.
CONDIZIONI_SRD = "special-abilities-and-conditions"
PICCOLO = re.compile(r"<small>.*?</small>", re.S)


def norma(nome: str) -> str:
    """La chiave di confronto: minuscole, senza accenti, senza fregi."""
    s = PICCOLO.sub("", nome)
    s = re.sub(r"\[[^\]]*\]|\([^)]*\)", "", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[’'`*_]", "", s.lower())
    return re.sub(r"[^a-z0-9+]+", " ", s).strip()


def _tipo_srd(rel: str) -> str:
    for pezzo, tipo in TIPI_SRD:
        if pezzo in rel:
            return tipo
    return "regola"


def indice(cache: Path, rete: bool = True) -> dict[str, list[dict]]:
    voci: dict[str, list[dict]] = {}

    def metti(chiave, voce):
        if chiave and len(chiave) > 2:
            voci.setdefault(chiave, []).append(voce)

    base = R.assicura(R.SRD35, cache, rete=rete)
    for rel in sorted(R.SRD35.file):
        testo = (base / rel).read_text(encoding="utf-8")
        tipo = _tipo_srd(rel)
        for rx in (TITOLO, GRASSETTO):
            for m in rx.finditer(testo):
                nome = PICCOLO.sub("", m.group("n")).strip()
                tipo_v = tipo if rx is TITOLO else ("condizione" if CONDIZIONI_SRD in rel else "regola")
                metti(norma(nome), {"fonte": "srd35", "tipo": tipo_v,
                                    "nome": nome, "dove": f"{rel}:{R.riga_di(testo, m.start())}"})
    base = R.assicura(R.PF1, cache, rete=rete)
    for db in sorted(R.PF1.file):
        con = sqlite3.connect(f"file:{base / db}?mode=ro", uri=True)
        try:
            righe = con.execute("select name, type, subtype from sections where name is not null").fetchall()
        except sqlite3.Error:
            righe = []
        finally:
            con.close()
        for nome, tipo, sub in righe:
            if tipo in TIPI_PF1 or sub == "condition":
                metti(norma(nome), {"fonte": "pf1", "tipo": TIPI_PF1.get(tipo, "condizione"),
                                    "nome": nome, "dove": db})
    return voci


def carica_indice(cache: Path, rete: bool = True) -> dict[str, list[dict]]:
    file = cache / "lessico-indice.json"
    if file.is_file():
        return json.loads(file.read_text(encoding="utf-8"))
    voci = indice(cache, rete=rete)
    file.write_text(json.dumps(voci, ensure_ascii=False), encoding="utf-8")
    return voci


def carica_tabella(percorso: Path = TABELLA) -> list[dict]:
    """La tabella italiana: YAML semplice, una voce per elemento (senza pyyaml)."""
    voci, voce = [], None
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*(-\s+)?(\w+):\s*(.*?)\s*$", riga)
        if not m:
            continue
        if m.group(1):
            voce = {}
            voci.append(voce)
        valore = m.group(3).strip().strip('"')
        if voce is not None:
            voce[m.group(2)] = None if valore in ("", "null", "~") else valore
    return voci


def tabella_pf1(percorso: Path = TABELLA_PF1, tipo: str = "talento") -> dict[str, dict]:
    """Nome italiano PF1e normalizzato → voce PRD, per un tipo (talento, incantesimo, abilità, condizione)."""
    m = {}
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if riga.startswith("#") or "\t" not in riga or riga.startswith("italiano\t"):
            continue
        it, en, t = (riga.split("\t") + ["talento"])[:3]
        if t == tipo:
            m.setdefault(norma(it), {"it": it, "pf1": en, "srd35": None, "tipo": t})
    return m


def e_pf1(file: str, testo: str) -> bool:
    """Il file è di un modulo PF1e? Lo dice sistemi.toml (ADR-0111, L2), più la
    riga «Sistema» del testo; senza dmcore.sistemi (test isolati) come prima,
    dal percorso o dalla riga."""
    try:
        from dmcore.sistemi import sistema_di
        if sistema_di(file) == "pf1e":
            return True
    except Exception:  # noqa: BLE001 — ripiego chiesto dal thread delle regole
        pass
    return bool(MODULO_PF1.search(file)) or bool(re.search(
        r"^(?:\*\*)?(?:Sistema|Regole|System)(?:\*\*)?\s*:?\s*(?:\*\*)?\s*(?:Pathfinder|PF1e)", testo[:3000], re.I | re.M))


def tabella_35(percorso: Path = TABELLA_35) -> list[dict]:
    """Le voci generate italiano 3.5 → SRD 3.5, nella forma di carica_tabella()."""
    voci = []
    if not percorso.is_file():
        return voci
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if riga.startswith("#") or "\t" not in riga or riga.startswith("italiano\t"):
            continue
        it, en, tipo, abb = (riga.split("\t") + ["", ""])[:4]
        voci.append({"it": it, "srd35": en, "tipo": tipo, "abbinamento": abb})
    # «variante …» nell'abbinamento: il nome si corregge con la voce dello stesso tipo e dello stesso
    # inglese che non è una variante (per esempio la forma SRD senza il mago, DM 2026-11-07).
    giuste = {(v["tipo"], norma(v["srd35"])): v for v in voci if not v["abbinamento"].startswith("variante")}
    out = []
    for v in voci:
        g = giuste.get((v["tipo"], norma(v["srd35"]))) if v["abbinamento"].startswith("variante") else None
        if g:
            g["varianti"] = "|".join(x for x in (g.get("varianti"), v["it"]) if x)
        else:
            out.append(v)
    return out


@functools.lru_cache(maxsize=None)
def nomi_con_e() -> frozenset[str]:
    """I nomi delle tabelle che contengono « e »/« and »: non vanno divisi in due."""
    nomi = set()
    for v in tabella_35() + carica_tabella():
        nomi.update(norma(x) for x in (v.get("it") or "", v.get("srd35") or ""))
    for riga in TABELLA_PF1.read_text(encoding="utf-8").splitlines():
        if not riga.startswith("#") and "\t" in riga:
            nomi.update(norma(x) for x in riga.split("\t")[:2])
    nomi.update(talenti_dei_manuali())
    return frozenset(n for n in nomi if " e " in n or " and " in n)


@functools.lru_cache(maxsize=None)
def talenti_dei_manuali(percorso: Path = TALENTI_MANUALI) -> dict[str, dict]:
    """Nome inglese normalizzato → {srd35, manuale}: un talento che esiste in un manuale 3.5."""
    m: dict[str, dict] = {}
    if percorso.is_file():
        for riga in percorso.read_text(encoding="utf-8").splitlines():
            if riga.startswith("#") or riga.startswith("inglese\t") or "\t" not in riga:
                continue
            en, man, *_ = riga.split("\t") + [""]
            m.setdefault(norma(en), {"srd35": en, "manuale": man, "tipo": "talento"})
    return m


@functools.lru_cache(maxsize=None)
def talenti_pf1_dei_manuali(percorso: Path = TALENTI_PF1) -> set[str]:
    """Nomi inglesi normalizzati dei talenti PF1e di tutti i manuali (Archives of Nethys)."""
    if not percorso.is_file():
        return set()
    return {norma(r.split("\t")[0]) for r in percorso.read_text(encoding="utf-8").splitlines()
            if r and not r.startswith("#") and not r.startswith("inglese\t")}


@functools.lru_cache(maxsize=None)
def oggetti_campagna(percorso: Path = OGGETTI_CAMPAGNA) -> set[str]:
    """I nomi della prima colonna delle tabelle di OGGETTI-DELLA-CAMPAGNA.md, normalizzati."""
    if not percorso.is_file():
        return set()
    nomi = set()
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if riga.lstrip().startswith("|") and celle and celle[0] and celle[0] != "Nome" \
                and not set(celle[0]) <= set("-: "):
            nomi.add(norma(celle[0].strip("*_ ")))
    return nomi


def mappa_italiana(tabella: list[dict]) -> dict[str, dict]:
    m = {}
    for v in tabella:
        for nome in [v.get("it", "")] + [x.strip() for x in (v.get("varianti") or "").split("|") if x.strip()]:
            m[norma(nome)] = v
    return m


# ---------------------------------------------------------------- controllo

# Dopo «Talenti»/«Feats» l'elenco comincia con un nome (maiuscola, o corsivo/grassetto): «Feats Blind-Fight»,
# «Regional feats: Cosmopolitan», «i talenti Tiro Rapido». Non sono elenchi «more feats. Basically», «feats worth»,
# «4 metamagic feats; Spellcraft», «I talenti sono quelli di», «8 talenti (3 di livello», «Feats (1,600+ general)»,
# «Talenti e capacità».
RIGA_TALENTI = re.compile(r"\b(?i:talenti|feats)\b(?:\s+di\s+\w+)?(?:\*\*)?(?:\s*\([^)]*\))?(?:\*\*)?:?(?:\*\*)?:?[ \t]+"
                          r"(?=[*_]*[A-ZÀ-Ý])(?P<lista>.+)$")
MARCA_FUORI_SRD = re.compile(
    r"Private source|Non SRD|PF1e|Pathfinder|homebrew|della casa|\[CANONE|Celestial|"
    r"Complete |Races of|Draconomicon|Monster Manual|Manuale dei Mostri|Libro delle", re.I)


# Dove finisce l'elenco dei talenti: il campo seguente dello statblocco, una frase, una cella.
FINE_CAMPO = re.compile(
    r"\*\*[^*]{1,40}\*\*\s*:|\*\*(?:Abilit|Skills|Talenti (?:da|bonus)|Equipaggiamento|Tattiche|Lingu|"
    r"Qualit|SQ|QS\b|Ambiente|Organizzazione|Tesoro|Allineamento|Avanzamento|Attacc|Difesa|Iniziativa)|"
    r"(?<=[a-z\)])\.\s|\s—\s|\||\):\s|"
    r"(?:^|(?<=[\s·,;]))(?:Abilità|Skills|Linguaggi|Lingue|Languages|Qualità speciali|Equipaggiamento|SQ|QS|TS)\b")


# «Incidere Rune (Inscribe Rune)», «Stile del Serpente (Snake Style, PF1e)»: il nome italiano non è in tabella
# ma il DM ha messo tra parentesi il talento inglese di un manuale (2026-11-07). Si controlla l'inglese.
INGLESE_TRA_PARENTESI = re.compile(r"(?<![\w*])([A-ZÀ-Ý][^,;·()]*?)\s*\(\s*([A-Z][A-Za-z' -]+?)\s*(?:[,;][^)]*)?\)")


def _inglese_tra_parentesi(m: re.Match) -> str:
    k = norma(m.group(2))
    noto = k in talenti_dei_manuali() or k in inglesi_dei_manuali() or k in talenti_pf1_dei_manuali()
    return m.group(2) if noto else m.group(0)


def termini_della_riga(lista: str) -> list[str]:
    lista = FINE_CAMPO.split(lista.replace("Arms/Armor", "Arms and Armor"))[0]
    lista = INGLESE_TRA_PARENTESI.sub(_inglese_tra_parentesi, lista)
    lista = re.sub(r"\([^)]*\)|\([^)]*$", "", lista)  # anche la parentesi lasciata aperta dalla fine del campo
    lista = re.split(r"(?<=\S)\s{2,}(?=[A-Z])|--", lista)[0]  # «Dodge (nota) In terms of…», «Focus (x)--Bonus»
    out = []
    pezzi = []
    for p in re.split(r"[,;·]", lista):
        # «Tiro Rapido e Tiro Multiplo» sono due talenti; «Creare Armi e Armature Magiche» è uno solo.
        intero = norma(re.sub(r"\[[^\]]*\]|\*|`", "", p).strip(" .:"))
        pezzi += [p] if intero in nomi_con_e() else re.split(r"\s+(?:e|and)\s+(?=[A-Z])", p)
    for pezzo in pezzi:
        t = re.sub(r"\[[^\]]*\]|\*|`|\bB\b|\bx\d+\b|\+\d+", "", pezzo)
        t = CODA.sub("", t.replace("\u2011", "-").replace("\\", "")).strip(" .:»«")
        t = SIGLA.sub("", t)
        if 2 < len(t) < 45 and not re.search(r"\d", t) and t[0].isupper():
            out.append(t)
    return out


# «GoadCAd», «EnduranceB»: le sigle del manuale (o la B del talento bonus) attaccate al nome, come negli
# statblock dei manuali inglesi; «fonte: SRD», «opzionale» in coda. Si staccano prima di cercare il nome.
SIGLA = re.compile(r"(?<=[a-z\)])(?>(?:CMage|CAdv|CArc|CDiv|CSco|CWar|DotU|FRCS|LEoF|PHB2|RotW|CAd|CAr|CSc|CoV|DMG|DrM|Dra|ECS|EPH|HoB|LoM|MIC|MM\d?|MoF|"
                   r"PGF|PH2|PlH|RoD|RoE|RoF|RoS|SpC|ToB|Und|XPH|CC|CD|CM|CP|CS|CV|CW|FF|LM|MH|PH|SS|UA|UE|B)){1,4}$")
CODA = re.compile(r"\s+(?:fonte\s*:.*|opzionale.*)$", re.I)


_INGLESI: dict[str, dict] = {}


def inglesi_dei_manuali() -> dict[str, dict]:
    """Nome inglese → voce, per i talenti della tabella 3.5 (anche fuori SRD)."""
    if not _INGLESI:
        for v in tabella_35():
            if v["tipo"] == "talento" and v["srd35"]:
                _INGLESI.setdefault(norma(v["srd35"]), v)
    return _INGLESI


def controlla_testo(testo: str, idx: dict, ita: dict, file: str = "", pf1: dict | None = None) -> list[dict]:
    rilievi = []
    modulo_pf1 = pf1 is not None and e_pf1(file, testo)
    righe = testo.splitlines()
    for n, riga in enumerate(righe, 1):
        if riga.lstrip().startswith("#"):
            continue  # un titolo («## Feats: Key Categories») non è uno statblocco
        if re.match(r"\s*(?:>\s*)*era:", riga):
            continue  # «era: talenti …» registra la versione di prima, corretta sopra: è storia
        m = RIGA_TALENTI.search(riga)
        if not m:
            continue
        # Statblock dei manuali inglesi trascritti con «\» a fine riga: il campo continua sotto.
        k = n
        while riga.rstrip().endswith("\\") and k < len(righe) and k - n < 12:
            riga = riga.rstrip()[:-1].rstrip() + " " + righe[k].strip()
            k += 1
        m = RIGA_TALENTI.search(riga)
        # L'elenco va a capo: si legge anche la riga dopo, se continua lo stesso campo.
        if k == n and n < len(righe) and righe[n].strip() and not re.match(r"\s*(?:\*\*|[|#>`-]|\d)", righe[n]) \
                and re.search(r"[·,\w]\s*$", riga) and not FINE_CAMPO.search(m.group("lista")):
            m = RIGA_TALENTI.search(riga.rstrip() + " " + righe[n].strip())
        lista = m.group("lista")
        if re.search(r"Skills and Feats", riga):
            lista = lista.rsplit(";", 1)[-1]  # formato 3.0: le abilità, poi «;» e i talenti
        for t in termini_della_riga(lista):
            k = norma(t)
            if modulo_pf1:
                v = pf1.get(k)
                if v:
                    esito = "tabella"
                elif ita.get(k):
                    esito, v = "nome 3.5", ita.get(k)
                elif any(e["fonte"] == "pf1" for e in idx.get(k, [])):
                    esito = "fonte"
                elif k in talenti_pf1_dei_manuali():
                    esito = "fonte"  # nome inglese di un talento PF1e fuori dal PRD (Archives of Nethys)
                elif MARCA_FUORI_SRD.search(riga.replace("PF1e", "").replace("Pathfinder", "")):
                    esito = "marcato"
                else:
                    esito = "sconosciuto"
                rilievi.append({"file": file, "riga": n, "termine": t, "esito": esito, "sistema": "pf1",
                                "srd35": None, "pf1": (v or {}).get("pf1")})
                continue
            v = ita.get(k)
            if v and k != norma(v.get("it", "")):
                esito = "variante"
            elif v:
                esito = "tabella"
            elif k in idx:
                esito = "fonte"
            elif k in inglesi_dei_manuali():
                # nome inglese di un talento di un manuale ufficiale (5° Clone): esiste, il nome
                # italiano è in tabella; la correzione dei booklet lo porta in italiano.
                esito, v = "fonte", inglesi_dei_manuali()[k]
            elif k in talenti_dei_manuali():
                # nome inglese di un talento di un manuale 3.5 non tradotto in tabella (indice dei manuali)
                esito, v = "fonte", talenti_dei_manuali()[k]
            elif MARCA_FUORI_SRD.search(riga):
                esito = "marcato"
            else:
                esito = "sconosciuto"
            rilievi.append({"file": file, "riga": n, "termine": t, "esito": esito,
                            "sistema": "3.5", "srd35": (v or {}).get("srd35"), "pf1": (v or {}).get("pf1")})
    return rilievi


# Gli altri campi dello statblocco (ADR-0110, lotto 2): incantesimi e capacità magiche, abilità, oggetti.
# Il tipo è quello delle tabelle; i nomi si leggono dai corsivi (incantesimi, oggetti) o prima del bonus (abilità).
CAMPI = (
    ("incantesimo", re.compile(
        r"^\W{0,6}(?:Incantesimi|Capacità magiche|Spells|Spell-Like Abilities|Spell-like abilities)\b(?P<lista>.*)$", re.I)),
    ("abilità", re.compile(r"^\W{0,6}(?:Abilità|Skills)\b\W{0,6}(?P<lista>[^\n]*[+−-]\d.*)$", re.I)),
    ("oggetto magico", re.compile(
        r"^\W{0,6}(?:Equipaggiamento|Possedimenti|Gear|Combat Gear|Other Gear|Oggetti magici)\b(?P<lista>.*)$", re.I)),
)
CORSIVO = re.compile(r"(?<![*\w])\*(?!\*)(?P<n>[^*\n]{3,60}?)\*(?!\*)|(?<![_\w])_(?P<m>[^_\n]{3,60}?)_(?![_\w])")
NON_NOME = re.compile(r"\d|\b(?:a volontà|at will|giorno|day|CD|DC|LI|CL|livello|level|conosciut|prepar|inutile)\b", re.I)


def termini_del_campo(tipo: str, lista: str) -> list[str]:
    if tipo == "abilità":
        out = []
        for pezzo in re.split(r"[,;·]", re.sub(r"\([^)]*\)", "", lista)):
            m = re.match(r"\s*\**\s*(?P<n>[A-Za-zÀ-ÿ’' ]{3,40}?)\s*\**\s*[+−-]\s*\d", pezzo)
            if m:
                out.append(m.group("n").strip())
        return out
    out = []
    for m in CORSIVO.finditer(lista):
        for t in re.split(r"\s*[,;/]\s*", m.group("n") or m.group("m")):
            t = re.sub(r"\s*[+−-]\s*\d+\s*$", "", t.strip(" .,:;"))
            if t and not NON_NOME.search(t) and len(t.split()) <= 7:
                out.append(t)
    return out


# «pozione di cura ferite gravi», «bacchetta di dardo incantato»: il nome dopo è un incantesimo.
CONTENITORE = re.compile(r"^(?:pozion[ei]|pergamen[ae]|bacchett[ae]|olio|oli|potions?|scrolls?|wands?|oils?)"
                         r"\s+(?:di|del|della|dello|dell|of)\s+(?P<n>.+)$", re.I)


# «anello di protezione», «verga della negazione»: nelle tabelle del GDM e di Mephit c'è solo il resto.
PORTATORE = re.compile(r"^(?:anell[oi]|verg[ae]|baston[ei]|rings?|rods?|staffs?)\s+"
                       r"(?:dell['’]|della|dello|delle|degli|dei|del|di|of(?:\s+the)?)\s*(?P<n>\S.*)$", re.I)


def composto(t: str, equip: dict, proprieta: dict) -> bool:
    """«Martello da guerra sacro»: un'arma o armatura della tabella più proprietà magiche note.

    Le proprietà sono aggettivi: si confrontano senza la vocale finale (sacra/sacro, affilata/affilato).
    """
    parole = norma(t).split()
    radici = {norma(k)[:-1] for k in proprieta if " " not in k}
    for i in range(len(parole) - 1, 0, -1):
        if " ".join(parole[:i]) in equip and all(p[:-1] in radici for p in parole[i:]):
            return True
    return False


def tabelle_per_tipo() -> tuple[dict[str, dict], dict[str, dict]]:
    """{tipo: {chiave italiana: voce}} per la 3.5 (tsv e yaml curato) e per PF1e."""
    t35: dict[str, dict] = {"proprietà magica": {}}
    for v in tabella_35() + carica_tabella():
        tipo = v.get("tipo") or "talento"
        tipo = "oggetto magico" if tipo == "oggetto" else tipo
        for nome in [v.get("it", "")] + [x.strip() for x in (v.get("varianti") or "").split("|") if x.strip()]:
            t35.setdefault(tipo, {})[norma(nome)] = v
    tpf: dict[str, dict] = {}
    for tipo, _ in CAMPI:
        tpf[tipo] = tabella_pf1(tipo=tipo)
    tpf["proprietà magica"] = tabella_pf1(tipo="proprietà magica")
    tpf["oggetto magico"].update(tpf["proprietà magica"])
    tpf["equipaggiamento"] = tabella_pf1(tipo="equipaggiamento")
    return t35, tpf


GRADO = re.compile(r"^(greater|lesser|mass|improved|superior|communal|major|minor)\s+(.+)$")


def chiavi_inglesi(k: str) -> list[str]:
    """«greater teleport» si cerca anche come «teleport greater», l'ordine dei titoli dell'SRD."""
    m = GRADO.match(k)
    return [k, f"{m.group(2)} {m.group(1)}"] if m else [k]


def controlla_campi(testo: str, idx: dict, t35: dict, tpf: dict, file: str = "") -> list[dict]:
    """Incantesimi, abilità e oggetti magici dei campi dello statblocco, contro le tabelle del loro tipo."""
    rilievi = []
    modulo_pf1 = e_pf1(file, testo)
    fonte = "pf1" if modulo_pf1 else "srd35"
    for n, riga in enumerate(testo.splitlines(), 1):
        for tipo, rx in CAMPI:
            m = rx.search(riga)
            if not m:
                continue
            for t in termini_del_campo(tipo, m.group("lista")):
                tipo_t = tipo
                c = CONTENITORE.match(t) if tipo == "oggetto magico" else None
                if c:
                    t, tipo_t = c.group("n"), "incantesimo"
                k = norma(t)
                tab = tpf.get(tipo_t, {}) if modulo_pf1 else t35.get(tipo_t, {})
                if tipo_t == "oggetto magico":
                    tab = {**(tpf if modulo_pf1 else t35).get("equipaggiamento", {}), **tab}
                    p = PORTATORE.match(t)
                    if k not in tab and p and norma(p.group("n")) in tab:
                        k = norma(p.group("n"))
                v = tab.get(k)
                tabs = tpf if modulo_pf1 else t35
                if (not v and tipo_t == "oggetto magico"
                        and composto(t, tabs.get("equipaggiamento", {}), tabs.get("proprietà magica", {}))):
                    v = {"it": t}
                if v and not modulo_pf1 and k != norma(v.get("it", "")):
                    esito = "variante"
                elif v:
                    esito = "tabella"
                elif modulo_pf1 and t35.get(tipo_t, {}).get(k):
                    esito, v = "nome 3.5", t35[tipo_t][k]
                elif any(e["fonte"] == fonte for ch in chiavi_inglesi(k) for e in idx.get(ch, [])):
                    esito = "fonte"
                elif tipo_t == "oggetto magico" and k in oggetti_campagna():
                    esito = "campagna"
                elif MARCA_FUORI_SRD.search(riga):
                    esito = "marcato"
                else:
                    esito = "sconosciuto"
                rilievi.append({"file": file, "riga": n, "termine": t, "esito": esito, "tipo": tipo,
                                "sistema": "pf1" if modulo_pf1 else "3.5",
                                "en": (v or {}).get("pf1" if modulo_pf1 else "srd35")})
            break
    return rilievi


def risolvi(termine: str, idx: dict, ita: dict) -> dict:
    """Il termine nelle due fonti: dalla tabella italiana se c'è, se no dall'indice."""
    v = ita.get(norma(termine))
    if v:
        return {"srd35": v.get("srd35"), "pf1": v.get("pf1"), "da": "tabella", "nota": v.get("nota")}
    out = {"srd35": None, "pf1": None, "da": "indice", "nota": None}
    for e in idx.get(norma(termine), []):
        out[e["fonte"]] = out[e["fonte"]] or e["nome"]
    return out


def verifica_tabella(tabella: list[dict], idx: dict) -> list[str]:
    """Ogni nome inglese della tabella deve stare nella sua fonte."""
    errori = []
    for v in tabella:
        for f in ("srd35", "pf1"):
            n = v.get(f)
            if n and not any(e["fonte"] == f for e in idx.get(norma(n), [])):
                errori.append(f"{v.get('it')}: {f} «{n}» non è nella fonte")
    return errori


def misura_casi(casi: list[dict], idx: dict, ita: dict) -> list[dict]:
    out = []
    for c in casi:
        r = risolvi(c["termine"], idx, ita)
        giusto = all(norma(r[f] or "") == norma(c.get(f) or "") for f in ("srd35", "pf1"))
        out.append({**c, "trovato_srd35": r["srd35"], "trovato_pf1": r["pf1"], "giusto": giusto})
    return out


def file_da(percorsi: list[str], volumi: bool = False) -> list[Path]:
    out = []
    for p in map(Path, percorsi):
        p = p if p.is_absolute() else ROOT / p
        out += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    return [f for f in out if f.is_file() and (volumi or ".hb.md" not in f.name)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", help="cartella della cache dell'SRD (vedi riscontro_srd.py)")
    ap.add_argument("--offline", action="store_true", help="non scaricare: solo cache")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("indice")
    c = sub.add_parser("cerca")
    c.add_argument("nome")
    sub.add_parser("verifica-tabella")
    m = sub.add_parser("casi")
    m.add_argument("file")
    m.add_argument("--check", action="store_true")
    k = sub.add_parser("controlla")
    k.add_argument("percorsi", nargs="*", help="file o cartelle; con --tutto, il repo fuori da plans/")
    k.add_argument("--tutto", action="store_true",
                   help="tutte le cartelle del repo tranne plans/ (storia, ADR-0109), scripts/ e .github/")
    k.add_argument("--massimo-sconosciuti", type=int, default=None,
                   help="con --check: fallisce se i talenti sconosciuti superano questo numero (ratchet)")
    k.add_argument("--json", action="store_true")
    k.add_argument("--check", action="store_true")
    k.add_argument("--volumi", action="store_true", help="legge anche i volumi .hb.md generati (conto prima e dopo dei booklet)")
    k.add_argument("--campi", action="store_true",
                   help="anche incantesimi, abilità e oggetti magici dei campi dello statblocco (conto per tipo)")
    a = ap.parse_args(argv)
    cache = R.cartella_cache(a.cache)

    if a.cmd == "indice":
        (cache / "lessico-indice.json").unlink(missing_ok=True)
        idx = carica_indice(cache, rete=not a.offline)
        print(f"lessico: {len(idx)} termini in {cache / 'lessico-indice.json'}")
        return 0
    idx = carica_indice(cache, rete=not a.offline)
    # Le voci curate di lessico_it.yaml prevalgono su quelle generate di lessico_it_35.tsv.
    ita = {**mappa_italiana(tabella_35()), **mappa_italiana(carica_tabella())}
    if a.cmd == "verifica-tabella":
        errori = verifica_tabella(carica_tabella(), idx)
        print("\n".join(errori) or f"lessico: tabella ok, {len(carica_tabella())} voci tutte nelle fonti")
        return 1 if errori else 0
    if a.cmd == "casi":
        casi = json.loads(Path(a.file).read_text(encoding="utf-8"))["casi"]
        esiti = misura_casi(casi, idx, ita)
        for e in esiti:
            if not e["giusto"]:
                print(f"SBAGLIATO «{e['termine']}»: atteso 3.5 {e.get('srd35')} / PF1e {e.get('pf1')}, "
                      f"trovato {e['trovato_srd35']} / {e['trovato_pf1']}")
        giusti = sum(e["giusto"] for e in esiti)
        print(f"lessico: {giusti} casi giusti su {len(esiti)}")
        return 1 if a.check and giusti < len(esiti) else 0
    if a.cmd == "cerca":
        k_ = norma(a.nome)
        v = ita.get(k_)
        chiavi = [k_] + ([norma(x) for x in (v.get("srd35"), v.get("pf1")) if x] if v else [])
        trovate = [e for ch in dict.fromkeys(chiavi) for e in idx.get(ch, [])]
        if v:
            print(f"tabella: {v.get('it')} → 3.5 {v.get('srd35') or '—'} → PF1e {v.get('pf1') or '—'}"
                  + (f" ({v['nota']})" if v.get("nota") else ""))
        for e in trovate:
            print(f"{e['fonte']:6} {e['tipo']:12} {e['nome']}  [{e['dove']}]")
        return 0 if trovate or v else 1
    pf1 = tabella_pf1()
    percorsi = list(a.percorsi)
    if a.tutto:
        percorsi += [str(d) for d in sorted(ROOT.iterdir()) if d.is_dir()
                     and d.name not in ("plans", "scripts", ".git", ".github") and not d.name.startswith(".")]
        percorsi += [str(f) for f in sorted(ROOT.glob("*.md"))]
    if not percorsi:
        ap.error("controlla: servono dei percorsi, o --tutto")
    # Le righe dei talenti si confrontano solo con i talenti della tabella.
    ita_t = {k: v for k, v in ita.items() if v.get("tipo", "talento") == "talento"}
    rilievi = [r for f in file_da(percorsi, a.volumi)
               for r in controlla_testo(f.read_text(encoding="utf-8", errors="ignore"), idx, ita_t,
                                        str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f), pf1)]
    ignoti = [r for r in rilievi if r["esito"] in ("sconosciuto", "variante", "nome 3.5")]
    if a.campi:
        t35, tpf = tabelle_per_tipo()
        campi = [r for f in file_da(percorsi, a.volumi)
                 for r in controlla_campi(f.read_text(encoding="utf-8", errors="ignore"), idx, t35, tpf,
                                          str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f))]
        if a.json:
            rilievi = rilievi + campi
        else:
            for r in campi:
                if r["esito"] in ("variante", "nome 3.5", "sconosciuto"):
                    print(f"{r['file']}:{r['riga']}: {r['tipo']} {r['esito']} «{r['termine']}»"
                          + (f" → {r['en']}" if r.get("en") else ""))
            for tipo, _ in CAMPI:
                rr = [r for r in campi if r["tipo"] == tipo]
                print(f"lessico campi: {tipo} {len(rr)} letti · " + " · ".join(
                    f"{e} {sum(1 for r in rr if r['esito'] == e)}"
                    for e in ("tabella", "fonte", "campagna", "marcato", "variante", "nome 3.5", "sconosciuto")))
    if a.json:
        print(json.dumps(rilievi, ensure_ascii=False, indent=1))
    else:
        for r in ignoti:
            cosa = {"variante": "variante non ufficiale", "nome 3.5": "nome 3.5 in un modulo PF1e"}.get(
                r["esito"], "talento sconosciuto")
            print(f"{r['file']}:{r['riga']}: {cosa} «{r['termine']}»")
        conti = {e: sum(1 for r in rilievi if r["esito"] == e) for e in ("tabella", "fonte", "marcato", "variante", "nome 3.5", "sconosciuto")}
        print(f"lessico: {len(rilievi)} talenti letti · " + " · ".join(f"{k} {v}" for k, v in conti.items()))
    if not a.check:
        return 0
    # Varianti e nomi 3.5 nei moduli PF1e hanno sempre il nome giusto in tabella: bloccano subito.
    # Gli sconosciuti chiedono il DM o una marca: il ratchet impedisce solo che crescano.
    sbagliati = [r for r in ignoti if r["esito"] != "sconosciuto"]
    sconosciuti = len(ignoti) - len(sbagliati)
    if a.massimo_sconosciuti is None:
        return 1 if ignoti else 0
    if sconosciuti > a.massimo_sconosciuti:
        print(f"lessico: {sconosciuti} talenti sconosciuti, più del massimo {a.massimo_sconosciuti}: "
              "usa il nome della tabella, o marca la fonte (GUIDA-MARCATURE)", file=sys.stderr)
    return 1 if sbagliati or sconosciuti > a.massimo_sconosciuti else 0


if __name__ == "__main__":
    sys.exit(main())
