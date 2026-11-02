# ADR-0103 — Le regole dei master si riscontrano sull'SRD scaricato in cache

**Stato**: proposta, in canale testing (ADR-0099); la promozione a stable chiede l'ok del DM
**Data**: 2026-10-23
**Decisione-fonte**: il DM (Jfs), 2026-10-23: *«aggiungi se ci sono tools skills pipeline plugin e tools che non sono presenti nel repo aggiungili ed integrali così come per tutti gli altri strumenti in un flusso coerente e con architetture di casi d'uso tipo Sourcery AI e spiegazione di architettura software e documentazione»*. Il solo candidato che la ricerca del giorno stesso ([RICERCA](../esperimenti/ricerca-rete-2026-10-23/RICERCA.md) §3) raccomanda di adottare.
**Rapporti**: applica [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (entra in testing); rispetta [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (stdlib, pyyaml facoltativo per il YAML); tiene fuori dal repo i testi di terzi come la skill di scrittura italiana di [ADR-0097](ADR-0097-scrittura-italiana-entra-come-eccezione.md); si aggiunge ai controlli di qualità di [ADR-0095](ADR-0095-il-giro-ha-correzione-verifica-e-seconda-passata.md) e [ADR-0098](ADR-0098-la-qualita-delle-mappe-si-misura-con-uno-standard.md).

## Contesto

I master dicono «SRD» molte volte: DEF-1 e DEF-2 di ARC-08 lo nominano 55
volte, quasi sempre accanto a un numero (un raggio in metri, una CD, i pf di
una creatura). Fino a oggi quei numeri li controllava un lettore a memoria. Il
giro della Sessione 2 ne ha segnati nove come «a memoria», e il triage ne ha
accettato uno sbagliato: la *freccia assassina* che fa «50 danni» per l'SRD
3.5, quando i 50 danni sono la regola di Pathfinder e il 3.5 dice «save or
die».

La ricerca in rete del 2026-10-23 ha trovato due archivi aperti che si
leggono con la libreria standard: l'SRD 3.5 in Markdown
([olimot/srd-v3.5-md](https://github.com/olimot/srd-v3.5-md), 86 file, 7,5 MB)
e il PRD di Pathfinder 1e in SQLite
([devonjones/PSRD-Data](https://github.com/devonjones/PSRD-Data), un database
per manuale, 44 MB senza l'indice). Entrambi sono Open Game Content sotto OGL
1.0a. La prova ha riscontrato le nove regole in 0,04 s.

I siti dell'SRD (d20srd.org, aonprd.com) sono bloccati dal proxy di queste
sessioni (RICERCA §6); `raw.githubusercontent.com` no, e in CI GitHub è
sempre raggiungibile.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Uno script che scarica le due fonti a commit fissato, file per file con lo sha256, in una cache fuori dal repo** (scelta) | il repo non contiene testi di terzi; la fonte è la stessa su ogni macchina e in CI; uno sha256 diverso ferma tutto | 50 MB al primo uso; serve la rete una volta; il file dei riscontri si scrive a mano |
| Mettere l'SRD nel repo con il testo della OGL | niente rete, mai | la OGL lo permetterebbe, ma la regola del repo per i testi di terzi è tenerli fuori (ADR-0097); 50 MB di storia git per sempre |
| `git clone` dei due repo, come nella prova | il comando che tutti conoscono | il commit si fissa, ma lo sha256 del singolo file no; 277 MB per PSRD-Data con le cartelle JSON che non servono |
| Leggere d20srd.org o aonprd.com a ogni controllo | sempre aggiornato | bloccati qui; nessuna garanzia che il testo resti uguale; HTML da raschiare |
| Continuare a controllare a memoria | nessun lavoro | è il modo che ha fatto passare la freccia sbagliata |

## Decisione

1. **`scripts/riscontro_srd.py`** con quattro comandi: `scarica` (anche
   `--da-cartella` da un clone locale e `--verifica`), `regola NOME`,
   `riscontra FILE`, `licenza`. Le fonti sono fissate nel codice: repository,
   commit e sha256 di ogni file. La cache sta in `--cache`, oppure in
   `$RUMBLINGSTONE_SRD_CACHE`, oppure in `~/.cache/rumblingstone/srd/`.
2. **Il riscontro è un file**, YAML o JSON, con una voce per regola: la regex
   nella fonte, quella nel master, e il confronto. `numero` moltiplica il
   valore della fonte per una scala (0,3 dai piedi ai metri, 9 dalla categoria
   d'età al raggio della presenza terrificante); `termine` confronta due
   parole con un elenco di equivalenze (`die` ↔ `muore`); `presenza` dice solo
   che la regola e l'affermazione esistono. Gli esiti sono concorda,
   discorda, non trovata, con file e riga di tutte e due le parti.
3. **Il primo file è quello di ARC-08**,
   `plans/esperimenti/ricerca-rete-2026-10-23/riscontri-arc08.yaml`: le regole
   numeriche di DEF-1 e DEF-2 che lo script sa controllare. Il rapporto è
   [RISCONTRO-ARC08](../esperimenti/ricerca-rete-2026-10-23/RISCONTRO-ARC08.md).
   I master non si correggono qui: le discordanze le decide il DM.
4. **Canale testing con un job CI non bloccante**, `riscontro-srd`. La rete
   in CI c'è, e senza un job lo strumento non accumulerebbe i 10 run che
   ADR-0099 chiede per salire. Il job scarica le fonti, esegue il file di
   ARC-08 e scrive la tabella nel riepilogo del run. Non usa `--strict`,
   perché una discordanza aperta è una domanda per il DM e non un guasto:
   diventa rosso solo se lo strumento si rompe (1 per uno sha256 sbagliato, 2
   per un file dei riscontri rotto, 3 per la rete). Niente `actions/cache`:
   sarebbe un'azione di terzi in più, e 50 MB da `raw` costano pochi secondi.
5. **La rete che manca si dice.** Senza cache e senza rete lo script esce 3,
   nomina il file che non è arrivato e suggerisce `--da-cartella`. `--offline`
   vieta di scaricare e dà lo stesso codice.
6. **La licenza si dichiara a ogni uscita.** Ogni rapporto termina con la
   riga OGL di ciascuna fonte usata; `licenza` dice dove sta il testo completo
   nella cache.

## Conseguenze

- Il giro dei lettori ha un passo in più: un rilievo segnato «a memoria» si
  scrive come voce di un file di riscontri prima del triage. La misura che
  la ricerca proponeva vale ancora: rilievi «a memoria» aperti dopo il triage
  e discordanze trovate.
- Il primo riscontro di DEF-1 e DEF-2 (53 voci, 0,1 s) ne trova tre
  discordanti: la freccia assassina di DEF-2 e, in DEF-1, due volte il raggio
  della presenza terrificante calcolato per un drago «adulto» (54 m) quando
  Fauci, per canone, è un adulto maturo (63 m).
- Lo script cerca espressioni, non capisce le regole. Una regex scritta male
  dà «non trovata», e un master che riformula la frase fa sparire il
  riscontro: il test del file di ARC-08 controlla solo che le regex compilino
  e che i master esistano, non che ogni voce trovi ancora il suo testo.
- Il riscontro automatico di tutto il corpus resta fuori: servirebbe un
  glossario italiano-inglese dei nomi di incantesimi, oggetti e creature che
  il repo non ha in forma leggibile da una macchina. I nomi in `regola` sono
  quelli inglesi dell'SRD.
- L'SRD non contiene il DMG (la tabella dell'EL, la balista) e il PRD del 2015
  non ha le macchine d'assedio di *Ultimate Combat*: per quelle regole lo
  script dice «non trovata», ed è la risposta giusta.
- Si paga: 50 MB in cache al primo uso, e un job CI da guardare per due
  settimane.

**Da rivedere se**: uno dei due archivi sparisce o cambia licenza (allora si
fissa una copia altrove, con lo stesso sha256); oppure dopo 14 giorni il job
ha dato falsi allarmi (una regex che si rompe a ogni ritocco del master vuol
dire che il formato dei riscontri è troppo fragile); oppure il DM chiede il
riscontro su tutto il corpus, e allora serve prima il glossario.
