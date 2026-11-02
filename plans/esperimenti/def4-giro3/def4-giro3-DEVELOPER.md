# DEF-4, giro 3: il rapporto del developer

Bersaglio: `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
(3.404 righe, lette tutte; ignorate le parti `<!-- storico -->`). Rubrica:
`skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md` §1-8.
Party: 4 PG di 13° livello, APL 13, tetto EL 17.

**INPUT GAP:**
- `skills/dnd-35-srd/references/` non contiene le tabelle dei mostri: i numeri del
  drago nero (adulto maturo e vecchio) li ho presi da d20srd.org, *Dragon, True*.
  Worg, hobgoblin, orco, adepto e i prezzi degli oggetti li ho controllati a memoria
  dell'SRD.
- Non sono SRD, quindi non li posso verificare: la razza mezzo-ogre/orco di Zog'tar
  (taglia, armatura naturale e caratteristiche di base, prima del template),
  il Runecaster di Balvar (BAB e TS), l'Occhio di Ossidiana, la Cintura di Tordek,
  il Treant di Adamantio (`DEF-3` A.2), le invocazioni di Artemis.
- Le schede dei PG non le ho aperte: armatura, Forza e velocità di volo reali di
  Thorik, Tordek e Artemis non le conosco, e i rilievi che ne dipendono sono
  condizionali.
- I PX dei GS molto sotto l'APL (CR 8 e meno contro il 13°) li ho stimati con la
  progressione della tabella DMG 2-6, che a memoria non ho per intero. Stima:
  CR 8 ≈ 650 in totale.
- Non ho aperto la tabella B4 (`PortaleForgia-P5-B4-CARRYOVER-...`), la mappa M7-C
  e l'atlante delle mappe.

## Rilievi

| # | Scena | Domanda della rubrica | Cosa non torna | Il conto giusto | Gravità | Prova (alla lettera) |
|---|---|---|---|---|---|---|
| 1 | 8 · tenda | §2 volo · §8 tattica | *Comando superiore* scritto come un ordine che vale 13 round, senza il nuovo TS. Per l'SRD, all'inizio di ogni sua azione dopo la prima, il bersaglio ritenta Volontà per liberarsi. Così com'è scritto tiene proni per 13 round tutti i PG tranne Thorik, e lo scontro è deciso | Volontà CD 20 al primo round, poi un **nuovo TS CD 20 all'inizio di ogni turno** del bersaglio: chi lo supera è libero | 🟠 | «Volontà **CD 20**, e si ripete ogni round per 13 round» |
| 2 | 6 · variante dall'alto | §2 volo | *Volare* dà 18 m solo senza armatura media o pesante e senza carico medio. Un nano in armatura completa (anche di mithral, che conta come media) vola a **12 m**. In 5 minuti fa 1.200 m con il doppio movimento, non 1.800: l'andata (1 km) ci sta, ma con 8 round di margine. Con la pozione d'invisibilità comprata (3 minuti) arriva a 720 m, quindi non copre il chilometro | Thorik (e chiunque porti armatura media o pesante): volo 12 m, 24 m/round → 1.200 m in 5 min; invisibilità di 3 min → 720 m | 🟠 | «18 m di velocità, circa 1.800 m in tutto: basta per l'andata» · «1 km lo copre appena» |
| 3 | 11 · sidebar «Scalare» | §1 EL e GS | Il drago nero **Vecchio** dell'SRD è GS **17**, non 16 (gli altri numeri della riga sono giusti: 287 pf, 16d4 CD 27, Presenza CD 24, morso +32, RI 22). La sidebar non dice se gli si mette sopra anche il template Avanzato del drago di base: con il template diventa GS 18, oltre il tetto | GS 17 = APL+3 solo per il gruppo di 14° che la riga presuppone; contro APL 13 è APL+4, al tetto. Con l'Avanzato: GS 18, fuori tetto | 🟠 | «Skullcrusher **Vecchio** dell'SRD (GS 16, EL = APL+3, sotto il tetto)» |
| 4 | A.2 · Zog'tar | §5 fuori SRD | **Presenza Minacciosa** non esiste nell'SRD per un barbaro/guerriero, e non porta `[INFERRED]` né una riga di Boost log. Anche con la formula della Presenza Terrificante dei draghi la CD verrebbe 10 + ½ DV (7) + CAR (+4) = 21, non 22 | o si toglie, o si marca `[INFERRED — needs DM confirmation]` con Boost log; CD 21 | 🟠 | «• Presenza Minacciosa: entro 9 m, Vol CD 22 o scosso 1d4 round» |
| 5 | §8 A · Scene 6-8 | PX contro le tabelle | 2.400 PX a testa per le Scene 6-8 «con il campo e Balvar». Lo scontro intero nella tenda, a tabella DMG per il 13°, vale: Zog'tar GS 15 = 7.800, Balvar GS 13 = 3.900, 4 guardie GS 8 ≈ 2.600, sacerdote GS 6 ≈ 300. In totale ≈ 14.600, cioè ≈ **3.650 a testa**. Senza Balvar ≈ 2.700. Pattuglia (EL 10), lupi (EL 9) e banda non hanno una voce PX | ≈ 3.650/PG se si combatte tutta la tenda; ≈ 2.700 con Balvar recuperato; più poche decine a testa per la pattuglia e i lupi | 🟠 | «Scene 6-8: il campo, Balvar, Zog'tar (GS 15) \| combattimento veloce \| 2.400» |
| 6 | §8 B · tesoro | tesoro contro le tabelle | L'equipaggiamento di Zog'tar (armatura completa di mithral +2 Grande, ascia a due mani +1 Grande, l'Occhio), di Balvar (mithral +2, anello +2, martello runico +1, polvere di diamante) e delle quattro guardie non è nel tesoro, e il testo non dice se si può prendere. La tabella DMG del tesoro per incontro dà circa 36.000 mo a EL 17 e 17.000-22.000 a EL 14-15; §8 B arriva a circa 10.400 più il Sigillo | una riga in §8 B per il bottino della tenda: solo l'equipaggiamento scritto negli statblocchi vale ≈ 40.000-45.000 mo, cioè il tesoro di un EL 17 | 🟠 | «### B. Tesoro PREGENERATO (i doni di Re Thorek I + il bottino del passato)» (nessuna riga per la tenda) |
| 7 | App. C.2 · versione veloce | §6 «un solo posto per la regola» | La versione veloce del campo ha un'altra regola: 3 tiri invece di 5 blocchi, Nascondersi **CD 20** invece di 22, Osservare come prova di infiltrazione, e la pattuglia scatta con «meno della metà» invece che con tre blocchi falliti | stesse CD del corpo (MS 20, Nascondersi 22) e stesso costo dei fallimenti; la versione veloce cambia solo il numero dei tiri | 🟠 | «Muoversi Silenz./Nascondersi/Osservare **CD 20** … meno della metà = la pattuglia» |
| 8 | 11 · A.1 | §1 GS | Il template Avanzato PF1e alza il GS di 1: il drago vale GS 15, e i PX sarebbero 7.800/4 = 1.950 a testa invece di 1.460. Il DM ha deciso di contarlo 14 (Q37, D40) | 1.950/PG se si segue il template; 1.460 per scelta dichiarata del DM | 🟡 | «senza alzare il GS: vale come un GS 15 e si conta come 14» |
| 9 | 8 e 10 · EL | §1 EL | Se Zog'tar si conta per quello che vale (GS 16, Boost log), la tenda senza Balvar è EL 17 (≈16,6), non 16, e così la breccia con le 4 guardie. La tenda intera resta a EL 17 (≈17,4) | senza Balvar EL 17 · breccia EL 17 | 🟡 | «Senza Balvar, **EL 16**» · «(Appendice A.2; EL 16, senza Balvar e senza il sacerdote» |
| 10 | 10 · breccia | PX | «Circa 1.950 a testa» conta il solo Zog'tar; sulla breccia ci sono anche le quattro guardie | ≈ 7.800 + 2.600 = 10.400 → **≈ 2.600/PG** | 🟡 | «Se Zog'tar si combatte solo qui, vale circa **1.950 a testa**» |
| 11 | 5 · banco | tesoro (prezzi) | lo sconto del 15% su 11.030 dà 9.375,5, non 9.350; totale acquisti 47.992, saldo ≈ 19.630 | 9.375 · totale 47.992 · saldo 19.628 | 🟡 | «SRD 11.030, pagata col −15% fatto al tavolo \| 9.350» |
| 12 | A.4 · Balvar | statblocco | L'anello +2 è di protezione (deviazione), e la deviazione vale anche contro i contatti. Con DES +2, il contatto è 14, non 12. L'errore è nella scheda del Bestiario (l'include è sincronizzato) | contatto 14 (10 + DES 2 + deviazione 2) | 🟡 | «ca-dettaglio: contatto 12, colto 22 (mithral +2, anello +2, DES +2)» |
| 13 | A.2 · guardie | statblocco | Volontà +1 con guerriero 8 (base +2) vuol dire SAG 8-9 (−1), ma allora Ascoltare e Osservare senza gradi fanno −1, non +1 (come per la pattuglia, che ha −1 e Vol +0). Lo spadone a 2d6+6 vuol dire FOR 18 senza Arma Specializzata, che un guerriero 8 di solito ha. La CA 20 non torna con armatura completa e DES +1 (19) | Ascoltare/Osservare −1, oppure Vol +2. Danno 2d6+8 se ha Arma Specializzata. CA 19 se non c'è altro | 🟡 | «TS Temp +8, Rifl +3, Vol +1 … Ascoltare +1 · Osservare +1 (… senza gradi nelle due abilità)» |
| 14 | A.3 · Durin | statblocco | Volontà: guerriero 6 base +2 e SAG 14 (+2) fanno +4, non +3. Non si usa scudo con un'arma doppia impugnata su due lati. L'ascia doppia orchesca ha critico ×3 su 20, non su 19-20 senza Critico Migliorato | Vol +4; CA senza scudo (21 con DES 0, se l'armatura completa +1 resta); critico 20/×3 | 🟡 | «CA 22 (arm. completa +1, scudo) · … Ascia Doppia +1 +9 (per lato, 1d8+5, 19-20/×3) · TS … Vol +3» |
| 15 | 6 · skill challenge | §6 chi tira | La «prova di gruppo» con la regola «riesce se riesce la metà» non è dell'SRD 3.5 (che ha solo aiutare un altro). Va bene come convenzione, ma è etichettata SRD | togliere «(SRD)» o scrivere «convenzione del modulo» | 🟡 | «**Ogni blocco è una prova di gruppo** (SRD): tirano tutti, e il blocco riesce se riesce almeno la metà» |
| 16 | 6 · skill challenge | §6 cosa costa il fallimento | Il testo non dice cosa succede dopo la pattuglia se i fallimenti continuano: il contatore riparte da zero? Una seconda pattuglia al sesto fallimento? | una riga: «dopo la pattuglia il contatore riparte da zero; al terzo fallimento successivo, un'altra pattuglia» (o quello che decide il DM) | 🟡 | «**Tre blocchi falliti** prima dei cinque: **la pattuglia** … Dopo lo scontro si riparte dal blocco in cui si era» |
| 17 | 6 · durata dell'invisibilità | §2 | Il conto dei 360 m usa un solo movimento a metà velocità per round. Con due azioni di movimento a passo furtivo un nano fa 6 m a round, cioè 720 m in 12 minuti (3,6 blocchi). Anche a 3 m/round, 360 m sono 1,8 blocchi, non due | o «un solo movimento a round» dichiarato come regola, o 720 m ≈ tre blocchi e mezzo | 🟡 | «Un nano in armatura, a passo furtivo, fa 3 m a round: 12 minuti coprono circa **360 m**, i primi **due blocchi**» |
| 18 | 8 · rinforzi | §8 tattica | Ronde di orchi e squadroni hobgoblin arrivano alla tenda in 1d4+2 e 2d4+2 round, ma come combattono una volta arrivati non è scritto. Lo stesso vale per i 2 wyvern della sidebar, che non hanno né statistiche né tattica | una riga per caso: chi va su chi, quando smette, cosa fa contro volo e invisibilità; per i wyvern, statistiche SRD (GS 6) | 🟡 | «Chi resta oltre il loro arrivo combatte l'orda, non più un generale» · «oppure 2 **wyvern** scortano il drago dal round 2» |
| 19 | 11 · duello | §3 tre TS | Nel duello ci sono Riflessi (soffio) e Volontà (Presenza, *corrompere l'acqua*), ma nessun effetto chiede Tempra. Se è voluto, non è dichiarato | dichiararlo, o dare al drago un effetto a Tempra | 🟡 | «Soffio ACIDO … Riflessi CD 28 ½» · «Presenza Terrificante … Volontà CD 25» |
| 20 | 10 · prova delle mura | §6 | «Forza o attacco CD 18»: un guerriero di 13° supera l'attacco con 1 sul d20 (bonus +20 o più). La via «Tenere la breccia» non ha incertezza per Thorik e Tordek | se si tira l'attacco, CD 30-32, o la via accetta solo la prova di Forza | 🟡 | «**Tenere la breccia** \| Forza o attacco, **CD 18**» |
| 21 | 6 · sciamani | statblocco | Un adepto ha incantesimi di 2° livello dal 4° (0 slot più quelli bonus di SAG), non solo dal 5°. Per gli orchi, con SAG bassa, l'effetto pratico è lo stesso | «dal 4° con SAG 14+, dal 5° altrimenti» | 🟡 | «(un adepto lancia incantesimi di 2° livello solo dal 5°)» |
| 22 | A.4 / Bestiario | coerenza | La scheda del Bestiario di Balvar chiama ancora Zog'tar «CR 14»; il modulo lo dà GS 15 | CR 15 | 🟡 | `Bestiario/villain/balvar-fuocospento-cr13.md`: «consigliere del generale **Zog'tar Deatheye** (CR 14)» |
| 23 | 4 · doni / §8 B | tesoro | Nella Scena 4 la fiducia piena dà 4 pozioni d'invisibilità CL 12 (4 × 1.200 = 4.800 mo); in §8 B, 4 di *cura ferite gravi* (6.600 mo); le 5 pozioni di *volare* regalate (3.750 mo) non sono in §8 B. Le due versioni sono dichiarate (Scena 6), ma §8 B ne conta una sola | elencare in §8 B le due versioni, e le 5 di *volare* | 🟡 | «**fiducia piena**: 4 Pozioni di Invisibilità CL 12» · «4 **pozioni di *cura ferite gravi***» |

## Conteggio per gravità

- 🔴: **0**
- 🟠: **7** (1-7)
- 🟡: **16** (8-23)

## Cosa ho verificato e torna

**Skullcrusher (A.1), contro d20srd.org più il template Avanzato.** Adulto maturo
SRD: FOR 27, DES 10, COS 21, INT 14, SAG 15, CAR 14, nat +21, BAB +22, Temp/Rifl/Vol
base 18/13/15, soffio CD 26, Presenza CD 23, RI 21, RD 10/magia, GS 14. Con +4 a
tutto e +2 nat:
- pf 22d12+154 = 297;
- CA 33, contatto 10, impreparato 31, 37 con *armatura magica*; la runa a CA 41;
- Temp +20, Rifl +17 (Riflessi Fulminei), Vol +19 (Volontà di Ferro);
- Lotta +40;
- morso +30 (2d8+10), artigli e ali +25 come attacchi secondari a −5, coda 2d6+15;
- soffio 14d4 in linea di 30 m, CD 28; Presenza raggio 63 m, CD 25;
- schiacciare 2d8+15 solo contro creature Piccole o minori;
- *oscurità* 21 m, *corrompere l'acqua* CD 25;
- 8 talenti per 22 DV; incantatore di 5° con 6/7/5 al giorno e CD 14+livello;
- velocità 18/45 (scarsa)/18; iniziativa +6; percezione cieca 18 m, scurovisione 36 m.

Tutti giusti. Il conto della RI (8-9 sul d20) torna, e la soglia a ⅓ (≈ 99 pf) pure.

**Zog'tar (A.2).**
- pf 283 = 168 + 10 + 7×15; in Ira 328 (COS 30).
- BAB +15, Lotta +29/+32.
- CA 26, contatto 12, 24 in Ira; il mithral alza la DES massima a +3.
- Mischia +29/+24/+19 (3d6+20) in Ira, +26 (3d6+16) fuori. Colpo Devastante a −4,
  quindi +25, con Riflessi a CD pari al danno, 3 m. Giavellotti +19, 1d8+13.
- TS Temp 18/21, Rifl 9, Vol 9/12/16.
- Ira Superiore: 13 round; 6 al giorno con Ira Extra.
- RD 3/— al 13°, Volontà Indomita al 14°, Percepire Trappole +4, Ira Instancabile
  al 17°.
- 7 talenti (6 + 1 da guerriero); prerequisiti del Colpo Devastante rispettati.
- Abilità coerenti con i gradi dichiarati. Attacco Poderoso −5/+10 e −10/+20 a due mani.

**Sacerdote.** Adepto 7: GS 6, 38 pf, TS +4/+4/+7, slot 3/4/3 con SAG 15, CD 12+liv,
*comando* CD 13, lista dell'adepto.

**Pattuglia.** Guerriero 4 hobgoblin: 30 pf, spada lunga +6 (1d8+3), TS +6/+2/+0. Otto
da GS 4 fanno EL 10.

**Altri statblocchi.**
- Worg SRD: GS 2, 30 pf, CA 14, morso +7 (1d6+4), sbilanciare, sensi +6, fiuto
  9/18/4,5 m. Dieci worg con dieci goblin fanno EL 9.
- Grask: hobgoblin combattente 1, 6 pf, CA 15, −10 ad Ascoltare mentre dorme.
- Balvar: CD 15+liv (SAG 20). *Barriera di lame* 13d6, CD 21; *ferire mortalmente*
  CD 20; *comando superiore* CD 20; glifo CD 18, 5d8. *Epurare invisibilità* 19,5 m
  per 13 minuti. Cercare e Disattivare CD 28, dissolvere CD 24. Glifo legato a una
  razza (SRD) e polvere da 200 mo. pf 96 (13d8+39) e Lotta +9.

**EL della tenda.** Con i GS dichiarati la somma fa EL 16,85, cioè 17, al tetto di
APL+4. Senza Balvar fa 15,96, cioè 16. Il drago sulla tenda la porta a EL 18-19.

**PX.**
- Skullcrusher a GS 14 contro il 13°: 5.850 in totale, 1.460 a testa.
- Zog'tar a GS 15: 1.950 a testa.
- Totale di §8 A: 6.360.

**Prezzi del banco, tutti SRD.**
- Pergamene: *silenzio* 150, *rimuovi maledizione* 375, *identificare* 125 (perla
  compresa), *dissolvi magie* al 9° 675, *resistere all'energia* al 7° 350 (20 di
  resistenza per 70 minuti), *ristorare* 800, *cura critiche* 700, *cura gravi* 375,
  *neutralizza veleno* 700.
- Pozioni: *volare* 750 (5 minuti), *invisibilità* 300 (3 minuti), *cura gravi* all'11°
  1.650 e 4 × 1.650 = 6.600, *velocità* 750, *neutralizza veleno* 750 (valida come
  incantesimo di 3° del druido o del ranger).
- Servizi: 60, 150, 280, 380, 5.450 per *rianimare morti*; *silenzio* all'8° 160.
- Bombe: 750 mo, CD 14.
- Armi e armature: ascia +1 del gelo 8.330; ascia d'adamantio 3.030, +2 a 11.030;
  scudo +2 con spuntoni +1 gelidi 12.480.
- Vendite: corazze e scudi +1/+3 e asce +1 col tetto di 2.500; incasso 28.364
  (Gunnvor 12.050, forziere 10.000, pesatore 6.314). Il totale degli acquisti
  torna (47.967) con il 9.350 dichiarato.

**Regole.**
- *Identificare* una pozione: Sapienza Magica CD 25, e prendere 10 con +15 la
  supera.
- La scuola con *individuazione del magico*: Sapienza Magica 15 + livello.
- Le Benedizioni (+2 morale) e il banchetto (+1 morale) non si sommano.
- Caduta da 4,5 m: 1d6. Stringersi: −4 al colpire e alla CA. Stabilità: +4.
- Gancio con incremento di 3 m; balestra pesante 1d10, incremento 36 m.
- Portata del morso del drago 4,5 m; *Attacco in Volo* concede un attacco solo.
- Thorik immune a *comando* con *mente vuota*; *comando* fallisce se l'ordine non si
  può eseguire.
- *Àncora dimensionale* non tocca il volo.
- *Silenzio* ha 6 m di raggio e dura 1 minuto per livello. *Vedere invisibilità* al
  5°: 50 minuti; *armatura magica* al 5°: 5 ore.

**Rubrica.**
- §2, volo e invisibilità: hanno risposta il campo, la tenda (il telo alto 6 m, i
  giavellotti, il palo, *epurare*), la breccia, il duello (percezione cieca e
  *vedere invisibilità*) e Vatore.
- §4, chi sente: alla tenda Grask in 1d4 round, il sacerdote in 1d4+1, le ronde in
  1d4+2, gli squadroni in 2d4+2, il drago in 70 round. Nella pattuglia e con i lupi,
  le ronde in 1d4+2. Lo sciamano chiama la banda in 1d4+2.
- §5, la soglia del boss: c'è per Skullcrusher (⅓ dei pf, il round in più dopo due
  colpi), per Zog'tar (30%) e per Balvar (30 pf).
- §1, chi non vola contro il drago: preparare l'azione sulle corde, le balestre delle
  mura, il gancio contro il contatto 10.
- §6, lo skill challenge del campo: dice chi tira, cosa tira, quanti successi servono
  (5) e cosa costano i fallimenti (tacca, pattuglia, CD +2), con una tabella delle
  complicazioni.
- §8, le tattiche: ci sono per la pattuglia, i lupi, gli sciamani, le guardie, Zog'tar
  sulla breccia, il drago sulla tenda e il drago sulle colline (§6).
