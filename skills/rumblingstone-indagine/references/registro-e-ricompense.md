# Il registro dell'indagine — Acume, Perizia, Metodo

Decisione di riferimento: [ADR-0022](../../../plans/adr/ADR-0022-competenza-guadagnata-sul-campo.md).
Qui c'è l'uso pratico. Il principio in una riga:

> **Chi spreme le meningi porta a casa qualcosa. Ma la moneta che premia
> *subito* e la moneta che resta sulla scheda non sono la stessa moneta.**

---

## 1. Acume — la moneta della serata

**Si guadagna** nel momento in cui succede la cosa che vogliamo premiare. Il
DM lo assegna a voce, sul posto, senza contabilità:

| Cosa fa il giocatore | Acume |
|---|---|
| Apre un nodo con una **porta grezza** (nessun grado nell'abilità ovvia) | **1** |
| **Collega due indizi** a voce, prima che il DM lo dica | **1** |
| Trova una **terza via** al nodo che non era scritta nel modulo, e regge | **1** |
| Sbaglia una deduzione, ma **argomentandola** su fatti veri | **1** |
| Tira bene | **0** — il dado non è merito |

Quell'ultima riga è metà del sistema. L'Acume non premia la scheda: premia
**il giocatore che ha parlato**.

**Si spende** subito, dal giocatore, dicendolo:

| Costo | Effetto |
|---|---|
| 1 | **+2** a una prova investigativa (grezza o d'abilità), dichiarato prima del tiro |
| 1 | **Una domanda sì/no** al DM su ciò che il PG può percepire ora. Il DM risponde onestamente |
| 2 | **Fatto → Lettura senza tirare**: il PG dice cosa significa e ha ragione |
| 2 | **Lettura del combattimento** (§5) |

**Si azzera a fine caso.** Non si accumula, non si porta alla sessione dopo,
non si scambia. Se un giocatore finisce il caso con 4 Acume in mano, il DM ha
sbagliato a non spingerlo a spenderli: ricordaglielo a metà.

## 2. Perizia — la moneta che resta

A fine caso, **ogni PG deposita una perizia** in un'abilità che ha
*davvero usato nella finzione*. Il DM ha diritto di veto su una perizia in
un'abilità che il PG non ha toccato: il criterio è la scena, non il
desiderio.

Chi ha lavorato di più ne deposita di più:

| Contributo nel caso | Perizie depositate |
|---|---|
| Ha partecipato | **1** |
| Ha aperto tre o più nodi, o ha detto la deduzione che ha svoltato il caso | **2** |
| Il caso si è chiuso grazie a una cosa che ha fatto lui, e il tavolo lo sa | **3** |

**Tre perizie nella stessa abilità = 1 grado vero.** Permanente. E quel grado
conta come **abilità di classe** per quel PG in quella sola abilità: l'ha
imparata sul campo.

**I tre paletti** (dall'ADR — non sono opzionali):

1. **1 grado da questo sistema per PG per livello.** Non c'è arretrato: se
   un livello passa senza che nessuna abilità arrivi a tre perizie, quel
   grado è perso.
2. **Vale il massimale SRD** (grado max = livello + 3 per abilità di classe).
   Un grado che sfonderebbe il massimale non si assegna: le perizie restano
   in banca fino al livello dopo.
3. **Le abilità solo per addestrati si aprono così**: Sapienza, Decifrare
   Scritture, Disattivare Congegni, Artigianato Magico. È il caso d'uso
   migliore del sistema: il primo grado è quello che *permette di provarci*,
   e apre una porta che prima era murata.

### Perché il tetto, in una riga da dire ai giocatori
> «Dopo cinque casi il tuo guerriero avrà due gradi in Cercare. Abbastanza
> per provarci sempre. Mai abbastanza per non aver bisogno di un ladro.»

## 3. Il Metodo — la moneta del gruppo

Questa è la risposta diretta a *«se nel gruppo non c'è un ladro, sopperire
come gruppo»*. Ogni caso chiuso fa guadagnare al **gruppo** un metodo, scelto
insieme fra quelli disponibili. Ogni metodo si usa **una volta per caso** ed
è dichiarato ad alta voce.

| Metodo | Effetto | Si sblocca |
|---|---|---|
| **Il Cerchio** | Il gruppo si ferma e mette in comune. Ogni PG dichiara un Fatto raccolto; un PG tira, con +2 per ogni Fatto portato (max +6). Successo: una Lettura che nessuno aveva | 1° caso chiuso |
| **Le Quattro Teste** | Il gruppo divide una scena in quattro: ognuno prende una porta diversa sullo stesso nodo. Tutte le prove si tirano; **basta un successo** e ogni successo aggiuntivo dà un pezzo in più | 2° caso |
| **La Mano Prestata** | Una volta per caso, un PG usa il **modificatore di caratteristica di un compagno presente** al posto del proprio, se il compagno descrive come glielo insegna | 3° caso |
| **Il Filo** | A inizio sessione il gruppo dichiara una domanda («chi ha pagato il traghettatore?»). Ogni Fatto trovato che la riguarda vale **1 Acume al gruppo**, spendibile da chiunque | 4° caso |
| **Il Ritorno** | Il gruppo può tornare su una scena già chiusa e **riaprire un nodo** con una porta nuova, alla luce di ciò che sa adesso. Senza tempo di gioco: è memoria, non viaggio | 5° caso |

I metodi **non stanno su nessuna scheda**: sopravvivono ai cambi di
composizione e non gonfiano nessuno. Se il gruppo perde un PG, il Metodo
resta.

## 4. Il registro — dove si scrive, e perché non si può non scriverlo

In tre sessioni nessuno ricorda chi ha depositato cosa. Il registro vive nel
branch di gruppo accanto allo XP ledger ([ADR-0007](../../../plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md)),
in fondo al file del caso. Formato:

```markdown
## Registro dell'indagine — «Il registro del molo»  (chiuso 12 Eleint)

| PG | Perizie depositate | Abilità | Banca dopo | Grado assegnato? |
|---|---|---|---|---|
| Thorik  | 2 | Intuizione | 2/3 | — |
| Tordek  | 3 | Cercare    | 3/3 → **azzerata** | ✅ 1 grado (di classe, sul campo) — tetto del livello 13 **usato** |
| Hella   | 1 | Raccogliere Informazioni | 1/3 | — |
| Artemis | 2 | Sapienza (storia) | 2/3 | — |

**Metodo guadagnato**: Le Quattro Teste (2° caso chiuso).
**Acume speso**: 7 su 9 assegnati. Due bruciati alla fine — spingere di più a metà.
```

L'ultima riga è per il DM, non per i giocatori: **l'Acume non speso è un
difetto di regia**, e va guardato come si guarda un punto morto in un
playtest (`rumblingstone-playtest`).

## 5. Regola opzionale — la lettura del combattimento

Per chi vuole la parte cinematografica: il colpo previsto prima di essere
tirato. **Costa 2 Acume**, si dichiara *prima dell'iniziativa*, e il
giocatore **descrive** cosa il PG sta leggendo nell'avversario. Poi sceglie
uno solo:

| Scelta | Effetto meccanico |
|---|---|
| «So dove è scoperto» | **+2 al primo tiro per colpire** del PG in questo scontro |
| «So come si muove» | il PG **agisce nel round di sorpresa** anche se non l'avrebbe potuto |
| «So quanto regge» | il DM dichiara la **fascia** di CA dell'avversario (bassa / media / alta) e se ha RD |

Tre paletti: **una sola lettura per PG per scontro**, non si accumula con
altre letture, e **non funziona su un avversario mai visto prima** — si legge
qualcuno che si è già osservato, anche solo per un momento. È deduzione, non
divinazione.

Se il tavolo non la usa dopo tre scontri, toglila: è un'opzione, e
un'opzione che nessuno prende è peso morto sul foglio delle regole.
