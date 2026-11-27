# Prova non d20: un sistema a mucchio di d10

> 2026-11-08 · dopo F6 di ADR-0112 · scelta del DM il 2026-11-08: «Lupi Mannari (mucchio di d10)», come prova e non per giocare · test: `scripts/tests/test_prova_non_d20.py` · plugin finto: `scripts/tests/dati/prova-mucchio-d10/`

## In breve

Un sistema senza famiglia d20 entra nel motore **senza toccare il nucleo**: cancello verde, formule sue, codice dei dadi suo, minaccia al posto dell'EL, termini e abilità suoi. Ma degli strumenti di oggi ci lavorano davvero **4 su 20**, uno a metà, e **15 rifiutano il file**. È quello che ADR-0112 dice al punto 6 (ambito d20): il nucleo non impedisce un sistema non d20, ma gli strumenti delle creature, del tesoro, dei PE e della stampa sono d20 per costruzione.

## Licenza

Le meccaniche sono scritte con parole e numeri nostri. Nel plugin non c'è una tabella, un nome di tratto o una frase dei manuali. Il meccanismo è quello generico dei giochi a mucchio di d10, nello stile di Lupi Mannari: tanti dadi quanti attributo più abilità, successo da una soglia in su, rilancio del dado più alto. Non è una conversione di un manuale, e i numeri non vanno presi come regole di un gioco pubblicato.

## Il plugin

| Capacità | Modo | Cosa c'è |
|---|---|---|
| `formule.regole` | dati | mucchio = attributo + abilità; mucchio con penalità (mai sotto zero); salute = vigore + taglia; iniziativa; difesa = il più basso fra destrezza e prontezza |
| `incontri.livello` | dati + codice | metodo «minaccia»: la somma dei successi attesi dei mucchi d'attacco, e i parametri del tiro (soglia 8, rilancio 10, «uno annulla» spento) |
| `termini.vietati` | dati | tiro salvezza, CA/GS/DV/BAB con un numero, punti ferita, d20 |
| `lessico.abilita` | dati | dieci nomi generici nostri, e le abilità 3.5 come estranee |
| le altre 12 | `non_supportato` | ognuna con il motivo (niente classi, GS, DV, liste d'incantesimi, soglie di livello, tesoro per livello, riquadro d20) |

Il codice del plugin sta in `codice/`: `dadi.py` dà la distribuzione esatta dei successi (frazioni, rilancio fermato dopo 40 rilanci con la coda sommata all'ultimo valore), `incontri.py` la minaccia.

## Cosa regge (misurato)

| Prova | Esito |
|---|---|
| `sistemi.py --check` e il controllo delle formule con il sistema attivo | 0 problemi |
| un file nella cartella del sistema | `sistema_di` dà il sistema nuovo |
| eredità nascosta | nessuna: niente famiglia, nessun modulo d20 visibile, nessuna delle 6 formule d20 passa |
| probabilità del tiro | sommano a 1 per 0-10 dadi; un dado riesce 3 volte su 10 (e 7/100 dei successi vengono dal rilancio) |
| successi attesi | n/3 per n dadi, a 12 decimali |
| tiro simulato | 20.000 tiri di 6 dadi con seme fisso: ogni valore con probabilità sopra l'1% sta entro 4 σ dalla distribuzione esatta |
| variante «uno annulla» (soglia 6, niente rilancio) | si ottiene solo cambiando i dati: un dado dà −1, 0, +1 con 1/10, 4/10, 5/10; quattro dadi danno 1,6 successi attesi |
| `suggest_encounter` | usa la minaccia del plugin: mucchi 6, 6 e 3 → 5 successi attesi; il 3.5 resta 12 per due GS 10 |
| `validate_modules` | in un modulo del sistema segnala «tiro salvezza», «CA 18» e «punti ferita», e lascia passare «mucchio di 7 dadi, Vigore 4 + Rissa 3» |

## Il censimento degli strumenti

Dei 20 strumenti del manifest che chiedono capacità di sistema:

- **4 trovano tutto nel plugin**: `domande_developer`, `validate_modules`, `validate_prosa`, `validate_standalone`;
- **1 a metà**: `suggest_encounter` (la minaccia sì, la lettura delle schede del Bestiario no);
- **15 non trovano niente** e devono rifiutare il file.

Il rifiuto è provato su 9 dei 15: `suggest_loot`, `update_xp`, `build_booklet_html` ed `export_booklet_typst` (le etichette) si fermano con «non_supportato»; `genera_creatura` dice «nessuna conversione»; `conformita_statblocchi`, `derive_statblocks`, `genera_attributi`, `impronta_creature` e `validate_bestiario` saltano il file e dicono quali regole mancano (F4). Gli altri 6 (`build_monster_catalog`, `coerenza_campagna`, `extract_statblocks`, `lessico_regole`, `riscontro_srd` e la parte di `export_booklet_typst` che non stampa le etichette) **non li ho provati** su un file del sistema.

## Note oneste

- **Il tiro non ha una capacità sua.** Nel catalogo non c'è una voce per la meccanica dei dadi, quindi soglia, rilancio e «uno annulla» stanno nei dati di `incontri.livello`. Funziona, ma è un posto preso in prestito. Se arriva un sistema non d20 vero, il catalogo vuole una riga per il tiro.
- **Le parole sono d20.** `suggest_encounter` mette la minaccia dove di solito c'è l'EL, e il numero di dadi dove c'è il GS: i conti tornano, ma testi e opzioni parlano ancora di GS ed EL.
- **Il rifiuto è un errore, non un messaggio.** `suggest_loot` e `update_xp` si fermano con un'eccezione `ErroreSistemi` che dice il motivo giusto, ma con lo stack di Python davanti.
- **Il plugin resta un test.** Sta in `scripts/tests/dati/` e non entra mai in `sistemi/`, come i due plugin delle prove del nove.

## Come si rifà

```
python3 -m pytest -q scripts/tests/test_prova_non_d20.py
python3 scripts/sistemi.py --check
```
