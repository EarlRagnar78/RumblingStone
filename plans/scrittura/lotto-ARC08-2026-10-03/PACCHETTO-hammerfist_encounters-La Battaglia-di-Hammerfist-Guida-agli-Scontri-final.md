# Pacchetto di riscrittura · hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 99.79 |
| penalità MQM | 3 |
| segnalazioni | 3 |
| Gulpease | 61.3 |
| ritmo | 0.42 |

## Cosa non si tocca

Nomi propri (46 diversi), numeri (65) e CD
(9): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 1112-1112 | box con più nomi propri Fauci di Palude, Mano, Rossa | un solo nome nuovo per box (read-aloud-adulti §1.1) | > *"Fauci di Palude, realizzando che la battaglia è perduta, si volta verso il campo dove stanno avanzando i nani. Con un ultimo atto di pura malvagità, sprigiona il suo soffio acido non per uccidere, ma per distruggere … |
| 2 | 1112-1112 | calco «stanno avanzando»: progressivo all'inglese: nel read-aloud basta il presente («cammini nel buio») | riscrivere all'italiana (italiano-nativo §1) | > *"Fauci di Palude, realizzando che la battaglia è perduta, si volta verso il campo dove stanno avanzando i nani. Con un ultimo atto di pura malvagità, sprigiona il suo soffio acido non per uccidere, ma per distruggere … |
| 3 | 1315-1315 | box con più nomi propri Borin, Dara | un solo nome nuovo per box (read-aloud-adulti §1.1) | > *"Il vento attraversa le lame piantate creando una melodia triste ma orgogliosa. Ogni ascia porta inciso in fretta il nome del guerriero che l'ha brandita. 'Thrain Scudoforte, servo fedele 80 anni.' 'Borin Manodura, di… |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
