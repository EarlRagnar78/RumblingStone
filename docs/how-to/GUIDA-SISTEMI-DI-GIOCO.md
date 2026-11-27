# Guida ai sistemi di gioco: usarli e aggiungerne uno

> Forma: **guida pratica** (Diátaxis). Risolve compiti a chi sa già cos'è un
> modulo e cos'è `dm.py`. Il formato dei file e l'elenco completo delle
> capacità stanno nel [riferimento dei plugin](../reference/RIFERIMENTO-PLUGIN-DI-SISTEMA.md);
> il perché nell'[architettura §19](../explanation/ARCHITETTURA.md#19-il-motore-delle-regole-e-i-sistemi-di-gioco)
> e negli ADR [0111](../../plans/adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md)
> e [0112](../../plans/adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md).

## 0 · In breve

```bash
python3 scripts/dm.py sistemi                    # sistemi attivi e cosa sa fare ogni strumento
python3 scripts/dm.py sistemi --di FILE          # il sistema di un file
python3 scripts/dm.py sistemi --check            # il cancello della CI
python3 scripts/genera_creatura.py --gs 5 --sistema pf1e   # uno strumento in un sistema
```

Oggi i sistemi attivi sono due: **dnd35**, predefinito e sistema della
campagna, e **pf1e**, sistema del Drappo e del Giardino a Qasr al-Milah.
Tutti e due sono anche di *rinforzo*: è lì che si cerca la versione più
potente di una regola, prima nel 3.5 e poi in PF1e.

## 1 · Sapere quale sistema usa un file

```bash
python3 scripts/dm.py sistemi --di "10-stand-alone/Il-Drappo-di-Tarsilia/README.md"
# pf1e
python3 scripts/dm.py sistemi --di "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
# dnd35
```

La risposta viene da `[moduli]` di `sistemi.toml`. Vince il percorso più
lungo che contiene il file; un file fuori da tutti usa `predefinito`. Ogni
strumento che dipende dal sistema fa la stessa domanda, quindi questa è anche
la risposta a «con quali regole lo controlla la CI?».

## 2 · Mettere un modulo in un altro sistema

Per esempio un modulo nuovo in Pathfinder 1e:

1. Aggiungi la cartella a `[moduli]` di `sistemi.toml`:

   ```toml
   [moduli]
   "10-stand-alone/Il-mio-modulo" = "pf1e"
   ```

   Il sistema deve stare in `[progetto] attivi`.
2. Nella testa del modulo scrivi la riga del sistema con un nome che il
   plugin riconosce (il campo `riconosci` di `sistemi/pf1e/sistema.toml`):

   ```markdown
   **Sistema:** Pathfinder 1e
   ```

   Se la riga e `sistemi.toml` dicono due sistemi diversi, il cancello è
   rosso.
3. Se il modulo ha un mondo diverso dai Forgotten Realms, aggiungilo anche a
   `[ambientazioni.moduli]`: il mondo è un asse diverso dal sistema (il Drappo
   è PF1e e Golarion, il Giardino PF1e non ha un mondo ufficiale).
4. Controlla:

   ```bash
   python3 scripts/dm.py sistemi --di "10-stand-alone/Il-mio-modulo/README.md"
   python3 scripts/dm.py sistemi --check
   ```

## 3 · Usare gli strumenti in un sistema

Gli strumenti delle creature (`conformita_statblocchi`, `derive_statblocks`,
`genera_attributi`, `impronta_creature`, `validate_bestiario`) prendono da
soli il sistema del file. Quattro strumenti di preparazione hanno
`--sistema`; senza, usano il predefinito:

| Compito | Comando | Scelta di campagna PF1e |
|---|---|---|
| PE e passaggi di livello | `python3 scripts/update_xp.py --sistema pf1e` | `--traccia lenta\|media\|veloce`, altrimenti `traccia_pe` |
| Incontro e suo GS | `python3 scripts/suggest_encounter.py --sistema pf1e …` | — (il GS è la somma dei PE) |
| Tesoro per incontro | `python3 scripts/suggest_loot.py --sistema pf1e …` | `--velocita lenta\|media\|veloce`, altrimenti `velocita_tesoro` |
| Una creatura da GS, tipo e ruolo | `python3 scripts/genera_creatura.py --gs 5 --sistema pf1e` | classi del PRD e multiclasse, es. `--classe "mago:5,mistificatore arcano:3"` |

Le scelte di campagna che il PRD lascia al GM stanno in `[opzioni.pf1e]` di
`sistemi.toml`. `genera_creatura --in CARTELLA` senza `--sistema` genera nel
sistema della cartella.

Uno strumento scritto sulle tabelle 3.5 che incontra un file di un sistema
con regole diverse **salta il file e dice quali regole mancano**, invece di
contarlo con le regole sbagliate. La tabella «Cosa sa fare ogni strumento con
ogni sistema attivo» di `dm.py sistemi` dice in anticipo dove succede.

## 4 · Accendere o spegnere un sistema

Spegnere vuol dire togliere l'id da `[progetto] attivi` (e da `rinforzo`, se
c'è). Il plugin resta nel repo ed elencato; le sue skill escono dai pacchetti,
perché `build-skills.sh` e `sync-skills.sh` chiedono a
`sistemi.py --skill-escluse` quali saltare. Un modulo assegnato in `[moduli]`
a un sistema spento rende il cancello rosso: o lo riassegni o non spegni.

## 5 · Aggiungere un sistema della famiglia d20

Vale per un sistema che condivide l'impianto d20 (dado, caratteristiche, TS,
BAB, GS). Un sistema non d20 oggi resta fuori: il plugin finto a mucchio di
d10 dei test entra senza toccare il nucleo, ma ci lavorano per intero solo 4
strumenti, 3 in parte (`suggest_encounter`, `genera_creatura`,
`verifica_scheda`) e 15 lo rifiutano; il tiro non ha una capacità nel catalogo.

1. **Prima la misura.** Scrivi da dove vengono le regole (SRD, PRD, un
   documento con licenza aperta) e scaricale in cache con
   `riscontro_srd.py` se si può. Ogni tabella del plugin si misura poi contro
   quella fonte (ADR-0121), non contro un valore scritto a mano.
2. **La cartella.** Crea `sistemi/<id>/sistema.toml` con `id`, `nome`,
   `tipo = "sistema"`, `famiglia = "d20"`, `licenza`, `fonti`, `riconosci`,
   `skill`. Parti copiando `sistemi/pf1e/sistema.toml`.
3. **Le capacità.** Per ognuna delle 20 del catalogo scegli un modo:
   `eredita` da `d20` o da un altro sistema quando la regola è la stessa
   (con il motivo), `dati` con i tuoi file in `sistemi/<id>/dati/` quando è
   diversa, `non_supportato` con il motivo quando non serve. Non lasciarne
   nessuna fuori: una capacità non dichiarata è un buco e il cancello lo
   dice. Esempio completo, che cambia una formula e un metodo: il plugin
   finto `scripts/tests/dati/prova-d20-due/`.
4. **Formule e algoritmi.** Una formula diversa va in un tuo `formule.toml`;
   un algoritmo che non è una tabella né una formula va in
   `sistemi/<id>/codice/<modulo>.py` ed è registrato in `[moduli]` come
   `nome = "modulo:funzione"`. Il linguaggio delle formule e le regole del
   codice sono nel riferimento, §6 e §7.
5. **Accendilo** in `[progetto] attivi`, e assegnagli i moduli in `[moduli]`.
6. **Prove.**

   ```bash
   python3 scripts/dm.py sistemi --check           # struttura, eredità, formule, moduli, righe «Sistema»
   python3 scripts/dm.py sistemi                   # la matrice: niente «mancante» per i sistemi attivi
   python3 -m pytest scripts/tests/test_sistemi*.py scripts/tests/test_formule.py \
       scripts/tests/test_prova_del_nove_2.py scripts/tests/test_impronta_creature.py -q
   ```

   Le uscite 3.5 devono restare identiche: i test con le impronte lo
   controllano.
7. **ADR e card.** Un sistema nuovo è una decisione di campagna: va a Jfs con
   una card e un ADR, come PF1e con ADR-0111.

## 6 · Se il cancello è rosso

| Messaggio di `sistemi.py --check` | Cosa vuol dire | Cosa fare |
|---|---|---|
| `il predefinito «X» non è fra gli attivi` | `predefinito` punta a un sistema spento | rimetti X fra gli `attivi` o cambia predefinito |
| `«X» non ha un plugin in sistemi/X/sistema.toml` | un id in `attivi` o `rinforzo` senza cartella | crea il plugin o togli l'id |
| `[moduli]: «C» usa «X», che non è attivo` | una cartella assegnata a un sistema spento | riassegnala o accendi X |
| `[moduli]: la cartella «C» non esiste` | la cartella è stata spostata o rinominata | correggi la chiave |
| `«N» eredita senza motivo` | manca `motivo` accanto a `eredita` | scrivi perché la regola è la stessa |
| `«N» deve avere uno e un solo modo fra (…)` | la capacità ha zero o due modi | lasciane uno: `dati`, `codice`, `eredita`, `non_supportato` |
| `«S» chiede «N», che «X» non dichiara` | uno strumento chiede una capacità che il plugin non copre | dichiarala, anche come `non_supportato` |
| `la riga «Sistema» dice «A», sistemi.toml [moduli] dice «B»` | il modulo e la configurazione non sono d'accordo | correggi la riga o aggiungi la cartella a `[moduli]` |
| `[moduli] nome: … non è in sistemi/X/codice/` | un modulo di codice punta fuori dalla cartella del plugin | sposta il file in `codice/` o correggi `modulo:funzione` |

Il caricatore è `scripts/dmcore/sistemi.py`, funzione `problemi()`: l'elenco
completo dei messaggi è lì.
