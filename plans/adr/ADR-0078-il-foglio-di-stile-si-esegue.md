# ADR-0078 — Il foglio di stile si esegue

- **Stato**: accettata
- **Data**: 2026-10-03
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-10-03: *«controlla se le skill del repo per
  la scrittura e revisione della prosa usano i migliori meccanismi per
  l'automazione, anche cercando in web le migliori soluzioni attuate in ambito
  di editoria professionale da Wizards of the Coast e Paizo, che usino
  strumenti e tecniche compatibili con le licenze di questo repo. Se ci sono
  inseriscile e misura l'incremento di qualità. Se questo incremento c'è,
  adottatelo nel repo come standard»*
- **Rapporti**: ritorna su [ADR-0077](ADR-0077-revisione-a-due-giri.md), che
  aveva scartato Vale e LanguageTool; usa il registro di
  [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) e il punteggio di
  [ADR-0059](ADR-0059-il-punteggio-di-qualita-e-mqm-adattato.md); applica la regola «una norma, un
  rilevatore» di [ADR-0060](ADR-0060-la-forma-rende-misurabile-cio-che-la-parola-non-distingue.md)

## Contesto

La domanda ha due metà, e la prima si chiude con un inventario. Le skill di
prosa del repo hanno già quello che le redazioni professionali usano e che si
può automatizzare: una guida di stile con soglie (`editorial-standards.md`,
`read-aloud-adulti.md`), un punteggio con severità pesate e soglia dichiarata
prima (MQM, ISO 5060), l'accordo fra valutatori (κ), la revisione a due giri
con approvazione per modifica (ADR-0077), il confronto prima/dopo, la regola
dei tre indizi. Il repo li ha misurati uno per uno e in più punti li ha
tarati meglio di quanto farebbe un'importazione.

Le fonti consultate il 2026-10-03:

| Fonte | Licenza o stato | Cosa insegna | Esito |
|---|---|---|---|
| Guida di casa D&D (WotC, DMs Guild) | distribuzione gratuita, testo non riproducibile | CMOS, parole approvate («mithral», non «mithril»), forme dei tiri | si prende l'idea, mai il testo; la forma «mithral» è nello SRD |
| Linee guida *Dungeon* e *Dragon* (Paizo) | pubbliche | read-aloud, struttura dell'incontro | già in `read-aloud-adulti.md` e `module-standard` (ricerca 2026-09 e 2026-10-01) |
| Foglio di stile del copyeditor | pratica di mestiere | le decisioni di grafia e di termine si scrivono una volta e si rileggono | **adottato**, vedi sotto |
| Vale | MIT | regole `substitution`, `consistency`, test delle regole accanto alle regole | si prende la **tecnica**; il programma resta fuori |
| Jar of Eyes, *Coordinating TTRPG Writing* | articolo | lista di controllo di redazione, tetto di parole per sezione | la lista c'è (`passate-redazionali.md`); il tetto no, per il motivo già scritto nella ricerca §3 |

Il repo aveva già un glossario che dice di fissare **una volta sola** come si
scrive ogni nome. Il solo controllo che lo applicava cercava le forme inglesi
da tradurre. La **grafia** non la guardava nessuno: il termine «DC» è vietato
da `validate_modules.py`, ma solo nei master DEF, e il registro delle norme lo
ammette (*«non guarda i sorgenti non ancora DEF»*).

## Misura prima di decidere

Sul contenuto di gioco (521 file, archivi esclusi, 837.305 parole), il
2026-10-03:

- MQM verde su 521 documenti con *Regiarax* nel testo, *mithril* in 16 righe
  di 5 file e il PG Hella scritto *Hellas* in 18 file. Il metro non poteva
  vedere il difetto perché nessuna norma pesata riguarda la grafia.
- Un generatore automatico di coppie di nomi a una lettera di distanza ha dato
  9 candidati. Letti nel contesto, 5 erano utili (*Channathgate/Cannathgate*,
  *Loranna/Lorana*, *Myconid/Myconoid*, *Regiarax/Regiarix* e *Hella's/Hellas*,
  che ha portato a *Hellas*) e 4 no: *Garruk* e *Karruk* sono due PNG, *Thorek*
  e *Thorik* un re e un PG, *Headed/Healed* due parole inglesi, *Hell's* è
  inglese. Precisione grezza 5 su 9.
- Fra i 5 utili, solo due diventano un refuso da correggere. *Loranna* sta nel
  nome di un file sorgente, *Myconoid* in un nome di file immagine. Gli altri
  due sono decisioni del DM.

La lezione è quella di ADR-0060 da un'altra parte: un criterio automatico trova
i candidati, e il contesto decide. Perciò il controllo non è un correttore.

## Decisione

**1. Il foglio di stile è una tabella nel glossario.** `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md`
§8 elenca le forme escluse con la forma canonica, uno stato e il perché. Non
nasce un secondo file: i parser esistenti del glossario si fermano prima del §8,
così una forma esclusa non diventa un nome canonico (era il primo guasto del
lotto).

**2. Due stati.** `refuso` è una decisione presa e ogni occorrenza è un rilievo
di `terminologia_non_canonica` (maggiore). `DM?` è una scelta che spetta al DM:
si conta, non si rimprovera. Un nome di file, un altro PNG o la citazione di una
fonte non entrano mai come `refuso`.

**3. Un rilevatore, non due.** Il controllo estende `check_glossario` di
`validate_prosa.py`, con la stessa chiave di norma e lo stesso peso. *DC* e il
riposo breve e lungo restano di `validate_modules.py`.

**4. Due comandi nuovi, uno bloccante.** `validate_prosa.py --foglio` stampa per
ogni riga le occorrenze, i refusi aperti e le scelte in sospeso; con `--strict`
esce 1 se c'è un refuso, ed è il passo di CI, a soglia zero.
`--proponi-grafie` propone coppie da guardare e non accusa nessuno.

**5. Gli archivi non si riscrivono.** Il controllo salta tutto ciò che
`misura_craft.ESCLUSI` dichiara archivio e le cartelle con un
`_SNAPSHOT-STORICO.md`. Il marcatore mancava: il primo giro ha corretto uno
snapshot, `fase1.py --check` l'ha fermato, il file è stato ripristinato e il
controllo ora lo conosce.

**6. Ogni regola ha il caso positivo e il negativo**, come i test delle regole
di Vale: 14 test nuovi, fra cui i falsi positivi e i guasti trovati lungo la strada
(*Garruk/Karruk*, nome di file, riga che spiega il cambio, *Hellas* dentro
*Hella*, snapshot storico).

## Alternative scartate

- **Installare Vale.** Non è stato installato. Ha un binario Go da scaricare in
  CI, regole pensate per l'inglese (ADR-0077 lo aveva già scritto) e nessuna
  funzione che il repo non copra in Python standard: i tipi `substitution` e
  `consistency` sono la tabella del §8. Il guadagno sarebbe una dipendenza.
- **Correggere in blocco le scelte del DM.** *Hellas*, *Channathgate* e
  *Therisol* stanno in 285 occorrenze, in nomi di file e in un file di scheda
  del `Bestiario/`. Una sostituzione automatica rompe i rimandi e decide il
  canone al posto di chi lo possiede.
- **Un tetto di parole per sezione**, come il formato WotC per gli incontri.
  Importare il numero di un altro formato è l'errore già documentato per
  Gulpease.
- **Un elenco di termini di regola da uniformare** (*PF/HP*, *CA/AC*, *GS/CR*).
  Il repo li mescola di proposito fra tavolo e scheda tecnica; misurato, 789 CA
  contro 267 AC non è un'incoerenza ma due registri.

## Misura dell'incremento

| | Prima | Dopo |
|---|---:|---:|
| Refusi aperti sul contenuto di gioco | 17 | 0 |
| Righe corrette | | 17, in 6 file |
| Refusi per 100.000 parole | 2,03 | 0 |
| Scelte del DM in sospeso che nessun controllo vedeva | 4 (285 occorrenze) | 0: decise il 2026-10-03 e applicate |
| Righe corrette con le quattro decisioni | | 200, in 24 file, più `state.yaml`, quattro file di skill e il catalogo dei mostri rigenerato |
| Documenti sotto soglia MQM | 0 su 521 | 0 su 521 |
| Rilievi delle altre norme di prosa | 229 | 229 |
| Falsi positivi del rilevatore, contati a mano | | 0 su 17 |

**Cosa questa misura non dice.** L'incremento è reale e piccolo: 17 occorrenze
in 837.000 parole. Nessun documento cambia classe di punteggio, e un lettore al
tavolo difficilmente se ne sarebbe accorto. Il guadagno è strutturale: il foglio
di stile esiste ed è eseguibile, il difetto non ricade (cancello a zero in CI),
e le quattro scelte del DM sono ora un numero e non un sospetto. Il recall del
rilevatore non è stimato: i test lo verificano solo sulle forme già scritte, e
una grafia nuova la scopre il generatore o un lettore, non il controllo.
Le correzioni delle scelte del DM seguono la sorgente: `state.md` si rigenera da `state.yaml` (ADR-0050), il catalogo dei mostri e il dossier con i loro script. Una riga che cita un nome di file non si corregge (il rimando si romperebbe): è un'esenzione dichiarata del controllo, e il costo è che una grafia sbagliata in prosa sulla stessa riga di un percorso passa.
Il generatore ha un limite noto: non vede le differenze sull'ultima lettera, e i
suoi filtri sono stati tarati sullo stesso campione di 9 candidati, quindi la
precisione dopo i filtri non è indipendente.

## Conseguenze

- Chi sceglie una grafia la scrive nel §8: la riga costa dieci secondi, come
  dice già la §7 del glossario, e dopo non si discute più.
- La CI blocca il ritorno di un refuso deciso. Le righe `DM?` non bloccano mai.
- Le quattro scelte sono state prese dal DM il 2026-10-03 e passano a `refuso`:
  il PG si chiama *Hella*, la città *Channathgate*, la PNG *Therysol*, e
  *swift action* si rende *azione veloce* (come nelle traduzioni e nelle regole
  italiane di comunità del 3.5; non ho trovato un testo ufficiale da citare).
  La riga `DM?` resta nel meccanismo per le scelte future, ma oggi la tabella
  non ne ha.
- Una norma nuova arriva con la sua misura: la riga del registro è nel
  commit, e il gate `validate_norme_editoriali.py` la verifica.
