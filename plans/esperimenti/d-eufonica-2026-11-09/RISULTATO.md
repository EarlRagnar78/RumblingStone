# La *d* eufonica: LanguageTool contro la regex del repo (2026-11-09)

> Misura per CODA D3 (norma decisa dal DM il 2026-11-08). Script: `misura.py`,
> che chiede a un **LanguageTool locale** (`scripts/avvia_languagetool.sh`, mai
> l'API pubblica) le segnalazioni della regola **ST_03_001** su ogni file di
> contenuto e le confronta, riga per riga, con `validate_lingua.d_eufonica_righe`.
> Si rifà con `python3 plans/esperimenti/d-eufonica-2026-11-09/misura.py http://127.0.0.1:8081`.

## Perché LanguageTool è il riferimento

È lo standard di fatto del controllo dell'italiano (LGPL), e la sua regola
ST_03_001 dice la stessa cosa della norma: *ad* ed *ed* davanti alla stessa
vocale, *a* ed *e* davanti alle altre. Accetta *ad esempio* e *ad es.*, e boccia
anche *ad eccezione*, *ad oggi*, *fino ad ora*. Non può stare nel cancello di CI
così com'è: vuole Java e un server di circa 200 MB, e la CI del repo è stdlib più
pochi pacchetti (ADR-0037). Da qui una regex del repo, **tarata su LanguageTool**,
come per l'apostrofo di ADR-0079.

## Esito

| Giro | Concordi | Solo LanguageTool | Solo regex |
|---|---:|---:|---:|
| Prima taratura (una riga alla volta) | 45 | 36 | 1 |
| Corsivo fra le parole e congiunzione a capo | 53 | 28 | 2 |
| **Dopo la correzione dei testi** | **0** | **26** | **0** |

Dopo la correzione restano **26 segnalazioni di LanguageTool, tutte fuori norma
per scelta o falsi positivi**:

- **«o o…» (17)**: LanguageTool propone *od*. Fuori norma: *od* è arcaico, e la
  norma del DM tocca solo *a/ad* ed *e/ed*.
- **lettere-etichetta (9)**: *Unità A attacca*, *Appendice A*, *§7.E*, *N, E e O*,
  *A/B/C/D/E*, *Squares A*. Sono nomi, non preposizioni né congiunzioni.

Le **due forme che solo la regex vedeva** erano errori veri che LanguageTool
perde: *comune e élfico* (Lythiel) e *tutto e **è sparita*** (Mira Serani): la
regex conta le vocali accentate e salta il grassetto.

Un caso solo di LanguageTool era vero e la regex non poteva vederlo: *intuizione
a⏎Artigianato* nelle due copie della guida della Corona, dove la riga dopo è
rientrata di quattro spazi e il validatore la tratta come codice. Corretto a mano.

## Cosa è stato corretto

58 righe in 42 file (due a mano), tutte con la forma della norma:
*legato ad Aegis Fang*, *ad attacchi*, *ed equipaggiamento*, *a ogni*, *a oggi*,
*a un*, *e indifesa*, *ed **è***. Nei titoli tutti maiuscoli la *d* è maiuscola
(*CAOS ED EROISMO*).

## Limiti onesti

- La regex non sa se una *a* è preposizione o lettera: le etichette maiuscole si
  salvano con un filtro di forma (*A* seguita da maiuscola sola), una *a*
  minuscola usata come etichetta sarebbe un falso positivo.
- Le righe trattate come codice (rientro di quattro spazi) non si controllano.
- Nei testi tradotti dall'inglese resta qualche *Ed* iniziale che LanguageTool
  e la regex accettano perché la norma lo vuole.
