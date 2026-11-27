# Regole ufficiali: tabelle dei termini 3.5 e PF1e (2026-11-07)

Lotto di [ADR-0110](../../adr/ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md).
Il DM ha chiesto vincoli su tutti i termini ufficiali, «una volta per tutte», misurati su almeno
30 prove, e tabelle complete prima delle prove. I testi delle fonti non entrano nel repo
(ADR-0103): qui ci sono solo i nomi e gli script.

## Le tabelle

| Tabella | Voci | Tipi principali |
|---|---|---|
| `scripts/lessico_it_35.tsv` (italiano → SRD 3.5) | 3.944 | incantesimi 1.398, talenti 986, oggetti magici 776, trappole 79, classi di prestigio 220, equipaggiamento 189, proprietà magiche 71, classi 46, abilità 40, condizioni 38, domini 35, mostri 31 |
| `scripts/lessico_it_pf1.tsv` (italiano PF1e → PRD) | 9.371 | mostri 2.213, incantesimi 2.112, oggetti magici 1.958, talenti 1.741, archetipi 395, equipaggiamento 271, proprietà magiche 196, archetipi di mostro 120, classi 44, razze 37 (Core e ARG, 37 su 37) |
| `scripts/talenti_manuali_35.tsv` (talenti inglesi di tutti i manuali 3.5, solo nomi) | 3.846 | 1.297 con sigla e pagina (crystalkeep, Chet Erez e Outlands 2007), il resto dall'elenco realmshelps; generata da `abbinamenti/indice_talenti_35.py` |
| `scripts/talenti_manuali_pf1.tsv` (talenti inglesi di tutti i manuali PF1e, solo nomi) | 3.432 | Archives of Nethys, `aonprd.com/Feats.aspx`; generata da `abbinamenti/indice_talenti_pf1.py` |

Ogni riga dice da dove viene la coppia (quarta colonna). Le fonti e il metodo di abbinamento
sono nell'intestazione di ciascuna tabella e in [abbinamenti/README.md](abbinamenti/README.md).

## Le fonti e come si abbinano

- **3.5**, nomi con l'inglese accanto:
  - database bilingue di Mephit (GPL-3);
  - 5° Clone, che dà manuale e pagina per incantesimi, talenti, classi e classi di prestigio,
    compresi i manuali non base;
  - tapionx (CC0), che copre gli incantesimi SRD.
- **3.5, abbinamento senza usare i nomi**:
  - SRD di Editori Folli: incantesimi per scuola, livelli e componenti; equipaggiamento per costo,
    danni o CA e peso;
  - tabelle del tesoro del GDM (scheda di Mindbender), per intervalli di d% e prezzo.
- **PF1e**:
  - link inglese di ogni pagina di Golarion (aon o d20pfsrd), con filtro di unicità;
  - archetipi per firma dei privilegi, livello e tipo Str/Sop/Mag, contro il PRD e aon.
- **Prontuari del DM** (PDF caricati il 2026-11-07): abilità e condizioni.

## Le misure

Fonte contro fonte, sulle voci che hanno tutte e due (`misura_tabelle.py`, `misura-tabelle.json`):

| Confronto | Concordi |
|---|---|
| incantesimi 3.5: miniaturefantasy+Sigil ↔ firma di Editori Folli | 505/506 |
| incantesimi 3.5: tapionx ↔ tabella | 600/605 (2 scambi bene/male di tapionx, 3 forme diverse) |
| incantesimi 3.5: 5° Clone ↔ tabella (prima di aggiungere il 5° Clone) | 562/566 (refusi del 5° Clone) |
| talenti 3.5: 5° Clone ↔ tabella | 181/188 (2 refusi di Mephit, 1 corretto) |
| classi 3.5: 5° Clone ↔ tabella | 30/31 (Ierofante, nome non riscontrato → Gerofante) |
| equipaggiamento 3.5: Mephit ↔ firma di Editori Folli | 118/125 (metallo/acciaio, refusi) |
| oggetti 3.5: tesoro del GDM ↔ Mephit | 170/221; le discordanze: refusi di Mephit, nomi con il mago, tabella dei maggiori fuori ordine |
| oggetti specifici 3.5: elenco oggetti del DM (prezzo+pagina del GDM) ↔ tabella | 65/69; 2 refusi di Mephit corretti, 1 refuso dell'elenco (nuove vite), 1 forma diversa (adamantio/adamantina) |
| abilità 3.5: prontuario del DM ↔ tabella | 35/35 |
| condizioni 3.5: prontuario del DM ↔ tabella | 34/38 → 2 decise (Portato via, Accovacciato) |
| archetipi PF1e: firma ↔ link di Golarion | 57/57, 38 astenuti |
| righe PF1e già in tabella ↔ aon / d20pfsrd | 1.699/1.701 · 1.975/2.015 |
| glossario del MdG di gdrzine ↔ tabella | 87% (nomi della 3.0: Arma Preferita, Specializzazione in un'Arma) |

Il cancello, 40 casi per tipo (30 nomi presi dalla tabella e 10 nomi sbagliati). «Prima» vuol dire
il controllo con il solo indice inglese, cioè com'era prima di questo lotto:

| Tipo | Prima | Dopo |
|---|---|---|
| incantesimi | 11/40 | 40/40 |
| abilità | 10/40 | 40/40 |
| oggetti magici | 10/40 | 40/40 |
| talenti (`casi.json`) | 13/40 | 40/40 |

Attenzione: i 30 nomi giusti vengono dalla stessa tabella che si misura, quindi provano che il
controllo li legge, non che la tabella sia completa. La prova vera sono i 10 sbagliati, e prima
di tutto i confronti fra fonti indipendenti qui sopra. Nella prima lista dei nomi sbagliati ne
avevo messi cinque veri (Acrobazia, Mantello elfico, Stivali della velocità, Stivali della
rapidità, Amuleto dell'armatura naturale): il controllo li ha accettati, ed era giusto.

Sui campi delle schede del repo (`controlla --tutto --volumi --campi`):
- oggetti sconosciuti: da 58 a 45; restano soprattutto oggetti unici della campagna;
- talenti sconosciuti: da 151 a 137, il cricchetto della CI scende a 137.

## I file caricati dal DM il 2026-11-07 (sera)

Otto PDF e zip. Cosa chiudono:

- **Trappole 3.5** (scheda di Mindbender, con GS, CD e prezzo): 79 trappole del GDM abbinate a `traps.md`
  dell'SRD senza usare i nomi (`abbina_trappole.py`). Tipo nuovo `trappola` in tabella.
- **Elenco oggetti magici 3.5** (con manuale, pagina e prezzo): 72 armi, armature, scudi e oggetti maledetti
  specifici abbinati all'SRD per prezzo e pagina del GDM. 65 erano già in tabella con lo stesso nome; 3 sono
  nuovi (Freccia assassina, Freccia assassina superiore, Spada lunga di ferro freddo perfetta); 2 refusi di
  Mephit corretti (Bracciali dell'indifeso, Spada berserker). Le altre ~1.300 voci vengono da manuali non base
  e non hanno il nome inglese accanto: non entrano.
- **Elenco talenti 3.5** (con sigla del manuale e pagina) e **Incantesimi da mago e stregone**: i nomi dei
  manuali base sono già tutti in tabella (201 talenti, 299 incantesimi); il resto viene da manuali non base,
  senza inglese. Confermano anche i nomi giusti di cinque forme sbagliate che il controllo segnala nei booklet
  (Orrido avvizzimento, Immagine proiettata, Folata di vento, Luci danzanti, Spezzare incantamento): sono
  correzioni della fase 5, non voci nuove.
- **Manuale dei veleni**, **Tomo dell'equipaggiamento 3.0**, **PnG**, **Cammini eroici e destini epici**:
  netbook di appassionati o materiale 3.0. Non sono nomi ufficiali e non entrano nella tabella.
- Dei 157 termini sconosciuti dei campi delle schede, nessuno si chiude con questi file: sono oggetti unici
  della campagna, note dentro i campi, nomi inglesi fuori SRD o forme sbagliate di nomi che la tabella ha già.

## Decisioni del DM (2026-11-07)

- Blown Away = **Portato via**, dal prontuario delle condizioni.
- Cowering = **Accovacciato** (card).
- Nomi con il mago: vale **la forma del manuale** (Zainetto pratico di Heward, Freccia acida di
  Melf); la forma SRD senza il nome è una variante da correggere (card).

## Buchi che restano

- **Mostri 3.5**: in tabella ci sono solo 31 voci del Manuale dei Mostri (5° Clone). In rete non
  c'è un elenco legale completo; gli indici completi esistono solo in scansioni piratate, che non
  si usano. Le strade sono due: l'indice cartaceo del DM, oppure l'elenco dei mostri usati nei
  booklet da confermare (card aperta).
- **Oggetti 3.5 dei manuali non base**, fuori dal GDM e da Mephit.
- **Archetipi PF1e** senza un abbinamento sicuro: circa 270.
- **Domini chiusi o mirror morti** (giro 2026-11-07): web.archive.org chiude la connessione;
  25edition.it oggi è un casinò; sigil.altervista.org non esiste; rpgcrossing rifiuta i programmi;
  miniaturefantasy, fandom e d20srd rispondono 403.
