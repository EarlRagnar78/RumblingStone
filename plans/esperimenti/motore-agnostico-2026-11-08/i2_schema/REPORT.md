# I2 · Schema dei file del plugin (2026-11-08)

**La domanda.** Con quale strumento si controllano i TOML dei plugin, cioè `sistemi.toml`, `sistema.toml` e i file di dati `pe`, `incontri` e `stampa`? Il controllo deve prendere i difetti prima che arrivino al tavolo, dare un messaggio che dica dove sta l'errore e girare dentro la skill impacchettata, senza `pip`.

**Come si rifà.** Lo script è `banco_schema.py`, in questa cartella. Va lanciato in un ambiente a parte con `pip install jsonschema pydantic fastjsonschema datamodel-code-generator tomli-w`. Gli schemi stanno in [`schemi/`](schemi/), i dati grezzi in [RISULTATI.json](RISULTATI.json). Le mutazioni non usano numeri casuali: sono sempre le stesse e sempre nello stesso ordine. Due esecuzioni hanno dato file identici byte per byte (`cmp`).

## Il metodo

Il banco produce 503 difetti di sette tipi sui 9 file veri dei plugin dnd35, pf1e e d20, più `sistemi.toml`:

| Tipo | Difetto |
|---|---|
| togli | chiave obbligatoria tolta |
| refuso | nome di chiave sbagliato, compreso `dati` scritto `dato` |
| tipo | tipo sbagliato: stringa al posto di un intero, intero al posto di una stringa, stringa al posto di una lista |
| valore | valore fuori dominio, cioè −7 o `inesistente` |
| estranea | chiave in più |
| ordine | soglie dei PE scambiate |
| vuoto | lista obbligatoria vuota |

Su ogni difetto girano quattro validatori, in un repo temporaneo costruito come in `test_sistemi_prova_del_nove`:

- **attuale**: `sistemi.problemi()` più gli strumenti che leggono il file (`soglie_di`, `combinatore`, `etichette`);
- **jsonschema** 4.26.0: gli schemi JSON Schema 2020-12 di questa cartella;
- **fastjsonschema** 2.21.1: gli stessi schemi dichiarati come bozza 7;
- **pydantic** v2.14: modelli rigidi più i validatori che una regola sola non sa scrivere.

Per ogni difetto il banco registra tre cose:

- l'esito: **presa** se c'è un messaggio, **crash** se esce un traceback, **sfuggita** se non succede niente;
- se il messaggio nomina la chiave sbagliata;
- se i file veri passano senza falsi allarmi.

## I risultati

| Validatore | Prese su 503 | Crash | Sfuggite | Messaggio che nomina la chiave | Falsi allarmi sui file veri | Si porta dentro il pacchetto |
|---|---|---|---|---|---|---|
| attuale (`problemi()` più gli strumenti) | 123 (24,5%) | **77** | **303** | 82 | 0 | sì, è già codice nostro |
| jsonschema 4.26.0 | 492 (97,8%) | 0 | 11 | 492 | 0 | **no**: dipende da `rpds-py`, compilato in Rust |
| **fastjsonschema 2.21.1** (stessi schemi) | **492 (97,8%)** | 0 | 11 | 488 | 0 | **sì**: puro Python, BSD-3, 0 dipendenze, 1.829 righe |
| pydantic v2.14 | 496 (98,6%) | 0 | 7 | 496 | 0 | **no**: `pydantic_core` è compilato |

Prese per tipo:

| Validatore | togli | refuso | tipo | valore | estranea | ordine | vuoto |
|---|---|---|---|---|---|---|---|
| attuale | 28/35 | 37/44 | 46/217 | 6/122 | 5/56 | 0/4 | 1/25 |
| jsonschema | 35/35 | 44/44 | 217/217 | 116/122 | 55/56 | 0/4 | 25/25 |
| fastjsonschema | 35/35 | 44/44 | 217/217 | 116/122 | 55/56 | 0/4 | 25/25 |
| pydantic | 35/35 | 44/44 | 217/217 | 117/122 | 54/56 | 4/4 | 25/25 |

## Cosa dicono i numeri

**Oggi un plugin sbagliato passa quasi sempre.** Il controllo attuale guarda la struttura di `sistema.toml`. Sui file di dati non controlla niente: `pe.toml`, `incontri.toml` e `stampa.toml` si leggono solo quando uno strumento li usa. Su `pe.toml` prende 5 difetti su 183. Nei 77 crash il DM vede un `TypeError` o un `ValueError` di Python al posto di un messaggio, per esempio quando una soglia diventa la stringa `"dodici"`. In più `problemi()` va in crash se l'id di un plugin diventa un intero, perché `sorted()` mescola chiavi stringa e chiavi intere.

**jsonschema e fastjsonschema prendono esattamente gli stessi difetti.** Delle 11 sfuggite, 5 sono regole che JSON Schema non sa scrivere:

- in `sistemi.toml` il `predefinito` deve stare fra gli `attivi`;
- le soglie dei PE devono crescere, e questo conta 4 casi.

Il codice attuale sa già fare il primo controllo. Il secondo va aggiunto. Le altre 6 sfuggite non sono difetti veri: un livello di difficoltà PF1e in più, o uno scarto di −7 al posto di −1, sono dati strani ma legali, e nessuno schema li deve rifiutare.

**Pydantic prende 4 casi in più**, cioè l'ordine delle soglie. Quella regola però è codice Python dentro il modello. Uno schema JSON più quella stessa riga di codice fa lo stesso lavoro.

**La prima versione degli schemi aveva due buchi**, uguali in tutti e due gli strumenti:

- `difficolta` accettava qualsiasi oggetto;
- `opzioni.pf1e` accettava qualsiasi chiave.

Il primo giro prendeva 484 difetti con JSON Schema e 489 con pydantic. Ho chiuso i buchi in tutti e due e ho rimisurato, come chiede la regola della configurazione rigorosa. I numeri della tabella sono quelli del secondo giro.

## La scelta, con la regola dello standard di fatto

- **Lo standard di fatto per descrivere file di configurazione è JSON Schema.** Lo usano taplo ed Even Better TOML negli editor, SchemaStore, Kubernetes e OpenAPI. È un file di dati: sta nel plugin accanto ai TOML, e un sistema nuovo porta il suo schema senza toccare il nucleo, come chiede ADR-0112. La misura non lo boccia: 97,8% delle prese, 0 falsi allarmi, il percorso della chiave nel messaggio.
- **Pydantic è bocciato** per il motore. Ha 4 prese in più, ma sono una regola che si scrive anche accanto a JSON Schema. Ha un modulo compilato che non si porta nella skill. E lo schema diventa codice Python invece di un dato del plugin.
- **Il validatore dentro la skill è fastjsonschema**, portato dentro il pacchetto con versione 2.21.1 e sha256 `c9e5b7e9…554667` del wheel. È l'unica implementazione misurata che sia puro Python, e prende esattamente quello che prende `jsonschema`. Il suo limite è che conosce solo fino alla bozza 7. Gli schemi quindi si scrivono con le parole della bozza 7, che restano valide nella 2020-12.
- **In CI gira anche `jsonschema`**, l'implementazione di riferimento, che controlla che gli schemi stessi siano validi. Lì il pacchetto non conta.
- **Le due regole che uno schema non esprime** (predefinito fra gli attivi, soglie crescenti) restano codice in `sistemi.py --check`, con un messaggio.

## Aggiunta del 2026-11-08: pydantic che legge i dati del plugin

**La domanda del DM.** Il nucleo compilato di pydantic potrebbe leggere gli schemi del plugin invece di avere modelli scritti a mano? Migliorerebbe qualcosa rispetto allo standard del repo?

**Come l'ho misurato.** Ho generato i modelli pydantic dagli stessi JSON Schema del plugin con [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) 0.91.0 (MIT), lo strumento standard di fatto per passare da JSON Schema a pydantic. Sono 282 righe di modelli generati, nessuna scritta a mano. Poi li ho fatti girare sugli stessi 503 difetti; nel banco è il validatore `ConPydanticDaSchema`. Il tempo l'ho misurato a parte, con la mediana di 200 validazioni per file, perché cambia da una macchina all'altra e non può entrare in RISULTATI.json.

| Validatore | Prese su 503 | Messaggio che nomina la chiave | Falsi allarmi | Tempo per un file | Da portare nel pacchetto |
|---|---|---|---|---|---|
| fastjsonschema (stessi schemi) | 492 | 488 | 0 | 11,1 µs | 1 file wheel universale, puro Python |
| **pydantic generato dagli schemi** | **492** (gli stessi 492) | **470** | 0 | 3,7 µs | `pydantic` (4,2 MB) più un `pydantic_core` compilato per ogni sistema operativo, processore e versione di Python (2,2 MB il solo wheel `cp313-win_amd64`) |
| pydantic scritto a mano | 496 | 496 | 0 | 5,0 µs | come sopra |
| jsonschema | 492 | 492 | 0 | 164,6 µs | `rpds-py` compilato |

**Cosa dicono i numeri.**

- Quando legge i dati del plugin, pydantic prende **esattamente gli stessi difetti** di JSON Schema. Il motivo è che applica le stesse regole, scritte nello schema.
- I 4 difetti in più del pydantic scritto a mano (le soglie che devono crescere) vengono da una riga di codice, non dal nucleo compilato. Quella riga si può mettere anche accanto a JSON Schema.
- I messaggi sono un po' peggiori: in 22 casi il messaggio non nomina la chiave sbagliata. Succede perché il modello generato traduce i nomi (per esempio `Capacita1`, `PeSoglie`).
- Pydantic è circa 3 volte più veloce di fastjsonschema. Qui però si validano 9 file una volta per esecuzione, cioè circa 0,1 ms in tutto, quindi il guadagno non si vede.
- Il costo invece si vede. La skill dovrebbe portarsi un `pydantic_core` compilato per ogni piattaforma. Il wheel `cp313` vale solo per Python 3.13, quindi va rifatto a ogni versione di Python. Il modello iemod-fetch porta solo puro Python proprio per evitarlo.

**Conclusione.** Pydantic è lo standard di fatto per i modelli dei dati *dentro* un'applicazione Python, per esempio in FastAPI. Per lo schema di un *file di configurazione* lo standard di fatto è JSON Schema: è indipendente dal linguaggio, gli editor lo leggono, e pydantic stesso lo esporta. La misura dice che pydantic, alimentato con i dati del plugin, non prende un difetto in più e ha un costo di pacchetto che il puro Python non ha. Quindi resta la scelta di prima: lo schema JSON nel plugin e fastjsonschema nella skill.

**Da rivedere se** la validazione diventa un costo che si vede (migliaia di file per esecuzione), oppure se la skill smette di dover girare senza `pip`.

## Proposta per F3

1. Ogni plugin ha accanto ai suoi dati uno `schemi/<file>.schema.json`. Il nucleo ha solo quello di `sistema.toml` e quello di `sistemi.toml`.
2. `sistemi.py --check` e il caricamento di un plugin validano ogni file prima di usarlo. In questo modo i 77 crash diventano messaggi. Il criterio di uscita è 0 crash sul banco di mutazione.
3. Il banco diventa un test, con un cricchetto: le prese non scendono sotto 492 su 503.
4. Lo schema si esporta anche per taplo, così nell'editor il DM vede l'errore mentre scrive.

**Da rivedere se** un sistema futuro ha bisogno di regole fra campi diversi che non si scrivono in bozza 7, oltre alle due di oggi. In quel caso si rimisura la bozza 2020-12, che oggi va solo con `jsonschema`, compilato, o con un'implementazione pura nuova.
