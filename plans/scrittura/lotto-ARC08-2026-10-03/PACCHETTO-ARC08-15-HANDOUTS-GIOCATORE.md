# Pacchetto di riscrittura · ARC08-15-HANDOUTS-GIOCATORE.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 98.26 |
| penalità MQM | 3 |
| segnalazioni | 2 |
| Gulpease | 76.6 |
| ritmo | 0.68 |

## Cosa non si tocca

Nomi propri (20 diversi), numeri (43) e CD
(0): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 119-127 | box con parentesi  | togliere la parentesi: all'orale non esiste (read-aloud-adulti §1.3) | > *Ricordato.* > *Ricordato.* > *Ricordato.* > > *(I nani anziani lo ripetono per ognuno dei 210 caduti. Al termine, i > 90 sopravvissuti pronunciano il **Giuramento delle 90**:)* > > **"Per i centodiciotto. Per i novant… |
| 2 | 119-127 | box con più nomi propri Drellin's, Ferry | un solo nome nuovo per box (read-aloud-adulti §1.1) | > *Ricordato.* > *Ricordato.* > *Ricordato.* > > *(I nani anziani lo ripetono per ognuno dei 210 caduti. Al termine, i > 90 sopravvissuti pronunciano il **Giuramento delle 90**:)* > > **"Per i centodiciotto. Per i novant… |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
