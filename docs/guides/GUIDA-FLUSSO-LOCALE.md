# Guida al flusso locale — far lavorare insieme tutti i tool del DM

> **A chi serve.** A chi si siede davanti al repo sulla propria macchina e vuole
> sapere **cosa c'è, cosa fa, e in che ordine si usa**. Le altre guide spiegano
> un mestiere alla volta (mappe, immagini, booklet, bestiario); questa spiega
> **come si incastrano**.

---

## §0 · TL;DR — la catena in cinque righe

```bash
# 1. il contenuto sta nei markdown: quelli sono i master (ADR-0003)
# 2. le mappe nascono da un contratto JSON, non da un disegno
python3 scripts/compile_map_json.py mappa.json -o mappa.md && python3 scripts/render_map_svg.py mappa.md
# 3. i booklet si assemblano da un manifest
python3 scripts/build_booklet_html.py MANIFEST.json --format both      # schermo
python3 scripts/export_booklet_typst.py MANIFEST.json --all            # stampa: UN volume
# 4. i gate dicono se qualcosa si è rotto
python3 scripts/dm.py doctor --ci
```

---

## §1 · Le quattro famiglie di tool, e cosa fa ognuna

| Famiglia | Tool | Cosa fa, in una riga |
|---|---|---|
| **Sessione** | `dm.py prep` · `suggest_encounter` · `suggest_loot` | prepara la serata: incontri a EL, tesoro, dossier |
| | `dm.py session` · `state_apply` · `session_recap` | chiude la serata: canone, recap per il gruppo e per PG |
| **Mappe** | `compile_map_json` → `render_map_svg` → `export_map_png` / `export_uvtt` | dal contratto JSON alla pergamena, al PNG, al VTT |
| | `import_watabou` · `suggest_map` | parti da un generatore esterno, o fatti proporre una pianta |
| **Materiali** | `build_booklet_html` · `export_booklet_pdf` · `export_booklet_typst` | i booklet: schermo, pagine sciolte, volume da stampa |
| | `build_chapter_marks` · `hype_homebrew` · `dm_dossier` | fregi di capitolo, recap impaginati, dossier PNG |
| **Controlli** | `validate_maps` · `validate_modules` · `validate_standalone` · `validate_bestiario` · `validate_skills` · `check_plans_discipline` | i gate che girano anche in CI |

L'elenco completo, generato dal manifest e sempre aggiornato, sta in
[`docs/tools/README.md`](../tools/README.md). Se un tool non è lì, **non esiste**
(ADR-0012).

---

## §2 · La regola che tiene insieme tutto

> **Il markdown è la verità. Tutto il resto è un artefatto rigenerabile.**

Da questa regola (ADR-0003) discende il resto:

- **non si modifica un HTML, un PDF, un `.hb.md` o un `.typ`**: si modifica il
  master markdown e si rigenera;
- **non si modifica un SVG di mappa**: si modifica il JSON e si ricompila;
- i PDF **non stanno nel repo** (`*.pdf` è in `.gitignore`): si rifanno in un
  comando quando servono.

Il corollario pratico: se ti trovi a correggere a mano un file generato, **stai
correggendo il posto sbagliato** e la tua correzione sparirà alla prossima
rigenerazione. È già successo: `PROCEDURA.md` §7 degli stemmi racconta la volta
in cui il generatore era andato alla deriva dai file che generava.

---

## §3 · Il flusso di una serata, dall'inizio alla fine

```
        PRIMA                          AL TAVOLO                 DOPO
  ┌──────────────────┐          ┌──────────────────┐    ┌──────────────────┐
  │ dm.py prep       │          │ i PDF stampati   │    │ dm.py session    │
  │ suggest_encounter│   ──▶    │ le mappe sul VTT │──▶ │ state_apply      │
  │ export_*_pdf     │          │ i prop in mano   │    │ session_recap    │
  └──────────────────┘          └──────────────────┘    └──────────────────┘
```

1. **Prima**: `dm.py prep <arco>` raccoglie quello che serve. Se manca un
   incontro, `suggest_encounter` lo propone all'EL giusto e `suggest_loot` gli
   attacca il tesoro. Le mappe si esportano in PNG per stampare o in `.uvtt` per
   Foundry/Roll20.
2. **Al tavolo**: carta e VTT. Nessuno script gira durante la partita — è una
   scelta, non una mancanza (vedi §6).
3. **Dopo**: `dm.py session` guida la chiusura. Le scritture di canone passano
   dal **triplo vincolo** di ADR-0007 (branch di gruppo + diff confermato +
   regioni `auto:`): nessun tool scrive nel canone di nascosto.

---

## §4 · La catena dei booklet — due binari, due destinazioni

Dal **2026-08-15** ci sono due strade, e non sono in concorrenza
([ADR-0020](../../plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md)):

| | Schermo | Stampa |
|---|---|---|
| **Comando** | `build_booklet_html.py MANIFEST.json --format both` | `export_booklet_typst.py MANIFEST.json --all` |
| **Motore** | Chromium (per i PDF sciolti) | `typst` |
| **Produce** | `.html` + `.hb.md`, e con `export_booklet_pdf.py` un PDF **per capitolo** | **un volume** `-STAMPA.pdf` |
| **Tipografia** | Georgia, font di sistema | **EB Garamond + Cinzel embeddati** (OFL, in `scripts/typst/fonts/`) |
| **Indice** | l'HTML ha i tab | **segnalibri PDF veri** + indice cliccabile |
| **Quando** | mandare una pagina a un giocatore, impaginare altrove | il libro |

Entrambe leggono **lo stesso manifest**: un capitolo aggiunto lì compare in
tutte e due. È l'unico punto in cui le due catene si toccano, ed è voluto.

### Installare `typst`

È un singolo eseguibile, Apache 2.0. Se manca, l'esportatore **te lo dice ed
esce pulito** — la catena HTML continua a funzionare da sola.

```bash
curl -sSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
sudo install typst-*/typst /usr/local/bin/
```

### I fregi di capitolo

`build_chapter_marks.py` genera i medaglioni che aprono i capitoli: **due serie
distinte**, una per la campagna (una per arco) e una per il modulo
autoconclusivo. L'esportatore Typst li aggancia da solo, per nome di file.

```bash
python3 scripts/build_chapter_marks.py --all
```

---

## §5 · La catena delle immagini

L'ordine conta, e il primo passo non è il prompt:

1. **direzione artistica** — le sei leve della skill
   [`rumblingstone-art-direction`](../../skills/rumblingstone-art-direction/SKILL.md):
   ancora storica, schede-personaggio, lock di seed e luce, gate di rifiuto;
2. **i prompt** — `dm.py prompts <arco>` estrae lo scheletro dalle scene
   (ADR-0015); i prompt li scrive una persona, non una regex;
3. **la generazione** — ComfyUI in locale (`scripts/comfyui-local/`), con il
   modello scelto **per licenza** e non per gusto
   ([ADR-0019](../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md));
4. **il gate di rifiuto**, il giorno dopo;
5. **la provenienza** — una riga per immagine, o non si committa.

Il dettaglio operativo sta in [`GUIDA-IMMAGINI.md`](GUIDA-IMMAGINI.md).

---

## §6 · Cosa questo repo **non** fa, e perché

Detto qui perché non lo si cerchi invano:

- **niente app da tavolo.** Nessun tracker d'iniziativa, nessun contatore di PF
  live: il repo produce **documenti**. Chi vuole quegli strumenti li usa
  accanto, non dentro;
- **niente generazione procedurale di mappe.** Le piante sono disegnate attorno
  agli incontri: una pianta casuale è più veloce e **peggiore**;
- **niente CMYK né PDF/X.** La catena Typst produce RGB, che basta per la stampa
  casalinga e per il digitale. Per una tiratura vera servirebbe Scribus, e allora
  si riapre ADR-0020;
- **niente scrittura automatica nel canone.** ADR-0007 non si aggira.

---

## §7 · Quando qualcosa si rompe

```bash
python3 scripts/dm.py doctor --ci     # tutti i gate in un colpo
python3 -m unittest discover -s scripts/tests
```

Se un gate è rosso, la skill
[`rumblingstone-debugging`](../../skills/rumblingstone-debugging/SKILL.md) dice
come si cerca la causa **prima** di proporre una correzione. Vale per
l'infrastruttura, non per il contenuto: le domande di regole e di canone hanno
le loro skill.

---

## §8 · Le altre guide

| Guida | Copre |
|---|---|
| [GUIDA-SETUP-MACCHINA](GUIDA-SETUP-MACCHINA.md) | da zero a repo funzionante |
| [GUIDA-MAPPE](GUIDA-MAPPE.md) | le tre modalità, il contratto JSON, l'export VTT |
| [GUIDA-IMMAGINI](GUIDA-IMMAGINI.md) | generatori, prompt, licenze dei pesi |
| [GUIDA-BOOKLET-E-PDF](GUIDA-BOOKLET-E-PDF.md) | manifest campo per campo, le due catene |
| [GUIDA-BESTIARIO](GUIDA-BESTIARIO.md) | statblocchi e catalogo |
| [GUIDA-CONDIVISIONE-IP](GUIDA-CONDIVISIONE-IP.md) | cosa si può mostrare, e a chi |
| [TOOL-AUTHORING-STANDARD](TOOL-AUTHORING-STANDARD.md) | come si scrive un tool nuovo (ADR-0012) |
