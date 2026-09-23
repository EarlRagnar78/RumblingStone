# PIANO — La qualità del codice, misurata prima e dopo

> **Stato**: 🟡 **riaperto il 2026-09-23 col lotto E** (§8, una libreria per le creature). I lotti 0, A, B, C, D sono chiusi dal 2026-09-03; del lotto E resta E9, bloccato su D3
> **Aperto**: 2026-09-03
> **Nasce da**: domanda del DM — *«per ogni script si dovrebbe guardare: c'è una
> libreria o un tool open source che risolve il problema? posso usare oggetti già
> sviluppati negli altri script? sto ricreando la ruota? ci sono test che
> validano il mio codice? … se si ristruttura, i miglioramenti si devono poter
> misurare, suppongo con un ADR e un piano ben congegnato — se ne vale la pena.»*
> **Risposta breve**: sì, ne vale la pena per **tre cose su cinque**. Le altre due
> sarebbero cerimonia. Questo piano dice quali, con i numeri di partenza.

---

## §1 · La misura di partenza (presa il 2026-09-03, non stimata)

| Cosa | Numero | Come si rimisura |
|---|---:|---|
| Script in `scripts/` | 46 | `ls scripts/*.py \| wc -l` |
| Righe totali | 17.771 | `wc -l scripts/*.py` |
| Moduli condivisi in `dmcore/` | 8 | `ls scripts/dmcore/*.py` |
| Script che usano `dmcore` | **10 su 46** → **16** | `grep -l "from dmcore" scripts/*.py \| wc -l` |
| Script senza un test che li nomini | **18 su 46** → **2** (i due che misurano, di proposito) | vedi §5 |
| Corpi di funzione **identici** in file diversi | **1** | AST, vedi §5 |
| Implementazioni di `slug`/`slugify` | **7** definizioni, **10** chiamanti → **1** | `grep -c "def slug"` |
| Record del catalogo con id divergente | **3** (§1 diceva 9: era sbagliato, §2 ne elencava già 3) | vedi §2 |
| Dipendenze esterne dichiarate | **0** → **il registro in `scripts/binari.py`**: Python minimo, 9 binari, 2 librerie, 9 catene | `python3 scripts/binari.py` |
| Script con uno **schema d'uso** documentato | 46 (nel manifest) | `tools_manifest.py --check` |
| Tool con un **caso d'uso** documentato | **0 su 54** → **54** | `tools_manifest.py --check` |

**La lettura onesta di questi numeri.** Un solo corpo di funzione duplicato su
17.771 righe è un risultato **buono**: il repo non è un ammasso di copie. Ma
`dmcore` è usato da **dieci script su quarantasei**, e le sette `slug` mostrano
dove la ruota è stata rifatta davvero.

---

## §2 · Il difetto che questa misura ha trovato

Sette funzioni che fanno la stessa cosa, e **una si comporta diversamente**:

```python
# sei script su sette
s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# build_monster_catalog.py — SENZA la normalizzazione
re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:80]
```

Senza `NFKD`, una lettera accentata non viene traslitterata: **viene buttata via**.

| Nome nel Bestiario | id nel catalogo | id ovunque altrove |
|---|---|---|
| `Lómyn RedTongue, bardo mezzelfo` | `l-myn-redtongue-…` | `lomyn-redtongue-…` |
| `Razorfiend «Blackspawn Alfa» — spawn draconico d'élite` | `…-d-lite` | `…-d-elite` |
| `Ghaurush … «il preventivo è scaduto»` | `…-preventivo-scaduto` | `…-preventivo-e-scaduto` |

**Nove record veri.** Non è teoria: è il catalogo su cui `suggest_encounter`
lavora, e sono id che nessun altro strumento della catena ricalcolerebbe uguali.

---

## §3 · Le domande del DM, una per una

### «C'è una libreria open source che risolve il problema meglio?»

**Quasi sempre sì, e quasi sempre non va usata** — ed è una decisione, non pigrizia.

Il repo è **stdlib-only** per un motivo che vale più delle librerie: gli
strumenti girano sul portatile del DM, prima di una sessione, senza rete e senza
`pip install`. Una dipendenza in più è un modo in più di non poter stampare il
booklet la sera del gioco. Le librerie che *sarebbero* migliori, e perché non ci
sono:

| Dove servirebbe | Libreria | Perché no |
|---|---|---|
| lettura HTML (`import_html_module`) | `beautifulsoup4`, `lxml` | `html.parser` basta; la conversione è stata fatta una volta |
| YAML (`monster_catalog`) | `PyYAML` | il sottoinsieme usato sta in 60 righe e non cambia |
| slug | `python-slugify` | **qui la libreria vincerebbe** — vedi §4, lotto A |
| PDF (`export_booklet_pdf`) | `reportlab` | Typst fa già tutto e non è Python |
| test | `pytest` | la CI usa `unittest`: **una dipendenza in meno nel percorso critico** |

⚠️ **Questa decisione non è scritta da nessuna parte.** È l'omissione vera:
`stdlib_only: true` sta in ogni voce del manifest come *constatazione*, mai come
*regola con un perché*. → **ADR proposto**, §4 lotto 0.

### «Posso usare oggetti già sviluppati negli altri script?»

Sì, e `dmcore` esiste apposta: `statblock` (il contratto del blocco),
`tabelle` (SRD e PF1e), `config`, `gitio`, `regions`, `schede`, `visibility`.
Ma lo usano **10 script su 46**. Le sette `slug` sono la prova che il riflesso
«guardo se c'è già» non è automatico.

### «Sto ricreando la ruota?»

Misurato: **una volta sola in modo grave** (le slug), **una volta in modo lieve**
(`col_label`, quattro istruzioni). Il resto del repo non duplica.

### «Ci sono test che validano il mio codice?»

370 test, e **18 script su 46 non ne hanno nessuno**. Non tutti servono allo
stesso modo: `compress_skills` e `measure_tokens` sono utilità di misura, e un
test lì è cerimonia. Ma `build_monster_catalog`, `validate_bestiario`,
`validate_maps` e `validate_modules` **sono cancelli della CI** e non hanno un
test che dimostri che bocciano davvero un file rotto — cioè: **non sappiamo se
quei gate funzionano**, sappiamo solo che passano.

Questo è il buco più serio del repo, e non è un problema di stile: è che un gate
che non boccia mai è indistinguibile da un gate rotto.

### «TDD e OOP migliorerebbero?»

**TDD: sì, e c'è la prova in questa PR.** Il generatore è stato scritto con il
collaudo come criterio d'accettazione, e il collaudo ha respinto la prima
versione (GS 7 con 38 pf). Poi i test hanno trovato altri tre difetti veri: il
chierico con la caratteristica sbagliata, i punteggi fuori banda, i due druidi
con incantesimi che non possono lanciare. **Nessuno dei quattro sarebbe emerso
rileggendo il codice** — sembravano tutti conti giusti.

**OOP: no, non come programma generale.** Questi script sono *filtri*: leggono
file, scrivono file, escono con un codice. Le funzioni sono la forma giusta, e
incapsularle in classi aggiungerebbe cerimonia senza togliere un difetto. Dove
l'oggetto **serve davvero** ce l'ha già: `Statblocco` è una dataclass,
`Binario` una NamedTuple, `Ruolo` una dataclass congelata. Il criterio è
semplice: **un oggetto dove c'è uno stato con degli invarianti**, una funzione
dove c'è una trasformazione.

### «Uno schema d'uso renderebbe più facile il debug?»

**Esiste già, e nessuno se ne accorge**: `scripts/tools.manifest.json` dichiara
per ogni tool argomenti, ingressi, uscite, codici d'uscita, determinismo, effetti
collaterali. È la fonte di `docs/tools/`, del server MCP e del gate di copertura.
Quello che manca non è lo schema — è il **caso d'uso**: *«questo tool serve a
questa domanda, e la risposta giusta è questa»*. È da lì che nascono i test dei
18 scoperti.

---

## §4 · I lotti, con la misura di accettazione

### ✅ Lotto 0 — L'ADR che manca: perché stdlib-only
La decisione più importante del repo non è scritta. **Accettazione**: un ADR che
dica il perché (il portatile del DM, la sera della sessione, senza rete), le
eccezioni ammesse (`pdfcpu` e `typst` sono binari, non librerie — ADR-0027) e il
**criterio per rivederla**.

**Chiuso il 2026-09-03**: [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md).
Scrivendolo è venuta fuori una cosa che questo piano dava per scontata: la frase
«il repo è stdlib-only» **oggi è falsa in un punto**. Quattro tool dichiarano
`pyyaml` e la CI fa `pip install pyyaml` prima di `validate_skills.py`, che è un
gate bloccante. L'ADR la tratta come debito circoscritto invece di far finta che
non ci sia, e ne discende una coda: `compress_skills.py` importa `yaml` senza
guardia e muore con una traccia di stack, dove `validate_skills.py` esce con un
messaggio e codice 2.

### ✅ Lotto A — Una `slug` sola, e i tre id che si raddrizzano
`dmcore/testo.py` con **una** implementazione, parametrica su troncamento e
ripiego. Le sette copie la chiamano. **Accettazione**: `grep -c "def slug"` = 1;
i nove record divergenti tornano coerenti; un test con `Città`, `Lómyn`,
`d'élite` e `12–13` (trattino lungo).
⚠️ Rigenera il catalogo → alcuni id cambiano: **va fatto in un commit suo**,
perché i riferimenti esistenti vanno visti.

**Chiuso il 2026-09-03** con `scripts/dmcore/testo.py` (`slug`, `piega_ascii`) e
25 test in `scripts/tests/test_testo.py`. Sette mutazioni della funzione, sette
colte. Quello che il piano non aveva previsto:

1. **I chiamanti erano dieci, non sette.** `import_ultraclear`, `validate_maps`
   ed `export_uvtt` chiamavano `render_map_svg.slugify` dall'esterno, di
   proposito: quel modulo è la fonte unica della convenzione del nome-file di
   una mappa. La convenzione resta lì, ora come `nome_mappa()` (48 caratteri,
   ripiego «mappa»), e chiama la `slug` condivisa.
2. **Il difetto era di tutte e sette, non di una.** `build_monster_catalog` era
   l'unica senza `NFKD`, ma tutte facevano `encode("ascii", "ignore")`, che
   **cancella** i caratteri non-ASCII che NFKD non riduce a una lettera base
   invece di separarli. Effetto misurato sul corpus vero: `griglia 33×33` →
   `griglia-3333`, `CR 12–13` → `cr-1213`, `Cutaway Sud→Nord` → `sudnord`. Due
   valori incollati in uno, e nessuno se n'era accorto perché il risultato è
   comunque un id valido. `piega_ascii()` mette un separatore.
3. **Il troncamento sporcava l'id.** `t[:48]` avveniva dopo `strip("-")`, quindi
   un id tagliato in mezzo a un separatore finiva con un trattino penzolante.
   Tre SVG su 27 ce l'avevano.

Il conto vero dei record di catalogo sbagliati è **3**, non 9 (§1 corretto; §2
ne elencava già tre). La rigenerazione, nel suo commit, tocca **3 id di
catalogo e 5 nomi di SVG**.

### ✅ Lotto B — I quattro cancelli che nessuno ha mai visto bocciare
Un test per `validate_bestiario`, `validate_maps`, `validate_modules`,
`build_monster_catalog` che gli dia in pasto un file **deliberatamente rotto** e
verifichi che escano **non-zero**. **Accettazione**: 4 gate su 4 con un test
negativo. È il lotto che vale di più, perché oggi non sappiamo se funzionano.

### ✅ Lotto C — Il caso d'uso, dove i test nascono
Per i 18 script senza test, una riga di caso d'uso nel manifest (`use_case`:
*«a quale domanda risponde»*) e, dove il tool decide qualcosa, un test che lo
verifichi. **Accettazione**: 46/46 con caso d'uso; i tool che *decidono* (non
quelli che *misurano*) con almeno un test.

**Chiuso il 2026-09-03.** Il campo `use_case` sta su **54 voci su 54**, è
obbligatorio nello schema e ha un gate che non si accontenta della presenza: una
copia del `summary` o una frase che non è una domanda vengono bocciate (provato
con quattro manifest rotti a posta, quattro bocciati). Arriva anche dove serve,
in `docs/tools/README.md` e davanti al summary nelle descrizioni MCP, che è il
posto dove un agente sceglie fra 46 strumenti.

Gli scoperti erano **14**, non 18: il lotto B e il lotto A ne avevano già
coperti quattro. Dodici decidono e ora hanno un test (`test_tool_decidono.py`,
35 test); i due che restano fuori sono `measure_tokens` e `compress_skills`, che
misurano, e un test scritto lì lo dice per iscritto perché non sembri una svista.

⭐ **Il lotto è servito a più dei test.** I difetti che ha trovato sono tutti
dello stesso tipo: uno strumento che *dichiara* una decisione e poi non la
prende.

1. **`index_skills` usciva sempre con 0.** `main()` era chiamato senza
   `sys.exit()`, quindi il valore di ritorno finiva nel nulla: i codici del
   manifest erano una promessa che solo argparse manteneva.
2. **`index_skills` accettava una cartella sorgente inesistente** e scriveva un
   `index.json` con zero voci. Un file che c'è e sembra buono è peggio di un
   errore.
3. **`import_watabou` con un JSON rotto usciva con 1 per caso**, non per scelta:
   `JSONDecodeError` arrivava in cima e Python usciva così. Chi scarica un export
   da un sito riceveva venti righe di traccia. È lo stesso difetto che
   `binari.py` aveva già deciso di non fare per i binari.
4. **`dm_dossier -o` fuori dal repo andava in traccia di stack** su
   `relative_to`, che alza `ValueError` dove `is_relative_to` risponde e basta.
5. **`suggest_loot` prometteva un codice 3 irraggiungibile.** Il ramo esiste
   (riga 319) ma `parse_encounter_md` ha un ripiego che sintetizza sempre una
   proposta, quindi la lista non è mai vuota. Dato un file che non è un output di
   `suggest_encounter`, lo strumento ripiegava su un EL **10 scritto nel codice**
   e generava tesoro invece di protestare.

I primi quattro sono corretti qui. Il quinto è andato al DM, perché cambiarlo
cambia cosa succede al tavolo.

**✅ Chiuso il 2026-09-03 dal DM, che aveva ragione su due punti**
([ADR-0038](adr/ADR-0038-l-el-viene-da-una-gerarchia-dichiarata.md)).

Il primo corregge me: *«se è chiamato da suggest_encounter l'EL viene da lì»*.
È così — `suggest_encounter` emette `**Combined EL**` per ogni proposta, e nella
catena documentata il 10 non si vedeva mai. Il rischio era più stretto di come
l'avevo scritto.

Il secondo apre una porta che il lotto non aveva visto: *«si potrebbe generare il
loot guardando l'avventura»*. La fonte **esiste già** — `campaign/state.md`
dichiara `**Party APL:** 13` nell'intestazione, fuori dalle regioni `auto:` — e
**nessuno dei due strumenti la leggeva**. `suggest_encounter` pretendeva `--el` a
ogni chiamata, uscendo con 2 senza: il numero era nel repo e ogni preparazione di
scontro lo riscriveva a mano.

Ora la gerarchia è `--el` → il file → il Party APL → il rifiuto, in
`dmcore/tavolo.py`, e l'origine del numero si stampa. Il 10 muto non c'è più, il
codice 3 è tornato raggiungibile, e `suggest_encounter` senza argomenti è
diventato una domanda sensata invece di un errore d'uso. 19 test, **8 mutazioni
su 8 colte**.

Metodo del lotto B, di nuovo: **10 mutazioni, 10 colte** dopo aver buttato le due
che non erano mutazioni vere (un rinomino coerente, e un controllo che avevo
aggiunto ed era ridondante perché `convert()` lo faceva già — la ruota
riscritta, dentro il piano che parla di ruote riscritte).

### ✅ Lotto D — L'ambiente riproducibile
Il DM chiede *«quali sono i requisiti software e hardware?»*, e oggi la risposta
è sparsa fra `GUIDA-SETUP-MACCHINA`, `dm.py doctor` e `binari.py`.
**Accettazione**: un file solo che dichiari Python minimo, binari opzionali con
la loro degradazione, e cosa serve *davvero* per ogni catena; `doctor` lo legge
invece di avere la propria lista.

**Chiuso il 2026-09-03**, estendendo `scripts/binari.py` invece di aggiungere una
quarta fonte accanto alle tre che c'erano. Ora dichiara `PYTHON_MINIMO`, i due
binari accettati con un ADR, **sette opzionali** con il loro ripiego, le **due
librerie** e **nove catene** di lavoro con cosa serve a ciascuna. `dm.py doctor`
e `docs/guides/GUIDA-SETUP-MACCHINA.md` leggono da lì; `python3 scripts/binari.py`
stampa il quadro e, nell'ultima sezione, la riga che serve davvero prima di una
sessione: **quali catene partono stasera**.

Le divergenze erano vere e misurate:

| Domanda | `doctor` diceva | la guida diceva | la CI fa |
|---|---|---|---|
| Python minimo | ≥ 3.8 | 3.11+ | installa 3.11 |
| binari conosciuti | pandoc e xelatex, più i 2 del registro | 8 in tabella | 8 nel manifest |

E una scoperta che ha corretto un ADR appena scritta: **le librerie Python sono
due, non una.** ADR-0037 diceva che `pyyaml` era l'unica; `Pillow` c'era già, in
`build_booklet_html.py` e `build_image_derivatives.py`. La differenza fra le due
è quella che conta, ed è ora scritta nell'ADR: `pyyaml` sta in un gate della CI e
non degrada, `Pillow` sta fuori dai gate e degrada da sola. La seconda è la forma
che una dipendenza Python può avere sotto questa regola; la prima è il debito.

**9 mutazioni, 9 colte** (`test_ambiente.py`, 15 test). Due dei test confrontano
due fonti — il registro contro i workflow, il registro contro il manifest — ed è
quello il punto: se qualcuno riscrive un numero in uno dei due posti, cadono. Il
primo giro ne ha trovato subito uno vero: `bash`, dichiarato da quattro tool nel
manifest, mancava dal registro.

**Coda dell'ADR-0037, chiusa qui**: `compress_skills.py` fa `import yaml` con la
guardia ed esce con 2 come `validate_skills.py`, invece che con una traccia.

---

## §5 · Come si rimisura (i comandi, non le impressioni)

```bash
grep -l "from dmcore" scripts/*.py | wc -l          # oggi 10 / 46
grep -c "def slug" scripts/*.py | grep -v ':0' | wc -l   # oggi 7
python3 - <<'EOF'                                    # corpi identici: oggi 1
import ast, hashlib, pathlib, collections
c = collections.defaultdict(list)
for f in pathlib.Path("scripts").glob("*.py"):
    for n in ast.walk(ast.parse(f.read_text())):
        if isinstance(n, ast.FunctionDef) and len(n.body) > 2:
            c[hashlib.md5(ast.dump(ast.Module(body=n.body, type_ignores=[])).encode()).hexdigest()].append(f.name)
print(sum(1 for v in c.values() if len(set(v)) > 1))
EOF
```

---

## §6 · Ne vale la pena? La risposta onesta

**Sì per il lotto B, e non è vicino.** Quattro cancelli della CI senza un test
che li veda bocciare sono altrettante cose di cui crediamo di fidarci. Costo: mezza
giornata.

**Sì per il lotto A**, perché c'è un difetto vero e misurabile con tre record
già sbagliati. Costo: due ore più il commit di rigenerazione. *A consuntivo: il
difetto era più largo di così, vedi il lotto.*

**Sì per il lotto 0**, perché una decisione non scritta viene rimessa in
discussione ogni volta che qualcuno chiede *«perché non usiamo una libreria?»* —
com'è appena successo. Costo: un'ora.

**Forse per C e D**, e solo per i tool che *decidono*.

> **A consuntivo (2026-09-03).** Il DM ha chiesto di farli entrambi per intero,
> `use_case` compreso. Il «forse» era mal riposto in un punto: il lotto C ha
> trovato **cinque difetti veri**, più di quanti ne avesse trovati il lotto A.
> Dove il «forse» era giusto è il campo `use_case`: 54 righe di compilazione che
> non hanno trovato niente, e il cui valore è di là da venire — lo si vedrà
> quando un agente sceglierà lo strumento giusto perché la descrizione MCP dice
> a quale domanda risponde. Il lotto D ha trovato tre fonti che divergevano e un
> errore in un ADR scritta il giorno prima.
>
> E il difetto che il lotto C aveva lasciato aperto al DM ne ha generato un
> altro, più grosso di quello che chiudeva: il repo dichiarava il livello del
> gruppo e nessuno strumento lo leggeva ([ADR-0038](adr/ADR-0038-l-el-viene-da-una-gerarchia-dichiarata.md)).

**No a una riscrittura OOP**, e no all'adozione di `pytest` come dipendenza: la
prima aggiungerebbe cerimonia a codice che è già nella forma giusta, la seconda
metterebbe una dipendenza nel percorso critico della CI per comodità di scrittura.
Il vantaggio vero — TDD — non richiede nessuna delle due, e in questa PR è già
stato applicato: **quattro difetti trovati dai test che una rilettura non
avrebbe trovato**.


---

## §7 · Da dove si comincia, in una chat nuova

```bash
# la misura di partenza, rifatta adesso: se i numeri di §1 non tornano,
# qualcuno ha già lavorato e questo piano va riletto prima di eseguirlo
grep -l "from dmcore" scripts/*.py | wc -l        # atteso 10
grep -c "def slug" scripts/*.py | grep -v ':0'    # atteso 7 file
python3 -m pytest scripts/tests/test_gate_bocciano.py -q   # atteso 22 verdi

# la prova che il difetto del lotto A è reale, su dati veri
python3 -c "
import re, unicodedata
c = lambda s: re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')
a = lambda s: re.sub(r'[^a-z0-9]+','-', unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()).strip('-')
print(c('Lómyn RedTongue'), '≠', a('Lómyn RedTongue'))"
```

**L'ordine consigliato**: **0** (l'ADR, un'ora, sblocca la discussione sulle
librerie) → **A** (la `slug`, due ore più un commit di rigenerazione a parte) →
**C** e **D** se il DM li vuole.

**Aggiornamento 2026-09-03**: 0 e A sono chiusi, restano C e D. I comandi di
verifica qui sopra vanno letti con i valori nuovi: `def slug` = 1,
`from dmcore` = 16 su 46 (erano 10), e `test_testo.py` verde con 25 test.

⚠️ **Il lotto A cambia degli id nel catalogo.** Va in un commit suo, e i
riferimenti esistenti vanno guardati prima di rigenerare: `grep -rn "l-myn\|d-lite"`.

**Il metodo che ha funzionato nel lotto B, e che vale per gli altri**: scritto il
test, **mutare il codice che dovrebbe coprire** e verificare che il test cada.
Nel lotto B ha trovato un difetto nel test stesso, che rileggendolo non si vedeva.

---

## §8 · Lotto E — Una libreria per le creature *(aperto 2026-09-23)*

> **Nasce da** la domanda del DM del 2026-09-23: *«se i tre script usano le
> stesse funzioni, si possono unire in una libreria unica, lasciando nei tre
> script solo le funzioni diverse che chiamano la libreria comune? così è meglio
> o più facile da unire in `dm.py`?»*
> **Risposta breve**: è meglio, ed è la forma che `dmcore/` ha già per le tabelle
> e per il blocco statistiche. Non ripara un difetto che esista oggi, perché la
> classe di errori che l'ha fatta nascere la prende già il cancello di
> `extract_statblocks --check` (ADR-0033, emendamento del 2026-09-23). Serve
> perché la prossima correzione di un lettore si faccia in un posto e non in tre.
> Per `dm.py` cambia poco: `dm.py` chiama i suoi strumenti con `subprocess`, e un
> sottocomando `bestiario` costa una ventina di righe con o senza libreria.

### §8.1 · Cosa NON rifà, e con chi confina

| Confine | Di chi è | Cosa resta fuori da questo lotto |
|---|---|---|
| Come si genera un **mostro** dal GS | `PIANO-GENERATORE-CREATURE-E-PNG`, lotto B | il ramo mostri di `genera_creatura` costruisce dal bersaglio per GS, non dall'array, **per progetto**. Non si unifica |
| I lotti J (template PF1e) e K (incontro tarato sul gruppo) | `PIANO-GENERATORE-CREATURE-E-PNG` §9-10 | non si toccano. Se partono prima di questo lotto, lavorano sul codice di oggi e il lotto E li rilegge |
| Le regole della conformità | `RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI` e ADR-0065 | il lotto sposta codice, non cambia una regola. Un numero del verificatore che cambia è un difetto del lotto |
| Il cancello blocco/prosa | ADR-0033, emendamento 2026-09-23 | resta in `extract_statblocks` |
| `slug` e testo | lotto A di questo piano | già in `dmcore/testo.py` |

### §8.2 · La misura di partenza (presa il 2026-09-23 su `45306c8`, rimisurata dopo le decisioni D1-D12 della conformità), e dopo E8

| Cosa | Prima del lotto | Dopo E8 | Come si rimisura |
|---|---:|---|---|
| Righe dei quattro script | **3.503** | **2.431**, più **1.288** nei tre moduli di `dmcore`: **3.719** in tutto (+216) | `wc -l scripts/{derive_statblocks,genera_attributi,genera_creatura,conformita_statblocchi}.py` |
| Funzioni e classi di primo livello | GA 32 · C 33 · D 5 · GC 26 | GA 6 · C 24 · D 5 · GC 26; in `dmcore` progressione 5 · lettore 23 · scelta 14 | `grep -cE "^def \|^class " …` |
| Espressioni regolari di modulo | GA 25 · C 14 · D 4 · GC 0 | GA 2 · C 6 · D 4 · GC 0; in `dmcore` progressione 1 · lettore 26 · scelta 4 | `grep -cE "^[A-Z_]+ = re.compile" …` |
| Simboli che `conformita_statblocchi` importa da `genera_attributi` | **23** | **0** (E3b) | lo script di §8.7, passo 3 |
| Import circolare `genera_attributi` ↔ `conformita_statblocchi` | **1**, pigro dentro `tetti_dai_ts` | **0** (E3b), e E4 lo vieta con un test | `grep -n "import conformita_statblocchi" scripts/genera_attributi.py` |
| Implementazioni della base dei TS (buono 2 + L/2, cattivo L/3) | **4**: `derive_statblocks.deriva`, `genera_creatura._tiri_salvezza`, `conformita_statblocchi.ts_attesi` (riscrive la formula invece di usare `T.ts_buono`), `genera_attributi` (tramite il verificatore) | **1**: `dmcore.progressione.ts_base_di` e `ts_base`, su `T.ts_buono` e `T.ts_cattivo` | `grep -n "ts_buono\|ts_cattivo\|2 + .*// 2" scripts/*.py` |
| Lettori di classi e DV dal testo | **3**: `derive_statblocks.leggi_scheda`, `genera_attributi.dadi_vita`, `conformita_statblocchi.composizione` | **3 in 2 posti**: `dadi_vita` e `composizione` nel lettore di `dmcore`; `derive_statblocks.leggi_scheda` resta dov'è (ADR-0066, punto 6) | lettura dei tre |
| Tabelle «ruolo → ordine delle caratteristiche» | **2**: `genera_attributi.PROFILI` (33 chiavi), `genera_creatura.RUOLI[…].priorita` (6 ruoli). **Dei 6 ruoli, 2 coincidono** (bruto, comandante); schermagliatore, tiratore, blaster e controllore ordinano diverso | **1**: `PROFILI` (D2 = a); i sei ruoli di `genera_creatura` ne nominano un profilo (E6) | `python3 -c` di §8.7, passo 4 |
| Corpi di funzione identici in file diversi (§5) | **1** | **1**, lo stesso di prima (`col_label` delle mappe), fuori dal lotto | lo script di §5 |
| Script che usano `dmcore` | **28 su 63** | **29 su 64**: il sessantaquattresimo è `impronta_creature` (E0), che lo usa | `grep -l "from dmcore" scripts/*.py \| wc -l` |
| Test | **1165** verdi, 21 saltati | **1194** verdi, 21 saltati | `python3 -m pytest -q scripts/tests/` |
| Taratura dello strato scelto | **1,50** in campione · **1,51** fuori | **1,50** · **1,51**, invariata | `python3 scripts/genera_attributi.py --taratura` |
| Conformità | **102** tornano · 5 come la fonte · 0 decisioni · 0 da correggere · 0 scarti del generatore | invariata | `python3 scripts/conformita_statblocchi.py --riepilogo` |

🔎 **Il fatto che cambia il disegno.** Il verificatore **dipende già** dal lettore
del generatore: 23 simboli, fra cui `PF_DADO`, `dadi_vita`, `pf_dado_sospetto`,
`numeri_della_fonte`. L'indipendenza fra chi genera e chi verifica, che la
risposta al DM dava per un principio da difendere, oggi è parziale. Il lotto
la rende **esplicita e verificata** invece che sottintesa: si condividono le
regole e il lettore, non la **scelta** (vedi D1).

### §8.3 · Il disegno

Tre moduli nuovi in `scripts/dmcore/`, separati per **chi li può importare**:

| Modulo | Contiene | Chi lo importa |
|---|---|---|
| `dmcore/progressione.py` | base dei TS e del BAB per classe e tipo (`Gruppo`, `CLASSE_LIVELLO`, `_classe`, `ts_attesi` senza caratteristiche, `bab_atteso`), costruita su `dmcore.tabelle` | tutti |
| `dmcore/lettura_creatura.py` | il lettore: `BLOCCO`, `PF_DADO`, `PEZZO_DADO`, `DV_DICHIARATI`, `SESTINA`, `BAB_SCRITTO`, `LOTTA_*`, `INIZIATIVA_*`, `senza_note`, `taglia_di`, `dadi_vita`, `robustezza`, `pf_dado_sospetto`, `dalla_scheda`, `numeri_della_fonte`, `composizione`, `dv_totali`, `dadi_di_pf`, `talenti`, e (E1) `plausibile` e `tetti_dai_ts`, che il verificatore usa | tutti, verificatore compreso (D1 = sì) |
| `dmcore/caratteristiche.py` | la **scelta**: gli strati di `genera_attributi.genera` (scheda, fonte, vincoli, l'uso del tetto dei TS, iniziativa a due candidati, array per ruolo con taglia e razza), `PROFILI`, `PER_TAGLIA`, `RAZZE` | i generatori (`genera_attributi`, `derive_statblocks`, il ramo PNG di `genera_creatura`), **mai** `conformita_statblocchi` |

I quattro script restano dove sono e con la stessa interfaccia: CI,
`tools.manifest.json`, skill e test li chiamano per nome. Dentro restano la riga
di comando e ciò che è solo loro (`proponi`/`applica`/`--check` di
`genera_attributi`, `verifica`/`giudica` del verificatore, `deriva` e il collaudo
PF1e di `derive_statblocks`, il ramo mostri e gli incantesimi di
`genera_creatura`).

🔒 **La regola che tiene insieme il disegno** diventa un test (E4): nessun
modulo importato da `conformita_statblocchi` può importare
`dmcore.caratteristiche`. Se una stessa funzione sceglie e verifica, un errore
di regola compare da tutte e due le parti e si conferma da solo: è successo con
la Tabella 1–1, che skill e costante sbagliavano allo stesso modo e un test
confrontava fra loro.

📜 **La decisione va in un ADR**: il numero si prende con
`python3 scripts/validate_docs.py --prossimo-adr` al momento di scriverlo
(il 2026-09-23 il primo libero era ADR-0066).

### §8.4 · I sotto-lotti

L'ordine è fisso: ognuno lascia il repo verde e l'impronta di E0 **identica**,
e va in un commit suo.

#### ✅ E0 · L'impronta di partenza *(chiuso 2026-09-23)*
`[engine: Opus, sessione principale · effort: medio · qualità: due esecuzioni sullo stesso commit danno lo stesso file, byte per byte]`
**Classe C.** Uno script `scripts/impronta_creature.py` (sola lettura, stdlib)
che scrive in JSON, ordinato e deterministico:
- per ogni statblocco del Bestiario: `genera_attributi.genera(…)` (valori e
  note), `conformita_statblocchi.giudica(…)`, l'esito di
  `extract_statblocks.controlla(…)`;
- per ogni scheda senza blocco: `derive_statblocks.deriva(leggi_scheda(…))`
  (blocco, conti, mancanti);
- per `genera_creatura.genera`: la griglia GS 1-20 × i 6 ruoli × tipo
  umanoide/mostro × `--piu-cattivi` sì/no, a seme fisso;
- `--taratura` di `genera_attributi` e `--riepilogo` del verificatore.

L'impronta si committa in `scripts/tests/fixtures/impronta-creature.json`, e un
test (`test_impronta_creature.py`) la rigenera e la confronta. **È il collaudo
di tutto il lotto**: un sotto-lotto che la cambia ha cambiato un comportamento, e
si ferma lì.
**Accettazione**: test verde; e la prova che morde, cioè una mutazione di una
riga in `tetti_dai_ts` fa cadere il test.

✅ **Fatto** (`scripts/impronta_creature.py`, fixture da 1,7 MB, 4 test).
Due esecuzioni danno lo stesso file byte per byte, in 2,6 secondi. Dentro:
108 statblocchi con **17 letture intermedie** ciascuno (dadi vita, `pf-dado`
sospetto con e senza GS, sestina della scheda e della fonte, numeri della
fonte, tetti dei TS, composizione, talenti, provenienza, e i vincoli su Des, Cos e For),
`genera` con e senza fonte, `giudica`, `pf_dado_corretto` normale e forzato;
95 derivazioni; 720 creature (GS 1-20 × 6 ruoli × mostro umanoide, PNG con
classe, bestia magica Grande × `--piu-cattivi`); taratura, riepilogo, i due
`--check` e la proposta di `--correggi-pf-dado`.
Due mutazioni provate, e cadono tutte e due sulla chiave che le nomina:
`+ 1` in `tetti_dai_ts` (354 chiavi su 85 schede, a partire da
`bruto-deforme-sottosuolo-cr11.md/letture/tetti_dai_ts/Cos`) e il flag `re.M`
tolto a `INIZIATIVA_SCRITTA` (a partire da `blue-psion-cr1.md/letture/iniziativa_ambigua`).
🔎 **Una cosa che il piano non sapeva**: nessuna scheda del Bestiario è oggi
scrivibile da `derive_statblocks --apply-ts` (le due proposte sono rimandi),
quindi `con_attributi`, la metà di `derive_statblocks` che chiama
`genera_attributi`, sul Bestiario non gira mai. L'impronta la fa girare su tre
schede di prova in una cartella temporanea (chiave `apply_ts`).

#### ✅ E1 · L'ADR e i moduli vuoti *(chiuso 2026-09-23)*
`[engine: Opus, sessione principale · effort: alto · qualità: il DM riconosce la decisione, e D1 è risposta]`
**Classe G.** L'ADR con il disegno di §8.3, i tre moduli con la sola docstring
e un `__all__` vuoto. Si scrive **dopo** la risposta a D1.
**Accettazione**: `validate_docs --sorgenti` verde; l'ADR indicizzato in
`docs/INDEX.md` §4.

✅ **Fatto**: [ADR-0066](adr/ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md),
D1 chiusa (**sì**), e `dmcore/progressione.py`, `dmcore/lettura_creatura.py`,
`dmcore/caratteristiche.py` con la sola docstring.
🔎 **Il disegno di §8.3 cambia in due punti, e l'ADR li dichiara.** Fra i 23
simboli che il verificatore prende dal generatore ci sono `tetti_dai_ts` e
`plausibile`, che §8.3 metteva nella scelta: `pf_dado_corretto` li usa per
ricostruire il bonus di `pf-dado`, e dalla scelta il verificatore non può
importare. Nessuno dei due sceglie (il primo ricava un limite da un TS scritto,
il secondo rifiuta un modificatore ricavato che il GS non regge), quindi vanno
nel lettore. Per la stessa ragione **E3a non sposta tutti e 23 i simboli**:
`tetti_dai_ts` usa `composizione`, `Scheda` e `talenti` del verificatore, e si
sposta con loro in E3b. *(Corretto in E3a: E1 diceva «22»; erano 21, perché
`ABBREVIAZIONI` era già passato in E2 con la progressione.)*

#### ✅ E2 · La progressione in un posto *(chiuso 2026-09-23)*
`[engine: Sonnet 5 o Opus · effort: alto · qualità: impronta identica, e un solo posto nel repo calcola la base dei TS]`
**Classe C.** Spostare in `dmcore/progressione.py` `Gruppo`, `CLASSE_LIVELLO`,
`_classe`, `_PRESTIGIO`, la base dei TS e `bab_atteso`. Le quattro copie della
base (§8.2) chiamano la funzione nuova. I nomi vecchi restano importabili dagli
script (`from dmcore.progressione import ts_base as _ts_base`, e il vecchio nome
come alias) finché E8 non li toglie.
**Accettazione**: impronta identica; `grep -n "2 + .*// 2" scripts/*.py`
vuoto; test nuovo `test_progressione.py` con i casi che il verificatore già
conosce (umanoide a TS variabile, paladino con Grazia divina, classi di
prestigio SRD) e una mutazione che lo fa cadere.

✅ **Fatto**: `dmcore/progressione.py` (`Gruppo`, `ABBREVIAZIONI`, `PRESTIGIO`,
`DADO_DI_CLASSE`, `CLASSE_LIVELLO`, `classe`, `ts_base_di`, `ts_base`,
`bab_atteso`). Le quattro copie della base chiamano `ts_base_di` o `ts_base`;
la formula riscritta nel verificatore è sparita e il `grep` è vuoto. Impronta
identica. `test_progressione.py`: 10 test, **3/3 mutazioni** (la fascia
dell'umanoide, il BAB arrotondato una volta sola sul totale, il BAB
dell'assassino). La seconda la prendeva l'impronta e non il test, al primo
giro: l'esempio del test dava lo stesso numero con i due arrotondamenti.
🐛 **Un falso verde del metodo, trovato provando le mutazioni**: mutazione e
ripristino della stessa lunghezza, nello stesso secondo, lasciano in
`__pycache__` il bytecode della mutazione, perché Python confronta solo data e
dimensione del sorgente. Il test ripristinato risultava rosso con il codice giusto;
con la mutazione al contrario sarebbe risultato verde con il codice sbagliato. Le
mutazioni del lotto si provano con `PYTHONDONTWRITEBYTECODE=1` e la cache
svuotata dopo il ripristino.

#### ✅ E3 · Il lettore in un posto *(chiuso 2026-09-23)*
`[engine: Opus, sessione principale · effort: alto · qualità: impronta identica, e il verificatore non importa più niente da genera_attributi]`
**Classe C, con rischio alto**: è la parte più grande (una trentina di simboli)
e quella dove una virgola sposta un numero. Spostare in
`dmcore/lettura_creatura.py` i simboli di §8.3. **In due commit**:
- **E3a**: i simboli di `genera_attributi` che il verificatore usa (i 23 di §8.2);
- **E3b**: `composizione`, `dv_totali`, `dadi_di_pf`, `talenti`, `leggi`/`Scheda`
  del verificatore.

⚠️ `derive_statblocks.leggi_scheda` **non** entra: legge schede in prosa per
derivare, con la sua struttura `Lettura`, e unificarlo cambierebbe le proposte
su 60 schede. Resta dov'è, e lo si dichiara nell'ADR.
**Accettazione**: impronta identica; `grep -n "import genera_attributi"
scripts/conformita_statblocchi.py` vuoto; `test_conformita_statblocchi.py`,
`test_genera_attributi.py` e `test_statblock.py` verdi senza modifiche alle
asserzioni (cambiano solo gli import).

✅ **E3a fatto**: 43 simboli di primo livello di `genera_attributi` in
`dmcore/lettura_creatura.py` (i 21 che il verificatore usava, più le loro
dipendenze: `ORDINE`, `TAGLIA`, `CLASSE_NEL_TIPO`, `FORMULA_DV`, `SESTINA` con le sue
parti, `sestine_citate`, `dalla_scheda`, le marche). Tagliati dal sorgente con
`ast` e non ricopiati: **l'albero sintattico di ognuno dei 43 è identico** a
quello di prima, flag delle regex compresi. `genera_attributi` li reimporta
tutti (36 nomi pubblici) come alias fino a E8. Il verificatore legge con
`L.` e dal generatore prende ancora un solo nome, `tetti_dai_ts`.
Impronta identica; i test di §8.4 verdi senza toccare un'asserzione.

✅ **E3b fatto**: 19 simboli del verificatore (`Scheda`, `leggi`,
`composizione`, `dv_totali`, `dadi_di_pf`, `talenti`, `provenienza`, le loro
regex, il non morto PF1e) e i 3 del tetto dei TS di `genera_attributi`
(`TS_CARATTERISTICA`, `TS_SCRITTI`, `tetti_dai_ts`) nel lettore, che ora ha
57 nomi pubblici. Gli alberi dei 19 sono identici a quelli di prima **tranne
tre rinomine** fatte apposta: il prefisso `L.` che dentro il modulo non serve
più, e `BAB`/`LOTTA`, che erano alias del verificatore, diventano
`BAB_SCRITTO`/`LOTTA_SCRITTA`. `tetti_dai_ts` è l'unica funzione riscritta: chiamava
`ts_attesi(s, {})` del verificatore per avere la base più i talenti, e adesso
somma `progressione.ts_base` e `talenti` direttamente. Impronta identica, e
l'impronta registra i tetti di ogni scheda.
**Il ciclo fra i due script non c'è più**: `conformita_statblocchi` non
importa `genera_attributi` e `genera_attributi` non importa il verificatore,
nemmeno dentro una funzione. Il piano metteva questa scomparsa in E4; è
arrivata con E3b, e E4 la rende un test.

#### ✅ E4 · Il grafo degli import *(chiuso 2026-09-23)*
`[engine: Sonnet 5 · effort: medio · qualità: il test morde su un import proibito aggiunto a mano]`
**Classe C.** Un test (`test_grafo_import_creature.py`) che legge gli import con
`ast` e verifica:
- nessun ciclo fra i quattro script e i tre moduli nuovi (l'import pigro in
  `tetti_dai_ts` sparisce qui);
- `conformita_statblocchi` e ogni modulo che importa non arrivano mai a
  `dmcore.caratteristiche`, nemmeno indirettamente.

**Accettazione**: verde; e rosso aggiungendo a mano
`import dmcore.caratteristiche` in `conformita_statblocchi.py`.

✅ **Fatto**: `test_grafo_import_creature.py`, 9 test, stdlib. Legge gli import
di tutti gli script e di tutto `dmcore` con `ast.walk`, quindi anche quelli
dentro una funzione, e verifica: nessun ciclo che passi per i sette nodi del
lotto; nessun percorso dal verificatore a `dmcore.caratteristiche`; nessun
modulo raggiunto dal verificatore che ci arrivi; la libreria non importa
script; il verificatore non raggiunge il generatore. **Morde** tre volte:
l'import aggiunto a mano nel verificatore (rosso, e il messaggio dice il
percorso), lo stesso import messo **dentro una funzione** del lettore (3 test
rossi), e il grafo di E2 ricostruito da `git show`, dove trova il vecchio ciclo
`genera_attributi → conformita_statblocchi → genera_attributi`.

#### ✅ E5 · La scelta delle caratteristiche in un posto *(chiuso 2026-09-23)*
`[engine: Opus, sessione principale · effort: alto · qualità: impronta identica, taratura 1,50 / 1,51 invariata]`
**Classe C.** Spostare in `dmcore/caratteristiche.py` gli strati di
`genera_attributi.genera` e le loro tabelle (`PROFILI`, `PER_TAGLIA`, `RAZZE`,
`ELITE`), `_dall_array`, `tetti_dai_ts`, `iniziativa_ambigua`, `des_vincolata`,
`des_da_iniziativa`, `cos_da_pf`, `for_da_lotta`, `dalla_fonte`.
`genera_attributi` tiene `proponi`, `applica`, `controlla`, `taratura` e la riga
di comando; `derive_statblocks.con_attributi` chiama `dmcore.caratteristiche`
direttamente.
**Accettazione**: impronta identica; `genera_attributi --check` e
`--taratura` invariati; E4 verde.

✅ **Fatto**: 24 simboli in `dmcore/caratteristiche.py` (gli array, `PROFILI`,
`PER_TAGLIA`, `RAZZE`, i vincoli, `dalla_fonte`, `_dall_array`, `genera`,
`riga_attributi`), tagliati con `ast` e con **alberi identici** a quelli di
prima. `genera_attributi` tiene `statblocchi`, `proponi`, `applica`,
`controlla`, `taratura` e la riga di comando, e scende da 1.170 a 352 righe.
`derive_statblocks.con_attributi` chiama `dmcore.caratteristiche` e
`dmcore.lettura_creatura`, e non importa più né il generatore né il
verificatore. Impronta identica, `--check` 93 blocchi, taratura 1,5 / 1,51,
E4 verde e di nuovo rosso con un import della scelta aggiunto al verificatore.

📏 **Il conto delle righe, onesto.** I quattro script passano da **3.503 a
2.465**; i tre moduli nuovi ne hanno **1.241**, e il totale sale a **3.706
(+203)**. La differenza sono docstring dei moduli e import degli alias, che E8
toglie. Il lotto non promette meno righe: promette una lettura e una scelta
in un posto solo.

#### ✅ E6 · Una tabella dei ruoli *(chiuso 2026-09-23, D2 = a)*
`[engine: Opus, sessione principale · effort: xhigh · qualità: il DM ha visto il diff dei blocchi prima del commit]`
**Classe K se D2 cambia l'ordine di una delle due tabelle**, perché cambia gli
`attributi` di blocchi del Bestiario. Si attua la risposta a D2 e:
- se cambia `PROFILI`: `genera_attributi --rigenera` in un commit suo, e il
  diff dei blocchi va al DM **prima** del commit (come il lotto A di L7);
- se cambia `genera_creatura`: l'impronta di E0 cambia sulla griglia dei PNG, e
  la si rigenera in un commit suo, che dice quali celle e perché.

**Accettazione**: una tabella sola; `conformita --riepilogo` senza scarti nuovi;
impronta rigenerata e motivata nel commit.

✅ **Fatto, con D2 = (a)**: vince `genera_attributi`. `Ruolo.priorita` non è più
un campo scritto a mano: ogni ruolo di `genera_creatura` nomina il suo profilo
(bruto → `brute`, schermagliatore → `skirmisher`, tiratore → `ranged`,
comandante → `commander`, controllore → `arcane`, blaster → `blaster`, la stessa
corrispondenza della misura di §8.2) e l'ordine si legge da `PROFILI` per chiave
esatta, non per sottostringa. `genera_creatura` importa `dmcore.caratteristiche`
per la tabella; il resto del ramo PNG ci passa in E7.

L'impronta cambia in **160 celle su 720**: tutte e sole quelle della forma `png`
dei quattro ruoli che divergevano, 20 GS con e senza `--piu-cattivi`. Le sezioni
`bestiario`, `derivazioni`, `apply_ts` e `gate` restano identiche, quindi nessun
blocco del Bestiario cambia e `--riepilogo` non ha scarti nuovi. Il verdetto del
collaudo PNG non cambia in nessuna cella. Con la matrice élite, prima
dell'aumento ogni 4 livelli, al tavolo cambia questo:

| Ruolo | Prima | Dopo | Cosa cambia nel blocco |
|---|---|---|---|
| schermagliatore | Des 15 For 14 Cos 13 Sag 12 Car 10 Int 8 | Des 15 For 14 Cos 13 Sag 12 Int 10 Car 8 | solo la riga delle caratteristiche |
| controllore (mago) | Int 15 Des 14 Cos 13 Sag 12 Car 10 For 8 | Int 15 Des 14 Cos 13 Car 12 Sag 10 For 8 | Volontà −1 |
| tiratore | Des 15 Cos 14 Sag 13 For 12 Car 10 Int 8 | Des 15 For 14 Cos 13 Sag 12 Int 10 Car 8 | **−1 pf per livello**, Tempra −1 |
| blaster (mago) | Int 15 Cos 14 Des 13 Sag 12 Car 10 For 8 | Int 15 Des 14 Cos 13 Car 12 Sag 10 For 8 | **−1 pf per livello**, Tempra −1, Volontà −1; CA, iniziativa e Riflessi +1 |

⚠️ Il costo vero è sui pf: un blaster mago di 9° passa da 40 a 31, un tiratore di
5° da 37 a 32. Il collaudo li dava già per PNG che «non reggono un incontro da
soli», e continua a darli così. La Forza in più del tiratore non entra in nessun
numero, perché tira con l'arco.

La fixture è rigenerata nel commit successivo a quello del codice, da sola.

#### ✅ E7 · Il ramo PNG di `genera_creatura` sulla libreria *(chiuso 2026-09-23)*
`[engine: Sonnet 5 · effort: alto · qualità: impronta identica sulla griglia dei mostri; sui PNG identica o motivata da E6]`
**Classe C.** Il ramo `_genera_png` usa l'array e la tabella dei ruoli di
`dmcore.caratteristiche`; il ramo mostri (dal bersaglio per GS) non si tocca
(§8.1). Incantesimi, carattere e collaudo restano in `genera_creatura`.
**Accettazione**: `test_genera_creatura.py` verde; impronta come detto.

✅ **Fatto**: la scelta del PNG sta in `dmcore.caratteristiche.matrice_png`
(matrice élite o standard nell'ordine del profilo, la caratteristica da
incantatore davanti, +1 ogni 4 livelli sulla prima), con i due commenti sui
difetti che l'avevano fatta così. `profilo_esatto` cerca un profilo per nome e
solleva `KeyError` invece di ripiegare sul bruto come `profilo_di`, che legge
una frase. `_genera_png` tiene solo il conto che racconta la scelta, e
`Ruolo.priorita` sparisce. `matrice_png` non sostituisce `_dall_array`, e la
docstring dice perché: quella ricostruisce una scheda che esiste, con il GS
come surrogato dei livelli, la razza e un ±1 sul nome del file.
Impronta identica su tutte le 720 celle. Sei test nuovi in
`test_genera_creatura.py` (`UnaTabellaDeiRuoli`), e cinque mutazioni su cinque
li fanno rossi: il tiratore su un altro profilo, la precedenza
dell'incantatore tolta, `profilo_esatto` che ripiega, un aumento ogni 5 livelli,
le caratteristiche in ordine alfabetico. `genera_creatura` 1.014 → 1.013 righe,
`caratteristiche` 494 → 541.

#### ✅ E8 · Gli alias se ne vanno, e il conto finale *(chiuso 2026-09-23)*
`[engine: Sonnet 5 · effort: medio · qualità: i numeri di §8.2 rimisurati, e nessun chiamante dei nomi vecchi]`
**Classe M.** Togliere gli alias lasciati da E2-E5 dove nessuno li chiama più
(test compresi, che passano ai nomi nuovi). Rimisurare §8.2 e scrivere i numeri
nuovi accanto ai vecchi.
**Accettazione**: tutti i gate di §8.5 verdi; `grep` dei nomi vecchi vuoto fuori
da `dmcore`.

✅ **Fatto**: `genera_attributi` importa da `dmcore` solo gli 11 nomi che usa
(erano 66, più `PRESTIGIO` rifatto a dizionario) e scende da 352 a 334 righe;
`conformita_statblocchi` ne tiene 6 più i moduli `L`, `P` e `T` (erano 32, con
`BAB`, `LOTTA`, `_classe`, `_NOMI`, `_PRESTIGIO` rinominati) e scende da 643 a
628. Dove il verificatore usava un alias rinominato ora scrive `L.LOTTA_TAGLIA`,
`L.LOTTA_MIGLIORATA`, `L.numeri_della_fonte`. I chiamanti esterni passano ai
moduli: 103 punti in sei file (`impronta_creature`, quattro test,
`validate_bestiario`, che ora prende `pf_dado_sospetto` dal lettore e non carica
più tutto il generatore).
**La verifica** non è un `grep`, che non distingue `GA.genera` da un
`genera` qualsiasi: `ast` legge ogni `modulo.attributo` dei quattro script in
tutto `scripts/`, e ogni nome che uno script riceve da `dmcore` ha **zero**
chiamanti esterni; un secondo giro controlla che nessun attributo letto manchi
dal modulo (zero). Il primo giro ne aveva perso uno, `C.LOTTA_MIGLIORATA`,
perché era un'assegnazione e non un import: l'ha trovato il test.
⚠️ **Restano nove nomi che uno script riprende da `dmcore` e altri leggono
passando per lo script**, e restano di proposito: `derive_statblocks` prende
sette nomi da `dmcore.tabelle` ed `estrai` da `dmcore.statblock` da prima del
lotto E, e `test_tabelle` verifica con `assertIs` che il derivatore usi proprio
quelle tabelle e non una copia; `genera_creatura.rendi` lo chiama
`suggest_encounter`. Nessuno dei nove viene da E2-E5. I numeri nuovi di §8.2 stanno accanto ai vecchi, nella colonna «Dopo E8».

#### ⬜ E9 · `dm.py bestiario` *(bloccato su D3)*
`[engine: Sonnet 5 · effort: medio · qualità: dm.py bestiario <azione> --help esce 0 e dà lo stesso output dello script]`
**Classe C.** Un sottocomando `dm.py bestiario {estrai,deriva,attributi,creatura,conformita}`
che passa gli argomenti allo script (come fanno già `prep` e `maps`, con
`subprocess` e `parse_known_args`). Gli script restano: la CI e il manifest li
chiamano per nome. Si aggiornano `scripts/README-automation.md`, la skill
`rumblingstone-automation` (poi `./scripts/build-skills.sh --no-deploy` e
`validate_skills.py`) e `tools.manifest.json` se il sottocomando ci va.
**Accettazione**: un test che per ogni azione confronta `dm.py bestiario X --help`
con `scripts/X.py --help`; `dm.py doctor --ci` verde.

### §8.5 · Il collaudo, dopo ogni sotto-lotto

Non si passa al sotto-lotto successivo finché tutti questi non sono verdi:

```bash
python3 -m pytest -q scripts/tests/                     # ≥ 1194 verdi (1165 prima del lotto)
python3 -m pytest -q scripts/tests/test_impronta_creature.py   # impronta di E0 identica
python3 scripts/impronta_creature.py --confronta        # la stessa, e dice dove diverge
python3 scripts/extract_statblocks.py --check           # 0 problemi
python3 scripts/validate_bestiario.py                   # catalogo in sync
python3 scripts/validate_bestiario.py --rules           # 5 avvisi, gli stessi
python3 scripts/genera_attributi.py --check             # 93 blocchi riproducibili
python3 scripts/genera_attributi.py --taratura          # 1,50 / 1,51
python3 scripts/conformita_statblocchi.py --check
python3 scripts/conformita_statblocchi.py --riepilogo   # 102 · 5 · 0 · 0 · 0
python3 scripts/derive_statblocks.py                    # 2 proposte, 92 ferme
python3 scripts/genera_creatura.py --gs 7 --ruolo bruto # stesso output di E0
python3 scripts/decisioni_dm.py --check
python3 scripts/validate_docs.py --sorgenti
python3 scripts/check_plans_discipline.py --base origin/main
python3 scripts/dm.py doctor --ci
```

E tre regole di metodo, già provate in questo piano:
- **scritto un test, si muta il codice che copre** e si verifica che cada (§7);
- **un sotto-lotto per commit**, con la riga di CHANGELOG nello stesso commit
  (regola d'oro, ADR-0009);
- **l'impronta non si rigenera mai per far passare un test**: si rigenera solo
  in E6, in un commit suo, con il motivo scritto.

### §8.6 · Le decisioni del DM

<!-- decisioni-dm: QUALITA-CODICE -->

| # | Ambito | Domanda |
|---|---|---|
| ~~D1~~ | E1 · E3 | ✅ **decisa dal DM il 2026-09-23: sì**, il verificatore condivide il lettore ([ADR-0066](adr/ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md)). **Il verificatore condivide il lettore?** Oggi lo fa già: importa 23 simboli da `genera_attributi`. **Sì** (consigliato): il lettore va in `dmcore/lettura_creatura.py` e lo usano tutti; l'indipendenza sta nelle regole e nella scelta, che il verificatore non importa mai (E4 lo prova). **No**: il verificatore tiene un lettore suo, copiato, più sicuro contro un errore di lettura condiviso e con una seconda copia da tenere allineata a mano |
| ~~D2~~ | E6 | ✅ **decisa dal DM il 2026-09-23: (a)**, vince `genera_attributi`; attuata in E6. **Quale tabella dei ruoli vince?** Dei 6 ruoli di `genera_creatura`, 4 ordinano le caratteristiche diversamente dal profilo corrispondente di `genera_attributi` (schermagliatore, tiratore, blaster, controllore). **(a)** vince `genera_attributi`: cambiano i PNG che `genera_creatura` genera d'ora in poi, nessun blocco del Bestiario; **(b)** vince `genera_creatura`: cambiano gli `attributi` di alcuni dei 15 blocchi scelti dall'array, che il DM vede prima; **(c)** si tengono separate e si dichiara perché |
| D3 | E9 | **`dm.py bestiario` si fa in questo lotto o dopo?** Costa poco e non dipende dalla libreria; farlo prima di E8 vuol dire toccare `dm.py` due volte se un'interfaccia cambia |

### §8.7 · Da dove si comincia, in una chat nuova

🔁 **Dopo la seconda PR del lotto (E6-E8) si riparte da qui.** Il blocco che
stava qui dopo la PR #158 e la misura più sotto sono di prima, e non tornano più
di proposito:

```bash
git fetch origin main && git log --oneline -1 origin/main                   # la PR di E6-E8 mergiata
wc -l scripts/{derive_statblocks,genera_attributi,genera_creatura,conformita_statblocchi}.py   # 2431
wc -l scripts/dmcore/{progressione,lettura_creatura,caratteristiche}.py      # 113 · 634 · 541
python3 scripts/impronta_creature.py --confronta                            # identica (rigenerata in E6)
python3 -m pytest -q scripts/tests/ | tail -1                               # 1194 passed
python3 scripts/decisioni_dm.py --check                                     # D3 di QUALITA-CODICE aperta
```

Resta **E9**, bloccato su **D3**: il DM ha scelto di lasciarla aperta, e la
seconda PR non l'ha toccata. Gli alias sono spariti in E8, quindi un
`dm.py bestiario` fatto adesso passa argomenti a script con l'interfaccia
definitiva e non tocca `dm.py` due volte, che era il rischio scritto in D3.
⚠️ Le mutazioni si provano con `PYTHONDONTWRITEBYTECODE=1` e la cache svuotata
dopo il ripristino (E2).

**Prima di tutto la misura.** Se un numero non torna con §8.2, qualcuno ha già
lavorato: si rilegge questo piano prima di eseguirlo.

```bash
git fetch origin main && git log --oneline -1 origin/main
python3 scripts/fase1.py scripts/genera_attributi.py scripts/conformita_statblocchi.py \
    scripts/derive_statblocks.py scripts/genera_creatura.py      # regola G6, sola lettura
wc -l scripts/{derive_statblocks,genera_attributi,genera_creatura,conformita_statblocchi}.py   # 3503
grep -n "import conformita_statblocchi" scripts/genera_attributi.py                            # 1 riga
python3 -m pytest -q scripts/tests/ | tail -1                                                  # 1165 passed
python3 scripts/conformita_statblocchi.py --riepilogo                                          # 102 · 5 · 0 · 0 · 0
python3 scripts/genera_attributi.py --taratura | grep "errore medio"                           # 1.5 · 1.51
python3 scripts/decisioni_dm.py --check                                                        # D1-D3 di QUALITA-CODICE aperte
```

Il passo 3 e il passo 4 di §8.2, se servono di nuovo:

```bash
# 3 · i simboli che il verificatore prende dal generatore
python3 - <<'PY'
import re; t = open("scripts/conformita_statblocchi.py").read()
print(len(sorted(set(re.findall(r"\bGA\.(\w+)", t)))))
PY
# 4 · la tabella dei ruoli: dopo E6 e' una, e ogni ruolo di genera_creatura ne
#     nomina un profilo (prima di E6 i ruoli avevano un ordine loro, e su 6
#     ne coincidevano 2)
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
import genera_creatura as GC
from dmcore import caratteristiche as CAR
for k, r in GC.RUOLI.items():
    print(f"{k:16} {r.profilo:11} {CAR.profilo_esatto(r.profilo)}")
PY
```

**Le skill da aprire** (ORCHESTRAZIONE, cinque domande): `rumblingstone-debugging`
per il codice, `rumblingstone-plans` per la tracciatura,
`rumblingstone-prosa-documenti` per l'ADR e i commit. `dnd-35-srd` solo se un
numero del verificatore cambia e bisogna capire quale regola ha toccato.

**L'ordine**: rispondere a **D1** → **E0** → **E1** → **E2** → **E3a** → **E3b**
→ **E4** → **E5** → (**D2** → **E6**) → **E7** → **E8** → (**D3** → **E9**).
E0-E5 non dipendono dal DM oltre D1, e sono la parte che rende possibile il
resto.

**L'effort, sotto-lotto per sotto-lotto**: alto per E1-E3 ed E5, dove si sposta
codice che decide numeri; xhigh per E6 se tocca il canone; medio per E0, E4, E8
ed E9. **Una PR per il gruppo E0-E5**, una per E6-E9: la prima si rivede come
spostamento puro (impronta identica), la seconda cambia comportamenti.

⚠️ **Il rischio vero è E3.** È dove un'espressione regolare spostata perde un
flag (`re.M`, `re.I`) e un numero cambia su tre schede su cento. L'impronta di E0
esiste per quello: senza, un errore di lettura su una scheda passerebbe come un
refactor riuscito.
