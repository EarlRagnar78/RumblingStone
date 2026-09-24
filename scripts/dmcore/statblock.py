"""statblock.py — il blocco statistiche come DATO, non come prosa (ADR-0021).

Il problema che risolve. Nel `Bestiario/` i numeri di 158 schede vivono dentro
frasi italiane: «**hp 34**; **AC 15** (+1 taglia), touch 11 … TS Temp +6». Una
prosa così si legge benissimo al tavolo e non si può usare per niente altro:
il catalogo tiene solo l'indice (id, nome, GS), la stampa non può fare un
riquadro perché non sa quale numero è quale, `suggest_encounter` bilancia sul
GS dichiarato senza poterlo verificare, e un +7 diventato +1 in trascrizione
non lo trova nessuno.

La soluzione, dentro i vincoli del repo (ADR-0003: il markdown è il master):
**un blocco recintato in testa alla scheda**, con i soli campi meccanici. La
prosa resta dov'era, sotto, e resta la cosa che si legge. Nessuna seconda copia
in un file parallelo: il blocco sta nella scheda, e chi corregge il numero lo
corregge una volta sola.

    ```statblocco
    gs: 2
    tipo: Small plant, 4d8+16
    ca: 15
    ca-dettaglio: contatto 11, colto alla sprovvista 15 (+1 taglia, +4 naturale)
    pf: 34
    velocita: 6 m
    ts: Temp +6, Rifl +1, Vol +2
    attacchi:
      - Mischia schianto +5 (1d4+1)
    voci:
      - Talenti: Allerta, Resistenza Fisica
    ```

Il formato è un sottoinsieme di YAML deliberatamente minuscolo — `chiave:
valore` e liste con `- ` — perché il repo è stdlib-only e perché un formato che
sta in venti righe di parser è un formato che si legge a occhio.

Questo modulo fa tre cose e nient'altro:
  * `leggi(testo)` — trova e legge il blocco di una scheda;
  * `estrai(testo)` — **prova** a ricavarlo dalla prosa, dicendo cosa non ha
    trovato: è il ponte per migrare le schede che esistono già;
  * `rendi(sb)` — lo riscrive in forma canonica, per poterlo inserire.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

APERTURA = "```statblocco"
CHIUSURA = "```"

# I campi obbligatori perché una scheda sia utilizzabile al tavolo: senza uno
# di questi il riquadro sarebbe una cornice con dentro dei buchi.
OBBLIGATORI = ("gs", "ca", "pf", "ts")
AMMESSI = (
    "nome", "gs", "tipo", "ca", "ca-dettaglio", "pf", "pf-dado", "ts", "velocita",
    "iniziativa", "sensi", "attributi", "attacchi", "voci", "tattica", "fonte",
)
LISTE = ("attacchi", "voci")


class StatblockError(ValueError):
    """Il blocco c'è ma non si può usare: campo ignoto, obbligatorio mancante."""


@dataclass
class Statblocco:
    nome: str = ""
    gs: str = ""
    tipo: str = ""
    ca: str = ""
    ca_dettaglio: str = ""
    pf: str = ""
    pf_dado: str = ""
    ts: str = ""
    velocita: str = ""
    iniziativa: str = ""
    sensi: str = ""
    attributi: str = ""
    attacchi: list[str] = field(default_factory=list)
    voci: list[str] = field(default_factory=list)
    tattica: str = ""
    fonte: str = ""

    @property
    def completo(self) -> bool:
        return all(getattr(self, c.replace("-", "_")) for c in OBBLIGATORI)

    def mancanti(self) -> list[str]:
        return [c for c in OBBLIGATORI if not getattr(self, c.replace("-", "_"))]


def _campo(chiave: str) -> str:
    return chiave.replace("-", "_")


def leggi(testo: str) -> Statblocco | None:
    """Il blocco della scheda, o `None` se non ce n'è uno.

    Un blocco malformato **non** è come un blocco assente: solleva. Una scheda
    che dichiara i suoi numeri e li dichiara male è peggio di una che non li
    dichiara, perché ci si fida.
    """
    righe = testo.split("\n")
    try:
        inizio = next(i for i, r in enumerate(righe) if r.strip() == APERTURA)
    except StopIteration:
        return None
    try:
        fine = next(i for i in range(inizio + 1, len(righe)) if righe[i].strip() == CHIUSURA)
    except StopIteration:
        raise StatblockError("blocco «statblocco» aperto e mai chiuso")

    sb = Statblocco()
    chiave_lista = None
    for r in righe[inizio + 1:fine]:
        if not r.strip():
            continue
        if r.lstrip().startswith("- "):
            if chiave_lista is None:
                raise StatblockError(f"voce di elenco fuori da un campo: {r.strip()!r}")
            getattr(sb, chiave_lista).append(r.lstrip()[2:].strip())
            continue
        if ":" not in r:
            raise StatblockError(f"riga senza «chiave: valore»: {r.strip()!r}")
        chiave, _, valore = r.partition(":")
        chiave = chiave.strip()
        if chiave not in AMMESSI:
            raise StatblockError(f"campo sconosciuto «{chiave}» "
                                 f"(ammessi: {', '.join(AMMESSI)})")
        if chiave in LISTE:
            chiave_lista = _campo(chiave)
            if valore.strip():
                getattr(sb, chiave_lista).append(valore.strip())
        else:
            chiave_lista = None
            setattr(sb, _campo(chiave), valore.strip())
    if sb.mancanti():
        raise StatblockError("campi obbligatori mancanti: " + ", ".join(sb.mancanti()))
    return sb


def rendi(sb: Statblocco) -> str:
    """Il blocco in forma canonica: stesso ordine, sempre, così i diff si leggono."""
    fuori = [APERTURA]
    for chiave in AMMESSI:
        valore = getattr(sb, _campo(chiave))
        if not valore:
            continue
        if chiave in LISTE:
            fuori.append(f"{chiave}:")
            fuori += [f"  - {v}" for v in valore]
        else:
            fuori.append(f"{chiave}: {valore}")
    fuori.append(CHIUSURA)
    return "\n".join(fuori)


# ── il ponte: dalla prosa al blocco ──────────────────────────────────────────
# Queste espressioni descrivono come sono scritte le schede che ESISTONO, non
# come dovrebbero essere scritte. Ogni volta che una scheda non si lascia
# leggere, la scelta è due: allargare qui, o correggere la scheda. Allargare
# qui è quasi sempre la risposta sbagliata — una libreria con quindici dialetti
# è una libreria che nessuno script potrà mai usare davvero.

_RE = {
    # Quattro dialetti, tutti presenti nella libreria: «**hp 34**», «(5 HP)»,
    # «**HP**: 84» e — il quarto, trovato chiudendo il lotto H — «hp ~30».
    #
    # La tilde e' il motivo per cui venti schede risultavano «senza numeri»
    # mentre i numeri ce li avevano: il DM li aveva scritti approssimati, e il
    # lettore non riconosceva la forma. Sono numeri SUOI, e derivarli da capo
    # avrebbe voluto dire sostituirli con numeri inventati.
    # Settimo dialetto (lotto I): l'etichetta porta la sigla fra parentesi —
    # «**Punti Ferita (PF):** **44**», «**Classe Armatura (CA):** **20**». Senza
    # tollerarla, due schede coi numeri del DM scritti nero su bianco
    # risultavano vuote, e il derivatore proponeva di rimpiazzarli: 9 punti
    # ferita al posto di 44, 285 al posto di 405. Cioe' il difetto peggiore che
    # questa catena possa avere — sostituire un numero del DM con uno inventato.
    "pf": re.compile(r"(?i:\*{0,2}Punti Ferita(?:\s*\([^)]{0,6}\))?\*{0,2})\s*:?\*{0,2}\s*\*{0,2}[~≈]?\s*(\d{1,4})"
                     r"|\*{0,2}(?:hp|pf|PF|HP)\*{0,2}[:\s]\s*[~≈]?\s*\*{0,2}(\d{1,4})\*{0,2}"
                     # «(104 HP with skeleton template)»: dopo «HP» puo' seguire
                     # del testo dentro la stessa parentesi.
                     r"|\(\*{0,2}[~≈]?\s*(\d{1,4})\s*(?:HP|hp|PF|pf)\b"),
    # I dadi vita, non i dadi di danno: si cercano nella frase di apertura
    # («Small plant, 4d8+16.») o accanto ai pf, mai in fondo a un attacco.
    "pf_dado": re.compile(r"(?:^|\n)[^\n]{0,80}?\b(\d{1,3}d\d{1,2}(?:\s*[+-]\s*\d+)?)\b"
                          r"(?=[^\n]{0,40}(?:\.|\bhp\b|\bpf\b))", re.I),
    "ca": re.compile(r"(?i:\*{0,2}Classe Armatura(?:\s*\([^)]{0,6}\))?\*{0,2})\s*:?\*{0,2}\s*\*{0,2}[~≈]?\s*(\d{1,2})"
                     r"|\*{0,2}\b(?:AC|CA)\b\*{0,2}[:\s]\s*[~≈]?\s*\*{0,2}(\d{1,2})\*{0,2}"),
    # Il dettaglio della CA e' la parentesi che la segue, e **finisce li'**.
    # Correndo fino a fine riga si portava dietro velocita' e attacchi, che
    # nella forma italiana stanno sulla stessa riga: usciva
    # «ca-dettaglio: Volo 24m, attacchi: artigli +8/+8 …».
    # ⚠️ Le SIGLE si cercano come sigle: `re.I` su «CA» faceva combaciare il
    # «ca» minuscolo dentro un'altra parola, e il dettaglio finiva per essere
    # velocita' e attacchi presi da tutt'altro punto del file.
    "ca_dettaglio": re.compile(
        r"(?:\*{0,2}\b(?:AC|CA)\b\*{0,2}|(?i:\*{0,2}Classe Armatura\*{0,2}))"
        r"[:\s]\s*[~≈]?\s*\*{0,2}\d{1,2}\*{0,2}\s*(\([^)\n]*\))"),
    # Il segnale che il numero e' una STIMA e non una lettura. Si conserva:
    # trascrivere «hp ~30» come «pf: 30» promuove un'approssimazione a fatto, e
    # al tavolo non si distinguerebbe piu' da un numero preso da un manuale.
    # Due forme: la tilde PRIMA del numero («hp ~30») e la tilde dentro la
    # parentesi che segue («(**~405 HP**)»). La seconda mancava, e un drago con
    # 405 punti ferita dichiaratamente stimati risultava un dato esatto.
    "approssimato": re.compile(r"(?:hp|pf|PF|HP|AC|CA)\*{0,2}[:\s]\s*[~≈]"
                               r"|\(\*{0,2}[~≈]\s*\d{1,4}\s*(?:HP|hp|PF|pf)\b"),
    # Il divario fra un tiro e l'altro va tenuto largo: la forma italiana estesa
    # «Tempra +7, Riflessi +10, Volontà +6 (+2 vs incantamento)» ci sta appena.
    # ⚠️ Il gap ammette un a capo (`[^.]` invece di `[^.\n]`): una scheda del
    # lotto I mandava a capo fra «Temp +6,» e «Rifl +7», e i tre tiri salvezza
    # sparivano tutti e tre. Il punto resta il confine, e ventiquattro caratteri
    # non bastano a scavalcare una frase — ma bastano a scavalcare una riga.
    # Sesto dialetto, trovato nel lotto I: i tre tiri salvezza su tre righe
    # d'elenco separate, ognuna col proprio conto fra parentesi —
    #
    #     - **Tempra:** +10 (+8 Base, +2 Cos)
    #     - **Riflessi:** +8 (+4 Base, +4 Des)
    #     - **Volontà:** +14 (+9 Base, +5 Sag)
    #
    # È la forma dei dossier dei villain, e sono nove schede. La riga unica non
    # li vede perché fra un tiro e l'altro ci sono trenta caratteri e un a capo.
    # Qui si leggono uno per uno, e si accettano solo se ci sono tutti e tre:
    # due su tre sarebbe un blocco che sembra completo e non lo è.
    # Le forbici: «58–90», con il trattino lungo o corto.
    # ⚠️ Fra l'etichetta e il numero le schede mettono asterischi e due punti in
    # ordine libero — «**Punti Ferita:** 58–90» ha i due punti PRIMA degli
    # asterischi. Un separatore permissivo invece di una sequenza fissa.
    "forbice_pf": re.compile(r"(?:Punti Ferita|\bhp\b|\bPF\b)[:*\s]+"
                             r"(\d{1,3})\s*[–—-]\s*(\d{1,3})\b", re.I),
    "forbice_ca": re.compile(r"(?:Classe Armatura|\bCA\b|\bAC\b)[:*\s]+"
                             r"(\d{1,2})\s*[–—-]\s*(\d{1,2})\b", re.I),
    "ts_temp": re.compile(r"^\s*[-*]?\s*\**Tempra\**\s*:?\**\s*([+-]\d+)", re.M | re.I),
    "ts_rifl": re.compile(r"^\s*[-*]?\s*\**Riflessi\**\s*:?\**\s*([+-]\d+)", re.M | re.I),
    "ts_vol": re.compile(r"^\s*[-*]?\s*\**Volont[àa]\**\s*:?\**\s*([+-]\d+)", re.M | re.I),
    "ts": re.compile(r"Temp[a-zà]*\**\s*\**([+-]\d+)[^.]{0,24}?Rifl[a-zei]*\**\s*\**([+-]\d+)"
                     r"[^.]{0,24}?Vol[a-zontà]*\**\s*\**([+-]\d+)", re.I),
    # Forma compatta: «TS +2/+9/+1», nell'ordine Tempra/Riflessi/Volonta'.
    # Una scheda sola la usa, ma e' inequivocabile e costa due righe.
    "ts_barre": re.compile(r"\bTS\s*\**\s*([+-]\d+)\s*/\s*([+-]\d+)\s*/\s*([+-]\d+)"),
    # Le schede trascritte dai manuali sono in inglese: stessa cosa, altro nome.
    "ts_en": re.compile(r"Fort[a-z]*\**\s*\**([+-]?\d+)[^.\n]{0,14}?Ref[a-z]*\**\s*\**([+-]?\d+)"
                        r"[^.\n]{0,14}?Will\**\s*\**([+-]?\d+)"),
    # ⚠️ L'alternativa piu' LUNGA per prima, o «Vel» mangia meta' di «Velocità»
    # e il resto finisce nel valore: usciva «velocita: ocità: 9 m a piedi».
    "velocita": re.compile(r"\b(?:Velocità|Velocita|Speed|Vel)\b\.?\**\s*:?\s*([^.;|\n]+)"),
    "iniziativa": re.compile(r"\bInit(?:iativa|\.)?\**\s*:?\s*\**([+-]\d+)"),
    # «CR 1/2» è mezzo grado, non uno: catturare solo la prima cifra farebbe
    # sembrare un goblin il doppio di quello che è.
    # «**Grado di Sfida (GS):** 9» — fra la sigla e i due punti c'e' una
    # parentesi, ed e' bastata a rendere invisibili nove schede.
    "gs": re.compile(r"Grado di Sfida[^:\n]{0,12}:\**\s*(\d{1,2}\s*/\s*\d|\d+\.\d+|\d{1,2})"
                     r"|\*{0,2}(?:CR|GS)\*{0,2}[:\s]\s*\*{0,2}(\d{1,2}\s*/\s*\d|\d+\.\d+|\d{1,2})"),
    "tipo": re.compile(r"^\s*((?:Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal)\s+[^.]{2,80})\.",
                       re.M | re.I),
    "attacco": re.compile(r"^\*{0,2}(Mischia|Distanza|Melee|Ranged)\*{0,2}\s+([^\n]+)", re.M),
    "voce": re.compile(r"\*{0,2}\b(Talenti|Abilità|Speciali|Capacità|Incantesimi)\*{0,2}\s*:\s*"
                       r"([^.\n]+)"),
}


def _fino_al_punto(s: str) -> str:
    """La prima frase, tenendo insieme le parentesi: «+5 (1d4+1). Altro» → «+5 (1d4+1)»."""
    fuori = []
    livello = 0
    for i, c in enumerate(s):
        if c == "(":
            livello += 1
        elif c == ")":
            livello = max(0, livello - 1)
        elif c == "." and livello == 0 and (i + 1 >= len(s) or s[i + 1] in " \n"):
            break
        fuori.append(c)
    return "".join(fuori).strip()


def estrai(testo: str) -> tuple[Statblocco, list[str]]:
    """Prova a ricavare il blocco dalla prosa. Ritorna (blocco, campi non trovati).

    Non indovina: se un numero non c'è nel testo, resta vuoto e finisce
    nell'elenco dei mancanti. Una scheda inventata a metà sarebbe peggio di una
    scheda non migrata.
    """
    sb = Statblocco()
    # Il GS e il tipo possono stare in testa al documento, fuori dalla sezione
    # delle statistiche; i numeri della creatura, no. Vedi finestra_statistiche().
    intero, testo = testo, finestra_statistiche(testo)
    for chiave in ("pf", "ca", "velocita", "iniziativa", "gs", "tipo", "pf_dado"):
        m = _RE[chiave].search(testo)
        if m:
            # `pf` ha due rami alternativi: vale il gruppo che ha catturato.
            valore = next((g for g in m.groups() if g), "")
            setattr(sb, chiave, valore.strip().rstrip(",;"))
    for chiave in ("gs", "tipo"):
        if not getattr(sb, chiave):
            m = _RE[chiave].search(intero)
            if m:
                # 🐛 come sopra: `gs` ha due rami, e `group(1)` e' None quando
                # scatta il secondo («→ CR 12» di Sethrax). Il lettore crollava.
                valore = next((g for g in m.groups() if g), "")
                setattr(sb, chiave, valore.strip())
    m = _RE["ca_dettaglio"].search(testo)
    if m:
        # La barra verticale separa i CAMPI nelle schede a coppie chiave/valore:
        # oltre quella non c'è più il dettaglio della CA, c'è un altro campo.
        sb.ca_dettaglio = m.group(1).split("|")[0].strip().lstrip(",").strip()
    def segno(v: str) -> str:
        return v if v[0] in "+-" else "+" + v

    m = (_RE["ts"].search(testo) or _RE["ts_en"].search(testo)
         or _RE["ts_barre"].search(testo))
    if m:
        sb.ts = (f"Temp {segno(m.group(1))}, Rifl {segno(m.group(2))}, "
                 f"Vol {segno(m.group(3))}")
    else:
        # I tre tiri su tre righe separate. Si accettano SOLO se ci sono tutti e
        # tre: due su tre darebbe un blocco dall'aria completa a cui manca un
        # numero, che è peggio di un blocco che dichiara di non averlo.
        pezzi = [_RE[f"ts_{k}"].search(testo) for k in ("temp", "rifl", "vol")]
        if all(pezzi):
            sb.ts = ", ".join(f"{nome} {segno(p.group(1))}" for nome, p in
                              zip(("Temp", "Rifl", "Vol"), pezzi))
    # L'attacco finisce dove finisce la frase: nel formato compatto del repo
    # dopo il danno segue spesso tutt'altro («… (1d4+1). Scurovisione 18 m»).
    sb.attacchi = [f"{a} {_fino_al_punto(b)}" for a, b in _RE["attacco"].findall(testo)][:4]
    sb.voci = [f"{a}: {b.strip()}" for a, b in _RE["voce"].findall(testo)][:4]
    # Il markdown residuo non serve dentro un campo che verrà impaginato a parte.
    for chiave in ("tipo", "ca_dettaglio", "velocita"):
        setattr(sb, chiave, getattr(sb, chiave).replace("**", "").strip())
    sb.attacchi = [a.replace("**", "").strip() for a in sb.attacchi]
    sb.voci = [v.replace("**", "").strip() for v in sb.voci]
    # I dadi vita devono essere COERENTI con i pf. La frase di un attacco
    # («morso +24 (3d6+10 + 1d6 acido)») ha la stessa forma dei dadi vita, e
    # senza questo controllo usciva «pf: 215, pf-dado: 3d6+10» — due numeri che
    # si smentiscono a vicenda dentro lo stesso blocco. Meglio nessun dado vita
    # che un dado vita preso da un attacco.
    if sb.pf_dado and sb.pf:
        m2 = re.fullmatch(r"(\d+)d(\d+)\s*([+-]\s*\d+)?", sb.pf_dado.replace(" ", ""))
        try:
            n, faccia, extra = int(m2.group(1)), int(m2.group(2)), m2.group(3) or "0"
            media = n * (faccia / 2 + 0.5) + int(extra.replace(" ", ""))
            if abs(media - int(sb.pf)) > max(8, int(sb.pf) * 0.5):
                sb.pf_dado = ""
        except (AttributeError, ValueError):
            sb.pf_dado = ""

    # Una FORBICE lasciata aperta dal DM non è un numero da scegliere.
    #
    # Il dossier del Ghostlord scrive «Punti Ferita: 58–90 (13 DV; DM adatta al
    # livello del party — usare 90 se il party è ottimizzato)» e «Classe
    # Armatura: 24–26». Prendere il numero basso e tacere butterebbe via
    # un'istruzione di regia, e la scheda direbbe una cosa che il DM non ha
    # detto. Il blocco tiene l'estremo basso — serve un numero, e il basso è il
    # meno rischioso — e la forbice viene scritta accanto, dove si legge.
    for campo, etichetta in (("pf", "punti ferita"), ("ca", "CA")):
        m = _RE["forbice_" + campo].search(testo)
        if m:
            basso, alto = m.group(1), m.group(2)
            setattr(sb, campo, basso)
            sb.voci.append(f"⚠ Forbice del DM: {etichetta} {basso}–{alto} "
                           "(adattare al livello del gruppo)")

    # Se la prosa scriveva «hp ~30», il numero e' una STIMA del DM. Il blocco lo
    # dice, perche' altrimenti al tavolo non si distingue piu' da un numero
    # preso da un manuale — ed e' esattamente la confusione che ADR-0021 vieta.
    #
    # ⚠️ Ma il «~» va cercato dove i valori sono stati LETTI, non in tutto il
    # documento. Una scheda del lotto I chiudeva con una riga di collaudo — «PF
    # T1-1 riga CR 8 (CA ~21 / hp ~85)» — che parla della tabella di riferimento,
    # non della creatura: i suoi numeri erano esatti e il blocco li dichiarava
    # stimati. Marcare come incerto un numero certo e' lo stesso difetto di
    # marcare come certo un numero incerto, in direzione opposta: in due mesi
    # nessuno si fida piu' del marcatore.
    if _approssimato_dove_conta(testo):
        nota = "valori approssimati nella prosa d'origine (scritti con «~»)"
        sb.fonte = f"{sb.fonte} · {nota}" if sb.fonte else nota
    return sb, sb.mancanti()


def finestra_statistiche(testo: str) -> str:
    """La parte del documento che parla della creatura di QUESTA scheda.

    ⚠️ Difetto trovato nel lotto I, e vale la pena spiegarlo perché non è
    evidente: un dossier di villain descrive il villain **e il suo seguito**. Il
    Conte Valerius ha una sezione «Guardie del Corpo (×2 Guardamaglie)» con
    «CA: 24 (armatura completa +2)» e «PF: ~100 ciascuno». Il parser leggeva la
    CA giusta del Conte (13) e ci attaccava il dettaglio delle **guardie**, e
    marcava i suoi punti ferita esatti come «approssimati» perché il «~» delle
    guardie era da qualche parte nel file.

    Il risultato era un blocco che sembrava a posto e descriveva due creature
    diverse — il modo in cui un errore sopravvive a una rilettura.

    Quindi: dove la scheda è strutturata con intestazioni, si guarda **solo la
    sezione delle statistiche**, cioè da dove compaiono «Punti Ferita» o
    «Classe Armatura» fino alla prossima intestazione. Dove non lo è, si guarda
    tutto come prima: le schede compatte non hanno seguito.
    """
    righe = testo.split("\n")
    inizio = None
    for i, r in enumerate(righe):
        if re.search(r"\*{0,2}(Punti Ferita|Classe Armatura)\*{0,2}\s*:", r, re.I):
            inizio = i
            break
    if inizio is None:
        return testo
    # Si risale all'intestazione che apre la sezione, per non perdere il GS e il
    # tipo che spesso stanno qualche riga sopra.
    apertura = 0
    for i in range(inizio, -1, -1):
        if righe[i].startswith("#"):
            apertura = i
            break
    fine = len(righe)
    for i in range(inizio + 1, len(righe)):
        if righe[i].startswith("#"):
            fine = i
            break
    return "\n".join(righe[apertura:fine])


def _approssimato_dove_conta(testo: str) -> bool:
    """Vero se il «~» sta su un valore che il parser ha davvero letto.

    Guarda le sole righe in cui pf o CA compaiono come valore della creatura, e
    salta quelle che parlano di una tabella di riferimento.
    """
    for riga in testo.split("\n"):
        if "T1-1" in riga or "Benchmark" in riga or "riga CR" in riga:
            continue
        if _RE["approssimato"].search(riga):
            return True
    return False


def togli_blocco(testo: str) -> str:
    """Il testo senza il blocco: serve a chi impagina la prosa a parte."""
    righe = testo.split("\n")
    try:
        inizio = next(i for i, r in enumerate(righe) if r.strip() == APERTURA)
        fine = next(i for i in range(inizio + 1, len(righe)) if righe[i].strip() == CHIUSURA)
    except StopIteration:
        return testo
    return "\n".join(righe[:inizio] + righe[fine + 1:]).lstrip("\n")
