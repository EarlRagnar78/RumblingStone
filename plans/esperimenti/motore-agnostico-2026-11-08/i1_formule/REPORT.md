# I1 — Quale linguaggio per le formule d20 (2026-11-08)

**Domanda**: con quale motore di espressioni le formule del sistema (oggi funzioni Python in `dmcore`) possono stare nei file del plugin, senza perdere correttezza né sicurezza, e restando impacchettabili nella skill come in iemod-fetch?

**Come si rifà**: `banco_formule.py` in questa cartella, con le librerie installate in un ambiente a parte (`pip install simpleeval asteval cel-python common-expression-language`). I dati grezzi sono in [RISULTATI.json](RISULTATI.json). Domini e casi sono fissi; cambia da una macchina all'altra solo la colonna dei microsecondi.

## Risultato (Python 3.13.18)

| Motore | Formule giuste (7, 598 casi) | Formule riscritte per il dialetto | Ostili non rifiutate (su 50) | Deterministico | µs per valutazione | Impacchettabile |
|---|---|---|---|---|---|---|
| `ast` della libreria standard, lista bianca (controllo, codice nostro) | 7/7 | 0 | **0** | sì | 4,2 | sì: niente da portare |
| **simpleeval 1.0.8 ristretto** (solo la sua API pubblica: nodi e operatori aritmetici, risultato intero) | 7/7 | 0 | **0** | sì | 13,3 | **sì: un file di 1.024 righe, MIT, 0 dipendenze** |
| simpleeval 1.0.8 come esce | 7/7 | 0 | 4 (`x = 1`, f-string, `'%s' % dv`, `dv.real`) | sì | 11,3 | sì |
| asteval 1.0.10 (`minimal=True`, senza import) | 7/7 | 0 | **10**, fra cui **`open('/etc/passwd')` che apre il file** e `sum(range(10**12))` che non termina | sì | 31,1 | sì |
| cel-python 0.5.0 (CEL puro Python) | 7/7 | **6 su 7** | 1 (`'%s' % dv` dà 3) | sì | 199,5 | **no**: 7 dipendenze, fra cui `google-re2` e `pendulum` compilate |
| common-expression-language 0.10.0 (CEL in Rust) | 7/7 | **6 su 7** | 0 | sì | 9,5 | **no**: modulo compilato per piattaforma, più 4 dipendenze da riga di comando |

**La trappola di CEL, misurata.** CEL non ha la divisione intera arrotondata in basso (`//`): la sua `/` fra interi **tronca verso zero**. Il d20 arrotonda in basso. Scritta alla lettera, `(punteggio - 10) / 2` sbaglia **5 casi su 61** (For 1, 3, 5, 7, 9: modificatore −4 invece di −5, e così via), e lo fa in silenzio. Per essere giusta in CEL va scritta `punteggio >= 10 ? (punteggio - 10) / 2 : -((11 - punteggio) / 2)`. CEL non ha nemmeno `max`, quindi 6 formule su 7 cambiano forma rispetto al manuale.

## Lettura

- **CEL è lo standard di fatto per le regole in configurazione** (Kubernetes, Envoy, Firebase), e il criterio di Jfs parte da lì. Qui però non passa due criteri. Non è impacchettabile: nessuna delle due implementazioni Python è puro Python senza dipendenze compilate. E la sua aritmetica intera non è quella del d20: costringe a riscrivere le formule del manuale in una forma dove un errore resta muto.
- **simpleeval è la libreria Python più diffusa e longeva per questo problema**: un file solo, MIT, nessuna dipendenza. Come esce lascia passare cose innocue ma fuori tema. Ristretta con la sua API pubblica (`nodes` e `operators`), rifiuta tutte e 50 le ostili e dà gli stessi numeri del codice di oggi su tutti i 598 casi. Le formule restano scritte come nel manuale (`2 + dv // 2`).
- **asteval è da escludere**: anche nella configurazione minima apre file e accetta cicli che non terminano.
- Il valutatore nostro su `ast` passa tutto ed è il più veloce. Per la regola del DM del 2026-11-08, però, si parte dallo standard quando lo standard passa la misura, e simpleeval ristretto la passa. Il nostro resta come **controllo** nel banco.

## Proposta per F3

1. Le formule nei TOML del plugin si valutano con **simpleeval ristretto**, portato dentro il pacchetto (versione 1.0.8 e sha256 fissati, licenza MIT scritta), come iemod-fetch fa con le sue due librerie.
2. Al caricamento del plugin, `sistemi.py --check` analizza ogni formula una volta. Se ci sono un nome che la formula non dichiara o un nodo fuori lista, il plugin si ferma in CI e non al tavolo.
3. Il banco delle formule di §3 del piano diventa un test: ogni formula del plugin d20 deve dare lo stesso numero della funzione che sostituisce, su tutto il dominio.

**Da rivedere se** una formula di un plugin futuro ha bisogno di qualcosa che simpleeval ristretto rifiuta (decimali, tabelle dentro l'espressione). In quel caso la regola va in un modulo di codice del plugin (F5) e non si allarga la lista bianca.
