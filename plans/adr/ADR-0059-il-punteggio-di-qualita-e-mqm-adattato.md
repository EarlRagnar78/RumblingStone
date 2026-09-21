# ADR-0059 — Il punteggio di qualità è MQM adattato, e la soglia nasce dal repo

**Stato**: accettata (2026-09-21), attuata
**Attua**: [PIANO-MISURA-EDITORIALE-STANDARD](../PIANO-MISURA-EDITORIALE-STANDARD.md) F1.4 · F2.1 · F2.2 · F2.5
**Numero**: riservato da quel piano il 2026-09-19, occupato oggi
**Strumento**: `scripts/punteggio_mqm.py` · **Specifica**: `scripts/specifiche-qualita.yaml`

---

## Contesto

`misura_craft.py` risponde alla domanda «questo congegno c'è?». Ha trovato
difetti veri, ma è una metrica costruita in casa: **tutto pesa uguale**, non
c'è una soglia di accettazione, e il metro d'oro l'ha scritto un valutatore
solo. Un box di tredici righe e una contraddizione col canone valgono
un'unità a testa.

Il mestiere ha risposto prima di noi. **MQM**, dal 2024 anche **ISO 5060**,
definisce l'errore come *«mancato rispetto delle specifiche di progetto»* — non
«brutto», ma **difforme da ciò che era stato dichiarato** — e lo pesa con tre
severità, **minore 1 · maggiore 5 · critico 25**, dove il critico è pass/fail
assoluto. È esattamente il problema del repo: una skill dichiara una norma, un
documento non ce l'ha.

## Decisione

**Il punteggio di qualità editoriale è MQM adattato, la specifica sta in un
YAML fuori dal codice, e la soglia nasce dalla distribuzione misurata del repo.**

Quattro vincoli, e ognuno chiude un modo di sbagliare:

1. **Le severità sono quelle canoniche**, e solo il critico è pass/fail. Un
   solo critico boccia il documento qualunque sia il punteggio.
2. **La specifica è dati, non codice.** `specifiche-qualita.yaml` contiene
   pesi, norme, classi e soglie: cambiare una soglia è una decisione di
   prodotto, e il DM deve poterla prendere senza toccare Python.
3. **Nessun rilevatore nuovo.** Il punteggio **riusa** `misura_craft` e
   `validate_prosa`; una norma entra solo se qualcosa già la misura. È il
   criterio *una norma, un rilevatore*, e la conseguenza è scomoda e
   dichiarata: delle ~40 norme del registro ne entrano **quattro**, e
   `--norme` lo stampa invece di lasciar credere che le altre valgano zero.
4. **La soglia nasce dal repo.** `--distribuzione` (lotto F1.4) misura
   P10/P25/P50/P75 per classe, e la soglia è quel valore arrotondato in basso.
   Il cancello **nasce verde e non butta via niente**; da lì si stringe per
   gradi, e ogni stretta porta la sua ragione (ADR-0036).

## I numeri di partenza, misurati il 2026-09-21

| Classe | n | P10 | P25 | P50 | P75 | min | Soglia scelta |
|---|---:|---:|---:|---:|---:|---:|---:|
| `master_def` | 5 | 97,51 | 97,90 | 98,26 | 99,12 | 97,25 | **97,0** (P25 arrotondato) |
| `arco` | 479 | 100,00 | 100,00 | 100,00 | 100,00 | 88,41 | **88,0** (vedi sotto) |
| `campagna` | 31 | 100,00 | 100,00 | 100,00 | 100,00 | 100,00 | — (classe mista) |
| `documento` | — | — | — | — | — | — | — (norme diverse, ADR-0035) |

⚠️ **Su `arco` la regola «soglia = P10» non si applica, e va detto perché.** La
distribuzione è talmente schiacciata sul 100 che il P10 **è** 100: usarlo
boccerebbe tutta la coda, cioè l'opposto dell'istruzione del DM *«una soglia
ragionevole, per non buttare via nulla»*. La soglia nasce quindi dal **minimo**
misurato, e la stretta successiva è scritta nel file (`prossima_stretta: 95,0`,
che oggi boccerebbe 5 file su 479).

## Conseguenze

- Il cancello `punteggio_mqm.py --soglia` entra in CI ed è **verde alla nascita
  su 515 documenti**.
- Il pass/fail sui critici è **cablato e non scatta mai**, perché nessun
  rilevatore di severità critica esiste: i tre casi (statblocco inventato,
  contraddizione con `state.md`, EL oltre APL+4) vogliono un confronto col
  canone che nessuno script fa. È pronto, non attivo, e il test lo prova su una
  specifica di prova invece di fingere che funzioni sul repo.
- `misura_craft` **resta**: il punteggio affianca, non sostituisce (F3.5).

## Limiti dichiarati

1. **Quattro norme su quaranta.** Il punteggio copre ciò che ha un rilevatore,
   e un documento a 100 può violare trentasei norme che nessuno guarda. Il
   numero non è un giudizio di qualità: è un giudizio di **conformità a ciò che
   si misura oggi**.
2. **Il κ non è misurato.** F3.3 chiede un accordo ≥ 0,6 fra la macchina e il
   DM su un campione, e quel campione costa tempo al DM. Finché non esiste, il
   punteggio è coerente con sé stesso e **non si sa se è coerente col DM**.
   Questa ADR non lo nasconde e non fa finta che un secondo modello basti.
3. **Due difetti trovati nello strumento mentre lo si scriveva**, entrambi
   della famiglia «un criterio che non pesca si traveste da repo pulito»: le
   prime soglie erano **inventate** (scritte prima di eseguire F1.4), e il
   classificatore usava `Path.match`, che confronta solo la coda del percorso —
   **294 documenti su 515 finivano «fuori classe»**, cioè senza soglia, cioè
   non bocciabili. Entrambi hanno ora un test che li riprende.
