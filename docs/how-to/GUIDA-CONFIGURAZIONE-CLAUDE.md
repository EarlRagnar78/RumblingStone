# Configurazione di Claude Code nel repo: scelte e ritorno indietro

Questa guida raccoglie le scelte fatte il 2026-11-19 sulla configurazione di
Claude Code per RumblingStone. Per ognuna dice che cosa cambia, con quale
misura è entrata e come si torna indietro, tutta o in parte. Le decisioni
complete stanno negli ADR citati; la storia, nelle voci della memoria storica
(`python3 scripts/memoria_storica.py --adr 140`, `--adr 141`, `--adr 142`,
`--adr 143`, `--adr 146`, `--adr 149`, `--adr 153`).

## 1. La catena: come la configurazione arriva a una sessione

Nei thread del progetto Claude parte nella cartella che contiene il clone
(`/home/user`), non nel repo. La configurazione del repo ci arriva così:

1. lo script d'avvio dell'ambiente cloud `RumblingStone-corpus` lancia
   `RumblingStone/scripts/claude-progetto.sh "$PWD"`;
2. lo script scrive in `/home/user` un `CLAUDE.md` corto, una copia di
   `.claude/settings.json` (hook a percorso assoluto, regole `Read` ancorate
   con il nome del repo davanti) e `.mcp.json`;
3. lo stesso script scrive anche a livello utente: `~/.claude/settings.json`
   (hook a percorso assoluto, `enabledPlugins`, regole `Read` ancorate rese
   assolute con `//`), la sola voce `rumblingstone-tools` in `~/.claude.json`,
   e costruisce le skill del repo in `~/.claude/skills` prima che la sessione
   parta (circa 8 secondi). `~/.claude/settings.json` si sovrascrive solo se
   manca o se è elencato in `~/.claude/.generato-da-rumblingstone`;
4. le regole di `RumblingStone/.claude/rules/` non vanno copiate: Claude Code
   le carica da sole quando legge un file del repo.

**Il livello utente è quello che conta.** Dal 22/11 circa i thread partono in
`/home/user` ma ignorano `/home/user/.claude/settings.json`: nei log
diagnostici gli hook SessionStart passano da 2 a 1 dal 23/11, e il primo
thread dopo la #510 non aveva né hook del repo, né skill `rumblingstone-*`,
né `rumblingstone-tools`, e aveva accesi tutti i circa 35 plugin dell'account.
Gli agenti arrivavano lo stesso, perché `.claude/agents` è un collegamento
alla cartella del repo. La copia in `/home/user/.claude/settings.json` resta
per le sessioni lanciate a mano in quella cartella. Misura e limiti nella
correzione del 25/11 di ADR-0146.

Un plugin che l'account aggiunge dopo l'ultima revisione di `enabledPlugins`
si accende da solo: va spento con una riga `false` in `.claude/settings.json`.
Il 25/11 sono stati spenti così `superpowers`, `agentic-council`, `ai-mentor`,
`frontend-design` e `skill-creator`.

Il primo hook che la sessione esegue è `.claude/hooks/session-start.sh`
(SessionStart, registrato in `.claude/settings.json`): in background ricostruisce
le skill del repo e le copie per gli altri agenti, scrive l'esito in
`.claude/.skills-sync-status` (`syncing`, `ok <sha>`, `failed`) e nei container
cloud installa gli hook git (`install-git-hooks.sh`, quindi il `pre-push` di
ADR-0143). Non blocca mai la sessione: se fallisce, avvisa ed esce 0.

Chi lavora in locale dalla radice del repo usa direttamente i file del repo;
`claude-progetto.sh` lì non scrive nulla.

**Un container già partito** tiene la copia che c'era al suo avvio. Dopo un
merge che tocca `.claude/settings.json`, `.mcp.json` o lo script, si rilancia:

```bash
RumblingStone/scripts/claude-progetto.sh
```

## 2. Le scelte, una per una

| # | Scelta | ADR, PR, merge | Misura con cui è entrata |
|---|---|---|---|
| 1 | La configurazione del repo arriva nei thread (script, hook che trova il repo dal suo percorso) | ADR-0140, #486, `43be2dce` | hook e `rumblingstone-tools` presenti; contesto iniziale +4.852 token |
| 2 | Dieci connettori dell'account negati con `permissions.deny` (Gmail, Google Drive, Channel3, Clipkit, Mobbin, Microsoft Learn, MDN, Shutterstock, bioRxiv, pg-aiguide) | ADR-0140 punto 4, #486 | da 84 a 58 tool su un server di prova |
| 3 | Plugin dell'account mai usati nel repo spenti con `enabledPlugins: false` | ADR-0140 punto 5, #487, `983791d0` | contesto iniziale da 59.670 a 53.965 token (−9,6%) |
| 4 | Riaccesi i nove plugin di metodo di sviluppo (`sdd`, `sadd`, `engineering`, `reflexion`, `docs`, `fpf`, `ddd`, `recursive-decomposition`, `mcp`) | ADR-0140 punto 5, #488, `a4fbfafd` | costo dichiarato: +2.347 token (+4,3%), scelta del DM |
| 5 | AGENTS.md diviso in regole `.claude/rules/rs-*.md` che arrivano con i file | ADR-0141, #489, `e1198477` | su uno script −45% di caratteri rispetto ad AGENTS.md intero |
| 6 | `.claudeignore` tradotto in regole `Read(...)` di `permissions.deny` | ADR-0142, #490, `f36785eb` | righe trovate nelle ricerche fino a −39% |
| 7 | I gate bloccanti e veloci della CI girano prima del push (`gate_locale --pre-push` con pre-commit, hook locale); nei thread lo installa l'avvio | ADR-0143 | 7 dei 12 rossi recenti presi in locale, 45 s a push |
| 8 | Hook PreToolUse `vincolo_skill.py`: la prosa di gioco senza `rumblingstone-narrative-style` caricata si ferma; dodici agenti in `.claude/agents/` in tre classi con le skill precaricate; hook UserPromptSubmit e Stop `instradamento_agenti.py` che suggeriscono agente e catena per il lavoro in arrivo, e un PreToolUse che ferma push e PR se la catena scritta nelle istruzioni non è stata chiamata; cricchetto della prosa in CI | ADR-0146 | prima: zero caricamenti di skill su 188 chiamate in cinque thread; l'hook si attiva su circa 200 modifiche su 2.944 ai file di gioco; il cricchetto ne avrebbe fermata 1 su 157; l'instradamento indovina il primo agente in 23 frasi vere su 33 |
| 9 | La configurazione arriva anche a livello utente (`~/.claude/settings.json`, `~/.claude.json`, skill costruite prima dell'avvio); spenti `superpowers`, `agentic-council`, `ai-mentor`, `frontend-design`, `skill-creator` | ADR-0146, correzione del 25/11 (#518) | sessione nuova in `/home/user`: con la configurazione utente hook del repo attivi, `rumblingstone-tools` connesso, 12 plugin; senza, nessun hook del repo e 39 plugin |
| 10 | Il tredicesimo agente, `sincronizzatore-giocato` (Tecnici), porta il giocato sul ramo di gruppo; l'hook UserPromptSubmit aggiunge l'esito di `sincronia_giocato.py --avviso` quando si parla del giocato; il PreToolUse del push diventa anche cancello del canone (push che riscrive un ramo `campaign-group-*`, canone su main, rami morti di `plans/rami-di-gruppo.json`) e il suo matcher comprende gli strumenti MCP di GitHub che scrivono (`push_files`, `create_or_update_file`, `delete_file`, `create_branch`, `merge_pull_request`, `update_pull_request_branch`; anche `--prune` e i refspec a glob) | ADR-0149 | il 21/11 il ramo di gruppo era fermo al 12/10; su `ce345991` la misura dà 1.398 commit di main mancanti da 41 giorni, sette patch ferme e una serata non registrata |
| 11 | Il cancello del push legge la riga «Catena:» anche dalla trascrizione: prima il registro scritto dall'hook UserPromptSubmit, poi l'ultima catena nei messaggi a Claude (testo scritto, righe `isMeta` comprese, mai `tool_result` né `isSidechain`). Il messaggio di avvio di un thread arriva come riga `isMeta` e l'hook del prompt non scatta su di lui. In CI, `documentazione_allineata.py --rispetto-a` boccia la PR che aggiunge un agente, uno script, un workflow o un hook senza citarlo nel suo indice | ADR-0153 | il 27/11 un `git push --dry-run` in un thread con `Catena: sviluppatore → autore-documenti` passava con «nessuna catena scritta nelle istruzioni»; sulla #510 il cancello della documentazione avrebbe trovato 15 elementi scoperti |
| 12 | Il quattordicesimo agente, `custode-memoria` (Tecnici), risponde da memoria del progetto, file storico e coda con `memoria_custode.py cerca`; due hook PreToolUse in testing: `memoria_custode.py --hook-merge` su `Bash\|mcp__github__merge_pull_request` (da Bash solo `gh pr merge` e `gh api .../pulls/N/merge` in `PUT`; il resto esce 0 senza leggere la memoria) esce 2 se una riga tolta dalla memoria del progetto dall'ultima istantanea dello specchio non è archiviata o se `MEMORY.md` supera 16.384 byte, `--hook-scrittura` su Write, Edit e MultiEdit dentro la cartella della memoria avvisa senza bloccare; esiti in `.claude/.custode-memoria.jsonl` | ADR-0151 | il 27/11, togliendo una alla volta le 56 righe di `MEMORY.md`, 12 non erano archiviate; hook di merge con mediana 129 ms (massimo 228), di scrittura 45 ms fuori dalla memoria e 89 ms dentro; con Bash nel matcher (correzione del 27/11) mediana su ogni comando Bash fra 46 e 54 ms, prima 42-47 |
| 13 | Il primo comando slash del repo, `/lavoro-in-corso`, con lo stesso testo in `.claude/commands/` (Claude Code) e in `.opencode/commands/` (OpenCode): rigenera `plans/LAVORO-IN-CORSO.md` con `lavoro_in_corso.py --fetch` e ne fa un riassunto; il `CLAUDE.md` scritto da `claude-progetto.sh` porta la riga che rimanda alla pagina | ADR-0157 | il 27/11 la pagina vera ha 8 filoni e mostra 4 PR aperte, 3 rami e 28 cartelle condivise recenti che nessun documento elencava |

## 3. Tornare indietro

Per ogni scelta c'è un ritorno completo (revert della PR) e, dove ha senso, un
ritorno parziale. Dopo ogni ritorno: si rilancia `claude-progetto.sh` nei
container già partiti e si fa la verifica della colonna a destra.

| # | Ritorno completo | Ritorno parziale | Verifica |
|---|---|---|---|
| 1 | togliere la riga di `claude-progetto.sh` dallo script d'avvio dell'ambiente (la cambia solo il DM), poi `git revert` del merge di #486 | nessuno | in un thread nuovo `/home/user/CLAUDE.md` non esiste |
| 2 | togliere le righe `mcp__…` da `permissions.deny` in `.claude/settings.json` | togliere la riga di un solo connettore, oppure riaccenderlo per la sessione con `/mcp` | il connettore torna nell'elenco dei tool |
| 3, 4 | `git revert` del merge di #487 o di #488 | in `enabledPlugins` mettere `true` (o `false`) sulla riga del plugin | `claude -p --output-format stream-json --verbose "ok"` dalla cartella dei thread: campo `plugins` dell'evento `init` |
| 5 | `git revert` del merge di #489: tornano il CLAUDE.md che fa leggere AGENTS.md intero e nessuna regola `rs-*` | togliere una regola dalla tabella `SEZIONI` di `scripts/regole_claude.py` mettendo le sue sezioni nel nucleo, poi `python3 scripts/regole_claude.py` | `python3 scripts/regole_claude.py --misura`; in una sessione, leggere un file e chiedere quali `.claude/rules` sono nel contesto |
| 6 | togliere tutte le righe `Read(...)` da `permissions.deny` (o `git revert` della PR) | lasciare leggibile una voce: in `.claudeignore` metterla sotto un commento `# leggibile: motivo`, poi `python3 scripts/claudeignore_deny.py` | aprire con Read un file di quella voce |
| 7 | `git revert` della PR; su una sola macchina `rm .git/hooks/pre-push` | togliere un gate dal hook aggiungendolo a `LENTI` in `scripts/gate_locale.py` con i secondi misurati | `python3 scripts/gate_locale.py --pre-push --elenco` |
| 8 | `git revert` della PR, poi `claude-progetto.sh` nei container già partiti | togliere il gruppo `PreToolUse` da `.claude/settings.json` (spegne l'hook), i gruppi `UserPromptSubmit` e `Stop` (spengono l'instradamento), il gruppo `PreToolUse` con matcher `Bash\|mcp__github__create_pull_request\|…` (spegne il cancello del push e, dalla scelta 10, quello del canone), il passo «Prosa — il testo cambiato non peggiora» da `ci.yml` (spegne il cricchetto), o un solo file da `.claude/agents/`; un tipo di file di prosa nuovo si aggiunge a `PROSA_PURA` in `scripts/vincolo_skill.py` | `python3 scripts/vincolo_skill.py --classe FILE`; in una sessione, `/agents` elenca gli agenti |
| 9 | togliere da `claude-progetto.sh` il blocco «Livello utente», poi `rm ~/.claude/settings.json ~/.claude/.generato-da-rumblingstone` e la voce `rumblingstone-tools` da `~/.claude.json` | riaccendere un plugin con `true` sulla sua riga di `enabledPlugins`; `RS_SALTA_SKILL=1` salta la costruzione delle skill | in `/home/user`, `claude -p --output-format stream-json --verbose "ok"`: campi `plugins` e `mcp_servers` dell'evento `init` |
| 10 | `git revert` della PR, poi `claude-progetto.sh` nei container già partiti | togliere dal matcher del PreToolUse del push i quattro strumenti `mcp__github__…` (il cancello torna sul solo Bash), togliere `.claude/agents/sincronizzatore-giocato.md` (resta lo script), o disattivare il workflow `sincronia-giocato.yml` dalla scheda Actions | `python3 scripts/sincronia_giocato.py --check`; in una sessione, `/agents` elenca tredici agenti |
| 11 | `git revert` della PR | togliere `or catena_dalla_trascrizione(...)` in `decidi_cancello` di `scripts/instradamento_agenti.py` (il cancello torna al solo registro), o il passo «Documentazione — la struttura nuova è citata nel suo indice» da `ci.yml` | `python3 -m pytest scripts/tests/test_instradamento_agenti.py scripts/tests/test_documentazione_allineata.py`; `python3 scripts/documentazione_allineata.py --rispetto-a origin/main` |
| 12 | `git revert` della PR, poi `claude-progetto.sh` nei container già partiti | togliere da `.claude/settings.json` il gruppo PreToolUse con matcher `Bash\|mcp__github__merge_pull_request` (spegne il blocco del merge), o solo `Bash|` dal matcher (il blocco resta sullo strumento MCP) o il comando `memoria_custode.py --hook-scrittura` dal gruppo di Write ed Edit; togliere `.claude/agents/custode-memoria.md` (resta lo script) | `python3 scripts/memoria_custode.py --riepilogo`; in una sessione, `/agents` elenca quattordici agenti |
| 13 | `git revert` della PR, poi `claude-progetto.sh` nei container già partiti | togliere `.claude/commands/lavoro-in-corso.md` o `.opencode/commands/lavoro-in-corso.md` (spegne il comando in un solo strumento; lo script resta), o la riga «Per il lavoro in corso fuori da main» da `claude-progetto.sh` | `python3 scripts/lavoro_in_corso.py --check`; in una sessione, `/lavoro-in-corso` compare fra i comandi |

Due regole valgono per ogni ritorno:

- **AGENTS.md e `.claudeignore` sono le fonti.** Le regole generate si
  rigenerano, non si correggono a mano: `regole_claude.py --check` e
  `claudeignore_deny.py --check` girano nei test e bocciano la deriva.
- **Un ritorno è una PR come le altre**, con la sua riga in
  `plans/CHANGELOG.md`, la voce nella memoria storica e la misura prima e dopo.

## 4. Come si misura

| Che cosa | Comando |
|---|---|
| contesto iniziale, plugin, server, skill | `cd /home/user && claude -p --max-turns 1 --output-format stream-json --verbose "Rispondi solo: ok"`: evento `init` e `usage` del `result` |
| ripartizione del contesto | `cd /home/user && claude -p "/context"` |
| regole caricate per compito | `python3 scripts/regole_claude.py --misura` |
| righe trovate nelle ricerche | `rg -c PAROLA . ` contro la stessa ricerca con le voci di `.claudeignore` come `--ignore-file` |
| uso delle skill di prosa (blocchi, passaggi, promemoria dell'hook) | `python3 scripts/vincolo_skill.py --riepilogo` |
| agenti suggeriti, quanti thread li hanno chiamati, push passati, bloccati e in deroga | `python3 scripts/instradamento_agenti.py --riepilogo` |
| agenti, script, workflow e hook che il loro indice non cita | `python3 scripts/documentazione_allineata.py --debito` |
| se serve un thread di `autore-documenti`, con motivi, lavoro e stima in token | `python3 scripts/documentazione_allineata.py --attiva --json` |

`claude -p` non vede i connettori di claude.ai: il loro peso si misura solo in
un thread vero.

## 5. Cose provate che non funzionano

- **`.claudeignore`**: Claude Code non lo legge. Un file elencato lì si apre
  comunque (prova del 2026-11-19). Per questo esiste la scelta 6.
- **Un RAG o un grafo sulle istruzioni**: scartati, perché una regola
  obbligatoria potrebbe non arrivare. Le regole a percorso sono deterministiche.
- **Il CLAUDE.md senza la riga di `fase1.py`**: le regole arrivano dopo il primo
  file letto, e in prova l'agente aveva risposto senza lanciare `fase1.py`. La
  riga resta nel CLAUDE.md dei thread.
- **Tutti i gate della CI prima del push** (`gate_locale --rapido`, 3 min 11 s):
  su 100 push costa più tempo dei rossi che evita. Il hook tiene solo i gate
  bloccanti sotto i 15 secondi (ADR-0143).
- **Le skill del repo «doppie»**: misurate con `/context`, costano circa 0,7k
  token, non i 5k stimati all'inizio. Niente da correggere.
