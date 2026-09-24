# SPEC — Il server MCP sui tool del repo

> **Cos'è questo documento.** Un ADR registra una **decisione**; questo registra un
> **sistema**: cosa fa, cosa deliberatamente non fa, e — la parte che conta —
> **contro cosa si difende**. Esiste separato perché il modello di sicurezza di
> un server che esegue 48 programmi va scritto dove lo si rilegge prima di
> toccarlo, non dedotto dal codice sei mesi dopo.
> Decisione: [ADR-0030](adr/ADR-0030-server-mcp-sui-tool.md) ·
> Lotto **G1** di [PIANO-CHIUSURA-CATENA-EDITORIALE](PIANO-CHIUSURA-CATENA-EDITORIALE.md) ·
> Chiude la promessa di [ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md).

## 1. Il problema

`docs/tools/mcp-tools.json` descrive **48 tool** con nome, descrizione e
`inputSchema` completo. È generato da `scripts/tools.manifest.json`, che ADR-0012
ha eletto a fonte di verità. Ma **nessuno lo consuma**: è un descrittore senza
server. Un agente che vuole lanciare `suggest_encounter` deve farselo raccontare
in prosa, e chi lo guida deve incollare righe di comando a mano.

Il costo non è la comodità. È che **la fonte di verità non ha un lettore**, quindi
niente verifica che resti vera: uno schema sbagliato non rompe nulla finché
nessuno prova a usarlo.

## 2. Obiettivi

| | |
|---|---|
| **G-1** | Un client MCP scopre i tool del repo e li esegue, senza che nessuno incolli comandi |
| **G-2** | La fonte di verità acquista un consumatore: se uno schema è sbagliato, si vede |
| **G-3** | Un agente **non può** fare, tramite il server, ciò che il DM non ha consentito |
| **G-4** | Zero dipendenze: stdlib, come tutto il resto degli `scripts/` |

## 3. Non obiettivi — dichiarati, non dimenticati

- **Non è un server di rete.** Solo stdio. Nessuna porta, nessun bind, nessuna
  autenticazione — perché non c'è niente da autenticare: chi lancia il processo è
  già chi possiede il repo.
- **Non è una shell.** Non esiste un tool «esegui questo comando». Se serve una
  cosa nuova, si aggiunge uno script e si registra nel manifest.
- **Non espone `resources` né `prompts`** (le altre due superfici MCP). Solo
  `tools`. Le si aggiunge quando servono, non «già che ci siamo».
- **Non fa streaming** dell'output: i tool di questo repo finiscono in secondi.
- **Non sostituisce `dm.py`.** Chi sta al terminale continua a usare la CLI.

## 4. Il modello di sicurezza

Un server MCP che espone 48 programmi **è una superficie d'esecuzione**, e va
trattata come tale. Sei difese, ognuna contro una cosa precisa.

| # | Difesa | Contro cosa |
|---|---|---|
| **S-1** | **Solo allowlist.** Gli unici eseguibili sono quelli dichiarati nel manifest. Nessun tool generico | esecuzione arbitraria |
| **S-2** | **Niente shell.** `subprocess.run` con lista argv, `shell=False`, nessuna interpolazione in stringa | injection via `;`, `$(…)`, backtick |
| **S-3** | **Argomenti validati sullo schema** prima di eseguire: tipo giusto, `enum` rispettato, nessuna chiave sconosciuta | un valore che diventa un'opzione |
| **S-4** | **I percorsi restano nel repo.** Ogni argomento di tipo `path` è risolto e deve stare sotto la radice | `../../etc/passwd`, percorsi assoluti |
| **S-5** | **Read-only per difetto.** I tool con `writes_canon` o `git_commit` sono **elencati ma rifiutano di partire** senza `--allow-write` | un agente che scrive il canone di sua iniziativa |
| **S-6** | **Timeout e tetto all'output** (120 s, 256 KiB) | un tool che appende, e un output che soffoca il contesto del client |

**S-5 merita una riga in più**, perché è l'unica che non nasce da un manuale di
sicurezza ma da questo repo: [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md) vuole
che il canone si scriva su un branch di gruppo, dopo la sessione, con l'occhio
del DM sopra. Cinque tool su cinquanta possono scriverlo — `session_wizard`,
`state_apply`, `dm`, `new-campaign-group`, `import_html_module` — e quattro di
essi **fanno anche commit**. Un agente che li lanciasse perché «sembrava il passo
successivo» non violerebbe una regola di sicurezza: violerebbe il **flusso di
lavoro del DM**, che è peggio, perché non se ne accorgerebbe nessuno subito.

Sono elencati e non nascosti di proposito: il client deve **poter vedere** che
esistono e perché non partono. Un tool invisibile diventa una richiesta a mano.

### Cosa questo modello NON copre

- **Ciò che i tool fanno di loro.** Il server garantisce *quale* programma parte e
  con quali argomenti; non ispeziona cosa quel programma poi scrive.
- **Il contenuto restituito.** L'output di un tool è dato, non istruzioni. Un
  client che lo tratta come comandi ha un problema suo, e nessun server lo cura.

## 5. Superficie di protocollo

JSON-RPC 2.0 su stdio, un messaggio per riga (trasporto stdio di MCP).

| Metodo | Cosa fa |
|---|---|
| `initialize` | dichiara versione di protocollo e capacità (`tools`) |
| `notifications/initialized` | accettata e ignorata (è una notifica) |
| `tools/list` | i 48 tool, con `inputSchema` e **annotazioni** |
| `tools/call` | esegue, restituisce `content` testuale |
| `ping` | risponde `{}` |

Le **annotazioni** (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
`openWorldHint`) sono derivate dal manifest: `readOnly` = non scrive canone e non
committa; `destructive` = fa commit. È il modo standard di dire a un client cosa
sta per fare, e finora `mcp-tools.json` **non le aveva**: un client non
distingueva un validatore da uno script che scrive il canone.

## 6. Tassonomia degli errori — la distinzione che conta

> **Un tool che esce diverso da zero non è un errore di protocollo.**

`validate_lingua` esce **1** per progetto e in CI è `continue-on-error`; il suo
codice 1 è un **risultato**. Se il server lo trasformasse in un errore JSON-RPC,
il client vedrebbe un guasto dove c'è un referto.

| Situazione | Risposta |
|---|---|
| JSON malformato, metodo ignoto, parametri mancanti | **errore JSON-RPC** (`-32700`, `-32601`, `-32602`) |
| Tool sconosciuto, argomento fuori schema, percorso fuori dal repo, scrittura non consentita | **errore JSON-RPC** `-32602` — la chiamata non è mai partita |
| Tool eseguito, uscita ≠ 0 | **risultato** con `isError: true`, stdout+stderr, e il **significato del codice** preso da `exit_codes` del manifest |
| Timeout | **risultato** con `isError: true` che dice quanti secondi |

L'ultima riga della terza è la parte utile: il manifest sa già che per
`suggest_encounter` il codice 3 vuol dire *«nessuna proposta assemblabile»*.
Restituirlo tradotto è la differenza fra un agente che ritenta a caso e uno che
cambia parametri.

## 7. Osservabilità

Niente log su `stdout`: **stdout è il canale del protocollo**, e una riga di
diagnostica lì dentro rompe il trasporto. Diagnostica su `stderr`, spenta di
default, `--verbose` per accenderla. Ogni chiamata registra: tool, durata, codice
d'uscita, byte troncati.

## 8. Come si verifica

- **Test di protocollo**: il server viene guidato *attraverso stdio* — `initialize`
  → `tools/list` → `tools/call` — come lo guiderebbe un client. Non chiamando le
  funzioni interne, che è il modo di avere test verdi e un server che non parla.
- **Test delle difese**: una per una. Traversamento di percorso, valore che
  comincia per `-`, chiave sconosciuta, tool che scrive canone senza
  `--allow-write`, timeout.
- **Test di aderenza al manifest**: i tool esposti sono esattamente quelli non-lib
  del manifest, e le chiavi dello schema si derivano con **la stessa funzione**
  che usa l'emettitore di `mcp-tools.json`. Due regole per lo stesso nome sono due
  regole, e una invecchia.

## 9. Domande aperte

- **Le `resources` MCP** esporrebbero `campaign/state.md` e il bestiario in
  lettura. Utile, ma è un'altra superficie: si valuta quando qualcuno la chiede.
- **La concorrenza** non è gestita: una chiamata alla volta. Due
  `build_monster_catalog` insieme si pesterebbero i piedi, e il server non è il
  posto giusto per il lock — lo è il tool.
