# ADR-0030 — Il server MCP esiste, ed è read-only per difetto

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: lotto **G1** di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md)
**Chiude la promessa di**: [ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) ·
**Progetto per esteso**: [`SPEC-SERVER-MCP.md`](../SPEC-SERVER-MCP.md) ·
**Vincolata da**: [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md)

## Contesto

ADR-0012 ha eletto `scripts/tools.manifest.json` a **fonte di verità** dei tool, e
da lì si generava `docs/tools/mcp-tools.json`: 48 voci con descrizione e
`inputSchema` completo. Un descrittore MCP perfetto — **e nessun server che lo
leggesse**.

Una fonte di verità senza consumatori non resta vera. Lo si è visto appena il
server ha provato a usarla davvero:

- **tre delle 48 voci erano cartelle**, non programmi. `converters/html-to-markdown`
  e `converters/pdf-to-md-engine` hanno per «invocazione» la stringa *«(vedi
  converters/…/README)»*, e `converters/image-to-webp` è anch'essa una directory.
  Il descrittore prometteva tre tool che non possono partire;
- **`invocation` non è un comando**, è una riga d'esempio per gli umani: mescola
  l'eseguibile con segnaposto e flag di comodo — `MANIFEST.json`, `<cartella>`,
  `--all`, `--check`, `--stampa`. Nove tool su quarantasei ne hanno uno. Un server
  che la usasse verbatim lancerebbe `--all` che nessuno ha chiesto;
- **nessuna voce portava gli effetti collaterali.** Il manifest sa che
  `state_apply` scrive il canone e fa commit; `mcp-tools.json` no. Un client non
  distingueva un validatore da uno script che tocca il canone.

Nessuno di questi tre difetti era visibile prima, perché **niente leggeva il
descrittore**.

## Decisione

**`scripts/mcp_server.py`**: JSON-RPC 2.0 su stdio, stdlib, catalogo derivato dal
manifest. Espone `initialize`, `tools/list`, `tools/call`, `ping`.

Le decisioni che contano sono tre.

### 1. Il comando si deriva da `path` + `language`, mai da `invocation`

`invocation` resta quello che è: documentazione per un essere umano. Il fatto a
macchina sono il percorso e il linguaggio. E un tool si espone **solo se il suo
`path` è un file eseguibile**: `mcp_eseguibile()` sta in `tools_manifest.py` — cioè
in un posto solo — e la usano sia l'emettitore sia il server. Con due copie
diventano due regole, e una invecchia in silenzio.
`mcp-tools.json` scende da **48 a 46 voci**, ed è una correzione, non una perdita:
le tre tolte non partivano.

### 2. Sei difese, perché è una superficie d'esecuzione

Questo processo lancia 46 programmi per conto di un agente. Le difese sono
elencate in `SPEC-SERVER-MCP.md` §4 e hanno un test a testa:
**S-1** solo allowlist · **S-2** niente shell (argv come lista, `shell=False`) ·
**S-3** argomenti validati sullo schema prima di partire · **S-4** percorsi
confinati sotto la radice · **S-5** read-only per difetto · **S-6** timeout 120 s e
tetto di 256 KiB.

### 3. S-5 non nasce da un manuale di sicurezza, nasce da qui

**I cinque tool che scrivono contenuto — `session_wizard`, `state_apply`, `dm`,
`new-campaign-group`, `import_html_module`, quattro dei quali fanno anche commit —
sono elencati ma non partono senza `--allow-write`.**

ADR-0007 vuole che il canone si scriva su un branch di gruppo, dopo la sessione,
con l'occhio del DM sopra. Un agente che li lanciasse perché «sembrava il passo
successivo» non violerebbe una regola di sicurezza: violerebbe **il flusso di
lavoro del DM**, che è peggio, perché lì per lì non se ne accorge nessuno.

Sono **elencati e non nascosti** di proposito, con il motivo scritto nella loro
descrizione. Un tool invisibile diventa una richiesta fatta a mano, di nascosto.

### 4. Un'uscita ≠ 0 è un risultato, non un guasto

`validate_lingua` esce **1** per progetto (in CI è `continue-on-error`): il suo
codice 1 è un **referto**. Il server restituisce quindi `isError: true` **nel
risultato**, non un errore JSON-RPC, e vi allega **il significato del codice preso
dal manifest** — per `suggest_encounter` il 3 vuol dire *«nessuna proposta
assemblabile»*. È la differenza fra un agente che ritenta a caso e uno che cambia
parametri. Gli errori JSON-RPC restano per le chiamate che **non sono mai partite**.

## Conseguenze

**Buone.**
- La fonte di verità ha finalmente un lettore, e ha subito trovato tre difetti che
  nessuno vedeva.
- Le annotazioni MCP (`readOnlyHint`, `destructiveHint`, `idempotentHint`)
  arrivano al client: prima `validate_prosa` e `state_apply` si assomigliavano.
- Il gate CI fa **parlare il server sul suo trasporto**, non solo passare i test
  interni. Un server che supera i test e non risponde a `tools/list` non serve.

**Il prezzo, dichiarato.**
- **Una superficie d'esecuzione in più.** Non c'era e adesso c'è. È il motivo per
  cui le difese sono scritte su un documento a parte e hanno un test a testa.
- **`--allow-write` è un interruttore grosso**: acceso, abilita tutti e cinque. Un
  permesso per singolo tool sarebbe più fine; è un'aggiunta che si fa quando serve,
  non prima.
- **Una chiamata alla volta**: nessuna concorrenza. Due `build_monster_catalog`
  insieme si pesterebbero i piedi, e il lock è cosa del tool, non del server.
- **Solo `tools`**: niente `resources` né `prompts`. Sono altre superfici e si
  aggiungono quando qualcuno le chiede.

**Cosa NON decide.** Non decide che gli agenti debbano usare questo canale invece
della CLI: chi sta al terminale continua con `dm.py`. E non copre cosa i tool
facciano una volta partiti — il server garantisce **quale** programma parte e con
quali argomenti, non cosa quel programma scrive.
