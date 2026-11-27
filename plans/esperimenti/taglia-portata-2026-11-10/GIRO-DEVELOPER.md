# Giro "developer" — taglia, spazio, portata nelle 205 schede

Data: 2026-11-10. Sola lettura sul repo: nessun file modificato.
Metodo: estratti tutti i 205 blocchi ```statblocco (148 file); controllate una per una le 59 schede non Medie (55 Grandi o più, 4 Piccole); lette tipo/razza/attacchi delle 146 Medie; cercate le armi con portata nei blocchi e nella prosa degli stessi file; grep di coerenza nei master ARC07.

## 1. Righe da correggere o da far decidere al DM

| file | creatura | campo | scritto | dovrebbe essere | fonte | certezza |
|---|---|---|---|---|---|---|
| `10-stand-alone/Il Giardino di Sale e Calce PF1e/appendice_creature.md` (blocco r. 7) | Karkator, aboleth mezzo-immondo gigante (PF1e) | `portata:` | 4,5 m | **6 m**. L'aboleth PF1e è Enorme con Space 15 ft./Reach 15 ft. (portata "alta", non "lunga" come nel 3.5); l'archetipo gigante alza solo la taglia, quindi Mastodontico alto = 20 ft. La prosa dello stesso file (r. 30) dice già «spazio 6 m, portata 6 m»: il blocco la contraddice. La versione 3.5 (4,5 m) è giusta e non va toccata. | https://aonprd.com/MonsterDisplay.aspx?ItemName=Aboleth ; https://aonprd.com/MonsterTemplates.aspx?ItemName=Giant | alta |
| `Bestiario/mostri/gnoll-hyenodon-rider-cr4.md` | Gnoll Hyenodon Rider | `portata:` | 1,5 m | **1,5 m (3 m con la lancia da cavaliere, e allora non i quadretti adiacenti)**. L'unico attacco in mischia è la «lancia da carica» (lance): in 3.5 ha portata e non colpisce gli adiacenti. Lo script non ha riconosciuto il nome «lancia da carica». | https://www.d20srd.org/srd/equipment/weapons.htm (Lance) | alta |
| `Bestiario/mostri/gnoll-hyenodon-rider-cr4.md` | idem, in sella | `spazio:` | 1,5 m | Da decidere: il blocco descrive il cavaliere (Medio, 1,5 m è giusto a piedi), ma in sella occupa lo spazio della cavalcatura. Se l'ienodonte è Grande, sulla griglia sono 3 m. La taglia dell'ienodonte non è scritta nella scheda. | SRD 3.5, Mounted Combat (regola a memoria, non riaperta); taglia dell'ienodonte NON verificata (non è SRD; in PF1e lo hyaenodon è Grande) | media (regola) / bassa (taglia ienodonte) |
| `Bestiario/mostri/thayan-knight-cr8.md` | Thayan Knight | `portata:` | 1,5 m | **1,5 m (3 m con la lancia da cavaliere, e allora non i quadretti adiacenti)**. L'attacco è solo in prosa (r. 20: «+1 lance +13/+8»), il blocco non ha `attacchi:` e lo script non l'ha visto. In sella al cavallo da guerra pesante (Grande) lo spazio sulla griglia è 3 m: stessa nota del gnoll. | https://www.d20srd.org/srd/equipment/weapons.htm (Lance) | alta (arma) / media (spazio in sella) |
| `Bestiario/png/Lirien/Lirien.md` | Lirien Amaranti (scheda PF1e trascritta) | `portata:` | 1,5 m | Il campo è difendibile (la frusta non minaccia), ma manca la nota: **1,5 m (4,5 m con la frusta, anche adiacenti; con la frusta non minaccia)**. Inoltre la prosa dice «portata 10 ft» (r. 28) e «tiene la distanza con la frusta, a 3 m» (r. 152): la frusta ha portata 15 ft = 4,5 m sia in PF1e sia in 3.5. La build è «trascritta dalla scheda del giocatore» e CANONIZZATA DAL DM (2026-07-20): decide il DM se correggere 10 ft → 15 ft. | https://aonprd.com/EquipmentWeaponsDisplay.aspx?ItemName=Whip ; https://www.d20srd.org/srd/equipment/weapons.htm (Whip) | alta (regola); decisione al DM |
| `Bestiario/villain/beholder-death-tyrant-cr14.md` (prosa r. 42) | Beholder death tyrant mezzo-illithid | prosa «Spazio 3 m, portata 3 m (4,5 m coi tentacoli)» contro `portata: 1,5 m` del blocco | due valori diversi nello stesso file | Il **blocco è giusto** per la fonte (1,5 m): la copia realmshelps nel repo (`03_la Cittadella/_testi-altrui/realms-helps-creature-beholder-death-tyrant.md` r. 53) dà «Space: 10 ft./5 ft.», come il beholder del Manuale dei Mostri. Va corretta la prosa, oppure il DM conferma che i tentacoli da illithid arrivano più lontano e allora va corretto il blocco. Nessun marcatore CANONE sulla portata; non so da dove venga il «3 m / 4,5 m». Il beholder non è nell'SRD (pagina d20srd 404). | copia realmshelps nel repo; Monster Manual 3.5 (a memoria) | alta (il conflitto), media (quale dei due vince) |
| `Bestiario/mostri/hobgoblin-captain-cr8.md` | Hobgoblin Captain | `portata:` | 1,5 m | Da decidere: fra le voci c'è «Armatura completa +2, lancia pesante» (heavy lance), ma l'attacco scritto è la spada lunga. Se la lancia si usa, serve la nota «(3 m con la lancia da cavaliere, e allora non i quadretti adiacenti)» e una cavalcatura; se è solo colore, niente. | https://www.d20srd.org/srd/equipment/weapons.htm (Lance) | bassa |
| `Bestiario/mostri/drow-priestess9-cr11.md` | Drow Priestess of Lolth 9 | `portata:` | 1,5 m | Da decidere: l'attacco (solo in prosa, r. 24) è «+1 snake-headed whip/scourge +8/+3 (1d4+2 + veleno)». Se è una *frusta* a tutti gli effetti: 4,5 m senza minacciare. Se è il flagello a teste di serpente dei Reami (scourge), che io ricordo senza portata: 1,5 m va bene. La scheda non sceglie. | SRD Whip (URL sopra); flagello delle sacerdotesse: fonte Forgotten Realms, non verificata | bassa |
| `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md` (blocco r. 1563) | Sentinella Silenziosa (Golem di Mithral) | `taglia:`/`spazio:`/`portata:` | Grande, 3 m, 3 m | Solo segnalazione: il golem di mithral ufficiale (SRD epico) è **Enorme, 15 ft./15 ft.** Qui è un mostro del modulo (18 DV, «Grande, veloce e fluido», pf «del modulo»), quindi quasi certamente voluto; non c'è però un marcatore CANONE sulla taglia. Internamente coerente (−1 taglia in CA, Lotta +25 = 13+8+4). | https://www.d20srd.org/srd/epic/monsters/golem.htm | alta (il dato SRD), bassa (che sia un errore) |

## 2. Differenze dall'ufficiale già decise dal DM (non errori, nessuna azione)

- **Treant di Adamantio** (3 blocchi: `ARC07-DEF-3` r. 1550, `ARC07-DEF-4` r. 4416, `homebrew/.../09-SCHEDA-HELLA-RISORTA.md` r. 69): Grande 3 m/3 m; il treant SRD è Enorme 15 ft./15 ft. Il testo dice «tenuto **Grande** come nel canone» con `[CANONE — DM 2026-10-18]`. Coerente con la prosa («Spazio 3 m, portata 3 m», «entro 3 m»).
- **Azarr Kul** (`azarr-kul-final-cr17.md`): blocco Medio; col pre-buff (*giusto potere*) diventa Grande, portata 3 m, ed è già scritto in prosa (r. 51) e nella voce del blocco. Va bene così.
- **Hella, Avatar della Radice**: Enorme 4,5/4,5 m come il treant SRD; salto di due taglie dichiarato «Non SRD». Coerente.

## 3. Draghi: taglia contro età (tutte coerenti)

Tabella SRD verificata online (https://www.d20srd.org/srd/monsters/dragonTrue.htm): Enorme = 15 ft./10 ft. (15 ft. col morso) → «4,5 m, 3 m (4,5 m con il morso)» giusto.

| scheda | età dichiarata | taglia SRD per quell'età | scritto | esito |
|---|---|---|---|---|
| Skullcrusher il Nero (DEF-4 r. 4020) | nero adulto maturo, avanzato | Enorme (il nero è Grande fino ad adulto, Enorme da adulto maturo ad antico) | Enorme | ok |
| Skullcrusher Vecchio (DEF-4 r. 4105; copia in `02-CHI-CE-STANOTTE.md`) | nero vecchio | Enorme | Enorme | ok |
| Tyrgarun | blu vecchio | Enorme (blu: Enorme da adulto a molto vecchio) | Enorme | ok |
| Ozyrrandion | verde adulto, avanzato a 22 DV (Boost log: da giovane ad adulto) | Enorme (verde: Enorme da adulto) | Enorme | ok |
| Arbitrax | rosso giovane adulto, 19 DV | Enorme (rosso: Enorme da giovane adulto) | Enorme | ok |
| Avatar di Tiamat | esterno Enorme (non un drago per età) | — | Enorme, portata da drago | coerente con la sua prosa; originale RHoD non verificato |
| Wyvern (2) (DEF-4 e copia) | wyvern SRD | Grande 10 ft./5 ft. | Grande 3 m/1,5 m | ok |

## 4. Coerenza interna dei master ARC07 (punto 4)

Grep di «portata / arriva a / quadrett» su `ARC07-DEF-1…5` e `ARC07-BARILE-SULLA-TENDA.md`: **nessuna frase contraddice i nuovi campi.** Frasi controllate: DEF-1 r. 780 (Xorn élite «Spazio 3 m, portata 3 m»), r. 1730 e mappa r. 3060 (Terros «3×3 quadretti, Enorme, spazio 4,5 m»), r. 1899 («Portata 4,5 m»); DEF-3 r. 1102 (Avatar «portata 4,5 m»), r. 1574/1584 (Treant «portata 3 m», «entro 3 m»), r. 1633; DEF-4 r. 3104 («Zog'tar è Grande e arriva a 3 m»), r. 3507 («Il morso ha portata 4,5 m»), r. 4043 («Spazio 4,5 m, portata 3 m (morso 4,5 m)»). Il BARILE parla solo di quadretti di deviazione e d'olio, non di portate.

## 5. Armi con portata (punto 3)

- Già giuste: `monaco-pugno-del-destino-cr7.md` (catena chiodata 3.5: 3 m, anche adiacenti); `chierico-gruumsh-cr11.md` (picca lunga/longspear: 3 m, non adiacenti); «Asservito armato» 3.5 (lancia lunga); «Miliziano della Torre» PF1e (lancia lunga: in PF1e la regola è la stessa del 3.5).
- PF1e: «Asservito armato» PF1e ha la lancia corta (niente portata, giusto); tridente (Tariq, Skum) non ha portata in nessuno dei due sistemi; nessuna catena chiodata né alabarda nelle schede PF1e. Nessun errore di regola PF1e tranne Karkator (tabella) e la frusta di Lirien.
- Mancanti: le tre lance da cavaliere e le due fruste della tabella al §1.
- Nessuna alabarda, falcione, guisarme, ranseur, picca vera e propria nelle righe d'attacco delle 205 schede (l'«alabarda» compare solo in un testo di colore del Collezionista).
- Nota generale, non un errore: i cavalieri (gnoll, Thayan Knight, fantini del Palio, goblin worg raider) hanno il blocco del solo cavaliere; in sella lo spazio è quello della cavalcatura. Il goblin sul worg Medio resta a 1,5 m; cavallo e (forse) ienodonte portano a 3 m.

## 6. Cose che NON ho potuto verificare su una fonte

- **Razorfiend** rosso/blu/verde/bianco (Grande 3 m/3 m) e **Blackspawn Alfa** (Enorme 4,5/4,5): non SRD. A memoria il greenspawn razorfiend (Red Hand of Doom / Monster Manual IV) è Grande con Space 10 ft., Reach 10 ft., quindi la portata «alta» è giusta e l'Alfa Enorme a 4,5 m ne segue. Certezza media, nessuna fonte aperta. Le schede non scrivono Space/Reach in prosa.
- **Lucertola del tuono** (Grande 3 m/1,5 m): ricostruita dal DM, la prosa dice già «Spazio 3 m; Portata 1,5 m» (coerente). L'originale della web enhancement di RHoD non l'ho potuto leggere.
- **Loxo** (Grande 3 m/3 m): Monster Manual II 3.0, a memoria Face/Reach 5×5/10 ft. → portata alta giusta. Certezza media.
- **Bone naga** (Grande 3 m/1,5 m): Monster Manual II; allineata ai naga SRD 3.5 (10 ft./5 ft., verificati). Certezza media.
- **Myconid sovereign** (Grande 3 m/3 m), lavoratore Piccolo, guardie Medie: trascrizione homebrew, bipedi; plausibile, non verificato.
- **Beholder, mind flayer, githyanki**: non sono nell'SRD; taglie a memoria dal Manuale dei Mostri (beholder Grande 10/5; illithid e githyanki Medi).
- **Leone crudele, orso bruno, cavallo, gufo gigante celestiale**: gufo gigante verificato (Grande 10/5); gli altri a memoria (Grandi 10/5), le pagine d20srd che ho provato hanno dato 404 o tabella vuota.
- **Krusk** (mezzorco con archetipo gigante PF1e → Grande 3/3), **Bruto deforme** (gigante di pietra + gigante PF1e → Enorme 4,5/4,5), **Zog'tar** (mezzo-ogre Grande 3/3), **Wyrmlord Karruk** (gigante delle colline, Grande 3/3): coerenti con base SRD (giganti 10/10 verificati) più una taglia; il mezzo-ogre non è SRD (a memoria Grande 10/10).

## 7. Verificate online e giuste

Wyvern, treant, aboleth 3.5 (Enorme 15/10; 17-24 DV Mastodontico → 6 m/4,5 m giusto), chuul 3.5 (17 DV → Enorme 15/10) e PF1e (Grande 10/5), ragno fase 3.5 (9-15 DV Enorme) e PF1e (Grande 10/5 → gigante Enorme 15/10), bebilith e retriever (Enormi 15/10), xorn (medio 5/5; anziano Grande 10/10, 16-21 DV resta Grande), elementale della terra anziano (Enorme 15/15, 25-48 DV Enorme), ogre e ogre mage (10/10), centauro (10/5), minotauro (10/10), gigante delle colline e di pietra (10/10), megere (annis Grande 10/10; verde e marina Medie), worg (5-6 DV Medio: il worg a 6 DV è giusto Medio), gufo gigante, draghi neri/blu/verdi/rossi per età, regole delle armi con portata 3.5, frusta PF1e, archetipo gigante PF1e.

Schede Medie e Piccole (146 + 4): nessuna taglia sospetta. Le 9 «senza indizi» sono tutte Medie davvero: druido del Cerchio (umanoide), comandante del Teschio Nero (umano di Thay), Lirien (mezzelfo), Azarr Kul (hobgoblin mezzo-drago, Medio), Ghostlord (mezz'elfo lich), Salvatore (umano), Sethrax e Xal'thor (illithid Medi), Sonjak (drow). Goblin e blue sono Piccoli; nessun gigante, ogre, troll, golem o animale grande è dichiarato Medio. Il «Servitore della Spora» (umanoide fungino, Medio) non ha altri dati nel file: lasciato com'è.

## Conteggio

- **Verificate: 205 schede su 205** lette (59 non Medie una per una, di cui 36 con creatura base confermata su fonte online, le altre a memoria o homebrew; 146 Medie su tipo, razza e attacchi).
- **Giuste: 198.** Da correggere 4 (Karkator PF1e, gnoll hyenodon rider, Thayan Knight, nota frusta di Lirien); da far decidere al DM 3 (hobgoblin captain, drow priestess, golem di mithral). In più una prosa da allineare al blocco (beholder death tyrant) e la prosa «10 ft / 3 m» della frusta di Lirien.

## Decisione del DM (2026-11-10)

Jfs sceglie «SRD sui tre testi, il resto tuo». Beholder tiranno della morte: la prosa segue il blocco e la fonte (portata 1,5 m). Capitano hobgoblin: 3 m con la lancia da cavaliere. Sacerdotessa drow: la frusta è una frusta dell'SRD (4,5 m, non minaccia). Il golem Sentinella resta Grande e i cavalieri in sella tengono lo spazio scritto dal DM.

Stessa sera Jfs corregge: «metti tutte standard SRD». La frusta non minaccia; il cavaliere senza lancia minaccia a 1,5 m. Quindi anche: Sentinella Silenziosa Enorme (4,5 m, 3×3 quadretti, portata 4,5 m), con i numeri che la taglia trascina: CA 29 (contatto 10, colto 27), schianti +19, Lotta +29, Overdrive CA 23, +40 pf da costrutto Enorme (i 160 pf restano del modulo). Cavalieri (gnoll sull'ienodonte, cavaliere di Thay): in sella occupano i 3 m della cavalcatura Grande. Non verificato: la taglia dell'ienodonte (non SRD; Grande in PF1e).
