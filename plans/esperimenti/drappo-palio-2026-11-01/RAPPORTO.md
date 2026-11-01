# Il Drappo di Tarsilia e il Palio di Channathgate: quanto sono lo stesso modulo

**Data**: 2026-11-01 · **Piano**: [PIANO-TRAVASO-DRAPPO-CAMPAGNA](../../PIANO-TRAVASO-DRAPPO-CAMPAGNA.md) §3-bis, lotto C1
**Richiesta del DM** (2026-11-01): *«se è lo stesso modulo il drappo che è derivato dovrà
mettere l'origine, mentre se è vero il contrario le indicazioni devono andare nel senso
opposto; se sono diversi bisogna capire misurando quando sono identici e poi decidere,
permettendo la giocabilità sia nella campagna che come stand alone»*.

Le misure si rigenerano con:

```bash
python3 scripts/misura_derivazione.py \
  plans/esperimenti/drappo-palio-2026-11-01/corrispondenze.json \
  --json plans/esperimenti/drappo-palio-2026-11-01/MISURA.json \
  --md   plans/esperimenti/drappo-palio-2026-11-01/MISURA.md
```

`MISURA.md` è l'uscita completa, con tutti i 74 concetti uno per uno. Qui sotto ci sono
le conclusioni.

## 1. Chi deriva da chi

Il Drappo deriva dal Palio. Nessuna delle fonti dice il contrario:

| Fonte | Cosa dice |
|---|---|
| Storia git | il Palio nasce il **2026-07-01** (`77f03d5b`, *«Palio di Channathgate — standalone adventure + campaign integration»*), il Drappo il **2026-08-14** (`db4e84d7`, *«il sistema del Palio come modulo autonomo (Golarion, PF1e)»*) |
| Piano del Drappo | richiesta-fonte del DM del 2026-08-14: *«dato il palio di Channathgate possiamo fare una variante…»*; §1: «si riusa il **sistema** del Palio», «NON si tocca l'arco P2D» |
| Hub del Drappo §10 | «il sottosistema della corsa […] sviluppato per l'arco *Il Palio di Channathgate* e qui riscritto per PF1e» |
| `IP-E-LICENZE.md` del Drappo | la tabella del lessico Channathgate → Tarsilia (Tratta → Sorte, Mossa → Stacco, nerbo → scudiscio, Gonfaloniere → Sovrintendente, drappellone → Drappo) |

C'è un solo flusso all'indietro, e precede il Drappo: la serie di stemmi Golarion entra
nella cartella del Palio il 2026-08-10 (PR #100), quattro giorni prima del Drappo, e il
Drappo la cita senza copiarla. Nessun concetto del Drappo è poi rientrato nel Palio:
cercando con `git log -S` i termini che i due hanno in comune (Onore del Fantino, Morale
del Rione, Dirigenza), la prima comparsa è sempre nel Palio.

Il Palio a sua volta si dichiara **a doppio uso** fin dalla prima riga di
`…-CHANNATHGATE-AVVENTURA.md`: avventura autoconclusiva in 3.5/PF1e ad APL 12-13, più
il file gemello `…-INTEGRAZIONE.md` per la campagna. I richiami alla campagna sono
concentrati lì (133 su 336 contati nei quindici file); i file delle tre giornate ne hanno
6, 18 e 12, quasi tutti nei riquadri marcati «aggancio campagna».

## 2. Quanto sono identici

Due assi, che danno risposte opposte.

**Testo: niente in comune.** Su 40.036 sequenze di sei parole del Drappo, 7 compaiono
anche nel Palio (0,02%), e sono frasi come «alba la benedizione del cavallo» o «3
successi prima di 3 fallimenti». Nessuna delle 2.234 frasi del Drappo è copiata dal
Palio, nemmeno in parte (soglia: 60% dei 4-grammi). Il Drappo è stato scritto da capo.
Dal conto sono esclusi `IP-E-LICENZE.md` e i due `PROMPT-*`, che citano il Palio
apposta: con `IP-E-LICENZE.md` dentro, quel solo file sale al 2,4%, per la tabella del
lessico e i crediti delle icone.

**Impianto: lo stesso scheletro.** Sui 74 concetti dichiarati in `corrispondenze.json`:

| Dimensione | Condivisi | di cui con lo stesso nome | Solo Palio | Solo Drappo | Quota condivisa |
|---|---|---|---|---|---|
| Contrade | 11 | 10 | 1 (i motti) | 0 | 92% |
| PNG (per ruolo) | 8 | 2 | 3 | 1 | 67% |
| Scene | 15 | 8 | 3 | 5 | 65% |
| Regole della corsa | 7 | 5 | 6 | 0 | 54% |
| Struttura | 5 | 5 | 4 | 5 | 36% |
| **Totale** | **46** | **30** | **17** | **11** | **62%** |

In parole: le stesse otto contrade con gli stessi nomi (Unicorno diventa Leocorno), le
divinità tradotte una a una da Faerûn a Golarion, le tre giornate con la stessa sequenza
di scene (emissari, assegnazione dei cavalli, Partiti, sbandierata, sfida dei canti,
cena, assalto notturno alla stalla, benedizione, corteo, partenza, corsa in tre giri,
decreto), gli stessi due contatori 0-10 (*Morale del Rione* e *Onore del Fantino*, già
nel Master del Palio §3.3), la frusta in corsa, il cavallo scosso che può vincere,
l'inseguimento a lunghezze. I PNG sono nuovi di nome ma coprono gli stessi ruoli: chi
governa la corsa, i capitani, la mente del sabotaggio che sta nel Bruco, il denaro
dell'Oca, l'Istrice dei poveri.

⚠️ Le corrispondenze sono una lettura mia, non una misura neutra. Lo script conta quello
che il file dichiara; un concetto mal scelto sposta le quote. Per questo il file è a
parte e si può correggere.

## 3. Dove divergono

| | Palio di Channathgate | Drappo di Tarsilia |
|---|---|---|
| Sistema e livello | 3.5 (con conversione PF1e), PG di 12°-13° | PF1e, sei PG di 3° |
| Chi sono i PG | i PG della campagna, che entrano nella Dirigenza di una contrada dopo le prove d'ammissione | sei pregenerati, gli uffici dell'Istrice |
| Posta | la Matrice del Mythal e la Meraviglia d'assedio per Rethmar | l'Istrice sparisce se non arriva fra i primi tre |
| Aggancio | March Clock, Consiglio di Rethmar, Sonjak, Collezionista, cavalcata di soccorso al Giorno 4 | nessuno: la città non sta in nessuna campagna |
| Solo qui | prove d'ammissione, rito del fazzoletto, Fantino della Nonna, Sospetto 0-5, Influenza nei Partiti, Fantino Cavaliere o Ladro, bomboloni e brenne, eventi di giro d10 | Peso di contrada, rissa alla fontana, tavola di fuori, uomo con la fascia grigia, salvataggio in tintoria, curva nord, apparato d'uso completo |
| Sabotaggio della stalla | drow di Sonjak, GS 11-12 | Sfregio e i bravacci, GS 5 |
| Motti | otto motti del Palio | otto motti nuovi, nessuno ripreso |
| Testo | — | riscritto da capo |

## 4. Un errore trovato misurando

L'hub del Drappo §10 dice: «Nomi, contrade, motti, PNG e trama di questo modulo sono
nuovi». Per le contrade non è vero: i nomi sono gli stessi otto, e lo dice lo stesso
modulo in `IP-E-LICENZE.md` §4 («i nomi delle contrade sono quelli reali»). Sono nuovi i
motti, le livree, le divinità e le persone. Nemmeno «trama nuova» regge del tutto: la
sequenza delle scene è quella del Palio. Corretto in questa PR, perché è il derivato che
dichiara male la propria origine.

## 5. Giocabilità

| Dove si gioca | Con cosa | Stato |
|---|---|---|
| Nella campagna, dopo Hammerfist | il Palio, `…-INTEGRAZIONE.md` compreso | già così |
| Stand alone ad alto livello, Reami | il Palio senza `…-INTEGRAZIONE.md` | dichiarato dal Palio stesso; non verificato al tavolo |
| Stand alone a basso livello, fuori dai Reami | il Drappo | collaudo alfa scritto, nessun tavolo vero |

Giocare il Drappo dentro la campagna non ha senso così com'è: livello 3 contro 13,
Golarion contro i Reami, e il Palio fa già quel lavoro. Un innesto vorrebbe dire
riscrivere il Drappo per diventare il Palio.

## 6. Decisione proposta (ADR breve)

**Contesto.** I due moduli condividono il sistema e lo scheletro (62% dei concetti) ma
non il testo (0 frasi). Il Drappo dichiara l'origine, con un errore sulle contrade; il
Palio non nomina mai il Drappo. Il piano del Drappo del 2026-08-14 vieta di toccare i
file dell'arco 09, per non far dipendere una copia dall'altra.

**Proposta.** Collegamento nei due sensi, senza unire nulla:
- il Drappo, che è il derivato, dichiara l'origine in modo esatto nell'hub §10, con la
  tabella delle divergenze e il rimando a questa misura (fatto in questa PR per la
  parte che corregge un errore);
- il Palio riceve una riga in testa a `…-CHANNATHGATE-AVVENTURA.md` che rimanda al
  Drappo come versione derivata per PF1e a basso livello. È l'unico tocco all'arco 09,
  e va contro la lettera della regola del 2026-08-14: per questo sta su una card;
- un test verifica che i due rimandi esistano, così il collegamento non si perde.

**Alternative scartate.** Fondere i due in un sistema della corsa comune: è la riscrittura
che il piano del Drappo vietava, e romperebbe un testo collaudato (regola del DM del
2026-10-31: si abbandona la decisione che porta una regressione misurabile). Lasciare
solo la dichiarazione nel Drappo: chi apre il Palio non saprebbe che esiste una versione
già pronta per un altro tavolo.

**Conseguenze.** Nessun testo giocato cambia. Se il Palio o il Drappo cambiano scene o
regole, si rilancia lo script e la tabella delle divergenze si aggiorna a mano dal suo
risultato.

**Da rivedere se** uno dei due viene riscritto in modo da cambiare lo scheletro, o se il
DM decide di bonificare i nomi delle contrade del Drappo (Lotto 4 del suo piano): a quel
punto la quota delle contrade scende e il rapporto va rifatto.
