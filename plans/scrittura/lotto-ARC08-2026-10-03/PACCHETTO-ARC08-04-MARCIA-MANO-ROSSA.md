# Pacchetto di riscrittura · ARC08-04-MARCIA-MANO-ROSSA.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/ARC08-04-MARCIA-MANO-ROSSA.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 100.0 |
| penalità MQM | 0 |
| segnalazioni | 1 |
| Gulpease | 54.8 |
| ritmo | 1.05 |

## Cosa non si tocca

Nomi propri (42 diversi), numeri (22) e CD
(0): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 36-39 | tic minori in gruppo antitesi, trattino come respiro | riscrivere il paragrafo: presi insieme suonano generati (italiano-nativo §9) | - **Non rientra nel corpo principale**: la sconfitta/dispersione del distaccamento (D11) non altera il totale dell'orda principale che marcia verso Rhest — è già contabilizzata separatamente in state.md §2.2 come perdita… |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/ARC08-04-MARCIA-MANO-ROSSA.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/ARC08-04-MARCIA-MANO-ROSSA.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/ARC08-04-MARCIA-MANO-ROSSA.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
