# Ricerca: metodi misurabili per la prosa e l'architettura delle avventure

**Data**: 2026-10-22 · **Richiesta del DM**: cercare in rete metodi definiti e
misurabili per giudicare e migliorare la prosa fantasy (meno meccanica, meno
anglofona, bella e coerente) e l'architettura, la logica e la coerenza delle
avventure; applicarli al repo e farne standard dove migliorano qualità e
giocabilità.

**Fonti**: WebSearch e WebFetch (Firecrawl senza crediti). Testi di terzi non
copiati: solo riferimenti e citazioni brevi. Censimento del repo fatto prima
della ricerca, per non rifare ciò che esiste.

## 1. Cosa il repo misura già

La prosa ha molti rilevatori di difetti (calchi con firma certa, tic dell'IA,
tetti dei box, foglio di stile, MQM come cancello) e un solo giudice di
qualità: il cieco del DM ([ADR-0093](adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md)).
L'architettura ha le sezioni obbligatorie (`validate_modules`), il contratto
delle scene (`copertura_scene`), le domande del developer
([ADR-0092](adr/ADR-0092-le-domande-dell-alto-livello.md)) e le letture a freddo.
La coerenza ha i numeri degli statblocchi e l'invarianza dei fatti nelle
riscritture, non la verità fra scene e fra archi.

I buchi principali:

| Area | Cosa non è misurato |
|---|---|
| prosa | calchi sintattici oltre le sei regex; ripetizioni fra box; voce distinta dei PNG; il perché di un voto del DM |
| architettura | la domanda drammatica di ogni scena; la rete degli indizi (norma 🔴 in `rumblingstone-indagine`); scelte con conseguenza visibile; presagio del cattivo; topologia della mappa (lotto 2 di AVVENTURE-COMMUNITY, ⬜) |
| coerenza | fatti in contraddizione fra scene e archi; fronti e orologi senza schema |

## 2. Cosa c'è in rete, per la prosa

| Metodo | Fonte | Cosa dà | Per noi |
|---|---|---|---|
| **TTCW**, 14 test sì/no (ritmo, scena contro esposizione, cliché, mondo sensoriale, sottotesto) | Chakrabarty et al., CHI 2024, [arXiv 2309.14556](https://arxiv.org/abs/2309.14556) | κ fra esperti 0,27-0,66; i giudici LLM non correlano | checklist per il voto del DM, 5-6 test validi per un box |
| **LAMP**, tassonomia di 8.035 correzioni di scrittori su testi di LLM | Chakrabarty et al. 2025, [arXiv 2409.14509](https://arxiv.org/abs/2409.14509) | fraseggio goffo 28%, struttura 20%, esposizione ridondante 18%, cliché 17% | etichette per dire *perché* una versione perde |
| **HANNA**, 6 criteri Likert | Chhun et al. 2022, [arXiv 2208.11646](https://arxiv.org/abs/2208.11646), MIT | accordo umano basso (coerenza 0,29) | conferma che il voto assoluto è debole |
| **LitBench**, 43.827 coppie di preferenza | Fein et al. 2026, [arXiv 2507.00769](https://arxiv.org/abs/2507.00769) | il confronto a coppie batte il voto assoluto | conferma la scelta di ADR-0093 |
| **Slop Score** e **slop-forensics** | [github.com/sam-paech](https://github.com/sam-paech/slop-score), MIT | parole e trigrammi sovrarappresentati nei testi di LLM, «not X but Y» | il metodo si trasferisce, le liste inglesi no |
| **Translationese italiano**: possessivi, pronomi soggetto, dimostrativi | Ondelli e Viale, [JADT 2010](https://www.ledonline.it/ledonline/JADT-2010/allegati/JADT-2010-0573-0584_013-Ondelli.pdf) | differenze piccole, giornalismo, senza test | segnali, non soglie |
| **Anglicismi sintattici**: soggetto preverbale con informazione nuova, aggettivo complesso prima del nome, stare + gerundio | Cerruti, [Il Segno e le Lettere](https://www.ledonline.it/Il-Segno-le-Lettere/allegati/728-Contatto-Interlinguistico-Cerruti.pdf) | regole su analisi a dipendenze | servono Stanza o spaCy, non installati |
| **READ-IT**, **Profiling-UD** | ItaliaNLP Lab ([W11-2308](https://aclanthology.org/W11-2308.pdf), [LREC 2020](https://aclanthology.org/2020.lrec-1.883)) | leggibilità su quattro livelli di tratti | READ-IT è un servizio, il codice non è libero |
| **Norme percettive italiane**, 1.121 parole valutate sui cinque sensi | Vergallito et al. 2020, [BOA Bicocca](https://boa.unimib.it/handle/10281/267364), CC BY 4.0 | il dettaglio sensoriale diventa un numero | copertura limitata |
| **MATTR**, sovrapposizione fra frasi adiacenti (alla TAACO) | McCarthy e Jarvis 2010; [TAACO](https://soletlab.asu.edu/taaco/) | diversità lessicale e coesione | MTLD è instabile sotto le 100 parole |

## 3. La prova: queste misure prevedono il voto del DM?

Ogni misura della §2 calcolabile senza parser l'ho provata sulle **38 coppie
già votate alla cieca** dal DM (giro 2: 16, giro 3: 9, prova del 2026-10-21:
13). Per ogni coppia: la misura è più alta nella versione vincente o nella
perdente? Una misura utile dovrebbe stare dalla parte del vincitore molto più
spesso di metà delle volte.

| Misura | vincente più alta | più bassa | pari | p (binomiale, due code) |
|---|---|---|---|---|
| possessivi ‰ | 11 | 3 | 24 | 0,057 |
| deviazione standard delle frasi | 14 | 22 | 2 | 0,24 |
| sovrapposizione fra frasi adiacenti | 13 | 8 | 17 | 0,38 |
| Gulpease | 21 | 17 | 0 | 0,63 |
| dettagli sensoriali ‰ | 20 | 16 | 2 | 0,62 |
| MATTR (finestra 25) | 20 | 17 | 1 | 0,74 |
| parole | 19 | 17 | 2 | 0,87 |
| pronomi soggetto, dimostrativi, «non X, ma Y», verbi di filtro, emozioni nominate, connettivi in apertura, -mente, gerundi in coda | quasi sempre pari | | | non valutabili |

**Nessuna misura prevede il DM.** L'unico segnale vicino alla soglia va nel
verso *opposto* all'ipotesi del translationese: le versioni che vincono hanno
più possessivi, non meno. Leggo questo come un indizio che il DM premia il
referente chiaro («la sua ascia») più della forma «italiana da manuale», ma su
14 coppie con differenza non è una prova. I tic che la letteratura segnala
(«non X, ma Y», verbi di filtro, emozioni nominate) nei nostri box sono già
quasi a zero, perché i rilevatori del repo li hanno tolti.

Due limiti onesti. Le coppie sono riscritture leggere, quindi le differenze
sono piccole e la prova ha poca potenza. E nessun indice della §2 ha una
correlazione pubblicata col giudizio umano sulla narrativa italiana.

**Conclusione per la prosa.** Le misure automatiche della letteratura non
diventano cancelli: aggiungerebbero norme che non spiegano le scelte del DM.
Quello che manca è sapere *perché* il DM sceglie. Il voto cieco può portare,
facoltativa, un'etichetta presa da LAMP e TTCW, e dopo una cinquantina di voti
etichettati si rifà questa prova sulle misure che corrispondono alle etichette
più frequenti.

## 4. Cosa c'è in rete, per l'architettura

| Criterio | Fonte | Regola verificabile |
|---|---|---|
| **Three Clue Rule** e struttura a nodi | J. Alexander, [The Alexandrian](https://thealexandrian.net/?p=7985) | ogni conclusione ha ≥3 indizi da ≥2 nodi; nessun nodo raggiungibile da un arco solo |
| **Domanda drammatica** e punti di decisione | Angry GM, [four things](https://theangrygm.com/four-things-youve-never-heard-of-that-make-encounters-not-suck/) | ogni scena giocabile ha una domanda sì/no e ≥2 decisioni; l'atto ha un «se falliscono» che non è la morte |
| **Agency**: conseguenza percepibile | Wardrip-Fruin et al., [DiGRA 2009](https://www.cs.uky.edu/~sgware/reading/papers/wardripfruin2009agency.pdf) | ogni «Se i PG…» rimanda a una scena dopo o a un'eco |
| **Fronti** | Dungeon World, [Fronts](https://roll20.net/compendium/dw/Rules:Fronts) | 2-3 pericoli per fronte, impulso, 1-3 presagi, catastrofe |
| **Orologi** | Blades in the Dark, [Progress clocks](https://roll20.net/compendium/BITD/Rules:Progress%20clocks) | 4, 6 o 8 segmenti, riempiti ≤ totale, «quando si riempie» |
| **Presagio del cattivo** | Bryce Lynch, [standard](https://tenfootpole.org/ironspike/?page_id=1201) | il boss è nominato o indiziato in ≥2 scene prima dello scontro |
| **Chiave della stanza** | J. Alexander, [Art of the Key 2](https://thealexandrian.net/wordpress/35201/roleplaying-games/the-art-of-the-key-part-2-the-essential-key) | box, poi prove reattive, poi grassetti, poi antefatto breve |
| **Jaquaying** | J. Alexander, [Jaquaying](https://thealexandrian.net/wordpress/13085/roleplaying-games/jaquaying-the-dungeon) | ingressi ≥2, almeno un anello per livello (già nel lotto 2 di AVVENTURE-COMMUNITY) |
| **Formato AP** | Paizo, [RPG Superstar](https://paizo.com/blog/rpg-superstar-trade-advice-from-your-future) | ~500 parole per incontro, antefatto ≤2 pagine |
| **Motivazioni delle quest** | Doran e Parberry, [PCG 2011](https://ianparberry.com/pubs/pcg2011.pdf) | varietà: non più del 40% delle missioni con la stessa motivazione |

Una prima conta sui cinque master di ARC-07: **la domanda drammatica non è
scritta come domanda in nessuna delle 39 scene** (una sola «posta in gioco» in
DEF-2). Contando anche l'«Obiettivo» scritto, 14 scene di scontro o sociali
restano senza né l'una né l'altro (D18, lotto 7b), e il
«se falliscono» non mortale c'è in 2 master su 5. Il «Se i PG…» c'è ovunque
(35 blocchi), ma niente dice se porta a una conseguenza visibile.

A differenza della prosa, queste regole non chiedono di prevedere un gusto:
sono regole di mestiere accettate (la Three Clue Rule è il riferimento del
settore), e un loro mancato rispetto è un difetto che il tavolo paga. Si
misurano come le domande del developer di ADR-0092: prima una calibrazione
sui master esistenti (quanti rilievi sono difetti veri), poi il cancello solo
sui master nuovi.

## 5. Proposta

Diventa il lotto 7 di [PIANO-AVVENTURE-COMMUNITY](PIANO-AVVENTURE-COMMUNITY-2026-10.md), che ha già il lotto 3 «indagine» aperto sulla stessa materia (regola d'apertura di ADR-0044). Le domande al DM stanno lì, nella §2 del lotto.
