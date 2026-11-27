# Esito della prova A/B del lotto 2 (ADR-0114)

Skill vecchie (main c83b95a) contro skill nella scheda (lotto 2), 54 consegne con
trappola, un'esecuzione per versione, lettere a caso. Ogni esecutore lavorava su
una copia del repo senza `skills/*/evals/` e senza le consegne dell'esperimento,
così non poteva leggere la trappola. Un giudice per skill ha contato alla cieca
(`giudizi.json`, chiave in `chiave.json`). Le 108 risposte sono fuori dal repo,
in `/mnt/project-files/standard-prompt-2026-11-08/ab-lotto2/`.

| Misura (somma sui casi) | Vecchia | Nuova |
|---|---:|---:|
| inventati_senza_marca | 32 | 30 |
| marche | 98 | 115 |
| marche_con_domanda_e_base | 74 | 95 |

Per caso: la nuova inventa meno in 4, di più in 4, pari in 46. Test del segno a
una coda: p = 0,637. **La nuova non peggiora gli inventati senza marca**, e non
li migliora in modo dimostrato. Quello che cresce sono le marche nella forma
giusta, con domanda e base (+28%).

Per skill, gli inventati sono uguali in 14, scendono in 3 (indagine 19 → 16,
module-standard 8 → 7, narrative-style e playtest 1 → 0) e salgono in 2:
`npc-villain-boosting` 1 → 2 (un'etichetta GENERATO usata male) e
`dnd-35-srd` 0 → 3 (regole SRD dette a memoria: l'incidente di Usare Oggetti
Magici, la penalità della raffica a Monaco 9, un talento bonus inesistente).

## Rimisura di dnd-35-srd

La scheda nuova di `dnd-35-srd` ha lo stesso contenuto della vecchia, riordinato.
Si è aggiunta una domanda a «Prima di consegnare» (regole SRD lette, non a
memoria) e si sono rifatte le 3 consegne con due esecuzioni per versione, un
giudice alla cieca su 12 risposte (`rimisura-srd-*.json`).

| Misura | Vecchia | Nuova |
|---|---:|---:|
| inventati_senza_marca | 3 | 3 |
| marche | 13 | 15 |
| marche_con_domanda_e_base | 13 | 15 |

Pari. Lo 0 → 3 della prima tornata era rumore di un'esecuzione sola: lo stesso
errore (la raffica a Monaco 9) compare in tutte e due le versioni, quindi è un
difetto del contenuto, non della scheda.

## Che cosa non dice

- Un'esecuzione per consegna è poco: le differenze per skill sotto 3 fatti
  stanno nel rumore, come mostra la rimisura.
- Il giudice è un modello e conta con il suo metro; il riscontro vero resta il
  DM al tavolo.
- La prova misura le invenzioni sulle trappole, non la qualità della prosa né il
  costo in token.
