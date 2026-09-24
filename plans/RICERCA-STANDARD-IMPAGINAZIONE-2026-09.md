# RICERCA — Gli standard di impaginazione e resa grafica, e quali sono misurabili

> **Cos'è**: il gemello della ricerca sulla prosa, dal lato **impaginazione,
> stampa e accessibilità**. Cosa prescrivono gli standard veri, quali
> diventano un controllo eseguibile, e a che punto sta la catena di stampa del
> repo — misurato sui parametri reali del tema e sulle metriche dei font, non
> stimato a occhio.
>
> **Stato**: ✅ ricerca completa (2026-09-19) · **Gemella di**:
> [RICERCA-STANDARD-PROSA-WOTC-PAIZO](RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md)
> **Alimenta**: [PIANO-MISURA-EDITORIALE-STANDARD](PIANO-MISURA-EDITORIALE-STANDARD.md)

---

## 1 · Qui gli standard sono più duri che sulla prosa

È la differenza che vale la pena dire subito: sulla prosa gli editori hanno
**convenzioni di casa**, e la norma ISO (5060) riguarda il *processo* di
valutazione. Sull'impaginazione esistono **norme ISO sul manufatto**, con
validatori che le verificano file per file.

### 1.1 · PDF/UA — ISO 14289

Lo standard dell'accessibilità del PDF: albero dei tag obbligatorio, ordine di
lettura logico, mappatura Unicode dei font, metadati leggibili a macchina.
La parte che lo rende **operativo** è il **Matterhorn Protocol**, che traduce
la norma in **136 punti di controllo verificabili**, e il validatore libero
**veraPDF** che li esegue.

### 1.2 · PDF/X — ISO 15930

Lo standard dello scambio per la stampa professionale: ammette solo ciò che
serve in tipografia. Le varianti che contano sono PDF/X-1a (solo CMYK, niente
trasparenza), PDF/X-3 (RGB con profilo ICC) e PDF/X-4 (trasparenza viva).

⚠️ **Una dichiarazione di conformità non è una conformità verificata**: un file
può dichiararsi conforme e fallire la validazione per un font mancante o uno
spazio colore illegale. Serve il validatore, non l'etichetta.

### 1.3 · Le misure tipografiche

- **Lunghezza di riga**: 45-75 caratteri su colonna singola (regola di
  Bringhurst), **40-50 su impaginato a più colonne**.
- **Interlinea**: rapporto **1,4-1,6** per il testo corrente, 1,1-1,3 per i
  titoli. Più larga è la misura, più interlinea serve.
- **Vedove, orfane e fiumi**: la riga sola in cima alla colonna, la riga sola
  in fondo, e il canale bianco verticale che attraversa il testo giustificato.

### 1.4 · La tradizione del manuale di ruolo

Le **due colonne** sono la forma del manuale di ruolo dal 1977 (AD&D), e la
ragione è la stessa misura di §1.3: a formato pagina pieno, una riga singola
di corpo 10-11 pt è troppo lunga da leggere.

🔎 **Ed esiste un pacchetto Typst `pf2e-style`** che riproduce l'impianto
Paizo. Il repo impagina già in Typst, quindi è direttamente confrontabile.
⚠️ **Non ho potuto verificarne licenza e parametri**: `typst.app` è bloccato
dal proxy di rete di questo ambiente. Resta un appiglio da controllare, non
una cosa da adottare al buio.

---

## 2 · La catena del repo, misurata

Parametri letti da `scripts/typst/tema-rumblingstone.typ`, e larghezza media
del carattere **misurata sulle metriche vere di EB Garamond** (`fontTools`,
media pesata sulla frequenza delle lettere in italiano): **0,3717 em**.

🔎 **Garamond è stretto**, e questo è il motivo per cui la stima a occhio non
bastava: avevo in mente ~0,48 em, e avrei sbagliato del 30% — nella direzione
sbagliata.

| Formato | colonne | misura | corpo | **caratteri/riga** | fascia | |
|---|---:|---:|---:|---:|---|---|
| **A5** | 1 | 346 pt | 9,6 pt | **97** | 45-75 | 🔴 **ben oltre** |
| **A4** | 2 | 236 pt | 10,2 pt | **62** | 40-50 (multicolonna) · 45-75 (generale) | 🟡 sopra la prima, dentro la seconda |

| Altro | Stato |
|---|---|
| interlinea `leading: 0.62em` → rapporto **1,62** | 🟡 appena sopra 1,4-1,6 — ma su una misura da 97 caratteri l'interlinea generosa è **giusta**: è la misura a essere sbagliata, non l'interlinea |
| font EB Garamond · Cinzel · Inconsolata, tutti **OFL e incorporati**, nessun font di sistema | 🟢 |
| margini **speculari** (`inside`/`outside`) + `binding: left` | 🟢 è ciò che distingue un libro da una risma |
| titoli `sticky` — nessun titolo orfano in fondo a una colonna | 🟢 la vedova più visibile è già presidiata |
| **tag PDF** prodotti, con ripiego dichiarato su un bug di typst | 🟢 e la cosa giusta: quando ripiega **lo dice**, invece di consegnare un PDF diverso da quello promesso |
| **nessuno standard PDF dichiarato** in tutta la catena (né PDF/X né PDF/UA) | 🔴 |
| `validate_booklets` controlla manifest, immagini, pagine, segnalibri | 🟡 zero controlli **tipografici** |

### 🔴 Il risultato che conta

> **L'A5 — il formato che il commento del tema chiama «la misura di un manuale
> tascabile vero» — è a 97 caratteri per riga.** È oltre ogni fascia
> raccomandata, di parecchio.

Ed è il gemello esatto del 17% di read-aloud fuori norma trovato sulla prosa:
una cosa fatta con cura, con una ragione scritta accanto, che **nessuno aveva
misurato**.

⚠️ **Margine d'errore dichiarato**: 0,3717 em è una media pesata su minuscole
e spazio; il testo vero ha maiuscole, punteggiatura e una giustificazione che
muove la spaziatura. Do a questa stima un **±10%**. Anche al minimo, l'A5
resta a **~87** caratteri per riga: la conclusione non cambia.

### Le tre uscite possibili, e quale fa l'industria

| | Come | Effetto misurato |
|---|---|---|
| **a** | **due colonne anche su A5** | colonna ~162 pt → **~45 car./riga**, dentro la fascia multicolonna. È ciò che il tema **già fa su A4**, ed è la tradizione del manuale di ruolo dal 1977 |
| b | corpo da 9,6 a ~13 pt | arriva a ~70 car./riga ma gonfia il numero di pagine |
| c | misura più stretta (~8,8 cm) | arriva a ~70 ma lascia margini enormi: si spreca carta |

**La (a) è l'unica che risolve senza costi**, e allinea A5 e A4 alla stessa
logica invece di tenerne due.

---

## 3 · Cosa diventa un controllo

| # | Norma | Severità | Come si misura |
|---|---|---|---|
| **L1** | caratteri per riga dentro la fascia del formato | **maggiore** | dai parametri del tema + metriche del font: è **aritmetica**, non giudizio |
| **L2** | interlinea 1,4-1,6 | minore | lettura diretta di `leading` |
| **L3** | font incorporati, nessun font di sistema | **critico** | un font non incorporato rende il PDF non stampabile: è il pass/fail assoluto della stampa |
| **L4** | conformità **PDF/UA** | maggiore | `veraPDF` sui 136 punti del Matterhorn |
| **L5** | conformità **PDF/X** per l'edizione da stampa | maggiore | preflight, solo sui volumi destinati alla tipografia |
| **L6** | vedove e orfane | minore | ⚠️ **non misurabile dal sorgente**: serve il PDF reso |

⚠️ **E qui vale la regola uscita dalla ricerca gemella — *una norma, un
rilevatore*.** L1-L3 si leggono dal tema e vanno dentro `validate_booklets`,
che già esiste; non nasce un secondo script.

---

## 4 · Cosa NON ho potuto misurare, e perché

Questa sezione esiste perché ADR-0056 vuole scritta la ragione di ogni buco.

- **`typst`, `veraPDF` e `pdftotext` non sono installati** in questo ambiente.
  Quindi L4, L5 e L6 sono **progettati e non eseguiti**: non ho compilato un
  volume né validato un PDF. Chiamarli «verificati» sarebbe falso.
- **`typst.app` è bloccato dal proxy**, quindi il pacchetto `pf2e-style` resta
  un appiglio non ispezionato: licenza e parametri da controllare prima di
  qualunque adozione.
- **La resa a occhio** — se una pagina «è bella» — non la misura niente di
  tutto questo, esattamente come sulla prosa.

---

## 5 · Cosa alimenta

| Va in | Cosa |
|---|---|
| `PIANO-MISURA-EDITORIALE-STANDARD` F1.1 | L1-L6 come righe della tipologia, con la severità |
| `scripts/validate_booklets.py` | L1, L2, L3 — si **estende**, non si duplica |
| `skills/rumblingstone-editoria` | la fascia dei caratteri per riga non è scritta da nessuna parte nella skill |
| `skills/REGISTRO-NORME-EDITORIALI.md` | le sei norme, con le tre non eseguite e la loro ragione |
| **Decisione DM** | l'A5 a 97 caratteri per riga: due colonne, o si lascia? |

---

## Fonti

[PDF/UA — ISO 14289](https://pdfa.org/resource/iso-14289-pdfua/) ·
[PDF/X — ISO 15930](https://pdfa.org/resource/iso-15930-pdfx/) ·
[ISO 14289-1:2014 su iso.org](https://www.iso.org/obp/ui/en/#!iso:std:64599:en) ·
[Preflight: cosa controlla davvero](https://freetoolonline.com/guides/en/pdf-preflight-online-what-it-actually-checks.html) ·
[Lunghezza di riga ottimale](https://baymard.com/blog/line-length-readability) ·
[Measure / line length — Google Fonts Knowledge](https://fonts.google.com/knowledge/using_type/understanding_measure_line_length) ·
[Interlinea e misura](https://loremforge.com/learn/line-length-leading-and-measure) ·
[Vedove, orfane e fiumi](https://www.adobe.com/creativecloud/design/discover/typography/widows-and-orphans.html) ·
[Colonne nel manuale di ruolo](https://documentdesignfall17.wordpress.com/2017/11/10/the-evolution-of-the-role-playing-game-page-layout/) ·
[pacchetto Typst `pf2e-style`](https://typst.app/universe/package/pf2e-style/)
