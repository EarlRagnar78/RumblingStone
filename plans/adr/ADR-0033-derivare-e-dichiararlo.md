# ADR-0033 — Leggere prima di derivare, e non derivare alla cieca

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: DM, lotto **H1**, *«per le statistiche usa le tabelle per
generare mostri e PNG che sono SRD, o dove non possibile usa i contenuti gratuiti
di Pathfinder quando non c'è un equivalente nel SRD»*
**Emenda**: [ADR-0021](ADR-0021-statblocchi-machine-readable.md) §3

## Contesto

ADR-0021 aveva lasciato **75 schede su 157** senza blocco statistiche, e il piano
le descriveva come *«non è una decisione, è fatica»*. Misurato, non lo erano: la
fatica presupponeva che i numeri ci fossero da trascrivere, e
`extract_statblocks.py --apply` su quelle 75 estraeva **zero**.

Da lì la richiesta del DM: derivarli dalle tabelle. Eseguendola, il debito si è
rivelato **tre cose diverse**, e solo una era quella che sembrava.

### 1. Cinque schede non sono creature — e non lo saranno mai

`Consiglio_Rethmar` è un **organo collegiale di sette seggi**.
`Profughi_Guado_di_Drellin` è una **popolazione** di ~1.500 anime, che dichiara
già di non portare statistiche *(«ruoli + stime dichiarate + puntatore [Private —
Red Hand of Doom]»)*, ed è una scelta di IP, non una dimenticanza.
`ondata-giganti-fanteria-cr15` è un **aggregato di combattimento di massa**: il
suo «GS 15» è un EL, non il GS di una creatura. `Witchwood_e_Tiri_Kitor` e
`Secondo_Anello_Rethmar` sono **dossier di più PNG**, e il primo lo dice da sé
(*«gli statblock vivono già nell'arco»*).

Forzarci sopra `gs/ca/pf/ts` vorrebbe dire **inventare un mostro che non esiste**.
Finché non c'era un modo di dirlo, quelle cinque risultavano «da migrare» per
sempre: debito che nessuno poteva estinguere, cioè un numero che smette di
significare qualcosa.

**Decisione**: il marcatore `[NON-CREATURA]` nel titolo, con **la ragione scritta
sotto**, toglie la scheda dal conto. Non è un'esenzione silenziosa: si legge nel
file, e `extract_statblocks.py` la conta a parte.

### 2. Dieci schede i numeri li avevano — in dialetti che il lettore non sapeva leggere

Questo è il difetto grosso, e non si vedeva perché il sintomo («la prosa non dice
i numeri») era indistinguibile dalla causa vera («il lettore non li riconosce»).

| Dialetto | Esempio | Schede |
|---|---|---|
| tilde d'approssimazione | `hp ~30; AC ~16` | 10 |
| italiano esteso | `**Punti Ferita:** 60` · `**Classe Armatura:** 19` · `**Tiri Salvezza:** Tempra +7, Riflessi +10, Volontà +6` | 15 |
| GS fra parentesi | `**Grado di Sfida (GS):** 9` | 9 |
| forma compatta a barre | `TS +2/+9/+1` | 1 |
| parentesi con testo dentro | `(104 HP with skeleton template)` | 1 |

Sono **numeri del DM**. Derivarli da capo avrebbe voluto dire sostituire valori
veri con valori calcolati, il danno esatto che ADR-0021 §3 teme. La prova sta in
una scheda sola: per `skeletal-dire-lion-cr6` la derivazione produceva **136 pf**;
la scheda ne diceva **104**, scritti dal DM.

**Decisione**: il lettore impara i dialetti. E quando il numero era una **stima**
(`hp ~30`), il blocco lo dice, con `fonte: valori approssimati nella prosa d'origine`
perché trascrivere `pf: 30` promuoverebbe un'approssimazione a fatto, e al
tavolo non si distinguerebbe più da un numero preso da un manuale.

**Esito: da 82 a 92 schede con il blocco per sola lettura**, e altre **8** chiuse
derivando i soli TS: **100 su 157**, e il debito da 75 a **52**.

### 3. La derivazione vera: fatta, provata, e non abilitata a scrivere

`scripts/derive_statblocks.py` implementa la gerarchia di fonti chiesta dal DM:

- **SRD 3.5** per tutto ciò che il SRD copre: tabella dei tipi di creatura (dado
  dei DV, BAB, TS buoni), progressioni dei TS per classe (comprese le classi PNG),
  **matrici delle caratteristiche** (elite 15/14/13/12/10/8, standard
  13/12/11/10/9/8, le stesse che PF1e chiama *heroic* e *basic*), armatura
  naturale e modificatori per taglia, tabella delle armature;
- **Pathfinder 1e** solo dove il SRD non ha un equivalente: **non esiste una
  tabella «statistiche per GS» nel SRD 3.5**, e la Tabella 1–1 del Bestiary è
  contenuto libero OGL.

⚠️ **Ma la tabella PF1e si usa come guardia, non come fonte.** Non fornisce
numeri: rifiuta i nostri quando sono assurdi. Due ragioni, entrambe misurate:
i suoi valori sono tarati su PF1e, che a parità di GS è più duro del 3.5 su cui
questa campagna gira; e serve un controllo d'uscita, perché il modo in cui questa
derivazione sbaglia **non è rumoroso**.

**E il collaudo respinge tutto.** Su 60 schede, zero superano il proprio controllo
di sanità: CA 11 per un GS 9, pf 22 per un GS 14, CA 80 per un PNG di GS 8. Il
motivo è strutturale, non un difetto da correggere con un'altra passata: **le
schede sono documenti in prosa, non dati.** Un'espressione regolare ci trova
sempre qualcosa di plausibile: «Esperto 2» quando la riga diceva «Esperto 2 /
Acolita 6», «16d12» quando quello era il conteggio giusto ma le caratteristiche
no, e un numero sbagliato con l'aria di un conto entra nel canone e ci resta
fino al tavolo.

**Decisione: lo strumento propone, e scrive una cosa sola.**

La prima versione non scriveva niente, e la guardia *sopprimeva* invece di
annotare: risultato, zero proposte. **Uno strumento che non dice niente non fa
correggere niente**: il rilievo è del DM, ed era giusto. Corretto così:

1. **la guardia annota.** Una proposta con scritto sopra *«⚠ FUORI BERSAGLIO per
   GS 9»* si guarda e si giudica; una proposta soppressa non esiste. Sono **15**.
2. **si scrive un campo solo, e solo i TS** (`--apply-ts`), e solo dove **GS, CA
   e pf li ha scritti il DM**. I tiri salvezza sono la cosa più meccanica del
   sistema: la base è **esatta** dalle tabelle SRD (progressione di classe, o
   tipo di creatura più DV), e l'unica incertezza è il modificatore di
   caratteristica, che viene dalla matrice dichiarata. Non è un numero
   indovinato: è un numero calcolato con una convenzione scritta, su una scheda
   di cui il resto è verificabile a occhio. **Otto schede chiuse così.**
3. **CA e pf non si scrivono mai.** Dipendono da equipaggiamento e Costituzione,
   che da una scheda in prosa non si leggono con affidabilità sufficiente. Lì lo
   strumento resta un proponitore, ed è la stessa disciplina di
   `import_ultraclear.py` per le mappe (bozza più rapporto) che ADR-0021 §3
   cita come precedente.

⚠️ E `allow_abbrev=False` sul parser, perché `argparse` accettava `--apply` come
abbreviazione di `--apply-ts`: chi lo scrivesse aspettandosi la scrittura larga,
quella che **non esiste**, otterrebbe comunque una scrittura.

## Conseguenze

**Buone.**
- Il debito è **misurato bene** per la prima volta: **52**, non 75, e nessuno di
  quei 52 è un falso debito.
- Dieci schede hanno i numeri del DM invece di non averne, e otto hanno i TS
  calcolati dalle tabelle con il conto scritto accanto.
- Il lettore conosce cinque dialetti in più: ogni scheda futura scritta in uno di
  quelli entra da sola.
- La stima resta distinguibile dal dato.

**Il prezzo, dichiarato.**
- **Le 52 restano aperte**, e questo ADR non finge il contrario. Si chiudono a
  mano, una per una, con lo strumento che propone il conto, ed è una sessione a
  sé, come il piano diceva.
- **Il derivatore scrive un campo su tre**, e gli altri due li propone soltanto.
  È poco, ed è deliberato: la parte che scrive è quella dove l'errore si vede.
- **La guardia PF1e è tarata su PF1e.** Per un 3.5 è severa, e ora che annota
  invece di respingere il rumore si vede nelle proposte.
- ⚠️ **Non tutte le righe della tabella per GS sono verificate.** Le righe
  GS 8 e 10-16 vengono dalla fonte; **GS 1-7 e 17-20 le ho interpolate io**, e il
  campo `PER_GS_VERIFICATE` lo dichiara: su una riga interpolata l'avviso lo dice,
  perché un giudizio duro non si dà su un numero che nessuno ha controllato.

**Cosa NON decide.** Non emenda ADR-0021 sulla forma del blocco né sul divieto di
un `Bestiario/dati/*.yaml` parallelo. Emenda **solo** §3, e solo per dire che la
derivazione dichiarata è ammessa **se supera un collaudo**, cosa che oggi non
succede per nessuna scheda.

## Emendamento — 2026-09-23: leggere prima di derivare vuol dire anche rileggere

Il principio di questo ADR era giusto e non è bastato. Il 2 settembre
`--apply-ts` ha scritto i TS di otto schede **dove la prosa li aveva già**,
perché il lettore non riconosceva ancora la forma dei dossier. Il giorno dopo
il lettore l'ha imparata, e i blocchi scritti non sono stati riletti. Per tre
settimane sei villain e PNG hanno avuto nel blocco TS diversi da quelli del DM,
in un caso di sette punti.

**Cosa si aggiunge.** Un campo del blocco che la prosa della stessa scheda
scrive diverso è un errore di `extract_statblocks --check`, e fa rossa la CI.
Il controllo non decide il verso: dice che uno dei due è rimasto indietro. Si
confrontano solo numeri, si saltano le note e le forbici («GS 17-19»).

**Il limite, dichiarato.** Dove la prosa tace il controllo non vede niente: è il
caso dei due razorfiend, i cui TS derivati contraddicono solo la formula dei
dadi vita. Per quelli la decisione è del DM (D10 e D11 di
`RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI` §9).

