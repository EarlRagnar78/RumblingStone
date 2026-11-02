# ARC07-DEF-4, lettura finale del developer (giro 4, 2026-10-19, prima della stampa)

Bersaglio: il master `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` dalla Scena 5 alla
Scena 11 con le Appendici A, C e D, la regia (`01-REGIA-SERATA.md`), il §0-bis,
la scheda di Durik e il capitolo B4, confrontati con il generato
`ARC07-NOTTE-E-ALBA-BOOKLET.hb.md`. Rubrica:
`skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`.

**Lo strumento.** `python3 scripts/domande_developer.py --file …DEF-4…` dà gli
stessi 6 rilievi di stamattina (D2 ×3 Scena 2, D15 Scena 6, D10 Scena 7, D1
Scena 8), tutti dichiarati in `plans/domande-developer.json`; `--check` esce 0.
Stasera si parte dalla Scena 5, quindi i tre della Scena 2 non contano.

**Cosa ho rifatto a mano, e torna.** Skullcrusher (A.1) sul drago nero adulto
maturo SRD con il template Avanzato: pf 297, CA 33/37, contatto 10, TS
+20/+17/+19, Lotta +40, morso +30 (2d8+10), artigli/ali/coda +25 con metà e
1,5 volte la FOR, soffio 14d4 CD 30 (28 + Capacità Focalizzata), Presenza CD 25
a 63 m, schiacciare CD 28, 8 talenti per 22 DV, incantesimi 6/7/5 CD 14. A.1-bis
(Vecchio): CD 31 e 26. Zog'tar (A.2): 283/328 pf, CA 26/24, contatto 12,
attacchi +29 e +26, Lotta +29/+32, TS, Ira 6/giorno per 13 round, Presenza
Minacciosa CD 21, Colpo Devastante +25. Sacerdote: adepto 7, 3/4/3, CD 12+liv.
Balvar: CA 24, *barriera di lame* 13d6 CD 21, *uccidere i viventi* e *comando
superiore* CD 20. Durin, worg, orchi, hobgoblin guerriero 4, wyvern: coincidono
con l'SRD e con `VERIFICHE-SRD.md`. PX: drago 5.850, wyvern 325 l'una (1.625 a
testa), Zog'tar 7.800, guardie 650 l'una, tenda ≈ 14.625 (3.650 a testa).
Rune di Zeth (350 mo, 20 di resistenza, 70 minuti), bombe di Kettra (750 mo,
CD 14), volo e invisibilità in metri e round, glifi e soglia di Balvar
(5d8 CD 18, *epurare* a 19,5 m per 13 minuti, Cercare/Disattivare CD 28),
bottino della tenda (≈ 49.750). M7-C: le posizioni del testo (N2, M4-N4, M9,
J8, M12-N13, K12/L10/O10/P11, P13, S5-S13, L14-N14, N15, W11) coincidono con la
griglia, e il *silenzio* di Balvar da P13 prende Grask a N15. Le decisioni del
DM (Bane che tace, Bracieri che valgono, Ghermire e Fluttuare, CA 22/16 di
Vatore, 1d4+2 per la ronda, wyvern a EL 14) sono entrate nel master, nella
regia e nel generato. Il volume dei giocatori non porta marche
`[CANONE]`/`[INFERRED]`, e le dieci boccette tornano con la tabella del master.

Non ho trovato niente che rompa la serata.

---

## 🟠 Il DM si blocca al tavolo

**O1 · §0-bis, «Il giro di Skullcrusher»: la pagina da stampare non ha le wyvern né Ghermire e Fluttuare.**
Prova: il riquadro dice soltanto *«Volo: resta in quota, picchia e risale
(Attacco in Volo)»*, e chiude con la Cintura che rifiuta. Mancano le due wyvern
che stasera entrano al round 2 (G2-15), i due talenti della decisione 6, la CA
41 della Catena e il Bane che tace. Il §0 dice «Cosa stampare: la
Quick-Reference», e chi gioca da quella pagina dimentica le wyvern. La regia
§4 le ha, il §0-bis no.
→ Due righe nel riquadro: «Dal round 2: 2 wyvern (A.6) su chi tiene la corda e
su chi vola. Ghermire e Fluttuare: Scena 11, «Ghermire e Fluttuare»; la
Catena, CA 41; il Bane qui tace, la *Dragondoom* vale».

**O2 · Scena 11, *Ghermire*: le due frasi sul danno sembrano dirsi il contrario.**
Prova: *«A ogni prova di lotta vinta nei round dopo la preda riprende il danno
del morso. Il danno automatico di Ghermire vale solo contro chi è tre taglie
più piccolo, quindi non contro i PG Medi.»* Con un nano in bocca il DM non sa
se ogni round gli fa 2d8+10 o niente. Le due regole valgono tutte e due
(presa migliorata e *Snatch*), ma la seconda frase si legge come una smentita
della prima.
→ «Contro un PG Medio il danno non è automatico: ogni round tira la lotta (+20
con la sola bocca), e se vince il morso fa 2d8+10».

**O3 · Scena 8 contro A.2: «Colpo Possente» non esiste nello statblocco, e il «pieno» non è il pieno.**
Prova: tattiche, *«Colpo Possente moderato (−5/+10)»* e *«un ultimo Colpo
Possente pieno −10/+20»*; A.2, *«Attacco Poderoso a due mani: fino a −15 al
colpire per +30 ai danni»*, e la tabella dei Treant dice «Attacco Poderoso».
Chi cerca «Colpo Possente» in A.2 non lo trova, e accanto c'è il **Colpo
Devastante**, un talento diverso: tre nomi per due cose. Alla soglia del 30%
il DM non sa se tirare −10/+20 o −15/+30.
→ «Attacco Poderoso» in tutta la Scena 8, e un numero solo per l'ultimo colpo:
«Attacco Poderoso pieno, −15/+30».

---

## 🟡 Migliorabile, e costa poco

**Y1 · Scena 11, «La sequenza»: il soffio con la preda in bocca, di solito, non è carico.**
Prova: *«Al turno dopo si ferma a 15 m e sceglie: lo lascia cadere […] oppure
[…] lo tiene in bocca e soffia sugli altri»*. Il soffio aderente del round 1
porta la ricarica a 1d4+1 round: al round 3 è carico solo con un 1 sul dado.
→ Aggiungere «se il soffio è tornato».

**Y2 · Scena 11: nel round a terra la nube di *Fluttuare* non c'è.**
Prova: *«Scende sotto i 6 m solo per l'attacco completo contro chi lo ha
inchiodato con le corde, e la nube copre la sua ritirata»*. Il DM può mettere
il 20-50% di mancare proprio nel round delle corde, che è quello del gruppo.
→ «Nel round inchiodato è a terra e non fluttua: niente nube. La nube viene
dopo, quando torna a fluttuare basso».

**Y3 · Scena 11, chi ghermisce: la sequenza salta «Chi sceglie».**
Prova: *«In picchiata, con Attacco in Volo, morde chi lo ha ferito di più»*,
mentre «Chi sceglie» mette prima chi ha detto la Catena e chi tiene la corda.
→ «morde il bersaglio di «Chi sceglie»».

**Y4 · *Corrompere l'acqua*: due momenti diversi.**
Prova: A.1, *«Lo usa al primo round se vede qualcuno bere»*; Scena 11 lo mette
nei round 2-3, e il round 1 è del soffio (due azioni standard).
→ In A.1 «al primo turno libero dal soffio, se vede qualcuno bere».

**Y5 · Durik e il soffio: il danno massiccio scatta quasi sempre, e la scheda sembra vietare il richiamo.**
Prova: Durik ha Riflessi +10 contro CD 30 e prende il 50% in più: in media 52
danni, oltre i 50 del danno massiccio (Tempra CD 15, lui +11). Nessuna riga lo
dice. La scheda (cap. VI) aggiunge: *«Se l'Evocazione è spenta, perché hai
chiamato i due Treant insieme, non puoi richiamarlo subito»*, e la giocatrice
può leggerla come un divieto anche dopo i due Treant dell'alba, che per la
Scena 5 (D65) non spengono l'Evocazione.
→ Nella riga 4-bis: «senza runa, il soffio gli fa più di 50: Tempra CD 15 o
torna polvere; dopo i Treant dell'alba resta una carica per richiamarlo».

**Y6 · La runa di Zeth su Durik: chi la attiva?**
Prova: Scena 5, *«Per Durik vale di più»*; regia §4, la runa è una delle *«due
risposte del gruppo»*. Durik ha INT 4 e non attiva niente, e il testo non dice
se la runa si attiva su un altro.
→ «La attiva chi la porta, toccando il bersaglio: Hella la mette su Durik».

**Y7 · §8 A: il totale non conta le wyvern, che stasera ci sono.**
Prova: *«TOTALE beat […] ~7.610/PG»* somma 1.460 per il duello; con le wyvern
il duello vale 1.625, quindi **~7.775**.
→ Aggiungere «(~7.775 con le wyvern)».

**Y8 · Il danno massiccio non è una regola della casa.**
Prova: §0-bis e Scena 8, *«Danno massiccio (regola della casa)»*. 50 danni e
Tempra CD 15 sono la regola SRD (*Injury and Death*). Va verificato in
`campaign/lore/house-rules.md` se la casa aggiunge qualcosa, per esempio che
valga anche per il soffio.
→ «Danno massiccio (SRD)», oppure scrivere che cosa aggiunge la casa.

**Y9 · Regia §0 e §4: «regia veloce» vuol dire due cose.**
Prova: §0, *«il duello con la regia veloce dal primo round invece che dal
terzo»*; §4, *«il duello passa alla regia veloce, `DEF-4` Appendice C.3, tre
scambi»*. C.3 sostituisce il duello e non ha round.
→ Nel §0: «saltare le battute della regia dei primi due round (Scena 11)»,
oppure «C.3 al posto del duello».

**Y10 · Regia §4: «Quattro cose da tenere davanti», e sono cinque.**
→ «Cinque cose».

**Y11 · M7-B: tutti i PG e il re stanno sulla riga 16.**
Prova: D16, G16, L16 (il re), Q16, T16, U16. Una linea di 30 m lungo la riga li
prende tutti e sei, re compreso, e la Scena 11 vuole il primo soffio «sul gruppo
più fitto».
→ Nella nota della mappa: «posizioni di partenza: le sceglie il tavolo; se non
le sceglie, sfalsale su due righe».

**Y12 · Ghermire e l'Ancoraggio della Montagna: il canone non è d'accordo.**
Prova: `state-ramo-di-gruppo.md` (riga dei Bracieri) dà ancora a Tordek
*«Ancoraggio della Montagna 2/day (immediata, nega il movimento forzato)»*,
mentre `sessione-4.md` dice che Tordek l'ha dato a Hella come Dono. Se Roberto
lo usa quando il drago lo ghermisce, il DM deve decidere al tavolo se c'è e se
ferma la salita.
→ Una riga in «Chi non vola»: «l'Ancoraggio è passato a Hella (Doni): Tordek
non l'ha», oppure il contrario, a scelta del DM.

**Y13 · Le guardie di Zog'tar: il danno del giavellotto non torna con quello dello spadone** (da verificare).
Prova: A.2, *«spadone +14 (2d6+6)»* e *«giavellotti +9 (1d6+4)»*. Lo spadone
torna con FOR 17 (8 + 3 + Arma Focalizzata, Focalizzata Superiore e arma
perfetta; 2d6 + 4 + 2 di specializzazione); con FOR 17 il giavellotto fa
1d6+3, perché la specializzazione è sullo spadone.
→ «giavellotti +9 (1d6+3)», se le caratteristiche sono quelle.

**Y14 · Zog'tar, velocità 12 m in armatura di mithral** (da verificare).
Prova: A.2, *«Velocità 12 m»*. Il movimento veloce del barbaro (+3 m) vale in
armatura media, e il mithral fa della completa un'armatura media, ma l'armatura
media rallenta: da 9 m base si arriva a 9 m, non a 12. Dipende dalla velocità
base del mezzo-ogre, che l'appendice non dà.
→ Scrivere la velocità base, o portare la velocità a 9 m.

---

🔴 0 · 🟠 3 · 🟡 14
