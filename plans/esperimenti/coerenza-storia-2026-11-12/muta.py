#!/usr/bin/env python3
"""muta.py — banco di mutanti per verifica_storia.py e per i cancelli che ci sono già.

Ogni mutante inserisce UNA riga falsa contro state.yaml in un file vero di una
copia del repo, poi chiede a tre strumenti se la vedono:
  - verifica_storia.py (il prototipo, àncora su state.yaml)
  - coerenza_campagna.py fatti (prosa contro prosa, il cancello di oggi)
  - validate_state.py (lo schema e le regole R1-R13 di state.yaml)

Metà dei mutanti di ogni regola è scritta «come la scriverebbe uno script»
(forma piana), metà «come la scriverebbe un autore» (parafrasi: numeri in
lettere, soggetto in un'altra frase, sinonimi). La seconda metà misura il
limite vero: estrarre il fatto dalla prosa.

Uso: python3 muta.py OUT.json   (copia il repo in una cartella temporanea)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[2]
A7 = "07_il Portale Della Forgia Eterna"
A8 = "08_La Battaglia Di Hammerfist"
A9 = "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
F9 = f"{A9}/Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md"
F9b = f"{A9}/Arco-Post-Hammerfist-P2A-Torre-PARTE1.md"
F8 = f"{A8}/ARC08-01-GUIDA-DM.md"
F7 = f"{A7}/ARC07-DEF-5-RITORNO-HAMMERFIST.md"
FC = "campaign/DM-QUICKSTART-ARC09.md"

# (id, regola, forma, file, riga da inserire)
MUTANTI = [
    ("S1-p1", "S1", "piana", F9, "- Day 39: l'orda della Mano Rossa arriva a Rethmar e si accampa."),
    ("S1-p2", "S1", "piana", FC, "L'armata di Azarr Kul giunge sotto Rethmar al Giorno 44."),
    ("S1-p3", "S1", "piana", F9b, "**Arrivo dell'orda a Rethmar:** Giorno 38."),
    ("S1-a1", "S1", "parafrasi", F9, "Quaranta giorni dopo la partenza dal Fane, le tende hobgoblin coprono la piana sotto Rethmar."),
    ("S1-a2", "S1", "parafrasi", FC, "Le mura di Rethmar vedranno le insegne della Mano Rossa il trentottesimo giorno di marcia."),
    ("S1-a3", "S1", "parafrasi", F9b, "Il Day 40 è quello dell'assalto: l'orda è lì da una notte sola."),
    ("S2-p1", "S2", "piana", F9, "- Day 15: Terrelton cade."),
    ("S2-p2", "S2", "piana", FC, "Il ponte di Skull Gorge viene attraversato al Giorno 4."),
    ("S2-p3", "S2", "piana", F8, "Drellin's Ferry brucia il Giorno 10, mentre i nani si preparano."),
    ("S2-a1", "S2", "parafrasi", F9, "Terrelton resiste fino al ventiduesimo giorno, poi apre le porte."),
    ("S2-a2", "S2", "parafrasi", FC, "La gola del ponte la passano il sesto giorno, senza che nessuno la difenda."),
    ("S2-a3", "S2", "parafrasi", F8, "Quando il traghetto di Drellin brucia sono passati dieci giorni dal Fane."),
    ("S3-p1", "S3", "piana", F9, "- Torneo di Dauth: Day 20-22."),
    ("S3-p2", "S3", "piana", FC, "La Torre Invisibile si affronta nei Giorni 22-24."),
    ("S3-p3", "S3", "piana", F9b, "Il raid a Rhest va giocato al Day 36."),
    ("S3-a1", "S3", "parafrasi", F9, "Il torneo comincia tre giorni dopo la Cerimonia delle 100 Asce."),
    ("S3-a2", "S3", "parafrasi", FC, "I campioni si sfidano a Dauth fra il ventesimo e il ventiduesimo giorno."),
    ("S3-a3", "S3", "parafrasi", F9b, "Zalkatar va raggiunto prima che finisca la terza settimana di marcia."),
    ("S4-p1", "S4", "piana", F9b, "Pensato per un party di livello 10."),
    ("S4-p2", "S4", "piana", F8, "I PG di livello 16 affrontano qui l'ondata finale."),
    ("S4-p3", "S4", "piana", F7, "Scontro calibrato per 4 PG di livello 11."),
    ("S4-a1", "S4", "parafrasi", F9b, "Gli eroi, ormai al decimo livello, entrano nella Torre."),
    ("S4-a2", "S4", "parafrasi", F8, "Quattro personaggi di sedicesimo reggono l'ondata senza i pregen."),
    ("S4-a3", "S4", "parafrasi", F7, "EL 13 per un gruppo di 11°."),
    ("S5-p1", "S5", "piana", F9, "Hella impugna Aegis Fang contro il drago."),
    ("S5-p2", "S5", "piana", FC, "La Corona di Adamantio di Tordek brilla nella sala."),
    ("S5-p3", "S5", "piana", F7, "Artemis indossa la Collana dei Semi Eterni."),
    ("S5-a1", "S5", "parafrasi", F9, "L'ascia di Thorik ora la porta Tordek, che la stringe senza saperla usare."),
    ("S5-a2", "S5", "parafrasi", FC, "Sulla testa di Artemis la Corona pesa come un debito."),
    ("S5-a3", "S5", "parafrasi", F7, "L'anello caotico è passato al dito di Hella."),
    ("S6-p1", "S6", "piana", F7, "Thorik paga −2 COS permanente."),
    ("S6-p2", "S6", "piana", F9, "Tordek ha −2 DES permanenti dal rito."),
    ("S6-p3", "S6", "piana", FC, "Thorik: −2 SAG permanente dalla Corona."),
    ("S6-a1", "S6", "parafrasi", F7, "Il rito toglie a Thorik due punti di Costituzione per sempre."),
    ("S6-a2", "S6", "parafrasi", F9, "Tordek ne esce più lento: perde due punti di Destrezza, e non li riavrà."),
    ("S6-a3", "S6", "parafrasi", FC, "Thorik porta il segno del rito: la sua Saggezza scende di 2, definitivamente."),
]


def gira(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)


def main(out: Path) -> int:
    tmp = Path(tempfile.mkdtemp(prefix="muta-storia-"))
    for d in (A7, A8, A9, "campaign", "scripts", "Bestiario", "sistemi"):
        shutil.copytree(REPO / d, tmp / d, symlinks=True)
    shutil.copy(REPO / "sistemi.toml", tmp / "sistemi.toml")
    (tmp / "plans/esperimenti/coerenza-storia-2026-11-12").mkdir(parents=True)
    shutil.copy(QUI / "verifica_storia.py", tmp / "plans/esperimenti/coerenza-storia-2026-11-12/")
    vs = tmp / "plans/esperimenti/coerenza-storia-2026-11-12/verifica_storia.py"
    # base: cosa vedono già gli strumenti sulla copia pulita
    def fatti_set(arco):
        r = gira([sys.executable, "scripts/coerenza_campagna.py", "fatti", arco, "--json"], tmp)
        d = json.loads(r.stdout)
        return {(o["file"], o["riga"]) for c in d["contraddizioni"] for v in c["valori"] for o in v["occorrenze"]}
    def storia_set(arco):
        r = gira([sys.executable, str(vs), "--radice", str(tmp), "--archi", arco, "--json"], tmp)
        d = json.loads(r.stdout)
        return {(x["file"], x["riga"]): x for x in d["violazioni"]}
    base_fatti = {a: fatti_set(a) for a in (A7, A8, A9, "campaign")}
    esiti = []
    for mid, regola, forma, rel, riga in MUTANTI:
        p = tmp / rel
        orig = p.read_text(encoding="utf-8")
        righe = orig.splitlines()
        # dopo la prima riga vuota dopo il titolo, fuori da blocchi di codice
        pos = next((i for i in range(5, len(righe)) if righe[i].strip() == "" and not
                    sum(1 for r in righe[:i] if r.lstrip().startswith("```")) % 2), len(righe))
        nuove = righe[:pos + 1] + [riga, ""] + righe[pos + 1:]
        p.write_text("\n".join(nuove) + "\n", encoding="utf-8")
        n = pos + 2
        arco = rel.split("/")[0]
        vs_hit = storia_set(arco).get((rel, n))
        f_hit = (rel, n) in (fatti_set(arco) - base_fatti[arco])
        # validate_state legge solo state.yaml: per un mutante di prosa è cieco per costruzione
        esiti.append({"id": mid, "regola": regola, "forma": forma, "file": rel, "riga": n, "testo": riga,
                      "verifica_storia": bool(vs_hit), "dettaglio": vs_hit,
                      "coerenza_campagna": f_hit, "validate_state": False})
        p.write_text(orig, encoding="utf-8")
        print(f"{mid:7} vs={'✓' if vs_hit else '·'} cc={'✓' if f_hit else '·'}  {riga[:70]}", flush=True)
    # S7: un'eco armata nuova senza scena
    st = tmp / "campaign/state.yaml"
    orig = st.read_text(encoding="utf-8")
    st.write_text(orig.replace("villain:\n", "- id: E-99z\n  data: '2026-11-12'\n  autore: Tordek\n"
                               "  fatto: mutante\n  tono: grigio\n  miccia: lunga (ARC-09)\n"
                               "  payoff: mutante\n  stato: armato\n  tag: 🔫 armato\nvillain:\n", 1), encoding="utf-8")
    r = gira([sys.executable, str(vs), "--radice", str(tmp), "--json"], tmp)
    d = json.loads(r.stdout)
    hit = any("E-99z" in x["atteso"] for x in d["violazioni"])
    rv = gira([sys.executable, "scripts/validate_state.py"], tmp)
    esiti.append({"id": "S7-p1", "regola": "S7", "forma": "piana", "file": "campaign/state.yaml", "riga": 0,
                  "testo": "eco E-99z armata senza scena", "verifica_storia": hit, "dettaglio": None,
                  "coerenza_campagna": False, "validate_state": rv.returncode != 0})
    st.write_text(orig, encoding="utf-8")
    out.write_text(json.dumps(esiti, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp)
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
