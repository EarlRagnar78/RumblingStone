# Giro del 2026-10-18 sui cinque master di ARC-07

Il DM, dopo l'unione della PR #243: *«riscrivere i booklet dell'arco 07 e
misurare il miglioramento rispetto alla versione precedente con un altro giro
di playtester, developer e DM, e avere il booklet aggiornato»*.

Il giro ha avuto quattro passi:

1. **Le letture.** Per ognuno dei cinque DEF hanno letto un developer, un
   playtester e un DM a freddo, quindici letture in tutto. Le rubriche erano
   quelle di `rumblingstone-playtest/references/` e di
   `rumblingstone-module-standard/references/sviluppo-degli-incontri.md`.
   Ogni lettore era un agente nuovo, che vedeva solo il master e la sua vista.
2. **La correzione.** Un correttore per DEF ha unito i rilievi doppi. Ogni 🔴 e
   🟠 ha avuto uno di tre esiti: corretto nel master, rimandato al DM se tocca
   canone o bilanciamento, oppure respinto con la riga che lo smentisce. Gli
   esiti sono in `DEF-n/FIX.md`.
3. **La verifica.** Un verificatore nuovo per DEF ha controllato ogni 🔴 e 🟠
   sul master corretto, e ha cercato gli errori introdotti dalla correzione.
   Il rapporto è in `DEF-n/VERIFICA.md`.
4. **Il secondo giro.** Il correttore ha chiuso i parziali e i nuovi trovati
   dalla verifica. È la sezione «Secondo giro» in fondo a `FIX.md`.

## Il confronto con i giri di prima

⚠️ I numeri dei giri precedenti non si confrontano uno a uno con questi. I
lettori di oggi sono agenti nuovi, e due rubriche sono cambiate nel frattempo:
il developer ha otto domande, e il DM a freddo esegue il primo passo intero.
Inoltre su DEF-1, 2 e 3 il developer e il DM a freddo non avevano mai letto.
La misura onesta del miglioramento è quindi dentro questo giro: prima e dopo
la correzione, sugli stessi rilievi.

Ultimo giro precedente per ciascun master, in 🔴·🟠·🟡:

| Master | Lettore | Playtester | DM a freddo | Developer |
|---|---|---|---|---|
| DEF-1 | 1·10·21 | 0·6·29 (giro 6) | — | — |
| DEF-2 | 0·7·16 | 0·4·12 | — | — |
| DEF-3 | 0·9·17 | 0·5·13 | — | — |
| DEF-4 | 0·5·16 (giro 4) | 0·6·17 | 0·8·11 | 1·7·24 (giro 1) |
| DEF-5 | 1·5·15 (giro 2) | 0·6·13 (giro 3) | 0·5·17 | 0·3·13 (giro 2) |

Questo giro, sui master di partenza (commit `c6e1999a`):

| Master | Developer | Playtester | DM a freddo | 🔴+🟠 |
|---|---|---|---|---:|
| DEF-1 | 1·10·12 | 1·13·22 | 0·17·20 | 42 |
| DEF-2 | 0·5·13 | 0·7·13 | 0·7·20 | 19 |
| DEF-3 | 0·10·11 | 0·10·23 | 0·8·20 | 28 |
| DEF-4 | 0·2·17 | 0·6·21 | 0·9·17 | 17 |
| DEF-5 | 0·5·16 | 0·4·12 | 0·5·11 | 14 |

I 🔴+🟠 sono 120 prima di togliere i doppi. I correttori hanno registrato 142
esiti, fra corretti, rimandati e respinti. I due numeri non coincidono perché
ogni correttore ha unito o diviso i rilievi a modo suo: il dettaglio è in
`FIX.md`.

Dopo la correzione e la verifica:

| Master | Corretti | Al DM | Respinti | Verifica: chiusi · parziali · aperti | Nuovi 🟠 | Dopo il secondo giro |
|---|---:|---:|---:|---|---:|---|
| DEF-1 | 23 | 6 | 0 | 22 · 2 · 0 | 0 | parziali chiusi |
| DEF-2 | 25 | 4 | 1 | 13 · 1 · 0 | 0 | parziali chiusi |
| DEF-3 | 23 | 9 + 1 | 2 | 12 · 4 · 0 | 0 | resta parziale M#21, che aspetta la Decisione 5 |
| DEF-4 | 16 | 6 | 0 | 6 · 3 · 0 | 1 | parziali e nuovo chiusi |
| DEF-5 | 22 | 4 | 1 | 7 · 3 · 0 | 1 | parziali e nuovo chiusi |

Il risultato: **nessun 🔴 o 🟠 resta aperto senza un esito**. La verifica non
ha trovato nessun nuovo 🔴. Ha trovato due nuovi 🟠, l'arco degli hobgoblin in
DEF-5 e uno in DEF-4, ed entrambi sono chiusi. Restavano le 29
decisioni del DM in [`DECISIONI-DM.md`](DECISIONI-DM.md).

## Le decisioni del DM

Il DM ha scelto «Tutte»: valgono le 29 raccomandate, e per i tre fatti che
solo lui sa vale il ripiego scritto nella decisione (Hella con SAG 20 e scudo
leggero; Varis si sente col guanto e si firma solo a pelle nuda; Therysol
resta com'è, perché DEF-2 e DEF-3 raccontano il passato e `state.md` il
presente). Ogni decisione è nel master con `[CANONE — DM 2026-10-18]`, e la
divergenza dall'SRD è dichiarata dove c'è. Nei cinque DEF non resta nessun
`[INFERRED]`.

Le decisioni toccano anche altri file, aggiornati nello stesso lotto: la voce
di Fauci di Diamante (GS 11 → 12, con `Boost log:`), una voce nuova per il
Treant di Adamantio, la scheda di Hella risorta, la Collana, la Cintura della
Devastazione (4 cariche al giorno, +2d6), `campaign-party.md`, gli handout di
ARC-07, la guida DM di ARC-08 per i pf di Dana e la mappa M7-C. `state.md`
non si tocca su `main`: la riga della Cintura è in una patch per il ramo di
gruppo, che applica il DM.

## Cosa misura `misura_craft`

| Master | righe prima → dopo | box | box > 12 righe |
|---|---|---:|---:|
| DEF-1 | 2679 → 2783 | 28 | 0 |
| DEF-2 | 1014 → 1046 | 19 | 0 |
| DEF-3 | 1368 → 1423 | 19 | 0 |
| DEF-4 | 3765 → 3817 | 35 | 0 |
| DEF-5 | 748 → 783 | 7 | 0 |

I box non sono cambiati. Le correzioni stanno nel testo per il DM: Quickstart,
tabelle, contingenze e righe «se i PG fanno…». Su DEF-1, 2 e 5 il congegno
`tattiche` è salito di 2-7, e su DEF-1 e 3 le `battute` sono salite di 4-16.
Sono indicatori e non voti.

## Cosa questo giro non ha potuto verificare

- **I numeri SRD sono stati confrontati dopo il giro, su mirror dell'SRD 3.5.**
  d20srd.org resta bloccato dal proxy, e Firecrawl non ha crediti. Hanno
  risposto il D&D Wiki, birthright.net e rpgcrossing.com, che riportano il
  testo SRD 3.5. Il rapporto è [`VERIFICA-SRD.md`](VERIFICA-SRD.md), con
  l'URL di ogni pagina: circa 40 voci confermate, compreso il rilievo #1 del
  developer di DEF-4, e 9 discrepanze, tutte corrette. Gli attacchi degli
  Xorn comuni sono passati a quelli SRD. Fauci ha la portata di 3 m e
  l'ottavo talento. Terros sale al livello dell'Elementale anziano dell'SRD:
  FOR 34, 9 m, schianto +33 (2d10+12), Lotta +42. Al Vecchio Skullcrusher
  sono stati corretti i raggi della Presenza e dell'*oscurità*. Il morso
  della viverna e la Volontà di Durin tornano col conto. Una cosa resta al
  DM: Terros ha Robustezza, quindi i pf darebbero 348 e non 345. Il numero
  non è cambiato, perché sposta le soglie 260 e 172 in più file, e lo
  scontro è già stato giocato. Restano non verificati la tabella PX, i
  servizi d'incantesimo, i tratti del tipo Elementale e il materiale non SRD.
- **`registro_letture.py` non registra queste letture.** Vuole una corsa di
  `lettura_a_scene.py` con `stato.json`, mentre queste letture sono state
  fatte sul master intero. In più sono state fatte prima della correzione.
  Il cancello resta verde, perché nessun master è sotto cancello. Gli avvisi
  «il dm ha letto un testo che non c'è più» restano veri.
- **Il lettore a freddo non ha riletto in questo giro.** Il DM ha chiesto
  developer, playtester e DM.
