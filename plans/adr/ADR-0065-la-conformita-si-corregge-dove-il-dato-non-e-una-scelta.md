# ADR-0065 — La conformità 3.5 si corregge solo dove il numero sbagliato è uno

- **Stato**: 🟢 accettata
- **Data**: 2026-09-23
- **Contesto**: ordine del DM, 2026-09-23 — *«correggi i 20 statblocchi in modo che pf-dado contenga davvero i dadi vita, mentre il danno dell'arma va nel campo adatto […] controlla che pf, tiri salvezza e attacco tornino con le caratteristiche, verificando dove le caratteristiche non sono scelte, e quindi si devono correggere gli statblocchi scrivendo quelli corretti»*
- **Estende**: [ADR-0064](ADR-0064-gli-attributi-si-scrivono-nel-bestiario.md), che ha scritto le caratteristiche; [ADR-0047](ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md) per le decisioni che restano al DM

---

## Contesto

Con le caratteristiche in tutti i 108 statblocchi si possono finalmente
verificare le identità del 3.5: pf nella fascia dei dadi vita, TS dalle
progressioni, BAB, lotta, attacco. Lo strumento è
`scripts/conformita_statblocchi.py`.

La prima esecuzione segnava **23 statblocchi da correggere**. Guardati uno per
uno, la maggior parte erano errori **del verificatore**: i DV razziali del
minotauro letti come totali, «Robustezza Migliorata» contata come Robustezza,
l'errata del retriever («la prosa diceva BAB +10») letta come dato, il tipo
umanoide trattato come se avesse sempre buona la Tempra. Ogni falso positivo è
diventato una prova in `test_conformita_statblocchi.py`.

Anche su quelli veri restava una domanda: **quale numero si corregge?** Se la
lotta non torna con la Forza, è sbagliata la lotta o la Forza?

## Decisione

### 1. Le caratteristiche nella riga `attributi` sono un'inferenza; i numeri sono del DM

Pf, TS, BAB, lotta e attacco li ha scritti il DM. La riga `attributi` l'ha
scritta uno script, e quando le due cose divergono **si corregge la riga**, non
lo statblocco. È il caso dei myconid: le loro caratteristiche venivano da una
bozza con un GS diverso, e la lotta e l'attacco scritti dal DM dicono
un'altra Forza. `genera_attributi` ora la ricava da BAB e lotta.

### 2. Un numero del DM si corregge solo se è l'unico che non torna

Si corregge quando **tutto il resto dello statblocco concorda** sul valore
giusto e l'aritmetica SRD lo determina senza ambiguità. Il gnoll guerriero 2
dichiara BAB +2: gnoll 2 DV (+1) più Warrior 2 (+2) fanno +3, e la sua lotta +5
e la sua ascia +5 **presupponevano già** +3. Il numero sbagliato era uno.

Si corregge il minimo: il BAB da cui dipendono lotta e attacco conta come **un**
errore, non tre, e quando cambia si portano con lui i numeri che ne derivano
(lo spadone del githyanki scende di 1 insieme al suo BAB).

### 3. Due numeri che puntano in direzioni opposte sono una decisione del DM

Il goblin warrior scrive For 9 e danno −1, ma lotta −3 e attacco +2 presuppongono
For 11: due numeri contro due. Una regola che sceglie qui sceglie a caso. Questi
casi vanno nella tabella `decisioni-dm` del piano (ADR-0047), e il verificatore
**la legge**: finché la riga è aperta, lo scarto esce come «decisione aperta»,
non come errore.

### 4. Uguale alla fonte non è un errore

Se lo statblocco trascritto dice quello che dice la sua fonte PCGen, lo scarto è
della fonte (un talento, un oggetto, una non-competenza che il verificatore non
modella) e correggerlo allontanerebbe la scheda dalla fonte.

### 5. Ogni correzione porta una marca, e si riproduce

Le correzioni di `pf-dado` sono **generate** e un cancello in CI le verifica
(`conformita_statblocchi.py --check`); quelle di pf, TS e BAB sono **undici,
fatte a mano una per una**, e ognuna porta sotto il blocco una riga
`[INFERRED — needs DM confirmation] correzione 3.5` con il valore vecchio, quello
nuovo e il conto SRD che li separa.

## Conseguenze

**Buone.**

- **`pf-dado` registra i dadi vita in tutti gli statblocchi.** Erano 46 su 95 a
  non farlo: 26 portavano il danno di un'arma, già presente in `attacchi`; 20 una
  parte sola dei dadi (`4d8` per un ogre con sei livelli da barbaro). **42 sono
  ricostruiti** dalla formula che la scheda scrive o dalle classi del tipo, **4
  sono tolti** (classi di prestigio non SRD: inventarne il dado sarebbe peggio
  del campo vuoto). La causa è chiusa: il lettore di settembre li rifiutava, ma
  nessuno aveva ricontrollato i blocchi scritti prima.
- **Sui 95 statblocchi verificabili**: 77 tornano, 3 sono uguali alla fonte, 7 sono
  decisioni aperte, **0 da correggere**, 8 hanno scarti di un punto su
  caratteristiche generate.
- **Il sospetto del DM sui template PF1e è stato misurato**: nessuno scarto si
  spiega con Advanced o Giant. I potenziati (Ghaurush, il bruto deforme, il
  razorfiend alfa) tornano, perché il template sta già nelle caratteristiche
  che il DM ha scritto.

**Il prezzo, dichiarato.**

- **13 statblocchi non si verificano**: classi di prestigio non SRD, tipo non
  dichiarato, umanoidi da 1 DV senza classe scritta. Dirlo è meglio che
  indovinare una progressione.
- **Il verificatore non modella** oggetti magici, la maggior parte dei talenti,
  i bonus razziali ai TS, la non-competenza nelle armi esotiche. Per questo un
  TS sopra l'atteso di 1-4 punti è accettato, e solo quello sotto è un errore.
- **Le 8 schede con caratteristiche generate** che non tornano di un punto
  restano come sono: lo scarto parla del generatore, e correggere lo statblocco
  per farlo tornare con un numero scelto sarebbe il contrario del punto 1.

## Fonti

- SRD 3.5: tipi di creatura (dado, BAB, TS buoni — l'umanoide «varia»), classi
  base e di prestigio, *Improving Monsters*, lotta e modificatore di taglia.
- PF1e Bestiary, Table 1–1, trascritta in `scripts/pf1e-statistiche-per-gs.yaml`.
- `Bestiario/pregen-pcgen/`: le fonti PCGen e SRD citate dalle schede.
