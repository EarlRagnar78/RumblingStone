# ADR-0038 — L'EL viene da una gerarchia dichiarata, non da un numero nel codice

> **Stato**: accettata · **Data**: 2026-09-03 · **Decide**: G. Samuele (DM)
> **Nasce da**: rilievo del DM sul difetto n. 5 del lotto C di
> `PIANO-QUALITA-DEL-CODICE` — *«se il file non propone nessun EL si potrebbe
> generare il loot guardando l'avventura, oppure se è chiamato da
> suggest_encounter l'EL viene da lì, o mi sbaglio?»*
> **Rapporti**: chiude una coda che il lotto C aveva lasciato aperta di
> proposito, perché cambiare quel ripiego cambia cosa succede al tavolo.

## Il contesto

Il lotto C aveva trovato che `suggest_loot`, davanti a un file che non è un
output di `suggest_encounter`, non protestava: ripiegava su un EL **10 scritto
nel codice** (`el = pr["el"] if pr["el"] is not None else (args.el or 10.0)`) e
generava tesoro come se niente fosse. Il manifest prometteva un codice d'uscita
3 per quel caso, e il ramo era irraggiungibile.

Il DM ha fatto due osservazioni, e reggono tutte e due.

**La prima corregge la descrizione del difetto.** Nella catena documentata l'EL
viene da `suggest_encounter`, che emette `**Combined EL**` per ogni proposta.
Verificato eseguendola: `--el 12` produce quattro proposte e il loot esce su
EL 13. Il 10 non si vedeva mai. Il rischio era più stretto di come era stato
scritto.

**La seconda apre una porta che nessuno aveva visto.** `campaign/state.md`
dichiara nell'intestazione:

```
**Party APL:** 13 (ARC-07 D8 — livello reale già raggiunto durante l'Arco 07)
```

Sta fuori dalle regioni `auto:`, quindi è prosa del DM e nessuno script la
sovrascrive: è la dichiarazione di chi ha l'autorità per farla. E **nessuno dei
due strumenti la leggeva**. `suggest_encounter` pretendeva `--el` a ogni
chiamata, uscendo con 2 senza. Il numero era nel repo e ogni preparazione di
scontro lo riscriveva a mano.

## La decisione

**L'EL viene da una gerarchia di quattro gradini, e chi lo usa dice sempre da
quale.**

| ordine | fonte | perché sta lì |
|---|---|---|
| 1 | `--el` | l'ha scritto il DM adesso, per questo scontro |
| 2 | `**Combined EL**` del file di incontro | calcolato sui mostri veri di quello scontro |
| 3 | `**Party APL:**` di `state.md` | un punto di partenza dichiarato dal DM, non una scelta di regia |
| 4 | rifiuto (`return 2` o `3` secondo il ramo) | non c'è da dove partire, e inventare era il difetto |

Sta in `scripts/dmcore/tavolo.py` (`leggi_apl`, `origine_el`), in un posto solo,
e la usano `suggest_loot` e `suggest_encounter`.

`origine_el()` restituisce il numero **e l'etichetta di provenienza**, che i due
strumenti stampano su stderr quando la fonte non è quella che ci si aspetta —
`suggest_encounter` tace se il numero viene da `--el`, `suggest_loot` tace se
viene dal file. Un default silenzioso è come ci si era arrivati.

## Perché il terzo gradino avverte invece di limitarsi a dare il numero

**APL non è EL**, e trattarli come sinonimi è il modo in cui questa comodità
diventerebbe un danno. Un incontro di EL pari all'APL è lo scontro «medio» del
manuale: consuma circa un quarto delle risorse giornaliere e nessuno se lo
ricorda. Il boss di fine arco sta tre o quattro gradini sopra, e questa
decisione non ha modo di saperlo.

Per questo l'etichetta del terzo gradino dice per esteso che è un punto di
partenza e che per un boss si usa `--el`, e un test tiene ferma quella frase.
Il valore della decisione è togliere un numero muto dal codice, non scegliere
al posto del DM.

## Le conseguenze

**Quello che si guadagna.**

- `python3 scripts/suggest_encounter.py` senza argomenti diventa una domanda
  sensata — *«cosa metto davanti al gruppo stasera?»* — invece di un errore
  d'uso.
- Il 10 scritto nel codice non c'è più, e con lui l'unico punto in cui uno
  strumento inventava un numero senza dirlo.
- Il codice d'uscita 3 di `suggest_loot`, che il lotto C aveva trovato
  irraggiungibile, torna raggiungibile e descrive un caso vero: manca l'EL nel
  file, manca `--el`, e manca anche il Party APL.

**Quello che si paga.**

- **Un accoppiamento nuovo**: due strumenti di prep leggono `campaign/state.md`,
  che prima non guardavano. È lettura, mai scrittura, e degrada a `None` se il
  file non c'è o non ha la riga — ma se qualcuno cambia il formato di quella
  riga, i due perdono il gradino 3. Un test lo verifica sullo state vero, e cade
  quando succede.
- **Un numero comodo è un numero che si smette di scegliere.** Il rischio non è
  tecnico: è che il DM prenda l'APL come EL per abitudine. L'avviso su stderr è
  la difesa, e non è una difesa forte.
- **`render_loot()` ha ancora un `else 10` difensivo** per il caso `el=None`,
  che dopo questa decisione non arriva più da nessun chiamante. È codice morto,
  ma è un clamp di visualizzazione e non una decisione: toglierlo è un'altra
  cosa, e non è stato fatto qui.

**Quando si rivede.** Se un giorno `state.md` acquistasse un EL suggerito per
beat — cioè un numero che *è* una scelta di regia e non un livello medio — quel
numero prenderebbe il posto del gradino 3 e l'avviso non servirebbe più.
