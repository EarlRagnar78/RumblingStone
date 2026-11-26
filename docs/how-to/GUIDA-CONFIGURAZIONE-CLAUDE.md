# Configurazione di Claude Code nel repo: scelte e ritorno indietro

Questa guida raccoglie le scelte fatte il 2026-11-19 sulla configurazione di
Claude Code per RumblingStone. Per ognuna dice che cosa cambia, con quale
misura è entrata e come si torna indietro, tutta o in parte. Le decisioni
complete stanno negli ADR citati; la storia, nelle voci della memoria storica
(`python3 scripts/memoria_storica.py --adr 140`, `--adr 141`, `--adr 142`,
`--adr 143`).

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
| 8 | `git revert` della PR, poi `claude-progetto.sh` nei container già partiti | togliere il gruppo `PreToolUse` da `.claude/settings.json` (spegne l'hook), i gruppi `UserPromptSubmit` e `Stop` (spengono l'instradamento), il gruppo `PreToolUse` con matcher `Bash|mcp__github__create_pull_request` (spegne il cancello del push), il passo «Prosa — il testo cambiato non peggiora» da `ci.yml` (spegne il cricchetto), o un solo file da `.claude/agents/`; un tipo di file di prosa nuovo si aggiunge a `PROSA_PURA` in `scripts/vincolo_skill.py` | `python3 scripts/vincolo_skill.py --classe FILE`; in una sessione, `/agents` elenca gli agenti |
| 9 | togliere da `claude-progetto.sh` il blocco «Livello utente», poi `rm ~/.claude/settings.json ~/.claude/.generato-da-rumblingstone` e la voce `rumblingstone-tools` da `~/.claude.json` | riaccendere un plugin con `true` sulla sua riga di `enabledPlugins`; `RS_SALTA_SKILL=1` salta la costruzione delle skill | in `/home/user`, `claude -p --output-format stream-json --verbose "ok"`: campi `plugins` e `mcp_servers` dell'evento `init` |

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
