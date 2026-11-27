# PIANO — I sistemi di gioco come plugin attivabili

> **Stato**: ✅ chiuso (2026-11-08), L0-L8 fatti, D1-D5 decise, ADR-0111 accettata; continua in [PIANO-MOTORE-AGNOSTICO-D20](PIANO-MOTORE-AGNOSTICO-D20.md) · **Classe**: G per la regola, C per i lotti
> **Nasce da**: il messaggio del DM del 2026-11-07 (citato in [ADR-0111](adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md)): plugin per tutto il giro di strumenti, skill e agent, un set di regole diverso senza rifare tutto, in modo misurabile e deterministico, con un file di configurazione generale che attiva e disattiva i sistemi e mostra quelli supportati.
> **Decisione**: [ADR-0111](adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md), accettata il 2026-11-08 con D1-D5 decise (D4: `[ambientazioni]` in `sistemi.toml`).
> **Dipende da**: ADR-0110 (termini ufficiali, ramo `regole-ufficiali`): `lessico_it.yaml`, `lessico_it_pf1.tsv`, `lessico_regole.py` sono il primo contenuto dei plugin, e restano loro.
> **Misure**: [plans/esperimenti/sistemi-plugin-2026-11-07/](esperimenti/sistemi-plugin-2026-11-07/) (`censimento.py`, `CENSIMENTO.json`, `impronte.py`, `IMPRONTE.json`).
>
> **In breve**: su 202 script, 31 dipendono dal sistema di gioco e 171 no. Il sistema di un modulo si decide in tre modi diversi, la lista dei termini 5e vietati ha due copie, e un sistema d20 nuovo oggi tocca 24 file. Il piano porta tutto a un file `sistemi.toml` e a plugin di dati in `sistemi/<id>/`, un lotto alla volta, con un banco che verifica che le uscite sui moduli 3.5 non cambino di un byte.

---

## §1 · Audit: lo stato di oggi

### §1.1 Gli script (censimento deterministico)

`python3 plans/esperimenti/sistemi-plugin-2026-11-07/censimento.py` conta nove famiglie di termini in ogni script e confronta il risultato con una classificazione scritta a mano, riga per riga, con il motivo. Con `--check` esce 1 se un file con punteggio ≥ 10 non è classificato. La conta da sola è rumorosa («GS» in `render_schemi.py` è il Giardino di Sale), per questo decide la classificazione e non il punteggio.

| Fascia | Cosa vuol dire | File | Esempi |
|---|---|---|---|
| A | regole cablate nel codice | 17 | `dmcore/tabelle.py` (TIPI, CLASSI, BAB, TAGLIE, ARMATURE), `dmcore/progressione.py` (DV, TS, BAB), `dmcore/caratteristiche.py`, `dmcore/incantesimi.py`, `dmcore/lettura_creatura.py` (`NON_MORTO_PF1E`), `update_xp.py` (soglie PE 3.5), `suggest_loot.py` (DMG 3.5 Tab. 3-5), `suggest_encounter.py`, `validate_bestiario.py`, i generatori |
| B | liste di termini per sistema | 5 | `validate_modules.py` e `validate_standalone.py` (5e vietati, due copie), `validate_prosa.py` (abilità 3.5), `coerenza_campagna.py` (classi e razze), `riscontro_srd.py` (fonti) |
| C | decide il sistema di un modulo | 2 | `domande_developer.py` (profilo + `ABILITA_ESTRANEE`), `dmcore/censimento.py` (Drappo per percorso) |
| D | etichette d20 in stampa | 7 | `build_booklet_html.py`, `export_booklet_typst.py`, `dmcore/schede.py`: oggi uguali in 3.5 e PF1e, tranne BMC/DMC sulla scheda del PG PF1e |
| N | neutro | 171 | mappe, stampa, prosa, piattaforma |

Le quattro misure di partenza (da `CENSIMENTO.json`):

| Misura | Oggi | Obiettivo |
|---|---|---|
| M1 · modi di decidere il sistema di un modulo | 3 (percorso, riga «**Sistema:**» in 26 master con 10 grafie, `sistema` in 3 profili) | 1 (`sistemi.toml`) |
| M2 · copie della lista dei termini 5e | 2 | 1 |
| M3 · costanti maiuscole a livello di modulo nei file A (tabelle e regex insieme) | 76 | tetto a cricchetto, scende a ogni lotto; le regex restano |
| M4 · file di codice da toccare per un sistema d20 nuovo | 24 | 0 (solo `sistemi/<id>/` e una riga in `sistemi.toml`) |

### §1.2 Skill e agent

| Skill | Asse | Nota |
|---|---|---|
| `dnd-35-srd`, `dnd-35-rules` | sistema `dnd35` | |
| `pathfinder-1e-srd` | sistema `pf1e` | serve anche ai moduli 3.5, come rinforzo: non si può spegnere quando PF1e non è il sistema base |
| `npc-villain-boosting` | rinforzo 3.5 + PF1e | usa i template PF1e sui PNG 3.5 |
| `forgotten-realms-lore` | ambientazione | Golarion non ha una skill sua: sta dentro `pathfinder-1e-srd` |
| le altre 13 `rumblingstone-*` | neutre | `module-standard` scrive la riga «Sistema: D&D 3.5 SRD (max PF1e), MAI 5e» come norma |

`build-skills.sh` e `sync-skills.sh` (matrice in `scripts/agents.conf`) installano tutte le 18 skill per sette agenti, senza sapere quale sistema è in uso.

### §1.3 Cosa il piano non rifà

- Le tabelle dei termini e il cancello sui nomi (ADR-0110): il plugin le punta per percorso.
- Le fonti in cache (ADR-0103, `riscontro_srd.py`): il plugin dichiara quale fonte è sua.
- Il manifest dei tool (ADR-0012): si aggiunge un campo, non un secondo registro.

## §2 · Sviluppo: i lotti

Ogni lotto è una PR. Ogni PR lancia `impronte.py --confronta` prima e dopo: le 12 impronte restano identiche, o la differenza è una correzione che il DM ha visto.

| Lotto | Cosa | File toccati | Misura |
|---|---|---|---|
| **L0** ✅ | censimento, banco d'invarianza, ADR-0111 proposta, questo piano | `plans/` | M1-M4 di partenza |
| **L1** ✅ | fondazione: `sistemi.toml`, `sistemi/catalogo.toml` (12 capacità), plugin `sistemi/d20/` (famiglia), `sistemi/dnd35/`, `sistemi/pf1e/`; `scripts/dmcore/sistemi.py` (caricatore), `scripts/sistemi.py` (elenco, matrice, `--di`, `--skill`, `--json`, `--check`, in CI); campo `sistema.capacita` nello schema e in 16 voci del manifest; `test_sistemi.py` | nessuno strumento esistente cambia comportamento | impronte 12/12; matrice di 24 righe; dnd35 2 capacità in dati e 10 nel codice, pf1e 1 · 6 · 5 non supportate; 0 mancanti |
| **L1-bis** ✅ | PF1e supportato nei 5 casi che L1 dichiarava «non supportato» (richiesta del DM del 2026-11-07): `estrai_prd_pf1e.py` scrive `sistemi/pf1e/dati/{pe,incontri,tesoro,creature}.toml` dal PRD in cache, con la fonte; `sistemi.toml` `[opzioni.pf1e]` (traccia PE, velocità del tesoro); `--sistema` in `update_xp`, `suggest_encounter`, `suggest_loot`, `genera_creatura`; classi, classi di prestigio e razze PF1e in `coerenza_campagna` per i file dei moduli PF1e; `dmcore/creature_pf1e.py`; `test_sistemi_pf1e.py` | il predefinito resta dnd35: uscita 3.5 identica | impronte 12/12; pf1e da 2 · 6 · 5 a 7 · 6 · 0 (dati · codice · non supportato) |
| **L2** ✅ | un rilevamento solo: `build_monster_catalog` e `dmcore/censimento` escludono i moduli non 3.5 con `sistema_di()` invece che per nome; `domande_developer` prende il sistema da `sistemi.toml` e rifiuta «sistema» nei profili (tolto da 3 profili del Drappo); la riga «**Sistema:**» dei moduli è controllata contro `sistemi.toml` da `sistemi.py --check` (campo `riconosci` nei plugin); `e_pf1()` involucro di `sistema_di()`, con l'ok del thread delle regole (dopo la #319) | 5 + test | M1 misurato 5 → 1; il Giardino PF1e esce dal catalogo dei mostri (proposto in 7 incontri su 120 a EL 17-18, ora 0) e dal censimento del Bestiario |
| **L3** ✅ | termini: una lista 5e sola (`sistemi/d20/dati/termini-vietati.toml`, letta da `validate_modules` e `validate_standalone`), abilità per sistema (`lessico.abilita` di dnd35 e pf1e, letta da `validate_prosa` e `domande_developer`), classi e razze 3.5 di `coerenza_campagna` in `sistemi/dnd35/dati/entita.toml` | 5 + test | M2 2 → 1; 0 rilievi nuovi su master e stand-alone; nei moduli PF1e le forme meccaniche riconosciute da `validate_prosa` passano da 64 a 93 |
| **L4** ✅ | regole semplici: soglie PE 3.5 in `sistemi/dnd35/dati/pe.toml` (`update_xp` legge ogni sistema dal plugin, `THRESHOLDS` caricato dai dati); EL con il `metodo` del plugin (`potenze` con `raddoppio = 2` per il 3.5, `somma_px` per PF1e; `suggest_encounter.combinatore()`); `suggest_loot` sceglie dal predefinito di `sistemi.toml`. Il PF1e supportato l'aveva già fatto L1-bis | 3 + test | capacità dnd35 nel codice 7 → 5; nomi di sistema cablati nei tre strumenti 7 → 0; uscite 3.5 e PF1e identiche; M3 resta 79 |
| L5 ✅ (L5a, L5b, L5c, L5d) | nucleo delle creature: `dmcore/tabelle`, `progressione`, `caratteristiche`, `incantesimi`, `lettura_creatura` leggono le tabelle dal plugin; il grafo d'import resta quello di `test_grafo_import_creature.py` — **L5a** (2026-11-07): tipi, classi (con BAB e classi PNG), taglie, armature, scudi e matrici elite/standard in `sistemi/dnd35/dati/creature.toml`, letti da `dmcore/tabelle.py` con gli stessi nomi; **L5b** (2026-11-07): griglie degli incantatori e incantesimi conosciuti, classi incantatrici, classi di prestigio, profili di ruolo, modificatori per taglia e razziali; **L5c** (2026-11-07): liste degli incantesimi 3.5 nel plugin dnd35, aggiunte APG nel plugin pf1e | 5 + 7 consumatori | M3 al minimo; impronte dei generatori identiche |
| L6 ✅ | skill e agent: `build-skills.sh`/`sync-skills.sh` chiedono a `sistemi.py --skill` quali skill installare (D5); `AGENTS.md` e `skills/ORCHESTRAZIONE.md` lo dicono | 4 | numero di skill installate per configurazione |
| L7 ✅ | etichette di stampa dal plugin (serve solo per BMC/DMC sulla scheda PF1e o per un sistema non d20) | 3 | stampa identica sui booklet 3.5 |
| L8 ✅ | prova del nove: un sistema d20 finto nei dati dei test (`prova-d20`) si aggiunge senza toccare codice | 0 | M4 = 0 |

### §2.1 Il file generale (L1, con le consigliate di D1, D2 e D4; i file veri sono `sistemi.toml` e `sistemi/*/sistema.toml`)

```toml
# sistemi.toml — i sistemi di gioco del progetto (ADR-0111)

[progetto]
predefinito = "dnd35"
attivi = ["dnd35", "pf1e"]
# dove si cerca la versione più potente di una regola, in ordine
# (preferenza del DM del 2026-10-18)
rinforzo = ["dnd35", "pf1e"]

[moduli]
# percorso dalla radice = sistema; vince il più specifico
"10-stand-alone/Il-Drappo-di-Tarsilia" = "pf1e"
"10-stand-alone/Il Giardino di Sale e Calce PF1e" = "pf1e"

[ambientazioni]          # solo se D4 = sì
attive = ["forgotten-realms", "golarion"]
"10-stand-alone/Il-Drappo-di-Tarsilia" = "golarion"
```

E il descrittore di un plugin:

```toml
# sistemi/pf1e/sistema.toml
id = "pf1e"
nome = "Pathfinder 1ª edizione"
famiglia = "d20"
licenza = "OGL 1.0a"
fonti = ["PRD PSRD-Data@76ea4784"]
skill = ["pathfinder-1e-srd"]

[capacita]
"lessico.italiano" = "../../scripts/lessico_it_pf1.tsv"     # ADR-0110
"creature.statistiche_per_gs" = "../../scripts/pf1e-statistiche-per-gs.yaml"
"termini.vietati" = { eredita = "d20", motivo = "le meccaniche 5e sono vietate in tutta la famiglia" }
"pe.soglie" = "dati/pe.toml"
"creature.costruzione" = "non supportato"   # oggi si costruisce in 3.5 con il rinforzo PF1e
```

`python3 scripts/sistemi.py` stamperà la matrice:

```
strumento            capacità                  dnd35   pf1e
update_xp            pe.soglie                 ✅      ✅
suggest_loot         tesoro.per_gs             ✅      ⬜ non supportato
genera_creatura      creature.costruzione      ✅      ⬜ non supportato
validate_modules     termini.vietati           ✅      ↪ eredita d20
```

### §2.2 Cosa ha trovato L1

- Il banco d'invarianza aveva un difetto suo: `update_xp --check` stampa l'ora, e l'impronta cambiava a ogni minuto. Adesso `impronte.py` sostituisce la riga dell'orologio; la base è stata riscritta da `main` (99337894, poi 9fc7f515 dopo #314 e #316), e 12 impronte su 12 tornano.
- `build_monster_catalog.py` esclude dal catalogo il Drappo ma non il Giardino PF1e: oggi `scripts/monster_catalog.yaml` contiene una voce PF1e (l'appendice delle creature del Giardino, GS 16, ruolo boss) che `suggest_encounter` può proporre in un incontro 3.5. Con un rilevamento solo (L2) il buco si chiude. È il primo caso misurato di tre rilevamenti che divergono.

- Con ADR-0110 su main (#316) è arrivato `scripts/lessico_regole.py`, che decide il sistema con `e_pf1()`: i rilevamenti in fascia C salgono a 3 e M4 a 25. Le sue tabelle (`lessico_it_35.tsv`, `lessico_it_pf1.tsv`) entrano nei plugin come capacità `lessico.italiano` in dati, senza toccarle.

### §2.3 Cosa ha trovato L1-bis (PF1e nei 5 casi)

- **Numeri**: nessuno scritto a mano. Sei tabelle del PRD (book-cr 2743, 3653, 3655, 3661; book-b1 116, 160) diventano quattro file TOML; `estrai_prd_pf1e.py --check` rifà l'estrazione e confronta i byte (in `test_sistemi_pf1e.py`, saltato dove il PRD non è in cache).
- **Incontri**: in PF1e il GS dell'incontro è la somma dei PE, poi il GS più alto che la somma raggiunge. Coincide col 3.5 sui casi pari (due GS 10 → 12, quattro → 14) e diverge sui dispari (tre GS 10: 13 in PF1e, 13,17 in 3.5; due GS ½: 1 contro 2,5). Le creature proposte vengono ancora dal catalogo comune, che contiene mostri 3.5: separarlo è L2.
- **Tesoro**: il PRD dà il valore per incontro per APL e velocità, non la ripartizione. Monete, gemme e oggetti restano nelle proporzioni della riga 3.5 dello stesso livello, e la nota in fondo lo dice. Il PRD lo tara su 4 PG; con `--pcs` diverso lo strumento divide la stessa somma.
- **Creature**: la conversione parte dal blocco 3.5 già sul bersaglio del GS e risolve di nuovo la caratteristica dei pf sul dado PF1e (Carisma per i non morti). Senza questo un non morto GS 7 passava da 105 a 35 pf. Dove il BAB PF1e del tipo è più alto (costrutto, non morto) l'attacco sale sopra il bersaglio: è la regola del tipo, e il conto lo dice. Gigante ed elementale diventano umanoide ed esterno. Mancano: i pf bonus dei costrutti per taglia (la tabella non c'è nel PRD in cache, il conto lo segnala) e i livelli di classe (rifiutati con un messaggio).
- **Classi e razze**: 3.5 invariato; nei file dei moduli PF1e `coerenza_campagna` riconosce anche l'ultima parola di ogni classe e classe di prestigio PF1e (174 parole contro 67). Le razze PF1e sono arrivate con la PR #318 del thread delle regole ufficiali (37 righe `razza`, lette con `lessico_regole.tabella_pf1`): 49 parole contro le 23 del 3.5. `RAZZE` oggi non la legge nessun controllo di `coerenza_campagna`.
- **Limite della matrice, ancora vero**: una riga ✅ dice che il sistema ha il dato, non che ogni strumento della riga lo legga. Per `creature.costruzione` lo legge solo `genera_creatura`; `derive_statblocks`, `conformita_statblocchi`, `genera_attributi` e `suggest_encounter` lavorano ancora in 3.5 (L5).

### §2.4 Cosa ha trovato L2

- **M1 misurato**: `censimento.py` ora conta i rilevamenti invece di dichiararli. Su main prima di L2 erano 5: `sistemi.toml`, tre script che decidevano da soli (`build_monster_catalog` e `dmcore/censimento` per nome del Drappo, `lessico_regole.e_pf1`), i profili di `domande-developer.json` con «sistema». Dopo L2 sono 2, e resta `e_pf1`.
- **Il buco del Giardino PF1e**, chiuso: con il catalogo di prima l'appendice PF1e (GS 16) usciva in 3 incontri su 60 a EL 17 e in 4 su 60 a EL 18 (semi 1-60); con quello nuovo 0 e 0. Il catalogo passa da 387 a 386 voci, e l'impronta di `suggest_encounter` cambia solo nella riga del conteggio: è l'unica impronta riscritta.
- **`e_pf1()` sbagliava il Drappo**: diceva PF1e solo per 3 file su 22 (quelli con la riga «Sistema» o «PF1E» nel nome), e gli altri 19 erano controllati con le tabelle 3.5. Ora chiede prima a `sistema_di()` (con il ripiego di prima se `dmcore.sistemi` non si importa, come chiesto dal thread delle regole): 22 su 22, M1 a 1. Misura del cancello dei termini, prima → dopo: su main talenti sconosciuti 133 → 131 e «nome 3.5» 0 → 0 (il cancello bloccante non cambia); sopra la #319 97 → 95. Le due voci risolte sono «Incanalare Selettivo» nei booklet del Drappo. Nei campi (conto non bloccante) le abilità passano da tabella 190 · nome 3.5 1 · sconosciute 28 a 194 · 3 · 22: i due «nome 3.5» nuovi sono «Percepire Intenzioni» (3.5) dove PF1e dice «Intuizione», nei due booklet del Drappo. Il Drappo usa «Percepire Intenzioni» in una trentina di punti per scelta dichiarata («chiamate all'italiana come al tavolo»): rinominarle è una decisione del DM, non di questo lotto.
- **La riga «Sistema»**: 18 moduli la scrivono (archivio escluso), 0 divergono da `sistemi.toml`. «D&D 3.5 (max PF1e)» è 3.5: vince il nome che compare per primo.

### §2.5 Cosa ha trovato L3

- **Le due copie della lista 5e non erano la stessa lista**: `validate_modules` non vedeva «azione bonus», «azione del covo», «con vantaggio» né «con svantaggio»; `validate_standalone` non vedeva «bonus action» né «lair action». La lista unica è l'unione delle due, nel plugin della famiglia d20 (3.5 e PF1e la ereditano). Sui master e sugli stand-alone l'unione trova 0 rilievi nuovi: le uscite dei due validatori sono identiche prima e dopo. Il buco era vero ma oggi vuoto; da adesso un «con vantaggio» in un modulo 3.5 viene bocciato da tutti e due.
- **Le tre voci del canone deprecato** (Nymeria, Skulldark, il cane da guerra costrutto) restano in `validate_modules`: sono canone della campagna, non regole di un sistema.
- **Abilità PF1e nei moduli PF1e**: `validate_prosa --caratteristiche` cercava nei moduli PF1e le abilità 3.5 (31 nomi). Ora prende quelle del sistema del file: le 26 PF1e dal TSV delle regole, più le 3.5 per i nomi comuni. Nei moduli PF1e le forme meccaniche riconosciute passano da 64 a 93 (sono le abilità PF1e come «Percezione +12»); 0 abilità minuscole nuove, il controllo resta verde su 587 file.
- **Non è cambiato**: `domande_developer` 55 rilievi come prima, `coerenza_campagna fatti --check` verde, impronte 12/12. M3 resta 79: conta le tabelle dei file di fascia A, e L3 tocca file di fascia B. M4 resta 27: i file da toccare per un sistema nuovo scendono solo con L4-L5.

### §2.6 Cosa ha trovato L4

- **La misura che si muove**: le capacità dnd35 ancora nel codice passano da 7 a 5 (`pe.soglie` e `incontri.livello` diventano dati); nei tre strumenti i confronti con il nome `"dnd35"` passano da 7 a 0, così un sistema predefinito diverso in `sistemi.toml` cambia le loro uscite senza toccarli.
- **Le uscite non cambiano**: impronte 12/12 sul 3.5; con `--sistema pf1e` le uscite di `update_xp` (tracce media e veloce), `suggest_encounter --seed 42` e `suggest_loot --el 10` hanno lo stesso md5 prima e dopo.
- **M3 non scende, e il perché**: `THRESHOLDS` non è più una tabella nel codice, ma `suggest_encounter` ha guadagnato `METODI` (i due modi di combinare i GS). Il censimento conta tutte e due come «tabelle costanti»: METODI è un elenco di funzioni, non di numeri di regole, ma non lo distinguo con un'eccezione fatta apposta. Il numero onesto è 79 → 79.
- **Cosa resta codice, per scelta**: le due formule (EL = r·log2 Σ 2^(GS/r) e la somma dei PE PF1e). Il plugin sceglie il metodo e il parametro; un sistema nuovo con un modo di combinare diverso aggiunge una riga a `METODI`. Le fonti scaricate di `riscontro_srd.FONTI` (URL e sha256 fissati) passano al lotto L8: si spostano solo se la prova del nove ne ha bisogno.
- **Fonte dei numeri 3.5**: la tabella dei PE e la regola dell'EL non sono nell'SRD in cache (sono PHB Tab. 3-2 e DMG p. 49). Sono spostati senza cambiare un numero, e un test lo controlla.

### §2.7 Cosa ha trovato L5a

- **Le tabelle base delle creature 3.5 sono dati**: tipi, classi, BAB per classe, classi PNG, taglie, armature, scudi e matrici stanno in `sistemi/dnd35/dati/creature.toml`, e `dmcore/tabelle.py` le carica una volta con i nomi di sempre, così i 7 consumatori non cambiano. `creature.costruzione` del 3.5 passa da codice a dati: le capacità dnd35 nel codice scendono da 5 a 4.
- **Prova che nessun numero si è mosso**: `test_sistemi_creature.py` confronta l'impronta di ogni tabella con quella delle costanti di main b0a74ae; impronte dei generatori 12/12; talenti sconosciuti 0 (cancello `--massimo-sconosciuti 0`). L'ordine di `BAB_CLASSE` ora segue quello di `CLASSI`: nessuno lo scorre, si legge solo per chiave.
- **M3 79 → 76**, ma conta male: le tabelle diventate comprensioni sopra i dati (`TIPI = {k: … for …}`) il censimento le conta ancora come tabelle costanti. Il numero vero di tabelle con numeri di regole scritte nel codice scende di 9 (le 9 costanti spostate).
- **Cosa resta per L5b**: `INCANTATORI` e `CONOSCIUTI` di tabelle.py, `progressione.PRESTIGIO`, `caratteristiche.PROFILI`/`RAZZE`, `incantesimi.LISTE`. La lettura del DM di un booklet 3.5 rigenerato si fa a L5b, dove possono cambiare le uscite; L5a ha valori identici per test.

### §2.8 Cosa ha trovato L5b

- **Spostate 19 costanti senza cambiare un valore**: le 8 griglie degli incantatori (mago, stregone e i suoi conosciuti, chierico = druido, adepto, bardo e i suoi conosciuti, ranger = paladino), `INCANTATORI`, `LIVELLO_INCANTATORE_RIDOTTO`, `INCANTATORI_SENZA_ANCORA` di `tabelle.py`; `PRESTIGIO` di `progressione.py`; `PROFILI`, `PROFILO_DI_RIPIEGO`, `PER_TAGLIA`, `RAZZE` di `caratteristiche.py`. Stanno in `creature.toml` sotto `[griglie]`, `[incantatori]`, `[incantatori_regole]`, `[prestigio]`, `[profili]`, `[per_taglia]`, `[[razze]]`. Le tabelle in cui l'ordine conta (profili, razze) sono array di tabelle TOML, quindi l'ordine resta quello del file.
- **Prova**: `test_sistemi_creature.py` confronta l'impronta di ognuna con quella di main c258a3e; gli alias (druido = chierico, paladino = ranger) restano lo stesso oggetto; impronte dei generatori 12/12; `sistemi.py --check` verde.
- **Trovato strada facendo**: `progressione.NOMI_DI_CLASSE` è ordinato per lunghezza partendo da un `set`, quindi a parità di lunghezza l'ordine cambia a ogni esecuzione (PYTHONHASHSEED) già su main. Non è un difetto visibile: due nomi della stessa lunghezza non possono essere uno il prefisso dell'altro, quindi la regex trova le stesse cose. Il test confronta l'insieme, non l'ordine.
- **M3 76 → 73** (stesso limite di L5a: le comprensioni sopra i dati contano ancora).
- **Lettura del DM**: le uscite dei generatori sono identiche per impronta, quindi un booklet 3.5 rigenerato è uguale a quello di prima. La lettura chiesta da §3 serve dove un'uscita cambia: la sposto a L8 (prova con un sistema finto), dove cambia di sicuro.
- **Cosa resta per L5c**: `incantesimi.LISTE` e le tabelle che la accompagnano (`_ARCANO`, `CANONICA`, `FUNZIONE_DI_RIPIEGO`), ~330 righe di liste di classe.

### §2.9 Cosa ha trovato L5c

- **Le liste di incantesimi sono dati**: `LISTE`, `CANONICA`, `FUNZIONE_DI_RIPIEGO`, `SENZA_LISTA` in `sistemi/dnd35/dati/incantesimi.toml`; `PF1E_SOLO` (le aggiunte dell'APG) in `sistemi/pf1e/dati/incantesimi.toml`. Il plugin pf1e dichiara `creature.incantesimi` con i due file in fila: la lista core 3.5, che per PF1e è abbastanza vicina, e le sue aggiunte. `dmcore/incantesimi.py` scende da 711 a 236 righe e tiene solo la logica (funzioni tattiche, scelta, ripiego).
- **Prova**: 5 impronte identiche a prima (`test_sistemi_creature.py`), mago e stregone restano lo stesso oggetto in entrambe le liste, impronte dei generatori 12/12, `test_incantesimi.py` (che confronta ogni voce con le ancore delle skill) verde.
- **M3 73 → 72**. Capacità ancora nel codice: dnd35 `fonti.regole` (L8) e `creature.regole_di_tipo`, pf1e le stesse due, d20 `statblocco.campi`.
- **Resta per L5d**: `creature.regole_di_tipo` (dnd35 punta a `tabelle.TIPI`, che ormai è dati, insieme a `ALIAS_TIPO`; pf1e a `lettura_creatura.NON_MORTO_PF1E`) e `statblocco.campi` di d20 (`statblock.OBBLIGATORI`/`AMMESSI`). Lotto a parte perché tocca `lettura_creatura` e `statblock`, che il verificatore importa.

### §2.10 Cosa ha trovato L5d

- **Le ultime capacità L5 sono dati**: `statblocco.campi` della famiglia d20 in `sistemi/d20/dati/statblocco.toml` (campi obbligatori, ammessi, a lista); `creature.regole_di_tipo` del 3.5 in `creature.toml` (`[tipi]` e il nuovo `[alias_tipo]`); quella di PF1e nel `[tipi.undead]` che il plugin pf1e aveva già. `lettura_creatura.NON_MORTO_PF1E` ora lo legge da lì invece di tenerne una copia: era la stessa terna (d8, BAB 3/4, Volontà), scritta due volte.
- **Prova**: 5 impronte identiche; un test dice che nessuna capacità di L5 è più nel codice per d20, dnd35 e pf1e; banco 12/12.
- **Capacità ancora nel codice**: solo `fonti.regole` (URL e sha256 delle fonti), assegnata a L8. **M3 72 → 68.**
- **Ancora vero dal limite della matrice**: una capacità «dati» dice dove sta la regola, non che ogni strumento la legga per il sistema del file. `derive_statblocks`, `conformita_statblocchi` e `genera_attributi` leggono ancora le tabelle 3.5 anche su una scheda PF1e; il cambio di sistema per file è il lavoro di L6-L8.

### §2.11 Cosa ha trovato L6

- **Cosa cambia**: `build-skills.sh` e `sync-skills.sh` chiedono a `sistemi.py --skill-escluse` quali skill saltare. Si saltano solo le skill che un plugin dichiara (`skill = [...]` in `sistema.toml`) quando quel sistema non è né in `attivi` né in `rinforzo` (D5). Le altre 14 (campagna, prosa, mappe, ambientazione, …) si costruiscono sempre. `--skill=<nome>` vince sull'esclusione.
- **Misura, skill costruite per configurazione** (`build-skills.sh --dry-run`):

| `attivi` | `rinforzo` | skill costruite |
|---|---|---|
| dnd35, pf1e | dnd35, pf1e (oggi) | 18 di 18 |
| dnd35 | pf1e | 18 |
| dnd35 | — | 17 (salta `pathfinder-1e-srd`) |
| pf1e | — | 15 (salta le 3 del 3.5) |

- **Con la configurazione di oggi non cambia niente**: 18 di 18, quindi i pacchetti della CI («Build skill packages») sono gli stessi.
- **Limite**: `forgotten-realms-lore` è un'ambientazione, non un sistema, e D4 la mette in una sezione separata che ancora non esiste. Per ora si installa sempre.

### §2.12 Cosa ha trovato L7

- **Una capacità nuova, la tredicesima**: `stampa.etichette` (CA, pf, TS, Vel, GS, Iniziativa, Sensi) in `sistemi/d20/dati/stampa.toml`; dnd35 e pf1e la ereditano. `build_booklet_html.py` ed `export_booklet_typst.py` la leggono per il sistema del manifest (`sistema_di`), `statblock.etichetta_gs` per la sigla del GS; il tema Typst riceve le sigle come parametro `etichette:` di `#statblocco()`.
- **Misura**: i 19 booklet rigenerati in HTML e in `.hb.md` sono **identici byte per byte** a prima. Il sorgente `.typ` cambia in 98 righe, e sono tutte la riga `etichette: (…)` aggiunta a ogni riquadro, con le stesse sigle che il tema scriveva prima a mano. Il PDF non l'ho compilato in locale (typst non è installato e lo scaricamento è stato negato); l'identità del PDF segue dal fatto che i valori passati sono quelli che il tema aveva cablati.
- **Cosa non fa ancora**: BMC/DMC sulla scheda del PG PF1e. Le schede di oggi non le stampano, e aggiungerle è una scelta di contenuto, non una migrazione: resta per quando il DM vorrà le schede PF1e complete.

### §2.13 Cosa ha trovato L8 (la prova del nove)

- **La prova**: `scripts/tests/test_sistemi_prova_del_nove.py` costruisce un repo temporaneo con `sistemi/`, `sistemi.toml`, il manifest degli strumenti e i file che i plugin elencano, ci aggiunge il plugin finto `scripts/tests/dati/prova-d20/` (tre file `.toml`, nessun codice) e una riga in `[progetto] attivi` e in `[moduli]`. Poi usa gli strumenti veri senza cambiarne una riga.
- **Cosa passa** (9 test): il cancello `sistemi --check` resta verde; tutte le 13 capacità del catalogo sono coperte; un modulo dichiarato prende il sistema nuovo e gli altri restano 3.5; le soglie PE finte arrivano in `update_xp.soglie_di`; il raddoppio 3 arriva in `suggest_encounter.combinatore` (due GS 10: EL 12 in 3.5, EL 13 nel sistema di prova); quello che il plugin eredita è identico al 3.5; nessuna skill cambia.
- **M4 vero = 0 per un sistema d20 che cambia dati**. Il numero del censimento (27) conta i file che *dipendono* dal sistema, non quelli da toccare: non scende con L8, e non è il criterio giusto per la prova. Il criterio di §3 («un sistema finto si aggiunge con 0 file di codice toccati») è soddisfatto.
- **Dove la prova non arriva, detto chiaro**:
  - un sistema con un **modo nuovo di combinare i GS** aggiunge una riga a `METODI` in `suggest_encounter.py`: è codice, ed è voluto (§2.6);
  - un sistema **non d20** (niente GS, CA, TS) non eredita `statblocco.campi` e i generatori di creature non lo sanno costruire: la prova vale per la famiglia d20;
  - `fonti.regole` resta nel codice: il plugin di prova la eredita dal 3.5 e non ne ha avuto bisogno, quindi per la regola di L4 non si sposta;
  - `derive_statblocks`, `conformita_statblocchi` e `genera_attributi` leggono ancora le tabelle del 3.5 anche su una scheda PF1e (§2.10).
- **Lettura del DM**: la prova non cambia nessuna uscita della campagna, perché il sistema finto vive solo nel test. La lettura di un booklet 3.5 rigenerato non serve per nessun lotto: tutte le uscite sono rimaste identiche (impronte 12/12, 19 booklet HTML identici byte per byte).

## §3 · Validazione

| Controllo | Quando | Criterio |
|---|---|---|
| Banco d'invarianza (`impronte.py --confronta`) | ogni lotto, prima e dopo | 12/12 impronte identiche sui moduli 3.5 |
| `censimento.py --check` | ogni lotto, poi in CI | nessun file con punteggio ≥ 10 senza classe; M3 non sale |
| `sistemi.py --check` | da L1, in CI (canale testing di ADR-0099, poi stable) | ogni capacità chiesta da uno strumento esiste, eredita con motivo, o è `non supportato` dichiarato |
| Rifiuto pulito | da L4 | uno strumento su un modulo senza la capacità esce 2 prima di scrivere, come `binari.py` |
| Test esistenti | ogni lotto | `test_grafo_import_creature.py` e tutta la suite verdi; nessun test saltato |
| Prova del nove | L8 | un sistema finto si aggiunge con 0 file di codice toccati |
| Lettura del DM | L2 e L5 | la matrice e un booklet 3.5 rigenerato letti dal DM, non solo i validatori |

## §4 · Decisioni al DM

| # | Domanda | Consigliata | Cosa cambia |
|---|---|---|---|
| D1 | Formato del file generale | **TOML** | TOML ha le sezioni di un INI, liste e tipi veri, e si legge con `tomllib` della libreria standard. INI (`configparser`) non ha liste né tipi: «attivi» diventa una stringa da spezzare. YAML è già nel repo ma chiede PyYAML o il lettore ridotto di `dmcore/config.py` |
| D2 | Dove si dichiara il sistema di un modulo | **in `sistemi.toml` per cartella; la riga «Sistema:» resta nel master per chi legge, e un controllo verifica che dica lo stesso** | con la riga come fonte servirebbe normalizzare 10 grafie in 26 file; con i profili resterebbero fuori i master senza profilo |
| D3 | Quanto fare adesso | **L1 e L2 in una PR, poi un lotto per PR con il banco** | tutto in una PR vuol dire L5 (il rischio più alto) insieme alla fondazione, e una revisione molto più difficile |
| D4 | L'ambientazione (Forgotten Realms, Golarion) nello stesso file | **sì, in una sezione separata** | i due assi sono diversi (il Drappo è PF1e e Golarion, il Giardino PF1e è PF1e ma non Golarion); tenerli insieme evita un secondo file |
| D5 | Quali skill installare per gli agent | **quelle dei sistemi attivi più quelle dei sistemi di rinforzo** | filtrare solo sugli attivi toglierebbe `pathfinder-1e-srd` a una campagna solo 3.5, che la usa per i villain; installare sempre tutto lascia la configurazione solo informativa |

## §5 · Checklist

- [x] L0 · censimento, banco d'invarianza, ADR-0111 proposta, piano (2026-11-07)
- [x] D1-D5 decise (2026-11-08: le consigliate; D4 applicata con `[ambientazioni]` e `ambientazione_di()`)
- [x] L1 · fondazione (2026-11-07): la matrice dice per ogni sistema come copre ogni capacità; finché L3-L5 non migrano gli strumenti, una riga dice dove sta la regola del sistema, non che quello strumento la legga già da lì (es. `validate_prosa` usa ancora le abilità 3.5 anche su un modulo PF1e)
- [x] L1-bis · PF1e nei 5 casi non supportati (2026-11-07): PE, incontri, tesoro, classi e razze, costruzione delle creature
- [x] L2 · un rilevamento solo (2026-11-07): catalogo, censimento, domande del developer, `e_pf1`, cancello della riga «Sistema»; M1 5 → 1
- [x] L3 · termini (2026-11-07): lista 5e unica nel plugin d20, abilità e entità dai dati dei plugin; M2 2 → 1
- [x] L4 · regole semplici (2026-11-07): PE ed EL dal plugin, nessun «dnd35» cablato in update_xp, suggest_encounter, suggest_loot
- [x] L5 · nucleo delle creature (2026-11-07): L5a tabelle base, L5b incantatori, prestigio, profili, taglie e razze, L5c liste di incantesimi, L5d regole di tipo e campi dello statblocco, tutto dal plugin con impronte dei valori identiche
- [x] L6 · skill e agent (2026-11-07): build-skills.sh e sync-skills.sh saltano le skill dei sistemi né attivi né di rinforzo (`sistemi.py --skill-escluse`)
- [x] L7 · etichette di stampa (2026-11-07): capacità `stampa.etichette` della famiglia d20, lette dalle due catene per il sistema del manifest
- [x] L8 · prova del nove (2026-11-07): `test_sistemi_prova_del_nove.py`, plugin finto `prova-d20` di soli dati, 0 file di codice toccati
