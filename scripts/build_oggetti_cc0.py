#!/usr/bin/env python3
"""
build_oggetti_cc0.py — gli oggetti di scena del tema «texture» delle mappe, dai
modelli 3D CC0 resi dall'alto con Blender (R4-ter di PIANO-RESA-E-ASSET, D17).

Nel tema texture una roccia, una statua, un letto non sono più un glifo
vettoriale: sono una tessera webp con trasparenza, resa da un modello 3D
zenitale con la stessa camera, la stessa luce e la stessa scala per ogni
oggetto. La pergamena tiene i glifi. Restano glifi anche nel tema texture il
fuoco e gli effetti, le porte, le finestre e le sbarre (ruotano con l'asse del
muro, ADR-0083) e i segnali che non sono oggetti: `RESTANO_GLIFI` nel renderer.

Le fonti, con la licenza letta alla fonte il 2026-10-09:

- **Poly Haven**, CC0 1.0 (pagina «License»): il glTF 1k di ogni modello, con
  l'MD5 di ogni file dichiarato dall'API e verificato. Gli id del primo giro
  hanno anche l'MD5 del glTF fissato qui: se Poly Haven cambia il modello, lo
  scaricamento si ferma invece di produrre una tessera diversa in silenzio.
- **Quaternius**, Fantasy Props MegaKit, solo la versione Standard (gratuita),
  CC0 1.0. Lo zip lo scarica il DM da itch.io: l'impronta dello zip è fissata
  in `QUATERNIUS_ZIP_SHA256` e lo zip deve contenere un file di licenza che
  dice CC0. La tabella `simbolo → file` si scrive sui nomi veri
  (`--elenca-quaternius`), non su nomi indovinati.

I modelli scaricati stanno in `asset-esterni/oggetti-cc0/`, ignorata da git.
Nel repo entrano le tessere (`scripts/oggetti-cc0/<tessera>.webp`) e l'indice,
con fonte, id, licenza, MD5 dei file d'origine e sha256 della tessera.

    python3 scripts/build_oggetti_cc0.py                    # scarica Poly Haven, rende, scrive le tessere
    python3 scripts/build_oggetti_cc0.py --prova           # solo il giro di prova (PILOTA)
    python3 scripts/build_oggetti_cc0.py --scarica-solo     # scarica e verifica, senza Blender
    python3 scripts/build_oggetti_cc0.py --rendi            # rende da asset-esterni/, senza rete
    python3 scripts/build_oggetti_cc0.py --quaternius Z.zip # aggiunge i modelli Quaternius dallo zip
    python3 scripts/build_oggetti_cc0.py --elenca-quaternius Z.zip   # impronta, licenza, nomi dei file
    python3 scripts/build_oggetti_cc0.py --misura-stile     # luce, saturazione, dettaglio per fonte
    python3 scripts/build_oggetti_cc0.py --da-immagini DIR --variante a -o CAND  # PNG di ComfyUI → candidati
    python3 scripts/build_oggetti_cc0.py --check            # niente rete: tessere e indice combaciano

Blender: il binario `blender` nel PATH, `--blender CMD`, oppure il modulo `bpy`
nel Python che esegue lo script (`pip install bpy`, Python 3.13).

`--check` esce 0 anche se le tessere non sono ancora state fatte (lo dice); esce
1 se una tessera manca, non combacia o viene da un modello non verificato.
Exit 2 senza Pillow, o senza Blender quando serve rendere.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import posixpath
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
USCITA = RADICE / "oggetti-cc0"
INDICE = USCITA / "indice.json"
CACHE = REPO / "asset-esterni" / "oggetti-cc0"
SCENA = RADICE / "blender" / "rendi_oggetti.py"
API = "https://api.polyhaven.com/files/{id}"
PAGINA = "https://polyhaven.com/a/{id}"
PAGINA_QUATERNIUS = "https://quaternius.com/packs/fantasypropsmegakit.html"
LATO = 96         # px della tessera: una cella del renderer è 28 px, così regge un PNG a 3×
QUALITA = 80      # webp con trasparenza

#: I lock del set (`rumblingstone-art-direction` §4): uguali per ogni modello.
#: La luce viene da nord-ovest, alta, come l'ombra disegnata sotto i glifi della
#: pergamena (spostata a sud-est). L'impronta è la frazione della cella che il
#: lato lungo del modello occupa: la scala non è quella vera, perché una statua
#: e un vaso devono leggersi entrambi in un quadretto da 1,5 m.
LOCK = {
    "campioni": 64, "seme": 0, "denoise": True, "lato_render": 2 * LATO,
    "fondo": 0.9, "sole": 2.2, "sole_morbidezza_gradi": 8,
    "sole_azimut_gradi": 315, "sole_elevazione_gradi": 65,
    "impronta": 0.76,
}

#: (simbolo, fonte, id). Più righe per lo stesso simbolo sono varianti, scelte
#: cella per cella come le varianti dei glifi. Fonte «polyhaven»: l'id dell'API.
#: Fonte «quaternius»: il percorso del modello dentro lo zip Standard.
OGGETTI: tuple[tuple[str, str, str], ...] = (
    ("🪨", "polyhaven", "boulder_01"),
    ("🪨", "polyhaven", "namaqualand_boulders_01"),
    ("🗿", "polyhaven", "gothic_statue"),
    ("🏮", "polyhaven", "stone_fire_pit"),
    ("🛏", "polyhaven", "GothicBed_01"),
    ("🏺", "polyhaven", "ceramic_pot"),
    ("🪑", "polyhaven", "WoodenTable_01"),
    ("🛢", "polyhaven", "wine_barrel_01"),
    ("📦", "polyhaven", "wooden_crate_02"),
    ("🪵", "polyhaven", "dead_tree_trunk_02"),
    ("🧰", "polyhaven", "treasure_chest"),
    ("📚", "polyhaven", "wooden_bookshelf_worn"),
    ("🗄", "polyhaven", "GothicCabinet_01"),
    ("🕯", "polyhaven", "brass_candleholders"),
    ("🌾", "polyhaven", "fern_02"),
    ("🧱", "polyhaven", "namaqualand_rocks_01"),
)

#: Le tessere che non seguono i lock comuni. Il muretto 🧱 (D21) continua come
#: un muro: occupa la cella intera sul lato lungo, così due tratti vicini si
#: toccano, e si rende due volte, est-ovest e nord-sud. Si gira il modello e non
#: l'immagine, perché la luce deve restare da nord-ovest; la tessera nord-sud si
#: chiama «<tessera>-ns» e il renderer la sceglie dai vicini.
OPZIONI: dict[str, dict] = {
    "namaqualand_rocks_01": {"impronta": 1.0, "orientabile": True},
}
SUFFISSO_NS = "-ns"

#: I simboli che Poly Haven non copre e che si cercano nella parte gratuita di
#: Quaternius (D17). Restano glifi finché il DM non ha mandato l'elenco dei
#: file dello zip e la tabella non ha la riga con il nome vero.
CERCATI_IN_QUATERNIUS = "⛺⚒🛐👑⚰🦴🍄⛲🧪🪓🔮🔷🔺"

#: Il giro di prova (D17: «misurala su una prova, e portala al DM prima di
#: estenderla»): gli oggetti delle due mappe del confronto, M7-D livello 1
#: (interni, con quattro celle di muretto) e il cortile interno di ARC07 (esterno).
PILOTA = ("boulder_01", "namaqualand_boulders_01", "gothic_statue", "stone_fire_pit",
          "ceramic_pot", "GothicBed_01", "WoodenTable_01", "namaqualand_rocks_01")

#: L'MD5 del glTF 1k letto dall'API il 2026-10-09 (`api.polyhaven.com/files/<id>`).
GLTF_FISSATI = {
    "boulder_01": "26e2eef4a1f68c9557c65cd375b21d6c",
    "namaqualand_boulders_01": "904c7349856f65f757b7f6fd36f57641",
    "gothic_statue": "4fb49ae8f4278a0f5f1c7ca89a416f69",
    "stone_fire_pit": "f3a23e45ee66802ccc7a5462a9371ae3",
}

#: L'impronta dello zip Standard di Quaternius, fissata la prima volta che il
#: DM lo installa. Vuota: lo zip non è ancora arrivato, e --quaternius si ferma
#: dopo aver stampato l'impronta da scrivere qui.
QUATERNIUS_ZIP_SHA256 = ""
#: (simbolo, percorso del modello nello zip): si riempie con --elenca-quaternius.
QUATERNIUS: tuple[tuple[str, str], ...] = ()

PAROLE_CC0 = ("cc0", "creative commons zero", "publicdomain/zero")

#: Le tessere generate in locale con ComfyUI (D25) che hanno vinto il
#: confronto: (simbolo, id dell'immagine). Vuota finché il DM non ha generato,
#: misurato e scelto. La provenienza (modello, seme, licenza dei pesi) sta
#: nell'indice, letta da PROVENIENZA.txt (ADR-0019 §2).
GENERATE: tuple[tuple[str, str], ...] = ()
PROMPT_COMFYUI = REPO / "plans" / "esperimenti" / "oggetti-cc0-2026-10" / "comfyui" / "PROMPT-OGGETTI-ZENITALI.md"
LICENZA_GENERATA = "generata in locale, pesi ammessi da ADR-0019"


def _rel(p: Path) -> str:
    """Il percorso come lo legge il DM: relativo al repo quando ci sta dentro."""
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def _tessera(fonte: str, ident: str) -> str:
    if fonte == "polyhaven":
        return ident
    return "quaternius-" + PurePosixPath(ident).stem.lower().replace(" ", "-")


def tabella() -> list[tuple[str, str, str, str]]:
    """(simbolo, fonte, id, tessera) di tutti gli oggetti, Quaternius compreso."""
    righe = [(s, f, i, _tessera(f, i)) for s, f, i in OGGETTI]
    righe += [(s, "quaternius", p, _tessera("quaternius", p)) for s, p in QUATERNIUS]
    righe += [(s, "comfyui", i, i) for s, i in GENERATE]
    return righe


def _pillow():
    try:
        from PIL import Image
    except ImportError:
        print("✗ build_oggetti_cc0 ha bisogno di Pillow: pip install -r requirements.txt",
              file=sys.stderr)
        return None
    return Image


def _scarica(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "RumblingStone build_oggetti_cc0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def _md5(dati: bytes) -> str:
    return hashlib.md5(dati).hexdigest()


def _sha256(dati: bytes) -> str:
    return hashlib.sha256(dati).hexdigest()


def _percorso_sicuro(base: Path, rel: str) -> Path:
    """`rel` dentro `base`, mai fuori: niente percorsi assoluti né `..`."""
    p = PurePosixPath(rel)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise ValueError(f"percorso non ammesso: {rel}")
    return base.joinpath(*p.parts)


# --- Poly Haven ---------------------------------------------------------------

def scarica_polyhaven(pid: str) -> dict:
    """Il glTF 1k e i suoi file in CACHE/polyhaven/<id>/, ogni MD5 verificato
    contro l'API; `fonte.json` registra URL e MD5 per il render senza rete."""
    voce = json.loads(_scarica(API.format(id=pid)))["gltf"]["1k"]["gltf"]
    atteso = GLTF_FISSATI.get(pid)
    if atteso and voce["md5"] != atteso:
        raise ValueError(f"{pid}: Poly Haven dichiara un glTF diverso da quello fissato "
                         f"({voce['md5']} invece di {atteso}): rivedi il modello prima di aggiornarlo")
    cartella = CACHE / "polyhaven" / pid
    file = {f"{pid}_1k.gltf": {"url": voce["url"], "md5": voce["md5"]}}
    file.update({rel: {"url": v["url"], "md5": v["md5"]} for rel, v in voce["include"].items()})
    for rel, v in file.items():
        dati = _scarica(v["url"])
        if _md5(dati) != v["md5"]:
            raise ValueError(f"{pid}/{rel}: MD5 {_md5(dati)} diverso da quello dell'API ({v['md5']})")
        dest = _percorso_sicuro(cartella, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(dati)
    fonte = {"fonte": "Poly Haven", "id": pid, "pagina": PAGINA.format(id=pid),
             "licenza": "CC0 1.0", "modello": f"{pid}_1k.gltf", "file": file}
    (cartella / "fonte.json").write_text(json.dumps(fonte, indent=1) + "\n", encoding="utf-8")
    return fonte


def verifica_in_cache(tessera: str) -> dict:
    """La `fonte.json` di un modello in cache, dopo aver riverificato ogni file."""
    cartella = next((c for c in (CACHE / "polyhaven" / tessera, CACHE / "quaternius" / tessera)
                     if (c / "fonte.json").exists()), None)
    if cartella is None:
        raise FileNotFoundError(f"{tessera}: modello non scaricato in {_rel(CACHE)}/")
    fonte = json.loads((cartella / "fonte.json").read_text(encoding="utf-8"))
    for rel, v in fonte["file"].items():
        p = _percorso_sicuro(cartella, rel)
        if not p.exists():
            raise FileNotFoundError(f"{tessera}/{rel}: manca")
        dati = p.read_bytes()
        if "md5" in v and _md5(dati) != v["md5"]:
            raise ValueError(f"{tessera}/{rel}: MD5 diverso da quello registrato allo scaricamento")
        if "sha256" in v and _sha256(dati) != v["sha256"]:
            raise ValueError(f"{tessera}/{rel}: sha256 diverso da quello registrato all'estrazione")
    fonte["_cartella"] = str(cartella)
    return fonte


# --- Quaternius ---------------------------------------------------------------

def _licenza_nello_zip(z: zipfile.ZipFile) -> tuple[str | None, str]:
    for nome in z.namelist():
        base = PurePosixPath(nome).name.lower()
        if base.startswith("license") or base.startswith("licence"):
            testo = z.read(nome).decode("utf-8", "replace")
            return nome, testo
    return None, ""


def elenca_quaternius(zpath: Path) -> int:
    dati = zpath.read_bytes()
    print(f"zip: {zpath.name}  ({len(dati)} byte)")
    print(f"sha256: {_sha256(dati)}")
    with zipfile.ZipFile(io.BytesIO(dati)) as z:
        nome, testo = _licenza_nello_zip(z)
        if nome:
            cc0 = any(p in testo.lower() for p in PAROLE_CC0)
            print(f"licenza: {nome} — {'dice CC0' if cc0 else '⚠ NON dice CC0'}")
            for riga in testo.strip().splitlines()[:6]:
                print(f"    {riga}")
        else:
            print("licenza: ⚠ nessun file di licenza nello zip")
        modelli = sorted(n for n in z.namelist()
                         if PurePosixPath(n).suffix.lower() in (".gltf", ".glb"))
        print(f"modelli glTF: {len(modelli)}")
        for n in modelli:
            print(f"    {n}")
    print(f"\nSimboli che si cercano qui: {' '.join(CERCATI_IN_QUATERNIUS)}")
    return 0


def estrai_quaternius(zpath: Path) -> list[dict]:
    """Estrae i modelli di QUATERNIUS (e i file che il glTF richiama) in
    CACHE/quaternius/<tessera>/, dopo aver verificato impronta e licenza."""
    dati = zpath.read_bytes()
    impronta = _sha256(dati)
    if not QUATERNIUS_ZIP_SHA256:
        raise ValueError(f"impronta dello zip non ancora fissata: è {impronta}. "
                         f"Scrivila in QUATERNIUS_ZIP_SHA256 dopo averne letto la licenza "
                         f"(--elenca-quaternius)")
    if impronta != QUATERNIUS_ZIP_SHA256:
        raise ValueError(f"{zpath.name}: sha256 {impronta} diverso da quello fissato "
                         f"({QUATERNIUS_ZIP_SHA256}): è un altro zip, forse la versione Pro")
    fonti = []
    with zipfile.ZipFile(io.BytesIO(dati)) as z:
        nome, testo = _licenza_nello_zip(z)
        if not nome or not any(p in testo.lower() for p in PAROLE_CC0):
            raise ValueError(f"{zpath.name}: lo zip non contiene una licenza che dica CC0")
        for simbolo, interno in QUATERNIUS:
            tessera = _tessera("quaternius", interno)
            cartella = CACHE / "quaternius" / tessera
            richiesti = [interno]
            if interno.lower().endswith(".gltf"):
                gltf = json.loads(z.read(interno))
                base = PurePosixPath(interno).parent
                uris = [b.get("uri") for b in gltf.get("buffers", [])]
                uris += [i.get("uri") for i in gltf.get("images", [])]
                # i pacchetti richiamano spesso le texture con «../»: si tiene
                # il percorso interno dello zip, così il glTF le ritrova
                richiesti += [posixpath.normpath(str(base / urllib.parse.unquote(u)))
                              for u in uris if u and not u.startswith("data:")]
            file = {}
            for n in richiesti:
                contenuto = z.read(n)
                rel = n
                dest = _percorso_sicuro(cartella, rel)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(contenuto)
                file[rel] = {"zip": zpath.name, "voce": n, "sha256": _sha256(contenuto)}
            fonte = {"fonte": "Quaternius", "id": interno, "pagina": PAGINA_QUATERNIUS,
                     "licenza": "CC0 1.0", "pacchetto": "Fantasy Props MegaKit [Standard]",
                     "zip_sha256": impronta, "modello": interno, "file": file}
            (cartella / "fonte.json").write_text(json.dumps(fonte, indent=1) + "\n",
                                                 encoding="utf-8")
            fonti.append(fonte)
    return fonti


# --- Blender -----------------------------------------------------------------

def comando_blender(esplicito: str | None) -> list[str] | None:
    """Il modo di far girare la scena: `--blender`, il modulo bpy, o il binario.

    Il modulo viene prima del programma: la sua versione la fissa
    `requirements-completo.txt`, quella del programma la decide la distribuzione.
    Il 2026-10-09, sulla macchina del DM, il Blender di Debian (4.3, senza
    OpenImageDenoise) veniva preso al posto del bpy 5.2 del `.venv`."""
    if esplicito:
        return [*esplicito.split(), "-b", "--factory-startup", "-noaudio", "-P", str(SCENA), "--"]
    if importlib.util.find_spec("bpy") is not None:
        return [sys.executable, str(SCENA)]
    if shutil.which("blender"):
        return ["blender", "-b", "--factory-startup", "-noaudio", "-P", str(SCENA), "--"]
    return None


def rendi(fonti: dict[str, dict], blender: list[str], Image) -> dict[str, dict]:
    """Rende ogni modello in un PNG a 2×LATO, lo riduce a LATO e lo scrive in webp."""
    USCITA.mkdir(exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    # dentro asset-esterni/ e non in /tmp: il Blender in flatpak ha una /tmp sua
    with tempfile.TemporaryDirectory(dir=CACHE) as tmp:
        t = Path(tmp)
        modelli = []
        for k, f in fonti.items():
            opz = OPZIONI.get(k, {})
            assi = ("ew", "ns") if opz.get("orientabile") else ("ew",)
            for asse in assi:
                nome = k + (SUFFISSO_NS if asse == "ns" else "")
                modelli.append({"tessera": nome, "asse": asse,
                                "impronta": opz.get("impronta", LOCK["impronta"]),
                                "modello": str(Path(f["_cartella"]) / f["modello"]),
                                "uscita": str(t / f"{nome}.png")})
        lavoro = {"lock": LOCK, "esiti": str(t / "esiti.json"), "modelli": modelli}
        (t / "lavoro.json").write_text(json.dumps(lavoro), encoding="utf-8")
        r = subprocess.run([*blender, str(t / "lavoro.json")], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"Blender è uscito con {r.returncode}:\n{r.stderr[-2000:]}")
        esiti = json.loads((t / "esiti.json").read_text(encoding="utf-8"))
        versione = next((ln.split(" ", 1)[1] for ln in r.stdout.splitlines()
                         if ln.startswith("Blender ")), "?")
        risultato = {}
        for m in modelli:
            k = m["tessera"]
            webp = tessera_webp(Image, (t / f"{k}.png").read_bytes())
            (USCITA / f"{k}.webp").write_bytes(webp)
            risultato[k] = {"render": esiti[k], "byte": len(webp), "sha256": _sha256(webp),
                            "blender": versione}
            print(f"✓ {k}: {len(webp)} byte")
    return risultato


def tessera_webp(Image, png: bytes) -> bytes:
    im = Image.open(io.BytesIO(png)).convert("RGBA").resize((LATO, LATO), Image.LANCZOS)
    out = io.BytesIO()
    im.save(out, "WEBP", quality=QUALITA, method=6)
    return out.getvalue()


def scrivi_indice(voci: dict[str, dict]) -> None:
    """Fonde le voci nuove con l'indice che c'è: un giro di prova non cancella
    le tessere già fatte, e un simbolo elenca solo le tessere che esistono."""
    vecchio = json.loads(INDICE.read_text(encoding="utf-8")) if INDICE.exists() else {}
    tessere = {**vecchio.get("tessere", {}), **voci}
    simboli: dict[str, list[str]] = {}
    for s, _, _, k in tabella():
        if k in tessere:
            simboli.setdefault(s, []).append(k)
    orientabili = sorted(k for k, o in OPZIONI.items()
                         if o.get("orientabile") and k in tessere and k + SUFFISSO_NS in tessere)
    indice = {"lato": LATO, "qualita": QUALITA, "lock": LOCK, "opzioni": OPZIONI,
              "simboli": simboli, "orientabili": orientabili,
              "tessere": dict(sorted(tessere.items()))}
    INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def costruisci(args) -> int:
    Image = _pillow()
    if Image is None:
        return 2
    righe = [r for r in tabella() if not args.prova or r[3] in PILOTA]
    if args.quaternius:
        try:
            estrai_quaternius(args.quaternius)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
            print(f"✗ Quaternius: {e}", file=sys.stderr)
            return 1
    if not args.rendi:
        for _, fonte, ident, k in righe:
            if fonte != "polyhaven":
                continue
            try:
                scarica_polyhaven(ident)
                print(f"✓ scaricato e verificato: {ident}")
            except (OSError, ValueError, KeyError) as e:
                print(f"✗ {ident}: {e}", file=sys.stderr)
                return 1
    if args.scarica_solo:
        print(f"Modelli in {_rel(CACHE)}/. Per le tessere: --rendi")
        return 0
    fonti = {}
    for _, fonte, _, k in righe:
        if fonte == "quaternius" and not (CACHE / "quaternius" / k / "fonte.json").exists():
            print(f"○ {k}: lo zip di Quaternius non è stato dato (--quaternius), resta il glifo")
            continue
        try:
            fonti[k] = verifica_in_cache(k)
        except FileNotFoundError as e:
            if not args.rendi:
                print(f"✗ {e}", file=sys.stderr)
                return 1
            print(f"○ {e}: resta il glifo")
        except (OSError, ValueError) as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1
    if not fonti:
        print("○ nessun modello da rendere")
        return 0
    blender = comando_blender(args.blender)
    if blender is None:
        print("✗ serve Blender: il binario `blender` (blender.org, GPL), --blender CMD, "
              "oppure `pip install bpy` nel Python che lancia lo script", file=sys.stderr)
        return 2
    try:
        fatte = rendi(fonti, blender, Image)
    except (RuntimeError, OSError, KeyError, ValueError) as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    voci = {}
    for nome, fatta in fatte.items():
        k = nome.removesuffix(SUFFISSO_NS) if nome not in fonti else nome
        f = fonti[k]
        voci[nome] = {"fonte": f["fonte"], "id": f["id"], "pagina": f["pagina"],
                      "licenza": f["licenza"], "verificato": True, "file": f["file"],
                      **({"zip_sha256": f["zip_sha256"]} if "zip_sha256" in f else {}),
                      **({"asse": "ns" if nome != k else "ew"} if k in OPZIONI and
                         OPZIONI[k].get("orientabile") else {}),
                      **fatta}
    scrivi_indice(voci)
    print(f"Indice: {_rel(INDICE)} — poi: python3 scripts/dm.py maps texture")
    return 0


# --- le immagini generate con ComfyUI (D25) ------------------------------------

def da_immagini(cartella: Path, variante: str, uscita: Path, Image) -> int:
    """Le PNG di `comfyui_batch.py` (sfondo bianco) in tessere candidate: lo
    sfondo si toglie partendo dagli angoli, l'oggetto si ritaglia e si mette
    nella cella con la stessa impronta dei modelli (D20). L'uscita è una
    cartella di candidati, con l'indice, per `misura_resa.py candidati` e
    `coppie`: non entra in scripts/oggetti-cc0/ finché non vince."""
    import re
    import numpy as np
    testo = PROMPT_COMFYUI.read_text(encoding="utf-8")
    simbolo_di = dict((m.group(1), m.group(2)) for m in
                      re.finditer(r"<!--\s*img\s+id=(\S+)[^>]*?simbolo=(\S+)\s*-->", testo))
    prov = {}
    pf = cartella / "PROVENIENZA.txt"
    if pf.exists():
        for riga in pf.read_text(encoding="utf-8").splitlines():
            prov[riga.split(" ·", 1)[0].strip()] = riga.strip()
    uscita.mkdir(parents=True, exist_ok=True)
    tessere, simboli = {}, {}
    for ident, simbolo in simbolo_di.items():
        if not ident.endswith(f"-{variante}"):
            continue
        png = cartella / f"{ident}.png"
        if not png.exists():
            print(f"○ {ident}: immagine non generata")
            continue
        im = np.asarray(Image.open(png).convert("RGB"), dtype=np.float64)
        angoli = np.concatenate([im[:8, :8].reshape(-1, 3), im[:8, -8:].reshape(-1, 3),
                                 im[-8:, :8].reshape(-1, 3), im[-8:, -8:].reshape(-1, 3)]).mean(axis=0)
        figura = np.sqrt(((im - angoli) ** 2).sum(axis=2)) > 30
        if figura.sum() < 50:
            print(f"✗ {ident}: nessuna figura sullo sfondo", file=sys.stderr)
            continue
        ys, xs = np.nonzero(figura)
        rgba = np.dstack([im, figura * 255.0]).astype("uint8")
        ritaglio = Image.fromarray(rgba, "RGBA").crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        lato = 2 * LATO
        scala = LOCK["impronta"] * lato / max(ritaglio.size)
        ritaglio = ritaglio.resize((max(1, round(ritaglio.width * scala)),
                                    max(1, round(ritaglio.height * scala))), Image.LANCZOS)
        tela = Image.new("RGBA", (lato, lato), (0, 0, 0, 0))
        tela.alpha_composite(ritaglio, ((lato - ritaglio.width) // 2, (lato - ritaglio.height) // 2))
        out = io.BytesIO()
        tela.save(out, "PNG")
        webp = tessera_webp(Image, out.getvalue())
        (uscita / f"{ident}.webp").write_bytes(webp)
        tessere[ident] = {"fonte": "ComfyUI", "id": ident, "licenza": LICENZA_GENERATA,
                          "provenienza": prov.get(ident, ""), "verificato": bool(prov.get(ident)),
                          "byte": len(webp), "sha256": _sha256(webp)}
        simboli.setdefault(simbolo, []).append(ident)
        print(f"✓ {ident} → {simbolo}: {len(webp)} byte")
    (uscita / "indice.json").write_text(json.dumps(
        {"lato": LATO, "qualita": QUALITA, "variante": variante, "simboli": simboli,
         "orientabili": [], "tessere": tessere}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0 if tessere else 1


# --- controlli e misure --------------------------------------------------------

def controlla() -> int:
    if not INDICE.exists():
        print("○ build_oggetti_cc0: tessere degli oggetti non ancora fatte (scripts/oggetti-cc0/). "
              "Nel tema texture restano i glifi: python3 scripts/build_oggetti_cc0.py")
        return 0
    sys.path.insert(0, str(RADICE))
    import render_map_svg as R
    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    errori = []
    tab = {k: s for s, _, _, k in tabella()}
    for s, ks in indice.get("simboli", {}).items():
        if R.resta_glifo(s):
            errori.append(f"{s}: è un simbolo che resta glifo (RESTANO_GLIFI o chiusura)")
        for k in ks:
            if tab.get(k) != s:
                errori.append(f"{s} → {k}: la tabella OGGETTI non lo dice")
    for k in indice.get("orientabili", []):
        if not OPZIONI.get(k, {}).get("orientabile"):
            errori.append(f"{k}: orientabile nell'indice ma non in OPZIONI")
        if k + SUFFISSO_NS not in indice.get("tessere", {}):
            errori.append(f"{k}: manca la tessera nord-sud {k + SUFFISSO_NS}")
    for k, voce in indice.get("tessere", {}).items():
        p = USCITA / f"{k}.webp"
        if not p.exists():
            errori.append(f"{k}: manca la tessera")
        elif _sha256(p.read_bytes()) != voce.get("sha256"):
            errori.append(f"{k}: la tessera non combacia con l'indice")
        if voce.get("licenza") == LICENZA_GENERATA:
            if not voce.get("provenienza"):
                errori.append(f"{k}: immagine generata senza la riga di PROVENIENZA (ADR-0019 §2)")
        elif voce.get("licenza") != "CC0 1.0":
            errori.append(f"{k}: licenza «{voce.get('licenza')}», ammesse CC0 1.0 o {LICENZA_GENERATA}")
        if voce.get("verificato") is not True:
            errori.append(f"{k}: il modello d'origine non è stato verificato contro la fonte")
        if voce.get("fonte") == "Quaternius" and voce.get("zip_sha256") != QUATERNIUS_ZIP_SHA256:
            errori.append(f"{k}: viene da uno zip Quaternius diverso da quello fissato")
    for s in indice.get("simboli", {}):
        errori += approvazioni({"simboli": {s: []}}, fonte_di(USCITA, s))
    for e in errori:
        print(f"✗ build_oggetti_cc0: {e}")
    if not errori:
        n = len(indice.get("tessere", {}))
        print(f"✓ build_oggetti_cc0: {n} tessere CC0 per {len(indice.get('simboli', {}))} simboli, "
              f"{sum(v['byte'] for v in indice.get('tessere', {}).values())} byte")
    return 1 if errori else 0


SCHEDA_RESA = RADICE / "scheda-resa.json"


def adotta(cartella: Path | None = None) -> int:
    """Dopo i voti (D23): tiene in `scripts/oggetti-cc0/` solo i simboli la cui
    tessera la misura non boccia e il DM ha preferito al glifo. Senza cartella
    sfoltisce le tessere CC0 già rese; con una cartella di candidati (per
    esempio di `--da-immagini`) copia dentro le tessere approvate, al posto di
    quelle che il simbolo aveva."""
    sorgente = cartella or USCITA
    if not (sorgente / "indice.json").exists():
        print(f"✗ {sorgente} non ha indice.json: prima le tessere "
              "(build_oggetti_cc0.py --prova, o --da-immagini)", file=sys.stderr)
        return 1
    ind_s = json.loads((sorgente / "indice.json").read_text(encoding="utf-8"))
    tenuti, scartati = [], {}
    for s in ind_s.get("simboli", {}):
        errori = approvazioni({"simboli": {s: []}}, fonte_di(sorgente, s))
        (scartati.__setitem__(s, errori) if errori else tenuti.append(s))

    def _sue(ind, s):
        ks = list(ind.get("simboli", {}).get(s, []))
        return ks + [k + SUFFISSO_NS for k in ks if k + SUFFISSO_NS in ind.get("tessere", {})]

    dest = json.loads(INDICE.read_text(encoding="utf-8")) if INDICE.exists() else {
        "lato": LATO, "qualita": QUALITA, "lock": LOCK, "opzioni": OPZIONI}
    dest.setdefault("simboli", {}), dest.setdefault("tessere", {})
    via = [s for s in (scartati if cartella is None else tenuti) if s in dest["simboli"]]
    for s in via:
        for k in _sue(dest, s):
            dest["tessere"].pop(k, None)
            (USCITA / f"{k}.webp").unlink(missing_ok=True)
        del dest["simboli"][s]
    if cartella is not None:
        USCITA.mkdir(exist_ok=True)
        for s in tenuti:
            for k in _sue(ind_s, s):
                shutil.copyfile(cartella / f"{k}.webp", USCITA / f"{k}.webp")
                dest["tessere"][k] = ind_s["tessere"][k]
            dest["simboli"][s] = list(ind_s["simboli"][s])
    dest["orientabili"] = sorted(k for k in dest.get("orientabili", [])
                                 if k in dest["tessere"] and k + SUFFISSO_NS in dest["tessere"])
    dest["tessere"] = dict(sorted(dest["tessere"].items()))
    INDICE.write_text(json.dumps(dest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for s in tenuti:
        print(f"✓ {s}: tessera adottata")
    for s, errori in scartati.items():
        print(f"○ {s}: resta il glifo — {errori[0]}")
    nuove = [(s, k) for s in tenuti for k in ind_s["simboli"][s]
             if ind_s["tessere"][k].get("fonte") == "ComfyUI"]
    if nuove:
        print("\nAggiungi a GENERATE in build_oggetti_cc0.py (o incolla queste righe nella chat):")
        for s, k in nuove:
            print(f'    ("{s}", "{k}"),')
    rifare = [s for s in da_rifare() if s in ind_s.get("simboli", {})]
    if rifare:
        print(f"\nDa rifare, perché nessuna andava bene: {' '.join(rifare)}. Una nuova immagine "
              "(comfyui_batch.py --solo …) o un altro modello CC0, poi misura_resa.py coppie di nuovo.")
    print("\nPoi: python3 scripts/dm.py maps texture && python3 scripts/build_oggetti_cc0.py --check")
    return 0


def fonte_di(cartella: Path, simbolo: str) -> str:
    """La fonte di un simbolo in una cartella di tessere, come la scrive la
    pagina di scelta e come la cerca `adotta`: quella dichiarata dalle sue
    tessere (Poly Haven, Quaternius, ComfyUI), o il nome della cartella se non
    la dichiarano. Non dipende dalla cartella quando c'è: una tessera ComfyUI
    adottata in `scripts/oggetti-cc0/` resta ComfyUI."""
    try:
        ind = json.loads((cartella / "indice.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        ind = {}
    fonti = {ind.get("tessere", {}).get(k, {}).get("fonte") for k in ind.get("simboli", {}).get(simbolo, [])}
    fonti.discard(None)
    return " + ".join(sorted(fonti)) if fonti else cartella.resolve().name


def approvazioni(indice: dict, fonte: str | None = None) -> list[str]:
    """D23: una tessera sostituisce un glifo solo se la misura non la boccia
    (`misura_resa.py candidati --registra`) e il DM l'ha preferita al glifo nel
    confronto (`misura_resa.py coppie`, `voti`), in ogni ambiente provato. Con
    `fonte`, la tessera preferita dev'essere proprio di quella fonte: chi ha
    scelto ComfyUI non ha approvato la tessera CC0 dello stesso simbolo."""
    scheda = json.loads(SCHEDA_RESA.read_text(encoding="utf-8")) if SCHEDA_RESA.exists() else {}
    verdetti, pref = scheda.get("candidati", {}), scheda.get("preferenze_dm", {})
    errori = []

    def presa(x: str) -> bool:
        return x == "tessera" or (x.startswith("tessera:") and (fonte is None or x == f"tessera:{fonte}"))
    for s in indice.get("simboli", {}):
        v, d = verdetti.get(s, {}), pref.get(s, {})
        if not v:
            errori.append(f"{s}: nessuna misura contro il glifo (misura_resa.py candidati DIR --registra)")
        elif any(x == "perde" for x in v.values()):
            errori.append(f"{s}: la misura la boccia contro il glifo ({v})")
        if not d:
            errori.append(f"{s}: il DM non l'ha ancora confrontata (misura_resa.py coppie, voti)")
        elif any(x == "nessuna" for x in d.values()):
            errori.append(f"{s}: per il DM nessuna va bene ({d}): la tessera si butta; rifalla "
                          "(comfyui_batch.py) o cercane un'altra, poi un nuovo confronto")
        elif any(x == "uguali" for x in d.values()):
            errori.append(f"{s}: il DM non vede differenze ({d}): resta il glifo, che costa meno")
        elif not all(presa(x) for x in d.values()):
            chi = "il glifo" if "glifo" in d.values() else "la tessera di un'altra fonte"
            errori.append(f"{s}: il DM ha preferito {chi} ({d})")
    return errori


def da_rifare() -> list[str]:
    """I simboli per cui il DM ha detto «nessuna va bene»: si butta l'immagine e si rifà."""
    scheda = json.loads(SCHEDA_RESA.read_text(encoding="utf-8")) if SCHEDA_RESA.exists() else {}
    return sorted(s for s, d in scheda.get("preferenze_dm", {}).items() if "nessuna" in d.values())


def misura_stile(cartella: Path | None = None) -> dict[str, dict]:
    """Per tessera: luminanza media, contrasto (deviazione della luminanza),
    saturazione media e dettaglio (gradiente medio), sui soli pixel opachi.
    Il fotografico di Poly Haven e il low-poly di Quaternius si confrontano qui."""
    Image = _pillow()
    if Image is None:
        return {}
    cartella = cartella or USCITA
    indice = json.loads((cartella / "indice.json").read_text(encoding="utf-8"))
    out = {}
    for k, voce in indice.get("tessere", {}).items():
        im = Image.open(cartella / f"{k}.webp").convert("RGBA")
        w, h = im.size
        px = im.load()
        lum, sat, grad = [], [], []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a < 200:
                    continue
                L = 0.2126 * r + 0.7152 * g + 0.0722 * b
                mx, mn = max(r, g, b), min(r, g, b)
                lum.append(L)
                sat.append(0 if mx == 0 else (mx - mn) / mx)
                if x + 1 < w and y + 1 < h and px[x + 1, y][3] >= 200 and px[x, y + 1][3] >= 200:
                    r2, g2, b2, _ = px[x + 1, y]
                    r3, g3, b3, _ = px[x, y + 1]
                    L2 = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
                    L3 = 0.2126 * r3 + 0.7152 * g3 + 0.0722 * b3
                    grad.append(abs(L2 - L) + abs(L3 - L))
        n = len(lum) or 1
        media = sum(lum) / n
        out[k] = {"fonte": voce["fonte"], "copertura": round(len(lum) / (w * h), 3),
                  "luminanza": round(media, 1),
                  "contrasto": round((sum((v - media) ** 2 for v in lum) / n) ** 0.5, 1),
                  "saturazione": round(sum(sat) / n, 3),
                  "dettaglio": round(sum(grad) / (len(grad) or 1), 2)}
    return out


def stampa_stile() -> int:
    if not INDICE.exists():
        print("○ nessuna tessera da misurare")
        return 0
    misure = misura_stile()
    print(f"{'tessera':32} {'fonte':11} {'cop.':>5} {'lum.':>6} {'contr.':>6} {'sat.':>6} {'dett.':>6}")
    for k, m in misure.items():
        print(f"{k:32} {m['fonte']:11} {m['copertura']:5} {m['luminanza']:6} "
              f"{m['contrasto']:6} {m['saturazione']:6} {m['dettaglio']:6}")
    for fonte in sorted({m["fonte"] for m in misure.values()}):
        gruppo = [m for m in misure.values() if m["fonte"] == fonte]
        medie = {c: round(sum(m[c] for m in gruppo) / len(gruppo), 3)
                 for c in ("luminanza", "contrasto", "saturazione", "dettaglio")}
        print(f"media {fonte}: {medie}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true",
                   help="niente rete: le tessere combaciano con l'indice e vengono da modelli verificati")
    g.add_argument("--elenca-quaternius", type=Path, metavar="ZIP",
                   help="impronta, licenza e modelli glTF dello zip Standard di Quaternius")
    g.add_argument("--misura-stile", action="store_true",
                   help="luminanza, contrasto, saturazione e dettaglio delle tessere, per fonte")
    g.add_argument("--scarica-solo", action="store_true",
                   help="scarica e verifica i modelli di Poly Haven, senza rendere")
    g.add_argument("--rendi", action="store_true",
                   help="rende dai modelli già in asset-esterni/oggetti-cc0/, senza rete")
    ap.add_argument("--prova", action="store_true", help="solo i modelli del giro di prova (PILOTA)")
    ap.add_argument("--quaternius", type=Path, metavar="ZIP",
                    help="lo zip Fantasy Props MegaKit [Standard]: estrae i modelli della tabella")
    ap.add_argument("--blender", help="il comando di Blender, se non è nel PATH")
    g.add_argument("--da-immagini", type=Path, metavar="DIR",
                   help="le PNG di comfyui_batch.py in tessere candidate (con --variante e -o)")
    g.add_argument("--adotta", nargs="?", const=True, type=Path, metavar="DIR",
                   help="dopo i voti: tiene solo le tessere preferite al glifo; con DIR copia "
                        "dentro le candidate approvate (per esempio di --da-immagini)")
    ap.add_argument("--variante", default="a", help="--da-immagini: quale dei quattro semi (a-d)")
    ap.add_argument("-o", "--uscita", type=Path, help="--da-immagini: la cartella dei candidati")
    args = ap.parse_args(argv)
    if args.check:
        return controlla()
    if args.elenca_quaternius:
        return elenca_quaternius(args.elenca_quaternius)
    if args.misura_stile:
        return stampa_stile()
    if args.adotta:
        return adotta(None if args.adotta is True else args.adotta)
    if args.da_immagini:
        Image = _pillow()
        if Image is None:
            return 2
        if not args.uscita:
            ap.error("--da-immagini vuole -o <cartella dei candidati>")
        return da_immagini(args.da_immagini, args.variante, args.uscita, Image)
    return costruisci(args)


if __name__ == "__main__":
    sys.exit(main())
