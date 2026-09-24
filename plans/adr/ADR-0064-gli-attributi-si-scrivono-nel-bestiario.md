# ADR-0064 — Gli `attributi` si scrivono nel Bestiario, e ognuno dice da dove viene

- **Stato**: 🟢 accettata
- **Data**: 2026-09-23
- **Contesto**: ordine del DM, 2026-09-21 — *«generare coerentemente gli stat block nei 96 stat blocchi che non li hanno usando dei generatori random che utilizzano le regole di dnd 3.5 e/o pathfinder 1e o gli stat array elite e std […] (usa le regole deterministiche più affidabili con una percentuale di random in modo che non siano tutti uguali se possibile)»*
- **Emenda**: [ADR-0033](ADR-0033-derivare-e-dichiararlo.md), la regola «lo strumento propone, e scrive una cosa sola»
- **Emendata da**: [ADR-0065](ADR-0065-la-conformita-si-corregge-dove-il-dato-non-e-una-scelta.md), lo stesso giorno — vedi *Emendamento* in fondo
- **Rende possibile**: le tre identità profonde di [RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI](../RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI.md) §5

---

## Contesto

La ricerca sulla conformità meccanica aveva trovato un muro solo: **14
statblocchi su 110** dichiaravano `attributi`. Senza For, Des e Cos non si
ricava nessuna delle tre identità profonde del 3.5: i pf dai DV e dalla
Costituzione, i TS dalla progressione, l'attacco da BAB, modificatore e taglia.
La ricerca chiudeva con una decisione aperta per il DM, e il DM ha deciso:
generarli.

ADR-0033 però dice che lo strumento **propone**, e scrive un campo solo (i TS)
e solo dove GS, CA e pf li ha scritti il DM. `genera_creatura.py` lo ripete nel
suo docstring: *«mai dentro `Bestiario/`»*. Eseguire l'ordine vuol dire
allargare quel confine, e un confine si allarga per iscritto.

## Decisione

**`scripts/genera_attributi.py` scrive la riga `attributi` nei 94 statblocchi
che non l'hanno, alle condizioni che seguono.** Nessuna è facoltativa.

### 1. Si copia prima di generare

Quattro strati, in ordine: la sestina **trascritta** dalla fonte citata in
`Bestiario/pregen-pcgen/`; la Destrezza **letta** in `ca-dettaglio`; Des e Cos
**derivate** da CA di contatto e pf; l'array del Manuale del DM **scelto** per
ruolo, con taglia e razza SRD. Le tabelle sono quelle di `dmcore.tabelle`, le
stesse di `genera_creatura`.

Lo strato 0 copre **39 file su 94**. La prima stesura non l'aveva, e generava
numeri per 42 file che citavano la loro fonte. Quando la fonte contiene più
creature, la sestina si sceglie **per nome** (l'intestazione «2. Myconid Elite
Guards» ↔ `myconid-elite-guard`) e mai per compatibilità numerica: quella
regola, provata, dava al *myconid worker* la Forza 26 del sovrano.

### 2. Ogni blocco dice da dove viene

Sotto il blocco una riga di marca, specifica di questo script:

- `[INFERRED — needs DM confirmation]` sempre, perché è la regola 5 di
  `AGENTS.md`;
- **trascritti** o **generati**, perché le due cose valgono in modo diverso;
- le **divergenze** fra fonte e statblocco, quando ci sono (10 file). La guardia
  annota e non sopprime, come ADR-0033 ha imparato a fare.

Dove la fonte e lo statblocco divergono vince lo statblocco **solo** se
l'indizio è forte: Cos da pf con DV verificati. La CA di contatto somma anche
deviazione e schivata, e con un DV solo il pf può essere la media o il massimo:
in quei casi resta la fonte, e la divergenza si scrive.

### 3. Si riproduce, e un cancello lo verifica

Il caso c'è: ±1 a somma zero su due secondarie. Ma **il seme è il nome del
file**, non l'orologio. `genera_attributi.py --check` gira in CI e fallisce se
un blocco marcato non è quello che la regola produce, se un valore esce da
1–45, o se un file ha due blocchi o due marche. `--rigenera` riscrive **solo** i
blocchi marcati: un blocco scritto dal DM non si tocca mai.

### 4. Si esce togliendo la marca

Quando il DM conferma o corregge un blocco, toglie la riga di marca. Da quel
momento il blocco è suo: il cancello smette di guardarlo e `--rigenera` non lo
riscrive.

## Conseguenze

**Buone.**

- Le identità profonde hanno una superficie: `attributi` c'è ora in **tutti i
  108** statblocchi che hanno il blocco `statblocco` (erano 14). Il
  rilevatore che le verifica diventa un lotto e smette di essere una decisione
  aperta.
- Lo strato 3 ha un errore **misurato**: sui 39 file con fonte, generando come
  se la fonte non ci fosse, sbaglia di **1,91 punti** in media (0,96 di
  modificatore, 79% entro ±1). `--taratura` lo ripete.
- Scrivendo il generatore è venuto fuori un difetto di dati: `pf-dado` riporta
  spesso il danno di un'arma (`1d8+7` accanto a «hp 93 (12 HD)»). In **20
  statblocchi su 95** i dadi non tornano coi DV dichiarati; col dado di classe
  SRD e col dado solo a GS ≥ 2 i sospetti sono **26**. `validate_bestiario
  --rules` ora li segnala, riusando lo stesso controllo.

**Il prezzo, dichiarato.**

- **55 blocchi su 94 sono scelti, non misurati.** Sono plausibili per ruolo, GS,
  taglia e razza, e restano una scelta. La marca lo dice file per file.
- **La taratura è in-campione.** Le regole vengono dall'SRD, ma è su questi 39
  file che si è visto che servivano, e il passo di progressione è stato
  lasciato com'era proprio per non adattarlo a loro (cambiarlo spostava
  l'errore di 0,04).
- **Le caratteristiche mentali restano le più lontane** (Int 2,7 · Car 2,3): il
  ruolo dice come una creatura combatte, non quanto è intelligente.
- **Due fonti non si leggono**: il PDF del death tyrant (la stdlib non lo apre, e
  il cancello deve poter rigenerare in CI) e il `Cha -4` di un export PCGen che
  stampa il modificatore al posto del punteggio. Quei file restano generati.
- **`validate_bestiario --rules` sale da 3 a 29 avvisi.** Non è peggiorato
  niente: sono 26 `pf-dado` sbagliati da prima, che adesso si vedono. Per la
  stessa ragione il lotto 3 della ricerca (promuovere `--rules` a cancello)
  **non si può fare ancora**: bloccherebbe su dati da correggere a mano.

## Fonti

- SRD 3.5, *Improving Monsters* (tabella «Changes to Statistics by Size»),
  modificatori razziali, dadi vita delle classi.
- Manuale del DM 3.5, matrici delle caratteristiche dei PNG, già in
  `scripts/dmcore/tabelle.py`.
- `Bestiario/pregen-pcgen/`: export PCGen e pagine SRD, archivio in sola lettura.

---

## Emendamento — 2026-09-23, qualche ora dopo

🔴 **I conti di questo ADR erano sbagliati, e il motivo è uno strato mancante.**
Correggendo `pf-dado` (ADR-0065) è venuto fuori che il sergente hobgoblin
scrive nella sua prosa «**Abilities**: Str 14, Dex 12, Con 14, Int 10, Wis 10,
Cha 8», e il generatore gli aveva dato Car 17. **27 dei 55** file contati qui
come «scelti» avevano i numeri del DM due righe sotto il blocco; altri 12 li
scrivevano in italiano («For 31, Des 13, Cos 23…»), e il lettore capiva solo
l'inglese.

| | questo ADR diceva | dopo l'emendamento |
|---|---:|---:|
| copiati dalla scheda stessa | — | **39** |
| trascritti dalla fonte | 39 | **37** (due schede scrivono i loro, e vincono) |
| scelti dall'array | 55 | **18** |

La decisione resta quella del §1-4, con uno strato in più **prima** di tutti:
la sestina che la scheda scrive. Quella è del DM e non si tocca, nemmeno quando
un vincolo dice altro: la divergenza si annota.

📏 **E la taratura ha guadagnato il banco che le mancava.** Le 39 sestine delle
schede sono state trovate **dopo** aver fissato le regole, quindi sono un banco
**fuori campione**: lo strato scelto ci sbaglia di **1,84 punti** (79% entro ±1
di modificatore), contro 1,63 sul banco in campione. Il generatore regge su file
che non ha visto; l'obiezione «in-campione» del §*Prezzo* ha adesso una risposta
misurata.


## Emendamento — 2026-09-23, sera

Due strati nuovi, entrambi **vincoli** e non scelte: un TS scritto sotto
l'atteso fa da **tetto** a Cos, Des o Sag, e l'iniziativa di una scheda che non
elenca i talenti ammette **due** Destrezze. Toccano solo un valore dell'array e,
davanti a un numero del DM, si annotano. Il lettore della sestina ora salta la
parentesi dopo il punteggio, e tre schede passano dall'array alla loro prosa.

| | dopo il primo emendamento | adesso |
|---|---:|---:|
| copiati dalla scheda stessa | 39 | **41** (tre nuovi, Karruk uscito dalla marca) |
| trascritti dalla fonte | 37 | 37 |
| scelti dall'array | 18 | **15** |

📏 La taratura scende a **1,50** in campione e **1,54** fuori (erano 1,63 e
1,84). Il banco fuori campione ha però un file in comune con quelli da cui il
tetto è nato, l'ogre frantumapietra: vedi ADR-0065, terzo emendamento.
