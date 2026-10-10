# Il collaudo delle mappe: lo strumento e il collaudatore

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- Lo strumento
- Le direttive nella griglia
- Il collaudatore a freddo
- Il giro completo
<!-- /indice -->

Una mappa si dice fatta quando si gioca, non quando è bella. Il collaudo ha
due parti, e servono tutte e due
([ADR-0082](../../../plans/adr/ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md),
piano [COLLAUDO-MAPPE](../../../plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md)):

- **lo strumento**, `scripts/collaudo_mappe.py`, conta ciò che si conta: celle
  raggiungibili, porte nel muro, scale con la loro gemella;
- **il collaudatore**, un agente a freddo, giudica ciò che si giudica: se le
  posizioni dicono quello che dice la scena, se il giocatore capisce la mappa
  senza il DM, se una mappa generata ha seguito il suo giro.

Il confine fra i due è quello di ADR-0067: il codice per ciò che ha una
risposta sola, l'LLM per il resto. Il collaudatore non corregge: segnala, e
corregge chi ha disegnato, col DM.

## Lo strumento

```bash
python3 scripts/collaudo_mappe.py FILE.md            # una mappa o un atlante
python3 scripts/collaudo_mappe.py                    # tutto il corpus
python3 scripts/collaudo_mappe.py FILE.md --strict   # esce 1 se resta un errore
python3 scripts/collaudo_mappe.py --json OUT.json    # per un altro programma
```

Legge la griglia con il parser del renderer e la funzione di ogni simbolo da
`scripts/legend.json`. Ha bisogno di `tcod` e `numpy`, che stanno in
`requirements-dev.txt` ([ADR-0084](../../../plans/adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md)):
senza, esce con 2 e dice come installarle. Le regole di movimento sono quelle dell'SRD, uguali in
3.5 e PF1e: diagonale 5-10-5, niente diagonale oltre l'angolo di un muro (sì
oltre una fossa o una creatura), una creatura Grande occupa 2×2 e un'Enorme 3×3.

| Codice | Classe | Cosa vuol dire |
|---|---|---|
| `simbolo/ignoto` | E | un simbolo né nella legenda universale né nella riga `LEGENDA` della mappa |
| `legenda/funzione-opposta` | E | la legenda locale ridefinisce un simbolo universale al contrario (il muro `⬛` usato come pavimento): **si cambia il simbolo, non la legenda** |
| `nord/mancante` | E | una mappa tattica senza `@north` |
| `posa/nel-muro` | E | una porta, una grata, una finestra fuori da un muro, o murata da due lati |
| `posa/fra-livelli` | E | una scala o una botola senza la sua gemella, o con una gemella nello stesso verso |
| `posa/solo-master` | E | una porta segreta nella versione per i giocatori |
| `raggiungibile/unita` · `raggiungibile/obiettivo` | E | nemici o obiettivi in una zona che i PG non raggiungono |
| `zone/separate` | A | zone percorribili non collegate: un piano superiore lo giustifica, una svista no |
| `ingombro/grande` | A | la creatura dichiarata con `@taglia` non arriva ai PG col suo ingombro |
| `posa/sul-pavimento` | A | un mobile che chiude l'unico varco |
| `posa/recinto` | A | una cella di sbarre senza porta né grata |
| `tipo/mancante` | A | la mappa non dichiara `@tipo`: si collauda come tattica |
| `tipo/illeggibile` | E | un tipo o un ambiente fuori elenco (`dmcore/legenda.py`); i controlli tattici restano accesi |
| `posa/verso-illeggibile` | E | una direttiva `@verso` che non si legge, o che punta a una cella senza chiusura |
| `posa/asse-ambiguo` | A | una chiusura con muri e passaggi su tutti e due gli assi: si disegna est-ovest finché il DM non scrive `@verso` |
| `posa/verso-contro-muri` | A | `@verso` dice un asse, i muri intorno l'altro: vince la direttiva, ma forse è un errore di battitura |
| `m1/copertura` · `m2/vuoto` · `m4/esposizione` | A | poche coperture, troppo campo aperto, troppo visibile da ovunque (M4 esatta con `tcod`, su tutte le celle; soglie euristiche, non calibrate) |

Gli **errori** (E) pesano nella *distanza dalla giocabilità*, la somma che il
rapporto stampa per ogni mappa; una mappa nuova esce a zero. Gli **avvisi** (A)
non bloccano mai: un ponte stretto sul vuoto viola M1 e M2 di proposito.

## Le direttive nella griglia

Righe che iniziano con `@`, dentro il blocco, dopo le righe della griglia. Il
renderer le ignora, quindi l'SVG non cambia.

```
@north N                              il nord (obbligatorio nelle tattiche)
@tipo tattica caverna                 tipo: tattica, strategica o schema;
                                      ambiente: interni, caverna, esterno o abitato
@collega B05 ; Mappe/ATLANTE.md#3 D12 la scala in B05 porta a D12 della mappa 3
@collega C15 ; fuori mappa ; <motivo> il livello collegato non ha una griglia
@taglia J07 ; Grande                  la creatura in J07 non è Media
@vista giocatori                      questa è la versione per i giocatori
@verso B05 ; NS                       la porta in B05 sta in un muro nord-sud
@deroga zone/separate ; il soppalco si raggiunge solo in volo, ed è voluto
```

**La gemella in un contratto JSON** sta nel campo `collega` della struttura
(`{"type": "🔽", "at": [25, 19], "collega": "M7-E-gallerie-372.md AA02"}`),
e il compilatore la scrive come `@collega`: la griglia si rigenera, quindi la
direttiva scritta a mano andrebbe persa. La cella si confronta per posizione,
`B2` e `B02` sono la stessa.

**L'asse delle chiusure** non si scrive: lo danno i quattro vicini
([ADR-0083](../../../plans/adr/ADR-0083-l-asse-delle-chiusure-si-ricava-dai-vicini.md)).
Muri (o il bordo, o un'altra chiusura) a ovest e a est, e un passaggio a nord o
a sud, vogliono una chiusura in un muro est-ovest, disegnata com'è; il caso
ruotato vuole un muro nord-sud, e il renderer gira il glifo di 90°. L'export
UVTT mette il portale lungo lo stesso muro. `@verso` serve solo dove il
collaudo dice `posa/asse-ambiguo`. Il rapporto JSON conta gli assi di ogni
mappa nel campo `chiusure`.

Una deroga senza un motivo vero (almeno 15 caratteri) vale come assente. Una
vista strategica o uno schema non ricevono i controlli tattici.

## Il collaudatore a freddo

Un agente che **non ha disegnato la mappa** e **non vede il piano né la
conversazione**. Riceve:

1. il master con la griglia (o l'atlante);
2. il testo della scena che la usa, nel suo master d'arco;
3. il rapporto di `collaudo_mappe.py` su quel file;
4. il PNG della mappa (`export_map_png.py`), e la versione per i giocatori se
   c'è.

Lavora **in sola lettura**: non corregge la mappa né il testo, li giudica. Il
prompt nomina i quattro materiali con il percorso, e per il testo della scena
le righe esatte; così il collaudatore non cerca da sé e non legge altro.

### La rubrica, in tre viste

**Vista del DM**

- Lo strumento è stato eseguito? Gli errori sono a zero, o ognuno ha una
  deroga con un motivo che regge?
- Le posizioni della griglia sono quelle del testo della scena (stesse celle,
  stesse creature, stesso numero)?
- Si capisce chi entra da dove, e in quanti round arriva al contatto?
- Ogni scala e ogni botola porta da qualche parte, e la gemella è nel verso
  giusto?

**Vista del giocatore**

- La versione per i giocatori non mostra porte segrete né trappole (D9).
- Il nord è dichiarato, e le annotazioni dicono «parete nord» sapendo dov'è.
- Ogni simbolo si capisce senza la legenda locale, e nessuno è fuori legenda.

**Il canone**

- Un elemento marcato `[PROPOSTA]` contraddice il canone del master o di
  `state.md`?
- C'è un'invenzione presentata come canone senza marca (una creatura, una
  posizione, un tempo d'arrivo che il testo della scena non dice)?

**Gli algoritmi**, per una mappa generata

- Il seme è scritto, la bozza è passata dal collaudo a distanza zero, e ogni
  correzione proposta è stata applicata o rifiutata per scritto.
- Per una mappa disegnata a mano questa vista giudica una cosa sola: se il
  motivo di ogni deroga regge.

### I codici

| Codice | La domanda |
|---|---|
| `M-STRUMENTO` | Resta un errore dello strumento senza deroga, o una deroga senza motivo? |
| `M-POSIZIONI` | Una posizione della griglia contraddice il testo della scena? |
| `M-ACCESSI` | Non si capisce da dove entrano i nemici o i PG, o in quanti round si toccano? |
| `M-LIVELLI` | Un passaggio fra livelli non porta dove il testo dice? |
| `M-SEGRETO` | La versione per i giocatori mostra qualcosa che non devono vedere? |
| `M-LETTURA` | Un simbolo non si capisce senza spiegazione, o due si confondono? |
| `M-GENERATA` | Una mappa generata non dichiara seme, collaudo o correzioni? |

### L'uscita

```
| # | Mappa | Cella | Codice | Cosa non va | Gravità | Prova |
```

Al più 25 righe, dalla più grave, senza preambolo. La **prova** cita alla
lettera, in breve, sia la griglia (la cella o la direttiva) sia il testo della
scena: un rilievo senza le due citazioni non si può verificare.

La gravità è quella delle letture a freddo: 🔴 il tavolo si ferma, 🟠 il DM
deve inventare, 🟡 si gioca ma si capisce male. Poi una riga **«Verificato
senza rilievi:»** con ciò che è stato controllato e regge, così un silenzio
non si confonde con un controllo saltato. In coda, **cosa il collaudo non ha
potuto verificare**: il divertimento, i tempi reali al tavolo, le scene sociali
sulla mappa.

> Questi dettagli (sola lettura, il canone, le due citazioni, le 25 righe, la
> riga dei verificati) stavano nel prompt dell'unica esecuzione del ruolo, il
> 2026-10-08 nella #226, e non qui. Quell'esecuzione fu interrotta quando la
> bozza D28 fu ritirata: il ruolo **non ha ancora prodotto un rapporto vero**.

## Il giro completo

1. Chi disegna scrive la griglia con la legenda universale e le direttive.
2. `collaudo_mappe.py` sul file, fino a zero errori o deroghe motivate.
3. `render_map_svg.py`, poi il PNG, e la verifica a vista (STEP 5 di
   `audit-mappe-workflow.md`).
4. Il collaudatore a freddo, in un subagente, con i quattro materiali.
5. Le correzioni di chi ha disegnato; di nuovo i passi 2 e 3.
6. Il DM, che decide le deroghe e le posizioni dubbie.
