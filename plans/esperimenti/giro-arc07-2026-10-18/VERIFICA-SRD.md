# Verifica in rete dei numeri SRD 3.5 nei master di ARC-07

Data: 2026-10-18. Sola lettura: nessun file del repo è stato toccato.
Master: `07_il Portale Della Forgia Eterna/ARC07-DEF-{1..5}-*.md` (le righe sotto si riferiscono a questi file).

**Fonti raggiungibili.** d20srd.org, d20pfsrd.com e web.archive.org sono bloccati dal proxy. Hanno risposto tre mirror dell'SRD 3.5:
- `dungeons.fandom.com/wiki/SRD:*` (D&D Wiki, OGL)
- `birthright.net/wiki/index.php/*` (sezione «D20 SRD (3.5)»)
- `www.rpgcrossing.com/srd/*.html` (il testo «System Reference Document v3.5»)

Per il PF1e ho usato `legacy.aonprd.com`. Alcune pagine non si sono aperte (errore del client o limite di richieste 429): sono elencate in fondo.

**Criterio (la regola del DM).** Un numero conta come discrepanza in due casi soli: il master lo attribuisce all'SRD e l'SRD dice un'altra cosa, oppure il conto aritmetico è sbagliato rispetto alle regole verificate. Le scelte marcate `⚠ Non SRD`, `[CANONE — DM …]` o con un `Boost log` sono **confermate come scelte dichiarate**, non sono discrepanze.

## Sigle delle fonti

| Sigla | URL |
|---|---|
| XE | https://dungeons.fandom.com/wiki/SRD:Elder_Xorn |
| XA | https://dungeons.fandom.com/wiki/SRD:Average_Xorn |
| EE | https://dungeons.fandom.com/wiki/SRD:Elder_Earth_Elemental |
| AB | https://dungeons.fandom.com/wiki/SRD:Awesome_Blow |
| BD | https://dungeons.fandom.com/wiki/SRD:Black_Dragon |
| DR | https://www.rpgcrossing.com/srd/monstersDrtoDw.html (draghi veri, regole generali + drago nero) |
| TR | https://birthright.net/wiki/index.php/Treant |
| WY | https://birthright.net/wiki/index.php/D20:Wyvern_(Creature) |
| WO | https://dungeons.fandom.com/wiki/SRD:Worg |
| GO | https://dungeons.fandom.com/wiki/SRD:Goblin |
| OR | https://birthright.net/wiki/index.php/D20:Orc_(Creature) |
| HB | https://birthright.net/wiki/index.php/Hobgoblin |
| DRU | https://www.rpgcrossing.com/srd/druid.html |
| ARM | https://www.rpgcrossing.com/srd/armor.html |
| CON | https://birthright.net/wiki/index.php/Consecrate |
| DUN | https://birthright.net/wiki/index.php/D20:Dungeons_(Rules) (tabella dei muri) |
| CMI | https://dungeons.fandom.com/wiki/SRD:Creating_Magic_Items |
| ED | https://dungeons.fandom.com/wiki/SRD:Energy_Drain,_Negative_Levels,_and_Level_Loss |
| RES | https://birthright.net/wiki/index.php/Restoration · https://birthright.net/wiki/index.php/Restoration,_Lesser |
| HEA | https://birthright.net/wiki/index.php/Heal |
| CMD | https://birthright.net/wiki/index.php/Command · https://dungeons.fandom.com/wiki/SRD:Range_(Spell_Descriptor) |
| ST | https://birthright.net/wiki/index.php/Saving_Throw |
| NAU | https://birthright.net/wiki/index.php/Nauseated |
| GOL | https://birthright.net/wiki/index.php/D20:Iron_Golem_(Creature) · https://dungeons.fandom.com/wiki/SRD:Golem |
| GRA | https://birthright.net/wiki/index.php/Grapple |
| KN | https://birthright.net/wiki/index.php/D20:Knowledge_(Skill) |
| RD | https://birthright.net/wiki/index.php/Raise_Dead · https://legacy.aonprd.com/coreRulebook/spells/raiseDead.html |
| MB | https://birthright.net/wiki/index.php/Mind_Blank |
| ADV | https://legacy.aonprd.com/bestiary/monsterAdvancement.html (template Avanzato PF1e) |

## Tabella

| voce | file:riga | cosa dice il master | cosa dice la pagina (URL) | esito | correzione proposta |
|---|---|---|---|---|---|
| **DEF-4 · rilievo #1 del developer: Colpo Devastante contro il Treant** | DEF-4:957 | il Colpo Devastante non funziona sul Treant, che è Grande come Zog'tar | «If the creature hits a corporeal opponent smaller than itself…»; prerequisiti FOR 25, Attacco Poderoso, Spingere Migliorato, taglia Grande o più (AB) | confermato (il rilievo è già corretto nel master) | — |
| Colpo Devastante di Zog'tar: −4 al colpire, CD pari al danno, 3 m, prono, 1d6 contro l'ostacolo | DEF-4:3610-3612, 3629 | +25 in Ira (+29 − 4), Riflessi CD = danno, vola via di 3 m e cade prono, +1d6 a lui e all'ostacolo | coincide (AB); il guerriero lo può prendere come talento bonus | confermato | — |
| Fauci di Diamante: base Xorn anziano | DEF-1:653-659 | anziano dell'SRD avanzato da 15 a 21 DV, sempre Grande | XE: Grande, 15d8+63 (130), FOR 25 COS 19, CA 25 (−1, +16 nat), contatto 9, morso +21 (4d8+7), 3 artigli +19 (1d6+3), TS +13/+9/+9, Avanzamento 16-21 DV (Grande) | confermato | — |
| Fauci: DV, pf, FOR, lotta, morso, artigli, TS | DEF-1:654-659 | 21d8+87 (181), FOR 27, BAB/Lotta +21/+33, morso +29 (4d8+8), artigli +26 (1d6+4), TS +16/+12/+12 | i conti tornano su XE: 21 DV × 4,5 + 84 + 3 = 181; +2 FOR dai DV 16 e 20; 21+8+4 = 33; 21+8−1+1 = 29; TS buoni da esterno +12 | confermato | — |
| Fauci: CA 28 (+19 nat), RD 10/contundente, Spaccare che cura | DEF-1:655, 663, 665 | `⚠ Non SRD` e Boost log; l'avvertenza dice «RD SRD 5/contundente, armatura naturale +16» | XE: RD 5/bludgeoning, +16 naturale | confermato (scelta dichiarata, e l'avvertenza cita i valori SRD giusti) | — |
| **Fauci: portata** | DEF-1:657 | «Spazio 3 m, portata 1,5 m» | XE: «Space/Reach: 10 ft./10 ft.» | **discrepanza** | portata **3 m** |
| Fauci: visione a 360° | DEF-1:657 | «niente fiancheggiamento, mai colto in fallo» | XE: All-around vision dà +4 a Cercare e Osservare e «A xorn can't be flanked»; nessuna immunità all'essere colto alla sprovvista (lo statblocco SRD ha un valore «flat-footed 25») | discrepanza (lieve: con DES 10 la CA non cambia) | togliere «mai colto in fallo», o marcarlo `⚠ Non SRD` |
| Fauci: talenti | DEF-1:659 | otto talenti, Incalzare compreso | a 21 DV spettano 8 talenti (1 + 21/3) più Incalzare bonus (XE lo segna «Cleave^B»): nove in tutto | discrepanza (lieve, non tocca i numeri) | aggiungere un talento (Incalzare Superiore, come nell'SRD) |
| **Fauci: morso e Spaccare nella regia** | DEF-1:699 | «morso +22 … Spaccare +26» | lo statblocco dello stesso master (r. 656, 661) dà morso +29 e Spaccare +33; +22/+26 sono i numeri di una stesura vecchia | **discrepanza (interna, aritmetica)** | **morso +29 · Spaccare +33** |
| **Xorn standard ×2 (GS 6)** | DEF-1:669-673; anche 152 | DV 7d8+21 (52 pf), morso +9 (4d6+3), 3 artigli +4 (1d4+1), Tempra +8, COS 17; RD 5/contundente; nessuna avvertenza | XA: 7d8+17 (48 pf), COS 15, morso +10 (4d6+3), 3 artigli +8 (1d4+1), Tempra +7 Rifl +5 Vol +5, CA 24 (+14 nat), contatto 10, Robustezza fra i talenti | **discrepanza** (presentato come lo Xorn medio dell'SRD) | **7d8+17 (48 pf) · morso +10 · artigli +8 · Tempra +7 · COS 15** (soglia di fuga a 15 pf invariata; r. 152 «Xorn 48 pf»). Altrimenti marcare `⚠ Non SRD` e mettere un Boost log |
| Xorn: Earth Glide «except metal» | DEF-1:642; Terros 1635-1643 | gli Xorn nuotano nella pietra; per Terros l'Altare di mithral conta come pietra, con avvertenza «Diverge dall'SRD» | XE/EE: «…almost any other sort of earth except metal»; *move earth* respinge di 9 m e stordisce 1 round, Tempra CD 15 nega | confermato (per Terros la divergenza è dichiarata) | — |
| Elementale della Terra anziano: base | DEF-1:1584-1599 (Terros) | «Elementale della Terra Avanzato (30 DV), Enorme» | EE: Enorme, 24d8+120 (228), Iniz −1, Vel 9 m, CA 22 (−2 taglia, −1 DES, +15 nat), contatto 7, BAB/Lotta +18/+37, 2 schianti +27 (2d10+11/19-20), FOR 33 DES 8 COS 21 SAG 11, TS +19/+7/+10, RD 10/—, GS 11, avanzamento 25-48 DV (Enorme) | vedi le righe seguenti | — |
| **Terros: CA, contatto, colto** | DEF-1:1592 | «CA 26 (−2 taglia, +18 naturale) · contatto 8 · colto 26»; DES 8 alla r. 1598 | con DES 8 (−1): 10 − 2 − 1 + 18 = **25**, contatto 10 − 2 − 1 = **7**, colto 25 (una DES negativa resta anche da colti) | **discrepanza (aritmetica)** | **CA 25, contatto 7, colto 25**; oppure armatura naturale +19 per tenere 26 |
| **Terros: FOR e velocità sotto la base SRD** | DEF-1:1589, 1594-1598 | FOR 31, Vel 6 m, schianto 2d10+10 | EE: l'anziano a 24 DV ha già FOR 33, Vel 30 ft (9 m), schianto 2d10+11; l'avanzamento a 30 DV aggiunge (1 punto ogni 4 DV) | **discrepanza** (il blocco si presenta come anziano SRD avanzato, ma ha FOR e velocità più basse dell'anziano base; manca un Boost log) | o **FOR 33-34, Vel 9 m, schianti 2d10+11/12** (lotta e colpire salgono di 1-2), o marcare `⚠ Non SRD` («ridotto apposta») e aggiungere un Boost log |
| Terros: lotta, colpire, TS | DEF-1:1593-1599 | +22/+40, schianto +30, TS +24/+9/+12 | conti coerenti con i numeri del master: BAB ¾ a 30 DV = +22; 22+8+10 = 40; 22+10−2 = 30; Tempra buona 17+7, Rifl 10−1, Vol 10+2 | confermato (aritmetica) | — |
| Earth Mastery | DEF-1:1610-1613 | +1 att/danni se entrambi toccano terra; −4 contro chi è in aria | EE: identico | confermato | — |
| Push | DEF-1:1614-1627 | prova di FOR statica CD 25, una volta per round | EE: spinta (bull rush) senza attacco di opportunità, con i modificatori di Earth Mastery sulla prova contrapposta | non è una discrepanza: `[CANONE — DM 2026-07-31]` | — |
| Nauseato | DEF-1:1559-1560 | «la condizione nauseato dell'SRD, che gli lascerebbe la sola azione di movimento» | NAU: «The only action such a character can take is a single move action per turn» | confermato | — |
| Immunità alla magia dei golem | DEF-1:1370-1373 | per l'SRD l'immunità copre ogni incantesimo che ammette RI, *grido superiore* compreso; qui il Diapason passa (dichiarato) | GOL: «An iron golem is immune to any spell or spell-like ability that allows spell resistance» (regola generale: «immunity to most magical and supernatural effects, except when otherwise noted») | confermato | — |
| Lotta: nessun limite di taglia; modificatore Enorme +8; parità al modificatore più alto | DEF-1:1968-1980 | come a fianco; Tordek +12/+16/+21 | GRA: BAB + FOR + mod. speciale di taglia (Grande +4, Enorme +8); «In case of a tie, the combatant with the higher grapple check modifier wins»; nessun limite di taglia per iniziare la lotta | confermato (Tordek: BAB 4+6 = 10, FOR +2 → 12; +4 Lotta Migliorata; ingrandito 10+3+4+4 = 21) | — |
| Skullcrusher, base drago nero adulto maturo | DEF-4:3471-3473, 3484-3522 | i numeri sono quelli della tabella del drago nero | BD/DR: Enorme, 22d12+110 (253), CA 29 (−2, +21 nat), contatto 8, BAB/Lotta +22/+38, attacco +28, TS +18/+13/+15, soffio 14d4 CD 26, Presenza CD 23, LI 5°, RI 21, RD 10/magia; FOR 27 DES 10 COS 21 INT 14 SAG 15 CAR 14; GS 14 | confermato | — |
| Skullcrusher con il template Avanzato | DEF-4:3485-3515 | 297 pf, CA 33 (+23 nat), contatto 10, colto 31, Lotta +40, morso +30 (2d8+10), artigli/ali +25, coda 2d6+15, TS +20/+17/+19, soffio CD 28, Presenza CD 25, incantesimi 6/7/5 | ADV: +4 a tutte le caratteristiche, +2 di armatura naturale. Conti: 22×6,5 + 154 = 297; 10 − 2 + 2 + 23 = 33; 22+8+10 = 40; 22+10−2 = 30; Rifl 13+2+2 (Riflessi Fulminei); Vol 13+4+2 (Volontà di Ferro); 10+11+7 = 28; 10+11+4 = 25 | confermato. **Il dubbio del playtester sull'armatura naturale +23 cade**: 21 SRD + 2 del template = 23 | — |
| Skullcrusher: raggio della Presenza, *oscurità*, linea del soffio, schiacciare, portata | DEF-4:3494, 3497-3505 | 63 m; 21 m; linea di 30 m; schiacciare 2d8+15 CD 28 solo su Piccole o minori; morso 4,5 m | DR: raggio 30 ft × categoria d'età (adulto maturo = 7 → 210 ft = 63 m); *oscurità* 10 ft per categoria (70 ft = 21 m); linea 100 ft per i Enormi; schiacciare «three or more size categories smaller», +1,5 × FOR, CD del soffio; Enorme 15 ft / 10 ft (15 ft col morso) | confermato | — |
| Skullcrusher: RD, RI, immunità, velocità, sensi, *corrompere l'acqua* | DEF-4:3485-3491, 3505-3507 | RD 10/magia, RI 21; immune acido, sonno, paralisi; 18 m, volare 45 m (scarsa), nuotare 18 m; percezione cieca 18 m, scurovisione 36 m; CD di *corrompere l'acqua* = Presenza | DR: tutto coincide | confermato | — |
| Skullcrusher Vecchio, base | DEF-4:3554-3556, 3561-3575 | Vecchio SRD: 287 pf, CD 27/24, GS 16 | DR: 25d12+125 (287), CA 32 (+24 nat), +25/+42, TS +19/+14/+16, soffio 16d4 CD 27, Presenza CD 24, LI 7°, RI 22, FOR 29, GS 16 | confermato | — |
| Vecchio con il template Avanzato | DEF-4:3562-3574 | 337 pf, CA 36, Lotta +44, morso +34 (2d8+11), coda 2d6+16, TS +21/+18/+20, CD 29/26, 6/7/7/5 | conti corretti sul Vecchio SRD più ADV | confermato | — |
| **Vecchio: raggio della Presenza** | DEF-4:3571 | «raggio 63 m» | DR: 30 ft × 8 (Vecchio) = 240 ft = **72 m** | **discrepanza** | **raggio 72 m** |
| **Vecchio: raggio di *oscurità*** | DEF-4:3572 | «Capacità magiche: come A.1» (A.1 dice raggio 21 m) | DR: 10 ft × 8 = 80 ft = **24 m** | **discrepanza** | «come A.1, ma *oscurità* con raggio **24 m**, più *crescita vegetale* 1/giorno» |
| Zog'tar: pf, CA, lotta, attacchi, TS, Ira, RD | DEF-4:3598-3623 | 283/328 pf, CA 26/24, contatto 12, +15/+29 (+32), +29 (3d6+20) in Ira, +26 (3d6+16) fuori, TS +18/+9/+9; Ira Superiore 13 round; RD 3/— | conti corretti: 14×12 + 10 + 7×15 = 283 (+45 in Ira); 10 − 1 + 10 + 3 + 4 = 26; 15+10+4 = 29; 15+13−1+1+1 = 29; TS base barbaro 14 + guerriero 1 = +11/+4/+4. Mezzo-ogre non è SRD, quindi le caratteristiche razziali non sono verificabili | confermato (aritmetica) | — |
| Zog'tar: giavellotti | DEF-4:3609 | +19 (1d8+13) | +19 torna (15 + DES 5 − 1). Il +13 ai danni è la FOR in Ira; fuori dall'Ira (round di sorpresa) è +10 | confermato, con una precisazione | facoltativo: «1d8+13 in Ira, 1d8+10 fuori» |
| Guardie di Zog'tar | DEF-4:3631-3635 | CA 19, 60 pf, TS +8/+3/+1, Ascoltare/Osservare +1 | HB: hobgoblin FOR 13 DES 13 COS 14 SAG 9, Allerta. Conti: 10+8+1 = 19; 8×5,5 + 16 = 60; guerriero 8 +6/+2/+2 → +8/+3/+1; Ascoltare/Osservare −1 + 2 (Allerta) = +1 | confermato (il rilievo #4 sulla CA è già corretto nel master) | — |
| Sacerdote, adepto 7 | DEF-4:3651-3659 | 38 pf, CA 12, +3 (1d6), TS +4/+4/+7, 3/4/3 | conti corretti (7d6+14; adepto con Volontà buona; SAG 15 dà +1 al 1° e al 2°) | confermato (aritmetica; la tabella dell'adepto non l'ho aperta in rete) | — |
| Pattuglia, hobgoblin guerriero 4 | DEF-4:3731 | 30 pf, spada lunga +6 (1d8+3), TS +6/+2/+0, Ascoltare/Osservare −1 | HB + conti: 4×5,5 + 8 = 30; 4+1+1 = 6; +1+2 di Specializzazione = +3; SAG 9 senza Allerta = −1 | confermato | — |
| Worg | DEF-4:3727 | GS 2, 30 pf, CA 14, morso +7 (1d6+4), sbilanciare, Ascoltare e Osservare +6 | WO: 4d10+8 (30), CA 14, morso +7 (1d6+4), sbilanciare, Listen +6 Spot +6, GS 2 | confermato | — |
| Goblin | DEF-4:3728 | GS 1/3, Ascoltare e Osservare +2, scurovisione 18 m | GO: identico | confermato | — |
| **Wyvern** | DEF-4:3733 | «SRD: GS 6, 59 pf, CA 18, volare 18 m, pungiglione +10 (1d6+4 e veleno, Tempra CD 17, 2d6 COS), morso +8 (2d8+2)» | WY: tutto coincide, tranne «bite +8 melee (**2d8+4**)» | **discrepanza** (lieve) | **morso +8 (2d8+4)** |
| Durin Rocciadura | DEF-4:3664-3666 | Guerriero 6, TS Temp +8 Rifl +2 Vol +3, SAG 14 | conto: Volontà base del guerriero 6 = +2, SAG 14 = +2 → **+4** | **discrepanza (aritmetica, lieve)** | **Vol +4** (o SAG 12-13) |
| Pozioni e bacchette del banco | DEF-4:1154-1158, 3340-3341, 718 | CFL 50, CFM 300, *volare* 750 (LI 5), *invisibilità* 300 (LI 3) e 1.200 (LI 12, 4 = 4.800), bacchetta di CFL 750, CFG all'11° 6.600 per 4 | CMI: pozione = livello × LI × 50 mo; bacchetta = livello × LI × 750 mo | confermato | — |
| Pergamene | DEF-4:1022, 1029, 1231, 1234, 1436-1439 | *dissolvi* (druido 4°) al 9° = 900; *resistere* al 7° = 350; *silenzio* al 3° = 150; *identificare* 125 (perla da 100 inclusa); *rimuovi paralisi* 150; *rimuovi maledizione* 375 | CMI: pergamena = livello × LI × 25 mo; le componenti costose si sommano al prezzo | confermato | — |
| Servizi | DEF-4:1147-1148, 1236-1239, 1438-1439 | livello × LI × 10 mo; *silenzio* all'8° = 160 mo e 8 minuti; servizi al 9° = 180 e 270 mo | formula SRD dei servizi d'incantesimo (pagina *Goods and Services* non aperta); i conti sono coerenti con la formula | conti confermati, formula non verificata in rete | — |
| Bacchetta di CFM | DEF-3:1233 | 750 × 2 × 3 = 4.500 mo a 50 cariche; ~2.250 a 25 | CMI: identico | confermato | — |
| Consacrare | DEF-2:309-310 | −1 ai non morti su attacchi, danni e TS; +3 sacro allo scacciare | CON: identico. Se nell'area c'è un altare del dio, i valori raddoppiano (−2/+6) | confermato | facoltativo: dire se la Stanza della Corona conta come «altare di Moradin» (allora −2/+6) |
| Rinuncia al TS | DEF-2:455-458 | `⚠ Non SRD`: l'SRD lascia rinunciare al TS solo contro un incantesimo | ST: «A creature can voluntarily forego a saving throw and willingly accept a spell's result» | confermato (avvertenza giusta) | — |
| Conoscenze senza addestramento | DEF-2:339 | «Sapienza/Conoscenze CD 15» | KN: «Knowledge (Int; Trained Only)… Without actual training, you know only common knowledge (DC 10 or lower)» | confermata la regola che i rapporti citavano. Il master non attribuisce niente all'SRD: resta il rilievo aperto (DEV#11, PT#12) di una CD 15 che chi non ha gradi non può tentare | indicare l'abilità esatta (Conoscenze (storia) o (religione)) oppure una prova di INT/SAG |
| Valori delle Benedizioni | DEF-2:674-675 | *Resist Energy* 1.000 mo; *Endure Elements* ~500 mo | CMI: pozione = livello × LI × 50 → *resistere all'energia* LI 3 = 300 mo; *sopportare gli elementi* LI 1 = 50 mo | non è una discrepanza secondo la regola (valore di riferimento, non attribuito all'SRD; FIX lo lascia) | se si vuole il prezzo SRD: 300 mo (700 al 7°, resistenza 20) e 50 mo |
| Muro dietro il trono | DEF-2:1042 | durezza 8, 360 pf per 3 m, Spezzare CD 35 | DUN: muratura 30 cm 90 pf CD 35; muratura rinforzata 30 cm 180 pf CD 45; pietra lavorata 90 cm 540 pf CD 50 (pf per sezione di 3 × 3 m); nessuna riga dà 360 pf con CD 35 | nessuna riga SRD corrispondente; il master non lo attribuisce all'SRD (geometria «invariata da ARC-06») | se si vuole SRD: pietra lavorata, 540 pf, CD 50 (o muratura, 90 pf, CD 35) |
| Slot del druido di 12° | DEF-3:1340-1341 | 6/5+2/4+1/4+1/3+1/3+1/2 (base SRD più i bonus di SAG 20) | DRU: 12° = 6/5/4/4/3/3/2. Bonus di SAG +5: 2/1/1/1/1 dal 1° al 5° (tabella dei bonus non aperta in rete) | confermato | — |
| CA e BAB di Hella | DEF-3:1310-1312 | CA 20 (+5 cuoio borchiato +2, +2 scudo +1, +3 nat), contatto 10, +10/+11, Vel 6 m | ARM: cuoio borchiato +3, scudo leggero +1; conti: 10+5+2+3 = 20; ranger 1 + druido 12 = +1 + 9 = +10 (DRU: BAB del 12° +9) | confermato | — |
| Livelli negativi | DEF-3:1156-1159 | segue l'SRD, ma dopo 24 ore niente TS e niente perdita di livello (regola del rito); si toglie con *ristorare* | ED: dopo 24 ore TS Tempra (CD 10 + ½ DV + CAR); se fallisce, il livello negativo sparisce e il livello scende di uno; si toglie con un incantesimo come *ristorare* | confermato (la divergenza è dichiarata) | — |
| *Rianimare morti* in 3.5 e in PF1e | DEF-3:166-169; DEF-2:846 | 3.5: perde un livello; PF1e: due livelli negativi permanenti; l'anima deve essere libera di tornare | RD: «loses one level (or 1 Hit Die)»; «the subject's soul must be free and willing to return»; PF1e: «gains two permanent negative levels» | confermato | — |
| Treant di Adamantio | DEF-3:1371-1420; DEF-4:3732; DEF-5:305 | base Treant SRD (Enorme, 7 DV, FOR 29, DES 8, COS 21, INT 12, SAG 16, CAR 12, +8, Attacco Poderoso, Spezzare Migliorato, Volontà di Ferro); 10 DV, TS +12/+3/+8, Lotta +20, CA 24, Travolgere 2d8+13 CD 24; `⚠ Non SRD` per FOR, +15 nat, 2d8, RD 10/adamantio, +18 | TR: Enorme 7d8+35 (66), CA 20 (−2, −1 DES, +13 nat), +5/+22, schianto +12 (2d6+9), Travolgere 2d6+13 CD 22, RD 10/tagliente, TS +10/+1/+7, talenti e abilità come nel master, GS 8; ADV (tabella delle taglie): da Enorme a Grande FOR −8, DES +2, COS −4, nat −3 | confermato (conti giusti, divergenze dichiarate; l'avvertenza «l'SRD darebbe FOR 21 e +10» è corretta) | — |
| Avatar della Radice | DEF-3:1435-1467 | CA 21 (−2, +13 nat), contatto 8, +10/+23, schianto +13 (2d6+5), Travolgere 2d6+7 CD 21, Vel 9 m | TR: schianti 2d6, portata 15 ft, +13 nat, 30 ft; conti: 10−2+13 = 21; 10+8+5 = 23; 10+5−2 = 13; 10 + 6 + 5 = 21 | confermato | — |
| Orco SRD | DEF-5:418-423; 99 | guerriero 1, GS ½, 5 pf, CA 13 (contatto 10, colto 13), falchion +4 (2d4+4/18-20), giavellotto +1 (1d6+3), TS +3/+0/−2, scurovisione 18 m, sensibilità alla luce | OR: identico; la sensibilità alla luce agisce «in bright sunlight or within the radius of a daylight spell» (quindi la luce della caverna non li abbaglia, come dice il master) | confermato | — |
| Hobgoblin sergente | DEF-5:431-436 | guerriero 5: 37 pf, CA 21, spada lunga perfetta +9 (1d8+4), arco +6, TS +6/+2/+1 | scheda del Bestiario `hobgoblin-sergente-cr5.md` (FOR 14 DES 12 COS 14 SAG 10) + HB + ARM: 5d10+10 = 37; 10+8+2+1 = 21; 5+2+1+1 = 9; 2+2 = +4; Vol 1+0 = +1 | confermato. Il «+1 morale entro 3 m» non è SRD, ma viene dalla scheda del Bestiario | — |
| Corsa ×3 in armatura pesante | DEF-5:471-472 | 18 m a round in armatura pesante, senza la DES alla CA | ARM: «When running in heavy armor, you move only triple your speed»; velocità 20 ft in armatura pesante → 60 ft = 18 m | confermato | — |
| Scudo pesante e arco | DEF-5:438-439 | con lo scudo pesante al braccio l'arco lungo non si usa (SRD) | ARM: «A heavy shield is so heavy that you can't use your shield hand for anything else» | confermato | — |
| Gittata di *comando* | DEF-5:302 | gittata vicina, 16,5 m al 13° | CMD: «25 feet… increases by 5 feet for every two full caster levels» → 25 + 30 = 55 ft = 16,5 m; *comando* 1 round, Volontà nega; «Fall» e «Flee» come nel master | confermato | — |
| *Ristorare*, *ristorare inferiore*, *guarigione* | DEF-5:478-483, 545 | *ristorare inferiore* porta da esausto ad affaticato; *ristorare* e *guarigione* tolgono l'esausto; 3 round per i due *ristorare*, azione standard per *guarigione*; *ristorare* da chierico, UOM CD 27; *ristorare inferiore* anche da druido | RES: *ristorare inferiore* Chr 2 Drd 2 Pal 1, 3 round, toglie l'affaticamento e porta l'esausto ad affaticato; *ristorare* Chr 4 Pal 4, toglie fatica ed esaurimento, dissolve i livelli negativi. HEA: azione standard, toglie «exhausted» e «fatigued». CD UOM 20 + LI (7° minimo per un 4° di chierico) = 27 | confermato | — |
| *Mente vuota* contro le Presenze | DEF-4:2289-2292 | per l'SRD le Presenze sono effetti di paura che influenzano la mente, e *mente vuota* protegge da tutti | MB: «protects against all mind-affecting spells and effects». Il testo SRD della Presenza Terrificante (DR) non dice che è «mind-affecting» | *mente vuota* confermata; la classificazione della Presenza come effetto mentale non si trova nel testo SRD del drago | facoltativo: marcarla `[CANONE — DM]` (è anche la lettura comune) |

## Riassunto delle discrepanze

1. **DEF-1:669-673 (e r. 152): Xorn standard.** È presentato come lo Xorn medio dell'SRD, ma ha 7d8+21 (52 pf), COS 17, morso +9, artigli +4 e Tempra +8. La pagina dice 7d8+17 (48 pf), COS 15, morso +10, artigli +8, Tempra +7.
2. **DEF-1:657: Fauci di Diamante, portata.** Il master dice 1,5 m, l'SRD dà 10 ft (3 m) allo Xorn anziano Grande. Due difetti minori: «mai colto in fallo» non c'è nell'SRD, e manca un talento (a 21 DV sono otto più Incalzare bonus).
3. **DEF-1:699: Fauci di Diamante nella regia.** Il morso è a +22 e lo Spaccare a +26, mentre lo statblocco dello stesso master dice +29 e +33.
4. **DEF-1:1592: Terros, CA.** Con DES 8 il conto dà 25, contatto 7 e colto 25, non 26/8/26.
5. **DEF-1:1589-1598: Terros sotto la base SRD.** È un «anziano avanzato a 30 DV», ma ha FOR 31 e velocità 6 m. L'anziano SRD a 24 DV ha già FOR 33, 9 m e schianto 2d10+11. Il blocco non ha né un `⚠ Non SRD` né un Boost log.
6. **DEF-4:3571: Skullcrusher Vecchio, raggio della Presenza.** Il master dice 63 m. Per il Vecchio (categoria 8) sono 72 m.
7. **DEF-4:3572: Skullcrusher Vecchio, *oscurità*.** Il master rimanda ad A.1, che dice 21 m. Per il Vecchio sono 24 m.
8. **DEF-4:3733: Wyvern.** Il morso è 2d8+2 nel master e 2d8+4 nella pagina SRD.
9. **DEF-4:3664: Durin.** Volontà +3 con SAG 14 su un guerriero di 6°: il conto dà +4.

Da segnalare, anche se non sono discrepanze secondo la regola del DM: il dubbio del playtester sull'armatura naturale +23 del drago **cade** (21 + 2 del template); il rilievo #1 del developer di DEF-4 (Colpo Devastante sul Treant) è confermato dall'SRD ed è già corretto nel master; *Consacrare* raddoppia (−2/+6) se l'area ha un altare del dio.

## Voci che nessuna pagina raggiungibile ha permesso di verificare

- Tabella PX del DMG (5.850 / 7.800 / 12.600): non è nell'SRD.
- Formula dei servizi d'incantesimo (livello × LI × 10 mo), pagina *Goods and Services*: i conti tornano con la formula, ma la pagina non si è aperta.
- Tabella dei bonus agli incantesimi per caratteristica alta (SAG 20 → 2/1/1/1/1) e tabella degli incantesimi dell'adepto.
- Tratti del tipo Elementale (immunità; nessuna immunità all'effetto mentale): la pagina `SRD:Elemental_Type` si è aperta senza la lista.
- Che la Presenza Terrificante sia un effetto mentale: il testo SRD del drago non lo dice.
- Mithral (una categoria più leggera, DES massima +2): la pagina dei materiali speciali non si è aperta.
- Regola del passo furtivo a metà velocità (Muoversi Silenziosamente e Nascondersi), Intimidire contrapposto e la condizione *scosso*: non cercate per limiti di richieste. Le scelte del master qui sono comunque `[CANONE]` o regole della casa.
- Salto deliberato (CD 15 per evitare i primi 3 m), copertura morbida +4 contro gli attacchi a distanza, bonus morali che non si sommano, creatura in panico messa all'angolo, parlare come azione gratuita.
- Incantesimi di DEF-4 (*epurare invisibilità*, *glifo di interdizione*, *barriera di lame*, *slay living*, *comando superiore*, *volare*, *silenzio*, *resistere all'energia*, *tentacoli neri* con presa +21): ricontrollati solo per aritmetica sulle formule, senza aprire le pagine.
- Pagine che hanno dato errore o limite di richieste: `SRD:Condition_Summary`, `SRD:Treant`, `SRD:Consecrate`, `SRD:Dungeons`, `SRD:Restoration`, `SRD:Knowledge`, `SRD:Knowledge_Skill`, `SRD:Iron_Golem` (fandom); `Wyvern`, `Worg`, `Knowledge` (birthright, 429); `hobgoblin.html`, `skillsII.html` (rpgcrossing). Per tutte, tranne quelle dell'elenco qui sopra, ho trovato un altro mirror.
- Non SRD, quindi non verificabili su nessuna pagina: mezzo-ogre, golem di mithral (Sentinella), Runecaster, Dream Dwarf, *Ira Extra*, gli artefatti.
