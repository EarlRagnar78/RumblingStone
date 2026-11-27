# P16 · Lotto ARC-08: le marcature `[INFERRED]` rimaste (2026-11-04)

> Voce P16 dell'indice §0 di `plans/STATO-E-ORDINE-DEI-PIANI.md`. Primo lotto,
> come vuole la voce: prima ARC-08, poi ARC-09, poi il resto.
> Regole usate: la regola del DM del 2026-10-31 (fra due decisioni vince quella
> senza regressione misurabile, i dubbi vanno a una card con la consigliata) e la
> preferenza del 2026-10-18 (la versione più potente e terrificante, cercando D&D
> 3.5, poi PF1e, poi l'SRD, con la fonte segnata).

## 1. Il conto vero

La voce P16 diceva 44 marcature in tutto, 3 in ARC-08. Il conto si faceva con
`grep "\[INFERRED\]\|\[PROPOSTA\]"`, che vede solo il marcatore nudo e salta
`[INFERRED — nota]`. Rimisurato con `scripts/inventory_inferred.py` su `main`
(8d4bb89):

| Misura | Aperte in tutto il repo | ARC-08 |
|---|---:|---:|
| P16, a mano | 44 | 3 |
| `inventory_inferred.py` su `main` | 244 | 98 |
| `main`, con le due correzioni allo strumento (§2) | 240 | 109 |
| dopo questo lotto, parte A (§3) | 227 | 96 |

## 2. Due correzioni al contatore (ADR breve)

**Contesto.** Lo strumento contava come debito anche le righe che *descrivono*
la convenzione («oggetti fuori SRD marcati `[INFERRED]`», «`null` = [INFERRED]»):
21 righe in tutto. E leggeva riga per riga, quindi non vedeva un marcatore la cui
nota va a capo (`[INFERRED — la frana non ha numeri…` su due righe): 17 marcature
vere non comparivano, 14 delle quali in ARC-08.

**Decisione.** Le righe che nominano la convenzione passano alla classe «meta»
(il marcatore subito dopo «marcato», «flag», «non più», «`null` =», «le scelte»).
Il marcatore si cerca sul testo intero, con la nota che può andare a capo fino a
tre volte. Tre test nuovi in `scripts/tests/test_inventory_inferred.py`.

**Conseguenze.** Il numero sorvegliato scende di 21 e sale di 17 per motivi che
non sono lavoro fatto: il conto di §1 li separa. La baseline del ratchet si
abbassa al numero nuovo nello stesso commit.

## 3. Parte A: chiuse da una regola, da un conto o da una decisione già presa

| Dove | Cosa | Perché si chiude |
|---|---|---|
| Mappe L2, scale della scarpa | 30 m di rampa | sono i 20 quadretti AM-BF della mappa, a 1,5 m |
| Mappe L2, strada a tornanti | 530 m | conto: 80 m di quota al 15% = 533 m |
| Mappe L2, scala della cittadella | 20 m | conto: da +100 a +120, le quote del DM del 2026-10-22 |
| Mappe L2, pendio | 27% | conto: 80 m su 300 m |
| Mappe L3, pendio della carica | 27% | conto: 30 m su 110 m |
| DEF-2, Muro Est e breccia (2) | il Muro Est sta nel settore della Torre Est | stesse colonne CM-CP della torre sulla MAPPA 2A |
| DEF-2, la riserva | entra un reparto solo | il libretto dice «entra come terzo reparto», al singolare |
| DEF-2, il corno della ritirata | **cambia**: prima nessun settore prendeva tacche | la domanda 14, decisa dal DM il 2026-10-22: il settore che un eroe lascia prende le tacche. La Torre Ovest no, perché Dara tira dalla torre. È la versione più dura, quindi nessuna regressione |
| DEF-1, Osservare sotto 20 senza allarme | Ricognizione «parziale» | «fallito» vuole l'allarme, e `ARC08-10` §5.5 dà «parziale» a ogni riga non elencata |
| ESITI, «Tornerà?» | la risposta segue la carta S2 | è un se: carta tenuta sì, carta tolta no |
| GUIDA e scontri, Benedizione di Moradin (2) | +4 sacro solo con l'incantesimo | SRD: un bonus viene da una fonte; senza incantesimo non c'è |

## 4. Le card al DM, una per dubbio

1. **La quota sul mare (25 marcature nelle mappe).** Il DM il 2026-10-22 ha dato
   le quote dalla piana (0, +80, +100, +120). I 870 m sul mare li ha aggiunti un
   agente, e ARC-07 li riprende. In 3.5 la quota conta solo sopra i 1.500 m
   (*Guida del DM*, passi bassi), quindi nessun numero di gioco cambia.
   *Consigliata*: tenerli, come dato di colore, coerenti in ARC-07 e ARC-08.
2. **Le baliste contro il drago a 45 m (DEF-2 Scena 2).** A: fuori gittata
   (le mappe, senza fonte). B: *Guida del DM* 3.5, incremento 36 m, a 45 m −2.
   C: balista pesante PF1e, 54 m, nessuna penalità. *Consigliata*: B, la prima
   fonte nell'ordine e la più dura delle due con fonte. ✅ **Decisa dal DM il
   2026-11-04: B.** Applicata in DEF-2 (domanda 2 e Scena 2) e nella MAPPA 3 di L2.
3. **L'Aura della Forgia Eterna già spesa (GUIDA, scontri).** Thorik l'ha usata
   nella battaglia antica, mille anni prima ma pochi giorni prima per lui.
   *Consigliata*: conta il tempo di Thorik, quindi nella carica finale
   quella settimana non c'è.
   ✅ **Decisa dal DM il 2026-11-04: come consigliata.** Applicata in GUIDA e scontri.
4. **Borin che fa da scudo al Re contro il soffio (DEF-2 Scena 6).** In 3.5 un
   soffio a cono non si para con il corpo: chi è nel cono tira i Riflessi, e una
   creatura davanti non dà copertura contro un'area. Il master dava al Re metà
   danni senza tiro e +2 al morale. *Consigliata*: seguire la regola: resta la
   spinta (opzione B, SRD) per togliere il Re dal cono; l'opzione A e il suo +2
   escono.
   ✅ **Decisa dal DM il 2026-11-04: come consigliata.** In DEF-2 l'opzione A
   diventa «davanti alla lancia» (round 5, la parte che non riguardava il
   soffio), escono il dimezzo senza tiro e i due +2 al morale (tabella e round
   3-4), la scheda della serata dice «spinto / davanti alla lancia», e la MAPPA
   3 di L2 è allineata. `hammerfist_encounters` ha ancora la versione vecchia:
   è il file che MASTER-DEF D6 propone di archiviare, e lì resta.
5. ~~**Le altre scelte del master (§5).**~~ Card ritirata il 2026-11-04: il DM
   ha chiesto che si chiuda solo ciò che è già fatto, risolto o superato, mai in
   blocco per comodità. Rifatta come §4-bis.

## 4-bis. Le card rifatte con lo schema del DM (2026-11-04)

Regola di Jfs, 2026-11-04: una marcatura si chiude solo se è già fatta, risolta
o superata, e la card lo dice con la prova; il resto è una decisione vera.

- **Card «chiuse perché risolte o superate»**: le 13 della parte A (§3), più
  B19 (le frecce di Dara: il DM ne ha fissato la CD il 2026-10-23, quindi le ha
  già messe in gioco). Si chiede solo di confermare. ✅ **Confermate tutte e 14 dal DM il 2026-11-04.**
- **Sette card di decisione**, una per tema, sulle scelte del master ancora
  aperte (colonna «Card» di §5): 1 il morale, 2 il cancello e Gorthak, 3 il
  drago e il cavaliere, 4 Grimjaw e il Re, 5 la ritirata e i tunnel, 6 le forze
  e i pregen, 7 dopo la battaglia. Nessuna è già decisa altrove: cercate in
  `giro-arc08-sessione1-2026-10-21/`, `giro-arc08-sessione2-2026-10-22/`,
  `a3-arc08/` e nel canone del 2026-10-30 sul Cuore della Montagna (che fissa lo
  schieramento in ARC-07, non quanti nani arrivano al Cuore in ARC-08).

**Risposte del DM, 2026-11-04.** Card 1 (morale): come scritte. Card 3 (drago e
cavaliere): come scritte tranne la mira di Dara, tolta (Dara a +17 colpisce la
CA 37 solo col 20, la CA 29 con 12). Card 4 (Grimjaw e il Re): come scritte.
Card 6 (forze e pregen): come scritte. Card 2 (cancello e Gorthak): come scritte. Card 5 (ritirata e tunnel): come scritte, al Cuore arrivano 90 nani meno le perdite del Registro. Card 7 (dopo la battaglia): come scritte. Quota sul mare: tenuta (piana 870 m), con i gradoni del DM del 2026-10-22 (+80, +100, +120 = 950, 970, 990 m); controllati coerenti: strada 530 m al 15% per 80 m, pendio 80 m su 300 m (27%), canyon +30 e torrione +60 sotto il fronte sud. Condotto della sorgente: tenuto, largo 1,5 m (corretta la COMPRENSIONE che diceva «carponi»), e nell'ondata 3 cinque bugbear lo risalgono e sbucano dietro l'altare. L'ottagono del Cuore (L3, MAPPA 3Z) non era in nessuna card: è chiuso perché misurato sulla griglia (27 quadretti, 40,5 m); il condotto della sorgente (L3, MAPPA 5) va a una card sua. Nel testo la marca è
`[CANONE — DM 2026-11-04, P16, <tema>]`.

## 5. Parte B: le scelte del master, da fare canone in blocco

Sono le marcature in cui il master ha già scritto una scelta, e la scelta è la
versione più dura o serve alla scena senza toccare i numeri di un nemico.

| # | Dove | La scelta del master | Consiglio | Card |
|---|---|---|---|---|
| B1 | DEF-2 tabella del morale, Scena 2 | un eroe che colpisce il drago nel sorvolo: +1 | canone | 1 · Morale |
| B2 | DEF-2 morale, Scena 6, appendice | il Re che cade sul cancello: −2 | canone | 1 · Morale |
| B3 | DEF-2 Scena 2 e appendice | lo sportello del cancello, largo un nano | canone | 2 · Cancello |
| B4 | DEF-2 Scena 2 | Gorthak che fugge il Giorno 1: il cancello perde la metà quel giorno | canone | 2 · Cancello |
| B5 | DEF-2 Scena 2 | il macigno colpito non parte (non provato negli script) | canone | 3 · Drago |
| B6 | DEF-2 Scena 2 | la testa centrale di Gorthak chiama un reparto in più (la scheda dava +2 morale) | canone: un reparto vale più di +2 | 1 · Morale |
| B7 | DEF-2 Scena 2 e appendice | Gorthak sotto metà: un round di Furia, poi la fuga | canone | 2 · Cancello |
| B8 | DEF-2 Scena 2 | il cancello caduto il Giorno 1: una tacca a round | canone | 2 · Cancello |
| B9 | DEF-2 Scena 2 | il sorvolo al round 4, 1d4 PFU ai balestrieri di una torre | canone | 3 · Drago |
| B10 | DEF-2 notte | il cancello riparato di +20 pf a notte | canone | 2 · Cancello |
| B11 | DEF-2 Scena 4 | Grimjaw senza sfidante: +1 ad AU e DU, e al round 2 il Re scende a cercarlo | canone | 4 · Grimjaw |
| B12 | DEF-2 Scena 4 | il Re torna con 4d10+20 danni | canone | 4 · Grimjaw |
| B13 | DEF-2 notte | il Coro fa crollare la rampa: Torre Est a fronte 1 | canone | 4 · Grimjaw |
| B14 | DEF-2 Scena 6 | il cancello caduto: il Cancello combatte nell'androne | canone | 2 · Cancello |
| B15 | DEF-2 Scena 6 | la lancia del cavaliere nella picchiata | canone | 3 · Drago |
| B16 | DEF-2 Scena 6, Nala | l'*immagine silenziosa*: se Fauci ci crede, la sequenza slitta di un round | canone | 3 · Drago |
| B17 | DEF-2 Scena 6 | il soffio toglie 1d4 di CA alle armature, per sempre (non SRD) | canone, ⚠️ non SRD | 3 · Drago |
| B18 | DEF-2 Scena 6, Dara | la mira: +1 al tiro dopo (non SRD) | **esce**: nessuna fonte, e la versione senza è la più dura | 3 · Drago |
| B19 | DEF-2 Scena 6, armeria, tesoro | le due frecce ammazzadraghi di Dara | canone: il DM ne ha già fissato la CD (2026-10-23) | già risolta: card «chiuse perché risolte» |
| B20 | DEF-2 Scena 7 | Nala +2 alla porta (le lanterne) | canone | 5 · Ritirata |
| B21 | DEF-2 Scena 7 | i nani al Cuore: 90 come tetto, le perdite nel Registro | canone | 5 · Ritirata |
| B22 | DEF-2 Scena 8 | senza un ordine a round cadono 1d4 nani e un bugbear passa | canone | 5 · Ritirata |
| B23 | DEF-2 dopo | la corona nera, se il soffio ha preso il Re | canone | 5 · Ritirata |
| B24 | DEF-1 Fase 3 | due round alla torre dopo uno scontro aperto, una prova sola | canone | 5 · Ritirata |
| B25 | DEF-1 Sessione 1 | il Re al Cancello se Borin non lo convince | canone | 4 · Grimjaw |
| B26 | DEF-1 sorvolo | il fumo dell'acido: Tempra CD 15 o nauseato 1 round | canone | 3 · Drago |
| B27 | DEF-1 regia | l'orda terrificante se il tavolo va liscio (+1 AU e DU) | canone | 1 · Morale |
| B28 | DEF-1 leve | Grimjaw cerca l'eroe che ha visto sul pendio | canone | 4 · Grimjaw |
| B29 | DEF-1 e GUIDA, Dara e Nala | +18 a Osservare e Ascoltare di Dara; 8 + Int punti della Spia Maestra | canone, da riscontrare sul manuale quando c'è | 6 · Forze |
| B30 | DEF-1 duello | la frana: 4d6, Riflessi CD 15 | canone | 5 · Ritirata |
| B31 | ARC08-19 | la riserva entra nel settore che cede e non torna | canone | 5 · Ritirata |
| B32 | GUIDA, élite | 4 capitani su worg; 70 élite = 40 worg rider e 30 sergenti; 5 adepti | canone | 6 · Forze |
| B33 | GUIDA, finale | i 50 hobgoblin d'élite con la scheda dei guerrieri 3; uno contro uno i veterani GS 5 | canone | 6 · Forze |
| B34 | GUIDA, finale | il conto della Guarigione parte dal round 1, o dall'11 senza flashback | canone | 5 · Ritirata |
| B35 | GUIDA e scontri | Inathiel si gioca col gufo gigante celestiale GS 6 | canone | 6 · Forze |
| B36 | GUIDA e scontri, ricompense | i seguaci: quanti e come col *Comando* della *Guida del DM* | canone | 7 · Dopo |
| B37 | ESITI §4 | Fauci fugge nelle montagne meridionali; il punto lo fissa ARC-09 | canone | 7 · Dopo |
| B38 | ESITI §4 | il cavaliere conosce il piano fino a Rethmar | canone | 7 · Dopo |
| B39 | ESITI §4 | dell'uovo di Fauci il cavaliere non sa niente (eco per ARC-10) | canone | 7 · Dopo |
| B40 | ESITI §4 | lo scrutare di Hella lo vede ferito, a terra, nelle montagne | canone | 7 · Dopo |
| B41 | ESITI §4 | la comunione della Corona: livello dell'incantatore 20, come un artefatto | canone, la versione più forte | 7 · Dopo |
| B42 | ESITI §5.5 | il ripiego se il flashback non si gioca | canone | 7 · Dopo |
| B43 | ESITI §6 | l'armeria: oggetti perfetti e consumabili, niente magia su misura | canone | 7 · Dopo |
| B44 | HANDOUTS | la Mente Vuota di Thorik non blocca la visione, perché viene dalla Corona stessa | canone: se la bloccasse, ARC-08 non avrebbe la sua cornice | 7 · Dopo |

## 6. Fuori da questo lotto, perché la domanda è già al DM

- **MASTER-DEF D6** (censimento delle versioni) contiene già i troll dell'ariete
  (DEF-2 Scena 2 e appendice), la riserva a +3 al morale e l'archiviazione di
  `hammerfist_encounters` dopo la fusione. Non si chiedono due volte: quando il
  DM risponde a D6, le marcature si chiudono con quella risposta.
- **P09** contiene già cosa succede quando Fauci lascia Thorik: la presa al volo
  con Riflessi CD 20 (GUIDA e scontri) aspetta quella risposta.

## 7. Come si applica

Le risposte del DM entrano nel testo come `[CANONE — DM <data>, P16 <n>]` al
posto della marcatura. B18 e la card 4 tolgono testo: si riscrive la riga, e il
conto di §1 si aggiorna con `python3 scripts/inventory_inferred.py --check`.

## Da rivedere se

- Il DM cambia le quote delle mappe o il libretto delle battaglie di massa: la
  parte A sulle mappe e sulle tacche dipende da quelle due fonti.
- Lo strumento conta di nuovo marcature dentro i blocchi di codice o i
  commenti `<!-- storico -->`: oggi le conta, ed è una scelta da rivedere con
  ARC-09.

## 8. Quota sul mare abbassata (DM, 2026-11-04)

Dopo la card, il DM ha chiesto una quota più realistica, in linea con la carta
della valle (fasce: piana sotto 400 m, colline 400-900, montagna oltre 900 con
neve). Hammerfist sta nella fascia delle colline sotto il North Wall, sopra la
piana di Dauth (490 m, Porta Sud 530 m). Scelta del DM: **piana a 520 m**, quindi
cancello 600, cortile interno 620, cittadella 640; canyon 550, torrione 580,
linea hobgoblin 570, piede della cinta 595, piattaforma del cancello 615. I
gradoni +80/+100/+120 non cambiano. Stesso spostamento (−350 m) in ARC-07
(M7-B, M7-C, M7-H, DEF-4), nella carta regionale e nell'aria del barile
(1,17 kg/m³ a 520 m, ISA; `simula_barile.py` non la usa, i suoi esiti non
cambiano).
