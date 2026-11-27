# Verificatore logico (Prolog) per le regole: esito della misura

Data: 2026-11-11. Richiesta del DM: valutare lo stack «grafo di eventi + regole
in Prolog + la regola violata o il controesempio restituiti all'LLM perché si
corregga», chiamato attraverso il server MCP, e misurare se entra nel repo.
Decisione in [ADR-0124](../../adr/ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md).

## 1. Cosa c'era già (audit)

| Pezzo dello stack proposto | Nel repo oggi |
|---|---|
| Server MCP che chiama le regole | c'è: `scripts/mcp_server.py` (rumblingstone-tools, ADR-0030), 137 tool dal manifest, allowlist, sola lettura per difetto |
| L'LLM come client, verificatori deterministici | è la regola di ADR-0067: gli script non chiamano modelli, l'LLM chiama i tool e ciò che produce passa dai cancelli |
| «Grafo di eventi» con rifiuto dell'azione insicura | `campaign/state.yaml` + `dmcore/delta_sessione.py`: un delta si applica tutto o niente, e un `da` diverso dallo stato di oggi lo rifiuta (è l'esempio del rollback, in versione nostra); `validate_state.py` R1-R12 |
| Regole come dati | sì: `sistemi/<id>/dati/*.toml` + formule simpleeval (ADR-0111/0112) |
| La regola esatta che fallisce | in parte: `talenti.manca` dà «Des 13 (ha 11)», i validatori danno R1…R12, F1…O3; molti altri danno testo libero |

**Il buco vero trovato**: nessun cancello controlla i **prerequisiti dei talenti
sulle schede che esistono**. `talenti.manca` lo usa solo il generatore. Per
questo il caso di prova è questo.

## 2. Banco di prova

- `estrai.py` legge le 243 schede del Bestiario con `dmcore.lettura_creatura`
  (126 leggibili, **74 con una riga Talenti/Feats**), 263 talenti riconosciuti,
  74 nomi non riconosciuti (22%, quasi tutti talenti fuori SRD o nomi italiani
  non nel lessico: «Incantesimi Focalizzati», «Multiattacco», «Attacco in Volo»).
- Gli **stessi fatti** vanno a tre motori: Python (`talenti.manca`, il codice che
  c'è), SWI-Prolog 9.0.4 (`regole.pl`, processo esterno), clingo 5.8.3 (ASP,
  ruota PyPI, dentro Python).
- `muta.py` inietta 141 difetti nelle schede pulite (caratteristica, BAB,
  talento prerequisito, livello di classe a soglia − 1).

## 3. Misure

| Misura | Python (esistente) | SWI-Prolog | clingo |
|---|---|---|---|
| Violazioni sulle 74 schede vere | 30 | 30 (stesse) | 30 (stesse) |
| Difetti iniettati trovati | **141/141** | 141/141 | 141/141 |
| Difetti in più trovati dalla chiusura transitiva | — | **0** | — |
| Tempo, 141 mutanti | **0,8 ms** | 56,5 ms (processo) | 30,5 ms |
| Righe di regola | 27 | 32 + 70 di traduzione fatti | 14 + la stessa traduzione |
| Come entra nel pacchetto | già dentro | binario di sistema (apt), **non** si porta nel bundle; janus (ponte Python) solo da 9.1, Ubuntu 24.04 ha 9.0.4 | ruota PyPI MIT, si porta nel bundle |
| Errori introdotti dalla traduzione | — | 0 (dopo la codifica UTF-8) | **3 falsi positivi** al primo giro (costante `character` contro stringa `"character"`) |

**La chiusura transitiva non aggiunge niente nella verifica.** Nei dati 3.5 i
prerequisiti indiretti sono già ripetuti su ogni talento (0 su 110); nel PF1e
no (89 su 1.227), ma una scheda che ha il talento intermedio viene già
controllata su quello, e una che non lo ha viene già segnalata per la sua
mancanza. La ricorsione serve a **pianificare** («che cosa devo prendere per
arrivare a Turbine di Colpi»), non a verificare.

## 4. Cosa ha trovato davvero il lavoro (indipendente dal motore)

1. **30 violazioni in 19 schede** del Bestiario. Campione letto a mano su 8
   schede: 6 hanno difetti veri (es. drow assassina: Tiro Preciso senza Tiro
   Ravvicinato, «Attacco Rapido» = Spring Attack senza Schivare/Mobilità;
   ogre frantumapietra: Incalzare Potenziato senza Incalzare; Krusk: Duro a
   Morire senza Resistenza Fisica; guardia nobile drow: Combattere con Due
   Armi Migliorato con BAB +3; Skullcrusher: Combattere con Due Armi con Des 11),
   2 sono errori di **lettura** (la classe non sta nella riga `tipo:`, quindi
   chierica e maga risultano senza livello d'incantatore). Il monaco dà 5 falsi
   positivi perché i talenti bonus del monaco ignorano i prerequisiti e nessuno
   dei tre motori lo modella ancora. Nessuna correzione fatta: sono schede di
   canone, decide il DM.
2. **D1, difetto nei dati 3.5**: in `sistemi/dnd35/dati/talenti.toml` la tabella
   `[capacita]` usa le classi in italiano (`chierico`), i prerequisiti `classe`
   in inglese (`fighter`), e `genera_creatura.py` passa l'italiano. Verificato:
   `manca('dnd35', 'Weapon Specialization', guerriero 4)` → «fighter 4° livello»,
   quindi un guerriero 3.5 generato non prende mai Specializzazione in
   un'Arma.
3. **D2**: `Leadership` chiede `classe.character`, che nessuno scrive in
   `Stato.livelli`: il generatore la considera sempre non presa.

Formalizzare le regole in un'altra lingua ha fatto emergere D1 e D2, perché
obbliga a dare una sola identità a ogni classe. Lo stesso risultato lo dà un
test Python sulle chiavi; non serve un motore logico per tenerlo.

## 5. Cosa non è stato misurato

- **Il giro di autocorrezione dell'LLM** (messaggio libero contro «regola +
  atteso + ha»): nel container non c'è una chiave per un modello, e ADR-0067
  vieta agli script di chiamarne uno. Protocollo proposto: 40 dei 141 mutanti,
  l'agente li corregge via MCP una volta con il messaggio di oggi e una volta
  con l'uscita strutturata, alla cieca; si conta chi arriva a 0 violazioni in
  un giro senza introdurre difetti nuovi.
- **Il grafo di eventi del canone** (chi sa cosa, chi porta cosa nel tempo):
  qui la parte difficile è estrarre i fatti dalla prosa, non ragionarci sopra.
  `coerenza_campagna.py fatti` lo fa con prudenza a regex; un motore logico non
  cambia quel collo di bottiglia.

## Riprodurre

```bash
sudo apt install swi-prolog-nox            # solo per il confronto
pip install clingo==5.8.3                  # solo per il confronto
cd plans/esperimenti/prolog-verificatore-2026-11-11
python3 estrai.py > fatti-bestiario.json
python3 verifica_python.py fatti-bestiario.json
python3 verifica_prolog.py fatti-bestiario.json
python3 verifica_clingo.py fatti-bestiario.json
python3 muta.py fatti-bestiario.json       # scrive misure-mutanti.json
```

## 6. Dopo la scelta del DM (2026-11-11, «Strumento talenti in Python via MCP»)

- `scripts/verifica_talenti.py`, nel manifest e nel server MCP in sola lettura.
  Prova end-to-end: `tools/call verifica_talenti` su Krusk restituisce
  `{"regola": "talento", "atteso": "Endurance", "riga": 20}`.
- Falsi positivi tolti dal banco: 5 del monaco (talenti bonus senza
  prerequisiti), 1 di Jorr (Tiro Rapido dello stile del ranger), 1 di Khorn (Competenza negli Scudi data dalla classe), 2 di
  schede senza classi dichiarate (passano fra i non verificabili). Da 30
  violazioni in 19 schede a **21 in 11**.
- D1 e D2 corretti in `talenti.manca`; nell'impronta delle creature generate
  cambiano solo i talenti che la correzione vuole (40 voci 3.5: Autorità ai
  comandanti, Arma Specializzata e Arma Focalizzata Superiore ai guerrieri,
  Padronanza degli Incantesimi al mago).

## 7. Cascata delle fonti e talenti dei manuali (DM, 2026-11-12)

Il DM ha chiesto che la verifica segua l'ordine **SRD d20 → D&D 3.5 → PF1e** e
che i prerequisiti mancanti si cerchino nel repo e in rete (PCGen compreso).

- **SRD 3.5 completo**: i dati avevano solo `feats.md` (110 talenti).
  `estrai_talenti.py` ora legge anche i talenti dei mostri, epici, psionici e
  divini dell'SRD: **363**. L'impronta delle creature generate non cambia.
- **Manuali 3.5 fuori SRD**: dndtools.net non risponde. Due fonti, fuse in
  `sistemi/dnd35/dati/talenti_manuali.toml` (**2.193 talenti**) dagli script di
  `plans/esperimenti/talenti-manuali-35-2026-11-12/`:
  1. i dati PCGen di BahamutDragon/pcgen (campi `PRExxx`, 2.037 talenti);
  2. le tabelle Feat/Prerequisite delle 138 pagine dei manuali di
     srd.dndtools.org (1.553 talenti), lette con lo stesso lettore dell'SRD.
  In comune 1.156: **803 con gli stessi prerequisiti leggibili, 353 diversi**.
  Dove ci sono tutte e due vince la tabella del manuale e si aggiunge ciò che
  solo PCGen legge (esempio: a Two-Weapon Pounce PCGen non mette il BAB +6).
  1.126 talenti hanno almeno un prerequisito che la regola non sa leggere
  (`altro`: taglia, razza, tiro salvezza base, divinità). Si prendono solo
  nome, manuale e prerequisiti. Dei 3.998 nomi di `talenti_manuali_35.tsv`,
  **1.715 restano senza prerequisiti** (riviste Dragon, web, parte di Eberron).
- **PF1e** è l'ultima fonte: un nome che nessun libro 3.5 ha si verifica col PRD.
  Sul Bestiario di oggi non serve mai (0 casi), ma la prova c'è nel test.
- Ogni voce porta `fonte` (`srd`, `srd-mostri`, `3.5 Complete Warrior`, `pf1e apg`).
- **D3, trovato strada facendo**: il lessico scrive «Incantesimi focalizzati
  (bene, caos, legge o male)» e il generatore cercava «Incantesimi
  Focalizzati»: 28 creature «controllore» avevano la nota «non è un talento».
  Corretto in `talenti._per_chiave`.
- **Classi che la lettura non conosce** (classi di prestigio nel `tipo`: Deep
  Diviner, Hammer of Moradin, Berserker Furioso): livello d'incantatore, capacità
  e livelli di classe passano fra i non verificabili, con la nota che dice
  quali classi. Il mago specialista (Diviner 5) conta come mago.

Bestiario dopo il giro: 73 schede con talenti, **23 violazioni in 12 schede**
(21 da `srd`; 1 da `srd-mostri`: Colpo Terrificante senza Spingere Migliorato;
1 da un manuale: *Rend* del Draconomicon senza *Snatch*), 41 prerequisiti non
verificabili, 15 nomi non riconosciuti (8 sono pezzi di prosa presi per
talenti, 7 nomi veri: Virata ×3, Critico Potente, Iniziato della Natura, Anima
Forte, Specializzazione nello Scudo).

**Limiti da dire**: le due fonti non concordano su 353 talenti su 1.156, quindi
una violazione che viene da un manuale va riletta sul libro prima di toccare la
scheda. Il repo PCGen non dichiara una licenza, e srd.dndtools.org riporta
testo di manuali non OGL. Qui entrano solo
fatti di regola (nome, soglie), come già per gli indici dei nomi; se il DM
preferisce non tenerli, `talenti_manuali.toml` si toglie e quei talenti
tornano «non verificabili, fonte 3.5 manuale».
