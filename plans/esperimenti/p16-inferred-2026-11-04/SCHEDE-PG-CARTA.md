# Le schede di carta dei PG (foto del DM, 2026-11-05)

Fonte delle caratteristiche dei PG per il lotto P16 «PG» (e per il 4g-2 di
ADR-0088). Il DM ha mandato il 2026-11-05 la foto del foglio con i quattro PG,
«le schede attuali con gli oggetti e le modifiche». La foto sta nei file del
progetto (`/mnt/project-files/schede-pg-2026-11-05/scheda-dm-2026-11-05.jpg`) e
non nel repo; qui c'è la trascrizione.

## Trascrizione

| PG | Classe | FOR | DES | COS | INT | SAG | CAR | Temp | Rifl | Vol | CA (sprovv., contatto) | PF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Thorik Skulldark | Guerriero 13 | 20 | 12 | 16 | 13 | 12 | 9 | 13 | 6 | 11 | 28 (27, 17) | 115 |
| Tordek Durinheart | Guerriero 4 / Monaco 9 | 20 | 16 | 16 | 14 | 18 | 8 | 14 | 11 | 12 | 24 (21, 21) | 106 |
| Artemis Blackrock | Warlock 13 | 10 | 18 | 14 | 10 | 10 | 18 | 7 | 8 | 8 | 25 (21, 16) | 74 |
| Hella Stonehead | Ranger 1 / Druida 12 | 16 | 13 | 12 | 12 | 18 | 10 | 10 | 7 | 12 | 22 (21, 12) | 80 |

Oggetti scritti sulle righe dell'armatura e delle armi:

- **Thorik.** Armatura completa di mithral +1, scudo pesante +1, armatura naturale +1, anello di protezione +1. Armi: Aegis Fang e scudo. Nessun oggetto dà caratteristiche. Modificatori ai tiri salvezza: +1 contro trappole, +2 contro veleno, +2 contro incantesimi, +1 contro paura.
- **Tordek.** Armatura +1 `[INFERRED — L'«armatura +1» della carta è l'amuleto dell'armatura naturale +1?; base: la scheda PCGen al 12° livello ha l'amuleto, e il contatto 21 della carta torna solo se Tordek non porta armatura, perché un monaco in armatura perde il bonus di Saggezza alla CA]`, bracciali, anello +3, arco composito +4. Non scritto sulla carta: *mantello della resistenza +1* (+1 a tutti i tiri salvezza), dalla scheda PCGen al 12° livello `[CANONE — DM 2026-11-21, card «Sì, mantello della resistenza +1»]`. Le caratteristiche coincidono con la scheda PCGen già nel repo.
- **Artemis.** Giaco di maglia di mithral +2, buckler. Nessun oggetto dà caratteristiche.
- **Hella.** Cuoio borchiato, scudo, anello di deviazione +1, amuleto.

I numeri più incerti nella foto sono i bonus di alcune righe e le abilità. Le caratteristiche sono state lette sulla foto ingrandita.

## Decisioni del DM (2026-11-05; Tordek 2026-11-21)

- **Tordek.** È Guerriero 4 / Monaco 9, come in `campaign/state.yaml`: la trascrizione diceva Barbaro 9, e il DM ha confermato il Monaco il 2026-11-21. I tiri salvezza della carta tornano con il Monaco (Temp 13, Rifl 10, Vol 11, più il +1 del *mantello della resistenza +1* indossato nella scheda PCGen al 12° livello, `PG/Artefatti/Artefatti-Pg/Tordek/Tordek Durinheart 12 lvl modificato.pdf`), non con il Barbaro (Rifl 7, Vol 8).
- **Thorik.** Il colpo di Zog'tar dell'ultima serata è entrato contro la CA 28 della carta, quindi al tavolo la carta non aveva ancora i prezzi dei riti. Il DM dice che la DES 12 della carta ha già il −2 della Corona, e manca il rito dello Smeraldo (−2 DES, +2 COS, +4 CAR). Il risultato è FOR 20, DES 10, COS 18, INT 13, SAG 12, CAR 13. Si porta dietro Riflessi 5, CA 27 (sprovvista 27, contatto 16) e PF 128. Il colpo di Zog'tar resta buono: con una CA più bassa entrava lo stesso.
- **Artemis.** I valori della carta, nessun modificatore permanente.
- **Hella.** La carta non è stata aggiornata dopo il rito. Sulla riga dei tiri salvezza c'è «amuleto SAG +2» e «guanti della forza dell'orco +2», e il DM conferma che l'amuleto è di Saggezza. Il risultato:
  - FOR 16, cioè 14 più i guanti;
  - DES 13, COS 12, INT 12, CAR 10;
  - SAG 20: base 16 più il +4 della Collana. Il Periapto non si somma, perché sono due bonus di potenziamento.

  Il DM poi ha detto anche: «ha quello che c'è scritto nella carta». Quindi l'equipaggiamento è quello della carta:
  - corazza di piastre di pelle di drago +1, con il cristallo del riposo e un secondo cristallo che non si legge tutto;
  - brocchiere, Anello di Deviazione +1, anello degli incantesimi (3 livelli), Mantello dello Svanire;
  - guanti, periapto e ascia nanica di adamantio.

  Lo statblocco A.1 di DEF-3 e il tesoro C di §11 sono allineati: CA 25 (contatto 12, colta alla sprovvista 24) con il +3 naturale della Collana, 80 PF, tiri salvezza +11/+7/+13, Lotta +13.

## Riscontro con le abilità senza gradi

Nelle abilità senza gradi il numero è il bonus della caratteristica più la penalità dell'armatura. Penalità della carta: Thorik −5, Tordek 0, Artemis 0, Hella −5.

- **Thorik.** Equilibrio −4 vuol dire DES 12 (+1) al momento della scrittura. Valutare 1, Raggirare −1, Guarire 1 e Cercare 1 danno INT 13, CAR 9 e SAG 12. Concentrazione 2 andrebbe con COS 14: forse è una riga rimasta da prima di un aumento. Si tiene COS 16.
- **Tordek.** Valutare 2, Raggirare −1 e Guarire 4 tornano con 20/16/16/14/18/8.
- **Artemis.** Equilibrio +4, Raggirare +4, Scalare 0, Guarire 0 e Cercare 0 tornano con 10/18/14/10/10/18.
- **Hella.** Le righe tornano tutte con 16/13/12/12/18/10:
  - Equilibrio −4 vuol dire DES 13;
  - Scalare −2 vuol dire FOR 16;
  - Saltare −8 conta anche il −6 della velocità di 6 m;
  - Concentrazione 17 vuol dire COS 12 più 16 gradi;
  - Percepire Intenzioni 4 vuol dire SAG 18.

  I PF 80 vanno bene con COS 12. L'appendice A.1 di DEF-3 (COS 18, ~110 PF) non torna con la carta.

## Oggetti del Magic Item Compendium di Hella (DM 2026-11-05)

Il DM conferma che vengono tutti dal Magic Item Compendium. I dati sono presi dal testo del manuale:

| Oggetto | Prezzo | Cosa fa |
|---|---|---|
| Cristallo del riposo (*restful crystal*), sulla corazza | 500 mo | dormire con l'armatura addosso non affatica |
| Cristallo del ritorno (*crystal of return*), sull'ascia | 1.000 mo (minore) | estrarre l'arma è un'azione gratuita; se nessuno la tiene, la richiama in mano da 9 m come azione di movimento |
| Mantello dello Svanire (*vanisher cloak*) | 2.500 mo | 3 cariche al giorno, come *invisibilità* per 2-4 round, anche per gli alleati adiacenti |
| Anello degli Incantesimi Silenziosi (*ring of silent spells*) | 2.000 mo | 1 volta al giorno: *silenzio* su di lei e fino a tre incantesimi di 3° livello o meno senza componenti verbali |

Il cristallo del ritorno è un cristallo d'arma, non d'armatura, quindi va sull'ascia. Ho scelto il grado minore: il superiore aggiunge solo «ritornante», che funziona con le armi da lancio e all'ascia non dà niente. Il corredo vale circa 23.345 mo.
