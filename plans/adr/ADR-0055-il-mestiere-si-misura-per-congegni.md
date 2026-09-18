# ADR-0055 — Il mestiere si misura per congegni dichiarati, non per copertura dei pilastri

- **Stato**: accettata (2026-09-18), **attuata** (`scripts/misura_craft.py`, 17 test)
- **Decisore**: DM — *«c'è un modo di misurare che il nuovo stile a 9 pilastri
  (e i vari stili) e le altre cose inserite sono presenti in quella parte
  citata, in che percentuale»*
- **Rapporti**: attua ADR-0036 (*misurare il miglioramento, non lo stato*) ·
  applica ADR-0053 (*un matcher largo traveste l'ignoranza*) · normativa per
  `plans/PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI.md`

---

## Contesto

Il repo ha uno **stile a nove pilastri** (Salvatore, Tolkien, Casa di Davide,
Mercer, GoT, BG3, BG1–2, PoE, Andor) e una serie di congegni introdotti nel
tempo — orologi, contingenze, vie non combattive, modi di fallimento. Il DM
chiede la cosa ragionevole: **sono arrivati nelle parti scritte prima?**

La richiesta nomina una «percentuale dei nove pilastri». Misurarla alla lettera
darebbe un numero **che premia il difetto**.

## Decisione

**Non si conta la copertura dei pilastri. Si contano i congegni che lasciano
una traccia scritta**, e si confronta ogni documento con due **banchi** scelti
dal DM: l'Abbazia della Rotta Sicura e il Palio di Channathgate.

L'unica percentuale che si pubblica è la **copertura dei congegni** (quanti su
17 sono presenti), sempre affiancata dalla colonna che conta davvero: il
**debito verso i banchi** — quali congegni i due documenti migliori hanno e
questo no.

### Perché non la copertura dei pilastri

🔴 La skill dello stile dichiara una *fusion rule*: **«never all nine at once.
Every scene has ONE lead pillar and at most two support»**. Un documento che
portasse tutti e nove i pilastri in ogni scena **violerebbe** lo standard. Una
«copertura 9/9» misurerebbe quanto un testo sbaglia, e un piano costruito su
quel numero spingerebbe a peggiorare i documenti migliori.

⚠️ E c'è un precedente **misurato** in questo repo:
`PIANO-PROSA-CHE-NON-SEMBRI-GENERATA` provò i rilevatori di tropi sul contenuto
di gioco e trovò **64 falsi positivi su 64**. Lo stile come *tessitura* non si
misura a macchina; fingere di sì produce numeri che sembrano informativi e non
lo sono.

### Cosa si misura al suo posto, e la cosa che risponde davvero alla domanda

I documenti che **applicano** la fusion rule la **scrivono**:
`(Casa di Davide lead)`, `(BG3 lead)`, `(Mercer support)`. Quella marca si
conta, ed è la risposta letterale alla domanda del DM — non «quanti pilastri
tocchi» ma «**dichiari quale guida**».

🔎 Misurata sul repo di oggi, la marca esiste in **quattro documenti soli**:
DEF-2, DEF-3, DEF-4, DEF-5. Non in DEF-1, non nell'Abbazia, non nel Palio, non
in nessun file di ARC-08 e ARC-09.

## Conseguenze

**Buone.**
- La domanda «lo stile è arrivato qui?» ha una risposta con un comando dietro.
- Il confronto è contro **documenti veri del repo**, non contro un ideale: se un
  banco non ha un congegno, quel congegno non diventa un debito per nessuno.

**Costi, dichiarati.**
- 🔴 **Ogni conteggio è un indizio, non un verdetto.** Un documento può fare una
  cosa bene senza la marca che lo script cerca, e portarne la marca senza farla
  bene. Il numero dice **dove guardare**; la lettura resta al DM.
- ⚠️ **Le virgolette dritte non sono sempre dialogo.** Il rilevatore delle
  battute chiede ≥3 parole e punteggiatura di frase, perché nel Palio `"…"`
  dà 128 hit e sono **titoli di canzoni**. Un documento che scrivesse i dialoghi
  con `"` corte verrebbe contato sotto: è un **limite scritto**, non nascosto.
- ⚠️ La soglia non esiste apposta: non c'è un «voto minimo». Un piano che un
  giorno volesse imporne uno dovrà scrivere **perché**, o diventa un tappeto.

## La prova che la decisione serviva: la prima tabella diceva il falso

La prima esecuzione ha prodotto numeri **che invertivano la verità**, e la sola
prova a sostegno era la tabella stessa. Cinque rilevatori su diciassette erano
sbagliati, e un sesto difetto non era in nessun rilevatore:

| Difetto | Cosa produceva | Correzione |
|---|---|---|
| `^>` per il read-aloud | DEF-1 segnava **183 read-aloud**: sono `> **Sistema: D&D 3.5 SRD**`. L'Abbazia ne segnava 11, tutti veri. **Il numero diceva il contrario del vero** | solo citazioni in corsivo → DEF-1 **24**, Abbazia **11 invariati** |
| grassetto sullo spotlight | il Palio nomina tutti e quattro i PG e non li scrive mai in grassetto → **0**. Misurava il markdown | tolto `**` |
| «eco» senza plurale | il Palio ha un **file intero** `PALIO-CONSEGUENZE-ECHI.md` e segnava **zero echi** | `\bech[io]\b` |
| `Nome: «…»` per le voci PNG | **zero in tutti e 12 i bersagli**: una forma inventata, che nessun documento usa | due convenzioni vere, con il filtro contro i titoli |
| `\bWant\b` per il grigio politico | non matcha **niente** in tutto il repo | rimossa |
| 🔴 **bersagli campionati** | misuravo **6 file del Palio su 15**, **1 di ARC-08 su 23**, **4 del Torneo su 22**. Gli zeri sembravano assenze di mestiere ed erano **assenze di misura** | glob, e un modello che non pesca niente **alza un errore** |

L'ultima riga è la stessa forma d'errore del censimento tarato sul campione, e
adesso non può più restare muta: `espandi()` fallisce rumorosamente.

## 🔴 Addendum (stesso giorno) — e anche la diagnosi era sbagliata

Il DM, letta la prima versione: *«ma sei sicuro? controlla davvero tutto…
parti da quello che è definito davvero per la parte di scrittura, stile e
linea editoriale, e che c'è davvero nel repo skills»*.

Aveva ragione, e l'errore era **lo stesso di cui questo ADR parla, commesso un
livello più in su**: avevo preso i congegni da due skill e non avevo aperto la
cartella `references/`, che in `rumblingstone-narrative-style` contiene **dieci
file**. Dentro ci sono standard di scrittura **numerici e normativi** che
nessuno misurava — e una delle mie conclusioni era falsa per quel motivo:

> ~~«voci PNG: pretendeva `Nome: «…»`, una forma inventata che nessun documento
> usa»~~ → `editorial-standards.md` §2 la **prescrive**
> (`**NOME (registro/tono):** *«battuta»*`). Non è inventata: **è dichiarata e
> quasi nessuno la segue** — sei occorrenze in tutto il repo.

**Perché il difetto è lo stesso.** Un rilevatore tarato sul campione dichiara
copertura che non ha; un *criterio* tarato su due skill su diciotto fa
esattamente lo stesso, e in più sembra completo. La regola che ne esce, e che
questo ADR aggiunge alla decisione:

> **Un congegno entra nel metro solo dopo aver letto la fonte che lo dichiara —
> il file, non il titolo del file.** Il terzo campo di `CONGEGNI` non è una
> citazione decorativa: è la prova che qualcuno è andato a leggere.

E il fatto misurato che ne è uscito, il più grave del lotto: **ADR-0014
(«regia sensoriale obbligatoria», luglio 2026) è stato applicato a un
documento solo**, `ARC07-DEF-1`, nel commit che lo ha introdotto. La
chiusura su «Che fate?» che prescrive per **ogni** box di combattimento
esiste **una volta in tutto il repo**. Il lint che avrebbe dovuto
presidiarlo conta le occorrenze della **parola** «read-aloud» e gira solo
sui 5 master DEF: **96 file su 100 non sono mai stati guardati**.

## 🔴 Addendum 2 — il terzo strato, e tre cifre pubblicate da correggere

Il 2026-09-18, **usando** lo strumento per riscrivere DEF-4, i numeri non si
muovevano mentre il testo cambiava. Il difetto era lo stesso di questo ADR, al
terzo giro: **un metro tarato su una forma sola**.

`editorial-standards.md` §2 **prescrive** `> **Read-aloud (X).** *prosa*`, e il
rilevatore contava solo i box che cominciano con corsivo **nudo** — saltando
**proprio quelli scritti a norma**. Con tre conseguenze:

1. **DEF-4 ha 15 read-aloud, non 5**; **DEF-5 ne ha 4, non zero**; e la frase
   «DEF-4 ha il divario più grave col Palio» era **invertita** — 15,7 contro
   13,4 ogni 1.000 righe.
2. `box_read_aloud()` aveva lo stesso buco: `--box` misurava DEF-4 su **2** box
   invece che 12.
3. `difetti_dei_box()` contava parentesi e nomi propri **dell'etichetta**, che
   è rivolta al DM e non si legge: ogni box a norma risultava **peggiore**.
   DEF-4 segnava 9 «con parentesi» e ne ha **2**.

🟢 **Reggono le due conclusioni più forti**, riverificate: Torre di Zalkatar e
Battaglia Finale sono davvero a **zero** read-aloud, in 12 e 16 file.

**La lezione che questo ADR incassa**: la regola dell'addendum 1 — *leggere la
fonte che dichiara il congegno* — non basta. Serve anche **usare lo strumento
su un caso vero**: tre difetti su tre sono emersi scrivendo, non leggendo.

## Alternative scartate

1. **Contare la copertura dei nove pilastri.** Scartata: contraddice la fusion
   rule, vedi sopra.
2. **Un punteggio unico di «qualità».** Scartata: somma congegni che non sono
   commensurabili (un orologio non vale un read-aloud) e nasconde proprio
   l'informazione utile, cioè *quale* congegno manca.
3. **Un cancello in CI che boccia sotto una soglia.** Scartata **per ora**: non
   esiste una soglia difendibile, e ADR-0036 dice di misurare il miglioramento.
   Il presidio è il piano, non il rosso.
