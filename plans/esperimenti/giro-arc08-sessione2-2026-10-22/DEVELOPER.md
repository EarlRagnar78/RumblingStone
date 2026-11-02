# DEVELOPER · lettura a freddo di ARC-08 Sessione 2 «Tre giorni di sangue e ferro»

**Chi sono.** Developer di incontri a freddo (domanda del developer: «si gioca?»).
Non ho visto altri rapporti del giro e non conosco il repo.

**Cosa ho letto**, tutto in `freddo/`: `SESSIONE-2.md` (1582 righe, per intero),
`LIBRETTO.md`, `SEGRETI-DM.md`, `HANDOUT-GIOCATORE.md`, e la rubrica
`sviluppo-degli-incontri.md` (§1-§17 e «Come si scrive un rilievo»). In
`freddo/` ci sono anche `dm-a-freddo.md`, `lettore-a-freddo.md` e
`playtester-a-freddo.md`: sono rapporti di altri ruoli, **non li ho aperti**. Python
solo per calcoli e simulazioni, con dadi veri: `calc.py` nello scratchpad della
sessione, nessun file letto fuori da `freddo/`.

**Scostamenti dalla rubrica, dichiarati.**

1. Niente web, quindi niente URL del mirror SRD. Le regole che cito (SRD 3.5)
   vengono dalla memoria; dove un rilievo dipende da un testo che non ho potuto
   rileggere lo scrivo (`a norma 3.5`, «da verificare»). La *prova* è sempre
   una citazione dal master.
2. «Esiti V/S/R» non è definito nella rubrica che ho. L'ho letto come
   **V**ittoria · **S**confitta · **R**itirata (o resa).
3. I numeri di riga sono quelli di `SESSIONE-2.md`; per gli altri file scrivo il
   nome (`LIBRETTO.md:riga`).
4. Le simulazioni sono modelli semplici (attacco completo, niente Attacco
   Poderoso né cure, un solo bersaglio): servono per l'ordine di grandezza, non
   per il decimale. Le cifre sono arrotondate.

---

## Tabella-quadro · ogni incontro contro la sua scheda

Segni: ✅ regge · ⚠️ regge con riserva (rilievo in tabella) · ❌ manca o non regge.
«Esiti» dice se V, S e R sono tutti scritti e se i dadi possono davvero
produrli.

| Incontro | Scopo | Posta | Statistiche | Tattiche | Terreno | Esiti V / S / R |
|---|---|---|---|---|---|---|
| **S1** alba e leve (`:408`) | spiegare la serata, leggere le leve di S1 | niente: apparecchia | n/a | n/a | n/a | n/a. ⚠️ 15' per 12 leve + 10' di libretto + scelte (D-R37) |
| **S2a** Giorno 1, libretto (`:497`) | primo assedio a reparti | tacche, brecce, morale, 2 trappole spese | ✅ i numeri dei reparti tornano fra §0-bis, libretto e segreti | ✅ carte per round | ✅ | V (nessuna breccia) ✅ · S (breccia, riserva) ✅ · R: non c'è, giusto |
| **S2b** Gorthak + 2 troll sul ponte (`:527`) | il duello al cancello | +2 morale, metà dei pf del cancello, `Comandanti logorati` | ⚠️ sei colpi per ettin senza i talenti (D-R3); ariete fa 12 round, non 7 (D-R4); GS 12 non derivabile (D-G1) | ✅ round per round, soglia 101 | ⚠️ ponte 6×7,5 m, fossato, sportello: il fossato non lo usa nessuno (D-R7) | V ⚠️ (Borin da solo: ~metà delle volte cade prima, D-R2) · S ❌ non scritta (che succede a un PG a 0 pf sul ponte?) · R ✅ fuga di Gorthak |
| **S2c** il sorvolo (`:606`) | far vedere il drago, 1 pf del morale | +1 morale se un eroe lo ferisce (15%) | ⚠️ CA 37 dichiarata, 2 eroi su 4 «niente» (D-R9) | ✅ un passaggio | ✅ | V (colpo a segno) ~15% · S n/a · R: il drago se ne va, sempre |
| **S3** notte 1 (`:733`) | conto, recuperi | pf del cancello, morte di un pregen | ⚠️ aritmetica del cancello (D-R12) | n/a | n/a | n/a |
| **S4a** Giorno 2, libretto + Cantitrici (`:782`) | tenere le Mura | Cantitrici: `pieno/parziale/fallito` | ⚠️ «fallito» non toglie il Coro (D-R15) | ✅ | ✅ rampa | V ✅ · S ⚠️ costo lieve · R n/a |
| **S4b** Grimjaw + 4 orog alla breccia (`:833`) | il comandante che fugge | +2 morale, `Comandanti logorati` | ⚠️ EL ~15 contro un PG (D-R2) | ✅ round per round | ⚠️ caduta di 12 m: nessuno la usa (D-R7) | V ⚠️ (con 1 PG solo ~100% di sconfitta nel mio modello) · S ❌ non scritta · R ✅ «sotto 89 fugge» + variante del Re |
| **S5** notte 2 (`:952`) | il Re annuncia | decisione del Re (fissa) | n/a | n/a | n/a | n/a |
| **S6a** Giorno 3, cancello (`:1004`) | il crollo | morale, `Posizioni tenute` | ⚠️ D-R23 (round 3-4: chi tira cosa) | ✅ | ✅ | V/S/R ⚠️ tabella dei bonus c'è |
| **S6b** il soffio sulla 2B (`:1038`) | salvare il Re | Re vivo con 8 pf (canone), Borin, pf del drago | ❌ niente attacchi in mischia di Fauci (D-R20); breath+carica nello stesso round (D-R19); Borin B all'1-15% (D-R16) | ⚠️ sequenza a 4 round ottima; le opzioni sono 1 su 3 vive | ✅ 2B-CORRETTA, quote date | V ⚠️ `protezione` lo azzera (D-R18) · S ✅ Re morto, §8 · R ❌ il drago atterra solo con >50 danni, che il gruppo non può fare (D-R10) |
| **S7** la ritirata (`:1177`) | far passare 90 nani | nani salvi, Re, Dana | ❌ orde senza statistiche (120 dalla Porta) | ❌ nessuna | ✅ H3-1 non vista | V/S/R: ❌ nessun tiro, l'esito esce dall'assegnazione dei posti (D-R25) |
| **S8** l'incrocio silenzioso (`:1241`) | l'imboscata al Re a 8 pf | Re, nani caduti, 2 PG paralizzati | ⚠️ A.7: IUD vs flanking (D-R32), CD 16 (D-R41) | ✅ per i bugbear, ⚠️ per chi li affronta | ⚠️ buio vs scurovisione (D-R30) | V ⚠️ 92% svelata (D-R29) · S ✅ Re morto, §2 di ARC08-10 · R ✅ bugbear svaniscono sotto 4 |
| **S9** la porta (`:1342`) | chiusura | scheda | n/a | n/a | n/a | n/a |

**Budget (EL contro APL 12,25: Borin 13, gli altri tre 12).** Rifatto con la
tabella della DMG (somma di unità a 2 CR = doppio):

| Scontro | Dichiarato | Rifatto | Lettura |
|---|---|---|---|
| Gorthak GS 12 + 2 troll GS 5 | ~13 | **12,5** | APL +0,5: onesto *per quattro* |
| Grimjaw GS 14 + 4 orog GS 7 | ~15 | **14,9** | APL +2,5: duro per quattro, non per uno |
| 8 bugbear GS 9 | 15 | **15,0** | APL +2,8 |
| 8 bugbear + 7 hobgoblin GS 5 | non scritto | **15,6** | gli hobgoblin non spostano il totale |
| Fauci GS 15 + cavaliere GS 10 | non scritto | **15,5** | nessuno lo combatte, per scelta |

I tre EL tornano. Il problema non è il conto: è **chi lo gioca** (D-R2).

---

## Rilievi

| # | Scena | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| D-R1 | 2, 4 | §1 · manca | I due duelli hanno **un PG in scena e tre fermi**: 25' extra a Gorthak, 30' a Grimjaw. Per partecipare gli altri devono lasciare il settore, che «prende le tacche»: la scelta è fra annoiarsi e perdere un muro. Non c'è un modo di tenere gli altri tre in gioco (il loro round di battaglia, per esempio, giocato in parallelo mentre il duello è sulla mappa). | 🟠 | «Un eroe di un altro settore può unirsi al duello lasciando il suo, che in quel round tira senza di lui **e prende le tacche**» (`SESSIONE-2.md:559`); «gli altri possono unirsi come per Gorthak, lasciando il loro settore alle tacche» (`:871-872`); «25 minuti di libretto, più 25' se si sfida Gorthak» (`:117`) |
| D-R2 | 2, 4 | §0 · altro (EL) | I due EL sono dimensionati **per quattro PG** e il testo mette in scena **uno**: Borin ha «il duello sul ponte» (§1, `:285-286`). Simulato con le statistiche dell'Appendice A (Borin CA 25, 142 pf, attacco completo, trolli dal round 2): **Gorthak + 2 troll, Borin solo: Borin cade prima della fuga di Gorthak il 52% delle volte** (63% di fuga di Gorthak con quattro colpi); con Dara dalla torre +19/−2 la sconfitta di Borin scende a 2%. **Grimjaw + 4 orog, un PG solo: sconfitta ~100%** (ogni orog +13/+8 1d12+10, Grimjaw in Furia +24/+19/+14; ~85 danni a round contro CA 25): con Dara e un colpo infuocato di Thorin Grimjaw fugge l'81% delle volte, in ~2 round. Il master non dice che il duello va giocato in più eroi, né quanto costa giocarlo da soli. | 🟠 | «Il duello sul ponte è suo, se lo vuole» (`:284-286`, §1 Borin); «contro uno solo sono quasi impossibili: per questo il libretto fa fuggire i comandanti a metà» (`:198-199`); ma la fuga è a 101/89 pf e **c'è una guardia da 63 pf davanti**: «chi vuole colpire Grimjaw in mischia deve prima superarne uno» (`:880`) |
| D-R3 | 2 | §17 · regola | Gorthak ha **sei attacchi**, tre per mano, tutti al massimo del suo bonus. A norma 3.5 la mano secondaria dà **un** attacco in più (tre servono Combattere con Due Armi Migliorato e Superiore, che richiedono Des 15/19; l'ettin ha Des 8 di serie, a memoria). Il «Superior Two-Weapon Fighting» dell'ettin toglie solo le penalità. L'Appendice non elenca quei talenti. Con quattro colpi (+21/+16/+11 e +21) l'uscita di Gorthak passa da ~52 a ~40 danni a round. | 🟠 | «due randelli +21/+16/+11 (2d6+10 e 2d6+5)» (`:187`); «randello Enorme +1 +21/+16/+11 … e … +21/+16/+11, senza penalità per le due armi» (`:1522`); «Allerta, Iniziativa Migliorata, Attacco Poderoso, Incalzare, Spezzare Migliorato, Volontà di Ferro» (`:1522`); «sei colpi» (`:573`, `:697`) |
| D-R4 | Zona 1 | §17 · regola | Il tempo che l'ariete impiega a sfondare il cancello non torna. 3d10+20 fa **36,5** di media, non 32; tolta la durezza 20 restano **16,5** a round, quindi **12 round** per 200 pf, non «circa sette». Se «32» era già netto, 3d10+20 è sbagliato; se è lordo, i sette round sono sbagliati. Il ritmo vero del cancello è comunque in round di battaglia (1 minuto = 10 round), e a questo ritmo il cancello cadrebbe il Giorno 1. | 🟡 | «3d10+20 a round, 32 di media meno la durezza: se ci si accanisce, lo sfonda in circa sette round» (`:357-359`) |
| D-R5 | 2 | §17 · regola | La discesa dalla piattaforma non dura due round. Scalare una corda annodata è un quarto della velocità per azione di movimento: a un'azione di round completo, **metà**. Borin (6 m): 3 m a round, **5 round** per 15 m; Dara (9 m): 4,5 m, **3-4 round**. | 🟡 | «Scalare CD 0, a un quarto della velocità: due round per i 15 m» (`:566-567`) |
| D-R6 | 2, 4 | §17 · manca | **CA e pf di ogni bersaglio.** I giganti sono un bersaglio dichiarato (Dara tira per cancellare il macigno) e non hanno CA né pf; la distanza è 50-100 m e Dara ha incrementi di 30 m (da −2 a −6, a 100 m più il 4° incremento); gli adepti della palla di fuoco non hanno né statistiche né un nome in Appendice. | 🟠 | «Dara può tirare … contro i giganti al gomito … +23 contro la loro CA … se colpisce il macigno di quel round … non parte» (`:518-523`); «otto giganti … a 50-100 m dalle mura» (`:524-525`); «la palla di fuoco … gli adepti dalla strada» (`:507`) |
| D-R7 | 2, 4 | §12 · manca | **Ogni pericolo della mappa ha un nemico che ci spinge dentro i PG, e i PG lo usano?** Nessuno. Il fossato (3 m, Nuotare 15) è citato nel box PF1e come uso di Spingere per Gorthak (+4), ma le tattiche di Gorthak non spingono mai. Gli orog di Grimjaw non spingono dalla breccia (caduta di 12 m, 4d6). Il ponte da 80 pf non è un'arma (lo si taglia con Gorthak sopra?). Sono scenografia: vanno nel box, non nelle tattiche, oppure qualcuno li usa. | 🟡 | «Sul ponte Gorthak ha +4 contro un nano: chi finisce nel fossato nuota (CD 15)» (`:253-255`); tattiche di Gorthak: round 1-3 e «sotto 101» senza spinte (`:693-705`); «dentro, una caduta di 12 m nel cortile (4d6)» (`:1580`) |
| D-R8 | 4 | §8 · manca | La carta di Gorthak del Giorno 2 non dice cosa fare se Gorthak **non è mai stato sfidato** (pf pieni, nessuna fuga) né se è fuggito con pf ≤ 101+15. «Fuggito ma sopra metà»: al Giorno 2 ha pf = (fuga < 101) + 15, quindi la condizione si avvera solo per chi è scappato fra 87 e 100. | 🟡 | «**Gorthak al cancello**, se è fuggito il Giorno 1 ma ha i pf sopra metà; se no, **la palla di fuoco**» (`:826`) |
| D-R9 | 2 | §1 · manca | Al sorvolo **Borin e Nala non fanno niente**, dichiarato. Nala ha *velocità*, *immagine silenziosa* e *Ispirare Coraggio* sulla scheda, e potrebbe fare qualcosa (un'illusione che attiri il soffio altrove). Cinque minuti, quindi 🟡. | 🟡 | «**Borin e Nala**: niente che arrivi a 45 m, salvo il martello lanciato di Borin, che non ha» (`:647-648`) |
| D-R10 | 6 | §5 · regola | Il «boss che cambia» di Fauci (atterra sopra i 50 danni, sale sotto ~230 pf) **non scatta mai**. Dara ha +21 contro CA 37: ogni freccia colpisce con 16-17+ (20-25%), con −4/−6 di distanza (D-R21) con 19-21 (5-10%). Per più di 50 danni (1d8+8, media 12,5) servono **4 frecce a segno**: con Tiro Rapido (+19/+19/+14/+9 contro 37) ogni freccia è un 20 naturale; nei due round utili la probabilità è ~0. Le due frecce assassine (Tempra CD 20 contro +21) uccidono solo con un 1 naturale: ~1% a freccia, con il colpo a segno incluso. «Il tiro impossibile» (§1) è impossibile davvero. Tutti i rami «se atterra» (Tattiche, Contingenze, Echo) sono testo morto. | 🟠 | «Se Dara colpisce Fauci per **più di 50 danni in tutto**, al round 5 il drago atterra su un bastione» (`:1101-1103`); «Fauci ha Tempra +21: muore con un 1 naturale» (`:1099`); «il tiro impossibile» (`:296-297`); «se atterra su un bastione: attacco completo» (`:720`); «se è atterrato su un bastione, è la mappa: 337 pf» (`:1421`) |
| D-R11 | 2 | §0 · altro | La scelta fra baliste A e B è inutile: le baliste hanno **+16** contro CA 37, cioè solo il 20 naturale (5%), e 3d8+10 contro 337 pf. Non cambia niente al tavolo (né il morale, che chiede un colpo a segno). | 🟡 | «+16 (il +18 della MAPPA 3, −2) contro CA 37, 3d8+10» (`:661-662`) |
| D-R12 | 3, 5 | §17 · regola | I pf del cancello non tornano fra le righe. Partenza 200; Giorno 1 −80 = 120; la notte aggiunge **+20** (`:765-767`) = 140; Giorno 2 −80 = 60; seconda notte +20 = 80. Scena 5 e Scena 4 parlano invece di **40** («−80, a 40»). Canone: il cancello cade il Giorno 3 in ogni caso, quindi non blocca, ma il tavolo che conta i pf trova tre cifre. | 🟡 | «−80 il Giorno 1, −80 il Giorno 2» (`:356`); «nella notte valgono **+20**» (`:766`); «Il cancello ha 40 pf, o quelli che i dadi hanno lasciato, più le riparazioni» (`:966`) |
| D-R13 | 4 | §8 · manca | «Superare» una guardia non è definito: uccidere, spostarsi, o basta non averla in mezzo? Gli incantesimi (*colpo infuocato*) e le frecce di Dara dall'alto saltano la guardia o no? Dal modello: se vale solo la mischia, il duello di Borin da solo è un'esecuzione, se valgono le frecce e gli incantesimi il pericolo svanisce. | 🟡 | «guardia del corpo: chi vuole colpire Grimjaw in mischia deve prima superarne uno» (`:880`) |
| D-R14 | 0, 4 | §9 · contraddizione | La riga di *comunione* sul settore di Grimjaw («il DM sceglie lo stesso … dopo il round 1») dice il contrario della regola della scena («Grimjaw … nel settore che ha preso più tacche ieri … a pari, la Torre Est»), che si decide **al round 1** e senza il DM. | 🟡 | «il DM sceglie lo stesso il settore di Grimjaw dopo il round 1 (Scena 4)» (`:156`); la tabella del Giorno 2, round 1: «Grimjaw e la guardia nera, nel settore che ha preso più tacche ieri o che ha meno reparti» (`:824`) |
| D-R15 | 4 | §0 · contraddizione | Le Cantitrici «cadute» non incidono. Sono cinque; se le Mura cedono entro il round 3 «ne cadono due» e il Coro «si perde quando ne restano due»: ne restano **tre**, quindi il Coro c'è. La riga `fallito` di *Cantitrici protette* non toglie niente di quello che il finale usa («se ne restano almeno tre»). La posta dichiarata («è una cosa in più da perdere») non si perde. | 🟡 | «ne cadono due, e il Coro si perde quando ne restano due» (`:907-908`); «Il Coro e la *cura ferite gravi di massa*, se ne restano almeno tre» (`:1451`); «Sa: che il Coro chiede tre voci, e che con due non c'è più» (`:810`) |
| D-R16 | 6 | §17 · regola | **Borin, opzione B: la prova è sbagliata.** Spingere in 3.5 è una prova di Forza **contrapposta** (lo scrive il box PF1e alle righe 253-255), non una CD 25. Con Forza +5 la prova vale **5% (con Postura Difensiva +7: 15%)**, e il Re, che vuole stare sulla piattaforma, non ha motivo di farsi spostare; tre quadretti richiedono +10 oltre il risultato. L'opzione C è dichiarata irraggiungibile. Resta una sola scelta praticabile, **A**, che costa a Borin ~35 pf su 142: il sacrificio «che il nipote di un re può fare una volta» non ha costo vero. | 🟠 | «Forza **CD 25** (Borin ha For 20, +5; in Postura Difensiva For 24, +7): se riesce, lo spinge tre quadretti a nord» (`:1082-1084`); «spingere (*bull rush*) … in 3.5 è una prova di Forza contrapposta» (`:253-255`); «Borin non lo raggiunge, e il DM lo dice prima che scelga» (`:1089-1090`) |
| D-R17 | 6, 7, 8 | §5 · contraddizione | **Il Re a 8 pf è una regola inventata che annulla le scelte dei PG.** Dice che «le cure lo tengono vivo e non lo rimettono in piedi: ogni pf sopra gli 8 lo mangia l'acido». Quindi la *guarigione* di Thorin (120 pf, una delle sue 4 caselle di 6° livello), proposta come opzione al riga 1112, **non vale niente**. Poi: «perde 2d6 a round finché non lo stabilizzano, e muore a −10»: a 8 pf non è in agonia, e *stabilizzare* (Guarire CD 15) vale per i morenti; non si dice se la perdita continui con una cura già fatta, né cosa la ferma. Scena 7 (18 round) e la marcia di mezz'ora la pagano con un'azione di Thorin a round. I dadi non portano a 8: media soffio 35 + lancia 38 su ~150 pf. È un esito scritto, non una conseguenza. | 🟠 | «ogni pf sopra gli 8 lo mangia l'acido prima del Cuore» (`:1138`); «perde **2d6 a round** finché non lo stabilizzano, e muore a −10» (`:1139-1140`); «ogni round in cui non lo cura, l'acido toglie 2d6 … Quando lo stabilizza, il Re resta a **8 pf** fino al Cuore» (`:1229-1230`); «***Guarigione*** sul Re dopo il soffio, al round 5: 120 pf» (`:1112`) |
| D-R18 | 5, 6 | §5 · manca | **Il soffio è il solo pericolo della scena e una preparazione da 3° livello lo azzera.** Il Re lo dice la sera prima («Domani il drago viene per me»), *comunione* lo conferma, e *protezione dall'energia* (acido, 120 danni, 10 minuti per livello) assorbe 14d4 (35 di media) con un margine di 85. Il master lo sa («È la cosa giusta da fare, e funziona») e non dà a Fauci niente d'altro: nessun secondo soffio dopo 1d4 round, nessuna morsa, nessuna *nube maleodorante* sulla piattaforma. L'eco della «corona nera» (§9) presuppone l'acido che non c'è. | 🟠 | «`Con la protezione dall'energia, l'acido del cono non c'è`» (`:1142`); «Domani il drago viene per me» (`:972`); «dopo il soffio, se non atterra, risale e non torna» (`:718-719`); «La corona nera … l'acido ha annerito la Corona» (`:1454`) |
| D-R19 | 6 | §17 · regola | **Economia d'azione.** Il round 4 mette insieme il soffio di Fauci (azione standard) e la **carica in picchiata** del cavaliere con triplo danno. Il danno triplo del cavaliere (3d8+21) richiede che la cavalcatura **carichi** (Carica Devastante / Spirited Charge); un drago che soffia non sta caricando. *Attacco in Volo* (Flyby) è una sola azione standard con un movimento prima e uno dopo, quindi o soffia o carica. | 🟠 | «**il soffio a cono** … Il cavaliere carica in picchiata con la lancia sul Re (+18 in carica contro CA 30, 3d8+21 …)» (`:1071`); «in carica in sella danni tripli con Carica Devastante» (`:1532`) |
| D-R20 | 6, 8 | §8 · manca | **Fauci non ha attacchi in mischia.** L'Appendice A.5 dà CA, pf, TS, soffio, Presenza e incantesimi, e nessuno fra morso, artigli, coda, ali. Le Tattiche («attacco completo su chi lo ha ferito di più, coda sulle guardie») e la contingenza «combattono il drago sulla piattaforma» li usano. Il DM deve aprire `Bestiario/` o inventarli. | 🟠 | «Se atterra su un bastione: attacco completo su chi lo ha ferito di più, coda sulle guardie» (`:720-721`); «combattono il drago sulla piattaforma … è la mappa: 337 pf» (`:1421`); A.5 (`:1530`) senza attacchi |
| D-R21 | 6 | §17 · regola | La distanza di Dara contro il drago è sottostimata. Il master mette Dara «in cima alla Torre Ovest, fuori mappa, ~45 m a ovest» (`:1056`) e Fauci tra AI26 e V24 (colonne 35 e 22 di una griglia da 1,5 m = 33-52 m oltre il bordo): **78-97 m**, cioè il 3° o 4° incremento (−4 / −6), non «−2». Contro CA 37 diventa il 5% per freccia. | 🟡 | «+1 della mira, −2 per la distanza, contro CA 37» (`:1096`); «Dara … fuori mappa, ~45 m a ovest» (`:1056`); «scende in AI26 → V24» (`:1058`) |
| D-R22 | 6 | §1 · contraddizione | Due versioni dell'acido sul Re con la protezione: «il Re prende lo stesso la lancia del cavaliere, **e l'acido sull'armatura** (sotto)», e dieci righe dopo «l'acido del cono non c'è». In più «il Re è ferito dalla lancia e dalla **caduta**»: nessuna caduta è in scena, salvo l'opzione B di Borin. | 🟡 | `:1108-1109` contro `:1142-1144` |
| D-R23 | 6 | §0 · altro | Dopo la sequenza sulla 2B (4 round griglia + 2) i round 3 e 4 di battaglia riprendono «senza la carta», ma **dove sono i quattro eroi?** Sono sul cancello a portare il Re (due portatori…), il loro settore è caduto, e nessuno dice chi tira cosa. Il cancello «è caduto» al round 1: è una breccia (−2 morale, settore fuori gioco) o no? | 🟡 | «il cancello è caduto: il fronte del Cancello resta quello del Giorno 2 `[INFERRED]`» (`:1008`); «Si torna al libretto: round 3 e 4 del Giorno 3» (`:1161`) |
| D-R24 | 6 | §17 · manca | Le Guardie Reali (12) non hanno CA, pf né TS, e ne «cadono sei-otto» a un soffio di 35 di media a testa con Riflessi CD 29. È un numero fisso, non un tiro. | 🟡 | «delle dodici guardie sulla piattaforma ne cadono sei-otto» (`:1148-1149`) |
| D-R25 | 7 | §6 · manca | **La ritirata è uno skill challenge a metà.** Chi tira: nessuno (solo il tunnel: Forza CD 20 o sapere bardico CD 15). Cosa tira: niente. Quanti successi servono: n/a. Costo dei fallimenti: «una breccia senza nessuno costa 1d4 nani a round». Il risultato (90 / 80-89 / <80) esce dall'assegnazione dei posti, e un incantesimo lo azzera: *barriera di lame* (6°, 12 minuti, ben oltre i 18 round) chiude una via per tutte e tre le fasi, e *muro di pietra* di Dana un'altra. Le fasi sono sei round l'una contro ~40, ~40, ~120 orchi (e le brecce est e ovest); **dell'orda della Porta Interna non c'è nemmeno una riga di statistiche** (orchi? hobgoblin?). Venti minuti di tavolo senza dadi per i giocatori. | 🟠 | «una breccia senza nessuno costa **1d4 nani a round** `[INFERRED]`» (`:1214`); «Ogni via chiusa per tutta la fase non costa nessuno» (`:1218`); «dalla Porta Interna, ~120, dal round 4 della fase 1» (`:1215`); «È una scena di tempo, non di uccisioni» (`:1198-1199`) |
| D-R26 | 6, 7 | §1 · contraddizione | La Porta Interna **regge mezz'ora** in Scena 6 e **«dal round 4»** in Scena 7 (24 secondi). Ha 90 pf (§2, Zona 4). | 🟠 | «La Porta Interna regge mezz'ora (Scena 7)» (`:1175`) contro «l'orda a contatto … dal round 4 dalla porta» (`:1199-1200`) e «Porta Interna (90 pf)» (`:389`) |
| D-R27 | 7, 8 | §13 · contraddizione | «L'ultimo a entrare chiude la statua dietro di sé», eppure al round 4 di Scena 8, mezz'ora di marcia dopo, arrivano «**30 orchi** dal tunnel sud» se «la retroguardia … ha lasciato una breccia aperta». Quale breccia, e per dove entrano, se la statua è chiusa? Quanto ci mettono? | 🟡 | `:1232-1233` e `:1285` |
| D-R28 | 7, 8 | §15 · manca | Orchi (A.9, GS 2) e hobgoblin sono **dossi** per un gruppo di 12°/13°: 7 hobgoblin e 30 orchi sparirebbero con una *barriera di lame* o una *palla di fuoco*. Il testo non scrive perché esistono (diversione, allarme, pressione sul chokepoint) né li dichiara sacrificabili. | 🟡 | «gli hobgoblin tengono l'anello» (`:1284`); «30 orchi dal tunnel sud» (`:1285`) |
| D-R29 | 8 | §17 · regola | **Il tiro che dovrebbe svelare l'imboscata è fisso e sbagliato di direzione.** Osservare CD 25 (una prova a testa) contro il Nascondersi +17. In 3.5 è una prova contrapposta (media 27), e a CD 25 fissa passano **Dara 80% (+20), Nala 55% (+15)**, Thorin 10%, Borin 0%: **l'imboscata è svelata 92% delle volte** (63% se si contano −1 ogni 3 m di distanza). Il master poi chiede a chi supera di avvisare («chi è avvisato non è colto alla sprovvista»), quindi l'attacco mortale non ha il suo furtivo/«colto alla sprovvista». Lo scenario modale è un combattimento senza sorpresa. | 🟠 | «**Osservare CD 25**, una prova a testa, contro il buio dei tunnel est e ovest. Chi la supera vede le sagome: può avvisare» (`:1282`); «Osservare CD 25 (il loro Nascondersi +17 nel buio)» (`:179`); «Dara … +20 contro CD 25» (`:1307`) |
| D-R30 | 8 | §17 · manca | **Chi vede al buio.** Nani (scurovisione 18 m) e bugbear (18 m) vedono entrambi senza luce; il «buio» non dà occultamento contro la scurovisione entro 18 m, e Nascondersi richiede copertura o occultamento. Il master usa «il buio dei tunnel» come copertura e non dice se serva un riparo (stalagmiti, bocche di tunnel). Le schede dei pregen (Handout 1-4) non scrivono nemmeno la scurovisione. | 🟠 | «contro il buio dei tunnel est e ovest» (`:1282`); «scurovisione 18 m, fiuto … Nascondersi +17» (`:1534`); «Le torce non arrivano alle pareti» (`:1249`); Handout 1-4 senza la riga (`HANDOUT-GIOCATORE.md:99-173`) |
| D-R31 | 8 | §16 · manca | **Un PG fuori gioco per un tiro salvezza, senza via d'uscita.** Tempra CD 16 contro l'attacco mortale: **paralisi 1d6+2 round, senza nuovo TS**, oppure **morte** («o morto, se lo sceglie», A.7). Per un assassino che sceglie la morte, Nala (Tempra +8) cade il **25%** (con la Presenza di Borin +2) e un pregen a caso il 39% (almeno uno su quattro). Un paralizzato è indifeso: colpo di grazia (e furtivo) lo uccide al round dopo. Il testo non dice come esce (alleato? *libertà di movimento*, che Thorin ha e non ha preparata), né cosa fa il giocatore nei ~6 round che restano in una scena di 30-40 minuti. | 🟠 | «**attacco mortale** sul primo colpo: Tempra **CD 16** o paralizzato 1d6+2 round» (`:1283`); «(o morto, se lo sceglie)» (`:1534`); «*Libertà di Movimento* (4°) … niente lotta, paralisi» (`HANDOUT-GIOCATORE.md:245`) |
| D-R32 | 8 | §17 · contraddizione | **Schivare prodigioso migliorato** a un Ladro 5 / Assassino 2: l'SRD lo dà al Ladro dall'8° livello (qui 5, e l'assassino non lo dà). Al Ladro 5 spetta *schivare prodigioso* (non colto alla sprovvista), che permette di fiancheggiarlo. In più il master si contraddice: i bugbear «combattono in coppia per **fiancheggiare**» e Nala fa «il furtivo +3d6 sui bugbear **fiancheggiati**», mentre A.7 dice «non si fiancheggia». Il furtivo di Nala non esiste, o i bugbear sono più forti dell'SRD. | 🟠 | «schivare prodigioso migliorato (non si fiancheggia)» (`:1534`); «in coppia, per fiancheggiare» (`:728-729`, `:1284`); «il furtivo +3d6 sui bugbear fiancheggiati» (`:1316`) |
| D-R33 | 8 | §2 · manca | **Invisibile, silenzioso, fiuto.** *Invisibilità* (Nala, 2°, otto minuti, tocco) sul Re risolve in un incantesimo la scena che dice «il Re deve avere qualcuno davanti a ogni lato». I bugbear hanno fiuto (9 m, individuano la fonte), ma il master non lo usa contro l'invisibilità e il Re a 8 pf non ha altra difesa; *silenzio* è dichiarato «non serve» e la diversione è fatta di rumore: lo si dovrebbe poter usare per un danno. Non c'è una riga su cosa cambia. | 🟠 | *Invisibilità* (2°): «tocco, dura 8 minuti» (`HANDOUT-GIOCATORE.md:281`); «*Silenzio* non serve» (`:1312`); «scurovisione 18 m, fiuto» (`:1534`); «il Re deve avere qualcuno davanti a ogni lato al round 2» (`:1290`) |
| D-R34 | 8 | §8 · manca | **Come arrivano i bugbear al Re.** La mappa propone il Re in Q19 con i portatori in P19 e R19 e Borin in **Q15**, quattro quadretti a nord, dietro il Pilastro: le caselle libere intorno al Re sono la riga 20 (3 caselle). I bugbear escono «insieme» al round 2 dalle bocche (a oltre 16 quadretti, 24 m, contro i 9 m di velocità): non si capisce se sono già nella caverna; e lo studio dell'attacco mortale (3 round entro 9 m dal bersaglio, senza che nessuno se ne accorga) avviene durante una marcia di mezz'ora senza prove (Ascoltare, Osservare, fiuto). «Coprire» il Re non ha regola: occupare le tre caselle? Dara in cima alla stalagmite è lontana. | 🟠 | «la mappa propone Borin Q15, Thorin O19, Nala O15, Dara L9» (`:1270-1271`); «il Re in Q19 … portatori in P19 e R19» (`:1268-1269`); «Hanno studiato i bersagli dall'avvicinamento» (`:1283`); «studiano i bersagli per tre round dal buio dei tunnel, durante la marcia» (`:725-726`) |
| D-R35 | 8 | §14 · manca | I 30 orchi del round 4 non hanno nessun segno che li preceda (un corno, dei passi, un conto alla rovescia). Chi non ha divinato non lo sa prima del colpo. | 🟡 | riga del round 4: «se la retroguardia della Scena 7 ha lasciato una breccia aperta nella fase 3, **30 orchi** dal tunnel sud» (`:1285`) |
| D-R36 | 4, 6, 7, 8 | §10 · manca | **Riga di scala.** Solo la Scena 2 ha «Tre pregen / Cinque giocatori»; Scene 4 e 8 hanno ritardo/liscio/difficoltà, ma non dicono cosa cambia con tre o cinque PG; Scene 6 e 7 non hanno la sidebar. Nessuna dice a quale riga appartiene «il gruppo di stasera» (4 pregen, APL 12,25). | 🟡 | «Scalare lo scontro» (`:673-686`, `:942-950`, `:1330-1340`); Scene 6-7 senza |
| D-R37 | 0 | §0 · altro | **I tempi non tornano.** Sommando la tabella: min 3h00, max 4h10 (con tutti e tre i duelli), non «3 h 35 e 4 h 30». La Scena 1 ha 15' per leggere 12 leve, spiegare quattro paragrafi del libretto (la riga stessa dice «Dieci minuti») e fare le tre scelte. | 🟡 | tabella `:115-126`; «Il totale sta fra **3 h 35** e **4 h 30**» (`:128`); Scena 1 `:429-456` |
| D-R38 | 0 | §1 · contraddizione | «Tre mazzi dell'orda per giorno, **uno per settore**»: i settori sono **quattro** (Cancello, Mura, Torre Ovest, Torre Est). SEGRETI §4: «per ogni settore, quattordici reparti». Servono 4 mazzi (56 carte al giorno, con picche per 24 hobgoblin: più di un mazzo di carte). | 🟡 | `:97-100`; `SEGRETI-DM.md:182-184`; `LIBRETTO.md:41-46` |
| D-R39 | 0 | §0 · altro (forma) | Ventuno rimandi a «**domanda N**» e a «**dell'apparato**» restano nel testo che va in stampa: puntano a scelte aperte al DM che il lettore non ha. Righe 133, 156, 235, 239, 335, 351, 574, 585, 608, 654, 867, 889, 929, 1010, 1097, 1132, 1167, 1226, 1476, 1524, 1579. | 🟡 | «`[INFERRED — domanda 1 dell'apparato]`» (`:133`); «`[INFERRED — domanda 12]`» (`:239`, `:1010`) |
| D-R40 | Handout | §17 · regola | **La carta di Thorin ha 7 incantesimi di 3° e non ne ha 6.** Chierico 12° (tabella): 4 base + 1 di dominio + 1 di Saggezza 22 = 6. La carta elenca *cura ferite gravi* ×2, *preghiera*, *dissolvi magie*, *rimuovere maledizione*, *protezione dall'energia*, *scolpire pietra*: 7. Gli altri livelli tornano (8/8/6/5/4 per 1°/2°/4°/5°/6°). Uno va tolto, e il master ne usa tre (*preghiera*, *protezione*, *scolpire pietra*) nelle scene; il candidato è *rimuovere maledizione* o una *cura gravi*. | 🟡 | `HANDOUT-GIOCATORE.md:248-253` |
| D-R41 | 8 | §17 · regola | La CD dell'attacco mortale è **10 + livello da assassino (2) + mod. Int**: CD 16 richiede **Int 18**. La fascia dell'intelletto +2 del tesoro suggerisce Int di base 16, mai scritta nell'Appendice (che non scrive nessuna caratteristica). Se è Int 10 +2, la CD è 13. | 🟡 | «Tempra **CD 16**» (`:1534`); «*fascia dell'intelletto +2*» (`:1477`) |
| D-R42 | 3, 7, 8 | §0 · altro | **Dana arriva al Cuore con 20 pf** (canone) e non c'è nessuna scena in cui li perde: la notte 1 «spende quello che ha», la ritirata «ha 20 pf», il muro di pietra è una risorsa. Il passaggio da 142 a 20 non ha un pericolo che lo spieghi; se il tavolo non lo vede, il numero è decorazione. | 🟡 | «arriva al Cuore con 20 pf e un *muro di pietra*» (`:757-758`, `:1220-1221`) |
| D-R43 | 2, 8 | §2 · manca | La contingenza **sortita** («sotto settecento paia d'occhi») non risponde a «e se sono invisibili?»: Nala ha *invisibilità* e Dara *passare senza tracce* (4 compagni, 4 ore); un'incursione notturna ha una risposta e il master dice solo che ci sono «settecento paia d'occhi». | 🟡 | «il campo è sulla piana, a 500 m-1 km, sotto settecento paia d'occhi» (`:1418`) |

---

## Domande aperte (D-An)

- **D-A1.** I duelli (Gorthak, Grimjaw) sono pensati **per un PG** o **per il
  gruppo**? Se per uno, l'EL va ricalcolato (D-R2); se per il gruppo, serve la
  regola che tiene in gioco gli altri tre senza far perdere il settore (D-R1).
  Un'idea di sostegno: i reparti tirano comunque, e chi si unisce prende le tacche
  solo se il settore ne avrebbe preso senza di lui.
- **D-A2.** Il Re a 8 pf è un **esito scritto** o una **conseguenza dei dadi**? Se
  è scritto, il master lo dica ai giocatori in chiaro (le cure non lo alzano) e tolga
  le opzioni che promettono il contrario. Se è una conseguenza, serve un soffio che
  lo porti lì (due soffi? mischia?).
- **D-A3.** *Protezione dall'energia* è «la cosa giusta e funziona» (`:1107`): è
  la risposta voluta (premia chi ha divinato) o un buco? Se voluta, la scena ha
  bisogno di un secondo pericolo che la preparazione non copra (D-R18).
- **D-A4.** Il bugbear assassino sceglie la **morte** o la **paralisi**? La
  scheda dice «se lo sceglie»: chi decide, con quali bersagli (D-R31)?

## Considerazioni generali (D-Gn)

- **D-G1 · Le statistiche della Appendice A non si possono rifare da sole.** Nessun
  blocco dà le caratteristiche. Ricostruendo da ciò che c'è: **Gorthak** ha Str 29
  (+9: danni +10/+5, giavellotto +9, come si legge), Con 28 (202 pf = 15d8 +
  15×9; Tempra +18 = 9 + 9), Des 14 (Iniz +6, Rifl +7); l'ettin dell'SRD ha Str 21,
  Con 15, Des 8, e il GS **12** dichiarato non esce dalla regola della DMG (ettin GS 6
  con +5 DV = GS 7); il resto è potenziamento, che deve stare nel `Boost log:`.
  L'attacco +21 è uno sopra 11 + 9 − 1 + 1 = 20, e due sopra se il randello Enorme
  è davvero Enorme per un Grande (−2). **Fauci** torna: 337 pf = 25d12 + 25×7 (Con
  24-25), Tempra +21 = 14 + 7, CD soffio 29 = 10 + 12 + 7. **Grimjaw**: +4 Forza
  e Costituzione danno +24/+19/+14, 1d10+11 e +26 pf (13 DV × 2), tutto coerente.
  **Troll (A.2):** tutti i numeri tornano all'SRD (CA 16/11/14, 63 pf, TS +11/+4/+3,
  +9/+9/+4, sbranare 2d6+9). **Tabella dei pregen (A.11) contro Handout 1-4:**
  identica. **Quick-reference contro libretto contro segreti:** AU/DU/PFU dei
  reparti, i bianchi 34/30/31/32, il fronte 3/4/5 del Cancello: tornano.
- **D-G2 · Le cose che ho controllato e tornano** (così non si rifanno): il budget
  PX (zero), le quattro parti dell'EL (D-G1), la CD di *colpo infuocato* (21) e di
  *barriera di lame* (22) con Sag 22, i PF di *guarigione*/*ferire* (120), la durata di
  *protezione dall'energia* (120 minuti, 120 danni), *immagine silenziosa* (12 cubi,
  216 m), i prezzi della freccia assassina (2.282 mo), l'attacco di Dara (+19/+14/+9,
  +17/+17/+12/+7 con Tiro Rapido, +21/+19 contro i draghi), il «spremersi» di
  Gorthak (−4/−4, SRD), *scudo*/*armatura magica* (7 minuti / 7 ore: coprono il
  Giorno 1 e il 3 se lanciati all'alba), la Presenza terrificante (scosso per 4d6 round, immunità 24 ore: il
  Giorno 3 è passato oltre).
- **D-G3 · I tre TS** (§3): Volontà (Presenze), Riflessi (soffi, palla di fuoco),
  Tempra (solo l'attacco mortale, Scena 8): voluto o no, il Tempra è un'unica
  scena e va sul PG con il TS più basso (Nala +8). Lo dico in D-R31.
- **D-G4 · Quello che funziona** e vorrei non perdere nel rimaneggiamento: la
  sequenza a quattro round della 2B («preparare / Presenza / posizione / soffio»)
  dà ai giocatori il tempo di scegliere; il blocco «Se lo divinano» c'è e copre la
  quasi totalità dei segreti; i comandanti che fuggono a metà evitano il «boss che
  si allunga»; la regola del tavolo in ritardo/liscio/in difficoltà è già misurata
  in minuti; il Re sulla piattaforma dà al soffio un bersaglio e una ragione.
- **D-G5 · Rubrica non applicabile.** §7 (i sette modi di gioco) vale per i gruppi
  nuovi, non per i quattro del tavolo (i profili veri sono in
  `campaign-dm-strategy`, che non ho): non l'ho valutata.

---

## Riepilogo

43 rilievi (D-R1 … D-R43): **🔴 0 · 🟠 18 · 🟡 25**.

- 🔴 **0.** Niente blocca il tavolo da solo: ogni vuoto ha un ripiego (il DM può
  scegliere un numero). Se dovessi spostare un rilievo in alto sarebbe
  **D-R25** (Scena 7 senza tiri) o **D-R31** (un PG paralizzato 6 round nella
  scena finale, con il colpo di grazia possibile).
- 🟠 **18:** D-R1, D-R2, D-R3, D-R6, D-R10, D-R16, D-R17, D-R18, D-R19, D-R20,
  D-R25, D-R26, D-R29, D-R30, D-R31, D-R32, D-R33, D-R34.
- 🟡 **25:** D-R4, D-R5, D-R7, D-R8, D-R9, D-R11, D-R12, D-R13, D-R14, D-R15,
  D-R21, D-R22, D-R23, D-R24, D-R27, D-R28, D-R35, D-R36, D-R37, D-R38, D-R39,
  D-R40, D-R41, D-R42, D-R43.

**In sintesi.** La serata è ben costruita nella forma (sequenza della 2B,
comandanti che fuggono, «Se lo divinano», righe di scala sul libretto). Le sue
debolezze sono tre e si vedono tutte con i dadi: **(1)** i duelli sono dimensionati
per il gruppo e giocati da uno (D-R1-D-R2); **(2)** i due momenti simbolici della
sera, il tiro di Dara e il Re a 8 pf, sono esiti scritti che i dadi non producono
(D-R10, D-R17, D-R18); **(3)** la Scena 8 dipende da una CD 25 fissa e da uno
schivare prodigioso migliorato che l'SRD non dà, quindi il suo caso modale è
un combattimento senza sorpresa (D-R29, D-R32). Il resto è aritmetica e rimandi.
