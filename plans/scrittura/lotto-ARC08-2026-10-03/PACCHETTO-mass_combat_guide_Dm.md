# Pacchetto di riscrittura · mass_combat_guide_Dm.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 99.85 |
| penalità MQM | 1 |
| segnalazioni | 1 |
| Gulpease | 65.0 |
| ritmo | 0.27 |

## Cosa non si tocca

Nomi propri (11 diversi), numeri (43) e CD
(4): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 475-475 | sembra/pare «sembrava» | dire cosa c'è, o descrivere la cosa che non torna (D13) | > *"Proprio quando tutto sembrava [situazione], [PG nome] [azione eroica]. L'effetto è [immediato/drammatico]: [conseguenza visibile]."* |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
