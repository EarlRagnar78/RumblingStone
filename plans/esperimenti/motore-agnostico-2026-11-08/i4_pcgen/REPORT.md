# I4 · Cosa prendiamo da PCGen (2026-11-08)

**Domanda.** [PCGen](https://github.com/PCGen/pcgen) è il riferimento che il DM ha indicato per un motore d20 guidato dai dati. Quali delle sue idee adottiamo, quali no, e per quale motivo?

**Come si rifà.** Lo script `conta_pcgen.py` di questa cartella lavora su un clone parziale di PCGen. Il comando per prepararlo è scritto nella docstring dello script. Il commit misurato è `d96d4da3` del 2026-11-05. I dati grezzi stanno in [RISULTATI.json](RISULTATI.json). Ho letto direttamente i file del clone e non pagine di riassunto:

- `system/gameModes/35e` e `system/gameModes/Pathfinder`;
- `core_rulebook.pcc` e i file `cr__*.lst` del Core Rulebook PF1e;
- il RSRD 3.5.

## Misure

| Insieme di dati | File `.lst` | Formulario vecchio (`BONUS:`) | Formulario nuovo (`MODIFY:`) | Quota del nuovo | Variabili dichiarate |
|---|---|---|---|---|---|
| PF1e Core Rulebook | 39 | 6.141 | 24 | **0,39%** | 16 |
| 3.5 RSRD | 84 | 11.898 | 0 | **0%** | 0 |

Le formule che il *game mode* scrive come testo, senza contare i numeri soli, che sono righe di tabella, sono 9 in 3.5 e 13 in Pathfinder. Eccone alcune:

- `SPELLBASEDC:10+SPELLLEVEL+BASESPELLSTAT`, cioè la nostra `cd_incantesimo`;
- `STATMOD:floor(SCORE/2)-5`, cioè la nostra `mod`;
- `MINXP:(LEVEL*LEVEL-LEVEL)*500`;
- `SPELLRANGE:CLOSE|floor(CASTERLEVEL/2)*5+25`.

## Che cosa dicono i numeri

- **Le formule d20 come testo nei dati funzionano.** PCGen le tiene così da sempre, e sono le stesse formule che I1 ha messo nel banco. È una conferma esterna della fase F3.
- **Migrare il linguaggio delle formule costa molto.** PCGen ha introdotto un formulario nuovo, con variabili tipizzate e uno scope (`GLOBAL`, `LOCAL`, `CHANNEL`) in `cr__variables.lst`, e lo applica con `MODIFY`. Nel commit di oggi il nuovo copre lo 0,39% del Core Rulebook PF1e e lo 0% del RSRD 3.5. I due sistemi convivono, e chi scrive i dati deve conoscerli tutti e due. Era il rischio scritto in §5 del piano, e ora è misurato.

## Concetti di PCGen e cosa ne facciamo

| PCGen | Da noi | Lo adottiamo? | Motivo |
|---|---|---|---|
| *game mode* (`system/gameModes/<modo>`): regole di base del sistema | `sistemi/<id>/sistema.toml` più `dati/` | **sì, c'è già** (ADR-0111) | è lo stesso taglio |
| manifest `.pcc`: `GAMEMODE`, `BOOKTYPE`, `RANK`, `PCC:` (include), un file per ogni tipo (`STAT:`, `SAVE:`, `DATACONTROL:`) | `sistema.toml` con le capacità che puntano ai file | **sì, c'è già** | ogni capacità nomina il suo file, come fa PCGen per tipo |
| `ALLOWEDMODES`: un dato vale per più modi | `eredita` dalla famiglia `d20` | **sì, c'è già** | la stessa idea, scritta come eredità |
| `SOURCELONG`, `SOURCEWEB`, `SOURCEDATE`, `COPYRIGHT`, `ISOGL` nel manifest | `fonti.regole` oggi è codice | **sì → F1** | per PCGen le fonti sono dati del pacchetto, ed è quello che fa F1 con `fonti.toml` |
| formule come testo nei dati (`SPELLBASEDC`, `STATMOD`) | `formule.toml` del plugin, valutato con simpleeval ristretto (I1) | **sì → F3** | quando possibile usiamo nomi di variabile leggibili, come fa PCGen |
| variabili dichiarate con tipo (`GLOBAL:NUMBER=STR`) | ogni formula dichiara i suoi ingressi; un nome non dichiarato ferma il plugin in CI (I1, proposta 2) | **sì, la dichiarazione** | prende gli errori di battitura nelle formule |
| scope delle variabili (`LOCAL:PC.STAT`, `CHANNEL`) | — | **no** | serve a una scheda del personaggio che cambia mentre la si usa. I nostri strumenti calcolano un blocco statistiche e finiscono |
| funzioni del motore usate dai dati (`d20Mod()`, `classlevel()`) | una lista corta di funzioni ammesse dal valutatore; gli algoritmi veri stanno nei moduli del plugin (I3) | **sì, in forma ridotta** | in PCGen queste funzioni sono codice Java del nucleo. Da noi, se sono di un sistema, stanno nel plugin |
| `DATACONTROL`/`FACTDEF` (`DATAFORMAT:String`): lo schema dei dati, in un linguaggio di PCGen | JSON Schema accanto ai dati (I2) | **il concetto sì, il formato no** | JSON Schema è uno standard con librerie ed editor; il formato di PCGen ha solo il parser di PCGen |
| formato LST: tag separati da tabulazioni | TOML | **no** | non ha librerie standard né controllo negli editor; TOML ha `tomllib` nella libreria standard |
| due formulari che convivono (`BONUS` e `MODIFY`) | — | **no, è la lezione** | in F3 ogni formula si migra insieme al test che la confronta con la funzione Python, e il nucleo non tiene una seconda strada. Nessun periodo di convivenza oltre la PR |
| schede di uscita FreeMarker (`base.xml.ftl`) | modelli typst (ADR-0105, ADR-0106) | fuori da questo piano | la stampa ha già il suo standard |

## Note oneste

- Ho letto solo due insiemi di dati e due *game mode*, non tutto PCGen. La quota del formulario nuovo potrebbe essere più alta in altri insiemi.
- Non ho trovato una data verificata per l'introduzione del formulario nuovo, quindi non la scrivo. Il dato misurato è la quota di oggi.
- Il codice di PCGen non si riusa: è Java, e il nostro motore è Python. Da PCGen prendiamo il taglio dei dati.
