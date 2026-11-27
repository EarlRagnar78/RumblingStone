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
4. **Dodici agenti in `.claude/agents/`, in tre classi**, ognuno con le skill
   precaricate e un corpo corto che rimanda ai `references/`:

   | Classe | Agente | Skill precaricate |
   |---|---|---|
   | Autori | `autore-prosa-gioco` | narrative-style, campaign |
   | Autori | `autore-master` | module-standard, narrative-style, campaign |
   | Autori | `autore-documenti` | prosa-documenti, plans |
   | Tecnici | `sviluppatore` | debugging, automation |
   | Tecnici | `integratore-dm` | automation, debugging |
   | Tecnici | `piattaforma` | plans, edizione |
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

   `integratore-dm` tiene il motore del DM (`dm.py`, `dmcore`, i plugin di
   sistema, il server MCP, il manifest degli strumenti) e lavora in TDD a
   piccoli incrementi; `sviluppatore` tiene il resto di `scripts/`, la CI e
   gli hook. Lo ha chiesto Jfs il 20/11, con due precisazioni che valgono
   per entrambi. Le librerie già usate nel repo sono standard del repo e si
   usano liberamente. Per un problema nuovo si adotta la libreria che è lo
   standard di fatto della comunità invece di riscriverla, e la libreria
   entra come finora per i canali di ADR-0099: unstable, testing per almeno
   14 giorni e 10 run su main, poi stable. ADR-0037 dice come la si dichiara
   per il portatile del DM, non la vieta.

   Il dodicesimo, `piattaforma`, l'ha scelto Jfs su card il 20/11: tiene i
   canali di ADR-0099, le versioni fissate (requirements, registro dei
   binari, azioni della CI), le promozioni, i rilasci e la roadmap, e non
   tocca il codice degli script. `autore-documenti` tiene aggiornata la
   documentazione di tutto il progetto dopo ogni modifica. Non può
   interrogare gli altri agenti, quindi lavora dal diff e dai loro
   resoconti: ogni agente chiude il resoconto con la riga «Documentazione da
   aggiornare:», e `test_agenti.py` lo controlla. Un sottoagente di Claude Code non
   avvia altri agenti: la catena (per esempio `integratore-dm`, poi
   `regolista` sui numeri) la guida il thread principale, e ogni agente
   scrive nel resoconto chi va chiamato dopo.

   Gli agenti sono poi diventati quattordici: il tredicesimo,
   `sincronizzatore-giocato`, viene da [ADR-0149](ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md); il quattordicesimo,
   `custode-memoria` (Tecnici), da [ADR-0151](ADR-0151-la-memoria-del-progetto-ha-uno-specchio-e-un-custode.md).
5. **Nei thread** `claude-progetto.sh` collega `<cartella>/.claude/agents` alla
   cartella del repo e scrive nel CLAUDE.md una riga con l'albero di decisione
   (chi legge, quale skill, quale agente).
6. **Cricchetto `scripts/cricchetto_prosa.py`**, bloccante in CI sulle PR: sui
   file di gioco cambiati (stessa regola dell'hook) nessuna norma che
   `punteggio_mqm` misura ha più difetti che nel punto in cui il ramo si stacca
   da main. Nessuna soglia nuova: norme e rilevatori sono quelli del registro.
   Entra anche nell'hook pre-push, perché `gate_locale` legge `ci.yml`.
7. **Instradamento `scripts/instradamento_agenti.py`**, due hook nei thread.
   Jfs ha chiesto di vincolare il coordinatore a chiamare gli agenti in base
   al lavoro; il coordinatore gira fuori dal repo e i suoi hook non li decide
   il repo, quindi il vincolo sta dove il lavoro arriva. UserPromptSubmit
   legge il messaggio che entra nel thread, riconosce il tipo di lavoro con i
   trigger delle descrizioni delle skill (`instradamento_skill.raggiunte`,
   più poche parole proprie per piattaforma, CI e regole) e mette nel
   contesto l'agente e la catena. Stop registra in `.claude/.uso-agenti.jsonl`
   se il thread li ha chiamati. Nessuno dei due blocca.
8. **Il blocco vero sta sul push.** Jfs l'ha chiesto il 20/11: il
   coordinatore scrive nelle istruzioni di ogni thread una riga
   «Catena: a → b → c», l'hook UserPromptSubmit la legge e la registra. Un
   hook PreToolUse su `git push`, `gh pr create`, `gh pr ready` e sulla
   creazione di una PR via MCP esce 2 se nella sessione manca la chiamata
   Agent di uno di quegli agenti o di `autore-documenti`. La via d'uscita è
   esplicita: `instradamento_agenti.py --deroga "motivo"`, con almeno 15
   caratteri, resta nella trascrizione e nel registro. Senza una catena
   scritta non si blocca niente: il riconoscimento per parole sbaglia, e un
   blocco su un suo errore fermerebbe lavoro legittimo. Lo Stop non blocca:
   un turno che finisce senza push è spesso solo una risposta, e un blocco lì
   costringerebbe a girare a vuoto.

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
- **L'instradamento è per parole e sbaglia.** Sulle 33 frasi vere del DM con
  una skill attesa (`plans/instradamento/casi.json`) il primo agente
  suggerito è giusto in 23, manca in 4 e sbaglia in 6, quasi tutte frasi di
  coerenza che portano alla prosa invece che a `custode-canone`. Per questo
  suggerisce e non blocca, e chiede di scrivere nel resoconto quando lo si
  ignora.
  *(Nota del 2026-11-27: quelle frasi hanno etichette di skill, in parte usate
  anche per tarare i trigger. Su 29 messaggi veri etichettati per agente il
  primo agente è giusto in 7, e sul test in 4 su 18, contro 6 della costante
  «sviluppatore»; misura, set d'oro e cricchetto in
  [ADR-0154](ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md).)*
- **Il cancello del push controlla le chiamate, non il loro esito.** Un
  agente chiamato e ignorato conta come chiamato; un `custode-canone` che
  trova un 🔴 non ferma il push. Una deroga vale per tutta la sessione. Il
  cancello non vede un push fatto da un sottoagente né uno fuori da Claude
  Code. Sui 144 comandi Bash di questo thread il riconoscimento del push ha
  preso gli 8 push veri e 1 heredoc che citava un push dentro una prova.
  Non c'è uno storico su cui tararlo: le catene scritte nascono adesso. La
  misura è `--riepilogo` dopo una settimana: push passati, bloccati, in
  deroga.
  *(Nota del 2026-11-27: la misura non si è potuta fare, perché i registri
  `.claude/.uso-*.jsonl` sono in `.gitignore` e restano nel container; per
  l'instradamento la sostituisce il set d'oro di
  [ADR-0154](ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md).)*
- La norma «il box che promette» (§2-quater di `read-aloud-adulti.md`, misura
  `misura_craft --apertura`) arriva con la #508. Il cricchetto la vedrà
  quando entra fra le norme di `punteggio_mqm`, non prima.

**Correzione del 25/11: gli hook non arrivavano più nei thread.** Dal 22/11
circa i thread del progetto partono in `/home/user` e ignorano il
`/home/user/.claude/settings.json` che `claude-progetto.sh` scrive (ADR-0140).
Nei log diagnostici di Claude Code le sessioni del 20-21/11 lanciavano 2 hook
SessionStart, quelle dal 23/11 uno solo, quello della piattaforma;
`.claude/.skills-sync-status` è fermo al 20/11. Il primo thread partito dopo il
merge della #510 («Rendere epico il passaggio da ARC-07 ad ARC-08») non aveva
gli hook di questo ADR (instradamento, cancello del push, vincolo della
prosa), nessuna skill `rumblingstone-*` nell'elenco, nessun server
`rumblingstone-tools`, e tutti i circa 35 plugin dell'account accesi
(finance, small-business, marketing…). Gli agenti invece arrivavano, perché
`.claude/agents` è una cartella collegata e non passa da `settings.json`.

`claude-progetto.sh` ora scrive anche a livello utente, che si legge sempre:

- `~/.claude/settings.json`, copia di quello del repo con gli hook a percorso
  assoluto, `enabledPlugins` e le regole `Read` ancorate rese assolute con
  `//`;
- in `~/.claude.json` la sola voce `rumblingstone-tools` di `mcpServers`;
- le skill del repo in `~/.claude/skills`, costruite prima che parta la
  sessione (8 secondi), invece di aspettare l'hook d'avvio.

Le impostazioni utente scritte da altri non si toccano: lo script sovrascrive
`~/.claude/settings.json` solo se manca o se è elencato in
`~/.claude/.generato-da-rumblingstone`.

Nello stesso cambio `.claude/settings.json` spegne cinque plugin arrivati
sull'account dopo la scelta del 19/11, con la stessa regola (restano accesi
solo i plugin usati nello storico): `superpowers`, il cui hook SessionStart
imponeva di invocare le sue skill generiche «anche all'1% di probabilità», in
concorrenza con l'instradamento del repo; `agentic-council`, 38 agenti in
concorrenza con i 12 del repo; `ai-mentor`, `frontend-design`, `skill-creator`.

Prova: una sessione Claude Code nuova lanciata in `/home/user` nello stesso
container. Con la configurazione utente scattano l'hook di instradamento
(UserPromptSubmit) e il PreToolUse su Bash, `rumblingstone-tools` è connesso,
le skill del repo ci sono e i plugin accesi sono esattamente i 12 voluti.
Senza (file spostato): nessun hook del repo, 39 plugin.
`scripts/tests/test_claude_progetto.py` ha 9 prove verdi, tre nuove.

Quello che resta scoperto:

- un plugin che l'account aggiunge in futuro si accende da solo finché
  qualcuno non lo mette in `enabledPlugins`;
- i container già partiti devono rilanciare `claude-progetto.sh`;
- del cambio della piattaforma si conosce l'effetto, non la causa;
- la prova è una sessione headless nello stesso container, non ancora un
  thread vero.

## Come si torna indietro

Togliere il gruppo `PreToolUse` da `.claude/settings.json` spegne l'hook, e
i gruppi `UserPromptSubmit` e `Stop` spengono l'instradamento, il secondo
gruppo `PreToolUse` (matcher `Bash|mcp__github__create_pull_request`) spegne il
cancello del push;
togliere il passo «Prosa — il testo cambiato non peggiora» da `ci.yml` spegne
il cricchetto. Gli agenti si tolgono cancellando `.claude/agents/`. Dettagli in
[`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`](../../docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md).

## Come si misura

- Uso: `python3 scripts/vincolo_skill.py --riepilogo` (blocchi, passaggi,
  promemoria). Da ripetere dopo una settimana di thread, contro lo zero del
  campione del 20/11. *(Nota del 2026-11-27: il registro
  `.claude/.uso-skill.jsonl` è locale al container, e la ripetizione non si è
  potuta fare; vedi [ADR-0154](ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md).)*
- Classe di un file: `python3 scripts/vincolo_skill.py --classe FILE`.
- Agenti: `python3 scripts/instradamento_agenti.py --riepilogo` (suggerimenti
  dati, turni chiusi, quanti hanno chiamato il primo agente suggerito);
  `--prova "testo"` mostra che cosa suggerirebbe.
- Cricchetto: `python3 scripts/cricchetto_prosa.py --rispetto-a origin/main`.
