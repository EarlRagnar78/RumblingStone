# RICERCA — cosa vale la pena prendere dal panorama dei tool per DM (agosto 2026)

**Aperta**: 2026-08-15
**Domanda-fonte (DM)**: *«può servire analizzare questi thread Reddit per vedere cosa
si può usare o quali idee includere nel repo e nel mini modulo, se ha senso e porta
valore aggiunto ed è compatibile con le licenze»* — con due link:
`r/rpg/comments/1rd55ll` (*my favourite DM tools after testing 15 different apps*) e
`r/dndai/comments/1be4zkb` (*RPG AI tools mega-discussion thread*).

> **La conclusione in una riga**: di quindici app testate da altri, **una sola idea
> vale il costo di importarla** — la trascrizione della sessione registrata, che oggi
> è l'unico anello mancante fra il tavolo e `session_recap.py`. Tutto il resto o è già
> nel repo in forma migliore, o è un servizio a pagamento che non si può importare, o
> è arte con licenza non verificabile.

---

## §0 · Quello che non sono riuscito a leggere — dichiarato prima di tutto

**I due thread non sono raggiungibili da questo ambiente.** Reddit è bloccato a monte:
il proxy di rete risponde `CONNECT tunnel failed, 403` su `curl`, la fetch diretta
rifiuta il dominio, e anche gli estrattori esterni falliscono sull'URL. Ho recuperato
**solo** quanto i motori di ricerca espongono come anteprima:

- del thread r/rpg, l'elenco per come compare nello snippet — *«Notion (World builder);
  Saga20 (Campaign tracker); Syrinscape (Music) …»*, troncato lì;
- del thread r/dndai, la sola riga d'apertura: è un **mega-thread aperto del marzo
  2024** in cui ognuno posta il proprio tool, senza una lista redazionale.

Quindi **non ho letto i commenti né la lista completa**, e non fingo di averlo fatto.
Quello che segue è l'analisi delle **categorie** che quei thread coprono e dei tool
nominati o dominanti oggi, ciascuno verificato alla fonte — licenza inclusa. Se il DM
incolla il testo dei due thread, l'analisi si aggiorna sui nomi veri in mezz'ora.

---

## §1 · Il panorama, per categoria — e cosa risponde già il repo

| Categoria | Chi la occupa fuori | Cosa ha il repo | Divario reale |
|---|---|---|---|
| **Wiki di mondo** | Notion, Obsidian, World Anvil, Kanka | markdown in git + `validate_*` + skill di canone | **nessuno**: qui il canone è versionato e validato a macchina, cosa che nessuno dei quattro fa |
| **Tracker di campagna / recap** | Saga20, GM Assistant, Tabletop Arc, Archivist | `state.md` + `state_apply.py` + `session_recap.py` + `next_session.py` | **uno, e vero**: manca il pezzo *audio → verbale di sessione*. Vedi §3 |
| **Ambiente sonoro** | Syrinscape, Tabletop Audio | cue **descritti**, non brani (ADR-0014, cassetta del DM §5) | nessuno — e la forma del repo è **più portabile**, vedi §2.3 |
| **Mappe** | Inkarnate, Dungeondraft, Dungeon Alchemist | contratto JSON → master → SVG → PNG → UVTT | nessuno sul funzionale; il divario è **artistico**, ed è già tracciato (Lotto 6) |
| **Impaginazione** | Homebrewery, Affinity | `build_booklet_html.py` + Homebrewery self-hosted | tipografia embedded, già tracciata |
| **Al tavolo** (iniziativa, HP) | Improved Initiative, Fight Club, DM's Toolbox | niente — **per scelta** | fuori perimetro: questo è un repo di documenti, non un'app di gioco |
| **Generazione immagini** | Midjourney, ChatGPT Images, CharGen | prompt standardizzati (ADR-0015) + ComfyUI locale | la produzione dei raster, già tracciata |

---

## §2 · I tre tool nominati nello snippet — verdetto uno per uno

### 2.1 Notion — ❌ non importabile, e non serve

SaaS proprietario. Il valore che il thread gli attribuisce (*world builder*) qui è già
coperto meglio: un database Notion non ha diff, non ha revisione, non ha gate. Il repo
ha `git`, `validate_bestiario`, `validate_maps`, `check_plans_discipline`.

**Idea da rubare**: nessuna. L'unica tentazione — i wiki-link `[[così]]` in stile
Obsidian — **peggiorerebbe** il repo: `validate_standalone.py` e `validate_modules.py`
verificano i link relativi, e i wiki-link li renderebbero non verificabili.

### 2.2 Saga20 — ❌ il servizio, ✅ l'idea

Tracker di campagna a **9 USD/mese** che registra la sessione, la trascrive e ne fa un
riassunto. La recensione comparativa più seria che ho trovato (EN World, tre tool a
confronto) gli dà il punteggio migliore ma segnala anche il problema che qui è
dirimente: nei concorrenti *«l'audio resta archiviato senza un modo chiaro di
cancellarlo»*.

**Non si importa** — è un servizio. **L'idea sì**, ed è l'unica del lotto che paga:
vedi §3.

### 2.3 Syrinscape — ❌ e il repo fa già meglio

Libreria sonora in abbonamento, con licenza per traccia. Importare i titoli dei brani
in un modulo creerebbe una **dipendenza che il lettore non può soddisfare
legalmente** senza pagare.

Il repo ha già la forma giusta, ed è scritta nella cassetta del DM del Drappo:

> *«Non serve una colonna sonora. Servono quattro cue per serata, e il silenzio in
> mezzo. Nessun titolo di brano: **descrizioni**, così ognuno usa quello che ha.»*

Un cue come *«un tamburo solo, lento, e poi stop netto sul nome»* funziona con
Syrinscape, con YouTube, con una playlist personale e con un DM che batte le nocche sul
tavolo. Un titolo di brano funziona solo per chi ha quell'abbonamento.
**Nessuna modifica**: questa è già la scelta migliore, e va lasciata in pace.

---

## §3 · L'unica proposta che paga — la trascrizione locale della sessione

**Il divario**, in una riga: `session_recap.py` legge
`campaign/sessions/YYYY-MM-DD_session-*.md` e ne ricava il recap per i giocatori. Ma
**quel file lo scrive il DM a mano, dopo**, quando è stanco — ed è il punto in cui la
catena si rompe più spesso. È esattamente ciò che Saga20 e simili vendono a 9-27 USD
al mese.

**La versione license-clean**: [whisper.cpp](https://github.com/ggml-org/whisper.cpp) —
**licenza MIT**, implementazione C/C++ senza dipendenze, inferenza **CPU-only**, e
soprattutto **interamente locale**: i pesi si scaricano una volta e poi non c'è
nessuna rete. Il problema di riservatezza dei servizi cloud — la voce dei giocatori
caricata su un server terzo — **non si pone**: l'audio non esce dalla macchina del DM.

Forma proposta: `scripts/transcribe_session.py`, che prende un file audio e produce la
**bozza** del verbale nel formato che `state_apply.py` e `session_recap.py` già
leggono, con i campi obbligatori vuoti e da riempire.

⚠️ **Non è una decisione da prendere di sfuggita**, e per questo qui c'è la proposta e
non il codice:

1. sarebbe la **prima dipendenza da un binario esterno** nel toolkit — finora tutto è
   stdlib o browser headless. ADR-0012 chiede il manifest; questo chiede **un ADR
   suo**, con la regola di degradazione (se il binario non c'è, lo script dice come
   installarlo ed esce pulito, non fallisce a metà);
2. tocca il **consenso**: registrare i giocatori si chiede prima. La regola va scritta
   nel tool, non lasciata al buon senso;
3. la trascrizione produce una **bozza**, mai canone. ADR-0007 (triplo vincolo sulle
   scritture di canone) resta intatto: il DM legge, taglia e firma.

**Costo stimato**: mezza giornata per lo script + l'ADR. **Guadagno**: chiude C3 della
ricerca precedente e toglie l'attrito dove la campagna lo perde davvero.

---

## §4 · Quello che ho verificato e scartato

| Tool | Licenza verificata | Verdetto |
|---|---|---|
| **whisper.cpp** | **MIT**, offline, CPU-only | ✅ unico candidato all'import (§3) |
| **Kanka** | **non è open source**: sorgente pubblico ma con **Commons Clause** sopra (Owlchester SNC) — vietato «vendere» il software, inclusi hosting e supporto a pagamento | ❌ come codice da importare. Utilizzabile come servizio esterno, ma duplicherebbe il canone: due fonti di verità, e quella fuori dal repo non ha gate |
| **Notion · World Anvil · Saga20 · GM Assistant · Tabletop Arc · Archivist · CharGen** | SaaS proprietari, da 9 a 27 USD/mese | ❌ non importabili per costruzione |
| **Syrinscape · Tabletop Audio** | licenza per traccia / termini proprietari | ❌ come asset. Vedi §2.3 |
| **Inkarnate · Dungeondraft · Dungeon Alchemist** | asset proprietari | ❌ già sulla lista nera del capitolato del booklet |
| **Improved Initiative · Fight Club · DM's Toolbox** | varie, alcune libere | ❌ **fuori perimetro**: sono app da usare *durante* la partita; il repo produce documenti |
| **game-icons.net · Watabou · font OFL** | CC BY 3.0 · permissivi · OFL | ✅ **già dentro**, con attribuzione in `CREDITS.md` |

---

## §5 · E il mini-modulo? — niente, ed è una buona notizia

Su `STANDALONE-Il-Drappo-di-Tarsilia/` la risposta onesta è **nessun cambiamento**:

- i **suoni** sono già nella forma portabile (§2.3);
- la **continuità fra le serate** ha già `STATO-DEL-MODULO.md`, che è di carta e sta in
  una pagina: per tre serate un tracker in abbonamento sarebbe sovradimensionato;
- la **trascrizione** del §3 è pensata per la campagna lunga. Su tre serate il verbale
  non serve: il modulo finisce prima che la memoria diventi un problema.

Quello che al Drappo manca davvero resta quello già misurato nel capitolato
(`PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`): **immagini raster**, tipografia
embedded, mappa in versione giocatore, PDF unico. Nessuno dei quindici tool testati da
altri lo risolve al posto nostro.

---

## §6 · Il criterio, per la prossima volta

Da questa ricerca esce una regola riusabile, e vale la pena scriverla:

> **Un tool esterno entra nel repo solo se supera tre soglie**: la licenza permette
> l'uso *e* la ridistribuzione di ciò che produce; funziona **offline** o degrada
> in modo pulito; e sostituisce un attrito **misurato**, non uno immaginato.

Le prime due si verificano in dieci minuti. La terza è quella che scarta quasi tutto:
il repo non ha un problema di funzionalità mancanti, ha un problema di **arte**, e
l'arte non si risolve abbonandosi a un tracker di campagna.
