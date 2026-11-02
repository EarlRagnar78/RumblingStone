# ARC07-DEF-4, Scene 5-11 — il developer a freddo (giro 4, 2026-10-19)

Lettura per la serata di stasera: il gruppo riprende dalla Scena 5 con 3 tacche
su 8, la dotazione **dall'alto** del re (5 *volare*, 4 «di CFC», niente
invisibilità del re), 2 pozioni d'*invisibilità* comprate, fiducia piena,
banco speso. Rubrica: `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`,
tutte e 16 le domande. Prima di cominciare ho riletto il giro del 2026-10-18
(`plans/esperimenti/giro-arc07-2026-10-18/DEF-4/DEVELOPER.md`): i suoi rilievi
#1, #2, #3, #5, #6, #7, #8, #10, #12, #17, #18 e #19 risultano chiusi nel testo
di oggi, e qui non li ripeto. Quelli ancora aperti compaiono sotto con il loro
numero di allora.

**Lo strumento.** `python3 scripts/domande_developer.py --file …DEF-4…` trova 6
rilievi (D2 ×3 Scena 2, D15 Scena 6, D10 Scena 7, D1 Scena 8), tutti dichiarati
in `plans/domande-developer.json`; `--check` esce 0. Una delle sei ragioni è
sbagliata: vedi 🟡 Y15.

**L'SRD.** Il mirror `skills/dnd-35-srd/references/` è un riassunto: non ha il
testo di *comando*, del talento *Ghermire* (Snatch), della tabella dell'adepto
né le schede di hobgoblin e orco. Dove serviva quel testo ho scritto «da
verificare».

---

## 🟠 Il DM si blocca al tavolo

**O1 · Scena 9, Vatore: la CA e i tempi della ronda non ci sono** (era il #15).
Prova: *«La CA contro cui si tira quel colpo, e in quanti round arriva la ronda
`[INFERRED — needs DM confirmation]`.»* La frase non ha né verbo né numeri.
«Lo feriscono» e «Cercano di ucciderlo» sono due righe della tabella, e il suo
urlo è un allarme (G2-26): al tavolo il DM non sa cosa deve battere il tiro, né
quando arriva qualcuno.
→ Scrivere i due numeri, per esempio «CA 16 [INFERRED]; la ronda in 1d4+2 round,
come per la pattuglia», e farli confermare al DM.

**O2 · Scena 11, «Chi non vola»: mancano i tre poteri di Tordek contro un drago Enorme.**
Prova: la sezione propone a Tordek soltanto la corda e il *«Pugno Stordente»*
preparato. La sua scheda dei Bracieri
(`PG/Artefatti/Artefatti-Pg/Tordek/05_Bracieri_Gemelli_Scheda_PG_Completa.md`)
ha però:
(a) *Diventare una Collina*, che «la prima volta si attiva **da sé**» quando uno
scontro con una creatura Enorme+ lo porta sotto metà pf. Skullcrusher è
Enorme, e stasera potrebbe essere la prima attivazione, che la scheda vuole
«senza preavviso»;
(b) *Salto Fiammeggiante* 3/giorno, un salto verticale fuori dalle regole
normali, che arriva al drago quando picchia basso;
(c) *Castigo del Drago* sui guanti, +2 al potenziamento e +2d6 contro i draghi.
Il modulo dice soltanto che la Cintura rifiuta. Il DM non sa se rifiutano anche
i Bracieri, che sono un altro oggetto, e Roberto glielo chiederà.
→ Una riga in «Chi non vola», prima della corda: «I Bracieri non rifiutano:
Collina (portata 3 m), Salto Fiammeggiante fino al drago in picchiata, Castigo
del Drago valgono come sempre», oppure, se il DM decide il contrario, il rifiuto
scritto anche per loro.

**O3 · Scena 11 e A.1: Skullcrusher ha *Ghermire*, e nessuna tattica lo usa.**
Prova: A.1 *«Talenti: Attacco in Volo, Attacco Poderoso, Fluttuare, Ghermire,
…»* e *«Lotta +40»*. *Ghermire* compare solo nello statblocco. Un drago Enorme
che vola e ha Lotta +40 afferra un nano, sale e lo lascia cadere, oppure lo
porta via, o lo butta nella fucina del cortile (rubrica §12: il pericolo che il
nemico usa). Se il DM legge il talento al tavolo, deve decidere da solo se
Skullcrusher lo usa, contro chi e con quale caduta. Se lo usa, cambia anche
«Chi sceglie»: il bersaglio afferrato non può più chiamarlo. Il testo SRD del
talento è da verificare: il mirror non lo contiene.
→ Una riga nelle tattiche, «Ghermire: lo usa / non lo usa, perché…». Se lo usa:
su chi (per esempio su chi tiene la corda), a che quota lo lascia e quanti
danni fa la caduta (SRD).

**O4 · Scena 8: due regole diverse per decidere se c'è stato un allarme.**
Prova: «Chi accorre al grido»: *«Le ronde di orchi più vicine arrivano alla
tenda in 1d4+2 round»*. Il round 1 di Zog'tar è *«Ira Barbarica (“A ME, CANI!…”)»*,
e con 283 pf il generale arriva sempre al suo primo turno. «Come si decide»
(D51) però conta come allarme solo *«Qualcuno esce dalla tenda a gridare, o
Grask suona?»*. Con Grask già sistemato e nessuno uscito, le ronde arrivano lo
stesso al grido e fanno quadrato attorno al telo, e il testo chiama la cosa
«in silenzio», senza il successo in meno. Il bivio di Artemis, *«uccidere
Zog'tar in **silenzio** (blast mirato) tiene basso l'allarme»*, promette a
Igor un esito che il blast da solo non può dargli: senza una bolla di
*silenzio* sulla tenda il grido c'è comunque.
→ Aggiungere a «Come si decide» una terza domanda («Le ronde sono arrivate
alla tenda? Allora è allarme») e nel bivio di Artemis scrivere «con il
*silenzio* sulla tenda».

**O5 · Scena 7, Balvar «sta con chi sta vincendo»: mancano il criterio e la tattica.**
Prova: *«**Trattativa aperta**, nessuno l'ha minacciato | il primo round guarda.
Dal secondo sta con chi sta vincendo»*. Stasera è il caso più probabile,
perché parlargli durante lo scontro non costa tacche (D39). Il testo non dice
come il DM stabilisce chi vince al round 2: Zog'tar ha 283 pf e non è ancora
ferito sul serio. Non dice nemmeno cosa fa Balvar quando passa dalla parte dei
PG: «Come si combatte» copre solo il Balvar nemico.
→ Una riga sola: «Vince chi ha tolto più di metà dei pf all'altra parte, o
Zog'tar se nessuno ci è riuscito. Con i PG: *dissolvi* sul nemico, la
*barriera* che taglia fuori le guardie, mai contro il generale in faccia».

**O6 · Scene 6 e 8, A.6: le ronde e il sergente non hanno numeri** (era il #9).
Prova: A.6 *«Ronda di orchi | … | quattro orchi SRD (combattente 1, GS 1/2) e
un sergente guerriero 3»*, *«Pattuglia di 4 orchi | complicazione 3 | Guerriero
3»*. Non ci sono CA, pf né attacco. Dopo il grido di Zog'tar, che stasera è
quasi certo (O4), le ronde arrivano a ondate, *«un'altra ogni round»*, e
aspettano chi esce. Il DM ne ha bisogno al primo PG che mette il naso fuori.
Il testo non va d'accordo nemmeno con sé stesso: nella Scena 5 la ronda ha
*«ascia 1d12+3»*, nella Scena 8 *«tirano le lance»*, e l'orco SRD porta un
falcione (da verificare: il mirror non ha la scheda).
→ In A.6, una riga per l'orco combattente 1 e una per il sergente guerriero 3
(CA, pf, attacco, arma), e la complicazione 3 dichiarata uguale alla ronda.

---

## 🟡 Migliorabile

**Y1 · Scene 6-7, Grask stasera: con il volo è sveglio.** Lo stato di Grask si
fissa all'atterraggio, ed è *«sveglio finché l'ultima tacca segnata è la 4ª»*.
Il gruppo parte da 3. Se esce subito in volo (1 tacca), atterra alla 4ª e
**Grask è sveglio**. A piedi (2 tacche), o con una qualunque tacca spesa prima
nella Scena 5, atterra alla 5ª e Grask dorme. Il testo lo permette già, ma il
DM deve fare il conto al tavolo, ed è un conto che rovescia l'intuizione:
volare costa meno tacche e trova Grask sveglio.
→ Una riga in «Chi li può scoprire in volo»: «Con 3 tacche e il volo subito,
Grask è sveglio».

**Y2 · Scene 7-8 e M7-C: il *silenzio* di Balvar copre Grask.** Balvar è a P13
e il *silenzio* ha raggio 6 m. Grask sta a N15, a 3 m. Se Balvar combatte con
Zog'tar e attiva la runa al round 3, il corno che Grask suona al round 3 o 4
(1d4 dopo il primo grido) non fa suono, e per la regola già scritta *«un corno
che non fa suono non chiama nessuno»*. Il drago non arriva per colpa del suo
stesso runaio. Il testo non lo considera.
→ Una riga: «la bolla di Balvar prende anche Grask: se il corno suona dentro,
non chiama» (oppure: il telo ferma la bolla, se il DM preferisce).

**Y3 · Scena 10, la breccia: «colto alla sprovvista» e «l'Occhio lo avverte».**
Prova: *«il primo colpo lo prende colto alla sprovvista, poi l'Occhio di
Ossidiana lo avverte (Appendice A.2)»*. A.2 gli dà Schivare Prodigioso
Migliorato, quindi colto alla sprovvista Zog'tar ha la stessa CA, 26, e non
perde la DES contro un invisibile (lo dice la Scena 8). A.2 inoltre non dà
all'Occhio nessun potere di avvertire: l'Occhio marca un bersaglio e basta.
→ Togliere «colto alla sprovvista»; per l'Occhio scrivere cosa fa contro un
invisibile, o niente.

**Y4 · Scena 8, Via A: Intimidire contro una CD fissa** (era il #14). Prova:
*«Intimidire **CD 22** con la Corona scoperta»*. Nell'SRD Intimidire si tira
contro il livello del bersaglio, quindi a CD fissa è una regola della casa, ma
nessuno la dichiara tale. Il testo non dice nemmeno se la Volontà Indomita di
Zog'tar ci entra.
→ Aggiungere `[regola della casa]` e una parola sulla Volontà Indomita.

**Y5 · Scena 6 e A.6: lo squadrone ha due Ascoltare.** La tabella della
sorveglianza dà agli squadroni *«Ascoltare e Osservare **+2**»*; A.6 dice che
lo squadrone *«ha i numeri della pattuglia dei tre fallimenti»*, che ha
*«Ascoltare e Osservare −1»*.
→ Tenere un solo valore.

**Y6 · Scena 11 e §8 A: le wyvern di stasera mancano dappertutto tranne nella sidebar.**
Per G2-15 il gruppo di stasera (fiducia piena, artefatti, banco speso) conta
come straripante, quindi le 2 wyvern ci sono dal round 2. Mancano però nel
budget PX di §8 A, nella regia dei primi due round, in «Chi non vola», dove
sarebbero proprio ciò che i PG a terra possono colpire quando scendono a
pungere chi tiene la corda, e nella Quick-Reference. L'EL del duello con le
wyvern non è scritto da nessuna parte.
→ Una riga in §8 A e una in «Chi non vola»; l'EL accanto alla sidebar.

**Y7 · Scena 5 e Scena 11: la runa di Zeth si può attivare al corno dell'alba.**
Prova: *«va attivata quando il drago compare»* e, nella Scena 11, *«la attiva
adesso, con un'azione standard»*. La runa dura 70 minuti. All'alba il corno
suona circa 7 minuti prima che il drago arrivi, e i PG sono sulle mura a
sentirlo. Attivarla lì è legale, e il modulo spinge il tavolo a spendere
l'azione del round 1.
→ «Si può attivare al corno: dura più del volo del drago».

**Y8 · Scena 8: «Benedizione della Forgia» è il nome di due cose diverse.**
Prova: *«THORIK — Benedizione della Forgia: … +2 sacro ai danni»*. Sui
Bracieri di Tordek la *Benedizione della Forgia Eterna* è la fonte delle 4
cariche, e *Benedizione della Forgia — Frantumare* è un altro potere ancora.
Se Roberto al tavolo dice «uso la Benedizione della Forgia», il DM ha due
candidati.
→ Rinominare la scelta di Thorik, per esempio «la preghiera a Moradin».

**Y9 · Scena 8: il Colpo Devastante contro il telo del glifo.** Zog'tar scaglia
un PG *«contro il palo o fuori dal telo»*. Il telo dietro il seggio (L14–N14)
porta il glifo legato ai nani. Il testo non dice se un nano scagliato lì lo
fa scattare, con 5d8 sonori e il boato, che è un allarme. È il pericolo della
mappa che il nemico può usare (rubrica §12).
→ Una riga: «scagliato contro il telo del seggio, un nano fa scattare il
glifo» (oppure no).

**Y10 · Scena 8: i rinforzi arrivano senza un segno** (rubrica §14). I tempi
di ronde e squadroni ci sono, ma niente dice come se ne accorgono i PG prima
che il telo sia circondato: torce, passi, un ordine gridato fuori.
→ «Un round prima: torce che si muovono sul telo e un ordine in goblin».

**Y11 · Scena 11, *Fluttuare* e le macerie.** A.1 ha *Fluttuare* (Hover);
nelle tattiche non compare, e nel cortile ci sono macerie (M7-B, righe 6 e
12). L'effetto della polvere sollevata da un Enorme in volo basso va
verificato sull'SRD, che il mirror non ha.
→ Dire se lo usa; se no, una parola sul perché.

**Y12 · Bestiario, Skullcrusher: la scheda dà ancora il drago di prima.**
`Bestiario/villain/skullcrusher-il-nero-cr12.md` ha **CR 12** nel campo che
legge `suggest_encounter`, e la sua riga `Source` dice *«GS 12: CA 27, PF 240,
soffio acido 12d4 CD 24»*. La riga rimanda anche a `ERRATA-ARC07-35-Verification.md`
§2.3, che ha gli stessi numeri vecchi. A.1 dice GS 14, CA 33/37, 297 pf, 14d4
CD 28, e lo stesso file nel suo `Boost log` dice CR 14. Il booklet di stasera
usa A.1, quindi la serata non si rompe; la rompe un DM che prepara dal
Bestiario.
→ CR 14 nel campo, la riga `Source` allineata ad A.1, una nota d'errata su §2.3.

**Y13 · Bestiario, Balvar.** Nella scheda
(`Bestiario/villain/balvar-fuocospento-cr13.md`, «Notes») Zog'tar è *«(CR
14)»*; A.2 e la sua scheda gli danno GS 15. Lo statblocco incluso in A.4
coincide con il Bestiario. Ho controllato CA 24, contatto 14, pf 101, TS
+13/+8/+17, BAB +9, *barriera di lame* CD 21, *slay living* CD 20 e *comando
superiore* CD 20.
→ «CR 15».

**Y14 · Treant di Adamantio: FOR 28 o 29.** La Scena 5 e A.6 dicono *«FOR 28»*;
`DEF-3` A.2 e la nota della scheda `Bestiario/mostri/treant-di-adamantio-cr10.md`
dicono **FOR 29**. Gli altri numeri coincidono (90 pf, CA 24, RD 10/adamantio,
schianti +18, 2d8+9).
→ FOR 29 in DEF-4.

**Y15 · `plans/domande-developer.json`: la ragione del D1 sulla Scena 8 è falsa.**
La ragione dice *«il drago non combatte nella Scena 8»*. La Scena 8 ha invece
«Il corno e il drago sulla tenda», con la sua tattica e un EL 18-19. Il
rilievo resta un falso positivo per un'altra ragione: la risposta per chi
resta a terra c'è, ed è *«L'uscita è il telo tagliato e il buio fuori»*.
→ Correggere la ragione con questa citazione.

**Y16 · A.6: «nessuna ha una scheda sua nel repo» non è vero.** `Bestiario/mostri/`
ha `worg-cavalcatura-cr2.md` (51 pf, morso +9 1d8+4),
`goblin-warrior1-cr05.md`, `orco-regular-warrior4-cr3.md` e altre schede, ma
sono della Mano Rossa del 1372 e non coincidono con il worg SRD di A.6 (30 pf,
morso +7 1d6+4), che per il 372 è quello giusto. Chi le cerca prende quelle
sbagliate.
→ «Le schede di `Bestiario/mostri/` sono del 1372: qui valgono quelle SRD».

**Y17 · Da verificare sull'SRD, che il mirror non contiene.**
(a) Grask, *«Ascoltare e Osservare +2»*: per quanto ricordo, l'hobgoblin SRD ha
Ascoltare +2 e Osservare +0. Stasera conta, perché all'atterraggio si tira
Nascondersi contro il suo Osservare (Y1).
(b) *Comando* «Cadi» su chi vola: *«Chi vola **scende fino a terra** nel suo
turno, senza danni da caduta»* è attribuito all'SRD, ma il mirror non ha il
testo dell'incantesimo, e sembra una regola del DM.
→ Confrontare tutti e due con d20srd.org prima della stampa; se il secondo è
una scelta del DM, marcarlo `[CANONE — DM]`.

---

## Le sedici domande sulle Scene 5-11

✓ risponde · ◐ in parte (rilievo) · ✗ no · — non si applica.

| # | Domanda | Verdetto |
|---|---|---|
| 1 | Tier: chi non ha niente da fare | ◐ tenda ✓ (Cintura, Via A, Treant); duello ◐: le corde ci sono, i poteri di Tordek no (O2) |
| 2 | Volo, invisibilità, silenzio | ✓ campo, variante dall'alto, tenda (soglia, glifi, bolla), Vatore; stasera Grask sveglio col volo (Y1) |
| 3 | Tempra, Riflessi, Volontà | ✓ tenda (*slay living*, barriera, *comando*); duello ✓ stasera grazie al veleno delle wyvern |
| 4 | Chi sente il rumore | ◐ due definizioni di allarme (O4); il corno sotto il *silenzio* di Balvar (Y2); la ronda di Vatore (O1) |
| 5 | Il boss cambia | ✓ Zog'tar 30%, Balvar sotto 30 pf, Skullcrusher a ⅓ e la corda |
| 6 | Skill challenge per intero | ✓ chi, cosa, CD, quanti, costo, azzeramento dopo la pattuglia |
| 7 | Chi si diverte | — profili veri del gruppo |
| 8 | Ogni scontro possibile ha la tattica | ◐ ronde senza numeri (O6); Balvar che cambia parte (O5); Vatore senza CA (O1); *Ghermire* (O3) |
| 9 | Segreto e divinazione | ✓ blocchi «Se lo divinano» per Balvar e per Vatore |
| 10 | Riga di scala | ✓ Scene 6, 8, 10, 11 (la 7 rimanda alla 8) |
| 11 | Il mostro insostituibile | ✓ Catena, nome detto prima del colpo, Occhio, lastra d'ardesia |
| 12 | Il pericolo che qualcuno usa | ◐ la caduta dal camminamento sì; fucina e cisterna solo per i PG; il glifo del telo (Y9) |
| 13 | L'incontro resta uno | ✓ tenda a ondate dichiarate; la breccia è un incontro suo con EL |
| 14 | Il rinforzo che si vede arrivare | ◐ il drago sì (corno, ombra sul telo); le ronde no (Y10) |
| 15 | Niente dossi | ✓ pattuglia (esenzione dichiarata), ronde «sopra il tetto per scelta» |
| 16 | Il PG fuori gioco per un TS | ✓ *comando superiore* con nuovo TS a ogni turno; *slay living* con la via del ritorno; telo con Riflessi a ogni round |

## I numeri ricontrollati che tornano (Scene 5-11)

Zog'tar in A.2 (CA 26 col mithral, iniziativa +9, giavellotti +19, 1d8+13).
L'adepto 7 del sacerdote (3/4/3, *comando* CD 13). Il worg SRD. Le wyvern SRD.
Le pozioni di *volare*: 5 minuti, 12 m in armatura, 1 km in 42 round contro i
70 del drago. La caduta di 4,5 m, 1d6. Il gancio contro il contatto 10 del
drago, con −2 per incremento. La Presenza a 63 m. Lo stregone di 5° (6/7/5).
Le coordinate di M7-C coincidono con il testo: il telo a sinistra è il fianco
est, e Grask a N15 sta due quadretti dietro il seggio.

🔴 0 · 🟠 6 · 🟡 17
