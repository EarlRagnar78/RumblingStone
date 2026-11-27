# ADR-0111 — Il sistema di gioco è un plugin di dati, scelto in un file solo

**Stato**: accettata (2026-11-08, il DM: «Tutti e due, D4 sì», insieme ad ADR-0112). D1-D5 di [PIANO-SISTEMI-DI-GIOCO-PLUGIN](../PIANO-SISTEMI-DI-GIOCO-PLUGIN.md) decise con le consigliate: TOML, sistema per cartella in `sistemi.toml`, un lotto per PR, l'ambientazione in una sezione separata, le skill dei sistemi attivi e di rinforzo
**Data**: 2026-11-07
**Decisione-fonte**: il DM (Jfs), 2026-11-07: *«l'idea di plugin sia per tutto il giro di skill, agent ecc. e per poi introdurre con la stessa logica un set di regole diverso senza reinventare di nuovo la ruota, in modo ingegneristico, misurabile e deterministico […] con un file di configurazione generale dove vengano attivati o disattivati i sistemi di gioco e che presenti anche quelli supportati dal repo e dai tool (una specie di ini file)»*
**Rapporti**: usa ADR-0110 (termini ufficiali, tabelle e cancello, ramo `regole-ufficiali`) come primo contenuto dei plugin; rispetta [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (solo libreria standard: `tomllib` c'è da Python 3.11), [ADR-0103](ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md) (le fonti in cache), [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (si entra in testing con la misura), ADR-0012 (il manifest dei tool è la fonte di verità).

## Contesto

Il censimento del 2026-11-07 ([CENSIMENTO.json](../esperimenti/sistemi-plugin-2026-11-07/CENSIMENTO.json), script deterministico accanto) ha letto 202 script. **31 dipendono dal sistema di gioco**: 17 hanno regole cablate nel codice (tabelle SRD 3.5 e bersagli PF1e in `dmcore/tabelle.py`, `progressione.py`, `caratteristiche.py`, `incantesimi.py`, le soglie PE in `update_xp.py`, il tesoro in `suggest_loot.py`), 5 hanno liste di termini per sistema, 2 decidono il sistema da soli, 7 stampano etichette d20. Gli altri 171 sono neutri.

Il sistema di un modulo oggi si decide in **tre modi** che non si parlano: dal percorso (il Drappo in `dmcore/censimento.py` e in `build_monster_catalog.py`, `e_pf1()` sul ramo delle regole ufficiali), dalla riga «**Sistema:**» in 26 master scritta in 10 grafie diverse, e dal campo `sistema` in 3 profili di `plans/domande-developer.json`. La lista dei termini 5e vietati esiste in **due copie** con forme diverse (`validate_modules`, `validate_standalone`). Aggiungere un sistema della famiglia d20 oggi vuol dire toccare **24 file** di codice.

In questo repo PF1e ha due ruoli: è il sistema base di due moduli (il Drappo, il Giardino a Qasr al-Milah) ed è la **fonte di rinforzo** dei moduli 3.5 (template, bersagli per GS, la versione più potente scelta dal DM). Un plugin deve sapere fare tutte e due le cose.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Plugin di dati** (cartella `sistemi/<id>/` con un descrittore TOML e i file di tabelle; un caricatore unico; le capacità dichiarate nel manifest dei tool) | deterministico, leggibile dal DM, nessuna dipendenza, controllabile con un cancello; i dati di ADR-0110 entrano come sono | il codice che oggi ha le tabelle va riscritto per leggerle (lotti L4-L5); una regola che è un algoritmo e non una tabella resta codice |
| Plugin di codice (moduli Python caricati con `importlib.metadata` o `pluggy`) | ogni sistema può cambiare anche gli algoritmi | codice eseguito per configurazione, più difficile da verificare e da leggere; `pluggy` è una dipendenza; per due sistemi d20 è più di quanto serve |
| Stato attuale con `if pf1e` dove serve | nessun lavoro ora | ogni sistema nuovo tocca 24 file; i tre rilevamenti continuano a divergere |
| Un ramo o un fork per sistema | isolamento totale | i miglioramenti vanno portati a mano su ogni ramo: è il problema che ADR-0090 ha chiuso per i gruppi |

## Decisione

**Il sistema di gioco entra nel repo come plugin di dati, e un file solo dice quali sono attivi e quale sistema usa ogni modulo.**

1. `sistemi.toml` in radice (TOML: sezioni come un INI, liste e tipi veri, letto con `tomllib` della libreria standard). Contiene `[progetto]` con `predefinito`, `attivi` e `rinforzo` (l'ordine in cui si cerca la versione più potente: oggi `dnd35`, poi `pf1e`), `[moduli]` con percorso → sistema, e `[ambientazioni]` (D4, sì) con `predefinito`, `elenco` (nome e skill di ogni mondo) e `moduli` percorso → ambientazione, letta da `sistemi.ambientazione_di()`.
2. Ogni plugin è `sistemi/<id>/sistema.toml` più i suoi file di dati. Il descrittore dichiara `id`, `nome`, `famiglia`, `licenza`, `fonti`, `skill` e la tabella `[capacita]`: nome della capacità → file di dati, oppure `{ eredita = "dnd35", motivo = "…" }`, oppure `"non supportato"`. **Nessuna eredità implicita**: una regola presa da un altro sistema è scritta, con il motivo.
3. `scripts/dmcore/sistemi.py` è l'unico caricatore: `sistema_di(percorso)`, `attivi()`, `dato(sistema, capacita)`. Sostituisce i tre rilevamenti di oggi; `e_pf1()` resta come involucro finché il cancello di ADR-0110 lo usa.
4. Ogni voce di `scripts/tools.manifest.json` che dipende dal sistema dichiara `sistema.capacita`. `scripts/sistemi.py` stampa la matrice strumenti × sistemi (cosa è supportato, cosa eredita, cosa manca) e con `--check` fa da cancello: un sistema attivo senza una capacità che uno strumento chiede è rosso; uno strumento chiamato su un modulo il cui sistema non ha la capacità esce con 2 e dice cosa manca, come fa `binari.py` con un binario assente.
5. Le skill di sistema (`dnd-35-srd`, `dnd-35-rules`, `pathfinder-1e-srd`) e di ambientazione (`forgotten-realms-lore`) sono elencate nei plugin; `build-skills.sh` e `sync-skills.sh` le installano secondo D5.
6. Si migra a lotti (L1-L8 del piano). Ogni lotto passa il **banco d'invarianza**: le 12 impronte di [impronte.py](../esperimenti/sistemi-plugin-2026-11-07/impronte.py) restano identiche byte per byte sui moduli 3.5. Le tabelle costanti nei file di fascia A hanno un tetto a cricchetto che scende a ogni lotto.

## Conseguenze

- Un sistema nuovo della famiglia d20 si aggiunge scrivendo `sistemi/<id>/` e una riga in `sistemi.toml`: l'obiettivo misurato è 0 file di codice toccati, contro 24 di oggi.
- Il DM vede in un posto solo quali sistemi ci sono, quali sono attivi e cosa ogni strumento sa fare con ciascuno.
- **Quello che non diventa gratis.** Un sistema fuori dalla famiglia d20 (5e, un OSR, un sistema a dadi diversi) non ha GS, CA e TS come li legge `dmcore/statblock.py`: chiede capacità nuove e un generatore suo. Il plugin rende visibile cosa manca, non lo scrive. Lo stesso vale per PF1e come sistema base dei generatori: oggi `genera_creatura` costruisce creature 3.5 con il rinforzo PF1e; costruire creature PF1e native (BMC/DMC, abilità fuse) è lavoro nuovo e in matrice risulterà `non supportato` finché qualcuno non lo fa.
- Il lotto delle creature (L5) è il più rischioso: i moduli `dmcore` hanno un grafo d'import vincolato (il verificatore non importa la scelta, `test_grafo_import_creature.py`) che il caricatore deve rispettare.
- Le tabelle dei termini restano del thread delle regole ufficiali (ADR-0110): il plugin le punta per percorso e non cambia il significato degli esiti di `controlla_testo()`.

**Da rivedere se**: un lotto non passa il banco d'invarianza e la differenza non si spiega con una correzione voluta dal DM; oppure, a L5 finito, aggiungere un sistema d20 di prova tocca ancora più di 2 file fuori da `sistemi/`; oppure il DM sceglie di portare un sistema fuori dalla famiglia d20, che riapre il punto 4.
