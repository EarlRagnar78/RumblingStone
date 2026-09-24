# ADR-0067 — Il confine dichiarato fra il codice e l'LLM

- **Stato**: accettata
- **Data**: 2026-09-16
- **Numero**: nata come ADR-0050 nella PR #143 (bozza, mai mergiata);
  rinumerata al porto su `main` il 2026-09-24, perché nel frattempo 0050 era
  stato assegnato a [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md)
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: risposta del DM alla domanda 1 di
  [PIANO-PIPELINE-IBRIDE-GROUNDING-E-MISURA](../PIANO-PIPELINE-IBRIDE-GROUNDING-E-MISURA.md)
  §0.3, sul documento esterno del 2026-09-16
- **Rapporti**: applica ad_hoc la ragione di
  [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (offline la sera della
  sessione) al caso che ADR-0037 non aveva previsto, cioè una dipendenza che non
  è una libreria ma un servizio. Eredita il modello di sicurezza di
  [ADR-0030](ADR-0030-server-mcp-sui-tool.md) e la clausola sui pesi di
  [ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md)

## Contesto

Un documento esterno consegnato dal DM il 2026-09-16 propone di far chiamare un
modello linguistico **dagli script**: un router che smista le richieste, un
generatore narrativo e un direttore di stile in parallelo, un critico a
temperatura zero che scarta i blocchi incoerenti, un decoratore che arreda le
stanze di una mappa.

Oggi nessuno script di questo repo chiama un modello linguistico. La misura del
2026-09-16: **52 script Python** in `scripts/`, **12 moduli** in
`scripts/dmcore/`, **23.371 righe**, e un solo file che apre un socket —
`scripts/comfyui_batch.py`, verso `http://127.0.0.1:8188`, per le immagini.
L'LLM in questo repo è un **client**: legge le skill, chiama i tool attraverso
il server MCP, e ciò che produce passa dai gate.

La proposta non è assurda, ed è già in casa per le immagini. Il punto è che il
confine non era mai stato scritto, e senza una riga che lo fissi la domanda
torna a ogni piano, come è tornata quella delle librerie fino ad ADR-0037.

## La decisione

**Gli script del repo restano deterministici, stdlib e offline. Una chiamata a
un modello vive solo in uno script-ponte dichiarato, che è opzionale, degrada
pulito senza rete e non è mai un passo bloccante della CI.**

Un ponte deve rispettare tutte le condizioni che seguono. Non sono
raccomandazioni: uno script che ne violi una non è un ponte, è una dipendenza di
rete infilata nella catena.

1. **Nessun'altra catena lo attraversa.** Nessuno script deterministico importa
   un ponte né lo invoca. Il ponte produce un file, e il file entra nella catena
   dalla porta normale (il contratto JSON, il master markdown, la scheda).
2. **Degradazione scritta.** Senza rete, senza chiave o senza servizio, il ponte
   stampa cosa manca ed esce con un codice non zero. Mai una traccia di stack,
   mai un output parziale scritto su disco.
3. **In CI solo ciò che gira senza il servizio.** `--help`, `--dry-run`, la
   composizione del prompt, la validazione dell'output contro lo schema. Il
   precedente è `comfyui_batch.py`: la CI ne prova sei invocazioni e nessuna
   tocca il servizio.
4. **L'output è un candidato, non un artefatto.** Ciò che torna da un modello
   passa per un validatore deterministico prima di diventare un file del repo.
   Se il validatore boccia, il ponte non riprova in silenzio: riporta l'errore.
5. **Le difese di ADR-0030.** Nessuna shell, argomenti come lista, percorsi
   confinati sotto la radice del repo, nessuna scrittura di canone (ADR-0007: il
   canone si scrive su un branch di gruppo, col diff sotto gli occhi del DM).
6. **Il modello si dichiara.** Nome, versione e chi lo serve stanno nel manifest
   dei tool, come `external_bins` dichiara i binari. Un modello che cambia sotto
   i piedi è la stessa classe di problema del `typst` a «latest» di ADR-0020 §3.
7. **I termini si guardano prima.** ADR-0019 vale per i pesi locali; per un
   servizio remoto vale il suo contratto d'uso, e va verificato sulla fonte
   primaria prima che il ponte entri nel repo.

## Perché non le altre due strade

**L'LLM dentro gli script** costa il determinismo, ed è la proprietà su cui
questo repo ha costruito tutto il resto: `test_determinism.py`, il piano di
scena 3D confrontato byte a byte su due giri in CI, i **742 test** che girano in
quindici secondi senza rete. Una catena che passa da un modello non si può
confrontare con `cmp`, e i gate che oggi mordono smetterebbero di poterlo fare.

**Il divieto assoluto** avrebbe mentito su un fatto già vero: `comfyui_batch.py`
esiste, chiama un servizio, e nessuno lo considera un'anomalia. Una regola che
il repo viola già il giorno in cui la scrive non regge un mese.

## Conseguenze

**Diventa più facile** dire di sì a una proposta come quella del documento senza
riaprire ogni volta la discussione sulle dipendenze: la domanda diventa «rispetta
le sette condizioni?», che ha una risposta verificabile.

**Diventa più difficile** costruire una catena a più passi di modello. Un ponte
produce un candidato e si ferma; una pipeline «generatore → critico → mixer»
sono tre ponti, tre file intermedi e tre validazioni, e il costo si vede. Questo
è voluto: rende visibile il prezzo di un'architettura che il documento sorgente
presentava come gratuita.

**Va rivisitata** il giorno in cui un ponte esiste davvero e il DM lo usa per una
sessione vera. Finché nessuno l'ha costruito, le sette condizioni sono
un'ipotesi ragionata, tarata su un precedente solo. La prova è il lotto E del
piano, e la riga di quel lotto in `plans/CHANGELOG.md` dirà quale condizione ha
retto e quale no.
