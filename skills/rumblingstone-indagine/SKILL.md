---
name: rumblingstone-indagine
description: >
  Come si costruisce e si gioca un CASO in RumblingStone: misteri, enigmi,
  indizi che sembrano slegati e che si ricompongono nel disegno finale, e il
  congegno arcano o aberrante che li spiega tutti insieme. Copre il nodo
  d'indizio a tre strati (Fatto/Lettura/Nome), le SEI PORTE che fanno entrare
  nell'indagine anche i PG senza un solo grado speso in abilità (prove grezze
  di FOR/DES/COS/INT/SAG/CAR), il registro delle ricompense (Acume, Perizia,
  Metodo — ADR-0022), la scena di ricomposizione e la gestione del vicolo
  cieco. Use WHENEVER si scrive, si prepara o si gioca un'indagine: "indagine",
  "caso", "mistero", "giallo", "enigma", "indizio", "indizi", "chi è stato",
  "omicidio", "sparizione", "investigazione", "deduzione", "ricomposizione",
  "vicolo cieco", "i giocatori non trovano niente", "il gruppo non ha un
  ladro", "prova grezza", "punti Acume", "Perizia", "congegno", "macchina
  arcana", "rituale da fermare", "cospirazione", "innesco in piena vista",
  "trappola scenografica", "cosa stanno costruendo i villain",
  "chi è l'assassino", "impostore", "non è chi dice di essere",
  "cospirazione", "sparizione", "è scomparso", "accusa falsa",
  "hanno incastrato il PG", "che tipo di mistero".
---

# RumblingStone — Il caso: indagine, enigmi, ricomposizione

Questa skill copre un tipo di sessione che il repo non sapeva scrivere: quella
in cui **il climax è cognitivo**. Non si vince perché si è colpito più forte,
si vince perché a un certo punto sei cose viste in tre serate diverse
diventano una sola cosa.

> **Il vincolo che ha dato forma a tutta la skill**: a questo tavolo i punti
> abilità sono andati sul danno. Un caso che si apre solo con Cercare e
> Sapienza esclude tre giocatori su quattro dal proprio gioco. La soluzione
> **non è abbassare le CD** — è cambiare l'unità di misura dell'indizio.
> Vedi §2 e `references/nodi-e-sei-porte.md`.

## Confini con le altre skill (ADR-0008 §1)

| Se la domanda è… | La skill è… |
|---|---|
| Come suona la prosa, quale pilastro guida la scena | `rumblingstone-narrative-style` (questa skill **è** il suo pilastro 9, la cui ancora letteraria è Umberto Eco, *Il nome della rosa* — vedi `references/documento-ed-errore-fecondo.md`) |
| Quanto fa una prova, cosa è «solo per addestrati», i massimali dei gradi | `dnd-35-srd` |
| Chi è il colpevole nella campagna, cosa sa già il gruppo | `rumblingstone-campaign` + `campaign/state.md` |
| Come si struttura la quest in tappe e fazioni | `rumblingstone-narrative-style/references/quest-design-baldur.md` |
| Quanto dura davvero un caso al tavolo | `rumblingstone-playtest` |
| **Se questo arco debba avere un caso, e di che famiglia** — la varietà fra un arco e l'altro | `rumblingstone-narrative-style/references/varieta-fra-archi.md` |

**Ordine di caricamento** per scrivere un caso: `campaign-coherence.md` +
`state.md` (cosa è vero) → questa skill (come si struttura) →
`rumblingstone-narrative-style` (come suona) → **`italiano-nativo.md` §9 e
`read-aloud-adulti.md` prima di consegnare qualsiasi testo giocatore.**

---

## 1. Le quattro regole non negoziabili

1. **Il Fatto non si tira mai.** Ogni indizio ha uno strato oggettivo che i
   PG ottengono per il solo fatto di essere lì e di guardare. Fallire una
   prova toglie l'*interpretazione*, mai il fatto. Un caso in cui un tiro
   fallito cancella un'informazione necessaria è un caso rotto — e nessuna
   quantità di improvvisazione del DM lo ripara al tavolo.
2. **Tre porte per nodo, di cui una fisica.** Ogni nodo d'indizio dichiara
   almeno tre delle sei caratteristiche come vie d'accesso, e **almeno una
   dev'essere FOR, DES o COS**. È la clausola che obbliga chi scrive a dare
   qualcosa da fare a chi ha costruito il PG per menare (§2).
3. **L'enigma non è un lucchetto.** Risolto dà un vantaggio; non risolto non
   ferma il caso, lo rende più caro. Un enigma che blocca è una trappola per
   il DM, non per i giocatori (`references/congegno-e-enigmi.md` §4).
4. **Il congegno è la stanza, non un premio.** Capire la macchina non dà
   bonus ai tiri: dà **azioni che prima non esistevano** e cambia le
   tattiche che funzionano. Trasformare la fatica dell'indagine in «+2 per
   colpire e conoscete i punti deboli» brucia in un round tutto il piacere
   della scoperta (`references/congegno-e-enigmi.md` §8).
5. **Si mostra una parte, mai il tutto.** L'effetto prima della causa, il
   pezzo fuori contesto, la misdirection *onesta* (si punta la luce su
   qualcosa di vero, solo non il più importante), e il congegno intero
   visto **una volta sola**. Un congegno rivelato tutto insieme è
   un'illustrazione (§4 dello stesso file).
6. **La ricomposizione la fa un giocatore, se ci arriva.** Il DM la prepara
   scritta come rete di sicurezza e la legge solo se il tavolo non ci
   arriva. È l'`[HDYWTDT]` di Mercer applicato alla deduzione: il colpo
   finale lo tira chi ha fatto il lavoro.

## 2. Le sei porte, in una tabella

Lo stesso nodo, sei modi di entrarci. **Questa è la tabella che risolve il
problema del tavolo**: il barbaro non «aiuta il ladro a cercare», legge la
stessa scena con lo strumento che ha.

| Porta | Cosa chiede al giocatore | Cosa restituisce |
|---|---|---|
| **FOR** | provare il peso, la resistenza, la forza che ci è voluta | *quanti* erano, o *quanto* era forte chi l'ha fatto |
| **DES** | rifare il gesto, ripercorrere il movimento | *come* è andata: l'angolo, il percorso, la mano usata |
| **COS** | il corpo che sa — quanto si resiste, quanto fa male, quanto freddo faceva | *quando*, e quanto è durata |
| **INT** | il collegamento, il conto che non torna | il *perché* — e il nome, quando c'è |
| **SAG** | l'agio che manca, la cosa fuori posto, la faccia che mente | *cosa* è sbagliato in questa scena |
| **CAR** | farlo dire a qualcuno — con le buone, con le cattive, con la faccia tosta | quello che nessun oggetto può dire |

Regola di scrittura: **una porta non è uno sconto, è un taglio diverso.**
FOR non dà la stessa informazione di INT con una CD più bassa: dà un pezzo
*differente* dello stesso nodo. Se due porte restituiscono la stessa frase,
una delle due è finta — riscrivila o toglila.

Meccanica: prova di caratteristica grezza = **d20 + modificatore, nessun
grado** (`dnd-35-srd/references/core-mechanics.md`). Le CD e il rapporto con
le prove d'abilità normali sono in `references/nodi-e-sei-porte.md` §3.

## 3. Domain → File

| Se stai facendo… | Leggi |
|---|---|
| **Scegliere che tipo di mistero è** — le sei famiglie (chi è stato · impostore · cospirazione · sparizione · accusa falsa · congegno), la firma degli indizi di ciascuna, la chiave tipica, l'errore da evitare, come finisce | `references/famiglie-di-caso.md` |
| Scrivere gli indizi: il nodo a tre strati, le sei porte per esteso con esempi giocati, le CD, la mappa dei nodi, **il vicolo cieco** | `references/nodi-e-sei-porte.md` |
| Premiare chi ha spremuto le meningi: **Acume, Perizia, Metodo**, i tetti, il registro da tenere (ADR-0022) | `references/registro-e-ricompense.md` |
| Scrivere **la scena in cui tutto si ricompone**, i falsi indizi progettati, il combattimento pre-letto | `references/ricomposizione.md` |
| **Scrivere il documento** che porta l'indizio (e le assenze che sono la prova), il **regolamento** della comunità chiusa come motore politico, **l'errore fecondo** quando il tavolo deduce male, il dettaglio d'epoca che *è* il meccanismo | `references/documento-ed-errore-fecondo.md` |
| Il disegno finale: le schegge, la chiave di lettura, **il congegno arcano/aberrante/mistico**, la **regia del prestigiatore**, **l'innesco in piena vista**, il congegno nell'**agenda dei villain**, il congegno come **terzo attore** in combattimento, il **dosaggio** | `references/congegno-e-enigmi.md` |

## 4. Lo scheletro di un caso (una pagina)

**Prima si sceglie la famiglia** (`references/famiglie-di-caso.md`): chi è
stato · l'impostore · la cospirazione · la sparizione · l'accusa falsa · il
congegno. È la decisione che determina la firma degli indizi. Il congegno è
**una** famiglia su sei, ed è la più costosa in stupore: una per arco.

```
IL SEGRETO       la verità intera, che il DM sa dal primo minuto — e i PG no.
                 (colpevole · vera identità · chi è alleato di chi ·
                  dov'è finito · chi ha costruito le prove · la macchina)
LA CHIAVE        l'informazione che ricodifica tutto in una volta.
                 Arriva a ~2/3 del caso: quello è il picco.
LE SCHEGGE       6-9 nodi. Ognuno ha una spiegazione INNOCENTE
                 plausibile nel momento in cui lo si trova.
CHI CI GUADAGNA  chi vuole che la verità non si sappia, e cosa fa nel
                 frattempo — agisce, non aspetta i PG.
L'INNESCO        il dettaglio dato gratis, in piena vista, in una scena
                 che parla d'altro — e che se nessuno lo tocca SCATTA.
                 (obbligatorio solo nella famiglia «congegno»)
IL COSTO         cosa succede mentre i PG capiscono. Il tempo è un
                 avversario, non uno sfondo.
LA PORTA CHIUSA  la cosa che non capiranno mai del tutto.
                 Un caso senza residuo non ha mai fatto paura.
```

Numeri di partenza (da tarare al primo collaudo, Lotto I5): **6-9 nodi per
caso**, di cui almeno 3 raggiungibili senza alcun grado d'abilità; **2-3
sessioni**; **1 sola chiave di lettura** — due chiavi sono due casi.

### La tabella delle dicerie: due sono false, e si sa quali

Il modo più economico che esista di seminare schegge. Una tabella `1d8` all'osteria
in cui **due voci sono deliberatamente false** — e il DM sa quali — costa quattro
righe e fa insieme:

1. dà al tavolo materiale da verificare invece che da credere: una diceria falsa
   **si smonta**, ed è una scena;
2. rende il fallimento informativo — chi insegue la voce sbagliata non ha perso il
   turno, ha eliminato una possibilità;
3. protegge dal difetto opposto, il tavolo che prende ogni parola di un PNG come
   canone perché finora lo era sempre stata.

**La regola**: le false sono false **per un motivo** — qualcuno ci guadagna, o
qualcuno ha capito male in buona fede. Una diceria falsa a caso è rumore; una
diceria falsa con un padre è un nodo.

⚠️ **Va scritto quali sono**, nel testo del DM, accanto alla tabella. Una tabella
di dicerie senza la riga «la 3 e la 7 sono false» costringe il DM a decidere al
volo, e al volo si decide diversamente ogni sera.

Stessa logica per la **tabella di reazione** di un capo-fazione (`1d20` +
modificatori, dove i modificatori sono *le cose che i PG hanno fatto*): rende la
trattativa un esito, non una sentenza del DM.
Esemplare: `10-stand-alone/L'abbazia Della Rotta Sicura/` — *«Dicerie all'osteria
(1d8 — due sono false, deliberatamente)»* e la reazione di Malaluna.

## 5. Autocontrollo prima di consegnare un caso

Oltre a quello di `narrative-style` (§Self-check) e alla coerenza:

0. **Prova della famiglia**: so quale delle sei famiglie è questo caso, e
   il congegno c'è solo se serve? (Se ogni caso che scrivi ha una macchina,
   stai bruciando l'unica famiglia che non si può ripetere.)
1. **Prova del guerriero**: prendi il PG con meno gradi in abilità del
   gruppo. Ripercorri il caso solo con lui. Trova almeno tre nodi? Se no, il
   caso non è pronto — non è «difficile», è chiuso.
2. **Prova del Fatto**: c'è un solo nodo dove un tiro fallito toglie
   un'informazione necessaria? Riscrivilo a tre strati.
3. **Prova della scheggia**: ogni indizio ha una spiegazione innocente al
   momento in cui lo si trova? Se un indizio urla «sono un indizio», la
   ricomposizione finale non sorprenderà nessuno.
4. **Prova della chiave**: la ricomposizione usa **solo** cose che i
   giocatori hanno già visto? Un solo elemento nuovo e la scena diventa il
   DM che si spiega da solo.
5. **Prova del registro**: so chi ha depositato quale perizia, e dove l'ho
   scritto? (`references/registro-e-ricompense.md` §4.)
6. **Prova del power-up**: la ricompensa per aver capito la macchina è un
   bonus numerico? Se sì, riscrivila come **azione nuova** o come **stanza
   che cambia**.
7. **Prova del prestigiatore**: il tavolo, ripensandoci, può dire «quel
   pezzo l'avevamo visto»? (Se invece può dire «ce l'aveva detto il DM»,
   hai mostrato troppo e troppo presto.)
8. **Prova del dosaggio**: quanti congegni e quanti inneschi ci sono in
   questo arco? (Più di uno intero, o più di due inneschi → togli.)
9. **Prova del residuo**: cosa resta di non spiegato? Se niente, aggiungi
   qualcosa — e non spiegarlo nemmeno alla sessione dopo.
