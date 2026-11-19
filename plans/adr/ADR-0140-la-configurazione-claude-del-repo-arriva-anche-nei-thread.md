# ADR-0140 — La configurazione Claude del repo arriva anche nei thread

**Stato**: proposta (2026-11-19), in attesa della scelta del DM sulla card del thread «Applicare le best practice di Claude Code»
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
   La modifica la approva il DM; senza, lo script resta inerte.

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

**Quello che non si sa ancora.** La misura viene da `claude -p`, non da un
thread. Se il runtime dei thread esclude le impostazioni di progetto, lo
script non serve; lo dice solo un thread aperto dopo la modifica dello script
d'avvio. Lo stato passa ad «accettata» solo con quella misura.

**Test**: `scripts/tests/test_claude_progetto.py` (file scritti, percorsi che
esistono, JSON validi, file altrui non toccati, rilancio idempotente, repo come
destinazione ignorato).
