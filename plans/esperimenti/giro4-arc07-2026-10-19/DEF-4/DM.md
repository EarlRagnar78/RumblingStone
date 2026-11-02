# Giro 4 · ARC-07 · DEF-4 — il DM a freddo della serata «La Notte e l'Alba»

Rubrica: `skills/rumblingstone-playtest/references/dm-a-freddo.md`, nelle tre
fasi. Materiale: il booklet `ARC07-NOTTE-E-ALBA-BOOKLET.manifest.json` nell'ordine
del manifest (intro, regia, Seme, cassetta, DEF-4, Forgia ricorda, Durik) e le
cinque pagine ✉ di `ARC07-NOTTE-E-ALBA-GIOCATORI.manifest.json`, controllate anche
nella forma stampata (`ARC07-NOTTE-E-ALBA-GIOCATORI.hb.md`). Stato vero del gruppo:
`stato-del-gruppo/sessione-4.md`, `state-ramo-di-gruppo.md` e le due patch del
2026-10-18 (Cintura a 4 cariche, Bane di Aegis Fang contro Fauci).

**Tempo di preparazione dichiarato: un'ora.** Dove l'ora finisce è il rilievo
O7. **Limite della corsa**: la vista di chi scorre l'ho letta io, non un agente
nuovo, e quella della regia dopo averla già letta per intero. Le risposte del
primo passo sono quindi più generose di quelle di un lettore davvero a freddo.
Il terzo passo l'ho fatto sul mio diario, senza `ricordo_lettura.py` su un
agente nuovo.

Il booklet stampato è allineato ai sorgenti di stamattina: la riga delle
wyvern (G2-15), lo stato di Grask (G2-29) e la Cintura a 4 cariche ci sono.
Le immagini e i fregi del manifest esistono tutti.

---

## Le tre domande del giro

**1. Struttura e ordine del booklet.** L'ordine dei capitoli è quasi quello in
cui il DM li usa stasera: regia, poi il Seme (la prima cosa che il tavolo
chiede), DEF-4 dalla Scena 5, la Forgia aperta durante la Scena 11, Durik
accanto alla giocatrice. Ci sono tre attriti. DEF-4 è stampato intero, con le
Scene 1-4 già giocate prima della Scena 5. Il suo §0 ha una **seconda
scaletta** («La vostra serata», lettura da 1 h 10) e una **seconda prima
battuta** (Durin, *«Quando uscite?»*) che la regia non nomina (O1, O7). Il
capitolo VI è una pagina ✉ della giocatrice stampata solo nel volume del DM
(Y12).

**2. La regia e lo stato vero del gruppo.** Le tre tacche, la fiducia piena,
il torque non consegnato, Hella risorta e il debito di Thorik ci sono e sono
giusti. Il conto delle tacche invece è fatto **a piedi**, e questo gruppo ha
la dotazione dall'alto: è il rilievo rosso (R1). Dell'inventario la regia
nomina solo *volare* e *invisibilità*. Mancano le rune d'acido, le tre
*velocità*, il *Vigore della Forgia*, i tre Doni di Hella e la pozione n. 10.
Mancano anche le richieste rimaste aperte al banco, che decidono il volo e il
Seme (O2, O3, O6).

**3. Gli handout ✉.** Con il canone e con il master sono coerenti, salvo una
riga sulle boccette (Y5). Ad alta voce reggono: tutti i riquadri stanno sotto
le 12 righe, e in ogni riquadro c'è al massimo un nome proprio nuovo, Gunnvor
compresa (Y7). Il guaio è la **consegna stampata**. La riga «leggilo ad alta
voce, la riga in fondo è solo per te» sparisce nella stampa, sostituita da «in
privato». Ma la regia fa leggere gli echi ad alta voce: un giocatore che legge
la pagina intera legge anche la riga privata (O9).

---

## Primo passo · la vista di chi scorre

`python3 scripts/vista_di_chi_scorre.py` sulla regia (`01-REGIA-SERATA.md`) e su
DEF-4.

| Domanda | Dalla vista della regia | Dalla vista di DEF-4 |
|---|---|---|
| 1 · la serata in tre frasi | le ultime scelte nella fortezza, il campo andata e ritorno, l'alba, stop sull'esito del duello (dalla tabella del §0) | la dice bene il riquadro «La serata in tre frasi», con la ripresa dalla notte a 3 tacche |
| 2 · chi si oppone, e cosa vuole | **non lo so**: la vista non nomina né Zog'tar né Skullcrusher, c'è solo «dalla postierla al drago» | Zog'tar e Skullcrusher; il drago combatte per un contratto inciso da un runaio |
| 3 · cosa preparo | echi, boccette, M7-C e M7-B. Le schede (A.1, A.2, A.4, Durik, Forgia) sono in una tabella, e la vista non le mostra | «la lista di lettura da un'ora e dieci, il dado dei caduti e i Treant di Hella». Della regia non dice niente |
| 4 · cosa mi ha fatto rispondere | la tabella del §0, finita per intero nel campo «La serata» | il riquadro del Quickstart |

| # | Passo | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| V1 | 1 | `D-AVVERSARIO` | la regia non nomina chi si oppone in nessun punto visibile | 🟡 | vista: «TITOLI … Regia della serata — dalla postierla al drago», nessun nome |
| V2 | 1 | `D-RUMORE` | grassetti di servizio nella vista della regia, e grassetti d'apparato in quella di DEF-4 | 🟡 | regia: «Cos'è. · 0 · I · II · III · Stop · Totale»; DEF-4: «MASTER DEFINITIVO … · Palio di Channathgate · Sostituisce e fonde» |
| V3 | 1 | `D-PREPARA` | le due viste mandano a due letture diverse, e nessuna delle due cita l'altra | 🟠 | vedi O7 |

---

## Secondo passo · la preparazione, voce per voce

| Codice | Esito | Dove, o quale rilievo |
|---|---|---|
| `P-RILIEVI` | fatto: ogni rilievo qui sotto ha la correzione in una riga | sotto |
| `P-GRUPPO` | rilievo: non è registrato chi porta cosa, cosa è stato comprato fra le richieste aperte, e se Thorik ha dato l'ascia a Thorgrim al consiglio | O2, Y8 |
| `P-MONDO` | fatto: Grask a 4ª/5ª tacca, il drago sulle colline, il corno, le ronde, l'orda che si sveglia all'8ª tacca. Tutto in DEF-4 Scene 6-8; la regia non ne porta niente | R1 |
| `P-STATO` | rilievo: le risorse del duello e i Doni di Hella non sono nel booklet | O6, Y13 |
| `P-STILE` | fatto: ritratti e tavola di Skullcrusher presenti; la regia non ricorda che i ritratti si mostrano dopo l'incontro | Y17 |
| `P-IMMAGINI` | fatto: nessuna immagine manca per stasera (`corredo.json`: «Nessuna immagine nuova») | — |
| `P-HANDOUT` | rilievo: manca un ✉ per il contratto del Seme, e la lavagna del banco (§9 n. 5) non è nel volume di stasera | O8, Y20 |
| `P-FLUSSO` | rilievo: due prime battute, due scalette | O1, O7 |
| `P-DOMANDE` | rilievo: tre domande prevedibili senza risposta scritta | O6, Y9, Y16 |
| `P-CONGEGNI` | rilievo: l'orologio è spiegato giusto in DEF-4 e conteggiato male nella regia | R1, O3 |
| `P-INTERAZIONI` | rilievo: Scudo del Custode ed Eco del Custode contro il soffio; Durik e la runa d'acido; la reazione dell'Anello se Artemis firma | O6, Y16, Y19 |
| `P-CONFINE` | rilievo: la riga «solo per te» degli echi esce stampata come pagina da leggere | O9 |

---

## I rilievi

### 🔴 Rompe la serata

**R1 · Regia §2 (e Seme, passo 3) · il conto delle tacche è fatto a piedi, e
questo gruppo vola.**
Prova, regia §2: *«Il campo a piedi ne costa almeno 3 […] e 3 + 3 fa 6 […] In
fortezza non avanza niente. Una tacca spesa qui porta a 7»*. E sul Seme:
*«Costa 1 tacca, e con il conto qui sopra porta a 7: si rientra di corsa. Dillo
prima che scelgano.»* La regia dice al DM di annunciarlo al tavolo con i numeri.
Ma il gruppo ha 5 pozioni di *volare*, Artemis vola a volontà e Hella vola da
aquila. In DEF-4 §4 il volo costa 1 tacca all'andata e 1 al ritorno («serve un
secondo *volare*»): sono 2 tacche, e si arriva a 5. Un'ora in fortezza (il Seme
**o** la veglia dei semi) porta a 6, cioè «≤ 6, in tempo». E c'è il
congegno che la regia non nomina. DEF-4 §0: *«Con 3 tacche segnate e il volo,
quando atterrano alla tenda Grask è sveglio […] Se prima Hella veglia i semi, il
volo è la 5ª tacca e Grask dorme.»* Spendere una tacca in fortezza **aiuta**
alla tenda. Il tavolo, a cui il DM ha detto «non avanza niente», rimanda il Seme
e la veglia, e arriva alla tenda con Grask sveglio. È la prima decisione della
serata, e la regia la sbaglia.
**Correzione**: riscrivere il §2 con due conti, volo (3 + 1 + 1 = 5, una tacca
libera) e piedi (3 + 3 = 6). Aggiungere la riga di Grask: la quarta tacca
segnata lo lascia sveglio, la quinta lo addormenta, e lo stato si fissa
all'atterraggio. Correggere allo stesso modo il passo 3 del Seme.

### 🟠 Il DM si blocca al tavolo

**O1 · Atto 0 e Atto I · chi parla per primo.**
La regia apre con il box dell'intro, gli echi e il Seme. DEF-4 §0, «La prima
battuta», apre invece con Durin: *«Si riapre nel cortile […] Durin li raggiunge
con la mappa del campo arrotolata sotto il braccio e chiede una cosa sola:
«Quando uscite?»»*. Nella regia Durin non compare mai, e il DM che apre DEF-4
§4, come la regia gli dice, trova un'altra apertura.
**Correzione**: nella regia §2, prima riga: *«Dopo gli echi, entra Durin: «Quando
uscite?». Poi il Seme.»*

**O2 · Atto I · le richieste aperte al banco e chi porta cosa.**
Sessione-4: *«Quali di queste il gruppo ha preso davvero non è scritto: ______»*
e *«A chi è andato ogni pezzo: non registrato al tavolo»*. DEF-4 Scena 5: *«Si
chiudono all'inizio della serata, dentro la tacca della fucina già segnata»*, e
§0: *«chi porta cosa si chiede al tavolo prima della Scena 6»*. La regia non dice
né l'una né l'altra cosa. Eppure la pietra di *silenzio* (160 mo, 8 minuti)
regge la variante dall'alto, e la pergamena di *identificare* (125 mo) è quella
che serve al Seme, che il capitolo II dà per già in mano («la pergamena del re»).
**Correzione**: un passo 0 nell'Atto I: chiudere la tabella «Le richieste rimaste
aperte» (DEF-4 Scena 5), poi far dire a ciascuno cosa porta; due minuti.

**O3 · Regia §1 e §3, intro · l'invisibilità a piedi è conteggiata male.**
Regia §3: *«il primo blocco a piedi lo coprono solo le due pozioni comprate; dopo
si tira Nascondersi CD 22»*. DEF-4 Scena 6: *«Una pozione comprata alla cappella
dura 3 minuti, circa 90 m: mezzo blocco. Non ne toglie uno, e il blocco in cui
finisce si tira a Nascondersi.»* Inoltre le pozioni d'invisibilità sono **tre**,
non due: le due comprate più la n. 10 delle boccette (3 minuti). E per quattro PG
non coprono comunque tutti.
**Correzione**: *«Le tre pozioni d'invisibilità (due comprate, la n. 10) coprono
mezzo blocco l'una: a piedi si tira Nascondersi CD 22 dal primo blocco.»*

**O4 · Regia §4 · le wyvern del duello.**
DEF-4 Scena 11, la tabella di scala: *«Un gruppo di 13° con la fiducia piena del
consiglio, tutti gli artefatti e il banco della fucina speso conta come
straripante: le wyvern ci sono [G2-15]»*. Questo gruppo ha tutte e tre le cose.
Le «tre cose da tenere davanti» della regia non le nominano, e le statistiche
delle wyvern sono solo dentro quella tabella, non in Appendice A. Contro i
valori SRD: il mirror `skills/dnd-35-srd` ha solo «Wyvern … CR 6», quindi 59 pf,
CA 18 e il veleno CD 17 sono **da verificare**.
**Correzione**: quarta voce nella regia §4: *«Dal round 2, due wyvern (DEF-4
Scena 11, tabella di scala) vanno su chi tiene la corda e su chi vola.»* E le
loro statistiche in A.1.

**O5 · Regia §4 e §6 · il dado dei caduti.**
Sessione-4: *«Quattro tiri sul Registro delle Perdite […] da fare alla Scena
10»*. DEF-4 Scena 10, «Dalla notte»: *«Si tira il dado dei caduti: 1d4 per ogni
tipo di cura comprata (per il gruppo del 25 settembre, quattro tiri)»*. La regia
§4 elenca «i Treant, il campo allertato, Zog'tar vivo o morto» e salta questa
riga, e il registro del §6 non ha la casella.
**Correzione**: nella regia §4 aggiungere *«e quattro tiri di 1d4 del dado dei
caduti: i nomi vanno fra i caduti del 372»*, e una riga nel registro.

**O6 · Regia §4 · le risorse del duello, e i Doni di Hella.**
Le risorse che decidono il duello non sono nella regia:
- le **2 rune di *resistere all'energia*, acido 20** (sessione-4, «Comprato»).
  DEF-4 Scena 5: *«Se la attivano uscendo dalla postierla, all'alba è scaduta:
  va attivata quando il drago compare»*;
- le **3 pozioni di *velocità***;
- il ***Vigore della Forgia*** (3 cariche per PG, 3d8+5) e la **Pelle di
  Pietra** (resistenza al fuoco 10), che durano 24 ore vissute dalla preghiera
  (§0-bis). Nessun documento dice quando il gruppo ha pregato all'Altare, quindi
  il DM non sa se all'alba ci sono ancora.
I **tre Doni** di Hella non sono in nessun capitolo del booklet: il *Scudo del
Custode* (1/g, prende dimezzato il danno di un alleato entro 9 m), l'Eco del
Custode (Thorik accelerato 3 round), la RD 3/adamantino e il *Rovo Eldritch*.
Stanno solo in `state.md` (righe 91-94 e 454), e il blast di Artemis ora è 6d6.
La domanda *«Hella usa lo Scudo su Durik contro il soffio?»* arriverà, e il
booklet non ha la risposta.
**Correzione**: un riquadro nella regia §4, «Cosa hanno in mano per il drago»:
rune, velocità, Vigore (con la riga «se la preghiera è oltre le 24 ore, niente»),
i tre Doni e il blast a 6d6.

**O7 · Preparazione · non entra nell'ora.**
DEF-4 §0: *«Leggi solo questo, in quest'ordine, in un'ora e dieci minuti»*, più
*«altri 10 minuti di lettura, da fare prima della lista»*. A questo si sommano
la regia (9 minuti, dice la vista), il Seme, la Forgia e Durik: circa un'ora e
tre quarti. Con un'ora, seguendo la lista di DEF-4, il DM si ferma alle Scene
7-8. Vatore, la tabella «Dalla notte» e il duello restano da preparare. La
regia non cita la lista di DEF-4, e la lista di DEF-4 non cita la regia: sono
due scalette per la stessa serata.
**Correzione**: una lista sola, nella regia §1, che sostituisce quella di DEF-4
per questo gruppo e sta nei 60 minuti. Si può togliere la Scena 6 a piedi, perché
il gruppo vola.

**O8 · Il Seme, passo 5 · il contratto si legge a voce, e non ha un foglio.**
Prova: *«Il DM legge le clausole 1-8 a voce, nell'ordine, poi la firma della
bottega.»* Le otto clausole sono circa 35 righe, il triplo del tetto di
`read-aloud-adulti.md` §2 (*«Oltre le 12 righe l'attenzione cade»*). E un tavolo
che deve decidere se firmare vorrà rileggerle. DEF-4 Scena 5 ha già la versione
«In breve», di un paragrafo.
**Correzione**: un ✉ «Il contratto del Seme», con le clausole 1-8 e la firma
della bottega e niente sul creditore. A voce si legge solo il box finale.

**O9 · Pagine ✉ degli echi, consegna stampata · la riga privata finisce letta
ad alta voce.**
Sorgente: *«Il DM ti chiede di leggerlo ad alta voce; la riga in fondo è solo per
te.»* Nella stampa (`ARC07-NOTTE-E-ALBA-GIOCATORI.hb.md`, righe 29, 56, 82, 107)
quella frase sparisce e resta solo *«Pagina da consegnare al giocatore indicato,
in privato.»* La regia §1 dice invece *«Li fai leggere ad alta voce all'inizio
dell'Atto I»*. Il giocatore di Artemis legge la pagina intera, e la riga che
dovrebbe tenere per sé va a tutto il tavolo: *«Nel campo c'è qualcuno che, come
voi, non è di qui.»*
**Correzione**: nella regia §1, *«leggete ad alta voce solo il riquadro; la riga
in grassetto è vostra»*. Oppure separare la riga «Solo per te» dal riquadro
nella pagina stampata.

### 🟡 Migliorabile

| # | Dove | Prova | Correzione |
|---|---|---|---|
| Y1 | regia §0 | colonna «Tre ore», *«Totale: circa 3 ore e 25»* | dire quali 25 minuti si tagliano: il Seme rinviato al 1372, o C.3 dal primo round |
| Y2 | intro N4, regia | *«Durik è sempre presente»*; DEF-4 Scena 6: *«Durik non tira: è alla postierla o nel seme»* | *«sempre, tranne nel campo: postierla o terzo seme»* |
| Y3 | ✉ boccette, consegna | *«passa la mano sulla sola che ferma Kettra»*; sessione-4: *«due la fermano, la brodaglia (n. 2) e la cura con la cera nera (n. 4)»* | allineare il log o l'handout (il master dice una) |
| Y4 | ✉ boccette, stampa | riga 133: *«Pagina da consegnare al giocatore indicato, in privato»* per una pagina *«Per tutto il tavolo»* | etichetta «a tutto il tavolo» |
| Y5 | ✉ boccette | *«Read-aloud (Mercer lead)»*, *«(Tolkien lead)»*, *«(Andor lead)»* stampati sulla pagina dei giocatori | togliere le etichette dei pilastri dalla pagina ✉ |
| Y6 | ✉ boccette | *«E qualcuno di voi l'ha presa a un goblin della Mano Rossa: la ricetta ha mille anni»* | la conclusione la tira il tavolo (DEF-4: «chi l'ha presa… scopre»): lasciare solo la frase di Kettra |
| Y7 | ✉ Tordek | *«quando Gunnvor apre la bocca della forgia»*; DEF-4 Scena 5: il capo fabbro è *«inventato al momento»*, e il tavolo l'ha conosciuto senza nome | *«quando la capo fabbro apre…»* |
| Y8 | ✉ Thorik | *«con la stessa nota che fa quando la batti sull'incudine per raddrizzarla, solo più bassa, e non sei stato tu»*: tre livelli di subordinate (§1 punto 2). La riga privata presuppone come è andato il gesto dell'ascia al consiglio, che sessione-4 non registra | spezzare la frase; chiedere al DM se Thorik ha porto l'ascia a Thorgrim |
| Y9 | ✉ Tordek | *«Stanotte, se parlano, ascoltali fino in fondo: non tutto quello che porti è venuto qui per combattere»*; il Seme: *«I Bracieri […] non commentano»* | una riga nella regia su cosa dicono i Bracieri se Tordek li interroga, o togliere l'invito |
| Y10 | cassetta | mancano dal cast e dalla pronuncia Kettra, Brynja, Gunnvor, Grask, Hrodgar, Hald; *«Le mura all'alba (DEF-4 scena 4)»*, *«Il duello (DEF-4 §4)»*, *«Thorgrim consegna il martello (scena 2)»* | aggiungere i sei; rimandi alle Scene 10 e 11; «l'ascia», Scena 4, già giocata. Il momento di stasera è il finisher del duello |
| Y11 | Forgia ricorda §1 | *«Dalla Scena 5 del duello si registrano due dati»* (numerazione del vecchio P5, stasera la Scena 5 è la fortezza); *«numero di colpi andati a segno»*: con un gruppo di 13° N = 3 al secondo round | «Scena 11 di DEF-4»; dire che N arriva a 3 quasi sempre |
| Y12 | capitolo VI | la scheda di Durik ha la consegna *«Per la giocatrice di Hella»*, ma è stampata solo nel volume del DM | metterla anche nel volume dei giocatori, o scrivere nella regia che la giocatrice ha la sua copia del 25 |
| Y13 | regia, Hella | la patch del 2026-10-18 fissa per Hella la guarigione rapida 1 su terra o pietra, sospesa il round dopo un danno da fuoco; il booklet non lo dice, e l'orda ha incendiari (DEF-4 §1) | una riga nel riquadro di O6 |
| Y14 | Scena 5 | sessione-4: *«19.603 mo […] D43 non lo applica»*; DEF-4: *«ne servono circa 21.800 [G2-56]»* | il DM sceglie, perché stasera le richieste aperte si pagano in monete |
| Y15 | DEF-4 Scena 5 | *«Quella che il tavolo ha comprato di sicuro è una runa»*; il conto, poco sotto: *«Runa di resistere all'energia […] 2»* | «le due rune» |
| Y16 | Scena 11, Durik | runa d'acido 20 su Durik vulnerabile (+50%): se la resistenza si toglie prima o dopo l'aumento, il mirror SRD del repo non lo dice. **Da verificare** | scriverlo nella riga 4-bis |
| Y17 | regia §0, immagini | Balvar e Zog'tar sono *«i ritratti sotto le loro schede d'entrata»*; DEF-4: *«Ai giocatori si mostra dopo l'incontro, non prima»* | aggiungere «dopo l'incontro» |
| Y18 | regia §6, registro | mancano: chi ha bevuto la n. 4 (il segno che Vatore vede), dove sono andati i Treant, il corno (rubato o suonato), Balvar portato dentro e Hald, i caduti del dado | quattro righe nel registro |
| Y19 | Seme | *«Il DM sceglie il tono in base a come Artemis ha gestito finora la propria avidità»*: A o B non è deciso, e serve se Artemis firma stasera | il DM sceglie prima della serata |
| Y20 | DEF-4 §9 | *«Il banco della fucina, nel volume dei giocatori: la lavagna di Gunnvor»*; non è nel volume di stasera, e le richieste aperte si chiudono stasera | aggiungerla al manifest dei giocatori, o dire che non serve |
| Y21 | regia §3, Scena 9 | *«Dieci minuti, al ritorno»*: niente sul ritorno in volo, il caso probabile; DEF-4 l'ha già scritto: *«Se tornano in volo […] Vatore è sulle mura all'alba»* | una riga |

---

## Terzo passo · il giorno dopo, al tavolo

Fatto sul mio diario, senza un agente nuovo (limite dichiarato in testa).

- **Chi entra per primo, e cosa dice?** Due risposte: secondo la regia il DM
  stesso, con il box dell'intro e *«Questo è quello che vi è rimasto addosso
  della notte»*; secondo DEF-4 Durin, con *«Quando uscite?»*. È O1.
- **Se i giocatori chiedono «quante tacche ci costa il Seme, se voliamo?»**: la
  risposta giusta (si arriva a 6, in tempo, e Grask dorme se l'ora del Seme
  viene prima del volo) è in DEF-4 §0 e §4. Quella della regia è sbagliata.
  È R1.
- **Dove sono dovuto tornare indietro**: dalla regia a DEF-4 §0 per Grask e
  per la prima battuta; da DEF-4 Scena 11 a `state.md` per i Doni di Hella, che
  nel booklet non ci sono. Al tavolo sono un minuto ciascuno: sopra la soglia
  dei 30 secondi.

Il diario ha una cosa che il master non ha: l'ordine di Durik e della runa
d'acido sul soffio. L'ho segnato come da verificare, non come canone.

---

🔴 1 · 🟠 10 · 🟡 23
