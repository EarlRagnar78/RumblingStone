#!/usr/bin/env python3
"""validate_norme_editoriali.py — una norma senza misura deve almeno avere un nome.

🔴 **Il difetto che questo cancello presidia, e che è già successo.**

Il 2026-09-18 si è scoperto che `references/read-aloud-adulti.md` dichiarava da
agosto **box ≤ 12 righe, un solo nome proprio nuovo, niente parentesi**, e che
**nessuno strumento del repo lo guardava**. `ADR-0014` («regia sensoriale
obbligatoria», luglio) era stato applicato a **un documento su cento**: la
chiusura su «Che fate?», prescritta per *ogni* box di combattimento, esisteva
**una volta in tutto il repo**.

Nessuno se n'era accorto perché **una norma non misurata non fa rumore quando
viene ignorata**. E la scopribilità non c'entrava: tutti e 56 i file
`references/` sono citati dal loro `SKILL.md` — un cancello sulla citazione
sarebbe verde e inutile.

## Cosa controlla, quindi

1. **Copertura**: ogni file della superficie normativa sta in
   `skills/REGISTRO-NORME-EDITORIALI.md`. Aggiungerne uno senza registrarlo è
   rosso — è così che una norma torna a nascondersi.
2. **Onestà dei rimandi**: ogni `misura_craft` citato dal registro nomina un
   congegno che **esiste davvero** in `scripts/misura_craft.py`, e ogni script
   citato è un file che esiste. È ADR-0053 applicato al registro stesso: un
   rimando inventato è peggio di un buco dichiarato, perché sembra copertura.
3. **Ragione scritta**: ogni riga 🔴 porta un perché dopo il trattino. Un
   «non misurato» nudo non è una decisione, è una dimenticanza con un'icona.
4. **Severità dichiarata** (lotto F1.1 di `PIANO-MISURA-EDITORIALE-STANDARD`):
   ogni norma dice **quanto costa violarla** — `critico` 25, `maggiore` 5,
   `minore` 1 — oppure porta una ragione scritta per non avere un peso. Senza
   questa colonna il punteggio di ADR-0059 deve indovinare, e una metrica che
   indovina i pesi misura il suo autore.
5. **Accordo con `specifiche-qualita.yaml`**: le norme che hanno un rilevatore
   portano la loro **chiave** accanto alla severità, e la severità nel registro
   deve essere quella nello YAML. È lo stesso disegno di `decisioni_dm --check`
   (ADR-0047): **una casa sola** per il dato, e un cancello che fa rossa la CI
   quando le due copie divergono.
6. **Il conto è derivato, non scritto**: la tabella «il conto onesto» del §4 si
   confronta con le righe vere. 🐛 Scritta a mano, diceva **16+9+12+3 = 40** su
   **39** righe e il testo accanto parlava di *«undici norme su trentaquattro»*
   — tre numeri, tre verità diverse, nessuna esatta. Diciannovesimo caso della
   famiglia «un numero scritto a mano invecchia in silenzio».

7. **La superficie delle norme scoperte** (ex `superficie_norme.py`,
   ADR-0062, fuso qui il 2026-10-22): ogni 🔴 ha una riga che dice se manca il
   codice o il dato, e la rimisura. `--superficie` stampa la tabella.

⚠️ **Cosa NON controlla**: se le norme siano *rispettate*. Quello lo dicono
`misura_craft`, `validate_modules`, `validate_prosa` — e in dieci casi su
trentuno, oggi, **niente**. Il registro serve a rendere quel dieci **visibile**.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
REGISTRO = ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md"

#: La superficie normativa: dove vivono le regole di prosa, stile e linea
#: editoriale. Le altre skill (SRD, lore, mappe) non ci entrano: non dettano
#: norme di scrittura.
SUPERFICIE = (
    "skills/rumblingstone-narrative-style/references",
    "skills/rumblingstone-indagine/references",
)

#: Gli ADR che dettano norme di scrittura e che quindi vanno registrati.
ADR_NORMATIVI = ("ADR-0014",)

_CONGEGNO = re.compile(r"congegno `([^`]+)`")
_SCRIPT = re.compile(r"`(validate_\w+\.py|misura_craft[^`]*)`")
_ROSSO = re.compile(r"^\|.*🔴\s*(?:non misurato)?\s*(.*?)\s*\|\s*$", re.M)

#: Le tre severità di ADR-0059, e i loro pesi. Vivono nello YAML: qui si
#: controlla solo che il registro non ne inventi una quarta.
SEVERITA = ("critico", "maggiore", "minore")
SPECIFICHE = ROOT / "scripts" / "specifiche-qualita.yaml"
#: La riga di una norma: file | norma | severità | stato.
_COLONNE_NORMA = 4


def congegni_veri() -> "set[str]":
    testo = (ROOT / "scripts" / "misura_craft.py").read_text(encoding="utf-8")
    return set(re.findall(r'^\s*\("([^"]+)",\s*$', testo, re.M))


def righe_norma(testo: str) -> "list[list[str]]":
    """Le righe di norma del registro, spezzate in celle.

    Una riga di norma comincia con un file o un ADR fra backtick. Le righe di
    intestazione e i separatori non passano di qui.
    """
    fuori = []
    for riga in testo.splitlines():
        if not riga.startswith("| `"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        fuori.append(celle)
    return fuori


def severita_dello_yaml() -> "dict[str, str]":
    """chiave della norma -> severità, letta da `specifiche-qualita.yaml`.

    Lettura a mano invece che con `yaml`: questo cancello gira in CI, dove
    `pyyaml` non e' garantito (ADR-0037, stdlib-only). Il formato del file e'
    noto e piatto, e un parser di due righe e' onesto quanto una dipendenza in
    piu'. Se il file cambia forma, il test lo dice.
    """
    if not SPECIFICHE.exists():
        return {}
    fuori, chiave, dentro = {}, None, False
    for riga in SPECIFICHE.read_text(encoding="utf-8").splitlines():
        if riga.startswith("norme:"):
            dentro = True
            continue
        if dentro and riga and not riga.startswith((" ", "#")):
            break
        if not dentro or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^  (\w+):\s*$", riga)
        if m:
            chiave = m.group(1)
            continue
        m = re.match(r"^    severita:\s*(\w+)\s*$", riga)
        if m and chiave:
            fuori[chiave] = m.group(1)
    return fuori


def conto_vero(testo: str) -> "dict[str, int]":
    """Quante norme per stato, contate sulle righe e non sulle emoji.

    🐛 Il conto stampato in fondo contava le **occorrenze delle emoji in tutto
    il file**, prosa compresa: dava 47 dove le norme sono 39.
    """
    conto = {"🟢": 0, "🟡": 0, "🔴": 0, "⚪": 0}
    for celle in righe_norma(testo):
        stato = celle[-1]
        for e in conto:
            if stato.startswith(e) or f" {e}" in stato[:4]:
                conto[e] += 1
                break
    return conto


# ─────────────────────────────────────────── la superficie delle norme scoperte
#
# *«Questa norma non e' misurata: manca il codice, o manca il dato?»* Fino al
# 2026-10-22 la risposta stava in `superficie_norme.py` (ADR-0062), un gemello
# che questo cancello gia' richiamava al punto 6 e che la CI rieseguiva in un
# passo suo. Lotto 7e di PIANO-AVVENTURE-COMMUNITY: uno strumento solo.
#
# I quattro stati, e il passo successivo in ognuno:
#
# | stato | cosa manca | il passo successivo |
# |---|---|---|
# | `SUPERFICIE_VUOTA` | la convenzione esiste e ha zero occorrenze | marcare il contenuto |
# | `CONVENZIONE_ASSENTE` | nessuno ha deciso come si marca | una decisione di forma |
# | `OGGETTO_ASSENTE` | non esiste il file di cui la norma parla | produrlo, o ammetterlo |
# | `FUORI_DOMINIO` | il fatto non e' nel testo, o manca lo strumento | si dichiara e si chiude |
#
# Una superficie vuota NON e' un difetto e non boccia: boccia una riga che ha
# smesso di dire il vero (una forma che ora ha occorrenze, un oggetto comparso).
# Le norme che sono letture di un agente, e i fatti del tavolo, stanno nel §5 del
# registro, fuori dal conto: un cancello su un giudizio sarebbe rumore (ADR-0073).
SUPERFICIE_VUOTA = "SUPERFICIE_VUOTA"
CONVENZIONE_ASSENTE = "CONVENZIONE_ASSENTE"
OGGETTO_ASSENTE = "OGGETTO_ASSENTE"
FUORI_DOMINIO = "FUORI_DOMINIO"

def _file_di_gioco() -> "list[Path]":
    """Il contenuto di gioco vivo, **riusando l'insieme che il repo dichiara**.

    🐛 **La prima stesura ne teneva uno suo, e ha sbagliato al primo giro.**
    Escludeva le cartelle con il punto davanti e le sei di lavoro, e si e'
    dimenticata `build/`: la forma `COLORE DOMINANTE` risultava presente **5
    volte**, e la norma sulla tinta d'arco veniva dichiarata «misurabile ora».
    Le cinque occorrenze erano le copie generate della skill che quella forma
    la **prescrive**, non archi che la dichiarano.

    Ventesimo caso della famiglia «un criterio largo si inventa copertura», e
    la cura e' sempre la stessa: `misura_craft.file_di_gioco_p1()` questo
    insieme lo definisce gia', con `ESCLUSI`, `ESCLUSI_NOME` e le cartelle che
    si dichiarano archivio con un `_SNAPSHOT-STORICO.md`. Si riusa.
    """
    import misura_craft as mc  # noqa: PLC0415
    return mc.file_di_gioco_p1()


def _conta(forma: str) -> int:
    """Quante volte la forma dichiarata compare nel contenuto di gioco."""
    rx = re.compile(forma)
    return sum(len(rx.findall(f.read_text(encoding="utf-8", errors="replace")))
               for f in _file_di_gioco())


def _conta_file(modello: str) -> int:
    return len([p for p in ROOT.glob(modello) if p.is_file()])


#: 🔴 **Le norme che nessuno misura, e cosa manca a ciascuna.**
#:
#: Ogni riga dichiara la **forma** che andrebbe cercata. Se la forma e' `None`,
#: nessuno ha ancora deciso come si marca quella cosa — e la decisione viene
#: prima del codice, sempre.
NORME_SCOPERTE = (
    {
        "chiave": "el_oltre_il_tetto",
        "norma": "npc-villain-boosting — EL <= APL+4, e oltre il tetto un `Boost log:`",
        "prerequisito": "gli incontri dichiarano il loro EL nella forma prescritta",
        "forma": r"\*\*EL\*\*:\s*\[?\d",
        "dove": "AGENTS.md riga 352 prescrive `**EL**: [N]`",
        "rilevatore_pronto": "validate_modules.py --tetto-el",
        "sblocca": "PIANO-MARCATURA-DEGLI-INCONTRI M1-M3",
    },
    {
        "chiave": "tinta_arco_ripetuta",
        "norma": "varieta-fra-archi.md — mai due archi di fila con la stessa tinta",
        "prerequisito": "ogni arco dichiara le sue cinque righe d'intestazione",
        "forma": r"COLORE DOMINANTE",
        "dove": "varieta-fra-archi.md prescrive COLORE DOMINANTE / CONTRAPPUNTO / "
                "FAMIGLIA DI CASO / CONGEGNO / IL PICCO",
        "rilevatore_pronto": None,
        "sblocca": "una riga per arco, nove righe in tutto",
    },
    {
        "chiave": "nodi_marcati",
        "norma": "nodi-e-sei-porte.md, congegno-e-enigmi.md, ricomposizione.md — >=3 porte "
                 "per nodo (>=1 fisica), 6-9 nodi per caso, mai piu' di 9 elementi nella "
                 "ricomposizione",
        "prerequisito": "i nodi d'indagine sono marcati",
        "forma": None,
        "dove": "nessuna forma prescritta: `nodi-e-sei-porte.md` descrive il nodo "
                "a tre strati ma non dice come si marca sulla pagina",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-INDAGINE-E-DEDUZIONE I6, gated su I5",
    },
    {
        "chiave": "box_di_luogo_senza_creature",
        "norma": "read-aloud-adulti.md §2-bis — il box di luogo non descrive le creature (Dungeon)",
        "prerequisito": "ogni box dichiara il suo tipo: di luogo, d'ingresso, di round",
        "forma": None,
        "dove": "nessuna forma prescritta: l'etichetta `**Read-aloud (pilastro).**` "
                "dice la voce, non il tipo del box; senza il tipo, i 322 nomi del "
                "registro pescano 315 box su 501 (dei, PG, artefatti)",
        "rilevatore_pronto": None,
        "sblocca": "PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE B2, D3",
    },
    {
        "chiave": "fatto_da_due_nodi",
        "norma": "nodi-e-sei-porte.md — ogni fatto raggiungibile da >=2 nodi",
        "prerequisito": "le conclusioni e gli indizi sono marcati",
        "forma": r"<!--\s*indizio\s+C\d+",
        "dove": "la marcatura `<!-- conclusione C1: … -->` e `<!-- indizio C1 -->` di "
                "`sviluppo-degli-incontri.md` §21 (2026-10-22): nessun master la usa ancora",
        "rilevatore_pronto": "domande_developer.py (D21)",
        "sblocca": "il primo master con un'indagine che la marca",
    },
    {
        "chiave": "gradi_dei_pg",
        "norma": "registro-e-ricompense.md — tetto livello+3, max +6, 1 grado/PG/livello",
        "prerequisito": "esiste una scheda personaggio leggibile per i quattro PG",
        "forma": None,
        "oggetto": "PG/*Scheda*.md",
        "dove": "in `PG/` ci sono gli artefatti e le immagini, **nessun master di "
                "scheda personaggio**: lo dice anche INDEX, «il layout schede e' "
                "pronto e aspetta i numeri veri»",
        "rilevatore_pronto": None,
        "sblocca": "le schede A4 dei quattro PG — gated sul DM",
    },
    {
        "chiave": "eco_che_anticipa",
        "norma": "consequence-echoes.md §3-ter regola 3 — un eco per un PG non anticipa",
        "prerequisito": "ogni eco per un PG dichiara quale scena del master prepara",
        "forma": None,
        "dove": "nessuna forma prescritta: i fogli-eco non dicono a quale scena "
                "portano, e senza quel legame nessuno sa cosa sarebbe un'anticipazione",
        "rilevatore_pronto": None,
        "sblocca": "una convenzione di marcatura eco → scena, poi il confronto col master",
    },
    {
        "chiave": "statistiche_base",
        "norma": "ADR-0092 — lo statblocco di un PNG che si prepara porta la riga "
                 "«Statistiche base», e Prima del combattimento dice avvisato e sorpreso",
        "prerequisito": "un lotto che porta la riga sugli statblocchi che la vogliono",
        "forma": None,
        "dove": "11 statblocchi su 37 la vogliono e non ce l'hanno (PIANO-AVVENTURE-COMMUNITY "
                "§3): un controllo oggi fallirebbe su schede che nessuno sta toccando",
        "rilevatore_pronto": None,
        "sblocca": "il primo lotto che porta la riga: allora un conto in validate_bestiario --forma",
    },
    {
        "chiave": "appunti_quattrocento_parole",
        "norma": "quiz-a-due-agenti.md — gli appunti del lettore stanno in 400 parole",
        "prerequisito": "gli appunti di ogni esecuzione del quiz stanno in un posto fisso del repo",
        "forma": None,
        "dove": "oggi gli appunti vivono nello scratchpad di chi orchestra; i due del "
                "2026-09-26 sono stati copiati a mano in plans/esperimenti/quiz-def4/",
        "rilevatore_pronto": None,
        "sblocca": "una cartella per esecuzione, poi quiz_lettura.py --check conta le parole",
    },
    {
        "chiave": "pronome_soggetto_pro_drop",
        "norma": "italiano-nativo.md §1 — l'italiano è pro-drop: niente pronome soggetto "
                 "esplicito, se non per enfasi",
        "prerequisito": None,
        "forma": None,
        "dove": "manca lo **strumento**: provato il 2026-10-18 (ADR-0093), il pronome "
                "tonico in posizione di soggetto dà 3 colpi in tutti i box, tutti cambi "
                "di soggetto legittimi. Serve sapere chi era il soggetto prima",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
    {
        "chiave": "due_livelli_di_subordinate",
        "norma": "read-aloud-adulti.md — max due livelli di subordinate",
        "prerequisito": None,
        "forma": None,
        "dove": "qui non manca il **dato**, manca lo **strumento**: serve un parser "
                "sintattico dell'italiano. Il segnale povero — contare le virgole — "
                "darebbe i falsi positivi 64/64 gia' visti in PROSA-CHE-NON-SEMBRI-GENERATA",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
    {
        "chiave": "adr_nuovo_con_alternative",
        "norma": "ADR-0000-template.md (D7 di PIANO-RECUPERO) — un ADR nuovo ha le "
                 "alternative considerate e la condizione «Da rivedere se»",
        "prerequisito": "esiste un ADR scritto dopo il modello del 2026-10-10",
        "forma": None,
        "oggetto": "plans/adr/ADR-0089-*.md",
        "dove": "gli 87 ADR accettati non si riscrivono; il primo scritto col modello "
                "nuovo e' il 0089, perche' il 0088 e' prenotato da una proposta gia' scritta",
        "rilevatore_pronto": None,
        "sblocca": "il primo ADR nuovo: allora un controllo in validate_docs dal 0089 in poi",
    },
    {
        "chiave": "corpo_pr_onesto",
        "norma": ".github/pull_request_template.md (D7 di PIANO-RECUPERO) — un controllo "
                 "non girato si scrive «non eseguito», e si dice come si torna indietro",
        "prerequisito": None,
        "forma": None,
        "dove": "il corpo di una PR sta su GitHub, non in un file del repo: nessuno "
                "script lo legge, e il modello resta il promemoria",
        "rilevatore_pronto": None,
        "sblocca": None,
    },
)


def misura() -> "list[dict]":
    """Lo stato di ogni norma scoperta. Deterministico: solo conteggi su file."""
    fuori = []
    for n in NORME_SCOPERTE:
        riga = dict(n)
        if n["prerequisito"] is None:
            riga["stato"], riga["occorrenze"] = FUORI_DOMINIO, None
        elif n.get("oggetto"):
            riga["occorrenze"] = _conta_file(n["oggetto"])
            riga["stato"] = OGGETTO_ASSENTE if not riga["occorrenze"] else SUPERFICIE_VUOTA
        elif n["forma"] is None:
            riga["stato"], riga["occorrenze"] = CONVENZIONE_ASSENTE, None
        else:
            riga["occorrenze"] = _conta(n["forma"])
            riga["stato"] = SUPERFICIE_VUOTA if not riga["occorrenze"] else "MISURABILE"
        fuori.append(riga)
    return fuori


def problemi() -> "list[str]":
    """Le righe che hanno smesso di dire il vero. Una superficie vuota NON lo e'."""
    errori = []
    for r in misura():
        if r["stato"] == "MISURABILE":
            errori.append(
                f"«{r['chiave']}»: la forma «{r['forma']}» ha ora {r['occorrenze']} "
                "occorrenze — la norma e' diventata misurabile e la riga del "
                "registro va aggiornata da 🔴 a 🟢")
        if r["stato"] == OGGETTO_ASSENTE and _conta_file(r["oggetto"]):
            errori.append(f"«{r['chiave']}»: l'oggetto e' comparso")
    return errori


ETICHETTA = {
    SUPERFICIE_VUOTA: "🟡 superficie vuota",
    CONVENZIONE_ASSENTE: "🔴 convenzione assente",
    OGGETTO_ASSENTE: "🔴 oggetto assente",
    FUORI_DOMINIO: "⚪ fuori dominio",
    "MISURABILE": "🟢 misurabile ORA",
}


def stampa_superficie(righe: "list[dict]") -> None:
    print("\nSUPERFICIE DELLE NORME NON MISURATE\n" + "=" * 70)
    print("Per ognuna: manca il codice, o manca il dato? La risposta cambia il")
    print("passo successivo, e quasi mai il problema e' il codice.\n")
    conta = {}
    for r in righe:
        conta[r["stato"]] = conta.get(r["stato"], 0) + 1
        occ = "—" if r["occorrenze"] is None else str(r["occorrenze"])
        print(f"  {ETICHETTA[r['stato']]:26} occorrenze: {occ:>4}   {r['chiave']}")
        print(f"      {r['norma']}")
        if r["prerequisito"]:
            print(f"      serve: {r['prerequisito']}")
        if r.get("rilevatore_pronto"):
            print(f"      🟢 il rilevatore ESISTE GIA': {r['rilevatore_pronto']}")
        if r.get("sblocca"):
            print(f"      lo sblocca: {r['sblocca']}")
        print()
    print("  " + " · ".join(f"{ETICHETTA[s]} {n}" for s, n in sorted(conta.items())))
    print("\n  ⚠️  «superficie vuota» vuol dire che il rilevatore e' pronto e il")
    print("      contenuto non e' marcato: il giorno che lo e', la norma si accende")
    print("      da sola. «convenzione assente» vuol dire che prima di scrivere")
    print("      codice qualcuno deve DECIDERE una forma — e quella decisione non")
    print("      e' di uno script.\n")



def controlla() -> "list[str]":
    errori: "list[str]" = []
    if not REGISTRO.exists():
        return [f"manca {REGISTRO.relative_to(ROOT)}"]
    testo = REGISTRO.read_text(encoding="utf-8")

    # 1 · copertura: ogni file normativo è nominato
    for cartella in SUPERFICIE:
        d = ROOT / cartella
        if not d.is_dir():
            errori.append(f"superficie dichiarata inesistente: {cartella}")
            continue
        for f in sorted(d.glob("*.md")):
            if f.name not in testo:
                errori.append(
                    f"norma non registrata: {cartella}/{f.name} — aggiungila a "
                    "REGISTRO-NORME-EDITORIALI.md con la sua norma e chi la misura")
    for adr in ADR_NORMATIVI:
        if adr not in testo:
            errori.append(f"ADR normativo non registrato: {adr}")

    # 2 · onestà: i rimandi nominano cose che esistono
    #
    # ⚠️ Solo sulle righe che AFFERMANO una misura. Una riga 🔴 può nominare
    # uno script inesistente **apposta**: è successo alla prima stesura, dove
    # la riga di ADR-0022 cita `validate_pg.py` per dire che non esiste. Un
    # cancello che bocciasse anche quello impedirebbe di scrivere il vero.
    veri = congegni_veri()
    for riga in testo.splitlines():
        if not riga.startswith("|") or "🔴" in riga:
            continue
        for nome in set(_CONGEGNO.findall(riga)):
            if nome not in veri:
                errori.append(
                    f"il registro cita il congegno «{nome}», che non esiste in "
                    "misura_craft.py — un rimando inventato sembra copertura (ADR-0053)")
        for s in set(_SCRIPT.findall(riga)):
            base = s.split()[0].split("--")[0].strip()
            if base and not base.endswith(".py"):
                base += ".py"          # il registro cita «misura_craft --box»
            if base and not (ROOT / "scripts" / base).exists():
                errori.append(f"il registro cita lo script «{base}», che non esiste")

    # 3 · ogni 🔴 porta il suo perché
    for i, riga in enumerate(testo.splitlines(), 1):
        if "🔴" not in riga or not riga.startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        stato = celle[-1]
        if "🔴" in stato and "—" not in stato:
            errori.append(
                f"r.{i}: «non misurato» senza una ragione dopo il trattino — "
                "una riga nuda non è una decisione")

    # 4 · ogni norma dichiara quanto costa violarla (F1.1)
    righe = righe_norma(testo)
    for celle in righe:
        if len(celle) != _COLONNE_NORMA:
            errori.append(
                f"«{celle[1][:50]}»: la riga ha {len(celle)} colonne invece di "
                f"{_COLONNE_NORMA} — manca la severità (F1.1)")
            continue
        sev = celle[2]
        if not any(s in sev for s in SEVERITA):
            if not sev.startswith("—") or len(sev) < 4:
                errori.append(
                    f"«{celle[1][:50]}»: severità assente o inventata — "
                    "dev'essere critico / maggiore / minore, oppure «— » con la "
                    "ragione per cui la norma non si pesa")

    # 5 · registro e specifiche non divergono (lo stesso disegno di ADR-0047)
    yaml_sev = severita_dello_yaml()
    viste = set()
    for celle in righe:
        if len(celle) != _COLONNE_NORMA:
            continue
        m = re.search(r"`(\w+)`", celle[2])
        if not m:
            continue
        chiave = m.group(1)
        viste.add(chiave)
        if chiave not in yaml_sev:
            errori.append(
                f"il registro dichiara la chiave «{chiave}», che "
                "specifiche-qualita.yaml non conosce — un rimando inventato "
                "sembra copertura (ADR-0053)")
        elif yaml_sev[chiave] not in celle[2]:
            errori.append(
                f"«{chiave}»: il registro dice «{celle[2]}», lo YAML dice "
                f"«{yaml_sev[chiave]}» — il dato ha una casa sola (ADR-0047)")
    for chiave in sorted(set(yaml_sev) - viste):
        errori.append(
            f"«{chiave}» pesa nel punteggio ma nessuna riga del registro la "
            "rivendica: una norma che conta senza essere registrata e' il "
            "difetto che ADR-0056 presidia, al contrario")

    # 6 · ogni 🔴 ha la sua riga nella superficie, e la riga non mente
    #
    # ⚠️ ADR-0056 pretende che un «non misurato» porti una **ragione scritta**.
    # Dal 2026-09-21 pretende una cosa in piu': che la ragione sia **rimisurata
    # da un comando**. Una ragione in prosa invecchia come qualunque altra cosa
    # scritta a mano: e' successo ai «27 ADR mancanti», che erano zero.
    errori.extend(problemi())
    # 🐛 Il criterio e' il **prefisso** della cella di stato (`conto_vero`): due
    # righe 🟢 citano un 🔴 dentro la loro spiegazione.
    rosse = conto_vero(testo)["🔴"]
    if rosse != len(NORME_SCOPERTE):
        errori.append(
            f"il registro ha {rosse} norme 🔴 e la superficie ne descrive "
            f"{len(NORME_SCOPERTE)}: ogni «non misurato» deve avere la sua riga in "
            "NORME_SCOPERTE, altrimenti la ragione torna a essere prosa che "
            "nessuno rimisura")

    # 7 · il conto del §4 e' quello vero
    conto = conto_vero(testo)
    for emoji, atteso in re.findall(r"^\|\s*(🟢|🟡|🔴|⚪)[^|]*\|\s*(\d+)\s*\|$",
                                    testo, re.M):
        if conto[emoji] != int(atteso):
            errori.append(
                f"«il conto onesto» dice {atteso} righe {emoji}, e sono "
                f"{conto[emoji]} — il conto si deriva, non si ricorda")
    return errori


def main(argv=None) -> int:
    import argparse  # noqa: PLC0415
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--superficie", action="store_true",
                    help="la tabella delle norme scoperte: manca il codice o manca il dato? "
                         "(era superficie_norme.py, ADR-0062)")
    ap.add_argument("--json", action="store_true",
                    help="con --superficie: il rapporto in JSON, per la catena")
    args = ap.parse_args(argv)
    if args.superficie:
        righe = misura()
        if args.json:
            print(json.dumps({"tool": "validate_norme_editoriali", "norme_scoperte": righe},
                             ensure_ascii=False, indent=2))
        else:
            stampa_superficie(righe)
        return 0
    errori = controlla()
    for e in errori:
        print(f"  ✗ {e}")
    if errori:
        print(f"✗ validate_norme_editoriali: {len(errori)} problema/i")
        return 1
    testo = REGISTRO.read_text(encoding="utf-8")
    conto = conto_vero(testo)
    n = sum(conto.values())
    pesate = len(severita_dello_yaml())
    print(f"✓ validate_norme_editoriali: {n} norme registrate "
          f"({conto['🟢']} 🟢 · {conto['🟡']} 🟡 · {conto['🔴']} 🔴 · "
          f"{conto['⚪']} ⚪), ogni rimando esiste, ogni buco ha una ragione, "
          f"ogni norma una severità — {pesate} entrano nel punteggio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
