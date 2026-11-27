# ADR-0121 — Un plugin di regole si misura contro la fonte, non contro la sua dichiarazione

**Stato**: proposta (2026-11-09)
**Data**: 2026-11-09
**Decisione-fonte**: il DM (Jfs), 2026-11-09: *«controllare che le regole plugin per d20srd d&d 3.5 e pf1e siano davvero complete funzionanti ed utilizzate e correggile se necessario misurando il miglioramento»*.
**Rapporti**: completa [ADR-0111](ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md) e [ADR-0112](ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md). Misure e rapporto in [plans/esperimenti/plugin-regole-2026-11-09/](../esperimenti/plugin-regole-2026-11-09/RAPPORTO.md).

## Contesto

`scripts/sistemi.py` dava 16 capacità su 16 per dnd35 e per pf1e. Il controllo verifica però solo che una capacità sia **dichiarata**. Non verifica che la tabella dietro sia completa, né che i numeri siano quelli della fonte.

I test delle tabelle 3.5 confrontano i dati con le «righe d'àncora verificate» delle skill (`dnd-35-srd/references/classes.md`, `spells.md`), non con l'SRD. Misurando contro l'SRD in cache sono emersi due casi:

- l'àncora del ranger e quella dei conosciuti del bardo riportano numeri PF1e (in parte sbagliati anche per PF1e), con l'etichetta «SRD»;
- l'àncora delle liste aveva gli stessi 8 incantesimi a livello sbagliato del plugin.

In tutti e due i casi il test era verde perché confrontava due copie dello stesso errore.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Una misura che estrae le tabelle vere da SRD 3.5 e PRD PF1e in cache e le confronta riga per riga con il plugin** (scelta) | dice coperte, giuste, sbagliate e non verificabili per ogni tabella; riproducibile, senza rete; trova gli errori delle àncore | legge l'HTML delle tabelle SRD/PRD, che può cambiare con un nuovo commit della fonte |
| Fidarsi delle àncore delle skill | nessun lavoro | le àncore sono scritte a mano e qui erano sbagliate |
| Rifare i plugin interi da zero, generati dalla fonte | nessun numero scritto a mano | cambia anche quello che è giusto; il DM ha già scelto dove il 3.5 cede al PF1e (livello d'incantatore −3) |

## Decisione

1. Ogni tabella di regole di un plugin si misura contro la fonte in cache con
   `plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py`, non
   contro un'àncora scritta a mano. Una divergenza voluta (scelta del DM)
   si scrive nei dati con la fonte, come il «−3» di `formule.toml`.
2. Le correzioni entrano solo con prima e dopo misurati, e con il banco
   d'invarianza (`impronta_creature.py --confronta`, `impronte.py --confronta`)
   che cambia solo dove la correzione lo vuole.
3. Le scelte tra 3.5 e PF1e vanno al DM in card, perché scegliere una
   tabella intera è una scelta di campagna. Mescolare le due tabelle invece
   non si fa. Per ranger, paladino e bardo il DM ha scelto il 2026-11-09
   «Tabelle PF1e intere, segnate». Le classi così scelte sono elencate in
   `incantatori_regole.griglia_pf1e`, e la misura le confronta con il PRD
   invece che con l'SRD.
4. La misura parte in prova (in `plans/esperimenti/`). Passa a cancello in CI
   con la promozione di ADR-0099, dopo il lotto delle classi PF1e. I dati di
   quel lotto li genera dal PRD il thread della #363. Costruttore, strumenti e
   misura li fa questo thread.

## Misura

- dnd35, prima: 97% delle righe misurate coperte, 31 righe sbagliate (griglie
  di ranger, paladino e adepto, conosciuti del bardo, 8 incantesimi).
  Mancavano 12 classi di prestigio, 3 armature e 7 abilità.
- dnd35, dopo questa PR: 100% coperto, 605 righe giuste su 606 verificabili.
  Ranger, paladino e bardo seguono il PRD PF1e come da card. L'unica riga che
  resta è il TS dell'umanoide, una scelta da scrivere. 185
  voci delle liste non si possono verificare perché il loro nome italiano non
  è quello del lessico.
- pf1e, prima: 36% coperto (39/108 righe). Mancavano classi, armature e
  griglie, e `genera_creatura --sistema pf1e` rifiutava i livelli di classe.
- pf1e, dopo il lotto PF1e: **217/217 righe coperte e giuste**, con la misura
  estesa all'uso. Su main 421dbd0 la stessa misura dà 59 righe coperte e 46
  giuste. Il dettaglio è nel rapporto, § Lotto PF1e:
  - 55 classi su 55 generate, che passano il cancello PF1e;
  - 20 tipi su 20 portati in PF1e che lo passano, contro 7 prima.
- `derive_statblocks` leggeva armature e scudi per pezzi di parola: 11 scudi
  e 2 armature inventati, 1 armatura vera non letta. Ora legge a parola intera
  e parte dal nome più lungo.
- Regole complete (2026-11-10, richiesta del DM): `plans/esperimenti/regole-complete-2026-11-10/`
  misura le parti che la misura di sopra non guardava (inventario in `INVENTARIO.md`).
  Su main f65d78e: PF1e 1546/1551 giuste su 1733 righe (PE, PE per GS, tesoro,
  statistiche per GS, modificatore, liste 3.5 riusate dal pf1e contro il PRD, nomi
  italiani), 3.5 166/172. Trovati: EL 19 del tesoro 3.5 (60.000 contro 61.000,
  corretto), «scaglie» letta come armatura (ora «corazza a scaglie»), e i talenti dei
  PNG generati: 1 «talento firma» senza prerequisiti contro i 3-8 della regola (0/10,
  lotto 3).
- Lotto 3 delle regole complete (talenti dei PNG): `estrai_talenti.py` scrive
  `sistemi/{pf1e,dnd35}/dati/talenti.toml` dal PRD (1.227 talenti, 9 libri) e
  dall'SRD (110), con prerequisiti, tipi, talenti bonus di classe (dalla tabella e
  dal testo delle capacità) e concessi; la capacità nuova `creature.talenti` la usa
  `dmcore/talenti.py`. Misura con la stessa forma, atteso contato a mano sul
  manuale al 7° livello per ogni classe: numero 3.5 0/11 → 11/11, PF1e 0/32 →
  32/32; prerequisiti dei talenti generali ricontrollati 11/11 e 32/32 (prima non
  ricontrollabili: il generatore non teneva BAB e livelli). Restano: talento
  umano (il generatore non sceglie la razza), prerequisiti di gradi (talento
  saltato, non inventato).
- Lotto 2 delle regole complete (nomi d'incantesimo 3.5): 108 nomi delle liste
  classe × funzione (185 voci) erano traduzioni libere, fuori dal lessico, e la
  misura non li poteva verificare. Portati al nome ufficiale, la misura di sopra
  passa da 441 giuste e 185 non verificabili a 626/626 (3.5 da 605/606 a
  790/791), e ha visto due livelli sbagliati che il nome nascondeva (*scudo della
  legge* 8° del chierico, *spaventare* 2° del bardo, corretti). Le liste riusate
  dal pf1e: 445 + 181 non verificabili → 626/626, con `[livello_pf1e]` per le due
  voci che il PRD sposta o non ha (*metamorfosi* 5°, *cura ferite minori*).
- Lotto 4 delle regole complete: i due limiti dichiarati qui sopra per il PF1e
  (requisiti delle classi di prestigio non controllati, sciamano senza livello 0)
  sono chiusi. Requisiti delle 18 classi letti dal PRD e confrontati con una
  seconda lettura (18/18); per ogni classe una via d'ingresso legale costruita a
  mano dà requisiti ✓ e talenti richiesti presi (0/18 → 18/18). Gradi,
  allineamento e requisiti narrativi il generatore non li tiene: li scrive nel
  conto come «da verificare dal DM». Le 17 orazioni dello sciamano vengono dal
  testo «0-Level Shaman Spells» dell'ACG, che la tabella `spell_lists` non ha.
- Lotto 5 delle regole complete: i tratti dei tipi di creatura. Il generatore
  dava Costituzione a non morti e costrutti 3.5, e Int 8 con fino a nove
  talenti a melme, parassiti e costrutti senza mente. Ora i tratti stanno in
  `sistemi/dnd35/dati/creature.toml` (`[tratti_tipo]`, `[pf_bonus_costrutti]`
  letto dalla tabella dell'SRD «Construct Traits»). I pf dei tipi senza
  Costituzione sono i soli dadi (più il bonus di taglia del costrutto), con più
  DV fino a 2×GS, e quello che manca al bersaglio si scrive nel conto. Il PF1e
  porta i pf del non morto sul bersaglio col Carisma. Misura sui mostri generati
  (15 tipi × GS 3/7/12, più il costrutto alle 9 taglie): 3.5 da 33/45 e 0/9 a
  45/45 e 9/9, PF1e da 36/45 e 0/9 a 45/45 e 9/9. Nello stesso lotto il terzo
  limite PF1e dichiarato nel rapporto (costrutti Fine e Diminutive senza pf
  bonus) è chiuso con la tabella «Construct Size» del PRD pubblicato
  (legacy.aonprd.com): «—», cioè 0; l'estrattore esige che concordi con le
  schede per le altre sette taglie. Dei tre limiti del rapporto non ne resta
  nessuno.

## Conseguenze

- Il cruscotto di `sistemi.py` resta una misura della dichiarazione. Il passo
  dopo è fargli leggere la copertura misurata, così non sembra più verde di
  quanto è.
- Le àncore delle skill che si dicono «SRD» vanno riscontrate con la stessa
  misura. Quelle di ranger e bardo ora dicono «PRD PF1e, not SRD 3.5».
- Un bardo o un ranger 3.5 generato è più forte di quello del manuale, e la
  cosa è voluta: il conto lo dice ogni volta.
- Un non morto o un costrutto 3.5 generato ha meno pf del bersaglio del suo GS
  (GS 7: 91-97 contro 102; GS 12: 156 contro 192). È la regola del tipo, e i
  mostri dell'SRD la pagano allo stesso modo con immunità e RD che il
  generatore non aggiunge: il DM le mette, o sceglie un altro tipo.
- **Quello che non è misurato:** CD e capacità speciali delle classi, talenti
  (hanno il loro cancello), oggetti magici, e PE, tesoro e incontri PF1e (già
  generati dal PRD con `--check`).

## Da rivedere se

- cambia il commit di una delle due fonti in `fonti.toml` (la misura va rifatta);
- il DM sceglie un'altra gerarchia tra 3.5 e PF1e per le tabelle degli incantatori.
