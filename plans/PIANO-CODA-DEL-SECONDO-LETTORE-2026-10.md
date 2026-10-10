# Piano: la coda del secondo lettore (cosa è fatto, cosa resta)

> **Metodo.** Chiude [ADR-0079](adr/ADR-0079-un-secondo-rilevatore-per-la-prosa.md)
> (opzione B) e dice cosa resta, in ordine di urgenza, con chi può farlo. Nasce
> perché la misura ha trovato difetti veri che **non ho corretto**: o perché la
> scelta è del DM, o perché sono un lotto di contenuto da fare a parte.
>
> **Stato**: lotto di infrastruttura chiuso (PR #214); coda aperta.

## 1. Fatto (PR #214)

- [x] Misura di Vale, LanguageTool e proselint sul repo, a due giri, con un secondo
      lettore cieco (κ 0,53) e un corpus di richiamo scritto da un terzo
      ([RICERCA](RICERCA-SECONDO-RILEVATORE-VALE-LT-PROSELINT-2026-10.md))
- [x] ADR-0079 accettata, opzione B: LanguageTool è un **secondo lettore
      facoltativo**, locale, fuori dalla CI
- [x] `ciclo_prosa.py segnala --languagetool URL`: tre regole, numeri di riga
      giusti (offset UTF-16), rifiuta ogni indirizzo non locale
- [x] `scripts/avvia_languagetool.sh`, voce nel manifest, `java` e `mvn` tra i
      binari opzionali
- [x] `validate_lingua`: avviso sull'apostrofo al posto dell'accento (156 righe)
- [x] `validate_prosa`: il foglio di stile non scarta più `Hellas/druidi` né una
      riga con una freccia lontana; 14 righe di grafie sbagliate corrette in 6 file

## 2. Da fare, in ordine di urgenza

**1. Il genere di *Torre* nel modulo del Palio (decide il DM).** Il modulo scrive
*della Torre* 15 volte e *del Torre* 12, e *alla Civetta* 8 volte contro 1 *alle
Civetta*. È prosa che il master legge a voce: il tavolo sente l'incoerenza. Una
domanda sola al DM («la contrada è *la Torre* o *il Torre*?»), poi 12 righe da
uniformare in `STANDALONE-Il-Drappo-di-Tarsilia/`. Nello stesso passo gli altri
quattro difetti di concordanza che il secondo lettore ha confermato: *del Mano
Rossa* ×3 (`ESPANSIONE NARRATIVA POST-HAMMERFIST.md`, righe 373, 439, 506), *nel
Tana dei Minotauri* (riga 20 dello stesso file), *dalla Conoscenze*
(`EST-FASE4-SAARVITH-REGIARIX-BOSS-CR13.md`, riga 77). Dopo, rilanciare
`ciclo_prosa.py segnala --languagetool` sui file toccati e controllare che i
rilievi veri siano a zero.

**2. Gli accenti del Bestiario (nessuna decisione da prendere).** 140 delle 156
righe dell'avviso sull'apostrofo stanno in `Bestiario/`, e 67 sono lo stesso
blocco («Questa voce esiste perche' `build_monster_catalog.py`… non e'
raggiungibile da nessuno strumento») copiato in 57 schede: non c'è un generatore
nel repo, è testo scritto a mano. Un lotto meccanico: sostituire solo le forme
della lista di `validate_lingua` sulle righe segnalate, rilanciare il validatore
(gli avvisi calano di 140), `fase1.py --check` prima, `pregen-pcgen/` escluso
(sola lettura). Il lotto tocca 57 schede: va in una PR a sé.

**3. Il campo *Etichetta regia* troncato in `PROMPT-IMMAGINI-07ILP.md`
(decide il DM sul come).** 32 righe del file hanno il campo tagliato dopo una
parentesi chiusa (*«Etichetta regia: isolamento).»*). È un difetto sistematico:
cercare chi compila quel file (`extract_scene_prompts`?) prima di correggere a
mano, altrimenti la prossima generazione lo rifà. Non urgente per il tavolo: sono
prompt per le immagini.

**4. La *d* eufonica (decide il DM).** *legato a Aegis Fang*, *a area*: il repo non
ha una norma. Se il DM la vuole (*ad* solo davanti alla stessa vocale), va
scritta in `editorial-standards.md`, registrata in
`skills/REGISTRO-NORME-EDITORIALI.md` e misurata; altrimenti resta com'è. Una
norma senza misura non esiste (ADR-0056).

**5. Il richiamo grammaticale resta cieco.** Accordo di verbo e di aggettivo,
congiuntivo, ausiliare: 0 su 40 per LanguageTool e per i rilevatori del repo. Non
si risolve con uno strumento. Resta il lettore a freddo di
`rumblingstone-playtest` (ADR-0075) e, quando serve una verifica in più, il
secondo lettore di questo piano. Da rivedere se le regole italiane di
LanguageTool migliorano: la procedura sta nella ricerca e si rifà in un'ora.

## 3. Quando usare il secondo lettore

Su un master o un handout **prima** di dichiararlo definitivo, come il lettore a
freddo: `scripts/avvia_languagetool.sh` in un terminale, poi
`python3 scripts/ciclo_prosa.py segnala FILE --languagetool http://127.0.0.1:8081`.
Un rilievo su due è falso: si legge, non si applica. Non entra nel punteggio e
non è un cancello.

## 4. Per aprire una chat pulita

Il primo messaggio, da incollare:

> Leggi `plans/PIANO-CODA-DEL-SECONDO-LETTORE-2026-10.md` §2. Parti dal punto 1:
> chiedimi se la contrada è *la Torre* o *il Torre*, poi uniforma le 12 righe del
> modulo del Palio e correggi i quattro difetti di concordanza elencati. Prima
> `python3 scripts/fase1.py --check` sui file; apri una PR in bozza.
