#!/usr/bin/env python3
"""verifica.py [CARTELLA] — controlla i risultati di un giorno di prove sulla RTX 4050 (ADR-0136).

Legge `prove.json` (cosa aspetta ogni prova) e la cartella dei risultati
(di serie ~/rumblingstone-prove-4050/<oggi>, o una cartella estratta dall'archivio di
riporta.sh) e scrive `verifica.json` e `verifica.md` accanto ai risultati.

Per ogni prova lo stato è uno di:
  ok             i file ci sono e i numeri tornano
  ko             la prova è partita ma qualcosa non torna (detto in «note»)
  da completare  manca un passo a mano (il foglio alla cieca della prosa)
  non fatta      nessun risultato

«ok» vuol dire che la prova è girata come doveva, non che la tecnica migliora: il verdetto
lo dà il thread della prova con la sua regola. Esce con 1 se almeno una prova è «ko».
Solo libreria standard: gira sull'host, nel container e su WSL2.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
VRAM_MIB = 6144  # la RTX 4050 del portatile
# FLEURS it_it/dev, 40 righe, large-v3-turbo-q8_0, -mc 0, senza VAD: 2,3% sulla CPU del container
# (MISURE.md della #424). Sulla GPU il testo dovrebbe essere lo stesso: un punto di tolleranza.
WER_SOGLIA = 0.023
WER_TOLLERANZA = 0.01
# Il modello q8_0 pesa ~870 MB: se la memoria della NVIDIA sale meno di così mentre whisper gira,
# ha lavorato un'altra scheda (quella integrata, con Vulkan) o la CPU.
VRAM_WHISPER_MIB = 400


def leggi_esito(cartella: Path) -> dict:
    f = cartella / "esito.txt"
    if not f.exists():
        return {}
    out = {}
    for riga in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if ": " in riga:
            k, v = riga.split(": ", 1)
            out[k.strip()] = v.strip()
    return out


def leggi_json(f: Path):
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def vram_usata(cartella: Path) -> list[tuple[int, int]]:
    """(MiB usati, MiB totali) in ogni foto di gpu.txt (righe CSV di nvidia-smi)."""
    f = cartella / "gpu.txt"
    if not f.exists():
        return []
    return [(int(m.group(1)), int(m.group(2))) for m in
            re.finditer(r",\s*(\d+)\s*MiB,\s*(\d+)\s*MiB", f.read_text(encoding="utf-8", errors="replace"))]


# --- i controlli, uno per prova ----------------------------------------------------------

def c_controlla(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    testo = (c / "macchina.txt").read_text(encoding="utf-8", errors="replace")
    note = [" ".join(r.split()) for r in testo.splitlines() if r.startswith("✗")]
    gpu = next((r for r in testo.splitlines() if " GPU " in f" {r} "), "")
    return ("ko" if note else "ok"), note, {"gpu": gpu[4:].strip()}


def c_lettore(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    note, numeri = [], {}
    risposte = sorted(c.glob("risposte-*.json"))
    if not risposte:
        return "ko", ["nessun risposte-*.json"], numeri
    r = leggi_json(risposte[-1]) or {}
    attese = int(esito.get("domande", "0") or 0)
    numeri.update(risposte=len(r), domande=attese, minuti=esito.get("minuti"))
    if attese and len(r) < attese:
        note.append(f"risposte {len(r)} su {attese}: corsa interrotta, rilanciala (riparte da dove era)")
    ps = leggi_json(c / "ollama-ps.json") or {}
    for m in ps.get("models", []):
        numeri["in_vram"] = round(m.get("size_vram", 0) / max(m.get("size", 1), 1), 2)
        if numeri["in_vram"] < 1:
            note.append(f"solo il {numeri['in_vram']:.0%} del modello in VRAM: il tempo vale con quella riserva")
    return ("ko" if attese and len(r) < attese else "ok"), note, numeri


def c_schede(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    m = leggi_json(c / "misure.json")
    if not m or "sintesi" not in m:
        return "ko", ["misure.json manca o è rotto"], {}
    s = m["sintesi"]
    attese = int(s.get("schede", 0)) * int(s.get("ripetizioni", 0))
    note = []
    numeri = {"migliora_secondo_la_regola": s.get("migliora")}
    for b in ("libero", "vincolato"):
        x = s.get(b, {})
        numeri[b] = {k: x.get(k) for k in ("risposte", "valide", "s8_per_scheda", "token_al_secondo")}
        if attese and x.get("risposte", 0) < attese:
            note.append(f"{b}: {x.get('risposte', 0)} risposte su {attese}")
    return ("ko" if note else "ok"), note, numeri


def c_trascrizione(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    note = []
    disp = (c / "dispositivo.txt").read_text(encoding="utf-8", errors="replace")
    grezza = (c / "grezza.txt").read_text(encoding="utf-8", errors="replace").strip()
    backend = esito.get("backend", "?")
    numeri = {"backend": backend, "secondi": esito.get("secondi"),
              "volte_tempo_reale": esito.get("volte_tempo_reale"),
              "dispositivo": disp.splitlines()[0] if disp.strip() else ""}
    misura = c / "misura.txt"
    if misura.exists():
        testo = misura.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'"wer":\s*([0-9.]+)', testo)
        if m:
            numeri["wer"] = float(m.group(1))
            if numeri["wer"] > WER_SOGLIA + WER_TOLLERANZA:
                note.append(f"parole sbagliate {numeri['wer']:.1%}: sopra il {WER_SOGLIA:.1%} della CPU del "
                            "container (più un punto): la GPU non dà lo stesso testo")
        else:
            numeri["misura"] = testo.strip()[:300]
    if not grezza:
        note.append("trascrizione vuota: vedi whisper.log")
    sulla_gpu = bool(re.search(r"nvidia|geforce|rtx", disp, re.I))
    numeri["sulla_gpu"] = sulla_gpu
    if backend != "cpu" and not sulla_gpu:
        note.append("whisper-cli non mostra la scheda NVIDIA: è andato sulla CPU")
    prima, picco = esito.get("vram_prima_mib", ""), esito.get("vram_picco_mib", "")
    if prima.isdigit() and picco.isdigit():
        numeri["vram_salita_mib"] = int(picco) - int(prima)
        if backend != "cpu" and numeri["vram_salita_mib"] < VRAM_WHISPER_MIB:
            note.append(f"la memoria della NVIDIA è salita di {numeri['vram_salita_mib']} MiB mentre whisper "
                        "girava: ha lavorato un'altra scheda (quella integrata?) o la CPU")
    return ("ko" if note else "ok"), note, numeri


def c_drappo(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    r = leggi_json(c / "riepilogo.json")
    if not r:
        return "ko", ["riepilogo.json manca o è rotto"], {}
    imm = r.get("immagini", [])
    attese = len([t for t in esito.get("tavole", "").split(",") if t]) * int(esito.get("semi", "0") or 0)
    fatte = [i for i in imm if i.get("esito") == "ok"]
    vram = max((i.get("vram_picco_mib") or 0 for i in imm), default=0)
    ram = max((i.get("ram_comfyui_picco_mib") or 0 for i in imm), default=0)
    numeri = {"fatte": len(fatte), "attese": attese, "vram_picco_mib": vram, "ram_picco_mib": ram,
              "minuti": r.get("minuti_totali"), "cpu": r.get("cpu")}
    note = []
    if attese and len(fatte) < attese:
        note.append(f"tavole fatte {len(fatte)} su {attese}")
    if r.get("cpu"):
        note.append("girata sulla CPU, non sulla GPU")
    for i in fatte:
        if i.get("file") and not (c / i["file"]).exists():
            note.append(f"manca {i['file']} (riporta.sh lo tiene se è sotto gli 8 MB)")
    if vram and vram < 1024:
        note.append(f"picco di VRAM {vram} MiB: la GPU non sembra usata")
    return ("ko" if note else "ok"), note, numeri


def c_immagini(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    r = leggi_json(c / "riepilogo.json")
    if not r:
        return "ko", ["riepilogo.json manca o è rotto"], {}
    scene = r.get("scene", [])
    note = []
    for s in scene:
        if not list((c / s["scena"]).glob("**/5_finale.png")):
            note.append(f"{s['scena']}: nessun 5_finale.png ({str(s.get('esito'))[:120]})")
    numeri = {"scene": len(scene), "secondi_totali": r.get("secondi_totali"),
              "giudice": esito.get("giudice"), "comfyui": esito.get("comfyui")}
    if not scene:
        note.append("nessuna scena nel riepilogo")
    return ("ko" if note else "ok"), note, numeri


def c_prosa(c: Path, esito: dict) -> tuple[str, list[str], dict]:
    corse = [p for p in c.iterdir() if p.is_dir() and p.name.startswith("L-") and "tempi" not in p.name]
    fogli = sorted(c.glob("foglio-*.md"))
    numeri = {"modello": esito.get("modello"), "minuti": esito.get("minuti"), "corse": len(corse)}
    if not corse:
        return "ko", ["nessuna corsa dei dieci casi (fermata dopo il primo?)"], numeri
    if not fogli:
        return "da completare", ["manca il foglio alla cieca"], numeri
    testo = fogli[-1].read_text(encoding="utf-8", errors="replace")
    tutti = re.findall(r"Preferito:\s*(\S*)", testo)
    votati = [v for v in tutti if v in ("1", "2", "=")]
    numeri.update(voti=len(votati), coppie=len(tutti))
    if len(votati) < len(tutti):
        return "da completare", [f"foglio alla cieca: {len(votati)} voti su {len(tutti)}"], numeri
    return "ok", [], numeri


CONTROLLI = {"controlla": c_controlla, "lettore-coerenza": c_lettore, "schede-vincolate": c_schede,
             "trascrizione-gpu": c_trascrizione, "drappo-flux": c_drappo, "immagini": c_immagini,
             "prosa": c_prosa}


def codici_del_kit(ris: Path) -> dict:
    """Le uscite registrate da kit.sh in kit.tsv: id → (codice, minuti)."""
    f = ris / "kit.tsv"
    out = {}
    if f.exists():
        for riga in f.read_text(encoding="utf-8").splitlines():
            parti = riga.split("\t")
            if len(parti) >= 3:
                out[parti[0]] = {"codice": int(parti[1]), "minuti": int(parti[2])}
    return out


def verifica(ris: Path, manifesto: dict) -> dict:
    kit = codici_del_kit(ris)
    esiti = {}
    for p in manifesto["prove"]:
        c = ris / p["uscita"]
        mancano = [f for f in p["file_attesi"] if not (c / f).exists()]
        voce = {"thread": p["thread"], "kit": kit.get(p["id"])}
        if not c.exists() or (p["id"] != "controlla" and not (c / "esito.txt").exists()) \
                or (p["id"] == "controlla" and not (c / "macchina.txt").exists()):
            # kit.sh l'ha lanciata ma non ha lasciato risultati (server spento, box assente...):
            # non è «non fatta», è fallita prima di cominciare
            if voce["kit"] and voce["kit"]["codice"] != 0:
                voce.update(stato="ko", numeri={},
                            note=[f"non è partita: lo script è uscito con {voce['kit']['codice']} senza risultati"])
            else:
                voce.update(stato="non fatta", note=[], numeri={})
        elif mancano and p["id"] != "prosa":
            voce.update(stato="ko", note=[f"mancano: {', '.join(mancano)}"], numeri={})
        else:
            esito = leggi_esito(c)
            try:
                stato, note, numeri = CONTROLLI[p["id"]](c, esito)
            except (OSError, ValueError, KeyError, TypeError) as e:
                stato, note, numeri = "ko", [f"risultati illeggibili: {type(e).__name__}: {e}"], {}
            vram = vram_usata(c)
            if vram:
                numeri["vram_mib_foto"] = [u for u, _ in vram]
                if max(tot for _, tot in vram) > VRAM_MIB + 100:
                    note.append(f"la GPU ha più di {VRAM_MIB} MiB: non è la 4050, i tempi non valgono per lei")
            if voce["kit"] and voce["kit"]["codice"] != 0 and stato == "ok":
                stato = "ko"
                note.append(f"lo script è uscito con {voce['kit']['codice']}")
            voce.update(stato=stato, note=note, numeri=numeri)
        esiti[p["id"]] = voce
    return esiti


def scrivi_md(esiti: dict, ris: Path) -> str:
    righe = [f"# Verifica delle prove 4050 · {ris.name}", "",
             "| Prova | Stato | Note | Thread |", "|---|---|---|---|"]
    for k, v in esiti.items():
        note = "; ".join(v["note"]) or "·"
        righe.append(f"| {k} | {v['stato']} | {note} | {v['thread']} |")
    righe += ["", "«ok» = la prova è girata come doveva; il verdetto sulla tecnica lo dà il suo thread.", ""]
    return "\n".join(righe)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    radice = Path(os.environ.get("PROVE_DIR", Path.home() / "rumblingstone-prove-4050"))
    ap.add_argument("cartella", nargs="?", type=Path, default=radice / dt.date.today().isoformat())
    ap.add_argument("--manifesto", type=Path, default=QUI / "prove.json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if not a.cartella.is_dir():
        print(f"ERRORE: nessuna cartella {a.cartella}", file=sys.stderr)
        return 2
    esiti = verifica(a.cartella, json.loads(a.manifesto.read_text(encoding="utf-8")))
    (a.cartella / "verifica.json").write_text(json.dumps(esiti, indent=1, ensure_ascii=False) + "\n",
                                              encoding="utf-8")
    md = scrivi_md(esiti, a.cartella)
    (a.cartella / "verifica.md").write_text(md, encoding="utf-8")
    if not a.quiet:
        print(md)
    return 1 if any(v["stato"] == "ko" for v in esiti.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
