# MAPPE — CENSIMENTO (T5a)

> **Scopo**: inventario di tutti i file-mappa degli archi 00-09 (pattern
> `*MAPPE*`, `*Ultra-Clear*`/`*UltraClear*`, `*Lotto*`, `TACTICAL-GRIDS*`,
> `*FASE*-MAPPA*`, atlanti, + tutto il contenuto di cartelle `Mappe/`) per il
> lotto **T5a** di `PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md` §2.
> **Task**: eseguire `scripts/render_map_svg.py` su ogni file, produrre SVG in
> `rendered/` accanto al sorgente, censire scala/parsabilità/companion.
> **Questo lotto non corregge nulla** (niente fix di griglie KO, niente
> scrittura di companion mancanti — quello è T5b/T5c). Engine: **Sonnet 5**.
> Sessione: 2026-07-03.

---

## Legenda colonne

- **Scala dichiarata**: il file dichiara esplicitamente "1.5m/quadrato" (o
  equivalente) per la mappa. Sì/No.
- **Griglia parsabile**: `render_map_svg.py` trova ≥1 griglia emoji-cella con
  ≥3 righe. Sì/No.
- **Companion**: presenza dei 3 blocchi Ambiente/Tattiche/Evoluzione (T3) nel
  file sorgente. `nessuno` / `parziale` / `completo`.
- **SVG**: `ok` (generato in `rendered/`) / `KO` (motivo in nota) / `n/a`
  (file non è un master di griglia — atlante, indice, spec testuale).

---

## Arco 07 — Il Portale della Forgia Eterna

| File | Mappa | Scala dichiarata | Griglia parsabile | Companion | SVG |
|---|---|---|---|---|---|
| `Mappe/Portale-Forgia-L1-REVISED-UltraClear.md` | MAPPA PF-1: Stanza della Corona (20×14) | Sì | Sì | nessuno | ok |
| `Mappe/Portale-Forgia-L1-REVISED-UltraClear.md` | MAPPA PF-2: Sala della Forgia Eterna (27×27) | Sì | Sì | nessuno | ok |
| `Mappe/Portale-Forgia-L2-REVISED-UltraClear.md` | Mappa #1 (21×53) — titolo grezzo `[COLONNA K = 15m da Nord]` | Sì | Sì (titolo automatico impreciso — vedi nota 1) | nessuno | ok |
| `Mappe/Portale-Forgia-L2-REVISED-UltraClear.md` | MAPPA PF-4: Forgia Adamantina (33×25) | Sì | Sì | nessuno | ok |
| `Mappe/Portale-Forgia-L3-FINALE-REVISED.md` | Foresta di Cristallo Gigante + Camera Sferica Boss + altre (4 fence) | No (usa "1.5m/5ft" solo in legenda) | **No** | n/a | **KO — nota 2** |
| `Mappe/TACTICAL-GRIDS-COMPLETE.md` | Spec testuali (coordinate in prosa, no griglia visuale) | Sì (in header standard) | **No** | n/a | **KO — nota 3** |
| `Mappe/Atlante-Visivo-Mappe.md` | — (file STUB dichiarato, rimanda a TACTICAL-GRIDS) | — | No | — | n/a |
| `ARC07-ATLANTE-ASSET.md` | — (catalogo immagini/musica, non è un master mappa) | — | No | — | n/a |

## Arco 08 — La Battaglia di Hammerfist

| File | Mappa | Scala dichiarata | Griglia parsabile | Companion | SVG |
|---|---|---|---|---|---|
| `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md` | Dirupo Mortale / Campo Hobgoblin (40×40) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md` | Fortezza vista dall'alto (50×80) — **ARC-08 assedio** | Sì | Sì | **completo (T5b, sessione 4)** | ok |
| `Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md` | MAPPA H3-1: Ingresso Passaggi Antichi (40×40) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-1-Ricognizione.md` ⚠️ DEPRECATED (A8) | Mappa #1 (20×100) — titolo grezzo intestazione colonne | Sì | Sì (titolo automatico impreciso — nota 1) | parziale (nota testuale "Copertura Roccia", "Canyon stretto" inline, non nei 3 blocchi) | ok |
| `Mappe/Hammerfist-Lotto-1-Ricognizione.md` ⚠️ DEPRECATED (A8) | Mappa #2 (28×30) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-2-Assedio.md` | MAPPA 2A: Fortezza vista dall'alto (34×80) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-3-FINALE.md` | MAPPA 3X: Ingresso Passaggi Antichi (40×40) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-3-FINALE.md` | GRIGLIA 33×33 Caverna Intersection | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-3-FINALE.md` | Golden Sphere Manifestation Round 8 (40×41) | Sì | Sì | nessuno | ok |
| `Mappe/Hammerfist-Lotto-3-FINALE.md` | Ground Battle 120m×200m (30×71) | Sì | Sì | nessuno | ok |
| `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` | Diagrammi ASCII box-drawing (▓, ║, no griglia numerata a celle) | Parziale (in prosa) | **No** | n/a (è l'atlante-indice) | **KO — nota 3** |
| `ARC08-14-ATLANTE-IMMAGINI.md` | — (catalogo immagini, non è un master mappa) | — | No | — | n/a |
| `ARC08-91-DEPRECATO-atlante-visivo-v2.md` ⚠️ DEPRECATED | Diagrammi ASCII box-drawing pre-Ultra-Clear | No | **No** | n/a (superato da L1-L3 Ultra-Clear) | **KO — nota 4** |
| `ARC08-92-DEPRECATO-atlante-visivo-v3-complete.md` ⚠️ DEPRECATED | Diagrammi ASCII box-drawing pre-Ultra-Clear | No | **No** | n/a (superato da L1-L3 Ultra-Clear) | **KO — nota 4** |

## Arco 09 — Continuazione dopo Hammerfist

| File | Mappa | Scala dichiarata | Griglia parsabile | Companion | SVG |
|---|---|---|---|---|---|
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | Campo Drow 1: Burning Operations Base (53×40) | Sì | Sì | **completo (T5b, sessione 4)** — riportato inline nel sorgente, non solo nel template (nota 5 aggiornata) | ok |
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | Campo Drow 2: Forward Base (66×53 — griglia abbreviata `[continues...]`, nota 6) | Sì | Sì (parziale: righe ripetute per compressione, SVG riflette solo ciò che è scritto) | **completo (T5b, sessione 4)** — EVOLUZIONE `[INFERRED]`, griglia comunque da completare in T5c | ok (grid incompleta — T5c) |
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO-Description.md` | — (testo narrativo/atmosfera dei 3 campi, non griglia) | — | No | — | n/a — **nota 7: file NON è più 0 byte, contenuto già presente** |
| `Arco-Post-Hammerfist-P1-MAPPE-COMPLETO.md` | Cerchio di Hellas vs Treant, Rituale (Tre ondate), + altre | Sì (in prosa) | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2A-Torre-PARTE1-MAPPE.md` | Torre — Livello 1 | parziale | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2A-Torre-PARTE2-MAPPE-Livelli2-3.md` | Torre — Livelli 2-3 | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2A-Torre-PARTE3-MAPPE-Livello4.md` | Torre — Livello 4 | Sì | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2A-Torre-PARTE4-MAPPE-Boss-Zalkatar.md` | Torre — Boss Zalkatar | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2B-Torneo-MAPPE-COMPLETO.md` | Arena del Torneo | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2B-Torneo-MAPPE-COMPLETO-2.md` | Arena del Torneo (v2) | Sì | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P2D-PALIO-MAPPE.md` | Città/Piazza del Palio (companion SVG a mano già in `P2D-Palio-Allegati/mappe/*.svg`, nota 9) | Sì | **No** | n/a | **KO — nota 8/9** |
| `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE0-NOTTE-DEI-DROW-MAPPA.md` | Fase 0 | Sì | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE1-ASSEDIO-MAPPA.md` | Fase 1 | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE2-RITUALISTI-MAPPA.md` | Fase 2 | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE3-AZARRKUL-AVATAR-MAPPA.md` | Fase 3 | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE4-CIRCOLO-MYTHAL-STATUE-MAPPA.md` | Fase 4 | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-Ghostlord-LICH-ALLEANZA-MAPPE.md` | Alleanza Ghostlord | Sì | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-Sabotaggio-Campi-Drow-MAPPE.md` | Sabotaggio Campi Drow | No | **No** | n/a | **KO — nota 8** |
| `Arco-Post-Hammerfist-P3-Starsong-Hill-ALLEANZA-ELFI-MAPPE.md` | Alleanza Elfi | No | **No** | n/a | **KO — nota 8** |

---

## Riepilogo numerico

- **File censiti**: 34 (tutti quelli che matchano i pattern del task o vivono
  in una cartella `Mappe/`).
- **Griglie emoji trovate e renderizzate**: **16 SVG**, in 9 file sorgente
  (5 preesistenti dall'esemplare T2 + 11 nuovi in questo lotto), tutti in
  `rendered/` accanto al sorgente. Nessun errore di rendering (XML valido,
  `python3 scripts/render_map_svg.py <file> --list` li trova tutti).
- **KO (nessuna griglia emoji parsabile)**: 22 mappe/file, tutte per lo
  stesso motivo di fondo — **formato diverso dall'emoji-grid**, non un bug
  del parser. Si dividono in 4 categorie (vedi note 2-4, 8):
  - 1 file con griglia **ASCII lettere+simboli testuali** (`[X1]`, `C`, `.`)
    invece di celle-emoji (nota 2).
  - 4 file con **diagrammi ASCII box-drawing** (▓/║/┌) senza griglia
    numerata a celle — 2 sono già marcati ⚠️ DEPRECATED (nota 3-4).
  - 16 file (quasi tutta la Parte 2-3 di ARC-09: Torre, Torneo, Palio,
    Battaglia Finale FASE0-4, Ghostlord, Sabotaggio, Starsong Hill) sono
    **descrizioni tattiche in prosa con coordinate testuali** (es. "fila 20,
    colonna 20"), mai state in formato griglia-emoji: non è materiale
    "da riparare", è un formato editoriale diverso che il renderer non
    copre (nota 8).
  - 4 file sono **atlanti/indici/cataloghi** (immagini, musica, spec) senza
    alcuna griglia da renderizzare per costruzione (n/a, non KO).
- **Companion (Ambiente/Tattiche/Evoluzione)**: **0 file sorgente** ha i 3
  blocchi inline nel formato template T3 (l'unico esemplare compilato,
  Campo Drow 1, vive nel file template, non nel sorgente — nota 5). Materiale
  per **T5b** (le mappe con tattiche sparse da consolidare: Portale-Forgia
  L1/L2, Hammerfist L1-L3 + Lotto 1-3, Campo Drow 1-2) e **T5c** (le mappe
  senza alcuna tattica esistente, generazione da zero).

---

## Note

1. **Titolo automatico impreciso**: il parser preferisce come titolo la prima
   riga "a prosa" dentro il fence; su 2 file cattura l'intestazione delle
   colonne (`A B C D...`) invece del vero nome della mappa perché non c'è un
   banner `═══` sopra la griglia. La griglia e l'SVG sono corretti (celle,
   colori, legenda); solo l'etichetta in alto allo SVG è da correggere a
   mano in un lotto successivo (fuori scope: T5a non corregge contenuti).
2. **Portale-Forgia-L3-FINALE-REVISED.md**: usa un formato a lettere-riga
   (`A B C...`) con simboli testuali tra parentesi quadre (`[X1]`, `[Th]`,
   `C`, `.`) invece di emoji-per-cella. È un master di griglia valido e
   leggibile da umano, ma **non è nel formato che `render_map_svg.py`
   riconosce** (righe `\d+ <emoji>...`). Nessuna azione in T5a; eventuale
   estensione del parser o riscrittura del master è fuori scope (valutare in
   T5c se la Camera Sferica Boss va giocata presto).
3. **TACTICAL-GRIDS-COMPLETE.md** e **Atlante-Hammerfist-Mappe-COMPLETE.md**:
   sono companion-spec testuali (coordinate a lettere/numeri in prosa, es.
   "Squares D3-E4"), non griglie visuali — coprono lo stesso contenuto delle
   mappe REVISED/Lotto già renderizzate ma in formato descrittivo. Non è un
   fallimento di parsing, è materiale complementare che resta come testo.
4. **ARC08-91/92-DEPRECATO**: diagrammi ASCII pre-Ultra-Clear, già marcati
   ⚠️ DEPRECATED nel proprio banner e superati dai master `Hammerfist-L1/L2/
   L3-REVISED-Ultra-Clear.md` (che sono già renderizzati, sopra). Nessuna
   azione: regola d'oro §0.5, non si cancellano, restano con banner.
5. **Campo Drow 1** — **aggiornata (T5b, sessione 4)**: il companion
   3-blocchi era solo l'ESEMPIO COMPILATO dentro
   `campaign/templates/mappa-tattica-template.md` (righe 76+); ora è anche
   riportato inline nel file sorgente
   `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`, sostituendo la vecchia
   sezione "Tattiche Raid" (stesso contenuto, riorganizzato).
6. **Campo Drow 2**: la griglia dichiara 80×53 ma il master markdown la
   abbrevia con `[continues...]` a un certo punto (già noto, vedi piano
   trasversale §2 T5c). L'SVG generato qui riflette solo le righe
   effettivamente scritte nel sorgente — è **corretto rispetto al master
   attuale**, ma il master stesso è incompleto. Completare la griglia è
   compito di **T5c** (Opus 4.8), non di T5a.
7. **SUPPLEMENTO-P1C-...-Description.md**: il piano trasversale (§2, T5c)
   lo cita come "0 byte" (task ARC-09 §161 aperto). Verificato in questa
   sessione: il file **ha già 3276 byte** di contenuto narrativo completo
   per i 3 campi drow — la nota nel piano è superata. Nessuna azione
   necessaria in T5c per questo punto; da correggere il riferimento nel
   piano trasversale in un futuro aggiornamento di quel documento.
8. **16 file "narrativi" di ARC-09 P2/P3**: usano coordinate in prosa
   (es. "Zona PG iniziale: File 4, colonne 8–24") invece di griglie
   emoji-cella. Non hanno mai avuto un master in formato griglia — non sono
   quindi "griglie da riparare" ma un genere di file diverso (piano di
   combattimento testuale). Se il DM vuole la stessa qualità visuale di
   Campo Drow/Hammerfist per questi incontri, serve **scrivere ex novo** una
   griglia emoji equivalente: lavoro generativo, quindi **T5c (Opus 4.8)**,
   non T5a/T5b.
9. **P2D-Palio-Allegati/mappe/*.svg**: 4 SVG già presenti (Palio di
   Channathgate) ma **non generati da questa pipeline** — non hanno un
   master markdown a griglia-emoji corrispondente in
   `Arco-Post-Hammerfist-P2D-PALIO-MAPPE.md`. Prodotti a mano/altro
   strumento nell'arco originale del Palio. Lasciati intatti (regola d'oro
   §0.5); non rientrano nel censimento SVG di questa pipeline.

---

## Prossimi lotti collegati

- **T5b** (Sonnet 5): consolidare le mappe CON tattiche sparse nei 3 blocchi
  template — parti da giocare prima (Portale-Forgia L1/L2 per P3B/P5,
  Hammerfist Lotto 2/3 per l'assedio, Campo Drow 1-2 per le quest ARC-09
  imminenti).
- **T5c** (Opus 4.8): completare la griglia Campo Drow 2, scrivere
  companion generativi dove manca ogni tattica, valutare se estendere il
  parser (o riscrivere a griglia-emoji) per Portale-Forgia-L3 (nota 2) e per
  i 16 file narrativi di ARC-09 P2/P3 (nota 8) — solo per le parti
  effettivamente imminenti al tavolo.
