# Le tattiche dei draghi: proposta e misura (15/11/2026)

Domanda di Jfs: i draghi sono le creature più intelligenti del gioco, quindi
devono avere tattiche superiori, e diaboliche dove ha senso. Le tattiche devono
seguire il carattere, gli obiettivi e quello che il drago sa dei PG, e cambiare
con l'ambiente e con quello che il drago percepisce. Skullcrusher è escluso: ha
già il suo thread.

Metodo, lo stesso di Skullcrusher:
- **Le quattro domande del drago, in ordine di priorità.** Cosa teme di perdere
  davanti al suo pubblico? Cosa non vuole perdere (il tesoro o lo scopo)? Che
  cosa succede se lo tirano giù? Qual è il suo punto debole?
- **Una sorpresa funziona per intero solo la prima volta.**
- **Una tabella «se i PG...»** con quello che il drago percepisce davvero.
- **Solo capacità della scheda** (cancello `coerenza_campagna.py fatti --tattiche`).

**Esito delle card del 15/11:** il DM ha scelto la consigliata su tutte e quattro (Fauci con la fuga a 112 pf; Tyrgarun stregone nelle Fasi 1-3 e la condizione scritta per la Fase 4; Arbitrax il bruto col difetto; Regiarix e il drago di Vaereth rifatti sull'SRD). Corrompere acqua e oscurità per Fauci restano proposte, non entrano nella scheda.

La misura sta in `simula_scontri.py` e `profili_draghi.py`, con 20.000 prove per
riga. Le tabelle complete sono in `ESITI-tabelle.md`; le stime e i limiti sono in
fondo a questo file.

---

## 1. Fauci di Palude (nero, GS 15), ARC-08 Hammerfist

Scheda: `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`, §1, tattiche alla riga 125.

**Carattere.** È un predatore di palude: paziente, sadico, si gode la paura
che semina. È l'erede di una ferita di famiglia, la cicatrice che l'ascia lasciò
sul capostipite. Non parla quasi mai.
**Obiettivo.** Fare di Hammerfist un messaggio di terrore per conto della Mano Rossa.
**Cosa sa.** Gli esploratori dell'orda gli hanno detto dove sono mura, balliste e
porte. Dei PG non sa niente finché Aegis Fang non canta (canone del 20/10). Dopo
il primo scambio vede da solo tre cose: chi vola, chi cura, e chi non trema (Thorik
ha il vuoto mentale).
**Le quattro domande.**
1. Essere cacciato davanti all'orda che guarda.
2. Lasciare Hammerfist in piedi.
3. Finire sulle mura in mezzo ai nani.
4. L'ascia, cioè Dragondoom e la cicatrice della stirpe.

**Cosa resta del canone.** La presa di Thorik com'è scritta (morso in
picchiata, salita, soffio con lui in bocca, caduta), «Portatore», l'Odio della
stirpe.

**Cosa propongo (solo incantesimi della scheda).**
- *Immagine speculare* prima di farsi vedere e di nuovo prima della picchiata.
  La scheda ce l'ha e il canone non la usa. Contro due guerrieri in mischia e
  una deflagrazione occulta è l'incantesimo che rende di più.
- *Dissolvi magie* su chi vola e potrebbe prendere Thorik al volo (Hella con lo
  Scudo del Custode, una pozione di *volare*). Solo se l'ha visto fare: la
  prima volta il trucco dei PG funziona.
- *Nube maleodorante* sui nani prima di scendere a finire Thorik, così i
  compagni nauseati non lo raggiungono. È la mossa diabolica: atterra quando
  nessuno può rispondere.
- Il soffio va sulla guaritrice: Hella tiene in piedi il gruppo, e Fauci la vede curare.
- **La fuga a un terzo dei pf (112) e non a 50.** Un drago con INT 16 non resta
  a terra a 60 pf in mezzo a una fortezza nanica: torna, ed è una nemesi più credibile.
- *Corrompere acqua* a volontà sulle cisterne di Hammerfist nelle notti
  dell'assedio: questo è terrore vero, ma tocca la trama ed è una scelta di canone (card).
- *Oscurità* (3 al giorno, raggio 21 m). Attenzione: nell'SRD 3.5 l'oscurità
  magica dà occultamento anche a chi ha scurovisione, quindi funziona anche
  contro i nani. Fauci la mette sulle balliste, non su di sé, perché la
  percezione cieca gli dice dove sono i bersagli ma non toglie l'occultamento.

**Tabella «se i PG...»**
| Se i PG… | Fauci… |
|---|---|
| stanno compatti a terra | soffio in linea su tre, poi nube |
| sono sparsi | soffio sulla guaritrice, *dardo incantato* non serve; aspetta che si raccolgano attorno a un ferito |
| volano con le pozioni | *dissolvi* su chi vola vicino a Thorik, mai su chi non lo minaccia (lezione di Skullcrusher) |
| sono invisibili (Mantello dello Svanire) | percezione cieca a 18 m: sa il quadretto, ma il 50% di mancare resta; soffia in linea sul quadretto |
| hanno *resistere all'energia* (acido) | lo vede dal soffio che morde poco, e passa a morsi in passata e nube |
| Thorik si aggrappa al collo (variante del 20/10) | atterra e rotola, come dice il canone |

**Misura** (T1 la classica, T1 sparsi, T2 tutti in volo, T3 con *resistere all'energia* e sparsi):
| | almeno un PG morto | drago ucciso | drago fuggito | danno al drago |
|---|---|---|---|---|
| canone, fuga a 50 | 48-59% | 2-3% | 49-73% | 268-298 |
| nuova, fuga a 50 | 7-47% | 0-1% | 51-84% | 249-296 |
| nuova, fuga a 112 | 5-34% | 0% | 69-95% | 214-240 |

La tattica nuova **uccide meno PG e muore meno**: è il risultato che il metodo
prevedeva. Un drago che ragiona non scambia pf con un PG. Il terrore lo fa nel
modo, non nel conto dei morti: la nube prima di atterrare, il soffio sulla
guaritrice, la fuga che lascia una nemesi viva. Se Jfs vuole più morti, la leva
è la soglia di fuga, non la tattica.

---

## 2. Tyrgarun (blu molto vecchio, GS 19), ARC-09 Rethmar

Scheda: `Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md`, tattiche righe 61-68.

**Carattere.** Aristocratico, freddo, sprezzante. È un alleato della Mano
Rossa, non un servo: il cielo di Rethmar è suo. Il blu ama le illusioni e le
voci false. **Obiettivo:** spezzare la volontà della città senza mai scendere.
**Cosa sa.** Da Fauci, se è sopravvissuto, o dai superstiti dell'orda, sa
dell'ascia che canta e del nano che non trema. Dalla Mano Rossa sa del Circolo
degli Otto, ma non sa che cosa farà il Mythal finché il cerchio non comincia a
chiudersi.
**Le quattro domande.**
1. Essere inchiodato a terra davanti a due eserciti: il Mythal è il suo incubo.
2. Il prezzo pattuito con la Mano Rossa.
3. Il cerchio che si chiude.
4. L'ascia.

**Cosa sbaglia il canone.** È uno stregone di 11° con *invisibilità
superiore*, *pelle di pietra*, *porta dimensionale*, *muro di forza*,
*telecinesi*, *velocità*, *dissolvi magie* e *fulmine*, e la sua tattica è «passate di soffio».

**Cosa propongo.**
- **Fasi 1-3, il terrore.** *Imitazione dei suoni* a volontà: dà ordini falsi
  con la voce dei comandanti («ritirata dal bastione est!»), e chi lo ascolta
  fa un TS Volontà per accorgersene. *Terreno allucinatorio* (1 al giorno) per
  una breccia finta. Passate di soffio da *invisibilità superiore*, ma la prima
  volta sola: quando vede una *luminescenza* o una polvere che lo segna, cambia
  settore e torna visibile.
- **Contro il Mythal.** *Pelle di pietra* all'alba (dura 110 minuti, tutta la
  battaglia). Quando il cerchio comincia a chiudersi lancia *immagine
  speculare*, poi colpisce chi tiene il focus con *telecinesi* (spinta
  violenta) o con un *fulmine* dall'alto.
- **Fase 4, a terra.** Il Mythal nega il volo, non lo scavare (6 m). Scava sotto
  la mischia ed esce dentro il cerchio. È la sola tattica che lo fa arrivare al
  focus senza passare dai nani.

**Misura, Fase 4** (con il −2 del Mythal a tiri e TS):
| | contro i soli PG, intatto | già ferito (250 pf), con alleati (STIMA) |
|---|---|---|
| canone | PG travolti, 59-80% almeno un morto | drago ucciso 23-45% |
| nuova | PG travolti, 66-84% | drago ucciso 0-1% |

**Questo è il risultato più importante del thread.** Il «GS effettivo 16-17» a
terra (riga 83 della scheda, riga 184 di STRUTTURA) non regge. Il Mythal toglie
il volo ma non il soffio da 20d8 con CD 30, e quel soffio da solo mette giù due
PG in due round. Il canone di oggi è battibile solo se Tyrgarun arriva ferito e
ci sono gli alleati. Con la tattica nuova non lo è nemmeno così. Quindi la
Fase 4 è una scelta di Jfs (card): scale e tattica vanno decise insieme.

---

## 3. Arbitrax / Abithriax (rosso giovane adulto, GS 15), ARC-09 altare campale

Scheda: `Bestiario/villain/arbitrax-drago-rosso-cr15.md`, tattiche righe 41-45.

**Carattere.** Il più giovane e il meno intelligente (INT 14). È vanitoso,
bullo e impaziente (Intimidire +29). Vuole farsi vedere dai sacerdoti della
Regina. **Obiettivo:** che il rito non si fermi, e tornare vivo dal suo tesoro.
**Cosa sa.** I sacerdoti gli hanno detto che i PG puntano ai focus. Se Fauci è
tornato, sa dell'ascia.
**Le quattro domande.**
1. Fallire davanti ai sacerdoti.
2. Il suo tesoro (fugge a 80 pf, come dice il canone).
3. Il Mythal.
4. Il freddo, a cui è vulnerabile.

**Correzione di regola, non di canone.** Riga 35 e riga 43: «vista cieca 18 m».
I draghi hanno la **percezione cieca** (SRD: sanno il quadretto, ma il 50% di
mancare un invisibile resta). La nota di Fauci lo dice già.
**Verificato:** *favore divino* e *cura ferite moderate* sono legali, perché il
rosso SRD lancia anche incantesimi da chierico e dei domini Caos, Male e Fuoco
come arcani (d20srd, «Dragon, True»).

**Cosa propongo.** Un drago diverso dagli altri: il bruto, con un difetto che i PG possono leggere.
- Il primo bersaglio è chi lo ferisce col freddo: lo sa, e lo teme.
- Si cura con *cura ferite moderate* sotto 150 pf.
- **Il difetto:** il primo nano che lo ferisce in mischia lo offende. Arbitrax
  atterra e lo schiaccia per due round, con l'attacco completo e poi il Colpo
  Terrificante. È l'apertura che un gruppo attento sfrutta.

**Misura:**
| | almeno un PG morto | drago fuggito |
|---|---|---|
| canone, PG senza preparazione | 51-86% | 16-64% |
| nuova, PG senza preparazione | 64-87% | 15-46% |
| canone, PG con *resistere all'energia* (fuoco) | **0%** | 100% |
| nuova, PG con *resistere all'energia* | 20% | 87% |

Un drago rosso riconoscibile si neutralizza con *resistere all'energia* 30,
che Hella può lanciare su tutti. Il canone non reagisce: soffia ancora, e i PG
non perdono nessuno. La tattica nuova si accorge che il fuoco non morde e passa
ai morsi su Artemis. Da sola, la reazione alla resistenza vale più di tutto il resto.

---

## 4. Ozyrrandion (verde adulto, GS 14), ARC-09 Torre Invisibile

Scheda: `Bestiario/villain/ozyrrandion-drago-verde-cr14.md`, tattiche righe 43-50.
È già la tattica migliore del gruppo: invisibile sotto la volta, *suggestione*
mentre Zalkatar tratta, soffio dall'invisibilità. Propongo solo il carattere, il
**tentatore**. Ha un patto con Zalkatar, non un debito: a metà scontro, se va
male, offre ai PG di tradire Zalkatar in cambio di una via libera e di un pezzo
del tesoro della Torre. Ha Diplomazia +32 e Raggirare +28, ed è vero a metà.
**Cosa sa:** molto. Sethrax ha visto il gruppo al Torneo e Zalkatar ha studiato
l'Anello di Artemis, quindi conosce lo stile di ognuno. È il solo drago che parte
informato, e deve sembrarlo: *charme* su Tordek, mai su Thorik (vuoto mentale).
Nessuna simulazione: la tattica cambia poco, e senza Zalkatar nel modello il numero direbbe poco.

## 5. Avatar di Tiamat (GS 17), ARC-09 finale

Scheda: `Bestiario/villain/Avatar_Tiamat/avatar-tiamat-cr17.md`, tattiche righe 41-44.
Il ritmo leggibile (due round di mischia e uno di soffio) è voluto dalla
Fase 3, e lo lascio. Propongo una sola cosa: è una dea, e il suo bersaglio è il
Mythal, non il PG più vicino. Tra un soffio e l'altro cerca chi tiene il cerchio,
come Tyrgarun, ma con l'aura e non scavando.

## 6. Regiarix (nero, Rhest) e il drago rosso dell'invasione di Dauth

Schede rifatte sull'SRD dopo la card del 15/11 (prima dicevano quanto segue).
- **Regiarix** (`09_.../Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md`, §2, righe 40-64):
  è «Grande, 22 DV», ma nell'SRD il nero adulto è Grande con 19 DV e il maturo
  è Enorme con 22. Le Armate lo danno «giovane adulto» con GS 10. Nessuna fonte.
- **Il drago rosso del Giorno 3** (`09_.../Arco-Post-Hammerfist-P2B-Torneo-STATBLOCCHI-COMPLETO.md`, §7, righe 157-181):
  è la cavalcatura dei Githyanki di Vaereth (MAPPE-COMPLETO-2 r.213), non uno
  dei cinque draghi della Mano Rossa. La scheda non torna: 25 DV sono quelli del
  rosso adulto maturo, non dell'adulto; For 37; manovrabilità «media» invece di
  scarsa; «fiuto», che i draghi non hanno. Tatticamente, atterrare al centro
  dell'arena (20,20) è il contrario di quello che fa un drago. Proposta: lascia
  i cavalieri e risale. È il solo drago che non sa niente dei PG, e lo si gioca
  solo su quello che vede.

---

## Stime e limiti (onesti)
- I PG sono quelli della carta del 05/11. I bonus d'attacco di Thorik e Tordek
  sono una STIMA (come per Skullcrusher); con +4 gli esiti cambiano poco (`ESITI-buff4.md`).
- Il modello non ha alleati, evocati, pozioni, quadretti né Durik. Gli alleati di
  Tyrgarun sono un'astrazione (40 pf a round, metà dei suoi round), una STIMA.
- «Vinto» vuol dire due PG a terra nello stesso round, cioè il gruppo si rompe.
  Nella scena vera i PG si ritirerebbero prima.
- Il focus del Mythal è Artemis (STIMA): il canone non dice chi tiene il cerchio.
- Le invocazioni di Artemis non sono nel repo. Se ha un modo di vedere
  l'invisibile, le passate invisibili di Tyrgarun valgono meno: è da chiedere a Jfs.
