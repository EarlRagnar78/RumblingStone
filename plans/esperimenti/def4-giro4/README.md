# Giro 4 su `ARC07-DEF-4`: la conferma dopo le decisioni del 12 ottobre

Il master letto è quello con D49-D63 applicate (commit `18268dc` del ramo
`claude/project-thread-e860p0`). Le letture sono **un subagente alla volta**:
prima il lettore, poi il playtester, poi il DM a freddo rifatto. Si corregge
fra una lettura e l'altra.

| Lettura | 🔴 | 🟠 | 🟡 | Rapporto |
|---|---:|---:|---:|---|
| lettore (intero, a blocchi, con diario) | 0 | 5 | 16 | `def4-giro4-LETTORE.md`, `def4-giro4-LETTORE-diario.md` |
| playtester (due percorsi, i Treant in tutte e quattro le destinazioni) | 0 | 6 | 17 | `def4-giro4-PLAYTESTER.md` |
| DM a freddo (`lettura_a_scene.py`) | | | | da fare |

Il lettore non è passato da `lettura_a_scene.py` (il percorso del file gliel'ha
dato chi orchestra) e non entra in `letture-a-freddo.json`.

## Il triage del lettore

| # | Rilievo | Esito |
|---|---|---|
| 1 🟠 | la pozione d'invisibilità comprata copre «il primo blocco» o «mezzo blocco» | corretto: mezzo blocco, e quel blocco si tira a Nascondersi |
| 2 🟠 | «ucciso e basta» contro le guardie che scappano gridando | corretto: due domande in ordine, allarme e poi spettacolo; un allarme senza spettacolo costa il successo e basta |
| 3 🟠 | l'indizio del capitano sta nella Scena 5 | spostato in Scena 4, «Il fianco est»; la Scena 5 rimanda |
| 4 🟠 | il §0 della serata non dice che i Treant e il dado dei caduti sono in Scena 5 | aggiunte due righe al §0 |
| 5 🟠 | Zog'tar catturato: il dopo | scritto `[INFERRED]` (la cella, la giustizia del re) e una riga in §7; **D69** al DM |
| 6 | metà di 5 *volare* | 2, per difetto, `[INFERRED]` → D71 |
| 7 | la variante dice *volare* comprato | corretto: la dotazione del re o il volo proprio |
| 8 | le pozioni del re e i 10.000 mo del forziere | un dono a parte, `[INFERRED]` → D71 |
| 9 | «(Scena 5)» per Balvar non sorvegliato | corretto in Scena 6 |
| 10 | Balvar entra nella fortezza in tre modi | allineati: postierla con garanzia e catene anche a piedi; da solo all'alba entra dalla postierla aperta, `[INFERRED]` → D71 |
| 11 | Balvar senza Nascondersi e Muoversi Silenziosamente | −1, dalla CA (armatura completa di mithral), `[INFERRED]` → D71 |
| 12 | quando si sveglia Zog'tar | regola SRD scritta; −8 se imbavagliato, `[INFERRED]` → D69 |
| 13 | il drago senza ordine fra i bersagli | ordine scritto, `[INFERRED]` → D71 |
| 14 | TS di A.1-bis | rifatti: Rifl +18, Vol +20; nono talento e soglia di fuga (~112 pf) scritti → D71 |
| 15 | le wyvern senza numeri | riga SRD nella tabella |
| 16 | il dado dei caduti con due regole | una regola sola: un tiro per tipo di cura, le bacchette un tiro; all'alba se la Scena 10 salta |
| 17 | PX di Zog'tar umiliato o catturato | sconfitto vale come ucciso (DMG); il rimando della Scena 10 riscritto |
| 18 | dodici ore o otto | le prime quattro fra arrivo, porta e consiglio, `[INFERRED]` → D71 |
| 19 | cinque pozioni di *neutralizza veleno* (4°) | **D70** al DM: è nel conto del tavolo del 25 settembre |
| 20 | «sosta» ambiguo | riscritto: un minuto al buio |
| 21 | quanto costa a Balvar finire la lastra | un'azione di round pieno, l'ultima, `[INFERRED]` → D71 |

Tolte anche le sigle di decisione rimaste nel testo stampato (`(D18`, `(D40,
D58)`, `(Scena 5, D62)`), che la CI non boccia ma ADR-0070 non vuole.

## Il triage del playtester

Il playtester ha letto `cbc083c`; D64-D68 (`4981480`) sono arrivate mentre
leggeva, e ne chiudono in parte due rilievi.

| # | Rilievo | Esito |
|---|---|---|
| 1 🟠 | le cariche della Collana | chiuso da D65 (le tre cariche sono una riserva sola, l'eccezione dell'alba è nella scheda) |
| 2 🟠 | *trasporto vegetale* salta la Scena 6 | niente alberi vivi entro 500 m dalla tenda → D74 c |
| 3 🟠 | *silenzio* su Grask e la bolla alla tenda | allarme senza corno → D74 d |
| 4 🟠 | la ronda dopo la pattuglia senza tattica | grida, campo pre-allertato → D74 e |
| 5 🟠 | il Treant senza TS e FOR | FOR 28 e TS dai numeri dei suoi schianti → D74 a |
| 6 🟠 | il bottino della tenda non lo compra nessuno | si vende nel 1372; l'armatura di Zog'tar al re → D74 o |
| 7 | «Due tengono la tenda» senza il costo del mese | scritto nella colonna del costo |
| 8 | la tacca di un Treant alla tenda | 0 → D74 b |
| 9 | un Treant nella tenda è spettacolare? | sì → D74 b |
| 10 | Durik dopo l'ora | resta con Hella → D74 g |
| 11 | il fiuto dei lupi in tacche | una tacca → D74 f |
| 12 | un blocco fallito consuma l'invisibilità | non corretto: le tacche non sono minuti (#23) |
| 13 | l'atterraggio senza prova | prova solo con Grask sveglio → D74 h |
| 14 | chi torna in volo al corno | dentro prima del drago → D74 i |
| 15 | Balvar conta per la metà? | sì → D74 k |
| 16 | il peso di Zog'tar e la forma selvatica | 300 kg, una bestia Grande lo porta → D74 j |
| 17 | gli slot di Hella all'alba | restano spesi, come l'SRD |
| 18 | la breccia con l'attacco a CD 18 | attacco contro CA 28 → D74 l |
| 19 | le wyvern senza tattica | scritta → D74 m |
| 20 | gli aiutanti alla corda | al massimo tre → D74 n |
| 21 | il rimando dell'orologio alla Scena 8 | riga in Scena 8 verso §8 B |
| 22 | la penalità al ritorno | chiusa da D64 e D72 |
| 23 | le tacche e le ore | detto che una tacca non è un'ora → D74 p |

## Il DM a freddo · 🔴 0 · 🟠 8 · 🟡 11

Rapporto: [`def4-giro4-DM.md`](def4-giro4-DM.md); la corsa in `corsa-dm/dm/`.
Letto sul testo di `3909e7e`. Le correzioni sono nel commit che porta questo
triage.

| # | Rilievo | Esito |
|---|---|---|
| 1 🟠 | «La vostra serata» non entra in un'ora | tempi per ogni scena fino alla 11, e cosa si legge *solo* di ognuna: 60 minuti |
| 2 🟠 | da dove si riparte stasera | la premessa dice le scelte rimaste della Scena 5; in §0 la prima battuta (Durin nel cortile) e le tre scelte |
| 3 🟠 | Grask per chi torna in volo | in §0: la tacca del volo si segna alla partenza, con 3 tacche Grask è sveglio; con la veglia dei semi dorme. L'`[INFERRED]` dell'atterraggio era già chiuso da D74 h |
| 4 🟠 | la veglia dei semi per questo gruppo | **D75** (A): la veglia costa la tacca anche a questo gruppo |
| 5 🟠 | il dado dei caduti alla Scena 10 | la regola copiata nella riga «Dalla notte»: 1d4 per tipo di cura, il numero è quanti difensori con un nome muoiono, non tocca ARC-08. Il log del gruppo → **D76 d** |
| 6 🟠 | Vatore con chi torna in volo | riga «Se tornano in volo» nella Scena 9 `[INFERRED]`: lo vedono dall'alto, scendono o lo ritrovano sulle mura |
| 7 | il segno della pozione n. 4 e Vatore | riga «Se uno di loro porta il segno» nella Scena 9 `[INFERRED]`: CD 14 per parlargli, Sal in ARC-09 lo cerca |
| 8 🟠 | i quindici `[INFERRED]` | chiusi da D74 sul testo che il DM non aveva ancora |
| 9 🟠 | tre fatti del gruppo mancanti | **D76**: non ancora giocati; §0 dice di chiederlo al tavolo prima della Scena 6, e che la n. 4 nessuno l'ha bevuta |
| 10 | il percorso del booklet della regia | **residuo**: un percorso di file è apparato, e il master si stampa (ADR-0070) |
| 11 | le Benedizioni di Moradin alla Scena 4 | la parentesi (morale, al colpire e ai danni, 12 ore) anche lì |
| 12 | quanto vale una tacca in ore | «circa un'ora a tacca, tranne la sosta e il sonno» |
| 13 | la runa di Zeth al duello | round 1: chi ce l'ha la attiva adesso, azione standard |
| 14 | chi sceglie il drago e la riga «ignora Hella» | la riga di scalatura dice che va scelta, e che senza vale «Chi sceglie» |
| 15 | i ritratti che mancano per stasera | **residuo**: immagini, lavoro di `art-direction` fuori da questo piano |
| 16 | Balvar in volo, il rimando | «(se tornano in volo: Scena 8, …)» nella riga della Scena 7 |
| 17 | Treant e wyvern fuori da A.6 | due righe in A.6 |
| 18 | la vista si ferma sull'apparato | **residuo**: le etichette in grassetto sono la testata standard dei master (`module-standard`); cambiarle è un lavoro di tutti i DEF |
| 19 | la nota sul repo in §0-ter | dentro `<!-- apparato -->` |

La correzione del 6 ha chiuso anche il residuo D2 della Scena 7 in
`domande-developer.json` («e se volano?»), tolto dal registro.
