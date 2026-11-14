# Riferimento dei plugin di sistema

> Forma: **riferimento** (Diátaxis). Descrive com'è fatto un plugin e cosa
> controlla il cancello, verificato sul codice di main al 2026-11-10. I
> compiti (mettere un modulo in PF1e, aggiungere un sistema) sono nella
> [guida ai sistemi di gioco](../how-to/GUIDA-SISTEMI-DI-GIOCO.md); il perché in
> [ADR-0111](../../plans/adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md)
> e [ADR-0112](../../plans/adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md).
> Fonte di verità del comportamento: `scripts/dmcore/sistemi.py` e
> `scripts/dmcore/formule.py`. Se questo documento e il codice divergono, ha
> ragione il codice e va corretto il documento.

## 1 · File e cartelle

```text
sistemi.toml                      configurazione del progetto
sistemi/catalogo.toml             le capacità che un plugin può dichiarare
sistemi/<id>/sistema.toml         il descrittore del plugin
sistemi/<id>/dati/*.toml          i dati delle capacità in modo «dati»
sistemi/<id>/codice/*.py          funzioni registrate in [moduli]
scripts/dmcore/sistemi.py         il caricatore unico (solo stdlib, tomllib)
scripts/dmcore/formule.py         il valutatore delle formule
scripts/dmcore/_vendor/           simpleeval 1.0.8, con LIBRERIE.toml
scripts/sistemi.py                rapporto e cancello (dm.py sistemi)
```

Plugin presenti: `d20` (famiglia), `dnd35` e `pf1e` (sistemi). Un dato può
stare anche fuori da `sistemi/` (per esempio `scripts/lessico_it_pf1.tsv`):
conta il percorso dichiarato.

## 2 · `sistemi.toml`

| Chiave | Tipo | Significato |
|---|---|---|
| `[progetto] predefinito` | id | il sistema di un file fuori da `[moduli]`; deve stare fra gli `attivi` |
| `[progetto] attivi` | lista di id | i sistemi accesi; non vuota; ognuno con un plugin di `tipo = "sistema"` |
| `[progetto] rinforzo` | lista di id | dove si cerca la versione più potente di una regola, in ordine |
| `[moduli]` | percorso → id | il sistema di una cartella; vince il percorso più lungo; la cartella deve esistere e il sistema essere attivo |
| `[opzioni.<id>]` | chiave → valore | scelte di campagna che la fonte lascia al GM (PF1e: `traccia_pe`, `velocita_tesoro`), lette con `opzione(id, chiave)` |
| `[ambientazioni] predefinito` | nome | il mondo di un file fuori da `[ambientazioni.moduli]`; deve stare nell'elenco |
| `[ambientazioni.elenco]` | nome → `{ nome, skill }` | i mondi; ogni skill deve esistere in `skills/` |
| `[ambientazioni.moduli]` | percorso → nome | il mondo di una cartella |

## 3 · `sistema.toml`

| Campo | Obbligatorio | Significato |
|---|---|---|
| `id` | sì | uguale al nome della cartella |
| `nome` | sì | nome leggibile |
| `tipo` | sì | `"sistema"` (attivabile) o `"famiglia"` (solo da cui ereditare) |
| `licenza` | sì | licenza delle regole, per esempio `"OGL 1.0a"` |
| `fonti` | sì | lista di testi di riferimento; i dettagli in `dati/fonti.toml` |
| `skill` | sì | skill del sistema; devono esistere in `skills/`; si impacchettano se il sistema è attivo o di rinforzo, con quelle della famiglia |
| `capacita` | sì | tabella capacità → modo (§4) |
| `famiglia` | no | id di un plugin di `tipo = "famiglia"`; dove si cercano i `[moduli]` mancanti |
| `riconosci` | no | regex con cui la riga «**Sistema:**» di un modulo nomina il sistema |
| `[moduli]` | no | nome → `"modulo:funzione"` (§7) |

## 4 · I quattro modi di una capacità

```toml
[capacita]
"pe.soglie"        = { dati = ["sistemi/pf1e/dati/pe.toml"], nota = "tre tracce" }
"formule.regole"   = { eredita = "d20", motivo = "stesse formule in 3.5 e PF1e" }
"tesoro.per_livello" = { non_supportato = "il sistema non ha tesoro per livello" }
"lessico.entita"   = { codice = ["scripts/x.py:CLASSI"], lotto = "L3" }
```

| Modo | Campi | Regola del cancello |
|---|---|---|
| `dati` | `dati` (lista di percorsi), `nota` facoltativa | ogni file esiste; `dati(id, nome)` fonde i `.toml` nell'ordine, gli altri formati li legge lo strumento |
| `eredita` | `eredita` (id), `motivo` | il plugin esiste, il motivo c'è, la catena non è circolare |
| `codice` | `codice` (`file:NOME`), `lotto` | il file esiste, `NOME` vi è definito, il lotto che lo migra è scritto; oggi nessun plugin lo usa |
| `non_supportato` | `non_supportato` (motivo) | il motivo c'è; lo strumento rifiuta il modulo |

Una voce ha **un solo** modo. Una capacità che uno strumento chiede e che un
sistema attivo non dichiara è un errore: non c'è eredità implicita.
`capacita(id, nome)` segue l'eredità e restituisce una `Copertura` con `modo`
(`dati`, `codice`, `non_supportato`, `mancante`), `da` (il plugin che la
dichiara davvero), `catena` e `voci`.

## 5 · Il catalogo delle capacità

Una riga per ogni capacità di `sistemi/catalogo.toml`. «Chi la chiede» è il
campo `sistema.capacita` di `scripts/tools.manifest.json` (le parentesi sono
note); le colonne dnd35 e pf1e danno i `dati` di `sistema.toml` o il plugin da
cui la capacità è ereditata. `scripts/tests/test_riferimento_plugin.py` lo
controlla: una PR che cambia una capacità, chi la chiede o i suoi file
aggiorna anche questa tabella.

| Capacità | Cosa contiene | Chi la chiede | dnd35 | pf1e |
|---|---|---|---|---|
| `termini.vietati` | le meccaniche di altri sistemi che in un modulo non hanno posto (oggi le 5e) | validate_modules, validate_standalone | da d20: `termini-vietati.toml` | da d20: `termini-vietati.toml` |
| `lessico.abilita` | i nomi delle abilità del sistema, e quelli di altri sistemi da segnalare | domande_developer, validate_prosa | `abilita.toml` | `abilita.toml`, `lessico_it_pf1.tsv` |
| `lessico.entita` | classi e razze con cui si riconoscono i personaggi nel testo | coerenza_campagna | `entita.toml` | `lessico_it_pf1.tsv` |
| `lessico.italiano` | i nomi ufficiali italiani delle regole e il loro corrispondente SRD/PRD (ADR-0110) | lessico_regole | `lessico_it_35.tsv` | `lessico_it_pf1.tsv` |
| `fonti.regole` | il testo di riferimento in cache su cui si riscontrano le regole (ADR-0103) | lessico_regole, riscontro_srd, verifica_scheda | `fonti.toml` | `fonti.toml` |
| `pe.soglie` | i punti esperienza per passare di livello | update_xp | `pe.toml` | `pe.toml` |
| `tesoro.per_livello` | il tesoro per livello d'incontro o per GS | suggest_loot | `loot_tables.yaml`, `magic_items_srd.yaml` | `tesoro.toml` |
| `incontri.livello` | come si somma la sfida di più creature in un incontro | suggest_encounter | `incontri.toml` | `incontri.toml` |
| `creature.costruzione` | le tabelle per costruire una creatura: tipi, classi, DV, TS, BAB, taglie, armature, array; anche `[tratti_tipo]` (chi non ha Costituzione o Intelligenza) `[pf_bonus_costrutti]` (pf bonus dei costrutti per taglia) e `[gs]` (grado di sfida di chi è fatto di livelli di classe: scarto per classi da PG e da PNG, eccezioni di razza, parole che dichiarano un modello) e, nel 3.5, `[movimento]` (velocità a terra delle sette razze dell'SRD e di nove razze senza dadi vita razziali, categoria delle armature, velocità ridotta, movimento veloce di barbaro e monaco; ADR-0126, lotto 7) e `[difese]` (resistenza agli incantesimi delle razze con «N + livelli di classe» e del monaco, riduzione del danno del barbaro per livello, immunità che l'SRD dà ai tipi di creatura; ADR-0126, lotto 7) e `[linguaggi]` (linguaggi automatici delle sette razze dell'SRD, di nove razze senza dadi vita razziali fra cui hobgoblin, orco, drow e duergar, e Druidico del druido; ADR-0126, lotto 7) e `[oggetti]` (prezzi degli oggetti magici dell'SRD, prezzo base del bonus di potenziamento di armi e armature, capacità speciali di armi, armature e scudi, prezzi delle pergamene, costo in più di adamantio e mithral, prezzo di armi, armature e scudi comuni e della fattura perfetta, valore dell'equipaggiamento di un PNG per livello dalla Tabella 4-23 del DMG 3.5, nomi con cui una scheda scrive un oggetto; ADR-0126, lotto 8; in PF1e `[oggetti.png]`, la Tabella 14-9 del Core Rulebook col totale e le cinque categorie, e `[[codex]]`, i 454 PNG dell'NPC Codex e del Monster Codex con classe, livello e oggetti, ADR-0134) e `[mdl]` (modificatore di livello delle dieci razze che l'SRD presenta senza dadi vita razziali; ADR-0126, lotto 5) e, in PF1e, `[modelli]` (i sette modelli semplici del Bestiary: Avanzato, Gigante, Giovane, Celestiale, Immondo, Entropico, Risoluto, con la fonte per riga, le difese per dadi vita e i passi dei dadi di danno; lotto J del generatore, calcolo in `dmcore/modelli.py`) | conformita_statblocchi, derive_statblocks, genera_attributi, genera_creatura, impronta_creature, suggest_encounter, verifica_scheda | `creature.toml`, `classi_manuali.toml`, `talenti_in_piu.toml`, `gs.toml`, `movimento.toml`, `difese.toml`, `linguaggi.toml`, `oggetti.toml`, `mdl.toml` | `creature.toml`, `classi.toml`, `liste_incantesimi.toml`, `talenti_in_piu.toml`, `gs.toml`, `oggetti.toml`, `codex.toml`, `modelli.toml` |
| `creature.statistiche_per_gs` | i bersagli numerici per GS (pf, CA, attacco, CD) | derive_statblocks, genera_creatura, validate_bestiario | da pf1e: `pf1e-statistiche-per-gs.yaml` | `pf1e-statistiche-per-gs.yaml` |
| `creature.talenti` | i talenti con i prerequisiti, i talenti bonus delle classi e le capacità che i talenti chiedono; in PF1e anche `[requisiti."<classe di prestigio>"]` (BAB, talenti, gradi, incantesimi, capacità; `altro` = ciò che decide il DM) per 18 classi di prestigio; regola in `dmcore/talenti.py` | genera_creatura, verifica_scheda, verifica_talenti | `talenti.toml`, `talenti_manuali.toml` (manuali 3.5 fuori SRD, da PCGen), `talenti_equivalenti.toml` | `talenti.toml` |
| `creature.gradi` | i gradi delle abilità: caratteristica chiave, punti per livello di classe e per dado vita di tipo, massimo dei gradi (ADR-0124); nel 3.5 anche le abilità di classe e di dominio, le sinergie e i bonus di razza e di taglia alle abilità delle sette razze dell'SRD e di nove razze senza dadi vita razziali, la penalità di armatura alla prova e il modificatore della velocità a Saltare (ADR-0126, lotto 6); in `effetti_talenti.toml` i talenti che alzano il bonus di un'abilità (ADR-0126, lotto 4) | verifica_scheda | `gradi.toml`, `classi_manuali.toml`, `effetti_talenti.toml` | `gradi.toml`, `classi.toml`, `effetti_talenti.toml` |
| `creature.liste_incantesimi` | le liste di classe e di dominio degli incantesimi per livello: chi può lanciare che cosa (ADR-0124 §10) | verifica_scheda | `liste_incantesimi.toml` (SRD), `liste_incantesimi_manuali.toml` (manuali 3.5, solo nomi e livelli) | `liste_incantesimi.toml` |
| `bonus.cumulo` | il cumulo dei bonus per tipo e le sorgenti (oggetti, talenti, razze) che una scheda può dichiarare su TS e attacco (ADR-0126) | verifica_scheda (tramite `dmcore.bonus`) | da d20: `bonus.toml` | da d20: `bonus.toml` |
| `creature.armi` | le armi: dado per taglia Media, critico, impugnatura, il dado al cambiare della taglia (ADR-0126, lotto 2) | verifica_scheda | `armi.toml` (SRD) | da dnd35: `armi.toml` (72 armi del manuale base uguali all'SRD) |
| `creature.incantatori` | gli incantesimi al giorno e conosciuti per livello di classe, la caratteristica che li governa (ADR-0126, lotto 3) | verifica_scheda | `incantatori.toml` (SRD) | `incantatori.toml` (PRD) |
| `creature.prestigio` | i requisiti delle classi di prestigio: BAB, gradi, talenti, razza, allineamento, livello d'incantesimo; solo nomi e numeri (ADR-0126, lotto 3-bis) | verifica_scheda | `prestigio.toml` (SRD e manuali, da PCGen) | `prestigio.toml` (PRD, 10 classi del Core) |
| `creature.base` | le creature base: taglia, tipo, dadi vita razziali, armatura naturale, caratteristiche, attacchi naturali col dado, modificatore di livello, `avanza = "classe"` per chi avanza per classe (SRD 3.5, 52 creature; ADR-0134); per i draghi veri il dado per taglia (ADR-0126, lotto 5) | verifica_scheda | `creature_base.toml` (SRD, 409 creature e draghi per taglia) | `creature_base.toml` (PRD, Bestiary 1-4, 1138 creature) |
| `creature.incantesimi` | le liste di incantesimi per classe | genera_creatura | `incantesimi.toml` | `incantesimi.toml` del 3.5 e del PF1e |
| `creature.regole_di_tipo` | le regole di tipo che cambiano i conti (es. il non morto PF1e usa il Carisma) | conformita_statblocchi, verifica_scheda | `creature.toml` | `creature.toml` |
| `creature.conformita` | i conti che il controllo delle schede sa fare nel sistema, e come si arrotondano i pf | conformita_statblocchi, verifica_scheda | `conformita.toml` | `conformita.toml`, `conformita_prd.toml` |
| `statblocco.campi` | i campi meccanici del blocco statistiche | build_monster_catalog, conformita_statblocchi, extract_statblocks, genera_creatura, validate_bestiario, verifica_scheda | da d20: `statblocco.toml` | da d20: `statblocco.toml` |
| `statblocco.taglie` | spazio e portata per taglia (tabella SRD, ADR-0128) | — (la legge `dmcore.statblock`, nessuno strumento la dichiara nel manifest) | da d20: `taglie.toml` | da d20: `taglie.toml` |
| `formule.regole` | le formule del sistema scritte come nel manuale, valutate da `dmcore.formule` | genera_creatura, verifica_scheda (le usa anche il nucleo) | da d20: `formule.toml` | da d20: `formule.toml` |
| `stampa.etichette` | le sigle meccaniche stampate nel riquadro della creatura | build_booklet_html, export_booklet_typst | da d20: `stampa.toml` | da d20: `stampa.toml` |

Per rifare la tabella: `python3 scripts/dm.py sistemi --json`.

Il formato interno di ogni file di dati è quello dei file esistenti, con la
fonte in testa (`fonte = "…"`). **Non c'è ancora uno schema per capacità**:
ADR-0112 §3 lo prevede (JSON Schema accanto ai dati, fastjsonschema nella
skill), ma su main il cancello controlla la struttura del plugin, non i
campi dentro i file di dati. Un campo scritto male si scopre dallo strumento
che lo legge o dai suoi test.

## 6 · Le formule

Capacità `formule.regole`, oggi in `sistemi/d20/dati/formule.toml`:

```toml
[formule.ts_buono]
espressione = "2 + dv // 2"
ingressi = ["dv"]
fonte = "SRD 3.5, «Creature Improvement by Type»"
```

| Regola | Valore |
|---|---|
| Nodi ammessi | espressione, costante, nome, operazione binaria e unaria, confronto, `if … else`, chiamata |
| Operatori | `+ - * // %`, segno, `> >= < <= == !=` |
| Funzioni | solo `max` e `min`, senza argomenti con nome |
| Costanti | solo intere |
| Nomi | solo quelli in `ingressi` |
| Risultato | intero, altrimenti errore |
| Uso | `formula("ts_buono", "pf1e")(dv=6)` → 5 (pf1e eredita da d20) |

Attributi, indici, potenze, stringhe e assegnazioni sono rifiutati. Il
cancello (`formule.problemi()`, dentro `sistemi.py --check`) controlla ogni
formula di ogni plugin senza valutarla; `test_formule.py` confronta le sei
formule con le funzioni Python che hanno sostituito, su tutto il dominio, e
ricontrolla lo sha256 di simpleeval.

## 7 · I moduli di codice

```toml
[moduli]
somma_px = "incontri:somma_px"     # sistemi/pf1e/codice/incontri.py, funzione somma_px
```

| Regola | Valore |
|---|---|
| Riferimento | `"modulo:funzione"`, nomi `[a-z_][a-z0-9_]*`, la funzione non comincia con `__` |
| Dove | solo `sistemi/<id>/codice/<modulo>.py`; `..`, percorsi assoluti, moduli della libreria standard e symlink verso fuori sono rifiutati prima di eseguire |
| Nome del modulo caricato | `rs_plugin.<id>.<modulo>`: due plugin con lo stesso file non si scambiano il codice |
| Ricerca | `modulo(id, nome)` cerca in `[moduli]` del plugin, poi della sua famiglia |
| Cosa deve essere | una funzione definita in quel file (non importata) |
| Sicurezza | il file viene **eseguito**: è codice Python rivisto in PR come il nucleo, non una sandbox |

Contratto delle funzioni di oggi, per `incontri.livello`: il campo `metodo`
del file di dati nomina la funzione; `suggest_encounter` la chiama con il
dizionario dei dati della capacità e riceve un combinatore
`lista di GS → EL`. Esempi: `potenze` in `sistemi/d20/codice/incontri.py`,
`somma_px` in `sistemi/pf1e/codice/incontri.py`, `piu_forte` nel plugin
finto `scripts/tests/dati/prova-d20-due/`.

## 8 · L'interfaccia di `dmcore.sistemi`

| Funzione | Restituisce |
|---|---|
| `sistema_di(percorso)` | l'id del sistema del file (§2, `[moduli]`) |
| `ambientazione_di(percorso)` | il mondo del file |
| `attivi()`, `predefinito()`, `progetto()` | la configurazione |
| `plugin(id)` | il descrittore letto, o errore se l'id non esiste |
| `capacita(id, nome)` | la `Copertura` dopo l'eredità |
| `dati(id, nome)` | i dati TOML fusi; errore se il modo non è `dati` |
| `regole(id)`, `regole_di(percorso)` | il contesto esplicito, con `.dati(nome)` e `.capacita(nome)` |
| `regole_diverse(id, strumento, scritto_per="dnd35")` | le capacità di uno strumento che `id` legge da dati diversi; vuoto = lo strumento può lavorare |
| `modulo(id, nome)`, `moduli(id)` | una funzione registrata; i nomi visibili |
| `opzione(id, chiave, default)` | una scelta di `[opzioni.<id>]` |
| `sistema_dichiarato(testo)` | il sistema che la riga «**Sistema:**» di un testo nomina |
| `skill_da_installare()`, `skill_escluse()` | le skill da impacchettare e da saltare |
| `problemi(root, strumenti)` | i difetti della configurazione; vuoto = verde |

Errori: `ErroreSistemi` (configurazione o plugin illeggibile) e
`dmcore.formule.ErroreFormula`. Tutto è in cache per radice del repo: stesso
albero, stesso risultato, nessuna rete, nessuna scrittura.

## 9 · Cancelli e prove

| Controllo | Comando | In CI |
|---|---|---|
| Struttura, eredità, file, formule, moduli, riga «Sistema» | `python3 scripts/dm.py sistemi --check` | bloccante |
| Le formule danno i numeri di prima | `scripts/tests/test_formule.py` | suite |
| Un plugin d20 finto entra senza toccare il nucleo | `scripts/tests/test_prova_del_nove_2.py`, `test_sistemi_prova_del_nove.py` | suite |
| Un plugin non d20 finto: chi lo lavora e chi lo rifiuta | `scripts/tests/test_prova_non_d20.py` | suite |
| `verifica_scheda` dichiara nel manifest ogni capacità che legge | `scripts/tests/test_capacita_verifica_scheda.py` | suite |
| Il §5 di questo file dice quello che dicono catalogo, manifest e plugin | `scripts/tests/test_riferimento_plugin.py` | suite |
| Le schede PF1e tornano con le regole PF1e | `python3 scripts/conformita_statblocchi.py --cancello-moduli` | bloccante sui conti fatti |
| Le tabelle dei plugin contro SRD e PRD | `plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py` | no, in prova (ADR-0121) |

## 10 · Limiti noti

- Nessuno schema per i file di dati (§5).
- L'ambito è la famiglia d20; un sistema non d20 è solo una prova nei test.
- Il codice dei plugin è eseguito, non isolato (§7).
- La capacità `codice` esiste nel catalogo ma nessun plugin la usa più dopo
  L8; resta per un sistema nuovo da migrare a lotti.
