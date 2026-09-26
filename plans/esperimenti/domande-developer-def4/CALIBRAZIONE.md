# Calibrazione di `domande_developer.py` sul DEF-4 giocato al tavolo

Lo strumento misura sei delle sette domande del developer di
`rumblingstone-module-standard/references/sviluppo-degli-incontri.md`. Prima di
fidarsene si è provato su un testo di cui i difetti si conoscono già: `ARC07-DEF-4`
al commit `ddd683c`, la versione che il gruppo ha giocato il 2026-09-25. I
difetti noti vengono da tre fonti indipendenti dallo strumento: il tavolo, la
prima lettura a freddo e la seconda.

Si riproduce così:

```
git show "ddd683c:07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md" > /tmp/def4.md
python3 scripts/domande_developer.py --file /tmp/def4.md
```

## Quanto trova

| Difetto noto | Chi l'aveva trovato | Regola | Trovato? |
|---|---|---|---|
| nessuna risposta per chi sorvola il campo | il tavolo (la variante dall'alto nasce lì) | D2 · Scena 6 | ✅ |
| lo scontro nella tenda fa suonare il corno? | seconda lettura, playtester #24 🔴 | D4 · Scena 7 | ✅ |
| Tordek senza mezzi contro il drago in quota | prima lettura, playtester #42 🟠 | D1 · Scena 11 | ✅ |
| «Furtività», abilità che in 3.5 non c'è | prima lettura, playtester #35 🟡 | D6-5E | ✅ |
| nessun effetto chiede Tempra | `RICERCA-MANUALE-DEL-MASTER` §2, contato a mano | D3 | ✅ |

**Cinque su cinque.** Nessuno di questi era nel mirino di un cancello: i tre
delle letture a freddo erano rilievi in prosa, e il primo l'ha trovato il
tavolo.

## Quanto sbaglia

Nove rilievi in tutto. Oltre ai cinque veri:

| Rilievo | Perché non è un difetto |
|---|---|
| D2 · Scena 2 (due volte) | la pattuglia di Durin viene incontro ai PG: non è un luogo da superare |
| D2 · Scena 7, volo | la risposta c'è, ma nella Scena 6 (l'atterraggio vicino alla tenda) |
| D1 · Scena 8 | il drago non combatte lì: la «picchiata» annuncia la Scena 11 |

**Precisione 5 su 9.** È il costo di uno strumento che guarda la forma e non il
senso, e il motivo per cui ogni rilievo si dichiara in
`plans/domande-developer.json` con la sua ragione invece di diventare un
errore bloccante.

## Due forme corrette dalla calibrazione

- **D1**, la risposta per chi non vola. La prima forma accettava «a terra» e
  «atterra», e dichiarava risolta la Scena 11: in una scena lunga con un drago
  quelle parole ci sono sempre, nella descrizione. Adesso la risposta va scritta
  come tale («chi non vola può…», «armi a distanza», «lo costringe a
  scendere»).
- **D6-5E**, le abilità estranee. Il Drappo è un modulo PF1e, dove Percezione,
  Furtività e Intuizione esistono: il profilo del modulo dichiara il sistema.

## Sul testo di oggi

Degli stessi nove, restano i quattro falsi positivi e **uno vero: D1 · Scena
11**. Il rilievo #42 del playtester non è mai stato chiuso. Scene 6 e 7,
l'abilità 5e e la Tempra sono state corrette nei lotti M5-M7 e F3.
