# Le passate redazionali — il giro, non la norma

La **norma** sta in `editorial-standards.md` (come si scrive) e in
`italiano-nativo.md` (come non si scrive tradotto). Qui c'è il **giro**: quante
passate, cosa si guarda in ciascuna, quando un testo è chiuso e come si riapre.

Perché serviva. Il repo aveva un processo scritto per il **collaudo al tavolo**
(`rumblingstone-playtest`, nove sezioni) e **niente** per la revisione del testo:
la norma esisteva e il giro no. Nel colophon di un AP la redazione è il mestiere
più affollato — diciassette nomi su cinquanta — ed è quello che qui non aveva
forma.

---

## Le tre passate, in quest'ordine, e mai insieme

Guardare tutto in una volta significa vedere i refusi e non la struttura. Una
cosa alla volta.

### 1ª — La struttura (si legge saltando)

Non si legge il testo: si guarda **la forma**.

- Le sezioni obbligatorie ci sono tutte? (`validate_modules` lo dice gratis: si
  esegue **prima**, non si controlla a mano)
- L'ordine è quello dell'uso? Corpo in ordine di gioco, appendici a salto.
- Ogni scena ha un'uscita: cosa fa passare oltre, e cosa succede se non arriva.
- I rimandi puntano a qualcosa che esiste.

**Si chiude quando**: nessuna sezione manca e nessun rimando è rotto.
⚠️ **Non si tocca una virgola in questa passata.** Correggere prosa mentre si
guarda la struttura è il modo di finire con una struttura non guardata.

### 2ª — La voce (si legge ad alta voce, davvero)

Questa è l'unica passata che **richiede la bocca**. Il traduttese e i tic dell'IA
si sentono e non si vedono: un periodo che sulla pagina sembra normale, letto a
voce, inciampa.

- I dieci calchi di `italiano-nativo.md` §1 — il possessivo sulle parti del
  corpo, il progressivo, *realizzare*, *eventualmente*, la nominalizzazione.
- I tic di §9: **l'antitesi «non X: è Y» massimo una per documento**, le maiuscole
  di portento massimo una, il tricolon che non finisce mai.
- Il read-aloud: sta in sei secondi? Chiude su un decision point?
- ⚠️ **Gli echi sono testo come gli altri.** È la cosa che il tavolo nomina per
  prima quando suona tradotto, e la si salta perché «sono note», non prosa
  (`consequence-echoes.md`).

**Si chiude quando**: una lettura ad alta voce non inciampa in nessun punto.

### 3ª — Le bozze (si legge una riga alla volta, dal fondo)

Dal fondo verso l'inizio: leggendo in avanti il cervello completa le parole, ed è
per questo che i refusi sopravvivono a tre riletture.

- `validate_lingua.py` prima, sempre: accenti, doppi spazi, punteggiatura. Ciò
  che una macchina trova non si cerca a mano.
- Poi il resto: concordanze, numeri (una CD scritta due volte deve essere la
  stessa), nomi propri contro il glossario.

**Si chiude quando**: `validate_lingua` è pulito e la lettura all'indietro non
trova più niente.

---

## Quando un testo è **chiuso**

Le tre passate fatte, in ordine, e i gate verdi. Un testo chiuso:

- **non si tocca per migliorarlo.** Una modifica «già che ci sono» è una modifica
  non revisionata, e rientra dalla finestra dopo essere uscita dalla porta;
- si può **stampare**: da [ADR-0023](../../../plans/adr/ADR-0023-colophon-di-edizione.md)
  porta una versione, quindi due copie diverse si distinguono.

## Come si **riapre**

Tre casi soli, e ognuno ha una regola:

| Caso | Cosa si fa |
|---|---|
| **Un errore** (un numero sbagliato, una contraddizione) | si corregge, si **alza la versione**, e se qualcuno ha già stampato si scrive un `ERRATA-*.md` |
| **Il tavolo ha giocato** e qualcosa non ha funzionato | la correzione passa da `rumblingstone-playtest` §7, non da qui: è collaudo, non redazione |
| **Contenuto nuovo** | non è una riapertura: è un testo nuovo, e rifà le tre passate |

⛔ **Non è una riapertura**: «rileggendolo non mi piace più». Quello è
riscrivere, e un testo riscritto ricomincia dalla prima passata.

---

## Chi fa cosa (per non sprecare token)

| Livello | Chi |
|---|---|
| Sezioni obbligatorie, rimandi, termini banditi | `validate_modules.py` — gratis, in CI |
| Refusi meccanici, accenti, spazi | `validate_lingua.py` — gratis, in CI |
| Calchi «sempre» e nomi inglesi dove il canone vuole l'italiano | `validate_prosa.py` — su **tutto** il contenuto |
| Calchi di registro (possessivo, progressivo) e **tic a densità** | `validate_prosa.py` — su read-aloud **e su tutti i file per i giocatori** (hint, teaser, echi, handout, prop) |
| Voce, ritmo, se una scena suona tradotta | **umano o agente**, con questo file + `italiano-nativo.md` |
| Se può uscire, con che crediti | [`rumblingstone-edizione`](../../rumblingstone-edizione/SKILL.md) |

⚠️ **Nessun gate sostituisce la 2ª passata.** Un validatore trova «realizzi che»;
non trova una scena che suona tradotta pur essendo in italiano corretto. I gate
tolgono il rumore **perché la lettura ad alta voce senta il resto**.
