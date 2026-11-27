# ADR-0151 — La memoria del progetto ha uno specchio e un custode

**Stato**: accettata (2026-11-27): il DM ha scelto sulle due card del thread la copia redatta nel repo con quella completa in `/mnt`, e l'hook di merge bloccante
**Data**: 2026-11-27
**Decisione-fonte**: il DM (Jfs), 2026-11-27, thread «Creare l'agente custode della memoria»: un agente che porti la memoria storica dal progetto al repo, risponda agli altri agenti dalla memoria del progetto e da quella storica, tenga una copia della memoria nel repo, e un obbligo (regola o hook) di chiamarlo prima del merge.
**Rapporti**: rende misurabile la regola «archivia prima di togliere» di [ADR-0127](ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md); usa la coda di [ADR-0137](ADR-0137-la-memoria-storica-si-scrive-a-ogni-blocco-di-lavoro-non-solo-al-merge.md) e il suo cancello di [ADR-0138](ADR-0138-la-coda-della-memoria-storica-ha-un-cancello.md); lancia il tetto di [ADR-0139](ADR-0139-la-memoria-corta-ha-un-tetto-misurato.md) a ogni verifica. Aggiunge il quattordicesimo agente a quelli di [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md) §4; i canali sono quelli di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md).

## Contesto

Il 27/11 il coordinatore ha riscritto la riga di stato di `MEMORY.md` senza
archiviare quella vecchia. Se n'è accorto da sé; l'unico fatto perso (l'ordine
del voto cieco sui box del Consiglio) è stato recuperato in coda. Nessuno
strumento poteva vederlo: la memoria del progetto non ha storia, e senza sapere
quale riga c'era ieri la regola di ADR-0127 non la misura nessuno.

Misure su main `076a74d1` (audit del thread, in
`/mnt/project-files/custode-memoria-2026-11-27/AUDIT.md`):

| Che cosa | Misura |
|---|---|
| `MEMORY.md` | 15.324 byte; tetto 12.288 (ADR-0139), limite della piattaforma 16.384 |
| coda, `memoria_coda.py --check` | esce 1: cinque campi mancanti in un file |
| `--confronta-memoria` | 152 righe con gettoni (PR, ADR, SHA, percorsi) che il repo non ha |
| file della memoria con dati personali | 5 su 87; il repo è pubblico |
| righe di `MEMORY.md` tolte una alla volta | 56: 44 archiviate, 12 no (verrebbero fermate) |

Il fatto che cambia la fattibilità: nei thread la memoria è una cartella di
file (`/tmp/claude/memory/team/<mount>`, ricavata da
`CLAUDE_COWORK_MEMORY_PATH_OVERRIDE` e `CLAUDE_MEMORY_STORES`), 87 file
sincronizzati col servizio della memoria. Un thread la scrive con Write ed
Edit, quindi un hook del repo la vede. Il coordinatore scrive con strumenti
suoi, che nessun hook del repo intercetta.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Specchio fuori dal repo, `memoria_custode.py` con `verifica` al merge e un agente che lo usa** (proposta) | la storia nasce da qualunque thread, senza chiedere niente al coordinatore; stdlib; il merge è il punto in cui ogni thread passa | le scritture del coordinatore si vedono dopo, non si impediscono |
| Solo la regola nell'agente e nelle istruzioni | nessun codice | è la forma che il 27/11 non ha retto |
| Un servizio o un'API di rete per la memoria | potrebbe vedere anche il coordinatore | la piattaforma la sincronizza già; un server in più è codice senza una misura che lo chieda |
| Indice semantico sulla memoria | ricerca per significato | ADR-0127 lo rimanda finché una ricerca per parole non fallisce davvero |
| Copia integrale della memoria nel repo | niente resta fuori | il repo è pubblico e 5 file hanno dati personali |

## Decisione

1. **Lo specchio.** `memoria_custode.py specchia` scrive un'istantanea completa
   della memoria, con un `MANIFEST.json` di sha256, in
   `/mnt/project-files/memoria-progetto-specchio/istantanee/`, solo quando il
   contenuto cambia, in modo atomico e con un lucchetto. La prima è del 27/11
   alle 06:17 UTC (`20261127T061735Z`). I termini riservati stanno in
   `RISERVATI.txt` nello specchio, fuori dal repo.
2. **La verifica.** `verifica` confronta la memoria con l'ultima istantanea.
   Una riga tolta è archiviata se ogni suo gettone compare nel repo, nel file
   storico, in coda o nella memoria nuova, e se le sue parole sparite sono al
   più due oppure una sola voce ne contiene almeno il 70%. Una riga con un
   termine riservato o un'email resta solo nello specchio e conta come
   archiviata lì. Esce 1 se una riga non è archiviata o se `MEMORY.md` supera
   16.384 byte; il tetto di 12 KB, i difetti della coda, un `RISERVATI.txt`
   che manca o è vuoto e i link `[[nome]]` rotti fra le note sono avvisi. Se
   passa, l'istantanea avanza.
3. **Il rimedio.** `archivia` scrive in coda una voce con le righe tolte,
   testuali, e rifiuta quelle con dati riservati. Senza un `RISERVATI.txt`
   leggibile e non vuoto `archivia` e `redigi` falliscono chiusi: escono 1
   senza scrivere niente, perché senza l'elenco un dato personale passerebbe
   come riga qualunque (correzione del 27/11, rilievo Codex P1 sulla #529).
4. **La lettura da tre fonti.** `cerca` risponde da memoria del progetto, file
   storico e coda, con la fonte di ogni riga. Per ogni nota trovata aggiunge
   le note collegate a un passo con `[[nome]]`, in uscita e in entrata, con la
   fonte `memoria-link`; `--senza-link` le toglie. Dal server MCP in sola lettura
   escono solo `cerca` e `verifica`: `specchia`, `archivia` e `redigi` sono in
   `mcp_vietati`.
5. **Due hook nei thread**, in `.claude/settings.json`, nel canale testing:
   - `--hook-merge`, PreToolUse su `Bash|mcp__github__merge_pull_request`:
     esce 2 solo per righe tolte non archiviate o per `MEMORY.md` oltre 16.384
     byte. Da Bash riconosce `gh pr merge` (con `-R`, `--repo` o `GH_REPO`, o
     senza se la cartella è il repo) e `gh api .../pulls/N/merge` solo con
     `PUT`, perché in `GET` è una lettura; ogni altro comando esce 0 senza
     leggere la memoria. Il blocco dice di creare `RISERVATI.txt` quando
     manca;
   - `--hook-scrittura`, PreToolUse su Write, Edit e MultiEdit dentro la
     cartella della memoria: avvisa con `additionalContext` e non blocca.

   Ogni esito va in `.claude/.custode-memoria.jsonl` (ignorato da git);
   `--riepilogo` lo conta. L'hook di scrittura diventa bloccante non prima del
   2026-12-12, con almeno 10 eventi nel registro, zero falsi avvisi non
   spiegati, p95 sotto 1 s e l'ok del DM.
6. **L'agente `custode-memoria`** (Tecnici, il quattordicesimo): risponde con
   `cerca` citando fonte e riga, lancia `verifica` prima di toccare la memoria
   e prima di un merge, e se fallisce `archivia`. Non copia dati personali nel
   repo.
7. **La copia nel repo** (scelta del DM, card del 2026-11-27). `redigi --uscita
   plans/memoria-progetto/` copia la memoria con le righe riservate sostituite
   da un'impronta; la copia completa resta nelle istantanee in `/mnt`. Scartate
   la copia solo in `/mnt` e quella integrale nel repo, che è pubblico. La prima
   copia entra con questa PR (87 file, 25 righe riservate); dopo si rigenera in
   una PR di sola storia, di norma con la piega del lunedì.
8. **Il merge bloccante** (scelta del DM, card del 2026-11-27). L'hook di merge
   blocca; scartato il solo avviso, la forma che ADR-0127 e ADR-0139 avevano
   già provato.

## Le conseguenze

- Le misure del codice: 27 test nuovi; suite intera 3.588 passati e 19
  saltati; `gate_locale --pre-push` 54 passi verdi; `tools_manifest --check`
  155 conformi; `prove_skill controlla --agenti` 44 casi per 14 agenti. Tempi
  degli hook: merge con mediana 129 ms e massimo 228; scrittura 45 ms fuori
  dalla memoria e 89 ms dentro; il timeout è 10 s.
- Le correzioni del 27/11, dopo la #529: suite intera 3.639 passati e 19
  saltati; `gate_locale --pre-push` 56 passi verdi; `tools_manifest --check`
  156 conformi. Con Bash nel matcher l'hook gira su ogni comando: mediana fra
  46 e 54 ms (prima 42-47), 100-150 ms su un merge vero. Sulla memoria del
  27/11 i link fra le note sono 208 in 92 note, nessuno rotto.
- Le prove dell'agente con `claude -p` (CLI 2.1.332), le prime: 0,85
  (`risponde-da-tre-fonti` 0,8, `trappola-dati-personali` 0,75,
  `trappola-riga-tolta` 1,0). Due giudici erano troppo stretti: `01-cerca`
  guardava la risposta e l'agente aveva usato `cerca` senza nominarlo, quindi
  ora guarda la traccia (`target: trace`, come gli altri giudici d'uso);
  `01-rifiuta` non accettava «Non ho fatto la copia». Le stesse esecuzioni,
  rivalutate, danno 1,0. I giudici sono stati corretti dopo aver visto le
  risposte e non ci sono esecuzioni nuove: il 1,0 va confermato dalla prossima
  tornata. Entrambi gli esiti sono in `.claude/agent-evals/ESITI.jsonl`.
- Quello che si paga: un thread può essere fermato al merge per righe tolte da
  altri, il coordinatore compreso. Il rimedio è un comando, `archivia`, e il
  messaggio dell'hook lo dice. Delle 56 righe di `MEMORY.md` di oggi, 12
  fermerebbero un merge se fossero tolte senza archiviarle.
- **Cosa non vede.** Il merge dall'interfaccia di GitHub non passa
  dall'hook. Da Bash il riconoscimento è lessicale: un merge lanciato da uno
  script, da un alias o con `eval` non si vede. Le scritture del coordinatore si vedono solo
  alla verifica successiva. Un hook in timeout lascia passare il merge, e così
  un errore interno. Il confronto è per righe e per parole: una riga riscritta
  con parole diverse conta come fatti persi anche se dice la stessa cosa.
- Il messaggio di rifiuto S-7 di `scripts/mcp_server.py` era scritto per
  `prove_skill` e, per i comandi vietati di `memoria_custode`, diceva una cosa
  falsa. Dal 27/11 il motivo viene dalle `side_effects.notes` del manifest di
  ciascun tool.

## Da rivedere se

- il coordinatore toglie righe non archiviate due volte in una settimana: la
  verifica al merge non basta e serve un controllo dalla parte della
  piattaforma;
- l'hook di merge ferma un thread per righe non sue più di una volta a
  settimana;
- la piattaforma cambia il percorso della memoria o il limite di 16 KB;
- la copia nel repo, se il DM la sceglie, lascia passare un dato personale.
