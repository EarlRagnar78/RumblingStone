# ADR-0060 — La forma rende misurabile ciò che la parola non distingue

**Stato**: accettata (2026-09-20), attuata
**Contesto**: [PIANO-QUATTRO-ORDINI](../PIANO-QUATTRO-ORDINI-2026-09-20.md) §2D ·
[RICERCA-STANDARD-PROSA-WOTC-PAIZO](../RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md) §3
**Sostituisce**: la voce «non misurabile» di quella ricerca, §3, secondo punto

---

## Contesto

Il 2026-09-19 la ricerca sugli standard di WotC e Paizo ha archiviato una delle
loro prescrizioni come **non misurabile**, con la ragione scritta che ADR-0056
richiede:

> *«Le maiuscole di caratteristiche e abilità. In italiano la convenzione WotC
> non si trasferisce pulita:* Forza *è anche un sostantivo comune, e un
> rilevatore darebbe più falsi positivi che errori. Si registra come norma non
> misurata, con la ragione.»*

La ragione era vera **del rilevatore che avevo in mente**, e il numero lo
conferma: `\b(forza|destrezza|…)\b` pesca **2.014** occorrenze nei 511 file di
gioco, e la quasi totalità sono sostantivi comuni.

Il giorno dopo il DM ha fatto un'obiezione di merito:

> *«se compaiono nello statblock di un PNG o mostro sono seguiti da un numero,
> come ad esempio* Forza 25*; nel caso di prove non dovrebbe essere nella forma
> simile a* prova di Forza CD 25*? In questo modo è più facile distinguerli?
> Puoi verificare se apporta dei miglioramenti misurandoli?»*

## Decisione

**Quando una parola non distingue, si misura la forma in cui compare.** Una
caratteristica di gioco non si riconosce dal lemma — che la lingua condivide
con un sostantivo comune — ma dal **contesto meccanico**, che un sostantivo
comune non ha mai: un punteggio accanto, un modificatore col segno, una CD
sulla stessa riga, un tipo di bonus davanti.

Quattro forme, in `validate_prosa.py --caratteristiche`:

| | Forma | Occorrenze | Fuori norma |
|---|---|---|---|
| **F1** | caratteristica + punteggio — `Forza 25` | 1 | 0 |
| **F2** | abilità + modificatore **senza spazio dopo il segno** — `Nuotare +9` | 213 | 0 |
| **F3** | `prova/tiro/TS di X` **con una CD sulla stessa riga** | 38 | 2 |
| **F4** | `bonus/modificatore di X` | 6 | 1 |
| | **totale** | **258** | **3** |

**Zero falsi positivi**, controllati uno per uno a mano. Le tre violazioni sono
state corrette nello stesso lotto, e la soglia del cancello è **zero**.

## Conseguenze

- Una voce «non misurabile» del registro **si può ritirare**, e ritirarla è un
  lavoro dovuto. La ricerca che l'aveva scritta porta ora la correzione con la
  misura accanto.
- La regola si generalizza oltre questo caso: prima di dichiarare non
  misurabile una norma su un termine ambiguo, **si cerca la forma**. Vale per
  gli incantesimi in corsivo (che infatti compaiono in forme dichiarate), e
  varrà per le taglie e le scuole di magia il giorno che qualcuno le guarderà.
- ⚠️ Il contrario è altrettanto vero e va detto: **non tutte le norme hanno una
  forma**. *«La prosa è bella»* non ne ha nessuna, e nessuna quantità di regex
  gliela dà.

## Limiti dichiarati

1. **Il rilevatore vede solo le quattro forme.** Un errore di maiuscola in una
   frase discorsiva — *«tira forza per aprirla»*, senza CD — non si vede. È una
   scelta: quel caso costa più falsi positivi di quanti errori trovi.
2. **L'elenco delle abilità è scritto a mano**, ed è l'unico punto di questo
   controllo che non viene da un dato del repo. Un'abilità mancante è un falso
   negativo silenzioso. 🔎 Il rischio si è già manifestato **al contrario**: al
   primo giro l'elenco conteneva `intuizione`, il conto saliva da 3 a **25**, e
   le ventidue in più erano *«bonus di intuizione +4»*, che in 3.5 è un **tipo
   di bonus** e non l'abilità (l'abilità è *Percepire Intenzioni*).
3. **Le sigle non sono misurate**, e sono la forma dominante: `For 25`, `Des 14`
   compaiono **688** volte. Sono maiuscole per costruzione, quindi non c'è
   niente da controllare — ma se un giorno qualcuno scrivesse `for 25`, questo
   controllo non lo vedrebbe.
