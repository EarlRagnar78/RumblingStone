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
> (T-2, T-3, T-6, S-2, M7-B, CM-1) sono **rese a pergamena SVG** in
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
| **T-3** | Campo dei Cristalli Viventi (skill + Varis) | DEF-1 §6/§6-bis | tattica/skill | ✅ |
| **T-4** | Tempio di Mithral: salto gravitazionale | DEF-1 §7a | sezione/co-op | ✅ |
| **T-5** | Anticamera della Magnetite: la Sentinella | DEF-1 §7b | tattica combat | ✅ |
| **T-6** | Camera dell'Altare: **TERROS L'ANTICO** | DEF-1 §8 | tattica BOSS | ✅ |
| **S-1** | Sala della Forgia Eterna (8 affreschi) | DEF-2 | hub/scenica | ✅ |
| **S-2** | Stanza della Corona (purificata) | **geometria canonica ARC-06**: `06_.../CoronaDiAdamantio/Tactics_and_maps.md` + stato DEF-2 | hub/scenica | ✅ |
| **R-1** | Il Cerchio del Rito (resurrezione) | DEF-3 | rituale/scenica | ✅ |
| **M7-A** | Hammerfist ≈372 DR (fortezza & orda) | DEF-4 | strategica | ✅ |
| **M7-B** | L'Arena del Duello: **SKULLCRUSHER** | DEF-4 | tattica BOSS | ✅ |
| **CM-1** | Il Cuore della Montagna (1372, arrivo) | **geometria canonica ARC-08**: Atlante-Hammerfist **MAPPA 5** (⚠️ scala 3 m) + regia DEF-5 | scenica/climax 3B | ✅ |

> Rese SVG storiche (ancora valide, stanze «prima visita»): `Portale-Forgia-L1`
> (Stanza Corona/Belkram, Sala Forgia), `Portale-Forgia-L2` (colonna-K, Forgia
> Adamantina). Non sostituiscono le mappe-beat qui sopra: sono un'altra fase.

## 📑 INDICE
- **DEF-1 · Piano della Terra**: T-1 · T-2 · T-3 · T-4 · T-5 · T-6
- **DEF-2 · Ritorno & Affreschi**: S-1 · S-2
- **DEF-3 · Resurrezione**: R-1
- **DEF-4 · Viaggio a ≈372 DR**: M7-A · M7-B
- **DEF-5 · Ritorno a Hammerfist**: CM-1

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
   │ cristallo│ o  │  │ (30-60 m)    ▓ 💠 ▓ (Skill+    ~~ (grigia) ~~ │TEMPIO
   │  ◎ ◎ ◎   │ n  ╲  ╱ [XORN×3:      ▓▓▓   Varis)      50 m sopra ▲  │MITHRAL
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
  Fang, che vibra verso il Tempio (EST). Varis: la sua runa è al Campo (T-3).
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
01    🟫 🟫 🔷 🔷 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🔷 🔷 🟫 🟫 🟫 🟫
02    🟫 🔷 🔷 🔷 🟫 🟫 🕳️ 🟫 🟫 🟫 🟫 🟫 🔷 🔷 🔷 🟫 🟫 🟫
03    🟫 🔷 🔷 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🔷 🔷 🟫 🟫 🟫
04    🟫 🟫 🟫 🟫 🟫 🛡️ 🟫 🟫 🔮 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫
05    🟫 🟫 🟫 🟫 🟫 🟫 🥋 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🕳️ 🟫 🟫 🟫
06    🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫
07    🟫 🔷 🔷 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🔷 🔷 🟫 🟫
08    🟫 🔷 🔷 🟫 🟫 🟫 💠 🟫 🟫 🟫 🟫 🟫 🟫 🔷 🔷 🔷 🟫 🟫
09    🟫 🟫 🔷 🟫 🟫 🟫 ⬛ 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🔷 🟫 🟫 🟫
10    🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫
════════════════════════════════════════════════════════════════════════
LEGENDA · 🔷 Cristallo Gigante (copertura totale, indistruttibile) · 🟫 roccia
frastagliata (terreno difficile) · 🕳️ punto d'emersione Xorn · ⬛ Fauci di
Diamante (élite) · 💠 base corrosa del pilastro (crolla → ponte) · 🛡️ Thorik
(F04) · 🔮 Artemis (I04) · 🥋 Tordek (G05).
```
- **Tipo / scala**: tattica, 18×10, 1,5 m. Combattimento d'imboscata.
- **Terreno & altitudini**: tutto **terreno difficile** (movimento ×2) + gravità
  2× → il party è LENTO; i cristalli 🔷 danno **copertura totale**
  (indistruttibili). Il pilastro corroso 💠 (G08) può essere fatto **crollare**
  (→ ponte o area bloccata).
- **Posizioni iniziali**: Thorik F04, Artemis I04, Tordek G05. **Xorn 1** emerge
  a G02, **Xorn 2** a O05 (🕳️); **Fauci di Diamante** (élite, 180 pf) attende a
  G09 (⬛), sotto il pilastro.
- **Tattiche Xorn (nemico, round-per-round)**: Earth Glide → **emergono, colpo
  pieno (3 artigli + morso), riaffondano** con **azione preparata** — NON restano
  2 round in superficie (colpiscili solo quando sono fuori). Fauci di Diamante a
  90 pf **si rifugia nel cristallo** (+4 CA) e tende un altro agguato.
- **Tattiche PG**: bersagliare gli Xorn *nel round in cui emergono* (readied);
  usare i cristalli come copertura contro il caster; far crollare 💠 per
  intrappolare la Fauci. Artemis in volo evita il terreno difficile.
- **Evoluzione**: se i PG demoliscono/negoziano (3 vie, §5), lo scontro cambia:
  demolizione = crolli, ordine = tregua, negoziato = Diplomazia (Terran) CD 18.
- **Riferimento**: DEF-1 §5.

## MAPPA T-3 — CAMPO DEI CRISTALLI VIVENTI + SEME DI VARIS (skill challenge)

```
════════════════════════════════════════════════════════════════════════
 CAMPO DEI CRISTALLI VIVENTI — 30 m × 12 m (20 col × 8 righe · 1,5 m)
 GRAVITÀ 2×   ·   ingresso da OVEST (A), uscita a EST (T)
════════════════════════════════════════════════════════════════════════
COL →  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T
01    🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️ 🌫️
02    🟫 🟫 💠 🟫 💚 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🟫 🟫
03    🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🟫
04    🟫 🟫 💠 🟫 💠 🟫 💠 🟫 💠 💎 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🟫 🟫
05    🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🔴 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🟫
06 →  🚪 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🚪
07    🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💚 🟫 💠 🟫 🟫
08    🟫 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 💠 🟫 🟫 🟫
════════════════════════════════════════════════════════════════════════
LEGENDA · 💠 Cristallo Vivente (canta) · 💎 Madre Cristallo (J04, alt. 5 m) ·
💚 crepato (riforgiabile → +2, E02 e O07) · 🔴 runa di Varis (J05; l'Anello di
Artemis la capta ≤6 m) · 🌫️ vuoto/gravità laterale (non attraversare) ·
⬜ corridoio libero (riga 06, ingresso/uscita) · 🟫 suolo.
```
- **Tipo / scala**: skill challenge (6 successi / 3 fallimenti) + gancio
  personale di Artemis (Seme di Varis). Non è un combat.
- **Terreno & altitudini**: campo di cristalli cantanti; la **Madre Cristallo**
  (💎 J04) è a **5 m di quota**; riga 06 è il **corridoio sicuro**; sopra riga 01
  è **vuoto laterale** (🌫️, gravità a 90° — non attraversare).
- **Posizioni notevoli**: 2 cristalli **crepati** (💚 E02, O07) → riforgiabili
  (bonus +2 alla vulnerabilità sonora di Terros). **Runa di Varis** 🔴 a J05 —
  l'Anello la capta entro 6 m (aggancio §6-bis).
- **Prove (CD)**: Sapienza Magica / Intrattenere (canto) / Artigianato (gemme) /
  Concentrazione, CD 15-22 (DEF-1 §6). Riforgiare un cristallo = Artigianato CD
  20 → +2. Analizzare/estirpare il Seme di Varis = Sapienza Magica CD 20.
- **Tattiche PG**: distribuire le prove sui punti forti; NON toccare i cristalli
  sani a caso (dissonanza → −2). Artemis decide sul Seme (avidità vs lealtà, §6-bis).
- **Evoluzione**: 6 successi → il coro «benedice» il party (vulnerabilità sonora
  di Terros armata). 3 fallimenti → dissonanza (1d6 sonico, niente bonus).
- **Riferimento**: DEF-1 §6 e §6-bis.

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
             │          │      [dopo aver colpito le Rune di Attracco]
   ~~~~~~~~~~┴~~~~~~~~~~~┴~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   ~~~~~~~~~~ OCEANO DI ROCCIA (grigia, liquida-ma-cede) ~~~~~~~~~~~~~~~~
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
════════════════════════════════════════════════════════════════════════
```
- **Tipo / scala**: sezione verticale co-op (puzzle di gravità), non combat.
- **Terreno & altitudini**: il **Tempio-cubo** fluttua **50 m sopra** l'Oceano di
  Roccia e ha **gravità propria** (i corridoi ruotano 90° ogni 20 m). Sotto:
  Oceano di Roccia (semiliquido, cede — chi cade affonda lento, non muore subito).
- **Ruoli/posizioni**: **Tordek** = navigatore (Saltare CD 25 + Rune di Attracco);
  **Thorik** = ancora (FOR CD 20 tiene il cavo); **Artemis** = traghettatore (vola
  col cavo). A ~20 m la gravità del Tempio cattura chi salta → "cade" verso il portale.
- **Tattiche PG**: sincronizzare — Tordek salta e aggancia, Thorik ancora, Artemis
  porta la corda agli altri (Scalare CD 15). Fallire il salto = caduta nell'Oceano
  (recuperabile, costa tempo).
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
            🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲            (metallo incollato alla parete)
          🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲
        🧲 ⬜ ⬜ ⬜ ⬜ 🤖 ⬜ ⬜ ⬜ ⬜ ⬜ 🧲          🤖 = SENTINELLA (centro)
      W 🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲 E
        🧲 ⬜ ⬜ ⬜ ⬜ 🥋 ⬜ ⬜ ⬜ ⬜ ⬜ 🧲          🥋 = TORDEK (unico in piedi)
          🧲 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🧲
            🧲 ⬜ ⬜ [🕸️ ARTEMIS] ⬜ ⬜ 🧲          🕸️ = Artemis prono/indifeso
              🧲 🧲 🧲 🚪 🚪 🧲 🧲 🧲            (gravità 10×)
                         S (porta sigillata)
════════════════════════════════════════════════════════════════════════
LEGENDA · 🧲 pareti di magnetite LETALI per chi porta metallo · ⬜ pavimento
(gravità 2×, gestibile SOLO per Tordek) · 🤖 Sentinella di Mithral (160 pf) ·
⛓️ Thorik immobilizzato alla parete · 🕸️ Artemis prono (gravità 10×).
```
- **Tipo / scala**: tattica, esagono Ø 18 m. **Duello forzato** Tordek vs Sentinella.
- **Terreno & altitudini**: pavimento a **gravità 2×** (gestibile solo da Tordek);
  le **pareti di magnetite** 🧲 *attirano il metallo* → chi porta armatura/armi
  metalliche viene **incollato** (Thorik ⛓️) o schiacciato a terra (Artemis 🕸️,
  gravità localizzata 10×). Porta sud **sigillata** fino alla vittoria.
- **Posizioni**: Sentinella al centro; Tordek unico libero (Bracieri = niente
  metallo che la magnetite prende — o meglio, la controlla). Thorik alla parete N,
  Artemis prono a S.
- **Tattiche Sentinella (nemico)**: RD 15/adamantio + contundente → **solo i
  Bracieri di Tordek** passano; a **80 pf** entra in **Overdrive** (3 attacchi/CA
  24); a **0** il petto si apre → **colpo finale** = **Geode di Smeraldo** +
  **risveglio pieno dei Bracieri** (Fuoco+Terra). Ignora Thorik/Artemis (immobili).
- **Tattiche PG**: è **il momento di Tordek** (Shine Time). Thorik può liberarsi
  (FOR CD 28) per aiutare; Artemis, se si spoglia del metallo, striscia fuori dalla
  gravità localizzata. 3 crepe = guscio infranto.
- **Evoluzione**: alla sconfitta la magnetite si spegne, la porta S si apre → T-6.
- **Riferimento**: DEF-1 §7b.

## MAPPA T-6 — CAMERA DELL'ALTARE: TERROS L'ANTICO (tattica BOSS · CR 15)

```
════════════════════════════════════════════════════════════════════════
 CAMERA CENTRALE — sfera Ø 60 m · ZERO-G ovunque TRANNE l'Altare (6 m)
 Vista: piano equatoriale attorno all'Altare (24 col × 16 righe · 1,5 m)
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← muro curvo: crash 2d6 se spinti (Push)
02    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
03    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️      ZONA ZERO-G
04    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🔮 Artemis vola qui (Terros −4 vs aria)
05    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
06    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟡🟡🟡🟡🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🟡 = bordo Altare (rune smeraldo)
07    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟩🟩🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
08    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟩⬛⬛🟩🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← ⬛ = TERROS (init: sull'Altare)
09    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟩⬛⬛🟩🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️
10    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🛡️🟩🟩🟩🥋🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← 🛡️Thorik  🥋Tordek (sull'Altare)
11    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟩🟩🟩🟩🟩🟩🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
12    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🟡🟡🟡🟡🟡🟡🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️   ← ALTARE Ø 6 m = gravità normale
13    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
14    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️      Earth Glide: Terros
15    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️      entra/esce dall'Altare
16    🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️🌫️
════════════════════════════════════════════════════════════════════════
LEGENDA · 🟩 Altare calpestabile (grav. normale) · 🟡 bordo/rune smeraldo
⬛ Terros (Enorme, 4,5 m) · 🛡️ Thorik · 🥋 Tordek · 🔮 Artemis · 🌫️ ZERO-G
DILEMMA: sull'Altare = Earth Mastery +1 per Terros MA stabilità e no-Onda-in-
aria; in zero-G = eviti Earth Mastery MA Push ti sbatte al muro (2d6) e ti
serve volo/Equilibrio. Artemis in 🌫️ = quasi intoccabile (−4 boss) = star DPS.
Terros NON vola: tienilo in zero-G → perde la rigenerazione e fatica.
────────────────────────────────────────────────────────────────────────
SCENOGRAFIA (MAP 6): ingresso a NORD = 🌉 PONTE DI CRISTALLO (45 m; 50% crolla
se Terros usa un colpo sismico → caduta 15 m, taglia la ritirata: non sostarci).
PIATTAFORME LATERALI 🟦 a EST e OVEST (+3 m, scale): posizioni di tiro per
Artemis. ALTARE centrale 🟩: lo Smeraldo 💚 LEVITA sopra; alla VITTORIA l'Altare
scende e la gemma diventa raggiungibile (§9). PARETI SFERICHE di cristallo:
vista sul Piano oscuro fuori; aria pura dentro. Acustica: ogni colpo è un tuono.
════════════════════════════════════════════════════════════════════════
```
- **Tipo / scala**: tattica BOSS, sfera Ø 60 m. **Terros l'Antico, CR 15, 345 pf**.
- **Terreno & altitudini**: **ZERO-G** ovunque (🌫️) tranne l'**Altare** centrale
  (Ø 6 m, gravità normale). In zero-G chi non vola si muove solo **spingendosi**
  (linea retta, ½ mov) e combatte a **−4** senza appiglio; spinto contro il **muro
  curvo** subisce **2d6** (crash). L'Altare è l'unico terreno «solido».
- **Posizioni iniziali**: Terros ⬛ sull'Altare (L08-M09); Thorik 🛡️ (J10) e Tordek
  🥋 (N10) sull'Altare; Artemis 🔮 in volo nella zona zero-G.
- **Tattiche Terros (nemico — soglie & giro, DEF-1 §8)**: **345 pf**; a **260** usa
  **Scudo di Geodi** (+4 CA, no critici); a **172** si ritira sull'Altare e
  **rigenera 15/round** a contatto con la pietra; a **0** si sbriciola → **Smeraldo**.
  Giro (3.5, 1 azione/round): full-attack 2 schianti +30 (2d10+10 + Push FOR 25) ·
  **Onda Gravitazionale** (ricarica 1d4: tutti "cadono" 9 m, Rifl 22) · **Stalattiti**
  (ricarica 5-6: 8d6 raggio 9 m) · **Earth Glide** dentro/fuori l'Altare. **−4 vs
  chi vola**; **sonico ×1,5**.
- **Contro-momenti PG (add-on)**: Artemis (azione preparata) **disintegra le
  stalattiti** (contatto CA 12) ed è lo **star DPS** dall'alto (sfrutta sonico);
  Tordek **frantuma lo Scudo** con >15 danni sonici → Terros frastornato; Thorik lo
  **inchioda** (FOR vs Lotta +40, con Aiuto+Benedizione) impedendo l'Earth Glide.
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
            │                                                    │
            │                 🔲 col.adam. (sud)                 │
      [ A6 ]╲                                                    ╱[ A7 ]
   «Tempo»   ╲   († corpo di Hella — vegliato da Therysol)      ╱ «Hammerfist»
   (→80%,    ╲                                                 ╱  LIVE ⏳3g18h
   portale)   └───────────[ A8 «Ritorno Trionfale» ]──────────┘  +Aegis Bane
                          SUD  ▲   (vuoto → 60%)
════════════════════════════════════════════════════════════════════════
LEGENDA · A1-A8 affreschi 8×5 m (vetro indistruttibile) · 🔲 colonne sacre
(1 mithral N, 3 adamantio) · ╔╗ Altare 2×2 m + Forgia Eterna · (*) spawn ·
† corpo di Hella (davanti ad A8) · [P1] portale sempre aperto.
```
- **Tipo / scala**: hub scenico (Cronaca Vivente), ottagono Ø 40 m. Zona **sicura**.
- **Terreno & altitudini**: pavimento piano; **Altare** centrale rialzato con la
  **Forgia Eterna**; 8 affreschi 8×5 m alle pareti (vetro indistruttibile); soffitto
  15 m. Distanze: spawn→Altare 6 m; Altare→parete 15 m.
- **Posizioni notevoli**: † **corpo di Hella** davanti ad **A8** (per la
  manifestazione, aggancio a R-1/DEF-3). Therysol veglia. **Cuore di Moradin**
  sull'Altare (usato in DEF-3).
- **Ambiente dinamico (la Sala HA REGISTRATO la Terra — mostralo)**: **A4** (Fuoco)
  chiuso · **A5** (Terra) si chiude → «Forza Sostenuta» · **A2** al 80% (la 4ª
  figura, Hella, prende contorno) · **A6** (Tempo) 80%, il portale pulsa · **A8**
  60% · **A7** (Hammerfist) LIVE ⏳~3g18h + Aegis Fang Bane vs Fauci.
- **Tattiche/uso PG**: è a Thorik (Corona) che gli affreschi «reagiscono» (A3
  Moradin gira la testa). Un solo sacro attivo per volta (Benedizione della
  Cronaca, no stacking).
- **Riferimento**: DEF-2 (Cronaca Vivente); resurrezione = R-1/DEF-3.

## MAPPA S-2 — LA STANZA DELLA CORONA DI ADAMANTIO (santuario in purificazione)

> **Geometria CANONICA** (invariata dall'incontro giocato di ARC-06):
> `06_Stanza-corona-di-adamantio/CoronaDiAdamantio/Tactics_and_maps.md` — stessi
> posizionamenti di trono, muro, colonne, statue, alcove, macerie e ingresso.
> Qui è mostrata nello **stato ARC-07** (santuario in purificazione, DEF-2).

```
════════════════════════════════════════════════════════════════════════
 STANZA DELLA CORONA — 15 m × 19,5 m (10 col × 13 righe · 1,5 m/quadretto)
 NORD in alto (trono/muro) · ingresso a SUD (righe basse) · ora SANTUARIO
════════════════════════════════════════════════════════════════════════
@north S
COL →   A  B  C  D  E  F  G  H  I  J
13     ⬛ 🗿 🗿 📜 🌀 📜 🗿 🗿 ⬛ ⬛   NORD · 📜 muro→PARETE della CRONACA · 🌀 portale drow SIGILLATO (dietro)
12     🔲 ⬛ 🔲 ⬛ 👑 👑 ⬛ 🔲 ⬛ 🖼️   👑 TRONO (E-F12, VUOTO: la Corona è di Thorik) · 🖼️ Dipinti Invisibili
11     🔲 ⬛ 🔲 ⬛ ✝️ ⬛ ⬛ 🔲 🪨 🖼️   ✝️ E11 = dove sedeva Belkram (ARC-06) · 🪨 macerie
10     🔲 ⬛ 🔲 ⬛ ⬛ ⬛ ⬛ 🔲 ⬛ ⬛   B10 = ex nascondiglio Yochlol 2
09     ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛   H09 = ex nascondiglio Yochlol 1
08     🗿 ⬛ 🔲 ⬛ ⬛ ⬛ 🔲 ⬛ 🗿 ⬛
07     ⬛ 🪨 ⬛ ⬛ ⬛ ⬛ ⬛ 🪨 ⬛ ⬛   🪨 macerie (terreno difficile ×2)
06     🗿 ⬛ 🔲 ⬛ ⬛ ⬛ 🔲 ⬛ 🗿 ⬛
05     ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
04     ⬛ ⬛ 🔲 ⬛ ⬛ ⬛ 🔲 ⬛ ⬛ ⬛
03     ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛
02     ⬛ ⬛ ⬛ 🚪 🚪 🚪 ⬛ ⬛ ⬛ ⬛   🚪 INGRESSO (D-F02, sud · collegamento P1 ↔ Sala della Forgia)
01     ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛ ⬛   SUD
════════════════════════════════════════════════════════════════════════
LEGENDA · ⬛ pavimento (ora pulito) · 🔲 colonne parallele (copertura +4 CA,
spezzano la linea di vista) · 🗿 statue di Moradin (deturpate in ARC-06 → in
restauro) · 🗿 in B13/H13/A08/I08 = alcove-nicchie (statue del culto deturpate, in restauro); in C13/G13/A06/I06 = statue dei re · 🪨 macerie (terreno difficile) · 📜 muro dietro il
trono = ora PARETE della CRONACA (incisioni-specchio, DEF-2 §6) · 🌀 portale
drow SIGILLATO (dietro il muro; inerte dalla caduta di Urialle) · 👑 trono
vuoto · 🖼️ Dipinti Invisibili (J11-J12, come in ARC-06) · ✝️ postazione di
Belkram (ARC-06) · 🚪 ingresso sud.
```
- **Tipo / scala**: hub scenico specchio, 10×13 (15×19,5 m), 1,5 m/quadretto.
  Ora **santuario sicuro** (Consacrare) — il *desecrate* di ARC-06 è dissolto.
- **Terreno & luce**: pavimento pulito; macerie 🪨 (B07/H07/I11) = terreno
  difficile; colonne 🔲 e statue 🗿 = copertura +4. La luce viola-verde delle
  torce drow è **sostituita** dalla luce calda del Portale: illuminazione
  normale (niente miss chance).
- **Posizioni notevoli (INVARIATE da ARC-06)**: trono **E-F12**; muro dietro il
  trono **D-F13** (durezza 8, 360 pf/3 m, Spezzare CD 35) → ora vi si incide la
  **Cronaca** («La Seconda Gemma», la sagoma-druida che si riempie, DEF-2 §6);
  **portale drow E13** dietro il muro, **sigillato e inerte**; Dipinti
  Invisibili **J11-J12**; ingresso **D-F02** (sud). Reliquia nascosta sotto il
  trono (Osservare CD 22, DEF-2 §10).
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
                           │
         🔮 ARTEMIS ───────┼─────── 🥋 TORDEK
         (Ring, UMD 18)    │        (ki, Concentr. 20)
      OVEST                │                        EST
                   ╔═══════╪═══════╗
                   ║   🟡 ALTARE   ║   🟡 = Cuore di Moradin
                   ║  († Hella,   ║        (posato sul cuore di Hella)
                   ║   3 semi:    ║   † = corpo di Hella (supino)
                   ║  🌰 fronte   ║   🌰 = seme (mano sx / mano dx / fronte)
                   ║ 🌰 sx  dx 🌰 ║        → triangolo inscritto nel cerchio
                   ╚═══════╪═══════╝
                           │
                    (SUD = VUOTO)
                  ← da qui fluisce l'energia →
                  ← e QUI, allo Step 5, appare
                    ✦ LA CUSTODE DELLE RADICI (§6)
                          SUD  ▲
════════════════════════════════════════════════════════════════════════
LEGENDA · 🟡 Altare 2×2 m + Cuore di Moradin · † corpo di Hella · 🌰 3 semi
(triangolo) · 🛡️ Thorik (N) · 🥋 Tordek (E) · 🔮 Artemis (O) · SUD vuoto
(energia + soglia della Custode).
```
- **Tipo / scala**: rituale scenico (cerchio Ø 6 m nella Sala S-1). Zona **sacra e
  sicura** — ma la posta è emotiva/spirituale, non combat.
- **Terreno & posizioni**: 3 officianti ai vertici N/E/O di un triangolo inscritto;
  i **3 semi** (🌰 fronte + 2 mani) sul corpo di Hella; il **Cuore di Moradin** 🟡
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
   NORD ▲  ╔══════════════════════════════════════════════╗
          ║   🏰🏰🏰  HAMMERFIST GIOVANE (mura bianche)  🏰🏰🏰 ║  ← Zona 1 (sicura)
          ║   🏰  [Sala del Trono: Re Thorek I]  [Fucina]  🏰 ║     arrivo del portale
          ║   🏰🏰  ═══ camminamenti ═══  BRECCIA▓▓  🏰🏰🏰🏰 ║  ← Zona 3 (mura, alba)
          ╚════════════════▲▲▲═══════════════▲▲▲═════════════╝
                    scale d'assedio / arieti ↑ (l'orda preme)
   ~~~~~~~~~~~~~~~~~~~~~~~ CORTILE INTERNO (arena del duello → M7-B) ~~~~~~~~~
          ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺  ← Zona 2: MARE DI TENDE
   GP1▪   ⛺⛺⛺  ╔═══════════╗  ⛺⛺⛺   👤VATORE (§5, tra le tende)  ▪GP2
          ⛺⛺  ║ TENDA DEL  ║  ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺
          ⛺⛺  ║  COMANDO   ║  ⛺⛺  ⚔️ZOG'TAR + 4 sergenti (Sc.3)
          ⛺⛺  ╚═══════════╝  ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺
   GP3▪   ⛺⛺⛺⛺⛺⛺ (10.000 dormono) ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺  ▪GP4
          — — — — foresta d'approccio (partenza PG, Sc.3) — — — —  SUD ▼
════════════════════════════════════════════════════════════════════════
LEGENDA · 🏰 mura/fortezza (bianche, nuove) · ▓ breccia · ⛺ tende (copertura) ·
▪GP posti di guardia · ╔╗ tenda del comando (Zog'tar) · 👤 Vatore · ⚔️ scontro
veloce · SKULLCRUSHER entra dall'alto sul cortile interno → M7-B.
```
- **Tipo / scala**: strategica (infiltrazione + orientamento). Non è una griglia
  di combattimento; il duello è su M7-B.
- **Terreno & zone**: **Zona 1** = Hammerfist giovane (mura bianche, sicura, arrivo
  del portale) · **Zona 2** = **mare di tende** dell'orda (10.000 dormono; le tende
  = copertura) · **Zona 3** = mura all'alba con la **breccia** ▓. **Posti di
  guardia** GP1-GP4 ai margini.
- **Posizioni notevoli**: **Tenda del Comando** (Zog'tar Deatheye, GS 14, + 4
  sergenti hobgoblin) al centro delle tende; **Vatore** (§5, il futuro Sal) tra le
  tende — incontro grigio col villain prima che sia villain; **Re Thorek I** nella
  Sala del Trono (Zona 1).
- **Tattiche PG (infiltrazione, skill challenge «Mare di Nemici»)**: muoversi di
  copertura in copertura (tende), evitare/neutralizzare i GP; tabella d6 di
  complicazioni (pattuglie, lupi, hobgoblin) in DEF-4 §3. Fallire → allarme
  (l'orda si sveglia). Scelta se affrontare Zog'tar (§4-bis) o aggirarlo.
- **Evoluzione**: raggiunto il cortile all'alba → **Skullcrusher** entra dall'alto → M7-B.
- **Riferimento**: DEF-4 §1-bis, §3, §4-bis, §5.

## MAPPA M7-B — L'ARENA DEL DUELLO: SKULLCRUSHER IL NERO (tattica BOSS · GS 12)

```
════════════════════════════════════════════════════════════════════════
 CORTILE INTERNO — 36 m × 27 m (24 col × 18 righe · 1,5 m) · cielo aperto
 Skullcrusher entra da V1 (quota ~45 m) e picchia. PG partono da riga 16-17.
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️🐉☁️☁️  ← 🐉 Skullcrusher (quota ~45 m, V1)
02    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️     ZONA AEREA (solo volo/gittata)
03    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️
04    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰  ← camminamenti +4,5 m (arcieri nani)
05    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
06    🏰🟫🟫🟫▓▓🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫▓▓🟫🟫🟫🟫🟫🏰  ← ▓ macerie (copertura +4 CA)
07    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
08    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
09    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰  ← ⬛ impronta d'atterraggio (4,5 m)
10    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
11    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
12    🏰🟫🟫🟫▓▓🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫▓▓🟫🟫🟫🟫🟫🏰
13    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
14    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
15    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
16    🏰🟫🟫🛡️🟫🟫🥋🟫🟫🟫🟫👑🟫🟫🟫🟫🔮🟫🟫🌙🟫🟫🟫🏰  ← 🛡️Thorik 🥋Tordek 🔮Artemis 🌙Hella
17    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰    👑 Re Thorek I (alle spalle; 8 pf se Sc.4 fallita)
18    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
════════════════════════════════════════════════════════════════════════
LEGENDA · ☁️ zona aerea (serve volo o gittata) · 🐉 Skullcrusher (quota) ·
⬛ impronta d'atterraggio (Enorme) · 🟫 cortile · ▓ macerie (copertura +4) ·
🏰 mura/camminamenti (+4,5 m, arcieri nani) · 👑 Re Thorek I · 🛡️🥋🔮🌙 i 4 PG.
```
- **Tipo / scala**: tattica BOSS, 24×18. **Skullcrusher il Nero, GS 12** (capostipite
  di Fauci di Palude). Cielo aperto.
- **Terreno & altitudini**: **zona aerea** ☁️ (righe 01-03, quota; il drago vi resta:
  serve **volo o gittata**); **camminamenti +4,5 m** 🏰 (arcieri nani, copertura e
  altezza); **macerie** ▓ (copertura +4 CA) al suolo; **impronta d'atterraggio** ⬛
  (dove il drago Enorme si posa se scende).
- **Posizioni iniziali**: PG a riga 16 (Thorik D16, Tordek G16, Artemis Q16, Hella
  T16); **Re Thorek I** dietro (riga 17). Skullcrusher a V1, quota ~45 m.
- **Tattiche Skullcrusher (nemico — dilemma centrale)**: **NON vuole atterrare** (in
  cielo è un dio): soffio d'acido in picchiata, poi risale. A terra è vulnerabile al
  **full-attack** ma devastante. **Meccanica «la Forgia ricorda le ferite»**: ogni
  ferita inferta qui si riporta su **Fauci di Palude** nel 1372 (carry-over B4).
- **Tattiche PG**: **costringerlo giù** — Artemis in volo lo tormenta, **Aegis Fang
  scagliata** (cicatrice d'ala → B4), tiri dai camminamenti; oppure colpirlo
  dall'alto. Proteggere Re Thorek I (se Sc.4 fallita, è a 8 pf). 3 esiti aperti.
- **Evoluzione**: alla vittoria il **Rubino si accende** (D5/D16) → ritorno (CM-1/DEF-5).
- **Riferimento**: DEF-4 §5 (+ carry-over B4).

---

# DEF-5 · IL RITORNO A HAMMERFIST (1372)

## MAPPA CM-1 — IL CUORE DELLA MONTAGNA (arrivo & apparizione · Incontro 3B)

> **Geometria CANONICA** (invariata): `08_.../Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`
> **MAPPA 5** (master vivo; il Lotto-3-FINALE è la generazione storica dello
> stesso contenuto). Caverna-cattedrale **100 m × 80 m × 40 m** di altezza.
> ⚠️ **Scala 3 m/quadretto** [deviazione A4 dalla convenzione 1,5 m: griglia
> originale disegnata così; NON ridisegnata per non alterare posizioni/portate
> già usate nel testo. Non mischiare quadretti di mappe a scale diverse.]

```
════════════════════════════════════════════════════════════════════════════════
 IL CUORE DELLA MONTAGNA — caverna sacra 100 m × 80 m (33 col × 27 righe · 3 m)
 Soffitto 40 m (stalattiti bioluminescenti) · Giorno 3 dell'assedio (1372)
════════════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g
01    🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🚪🚪🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨  ← 🚪 PORTA DI MITHRAL 6×6 m (P-Q01, unico ingresso)
02    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔴🔴🔴🔴⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  ← 🔴 ondata nemica in corso (entra dalla porta)
03    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔴🔴⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨
04    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵🔵🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  ┐
05    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵🔵⬛⬛⬛⬛⬛🔵🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  │
06    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  │
07    🪨⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛🪨  │ 🔵 CERCHIO DIFENSIVO
08    🪨⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛🪨  │ dei 90 NANI
09    🪨⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛🪨  │ (anello a 30 m
10    🪨⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🪨  │  dall'altare;
11    🪨⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🪨  │  3 file: 60 guerrieri
12    🪨⬛⬛⬛⬛⬛🔵⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛🔵⬛⬛⬛⬛⬛🪨  │  + 20 balestrieri
13    🪨🟨🟨🔺⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⭐✨⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛🔺🟨🟨⬛🪨  │  + 10 capi al centro)
14    🪨⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⚫⭐⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛🪨  │
15    🪨🔺⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛🔺⬛🪨  │ ⭐ ALTARE DI MORADIN
16    🪨⬛⬛⬛⬛⬛🔵⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛🔵⬛⬛⬛⬛⬛🪨  │ (P-Q 13-14 · Ø 6 m,
17    🪨⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🪨  │  +3 m, basalto+rune oro)
18    🪨⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🪨  │ ⚫ RE THOREK (8 pf)
19    🪨⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛🪨  │ ✨ SFERA DORATA (R8!)
20    🪨⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛🪨  │
21    🪨⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛🗿⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛🪨  │
22    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  │
23    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵🔵⬛⬛⬛⬛⬛🔵🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  │
24    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵🔵🔵🔵🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨  ┘
25    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨
26    🪨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🪨
27    🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨
════════════════════════════════════════════════════════════════════════════════
LEGENDA · ⬛ pavimento di caverna · 🪨 pareti · 🚪 porta di mithral 6×6 m (P-Q01,
nord — unico ingresso; ward difensivi collassati) · 🗿 10 STATUE dei Re
Ancestrali (cerchio a 20 m dall'altare, alte 4 m, occhi di rubino — copertura) ·
🔵 90 nani (anello a 30 m) · ⭐⚫✨ altare +3 m con Re Thorek e sfera ·
🟨 piattaforme laterali Est/Ovest (+1,5 m, 6×3 m — tiratori) · 🔺 stalagmiti
(copertura parziale) · 🔴 ondata nemica. Soffitto 40 m: stalattiti di cristallo
BIOLUMINESCENTI (luce piena ovunque, niente *darkness*).
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
                           ▼  ROUND 8: ESPLOSIONE DI LUCE (non violenta)
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
  Sessione 3 dell'ARC-08 — lato ARC-07 = DEF-5 §3-§4). **3 m/quadretto**.
- **Terreno & altitudini**: altare **+3 m** (P-Q 13-14, basalto nero, rune
  d'oro); piattaforme laterali **+1,5 m** (B-C13 ovest, c-d13 est — posizioni
  sopraelevate per tiratori, stalagmiti 🔺 = copertura parziale); soffitto
  **40 m** — le stalattiti possono **crollare** su effetti ad area potenti
  (Terremoto ecc.): 4d6 contundenti, raggio 3 m, **Riflessi CD 18** annulla.
- **Posizioni**: **90 nani** in anello a 30 m (fila esterna 60 guerrieri con
  scudi, mediana 20 balestrieri, interna 10 capi + **Re Thorek** ⚫ sull'altare,
  critico a 8 pf, stabilizzato, cosciente ma incapace di combattere); **10
  statue** 🗿 sul cerchio a 20 m (Q07·U09·W12·W16·U19·Q21·M19·K16·K12·M09);
  nemici dalla **porta nord** P-Q01.
- **Le ondate (Incontro 3B — se giocato per intero, lato ARC-08)**:
  | Round | Ondata | Note tattiche |
  |---|---|---|
  | 1-2 | **30 Orchi berserker** | carica sconsiderata porta→altare |
  | 3-5 | **20 Hobgoblin sergenti** | muro di scudi, **immuni a paura**, tengono impegnati i nani |
  | 6-8 | **15 Bugbear assassini** | Nascondersi +12, puntano i capi e Re Thorek — **interrotti dall'Apparizione** |
  | 9-10 | **Grimjaw + 10 Orog** (se vivo) | vede il ribaltone: ritirata strategica O sfida personale a Thorik; se già morto → capitano minore, auto-ritirata |
- **⏱️ Timing dell'Apparizione (due regie valide)**: giocando il **3B completo**
  (lato ARC-08, coi PNG giocabili Borin/Dara/Thorin/Nala) i PG appaiono al
  **Round 8**, nel mezzo dell'ondata 3; giocando **solo il lato ARC-07**
  (DEF-5 §4, arrivo compresso) appaiono nell'istante in cui le porte cedono.
  Stessa scena, stesso altare: cambia solo quanto assedio si gioca prima.
- **Effetti immediati dell'Apparizione**: nani **+6 morale** (da −4 a +2),
  guariscono **2d8 pf**, **immuni a paura 1 h**; nemici **Volontà CD 25** o
  scossi 1d6 round (la maggioranza fallisce; ~⅔ della prima ondata in panico);
  Re Thorek apre gli occhi (riconosce Thorik: la Corona risuona); gli **occhi di
  rubino delle 10 statue si ACCENDONO** (benedizione ancestrale); i PG hanno un
  **round di sorpresa**.
- **Transizione**: da PNG giocabili → veri PG. Poi pulizia (DEF-5 §5, doppia
  modalità) → portale di Dana → bastioni (ARC-08, `ARC08-11-PONTE-ARRIVO.md`).
- **Riferimento**: geometria/ondate = Atlante-08 **MAPPA 5**; regia lato ARC-07
  = DEF-5 §3-§5; cucitura = ARC08-11.

---

## NOTA DI RESA (futuro)
Queste 12 mappe sono la **fonte ASCII canonica**. La resa a pergamena SVG a
fedeltà piena (senza perdere annotazioni/posizioni/token) è il task
`plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md` (F5 = passata ARC-07). Fino ad
allora si stampa direttamente l'ASCII ultra-clear di questo Atlante.
