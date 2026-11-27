# ADR-0140 — La configurazione Claude del repo arriva anche nei thread

**Stato**: accettata (2026-11-19), dopo la prova in un thread vero (sotto)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19, chat di progetto: verificare quali best practice di Claude Code il repo usa, adottare quelle utili e misurare il miglioramento contro main.
**Rapporti**: rende effettivi nei thread l'hook di [ADR-0030](ADR-0030-server-mcp-sui-tool.md) (server `rumblingstone-tools`), gli `skillOverrides` di `.claude/settings.json` e l'instradamento delle skill di [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md). L'audit completo sta fuori dal repo, in `/mnt/project-files/best-practice-claude-code-2026-11-19/AUDIT.md`.

## Contesto

Nei thread del progetto su claude.ai Claude Code parte nella cartella che
contiene il clone (`/home/user`), non nel repo. Claude Code legge CLAUDE.md,
AGENTS.md, `.claude/settings.json` e `.mcp.json` dalla cartella di lavoro e
dalle sue antenate; le sottocartelle no. Misurato nel thread del 19/11:

- `AGENTS.md` non è nel contesto iniziale;
- l'hook SessionStart non è girato (`.claude/.skills-sync-status` non esiste,
  `.claude/skills/` non esiste);
- `anthropic-skills:dnd-35-rules`, spenta dal repo, compare fra le skill;
- il server `rumblingstone-tools`, citato dalle istruzioni di progetto, manca.

Le regole del repo arrivano a un thread solo dalle istruzioni di progetto,
dalla memoria del progetto e da ciò che Claude decide di leggere.

L'articolo sulle best practice incollato dal DM consiglia un CLAUDE.md corto
con rimandi ai file di dominio (progressive disclosure) e hook per le regole
che devono valere sempre. Le sue cifre sono di terzi e qui non fanno da
obiettivo.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Script del repo, lanciato dallo script d'avvio dell'ambiente, che scrive nella cartella di lavoro un CLAUDE.md corto, il `settings.json` del repo con l'hook a percorso assoluto e il `.mcp.json`** (scelta) | una fonte sola, il repo; il CLAUDE.md rimanda e non incorpora; funziona anche per un altro nome di cartella | serve una riga nello script d'avvio, che cambia solo il DM; il `settings.json` generato è una copia |
| CLAUDE.md con `@RumblingStone/AGENTS.md` | una riga | carica a ogni thread 24.894 caratteri (circa 7.000 token stimati), anche quando il compito non tocca la campagna: è l'opposto della progressive disclosure |
| Collegamenti simbolici a `.claude/` e `.mcp.json` del repo | niente copia | l'hook e il server usano percorsi relativi alla cartella di progetto e fallirebbero; i link non si scrivono con Edit |
| Lasciare com'è | niente da fare | hook, skill del repo e tool del DM restano inerti nel modo di lavoro più usato |

## Decisione

1. **`scripts/claude-progetto.sh [cartella]`** scrive nella cartella che
   contiene il repo (o in quella data):
   - `CLAUDE.md` di sei righe: dove sta il repo, quando leggere `AGENTS.md`,
     `MEMORIA.md` e la memoria storica, il server dei tool, lo stato delle skill;
   - `.claude/settings.json`: quello del repo, con `$CLAUDE_PROJECT_DIR`
     sostituito dal percorso del repo;
   - `.mcp.json`: quello del repo, con gli argomenti a percorso assoluto.

   Non sovrascrive un file che non ha scritto lui (elenco in
   `.claude/.generato-da-rumblingstone`) e non scrive mai dentro il repo.
2. **L'hook SessionStart** trova il repo dal proprio percorso invece che da
   `CLAUDE_PROJECT_DIR`. Lanciato dalla radice del repo fa esattamente quello
   che faceva prima.
3. **Lo script d'avvio dell'ambiente `RumblingStone-corpus`** riceve una riga:
   `if [ -x RumblingStone/scripts/claude-progetto.sh ]; then RumblingStone/scripts/claude-progetto.sh "$PWD" || true; fi`.
   Approvata dal DM il 2026-11-19; resta inerte finché lo script non è su main.
4. **I connettori che il progetto non usa** (Gmail, Google Drive, Channel3,
   Clipkit, Mobbin, Microsoft Learn, MDN, Shutterstock, bioRxiv, pg-aiguide)
   sono negati in `permissions.deny` del `settings.json` del repo (scelta del
   DM sulla card del 2026-11-19). Prova su un server di plugin con `claude -p`:
   una regola `deny` sul server toglie i suoi tool dall'elenco (da 84 a 58
   tool, 528 token in meno). Sui connettori di claude.ai la prova si può fare
   solo in un thread.

5. **I plugin dell'account che il repo non ha mai usato** sono spenti solo
   per questo progetto con `enabledPlugins: false` (scelta del DM del
   2026-11-19: «lascia i plugin che sono stati usati nel repo davvero nello
   storico»). Restano accesi `pdf-viewer`, `review` e `tdd`, gli unici con una
   prova nello storico: li ha accesi apposta la PR #205 (riga del 2026-10-02
   di `plans/CHANGELOG.md`). Per gli altri 29 né commit, né changelog, né
   memoria storica, né i file del progetto mostrano un uso; `engineering`,
   `docs` e `reflexion` compaiono solo come skill «solo nome» nella stessa
   PR, che è configurazione e non uso.

   **Correzione dello stesso giorno** (scelta del DM sulla card del
   2026-11-19, dopo la domanda «quelli delle tecniche dello sviluppo
   software non avrebbe senso tenerli?»): tornano accesi anche i nove
   plugin di metodo di sviluppo, `sdd`, `sadd`, `engineering`, `reflexion`,
   `docs`, `fpf`, `ddd`, `recursive-decomposition` e `mcp`, pur senza una
   prova d'uso nello storico. Restano spenti gli altri 20.

## Le conseguenze

**Misura contro main** (Claude Code 2.1.328 in modalità `-p`, stessa
installazione dei thread, cartella che contiene il clone, risposta di una
parola):

| | main | con lo script |
|---|---|---|
| Server `rumblingstone-tools` | assente | connesso, 135 tool |
| Hook SessionStart | non gira | gira (stato `syncing`, poi skill del repo in `~/.claude/skills/`) |
| Skill del repo nell'elenco | 0 | 18 |
| `anthropic-skills:dnd-35-rules` (spenta dal repo) | presente | assente |
| Contesto iniziale | 54.689 token | 59.541 token (+4.852, +8,9%) |

**Quello che si paga.** Circa 4.900 token in più a ogni thread: i nomi dei
135 tool del DM e le descrizioni delle 18 skill del repo. È il costo di avere
l'instradamento delle skill e i tool che AGENTS.md e le istruzioni di progetto
danno per presenti. Nel thread del 19/11 il contesto iniziale era di 131.128
token, e circa 113.000 caratteri venivano da plugin e connettori dell'account
che il progetto non usa: spegnerli, a mano del DM, vale molto di più di questi
4.900.

**Prova in un thread vero.** Il 2026-11-19 lo script è stato lanciato a mano
in `/home/user` dentro il thread che ha scritto questo ADR. Appena il
`settings.json` generato ha ricevuto le regole `deny`, il thread ha perso i
tool dei dieci connettori; al riavvio successivo della sessione l'hook
SessionStart è girato (stato `ok 916ed032 2026-11-19T06:47:01Z`) e
`rumblingstone-tools` si è connesso. Il runtime dei thread legge quindi
`/home/user/.claude/` e `/home/user/.mcp.json`.

*Nota del 25/11.* Dal 22/11 circa non è più vero: i thread partono ancora in
`/home/user` ma ignorano il `.claude/settings.json` di quella cartella (nei
log diagnostici gli hook SessionStart passano da 2 a 1 dal 23/11). La
cartella di progetto non basta più, e `claude-progetto.sh` scrive anche a
livello utente (`~/.claude/settings.json`, la voce `rumblingstone-tools` in
`~/.claude.json`, le skill in `~/.claude/skills`). Misura e limiti nella
correzione del 25/11 di
[ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md).

**Plugin spenti** (`claude -p` dalla cartella del clone dopo lo script, main
contro ramo): plugin da 36 a 7, server MCP da 102 a 2 (quelli che falliscono
all'avvio da 95 a 0), skill da 257 a 73, contesto iniziale da 59.670 a 53.965
token (−5.705, −9,6%). Rispetto alla cartella senza nessuna configurazione
(56.602 token) il saldo è −2.637 token, con i tool e le skill del repo
presenti.

**I nove plugin di sviluppo riaccesi** (stessa misura, main 983791d0 contro
ramo): plugin da 7 a 16, skill da 73 a 115, server MCP da 2 a 12, contesto
iniziale da 54.372 a 56.719 token (+2.347, +4,3%). Con `/context` la stima è
da 35,4k a 36,4k. I dieci server in più sono tutti di `engineering` (Slack,
Linear, Asana, Atlassian, Notion, GitHub, PagerDuty, Datadog, Google Calendar,
Gmail): nove falliscono all'avvio per la rete del container e Datadog chiede
l'accesso, quindi nessuno porta tool, solo avvisi.

**Test**: `scripts/tests/test_claude_progetto.py` (file scritti, percorsi che
esistono, JSON validi, file altrui non toccati, rilancio idempotente, repo come
destinazione ignorato).
