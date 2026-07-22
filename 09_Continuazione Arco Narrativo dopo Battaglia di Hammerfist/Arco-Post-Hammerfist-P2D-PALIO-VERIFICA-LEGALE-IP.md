# P2D — Verifica legale/IP dell'arco "Palio di Channathgate" (ARC-09)

> **Data verifica**: 2026-07-18. **Ambito**: tutti i file dell'arco P2D (testi, booklet
> Homebrewery, handout, mappe SVG/PNG, stemmi SVG in `P2D-Palio-Allegati/stemmi/`),
> confrontati con il **Regolamento del Palio di Siena** (regolamento comunale) e con lo
> **Statuto/politiche del Consorzio per la Tutela del Palio di Siena** (CTPS).
>
> ⚠️ **Nota**: questa è un'analisi documentale di conformità, non un parere legale
> professionale. Per un uso commerciale reale serve un avvocato IP e/o un contatto
> formale con il CTPS (che rilascia autorizzazioni onerose o "nulla osta").

---

## 1. Verdetto sintetico

| Scenario d'uso | Esito | Motivazione |
|---|---|---|
| **Uso privato al tavolo** (DM + gruppo) | ✅ **OK** | Nessuna riproduzione/esposizione *al pubblico* rilevante ex art. 9 Reg.; nessun fine di lucro. |
| **Pubblicazione gratuita su GitHub** (stato attuale) | ⚠️ **Rischio basso ma non nullo** | Opera trasformativa fantasy, non commerciale, con note IP esplicite; restano però gli elementi evocativi cumulativi del §3 (in particolare titoli araldici ufficiali + livree identiche + motti parafrasati). |
| **Uso commerciale (vendita del modulo, merchandising, loghi su prodotti)** | ❌ **NON conforme "senza problemi"** | Vedi §3–§5: l'insieme nome + titolo ufficiale + colori identici + motto parafrasato identifica in modo inequivocabile le Contrade reali, i cui simboli, denominazioni e colori sono **marchi registrati** gestiti dal CTPS; la produzione di beni con riferimenti alle Contrade/Palio richiede **espressa autorizzazione contrattuale** del Consorzio. In più c'è un **blocco indipendente e assorbente**: l'IP Wizards of the Coast (§6). |

**Conclusione operativa**: l'affermazione richiesta — *"i file possono essere usati per
fini commerciali senza problemi"* — **non può essere confermata**. Per un'edizione
commerciale servono le bonifiche del §7 **oppure** un contratto di autorizzazione CTPS,
**e comunque** la rimozione/sostituzione di tutto il materiale Forgotten Realms (§6).

---

## 2. Basi normative considerate

- **Regolamento del Palio (Comune di Siena)** — in particolare:
  - **art. 4**: le 17 Contrade, i loro stemmi e colori (allegato A del Regolamento);
  - **art. 8**: divieto di concorsi, lotterie e iniziative con interessi economici riferite al Palio;
  - **art. 9, co. 2**: *«Le loro insegne, bandiere, stemmi, imprese, costumi e raffigurazioni singole o collettive non possono essere riprodotte ed esposte al pubblico, o diffuse, senza la preventiva autorizzazione della Contrada interessata e del Magistrato delle Contrade. I contravventori sono perseguiti nei modi di legge.»*
- **Consorzio per la Tutela del Palio di Siena** (statuto art. 2 + politiche di tutela):
  - simboli e **colori** delle Contrade **registrati come marchi**; CTPS e Contrade unici titolari;
  - produzione di beni con riferimenti a Contrade/Palio **solo con espressa autorizzazione** (contratto oneroso per fini commerciali; "nulla osta" per fini non commerciali);
  - divieto di **accostamenti pubblicitari** con l'immaginario contradaiolo; il Consorzio richiama una *«corposa giurisprudenza»* a proprio favore.
- **Ordinamento generale** (il Regolamento comunale non vincola di per sé terzi fuori Siena, ma i diritti sono azionabili tramite): marchi registrati e marchi notori (art. 20 c.p.i., incl. tutela contro l'agganciamento alla rinomanza), diritto d'autore (l. 633/1941) sull'iconografia moderna, concorrenza sleale/agganciamento (art. 2598 c.c.).

---

## 3. Criticità riscontrate (bloccanti per uso commerciale)

### 3.1 Titoli araldici ufficiali riprodotti alla lettera
File: `...P2D-PALIO-CHANNATHGATE-AVVENTURA.md` §1.

| Nel repo | Denominazione ufficiale senese |
|---|---|
| *Nobile Contrada dell'Oca* | identica |
| *Nobil Contrada del Bruco* | identica |
| *Contrada Sovrana dell'Istrice* | identica |
| *Contrada Priora della Civetta* | identica |
| *Contrada del Leocorno* | identica |
| *Contrada della Torre / del Drago* | identiche |

Le denominazioni ufficiali sono tra i segni distintivi registrati/gestiti dal CTPS. È
l'elemento **più facilmente attaccabile** in un contesto commerciale.

### 3.2 Livree (combinazioni di colori) identiche — 8 su 8
I colori sono esattamente le livree ufficiali (che il Consorzio dichiara registrate come
marchi): Oca *verde e bianco bordati di rosso*; Torre *amaranto listato di bianco e
azzurro*; Bruco *giallo e verde listati d'azzurro*; Istrice *bianco con liste rosso, nero
e azzurro*; Drago *rosa/rosso e verde listati di giallo*; Civetta *nero e rosso listati
di bianco*; Leocorno *bianco e arancio listati d'azzurro*; Onda *bianco e celeste*.

### 3.3 Motti: dichiarati "originali", in realtà parafrasi riconoscibili
La nota IP interna (AVVENTURA §1, STEMMI-CANTI coda) afferma che i motti sono
*originali*. Il confronto smentisce in parte:

| Contrada | Motto ufficiale (confronto) | Motto nel repo |
|---|---|---|
| Istrice | *Sol per difesa io pungo* | *Pungo solo chi mi assale* |
| Leocorno | *Fiede e sana ugualmente il corno ch'io porto in fronte* | *Ferisce e sana il corno che porto* |
| Torre | *Oltre la forza, la potenza* | *Oltre il ferro, la volontà* |
| Civetta | *Vedo nella notte* | *Guardo dove la notte tace* |
| Drago | *Il cuor che nel petto m'arde divien fiamma nella bocca* | *Il cuore che arde parla in fiamme* |
| Onda | *Il colore del cielo, la forza del mare* | *Il cielo mi colora, il fiume mi arma* |
| Oca | *Clangit ad arma* ("suona all'armi") | *Al suono dell'oro, all'armi* |
| Bruco | *Come rivoluzion suona il mio nome* | *Nell'ombra mi rivolto* |

Presi da soli sarebbero difendibili come parodia/ispirazione; **sommati** a nomi, titoli
e colori identici rafforzano l'evocazione dei segni tutelati.

### 3.4 "Piazza il Campo" nella tavola raster
`P2D-Palio-Allegati/mappe/piazza-del-palio-panorama.png` etichetta la piazza
**"PIAZZA IL CAMPO OF CHANNATHGATE"** e la disegna a conchiglia con **nove spicchi
radiali in cotto** — la firma visiva di Piazza del Campo di Siena. Il toponimo reale va
rimosso per qualsiasi uso pubblico/commerciale (nei testi la piazza è già chiamata
correttamente "Piazza del Palio").

### 3.5 Rivalità storica replicata
La rivalità **Oca ↔ Torre** riproduce una rivalità reale; ulteriore indizio di
agganciamento. (Le altre rivalità del repo sono inventate.)

### 3.6 Contesto: scommesse e "partiti" a fini di gioco
L'art. 8 Reg. vieta iniziative con interessi economici legate al Palio reale. Le
scommesse **in-fiction** dell'avventura non vi ricadono (mondo immaginario), ma un
prodotto commerciale che presenti corruzione/scommesse **come "il Palio"** presta il
fianco alla censura del CTPS sull'uso *«lesivo o denigratorio dell'immagine della
festa»* — la loro politica di tutela copre anche contesti d'uso offensivi.

---

## 4. Elementi verificati e risultati POSITIVI

- **Stemmi SVG** (`P2D-Palio-Allegati/stemmi/*.svg`): arte vettoriale originale,
  composizioni diverse dall'iconografia ufficiale, con innesti Faerûn (moneta di Waukeen,
  disco di Shar, stella di Mystra, catene spezzate, falce di Selûne). **Non sono copie**
  degli stemmi reali. ✅
- **Tavole raster** (`channathgate-mappa.png`, panorama): città immaginaria, distretti
  con nomi inglesi originali; nessuno stemma/bandiera senese riprodotto. ✅ (resta il
  problema del label "Piazza il Campo", §3.4, e la **provenienza non documentata** dei
  PNG "forniti dal DM": va tracciata la licenza/fonte prima di qualsiasi uso commerciale).
- **Nessuna copia testuale del Regolamento**: il lessico tecnico (tratta, mossa, canapi,
  nerbo, barbaresco, drappellone…) è usato come terminologia storica descrittiva, non
  come riproduzione del testo. Peraltro il Regolamento è un atto ufficiale della PA
  (escluso dal diritto d'autore ex art. 5 l. 633/1941). ✅
- **Note IP presenti** in AVVENTURA §1 e STEMMI-CANTI (coda): dichiarano ispirazione
  storico-culturale e **uso non commerciale** — coerenti con lo stato attuale del repo,
  ma vanno corrette dove affermano che i motti sono "originali" (sono parafrasi, §3.3).
- **Icone game-icons.net** (solo proposte in STEMMI-CANTI, non ancora integrate):
  licenza **CC BY 3.0**, compatibile anche con uso commerciale **con attribuzione**. ✅

---

## 5. Perché "commerciale senza problemi" = NO (sintesi giuridica)

1. Il CTPS è titolare/gestore di **marchi registrati** su denominazioni, simboli e
   colori delle Contrade e per prassi **agisce in giudizio**; la produzione di beni con
   riferimenti alle Contrade è subordinata ad **autorizzazione contrattuale onerosa**.
2. Anche senza copia fotografica degli stemmi, la **combinazione** nome + titolo
   ufficiale + livrea identica + motto parafrasato realizza un richiamo inequivocabile
   ai segni tutelati: profilo di rischio per **contraffazione/evocazione di marchio
   rinomato** (art. 20, co. 1, lett. c, c.p.i.) e **concorrenza sleale per agganciamento**
   (art. 2598 c.c.), azionabile in Italia (foro naturale: Siena/sezioni specializzate).
3. L'eccezione parodistica/trasformativa aiuta l'opera **gratuita**; in ambito
   **commerciale** l'orientamento italiano sul merchandising evocativo è restrittivo.

---

## 6. Blocco indipendente: IP Wizards of the Coast (assorbente per TUTTO il repo)

A prescindere dal Palio, l'arco (e il repo intero) **non è commercializzabile** perché
contiene materiale **Forgotten Realms / D&D non-SRD** di Wizards of the Coast:
- **Channathgate** è una località canonica dei Reami (Channath Vale/Shaar), non un nome
  inventato; divinità FR ovunque (Mystra, Shar, Ilmater, Selûne, Waukeen, Torm, Mask…);
- PNG e trama derivano da **Red Hand of Doom** (Lord Jarmaath, Azarr Kul, Abithriax,
  Rhest, il Ghostlord…), avventura protetta;
- la **GPL-3** del repo può coprire solo il materiale proprio dell'autore: **non può
  licenziare IP di terzi** (WotC, CTPS), né sanarne l'uso.

Per un prodotto commerciale servirebbe una riambientazione world-neutral (o SRD-only)
oltre alle bonifiche Palio del §7.

---

## 7. Checklist di bonifica per un'eventuale edizione commerciale

1. **Rinominare le contrade** (niente Oca/Torre/Bruco/Istrice/Drago/Civetta/Leocorno/
   Onda): animali/simboli diversi o nomi di fantasia.
2. **Eliminare i titoli ufficiali** ("Nobile", "Sovrana", "Priora", "Capitana" riferiti
   a quelle contrade).
3. **Cambiare le livree**: combinazioni di colori diverse da tutte le 17 reali.
4. **Riscrivere i motti da zero** (non parafrasi di quelli reali).
5. **Rimuovere "Piazza il Campo"** dal PNG panorama (rinominare la fascia testo) e
   attenuare la geometria "a nove spicchi".
6. Rinominare l'evento (es. "la Corsa del Drappo di …") o mantenere "palio" solo come
   **nome comune** storico (le corse dette "palio" esistono in decine di città: il
   termine generico non è monopolizzabile, l'identità senese sì).
7. Correggere le **note IP** interne (§3.3) e documentare la **provenienza delle tavole
   raster**; se si integrano icone game-icons.net, aggiungere `CREDITS.md` (CC BY 3.0).
8. **Riambientare fuori da Forgotten Realms** (§6) o pubblicare solo sotto uso privato.
9. In alternativa alle bonifiche 1–6: richiedere al CTPS un **contratto di
   autorizzazione** (oneroso) o, per usi non commerciali pubblici, un **nulla osta**.

---

## 8. Stato attuale del repo rispetto ai due documenti

- **Nessuna violazione "attiva" del Regolamento** in senso stretto: il Regolamento
  disciplina la festa reale (corse, sorteggi, cavalli) e non è replicato testualmente;
  gli stemmi reali (allegato A) **non** sono riprodotti graficamente.
- **Compatibilità con le politiche CTPS**: accettabile **solo** finché l'uso resta
  privato/non commerciale, come dichiarato nelle note IP interne. Gli elementi del §3
  restano il punto debole e andrebbero bonificati anche solo per prudenza nella
  pubblicazione libera su GitHub.
