# DEF-5 · Il ritorno a Hammerfist — correzioni del giro 2

Esiti: CORRETTO 11 · DECISIONE DM 9 · RESPINTO 1 · 🟡 lasciati 19

I CORRETTO sono 4 fra i 🟠 e 7 fra i 🟡. Delle 9 decisioni, 5 vengono dai rilievi e 4 dai `[INFERRED]` che il master aveva già. Il master corretto è `07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md`. Non ho toccato nessun box: `misura_craft --box` dà ancora 9 box, 0 sopra le 12 righe, 0 con parentesi, e 1 con più di un nome, che c'era già prima.

Gate: `validate_modules` 0 errori · `domande_developer --check` ✓ · `copertura_scene --check` ✓ · `componenti --check` ✓ · `validate_prosa` ✓. `test_storico.py` dà 1 fallimento su `ARC07-DEF-3-RESURREZIONE-HELLA.md`, una riga di storia rimasta fuori da `<!-- storico -->`. Quel file è di un altro correttore, e io non l'ho toccato.

## I rilievi 🔴 e 🟠

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| La CA di Re Thorek manca, e il «CA 19» si legge male (DEV#1, PT#2, DM#1); Dana prende uno o tutti i colpi (PT#3) | 🔴 | DECISIONE DM (D1), e la parte di dati CORRETTA | Ho preso dalla Guida DM dell'ARC-08 la CA 30 (contatto 13, colto alla sprovvista 29) e i 196 pf: la scheda del Bestiario li ha corretti il 2026-10-16, mentre il master diceva ancora 195. Li ho riportati in A.6 e nella Quick-Reference, con i conti SRD per l'esausto (CA 27) e per il re steso (+4 contro gli attacchi a distanza). Ho riscritto il «CA 19» del round 6 e delle tattiche in modo che si capisca che è quella degli hobgoblin. Resta da decidere come si risolvono le frecce: con i numeri SRD Dana non è mai in pericolo, e il canone del 2026-10-18 dice che lo è |
| Gli orchi scossi sono fuori dall'anello, ma caricano chi scende dall'altare (DEV#2, PT#1) | 🟠 | DECISIONE DM (D2) | Due righe del master si contraddicono, e l'unica con il tag di canone è la tattica (D77). Per farle andare d'accordo bisogna spostare gli orchi o cambiare la tattica, e la scelta spetta al DM |
| I novanta nani non hanno statistiche, e non si sa cosa voglia dire «travolge» (DEV#3) | 🟠 | CORRETTO | Ho aggiunto una frase alle tattiche dei nani. Travolto vuol dire fuori dallo scontro, senza tiri. Quello che i nani fanno agli hobgoblin è già contato in quanti ne passano: i cinque hanno passato tutte e tre le file, e i nani tengono il varco sugli altri quindici. Resta dentro D90 («i nani non si tirano») |
| Le radici di Hella: quante volte, con che azione, fino a dove (DEV#4, DM#14 🟡) | 🟠 | DECISIONE DM (D3) | La frequenza decide l'esito dello scontro, e il canone D77 non la dà |
| Il *muro di spine* non blocca un varco (DEV#5) | 🟠 | RESPINTO, con una riga aggiunta | Nell'SRD per attraversare un *muro di spine* serve un'azione di round completo e una prova di Forza oltre 20 per ogni 1,5 m; aprirsi un passaggio con le armi costa 10 minuti ogni 30 cm. Un sergente con Forza 14 non passa: il muro blocca. Ho aggiunto alla riga «chiudono la porta» che regge anche il *muro di spine*, e che Hella, druida di 12°, ha nella lista tutti e due i muri (SRD: *muro di pietra* Drd 6, *muro di spine* Drd 5) |
| Dati da cercare fuori dal master (DEV#6) | 🟠 | CORRETTO, e il resto RESPINTO | Ho aggiunto ad A.5 la CA, il contatto, il colto alla sprovvista e l'iniziativa di Dana, e ad A.6 la CA del re, tutti dalla Guida ARC-08. In A.2 ho scritto il comando del sergente per intero: il +1 non è compreso nei tiri, quindi +10 e +7. Le Ali d'Ombra sono a volontà con un'azione gratuita (scheda dell'Anello). Respinto il resto: l'*Aura di Comando* e lo *Scudo del Custode* sono già descritti per intero nella tabella dei gesti |
| Il portale di Dana non ha una meccanica (PT#4, DEV#14 🟡, DM#7 🟡) | 🟠 | DECISIONE DM (D4) | Dana ha speso tutto, e nessun incantesimo da chierico apre un portale: qui manca un pezzo di canone |
| La scadenza per murare il varco nel ramo «meno luminoso», e l'iniziativa di Dana (PT#5) | 🟠 | DECISIONE DM (D5), e l'iniziativa CORRETTA | L'iniziativa +1 di Dana ora è in A.5. Se nel ramo «meno luminoso» il varco si possa ancora murare cambia lo scontro che il DM ha voluto «vero» (D77) |
| Il criterio dei due rami usa etichette di DEF-4 che il master non spiega (DM#2) | 🟠 | CORRETTO | Sotto la tabella dei due rami ho scritto in tre frasi cosa vogliono dire FUGGITO, VINTO SPORCO e la Catena spezzata, con il rimando a `DEF-4` Scena 11 e §6 |
| La tavola dell'Affresco A8: cosa c'è dipinto, e se è al 60 o all'80% (DM#3) | 🟠 | CORRETTO | Ho preso il contenuto da `DEF-2` §4: i quattro, Hella compresa e viva, Hammerfist sullo sfondo, i festeggiamenti abbozzati. La tavola va data all'80%, perché `DEF-2` la fa salire dopo la resurrezione. Manca ancora l'immagine da stampare, che va con il 🟡 delle immagini (DM#17) |

## I 🟡 corretti con una riga

| Rilievo | Cosa ho fatto |
|---|---|
| DEV#13 · *muro di pietra* nello slot di dominio | Nella Guida ARC-08 il *muro di pietra* sta in uno slot normale del 5° (il dominio è *colpo infuocato*), quindi si converte. Ora lo dice anche il master |
| PT#9 · immuni o no alla paura | In A.2 ora c'è «immuni alla paura», con la fonte (la tabella delle ondate dell'Atlante dell'ARC-08) e la nota che l'SRD non lo dà. Vince la versione più forte |
| PT#10 · bottino degli hobgoblin | Ho tolto il rimando circolare: il bottino lo conta l'ARC-08 (B4), non questo master |
| PT#13 · Acrobazia per scendere dall'altare | Saltare o Acrobazia CD 15 (SRD), nella tabella delle CD e nel gesto di Tordek |
| DM#10 · la piattaforma est | Sulla mappa la piattaforma è in d-e13, con la stalagmite in c. L'ho corretta nei tre punti in cui compare |
| DM#11 (in parte) · «ramo probabile» | Ho cambiato l'etichetta in «l'altro ramo», perché il ramo del gruppo di oggi è l'altro. La riga «sotto 2 giorni» resta fra i lasciati |
| DM#13 · il +1 morale | È fuori dal +9 e dal +6 (BAB 5, For +2, Arma Focalizzata +1, perfetta +1): in fila si tira a +10 e a +7 |

## I 🟡 lasciati

Il preavviso senza l'ordine (DEV#7, PT#6, DM#8: va deciso un numero) · il *comando* «Fuggi» che dura un round, e la lingua (DEV#8, PT#7) · l'ordine di iniziativa dentro il round di sorpresa (DEV#9) · il passaggio all'arco nel ramo luminoso (DEV#10) · l'orda in fila sotto un'area (DEV#12) · il blocco «Se lo divinano» (DEV#15) · cosa fa crollare le stalattiti (DEV#16, PT#8) · chi c'è durante un'ora di sosta (PT#11) · quali pergamene di *ristorare* ha il gruppo (PT#12, DM#16: servono le schede dei PG) · la vista che non dice cosa serve da fuori (DM#4) · i grassetti di servizio nella vista (DM#5) · il tempo di preparazione (DM#6) · il preavviso gridato dall'altare (DM#9) · la riga «sotto 2 giorni» (DM#11) · il fast-play nel ramo «meno luminoso» (DM#12) · «chi vi ha mandato?» (DM#15) · le immagini e la tavola A8 da stampare (DM#17) · i poteri nuovi fuori dal file (DM#18) · le torri che cadono senza un segnale (DM#19).

## Decisioni per il DM

### D1 · Le frecce al re, e Dana che gliele prende

Con i numeri SRD che ora sono in A.6, il re da esausto ha CA 27, e 31 contro gli archi perché è steso. Un sergente con l'arco tira a +7, quindi colpisce solo col 20. Senza critico un 1d8 non porta sotto 0 un re a 8 pf, e dai piedi di un altare alto 3 m chi tira non vede nemmeno un corpo steso. Così Dana non è mai in pericolo, mentre il canone del 2026-10-18 dice che nel ramo «meno luminoso» lo è, e che la abbattono «cinque o sei frecce».

**Decidi contro quale CA tirano gli hobgoblin quando Dana copre il re.**

- **SRD puro** · tirano al re, a CA 31, e Dana prende solo il colpo che lo ucciderebbe: non cade quasi mai, e il ramo «meno luminoso» perde il suo pericolo.
- **Dana bersaglio** · ogni freccia diretta al re va a Dana, contro la sua CA 29: con +7 colpisce solo il 20, quindi cambia poco rispetto alla prima.
- **Scudo di carne** · Dana si getta sul re e non si difende, quindi le frecce vanno contro la sua CA di contatto, 14 (non SRD): cinque archi le tolgono circa 15 pf a round, e cade in due round.

**Raccomandata: Scudo di carne.** È l'unica che rende veri i numeri che il DM ha già messo a canone («cinque o sei frecce»), ed è la più terrificante. Dana in ginocchio si vede anche dal basso, il re steso no. Diverge dall'SRD: in 3.5 non c'è una regola per chi si offre ai colpi, e il talento *In Harm's Way* del PF1e (Advanced Player's Guide) la renderebbe ancora più sicura, perché la freccia deve prima colpire il re.

### D2 · Dove sono i due orchi scossi

Sulla mappa gli orchi sono alla porta, nelle righe 02-03, e l'anello dei nani è nella riga 04, fra loro e l'altare. La tattica, che porta il tag D77, dice che caricano il primo PG che scende dall'altare. La regia del round 1 dice invece che i nani li spingono verso le porte e li circondano.

**Scegli se i due orchi rimasti sono dentro o fuori dall'anello.**

- **Già dentro** · sono i primi che hanno passato l'anello prima dell'aura, e stanno nelle righe 06-08: caricano nel round 1 chi scende. Bisogna spostare due segnalini sulla mappa.
- **Restano fuori** · caricano solo un PG che passa l'anello, e il gesto di Tordek diventa «va al varco». La scena comincia senza scontro.
- **L'anello si apre** · i nani li lasciano passare verso il PG che scende, e gli orchi arrivano al round 2.

**Raccomandata: Già dentro.** Tiene alla lettera il canone D77 e il gesto di Tordek, e la scena si apre con uno scontro. Basta spostare due segnalini, e la frase «i nani li incalzano verso le porte» resta vera per tutti quelli che scappano.

### D3 · Le radici di Hella

Il canone D77 dice che fanno come *intralciare*, ma su 6 m di raggio e per un round. Non dice quante volte si possono usare, con che azione, né fino a dove arrivano. La porta è a 36 m dall'altare.

**Fissa quante volte Hella usa le radici, e fino a dove.**

- **Una volta** · una volta per scena, con un'azione standard, alla gittata di *intralciare* (lunga, SRD: 264 m al 12° livello di incantatore).
- **A ogni round** · con un'azione standard per round: sulla fila che entra dalla porta (Riflessi +2 contro CD 15) blocca quasi tutti gli hobgoblin.
- **Solo all'arrivo** · solo nel round di sorpresa, come parte dell'apparizione.

**Raccomandata: Una volta.** Hella resta forte, e se ha preparato il suo *intralciare* vero, che è molto più largo, può lanciare anche quello. A ogni round toglierebbe agli hobgoblin la minaccia che il DM ha voluto.

### D4 · Il portale di Dana

Dana ha speso tutto tranne un *muro di pietra*, eppure apre il portale con una preghiera di un round. Se cade, lo aprono le Cantitrici, che hanno speso tutto anche loro. Nessun incantesimo da chierico apre un portale, e il master non dice quanto resta aperto né chi ci passa.

**Stabilisci da dove viene il potere del portale.**

- **Il luogo** · lo apre l'altare consacrato a Moradin, per chiunque del suo clero preghi lì per un round, e non costa uno slot. Resta aperto 1 minuto, e passano i PG, i Treant e Durik.
- **Dono di classe** · è un potere della Cantante Divina, 1 al giorno. Le Cantitrici però non lo sono, e allora il ripiego del §6 cade.
- **Costa il muro** · aprirlo spende l'ultimo *muro di pietra*: murare, curare e aprire diventano un triangolo, ma se il muro è già speso la caverna resta chiusa.

**Raccomandata: Il luogo.** Spiega perché lo possono aprire anche le Cantitrici, non tocca la scelta fra il muro e la cura, e la zona sacra c'è già nel canone (Consacrazione di Moradin, §2).

### D5 · Murare il varco nel ramo «meno luminoso»

Nel ramo luminoso il varco va murato entro la fine del round 1. Nel ramo «meno luminoso» gli hobgoblin entrano alla fine del round di sorpresa, e il master non dice se si fa ancora in tempo.

**Decidi se nel ramo «meno luminoso» il varco si mura in tempo.**

- **Troppo tardi** · gli hobgoblin sono già dentro alla fine del round di sorpresa: il muro chiude fuori l'ondata dopo, non loro.
- **Nel round di sorpresa** · se un PG lo chiede a Dana con il suo gesto, Dana lancia nel round di sorpresa e gli hobgoblin restano fuori.

**Raccomandata: Troppo tardi.** Va d'accordo con il canone del 2026-10-18 («cinque comunque, qualunque cosa facciano») e con lo «scontro vero» di D77. Con l'altra il ramo duro avrebbe una via d'uscita gratis.

### D6 · I tempi della serata `[INFERRED]`

Il Quickstart propone 2-3 minuti per la Scena 1, 10-15 per la Scena 2, 5 o 30-40 per la pulizia e 10 per il passaggio, con un segnale e un rimedio per ognuna.

**Conferma i tempi della serata, o cambiali.**

- **Conferma** · i tempi diventano canone e il tag cade.
- **Più lungo** · 20 minuti per la Scena 2, perché i gesti sono otto.

**Raccomandata: Conferma.** I rimedi ci sono già («SOPRA», il blocco di nani che travolge), e il DM a freddo non ha segnalato problemi sui tempi del tavolo.

### D7 · I tre esempi di «assorbi, poi rilancia» `[INFERRED]`

Sono tre: gli orchi che portano all'orda il nome dei Quattro, il torque nella mano del re, i due prigionieri da tenere.

**Conferma i tre esempi del §0-ter come canone.**

- **Canone** · i tre esempi diventano canone, e il tag cade.
- **Solo esempi** · restano esempi da adattare, scritti così, senza tag.

**Raccomandata: Canone.** Il primo è il più forte: nell'ARC-08 i generali sanno già che i Quattro sono tornati. Lo usa già il DM a freddo (P-MONDO).

### D8 · Il fischio dei sergenti `[INFERRED]`, e il ramo «meno luminoso» (DEV#11)

Il fischio arriva alla fine del round di sorpresa. Nel ramo «meno luminoso» è lo stesso istante in cui gli hobgoblin entrano, quindi lì il tavolo non ha nessun preavviso.

**Fissa quando si sente il fischio, in tutti e due i rami.**

- **Un round prima** · in tutti e due i rami il fischio arriva un round prima che entrino: alla fine del round di sorpresa nel ramo luminoso, subito dopo il quarto box nel ramo «meno luminoso».
- **Com'è** · si sente alla fine del round di sorpresa in tutti e due i rami.

**Raccomandata: Un round prima.** Risponde alla domanda 14 del developer (il rinforzo che i PG vedono arrivare) e non cambia il conto di chi passa.

### D9 · Scalare lo scontro `[INFERRED]`, e il quarto PG (DEV#17)

Il blocco fissa un EL intorno a 9, la scala in tempo e le righe per tre e per cinque PG. Con tre giocatori il quarto PG arriva lo stesso, ma non si sa chi lo muove.

**Conferma la scala e assegna il quarto PG.**

- **Un giocatore** · confermi la scala, e il quarto PG lo muove un giocatore presente, dal round 1.
- **Il DM** · confermi la scala, e il quarto PG lo muove il DM: difende il re e non cerca il finisher.

**Raccomandata: Un giocatore.** Il PG resta un protagonista e non diventa un PNG del DM, e il finisher può andare comunque a un giocatore.

## Seconda passata

Esiti: CHIUSO 4 (il PARZIALE e i tre NUOVI) · nessun box toccato.

| Rilievo di VERIFICA.md | Esito | Cosa ho fatto |
|---|---|---|
| DM#3 · la tavola dell'Affresco A8 (PARZIALE) | CHIUSO | Il master adesso dice che il repo non ha ancora una tavola da stampare. Finché manca la stampa, il DM la descrive a voce: lo dicono il §9 e la riga del Quickstart «Cosa si consegna». La tavola all'80% è entrata nella lista delle immagini che mancano (§9, Immagini) |
| NUOVO 1 · il *muro di spine*, la regola detta a metà | CHIUSO | Ho scritto la regola SRD per intero. La prova di Forza si fa con un'azione di round completo, e si avanza di 1,5 m ogni 5 punti oltre 20, quindi serve almeno 25 e un sergente arriva al massimo a 22. Con le armi da taglio ci si apre la strada a 30 cm ogni 10 minuti, e il fuoco magico brucia il muro in 10 minuti |
| NUOVO 2 · «il varco non lo chiude più nessuno» | CHIUSO | In «Le cure di Dana» ho aggiunto «a meno che Hella non abbia preparato un muro» |
| NUOVO 3 · l'Acrobazia in due punti su tre | CHIUSO | Ho aggiunto Acrobazia anche nella tabella «Dove sono tutti» |

Gate rilanciati. `misura_craft --box` dà 9 box, 0 sopra le 12 righe, 0 con parentesi e 1 con più di un nome, lo stesso di prima. `validate_modules` dà 0 errori. Passano `domande_developer --check`, `copertura_scene --check` e `validate_prosa`. `test_storico.py` adesso dà 8 su 8. `componenti --check` boccia solo `APPARATO-ARC07-DEF-5-RITORNO-HAMMERFIST.md`, che va rigenerato: come mi hai chiesto, non ho lanciato `--apparato`.
