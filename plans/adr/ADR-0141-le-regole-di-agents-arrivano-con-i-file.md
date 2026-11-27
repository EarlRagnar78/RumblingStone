# ADR-0141 — Le regole di AGENTS.md arrivano a Claude con i file a cui servono

**Stato**: accettata (2026-11-19)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19, card «Quale tecnica di contesto adotto per prima nel repo?»: scelta «Regole a percorso da AGENTS.md».
**Rapporti**: segue [ADR-0140](ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md) (la configurazione del repo nei thread). AGENTS.md resta la fonte di [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md).

## Contesto

AGENTS.md pesa 26 KB, circa 7.500 token. Il CLAUDE.md dei thread diceva di
leggerlo prima di toccare campagna, skill, script o booklet, quindi entrava
intero in quasi ogni compito, anche dove servono due sezioni su sei. Gli altri
agenti (Codex, Copilot, Cursor…) leggono AGENTS.md da soli: il file non si
può spezzare.

Claude Code ha un meccanismo documentato per questo: le regole in
`.claude/rules/*.md`. Una regola con `paths:` entra nel contesto quando
l'agente legge un file che corrisponde; una senza `paths:` entra al primo file
letto. Provato il 2026-11-19 in una cartella di prova e poi nel repo: le
regole del repo si caricano anche quando Claude parte nella cartella che
contiene il clone, con i percorsi relativi al repo.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **AGENTS.md resta la fonte; uno script ne ricava le regole e un test le tiene allineate** (scelta) | una fonte sola per tutti gli agenti; caricamento deterministico per percorso; il test garantisce che nessuna riga vada persa | le regole sono una copia generata; il nucleo sempre presente resta grande |
| Spezzare AGENTS.md a mano in regole | niente generatore | gli altri agenti perdono le regole o le trovano doppie |
| RAG o grafo sulle istruzioni | scelta fine dei pezzi | non deterministico: una regola obbligatoria si può perdere |
| Lasciare com'è | niente da fare | 26 KB a ogni compito |

## Decisione

1. **`scripts/regole_claude.py`** divide AGENTS.md ai titoli `##` (e ai `###`
   che la sua tabella nomina) e scrive cinque regole in `.claude/rules/rs-*.md`:

   | Regola | Quando entra | Sezioni |
   |---|---|---|
   | `rs-nucleo` | sempre, al primo file del repo | contenuto del repo, principio delle skill, regole d'oro G1-G6, tabella «Cosa carico», «Quando un agente risponde», DO/DON'T |
   | `rs-campagna` | archi, `10-stand-alone/`, `campaign/`, `Bestiario/`, `PG/` | convenzioni di campagna, politica delle regole |
   | `rs-inventario-skill` | `skills/`, script delle skill, `.claude/` | inventario delle diciotto skill |
   | `rs-strumenti-esterni` | `.claude/`, `.mcp.json`, server MCP, manifest dei tool | strumenti esterni |
   | `rs-agenti-supportati` | skill e contenuti | agenti supportati, protocollo dello stato delle skill |

   La tabella ha l'obbligo di coprire ogni sezione una volta sola: una
   sezione nuova senza regola ferma lo script.
2. **`--check`** esce 1 se `.claude/rules/` non è allineata;
   `scripts/tests/test_regole_claude.py` lo lancia in CI e verifica che le
   regole rimesse insieme contengano ogni sezione.
3. **Il CLAUDE.md dei thread** (`claude-progetto.sh`) non dice più di leggere
   AGENTS.md intero. Tiene una riga sola sempre presente: `fase1.py` prima di
   modificare (G6), perché le regole arrivano dopo il primo file letto e nella
   prova, senza quella riga, l'agente aveva risposto senza lanciare `fase1.py`.

## Le conseguenze

**Misura deterministica** (`regole_claude.py --misura`, caratteri caricati
dal primo file del compito contro AGENTS.md intero, 26.198):

| Compito | Regole | Caratteri | Rispetto ad AGENTS.md |
|---|---|---|---|
| script del repo | nucleo | 14.283 | −45% |
| piano o ADR | nucleo | 14.283 | −45% |
| master d'arco | nucleo, campagna, agenti | 21.9k | −16% |
| skill | nucleo, inventario, agenti | 20.2k | −22% |
| configurazione Claude | quattro su cinque | 22.7k | −12% |

**Misura su un compito vero** (`claude -p` dalla cartella del clone, «devo
modificare scripts/dm.py, preparati»), contesto all'ultimo turno: main 79.560
token (ha letto AGENTS.md, poi `fase1.py`), ramo 74.112 (regole arrivate con
`dm.py`, poi `fase1.py`): −5.448, −6,8%. Una corsa per lato: la cifra ha il
rumore di un agente, la tabella sopra no.

**Quello che non migliora.** Il nucleo è il 55% di AGENTS.md, perché le regole
d'oro e la tabella delle skill valgono per ogni compito. Ridurlo vuol dire
riscrivere AGENTS.md, che è un'altra decisione. Le regole arrivano al primo
file letto: una risposta data senza aprire file non le vede, come prima non
vedeva AGENTS.md. Gli altri agenti non cambiano.
