# ADR-0075 — Il ciclo del master vale per ogni piano

- **Stato**: accettata
- **Data**: 2026-09-27
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, prima di A3 di PIANO-MASTER-DEF: *«l'arco 07 è
  davvero completo anche con le nuove regole? ci hai fatto una passata anche
  con developer e playtester? […] tutti i piani da fare devono tenere conto di
  queste cose, sia quelli presenti in questo piano sia gli altri, se implicano
  una riscrittura o applicazione di stile»*
- **Rapporti**: raccoglie in una sequenza sola ADR-0073 (il contratto «In
  scena»), ADR-0074 (il master come componenti), le domande del developer
  (`sviluppo-degli-incontri.md`, da RICERCA-MANUALE-DEL-MASTER) e il collaudo a
  freddo di `rumblingstone-playtest`

## Contesto

Fra il 25 e il 27 settembre il repo ha preso quattro regole nuove sul master:
il contratto «In scena», i componenti con l'apparato generato, le domande del
developer, la lettura a freddo con il quiz. Ognuna è arrivata col suo ADR, il
suo strumento e il suo cancello, e ognuna è stata applicata a **un solo
master**, `ARC07-DEF-4`.

La domanda del DM era se questo bastasse. Misurato il 2026-09-27:

| Master di ARC-07 | Scene `### SCENA` | Contratto | Apparato | Box > 12 righe | Lettura a freddo |
|---|---:|---|---|---:|---|
| DEF-1 | 0 | no | no | 6 | no |
| DEF-2 | 0 | no | no | 1 | no |
| DEF-3 | 0 | no | no | 0 | no |
| DEF-4 | 13 | sì | sì | 0 | sì, con quiz |
| DEF-5 | 0 | no | no | 1 | no |

I cancelli in CI sono verdi su tutti e cinque, e non per la stessa ragione. Su
DEF-1, 2, 3 e 5 il contratto è spento da un profilo dichiarato in
`plans/copertura-scene.json`, con la ragione scritta (lotto F4 di
PIANO-LETTORE). Questa è onestà. La seconda ragione no: `copertura_scene` e la
parte per scene di `domande_developer` riconoscono una scena **solo** dal
titolo `### SCENA`. Un master di prova senza quel titolo, con un PNG che parla
senza scheda e nessun box, ha avuto **zero rilievi**. Il cancello non l'aveva
visto.

E i piani aperti che riscrivono contenuto (MESTIERE-BANCHI, MASTER-DEF,
INDAGINE, MARCATURA, DRAPPO) non nominavano nessuna delle quattro regole: erano
stati scritti prima, o le citavano una alla volta.

## La decisione

1. **Una sequenza sola.** `rumblingstone-module-standard` porta il **ciclo
   completo** in sette passi: scene riconoscibili, contratto, componenti,
   developer, box al metro, lettore e playtester a freddo, quiz. Un master è DEF
   quando li ha fatti tutti; con i soli cancelli è alfa. Vale per ogni arco
   diviso in DEF e per ogni stand-alone (ADR-0017). Il developer e il
   playtester sono obbligatori: un passo si salta solo con una decisione del DM
   scritta nel piano. Il DM, lo stesso giorno: *«nelle skill e l'ADR ci va come
   giro obbligatorio la parte del developer e del playtester, sia per tutti gli
   archi e gli stand-alone che vengono divisi in DEF»*.
2. **I piani la citano, non la copiano.** Un lotto che scrive, riscrive o
   rifinisce nello stile un master, un modulo o uno stand-alone dichiara nella
   colonna «qualità» i passi del ciclo, per numero, e quali salta e perché. La
   regola sta in `rumblingstone-plans`, dove la legge chi apre o aggiorna un
   piano.
3. **ARC-07 non è completo, e lo si dice.** Il lotto F4 di PIANO-LETTORE si
   allarga dal solo contratto al ciclo intero, e va **prima** di A3 di
   PIANO-MASTER-DEF: ARC-08 comincia dove finisce DEF-5, che è anche il
   prossimo master al tavolo.
4. **Il buco del cancello diventa un lotto**, non una nota: un master
   `ARC*-DEF-*` con zero scene riconosciute deve essere un rilievo (F6 di
   PIANO-LETTORE).

## La prova contro il tavolo

Il DM ha chiesto se il ciclo fa venire fuori i problemi che il tavolo ha già
trovato. Il banco è `ARC07-DEF-4` al commit `ddd683c`, il testo giocato il
2026-09-25, e le cose che il DM ha dovuto inventare (ADR-0073).

| Problema al tavolo | Il testo lo nominava? | Cancelli, passi 1-2 | Letture a freddo, passo 6 (calibrazione in PIANO-LETTORE §2) |
|---|---|---|---|
| i quartieri ospiti | sì, Scena 5, senza box | ✅ C1 «Scena 5 senza box», e il contratto (*Dove*) | — |
| le gallerie sotto la fucina | sì, fra parentesi | ✅ contratto (*Dove*) | ✅ lettore #18 |
| il capitano delle mura | sì, nella tabella delle scene | ✅ contratto (*Chi*) | ✅ lettore #40 |
| le guardie della tenda, senza volto | sì, con i soli numeri | ✅ contratto (*Chi* chiede scheda o Comparse) | ◐ lettore #33, #55 |
| la cappella con la sua chierica | **no** | — | ◐ playtester #14: «mancano prezzi, venditori» |
| l'alchimista | **no** | — | ◐ playtester #14, generico |
| l'araldo | **no** | — | ◐ lettore #33, che parla di un'altra guardia: legame debole |

Sulla versione giocata i cancelli dei passi 1-2 danno **16 rilievi** e
coprono i problemi che il testo nominava. Per quelli che non nominava
le letture danno solo segnali generici: nessun rilievo dice «manca una
cappella», «manca un alchimista» o «manca un araldo». Un DM che avesse letto
quei rapporti avrebbe corretto il mercato della Scena 5, non aggiunto quelle
tre persone. È il limite di ADR-0073: *uno script non vede quello che il testo
non nomina*.

I tre hanno una cosa in comune: sono i ruoli che un luogo abitato ha sempre,
e che i giocatori vanno a cercare quando hanno tempo libero. Da qui la
correzione, con lo stesso principio del contratto (non si misura un'assenza,
ma si chiede di fare l'elenco):

- il passo 2 chiede, nelle scene di tempo libero in un luogo abitato, una
  tabella **Chi si trova qui** con sei righe fisse (comando, culto, rimedi,
  bottega, messaggi, guardia) e «nessuno» dove manca;
- il playtester ha un codice nuovo, `P-ABITATO`, che fa quella domanda.
- al tavolo resta la rete sotto, il kit anti-improvvisazione di `campaign/` (un nome, un prezzo, una faccia): serve quando la tabella non è stata scritta, non al suo posto.

⚠️ La correzione è costruita sui tre casi che deve trovare, quindi su DEF-4 li
trova per forza. La prova vera è un modulo che non l'ha generata: **DEF-5**, il
ritorno a Hammerfist, che è di nuovo una fortezza abitata e il primo master di
F4.

**Il ciclo introduceva un problema, corretto nello stesso giorno.** Il passo 1
chiedeva `### SCENA` a tutti, ma gli stand-alone e DEF-5 hanno una struttura
loro (`## §N`), già dichiarata nei profili di `copertura-scene.json`. Il passo
vale ora così: `### SCENA` nei master `ARC*-DEF-*`, il titolo dichiarato nel
profilo per chi ha una struttura sua.

## Le conseguenze

- Una regola nuova sul master, da oggi, entra nel ciclo o non è arrivata: il
  ciclo è l'unico posto che i piani leggono.
- Quello che si paga: ogni lotto di riscrittura costa di più. Una sidebar
  aggiunta a DEF-1 passa per contratto, componenti e lettura a freddo, e DEF-1
  non ha ancora le scene nel formato che i cancelli vedono. La prima volta si
  paga la conversione.
- I passi 6 e 7 restano fuori dalla CI: sono letture di un agente, e un
  cancello su un giudizio sarebbe rumore (ADR-0073). Li tiene in vita il piano,
  che non chiude il lotto senza di loro.
- Il tetto delle 12 righe resta una misura e non un cancello, finché i master
  esistenti non ci stanno: oggi sarebbe rosso su tre master di ARC-07 su
  cinque, e un cancello sempre rosso viene spento. È la lezione di
  `validate_modules.py` sui punti 15-16.

## Aggiornamento del 2026-10-01 — il passo 7

Il DM, D1 di [PIANO-AGENT-SKILLS-ESTERNE](../PIANO-AGENT-SKILLS-ESTERNE.md):
il passo 7 è il **ricordo dal diario** della lettura a scene
(`ricordo_lettura.py`, ADR-0076), che non chiede una chiave approvata. Il quiz a
due agenti resta dove una chiave approvata esiste già (oggi DEF-4). Il resto
della decisione non cambia: i passi 6 e 7 li fa un agente, non sono cancelli,
e un master che non li ha fatti è alfa.
