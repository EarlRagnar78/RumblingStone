# Regole complete: inventario di ciò che i plugin hanno e di ciò che la misura non guardava

Richiesta del DM del 2026-11-10: verificare che le regole PF1e siano complete e, dove
non lo sono, completarle come per il 3.5; lo stesso per d20 SRD e 3.5. Si parte da
main f65d78e e dalla misura di ADR-0121.

**Perché un inventario.** «217/217» del PF1e e «605/606» del 3.5 dicono che le righe
*misurate* sono giuste. Non dicono che le regole ci sono tutte. Qui si elencano tutte
le parti di regola che un plugin (`sistemi/*/sistema.toml`) dichiara o che uno strumento
usa, e per ognuna se è misurata contro la fonte.

Fonti: SRD 3.5 `olimot/srd-v3.5-md@c7f30a0c`, PRD `PSRD-Data@76ea4784` (cache di
`riscontro_srd.py`). Misura nuova: `misura_regole_complete.py` (stessa forma di
`misura_plugin_regole.py`). Prima e dopo: `MISURA-PRIMA.md`, `MISURA-DOPO.md`.

## 1. Che cosa c'è e chi lo misura

| Parte di regola | 3.5 | PF1e | d20 | Misura prima di oggi | Misura da oggi |
|---|---|---|---|---|---|
| Tipi di creatura, taglie | ✓ | ✓ | — | ADR-0121 | invariata |
| Classi base, PNG, prestigio (DV, BAB, TS, gradi) | ✓ | ✓ (55) | — | ADR-0121 | invariata |
| Griglie, incantesimi conosciuti | ✓ | ✓ | — | ADR-0121 | invariata |
| Armature e scudi | ✓ | ✓ | — | ADR-0121 | invariata |
| Abilità (nomi) | ✓ | ✓ | — | ADR-0121 | invariata |
| Liste d'incantesimi classe × funzione (3.5) | ✓ | riusate | — | ADR-0121 contro SRD | **ora anche contro il PRD**, perché il plugin pf1e le riusa |
| Incantesimi «solo PF1e» (APG) | — | ✓ | — | nessuna | **nuova** |
| Liste di classe PF1e dal PRD | — | ✓ | — | ADR-0121 (uso) | invariata |
| Soglie PE | ✓ | ✓ (3 tracce) | — | solo 3.5 | **PF1e nuova** |
| PE per GS, difficoltà d'incontro | metodo | ✓ | — | nessuna | **PF1e nuova** |
| Tesoro per incontro | ✓ (`loot_tables.yaml`) | ✓ (3 velocità) | — | nessuna | **nuova, tutti e due** |
| Statistiche dei mostri per GS (Bestiary 1–1) | — | ✓ | — | nessuna | **nuova** |
| Formule (modificatore, TS, CD) | — | — | ✓ | nessuna | **modificatore nuova**; TS già dentro le classi |
| Talenti dei PNG generati | ✓ dal lotto 3 (`talenti.toml`, SRD) | ✓ dal lotto 3 (`talenti.toml`, PRD) | — | nessuna | **nuova (uso)**: numero per classe al 7° e prerequisiti |
| Nomi italiani di condizioni, talenti, incantesimi | lessico | lessico | — | ADR-0110 (termini) | **nuova: copertura contro la fonte** |
| Conformità delle schede | ✓ | ✓ (ADR-0119) | — | cancello | invariata |

## 2. Che cosa ha trovato la misura nuova

| Sistema | Tabella | Esito | Che cosa vuol dire |
|---|---|---|---|
| 3.5 | tesoro per livello d'incontro | 19/20 | EL 19 era 60.000 mo, l'SRD dice 61.000. **Corretto in questo lotto.** |
| 3.5 | talenti dei PNG generati | 0/5 (lotto 1); **11/11 dopo il lotto 3** | Un guerriero 7 ne aveva 1, la regola gliene dà 7. Ora tutte le 11 classi al 7° tornano col conto fatto a mano sul manuale. |
| PF1e | talenti dei PNG generati | 0/5 (lotto 1); **32/32 dopo il lotto 3** | Un fighter 7 ne aveva 1 su 8. Ora le 32 classi base, ibride e alternative al 7° tornano, e ogni talento generale ha i prerequisiti (32/32). |
| PF1e | liste 3.5 riusate dal pf1e | 445 giuste, 0 sbagliate, 181 non verificabili; **626/626 dopo il lotto 2** | I 181 erano nomi italiani fuori dal lessico. Portati al lessico, la misura ha visto *metamorfosi* (4° in 3.5, 5° in PF1e) e *cura ferite minori* (non esiste in PF1e): ora `[livello_pf1e]` nel plugin pf1e. |
| PF1e | «solo PF1e» | 54/55, 1 non verificabile | *Tamburi tonanti* (Thunderous Drums) non è nel PRD in cache: non si può dire se è giusto. |
| PF1e | PE, PE per GS, tesoro, statistiche per GS, modificatore | tutte giuste | 215 righe nuove misurate, nessun errore. |
| tutti | nomi italiani | 100% | Condizioni, talenti e incantesimi del Core hanno tutti un nome nel lessico. |

## 3. Il «talento firma» viola i prerequisiti

Il guerriero 7 generato ha «Sbilanciare Migliorato» con Int 8. Il talento chiede Int 13
e Maestria in Combattimento (PRD, Improved Trip; SRD uguale). Il generatore sceglie il
talento dal ruolo e non controlla i prerequisiti. Va nel lotto 3 insieme al numero.

**Chiuso dal lotto 3.** Il talento firma del carattere resta il primo da provare, ma
solo se il PNG lo può prendere; se non può, il generatore sceglie un altro carattere
dello stesso ruolo e lo scrive nel conto. Il numero viene dalla regola (generali per
livello, bonus e concessi di classe), i prerequisiti dal PRD e dall'SRD.

Che cosa il lotto 3 ha dovuto leggere oltre la tabella della classe: molti talenti
bonus il manuale li dà nel testo della capacità, non nella colonna «Special». Il
monaco riceve Colpo Senz'Armi Migliorato da «Unarmed Strike», il cavaliere un talento
di squadra da «Tactician», il cacciatore sceglie tra Tiro Preciso e Aggirare con
«Precise Companion», il ranger 3.5 è «trattato come se avesse» Tiro Rapido o
Combattere con Due Armi. Si leggono solo le capacità che ogni membro della classe
ha: i domini, i misteri, gli spiriti dello sciamano, i trucchi del ninja e i talenti
del ladro sono scelte, e restano fuori. I talenti mitici (Mythic Adventures) sono nei
dati ma il generatore non li prende mai: chiedono un grado mitico.

Che cosa resta, detto: il talento in più dell'umano (il generatore non sceglie la
razza); i talenti con prerequisiti di gradi d'abilità (saltati, non inventati: il
generatore non tiene i gradi); 4 talenti del Core PF1e e 1 SRD con prerequisiti che
la regola non sa leggere (Critical Mastery, Improved Familiar, Improvised Weapon
Mastery, Master Craftsman; restano fuori dalla scelta); battle herald e dragon
disciple hanno talenti bonus da una lista che il PRD non dà in forma leggibile
(ripiego sui generali, scritto nel conto).

## 3-bis. Trovato durante il lotto 3: i tratti dei tipi di creatura

Il generatore dà a ogni mostro i punteggi mentali del suo ruolo. Così una melma, un
parassita o un costrutto senza mente hanno Int 8 e quattro talenti, dove l'SRD e il
PRD dicono «nessun punteggio di Intelligenza» e quindi nessun talento. Nel 3.5 un
non morto e un costrutto escono con il bonus di Costituzione ai pf (10d12+40), che non
hanno: il non morto 3.5 non ha Costituzione, il costrutto prende il bonus fisso per
taglia. Il cancello `conformita_statblocchi` oggi non lo vede. Non è un difetto dei
talenti, è un tratto di tipo mancante: **lotto 5**, con la sua misura.

**Chiuso col lotto 5** (`MISURA-LOTTO5-PRIMA.md` / `-DOPO.md`): Cos «—» a non
morti e costrutti, Int «—» e niente talenti a melme, parassiti e costrutti,
pf bonus per taglia del costrutto dalla tabella dell'SRD, Tempra senza
Costituzione, Advanced che non dà pf a chi non ha Costituzione. Resta fuori,
detto: immunità, RD e scurovisione dei tipi non si aggiungono al blocco (sono
capacità speciali, il generatore non ne scrive), e un costrutto con mente
(«most constructs are mindless», non tutti) il generatore non lo fa.

Nello stesso lotto: pf bonus dei costrutti PF1e Fine e Diminutive, che il
rapporto di ADR-0121 dava come limite (nessuna scheda nel PRD). Ora vengono
dalla tabella «Construct Size» del PRD pubblicato (legacy.aonprd.com,
bestiary/creatureTypes.html): «—», cioè 0.

## 3-ter. Licenze

I dati del plugin PF1e prendono classi, talenti, razze e creature da 14 libri Paizo
(non solo Core, Bestiary e APG) e 5 creature del Tome of Horrors. `OGL.txt` dichiarava
6 voci: ora ne ha 25, col testo copiato dalla Sezione 15 del PRD. `LICENSES.md` §1 dice
le stesse fonti.

## 4. Residui già noti

| Residuo | Stato | Lotto |
|---|---|---|
| 181-185 nomi d'incantesimo 3.5 fuori dal lessico | **chiuso dal lotto 2**: 108 nomi (185 voci) portati al lessico; dietro i nomi c'erano 2 livelli sbagliati (*scudo della legge* 8° del chierico, *spaventare* 2° del bardo) | 2 |
| «scaglie» letta come armatura | **chiuso in questo lotto**: la chiave è «corazza a scaglie» (nome del lessico), test di regressione con un drago | 1 |
| costrutti minuti e piccolissimi senza pf bonus | nessuna scheda pubblicata li dà: resta dichiarato, non si inventa | — |
| sciamano senza incantesimi di livello 0 | **chiuso dal lotto 4**: il PRD le ha nel testo «0-Level Shaman Spells» (ACG), non nella tabella `spell_lists`; `estrai_prd_pf1e.py` ora legge le 17 orazioni da lì | 4 |
| prerequisiti delle classi di prestigio | **chiuso dal lotto 4**: i requisiti delle 18 classi letti dal PRD (`[requisiti]` in `talenti.toml`); il generatore controlla BAB, livello d'incantesimo arcano e divino e *channel energy* sulle classi messe prima, prende per primi i talenti richiesti e scrive nel conto ✓, ✗ e ciò che decide il DM (gradi, allineamento, imprese) | 4 |

## 5. Che cosa resta fuori, e perché

- **Testo delle regole** (benefici dei talenti, effetti delle condizioni, descrizioni degli
  incantesimi). Nessuno strumento lo legge; le skill rimandano alla fonte. Il lessico ha
  i nomi ufficiali, ed è quello che serve a `controlla_termini` (ADR-0110).
- **Oggetti magici e prezzi.** `magic_items_srd.yaml` ha 64 oggetti scelti a mano,
  non il catalogo. Da misurare se il DM vuole il generatore di tesori completo.
- **Equipaggiamento dei PNG 3.5.** Il generatore usa la colonna «heroic NPC» del PF1e anche
  in 3.5 (lo dice nel conto): la tabella 3.5 (DMG 4-23) non è nell'SRD.
- **Archetipi PF1e** (395 nel lessico): non servono al generatore di oggi.

## 6. Lotti

1. **Misura estesa e correzioni piccole** (questa PR): `misura_regole_complete.py`, EL 19,
   «corazza a scaglie».
2. **Nomi d'incantesimo 3.5** (fatto): 108 nomi di `incantesimi.toml` e dell'ancora
   `spells.md` portati al lessico ufficiale (ADR-0110); non verificabili da 181 a 0, 3.5
   da 605/606 a 790/791 nella misura di ADR-0121 (`MISURA-LOTTO2-PRIMA.md`, `-DOPO.md`).
3. **Talenti dei PNG** (fatto): numero per livello e classe (regola del manuale), scelti
   tra quelli di cui il PNG ha i prerequisiti (PRD e SRD); misura: 3.5 0/11 → 11/11,
   PF1e 0/32 → 32/32 (`MISURA-LOTTO3-PRIMA.md`, `MISURA-LOTTO3-DOPO.md`).
4. **Prestigio e sciamano** (fatto): requisiti d'accesso delle 18 classi di prestigio PF1e
   (letti 0/18 → 18/18; una via d'ingresso legale per classe, costruita a mano, 0/18 → 18/18);
   orazioni dello sciamano (`MISURA-LOTTO4-PRIMA.md`, `-DOPO.md`).
5. **Tratti dei tipi di creatura**: niente Int e niente talenti per i tipi senza mente,
   niente Costituzione per non morti e costrutti 3.5 (pf dal bonus del tipo); misura
   per tipo contro SRD e PRD, e il cancello che lo controlla.
