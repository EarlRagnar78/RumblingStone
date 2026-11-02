# ARC-07 — ATLANTE MAPPE DEFINITIVO (Il Portale della Forgia Eterna)
## Griglie tattiche ULTRA-CLEAR · scala 1,5 m/quadretto · con posizioni, ambiente & tattiche

> ⭐ **Documento MASTER delle mappe dell'arco.** Raccoglie in un solo posto **tutte**
> le mappe tattiche dei 5 master DEFINITIVI (ARC07-DEF-1…5), portate al **massimo
> standard ultra-clear** con: griglia a coordinate, **terreno & altitudini**,
> **posizioni di PG / PNG / villain**, **tattiche dei PG** e **tattiche di
> villain/mostri** (add-on DM), ed **evoluzione dell'ambiente**. È la versione che
> i booklet (`homebrew/`) includono e che il DM stampa.
>
> **Standard adottato** (i migliori esemplari della campagna, per struttura e
> dettaglio): `08_.../Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` (matrice +
> add-on tattici per mappa), `Mappe/Portale-Forgia-L1/L2-REVISED-UltraClear.md`
> (coordinate + viste + posizioni), e come **riferimento di dettaglio esterno**
> le battle map ufficiali di *Red Hand of Doom*
> (`00_Red Hand Of Doom/Immagini/Area Map/…/MappeIncontri/*.webp`: griglia +
> add-on DM per posizioni, ambiente e tattiche di PNG/villain/mostri).
>
> **ASCII = fonte canonica** (decisione DM 2026-07-23): l'ASCII ultra-clear porta
> **tutti** i dettagli senza perdite. Le **6 mappe a griglia rettangolare**
> (T-2, T-3, T-6, S-2, M7-B, CM-1, più la carta CM-2) sono **rese a pergamena SVG** in
> `Mappe/rendered/ARC07-MAPPE-DEFINITIVO_map*.svg` col renderer a fedeltà piena
> (F1-F5 di `plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md`: niente celle
> fantasma, dims validate, scala dichiarata, legenda locale automatica). Le
> mappe **schematiche** (T-1, T-4, T-5, S-1, R-1, M7-A) restano solo-ASCII per
> scelta: sono diagrammi, non griglie.
>
> **Sistema**: D&D 3.5 (max PF1e). **CD** non DC. Le mappe originali embedded nei
> master restano valide e identiche a queste: questo file le **consolida e
> arricchisce** (add-on tattici), non le contraddice.

---

## 📖 MATRICE DI CONTENUTO (chi è master di cosa)

| Mappa | Beat / scena | Master (fonte griglia) | Tipo | Stato |
|---|---|---|---|---|
| **T-1** | Piano della Terra: orizzonte & percorso | DEF-1 §4 | strategica | ✅ |
| **T-2** | Foresta di Cristalli: agguato Xorn | DEF-1 §5 | tattica combat | ✅ |
| **T-3** | Campo dei Cristalli Viventi (skill challenge) | DEF-1 §6 | tattica/skill | ✅ |
| **T-4** | Tempio di Mithral: salto gravitazionale | DEF-1 §7a | sezione/co-op | ✅ |
| **T-5** | Anticamera della Magnetite: la Sentinella | DEF-1 §7b | tattica combat | ✅ |
| **T-6** | Camera dell'Altare: **TERROS L'ANTICO** | DEF-1 §8 | tattica BOSS | ✅ |
| **S-1** | Sala della Forgia Eterna (8 affreschi) | DEF-2 | hub/scenica | ✅ |
| **S-2** | Stanza della Corona (purificata) | **geometria canonica ARC-06**: `06_.../StanzaCoronaDiAdamantio/Tactics_and_maps.md` + stato DEF-2 | hub/scenica | ✅ |
| **R-1** | Il Cerchio del Rito (resurrezione) | DEF-3 | rituale/scenica | ✅ |
| **M7-A** | Hammerfist ≈372 DR (fortezza & orda) | DEF-4 | strategica | ✅ |
| **M7-B** | L'Arena del Duello: **SKULLCRUSHER** | DEF-4 | tattica BOSS | ✅ |
| **M7-C** | La tenda del comando di Zog'tar | DEF-4 Scene 7-8, contratto JSON (`ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.json`) | tattica | ✅ |
| **M7-H** | Il campo del capo, attorno alla tenda | DEF-4 Scene 6-8 e `ARC07-BARILE-SULLA-TENDA.md`, contratto JSON (`ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.json`) | tattica | ✅ |
| **M7-S** | Hammerfist in sezione, 372 e 1372 | lotto D28, `ARC07-MAPPE-HAMMERFIST-372-1372.md` | sezione | ✅ |
| **M7-D** | Il corridoio della fucina, livello −1 (372 e 1372) | DEF-4 Scena 5 + D45, D47; contratto JSON | tattica | ✅ 372 e 1372 (D48) |
| **M7-E** | Le gallerie di Zeth, livello −2 (372 e 1372) | DEF-4 Scena 5 + D30, D48; contratto JSON | tattica | ✅ 372 e 1372 |
| **M7-F** | La fucina grande, livello −3 (372 e 1372) | D45, D48; contratto JSON | tattica | ✅ 372 e 1372 |
| **CM-1** | Il Cuore della Montagna (1372, arrivo) | **geometria canonica ARC-08**: Atlante-Hammerfist **MAPPA 5** (⚠️ scala 3 m) + regia DEF-5 | strategica/climax 3B | ✅ |
| **CM-2** | Il lato nord del Cuore (la pulizia, Scena 3) | DEF-5 Appendice B, carta a 1,5 m dello spazio di CM-1 | tattica | ✅ |

> Rese SVG storiche (ancora valide, stanze «prima visita»): `Portale-Forgia-L1`
> (Stanza Corona/Belkram, Sala Forgia), `Portale-Forgia-L2` (colonna-K, Forgia
> Adamantina). Non sostituiscono le mappe-beat qui sopra: sono un'altra fase.

## 📑 INDICE
- **DEF-1 · Piano della Terra**: T-1 · T-2 · T-3 · T-4 · T-5 · T-6
- **DEF-2 · Ritorno & Affreschi**: S-1 · S-2
- **DEF-3 · Resurrezione**: R-1
- **DEF-4 · Viaggio a ≈372 DR**: M7-A · M7-B · M7-C · M7-H · e sotto la montagna M7-S · M7-D · M7-E · M7-F (`ARC07-MAPPE-HAMMERFIST-372-1372.md`, coi loro stati del 1372)
- **DEF-5 · Ritorno a Hammerfist**: CM-1 · CM-2

---

# DEF-1 · IL PIANO DELLA TERRA

## MAPPA T-1 — PIANO DELLA TERRA: orizzonte & percorso (strategica)

```
════════════════════════════════════════════════════════════════════════
  PIANO ELEMENTALE DELLA TERRA — vista d'insieme (distanze in m, non in scala)
════════════════════════════════════════════════════════════════════════
   [ARRIVO 0 m]        [300 m-1 km]        [1-1,5 km]     [1,5-2 km]
   ┌──────────┐    ╱╲  FORESTA        ▓▓▓ CAMPO        ~~~~~ OCEANO   ┌────┐
   │  ◎ ◎ ◎   │═══╱  ╲ CRISTALLI    ▓ 💠 ▓ CRISTALLI  ~~ DI ~~ ROCCIA│ ▣▣ │
   │ piattaf. │ p  │XX│ GIGANTI      ▓💎▓  VIVENTI     ~~ (grigia) ~~ │ ▣▣ │
   │ cristallo│ o  │  │ (30-60 m)    ▓ 💠 ▓ (skill     ~~~~~~~~~~~~~~~ │TEMPIO
   │  ◎ ◎ ◎   │ n  ╲  ╱ [XORN×3:      ▓▓▓  challenge)   50 m sopra ▲  │MITHRAL
   └──────────┘ t   ╲╱   Fauci di                        l'oceano    │ 100m³
                i         Diamante]  ← Aegis Fang VIBRA verso il Tempio →└────┘
   ◎ = cristalli luminescenti · ponti = pietra galleggiante · XX = pilastro
   corroso (Xorn) · 💠 Cristalli Viventi · 💎 Madre Cristallo · ▣ portale
   (faccia INFERIORE del cubo, verso l'oceano; ruota 1 giro/ora)
   GRAVITÀ 2× — movimento LENTO ovunque (§3)
════════════════════════════════════════════════════════════════════════
```
- **Tipo / scala**: strategica (percorso ~2 km, ~2,5 h di viaggio). NON è una
  griglia di combattimento: orienta le 3 tappe (T-2 → T-3 → T-4/T-5/T-6).
- **Terreno & altitudini**: piattaforma d'arrivo (cristallo, stabile) → ponti di
  **pietra galleggiante** (larghi 3 m, cadono nel vuoto laterale = gravità 90°) →
  foresta → campo → **Oceano di Roccia** (grigia, semiliquida) sormontato dal
  **Tempio-cubo** a **50 m di quota**. **Gravità 2× ovunque** tranne dentro il
  Tempio (gravità propria) e sull'Altare di Terros (T-6).
- **Posizioni**: i PG partono da OVEST (piattaforma ◎). La **bussola** è Aegis
  Fang, che vibra verso il Tempio (EST). Il Seme-Mercato di Varis non è sul
  percorso aperto: è nel Tempio, dopo la Sentinella (DEF-1 §6-bis).
- **Tattiche PG**: viaggiare a passo ridotto (gravità), non sprecare voli lunghi
  (Artemis stanca le Ali). Il percorso è lineare: nessuna scorciatoia sicura.
- **Ambiente dinamico**: il portale del Tempio **ruota 1 giro/ora** — la faccia
  utile (inferiore) è raggiungibile solo in certe finestre (aggancio a T-4).
- **Riferimento**: DEF-1 §4 (Atlante delle Zone) e §3 (gravità).

## MAPPA T-2 — FORESTA DI CRISTALLI: agguato degli Xorn (tattica combat)

```
════════════════════════════════════════════════════════════════════════
 FORESTA DI CRISTALLI GIGANTI — 27 m × 15 m (18 col × 10 righe · 1,5 m)
 Terreno difficile ovunque (movimento ×2) · gravità 2×
════════════════════════════════════════════════════════════════════════
COL →  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R
01    🟫 🟫 🔷 🔷 🟫 🟫 🟫 🟫 🟫 🌫 🌫 🟫 🟫 🔷 🔷 🔷 🟫 🟫
02    🟫 🔷 🔷 🟫 🟫 🟫 🕳️ 🟫 🟫 🌫 🌫 🟫 🔷 🔷 🟫 🟫 🟫 🟫
03    🔷 🔷 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🌫 🌫 🟫 🔷 🔷 🟫 🟫 🟫
04    🔷 🟫 🟫 🟫 🟫 🛡️ 🟫 🟫 🔮 🟫 🌫 🌫 🟫 🟫 🟫 🟫 🟫 🟫
05    🟫 🟫 🟫 🟫 🟫 🟫 🥋 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🕳️ 🟫 🟫 🟫
06    🟫 🟫 🟫 🪨 🪨 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🪨 🪨 🟫 🟫 🟫
07    🟫 🟫 🔷 🪨 🪨 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🪨 🪨 🔷 🔷 🟫
08    🟫 🔷 🔷 🟫 🟫 🟫 💠 🟫 🟫 🟫 🌫 🌫 🟫 🟫 🔷 🔷 🟫 🟫
09    🟫 🔷 🟫 🟫 🟫 🟫 🟣 🟣 🟫 🟫 🌫 🌫 🟫 🟫 🔷 🟫 🟫 🟫
10    🔷 🟫 🟫 🟫 🟫 🟫 🟣 🟣 🟫 🟫 🟫 🌫 🌫 🔷 🟫 🟫 🟫 🟫
════════════════════════════════════════════════════════════════════════
LEGENDA · 🔷 Cristallo Gigante (copertura totale, indistruttibile) · 🟫 roccia
frastagliata (terreno difficile) · 🕳️ punto d'emersione Xorn · 🟣 Fauci di
Diamante (élite) · 💠 base corrosa del pilastro (crolla → ponte) · 🛡️ Thorik
(F04) · 🔮 Artemis (I04) · 🥋 Tordek (G05) · 🌫 fenditure larghe 3 m e
profonde 18 m (J-L 01-04 e K-M 08-10: caduta 6d10, risalita Scalare CD 20) ·
🪨 geodi di cristallo alti 3-5 m (D-E 06-07 e N-O 06-07: copertura totale, PF 80,
Durezza 8, si spaccano).
@north N
@taglia G9 ; Grande
@tipo tattica caverna
```
- **Tipo / scala**: tattica, 18×10, 1,5 m. Combattimento d'imboscata.
- **Terreno & altitudini**: tutto **terreno difficile** (movimento ×2) + gravità
  2× → il party è LENTO; i cristalli 🔷 danno **copertura totale**
  (indistruttibili). Il pilastro corroso 💠 (G08) può essere fatto **crollare**
  (→ ponte o area bloccata). Due **fenditure** 🌫 (J-L 01-04, K-M 08-10) tagliano la foresta
  e due **geodi** 🪨 (D-E 06-07, N-O 06-07) fanno copertura che si spacca
  (DEF-1, «Ambiente dinamico del piano»).
- **Posizioni iniziali**: Thorik F04, Artemis I04, Tordek G05. **Xorn 1** emerge
  a G02, **Xorn 2** a O05 (🕳️); **Fauci di Diamante** (élite, 181 pf `[CANONE — DM 2026-10-18]`) attende a
  G09-H10 (🟣, Grande), sotto il pilastro.
- **Tattiche Xorn (nemico, round-per-round)**: Earth Glide come nell'SRD.
  Emergono e mordono, e restano in superficie fino al loro turno successivo:
  per riaffondare nello stesso turno servirebbe Attacco Rapido. Al turno dopo
  fanno l'attacco completo (morso e 3 artigli) o riaffondano e riemergono
  accanto a un altro con un morso solo (master DEF-1 §5). Fauci di Diamante a
  90 pf **si rifugia nel cristallo** (+4 CA) e tende un altro agguato.
- **Tattiche PG**: colpire gli Xorn rimasti in superficie, e preparare azioni
  contro le riemersioni;
  usare i cristalli come copertura contro il caster; far crollare 💠 per
  intrappolare la Fauci. Artemis in volo evita il terreno difficile.
- **Evoluzione**: se i PG demoliscono/negoziano (3 vie, §5), lo scontro cambia:
  demolizione = crolli, ordine = tregua, negoziato = Diplomazia (Terran) CD 18.
- **Riferimento**: DEF-1 §5.

## MAPPA T-3 — CAMPO DEI CRISTALLI VIVENTI (skill challenge)

```
════════════════════════════════════════════════════════════════════════
 CAMPO DEI CRISTALLI VIVENTI — 30 m × 12 m (20 col × 8 righe · 1,5 m)
 GRAVITÀ 2×   ·   ingresso da OVEST (A06), uscita a EST (T06)
════════════════════════════════════════════════════════════════════════
COL →  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T
01    🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️   ← vuoto laterale
02    🟫 🔮 🟫 🟫 💚 🟫 🟫 🔮 🟫 🔮 🟫 🔮 🟫 🟫 🟫 🔮 🟫 🔮 🟫 🟫   💚 E02 crepato
03    🔮 🔮 🟫 🔮 🔮 🔮 🔮 🟫 🔮 🔮 🔮 🟫 🔮 🟫 🔮 🟫 🟫 🟫 🔮 🟫   triangoli · cerchi · esagono
04    🟫 🟫 🟫 🟫 🟫 🟫 🔮 🟫 🔮 🔷 🔮 🟫 🔮 🟫 🔮 🟫 🟫 🟫 🔮 🟫   🔷 J04 Madre Cristallo
05    🟫 🟫 🟫 🟫 🟫 🟫 🟫 🔮 🔮 🟫 🔮 🔮 🟫 🟫 🟫 🔮 🟫 🔮 🟫 🟫
06    ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜   ← corridoio libero
07    🟫 🔮 🔮 🔮 🟫 🔮 🔮 🟫 🔮 🟫 🔮 🟫 🟫 🟫 💚 🟫 🟫 🔮 🟫 🟫   💚 O07 crepato
08    🟫 🟫 🔮 🟫 🟫 🔮 🟫 🟫 🔮 🔮 🔮 🟫 🟫 🟫 🟫 🔮 🔮 🟫 🟫 🟫   ↓ faglia a sud (+30 min)
════════════════════════════════════════════════════════════════════════
LEGENDA · 💚 Cristallo Vivente crepato, riforgiabile (E02 e O07): curato vale +2
🔮 Cristallo Vivente che canta, alto 1-3 m: copertura ½, chi ci entra lo rompe
🔷 Madre Cristallo (J04), alta 5 m · 🌫️ vuoto laterale, gravità a 90°: non si attraversa
⬜ corridoio libero (riga 06) · 🟫 suolo del giardino
════════════════════════════════════════════════════════════════════════
@north N
@tipo tattica caverna
@luogo Piano della Terra, giardino dei Cristalli Viventi
```
- **Tipo / scala**: skill challenge (6 successi / 3 fallimenti). Non è un
  combat. Il gancio personale di Artemis (Seme-Mercato di Varis) non è qui: si
  gioca nel Tempio, dopo la Sentinella (DEF-1 §6-bis).
- **Terreno & altitudini**: campo di cristalli cantanti; la **Madre Cristallo**
  (🔷 J04) è a **5 m di quota**; riga 06 è il **corridoio sicuro**; sopra riga 01
  è **vuoto laterale** (🌫️, gravità a 90° — non attraversare).
- **Posizioni notevoli**: 2 cristalli **crepati** (💚 E02, O07) → riforgiabili
  (bonus +2 alla vulnerabilità sonora di Terros). La runa di Varis in J05
  delle stesure vecchie non si gioca (canone del §6): J05 è suolo, il varco
  a sud del cerchio interno verso la Madre.
- **Prove (CD)** (DEF-1 §6, a giri: ogni PG tira almeno una volta a giro, ogni
  abilità vale una volta per PG a giro): Diplomazia CD 20 · Conoscenze (natura o
  dungeon) CD 18 · Intrattenere (canto) CD 22 → +2, fallita −1 · Utilizzare
  Oggetti Magici CD 15, solo con i gradi · per i nani, Conoscenze (architettura
  e ingegneria) o Cercare sulla pietra CD 18 → +1. Riforgiare un cristallo
  crepato = Osservare CD 18 per trovarlo + 1 carica di *Vigore della Forgia* →
  +2; è la prova del giro di quel PG, e se fallisce conta un fallimento.
- **Tattiche PG**: distribuire le prove sui punti forti; NON toccare i cristalli
  sani a caso: staccarne o romperne uno conta un fallimento.
- **Evoluzione**: 6 successi → la **Frequenza della Confusione**, la notizia che
  Terros è vulnerabile al sonico e +2 ai TS contro di lui; 6 successi senza
  fallimenti → anche il **Diapason Armonico**. 3 fallimenti → i Cristalli
  urlano: **10d6 sonico a tutti, nessun TS**, e l'urlo sveglia e prepara Terros.
- **Riferimento**: DEF-1 §6 (il Seme di Varis è al §6-bis, nel Tempio).

## MAPPA T-4 — TEMPIO DI MITHRAL: approccio & salto gravitazionale (sezione)

```
════════════════════════════════════════════════════════════════════════
 APPROCCIO AL TEMPIO — sezione verticale (l'"alto" è relativo)
════════════════════════════════════════════════════════════════════════
        ┌───────────────── TEMPIO (cubo 100 m, ruota) ─────────────────┐
        │  ░░░░░░ gravità PROPRIA · corridoi ruotano 90° ogni 20 m ░░░  │
        └───────────────┬────────── ▣ PORTALE (faccia inferiore) ──────┘
                        │ 3) i PG salgono la corda (Scalare CD 15)
             ▲ gravità  │ 2) a ~20 m la gravità del Tempio CATTURA Tordek
             │ del      │    → "cade" verso il portale (Inception)
   50 m      │ Tempio   │ 1) TORDEK salta (Saltare CD 25, Take 10 = 26 ✓)
             │          │      [le Rune di Attracco si colpiscono all'arrivo]
   ~~~~~~~~~~┴~~~~~~~~~~~┴~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   ~~~~~~~~~~ OCEANO DI ROCCIA (grigia, liquida-ma-cede) ~~~~~~~~~~~~~~~~
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   Ruoli: Thorik = ANCORA (FOR CD 20) · Artemis = TRAGHETTATORE (vola col cavo)
          Tordek = NAVIGATORE (Saltare CD 25 + Rune di Attracco)
════════════════════════════════════════════════════════════════════════
```
- **Tipo / scala**: sezione verticale co-op (puzzle di gravità), non combat.
- **Terreno & altitudini**: il **Tempio-cubo** fluttua **50 m sopra** l'Oceano di
  Roccia e ha **gravità propria** (i corridoi ruotano 90° ogni 20 m). Sotto:
  Oceano di Roccia (semiliquido, cede — chi cade affonda lento, non muore subito).
- **Ruoli/posizioni**: **Tordek** = navigatore (Saltare CD 25 + Rune di Attracco);
  **Thorik** = ancora (FOR CD 20 tiene il cavo); **Artemis** = traghettatore (vola
  col cavo). A ~20 m la gravità del Tempio cattura chi salta → "cade" verso il
  portale, e all'arrivo Tordek colpisce le Rune di Attracco. Il Tempio è a
  **40 m** dalla riva e il portale **50 m** sopra l'oceano (D34): una è la
  distanza, l'altra l'altezza. Thorik sale per ultimo, e dal Tempio gli fa da
  Ancora Tordek (D87).
- **Tattiche PG**: sincronizzare — Tordek salta e aggancia, Thorik ancora, Artemis
  porta la corda agli altri (Scalare CD 15). Chi scivola deriva piano verso
  l'oceano e ci affonda in 3 round; Artemis ripesca chi è legato al cavo (round
  intero, FOR CD 15). Se non ce la fa, l'oceano lo risputa sulla riva dopo 1d4
  round, a 0 pf e stabile, e il riposo costa −12 h (D84-D85). La Frequenza o il
  Diapason alzano una scala di blocchi (Intrattenere CD 18, 4 prove riuscite):
  con la sola Frequenza arriva a metà strada (DEF-1 §7a).
- **Evoluzione**: il portale ruota (T-1) → tempismo. Entrati, si va a T-5 (Sentinella).
- **Riferimento**: DEF-1 §7a.

## MAPPA T-5 — ANTICAMERA DELLA MAGNETITE: la Sentinella (tattica combat)

```
════════════════════════════════════════════════════════════════════════
 ANTICAMERA DELLA MAGNETITE — esagono Ø 18 m · pareti MAGNETITE (🧲)
════════════════════════════════════════════════════════════════════════
                         N (parete nord)
                 🧲 🧲 🧲 🧲 🧲 🧲 🧲
              🧲 🧲 🧲 [⛓️ THORIK] 🧲 🧲 🧲      ⛓️ = Thorik immobilizzato
            🧲 ⬜ ⬜ [🕸️ ARTEMIS] ⬜ ⬜ 🧲          (metallo incollato alla parete)
          🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲
        🧲 ⬜ ⬜ ⬜ ⬜ 🤖 ⬜ ⬜ ⬜ ⬜ ⬜ 🧲          🤖 = SENTINELLA (centro)
      W 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 E
        🧲 ⬜ ⬜ ⬜ ⬜ 🥋 ⬜ ⬜ ⬜ ⬜ ⬜ 🧲          🥋 = TORDEK (unico in piedi)
          🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲
            🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲            🕸️ = Artemis prono, accanto a
              🧲 🧲 🧲 🚪 🚪 🧲 🧲 🧲            Thorik (gravità 10×)
                         S (porta sigillata)
════════════════════════════════════════════════════════════════════════
LEGENDA · 🧲 pareti di magnetite che incollano chi porta metallo · ⬜ pavimento
(gravità 2×, gestibile SOLO per Tordek) · 🤖 Sentinella di Mithral (160 pf) ·
⛓️ Thorik immobilizzato alla parete · 🕸️ Artemis prono accanto a lui (gravità 10×).
```
- **Tipo / scala**: tattica, esagono Ø 18 m. **Duello forzato** Tordek vs Sentinella.
- **Terreno & altitudini**: pavimento a **gravità 2×** (gestibile solo da Tordek);
  le **pareti di magnetite** 🧲 *attirano il metallo* → chi porta armatura/armi
  metalliche viene **incollato** (Thorik ⛓️) o schiacciato a terra (Artemis 🕸️,
  gravità localizzata 10×, accanto a Thorik). Porta sud **sigillata** fino alla
  vittoria; se Tordek cade, la magnetite si spegne e la porta si riapre.
- **Posizioni**: Sentinella al centro; Tordek unico libero (Bracieri = niente
  metallo che la magnetite prende — o meglio, la controlla). Thorik alla parete N,
  Artemis prono accanto a lui, a N.
- **Tattiche Sentinella (nemico)**: RD 15/adamantio + contundente → **solo i
  Bracieri di Tordek** passano, e i loro colpi sono di contatto (CA 11); il primo
  a segno in un round apre una **crepa**. Alla **prima crepa** entra in
  **Overdrive** (3 attacchi/CA 24); alla **terza crepa** (o a 0 pf) il petto si
  apre → **colpo finale** = **Geode di Smeraldo** + **risveglio pieno dei
  Bracieri** (Fuoco+Terra). Ignora Thorik e Artemis.
- **Tattiche PG**: è **il momento di Tordek** (Shine Time). Thorik può liberarsi
  (FOR CD 25) e da libero può solo Aiutare Tordek (+2 a CA o al tiro per colpire);
  Artemis, prono, non si sposta: con un'azione standard aiuta Thorik (+2 alla FOR)
  o incita Tordek (+2 al prossimo attacco). 3 crepe = vittoria.
- **Evoluzione**: alla sconfitta la magnetite si spegne, la porta S si apre → T-6.
- **Riferimento**: DEF-1 §7b.

## MAPPA T-6 — CAMERA DELL'ALTARE: TERROS L'ANTICO (tattica BOSS · CR 15)

```
════════════════════════════════════════════════════════════════════════
 CAMERA CENTRALE — sfera Ø 60 m · ZERO-G ovunque TRANNE l'ALTARE
 ALTARE 13,5 × 9 m = 9 × 6 quadretti da 1,5 m, angoli smussati
 Vista: piano equatoriale attorno all'Altare (24 col × 16 righe · 1,5 m)
════════════════════════════════════════════════════════════════════════
COL → A B C D E F G H I J K L M N O P Q R S T U V W X
01    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← muro curvo: crash 2d6 solo se sei già a <3 m
02    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
03    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️        ZONA ZERO-G (Ø 60 m)
04    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🔮 Artemis vola qui (Terros −4 vs aria)
05    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
06    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟡🟡🟡🟡🟡🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🟡 bordo di rune: ci finisci con la 1ª spinta
07    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟩🟩🟩🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
08    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟣🟣🟣🥋🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🟣 TERROS (Enorme, 3×3 quadretti)
09    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🛡️🟣🟣🟣🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🛡️ Thorik   🥋 Tordek (sull'Altare)
10    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟣🟣🟣🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
11    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟡🟡🟡🟡🟡🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← ALTARE 13,5 × 9 m (9×6 quadretti) = gravità normale
12    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
13    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
14    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️        Earth Glide: Terros
15    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️        entra/esce dall'Altare
16    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
════════════════════════════════════════════════════════════════════════
LEGENDA · 🟩 Altare calpestabile (grav. normale) · 🟡 bordo/rune smeraldo
🟣 Terros (Enorme, 4,5 m = 3×3) · 🛡️ Thorik · 🥋 Tordek · 🔮 Artemis · 🌫️ ZERO-G
────────────────────────────────────────────────────────────────────────
⚙️ GEOGRAFIA DELLA SPINTA (3 m = 2 quadretti, 1/round — vedi §8 statblock)
  ASSE LUNGO (E-O, 9 quadretti): Terros ne occupa 3, restano 3 per lato.
    La 1ª spinta ti porta sul bordo 🟡; la 2ª ti butta nello zero-G.
  ASSE CORTO (N-S, 6 quadretti): margine 1-2 quadretti. È l'ASSE LETALE:
    di qui una sola spinta ti fa uscire. I giocatori lo imparano al round 2.
  ↳ Questa asimmetria È il posizionamento: tenere il fianco corto verso
    Terros è l'errore che paga il tank.
────────────────────────────────────────────────────────────────────────
DILEMMA DELL'ALTARE (ha DUE lati, non uno):
  SULL'ALTARE  = Earth Mastery +1 per Terros contro di te,
                 MA i due nani hanno +4 di Stabilità contro la Spinta.
  IN ZERO-G    = eviti l'Earth Mastery, MA perdi del tutto la Stabilità
                 (Tordek non resiste più a nessuna spinta) e ti serve volo.
  Artemis in 🌫️ = quasi intoccabile (−4 al boss) = star DPS.
  Terros NON vola: nello zero-G non guarisce, ma il gruppo non ha come
  spingercelo (l'Onda non lo sposta, la spallata non è legale, DEF-1 8c-2b).
────────────────────────────────────────────────────────────────────────
⚠️ QUESTA GRIGLIA È LO STATO DAL ROUND 2 (Altare già centrato). Al round 1
l'Altare è ATTRACCATO alla soglia nord e si stacca col risveglio (§8a-8b).
SCENOGRAFIA (MAP 6): ingresso a NORD = 🚪 SOGLIA di mithral (si apre da sé;
l'Altare vi era ormeggiato). Dopo il distacco: ~27 m di zero-G fra soglia e
Altare — la via di fuga esiste, ma va attraversata in volo o a spinte.
Niente piattaforme laterali: Artemis tira in volo. ALTARE centrale 🟩: lo Smeraldo 💚 LEVITA sopra; alla VITTORIA l'Altare
scende e la gemma diventa raggiungibile (§9). PARETI SFERICHE di cristallo:
vista sul Piano oscuro fuori; aria pura dentro. Acustica: ogni colpo è un tuono.
════════════════════════════════════════════════════════════════════════
@north N
@taglia K8 ; Enorme
@tipo tattica interni
```
- **Tipo / scala**: tattica BOSS, sfera Ø 60 m. **Terros l'Antico, CR 15, 345 pf**.
- **Terreno & altitudini**: **ZERO-G** ovunque (🌫️) tranne l'**Altare** centrale
  (13,5 × 9 m, gravità normale). In zero-G chi non vola si muove solo
  **spingendosi** (linea retta, ½ mov) e combatte a **−4** senza appiglio; contro
  il **muro curvo** subisce **2d6** solo se ci arriva da meno di 3 m. L'Altare è
  l'unico terreno «solido».
- **Posizioni dal round 2** (Altare già centrato): Terros 🟣 sull'Altare (K08-M10,
  3×3); Thorik 🛡️ (J09) e Tordek 🥋 (N08) sull'Altare; Artemis 🔮 in volo nella
  zona zero-G. Al round 1 l'Altare è ancora attraccato alla soglia nord.
- **Tattiche Terros (nemico — soglie & giro, DEF-1 §8)**: **345 pf**; a **260** usa
  **Scudo di Geodi** (+4 CA, no critici); a **172** si ritira sull'Altare e
  **rigenera 15/round** a contatto con la pietra; a **0** si sbriciola → **Smeraldo**.
  Giro (3.5, 1 azione/round): full-attack 2 schianti +33 (2d10+12 + Push FOR 25) ·
  **Onda Gravitazionale** (ricarica 1d4: tutti "cadono" 9 m, Rifl 22) · **Stalattiti**
  (ricarica 5-6: 8d6 raggio 9 m) · **Earth Glide** dentro/fuori l'Altare. **−4 vs
  chi vola**; **sonico ×1,5**.
- **Contro-momenti PG (add-on)**: Artemis (azione preparata) **disintegra le
  stalattiti** (contatto CA 12) ed è lo **star DPS** dall'alto (sfrutta sonico);
  Tordek **frantuma lo Scudo** con >15 danni sonici → Terros frastornato; Thorik lo
  **inchioda** con una prova di FOR contro CD 25 statica (DEF-1 §8), impedendo
  l'Earth Glide.
  ⚠️ Se hanno saltato i Cristalli (T-3): niente Frequenza/Diapason → Terros a piena
  forza, nessun round di nausea.
- **Evoluzione**: a 0 pf → Rituale dello Smeraldo (§9, sinergia di tutti, emerge Durik).
- **Riferimento**: DEF-1 §8-§9.

---

# DEF-2 · RITORNO ALLA SALA & AFFRESCHI

## MAPPA S-1 — LA SALA DELLA FORGIA ETERNA (ottagono, 8 affreschi · hub)

```
════════════════════════════════════════════════════════════════════════
 SALA DELLA FORGIA ETERNA — ottagono Ø 40 m (26 quadretti) · soffitto 15 m
 Zona SICURA · Altare centrale · Portale P1 a NORD (→ Stanza della Corona)
════════════════════════════════════════════════════════════════════════
                          NORD  ▼  [P1 → Stanza Corona]
              ┌───────────[ A1 «L'Alba del Mondo» ]───────────┐
             ╱   (statico · Moradin forgia la Corona)          ╲
      [ A2 ]╱                                                    ╲[ A3 ]
   «4 Eroi» │        🔲 col.mithral (nord)                       │ «Visione»
   (→80%)   │                                                    │ (Thorik)
            │                    ✦ (*) spawn PG                  │
     OVEST  │   🔲col        ╔══════════════╗          🔲col     │  EST
   [ A4 ]───┤  (adam.)       ║   ALTARE     ║        (adam.)     ├───[ A5 ]
   «Fuoco»  │                ║  CUORE DI    ║                    │ «Terra»
   CHIUSO   │                ║   MORADIN    ║                    │ →«Forza
            │                ║  🔥 Forgia   ║                    │ Sostenuta»
            │                ╚══════════════╝                    │ (si chiude)
            │        † corpo di Hella · Therysol · Durik         │
            │                 🔲 col.adam. (sud)                 │
      [ A6 ]╲                                                    ╱[ A7 ]
   «Tempo»   ╲                                                  ╱ «Hammerfist»
   (→80%,    ╲                                                 ╱  LIVE ⏳3g20h
   portale)   └───────────[ A8 «Ritorno Trionfale» ]──────────┘  +Aegis Bane
                          SUD  ▲   (vuoto → 60%)
════════════════════════════════════════════════════════════════════════
LEGENDA · A1-A8 affreschi 8×5 m (vetro indistruttibile) · 🔲 colonne sacre
(1 mithral N, 3 adamantio) · ╔╗ Altare 2×2 m + Forgia Eterna · (*) spawn ·
† corpo di Hella accanto all'Altare, lato sud `[CANONE — DM 2026-10-18, G2-09]`,
vegliato da Therysol (davanti ad A8 solo per la manifestazione) · Durik fra il corpo e il pericolo · [P1] portale
sempre aperto.
```
- **Tipo / scala**: hub scenico (Cronaca Vivente), ottagono Ø 40 m. Zona **sicura**.
- **Terreno & altitudini**: pavimento piano; **Altare** centrale rialzato con la
  **Forgia Eterna**; 8 affreschi 8×5 m alle pareti (vetro indistruttibile); soffitto
  15 m. Distanze: spawn→Altare 6 m; bordo dell'Altare→parete ≈19 m (20 m dal
  centro; Ø 40 m).
- **Posizioni notevoli**: † **corpo di Hella** accanto all'**Altare**, sul lato
  sud, dove Therysol lo veglia da giorni (DEF-2 §2); il corpo si gira verso sud. I PG lo
  portano davanti ad **A8** solo per la manifestazione (DEF-2 §4), poi torna
  all'Altare per il rito (R-1/DEF-3). **Durik**, mosso dalla giocatrice di
  Hella, non ha una casella fissa: sta sempre fra il corpo e ciò che sente come
  pericolo, e se lo si allontana torna indietro. **Cuore di Moradin**
  sull'Altare (usato in DEF-3).
- **Ambiente dinamico (la Sala HA REGISTRATO la Terra — mostralo)**: **A4** (Fuoco)
  chiuso · **A5** (Terra) si chiude → «Forza Sostenuta» · **A2** al 80% (la 4ª
  figura, Hella, prende contorno) · **A6** (Tempo) 80%, il portale pulsa · **A8**
  60% · **A7** (Hammerfist) LIVE ⏳~3g20h all'arrivo + Aegis Fang Bane vs Fauci.
- **Tattiche/uso PG**: è a Thorik (Corona) che gli affreschi «reagiscono» (A3
  Moradin gira la testa). Un solo sacro attivo per volta (Benedizione della
  Cronaca, no stacking).
- **Riferimento**: DEF-2 (Cronaca Vivente); resurrezione = R-1/DEF-3.

## MAPPA S-2 — LA STANZA DELLA CORONA DI ADAMANTIO (santuario in purificazione)

> **Geometria CANONICA** (invariata dall'incontro giocato di ARC-06):
> `06_Stanza-corona-di-adamantio/StanzaCoronaDiAdamantio/Tactics_and_maps.md` — stessi
> posizionamenti di trono, muro, colonne, statue, alcove, macerie e ingresso.
> Qui è mostrata nello **stato ARC-07** (santuario in purificazione, DEF-2).

```
════════════════════════════════════════════════════════════════════════
 STANZA DELLA CORONA — 15 m × 19,5 m (10 col × 13 righe · 1,5 m/quadretto)
 NORD in alto (trono/muro) · ingresso a SUD (righe basse) · ora SANTUARIO
════════════════════════════════════════════════════════════════════════
@north S
COL →   A  B  C  D  E  F  G  H  I  J
13     ⬜ 🗿 🗿 📜 🌀 📜 🗿 🗿 ⬜ ⬜   NORD · 📜 PARETE della CRONACA · 🌀 portale, dietro
12     🔲 ⬜ 🔲 ⬜ 👑 👑 ⬜ 🔲 ⬜ 🖼️   👑 TRONO E-F12, vuoto · 🖼️ Dipinti Invisibili
11     🔲 ⬜ 🔲 ⬜ ✝️ ⬜ ⬜ 🔲 🪨 🖼️   ✝️ E11 = dove sedeva Belkram (ARC-06) · 🪨 macerie
10     🔲 ⬜ 🔲 ⬜ ⬜ ⬜ ⬜ 🔲 ⬜ ⬜   B10 = ex nascondiglio Yochlol 2
09     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜   H09 = ex nascondiglio Yochlol 1
08     🗿 ⬜ 🔲 ⬜ ⬜ ⬜ 🔲 ⬜ 🗿 ⬜
07     ⬜ 🪨 ⬜ ⬜ ⬜ ⬜ ⬜ 🪨 ⬜ ⬜   🪨 macerie (terreno difficile ×2)
06     🗿 ⬜ 🔲 ⬜ ⬜ ⬜ 🔲 ⬜ 🗿 ⬜
05     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
04     ⬜ ⬜ 🔲 ⬜ ⬜ ⬜ 🔲 ⬜ ⬜ ⬜
03     ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
02     🏰 🏰 🏰 🚪 🚪 🚪 🏰 🏰 🏰 🏰   🚪 INGRESSO sud D-F02, nel muro sud della navata
01     🏰 🏰 🏰 ⬜ ⬜ ⬜ 🏰 🏰 🏰 🏰   SUD · androne D-F01 verso la Sala della Forgia
════════════════════════════════════════════════════════════════════════
LEGENDA · ⬜ pavimento (ora pulito) · 🏰 roccia del muro sud · 🔲 colonne parallele (copertura +4 CA,
spezzano la linea di vista) · 🗿 statue di Moradin (deturpate in ARC-06 → in
restauro) · 🗿 in B13/H13/A08/I08 = alcove-nicchie (statue del culto
deturpate, in restauro); in C13/G13/A06/I06 = statue dei re · 🪨 macerie
(terreno difficile) · 📜 muro dietro il trono = ora PARETE della CRONACA
(le incisioni-specchio) · 🌀 portale drow SIGILLATO (nascosto dal 📜;
inerte dalla caduta di Urialle) · 👑 trono vuoto: la Corona è di Thorik ·
🖼️ Dipinti Invisibili (J11-J12, come in ARC-06) · ✝️ postazione di Belkram
(ARC-06) · 🚪 ingresso sud, collegamento P1 ↔ Sala della Forgia.
@tipo tattica interni
```
- **Tipo / scala**: hub scenico specchio, 10×13 (15×19,5 m), 1,5 m/quadretto.
  La navata utile è A-J/03-13 (15 × 16,5 m): la porta D-F02 sta nel muro sud
  e dà sull'androne D-F01.
  <!-- storico -->Dal 2026-10-21 il pavimento è ⬜ (⬛ è solo muratura piena) e la porta
  sta in un muro; nessuna posizione canonica è cambiata.<!-- /storico -->
  Ora **santuario sicuro** (Consacrare) — il *desecrate* di ARC-06 è dissolto.
- **Terreno & luce**: pavimento pulito; macerie 🪨 (B07/H07/I11) = terreno
  difficile; colonne 🔲 e statue 🗿 = copertura +4. La luce viola-verde delle
  torce drow è **sostituita** dalla luce calda del Portale: illuminazione
  normale (niente miss chance).
- **Posizioni notevoli (INVARIATE da ARC-06)**: trono **E-F12**; muro dietro il
  trono **D-F13** (durezza 8, 360 pf/3 m, Spezzare CD 35) → ora vi si incide la
  **Cronaca** («La Seconda Gemma», la sagoma-druida che si riempie, DEF-2 §6);
  **portale drow E13** dietro il muro, **sigillato e inerte**; Dipinti
  Invisibili **J11-J12** (porta chiusa, DEF-2 §4-bis); ingresso **D-F02**
  (sud). Reliquia nascosta sotto il dais del trono (Cercare CD 22, DEF-2 §10).
- **Memoria del luogo (regia)**: qui sedeva Belkram (✝️ E11) col worg, qui
  cadde **Hella** (ARC-06). I muschi e le ragnatele drow **seccano** sulle
  macerie e nelle alcove (la purificazione avanza a vista, sessione dopo
  sessione). Chi posa la mano sull'incisione della druida e ne dice il nome
  sente la **pietra CALDA** (DEF-2 §6).
- **Evoluzione**: ogni beat dell'arco aggiunge una riga alla Parete della
  Cronaca (specchio della Sala S-1). A resurrezione avvenuta, la sagoma-druida
  è **piena**.
- **Riferimento**: geometria = `06_.../Tactics_and_maps.md`; stato = DEF-2 §6/§10.

---

# DEF-3 · LA RESURREZIONE DI HELLA

## MAPPA R-1 — IL CERCHIO DEL RITO (Altare del Cuore di Moradin · rituale)

```
════════════════════════════════════════════════════════════════════════
 IL CERCHIO DEL RITO — al centro della Sala della Forgia (ottagono, DEF-2)
 Cerchio rituale Ø 6 m (raggio 3 m) attorno all'Altare · Sud lasciato VUOTO
════════════════════════════════════════════════════════════════════════
                          NORD  ▼
                        🛡️ THORIK
                    (Corona + Aegis Fang)
                   Conoscenze relig. CD 15
                           │ 3 m
                   ╔═══════╧═══════╗
   🔮 ARTEMIS      ║   🟡 ALTARE   ║      🥋 TORDEK
   (Ring, UMD 18)  ║  († Hella,    ║   (ki, Concentr. 20)
   OVEST ── 3 m ───╢   3 semi:     ╟─── 3 m ── EST
                   ║  🌰 fronte    ║
                   ║ 🌰 sx  dx 🌰  ║
                   ╚═══════╤═══════╝
                           │
                    (SUD = VUOTO)
                  ← da qui fluisce l'energia →
                  ← e QUI, allo Step 5, appare
                    ✦ LA CUSTODE DELLE RADICI (§6)
                          SUD  ▲
════════════════════════════════════════════════════════════════════════
LEGENDA · 🟡 Altare 2×2 m + Cuore di Moradin (posato sul cuore di Hella) ·
† corpo di Hella (supino) · 🌰 3 semi (mano sx / mano dx / fronte: triangolo
inscritto nel cerchio) · 🛡️ Thorik (N) · 🥋 Tordek (E) · 🔮 Artemis (O), tutti
a 3 m dal centro: con il SUD vuoto (energia + soglia della Custode) fanno una
croce. Therysol veglia ai margini (testimone, non officiante).
```
- **Tipo / scala**: rituale scenico (cerchio Ø 6 m nella Sala S-1). Zona **sacra e
  sicura** — ma la posta è emotiva/spirituale, non combat.
- **Terreno & posizioni**: 3 officianti a N, E e O, a 3 m dal centro
  dell'Altare (Tordek e Artemis alla sua altezza, come Thorik a nord): con il
  Sud vuoto fanno una croce. I **3 semi** (🌰 fronte + 2 mani) sul corpo di
  Hella formano un triangolo inscritto nel cerchio dei tre officianti; il **Cuore di Moradin** 🟡
  sull'Altare. **SUD lasciato VUOTO**: da lì fluisce l'energia e, allo Step 5,
  **appare la Custode delle Radici** (psicopompo, §6). Therysol testimone ai margini.
- **Ruoli/prove**: Thorik = Conoscenze (religioni) CD 15; Tordek = Concentrazione
  CD 20 (ki); Artemis = UMD 18 (Ring). Chi officia **non può fare altro** durante
  gli step (6 step corali).
- **Add-on grigio (Debito della Radice, §6)**: la Custode esige un pegno per il
  vuoto nel Sogno della Terra → 3 risposte (accettare servizio / rifiutare→il
  vuoto risale / offrire Durik come ponte). Registrato in state.md §7.
- **Evoluzione**: successo → Hella si risveglia **Ibrido Treant**, Durik si lega.
- **Riferimento**: DEF-3 (rito, §6, §7-bis).

---

# DEF-4 · IL VIAGGIO A ≈372 DR

## MAPPA M7-A — HAMMERFIST ≈372 DR: fortezza, campo dell'orda, mura (strategica)

```
════════════════════════════════════════════════════════════════════════
 HAMMERFIST ≈372 DR — vista strategica (non in scala; il duello è su M7-B)
════════════════════════════════════════════════════════════════════════
                       NORD ▲  la montagna: dentro, le sale scendono (M7-S)
   ⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️
        ╔════════════ 🔔 torre nord, +120 ═══════╗
        ║  fucina originale · la statua del re    ║  ← Zona 1: HAMMERFIST GIOVANE
        ║  CORTILE INTERNO, +100 → M7-B (duello)  ║     mura bianche, sicura
        ╚═══ porta e targa ════════ postierla ▫ 🗼╝  ← Zona 3: mura all'alba
              ╲ rampa finale ┊          scale ▲▲▲ ┊⇣    🌲🌲🌲🌲 BOSCO A EST
        ░░░░░░ SPIANATA DEGLI ARIETI, +80 ░░░░░░   ┊⇣    🌲 ✦ portale, ~500 m
                ╲╱╲╱ strada a tornanti ╲╱╲╱        ┊⇣    🌲🌲🌲🌲 (Scene 1-2)
   · · · · · · · · · piana dell'orda, quota 0 · · ┊ · · ·  ← le tende da 500 m
   ⛺🔥⛺   ⛺⛺🔥    ⛺🔥⛺    🔥⛺⛺   ⛺🔥⛺   ┊
   GP1▪   i clan degli orchi, a gruppi   ▪GP2 ┊  ← Zona 2: MARE DI TENDE
   ⛺🔥⛺ ┏━━━━━━━━━━━┳━━━━━━━━━━━┓ ⛺🔥⛺ ◄┘  via dei PG: fianco est, poi da nord
   🔥⛺⛺ ┃ ▪▪ ▪▪ ▪▪  ┃  ▪▪ ▪▪ ▪▪ ┃ ⛺⛺🔥      ⚔️ ZOG'TAR + 4 guardie (Sc. 8, M7-C)
   ⛺⛺🔥 ┣━━━━ ╔═══╩═══╗ ━━━━━┫ 🔥⛺⛺      ~1 km di cammino: cinque blocchi
   ⛺🔥⛺ ┃ ▪▪ ▪▪ ║COMANDO║ ▪▪ ▪▪ ┃ ⛺🔥⛺      👤 VATORE fra le tende (Sc. 9)
   🔥⛺⛺ ┗━━━━━━━━━━━┻━━━━━━━━━━━┛ ⛺⛺🔥
   GP3▪   ⛺🔥⛺   (10.000 dormono)   ⛺🔥⛺ ▪GP4
                       SUD ▼  oltre il campo: le colline, dove dorme il drago
────────────────────────────────────────────────────────────────────────
 IL PROFILO, NORD → SUD (le quote del DM, sulla piana dell'orda)
  +120 m ┌──┐ torre nord, la porta che entra nella montagna
         │  │
  +100 m ┘  └─────────────┐ porta e targa
           cortile, M7-B  │
                           ╲ rampa finale, 20 m
   +80 m                    ╲────────────────┐ spianata degli arieti
                                              ╲ strada a tornanti
                                               ╲___
                                                   ╲___
     0 m                                               ╲__ piana · ⛺🔥⛺ · COMANDO
         ├── dal ciglio, giù per i tornanti: circa 500 m ──┤ le tende, fino a 1 km ──┤
 La via dei PG non è questa sezione: dalla postierla (+100) giù per il
 fianco est, 100 m di dislivello, lungo il lato est del campo fino alla
 tenda, a circa 1 km di cammino; all'alba si risale lo stesso fianco.
────────────────────────────────────────────────────────────────────────
LEGENDA · ⛰️ montagna · 🏰╔╗ mura bianche, nuove · 🔔 campane · 🗼 torre est ·
▫ postierla · ░ la spianata, nuda · ╲ la rampa finale [INFERRED — needs DM
confirmation] e i tornanti · ▲ scale d'assedio sul tratto est · ⇣ la discesa
del fianco est · ⛺🔥 i clan degli orchi, tende a gruppi attorno al fuoco
della banda (copertura) · ▪▪ le lance hobgoblin, quattro tende attorno al
fuoco, ad anello attorno al capo · ━ le vie battute · ▪GP posti di guardia · ╔╗
la tenda del comando, sola nel suo spiazzo · ┊◄ la via dei PG · 👤 Vatore ·
⚔️ scontro · ✦ arrivo del portale.
Skullcrusher entra dall'alto sul cortile interno → M7-B.
════════════════════════════════════════════════════════════════════════
```
- **Tipo / scala**: strategica (infiltrazione + orientamento). Non è una griglia
  di combattimento; il duello è su M7-B.
- **Orientamento** (D44, 2026-10-08): nord in alto, la montagna. La fortezza
  ci si appoggia; porta principale e **postierla** sono nel muro sud, la
  postierla all'angolo sud-est sotto la torre est. Il campo dell'orda sta a sud,
  il bosco a est: il portale lascia i PG lì, a circa 500 m dalle mura (Scena 1).
  I PG escono dalla postierla, scendono per il fianco est della montagna (100 m
  di dislivello), costeggiano il lato est del campo e arrivano alla tenda del
  comando da nord, dalla parte della fortezza.
- **Le quote** `[CANONE — DM 2026-10-22, thread di ARC-08]`: la piana dell'orda, con
  il campo e la tenda M7-C, è a quota 0. La spianata nuda davanti alla porta,
  dove battono gli arieti, è un ripiano a **+80 m** e fa parte di questa
  mappa. La porta principale e il cortile del duello (M7-B) sono a **+100 m**,
  la torre nord con la porta che entra nella montagna a **+120 m**. Le tende
  stanno fra 500 m e 1 km dalle mura, e dalla spianata alla piana si scende
  per una strada a tornanti. Il profilo sotto la pianta le mette in fila. La
  quota sul mare il DM non l'ha data: le direttive di M7-B e M7-C mettono la
  piana a 870 m, come le mappe del 1372 di ARC-08 (cortile del duello a 970 m, che nel 1372 è il cortile interno) `[INFERRED — needs DM confirmation]`.
- **La rampa della porta** `[INFERRED — needs DM confirmation]`. Gli arieti
  stanno sulla spianata, a +80, e la porta è a +100: dall'una all'altra sale una rampa
  di terra battuta e pietra, larga quanto un ariete e lunga circa 150 m,
  addossata al gradone sotto il muro sud. Gli arieti si montano sulla spianata
  e si spingono su per la rampa, sotto il tiro del camminamento, fino al
  battente. Le scale d'assedio sul fronte sud non arrivano, perché lì le mura
  stanno sul ciglio, 24,5 m sopra la spianata: salgono sul tratto est, dove il
  fianco della montagna arriva al piede delle mura. È il camminamento est di
  Hrodgar (DEF-4 Scena 10).
- **La torre nord** `[INFERRED — needs DM confirmation]`. Sta sul gradone di
  +120, sopra il muro nord del cortile: su M7-B la riga 04 è il piede della
  roccia, S04 la base della torre e della sua scala, che sale di 20 m dentro
  la pietra. La porta di O-P04 entra nella montagna al livello del cortile,
  verso la sala del consiglio (M7-S).
- **Gli altri tempi.** Nel −1000 Hammerfist è più piccola e ha meno gradoni.
  Nel 1372 il ripiano di +80 diventa il cortile esterno con il cancello: è
  materia di ARC-08.
- **Terreno & zone**: **Zona 1** = Hammerfist giovane (mura bianche, sicura, arrivo
  del portale) · **Zona 2** = **mare di tende** dell'orda (10.000 dormono; le tende
  = copertura): fuori i clan degli orchi, a gruppi di ripari attorno al fuoco
  della banda; al centro il campo del capo, senza recinto, con le lance
  hobgoblin a gruppi attorno ai fuochi e lo spiazzo del comando (M7-C) · **Zona 3** = mura all'alba con la **breccia** ▓. **Posti di
  guardia** GP1-GP4 ai margini.
- **Posizioni notevoli**: **Tenda del Comando** (Zog'tar Deatheye, GS 15, + 4
  guardie hobgoblin, Guerriero 8) al centro delle tende; **Vatore** (§5, il futuro Sal) tra le
  tende — incontro grigio col villain prima che sia villain; **Re Thorek I** nella
  Sala del Trono (Zona 1).
- **Tattiche PG (infiltrazione, skill challenge «Mare di Nemici»)**: muoversi di
  copertura in copertura (tende), evitare/neutralizzare i GP; tabella d6 di
  complicazioni (pattuglie, lupi, hobgoblin) in DEF-4 Scena 6. Fallire → allarme
  (l'orda si sveglia). Scelta se affrontare Zog'tar (Scena 8, mappa M7-C) o aggirarlo.
- **Evoluzione**: raggiunto il cortile all'alba → **Skullcrusher** entra dall'alto → M7-B.
- **Riferimento**: DEF-4 Scene 2-9; la tenda del comando è la mappa M7-C (`ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md`).

## MAPPA M7-B — L'ARENA DEL DUELLO: SKULLCRUSHER IL NERO (tattica BOSS · GS 14)

```
════════════════════════════════════════════════════════════════════════
 CORTILE INTERNO — 36 m × 27 m (24 col × 18 righe · 1,5 m) · cielo aperto
 Nord in alto, la montagna. Skullcrusher entra da V1 (~45 m) e picchia. PG dalla riga 16.
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️⚫☁️☁️   Skullcrusher in quota, circa 45 m (V1)
02    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️   zona aerea: serve volo o gittata
03    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️
04    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🚪🚪🏰🏰🗼🔔🏰🏰🏰🏰   mura +4,5 m · O-P porta alla montagna · S torre nord, T campane
05    🏰⬛🏮🏮⬛🟫🟫🟫🟫🟫🟫🗿🗿⬜⬜⬜🟫🟫🟫🟫🟫🟫🟫🏰   B-E fucina originale (C-D forgia) · L-M la statua del re
06    🏰⬛🟫🟫🪨🪨🟫🟫🟫🟫⬜⬜⬜⬜🟫🟫🟫🪨🪨🟫🟫🟫🟫🏰   macerie: copertura +4 CA
07    🏰🟫⚒🟫🟫🟫🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰   C l'incudine del rito (Scena 12)
08    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🟫🟫🟦🟫🟫🟫🏰   T il pozzo: sotto c'è la cisterna
09    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⚔⚔⚔🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰   impronta del drago, 4,5 m
10    🏰🏗🟫🟫🟫🟫🟫🟫🟫🟫⚔⚔⚔🟫🟫🟫🟫🟫🟫🟫🟫🟫🏗🏰   B e W le gru: dal camminamento la corda scende qui
11    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⚔⚔⚔🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
12    🏰🟫🟫🟫🪨🪨🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🪨🪨🟫🟫🟫🟫🏰   macerie: copertura +4 CA
13    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
14    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
15    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬜⬜🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
16    🏰🟫🟫🔵🟫🟫🔵🟫🟫🟫🟫⬜⬜🟫🟫🟫🔵🟫🟫🔵🟫🟫🟫🏰   i 4 PG
17    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🔵⬜🟫🟫🟫🟫🟫🟫🟫🟫🟫⬜🏰   Re Thorek I, alle spalle dei PG
18    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🚪🚪🏰🏰🏰🏰🏰🏰🏰🏰🏰🚪🗼   L-M porta principale (la targa) · W postierla · X torre est
════════════════════════════════════════════════════════════════════════
LEGENDA · ☁️ zona aerea (serve volo o gittata) · ⚫ Skullcrusher · ⚔ impronta
d'atterraggio del drago (Enorme) · 🟫 cortile · ⬜ il selciato dalla porta
principale alla statua, alla porta della montagna e alla postierla ·
🪨 macerie (copertura +4) ·
🏰 mura e camminamenti (+4,5 m, arcieri nani) · 🔵 PG e Re Thorek I ·
⬛🏮 la fucina originale e la sua forgia · ⚒ l'incudine del rito · 🗿 la statua
del re · 🟦 il pozzo sulla cisterna · 🏗 gru con le corde · 🗼 torri · 🔔 campane.
@north N
@mark 1 ; V1 ; Skullcrusher (quota ~45 m)
@mark 2 ; D16 ; Thorik
@mark 3 ; G16 ; Tordek
@mark 4 ; L17 ; Re Thorek I (8 pf se la Scena 10 è andata male)
@mark 5 ; Q16 ; Artemis
@mark 6 ; T16 ; Hella, con Durik accanto
@mark 7 ; C5 ; La fucina originale, accesa da stanotte
@mark 8 ; T8 ; Il pozzo sulla cisterna
@mark 9 ; T4 ; Le campane della torre nord
@mark 10 ; W18 ; La postierla
@mark 11 ; U16 ; Durik, accanto a Hella
@mark 12 ; W2 ; Wyvern 1, di scorta: entra dal round 2
@mark 13 ; X2 ; Wyvern 2, di scorta: entra dal round 2
@tipo tattica esterno
@luogo Hammerfist ≈372 DR, il cortile interno e la porta principale
@quota 970 m ; s.l.m. [INFERRED — needs DM confirmation: il DM dà la piana a 0; qui è a 870 m, come nel 1372 di ARC-08]
@dislivello +100 m ; sulla piana dell'orda, a sud
```
- **Tipo / scala**: tattica BOSS, 24×18. **Skullcrusher il Nero, GS 14** (capostipite
  di Fauci di Palude). Cielo aperto.
- **Quota** `[CANONE — DM 2026-10-22]`: il cortile e la porta stanno a **+100 m** sulla
  piana dell'orda, la torre nord a +120 (M7-A, «Le quote»). Dal camminamento
  sud si guarda giù: la spianata degli arieti 20 m più in basso, nuda, e oltre
  il ciglio la piana, 100 m sotto, con le tende fino all'orizzonte.
- **Terreno & altitudini**: **zona aerea** ☁️ (righe 01-03, quota; il drago vi resta:
  serve **volo o gittata**); **camminamenti +4,5 m** 🏰 (arcieri nani, copertura e
  altezza); **macerie** 🪨 (copertura +4 CA) al suolo; **impronta d'atterraggio** ⚔
  (dove il drago Enorme si posa se scende).
- **Cosa c'è nel cortile** (la tabella «IL CORTILE» della Scena 11, sulla
  griglia dal 2026-10-08, lotto D28): la **fucina originale** a B-E05, con la
  forgia accesa a C-D05, che è la prima forgia della fortezza (D45); davanti,
  l'**incudine del rito** a C07 (Scena 12); il **pozzo** a T08, sopra la
  cisterna; le **campane** della torre nord a T04; le due **gru** a B10 e W10,
  con le corde che scendono dal camminamento; la **statua del re** a L-M05 (la
  sola, Scena 3); la **porta principale** con la targa a L-M18, la **postierla**
  a W18 sotto la torre est (D44); la porta che entra nella montagna a O-P04.
  Distanze utili: dall'impronta del drago (K-M 09-11) la forgia è a ~12 m, il
  pozzo a ~10 m. **Le gru non sono alla pari**: il gancio arriva a 15 m contando
  la quota; da B10 il bordo dell'impronta è a 13,5 m in piano, quindi il gancio
  prende il drago posato o a un paio di metri d'altezza; da W10 è già a 15 m in
  piano, e il gancio arriva solo se il drago picchia verso il muro est.
- **Nel 1372** (D46, D48): questo cortile è il nucleo del cortile interno di
  ARC-08 (D46), ingrandito nei secoli; la statua del re è la **statua del Re
  Antenato** di H3-1, e il tunnel di fuga dietro di lei viene scavato dopo il
  372. La griglia del 1372 è H3-1 (`08_.../Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`).
- **Posizioni iniziali**: PG a riga 16 (Thorik D16, Tordek G16, Artemis Q16, Hella
  T16, con Durik accanto a U16); **Re Thorek I** alle loro spalle, a L17.
  Sono le posizioni di riferimento: le sceglie il tavolo, e se non le sceglie
  sfalsale su due righe, perché una linea di 30 m lungo la riga 16 li prende tutti.
  Skullcrusher a V1, quota ~45 m: il soffio è una linea
  di 30 m, quindi al round 1 prima scende entro 30 m dai PG (movimento), poi
  soffia (azione standard). Le 2 wyvern di scorta (W2, X2) entrano dal round 2
  (Scena 11, sidebar di scala). I Treant dell'alba, se uno viene richiamato,
  entrano dalla porta principale L-M18.
- **Tattiche Skullcrusher (nemico — dilemma centrale)**: **NON vuole atterrare** (in
  cielo è un dio): soffio d'acido in picchiata, poi risale. A terra è vulnerabile al
  **full-attack** ma devastante. **Meccanica «la Forgia ricorda le ferite»**: ogni
  ferita inferta qui si riporta su **Fauci di Palude** nel 1372 (carry-over B4).
- **Tattiche PG**: **costringerlo giù** — Artemis in volo lo tormenta, **Aegis Fang
  scagliata** (cicatrice d'ala → B4), tiri dai camminamenti; oppure colpirlo
  dall'alto. Proteggere Re Thorek I (se la Scena 10 chiude con 0-1 successi, è a 8 pf). 3 esiti aperti.
- **Evoluzione**: alla vittoria il **Rubino si accende** (D5/D16) → ritorno (CM-1/DEF-5).
- **Riferimento**: DEF-4 Scena 11 (+ carry-over B4).

---

# DEF-5 · IL RITORNO A HAMMERFIST (1372)

## MAPPA CM-1 — IL CUORE DELLA MONTAGNA (arrivo & apparizione · Incontro 3B)

> **Geometria CANONICA** (invariata): `08_.../Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
> **MAPPA 5** (master vivo; il Lotto-3-FINALE è la generazione storica dello
> stesso contenuto). Caverna-cattedrale **100 m × 80 m × 40 m** di altezza.
> ⚠️ **Scala 3 m/quadretto** [deviazione A4 dalla convenzione 1,5 m: griglia
> originale disegnata così; NON ridisegnata per non alterare posizioni/portate
> già usate nel testo. Dal 2026-10-22 è dichiarata vista d'insieme
> (`@tipo strategica`): le miniature si muovono sulla carta **CM-2**, qui
> sotto, a 1,5 m. Non mischiare quadretti di mappe a scale diverse.]

```
════════════════════════════════════════════════════════════════════════════════
 IL CUORE DELLA MONTAGNA — caverna sacra 100 m × 80 m (33 col × 27 righe · 3 m)
 Soffitto 40 m (stalattiti bioluminescenti) · Giorno 3 dell'assedio (1372)
════════════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g
01    ⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰🏰🚪🚪🏰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰  ← 🚪 PORTA DI MITHRAL 6×6 m (P-Q01, unico ingresso)
02    ⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰🟤🟤🟤🔴🔴🔴🔴🟤🟤🟤⛰⛰🟤🟤⛰⛰⛰⛰⛰⛰⛰⛰  ← 🔴 ondata nemica in corso (entra dalla porta)
03    ⛰⛰⛰⛰🟤🟤🟤🟤🟤⛰🟤🟤🟤🟤🟤🔴🔴🟤🟤🟤🟤🟤⛰🟤🟤🟤🟤⛰⛰⛰⛰⛰⛰
04    ⛰⛰⛰🟤🔺🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🔺⛰⛰⛰⛰  ┐
05    ⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰  │
06    ⛰🟤🟤🟤🟤🟤🟤🟤🔵🔵🟤🟤🟤🔵🔵🔵🔵🔵🔵🟤🟤🟤🔵🔵🟤🟤🟤🟤🟤🟤🟤⛰⛰  │
07    ⛰🟤🟤🟤🟤🟤🟤🔵🔵🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🔵🔵🟤🟤🟤🟤🟤🟤⛰⛰  │ 🔵 SCHIERAMENTO
08    ⛰⛰🟤🟤🟤🟤🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵🔵🟤🟤🟤🟤🟤⛰⛰  │ dei 90 NANI
09    ⛰⛰⛰🟤🟤🟤🔵🔵🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🔵🔵🟤🟤🟤🟤⛰⛰⛰  │ (a 30 m dall'altare,
10    ⛰⛰🔺🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰  │  rivolto alla porta:
11    ⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰  │  centro pesante e
12    ⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰  │  due ali piegate;
13    ⛰🟨🟨🔺🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⭐✨🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔺🟨🟨🟤⛰  │  60+20+10)
14    ⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⚫⭐🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰  │
15    ⛰🔺🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔺🟤⛰  │ ⭐ ALTARE DI MORADIN
16    ⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰  │ (P-Q 13-14 · Ø 6 m,
17    ⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰  │  +3 m, basalto+rune oro)
18    ⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰  │ ⚫ RE THOREK (8 pf)
19    ⛰⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰⛰  │ ✨ SFERA DORATA (R8 · breve: porte)
20    ⛰⛰⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰  │
21    ⛰⛰⛰🔺🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔺🟤⛰⛰  │
22    ⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰  │
23    ⛰⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰  │
24    ⛰⛰⛰🟤🟤🔺🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰⛰  ┘
25    ⛰⛰⛰⛰⛰🟤🟤🟤🟤🟤🟤⛰🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔺⛰⛰⛰⛰⛰⛰
26    ⛰⛰⛰⛰⛰⛰⛰⛰🟤🟤⛰⛰⛰🟤🟤🟤🟤🟤🟤⛰⛰🟤🟤🟤⛰⛰⛰⛰⛰⛰⛰⛰⛰
27    ⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰
════════════════════════════════════════════════════════════════════════════════
LEGENDA · 🟤 pavimento di caverna · ⛰ roccia viva, le pareti della caverna ·
🏰 la muratura ai lati della porta · 🚪 porta di mithral 6×6 m (P-Q01,
nord — unico ingresso; ward difensivi collassati) · 🗿 10 STATUE dei Re
Ancestrali (cerchio a 20 m dall'altare, alte 4 m, occhi di rubino — copertura) ·
🔵 90 nani (schierati a 30 m, rivolti alla porta) · ⭐⚫✨ altare +3 m con Re Thorek e sfera (la
sfera compare in tutte e due le regie: al Round 8 nella lunga, quando le porte
cedono nella breve; i PG non sono segnati: compaiono sull'altare, P-Q 13-14) ·
🟨 piattaforme laterali Est/Ovest (+1,5 m, 6×3 m — tiratori) · 🔺 stalagmiti
(copertura parziale) · 🔴 ondata nemica, alla porta. I due orchi scossi che
restano dopo l'aura non sono segnati: sono già dentro lo schieramento, fra i nani e
l'altare (DEF-5 Scena 2). Soffitto 40 m: stalattiti di cristallo
BIOLUMINESCENTI (luce piena ovunque, niente *darkness*).
@north N
@tipo strategica caverna
@luogo Hammerfist, il Cuore della Montagna (sotto la fucina grande, livello −3)
@quota −150 m ; sotto il cortile di Hammerfist (livello 0) [INFERRED — needs DM confirmation]
@dislivello +3 m ; l'altare sul pavimento della caverna; le piattaforme laterali +1,5 m
```

### ⏫ EVENTO CLIMAX — L'APPARIZIONE (la sfera dorata)

```
                    [SOFFITTO 40 m]
                    🌟🌟🌟🌟🌟🌟🌟🌟   stalattiti bioluminescenti
                           │  (round 6-7: la sfera si forma e SCENDE lenta)
                           ▼
                      ✨✨✨✨✨
                    ✨  SFERA   ✨
                   ✨   DORATA   ✨   ← Ø 3 m · TRICOLORE
                    ✨ oro·verde ✨      (Topazio+Smeraldo+Rubino)
                      ✨·rosso✨
                           │
                           ▼  ROUND 8 (breve: le porte cedono): ESPLOSIONE DI LUCE
                      💥💥💥💥💥
                           │
                           ▼
                      ⭐ ALTARE ⭐  (+3 m)
                         ⚫ Re Thorek (8 pf → occhi che si aprono)
              [4 SILHOUETTE EMERGONO]
         🛡️ Thorik   🥋 Tordek   🔮 Artemis   🌙 Hella
              💫 I RUMBLING STONES SONO ARRIVATI 💫
```

- **Tipo / scala**: santuario + epic reveal (Incontro **3B**, il CLIMAX della
  Sessione 3 dell'ARC-08; lato ARC-07 = DEF-5 Scene 1-2). **3 m/quadretto**.
- **Terreno & altitudini**: altare **+3 m** (P-Q 13-14, basalto nero, rune
  d'oro); piattaforme laterali **+1,5 m** (B-C13 ovest, d-e13 est — posizioni
  sopraelevate per tiratori, stalagmiti 🔺 = copertura parziale); soffitto
  **40 m** — le stalattiti possono **crollare** su effetti ad area potenti
  (Terremoto ecc.): 4d6 contundenti, raggio 3 m, **Riflessi CD 18** annulla.
- **Posizioni**: **90 nani** schierati a 30 m, rivolti alla porta (al centro, davanti al varco, 40 guerrieri su quattro file di scudi con dietro 12 balestrieri e 6 capi; ai lati due ali piegate all'indietro verso l'altare, ciascuna di 10 guerrieri, 4 balestrieri e 2 capi `[CANONE — DM 2026-10-30]`) + **Re Thorek** ⚫ sull'altare,
  critico a 8 pf, l'acido che lo consuma finché l'Apparizione non lo ferma,
  cosciente a occhi chiusi, incapace di combattere; Madre Dana in ginocchio su
  di lui); **10
  statue** 🗿 sul cerchio a 20 m (Q07·U09·W12·W16·U19·Q21·M19·K16·K12·M09);
  nemici dalla **porta nord** P-Q01.
- **Le ondate (Incontro 3B — se giocato per intero, lato ARC-08)**:
  | Round | Ondata | Note tattiche |
  |---|---|---|
  | 1-2 | **30 Orchi berserker** | carica sconsiderata porta→altare |
  | 3-5 | **20 Hobgoblin sergenti** | muro di scudi, **immuni a paura**, tengono impegnati i nani (nella regia breve entrano dopo l'aura, che quindi non li tocca comunque) |
  | 6-8 | **15 Bugbear assassini** | Nascondersi +12, puntano i capi e Re Thorek — **interrotti dall'Apparizione** |
  | 9-10 | **Grimjaw + 10 Orog** (se vivo) | vede il ribaltone: ritirata strategica O sfida personale a Thorik; se già morto → capitano minore, auto-ritirata |
- **⏱️ Timing dell'Apparizione (due regie valide)**: giocando il **3B completo**
  (lato ARC-08, coi PNG giocabili Borin/Dara/Thorin/Nala; nella regia breve
  sono fra i dieci capi al centro, e non parlano) i PG appaiono al
  **Round 8**, nel mezzo dell'ondata 3; giocando **solo il lato ARC-07**
  (DEF-5 Scena 2, arrivo compresso) appaiono nell'istante in cui le porte cedono.
  Stessa scena, stesso altare: cambia solo quanto assedio si gioca prima.
- **Effetti immediati dell'Apparizione**: nani **+6 morale** (da −4 a +2),
  guariscono **2d8 pf**, **immuni a paura 1 h**; nemici **Volontà CD 25**: chi
  fallisce è in panico e fugge, chi fa 20 è scosso (D38);
  Re Thorek apre gli occhi (riconosce Thorik: la Corona risuona); gli **occhi di
  rubino delle 10 statue si ACCENDONO** (benedizione ancestrale); i PG hanno un
  **round di sorpresa**.
- **Transizione**: da PNG giocabili → veri PG. Poi pulizia (DEF-5 Scena 3, doppia
  modalità) → portale di Dana → bastioni (ARC-08, `ARC08-11-PONTE-ARRIVO.md`).
- **Riferimento**: geometria/ondate = Atlante-08 **MAPPA 5**; regia lato ARC-07
  = DEF-5 Scene 1-3; cucitura = ARC08-11.

### MAPPA CM-2 — IL LATO NORD DEL CUORE (la pulizia · Scena 3, combattimento completo)

> **Carta tattica a 1,5 m** dello stesso spazio di CM-1: il lato nord della
> caverna, dalla porta di mithral all'altare, 42 m × 48 m. Si gioca qui il
> 🎚️ [COMBATTIMENTO COMPLETO] della Scena 3. CM-1 resta la vista d'insieme,
> a 3 m, per sapere dove stanno i blocchi dei nani e da dove arrivano le ondate.
> Ogni quadretto di CM-1 vale due per due quadretti di CM-2: la statua Q07
> di CM-1 è la O-P 13-14 di CM-2, l'altare P-Q 13-14 è la M-P 25-28.
> Bracieri 🏮, caduti 🦴 e le punte di roccia di un quadretto lungo la parete
> nord sono dettagli della carta a 1,5 m, che la vista a 3 m non disegna.

```
════════════════════════════════════════════════════════════════════════════════
 CM-2 · IL CUORE DELLA MONTAGNA, LATO NORD — 42 m × 48 m (28 col × 32 righe · 1,5 m)
 La pulizia (Scena 3): dalla porta all'altare · Giorno 3 dell'assedio (1372)
════════════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b
01    ⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰🏰🏰🟤🟤🟤🟤🏰🏰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰  ← il varco della porta di mithral (M-P 01-02, 6 m)
02    ⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰🏰🏰🟤🟤🟤🟤🏰🏰⛰⛰⛰⛰⛰⛰⛰⛰⛰⛰
03    ⛰⛰⛰⛰⛰🟤🟤🟤🟤🟤🟤🟤🪨🟤🟤🪨🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰⛰⛰  ← 🪨 i battenti abbattuti (M03, P03)
04    ⛰⛰⛰⛰🟤🟤🟤🟤🟤🟤🟤🦴🟤🟤🦴🟤🟤🟤🟤🟤🟤🟤🟤🟤⛰⛰⛰⛰
05    ⛰⛰⛰🟤🟤🟤🟤🟤🟤🦴🟤🟤🦴🟤🟤🟤🦴🟤🟤🦴🟤🟤🟤🟤🟤⛰⛰⛰
06    ⛰⛰🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤⛰⛰  ┐ 🔵 lo schieramento dei nani, a 30 m dall'altare
07    🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤  │ (centro: 40 guerrieri, 12 balestrieri, 6 capi;
08    🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤  ┘  ali: 10+4+2 ciascuna; il DM le muove a blocchi)
09    🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤
10    🟤🟤🟤🟤🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🦴🔵🔵🔵🔵🟤🟤🟤🟤
11    🟤🟤🟤🟤🔵🔵🔵🔵🦴🟤🟤🔵🔵🔵🔵🦴🔵🟤🟤🟤🔵🔵🔵🔵🟤🟤🟤🟤
12    🟤🟤🟤🟤🔵🔵🔵🔵🟤🟤🟤🟤🦴🟤🟤🟤🟤🟤🟤🟤🔵🔵🔵🔵🟤🟤🟤🟤
13    🟤🟤🟤🟤🦴🔵🔵🔵🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤🔵🔵🔵🦴🟤🟤🟤🟤  ← 🗿 la statua Q07 della CM-1 (O-P 13-14)
14    🟤🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤
15    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔴🔴🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤  ← 🔴 i due orchi scossi (L15, M15)
16    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
17    🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤
18    🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿🟤🟤🟤🟤
19    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
20    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
21    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
22    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
23    🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿
24    🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿
25    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⭐🔵🔵⭐🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤  ← ⭐ altare +3 m (M-P 25-28) · 🔵 i PG
26    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🔵⭐⭐🔵🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤  ← il re e Dana (N-O 26-27)
27    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⭐⭐⭐⭐🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
28    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤⭐⭐⭐⭐🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
29    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
30    🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤🏮🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤
31    🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿
32    🟤🟤🗿🗿🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🟤🗿🗿
════════════════════════════════════════════════════════════════════════════════
LEGENDA · 🟤 pavimento di caverna · ⛰ roccia viva, la parete nord della caverna
LEGENDA · 🏰 la muratura ai lati del varco della porta
LEGENDA · 🪨 battenti di mithral abbattuti (terreno difficile, copertura ½)
LEGENDA · 🦴 i caduti dei primi due round, orchi e nani (terreno difficile)
LEGENDA · 🗿 statue dei Re Ancestrali su basi di 3 m, alte 4 m (copertura totale)
LEGENDA · 🏮 bracieri su treppiede (copertura ½, luce 9 m)
LEGENDA · ⭐ l'altare, Ø 6 m, alto 3 m: si sale con Scalare CD 15 in un round
LEGENDA · 🔵 i PG sull'altare e lo schieramento dei nani · 🔴 i due orchi scossi
LEGENDA · Gli hobgoblin entrano dal varco M-P 01 alla fine del round 1 della pulizia.
LEGENDA · I bordi est, ovest e sud sono tagli: la caverna continua (vedi CM-1).
════════════════════════════════════════════════════════════════════════════════
@north N
@tipo tattica caverna
@luogo Hammerfist, il Cuore della Montagna (lato nord, dalla porta all'altare)
@deroga struttura/senza-anelli ; caverna aperta: si gira attorno all'altare e alle statue, che sono isole nel vuoto, non blocchi di muro
@deroga m1/copertura ; la caverna è una cattedrale vuota: le sole coperture sono statue, bracieri e lo schieramento dei nani, ed è voluto
@deroga m2/vuoto ; lo spazio fra lo schieramento e l'altare è la terra di nessuno che gli hobgoblin devono attraversare
@deroga m4/esposizione ; luce piena dalle stalattiti e nessun muro interno: chi corre verso l'altare è visto da tutti
```

- **Distanze**: dal varco della porta al bordo dell'altare 33 m, 22 quadretti;
  dallo schieramento dei nani al centro dell'altare 30 m; dai due orchi scossi al
  bordo dell'altare 13,5 m, 9 quadretti. Gli hobgoblin, 6 m di velocità in
  armatura pesante, correndo coprono 18 m a round: la regia dei round della
  Scena 3 resta quella scritta.
- **Come si entra e come si gira**: il varco della porta è a nord; i bordi
  est, ovest e sud sono tagli della carta, e la caverna continua oltre (CM-1).
  Si gira attorno all'altare e alle statue; chi sale sull'altare (Scalare CD
  15) ha la quota di 3 m.
- **Chi c'è al primo round della pulizia**: i PG sull'altare, il re e Dana al
  centro; lo schieramento dei nani a nord; i due orchi scossi fra lo schieramento e l'altare.
  Gli hobgoblin non ci sono ancora: entrano dal varco alla fine del round 1.

---

## NOTA DI RESA (futuro)
Queste 12 mappe sono la **fonte ASCII canonica**. La resa a pergamena SVG a
fedeltà piena (senza perdere annotazioni/posizioni/token) è il task
`plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md` (F5 = passata ARC-07). Fino ad
allora si stampa direttamente l'ASCII ultra-clear di questo Atlante.
