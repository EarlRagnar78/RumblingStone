# Fotografia di partenza della prosa di ARC-07, prima del rifacimento

**Data**: 2026-10-18 · **Versione**: `main` dopo la #244, prima della #245 · **Protocollo**: ADR-0093 e `PROSA-DETERMINISTICA-2026-10-18` §6

È il «prima». Il «dopo» si misura con gli stessi comandi sul master rifatto, e
il rifacimento è migliorato solo se passa tutte e due le prove:

1. **nessun numero di queste tabelle peggiora** (il cancello di `ciclo_prosa`, e
   qui anche gli indicatori);
2. **il DM preferisce alla cieca la versione nuova in almeno 14 coppie su 20**
   del campione congelato in `campione-ARC07-DEF.json`.

## MQM (`punteggio_mqm.py`)

| Master | MQM |
|---|---:|
| DEF-1 Piano della Terra | 99,51 |
| DEF-2 Ritorno e affreschi | 97,53 |
| DEF-3 Resurrezione Hella | 98,76 |
| DEF-4 Viaggio 1.000 anni | 99,73 |
| DEF-5 Ritorno Hammerfist | 99,87 |

## Box contro le soglie (`misura_craft --box`)

| Master | Box | >12 righe | Parentesi | >1 nome | >4 frasi | >500 car |
|---|---:|---:|---:|---:|---:|---:|
| DEF-1 | 28 | 0 | 3 | 7 | 16 | 9 |
| DEF-2 | 19 | 0 | 1 | 8 | 13 | 8 |
| DEF-3 | 19 | 0 | 1 | 9 | 12 | 6 |
| DEF-4 | 35 | 0 | 2 | 2 | 18 | 4 |
| DEF-5 | 7 | 0 | 0 | 1 | 3 | 1 |

## Stile (`misura_craft --stile`, indicatori senza peso)

| Master | Parole di box | Gerundio in coda | -mente (‰) | Battute | >25 parole | >40 parole |
|---|---:|---:|---:|---:|---:|---:|
| DEF-1 | 2.059 | 0 | 1 (0,5) | 4 | 2 | 1 |
| DEF-2 | 1.655 | 0 | 2 (1,2) | 1 | 0 | 0 |
| DEF-3 | 1.307 | 0 | 0 | 8 | 6 | 3 |
| DEF-4 | 2.243 | 0 | 0 | 10 | 1 | 1 |
| DEF-5 | 456 | 0 | 0 | 3 | 0 | 0 |

Il confronto che dice che gli indicatori separano qualcosa: ARC-08, scritto
prima del ciclo di prosa, ha 9 gerundi in coda (1,7‰) e 30 avverbi in -mente
(5,8‰, sopra l'allarme) su 5.164 parole di box. I DEF di ARC-07, passati dal
ciclo, stanno già bassi su questi due: il margine di miglioramento misurabile
è nelle **battute lunghe di DEF-3** (6 su 8 oltre 25 parole) e nelle colonne
`>4 frasi` e `>500 car` della tabella dei box.

## Il campione per il cieco

Venti box, quattro per master, seme `20261018`, almeno 25 parole, escluse le
note per il DM con un numero di regola. Rispetto alla testa della #245
(`2080b98`) diciannove sono identici e uno cambia (DEF-5 Scena 3, somiglianza
0,90): il campione vale anche dopo la sua fusione.

## Come si rifà

```
python3 scripts/punteggio_mqm.py "07_il Portale Della Forgia Eterna/ARC07-DEF-*.md"
python3 scripts/misura_craft.py --box --stile
python3 scripts/cieco_versioni.py coppie --campione plans/esperimenti/prosa-cieco/campione-ARC07-DEF.json \
    --dopo <ref del rifacimento> --seme <un numero nuovo> --scheda SCHEDA.md --chiave CHIAVE.json
# il DM legge SCHEDA.md ad alta voce e scrive VOTI.txt, una riga «N A», «N B» o «N =»
python3 scripts/cieco_versioni.py esito --chiave CHIAVE.json --voti VOTI.txt
```

La chiave non si apre prima dei voti, e il seme di `coppie` si sceglie dopo il
rifacimento: chi riscrive non sa in che ordine il DM leggerà.
