# ADR-0036 — Misurare il miglioramento, non lo stato

> **Stato**: accettata · **Data**: 2026-09-03 · **Decide**: G. Samuele (DM)
> **Attua**: `plans/PIANO-PROSA-CHE-NON-SEMBRI-GENERATA.md` lotti E e F
> **Rapporti**: estende ADR-0035 (due prose, due norme). Non lo contraddice:
> lì i documenti hanno soglie assolute che funzionano, qui la prosa di gioco
> mostra perché non ne può avere.

## Il contesto

Un'analisi esterna delle skill di prosa del repo propone cinque estensioni. La
più forte è una misura quantitativa del ritmo — la **burstiness**, cioè la
varianza della lunghezza delle frasi — che l'analisi presenta come *«l'unico
segnale nella letteratura accademica con una definizione statistica precisa»*, e
osserva correttamente che il repo non misura mai il ritmo, solo i costrutti
nominati.

L'osservazione è giusta. La conclusione no, e il repo aveva già in casa la prova.

## La decisione

**Nessuna soglia assoluta sulla prosa di gioco. Si misura la differenza fra due
versioni dello stesso testo.**

`validate_prosa --prima-dopo [--rispetto-a REV]` conta cinque tic — frammenti
brevi, aperture ripetute consecutive, antitesi, trattini, maiuscole d'enfasi — e
dice se una riscrittura li ha tolti o aggiunti.

Della burstiness sopravvive **la sua forma non compressa**: sui file nominati
sulla riga di comando il rapporto stampa sotto il verdetto le lunghezze delle
frasi in ordine di lettura, con media e scarto. È una lente per chi legge, non
una voce del verdetto, e `profilo_lunghezze()` sta fuori da `conta_tic()` come
`burstiness()`.

## Perché: la burstiness dice il contrario del tavolo

`05-ECHI-HELLA.md` esiste in tre versioni, e la terza è stata riscritta il
2026-09-02 e giudicata migliore dal DM.

| versione | burstiness (CV) | frammenti ≤6 parole | aperture ripetute |
|---|---:|---:|---:|
| originale | 0,55 | 2 / 18 | 1 |
| intermedia | 0,52 | 2 / 18 | 1 |
| **riscritta, approvata** | **0,47** | **0 / 18** | **0** |

La burstiness **peggiora** sulla versione giudicata migliore, e il motivo è
strutturale: la riscrittura aveva tolto i frammenti brevi — *«Sono tuoi.»*, *«Non
sai se lui ha sentito.»* — e togliere frammenti riduce la varianza delle
lunghezze. **La metrica premia il tic che §9 vieta.**

Non è un difetto di taratura. Una soglia più bassa non lo aggiusta: la direzione
è sbagliata.

## Le altre due misure assolute, e perché non reggono

**Densità di frasi corte.** Il file peggiore del corpus (75%) è fatto di grida —
*«PORTATORE MALEDETTO!»*, *«ORA IO UCCIDO TE!»* — e di note telegrafiche di
regia — *«Treant lo lancia»*, *«Monaco SPARISCE teleport»*. Nessuna delle due è
il tic narrativo.

**Aperture ripetute.** Tre occorrenze in tutto il corpus. Mediana zero.

## E sui documenti del repo? Provato, e non separa niente

Restava un'obiezione onesta: sulla prosa di gioco la burstiness punta dalla
parte sbagliata *perché* il frammento breve lì è legittimo. Nei documenti il
frammento non è idioma, e il sospetto era l'opposto — paragrafi tutti uguali.
Misurata su 124 documenti, per famiglia:

| famiglia | n | q1 | mediana | q3 |
|---|---:|---:|---:|---:|
| ADR | 28 | 0,58 | 0,68 | 0,73 |
| piani | 28 | 0,63 | 0,70 | 0,91 |
| guide | 8 | 0,51 | 0,59 | 0,74 |
| skill (references) | 57 | 0,58 | 0,66 | 0,79 |

Le quattro bande stanno una sopra l'altra. E agli estremi non separa niente di
sensato: il documento più uniforme è `TOOL-AUTHORING-STANDARD.md` a 0,34, che è
uniforme perché è uno standard; i più «vari» sono tutti references di lore, che
sono schede in prosa travestita.

⚠️ **Un artefatto da tenere a mente se qualcuno rifà il conto.** Contando come fa
`prosa_documento()`, che tiene le voci di elenco perché per la densità del
trattino sono prosa, `spells.md` risultava il file più «vario» del repo con CV
2,51: una lista di incantesimi senza punto finale diventa **una frase da 587
parole**. La tabella qui sopra esclude le voci di elenco. Con dentro, la misura
classifica la sintassi Markdown, non il ritmo.

## Perché invece il confronto funziona

Grida e note di regia ci sono **prima e dopo**, quindi si annullano nella
differenza. Quello che resta è ciò che la riscrittura ha cambiato. Il caso Hella
lo dice in una riga:

```
05-ECHI-HELLA.md: migliorata rispetto a f14f1b8 — frammenti -2, aperture_ripetute -1
```

## Le conseguenze

**Quello che si guadagna.** Una risposta alla domanda che finora non aveva
risposta: *«questa riscrittura è meglio della precedente?»*. E un metro che non
dipende da un giudizio a memoria.

**Quello che si paga.**

- **Il confronto non dice se un testo è buono**, solo se è migliorato. Un testo
  pessimo che peggiora di poco esce «migliorato».
- **Serve una versione precedente.** Su un file nuovo non dice niente.
- **La burstiness resta calcolabile** (`burstiness()`) ma **fuori da
  `conta_tic()`**, di proposito. Serve a poter rifare la verifica, non a
  puntarci. Un test la tiene ferma: se un giorno smettesse di contraddire il
  giudizio del tavolo, quel test cade e la decisione va riesaminata.
- **Il profilo si stampa solo sui file nominati.** Una scansione senza argomenti
  confronta 255 file, e tre righe l'uno sarebbero un muro invece di un rapporto.
- **Il profilo non è un punteggio, e niente impedisce di leggerlo come tale.**
  Chi guarda due sequenze di numeri è tentato di preferire quella più mossa, che
  è esattamente l'errore che questa ADR scarta. La difesa è scritta nel
  docstring e in un test (`test_il_profilo_NON_entra_nel_verdetto`), non nel
  codice: il verdetto resta dei cinque tic.

## Quello che l'analisi ha azzeccato, e che è entrato

Due tic veri che il §9 non aveva, entrambi nella zona dove questo repo scrive di
più — artefatti, luoghi, lignaggi:

- **l'elusione della copula**: *si configura come*, *funge da*, *rappresenta* al
  posto di *è*;
- **l'inflazione di significato**: *testimonianza di*, *segna un punto di
  svolta*, dichiarare l'importanza invece di mostrarla.

Più una **watchlist del registro narrativo italiano**, perché le liste inglesi
(*delve*, *tapestry*) su un corpus italiano non servono.

Stanno in `italiano-nativo.md` §9.2-ter e §9.2-quater come **prescrizione**, non
come controllo: nel repo sono 20, 3 e 22 occorrenze, e buona parte sono
legittime (*«un tesoro che rappresenta il tuo passato»* è italiano corretto,
*«nel cuore della battaglia»* è spaziale). Un gate lì griderebbe al lupo.
