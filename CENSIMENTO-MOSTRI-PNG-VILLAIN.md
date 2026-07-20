# CENSIMENTO — Mostri · Villain · PNG (libreria Bestiario)

> **v1 (2026-07-08, lotto L0 del piano libreria)** — inventario completo di
> tutti gli asset di creature/personaggi del repo, prodotto per il
> `PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN.md`. Fa per la libreria ciò
> che `MAPPE-CENSIMENTO.md` ha fatto per le mappe: per ogni sorgente — dove
> sta, in che formato, se è già nello standard, quale azione (lotto) la
> riguarda. **Regola**: le stats esistenti si TRASCRIVONO, mai si rigenerano.
>
> **Legenda azione**: ✅ = già nello standard Bestiario · 🔁 L1 = da
> trascrivere nel formato standard (lotto L1) · 🔗 L3 = statblock d'arco da
> cross-linkare (resta master nell'arco) · 🎨 L4 = token da assegnare ·
> 📸 = storico/duplicato (non si converte).
>
> ---
> ## ✅ STATO: LOTTI L0-L5 COMPLETI (2026-07-11)
> Il piano libreria è **interamente eseguito** (PR #26 L0 + PR #29 L1-L5,
> mergiati). Le righe 🔁/🎨 qui sotto descrivono il **piano originale**; sono
> tutte **FATTE**. La libreria è la fonte viva: `Bestiario/README.md` +
> `scripts/monster_catalog.yaml`. Restano solo i punti **gated su conferma DM**
> (non bloccanti): scarto dei token inutilizzati, promozione di
> `validate_bestiario --rules` a gate. ✅ Khorn e Durgan Tozzefort sono stati
> **canonizzati dal DM (2026-07-12)** — non più `[INFERRED]`.

---

## §1 — Numeri a colpo d'occhio *(aggiornati post-L5, 2026-07-11)*

| Fonte | Quantità | Stato |
|---|---|---|
| `Bestiario/mostri|villain|png` — statblock standard `-crN.md` | **102** (era 57) | ✅ 57 ex-Armate + 45 trascritti/generati in L1-L2; validati da `validate_bestiario.py` |
| `Bestiario/villain|png` — dossier PNG nominati | **34** (17 villain + 17 png) | ✅ +4 mini-dossier villain in L2 (Avatar Tiamat, Tyrgarun, Karruk, Zarim) |
| `Bestiario/pregen-pcgen/` — sorgenti storiche | **~120 file** → **≈45 entità** | ✅ **TRASCRITTE in L1** (44 schede); i file restano sorgente storica sola-lettura |
| Statblock inline negli archi (`*STATBLOCCHI*.md`, `ARC08-02`, ecc.) | ~40 blocchi indicizzati | ✅ 🔗 restano master d'arco; dossier cross-linkati (L3); catalogo li indicizza |
| `Bestiario/tokens/` — immagini webp | **110** (3 sfondi/scene scartati in L4) | ✅ nomi-hash rinominati per soggetto; manifest `tokens/README.md`; 2 assegnati |
| `scripts/monster_catalog.yaml` — indice automatico | **293 record** (era 246) | ✅ rigenerato; walk deterministico (fix CI) |

## §2 — Libreria standard (stato attuale)

- **`mostri/` (43 statblock)**: unità generiche Mano Rossa, drow, gnoll,
  loxo/centauri, githyanki, thayan, non-morti del Ghostlord, difensori
  Rethmar/Dauth, razorfiend, ondate giganti. Convenzioni nel
  `mostri/README-CATALOGO-STORICO.md` (valide) + `Bestiario/README.md`.
- **`villain/` (9 statblock + 13 dossier)**: statblock di Azarr Kul, Avatar
  di Tiamat, Tyrgarun, Wyrmlord Karruk, Xal'thor, Zarim, Conte Valerius,
  Il Collezionista, Emissario Mano Rossa; dossier di Azarr Kul, Belkram,
  Conte Valerius, Ghostlord, Salvatore, Sethrax, Sonjak, Urialle, Xal'thor,
  Il Collezionista, Fauci di Palude, Generale Grimjaw, Gorthak il Trifronte.
- **`png/` (6 statblock + 17 dossier)**: statblock di Capitana Lorana,
  Therysol, Comandante Dauth (Durgan Tozzefort `[INFERRED]`), Arci-druido,
  Arcimago del Circolo, Druido-orso; dossier di Consiglio Rethmar, Lorana,
  Lythiel, Maewen, Tempestas, Therysol, Varis + i 10 file singoli
  (Borin Ferropugno, Capitano Lunapiena, Dana Forgiapietra, Dara
  Occhiolesto, Khorn, Nala Cantapietre, Orion Pelleorsa, Re Thorek,
  Signore Ventolesto, Thorin Runaforte).

## §3 — Sorgenti storiche `pregen-pcgen/` (→ lotto L1) — ✅ FATTO

> ✅ **Tutte le righe 🔁 di questa sezione sono state trascritte in L1**
> (2026-07-08). Le schede risultanti sono in `Bestiario/mostri|villain|png/`
> (cerca per nome in `scripts/monster_catalog.yaml`). La tabella resta come
> traccia della provenienza sorgente→scheda.
>
> Dedup a livello di **entità**: le varianti `spell/no-spell` e le copie
> byte-simili della stessa build sono UNA scheda da trascrivere. I file
> restano al loro posto come sorgente (sola lettura); la trascrizione va in
> `Bestiario/mostri/` (generici) o nella cartella del personaggio
> (nominati). CR dal filename dove dichiarato, altrimenti dal contenuto.

### §3.1 Radice (guardiani/aberrazioni ARC 02-06)

| Entità | Sorgenti | CR | Azione |
|---|---|---|---|
| Bebilith (guardiano delle rovine, pre-cattedrale) | htm (D&D Wiki) | 10 | 🔁 L1 → `mostri/bebilith-guardiano-cr10.md` |
| Retriever (mandato dai chierici di Abbathor per Aegis Fang) | 2 htm (Wiki + d20srd) | 11 | 🔁 L1 (una sola scheda) |
| Beholder Death Tyrant (difensore del tempio) | pdf | 13 | 🔁 L1 |
| Myconid Sovereign | 2 html (Kassoon) | — | 🔁 L1 (ARC-02 funghi) — ⚠️ verificare CR 3.5 vs 5e: la fonte Kassoon è 5e, trascrivere dai valori MM 3.5 |
| Phantom Fungus | html (d20srd) | 3 | 🔁 L1 |
| Underdark cleric Ainin (formato statblock) | html | 6 | 📸 variante della riga Ainin in §3.3 |
| Triple-Headed Ettin Barbarian | odt + pdf | — | 🔁 L1 → statblock di **Gorthak il Trifronte** (`villain/`), collegare al dossier |

### §3.2 `00_scaladossa-abbattor-funghi/` (testi con statblock inline)

| Entità | Sorgenti | Azione |
|---|---|---|
| Nani duergar di Abbathor — Scala di Ossa (gruppo) | txt | 🔁 L1 (estrazione statblock dal testo) |
| Epic fight dwarf/duergar (set d'incontro) | txt | 🔁 L1 |
| Fight fungi colony (colonia + guardie myconid) | 2 txt (raw+formatted = 📸 doppione) | 🔁 L1 |

### §3.3 `png_La_mano_rossa_del_destino/` (RHoD originale + custom, era ARC 00-04)

| Entità | Sorgenti | CR | Azione |
|---|---|---|---|
| Arbitrax, Drago Rosso (= Abithriax RHoD) | pcg + htm | ~8-10 | 🔁 L1 |
| Bothor-Malvur (underdark) | pcg | 6 | 🔁 L1 |
| Koth, bugbear draconico → «Signore dei Dragoni» | 2 pcg + htm | — | 🔁 L1 (2 stadi) |
| Capitan «Loranna Anitah» | pcg + htm | 7 | ✅ già a catalogo `png/Lorana/capitana-lorana-cr7.md` — L1 verifica valori PCGen↔scheda |
| Draon-hamann | pcg | 8 | 🔁 L1 |
| Draxoksus, hobgoblin sciamano draconico mezzo-immondo | pcg + 3 htm (+ copia in `Incontro-RedHandof-doom/` 📸) | 7 | 🔁 L1 (una scheda) |
| Druido Avarthel | pcg + htm | 9 | 🔁 L1 |
| Goblin worg raider | pcg + htm | 5 | 🔁 L1 |
| Ozyrrandion, drago verde (3 grafie) | 2 pcg + htm | 8 | 🔁 L1 (una scheda; RHoD) |
| Hell Hound mezzo-immondo | pcg + 2 htm | 4 | 🔁 L1 |
| Hell Hound draconico | 2 pcg (+ copia `regolari/`) | — | 🔁 L1 |
| Hobgoblin bladebearer 6 liv (+ variante longsword) | 2 pcg + 2 htm | ~6 | 🔁 L1 — dedup con «portalame» (versione IT, `regolari/`) |
| Hobgoblin Doom Hand cleric 5 liv + «Zarr Doom Hand Cleric» | 2 pcg + 2 htm | ~5 | 🔁 L1 (RHoD Doom Hand; Zarr = esemplare nominato) |
| Hobgoblin regular 3/4 liv + combattente GS2/CR3 (`regolari/`) | 5 pcg + 2 htm | 2-4 | 🔁 L1 (progressione schiere 2→4; complementare a `goblin-warrior1-cr05` e `hobgoblin-captain-cr8` già a catalogo) |
| Hobgoblin sergente (`regolari/`) | pcg | 5 | ✅ già a catalogo `mostri/hobgoblin-sergente-cr5.md` — L1 verifica |
| Hobgoblin veterans 6 liv | pcg + htm | ~6 | 🔁 L1 |
| Jorr Natherson (guida di Witchwood, RHoD) + build 8 liv | 2 pcg + 2 htm | ~5/8 | 🔁 L1 (2 stadi) |
| KulkorZhul War Adept base cr8 + varianti cr9 acid/fire/ice/lightning | 6 pcg + 7 htm | 8-9 | 🔁 L1 → **una scheda base + tabella varianti elementali** (niente 5 file quasi uguali) |
| Lómyn RedTongue, bardo 8 | pcg | ~8 | 🔁 L1 |
| Minotauro Karkilan | pcg + htm | 5 | 🔁 L1 |
| Monaco «Pugno del Destino» | pcg + htm | 7 | 🔁 L1 |
| Nano Morlin Coalhewer | pcg + htm | 12 | 🔁 L1 (fazione Dauth, già keyword del catalogo) |
| Ogre Skullcrusher | html | 5 | 🔁 L1 (nota: eredità Skullcrusher→Fauci, ARC08-10 §4.1) |
| Orco berserk 2 liv + orco regular | 3 pcg + 2 htm | 2 | 🔁 L1 (2 schede) |
| Rurik Gorunn, Martello di Moradin 10 liv | pcg + htm | ~10 | 🔁 L1 |
| Cavalcatura da paladino del Martello di Moradin (ariete) (`regolari/`) | pcg + htm | — | 🔁 L1 |
| Underdark cleric Ainin cr5 → cr6 | 2 pcg + 3 htm/html | 5/6 | 🔁 L1 (progressione 2 stadi) |
| Underdark deep warden Brieyn | pcg + htm | 7 | 🔁 L1 |
| Underdark dovil runecaster/deep diviner | pcg + 2 htm | 7 | 🔁 L1 |
| Worg | pcg + htm | 2 | 🔁 L1 |

### §3.4 `png_La_mano_rossa_del_destino/Duergar_figther_ponte/` (incontro del ponte)

| Entità | Sorgenti | CR | Azione |
|---|---|---|---|
| Chierico di Abbathor (base + build 11 liv) | pcg + 3 htm | ~4/11 | 🔁 L1 (2 stadi) |
| Blackguard | htm | — | 🔁 L1 |
| Duergar chierico 3 liv | 2 html | 4 | 🔁 L1 |
| Duergar guerriero 2 liv | html | 3 | 🔁 L1 |
| Duergar ladro 1 liv | html | 2 | 🔁 L1 |
| Duergar mago 3 liv | 2 html | 4 | 🔁 L1 |
| Duergar mago/ladro 8 liv | 2 htm | ~8 | 🔁 L1 |

## §4 — Gap (dossier ↔ statblock) → lotti L2/L3 — ✅ FATTO

> ✅ **Chiuso in L2/L3** (2026-07-08): Khorn ha ora lo statblock
> (`png/Khorn/khorn-ufficiale-hammerfist-cr8.md`, `[INFERRED]`); i 4 villain
> orfani hanno il mini-dossier (Avatar Tiamat, Tyrgarun, Karruk, Zarim); i
> dossier d'arco 🔗 sono cross-linkati e verificati (zero numeri duplicati).
> Il «Comandante Dauth» è ora **Durgan Tozzefort** (rinominato da Borin per
> non confliggere con Borin Ferropugno). La tabella resta come mappa storica.
> ✅ **Khorn e Durgan Tozzefort canonizzati dal DM (2026-07-12)**: i flag
> `[INFERRED]` sono stati rimossi da statblock, dossier e riferimenti d'arco.

**Dossier senza statblock proprio** (lo statblock canonico vive in un file
d'arco → 🔗 L3 cross-link, oppure manca → 🔁 L2):

| Personaggio | Statblock canonico oggi | Azione |
|---|---|---|
| Ghostlord | `09_.../P3-Ghostlord-LICH-ALLEANZA-STATBLOCCHI.md` | 🔗 L3 |
| Sethrax il Velato | `09_.../P2B-Torneo-STATBLOCCHI-COMPLETO.md` | 🔗 L3 |
| Sonjak / Urialle | `09_.../P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` + FASE0 | 🔗 L3 |
| Salvatore | `09_.../P2C-Salvatore-Mercante-TESTO.md` | 🔗 L3 |
| Fauci di Palude / Grimjaw / Gorthak | `08_.../ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` | 🔗 L3 (Gorthak: anche pregen Ettin §3.1) |
| Belkram | `04_tomba_di_Belkram/**` (storico) | 🔗 L3 (post-mortem, D13) |
| Eroi di Hammerfist (Borin F., Dara, Nala, Thorin R.) | `08_.../ARC08-02` (pregen) | 🔗 L3 |
| Maewen, Lythiel, Tempestas, Varis, Consiglio | schede nei dossier stessi | ✅ (verifica L2) |
| **Khorn** | **nessuno** (`[INFERRED]` dichiarato nel dossier) | 🔁 L2 (generare, flag [INFERRED], via npc-villain-boosting) |
| Re Thorek, Capitano Lunapiena, Dana F., Orion P., Signore Ventolesto | key stats sintetiche nel dossier | ✅ (verifica L2) |

**Statblock senza dossier** (villain/png "orfani" al livello base delle
cartelle): Avatar di Tiamat, Tyrgarun, Wyrmlord Karruk, Zarim, Emissario
Mano Rossa; Arci-druido, Arcimago del Circolo, Druido-orso, Comandante
Dauth → 🔁 L2 (mini-dossier col template `png-dossier-template.md`).

## §5 — Token (`tokens/`, → lotto L4) — ✅ FATTO

> ✅ **L4 eseguito** (2026-07-08/11): i file con nome-hash sono stati
> rinominati per soggetto; manifest in `Bestiario/tokens/README.md`; 2 token
> assegnati (Lythiel, Jorr); 3 sfondi/scene non-combattente scartati. Resta
> gated (conferma DM) l'assegnazione fine dei restanti e lo scarto di altri.

| Cartella | Contenuto | Stato |
|---|---|---|
| `tokens/Monster_And_Png/` (+ `Dragons/`, `Png/`, `immagini_Mostri_D&D_Campagna/`) | 72 webp | ✅ in libreria; assegnazione fine gated |
| `tokens/da-catalogare/` (ex `Png_And_Monster_To_Be_added`) | 38 webp | ✅ hash rinominati per soggetto; manifest nel README; scarti/assegnazioni residue gated DM |

## §6 — File igiene

- `.~lock.Epic_fight_dwarf_duergar.txt#` (lock LibreOffice) — **rimosso in
  L0** (stessa classe dei temporanei Word approvati in T-D11).
- Copie `Incontro-RedHandof-doom/Draxoksus*` = 📸 duplicati byte-simili
  della cartella madre: restano come storico, la trascrizione L1 usa la
  cartella madre.

## §7 — Gap PNG dell'AP originale (2026-07-20, post-L5)

> Il censimento L0 contava solo ciò che esisteva **nel repo**. Un secondo
> passaggio contro l'AP originale (Red Hand of Doom) ha rivelato PNG del
> manuale mai entrati in nessuna sorgente: i civici del Guado di Drellin
> (Norro Wiston, Sertieren, Derny, Delora Zann, Iormel, Kellin Shadowbanks),
> il secondo anello di Rethmar (Tredora Goldenbrow, Immerstal, Ulverth,
> Teyani Sura), Witchwood/Tiri Kitor (Warklegnaw, Trellara Nightshadow) e
> due Wyrmlord (Ulwai Stormcaller, Hravek Kharn). Censimento completo,
> diagnosi e lotti di reintegrazione: `plans/PIANO-REINTEGRAZIONE-PNG-AP-RHOD.md`.
> **Fatto (R1+R5)**: `png/Guado_di_Drellin/Profughi_Guado_di_Drellin.md`
> (6 PNG) + `png/Lirien/Lirien.md` (PNG caotico ricorrente). ✅ **Entrambi
> canonizzati dal DM (2026-07-20)** — flag `[INFERRED]` sciolti, righe in
> `state.md` §1/§3/§7/§8. **R2+R3 preparati (2026-07-20)**: `png/Secondo_Anello_Rethmar/` (Tredora, Immerstal, Ulverth, Teyani) e `png/Witchwood_Tiri_Kitor/` (Sellyria, Killiar[cross-link], Illian, Trellara, Warklegnaw), tutti `[INFERRED]`. Resta R4 (Ulwai + decisione DM).
