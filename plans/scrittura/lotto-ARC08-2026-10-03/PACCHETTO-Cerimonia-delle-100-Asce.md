# Pacchetto di riscrittura · Cerimonia-delle-100-Asce.md

<!-- pacchetto: originale="08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md" -->

Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a
togliere la segnalazione. Prima di scrivere si leggono i `references/` di
`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,
`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.

## Da che numero si parte

| misura | valore |
|---|---:|
| punteggio MQM | 99.03 |
| penalità MQM | 2 |
| segnalazioni | 4 |
| Gulpease | 72.3 |
| ritmo | 0.66 |

## Cosa non si tocca

Nomi propri (47 diversi), numeri (51) e CD
(3): `revisione` confronta i tre insiemi e blocca la modifica
che ne cambia uno. Una frase senza segnalazione resta com'è.

## I passaggi

| # | righe | norma | rimedio | il testo |
|---:|---|---|---|---|
| 1 | 19-19 | tic minori in gruppo copula elusa, trattino come respiro | riscrivere il paragrafo: presi insieme suonano generati (italiano-nativo §9) | - **100 asce cerimoniali** (non 210) sono piantate in cerchio nella **Sala di Pietra Antica** (l'atrio della cittadella). Ogni ascia rappresenta **un'unità o un guerriero notevole** — non una persona singola: è simbolico… |
| 2 | 42-48 | box con più nomi propri Eterni, Hammerfist, Thorek | un solo nome nuovo per box (read-aloud-adulti §1.1) | > *Re Thorek si volta verso i quattro di voi. Non sorride. La sua voce, già rauca dalla cantillazione, si fa una sola tonalità più piana.* > > *"Voi non siete nani della mia stirpe — tre lo siete, una no, ma il sangue no… |
| 3 | 42-42 | calco «La sua voce»: possessivo su una parte del corpo: in italiano è già implicito («alzò la mano») | riscrivere all'italiana (italiano-nativo §1) | > *Re Thorek si volta verso i quattro di voi. Non sorride. La sua voce, già rauca dalla cantillazione, si fa una sola tonalità più piana.* |
| 4 | 133-133 | tic minori in gruppo antitesi, trattino come respiro | riscrivere il paragrafo: presi insieme suonano generati (italiano-nativo §9) | Tempestas attende che il banchetto si calmi. Avvicina Thorik in un'alcova. **Non finge** — gli dice esplicitamente: *"Comandante, sono qui per due missioni. Una è onorare i vostri morti. L'altra è chiedervi di prestarci … |

## Il giro

```bash
cp '08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md' /tmp/riscritto.md         # si riscrive la copia, mai l'originale
python3 scripts/ciclo_prosa.py misura '08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md' /tmp/riscritto.md
# … si ritocca quello che resta, e si rimisura
python3 scripts/ciclo_prosa.py revisione '08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md' /tmp/riscritto.md -o REVISIONE.md
```

Ci si ferma quando un giro non abbassa le segnalazioni, o al giro 3.
Il documento di revisione va al DM, che approva modifica per modifica (D15).
