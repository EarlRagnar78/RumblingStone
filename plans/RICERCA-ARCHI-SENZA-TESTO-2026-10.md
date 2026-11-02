# RICERCA · Gli archi senza testo nel repo, e cosa si è perso nell'import

> **Cos'è.** Il censimento dei file non markdown (PDF, HTML, ODT, TXT) degli
> archi 00-10 e dei due standalone, con la risposta a una domanda per ognuno:
> il suo contenuto esiste anche in markdown, e se esiste, è arrivato intero?
> Dove un file vecchio dice una cosa diversa dal canone, la differenza è
> segnata in §4. Il DM le ha decise tutte il 2026-10-23.
>
> **Chi l'ha chiesto.** Il DM, il 2026-10-23: *«controllare se ci sono pdf o
> altri file relativi agli altri archi che sono presenti ma non scritti oppure
> dall'entrata magari qualche info è andata perduta»*. Dentro c'è il punto P28
> dell'indice (l'arco 05 solo in PDF); il resto diventa P30.
>
> **Il canone.** `campaign/lore/campaign-chronicle.md`, e per lo stato
> corrente `campaign/state.md`. Vince sui documenti vecchi.
>
> **Data**: 2026-10-23 · **Base**: `main` a `9334a85` · **Stato**: 🟡 misurato,
> D1-D12 decise dal DM il 2026-10-23, P30-b eseguito

## 0. Cosa ho guardato prima, e cosa questa ricerca non rifà

- [`SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05.md`](SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05.md)
  ha già ricostruito la catena 01-05 dal racconto del DM e dal registro XP, e
  la cronaca ne ha preso tutte le righe. Non la rifaccio. Il suo §2 è
  superato su due punti: l'arco 05 ha tre PDF e non due, e gli archi 01-03 non
  sono «da scrivere» allo stesso modo, perché la maggior parte del loro
  materiale è la trascrizione di manuali altrui (§3).
- La riga P28 dell'indice è nata dal triage delle chat del 2026-10-23 (ramo
  `claude/indice-triage-chat`, non ancora su `main`). Questa ricerca la esegue.
- `Bestiario/` ha già portato in markdown, con i numeri, una parte delle
  creature degli archi 02, 03, 04 e 06. Dove c'è, lo dico e non lo rifaccio.
- Fuori perimetro: le pagine `homebrew/*.html` degli archi 07, 09, 10 e del
  Drappo, che sono **generate** dai markdown (si rifanno con `dm.py`); i fogli
  `.ods` dell'arco 00, che non sono testo (il registro XP è già letto in
  `SOGGETTO-DISCESA` §6); le immagini; `Bestiario/pregen-pcgen/`, che non è un
  arco ma ha lo stesso problema (§3.8).

## 1. Come è stato misurato

Ogni PDF è passato da `pdftotext -layout`, ogni HTML e ODT da `pandoc -t
plain`. Dove un markdown dichiara di essere la stessa cosa, ho confrontato le
due versioni con uno script che elenca i numeri e i nomi propri presenti nella
fonte e assenti nel markdown. Lo script dà falsi positivi (date a piè di
pagina, parole incollate dall'estrazione), quindi ogni mancanza è stata
guardata a mano. Dove il markdown non c'è, ho cercato nel repo i nomi, i
numeri e le scene di ogni file (`grep -ril`), nella cronaca, nel Bestiario,
nelle schede dei PG e nei piani.

Il controllo trova ciò che è stato tolto o cambiato. Non trova ciò che la
fonte e il markdown sbagliano allo stesso modo.

## 2. Il censimento

| Arco | File non markdown (sorgenti) | Markdown nell'arco | Esito |
|---|---|---|---|
| 00 Mano Rossa | 2 PDF (schermo del DM, timeline e punti vittoria); 3 HTM sullo Shaar con 21 file d'appoggio; 2 TXT (`00_shar.txt`, `campagna_flusso.txt`); 4 ODS | 4 (le armate) | 🟠 `campagna_flusso.txt` ha appunti del DM mai portati (§3.1) |
| 01 La Miniera | 4 TXT | 0 | 🟠 trascrizioni di manuali; i due boss grell senza scheda (§3.2) |
| 02 Scala d'Ossa | 4 TXT, 1 file di lock di LibreOffice | 0 | 🟡 statblocchi nel Bestiario; due fili narrativi persi (§3.3) |
| 03 La Cittadella | 8 PDF, 4 HTML, 4 TXT, 1 ODT, 3 immagini WebP senza estensione | 0 | 🔴 il materiale più ricco e più perso: l'Orrore Palustre, Zanna, i drow del casato (§3.4) |
| 04 Tomba di Belkram | 4 HTML (2 doppioni), 6 TXT | 2 (doppioni, la celebromorfosi) | 🟡 la celebromorfosi è intera; trappole, Antenato Nanico e chierica di Lolth senza markdown (§3.5) |
| 05 Stanza Runica | 3 PDF | 0 → **1** con questa PR | ✅ trascritto in `ARC05-STANZA-RUNICA-TRASCRIZIONE.md`; 6 divergenze dal canone (§3.6) |
| 06 Corona di Adamantio | 16 PDF (8 doppioni in `_ARCHIVIO`), 4 TXT (2 doppioni), 1 file di swap di Kate | 25 | ✅ i PDF sono stampe dei markdown; nessuna perdita (§3.7) |
| 07 Portale della Forgia | 2 PDF; 2 TXT di provenienza delle immagini; 9 HTML generati | 129 | ✅ i due PDF sono in markdown (§3.7) |
| 08 Hammerfist | nessuno | 33 | ✅ |
| 09 Post-Hammerfist | 3 TXT (licenze e un README); 1 HTML generato | 129 | ✅ |
| 10 Abbazia della Rotta Sicura | 4 HTML; 1 HTML generato | 4 | ✅ gli HTML e i markdown coincidono (§3.7) |
| Drappo di Tarsilia | 1 TXT di provenienza; 5 HTML generati | 43 | ✅ |

Il primo conteggio del thread padre metteva l'arco 06 a 16 PDF e 25 markdown:
è giusto, e i PDF sono la stessa cosa dei markdown. Gli archi davvero senza
testo sono 01, 02, 03 e 05; l'04 lo è a metà.

## 3. Arco per arco

### 3.1 · Arco 00

- **`DM/RHoD_Timeline_and_VP.pdf`**: la timeline dell'orda (giorni 1-65) e la
  tabella dei punti vittoria dell'avventura originale. Il repo l'ha assorbita
  nel March Clock e negli echi (`Azarr Kul`, `Vraath`, `Tiri Kitor` in decine
  di file). Non si è perso niente che serva alla campagna.
- **`DM/RHoD_GM_Screen.pdf`**: uno schermo del DM di **Pathfinder** (azioni,
  lotta con BMC e DMC). Materiale di consultazione, non della campagna.
- **`00_shaar/`**: tre pagine di realmshelps.net salvate col traduttore di
  Google, più `00_shar.txt` copiato dallo stesso sito. Lore di Faerûn, già
  coperta dalla skill `forgotten-realms-lore`. È testo di un sito terzo
  (voce D12).
- **`campagna_flusso.txt`**: gli appunti del DM sull'apertura, e qui c'è la
  perdita. Nel repo **non** ci sono:
  - **Lando Norris**, che intercede presso Lord Jarmaath e alza l'offerta da
    3.500 a 4.500 mo;
  - **Khalzon Burn**, il capo con «la maschera dei draghi, quella della 5»;
  - il **negromante di Castel Wrath**, che rianima gli scheletri dei giganti e
    i resti della tribù della Luna della Morte (gli ogre restano scheletri, gli
    orchi diventano zombi);
  - le sostituzioni dallo *Splendente Sud*: il **gigante ciclope** e la
    **mantimera** al posto della chimera;
  - i goblin con orchi, ogre, sciamani orchi e ogre magi **schiavi degli
    hobgoblin**, due orchi barbari negli scontri importanti, un ogre magio come
    alternativa;
  - la taratura di uno scontro: «il chierico è GS 3, il portalame GS 6, gli
    altri GS 2 ma sono 4 e non 6».

  Ci sono invece Lord Jarmaath, Loranna Anitah (oggi Lorana), Kormul, la
  foresta di Amtar. Voce D8.
- **Il livello di partenza**: lo stesso file dice *«partono dall'ottavo
  livello»*, e il registro XP comincia a 28.000 PX, cioè l'8°. La cronaca
  intitola l'apertura «Phase A … (Levels 4–6)». Voce D7.

### 3.2 · Arco 01, La Miniera

- **`Miniera.txt`** (8.000 parole, inglese) e **`Miniera-ita.txt`** (la
  traduzione) sono il capitolo «Belkram's Fall» di *Expedition to
  Undermountain* (WotC) trascritto, col link alla copia su archive.org in
  testa. Clan Melairkyn, Gyudd erede di Re Melair IV, le nove stazioni di
  guardia, le nove chiavi della tomba (A-I), la tabella del tesoro della
  Cittadella, Drexlyn il nano vampiro. Il repo ne usa i nomi in tre prompt di
  immagini e in `SOGGETTO-DISCESA`.
- **`grellPatriarca.txt`**: il Grell Patriarca (grell mago 7, GS 10, 147 pf) e
  il «Tempio Nascosto» (EL 8), da *Lords of Madness* (WotC). **`grell
  necromante.txt`**: il suo seguito.
- La cronaca dà come nemici dell'arco il «Grell Necromancer» e il «Grell
  Patriarch, defeated». Nessuno dei due ha una scheda nel Bestiario: l'unico
  grell è quello della Torre Invisibile di ARC-09.
- Nessun appunto del DM dentro i due file lunghi (cercati i nomi dei PG,
  «nota», «modific», i GS sopra 10): è trascrizione pura.

Convertirli in markdown vorrebbe dire mettere nel repo un manuale WotC in una
forma più facile da copiare. Non lo propongo (voce D12).

### 3.3 · Arco 02, Scala d'Ossa

- **`00_nani_dwergar_abaddor_scala_di_ossa.txt`**: Adrick Garthun, Daxavalt e
  Kerg, Zenith Splintershield. Sono in
  `Bestiario/villain/duergar-scala-di-ossa-cr11.md`.
- **`Epic_fight_dwarf_duergar.txt`**: chierico di Abbathor 11, due
  antipaladini, tre duergar mago-ladro. Sono in
  `Bestiario/villain/abbathor-cleric11-cr11.md`,
  `abbathor-blackguard-cr10.md`, `Bestiario/mostri/duergar-mago-ladro8-cr7.md`.
- **`Fight_fungi_colony*.txt`** (le due versioni differiscono solo per il
  rientro): sovrano, guardie d'élite, guardie e operai miconidi. Sono in
  `Bestiario/mostri/myconid-*`.

Cosa si è perso:

- **Il duergar che scappa.** Il file dei duergar scrive accanto ai tre
  mago-ladro *«uno è quello fuggito»*, e gli appunti dello scontro dell'arco 03
  mettono in campo *«1 duergar mago scappato»*. Il Bestiario conserva la frase
  come variante; la cronaca non ha il filo. Voce D10.
- **Necromante o chierico.** La cronaca chiama il nemico dell'arco «evil
  dwarven necromancer of Abbathor». Il file, il registro XP («chierico di
  ABBATHOR duergar cr12 + cavalieri duergar») e il Bestiario dicono chierico,
  e il Bestiario gli dà GS 11 contro il 12 del registro. Voce D9.
- **I miconidi.** Il registro XP conta 6 operai, il file 4. Nella cronaca
  l'incontro coi miconidi non c'è, e la catena dei funghi (la Regina offesa due
  volte, §10 di `SOGGETTO-DISCESA`) non dice se uccidere una colonia di
  miconidi conta. La segnalo e non la apro come voce: è una domanda di
  scrittura, da porre quando l'arco si scrive.

### 3.4 · Arco 03, La Cittadella

Qui c'è il materiale più ricco e la parte più grande di ciò che non è
arrivato. Ciò che c'è:

- il Beholder Death Tyrant, in `Bestiario/villain/beholder-death-tyrant-cr14.md`
  (16 DV, 104 pf, GS 14, la versione più forte). Le fonti nell'arco ne danno
  altre due: il Death Tyrant di realmshelps (11 DV, 71 pf, GS 13) e il
  «Half-Illithid Beholder Zombie» GS 13 (`.odt` e `.html`). La scelta è già
  fatta dalla regola del DM sulla versione più potente; lo segno per chi
  cercasse le altre;
- il retriever, in `Bestiario/villain/retriever-cr11.md`.

Ciò che manca dappertutto, fuori dai file dell'arco:

- **L'Orrore Palustre d'Ombra** (`00_shadow-marsh/`, tre HTML e un TXT): una
  creatura del DM, aberrazione Enorme d'ombra, 14 DV, 133 pf, CA 23, GS 12,
  tentacoli che risucchiano livelli, poteri psionici (LM 7°, 35 PP), la palude
  di 15 m profonda 9 m che scende dal tempio. Gli appunti dello scontro la
  danno **giocata a 110 pf e CA 21, con un potere in meno e senza livelli
  negativi**. Non ha scheda nel Bestiario e non compare in nessun markdown.
- **Zanna**, ragno fase di taglia Grande chiesto dal DM (PDF di una chat):
  8 DV, 68 pf, CA 18. Nessuna scheda.
- **Lo scontro davanti al tempio** (`Scontro_davanti_tempio di moradin.txt`):
  EL 14 con il capitano del casato, tre guerrieri drow, il duergar fuggito,
  Zanna e l'Orrore; il veleno delle guardie è il minerale di luce oscura.
  Il registro XP lo conferma («orrore della palude + ragno fase + guardie
  casato drow»). La cronaca dell'arco non lo nomina.
- **I drow del casato** (`house_*.pdf`, cinque PDF): capitano (maresciallo 9,
  GS 10), guardie arcane, mago (warmage 8), sentinella dei ragni (ranger 9),
  combattenti. Sono pagine di un manuale WotC; nessuna scheda.
- **Il warlock** (`warlock_png_sazzt.pdf`): Saz'zt e Ruthenoc, «Warlocks
  beyond the Gate», da un manuale WotC. Il registro XP mette al tempio
  «warlock cr9 + 3 wraith + BEHOLDER». Gli appunti in `Tempio Nanico.txt`
  piazzano il Death Tyrant e tre spettri dietro i pilastri. La cronaca dà solo
  il beholder.
- **Il tempio** (`il Tempio di Moradin - in fondo guardiano da sx.txt`): gli
  otto pilastri, l'iscrizione «Racchiuso da un disegno divino…» e il
  meccanismo delle nove chiavi. È *Expedition to Undermountain* tradotto.

Due contraddizioni col canone:

- **Chi comanda il retriever.** La cronaca: lo stregone drow degli schiavisti.
  Il nome del file da cui il Bestiario l'ha preso: *«ordinato dai chierici di
  Abbathor di riportare Aegis Fang al loro re»*. Il registro XP lo mette
  subito dopo i duergar di Abbathor («RETRIEVER contro gli altri mentre Thorik
  dormiva»). Voce D11.
- **Lo scontro e il warlock fuori dalla cronaca.** Voce D11, seconda parte.

Igiene: `01_Il Guardiano/il_Guardiano`, `il_guardiano2` e
`00_shadow-marsh/shadow-marsh-horror` sono immagini WebP 1024 × 1024 senza
estensione. Nessuno strumento del repo le vede come immagini.

### 3.5 · Arco 04, Tomba di Belkram

- **La celebromorfosi** (`Stanza_celebromorfosi.html` e il suo markdown, in
  due cartelle identiche `00_` e `02_`): il confronto non trova numeri persi.
  ✅
- **`drow-cleric.html`**: la Chierica drow mezzo-illithid di Lolth (chierica 7,
  GS 8). Il markdown della stanza ha la «Drow Psionica Mezzo-Illithid» GS 8,
  che è un'altra scheda: della chierica, coi suoi incantesimi e i domini, non
  c'è traccia.
- **`Antenato_Nanico_cr13.html`**: l'Antenato Nanico, esterno Grande GS 13,
  167 pf, RD 15/adamantio. Nessuna scheda.
- **Le trappole e i mostri ritarati** (sei TXT): il cubo gelatinoso a 12 DV
  (GS 8, che il registro XP conferma: «cubo gelatinoso cr8»), il budino nero
  anziano, la fossa col pendolo GS 10 (T2), le torrette di incantesimi nei
  gargoyle (T7 e T11, due per stanza), il talento Colpo Possente per lo xorn,
  la stanza T3 con la fontana rossa e i due demoni a due bocche e quattro
  braccia (il registro: «2 drow cr9 + 2 carnevus demons»). Nessuno di questi
  ha un markdown. Lo xorn anziano sì
  (`Bestiario/mostri/xorn-anziano-fauci-di-diamante-cr12.md`).

### 3.6 · Arco 05, La Stanza Runica (P28)

Trascritto in
[`05_aa-stanza-runica/ARC05-STANZA-RUNICA-TRASCRIZIONE.md`](../05_aa-stanza-runica/ARC05-STANZA-RUNICA-TRASCRIZIONE.md),
coi numeri dei PDF e ogni divergenza segnata sulla riga. I tre PDF:
`dc53af8b-….pdf` è l'avventura intera (2.100 parole), il «riferimento rapido»
ne è il riassunto con qualche numero diverso, `stanzaRunica.pdf` è la mappa.
Le divergenze:

- **I funghi** (D1). I PDF ne fanno un aiuto per la druida: la spirale di
  zurkhwood porta alla runa nascosta, attivarla fa crescere i funghi, e il
  riferimento rapido aggiunge *Comunicare con i funghi*. Il canone dice che il
  gruppo li **brucia** e Hella perde il micelio. Convertendo vince il canone,
  come chiedeva la riga P28: nella trascrizione la regola resta, segnata.
- **Thorek Forgiamartello** (D2), «l'antico portatore della Corona». Nel canone
  Thorek è il re di Hammerfist, e Thorek I quello di mille anni fa.
- **La Gemma del Legame Spirituale** (D3), «chiave per la Corona». Nel canone
  le gemme sono tre (topazio, smeraldo, rubino), tutte nella Corona e tutte
  spente quando Thorik la indossa nell'arco 06; la Prova della Sala Profonda
  della Corona, che descrive proprio questa scena, attiva il topazio.
- **Le ricompense e i PX** (D4): la Benedizione di Thorek (+2 ai TS contro la
  paura) e il +1 slot non compaiono in nessuna scheda di PG; i PDF danno 4.800
  PE totali più bonus, il registro 5.800 per PG.
- **I nomi delle rune** (D5): dieci su dodici vengono da Tolkien.
- **I numeri che i tre PDF non si accordano** (D6): il soffitto (per fasce dal
  round 6 o 30 cm ogni 5 round dal 10), la CD di Conoscenze (25 o 28), il
  costo del dominio dei non morti (1d4 o 1d6 Saggezza), il round delle catene.

### 3.7 · Archi 06, 07, 10: nessuna perdita

- **06.** I nove PDF della Corona e della stanza portano in testa
  «OnlineMarkdown.com»: sono stampe dei markdown che stanno accanto. Il
  confronto trova solo date a piè di pagina e parole incollate
  dall'estrazione. I due TXT in inglese della Corona sono la prima versione di
  `00_corona_di_adamantio_completa_italiano.md`; restano fuori due esempi di
  missione per Moradin («la Sorgente Corrotta di Glimmerdeep», «il Martello
  Perduto di Thundarr») e il soprannome del rubino («Ruby of the Soulforge»).
  La divergenza fra questa cartella e la copia canonica in `PG/Artefatti/` è
  già segnata in `_SNAPSHOT-STORICO.md`.
- **07.** `BenedizioniDiMoradin.pdf` è in `DEF-2` §7 e in `DEF-3`.
  `SinergieArteFattiQuickReference.pdf` è in `PG/Artefatti/SINERGIE-ARTEFATTI-MASTER.md`;
  il PDF dà alla Trinità Divina +3 ai TS nel riquadro e +4 nel dettaglio, e il
  master tiene +4.
- **10.** I quattro HTML dell'Abbazia e i loro markdown coincidono: nessun
  numero perso, solo titoli incollati dall'estrazione.

### 3.8 · Fuori dagli archi, lo stesso problema

`Bestiario/pregen-pcgen/` contiene altre fonti grezze degli archi (una copia di
`00_scaladossa-abbattor-funghi/`, il retriever, il bebilith «guardiano delle
rovine prima della cattedrale», l'ettin a tre teste in `.odt` e `.pdf`, il
chierico dell'Underdark «Ainin»). Il bebilith e l'ettin non li ho incrociati
con il Bestiario: li lascio al lotto P30-a.

## 4. Il registro delle divergenze, per il DM

Ogni riga dice cosa dicono i file vecchi, cosa dice il canone, cosa proponevo e
cosa ha deciso il DM il 2026-10-23 (una card per voce). Le voci decise hanno
l'id barrato.

<!-- decisioni-dm: ARCHI-SENZA-TESTO -->

| # | Arco | Domanda |
|---|---|---|
| ~~D1~~ | 05 | **I funghi della Stanza Runica.** I PDF: la druida segue la spirale di zurkhwood, trova la Runa di Ysgard e i funghi crescono e la coprono. Il canone: il gruppo brucia i funghi della stanza e Hella perde il micelio. *Proposta*: vale il canone; quando l'arco si scrive, la spirale porta alla runa **e** il fuoco è la scorciatoia che il gruppo ha preso. La trascrizione resta com'è, segnata. **Deciso (DM, 2026-10-23)**: vale il canone, il gruppo brucia i funghi e Hella perde il micelio. Quando l'arco si scrive, la spirale resta come via lunga verso la runa e il fuoco è la scorciatoia che il gruppo ha preso |
| ~~D2~~ | 05 | **Chi è lo spirito nel sarcofago.** I PDF: «Thorek Forgiamartello, l'antico portatore della Corona». Il canone: Thorek è il re di Hammerfist, Thorek I suo antenato di mille anni fa, e una statua del Cuore è Thorek I. *Proposta*: chiedere se è Thorek I (il nome torna) o un altro portatore da rinominare. **Deciso (DM, 2026-10-23)**: è **Thorek I** Forgiamartello, l'antenato di mille anni fa, lo stesso della statua del Cuore |
| ~~D3~~ | 05 | **La gemma della prova.** I PDF: la Gemma del Legame Spirituale, chiave per la Corona. Il canone: tre gemme, tutte nella Corona e spente nell'arco 06; la Prova della Sala Profonda attiva il topazio. *Proposta*: la gemma dell'arco 05 è la chiave della stanza della Corona e non una quarta gemma; chiedere. **Deciso (DM, 2026-10-23)**: è la chiave della stanza della Corona e non una gemma della Corona. Le gemme restano tre |
| ~~D4~~ | 05 | **Le ricompense della Stanza Runica.** I PDF: Benedizione di Thorek (+2 permanente ai TS contro la paura) e +1 slot del livello più alto; 4.800 PE totali più bonus. Il registro XP: 5.800 PX per PG; nessuna scheda di PG porta la benedizione o lo slot. *Proposta*: chiedere se al tavolo sono state date; se sì vanno nelle schede, se no si scrive che non ci sono. **Deciso (DM, 2026-10-23)**: non sono state date. Niente Benedizione di Thorek né slot extra nelle schede; restano i 5.800 PX del registro |
| ~~D5~~ | 05 | **I nomi tolkieniani delle rune** (Moria, Erebor, Durin, Khazad-dûm e altri sei). Il canone non li usa. *Proposta*: restano nella trascrizione come documento d'archivio; un master li sostituisce con nomi nanici di Faerûn (regola di `SOGGETTO-DISCESA` §4-bis). **Deciso (DM, 2026-10-23)**: la trascrizione li tiene come archivio; un master li sostituisce con nomi nanici di Faerûn |
| ~~D6~~ | 05 | **I numeri in contrasto fra i tre PDF**: il soffitto (per fasce dal round 6, o 30 cm ogni 5 round dal 10), Conoscenze (natura) CD 25 o 28, il dominio dei non morti a 1d4 o 1d6 Saggezza, le catene dal round 4 o dal 7. *Proposta*: vale l'avventura intera (`dc53af8b`), salvo che il DM ricordi cosa ha usato. **Deciso (DM, 2026-10-23)**: valgono i numeri più duri: soffitto per fasce dal round 6, Conoscenze (natura) CD 28, dominio dei non morti a 1d6 Saggezza, catene dal round 4 |
| ~~D7~~ | 00 | **Il livello di partenza.** `campagna_flusso.txt` e il registro XP (28.000 PX): 8° livello. La cronaca: «Phase A … (Levels 4–6)». *Proposta*: correggere la cronaca a «8° livello», se il DM conferma che il gruppo non ha mai giocato i livelli 4-6. **Deciso (DM, 2026-10-23)**: il gruppo parte dall'8° livello; la cronaca è corretta |
| ~~D8~~ | 00 | **Gli appunti d'apertura mai portati**: Lando Norris e l'offerta da 3.500 a 4.500 mo, Khalzon Burn con la maschera dei draghi, il negromante di Castel Wrath con gli scheletri dei giganti e la tribù della Luna della Morte, ciclope e mantimera al posto della chimera, orchi e ogre schiavi degli hobgoblin. *Proposta*: chiedere quali sono successi al tavolo; quelli giocati entrano nella cronaca, gli altri restano appunti. **Deciso (DM, 2026-10-23)**: sono stati giocati tutti ed entrano nella cronaca dell'arco 00 |
| ~~D9~~ | 02 | **Il nemico della Scala d'Ossa**: «necromante di Abbathor» (cronaca) o chierico di Abbathor (file, registro XP, Bestiario)? E GS 11 (Bestiario) o 12 (registro)? *Proposta*: chierico, come dicono tre fonti su quattro; il GS lo decide la scheda giocata. **Deciso (DM, 2026-10-23)**: chierico di Abbathor, GS 11 come nel Bestiario; la cronaca è corretta |
| ~~D10~~ | 02-03 | **Il duergar mago fuggito.** I file lo fanno scappare dalla Scala d'Ossa e tornare davanti al tempio con i drow del casato. La cronaca non ha il filo. *Proposta*: entra nella cronaca se il DM conferma che è andata così. **Deciso (DM, 2026-10-23)**: sì, fugge e torna davanti al tempio; entra nella cronaca |
| ~~D11~~ | 03 | **Il retriever e lo scontro davanti al tempio.** Il retriever: comandato dallo stregone drow (cronaca) o mandato dai chierici di Abbathor a riprendere Aegis Fang (nome del file sorgente)? E lo scontro EL 14 (capitano del casato, tre drow, il duergar fuggito, Zanna, l'Orrore Palustre a 110 pf) e il warlock con tre spettri al tempio, che il registro XP conferma e la cronaca non nomina. *Proposta*: chiedere chi manda il retriever; lo scontro e il warlock entrano nella cronaca. **Deciso (DM, 2026-10-23)**: lo stregone drow comanda il retriever su commissione dei chierici di Abbathor, per riprendere Aegis Fang; lo scontro EL 14 e il warlock con i tre spettri entrano nella cronaca |
| ~~D12~~ | 00-03 | **Le trascrizioni di testi altrui nel repo**: il capitolo di *Expedition to Undermountain* (01, con il link ad archive.org), il Grell Patriarca di *Lords of Madness* (01), le pagine dei drow e dei warlock (03), le pagine di realmshelps.net (00, 03). *Proposta*: non convertirle in markdown; spostarle fuori dal repo, o almeno fuori dalle cartelle degli archi, se il repo diventa pubblico. Decide il DM, con la skill `rumblingstone-edizione`. **Deciso (DM, 2026-10-24, poi cambiato)**: prima «restano senza conversione», poi *«convertili anche il D12 in markdown, poi si cerca una soluzione adatta»*. Convertiti in 16 markdown nelle cartelle `_testi-altrui/` degli archi 00, 01 e 03 (elenco in §5-bis); dove tenerli resta da decidere |

## 5. Cosa propongo di fare (P30)

In ordine, una PR per lotto:

- **P30-a · Le schede che mancano** (agente, subito). Nel Bestiario, dai file
  dell'arco: l'Orrore Palustre d'Ombra con la versione giocata, Zanna, il Grell
  Patriarca, la Chierica drow mezzo-illithid di Lolth, l'Antenato Nanico, il
  cubo gelatinoso a 12 DV, il budino nero anziano. Sono quasi tutte creature
  ritarate o inventate dal DM, quindi testo suo. I drow del casato e i warlock
  restano rimandi a pagina (D12). Poi il bebilith e l'ettin di
  `pregen-pcgen/`. Con le voci POINTER delle creature dell'arco 05 si toglie la riga della
  trascrizione da `FUORI_RAGGIO` in `scripts/tests/test_png_archi_nel_bestiario.py`,
  messa da questa PR finché D1-D6 sono aperte.
- **P30-b · La cronaca corretta** ✅ (2026-10-23, con le risposte a D1-D11).
  Una riga per risposta nella cronaca degli archi 00-05.
- **P30-c · Le note del DM per gli archi 01-04** (agente; i testi altrui sono
  già convertiti, §5-bis, e le note li citano senza ricopiarli). Un
  markdown per arco con quello che è del DM: le trappole ritarate, gli scontri
  composti, le scelte di regia. Senza ricopiare i manuali.
- **P30-d · Igiene** (agente, classe M). L'estensione alle tre immagini WebP
  dell'arco 03; il file di lock `.~lock.Epic_fight_dwarf_duergar.txt#` e lo
  swap `.Belkram.md.kate-swp` via dal repo; i doppioni di `04_…/00_` e `02_`
  Celebromorfosi e di `06_…/_ARCHIVIO` verificati e, se il DM vuole, tolti.

Per l'arco 05 le risposte a D1-D6 sono nella trascrizione (tabella in testa)
e nella cronaca. Il master dell'arco è un'altra
cosa e non è chiesto.

## 5-bis. I testi altrui convertiti (D12)

Il DM ha chiesto il 2026-10-24 di convertire anche questi. Sono in una cartella
`_testi-altrui/` dentro ogni arco, così si spostano tutti insieme quando si
decide dove tenerli. Ognuno ha in testa la fonte e l'avviso che non è canone e
non va pubblicato. La conversione è automatica (`pdftotext`, `pandoc`, uno
script per paragrafi e titoli) e non corregge i refusi della fonte, quindi
`validate_lingua` e `build_monster_catalog` saltano quelle cartelle: il
catalogo ha già le creature dai sorgenti `.txt`, e contarle due volte darebbe
doppioni.

| Arco | Sorgente | Markdown |
|---|---|---|
| 00 | `00_shaar/00_shar.txt`, `Shaar.htm`, `Popolo dello Shaar.htm`, `Città e siti dello Shaar.htm` (realmshelps.net) | `00_Red Hand Of Doom/_testi-altrui/` (4 file) |
| 01 | `Miniera.txt`, `Miniera-ita.txt` (*Expedition to Undermountain*), `grellPatriarca.txt`, `grell necromante.txt` (*Lords of Madness*) | `01_LaMiniera/_testi-altrui/` (4 file) |
| 03 | i cinque `house_*_drow.pdf`, `warlock_png_sazzt.pdf`, `il Tempio di Moradin - in fondo guardiano da sx.txt`, `01_Il Guardiano/Realms Helps Creature_ Beholder, Death Tyrant.pdf` | `03_la Cittadella/_testi-altrui/` (8 file) |

Il rischio non cambia: sono testi coperti da diritti di altri, ora più facili
da copiare. Finché il repo è privato non pesa; prima di renderlo pubblico la
cartella va spostata o tolta (`rumblingstone-edizione`, gate d'uscita).

## 6. Limiti

- Il confronto automatico vede numeri e nomi, non il senso: una frase
  riscritta che dice il contrario passa. Le divergenze di §4 le ho trovate
  leggendo, e ho letto per intero solo i file di 00, 05 e le parti che
  riguardano i nemici di 01-04. Le trascrizioni lunghe dei manuali le ho
  cercate per appunti del DM, non lette riga per riga.
- Non ho aperto i fogli `.ods`, salvo il registro XP già letto in
  `SOGGETTO-DISCESA` §6.
- Quello che il DM ha deciso al tavolo e non ha mai scritto, questa ricerca
  non lo può trovare. Per questo D4, D8, D10 e D11 sono domande e non
  correzioni.
