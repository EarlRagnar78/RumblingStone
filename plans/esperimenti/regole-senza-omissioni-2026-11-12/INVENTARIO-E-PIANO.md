# Regole senza omissioni: inventario del divario e piano (2026-11-12)

Richiesta del DM (2026-11-12, 07:54): completare le regole dei plugin con tutto
quello che le fonti hanno, sezione per sezione, senza omettere nulla; trovare
altri siti per il riscontro; stringere la tolleranza sui bonus; aggiungere la
variante della campagna Rumbling Stone (SRD d20 → D&D 3.5 → PF1e, risultato più
forte per villain, PNG e mostri); logica deterministica e senza ambiguità; il
verificatore non salta niente di ciò che una scheda scrive, tranne descrizione
e tattica. Poi MCP aggiornato, controllo finale, correzione delle schede.

Questo documento è la fase di audit. Non contiene codice nuovo.

## 0. Informazioni che mancano e assunzioni

Mancano (chieste con due schede di decisione nel thread):
1. Fin dove arriva «senza omettere nulla»: le 37 pagine di varianti di
   Unearthed Arcana, le 3 pagine homebrew del sito e i sottosistemi che nessuna
   scheda del repo usa oggi (incarnum, truenaming, pact, shadow magic).
2. Come si sceglie «il più forte» fra tre sistemi senza creare schede ibride.

Assunzioni con cui procedo finché non dici altro:
- A1. Dalle fonti non OGL entrano solo nomi e numeri (tua scelta del 12/11).
- A2. La variante della campagna vale per villain, PNG e mostri. I PG restano
  alle regole del tavolo e non vengono toccati.
- A3. «Più forte» non scavalca la regola del 9/11: il numero deve ricostruirsi
  da una scheda legale (ADR-0118).
- A4. Un bonus che la scheda non dichiara (oggetto, talento, capacità) è una
  violazione, non una tolleranza.

## 1. Stato di oggi, misurato

| Che cosa | Valore |
|---|---|
| Schede con blocco `statblocco` nel Bestiario | 134 |
| Violazioni aperte | 7 in 6 schede (al DM) |
| Numeri sbagliati messi apposta e visti | 701 su 1.278 (55%) |
| Tolleranza sui tiri salvezza 3.5 | fino a **+4** sopra l'atteso passa in silenzio |
| Tolleranza sull'attacco 3.5 | da −1 a +2 passa in silenzio |
| Punti ferita | qualunque valore fra il minimo e il massimo dei dadi passa |
| Conti dichiarati dal plugin 3.5 | 10 |
| Conti dichiarati dal plugin PF1e | 14 in prova (CA, BMC, TS, incantesimi, incanalare…) |

Prova fatta oggi togliendo la tolleranza a tiri salvezza e attacco, senza
altre modifiche: le schede 3.5 con uno scarto passano da **3 a 28 su 120**.
Sono 33 tiri salvezza più alti dell'atteso (23 di +1, 6 di +2, 1 di +3, e 3
più bassi di 1) e 6 attacchi (5 di +1, 1 di −1). Quasi tutti saranno oggetti
o talenti non dichiarati alla verifica (mantello della resistenza, Volontà di
Ferro): è esattamente ciò che il lotto 1 deve leggere prima di accendere la
tolleranza zero, altrimenti sono 28 falsi allarmi.

Le tre tolleranze sono il motivo principale del 55%: un +4 a un tiro salvezza
oggi non si vede. È il punto che hai indicato ed è corretto.

## 2. Che cosa scrive una scheda e che cosa si verifica

| Campo della scheda | Schede che lo hanno | 3.5 oggi | PF1e oggi |
|---|---|---|---|
| pf, dadi vita | 134 | fascia min-max | fascia |
| BAB, lotta / BMC | ~120 | sì | sì |
| Tiri salvezza | 134 | sì, con +4 di tolleranza | sì |
| Iniziativa | 86 | sì | sì |
| Attacco (bonus) | 88 | sì, da −1 a +2 | sì |
| **Danno** dell'attacco | 88 | **no** | **no** |
| **CA e dettaglio della CA** | 125 | **no** (solo nei master) | sì, in prova |
| **Velocità** | 107 | **no** | **no** |
| Talenti: prerequisiti | 55 + 45 | sì | sì |
| **Talenti: quanti ne spettano** | 100 | **no** | **no** |
| Abilità: gradi massimi e punti | 29 | sì | sì |
| **Abilità: modificatore totale** | 29 | **no** | **no** |
| Incantesimi: lista e livello | 174 righe | sì | sì |
| **Incantesimi al giorno e conosciuti** | ~20 | **no** | in parte |
| **CD degli incantesimi e delle capacità** | ~60 | solo nei master | in parte |
| **Resistenza agli incantesimi, RD, immunità** | ~30 | **no** | **no** |
| **Sensi** | 57 | solo scurovisione | sì |
| **Equipaggiamento: valore contro la ricchezza del livello** | 31 | **no** | **no** |
| **GS** dalla composizione | 134 | **no** | in parte |
| Linguaggi | 16 | no | no |
| Descrizione, tattiche | tutte | fuori (coerenza: PR #379) | fuori |

Dodici campi in grassetto non hanno nessun controllo. «Il verificatore non
salta niente» oggi non è vero per circa metà di quello che una scheda scrive.

## 3. Sezione per sezione: fonti contro plugin

### 3.1 D&D 3.5 (srd.dndtools.org, 616 pagine; PCGen; SRD in cache)

| Sezione del sito | Pagine | Nel plugin `dnd35` | Divario |
|---|---|---|---|
| classes | 337 | 658 classi: dado vita, BAB, TS, punti abilità; 19 con talenti concessi | **capacità di classe per livello**, **incantesimi al giorno** delle classi dei manuali, **avanzamento d'incantatore** delle classi di prestigio (PCGen lo ha: oltre 1.100 righe `ADD:SPELLCASTER`), **requisiti** delle classi di prestigio (PCGen: righe `PRE…`), abilità di classe |
| feats | 38 + 97 tabelle dei libri | 363 SRD + 2.193 dei manuali, prerequisiti | conto dei talenti per DV e classe; **effetto sui numeri** (Robustezza, Volontà di Ferro, Arma Focalizzata sono nel codice, gli altri no); difetti (flaws) |
| magic/spells | 27 | liste: 601 SRD + 3.969 dei manuali | scuola e descrittore (CD con Incantesimi Focalizzati, scuole proibite), **slot e conosciuti**, poteri dei domini, nomi italiani |
| magic/psionics | 18 | solo le liste PCGen (psion, wilder, psychic warrior) | punti potere al giorno, poteri conosciuti; l'SRD psionico è in cache e non è usato |
| magic/invocations | 8 | niente | invocazioni di warlock e dragonfire adept per grado |
| magic/bladeMagic (Tome of Battle) | 2 | solo le liste PCGen (swordsage, warblade, crusader) | manovre conosciute e pronte per livello |
| magic/truename, shadow, pact | 6 | niente | sottosistemi interi |
| monsters | 6 | 15 tipi, tratti dei tipi, taglie | **creature base** (dadi razziali, armatura naturale, caratteristiche: servono per «Ogre + Barbaro 6»), **archetipi** (template), avanzamento per taglia |
| races | 2 | 23 nomi | modificatori di caratteristica, **modificatore di livello**, bonus razziali alle abilità, velocità |
| equipment | 5 | 30 armature, 11 scudi | **armi** (dado di danno, critico), **oggetti magici** (prezzo, tipo di bonus), costi di creazione |
| skills | 4 | 38 nomi, caratteristica chiave, gradi | sinergie, penalità di armatura, skill tricks, usi epici |
| basic | 4 | niente | capacità di carico (cambia la velocità), divinità → domini e arma preferita |
| epic | 5 | talenti epici | progressioni oltre il 20°, incantesimi epici |
| environment | 2 | niente | nessuna scheda lo usa: resta dichiarato fuori |
| variant (Unearthed Arcana) | 37 | niente | gestalt, tratti, difetti, punti incantesimo, linee di sangue… |
| homebrew | 3 | niente | invenzioni del sito, non regole |
| tools | 9 | niente | calcolatrici, non regole |

Manca del tutto, e serve a più conti insieme: **la regola di cumulo dei bonus
per tipo** (potenziamento, deviazione, morale, schivare…). Senza quella non si
può dire se una CA o un tiro salvezza sono legali.

### 3.2 PF1e (PSRD-Data in cache, 18 libri; aonprd.com raggiungibile)

| Sezione di aonprd.com | Nel plugin `pf1e` | Divario |
|---|---|---|
| Feats | 1.227 | aonprd ne ha circa il triplo (tutti i libri) |
| Classes | 55 classi con griglie | archetipi (nessuno), capacità per livello |
| PrestigeClasses | requisiti di 18 | tutte le altre |
| Spells | 1.536 nomi, 22 liste | i libri fuori dai 18 in cache |
| Monsters | tipi, taglie, tabella per GS | creature base, archetipi |
| Races | 37 razze (PR #318) | tratti razziali alternativi |
| Traits | niente | tratti del personaggio |
| Equipment, MagicItems | 12 armature, 6 scudi, tesoro per incontro | armi, oggetti magici, ricchezza dei PNG |
| Mythic | solo le liste | regole mitiche |
| Deities | niente | domini e arma preferita |
| Afflictions | niente | veleni e malattie (CD) |

### 3.3 Siti per il riscontro

| Sito | Sistema | Raggiungibile dal container | Uso |
|---|---|---|---|
| srd.dndtools.org | 3.5 | sì | fonte, già usata |
| PCGen (BahamutDragon/pcgen su GitHub) | 3.5 e PF1e | sì | fonte, già usata |
| **realmshelps.net** | 3.5 (talenti, incantesimi, classi, mostri, divinità) | **sì** | **seconda fonte indipendente per i manuali** |
| **aonprd.com** | PF1e, tutti i libri, OGL | **sì** | **fonte completa PF1e** |
| legacy.aonprd.com | PF1e PRD | sì | già usata |
| d20srd.org | SRD 3.5 | no (403) | servirebbe aprirla nell'ambiente |
| dndtools.net, new.dndtools.org, dndtools.one, dnd.arkalseif.info | 3.5 tutti i manuali | no (rete chiusa) | da aprire nell'ambiente se li vuoi |
| d20pfsrd.com | PF1e | no (410) | non necessario con aonprd |
| golarion.altervista.org | PF1e in italiano | via Firecrawl | nomi italiani |

Valutazione: con realmshelps per il 3.5 e aonprd per il PF1e ogni dato dei
manuali può avere due fonti. Dove ne resta una sola, la voce va marcata
«fonte unica» e non può generare una violazione certa.

## 4. Decisioni proposte (forma ADR)

**D-A. Tolleranza zero con bonus dichiarati.**
Contesto: +4 ai TS e +2 all'attacco passano. Decisione: ogni numero = base
calcolata + bonus che la scheda dichiara (oggetto, talento, capacità, razza),
sommati con la regola di cumulo per tipo. Uno scarto non spiegato è una
violazione. Conseguenze: molte schede oggi «verdi» diventeranno rosse finché
non dichiarano i loro bonus; è lavoro di correzione, non un difetto del metodo.
Da rivedere se: più di un terzo delle schede resta non verificabile.

**D-B. Variante della campagna come opzione esplicita.** (decisa dal DM il 2026-11-12: per elemento intero)
Contesto: SRD → 3.5 → PF1e, il più forte per villain, PNG e mostri.
Decisione: un'opzione `--variante rumblingstone` (e parametro MCP) che per
ogni *elemento* (classe, talento, incantesimo, tipo di creatura) prova i
sistemi nell'ordine e tiene quello che dà il risultato più forte, **tutto
intero**: mai il dado vita di un sistema e i tiri salvezza dell'altro per la
stessa classe. La scelta si scrive sulla scheda («Barbaro: PF1e»).
Conseguenze: deterministico e ripetibile; una scheda ibrida per numero non
passa. Da rivedere se: vuoi il massimo numero per numero (vedi scheda 2).

**D-B-bis. Il motore di gioco si può vincolare** (DM, 2026-11-12, 08:03).
Contesto: la variante «più forte» non deve essere l'unico modo. Decisione: un
solo parametro, `--motore` nella riga di comando e `motore` negli strumenti MCP,
uguale per il costruttore delle schede e per il verificatore, con quattro
valori chiusi:

| Valore | Regole ammesse | Uso |
|---|---|---|
| `srd35` | solo l'SRD d20 3.5 | scheda pubblicabile sotto OGL |
| `dnd35` | SRD più i manuali 3.5 | tavolo 3.5 puro |
| `pf1e` | solo PF1e | moduli PF1e |
| `rumblingstone` | SRD → 3.5 → PF1e, il più forte per elemento intero | variante della campagna |

Con un motore vincolato, un talento, una classe o un incantesimo che esiste
solo in un altro sistema è una violazione (`motore.fuori`), non una voce
accettata «dalla fonte successiva». Il motore usato si scrive nell'uscita e,
per le schede generate, nella scheda. Il valore predefinito resta quello del
sistema dichiarato dal file, come oggi; la variante si accende solo chiedendola.
Conseguenze: oggi la cascata è cablata in `verifica_talenti.risolvi` (una
scheda 3.5 arriva fino ai talenti PF1e): va resa dipendente dal motore. Da
rivedere se: serve un quinto motore (per esempio 3.0 o PF1e solo manuale base).

**D-B-ter. Le forme ibride** (DM, 2026-11-12, 08:07).
Contesto: nella variante il più forte si sceglie di norma per elemento intero,
ma una scheda può mescolare regole di sistemi diversi (per esempio la griglia
PF1e del ranger in una scheda 3.5, già decisa il 9/11). Decisione: la forma
ibrida è lecita **solo** col motore `rumblingstone` e solo se sta nel registro
delle regole custom del DM (un file `ibride.toml` del plugin della variante, da creare: elemento,
sistema da cui viene, sistema della scheda, fonte, data della scelta). Il
verificatore su ogni ibrida fa due conti: l'elemento è legale nel suo sistema
d'origine, ed è coerente col resto della scheda (stesse grandezze: livello di
classe, DV, caratteristiche; nessun doppio conteggio con l'equivalente 3.5).
Un'ibrida non registrata è `ibrida.non_dichiarata` anche nella variante; con un
motore vincolato è `motore.fuori`. Conseguenze: le scelte ibride già prese
(livello incantatore −3, griglie PF1e di ranger/paladino/bardo, Called Shots
di ARC-08) vanno portate nel registro nel lotto 11. Da rivedere se: il registro
supera le poche decine di voci, segno che serve una regola generale.

**D-C. Ogni campo della scheda ha un esito.**
Decisione: per ogni campo della tabella §2 lo strumento dà «torna», «violazione»
o «non verificabile, perché». Un campo senza esito è un difetto dello
strumento, e un test lo impedisce. Conseguenze: il numero dei non verificabili
salirà molto all'inizio; è la misura onesta di ciò che oggi si salta.

**D-D. Due fonti per ogni dato dei manuali.**
Decisione: PCGen + sito per il 3.5, più realmshelps come terza; PSRD + aonprd
per il PF1e. Dove divergono vince la fonte più vicina al libro e la voce è
marcata. Conseguenze: più lavoro di estrazione, meno falsi allarmi.

## 5. Piano

### 5.1 Audit (questa fase, chiusa con questo documento)
Fatto: inventario delle sezioni, dei campi e delle tolleranze; siti raggiungibili.
Resta: scaricare realmshelps e aonprd e contare le voci vere (i «circa» di §3.2).

### 5.2 Sviluppo, in lotti (un lotto = dati + regola + misura prima/dopo)

| Lotto | Contenuto | Chiude |
|---|---|---|
| 1 | Cumulo dei bonus per tipo; oggetti magici con tipo di bonus e prezzo (SRD, poi manuali); bonus dichiarati letti dalla scheda | tolleranza TS e attacco a zero; CA 3.5 |
| 2 | Armi (dado, critico), danno; taglia sul danno | danno |
| 3 | Classi: avanzamento d'incantatore, slot e conosciuti, requisiti delle classi di prestigio, capacità che toccano i numeri | incantesimi al giorno, CD, le 7 violazioni rimaste rigiudicate |
| 4 | Conto dei talenti per DV e classe; effetti dei talenti sui numeri | talenti |
| 5 | Razze e creature base (dadi razziali, armatura naturale, MdL), archetipi | GS, mostri con classe |
| 6 | Abilità: modificatore totale, sinergie, penalità di armatura | abilità |
| 7 | RI, RD, immunità, sensi, velocità e carico, linguaggi | qualità speciali |
| 8 | Ricchezza per livello contro l'equipaggiamento | equipaggiamento |
| 9 | Psionici, invocazioni, manovre; poi gli altri sottosistemi secondo la scheda 1 | sottosistemi |
| 10 | PF1e da aonprd: talenti, archetipi, classi di prestigio, incantesimi, tratti | PF1e completo |
| 11 | Parametro `motore` (D-B-bis: srd35, dnd35, pf1e, rumblingstone), variante della campagna (D-B) e registro delle forme ibride (D-B-ter) nel costruttore e nel verificatore | motore vincolabile e variante |
| 12 | MCP: parametri nuovi, documentazione, controllo finale, correzione delle schede | chiusura |

Stima onesta: sono dodici lotti, ognuno della taglia di quelli fatti il 12/11
(da mezza giornata a una giornata di lavoro di thread). Non si chiude in una
sessione. L'ordine mette prima ciò che alza di più la misura del 55%.

### 5.3 Verifica

- Banco con errori messi apposta per ogni campo nuovo; obiettivo dichiarato:
  dal 55% ad almeno il 90% sui numeri, con il resto spiegato voce per voce.
- Riscontro a campione sui libri: 30 voci per lotto prese a caso, confrontate
  fra le due fonti.
- Prova di determinismo: la stessa scheda verificata due volte, e generata due
  volte con la variante, dà byte identici.
- Test «nessun campo senza esito» (D-C).
- Dopo ogni lotto: quante schede passano da verdi a rosse, elenco al DM.

## 6. Rischi

- **Volume**: il «senza omissioni» sui manuali 3.5 sono migliaia di voci da
  fonti non ufficiali. Il rischio è riempire il repo di dati sbagliati che
  sembrano regole. La doppia fonte lo riduce, non lo azzera.
- **Schede rosse**: a tolleranza zero una parte grande del Bestiario andrà
  corretta o dovrà dichiarare i suoi bonus. È voluto, ma è lavoro tuo di
  decisione dove il bonus non ha una fonte.
- **PR #378**: è verde e aspetta il merge. Questo programma va in PR nuove,
  una per lotto, dopo il merge; altrimenti la #378 non si chiude più.

## 7. Appendice: le 28 schede con scarti a tolleranza zero

Prova del 2026-11-12, solo tiri salvezza e attacco. Per ogni scheda ho cercato
nel testo un bonus che spieghi lo scarto (mantello della resistenza, Volontà
di Ferro, Tempra Possente, Riflessi Fulminei, grazia divina, bonus razziale).
In 20 schede su 28 il testo non dichiara niente che lo spieghi: lì lo scarto è
un errore di conto o un bonus mai scritto, e va deciso scheda per scheda.

| Scheda | Scarto | Spiegazione scritta nella scheda |
|---|---|---|
| cultista-rakshasa-cr3 | Vol +1 | nessuna |
| drow-assassina-lolth-cr10 | Temp +2, Vol +2 | solo «+2 razziale vs incantesimi», che è condizionale |
| drow-fighter3-cr4 | Vol +1 | nessuna |
| drow-noble-guard-cr5 | Vol +2 | nessuna |
| drow-priestess9-cr11 | Vol +1 | nessuna |
| drow-wizard7-cr8 | Vol +1 | nessuna |
| duergar-mago3-cr4 | Vol +1 | nessuna |
| githyanki-warrior3-cr4 | Vol +1 | nessuna |
| hobgoblin-regular-warrior3-cr2 | Temp +1, Rifl +1, Vol −1 | Volontà di Ferro (ma la Volontà è sotto) |
| hobgoblin-regular-warrior4-cr3 | Rifl +1 | Tempra Possente (non tocca i Riflessi) |
| hobgoblin-veterans-warrior6-cr5 | tutti +1 | nessuna |
| kulkorzhul-war-adept-cr7 | tutti +1 | nessuna |
| monaco-pugno-del-destino-cr7 | Rifl +1 | nessuna |
| myconid-elite-guard-cr5 | Vol +1 | nessuna |
| myconid-sovereign-cr7 | Temp −1, Rifl +1, Vol −1 | talenti dichiarati, conto che non torna |
| nano-mastro-artigliere-guerriero8-cr8 | attacco −1 | nessuna |
| orco-berserk-barbaro2-cr2 | Vol +2 | nessuna (forse l'ira scritta nel valore base) |
| razorfiend-blue-cr9, razorfiend-red-cr9 | Vol +2, Vol +1 | nessuna |
| teschio-nero-commander-cr10 | Rifl +1 | Iron Will (non tocca i Riflessi) |
| thayan-red-wizard7-cr9 | Rifl +1, Vol +2 | nessuna |
| underdark-dovil-runecaster-cr7 | attacco +1 | nessuna |
| khorn-ufficiale-hammerfist-cr8 | attacco +1 | nessuna |
| avarthel-druido-cr9 | Temp +1, Vol +1 | nessuna |
| cavalcatura-ariete-moradin-cr5 | Temp +3 | cavalcatura del paladino |
| dauth-commander-mercenari-nani-cr12 | attacco +1 | nessuna |
| rurik-gorunn-cr10 | attacco +1 | nessuna |
| minotauro-karkilan-cr5 | attacco +1 | nessuna |

Tre schede «tutti +1» (hobgoblin veterani, war adept) fanno pensare a un
mantello della resistenza +1 mai scritto: è il caso tipico che il lotto 1 deve
far dichiarare.

## 8. Coordinamento con gli altri thread (2026-11-12, chiesto dal DM)

- Ordine dei merge, confermato dal coordinatore: PR #378 per prima (testa
  9a657b94 ferma), poi una PR per lotto da questo thread, con il ramo ripartito
  da main dopo ogni merge. La #379 non tocca il manifest e può andare prima o
  dopo la #378.
- ADR: uno solo per il programma, con una sezione per lotto; numeri da prenotare
  in `plans/adr-prenotati.json` nella prima PR di lotto (primo libero dopo
  0125, verificare 0123). ADR separati solo per la tolleranza zero e per la
  variante della campagna, se servono.
- Thread della #379 (coerenza della storia): a lui la coerenza fra tattiche,
  descrizione e scheda (regola S8). Da `verifica_scheda` gli serve, in JSON per
  scheda: file; talenti (nome canonico, riga); incantesimi (nome canonico,
  livello, usi o slot, riga); capacità speciali (nome, riga); righe di inizio e
  fine di «Tattiche» e «Descrizione». Entra nel lotto 3 o 4. La sua eventuale
  promozione di S1, S5-S7 tocca il manifest: va in fila dopo i lotti.
- Thread #370 (standard del volume) e #371 (documentazione): avvisati dal
  coordinatore che 28 schede del Bestiario verranno corrette.
- Dubbi di regola dal giro di lettura della #370 (serata, `ARC07-DEF-4`,
  2026-11-12), da riscontrare quando il lotto li copre; il testo esatto lo ha
  il thread della #370 e le correzioni passano da Jfs perché toccano il master:
  Concentrazione CD 21 nel duello (lotto 6, abilità), la CD di corrompere
  l'acqua (lotto 7, qualità speciali), il «fiancheggiamento spalla a spalla»
  della pattuglia (regola di combattimento, non un numero di scheda: lotto 12).
  Riscontro del 2026-11-13 sull'SRD, senza toccare il master: la
  Concentrazione CD 21 nella nube di Fluttuare è giusta (10 + metà dei 22 DV
  del drago); la CD di corrompere l'acqua (25, e 26 nella variante) è giusta,
  perché l'SRD la fa uguale alla Presenza Terrificante; il fiancheggiamento
  «spalla a spalla» è contro l'SRD, che vuole i due attaccanti ai lati
  opposti del bersaglio. La riga è canone del DM (2026-10-12): la corregge
  solo Jfs.
- Scadenze che toccano gli stessi conti: promozione dei 14 conti PF1e in prova
  (ADR-0119, 23/11) e xdist in testing fino al 22/11.

## 9. Lotto 1, primo passo (in locale, patch `lotto1-in-corso.patch`)

`verifica_scheda` a tolleranza zero su tiri salvezza e attacco, con
`--tolleranza` per tornare a prima. Stesso banco di errori messi apposta:

| | Con la tolleranza | Tolleranza zero |
|---|---|---|
| Errori visti | 701 su 1.279 (55%) | **957 su 1.222 (78%)** |
| TS gonfiati di +2 visti | 1 su 362 | 270 su 343 |
| Violazioni sulle schede vere | 7 in 6 schede | 32 in 26 schede |

Il denominatore scende perché il banco non muta un campo che ha già una
violazione. Restano non visti soprattutto BAB e lotta delle schede senza
composizione leggibile, e i TS dei dadi razziali dell'umanoide, che la regola
lascia variabili.

Dal thread dello standard del volume (PR #370, 9 commit locali, copia in
`/mnt/project-files/taglia-portata/taglia-portata.bundle`): ADR-0128 è suo
(campi `taglia`, `spazio`, `portata` in ogni recinto, 205 schede; tabella in
`taglie.toml` della famiglia d20, che arriva con la #370, capacità `statblocco.taglie`). Quindi il primo
ADR libero per questo programma è 0126. Quando la #370 è su main i lotti
leggono la taglia dal campo e non dalla riga del tipo. Schede che lui ha già
cambiato e che non correggo senza avvisarlo: Sentinella Silenziosa (DEF-1),
beholder-death-tyrant-cr14, hobgoblin-captain-cr8, drow-priestess9-cr11,
gnoll-hyenodon-rider-cr4, thayan-knight-cr8, Lirien, Karkator, ogre-skullcrusher-cr5,
Skullcrusher Vecchio e Wyvern di DEF-4.

## 10. Lotto 1-bis, misura di partenza (2026-11-12, in locale)

I conti dei recinti dei master (`conformita_statblocchi.conti_del_recinto`:
somma della CA, contatto e sprovvista, sensi, CD) oggi girano nel cancello dei
moduli e non in `verifica_scheda`. Applicati così come sono alle 134 schede
recintate del Bestiario trovano: CA 27, sensi 10 (scurovisione mancante), CD
del soffio 1. Danno anche 25 scarti sui pf, che però sono la regola «media» dei
master e nel Bestiario non vale (lì i pf stanno nella fascia dei dadi).
Il lotto 1-bis porta CA, sensi e CD in `verifica_scheda`, somma le voci della
CA per tipo con `dmcore.bonus` (due bonus di armatura non si sommano) e aggiunge
gli oggetti dell'SRD col prezzo. Da pubblicare dopo il merge della #380.

### Lotto 3-bis fatto (2026-11-12)

I requisiti delle classi di prestigio sono in `verifica_scheda` (ADR-0126,
«Lotto 3-bis»): `estrai_prestigio.py`, `muta_prestigio.py`,
`misure-prestigio.json`. Del lotto 3 del piano restano: l'avanzamento
d'incantatore dato dalle classi di prestigio («+1 livello della classe
esistente»: oggi una lista di un chierico 9 / Runecaster 4 si giudica da
chierico 9 o resta non letta), le capacità di classe che toccano i numeri, il
rigiudizio delle 7 violazioni di talenti (card aperta al DM) e l'uscita JSON
per scheda chiesta dal thread della #379. Vanno nel lotto 4.

### Lotto 4 fatto in parte (2026-11-12)

Il numero dei talenti è in `verifica_scheda` (ADR-0126, «Lotto 4»):
`muta_numero_talenti.py`, `misure-numero-talenti.json`. Del lotto 4 restano gli
effetti dei talenti sui numeri, e dal lotto 3 l'avanzamento d'incantatore delle
classi di prestigio, le capacità di classe che toccano i numeri, il rigiudizio
delle 7 violazioni di talenti (card aperta al DM) e l'uscita JSON per scheda
per il thread della #379.

### Lotto 4 chiuso (2026-11-12)

Gli effetti dei talenti sulle abilità sono nel conto dei gradi (ADR-0126,
«Lotto 4, seconda parte»): `estrai_effetti_talenti.py`, `muta_effetti_talenti.py`,
`misure-effetti-talenti.json`. Gli altri effetti (pf, tiri salvezza, iniziativa,
attacco, danno) erano già nei conti. Restano, fuori dal lotto 4: l'avanzamento
d'incantatore delle classi di prestigio, le capacità di classe che toccano i
numeri, il rigiudizio delle 7 violazioni di talenti (card aperta al DM),
l'uscita JSON per scheda per il thread della #379, e Autoipnosi fra le abilità
3.5 del plugin.

### Lotto 3-ter fatto (2026-11-12)

L'avanzamento d'incantatore delle classi di prestigio è in `verifica_scheda`
(ADR-0126, «Lotto 3-ter»): `estrai_prestigio.py` (voce `avanza`),
`muta_avanzamento.py`, `misure-avanzamento.json`. Dubbio nuovo per il DM:
`underdark-dovil-runecaster-cr7` lancia «da Diviner 5», Diviner 5 / Deep
Diviner 1 dà 6. Restano le liste proprie di Assassino e Guardia Nera.

### Lotto 5, seconda parte: il grado di sfida (2026-11-13)

Verifica `grado_di_sfida` (regola `numero.gs`), conto in `scripts/dmcore/gs.py`,
numeri in `gs.toml` (tabella `[gs]`, 3.5 e PF1e). Misura: violazioni 30 → 33,
non verificabili 293 → 371 (78 dubbi nuovi, tutti con la ragione). Banco
`muta_gs.py` → `misure-gs.json`: 92 su 98. Restano del lotto 5: modificatori
razziali delle caratteristiche, modificatore di livello, modelli, avanzamento
per dadi vita, mostri dei manuali, chiave per blocco in `--fatti`.

### Lotto 5, terza parte: i fatti scheda per scheda (2026-11-13)

`--fatti` ha la chiave `blocchi` (una voce per scheda del file: titolo, righe,
talenti) e S8 giudica i file con più schede scheda per scheda. Misura: talenti
dati da `--fatti` 500 → 748; S8 sul Bestiario 60 → 65 schede lette, 0
violazioni. Restano del lotto 5: modificatori razziali delle caratteristiche,
modificatore di livello, modelli, avanzamento per dadi vita, mostri dei manuali.

### Lotto 6, prima parte: le abilità di classe (2026-11-13)

`gradi.toml` del 3.5 ha le abilità di classe di 38 classi, quelle di cinque
domini, le sinergie e i bonus alle abilità delle sette razze dell'SRD.
`verifica_scheda` ha la regola `gradi.massimo.fuori_classe` (massimo dimezzato,
costo doppio) e conta il margine vero per le sette razze. Misura: violazioni
33 → 33, non verificabili 371 → 371; banco `muta_abilita.py`, ogni abilità +4
da sola: 10 → 16 su 162. Restano del lotto 6: penalità di armatura alla prova,
gradi dichiarati fra parentesi, bonus alle abilità delle razze dei mostri,
le stesse tabelle per PF1e.

### Lotto 6, seconda parte: la penalità di armatura alla prova (2026-11-13)

`gradi.toml` del 3.5 ha `[penalita_di_prova]` (nove abilità, Nuotare doppia,
dodici armature e sei scudi dell'SRD) e `verifica_scheda` la aggiunge ai gradi
minimi delle abilità che la subiscono, nella misura più bassa possibile.
Misura: violazioni 33 → 33, non verificabili 371 → 371; 62 schede con
un'armatura riconosciuta; banco, tutte +6: 18 → 20 su 32. Restano del lotto 6:
bonus alle abilità delle razze dei mostri, le stesse tabelle per PF1e. I gradi
dichiarati fra parentesi non si fanno: li scrive una scheda sola.

### Lotto 7, prima parte: la velocità a terra (2026-11-13)

`movimento.toml` del 3.5 (capacità `creature.costruzione`): velocità delle sette
razze, categoria delle armature, velocità ridotta, barbaro e monaco. Verifica
nuova `velocita` (regola `numero.velocita`). Misura: violazioni 33 → 33; 18
schede giudicate su 100 con la riga; banco `muta_velocita.py` 15 su 18 per
verso, su main 0. Restano del lotto 7: resistenza agli incantesimi, riduzione
del danno, immunità dei tipi, sensi delle razze, linguaggi.

### Lotto 7, seconda parte: resistenza agli incantesimi e riduzione del danno (2026-11-13)

`difese.toml` del 3.5 (capacità `creature.costruzione`): sei razze con la RI
«N + livelli di classe», monaco, RD del barbaro. Verifica nuova `difese`
(regole `numero.RI`, `numero.RD`). Misura: violazioni 33 → 34 (la RI del
Collezionista, 27 contro 38: decide il DM), non verificabili 371 → 372; 8 RI
giudicate su 26 scritte e 3 RD su 4; banco `muta_difese.py` 6 su 6 e 3 su 3 per
verso, su main 0. I sensi hanno già un controllo. Restano del lotto 7: immunità
dei tipi, linguaggi.

### Lotto 7, terza parte: le immunità del tipo (2026-11-13)

`[difese.immunita]` in `difese.toml`: le immunità dei sette tipi dell'SRD che
ne hanno. Regola nuova `tratti.immunita` nella verifica `difese`: formula
«tratti dei …» o elenco completo. Misura: violazioni 34 → 37 (tre non morti
senza i tratti: decide il DM); 18 schede in regola su 21 del tipo; banco 16 su
18, su main 0. Resta del lotto 7: i linguaggi.

### Lotto 7, quarta parte: i linguaggi automatici (2026-11-13)

`linguaggi.toml` del 3.5 (capacità `creature.costruzione`): linguaggi
automatici delle sette razze e Druidico del druido. Verifica nuova `linguaggi`
(regola `tratti.linguaggi`), solo per chi scrive la riga. Misura: violazioni
37 → 37; 7 schede giudicate su 24 con la riga; banco `muta_linguaggi.py` 13 su
13, su main 0. Lotto 7 chiuso. Fuori dal lotto, dichiarati: carico, RD che non
è N/—, sottotipi, razze dei mostri, PF1e.

### Lotto 8, prima parte: il valore dell'equipaggiamento (2026-11-13)

`oggetti.toml` del 3.5 (capacità `creature.costruzione`): 623 prezzi dell'SRD,
prezzo del potenziamento di armi e armature, valore dell'equipaggiamento di un
PNG per livello (DMG 3.5, Tabella 4-23, solo i numeri). Verifica nuova
`ricchezza` (regola `equipaggiamento.valore`): la somma degli oggetti dal
prezzo certo è un minimo, e conta solo se supera la tabella. Misura: violazioni
37 → 37, non verificabili 372 → 374; 7 schede con oggetti dal prezzo certo;
banco `muta_ricchezza.py`: 24 violazioni e 88 non verificabili su 112, su main
0. Resta del lotto 8: pozioni, pergamene, bacchette e bastoni, capacità
speciali, modificatore di livello delle razze dei mostri, tabella PF1e.

### Lotto 5, quarta parte: modificatore di livello delle razze senza dadi vita (2026-11-13)

`mdl.toml` del 3.5 (capacità `creature.costruzione`): dieci razze che l'SRD
presenta come combattenti di 1° livello, con la loro riga «Level Adjustment».
`ricchezza` le usa per il livello effettivo. Misura: violazioni 37 → 37, non
verificabili 374 → 374; banco `muta_ricchezza.py`: violazioni 24 → 57, non
verificabili 88 → 55. Resta del lotto 5: modificatori razziali alle
caratteristiche, modelli, avanzamento per dadi vita, mostri dei manuali.

### Lotto 8, seconda parte: capacità speciali, pozioni, pergamene, bacchette (2026-11-13)

`oggetti.toml` ha le capacità speciali di armi, armature e scudi e i prezzi
delle pergamene; i nomi italiani vengono dal lessico. Una capacità conta solo
attaccata al nome o al bonus, una bacchetta solo con le cariche scritte.
Misura: violazioni 37 → 37, non verificabili 374 → 374; valore riconosciuto
nel Bestiario 224.000 → 267.830 mo; banco, seconda prova: 41 → 57 su 125.
Resta del lotto 8: bastoni, materiali speciali, tabella PF1e.

### Lotto 8, terza parte: adamantio, mithral, bastoni con le cariche (2026-11-13)

`oggetti.toml` ha `[oggetti.materiali]` (adamantio e mithral, per categoria,
dalle tabelle di «Special Materials» dell'SRD). La verifica `ricchezza` somma
il materiale al potenziamento, conta l'oggetto di materiale speciale anche
senza «+N» e i bastoni con le cariche scritte. Misura: violazioni 33 → 33, non
verificabili 374 → 375 (Ghaurush Cenerevento GS 16: 36.300 mo contro 35.000,
razza senza modificatore di livello noto). Banco, terza prova: 1 → 52 su 125.
Resta del lotto 8: prezzo base degli oggetti comuni, tabella PF1e.

### Lotto 8, quarta parte: prezzo base, forme di ADR-0091, dati di ADR-0134 (2026-11-14)

`[oggetti.comuni]` e `[oggetti.perfetta]` nel 3.5; `ricchezza` conta prezzo
base e fattura, legge la riga delle Statistiche e le due voci
dell'equipaggiamento, non conta due volte recinto e prosa; regola
`equipaggiamento.da_png` («Improving Monsters», 52 creature che avanzano per
classe). PF1e: `oggetti.toml` (Tabella 14-9) e `codex.toml` (454 PNG), da
`estrai_codex.py` (`--check`, `--cerca CLASSE LIVELLO`). Misura: violazioni
30 → 30 (sette schede vere sopra la tabella, dichiarate dal DM sulle card
del 2026-11-14 con la riga «Equipaggiamento sopra la tabella»), non
verificabili 372 → 374. Banco, quarta prova: 0 → 50 su 118. Lotto 8 chiuso
per il 3.5; restano i prezzi degli oggetti PF1e.
