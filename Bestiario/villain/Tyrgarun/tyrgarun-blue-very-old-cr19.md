# Tyrgarun — Blue Very Old Dragon (Sky-Terror of Rethmar) [CANONE — DM 2026-07-02, D11 v2]
**Faction**: red-hand | **Role**: aerial-hazard / grounded-boss | **Environment**: aerial | **CR**: 19 (aerial hazard) → **16–17** (grounded, Fase 4) | **Source**: MM p.71 Blue Dragon Very Old (SRD 3.5) | **Status**: accepted


```statblocco
gs: 19
taglia: Enorme
spazio: 4,5 m
portata: 3 m (4,5 m con il morso)
ca: 40
ca-dettaglio: (-2 taglia, +29 naturale, +3 deviazione); contatto 11, colto alla sprovvista 40
pf: 405
pf-dado: 30d12+210
ts: Temp +27, Rifl +22, Vol +26
attributi: For 33 Des 10 Cos 25 Int 18 Sag 19 Car 18
velocita: 12 m, scavare 6 m, volare 45 m (scarsa)
iniziativa: +4
attacchi:
  - Mischia morso +39 (2d8+11); 2 artigli +37 (2d6+5); 2 ali +37 (1d8+5); coda +37 (2d6+16); stritolamento (2d8+16)
voci:
  - Soffio: linea 30 m, 20d8 elettricità, Rifl CD 32 dimezza, 1 ogni 1d4 round
  - Presenza terrificante 72 m, Vol CD 29
  - RI 25; RD 15/magia; immune a elettricità, paralisi e sonno
  - Incantesimi da stregone di 11° livello, al giorno 6/7/7/7/6/3, CD 14 + livello
  - Equipaggiamento: anello di protezione +3, mantello della resistenza +3, 2 pergamene di catena di fulmini (LI 11, Rifl CD 19), 1 pergamena di dissolvi magie superiore (LI 11), 3 pozioni di cura ferite gravi
fonte: corpo del drago blu molto vecchio dell'SRD 3.5 (30 DV) con Cos 25 e soffio 20d8 della scheda; conti rifatti sull'SRD
```

> [CANONE — DM 2026-09-23, D2] correzione 3.5 da `scripts/conformita_statblocchi.py`: **D2, deciso dal DM il 2026-09-23: lotta +46 → +49**: BAB +30 + Enorme (+8) + For 33 (+11). La For 33 la confermano il morso +38 (2d8+11), gli artigli e le ali (+5, metà For), la coda e lo stritolamento (+16, For e mezzo): la lotta era il solo numero che non tornava.

> [GENERATO] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

> `[CANONE — DM 2026-11-14]` Categoria d'età e grado di sfida: da «Old», GS 18, a **molto vecchio (Very Old), GS 19**. I 30 DV e il +29 di armatura naturale della scheda sono quelli del blu molto vecchio dell'SRD 3.5, che ha GS 19. Il file si chiamava `tyrgarun-blue-old-cr18.md`: il cancello di `extract_statblocks.py` vuole nel nome il GS del blocco. Il GS «16–17» a terra della Fase 4 non è stato ricalcolato.

> **Nota rinomina (2026-07-02, D11 v2 / A7)**: file precedentemente
> `tyrgarun-black-adult-cr13.md` (black adult, riserva). Corretto a **blue Old
> CR 18** per allineamento a **state.md §2.2**, INDICE, ARMATE-SYNC §2.1 e
> STRUTTURA §4-7/§9. Tyrgarun **NON è la cavalcatura di Azarr Kul**: è il
> **terrore dei cieli** della battaglia (D11 v2). Le meccaniche del set-piece
> (hazard di bombardamento, contromosse, inchiodamento del Mythal) vivono in
> `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA.md` §9.4 (C1.d).

---

## Profilo AEREO (Fasi 1-3) — *hazard, non incontro frontale*

A CR 19 in volo con Flyby è **imbattibile per design** per un party APL 14: si
gioca come **pericolo ambientale con contromosse quantificate** (vedi STRUTTURA
§9.4), non come statblock da azzerare a iniziativa.

**Size/Type**: Huge dragon (earth)

**Iniziativa** +4

**Difesa** **AC**: 40 (-2 taglia, +29 naturale, +3 deviazione), contatto 11, colto 40 · **HD**: 30d12+210 (**405 HP**) · **Saves**: Fort +27, Ref +22, Will +26 (con il +3 di resistenza del mantello) · **SR (RI)**: 25 | **DR (RD)**: 15/magic | **Immune**: elettricità, paralisi, sonno

**Attacco** **Speed**: 12 m, scavare 6 m, **volare 45 m (scarsa)**
**Attack**: Morso +39 mischia (2d8+11)
**Full**: Morso +39 (2d8+11), 2 artigli +37 (2d6+5), 2 ali +37 (1d8+5), coda +37 (2d6+16), stritolamento (Huge) 2d8+16
**Breath weapon (soffio)**: **linea 30 m, 20d8 elettricità**, Ref **CD 32** dimezza (10 + ½ DV + Cos), 1/1d4 round — *usato dall'alto sui bastioni come hazard di bombardamento*

**Tattiche**
- *Prima del combattimento e durante (profilo aereo, Fasi 1-3)*: resta in **volo alto**, alterna passate di soffio sui camminamenti e Snatch sulle balliste/serventi. **Non atterra mai** finché il Mythal non lo inchioda (Fase 4).
- *Il corredo, Fasi 1-3* `[CANONE — DM 2026-11-21, card]`:
  - *Catena di fulmini.* Le due pergamene le legge in volo sui camminamenti, nei round in cui il soffio si ricarica. Fanno 11d6 di elettricità al primo bersaglio (in media 38) e metà a un massimo di undici bersagli secondari entro 9 m dal primo; ognuno ha un TS Riflessi CD 19 per dimezzare e la resistenza agli incantesimi. Il primo bersaglio è chi lo minaccia di più, un servente di ballista o un PG che lancia; i secondari sono i serventi e la milizia attorno.
  - *Dissolvi magie superiore.* La legge sulle protezioni del Circolo degli Otto quando il cerchio del Mythal comincia a chiudersi, prima che si completi: ad area sul gruppo dei ritualisti, o mirata sull'arcimago che ha più incantesimi addosso. Ogni prova è d20 + 11 contro CD 11 + il livello d'incantatore di chi ha lanciato l'incantesimo: contro arcimaghi di alto livello riesce di rado, e lui lo sa.
  - *Mai sul Mythal.* *Dissolvi magie* non lo tocca: è un campo simile a un Mythal (`Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA.md` §7 r.181), e un mythal non si dissolve. A cerchio chiuso restano l'ancoraggio, che cerca di spegnere a terra (Fase 4, qui sotto), e la rottura del campo col tiro di `Arco-Post-Hammerfist-P2D-PALIO-CHANNATHGATE-INTEGRAZIONE.md` §4.2 r.194-197, che non dipende da lui.
  - *Le pozioni.* Le beve in volo dopo la fuga sotto 80 pf, una per round (3d8+5 l'una, in media 55 pf in tutto).
- *Lo stregone, Fasi 1-3* `[CANONE — DM 2026-11-15]`:
  - *All'alba* lancia *pelle di pietra*: 110 minuti, tutta la battaglia, e assorbe 110 danni da arma.
  - *Gli inganni.* Con *imitazione dei suoni* dà ordini falsi con la voce dei comandanti («ritirata dal bastione est!»; chi ascolta fa un TS Volontà CD 29 per accorgersene). Con *terreno allucinatorio* (1 al giorno) mostra una breccia che non c'è.
  - *L'invisibilità.* Le prime passate di soffio le fa da *invisibilità superiore*, ma la sorpresa vale per intero una volta sola: quando un incantesimo dei PG lo rende di nuovo visibile, cambia settore e torna a combattere visibile.
  - *Il Mythal.* Quando il cerchio comincia a chiudersi lancia *immagine speculare*, e colpisce chi tiene il focus con *telecinesi* (spinta violenta) o con un *fulmine* dall'alto.
  - *Artemis.* Artemis vede l'invisibile (invocazione *See the Unseen*, `PortaleForgia-P1-REVISED-Corretta.md` r.249), e all'inizio Tyrgarun non lo sa: nessuno dei suoi informatori l'ha visto contro un invisibile `[CANONE — DM 2026-11-15]`. Se ne accorge la prima volta che un suo colpo lo trova senza esitare mentre è invisibile. Da lì Artemis è per lui l'occhio del gruppo, e il primo *fulmine* dall'alto va su di lui, prima ancora di chi tiene il focus.
  - *Se lo sa dall'inizio.* Se Ozyrrandion è fuggito dalla Torre Invisibile e lo sapeva (con la *porta dimensionale* può fuggire prima di essersene accorto), e combatte accanto a lui nella seconda ondata, Tyrgarun lo sa fin dall'inizio: non apre con l'invisibilità sul settore di Artemis, la usa solo dove Artemis non ha la linea di vista `[CANONE — DM 2026-11-15]`. Lo sa anche dai reduci di Hammerfist, se là Artemis ha colpito Fauci di Palude mentre era invisibile `[CANONE — DM 2026-11-21, card]`: in quel caso fa lo stesso anche senza Ozyrrandion.
  - *Che cosa sa del resto.* Dell'ascia che canta e del nano che non trema sa da chi è tornato da Hammerfist; del Mythal sa che il Circolo degli Otto prepara qualcosa, non che cosa, finché non lo vede.
- *A terra (Fase 4)*: costretto alla mischia, usa stritolamento, coda e morso; cerca di sfondare verso il cerchio del Mythal per spegnere l'ancoraggio (se lo raggiunge e uccide un PG-focus, riguadagna il volo). Le pozioni in Fase 4 `[CANONE — DM 2026-11-21, card]`: col Mythal chiuso non può fuggire, ma bere costa l'azione standard, rende in media 18 pf e provoca un attacco di opportunità da ogni PG in mischia, mentre un attacco completo vale in media una cinquantina di danni su un PG con CA 30, e il soffio, quando è pronto, di più. Finché ha un PG in portata o in linea di soffio attacca e non beve. Beve solo nel round in cui non raggiunge nessuno, perché si è sganciato o perché i PG lo tengono a distanza dietro le mura: allora si muove verso il cerchio e beve.
- *Morale*: Se le contromosse dei PG (balliste, gufi Tiri Kitor, esca) hanno successo ripetuto, sceglie di ritirarsi 1d4 round per ricaricare — *non* di ingaggiare corpo a corpo.
- *Morale — trigger di fuga (nemesi ARC-10)*: se ridotto sotto **80 pf** *prima* che il
  Mythal sia completo, Tyrgarun **fugge** (scavare + volo appena fuori area) e
  diventa una **nemesi ricorrente** per campagne future. Se il Mythal è già attivo
  quando scende sotto 80 pf, **non può fuggire** e va abbattuto.

**Statistiche** **Abilities**: For 33, Des 10, Cos 25, Int 18, Sag 19, Car 18 · **BAB/Grapple**: +30/+49
**Feats**: Flyby Attack, Hover, Wingover, Multiattack, Power Attack, Cleave, Improved Initiative, Snatch, Wingstorm `[Private source — Savage Species, p. 40]`, Riflessi Fulminei, Volontà di Ferro — undici, quanti ne dànno 30 DV; gli ultimi due spiegano il Ref +19 della scheda e portano Will a +23, prima del mantello della resistenza +3 (con il mantello Ref +22, Will +26)
**Skills**: Spot +37, Listen +37, Nascondersi -4 (Huge), Raggirare +25, Concentrazione +30
**Incantesimi** da stregone di 11° livello (Car +4), al giorno 6/7/7/7/6/3, CD 14 + livello, la scheda non li elencava; conosciuti — 0: *individuazione del magico*, *mano magica*, *prestidigitazione*, *lettura del magico*, *suono fantasma*, *messaggio*, *resistenza*, *luce*, *frastornare*; 1°: *scudo*, *dardo incantato*, *colpo accurato*, *allarme*, *ritirata rapida*; 2°: *vedere invisibilità*, *immagine speculare*, *raffica di vento*, *resistere all'energia*, *invisibilità*; 3°: *dissolvi magie*, *velocità*, *fulmine*, *protezione dall'energia*; 4°: *invisibilità superiore*, *pelle di pietra*, *porta dimensionale*; 5°: *muro di forza*, *telecinesi*
**Equipaggiamento** `[CANONE — DM 2026-11-21, card]` (corredo «A · Tempesta e ferro»): anello di protezione +3 (18.000 mo; +3 di deviazione alla CA, che vale anche a contatto e colto alla sprovvista), mantello della resistenza +3 (9.000 mo; +3 di resistenza ai tiri salvezza, che non si somma con l'incantesimo *resistenza*), 2 pergamene di *catena di fulmini* LI 11 (1.650 mo l'una), 1 pergamena di *dissolvi magie superiore* LI 11 (1.650 mo), 3 pozioni di *cura ferite gravi* LI 5 (750 mo l'una; 3d8+5 pf). Totale 34.200 mo, il 24% del tesoro triplo a GS 18 (3 × 47.000 = 141.000 mo: il tesoro standard per GS è della Guida del DM 3.5, «Treasure Values per Encounter», il triplo dell'SRD, «Treasure: Triple standard»). A GS 19, quello del blocco, il tesoro triplo è 183.000 mo e il corredo ne vale il 19%. Le pergamene le usa da stregone. Tutti e due gli incantesimi sono nella lista del mago e dello stregone (6° livello), e Car 18 supera il 16 che serve per un incantesimo di 6°. Il livello dell'incantatore delle pergamene (11) è uguale al suo, quindi non tira la prova di livello dell'incantatore: per l'SRD scatta solo quando la pergamena ha un livello più alto di chi la legge. Le decifra con *lettura del magico*, che conosce. Le CD sono quelle della pergamena e non le sue: *catena di fulmini* Riflessi CD 19 (10 + 6 + 3, il minimo di Carisma per il 6°), *dissolvi magie superiore* con prova di dissolvere d20 + 11. Leggere una pergamena e bere una pozione sono azioni standard e provocano attacchi di opportunità.

**Capacità speciali**
- **Presenza Terrificante**: CD 29 (10 + ½ DV + Car), 72 m (creature con < 30 DV, Will o scosse/panico)
- **Special**: creare/distruggere acqua (a volontà (non SRD: l'SRD dà 3/giorno)), imitazione suoni (a volontà), ventriloquio 3/giorno, terreno allucinatorio 1/giorno, velo 1/giorno (non SRD: l'SRD lo dà dal drago antico)
- **Tempesta d'ali** (Wingstorm) `[Private source — Savage Species, p. 40]`: in volo stazionario, raffica che spegne fiamme e abbatte le creature piccole.
> ⚠ Prerequisito: Wingstorm chiede Hover e Flyby Attack, che ha; il *velo* chiede l'età antica (SRD), qui tenuto perché la Fase 4 lo nomina. PF1e: nel Bestiary il blu prende *veil* solo da antico, come in 3.5; anticiparlo di un'età si avvicina, non stravolge.

---

## Profilo A TERRA (Fase 4) — *uccidibile solo se arriva ferito e con gli alleati*

Il **Mythal del Circolo degli Otto** (STRUTTURA §7, canone P2D-INTEGRAZIONE
r.201) **gli nega il volo** entro l'area protetta. Senza Flyby/kiting il suo CR
effettivo scende a **~16-17**: epico ma battibile da party APL 14 + alleati.

> `[CANONE — DM 2026-11-15]` **Il «GS 16-17» non regge.** Il Mythal toglie il volo ma non il
> soffio da 20d8 (CD 30 con il −2): contro i soli PG, intatto, li travolge in
> due-tre round (almeno un PG morto nel 59-80% delle prove). La Fase 4 è
> battibile se valgono tutte e due le condizioni: **Tyrgarun arriva sotto i 250
> pf** (le contromosse delle Fasi 1-3 lo hanno logorato) **e combattono le
> statue-golem e gli alleati**. Così il modello lo dà ucciso nel 21-40% degli
> scontri col corredo del 2026-11-21 (CA 40, TS +3; senza corredo era il 23-45%), con la stima
> degli alleati di 40 pf a round e metà dei suoi round su di loro. Il modello non conta le
> pergamene, che spende nelle Fasi 1-3, né le pozioni, che in Fase 4 non beve finché ha un bersaglio.
> In Fase 4 combatte come scritto sotto, senza scavare sotto il cerchio: con lo
> scavo e una *pelle di pietra* piena non muore quasi mai. La *pelle di pietra*
> dell'alba conta solo per quel che ne resta: ogni colpo da arma delle Fasi 1-3
> (balliste comprese) ne consuma fino a 10 dei 110, e il DM tiene il conto. Se il
> Circolo la dissolve prima, la Fase 4 si gioca senza. Simulazione:
> `plans/esperimenti/tattiche-draghi-2026-11-15/`.

**Differenze dal profilo aereo:**
- **Speed**: 12 m, scavare 6 m — **niente volo** (Mythal attivo). Se il Mythal cade, torna al profilo aereo.
- **Soffio**: invariato (20d8 linea, CD 32) ma ora **tracciabile a terra**: i PG possono spezzare la linea di tiro con copertura/mura.
- **Malus da Mythal (già canone STRUTTURA §7)**: -2 a tutti i tiri per colpire e TS, niente teletrasporto/*velo* offensivo.
- **Difesa a terra**: CA 40, contatto 11, colto 40 (il Mythal non tocca la CA); tiri salvezza del blocco, mantello compreso, meno 2 per il Mythal.
- **Tattica**: vedi **Tattiche** qui sopra, *A terra (Fase 4)*.

---

**Cross-ref**: state.md §2.2 · INDICE r.27/443 · ARMATE-SYNC §2.1/§4-Fase1 ·
STRUTTURA §4/§5/§7/§9.4 · `Bestiario/villain/Azarr_Kul/Azarr_Kul/Azarr_Kul.md` (Tyrgarun NON cavalcatura).

Benchmark: PF T1-1 riga 18: CA 40 sopra (33) / pf 405 sopra (300) / attacco +39 sopra (+28) / danno pieno ~100 in linea (100) / CD 32 sopra (25) / TS buono +27 sopra (20). Il corpo è quello del blu molto vecchio dell'SRD (GS 19), con Cos 25 e soffio 20d8: al tavolo vale GS 19-20 in volo. Il file lo tiene a 18, sopra il tetto EL dell'APL 13 (+4 = 17): resta un pericolo da negare, non un nemico da abbattere, finché il Mythal non lo inchioda.

Boost log: conti rifatti sull'SRD del blu molto vecchio, nessun numero sceso — GS 18 → 18 (il corpo vale 19-20) — armatura naturale +29 dell'SRD, CD del soffio da 10 + ½ DV + Cos, due talenti liberi su undici, incantesimi da stregone di 11° livello che il drago ha per l'SRD e la scheda non scriveva.

Boost log: 2026-11-21 — corredo dal tesoro triplo, card «A · Tempesta e ferro», nessun numero sceso — GS 18 → 18 (il blocco dice 19 dal 2026-11-14; il corpo vale 19-20) — anello di protezione +3 e mantello della resistenza +3 (CA 37 → 40, contatto 8 → 11, colto 37 → 40, TS +3), due pergamene di *catena di fulmini*, una di *dissolvi magie superiore* e tre pozioni di *cura ferite gravi*, per 34.200 mo dentro il tesoro triplo: gli oggetti escono dal tesoro e non alzano il GS. Il tetto EL dell'APL 13 (+4 = 17) era superato già prima del corredo, e il file lo dichiara: in volo resta un pericolo da negare, a terra si abbatte solo ferito, col Mythal e con gli alleati.

> <!-- storico -->
> era: CA 35 (+27 naturale), colto 35, da prosa d'origine.
> era: Vol +22, morso +38, artigli, ali e coda +36, da prosa d'origine.
> era: soffio Ref CD 29, presenza terrificante 55 m, da prosa d'origine.
> era: nove talenti su undici, nessun incantesimo, da prosa d'origine.
> era: CA 37, contatto 8, colto 37; TS Temp +24, Rifl +19, Vol +23; nessun oggetto, prima della card del 2026-11-21.
> <!-- /storico -->
