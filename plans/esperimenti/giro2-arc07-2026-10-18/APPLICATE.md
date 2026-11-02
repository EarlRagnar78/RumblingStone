# Giro 2 ARC-07 — decisioni applicate ai cinque master

Questo file dice che cosa è entrato nei master ARC07-DEF-1…5 dalle
raccomandazioni di [`DECISIONI-DM.md`](DECISIONI-DM.md), con l'opzione «Tutte».
Il DM non ha ancora risposto alla scheda: ogni modifica porta un tag
`[CANONE — DM 2026-10-18, G2-NN]` o sta in una riga che cita il codice. Per
annullarne una basta cercare il codice nei master (`grep -n "G2-NN"`). Il tag
non va in stampa, perché `togli_storico` toglie i `[CANONE …]`.

Niente commit: le modifiche sono nella copia di lavoro.

## Conteggio degli `[INFERRED`

| File | Prima | Dopo |
|---|---:|---:|
| ARC07-DEF-1-PIANO-TERRA-TERROS.md | 6 | 1 |
| ARC07-DEF-2-RITORNO-E-AFFRESCHI.md | 9 | 0 |
| ARC07-DEF-3-RESURREZIONE-HELLA.md | 5 | 1 |
| ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md | 0 | 1 |
| ARC07-DEF-5-RITORNO-HAMMERFIST.md | 4 | 2 |
| **Cinque master** | **24** | **5** |
| Mappe/ARC07-MAPPE-DEFINITIVO.md | 1 | 0 |

I cinque `[INFERRED` rimasti sono le parti numeriche di decisioni che le
fonti non coprono. Tre sono nuovi, perché hanno separato la regola, ormai
canone, dal numero ancora da decidere (DEF-3, DEF-4, DEF-5 r.775). Nei master
ci sono 80 tag `G2-NN]`.

## Le decisioni una per una

G2-02, G2-03 e G2-13 sono chiuse o barrate nel file delle decisioni e non
compaiono.

| Codice | Applicata / Lasciata INFERRED / Non applicabile | Dove (master §) | Nota |
|---|---|---|---|
| G2-01 | Applicata | DEF-2 §0-bis · DEF-3 §0, §9 riga del sonno | −4 h prima del rito, 8 h dopo |
| G2-04 | Applicata | DEF-2 §8 · DEF-3 §8-ter | Una porta sola |
| G2-05 | Applicata | DEF-2 §6, tabella delle stanze, ponte §11 · DEF-3 §0-bis riga 5, §5 Il richiamo | +1 senza tipo al TS Volontà dello Step 5 |
| G2-06 | Applicata in parte | DEF-1 §2, §7b · DEF-2 §7 · DEF-3 Mantello, Incarnato | 24 ore vissute per tutte. Su Incarnato frequenza, azione e durata di ogni uso restano INFERRED (DEF-3 r.1249) |
| G2-07 | Applicata | DEF-3 §0 · DEF-5 «Con tre giocatori» | Tira un giocatore presente, le scelte di canone restano al giocatore assente |
| G2-08 | Applicata | DEF-4 Scena 10, Scena 11 «Il re», A.5 · `Bestiario/png/re-thorek-i-cr16.md` | Soglia a colpi. Nel Bestiario corretti Key stats, Source, Status e nota, perché lo statblocco completo non esiste. Il titolo non è stato toccato, per non rompere il catalogo |
| G2-09 | Applicata | DEF-2 S-1 · `Mappe/ARC07-MAPPE-DEFINITIVO.md` S-1 | Lato sud. S-1 è solo ASCII, senza JSON: corretti la legenda e «Posizioni notevoli». `render_map_svg` non ha cambiato nessun SVG. Durik e la distanza di circa 19 m c'erano già |
| G2-10 | Non applicabile | — | È una domanda da fare ai giocatori |
| G2-11 | Applicata | DEF-3 §0 | Si rinvia; se non si può, «Frase prima» |
| G2-12 | Applicata | DEF-3 §8-bis | Torna come *resurrezione*. «prepara» diventa «ripassa gli incantesimi» |
| G2-14 | Applicata | DEF-4 §6 · DEF-5 Scena 1 | Torna tutto |
| G2-15 | Applicata | DEF-4 riquadro delle wyvern, Scena 11 | Sì, scortano |
| G2-16 | Applicata | DEF-2 §0-bis | Le ore da svegli costano per intero |
| G2-17 | Applicata | DEF-2 Scena 1 riga «bottega», §8 | Solo riti |
| G2-18 | Applicata | DEF-1 §0 · DEF-2 · DEF-3 (più tre righe: Altare, Doni, parlare con i morti) · DEF-5 (blocco nuovo) | Su DEF-5 il blocco porta il tag CANONE, ma le risposte le ho scritte io e restano INFERRED (DEF-5 r.144): il DM non le ha viste |
| G2-19 | Applicata | DEF-3 riga 2-su-3 | Il primo uso va perso |
| G2-20 | Applicata | DEF-3 §0, §9 riga Therysol, riga 0-su-3 | Tiene il Sud chi non officia: Therysol, Durik o un quinto PG. I tre officianti tirano |
| G2-21 | Applicata | DEF-3 sotto la tabella §0-bis | Niente 10, niente aiuti; gli incantesimi lanciati prima valgono |
| G2-22 | Applicata | DEF-3 §9 | Il Cuore si tocca e basta. Il seme resta chiuso fino ad ARC-09 |
| G2-23 | Applicata | DEF-3 §9 | Durante l'ora d'indagine non si dona |
| G2-24 | Applicata | DEF-4 Scena 8, Scena 11 | Vince la picchiata |
| G2-25 | Applicata | DEF-4 Scena 7 | Morte vera |
| G2-26 | Applicata in parte | DEF-4 Scena 9 | L'urlo dà l'allarme (canone). La CA 15 di Vatore e i tempi della ronda restano INFERRED (r.2671): nessuna fonte per il numero |
| G2-27 | Applicata | DEF-4 Scena 9, blocco nuovo «Se lo divinano: Vatore, il Sigillo, Zeth» | Una mezza verità per segreto |
| G2-28 | Applicata | DEF-4 Appendice B | Sempre acceso, tranne in mano ad Artemis |
| G2-29 | Applicata | DEF-4 Scena 6, Scena 7 | Lo stato di Grask cambia all'atterraggio |
| G2-30 | Applicata | DEF-4 Scena 13 | Senza modifiche al testo: il taglio era già nel master |
| G2-31 | Applicata | DEF-5 round 6, A.5 | Le frecce tirano contro la CA di contatto di Dana, 14 |
| G2-32 | Applicata | DEF-5 Scena 2, tabella «Dove» e tattiche | Già dentro l'anello. La legenda di CM-1 nell'Atlante ora lo dice; la griglia resta lo stato dell'arrivo, con l'ondata alla porta |
| G2-33 | Applicata | DEF-5 Scena 2, sotto la tabella dei gesti | Una volta per scena |
| G2-34 | Applicata in parte | DEF-5 §6 | Il potere viene dall'altare (canone). Quanto resta aperto il portale resta INFERRED (r.775) |
| G2-35 | Applicata | DEF-5 Scena 2, ramo meno luminoso | Troppo tardi per murare il varco |
| G2-36 | Applicata | DEF-5 Quickstart | Tag |
| G2-37 | Applicata | DEF-5 §0-ter | Tag |
| G2-38 | Applicata | DEF-5 Scena 2 | Tag, e una riga: nel ramo duro il fischio arriva con l'ingresso degli scudi |
| G2-39 | Applicata | DEF-5 Scalare | Tag |
| G2-40 | Applicata | DEF-1 §7a Navigatore | Una spinta sola, con nota Non-SRD. Il «Prendere 10 = 26» è ancora da confermare |
| G2-41 | Applicata | DEF-1 §8 | Diventano sonici il danno senz'armi e il Pugno Frana, il fuoco no |
| G2-42 | Applicata | DEF-1 §8 Contingenze | Duello formale fino all'arrocco, a 172 pf |
| G2-43 | Applicata in parte | DEF-1 §5 | La striscia la sceglie chi legge la pietra (canone). Le misure 3×30 m restano INFERRED (r.689) |
| G2-44 | Applicata | DEF-1 §7, regola di caduta §3 | Un round a prova; al terzo fallimento cade chi sta sui blocchi |
| G2-45 | Applicata | DEF-1 §9 Fase 1 | Nuovo punto sul rifiuto: si riposa, e al secondo rifiuto la Corona prende |
| G2-46 | Applicata | DEF-1 §7a | Nessun aiuto da Aegis Fang |
| G2-47 | Applicata | DEF-1 §7b | Tre attacchi sempre |
| G2-48 | Applicata | DEF-1 §8 Scalare | Spinta 26, Radice 25, segno canone. Mancano ancora Boost log e benchmark (DEV#20) |
| G2-49 | Applicata | DEF-1 §8 Contingenze | La fatica non si cura nel Piano |
| G2-50 | Applicata | DEF-2 §4-bis, N4 | CD confermate; N4 passa per Sapienza Magica CD 20. `componenti.py` ha rigenerato l'APPARATO di DEF-4, con una riga CD in più |
| G2-51 | Applicata | DEF-2 §0 | Anche A8 tra le cose da non tagliare mai |
| G2-52 | Applicata | DEF-2 §4, A3 | Tag |
| G2-53 | Applicata | DEF-2 §4-bis | Muti per tutto l'arco |
| G2-54 | Applicata | DEF-2 §8 | Il giuramento rotto vela il pannello A8 |
| G2-55 | Applicata | DEF-2 §4, A6 | Tag |
| G2-56 | Applicata in parte | DEF-4 r.1451 | Nel master è entrato solo il tag. Lo scalo dalla cassa del 1372 va nel registro del ramo di gruppo: non applicabile qui |
| G2-57 | Non applicabile | — | Riguarda i PE del ramo di gruppo, e la decisione spetta al DM |
| G2-58 | Applicata in parte | DEF-3 storico K3 | Una riga sulla regola per i gruppi futuri. Il prezzo riscosso sta nel ramo di gruppo |

## Cancelli

Tutti verdi dopo le modifiche:

- `componenti.py --apparato`
- `misura_craft.py --box`: 142 riquadri, nessuno oltre le 12 righe, nessuna parentesi. Uno ha più di un nome proprio, in DEF-5, ma c'era già
- `validate_modules.py`
- `domande_developer.py --check`: 18 rilievi, tutti dichiarati
- `copertura_scene.py --check`: 15 rilievi, tutti dichiarati
- `test_storico.py`: 8 passati
- `validate_bestiario.py`
- `validate_maps.py`
- `decisioni_dm.py --check`

`validate_prosa` segnala «sta guardando» in DEF-4 r.3249. La riga c'era già
prima di queste modifiche.
