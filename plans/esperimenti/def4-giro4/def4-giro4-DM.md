# DEF-4, giro 4 · il DM a freddo

**Bersaglio**: `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
al commit `3909e7e` (impronta letta `e8687781…f8288`, la stessa di `git show
3909e7e:<master>`). Le parti fra `<!-- storico -->` e `<!-- apparato -->` sono
state saltate.
**Rubrica**: `skills/rumblingstone-playtest/references/dm-a-freddo.md`, tre passi.
**Chi legge**: un DM che non ha scritto il modulo e deve condurre stasera il
gruppo vero, che riparte dalla notte del 372 con 3 tacche segnate.
**Tempo di preparazione dichiarato**: **un'ora**.
**Corsa**: `plans/esperimenti/def4-giro4/corsa-dm/dm/` (`diario.jsonl`,
`stato.json`), 17 passaggi su 17, nessuno smesso.

⚠️ **Limiti di questa corsa, da dire subito.**
- La rubrica vuole un agente **nuovo** per la vista (passo 1) e per il giorno
  dopo (passo 3). Qui è stato lo stesso agente: la vista è stata letta e
  annotata **prima** di aprire la prima scena, e il giorno dopo è stato
  risposto dal solo diario (`ricordo_lettura.py domande` e `chiedi`), ma la
  memoria della lettura c'era. Le risposte del passo 3 vanno pesate così.
- L'ora è finita a metà della Scena 6 (rilievo 1). Ho proseguito oltre, per
  dare al DM una preparazione intera, e lo segno: i rilievi nati dopo il
  minuto 60 portano «oltre l'ora» nella prova.
- Durante la lettura il ramo è andato avanti (`21e7fc1`, «D74 decisa dal DM:
  sì a tutto, canone in DEF-4»): il master sul disco non è più quello letto.
  Questo rapporto vale per `3909e7e`; alcuni rilievi potrebbero essere già
  chiusi da D74, che non ho letto per restare a freddo.

---

## Primo passo · la vista di chi scorre

`python3 scripts/vista_di_chi_scorre.py <master>`, risposte scritte prima di
aprire il testo.

1. **Cosa succede stasera.** Dalla vista: il portale posa i PG nel bosco al
   tramonto, il re chiede Zog'tar di notte e il drago all'alba, poi il rito e il
   Rubino. **Per il mio gruppo è sbagliato**: tramonto, portale e consiglio sono
   già giocati. La vista non mostra il riquadro «La vostra serata», che dice da
   dove si riparte e dove ci si ferma.
2. **Chi si oppone.** Zog'tar (cosa vuole: la vista non lo dice) e Skullcrusher,
   che combatte per contratto di «un runaio» senza nome. Vatore: alleato o
   nemico, dalla vista non si capisce.
3. **Cosa preparare.** Appendice A, l'orologio della notte, le mappe
   dell'Appendice D, gli handout di §9, la variante A.1-bis. Non si vede il
   booklet della regia, né il log del gruppo che «La vostra serata» chiede di
   leggere.
4. **Cosa mi ha fatto rispondere.** Il riquadro «La serata in tre frasi» e le
   righe «In scena». Rumore: i grassetti di servizio (*MASTER DEFINITIVO…*,
   *Sistema: D&D 3.5 SRD*, *CD*, *1,5 m/quadretto*, *4 PG*), venti CD senza
   contesto (`CD 20 ← …`), e tre «prime frasi» di scena che non sono frasi:
   un link d'immagine (Scena 1), una nota di servizio (Scena 8), *«Il canone di
   §6 è esplicito»* (Scena 12).

## Secondo passo · la preparazione a scene

Il diario intero è in `corsa-dm/dm/diario.jsonl` (si stampa con
`python3 scripts/lettura_a_scene.py diario plans/esperimenti/def4-giro4/corsa-dm/dm`).
L'ago è rimasto fra 0 e +2 per tutta la lettura: il master si conduce, e le
scene della notte (6-8) e il duello (11) sono preparate meglio di quanto un DM
a freddo si aspetti. I buchi stanno quasi tutti nel **raccordo fra il master e
questo gruppo**: il master descrive bene ogni via, ma per il gruppo che vola,
con 3 tacche e una druida che non ha deciso niente, lascia al DM alcuni conti.

**Il conto del tempo**, come è andato davvero:

| Pezzo | Minuti | Cumulato |
|---|---:|---:|
| premessa, §0 e «La vostra serata» | 15 | 15 |
| il log del 25 settembre sul ramo del gruppo | 5 | 20 |
| Atto I scorso (già giocato) | 10 | 30 |
| l'orologio della notte | 6 | 36 |
| Scena 5, solo Treant e dado dei caduti | 12 | 48 |
| Scena 6, il mare di tende | 21 | **69 — l'ora finisce qui** |
| Scene 7-9 | 40 | 109 |
| Scene 10-11 | 25 | 134 |
| Scene 12-13 scorse, appendici A e D | 20 | ≈155 |

«La vostra serata» chiede da sola 10 + 15 + 25 + 5 minuti più le Scene 10 e 11
senza tempo, più A.1, più il log, più le due cose della Scena 5: è già oltre
l'ora prima di cominciare.

### La preparazione del DM, voce per voce (D12)

| Voce | Esito | Cosa |
|---|---|---|
| `P-RILIEVI` | fatto | ogni rilievo qui sotto ha la risposta che darei al tavolo, nella colonna della correzione |
| `P-GRUPPO` | **manca nel repo** | il log del 25/9 (ramo `campaign-group-rumblingstone`) dà fiducia piena, 5 *volare* + 4 «CFC» del re, 2 *invisibilità* comprate, la tacca della fucina. Non dà: se hanno preso il **Nome** della targa, se qualcuno ha bevuto la pozione n. 4 (il segno che Vatore vede), se hanno comprato la **pietra del silenzio**: la riga delle richieste aperte è ancora «______». Rilievo 9 |
| `P-MONDO` | fatto | l'orologio (8 tacche), Grask sveglio fino alla 4ª, il drago sulle colline e il corno a 70 round, le ronde 1d4+2, gli squadroni 2d4+2, Zog'tar vivo all'alba se non lo raggiungono: tutto nel master |
| `P-STATO` | fatto, fuori dal master | APL 13 e livelli da `campaign/state.md` del ramo del gruppo (Hella Ranger 1 / Druido 12); il master non rimanda a `state.md`, e la scalatura A.1-bis dipende dal livello. Durik nel §1 |
| `P-STILE` | fatto | ritratti di Durin, Re Thorek, Thorgrim, Zeth, Zog'tar, Balvar, Vatore e la tavola del drago ci sono tutti; schede d'entrata con «Suona» per ognuno |
| `P-IMMAGINI` | **elencate, non generate** | per stasera mancano: Hrodgar, Hald, Grask, il sacerdote dell'orda; nessuna tavola per il volo sul campo, l'esterno della tenda nera o le mura all'alba. Rilievo 15 |
| `P-HANDOUT` | fatto | per stasera non ne manca nessuno: piano di battaglia e le dieci boccette sono in `homebrew/volume-mille-anni/`, gli echi nel booklet della serata |
| `P-FLUSSO` | rilievo | la via del mio gruppo (volo) passa bene fino alla tenda; dopo, Vatore e Balvar chiedono al DM di decidere. Rilievi 6, 7 |
| `P-DOMANDE` | fatto | le domande provate sono nel passo 3; quelle senza risposta sono i rilievi 4, 5, 9, 12 |
| `P-CONGEGNI` | rilievo | orologio, skill challenge, Catena, corde e dado dei caduti si conducono; Grask e i Treant no, per questo gruppo. Rilievi 3, 4, 5 |
| `P-INTERAZIONI` | rilievo | la runa di *resistere all'energia* non è ricordata al duello; la pozione n. 4 non torna nella Scena 9. Rilievi 7, 13 |
| `P-CONFINE` | fatto | il master separa bene «Dati per il DM (non da leggere)» e «Cosa NON dire»; nella mia preparazione ho tenuto a parte quello che i PG sanno (il log) da quello che so io (Hald, la Catena, Vatore = Sal) |

## Terzo passo · il giorno dopo, al tavolo

Dal solo diario (`ricordo_lettura.py domande` e `chiedi`), con il limite detto
in testa.

- **Chi entra per primo, e cosa dice?** *Se il tavolo esce subito*: Durin alla
  postierla, *«Tornate. Il Padre non butta via un dono così.»* (diario, 8). *Se
  la serata si apre nella fortezza*, come lasciano intendere la premessa e la
  regia: **non è rimasto niente**. Il diario dice «il master non mi dà la prima
  battuta della ripresa» (17). È il rilievo 2.
- **Se i giocatori chiedono «torniamo in volo?», cosa rispondo e dove?** Sì: 5
  *volare*, tre all'andata (Thorik, Tordek, Hella), le due rimaste ai nani al
  ritorno, Hella da aquila, Artemis vola da sé; Scena 6, «Chi vola, e chi no»
  (8). Il conto per il mio gruppo l'ho fatto io: il master non lo fa.
- **Se chiedono «quanto manca all'alba, in ore?»**: non lo so. Il diario
  annota tre misure diverse della tacca e un `[INFERRED]` (2, 6). Rilievo 12.
- **Se chiedono «Balvar viene con noi?»**: la risposta c'è (D55, D66), ma nella
  Scena 8 e non nella 7 dove nasce la domanda (10).
- **Dove sono tornato indietro, e quanto ho perso?** Alla Scena 5 per i Treant
  (subito trovati) e per il dado dei caduti (220 righe dentro il banco, due
  minuti); al log del gruppo su un altro ramo (cinque minuti); al percorso del
  booklet della regia, cercato a mano (due minuti); a `state.md` per il
  livello. Le invenzioni mie, segnate come tali: tre nomi nanici per i caduti
  delle mura, e Vatore spostato sulle mura perché il gruppo vola.

Le sette domande del pacchetto, in breve: la serata è *volo sul campo, tenda
con Balvar e Zog'tar, Vatore, mura e duello, stop sull'esito*; l'avversario è
Zog'tar (vuole Hammerfist), Skullcrusher (il tesoro e un secondo re davanti
all'orda), Balvar (che la fortezza cada in fretta, e essere ricordato); si
parte dalla fortezza con 3 tacche e si arriva al cortile; se falliscono la
prova centrale il duello si gioca lo stesso, gli avi intervengono e la vittoria
è «sporca»; il picco è Balvar, *«Quindi non è oggi.»*; finisce sull'esito del
duello; ho riletto la Scena 5, il log e il booklet.

---

## L'uscita

Gravità: 🔴 *la serata non si capisce senza leggere tutto* · 🟠 *il DM perde
più di 30 secondi a cercare* · 🟡 *se ne accorge un DM attento*.

| # | Passo | Codice | Cosa manca | Gravità | Prova | Correzione minima |
|---|---|---|---|---|---|---|
| 1 | 2 | `D-TEMPO` | «La vostra serata» non entra in un'ora: l'ora finisce a metà della Scena 6, e il duello, che è metà serata, resta senza preparazione | 🟠 | «§4 «L'orologio della notte» (10 min) · Scena 6 il mare di tende (15 min) · Scene 7 e 8 […] (25 min) · Scena 9 Vatore (5 min) · Scene 10 e 11, le mura e il duello, con l'Appendice A.1» (§0): la somma è già 55 minuti senza le Scene 10-11, senza il log e senza la Scena 5 | dare un tempo anche alle Scene 10-11 e dire cosa si legge **solo** di ognuna (per il duello: scheda d'entrata, il giro, «Chi sceglie», le corde, A.1), così che il totale stia in 60 |
| 2 | 1, 3 | `D-SERATA` | da dove si comincia stasera e chi parla per primo: la premessa dice che la Scena 5 è ancora aperta, «La vostra serata» che la fortezza è giocata; nessuna delle due dà la prima battuta della ripresa; la vista mostra solo il tramonto | 🟠 | «il resto della Scena 5 è ancora aperto, poi il campo» (premessa) contro «Il resto del master (Atto I, la fortezza, il banco) è già giocato: lo apri solo se ti chiedono qualcosa» (§0) | una riga in «La vostra serata»: *si riapre nei quartieri ospiti, Durin entra con …; le scelte ancora possibili sono sosta, banchetto, veglia dei semi*; e il riquadro letto dalla vista deve essere questo, non quello dell'arco |
| 3 | 2 | `P-CONGEGNI` | Grask per questo gruppo: con il volo l'ultima tacca segnata è la 4ª, quindi è **sveglio** all'atterraggio; non è detto se la tacca del volo si segna alla partenza o all'arrivo, e la prova dell'atterraggio contro di lui è `[INFERRED]` | 🟠 | «sveglio finché l'ultima tacca segnata è la **4ª**, addormentato da quando si segna la **5ª**» (Scena 6, Grask) · «chi scende visibile tira Nascondersi contro il suo Osservare […] `[INFERRED — needs DM confirmation]`» | in «Dove si riprende» una riga: *con 3 tacche e il volo, Grask è sveglio quando atterrate*; e chiudere l'`[INFERRED]` dell'atterraggio |
| 4 | 2 | `P-CONGEGNI` | i Treant per questo gruppo: Hella non ha deciso niente, e il master non dice se per averli all'alba deve spendere stanotte la tacca «veglia i semi», o se li ha comunque | 🟠 | «la tacca della notte resta **una**: vegliare i semi che si aprono» (Scena 5) e «Se Hella ha vegliato i semi, i due Treant […] caricano» (Scena 10), contro «Per **questo** gruppo […] i Treant restano dove la giocatrice li vuole» (Scena 5) | una riga nella tabella dei Treant: *per il gruppo del 25/9 la veglia costa / non costa la tacca*; e chiudere l'`[INFERRED]` del Treant alla tenda |
| 5 | 2 | `D-SALTO` | il dado dei caduti: si tira alle mura ma la regola sta a metà del banco della Scena 5; non dice cosa vuol dire il numero (quanti morti?); il log del gruppo lo manda al *Registro delle Perdite* di ARC-08, il master dice di no | 🟠 | «Alla Scena 10 si tira **1d4** per ogni **tipo**» (Scena 5, dentro il banco) · alla Scena 10 solo «nessuno sulla prova: il dado dei caduti del 372 (Scena 5)» · log: «Quattro tiri sul *Registro delle Perdite* di ARC-08» | copiare nella tabella «Dalla notte» della Scena 10 la regola in una riga (*quattro tiri da 1d4, il numero è quanti difensori con nome muoiono, non tocca ARC-08*); correggere il log del gruppo |
| 6 | 2 | `P-FLUSSO` | Vatore con il gruppo che torna in volo: la scena è scritta per chi passa a piedi o invisibile fra le tende; chi vola sopra i 20 m non ha motivo di atterrare nel campo | 🟠 | «chi torna in volo lo vede dall'alto, e la scena comincia da dove atterra» (Scena 6) · Scena 9: «Se passano invisibili» c'è, «se volano» no | una riga nella Scena 9: *se il gruppo torna in volo, Vatore è sulle mura nel caos dell'alba (come «se il tavolo ha fretta»), oppure lo vedono dall'alto e decidono loro se scendere* |
| 7 | 2 | `P-INTERAZIONI` | la pozione n. 4 dalla cera nera lascia un segno che «Vatore vede»; nella Scena 9 non c'è cosa fa quando lo vede | 🟡 | «un riflesso violaceo sotto la pelle del polso, che vedono soltanto gli agenti della gilda del Collezionista. Vatore lo vede» (Scena 5) | una riga nella tabella di Vatore: *se un PG ha il segno, Vatore lo guarda e …* |
| 8 | 2 | `L-AMBIGUO` | quindici `[INFERRED — needs DM confirmation]` sulla strada di stasera, in un master DEF dopo D49-D73: sette nella sola Scena 6 (atterraggio contro Grask, lupi che contano doppio, ronda abbattuta in 2 round, Durik richiamato alla tenda, *trasporto vegetale*, il drago a 42 contro 70 round, l'allarme senza corno) | 🟠 | conteggio sui passaggi ricevuti dalla corsa: Scena 5 1, §4 1, Scena 6 7, Scena 7 1, Scena 8 2, Scena 10 1, Scena 11 2 | una decisione DM per ognuno, o almeno per i quattro che il gruppo che vola incontra di sicuro (Grask, Treant alla tenda, l'allarme senza corno, Balvar nel ritorno) |
| 9 | 2 | `P-GRUPPO` | il master manda al log del 25/9 per «la fiducia, le pozioni, cosa hanno venduto e comprato», ma il log non dice se hanno il Nome della targa, la pietra del silenzio, chi ha bevuto la n. 4 | 🟠 | «stanno nel log della serata del 25 settembre, sul ramo del gruppo» (§0) · log: «Quali di queste il gruppo ha preso davvero non è scritto: ______» | **manca nel repo**: chiedere al DM le tre risposte e scriverle nel log; nel master basta il percorso del log |
| 10 | 2 | `D-PREPARA` | «la regia della serata, nel suo booklet» senza percorso | 🟡 | «la regia della serata, nel suo booklet, dice dove tagliare» (§0); il file è `homebrew/sessione-notte-e-alba/01-REGIA-SERATA.md`, trovato a mano | il percorso fra parentesi |
| 11 | 2 | `L-ORDINE` | le Benedizioni di Moradin si danno alla Scena 4 come «+2/+2» e si spiegano solo alla Scena 6 | 🟡 | «le Benedizioni di Moradin +2/+2» (Scena 4) · «+2 morale al colpire e ai danni, 12 ore» (Scena 6) | la parentesi della Scena 6 anche nella Scena 4 |
| 12 | 2, 3 | `L-NUMERO` | quanto vale una tacca in ore: tre misure diverse e un `[INFERRED]`; se il tavolo chiede l'ora, il DM non ha la risposta | 🟡 | «otto ore, e ogni cosa ne costa» (titolo §4) · «Fermarsi **tre ore** · dormire **otto ore** — **2** · **6**» · «Una tacca non è un'ora […] `[INFERRED — needs DM confirmation]`» (Scena 1) | una riga: *una tacca vale circa un'ora del mondo, tranne la sosta e il sonno, che costano meno di quanto durano* (o quello che il DM decide) |
| 13 | 2 | `P-INTERAZIONI` | la runa di *resistere all'energia* acido 20, comprata in due, non è ricordata al duello, e va attivata quando il drago compare (azione standard) | 🟡 | «Se la attivano uscendo dalla postierla, all'alba è scaduta: va attivata quando il drago compare» (Scena 5); la Scena 11 non la nomina | una riga nel giro di Skullcrusher, round 1: *chi ha la runa di Zeth la attiva adesso* |
| 14 | 2 | `L-AMBIGUO` | chi sceglie il drago: «colpisce solo chi ha un nome… se non lo sa lo chiede», ma il box del round 1 fa gridare i nomi da ottocento nani; e la scalatura «ignora Hella» va contro D71 che la mette fra i preferiti | 🟡 | «Colpisce solo chi ha un nome, e il nome lo dice prima» (D71) · «il vostro stesso nome gridato da ottocento nani» (Round 1) · «Il drago la ignora finché non lo ferisce» (scalatura) | dire che dopo il round 1 i nomi li sa, e che la riga della scalatura vale solo se il DM la sceglie |
| 15 | 2 | `P-IMMAGINI` | per stasera mancano i ritratti di Hrodgar, Hald, Grask e del sacerdote, e una tavola per il volo, la tenda nera da fuori, le mura all'alba | 🟡 | `Immagini/ritratti/` a `3909e7e`: Balvar, Durin, Re Thorek, Thorgrim, Vatore, Zeth, Zog'tar | elenco per `rumblingstone-art-direction`; la corsa non può generarle |
| 16 | 2 | `L-ORDINE` | Balvar recuperato con il gruppo in volo: la risposta (D55, D66) è nella Scena 8, la domanda nasce nella Scena 7 | 🟡 | «Per arrivarci torna con i PG: nel ritorno a piedi tira con loro» (Scena 7) senza rimando · «Se Balvar è recuperato e il gruppo torna in volo» (Scena 8) | «(se tornano in volo: Scena 8)» nella riga della Scena 7 |
| 17 | 2 | `D-PREPARA` | due statblocchi di stasera fuori dall'Appendice A: i Treant (in `DEF-3` A.2, con FOR e TS `[INFERRED]`) e le wyvern della scalatura | 🟡 | «statblocco in `DEF-3` Appendice A.2» (Scena 5) · «le 2 **wyvern** […] (SRD, *Wyvern*: GS 6, 59 pf …)» solo nella sidebar | due righe in A.6 |
| 18 | 1 | `D-RUMORE` | la vista si ferma su grassetti di servizio, venti CD senza contesto e tre prime frasi di scena che non dicono niente | 🟡 | «GRASSETTI: MASTER DEFINITIVO — fast-play cinematografico · Sistema: D&D 3.5 SRD · CD · 1,5 m/quadretto · 4 PG» · Scena 1: «![Il portale del Tempo] e il percorso dell’immagine» · Scena 12: «Il canone di §6 è esplicito» | togliere il grassetto alle etichette d'apparato; aprire ogni scena con una frase di gioco |
| 19 | 2 | `D-RUMORE` | in §0-ter, la pagina «che serve mentre giochi», c'è una nota sullo stato del repo, fuori da `<!-- apparato -->` | 🟡 | «ed è la quarta cosa dichiarata e mai applicata di questo repo: il marcatore `[HDYWTDT]` era a zero in tutti e nove gli archi» | metterla fra `<!-- apparato -->` o toglierla |

**Conteggi**: 19 rilievi · 🔴 0 · 🟠 8 · 🟡 11.

**Cosa questa lettura non ha potuto verificare**: il ritmo vero al tavolo (le
tre ore della regia); se D74 (`21e7fc1`) chiude già qualcuno di questi
rilievi; le risposte di un agente davvero nuovo ai passi 1 e 3; la griglia
della M7-C, che sta in un altro file; il contenuto del booklet della regia oltre
la sua prima pagina.

## La registrazione della lettura

La corsa è in `plans/esperimenti/def4-giro4/corsa-dm/dm/`. La registrazione
con `registro_letture.py --registra … --ruolo dm` è stata tentata e **rifiutata
dallo strumento**: il master sul disco è cambiato durante la lettura (D74), e
il registro accetta solo la lettura del testo che c'è. Vedi la risposta finale
a chi ha avviato la corsa.
