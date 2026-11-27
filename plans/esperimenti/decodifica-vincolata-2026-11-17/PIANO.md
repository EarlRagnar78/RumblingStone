# Decodifica vincolata delle «Tattiche»: piano della misura

> Tecnica 3 del thread «Applicare Document AI e Explainable AI» (le altre: 1 glifi
> #398, 2 PDF/A-2a #416, 4 provenienza IPTC #418, 5 andata e ritorno del testo,
> misurata il 13/11 e senza margine). Il DM ha scelto il 17/11 sulla card «Sì,
> quando accendi l'ASUS»: la prova gira sulla RTX 4050, e la tecnica entra nel
> repo solo se la misura dice che migliora.

## Ipotesi

`scripts/genera_creatura.py` fa già da tabelle tutti i numeri di una scheda:
lì un vincolo sul modello non aggiunge niente. Il testo che un modello locale
sbaglia è quello che rimanda alla scheda: le «Tattiche» che nominano un
incantesimo o un talento che la creatura non ha. È l'errore che il controllo
S8 (`coerenza_campagna.py fatti DIR --tattiche`, ADR-0125) trova nel Bestiario.
La decodifica vincolata (il campo `format` di Ollama con uno schema JSON, che
llama.cpp traduce in una grammatica) può impedirlo per costruzione: l'azione di
ogni passo è un enum delle voci della scheda.

## Prova

| Cosa | Valore |
|---|---|
| Schede | 12 PNG umanoidi di `genera_creatura.py`, semi fissi (`CAMPIONE` nello script): mago, chierico, stregone, druido, bardo, ranger, paladino, guerriero; GS 4-12 |
| Modello | `qwen2.5:7b` di serie (Apache 2.0, lo stesso del lettore); se ne può passare un altro |
| Bracci | **libero**: le tattiche in tre righe Markdown, incantesimi in corsivo. **vincolato**: JSON con lo schema, da 1 a 4 passi per fase, `azione` in enum (incantesimi, talenti e attacchi della scheda più sette azioni comuni), `bersaglio` e `perche` liberi ma corti; lo script lo scrive in Markdown |
| Campionamento | temperatura 0,7, seme = numero della ripetizione, 3 ripetizioni: 72 risposte; tetto di 1500 token a risposta, e le risposte troncate dal tetto si contano (`troncate`) |
| Misure | violazioni S8 per scheda (la funzione del cancello, `verifica_tattiche`); nomi del plugin dnd35 fuori dalla scheda senza guardare il corsivo; risposte valide; copertura delle voci della scheda; secondi e token al secondo |

## Regola del verdetto, scritta prima della misura

La tecnica **migliora** se, sulle stesse schede: (1) il vincolato ha meno
violazioni S8 per scheda del libero, (2) tutte le sue risposte sono valide,
(3) la sua copertura delle voci della scheda è almeno l'80% di quella del
libero e almeno una voce per risposta in media. La condizione (3) c'è perché
un vincolo che fa scrivere solo «avanzare» non viola niente ma non serve; il
minimo di una voce vale anche quando il libero non ne nomina nessuna.

Se migliora, la PR della tecnica porta il braccio vincolato in un comando del
repo (le «Tattiche» di `genera_creatura.py` scritte dal modello locale, con lo
schema) e ne registra la misura in un ADR. Se non migliora, si scrive l'esito
qui e nel thread, e non entra niente.

## Limiti dichiarati

- Il vincolo garantisce nomi coerenti con la scheda, non tattiche buone: la
  qualità della prosa la giudica il DM alla cieca (ADR-0093), e questa prova
  non la misura.
- `perche` e `bersaglio` restano testo libero e possono nominare un
  incantesimo: S8 li legge, quindi la misura lo conta.
- S8 riconosce un incantesimo solo in corsivo. Se il libero non usa il corsivo,
  S8 gli conta meno errori di quelli che fa; per questo c'è il secondo conto
  (`fuori_lista`), che cerca i nomi senza guardare la formattazione. Anche
  questo ha un buco dichiarato: gli incantesimi di una parola sotto le 9
  lettere («luce», «sonno») non li conta, perché sono anche parole comuni.
- Del libero si legge tutto quello che il modello scrive: lo script toglie
  solo titoli, numeri d'elenco e grassetto, perché `verifica_scheda` legge una
  riga in grassetto come l'inizio di un'altra sezione e S8 non vedrebbe il
  resto. Un preambolo («Ecco le tattiche») entra nel testo e non pesa.
- Non è provato che l'Ollama del portatile rispetti `maxLength` nello schema:
  se non lo fa, un `perche` lungo può arrivare al tetto dei token. Si vede dal
  conto `troncate`, e in quel caso la condizione (2) va letta con quel numero.
- Lo script è provato nel container con un Ollama finto
  (`scripts/tests/test_prove_4050.py`), mai su una GPU.

## Correzioni prima della misura (18/11)

Rilettura chiesta dal DM, prima che la prova girasse. Tre errori dello script,
nessuno della regola del verdetto, che resta com'era:

1. il libero perdeva violazioni per l'impaginazione: righe in grassetto,
   elenchi numerati e titoli sparivano o nascondevano il testo a S8 (su quattro
   forme della stessa risposta con una *palla di fuoco* che la scheda non ha, S8
   ne trovava una su quattro; ora quattro su quattro);
2. il tetto di 700 token troncava un JSON pieno (12 passi da circa 90 token):
   la risposta sarebbe stata «non valida» per il tetto, e la condizione (2)
   sarebbe caduta per questo. Ora 1500, e le troncate si contano;
3. un `bersaglio` o un `perche` non testuale faceva cadere lo script invece di
   contare la risposta come non valida.

Il difetto del generatore dichiarato alla prima stesura (*Incantesimi
focalizzati* con «(bene, caos, legge o male)») è corretto dalla #468.

## Come si lancia

`scripts/prove-4050/schede-vincolate.sh`, dalla
[guida del portatile](../../../docs/how-to/GUIDA-PROVE-PORTATILE-4050.md) §3-ter.
