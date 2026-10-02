# L11 · Il giro sulle skill di scrittura: i risultati

Il voto è `scripts/voto_scrittura.py`: ogni controllo chiama un rilevatore che
esiste già nel repo (`misura_craft`, `validate_prosa`) e una norma registrata.
I casi sono in `casi.json`: dieci, cinque di taratura e cinque di verifica, una
coppia per genere (apertura, combattimento, dialogo, testo per un giocatore,
documento del repo). I voti per corsa sono in `voti.json`, e un test li tiene
allineati ai testi.

## Le tre condizioni

| condizione | che cosa | taratura | verifica |
|---|---|---:|---:|
| A-senza | tre agenti senza le skill (una corsa rifatta, vedi sotto) | 86/96 (89%) | 81/99 (81%) |
| A-con | tre agenti con le skill com'erano il 2026-10-01 | 94/96 (97%) | 96/99 (96%) |
| B-con | tre agenti con le skill corrette sui fallimenti di taratura | 96/96 (100%) | 99/99 (100%) |
| C-con | tre agenti con le skill di L12 (indici, §1-bis, domanda 8 con `ciclo_prosa`), solo verifica | — | 98/99 (98%) |

Casi superati per intero (tutti i controlli), su tre corse:

| caso | insieme | genere | A-senza | A-con | B-con |
|---|---|---|---:|---:|---:|
| S01 | taratura | apertura | 0 | 3 | 3 |
| S02 | taratura | combattimento | 0 | 2 | 3 |
| S03 | taratura | dialogo | 0 | 2 | 3 |
| S04 | taratura | per un giocatore | 3 | 3 | 3 |
| S05 | taratura | documento | 3 | 3 | 3 |
| S06 | verifica | apertura | 0 | 2 | 3 |
| S07 | verifica | combattimento | 0 | 2 | 3 |
| S08 | verifica | per un giocatore | 3 | 2 | 3 |
| S09 | verifica | dialogo | 0 | 3 | 3 |
| S10 | verifica | documento | 3 | 3 | 3 |

## Cosa dicono, e cosa no

Le skill servono dove c'è una forma da rispettare: il box etichettato, il
dialogo nella forma `**NOME (tono):**`, P1, il finisher al giocatore. Senza le
skill nessuno dei sei casi di box o di dialogo passa intero; con le skill
passano quasi tutti. Sui testi per un giocatore e sui documenti le tre
condizioni si equivalgono: lì `AGENTS.md`, che ogni agente riceve comunque,
basta.

Il passaggio da A-con a B-con sulla verifica (96% → 100%) è piccolo e va letto
con prudenza. Le correzioni alle skill erano mirate ai due fallimenti di
taratura (etichetta su ogni box, tono breve nel dialogo), e in verifica il
dialogo sbagliato non c'è più. Ma sono tre corse per condizione: un caso in più
o in meno sposta tre punti.

Il voto misura la conformità alle norme, non se la prosa è bella. Quello resta
alla lettura ad alta voce (`passate-redazionali.md`, 2ª passata) e al giudizio
del DM.

## Quattro correzioni al metro, non allo stile

Ognuna rendeva il voto più severo della norma, e ognuna vale per tutte le
condizioni, rimisurate dopo.

- `validate_prosa` leggeva la sola prima riga dei soli box senza etichetta: il
  59% delle parole di read-aloud del repo. Ora riusa `box_read_aloud`; i
  rilievi sul repo passano da 180 a 229.
- Le sigle delle caratteristiche (DES, COS, CAR) e ARC contavano come
  «maiuscole di enfasi»: tre handout su tre bocciati per aver riportato bene
  `state.md`.
- L'etichetta su una riga sua, sopra il box o in testa alla citazione, non
  contava: era la forma di tre bocciature su tre della tornata B, e la norma
  non dice su che riga stia.
- Le cartelle vuote delle corse fermate dal limite dell'API valevano zero.

## Le corse che non contano, e perché

- **A-senza-2** è in `scartate/`: aveva letto `voto_scrittura.py` per intero.
  Rifatta come A-senza-4, con il divieto esplicito su `scripts/`.
- **Tutte le corse senza skill ricevono `AGENTS.md`** all'avvio, con i tetti
  dei box e il «Che fate?». Il confronto è fra le skill e il loro riassunto, non
  fra le skill e il nulla.
- **Le corse con le skill hanno letto L11 nel piano** per scrivere S05 e S10,
  e lì c'erano già D13 e D14. A e B leggono lo stesso piano, quindi il
  confronto fra loro regge.
- **B-con-2** ha visto tre righe di altre corse in un risultato di grep, senza
  aprirle. Lo dichiara lei; il caso toccato (S09) passa in tutte e tre le corse.

## Cosa hanno trovato le corse, oltre al voto

Tre corse su tre della tornata B, indipendenti, segnalano le stesse due
incoerenze nel canone. Sono per il DM, non per le skill:

- DEF-5 §9 vuole il carry-over contro Fauci nell'handout «Lo Stato dei
  Custodi»; `ARC07-HANDOUTS.md` vieta di rivelarlo in un handout.
- DEF-5 §0-bis fa svanire all'alba le pozioni antiche; DEF-4 §6 (canone del
  2026-09-25) dice che torna tutto ciò che i PG portano. `ARC08-11-PONTE-ARRIVO.md`
  dà ancora a Thorik «−2 COS», contro «−4 DES / +2 COS / +4 CAR» di `state.md`.

## La tornata C (L12, 2026-10-02)

Tre agenti sui soli casi di verifica, con le skill come le ha lasciate L12:
l'indice in testa ai references, i casi veri di `italiano-nativo` §1-bis, la
domanda 8 della self-check. **Tutti e tre hanno eseguito `ciclo_prosa.py
segnala` sui loro testi prima di consegnarli**, senza che il prompt lo
nominasse; uno ha trovato un'antitesi con trattino, l'ha corretta e ha
rimisurato. È la prima prova che la domanda 8 arriva da sola.

98 su 99, contro il 100% della tornata B. La sola bocciatura è un falso
positivo del rilevatore dei calchi: «la **sua** voce nella tua testa», detto
della voce di Durik, cioè di un altro. È il confine che §1-bis scrive per il
possessivo (dice *di chi*), e il rilevatore non può vederlo. Contato a mano, C
vale quanto B.

Due correzioni al metro, tutte e due più severe della norma, rimisurate su
tutte le corse senza che A o B cambino di un voto:

- l'etichetta che va a capo («**Read-aloud (BG3 lead).** *Da leggere solo
  se…*») non contava, perché si guardava l'ultima riga sopra il box e non il
  paragrafo. Due bocciature su tre della tornata C;
- una tornata che gira su un insieme solo valeva zero sull'altro. Ora un
  insieme che la corsa non ha scritto vale «—».

Le corse segnalano di nuovo le tre incoerenze di canone della tornata B, e una
quarta: il Rubino ha tre descrizioni diverse («Cuore della Leggenda» in
`DEF-4` e `DEF-5`, altre due altrove). Sono per il DM.
