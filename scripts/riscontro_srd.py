#!/usr/bin/env python3
"""
riscontro_srd.py — riscontra le regole dei master sull'SRD 3.5 e sul PRD PF1e.

Nato dalla prova di ``plans/esperimenti/ricerca-rete-2026-10-23/`` (§3 di
RICERCA.md): le regole che un giro di lettori controlla «a memoria» si
riscontrano sul testo delle due fonti aperte, e la prova ha trovato una
discordanza vera (la *freccia assassina* di DEF-2). Canale **testing** di
ADR-0099; la decisione è ADR-0103.

Le fonti, entrambe Open Game Content sotto OGL 1.0a:

  - SRD 3.5 in Markdown, ``olimot/srd-v3.5-md`` (Wizards of the Coast; la
    Product Identity è esclusa, vedi ``basic-rules-and-legal/legal-information.md``);
  - PRD di Pathfinder 1e in SQLite, ``devonjones/PSRD-Data`` (Paizo; l'avviso
    è nel libro ``book-ogl.db``).

Si scaricano da ``raw.githubusercontent.com`` a un commit fissato, file per
file, e ogni file si controlla con lo sha256 scritto qui sotto. Stanno in una
cache **fuori dal repo**: ``--cache``, oppure ``$RUMBLINGSTONE_SRD_CACHE``,
oppure ``$XDG_CACHE_HOME/rumblingstone/srd``, oppure
``~/.cache/rumblingstone/srd``. Nel repo non entra niente delle due fonti.

Uso:
    python3 scripts/riscontro_srd.py scarica                 # rete: riempie la cache
    python3 scripts/riscontro_srd.py scarica --da-cartella srd35=DIR pf1=DIR
                                                             # da cloni già fatti
    python3 scripts/riscontro_srd.py scarica --verifica      # rifà gli sha256
    python3 scripts/riscontro_srd.py regola "Slaying Arrow"  # una regola per nome
    python3 scripts/riscontro_srd.py riscontra FILE.yaml [--md OUT] [--json OUT] [--strict]
    python3 scripts/riscontro_srd.py licenza                 # dove sta il testo OGL

Il file dei riscontri (YAML o JSON) ha una chiave ``riscontri``, un elenco.
Ogni voce:

    id, cosa           chi l'ha chiesto e che cosa si controlla
    fonte              srd35 | pf1
    file               (srd35) il file dell'SRD; senza, si cerca in tutti
    libro, sezione     (pf1) il database e il nome della sezione; senza
                       libro, in tutti
    regola             regex che deve stare nella fonte; il gruppo (?P<v>...)
                       è il valore da confrontare
    regola_non         regex che NON deve stare nel passo trovato (facoltativa)
    master             il file del repo che afferma la regola (facoltativo)
    affermazione       regex nel master, con il suo gruppo (?P<v>...); conta
                       ogni occorrenza
    confronto          presenza (default) | numero | termine
    scala              per numero: il valore della fonte si moltiplica per
                       questo (0.3 da piedi a metri)
    tolleranza         per numero, default 1e-6
    equivale           per termine: {valore della fonte: [forme accettate]}

Esiti: **concorda**, **discorda**, **non trovata** (nella fonte o nel master),
ognuno con la citazione: file e riga dell'SRD, oppure libro e sezione del PRD,
e file e riga del master. Il confronto «numero» e «termine» lo fa lo script;
«presenza» dice solo che la regola sta nella fonte e l'affermazione nel master.

Exit: 0 rapporto prodotto (anche con discordanze) · 1 con --strict, una
discordanza o una regola non trovata; oppure uno sha256 che non combacia;
oppure ``regola`` senza risultati · 2 errore d'uso (file dei riscontri
illeggibile, regex sbagliata) · 3 fonti non disponibili: la cache non le ha e
la rete non risponde (o ``--offline``). Lo dice sempre, non tace.

Legge il repo; scrive solo nella cache e in --md/--json. Rete solo per
``scarica`` o quando la cache è incompleta.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ESITO_RETE = 3

URL_RAW = "https://raw.githubusercontent.com/{repo}/{commit}/{path}"


@dataclass
class Fonte:
    chiave: str
    nome: str
    repo: str
    commit: str
    licenza: str
    file_licenza: str
    file: dict[str, str] = field(default_factory=dict)

    def cartella(self, cache: Path) -> Path:
        return cache / f"{self.repo.split('/')[-1]}-{self.commit[:12]}"


#: Fissate il 2026-10-23 dai cloni della ricerca in rete; sha256 di ogni file
#: com'è servito da raw.githubusercontent.com a quel commit.
SRD35 = Fonte(
    chiave="srd35",
    nome="SRD 3.5",
    repo="olimot/srd-v3.5-md",
    commit="c7f30a0ce11a579f75456746f278a4c75f67b4c1",
    licenza=("Open Game License 1.0a. System Reference Document © 2000-2003 "
             "Wizards of the Coast, Inc.; la Product Identity elencata nel "
             "file della licenza non è Open Content."),
    file_licenza="basic-rules-and-legal/legal-information.md",
    file={
        "basic-rules-and-legal/alignment-and-description.md": "eae3e1f35255a8a7e8824becab24464e4e0ab9a43967f58fb21a20966665a631",
        "basic-rules-and-legal/basics-and-ability-scores.md": "c5282cd309966f771bdc04cd19929a1c32bb34200a0e567048eda80205057f69",
        "basic-rules-and-legal/carrying-movement-and-exploration.md": "1fd3ff8ccef1ef75a26da555edb253a5bb1ba2b3e9bccab6066774d9390e96b1",
        "basic-rules-and-legal/character-classes-i.md": "c8d7806972abdfbf7aa0fa27c4e1af17e65d722738939df6507c5d758364b0aa",
        "basic-rules-and-legal/character-classes-ii.md": "c0ff9256588acec9b11fc1b743a0d332d52f5dbb792ac5c937854c1903d6d537",
        "basic-rules-and-legal/combat-i-basics.md": "b80cb8f476b3cc0e7922596688d84b0b7528b89bf3df76e573fd3d5b0f6165d3",
        "basic-rules-and-legal/combat-ii-movement-modifiers-and-special-actions.md": "964fdfdf8f7bf449df77745eba63800f5e3218c9c4ff9f8cf750b3ea654b1229",
        "basic-rules-and-legal/equipment.md": "9fafe6009b85ade1162a3ecde8656641c5c123ba4d33238f7a419aaa8e0d2f6b",
        "basic-rules-and-legal/feats.md": "0cb39f29808f581d118c667881c4b30ed3614429277725e95f79680e86937f3c",
        "basic-rules-and-legal/legal-information.md": "eaa0efada1aeea322e6dd4dd4d4cf0d2a52974b4ac13becdfabfd6e7596a1c18",
        "basic-rules-and-legal/npc-classes.md": "ce88859b653c9a8db8985b1a8828d0f789c59d7651f0ec9c70b7cbbacb8f2df1",
        "basic-rules-and-legal/planes.md": "d3582281ea553d39f8291505db22d1906c0a88d3dde360fc7eb87d72d2f01ca5",
        "basic-rules-and-legal/prestige-classes.md": "8a9dd907dd7f7cc76a6e0eaf47dfd009c8ddb2ee63d417974960f7b2777830b6",
        "basic-rules-and-legal/races.md": "aec246b52170180303852af6785f60cc4b7e23580d1f7b9f130b21936a616bd4",
        "basic-rules-and-legal/skills-i.md": "e8cb461960f53ab1d53268093ea4bf7b3f5a24ba78ee9b5d6c57b0a5ee741fb6",
        "basic-rules-and-legal/skills-ii.md": "697cd15c05efa788bb4068a9f423c99edc20c1f15db525fadc44b0cea8b18501",
        "basic-rules-and-legal/special-abilities-and-conditions.md": "1b028af9c2e625c892c3ff9b07f526e6e0a072ec4c9f40883d746d65c1f575aa",
        "basic-rules-and-legal/special-materials.md": "5702ba682bf95c0a1d491d79e969d2075885d3e17b4da53990503f676b8c94ff",
        "basic-rules-and-legal/traps.md": "33c9b4cd8bd72ca31a337cef4ffc060ea91f63902631cc29bdddd411f8a233c9",
        "basic-rules-and-legal/treasure.md": "3a715aa04843fbb01e42471e2fc7f7f72cd2586d8c9114f6a8b2135e2f1dfb3e",
        "basic-rules-and-legal/types-subtypes-and-special-abilities.md": "c8ece11312246fdab4d7760a1fd035bb3568b5a8d8768b1a2eab1bbcc3857be2",
        "basic-rules-and-legal/wilderness-weather-and-environment.md": "59908fd402b7734b8a2ae3543b30deed6c6881788e529438d539678910923a04",
        "divine/divine-abilities-and-feats.md": "42afc38716805155f62a07ff84c45ea053d38e6a81dac8774ba4b9a7f71f08a2",
        "divine/divine-domains-and-spells.md": "6f77bd275a846d5c179c34f6a0105f52208bba3d2207273e0766efa42442fc3a",
        "divine/divine-minions.md": "57b1513d141a4269ee7dc3ca8aec85e88597f8f7c01171b207ff52489193f996",
        "divine/divine-ranks-and-powers.md": "2292ee4c7c4edea2a36164900aa7d386332d138bad87b562d0e0cdf360751bca",
        "epic/epic-classes.md": "a04dcbe3f5ae003eb6fd292248bfcf6599542ff6de3fc97a7e824b5be3955d58",
        "epic/epic-feats.md": "44b8acdabc2d037036e8665a55a5bfb03837475c903eedc9bd1dbf8f53090cf8",
        "epic/epic-level-basics.md": "583a08ebdbd360b77e474067c69175c2a41686c948c4becba8374fc558675ee3",
        "epic/epic-magic-items-1.md": "becb2af6afceb0218fe85a61d7fb62765d8677fa78305019c9490067c7452ba0",
        "epic/epic-magic-items-2.md": "44b36bf50543abd32b1cafa93b77d1fbdf8283473405d329259b562e6da38627",
        "epic/epic-monsters-a-e.md": "cd78af8a335ba10ac4bf2d851f6d184c8df0c26a022cd7096b82cbf0c32d3edc",
        "epic/epic-monsters-g-w.md": "e78ef97ddd69d4d7b7f2008158c34fa3bc395803b52c71587f93cdd18ad34254",
        "epic/epic-obstacles.md": "5c98691b0d656fe582a3e675ac408f20bf9ad0885efd4d3b17ed41a0b4007974",
        "epic/epic-prestige-classes.md": "3be0be570419298601d62fd49c71f0b19d18f4982041ca18064c7463a0cc82ea",
        "epic/epic-skills.md": "e86a01d5c56a38fc0f21e15732c4450363b87cc359e8665fc9ad386a870981fd",
        "epic/epic-spells.md": "06ca265c831718667cbb8ac416bad6682bca1a0e02b38d7ccd60e5ea175004b6",
        "magic-items/magic-items-i-basics-and-creation.md": "3702c37368abc7a5039c6fd813cb3c436b857a6b3fe0c44865ace59071bbe5fb",
        "magic-items/magic-items-ii-armor-and-weapons.md": "43f636ddbe6287a6b108f1aa99737b0d40220a782f18a2db05aec4d270b6b9b6",
        "magic-items/magic-items-iii-potions-rings-and-rods.md": "430c3a94c5e4719f25f6f51c9f307309d1eee83e188014e3a6208d9c26761274",
        "magic-items/magic-items-iv-scrolls-staffs-and-wands.md": "0144fb10255f6b15cc27f749d2e1710083374684182fc17c0b36625fcc180a1b",
        "magic-items/magic-items-v-wondrous-items.md": "912fcb6c7344b9cc179470235702a5d257c30a2c89a735353eb54dac87088c29",
        "magic-items/magic-items-vi-intelligent-cursed-and-artifacts.md": "5b7eaa43dccd30297108a45bac653afaf5766fc2ac9e0231305acc09862f42ce",
        "monsters/improving-monsters.md": "ac4747c77f5de2ec95824c0a2abf70fa79559ae7866087a12e612691b0db22a1",
        "monsters/monster-feats.md": "6f86453bfd7a4660b0b41573614ac7bef86924b258cf7210734e6eb63a4201c4",
        "monsters/monsters-animals.md": "28d22da97378f85196b16f19702c7c348297c5a4440c3c8713badc0027ed3ee2",
        "monsters/monsters-as-races.md": "178475359557af6b352b6c5e37ba7ccb36774793734eadbe36900635c4169959",
        "monsters/monsters-b-c.md": "0d5fa3d732ae2503e146d745891c53e7ffe4bdc7f7df6b5803231878ff80c23f",
        "monsters/monsters-d-de.md": "c4d6512d2d2b2d77a548d5d8167b8f36a890505c1317ee9a29e1f9ff8a51e192",
        "monsters/monsters-di-do.md": "c122cea94766f5fb0a15a42f1345240c502ea3ad0445e71672963a81b687f20e",
        "monsters/monsters-dr-dw.md": "056c89c4abecc899ab192d0b25288dfc5b9e9f726cbf29f0b5f35028c33814e8",
        "monsters/monsters-e-f.md": "4e78466792f661956bd262086802238c70bceea4ec5eb3d7598a87e41bac2fd1",
        "monsters/monsters-g.md": "edb70c538d2aa89d3e695c1889c5d0b73c62c639c57ef93d5d6a425de93d066e",
        "monsters/monsters-h-i.md": "621d791b3fefd9bd2301559a062fda572eb2d22e5d2404995ef5c0b16f790163",
        "monsters/monsters-intro-a.md": "283348e6fc37ac7b920081a991043887d5147870d32f505180f46f205d6f46d6",
        "monsters/monsters-k-l.md": "cba978b4b07c18dd616c77aadf15a2e683d125f9924d8b4a878b4944cd012044",
        "monsters/monsters-m-n.md": "b2fc0530f557cdf29d5e0282831f5438481fbcbf00f22b68c6c293a9a566fe47",
        "monsters/monsters-o-r.md": "9f1164e48dd5e68047121840b11ad13cd0634e5e919d7f31fd5ac99422714d6d",
        "monsters/monsters-s.md": "0ccf20d62183d71bc61bf2c2be1c6a49004d2b40ff04bb540bf4956d06cc87bb",
        "monsters/monsters-t-z.md": "44d160d4c91daab01d95abc56e5591f9b62b433b7b9e9f8a52fc4c4d9acb9518",
        "monsters/monsters-vermin.md": "9559cdf76b2d1bc73f226e4514770c0274bb230d94a9c908bc91d9d59e8f3ab0",
        "psionics/psionic-classes.md": "d1b16d63b0a7c481031536420ba2167553e281508a7c386312a0c532eea85b5a",
        "psionics/psionic-feats.md": "004906a9bcef6056c21fb4742fd38d3bd4cf662d214a8ad4a6c9c782b37a939e",
        "psionics/psionic-items.md": "093805966f3337099188852a728df43733c7ffdc0be212ef1d49abb9fcbf4451",
        "psionics/psionic-monsters.md": "90358d354d494ac6fd05c5903e3b65c92904c5d7bc1256946535ca3d311cbeb4",
        "psionics/psionic-powers-a-c.md": "1ec2e7f14e40b27f66961a3163b142507dc9e47dd2e61ffd1e17092f27fbd003",
        "psionics/psionic-powers-d-f.md": "0883dacf863663f1e4b2fd83d7f88f3f08df10ff33ae0f3ff9614023e80b003d",
        "psionics/psionic-powers-g-p.md": "431dbc694027e8ebb86345d134a310d82dbcb3e403c36a080a6773a84a78b8d5",
        "psionics/psionic-powers-list.md": "55fd8703570ea8fbc444efce410fbc169b6ab662fdc2aa0c7e6b5823e27fcd9a",
        "psionics/psionic-powers-overview.md": "30aa00336dc9c0a0d823f0b579296f81f17e5ebd20b13906ec10858c5a018919",
        "psionics/psionic-powers-q-w.md": "6bf1ce94a5ade8a67c3034cfae63c233178919c4218a469743bd68072df463d5",
        "psionics/psionic-races.md": "525ffda354ca75624c8cdc0a930d2e1ec4b39a2ca375b4d9a00f7acd461efbc5",
        "psionics/psionic-skills.md": "4c9cbd5170522eeb6b4226d735569e3d2c48e94614986f8f420eec5c1d984b5c",
        "psionics/psionic-spells.md": "238bc961c1a9b2110a49c0ad3df992f42422e4347837b9ff5041fce02dc9463b",
        "spells/magic-overview.md": "04f5bc9be251f73cef7a6f52ae7e4a9eaf3075c684a170161a57e5d57b73bf35",
        "spells/spell-list-i.md": "d630da3efa8520a1c92dc126b98e5b29eab48bac145c771fc54cb21be1270460",
        "spells/spell-list-ii.md": "15f368e79e860d697fce4569fe337da05b25aafeba9aab1f03ca8ef410ca9ecc",
        "spells/spells-a-b.md": "499fea42d591765acc033994915e92463503e153d1378db3fbd09f65da5efcb2",
        "spells/spells-c.md": "0c01f59c4d8a0ed68fb6a4ee763e357aa04c2c7bd492bd86ea64ca9449eaa545",
        "spells/spells-d-e.md": "d974d9150e5fe3e1b489db3f0acb19c6e4faa26541743bdfc713035ee83c6b75",
        "spells/spells-f-g.md": "1ffc41791f62d60b0b15be52bce1421d3525e7ccac79d16bdfb3e4cbc582ff8e",
        "spells/spells-h-l.md": "6bd81adb02a291b6102f910f1d7004566c3eb6bd0a55d01ada8eafe8e0376e1d",
        "spells/spells-m-o.md": "6c7cc51905361f79c85bc863e0043b4d1b803db3500f9b9bd35e42ad6c703d43",
        "spells/spells-p-r.md": "be2b68582bd1fd2ed4eac8413bf156e6a0feddba145aa756e4caa601a01805bb",
        "spells/spells-s.md": "a7f4a6d69936b1d3036553bf61be7e043adda1e323e9276c55524e23c67e5e0a",
        "spells/spells-t-z.md": "3695d357c8b497ff84acd70d787cf3a3ab9c5fb22a946df8936cb0847c7239cd",
    },
)

PF1 = Fonte(
    chiave="pf1",
    nome="PRD PF1e",
    repo="devonjones/PSRD-Data",
    commit="76ea4784604145ba3dea40eb56f83bb904759467",
    licenza=("Open Game License 1.0a. Pathfinder Roleplaying Game Reference "
             "Document © Paizo Publishing, LLC; avviso e sezione 15 nel "
             "libro book-ogl.db."),
    file_licenza="book-ogl.db",
    file={
        "book-acg.db": "b5028bda1a6ec73dd59274818a6f1b4476f9fa00455582c635326e07080ef4fc",
        "book-apg.db": "4a0c20cbfeba5380c6d45843dc900fc37e6de889bd54fdea12714467e253616c",
        "book-arg.db": "4e315e8544db87fe9a9f04fa25667d869e121976a4c8e9af7a10f2fda64aef97",
        "book-b1.db": "a7ac330dd0dae5f0bf1098a8f94c4e44d3bb696e3f25b156cb16400dc3188fed",
        "book-b2.db": "096a6e6a0d2061f7aca3a82b2ca9deab7f046ab3882fdf2c97e5676cbf2beb25",
        "book-b3.db": "be2bdb22e5eb2a77ce3ea78eb135c15a0a70893cbed1e9debdb69addeb72e64c",
        "book-b4.db": "fc138687c1eac32d78295321486ad6057764720bf74bb911dec4ddc4b6edaabd",
        "book-cr.db": "28d0b07b1da94061220561b29c81cfcece25f79291537d0ff2f7b84d982440ab",
        "book-gmg.db": "a870bc0d0e7d461fb05c6c9747b29ae407d86d1b72db5086507c00ed75d2b8d2",
        "book-ma.db": "d8cad9b71251335f3f8d981f71700361255bda8fea31f01b0c77a7f67cc224bd",
        "book-mc.db": "3d0b8454151c5f6886fe82f3327aba083df0abbe3f1feeca852d058dc515fed1",
        "book-npc.db": "00907c6c65a9fbb19ac97014b167ea82ca5e00b63d847169490045abf791eb26",
        "book-ogl.db": "1bf702e44699af26b398efffd75c89c5efd2ab18d3f91515c3af895370986a8a",
        "book-tech.db": "e2882116576f2ce1cb91969b15508b98fb952a00b4fcda46a13633c42033172a",
        "book-uc.db": "0ebffab6b0ca1d6448e432710c3c34f780d1d268cad815bbf34348e39550a5cb",
        "book-ucampaign.db": "2a74f5b5566a1c01fda8b4d131c9561cf99ee78a9b1398653a08f3048fe11d81",
        "book-ue.db": "f08936bfede97770cd50fd6d3cf14df7bcd25b910631b298e15991fe32fa9168",
        "book-um.db": "019e2257e6265e568a6103bd9b733615d91d4353c3102cc0664740631fb970d8",
    },
)

FONTI = {f.chiave: f for f in (SRD35, PF1)}


class FontiMancanti(Exception):
    """La cache non ha le fonti e non si possono scaricare."""


class ImprontaSbagliata(Exception):
    """Un file scaricato o copiato non ha lo sha256 fissato."""


class ErroreUso(Exception):
    pass


# ---------------------------------------------------------------- cache

def cartella_cache(argomento: str | None) -> Path:
    if argomento:
        return Path(argomento).expanduser()
    if os.environ.get("RUMBLINGSTONE_SRD_CACHE"):
        return Path(os.environ["RUMBLINGSTONE_SRD_CACHE"]).expanduser()
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "rumblingstone" / "srd"


def sha256(percorso: Path) -> str:
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def scarica_url(url: str, destinazione: Path, timeout: float = 60) -> None:
    """Scarica ``url`` in ``destinazione``. Separata per i test."""
    with urllib.request.urlopen(url, timeout=timeout) as r, open(destinazione, "wb") as f:
        shutil.copyfileobj(r, f)


def _metti(fonte: Fonte, cache: Path, rel: str, sorgente) -> None:
    """Porta un file nella cache passando da un temporaneo e dallo sha256."""
    finale = fonte.cartella(cache) / rel
    finale.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=finale.parent, prefix=".scarico-")
    os.close(fd)
    tmp = Path(tmp)
    try:
        sorgente(tmp)
        trovato = sha256(tmp)
        if trovato != fonte.file[rel]:
            raise ImprontaSbagliata(
                f"{fonte.nome}, {rel}: sha256 {trovato[:16]}…, atteso "
                f"{fonte.file[rel][:16]}… (commit {fonte.commit[:8]})")
        os.replace(tmp, finale)
    finally:
        if tmp.exists():
            tmp.unlink()


def mancanti(fonte: Fonte, cache: Path) -> list[str]:
    base = fonte.cartella(cache)
    return [rel for rel in sorted(fonte.file) if not (base / rel).is_file()]


def assicura(fonte: Fonte, cache: Path, rete: bool = True, avvisa=print) -> Path:
    """Restituisce la cartella della fonte, scaricando i file che mancano."""
    da_fare = mancanti(fonte, cache)
    if not da_fare:
        return fonte.cartella(cache)
    if not rete:
        raise FontiMancanti(
            f"{fonte.nome}: {len(da_fare)} file su {len(fonte.file)} non sono in "
            f"{fonte.cartella(cache)} e --offline vieta di scaricarli")
    avvisa(f"{fonte.nome}: scarico {len(da_fare)} file da {fonte.repo}@{fonte.commit[:8]}",
           file=sys.stderr)
    for rel in da_fare:
        url = URL_RAW.format(repo=fonte.repo, commit=fonte.commit, path=rel)
        try:
            _metti(fonte, cache, rel, lambda tmp, u=url: scarica_url(u, tmp))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            raise FontiMancanti(
                f"{fonte.nome}: la rete non risponde scaricando {url} ({e}). "
                f"Senza rete: `scarica --da-cartella {fonte.chiave}=CLONE` da un "
                f"clone di {fonte.repo} al commit {fonte.commit[:8]}") from e
    return fonte.cartella(cache)


def da_cartella(fonte: Fonte, cache: Path, origine: Path) -> int:
    """Copia nella cache i file fissati da un clone locale, con lo sha256."""
    n = 0
    for rel in mancanti(fonte, cache):
        src = origine / rel
        if not src.is_file():
            raise FontiMancanti(f"{fonte.nome}: {src} non c'è")
        _metti(fonte, cache, rel, lambda tmp, s=src: shutil.copyfile(s, tmp))
        n += 1
    return n


def verifica(fonte: Fonte, cache: Path) -> list[str]:
    base = fonte.cartella(cache)
    return [rel for rel in sorted(fonte.file)
            if (base / rel).is_file() and sha256(base / rel) != fonte.file[rel]]


# ---------------------------------------------------------------- lettura

_TAG = re.compile(r"<[^>]+>")


def pulisci(testo: str) -> str:
    """Toglie i tag HTML delle tabelle e comprime gli spazi, per citare."""
    testo = re.sub(r"</t[dh]>\s*<t[dh][^>]*>", " | ", testo)
    testo = _TAG.sub(" ", testo)
    return re.sub(r"\s+", " ", testo).strip()


def taglia(testo: str, centro: int, larghezza: int = 220) -> str:
    inizio = max(0, centro - larghezza // 3)
    pezzo = testo[inizio:inizio + larghezza]
    return ("…" if inizio else "") + pulisci(pezzo) + ("…" if inizio + larghezza < len(testo) else "")


def riga_di(testo: str, pos: int) -> int:
    return testo.count("\n", 0, pos) + 1


@dataclass
class Passo:
    """Un punto di una fonte o del master, con la citazione."""
    citazione: str
    testo: str
    valore: str | None
    estratto: str


def _valore(m: re.Match) -> str | None:
    return m.group("v") if "v" in m.re.groupindex else None


def _punto(m: re.Match) -> int:
    """Dove citare: il valore, se la regex ne ha uno, altrimenti l'inizio."""
    return m.start("v") if "v" in m.re.groupindex and m.group("v") is not None else m.start()


def cerca_srd35(base: Path, fonte: Fonte, regola: re.Pattern, file: str | None) -> Passo | None:
    candidati = [file] if file else sorted(fonte.file)
    for rel in candidati:
        p = base / rel
        if not p.is_file():
            if file:
                raise ErroreUso(f"{rel}: non è un file dell'SRD 3.5 fissato")
            continue
        testo = p.read_text(encoding="utf-8")
        m = regola.search(testo)
        if m:
            # Il «passo» è il paragrafo (o la riga di tabella) che contiene la regola.
            a = testo.rfind("\n", 0, m.start()) + 1
            b = testo.find("\n", m.end())
            b = len(testo) if b < 0 else b
            return Passo(citazione=f"{fonte.nome}, {rel}:{riga_di(testo, _punto(m))}",
                         testo=testo[a:b], valore=_valore(m),
                         estratto=taglia(testo, _punto(m)))
    return None


def sezioni_pf1(db: Path, nome: str) -> list[tuple[str, str, str]]:
    """(fonte, url, testo) di ogni sezione chiamata ``nome``, col suo sottoalbero."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        uscita = []
        for lft, rgt, source, url in con.execute(
                "select lft, rgt, source, url from sections where name = ? collate nocase "
                "order by lft", (nome,)):
            corpi = [c for (c,) in con.execute(
                "select body from sections where lft between ? and ? and body is not null "
                "order by lft", (lft, rgt))]
            uscita.append((source, url or "", pulisci("\n".join(corpi))))
        return uscita
    finally:
        con.close()


def cerca_pf1(base: Path, fonte: Fonte, regola: re.Pattern, libro: str | None,
              sezione: str) -> Passo | None:
    libri = [libro] if libro else sorted(fonte.file)
    for db in libri:
        if db not in fonte.file:
            raise ErroreUso(f"{db}: non è un libro del PRD fissato")
        for source, url, testo in sezioni_pf1(base / db, sezione):
            m = regola.search(testo)
            if m:
                return Passo(citazione=f"{fonte.nome}, {source} › {sezione} ({db})",
                             testo=testo, valore=_valore(m),
                             estratto=taglia(testo, _punto(m)))
    return None


# ---------------------------------------------------------------- confronto

def numero(testo: str, inglese: bool = False) -> float:
    """Un numero scritto all'italiana (master) o all'inglese (fonte).

    Italiano: «4,5» → 4.5, «2.282» → 2282. Inglese: «2,282» → 2282, «1.5» → 1.5.
    """
    t = testo.strip().replace("\u2009", "").replace(" ", "")
    migliaia, decimali = (",", ".") if inglese else (".", ",")
    if re.fullmatch(rf"\d{{1,3}}(\{migliaia}\d{{3}})+", t):
        t = t.replace(migliaia, "")
    return float(t.replace(decimali, "."))


def normalizza(testo: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", testo)).strip().lower()


def confronta(voce: dict, fonte_v: str | None, master_v: str | None) -> bool:
    modo = voce.get("confronto", "presenza")
    if modo == "presenza":
        return True
    if fonte_v is None or master_v is None:
        raise ErroreUso(f"{voce['id']}: «{modo}» vuole il gruppo (?P<v>…) in regola e affermazione")
    if modo == "numero":
        atteso = numero(fonte_v, inglese=True) * float(voce.get("scala", 1))
        return abs(numero(master_v) - atteso) <= float(voce.get("tolleranza", 1e-6))
    if modo == "termine":
        accettati = {normalizza(fonte_v)}
        for chiave, forme in (voce.get("equivale") or {}).items():
            if normalizza(str(chiave)) == normalizza(fonte_v):
                accettati |= {normalizza(str(f)) for f in forme}
        return normalizza(master_v) in accettati
    raise ErroreUso(f"{voce['id']}: confronto «{modo}» sconosciuto (presenza, numero, termine)")


def compila(voce: dict, chiave: str) -> re.Pattern | None:
    if not voce.get(chiave):
        return None
    try:
        return re.compile(voce[chiave], re.MULTILINE)
    except re.error as e:
        raise ErroreUso(f"{voce.get('id', '?')}: «{chiave}» non è una regex valida: {e}") from e


@dataclass
class Esito:
    id: str
    cosa: str
    esito: str              # concorda | discorda | non trovata
    dove: str               # «» | «nella fonte» | «nel master»
    fonte: str              # citazione
    fonte_dice: str
    master: str
    master_dice: str


def riscontra_voce(voce: dict, basi: dict[str, Path], repo: Path) -> Esito:
    for k in ("id", "fonte", "regola"):
        if not voce.get(k):
            raise ErroreUso(f"riscontro senza «{k}»: {voce}")
    fonte = FONTI.get(voce["fonte"])
    if fonte is None:
        raise ErroreUso(f"{voce['id']}: fonte «{voce['fonte']}» sconosciuta (srd35, pf1)")
    regola = compila(voce, "regola")
    if fonte.chiave == "srd35":
        passo = cerca_srd35(basi["srd35"], fonte, regola, voce.get("file"))
    else:
        if not voce.get("sezione"):
            raise ErroreUso(f"{voce['id']}: una regola del PRD vuole «sezione»")
        passo = cerca_pf1(basi["pf1"], fonte, regola, voce.get("libro"), voce["sezione"])
    cosa = voce.get("cosa", "")
    if passo is None:
        dove = voce.get("file") or voce.get("sezione") or "tutta la fonte"
        return Esito(voce["id"], cosa, "non trovata", "nella fonte",
                     f"{fonte.nome}, {dove}", "", voce.get("master") or "", "")
    fonte_dice = passo.estratto
    non = compila(voce, "regola_non")
    if non is not None and non.search(passo.testo):
        return Esito(voce["id"], cosa, "discorda", "", passo.citazione,
                     fonte_dice, "", f"la fonte contiene «{voce['regola_non']}»")
    if not voce.get("master"):
        return Esito(voce["id"], cosa, "concorda", "", passo.citazione, fonte_dice, "", "")
    percorso = repo / voce["master"]
    if not percorso.is_file():
        raise ErroreUso(f"{voce['id']}: il master {voce['master']} non c'è")
    testo = percorso.read_text(encoding="utf-8")
    affermazione = compila(voce, "affermazione")
    if affermazione is None:
        raise ErroreUso(f"{voce['id']}: c'è «master» senza «affermazione»")
    occorrenze = list(affermazione.finditer(testo))
    if not occorrenze:
        return Esito(voce["id"], cosa, "non trovata", "nel master", passo.citazione,
                     fonte_dice, voce["master"], "")
    for m in occorrenze:
        cit = f"{voce['master']}:{riga_di(testo, _punto(m))}"
        if not confronta(voce, passo.valore, _valore(m)):
            dice = taglia(testo, _punto(m), 160)
            if passo.valore is not None:
                dice += f" (valore «{normalizza(_valore(m) or '')}» contro «{passo.valore}»"
                dice += f" × {voce['scala']})" if voce.get("scala") else ")"
            return Esito(voce["id"], cosa, "discorda", "", passo.citazione, fonte_dice, cit, dice)
    m = occorrenze[0]
    righe = ", ".join(str(riga_di(testo, _punto(o))) for o in occorrenze)
    return Esito(voce["id"], cosa, "concorda", "", passo.citazione, fonte_dice,
                 f"{voce['master']}:{righe}", taglia(testo, _punto(m), 160))


def leggi_riscontri(percorso: Path) -> list[dict]:
    try:
        testo = percorso.read_text(encoding="utf-8")
    except OSError as e:
        raise ErroreUso(f"{percorso}: {e}") from e
    if percorso.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as e:
            raise ErroreUso("pyyaml non c'è: usa un file .json o installa requirements.txt") from e
        try:
            dati = yaml.safe_load(testo)
        except yaml.YAMLError as e:
            raise ErroreUso(f"{percorso}: YAML non valido: {e}") from e
    else:
        try:
            dati = json.loads(testo)
        except json.JSONDecodeError as e:
            raise ErroreUso(f"{percorso}: JSON non valido: {e}") from e
    if isinstance(dati, list):
        return dati
    if not isinstance(dati, dict) or not isinstance(dati.get("riscontri"), list):
        raise ErroreUso(f"{percorso}: manca l'elenco «riscontri»")
    return dati["riscontri"]


def _cella(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ") or "—"


def tabella(esiti: list[Esito], fonti: list[Fonte]) -> str:
    righe = ["| id | che cosa | la fonte dice | il master dice | esito |",
             "|---|---|---|---|---|"]
    for e in esiti:
        fonte = f"{e.fonte_dice} ({e.fonte})" if e.fonte_dice else e.fonte
        master = f"{e.master_dice} ({e.master})" if e.master_dice else e.master
        esito = f"**{e.esito}**" if e.esito != "concorda" else e.esito
        if e.dove:
            esito += f" {e.dove}"
        righe.append(f"| {_cella(e.id)} | {_cella(e.cosa)} | {_cella(fonte)} | "
                     f"{_cella(master)} | {esito} |")
    conta = {k: sum(1 for e in esiti if e.esito == k) for k in ("concorda", "discorda", "non trovata")}
    righe += ["", " · ".join(f"{k}: {v}" for k, v in conta.items()), ""]
    righe += [f"Citazioni da {f.nome} ({f.repo}@{f.commit[:8]}): {f.licenza}" for f in fonti]
    return "\n".join(righe) + "\n"


# ---------------------------------------------------------------- comandi

def cmd_scarica(args, cache: Path) -> int:
    if args.verifica:
        cattivi = {f.nome: verifica(f, cache) for f in FONTI.values()}
        for nome, elenco in cattivi.items():
            for rel in elenco:
                print(f"✗ {nome}, {rel}: sha256 diverso da quello fissato")
        for f in FONTI.values():
            m = mancanti(f, cache)
            print(f"{f.nome}: {len(f.file) - len(m)} file su {len(f.file)} in {f.cartella(cache)}")
        return 1 if any(cattivi.values()) else 0
    origini = {}
    for coppia in args.da_cartella or []:
        chiave, _, cartella = coppia.partition("=")
        if chiave not in FONTI or not cartella:
            raise ErroreUso(f"--da-cartella vuole FONTE=CARTELLA, FONTE fra {', '.join(FONTI)}")
        origini[chiave] = Path(cartella).expanduser()
    for f in FONTI.values():
        if args.fonte and f.chiave != args.fonte:
            continue
        if f.chiave in origini:
            n = da_cartella(f, cache, origini[f.chiave])
            print(f"{f.nome}: {n} file copiati da {origini[f.chiave]}, sha256 controllati")
        else:
            assicura(f, cache, rete=not args.offline)
        print(f"{f.nome}: {len(f.file)} file in {f.cartella(cache)} ({f.repo}@{f.commit[:8]})")
    return 0


def cmd_regola(args, cache: Path) -> int:
    nome = args.nome.strip()
    trovate = 0
    if args.fonte in (None, "srd35"):
        base = assicura(SRD35, cache, rete=not args.offline)
        titolo = re.compile(
            rf"^(?:#{{1,6}}\s*{re.escape(nome)}\s*$|\*\*{re.escape(nome)}:?\*\*:?)",
            re.IGNORECASE | re.MULTILINE)
        for rel in sorted(SRD35.file):
            testo = (base / rel).read_text(encoding="utf-8")
            for m in titolo.finditer(testo):
                trovate += 1
                righe = testo[m.start():].split("\n")[:args.righe]
                print(f"## {SRD35.nome}, {rel}:{riga_di(testo, m.start())}\n")
                print("\n".join(pulisci(r) if "<t" in r else r for r in righe).rstrip(), "\n")
    if args.fonte in (None, "pf1"):
        base = assicura(PF1, cache, rete=not args.offline)
        for db in sorted(PF1.file):
            for source, url, testo in sezioni_pf1(base / db, nome):
                trovate += 1
                print(f"## {PF1.nome}, {source} › {nome} ({db})\n")
                print(testo[:args.righe * 80] + ("…" if len(testo) > args.righe * 80 else ""), "\n")
    if not trovate:
        print(f"«{nome}»: nessun titolo con questo nome. Il nome è quello inglese "
              f"dell'SRD (Slaying Arrow, non freccia assassina).", file=sys.stderr)
        return 1
    usate = [f for f in (SRD35, PF1) if args.fonte in (None, f.chiave)]
    print("\n".join(f"Citazioni da {f.nome} ({f.repo}@{f.commit[:8]}): {f.licenza}" for f in usate))
    return 0


def cmd_riscontra(args, cache: Path) -> int:
    voci = leggi_riscontri(Path(args.file))
    servono = sorted({v.get("fonte") for v in voci if v.get("fonte") in FONTI})
    basi = {k: assicura(FONTI[k], cache, rete=not args.offline) for k in servono}
    repo = Path(args.repo).resolve()
    esiti = [riscontra_voce(v, basi, repo) for v in voci]
    testo = tabella(esiti, [FONTI[k] for k in servono])
    print(testo, end="")
    if args.md:
        Path(args.md).write_text(testo, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"fonti": {k: {"repo": FONTI[k].repo, "commit": FONTI[k].commit,
                           "licenza": FONTI[k].licenza} for k in servono},
             "esiti": [e.__dict__ for e in esiti]},
            ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if args.strict and any(e.esito != "concorda" for e in esiti):
        return 1
    return 0


def cmd_licenza(args, cache: Path) -> int:
    for f in FONTI.values():
        print(f"{f.nome} — {f.repo}@{f.commit[:8]}\n  {f.licenza}\n"
              f"  testo completo: {f.cartella(cache) / f.file_licenza}")
    return 0


def costruisci_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="riscontro_srd.py",
        description="Riscontra le regole dei master sull'SRD 3.5 e sul PRD PF1e "
                    "(OGL 1.0a), scaricati a commit fissato in una cache fuori dal repo.",
        epilog="Exit: 0 ok · 1 discordanze con --strict, sha256 sbagliato, regola "
               "non trovata · 2 uso · 3 fonti non disponibili (rete o --offline).")
    p.add_argument("--cache", default=None,
                   help="cartella della cache (default: $RUMBLINGSTONE_SRD_CACHE o "
                        "~/.cache/rumblingstone/srd)")
    p.add_argument("--offline", action="store_true",
                   help="non scaricare: se la cache è incompleta esce 3")
    sub = p.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("scarica", help="riempie la cache a commit fissato, con lo sha256")
    s.add_argument("--fonte", choices=sorted(FONTI), default=None, help="una sola fonte")
    s.add_argument("--da-cartella", nargs="+", metavar="FONTE=DIR", default=None,
                   help="copia da un clone locale invece di scaricare")
    s.add_argument("--verifica", action="store_true",
                   help="rifà lo sha256 dei file in cache, senza scaricare")

    r = sub.add_parser("regola", help="cerca una regola per nome (inglese) nelle due fonti")
    r.add_argument("nome", help="il nome come nell'SRD, es. «Slaying Arrow», «Scent»")
    r.add_argument("--fonte", choices=sorted(FONTI), default=None, help="una sola fonte")
    r.add_argument("--righe", type=int, default=12, help="quante righe mostrare (default 12)")

    c = sub.add_parser("riscontra", help="esegue un file di riscontri (YAML o JSON)")
    c.add_argument("file", help="il file dei riscontri")
    c.add_argument("--repo", default=str(REPO), help="radice per i percorsi dei master")
    c.add_argument("--md", default=None, help="scrive la tabella Markdown anche qui")
    c.add_argument("--json", default=None, help="scrive gli esiti in JSON")
    c.add_argument("--strict", action="store_true",
                   help="esce 1 se resta una discordanza o una regola non trovata")

    sub.add_parser("licenza", help="licenza delle due fonti e dove sta il testo")
    return p


def main(argv: list[str] | None = None) -> int:
    args = costruisci_parser().parse_args(argv)
    cache = cartella_cache(args.cache)
    comandi = {"scarica": cmd_scarica, "regola": cmd_regola,
               "riscontra": cmd_riscontra, "licenza": cmd_licenza}
    try:
        return comandi[args.comando](args, cache)
    except FontiMancanti as e:
        print(f"✗ fonti non disponibili: {e}", file=sys.stderr)
        return ESITO_RETE
    except ImprontaSbagliata as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    except ErroreUso as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
