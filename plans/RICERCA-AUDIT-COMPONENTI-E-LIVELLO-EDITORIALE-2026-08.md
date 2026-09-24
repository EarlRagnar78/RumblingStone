# 🔍 RICERCA — Cosa manca, componente per componente, e cosa serve davvero per il livello editoriale

> **Cos'è.** Un audit di tutto il repo fatto *leggendo il codice e riproducendo i
> difetti*, non a impressione — nato dalla domanda del DM (2026-08-22) «cosa manca
> in RumblingStone, cosa si può aggiungere e migliorare di tutti i componenti»,
> posta insieme a una ricerca esterna su **Typst vs LaTeX**, sui template in stile
> Wizards of the Coast / Paizo e sulle «figure editoriali» dietro un manuale
> stampato.
>
> **Come leggerlo.** Il §1 è il verdetto in una pagina. Il §2 è la catena di
> stampa, dove stanno i difetti *verificati* — cioè riprodotti con un comando, non
> supposti. Il §3 traduce le figure editoriali della ricerca in skill di questo
> repo. Il §4 passa gli altri nove componenti. Il §5 dice cosa **non** fare. Il §6
> propone la sequenza. Il §7 corregge tre errori contenuti nella ricerca in
> ingresso, perché copiarli costerebbe una giornata.
>
> **Cosa questo documento non è.** Non era un piano approvato: al momento della
> scrittura nessun lotto era aperto. **Il 2026-08-22 il DM ha approvato E5 ed E8 e
> ha chiesto di eseguire tutto**: lo stato di attuazione è nel §9, in fondo.

---

## §1 · Il verdetto in una pagina

Il repo sta molto meglio di quanto la domanda lasci pensare: il testo è completo,
il canone è tracciato, la CI ha 70+ controlli, la pipeline mappe arriva a Foundry,
e da `ADR-0020` esiste una vera catena di stampa in Typst. **Il divario non è più
"manca l'infrastruttura", è "l'infrastruttura ha cinque buchi misurabili e una
mezza dozzina di rifiniture da manuale stampato".**

### I difetti verificati (non ipotesi: riprodotti)

| # | Difetto | Prova | Impatto |
|---|---|---|---|
| **D1** | **Le immagini non entrano nel volume da stampa.** Il convertitore markdown→Typst non gestisce `![alt](path)`: la sintassi cade nella regola dei link e l'immagine diventa **il testo dell'alt preceduto da `!`** | `sorgente()` sul manifest del Palio stampa 13 righe: `!Stemma Oca`, `!Piazza del Palio`, `!Channathgate`… ; stessa cosa su 6 ritratti del fascicolo giocatori del Drappo | **alto** — l'edizione «da libro» è l'unica delle due catene che *non* mostra gli stemmi, ed è quella che dovrebbe |
| **D2** | **Il monospazio non è embedded.** Il tema chiede `DejaVu Sans Mono` (`tema-rumblingstone.typ:143`) ma `scripts/typst/fonts/` contiene solo EB Garamond e Cinzel | `ls scripts/typst/fonts/` (al 2026-08; oggi i font stanno in `scripts/fonts/`, che contiene anche Inconsolata) <!-- validate-docs: ignore --> | medio — è *esattamente* il difetto che ADR-0020 voleva chiudere («i font restano quelli di sistema»), sopravvissuto nei blocchi di codice |
| **D3** | **Chiavi di manifest ignorate in silenzio.** La catena di stampa legge `title/subtitle/brand/banner/footer/front_matter` e basta: `cover_image`, `intro_md`, `header`, `player_footer`, `cover_tag`, `out` esistono nei manifest e nella catena HTML, e in stampa **non fanno niente e non avvisano** | `grep cover_image scripts/export_booklet_typst.py` → nulla; presenti in 9 manifest su 11 | medio-alto — ADR-0020 prometteva «la divergenza diventa un controllo automatico, non una promessa». Oggi è ancora una promessa |
| **D4** | **Nessun gate CI sulla stampa.** `typst` non è installato in CI: si verifica solo che il manifest delle schede *risolva*. Il tema `.typ`, il convertitore e i 4 booklet non hanno **nessuna** prova che compilino | `.github/workflows/ci.yml`, step «Schede pregenerate — manifest risolvibile senza typst» | alto — è l'unico pezzo del repo dove una regressione arriva al DM invece che alla CI |
| **D5** | **La scorecard di qualità non copre la catena editoriale.** `docs/audit/SCORECARD.md` è del 2026-07-24; `export_booklet_typst.py`, `build_chapter_marks.py` e `dmcore/schede.py` sono di agosto | la sezione D elenca 3 script, oggi sono 6 | basso, ma è un contratto ADR-0012 che scade da solo |

### Il divario che il DM sente ma non ha un nome

Le due catene ora **producono due libri diversi**. La stampa ha EB Garamond
embedded, capolettera no, fregi sì; l'HTML — e quindi i ~40 PDF A4 di
`export_booklet_pdf.py` — usa ancora **Georgia**, font di sistema
(`build_booklet_html.py:81`). Lo stesso capitolo, dato a due giocatori su due
macchine, ha due facce. Il divario **[2] tipografia embedded** del capitolato del
Drappo è chiuso **a metà**: sul binario nuovo sì, su quello che il gruppo usa
davvero no.

---

## §2 · La catena di stampa: dai difetti alla rifinitura da manuale

### §2.1 · Le cinque riparazioni (nessuna decisione da prendere, sono bug)

1. **Immagini in Typst** (D1). Una regola nel convertitore, prima di quella dei
   link: `![alt](src)` → `#figure(image("/percorso", width: …), caption: [alt])`.
   Da decidere una volta sola e scrivere nel tema, non nei master:
   larghezza di default in colonna (100% della colonna), soglia oltre la quale
   l'immagine **scavalca le due colonne** come già fanno le tabelle da 4+ colonne,
   e cosa fare se il file non esiste (avviso a `stderr` + segnaposto, **mai** un
   volume che compila con un buco silenzioso).
2. **Monospazio embedded** (D2). O si aggiunge un mono OFL a `fonts/` con il suo
   `OFL.txt` (candidati da verificare, non da ereditare da qui), o si toglie il
   `show raw` e i blocchi di codice usano il Garamond. La seconda è gratis e in un
   manuale di gioco i blocchi `raw` sono quattro.
3. **Parità fra i manifest** (D3). Non «implementare tutte le chiavi»: **dichiarare
   il contratto**. Uno `schemas/booklet_manifest.schema.json` (il repo ne ha già
   tre in `scripts/schemas/`) più un controllo che, per ogni chiave dichiarata,
   dica quale catena la consuma. Le chiavi che la stampa non usa diventano un
   **warning esplicito**, non un silenzio.
4. **Gate CI sulla stampa** (D4). `typst` è **un singolo binario statico**: in CI si
   scarica in ~2 s da GitHub Releases (Apache 2.0, versione **fissata**, mai
   `latest` — un compilatore che si aggiorna da solo è una CI che diventa rossa di
   notte). Il gate minimo: compilare i 4 manifest del Drappo e il Palio, e
   verificare che il PDF esista, superi una soglia di byte e **contenga i
   segnalibri attesi**. Costo stimato: mezza giornata; è il controllo che oggi
   manca di più.
5. **Scorecard** (D5). Rigenerare le sezioni D/G con i sei script nuovi.

### §2.2 · Le rifiniture che separano «documento impaginato» da «manuale»

Qui non ci sono bug: c'è il mestiere. In ordine di rapporto effetto/costo.

| | Cosa | Perché conta al tavolo | Costo | Dove si tocca |
|---|---|---|---|---|
| **R1** | **Capolettera** a inizio capitolo e a inizio scena | è il segno che dice «qui comincia qualcosa» prima che il lettore legga il titolo; è la firma di un AP | basso | tema + una direttiva nei master |
| **R2** | **Blocco statistiche come componente**, non come prosa | il Bestiario ha **161 schede** che oggi in stampa escono come paragrafi: CA, pf e TS annegati nel testo. Al tavolo la scheda si consulta in tre secondi o non si consulta | **medio-alto** (vedi §3: serve il dato strutturato) | tema + `dmcore` |
| **R3** | **Margini speculari** (`inside`/`outside`) | oggi `x: 1.7cm` simmetrico (`tema:90`): stampato fronte-retro e rilegato, il testo entra nella piega. È una riga di codice | **bassissimo** | `tema:90` |
| **R4** | **Riquadro laterale** (regola opzionale / nota di ambientazione), distinto da `#leggi` e `#nota` | i due box attuali coprono «leggi ad alta voce» e «regia DM»; manca il terzo caso — la regola facoltativa — che oggi diventa prosa indistinguibile | basso | tema |
| **R5** | **Modalità carta bianca** (`--carta bianca`) | l'avorio `#f6efe0` copre **ogni** A4: su una stampante di casa sono 60 pagine di fondo pieno. Un manuale si stampa anche in economia | basso | tema + flag |
| **R6** | **Segno di fine sezione** (il quadratino/rombo di Paizo) e **ornamenti al numero di pagina** | dicono al lettore «la voce finisce qui» senza una riga vuota; costano due glifi | bassissimo | tema |
| **R7** | **Riferimenti interni cliccabili**: `vedi §4` → link, `[testo](file.md)` → rimando reale invece che testo piatto (`export_booklet_typst.py:144`) | in un PDF di 60 pagine un rimando non cliccabile è un rimando che nessuno segue | medio | convertitore |
| **R8** | **Indice analitico** (mostri, PNG, luoghi, oggetti) | è la differenza fra consultare e sfogliare; Typst lo fa nativamente con contatori e `query` | medio | tema + convenzione nei master |
| **R9** | **Imposizione** — A5 piegato su A4, o fascicolo a punto metallico | è l'unico modo di avere *un libretto* invece di una risma. Typst la fa con una seconda passata sul PDF | medio | script nuovo |
| **R10** | **Copertina vera** (`cover_image` in stampa, chiude anche D3 e il divario **[5]** del capitolato) | — | basso | tema |
| **R11** | **Tag PDF / accessibilità** | oggi la compilazione **ripiega su `--no-pdf-tags`** per un bug interno di Typst 0.15.1 e lo dichiara. Va **riprovato a ogni aggiornamento**, con una riga in CI che fallisce quando il ripiego non serve più — così la riga si toglie da sola | basso | `compila()` |
| **R12** | **Fondo carta come texture**, non come tinta piatta | è il 20% dell'effetto «libro» a costo di un'immagine; ma pesa sul PDF e sull'inchiostro. Va insieme a **R5** | basso | tema |

### §2.3 · I numeri della ricerca in ingresso, misurati su questo tema

La ricerca esterna proponeva un blueprint editoriale (margini, corpo,
interlinea, gutter). Confrontato con `tema-rumblingstone.typ`, il quadro è
**meno drammatico di quanto la ricerca suggerisca**: metà dei parametri sono già
a posto, e due delle raccomandazioni non vanno applicate alla lettera.

| Parametro | Blueprint della ricerca | Qui oggi | Verdetto |
|---|---|---|---|
| Formato / colonne | A4, 2 colonne | A4, 2 colonne (`tema:175`) | ✅ |
| Margini | superiore/inferiore ~2.5 cm, **interno ≠ esterno** | 2.1 / 2.0 / **1.7 simmetrico** | ⚠️ manca la specularità → **R3** |
| Gutter fra colonne | 0.5–0.65 cm | **default Typst** (~7 mm, mai dichiarato) | 🟡 accettabile, ma va **scritto**: un default non è una scelta |
| Corpo del testo | 8.5–9.5 pt | 10.2 pt EB Garamond | 🟡 il Garamond ha occhio piccolo: 10.2 pt *lì* legge come ~9 pt altrove. **La misura giusta non è il corpo, sono i caratteri per riga**: colonna da ~8.4 cm ≈ 50 caratteri, contro i 35-45 di un manuale. Da verificare sul volume vero, non a occhio |
| Giustificazione | giustificato + sillabazione | `justify: true`, `lang: "it"` → sillabazione italiana attiva di default | ✅ (nessun intervento: è già corretto) |
| Rientro di prima riga | sì | `1.1em`, e Typst non lo applica dopo i titoli | ✅ |
| Tabelle larghe | a piena larghezza | ≥4 colonne flottano sulle due colonne (`tema:64`) | ✅ — è già la soluzione da manuale |
| Vedove e orfane | controllo | Typst ne gestisce una parte da solo; **il caso vero da controllare è il titolo in fondo colonna** (`set block(sticky: true)`) | 🔎 da verificare al primo volume, non da assumere |
| Palette | «crimson WotC / verde Paizo» | avorio/seppia/rosso propri | ✅ **e va tenuto così** — vedi §5 |

---

## §3 · Le figure editoriali della ricerca, tradotte in skill di questo repo

La ricerca in ingresso individua quattro mestieri dietro un manuale stampato
(layout designer, tipografo, art director, pre-press) e li mappa su «skill
agentiche». La mappatura è giusta, e su questo repo dice una cosa precisa:

| Mestiere | Qui c'è? | Cosa manca |
|---|---|---|
| **Art director** | ✅ `skills/rumblingstone-art-direction/` — bibbia visiva, scheda-personaggio, **gate di rifiuto** | niente: è la parte più matura |
| **Layout designer / tipografo** | ❌ **nessuna skill** | il mestiere vive dentro un `.typ` di 180 righe che nessun documento spiega: quando una tabella scavalca, quando una figura è a piena pagina, quando un box è `#leggi` e non `#nota`. È una **skill `rumblingstone-editoria`** che manca |
| **Pre-press** | 🟡 parziale | imposizione (**R9**), soglie d'inchiostro (**R5**), tag PDF (**R11**); CMYK/PDF-X restano fuori per scelta (ADR-0020) |
| **Data engineer degli statblocchi** | ❌ | è il pezzo grosso, qui sotto |

### Il pezzo grosso: gli statblocchi come **dato**, non come prosa

La ricerca chiama «Skill 1: Strict Schema-Driven Data Parsing» quello che qui è il
divario strutturale più profondo, e vale la pena vederlo per quello che è.

Oggi `scripts/monster_catalog.yaml` contiene **312 record** con
`id/name/cr/faction/role/environment/source_file`: è un **indice**, non una
scheda. I numeri veri — CA, pf, TS, attacchi, TpC, capacità — vivono come **prosa
italiana** dentro 161 markdown (`Bestiario/**`). Conseguenze, tutte già visibili:

- in stampa un mostro non può diventare un riquadro: nessuno sa quale numero è
  quale (**R2** è bloccato da qui);
- `suggest_encounter.py` bilancia sul GS dichiarato e **non può verificarlo**
  contro i numeri reali;
- l'export UVTT porta a Foundry muri e luci ma **non i mostri**;
- il potenziamento PNG (skill `npc-villain-boosting`) si fa a mano su prosa;
- un errore di trascrizione (un +7 diventato +1) non è rilevabile da nessun gate.

La strada che il repo userebbe se lo decidesse — coerente con ADR-0003 (master
markdown, layout generati): **un blocco YAML in testa alla scheda**, con i campi
meccanici, e la prosa che resta prosa sotto. Il markdown resta il master; il
validatore controlla la coerenza fra il blocco e il testo; il catalogo si arricchisce
da solo; il tema Typst guadagna `#statblocco()`; l'export VTT guadagna i mostri.

⚠️ **È il lavoro più costoso dell'intero documento** (161 schede, anche con un
estrattore semi-automatico) e la decisione è del DM. Se la risposta è no, **R2 va
chiuso come "non si fa"** invece di restare in sospeso.

---

## §4 · Gli altri componenti

### 4.1 · Mappe — il componente più maturo del repo
3 modalità, contratto JSON validato, renderer deterministico byte-identico, import
Watabou, import ultra-clear con report dei conflitti, export UVTT collaudato in CI.
**Cosa manca**: (a) le ~30 mappe ultra-clear non ancora migrate al contratto —
lavoro noioso e non urgente; (b) l'**editor visuale** è pianificato allo 0% e il suo
primo passo (`legend.json` condiviso + gate di sync) **ha valore da solo** anche se
l'editor non si fa mai; (c) le mappe non entrano nella stampa se non come immagini —
cioè oggi **non entrano affatto** (D1); (d) manca la **mappa versione giocatore**
(divario **[3]** del capitolato), che è una passata del renderer con i livelli
tattici spenti, non un disegno nuovo.

### 4.2 · Automazione DM (`dm.py`)
12 sottocomandi, apply engine su regioni marcate, visibilità per-PG, 31 test.
**Cosa manca**: il collaudo al tavolo — dichiarato, gated, giusto così. **Cosa si
può aggiungere**: (a) la **trascrizione locale della sessione** (già istruita in
`RICERCA-TOOL-ESTERNI-DM` come R1: whisper.cpp, MIT, offline) che chiuderebbe il
recap automatico fra le serate — richiede un ADR perché è la prima dipendenza da
binario esterno **dopo** Typst, e ora il precedente esiste; (b) `dm.py stampa`
come sottocomando: oggi la catena di stampa si invoca solo a mano, ed è l'unico
tool del toolkit fuori dall'orchestratore (ADR-0002).

### 4.3 · Immagini e arte
La skill c'è, i prompt ci sono, la bibbia visiva c'è, l'infrastruttura ComfyUI c'è.
**Manca la generazione**: zero raster (divario **[1]**, il più visibile di tutti) —
ed è gated sulla GPU del DM, non su di noi. **Cosa si può aggiungere senza GPU**:
lo **script che legge i prompt e fissa i seed** scrivendo le righe di
`PROVENIENZA.txt` (stdlib + urllib): è ciò che rende la serie *riproducibile*
invece che irripetibile, e si scrive prima di avere la scheda video.

### 4.4 · Bestiario
161 schede, catalogo generato, validatore con `--rules` non bloccante.
**Cosa manca**: il dato strutturato (§3), e i **token** in `Bestiario/tokens/` —
coda cosmetica già tracciata. **Cosa si può migliorare**: rendere `--rules`
bloccante quando il rumore sarà a zero; oggi è un controllo che nessuno legge.

### 4.5 · Skill (14)
Set focalizzato, governance in ADR-0008, build multi-agente, gate CI su
frontmatter e link. **Manca**: `rumblingstone-editoria` (§3). **Da valutare**: le
skill sono 14 e ADR-0008 avvisa sul costo di frammentazione — una in più va
motivata, non aggiunta per simmetria.

### 4.6 · Convertitori
`converters/` è il pezzo più vecchio e più lontano dallo standard ADR-0012 (voci
`1` e `0` in scorecard, dipendenze esterne non dichiarate, path storici). Non è
urgente: non sta sul cammino di nessuna sessione. Vale come **debito dichiarato**,
non come lavoro.

### 4.7 · CI e qualità
Ottima: 70 test, gate su piani, mappe, bestiario, moduli, standalone. **Buchi**:
la stampa (D4), `shellcheck` non bloccante, e — dettaglio che vale un minuto —
la CI installa `pyyaml` mentre gli script si dichiarano stdlib-only: la
contraddizione è nota (`compress_skills.py` in scorecard) e va o sanata o scritta.

### 4.8 · Contenuto e canone
Gli archi 07/08/09 sono chiusi come *piani* e aperti come *gioco*: la coda è tutta
gated sul tavolo, ed è la forma corretta. Nessuna azione.

### 4.9 · IP
ADR-0005 + il modulo standalone come dimostrazione di bonifica. Coda documentale
già tracciata (nota sui motti, provenienza delle 2 tavole del DM). **Va aggiunto
un punto nuovo**, che nasce proprio da questa ricerca: se un giorno si importa un
template Typst di terzi, la sua licenza e il suo *trade dress* entrano nel repo —
vedi §5.

---

## §5 · Cosa NON fare (le rinunce, scritte perché non si riaprano ogni sei mesi)

1. **Non passare a LaTeX.** La ricerca lo tratta come alternativa aperta: qui la
   decisione è già presa e motivata (ADR-0020). Typst compila in millisecondi, sta
   in un binario, e l'errore lo legge un umano. Niente di ciò che manca in §2 si
   risolve cambiando motore.
2. **Non importare `mythographer-5e`, `owlbear` o simili.** Esistono davvero e sono
   fatti bene, ma sono **il vestito di un altro**: replicano la trade dress di D&D
   5e (bordo pergamena, banda cremisi, blocchi mostro), cioè l'identità visiva di
   Wizards — esattamente il terreno che ADR-0005 tiene a distanza. Il repo ha già
   una sua faccia (avorio/seppia/rosso, medaglioni, fregi); **è un vantaggio, non
   una mancanza**.
3. **Non usare `@preview/<pacchetto>` senza vendorizzarlo.** Typst scarica i
   pacchetti dalla rete alla prima compilazione: significa build non riproducibile
   e una dipendenza di rete dentro una catena che oggi funziona offline. Se serve
   un pacchetto (p.es. `droplet` per **R1**), o si vendorizza nella cache locale
   con la sua licenza — c'è già il precedente ADR-0010 per le skill di terzi — o si
   scrivono le 30 righe a mano. Per il capolettera, 30 righe.
4. **Non inseguire CMYK/PDF-X adesso.** Rinuncia già dichiarata in ADR-0020: si
   riapre il giorno di una tiratura vera, e quel giorno si valuta Scribus.
5. **Non fare una seconda copia dei dati.** Vale per gli statblocchi (§3): il
   blocco YAML sta *dentro* il master, non in un file parallelo. Il repo ha già
   pagato questa lezione con le schede pregenerate.

---

## §6 · Sequenza proposta

Nessuno di questi lotti è aperto: è una proposta di ordine, con il costo onesto.

| Lotto | Contenuto | Costo | Gate |
|---|---|---|---|
| **E1** | D1 immagini + D2 mono + R3 margini speculari | mezza giornata | nessuno — sono bug |
| **E2** | D4 gate CI sulla stampa (typst a versione fissa) + R11 tag PDF | mezza giornata | nessuno |
| **E3** | D3 schema del manifest + parità dichiarata fra le due catene | mezza giornata | nessuno |
| **E4** | R1 capolettera, R4 riquadro laterale, R6 segni di fine, R10 copertina, R5 carta bianca | 1 giornata | nessuno |
| **E5** | Tipografia embedded **anche** sulla catena HTML (chiude [2] per davvero) | mezza giornata | ⚠️ tocca **tutti** i booklet della campagna: serve il via libera del DM |
| **E6** | Skill `rumblingstone-editoria` + scorecard aggiornata (D5) | mezza giornata | — |
| **E7** | R7 rimandi cliccabili, R8 indice analitico, R9 imposizione | 1-2 giornate | dopo E1-E4 |
| **E8** | **Statblocchi strutturati** → `#statblocco()` (R2) + mostri in UVTT + verifica GS | **grande** | ⚠️ decisione DM (§3) |

Fuori sequenza perché gated altrove: raster (GPU del DM), mappa versione
giocatore (una passata del renderer, si può fare in E4), trascrizione sessione
(ADR da scrivere), collaudo al tavolo.

---

## §7 · Errata della ricerca in ingresso

Da non copiare, e verificato punto per punto.

1. **Il pacchetto per il capolettera non si chiama `dropcap`.** La ricerca propone
   `#import "@preview/dropcap:0.1.0": dropcap`: quel pacchetto non è quello. Il
   pacchetto reale su Typst Universe è **`droplet`** (0.3.1), e la funzione è
   `dropcap`. Vale comunque il §5.3: prima di importarlo, vendorizzarlo.
2. **`center([...])` non esiste in Typst.** Ricorre in tre esempi della ricerca.
   La forma corretta è `align(center)[...]` — come già fa il tema del repo.
3. **`locate(loc => …)` è la vecchia sintassi.** Dalla 0.11 si usa `context`, che è
   quello che il tema usa già in testatina e piede. Copiare l'esempio della
   ricerca porterebbe indietro il codice, non avanti.

Marginali: il blueprint dei margini/corpo è ragionevole ma va misurato in
caratteri per riga (§2.3), e la palette proposta è di terzi (§5.2).

---

## §8 · Se si fa una cosa sola

**E1.** Un'edizione da stampa che non stampa gli stemmi, e che al loro posto
scrive `!Stemma Oca`, è l'unico difetto di questo elenco che un giocatore vede
prima del DM.


---

## §9 · Stato di attuazione (2026-08-22)

Mandato del DM, testuale: *«metti typst nella CI così si testa la compilazione,
E5 ok, E8 ok, e risolvi tutti i bug riscontrati… rendi disponibili i font
necessari direttamente nel repo… inserisci tutti gli enhancement necessari»*.

### I cinque difetti

| | Stato | Come |
|---|---|---|
| **D1** immagini | ✅ | `#figura()`; l'orizzontale scavalca le due colonne, la mancante dà avviso e segnaposto |
| **D2** monospazio | ✅ | Inconsolata in `scripts/fonts/`, insieme a Garamond e Cinzel e ai `.woff2` per l'HTML |
| **D3** chiavi ignorate | ✅ | `schemas/booklet_manifest.schema.json` + `validate_booklets.py`; `cover_image`, `intro_md` e `meta` ora valgono anche in stampa |
| **D4** nessun gate | ✅ | `typst` in CI a versione fissata + compilazione vera di tutti i volumi coi segnalibri |
| **D5** scorecard | ✅ | aggiornata coi sei script della catena editoriale |

### Due difetti che l'audit non aveva visto, trovati compilando

Il §1 diceva «riprodotti, non supposti». Compilare per la prima volta ha
mostrato che il quadro era peggio: **due booklet della campagna non avevano mai
compilato**.

- `**Seggio**/Deputazione`: grassetto attaccato a una barra — chiudeva male in
  Typst («unclosed delimiter»);
- `*Il peso **(nota.)***`: corsivo che contiene un grassetto — veniva spezzato
  lasciando un asterisco orfano *dentro* il grassetto.

L'enfasi ora esce come `#strong[...]`/`#emph[...]` e la regex è diventata una
pila. È la conferma pratica della tesi del §1: senza gate non si è «non
testati», si è «rotti e non lo sappiamo».

### I lotti

| Lotto | Stato | Nota |
|---|---|---|
| **E1** bug + margini speculari | ✅ | |
| **E2** gate CI + tag PDF | ✅ | il ripiego `--no-pdf-tags` resta, ma ora passa sotto la CI a ogni PR |
| **E3** schema + parità | ✅ | |
| **E4** rifiniture | 🟡 | fatti: riquadro laterale, versale, segni di fine, ornamenti, copertina, carta bianca, titoli `sticky`. **Non** il capolettera *annegato*: serve `droplet`, che Typst scarica dalla rete — è una decisione sul vendoring, non una riga di tema (ADR-0020 §rev. 5) |
| **E5** tipografia HTML | ✅ | nove booklet rigenerati; `--no-font-embed` per il file leggero |
| **E6** skill + scorecard | ✅ | `skills/rumblingstone-editoria/` |
| **E7** rimandi, indice analitico, imposizione | 🟡 | fatti i **rimandi cliccabili** fra capitoli dello stesso volume. Indice analitico e imposizione restano: il primo vuole una convenzione nei master, la seconda una dipendenza nuova |
| **E8** statblocchi | 🟡 | ADR-0021: formato, lettore, estrattore, `#statblocco()` in stampa, gate. **82 schede su 157 migrate**; le altre 75 sono a rapporto, campo per campo. Non si è inventato niente |

### Cosa resta, e perché non è «da fare quando c'è tempo»

Le quattro cose fuori sono **decisioni**, ognuna già scritta dove va presa:
capolettera annegato → vendoring dei pacchetti Typst; imposizione → una
dipendenza PDF nuova; indice analitico → una convenzione di marcatura nei
master; le 75 schede → o si completano a mano al tavolo, o si accetta che la
libreria abbia due velocità.

Gated altrove, come già dichiarato: le illustrazioni raster (GPU del DM), la
mappa in versione giocatore, il collaudo al tavolo.

---

## §11 · Chiusura (2026-09-03): chi ha chiuso cosa

Fra il 27 agosto e il 3 settembre le quattro code del §10 sono state chiuse — da
altre sessioni, dentro il **PIANO-CHIUSURA-CATENA-EDITORIALE**, non qui. Vale la
pena scrivere chi, perché per undici giorni questa ricerca è rimasta indicata in
`INDEX.md` come «aperta su quattro voci» mentre non lo era più: una riga di
tracciatura che non si aggiorna è peggio di una riga assente, perché la si crede.

| Coda | Chiusa da | Come |
|---|---|---|
| **capolettera annegato** | [ADR-0026](adr/ADR-0026-vendoring-pacchetti-typst.md) | `droplet:0.3.1` **vendorizzato** in `scripts/typst/packages/` con la sua licenza. La decisione che il §5 di questa ricerca diceva «va presa in un ADR suo» è stata presa così |
| **indice analitico** | ADR-0026 | `in-dexter:0.7.2`, sempre vendorizzato; le voci le marca l'esportatore dal glossario invece che a mano |
| **imposizione** | [ADR-0027](adr/ADR-0027-imposizione-con-pdfcpu.md) | `pdfcpu` come seconda dipendenza binaria — e la regola di degradazione pulita scritta **una volta sola in codice** (`scripts/binari.py`) invece che a parole in ogni script |
| **le 19 schede incomplete** | PIANO-CHIUSURA §H | Bestiario **157/157**: hanno insegnato al parser a leggere anche i dossier, invece di fermarsi dove si era fermato l'estrattore |

Resta una cosa sola, aggiunta oggi: **`--formato a5`**. Non è un doppione
dell'imposizione, le sta accanto — `pdfcpu booklet` prende il volume A4 e ne mette
due per foglio scalando al 71%, cioè porta il corpo da 10,2 pt a ~7,2. Comporre in
A5 (una colonna, 9,6 pt) e *poi* imporre tiene la misura di un tascabile vero.

Gated come sempre dichiarato: le illustrazioni raster, la mappa in versione
giocatore, il collaudo al tavolo, e le schede A4 dei quattro PG — in `PG/` non
esistono master di scheda personaggio, e il layout aspetta i numeri veri.
