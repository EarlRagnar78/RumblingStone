# ADR-0093 — La prosa è migliorata se il DM la sceglie alla cieca; i numeri dicono solo dove guardare

**Stato**: accettata (dal DM il 2026-10-19)
**Data**: 2026-10-18
**Decisione-fonte**: richiesta del DM del 2026-10-18 («cerchi metodi per migliorare la prosa in rete […] che possono essere misurati ed applicati nel repo […] con una verifica misurabile di miglioramento»), lotto 4 di [PIANO-AVVENTURE-COMMUNITY](../PIANO-AVVENTURE-COMMUNITY-2026-10.md)

## Contesto

Il DM vuole rifare i master DEF di ARC-07 e misurare se la prosa migliora. Il
repo misura già bene i **difetti**: nove strumenti, 47 norme misurate. Non
misura la **qualità**, e i due numeri che ci provano non si muovono più: il
punteggio MQM dei master DEF ha mediana 99,51, e il voto delle corse è al 100%.

Due giri di ricerca in rete (le note sono in
`plans/esperimenti/avventure-community/note-prosa-*.md`) dicono la stessa cosa
da due lati:

- nessun metodo deterministico misura la qualità della prosa. I giudici LLM
  non concordano con gli esperti umani (κ vicino a zero in TTCW, Chakrabarty
  2024, e in «Measuring AI Slop», 2025), e ottimizzare un indice di
  leggibilità peggiora il testo (Martinc 2023);
- nessuna fonte letta mostra che una passata di sole regole migliori la
  preferenza di un lettore umano.

Ci sono però forme che separano il testo generato da quello rivisto, con una
fonte che dice perché contano. Misurate sui box di oggi:

| Indicatore | Fonte | ARC-08 | DEF di ARC-07 |
|---|---|---|---|
| gerundio in coda | Reinhart e altri, PNAS 2025: i modelli istruiti usano le participiali da 2 a 5 volte più degli umani | 9 (1,7‰), 9 veri su 9 | 0 |
| avverbi in -mente | Browne e King; Blatt 2017, correlazione sotto le 50 ogni 10.000 parole | 30 (5,8‰) | da 0 a 1,2‰ |
| battute dei PNG oltre 25 parole | regola d'industria dei dialoghi di gioco (BioWare, citata dalla Neverwinter Vault) | 0 su 1 | 9 su 26 |

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Il cieco del DM decide, gli indicatori dicono dove guardare** (la scelta) | è l'unica misura della qualità che la letteratura sostiene; costa venti letture | serve il tempo del DM; venti coppie dicono «meglio», non «quanto meglio» |
| Un giudice LLM che sceglie fra le due versioni | automatico, ripetibile | κ vicino a zero con gli esperti; nel repo il κ con il DM non è mai stato misurato (`campioni_kappa.py`) |
| Gli indicatori nuovi diventano norme pesate nel MQM | il miglioramento si vede nel numero | Goodhart: il testo si riscrive per il numero. Il bersaglio non è lo zero (l'italiano usa il gerundio), e le soglie vengono da corpora inglesi |
| Un parser (Stanza) per gli stampi sintattici e le subordinate | chiuderebbe la norma dei due livelli di subordinate | una dipendenza nuova e pesante per un segnale non ancora tarato; resta un passo successivo |

## Decisione

**Una riscrittura della prosa di gioco è migliorata solo se il DM, alla cieca,
preferisce la versione nuova in almeno 14 coppie su 20.** Gli indicatori
deterministici non decidono: dicono dove guardare, e servono a controllare che
nessuna norma cresca.

1. **`scripts/cieco_versioni.py`** fa il confronto in tre passi. `campione`
   sceglie i box con un seme e ne congela il testo **prima** di riscrivere;
   `coppie` trova i box corrispondenti nella versione nuova e li mette in
   ordine casuale, con la chiave in un file a parte; `esito` scioglie la chiave
   e applica il criterio. Le coppie identiche non si votano, e il pari non
   vince.
2. **`misura_craft --stile`** conta tre indicatori senza peso: il gerundio in
   coda, gli avverbi in -mente e le battute dei PNG oltre 25 e oltre 40
   parole. Gerundi e avverbi si leggono contro la **fascia umana italiana**
   (dieci titoli del Gruppo Chimera: 1,0-3,1‰ e 3,8-13,4‰), sotto come sopra;
   la prima stesura usava un allarme a 5‰ da Blatt, che cadeva sulla mediana
   umana. Non entrano nel MQM e non sono un cancello.
3. **Il campione di ARC-07 è congelato ora**, in
   `plans/esperimenti/prosa-cieco/campione-ARC07-DEF.json`: venti box, quattro
   per DEF, seme 20261018, presi da `main` prima di ogni riscrittura.
4. **Dopo il primo voto, la misura decide e il cieco fa il resto** (il DM,
   2026-10-18 sera: «voglio la misura aggiornata, e quando non misura un reale
   miglioramento si usa la scelta alla cieca»). `coppie` applica a ogni coppia
   le due regole del voto (`read-aloud-adulti.md` §2-ter): meno dettagli
   sensoriali perde, un monologo spezzato in tre pezzi o più perde. Al DM
   vanno solo le coppie indecise, più quattro già decise come controllo;
   `esito` conta le decise come voti e, se il DM smentisce più di un
   controllo, dice che la misura è caduta e si rifà il cieco intero. Sulle
   sedici coppie del primo voto la misura ne decide 13 e ne sbaglia una (A1,
   dove la nuova ha più dettagli e il DM ha scelto la vecchia): è misurata sui
   dati da cui è nata, e i controlli servono a vedere se regge fuori.
   `ciclo_prosa misura` la usa come cancello: un box impoverito è un peggioramento.
5. **Due candidati scartati, con la misura.** Il pronome soggetto tonico (la
   norma pro-drop di `italiano-nativo.md` §1) dà 3 colpi in tutti i box, e
   sono tutti e tre cambi di soggetto legittimi: precisione 0 su 3. La
   spiegazione dopo il gesto («come a dire», «segno che») fa zero ovunque. La
   norma pro-drop entra nel registro come 🔴, con la ragione.

## Conseguenze

- Il rifacimento di ARC-07 ha un criterio scritto prima di cominciare, e un
  campione che non si può scegliere dopo.
- Il DM deve leggere venti coppie ad alta voce. Senza quella lettura il
  rifacimento può dire «nessuna norma è cresciuta», non «la prosa è migliorata».
- Il campione è preso prima della #245. La #245 cambia **uno** dei venti box
  (somiglianza 0,90); gli altri diciannove sono identici. Il campione resta
  valido anche dopo la sua fusione.
- I DEF di ARC-07 stanno **sotto** la fascia umana su gerundi e avverbi (0 e al
  più 1,2‰), ARC-08 ci sta dentro. Il ciclo di prosa li ha tolti più di quanto
  faccia uno scrittore italiano: può essere pulizia o appiattimento, e lo dice
  solo il cieco. Il rifacimento non deve rincorrere la fascia né allontanarsene.
- **Il primo voto, 2026-10-18**: sul rifacimento della #249 il DM sceglie la nuova in 8 coppie su 16 (quattro identiche), mentre MQM e soglie dei box migliorano tutti. Il criterio ha fatto quello per cui c'è: ha detto «non meglio» dove i numeri dicevano «meglio» ([ESITO](../esperimenti/prosa-cieco/ESITO-ARC07-2026-10-18.md)). Lo stesso giorno `esito` impara a togliere le coppie identiche e a riproporzionare la soglia (12 su 16), e `coppie` a ricomporre un box spezzato in battute.
- Il campione non distingue i box di luogo da quelli d'evento, perché i box non
  dichiarano il tipo (PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE, D3). Lo dice, e non lo
  simula.

**Da rivedere se**: i controlli smentiscono la misura in due giri di fila
(allora le due regole tornano ipotesi e decide di nuovo solo il cieco). E se: il κ fra un giudice automatico e il DM, misurato su almeno
venti coppie, supera 0,6. Allora il giudice può fare il primo giro e il DM
solo i casi dubbi. Oppure: il DM preferisce alla cieca la versione con meno
gerundi in coda e meno avverbi in almeno 14 coppie su 20, e allora i due
indicatori possono diventare norme minori.
