# Riferimento del Bestiario: cartelle, nomi, statblock, dossier

> Forma: **riferimento** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)). Descrive com'è fatta una scheda del Bestiario; la ricetta per aggiungerne una sta nella guida. Nato il 2026-11-10 dalle sezioni di riferimento di [GUIDA-BESTIARIO](../how-to/GUIDA-BESTIARIO.md). Le sezioni tengono il numero che avevano lì, così un rimando scritto prima («GUIDA-BESTIARIO §N») resta vero: nella guida, al posto della sezione, c'è un rimando a questo file.

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
# Nome Creatura (contesto) [CANONE — DM 2026-05-05]
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
| `Source` | **sempre citata**: `MM p.NNN`, `RHoD p.NN`, `FRCS`, `SRD`, o una marca `[INFERRED — domanda; base: …]` se costruita |
| `Status` | `accepted` (canone confermato dal DM) o `inferred` (proposta) |

**Regole di contenuto:**
- niente **testo verbatim non-SRD** (copyright): degli incantesimi si citano
  nome, livello e CD, non la descrizione;
- niente **poteri inventati senza flag**: se non è attestato, marcalo
  `[INFERRED — <domanda al DM>; base: <fonte o dato>]` ([GUIDA-MARCATURE](GUIDA-MARCATURE.md));
- `Notes:` finale = **come si usa nella campagna** (dove compare, con chi,
  perché): è la parte che ti serve davvero al tavolo.

### Titolo e stato di canone

Nel titolo H1 ci va il flag:

- `[CANONE — DM AAAA-MM-GG]` → il DM l'ha confermato: è canone;
- `[INFERRED — <domanda>; base: <…>]` → ricostruito o proposto, in attesa.

La grammatica completa è in [GUIDA-MARCATURE](GUIDA-MARCATURE.md); le schede
vecchie con `[ACCEPTED — DM-canon …]` sono state migrate il 2026-11-07 (ADR-0109).

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

**La forma delle due schede** ([ADR-0091](../../plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md)):
lo statblocco porta **Difesa · Attacco · Statistiche · Capacità speciali ·
Tattiche** in quest'ordine, come le AP di Pathfinder 1e; il dossier, se ha
sezioni, porta **Chi è · Aspetto e voce · Cosa vuole · Nella campagna ·
Esiti possibili · Fonti e canone**, più **In combattimento** quando rimanda a
uno statblocco. I numeri stanno solo nello statblocco, e il dossier ci rimanda.
Le schede di prova: Lorana, Ushgar, Balvar. Il conto:

```bash
python3 scripts/validate_bestiario.py --forma   # rapporto, non blocca
```

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
eventuali livelli di classe, e le tabelle producono i numeri. Vedi [GUIDA-BESTIARIO §6-ter](../how-to/GUIDA-BESTIARIO.md#6-ter-costruire-una-creatura-che-non-cè).

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
