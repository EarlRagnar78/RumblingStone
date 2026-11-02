# Correzioni di DEF-4 e del booklet della serata (giro 4, 2026-10-19)

Questo file dà una riga per ogni rilievo di `DM.md`, `DEVELOPER.md`,
`PLAYTESTER.md` e `../COERENZA-PNG-MAPPE.md`. Ogni riga dice se il rilievo è
**corretto**, **lasciato** o **al DM**. Al DM vuol dire che la domanda è in
`../DECISIONI-DM.md` e che il testo porta la proposta come riga
`[INFERRED — needs DM confirmation]`.

Nella tabella le sigle stanno per questi file:

| Sigla | File |
|---|---|
| DEF-4 | `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` |
| regia | `homebrew/sessione-notte-e-alba/01-REGIA-SERATA.md` |
| intro | `homebrew/sessione-notte-e-alba/00-INTRO-DOVE-SIAMO.md` |
| Seme | `homebrew/sessione-notte-e-alba/02-IL-SEME.md` |
| echi | `homebrew/sessione-notte-e-alba/03..06-ECHI-*.md` |
| Atlante | `Mappe/ARC07-MAPPE-DEFINITIVO.md` |

**Conti.**

| Esito | Rilievi |
|---|---|
| corretti | 68 |
| corretti solo in parte | 5 |
| lasciati | 3 |
| al DM | 24 |
| **in tutto** | **100** |

I rilievi al DM diventano 27 voci in `DECISIONI-DM.md`, perché i rilievi si
toccano: una voce può venire da più rilievi, e anche alcuni rilievi corretti
portano una proposta da confermare.

## Note da applicare fuori dal mio perimetro

**`plans/domande-developer.json`, D1 sulla Scena 8 di DEF-4** (DEV Y15). Non ho
toccato il file. Questo è il nuovo testo della `ragione`, da applicare tu:

> falso positivo: la Scena 8 ha il drago sulla tenda («Il corno e il drago
> sulla tenda»), ma la risposta per chi resta a terra c'è: «L'uscita è il telo
> tagliato e il buio fuori»

**Il Rubino ha un nome solo.** In DEF-4 (circa r.167 e r.3521) «Cuore della
Leggenda» chiamava il Rubino, e ora è «la Possanza Nanica», come nella scheda
dell'artefatto in `PG/Artefatti/`. Nella scheda «Cuore della Leggenda» resta
il sacrificio del Rituale 3, un'altra cosa, e lì non l'ho toccato.

**Il saldo della fucina segue D43.** Su tua indicazione DEF-4 Scena 5 dice
19.603 mo pagate, senza trattenuta. Prima diceva «ne servono circa 21.800»,
con la marca `[CANONE — DM 2026-10-18, G2-56]`. Le due decisioni del DM si
contraddicono, quindi ho chiesto conferma (`DECISIONI-DM.md` n. 10).

**Skullcrusher non è rinominato.** Su tua indicazione il file resta
`skullcrusher-il-nero-cr12.md`. Per questo resta 12 anche il campo `CR`
dell'intestazione: `validate_bestiario.py` boccia un campo diverso dal numero
nel nome del file. Il GS 14 vero è nella riga `Source` (CA 33/37, 297 pf,
soffio 14d4 CD 28) e in una nota. Il catalogo di `suggest_encounter` legge
ancora 12. Per portarlo a 14 servono tre cose: rinominare il file in `-cr14`,
seguire i rimandi e rigenerare `scripts/monster_catalog.yaml`. È un lotto a
parte, e lo decidi tu.

**`APPARATO-ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` è rigenerato** con
`componenti.py --apparato`. È il file che il master genera, e
`componenti.py --check` lo voleva allineato.

## DM a freddo (`DM.md`)

| # | Esito | Come |
|---|---|---|
| R1 | corretto | Regia §2: due conti delle tacche, in volo 3 + 1 + 1 = 5 con una tacca libera, a piedi 3 + 3 = 6. C'è anche la riga di Grask: sveglio se l'ultima tacca è la 4ª, addormentato dalla 5ª, e lo stato si fissa all'atterraggio. Il Seme ha una nota in testa (passo 3: «verso le 7» è il conto a piedi, in volo si arriva a 6 e Grask dorme). M7-C è allineata |
| O1 | corretto | Regia §2: dopo gli echi entra Durin con «Quando uscite?», poi il Seme. DEF-4 §0 dice che la prima battuta viene dopo gli echi |
| O2 | corretto | Regia §2, passo 0: chiudere le richieste aperte e chiedere chi porta cosa. Il Seme dice che la pergamena di *identificare* (125 mo) si compra lì. Nel registro §6 c'è la riga |
| O3 | corretto | Le pozioni d'invisibilità sono tre, le due comprate più la n. 10, e ognuna copre mezzo blocco: regia §1 e §3, intro |
| O4 | corretto | Regia §4: la quarta voce sono le wyvern dal round 2. In DEF-4 il morso è nella sidebar e i numeri sono in A.6. M7-B ha due mark W2 e X2 |
| O5 | corretto | Regia §4: il dado dei caduti alla Scena 10, quattro tiri. Nel registro §6 c'è la riga |
| O6 | corretto | Regia §1, tabella «Cosa hanno in mano»: rune, *velocità*, Benedizioni con la domanda sulle 24 ore, i tre Doni di Hella e la guarigione rapida, il blast a 6d6, i Bracieri, Aegis Fang |
| O7 | corretto | Regia §1: una lista di lettura da un'ora, che sostituisce quella di DEF-4. Regia e DEF-4 §0 dicono tutte e due che per stasera vince la regia |
| O8 | corretto in parte | Il Seme, in testa: al passo 5 non si leggono le otto clausole, ma «In breve» di DEF-4 e il box finale. Il ✉ del contratto manca: va aggiunto al manifest dei giocatori, che è fuori dal mio perimetro (`DECISIONI-DM.md` n. 27) |
| O9 | corretto | Echi: fuori dal blocco consegna c'è «Ad alta voce si legge solo il riquadro qui sotto.» e «Solo per te: questa riga non si legge agli altri.», così le due frasi arrivano anche sulla stampa. La regia §1 lo dice ad alta voce. Corretto il testo, non il generatore |
| V1 | corretto | Regia: c'è il paragrafo «Chi si oppone» (Zog'tar, Balvar, Skullcrusher) |
| V2 | lasciato | I grassetti di servizio della regia sono le etichette della tabella del §0. Quelli d'apparato di DEF-4 non sono nei rilievi di stasera |
| V3 | corretto | Con O7 |
| Y1 | corretto | Regia §0: i 25 minuti da tagliare. DEF-4 Scena 6: Grask sveglio se si vola subito |
| Y2 | corretto | Intro N4: Durik è sempre presente, tranne nel campo (postierla o terzo seme) |
| Y3-Y6 | al DM | L'✉ delle boccette è fuori dal mio perimetro (n. 27) |
| Y7 | corretto | Eco di Tordek: «Gunnvor apre» è diventato «la maestra armaiola apre». Il box è cambiato e il cancello passa |
| Y8 | al DM | Il gesto dell'ascia al consiglio (n. 18). La frase lunga dell'eco di Thorik è lasciata: il box è sotto il tetto e il cancello non segnala niente |
| Y9 | al DM | Cosa dicono i Bracieri (n. 19) |
| Y10 | corretto | Cassetta: nel cast e nella pronuncia ci sono Brynja, Kettra, Gunnvor, Hrodgar, Hald e Grask. I cue puntano alle Scene 10 e 11. Il momento di DEF-4 è il colpo finale del duello, mentre il gesto con l'ascia (Scena 4) è già stato giocato. Thorgrim vuole «l'ascia», non «il martello» |
| Y11 | corretto | Forgia Ricorda: tre rimandi da «Scena 5» a «Scena 11 di DEF-4», più la nota che N arriva a 3 quasi sempre |
| Y12 | corretto | Regia §1: la giocatrice usa la sua copia della scheda di Durik del 25, o il DM le passa il capitolo VI (n. 26) |
| Y13 | corretto | Regia §1: la guarigione rapida 1 su terra o pietra, sospesa il round dopo un danno da fuoco |
| Y14 | corretto | DEF-4 Scena 5: 19.603 mo, D43 (n. 10) |
| Y15 | corretto | DEF-4 Scena 5: «ne ha comprate due» |
| Y16 | al DM | L'ordine fra resistenza e vulnerabilità su Durik va verificato sull'SRD (n. 23) |
| Y17 | corretto | Regia §0: i ritratti si mostrano dopo l'incontro |
| Y18 | corretto | Regia §6: righe per la n. 4, i Treant, il corno, Balvar e Hald, il dado dei caduti, lo Scudo |
| Y19 | al DM | Il tono A o B dell'Anello (n. 20) |
| Y20 | corretto | Regia §1: la lavagna del banco non serve stasera, le richieste si chiudono a voce |
| Y21 | corretto | Regia §3: Vatore sulle mura se tornano in volo. DEF-4 Scene 9 e 10 portano la proposta come INFERRED (n. 11) |

## Developer a freddo (`DEVELOPER.md`)

| # | Esito | Come |
|---|---|---|
| O1 | al DM | DEF-4 Scena 9: la ronda arriva in 1d4+2 round, come nel campo. Per la CA di Vatore la proposta INFERRED è la CA 22 di Sal (n. 1, 2) |
| O2 | corretto | DEF-4 Scena 11, «Chi non vola»: i Bracieri non rifiutano, con Castigo del Drago, Salto Fiammeggiante e la Collina. È una proposta INFERRED (n. 5). Nella regia §1 c'è la riga |
| O3 | al DM | *Ghermire*: proposta INFERRED nella Scena 11, stasera non lo usa (n. 6) |
| O4 | corretto | DEF-4 Scena 8, «Come si decide»: una ronda che arriva a vedere lo scontro è un allarme. Per la via silenziosa di Artemis servono anche ronde che non arrivano, o una bolla di *silenzio* |
| O5 | al DM | DEF-4 Scena 7: il criterio e la tattica di Balvar con i PG, come proposta INFERRED (n. 8) |
| O6 | corretto | DEF-4 A.6: la ronda ha i numeri degli orchi SRD di DEF-5 A.1, falchion 2d4+4 anche nella Scena 5, e la complicazione 3 è la ronda. Per il sergente c'è una proposta INFERRED (n. 9) |
| Y1 | corretto | DEF-4 Scena 6: con 3 tacche e il volo subito, Grask è sveglio |
| Y2 | al DM | DEF-4 Scena 6: la bolla di Balvar prende Grask, come proposta INFERRED (n. 13) |
| Y3 | corretto | DEF-4 Scena 10: tolti «colto alla sprovvista» e «l'Occhio lo avverte». Resta l'invisibilità contro Schivare Prodigioso Migliorato |
| Y4 | corretto | DEF-4 Scena 8, Via A: marca `[regola della casa]`, più una riga sulla Volontà Indomita, che non entra perché Intimidire non è un TS |
| Y5 | corretto | DEF-4 A.6: lo squadrone ha Ascoltare e Osservare +2, come nello skill challenge |
| Y6 | corretto in parte | Morso delle wyvern nella sidebar, mark su M7-B, riga nella regia. EL e PX al DM (n. 16) |
| Y7 | corretto | DEF-4 Scene 5 e 11: la runa si attiva al corno dell'alba o dopo |
| Y8 | corretto | DEF-4 Scena 8: «THORIK — la preghiera a Moradin (non è la *Benedizione della Forgia* dei Bracieri di Tordek)» |
| Y9 | al DM | DEF-4 Scena 8: il glifo del telo, come proposta INFERRED (n. 14) |
| Y10 | corretto | DEF-4 Scena 8: un round prima dei rinforzi si vedono torce sul telo e si sente un ordine gridato in orchesco |
| Y11 | al DM | *Fluttuare*: proposta INFERRED nella Scena 11 (n. 6) |
| Y12 | corretto in parte | Scheda di Skullcrusher: `Source` allineata ad A.1, e la nota dice che ERRATA §2.3 è superata. Il campo `CR` resta 12 per il nome del file (vedi sopra). ERRATA §2.3 è fuori dal mio perimetro (n. 27) |
| Y13 | corretto | Scheda di Balvar: Zog'tar è CR 15 |
| Y14 | corretto | DEF-4 Scena 5 e A.6: il Treant con i numeri di DEF-3 A.2 (FOR 29, TS +12/+3/+8, Travolgere, vulnerabile al fuoco) |
| Y15 | corretto | Il nuovo testo della ragione è nella prima sezione, da applicare tu |
| Y16 | corretto | DEF-4 A.6: le schede del Bestiario sono del 1372, e qui valgono quelle SRD |
| Y17 | al DM | L'Osservare di Grask e *comando* «Cadi» vanno verificati sull'SRD (n. 24) |

## Playtester a freddo (`PLAYTESTER.md`)

| # | Esito | Come |
|---|---|---|
| 1 | corretto | DEF-4 Scena 7: c'è il paragrafo «L'invisibilità finisce durante la trattativa» |
| 2 | corretto | DEF-4 Scena 8: Zog'tar ci sta nel buco portatile (0,5 m³ contro 7,5). L'aria è una proposta INFERRED (n. 12) |
| 3 | al DM | Come DEV O1 (n. 1, 2) |
| 4 | corretto | DEF-4 Scena 5, «Chi legge le pergamene», e la regia §1: Usare Oggetti Magici con CD 20 + livello dell'incantatore, come il modulo. La lista del druido è da verificare |
| 5 | corretto | Come DEV Y7 |
| 6 | al DM | La quota fra un turno e l'altro: proposta INFERRED, circa 15 m (n. 6) |
| 7 | corretto | DEF-4 Scena 11: lo Scudo del Custode sulla riga del re. Regia §1 e §4 |
| 8 | corretto | Come DEV O2 |
| 9 | al DM | *Corrompere l'acqua*: proposta INFERRED nella Scena 11 (n. 7) |
| 10 | corretto | Come DEV Y8 |
| 11 | al DM | La regia §1 chiede di deciderlo prima di cominciare (n. 3) |
| 12 | corretto | DEF-4 Scena 10: Vatore dopo il primo box, come proposta INFERRED (n. 11) |
| 13 | al DM | Il Torque (n. 17) |
| 14 | corretto | Come DM Y14 |
| 15 | lasciato | I tempi dell'Atto I riguardano le Scene 1-4, già giocate, e stasera non pesano |
| 16 | al DM | Hald e Balvar (n. 21) |
| 17 | al DM | La mappa del campo (n. 22) |
| 18 | al DM | DEF-4 Scena 5: arma a spargimento con incremento 3 m, come proposta INFERRED (n. 15) |

## Coerenza fra master, schede e mappe (`../COERENZA-PNG-MAPPE.md`)

| # | Esito | Come |
|---|---|---|
| 1 | corretto | M7-C, JSON e `.md`: chi vola sotto il telo resta nella portata dell'ascia. Ricompilata e renderizzata in tutti e due i temi |
| 2 | corretto | M7-C: Grask è sveglio fino alla 4ª tacca e dorme dalla 5ª, e lo stato si fissa all'atterraggio |
| 3 | corretto in parte | Come DEV Y12. Il file non è rinominato |
| 4 | al DM | Come DEV O1 |
| 5 | corretto | M7-B: mark 12 e 13 per le wyvern (W2, X2), «entrano dal round 2». Il morso è nella sidebar. Le due copie di M7-B, nell'Atlante e in DEF-4 Appendice D, sono identiche. Il blocco SRD della wyvern è quello verificato nel giro del 2026-10-18 |
| 6 | corretto | Atlante, sotto M7-B: le gru non sono alla pari. Da B10 il gancio arriva sull'impronta, da W10 solo se il drago picchia verso il muro est |
| 7 | corretto | DEF-4 §0-bis e Scena 8, regia §3: Tempra CD 15 sopra i 50 danni, house rule. La cattura del Q29 vale per chi cade a 0 |
| 8 | corretto | Atlante: M7-B ha GS 14 nel titolo e nel testo |
| 9 | corretto | Atlante: M7-A dice GS 15, più 4 guardie hobgoblin (Guerriero 8) |
| 10 | corretto | Atlante: «se la Scena 10 chiude con 0-1 successi». Il mark 4 non l'ho spostato: sulla griglia il re è il 🔵 di L16. Ho corretto invece la prosa («dietro, riga 17» → «L16, alle spalle della prima fila») |
| 11 | corretto | DEF-4 Scena 10: la riga 0 dice «e Re Thorek a 8 pf, come con 1» |
| 12 | corretto | M7-B: mark 11 per Durik a U16. Nell'Atlante, i Treant richiamati entrano da L-M18 |
| 13 | corretto | Atlante, sotto M7-B: al round 1 prima scende entro 30 m dai PG, poi soffia. Nessun numero nuovo di quota |
| 14 | corretto | M7-C: due guardie restano al seggio e due vanno su chi lancia. I rinforzi aspettano fuori finché Zog'tar è in piedi |
| 15 | corretto | Come DEV Y14 |
| 16 | corretto | DEF-4, schede d'entrata della tenda: Zog'tar ha l'armatura di mithral annerita, di fattura nanica, e le guardie battono il piatto dello spadone |
| 17 | corretto | Scheda di Balvar: CR 15, e in Tattiche il *Morale* sotto i 30 pf (D52, D71) |
| 18 | corretto | Scheda di Re Thorek I: 182 anni |
| 19 | corretto | Scheda di Durin: «Scena 10» |
| 20 | corretto | Scheda di Skullcrusher: tolto «cadde sotto Aegis Fang impugnata da Thorgrim». La frase nuova la sceglie il DM (n. 25) |
| 21 | corretto in parte | Scheda di Sal: c'è la frase del master. «Cosa vuole» ed «Esiti possibili» sono ancora `[DA SCRIVERE]`, perché riempirli vorrebbe dire inventare |
| 22 | corretto | Scheda di Thorgrim: Motivation, «Aspetto e voce» e «Cosa vuole» presi dalla scheda d'entrata della Scena 4. Per sé, la scheda dice ancora che manca. DEF-4 §6 dice: «gli antenati, chiamati da Thorgrim che dà l'ordine» |
| 23 | corretto | Scheda del Ghostlord: «un incappucciato che si presentò come chierico di Shar: era Vatore» (Q4-bis). La riga Status è lasciata: non è nei rilievi di stasera |
| 24 | corretto | Regia §3 e §4: due note d'improvvisazione per gli scontri senza griglia. Le griglie vere sono un lotto di mapmaking |
| 25 | lasciato | Nessuna correzione per stasera, come dice il rilievo. DEF-4 A.6 avverte che le schede del Bestiario sono del 1372 |

## Il cancello

Ho girato
`python3 plans/esperimenti/giro4-arc07-2026-10-19/cancello.py "<file>" "<file>"`
dalla radice del repo su ogni file toccato.

**Esiti.**

- Nessun box è peggiorato, impoverito o tolto, e nessuno supera le 12 righe.
- Nessun box votato dal DM è cambiato.
- Le segnalazioni sono uguali alla base 8a6b1e1 in ogni file.
- Gli echi passano tutti e quattro (`✓ passa`). L'eco di Tordek ha 1 box
  cambiato, per Y7.

**Le righe ✗ «fatto cambiato».** Sono le sole che restano, e tutte vengono da
una correzione. Il controllo conta nomi, numeri e CD sull'intero file, quindi
ogni fatto aggiunto da un rilievo lo fa scattare:

| File | Cosa cambia, e per quale rilievo |
|---|---|
| DEF-4 | Tolti «Cuore» ×2 (il Rubino), 28 ×2 (la FOR del Treant), 21.800, 19.600 e 56 (G2-56), «Occhio» (Y3). Aggiunti i numeri e le CD delle correzioni: danno massiccio CD 15, ronde, Treant, sergente, pergamene CD 23/25/27, *corrompere* CD 25, 19.603 |
| regia | Le tabelle delle risorse e delle tacche (O6, R1, PT #4) |
| intro | Le tre pozioni e la Collana (O3, Y2) |
| Seme | La nota sulle tacche e i 125 mo di *identificare* (R1, O2) |
| Cassetta | I sei PNG nuovi e i rimandi alle Scene 10 e 11 (Y10) |
| Forgia Ricorda | La Scena 11 e la nota su N (Y11) |
| Atlante | Il GS, le gru e il soffio (COERENZA 6, 8-10, 12, 13) |
| M7-C | Le tacche di Grask (COERENZA 2) |
| schede del Bestiario | CR 15, 182, Scena 10, GS 14 e i numeri di A.1 (COERENZA 3, 17-23) |

**Gli altri gate**, sullo stato finale:

```
✓ validate_modules: 5 master conformi alla checklist module-standard — 0 errori
✓ copertura_scene: 15 rilievi, tutti dichiarati con la ragione
✓ domande_developer: 18 rilievi, tutti dichiarati con la ragione
✓ componenti: apparato e copie allineati
✓ validate_maps: 53 SVG in 8 dir rendered/, 31 master — tutti ben formati, tracciabili e allineati. Tema texture: 53 SVG.
✓ validate_bestiario: struttura ok, 187 statblock validi, catalogo in sync.
✓ validate_norme_editoriali: 105 norme registrate
ciclo_prosa segnala: 0 segnalazioni su DEF-4, regia, intro, Seme, echi, cassetta,
Forgia Ricorda, Atlante e M7-C; nelle schede di Thorgrim, Ghostlord e Sal 1 → 1,
la stessa della base
```

### L'uscita del cancello, file per file

```
== 07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md
box cambiati: 0
misura       box 37→37  parole 2284→2284  sens 126→126  -mente 1→1  30-70 43→43
segnalazioni 0→0 · MQM [99.98, 99.98] · Gulpease [66.9, 66.9] · ritmo [0.64, 0.64]
✗ fatto cambiato: nomi propri: tolti {'Cuore': 2, 'Treant': 1, 'Occhio': 1}, aggiunti {'Skullcrusher': 1, 'Salvatore': 2, 'Hella': 2, 'Thorek': 1, 'Senza': 1, 'Mano': 1, 'Cintura': 1, 'Tordek': 4, 'Aegis': 1, 'Fang': 1, 'Thorik': 1, 'Collana': 1, 'Bracieri': 4, 'Artemis': 4, 'Moradin': 1, 'Rossa': 1, 'Drago': 1}
✗ fatto cambiato: numeri: tolti {'11': 1, '28': 2, '19.600': 1, '21.800': 1, '56': 1}, aggiunti {'07': 1, '4': 6, '2': 12, '7': 1, '5': 6, '3': 10, '13': 3, '1372': 1, '27': 2, '6': 4, '1': 6, '25': 2, '9': 1, '0': 2, '8': 7, '10': 3, '12': 3, '15': 3, '30': 1, '18': 1, '20': 2, '16': 1, '22': 1, '24': 1, '50': 2, '23': 1, '29': 2, '70': 2, '19.603': 1, '0,5': 1, '7,5': 1}
✗ fatto cambiato: CD: tolti -, aggiunti {'CD25': 2, 'CD15': 2, 'CD23': 1, 'CD27': 2, 'CD24': 1}
✗ 3 non passano

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/00-INTRO-DOVE-SIAMO.md
box cambiati: 0
misura       box 1→1  parole 49→49  sens 3→3  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [70.0, 70.0] · ritmo [0.2, 0.2]
✗ fatto cambiato: nomi propri: tolti -, aggiunti {'Collana': 1}
✗ fatto cambiato: numeri: tolti -, aggiunti {'1': 1, '4': 1, '6': 1, '10': 1}
✗ 2 non passano

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/01-REGIA-SERATA.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [66.9, 65.7] · ritmo [0.78, 0.75]
✗ fatto cambiato: nomi propri: tolti {'Senza': 1}, aggiunti {'Skullcrusher': 3, 'Artemis': 5, 'Forgia': 2, 'Hella': 7, 'Thorik': 3, 'Tordek': 2, 'Zeth': 2, 'Cuore': 1, 'Cintura': 1, 'Bracieri': 3, 'Drago': 1, 'Aegis': 1, 'Fang': 1, 'Fauci': 2, 'Treant': 1}
✗ fatto cambiato: numeri: tolti -, aggiunti {'0': 10, '4': 24, '10': 9, '2': 12, '5': 14, '15': 1, '20': 3, '6': 8, '9': 4, '11': 3, '3': 17, '25': 3, '1372': 3, '7': 3, '8': 1, '1': 13, '50': 1, '12': 1, '22': 2, '70': 3, '17': 1, '27': 2, '23': 1, '24': 1, '18': 2, '2026': 1, '07': 1, '372': 2, '150': 2, '160': 1, '125': 1, '375': 1, '4,5': 1}
✗ fatto cambiato: CD: tolti -, aggiunti {'CD22': 2, 'CD17': 1, 'CD27': 1, 'CD23': 1, 'CD25': 1, 'CD15': 1}
✗ 3 non passano

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/02-IL-SEME.md
box cambiati: 0
misura       box 1→1  parole 59→59  sens 6→6  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [64.3, 64.3] · ritmo [0.39, 0.39]
✗ fatto cambiato: numeri: tolti -, aggiunti {'6': 1, '125': 1, '0': 1, '3': 1, '7': 1, '2': 1, '5': 2, '4': 1}
✗ 1 non passano

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/03-ECHI-THORIK.md
box cambiati: 0
misura       box 2→2  parole 92→92  sens 3→3  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [64.4, 64.4] · ritmo [0.58, 0.58]
✓ passa

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/04-ECHI-TORDEK.md
box cambiati: 1
misura       box 2→2  parole 83→85  sens 6→6  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [68.8, 68.1] · ritmo [0.45, 0.47]
✓ passa

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/05-ECHI-ARTEMIS.md
box cambiati: 0
misura       box 2→2  parole 78→78  sens 5→5  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [72.6, 72.6] · ritmo [0.6, 0.6]
✓ passa

== 07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/06-ECHI-HELLA.md
box cambiati: 0
misura       box 2→2  parole 80→80  sens 2→2  -mente 0→0  30-70 100→100
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [76.1, 76.1] · ritmo [0.38, 0.38]
✓ passa

== 07_il Portale Della Forgia Eterna/ARC07-CASSETTA-DEL-DM.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [74.0, 74.0] · ritmo [0.77, 0.77]
✗ fatto cambiato: nomi propri: tolti -, aggiunti {'Skullcrusher': 1, 'Hella': 1, 'Sorella': 1, 'Thorik': 1}
✗ fatto cambiato: numeri: tolti {'2': 1}, aggiunti {'4': 5, '5': 3, '6': 1, '8': 1, '11': 2, '10': 3}
✗ 2 non passano

== 07_il Portale Della Forgia Eterna/PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [67.9, 66.4] · ritmo [0.94, 0.93]
✗ fatto cambiato: numeri: tolti -, aggiunti {'4': 3, '11': 3, '3': 1, '13': 1}
✗ 1 non passano

== 07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-DEFINITIVO.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [60.9, 60.7] · ritmo [0.86, 0.85]
✗ fatto cambiato: nomi propri: tolti -, aggiunti {'Hella': 1, 'Treant': 1}
✗ fatto cambiato: numeri: tolti {'12': 1, '17': 1}, aggiunti {'1': 3, '2': 5, '8': 1, '0': 1, '30': 2, '15': 3, '10': 1, '11': 2, '13,5': 1, '14': 1}
✗ 2 non passano

== 07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [60.4, 60.1] · ritmo [0.66, 0.64]
✗ fatto cambiato: numeri: tolti -, aggiunti {'6': 1, '3': 2, '4': 3, '5': 3}
✗ 1 non passano

== Bestiario/png/durin-rocciadura-cr6.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [91.23, 91.23] · Gulpease [59.8, 59.8] · ritmo [0.59, 0.59]
✗ fatto cambiato: numeri: tolti {'4': 1}, aggiunti {'10': 1}
✗ 1 non passano

== Bestiario/png/re-thorek-i-cr16.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [64.2, 64.2] · ritmo [0.63, 0.63]
✗ fatto cambiato: numeri: tolti {'180': 1}, aggiunti {'182': 1}
✗ 1 non passano

== Bestiario/png/thorgrim-barbadiferro.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 1→1 · MQM [100.0, 100.0] · Gulpease [61.3, 63.0] · ritmo [0.52, 0.61]
✗ fatto cambiato: nomi propri: tolti -, aggiunti {'Thorik': 2}
✗ fatto cambiato: numeri: tolti {'07': 1}, aggiunti {'4': 4}
✗ 2 non passano

== Bestiario/villain/Ghostlord/Ghostlord.md
box cambiati: 0
misura       box 2→2  parole 67→67  sens 0→0  -mente 0→0  30-70 50→50
segnalazioni 1→1 · MQM [99.43, 99.43] · Gulpease [70.7, 70.7] · ritmo [0.69, 0.69]
✗ fatto cambiato: numeri: tolti -, aggiunti {'5': 1, '4': 1}
✗ 1 non passano

== Bestiario/villain/Salvatore/Salvatore.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 1→1 · MQM [100.0, 100.0] · Gulpease [57.8, 57.8] · ritmo [0.87, 0.87]
✗ fatto cambiato: numeri: tolti -, aggiunti {'9': 1, '4': 1}
✗ 1 non passano

== Bestiario/villain/balvar-fuocospento-cr13.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [56.7, 56.6] · ritmo [0.91, 0.89]
✗ fatto cambiato: numeri: tolti {'14': 1}, aggiunti {'15': 1, '30': 1}
✗ 1 non passano

== Bestiario/villain/skullcrusher-il-nero-cr12.md
box cambiati: 0
misura       box 0→0  parole 0→0  sens 0→0  -mente 0→0  30-70 0→0
segnalazioni 0→0 · MQM [100.0, 100.0] · Gulpease [64.4, 67.2] · ritmo [0.82, 0.82]
✗ fatto cambiato: numeri: tolti {'27': 1, '240': 1, '24': 1}, aggiunti {'07': 1, '4': 3, '2.3': 2, '12': 2, '14': 7, '15': 1, '33': 2, '37': 2, '297': 2, '28': 2, '11': 1, '2026': 4, '10': 3, '09': 1, '17': 1, '19': 2}
✗ fatto cambiato: CD: tolti {'CD24': 1}, aggiunti {'CD28': 2}
✗ 2 non passano

```
