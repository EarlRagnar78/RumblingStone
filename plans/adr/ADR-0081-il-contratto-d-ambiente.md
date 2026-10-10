# ADR-0081 — Il contratto d'ambiente: una dichiarazione, un orchestratore, e si toglie solo ciò che si possiede

- **Stato**: **accettata** (il DM, il 2026-10-08, D1-D11 di [PIANO-AMBIENTE-RIPRODUCIBILE](../PIANO-AMBIENTE-RIPRODUCIBILE.md)); **non attuata**
- **Data**: 2026-10-08
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: estende il lotto D di [PIANO-QUALITA-DEL-CODICE](../PIANO-QUALITA-DEL-CODICE.md) (`binari.py`); rispetta [ADR-0002](ADR-0002-cli-unica-dm-orchestratore.md) (un solo ingresso) e [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) (il canone non si tocca); emenda [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) col lock (lotto A3); convive con PI-3 e PI-3b di [PIANO-PRATICHE-DI-INGEGNERIA](../PIANO-PRATICHE-DI-INGEGNERIA.md)

## Contesto

Alla domanda «la mia macchina è come la CI?» il repo risponde solo in parte.
`binari.py` dice **cosa** serve e cosa succede senza, ma non **quale versione**:
typst è fissato a 0.15.1 dentro `ci.yml`, mentre il registro consiglia di
scaricarlo da `releases/latest`. La CI scarica typst senza controllare il
checksum. Il DM lavora su Python 3.13 e la CI prova solo 3.11. Le dipendenze
pip sono tutte `>=`, quindi la CI installa l'ultima versione e il portatile
quella che aveva. `install-git-hooks.sh` scrive in `.git/hooks/` sopra quello
che trova, e sulla macchina del DM oggi non c'è nessun hook.

Il DM ha incollato un brief generico per un «bootstrapper deterministico». Il
metodo del brief è giusto: stati espliciti, prova funzionale, idempotenza,
rimozione che conosce i propri confini. La forma che propone (un eseguibile
nuovo, un `SETUP.md` nuovo, una fonte di versioni nuova) duplicherebbe tre
cose che il repo ha già.

## Decisione

0. **La CI è lo standard, e la macchina combacia.** Le versioni le definisce
   la CI; un aggiornamento entra prima in CI con una PR che lo prova, poi sulla
   macchina. Entra per una correzione di sicurezza o una funzione che vale il
   cambio, mai perché è uscito.
1. **Una dichiarazione sola: `scripts/binari.py`.** Prende la versione, la
   classe di parità, i profili e, per piattaforma, URL e checksum di ogni
   binario. La CI legge da lì, non dichiara versioni per conto suo. Le
   dipendenze Python si fissano con un lock con hash generato dai pavimenti di
   `requirements*.txt`, che restano la dichiarazione. Python è **uno solo, il
   3.13**, la versione di Debian stable; si sale quando sale Debian. Chromium è
   **Chrome for Testing** a una versione fissa, la stessa ovunque.
2. **Un orchestratore solo: `dm.py ambiente`**, stdlib-only, con `piano`,
   `setup`, `verifica`, `stato`, `aggiorna`, `rimuovi` e i profili `dm`,
   `sviluppo`, `completo`. `dm.py doctor` resta la vista breve.
3. **Tre piattaforme**: Debian stable, Ubuntu stable (24.04, poi 26.04 con una
   PR), Bazzite. Su Bazzite, che è immutabile, l'ambiente vive in un distrobox
   Debian 13 e il sistema ospite non si tocca. Ogni componente ha una classe di
   verifica nel registro (versione, configurazione, solo-locale); per tutto ciò
   che la CI usa, la classe è la versione esatta.
4. **Si toglie solo ciò che si possiede.** Lo stato dell'orchestratore vive
   fuori dal repo, in `$XDG_STATE_HOME/rumblingstone/<id-del-clone>/`, e
   registra per ogni risorsa se c'era prima. Possiede il `.venv`, i binari in
   `~/.local/bin` che ha installato, gli hook e il valore di `core.hooksPath`.
   I pacchetti di sistema si installano solo dopo una conferma (D1) e finiscono
   in un registro, perché `apt` non ha un *undo*: si confronta `dpkg-query`
   prima e dopo, e la rimozione toglie solo la differenza, dopo una simulazione
   mostrata, mai con `autoremove` né `purge`. Chiavi SSH e
   GPG, credenziali, configurazione git dell'utente e contenuto del repo non si
   toccano mai.
5. **Nessun PASS senza prova.** Una versione stampata dimostra solo che il
   programma parte: la verifica produce un file vero (una pagina typst, un
   libretto pdfcpu, un PDF di Chromium) in una cartella temporanea e lo
   cancella. Ciò che non si può stabilire è `UNKNOWN`, ed esce con 2.
6. **Il secondo giro non cambia niente, e la CI lo prova**: setup due volte,
   rimozione, `git status` pulito.

## Conseguenze

- Diventa possibile rispondere «sì, la tua macchina è come la CI», componente
  per componente, con un JSON che la CI stessa produce.
- Una versione cambia in un posto, e Dependabot continua a proporre gli
  aggiornamenti delle librerie, con il lock al posto dei `>=` installati.
- Si paga: un sottocomando di `dm.py` di dimensioni non piccole; i checksum da
  aggiornare a mano a ogni versione di typst, pdfcpu, shellcheck e Chrome for
  Testing; tre job CI in più (Debian in container, distrobox, ciclo
  setup-rimuovi); su Ubuntu un PPA (deadsnakes) per avere Python 3.13.
- Il passaggio da 3.11 a 3.13 è un emendamento ad ADR-0037: chi ha ancora 3.11
  resta fuori, ed è voluto.
- Si paga anche il lock: il comando d'installazione del DM cambia, e la forma
  dei file (`.in` accanto ai `.txt`, oppure un `.lock` a parte) dipende da come
  Dependabot riconosce `pip-compile`. Si misura nel lotto A3 prima di scegliere.
- Con D1 il setup può usare `sudo`. Il comando si mostra per intero prima della
  conferma, e nessun aggiornamento di sistema parte per installare un pacchetto.
- Resta `UNKNOWN` in CI l'host Bazzite: la CI prova il distrobox, non il
  sistema immutabile. La prova sull'host si fa a mano. Windows e le altre
  distribuzioni non sono supportate, e `setup` lo dice prima di toccare niente.
- Da rivedere quando la CI passa a Ubuntu 26.04 (avviso di GitHub per il 19
  ottobre 2026): il runner è un componente del contratto e cambia con una PR
  che lo prova. Ubuntu 26.04 ha Python 3.14 di sistema, quindi il PPA resta.
