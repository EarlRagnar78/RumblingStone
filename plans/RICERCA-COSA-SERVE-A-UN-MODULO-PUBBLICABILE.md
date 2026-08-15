# RICERCA — cosa separa un modulo *scritto bene* da un modulo *che si gioca*

**Aperta**: 2026-08-15
**Domanda-fonte (DM)**: *«cosa manca davvero tra le skill e gli script che può rendere
questo minimodulo e anche la campagna RumblingStone memorabile e giocabile — cioè
tutto quello che c'è davvero di lavoro dietro alla pubblicazione di un modulo che
diventa memorabile per i giocatori e bello da masterizzare per i DM? E cosa può essere
riportato nel repo principale per diventare canone?»*

**Metodo**: audit del `STANDALONE-Il-Drappo-di-Tarsilia` e del repo contro la prassi
editoriale consolidata delle avventure pubblicate (Paizo, WotC, produzione indie
di qualità) — non contro un'indagine web fatta oggi, ma contro convenzioni note e
verificabili aprendo un qualsiasi modulo stampato: foglio del cast, guida alla
pronuncia, indice dei read-aloud, inserto per lo schermo, prop fisici, questionario
di playtest, note di accessibilità.

> **La conclusione in una riga**: al modulo non manca *contenuto*. Manca l'**apparato
> d'uso** — le sei-sette pagine che nessuno legge per piacere e senza le quali un DM
> passa la serata a cercare invece che a raccontare.

---

## §1 · Il divario, in tre famiglie

### A · L'apparato d'uso al tavolo — **il buco più grosso**

| # | Cosa manca | Perché conta | Costo |
|---|---|---|---|
| A1 | **Foglio del cast** — tutti i PNG su una pagina: nome, contrada, cosa vuole, il tic vocale, dove si trova | Il DM cerca in cinque file il nome dell'ostessa mentre sei persone aspettano | basso |
| A2 | **Guida alla pronuncia** | Un DM che esita su un nome lo usa meno. I nomi che il tavolo non ripete non esistono | bassissimo |
| A3 | **Indice dei read-aloud** — dove sta ogni box, in ordine di gioco | Si leggono **prima**, ad alta voce, in preparazione. È l'unico modo perché suonino bene | basso |
| A4 | **Inserto per lo schermo del DM** — una pagina, tutte le CD e le soglie | Esiste il §7 delle regole, ma non è impaginato per stare davanti agli occhi | basso |
| A5 | **Cue sonori/ambientali** — la `rumblingstone-module-standard` li chiede già («cue musicali») e **non esistono in nessun file del repo** | È il moltiplicatore d'atmosfera più economico che ci sia | basso |

### B · La memorabilità — quello che i giocatori si portano a casa

| # | Cosa manca | Perché conta | Costo |
|---|---|---|---|
| B1 | **Prop fisici**: il contratto di Vesca, la pagina del registro dei morti, la ricevuta di Salle, il decreto | Un foglio che passa di mano al tavolo vale dieci minuti di descrizione. Il repo **ha già i template Homebrewery** (`campaign/templates/homebrew/lettera.hb.md`, `profezia`, `avviso-torneo`) e il modulo **non li usava** | medio |
| B2 | **Il momento da fotografare** — dichiarare, per ogni serata, la scena che il tavolo racconterà | Nessuna convenzione nel repo. Un modulo che non sa qual è il suo picco lo sprecacon la fretta | bassissimo |
| B3 | **Carte da tavolo** (segnaposto contrada, ordine di corsa) | Rende visibile lo stato della gara senza spiegarlo | basso |
| B4 | **Variante di stampa accessibile** (alto contrasto, corpo grande, legenda mappe safe per daltonici) | Un giocatore su dodici non distingue rosso e verde: le mappe usano **entrambi** per PG e nemici | basso |

### C · La continuità fra le sessioni — quello che chiedevi esplicitamente

| # | Cosa manca | Perché conta | Costo |
|---|---|---|---|
| C1 | **Stato del modulo** — i due contatori, i patti scritti, le scelte fatte, gli echi aperti, in **un file solo** | `dm.py session` esiste ma è **vincolato ad ADR-0007**: branch di gruppo + `campaign/state.md`. Un modulo di tre serate non ha niente di tutto questo e resta **senza memoria** fra una serata e l'altra | medio |
| C2 | **Echo Ledger** — la `module-standard` lo richiede (§11) e il modulo ha gli echi **sparsi**, non registrati | È il meccanismo BG3 del repo: senza registro, gli echi non tornano mai | basso |
| C3 | **Recap fra le serate** | `session_recap.py` legge lo `state.md` della campagna: inutilizzabile qui | medio |

### D · Il collaudo — come si passa da alfa a canone

| # | Cosa manca | Perché conta | Costo |
|---|---|---|---|
| D1 | **Skill di playtest** — non esiste in nessuna forma | Il repo sa *scrivere* e sa *validare a macchina*, ma **non sa collaudare al tavolo**: cosa si misura, chi lo annota, quando un modulo smette di essere alfa | medio |
| D2 | **Questionario di feedback** giocatori + DM | Senza, il playtest produce impressioni e non dati | basso |
| D3 | **Validator del modulo standalone** — `validate_modules.py` copre **solo** `ARC*-DEF-*.md`: il modulo nuovo non ha **nessun gate** | Un file rinominato e nessuno se ne accorge finché non si apre al tavolo | medio |
| D4 | **Validator aritmetico delle schede pregenerate** | Gli errori sulle sei schede li ho trovati **a mano**. Una macchina li trova sempre e gratis | medio |
| D5 | **Budget incontri PF1e** — `suggest_encounter.py` fa la matematica **3.5** (EL logaritmico), non i **px per GS** di PF1e | La tabella di scalabilità 4/5/6/7 l'ho calcolata a mano | medio |

### E · Cose che ci sono già e vanno solo **usate**

| Cosa | Dove | Nel modulo |
|---|---|---|
| **Export VTT** (Foundry/Roll20) | `scripts/export_uvtt.py` | ❌ mai lanciato |
| **Template prop Homebrewery** | `campaign/templates/homebrew/` | ❌ mai usati |
| **Glossario e loc kit** | `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md` | ❌ il modulo non ci si aggancia |
| **Estrazione prompt scene** | `scripts/extract_scene_prompts.py` (ADR-0015) | ❌ i prompt li ho scritti a mano |

---

## §2 · Cosa diventa canone nel repo principale

Non tutto quello che serve al modulo serve alla campagna. Questa è la separazione.

| Elemento | Standalone | Campagna | Come |
|---|---|---|---|
| **Skill `rumblingstone-playtest`** | ✅ | ✅ **canone** | il collaudo serve identico alle sessioni della campagna: cosa si misura, il questionario, alfa→beta→giocato |
| **`validate_standalone.py`** | ✅ | 🟡 parziale | il gate sui **riferimenti incrociati** e sull'**aritmetica delle schede** vale per tutto il repo; le sezioni obbligatorie sono specifiche del formato standalone |
| **Foglio del cast + pronuncia** | ✅ | ✅ **canone** | va aggiunto alla `rumblingstone-module-standard` come sezione obbligatoria: la campagna ha **centinaia** di PNG e nessun foglio del cast |
| **Cue sonori** | ✅ | ✅ **canone** | la module-standard li cita già e nessuno li ha mai prodotti: qui nasce la convenzione |
| **Echo Ledger operativo** | ✅ | ✅ già canone, ma **non applicato** | la standard lo richiede al §11; questo modulo fornisce il **formato di riferimento** |
| **Stato leggero di modulo** | ✅ | ❌ | la campagna ha `state.md` + ADR-0007, che è più forte. Non si tocca |
| **Prop fisici** | ✅ | ✅ **canone** | i template esistono: manca la **regola** «ogni beat che consegna un documento lo consegna davvero» |
| **Variante accessibile** | ✅ | ✅ **canone** | riguarda le mappe di tutta la campagna (rosso/verde nella legenda) |
| **Budget PF1e** | ✅ | 🟡 | la campagna gira in 3.5; utile solo per i boost via `npc-villain-boosting` |

---

## §3 · Priorità — cosa vale davvero la pena

Ordinate per **memorabilità al tavolo per unità di lavoro**, non per completezza.

1. **B1 · I prop fisici.** Quattro fogli che passano di mano. Nessun'altra voce di
   questa lista produce altrettanto ricordo.
2. **A1+A2+A3+A4 · L'apparato d'uso** in un file solo. È la differenza fra un DM che
   racconta e un DM che cerca.
3. **D1+D2 · Il collaudo.** Senza, il modulo resta alfa per sempre e la campagna
   continua a non avere un metodo.
4. **C1+C2 · La memoria fra le serate.** Tre sessioni senza stato = i patti del
   Giorno 2 dimenticati al Giorno 3.
5. **D3+D4 · I gate a macchina.** Costano una volta e pagano per sempre.
6. **A5 · I cue sonori.** Cinque righe per serata.
7. **E · Usare quello che c'è**: UVTT, template prop, glossario.
8. **B4 · Accessibilità.** Poco lavoro, e riguarda una persona su dodici.

---

## §4 · Quello che **non** serve, e perché

Un audit onesto dice anche cosa lasciar stare:

- **Un sistema di achievement/badge per i giocatori.** Funziona nei giochi
  competitivi, non a un tavolo di sei adulti in tre serate.
- **Un generatore di PNG casuali.** Il modulo ha ventidue personaggi scritti: un
  generatore produrrebbe nomi senza volere niente, che è il difetto opposto.
- **Un "encounter builder" grafico.** Il contratto JSON delle mappe copre già il
  bisogno reale; l'editor visuale è un piano a sé (`PIANO-EDITOR-VISUALE-MAPPE`).
- **La traduzione inglese.** ADR-0016 l'ha già decisa: sorgente italiana, edizione
  inglese solo su materiale IP-pulito e finito. Questo modulo non lo è ancora.
- **Un sito/landing page.** Prima si gioca, poi si pubblica.

---

## §5 · Stato d'attuazione

Chiuso nel **Lotto 5** del `PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md` (2026-08-15):
A1-A5, B1-B2, B4, C1-C2, D1-D4, E (UVTT + template prop).
Restano ⬜: **B3** (carte da tavolo), **C3** (recap automatico fra le serate),
**D5** (budget PF1e come script) — tutti e tre gated su una sessione vera, perché
senza tempi reali si ottimizzerebbe alla cieca.
