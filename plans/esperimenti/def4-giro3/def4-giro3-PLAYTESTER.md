# Playtester a freddo — ARC07-DEF-4, giro 3

Bersaglio: `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
(3.403 righe, letto per intero in blocchi consecutivi, nell'ordine di gioco).
Rubrica: `skills/rumblingstone-playtest/references/playtester-a-freddo.md`.
Party simulato: Thorik, Tordek, Hella (druida 12), Artemis, APL 13, Durik al
seguito di Hella; capacità ricavate solo dal modulo. Le parti fra
`<!-- storico -->` sono state ignorate.

INPUT GAP: la rubrica rimanda a `sviluppo-degli-incontri.md` per le quattro
domande del developer; non l'ho aperto e ho usato solo le domande come sono
scritte nella rubrica.
INPUT GAP: non ho le schede dei PG. Classe di Artemis (invocazioni, «blast»,
Ali d'Ombra: sembra un warlock, `[Private source]`), razza di Hella (il modulo
la chiama «nana del sogno»; il brief dice umana), statblocco di Durik, Cintura
della Devastazione, Collana dei Semi e Mente Vuota sono noti solo per quello che
il modulo ne dice.
INPUT GAP: non ho aperto i file esterni citati come fonte di un numero che qui
manca: lo statblocco dei Treant in `DEF-3` §7, la tabella B4 «La Forgia
ricorda», il *Registro delle Perdite* di ARC-08, l'handout delle pozioni,
l'atlante con la griglia di M7-C (qui c'è solo l'SVG, di cui ho verificato
l'esistenza ma non il contenuto).
INPUT GAP: il log della serata del 25 settembre «sul ramo del gruppo» (fiducia
del consiglio, pozioni in mano) è fuori dal modulo e non l'ho letto (vietato
git). Ho usato il conto della fucina che il modulo riporta.
INPUT GAP: nell'SRD del repo (`skills/dnd-35-srd/references/`) non c'è la
tabella per età del drago nero né la tabella dei difetti degli oggetti
maledetti: i numeri di Skullcrusher li ho rifatti dalle regole (DV, modificatori,
CD = 10 + ½ DV + mod.), la riga 26-29 dei difetti non l'ho verificata.

## Rilievi

| # | Scena | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| 1 | 4 → 6 (e §8 B, C.1) | P-ECONOMIA | Per un gruppo nuovo i doni del consiglio hanno due versioni incompatibili, e il modulo lascia la scelta aperta. Dalla scelta dipende la matematica dello skill challenge (12 minuti d'invisibilità = due blocchi). Non è detto nemmeno se le 5 pozioni di *volare* «regalate dal re» arrivino anche con la fiducia dimezzata: senza di loro la variante dall'alto non esiste | 🟠 | Scena 4: «**fiducia piena**: 4 Pozioni di Invisibilità CL 12, le Benedizioni di Moradin +2/+2, la mappa accurata del campo». §8 B: «Scena 4 (il consiglio, se fiducia piena) · **Benedizione degli Antenati**: 4 **pozioni di *cura ferite gravi***». Scena 6: «Quale delle due versioni resta nel master per i gruppi futuri è una decisione del DM.» Banco: «Non si vendono: le **regala il re**, tramite il sergente» |
| 2 | 7 → 8 → ritorno | P-AZIONE | Balvar recuperato deve arrivare al cortile per sciogliere la Catena, ma il modulo prevede solo il ritorno a piedi. Col ritorno in volo, che è la via del gruppo che riprende stasera, non c'è risposta: Balvar non vola, Artemis porta «uno alla volta». A piedi, poi, «tira con loro» senza modificatori: lo statblocco non ha Nascondersi né Muoversi Silenziosamente | 🟠 | «Per arrivarci torna con i PG: nel ritorno a piedi tira con loro, alla postierla lo fa entrare Durin». A.4: «velocita: 6 m», abilità elencate: «Percepire Intenzioni +13, Concentrazione +19, Sapienza Magica +19, Conoscenze (storia) +19, Artigianato (incidere rune) +19» |
| 3 | 8 → 10 | P-AZIONE | Catturare Zog'tar è premiato, ma non c'è scritto come si porta un prigioniero Grande e in armatura di piastre per 1 km di campo. Mancano la prova di Nascondersi con il prigioniero, il peso per chi vola o lo porta e cosa fa se grida | 🟠 | «**Se Zog'tar è catturato** … Portarlo alle mura vale **un successo in più** nella prova della Scena 10.» A.2: «Grande · CM», «arm. completa di mithral +2» |
| 4 | 5 → 10 → 11 | P-RISORSA | I due Treant di Hella entrano in gioco all'alba con un mezzo statblocco: mancano danni, CA, velocità e durata, e il modulo non dice se possono venire nel cortile contro il drago. La giocatrice lo chiederà: è il «beat di potere della druida risorta» | 🟠 | «**due Treant di Adamantio** (statblock `DEF-3` §7: 90 pf, RD 10/adamantio, 2 schianti +18, danni doppi alle strutture) che caricano il fianco dell'orda». Scena 11, Hella: solo «le radici salgono dal cortile» |
| 5 | 11 / A.1 | P-RISORSA | Il template Avanzato dà +2 di armatura naturale, ma la CA non lo conta: l'armatura naturale dovrebbe essere +25, quindi CA 35, 39 con *armatura magica* e 43 per colpire la runa della Catena | 🟡 | A.1: «template **Avanzato** … (+4 a tutte le caratteristiche, +2 di armatura naturale)» e «CA 33 (−2 taglia, +2 DES, +23 naturale)». Scena 11: «colpirla è un attacco contro **CA 41**: la CA piena, 37 con l'armatura magica, più 4» |
| 6 | 8 / A.2 | P-RISORSA | Giavellotti di Zog'tar: BAB 15 + DES 5 − 1 taglia fa +19, e l'Ira non cambia la mischia a distanza | 🟡 | «A distanza: 3 giavellotti Grandi +20 in Ira (1d8+13)»; «BAB/Lotta: +15»; «DES 20» |
| 7 | 5 (rune di Zeth) | P-ECONOMIA | Il prezzo delle rune d'annullamento è calcolato su *dissolvi magie* di 3°, ma il modulo dice che Zeth è un druido, e per il druido *dissolvi magie* è di 4° (lo dice anche l'SRD del repo, `spells.md` riga 217): 4 × 9 × 25 fa 900 mo | 🟡 | «come una pergamena di *dissolvi magie* a quel livello, **675 mo** l'una»; «Nessuno in fortezza la sa lanciare: Moradin non dà il dominio della Magia, e Zeth è un druido» |
| 8 | 8 (Balvar) | P-RISORSA | Nell'SRD *comando superiore* concede un nuovo TS Volontà a ogni round. Il modulo lo fa «ripetere» per 13 round senza scriverlo | 🟡 | «Volontà **CD 20**, e si ripete ogni round per 13 round» |
| 9 | 5 (vendere) | P-ECONOMIA | Le regole generali di vendita (forziere fino a 10.000, pesatore a metà fino a 15.000) e la tabella giocata (Gunnvor paga **prezzo pieno**, 12.050 mo fuori dal forziere) danno risposte diverse per le armature naniche comuni. Per Gunnvor non c'è un tetto, e lei stessa dice che non paga in monete | 🟡 | «il resto (…) lo compra il pesatore **a metà prezzo, in gemme**, fino a **15.000 mo**» contro «Asce e balestre naniche comuni o perfette · Gunnvor · **prezzo pieno** SRD» e «Gunnvor 12.050»; GUNNVOR: «Stanotte non vendo. Scambio.» |
| 10 | §2 Zona 2 → 6 | P-CD | La prova per capire qual è la tenda del generale è protetta da una riga «non dire», ma Durin la regala alla postierla. Dalla mappa del campo data con la fiducia piena non discende nessun effetto scritto, salvo il −2 se manca | 🟡 | Zona 2, «🚫 Cosa NON dire»: «**Quale tenda è quella del generale.** Si deduce da dove *non* passano le pattuglie (Osservare CD 18)». Scena 6: ««La tenda nera al centro è del generale» · vero» |
| 11 | 6 | P-AZIONE | Non è detto se il conto dei fallimenti si azzera dopo la prima pattuglia. Al sesto fallimento ne arriva una seconda? | 🟡 | «**Tre blocchi falliti** prima dei cinque: **la pattuglia**.» / «Dopo lo scontro si riparte dal blocco in cui si era» |
| 12 | 6-8 (Grask) | P-AZIONE | Rubare o rompere il corno ha un esito scritto, ma nessun numero per spezzare la catena o la custodia (durezza, pf, Forza CD, Scassinare) | 🟡 | «la custodia è **incatenata al suo polso**»; «lo si lega, lo si addormenta o gli si ruba il corno»; «**Se rubano o rompono il corno**…» |
| 13 | 5-6-11 (Hella) | P-RISORSA | Le cariche dell'Evocazione dei Guardiani sono «del giorno», ma il conto mette la notte e l'alba sulla stessa giornata. Se all'alba si ricaricano, Durik richiamato alla tenda non costa niente al duello | 🟡 | «Costa **due** delle tre cariche del giorno»; «Richiamarlo prima, alla tenda, costa una carica … Con i due Treant dell'alba, che ne costano due, le cariche finiscono tutte e tre.» |
| 14 | 5 (fucina) | P-OROLOGIO | La pergamena di *identificare* si lancia in un'ora. Il modulo non dice se l'ora sta dentro la tacca della fucina o ne costa un'altra | 🟡 | «Si lancia in un'ora e brucia una perla da 100 mo»; «Tutta la trattativa costa **una** tacca» |
| 15 | 6 (lupi) | P-AZIONE | Il modulo non sa se Hella ha la stabilità dei nani. La regola dello sbilanciare resta aperta proprio sul PG più fragile | 🟡 | «(anche Hella, se la sua scheda di nana del sogno ha la stabilità)» |
| 16 | 7 | P-SPOTLIGHT | Nella trattativa con Balvar Thorik legge, Artemis vede l'aura, Tordek «arriva alla scaglia». Hella non ha niente: non capisce il nanico antico, e la scena non le dà una leva | 🟡 | «Fra i PG, i nani lo capiscono **a fatica** … Thorik lo **legge**»; «Artemis vede l'aura, Thorik legge il nanico antico, Tordek arriva alla scaglia» |
| 17 | 11 (cortile) | P-AZIONE | Spingere qualcosa nella fucina: non è detto con quale azione o prova, né se il «qualcosa» possa essere il drago Enorme in volo | 🟡 | «ci si può spingere dentro qualcosa. Il drago è **immune all'acido, non al calore della forgia**: 4d6» |
| 18 | 11 (corde) | P-AZIONE | Il meccanismo delle corde vuole tre ruoli: gancio dal camminamento, tiro a terra, colpo. Coi due nani alla corda e Artemis in volo, chi lancia il gancio non è detto, e nemmeno se possono farlo i nani delle mura | 🟡 | «**chi lancia il gancio** (sul camminamento, accanto alla gru)»; «**chi tira** (a terra, alla corda)»; «Così Thorik e Tordek hanno sempre un'azione» |
| 19 | §8 A | P-RISORSA | I PX delle Scene 6-8 (2.400) sono sotto il conto della stessa tabella DMG che il modulo usa per il drago: EL 17 contro il 13° vale 3.900 a testa, e il solo Zog'tar 1.950 | 🟡 | «Scene 6-8: il campo, Balvar, Zog'tar (GS 15) · combattimento veloce · 2.400»; «Il duello è al conto della tabella»; «Zog'tar (GS 15) circa 1.950» |
| 20 | 5 (pozioni) | P-RISORSA | La «brodaglia» è dichiarata di 2° livello e fa l'effetto di *eroismo*, che è di 3° | 🟡 | «Una pozione di 2° livello … fa l'effetto di *eroismo* per 10 minuti» |
| 21 | 8 / A.4 | P-RISORSA | Balvar ha una lista d'incantesimi senza slot al giorno. Il DM non sa quante volte può lanciare *dissolvi magie* su chi vola | 🟡 | «**Incantesimi** da chierico di 13° livello, **CD 15 + livello**: *dispel magic, magic circle against good, …*»; «*comando superiore* (5° livello, uno slot che aveva libero)» |
| 22 | App. C.2 | P-CD | La versione veloce di Zog'tar dà «−4 alla sorpresa» senza dire a quale tiro si applica, se la sorpresa non c'è più | 🟡 | «Se l'infiltrazione è fallita, è sveglio: −4 alla sorpresa, un solo scambio.» |
| 23 | 1 → 6 | P-OROLOGIO | Se il gruppo salta pattuglia e consiglio e va dritto al campo al tramonto, l'orologio non è partito (parte «dopo il consiglio»). Il modulo non dice da quante tacche si parte | 🟡 | «l'orologio della notte (§4) comincia a contare dopo il consiglio» |
| 24 | 2 | P-CD | I tre modi di farsi riconoscere valgono «se sinceri». Se i PG mentono sull'identità, o si nascondono alla pattuglia, non c'è una prova | 🟡 | «**Tre modi di farsi riconoscere** (tutti funzionano, nessun tiro se sinceri)» |

**Conteggio**: 🔴 0 · 🟠 4 · 🟡 20 · totale 24.

## Le scene, simulate

`Scena N · azione → risposta trovata / rilievo #`

- Scena 1 · arrivo e TS → risposta trovata (Volontà CD 20, −2 per 1d4 round, guarigione del passaggio) · Hella o Artemis volano a guardare il drago → risposta trovata («non attacca: aspetta l'alba») · vanno dritti al campo saltando il consiglio → rilievo #23
- Scena 2 · mostrano la Corona → risposta trovata (via A) · attaccano la pattuglia → risposta trovata (§6, CD +4 al consiglio) · mentono o si nascondono → rilievo #24
- Scena 3 · leggono la targa → risposta trovata (Fatto gratis) · Tordek guarda il cesello → risposta trovata (Mestiere, gratis) · nessuno prende il Nome → risposta trovata (torna alle Scene 4 e 13)
- Scena 4 · Diplomazia col re → risposta trovata (CD 20/16) · Intimidire → risposta trovata (stessa prova) · fiducia piena: cosa ricevono → rilievo #1
- Scena 5 · comprano e vendono → risposta trovata, banco con quantità, prezzi SRD verificati e tetti, ma rilievi #7, #9, #14 · cercano il chierico incappucciato → risposta trovata (era Vatore, cera nera) · dormono otto ore → risposta trovata (6 tacche, guarigione SRD) · Hella veglia i semi → risposta parziale, rilievi #4 e #13
- Scena 6 · attraversano a piedi → risposta trovata (cinque blocchi, CD 20/22, d6 di complicazioni), ma rilievo #11 · volano invisibili col *silenzio* → risposta trovata (1 tacca, numeri SRD giusti) · fermano il corridore → risposta trovata (Via B) · rubano il corno a Grask → rilievo #12 · lupi e sbilanciare → rilievo #15 · la tenda giusta → rilievo #10
- Scena 7 · entrano dalla soglia con un nano → risposta trovata (*epurare*, si passa alla Scena 8) · parlano con Balvar → risposta trovata (patto, nipote, Raggirare contro +13) · Hella in scena → rilievo #16
- Scena 8 · round di sorpresa → risposta trovata · combattono in volo sotto il telo → risposta trovata (portata 6 m, palo, *comando*), ma rilievi #6, #8, #21 · catturano Zog'tar → rilievo #3 · si torna con Balvar → rilievo #2 · Via A con la Corona → risposta trovata
- Scena 9 · parlano / derubano / feriscono Vatore → risposta trovata per tutte e quattro le righe, e per il passaggio invisibile
- Scena 10 · scelgono una delle tre vie → risposta trovata · Zog'tar vivo sulla breccia → risposta trovata (stringersi, caduta 1d6) · i Treant contano → risposta trovata (+1 successo), ma rilievo #4
- Scena 11 · chi non vola prepara un'azione → risposta trovata · corde delle gru → rilievo #18 · spingere nella fucina → rilievo #17 · colpire la runa della Catena → risposta trovata, numero sbagliato (rilievo #5) · due PG a terra → risposta trovata (§6, gli avi intervengono)
- Scene 12-13 · nessuna azione richiesta ai giocatori, salvo l'`[HDYWTDT]` dell'ascia → risposta trovata. Stasera non si giocano: la serata si ferma all'esito del duello
- App. C · versioni veloci → C.1 e C.3 rispondono; C.2 → rilievo #22, e anche C.1 ripete l'invisibilità del rilievo #1

**Le domande del developer, sui due scontri e sul campo.** *E se volano?* Hanno
risposta nella tenda, sulla breccia, nel cortile e sopra il campo. *E se sono
invisibili?* Rispondono le guardie (50%), i worg col fiuto, il drago con la
percezione cieca, gli sciamani dopo il corno e la runa della soglia. *Chi sente
il rumore, e in quanti round arriva?* Ronde in 1d4+2 round, squadroni in 2d4+2,
sacerdote in 1d4+1, drago in 70 round dal corno. *Il PG che non vola?* Ha la
sezione «Chi non vola», con il buco del rilievo #18. *Lo skill challenge dice
chi tira, cosa, e quanto costa un fallimento?* Sì: tutti tranne Durik, la prova
cambia con l'invisibilità, il fallimento costa +1 tacca e porta alla pattuglia
(resta il rilievo #11).

**`P-ABITATO` (Scena 5, la fortezza di notte).** Il modulo dice chi c'è per
ciascun ruolo: comando (Durin), culto (Brynja), rimedi (Kettra), armi
(Gunnvor), messaggi (assenti, ed è scritto), guardia (Hrodgar). Scrive le
quantità, cosa compra e a che tetto, e chi identifica, in quanto tempo e con
che prova. L'unico buco è il tetto di Gunnvor (#9).

**Numeri verificati con l'SRD, e che tornano.** Pozioni, pergamene e servizi
(*volare*, *invisibilità*, *cura*, *ristorare*, *rianimare morti*, *silenzio*,
*identificare*, Usare Oggetti Magici CD 21 e 23), la runa di *resistere
all'energia* (20, 70 minuti, 350 mo), la bomba di Kettra (5d6, CD 14, 750 mo),
*epurare invisibilità* (19,5 m, 13 minuti), il *glifo di interdizione* (5d8,
Cercare e Disattivare CD 28, *dissolvi* CD 24), *barriera di lame* e *uccidere
i viventi*. Il passo furtivo del nano (3 m a round, 360 m in 12 minuti), i
worg, la caduta di 4,5 m, i conti della fucina (47.967 e 28.364 mo, saldo 19.603
mo). Per Zog'tar tornano pf, CA, TS, Lotta, mischia e Colpo Devastante; per
Skullcrusher pf, soffio CD 28, Presenza CD 25 a 63 m, TS, RI 21, incantesimi
e schiacciare. I PX del drago (5.850, 1.460 a testa) sono giusti.

## Cosa la simulazione non ha potuto verificare

- Se il tavolo si annoia, e quanto durano davvero le scene rispetto ai minuti
  dichiarati: per stasera, le circa tre ore del §0.
- Le capacità reali dei PG: quante risorse di volo e d'invisibilità ha il
  gruppo oltre a quelle comprate, se Artemis può portare un nano in armatura,
  quanta Diplomazia e quanto Muoversi Silenziosamente hanno i nani. Lo skill
  challenge a CD 20/22 per nani in armatura pesante potrebbe dare molti più
  fallimenti del previsto: il conto delle tacche verso il giallo o il rosso
  dipende dai loro modificatori, che non ho.
- La griglia di M7-C, che nel modulo c'è solo come immagine: posizioni, il «telo
  a sinistra» (fianco est) e la distanza fra la soglia e il seggio.
- I numeri esterni: Treant (`DEF-3`), tabella B4, *Registro delle Perdite*,
  scheda di Durik, statblocco di Balvar oltre la copia in A.4 (BAB e livello
  d'incantatore del Runecaster sono `[Private source]`).
- La riga 26-29 della tabella SRD dei difetti degli oggetti maledetti (cura con
  la cera nera): la tabella non è nell'SRD del repo.
