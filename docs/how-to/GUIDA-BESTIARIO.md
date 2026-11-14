# Guida completa — aggiungere un mostro, un PNG o un villain

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

> **Cosa copre**: dove va il file, come si chiama, che formato deve avere,
> come si dichiara cosa è canone e cosa no, come si rigenera il catalogo,
> come far passare il gate della CI, e **quando conviene potenziare un
> mostro esistente invece di crearne uno nuovo**.
>
> **Regola d'oro della libreria**: una creatura si scrive **una volta sola**.
> Se ti serve un nemico simile a uno che esiste già, **non rigenerarlo**:
> parti da quello e potenzialo (§8).

---

## 0. TL;DR — il ciclo completo

```bash
# 0. serve davvero una scheda nuova? (§8, §6-ter)
#    c'è già qualcosa di simile   → potenzialo, non duplicarlo
#    non c'è niente e serve ora   → python3 scripts/genera_creatura.py --gs N

# 1. crea il file nella cartella giusta col nome giusto (RIFERIMENTO-BESTIARIO §1, §2)
#    Bestiario/mostri/nome-crN.md   ·   Bestiario/villain/<Nome>/nome-crN.md

# 2. scrivi lo statblock nel formato standard (RIFERIMENTO-BESTIARIO §3)

# 3. RIGENERA IL CATALOGO — obbligatorio, altrimenti la CI diventa rossa
python3 scripts/build_monster_catalog.py

# 4. verifica prima di committare
python3 scripts/validate_bestiario.py
python3 scripts/validate_bestiario.py --rules   # avvisi non bloccanti (GS, policy)
```

---

## 1. Dove va cosa

→ Ora in [RIFERIMENTO-BESTIARIO §1](../reference/RIFERIMENTO-BESTIARIO.md#1-dove-va-cosa), che è un riferimento.

---

## 2. Come si chiama il file

→ Ora in [RIFERIMENTO-BESTIARIO §2](../reference/RIFERIMENTO-BESTIARIO.md#2-come-si-chiama-il-file), che è un riferimento.

---

## 3. Il formato dello statblock (obbligatorio)

→ Ora in [RIFERIMENTO-BESTIARIO §3](../reference/RIFERIMENTO-BESTIARIO.md#3-il-formato-dello-statblock-obbligatorio), che è un riferimento.

---

## 4. I dossier (solo `villain/` e `png/`)

→ Ora in [RIFERIMENTO-BESTIARIO §4](../reference/RIFERIMENTO-BESTIARIO.md#4-i-dossier-solo-villain-e-png), che è un riferimento.

---

## 5. Rigenerare il catalogo (passaggio che tutti dimenticano)

`scripts/monster_catalog.yaml` è l'indice di tutta la libreria, usato da
`suggest_encounter` e dagli agenti. **Va rigenerato ogni volta che tocchi
uno statblock**:

```bash
python3 scripts/build_monster_catalog.py            # rigenera
python3 scripts/build_monster_catalog.py --check    # dry-run: dice solo se è disallineato
```

Se lo dimentichi, `validate_bestiario` fallisce in CI con «catalogo non in
sync». Serve davvero: senza rigenerare, il tuo mostro **non esiste**
per gli strumenti di preparazione.

---

## 6. Validare prima di committare

```bash
python3 scripts/validate_bestiario.py          # GATE: errori bloccanti
python3 scripts/validate_bestiario.py --rules  # avvisi (GS vs benchmark, policy flag)
python3 scripts/validate_bestiario.py --json   # report JSON, se ti serve automatizzare
```

Cosa controlla il gate:

1. la **struttura standard** esiste e le vecchie cartelle legacy no;
2. ogni statblock rispetta **naming, header obbligatori, coerenza CR** e ha
   uno **stato dichiarato**;
3. ogni dossier ha un **titolo H1**;
4. `mostri/` contiene **solo** statblock;
5. il **catalogo è in sync**.

`--rules` non blocca: segnala scostamenti dai benchmark di GS e dalle policy
dei flag, utile per capire se il CR che hai messo è realistico.

---

## 6-bis. Il blocco `statblocco` a macchina, e i tre strumenti che lo riempiono

→ Ora in [RIFERIMENTO-BESTIARIO §6-bis](../reference/RIFERIMENTO-BESTIARIO.md#6-bis-il-blocco-statblocco-a-macchina-e-i-tre-strumenti-che-lo-riempiono), che è un riferimento.

---

## 6-ter. Costruire una creatura che non c'è

`suggest_encounter` **pesca** dal catalogo. Quando serve qualcosa che nel
catalogo non c'è, `genera_creatura` la **costruisce** dalle tabelle
([ADR-0034](../../plans/adr/ADR-0034-generare-dalle-tabelle.md)).

```bash
# un bruto di GS 7, umanoide, taglia media
python3 scripts/genera_creatura.py --gs 7 --tipo umanoide --ruolo bruto

# lo stesso, ma più cattivo di quanto il GS prometta
python3 scripts/genera_creatura.py --gs 7 --ruolo bruto --piu-cattivi

# un PNG con livelli di classe: gli incantesimi vengono dalle tabelle SRD
python3 scripts/genera_creatura.py --gs 9 --ruolo blaster --classe mago:9

# il ruolo dice COME combatte, la funzione COSA fa con gli incantesimi:
# un chierico da guerra è ruolo «bruto» e funzione «supporto»
python3 scripts/genera_creatura.py --gs 9 --ruolo bruto --classe chierico:9 \
    --funzione supporto

# tre proposte riproducibili, in una cartella di lavoro
python3 scripts/genera_creatura.py --gs 5 --quanti 3 --seed 42 --in /tmp/bozze
```

**I sei ruoli** (bruto, schermagliatore, tiratore, comandante, controllore,
blaster) non decidono solo i numeri: ognuno porta un **talento firma**, una
**tattica in una riga** e una **debolezza sfruttabile**. Quest'ultima è la parte
che conta: senza, esce un mostro intercambiabile, e un mostro intercambiabile te
lo scrivi prima da solo che a leggerlo.

#### Gli incantatori: due assi, non uno

⚠️ Il ruolo tattico e la **funzione da incantatore** sono due cose diverse, e
confonderle era un difetto vero del tool fino al lotto I: le liste erano indicate
per ruolo, e un druido costruito come «controllore» riceveva *armatura magica*,
*sonno* e *dito della morte* — che sono da mago. Due schede del Bestiario ci sono
passate.

| Asse | Valori | Cosa decide |
|---|---|---|
| `--ruolo` | bruto · schermagliatore · tiratore · comandante · controllore · blaster | come combatte: caratteristiche, arma, CA, punti ferita |
| `--funzione` | controllore · blaster · supporto · utilità | quali incantesimi sceglie |

La chiave delle liste è la **lista di classe**, non la tradizione: chierico e
druido sono tutti e due divini e hanno liste diverse, e il bardo ha la sua. Sono
21 celle su sette classi (mago, stregone, chierico, druido, bardo, ranger,
paladino); mago e stregone condividono la lista perché nel SRD **è la stessa**.
Se chiedi una cella che nel gioco non esiste — un mago «supporto» — ripiega su
un'altra funzione **della stessa classe**, mai sulla lista di un'altra, e te lo
scrive nel conto.

Se ometti `--funzione`, si deduce dal ruolo (comandante e bruto → supporto,
tiratore → blaster, schermagliatore → utilità).

⚠️ **L'adepto resta scoperto**: è fuori dalle 21 celle, e il generatore preferisce
lasciare il vuoto dichiarato piuttosto che dargli la lista del mago.

⚠️ **Ranger e paladino lanciano da `livello − 3`**, e su **Saggezza** — non su
Carisma, che è la regola di Pathfinder e che questo repo aveva scritta sbagliata
nella skill 3.5 fino al lotto I.

**`--piu-cattivi`** applica il template *Advanced* di Pathfinder 1e: +4 a tutte
le caratteristiche, +2 di armatura naturale, +2 su tutti i tiri, **senza alzare
il GS**. Il template vale GS +1: la creatura è venduta come GS *n* e picchia come
GS *n+1*, e **lo dichiara di sé** in una voce del blocco. È una riga sola da
disfare se al tavolo è troppo.

**`--template NOME`** applica uno dei sette modelli semplici di Pathfinder 1e
al blocco finito, sempre senza cambiare il GS scritto: `advanced` (è
`--piu-cattivi`), `giant` (una taglia in più, +4 a Forza e Costituzione, −2 a
Destrezza, +3 di armatura naturale, dadi di danno un passo più su), `young` (il
contrario, e vale GS −1: serve ad alleggerire), `celestial`, `fiendish`,
`entropic`, `resolute` (scurovisione, resistenze, riduzione del danno,
resistenza agli incantesimi e punire una volta al giorno, secondo i dadi vita).
Il blocco dice in una voce quanto vale davvero e la riga `fonte:` lo ripete. I
numeri stanno in `sistemi/pf1e/dati/modelli.toml`, ognuno con la sua fonte nel
PRD. Gigante non si applica a una creatura Colossale, Giovane né a una
Piccolissima né a un drago. Gli archetipi di classe non sono modelli e il
generatore non li ha.

```bash
python3 scripts/genera_creatura.py --gs 7 --ruolo bruto --template giant
```

Su un incantatore `--piu-cattivi` accende anche **`--incantesimi pf1e`**, che
innesta gli incantesimi PF1e che in 3.5 **non esistono** — la linea della *fossa*,
*scirocco*, *saette*, *benedizione del fervore*. Uno per livello d'incantesimo,
e ognuno finisce fra i rincari col suo nome PRD, perché va letto lì: non c'è un
paragrafo 3.5 su cui ripiegare. `--incantesimi srd` lo spegne tenendo il template.

⚠️ **Non scambia gli incantesimi condivisi, ed è deliberato.** Sulla lista comune
PF1e non è più forte: *grasso*, *polvere scintillante* e i *tentacoli neri* sono
stati indeboliti, il «salva o muori» convertito in danno, il polimorfismo
riscritto. Vendere come «più cattivo» qualcosa di più debole è il modo peggiore
di sbagliare — invisibile alla generazione, e scoperto al tavolo.

**Dove finisce.** A schermo, o in una cartella con `--in`. **Mai dentro
`Bestiario/`**: il tool si rifiuta, e ti dice perché. Nel canone copi tu, dopo
aver letto: è lo stesso confine di `derive_statblocks`.

⚠️ **Quando NON usarlo.** Se nel catalogo c'è già qualcosa di simile,
**potenzia** quella (skill `npc-villain-boosting`) invece di generare un
doppione. Se la creatura ha un ruolo nella trama, **scrivila a mano**: il
generatore al massimo ti dà l'ossatura. Il suo caso vero è l'**incontro di
passaggio**.

### Incontri che non si ripetono

`suggest_encounter` può pescare **in parte** dal generatore, così due sessioni
non danno mai lo stesso incontro:

```bash
python3 scripts/suggest_encounter.py --el 9 --con-generatore
python3 scripts/suggest_encounter.py --el 9 --con-generatore --piu-cattivi
```

Una creatura generata entra in ogni proposta e il resto resta pescato dal
Bestiario. I blocchi delle generate sono stampati per intero in fondo, col conto
aperto. `--piu-cattivi` tocca **solo** la parte generata: i mostri veri del
catalogo restano quelli che sono.

### Quando una scheda NON è una creatura

Il Bestiario contiene anche cose che una creatura non sono: un organo collegiale,
una popolazione, un'ondata di combattimento di massa che è un **aggregato** di
altre schede, un dossier che punta agli statblocchi che vivono altrove. Quelle
**non devono avere un blocco**, e forzarcelo vorrebbe dire inventare un mostro
che non esiste.

Si marcano nel titolo, **con la ragione scritta sotto**:

```markdown
# Il Consiglio di Rethmar [NON-CREATURA]

> **Non è una creatura** (ADR-0033): è un organo collegiale di sette seggi.
> Gli statblocchi dei singoli consiglieri stanno nelle loro schede.
```

Da lì in poi la scheda **esce dal debito di migrazione** e **dal catalogo dei
mostri**, così `suggest_encounter` non può proporti un consiglio comunale come
incontro. Non è un'esenzione silenziosa: la ragione si legge nel file.

---

## 7. Aggiungere un mostro: la procedura completa

1. **Cerca prima**: `grep -ril "<nome>" Bestiario/`: c'è già qualcosa di simile?
   Se sì → §8 (potenzia, non duplicare).
2. **Scegli la cartella** e il **nome file** col CR ([RIFERIMENTO-BESTIARIO](../reference/RIFERIMENTO-BESTIARIO.md) §1, §2).
3. **Scrivi lo statblock** nel formato standard ([RIFERIMENTO-BESTIARIO](../reference/RIFERIMENTO-BESTIARIO.md) §3), citando la fonte.
4. Se è un villain/PNG nominato: **scrivi anche il dossier** ([RIFERIMENTO-BESTIARIO](../reference/RIFERIMENTO-BESTIARIO.md) §4).
5. **Rigenera il catalogo**: `python3 scripts/build_monster_catalog.py`.
6. **Valida**: `python3 scripts/validate_bestiario.py`.
7. Se cambia il canone di campagna (nuovo villain attivo, morte, alleanza):
   aggiorna `campaign/state.md`, e ricordati che le scritture di canone
   passano da `dm.py session` (ADR-0007), non a mano sulle regioni `auto:`.
8. **Traccia**: riga in `plans/CHANGELOG.md` se è un lotto di lavoro.

---

## 8. Potenziare invece di creare (quasi sempre la scelta giusta)

Se il party è di livello 13 e hai uno statblock CR 9 che ti piace, **non
scrivere un mostro nuovo**: potenzialo. Il repo ha una skill dedicata,
`npc-villain-boosting`, con tre metodi:

| Metodo | Quando |
|---|---|
| **Dadi Vita aggiuntivi** (advancement 3.5) | vuoi lo stesso mostro «più grosso», stessa identità |
| **Livelli di classe** | vuoi dargli un mestiere (il capitano gnoll che è anche chierico) |
| **Template** (3.5) o **simple template PF1e** (avanzato, elementale…) | vuoi cambiargli natura in fretta, con numeri già tarati |

Chiedi pure a un agente: *«potenzia razorfiend CR 9 per un party APL 13»*,
la skill si attiva da sola e applica i benchmark di GS. L'esemplare in repo
è `Bestiario/mostri/razorfiend-blackspawn-alfa-cr13.md` (Huge 16 DV,
ottenuto avanzando il razorfiend CR 9).

Il file nuovo, se lo crei, segue comunque [RIFERIMENTO-BESTIARIO](../reference/RIFERIMENTO-BESTIARIO.md) §2-§3, e il vecchio **resta**:
la truppa d'ondata e l'élite convivono.

**E il generatore?** Serve per il caso opposto: quando nel catalogo **non c'è
niente di simile**. Se qualcosa c'è, potenziare è quasi sempre meglio: la
creatura ha già un nome, una fazione e una storia, e il generatore quelle non
te le dà (§6-ter).

---

## 9. Se la CI diventa rossa

| Messaggio | Causa e rimedio |
|---|---|
| **catalogo non in sync** | hai toccato uno statblock senza rigenerare → `python3 scripts/build_monster_catalog.py` e committa lo YAML |
| **header mancante** | manca uno dei sei (`Faction/Role/Environment/CR/Source/Status`) → aggiungilo, sulla riga singola separata da ` | ` |
| **CR filename ≠ CR header** | allinea i due (ricorda `05` = ½) |
| **stato non dichiarato** | metti `[CANONE — DM …]` o `[INFERRED — …; base: …]` nel titolo **e** `Status:` nell'header |
| **filename non conforme** | kebab-case minuscolo + `-crN.md`, niente spazi o maiuscole |
| **`mostri/` contiene non-statblock** | spostalo: i dossier vanno in `villain/` o `png/` |
| **dossier senza titolo** | aggiungi un `# Titolo` in cima |
| **struttura legacy rilevata** | esistono ancora `Armate-UNITA-NUOVE/`, `Monsters_Sheets/` o `PNG/` a root → vanno migrate in `Bestiario/` |

---

## 10. Dove sta il resto

| Cosa | Dove |
|---|---|
| Indice e regole della libreria | [`Bestiario/README.md`](../../Bestiario/README.md) |
| Template dossier PNG/villain | `campaign/templates/png-dossier-template.md` |
| Potenziamento: decisione, metodi, workflow | skill `npc-villain-boosting` (`references/boost-decision.md`, `boost-methods-35.md`, `boost-workflow.md`) |
| Regole 3.5 / PF1e per costruire | skill `dnd-35-srd` · `pathfinder-1e-srd` |
| Censimento di ciò che manca (cosa dell'AP non è ancora in repo) | [`CENSIMENTO-MOSTRI-PNG-VILLAIN.md`](../../CENSIMENTO-MOSTRI-PNG-VILLAIN.md) (radice del repo) |
| Parametri esatti degli script | [`scripts/README-automation.md`](../../scripts/README-automation.md) · [`docs/tools/README.md`](../tools/README.md) |
| Proporre incontri col catalogo | `python3 scripts/dm.py prep --el 13 --env underground` |

## Il blocco statistiche (dal 2026-08-22)

→ Ora in [RIFERIMENTO-BESTIARIO](../reference/RIFERIMENTO-BESTIARIO.md#il-blocco-statistiche-dal-2026-08-22), che è un riferimento.
