# Guida completa — aggiungere un mostro, un PNG o un villain

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

# 1. crea il file nella cartella giusta col nome giusto (§1, §2)
#    Bestiario/mostri/nome-crN.md   ·   Bestiario/villain/<Nome>/nome-crN.md

# 2. scrivi lo statblock nel formato standard (§3)

# 3. RIGENERA IL CATALOGO — obbligatorio, altrimenti la CI diventa rossa
python3 scripts/build_monster_catalog.py

# 4. verifica prima di committare
python3 scripts/validate_bestiario.py
python3 scripts/validate_bestiario.py --rules   # avvisi non bloccanti (GS, policy)
```

---

## 1. Dove va cosa

| Cartella | Cosa ci va | Formato |
|---|---|---|
| `Bestiario/mostri/` | unità e mostri **generici e ripetibili** (fanteria drow, gnoll, razorfiend…) | **1 file = 1 statblock**, `nome-crN.md`. Qui **solo statblock** (più i README) |
| `Bestiario/villain/` | antagonisti **unici e nominati** (Azarr Kul, Ghostlord, Mira Serani…) | una **cartella per villain**: dossier + statblock. Statblock senza dossier stanno al livello base |
| `Bestiario/png/` | PNG unici **non antagonisti** (alleati/neutrali: Lorana, Lirien…) | come `villain/` |
| `Bestiario/pregen-pcgen/` | sorgenti storiche PCGen (`.pcg`, export HTML/PDF/TXT) | **sola lettura**: si trascrive nel formato standard, non si modifica |
| `Bestiario/tokens/` | immagini `.webp` (token e ritratti) | sottocartelle `mostri/`, `png/`, `Dragons/`, `da-catalogare/` |

**Come scegliere**: se la creatura può comparire in più scene senza un nome
proprio → `mostri/`. Se ha un nome, una storia e degli obiettivi → `villain/`
(se è ostile) o `png/` (se non lo è).

---

## 2. Come si chiama il file

- **kebab-case minuscolo**, con il CR alla fine: `bone-naga-cr10.md`,
  `razorfiend-blackspawn-alfa-cr13.md`;
- **`05` significa CR ½** (`goblin-scout-cr05.md`);
- il **CR nel nome deve combaciare** con quello dichiarato nell'header,
  se li cambi, cambiali in entrambi i posti;
- **varianti**: file distinti **solo se i numeri cambiano** (war adept
  fuoco/ghiaccio = due file). Gli export «con incantesimi / senza
  incantesimi» della stessa build sono **una sola scheda**.

---

## 3. Il formato dello statblock (obbligatorio)

```markdown
# Nome Creatura (contesto) [ACCEPTED — DM-canon 2026-05-05]
**Faction**: ghostlord-undead | **Role**: caster-melee | **Environment**: any | **CR**: 10 | **Source**: MM II p.146 | **Status**: inferred

Large aberration (undead) HD 13d12 (84 HP). AC 18 (-1 size, +3 Dex, +6 natural).
Fort +4 Ref +7 Will +13. BAB/Grapple +9/+18. Sting +13 (1d4+7 + paralysis Fort
CD 20). Str 20 Dex 17 Con - Int 16 Wis 15 Cha 17. Spells as Sorcerer 8
(CL 8, CD 13+liv): 0-6 1-7 2-7 3-7 4-5. Undead traits.
Notes: guardiana della lair del Ghostlord.
```

**I sei header sono obbligatori**: senza uno solo, la CI fallisce:

| Header | Cosa ci scrivi |
|---|---|
| `Faction` | a chi appartiene (`mano-rossa`, `ghostlord-undead`, `drow`, `neutrale`…) |
| `Role` | funzione tattica (`melee`, `caster`, `skirmisher`, `boss`, `caster-melee`…) |
| `Environment` | dove compare (`any`, `underground`, `forest`, `urban`…) |
| `CR` | numero, coerente col filename |
| `Source` | **sempre citata**: `MM p.NNN`, `RHoD p.NN`, `FRCS`, `SRD`, o `[INFERRED]` se costruita |
| `Status` | `accepted` (canone confermato dal DM) o `inferred` (proposta) |

**Regole di contenuto:**
- niente **testo verbatim non-SRD** (copyright): degli incantesimi si citano
  nome, livello e CD, non la descrizione;
- niente **poteri inventati senza flag**: se non è attestato, marcalo
  `[INFERRED — needs DM confirmation]`;
- `Notes:` finale = **come si usa nella campagna** (dove compare, con chi,
  perché): è la parte che ti serve davvero al tavolo.

### Titolo e stato di canone

Nel titolo H1 ci va il flag:

- `[ACCEPTED — DM-canon YYYY-MM-DD]` → il DM l'ha confermato: è canone;
- `[INFERRED — needs DM confirmation]` → ricostruito o proposto, in attesa.

Lo stesso stato va ripetuto in `**Status**`. Quando il DM approva: cambi il
flag, aggiorni `Status`, e se tocca il canone di campagna aggiorni
`campaign/state.md` (§8 changelog).

---

## 4. I dossier (solo `villain/` e `png/`)

Un antagonista nominato ha **due file**: lo statblock (i numeri) e il
**dossier** (chi è). Template: `campaign/templates/png-dossier-template.md`.

Struttura del dossier: **Role · Status · Location · Motivation · CR · Key
stats · Esiti · Notes**. Deve avere un **titolo H1** (lo verifica la CI).

Il dossier è dove vivono le cose che i numeri non dicono: cosa vuole, di chi
si fida, cosa succede se muore, cosa succede se scappa, e i **rami aperti**
lasciati alle decisioni del DM.

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

Oltre alla prosa, ogni scheda porta (o dovrebbe portare) un **blocco recintato**
coi soli numeri (`gs`, `ca`, `pf`, `ts` e il resto) che è quello che leggono la
stampa, l'export e i controlli ([ADR-0021](../../plans/adr/ADR-0021-statblocchi-machine-readable.md)).
**Oggi il Bestiario è a posto: 157 schede su 157**: 124 col blocco, 27 che i
numeri li hanno altrove, 6 che creature non sono. Per riempirlo ci sono **tre**
strumenti, e fanno cose diverse:

```bash
python3 scripts/extract_statblocks.py            # cosa si può TRASCRIVERE, e cosa manca
python3 scripts/extract_statblocks.py --apply    # scrive dove la prosa dice tutto
python3 scripts/derive_statblocks.py             # cosa si può DERIVARE, col conto scritto
python3 scripts/derive_statblocks.py --apply-ts  # scrive i soli TS (vedi sotto)
python3 scripts/genera_creatura.py --gs 7        # COSTRUISCE una creatura che non c'è
```

**`extract_statblocks` trascrive**: legge i numeri che hai già scritto in prosa.
Conosce parecchi dialetti: `**hp 34**`, `(5 HP)`, `hp ~30`, `**Punti Ferita:**
60`, `**Classe Armatura:** 19`, `**Tiri Salvezza:** Tempra +7, Riflessi +10,
Volontà +6`, `**Grado di Sfida (GS):** 9`, `TS +2/+9/+1`, quindi **scrivi come ti
viene** e lui probabilmente ci arriva. Se il numero era una stima (`hp ~30`), il
blocco lo dichiara invece di spacciarla per un dato.

**`derive_statblocks` deriva** dalle tabelle: SRD 3.5 per tipo di creatura,
progressioni dei TS, matrici elite/standard, taglie e armature; la tabella per GS
di Pathfinder 1e **solo come guardia**, che marca la proposta *«⚠ FUORI
BERSAGLIO»* quando il conto non torna. ⚠️ **Scrive un campo solo, i tiri
salvezza, e solo dove GS, CA e pf li hai scritti tu**: la base dei TS è esatta
dalle tabelle, mentre CA e pf dipendono da equipaggiamento e Costituzione, che da
una scheda in prosa non si leggono. Per quelli **propone e basta**, col conto per
esteso, e decidi tu ([ADR-0033](../../plans/adr/ADR-0033-derivare-e-dichiararlo.md)).

**`genera_creatura` costruisce** una creatura che nel Bestiario **non c'è**. Non
legge nessuna scheda: parte da quello che dichiari tu: GS, tipo, taglia, ruolo,
eventuali livelli di classe, e le tabelle producono i numeri. Vedi §6-ter.

### Quando i numeri stanno da un'altra parte

Ventisette schede non hanno il blocco perché **non devono averlo**: i numeri sono
già scritti altrove, e una seconda copia diverge alla prima errata. Le schede
stampabili dei quattro pregen stanno in `08_…/ARC08-02`, i PNG alleati in
`ARC08-01`; certi dossier puntano al proprio statblocco e certi statblocchi al
proprio dossier; due schede registrano lo **stato finale di canone** di un PNG
morto e rimandano ai numeri storici del modulo.

Si marcano come le non-creature, **ma con una differenza**: il rimando deve dire
*dove*, e il controllo va a vedere che quel posto esista.

```markdown
# Re Thorek Hammerfist [RIMANDO]
**Key stats**: → `08_.../ARC08-01-GUIDA-DM.md` §PNG Alleati. NON duplicare.
```

⚠️ È il marcatore più facile da abusare: basta dire «i numeri stanno altrove» e
nessuno controlla. Perciò `extract_statblocks --check` **controlla**: un rimando
senza bersaglio, o con un bersaglio che non esiste, fa uscire il gate rosso.

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
2. **Scegli la cartella** (§1) e il **nome file** col CR (§2).
3. **Scrivi lo statblock** nel formato standard (§3), citando la fonte.
4. Se è un villain/PNG nominato: **scrivi anche il dossier** (§4).
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

Il file nuovo, se lo crei, segue comunque §2-§3, e il vecchio **resta**:
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
| **stato non dichiarato** | metti `[ACCEPTED — DM-canon …]` o `[INFERRED — …]` nel titolo **e** `Status:` nell'header |
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

Una scheda può portare in testa, subito **dopo** l'intestazione, un blocco coi
soli campi meccanici ([ADR-0021](../../plans/adr/ADR-0021-statblocchi-machine-readable.md)).
La prosa resta dov'è: il blocco serve agli script, la prosa serve all'occhio.

````markdown
```statblocco
gs: 2
tipo: Small plant, 4d8+16
ca: 15
ca-dettaglio: contatto 11, colto alla sprovvista 15 (+1 taglia, +4 naturale)
pf: 34
pf-dado: 4d8+16
ts: Temp +6, Rifl +1, Vol +2
velocita: 6 m
attacchi:
  - Mischia schianto +5 (1d4+1)
voci:
  - Talenti: Allerta, Resistenza Fisica
```
````

- obbligatori: `gs`, `ca`, `pf`, `ts`. Gli altri campi sono in
  `scripts/schemas/statblock.schema.json`;
- `pf-dado` sono i **dadi vita**, non i dadi di danno;
- il `gs` deve coincidere col `-crN.md` del nome del file: è il modo tipico in cui
  una scheda potenziata resta indietro, e il gate lo controlla;
- «CR 1/2», «0.5» e `-cr05.md` sono lo stesso grado.

Per scriverlo non serve farlo a mano:

```bash
python3 scripts/extract_statblocks.py                 # cosa si riesce a ricavare
python3 scripts/extract_statblocks.py --apply         # scrive SOLO i blocchi completi
python3 scripts/extract_statblocks.py --check         # il gate (gira in CI)
```

L'estrattore **non inventa**: se un numero non c'è nella prosa, la scheda finisce
nel rapporto invece di ricevere un blocco a metà. Alla prima passata: 82 schede su
157 migrate, 75 da fare a mano.

In stampa il blocco diventa un riquadro (`#statblocco()`), coi numeri dove il DM
li cerca invece che dentro un paragrafo.
