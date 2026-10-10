# Glossario bloccato e localizzazione

> **A cosa serve.** Fissare **una volta sola** come si scrive ogni nome proprio
> della campagna, e cosa succede a quel nome se un giorno esisterà un'edizione
> inglese. È il *loc kit* previsto da [ADR-0016](../plans/adr/ADR-0016-lingua-sorgente-e-edizioni.md):
> costa poco adesso, costa settimane a farlo dopo.
>
> **Regola d'uso**: se un nome è in questa tabella, si scrive **così** in ogni
> file nuovo. Se non c'è, aggiungilo tu la prima volta che lo inventi.

**Lingua sorgente: italiano** (ADR-0016). L'inglese in tabella è la resa
**prevista**, non un testo esistente: serve a impedire che fra due anni lo
stesso nome esca in tre modi diversi.

---

## 1. La regola dei nomi misti (perché non si uniforma)

Il repo mescola nomi inglesi e italiani, e **va bene così**: è Faerûn, dove il
Comune convive con le lingue razziali. La regola che ci sta sotto, resa
esplicita:

| Categoria | Lingua | Perché |
|---|---|---|
| **Nomi propri di persona e di luogo canonici FR** | come in FR | *Hammerfist*, *Rethmar*, *Dauth*: sono già canone di ambientazione |
| **Artefatti nominati in Comune** | inglese | *Aegis Fang* è un nome proprio, non una descrizione |
| **Artefatti nominati in nanico/descrittivi** | italiano | *Corona di Adamantio*, *Bracieri Gemelli di Moradin* |
| **Soprannomi e epiteti** | **italiano** | *Barbadiferro*, *Fuocospento*, *il Velato*, *Seta-Argento* — sono **parlanti**, e in italiano parlano |
| **Termini di regolamento** | italiano al tavolo | **CD** non DC, **TS**, **Lotta**, **azione veloce** |

⚠️ **Non uniformare i nomi esistenti.** Sono già in centinaia di file, nelle
mappe, nelle immagini e nelle schede dei giocatori. Il costo supera di molto il
beneficio estetico.

---

## 2. Personaggi giocanti

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Thorik | Thorik | invariato |
| Tordek Durinheart | Tordek Durinheart | invariato |
| Hella Oakenshield | Hella Oakenshield | invariato |
| Artemis | Artemis | invariato |
| Durik | Durik | compagno di Hella, **maschio** |

## 3. Artefatti

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Aegis Fang | Aegis Fang | **DNT** — già inglese |
| Corona di Adamantio | Crown of Adamantine | tradurre: è descrittivo |
| Ring of Chaotic Illumination | Ring of Chaotic Illumination | **DNT** — già inglese in tutte le schede |
| Bracieri Gemelli di Moradin | Twin Braziers of Moradin | tradurre |
| Collana dei Semi Eterni | Necklace of Eternal Seeds | tradurre |
| Cuore di Moradin | Heart of Moradin | tradurre |
| Cintura della Devastazione | Belt of Devastation | oggetto custom del PG (D17) |
| Smeraldo della Forza · Topazio del Tempo · Rubino della Leggenda | Emerald of Strength · Topaz of Time · Ruby of Legend | le tre gemme della Corona |
| Frequenza della Confusione | Frequency of Confusion | conoscenza, non oggetto |
| Diapason Armonico | Harmonic Tuning Fork | **speso** sulla Sentinella |
| Seme-Mercato (di Varis) | Market-Seed | innesto planare |

## 4. Antagonisti e PNG

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Terros l'Antico | Terros the Ancient | GS 15, **sconfitto** |
| Skullcrusher il Nero | Skullcrusher the Black | **DNT** sul nome |
| Fauci di Palude | Swamp Maw | drago nero, ARC-08 |
| Balvar Fuocospento | Balvar Quenchfire | *Fuocospento* è parlante: la resa deve restare parlante |
| Zog'tar Deatheye | Zog'tar Deatheye | **DNT** |
| Thorgrim Barbadiferro | Thorgrim Ironbeard | parlante |
| Re Thorek I / Re Thorek Hammerfist | King Thorek | |
| Durin Rocciadura | Durin Hardstone | parlante |
| Il Collezionista | The Collector | |
| Varis «Seta-Argento» | Varis "Silversilk" | parlante |
| Sethrax il Velato | Sethrax the Veiled | |
| Sonjak · Xal'thor · Zalkatar · Vatore · Therysol | invariati | **DNT** |
| Sentinella Silenziosa / di Mithral | Silent Sentinel | **sconfitta** |
| Madre Cristallo | Crystal Mother | |
| Custode delle Radici | Root Warden | psicopompo, ARC-07 #3 |

## 5. Luoghi e concetti della campagna

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Valle di Channath / Cannath Vale | Cannath Vale | equivalente dell'Elsir Vale |
| Palio di Channathgate | Palio of Channathgate | ⚠️ *Palio* **DNT**: è un prestito culturale, non si traduce |
| Hammerfist Holds | Hammerfist Holds | **DNT** |
| Rethmar · Dauth · Drellin's Ferry | invariati | **DNT** |
| Sala della Forgia Eterna | Hall of the Eternal Forge | |
| Portale della Forgia Eterna | Portal of the Eternal Forge | titolo dell'ARC-07 |
| Stanza della Corona | Crown Chamber | |
| Tempio di Mithral | Mithral Temple | |
| Oceano di Roccia | Ocean of Stone | Piano della Terra |
| Incudine del Mondo | Anvil of the World | anche l'epiteto di Terros |
| La Cronaca Vivente · «La Forgia Ricorda» | The Living Chronicle · "The Forge Remembers" | |
| Trinità Divina | Divine Trinity | sinergia S4 |
| Colpo dell'Alba Oscura | Dark Dawn Strike | sinergia S3 |
| Orologio di Hammerfist | Hammerfist Clock | il countdown |
| Custodi Eterni · Cerimonia delle 100 Asce | Eternal Wardens · Ceremony of the Hundred Axes | ARC-08 |

## 6. Lista «non tradurre» (DNT) — categorie

Oltre alle voci marcate DNT sopra, **non si traducono mai**:

1. **Nomi di divinità**: Moradin, Abbathor, Lathander, Mask, Shar, Tiamat.
2. **Nomi propri di persona** senza componente descrittiva.
3. **Toponimi canonici dei Forgotten Realms.**
4. **Nomi di incantesimi 3.5**, che restano in inglese corsivo anche nel testo
   italiano: *black tentacles*, *dispel magic*, *righteous might*. È già la
   prassi del repo e va mantenuta.
5. **Sigle di sistema** nei file tecnici: CR, HD, DR, SR. *(Nel testo da tavolo
   valgono invece gli equivalenti italiani — vedi §1.)*

## 7. Quando aggiungi un nome nuovo

Tre domande, in ordine:

1. **È parlante?** (*Fuocospento*, *Barbadiferro*, *il Velato*) → **italiano**,
   e annota accanto una resa inglese che resti parlante.
2. **È un nome proprio secco?** → come viene, e finisce in **DNT**.
3. **È canone FR?** → esattamente come in FR, mai reinventato.

Poi aggiungilo qui. La riga costa dieci secondi; ritrovarsi lo stesso PNG con
tre grafie costa una giornata di *grep*.

## 8. Forme escluse — il foglio di stile che si esegue

> **Cos'è.** Ogni redazione professionale tiene un *foglio di stile*: l'elenco
> delle decisioni di grafia e di termine prese una volta, perché il copyeditor
> e il correttore di bozze non le riprendano da capo a ogni pagina. WotC lo
> fissa nella sua guida di casa («mithral», non «mithril»); Paizo lo affida a
> chi cura il testo. Qui il foglio è questa tabella, e **`python3
> scripts/validate_prosa.py` la legge**: non c'è un secondo elenco da
> tenere in sincronia ([ADR-0078](../plans/adr/ADR-0078-il-foglio-di-stile-si-esegue.md)).
>
> **Stato**, una parola per riga:
>
> | Stato | Cosa succede |
> |---|---|
> | `refuso` | la decisione è presa: ogni occorrenza è un rilievo di `terminologia_non_canonica` (maggiore) |
> | `DM?` | due grafie convivono e **la scelta è del DM**: non è un rilievo, ma `--foglio` le conta e le elenca finché non decide. Oggi nessuna riga è in questo stato |
>
> **Come si aggiunge una riga.** Prima si guarda il contesto: una forma può
> essere un altro PNG (*Garruk* non è *Karruk*), un nome di file
> (`Myconoid.webp`) o la citazione di una fonte. Una forma che ha un uso
> legittimo non entra come `refuso`. La riga che spiega il cambio («*mithril* →
> *mithral*») non è un rilievo: il controllo salta le righe che contengono la
> forma canonica o una freccia.

| Forma esclusa | Forma canonica | Stato | Perché |
|---|---|---|---|
| `Regiarax` | Regiarix | refuso | il nome del boss di RHoD è *Regiarix*; la correzione era già stata fatta una volta (`state-changelog.md`) e una citazione di fonte era rimasta |
| `mithril` | mithral | refuso | in 3.5 il metallo si scrive *mithral* (SRD); *mithril* è la grafia di Tolkien. Il repo scrive *mithral* nel resto dei file e WotC lo prescrive nella guida di casa |
| `Hellas` | Hella | refuso | decisione del DM, 2026-10-03: il PG si chiama *Hella* (§2). Un nome di file o di cartella che contiene *Hellas* non è una grafia e resta com'è finché il file non si rinomina |
| `Cannathgate` | Channathgate | refuso | decisione del DM, 2026-10-03: la città è *Channathgate*, come il *Palio di Channathgate* (§5). *Cannath Vale* resta com'è |
| `Therisol` | Therysol | refuso | decisione del DM, 2026-10-03: il glossario (§4) dice *Therysol* |
| `azione rapida` | azione veloce | refuso | decisione del DM, 2026-10-03: *swift action* si rende *azione veloce*, come nelle traduzioni e nelle regole italiane di comunità del 3.5 e come dice il §1 |

> **Fuori dalla tabella, di proposito.** *DC* → *CD* è già un divieto di
> `validate_modules.py` (`BANNED`) e di `validate_standalone.py`: una norma, un
> rilevatore. Lo stesso per il riposo breve e lungo.
