# ADR-0054 — Un archivio non è una copia, e un cancello non è una forma

- **Stato**: accettata (2026-09-17), **attuata**
- **Decide**: chi entra nel censimento degli statblocchi d'arco, e con quale criterio
- **Corregge**: il cancello introdotto da me il giorno prima (lotto 4d-5)
- **Non tocca**: la regola di `test_archivi_non_indicizzati.py` — chi **indicizza**
  continua a saltare gli archivi

---

## Contesto

Il lotto 4d-5 aveva aggiunto un cancello che cercava i documenti d'arco con
statistiche scritte in prosa, per garantire che nessuna creatura giocabile
restasse fuori dal pool degli incontri. Rimisurando il giorno dopo su richiesta
del DM — *«considera tutta la prosa davvero negli archi… vedi anche negli
archivi se è stato tralasciato qualcosa»* — il cancello si è rivelato sbagliato
**in due modi indipendenti**, e nessuno dei due era visibile dal suo interno.

### 1 · Conosceva una forma di statblocco su tre

Il matcher pretendeva il trattino, l'unica forma che avevo davanti scrivendolo:

| Forma | Dove | La vedeva? |
|---|---|---|
| `- CA: 22` | arco 09 (Torre, Torneo, Rhest) | sì |
| `**CA:** 22` | archi 07 e 08 | **no** |
| `**CA** 18` (senza due punti) | il Palio, l'Abbazia | **no** |

**Misura: 23 documenti visti su 38.** Fra i quindici che non si vedevano:
`ARC08-01-GUIDA-DM.md` (57 marche, la guida del DM della Battaglia di
Hammerfist) e — il caso che decide questo ADR — **un'avventura stand-alone
intera**, `10-stand-alone/L'Abbazia della Rotta Sicura`: 1.419 righe, un
appendice di statblocchi tutto suo, e **zero** voci nel Bestiario.

🔴 **Il difetto non è la larghezza del regex.** È che il cancello era tarato sul
campione che avevo sotto gli occhi e **dichiarava** una copertura che non aveva
misurato. È la forma d'errore di ADR-0053 — «non lo so» travestito da risposta
sicura — ricomparsa dentro il cancello che quella lezione doveva presidiare.

### 2 · Saltava gli archivi in blocco, e in `_ARCHIVIO/` c'erano i master

Il cancello escludeva `_ARCHIVIO/` con una riga (`if "_ARCHIVIO" in str(p):
continue`), ereditando la regola di `test_archivi_non_indicizzati.py`. Quella
regola è giusta **per chi indicizza**: archiviare dodici istantanee portò il
catalogo da 305 a 311 record con un doppione, ed è un difetto vero e misurato.

Ma il censimento non indicizza: **sorveglia**. E la prova che la distinzione
serviva era già scritta nel repo — `ARC07-MATRICE-VERSIONI.md` **dichiara
MASTER** sette file che stanno dentro `_ARCHIVIO/`:

| File in `_ARCHIVIO/` | Come la matrice lo dichiara |
|---|---|
| `PortaleForgia-P4-PianoTerra-COMPLETO-alternative.md` | **MASTER narrativo** (DM 2026-07-03) |
| `PortaleForgia-P4-PianoTerra-RICALIBRATO.md` · `Terros.md` | **MASTER di combattimento** — power-up VOLUTO (D8) |
| `PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md` | **MASTER** (eletto in B2) |
| `PortaleForgia-P5-DEFINITIVO-PARTE1/2.md` | **MASTER lungo** |
| `PortaleForgia-P5-FASTPLAY.md` | **MASTER da tavolo** |
| `PortaleForgia-P6-INTEGRAZIONE-Completa.md` | **MASTER parziale** (battaglia antica viva) |

Di tutti i file d'archivio con statblocchi, **cinque su cinque sono master
dichiarati**: non uno è davvero superato. Dentro ci stava `Terros.md` — lo
statblocco di un **boss da GS 15** che nessuno strumento raggiungeva.

## Decisione

**Tre criteri, tutti dichiarati, nessuno dedotto**, in `scripts/dmcore/censimento.py`.

1. **Le tre forme si riconoscono tutte**, e l'inline resta **stretto**: dopo la
   marca deve venire una cifra, un modificatore o il nome di un tiro salvezza
   (`**TS** Temp +7` non comincia per cifra). Allargarlo a «una parola
   qualunque» farebbe passare la prosa — e un matcher che riconosce tutto non è
   un cancello. Il controprova è nel test: la prosa della Torre resta sotto
   soglia.
2. **Gli archivi restano fuori dall'indicizzazione, i master dichiarati
   rientrano nella sorveglianza.** Chi decide non è un'euristica sul nome della
   cartella: è la matrice delle versioni, letta riga per riga. Forma di
   ADR-0041 (contare quel che è dichiarato) applicata alla provenienza.
3. **Un master d'archivio si rende raggiungibile con un POINTER, non
   indicizzandolo.** Il `source_file` del record resta dentro `Bestiario/`,
   quindi la regola dei doppioni non si tocca: `Terros.md` è raggiungibile e
   l'archivio continua a non produrre record.
4. **Un documento che porta numeri ma non creature si esclude *con il
   motivo*** (`FUORI_RAGGIO`): le schede dei PG dell'ARC-07, il sistema di
   combattimento di massa, le guide della Corona. Stessa disciplina di
   `perche_senza_scheda` in ADR-0053 — un'esclusione senza motivo scritto è
   indistinguibile da una dimenticanza, ed è esattamente così che l'Abbazia era
   sparita.

### Il corollario sui POINTER: un percorso si risolve, non si legge

Misurando è emerso un terzo difetto, della stessa famiglia. Il cancello
verificava l'aggancio **confrontando sottostringhe**, e undici voci del
Bestiario citavano la propria fonte così:

> `**Key stats**: → statblock in `08_.../ARC08-01-GUIDA-DM.md``

Un umano capisce quei puntini. `Path.exists()` no. Erano **POINTER che non
puntavano**, e il cancello li contava buoni. Altri sei citavano un percorso
sbagliato di un livello di cartella (`Bestiario/png/Lorana/Lorana.md`, quando il
file è `…/Lorana/Lorana/Lorana.md`).

**Adesso l'aggancio si risolve**: 130 citazioni, tutte aprono un file che c'è.

## Alternative scartate

| | Perché no |
|---|---|
| **Indicizzare gli archivi** | Disferebbe una decisione provata da un incidente vero (305 → 311 con un doppione). Il POINTER ottiene la raggiungibilità senza il costo |
| **Escludere `_ARCHIVIO` e basta, come prima** | Toglie dal raggio sette master dichiarati dal DM, fra cui un boss da GS 15. È il difetto che questo ADR chiude |
| **Un matcher generoso («qualunque parola dopo la marca»)** | Riconoscerebbe la prosa. È la lezione di ADR-0053 al contrario: un matcher permissivo non riduce l'ignoranza, la traveste |
| **Dedurre i master dal nome del file** | `-COMPLETO-alternative` *suona* superato ed è il MASTER narrativo; `-RICALIBRATO` suona provvisorio ed è il master di combattimento. Il nome mente, la matrice no |
| **Spostare i master fuori da `_ARCHIVIO/`** | Sarebbe più pulito, ma muove sette file che decine di documenti citano per percorso. Costo alto, guadagno nullo rispetto al POINTER |

## Conseguenze

**Quel che si guadagna.** Il pool degli incontri passa da **352 a 397 voci** (372 col censimento, poi D18), e
le venti nuove non sono comparse: sono l'intero cast dell'Abbazia della Rotta
Sicura (Padre Anselmo Grifo GS 9, le Tre Sorelle del Frangente, i corsari della
*Zanna di Bruma*), **Terros l'Antico GS 15**, **Skullcrusher il Nero** —
capostipite della stirpe di Fauci di Palude — **Zog'tar Deatheye GS 14**, e i
mostri della ceremorfosi dell'ARC-04. Tre cancelli nuovi, tutti provati
all'indietro: rimettere l'esclusione cieca, restringere il matcher e riabbreviare
un percorso diventano tutti e tre rossi.

**Quel che si perde.** `censimento.py` va tenuto vero: se il DM adotta una
quarta forma di statblocco, il cancello tace di nuovo. Il presidio possibile è
scritto nel test — la prova all'indietro gira **sul file vero dell'Abbazia**,
non su un fixture, quindi un restringimento futuro si vede subito; una forma
nuova, no.

✅ **Le due incoerenze che questo lotto aveva dichiarato aperte sono state
decise dal DM il 2026-09-17**, e la decisione è scritta dove si legge:

| | Deciso |
|---|---|
| **Skullcrusher il Nero** — `CR 11` in un file, **GS 12** in un altro | **GS 12**; l'archivio porta l'errata accanto alla riga |
| Il boss del Piano della Terra — **GS 13** narrativo contro **GS 15** ricalibrato | **GS 15 (Terros)** è il boss che si gioca; la cornice a GS 13 resta raggiungibile ma dichiara di non essere un secondo mostro |

🔎 **E correggendo Skullcrusher il cancello di D18 ha trovato un errore mio**: la
voce che avevo appena scritto puntava a `PortaleForgia-P6-INTEGRAZIONE-Completa.md`,
che il drago lo **nomina** soltanto. I numeri (CA 27, PF 240, soffio 12d4 CD 24)
stanno in `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`, e `ERRATA-ARC07-35-Verification.md`
§2.3 li dichiara per esteso. Il cancello lo ha visto perché contava **due**
«Skullcrusher il Nero» nel catalogo.

## D18 — spezzare per intestazione, verificando che non esistano già

**Decisa dal DM il 2026-09-17**, nella forma che il lotto aveva proposto come (a).
`build_monster_catalog.py` produceva **un record per file**: un documento con
dodici creature diventava una voce intitolata al documento, con un GS arbitrario.

**19 → 8**, e il pool passa da **372 a 397**. Quel che ne è uscito non sono
comparse: gli **otto fantini del Palio**, i **Sicari di Sonjak**, il Gonfaloniere
Aldemar Vosk, la Drow Chierica di Lolth, gli esempi d'onda di Rethmar.

⚠️ **La deduplica è la parte che poteva far danno**, ed è ancorata a un fatto
dichiarato: si confrontano i nomi **solo** dentro l'insieme delle voci del
Bestiario che citano *quel* documento come `Source`. Il legame documento↔voce
l'ha scritto qualcuno; la somiglianza sceglie solo *quale* voce corrisponde a
*quale* intestazione, dentro un insieme già ristretto a mano. È il modo di
rispettare ADR-0053 senza rinunciare a dedurre.

🔴 **E il rischio opposto ha il suo presidio.** Togliere il record di file per
«fare pulizia» toglierebbe creature dal pool quando il documento ne contiene una
che nessuna voce nomina. Il record sparisce **solo** quando ogni creatura che il
documento nomina ha già la sua voce: gli **otto** che restano sono quelli dove
non è vero, e vanno bene così.

🐛 Due difetti nei nomi generati, trovati misurando: la numerazione del Palio è
**multi-livello** (`### 3.2 Drow Chierica`) e lasciava nomi che cominciavano per
cifra; e la coda tagliata lasciava parentesi mai chiuse («Aldemar Vosk (LN»).
Entrambi hanno un cancello.

## Riferimenti

- `plans/PIANO-RIPRESA-PR-ABBANDONATE.md` §4.8.12 — il lotto, misure e validazione
- [ADR-0053](ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) — la chiave si dichiara; qui si dichiara la provenienza
- [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md) — la forma «contare quel che è dichiarato, e un gate lo verifica»
- [ADR-0021](ADR-0021-statblocchi-machine-readable.md) — i numeri sono un dato, e non se ne tiene una seconda copia
- `scripts/dmcore/censimento.py` · `scripts/tests/test_censimento_forme.py`
- `scripts/tests/test_archivi_non_indicizzati.py` — la regola che questo ADR **non** tocca
