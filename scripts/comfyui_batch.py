#!/usr/bin/env python3
"""comfyui_batch.py — genera la serie di immagini di un modulo da ComfyUI, in modo RIPETIBILE.

Il repo sapeva già **scrivere** i prompt (ADR-0015) e **dirigerli**
(skill `rumblingstone-art-direction`). Mancava il pezzo in mezzo: eseguirli in
un ordine, con un seed annotato, e lasciare per iscritto con che pesi è stata
fatta ogni immagine (ADR-0019).

Generare a mano dalla GUI produce **una serie irripetibile**: fra un anno, con
due immagini da rifare, non si sa più né il prompt esatto né il seed. Questo
script legge i prompt **dal markdown** (che resta il master, ADR-0003), compone
il look comune e l'ancora storica, POSTa i workflow all'API locale di ComfyUI,
salva i PNG coi nomi esatti che i documenti si aspettano e scrive la riga di
`PROVENIENZA.txt`.

    PROMPT-RITRATTI-E-TAVOLE.md  →  workflow JSON  →  ComfyUI  →  <id>.png
                                                              →  PROVENIENZA.txt

⚖️ La licenza sta nei **pesi**, non nel software (ADR-0019): SDXL è il default,
FLUX.1 [schnell] è ammesso, **FLUX.1 [dev] è rifiutato dallo script** — non è un
avvertimento, è un exit 1.

Uso:
    python3 scripts/comfyui_batch.py --lista                 # cosa verrebbe generato
    python3 scripts/comfyui_batch.py --dry-run               # i prompt composti, senza rete
    python3 scripts/comfyui_batch.py                         # genera i 18 mancanti
    python3 scripts/comfyui_batch.py --solo ritratto-vanna --reroll 1 --forza \\
        --motivo «tre dita alla mano sinistra, la posa non regge l'inquadratura»
    python3 scripts/comfyui_batch.py --solo ritratto-vanna --fissa-seed   # lo blocca

Input:  un markdown coi blocchi annotati `<!-- img id=... size=... stile=... -->`
        (default: STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md)
Output: `<cartella del markdown>/<id>.png`, una riga per file in
        `PROVENIENZA.txt` (la scelta) e, a ogni `--reroll`, una riga in
        `SCARTI.txt` (il giudizio che l'ha preceduta)

Dipendenze: **sola stdlib** (urllib + json). Serve ComfyUI in ascolto in locale
(`scripts/comfyui-local/start.sh`); se non c'è, lo script dice come si avvia ed
esce pulito, senza lasciare file a metà.

Exit code: 0 = ok · 1 = ComfyUI assente, generazione fallita o pesi vietati ·
2 = uso errato (markdown mancante, id inesistente, `--reroll` senza `--motivo`).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DEFAULT = (
    ROOT
    / "STANDALONE-Il-Drappo-di-Tarsilia"
    / "ALLEGATI"
    / "immagini"
    / "PROMPT-RITRATTI-E-TAVOLE.md"
)
SERVER_DEFAULT = "http://127.0.0.1:8188"

# ── I pesi, e cosa se ne può fare ────────────────────────────────────────────
# ADR-0019: la licenza sta nei pesi, non nel software. Chi aggiunge una riga qui
# dichiara la licenza; chi mette `ammesso: False` sta chiudendo una porta, non
# esprimendo un gusto.
MODELLI = {
    "sdxl": {
        "checkpoint": "sd_xl_base_1.0.safetensors",
        "etichetta": "SDXL 1.0 base",
        "licenza": "OpenRAIL++-M (uso commerciale ammesso)",
        "ammesso": True,
        "steps": 30,
        "cfg": 7.0,
        "sampler": "dpmpp_2m",
        "scheduler": "karras",
    },
    "flux-schnell": {
        "checkpoint": "flux1-schnell-fp8.safetensors",
        "etichetta": "FLUX.1 [schnell] fp8",
        "licenza": "Apache-2.0",
        "ammesso": True,
        "steps": 4,
        "cfg": 1.0,
        "sampler": "euler",
        "scheduler": "simple",
    },
}

# Se il nome del checkpoint contiene una di queste, i pesi sono non commerciali.
# La licenza di FLUX.1 [dev] esclude anche l'uso «indirettamente connesso ad
# attivita' commerciali»: un modulo che un giorno potrebbe essere pubblicato non
# puo' contenerne. Vedi ADR-0019 §1.
PESI_VIETATI = ("flux1-dev", "flux.1-dev", "flux-dev", "fluxdev")

AVVIA_COMFYUI = """\
ComfyUI non risponde su {server}.

  scripts/comfyui-local/start.sh        # avvia il box e ComfyUI con --lowvram
  → http://127.0.0.1:8188

Setup la prima volta: scripts/comfyui-local/README.md (Distrobox + pesi).
Niente panico se non lo avvii ora: i segnaposto vettoriali del modulo restano
stampabili, e nessun file e' stato scritto (ADR-0019 §4).
"""

ANNOTAZIONE = re.compile(
    r"<!--\s*img\s+(?P<campi>[^>]*?)\s*-->\s*\n```\n(?P<corpo>.*?)\n```",
    re.DOTALL,
)
BLOCCO = re.compile(
    r"<!--\s*blocco\s+id=(?P<id>[a-z0-9-]+)\s*-->\s*\n```\n(?P<corpo>.*?)\n```",
    re.DOTALL,
)
CAMPO = re.compile(r"(\w+)=([^\s]+)")


@dataclass
class Immagine:
    """Una riga della serie: cosa generare, quanto grande, con che seed."""

    ident: str
    larghezza: int
    altezza: int
    stile: str
    serie: str
    corpo: str
    seed_fissato: int | None

    def seed(self, reroll: int) -> int:
        """Il seed: quello annotato se c'e', altrimenti uno stabile derivato dall'id.

        Derivarlo dall'id invece di sorteggiarlo significa che la serie e'
        riproducibile *anche prima* di aver scelto i seed buoni: due macchine
        diverse partono dalle stesse immagini. `--reroll` cambia il seed in modo
        altrettanto deterministico, cosi' anche il secondo tentativo si rifa'.
        """
        if self.seed_fissato is not None and reroll == 0:
            return self.seed_fissato
        base = self.ident if reroll == 0 else f"{self.ident}#{reroll}"
        digest = hashlib.sha256(base.encode("utf-8")).hexdigest()
        return int(digest[:8], 16) % (2**31 - 1)


# ── Lettura del markdown ─────────────────────────────────────────────────────


def leggi_blocchi(testo: str) -> dict[str, str]:
    """I blocchi condivisi del §1: look comune, negativi, ancora storica."""
    return {m.group("id"): _riga_unica(m.group("corpo")) for m in BLOCCO.finditer(testo)}


def leggi_immagini(testo: str) -> list[Immagine]:
    """Le immagini annotate, nell'ordine in cui compaiono nel documento."""
    fuori = []
    for m in ANNOTAZIONE.finditer(testo):
        campi = dict(CAMPO.findall(m.group("campi")))
        if "id" not in campi or "size" not in campi:
            continue
        larghezza, _, altezza = campi["size"].partition("x")
        seed = campi.get("seed")
        fuori.append(
            Immagine(
                ident=campi["id"],
                larghezza=int(larghezza),
                altezza=int(altezza),
                stile=campi.get("stile", "tavola"),
                serie=campi.get("serie", "base"),
                corpo=_riga_unica(m.group("corpo")),
                seed_fissato=int(seed) if seed and seed.isdigit() else None,
            )
        )
    return fuori


def _riga_unica(blocco: str) -> str:
    """Un blocco di prompt a capo multiplo diventa una riga sola, senza doppi spazi."""
    return " ".join(blocco.split())


def componi(img: Immagine, blocchi: dict[str, str]) -> tuple[str, str]:
    """Il prompt positivo e quello negativo, come li vedra' il modello.

    I prompt dei ritratti nel markdown iniziano con il segnaposto `[look comune]`:
    qui viene **sostituito**, non affiancato, cosi' il testo composto e' quello
    che il DM legge nel documento e non una sua approssimazione.
    """
    ancora = blocchi.get("ancora-storica", "")
    if img.stile == "ritratto":
        prefisso = ", ".join(p for p in (blocchi.get("look-comune", ""), ancora) if p)
    else:
        prefisso = ancora

    corpo = img.corpo
    if "[look comune]" in corpo:
        corpo = corpo.replace("[look comune] +", prefisso + ",").replace(
            "[look comune]", prefisso
        )
    elif prefisso:
        corpo = f"{prefisso}, {corpo}"
    return _riga_unica(corpo), blocchi.get("negativi", "")


# ── Il workflow ──────────────────────────────────────────────────────────────


def workflow(img: Immagine, positivo: str, negativo: str, seed: int, mod: dict) -> dict:
    """Il grafo txt2img in formato API di ComfyUI: nodo -> class_type + inputs.

    Un grafo solo per tutti i modelli, con i parametri di campionamento presi dal
    registro: SDXL vuole 30 passi a cfg 7, FLUX schnell 4 passi a cfg 1. Il
    `batch_size` resta 1 di proposito — su 6 GB di VRAM un batch e' il modo piu'
    rapido di far uscire ComfyUI per memoria esaurita.
    """
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": mod["steps"],
                "cfg": mod["cfg"],
                "sampler_name": mod["sampler"],
                "scheduler": mod["scheduler"],
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": mod["checkpoint"]},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": img.larghezza,
                "height": img.altezza,
                "batch_size": 1,
            },
        },
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": positivo, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negativo, "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": f"rumblingstone/{img.ident}", "images": ["8", 0]},
        },
    }


# ── Il client, in sola stdlib ────────────────────────────────────────────────


class Comfy:
    """Il minimo indispensabile dell'API di ComfyUI: accoda, aspetta, scarica."""

    def __init__(self, server: str, attesa_max: int):
        self.server = server.rstrip("/")
        self.attesa_max = attesa_max
        self.client_id = str(uuid.uuid4())

    def _get(self, percorso: str) -> bytes:
        with urllib.request.urlopen(f"{self.server}{percorso}", timeout=30) as r:
            return r.read()

    def stats(self) -> dict:
        return json.loads(self._get("/system_stats"))

    def accoda(self, grafo: dict) -> str:
        corpo = json.dumps({"prompt": grafo, "client_id": self.client_id}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.server}/prompt",
            data=corpo,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["prompt_id"]

    def aspetta(self, prompt_id: str) -> list[dict]:
        """Poll della cronologia finche' il nodo SaveImage non dichiara le immagini.

        ComfyUI ha una coda asincrona: la POST torna subito, il lavoro finisce
        dopo. Si aspetta sulla cronologia perche' e' l'unico canale che non
        richiede una websocket (e quindi una dipendenza in piu').
        """
        scadenza = time.monotonic() + self.attesa_max
        while time.monotonic() < scadenza:
            storia = json.loads(self._get(f"/history/{prompt_id}"))
            voce = storia.get(prompt_id)
            if voce:
                stato = voce.get("status", {})
                if stato.get("status_str") == "error":
                    raise RuntimeError(_errore_leggibile(stato))
                immagini = voce.get("outputs", {}).get("9", {}).get("images", [])
                if immagini:
                    return immagini
                if stato.get("completed"):
                    raise RuntimeError("il workflow e' finito senza produrre immagini")
            time.sleep(2)
        raise RuntimeError(f"nessuna immagine dopo {self.attesa_max}s")

    def scarica(self, immagine: dict) -> bytes:
        query = urllib.parse.urlencode(
            {
                "filename": immagine["filename"],
                "subfolder": immagine.get("subfolder", ""),
                "type": immagine.get("type", "output"),
            }
        )
        return self._get(f"/view?{query}")


def _errore_leggibile(stato: dict) -> str:
    """Estrae il messaggio utile dalla cronologia, che annida gli errori."""
    for tipo, dati in stato.get("messages", []):
        if tipo == "execution_error":
            nodo = dati.get("node_type", "?")
            return f"{nodo}: {dati.get('exception_message', 'errore ignoto')}"
    return "esecuzione fallita in ComfyUI"


# ── Provenienza (ADR-0019 §2) ────────────────────────────────────────────────

INTESTAZIONE_PROVENIENZA = """\
# Provenienza delle immagini — ADR-0019 §2
#
# Una riga per file, nel formato:
#   <file> · <modello e versione> · <licenza dei pesi> · seed <n> · <data> · <chi>
#
# Senza la sua riga, un'immagine non si committa: è l'unica cosa che rende
# reversibile fra un anno la scelta dei pesi. Le righe le scrive
# scripts/comfyui_batch.py; a mano si aggiungono solo gli asset importati.
#
# Pesi ammessi: SDXL (OpenRAIL++-M) · FLUX.1 [schnell] (Apache-2.0).
# FLUX.1 [dev] è vietato — la sua licenza esclude anche l'uso «indirettamente
# connesso ad attività commerciali». Lo script lo rifiuta da solo.
"""


def scrivi_provenienza(percorso: Path, nome: str, riga: str) -> None:
    """Aggiunge o **sostituisce** la riga di un file. Idempotente: rigenerare
    un'immagine aggiorna la sua riga invece di accodarne una seconda."""
    righe: list[str] = []
    if percorso.exists():
        righe = percorso.read_text(encoding="utf-8").rstrip("\n").split("\n")
    else:
        righe = INTESTAZIONE_PROVENIENZA.rstrip("\n").split("\n")

    prefisso = f"{nome} ·"
    for i, esistente in enumerate(righe):
        if esistente.startswith(prefisso):
            righe[i] = riga
            break
    else:
        righe.append(riga)
    percorso.write_text("\n".join(righe) + "\n", encoding="utf-8")


INTESTAZIONE_SCARTI = """\
# Scarti della serie — il registro di cosa NON si e' tenuto, e perche'
#
# Una riga per tentativo buttato, nel formato:
#   <id> · seed <n> · reroll <k> · <motivo>
#
# PROVENIENZA.txt registra la scelta; questo registra il giudizio che l'ha
# preceduta, che e' il lavoro vero e l'unico che altrimenti non lascia traccia.
# Il gate di rifiuto (skills/rumblingstone-art-direction/SKILL.md §6) dice
# quando un'immagine si butta invece di tenerla perche' «e' gia' venuta»: senza
# questo file, chi rifa' la serie fra un anno ripercorre gli stessi vicoli
# ciechi uno per uno.
#
# Il motivo e' testo libero e OBBLIGATORIO: --reroll senza --motivo esce 2.
# Scrivere «brutta» non serve a nessuno; «tre dita alla mano sinistra e la
# posa non regge l'inquadratura del capitolo» si.
"""


def scrivi_scarto(percorso: Path, ident: str, seed: int, reroll: int, motivo: str) -> None:
    """Registra un tentativo buttato. Idempotente sulla coppia (id, reroll):
    rilanciare lo stesso comando aggiorna la riga invece di accodarne una
    seconda, come fa gia' scrivi_provenienza per la scelta."""
    percorso.parent.mkdir(parents=True, exist_ok=True)
    if percorso.exists():
        righe = percorso.read_text(encoding="utf-8").rstrip("\n").split("\n")
    else:
        righe = INTESTAZIONE_SCARTI.rstrip("\n").split("\n")

    riga = f"{ident} · seed {seed} · reroll {reroll} · {motivo.strip()}"
    prefisso = f"{ident} · seed {seed} · reroll {reroll} ·"
    for i, esistente in enumerate(righe):
        if esistente.startswith(prefisso):
            righe[i] = riga
            break
    else:
        righe.append(riga)
    percorso.write_text("\n".join(righe) + "\n", encoding="utf-8")


def fissa_seed(percorso: Path, ident: str, seed: int) -> bool:
    """Scrive `seed=<n>` nell'annotazione di un'immagine, nel markdown master.

    E' il passo che trasforma «e' venuta bene» in «si rifa'»: senza, la
    generazione buona e' un colpo di fortuna non ripetibile (skill
    art-direction §4). Tocca **solo** la riga di annotazione, mai il prompt.
    """
    testo = percorso.read_text(encoding="utf-8")
    schema = re.compile(rf"(<!--\s*img\s+id={re.escape(ident)}\s[^>]*?)(\s*-->)")
    trovato = schema.search(testo)
    if not trovato:
        return False
    campi = re.sub(r"\s+seed=\d+", "", trovato.group(1))
    percorso.write_text(
        testo[: trovato.start()] + f"{campi} seed={seed}{trovato.group(2)}" + testo[trovato.end() :],
        encoding="utf-8",
    )
    return True


# ── CLI ──────────────────────────────────────────────────────────────────────


def costruisci_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="comfyui_batch.py",
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--prompts", type=Path, default=PROMPTS_DEFAULT,
                   help="Il markdown coi prompt annotati (default: quello del Drappo).")
    p.add_argument("--out", type=Path, default=None,
                   help="Cartella dei PNG (default: quella del markdown).")
    p.add_argument("--modello", choices=sorted(MODELLI), default="sdxl",
                   help="Quali pesi usare (default: sdxl, ADR-0019).")
    p.add_argument("--checkpoint", default=None,
                   help="Nome del file di checkpoint, se diverso da quello del registro.")
    p.add_argument("--serie", choices=["base", "extra", "tutto"], default="base",
                   help="base = i 18 del capitolato (default) · extra = solo gli oltre · tutto.")
    p.add_argument("--solo", action="append", default=[], metavar="ID",
                   help="Genera solo questo id (ripetibile).")
    p.add_argument("--reroll", type=int, default=0,
                   help="Cambia seed in modo deterministico: 1 = secondo tentativo, 2 = terzo.")
    p.add_argument("--motivo", default=None, metavar="TESTO",
                   help="Perche' il tentativo precedente si butta. OBBLIGATORIO con "
                        "--reroll: finisce in SCARTI.txt.")
    p.add_argument("--steps", type=int, default=None, help="Passi di campionamento.")
    p.add_argument("--cfg", type=float, default=None, help="Aderenza al prompt (CFG).")
    p.add_argument("--server", default=SERVER_DEFAULT, help=f"API ComfyUI (default: {SERVER_DEFAULT}).")
    p.add_argument("--attesa-max", type=int, default=900, metavar="SEC",
                   help="Secondi massimi di attesa per immagine (default: 900).")
    p.add_argument("--autore", default="DM", help="Chi ha generato, per PROVENIENZA.txt.")
    p.add_argument("--forza", action="store_true",
                   help="Rigenera anche i PNG gia' presenti (default: li salta).")
    p.add_argument("--fissa-seed", action="store_true",
                   help="Dopo la generazione, scrive il seed usato nel markdown.")
    p.add_argument("--lista", action="store_true", help="Elenca la serie risolta ed esci.")
    p.add_argument("--dry-run", action="store_true",
                   help="Compone i prompt e li stampa: nessuna rete, nessun file.")
    return p


def seleziona(immagini: list[Immagine], serie: str, solo: list[str]) -> list[Immagine]:
    if solo:
        per_id = {i.ident: i for i in immagini}
        ignoti = [s for s in solo if s not in per_id]
        if ignoti:
            raise KeyError(", ".join(ignoti))
        return [per_id[s] for s in solo]
    if serie == "tutto":
        return list(immagini)
    return [i for i in immagini if i.serie == serie]


def main(argv: list[str] | None = None) -> int:
    args = costruisci_parser().parse_args(argv)

    if not args.prompts.is_file():
        print(f"✗ markdown dei prompt non trovato: {args.prompts}", file=sys.stderr)
        return 2

    # --reroll dice che il tentativo prima si butta. Buttarlo senza scrivere
    # perche' e' esattamente il buco che SCARTI.txt chiude, quindi qui si esce
    # PRIMA di leggere, scrivere o chiamare la rete: un rifiuto senza motivo
    # non deve nemmeno cominciare.
    if args.reroll and not (args.motivo or "").strip():
        print(
            "✗ --reroll senza --motivo.\n"
            "  Un reroll butta il tentativo precedente, e il motivo e' l'unica cosa\n"
            "  che fra un anno evita di ripercorrere lo stesso vicolo cieco.\n"
            "  Esempio: --reroll 1 --motivo «tre dita alla mano sinistra, e la posa\n"
            "  non regge l'inquadratura del capitolo».",
            file=sys.stderr,
        )
        return 2

    testo = args.prompts.read_text(encoding="utf-8")
    blocchi = leggi_blocchi(testo)
    immagini = leggi_immagini(testo)
    if not immagini:
        print(f"✗ nessuna annotazione <!-- img ... --> in {args.prompts}", file=sys.stderr)
        return 2

    try:
        serie = seleziona(immagini, args.serie, args.solo)
    except KeyError as e:
        print(f"✗ id inesistente: {e}. Vedi --lista.", file=sys.stderr)
        return 2

    mod = dict(MODELLI[args.modello])
    if args.checkpoint:
        mod["checkpoint"] = args.checkpoint
        mod["etichetta"] = args.checkpoint
    if args.steps is not None:
        mod["steps"] = args.steps
    if args.cfg is not None:
        mod["cfg"] = args.cfg

    # Il cancello sui pesi. Sta PRIMA di ogni scrittura e di ogni chiamata di
    # rete, perche' un'immagine fatta con pesi vietati e' un problema anche se
    # non viene committata: ADR-0019 §1.
    ckpt = mod["checkpoint"].lower()
    if not mod["ammesso"] or any(v in ckpt for v in PESI_VIETATI):
        print(
            f"✗ pesi non ammessi: «{mod['checkpoint']}».\n"
            "  FLUX.1 [dev] gira sotto BFL Non-Commercial v2.0, che esclude anche\n"
            "  l'uso «indirettamente connesso ad attivita' commerciali». Un modulo\n"
            "  che un giorno potrebbe essere pubblicato non puo' contenerne.\n"
            "  Usa --modello sdxl (default) o --modello flux-schnell. Vedi\n"
            "  plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md §1.",
            file=sys.stderr,
        )
        return 1

    cartella = args.out or args.prompts.parent

    if args.lista:
        print(f"{len(serie)} immagini · {args.prompts.name} · modello {mod['etichetta']}")
        for img in serie:
            stato = "già presente" if (cartella / f"{img.ident}.png").exists() else "da fare"
            fissato = f"seed {img.seed_fissato} (fissato)" if img.seed_fissato else f"seed {img.seed(args.reroll)}"
            print(f"  {img.ident:26} {img.larghezza}x{img.altezza:<5} {img.stile:9} {img.serie:6} {fissato:22} {stato}")
        return 0

    if args.dry_run:
        for img in serie:
            positivo, negativo = componi(img, blocchi)
            print(f"── {img.ident} · {img.larghezza}x{img.altezza} · seed {img.seed(args.reroll)}")
            print(f"   + {positivo}")
            print(f"   − {negativo}\n")
        print(f"{len(serie)} prompt composti · nessun file scritto, nessuna chiamata di rete.")
        return 0

    comfy = Comfy(args.server, args.attesa_max)
    try:
        stats = comfy.stats()
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        print(AVVIA_COMFYUI.format(server=args.server), file=sys.stderr)
        return 1

    for dispositivo in stats.get("devices", []):
        vram = dispositivo.get("vram_total", 0)
        if 0 < vram < 8 * 1024**3:
            print(
                f"⚠ {dispositivo.get('name', 'GPU')}: {vram / 1024**3:.1f} GiB di VRAM.\n"
                "  Verifica che ComfyUI sia stato avviato con --lowvram "
                "(scripts/comfyui-local/start.sh lo fa gia').",
            )

    provenienza = cartella / "PROVENIENZA.txt"
    scarti = cartella / "SCARTI.txt"
    fatte, saltate, fallite = 0, 0, 0

    for img in serie:
        destinazione = cartella / f"{img.ident}.png"
        if destinazione.exists() and not args.forza:
            print(f"· {img.ident}: già presente, salto (--forza per rifarla)")
            saltate += 1
            continue

        seed = img.seed(args.reroll)
        # Lo scarto si registra PRIMA di rigenerare: il tentativo di ieri e'
        # stato buttato comunque, anche se quello di oggi fallisce.
        if args.reroll:
            scrivi_scarto(scarti, img.ident, img.seed(args.reroll - 1),
                          args.reroll - 1, args.motivo)
        positivo, negativo = componi(img, blocchi)
        print(f"▸ {img.ident} · {img.larghezza}x{img.altezza} · seed {seed} … ", end="", flush=True)
        try:
            prompt_id = comfy.accoda(workflow(img, positivo, negativo, seed, mod))
            uscite = comfy.aspetta(prompt_id)
            dati = comfy.scarica(uscite[0])
        except (urllib.error.URLError, OSError, RuntimeError, KeyError, json.JSONDecodeError) as e:
            print(f"✗ {e}")
            fallite += 1
            continue

        # Si scrive solo a download completo: niente PNG troncati sul disco.
        cartella.mkdir(parents=True, exist_ok=True)
        destinazione.write_bytes(dati)
        scrivi_provenienza(
            provenienza,
            destinazione.name,
            f"{destinazione.name} · {mod['etichetta']} · {mod['licenza']} · "
            f"seed {seed} · {date.today().isoformat()} · {args.autore}",
        )
        if args.fissa_seed and fissa_seed(args.prompts, img.ident, seed):
            print(f"✓ {len(dati) // 1024} KiB · seed fissato nel markdown")
        else:
            print(f"✓ {len(dati) // 1024} KiB")
        fatte += 1

    print(f"\n{fatte} generate · {saltate} saltate · {fallite} fallite → {cartella}")
    if fatte:
        print(
            "Il gate di rifiuto si applica IL GIORNO DOPO, non adesso: dopo quaranta\n"
            "generazioni si tiene tutto quello che e' «abbastanza». I sei controlli\n"
            "stanno in skills/rumblingstone-art-direction/SKILL.md §6."
        )
    return 1 if fallite else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
