# Giro 4 · ARC-07 — coerenza fra master, schede e mappe

Lettura a freddo del 2026-10-19, per la serata che parte dalla Scena 5 di
`ARC07-DEF-4` e arriva all'esito del duello, con `ARC07-DEF-5` subito dopo.
Nessun file del repo è stato modificato oltre a questo.

**Cosa è stato letto.** `ARC07-DEF-4` (Scene 6-11, Appendici A e D),
`ARC07-DEF-5` (Scene 2-3, Appendici A e B), le schede di `Bestiario/`
(villain: Skullcrusher, Zog'tar, Balvar, Salvatore, Ghostlord; png: Durin,
Re Thorek I, Thorgrim, Re Thorek Hammerfist, Dana; mostri: Treant, worg,
hobgoblin sergente), la scheda di Durik (`homebrew/sessione-resurrezione-mille-anni/08-SCHEDA-DURIK.md`),
l'Atlante `Mappe/ARC07-MAPPE-DEFINITIVO.md` (M7-A, M7-B, CM-1), la mappa
`Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md` col suo JSON, lo stato del gruppo
(`stato-del-gruppo/sessione-4.md`) e la patch del 2026-10-18.

**Misure.** `python3 scripts/validate_maps.py`: 53 SVG, 31 master, tutti
allineati (exit 0). Le griglie M7-A e M7-B dell'Appendice D di DEF-4 sono
identiche a quelle dell'Atlante (diff vuoto). Il booklet
`ARC07-NOTTE-E-ALBA-BOOKLET.hb.md` è rigenerato dopo l'ultima modifica del
master e porta gli stessi numeri (controllo a campione su otto stringhe).
`python3 scripts/validate_bestiario.py --forma`: 37 statblocchi su 37, 24
dossier su 24, 16 schede brevi su 16 nella forma di ADR-0091.

**Fonte delle regole.** Il mirror `skills/dnd-35-srd/references/` è sottile:
contiene il danno massiccio, il prono, l'occultamento e la tabella dei draghi,
non i blocchi delle wyvern né i livelli degli incantesimi. Dove il mirror non
basta, il controllo è «da verificare» e non c'è un rilievo.

---

## 1. Quello che torna

Lo dico prima, perché è la maggior parte del lavoro e il DM può fidarsene.

| PNG / creatura | Master | Scheda | Esito |
|---|---|---|---|
| Balvar | DEF-4 A.4 | `villain/balvar-fuocospento-cr13.md` | il blocco è un `include` della scheda: CA 24/14/22, 101 pf, TS, martello +11/+6, Percepire Intenzioni +13 identici. CD 20 di *slay living*, 21 di *blade barrier*, 20 di *comando superiore* (5° livello, come dice la scheda) coincidono nella Scena 7, nella Scena 8 e in M7-C |
| Zog'tar | DEF-4 A.2 | `villain/zog-tar-deatheye-cr15.md` (POINTER) | GS 15, CA 26 mithral, 283/328 pf, RD 3/—, Presenza CD 21: la riga Source della scheda e i quattro Boost log coincidono col master. Ho rifatto i conti di ascia (+29, 3d6+20), giavellotti (+19, 1d8+13), Lotta (+29/+32), CA e TS: tornano |
| Skullcrusher | DEF-4 A.1 | `villain/skullcrusher-il-nero-cr12.md` (POINTER) | il blocco del master è coerente con l'adulto maturo dell'SRD più il template Avanzato (297 pf, CA 33/37, soffio 14d4 CD 28, Presenza CD 25 su 63 m, RI 21). La scheda **non** coincide: vedi 🟠 3 |
| Durin | DEF-4 A.3 | `png/durin-rocciadura-cr6.md` | Guerriero 6, 52 pf, CA 22: coincidono, e i conti tornano |
| Re Thorek I | DEF-4 A.5, Scena 11 | `png/re-thorek-i-cr16.md` | nessuno statblocco, soglia a colpi: coincidono |
| Hobgoblin sergente | DEF-5 A.2 | `mostri/hobgoblin-sergente-cr5.md` | 37 pf, CA 21/19, +9 e +6, TS e talenti identici |
| Dana, Re Thorek (1372) | DEF-5 A.5, A.6 | dossier + `ARC08-01-GUIDA-DM.md` | CA 29 e 142 pf; CA 30 e 196 pf. Coincidono; la CA da esausto (27/10/27) è giusta |
| Durik | DEF-4 Scena 11, DEF-5 A.4 | scheda di Durik | 102 pf, CA 21, morso +15, vulnerabilità all'acido +50%: coincidono |
| M7-C | Scene 7-8, Appendice D | `ARC07-MAPPE-M7C-*.md` e `.json` | soglia M4-N4, palo M9, bracieri O6 e J11, seggio M12-N13, guardie K12/L10/O10/P11, Balvar P13, telo est S5-S13, telo del glifo L14-N14, Grask N15, sacerdote W11: tutto coincide. Il fondo buio P12-R13 è davvero fuori dai raggi dei bracieri (≥ 9 m da tutti e due). Il cono di 18 m del Fuori-Posto da P13 arriva a N2, dove la mappa mette i PG (16,5 m) |
| CM-1 | DEF-5 Scena 2 | Atlante | altare P-Q 13-14, re a P14, le dieci statue alle coordinate dichiarate, piattaforme B-C13 e d-e13, porta P-Q01: verificato cella per cella |

---

## 2. Rilievi

### 🟠 1 · M7-C dice il contrario del master su chi vola sotto il telo

- **Scena**: 8, la tenda. Il gruppo di stasera ha le cinque pozioni di *volare*
  del re (`sessione-4.md`), quindi il caso è probabile.
- **Prova**: M7-C, Tattiche: *«Chi vola sotto il telo (6 m al palo, 3 m ai lati;
  Scena 8): resta fuori dalla portata dell'ascia»* (anche nel JSON, riga 491).
  DEF-4 Scena 8: *«Sotto il telo chi vola **non** esce dalla portata dell'ascia:
  Zog'tar è alto 3 m e arriva a 3 m oltre, cioè fino al colmo.»*
- Il booklet della serata porta il testo giusto; sbaglia solo la mappa, che il
  DM apre per le tattiche.
- **Correzione**: nel JSON di M7-C, «resta fuori dalla portata» → «resta **nella**
  portata dell'ascia fino al colmo; ne esce solo chi sta fuori dal telo», poi
  `compile_map_json.py`.

### 🟠 2 · M7-C mette Grask addormentato, e stasera è probabilmente sveglio

- **Scena**: 6-7, l'atterraggio alla tenda.
- **Prova**: M7-C, mark 8 e Disposizione iniziale: *«Grask, l'araldo: dorme
  seduto fuori»*. DEF-4 Scena 6: *«sveglio finché l'ultima tacca segnata è la
  4ª, addormentato da quando si segna la 5ª»*, e lo stato si fissa
  all'atterraggio (G2-29). Il gruppo ha **3 tacche** (`sessione-4.md`); il volo
  ne costa 1. Se nella Scena 5 non ne spendono altre, arrivano a 4 e Grask è
  sveglio: chi atterra tira Nascondersi o Muoversi Silenziosamente contro di lui.
- **Correzione**: mark 8 e Disposizione iniziale → «Grask seduto fuori: sveglio
  fino alla 4ª tacca, addormentato dalla 5ª (lo stato si fissa all'atterraggio)».

### 🟠 3 · La scheda di Skullcrusher dà ancora i numeri del GS 12

- **Scena**: 11. Il DM che apre il Bestiario trova un altro drago.
- **Prova**: `villain/skullcrusher-il-nero-cr12.md`, riga 4: *«**CR**: 12»*;
  riga Source: *«GS 12: CA 27, PF 240, soffio acido 12d4 CD 24»*. Il master A.1
  dice GS 14 (vale 15), CA 37 con *armatura magica*, 297 pf, 14d4 CD 28. Il
  Boost log della stessa scheda dice già «CR 14 → 14». La seconda fonte che la
  scheda dichiara, `ERRATA-ARC07-35-Verification.md` §2.3, dice anch'essa
  *«GS 12 … PF 240 … CD 24»*. Il nome del file è ancora `-cr12`.
- **Correzione**: CR 14 e i numeri di A.1 nella riga Source; in ERRATA §2.3 una
  riga «superato dal canone DM 2026-09-27 e Q37: vale DEF-4 A.1»; il file si
  rinomina in `-cr14` come vuole ADR-0091 §4-bis.4 (i rimandi vanno seguiti).

### 🟠 4 · Vatore: la CA e i round della ronda mancano

- **Scena**: 9.
- **Prova**: DEF-4 Scena 9: *«La CA contro cui si tira quel colpo, e in quanti
  round arriva la ronda `[INFERRED — needs DM confirmation]`»*. Il primo colpo a
  segno decide quattro righe della tabella (e la sincronizzazione su Sal), ma non
  c'è il numero contro cui tirare. La scheda di Sal dà la CA del 1372, non quella
  di Vatore.
- **Correzione**: il DM fissa due numeri prima della serata (CA di Vatore,
  round della ronda) e li scrive accanto alla marca; fino ad allora non li
  invento.

### 🟠 5 · Le wyvern stasera ci sono, e M7-B non sa dove

- **Scena**: 11.
- **Prova**: Sidebar di scala: *«Un gruppo di 13° con la fiducia piena del
  consiglio, tutti gli artefatti e il banco della fucina speso conta come
  straripante: le wyvern ci sono» `[G2-15]`*. Il gruppo ha la fiducia piena e ha
  speso 47.967 mo al banco (`sessione-4.md`). M7-B non ha un punto d'ingresso,
  una quota né un mark per le due wyvern; nel Bestiario non c'è una scheda
  wyvern. I numeri ci sono solo in DEF-4 A.6 e nella sidebar (la sidebar non
  riporta il morso).
- **Correzione**: due mark su M7-B (per esempio in quota dietro V1, «entrano dal
  round 2») e il morso nella sidebar come in A.6. Il blocco SRD della wyvern va
  confrontato sul sito: nel mirror del repo non c'è, quindi da verificare.

### 🟠 6 · Il gancio delle gru non arriva sull'impronta del drago

- **Scena**: 11, «Chi non vola».
- **Prova**: il master: il gancio arriva *«a cinque incrementi, 15 m … dalle gru
  in B10 e W10 il gancio prende il drago quando picchia entro 15 m da una delle
  due, contando anche la quota»*. Su M7-B l'impronta ⚔ è a K-M 09-11: da W10 il
  quadretto più vicino (M10) è a 10 quadretti, cioè 15 m **in piano**; con
  qualunque quota il drago è fuori portata. Da B10 il bordo K è a 13,5 m, e ci
  si arriva solo se il drago è a 3 m o meno. L'Atlante scrive *«ciascuna gru a
  ~13 m»*, e il DM al tavolo pensa che basti.
- **Correzione**: o spostare l'impronta (o una seconda impronta) entro 9
  quadretti da ciascuna gru, o scrivere nell'Atlante «da W10 il gancio non
  arriva all'impronta: serve che il drago picchi verso il muro».

### 🟠 7 · Il danno massiccio è attivo, e il master non lo nomina

- **Scene**: 8 e 10 (Zog'tar), 11 (il drago).
- **Prova**: `campaign/lore/house-rules.md` r.47: *«Massive Damage Rule: ACTIVE.
  50+ HP damage in one hit → Fort DC 15 or die»*; il mirror SRD lo conferma
  (`combat.md` r.206). Zog'tar con Colpo Possente −5/+10 fa in media 40,5, con
  −10/+20 in media 50,5, e l'ascia è ×3: un critico supera i 50 quasi sempre. Il
  master scrive *«Separa il gruppo e lascia vivo il bersaglio»* e *«Zog'tar non
  uccide i PG che cadono: li vuole vivi»* (Q29), senza dire se la cattura
  sospende il TS sul danno massiccio.
- **Correzione**: una riga nel giro di Zog'tar: «sopra i 50 danni il bersaglio
  tira Tempra CD 15 (house rule); la cattura del Q29 vale per chi cade a 0, non
  per chi fallisce questo TS», oppure l'esenzione, se è quella che il DM vuole.

### 🟡 8 · L'Atlante chiama M7-B «GS 12»

- **Scena**: 11. **Prova**: `ARC07-MAPPE-DEFINITIVO.md`, titolo di M7-B:
  *«tattica BOSS · GS 12»* e *«Skullcrusher il Nero, GS 12»*. Il master: GS 14.
- **Correzione**: GS 14 (vale 15) nelle due righe.

### 🟡 9 · L'Atlante dà a Zog'tar il GS 14 e quattro sergenti

- **Scene**: 6-8. **Prova**: M7-A nell'Atlante: *«Tenda del Comando (Zog'tar
  Deatheye, GS 14, + 4 sergenti hobgoblin)»*. Il master: GS 15 e quattro guardie
  Guerriero 8; i sergenti (Guerriero 5) sono quelli di DEF-5.
- **Correzione**: «GS 15, + 4 guardie hobgoblin (Guerriero 8)».

### 🟡 10 · Dove sta il re nel cortile

- **Scena**: 11. **Prova**: M7-B, mark 4: *«L16 ; Re Thorek I»*, sulla riga dei
  PG. L'Atlante, poche righe sotto: *«Re Thorek I dietro (riga 17)»*; il master:
  *«sta nel cortile alle spalle dei PG»*. L'Atlante scrive anche *«se Sc.4
  fallita, è a 8 pf»*, mentre gli 8 pf vengono dalla Scena 10.
- **Correzione**: mark 4 a L17; «se la Scena 10 chiude con 1 successo».

### 🟡 11 · Con zero successi alle mura, quanti pf ha il re?

- **Scena**: 10 → 11. **Prova**: la riga «1» della tabella delle mura dà *«Re
  Thorek a 8 pf»*; la riga «0» (la breccia cede) non dice niente del re, e M7-B
  scrive *«8 pf se la Scena 10 è andata male»*.
- **Correzione**: una parola nella riga 0: «e Re Thorek a 8 pf, come con 1».

### 🟡 12 · Durik e i Treant non hanno una casella su M7-B

- **Scena**: 11. **Prova**: mark 6: *«T16 ; Hella, con Durik accanto»*; la regia
  ha una battuta per Durik (4-bis). I due Treant dell'alba caricano fuori, ma
  uno può essere richiamato nel duello (Scena 6, «Chi vola, e chi no»).
- **Correzione**: mark per Durik (U16) e, se serve, una nota «Treant: entrano
  dalla porta L-M18».

### 🟡 13 · La quota d'ingresso e la linea del soffio

- **Scena**: 11, round 1. **Prova**: M7-B mette il drago a V1 *«circa 45 m»*;
  il round 1 *«Apre col Soffio acido sul gruppo più fitto»*, e il soffio è una
  linea di 30 m. Per soffiare sui PG alla riga 16 deve prima scendere sotto i
  30 m di distanza (movimento più azione standard: si può, ma va detto).
- **Correzione**: una riga sotto la griglia: «round 1: picchia fino a ~20 m di
  quota sopra il cortile, poi soffia».

### 🟡 14 · M7-C semplifica le guardie e i rinforzi

- **Scena**: 8. **Prova**: M7-C, round 1: *«le quattro guardie ingaggiano i PG
  più esposti»*. Il master: *«due restano al seggio e due vanno sul PG più
  esposto»*, e le due che vanno scelgono chi lancia o colpisce da lontano. Sui
  rinforzi M7-C dà solo i round d'arrivo; il master aggiunge che non entrano
  finché Zog'tar è in piedi, aspettano fuori e le ondate non finiscono.
- **Correzione**: copiare le due frasi del master nel JSON di M7-C.

### 🟡 15 · Il Treant di DEF-4 ha numeri più bassi della sua fonte

- **Scene**: 10-11. **Prova**: DEF-4 A.6: *«FOR 28, TS Temp +11 Rifl +2 Vol
  +7»*. DEF-3 A.2, che la scheda `mostri/treant-di-adamantio-cr10.md` dichiara
  come fonte: FOR 29, Tempra +12, Riflessi +3, Volontà +8, più Travolgere e la
  vulnerabilità al fuoco. DEF-5 A.3 non dà FOR né TS.
- **Correzione**: A.6 di DEF-4 con i numeri di DEF-3 A.2.

### 🟡 16 · Le schede d'entrata della tenda non descrivono le armi delle schede

- **Scene**: 7-8. **Prova**: la scheda d'entrata di Zog'tar: *«armatura
  completa di piastre annerite»*; A.2: *«armatura completa di mithral +2 … è
  preda presa ai nani, e i nani la riconoscono»*. Le guardie, fra le comparse,
  *«battendo l'asta per terra»*; A.2 dà loro lo spadone e i giavellotti.
- **Correzione**: «armatura di mithral annerita, di fattura nanica» e «battendo
  il piatto dello spadone per terra».

### 🟡 17 · Scheda di Balvar: il GS del generale e la soglia di morale

- **Scena**: 7-8. **Prova**: Notes: *«consigliere del generale **Zog'tar
  Deatheye** (CR 14)»*: è 15. **Tattiche** rimanda alla Scena 7 ma non porta il
  *Morale* che ADR-0091 chiede (la soglia dei 30 pf e la lastra, D52).
- **Correzione**: CR 15; in Tattiche «*Morale*: sotto i 30 pf non fugge, finisce
  di incidere la lastra (round completo, D52/D71)».

### 🟡 18 · L'età di Re Thorek I

- **Scena**: 4, con eco nell'11. **Prova**: `png/re-thorek-i-cr16.md`: *«Nano di
  180 anni»*; nella Source della stessa scheda e nel master (Scena 4): *«182
  anni»*.
- **Correzione**: 182 nel Summary.

### 🟡 19 · Durin «muore alle mura nella Scena 4»

- **Scena**: 10. **Prova**: `png/durin-rocciadura-cr6.md`: *«al più muore alle
  mura nella Scena 4, che è una battaglia di massa»*. La Scena 4 è il consiglio;
  le mura sono la 10.
- **Correzione**: «Scena 10».

### 🟡 20 · La scheda di Skullcrusher fissa un esito che il master lascia aperto

- **Scena**: 11. **Prova**: la scheda: *«Cadde sotto Aegis Fang impugnata da
  **Thorgrim Barbadiferro**»* (lo dice anche Aegis Fang ad A7, in DEF-2). Il
  master: il duello lo fanno i PG, Thorik porta Aegis Fang, e l'esito è
  *«aperto — MAI fisso»*: il drago può anche fuggire ferito.
- **Correzione**: decisione del DM. Una lettura che regge tutto è «Aegis Fang
  ricorda il drago caduto sotto i suoi colpi, e non dice in quali mani»; la
  scheda va allineata a quella che il DM sceglie.

### 🟡 21 · La scheda di Sal racconta un Vatore diverso

- **Scena**: 9. **Prova**: `villain/Salvatore/Salvatore.md` r.87: *«Ha appena
  visto quattro individui respingere un'orda intera da soli»*. Il master: *«Ha
  appena visto quattro ombre uscire vive dalla tenda del generale»*. Il dossier
  ha ancora `[DA SCRIVERE]` in «Cosa vuole» ed «Esiti possibili» (ADR-0091).
- **Correzione**: la frase del master; gli esiti si possono riempire col
  rimando alla tabella della Scena 9.

### 🟡 22 · Thorgrim: tre sezioni vuote, e un intervento che contraddice «non combatte»

- **Scene**: 4, 11 (§6). **Prova**: `png/thorgrim-barbadiferro.md` ha
  `[DA SCRIVERE]` in Motivation, «Aspetto e voce» e «Cosa vuole», mentre la
  Scena 4 del master ha aspetto e voce. DEF-4 §6, *vinto sporco*: *«Thorgrim e
  gli antenati intervengono e ricacciano il drago»*; A.5 e la scheda: *«un
  vecchio, vivo e fragile, che non combatte»*.
- **Correzione**: riempire le due sezioni dalla Scena 4; nel §6 «gli antenati,
  guidati da Thorgrim che dà l'ordine».

### 🟡 23 · Ghostlord: chi ha dato i componenti a Zeth

- **Scena**: 5 (e il riconoscimento della Scena 9). **Prova**:
  `villain/Ghostlord/Ghostlord.md`: *«ingannato da un chierico incappucciato di
  Shar»*. Il master: *«Era Vatore»* (Q4-bis), che è un ladro, non un chierico;
  Zeth lo crede un chierico. La riga Status è `[DA SCRIVERE]`.
- **Correzione**: «da un incappucciato che si presentò come chierico (era
  Vatore, `ARC07-DEF-4` Scena 5, Q4-bis)».

### 🟡 24 · Tre scontri possibili di stasera senza griglia

- **Scene**: 6, 10, 11. **Prova**: la pattuglia dei tre fallimenti (otto
  hobgoblin, EL 10) e la squadra dei lupi (EL 9) della Scena 6 si giocano su
  M7-A, che si dichiara *«non in scala»*. Zog'tar sulla breccia (EL 16, Scena
  10) si gioca su un camminamento *«largo quanto un tavolo da pranzo»* che
  nessuna mappa disegna, con lo stringersi, il bordo e la caduta di 4,5 m.
  Il duello sulla spianata (arieti sabotati) dice da sé *«M7-B non serve»* e non
  ha una mappa. Il ritorno a piedi è probabile anche per chi va in volo (le
  pozioni bastano per l'andata, Scena 6).
- **Correzione**: per stasera basta una nota d'improvvisazione (fascia di tende
  M7-C fuori dal telo per il campo; una striscia di 1 quadretto per 12 col
  bordo a 4,5 m per la breccia). Le griglie vere sono un lotto di mapmaking.

### 🟡 25 · PNG e creature senza scheda, e un worg che non è quello del master

- **Scene**: 5-11. **Prova**: Kettra, Brynja, Gunnvor, Grask, Hrodgar, Hald,
  il sacerdote dell'orda e le wyvern vivono solo nel master (cercati in
  `Bestiario/` e `campaign/`). I numeri che servono ci sono (Grask, sacerdote,
  wyvern in A.2/A.6), quindi non è un blocco. Attenzione al worg: il master usa
  il worg SRD (30 pf, CA 14, morso +7 1d6+4); in `mostri/` c'è solo
  `worg-cavalcatura-cr2.md` (6 DV, 51 pf, morso +9 1d8+4), che è la cavalcatura
  della Mano Rossa.
- **Correzione**: nessuna per stasera; il DM non apre la scheda del worg del
  Bestiario per la Scena 6.

---

## 3. Le schede ADR-0091 della serata

| Scheda | Tipo | Le cinque etichette | Cosa manca |
|---|---|---|---|
| Balvar | statblocco | Difesa, Attacco, Statistiche, Capacità speciali, Tattiche: tutte | il *Morale* dentro Tattiche (🟡 17) |
| Skullcrusher, Zog'tar, Durin, Re Thorek I | POINTER | esenti (ADR-0091 §3, L-D3) | la scheda di Skullcrusher porta numeri superati (🟠 3) |
| Thorgrim | dossier, NON-CREATURA | non ha statblocco | `[DA SCRIVERE]` in tre punti (🟡 22) |
| Salvatore | dossier | — | `[DA SCRIVERE]` in «Cosa vuole» ed «Esiti possibili» (🟡 21) |
| Ghostlord | dossier | — | Status `[DA SCRIVERE]` (🟡 23) |
| Dana, Re Thorek Hammerfist | dossier brevi con rimando | — | niente |
| Treant, hobgoblin sergente, worg | `mostri/`, fuori da ADR-0091 | — | numeri del Treant di DEF-4 non allineati (🟡 15) |

Il gate `--forma` passa su tutte: misura la presenza delle sezioni, non se
dentro c'è un `[DA SCRIVERE]` né se il numero è quello del master.

---

🔴 0 · 🟠 7 · 🟡 18
