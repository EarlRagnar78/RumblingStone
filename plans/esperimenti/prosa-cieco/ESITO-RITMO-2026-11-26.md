# Il ritmo della frase al cieco: il repo contro le case

**Data**: 2026-11-26 · **Protocollo**: [ADR-0093](../../adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md) · **Ricerca**: [RICERCA-PROSA-PECULIARE-2026-11](../../RICERCA-PROSA-PECULIARE-2026-11.md) §3.4 · **Materiale**: [`ritmo-2026-11-19/`](ritmo-2026-11-19/)

**Esito: nessuna differenza dimostrata, con la frase breve davanti.** Sulle 20
coppie non di controllo il DM ha preferito 13 volte la versione con le frasi
brevi e 7 volte quella con le frasi più lunghe. La soglia scritta prima del
voto era 14 su 20, quindi non è raggiunta. Come stabilito prima del voto, non
si tocca niente: il ritmo del repo non si corregge verso quello delle case e
non diventa una caratteristica dello standard.

## La domanda

I box del repo hanno frasi più corte di quelle delle case. Nel corpus del
2026-11-19 la mediana è di 11-15 parole per frase in ARC-07, 08 e 09, contro
16 per Dragons' Lair, 17 per Chimera e 18 per Paizo. Nessuno aveva mai scelto
questo scostamento. Il cieco doveva dire se tenerlo come tratto proprio, se
riallinearlo alle case o se lasciarlo com'è.

## Come era costruito

Il LEGGIMI è stato scritto prima del voto e c'è ancora, insieme alla scheda,
alla chiave e ai testi delle due versioni. All'epoca la chiave stava in una
cartella a parte, chiusa fino al voto.

- Il campione l'ha fatto `cieco_versioni.py campione` con il seme 20261119:
  5 box per file da sette file di ARC-08 e ARC-09, per un totale di 34. Prima
  dell'estrazione sono stati tolti i 4 box che non sono voce del narratore,
  cioè una nota per il DM e tre battute o monologhi di PNG. Sui 30 rimasti
  sono stati estratti 24 box con lo stesso seme. ARC-07 è rimasto fuori per
  via della serata in corso e dei box congelati.
- Entrambe le versioni sono riscritte, così nessuna è il testo del repo.
  Cambia solo la lunghezza delle frasi: la mediana è di 11 parole per la
  versione breve e di 16 per la lunga. Nelle due versioni restano uguali i
  nomi, i sensi e gli avverbi in -mente, e l'ultima frase è identica. La
  lunghezza totale non scarta di oltre il 10% (1.546 parole contro 1.604).
- A e B sono stati ordinati a caso con il seme 1119. Per lo strumento la
  versione «nuova» è la lunga.
- Nelle quattro coppie di controllo una delle due versioni ha un dettaglio
  sensoriale in meno.

## Il voto

Il DM ha votato le coppie 1-20 il 2026-11-25 e le coppie 21-24 il 2026-11-26.

| | Coppie |
|---|---:|
| vince la breve (ritmo del repo) | 13 |
| vince la lunga (ritmo delle case) | 7 |
| pari | 0 |
| intervallo di Wilson al 95% sulla quota della breve | 0,43-0,82 |

L'intervallo contiene 0,5, per cui il risultato è compatibile con nessuna
preferenza. Pende però dalla parte della frase breve: un cieco più lungo
potrebbe arrivare alla soglia, ma questo non lo dimostra.

`esito` riporta «nuova 9 · vecchia 15 su 24», perché conta anche i controlli
e li misura sulla soglia di 24. Il conto valido è quello sulle 20 coppie non
di controllo, come diceva il LEGGIMI.

## I controlli

Il DM ne ha confermati 2 su 4. Nelle coppie 1 e 7 ha scelto la versione con un
dettaglio sensoriale in meno: «conta le tende» al posto di «conta i fuochi», e
lo stendardo senza «rosso». Per `esito` questo basta a dire «misura smentita».
Qui però la misura non ha deciso nessuna coppia, perché tutte e 24 sono andate
al voto. Il controllo dice un'altra cosa: **una sola parola di senso in meno
non decide la scelta**. La regola 1 del §2-ter di `read-aloud-adulti.md` (5 su
5) nasce da riscritture che toglievano più dettagli. Resta valida, ma
`verdetto_misurato` la applica già a una parola di differenza, ed è più
fiducioso di quanto i voti giustifichino. Prima di cambiarlo serve un cieco
fatto apposta.

## Che cosa ha visto il DM, oltre al voto

- **Due frasi oscure del repo.** Non vengono dalla riscrittura ma dai master:
  «marciano anche da fermi» (ARC08-DEF-1, Fase 3) e «prende la luce delle
  torce e la tiene» (ARC08-DEF-2, Scena 9). Vanno corrette sul file, una
  alla volta e con il sì del DM (ADR-0077).
- **I nomi dei luoghi.** Il box di Rhest usa i nomi del libro, mentre
  `fr-cannath-vale.md` indica Lhesper e Lhespenbog. Il DM ha scelto i nomi
  della Cannath Vale (card del 2026-11-25), e la sostituzione nei file di
  gioco la fa un thread a parte.

## Limiti

- In 4 coppie la battuta di un PNG pesa per metà del box ed è uguale nelle due
  versioni. In quelle coppie il voto dipende poco dal ritmo.
- La mediana delle case viene da box inglesi (Paizo) e da due editori italiani
  di traduzioni. È un ordine di grandezza.
- C'è un solo votante, e conosce bene il testo del repo: l'abitudine al suo
  ritmo può pesare.
