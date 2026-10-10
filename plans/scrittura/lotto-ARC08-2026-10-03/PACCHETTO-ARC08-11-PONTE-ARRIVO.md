# Pacchetto di riscrittura · ARC08-11-PONTE-ARRIVO.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 99.32 |
| penalità MQM | 1 |
| segnalazioni | 2 |
| Gulpease | 68.2 |
| ritmo | 0.56 |

## Cosa non si tocca

Nomi propri (32 diversi), numeri (25) e CD
(0): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 76-82 | box con più nomi propri Corona, Cuore, Forgia, Moradin | un solo nome nuovo per box (read-aloud-adulti §1.1) | > *"Il mondo si frantuma in luce rossa. Il rosso vi tira attraverso le > ere — non c'è dolore, solo vertigine cosmica. Poi: pietra, calore, > il rombo di un assedio. Non la quiete della Forgia — il **fragore** > del Cuor… |
| 2 | 76-82 | tic minori in gruppo antitesi, trattino come respiro | riscrivere il paragrafo: presi insieme suonano generati (italiano-nativo §9) | > *"Il mondo si frantuma in luce rossa. Il rosso vi tira attraverso le > ere — non c'è dolore, solo vertigine cosmica. Poi: pietra, calore, > il rombo di un assedio. Non la quiete della Forgia — il **fragore** > del Cuor… |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
