# ADR-0020 — L'edizione da stampa esce da un secondo binario, non dal browser

**Stato**: accettata *(via libera del DM 2026-08-15, dopo il campione)*
**Data**: 2026-08-15
**Decisione-fonte**: domanda del DM del 2026-08-15 sui tool open source per
arrivare al livello Paizo/WotC, e l'analisi in
`plans/RICERCA-TOOL-ESTERNI-DM-2026-08.md` §3-ter.

## Contesto

[ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md) ha fissato la catena
attuale: manifest → `build_booklet_html.py` → HTML + sorgente Homebrewery →
`export_booklet_pdf.py` → **un PDF A4 per capitolo**, stampato da Chromium
headless.

Quella catena ha fatto il suo lavoro e va tenuta. Ha però un limite che non si
supera con altro CSS, perché è nello strumento: **Chromium impagina pagine web,
non libri**.

- niente controllo su **vedove e orfane**;
- niente **crenatura** fine né gestione della spaziatura ottica;
- l'**indice** non diventa una struttura di segnalibri degna;
- i font restano **quelli di sistema** — il booklet usa Georgia, e su una
  macchina che non ce l'ha il PDF cambia faccia;
- **un file per capitolo**, mentre un lettore vuole *un* volume.

Sono esattamente quattro dei sei divari misurati nel capitolato del Drappo
(`PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md` §2). Nessuno è un difetto di come è
scritto il codice: sono il soffitto del browser come motore di stampa.

## Decisione

**L'edizione da stampa si genera con un secondo binario — Typst — e la catena
HTML resta invariata.**

### 1. Due binari, due destinazioni

| Catena | Motore | Serve a |
|---|---|---|
| **schermo / Homebrewery** | `build_booklet_html.py` → HTML + `.hb.md` | leggere, condividere, impaginare altrove. **Non cambia** |
| **stampa** | manifest → `.typ` → **Typst** → PDF unico | il volume: tipografia embedded, segnalibri, un file solo |

È la separazione che usa qualsiasi editore: una versione per leggere a schermo,
una per il torchio. **Non** si sostituisce la prima con la seconda — un booklet in
HTML si apre ovunque e un PDF no.

### 2. Perché Typst e non gli altri

- **Typst** — Apache 2.0, CLI (`typst compile`), font embedded via `--font-path`,
  linguaggio di impaginazione scriptabile, compilazione incrementale. Un sorgente
  di testo che sta in git e produce un PDF vero: è il modello che questo repo usa
  già per tutto il resto.
- ❌ **LaTeX** — farebbe il lavoro, ma la catena di distribuzione è pesante e i
  messaggi d'errore sono un mestiere a parte.
- ❌ **Scribus** (GPL) — fa CMYK e PDF/X, che servirebbero per una stampa
  professionale vera. Ma è **GUI-first**: lo scripting è fragile e il sorgente è
  un file binario, cioè l'opposto di un repo che genera tutto da testo
  versionato. **Da riconsiderare solo se si arriva a una tiratura reale.**

### 3. Le condizioni della dipendenza esterna

È la **prima dipendenza da un binario esterno** del toolkit (finora: solo
stdlib e un browser headless). Vale quindi ADR-0012 per intero, più due regole:

1. **degradazione pulita** — se `typst` non è installato, l'esportatore dice
   quale binario manca e come si installa, ed esce con codice non-zero **senza
   lasciare file a metà**. La catena HTML continua a funzionare da sola;
2. **il sorgente `.typ` è generato, non scritto a mano** — vale ADR-0003
   (markdown master, layout generati): il contenuto resta nei `.md` del modulo, e
   il `.typ` è un artefatto rigenerabile.

### 4. I font

Caratteri **OFL** embeddati, non font di sistema. Candidati da verificare al
momento dell'attuazione — la licenza si ricontrolla, non si eredita da questo
ADR.

## Attuazione — quello che si è scoperto facendola

Tre cose emerse solo montando la pipeline, e che vale la pena aver scritto:

1. **Con `--root`, in Typst i percorsi assoluti sono relativi alla RADICE.**
   Passare il percorso del filesystem fa cercare `/home/...` dentro la radice e
   fallisce. È l'errore che si prende chiunque monti Typst la prima volta.
2. **Le tabelle da 4+ colonne scavalcano le due colonne.** In una colonna da
   8 cm si spezzano perfino le parole del titolo: sopra quella soglia il tema le
   fa flottare a piena larghezza, che è ciò che fa un manuale stampato.
3. ⚠️ **Typst 0.15.1 ha un bug interno** nella costruzione dell'albero dei tag
   PDF (`internal error: parent group`) su documenti con float dentro strutture
   annidate. L'esportatore **riprova con `--no-pdf-tags` e lo dichiara a video**:
   il volume è completo e i segnalibri ci sono, ma manca il livello di
   accessibilità per i lettori di schermo. La riga di fallback si toglie il
   giorno che una versione nuova compila — non prima, e non in silenzio.

## Conseguenze

- Più facile: si chiudono **[2] tipografia, [4] PDF unico con segnalibri** e metà
  di **[6] frontespizio** con un solo strumento, senza toccare
  `build_booklet_html.py` — quindi **senza rischio per i booklet della campagna**,
  che è il motivo per cui la catena HTML non si tocca.
- Più difficile / rinunce: **due catene da mantenere**. Un capitolo aggiunto al
  manifest e non ricontrollato sull'altra catena produce due edizioni divergenti.
  Mitigazione: entrambe leggono **lo stesso manifest**, e la divergenza diventa un
  controllo automatico, non una promessa.
- **Rinuncia dichiarata**: niente CMYK né PDF/X. Per la stampa casalinga e per la
  distribuzione digitale l'RGB va bene; per una tiratura vera servirebbe Scribus,
  e a quel punto si riapre questo ADR.
- Da rivisitare: **al primo modulo stampato davvero**. Finché si stampa in casa su
  A4, l'unica prova che conta è che il volume si apra e i segnalibri funzionino.

## Copertura

- `scripts/export_booklet_typst.py` — il secondo binario, nel manifest, con la
  degradazione pulita se `typst` non è installato
- `scripts/typst/tema-rumblingstone.typ` — il tema: due colonne, carta avorio,
  box read-aloud, aperture di capitolo col fregio, tabelle larghe che scavalcano
  le colonne
- `scripts/typst/scheda-pg.typ` + `scripts/dmcore/schede.py` — **le schede
  pregenerate come schede, non come capitoli** (`"layout": "schede"` nel
  manifest): una pagina A4 per personaggio, a due pannelli, coi dati letti dai
  master `PREGEN-*.md` e `FASCICOLO-*.md` invece che ricopiati. Il testo a
  colonne va bene per un manuale e non per un foglio che sta in mano tre serate:
  a metà combattimento nessuno cerca la CA dentro un paragrafo
- `scripts/typst/fonts/` — EB Garamond e Cinzel **con il loro OFL.txt**: la
  tipografia è embedded, quindi il PDF ha la stessa faccia ovunque
- [`docs/guides/GUIDA-FLUSSO-LOCALE.md`](../../docs/guides/GUIDA-FLUSSO-LOCALE.md)
  — come le due catene lavorano insieme
- [`docs/guides/GUIDA-BOOKLET-E-PDF.md`](../../docs/guides/GUIDA-BOOKLET-E-PDF.md)
  — la traccia stampa accanto a quella schermo
- [ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md) — la catena HTML,
  che resta
- [ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) — manifest e smoke
  del nuovo tool
