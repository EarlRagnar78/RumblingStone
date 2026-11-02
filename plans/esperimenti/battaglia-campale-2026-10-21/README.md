# La battaglia campale di Hammerfist: la taratura del libretto

Esperimento del 2026-10-21 per `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md`
([ADR-0096](../../adr/ADR-0096-la-battaglia-campale-si-gioca-con-un-libretto.md)).
Gli script non sono strumenti del repo: servono a rifare i numeri.

- `simula.py`: un settore, un giorno (la prima versione, v1).
- `tre_giorni.py`: quattro settori, tre giorni, le perdite che passano da un
  giorno all'altro, la notte, il morale, la pressione e le brecce (v2, quella
  del libretto). `python3 -I tre_giorni.py 1372 2 3 1 B` è l'orda feroce nel
  modo B; il quarto numero è la ferocia (0 normale, 1 feroce, 2
  terrificante), il quinto il modo (B o C).

## Cosa è venuto (3.000 battaglie per riga, seme 1372)

«Breccia» è la riga Breccia contenuta di `ARC08-10` §5.2 (brecce nei giorni 1-2:
0 / 1 / 2+); «posizioni» la riga Posizioni tenute di §5.3 (reparti vivi alla
ritirata: tre quarti o più / da un terzo / meno). Pieno/parziale/fallito, in %.

| Orda | Modo | Gioco | Breccia | Posizioni |
|---|---|---|---|---|
| normale | B | attento | 82/15/2 | 90/9/1 |
| feroce | B | attento | 70/21/8 | 74/18/9 |
| feroce | B | sempre colpire | 72/17/11 | 27/39/34 |
| feroce | B | sempre tenere | 9/24/67 | 54/31/15 |
| feroce | B | sempre caricare | 30/21/49 | 1/8/91 |
| feroce | C | sempre colpire | 72/12/16 | 58/26/16 |
| terrificante | B | attento | 45/30/25 | 37/30/33 |

Il gioco «attento» tiene un reparto ridotto a 4 PFU o meno, carica contro gli
orchi, altrimenti colpisce, e l'eroe combatte sempre. Nel modo C il gioco
migliore è colpire sempre (tenere costa tacche che nessun eroe compensa).

## La correzione dopo le letture a freddo

La prima taratura aveva un errore di uno nel dado bianco, trovato dalla
lettura a freddo del DM: mancare di k vuol dire che l'orda supera di k−1, quindi
le fasce sono 1-5, 6-10, 11+ e non 1-4, 5-9, 10+. Il simulatore faceva perdere
un PFU anche a pareggio. Con il conto giusto i nani erano più forti e il modo
C con +2 a ogni dado vinceva quasi sempre (96% breccia «pieno»): il capitano
ora non dà bonus, e il terzo reparto basta. I numeri sopra sono quelli
corretti.

## La v3: terreno, capacità, baliste, trappole e l'avanguardia

Il 2026-10-21 il DM ha chiesto battaglie meno monotone e una prova che sia
l'avanguardia. `assedio_v3.py` aggiunge le merlature delle Mura, i balestrieri
sulle torri, la balista di ogni torre, Spezzare la carica e il Muro di scudi,
le capacità dell'orda (`ARC08-19`), le trappole che annullano tacche e il
tetto di ±2 del morale sui dadi. `avanguardia.py` è la scaramuccia della
Sessione 1. Le politiche sono quelle «attente», con l'ordine per reparto.

| Orda (ferocia v3) | Trappole | Breccia | Posizioni |
|---|---|---|---|
| normale (1) | 4 | 90/9/1 | 86/14/0 |
| feroce (2) | 0 | 67/22/11 | 51/35/14 |
| feroce (2) | 6 | 73/21/6 | 55/36/9 |
| terrificante (3) | 4 | 45/31/24 | 18/39/43 |

Il morale è la leva più sensibile: con l'orda feroce, partire da 0 invece che
da +1 porta la breccia «pieno» dal 73% al 50%, e senza il tetto di ±2 era
peggio. Un reparto delle mura perso prima dell'assedio la porta al 32%. Per
questo l'avanguardia costa solo trappole.

Questa tabella è della prima v3, con le trappole valide il solo giorno 1.
Quella in uso è la successiva.

### La v3 dopo le letture del 2026-10-21

Tre cambi nello script, decisi dopo il triage del giro sulla Sessione 1
(`plans/esperimenti/giro-arc08-sessione1-2026-10-21/TRIAGE.md`, T25, T32,
T47, T60):

- una trappola annulla una tacca **del giorno 1 o del giorno 2** (decisione
  del DM; prima valeva il solo giorno 1, e dalla terza trappola in poi non
  cambiava niente);
- la carta dei giganti tira **un macigno per settore** al round 2 dei giorni
  1 e 2: lo script lo faceva già, ora lo dice anche il libretto;
- il macigno conta il +1 del primo giorno e il morale, **non le merlature**
  delle Mura, come dicono i Segreti dell'orda.

In più lo script prende un ottavo argomento, la politica: `attento` (il
default), oppure `tenere`, `colpire`, `caricare` dati sempre a tutti i
reparti. I comandi:

```bash
for f in 1 2 3; do for t in 0 3 4 5 6; do python3 -I assedio_v3.py $f $t 1; done; done
python3 -I assedio_v3.py 2 4 1 1372 0 1 2 tenere     # e colpire, caricare
python3 -I assedio_v3.py 2 4 1 1372 0 0               # morale di partenza 0
python3 -I assedio_v3.py 2 4 1 1372 1 1               # un reparto perso prima
for r in 2 3 4 5 6; do python3 -I avanguardia.py 2 $r; done
```

3.000 battaglie per riga, seme 1372. Breccia e posizioni come sopra,
pieno/parziale/fallito in %.

| Orda (ferocia v3) | 0 trappole | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| normale (1), breccia | 87/11/2 | 95/4/0 | 96/4/0 | 97/2/0 | 98/2/0 |
| normale (1), posizioni | 84/14/2 | 87/12/0 | 88/12/1 | 87/12/0 | 88/12/1 |
| feroce (2), breccia | 67/22/10 | 78/16/5 | 83/14/4 | 87/10/3 | 89/9/2 |
| feroce (2), posizioni | 50/37/13 | 57/33/10 | 58/34/7 | 60/33/6 | 60/33/7 |
| terrificante (3), breccia | 37/28/35 | 47/31/22 | 53/28/20 | 58/26/16 | 63/22/15 |
| terrificante (3), posizioni | 16/36/48 | 18/40/42 | 20/42/38 | 22/40/38 | 23/39/38 |

Ogni trappola fino alla sesta vale ora tre o quattro punti di breccia
«pieno» con l'orda feroce. Con 3-6 trappole la riga «Feroce» del libretto
passa da 7 a 8-9 su 10 di breccia contenuta e da poco più di metà a sei su
dieci di posizioni tenute. La ferocia di default resta feroce.

Le politiche estreme, orda feroce e 4 trappole:

| Politica | Breccia | Posizioni | Reparti vivi su 8 |
|---|---|---|---|
| attento | 83/14/4 | 58/34/7 | 5,6 |
| sempre tenere | 25/41/34 | 94/6/0 | 7,3 |
| sempre colpire | 67/21/12 | 10/37/52 | 2,7 |
| sempre caricare | 14/22/64 | 0/2/98 | 0,3 |

Il morale resta la leva più sensibile: da 0 invece che da +1 la breccia
«pieno» scende dall'83% al 60%, e un reparto delle mura perso prima
dell'assedio la porta al 36%.

L'avanguardia non cambia: lo script ritirava già tutto il gruppo insieme e
contava le trappole sul gruppo, che ora sono la regola del libretto (la
ritirata di gruppo l'ha decisa il DM). Rifatta con gli stessi comandi, dà gli
stessi numeri:

| Avanguardia, orda feroce | Trappole portate a casa | Squadre travolte |
|---|---|---|
| ritirata dopo il round 2 | 4,0 (sempre 4) | 0 |
| ritirata dopo il round 3 | 5,1 (6+ nel 35%) | 0,25 |
| dopo il round 4 | 5,0 (6+ nel 36%) | 0,9 |
| dopo il round 5 | 3,9 | 1,9 |
| dopo il round 6 | 2,2 | 2,9 |

## Cosa non è provato

- Le carte di Gorthak, Grimjaw e della palla di fuoco, il gesto Sfidare, il
  Fuoco di copertura, la retroguardia dell'avanguardia, la sfida e la caduta
  del sergente, l'inganno di Nala.
- Il modo C e le politiche estreme con le regole della v3.
- Due eroi nello stesso settore, il settore senza eroe, il modo A.
- I tempi: tre o quattro minuti a round sono una stima, non una misura.
- Se è divertente: lo dice solo il tavolo.
