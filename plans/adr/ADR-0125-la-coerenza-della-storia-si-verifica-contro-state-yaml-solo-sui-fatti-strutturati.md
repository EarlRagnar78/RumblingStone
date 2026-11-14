# ADR-0125 — La coerenza della storia si verifica contro state.yaml, e solo sui fatti che state.yaml ha come campi

**Stato**: accettata (2026-11-12, card del DM «Solo le regole precise, in testing»)
**Data**: 2026-11-12
**Decisione-fonte**: il DM (Jfs), 2026-11-11, nel thread della #378: *«L'idea che ha dato inizio al thread ha senso applicarla per la parte di generazione e coerenza della storia?»*; poi la card «Sì, thread separato».
**Rapporti**: applica alla storia il pattern di [ADR-0124](ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) (regola, atteso, ha, `file:riga`); si appoggia ad [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) (`state.yaml` è il master dei fatti) e ad [ADR-0067](ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md). Misure in [plans/esperimenti/coerenza-storia-2026-11-12/ESITO.md](../esperimenti/coerenza-storia-2026-11-12/ESITO.md).

## Contesto

Per la storia c'erano già due controlli deterministici. `coerenza_campagna
fatti` confronta la prosa con la prosa (due valori diversi per la stessa
entità) e non sa quale è giusto. `validate_state` controlla `state.yaml` ma
non legge la prosa. Mancava il pezzo in mezzo: la prosa contro il canone
strutturato, con un valore atteso da rimandare a chi scrive.

Banco: 35 incoerenze di storia già trovate e corrette nel progetto, un
prototipo con sette regole, il replay sui commit prima delle correzioni, 37
mutanti, la lettura di ogni rilievo su main.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Regole Python con àncora su `state.yaml`, solo sui campi che ci sono** (scelta) | dice `atteso`; 18 mutanti piani su 19; ha trovato su main un residuo di 4 mesi (Day 40 nel playbook) che nessun cancello vedeva | aggiunge 4 difetti storici su 35; 1 parafrasi su 18; precisione 7 su 13 su main |
| Strutturare altri fatti in `state.yaml` (numeri delle armate, anni del viaggio, «chi sa cosa» con il tempo) per coprire i K2 | 8 difetti storici in più diventerebbero deterministici | è canone nuovo: il tempo di §4 e i numeri di §2 li decide il DM, non un lotto d'infrastruttura (R7) |
| Prolog o clingo sul grafo degli eventi | ricorsione e regole temporali dichiarative | nessuna delle 35 incoerenze chiedeva una regola ricorsiva o temporale; §4 non ha il tempo, quindi la condizione di ADR-0124 per riaprirli non c'è |
| NLI o giudice LLM sulla prosa | legge le parafrasi | NLI già misurata e scartata (28 delle prime 30 sono rumore); un giudice LLM non è deterministico e va contro ADR-0067 |

## Decisione

1. **Per la storia vale il pattern di ADR-0124**: ogni verificatore che un
   LLM chiama restituisce `regola`, `atteso`, `ha`, `file`, `riga`. L'atteso
   viene da `campaign/state.yaml`, mai da un altro file di prosa.
2. **Si verificano solo i fatti che `state.yaml` ha già come campi.** Per gli
   altri il verificatore tace e lo dice (`non_verificabili`): oggi «chi sa
   cosa», 31 righe su 31 senza tempo.
3. **Nessun motore logico e nessun modello** per la coerenza della storia: la
   misura dice che il collo di bottiglia è leggere il fatto, non ragionarci.
4. **Le regole precise entrano nel repo, le altre restano in laboratorio**
   (card del DM del 2026-11-12, «Solo le regole precise, in testing»). S1
   (arrivo dell'orda), S5 (portatore), S6 (modifiche permanenti) e S7 (echi
   armati senza scena) stanno in `scripts/coerenza_campagna.py fatti --state`,
   in canale testing ([ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)) e nel server MCP in sola
   lettura. Sui mutanti piani e sul replay delle «−2 COS» danno gli stessi
   rilievi del prototipo. S2, S3 e S4 restano in
   `plans/esperimenti/coerenza-storia-2026-11-12/` finché la precisione non
   passa. Il server MCP mette ora le opzioni di un sottocomando dopo il suo
   nome, nell'ordine del manifest: prima `coerenza_campagna` via MCP rispondeva
   solo con l'errore d'uso.
5. **Non è un cancello.** Una frase d'autore sfugge quasi sempre, quindi il
   verde non vuol dire coerente. Il DM che legge resta il controllo vero
   (vedi la lettura scena per scena del 2026-11-02).

## Conseguenze

- Chi genera un master nuovo (un LLM via MCP, o il DM) riceve «atteso 42,
  trovato 40, `file:riga`» invece di «42 e 40 si contraddicono».
- Ogni nuovo campo strutturato di `state.yaml` diventa verificabile a costo
  basso, con una regola di poche righe.
- Si rinuncia a coprire le parafrasi e le incoerenze di struttura (generazioni
  di file, sequenze di eventi, fazioni fuse): 13 delle 35 storiche restano al
  giudizio.
- Se l'àncora è sbagliata il verificatore la difende (caso del pegno del
  Rituale 3, 2026-08-06).

## Aggiunta del 2026-11-13: S8, le tattiche contro la scheda

Stesso criterio del punto 4 (solo regole precise, in canale testing), con
un'àncora diversa: non `state.yaml` ma la scheda, letta da `verifica_scheda
--fatti` ([ADR-0126](ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md)).
`coerenza_campagna.py fatti --tattiche` segnala un incantesimo (in corsivo) o
un talento (con le maiuscole, o di più parole anche in minuscolo) che le
«Tattiche» di una scheda del Bestiario nominano e che la scheda non ha, né fra
i fatti né scritto altrove nel file (pozioni, pergamene, capacità magiche).

- **Misura su main (3cc11aee)**: 0 violazioni su 220 menzioni in 60 schede.
  Prima dei filtri erano 9, tutte false, lette una per una: nomi fra parentesi
  che il normalizzatore toglieva (5), «la Corona» presa per un talento, una
  nota di correzione del DM, l'incantesimo di chi attacca la creatura («contro
  *polvere luccicante*»), l'incantesimo che il padrone passa alla cavalcatura
  con condividere incantesimi.
- **Mutanti** (`muta_tattiche.py`, 569): la scheda perde ciò che la tattica
  usa, 181 visti su 183; la tattica usa ciò che la scheda non ha, 178 su 180;
  scambio fra due incantesimi della scheda, 0 falsi allarmi su 26. Parafrasi:
  talento di più parole in minuscolo 60 su 60; incantesimo senza corsivo 0 su
  60; talento di una parola in minuscolo 0 su 60.
- **Limiti**: i mutanti usano lo stesso dizionario della regola, quindi la
  misura è ottimistica. Un nome che è anche una parola comune della scheda
  («velocità», «fendere») passa sempre, perché «scritto altrove» lo assolve
  (4 mutanti su 363). Si leggono solo i file con una scheda sola (5 del
  Bestiario ne hanno di più) e non i master degli archi, dove le tattiche
  rimandano a una scheda in un altro file (4 falsi allarmi su 4 nella prova).
  «Descrizione» non si legge: 7 schede su 60 ne hanno una e nessuna nomina
  regole. Non dice se la tattica è buona, solo se usa ciò che c'è.
- **Scartato con la misura**: leggere anche gli incantesimi senza corsivo.
  Su main 32 menzioni in più e 2 falsi allarmi su 2 («un muro di forza» dei
  PG, «soffio di fuoco» del drago), nessun errore vero trovato.

## Aggiunta del 2026-11-13: i giorni di «chi sa cosa» e la regola T2

Il DM ha chiuso le quattro domande della proposta
(`plans/esperimenti/grafo-eventi-2026-11-12/PROPOSTA-GIORNI-CHI-SA-COSA.md`) e
la riga 69 di ARC07-DEF-1. Le righe di `conoscenze` in `state.yaml` hanno due
campi facoltativi: `dal_giorno` (giorno del March Clock, 0 = prima del Day 1)
e `informato_da` (`png_id`). `validate_state` (R10) vuole che `informato_da`
sia nell'anagrafica. `coerenza_campagna fatti --state` ha la regola **T2**:
chi informa un PNG sa qualcosa non dopo di lui.

- **Che cosa ha deciso il DM e che cosa no.** Decisi: la lettera di Brenna
  (Thorik comandante, consegna al Giorno 22), Norro e il titolo (dal Giorno
  23), Brenna e Lorana (direttamente, dal 16-18), «I Rumbling Stones» in
  DEF-1, e il Collezionista che sa dei Custodi e degli artefatti dalla sua
  gilda, dal Giorno 22 (riga nuova). Dei 27 giorni **proposti** il DM ne ha confermati 22 su card; i cinque a
  fiducia bassa restano senza giorno: un buco contato vale più di un giorno
  indovinato.
- **T1 non entra.** La regola temporale sulla prosa («un PNG mostra di sapere
  prima del suo giorno») ha bisogno di tre cose che `state.yaml` non ha: una
  chiave per il fatto, gli alias del PNG e la finestra di giorni di ogni file.
  Resta in `grafo.py`, dove su main dava 1 rilievo vero su 3.
- **T2 è debole.** Senza una chiave per il fatto il confronto è fra PNG: vede
  l'informatore che non sa nulla in tempo, non quello che sa in tempo un'altra
  cosa. Su main 0 violazioni; la catena che il laboratorio aveva trovato
  (Tempestas → Brenna) è stata sciolta dal DM, non dalla regola.
- **Non verificabili**: le righe senza `dal_giorno`, 6 su 33: i Tiri Kitor,
  che non sanno nulla, e le cinque non confermate.

**Da rivedere se**: il DM dà il tempo alle righe di §4 «chi sa cosa» (allora
le regole diventano temporali, e Prolog o clingo vanno rimisurati come dice
ADR-0124); oppure su 30 rilievi letti in canale testing la precisione delle
regole promosse scende sotto il 70%; oppure un master scritto via MCP mostra
che l'LLM non corregge con `atteso` meglio che con il solo messaggio.
