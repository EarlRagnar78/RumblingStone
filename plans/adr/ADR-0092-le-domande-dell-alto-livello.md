# ADR-0092 — Le domande dell'alto livello entrano nel developer, e lo statblocco dice com'è senza preparazione

**Stato**: accettata
**Data**: 2026-10-18
**Decisione-fonte**: discussione DM del 2026-10-18 (lotto 1 di [PIANO-AVVENTURE-COMMUNITY](../PIANO-AVVENTURE-COMMUNITY-2026-10.md)), dalla [RICERCA-AVVENTURE-COMMUNITY](../RICERCA-AVVENTURE-COMMUNITY-2026-10.md)

## Contesto

Il DM ha chiesto di confrontare i master DEF con le migliori avventure della
community 3.5 e PF1e. La ricerca ha trovato lo standard già più severo della
media, con un buco preciso: l'alto livello. Chi scrive dall'11° in su (i giudici
di RPG Superstar, Pathfinder Society, Necromancer) scrive ogni segreto contro la
divinazione, scala ogni scontro e non mette orde di GS basso. Nei cinque master
di ARC-07, con i PG al 13°, la riga di scala manca in cinque scontri su otto, e nessun master dice cosa succede se il gruppo divina un segreto.

Lo statblocco di ADR-0091 ha già *Prima / Durante / Morale*. Non dice com'è il
PNG **senza** gli incantesimi di preparazione: 11 statblocchi su 37 del
Bestiario dichiarano una preparazione, e solo due scrivono quali numeri la
includono (Draxoksus, Ozyrrandion).

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Otto domande nuove nel developer, quattro misurate, valide dai master nuovi; la riga «Statistiche base» nello statblocco | entra dove si scrive (i master di ARC-08), e la misura c'è dal primo giorno | i cinque master di ARC-07 restano con i rilievi aperti, dichiarati |
| Applicare tutto anche ai master di ARC-07 | il repo sarebbe uniforme | sono già giocati, e la prosa di un master giocato si aggiunge e non si riscrive (D3 di MESTIERE-BANCHI) |
| Stampare lo statblocco senza preparazione, con la versione potenziata in nota | è il formato 3.5 classico | contro la regola del DM (ADR-0091 §4-bis): si stampa la versione più forte |
| Solo la ricerca, nessuna norma | costa zero | AGENTS.md G3: una norma senza misura e senza lotto non è arrivata |

## Decisione

**Le §9-§16 di `sviluppo-degli-incontri.md` sono domande del developer come le
prime otto, e lo statblocco di un PNG che si prepara porta la riga «Statistiche
base».**

1. **Le domande.** §9 il segreto e la divinazione, §10 la riga di scala per ogni
   scontro, §11 il mostro insostituibile, §12 il pericolo che qualcuno usa, §13
   l'incontro che resta uno, §14 il rinforzo che i PG vedono arrivare, §15
   niente orde di GS basso, §16 il PG fuori gioco per un TS. Le §9 e §15 valgono
   dal 9° livello.
2. **La misura.** `domande_developer.py` misura la forma di quattro: **D9** (un
   master con segreti in due scene e senza il blocco «Se lo divinano»), **D10**
   (uno scontro senza la riga di scala), **D15** (sei o più nemici contati senza
   ciò che li tiene in vita), **D16** (un effetto «salva o sei fuori» senza via
   d'uscita). Il livello del gruppo sta nel profilo (`apl`) di
   `plans/domande-developer.json`; dove manca vale il 13°. Le §11-§14 restano
   alla lettura, come la §8.
3. **Lo statblocco.** Si stampa potenziato, come vuole il DM. Quando *Prima del
   combattimento* dichiara incantesimi, pozioni o oggetti di preparazione, sotto
   le **Tattiche** va una riga:

   ```
   **Statistiche base** senza *scudo della fede* e *forza del toro*: CA 24, contatto 12; Mischia +18/+13 (1d10+7); TS Vol +9
   ```

   Solo i numeri che cambiano. E *Prima del combattimento* dice due cose:
   **se è avvisato** (quanti round gli servono, in che ordine lancia) e **se è
   sorpreso** (cosa fa senza preparazione).
4. **Da quando.** Per i master nuovi e per quelli che un lotto riscrive, a
   cominciare da ARC-08 (S1 di PIANO-MASTER-DEF), e per gli statblocchi che un
   lotto tocca. I rilievi sui master di ARC-07 sono residui dichiarati, con la
   ragione, in `plans/domande-developer.json`.

## Conseguenze

- Un master nuovo di ARC-08 nasce sotto D9, D10, D15 e D16 in `--check`, come è
  nato sotto D1-D6.
- La calibrazione sui nove moduli sotto cancello (il piano, §2): D10 trova 9
  scontri, **6 veri**; D9 ne trova 1, vero a metà; D15 ne trova 1, falso per
  intenzione; D16 nessuno, quindi **non è calibrata**. Sono indicatori: vedono
  la forma, non se la risposta regge.
- La riga «Statistiche base» si conta e non blocca: la conta il piano, e
  diventa un controllo quando il primo lotto di statblocchi la porta.
- Il DM che sorprende un boss non deve più ricalcolarlo a mano. In cambio lo
  statblocco cresce di una riga.
- Non entrano i subtier PFS, i punteggi da torneo, i limiti di parole, l'albero
  delle contingenze tolto, né il rifiuto del read-aloud (la ricerca, §4).

**Da rivedere se**: dopo i primi due master di ARC-08 la precisione di D10
scende sotto la metà (vuol dire che la forma non è la riga di scala), oppure il
playtester a freddo trova un segreto rotto da una divinazione in un master che
D9 dava per buono.
