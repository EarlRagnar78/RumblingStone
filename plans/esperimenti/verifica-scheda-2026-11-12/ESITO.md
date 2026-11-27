# Verifica di una scheda via MCP e divario delle regole: misura del 2026-11-12

Richieste del DM (2026-11-12): verificare via server MCP non solo i talenti ma
anche BAB, gradi delle abilità e «tutto quello che la scheda scrive», con le
regole del plugin del sistema e nell'ordine **SRD d20 → D&D 3.5 → PF1e**;
misurare che cosa manca ai plugin rispetto a SRD, srd.dndtools.org, PCGen e
chiudere il divario dove la misura dice che serve. Decisione in
[ADR-0124](../../adr/ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) §6-§7.

## 1. Che cosa c'è adesso

`scripts/verifica_scheda.py`, nel manifest e quindi nel server MCP, sola
lettura. Una chiamata, un'uscita: per ogni difetto `verifica` (talenti o
numeri o abilita), `regola`, `atteso`, `ha`, `fonte`, `file:riga`. Chiama
`verifica_talenti` e `conformita_statblocchi.giudica`; l'unica regola sua è
quella dei gradi delle abilità (§2-bis).

Bestiario: 126 schede lette, **23 violazioni in 12 schede** (tutte di
talenti), 65 voci non verificabili.

## 2. Quanto vede: numeri sbagliati messi apposta

`muta_numeri.py` cambia un numero per volta nelle schede `*-cr*.md` pulite e
chiede allo strumento se lo vede.

| Errore messo | Visto |
|---|---|
| BAB +1 | 66 / 91 |
| lotta +3 | 74 / 101 |
| tiro salvezza −2 (Temp, Rifl, Vol) | 89 / 121, 88 / 121, 79 / 120 |
| tiro salvezza +5 | 91 / 121, 91 / 121, 87 / 120 |
| tiro salvezza +2 | 1 / 121, 0 / 121, 0 / 120 |
| **Totale** | **666 / 1.278 (52%)** |

Perché ne perde metà, contato sui mutanti persi:

- **Tiri salvezza +2: non li vede per regola.** `conformita_statblocchi`
  accetta fino a +4 sopra il minimo, perché un mantello della resistenza o un
  talento non stanno nella riga dei TS. È una scelta, non un difetto, ma vuol
  dire che un TS gonfiato di 2 passa.
- **La regola non parte** su circa un quarto delle schede: la composizione dei
  dadi vita non è nota (9 dei 25 BAB persi, 19 dei 32 Tempra persi) oppure la
  scheda ha una **classe che il plugin non conosce** (5 e 5).
- **Parte ma tollera lo scarto** (10 BAB, 26 lotte): il confronto accetta
  ±1 o varianti dichiarate.
- **Schede a dossier** (`Bestiario/png/*/*.md`): la lettura dei numeri non è
  collaudata su quel formato («BAB/Lotta: +8 / +10» letto come lotta 8), quindi
  i loro numeri vanno fra i non verificabili.
- **Gradi delle abilità: non c'era nessun controllo.** Aggiunto in questo
  giro, vedi §2-bis.

## 2-bis. Gradi delle abilità (capacità nuova `creature.gradi`)

`estrai_gradi.py` scrive le regole nei due plugin, da fonti OGL in cache:
`sistemi/dnd35/dati/gradi.toml` (SRD 3.5: 37 abilità con la caratteristica
chiave, punti per livello di 65 classi, punti per dado vita di 15 tipi; massimo
= dadi vita + 3, primo dado × 4) e `sistemi/pf1e/dati/gradi.toml` (PRD: 26
abilità, 13 tipi; massimo = dadi vita, +3 d'abilità di classe; i punti per
livello delle classi erano già in `classi.toml`).

La scheda scrive il bonus, non i gradi. Lo strumento calcola i gradi **minimi**
che un bonus chiede (bonus − caratteristica − margine per sinergia, razza e
talenti) e applica due condizioni necessarie: `gradi.massimo` per abilità e
`gradi.punti` sulla somma.

Bestiario: 33 schede con una riga di abilità; 29 pulite, 4 non calcolabili (3
per classi di prestigio fuori dal plugin, 1 per il tipo), **0 segnalazioni
sulle schede vere**. Con errori messi apposta (`muta_abilita.py`, 29 schede):

| Errore messo | Visto |
|---|---|
| una abilità +4 | 3 / 29 |
| una abilità +8 | 18 / 29 |
| una abilità +12 | 21 / 29 |
| tutte le abilità +3 | 4 / 29 |
| tutte le abilità +6 | 14 / 29 |

Vede gli errori grossi e non quelli piccoli: il margine (da 4 a 13 punti) è
largo apposta per non segnalare schede giuste. Per stringerlo servono i bonus
razziali per razza e le abilità di classe per classe, che il plugin non ha.

## 2-ter. Classi dei manuali 3.5 fuori SRD (2026-11-12, secondo lotto)

`sistemi/dnd35/dati/classi_manuali.toml`, da
`plans/esperimenti/classi-manuali-35-2026-11-12/estrai_classi.py`: **658 classi**
(dado vita, BAB, tiri salvezza buoni, punti abilità, abilità di classe, nome
italiano del lessico per 194). Solo nome e numeri (scelta del DM).

| Fonte | Classi |
|---|---|
| srd.dndtools.org (332 pagine di classi; 25 erano già nel plugin) | 304 |
| di cui anche in PCGen | 153: **136 con gli stessi numeri, 17 diverse** |
| solo PCGen (`TYPE` da personaggio; via i dadi vita razziali e le classi decadute) | 354 |

Le 17 su cui le fonti divergono, le 10 senza tabella leggibile, le 2 col BAB
irregolare e quelle coi tiri salvezza «medi» **non entrano nei conti**: restano
sconosciute, quindi «non verificabili». Il sito sbaglia almeno due dadi vita
che conosco dal libro (Factotum e Healer d6, il libro e PCGen danno d8): per
questo una divergenza non si risolve a favore di nessuno.

| Misura | Prima | Dopo |
|---|---|---|
| Classi che la lettura conosce (3.5) | 30 | 30 + 612 dei manuali |
| Numeri sbagliati messi apposta, visti | 666 / 1.278 | **701 / 1.278** |
| Schede con abilità calcolabili | 29 | **32** |
| Voci non verificabili su Bestiario e archi 00-09 | 82 | **76** |
| Violazioni | 26 | 28 (2 prima nascoste: Rurik, livello d'incantatore 4 con un talento che ne chiede 5; il runecaster dovil senza incantesimi divini) |
| Schede del Bestiario che cambiano lettura | — | 4 (Rurik, Balvar, il dovil, Zarim: ora la composizione si legge) |

Il guadagno è piccolo perché nel repo le classi fuori SRD con un livello
scritto sono poche: warlock (24 volte, quasi tutte nei moduli e non in schede),
shaman, dragon shaman, deep diviner, favored soul, knight, scout, swordsage.

Limiti: un nome dei manuali vale solo scritto intero («tempest» leggeva
«Cantore delle tempeste 2» come 2 livelli di Tempest, corretto prima del
commit); un nome che finisce con una classe dell'SRD («Red Wizard 7») si legge
ancora come quella classe; le 354 classi solo PCGen hanno una fonte sola e
nessun riscontro; la progressione degli incantatori di queste classi non c'è.

## 2-quater. Prerequisiti fisici: movimento, taglia, tipo, attacchi naturali

Dopo le classi, 30 delle 76 voci non verificabili erano prerequisiti che la
regola non leggeva («Fly speed», «Three or more natural attacks», «size Large
or larger», «Natural armor», «Base Fortitude save bonus +2», «dragon type»).
Non mancavano dati nei plugin: mancava la lettura del fatto dalla scheda.
`verifica_talenti.fatti_fisici` legge velocità (volo, nuoto, scalare, scavare,
in metri o piedi), taglia, tipo, attacchi naturali, armatura naturale, soffio e
tiri salvezza base; `giudica_altro` li confronta col prerequisito. Se la scheda
non ha la riga da cui leggere, il prerequisito resta non verificabile.

| Misura | Prima | Dopo |
|---|---|---|
| Voci non verificabili (Bestiario e archi 00-09) | 76 | **47** |
| Violazioni nuove sulle schede vere | — | 0 (i 29 prerequisiti letti sono tutti soddisfatti) |
| Fatti tolti apposta (`muta_fisici.py`) | — | volo 5/5, taglia 2/2, attacchi naturali 2/4 |

I 2 attacchi naturali non visti: la scheda scrive solo l'attacco singolo, e da
quello non si conclude che gli attacchi siano pochi. Dei 1.515 prerequisiti
`altro` dei talenti dei manuali, questi schemi ne coprono un centinaio; i più
numerosi restano razza (357), capacità di classe (187), divinità o regione
(101): la razza è il prossimo che si può leggere dalla scheda.

## 2-quinquies. Incantesimi: lista della classe e livello

Capacità nuova `creature.liste_incantesimi`. Per il 3.5
`sistemi/dnd35/dati/liste_incantesimi.toml`, generato dalla riga «Level:» di
ogni incantesimo dell'SRD (`plans/esperimenti/incantesimi-35-2026-11-12/`): 601
incantesimi, 7 classi, 22 domini. Per il PF1e le liste del PRD c'erano già
(ADR-0119, lotto 3) e nessuno strumento le leggeva. `verifica_scheda.incantesimi`
legge le righe «N° — *nome*, *nome*» sotto un'intestazione che nomina la classe.

| Misura | Valore |
|---|---|
| Righe di incantesimi per livello nel repo | 203: 109 con la classe leggibile, 94 no (non giudicate) |
| Violazioni sulle schede vere | **6** |
| Nomi che le liste non hanno | 63 (manuali fuori SRD, varianti del nome italiano) |
| Livello abbassato di uno apposta, visto | 82 / 85 |
| Incantesimo fuori lista aggiunto apposta, visto | 85 / 85 |

Le 6: *Grazia del Gatto* al 1° e *Suggestione di Massa* al 3° di un bardo
(Salvatore); *profanare* al 2° per due chierici, dove il lessico dice che
«Profanare» è *Unhallow* (5°) e l'incantesimo di 2° è «Dissacrare»
(*Desecrate*); *Fulmine* a un bardo in due file di ARC-08.

Limiti: adepto, assassino e guardia nera non hanno lista (nell'SRD sta nel
testo della classe); le liste delle classi dei manuali (warmage, hexblade,
healer: il sito le ha) non sono caricate; non si controlla quanti incantesimi
al giorno; un livello più alto del dovuto passa sempre.


## 2-sexies. Chiusura delle violazioni, liste dei manuali, razza

Richiesta del DM (2026-11-12): correggere gli errori, ma prima finire la parte
delle classi (righe senza classe, liste delle classi dei manuali, razza).

| Misura | Prima | Dopo |
|---|---|---|
| Violazioni (Bestiario + moduli) | 34 in 20 schede | **7 in 6 schede** |
| Righe di incantesimi senza classe leggibile | 94 su 203 | 16 su 174 (29 erano intervalli «1–4:», non righe di livello) |
| Incantesimi nelle liste 3.5 | 601 (SRD) | 601 + 3.969 dei manuali (PCGen) |
| Classi con una lista | 7 | 84, più 62 che pescano da liste altrui |
| Livello abbassato di uno apposta, visto | 82 / 85 | 123 / 127 |
| Incantesimo fuori lista aggiunto apposta, visto | 85 / 85 | 124 / 127 |
| Voci non verificabili | 120 | 129 (le righe nuove portano nomi che le liste non hanno) |

Dove sono finite le 34: 12 erano falsi positivi dello strumento (talento che
la classe del manuale concede, talento equivalente, fonti dei manuali che
divergono, file con più schede), 16 sono state corrette in 9 schede, 1 è nuova
(righe che prima non si leggevano), 7 restano.

Corrette (nessun numero scritto cambia):

| Scheda | Correzione |
|---|---|
| orco-berserk-barbaro2-cr2 | «Carica Devastante» era *Powerful Charge* nella fonte PCGen: ora «Carica Possente» |
| abbathor-cleric11-cr11, emissario-red-hand-cr12 | *profanare* (5°) scritto al 2° per *dissacrare* |
| drow-trickster-arcano-cr11 | aggiunto Tiro Ravvicinato (aveva 5 talenti su 6) |
| drow-assassina-lolth-cr10 | 5 talenti con 9 DV: aggiunto Tiro Ravvicinato, tolti Furtivo e Attacco Rapido |
| drow-noble-guard-cr5 | *Improved Two-Weapon Fighting* (BAB +6, ne ha +3) → *Combat Reflexes* |
| ogre-frantumapietra-barbaro6-cr9 | Incalzare Potenziato → Spingere Migliorato, prerequisito di Colpo Terrificante |
| bruto-deforme-sottosuolo-cr11, ogre-micelio-sporeborn-cr8 | Lottare Migliorato (e Sbilanciare Migliorato) segnati «(B)», talenti bonus della creatura |

Le 7 rimaste, vere anche con i dati delle classi dei manuali:

| Dove | Che cosa | Perché resta |
|---|---|---|
| Salvatore.md:217, :221 | *Grazia del Gatto* al 1°, *Suggestione di Massa* al 3° | l'Accordo Sublime pesca dalle liste di bardo e mago ma dà solo slot dal 4° in su; la Spia non lancia |
| ARC08-01:679, ARC08-02:603 | *Fulmine* fra gli incantesimi da bardo di Tempestas | non è in nessuna lista da bardo; lo Stormsinger non è nei dati PCGen e la sua pagina non lo concede |
| rurik-gorunn-cr10.md:21 | *Divine Armor* chiede livello d'incantatore divino 5 | paladino 8 = LI 4; il Martello di Moradin non fa avanzare gli incantesimi. PCGen lo accetta perché conta il livello di classe |
| underdark-dovil-runecaster-cr7.md:23 | *Inscribe Rune* chiede incantesimi divini | divinatore, deep diviner e guerriero non ne lanciano |
| Arco-Post-Hammerfist-P1C:361 | *Flame Strike* al 4° per un chierico 8 | è di 5°; le tattiche dell'incontro (righe 374-480) sono costruite su quel colpo |

Limiti: «(B)» è una dichiarazione del DM, lo strumento la accetta solo per chi
ha dadi vita razziali ma non sa se la creatura dovrebbe averla. Razza e
allineamento non cambiano nessun esito sulle schede di oggi: nessun talento
scritto li chiede in una forma che la riga del tipo permetta di giudicare. I
nomi italiani degli incantesimi dei manuali non sono nel lessico: una scheda
che li scrive in italiano resta non verificabile. L'ambiente non è usato da
nessuna regola.

## 3. Divario dei plugin, sezione per sezione

| Sezione | Plugin `dnd35` oggi | SRD 3.5 in cache | srd.dndtools.org | Dati PCGen (WotC 3.5) | Plugin `pf1e` |
|---|---|---|---|---|---|
| Talenti | 363 SRD + 2.193 dei manuali (da oggi) | 363 | 38 pagine, 1.553 in tabella | 2.037 | 1.227 |
| Classi base | 11 + 5 da PNG | 11 + psioniche | 65 pagine | 74 file `class` (base e prestigio) | 55 |
| Classi di prestigio | 14 (SRD) | 14 + epiche e psioniche | **268 pagine** | compresi sopra | nelle 55 |
| Abilità | nomi + caratteristica chiave di 37 (da oggi) | pagine complete | 4 pagine | 28 file | 26 con la chiave (da oggi) |
| Punti abilità per livello | 65 classi, 15 tipi (da oggi) | nelle pagine di classe e di tipo | nelle pagine di classe | campi `STARTSKILLPTS` | classi + 13 tipi (da oggi) |
| Incantesimi (liste per classe) | 6 classi, liste corte del generatore | tutti | 27 pagine | 72 file | liste complete |
| Razze | 20 | Core + mostri | 2 pagine indice | 57 file | 37 + 100 voci |
| Tipi di creatura | 15 | sì | sì | — | 13 |
| Equipaggiamento | 30 armature, 11 scudi | sì | 5 pagine | 98 file | 12 + 6 |
| Poteri psionici, invocazioni, magie alternative | assenti | psionici sì | 18 + 8 + 8 pagine | parziale | — |
| Mostri | Bestiario del repo | sì | 5 pagine indice | — | — |
| Varianti (Unearthed Arcana) | assenti | no | 37 pagine | parziale | — |

Il sito ha 616 pagine nella mappa; 404 sono classi (base e di prestigio) e
manuali.

## 4. Ordine in cui chiudere (dal più utile alla verifica)

1. **Punti e gradi delle abilità** (3.5 e PF1e): fatto in questo giro (§2-bis).
   Per vedere anche gli errori piccoli servono le abilità di classe per classe
   e i bonus razziali per razza.
2. **Classi di prestigio e classi base fuori SRD** (BAB, TS, dado vita, punti
   abilità, avanzamento da incantatore): toglie «la regola non parte» e i
   «non verificabili per classe ignota». Fonti: srd.dndtools.org e PCGen,
   con lo stesso confronto fra le due fatto per i talenti.
3. **Composizione dei dadi vita non nota**: è lettura delle schede, non
   regola; va vista scheda per scheda.
4. **Liste di incantesimi complete per classe** (oggi il generatore ne ha
   poche): serve a controllare che un incantesimo scritto sia della lista e
   del livello giusti.
5. Razze dei manuali, equipaggiamento, psionici: dopo, e solo se una misura
   come quella del §2 mostra errori che oggi passano.

## 5. Limiti

- srd.dndtools.org riporta manuali non OGL e il repo PCGen non dichiara una
  licenza: nel repo entrano solo fatti di regola (nomi, soglie, progressioni),
  mai testo. Se il DM non vuole tenerli, i file `*_manuali.toml` si tolgono
  senza toccare il codice.
- Sui talenti le due fonti divergono in 353 casi su 1.156: una violazione che
  viene da un manuale va riletta sul libro prima di correggere la scheda.
- Il giro di autocorrezione su un modello vero resta non misurato (ESITO del
  2026-11-11, §5).

## Riprodurre

```bash
python3 scripts/verifica_scheda.py Bestiario
python3 plans/esperimenti/verifica-scheda-2026-11-12/muta_numeri.py
python3 plans/esperimenti/verifica-scheda-2026-11-12/muta_abilita.py
python3 plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py --check
```
