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
| Campionamento | temperatura 0,7, seme = numero della ripetizione, 3 ripetizioni: 72 risposte |
| Misure | violazioni S8 per scheda (la funzione del cancello, `verifica_tattiche`); nomi del plugin dnd35 fuori dalla scheda senza guardare il corsivo; risposte valide; copertura delle voci della scheda; secondi e token al secondo |

## Regola del verdetto, scritta prima della misura

La tecnica **migliora** se, sulle stesse schede: (1) il vincolato ha meno
violazioni S8 per scheda del libero, (2) tutte le sue risposte sono valide,
(3) la sua copertura delle voci della scheda è almeno l'80% di quella del
libero. La condizione (3) c'è perché un vincolo che fa scrivere solo
«avanzare» non viola niente ma non serve.

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
  (`fuori_lista`), che cerca i nomi senza guardare la formattazione.
- Il campione ha un difetto del generatore che la prova non corregge: il
  talento *Incantesimi focalizzati* esce con «(bene, caos, legge o male)» al
  posto di una scuola.
- Lo script è provato nel container con un Ollama finto
  (`scripts/tests/test_prove_4050.py`), mai su una GPU.

## Come si lancia

`scripts/prove-4050/schede-vincolate.sh`, dalla
[guida del portatile](../../../docs/how-to/GUIDA-PROVE-PORTATILE-4050.md) §3-ter.
