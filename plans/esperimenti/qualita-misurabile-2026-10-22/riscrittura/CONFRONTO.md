# Catena vecchia, catena nuova e fusione sui box di ARC-07 e ARC-08

> **Aprire solo dopo aver votato** `cieco/SCHEDA-CIECA.md`. Qui si dice quale
> versione è V, quale N e quale F.

Prova del 2026-10-22, thread q4s7mw (PR #264). Ogni numero viene da uno
strumento del repo chiamato da `esegui.py`; gli script di `scripts/` non sono
stati toccati, e la catena N è simulata filtrando i loro rilievi. Le misure non
prevedono il voto del DM (calibrazione sulle 38 coppie già votate: nessuna sotto
la soglia, `../CALIBRAZIONE.txt`). Dicono dove le versioni differiscono, non
quale è migliore: quello lo dice il cieco.

## 1. Che cosa si è fatto

| Passo | Dove | Come si rifà |
|---|---|---|
| Base: 229 box e 68 scene misurati con le due catene, con i tempi | `base/BASE.txt`, `base/BASE.json` | `python3 esegui.py base` |
| Campione: 16 box (8 ARC-07, 8 ARC-08), seme 20261022, senza i 25 congelati | `campione/CAMPIONE.json` | `python3 esegui.py campione` |
| Criterio della fusione, scritto alle 06:22 prima di misurare V e N | `CRITERIO-FUSIONE.txt` | |
| Riscritture a mano, con tutte le iterazioni e il perché di ogni modifica | `versioni/BOX.md` | `python3 esegui.py misura` |
| Sei scene con le sole aggiunte di D18-D19 | `scene/S1.md` … `S6.md` | |
| Misura incrociata di O, V, N, F con tutte le misure | `misure/INCROCIATA.json`, `misure/RIASSUNTO.txt` | `python3 esegui.py incrociata` |
| Scheda cieca (V contro N; F contro O) e chiavi a parte | `cieco/SCHEDA-CIECA.md`, `chiave/` | `python3 esegui.py cieco` |
| Pagina di confronto | `CONFRONTO.html` | `python3 esegui.py pagina` |

Le due catene:

- **V** usa la skill `rumblingstone-narrative-style` (con `italiano-nativo.md` e
  `read-aloud-adulti.md`) e `rumblingstone-module-standard`, più `ciclo_prosa`
  (segnala, box_impoveriti, confronta_fatti), `validate_prosa`, `punteggio_mqm`,
  `misura_craft --stile` e `--costrutto-italiano`, `voto_scrittura`,
  `domande_developer` D1-D17.
- **N** è V senza ciò che l'inventario toglie o declassa (soglia dei nomi
  distinti, possessivo sulle parti del corpo, watchlist dei tic, `--costrutto-italiano`;
  P1 resta come indicatore), più `misura_sintassi`, `domande_developer` D18-D21
  (D20 come indicatore), `coerenza_campagna fatti` e le etichette LAMP/TTCW di
  `cieco_versioni.ETICHETTE` usate come checklist.

Chi riscrive è lo stesso agente per i due arm. Ogni arm tocca solo ciò che le
sue misure segnalano; N in più applica la checklist delle etichette, e ogni
modifica fatta per un'etichetta è scritta nel commento della versione.

## 2. I numeri principali

**Base (229 box, 68 scene).**

| | V | N |
|---|---:|---:|
| rilievi sui box | 229 | 68 |
| di cui solo di quella catena | 191 | 30 |
| box puliti | 74 | 176 |
| ARC-07 (124 box): rilievi | 76 | 14 |
| ARC-08 (105 box): rilievi | 153 | 54 |
| rilievi sulle scene | 20 | 40 |
| tempo, tre corse | 2,35-2,57 s | 6,79-7,85 s, + 1,5-1,6 s per caricare spaCy |
| righe degli strumenti | 5.582 | 6.980 |

Il 56% dei rilievi di V sui box viene da `--costrutto-italiano` (129) e un altro
23% dal tetto dei nomi distinti (53). Senza queste due norme V scende a 47
rilievi, contro i 68 di N. Metà del tempo di N è `coerenza_campagna` (3,5-4,4 s).

**Campione (16 box): somme, o medie dove è scritto.**

| misura | O | V | N | F |
|---|---:|---:|---:|---:|
| rilievi della catena V | 25 | 6 | 17 | 6 |
| rilievi della catena N | 18 | 9 | 0 | 0 |
| unione delle due | 35 | 15 | 17 | 6 |
| penalità MQM | 11 | 6 | 7 | 6 |
| dettagli sensoriali | 71 | 71 | 71 | 71 |
| parole | 1.207 | 1.222 | 1.175 | 1.208 |
| Gulpease (media) | 62,17 | 62,85 | 63,20 | 63,46 |
| livelli di subordinate, max (media) | 1,63 | 1,56 | 1,13 | 1,25 |
| avverbi in -mente | 6 | 6 | 2 | 4 |
| box cambiati rispetto all'originale | | 11 | 11 | 14 |

Ogni catena pulisce le proprie misure e lascia quelle dell'altra: V resta con 6
soggetti preverbali, 1 aggettivo complesso, 1 frase oltre due livelli e 1
stare + gerundio che non vede; N resta con 10 box «senza c'è», 6 «più nomi
propri» e 1 possessivo. Nessuna riscrittura toglie dettagli sensoriali.
F vince sull'unione per costruzione: il criterio somma anche le norme che N ha
tolto (vedi §5).

La fusione, box per box (regole di `CRITERIO-FUSIONE.txt`): **F = V** in 7 box
(B04, B05, B06, B09, B12, B13, B14), **F = N** in 6 (B07, B08, B10, B11, B15,
B16; in B07 e B15 V e N sono l'originale), **fusione vera** in 3 (B01, B02,
B03: il testo di N col «c'è» di V). In tutti e sette i casi «F = V» V vince
solo nella famiglia «solo V»: sulle norme che restano anche in N i due arm
sono pari.

## 3. Strumento per strumento, norma per norma

«Veri» è la mia lettura di ogni rilievo del campione, con la norma della skill
in mano. Le raccomandazioni sulla qualità della prosa restano sospese al cieco;
quelle sul funzionamento degli strumenti si reggono sul dato.

| Strumento · norma | Catena | Base V / N | Campione: cosa ha portato | Raccomandazione |
|---|---|---:|---|---|
| `misura_craft --costrutto-italiano` | V | 129 / 0 | 10 box su 16 segnalati; V ha aggiunto 8 «c'è/ci sono» e 2 dislocazioni. Il controllo passa per sbaglio su B10: «, gli animali» è letto come dislocazione | **TOGLIERE**. Segnala il 56% dei box e la riscrittura che chiede è una formula; se il «c'è» piaccia lo dirà il cieco (coppie V-N di B01-B06, B09, B12-B14) |
| MQM `box_piu_di_un_nome_proprio` (nomi distinti) | V | 53 / 0 | 6 box. In 6 su 6 l'unico modo di stare sotto era togliere un nome, e `confronta_fatti` ha bocciato tutte e sei le V1 («Forgia», «Moradin», «Bracieri», «Thorek», «Dana» ×2, «Hammerfist», «Mano Rossa»); le V2 rimettono i nomi e il rilievo resta. Nessuno dei sei era un nome **nuovo** per il tavolo | **TOGLIERE come norma di riscrittura** (DECLASSARE a indicatore): contraddice l'invarianza dei fatti 6 volte su 6, ⚖️ specifiche del DM |
| `validate_prosa` possessivo sul corpo | V | 8 / 0 | 1 caso (B13, «le loro mani»: dice di chi sono le mani, dopo due soggetti) | **TOGLIERE**: 1 rilievo, e la calibrazione va nel verso opposto (11 a 3) |
| `ciclo_prosa` watchlist dei tic | V | 0 / 0 | nessuno | **TOGLIERE** (zero anche nella base) |
| `misura_craft` P1 | V; in N indicatore | 1 / 0 | 0 rilievi; ma «potete vedere» in B10 e B12 non lo prende (la forma con il modale non è nell'elenco). In N l'ha tolto la checklist («inglese») | **DECLASSARE**, come dice l'inventario; il buco del modale è da segnare nel registro |
| `voto_scrittura` (controlli dei box) | V | 98 doppioni, 0 propri | ogni suo controllo è già di MQM o di `segnala`; `box_un_nome` conta anche i PG (65 contro 53) | **TOGLIERE** il passaggio nella catena (FONDERE, come dice l'inventario) |
| `validate_prosa` calchi | entrambe | 16 doppioni di `segnala` | stessa regex, stesse righe | **FONDERE** in una superficie |
| stare + gerundio (regex di `validate_prosa`) | entrambe | 7 / 10 | 4 casi, 4 veri. La regex ne vede 3: in B03 «sta / incidendo» va a capo e la regex riga per riga lo perde; spaCy lo trova | **FONDERE** regex e `misura_sintassi.stare_gerundio` (o la regex sul testo del box unito) |
| `misura_sintassi` soggetto preverbale | N | 0 / 18 | 6 rilievi, 5 veri (B10 ×2, B11 ×2, B16). Il sesto (B01) è un errore del parser: N l'ha inseguito spostando un complemento | **TENERE** come norma di riscrittura, con la precisione dichiarata |
| `misura_sintassi` aggettivo complesso | N | 0 / 2 | 1 rilievo, falso («lontanissimo» preso per aggettivo di «cubo», B02): è lo stesso errore già letto nel README di `sintassi/` | **DECLASSARE** a indicatore: 0 veri su 2 nella base |
| `misura_sintassi` oltre due livelli | N | 0 / 7 | 2 box (B08, B09) riscritti; la media dei livelli massimi scende da 1,63 a 1,13 in N | **TENERE come indicatore, non come obiettivo**: la calibrazione dice che il DM sceglie la versione con più livelli 11 volte su 12 (p 0,006). N va nel verso che il DM finora non ha premiato |
| `misura_craft --stile` gerundio in coda | entrambe | 10 / 10 | 4 casi, 4 veri, corretti in tutti e due gli arm | **TENERE** |
| maiuscole, parentesi, «sembra», tic in gruppo | entrambe | 8, 7, 2, 4 | 1 caso (maiuscole, B12), corretto in tutti e due | **TENERE** |
| `ciclo_prosa.box_impoveriti` | entrambe | | 1 rilievo, falso: in B14 V1 togliere «Mano Rossa» toglie «Rossa», che il lessico sensoriale conta come colore | **TENERE**, togliendo dal lessico sensoriale le parole dei nomi propri |
| `ciclo_prosa.confronta_fatti` | entrambe | | ha fermato 6 riscritture su 6 che toglievano un nome | **TENERE**: è la sola garanzia che ha lavorato |
| `coerenza_campagna fatti` | N | ARC-07 0 su 90 attributi, ARC-08 1 su 276 | con i box sostituiti il conto non cambia in nessun arm (0 e 1) | **TENERE sull'arco**, fuori dal ciclo dei box: i box non portano gli attributi che legge, e costa metà del tempo di N |
| `punteggio_mqm` | entrambe | | penalità 11 → V 6, N 7, F 6: muove con le stesse norme degli altri | **TENERE** come non-regressione (ADR-0059), non come prova di miglioramento |
| etichette LAMP/TTCW come checklist | N | non misurabili | 10 interventi in 7 box: spiega 4 (B09, B10, B14, B16), goffo 3 (B03, B10 «puntellano», B13), inglese 2 (B10, B12), ricercata 1 (B13). N chiude con 32 parole e 4 avverbi in -mente meno dell'originale | **TENERE come checklist**; l'effetto si vede solo nel cieco, coppie B03, B09, B10, B12, B13, B14, B16 |
| `domande_developer` D18 | N | 0 / 17 | 5 scene: una riga **Domanda:** ciascuna, D18 da 1 a 0 | **TENERE** |
| `domande_developer` D19 | N | 0 / 3 | 3 blocchi di scelta: una riga di conseguenza ciascuno, D19 da 1 a 0 | **TENERE** come indicatore (inventario: 2½ veri su 5) |
| `domande_developer` D20 | N, indicatore | 0 / 1 | il solo rilievo è falso: «Ultimi Campioni» preso dal titolo come nome del boss (ARC08-01, 4D) | **DECLASSARE**, come dice l'inventario |
| `domande_developer` D21 | N | 0 / 0 | nessun master marca la rete degli indizi | **TENERE** (aspetta la marcatura) |

## 4. Le scene

| | Scena | Aggiunta | Prima → dopo |
|---|---|---|---|
| S1 | ARC07-DEF-1, Scena 3 (gli Xorn) | **Domanda:** il gruppo attraversa la foresta col suo mithral e col pilastro ancora in piedi? | D18 1 → 0 |
| S2 | ARC07-DEF-1, Scena 5 (il Seme) | «Se Tordek lo tocca» → una riga nuova nella tabella echi | D19 1 → 0 |
| S3 | ARC07-DEF-4, Scena 4 (il consiglio) | «Se Thorik gliela porge» → al consiglio Thorgrim è fra quelli che si fidano | D19 1 → 0 |
| S4 | ARC07-DEF-4, Scena 8 (Zog'tar) | **Domanda:** Zog'tar cade prima che i rinforzi facciano quadrato attorno alla tenda? | D18 1 → 0 |
| S5 | ARC07-DEF-5, Scena 3 (la pulizia) | **Domanda:** il re resta vivo quando i cinque hobgoblin passano l'anello? | D18 1 → 0 |
| S6 | ARC08-01, Incontro 1C | una domanda e una conseguenza (i bonus valgono nell'Incontro 2A) | D18 1 → 0, D19 1 → 0 |

Da una a tre righe per scena; nient'altro cambia. Ogni aggiunta porta
`[INFERRED — needs DM confirmation]`: la domanda e il punto in cui si vede la
conseguenza li ho dedotti dal testo, e il canone è del DM. Il rilievo D1 di S4
e S5 c'è prima e dopo, e non riguarda le aggiunte.

## 5. Che cosa non dicono questi numeri

- **Il criterio di fusione premia V per come è scritto.** Somma le tre famiglie,
  e la famiglia «solo V» contiene le norme che N ha tolto apposta. Così F = V in
  7 box anche dove V e N sono pari su tutto il resto. Se il cieco dà ragione a
  N nelle coppie V-N, il criterio va riscritto senza quella famiglia; se dà
  ragione a V, le norme tolte vanno riaperte.
- **Le misure di N sono state pulite anche quando sbagliavano** (B01, B02):
  la regola era «finché le misure sono pulite», e due modifiche servono solo al
  parser.
- **Le etichette LAMP non hanno una misura**: i 10 interventi fatti con la
  checklist sono la parte di N che i numeri non vedono, e anche quella che
  cambia di più il testo (B14 perde una frase, B16 la chiusa).
- **Un solo scrittore** per i due arm: il confronto misura le catene attraverso
  le mie scelte.
- **Pochi box di ARC-07 avevano rilievi**: i DEF sono già passati da più giri,
  e il massimo per box era 2 in V e 1 in N. ARC-08 ha dato il campione più
  vario.

## 6. Il voto

`cieco/SCHEDA-CIECA.md` ha due parti: **14 coppie V contro N** (B07 e B15 hanno
le due versioni identiche e non si votano) e **3 coppie F contro originale**
(B01-B03, dove F è un testo nuovo). Si vota una riga per coppia, con le
etichette se si vuole: `7 B goffo spiega`. Le chiavi sono in `chiave/` (in
CHIAVE-V-N la versione «nuova» è N; in CHIAVE-F-O è F). L'esito:

    python3 scripts/cieco_versioni.py esito --chiave plans/esperimenti/qualita-misurabile-2026-10-22/riscrittura/chiave/CHIAVE-V-N.json --voti VOTI-1.txt
    python3 scripts/cieco_versioni.py esito --chiave plans/esperimenti/qualita-misurabile-2026-10-22/riscrittura/chiave/CHIAVE-F-O.json --voti VOTI-2.txt

Nessuna coppia è decisa dalla misura: i dettagli sensoriali sono pari in tutte,
e `CONTROLLI` è stato alzato perché tutte vadano al DM. Se `esito` scrive
«misura smentita» vuol dire solo questo: qui la misura non ha deciso niente.

Che cosa rendere obsoleto lo dice il voto: se N vince le coppie V-N, si tolgono
dalla catena `--costrutto-italiano`, il tetto dei nomi distinti, il possessivo e
`voto_scrittura`, e la fusione si rifà senza la famiglia «solo V». Le correzioni
agli strumenti della §3 (stare + gerundio a capo, «Rossa» nel lessico, P1 col
modale, D20 sui titoli) valgono comunque, perché sono errori di misura e non di
gusto.
