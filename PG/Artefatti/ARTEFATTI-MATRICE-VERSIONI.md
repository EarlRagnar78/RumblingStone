# ARTEFATTI — Matrice Versioni × Contenuto (task T4, piano trasversale)

> **Scopo**: fare per `PG/Artefatti/` ciò che `ARC07-MATRICE-VERSIONI.md` ha
> fatto per i file-avventura: **un master eletto per artefatto**, ruolo di
> ogni altro file, stato leggibile in 10 secondi. Nasce dal task **T4** del
> `PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md`.
>
> **Regole (D9/D10, piano ARC-07)**: `PG/Artefatti/` è la **fonte canonica**;
> le copie altrove sono snapshot storici con banner. I file ridondanti si
> DEPRECANO con banner, mai eliminati. Lo **stato corrente** dei poteri vive
> in `campaign/state.md` §6 (✅ dal T6c 2026-07-04 la tabella è a **doppia
> colonna etichettata**: «Today at the table ARC-07 P4» / «Prepared ARC-09
> entry» — vedi la nota [T4-a] in fondo, ora risolta).
> **Legenda stato**: ⭐ MASTER = versione viva · *annesso* = supporto citato
> dal master · 📸 snapshot = storico, non aggiornare · ~~DEPRECATO~~ ·
> HANDOUT = materiale giocatore.


---

## 0. VERSIONI VIVE — il registro (ADR-0071, dal 2026-09-25)

> **Perché c'è.** Il DM, il 2026-09-25: *«non c'è stato mai un versionamento,
> che credo sia la scelta migliore per gestire questi artefatti complessi ed
> integrati nella campagna»*. Fino a oggi una pagina si correggeva sul posto e
> niente diceva quale delle quattro pagine HTML di una cartella fosse quella
> viva; la pagina a due gemme della Corona portava ancora i Doni superati.
>
> **La regola.** Ogni artefatto cresce per **stadi** (un rituale, una quest,
> una scelta: il modello è *Weapons of Legacy*). Ogni stadio ha una pagina per
> il giocatore e una per il DM. Ogni pagina porta la sua **versione** nella
> meta `versione-artefatto` e in fondo alla pagina, nella forma
> `artefatto · S<stadio> · r<revisione> · <data>`. La revisione sale a ogni
> modifica del contenuto; la versione precedente va in `_ARCHIVIO/` della
> cartella, con un banner. Il test `scripts/tests/test_versioni_artefatti.py`
> confronta questa tabella con le pagine.
>
> **Cosa non dice.** A che stadio è il tavolo lo dice `campaign/state.md` §6,
> che si scrive sul ramo del gruppo (ADR-0007). Qui c'è quale pagina stampare
> per ogni stadio. L'audit che ha fissato le versioni `r1`/`r2` è
> `ARTEFATTI-AUDIT-POTERI-2026-09-25.md`.

<!-- versioni-artefatti -->
| Artefatto | Stadio | Pagina giocatore | Pagina DM | Versione | Stato |
|---|---|---|---|---|---|
| corona | 0 · indossata | `00-La Corona di Adamantio-ogetto&Prove/00_Corona_0_Gemme.html` | `00-La Corona di Adamantio-ogetto&Prove/00_Corona_0_Gemme_DM.html` | `corona · S0 · r5 · 2026-09-25` | ✅ passato |
| corona | 1 · Topazio | `00-La Corona di Adamantio-ogetto&Prove/01_Corona_1_Gemma.html` | `00-La Corona di Adamantio-ogetto&Prove/01_Corona_1_Gemma_DM.html` | `corona · S1 · r6 · 2026-09-25` | ✅ passato |
| corona | 2 · Smeraldo | `00-La Corona di Adamantio-ogetto&Prove/02_Corona_2_Gemme.html` | `00-La Corona di Adamantio-ogetto&Prove/02_Corona_2_Gemme_DM.html` | `corona · S2 · r6 · 2026-09-25` | ▶ oggi |
| corona | 3 · Rubino | `00-La Corona di Adamantio-ogetto&Prove/03_Corona_3_Gemme.html` | `00-La Corona di Adamantio-ogetto&Prove/03_Corona_3_Gemme_DM.html` | `corona · S3 · r7 · 2026-09-28` | ⬜ al Rituale 4, intera dopo l'uso del Rubino |
| aegis | 0 · pre-risveglio | `Aegis Fang/00_Aegis_Fang_Stadio0.html` | `Aegis Fang/00_Aegis_Fang_Stadio0_DM.html` | `aegis · S0 · r7 · 2026-09-25` | ▶ oggi |
| aegis | 1 · risveglio pieno | `Aegis Fang/01_Aegis_Fang_Stadio1.html` | `Aegis Fang/01_Aegis_Fang_Stadio1_DM.html` | `aegis · S1 · r4 · 2026-09-25` | ⬜ al Rituale 4 |
| anello | 0 · l'anello del caos | `ringOfChaoticIllumination/01_Anello_S0_Originale.html` | `ringOfChaoticIllumination/01_Anello_S0_Originale_DM.html` | `anello · S0 · r5 · 2026-09-25` | ✅ passato |
| anello | 1 · le due divinità | — | `ringOfChaoticIllumination/02_Anello_S1_Due_Divinita_DM.html` | `anello · S1 · r4 · 2026-09-25` | scritto, mai dato al giocatore (D11) |
| anello | 2 · il Riforgiato | `ringOfChaoticIllumination/00_Ring_Riforgiato.html` | `ringOfChaoticIllumination/00_Ring_Riforgiato_DM.html` | `anello · S2 · r5 · 2026-09-25` | ▶ oggi |
| anello | 3 · il Caos Ultimo | `ringOfChaoticIllumination/04_Anello_S3_Caos_Ultimo.html` | `ringOfChaoticIllumination/04_Anello_S3_Caos_Ultimo_DM.html` | `anello · S3 · r6 · 2026-09-25` | ⬜ alla Torre Invisibile (D13 decisa) |
| bracieri | 0 · dormienti | `Tordek/00_Bracieri_S0_Dormienti.html` | `Tordek/00_Bracieri_S0_Dormienti_DM.html` | `bracieri · S0 · r4 · 2026-09-25` | ✅ passato |
| bracieri | 1 · Fuoco | `Tordek/04_Bracieri_Gemelli_Scheda_PG_Fuoco.html` | `Tordek/04_Bracieri_Gemelli_Scheda_PG_Fuoco_DM.html` | `bracieri · S1 · r5 · 2026-09-25` | ✅ passato |
| bracieri | 2 · Fuoco e Terra | `Tordek/05_Bracieri_Gemelli_Scheda_PG_Completa.html` | `Tordek/05_Bracieri_Gemelli_Scheda_PG_Completa_DM.html` | `bracieri · S2 · r6 · 2026-09-25` | ▶ oggi |
| bracieri | 3 · le Chiavi della Forgia | `Tordek/06_Bracieri_S3_Chiavi_della_Forgia.html` | `Tordek/06_Bracieri_S3_Chiavi_della_Forgia_DM.html` | `bracieri · S3 · r4 · 2026-09-25` | ⬜ a Dauth (D16 decisa) |
| collana | 0 · i semi | — | `Hella/00_Collana_S0_I_Semi_DM.html` | `collana · S0 · r3 · 2026-09-25` | ✅ passato (solo DM: la Collana non esisteva) |
| collana | 1 · Radicata | `Hella/01_Collana_Radicata.html` | `Hella/01_Collana_Radicata_DM.html` | `collana · S1 · r6 · 2026-09-25` | ▶ dopo il rito |
| collana | 2 · Fiorita | `Hella/03_Collana_S2_Fiorita.html` | `Hella/03_Collana_S2_Fiorita_DM.html` | `collana · S2 · r4 · 2026-09-25` | ⬜ al Cerchio Sacro (D17 decisa) |
| collana | 3 · Foresta che Cammina | `Hella/04_Collana_S3_Foresta_che_Cammina.html` | `Hella/04_Collana_S3_Foresta_che_Cammina_DM.html` | `collana · S3 · r4 · 2026-09-25` | ⬜ a Rethmar (D17 decisa) |
| durik | 1 · Radicata | `Hella/02_Durik_Guardiano_di_Pietra.html` | `Hella/02_Durik_Guardiano_di_Pietra_DM.html` | `durik · S1 · r3 · 2026-09-25` | ▶ dopo il rito |

**Le revisioni del 2026-09-25 pomeriggio** (`r2`/`r3`) applicano le risposte del DM alle domande D1-D12 dell'audit: tolte le marcature «da confermare». La pagina del giocatore dell'Anello S1 è stata tolta (D11: mai data al tavolo).

**Revisioni precedenti.** `corona · S1 · r1` e `corona · S2 · r1` (la pagina a
due gemme del 2026-08-01 e la sua versione DM) e `corona · S3 · r1` sono in
`00-La Corona di Adamantio-ogetto&Prove/_ARCHIVIO/pagine-v1-2026-09-25/`.
`aegis · S0 · r1`, `anello · S2 · r1`, `bracieri · S2 · r1`, `collana · S1 · r1`
sono le stesse pagine prima di questo audit: la storia le tiene (`git log`).

**Stadi (2026-09-25, sera).** Tutti gli artefatti hanno una pagina per ogni
stadio, per il giocatore e per il DM. Le ultime tre decisioni (D15 Aegis S1,
D16 Bracieri S3, D17 Collana S2-S3) le ha prese il DM la sera stessa. Restano
solo DM, perché non hanno un giocatore: l'Anello S1 (mai dato) e la Collana S0
(la Collana non esisteva).

**Immagini (2026-09-25, notte, ADR-0072).** Ogni pagina porta la sua
immagine dentro, in webp, come le schede di prima: quale immagine lo dice
`immagini-artefatti.json`, la mette `python3 scripts/incorpora_immagini_artefatti.py`.
⚠️ **Dopo ogni rigenerazione di una pagina va rilanciato**: i generatori
riscrivono l'HTML intero, e `test_immagini_artefatti.py` diventa rosso.
Mancano un'immagine di Aegis Fang e una dei Bracieri dormienti: da
commissionare (`rumblingstone-art-direction`).

---

## 1. CORONA DI ADAMANTIO (Thorik) — l'artefatto più complesso

**⭐ MASTER DM**: `PG/Artefatti/LaCorona_di_Adamantio-DM.md` (guida
onnicomprensiva, già eletta fonte canonica in A10/D9).
**Versione definitiva, per stadio (2026-09-25)**: le otto pagine
`00…03_Corona_*{,_DM}.html`, registrate in §0. Il master DM resta la fonte
delle regole, con un banner sui quattro punti superati; il confronto potere
per potere è in `ARTEFATTI-AUDIT-POTERI-2026-09-25.md` §1.
**HANDOUT giocatore — stato attuale**: `Artefatti-Pg/00-La Corona di
Adamantio-ogetto&Prove/00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` (creata in T4:
una pagina, solo i poteri sbloccati, due snapshot etichettati).

Cartella `Artefatti-Pg/00-La Corona di Adamantio-ogetto&Prove/`:

| File | Ruolo | Stato |
|---|---|---|
| `000_Guida_Dm_ogetto_prove_rituali_sfide.md` (37 KB) | prove/rituali/sfide in dettaglio | *annesso DM* (citato dal MASTER) |
| `000_Corona_adamantio_ogetto.md` | scheda-oggetto sintetica | 📸 **ASSORBITO nel MASTER** (T6b: banner in testa; il master prevale, es. sul prereq BAB) |
| `00_corona_di_adamantio_completa_italiano.md` | generazione precedente in italiano | 📸 snapshot `[INFERRED]` |
| `00_corona_adamantio_in_inglese.txt`, `00_corona_adamantio_in_inglese&rituali.txt` | generazioni in inglese | 📸 snapshot |
| `00_corona_di_adamantio_i_rituali_descrizioni_interventi_divini.md` | descrizioni rituali/interventi divini | *annesso DM* |
| `00_corona_di_adamantio_momento_risveglio_1_prova_scheda_giocatore.md` | scena risveglio + 1ª prova | *annesso* (materiale scena) |
| `00_Schede_avvenimenti_Corona_di_Adamantio-ALT.md` | registro avvenimenti (formulazione sacrifici più chiara) | ⭐ **eletta (T6b)** tra le 2 varianti |
| `00_Schede_avvenimenti_Corona_di_adamantio.md` | idem, differiva di 1 parola | 📸 SUPERATA (T6b: banner) |
| `00_scheda_Giocatore.md` | scheda giocatore, generazione 1 | ~~superata~~ dalla SCHEDA-GIOCATORE-STATO-ATTUALE |
| `00_Scheda_Giocatore_Aggiornata_Fase2.md`, `01_Scheda_Giocatore_Sintesi_Pratica_Fase2.md` | schede giocatore Fase 2 | ~~superate~~ (contenuto assorbito nella STATO-ATTUALE) |
| `00/01/02/03_Corona_N_Gemme{,_DM}.html` | **le otto pagine a stadi** (0-3 gemme, giocatore e DM), riscritte il 2026-09-25 | ⭐ **DEFINITIVE**: versioni nel registro §0; le revisioni precedenti di 01/02/03 in `_ARCHIVIO/pagine-v1-2026-09-25/`. Prima dell'audit: HANDOUT per stadio (stampare quello giusto) — **riconciliate col master in T6b**; i 2 dubbi sono stati **RISOLTI dal DM (2026-07-04)**: Stone's Awareness = Trappole **e** Comprendere Linguaggi (entrambi); Topazio = attivazione **1 ora**. Master, scheda giocatore e reference aggiornati |
| `Evoluzione_della_Scena-Trial_of_the_Deep_Hall.md` | scena del 2° rituale legacy | *annesso* (giocato) |
| `LaCorona_di_Adamantio-DM.pdf`, `LaCorona_di_Adamantio.pdf` | export PDF | 📸 generati (rigenerare dal MASTER) |
| immagini (`CoronaDiAdamantio.webp`, `Generated Image...webp`) | asset visivi | ok (C1: momento d'uso = risveglio gemme) |

**Progressione (artefatto vivo)** — dettagli nel MASTER; stato in state.md §6:

| Stadio | Trigger (rituale/gemma) | Sblocca | Stato al tavolo |
|---|---|---|---|
| Base | indossare da degno | Stone's Awareness; +2 CA deflessione | ✅ |
| Rituale 1 — Forge's Defense | visione della battaglia | legame + visioni | ✅ |
| Rituale 2 — Trial of the Deep Hall | tempio profano Underdark | Moradin's Insight (True Seeing 1/giorno; +4 Artigianato-fabbro) | ✅ giocato `[INFERRED: verificare che il giocatore lo stia usando]` |
| Gemma TOPAZIO (Tempo Immutabile) | rituale Piano del Fuoco (P3) | viaggio temporale 1/mese (costo: invecchia 1d10 anni) | ✅ **unica gemma accesa OGGI** (D8/D16) |
| Rituale 3 — Anvil of the World + Gemma SMERALDO | Piano della Terra (P4, IN CORSO) | Adamantine Will; Muro di Pietra / Terremoto controllato 1/settimana (1.000 mo) | 🟡 in palio |
| Gemma RUBINO (Dwarven Might) + Rituale 4 — Siege of the Eternal Forge | vittoria nella battaglia antica (P5) | ***Aura della Forgia Eterna*** 1/settimana — *Possenza Divina* e *Protezione dal Male* ai quattro; *Possenza Divina*, *Protezione dal Male*, *Benedizione* e uno *Scolpire Pietra* a ogni nano entro 30 m; **+4 morale** ad attacchi e TS per i nani in vista; nemici **Volontà CD 20** o **scossi** 1 minuto. La prima volta dura **fino all'alba**. Più **Corona +3**, **Senzienza**, e **il Rubino si consuma nel ritorno al 1372** (D16). ⚠️ **Il Mantle of Stone and Spirit NON è di questo rituale**: è del **Rituale 3** — vedi r.145 e la scheda giocatore r.35 (correzione DM 2026-09-20: la regola è che decide la scheda che il giocatore ha letto) | ⬜ da giocare — Rubino poi SPESO |

## 2. AEGIS FANG (Thorik)

**Versione definitiva (2026-09-25)**: `00_Aegis_Fang_Stadio0{,_DM}.html`, stadio 0, registro §0.
Lo stadio 1 (risveglio al Rituale 4) ha la fonte in `05_Aegis_Fang_Final_Awakening.html` e le
pagine da fare (lotto T10-e).

**Stato**: pre-risveglio pieno (+2 Returning Dwarven Waraxe, bonded — state.md §6).
Cartella `Artefatti-Pg/Aegis Fang/`:

| File | Ruolo | Stato |
|---|---|---|
| `00_Aegis_Fang-MASTER-DM.md` | Guida DM (master vivo, tabella di progressione a 2 stadi) | ⭐ **MASTER** (creato in **T6b** 2026-07-04, transcritto da `.docx` + HTML risveglio) |
| `00_Aegis_Fang-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | HANDOUT giocatore (Stadio 0, senza spoiler del risveglio) | ⭐ scheda giocatore (creata in **T7** 2026-07-04) |
| `Aegis Fang.docx` / `Aegis Fang.pdf` | scheda completa originale | 📸 export storico (fonte dello stadio base del master `.md`) |
| `05_Aegis_Fang_Final_Awakening.html` | risveglio finale (post-Siege) | *annesso* — fonte dello **Stadio 1** del master `.md` (risveglio pieno, ⬜ futuro) |
| `Avventure_per_nani.txt` | appunti | ⭐ canonico (refuso eletto/rinominato in T6a) |
| `DEPRECATO-Avvneture_per_nani-refuso-duplicato.txt` | appunti, duplicato byte-identico | 📸 deprecato (T6a: `git mv` dal refuso `Avvneture_per_nani.txt`, banner in testa) |
| `~$gis Fang.docx`, `~WRL0191.tmp` | file temporanei Word | ✅ **RIMOSSI (conferma DM 2026-07-04)** — `git rm`, erano lock/autosave Word senza contenuto utile |

> **↩ Eco del rituale P3B (v4-bis, DM 2026-09-12)**: Aegis Fang **non viene
> donata** al rituale di Hella — il dono di Thorik è il **+2 di deflessione
> della Corona**. L'arma però è **senziente (Ego 14)** e reagisce alla scelta
> del portatore: 🟢 se dona, **smette di dubitare di lui** (nessuna prova di
> opposizione per un arco); 🔴 se rifiuta, **lo giudica** nelle scene che
> riguardano Hella o dei nani da proteggere. **Riportato** nel master
> `00_Aegis_Fang-MASTER-DM.md` (§ *Costi e vincoli*). Fonte:
> `../../07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md` §5.
>
> ⚠️ **Superata la riga precedente**, che toglieva il *Returning* col «Filo
> dell'Ascia»: contraddiceva il profilo dello Stadio 1 (*«+4 Sacra
> **Ritornante**»*). Istantanea in
> `../../07_il Portale Della Forgia Eterna/_ARCHIVIO/doni-v1-2026-09-12/`.

## 3. RING OF CHAOTIC ILLUMINATION (Artemis)

**Versione definitiva, per stadio (2026-09-25)**: S0 `01_Anello_S0_Originale{,_DM}.html`,
S1 `02_Anello_S1_Due_Divinita{,_DM}.html`, S2 `00_Ring_Riforgiato{,_DM}.html` (oggi),
S3 `04_Anello_S3_Caos_Ultimo{,_DM}.html` (D13 decisa il 2026-09-25; la pagina del giocatore si consegna alla Torre). Registro §0,
confronto in `ARTEFATTI-AUDIT-POTERI-2026-09-25.md` §3. Lo stadio 1 viene dal PDF
`Artemis/Cerebromorphosis/Lord of Sun and Shadow - Power Analysis & Transformation Choices.pdf`,
che nessuna versione successiva riportava.

**⭐ MASTER**: `Artefatti-Pg/ringOfChaoticIllumination/00_Ring_of_Chaotic_Illumination_Revised.md`
(eletto in A10; banner presente). `Old/` deprecata con `_DEPRECATED-SNAPSHOT.md`.

| File | Ruolo | Stato |
|---|---|---|
| `PG/Artefatti/Ring of Chaotic Illumination.md` (top-level) | versione originale inglese pre-riforgiatura | 📸 snapshot storico (banner aggiunto in T6a) |
| `PG/Artefatti/Ring_of_chaotic_illumination-master.md` + `.odt`/`.pdf` (top-level) | "documento riservato DM", generazione 2 | 📸 snapshot storico (banner aggiunto al `.md` in T6a; export `.odt`/`.pdf` binari non bannerabili, stesso stato per riferimento) |
| `ringOfChaoticIllumination/00_..._Revised.html` / `Ring of Chaotic Illumination (Reforged).pdf` | export del MASTER | 📸 generati |
| `ringOfChaoticIllumination/00_Ring-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | HANDOUT giocatore (poteri costanti+attivati; poteri di crisi SOLO lato DM) | ⭐ scheda giocatore (creata in **T7** 2026-07-04) |
| `Artemis/Cerebromorphosis/Italiano/cerebromorphosis_italian-final.md` | sistema crisi Cerebromorphosis (IT, completo) | ⭐ **MASTER eletto (T6b)** — banner in testa |
| `Artemis/Cerebromorphosis/cerebromorphosis_system.md` (root + copia in `Italiano/`, byte-identiche) | stesso sistema di crisi, generazione **inglese** | 📸 snapshot storico (EN) |
| `Artemis/Cerebromorphosis/party_intervention_system.md` (root + `Italiano/`) · `Italiano/moradin_divine_guidance_italian.md` | **sottosistema distinto**: intervento di guida divina del party (non la crisi) | *annesso* al percorso di Artemis |
| `Artemis/Cerebromorphosis/**/*.pdf` | export vari (IT/EN) del sistema crisi + party-intervention | 📸 generati (binari, non bannerabili) |
| `PrestigeClass/lord_sun_shadow/` | classe di prestigio RIFIUTATA da Artemis | 📸 storia di progetto (percorso alternativo chiuso) |

## 4. BRACIERI GEMELLI + CINTURA DELLA DEVASTAZIONE (Tordek) — il modello

**Versione definitiva (2026-09-25)**: `05_Bracieri_Gemelli_Scheda_PG_Completa.html`, stadio 2
(Fuoco e Terra), registro §0; la parte DM è `01_Bracieri_Gemelli_di_Moradin.md`. Corretta la
Benedizione della Forgia, **permanente** (DM 2026-07-04), che la pagina dava «fino al completamento
dell'avventura». Le pagine per gli stadi 0, 1 e 3 sono il lotto T10-c.

**La cartella meglio organizzata del repo** (benchmark per le altre):
file numerati che raccontano la progressione, un file = uno stadio.

| File | Ruolo | Stato |
|---|---|---|
| `00_Cintura_della_Devastazione.md` | oggetto custom D17 (slot cintura) | ⭐ MASTER |
| `01_Bracieri_Gemelli_di_Moradin.md` | l'artefatto, lore + struttura | ⭐ MASTER |
| `02_Risveglio_Bracieri_di_Moradin.md` | stadio Fuoco (giocato ✅) | *annesso-stadio* |
| `03_Risveglio_Completo_Bracieri_Terra.md` | stadio Terra (giocato ✅) | *annesso-stadio* |
| `04_..._Scheda_PG_Fuoco.md/html` | HANDOUT giocatore (Fuoco) | superato dallo stadio Terra |
| `05_..._Scheda_PG_Completa.md` (+ `.html` canonico) | HANDOUT giocatore attuale | ⭐ HANDOUT — allineato al formato STATO-ATTUALE + registro sblocchi (**T7** 2026-07-04) |
| `05_..._Scheda_PG_Completa Final.html`, `05_..._Scheda_PG_Completa copy 2.html` | copie duplicate dell'HANDOUT | 📸 deprecate (T6a: banner in testa, non cancellate) |
| `apply_styles.py`, `rewrite_table.py`, `generate_therysol.py`, `b64_20pct.txt` | tooling locale usa-e-getta (path hardcoded) | 📸 marcato in T6a — vedi `README-tooling-locale.md` nella stessa cartella |

## 5. COLLANA DEI SEMI ETERNI (Hella)

**⭐ MASTER DM**: `Artefatti-Pg/Hella/01_Collana_dei_Semi_Eterni.md` (creata in
ARC-07 B9; file combinato player+DM, ora la parte DM). **⭐ HANDOUT giocatore**
(estratto in **T7** 2026-07-04): `Artefatti-Pg/Hella/00_Collana-SCHEDA-GIOCATORE-STATO-ATTUALE.md`
(2 snapshot: Radicata attuale / stati futuri ARC-09 gated). ⚠️ La scheda dice
"forgiatura imminente" (tavolo, corretto); state.md §6 la dà "Active
post-resurrection" (stato preparato): vedi [T4-a]. Gli **slot-dono del party
(3)** si legano al ramo del rifiuto del P3B §2-BIS.

**⭐ PAGINE stampabili** (2026-09-25), nella famiglia di `02_Corona_2_Gemme.html`
(blocchi di potere, riga meccanica, leggenda, versione giocatore e versione DM):

| File | Per chi |
|---|---|
| `Artefatti-Pg/Hella/01_Collana_Radicata.html` | la giocatrice |
| `Artefatti-Pg/Hella/01_Collana_Radicata_DM.html` | il DM: lore da rivelare, ramo del rifiuto, scheda tecnica, la Quaternità, stati futuri |
| `Artefatti-Pg/Hella/02_Durik_Guardiano_di_Pietra.html` | la giocatrice: Durik vive nel terzo seme, e la sua pagina sta accanto a quella della Collana |
| `Artefatti-Pg/Hella/02_Durik_Guardiano_di_Pietra_DM.html` | il DM: quando assegnare le Prove di Risonanza, perché ha questo aspetto, come non usarlo |

L'immagine della Collana è `collana-dei-semi-eterni.jpg` (Canva AI, provenienza in
`PROVENIENZA.txt`); quella di Durik è `PG/Immagini/web/DurikFront2.jpg`. I poteri vengono
dai fogli consegnati alla serata della resurrezione (`09-SCHEDA-HELLA-RISORTA.md`,
`08-SCHEDA-DURIK.md`). Il PDF si esporta dalla pagina (Chromium, «Stampa»); non è nel repo.

L'handout `00_…` della Collana ora è solo un rimando a queste pagine. Il lore del master
DM è allineato a `DEF-3` (i semi sul corpo, un dono per seme, l'Impronta di Durik nel
terzo). Decisioni del DM del 2026-09-25, scritte nelle pagine, nel master, nelle
sinergie e nella skill di campagna: al massimo due Treant, e insieme spengono
l'Evocazione per un mese; tipi dei poteri (Sop, i due doni nel corpo Str, il Rovo Mag);
la scheda tecnica è canone; F1-F4 sono canone, F1 e F4 chiuse finché non si gioca la
loro condizione. Chiusi anche gli ultimi tre punti: la Collana funziona sempre, anche in
forma selvatica; i semi tornano all'alba; gli stati futuri hanno i momenti
canone e i poteri da scrivere in ARC-09.

## 6. SINERGIE (party)

**⭐ MASTER**: `PG/Artefatti/SINERGIE-ARTEFATTI-MASTER.md` (creato in T4 —
versionato, con sezione "sinergie future Collana/Hella" [PROPOSTA]).
`Artefatti-Pg/Sinergie_Artefatti_QuickReference.html` e
`07_.../SinergieArteFattiQuickReference.pdf` = 📸 export da rigenerare dal
master a ogni cambio (data-versione in testa).

## 7. Riferimenti trasversali

- `skills/rumblingstone-campaign/references/campaign-artifacts.md` —
  riferimento meccanico consolidato (inglese, per gli agent AI). ✅ Sezione
  Corona sincronizzata in **T6b** (2026-07-04): *Moradin's Insight* spostato
  in "Active Powers" (Rituale 2 completato), aggiunto il +2 intuizione CA di
  *Stone's Awareness*, corretti gli sblocchi (Mantle = Rituale 3; aggiunta
  *Aura of the Eternal Forge* = Rituale 4) per allinearli al master DM.
- `campaign/state.md` §6 — tabella "stato corrente" (vedi [T4-a]).
- Template per nuovi artefatti vivi:
  `campaign/templates/artefatto-vivo-template.md` (T4).

---

### [T4-a] Nota di coerenza temporale (per il DM)

`state.md` convive su **due tempi**: §0 (cruscotto) è al **tavolo reale**
(ARC-07 P4 in corso, solo Topazio acceso), mentre §1/§6 descrivono lo
**stato preparato** all'ingresso di ARC-09 (Hella risorta, 3 gemme, Rubino
speso). Non è un errore di questo file: è l'eredità del "written forward"
(piano ARC-08 A0). Regola pratica: **per il tavolo di stasera vale D8/D16**
(solo Topazio); per la prep di ARC-08/09 vale §6. ✅ **RISOLTO (T6c,
2026-07-04)**: il DM ha scelto la **doppia colonna** — state.md §6 ora ha
le colonne «Oggi al tavolo (ARC-07 P4)» e «Preparato (ingresso ARC-09)»
nella stessa tabella; l'ambiguità è chiusa.
