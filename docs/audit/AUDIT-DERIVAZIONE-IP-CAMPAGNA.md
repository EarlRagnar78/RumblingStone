<!-- Audit di derivazione IP — misura, non parere legale. plans/CHANGELOG registra la modifica strutturale. -->
# Audit della derivazione IP nel testo di campagna

**Data:** 2026-09-11 · **Ambito:** tutto il testo di campagna del repo (`.md`, esclusi
`rendered/`, `homebrew/`, `_ARCHIVIO/`) · **Metodo:** conteggio di termini propri per
arco, normalizzato per 1.000 parole.

> **Perché esiste.** L'ADR ex-0018 della PR #72 poggiava su questo audit, e
> **l'audit non era nel repo**: il perimetro di prodotto che proponeva era
> un'asserzione senza prova. Rifatto da zero il 2026-09-11 sul testo di oggi, per
> rendere decidibile **D11**.
>
> ⚠️ **Non è un parere legale.** Misura quante volte il testo *nomina* cose di
> altri. La somiglianza sostanziale dell'espressione protetta — sequenza degli
> eventi, personaggi distintivi, ambientazioni specifiche — **non si conta**, e
> resta materia da avvocato (ADR-0005).

---

## 1. Cosa si è contato, e da dove

Le fonti non sono state indovinate: le **dichiara il repo**, in
`campaign/lore/campaign-history.md`, con i numeri di pagina.

| Famiglia | Termini contati |
|---|---|
| **RHoD** | Red Hand · Mano Rossa · Drellin · Brindol · Elsir · Wyrmlord · Azarr Kul · Ghostlord · Kulkor · Rhest · Vraath · Skull Gorge · Gola del Teschio · Dawn Way · Via dell'Alba · Saarvith · Ulwai · Hravek · Koth |
| **Undermountain** | Undermountain · Belkram |
| **Underdark (manuale)** | Maur · Cristal/Crystal Warrior |
| **Out of the Abyss** | Neverlight · Out of the Abyss |

Il comando che produce la tabella è in [§5](#5-il-comando-che-rifà-la-misura):
la quarta regola di [ADR-0045](../../plans/adr/ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md)
chiede che un lavoro su un insieme dichiari come lo conta.

---

## 2. La misura

Fra parentesi: occorrenze **per 1.000 parole**.

| Ambito | Parole | RHoD | Undermountain | Underdark | Out of the Abyss |
|---|---:|---:|---:|---:|---:|
| `00_Red Hand Of Doom` | 7.886 | 167 (**21,2**) | 10 (1,3) | 0 | 0 |
| `01`–`03`, `05` | **0** | — | — | — | — |
| `04_tomba_di_Belkram` | 2.838 | 0 (0,0) | 0 (0,0) | 0 | 0 |
| `06_Stanza-corona-di-adamantio` | 37.375 | 0 (0,0) | 144 (**3,9**) | 0 | 0 |
| `07_il Portale Della Forgia Eterna` | 128.318 | 23 (**0,2**) | 33 (0,3) | 0 | 0 |
| `08_La Battaglia Di Hammerfist` | 127.406 | 90 (**0,7**) | 0 (0,0) | 0 | 0 |
| `09_Continuazione…Hammerfist` | 178.338 | 1.004 (**5,6**) | 5 (0,0) | 0 | 0 |
| `10-stand-alone` | 21.986 | 0 (**0,0**) | 0 | 0 | 0 |
| `campaign/` | 95.117 | 725 (**7,6**) | 60 (0,6) | 15 (0,2) | 6 (0,1) |
| `Bestiario/` | 74.978 | 225 (**3,0**) | 17 (0,2) | 0 | 0 |
| `PG/` | 63.494 | 1 (0,0) | 0 | 0 | 0 |
| `STANDALONE-Il-Drappo-di-Tarsilia` | 63.870 | 3 (**0,0**) | 0 | 0 | 0 |
| **totale** | **801.606** | | | | |

---

## 3. Cosa conferma, e cosa cambia

**La tesi di ex-0018 regge, misurata di nuovo e su un repo cresciuto.** La
derivazione da RHoD **non è distribuita: è concentrata.**

| | ex-0018 (lug 2026) | oggi | |
|---|---|---|---|
| arco 00 | 20,2 | **21,2** | ✅ confermato — è impalcatura, non contenuto |
| arco 07 | 0,3 su 151.588 parole | **0,2** su 128.318 | ✅ confermato |
| arco 08 | 1,1 su 81.422 | **0,7** su 127.406 | l'arco è **cresciuto del 56%** e la densità è **scesa** |
| arco 09 | 5,3 su 195.739 | **5,6** su 178.338 | ✅ confermato — ed è **voluto** (`PIANO-REINTEGRAZIONE-PNG-AP-RHOD`, chiuso il 2026-07-20) |
| arco 06 · Undermountain | 8,8 | **3,9** | dimezzata, ma resta **la più alta del repo** per quella fonte |

**Due cose che ex-0018 non aveva misurato**, e che cambiano il perimetro:

1. 🔴 **`Bestiario/` è a 3,0** (225 occorrenze su 74.978 parole). L'ADR metteva
   `campaign/` fuori dal prodotto — giustamente, è il diario del tavolo, ed è
   infatti il corpo più denso di tutti (**7,6**) — ma il **bestiario esce col
   modulo**. Un perimetro che dice «archi 07+08 dentro» e tace sul bestiario
   lascia fuori il conto una dipendenza reale.
2. ✅ **I moduli autoconclusivi sono già puliti**: `10-stand-alone` a **0,0** e il
   Drappo a **0,0** (3 occorrenze in 63.870 parole). È il corpo grande più pulito
   del repo, e la cosa merita di essere detta perché `PIANO-VENDIBILITA` mette il
   Drappo alla linea 3 dei prodotti: **su quest'asse è già pronto**.

---

## 4. Cosa questa misura **non** dice

- **Non misura la somiglianza sostanziale.** Un testo che non nomina mai Brindol
  ma ne ricalca la sequenza degli eventi qui risulta a 0,0. È il limite che rende
  necessario l'avvocato, e nessun conteggio lo toglie.
- **Non distingue la citazione dall'uso.** Una riga che dice *«adattato da
  Undermountain p.165»* conta come un'occorrenza esattamente come un toponimo
  usato in narrazione — anzi, la prima è **buona pratica** (ADR-0033) e viene
  contata come se fosse debito.
- **Non guarda le immagini**, i nomi di mostri SRD, né le meccaniche. Il bestiario
  non-SRD ha già la sua misura in `PIANO-VENDIBILITA` §2 (~220 occorrenze).
- **Non è un gate.** Nessuno la ricontrolla: è una fotografia, e invecchierà come
  è invecchiata quella di luglio. Il rimedio, se un giorno serve, è il check
  `ip/forbidden-term` che ex-0018 proponeva — dato versionato, severità `error`
  sul ramo commerciale.

---

## 5. Il comando che rifà la misura

```bash
python3 - <<'PY'
import re
from pathlib import Path
TERMINI = {
 "RHoD": ["Red Hand","Mano Rossa","Drellin","Brindol","Elsir","Wyrmlord","Azarr Kul","Ghostlord",
          "Kulkor","Rhest","Vraath","Skull Gorge","Gola del Teschio","Dawn Way","Via dell'Alba",
          "Saarvith","Ulwai","Hravek","Koth"],
 "Undermountain": ["Undermountain","Belkram"],
 "Underdark-src": ["Maur","Cristal Warrior","Crystal Warrior"],
 "OutOfAbyss": ["Neverlight","Out of the Abyss"],
}
def testo(d):
    return "\n".join(f.read_text(encoding="utf-8", errors="ignore")
                     for f in Path(d).rglob("*.md")
                     if not any(x in str(f) for x in ("/rendered/", "/homebrew/", "/_ARCHIVIO/")))
for d in sorted(p for p in Path(".").glob("[01]*") if p.is_dir()) + \
         [Path(x) for x in ("campaign", "Bestiario", "PG", "STANDALONE-Il-Drappo-di-Tarsilia")]:
    t = testo(d); w = len(t.split())
    if not w:
        print(f"{str(d)[:36]:<38}{0:>8}  (vuoto)"); continue
    celle = [f"{n:>5} ({n/w*1000:>5.1f})" for n in
             (sum(len(re.findall(re.escape(p), t, re.I)) for p in ps) for ps in TERMINI.values())]
    print(f"{str(d)[:36]:<38}{w:>8}  " + "  ".join(celle))
PY
```

⚠️ **Vale quanto la sua lista di termini.** Aggiungere una fonte significa
aggiungerla qui: l'audit di luglio sbagliò proprio così, cercando solo RHoD e i
toponimi FR quando `campaign-history.md` ne dichiarava altre quattro. La lezione
di quella revisione vale come metodo: **prima di dichiarare pulito un arco, si
cercano tutte le fonti che il repo dichiara**, non quella che si ha in mente.
