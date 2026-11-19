# Punti chiave, grafo degli eventi, Prolog e RAG per «chi sa cosa»: esito della misura

Forma: spiegazione. Data: 2026-11-12. Fa seguito ad
[ADR-0125](../../adr/ADR-0125-la-coerenza-della-storia-si-verifica-contro-state-yaml-solo-sui-fatti-strutturati.md)
e al suo «Da rivedere se» (il tempo nelle righe di §4).

## La domanda

Il DM, il 12 novembre: *«mettendo dei punti chiave, questo Prolog potrebbe
migliorare usando anche un grafo degli eventi? Puoi verificare e misurare il
miglioramento usando anche un sistema RAG, tutto integrato?»*

## In breve

| domanda | risposta misurata |
|---|---|
| I punti chiave si ricavano da state.yaml? | **Solo in parte.** 6 righe di §4 su 31 hanno un giorno, e 2 di queste sono relative a un altro evento. Gli altri giorni li ho dovuti dedurre (`[INFERRED]` in `eventi.yaml`). Metterli nel canone è una scelta del DM |
| Con i punti chiave, Prolog o clingo trovano di più? | **No.** Python, SWI-Prolog e clingo danno le stesse violazioni: 29 su 29 sui mutanti e 6 su 6 su main, in pochi millisecondi. Prolog è più corto da scrivere (9 righe contro 26), ma è un binario in più. Per la regola di Jfs sullo standard di fatto si resta in Python |
| Il grafo e la regola ricorsiva servono? | **Sì, poco ma davvero.** 2 mutanti su 14 si vedono solo seguendo chi informa chi (Zalkatar da Sethrax, Brenna da Tempestas). La ricorsione trova anche **3 catene rotte dentro state.yaml** (sotto) |
| Il RAG supera il collo di bottiglia della parafrasi? | **Il recupero sì, la lettura no.** Con 20 candidati il recupero trova 22 mutanti su 25, comprese 8 parafrasi su 11. Il lettore locale (Qwen2.5-3B) però dice SÌ a 15 domande giuste su 22 e anche a 19 su 59 con il PNG sbagliato. Su main **0 rilievi veri su 23 righe** |
| Tutto integrato (regole + RAG) | parafrasi da 0/11 a **5/11**, piane invariate a 13/14; in cambio arrivano 42 rilievi in più sul corpus coi mutanti, e su main sono tutti falsi |

## Il banco

- **`eventi.yaml`**: il grafo, che non è canone.
  - Contiene 15 fatti con la loro origine (il giorno in cui diventano veri) e 22 righe «sa», di cui 6 per catena (`informato_da`, `ritardo`).
  - Ha poi 16 righe «non sa», gli alias dei PNG e le finestre in giorni di ogni file (dagli archi di state.yaml).
  - Ogni giorno dedotto dice da dove viene.
- **`grafo.py`**: le regole, identiche in tre motori:
  - `conosce` ricorsiva (punto fisso in Python, tabling in Prolog, chiusura in clingo);
  - T0, il fatto citato prima della sua origine;
  - T1, il PNG che sa prima del suo giorno, anche per catena;
  - T2, la catena rotta;
  - T3, il PNG che sa ciò che non sa.

  C'è anche l'estrattore a regole: alias del PNG, parole chiave del fatto, verbo di conoscenza, un solo PNG nella frase, niente futuro o condizionale.
- **`estrai_rag.py`**: il RAG.
  - Recupero ibrido: BM25 più `intfloat/multilingual-e5-small` (MIT), fusione per rango reciproco, solo sulle scene in cui la regola può scattare.
  - Lettura con `Qwen/Qwen2.5-3B-Instruct` (Apache-2.0) su CPU, in modalità greedy. Le risposte sono in `misure/cache-llm.json`, quindi il giro si ripete identico.
  - Le citazioni accettate vanno alle stesse regole di `grafo.py`.
  - La descrizione del PNG viene da state.yaml (`villain`), non è scritta per i mutanti.
- **`muta_grafo.py`**: 25 mutanti, ognuno in un file diverso:
  - 14 in forma piana e 11 in parafrasi;
  - per regola: T0 7, T1 7, T1 per catena 4, T3 7.
- **Corpus storico**: non c'è. Nei commit e nei piani di revisione non ho trovato incoerenze «chi sa cosa» corrette in passato. Quindi la misura poggia sui mutanti e sulla lettura di main.

## I numeri

### Mutanti

| estrattore | piana | parafrasi | rilievi fuori dai mutanti |
|---|---:|---:|---:|
| regole (regex) | **13/14** | 0/11 | 3 |
| RAG, 5 candidati | 7/14 | 3/11 | 7 |
| RAG, 20 candidati | 9/14 | 5/11 | 39 |
| regole + RAG 20 | 13/14 | **5/11** | 42 |

Per gruppo, con le regole: T0 4/4, T1 4/4, T1 per catena 2/2, T3 3/4. Il mutante perso nomina due PNG nella stessa frase («Mira Serani scopre che Lorana è viva»), e l'estrattore la scarta apposta. Nessuna parafrasi passa.

### Il lettore del RAG, solo sui 22 mutanti recuperati

| domanda | SÌ |
|---|---:|
| sul PNG giusto | 15/22 (68%) |
| su un altro PNG, non nominato nella frase | 19/59 (32%) |

Il lettore confonde «la frase parla del fatto» con «questo PNG lo sa». Dice NO anche a frasi piane come «Lorana scopre che sua figlia è stata uccisa e sostituita da un'aranea».

### Precisione su main

| estrattore | righe segnalate | vere |
|---|---:|---:|
| regole | 3 (più 3 catene rotte nel grafo) | 1, più le 3 catene |
| RAG, 20 candidati | 23 | 0 |

I falsi del RAG su main sono di tre tipi:
- il Seme di Varis letto come Seme di Porta;
- «Sal sa già» attribuito al Conte Valerius;
- tabelle di DM con l'elenco degli artefatti lette come «Ushgar sa quali artefatti».

### Motori

Python, Prolog e clingo danno insiemi di violazioni identici: 6 su main e 29 sul corpus coi mutanti. I tempi sono 0, 21 e 25 ms su main, e 0, 23 e 17 ms sui mutanti.

## Che cosa ha trovato, da portare al DM

1. **Tre catene rotte in state.yaml §4**, trovate dalla regola ricorsiva:
   - Salvatore sa chi sono i Custodi e quali artefatti portano «dal briefing del Collezionista», ma §4 non dice che il Collezionista lo sappia (sa solo dell'Anello di Artemis);
   - Brenna sa che Lorana è viva «dai rapporti di Tempestas», ma §4 non dice che Tempestas lo sappia.

   O §4 è incompleto, oppure la fonte va cambiata.
2. **`ARC07-DEF-1-PIANO-TERRA-TERROS.md:69`**: «I Custodi Eterni sono entrati nel Portale». In ARC-07 il titolo non esiste ancora, perché Re Thorek lo dà alla Cerimonia delle 100 Asce, al Day 21 (ARC08-12-CRONOLOGIA-MARCH-CLOCK). Può essere un'abbreviazione del DM o un anacronismo.
3. **I punti chiave di §4**: 25 righe su 31 non hanno un giorno di gioco. Senza giorni le regole T1 e T2 lavorano su date dedotte.

### Correzione del 12 novembre: la Cerimonia è al Day 21

Nella prima corsa avevo messo l'origine del titolo di Custodi Eterni al Day 19, la fine della battaglia. La cronologia approvata (ARC08-12, nota 1) la mette alla Cerimonia del Day 21. Ho corretto `eventi.yaml` (origine del fatto, righe «sa» collegate, finestre di ARC-07 14-19 e ARC-08 1-21) e rifatto tutte le corse: i numeri delle tabelle sopra sono quelli **dopo** la correzione e non sono cambiati (mutanti uguali; su main ancora 6 violazioni dalle regole, motori uguali; RAG 23 righe, 0 vere).

La correzione ha invece fatto emergere un fatto nuovo su state.yaml: la lettera di Brenna usa il titolo e la sua consegna è datata al Day 21 (e al Giorno 22 nello stesso file). È la domanda D1 di [PROPOSTA-GIORNI-CHI-SA-COSA.md](PROPOSTA-GIORNI-CHI-SA-COSA.md).

## Aggiornamento del 19 novembre: il lettore da 7B sulla RTX 4050

Il DM ha lanciato il kit sull'ASUS con la RTX 4050: `leggi_ollama.py` con `qwen2.5:7b` via Ollama, 636 risposte su 636 in circa 2 minuti (0,24 s a domanda). Il kit avverte che solo l'87% del modello stava in VRAM, quindi il tempo vale con quella riserva. Le risposte sono in `misure/risposte-qwen2.5-7b.json`; le due letture complete (`main-rag-7b.json`, `mut-rag-7b.json`) restano fuori dal repo, in `/mnt/project-files/prove-4050-risultati/2026-11-19/`.

| misura | lettore 3B (CPU, 12/11) | lettore 7B (4050, 19/11) |
|---|---:|---:|
| SÌ sui 560 candidati di main | 35 (6%) | 499 (89%) |
| righe segnalate su main dal RAG | 23 | 302 (673 rilievi) |
| di cui vere | 0 su 23 | non giudicate una per una; 6 prese a caso, 6 false |
| mutanti trovati (RAG da solo) | — | 21 su 25, parafrasi 8 su 11 |
| rilievi fuori dai mutanti | 42 (integrato) | 566 |
| SÌ sulle righe dei mutanti recuperati | 34 su 81 | 78 su 79 |

**Il 7B non entra come lettore.** Trova quasi tutti i mutanti solo perché dice SÌ quasi a tutto:
- sulle 79 domande fatte sulle righe dei 21 mutanti recuperati risponde SÌ 78 volte. Al massimo 21 di quelle domande sono sul PNG giusto, quindi col PNG sbagliato dice SÌ almeno 57 volte su 58 (98%). Il criterio chiedeva al massimo il 5%;
- fuori dai mutanti dice SÌ a 432 domande su 481;
- su main dice SÌ a 499 candidati su 560. La prima riga dell'elenco è la voce d'indice «Sonjak / Matrona Sajak … Matrona Drow, comanda forze sotterranee», letta come «Sonjak sa delle gemme».

Il 3B sbagliava dicendo troppi NO, il 7B sbaglia dicendo troppi SÌ: in tutti e due i casi il lettore non distingue «la frase parla del fatto» da «questo PNG lo sa».

Limiti di questa misura:
- le 302 righe su main non sono state lette una per una: la precisione «0 su 6» è un campione, non un conteggio. Con l'89% di SÌ su candidati presi per somiglianza non può però arrivare al 70% del criterio;
- la divisione fra PNG giusto e PNG sbagliato sui mutanti è un limite calcolato (almeno 98%), non un conteggio riga per riga;
- i testi letti sono quelli del commit 35248a20, non la testa di oggi;
- un solo modello da 7B, a 4 bit, con la domanda scritta per il 3B. Una domanda diversa o un 12B potrebbero cambiare la lettura, ma il 12B non sta nei 6 GB della 4050.

## Onestà sul banco

- **I giorni dedotti sono miei.** Le regole temporali sono esatte quanto i giorni che ricevono. Ne ho dedotti 16; sono in `eventi.yaml` con la loro fonte.
- **I mutanti li ho scritti io, sapendo come cercano le regole.** Il 13/14 piano è un tetto. Le parafrasi sono la stima onesta, e lì le regole fanno 0/11.
- **Le descrizioni dei fatti per il RAG le ho scritte io** (`FATTI_IT`), dopo aver scritto i mutanti. Le ho tenute neutre, ma il rischio di averle accordate ai mutanti c'è.
- **Due lettori, 3B su CPU e 7B sulla RTX 4050** (aggiornamento del 19/11, sopra). Nessuno dei due raggiunge il criterio. Il 12B di ADR-0089 non sta nei 6 GB della 4050.
- **La misura su main è piccola** (6 e 23 righe). Dice la direzione, non una percentuale stabile.

## Che cosa ne segue

- **Il motore logico non entra.** Con i punti chiave le regole diventano davvero temporali e ricorsive, ma Python le fa uguali, con zero dipendenze. È la stessa conclusione di ADR-0124, ora misurata anche con il tempo.
- **Il grafo con i giorni vale**, ma come dato e non come motore. Se il DM dà un giorno alle righe di §4 e una fonte che punta a un altro PNG, T1 e T2 diventano regole corte da portare in `coerenza_campagna --state`, come S1-S7.
- **Il RAG non entra, né con il lettore da 3B né con quello da 7B**: 0 rilievi veri su 23 su main col 3B; col 7B 302 righe segnalate, 6 su 6 false nel campione.
  - Il recupero funziona (8 parafrasi su 11 fra i primi 20 candidati), quindi il pezzo da rimisurare è solo il lettore.
  - Criterio per riprovare: sul banco dei mutanti almeno 90% di SÌ sulle domande giuste, al massimo 5% di SÌ col PNG sbagliato, e su main almeno 70% di precisione.
  - Il 19/11 il 7B sulla 4050 non l'ha raggiunto (almeno 98% di SÌ col PNG sbagliato). Riprovare ha senso solo cambiando la domanda al lettore o la macchina, non rilanciando lo stesso banco.

## Come si rifà

```bash
python3 grafo.py chiusura                     # chi sa cosa da quando, catene rotte
python3 grafo.py regex --json > misure/main-regex.json
python3 grafo.py motori misure/main-regex.json   # Python = Prolog = clingo
python3 muta_grafo.py prepara /tmp/mutato
python3 grafo.py regex --radice /tmp/mutato --json > /tmp/mut-regex.json
python3 muta_grafo.py valuta /tmp/mutato /tmp/mut-regex.json
# RAG: venv con torch (CPU), transformers, sentence-transformers
python estrai_rag.py --radice /tmp/mutato --out /tmp/mut-rag.json --k 20
python3 muta_grafo.py valuta /tmp/mutato /tmp/mut-regex.json /tmp/mut-rag.json
```

Il lettore su un'altra macchina (per esempio la RTX 4050 con Ollama), senza torch:

```bash
# nel container: recupero e domande
python estrai_rag.py --radice /tmp/mutato --out /tmp/x.json --k 20 \
  --modello ollama:qwen2.5:7b --domande-out misure/domande-ollama.json
# sulla macchina con Ollama (solo stdlib)
python3 leggi_ollama.py misure/domande-ollama.json --modello qwen2.5:7b --out misure/risposte-qwen2.5-7b.json
# di nuovo nel container: le risposte entrano in cache, la lettura non carica modelli
python estrai_rag.py --radice /tmp/mutato --out /tmp/mut-rag-7b.json --k 20 \
  --modello ollama:qwen2.5:7b --unisci misure/risposte-qwen2.5-7b.json
```

Dipendenze di laboratorio, fuori dal pacchetto:
- `swi-prolog-nox` (9.0.4, apt);
- `clingo==5.8.3`;
- `torch` 2.15 CPU;
- `transformers` 5.22;
- `sentence-transformers`.
