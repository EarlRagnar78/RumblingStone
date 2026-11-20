# ADR-0146 — Le skill di prosa si caricano per vincolo, non per memoria

**Stato**: proposta (2026-11-20)
**Data**: 2026-11-20
**Decisione-fonte**: il DM (Jfs), 2026-11-20, nel thread «Vincolare gli agenti all'uso delle skill»: «mi sembra che si perdano sempre pezzi», agenti specializzati «divisi in categorie e classi coerenti»; sulla card del cancello CI sceglie il cricchetto bloccante, «niente cancelli di prosa nuovi [...] deve forzare l'utilizzo»; sulla card degli agenti «mettili tutti e tre».
**Rapporti**: si appoggia a [ADR-0140](ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md) (la config arriva nei thread) e [ADR-0141](ADR-0141-le-regole-di-agents-arrivano-con-i-file.md) (regole a percorso); usa i rilevatori di [ADR-0059](ADR-0059-il-punteggio-di-qualita-e-mqm-adattato.md) e gli strati di [ADR-0058](ADR-0058-orchestrazione-a-strati-delle-skill.md); lascia il giudizio sulla qualità al voto alla cieca di [ADR-0093](ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md). Supera, per scelta del DM, la regola di memoria «niente cancelli di prosa nuovi».

## Contesto

AGENTS.md chiede di caricare `rumblingstone-narrative-style` e di leggerne i
`references/` prima di scrivere prosa di gioco. Nessuno lo controllava. Il
20/11 ho letto le trascrizioni di cinque thread recenti (dossier di ARC-09,
tattica di Skullcrusher, Eroi di Hammerfist, carte del Drappo, booklet di
ARC-07): nove pagine, 188 chiamate a strumenti, **zero** invocazioni di una
skill e **zero** letture di `skills/*/SKILL.md` o dei `references/`. È un
campione: le trascrizioni si leggono cento eventi alla volta e ho letto le
pagine più recenti di ogni thread, non le trascrizioni intere.

La causa è strutturale. All'avvio un thread vede di ogni skill solo nome e
descrizione; il corpo entra nel contesto solo se l'agente decide di
chiamarla, e la decisione non lascia traccia. Una norma in AGENTS.md chiede
memoria a chi non ne ha.

Misure sullo storico per tarare il vincolo (ultimi 400 commit senza merge):
2.944 modifiche a file di gioco, di cui 184 aggiungono un box read-aloud e 16
toccano un file di sola prosa. Un vincolo su tutti i file di gioco avrebbe
disturbato 2.944 volte; uno su prosa e box disturba circa 200 volte.

## Alternative considerate

| Opzione | Obbliga l'uso? | Costo | Scartata perché |
|---|---|---|---|
| Solo la norma in AGENTS.md (com'era) | no | zero | è la situazione misurata: zero caricamenti |
| Una skill indice che instrada | no | una skill in più | va invocata, ed è proprio il passo che salta |
| Albero di decisione nel CLAUDE.md dei thread | no, ma è sempre in contesto | una riga | tenuta, insieme all'hook |
| **Hook PreToolUse che blocca la prosa senza skill** (scelta) | sì | 45 ms per scrittura | — |
| Hook su ogni file di gioco | sì | blocca anche gli statblock | 2.944 interruzioni contro circa 200 |
| Solo misura in CI, non bloccante | no | zero | il DM: «la misura da sola non obbliga» |
| **Cricchetto bloccante sul testo cambiato** (scelta del DM) | no, ma ferma il peggioramento | circa 1 s in CI | — |

## Decisione

1. **Hook `scripts/vincolo_skill.py`** (PreToolUse su Edit, Write,
   MultiEdit, registrato in `.claude/settings.json`). Divide i file in tre
   classi. La **prosa pura** (introduzioni e capitoli dei volumi in
   `homebrew/volume-*/NN-*.md`, handout, recap, appendici, teaser) si blocca
   se la sessione non ha caricato `rumblingstone-narrative-style`. I **file
   misti** (master, schede del Bestiario) si bloccano solo se il testo nuovo
   contiene un box, riconosciuto da `misura_craft.box_read_aloud`. I
   **documenti** (`plans/`, `docs/`, `skills/`, i file della radice) non si
   bloccano mai: se manca `rumblingstone-prosa-documenti` arriva un
   promemoria. Con la skill caricata, i quattro `references/` obbligatori non
   ancora letti arrivano come promemoria (G1). Archivi, `.hb.md` e codice
   passano in silenzio. Un errore dell'hook lascia passare la scrittura.
2. **La skill conta come caricata** se la sessione l'ha invocata (strumento
   Skill o comando `/nome`), se un sottoagente l'ha invocata nella propria
   trascrizione, o se l'agente che scrive la precarica nel campo `skills:`.
3. **Registro d'uso** in `.claude/.uso-skill.jsonl` (ignorato da git): una
   riga per decisione su un file vincolato. `vincolo_skill.py --riepilogo`
   dà la misura che oggi costa una lettura di trascrizioni.
4. **Dieci agenti in `.claude/agents/`, in tre classi**, ognuno con le skill
   precaricate e un corpo corto che rimanda ai `references/`:

   | Classe | Agente | Skill precaricate |
   |---|---|---|
   | Autori | `autore-prosa-gioco` | narrative-style, campaign |
   | Autori | `autore-master` | module-standard, narrative-style, campaign |
   | Autori | `autore-documenti` | prosa-documenti, plans |
   | Tecnici | `sviluppatore` | debugging, automation |
   | Tecnici | `cartografo` | mapmaking |
   | Tecnici | `impaginatore` | editoria, edizione |
   | Tecnici | `art-director` | art-direction |
   | Tecnici | `regolista` | dnd-35-srd, pathfinder-1e-srd, npc-villain-boosting, campaign |
   | Verificatori | `lettore-a-freddo` | playtest, narrative-style |
   | Verificatori | `custode-canone` | campaign, forgotten-realms-lore |

   I verificatori sono in sola lettura (niente Edit né Write). Le classi
   ricalcano gli strati di ORCHESTRAZIONE: gli Autori portano la L1 e la L2,
   i Tecnici la L3 e la L4, i Verificatori il canone e il collaudo. Nessun
   agente carica le due prose insieme (ADR-0035); `rumblingstone-indagine`
   si carica su richiesta dall'autore della prosa. `test_agenti.py` lo
   controlla.
5. **Nei thread** `claude-progetto.sh` collega `<cartella>/.claude/agents` alla
   cartella del repo e scrive nel CLAUDE.md una riga con l'albero di decisione
   (chi legge, quale skill, quale agente).
6. **Cricchetto `scripts/cricchetto_prosa.py`**, bloccante in CI sulle PR: sui
   file di gioco cambiati (stessa regola dell'hook) nessuna norma che
   `punteggio_mqm` misura ha più difetti che nel punto in cui il ramo si stacca
   da main. Nessuna soglia nuova: norme e rilevatori sono quelli del registro.
   Entra anche nell'hook pre-push, perché `gate_locale` legge `ci.yml`.

## Le conseguenze

- Una sessione che scrive un handout o un box senza aver caricato la skill
  viene fermata, con il motivo e la strada (caricarla o affidare il lavoro ad
  `autore-prosa-gioco`).
- Sugli ultimi 300 commit il cricchetto avrebbe controllato 8 file su 157
  file di gioco cambiati e ne avrebbe fermato 1 (un box con una parentesi in
  più nella guida del DM di ARC-08). Lo storico del clone è corto, quindi il
  campione è piccolo.

**Quello che si paga.**

- **Caricata non vuol dire seguita.** L'hook garantisce che la skill sia nel
  contesto, non che l'agente la applichi. Il promemoria sui `references/` è
  un promemoria, non un blocco.
- **Il cricchetto vede la forma, non la qualità.** Un box di dieci righe senza
  tic può essere piatto e passa. E un cancello sulle metriche spinge a
  scrivere per la metrica. Il giudizio resta il voto alla cieca del DM.
- **Le scritture da Bash non passano dall'hook**: un `sed -i` o un heredoc
  su un file di prosa lo aggirano. Il cricchetto in CI le prende solo se
  peggiorano una norma.
- I modelli della prosa pura sono espressioni sui nomi dei file. Un tipo di
  file nuovo (per esempio un volume con un'altra cartella) resta «misto»
  finché non si aggiunge il modello; un test controlla che ogni modello peschi
  almeno un file.
- Il contesto: ogni agente costa circa 60 token di descrizione nella sessione
  principale; le skill precaricate pesano solo nel contesto del sottoagente
  (`autore-master` porta circa 53 KB di SKILL.md).
- La norma «il box che promette» (§2-quater di `read-aloud-adulti.md`, misura
  `misura_craft --apertura`) arriva con la #508. Il cricchetto la vedrà
  quando entra fra le norme di `punteggio_mqm`, non prima.

## Come si torna indietro

Togliere il gruppo `PreToolUse` da `.claude/settings.json` spegne l'hook;
togliere il passo «Prosa — il testo cambiato non peggiora» da `ci.yml` spegne
il cricchetto. Gli agenti si tolgono cancellando `.claude/agents/`. Dettagli in
[`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`](../../docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md).

## Come si misura

- Uso: `python3 scripts/vincolo_skill.py --riepilogo` (blocchi, passaggi,
  promemoria). Da ripetere dopo una settimana di thread, contro lo zero del
  campione del 20/11.
- Classe di un file: `python3 scripts/vincolo_skill.py --classe FILE`.
- Cricchetto: `python3 scripts/cricchetto_prosa.py --rispetto-a origin/main`.
