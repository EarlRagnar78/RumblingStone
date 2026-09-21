# ADR-0037 — Stdlib-only, e le eccezioni che esistono davvero

> **Stato**: accettata · **Data**: 2026-09-03 · **Decide**: G. Samuele (DM)
> **Attua**: `plans/PIANO-QUALITA-DEL-CODICE.md` lotto 0
> **Rapporti**: rende esplicito il `stdlib_only` che ADR-0012 §6 dava come
> preferenza senza motivarla; convive con ADR-0026 (pacchetti Typst
> vendorizzati) e ADR-0027 (`pdfcpu`), che riguardano binari, non librerie.

## Il contesto

`stdlib_only: true` compare in 44 delle 54 voci di `scripts/tools.manifest.json`.
ADR-0012 lo elenca fra le regole dello standard dei tool, con una riga:
*«`stdlib_only` preferito; ogni pacchetto di terze parti o binario esterno va
dichiarato nel manifest»*. Dice cosa va fatto, non perché, e neanche quando la
regola si può rompere.

Il risultato è che la domanda torna. È tornata il 2026-09-03, quando il DM ha
chiesto se per ogni script non convenisse guardare se esiste una libreria che
risolve il problema meglio. La risposta corretta quasi sempre è che la libreria
esiste e che va usata lo stesso il codice del repo, e senza un ADR quella
risposta sembra pigrizia.

## La decisione

**Gli script Python di questo repo usano la sola libreria standard. Le
dipendenze esterne ammesse sono binari, non pacchetti Python, e vanno dichiarate
nel manifest con la loro degradazione.**

Il motivo è dove gli strumenti girano: sul portatile del DM, la sera della
sessione, spesso senza rete. Un `pip install` che fallisce alle 20:45 è un
booklet che non si stampa. La libreria migliore vale meno della certezza che il
comando parta.

Le eccezioni ammesse sono di due tipi.

**Binari esterni**, dichiarati in `external_bins` e con una degradazione
scritta: `git` (8 tool), `bash` (4), `typst` (2), `python3` (2), `chromium` (2),
`cwebp`, `pandoc`, `inkscape`. Un binario si installa una volta con il gestore
di pacchetti del sistema e non ha un albero di versioni transitive; se manca, il
tool deve dirlo e uscire pulito, non lanciare una traccia di stack. ADR-0026 e
ADR-0027 sono due casi già decisi per questa via.

**Due librerie Python**, `pyyaml` e `Pillow`, che stanno su due piani diversi e
vanno tenute distinte. Vedi sotto.

> ⚠️ **Correzione del 2026-09-03** (lotto D). La prima stesura di questa ADR
> diceva che `pyyaml` era *«l'unica libreria Python nel repo»*. Era falso:
> `build_booklet_html.py` e `build_image_derivatives.py` usano **Pillow**. Le
> due non sono lo stesso caso, ed è la differenza che conta, non il numero.

## Le due librerie, e perché una sola è un debito

Quattro tool dichiarano `pyyaml` in `external_deps`: `build-skills`,
`compress_skills`, `sync-skills`, `validate_skills`. La CI la installa
esplicitamente:

```yaml
- run: pip install pyyaml
```

Quindi la frase «il repo è stdlib-only» oggi è falsa in un punto, e il punto sta
nel percorso critico: `validate_skills.py` è un gate bloccante del workflow.

I due modi in cui i quattro tool la gestiscono non sono lo stesso modo.

| Tool | Se `pyyaml` manca |
|---|---|
| `validate_skills.py` | messaggio su stderr e `sys.exit(2)` |
| `compress_skills.py` | `import yaml` nudo, traccia di stack → **corretto**, ora esce con 2 |
| `build_monster_catalog.py` (per confronto) | non la importa: scrive YAML a mano, 60 righe |

`build_monster_catalog` è la prova che il sottoinsieme di YAML usato qui si
scrive senza libreria. Il frontmatter delle skill è più vario del formato del
catalogo, e finché non c'è un parser scritto in casa che regga quel
frontmatter, `pyyaml` resta.

**Chiuso**: `compress_skills.py` ora fallisce come `validate_skills.py`, con un
messaggio e il codice 2, invece che con una traccia. Era il punto elencato come
coda opzionale in `PIANO-AUDIT-SCRIPTS-QUALITA-E-CONTRATTI.md`.

### `Pillow`: come dovrebbe stare una dipendenza Python

`Pillow` serve a ricomprimere le immagini grandi (`build_booklet_html.py`) e a
generare i derivati da impaginazione (`build_image_derivatives.py`). Nessuna
delle due cose è nel percorso critico, la CI non la installa, e **entrambi i
chiamanti degradano in modo dichiarato**: il primo incorpora l'immagine com'è e
ottiene un file più pesante con la stessa resa, il secondo esce dicendo come
installarla.

Questa è la forma che una dipendenza Python può avere sotto questa regola: fuori
dai gate, con un ripiego scritto, importata dentro la funzione che la usa e non
in testa al file. `pyyaml` non ce l'ha, e per questo è un debito mentre `Pillow`
non lo è.

## Le librerie che vincerebbero, e cosa costano

Il confronto è stato fatto guardando il codice, non a impressione.

| Dove servirebbe | Libreria | Verdetto |
|---|---|---|
| slug | `python-slugify` | vincerebbe sul singolo caso; il repo ne usa un sottoinsieme di quattro righe e lo tiene in `dmcore/testo.py` (lotto A) |
| lettura HTML (`import_html_module`) | `beautifulsoup4`, `lxml` | `html.parser` basta; la conversione si è fatta una volta sola |
| YAML | `pyyaml` | già dentro, come debito circoscritto |
| PDF (`export_booklet_pdf`) | `reportlab` | Typst fa già il lavoro, e non è una libreria Python |
| test | `pytest` | `unittest` regge 370 test; una dipendenza in meno nel percorso della CI |

Su `pytest` vale la pena essere espliciti, perché è la richiesta che torna più
spesso. Il vantaggio che si cerca adottandolo è il TDD, e il TDD non richiede
`pytest`: il lotto B di `PIANO-QUALITA-DEL-CODICE` ha scritto 22 test con
`unittest` e li ha collaudati mutando i validatori, cogliendo 6 mutazioni su 6.

## Le conseguenze

**Quello che si guadagna.** Un clone del repo e un Python 3.11 bastano per far
girare quasi tutto. La risposta alla domanda «perché non usiamo una libreria?»
sta scritta, con la sua data e il suo perché, invece di essere ricostruita ogni
volta da chi risponde.

**Quello che si paga.**

- **Codice scritto in casa dove una libreria sarebbe più corta.** Il parser YAML
  del catalogo, la lettura HTML, la slug. Sono righe da mantenere, e la
  giustificazione regge solo finché restano sottoinsiemi piccoli e stabili. Una
  di queste che cresce è un segnale, non un fastidio.
- **`pyyaml` resta un'incoerenza dichiarata.** Chi legge il manifest vede 44
  voci `stdlib_only` e quattro che non lo sono, e questa ADR non le chiude:
  dice che sono un debito e a quali condizioni si paga.
- **Nessun file di dipendenze.** Non esistono `requirements.txt` né
  `pyproject.toml`. Il lotto D ha risposto mettendo la dichiarazione in
  `scripts/binari.py`: Python minimo, binari con la loro degradazione, le due
  librerie e quale catena ha bisogno di cosa. `dm.py doctor` legge da lì.

**Quando si rivede.** Uno di questi tre fatti riapre la decisione:

1. un sottoinsieme scritto in casa supera le ~150 righe o acquista un difetto
   che la libreria corrispondente non avrebbe (il caso `slug` senza `NFKD`, con i
   suoi 9 record sbagliati, ci è andato vicino);
2. il repo smette di girare anche sul portatile del DM e vive solo in CI, dove
   installare è gratis;
3. una catena nuova richiede un formato che nessuno vuole scrivere a mano (un
   PDF letto invece che scritto, per dire).

Fuori da questi casi la risposta alla domanda «c'è una libreria migliore?» è
*«sì, e non si usa lo stesso»*.

---

## 🔴 Emendamento del 2026-09-21 — le dipendenze di sviluppo sono un piano diverso

**Stato**: accettato dal DM il 2026-09-21 · **Non rovescia** la decisione:
la restringe a ciò che davvero la motiva.

### Cosa è successo

La CI è andata rossa su tre file di test scritti in stile pytest. La CI esegue
`python -m unittest discover -s scripts/tests` e **pytest non era installato**:
due file non si importavano (`ModuleNotFoundError`), il terzo era fatto di
funzioni nude, che `unittest` importa **senza eseguire**. In locale si vedevano
**966** prove, in CI ne giravano **942**.

🔎 **Il terzo caso è quello che conta.** Il rosso si vede; una prova che non
gira **in silenzio** no. Ventiquattro prove scritte e nessuna eseguita dove
decide.

### La distinzione che mancava

La decisione del 2026-09-03 dice *«gli script Python di questo repo usano la
sola libreria standard»*, e la sua ragione è **dove girano**: il portatile del
DM, la sera, senza rete. Quella ragione **non si applica ai test**.

| | Dove gira | `pip install` è… | Regola |
|---|---|---|---|
| **esecuzione** (`scripts/`) | portatile del DM, la sera della sessione | un rischio alle 20:45 | **stdlib-only**, tre eccezioni dichiarate |
| **sviluppo** (`scripts/tests/`, CI) | qui e sul runner | **un passo del workflow** | dipendenze ammesse, elencate in `requirements-dev.txt` |

> **L'emendamento, in una riga**: *lo stdlib-only vale su ciò che il DM esegue.
> Un test non lo esegue il DM.*

**Ammesso**: `pytest`, in `requirements-dev.txt`. Le `TestCase` esistenti
girano identiche sotto entrambi i corridori, quindi **non si perde niente** e
non c'è una migrazione da fare.

⚠️ **Il vincolo che resta, e che è la parte operativa.** Ammettere pytest
riapre esattamente il buco del 2026-09-21 al contrario: con pytest le funzioni
nude girano, con `unittest` no, e chi scrive non se ne accorge. Quindi il repo
**gira entrambi i corridori** e il cancello
`scripts/tests/test_i_test_girano_in_ci.py` verifica che **vedano lo stesso
numero di prove**. Una divergenza è rossa: è la misura del difetto, non la
promessa di non ripeterlo.

### Due file di dipendenze, e la terza libreria

Il testo sopra dice *«nessun file di dipendenze: non esistono
`requirements.txt` né `pyproject.toml`»*. Da oggi esistono, e la ragione è la
tabella qui sopra: **due piani diversi vogliono due file diversi**.

🔴 **E misurando per scriverli è saltata fuori una terza libreria.** Un
attraversamento `ast` di tutti i `scripts/**/*.py` trova, fuori dalla libreria
standard, **`pyyaml` (13 file), `Pillow` (3), `tiktoken` (2)** — e `tiktoken`
questa ADR non la nominava. Degrada bene in entrambi i chiamanti
(`compress_skills.py` ripiega su parole × 1,3, `measure_tokens.py` su
caratteri ÷ 4), quindi è un'eccezione della stessa famiglia di Pillow, non un
debito come `pyyaml`. È la **seconda volta** che questa ADR sbaglia il conto
delle proprie librerie contandole a memoria, e la seconda volta che la
correzione arriva da un attraversamento invece che da una rilettura.

`bpy` e `mathutils` restano fuori da entrambi i file: non si installano con
pip, sono il Python interno di Blender.
