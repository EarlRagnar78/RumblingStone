# L11 · Il giro sulle skill di scrittura: i risultati

> **2026-10-23.** Il lotto 7e di PIANO-AVVENTURE-COMMUNITY voleva togliere il
> banco, perché i suoi controlli sono già dentro `punteggio_mqm.py` e la
> condizione B-con era al 100% (soffitto). Resta, perché `banco_prosa_locale.py`
> (ADR-0089) gli fa votare le corse del modello locale. Il rilevatore di
> «sembra»/«pare» ora vive in `validate_prosa.py` e il banco lo riusa.

Il voto è `voto_scrittura.py`: ogni controllo chiama un rilevatore che
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

## Il voto non regala più i box (ADR-0089, I1, 2026-10-10)

Un testo di due righe senza box, con «sembra», una parentesi e una metratura,
prendeva 81% in taratura e 78% in verifica: i sei controlli sui box passavano
quando il box non c'era. Ora falliscono, e lo stesso testo prende 44% e 42%.
Nessuna corsa di questa pagina cambia di un voto, perché in tutte il box c'era
dove il caso lo chiedeva. Restano superati per intero, anche dalla spazzatura,
i quattro casi che non hanno un controllo di presenza (S04, S05, S08, S10): per
confrontare due generatori si leggono i casi di box e di dialogo.

Le corse di un modello locale si scrivono con `scripts/banco_prosa_locale.py`
in `corse/L-<modello>-<n>/` e si votano qui come le altre.

## La prima corsa locale: `gemma4:e4b-it-qat` sull'ASUS (2026-10-10), scartata

Il DM l'ha fatta girare sul portatile con Bazzite (RTX 4050, 6 GB), con
`scripts/llm-locale/prova.sh` e il contesto pieno. Il voto è stato 40% in
taratura e 60% in verifica. **Quei numeri non misurano il modello**, e la corsa
è in [`scartate/`](scartate/README.md).

Qui avevo scritto che il server non tagliava nessun prompt. Era falso: lo
avevo letto in una riga del log, che riguardava il primo caso e basta. I
`prompt_tokens` di `corsa.json` dicono altro:

| caso | caratteri del prompt | token contati dal server | caratteri per token |
|---|---:|---:|---:|
| S01, S06, S08 | 75.000-79.000 | 21.900-23.300 | 3,4 |
| S02, S03, S04, S07 | ~86.600 | **12.291** ciascuno | 7,0 |
| S09 | 82.256 | 24.231 | 3,4 |

I quattro prompt più lunghi superavano i 24.576 token di contesto, e llama.cpp
dentro Ollama li ha tagliati a metà senza dare errore. S09 è entrato, ma ha
lasciato 345 token alla risposta, che è uscita vuota. S07 si è fermato al
tetto di 1.500 token a metà di una parola. Restano validi cinque casi su dieci.

Su quei cinque si vede comunque qualcosa. In S01 e S06 il modello scrive il
read-aloud etichettato, ma in paragrafi normali e non nella citazione in
corsivo (`> *…*`) che la norma prescrive. Rimesso nella forma giusta a mano,
ogni box cade ancora su due o tre norme di sostanza: più di un nome proprio,
«sembra», una decisione presa per i giocatori. In S02, che però è uno dei
casi tagliati, il modello scrive l'esito delle azioni di tutti e cinque i PG.

Dopo questa corsa, `banco_prosa_locale` controlla tre cose:

- **prima di chiamare** il server, se il prompt stimato più la risposta supera
  il contesto: in quel caso non parte (codice 4);
- **dopo ogni caso**, se il server ha contato meno di un token ogni cinque
  caratteri (il prompt è stato tagliato), se la risposta è vuota o si è fermata
  al tetto;
- se un caso è guasto, la corsa va in `prove-locali/`, fuori dal voto
  (codice 5).

Il contesto predefinito passa a 32.768 token e il tetto di risposta a 3.000.
I tempi invece si possono già usare: da 13 a 50 secondi a caso, circa 32
token al secondo, 40 strati su 43 nella GPU.

## La corsa valida: `gemma4:e4b-it-qat` sull'ASUS (2026-10-11)

La stessa prova, rifatta con 32.768 token di contesto e 3.000 di risposta.
Nessun caso guasto: ogni prompt è arrivato intero (da 21.931 a 25.889 token per
i casi di gioco) e ogni risposta si è chiusa da sola. Da 20 a 84 secondi a
caso, 533 secondi in tutto.

| condizione | taratura | verifica |
|---|---:|---:|
| B-con | 96/96 (100%) | 99/99 (100%) |
| A-senza | 86/96 (89%) | 81/99 (81%) |
| spazzatura (I1) | 44% | 42% |
| **L-gemma4e4bitqat-1** | **13/32 (40%)** | **14/33 (42%)** |

Il voto è al livello della spazzatura, e quasi tutto per una ragione sola.
In quattro casi su sei di gioco (S01, S02, S06, S07) il modello scrive il
read-aloud, spesso etichettato e in S02 e S07 chiuso su «Che fate?», ma in
paragrafi normali. La citazione in corsivo (`> *…*`) che la norma prescrive non
c'è, e senza il box cadono gli otto controlli che lo riguardano.

**Una prova diagnostica**, che non è la misura: rimettendo quei paragrafi nella
forma del box con uno script, senza toccare una parola, il voto sale a 30/32 in
taratura e 30/33 in verifica (94% e 91%). Restano due forme di dialogo, un
trattino e un `hdywtdt`. Quindi la forma delle norme si può recuperare dopo, con
un passo meccanico. Il resto il banco non lo vede, e si legge nei testi:

- in S02 il modello scrive azioni ed esiti dei cinque PG («Il tuo martello…
  incontra la prima scaglia»), cioè decide per i giocatori;
- nessun caso di combattimento porta le meccaniche che B-con mette accanto al
  box (la CD della Presenza Terrificante, chi non tira e perché, le righe per
  esito).

La soglia di ADR-0089 per «rispetta le norme» è il 90% in verifica: con il 42%
non la passa.

**Il foglio alla cieca** (DM, 2026-10-11): B-con preferita in 10 coppie su 10,
nessun pari. Quota della sfidante 0/10, Wilson al 95% [0,00, 0,28]. La soglia
per «il DM la usa come bozza» era 3 su 10 fra preferite e pari: anche qui no,
e senza un caso al limite.
