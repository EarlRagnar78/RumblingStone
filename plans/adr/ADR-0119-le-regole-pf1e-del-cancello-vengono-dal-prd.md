# ADR-0119 — Le regole PF1e del cancello delle schede vengono dal PRD, e i conti nuovi partono in prova

**Stato**: proposta (2026-11-09)
**Data**: 2026-11-09
**Canale (ADR-0099)**: stable dal 2026-11-25, scelta del DM sulla card del 2026-11-25 (*«Tutti e sei, con il codice»*, D8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md)). 0 avvisi dei conti in prova in 145 run su `main` e in 420 run di PR; i 14 conti passano da `in_prova` a `fatti`, e lo scarto porta sempre la chiave `conto` ([misura](../esperimenti/promozioni-2026-11-25/MISURE.md)).
**Decisione-fonte**: il DM (Jfs), 2026-11-09, thread «Scelte dell'8/11: Bestiario e norme»: *«deve coprire tutto. per le parti bloccanti nelle regole di pf1e apri i threads necessari a colmare questo vuoto nelle regole così sono complete»*. Regola del DM del 2026-11-03: un cancello nuovo parte non bloccante e diventa bloccante dopo la promozione.
**Rapporti**: completa F4 di [ADR-0112](ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md) (`creature.conformita`) e chiude la sua card F4 3 («lo dice e salta il conto»). Usa i dati del plugin PF1e di [ADR-0111](ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md) e il PRD a commit fissato di [ADR-0110](ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md). Il conto dell'attacco e il cancello dei numeri sui master sono di ADR-0118 (thread «Scelte dell'8/11»): questo ADR non li tocca. Segue la regola del DM «si parte dallo standard di fatto»: lo standard qui è il PRD, non una tabella nostra.

## Contesto

`conformita_statblocchi.py --cancello-moduli` controlla in CI le schede ```statblocco``` dei moduli PF1e (Il Drappo di Tarsilia, Il Giardino di Sale e Calce PF1e). Il 2026-11-09 ne saltava tre conti, perché nei dati del plugin PF1e mancava la regola: lotta (in PF1e BMC e DMC), scurovisione e la CD di *corrompere l'acqua*. Il censimento di tutti i numeri delle 14 schede ne ha trovati altri otto che nessun conto guardava, in nessuno dei due sistemi:

| Numero della scheda | Prima | Ora (conto) | Regola, dal PRD |
|---|---|---|---|
| BMC | saltato | `BMC` | BAB + For + taglia; Des se Minuscola o più piccola o con Manovre Agili (Core, book-cr 3437) |
| DMC | saltato | `DMC` | 10 + BAB + For + Des + taglia + deviazione, schivare, sacro… della CA (book-cr 3439) |
| scurovisione | saltata | `scurovisione` | dal tipo, dal sottotipo o dalla razza del Bestiario 1-4 (book-b1 361-433) |
| *corrompere l'acqua* | saltata | `corrompere_acqua` | la CD della presenza terrificante, come in 3.5 (book-b1 1112) |
| BAB | mai | `BAB` | classe per classe (55 tabelle del PRD) più i DV razziali del tipo |
| TS | mai | `TS` | base di classi e DV razziali + caratteristica + Tempra Possente, Riflessi Fulminei, Volontà di Ferro + mantello della resistenza |
| contatto, colto alla sprovvista | mai | `contatto_sprovvista` | CA − armatura − scudo − naturale; CA − Des − schivare |
| iniziativa nel recinto | mai | `iniziativa_recinto` | Des, +4 con Iniziativa Migliorata |
| talento Schivare | mai | `schivare` | +1 di schivare alla CA, sempre |
| visione crepuscolare | mai | `visione_crepuscolare` | come la scurovisione |
| bonus di `pf-dado` | mai | `pf_bonus` | DV × Cos + Robustezza (3, o 1 per DV) + fino a 1 per livello di classe preferita |
| pf con dadi di più tipi | mai | `pf_misti` | media dei dadi + bonus (primo dado al massimo se è di classe) |
| CD e LI degli incantesimi | mai | `cd_incantesimi` | 10 + caratteristica della classe + livello; LI = livello di classe |
| incanalare energia | mai | `incanalare` | (L+1)/2 d6, CD 10 + ½ L + Car, 3 + Car al giorno |

Restano fuori, e lo si dice:

- **attacco e danni**: il conto `attacco` è di ADR-0118, uguale nei due sistemi.
- **abilità**: le schede non scrivono i gradi, quindi il totale non si ricostruisce.
- **CD delle capacità speciali** (veleno, tentacoli paralizzanti…): la regola 10 + ½ DV + mod c'è, ma quale caratteristica usa lo dice la voce di ogni mostro, non una regola generale.
- **GS, velocità, portata**: vengono dalla voce del Bestiario o dal modulo, non da un conto.
- **le schede dei PG pregenerati** (`PREGEN-SEI-SCHEDE-PF1E.md`): non sono recinti ```statblocco```, e il cancello non le legge.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tabelle generate dal PRD (`conformita_prd.toml`), scelte e alias a mano (`conformita.toml`), conti nuovi in prova** (scelta) | ogni numero ha libro e sezione; `estrai_prd_pf1e.py --check` ridà gli stessi byte; un conto nuovo non rompe la CI di nessuno il giorno in cui arriva | due file per una capacità; gli alias italiani dipendono dal lessico |
| Scrivere le regole a mano in `conformita.toml` | un file solo | numeri senza fonte verificabile: è quello che la regola del DM sui numeri ricostruibili esclude |
| Riusare le tabelle 3.5 (`dnd35/creature.toml [classi]`) per il BAB e i TS | già pronte | in PF1e cambiano i DV e i tipi (costrutto, umanoide, esterno, non morto): sarebbe la regola di un altro sistema senza dirlo, quello che F4 vieta |
| Conti nuovi subito bloccanti | protezione piena da subito | contro la regola del DM sui cancelli nuovi; un falso positivo (un bonus razziale che il conto non conosce) fermerebbe ogni PR |

## Decisione

1. **`sistemi/pf1e/dati/conformita_prd.toml`** è generato da `plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py` dal PRD a commit fissato:
   - `[classi]`: BAB e TS di 55 classi (Core, APG, ACG, UC, UM, PNG e prestigio), ciascuna controllata livello per livello contro la formula;
   - `[alias_classi]`: il nome italiano ufficiale dal lessico;
   - `[sensi.tipi]`, `[sensi.sottotipi]`, `[sensi.razze]`: scurovisione in metri e visione crepuscolare;
   - `[corrompere_acqua]`: la frase del PRD, verificata dal generatore.
2. **`sistemi/pf1e/dati/conformita.toml`** tiene le scelte: quali conti si fanno, quali bonus della CA entrano nel DMC, i talenti dei TS, gli alias di tipo, razza e taglia. `[conti.mancanti]` è vuoto. La lotta 3.5 va in `[conti.non_applicabili]`.
3. **Due liste di conti.** `fatti` blocca il cancello, come prima. `in_prova` si conta, e `--cancello-moduli` lo stampa come avviso (⚠) senza fallire. `--cancello-moduli --severo` fa bloccare anche i conti in prova: serve ai test e alla promozione. Promuovere un conto vuol dire spostarlo da `in_prova` a `fatti`.
4. **Il 3.5 non cambia.** I conti nuovi vivono in `conti_di_classe` e `conti_dei_sensi`, e partono solo se il sistema ha `[classi]` e `[sensi]` nei dati. `--master` sui 34 file 3.5 dà lo stesso rapporto di prima, riga per riga.

## Misura

- **Sulle 14 schede vere**, i conti nuovi hanno trovato 7 numeri sbagliati. Tutti sono stati corretti alla regola, nella versione legale:
  - Vidalia: Volontà +6 → **+8**;
  - Sfregio: CA 18 → **19** (talento Schivare), contatto 16, DMC 18 → **20** (anello di deviazione e schivare);
  - cavallo: DMC 18 → **17** (21 contro sbilanciare), come il Bestiary; mancava la visione crepuscolare;
  - skum guerriero 8: Volontà +6 → **+8** (Volontà di Ferro);
  - Mastro Tariq: Robustezza non contata, 13d8+26 → **13d8+39**, pf 88 → **101**.
  Dopo le correzioni `--cancello-moduli --severo` è verde.
- **Prova del contrario** (`scripts/tests/test_conformita_pf1e.py`): quattro schede giuste passano. 27 mutazioni di un solo numero vengono bocciate tutte sul conto giusto. Un numero sbagliato nel Drappo o nel Giardino veri fa uscire il cancello con 0 in prova e con 1 da severo, o da promosso.
- **3.5:** il rapporto `--master` dei 34 file 3.5 è identico a quello di main, e `--riepilogo` e `--check` pure.

## Lotto 2 (2026-11-09): classi, griglie e armature del plugin

L'audit dei plugin (ADR-0121, PR #365) ha misurato il plugin PF1e contro il PRD: 39 righe coperte su 108, il 36%. Mancavano le classi (dado vita, gradi, griglie), le classi di prestigio, le armature. Il DM ha chiesto a questo thread di scrivere i dati e al thread dell'audit di verificarli.

Stessa decisione di sopra, estesa: i dati li genera `estrai_prd_pf1e.py`, con una lettura sola delle tabelle di classe (`_classi`).

- **`sistemi/pf1e/dati/classi.toml`** (nuovo, generato):
  - `[classi]`: 55 classi (21 base, 10 ibride, 5 PNG, 18 di prestigio, l'antipaladino) con dado vita, BAB, TS buoni, gradi per livello, libro e tabella del PRD;
  - `[incantatori]` e `[griglie]`: incantesimi (o estratti) al giorno di 22 classi;
  - `[conosciuti]` di 8 classi spontanee e `[preparati]` dell'arcanista, in tabelle a parte;
  - `[avanza_incantatore]`: i livelli delle classi di prestigio che danno «+1 livello di classe esistente»;
  - `[alias]`: il nome italiano di tutte e 55.
- **`sistemi/pf1e/dati/creature.toml`** prende `[armature]` (12) e `[scudi]` (6) da «Table: Armor and Shields», con penalità alla prova, fallimento arcano e nome italiano.

Tre regole PF1e sono scritte nel file e non lasciate a chi legge:

- trucchetti e orazioni sono a volontà: la cifra di livello 0 è quanti se ne preparano o conoscono, non slot (`livello_zero`);
- il «+1» del chierico è lo slot di dominio e non sta nella griglia (`slot_di_dominio`);
- lo «0» di ranger e paladino al 4° livello vuol dire «solo gli incantesimi bonus». Dove la classe non ha il livello 0, la prima cifra della riga è uno 0 d'allineamento, come nel plugin 3.5.

**Misura.** Riletto con il lettore indipendente dell'audit (`misura_plugin_regole.prd_pf1e`): le 26 classi base e PNG che misura coincidono su dado vita, BAB, TS, gradi e griglie; le 12 armature e i 6 scudi coincidono. Sulle 18 classi di prestigio quel lettore dà TS buoni vuoti, perché cerca un +2 al 1° livello e in PF1e il TS buono di prestigio parte da +1: lì vale la verifica livello per livello di `_classi`. `scripts/tests/test_classi_pf1e.py` tiene 60 righe note scritte a mano.

**Cosa non fa questo lotto.** I dati non sono ancora letti da nessuno strumento: il costruttore PF1e, `derive_statblocks` e `genera_creatura` li collega il thread dell'audit, che aggiorna anche la sua misura. Fino ad allora una scheda PF1e con livelli di classe è trattata come prima. Restano fuori le classi occulte e gli altri volumi che il PRD in cache non ha.

## Lotto 3 (2026-11-10): le liste di classe degli incantesimi

Il costruttore PF1e dell'audit sceglie gli incantesimi dalle liste PF1e e non più da quelle 3.5. `estrai_prd_pf1e.py` genera **`sistemi/pf1e/dati/liste_incantesimi.toml`** dalla tabella `spell_lists` di nove libri del PRD:

- `[liste."classe"]`: 22 classi, le stesse di `classi.toml [incantatori]`, livello per livello, con il nome del PRD;
- `[libro]`: il libro di ciascuno dei 1.536 incantesimi (623 del Core Rulebook), per chi vuole fermarsi al manuale base;
- `[nomi_it]`: il nome italiano del lessico, dove c'è (1.480).

Cosa resta fuori, scritto anche in testa al file:

- le versioni mitiche (65 righe) e la lista «Elementalist Wizard» (129 righe), che è una variante e non una classe;
- i livelli dal 7° al 9° che il PRD dà al warpriest copiando la lista del chierico (73 righe): la classe lancia fino al 6°;
- il livello 0 dello sciamano: il PRD non lo elenca, e il buco non è riempito a mano.

## Lotto 4 (2026-11-10): due aggiunte chieste dall'audit dei plugin

- **Classi contate due volte.** `_livelli_di_classe` leggeva tipo + nome: «ladro 4» scritto in tutti e due dava otto livelli, e BAB e TS non partivano. Ora si legge il tipo, e il nome solo se nel tipo non c'è classe.
- **Pf bonus dei costrutti per taglia** (`[pf_bonus_costrutti]` in `creature.toml`). La tabella nel PRD manca (book-b1 sezione 366 la annuncia e non la riporta). I numeri sono ricavati dalle schede dei Bestiary 1-4: il «+X» dei costrutti senza Robustezza, senza Costituzione e non mitici. Tiny 0 (2 schede), Small 10 (3), Medium 20 (13), Large 30 (15), Huge 40 (7), Gargantuan 60 (2), Colossal 80 (1 sola: il Wickerman). Fine e Diminutive non hanno schede e restano senza voce (aggiornato il 2026-11-10: prendono 0, «—», dalla tabella del PRD pubblicato su legacy.aonprd.com, che per le altre sette taglie concorda con le schede). Limite: il Colossal poggia su una scheda sola, e il Soulbound Shell (escluso perché ha Robustezza) darebbe +35 da Medium, cioè non torna con la regola.

## Conseguenze

- Nessun conto PF1e si salta più per regola mancante. Le parti ancora fuori (sopra) non dipendono da una regola che manca nei dati.
- Un modulo PF1e nuovo prende i conti senza codice nuovo. Una classe o una razza che il PRD non ha (Vigilante, i nomi italiani non nel lessico) non viene riconosciuta, e il conto di BAB e TS su quella scheda non parte. Non dà un falso allarme.
- Il TS non conosce i bonus razziali (per esempio la fortuna dell'halfling) né altri oggetti oltre al mantello della resistenza. Per questo il conto è in prova.
- Le correzioni ai moduli sono passate anche nel booklet DM del Drappo (`DRAPPO-BOOKLET-DM.hb.md`, rigenerato) e nella tabella degli scontri in `06-VILLAIN-E-AGENDE.md`.

## Da rivedere se

- Due settimane con il cancello verde sui moduli (2026-11-23): i conti in prova passano in `fatti`, come gli avvisi di `check_schede` (ADR-0114).
- Arriva un modulo PF1e con PNG di razze con bonus ai TS: allora `[ts]` prende i tratti razziali dal PRD.
- Il 3.5 vuole gli stessi conti (contatto e sprovvista, iniziativa nel recinto e Schivare sono identici): basta scrivere i dati nel plugin dnd35.
