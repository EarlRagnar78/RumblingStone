# Le guide di oggi stanno già in Diátaxis?

Misura del 2026-11-10 su main a f65d78e, prima di decidere se riorganizzare
`docs/`. Standard di fatto candidato: [Diátaxis](https://diataxis.fr/), con
quattro forme. Un **tutorial** insegna facendo, un passo dopo l'altro. Una
**guida pratica** (how-to) risolve un compito a chi sa già. Un
**riferimento** descrive com'è fatta una cosa. Una **spiegazione** dice perché
è fatta così.

## Metodo

Ogni sezione `##` di ogni guida è classificata a mano in una delle quattro
forme. «Dove sta il resto» e gli indici sono navigazione e non contano. Una
guida *sta in Diátaxis* se almeno l'80% delle sue sezioni ha la stessa forma.
La classificazione è a giudizio, non a macchina: chi rifà la misura può
spostare una sezione di confine e cambiare un verdetto di confine (MAPPE,
MARCATURE, SCHEDE-PROMPT), non i casi netti.

Legenda: T tutorial · H guida pratica · R riferimento · S spiegazione.

| Guida | Sezioni | T | H | R | S | Forma prevalente | Quota | Verdetto |
|---|---:|---:|---:|---:|---:|---|---:|---|
| GUIDA-SETUP-MACCHINA | 9 | 6 | 2 | 1 | 0 | tutorial | 67% | mista |
| GUIDA-BESTIARIO | 13 | 0 | 6 | 6 | 1 | pratica = riferimento | 46% | mista |
| GUIDA-BOOKLET-E-PDF | 11 | 0 | 6 | 3 | 2 | pratica | 55% | mista |
| GUIDA-MAPPE | 9 | 0 | 7 | 0 | 2 | pratica | 78% | mista (al confine) |
| GUIDA-IMMAGINI | 7 | 0 | 6 | 0 | 1 | pratica | 86% | **sta** |
| GUIDA-PATCH-RAMO-DI-GRUPPO | 5 | 0 | 4 | 1 | 0 | pratica | 80% | **sta** |
| GUIDA-CONDIVISIONE-IP | 8 | 0 | 4 | 1 | 3 | pratica | 50% | mista |
| RILASCIO | 7 | 0 | 5 | 1 | 1 | pratica | 71% | mista |
| GUIDA-MARCATURE | 4 | 0 | 0 | 3 | 1 | riferimento | 75% | mista (al confine) |
| GUIDA-SCHEDE-PROMPT | 4 | 0 | 0 | 3 | 1 | riferimento | 75% | mista (al confine) |
| TOOL-AUTHORING-STANDARD | 11 | 0 | 1 | 9 | 1 | riferimento | 82% | **sta** |
| LEGENDA-FUNZIONALE-SPEC | 7 | 0 | 0 | 3 | 4 | spiegazione | 57% | mista |
| GUIDA-FLUSSO-LOCALE | 8 | 0 | 1 | 0 | 7 | spiegazione | 88% | **sta** |
| ARCHITETTURA | 19 | 0 | 0 | 0 | 19 | spiegazione | 100% | **sta** |

**Risultato: 5 guide su 14 stanno già in una forma sola; 9 sono miste.**

## Cosa mescolano

- Le «Guida completa» (BESTIARIO, BOOKLET, MAPPE) mettono insieme la ricetta
  (H) e il formato dei file (R). È il caso che Diátaxis chiede di separare.
- Quasi tutte chiudono con un «Perché così» (S). Il danno è piccolo: il perché
  è una sezione in fondo, e chi cerca la ricetta non ci inciampa.
- Le due di fine ottobre e novembre (MARCATURE, SCHEDE-PROMPT) sono già quasi
  riferimento puro.

## Quanto costerebbe riorganizzare

- `docs/guides/` ha 12 file. Le guide sono citate da 61 file Markdown fuori da `docs/`:
  skill, AGENTS.md, piani e ADR. I numeri si rifanno con
  `grep -rl "docs/guides/" --include=*.md . | grep -v '^./docs/' | wc -l`.
  Spezzare BESTIARIO, BOOKLET e MAPPE in pratica + riferimento vuol dire sei
  file al posto di tre e rimandi da correggere in tutti quei file.
- `validate_docs.py` controlla che i link non siano rotti, quindi un errore si
  vede in CI. Il costo vero è la revisione, non il rischio.

## Raccomandazione (va a Jfs con una card)

Diátaxis entra come **regola per le guide nuove e come etichetta nell'indice**,
non come spostamento di file. In concreto:

1. `docs/INDEX.md` scrive accanto a ogni guida la sua forma prevalente. Chi
   cerca una ricetta sa dove andare, e le guide miste lo dichiarano.
2. Le guide nuove nascono in una forma sola. La prima è quella dei sistemi di
   gioco: una guida pratica d'uso e un riferimento per chi scrive un plugin.
3. Una guida mista si spezza solo quando la si tocca per altro, con i rimandi
   corretti nella stessa PR.

Alternative valutate: (B) riorganizzare subito `docs/` in quattro cartelle,
più pulito ma con 61 file da ricontrollare e nessun difetto misurato che lo
chieda; (C) niente Diátaxis, che però lascia senza regola le guide nuove.

## Dopo la riorganizzazione (ADR-0123, rimisurata il 2026-11-12)

Il DM ha scelto l'alternativa B. Stesso metodo e stesso criterio (80% delle
sezioni in una forma), sui file delle quattro cartelle. Le sezioni ridotte a
un rimando contano come navigazione. Classificazione a giudizio come sopra.

| | Prima (main f65d78e) | Dopo (questo ramo) |
|---|---:|---:|
| File di documentazione | 14 | 21 (5 nuovi dalle divisioni, 2 nuovi del 10/11) |
| In una forma sola | 5 (36%) | 15 (71%) |
| Misti | 9 | 6 |
| Link e percorsi rotti (`validate_docs --sorgenti`) | 0 | 0 |
| Ancore `#…` verso file del repo, rotte | 0 su 2 | 0 su 20 |

**Restano misti, e lo si dichiara:**

- `tutorials/GUIDA-SETUP-MACCHINA` (67% tutorial): la parte «cosa serve» è
  riferimento e il «se qualcosa non funziona» è guida pratica;
- `how-to/RILASCIO` (71%): «I numeri» è riferimento;
- `reference/GUIDA-MARCATURE` e `reference/GUIDA-SCHEDE-PROMPT` (75%): un
  «Perché così» in fondo;
- `reference/LEGENDA-FUNZIONALE-SPEC`: i confini di licenza e i limiti
  dichiarati sono fra riferimento e spiegazione;
- `reference/RIFERIMENTO-MAPPE`: dentro il tema texture c'è una ricetta «Da
  zero, in ordine».

Per la regola 2 di ADR-0123 si spezzano quando si toccano per altro. Nella
prima misura la §5 di GUIDA-MAPPE era contata come guida pratica: rileggendola
per spostarla, è soprattutto la descrizione dei formati e dei temi, quindi è
andata nel riferimento. È un caso di confine, come la misura aveva avvertito.
