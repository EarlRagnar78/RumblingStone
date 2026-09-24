# RICERCA — BDD o TDD: la misura su un caso vero

> **Cos'è**: la risposta, con i numeri, alla domanda del DM del 2026-09-24:
> *«se il framework BDD è migliorativo cambiamo gli ADR, ma mi dici per cosa
> sta e in che cosa migliora il TDD? Potresti misurare il miglioramento e il
> costo, così si capisce se abbandonare TDD e prendere questo BDD?»*
>
> **Stato**: ✅ ricerca completa (2026-09-24) · **Alimenta**:
> [PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5.0 e la
> sua decisione **D6** · **Non cambia**: nessun ADR e nessun metodo finché il DM
> non risponde alla D6.

---

## §1 · Che cos'è il BDD

**BDD** sta per *Behaviour-Driven Development*, sviluppo guidato dal
comportamento. L'ha proposto Dan North nel 2006 (*Introducing BDD*), partendo
da un problema del TDD: chi lo impara non sa da dove cominciare, cosa provare e
come chiamare i test. La sua risposta è stata cambiare le parole. Un test
diventa la descrizione di un comportamento, scritta nella forma
**Dato / Quando / Allora** (*Given / When / Then*), e il nome del test è una
frase che anche chi non programma può leggere.

Il BDD ha due metà che conviene tenere separate:

- **la pratica**: prima di scrivere codice, chi chiede la funzione e chi la
  costruisce scrivono insieme gli esempi concreti del comportamento atteso
  (*example mapping*, i *three amigos*). Gli esempi diventano il criterio
  d'accettazione;
- **il framework**: Cucumber, `behave`, `pytest-bdd`. Leggono file `.feature`
  in linguaggio Gherkin (che ha anche l'italiano: `Funzionalità`, `Scenario`,
  `Dato`, `Quando`, `Allora`) e collegano ogni frase a una funzione Python, lo
  *step*.

Il BDD **non sostituisce** il TDD. Ci sta sopra: il TDD decide come si scrive il
codice di una funzione, il BDD decide quali comportamenti il sistema deve avere
e lo dice in una lingua condivisa. Chi fa BDD, sotto gli scenari, di solito fa
anche TDD. La domanda utile quindi non è «BDD o TDD», ma **se il framework BDD
aggiunge qualcosa che il repo non ha già, e a che prezzo**.

## §2 · Cosa ho guardato prima

- **§5.0 del piano del ciclo di sessione** (rev. 2): prevede già i test
  d'accettazione scritti dalle storie, sopra il TDD del nucleo.
- **§4 dello stesso piano**: le storie U1-U7 sono **già** nella forma
  «Dato che… / quando il DM… / allora…». La metà «pratica» del BDD il repo la
  fa già, senza chiamarla così.
- **[ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md)**: gli
  script usano solo la libreria standard, `pytest` è ammesso solo come secondo
  corridore in CI (`requirements-dev.txt`).
- **I test di 4f-4** (`scripts/tests/test_gruppo_nuovo.py`): hanno nomi che
  sono già frasi italiane, come `test_le_conoscenze_sul_party_si_tolgono_da_sole`.

## §3 · L'esperimento

Un comportamento vero, riscritto due volte con la stessa copertura:
`dm.py gruppo nuovo` del lotto 4f-4, con logica nel nucleo, modulo in terminale
e comando completo su una copia del repo sotto git.

| | TDD (quello del repo) | BDD con `behave` |
|---|---|---|
| File | `scripts/tests/test_gruppo_nuovo.py` | `plans/esperimenti/bdd-gruppo-nuovo/features/` |
| Forma | 19 test `unittest` | 1 funzionalità, 15 scenari + uno schema da 8 esempi, 77 passi |

Tutti e due verdi al primo lancio. Per rifare la misura:

```bash
python3 -m venv /tmp/bdd && /tmp/bdd/bin/pip install behave pyyaml
/tmp/bdd/bin/behave plans/esperimenti/bdd-gruppo-nuovo/features
python3 -m pytest -q scripts/tests/test_gruppo_nuovo.py
python3 plans/esperimenti/bdd-gruppo-nuovo/mutanti.py /tmp/bdd/bin/behave
```

L'esperimento resta in `plans/esperimenti/` come prova riproducibile. Non gira
in CI: `behave` non è una dipendenza del repo.

## §4 · Le misure (2026-09-24)

| Misura | TDD | BDD `behave` | Differenza |
|---|---:|---:|---|
| **Difetti trovati**: mutanti uccisi su 16 (12 nel nucleo, 4 nel guscio) | **16** | **16** | nessuna |
| Righe da mantenere | 303 | 430 (90 `.feature` + 340 step) | **+42%** |
| Righe leggibili da chi non programma | 0 (19 nomi di test) | 90 | la vera differenza |
| Tempo della suite | 2,4 s | 3,5 s | +45% |
| Tempo dei 16 mutanti | 11 s | 16 s | +45% |
| Dipendenze nuove | 0 | 6 pacchetti, 3,2 MB | contro ADR-0037 |
| Con `pytest-bdd` al posto di `behave` | 0 | 6 moduli, 3,0 MB sopra `pytest` | idem |
| **Aggiungere un rifiuto** (PG al livello 21) | 2 righe | 3 righe in 2 file | pari |
| **Aggiungere un comportamento** (stesse risposte, stesso stato) | 6 righe, verde al primo colpo | 3 righe di scenario + 11 di step in 2 file, **errore al primo colpo** | più del doppio |

I 16 mutanti sono la stessa lista per le due suite
(`plans/esperimenti/bdd-gruppo-nuovo/mutanti.py`): clock non azzerato, «party» non contato nelle conoscenze,
«PG» non contato come traccia, portatore tenuto, March Clock che non riparte,
echi tenuti, «tieni» come scelta predefinita, zero PG accettati, scelta
inventata accettata, archi successivi marcati come non giocati, nome del gruppo
non controllato, percorso dei waypoint sbagliato, albero sporco ignorato,
niente commit, Ctrl-D che esce 0, PF al posto del livello.

🔎 **L'errore al primo colpo va raccontato, perché è il costo tipico del
framework.** Lo step nuovo usava le risposte minime del modulo, che negli step
non sono complete: l'arco di partenza viene aggiunto da una funzione di
contesto, lontano dal dizionario. In `unittest` le stesse risposte sono una
costante completa in cima al file. Il BDD separa la frase dal codice che la
esegue, e lo stato che passa fra i passi (`ctx`) è implicito. Su un repo
mantenuto da una persona sola questa indirezione si paga a ogni modifica.

## §5 · Cosa migliora davvero, e cosa no

**Migliora una cosa, ed è importante**: il file `.feature` si legge. Novanta
righe di italiano dicono cosa fa `gruppo nuovo` a chi non apre Python, e il DM
può correggere un esempio sbagliato senza leggere codice. È il motivo per cui il
BDD esiste.

**Non migliora**:

- **la capacità di trovare difetti**: 16 su 16 per tutti e due. La qualità la
  danno gli esempi scelti, non il formato;
- **la facilità di cambiare il sistema**: per aggiungere un caso si toccano due
  file invece di uno, e lo stato fra i passi è nascosto. Quello che rende facile
  il cambiamento è in §5.0 del piano (contratti, nucleo puro), e vale uguale con
  i due formati;
- **la disciplina**: le storie U1-U7 sono già scritte come Dato/Quando/Allora.
  La parte del BDD che conta, cioè decidere il comportamento con chi lo chiede
  prima di scrivere codice, il repo la fa già con le D del DM e le storie dei
  piani.

**Costa**: +42% di righe, +45% di tempo, tre megabyte di dipendenze contro
ADR-0037, e un secondo linguaggio (Gherkin) da tenere allineato al codice.

## §6 · La raccomandazione

**Non abbandonare il TDD, e non adottare il framework.** Il guadagno
misurato è la leggibilità, e il repo può averla senza framework:

1. **Gli scenari restano nel piano**, come le storie U1-U7 di oggi: tabella
   Dato/Quando/Allora, con un identificatore. Lì li legge e li corregge il DM,
   dove già guarda.
2. **Ogni test d'accettazione cita il suo scenario** nel nome o nella docstring
   (`U1`, `U2`…).
3. **Un gate di sola libreria standard** controlla che ogni scenario del piano
   abbia almeno un test che lo cita, e che nessun test citi uno scenario che non
   esiste. È la *tracciabilità* che il BDD ottiene col framework, ottenuta con
   uno script di poche decine di righe.

È la metà «pratica» del BDD senza la metà «framework». Tiene i numeri del TDD
(303 righe, 2,4 s, zero dipendenze, 16 su 16) e aggiunge quello che il `.feature`
dava di buono: una specifica leggibile, che fallisce in CI quando resta
indietro rispetto ai test.

Se il DM vuole invece il BDD pieno, la via meno costosa è `pytest-bdd`, perché
`pytest` è già in CI: serve un'eccezione scritta ad ADR-0037, come quella di
`pytest`, e una revisione di §5.0. È la **D6** di
[PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §8.

## §7 · Limiti della misura

- **Un solo caso.** `gruppo nuovo` ha un nucleo puro e un guscio sottile. Su un
  flusso con più interazione (il menu, la chiusura a domande) il `.feature`
  potrebbe rendere di più come documento. La misura andrebbe ripetuta sul primo
  lotto di Fase 1.
- **La leggibilità la giudica il DM, non uno strumento.** Le 90 righe del
  `.feature` sono in `plans/esperimenti/`: se le trova più utili della tabella
  U1-U7 del piano, il punto 1 di §6 perde forza.
- **`pytest-bdd` è pesato, non eseguito.** Ho misurato le dipendenze (8.1.0:
  `gherkin-official`, `Mako`, `packaging`, `parse`, `parse-type`,
  `typing-extensions`), non il tempo né le righe.
- **I mutanti sono scritti a mano**, come è convenzione del repo: dicono che le
  due suite trovano gli stessi 16 difetti, non che ne troverebbero altri allo
  stesso modo.
